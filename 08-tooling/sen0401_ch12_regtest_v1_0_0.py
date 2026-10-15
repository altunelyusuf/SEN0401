#!/usr/bin/env python3
"""SEN0401 chapter 12 (Mining and Consensus): the regtest run. Starts Bitcoin Core 31.1 nodes (the release binary of bitcoincore.org, sha256 in the record) on private chains in temporary data
directories and records what the nodes answered in ch12-evidence/regtest_run_v1_0_0.json: the block template and the coinbase it prescribes, the subsidy and the fees, the ordering of a template by
fee rate, the extra nonce, the checklist of a transaction and the checklist of a block (each rule broken once, on purpose, with the reason the node gives), the median time past, the
proof-of-work search done by this script, a double spend by a longer chain, the state machine of a version-bits deployment, and a strict and a lax node (one rule with two activation heights)
that split the chain. Nothing here touches the public network (-dnsseed=0 -listen=0 -connect=0 -fixedseeds=0); the nodes never talk to each other, blocks are handed over with submitblock.
One run, one record: hashes, keys and timings differ on a rerun; the chapter's claims are checked against the record of the saved run.
Usage: sen0401_ch12_regtest_v1_0_0.py [out.json] [--only b1,b2]   Environment: BITCOIN_BIN (directory of bitcoind and bitcoin-cli), TMPDIR."""
__version__ = "1.0.0"
import hashlib, json, os, shutil, struct, subprocess, sys, tempfile, time, traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
import sen0401_ch12_lib_v1_0_0 as L

BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
args = [a for a in sys.argv[1:] if not a.startswith("--") and not (a.startswith("b") and a[1:].isdigit())]
OUT = args[0] if args else os.path.join(HERE, "ch12-evidence", "regtest_run_v1_0_0.json")
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
TMP = tempfile.mkdtemp(prefix="ch12_regtest_", dir=os.environ.get("TMPDIR"))
R = {"_version": __version__, "phase": {}, "errors": {}}
T0 = time.time()
BITS = "207fffff"


class RPCError(Exception):
    pass


NODES = []


class Node:
    def __init__(self, name, port_base, chain="regtest", extra=()):
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
            if N is not A:
                N.stop()
    R["phase"][name] = round(time.time() - t, 1)
    print("phase", name, R["phase"][name], "s", flush=True)


A = Node("A", 19900)
st = A.start()
R["binary"] = {"bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest(), "version_line": subprocess.run([BIN + "/bitcoind", "-version"], capture_output=True, text=True).stdout.splitlines()[0]}
W = "w"
A.rpc("createwallet", W)
ADDR = A.rpc("getnewaddress", wallet=W)
PK = A.spk(ADDR, W)


def tip_info():
    h = A.rpc("getbestblockhash")
    return h, A.rpc("getblockheader", h)


def b1():
    """the first block: what a template says before anything is mined, the coinbase the node writes, the height in it, the witness commitment"""
    t = A.rpc("getblocktemplate", {"rules": ["segwit"]})
    R["b1_template0"] = {k: t[k] for k in ("version", "rules", "vbavailable", "vbrequired", "previousblockhash", "coinbasevalue", "target", "mintime", "mutable", "noncerange", "sigoplimit", "sizelimit", "weightlimit", "curtime", "bits", "height", "default_witness_commitment") if k in t}
    R["b1_template0"]["n_transactions"] = len(t["transactions"])
    R["b1_template0_keys"] = sorted(t)
    R["b1_mininginfo0"] = A.rpc("getmininginfo")
    h = A.rpc("generatetoaddress", 1, ADDR)[0]
    blk = A.rpc("getblock", h, 2)
    cb = blk["tx"][0]
    R["b1_block1"] = {"hash": h, "nTx": blk["nTx"], "version": blk["version"], "versionHex": blk["versionHex"], "bits": blk["bits"], "target": blk.get("target"), "weight": blk["weight"], "size": blk["size"]}
    R["b1_coinbase"] = {"txid": cb["txid"], "hash": cb["hash"], "version": cb["version"], "locktime": cb["locktime"], "vin": cb["vin"], "vout": cb["vout"], "size": cb["size"], "weight": cb["weight"], "vsize": cb["vsize"],
                        "hex": A.rpc("getrawtransaction", cb["txid"], False, h)}
    R["b1_getblock_raw_header"] = A.rpc("getblockheader", h, False)


def b2():
    """a longer chain: the subsidy at the edges of every halving (every 150 blocks on regtest), the difficulty that never changes (regtest does not retarget), the supply"""
    A.mine(2100, ADDR)
    R["b2_info"] = A.rpc("getblockchaininfo")
    R["b2_subsidy"] = {str(h): A.rpc("getblockstats", h, ["subsidy"])["subsidy"] for h in (1, 149, 150, 151, 299, 300, 449, 450, 1000, 2000)}
    R["b2_bits"] = {str(h): A.rpc("getblockheader", A.rpc("getblockhash", h))["bits"] for h in (1, 2015, 2016, 2017, 2100)}
    R["b2_times"] = {str(h): A.rpc("getblockheader", A.rpc("getblockhash", h))["time"] for h in (1, 2016, 2100)}
    R["b2_txoutset"] = A.rpc("gettxoutsetinfo")
    R["b2_total_amount_btc"] = R["b2_txoutset"]["total_amount"]
    R["b2_mining0"] = A.rpc("getmininginfo")


def raw_tx(vin, vout, locktime=0, version=2):
    """a non-segwit transaction from bytes; vin = [(txid_display, n, sequence)], vout = [(value, script_bytes)] (value may be out of range on purpose)"""
    s = struct.pack("<I", version) + P.cs_enc(len(vin))
    for txid, n, seq in vin:
        s += bytes.fromhex(txid)[::-1] + struct.pack("<I", n) + b"\x00" + struct.pack("<I", seq)
    s += P.cs_enc(len(vout))
    for v, sc in vout:
        s += struct.pack("<q", v) + P.cs_enc(len(sc)) + sc
    return (s + struct.pack("<I", locktime)).hex()


def b3():
    """the checklist of a transaction, rule by rule: each transaction is broken in one place and the reason of testmempoolaccept is recorded"""
    res = {}
    a2 = A.rpc("getnewaddress", wallet=W)
    unspent = [u for u in A.rpc("listunspent", 1, 9999999, [], True, wallet=W) if u["confirmations"] > 110 and u["amount"] > 1]
    u = unspent[0]
    u2 = unspent[1]
    def tm(hx):
        try:
            return A.rpc("testmempoolaccept", [hx])[0]
        except RPCError as e:
            return {"rpc_error": " ".join(str(e).split())[:300]}
    good = A.rpc("signrawtransactionwithwallet", A.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {a2: round(u["amount"] - 0.001, 8)}), wallet=W)["hex"]
    res["valid"] = tm(good)
    res["no_inputs"] = tm(A.rpc("createrawtransaction", [], {a2: 1}))
    res["no_outputs"] = tm(A.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {}))
    spk2 = A.spk(a2, W)
    res["negative_output"] = tm(raw_tx([(u["txid"], u["vout"], 0xffffffff)], [(-1, spk2)]))
    res["output_over_21_million"] = tm(raw_tx([(u["txid"], u["vout"], 0xffffffff)], [(2100000000000001, spk2)]))
    res["total_over_21_million"] = tm(raw_tx([(u["txid"], u["vout"], 0xffffffff)], [(2100000000000000, spk2), (2100000000000000, spk2)]))
    res["duplicate_input"] = tm(raw_tx([(u["txid"], u["vout"], 0xffffffff), (u["txid"], u["vout"], 0xffffffff)], [(1000, spk2)]))
    res["unknown_input"] = tm(raw_tx([("11" * 32, 0, 0xffffffff)], [(1000, spk2)]))
    over = A.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {a2: round(u["amount"] + 1, 8)})
    res["outputs_exceed_inputs"] = tm(A.rpc("signrawtransactionwithwallet", over, wallet=W)["hex"])
    res["unsigned"] = tm(A.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"]}], {a2: round(u["amount"] - 0.001, 8)}))
    lk = A.rpc("createrawtransaction", [{"txid": u["txid"], "vout": u["vout"], "sequence": 0xfffffffe}], {a2: round(u["amount"] - 0.001, 8)}, 5000)
    res["locktime_in_the_future"] = tm(A.rpc("signrawtransactionwithwallet", lk, wallet=W)["hex"])
    res["_locktime_note"] = {"height_now": A.rpc("getblockcount"), "locktime": 5000}
    # coinbase maturity: spend a coinbase at 1, 99 and 100 confirmations
    h = A.rpc("generatetoaddress", 1, ADDR)[0]
    cb = A.rpc("getblock", h, 2)["tx"][0]
    dest = A.rpc("getnewaddress", wallet=W)
    rawc = A.rpc("createrawtransaction", [{"txid": cb["txid"], "vout": 0}], {dest: round(float(cb["vout"][0]["value"]) - 0.001, 8)})
    sg = A.rpc("signrawtransactionwithwallet", rawc, wallet=W)["hex"]
    res["coinbase_1_confirmation"] = tm(sg)
    A.mine(98, ADDR)
    res["coinbase_99_confirmations"] = tm(sg)
    A.mine(1, ADDR)
    res["coinbase_100_confirmations"] = tm(sg)
    R["b3_tx_checklist"] = res
    R["b3_coinbase_maturity_const"] = "COINBASE_MATURITY"


def tip_for_block():
    h, hd = tip_info()
    ht = hd["height"] + 1
    return h, hd, ht


def b4():
    """the checklist of a block: a valid block is built from bytes and then broken in one place at a time; submitblock names the reason"""
    res = {}
    h, hd, ht = tip_for_block()
    info = A.rpc("getblockchaininfo")
    mtp, now = info["mediantime"], int(time.time())
    t0 = max(now, mtp + 1)
    bl = lambda **kw: L.build_block(h, ht, kw.pop("t", t0), kw.pop("bits", BITS), PK, **kw)
    sub = L.subsidy(ht, 150)
    R["b4_context"] = {"tip": h, "height_next": ht, "mediantime": mtp, "now": now, "subsidy_next": sub, "t0": t0}
    # each rule broken once; every block is built on the same parent, none is kept (the valid one is submitted last)
    res["merkle_root_wrong"] = A.submit(bl(merkle_override="aa" * 32, mine=True)["hex"])
    bad = bl(mine=False, nonce=0)
    n = 0
    while True:
        cand = bl(mine=False, nonce=n)
        if int(cand["hash"], 16) > L.bits_to_target(BITS):
            break
        n += 1
    res["proof_of_work_missing"] = A.submit(cand["hex"])
    R["b4_pow_fail_nonce"] = {"nonce": n, "hash": cand["hash"], "target": hex(L.bits_to_target(BITS))}
    res["time_equal_to_median_time_past"] = A.submit(bl(t=mtp)["hex"])
    res["time_two_hours_and_a_second_ahead"] = A.submit(bl(t=now + 7201)["hex"])
    res["reward_one_satoshi_too_high"] = A.submit(bl(value=sub + 1)["hex"])
    res["no_height_in_coinbase"] = A.submit(bl(bip34=False, extra=b"\x51\x51")["hex"])
    res["version_1"] = A.submit(bl(version=1)["hex"])
    res["wrong_difficulty_bits"] = A.submit(bl(bits="2000ffff")["hex"])
    res["coinbase_script_1_byte"] = A.submit(bl(ss_override=b"\x51")["hex"])
    res["coinbase_script_101_bytes"] = A.submit(bl(ss_override=L.push_num(ht) + b"\x51" * (101 - len(L.push_num(ht))))["hex"])
    # a coinbase twice: the second transaction is a coinbase too
    ctx2, full2, _ = L.coinbase_tx(ht, 0, PK, b"second")
    blk2 = bl(txs=[full2], txids=[ctx2])
    res["second_coinbase"] = A.submit(blk2["hex"])
    # first transaction not a coinbase
    unspent = [u for u in A.rpc("listunspent", 1, 9999999, [], True, wallet=W) if u["confirmations"] > 100][0]
    a2 = A.rpc("getnewaddress", wallet=W)
    stx = A.rpc("signrawtransactionwithwallet", A.rpc("createrawtransaction", [{"txid": unspent["txid"], "vout": unspent["vout"]}], {a2: round(unspent["amount"] - 0.001, 8)}), wallet=W)["hex"]
    stxid = A.rpc("decoderawtransaction", stx)["txid"]
    nocb = L.header_bytes(0x20000000, h, stxid, t0, BITS, 0)
    nonce, hh, _ = L.grind(0x20000000, h, stxid, t0, BITS)
    nocb = L.header_bytes(0x20000000, h, stxid, t0, BITS, nonce) + P.cs_enc(1) + bytes.fromhex(stx)
    res["first_transaction_not_a_coinbase"] = A.submit(nocb.hex())
    # a block heavier than 4,000,000 weight units: 130,000 outputs of 10 bytes each are 1.3 MB without witness data
    heavy = bl(extra_outputs=[(0, b"\x51")] * 130000)
    res["weight_over_the_limit"] = A.submit(heavy["hex"])
    R["b4_heavy"] = {"bytes": len(heavy["hex"]) // 2, "weight_if_no_witness": 4 * (len(heavy["hex"]) // 2)}
    # the valid block, last, is accepted; and the same block with a reward of less than the subsidy is another valid block (not submitted)
    ok = bl()
    R["b4_valid"] = {"hash": ok["hash"], "attempts": ok["attempts"], "nonce": ok["nonce"], "merkle": ok["merkle"], "coinbase_txid": ok["coinbase_txid"]}
    res["valid_block"] = A.submit(ok["hex"])
    R["b4_rules"] = res
    R["b4_height_after"] = A.rpc("getblockcount")
    R["b4_tip_is_valid"] = A.rpc("getbestblockhash") == ok["hash"]


def b5():
    """the reward: the subsidy plus the fees, the template that orders by fee rate, the extra nonce, the witness commitment, a miner that takes less"""
    a2 = A.rpc("getnewaddress", wallet=W)
    fees = {}
    ids = {}
    for rate in (2, 50, 10, 200):
        txid = A.rpc("sendtoaddress", wallet=W, address=a2, amount="0.5", fee_rate=rate)
        ids[rate] = txid
    t = A.rpc("getblocktemplate", {"rules": ["segwit"]})
    R["b5_template"] = {k: t[k] for k in ("version", "previousblockhash", "coinbasevalue", "target", "bits", "height", "curtime", "mintime", "default_witness_commitment", "sigoplimit", "sizelimit", "weightlimit", "coinbaseaux", "mutable") if k in t}
    R["b5_template"]["transactions"] = [{k: x[k] for k in ("txid", "hash", "fee", "weight", "sigops") if k in x} for x in t["transactions"]]
    R["b5_fee_rate_to_txid"] = {str(k): v for k, v in ids.items()}
    R["b5_mempool_entries"] = {str(k): {"vsize": A.rpc("getmempoolentry", v)["vsize"], "fee": A.rpc("getmempoolentry", v)["fees"]["base"]} for k, v in ids.items()}
    sub = L.subsidy(t["height"], 150)
    total_fee = sum(x["fee"] for x in t["transactions"])
    R["b5_reward"] = {"subsidy": sub, "fees": total_fee, "coinbasevalue": t["coinbasevalue"]}
    commit = bytes.fromhex(t["default_witness_commitment"])
    txs = [x["data"] for x in t["transactions"]]
    txids = [x["txid"] for x in t["transactions"]]
    prev, ht, bits = t["previousblockhash"], t["height"], t["bits"]
    tm = max(t["curtime"], t["mintime"])
    value = t["coinbasevalue"]
    # the extra nonce: the same transactions, two coinbases that differ in their extra bytes
    v1 = L.build_block(prev, ht, tm, bits, PK, value=value, extra=b"extranonce-1", txs=txs, txids=txids, commit_script=commit)
    v2 = L.build_block(prev, ht, tm, bits, PK, value=value, extra=b"extranonce-2", txs=txs, txids=txids, commit_script=commit)
    R["b5_extranonce"] = {"merkle_1": v1["merkle"], "merkle_2": v2["merkle"], "hash_1": v1["hash"], "hash_2": v2["hash"], "nonce_1": v1["nonce"], "nonce_2": v2["nonce"], "coinbase_txid_1": v1["coinbase_txid"], "coinbase_txid_2": v2["coinbase_txid"]}
    # a block that claims one satoshi more than subsidy + fees, then a block that claims one less
    over = L.build_block(prev, ht, tm, bits, PK, value=value + 1, extra=b"greedy", txs=txs, txids=txids, commit_script=commit)
    R["b5_greedy_submit"] = A.submit(over["hex"])
    under = L.build_block(prev, ht, tm, bits, PK, value=value - 1, extra=b"modest", txs=txs, txids=txids, commit_script=commit)
    R["b5_modest"] = {"hash": under["hash"], "submit": A.submit(under["hex"]), "height_after": A.rpc("getblockcount")}
    blk = A.rpc("getblock", under["hash"], 2)
    cb = blk["tx"][0]
    R["b5_modest"]["coinbase_output_sat"] = round(cb["vout"][0]["value"] * 1e8)
    R["b5_modest"]["total_fees_sat"] = round(total_fee)
    R["b5_modest"]["order_in_block"] = [x["txid"] for x in blk["tx"][1:]]
    R["b5_modest"]["mempool_after"] = A.rpc("getrawmempool")
    # the witness commitment, recomputed from the wtxids of the block
    wt = ["00" * 32] + [x["hash"] for x in blk["tx"][1:]]
    root = L.merkle_root(wt)
    com = [o for o in cb["vout"] if o["scriptPubKey"]["hex"].startswith("6a24aa21a9ed")][0]
    R["b5_witness_commitment"] = {"wtxids": wt, "witness_root": root, "reserved_value": "00" * 32, "commitment_in_block": com["scriptPubKey"]["hex"][12:], "recomputed": L.sha256d(bytes.fromhex(root)[::-1] + bytes(32)).hex(),
                                  "script": com["scriptPubKey"]["hex"], "template_commitment": t["default_witness_commitment"], "merkle_of_block": blk["merkleroot"], "txids_merkle": L.merkle_root([x["txid"] for x in blk["tx"]])}
    R["b5_coinbase_of_block"] = {"scriptsig": cb["vin"][0]["coinbase"], "witness": cb["vin"][0].get("txinwitness"), "n_outputs": len(cb["vout"])}
    # what the node itself writes into the coinbase of a template block (the first block of this phase's chain was mined by generatetoaddress)
    h2 = A.rpc("generatetoaddress", 1, ADDR)[0]
    cb2 = A.rpc("getblock", h2, 2)["tx"][0]
    R["b5_core_coinbase"] = {"scriptsig": cb2["vin"][0]["coinbase"], "height": A.rpc("getblockcount"), "locktime": cb2["locktime"], "sequence": cb2["vin"][0]["sequence"], "n_outputs": len(cb2["vout"]), "version": cb2["version"]}


def b6():
    """the 80 bytes are searched: a proof-of-work run by this script at the difficulty of regtest, and at two harder targets (more zero bits), with the number of attempts of each"""
    h, hd, ht = tip_for_block()
    out = {}
    pk = PK
    for bits, label in (("207fffff", "regtest"), ("1f00ffff", "bits 1f00ffff"), ("1e0fffff", "bits 1e0fffff")):
        t0 = time.time()
        ctxid, cfull, _ = L.coinbase_tx(ht, 5000000000, pk, b"pow")
        mr = L.merkle_root([ctxid])
        nonce, hh, att = L.grind(0x20000000, h, mr, int(time.time()), bits)
        out[label] = {"bits": bits, "nonce": nonce, "hash": hh, "attempts": att, "zero_bits": L.leading_zero_bits(hh), "seconds": round(time.time() - t0, 2), "expected_attempts": round(2 ** 256 / (L.bits_to_target(bits) + 1))}
    R["b6_grind"] = out


def b7():
    """two nodes, one chain: Mallory's payment to Carol is confirmed on node M, then a longer chain made by node B replaces it. Fresh chains, so that the subsidy is still 50 coins"""
    M = Node("M", 19910)
    M.start()
    Bn = Node("B", 19920)
    Bn.start()
    Bn.rpc("createwallet", "b")
    Wa, Wc = "m", "c"
    M.rpc("createwallet", Wa)
    M.rpc("createwallet", Wc)
    ma = M.rpc("getnewaddress", wallet=Wa)
    ca = M.rpc("getnewaddress", wallet=Wc)
    bpk_addr = Bn.rpc("getnewaddress", wallet="b")
    M.rpc("generatetoaddress", 101, ma)
    top = M.rpc("getblockcount")
    for i in range(1, top + 1):
        Bn.rpc("submitblock", M.rpc("getblock", M.rpc("getblockhash", i), 0))
    R["b7_sync"] = {"M": top, "B": Bn.rpc("getblockcount"), "same_tip": M.rpc("getbestblockhash") == Bn.rpc("getbestblockhash")}
    u = [x for x in M.rpc("listunspent", 1, 9999999, [], True, wallet=Wa) if x["amount"] >= 49][0]
    inp = [{"txid": u["txid"], "vout": u["vout"]}]
    amt = round(u["amount"] - 0.001, 8)
    pay = M.rpc("signrawtransactionwithwallet", M.rpc("createrawtransaction", inp, {ca: amt}), wallet=Wa)["hex"]
    back = M.rpc("signrawtransactionwithwallet", M.rpc("createrawtransaction", inp, {ma: amt}), wallet=Wa)["hex"]
    pay_id = M.rpc("decoderawtransaction", pay)["txid"]
    back_id = M.rpc("decoderawtransaction", back)["txid"]
    R["b7_txs"] = {"pay_to_carol": pay_id, "back_to_mallory": back_id, "input": u["txid"] + ":" + str(u["vout"]), "amount": amt}
    parent = M.rpc("getbestblockhash")
    xb = M.rpc("generateblock", ma, [pay])
    R["b7_before"] = {"block_x": xb["hash"], "carol_received": M.rpc("getreceivedbyaddress", ca, 1, wallet=Wc), "pay_confirmations": M.rpc("gettransaction", pay_id, wallet=Wc)["confirmations"], "height": M.rpc("getblockcount"),
                      "tips": M.rpc("getchaintips")}
    y1 = Bn.rpc("generateblock", bpk_addr, [back])
    y2 = Bn.rpc("generatetoaddress", 1, bpk_addr)[0]
    R["b7_chain_b"] = {"y1": y1["hash"], "y2": y2, "height_b": Bn.rpc("getblockcount"), "y1_prev": Bn.rpc("getblockheader", y1["hash"])["previousblockhash"], "parent": parent}
    R["b7_deliver_y1"] = M.submit(Bn.rpc("getblock", y1["hash"], 0))
    R["b7_after_equal_work"] = {"height": M.rpc("getblockcount"), "tips": M.rpc("getchaintips"), "pay_confirmations": M.rpc("gettransaction", pay_id, wallet=Wc)["confirmations"]}
    R["b7_deliver_y2"] = M.submit(Bn.rpc("getblock", y2, 0))
    gt = M.rpc("gettransaction", pay_id, wallet=Wc)
    R["b7_after"] = {"height": M.rpc("getblockcount"), "tip_is_y2": M.rpc("getbestblockhash") == y2, "tips": M.rpc("getchaintips"), "pay_confirmations": gt["confirmations"], "pay_walletconflicts": gt.get("walletconflicts"),
                     "carol_received": M.rpc("getreceivedbyaddress", ca, 1, wallet=Wc), "carol_received_0conf": M.rpc("getreceivedbyaddress", ca, 0, wallet=Wc), "mempool": M.rpc("getrawmempool"),
                     "back_confirmations": M.rpc("gettransaction", back_id, wallet=Wa)["confirmations"], "chainwork_tip": M.rpc("getblockheader", y2)["chainwork"], "chainwork_x": M.rpc("getblockheader", xb["hash"])["chainwork"]}
    Bn.stop()
    M.stop()


def b8():
    """the version-bits state machine on a private chain: a deployment that every block signals for, and one that nobody signals for; the block versions"""
    out = {}
    for name, extra, port in (("V", ["-vbparams=testdummy:0:9999999999"], 19930), ("F", ["-vbparams=testdummy:0:1", "-blockversion=536870912"], 19940)):
        N = Node(name, port, extra=extra)
        N.start()
        N.rpc("createwallet", "w")
        a = N.rpc("getnewaddress", wallet="w")
        rows = []
        for n in (143, 1, 143, 1, 143, 1):
            N.rpc("generatetoaddress", n, a)
            d = N.rpc("getdeploymentinfo")["deployments"]["testdummy"]
            rows.append({"height": N.rpc("getblockcount"), "status": d["bip9"].get("status"), "status_next": d["bip9"].get("status_next"), "statistics": d["bip9"].get("statistics"), "active": d.get("active"), "activation_height": d.get("height")})
        out[name] = {"rows": rows, "params": extra, "version_of_tip": N.rpc("getblockheader", N.rpc("getbestblockhash"))["versionHex"], "deploymentinfo": N.rpc("getdeploymentinfo")["deployments"]["testdummy"]}
        N.stop()
    R["b8_versionbits"] = out


def b9():
    """one rule, two activation heights: a strict node (the height in the coinbase is required, as BIP 34 says) and a lax node (the rule starts at height 100000); a block that the lax node accepts
    and the strict node refuses splits the chain, and a block of the strict chain is accepted by both"""
    S = Node("S", 19950)
    Lx = Node("L", 19960, extra=["-testactivationheight=bip34@100000"])
    S.start(), Lx.start()
    for N in (S, Lx):
        N.rpc("createwallet", "w")
    a = S.rpc("getnewaddress", wallet="w")
    pk = S.spk(a, "w")
    S.mine(3, a)
    for i in range(1, 4):
        Lx.rpc("submitblock", S.rpc("getblock", S.rpc("getblockhash", i), 0))
    R["b9_start"] = {"S": S.rpc("getblockcount"), "L": Lx.rpc("getblockcount"), "info_S": S.rpc("getdeploymentinfo")["deployments"]["bip34"], "info_L": Lx.rpc("getdeploymentinfo")["deployments"]["bip34"]}
    tip = S.rpc("getbestblockhash")
    t = S.rpc("getblockheader", tip)["time"] + 1
    lax = L.build_block(tip, 4, t, BITS, pk, bip34=False, extra=b"\x51\x51")
    R["b9_lax_block"] = {"hash": lax["hash"], "lax_node": Lx.submit(lax["hex"]), "strict_node": S.submit(lax["hex"]), "height_L": Lx.rpc("getblockcount"), "height_S": S.rpc("getblockcount")}
    # the lax chain goes on: two more blocks that carry no height
    prev = lax["hash"]
    for k in (5, 6):
        b = L.build_block(prev, k, t + k, BITS, pk, bip34=False, extra=b"\x51\x51" + bytes([k]))
        Lx.submit(b["hex"])
        prev = b["hash"]
    strict_try = S.submit(b["hex"])
    R["b9_lax_chain"] = {"height_L": Lx.rpc("getblockcount"), "tip_L": Lx.rpc("getbestblockhash"), "height_S": S.rpc("getblockcount"), "tip_S": S.rpc("getbestblockhash"), "strict_node_on_block_6": strict_try,
                         "same_tip": Lx.rpc("getbestblockhash") == S.rpc("getbestblockhash"), "tips_S": S.rpc("getchaintips"), "tips_L": Lx.rpc("getchaintips")}
    # the strict side: blocks with the height, extended by the strict node; the lax node accepts them as well, and takes the longer chain
    prev = tip
    strict_blocks = []
    for k in range(4, 10):
        b = L.build_block(prev, k, t + 100 + k, BITS, pk, extra=b"s" + bytes([k]))
        strict_blocks.append(b)
        prev = b["hash"]
    res = [{"height": 4 + i, "strict": S.submit(b["hex"]), "lax": Lx.submit(b["hex"])} for i, b in enumerate(strict_blocks)]
    R["b9_strict_chain"] = {"results": res, "height_S": S.rpc("getblockcount"), "height_L": Lx.rpc("getblockcount"), "same_tip": S.rpc("getbestblockhash") == Lx.rpc("getbestblockhash"), "tips_L": Lx.rpc("getchaintips")}
    # a block of version 1: the strict node refuses it for its version, the lax node (rule not yet active at its height) takes it
    tip2 = S.rpc("getbestblockhash")
    v1 = L.build_block(tip2, 10, t + 200, BITS, pk, version=1)
    R["b9_version_1"] = {"strict": S.submit(v1["hex"]), "lax": Lx.submit(v1["hex"])}
    for N in (S, Lx):
        N.stop()


def b10():
    """a node that is told a different block version: the blocks it mines carry it, and what a rolled version looks like to the validation (bits of BIP 320 set in the version)"""
    N = Node("V2", 19970, extra=["-blockversion=%d" % 0x2000e000])
    N.start()
    N.rpc("createwallet", "w")
    a = N.rpc("getnewaddress", wallet="w")
    N.mine(3, a)
    h = N.rpc("getbestblockhash")
    hdr = N.rpc("getblockheader", h)
    R["b10_rolled"] = {"versionHex": hdr["versionHex"], "accepted_height": N.rpc("getblockcount"), "rolled_bits": hex(hdr["version"] & 0x1fffe000), "top3": hdr["version"] >> 29}
    N.stop()


def b11():
    """the options of the node that belong to mining, from the binary's own help"""
    h = subprocess.run([BIN + "/bitcoind", "-help-debug"], capture_output=True, text=True).stdout
    R["b11_help_has"] = {k: (k in h) for k in ("-blockreservedweight", "-blockmintxfee", "-blockversion", "-vbparams", "-testactivationheight", "-ipcbind", "-blockmaxweight")}


for nm, fn in (("b1", b1), ("b2", b2), ("b3", b3), ("b4", b4), ("b5", b5), ("b6", b6), ("b7", b7), ("b8", b8), ("b9", b9), ("b10", b10), ("b11", b11)):
    phase(nm, fn)
R["total_seconds"] = round(time.time() - T0, 1)
A.stop()
json.dump(R, open(OUT, "w"), indent=1, sort_keys=True)
shutil.rmtree(TMP, ignore_errors=True)
print("written", OUT, R["total_seconds"], "s; errors:", list(R["errors"]))
