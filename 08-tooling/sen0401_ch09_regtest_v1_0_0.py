#!/usr/bin/env python3
"""SEN0401 chapter 9 (Transaction Fees): the regtest run. Starts Bitcoin Core 31.1 (the release binary from bitcoincore.org, sha256 checked against SHA256SUMS)
on a private regtest chain in a temporary data directory (no network node: -listen=0 -dnsseed=0 -connect=0), carries out every fee behaviour the chapter describes
and writes everything the node answered to ch09-evidence/regtest_run_v1_0_0.json. The chapter's claims later recompute from that file with an independent
transaction parser (sen0401_ch09_lib_v1_0_0.py). One run, one record: the fee-estimation history is random (fixed seed) and the keys are fresh, so a rerun gives other
txids and other numbers; the file records the run the claims were checked against.
Usage: sen0401_ch09_regtest_v1_0_0.py [out.json]   Environment: BITCOIN_BIN (directory of bitcoind and bitcoin-cli), TMPDIR."""
__version__ = "1.0.0"
import json, os, random, shutil, subprocess, sys, tempfile, time, hashlib, platform

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.environ.get("BITCOIN_BIN", "/home/claude/core31/bitcoin-31.1/bin")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "ch09-evidence", "regtest_run_v1_0_0.json")
DD = tempfile.mkdtemp(prefix="ch09_regtest_", dir=os.environ.get("TMPDIR"))
W = "w"
R = {"_version": __version__}
T0 = time.time()


class RPCError(Exception):
    pass


def rpc(method, *args, wallet=W, **named):
    """One bitcoin-cli call; the arguments go through standard input (-stdin), one per line, so that a transaction with thousands of outputs fits."""
    c = [BIN + "/bitcoin-cli", "-regtest", "-datadir=" + DD, "-rpcport=19473", "-rpcclienttimeout=600", "-stdin"]
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
    """Like rpc, but returns {'ok': value} or {'error': text} so a refusal is recorded as data."""
    try:
        return {"ok": rpc(method, *args, wallet=wallet, **named)}
    except RPCError as e:
        return {"error": " ".join(str(e).split())}


def start(extra=()):
    subprocess.run([BIN + "/bitcoind", "-regtest", "-datadir=" + DD, "-daemon", "-server", "-rpcport=19473", "-listen=0", "-dnsseed=0", "-discover=0", "-fallbackfee=0.0002",
                    "-rpcthreads=4"] + list(extra), capture_output=True, text=True, check=True)
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


def sat(x):
    return int(round(float(x) * 1e8))


def btc(s):
    return round(s / 1e8, 8)


CUR_ARGS = []


def restart():
    stop()
    start(CUR_ARGS)
    attempt("loadwallet", W, wallet=None)


def tcheck(label):
    """Does a block template hold every transaction of the mempool? (every transaction here is valid and mineable). Recorded after each phase."""
    n = len(rpc("getblocktemplate", {"rules": ["segwit"]}, wallet=None)["transactions"])
    m = rpc("getmempoolinfo", wallet=None)["size"]
    R.setdefault("template_check", []).append({"after": label, "template_txs": n, "mempool_txs": m})


def drain():
    """Mine until the mempool is empty. If a block leaves the mempool as it was (observed once with Bitcoin Core 31.1 after some phase), record it and restart the node."""
    stalls = 0
    while True:
        m = rpc("getmempoolinfo", wallet=None)["size"]
        if not m:
            return
        rpc("generatetoaddress", 1, ADDR)
        if rpc("getmempoolinfo", wallet=None)["size"] >= m:
            stalls += 1
            R.setdefault("stalls", []).append({"mempool": m, "tip": tip(), "template_txs": len(rpc("getblocktemplate", {"rules": ["segwit"]}, wallet=None)["transactions"])})
            if stalls > 3:
                mp = rpc("getrawmempool", True, wallet=None)
                R["stall_mempool"] = {k: {"vsize": v["vsize"], "fee": v["fees"]["base"], "anc": v["ancestorcount"], "desc": v["descendantcount"], "bip125": v.get("bip125-replaceable")} for k, v in list(mp.items())[:40]}
                gt = rpc("getblocktemplate", {"rules": ["segwit"]}, wallet=None)
                R["stall_template"] = {k: gt.get(k) for k in ("weightlimit", "sizelimit", "sigoplimit", "height")}
                R["stall_args"] = list(CUR_ARGS)
                json.dump(R, open(OUT + ".partial", "w"), indent=1, default=str)
                raise SystemExit("mempool does not drain even after restarts")
            restart()


def tip():
    return rpc("getblockcount", wallet=None)


def pay(address, amount, fee_rate):
    """The wallet pays `amount` to `address` at `fee_rate` sat/vB, spending confirmed coins only (minconf 1)."""
    return rpc("send", wallet=W, outputs={address: amount}, fee_rate=fee_rate, options={"minconf": 1})["txid"]


def mkutxo(amount):
    """A confirmed wallet output of exactly `amount` BTC; returns (txid, vout, amount)."""
    a = rpc("getnewaddress")
    t = pay(a, amount, 5)
    rpc("generatetoaddress", 1, ADDR)
    d = rpc("gettransaction", t, wallet=W)
    for det in d["details"]:
        if det["address"] == a:
            return {"txid": t, "vout": det["vout"], "amount": amount, "address": a}
    raise SystemExit("utxo not found")


def build(ins, fixed, change_addr, feerate, version=2, sequence=0xfffffffd, locktime=0, fee=None, change=True):
    """Signed raw transaction spending `ins` (list of utxo dicts), paying `fixed` ({address: BTC}), the rest to change after `feerate` sat/vB
    (or exactly `fee` satoshis). Two passes: the size is only known after signing. Returns (hex, decoded)."""
    total = sum(sat(i["amount"]) for i in ins)
    pay = sum(sat(v) for v in fixed.values())
    vin = [{"txid": i["txid"], "vout": i["vout"], "sequence": sequence} for i in ins]
    prev = [{"txid": i["txid"], "vout": i["vout"], "scriptPubKey": i["spk"], "amount": i["amount"]} for i in ins if "spk" in i]
    f = fee if fee is not None else 0
    for _ in range(3):
        outs = [{k: v} for k, v in fixed.items()]
        ch = total - pay - f
        if change and ch > 0:
            outs.append({change_addr: btc(ch)})
        raw = rpc("createrawtransaction", wallet=None, inputs=vin, outputs=outs, locktime=locktime, version=version)
        sg = rpc("signrawtransactionwithwallet", wallet=W, hexstring=raw, **({"prevtxs": prev} if prev else {}))
        dec = rpc("decoderawtransaction", sg["hex"], wallet=None)
        if fee is not None:
            break
        nf = int(-(-feerate * dec["vsize"] // 1))
        if nf == f:
            break
        f = nf
    return sg["hex"], dec


def utxo_of(txhex_dec, n, addr_hint=None):
    o = txhex_dec["vout"][n]
    return {"txid": txhex_dec["txid"], "vout": n, "amount": o["value"], "spk": o["scriptPubKey"]["hex"]}


def rec_tx(hexs, dec=None):
    dec = dec or rpc("decoderawtransaction", hexs, wallet=None)
    return {"txid": dec["txid"], "hex": hexs, "weight": dec["weight"], "vsize": dec["vsize"], "size": dec["size"], "version": dec["version"], "locktime": dec["locktime"]}


# ---------------------------------------------------------------------------------------------------------------- setup
R["env"] = {"python": platform.python_version(), "platform": platform.platform(), "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "bitcoind_sha256": hashlib.sha256(open(BIN + "/bitcoind", "rb").read()).hexdigest()}
start()
import atexit
atexit.register(lambda: (stop(), shutil.rmtree(DD, ignore_errors=True)))
R["env"]["version"] = rpc("getnetworkinfo", wallet=None)["subversion"]
R["env"]["connections"] = rpc("getconnectioncount", wallet=None)
rpc("createwallet", W, wallet=None)
ADDR = rpc("getnewaddress")
rpc("generatetoaddress", 110, ADDR)
R["mempoolinfo_fresh"] = rpc("getmempoolinfo", wallet=None)
R["estimate_fresh"] = attempt("estimatesmartfee", 144, wallet=None)
R["phase"] = {"setup_s": round(time.time() - T0, 1)}

# ---------------------------------------------------------------------------------------------------------------- fee estimation history
t = time.time()
random.seed(9)
for k in range(8):
    rpc("sendmany", "", {rpc("getnewaddress"): 0.5 for _ in range(60)})
rpc("generatetoaddress", 1, ADDR)
sent = 0
ROUNDS = int(os.environ.get("CH09_ROUNDS", "120"))
for rnd in range(ROUNDS):
    for i in range(22):
        fr = max(1.0, round(random.choice([1, 1, 2, 3, 5, 8, 12, 20, 35, 60, 100]) * random.uniform(0.8, 1.25), 2))
        pay(ADDR, 0.01, fr)
        sent += 1
    mp = rpc("getrawmempool", True, wallet=None)
    top = sorted(mp, key=lambda x: -mp[x]["fees"]["base"] / mp[x]["vsize"])
    pick = [x for x in top if not mp[x]["depends"]][:20]
    rpc("generateblock", ADDR, pick, wallet=W)
est = {}
for tgt in (2, 6, 25, 144):
    for mode in ("economical", "conservative"):
        est["%d_%s" % (tgt, mode)] = attempt("estimatesmartfee", conf_target=tgt, estimate_mode=mode, wallet=None)
    est["%d_default" % tgt] = attempt("estimatesmartfee", conf_target=tgt, wallet=None)
tcheck("estimation history")
R["estimate"] = {"rounds": ROUNDS, "sent": sent, "mined_per_block": 20, "results": est, "mempool_left": rpc("getmempoolinfo", wallet=None)["size"],
                 "tip": tip(), "listing_call": "bitcoin-cli -named estimatesmartfee conf_target=144"}
drain()
R["phase"]["estimation_s"] = round(time.time() - t, 1)

# ---------------------------------------------------------------------------------------------------------------- fee = inputs - outputs
t = time.time()
u20 = mkutxo(20.0)
dest = rpc("getnewaddress")
u20["spk"] = rpc("getaddressinfo", u20["address"])["scriptPubKey"]
hx, dec = build([u20], {dest: 1.0}, None, 0, fee=0, change=False)
tm = rpc("testmempoolaccept", [hx], wallet=None)[0]
snd = attempt("sendrawtransaction", hx, wallet=None)
sent_ok = rpc("sendrawtransaction", wallet=None, hexstring=hx, maxfeerate=0)
me = rpc("getmempoolentry", sent_ok, wallet=None)
bh = rpc("generatetoaddress", 1, ADDR)[0]
bs = rpc("getblockstats", bh, wallet=None)
blk = rpc("getblock", bh, 2, wallet=None)
cb = blk["tx"][0]
tcheck("fee arithmetic")
R["fee_arith"] = {"tx": rec_tx(hx, dec), "inputs_btc": 20.0, "outputs_btc": 1.0, "testmempoolaccept": tm, "sendrawtransaction_default": snd,
                  "mempoolentry_fees": me["fees"], "mempoolentry_vsize": me["vsize"], "block": bh, "blockstats": {k: bs[k] for k in ("subsidy", "totalfee", "height", "txs")},
                  "coinbase_out_sat": sum(sat(o["value"]) for o in cb["vout"]), "tip_after": tip()}

# ---------------------------------------------------------------------------------------------------------------- units
ua = mkutxo(1.0)
ua["spk"] = rpc("getaddressinfo", ua["address"])["scriptPubKey"]
base_raw = rpc("createrawtransaction", wallet=None, inputs=[{"txid": ua["txid"], "vout": ua["vout"]}], outputs=[{rpc("getnewaddress"): 0.1}])
U = {}
U["fee_rate_sat_vb_10"] = attempt("fundrawtransaction", hexstring=base_raw, options={"fee_rate": 10, "lockUnspents": False, "add_inputs": False, "changeAddress": rpc("getrawchangeaddress")})
U["feeRate_btc_kvb_0.0001"] = attempt("fundrawtransaction", hexstring=base_raw, options={"feeRate": 0.0001, "add_inputs": False, "changeAddress": rpc("getrawchangeaddress")})
U["feeRate_btc_kvb_10"] = attempt("fundrawtransaction", hexstring=base_raw, options={"feeRate": 10, "add_inputs": False, "changeAddress": rpc("getrawchangeaddress")})
U["fee_rate_sat_vb_1e6"] = attempt("fundrawtransaction", hexstring=base_raw, options={"fee_rate": 1000000, "add_inputs": False, "changeAddress": rpc("getrawchangeaddress")})
U["fee_rate_sat_vb_0.0001"] = attempt("fundrawtransaction", hexstring=base_raw, options={"fee_rate": 0.0001, "add_inputs": False, "changeAddress": rpc("getrawchangeaddress")})
for k, v in U.items():
    if "ok" in v:
        d = rpc("decoderawtransaction", v["ok"]["hex"], wallet=None)
        v["ok"] = {"fee": v["ok"]["fee"], "changepos": v["ok"]["changepos"], "vsize_unsigned": d["vsize"], "hex": v["ok"]["hex"]}
tcheck("units")
R["units"] = U

# ---------------------------------------------------------------------------------------------------------------- replace by fee
RB = {}
ur = mkutxo(1.0); ur["spk"] = rpc("getaddressinfo", ur["address"])["scriptPubKey"]
payee = rpc("getnewaddress"); chg = rpc("getrawchangeaddress")
h1, d1 = build([ur], {payee: 0.5}, chg, 2.0, sequence=0xffffffff)
rpc("sendrawtransaction", h1, wallet=None)
RB["fullrbf_flag"] = rpc("getmempoolinfo", wallet=None)["fullrbf"]
RB["t1"] = dict(rec_tx(h1, d1), sequence=d1["vin"][0]["sequence"], fee_sat=sat(rpc("getmempoolentry", d1["txid"], wallet=None)["fees"]["base"]))
h2, d2 = build([ur], {payee: 0.5}, chg, 4.0, sequence=0xffffffff)
r2 = attempt("sendrawtransaction", h2, wallet=None)
RB["t2"] = dict(rec_tx(h2, d2), sequence=d2["vin"][0]["sequence"], result=r2)
RB["t1_still_in_mempool"] = "ok" in attempt("getmempoolentry", d1["txid"], wallet=None)
f2 = sat(rpc("getmempoolentry", d2["txid"], wallet=None)["fees"]["base"]); RB["t2"]["fee_sat"] = f2
# equal fee, lower fee, fee short of the incremental relay fee by one satoshi, fee exactly enough
hs, ds = build([ur], {payee: 0.49999}, chg, 0, fee=f2)          # different output amount, same absolute fee
RB["equal_fee"] = dict(rec_tx(hs, ds), fee_sat=f2, result=attempt("sendrawtransaction", hs, wallet=None))
hl, dl = build([ur], {payee: 0.5}, chg, 0, fee=f2 - 50)
RB["lower_fee"] = dict(rec_tx(hl, dl), fee_sat=f2 - 50, result=attempt("sendrawtransaction", hl, wallet=None))
inc = d2["vsize"]  # incremental relay fee 0.1 sat/vB: the replacement needs ceil(0.1 * vsize_replacement) more satoshis than the replaced fee
hb = {}
for extra in (None,):
    pass
probe = build([ur], {payee: 0.5}, chg, 0, fee=f2 + 1)[1]
need = -(-probe["vsize"] // 10)   # ceil(0.1 * vsize)
RB["incremental"] = {"old_fee_sat": f2, "replacement_vsize": probe["vsize"], "need_extra_sat": need}
h_short, d_short = build([ur], {payee: 0.5}, chg, 0, fee=f2 + need - 1)
RB["short_by_one"] = dict(rec_tx(h_short, d_short), fee_sat=f2 + need - 1, result=attempt("sendrawtransaction", h_short, wallet=None))
h_ok, d_ok = build([ur], {payee: 0.5}, chg, 0, fee=f2 + need)
RB["exactly_enough"] = dict(rec_tx(h_ok, d_ok), fee_sat=f2 + need, result=attempt("sendrawtransaction", h_ok, wallet=None))
RB["mempool_after"] = list(rpc("getrawmempool", wallet=None))
# BIP 125 wallet path: the wallet's own transactions signal replaceability; bumpfee replaces
sw = pay(rpc("getnewaddress"), 0.2, 2)
dsw = rpc("getrawtransaction", sw, True, wallet=None)
fee_before = sat(-rpc("gettransaction", sw)["fee"])
bf = attempt("bumpfee", sw)
RB["bumpfee"] = {"orig_txid": sw, "orig_sequences": [v["sequence"] for v in dsw["vin"]], "orig_fee_sat": fee_before, "orig_vsize": dsw["vsize"], "result": bf,
                 "orig_in_mempool_after": "ok" in attempt("getmempoolentry", sw, wallet=None)}
if "ok" in bf:
    RB["bumpfee"]["new_fee_sat"] = sat(bf["ok"]["fee"]); RB["bumpfee"]["new_tx"] = rpc("getrawtransaction", bf["ok"]["txid"], True, wallet=None)["vsize"]
tcheck("replace by fee")
drain()
R["rbf"] = RB

# ---------------------------------------------------------------------------------------------------------------- minimum relay fee
MR = {}
um = mkutxo(1.0); um["spk"] = rpc("getaddressinfo", um["address"])["scriptPubKey"]
probe = build([um], {rpc("getnewaddress"): 0.5}, chg, 1.0)[1]
vs = probe["vsize"]
for name, fee in (("below_0.05", -(-vs * 5 // 100)), ("just_below", -(-vs // 10) - 1), ("exact_0.1", -(-vs // 10))):
    h, d = build([um], {rpc("getnewaddress"): 0.5}, chg, 0, fee=fee)
    MR[name] = {"fee_sat": fee, "vsize": d["vsize"], "result": attempt("testmempoolaccept", [h], wallet=None)}
MR["mempoolinfo"] = {k: R["mempoolinfo_fresh"][k] for k in ("mempoolminfee", "minrelaytxfee", "incrementalrelayfee")}
R["minrelay"] = MR

# ---------------------------------------------------------------------------------------------------------------- packages, TRUC, ephemeral anchors
PK = {}
up = mkutxo(1.0); up["spk"] = rpc("getaddressinfo", up["address"])["scriptPubKey"]
uc = mkutxo(1.0); uc["spk"] = rpc("getaddressinfo", uc["address"])["scriptPubKey"]
P2A = "bcrt1pfeesnyr2tx"
# 1. a zero-fee version 3 parent with an anchor output of value 0, and a child that pays for both
hp, dp = build([up], {P2A: 0.0}, chg, 0, version=3, fee=0)
PK["truc_parent"] = rec_tx(hp, dp)
PK["parent_alone"] = attempt("sendrawtransaction", hp, wallet=None)
anchor = {"txid": dp["txid"], "vout": 0, "amount": 0, "scriptPubKey": "51024e73"}
vin = [{"txid": dp["txid"], "vout": 0, "sequence": 0xfffffffd}, {"txid": uc["txid"], "vout": uc["vout"], "sequence": 0xfffffffd}]
for fee in (10000,):
    ch_raw = rpc("createrawtransaction", wallet=None, inputs=vin, outputs=[{chg: btc(sat(uc["amount"]) - fee)}], version=3)
    ch_sg = rpc("signrawtransactionwithwallet", wallet=W, hexstring=ch_raw, prevtxs=[anchor, {"txid": uc["txid"], "vout": uc["vout"], "scriptPubKey": uc["spk"], "amount": uc["amount"]}])
    PK["anchor_child"] = dict(rec_tx(ch_sg["hex"]), fee_sat=fee, spent_value_sat=sat(uc["amount"]), anchor_witness_empty=True)
PK["child_alone"] = attempt("sendrawtransaction", ch_sg["hex"], wallet=None)
PK["submitpackage_truc"] = attempt("submitpackage", [hp, ch_sg["hex"]], wallet=None)
# parent really sits at fee 0 and the package rate is (0 + 10000) / (vsize_parent + vsize_child)
rpc("generatetoaddress", 1, ADDR)
PK["after_mining"] = {"mempool": rpc("getmempoolinfo", wallet=None)["size"]}
# 2. an ordinary (version 2) parent below the minimum relay feerate, rescued by a child (the 28.0 limit lifted by 31.0 for non-TRUC parents)
un = mkutxo(1.0); un["spk"] = rpc("getaddressinfo", un["address"])["scriptPubKey"]
uo = mkutxo(1.0); uo["spk"] = rpc("getaddressinfo", uo["address"])["scriptPubKey"]
hpar, dpar = build([un], {rpc("getnewaddress"): 0.3}, chg, 0.05)
pinfo = rec_tx(hpar, dpar); pinfo["fee_sat"] = sat(1.0) - sum(sat(o["value"]) for o in dpar["vout"])
PK["v2_parent"] = pinfo
PK["v2_parent_alone"] = attempt("testmempoolaccept", [hpar], wallet=None)
chg_out = [i for i, o in enumerate(dpar["vout"]) if o["scriptPubKey"]["address"] == chg][0]
cin = utxo_of(dpar, chg_out)
hch, dch = build([cin, uo], {rpc("getnewaddress"): 0.2}, rpc("getrawchangeaddress"), 50.0)
PK["v2_child"] = rec_tx(hch, dch)
PK["submitpackage_v2"] = attempt("submitpackage", [hpar, hch], wallet=None)
tcheck("packages")
drain()
R["package"] = PK

# TRUC rules
TR = {}
ut = mkutxo(2.0); ut["spk"] = rpc("getaddressinfo", ut["address"])["scriptPubKey"]
a1, a2 = rpc("getnewaddress"), rpc("getnewaddress")
hp3, dp3 = build([ut], {a1: 0.3, a2: 0.3}, chg, 5.0, version=3)
rpc("sendrawtransaction", hp3, wallet=None)
TR["parent"] = rec_tx(hp3, dp3)
o1 = [i for i, o in enumerate(dp3["vout"]) if o["scriptPubKey"]["address"] == a1][0]
o2 = [i for i, o in enumerate(dp3["vout"]) if o["scriptPubKey"]["address"] == a2][0]
for n, a in ((o1, a1), (o2, a2)):
    pass
c1_in = dict(utxo_of(dp3, o1)); c2_in = dict(utxo_of(dp3, o2))
c1h, c1d = build([c1_in], {rpc("getnewaddress"): 0.1}, chg, 5.0, version=3)
TR["child1"] = dict(rec_tx(c1h, c1d), result=attempt("sendrawtransaction", c1h, wallet=None))
c2h, c2d = build([c2_in], {rpc("getnewaddress"): 0.1}, chg, 5.0, version=3)
TR["sibling_same_rate"] = dict(rec_tx(c2h, c2d), result=attempt("sendrawtransaction", c2h, wallet=None))
c2bh, c2bd = build([c2_in], {rpc("getnewaddress"): 0.1}, chg, 20.0, version=3)
TR["sibling_higher_rate"] = dict(rec_tx(c2bh, c2bd), result=attempt("sendrawtransaction", c2bh, wallet=None),
                                 child1_in_mempool_after="ok" in attempt("getmempoolentry", c1d["txid"], wallet=None))
c3h, c3d = build([c1_in], {rpc("getnewaddress"): 0.1}, chg, 5.0, version=2)
TR["v2_child_of_v3"] = dict(rec_tx(c3h, c3d), result=attempt("sendrawtransaction", c3h, wallet=None))
big_outs = {rpc("getnewaddress"): 0.001 for _ in range(40)}
c4h, c4d = build([c2_in], big_outs, chg, 30.0, version=3)
TR["big_child"] = dict(rec_tx(c4h, c4d), result=attempt("sendrawtransaction", c4h, wallet=None))
tcheck("truc")
drain()
R["truc"] = TR

# ---------------------------------------------------------------------------------------------------------------- cluster limits (the old 25/101 kvB chain limit, the new 64-transaction cluster)
CL = {"mempoolinfo": {k: rpc("getmempoolinfo", wallet=None)[k] for k in ("limitclustercount", "limitclustersize")}}
uch = mkutxo(5.0); uch["spk"] = rpc("getaddressinfo", uch["address"])["scriptPubKey"]
cur = uch
chain = []
res = []
for i in range(70):
    h, d = build([cur], {rpc("getnewaddress"): btc(sat(cur["amount"]) - 300)}, None, 0, fee=300, change=False)
    r = attempt("sendrawtransaction", h, wallet=None)
    res.append({"n": i + 1, "txid": d["txid"], "accepted": "ok" in r, "error": r.get("error")})
    if "error" in r:
        break
    cur = utxo_of(d, 0)
CL["chain"] = {"attempted": len(res), "accepted": sum(1 for x in res if x["accepted"]), "first_refusal": next((x for x in res if not x["accepted"]), None),
               "accepted_26th": res[25]["accepted"] if len(res) > 25 else None, "tail": res[-3:]}
tcheck("cluster chain")
drain()
R["cluster"] = CL

# ---------------------------------------------------------------------------------------------------------------- the pinning example of the chapter
PIN = {}
for label, ver in (("v2", 2), ("v3", 3)):
    ua_ = mkutxo(1.0); ua_["spk"] = rpc("getaddressinfo", ua_["address"])["scriptPubKey"]
    bob = rpc("getnewaddress")
    hP, dP = build([ua_], {bob: 0.2}, chg, 5.0, version=ver)
    rpc("sendrawtransaction", hP, wallet=None)
    pf = sat(rpc("getmempoolentry", dP["txid"], wallet=None)["fees"]["base"])
    bo = [i for i, o in enumerate(dP["vout"]) if o["scriptPubKey"]["address"] == bob][0]
    bin_ = utxo_of(dP, bo)
    n_out = 2900 if ver == 2 else 25
    outs = {rpc("getnewaddress"): 0.00005 for _ in range(n_out)} if n_out < 100 else None
    if outs is None:
        desc = [d["desc"] for d in rpc("listdescriptors")["descriptors"] if d["desc"].startswith("wpkh(") and not d["internal"]][0]
        pool = rpc("deriveaddresses", desc, [1000, 1000 + n_out - 1], wallet=None)
        vin = [{"txid": bin_["txid"], "vout": bin_["vout"], "sequence": 0xfffffffd}]
        olist = [{pool[i]: 0.00005} for i in range(n_out)]
        # distinct outputs with the same address are allowed in a raw transaction only as a list of single-pair objects
        total = sat(bin_["amount"]); pay_sat = n_out * 5000
        for f in (0, 1):
            pass
        fee_c = 0
        for _ in range(3):
            o2 = list(olist) + [{chg: btc(total - pay_sat - fee_c)}]
            raw = rpc("createrawtransaction", wallet=None, inputs=vin, outputs=o2, version=ver)
            sg = rpc("signrawtransactionwithwallet", wallet=W, hexstring=raw, prevtxs=[{"txid": bin_["txid"], "vout": bin_["vout"], "scriptPubKey": bin_["spk"], "amount": bin_["amount"]}])
            dC = rpc("decoderawtransaction", sg["hex"], wallet=None)
            nf = int(-(-5.0 * dC["vsize"] // 1))
            if nf == fee_c:
                break
            fee_c = nf
        hC = sg["hex"]
    else:
        hC, dC = build([bin_], outs, chg, 5.0, version=ver)
    rc = attempt("sendrawtransaction", hC, wallet=None)
    cf = fee_c if n_out >= 100 else None
    if cf is None:
        cf = sat(rpc("getmempoolentry", dC["txid"], wallet=None)["fees"]["base"]) if "ok" in rc else None
    # Alice replaces her payment: same input, a HIGHER feerate (6 sat/vB), different payee
    hR, dR = build([ua_], {rpc("getnewaddress"): 0.2}, chg, 6.0, version=ver)
    rr = attempt("sendrawtransaction", hR, wallet=None)
    need_fee = None
    PIN[label] = {"parent": dict(rec_tx(hP, dP), fee_sat=pf), "child": dict(rec_tx(hC, dC), fee_sat=cf, result=rc), "replacement_at_6": dict(rec_tx(hR, dR), fee_sat=int(-(-6.0 * dR["vsize"] // 1)), result=rr)}
    if "ok" in rc:
        want = pf + cf + -(-dR["vsize"] // 10)
        hR2, dR2 = build([ua_], {rpc("getnewaddress"): 0.2}, chg, 0, version=ver, fee=want)
        r3 = attempt("sendrawtransaction", hR2, wallet=None)
        PIN[label]["replacement_enough"] = dict(rec_tx(hR2, dR2), fee_sat=want, result=r3)
        PIN[label]["child_still_in_mempool"] = "ok" in attempt("getmempoolentry", dC["txid"], wallet=None)
    tcheck("pinning " + label)
    drain()
R["pinning"] = PIN

# ---------------------------------------------------------------------------------------------------------------- lock time: the fee sniping defence and its boundary
SN = {"samples": []}
for i in range(60):
    h = tip()
    txid = pay(ADDR, 0.001, 2)
    d = rpc("getrawtransaction", txid, True, wallet=None)
    SN["samples"].append({"tip": h, "locktime": d["locktime"], "sequences": [v["sequence"] for v in d["vin"]], "type_in": d["vin"][0].get("txinwitness") is not None})
tcheck("sniping samples")
drain()
h_tip = tip()
usn = mkutxo(1.0); usn["spk"] = rpc("getaddressinfo", usn["address"])["scriptPubKey"]
h_tip = tip()
edge = {}
for name, lt, seq in (("locktime_eq_tip", h_tip, 0xfffffffd), ("locktime_tip_plus_1", h_tip + 1, 0xfffffffd), ("locktime_tip_plus_1_final_sequence", h_tip + 1, 0xffffffff)):
    h, d = build([usn], {rpc("getnewaddress"): 0.5}, chg, 3.0, locktime=lt, sequence=seq)
    edge[name] = {"tip": h_tip, "locktime": lt, "sequence": seq, "result": rpc("testmempoolaccept", [h], wallet=None)[0]}
SN["edge"] = edge
# the same transaction becomes valid once the tip has moved
rpc("generatetoaddress", 1, ADDR)
h, d = build([usn], {rpc("getnewaddress"): 0.5}, chg, 3.0, locktime=h_tip + 1, sequence=0xfffffffd)
SN["edge_after_one_block"] = {"tip": tip(), "locktime": h_tip + 1, "result": rpc("testmempoolaccept", [h], wallet=None)[0]}
R["sniping"] = SN
R["phase"]["rules_s"] = round(time.time() - T0, 1)

# ---------------------------------------------------------------------------------------------------------------- ancestor-feerate mining under a tiny block (restart with -blockmaxweight)
drain()
# the inputs of both scenarios are made BEFORE the node is restarted with a tiny block (a wallet payment may need two inputs and then does not fit the tiny block)
PRE = []
for _ in range(6):
    x = mkutxo(1.0); x["spk"] = rpc("getaddressinfo", x["address"])["scriptPubKey"]; PRE.append(x)
drain()
CUR_ARGS[:] = ["-blockreservedweight=2000", "-blockmaxweight=" + os.environ.get("CH09_MAXW", "3600") + ""]
restart()
AM = {"node_args": ["-blockreservedweight=2000", "-blockmaxweight=" + os.environ.get("CH09_MAXW", "3600") + ""], "mempoolinfo": rpc("getmempoolinfo", wallet=None)["fullrbf"]}


def scenario(name, child_rate):
    out = {}
    ua2, ub2, uc2 = PRE.pop(), PRE.pop(), PRE.pop()
    dest = rpc("getnewaddress")
    hA, dA = build([ua2], {dest: 0.5}, chg, 20.0, sequence=0xfffffffd)
    hP, dP = build([ub2], {dest: 0.5}, chg, 1.0)
    chg_i = [i for i, o in enumerate(dP["vout"]) if o["scriptPubKey"]["address"] == chg][0]
    # the child spends the parent's CHANGE output (0.5 BTC minus fee) and pays the rest to a fresh address
    hC, dC = build([utxo_of(dP, chg_i)], {rpc("getnewaddress"): 0.1}, rpc("getrawchangeaddress"), child_rate)
    for hh in (hP, hC, hA):
        rpc("sendrawtransaction", hh, wallet=None)
    ent = {k: rpc("getmempoolentry", d["txid"], wallet=None) for k, d in (("A", dA), ("P", dP), ("C", dC))}
    bh = rpc("generatetoaddress", 1, ADDR)[0]
    blk = rpc("getblock", bh, 1, wallet=None)
    out = {"A": rec_tx(hA, dA), "P": rec_tx(hP, dP), "C": rec_tx(hC, dC), "child_rate_sat_vb": child_rate, "mempoolentries": {k: {kk: v.get(kk) for kk in ("vsize", "weight", "fees", "chunkfee", "chunkweight") if kk in v} for k, v in ent.items()},
           "block_txids": blk["tx"], "block_weight": blk["weight"]}
    out["fees_sat"] = {k: sat(ent[k]["fees"]["base"]) for k in ent}
    return out


AM["cpfp_wins"] = scenario("cpfp_wins", 100.0)
drain()
AM["cpfp_loses"] = scenario("cpfp_loses", 5.0)
R["ancestor_mining"] = AM
R["phase"]["total_s"] = round(time.time() - T0, 1)
stop()
shutil.rmtree(DD, ignore_errors=True)
os.makedirs(os.path.dirname(OUT), exist_ok=True)
json.dump(R, open(OUT, "w"), indent=1)
print("written", OUT, "in", R["phase"]["total_s"], "s")
