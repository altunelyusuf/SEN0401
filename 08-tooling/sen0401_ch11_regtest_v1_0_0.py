#!/usr/bin/env python3
"""SEN0401 chapter 11 (The Blockchain): the regtest run. Starts Bitcoin Core 31.1 nodes (the release binary of bitcoincore.org, sha256 in the record) on private chains in temporary data
directories and records what the nodes answered in ch11-evidence/regtest_run_v1_0_0.json: the block and its header as bytes, the block hash, the genesis blocks of the chains the book names,
the merkle roots of blocks of 1 to 16 transactions, the mutated block of CVE-2012-2459, a fork of two blocks of one height, the maturity of a coinbase, the height in the coinbase, the halving
every 150 blocks of regtest, the address prefixes, and the start-up of the testnet4, signet, custom signet and (refused) testnet3 chains. Nothing here touches the public network
(-dnsseed=0 -listen=0 -connect=0 -fixedseeds=0). One run, one record: hashes, keys and timings differ on a rerun; the chapter's claims are checked against the record of the saved run.
Usage: sen0401_ch11_regtest_v1_0_0.py [out.json] [--only b1,b2]   Environment: BITCOIN_BIN (directory of bitcoind and bitcoin-cli), TMPDIR."""
__version__ = "1.0.0"
import hashlib, json, os, shutil, subprocess, sys, tempfile, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P

BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
args = [a for a in sys.argv[1:] if not a.startswith("--") and not (a.startswith("b") and a[1:].isdigit())]
OUT = args[0] if args else os.path.join(HERE, "ch11-evidence", "regtest_run_v1_0_0.json")
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
TMP = tempfile.mkdtemp(prefix="ch11_regtest_", dir=os.environ.get("TMPDIR"))
R = {"_version": __version__, "phase": {}, "errors": {}}
T0 = time.time()


class RPCError(Exception):
    pass


class Node:
    def __init__(self, name, port_base, chain="regtest", extra=()):
        self.name, self.rpcport, self.port, self.chain = name, port_base, port_base + 1, chain
        self.dd = os.path.join(TMP, name)
        os.makedirs(self.dd, exist_ok=True)
        self.extra = list(extra)

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

    def rpc_args(self, method, *a):
        """the call the book prints: bitcoin-cli -regtest createwallet "" (arguments on the command line, so that an empty string stays an argument)"""
        r = subprocess.run([BIN + "/bitcoin-cli", "-" + self.chain, "-datadir=" + self.dd, "-rpcport=%d" % self.rpcport, method] + list(a), capture_output=True, text=True)
        return {"exit": r.returncode, "out": " ".join((r.stdout + r.stderr).split())[:300]}

    def attempt(self, method, *a, **kw):
        try:
            return {"ok": self.rpc(method, *a, **kw)}
        except RPCError as e:
            return {"error": " ".join(str(e).split())}

    def start(self):
        r = subprocess.run([BIN + "/bitcoind", "-" + self.chain, "-datadir=" + self.dd, "-daemon", "-server", "-rpcport=%d" % self.rpcport, "-port=%d" % self.port,
                            "-listen=0", "-dnsseed=0", "-discover=0", "-listenonion=0", "-fixedseeds=0", "-connect=0", "-fallbackfee=0.0002"] + self.extra, capture_output=True, text=True)
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

    def mine(self, n, addr):
        out = []
        while n > 0:
            k = min(n, 500)
            out += self.rpc("generatetoaddress", k, addr)
            n -= k
        return out


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


A = Node("A", 19700)
st = A.start()
R["binary"] = {"bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest(), "version_line": subprocess.run([BIN + "/bitcoind", "-version"], capture_output=True, text=True).stdout.splitlines()[0]}
W = "w"


def b1():
    """the node before any block: the genesis block of regtest, no wallet, the genesis coinbase"""
    R["b1_info0"] = A.rpc("getblockchaininfo")
    R["b1_nowallet"] = A.attempt("getnewaddress")
    R["b1_createwallet_empty_name"] = A.rpc_args("createwallet", "")
    R["b1_walletinfo_default"] = A.attempt("getwalletinfo")
    R["b1_listwallets"] = A.rpc("listwallets")
    R["b1_getnewaddress_default"] = A.attempt("getnewaddress")
    g = A.rpc("getblockhash", 0)
    R["b1_genesis"] = {"hash": g, "block": A.rpc("getblock", g), "header_hex": A.rpc("getblockheader", g, False), "block_hex": A.rpc("getblock", g, 0),
                       "coinbase_getrawtransaction": A.attempt("getrawtransaction", A.rpc("getblock", g)["tx"][0]),
                       "coinbase_gettxout": A.attempt("gettxout", A.rpc("getblock", g)["tx"][0], 0),
                       "txoutsetinfo": A.rpc("gettxoutsetinfo")}
    R["b1_datadir"] = sorted(os.listdir(A.dd))
    A.rpc_args("unloadwallet", "")
    A.rpc("createwallet", W)


def b2():
    """mine 500 blocks as the book does, the balance, and the halving every 150 blocks"""
    a = A.rpc("getnewaddress", wallet=W)
    R["addr"] = a
    t = time.time()
    hashes = A.mine(500, a)
    R["b2_mine500_seconds"] = round(time.time() - t, 2)
    R["b2_balance"] = A.rpc("getbalance", wallet=W)
    R["b2_balances"] = A.rpc("getbalances", wallet=W)
    R["b2_info"] = A.rpc("getblockchaininfo")
    R["b2_subsidy"] = {str(h): A.rpc("getblockstats", h, ["subsidy"])["subsidy"] for h in (1, 149, 150, 299, 300, 449, 450, 500)}
    R["b2_first_hashes"] = hashes[:2]


def hdr(h):
    return A.rpc("getblockheader", h, False)


def b3():
    """the serialized block: header, transaction counter, transactions; no size field; the blk file"""
    h = A.rpc("getblockhash", 120)
    raw = A.rpc("getblock", h, 0)
    blk = A.rpc("getblock", h, 2)
    R["b3_block"] = {"height": 120, "hash": h, "hex_head": raw[:200], "hex_bytes": len(raw) // 2, "header_hex": hdr(h), "json": {k: blk[k] for k in ("version", "versionHex", "merkleroot", "time", "mediantime", "nonce", "bits", "target", "difficulty", "chainwork", "nTx", "previousblockhash", "nextblockhash", "size", "strippedsize", "weight")}}
    d = os.path.join(A.dd, "regtest", "blocks")
    R["b3_blkfiles"] = sorted(os.listdir(d))
    f = open(os.path.join(d, "blk00000.dat"), "rb").read(8 + 285)
    key = open(os.path.join(d, "xor.dat"), "rb").read()
    R["b3_xor_key"] = key.hex()
    R["b3_blk_first_bytes_raw"] = f[:16].hex()
    dec = bytes(b ^ key[i % len(key)] for i, b in enumerate(f))
    R["b3_blk_first_bytes"] = dec[:16].hex()
    R["b3_blk_size_field"] = int.from_bytes(dec[4:8], "little")
    R["b3_blk_genesis_equals"] = dec[8:8 + 285].hex() == R["b1_genesis"]["block_hex"]
    R["b3_genesis_serialized_len"] = len(R["b1_genesis"]["block_hex"]) // 2
    # ten consecutive headers for the tamper experiment
    R["b3_headers_480_489"] = [hdr(A.rpc("getblockhash", i)) for i in range(480, 490)]
    R["b3_timestamps_110_121"] = [A.rpc("getblockheader", A.rpc("getblockhash", i))["time"] for i in range(110, 122)]
    R["b3_mediantime_121"] = A.rpc("getblockheader", A.rpc("getblockhash", 121))["mediantime"]
    R["b3_chainwork"] = {str(i): A.rpc("getblockheader", A.rpc("getblockhash", i))["chainwork"] for i in (0, 1, 2, 3)}
    R["b3_bip34"] = {}
    for i in (1, 16, 17, 127, 128, 255, 256, 500):
        b = A.rpc("getblock", A.rpc("getblockhash", i), 2)
        R["b3_bip34"][str(i)] = b["tx"][0]["vin"][0]["coinbase"][:12]


def b4():
    """blocks of 1 to 16 transactions: the merkle root the node computed against the transactions in the block"""
    out = {}
    a = A.rpc("getnewaddress", wallet=W)
    for n in (0, 1, 2, 3, 4, 5, 6, 7, 15):
        ids = []
        for i in range(n):
            ids.append(A.rpc("sendtoaddress", a, "0.01", wallet=W))
        if n == 0:
            h = A.rpc("generatetoaddress", 1, a)[0]
        else:
            h = A.rpc("generateblock", a, ids)["hash"]
        b = A.rpc("getblock", h, 1)
        out[str(len(b["tx"]))] = {"hash": h, "txids": b["tx"], "merkleroot": b["merkleroot"], "header_hex": hdr(h), "size": b["size"], "weight": b["weight"]}
    R["b4_blocks"] = out
    # the block of 4 transactions: proof for the third, verified by the node
    h4 = out["4"]["hash"]
    txid = out["4"]["txids"][2]
    proof = A.rpc("gettxoutproof", [txid], h4)
    R["b4_proof_for_third_of_4"] = {"txid": txid, "proof_hex": proof, "verify": A.rpc("verifytxoutproof", proof)}
    h16 = out["16"]["hash"]
    txid16 = out["16"]["txids"][10]
    proof16 = A.rpc("gettxoutproof", [txid16], h16)
    R["b4_proof_for_k_of_16"] = {"txid": txid16, "index": 10, "proof_hex": proof16, "verify": A.rpc("verifytxoutproof", proof16)}


def b5():
    """the mutated block of CVE-2012-2459: the same header, a duplicated last transaction"""
    a = A.rpc("getnewaddress", wallet=W)
    ids = [A.rpc("sendtoaddress", a, "0.02", wallet=W) for _ in range(2)]
    r = A.rpc("generateblock", a, ids, False)
    hexblk = r["hex"]
    blk = P.parse_block(bytes.fromhex(hexblk))
    raw = bytes.fromhex(hexblk)
    # find the transactions' byte ranges to duplicate the last one
    i = 80
    n, i = P.cs_dec(raw, i)
    starts = []
    for _ in range(n):
        starts.append(i)
        _, j = P.parse_tx_bytes(raw, i)
        i = j
    last = raw[starts[-1]:i]
    mutated = raw[:80] + P.cs_enc(n + 1) + raw[80 + len(P.cs_enc(n)):i] + last
    R["b5_mutation"] = {"n_original": n, "n_mutated": n + 1, "block_hash": r["hash"], "same_header": mutated[:80] == raw[:80],
                        "submit_mutated": A.attempt("submitblock", mutated.hex()), "count_after_mutated": A.rpc("getblockcount"),
                        "getblockheader_of_original_after_mutated": A.attempt("getblockheader", r["hash"]),
                        "submit_original": A.attempt("submitblock", hexblk), "count_after_original": A.rpc("getblockcount"),
                        "tip_is_original": A.rpc("getbestblockhash") == r["hash"]}


def b6():
    """a fork: two children of one parent; heights and hashes"""
    a = A.rpc("getnewaddress", wallet=W)
    parent = A.rpc("getbestblockhash")
    h1 = A.rpc("generatetoaddress", 1, a)[0]
    A.rpc("invalidateblock", h1)
    h2 = A.rpc("generatetoaddress", 1, A.rpc("getnewaddress", wallet=W))[0]   # another address: another coinbase, another hash
    A.rpc("reconsiderblock", h1)
    tips = A.rpc("getchaintips")
    active_before = A.rpc("getbestblockhash")
    h3 = A.rpc("generatetoaddress", 1, A.rpc("getnewaddress", wallet=W))[0]   # one more block on the active branch
    tips_after = A.rpc("getchaintips")
    R["b6_fork"] = {"parent": parent, "child1": h1, "child2": h2, "height1": A.rpc("getblockheader", h1)["height"], "height2": A.rpc("getblockheader", h2)["height"],
                    "prev1": A.rpc("getblockheader", h1)["previousblockhash"], "prev2": A.rpc("getblockheader", h2)["previousblockhash"], "tips": tips,
                    "active_before_extension": active_before, "extension": h3, "extension_prev": A.rpc("getblockheader", h3)["previousblockhash"], "tips_after": tips_after, "active_is": A.rpc("getbestblockhash")}


def b7():
    """coinbase maturity: spending a coinbase at 99 and at 100 confirmations"""
    a = A.rpc("getnewaddress", wallet=W)
    h = A.rpc("generatetoaddress", 1, a)[0]
    cb = A.rpc("getblock", h, 2)["tx"][0]
    dest = A.rpc("getnewaddress", wallet=W)
    val = cb["vout"][0]["value"]
    raw = A.rpc("createrawtransaction", [{"txid": cb["txid"], "vout": 0}], {dest: "%.8f" % (float(val) - 0.001)})
    signed = A.rpc("signrawtransactionwithwallet", raw, wallet=W)["hex"]
    res = {}
    res["confirmations_1"] = A.rpc("testmempoolaccept", [signed])[0]
    A.mine(98, a)
    res["confirmations_99"] = A.rpc("testmempoolaccept", [signed])[0]
    A.mine(1, a)
    res["confirmations_100"] = A.rpc("testmempoolaccept", [signed])[0]
    res["listunspent_note"] = "see testmempoolaccept results"
    R["b7_maturity"] = res


def b8():
    """the addresses of the chain, one of each type"""
    out = {}
    for t in ("legacy", "p2sh-segwit", "bech32", "bech32m"):
        out[t] = A.rpc("getnewaddress", "", t, wallet=W)
    R["b8_regtest_addresses"] = out


def b9():
    """other chains: testnet4, signet, a custom signet, testnet3"""
    res = {}
    for name, chain, extra, port in (("testnet4", "testnet4", [], 19720), ("signet", "signet", [], 19730), ("custom_signet", "signet", ["-signetchallenge=51"], 19740), ("testnet3_option", "testnet", [], 19750)):
        N = Node(name, port, chain, extra)
        s = N.start()
        entry = {"start": s, "extra": extra}
        if s.get("exit") == 0:
            entry["info"] = N.rpc("getblockchaininfo")
            g = N.rpc("getblockhash", 0)
            entry["genesis_hash"] = g
            entry["genesis_header_hex"] = N.rpc("getblockheader", g, False)
            N.rpc("createwallet", "t")
            entry["addresses"] = {t: N.rpc("getnewaddress", "", t, wallet="t") for t in ("legacy", "p2sh-segwit", "bech32", "bech32m")}
            entry["datadir"] = sorted(os.listdir(N.dd))
            N.stop()
        else:
            entry["datadir"] = sorted(os.listdir(N.dd))
        res[name] = entry
    R["b9_chains"] = res
    res2 = subprocess.run([BIN + "/bitcoind", "-help-debug"], capture_output=True, text=True).stdout
    R["b9_help_has"] = {k: (k in res2) for k in ("-testnet4", "-signetchallenge", "-signetseednode", "-testnet\n", "-regtest")}


for nm, fn in (("b1", b1), ("b2", b2), ("b3", b3), ("b4", b4), ("b5", b5), ("b6", b6), ("b7", b7), ("b8", b8), ("b9", b9)):
    phase(nm, fn)
R["total_seconds"] = round(time.time() - T0, 1)
A.stop()
json.dump(R, open(OUT, "w"), indent=1, sort_keys=True)
shutil.rmtree(TMP, ignore_errors=True)
print("written", OUT, R["total_seconds"], "s; errors:", list(R["errors"]))
