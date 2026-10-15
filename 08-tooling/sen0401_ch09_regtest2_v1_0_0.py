#!/usr/bin/env python3
"""SEN0401 chapter 9 (Transaction Fees): the second regtest run (Bitcoin Core 31.1, private regtest chain, no network node). The first run (sen0401_ch09_regtest_v1_0_0.py)
carries out the fee behaviour of the chapter; this one adds the experiments that the claims about signatures, lock time, dust, the option removed in 29.0, the order of a block
template and the 'twice paid' hazard of the book's RBF warning need. Writes ch09-evidence/regtest2_run_v1_0_0.json. Usage: sen0401_ch09_regtest2_v1_0_0.py [out.json]"""
__version__ = "1.0.0"
import json, os, shutil, subprocess, sys, tempfile, time, atexit

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ch09-evidence", "regtest2_run_v1_0_0.json")
DD = tempfile.mkdtemp(prefix="ch09_regtest2_", dir=os.environ.get("TMPDIR"))
PORT = "19475"
W = "w"
R = {"_version": __version__}
T0 = time.time()


class RPCError(Exception):
    pass


def rpc(method, *args, wallet=W, **named):
    c = [BIN + "/bitcoin-cli", "-regtest", "-datadir=" + DD, "-rpcport=" + PORT, "-rpcclienttimeout=600", "-stdin"]
    if wallet:
        c.append("-rpcwallet=" + wallet)
    if named:
        c.append("-named")
        lines = ["%s=%s" % (k, v if isinstance(v, str) else json.dumps(v)) for k, v in named.items()]
    else:
        lines = [a if isinstance(a, str) else json.dumps(a) for a in args]
    r = subprocess.run(c + [method], input="\n".join(lines), capture_output=True, text=True)
    if r.returncode:
        raise RPCError((r.stdout + r.stderr).strip())
    o = r.stdout.strip()
    try:
        return json.loads(o)
    except Exception:
        return o


def attempt(method, *args, wallet=W, **named):
    try:
        return {"ok": rpc(method, *args, wallet=wallet, **named)}
    except RPCError as e:
        return {"error": " ".join(str(e).split())}


def start(extra=()):
    subprocess.run([BIN + "/bitcoind", "-regtest", "-datadir=" + DD, "-daemon", "-server", "-rpcport=" + PORT, "-port=19476", "-listen=0", "-dnsseed=0", "-discover=0",
                    "-fallbackfee=0.0002", "-rpcthreads=4"] + list(extra), capture_output=True, text=True, check=True)
    for _ in range(120):
        try:
            rpc("getblockcount", wallet=None)
            return
        except RPCError:
            time.sleep(0.5)
    raise SystemExit("node did not start")


def stop():
    try:
        rpc("stop", wallet=None)
    except RPCError:
        pass
    time.sleep(3)


sat = lambda x: int(round(float(x) * 1e8))
btc = lambda s: round(s / 1e8, 8)
tip = lambda: rpc("getblockcount", wallet=None)


def mkutxo(amount):
    a = rpc("getnewaddress")
    t = rpc("send", wallet=W, outputs={a: amount}, fee_rate=5, options={"minconf": 1})["txid"]
    rpc("generatetoaddress", 1, ADDR)
    d = rpc("gettransaction", t, wallet=W)
    for det in d["details"]:
        if det["address"] == a:
            rpc("lockunspent", False, [{"txid": t, "vout": det["vout"]}])     # the wallet must not spend it by itself: the experiments spend it with raw transactions
            return {"txid": t, "vout": det["vout"], "amount": amount, "address": a, "spk": rpc("getaddressinfo", a)["scriptPubKey"]}
    raise SystemExit("utxo not found")


def build(ins, fixed, chg, fee_sat, version=2, sequence=0xfffffffd, locktime=0):
    """Signed raw transaction: inputs `ins`, outputs `fixed` ({address: BTC}), the rest minus `fee_sat` to `chg` (none when nothing is left)."""
    total = sum(sat(i["amount"]) for i in ins)
    pay = sum(sat(v) for v in fixed.values())
    vin = [{"txid": i["txid"], "vout": i["vout"], "sequence": sequence} for i in ins]
    prev = [{"txid": i["txid"], "vout": i["vout"], "scriptPubKey": i["spk"], "amount": i["amount"]} for i in ins]
    outs = [{k: v} for k, v in fixed.items()]
    if total - pay - fee_sat > 0:
        outs.append({chg: btc(total - pay - fee_sat)})
    raw = rpc("createrawtransaction", wallet=None, inputs=vin, outputs=outs, locktime=locktime, version=version)
    sg = rpc("signrawtransactionwithwallet", wallet=W, hexstring=raw, prevtxs=prev)
    return sg["hex"], rpc("decoderawtransaction", sg["hex"], wallet=None)


start()
atexit.register(lambda: (stop(), shutil.rmtree(DD, ignore_errors=True)))
R["env"] = {"version": rpc("getnetworkinfo", wallet=None)["subversion"], "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
rpc("createwallet", W, wallet=None)
ADDR = rpc("getnewaddress")
CHG = rpc("getrawchangeaddress")
rpc("generatetoaddress", 110, ADDR)

# ---- 1. the fee is signed: a transaction whose output value is changed after signing is refused
u = mkutxo(1.0)
h, d = build([u], {rpc("getnewaddress"): 0.5}, CHG, 1000)
orig = rpc("testmempoolaccept", [h], wallet=None)[0]
val = sat(d["vout"][0]["value"]).to_bytes(8, "little")
assert h.count(val.hex()) == 1
h2 = h.replace(val.hex(), (sat(d["vout"][0]["value"]) - 5000).to_bytes(8, "little").hex())
R["tamper"] = {"original_hex": h, "tampered_hex": h2, "original": orig, "tampered": rpc("testmempoolaccept", [h2], wallet=None)[0], "output0_original_sat": sat(d["vout"][0]["value"]), "output0_tampered_sat": sat(d["vout"][0]["value"]) - 5000}

# ---- 2. the book's warning: three versions of one payment that do not all conflict
a_, b_, c_ = mkutxo(1.0), mkutxo(1.0), mkutxo(1.0)
payee = rpc("getnewaddress")
v0h, v0 = build([a_], {payee: 0.4}, CHG, 1000)
v1h, v1 = build([a_, b_], {payee: 0.4}, CHG, 3000)
v2h, v2 = build([b_, c_], {payee: 0.4}, CHG, 6000)
S2 = {"v0": v0["txid"], "v1": v1["txid"], "v2": v2["txid"], "inputs": {"v0": [a_["txid"]], "v1": [a_["txid"], b_["txid"]], "v2": [b_["txid"], c_["txid"]]}, "inputs_vouts": {}}
S2["send_v0"] = attempt("sendrawtransaction", v0h, wallet=None)
S2["send_v1"] = attempt("sendrawtransaction", v1h, wallet=None)
S2["v0_in_mempool_after_v1"] = "ok" in attempt("getmempoolentry", v0["txid"], wallet=None)
S2["send_v2"] = attempt("sendrawtransaction", v2h, wallet=None)
S2["v1_in_mempool_after_v2"] = "ok" in attempt("getmempoolentry", v1["txid"], wallet=None)
# a miner that saved version 0 mines it (generateblock takes raw transactions that need not be in the mempool), then version 2 is still valid and is mined too
S2["mine_v0"] = attempt("generateblock", ADDR, [v0h], wallet=None)
S2["v2_in_mempool_after_v0_block"] = "ok" in attempt("getmempoolentry", v2["txid"], wallet=None)
S2["mine_v2"] = attempt("generateblock", ADDR, [v2h], wallet=None)
paid = 0
for th, mb in ((v0["txid"], S2["mine_v0"]), (v2["txid"], S2["mine_v2"])):
    t = rpc("getrawtransaction", th, True, mb["ok"]["hash"], wallet=None)
    paid += sum(sat(o["value"]) for o in t["vout"] if o["scriptPubKey"].get("address") == payee)
S2["payee_received_sat"] = paid
S2["payee_asked_sat"] = sat(0.4)
R["hazard"] = S2

# ---- 3. the order of a block template: highest fee rate first
us = [mkutxo(0.5) for _ in range(10)]
tx = []
rates = [1, 7, 3, 25, 12, 2, 50, 5, 18, 9]
for x, rt in zip(us, rates):
    hh, dd = build([x], {rpc("getnewaddress"): 0.2}, CHG, int(rt * 141))
    rpc("sendrawtransaction", hh, wallet=None)
    tx.append({"txid": dd["txid"], "vsize": dd["vsize"], "fee_sat": int(rt * 141), "weight": dd["weight"]})
gt = rpc("getblocktemplate", {"rules": ["segwit"]}, wallet=None)
order = [t["txid"] for t in gt["transactions"]]
R["template_order"] = {"sent": tx, "template_order": order, "template_fees": {t["txid"]: t["fee"] for t in gt["transactions"]}, "template_weights": {t["txid"]: t["weight"] for t in gt["transactions"]}}
rpc("generatetoaddress", 1, ADDR)

# ---- 4. lock time at the consensus rule: a block of height tip+1 may hold a lock time of tip, not tip+1
ul = mkutxo(1.0); um = mkutxo(1.0)
t0 = tip()
dest = rpc("getnewaddress")
hn, dn = build([ul], {dest: 0.3}, CHG, 1000, locktime=t0 + 1)       # lock time = height of the block it would join
hy, dy = build([um], {dest: 0.3}, CHG, 1000, locktime=t0)           # lock time = tip = height of the previous block
R["locktime_block"] = {"tip": t0, "next_block_height": t0 + 1, "locktime_next": t0 + 1, "locktime_tip": t0,
                       "mempool_next": rpc("testmempoolaccept", [hn], wallet=None)[0], "mempool_tip": rpc("testmempoolaccept", [hy], wallet=None)[0],
                       "block_with_next": attempt("generateblock", ADDR, [hn], wallet=None), "block_with_tip": attempt("generateblock", ADDR, [hy], wallet=None)}

# ---- 5. dust: the smallest output that is relayed, for three output types
uu = mkutxo(1.0)
dust = {}
p2wsh = rpc("getdescriptorinfo", "wsh(pk(0279be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798))", wallet=None)["descriptor"]
addr_wsh = rpc("deriveaddresses", p2wsh, wallet=None)[0]
cases = (("p2wpkh", rpc("getnewaddress"), 293), ("p2wpkh", rpc("getnewaddress"), 294), ("p2wsh", addr_wsh, 329), ("p2wsh", addr_wsh, 330),
         ("p2a", "bcrt1pfeesnyr2tx", 239), ("p2a", "bcrt1pfeesnyr2tx", 240), ("p2a", "bcrt1pfeesnyr2tx", 0))
for kind, ad, v in cases:
    hh, dd = build([uu], {ad: v / 1e8}, CHG, 1000)
    dust["%s_%d" % (kind, v)] = {"result": rpc("testmempoolaccept", [hh], wallet=None)[0], "vsize": dd["vsize"]}
R["dust"] = dust

# ---- 6. the wallet's own minimum fee rate against the node's relay minimum
wm = {}
for fr in (0.5, 1, 0.1):
    wm["fee_rate_%s" % fr] = attempt("send", outputs={rpc("getnewaddress"): 0.01}, fee_rate=fr, options={"minconf": 1})
R["wallet_min"] = wm
R["wallet_settings"] = {k: rpc("getwalletinfo")[k] for k in ("paytxfee",) if k in rpc("getwalletinfo")}
R["mempool_min"] = {k: rpc("getmempoolinfo", wallet=None)[k] for k in ("mempoolminfee", "minrelaytxfee", "incrementalrelayfee", "fullrbf", "limitclustercount", "limitclustersize", "maxmempool")}
rpc("generatetoaddress", 1, ADDR)
stop()

# ---- 7. the option removed in 29.0: a node started with it (a second data directory, no wallet, no mining)
d2 = tempfile.mkdtemp(prefix="ch09_opt_", dir=os.environ.get("TMPDIR"))
try:
    r = subprocess.run([BIN + "/bitcoind", "-regtest", "-datadir=" + d2, "-mempoolfullrbf=0", "-rpcport=19477", "-port=19478", "-listen=0", "-printtoconsole"], capture_output=True, text=True, timeout=60)
    R["removed_option"] = {"exit_code": r.returncode, "message": " ".join((r.stdout + r.stderr).split())[:400]}
except subprocess.TimeoutExpired:
    R["removed_option"] = {"exit_code": None, "message": "the node kept running (the option was accepted)"}
    attempt("stop", wallet=None)
shutil.rmtree(d2, ignore_errors=True)
R["phase"] = {"total_s": round(time.time() - T0, 1)}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(R, open(OUT, "w"), indent=1)
print("written", OUT, "in", R["phase"]["total_s"], "s")
