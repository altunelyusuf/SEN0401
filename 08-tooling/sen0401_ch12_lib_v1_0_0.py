#!/usr/bin/env python3
"""SEN0401 chapter 12 (Mining and Consensus): the library the chapter's executed claims call. Standard library only (plus sen0401_ch10_p2p_v1_0_0 for sha256d and the compact size integer).
* text(), has(), const(): read a saved source (08-tooling/ch12-evidence) and test that a passage or a constant is in it (whitespace collapsed).
* run(): the recorded regtest run (sen0401_ch12_regtest_v1_0_0.py, Bitcoin Core 31.1 nodes on private chains); every value read from it is a SINGLE-RUN value.
* the rules of the chapter written as functions: the block subsidy and the total supply, the compact target, the difficulty retarget of pow.cpp, the proof-of-work search,
  the median time past, the coinbase transaction and a whole block built from bytes (so that a rule can be broken on purpose), the version bits, the odds of dice, shares and attacks.
* quotes_report(), index_report(): the passages used from every source, and the fetch record of every source."""
__version__ = "1.0.0"
import datetime, hashlib, html, json, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
EV = os.path.join(HERE, "ch12-evidence")
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


def raw(fname):
    return open(os.path.join(EV, fname)).read().strip()


# ------------------------------------------------------------------------------------------------ bytes, headers, targets
sha256d = P.sha256d


def rev(h):
    return bytes.fromhex(h)[::-1].hex()


def header(hex80):
    """The 80 bytes of a block header taken apart; hashes and the block hash in the usual (reversed) display order."""
    b = bytes.fromhex(hex80)
    assert len(b) == 80
    return {"version": int.from_bytes(b[0:4], "little"), "prev": b[4:36][::-1].hex(), "merkle": b[36:68][::-1].hex(), "time": int.from_bytes(b[68:72], "little"),
            "bits": b[72:76][::-1].hex(), "nonce": int.from_bytes(b[76:80], "little"), "hash": sha256d(b)[::-1].hex(), "bytes": len(b)}


def bits_to_target(bits_hex):
    """The compact encoding: one byte of exponent and three of mantissa; target = mantissa * 256 ** (exponent - 3)."""
    n = int(bits_hex, 16) if isinstance(bits_hex, str) else bits_hex
    return (n & 0x7fffff) * 256 ** ((n >> 24) - 3)


def target_to_bits(t):
    """The inverse of bits_to_target, as GetCompact() of arith_uint256.cpp: the three most significant bytes, with the sign bit kept clear."""
    size = (t.bit_length() + 7) // 8
    c = t >> (8 * (size - 3)) if size > 3 else t << (8 * (3 - size))
    if c & 0x00800000:
        c >>= 8
        size += 1
    return c | (size << 24)


DIFF1 = 0xffff * 256 ** (0x1d - 3)
POWLIMIT_MAIN = 0x00000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffff


def difficulty(bits_hex):
    return DIFF1 / bits_to_target(bits_hex)


def work(bits_hex):
    return 2 ** 256 // (bits_to_target(bits_hex) + 1)


def leading_zero_bits(h):
    return 256 - int(h, 16).bit_length()


def pow_ok(hash_display, bits_hex):
    return int(hash_display, 16) <= bits_to_target(bits_hex)


def retarget(first_time, last_time, last_bits_hex, spacing=600, interval=2016, powlimit=POWLIMIT_MAIN):
    """CalculateNextWorkRequired of pow.cpp: the timespan between the first and the LAST block of the period (2015 gaps), clamped to a quarter and four times the target timespan."""
    target_timespan = spacing * interval
    span = last_time - first_time
    span = max(target_timespan // 4, min(span, target_timespan * 4))
    new = bits_to_target(last_bits_hex) * span // target_timespan
    return target_to_bits(min(new, powlimit))


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def median_time_past(times):
    t = sorted(times[-11:])
    return t[len(t) // 2]


# ------------------------------------------------------------------------------------------------ money
def subsidy(height, interval=210000):
    """GetBlockSubsidy: 50 coins shifted right once per halving, zero from the 64th."""
    h = height // interval
    return 0 if h >= 64 else (50 * 10 ** 8) >> h


def total_supply(interval=210000):
    """The sum over all blocks, by whole intervals, as the book's script is meant to do (integer halving)."""
    r, tot = 50 * 10 ** 8, 0
    while r > 0:
        tot += interval * r
        r //= 2
    return tot


def book_script_as_printed():
    """The script of the book run as printed (current_reward /= 2 is a float division in Python 3): returns the result and its type."""
    r, tot = 50 * 10 ** 8, 0
    while r > 0:
        tot += 210000 * r
        r /= 2
    return tot


# ------------------------------------------------------------------------------------------------ a coinbase transaction and a whole block, from bytes
def push_num(n):
    """CScript() << n: OP_0, OP_1..OP_16, otherwise a push of the minimal little-endian number (a zero byte is added when the top bit would be taken for a sign)."""
    if n == 0:
        return b"\x00"
    if 1 <= n <= 16:
        return bytes([0x50 + n])
    b = bytearray()
    x = n
    while x:
        b.append(x & 0xff)
        x >>= 8
    if b[-1] & 0x80:
        b.append(0)
    return bytes([len(b)]) + bytes(b)


def p2pkh_script(h160_hex):
    return bytes.fromhex("76a914" + h160_hex + "88ac")


def coinbase_tx(height, value, pk_script, extra=b"", bip34=True, version=2, locktime=0, sequence=0xffffffff, commit_script=None, ss_override=None, extra_outputs=()):
    """A coinbase transaction. Returns (txid_display_hex, full_serialization_with_witness_if_any_hex, stripped_hex). The input script is the height push (unless bip34 is False) and the extra bytes;
    with commit_script the second output carries the witness commitment and the input carries the 32-byte reserved value."""
    ss = ss_override if ss_override is not None else (push_num(height) if bip34 else b"") + extra
    if ss_override is None and len(ss) < 2:
        ss += b"\x00" * (2 - len(ss))
    outs = [(value, pk_script)] + ([(0, commit_script)] if commit_script else []) + list(extra_outputs)
    body = b"\x01" + bytes(32) + b"\xff\xff\xff\xff" + P.cs_enc(len(ss)) + ss + struct.pack("<I", sequence)
    body += P.cs_enc(len(outs)) + b"".join(struct.pack("<q", v) + P.cs_enc(len(s)) + s for v, s in outs)
    stripped = struct.pack("<I", version) + body + struct.pack("<I", locktime)
    if commit_script:
        full = struct.pack("<I", version) + b"\x00\x01" + body + b"\x01\x20" + bytes(32) + struct.pack("<I", locktime)
    else:
        full = stripped
    return sha256d(stripped)[::-1].hex(), full.hex(), stripped.hex()


def merkle_root(ids):
    """The merkle root of a list of txids (display order): pairs hashed as double SHA-256 of the two 32-byte hashes in internal byte order; an odd last hash is paired with itself."""
    lvl = [bytes.fromhex(i)[::-1] for i in ids]
    while len(lvl) > 1:
        if len(lvl) % 2:
            lvl.append(lvl[-1])
        lvl = [sha256d(lvl[i] + lvl[i + 1]) for i in range(0, len(lvl), 2)]
    return lvl[0][::-1].hex()


def header_bytes(version, prev_display, merkle_display, t, bits_hex, nonce):
    return (struct.pack("<i", version) + bytes.fromhex(prev_display)[::-1] + bytes.fromhex(merkle_display)[::-1] + struct.pack("<I", t)
            + bytes.fromhex(bits_hex)[::-1] + struct.pack("<I", nonce))


def grind(version, prev, merkle, t, bits_hex, start=0):
    """The proof-of-work search itself: raises the nonce until the double SHA-256 of the header is at most the target. Returns (nonce, hash_display, attempts)."""
    tgt = bits_to_target(bits_hex)
    n = start
    while True:
        h = sha256d(header_bytes(version, prev, merkle, t, bits_hex, n))[::-1]
        if int.from_bytes(h, "big") <= tgt:
            return n, h.hex(), n - start + 1
        n += 1
        if n > 0xffffffff:
            raise ValueError("nonce space exhausted")


def build_block(prev, height, t, bits_hex, pk_script, value=None, version=0x20000000, extra=b"", bip34=True, txs=(), txids=(), commit_script=None, merkle_override=None,
                mine=True, nonce=0, ss_override=None, extra_outputs=()):
    """A complete block as hex: coinbase first, then the given transactions (hex, with witness) whose ids are given. Returns {'hex', 'hash', 'merkle', 'coinbase_txid', 'nonce', 'attempts'}.
    value defaults to the subsidy of the height (regtest halves every 150 blocks) plus nothing; pass another value to break the reward rule; merkle_override breaks the merkle rule."""
    if value is None:
        value = subsidy(height, 150)
    ctxid, cfull, _ = coinbase_tx(height, value, pk_script, extra, bip34, commit_script=commit_script, ss_override=ss_override, extra_outputs=extra_outputs)
    ids = [ctxid] + list(txids)
    mr = merkle_override or merkle_root(ids)
    attempts = 1
    if mine:
        nonce, h, attempts = grind(version, prev, mr, t, bits_hex)
    else:
        h = sha256d(header_bytes(version, prev, mr, t, bits_hex, nonce))[::-1].hex()
    blk = header_bytes(version, prev, mr, t, bits_hex, nonce) + P.cs_enc(1 + len(txs)) + bytes.fromhex(cfull) + b"".join(bytes.fromhex(x) for x in txs)
    return {"hex": blk.hex(), "hash": h, "merkle": mr, "coinbase_txid": ctxid, "nonce": nonce, "attempts": attempts}


# ------------------------------------------------------------------------------------------------ version bits
def signals(version, bit):
    """BIP 9: the top three bits are 001 and the bit is set."""
    return (version >> 29) == 1 and bool((version >> bit) & 1)


def version_rolled_bits(version, mask=0x1fffe000):
    return version & mask


# ------------------------------------------------------------------------------------------------ odds
def p_attacker_ever_wins(q, z):
    """Nakamoto's section 11: the chance that an attacker with the share q of the hash rate ever catches up from z blocks behind (Poisson sum of the paper)."""
    p = 1.0 - q
    lam = z * q / p
    s = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam) * lam ** k / math.factorial(k)
        s -= poisson * (1 - (q / p) ** (z - k))
    return s


def dice_odds(target, dice=2, sides=6):
    """The chance that a throw of the dice is at most the target (the book's dice game, where a throw must not exceed the target)."""
    from itertools import product
    tot = sides ** dice
    return sum(1 for t in product(range(1, sides + 1), repeat=dice) if sum(t) <= target), tot


def blocks_per_period(share, spacing=10):
    """Minutes per block and days per 2016 blocks of a chain that keeps the share of the hash rate and the old difficulty."""
    m = spacing / share
    return m, 2016 * m / 1440


# ------------------------------------------------------------------------------------------------ chain parameters
_CLS = {"main": "CMainParams", "test": "CTestNetParams", "testnet4": "CTestNet4Params", "signet": "SigNetParams", "regtest": "CRegTestParams"}


def chain_section(chain):
    t = text("core_src_kernel_chainparams.cpp")
    starts = sorted((t.find("class " + c + " "), k) for k, c in _CLS.items())
    for i, (pos, k) in enumerate(starts):
        if k == chain:
            return t[pos:starts[i + 1][0] if i + 1 < len(starts) else len(t)]


def chain_value(chain, pattern):
    m = re.search(pattern, chain_section(chain))
    return m.group(1) if m else None


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)], sources without a quote)."""
    import sen0401_ch12_quotes_v1_0_0 as Q
    import sen0401_ch12_sources_v1_0_0 as S
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
    import sen0401_ch12_sources_v1_0_0 as S
    ok = []
    for sid, r in idx.items():
        if r.get("http") == 200 and r.get("sha256"):
            b = open(os.path.join(EV, r["file"]), "rb").read()
            if hashlib.sha256(b).hexdigest() == r["sha256"]:
                ok.append(sid)
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))
