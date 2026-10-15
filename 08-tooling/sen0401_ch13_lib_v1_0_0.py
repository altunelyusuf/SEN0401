#!/usr/bin/env python3
"""SEN0401 chapter 13 (Bitcoin Security): the library the chapter's executed claims call. Standard library only (plus sen0401_ch10_p2p_v1_0_0 for sha256d).
* text(), has(), const(): read a saved source (08-tooling/ch13-evidence) and test that a passage or a constant is in it (whitespace collapsed).
* run(): the recorded regtest run (sen0401_ch13_regtest_v1_0_0.py, Bitcoin Core 31.1 nodes on private chains); every value read from it is a SINGLE-RUN value.
* the arithmetic of the chapter as functions: base58check, the BIP 32 master key of a seed, the BIP 39 mnemonic, checksum and seed, the odds of losing and of being robbed with one key or with m of n,
  the sizes of timelocks.
* quotes_report(), index_report(): the passages used from every source, and the fetch record of every source."""
__version__ = "1.0.0"
import datetime, hashlib, html, json, math, os, re, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch10_p2p_v1_0_0 as P
EV = os.path.join(HERE, "ch13-evidence")
sha256d = P.sha256d
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


# ------------------------------------------------------------------------------------------------ keys and mnemonics
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58check(payload):
    d = payload + sha256d(payload)[:4]
    n = int.from_bytes(d, "big")
    s = ""
    while n:
        n, r = divmod(n, 58)
        s = B58[r] + s
    return "1" * (len(d) - len(d.lstrip(b"\0"))) + s


def bip32_master(seed):
    """BIP 32: HMAC-SHA512 with the key 'Bitcoin seed'; the left half is the private key, the right half the chain code; returns the serialized xprv."""
    import hmac
    i = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k, c = i[:32], i[32:]
    return b58check(bytes.fromhex("0488ade4") + b"\0" * 9 + c + b"\0" + k), k.hex(), c.hex()


def wordlist():
    return [w for w in open(os.path.join(EV, "bip39_english.txt")).read().split()]


def bip39_mnemonic(entropy):
    """BIP 39: the entropy plus ENT/32 bits of its SHA-256 are cut into groups of 11 bits, each an index into the list of 2048 words."""
    wl = wordlist()
    bits = bin(int.from_bytes(entropy, "big"))[2:].zfill(len(entropy) * 8)
    bits += bin(hashlib.sha256(entropy).digest()[0])[2:].zfill(8)[: len(entropy) * 8 // 32]
    return " ".join(wl[int(bits[k:k + 11], 2)] for k in range(0, len(bits), 11))


def bip39_valid(mnemonic):
    wl = wordlist()
    ix = {w: i for i, w in enumerate(wl)}
    ws = mnemonic.split()
    try:
        bits = "".join(bin(ix[w])[2:].zfill(11) for w in ws)
    except KeyError:
        return False
    ent = len(ws) * 11 * 32 // 33
    e = int(bits[:ent], 2).to_bytes(ent // 8, "big")
    return bin(hashlib.sha256(e).digest()[0])[2:].zfill(8)[: ent // 32] == bits[ent:]


def bip39_seed(mnemonic, passphrase=""):
    return hashlib.pbkdf2_hmac("sha512", mnemonic.encode(), ("mnemonic" + passphrase).encode(), 2048)


# ------------------------------------------------------------------------------------------------ odds
def p_lose(p_each, m, n):
    """The chance that fewer than m of n keys stay available when each is lost independently with probability p_each (funds stuck for an m-of-n scheme)."""
    from math import comb
    return sum(comb(n, k) * (1 - p_each) ** k * p_each ** (n - k) for k in range(m))


def p_theft(q_each, m, n):
    """The chance that at least m of n keys are stolen when each is stolen independently with probability q_each."""
    from math import comb
    return sum(comb(n, k) * q_each ** k * (1 - q_each) ** (n - k) for k in range(m, n + 1))


def iso(t):
    return datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


# ------------------------------------------------------------------------------------------------ sharing a secret (Shamir 1979)
SP = 2 ** 127 - 1          # a Mersenne prime: the field of the demonstration


def shamir_split(secret, k, n, coeffs, p=SP):
    """A (k, n) threshold scheme: the polynomial f(x) = secret + c1 x + ... + c(k-1) x^(k-1) mod p, the shares are the points (i, f(i)) for i = 1..n. coeffs are given, not drawn, so that the run repeats."""
    assert len(coeffs) == k - 1
    return [(i, (secret + sum(c * pow(i, j + 1, p) for j, c in enumerate(coeffs))) % p) for i in range(1, n + 1)]


def shamir_recover(shares, p=SP):
    """Lagrange interpolation at x = 0 from any k shares."""
    total = 0
    for i, (xi, yi) in enumerate(shares):
        num, den = 1, 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = num * (-xj) % p
                den = den * (xi - xj) % p
        total = (total + yi * num * pow(den, -1, p)) % p
    return total


def shamir_candidates(share, p=257):
    """For a (2, n) scheme over the small field p: the set of (secret, slope) pairs that are consistent with ONE share; every secret in the field has exactly one slope."""
    x, y = share
    return {(s, (y - s) * pow(x, -1, p) % p) for s in range(p)}


def count_sources_with(phrase):
    """In how many saved sources of the table does the phrase occur (whitespace collapsed)?"""
    import sen0401_ch13_sources_v1_0_0 as S
    n = 0
    for r in S.S:
        try:
            if re.sub(r"\s+", " ", phrase) in text(r[4]):
                n += 1
        except FileNotFoundError:
            pass
    return n


# ------------------------------------------------------------------------------------------------ the quotes of the sources
def quotes_report():
    """Every source's used passages re-read from the saved copy: returns (n_sources, n_fragments, failures[(id, fragment)], sources without a quote)."""
    import sen0401_ch13_quotes_v1_0_0 as Q
    import sen0401_ch13_sources_v1_0_0 as S
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
    import sen0401_ch13_sources_v1_0_0 as S
    ok = []
    for sid, r in idx.items():
        if r.get("http") == 200 and r.get("sha256"):
            b = open(os.path.join(EV, r["file"]), "rb").read()
            if hashlib.sha256(b).hexdigest() == r["sha256"]:
                ok.append(sid)
    return len(S.S), len(ok), sorted(set(r[0] for r in S.S) - set(ok))
