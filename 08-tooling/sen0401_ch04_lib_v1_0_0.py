"""sen0401_ch04_lib v1.0.0 - the chapter library of the chapter 4 deck (Keys and Addresses) and of its page tab 'chapter code'.
Standard library only (hashlib, struct, math), so it runs unchanged in the page's Python (Pyodide has no native RIPEMD-160: this file carries one, used only when hashlib lacks it).
Built from the chapter toolkit sen0401_ch04_keys_v1_1_0.py (the elliptic curve arithmetic, Base58Check, Bech32 and Bech32m, checked against Bitcoin Core 31.1, the sipa/bech32 reference
and the BIP350 test vectors by sen0401_ch04_verify_v1_0_0.py), plus the book's example values and a few helpers that keep every listing on the slides within one short line.
Not for use with real funds: it is not constant-time and takes no care over where randomness comes from."""
__version__ = "1.0.0"
import hashlib, struct

P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
# --- ec ---
def ec_add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    m = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (m * m - a[0] - b[0]) % P
    return (x, (m * (a[0] - x) - a[1]) % P)
def ec_mul(k, pt=G):
    out = None
    while k:
        if k & 1: out = ec_add(out, pt)
        pt = ec_add(pt, pt); k >>= 1
    return out
# --- end ec ---
def pub_bytes(pt, compressed=True):
    return (bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(32, "big")) if compressed else (b"\x04" + pt[0].to_bytes(32, "big") + pt[1].to_bytes(32, "big"))
def decompress(pub33):
    x = int.from_bytes(pub33[1:], "big"); y = pow((x**3 + 7) % P, (P + 1) // 4, P)
    assert (y * y - x**3 - 7) % P == 0, "x is not on the curve"
    return (x, y if y & 1 == pub33[0] & 1 else P - y)
dsha = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()
hash160 = lambda b: ripemd160(hashlib.sha256(b).digest())
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
def b58check(payload):
    data = payload + dsha(payload)[:4]; n = int.from_bytes(data, "big"); s = ""
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return "1" * (len(data) - len(data.lstrip(b"\0"))) + s
def b58check_decode(text):
    n = 0
    for ch in text: n = n * 58 + B58.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    raw = b"\0" * (len(text) - len(text.lstrip("1"))) + raw
    assert dsha(raw[:-4])[:4] == raw[-4:], "checksum does not match"
    return raw[:-4]
p2pkh = lambda pub: b58check(b"\x00" + hash160(pub))
p2sh = lambda script: b58check(b"\x05" + hash160(script))
wif = lambda k, compressed=True: b58check(b"\x80" + k.to_bytes(32, "big") + (b"\x01" if compressed else b""))
CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
BECH32, BECH32M = 1, 0x2bc830a3
def polymod(values):
    gen = (0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3); chk = 1
    for v in values:
        top = chk >> 25; chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if (top >> i) & 1 else 0
    return chk
hrp_expand = lambda hrp: [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp]
def convertbits(data, frm, to, pad=True):
    acc = bits = 0; out = []; maxv = (1 << to) - 1
    for v in data:
        acc = (acc << frm) | v; bits += frm
        while bits >= to: bits -= to; out.append((acc >> bits) & maxv)
    if pad and bits: out.append((acc << (to - bits)) & maxv)
    elif not pad and (bits >= frm or (acc << (to - bits)) & maxv): return None   # more than 4 bits of padding, or padding that is not zero
    return out
def bech_encode(hrp, data, const):
    values = hrp_expand(hrp) + data; pm = polymod(values + [0] * 6) ^ const
    return hrp + "1" + "".join(CHARSET[d] for d in data + [(pm >> 5 * (5 - i)) & 31 for i in range(6)])
def bech_check(addr):
    """the constant the checksum satisfies (BECH32, BECH32M) or None"""
    hrp, _, d = addr.lower().rpartition("1"); data = [CHARSET.find(c) for c in d]
    if -1 in data: return None
    pm = polymod(hrp_expand(hrp) + data)
    return pm if pm in (BECH32, BECH32M) else None
def segwit_address(hrp, ver, prog):
    return bech_encode(hrp, [ver] + convertbits(prog, 8, 5), BECH32 if ver == 0 else BECH32M)
def segwit_decode(hrp, addr):
    if addr != addr.lower() and addr != addr.upper(): return None   # mixed case
    if not addr.lower().startswith(hrp + "1"): return None
    const = bech_check(addr)
    if const is None: return None
    data = [CHARSET.find(c) for c in addr.lower().rpartition("1")[2]][:-6]
    if not data: return None
    ver = data[0]; conv = convertbits(data[1:], 5, 8, False)
    if conv is None: return None
    prog = bytes(conv)
    if (ver == 0 and const != BECH32) or (ver > 0 and const != BECH32M) or not 2 <= len(prog) <= 40 or ver > 16 or (ver == 0 and len(prog) not in (20, 32)): return None
    return ver, prog

# ---- added in 1.1.0 ----
def b58decode_int(text):
    n = 0
    for ch in text: n = n * 58 + B58.index(ch)
    return n
def ecdsa_sign(d, z, k):
    """teaching sketch: sign the 256-bit number z (a message hash) with private key d and nonce k (a real signer derives k deterministically or draws it from a secure source)"""
    r = ec_mul(k)[0] % N; s = pow(k, -1, N) * (z + r * d) % N
    return (r, s)
def ecdsa_verify(Q, z, sig):
    r, s = sig
    if not (1 <= r < N and 1 <= s < N): return False
    w = pow(s, -1, N); X = ec_add(ec_mul(z * w % N), ec_mul(r * w % N, Q))
    return X is not None and X[0] % N == r
def run_p2pkh(sig, pub, commitment):
    """the legacy P2PKH script <sig> <pubkey> OP_DUP OP_HASH160 <commitment> OP_EQUALVERIFY OP_CHECKSIG on a list used as a stack; the signature check is stood in for by a callable"""
    st = [sig, pub]; st.append(st[-1]); st.append(hash160(st.pop()))
    st.append(commitment); a, b = st.pop(), st.pop()
    if a != b: return False
    return st

def small_add(a, b, p):
    """point addition on y^2 = x^3 + 7 over F_p for a small prime p (None is the point at infinity); the same rules as ec_add, with p as an argument"""
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % p == 0: return None
    m = (3 * a[0] * a[0] * pow(2 * a[1], -1, p) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, p)) % p
    x = (m * m - a[0] - b[0]) % p
    return (x, (m * (a[0] - x) - a[1]) % p)
def small_order(pt, p):
    """how many times pt must be added to itself to reach the point at infinity"""
    n, q = 1, pt
    while q is not None: q = small_add(q, pt, p); n += 1
    return n

def is_probable_prime(n, rounds=24):
    """Miller-Rabin with the first prime bases: a composite number passes every one of them only with negligible probability"""
    if n < 2: return False
    for q in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % q == 0: return n == q
    d, r = n - 1, 0
    while d % 2 == 0: d //= 2; r += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)[:rounds]:
        x = pow(a, d, n)
        if x in (1, n - 1): continue
        for _ in range(r - 1):
            x = x * x % n
            if x == n - 1: break
        else: return False
    return True
def is_valid_b58check(text):
    """True if text is made of base58 characters and its last four bytes are the checksum of the rest"""
    try: b58check_decode(text); return True
    except (ValueError, AssertionError): return False

# ---- RIPEMD-160, used only where hashlib lacks it ----
_M = 0xFFFFFFFF
_RL = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15, 7,4,13,1,10,6,15,3,12,0,9,5,2,14,11,8, 3,10,14,4,9,15,8,1,2,7,0,6,13,11,5,12, 1,9,11,10,0,8,12,4,13,3,7,15,14,5,6,2, 4,0,5,9,7,12,2,10,14,1,3,8,11,6,15,13)
_RR = (5,14,7,0,9,2,11,4,13,6,15,8,1,10,3,12, 6,11,3,7,0,13,5,10,14,15,8,12,4,9,1,2, 15,5,1,3,7,14,6,9,11,8,12,2,10,0,4,13, 8,6,4,1,3,11,15,0,5,12,2,13,9,7,10,14, 12,15,10,4,1,5,8,7,6,2,13,14,0,3,9,11)
_SL = (11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8, 7,6,8,13,11,9,7,15,7,12,15,9,11,7,13,12, 11,13,6,7,14,9,13,15,14,8,13,6,5,12,7,5, 11,12,14,15,14,15,9,8,9,14,5,6,8,6,5,12, 9,15,5,11,6,8,13,12,5,12,13,14,11,8,5,6)
_SR = (8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6, 9,13,15,7,12,8,9,11,7,7,12,7,6,15,13,11, 9,7,15,11,8,6,6,14,12,13,5,14,13,13,7,5, 15,5,8,11,14,14,6,14,6,9,12,9,12,5,15,8, 8,5,12,9,12,5,14,6,8,13,6,5,15,13,11,11)
_KL = (0x00000000, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E)
_KR = (0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0x00000000)
def _rol(x, n): return ((x << n) | (x >> (32 - n))) & _M
def _f(j, x, y, z):
    if j < 16: return x ^ y ^ z
    if j < 32: return (x & y) | (~x & _M & z)
    if j < 48: return (x | (~y & _M)) ^ z
    if j < 64: return (x & z) | (y & (~z & _M))
    return x ^ (y | (~z & _M))
def _r160_block(h, block):
    x = struct.unpack("<16I", block)
    al, bl, cl, dl, el = h; ar, br, cr, dr, er = h
    for j in range(80):
        t = (_rol((al + _f(j, bl, cl, dl) + x[_RL[j]] + _KL[j // 16]) & _M, _SL[j]) + el) & _M
        al, el, dl, cl, bl = el, dl, _rol(cl, 10), bl, t
        t = (_rol((ar + _f(79 - j, br, cr, dr) + x[_RR[j]] + _KR[j // 16]) & _M, _SR[j]) + er) & _M
        ar, er, dr, cr, br = er, dr, _rol(cr, 10), br, t
    t = (h[1] + cl + dr) & _M
    return [t, (h[2] + dl + er) & _M, (h[3] + el + ar) & _M, (h[4] + al + br) & _M, (h[0] + bl + cr) & _M]
class _RIPEMD160:
    name = "ripemd160"; digest_size = 20; block_size = 64
    def __init__(self, data=b""):
        self._h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]; self._buf = b""; self._len = 0
        if data: self.update(data)
    def update(self, data):
        data = bytes(data); self._len += len(data); b = self._buf + data
        n = len(b) - len(b) % 64
        for i in range(0, n, 64): self._h = _r160_block(self._h, b[i:i + 64])
        self._buf = b[n:]; return None
    def copy(self):
        c = _RIPEMD160(); c._h = list(self._h); c._buf = self._buf; c._len = self._len; return c
    def digest(self):
        c = self.copy(); pad = b"\x80" + b"\0" * ((55 - c._len) % 64) + struct.pack("<Q", (c._len * 8) & 0xFFFFFFFFFFFFFFFF)
        c.update(pad); return struct.pack("<5I", *c._h)
    def hexdigest(self): return self.digest().hex()
def _native_ripemd(data):
    return hashlib.new("ripemd160", data).digest()
try:
    _native_ripemd(b"")
    ripemd160 = _native_ripemd
except Exception:
    ripemd160 = lambda data: _RIPEMD160(data).digest()


# ---- the book's example values (Mastering Bitcoin 3rd edition, chapter 4) ----
BOOK_K = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD     # the private key of the book's worked example
PROG_WPKH = bytes.fromhex("2b626ed108ad00a944bb2922a309844611d25468")             # witness programs the book prints
PROG_WSH = bytes.fromhex("648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f")
PROG_TR = bytes.fromhex("2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311")
EXT = ["bc1pqqqsq9txsqp", "bc1pqqqsq9txsqqqqp", "bc1pqqqsq9txsqqqqqqp", "bc1pqqqsq9txsqqqqqqqqp"]   # the book's length-extension strings: a 'q' inserted before the last 'p'
EATER = "1BitcoinEaterAddressDontSendf59kuE"                                       # a valid address that spells a message; nobody holds its key
SMALL_P, SMALL_PT = 17, (1, 5)                                                    # a toy field and a point of y^2 = x^3 + 7 over it


def bits_of(n_symbols, length):
    """the entropy of a secret drawn uniformly: length symbols out of n_symbols, in bits"""
    import math
    return round(length * math.log2(n_symbols), 1)


def multiples(n_max, pt=SMALL_PT, p=SMALL_P):
    """pt, 2pt, 3pt ... on the toy curve, up to n_max multiples; None is the point at infinity"""
    out, q = [], None
    for _ in range(n_max):
        q = small_add(q, pt, p); out.append(q)
    return out


def multisig_script(m, pubkeys):
    """the bare m-of-n multisignature script: OP_m <pubkey>... OP_n OP_CHECKMULTISIG, as bytes"""
    return bytes([0x50 + m]) + b"".join(bytes([len(k)]) + k for k in pubkeys) + bytes([0x50 + len(pubkeys), 0xAE])


def p2pk_script(pub):
    """<pubkey> OP_CHECKSIG: the original output script"""
    return bytes([len(pub)]) + pub + b"\xac"


def p2pkh_script(pub):
    """OP_DUP OP_HASH160 <hash160> OP_EQUALVERIFY OP_CHECKSIG"""
    return b"\x76\xa9\x14" + hash160(pub) + b"\x88\xac"


def single_typos(text):
    """every string that differs from text in exactly one position, with another base58 character there"""
    return [text[:i] + c + text[i + 1:] for i in range(len(text)) for c in B58 if c != text[i]]


def key_to_address(k, compressed=True):
    """private key -> public key -> P2PKH address"""
    return p2pkh(pub_bytes(ec_mul(k), compressed))
