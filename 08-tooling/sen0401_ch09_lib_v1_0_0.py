#!/usr/bin/env python3
"""SEN0401 chapter 9 (Transaction Fees): the library the chapter's executed claims call. Standard library only.
* text(), has(): read a saved source (08-tooling/ch09-evidence) and test that a passage is in it (whitespace collapsed).
* parse_tx(): an independent Bitcoin transaction parser (version, inputs, outputs, witness, lock time, txid, weight, virtual size), used to recompute from the raw
  hex the node answered with everything the node said about size and fees.
* run(): the recorded regtest run (sen0401_ch09_regtest_v1_0_0.py, Bitcoin Core 31.1); every value read from it is a SINGLE-RUN value.
* the small rules of the chapter written as functions: virtual size, fee rate, units, the signal of opt-in RBF, IsFinalTx, the replacement fee, the subsidy,
  the success probability of fee sniping, the package fee rate, the census of two mainnet blocks."""
__version__ = "1.0.0"
import hashlib, html, json, math, os, re, statistics
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.join(HERE, "ch09-evidence")
_T = {}


def text(fname):
    """The saved source as one string, whitespace collapsed; html and pdf copies are read through their .txt conversion."""
    if fname not in _T:
        p = os.path.join(EV, fname)
        if fname.endswith(".html") or fname.endswith(".pdf"):
            p = os.path.splitext(p)[0] + ".txt"
        s = open(p, errors="replace").read()
        if p.endswith(".txt") and fname.endswith(".html"):
            s = html.unescape(s)
        _T[fname] = re.sub(r"\s+", " ", s)
    return _T[fname]


def has(fname, *frags):
    t = text(fname)
    return all(f in t for f in frags)


def const(fname, name):
    """The value of a C++ constant or a markdown definition: `name{...}`, `name = ...;` or `name=...` in a saved source (first match), as written."""
    t = text(fname)
    m = re.search(re.escape(name) + r"\s*(?:\{|=)\s*([^;}\s,]+)", t)
    return m.group(1) if m else None


# ------------------------------------------------------------------------------------------------ transactions
def sha256d(b):
    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def _cs(b, i):
    n = b[i]
    if n < 253:
        return n, i + 1
    if n == 253:
        return int.from_bytes(b[i + 1:i + 3], "little"), i + 3
    if n == 254:
        return int.from_bytes(b[i + 1:i + 5], "little"), i + 5
    return int.from_bytes(b[i + 1:i + 9], "little"), i + 9


def _enc_cs(n):
    if n < 253:
        return bytes([n])
    if n < 65536:
        return b"\xfd" + n.to_bytes(2, "little")
    return b"\xfe" + n.to_bytes(4, "little")


def parse_tx(h):
    b = bytes.fromhex(h)
    i = 0
    ver = int.from_bytes(b[0:4], "little", signed=True); i = 4
    segwit = b[i] == 0 and b[i + 1] == 1
    if segwit:
        i += 2
    n, i = _cs(b, i)
    vin = []
    for _ in range(n):
        txid = b[i:i + 32][::-1].hex(); vout = int.from_bytes(b[i + 32:i + 36], "little"); i += 36
        sl, i = _cs(b, i); ss = b[i:i + sl]; i += sl
        seq = int.from_bytes(b[i:i + 4], "little"); i += 4
        vin.append({"txid": txid, "vout": vout, "scriptSig": ss.hex(), "sequence": seq, "witness": []})
    n, i = _cs(b, i)
    vout = []
    for _ in range(n):
        v = int.from_bytes(b[i:i + 8], "little"); i += 8
        sl, i = _cs(b, i); vout.append({"value": v, "spk": b[i:i + sl].hex()}); i += sl
    if segwit:
        for k in range(len(vin)):
            c, i = _cs(b, i)
            for _ in range(c):
                l, i = _cs(b, i); vin[k]["witness"].append(b[i:i + l].hex()); i += l
    lock = int.from_bytes(b[i:i + 4], "little"); i += 4
    assert i == len(b), "trailing bytes"
    base = ver.to_bytes(4, "little", signed=True) + _enc_cs(len(vin))
    for x in vin:
        base += bytes.fromhex(x["txid"])[::-1] + x["vout"].to_bytes(4, "little") + _enc_cs(len(x["scriptSig"]) // 2) + bytes.fromhex(x["scriptSig"]) + x["sequence"].to_bytes(4, "little")
    base += _enc_cs(len(vout))
    for o in vout:
        base += o["value"].to_bytes(8, "little") + _enc_cs(len(o["spk"]) // 2) + bytes.fromhex(o["spk"])
    base += lock.to_bytes(4, "little")
    weight = len(base) * 3 + len(b)
    return {"version": ver, "vin": vin, "vout": vout, "locktime": lock, "txid": sha256d(base)[::-1].hex(), "size": len(b), "base_size": len(base), "weight": weight,
            "vsize": -(-weight // 4), "segwit": segwit}


def vsize_of_weight(w):
    return -(-w // 4)


# ------------------------------------------------------------------------------------------------ the recorded run and the census
_RUN = {}


def run(name="regtest_run_v1_0_0.json"):
    if name not in _RUN:
        _RUN[name] = json.load(open(os.path.join(EV, name)))
    return _RUN[name]


def run2():
    """The second recorded run (sen0401_ch09_regtest2_v1_0_0.py): tamper, the three versions, template order, lock time at the block, dust, wallet minimum, the removed option."""
    return run("regtest2_run_v1_0_0.json")


def ev_json(name):
    if name not in _RUN:
        _RUN[name] = json.load(open(os.path.join(EV, name)))
    return _RUN[name]


def reason(a):
    """The node's reason in an attempt record {'error': 'error code: -26 error message: <reason>'} (empty when the call succeeded)."""
    e = a.get("error", "")
    return e.split("error message:", 1)[-1].strip() if e else ""


def census():
    if "census" not in _RUN:
        _RUN["census"] = json.load(open(os.path.join(EV, "mainnet_fee_census_v1_0_0.json")))
    return _RUN["census"]


def census_stats(height):
    """For the first transactions of a mainnet block (the coinbase excluded): how many, how many signal opt-in RBF (some input sequence below 0xfffffffe),
    how many carry lock time equal to the previous block height (the wallet defence), how many a lock time of 0, the median fee rate in sat/vB (fee over weight/4)."""
    b = census()["blocks"][str(height)]
    tx = [t for t in b["txs"] if not t["vin"][0]["coinbase"]]
    n = len(tx)
    sig = sum(1 for t in tx if rbf_signal([v["sequence"] for v in t["vin"]]))
    snipe = sum(1 for t in tx if t["locktime"] == height - 1)
    zero = sum(1 for t in tx if t["locktime"] == 0)
    rates = sorted(t["fee"] / (t["weight"] / 4) for t in tx)
    return {"n": n, "signal_rbf": sig, "locktime_prev_height": snipe, "locktime_zero": zero, "median_rate": round(statistics.median(rates), 2)}


# ------------------------------------------------------------------------------------------------ rules
def rbf_signal(seqs):
    """BIP 125: a transaction signals replaceability when at least one input has a sequence number below 0xfffffffe."""
    return any(s < 0xfffffffe for s in seqs)


def is_final(locktime, height, seqs, block_time=0):
    """Consensus IsFinalTx for a block of the given height: final when the lock time is 0, or below the height (a height lock time) or the time, or every input is final."""
    if locktime == 0:
        return True
    if locktime < (height if locktime < 500_000_000 else block_time):
        return True
    return all(s == 0xffffffff for s in seqs)


def conflict(a, b):
    """Two transactions conflict when they spend a common outpoint (here: sets of input labels)."""
    return bool(set(a) & set(b))


def min_replacement_fee(old_fee_sat, new_vsize, incremental_sat_per_kvb=100):
    """BIP 125 rule 4 with Bitcoin Core's incremental relay fee: the replacement must pay at least the replaced fee plus the incremental fee times its own size."""
    return old_fee_sat + -(-new_vsize * incremental_sat_per_kvb // 1000)


def subsidy(height):
    h = height // 210000
    return 0 if h >= 64 else (50 * 100_000_000) >> h


def snipe_probability(x):
    """Optech: with every other miner honest, a miner with share x of the hash rate wins the race to re-mine the last block and extend it with probability (x / (1 - x)) ** 2."""
    return (x / (1 - x)) ** 2


def feerate(fee_sat, vsize):
    return fee_sat / vsize


def btc_kvb_to_sat_vb(s):
    """A feerate printed in BTC per kilo-vbyte (the unit of estimatesmartfee) as satoshi per vbyte, exactly."""
    return Fraction(s) * 10 ** 8 / 1000


def package_rate(fees, vsizes):
    return Fraction(sum(fees), sum(vsizes))


def fee_share(fees_sat, subsidy_sat):
    return Fraction(sum(fees_sat), sum(fees_sat) + subsidy_sat * len(fees_sat))


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)])."""
    import sen0401_ch09_quotes_v1_0_0 as Q
    import sen0401_ch09_sources_v1_0_0 as S
    files = {r[0]: r[4] for r in S.S}
    bad, n = [], 0
    for sid, frags in Q.QUOTES.items():
        for f in frags:
            n += 1
            if not has(files[sid], re.sub(r"\s+", " ", f)):
                bad.append((sid, f[:70]))
    missing = [sid for sid in files if sid not in Q.QUOTES]
    return len(Q.QUOTES), n, bad, missing


def index_report():
    idx = json.load(open(os.path.join(EV, "sources_index_v1_0_0.json")))
    import sen0401_ch09_sources_v1_0_0 as S
    ok = [sid for sid, r in idx.items() if r.get("http") == 200 and r.get("sha256")]
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))
