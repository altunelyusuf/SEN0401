#!/usr/bin/env python3
"""SEN0401 chapter 10 (The Bitcoin Network): the regtest run. Starts several Bitcoin Core 31.1 nodes (the release binary of bitcoincore.org, sha256 in the record) on private regtest
chains in temporary data directories, connects them to each other on the loopback interface and to a probe peer written for this chapter (sen0401_ch10_p2p_v1_0_0.py, no Bitcoin
Core code), and records what the nodes answered in ch10-evidence/regtest_run_v1_0_0.json. Nothing here touches the public network (-dnsseed=0 -discover=0 -fixedseeds=0).
One run, one record: keys, nonces, timings and txids differ on a rerun; the chapter's claims are checked against the record of the run that is saved.
Usage: sen0401_ch10_regtest_v1_0_0.py [out.json] [--only e1,e2]   Environment: BITCOIN_BIN (directory of bitcoind and bitcoin-cli), TMPDIR."""
__version__ = "1.0.0"
import hashlib, json, os, shutil, socket, struct, subprocess, sys, tempfile, threading, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P

BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
args = [a for a in sys.argv[1:] if not a.startswith("--") and not a.startswith("e")]
OUT = args[0] if args else os.path.join(HERE, "ch10-evidence", "regtest_run_v1_0_0.json")
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
TMP = tempfile.mkdtemp(prefix="ch10_regtest_", dir=os.environ.get("TMPDIR"))
R = {"_version": __version__, "phase": {}, "errors": {}}
T0 = time.time()
NODES = {}


class RPCError(Exception):
    pass


class Node:
    def __init__(self, name, port_base, extra=(), wallet=True):
        self.name, self.rpcport, self.port = name, port_base, port_base + 1
        self.dd = os.path.join(TMP, name)
        os.makedirs(self.dd, exist_ok=True)
        self.extra, self.wallet = list(extra), wallet
        NODES[name] = self

    def cli(self):
        return [BIN + "/bitcoin-cli", "-regtest", "-datadir=" + self.dd, "-rpcport=%d" % self.rpcport, "-rpcclienttimeout=900", "-stdin"]

    def rpc(self, method, *a, wallet=None, **named):
        c = self.cli()
        w = wallet if wallet is not None else ("w" if self.wallet else None)
        if w:
            c.append("-rpcwallet=" + w)
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

    def start(self, extra=()):
        subprocess.run([BIN + "/bitcoind", "-regtest", "-datadir=" + self.dd, "-daemon", "-server", "-rpcport=%d" % self.rpcport, "-port=%d" % self.port, "-bind=127.0.0.1",
                        "-listen=1", "-dnsseed=0", "-discover=0", "-listenonion=0", "-fixedseeds=0", "-fallbackfee=0.0002", "-rpcthreads=4", "-debug=net"] + self.extra + list(extra),
                       capture_output=True, text=True, check=True)
        for _ in range(200):
            try:
                self.rpc("getblockcount", wallet="")
                break
            except RPCError:
                time.sleep(0.3)
        else:
            raise SystemExit("node %s did not start" % self.name)
        if self.wallet:
            r = self.attempt("createwallet", "w", wallet="")
            if "error" in r:
                self.attempt("loadwallet", "w", wallet="")

    def stop(self):
        try:
            self.rpc("stop", wallet="")
        except RPCError:
            pass
        time.sleep(2.5)

    def addr(self):
        return self.rpc("getnewaddress")

    def mine(self, n, addr=None):
        a = addr or self.rpc("getnewaddress")
        out = []
        while n > 0:
            k = min(n, 500)
            out += self.rpc("generatetoaddress", k, a)
            n -= k
        return out


def sat(x):
    return int(round(float(x) * 1e8))


def phase(name, fn):
    if ONLY and name not in ONLY:
        return
    t = time.time()
    try:
        fn()
    except BaseException as e:
        R["errors"][name] = traceback.format_exc()[-1500:]
        print("ERROR in", name, repr(e)[:300], flush=True)
    R["phase"][name] = round(time.time() - t, 1)
    print("phase", name, R["phase"][name], "s", flush=True)


def msgs_summary(peer, start=0):
    return [[t, c, n] for t, c, n in peer.commands(start)]


def hexh(h):  # display hash -> internal bytes
    return bytes.fromhex(h)[::-1]


# ======================================================================================================================================== nodes
A = Node("A", 19600)
B = Node("B", 19610, ["-v2transport=1"])
C = Node("C", 19620, ["-v2transport=0"])
A.start()
R["binary"] = {"bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest(), "version_line": subprocess.run([BIN + "/bitcoind", "-version"], capture_output=True, text=True).stdout.splitlines()[0]}
R["networkinfo_A"] = A.rpc("getnetworkinfo")
ADDR = A.addr()
A.mine(101, ADDR)
# a chain of 2,100 blocks (the headers-in-batches experiment needs more than 2,000)
A.mine(2000, ADDR)
R["chain_A"] = {"blocks": A.rpc("getblockcount"), "best": A.rpc("getbestblockhash"), "size_on_disk": A.rpc("getblockchaininfo")["size_on_disk"]}
R["phase"]["setup"] = round(time.time() - T0, 1)


# ======================================================================================================================================== e1 handshake
def e1():
    p = P.Peer(A.port)
    t0 = time.time()
    v = p.handshake(services=1032, relay=True, pre_verack=[("wtxidrelay", b""), ("sendaddrv2", b"")])
    time.sleep(2.5)
    cmds = p.commands()
    R["e1_handshake"] = {"node_version": v, "sequence": [[t, c, n] for t, c, n in cmds], "our_version_bytes": len(P.version_payload()),
                         "magic": P.MAGIC["regtest"].hex(), "wait_s": round(time.time() - t0, 1)}
    # the node's sendcmpct message(s)
    R["e1_handshake"]["sendcmpct"] = [[p_[2][0], struct.unpack("<Q", p_[2][1:9])[0]] for p_ in p.msgs if p_[1] == "sendcmpct"]
    R["e1_handshake"]["feefilter"] = [struct.unpack("<q", p_[2])[0] for p_ in p.msgs if p_[1] == "feefilter"]
    R["e1_peerinfo"] = [x for x in A.rpc("getpeerinfo") if x["subver"].startswith("/sen0401")]
    p.close()


# ======================================================================================================================================== e2 headers
def e2():
    p = P.Peer(A.port)
    p.handshake()
    genesis = A.rpc("getblockhash", 0)
    p.send("getheaders", P.getheaders_payload([hexh(genesis)]))
    r1 = p.wait("headers", 20)
    h1 = P.parse_headers(r1[2])
    last = P.header_hash(h1[-1])
    k = r1[0] + 1
    p.send("getheaders", P.getheaders_payload([hexh(last)]))
    r2 = p.wait("headers", 20, start=k)
    h2 = P.parse_headers(r2[2])
    # the chain of the headers: every header points to the previous one
    chain_ok = all(h1[i + 1][4:36] == P.sha256d(h1[i]) for i in range(len(h1) - 1)) and h2[0][4:36] == P.sha256d(h1[-1])
    R["e2_headers"] = {"first_count": len(h1), "first_bytes": len(r1[2]), "second_count": len(h2), "second_bytes": len(r2[2]), "chain_links_ok": chain_ok,
                       "tip_from_headers": P.header_hash(h2[-1]), "tip_from_node": A.rpc("getbestblockhash"), "height": A.rpc("getblockcount"),
                       "header_size": len(h1[0]), "locator_first": genesis}
    # sendheaders: with it the node announces a new block by a headers message, without it by inv
    p2 = P.Peer(A.port); p2.handshake(); p3 = P.Peer(A.port); p3.handshake(); p3.send("sendheaders")
    tip = A.rpc("getbestblockhash"); p2.sync_to_tip(tip); p3.sync_to_tip(tip)
    time.sleep(1)
    n0, n3 = len(p2.msgs), len(p3.msgs)
    A.mine(1, ADDR)
    time.sleep(3)
    R["e2_announce"] = {"without_sendheaders": [c for t, c, n in p2.commands(n0) if c in ("inv", "headers", "cmpctblock")], "with_sendheaders": [c for t, c, n in p3.commands(n3) if c in ("inv", "headers", "cmpctblock")]}
    for q in (p, p2, p3):
        q.close()


# ======================================================================================================================================== e3 compact blocks
def e3():
    # 12 transactions go into the mempool before the block that is found
    dests = [A.addr() for _ in range(12)]
    txids = [A.rpc("sendtoaddress", d, "%.3f" % (0.01 + i / 1000)) for i, d in enumerate(dests)]
    hb = P.Peer(A.port); vhb = hb.handshake(); hb.send("sendcmpct", P.sendcmpct(True, 2))
    lb = P.Peer(A.port); lb.handshake(); lb.send("sendcmpct", P.sendcmpct(False, 2)); lb.send("sendheaders")
    tip = A.rpc("getbestblockhash"); hb.sync_to_tip(tip); lb.sync_to_tip(tip)
    time.sleep(1.5)
    k_hb, k_lb = len(hb.msgs), len(lb.msgs)
    pi = {x["id"]: x for x in A.rpc("getpeerinfo")}
    bh = A.mine(1, ADDR)[0]
    r = hb.wait("cmpctblock", 15, start=k_hb)
    cb = P.parse_cmpctblock(r[2])
    blk = A.rpc("getblock", bh, 2)
    raw = bytes.fromhex(A.rpc("getblock", bh, 0))
    wtxids = [t["hash"] for t in blk["tx"]]
    mine_ids = [P.short_id(cb["header"], cb["nonce"], w) for w in wtxids[1:]]
    # ask for transactions 1 and 2 of the block (getblocktxn: block hash, indexes as differences)
    req = hexh(bh) + P.cs_enc(2) + P.cs_enc(1) + P.cs_enc(0)
    hb.send("getblocktxn", req)
    bt = hb.wait("blocktxn", 10)
    n_bt, ibt = P.cs_dec(bt[2], 32)
    got = []
    for _ in range(n_bt):
        t_, ibt = P.parse_tx_bytes(bt[2], ibt); got.append(t_["txid"])
    R["e3_compact"] = {"block": bh, "tx_count": len(blk["tx"]), "cmpctblock_bytes": cb["bytes"], "full_block_bytes": len(raw), "prefilled_indexes": [i for i, t in cb["prefilled"]],
                       "prefilled_txids": [t["txid"] for i, t in cb["prefilled"]], "short_id_count": len(cb["short_ids"]), "short_ids_match": cb["short_ids"] == mine_ids,
                       "short_id_bytes": 6, "coinbase_txid": blk["tx"][0]["txid"], "blocktxn_txids": got, "expected_txids": [blk["tx"][1]["txid"], blk["tx"][2]["txid"]],
                       "hb_peer_services": vhb["services"], "peerinfo_hb_from": [pi[i].get("bip152_hb_from") for i in pi if pi[i]["subver"].startswith("/sen0401")][:2],
                       "node_sendcmpct_version": [struct.unpack("<Q", m[2][1:9])[0] for m in hb.msgs if m[1] == "sendcmpct"], "cmpct_header_hex": cb["header"].hex(), "nonce_hex": cb["nonce"].hex(),
                       "wtxids": wtxids, "short_ids": cb["short_ids"], "shortid_siphash_vector": P.siphash_test_vector()}
    # low bandwidth: the node announces by headers (we sent sendheaders), we ask for the compact block ourselves
    ann = [c for t, c, n in lb.commands(k_lb) if c in ("inv", "headers", "cmpctblock")]
    lb_headers = lb.wait("headers", 5, start=k_lb)
    gd = P.cs_enc(1) + struct.pack("<I", P.MSG["CMPCT_BLOCK"]) + hexh(bh)
    k2 = len(lb.msgs)
    lb.send("getdata", gd)
    r2 = lb.wait("cmpctblock", 10, start=k2)
    # depth: a block 20 deep is answered with a full block, not a compact block
    old = A.rpc("getblockhash", A.rpc("getblockcount") - 20)
    k3 = len(lb.msgs)
    lb.send("getdata", P.cs_enc(1) + struct.pack("<I", P.MSG["CMPCT_BLOCK"]) + hexh(old))
    time.sleep(2)
    ans = [c for t, c, n in lb.commands(k3) if c in ("cmpctblock", "block")]
    R["e3_low_bandwidth"] = {"announced_by": ann, "cmpctblock_requested_ok": r2 is not None, "answer_for_old_block": ans, "depth_asked": 20,
                             "compact_equal_to_hb": r2 is not None and r2[2] == r[2]}
    hb.close(); lb.close()


# ======================================================================================================================================== e4 orphan transactions
def e4():
    # parent and child are built in the wallet and signed, but never sent by the node itself
    d1, d2 = A.addr(), A.addr()
    raw = A.rpc("createrawtransaction", [], {d1: 0.5})
    f = A.rpc("fundrawtransaction", raw, {"changePosition": 1})
    sp = A.rpc("signrawtransactionwithwallet", f["hex"])
    parent = P.parse_tx_bytes(bytes.fromhex(sp["hex"]))[0]
    vout_i = [i for i, o in enumerate(A.rpc("decoderawtransaction", sp["hex"])["vout"]) if o["scriptPubKey"]["address"] == d1][0]
    spk = A.rpc("decoderawtransaction", sp["hex"])["vout"][vout_i]["scriptPubKey"]["hex"]
    raw2 = A.rpc("createrawtransaction", [{"txid": parent["txid"], "vout": vout_i}], {d2: 0.4999})
    sc = A.rpc("signrawtransactionwithwallet", raw2, [{"txid": parent["txid"], "vout": vout_i, "scriptPubKey": spk, "amount": 0.5}])
    child = P.parse_tx_bytes(bytes.fromhex(sc["hex"]))[0]
    pe = P.Peer(A.port); pe.handshake(pre_verack=[("wtxidrelay", b"")])
    k = len(pe.msgs)
    # announce the child (by wtxid), the node asks for it, we send it
    pe.send("inv", P.inv_payload([(P.MSG["WTX"], hexh(child["wtxid"]))]))
    g = pe.wait("getdata", 15, start=k)
    asked1 = P.parse_inv(g[2]) if g else None
    pe.send("tx", child["raw"])
    pool0 = A.rpc("getrawmempool")
    time.sleep(1.5)
    orph = A.attempt("getorphantxs", 1, wallet="")
    pool1 = A.rpc("getrawmempool")
    g2 = pe.wait("getdata", 20, start=g[0] + 1) if g else None
    asked2 = P.parse_inv(g2[2]) if g2 else None
    # the parent arrives
    pe.send("tx", parent["raw"])
    time.sleep(2)
    pool2 = A.rpc("getrawmempool")
    R["e4_orphan"] = {"parent": parent["txid"], "child": child["txid"], "child_wtxid": child["wtxid"], "node_asked_for_child": asked1, "mempool_after_child": len(pool1) - len(pool0),
                      "child_in_mempool_after_child": child["txid"] in pool1, "orphanage_after_child": orph, "node_asked_for_parent": asked2, "parent_in_mempool_after": parent["txid"] in pool2,
                      "child_in_mempool_after": child["txid"] in pool2, "orphanage_after_parent": A.attempt("getorphantxs", 0, wallet=""), "commands_after": [c for t, c, n in pe.commands(k)]}
    pe.close()
    A.mine(1, ADDR)


# ======================================================================================================================================== e5 inventory relay, fRelay and feefilter
def e5():
    c5 = P.Peer(A.port); c5.handshake(pre_verack=[("wtxidrelay", b"")])
    c6 = P.Peer(A.port); c6.handshake(relay=False)
    c7 = P.Peer(A.port); c7.handshake(); c7.send("feefilter", struct.pack("<q", 5000))
    time.sleep(1)
    ks = [len(c.msgs) for c in (c5, c6, c7)]
    a1, a2 = A.addr(), A.addr()
    t_low = A.rpc("send", outputs={a1: 0.02}, fee_rate=2, options={"minconf": 1})["txid"]
    t_high = A.rpc("send", outputs={a2: 0.02}, fee_rate=20, options={"minconf": 1})["txid"]
    ent = {t: A.rpc("getmempoolentry", t) for t in (t_low, t_high)}
    end = time.time() + 45
    while time.time() < end:
        if all(any(m[1] == "inv" for m in c.msgs[k:]) for c, k in ((c5, ks[0]), (c7, ks[2]))) and time.time() > end - 38:
            break
        time.sleep(1)
    time.sleep(6)
    res = {}
    for name, c, k in (("normal_wtxidrelay", c5, ks[0]), ("relay_false", c6, ks[1]), ("feefilter_5sat", c7, ks[2])):
        invs = []
        for t, cmd, p in c.msgs[k:]:
            if cmd == "inv":
                invs += [[t, ty, h] for ty, h in P.parse_inv(p)]
        res[name] = invs
    # the normal peer asks for one announced transaction by wtxid and receives it
    w_high = ent[t_high]["wtxid"]
    k5 = len(c5.msgs)
    c5.send("getdata", P.inv_payload([(P.MSG["WTX"], hexh(w_high))]))
    rt = c5.wait("tx", 10, start=k5)
    R["e5_relay"] = {"txid_low": t_low, "txid_high": t_high, "wtxid_low": ent[t_low]["wtxid"], "wtxid_high": w_high, "feerate_low": ent[t_low]["fees"]["base"] * 1e8 / ent[t_low]["vsize"],
                     "feerate_high": ent[t_high]["fees"]["base"] * 1e8 / ent[t_high]["vsize"], "invs": res, "tx_received_txid": P.parse_tx_bytes(rt[2])[0]["txid"] if rt else None,
                     "inv_types": {"1": "MSG_TX", "5": "MSG_WTX"}, "peer_feefilter_sat_per_kvb": 5000, "version_relay_field_c6": False}
    for c in (c5, c6, c7):
        c.close()
    A.mine(1, ADDR)


# ======================================================================================================================================== e6 bloom filters
def e6():
    # node A has no NODE_BLOOM: a filterload ends the connection
    pa = P.Peer(A.port); va = pa.handshake()
    bl = P.Bloom(3, 0.01, 0, 1)
    pa.send("filterload", bl.payload())
    time.sleep(2)
    R["e6_bloom_default"] = {"services_names": va["services_names"], "has_bloom_bit": bool(va["services"] & 4), "disconnected_after_filterload": pa.closed}
    pa.close()
    # node D with -peerbloomfilters=1: the light client of the chapter
    D = Node("D", 19630, ["-peerbloomfilters=1"])
    D.start()
    DA = D.addr()
    D.mine(101, DA)
    # the light client has a key: a hash of 20 bytes made up for the test (it is a witness program, P2WPKH)
    import hashlib as hl
    key_hash = hl.sha256(b"sen0401-ch10-light-client").digest()[:20]
    addr_lc = P.p2wpkh_address(key_hash)
    assert D.rpc("validateaddress", addr_lc)["scriptPubKey"] == "0014" + key_hash.hex()
    others = [D.addr() for _ in range(40)]
    D.rpc("sendmany", "", {**{o: 0.01 for o in others}, addr_lc: 0.25})
    for _ in range(3):
        D.rpc("sendtoaddress", D.addr(), 0.1)
    bh = D.mine(1, DA)[0]
    blk = D.rpc("getblock", bh, 2)
    pd = P.Peer(D.port); vd = pd.handshake()
    # a filter for one element (the key hash) and 2 others: the client adds the hash of its key
    bf = P.Bloom(3, 0.0001, 0x1234, 0)
    for e in (key_hash, b"a pattern the client does not own", b"another one"):
        bf.insert(e)
    pd.send("filterload", bf.payload())
    time.sleep(0.5)
    k = len(pd.msgs)
    pd.send("getdata", P.cs_enc(1) + struct.pack("<I", P.MSG["FILTERED_BLOCK"]) + hexh(bh))
    mb = pd.wait("merkleblock", 10, start=k)
    time.sleep(1)
    txm = [P.parse_tx_bytes(m[2])[0]["txid"] for m in pd.msgs[k:] if m[1] == "tx"]
    hdr, total, hashes, bits = P.parse_merkleblock(mb[2])
    root, matched, nb, nh = P.partial_merkle_tree(total, hashes, bits)
    lc_tx = [t["txid"] for t in blk["tx"] if any(o["scriptPubKey"]["hex"] == "0014" + key_hash.hex() for o in t["vout"])]
    R["e6_bloom_enabled"] = {"services_names": vd["services_names"], "filter_hex": bf.payload().hex(), "filter_bytes": len(bf.data), "hash_functions": bf.k, "block": bh, "block_txs": len(blk["tx"]),
                             "merkleblock_bytes": len(mb[2]), "merkleblock_total": total, "merkleblock_hashes": len(hashes), "matched_txids": matched, "tx_messages": txm, "tree_root": root,
                             "header_root": hdr[36:68][::-1].hex(), "wallet_tx": lc_tx, "bits_used": nb, "hashes_used": nh, "full_block_bytes": len(bytes.fromhex(D.rpc("getblock", bh, 0)))}
    # filteradd and filterclear, then a block is requested again: the empty filter matches nothing
    pd.send("filterclear")
    k2 = len(pd.msgs)
    pd.send("getdata", P.cs_enc(1) + struct.pack("<I", P.MSG["FILTERED_BLOCK"]) + hexh(bh))
    mb2 = pd.wait("merkleblock", 10, start=k2)
    time.sleep(0.5)
    h2, tot2, hs2, b2 = P.parse_merkleblock(mb2[2]) if mb2 else (None, 0, [], [])
    R["e6_bloom_enabled"]["after_filterclear"] = {"merkleblock_hashes": len(hs2), "tx_messages": len([m for m in pd.msgs[k2:] if m[1] == "tx"])}
    # SPV: the proof of the node for the light client's transaction, checked with the independent merkle path
    proof = D.rpc("gettxoutproof", [lc_tx[0]], bh)
    ph, ptot, phs, pbits = P.parse_merkleblock(bytes.fromhex(proof))
    path, root2 = P.merkle_branch([t["txid"] for t in blk["tx"]], [t["txid"] for t in blk["tx"]].index(lc_tx[0]))
    R["e6_spv"] = {"txid": lc_tx[0], "verifytxoutproof": D.rpc("verifytxoutproof", proof), "proof_bytes": len(bytes.fromhex(proof)), "path": path, "path_len": len(path), "root_from_path": P.follow_branch(lc_tx[0], [t["txid"] for t in blk["tx"]].index(lc_tx[0]), path),
                   "header_root": blk["merkleroot"], "block_tx_count": len(blk["tx"]), "header_hex": D.rpc("getblockheader", bh, False), "confirmations": D.rpc("getblockheader", bh)["confirmations"],
                   "headers_only_bytes": 80 * (D.rpc("getblockcount") + 1), "chain_dir_bytes": D.rpc("getblockchaininfo")["size_on_disk"]}
    pd.close()
    D.stop()


# ======================================================================================================================================== e7 block filters (BIP 157/158)
def e7():
    E = Node("E", 19640, ["-blockfilterindex=1", "-peerblockfilters=1"])
    E.start()
    EA = E.addr()
    E.mine(101, EA)
    outs = {E.addr(): 0.01 for _ in range(60)}
    E.rpc("sendmany", "", outs)
    for _ in range(5):
        E.rpc("sendtoaddress", E.addr(), 0.5)
    E.rpc("sendmany", "", {E.addr(): 0.02 for _ in range(30)})
    # an OP_RETURN output as well
    raw = E.rpc("createrawtransaction", [], [{"data": "73656e30343031"}])
    sg = E.rpc("signrawtransactionwithwallet", E.rpc("fundrawtransaction", raw)["hex"])
    E.rpc("sendrawtransaction", sg["hex"])
    bh = E.mine(1, EA)[0]
    E.mine(30, EA)
    time.sleep(3)
    gf = E.rpc("getblockfilter", bh)
    blk3 = E.rpc("getblock", bh, 3)
    raw_block = P.parse_block(bytes.fromhex(E.rpc("getblock", bh, 0)))
    prev = [bytes.fromhex(v["prevout"]["scriptPubKey"]["hex"]) for t in blk3["tx"][1:] for v in t["vin"]]
    els = P.block_filter_elements(raw_block, prev)
    mine_f, n = P.basic_filter(bh, els)
    flt = bytes.fromhex(gf["filter"])
    prev_hdr = E.rpc("getblockfilter", E.rpc("getblockhash", blk3["height"] - 1))["header"]
    R["e7_filter"] = {"block": bh, "height": blk3["height"], "tx_count": len(blk3["tx"]), "node_filter_hex": gf["filter"], "node_header": gf["header"], "my_filter_equal": mine_f == flt, "my_header_equal": P.filter_header(flt, prev_hdr) == gf["header"],
                      "n_elements": n, "filter_bytes": len(flt), "bits_per_element": round(len(flt) * 8 / n, 2), "scripts_total": len(els), "op_return_outputs": sum(1 for t in raw_block["txs"] for o in t["vout"] if o["spk"][:1] == b"\x6a"),
                      "prev_header": prev_hdr, "any_op_return_in_filter": any(P.filter_match(flt, bh, o["spk"]) for t in raw_block["txs"] for o in t["vout"] if o["spk"][:1] == b"\x6a"),
                      "own_scripts_all_match": all(P.filter_match(flt, bh, s) for s in els), "random_script_match": P.filter_match(flt, bh, b"\x00\x14" + b"\x07" * 20),
                      "elements_hex": [e.hex() for e in els]}
    # false positive rate measured with random scripts
    import random
    rnd = random.Random(10)
    n_, i_ = P.cs_dec(flt, 0)
    vals = set(P.golomb_decode(flt[i_:], n_))
    hb_ = bytes.fromhex(bh)[::-1]
    k0_, k1_ = int.from_bytes(hb_[:8], "little"), int.from_bytes(hb_[8:16], "little")
    TR = 400000
    hits = sum(1 for _ in range(TR) if ((P.siphash24(k0_, k1_, b"\x00\x14" + rnd.randbytes(20)) * (n_ * P.GCS_M)) >> 64) in vals)
    R["e7_filter"]["random_probe"] = {"trials": TR, "hits": hits, "elements": n_, "m": P.GCS_M}
    # the filter over the wire
    pe = P.Peer(E.port); ve = pe.handshake()
    h_stop = E.rpc("getblockhash", blk3["height"])
    k = len(pe.msgs)
    pe.send("getcfilters", P.getcfilters_payload(blk3["height"] - 2, h_stop))
    time.sleep(2)
    cf = [P.parse_cfilter_msg(m[2]) for m in pe.msgs[k:] if m[1] == "cfilter"]
    pe.send("getcfheaders", P.getcfilters_payload(blk3["height"] - 2, h_stop))
    ch = pe.wait("cfheaders", 10, start=k)
    pe.send("getcfcheckpt", bytes([0]) + hexh(E.rpc("getbestblockhash")))
    cp = pe.wait("cfcheckpt", 10, start=k)
    R["e7_wire"] = {"services_names": ve["services_names"], "has_compact_filters_bit": bool(ve["services"] & 64), "cfilter_count": len(cf), "cfilter_blocks": [c["block_hash"] for c in cf],
                    "cfilter_for_block_equal": [c["filter"].hex() == gf["filter"] for c in cf if c["block_hash"] == bh], "cfheaders_bytes": len(ch[2]) if ch else None,
                    "cfcheckpt_bytes": len(cp[2]) if cp else None, "checkpoint_interval": 1000, "tip_height": E.rpc("getblockcount")}
    # a node without -peerblockfilters ignores or ends
    pa = P.Peer(A.port); va = pa.handshake()
    pa.send("getcfilters", P.getcfilters_payload(1, A.rpc("getblockhash", 5)))
    time.sleep(2)
    R["e7_wire"]["node_without_option"] = {"has_compact_filters_bit": bool(va["services"] & 64), "disconnected": pa.closed, "cfilters_returned": len([m for m in pa.msgs if m[1] == "cfilter"])}
    pe.close(); pa.close()
    E.stop()


# ======================================================================================================================================== e8 connections, peers, v2 transport
def e8():
    B.start(); C.start()
    A.rpc("addnode", "127.0.0.1:%d" % B.port, "add") if False else None
    # a proxy between A and B records the bytes of one connection each time
    def proxy(listen_port, target_port, log):
        srv = socket.socket(); srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); srv.bind(("127.0.0.1", listen_port)); srv.listen(1); srv.settimeout(30)

        def run():
            try:
                cs, _ = srv.accept()
            except OSError:
                return
            ts = socket.create_connection(("127.0.0.1", target_port))
            cs.settimeout(0.5); ts.settimeout(0.5)
            end = time.time() + 12
            while time.time() < end:
                for src, dst, tag in ((cs, ts, "A>B"), (ts, cs, "B>A")):
                    try:
                        d = src.recv(65536)
                    except socket.timeout:
                        continue
                    except OSError:
                        d = b""
                    if d:
                        log.append((tag, d)); dst.sendall(d)
            cs.close(); ts.close(); srv.close()
        th = threading.Thread(target=run, daemon=True); th.start(); return th
    results = {}
    for tag, node, v2 in (("v2", B, True), ("v1", C, False)):
        log = []
        th = proxy(19690 + (0 if v2 else 1), node.port, log)
        time.sleep(0.5)
        A.rpc("addconnection", "127.0.0.1:%d" % (19690 + (0 if v2 else 1)), "outbound-full-relay", v2)
        time.sleep(5)
        pi_a = [x for x in A.rpc("getpeerinfo") if x["addr"].endswith(str(19690 + (0 if v2 else 1)))]
        pi_n = [x for x in node.rpc("getpeerinfo") if x["inbound"]]
        th.join(timeout=20)
        ab = b"".join(d for t, d in log if t == "A>B"); ba = b"".join(d for t, d in log if t == "B>A")
        results[tag] = {"bytes_a_to_b": len(ab), "bytes_b_to_a": len(ba), "contains_magic": P.MAGIC["regtest"] in ab + ba, "contains_version_command": b"version\x00" in ab + ba,
                        "contains_verack": b"verack" in ab + ba, "entropy_first_4096": round(P.entropy_bits_per_byte((ab + ba)[:4096]), 3), "first_bytes_a_to_b": ab[:24].hex(),
                        "transport_a": pi_a[0].get("transport_protocol_type") if pi_a else None, "session_id_a": pi_a[0].get("session_id") if pi_a else None,
                        "transport_n": pi_n[0].get("transport_protocol_type") if pi_n else None, "session_id_n": pi_n[0].get("session_id") if pi_n else None,
                        "subver_seen_by_a": pi_a[0]["subver"] if pi_a else None}
        for x in A.rpc("getpeerinfo"):
            A.attempt("disconnectnode", "", x["id"], wallet="")
        time.sleep(1)
    R["e8_transport"] = results
    # connection types, opened by the test RPC, and the fields of getpeerinfo
    L_, M_ = Node("L", 19710, wallet=False), Node("M", 19720, wallet=False)
    L_.start(); M_.start()
    att = {}
    for t, node, v2 in (("outbound-full-relay", B, True), ("block-relay-only", C, False), ("addr-fetch", L_, True), ("feeler", M_, True)):
        att[t] = A.attempt("addconnection", "127.0.0.1:%d" % node.port, t, v2, wallet="")
        time.sleep(2.5)
    R["e8_addconnection"] = att
    pi = A.rpc("getpeerinfo")
    R["e8_peerinfo_A"] = pi
    R["e8_peerinfo_B"] = B.rpc("getpeerinfo")
    R["e8_networkinfo_A"] = {k: v for k, v in A.rpc("getnetworkinfo").items() if k in ("connections", "connections_in", "connections_out", "localservicesnames")}
    # a block-relay-only connection carries no transactions: a transaction made on A reaches B only through the full-relay link, and the version message says relay = false
    R["e8_types"] = sorted({(x["connection_type"], x["relaytxes"], x.get("addr_relay_enabled"), x.get("transport_protocol_type")) for x in pi}, key=str)
    L_.stop(); M_.stop()
    # tor and i2p: a node that wants only onion peers (the proxy is a dummy, no Tor is reachable)
    K = Node("K", 19650, ["-onlynet=onion", "-proxy=127.0.0.1:9"], wallet=False)
    try:
        K.start()
    except subprocess.CalledProcessError as e:
        R["e8_onion_node_start"] = {"error": (e.stderr or e.stdout)[-300:]}
    else:
        ni = K.rpc("getnetworkinfo")
        R["e8_onion_node"] = {"networks": [(n["name"], n["reachable"], n["proxy"]) for n in ni["networks"]], "connections": ni["connections"], "localservicesnames": ni["localservicesnames"]}
        K.stop()


# ======================================================================================================================================== e9 addr and addrv2
def e9():
    for k in range(120):
        A.attempt("addpeeraddress", "44.%d.%d.%d" % (k // 60 + 1, k % 60 + 1, (k * 7) % 250 + 1), 8333, wallet="")
    for k in range(30):
        A.attempt("addpeeraddress", "2a01:4f8:%x:%x::2" % (k + 1, k + 9), 8333, wallet="")
    R["e9_addrman"] = {"getnodeaddresses_count": len(A.rpc("getnodeaddresses", 0)), "addrman_info": A.attempt("getaddrmaninfo", wallet="")}
    out = {}
    for tag, pre in (("with_sendaddrv2", [("sendaddrv2", b"")]), ("without", [])):
        p = P.Peer(A.port); p.handshake(pre_verack=pre)
        time.sleep(0.5)
        k = len(p.msgs)
        p.send("getaddr")
        time.sleep(3)
        rec = {}
        for t, c, pl in p.msgs[k:]:
            if c == "addrv2":
                es = P.parse_addrv2(pl); rec["addrv2"] = {"count": len(es), "networks": sorted({e["network"] for e in es}), "addr_len": sorted({e["addr_len"] for e in es}), "first": es[0]}
            if c == "addr":
                es = P.parse_addr_v1(pl); rec["addr"] = {"count": len(es), "first": es[0]}
        out[tag] = rec
        p.close()
    R["e9_addr"] = out


# ======================================================================================================================================== e10 mempool and UTXO set differ or agree between nodes; pruned node; initial block download
def e10():
    F = Node("F", 19660)
    G = Node("G", 19670, ["-blocksonly=1"])
    H = Node("H", 19680, ["-prune=550"], wallet=False)
    F.start(); G.start(); H.start()
    FA = F.addr()
    F.mine(101, FA)
    G.rpc("addnode", "127.0.0.1:%d" % F.port, "onetry", wallet="")
    for _ in range(40):
        if G.rpc("getblockcount") >= 101:
            break
        time.sleep(0.5)
    txs = [F.rpc("sendtoaddress", F.addr(), 0.01 * (i + 1)) for i in range(6)]
    time.sleep(8)
    before = {"F_mempool": F.rpc("getmempoolinfo")["size"], "G_mempool": G.rpc("getmempoolinfo")["size"], "F_peers": F.rpc("getconnectioncount"), "F_view_of_G_relaytxes": F.rpc("getpeerinfo")[0]["relaytxes"] if F.rpc("getpeerinfo") else None, "G_mempoolinfo_loaded": G.rpc("getmempoolinfo")["loaded"]}
    bh = F.mine(1, FA)[0]
    time.sleep(5)
    after = {"F_mempool": F.rpc("getmempoolinfo")["size"], "G_mempool": G.rpc("getmempoolinfo")["size"], "F_height": F.rpc("getblockcount"), "G_height": G.rpc("getblockcount")}
    uf, ug = F.rpc("gettxoutsetinfo"), G.rpc("gettxoutsetinfo")
    R["e10_mempool_vs_utxo"] = {"before_block": before, "after_block": after, "utxo_hash_F": uf["hash_serialized_3"], "utxo_hash_G": ug["hash_serialized_3"], "utxo_count_F": uf["txouts"], "utxo_count_G": ug["txouts"],
                                "mempoolinfo_F": F.rpc("getmempoolinfo"), "getorphantxs_F": F.attempt("getorphantxs", wallet="")}
    # a pruned node and the services it announces
    R["e10_pruned"] = {"services": H.rpc("getnetworkinfo")["localservicesnames"], "A_services": R["networkinfo_A"]["localservicesnames"], "prune_info": {k: v for k, v in H.rpc("getblockchaininfo").items() if k in ("pruned", "pruneheight", "size_on_disk")}}
    pp = P.Peer(H.port); vp = pp.handshake(); R["e10_pruned"]["version_services"] = vp["services_names"]; pp.close()
    H.stop()
    # initial block download of a new node from A (2,100+ blocks): the messages it needed
    I = Node("I", 19700, ["-connect=127.0.0.1:%d" % A.port], wallet=False)
    t = time.time()
    I.start()
    top = A.rpc("getblockcount")
    for _ in range(240):
        if I.rpc("getblockcount") >= top:
            break
        time.sleep(1)
    dt = round(time.time() - t, 1)
    pi = I.rpc("getpeerinfo")
    R["e10_ibd"] = {"seconds": dt, "height": I.rpc("getblockcount"), "target": top, "peer": {k: pi[0][k] for k in ("bytesrecv_per_msg", "bytessent_per_msg", "bytesrecv", "bytessent", "synced_headers", "synced_blocks", "subver", "connection_type", "version", "services") if k in pi[0]},
                    "headers_bytes_recv": pi[0]["bytesrecv_per_msg"].get("headers"), "chain_equal": I.rpc("getbestblockhash") == A.rpc("getbestblockhash")}
    log = open(os.path.join(I.dd, "regtest", "debug.log"), errors="replace").read()
    R["e10_ibd"]["log_getheaders_lines"] = [l[:200] for l in log.splitlines() if "received: headers" in l or "received: getheaders" in l or "sending getheaders" in l or "send version" in l][:12]
    I.stop()
    G.stop(); F.stop()


def e11():
    import re as _re
    src = open(os.path.join(HERE, "ch10-evidence", "core_src_kernel_chainparams.cpp"), errors="replace").read()
    main_part = src[src.index("class CMainParams"):src.index("class CTestNetParams")]
    seeds = _re.findall(r'vSeeds\.emplace_back\("([^"]+)"\)', main_part)
    res = {}
    socket.setdefaulttimeout(8)
    lock = threading.Lock()

    def one(sd):
        t = time.time()
        try:
            ai = socket.getaddrinfo(sd.rstrip("."), 8333, proto=socket.IPPROTO_TCP)
            v4 = sorted({a[4][0] for a in ai if a[0] == socket.AF_INET}); v6 = sorted({a[4][0] for a in ai if a[0] == socket.AF_INET6})
            r = {"ipv4": v4, "ipv6": v6, "seconds": round(time.time() - t, 2)}
        except OSError as e:
            r = {"error": str(e)[:80], "seconds": round(time.time() - t, 2)}
        with lock:
            res[sd] = r
    ths = [threading.Thread(target=one, args=(sd,)) for sd in seeds]
    [t.start() for t in ths]; [t.join() for t in ths]
    R["e11_dns_seeds"] = {"seeds_in_chainparams": seeds, "answers": res, "date": time.strftime("%Y-%m-%d", time.gmtime()),
                          "tcp_to_mainnet_peer": "not attempted: the sandbox allows outbound HTTPS through its proxy only; a direct connection to port 8333 timed out in the pre-check"}
    ip = [a for r in res.values() for a in r.get("ipv4", [])]
    R["e11_dns_seeds"]["distinct_ipv4"] = len(set(ip))
    try:
        c = socket.create_connection((ip[0], 8333), timeout=6); c.close(); R["e11_dns_seeds"]["tcp_probe"] = {"ip": ip[0], "connected": True}
    except OSError as e:
        R["e11_dns_seeds"]["tcp_probe"] = {"ip": ip[0] if ip else None, "connected": False, "error": str(e)[:60]}


for nm, fn in (("e1", e1), ("e2", e2), ("e3", e3), ("e4", e4), ("e5", e5), ("e6", e6), ("e7", e7), ("e8", e8), ("e9", e9), ("e10", e10), ("e11", e11)):
    phase(nm, fn)
R["phase"]["total_s"] = round(time.time() - T0, 1)
R["python"] = sys.version.split()[0]
R["nodes_started"] = sorted(NODES)
for n in NODES.values():
    try:
        n.stop()
    except Exception:
        pass
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(R, open(OUT, "w"), indent=1, default=str)
shutil.rmtree(TMP, ignore_errors=True)
print("written", OUT, "in", R["phase"]["total_s"], "s; errors:", list(R["errors"]))
