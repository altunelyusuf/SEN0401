#!/usr/bin/env python3
"""SEN0401 chapter 10 (The Bitcoin Network): the library the chapter's executed claims call. Standard library only (plus sen0401_ch10_p2p_v1_0_0, which is also standard library only).
* text(), has(), const(): read a saved source (08-tooling/ch10-evidence) and test that a passage or a constant is in it (whitespace collapsed).
* run(): the recorded regtest run (sen0401_ch10_regtest_v1_0_0.py, Bitcoin Core 31.1 nodes on private chains); every value read from it is a SINGLE-RUN value.
* bitnodes(): the census of reachable mainnet nodes of the Bitnodes snapshot of 2026-10-15 (software, services, network).
* the small rules of the chapter written as functions: the chance of a rival block while a block travels, the parity code of a toy forward error correction, the toy bloom filter,
  the worked example of the Golomb-coded set, the double-spend odds of the paper, the size of the header chain.
* quotes_report(), index_report(): the passages used from every source, and the fetch record of every source."""
__version__ = "1.0.0"
import hashlib, html, json, math, os, re, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
EV = os.path.join(HERE, "ch10-evidence")
_T = {}
_J = {}


def text(fname):
    """The saved source as one string, whitespace collapsed; html and pdf copies are read through their .txt conversion."""
    if fname not in _T:
        p = os.path.join(EV, fname)
        if fname.endswith(".html") or fname.endswith(".pdf"):
            p = os.path.splitext(p)[0] + ".txt"
        s = open(p, errors="replace").read()
        if fname.endswith(".html"):
            s = html.unescape(s)
        _T[fname] = re.sub(r"\s+", " ", s)
    return _T[fname]


def has(fname, *frags):
    t = text(fname)
    return all(re.sub(r"\s+", " ", f) in t for f in frags)


def count(fname, frag):
    return text(fname).count(frag)


def const(fname, name):
    """The value of a C++ constant or a markdown definition: `name = ...;` or `name{...}` in a saved source (first match), as written."""
    t = text(fname)
    m = re.search(re.escape(name) + r"\s*(?:\{|=)\s*([^;}\s,]+)", t)
    return m.group(1) if m else None


def jload(name):
    if name not in _J:
        _J[name] = json.load(open(os.path.join(EV, name)))
    return _J[name]


def run():
    return jload("regtest_run_v1_0_0.json")


# ------------------------------------------------------------------------------------------------ the census of mainnet nodes (Bitnodes snapshot)
SERVICE_BITS = {1: "NETWORK", 4: "BLOOM", 8: "WITNESS", 64: "COMPACT_FILTERS", 1024: "NETWORK_LIMITED", 2048: "P2P_V2"}


def net_of(addr):
    if ".onion" in addr:
        return "onion"
    if ".i2p" in addr:
        return "i2p"
    if addr.startswith("[fc"):
        return "cjdns"
    if addr.startswith("["):
        return "ipv6"
    return "ipv4"


def bitnodes():
    """Census of the snapshot: total, per network, per software family, per service bit, top versions."""
    d = jload("bitnodes_snapshot_latest.json")
    N = d["nodes"]
    nets, ua, svc, ver = {}, {}, {}, {}
    for a, v in N.items():
        nets[net_of(a)] = nets.get(net_of(a), 0) + 1
        ua[v[1]] = ua.get(v[1], 0) + 1
        ver[v[0]] = ver.get(v[0], 0) + 1
        for b, nm in SERVICE_BITS.items():
            if v[3] & b:
                svc[nm] = svc.get(nm, 0) + 1
    knots = sum(n for u, n in ua.items() if "Knots" in u)
    sat = sum(n for u, n in ua.items() if u.startswith("/Satoshi:"))
    top = sorted(ua.items(), key=lambda x: -x[1])[0]
    return {"total": len(N), "reported_total": d["total_nodes"], "height": d["latest_height"], "timestamp": d["timestamp"], "nets": nets, "satoshi_prefix": sat, "knots": knots, "core_plain": sat - knots,
            "services": svc, "top_agent": top, "protocol_versions": sorted(ver.items(), key=lambda x: -x[1])[:3]}


def chain_size_ratio():
    """The size of the whole block chain (Blockchain.com chart, megabytes, last point) against the header chain at the tip height of mempool.space (80 bytes each)."""
    j = jload("blockchaincom_blocks_size.json")
    last = j["values"][-1]
    h = int(open(os.path.join(EV, "mempool_tip_height.txt")).read().strip())
    headers_mb = 80 * (h + 1) / 1e6
    return {"chain_mb": round(last["y"]), "date": last["x"], "tip_height": h, "headers_mb": round(headers_mb, 1), "ratio": round(last["y"] / headers_mb)}


# ------------------------------------------------------------------------------------------------ small rules of the chapter
def rival_block_probability(delay_s, interval_s=600):
    """A block-finding race: the chance that some miner finds a rival block while the first block is still travelling (blocks arrive as a Poisson process)."""
    return 1 - math.exp(-delay_s / interval_s)


def parity_code(parts):
    """The simplest forward error correction: one extra part, the XOR of the others; any one lost part can be rebuilt from the rest."""
    n = len(parts[0])
    par = bytearray(n)
    for p in parts:
        for i in range(n):
            par[i] ^= p[i]
    return bytes(par)


def rebuild(parts_with_none, parity):
    lost = [i for i, p in enumerate(parts_with_none) if p is None]
    assert len(lost) == 1
    x = bytearray(parity)
    for p in parts_with_none:
        if p is not None:
            for i in range(len(x)):
                x[i] ^= p[i]
    out = list(parts_with_none)
    out[lost[0]] = bytes(x)
    return out


def double_spend_probability(q, z):
    """Nakamoto's calculation (section 11 of the paper): the chance that an attacker with share q of the hash rate ever catches up from z blocks behind."""
    p = 1.0 - q
    lam = z * (q / p)
    s = 1.0
    for k in range(0, z + 1):
        poisson = math.exp(-lam)
        for i in range(1, k + 1):
            poisson *= lam / i
        s -= poisson * (1 - (q / p) ** (z - k))
    return s


def toy_bloom_experiment(n_bits=16, m_funcs=3, patterns=("A", "B"), trials=20000, seed=7):
    """The book's picture in numbers: the filter of 16 bits and 3 hash functions with two patterns added; the false positive rate measured on random patterns against the formula."""
    f = P.ToyBloom(n_bits, m_funcs)
    for p in patterns:
        f.add(p)
    inserted_ok = all(f.test(p) for p in patterns)
    rnd = random.Random(seed)
    fp = sum(1 for _ in range(trials) if f.test("x%d" % rnd.getrandbits(40)))
    k, n = m_funcs, len(patterns)
    # a pattern that the filter says "maybe" for although it was never added, and one it says "definitely not" for
    maybe = next("x%d" % i for i in range(10 ** 6) if f.test("x%d" % i))
    nope = next("x%d" % i for i in range(10 ** 6) if not f.test("x%d" % i))
    return {"bits_set": sum(f.bits), "inserted_ok": inserted_ok, "fp_measured": round(fp / trials, 3), "fp_formula": round((1 - math.exp(-k * n / n_bits)) ** k, 3), "maybe_exists": bool(maybe), "nope_exists": bool(nope)}


def dice_table():
    """The book's table of the differences of two dice: how often each difference 0..5 occurs among the 36 throws."""
    cnt = {}
    for a in range(1, 7):
        for b in range(1, 7):
            d = abs(a - b)
            cnt[d] = cnt.get(d, 0) + 1
    return [cnt[k] for k in sorted(cnt)]


def gcs_book_example():
    """The book's example: the numbers 849 653 476 900 379 sent as the first number and the differences of the sorted list; the receiver adds them back."""
    nums = [849, 653, 476, 900, 379]
    s = sorted(nums)
    deltas = [s[0]] + [s[i] - s[i - 1] for i in range(1, len(s))]
    back, acc = [], 0
    for d in deltas:
        acc += d
        back.append(acc)
    return {"sorted": s, "deltas": deltas, "back": back, "equal": back == s, "max_bits_original": max(x.bit_length() for x in nums), "max_bits_deltas": max(x.bit_length() for x in deltas[1:])}


def rice_roundtrip(values, p):
    """Golomb-Rice coding of a sorted list of numbers with parameter p (the quotient in unary, the remainder in p bits): the coded bits, and the decoded list."""
    enc = P.golomb_encode(values, p)
    nbits = 0
    last = 0
    for v in values:
        d = v - last; last = v
        nbits += (d >> p) + 1 + p
    return {"bits": nbits, "bytes": len(enc), "decoded": P.golomb_decode(enc, len(values), p), "fixed_bits": len(values) * max(v.bit_length() for v in values)}


def bip158_vectors():
    """Every test vector of BIP 158 (ten testnet blocks): the filter and the filter header recomputed from the block and the scripts it spends."""
    v = jload("bip-0158_testnet-19.json")
    ok = 0
    names = []
    for row in v[1:]:
        h, bh, bx, scripts, prevh, filt, hdr = row[:7]
        blk = P.parse_block(bytes.fromhex(bx))
        f, n = P.basic_filter(bh, P.block_filter_elements(blk, [bytes.fromhex(s) for s in scripts]))
        if f.hex() == filt and P.filter_header(bytes.fromhex(filt), prevh) == hdr and blk["hash"] == bh:
            ok += 1
        names.append(h)
    return ok, len(v) - 1


def bloom_bip37_vector():
    """The filter of the Bitcoin Core unit test (3 elements, false positive rate 0.01, tweak 0, update all) serialised with the independent implementation."""
    b = P.Bloom(3, 0.01, 0, 1)
    for h in ("99108ad8ed9bb6274d3980bab5a85c048f0950c8", "b5a2c786d9ef4658287ced5914b37a1b4aa32eee", "b9300670b4c5366e95b2699e8b18bc75e5f729c5"):
        b.insert(bytes.fromhex(h))
    return b.payload().hex()


def getpeerinfo_new_and_gone():
    """The keys of Bitcoin Core 31.1's getpeerinfo against the keys of the listing printed in the book."""
    book = {"id", "addr", "addrbind", "addrlocal", "network", "services", "servicesnames", "lastsend", "lastrecv", "last_transaction", "last_block", "bytessent", "bytesrecv", "conntime", "timeoffset",
            "pingtime", "minping", "version", "subver", "inbound", "bip152_hb_to", "bip152_hb_from", "startingheight", "presynced_headers", "synced_headers", "synced_blocks", "inflight", "relaytxes",
            "minfeefilter", "addr_relay_enabled", "addr_processed", "addr_rate_limited", "permissions", "bytessent_per_msg", "bytesrecv_per_msg", "connection_type"}
    now = set(run()["e8_peerinfo_A"][0])
    return sorted(now - book), sorted(book - now)


def book_keys_in_text():
    t = text("book_ch10_network.adoc")
    return [k for k in ("addrlocal", "connection_type", "bip152_hb_to", "minfeefilter") if k in t]


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)], sources without a quote)."""
    import sen0401_ch10_quotes_v1_0_0 as Q
    import sen0401_ch10_sources_v1_0_0 as S
    files = {r[0]: r[4] for r in S.S}
    bad, n = [], 0
    for sid, frags in Q.QUOTES.items():
        for f in frags:
            n += 1
            if not has(files[sid], f):
                bad.append((sid, f[:70]))
    missing = [sid for sid in files if sid not in Q.QUOTES]
    return len(Q.QUOTES), n, bad, missing


def index_report():
    idx = json.load(open(os.path.join(EV, "sources_index_v1_0_0.json")))
    import sen0401_ch10_sources_v1_0_0 as S
    ok = []
    for sid, r in idx.items():
        if r.get("http") == 200 and r.get("sha256"):
            b = open(os.path.join(EV, r["file"]), "rb").read()
            if hashlib.sha256(b).hexdigest() == r["sha256"]:
                ok.append(sid)
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))
