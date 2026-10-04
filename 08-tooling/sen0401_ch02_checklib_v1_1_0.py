#!/usr/bin/env python3
"""Helper functions for the executed claims of sen0401_ch02_corpus_v1_2_0.py (v1.1.0: emphasis marks of the book source _ + * are ignored when a phrase is looked up; python standard library only; nothing is imported from a Bitcoin library).

Three kinds of helper:
  * source readers: has_book / has_core / has_saved say whether a phrase occurs (white space collapsed, the book's index markup ((( ... ))) removed)
    in a chapter of the book (/home/claude/src/bitcoinbook), in a file of Bitcoin Core at the pinned commit 05bc2f5 (read with git show from
    /home/claude/src/bitcoin), or in a source saved in 08-tooling/ch02-sources;
  * algorithms restated from what was read: Bech32 checksum (BIP 173, reference procedure in the BIP's text), the serialization of a
    transaction and its identifier (ch06 of the book; Bitcoin Core src/primitives/transaction.cpp hashes the serialization without witness data),
    block header hash, Merkle root (ch11), difficulty bits (ch12), the secp256k1 curve and ECDSA signature (SEC 2 parameters re-read from Bitcoin
    Core's src/secp256k1), and Nakamoto's attacker-success probability (section 11 of the whitepaper);
  * the fixed data of the chapter: Alice's real transaction as printed in ch06 and ch03 of the book.
"""
__version__ = "1.1.0"
import hashlib, os, re, struct, subprocess, math

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/home/claude/src/bitcoinbook"
CORE = "/home/claude/src/bitcoin"
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
SAVED = os.path.join(HERE, "ch02-sources")

def _norm(t):
    t = re.sub(r"\(\(\(.*?\)\)\)", "", t, flags=re.S)
    t = re.sub(r"[_*+]", "", t)           # asciidoc emphasis and literal marks are not part of the words
    return " ".join(t.split())

def book_text(name): return _norm(open(os.path.join(BOOK, name), encoding="utf-8").read())
def core_text(path):
    r = subprocess.run(["git", "-c", "gc.auto=0", "-C", CORE, "show", "%s:%s" % (COMMIT, path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    return _norm(r.stdout)
def saved_text(name): return _norm(open(os.path.join(SAVED, name), encoding="utf-8", errors="replace").read())
def has_book(name, *phrases): t = book_text(name); return all(_norm(p) in t for p in phrases)
def has_core(path, *phrases): t = core_text(path); return all(_norm(p) in t for p in phrases)
def has_saved(name, *phrases): t = saved_text(name); return all(_norm(p) in t for p in phrases)

# ---------------------------------------------------------------- hashing helpers
def sha256d(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()
def rev_hex(b): return b[::-1].hex()

# ---------------------------------------------------------------- Bech32 (BIP 173 reference procedure)
B32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def bech32_polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if (b >> i) & 1 else 0
    return chk
def bech32_hrp_expand(hrp): return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
def bech32_verify(addr):
    """polymod of expanded hrp + data; the BIP says the string is valid when it equals 1"""
    hrp, data = addr.rsplit("1", 1)
    return bech32_polymod(bech32_hrp_expand(hrp) + [B32.find(c) for c in data])
def bech32_program(addr):
    """version and witness program (bytes) of a Bech32 segwit address, 5-bit groups regrouped to 8-bit"""
    hrp, data = addr.rsplit("1", 1)
    d = [B32.find(c) for c in data][:-6]
    ver, rest = d[0], d[1:]
    acc = bits = 0; out = []
    for v in rest:
        acc = (acc << 5) | v; bits += 5
        while bits >= 8: bits -= 8; out.append((acc >> bits) & 255)
    return ver, bytes(out)

# ---------------------------------------------------------------- Alice's transaction (ch06 and ch03 of the book print the same hex)
ALICE_HEX = ("01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba"
             "4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe"
             "2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e81713010000"
             "0000")
def _varint(b, i):
    n = b[i]
    if n < 0xfd: return n, i + 1
    w = {0xfd: 2, 0xfe: 4, 0xff: 8}[n]
    return int.from_bytes(b[i + 1:i + 1 + w], "little"), i + 1 + w
def parse_tx(h):
    b = bytes.fromhex(h); i = 4; version = int.from_bytes(b[:4], "little")
    segwit = b[i] == 0 and b[i + 1] == 1
    if segwit: i += 2
    start = i
    n_in, i = _varint(b, i); ins = []
    for _ in range(n_in):
        txid = b[i:i + 32]; vout = int.from_bytes(b[i + 32:i + 36], "little"); i += 36
        ln, i = _varint(b, i); script = b[i:i + ln]; i += ln
        i += 4
        ins.append((rev_hex(txid), vout, script.hex()))
    n_out, i = _varint(b, i); outs = []
    for _ in range(n_out):
        val = int.from_bytes(b[i:i + 8], "little"); i += 8
        ln, i = _varint(b, i); outs.append((val, b[i:i + ln].hex())); i += ln
    end = i
    if segwit:
        for _ in range(n_in):
            k, i = _varint(b, i)
            for _ in range(k):
                ln, i = _varint(b, i); i += ln
    assert i + 4 == len(b)
    stripped = b[:4] + b[start:end] + b[-4:]
    return {"version": version, "inputs": ins, "outputs": outs, "total": len(b), "stripped": len(stripped), "stripped_bytes": stripped}
def txid_of(h): return rev_hex(sha256d(parse_tx(h)["stripped_bytes"]))
def weight_of(h):
    t = parse_tx(h); return t["stripped"] * 3 + t["total"]       # base size counted four times, witness bytes once
def vsize_of(h): return -(-weight_of(h) // 4)                    # rounded up

# ---------------------------------------------------------------- block header, hashes, Merkle tree, difficulty
def header_bytes(version, prev_hex, merkle_hex, time, bits, nonce):
    return struct.pack("<I", version) + bytes.fromhex(prev_hex)[::-1] + bytes.fromhex(merkle_hex)[::-1] + struct.pack("<III", time, bits, nonce)
def block_hash(version, prev_hex, merkle_hex, time, bits, nonce): return rev_hex(sha256d(header_bytes(version, prev_hex, merkle_hex, time, bits, nonce)))
def merkle_root(txids_hex):
    level = [bytes.fromhex(t)[::-1] for t in txids_hex]
    while len(level) > 1:
        if len(level) % 2: level.append(level[-1])
        level = [sha256d(level[i] + level[i + 1]) for i in range(0, len(level), 2)]
    return rev_hex(level[0])
def bits_to_target(bits):
    exp, coef = bits >> 24, bits & 0xffffff
    return coef * 2 ** (8 * (exp - 3))

# ---------------------------------------------------------------- secp256k1 and ECDSA (textbook, for illustration; not constant time)
P = 2 ** 256 - 2 ** 32 - 977
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
GX = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
GY = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
def _add(a, b):
    if a is None: return b
    if b is None: return a
    (x1, y1), (x2, y2) = a, b
    if x1 == x2 and (y1 + y2) % P == 0: return None
    m = (3 * x1 * x1 * pow(2 * y1, -1, P) if a == b else (y2 - y1) * pow(x2 - x1, -1, P)) % P
    x3 = (m * m - x1 - x2) % P
    return x3, (m * (x1 - x3) - y1) % P
def ec_mul(k, pt=(GX, GY)):
    r = None
    while k:
        if k & 1: r = _add(r, pt)
        pt = _add(pt, pt); k >>= 1
    return r
def on_curve(pt): return (pt[1] ** 2 - pt[0] ** 3 - 7) % P == 0
def ecdsa_sign(priv, msg, k):
    z = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    r = ec_mul(k)[0] % N
    s = pow(k, -1, N) * (z + r * priv) % N
    return r, s
def ecdsa_verify(pub, msg, sig):
    r, s = sig; z = int.from_bytes(hashlib.sha256(msg).digest(), "big")
    if not (0 < r < N and 0 < s < N): return False
    w = pow(s, -1, N)
    pt = _add(ec_mul(z * w % N), ec_mul(r * w % N, pub))
    return pt is not None and pt[0] % N == r

# ---------------------------------------------------------------- Nakamoto, section 11
def attacker_success(q, z):
    p = 1.0 - q; lam = z * (q / p); s = 1.0
    for k in range(z + 1):
        poisson = math.exp(-lam)
        for i in range(1, k + 1): poisson *= lam / i
        s -= poisson * (1 - (q / p) ** (z - k))
    return s
def min_confirmations(q, limit=0.001):
    z = 0
    while attacker_success(q, z) >= limit: z += 1
    return z


# ---------------------------------------------------------------- added in 1.1.0
def subsidy(height, interval=210000):
    """Bitcoin Core GetBlockSubsidy (src/validation.cpp): 50 * COIN shifted right once per halving interval, zero from 64 halvings on"""
    halvings = height // interval
    return 0 if halvings >= 64 else (50 * 100_000_000) >> halvings
def sha256(b): return hashlib.sha256(b).digest()
