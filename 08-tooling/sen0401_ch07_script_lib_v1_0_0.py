#!/usr/bin/env python3
"""A Bitcoin Script interpreter and signature-checking library for chapter 7 (Authorization and Authentication) of
Mastering Bitcoin, 3rd edition, written in the Python standard library only (hashlib, hmac, struct) so that the same
functions run in the chapter builder, in the lecture deck's consoles and in the reader's browser (the page's Pyodide).

It follows Bitcoin Core's script interpreter (src/script/interpreter.cpp at commit 05bc2f5, saved in ch07-evidence) and
the proposals that define each rule, and it is checked against Bitcoin Core's own test data and against real mainnet
transactions by sen0401_ch07_verify_v1_0_0.py. What is here:
  * hashes: sha256, hash256, hash160 (RIPEMD-160 is written out when hashlib lacks it, as in the page's interpreter),
    BIP340 tagged hashes;
  * encodings: compactSize, Base58Check (BIP13 version bytes 0, 5), Bech32 and Bech32m (BIP173, BIP350), the
    scriptPubKey of an address and the address of a scriptPubKey;
  * secp256k1 in pure Python: public keys, ECDSA signing (RFC 6979) and verification with the lax DER parsing of
    consensus and the strict DER of BIP66, BIP340 Schnorr signing and verification, the BIP341 key tweak;
  * Script: opcodes, assembler and disassembler, script numbers, the stack machine (every opcode of Bitcoin Core,
    including OP_CHECKMULTISIG with its extra element, OP_CHECKLOCKTIMEVERIFY of BIP65, OP_CHECKSEQUENCEVERIFY of BIP112,
    the tapscript rules of BIP342), the verification flags Bitcoin Core names, and Core's error names;
  * signature hashes: the original algorithm (with the OP_CODESEPARATOR and FindAndDelete rules and the
    SIGHASH_SINGLE quirk), BIP143 for witness version 0, BIP341/BIP342 for taproot key path and script path;
  * VerifyScript: scriptSig then scriptPubKey on one stack, pay to script hash (BIP16), the witness programs of
    versions 0 and 1 (P2WPKH, P2WSH, taproot key path and script path with the control block's merkle proof);
  * helpers for worked examples: script templates, a classifier like Bitcoin Core's Solver, an execution trace.
Every function is pure; nothing here reads a file or the network. Speed is that of pure Python (about ten
milliseconds per signature check).
"""
__version__ = "1.0.0"
import hashlib, hmac, struct

# =====================================================================================================================
# hashes
# =====================================================================================================================
def sha256(b): return hashlib.sha256(b).digest()
def hash256(b): return sha256(sha256(b))
def sha1(b): return hashlib.sha1(b).digest()

_R1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8,
       3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12, 1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2,
       4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
_R2 = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2,
       15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13, 8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14,
       12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
_S1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8, 7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12,
       11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5, 11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12,
       9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
_S2 = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6, 9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11,
       9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5, 15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8,
       8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
_K1 = [0, 0x5a827999, 0x6ed9eba1, 0x8f1bbcdc, 0xa953fd4e]
_K2 = [0x50a28be6, 0x5c4dd124, 0x6d703ef3, 0x7a6d76e9, 0]


def ripemd160_pure(data):
    """RIPEMD-160 written out (Dobbertin, Bosselaers and Preneel, 1996)"""
    M = 0xffffffff
    rol = lambda x, n: ((x << n) | (x >> (32 - n))) & M
    def f(j, x, y, z):
        if j < 16: return x ^ y ^ z
        if j < 32: return (x & y) | (~x & M & z)
        if j < 48: return (x | (~y & M)) ^ z
        if j < 64: return (x & z) | (y & (~z & M))
        return x ^ (y | (~z & M))
    msg = bytearray(data) + b"\x80"
    msg += b"\x00" * ((56 - len(msg)) % 64) + struct.pack("<Q", len(data) * 8)
    h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    for off in range(0, len(msg), 64):
        X = struct.unpack("<16I", bytes(msg[off:off + 64]))
        a1, b1, c1, d1, e1 = h
        a2, b2, c2, d2, e2 = h
        for j in range(80):
            t = (rol((a1 + f(j, b1, c1, d1) + X[_R1[j]] + _K1[j // 16]) & M, _S1[j]) + e1) & M
            a1, e1, d1, c1, b1 = e1, d1, rol(c1, 10), b1, t
            t = (rol((a2 + f(79 - j, b2, c2, d2) + X[_R2[j]] + _K2[j // 16]) & M, _S2[j]) + e2) & M
            a2, e2, d2, c2, b2 = e2, d2, rol(c2, 10), b2, t
        t = (h[1] + c1 + d2) & M
        h = [t, (h[2] + d1 + e2) & M, (h[3] + e1 + a2) & M, (h[4] + a1 + b2) & M, (h[0] + b1 + c2) & M]
    return struct.pack("<5I", *h)


def ripemd160(b):
    try:
        return hashlib.new("ripemd160", b).digest()
    except (ValueError, TypeError):
        return ripemd160_pure(b)


def hash160(b): return ripemd160(sha256(b))
def tagged_hash(tag, data):
    th = sha256(tag.encode())
    return sha256(th + th + data)

# =====================================================================================================================
# compactSize, Base58Check, Bech32 / Bech32m
# =====================================================================================================================
def cs_encode(n):
    assert 0 <= n <= 0xffffffffffffffff
    if n < 253: return bytes([n])
    if n <= 0xffff: return b"\xfd" + struct.pack("<H", n)
    if n <= 0xffffffff: return b"\xfe" + struct.pack("<I", n)
    return b"\xff" + struct.pack("<Q", n)


def cs_decode(b, pos=0):
    f = b[pos]
    if f < 253: return f, 1
    if f == 0xfd: return struct.unpack_from("<H", b, pos + 1)[0], 3
    if f == 0xfe: return struct.unpack_from("<I", b, pos + 1)[0], 5
    return struct.unpack_from("<Q", b, pos + 1)[0], 9


_B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58check_encode(version, payload):
    raw = bytes([version]) + payload
    raw += hash256(raw)[:4]
    n = int.from_bytes(raw, "big"); s = ""
    while n: n, r = divmod(n, 58); s = _B58[r] + s
    return "1" * (len(raw) - len(raw.lstrip(b"\0"))) + s


def b58check_decode(s):
    n = 0
    for ch in s: n = n * 58 + _B58.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    raw = b"\0" * (len(s) - len(s.lstrip("1"))) + raw
    assert hash256(raw[:-4])[:4] == raw[-4:], "bad Base58Check checksum"
    return raw[0], raw[1:-4]


_BECH = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
def _polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]; chk = 1
    for v in values:
        b = chk >> 25; chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if (b >> i) & 1 else 0
    return chk
def _hrp_expand(hrp): return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]
def _convertbits(data, frm, to, pad=True):
    acc = bits = 0; ret = []; maxv = (1 << to) - 1
    for v in data:
        acc = (acc << frm) | v; bits += frm
        while bits >= to: bits -= to; ret.append((acc >> bits) & maxv)
    if pad and bits: ret.append((acc << (to - bits)) & maxv)
    elif not pad: assert bits < frm and not ((acc << (to - bits)) & maxv), "bad padding"
    return ret


def segwit_address(hrp, version, program):
    """BIP173 for witness version 0, BIP350 (Bech32m) for versions 1 to 16"""
    const = 1 if version == 0 else 0x2bc830a3
    data = [version] + _convertbits(program, 8, 5)
    pm = _polymod(_hrp_expand(hrp) + data + [0] * 6) ^ const
    return hrp + "1" + "".join(_BECH[d] for d in data + [(pm >> 5 * (5 - i)) & 31 for i in range(6)])


def segwit_decode(hrp, addr):
    pos = addr.rfind("1"); assert addr.lower() == addr or addr.upper() == addr
    addr = addr.lower(); assert addr[:pos] == hrp and 6 <= len(addr) - pos - 1
    data = [_BECH.index(c) for c in addr[pos + 1:]]
    const = _polymod(_hrp_expand(hrp) + data)
    version = data[0]
    assert const == (1 if version == 0 else 0x2bc830a3), "bad Bech32 checksum"
    prog = bytes(_convertbits(data[1:-6], 5, 8, False))
    assert 2 <= len(prog) <= 40 and version <= 16
    return version, prog

# =====================================================================================================================
# secp256k1 (pure Python; Jacobian coordinates)
# =====================================================================================================================
P = 2 ** 256 - 2 ** 32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)


def _jdouble(p):
    x, y, z = p
    if not y: return (0, 1, 0)
    s = 4 * x * y * y % P; m = 3 * x * x % P
    x3 = (m * m - 2 * s) % P
    return (x3, (m * (s - x3) - 8 * y ** 4) % P, 2 * y * z % P)


def _jadd(p, q):
    if not p[2]: return q
    if not q[2]: return p
    z1, z2 = p[2], q[2]
    u1 = p[0] * z2 * z2 % P; u2 = q[0] * z1 * z1 % P
    s1 = p[1] * z2 ** 3 % P; s2 = q[1] * z1 ** 3 % P
    if u1 == u2: return _jdouble(p) if s1 == s2 else (0, 1, 0)
    h = (u2 - u1) % P; r = (s2 - s1) % P
    h2 = h * h % P; h3 = h * h2 % P
    x3 = (r * r - h3 - 2 * u1 * h2) % P
    return (x3, (r * (u1 * h2 - x3) - s1 * h3) % P, h * z1 * z2 % P)


def _affine(p):
    if not p[2]: return None
    zi = pow(p[2], -1, P)
    return (p[0] * zi * zi % P, p[1] * zi ** 3 % P)


def point_mul(k, pt=G):
    k %= N
    r = (0, 1, 0); a = (pt[0], pt[1], 1)
    while k:
        if k & 1: r = _jadd(r, a)
        a = _jdouble(a); k >>= 1
    return _affine(r)


def point_add(a, b):
    if a is None: return b
    if b is None: return a
    return _affine(_jadd((a[0], a[1], 1), (b[0], b[1], 1)))


def lift_x(x):
    if not 0 <= x < P: return None
    y2 = (pow(x, 3, P) + 7) % P
    y = pow(y2, (P + 1) // 4, P)
    return None if y * y % P != y2 else (x, y if y % 2 == 0 else P - y)


def pubkey_serialize(pt, compressed=True):
    if compressed: return bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(32, "big")
    return b"\x04" + pt[0].to_bytes(32, "big") + pt[1].to_bytes(32, "big")


def pubkey_parse(b):
    """a public key as a point, or None: 33 bytes (02/03), 65 bytes (04, or the hybrid 06/07 that consensus still accepts)"""
    if len(b) == 33 and b[0] in (2, 3):
        pt = lift_x(int.from_bytes(b[1:], "big"))
        if pt is None: return None
        return pt if pt[1] & 1 == b[0] & 1 else (pt[0], P - pt[1])
    if len(b) == 65 and b[0] in (4, 6, 7):
        x, y = int.from_bytes(b[1:33], "big"), int.from_bytes(b[33:], "big")
        if x >= P or y >= P or (y * y - x ** 3 - 7) % P: return None
        if b[0] in (6, 7) and (y & 1) != (b[0] & 1): return None
        return (x, y)
    return None


def pubkey_create(secret, compressed=True):
    assert 1 <= secret < N, "a private key is a number from 1 to n - 1"
    return pubkey_serialize(point_mul(secret), compressed)

# ---- ECDSA ----
def _rfc6979(secret, msg32):
    x = secret.to_bytes(32, "big"); h1 = (int.from_bytes(msg32, "big") % N).to_bytes(32, "big")
    v = b"\x01" * 32; k = b"\x00" * 32
    k = hmac.new(k, v + b"\x00" + x + h1, hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()
    k = hmac.new(k, v + b"\x01" + x + h1, hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()
    while True:
        v = hmac.new(k, v, hashlib.sha256).digest()
        c = int.from_bytes(v, "big")
        if 1 <= c < N: return c
        k = hmac.new(k, v + b"\x00", hashlib.sha256).digest(); v = hmac.new(k, v, hashlib.sha256).digest()


def der_encode(r, s):
    def i(n):
        b = n.to_bytes((n.bit_length() + 7) // 8 or 1, "big")
        return b"\x02" + bytes([len(b) + (b[0] >> 7)]) + (b"\x00" if b[0] >> 7 else b"") + b
    body = i(r) + i(s)
    return b"\x30" + bytes([len(body)]) + body


def ecdsa_sign(secret, msg32, low_s=True):
    """a DER signature (without the sighash byte) of a 32-byte message, nonce by RFC 6979, S in the lower half (BIP62/BIP146)"""
    k = _rfc6979(secret, msg32)
    r = point_mul(k)[0] % N
    s = pow(k, -1, N) * (int.from_bytes(msg32, "big") + r * secret) % N
    if low_s and s > N // 2: s = N - s
    return der_encode(r, s)


def der_parse_lax(sig):
    """(r, s) the way consensus reads a signature before BIP66 (OpenSSL-like leniency), or None"""
    if len(sig) < 1 or sig[0] != 0x30: return None
    pos = 1
    def length():
        nonlocal pos
        if pos >= len(sig): return None
        lb = sig[pos]; pos += 1
        if lb & 0x80:
            lb -= 0x80
            if lb > len(sig) - pos: return None
            pos += lb
            return -1
        return lb
    if length() is None: return None
    vals = []
    for _ in range(2):
        if pos >= len(sig) or sig[pos] != 0x02: return None
        pos += 1
        if pos >= len(sig): return None
        lb = sig[pos]; pos += 1
        if lb & 0x80:
            lb -= 0x80
            if lb > len(sig) - pos: return None
            while lb > 0 and sig[pos] == 0: pos += 1; lb -= 1
            if lb >= 8: return None
            ln = 0
            while lb > 0: ln = (ln << 8) + sig[pos]; pos += 1; lb -= 1
        else:
            ln = lb
        if ln > len(sig) - pos: return None
        vals.append(sig[pos:pos + ln]); pos += ln
    r = int.from_bytes(vals[0].lstrip(b"\0"), "big") if len(vals[0].lstrip(b"\0")) <= 32 else 0
    s = int.from_bytes(vals[1].lstrip(b"\0"), "big") if len(vals[1].lstrip(b"\0")) <= 32 else 0
    return r, s


def ecdsa_verify(pubkey, msg32, der_sig):
    pt = pubkey_parse(pubkey)
    rs = der_parse_lax(der_sig)
    if pt is None or rs is None: return False
    r, s = rs
    if not (1 <= r < N and 1 <= s < N): return False
    if s > N // 2: s = N - s                                        # the verifier normalises, as libsecp256k1 does
    z = int.from_bytes(msg32, "big"); w = pow(s, -1, N)
    pt2 = point_add(point_mul(z * w % N), point_mul(r * w % N, pt))
    return pt2 is not None and pt2[0] % N == r

# ---- BIP340 Schnorr and the BIP341 tweak ----
def schnorr_pubkey(secret):
    return point_mul(secret)[0].to_bytes(32, "big")


def schnorr_sign(secret, msg32, aux=b"\x00" * 32):
    pt = point_mul(secret)
    d = secret if pt[1] % 2 == 0 else N - secret
    t = (d ^ int.from_bytes(tagged_hash("BIP0340/aux", aux), "big")).to_bytes(32, "big")
    rand = tagged_hash("BIP0340/nonce", t + pt[0].to_bytes(32, "big") + msg32)
    k0 = int.from_bytes(rand, "big") % N
    assert k0, "nonce is zero"
    R = point_mul(k0); k = k0 if R[1] % 2 == 0 else N - k0
    rb = R[0].to_bytes(32, "big")
    e = int.from_bytes(tagged_hash("BIP0340/challenge", rb + pt[0].to_bytes(32, "big") + msg32), "big") % N
    return rb + ((k + e * d) % N).to_bytes(32, "big")


def schnorr_verify(pub32, msg32, sig64):
    if len(pub32) != 32 or len(sig64) != 64: return False
    pt = lift_x(int.from_bytes(pub32, "big"))
    r, s = int.from_bytes(sig64[:32], "big"), int.from_bytes(sig64[32:], "big")
    if pt is None or r >= P or s >= N: return False
    e = int.from_bytes(tagged_hash("BIP0340/challenge", sig64[:32] + pub32 + msg32), "big") % N
    R = point_add(point_mul(s), point_mul(N - e, pt))
    return R is not None and R[1] % 2 == 0 and R[0] == r


def taproot_tweak_pubkey(internal32, merkle_root=b""):
    """(parity bit, 32-byte output key): Q = P + int(hashTapTweak(P || root)) * G, as BIP341 constructs it"""
    t = int.from_bytes(tagged_hash("TapTweak", internal32 + merkle_root), "big")
    assert t < N
    Q = point_add(lift_x(int.from_bytes(internal32, "big")), point_mul(t))
    return Q[1] & 1, Q[0].to_bytes(32, "big")


def taproot_tweak_seckey(secret, merkle_root=b""):
    pt = point_mul(secret)
    d = secret if pt[1] % 2 == 0 else N - secret
    t = int.from_bytes(tagged_hash("TapTweak", pt[0].to_bytes(32, "big") + merkle_root), "big")
    return (d + t) % N

# =====================================================================================================================
# opcodes, assembler, disassembler
# =====================================================================================================================
OP = {"OP_0": 0, "OP_PUSHDATA1": 76, "OP_PUSHDATA2": 77, "OP_PUSHDATA4": 78, "OP_1NEGATE": 79, "OP_RESERVED": 80}
for _i in range(1, 17): OP["OP_%d" % _i] = 80 + _i
OP.update({"OP_NOP": 97, "OP_VER": 98, "OP_IF": 99, "OP_NOTIF": 100, "OP_VERIF": 101, "OP_VERNOTIF": 102, "OP_ELSE": 103,
           "OP_ENDIF": 104, "OP_VERIFY": 105, "OP_RETURN": 106, "OP_TOALTSTACK": 107, "OP_FROMALTSTACK": 108,
           "OP_2DROP": 109, "OP_2DUP": 110, "OP_3DUP": 111, "OP_2OVER": 112, "OP_2ROT": 113, "OP_2SWAP": 114,
           "OP_IFDUP": 115, "OP_DEPTH": 116, "OP_DROP": 117, "OP_DUP": 118, "OP_NIP": 119, "OP_OVER": 120,
           "OP_PICK": 121, "OP_ROLL": 122, "OP_ROT": 123, "OP_SWAP": 124, "OP_TUCK": 125, "OP_CAT": 126,
           "OP_SUBSTR": 127, "OP_LEFT": 128, "OP_RIGHT": 129, "OP_SIZE": 130, "OP_INVERT": 131, "OP_AND": 132,
           "OP_OR": 133, "OP_XOR": 134, "OP_EQUAL": 135, "OP_EQUALVERIFY": 136, "OP_RESERVED1": 137, "OP_RESERVED2": 138,
           "OP_1ADD": 139, "OP_1SUB": 140, "OP_2MUL": 141, "OP_2DIV": 142, "OP_NEGATE": 143, "OP_ABS": 144,
           "OP_NOT": 145, "OP_0NOTEQUAL": 146, "OP_ADD": 147, "OP_SUB": 148, "OP_MUL": 149, "OP_DIV": 150,
           "OP_MOD": 151, "OP_LSHIFT": 152, "OP_RSHIFT": 153, "OP_BOOLAND": 154, "OP_BOOLOR": 155, "OP_NUMEQUAL": 156,
           "OP_NUMEQUALVERIFY": 157, "OP_NUMNOTEQUAL": 158, "OP_LESSTHAN": 159, "OP_GREATERTHAN": 160,
           "OP_LESSTHANOREQUAL": 161, "OP_GREATERTHANOREQUAL": 162, "OP_MIN": 163, "OP_MAX": 164, "OP_WITHIN": 165,
           "OP_RIPEMD160": 166, "OP_SHA1": 167, "OP_SHA256": 168, "OP_HASH160": 169, "OP_HASH256": 170,
           "OP_CODESEPARATOR": 171, "OP_CHECKSIG": 172, "OP_CHECKSIGVERIFY": 173, "OP_CHECKMULTISIG": 174,
           "OP_CHECKMULTISIGVERIFY": 175, "OP_NOP1": 176, "OP_CHECKLOCKTIMEVERIFY": 177, "OP_CHECKSEQUENCEVERIFY": 178,
           "OP_NOP4": 179, "OP_NOP5": 180, "OP_NOP6": 181, "OP_NOP7": 182, "OP_NOP8": 183, "OP_NOP9": 184,
           "OP_NOP10": 185, "OP_CHECKSIGADD": 186, "OP_INVALIDOPCODE": 255})
OP_NAME = {v: k for k, v in OP.items()}
ALIASES = {"OP_FALSE": 0, "OP_TRUE": 81, "OP_NOP2": 177, "OP_NOP3": 178, "OP_CLTV": 177, "OP_CSV": 178}
OP_IF, OP_ENDIF, OP_16, OP_RESERVED = 99, 104, 96, 80


def opname(code):
    if code in OP_NAME: return OP_NAME[code]
    return "OP_UNKNOWN%d" % code if code < 255 else "OP_INVALIDOPCODE"


class ScriptError(Exception):
    """the failure of a script, named as Bitcoin Core's script_error.h names it (EVAL_FALSE, BAD_OPCODE, ...)"""
    def __init__(self, name, detail=""):
        super().__init__(name + (": " + detail if detail else "")); self.name = name


def get_ops(script):
    """(position, opcode, data or None) for each operation; a push that runs past the end raises BAD_OPCODE"""
    return list(iter_ops(script))


def iter_ops(script):
    """the same, one operation at a time, so that a caller can stop before it meets a bad one (as the OP_SUCCESS scan of tapscript does)"""
    pc, n = 0, len(script)
    while pc < n:
        start = pc; op = script[pc]; pc += 1; data = None
        if op <= 78:
            if op < 76: ln = op
            else:
                w = {76: 1, 77: 2, 78: 4}[op]
                if pc + w > n: raise ScriptError("BAD_OPCODE", "push length cut off")
                ln = int.from_bytes(script[pc:pc + w], "little"); pc += w
            if pc + ln > n: raise ScriptError("BAD_OPCODE", "push runs past the end")
            data = script[pc:pc + ln]; pc += ln
        yield (start, op, data)


def push_data(d):
    n = len(d)
    if n < 76: return bytes([n]) + d
    if n <= 0xff: return b"\x4c" + bytes([n]) + d
    if n <= 0xffff: return b"\x4d" + struct.pack("<H", n) + d
    return b"\x4e" + struct.pack("<I", n) + d


def num_encode(n):
    if n == 0: return b""
    neg = n < 0; a = abs(n); out = bytearray()
    while a: out.append(a & 0xff); a >>= 8
    if out[-1] & 0x80: out.append(0x80 if neg else 0)
    elif neg: out[-1] |= 0x80
    return bytes(out)


def push_int(n):
    if n == 0: return b"\x00"
    if n == -1: return b"\x4f"
    if 1 <= n <= 16: return bytes([80 + n])
    return push_data(num_encode(n))


def num_decode(b, require_minimal=False, max_len=4):
    if len(b) > max_len: raise ScriptError("SCRIPTNUM", "number longer than %d bytes" % max_len)
    if require_minimal and b:
        if b[-1] & 0x7f == 0 and (len(b) <= 1 or b[-2] & 0x80 == 0): raise ScriptError("SCRIPTNUM", "non-minimal encoding")
    if not b: return 0
    v = int.from_bytes(b, "little")
    if b[-1] & 0x80: return -(v & ~(0x80 << (8 * (len(b) - 1))))
    return v


def cast_to_bool(b):
    for i, x in enumerate(b):
        if x:
            return not (i == len(b) - 1 and x == 0x80)
    return False


def assemble(text):
    """Bitcoin Core's test-script notation: OP_ names (with or without OP_), decimal numbers (pushed as the shortest
    number push), 0xHEX (inserted as raw bytes), 'text' (pushed), and the convenience <hex> (pushed)."""
    out = bytearray()
    for w in text.split():
        if w.lstrip("-").isdigit(): out += push_int(int(w))
        elif w.startswith("0x") and len(w) > 2: out += bytes.fromhex(w[2:])
        elif w.startswith("<") and w.endswith(">"): out += push_data(bytes.fromhex(w[1:-1]))
        elif len(w) >= 2 and w[0] == w[-1] == "'": out += push_data(w[1:-1].encode())
        else:
            name = w if w.startswith("OP_") else "OP_" + w
            if name in ALIASES: out.append(ALIASES[name])
            elif name in OP: out.append(OP[name])
            else: raise ValueError("unknown opcode %r" % w)
    return bytes(out)


def disassemble(script):
    parts = []
    try:
        for _, op, data in get_ops(script):
            if data is not None: parts.append("0" if op == 0 else data.hex())
            elif op == 0: parts.append("0")
            else: parts.append(opname(op))
    except ScriptError:
        parts.append("[error]")
    return " ".join(parts)

# =====================================================================================================================
# transactions (only what signature hashing needs)
# =====================================================================================================================
class Tx:
    def __init__(self, version=1, vin=None, vout=None, locktime=0, witness=None):
        self.version, self.locktime = version, locktime
        self.vin = vin or []          # [(prev_txid_internal_32, index, script_sig, sequence)]
        self.vout = vout or []        # [(value_in_satoshis, script_pubkey)]
        self.witness = witness or [[] for _ in self.vin]

    def serialize(self, witness=True):
        w = witness and any(self.witness)
        out = struct.pack("<i", self.version) + (b"\x00\x01" if w else b"")
        out += cs_encode(len(self.vin))
        for h, n, ss, seq in self.vin: out += h + struct.pack("<I", n) + cs_encode(len(ss)) + ss + struct.pack("<I", seq)
        out += cs_encode(len(self.vout))
        for v, spk in self.vout: out += struct.pack("<q", v) + cs_encode(len(spk)) + spk
        if w:
            for st in self.witness: out += cs_encode(len(st)) + b"".join(cs_encode(len(i)) + i for i in st)
        return out + struct.pack("<I", self.locktime)

    def txid(self): return hash256(self.serialize(False))[::-1].hex()
    def wtxid(self): return hash256(self.serialize(True))[::-1].hex()
    def weight(self): return len(self.serialize(False)) * 3 + len(self.serialize(True))


def parse_tx(h):
    b = bytes.fromhex(h) if isinstance(h, str) else bytes(h)
    ver = struct.unpack_from("<i", b, 0)[0]; p = 4; segwit = False
    if b[p] == 0 and b[p + 1] != 0: segwit = True; p += 2
    n, k = cs_decode(b, p); p += k; vin = []
    for _ in range(n):
        h32 = b[p:p + 32]; idx = struct.unpack_from("<I", b, p + 32)[0]; p += 36
        ln, k = cs_decode(b, p); p += k; ss = b[p:p + ln]; p += ln
        seq = struct.unpack_from("<I", b, p)[0]; p += 4; vin.append((h32, idx, ss, seq))
    n, k = cs_decode(b, p); p += k; vout = []
    for _ in range(n):
        v = struct.unpack_from("<q", b, p)[0]; p += 8
        ln, k = cs_decode(b, p); p += k; vout.append((v, b[p:p + ln])); p += ln
    wit = [[] for _ in vin]
    if segwit:
        for i in range(len(vin)):
            c, k = cs_decode(b, p); p += k; st = []
            for _ in range(c):
                ln, k = cs_decode(b, p); p += k; st.append(b[p:p + ln]); p += ln
            wit[i] = st
    lt = struct.unpack_from("<I", b, p)[0]; p += 4
    assert p == len(b), "trailing bytes after the lock time"
    return Tx(ver, vin, vout, lt, wit)

# =====================================================================================================================
# signature hashes
# =====================================================================================================================
SIGHASH_ALL, SIGHASH_NONE, SIGHASH_SINGLE, SIGHASH_ANYONECANPAY = 1, 2, 3, 0x80


def find_and_delete(script, pattern):
    """remove each aligned occurrence of pattern (a serialized push) from script, as Bitcoin Core's FindAndDelete does"""
    if not pattern: return script, 0
    res = bytearray(); found = 0; pc = 0; pc2 = 0; n = len(script)
    while True:
        res += script[pc2:pc]
        while n - pc >= len(pattern) and script[pc:pc + len(pattern)] == pattern: pc += len(pattern); found += 1
        pc2 = pc
        if pc >= n: break
        try: _, nxt = _next_op(script, pc)
        except ScriptError: break
        pc = nxt
    if found: res += script[pc2:]; return bytes(res), found
    return script, 0


def _next_op(script, pc):
    op = script[pc]; pc += 1
    if op <= 78:
        if op < 76: ln = op
        else:
            w = {76: 1, 77: 2, 78: 4}[op]
            if pc + w > len(script): raise ScriptError("BAD_OPCODE")
            ln = int.from_bytes(script[pc:pc + w], "little"); pc += w
        if pc + ln > len(script): raise ScriptError("BAD_OPCODE")
        pc += ln
    return op, pc


def _strip_codeseparators(script):
    out = bytearray(); pc = 0
    while pc < len(script):
        op, nxt = _next_op(script, pc)
        if op != 171: out += script[pc:nxt]
        pc = nxt
    return bytes(out)


def sighash_legacy(script_code, tx, nin, hashtype):
    """the original signature hash: the transaction with every other input's script blanked, this input's script replaced
    by the script code (code separators removed), and the hash type appended as four bytes"""
    if hashtype & 0x1f == SIGHASH_SINGLE and nin >= len(tx.vout):
        return b"\x01" + b"\x00" * 31                            # the quirk: a signature over the number one
    anyone = hashtype & SIGHASH_ANYONECANPAY; single = hashtype & 0x1f == SIGHASH_SINGLE; none = hashtype & 0x1f == SIGHASH_NONE
    sc = _strip_codeseparators(script_code)
    out = struct.pack("<i", tx.version)
    ins = [nin] if anyone else range(len(tx.vin))
    out += cs_encode(len(ins))
    for i in ins:
        h, n, _, seq = tx.vin[i]
        out += h + struct.pack("<I", n) + (cs_encode(len(sc)) + sc if i == nin else b"\x00")
        out += struct.pack("<I", 0 if i != nin and (single or none) else seq)
    nout = 0 if none else (nin + 1 if single else len(tx.vout))
    out += cs_encode(nout)
    for o in range(nout):
        if single and o != nin: out += struct.pack("<q", -1) + b"\x00"
        else: out += struct.pack("<q", tx.vout[o][0]) + cs_encode(len(tx.vout[o][1])) + tx.vout[o][1]
    out += struct.pack("<I", tx.locktime) + struct.pack("<I", hashtype)
    return hash256(out)


def sighash_v0(script_code, tx, nin, hashtype, amount):
    """BIP143: commit to the amount, hash the prevouts, sequences and outputs once, never hash a script per input"""
    base = hashtype & 0x1f; anyone = hashtype & SIGHASH_ANYONECANPAY
    hp = hs = ho = b"\x00" * 32
    if not anyone: hp = hash256(b"".join(h + struct.pack("<I", n) for h, n, _, _ in tx.vin))
    if not anyone and base not in (SIGHASH_SINGLE, SIGHASH_NONE): hs = hash256(b"".join(struct.pack("<I", s) for *_, s in tx.vin))
    if base not in (SIGHASH_SINGLE, SIGHASH_NONE):
        ho = hash256(b"".join(struct.pack("<q", v) + cs_encode(len(s)) + s for v, s in tx.vout))
    elif base == SIGHASH_SINGLE and nin < len(tx.vout):
        v, s = tx.vout[nin]; ho = hash256(struct.pack("<q", v) + cs_encode(len(s)) + s)
    h, n, _, seq = tx.vin[nin]
    pre = (struct.pack("<i", tx.version) + hp + hs + h + struct.pack("<I", n) + cs_encode(len(script_code)) + script_code +
           struct.pack("<q", amount) + struct.pack("<I", seq) + ho + struct.pack("<I", tx.locktime) + struct.pack("<I", hashtype))
    return hash256(pre)


def sighash_taproot(tx, nin, hashtype, spent, ext_flag=0, annex=None, tapleaf_hash=None, codesep_pos=0xffffffff, key_version=0):
    """BIP341 SigMsg and the tagged hash TapSighash; spent is the list of (amount, scriptPubKey) the inputs spend.
    Returns None for a hash type BIP341 does not define."""
    if hashtype not in (0, 1, 2, 3, 0x81, 0x82, 0x83): return None
    base = hashtype & 3 if hashtype else 1; anyone = hashtype & 0x80
    if hashtype & 3 == SIGHASH_SINGLE and nin >= len(tx.vout): return None
    m = bytes([hashtype]) + struct.pack("<i", tx.version) + struct.pack("<I", tx.locktime)
    if not anyone:
        m += sha256(b"".join(h + struct.pack("<I", n) for h, n, _, _ in tx.vin))
        m += sha256(b"".join(struct.pack("<q", a) for a, _ in spent))
        m += sha256(b"".join(cs_encode(len(s)) + s for _, s in spent))
        m += sha256(b"".join(struct.pack("<I", s) for *_, s in tx.vin))
    if hashtype & 3 not in (SIGHASH_NONE, SIGHASH_SINGLE):
        m += sha256(b"".join(struct.pack("<q", v) + cs_encode(len(s)) + s for v, s in tx.vout))
    m += bytes([ext_flag * 2 + (1 if annex is not None else 0)])
    if anyone:
        h, n, _, seq = tx.vin[nin]; a, spk = spent[nin]
        m += h + struct.pack("<I", n) + struct.pack("<q", a) + cs_encode(len(spk)) + spk + struct.pack("<I", seq)
    else:
        m += struct.pack("<I", nin)
    if annex is not None: m += sha256(cs_encode(len(annex)) + annex)
    if hashtype & 3 == SIGHASH_SINGLE:
        v, s = tx.vout[nin]; m += sha256(struct.pack("<q", v) + cs_encode(len(s)) + s)
    if ext_flag == 1: m += tapleaf_hash + bytes([key_version]) + struct.pack("<I", codesep_pos)
    return tagged_hash("TapSighash", b"\x00" + m)

# =====================================================================================================================
# the interpreter
# =====================================================================================================================
MAX_SCRIPT_SIZE, MAX_ELEMENT, MAX_OPS, MAX_STACK, MAX_PUBKEYS = 10000, 520, 201, 1000, 20
LOCKTIME_THRESHOLD = 500000000
SEQ_FINAL, SEQ_DISABLE, SEQ_TYPE, SEQ_MASK = 0xffffffff, 1 << 31, 1 << 22, 0xffff
VALIDATION_WEIGHT_OFFSET, VALIDATION_WEIGHT_PER_SIGOP = 50, 50
ALL_FLAGS = frozenset("P2SH STRICTENC DERSIG LOW_S NULLDUMMY SIGPUSHONLY MINIMALDATA DISCOURAGE_UPGRADABLE_NOPS CLEANSTACK "
                      "CHECKLOCKTIMEVERIFY CHECKSEQUENCEVERIFY WITNESS DISCOURAGE_UPGRADABLE_WITNESS_PROGRAM MINIMALIF "
                      "NULLFAIL WITNESS_PUBKEYTYPE TAPROOT DISCOURAGE_OP_SUCCESS DISCOURAGE_UPGRADABLE_PUBKEYTYPE DISCOURAGE_UPGRADABLE_TAPROOT_VERSION".split())
MAINNET_FLAGS = frozenset("P2SH DERSIG NULLDUMMY CHECKLOCKTIMEVERIFY CHECKSEQUENCEVERIFY WITNESS TAPROOT".split())   # consensus today
STANDARD_FLAGS = ALL_FLAGS                                                                                         # relay policy: all of them


def is_valid_der(sig):
    """BIP66's strict DER check on a signature with its hash type byte"""
    n = len(sig)
    if n < 9 or n > 73 or sig[0] != 0x30 or sig[1] != n - 3: return False
    lr = sig[3]
    if 5 + lr >= n: return False
    ls = sig[5 + lr]
    if lr + ls + 7 != n or sig[2] != 2 or lr == 0 or sig[4] & 0x80: return False
    if lr > 1 and sig[4] == 0 and not sig[5] & 0x80: return False
    if sig[lr + 4] != 2 or ls == 0 or sig[lr + 6] & 0x80: return False
    if ls > 1 and sig[lr + 6] == 0 and not sig[lr + 7] & 0x80: return False
    return True


def is_low_s(sig):
    rs = der_parse_lax(sig[:-1])
    return rs is not None and rs[1] <= N // 2


class Checker:
    """what the script engine needs from the spending transaction: signature checks, lock time and sequence"""
    def __init__(self, tx, nin, amount=0, spent=None):
        self.tx, self.nin, self.amount, self.spent = tx, nin, amount, spent

    def ecdsa(self, sig, pubkey, script_code, sigversion):
        if not sig or pubkey_parse(pubkey) is None: return False
        ht = sig[-1]
        h = sighash_v0(script_code, self.tx, self.nin, ht, self.amount) if sigversion == "WITNESS_V0" else sighash_legacy(script_code, self.tx, self.nin, ht)
        return ecdsa_verify(pubkey, h, sig[:-1])

    def schnorr(self, sig, pub32, sigversion, ex):
        if len(sig) not in (64, 65): raise ScriptError("SCHNORR_SIG_SIZE")
        ht = 0
        if len(sig) == 65:
            ht = sig[64]; sig = sig[:64]
            if ht == 0: raise ScriptError("SCHNORR_SIG_HASHTYPE")
        h = sighash_taproot(self.tx, self.nin, ht, self.spent, 1 if sigversion == "TAPSCRIPT" else 0, ex.get("annex"),
                            ex.get("tapleaf"), ex.get("codesep", 0xffffffff))
        if h is None: raise ScriptError("SCHNORR_SIG_HASHTYPE")
        if not schnorr_verify(pub32, h, sig): raise ScriptError("SCHNORR_SIG")
        return True

    def locktime(self, n):
        lt = self.tx.locktime
        if not ((lt < LOCKTIME_THRESHOLD and n < LOCKTIME_THRESHOLD) or (lt >= LOCKTIME_THRESHOLD and n >= LOCKTIME_THRESHOLD)): return False
        if n > lt: return False
        return self.tx.vin[self.nin][3] != SEQ_FINAL

    def sequence(self, n):
        seq = self.tx.vin[self.nin][3]
        if self.tx.version < 2 or seq & SEQ_DISABLE: return False
        mask = SEQ_TYPE | SEQ_MASK; a, b = seq & mask, n & mask
        if not ((a < SEQ_TYPE and b < SEQ_TYPE) or (a >= SEQ_TYPE and b >= SEQ_TYPE)): return False
        return b <= a


def _check_sig_encoding(sig, flags):
    if not sig: return
    if flags & {"DERSIG", "LOW_S", "STRICTENC"} and not is_valid_der(sig): raise ScriptError("SIG_DER")
    if "LOW_S" in flags and not is_low_s(sig): raise ScriptError("SIG_HIGH_S")
    if "STRICTENC" in flags and not (1 <= (sig[-1] & ~SIGHASH_ANYONECANPAY) <= 3): raise ScriptError("SIG_HASHTYPE")


def _check_pubkey_encoding(pk, flags, sigversion):
    if "STRICTENC" in flags:
        ok = (len(pk) == 33 and pk[0] in (2, 3)) or (len(pk) == 65 and pk[0] == 4)
        if not ok: raise ScriptError("PUBKEYTYPE")
    if "WITNESS_PUBKEYTYPE" in flags and sigversion == "WITNESS_V0" and not (len(pk) == 33 and pk[0] in (2, 3)):
        raise ScriptError("WITNESS_PUBKEYTYPE")


def _check_minimal_push(data, op):
    if not data: return op == 0
    if len(data) == 1 and 1 <= data[0] <= 16: return False
    if len(data) == 1 and data[0] == 0x81: return False
    if len(data) <= 75: return op == len(data)
    if len(data) <= 255: return op == 76
    if len(data) <= 65535: return op == 77
    return True


def is_op_success(op):
    return op == 80 or op == 98 or 126 <= op <= 129 or 131 <= op <= 134 or 137 <= op <= 138 or 141 <= op <= 142 or 149 <= op <= 153 or 187 <= op <= 254


DISABLED = {126, 127, 128, 129, 131, 132, 133, 134, 141, 142, 149, 150, 151, 152, 153}


def eval_script(stack, script, flags, checker, sigversion="BASE", ex=None, trace=None):
    """Run script on stack (a list of bytes, changed in place). Raises ScriptError; returns None on success.
    trace, if a list, receives (position, opcode name, copy of the stack after the operation)."""
    ex = ex if ex is not None else {}
    alt, vfexec = [], []
    if sigversion in ("BASE", "WITNESS_V0") and len(script) > MAX_SCRIPT_SIZE: raise ScriptError("SCRIPT_SIZE")
    ops = get_ops(script)
    nops = 0; minimal = "MINIMALDATA" in flags; begin = 0; ex["codesep"] = 0xffffffff
    def pop(): return stack.pop()
    def need(k):
        if len(stack) < k: raise ScriptError("INVALID_STACK_OPERATION")
    for opos, (pos, op, data) in enumerate(ops):
        fexec = all(vfexec)
        if data is not None and len(data) > MAX_ELEMENT: raise ScriptError("PUSH_SIZE")
        if sigversion in ("BASE", "WITNESS_V0") and op > OP_16:
            nops += 1
            if nops > MAX_OPS: raise ScriptError("OP_COUNT")
        if op in DISABLED: raise ScriptError("DISABLED_OPCODE")
        nxt = ops[opos + 1][0] if opos + 1 < len(ops) else len(script)
        if fexec and data is not None:
            if minimal and not _check_minimal_push(data, op): raise ScriptError("MINIMALDATA")
            stack.append(data)
        elif fexec or OP_IF <= op <= OP_ENDIF:
            if op == 79 or 81 <= op <= 96: stack.append(num_encode(op - 80))
            elif op == 97: pass
            elif op == 177:                                                     # OP_CHECKLOCKTIMEVERIFY (NOP2 before BIP65)
                if "CHECKLOCKTIMEVERIFY" in flags:
                    need(1); n = num_decode(stack[-1], minimal, 5)
                    if n < 0: raise ScriptError("NEGATIVE_LOCKTIME")
                    if not checker.locktime(n): raise ScriptError("UNSATISFIED_LOCKTIME")
            elif op == 178:                                                     # OP_CHECKSEQUENCEVERIFY (NOP3 before BIP112)
                if "CHECKSEQUENCEVERIFY" in flags:
                    need(1); n = num_decode(stack[-1], minimal, 5)
                    if n < 0: raise ScriptError("NEGATIVE_LOCKTIME")
                    if not n & SEQ_DISABLE and not checker.sequence(n): raise ScriptError("UNSATISFIED_LOCKTIME")
            elif op in (176, 179, 180, 181, 182, 183, 184, 185):
                if "DISCOURAGE_UPGRADABLE_NOPS" in flags: raise ScriptError("DISCOURAGE_UPGRADABLE_NOPS")
            elif op in (99, 100):
                val = False
                if fexec:
                    need(1); v = stack[-1]
                    if sigversion == "TAPSCRIPT" and (len(v) > 1 or (len(v) == 1 and v[0] != 1)): raise ScriptError("TAPSCRIPT_MINIMALIF")
                    if sigversion == "WITNESS_V0" and "MINIMALIF" in flags and (len(v) > 1 or (len(v) == 1 and v[0] != 1)): raise ScriptError("MINIMALIF")
                    val = cast_to_bool(v)
                    if op == 100: val = not val
                    pop()
                vfexec.append(val)
            elif op == 103:
                if not vfexec: raise ScriptError("UNBALANCED_CONDITIONAL")
                vfexec[-1] = not vfexec[-1]
            elif op == 104:
                if not vfexec: raise ScriptError("UNBALANCED_CONDITIONAL")
                vfexec.pop()
            elif op == 105:
                need(1)
                if cast_to_bool(stack[-1]): pop()
                else: raise ScriptError("VERIFY")
            elif op == 106: raise ScriptError("OP_RETURN")
            elif op == 107: need(1); alt.append(pop())
            elif op == 108:
                if not alt: raise ScriptError("INVALID_ALTSTACK_OPERATION")
                stack.append(alt.pop())
            elif op == 109: need(2); pop(); pop()
            elif op == 110: need(2); stack += stack[-2:]
            elif op == 111: need(3); stack += stack[-3:]
            elif op == 112: need(4); stack += stack[-4:-2]
            elif op == 113: need(6); x = stack[-6:-4]; del stack[-6:-4]; stack += x
            elif op == 114: need(4); stack[-4:] = stack[-2:] + stack[-4:-2]
            elif op == 115:
                need(1)
                if cast_to_bool(stack[-1]): stack.append(stack[-1])
            elif op == 116: stack.append(num_encode(len(stack)))
            elif op == 117: need(1); pop()
            elif op == 118: need(1); stack.append(stack[-1])
            elif op == 119: need(2); del stack[-2]
            elif op == 120: need(2); stack.append(stack[-2])
            elif op in (121, 122):
                need(2); n = num_decode(pop(), minimal)
                if n < 0 or n >= len(stack): raise ScriptError("INVALID_STACK_OPERATION")
                v = stack[-n - 1]
                if op == 122: del stack[-n - 1]
                stack.append(v)
            elif op == 123: need(3); stack[-3:] = [stack[-2], stack[-1], stack[-3]]
            elif op == 124: need(2); stack[-2:] = [stack[-1], stack[-2]]
            elif op == 125: need(2); stack.insert(len(stack) - 2, stack[-1])
            elif op == 130: need(1); stack.append(num_encode(len(stack[-1])))
            elif op in (135, 136):
                need(2); eq = stack[-1] == stack[-2]; pop(); pop(); stack.append(b"\x01" if eq else b"")
                if op == 136:
                    if eq: pop()
                    else: raise ScriptError("EQUALVERIFY")
            elif op in (139, 140, 143, 144, 145, 146):
                need(1); n = num_decode(pop(), minimal)
                n = {139: n + 1, 140: n - 1, 143: -n, 144: abs(n), 145: int(n == 0), 146: int(n != 0)}[op]
                stack.append(num_encode(n))
            elif op in (147, 148, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164):
                need(2); b = num_decode(stack[-1], minimal); a = num_decode(stack[-2], minimal); pop(); pop()
                r = {147: a + b, 148: a - b, 154: int(a != 0 and b != 0), 155: int(a != 0 or b != 0), 156: int(a == b), 157: int(a == b),
                     158: int(a != b), 159: int(a < b), 160: int(a > b), 161: int(a <= b), 162: int(a >= b), 163: min(a, b), 164: max(a, b)}[op]
                stack.append(num_encode(r))
                if op == 157:
                    if cast_to_bool(stack[-1]): pop()
                    else: raise ScriptError("NUMEQUALVERIFY")
            elif op == 165:
                need(3); c = num_decode(stack[-1], minimal); b = num_decode(stack[-2], minimal); a = num_decode(stack[-3], minimal)
                pop(); pop(); pop(); stack.append(b"\x01" if b <= a < c else b"")
            elif op in (166, 167, 168, 169, 170):
                need(1); v = pop()
                stack.append({166: ripemd160, 167: sha1, 168: sha256, 169: hash160, 170: hash256}[op](v))
            elif op == 171:
                begin = nxt; ex["codesep"] = opos
            elif op in (172, 173):
                need(2); sig, pk = stack[-2], stack[-1]
                if sigversion == "TAPSCRIPT":
                    ok = _tap_checksig(sig, pk, ex, flags, checker, sigversion)
                else:
                    code = script[begin:]
                    if sigversion == "BASE": code, _ = find_and_delete(code, push_data(sig))
                    _check_sig_encoding(sig, flags); _check_pubkey_encoding(pk, flags, sigversion)
                    ok = checker.ecdsa(sig, pk, code, sigversion)
                    if not ok and "NULLFAIL" in flags and sig: raise ScriptError("SIG_NULLFAIL")
                pop(); pop(); stack.append(b"\x01" if ok else b"")
                if op == 173:
                    if ok: pop()
                    else: raise ScriptError("CHECKSIGVERIFY")
            elif op == 186:
                if sigversion != "TAPSCRIPT": raise ScriptError("BAD_OPCODE")
                need(3); sig, num, pk = stack[-3], num_decode(stack[-2], minimal), stack[-1]
                ok = _tap_checksig(sig, pk, ex, flags, checker, sigversion)
                pop(); pop(); pop(); stack.append(num_encode(num + (1 if ok else 0)))
            elif op in (174, 175):
                if sigversion == "TAPSCRIPT": raise ScriptError("TAPSCRIPT_CHECKMULTISIG")
                i = 1; need(i)
                nk = num_decode(stack[-i], minimal)
                if nk < 0 or nk > MAX_PUBKEYS: raise ScriptError("PUBKEY_COUNT")
                nops += nk
                if nops > MAX_OPS: raise ScriptError("OP_COUNT")
                ikey = i = i + 1; ikey2 = nk + 2; i += nk; need(i)
                ns = num_decode(stack[-i], minimal)
                if ns < 0 or ns > nk: raise ScriptError("SIG_COUNT")
                isig = i = i + 1; i += ns; need(i)
                code = script[begin:]
                if sigversion == "BASE":
                    for k in range(ns): code, _ = find_and_delete(code, push_data(stack[-isig - k]))
                ok = True
                while ok and ns > 0:
                    sig, pk = stack[-isig], stack[-ikey]
                    _check_sig_encoding(sig, flags); _check_pubkey_encoding(pk, flags, sigversion)
                    if checker.ecdsa(sig, pk, code, sigversion): isig += 1; ns -= 1
                    ikey += 1; nk -= 1
                    if ns > nk: ok = False
                while i > 1:
                    i -= 1
                    if not ok and "NULLFAIL" in flags and not ikey2 and stack[-1]: raise ScriptError("SIG_NULLFAIL")
                    if ikey2 > 0: ikey2 -= 1
                    pop()
                need(1)
                if "NULLDUMMY" in flags and stack[-1]: raise ScriptError("SIG_NULLDUMMY")
                pop(); stack.append(b"\x01" if ok else b"")
                if op == 175:
                    if ok: pop()
                    else: raise ScriptError("CHECKMULTISIGVERIFY")
            else:
                raise ScriptError("BAD_OPCODE", opname(op))
        if len(stack) + len(alt) > MAX_STACK: raise ScriptError("STACK_SIZE")
        if trace is not None: trace.append((pos, opname(op) if data is None else ("PUSH %d" % len(data)), [s for s in stack]))
    if vfexec: raise ScriptError("UNBALANCED_CONDITIONAL")


def _tap_checksig(sig, pk, ex, flags, checker, sigversion):
    ok = bool(sig)
    if ok:
        ex["weight_left"] -= VALIDATION_WEIGHT_PER_SIGOP
        if ex["weight_left"] < 0: raise ScriptError("TAPSCRIPT_VALIDATION_WEIGHT")
    if len(pk) == 0: raise ScriptError("TAPSCRIPT_EMPTY_PUBKEY")
    if len(pk) == 32:
        if ok: checker.schnorr(sig, pk, sigversion, ex)
    elif "DISCOURAGE_UPGRADABLE_PUBKEYTYPE" in flags:                  # a key that is not 32 bytes is an unknown key type: it succeeds with any non-empty signature, but relay policy refuses it
        raise ScriptError("DISCOURAGE_UPGRADABLE_PUBKEYTYPE")
    return ok

# =====================================================================================================================
# VerifyScript: scriptSig, scriptPubKey, pay to script hash, witness programs
# =====================================================================================================================
def is_push_only(script):
    try: return all(op <= OP_16 and op != 80 for _, op, _ in get_ops(script))
    except ScriptError: return False


def witness_program(spk):
    """(version, program) when spk is a witness program (a version byte 0 or 1 to 16, then one push of 2 to 40 bytes)"""
    if 4 <= len(spk) <= 42 and (spk[0] == 0 or 81 <= spk[0] <= 96) and spk[1] + 2 == len(spk):
        return (0 if spk[0] == 0 else spk[0] - 80), spk[2:]
    return None


def is_p2sh(spk): return len(spk) == 23 and spk[0] == 0xa9 and spk[1] == 20 and spk[22] == 0x87


def _witness_serialize_size(stack):
    return len(cs_encode(len(stack))) + sum(len(cs_encode(len(i))) + len(i) for i in stack)


def tap_leaf_hash(leaf_version, script): return tagged_hash("TapLeaf", bytes([leaf_version]) + cs_encode(len(script)) + script)
def tap_branch_hash(a, b): return tagged_hash("TapBranch", min(a, b) + max(a, b))


def _verify_witness_program(wit, ver, prog, flags, checker, is_p2sh_, trace=None):
    stack = list(wit)
    if ver == 0:
        if len(prog) == 32:
            if not stack: raise ScriptError("WITNESS_PROGRAM_WITNESS_EMPTY")
            script = stack.pop()
            if sha256(script) != prog: raise ScriptError("WITNESS_PROGRAM_MISMATCH")
        elif len(prog) == 20:
            if len(stack) != 2: raise ScriptError("WITNESS_PROGRAM_MISMATCH")
            script = bytes([0x76, 0xa9, 20]) + prog + bytes([0x88, 0xac])
        else:
            raise ScriptError("WITNESS_PROGRAM_WRONG_LENGTH")
        return _exec_witness_script(stack, script, flags, "WITNESS_V0", checker, {}, trace)
    if ver == 1 and len(prog) == 32 and not is_p2sh_:
        if "TAPROOT" not in flags: return
        if not stack: raise ScriptError("WITNESS_PROGRAM_WITNESS_EMPTY")
        ex = {}
        if len(stack) >= 2 and stack[-1] and stack[-1][0] == 0x50: ex["annex"] = stack.pop()
        if len(stack) == 1:
            checker.schnorr(stack[0], prog, "TAPROOT", ex)
            return
        control, script = stack.pop(), stack.pop()
        if len(control) < 33 or len(control) > 33 + 32 * 128 or (len(control) - 33) % 32: raise ScriptError("TAPROOT_WRONG_CONTROL_SIZE")
        leaf_h = k = tap_leaf_hash(control[0] & 0xfe, script)
        for i in range(33, len(control), 32): k = tap_branch_hash(k, control[i:i + 32])
        internal = control[1:33]
        P_ = lift_x(int.from_bytes(internal, "big"))
        t = int.from_bytes(tagged_hash("TapTweak", internal + k), "big")
        ok = P_ is not None and t < N
        if ok:
            Q = point_add(P_, point_mul(t))
            ok = Q is not None and Q[0].to_bytes(32, "big") == prog and (Q[1] & 1) == (control[0] & 1)
        if not ok: raise ScriptError("WITNESS_PROGRAM_MISMATCH")
        ex["tapleaf"] = leaf_h                            # the hash of the executed leaf, not of the root the path folds up to
        if control[0] & 0xfe == 0xc0:
            ex["weight_left"] = _witness_serialize_size(wit) + VALIDATION_WEIGHT_OFFSET
            return _exec_witness_script(stack, script, flags, "TAPSCRIPT", checker, ex, trace)
        if "DISCOURAGE_UPGRADABLE_TAPROOT_VERSION" in flags: raise ScriptError("DISCOURAGE_UPGRADABLE_TAPROOT_VERSION")
        return
    if "DISCOURAGE_UPGRADABLE_WITNESS_PROGRAM" in flags: raise ScriptError("DISCOURAGE_UPGRADABLE_WITNESS_PROGRAM")


def _exec_witness_script(stack, script, flags, sigversion, checker, ex, trace):
    if sigversion == "TAPSCRIPT":
        for _, op, _ in iter_ops(script):
            if is_op_success(op):
                if "DISCOURAGE_OP_SUCCESS" in flags: raise ScriptError("DISCOURAGE_OP_SUCCESS")
                return
        if len(stack) > MAX_STACK: raise ScriptError("STACK_SIZE")
    for e in stack:
        if len(e) > MAX_ELEMENT: raise ScriptError("PUSH_SIZE")
    eval_script(stack, script, flags, checker, sigversion, ex, trace)
    if len(stack) != 1: raise ScriptError("CLEANSTACK")
    if not cast_to_bool(stack[-1]): raise ScriptError("EVAL_FALSE")


def verify_script(script_sig, script_pubkey, witness, flags, checker, trace=None):
    """Bitcoin Core's VerifyScript. Returns "OK" or the name of the error (EVAL_FALSE, SIG_NULLDUMMY, ...)."""
    flags = frozenset(flags)
    try:
        if "SIGPUSHONLY" in flags and not is_push_only(script_sig): raise ScriptError("SIG_PUSHONLY")
        stack = []
        eval_script(stack, script_sig, flags, checker, "BASE", None, trace)
        copy = list(stack) if "P2SH" in flags else None
        eval_script(stack, script_pubkey, flags, checker, "BASE", None, trace)
        if not stack or not cast_to_bool(stack[-1]): raise ScriptError("EVAL_FALSE")
        had = False
        if "WITNESS" in flags:
            wp = witness_program(script_pubkey)
            if wp:
                had = True
                if script_sig: raise ScriptError("WITNESS_MALLEATED")
                _verify_witness_program(witness, wp[0], wp[1], flags, checker, False, trace)
                del stack[:-1]
        if "P2SH" in flags and is_p2sh(script_pubkey):
            if not is_push_only(script_sig): raise ScriptError("SIG_PUSHONLY")
            stack = copy
            redeem = stack.pop()
            eval_script(stack, redeem, flags, checker, "BASE", None, trace)
            if not stack or not cast_to_bool(stack[-1]): raise ScriptError("EVAL_FALSE")
            if "WITNESS" in flags:
                wp = witness_program(redeem)
                if wp:
                    had = True
                    if script_sig != push_data(redeem): raise ScriptError("WITNESS_MALLEATED_P2SH")
                    _verify_witness_program(witness, wp[0], wp[1], flags, checker, True, trace)
                    del stack[:-1]
        if "CLEANSTACK" in flags and len(stack) != 1: raise ScriptError("CLEANSTACK")
        if "WITNESS" in flags and not had and witness: raise ScriptError("WITNESS_UNEXPECTED")
        return "OK"
    except ScriptError as e:
        return e.name
    except IndexError:
        return "INVALID_STACK_OPERATION"


def verify_input(tx, nin, spent, flags=MAINNET_FLAGS, trace=None):
    """Verify one input of tx against the outputs it spends: spent is the list of (amount, scriptPubKey) of every input."""
    amount, spk = spent[nin]
    return verify_script(tx.vin[nin][2], spk, tx.witness[nin], flags, Checker(tx, nin, amount, spent), trace)

# =====================================================================================================================
# templates, addresses, classification, signing helpers (for the worked examples)
# =====================================================================================================================
def p2pk_script(pub): return push_data(pub) + b"\xac"
def p2pkh_script(h20): return b"\x76\xa9\x14" + h20 + b"\x88\xac"
def p2sh_script(h20): return b"\xa9\x14" + h20 + b"\x87"
def p2wpkh_script(h20): return b"\x00\x14" + h20
def p2wsh_script(h32): return b"\x00\x20" + h32
def p2tr_script(x32): return b"\x51\x20" + x32
def op_return_script(data): return b"\x6a" + push_data(data)


def multisig_script(m, pubkeys):
    assert 1 <= m <= len(pubkeys) <= 20
    return push_int(m) + b"".join(push_data(p) for p in pubkeys) + push_int(len(pubkeys)) + b"\xae"


def script_to_address(spk, hrp="bc"):
    t, info = classify(spk)
    if t == "pubkeyhash": return b58check_encode(0, spk[3:23])
    if t == "scripthash": return b58check_encode(5, spk[2:22])
    if t in ("witness_v0_keyhash", "witness_v0_scripthash"): return segwit_address(hrp, 0, spk[2:])
    if t == "witness_v1_taproot": return segwit_address(hrp, 1, spk[2:])
    return None


def address_to_script(addr, hrp="bc"):
    if addr.lower().startswith(hrp + "1"):
        v, prog = segwit_decode(hrp, addr)
        return bytes([0 if v == 0 else 80 + v, len(prog)]) + prog
    v, h = b58check_decode(addr)
    return p2pkh_script(h) if v == 0 else p2sh_script(h)


def classify(spk):
    """the type of an output script, by Bitcoin Core's standard templates (Solver); the second value is a short description"""
    if len(spk) == 25 and spk[:3] == b"\x76\xa9\x14" and spk[23:] == b"\x88\xac": return "pubkeyhash", "OP_DUP OP_HASH160 <20 bytes> OP_EQUALVERIFY OP_CHECKSIG"
    if is_p2sh(spk): return "scripthash", "OP_HASH160 <20 bytes> OP_EQUAL"
    if len(spk) == 22 and spk[:2] == b"\x00\x14": return "witness_v0_keyhash", "0 <20 bytes>"
    if len(spk) == 34 and spk[:2] == b"\x00\x20": return "witness_v0_scripthash", "0 <32 bytes>"
    if len(spk) == 34 and spk[:2] == b"\x51\x20": return "witness_v1_taproot", "1 <32 bytes>"
    if spk[:1] == b"\x6a" and is_push_only(spk[1:]): return "nulldata", "OP_RETURN <data>"
    if len(spk) in (35, 67) and spk[0] in (33, 65) and spk[-1] == 0xac and len(spk) == spk[0] + 2: return "pubkey", "<pubkey> OP_CHECKSIG"
    try:
        ops = get_ops(spk)
        if len(ops) >= 4 and ops[-1][1] == 0xae and 81 <= ops[0][1] <= 96 and 81 <= ops[-2][1] <= 96:
            keys = [d for _, o, d in ops[1:-2] if d is not None and len(d) in (33, 65)]
            m, n = ops[0][1] - 80, ops[-2][1] - 80
            if len(keys) == n == len(ops) - 3 and m <= n: return "multisig", "%d-of-%d" % (m, n)
    except ScriptError:
        pass
    return "nonstandard", ""


def sign_ecdsa_input(tx, nin, script_code, secret, hashtype=SIGHASH_ALL, amount=None, sigversion="BASE"):
    h = sighash_v0(script_code, tx, nin, hashtype, amount) if sigversion == "WITNESS_V0" else sighash_legacy(script_code, tx, nin, hashtype)
    return ecdsa_sign(secret, h) + bytes([hashtype])


def sign_taproot_input(tx, nin, spent, secret, hashtype=0, tapleaf_hash=None, merkle_root=None, codesep=0xffffffff):
    """Schnorr signature for a key path spend (secret tweaked by merkle_root, b"" for no script tree) or, with tapleaf_hash, a script path leaf key"""
    if tapleaf_hash is None:
        h = sighash_taproot(tx, nin, hashtype, spent)
        sig = schnorr_sign(taproot_tweak_seckey(secret, merkle_root or b""), h)
    else:
        h = sighash_taproot(tx, nin, hashtype, spent, 1, None, tapleaf_hash, codesep)
        sig = schnorr_sign(secret, h)
    return sig + (bytes([hashtype]) if hashtype else b"")


def credit_and_spend(script_sig, script_pubkey, witness=(), amount=0, locktime=0, sequence=SEQ_FINAL, version=1):
    """Bitcoin Core's test arrangement: a crediting transaction with one output (script_pubkey, amount) and a spending
    transaction with one input that spends it. Returns (spend_tx, spent_list)"""
    credit = Tx(1, [(b"\x00" * 32, 0xffffffff, push_int(0) + push_int(0), SEQ_FINAL)], [(amount, script_pubkey)], 0)
    h = hash256(credit.serialize(False))
    spend = Tx(version, [(h, 0, script_sig, sequence)], [(amount, b"")], locktime, [list(witness)])
    return spend, [(amount, script_pubkey)]


def run(script_sig_asm, script_pubkey_asm, flags=("P2SH",), witness=(), trace=None, **kw):
    """assemble two scripts in Bitcoin Core's notation and verify them as a crediting/spending pair; "OK" or an error name"""
    tx, spent = credit_and_spend(assemble(script_sig_asm), assemble(script_pubkey_asm), witness, **kw)
    return verify_script(tx.vin[0][2], spent[0][1], tx.witness[0], flags, Checker(tx, 0, spent[0][0], spent), trace)
