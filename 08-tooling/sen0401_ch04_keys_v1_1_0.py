"""SEN0401 chapter 4 toolkit: the arithmetic and encodings of Keys and Addresses, in plain Python with only the standard
library, written for reading and checked against Bitcoin Core 31.1, the book's own reference library (sipa/bech32) and
the BIP350 test vectors (sen0401_ch04_verify_v1_0_0.py). Not for use with real funds: it is not constant-time and
takes no care over where randomness comes from."""
__version__ = "1.1.0"
import hashlib
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
hash160 = lambda b: hashlib.new("ripemd160", hashlib.sha256(b).digest()).digest()
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
