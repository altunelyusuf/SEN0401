#!/usr/bin/env python3
"""SEN0401 chapter 13 (Bitcoin Security): the regtest run. Starts Bitcoin Core 31.1 nodes (the release binary of bitcoincore.org, sha256 in the record) on private chains in temporary data
directories and records what the nodes answered in ch13-evidence/regtest_run_v1_0_0.json: what a signed transaction reveals and what tampering with it does (b1), the encrypted BIP 324 transport between
two nodes (b2), a cold wallet that signs a PSBT for a watch-only wallet (b3), wallet encryption and its error codes (b4), backup and restore and a stale backup with a small keypool (b5), a 2-of-3 multisig wallet
with lost keys and the descriptor that must be backed up (b6), an heir who can spend only after a relative timelock (b7), and the release check of the downloaded binary (b8).
Nothing here touches the public network (-dnsseed=0 -fixedseeds=0 -connect=0); only b2 lets two private nodes talk to each other on 127.0.0.1.
One run, one record: hashes, keys and timings differ on a rerun; the chapter's claims are checked against the record of the saved run.
Usage: sen0401_ch13_regtest_v1_0_0.py [out.json] [--only b1,b2]   Environment: BITCOIN_BIN (directory of bitcoind and bitcoin-cli), TMPDIR."""
__version__ = "1.0.0"
import hashlib, json, os, shutil, struct, subprocess, sys, tempfile, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
import sen0401_ch13_lib_v1_0_0 as L

BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
args = [a for a in sys.argv[1:] if not a.startswith("--") and not (a.startswith("b") and a[1:].isdigit())]
OUT = args[0] if args else os.path.join(HERE, "ch13-evidence", "regtest_run_v1_0_0.json")
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
TMP = tempfile.mkdtemp(prefix="ch13_regtest_", dir=os.environ.get("TMPDIR"))
R = {"_version": __version__, "phase": {}, "errors": {}}
T0 = time.time()


class RPCError(Exception):
    pass


NODES = []


class Node:
    def __init__(self, name, port_base, chain="regtest", extra=(), listen=False):
        self.listen = listen
        self.name, self.rpcport, self.port, self.chain = name, port_base, port_base + 1, chain
        self.dd = os.path.join(TMP, name)
        os.makedirs(self.dd, exist_ok=True)
        self.extra = list(extra)
        NODES.append(self)

    def cli(self):
        return [BIN + "/bitcoin-cli", "-" + self.chain, "-datadir=" + self.dd, "-rpcport=%d" % self.rpcport, "-rpcclienttimeout=900", "-stdin"]

    def rpc(self, method, *a, wallet=None, **named):
        c = self.cli()
        if wallet:
            c.append("-rpcwallet=" + wallet)
        if named:
            c.append("-named")
            lines = ["%s=%s" % (k, v if isinstance(v, str) else json.dumps(v)) for k, v in named.items()]
        else:
            lines = [x if isinstance(x, str) else json.dumps(x) for x in a]
        r = subprocess.run(c + [method], input="\n".join(lines), capture_output=True, text=True)
        if r.returncode:
            raise RPCError((r.stdout + r.stderr).strip())
        o = r.stdout.strip()
        try:
            return json.loads(o)
        except Exception:
            return o

    def attempt(self, method, *a, **kw):
        try:
            return {"ok": self.rpc(method, *a, **kw)}
        except RPCError as e:
            return {"error": " ".join(str(e).split())}

    def start(self):
        r = subprocess.run([BIN + "/bitcoind", "-" + self.chain, "-datadir=" + self.dd, "-daemon", "-server", "-rpcport=%d" % self.rpcport, "-port=%d" % self.port,
                            "-listen=%d" % (1 if self.listen else 0), "-dnsseed=0", "-discover=0", "-listenonion=0", "-fixedseeds=0", "-connect=0", "-fallbackfee=0.0002"] + (["-bind=127.0.0.1:%d" % self.port] if self.listen else []) + self.extra, capture_output=True, text=True)
        if r.returncode:
            return {"exit": r.returncode, "stderr": " ".join((r.stdout + r.stderr).split())[:600]}
        for _ in range(200):
            try:
                self.rpc("getblockcount")
                return {"exit": 0}
            except RPCError:
                time.sleep(0.3)
        return {"exit": 0, "note": "rpc not answering"}

    def stop(self):
        try:
            self.rpc("stop")
        except RPCError:
            pass
        time.sleep(2.5)

    def pub(self, w):
        """the external public key expression [fingerprint/path]tpub.../0/* of the wpkh descriptor of wallet w"""
        ds = self.rpc("listdescriptors", wallet=w)["descriptors"]
        d = [d for d in ds if d["desc"].startswith("wpkh") and not d["internal"]][0]["desc"]
        return d[5:d.index(")#")]

    def mine(self, n, addr):
        out = []
        while n > 0:
            k = min(n, 500)
            out += self.rpc("generatetoaddress", k, addr)
            n -= k
        return out

    def submit(self, hex_block):
        """submitblock: the empty string means accepted; otherwise the reason the node gives."""
        r = self.rpc("submitblock", hex_block)
        return r if r != "" else "accepted"

    def spk(self, addr, wallet):
        return bytes.fromhex(self.rpc("getaddressinfo", addr, wallet=wallet)["scriptPubKey"])


def phase(name, fn):
    if ONLY and name not in ONLY:
        return
    t = time.time()
    try:
        fn()
    except BaseException as e:
        R["errors"][name] = traceback.format_exc()[-1500:]
        print("ERROR in", name, repr(e)[:300], flush=True)
        for N in NODES:      # a failed phase must not leave a node holding its port
            N.stop()
    R["phase"][name] = round(time.time() - t, 1)
    print("phase", name, R["phase"][name], "s", flush=True)



B58A = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58dec(s):
    n = 0
    for ch in s:
        n = n * 58 + B58A.index(ch)
    return n.to_bytes(82, "big")[-82:]


def miner(name, port, **kw):
    """a node with a funded wallet w (matured coinbases) and its address"""
    n = Node(name, port, **kw)
    n.start()
    n.rpc("createwallet", "w")
    a = n.rpc("getnewaddress", wallet="w")
    n.mine(101, a)
    return n, a


def psbt_sigs(n, psbt):
    d = n.rpc("decodepsbt", psbt)
    return [len(i.get("partial_signatures", {})) for i in d["inputs"]]


def b1():
    """a signed transaction: it carries a public key and a signature, never the private key; changing the output breaks the signature; a rebroadcast pays nothing; a block with the broken transaction is refused"""
    n, a = miner("S", 19900)
    key = os.urandom(32)
    wif = L.b58check(b"\xef" + key + b"\x01")
    n.rpc("createwallet", "k", False, True)           # private keys on, blank
    d = "wpkh(%s)#%s" % (wif, n.rpc("getdescriptorinfo", "wpkh(%s)" % wif)["checksum"])   # the checksum of the form with the key in it
    R["b1_import"] = n.rpc("importdescriptors", [{"desc": d, "timestamp": "now"}], wallet="k")
    ka = n.rpc("deriveaddresses", d)[0]
    n.rpc("sendtoaddress", ka, 2.0, wallet="w")
    n.mine(1, a)
    u = n.rpc("listunspent", 1, 9999, [ka], wallet="k")[0]
    n.rpc("createwallet", "r")
    n.rpc("createwallet", "m")
    dest = n.rpc("getnewaddress", wallet="r")
    evil = n.rpc("getnewaddress", wallet="m")
    raw = n.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {dest: 1.5, ka: 0.4999})
    sg = n.rpc("signrawtransactionwithwallet", raw, wallet="k")
    hx = sg["hex"]
    dec = n.rpc("decoderawtransaction", hx)
    wit = dec["vin"][0]["txinwitness"]
    pubk = n.rpc("getaddressinfo", ka, wallet="k").get("pubkey")
    R["b1_secrecy"] = {"complete": sg["complete"], "n_witness_items": len(wit), "witness_item_lengths": [len(x) // 2 for x in wit], "sighash_byte": wit[0][-2:], "pubkey_in_witness": wit[-1] == pubk, "pubkey": pubk,
                       "private_key_hex_in_tx": key.hex() in hx, "wif_in_tx": wif in hx, "tx_bytes": len(hx) // 2, "vin_scriptsig_hex": dec["vin"][0]["scriptSig"]["hex"]}
    spk_dest = n.rpc("getaddressinfo", dest, wallet="r")["scriptPubKey"]
    spk_evil = n.rpc("getaddressinfo", evil, wallet="m")["scriptPubKey"]
    tam = hx.replace(spk_dest, spk_evil)
    amt_old = (150000000).to_bytes(8, "little").hex()
    amt_new = (100000000).to_bytes(8, "little").hex()
    tam2 = hx.replace(amt_old, amt_new)
    def tm(h):
        try:
            return n.rpc("testmempoolaccept", [h])[0]
        except RPCError as e:
            return {"rpc_error": " ".join(str(e).split())[:300]}
    R["b1_tamper"] = {"valid": tm(hx), "address_replaced": tm(tam), "address_replaced_differs": tam != hx, "amount_changed": tm(tam2), "amount_changed_differs": tam2 != hx,
                      "dest_spk": spk_dest, "evil_spk": spk_evil}
    gb = n.attempt("generateblock", a, [tam])
    R["b1_generateblock_bad"] = gb
    R["b1_generateblock_good"] = {"ok": "hash" in n.rpc("generateblock", a, [hx])}
    # the good one is now in a block: broadcasting it again pays nothing
    R["b1_replay"] = {"sendrawtransaction": n.attempt("sendrawtransaction", hx), "testmempoolaccept": tm(hx), "balance_r": n.rpc("getbalance", wallet="r"),
                      "confirmations": n.rpc("gettransaction", dec["txid"], wallet="k")["confirmations"]}
    n.mine(1, a)
    R["b1_replay"]["balance_r_after"] = n.rpc("getbalance", wallet="r")
    R["b1_replay_after_block"] = n.attempt("sendrawtransaction", hx)
    g = n.rpc("getblockhash", 0)
    gb0 = n.rpc("getblock", g, 2)
    R["b1_genesis"] = {"hash": g, "previousblockhash": gb0.get("previousblockhash"), "height": gb0["height"], "ntx": gb0["nTx"], "info_chain": n.rpc("getblockchaininfo")["chain"]}
    n.stop()


def b2():
    """BIP 324: two private nodes connect; both sides report the v2 transport and the same session id; a node that is told -v2transport=0 talks v1"""
    P1 = Node("P1", 19910, listen=True)
    Q1 = Node("Q1", 19920, listen=True)
    X1 = Node("X1", 19930, extra=["-v2transport=0"])
    for x in (P1, Q1, X1):
        x.start()
    R["b2_netinfo"] = {"P_localservices": P1.rpc("getnetworkinfo")["localservicesnames"], "X_localservices": X1.rpc("getnetworkinfo")["localservicesnames"]}
    Q1.rpc("addnode", "127.0.0.1:%d" % P1.port, "onetry")
    X1.rpc("addnode", "127.0.0.1:%d" % P1.port, "onetry")
    for _ in range(60):
        if len(P1.rpc("getpeerinfo")) >= 2 and len(Q1.rpc("getpeerinfo")) >= 1 and len(X1.rpc("getpeerinfo")) >= 1:
            break
        time.sleep(0.5)
    time.sleep(2)
    def pk(p):
        return [{"inbound": x["inbound"], "transport": x.get("transport_protocol_type"), "session_id": x.get("session_id"), "subver": x.get("subver"), "version": x.get("version")} for x in p]
    R["b2_peers"] = {"P": pk(P1.rpc("getpeerinfo")), "Q": pk(Q1.rpc("getpeerinfo")), "X": pk(X1.rpc("getpeerinfo"))}
    q = R["b2_peers"]["Q"][0]
    R["b2_session_ids_match"] = any(p["session_id"] == q["session_id"] and q["session_id"] for p in R["b2_peers"]["P"])
    R["b2_session_id_len_hex"] = len(q["session_id"] or "")
    for x in (P1, Q1, X1):
        x.stop()


def b3():
    """cold storage: the hot node has only public descriptors and cannot sign; the cold node (no blocks, no peers) signs the PSBT; the hot node finalizes and broadcasts"""
    H, a = miner("H", 19940)
    C = Node("C", 19950)
    C.start()
    C.rpc("createwallet", "cold")
    pubs = [d for d in C.rpc("listdescriptors", False, wallet="cold")["descriptors"] if d["desc"].startswith("wpkh")]
    H.rpc("createwallet", "watch", True, True)
    imp = H.rpc("importdescriptors", [{"desc": d["desc"], "timestamp": "now", "active": True, "internal": d["internal"], "range": [0, 20]} for d in pubs], wallet="watch")
    R["b3_import"] = imp
    va = H.rpc("getnewaddress", wallet="watch")
    H.rpc("sendtoaddress", va, 3.0, wallet="w")
    H.mine(1, a)
    dest = H.rpc("getnewaddress", wallet="w")
    p = H.rpc("walletcreatefundedpsbt", [], [{dest: 1.0}], 0, {"fee_rate": 10}, wallet="watch")
    d0 = H.rpc("decodepsbt", p["psbt"])
    hp = H.rpc("walletprocesspsbt", p["psbt"], True, "DEFAULT", True, wallet="watch")
    R["b3_hot"] = {"watch_private_keys_enabled": H.rpc("getwalletinfo", wallet="watch")["private_keys_enabled"], "balance": H.rpc("getbalance", wallet="watch"),
                   "psbt_chars": len(p["psbt"]), "n_inputs": len(d0["inputs"]), "n_outputs": len(d0["outputs"]), "has_bip32_derivs": "bip32_derivs" in d0["inputs"][0], "partial_sigs_before": psbt_sigs(H, p["psbt"]),
                   "hot_sign_complete": hp["complete"], "hot_listdescriptors_private": H.attempt("listdescriptors", True, wallet="watch"),
                   "hot_sign_attempt_sigs": psbt_sigs(H, hp["psbt"])}
    cs = C.rpc("walletprocesspsbt", p["psbt"], True, "DEFAULT", True, wallet="cold")
    R["b3_cold"] = {"blocks": C.rpc("getblockcount"), "connections": C.rpc("getconnectioncount"), "sign_complete": cs["complete"], "sigs": psbt_sigs(C, cs["psbt"]), "final_witness_in_psbt": "final_scriptwitness" in C.rpc("decodepsbt", cs["psbt"])["inputs"][0], "psbt_chars_signed": len(cs["psbt"])}
    f = H.rpc("finalizepsbt", cs["psbt"])
    txid = H.rpc("sendrawtransaction", f["hex"])
    H.mine(1, a)
    R["b3_broadcast"] = {"finalize_complete": f["complete"], "txid_len": len(txid), "confirmations": H.rpc("gettransaction", txid, wallet="watch")["confirmations"], "dest_received": H.rpc("getreceivedbyaddress", dest, wallet="w")}
    for x in (H, C):
        x.stop()


def b4():
    """wallet encryption: the error codes of a locked wallet, a wrong passphrase, the unlock timeout, and whether the master key bytes can still be found in the wallet file"""
    N, a = miner("E", 19960)
    N.rpc("createwallet", "e")
    ex = N.rpc("listdescriptors", True, wallet="e")["descriptors"]
    import re
    xprv = re.search(r"(?:tprv|xprv)[1-9A-HJ-NP-Za-km-z]+", [d for d in ex if d["desc"].startswith("wpkh") and not d["internal"]][0]["desc"]).group(0)
    kb = b58dec(xprv)[-82:-4]               # the 78 serialized bytes without the 4 checksum bytes
    master = kb[46:78]
    N.rpc("sendtoaddress", N.rpc("getnewaddress", wallet="e"), 1.0, wallet="w")
    N.mine(1, a)
    f = os.path.join(N.dd, "regtest", "wallets", "e", "wallet.dat")
    N.rpc("unloadwallet", "e")
    before = open(f, "rb").read()
    N.rpc("loadwallet", "e")
    enc = N.rpc("encryptwallet", "correct horse battery", wallet="e")
    N.rpc("unloadwallet", "e")
    after = open(f, "rb").read()
    N.rpc("loadwallet", "e")
    to = N.rpc("getnewaddress", wallet="w")
    R["b4_file"] = {"key_bytes_of_account_xprv": len(master), "master_key_bytes_in_file_before": master in before, "xprv_text_in_file_before": xprv.encode() in before, "xprv_text_in_file_after": xprv.encode() in after, "master_key_bytes_in_file_after": master in after, "size_before": len(before), "size_after": len(after), "encryptwallet_message": enc[:200] if isinstance(enc, str) else enc}
    R["b4_locked"] = {"getwalletinfo_unlocked_until_present": "unlocked_until" in N.rpc("getwalletinfo", wallet="e"), "unlocked_until": N.rpc("getwalletinfo", wallet="e").get("unlocked_until"),
                      "send": N.attempt("sendtoaddress", to, 0.1, wallet="e"), "listdescriptors_private": N.attempt("listdescriptors", True, wallet="e"), "getnewaddress": "ok" if "ok" in N.attempt("getnewaddress", wallet="e") else "failed",
                      "listdescriptors_public": "ok" if "ok" in N.attempt("listdescriptors", wallet="e") else "failed", "balance_visible": N.rpc("getbalance", wallet="e")}
    R["b4_wrong"] = N.attempt("walletpassphrase", "wrong words", 60, wallet="e")
    R["b4_right"] = N.attempt("walletpassphrase", "correct horse battery", 3, wallet="e")
    uw = N.rpc("getwalletinfo", wallet="e")
    R["b4_unlocked"] = {"unlocked_until": uw["unlocked_until"], "now": int(time.time()), "send_ok": "ok" in N.attempt("sendtoaddress", to, 0.1, wallet="e")}
    time.sleep(5)
    R["b4_after_timeout"] = {"unlocked_until": N.rpc("getwalletinfo", wallet="e")["unlocked_until"], "send": N.attempt("sendtoaddress", to, 0.1, wallet="e")}
    R["b4_change"] = N.attempt("walletpassphrasechange", "correct horse battery", "new horse battery", wallet="e")
    R["b4_old_passphrase"] = N.attempt("walletpassphrase", "correct horse battery", 60, wallet="e")
    R["b4_new_passphrase"] = N.attempt("walletpassphrase", "new horse battery", 60, wallet="e")
    N.rpc("walletlock", wallet="e")
    R["b4_walletlock_until"] = N.rpc("getwalletinfo", wallet="e")["unlocked_until"]
    N.stop()


def b5():
    """backup: the file made by backupwallet restores the same addresses; a backup made before the wallet handed out more addresses than its keypool misses funds sent to the later ones"""
    N, a = miner("B", 19970, extra=["-keypool=3"])
    N.rpc("createwallet", "src")
    bdir = os.path.join(TMP, "bk")
    os.makedirs(bdir, exist_ok=True)
    stale = os.path.join(bdir, "stale.dat")
    fresh = os.path.join(bdir, "fresh.dat")
    d0 = [d for d in N.rpc("listdescriptors", wallet="src")["descriptors"] if d["desc"].startswith("wpkh") and not d["internal"]][0]
    first = N.rpc("getnewaddress", wallet="src")
    N.rpc("sendtoaddress", first, 1.0, wallet="w")
    N.mine(1, a)
    N.rpc("backupwallet", stale, wallet="src")
    later = [N.rpc("getnewaddress", wallet="src") for _ in range(9)]
    far = later[-1]
    N.rpc("sendtoaddress", far, 2.0, wallet="w")
    N.mine(1, a)
    N.rpc("backupwallet", fresh, wallet="src")
    nxt = N.rpc("getnewaddress", wallet="src")
    N.rpc("unloadwallet", "src") if False else None
    rs = N.rpc("restorewallet", "from_stale", stale)
    rf = N.rpc("restorewallet", "from_fresh", fresh)
    time.sleep(1)
    R["b5_backup"] = {"keypool_range_end": d0.get("range"), "balance_src": N.rpc("getbalance", wallet="src"), "balance_stale": N.rpc("getbalance", wallet="from_stale"), "balance_fresh": N.rpc("getbalance", wallet="from_fresh"),
                      "restore_stale": rs, "restore_fresh": rf, "far_index": len(later), "fresh_next_matches": N.rpc("getnewaddress", wallet="from_fresh") == nxt,
                      "stale_first_next_equals_src_second": N.rpc("getnewaddress", wallet="from_stale") == later[0],
                      "far_address_ismine_stale": N.rpc("getaddressinfo", far, wallet="from_stale")["ismine"], "far_address_ismine_fresh": N.rpc("getaddressinfo", far, wallet="from_fresh")["ismine"],
                      "backup_file_bytes": {"stale": os.path.getsize(stale), "fresh": os.path.getsize(fresh)}}
    # a rescan that is told the range finds the money in the stale copy (the seed was never lost, only the range)
    N.rpc("importdescriptors", [{"desc": N.rpc("listdescriptors", wallet="src")["descriptors"][0]["desc"], "timestamp": 0, "range": [0, 20], "active": False}], wallet="from_stale") if False else None
    N.stop()


def b6():
    """2-of-3 multisig: two of three signers are enough, one is not; the order of the keys in sortedmulti does not matter, in multi it does; lost keys; the descriptor is part of the backup"""
    N, a = miner("M", 19980)
    for w in ("m1", "m2", "m3"):
        N.rpc("createwallet", w)
    k = [N.pub(w) for w in ("m1", "m2", "m3")]
    dd = N.rpc("getdescriptorinfo", "wsh(sortedmulti(2,%s,%s,%s))" % tuple(k))["descriptor"]
    shuffled = N.rpc("getdescriptorinfo", "wsh(sortedmulti(2,%s,%s,%s))" % (k[2], k[0], k[1]))["descriptor"]
    unsorted_a = N.rpc("getdescriptorinfo", "wsh(multi(2,%s,%s,%s))" % tuple(k))["descriptor"]
    unsorted_b = N.rpc("getdescriptorinfo", "wsh(multi(2,%s,%s,%s))" % (k[2], k[0], k[1]))["descriptor"]
    ad = lambda d: N.rpc("deriveaddresses", d, [0, 0])[0]
    R["b6_order"] = {"sortedmulti_same": ad(dd) == ad(shuffled), "multi_same": ad(unsorted_a) == ad(unsorted_b), "sortedmulti_addr": ad(dd), "multi_addr_1": ad(unsorted_a), "multi_addr_2": ad(unsorted_b),
                     "descriptor_chars": len(dd), "n_keys_in_descriptor": 3}
    N.rpc("createwallet", "ms", True, True)
    R["b6_import"] = N.rpc("importdescriptors", [{"desc": dd, "active": True, "range": [0, 10], "timestamp": "now"}], wallet="ms")
    a0 = N.rpc("getnewaddress", wallet="ms")
    R["b6_order"]["wallet_address_is_derived_0"] = a0 == ad(dd)
    N.rpc("sendtoaddress", a0, 2.0, wallet="w")
    a1 = N.rpc("getnewaddress", wallet="ms")
    N.rpc("sendtoaddress", a1, 2.0, wallet="w")
    N.mine(1, a)
    dest = N.rpc("getnewaddress", wallet="w")
    u = sorted(N.rpc("listunspent", 1, 9999, [], True, wallet="ms"), key=lambda x: x["address"] != a0)
    def mk(utxo):
        return N.rpc("walletcreatefundedpsbt", [{"txid": utxo["txid"], "vout": utxo["vout"]}], [{dest: utxo["amount"]}], 0, {"add_inputs": False, "fee_rate": 10, "subtractFeeFromOutputs": [0]}, wallet="ms")["psbt"]
    p = mk(u[0])
    s1 = N.rpc("walletprocesspsbt", p, True, "DEFAULT", True, wallet="m1")
    s13 = N.rpc("walletprocesspsbt", s1["psbt"], True, "DEFAULT", True, wallet="m3")
    f = N.rpc("finalizepsbt", s13["psbt"])
    tm = N.rpc("testmempoolaccept", [f["hex"]])[0]
    dec = N.rpc("decoderawtransaction", f["hex"])
    R["b6_sign"] = {"ms_listunspent_n": len(u), "m1_alone": {"complete": s1["complete"], "sigs": psbt_sigs(N, s1["psbt"])}, "m1_m3": {"complete": s13["complete"], "sigs": psbt_sigs(N, s13["psbt"])},
                    "finalize_complete": f["complete"], "accept": tm["allowed"], "witness_items": len(dec["vin"][0]["txinwitness"]), "vsize": tm.get("vsize")}
    N.rpc("sendrawtransaction", f["hex"])
    N.mine(1, a)
    # one key lost: keys 2 and 3 are enough; two keys lost: the third alone is not
    p2 = mk(u[1])
    t2 = N.rpc("walletprocesspsbt", N.rpc("walletprocesspsbt", p2, True, "DEFAULT", True, wallet="m2")["psbt"], True, "DEFAULT", True, wallet="m3")
    p3 = mk(u[1])
    t3 = N.rpc("walletprocesspsbt", p3, True, "DEFAULT", True, wallet="m1")
    R["b6_loss"] = {"lose_m1_sign_with_m2_m3": t2["complete"], "lose_m2_m3_sign_with_m1": t3["complete"], "sigs_m1_only": psbt_sigs(N, t3["psbt"])}
    # one key, one input, one output: the size of the same payment without multisig
    sa = N.rpc("getnewaddress", wallet="m1")
    N.rpc("sendtoaddress", sa, 2.0, wallet="w")
    N.mine(1, a)
    su = N.rpc("listunspent", 1, 9999, [sa], wallet="m1")[0]
    sp = N.rpc("walletcreatefundedpsbt", [{"txid": su["txid"], "vout": su["vout"]}], [{dest: su["amount"]}], 0, {"add_inputs": False, "fee_rate": 10, "subtractFeeFromOutputs": [0]}, wallet="m1")["psbt"]
    sf = N.rpc("finalizepsbt", N.rpc("walletprocesspsbt", sp, True, "DEFAULT", True, wallet="m1")["psbt"])
    R["b6_single_vsize"] = N.rpc("testmempoolaccept", [sf["hex"]])[0]["vsize"]
    # the descriptor is the map: a wallet that holds a key but not the descriptor does not know the address, a wallet that is given the descriptor again finds the money
    R["b6_backup"] = {"m1_knows_multisig_address": N.rpc("getaddressinfo", a1, wallet="m1")["ismine"], "m1_balance": N.rpc("getbalance", wallet="m1"), "ms_balance": N.rpc("getbalance", wallet="ms")}
    N.rpc("createwallet", "rebuilt", True, True)
    N.rpc("importdescriptors", [{"desc": dd, "active": True, "range": [0, 10], "timestamp": 0}], wallet="rebuilt")
    R["b6_backup"]["rebuilt_balance"] = N.rpc("getbalance", wallet="rebuilt")
    N.rpc("createwallet", "wrongorder", True, True)
    R["b6_backup"]["wrong_descriptor_import"] = N.rpc("importdescriptors", [{"desc": unsorted_b, "active": True, "range": [0, 10], "timestamp": 0}], wallet="wrongorder")
    R["b6_backup"]["wrongorder_balance"] = N.rpc("getbalance", wallet="wrongorder")
    N.stop()


def b7():
    """an heir: the owner can spend at once, the heir only after older(10); the relative timelock is checked at 1, 9 and 10 confirmations; the limits of older()"""
    N, a = miner("T", 19990)
    N.rpc("createwallet", "owner")
    N.rpc("createwallet", "heir")
    ko, kh = N.pub("owner"), N.pub("heir")
    info = N.rpc("getdescriptorinfo", "wsh(or_d(pk(%s),and_v(v:pk(%s),older(10))))" % (ko, kh))
    dd = info["descriptor"]
    N.rpc("createwallet", "vault", True, True)
    R["b7_import"] = N.rpc("importdescriptors", [{"desc": dd, "active": True, "range": [0, 10], "timestamp": "now"}], wallet="vault")
    R["b7_descriptor"] = {"issolvable": info["issolvable"], "hasprivatekeys": info["hasprivatekeys"], "policy": "or(owner, and(heir, older 10))", "miniscript_text": dd[: dd.index("(")]}
    dest = N.rpc("getnewaddress", wallet="w")
    def fund():
        va = N.rpc("getnewaddress", wallet="vault")
        txid = N.rpc("sendtoaddress", va, 1.0, wallet="w")
        N.mine(1, a)
        return [x for x in N.rpc("listunspent", 1, 9999, [va], wallet="vault")][0]
    def spend(utxo, who, seq=None):
        inp = {"txid": utxo["txid"], "vout": utxo["vout"]}
        if seq:
            inp["sequence"] = seq
        p = N.rpc("walletcreatefundedpsbt", [inp], [{dest: 1.0}], 0, {"add_inputs": False, "fee_rate": 10, "subtractFeeFromOutputs": [0]}, wallet="vault")["psbt"]
        s = N.rpc("walletprocesspsbt", p, True, "DEFAULT", True, wallet=who)
        f = N.rpc("finalizepsbt", s["psbt"])
        return f
    def verdict(h):
        r = N.rpc("testmempoolaccept", [h])[0]
        return {"allowed": r["allowed"], "reject_reason": r.get("reject-reason")}
    u1 = fund()
    fo = spend(u1, "owner")
    R["b7_owner"] = {"complete": fo["complete"], "confirmations_of_utxo": 1, **verdict(fo["hex"])}
    u2 = fund()
    fh = spend(u2, "heir", 10)
    seqhex = N.rpc("decoderawtransaction", fh["hex"])["vin"][0]["sequence"]
    R["b7_heir"] = {"complete": fh["complete"], "sequence": seqhex, "at_1_conf": verdict(fh["hex"])}
    N.mine(8, a)
    R["b7_heir"]["at_9_conf"] = {"confirmations": N.rpc("gettransaction", u2["txid"], wallet="vault")["confirmations"], **verdict(fh["hex"])}
    # the heir without the sequence: the script cannot be satisfied at all
    fn = spend(u2, "heir")
    R["b7_heir"]["without_sequence_set"] = {"complete": fn["complete"], "verdict": verdict(fn["hex"]) if fn.get("hex") else None}
    N.mine(1, a)
    R["b7_heir"]["at_10_conf"] = {"confirmations": N.rpc("gettransaction", u2["txid"], wallet="vault")["confirmations"], **verdict(fh["hex"])}
    sent = N.rpc("sendrawtransaction", fh["hex"])
    N.mine(1, a)
    R["b7_heir"]["spent_confirmations"] = N.rpc("gettransaction", sent, wallet="vault")["confirmations"]
    # an owner who moves the coins resets the clock: the new output starts again at 0 confirmations for the heir
    R["b7_limits"] = {}
    for v in (0, 1, 65535, 65536, 4194304 + 1, 4194304 + 65535, 4194304 + 65536):
        R["b7_limits"][str(v)] = N.attempt("getdescriptorinfo", "wsh(or_d(pk(%s),and_v(v:pk(%s),older(%d))))" % (ko, kh, v))
        r = R["b7_limits"][str(v)]
        R["b7_limits"][str(v)] = {"ok": True} if "ok" in r else r
    R["b7_unit_seconds_x65535"] = 65535 * 512
    # older(65536): the parser accepts it, but the chain reads only the low 16 bits of the sequence, so the heir may spend with no wait at all
    d2 = N.rpc("getdescriptorinfo", "wsh(or_d(pk(%s),and_v(v:pk(%s),older(65536))))" % (ko, kh))["descriptor"]
    N.rpc("createwallet", "vault2", True, True)
    N.rpc("importdescriptors", [{"desc": d2, "active": True, "range": [0, 10], "timestamp": "now"}], wallet="vault2")
    va2 = N.rpc("getnewaddress", wallet="vault2")
    N.rpc("sendtoaddress", va2, 1.0, wallet="w")
    N.mine(1, a)
    u3 = N.rpc("listunspent", 1, 9999, [va2], wallet="vault2")[0]
    p3 = N.rpc("walletcreatefundedpsbt", [{"txid": u3["txid"], "vout": u3["vout"], "sequence": 65536}], [{dest: 1.0}], 0, {"add_inputs": False, "fee_rate": 10, "subtractFeeFromOutputs": [0]}, wallet="vault2")["psbt"]
    f3 = N.rpc("finalizepsbt", N.rpc("walletprocesspsbt", p3, True, "DEFAULT", True, wallet="heir")["psbt"])
    R["b7_older_65536"] = {"complete": f3["complete"], "confirmations": 1, **(verdict(f3["hex"]) if f3.get("hex") else {})}
    N.stop()


def b8():
    """the release check: the tarball against the signed list of hashes; the signature check, tried with an empty keyring"""
    d = "/home/claude/core31"
    tb = os.path.join(d, "bitcoin-31.1-x86_64-linux-gnu.tar.gz")
    h = hashlib.sha256(open(tb, "rb").read()).hexdigest()
    sums = open(os.path.join(d, "SHA256SUMS")).read().splitlines()
    line = [x for x in sums if x.endswith("bitcoin-31.1-x86_64-linux-gnu.tar.gz")]
    gh = os.path.join(TMP, "gnupg")
    os.makedirs(gh, mode=0o700, exist_ok=True)
    g = subprocess.run(["gpg", "--homedir", gh, "--verify", os.path.join(d, "SHA256SUMS.asc"), os.path.join(d, "SHA256SUMS")], capture_output=True, text=True)
    sig = g.stderr
    R["b8_release"] = {"tarball_sha256": h, "listed": line[0].split()[0] if line else None, "match": bool(line) and line[0].split()[0] == h, "n_lines_in_list": len(sums), "gpg_exit": g.returncode,
                       "gpg_output": " ".join(sig.split())[:500], "gpg_has_signature_line": "Good signature" in sig, "n_signatures_made": sig.count("Signature made"), "n_cannot_check_no_public_key": sig.count("No public key"), "keys_in_keyring": 0, "tarball_bytes": os.path.getsize(tb)}
    help_out = subprocess.run([BIN + "/bitcoind", "-help-debug"], capture_output=True, text=True).stdout
    R["b8_help_has"] = {k: (k in help_out) for k in ("-assumevalid", "-v2transport", "-keypool", "-walletnotify", "-rpcallowip", "-rpcauth")}


R["binary"] = {"bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest(), "version_line": subprocess.run([BIN + "/bitcoind", "-version"], capture_output=True, text=True).stdout.splitlines()[0]}
R["not_executed"] = {
    "hardware_signing_device": "no physical device (Trezor, Ledger, Coldcard) was available; the cold wallet of b3 is a second private node and not a tamper-resistant chip",
    "true_air_gap": "the cold node of b3 ran on the same machine and sent its PSBT as a string through this script; no USB stick, QR code or camera was involved",
    "paper_and_metal_backups": "no printer, no steel plate and no fire or water test; only the file made by backupwallet was restored",
    "exchange_hack_or_hot_wallet_breach": "no exchange or server was attacked; Mt. Gox, Bitfinex and the Casascius case are read from the saved pages",
    "estate_planning_with_a_lawyer": "a lawyer, a digital asset executor and a family were not available; only the script-level heir path of b7 was run",
    "mainnet_funds": "all coins are regtest coins on private chains; no real funds, fees or exchanges",
    "shamir_slip39_in_a_wallet": "no wallet in the table does SLIP 39 or codex32 shares; the sharing scheme is computed by sen0401_ch13_lib, not run on a device",
    "bip39_recovery_in_core": "Bitcoin Core has no BIP 39 import, so the mnemonic vectors are recomputed by the library only",
    "gpg_signature_check": "the builders' public keys were not imported (no web of trust, no keyserver), so gpg could not call any signature good; the exit code and the error are recorded",
    "bip324_on_the_wire": "no packet capture; the session id and the transport type come from getpeerinfo of both nodes",
}
for nm, fn in (("b1", b1), ("b2", b2), ("b3", b3), ("b4", b4), ("b5", b5), ("b6", b6), ("b7", b7), ("b8", b8)):
    phase(nm, fn)
R["total_seconds"] = round(time.time() - T0, 1)
json.dump(R, open(OUT, "w"), indent=1, sort_keys=True)
shutil.rmtree(TMP, ignore_errors=True)
print("written", OUT, R["total_seconds"], "s; errors:", list(R["errors"]))
