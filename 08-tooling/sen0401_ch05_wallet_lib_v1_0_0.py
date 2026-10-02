"""SEN0401 chapter 5 library: the arithmetic and encodings of wallet recovery (seeds, BIP39 recovery codes, BIP32 extended keys,
output script descriptor checksums, a toy secret-sharing scheme) in plain Python with only the standard library, written for
reading, and checked in sen0401_ch05_verify_v1_0_0.py against the BIP32 test vectors, the BIP380 test vectors, the book's own
numbers and Bitcoin Core 31.1. Not for use with real funds: it is not constant-time and takes no care over where randomness
comes from. The elliptic curve and base58check parts follow sen0401_keys_toolkit_v1_0_0.py (chapter 4), copied here so that
this chapter does not depend on another chapter's file.
Run from 08-tooling (the word list is read from ch05-evidence/bip39_english.txt)."""
__version__ = "1.0.0"
import hashlib, hmac, os, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


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


def ser_p(pt):   # compressed public key bytes (BIP32 serP)
    return bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(32, "big")


def ser_uncompressed(pt):
    return b"\x04" + pt[0].to_bytes(32, "big") + pt[1].to_bytes(32, "big")


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


def p2pkh(pub):
    return b58check(b"\x00" + hash160(pub))


# ---------------- BIP39 ----------------
def wordlist():
    with open(os.path.join(HERE, "ch05-evidence", "bip39_english.txt")) as f:
        w = f.read().split()
    assert len(w) == 2048
    return w


def entropy_to_mnemonic(ent, words=None):
    words = words or wordlist()
    assert len(ent) * 8 in (128, 160, 192, 224, 256)
    cs_bits = len(ent) * 8 // 32
    bits = bin(int.from_bytes(ent, "big"))[2:].zfill(len(ent) * 8) + bin(hashlib.sha256(ent).digest()[0])[2:].zfill(8)[:cs_bits]
    return " ".join(words[int(bits[i:i + 11], 2)] for i in range(0, len(bits), 11))


def mnemonic_to_entropy(mn, words=None):
    words = words or wordlist()
    idx = [words.index(w) for w in mn.split()]
    bits = "".join(bin(i)[2:].zfill(11) for i in idx)
    cs_len = len(bits) // 33
    ent_bits, cs = bits[:-cs_len], bits[-cs_len:]
    ent = int(ent_bits, 2).to_bytes(len(ent_bits) // 8, "big")
    ok = bin(hashlib.sha256(ent).digest()[0])[2:].zfill(8)[:cs_len] == cs
    return ent, ok


def mnemonic_to_seed(mn, passphrase=""):
    return hashlib.pbkdf2_hmac("sha512", unicodedata.normalize("NFKD", mn).encode(),
                               unicodedata.normalize("NFKD", "mnemonic" + passphrase).encode(), 2048)


# ---------------- BIP32 ----------------
HARD = 2**31


def master(seed):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    k = int.from_bytes(I[:32], "big"); assert 0 < k < N
    return k, I[32:]


def ckd_priv(k, c, i):
    data = (b"\x00" + k.to_bytes(32, "big") if i >= HARD else ser_p(ec_mul(k))) + i.to_bytes(4, "big")
    I = hmac.new(c, data, hashlib.sha512).digest()
    il = int.from_bytes(I[:32], "big"); assert il < N
    return (il + k) % N, I[32:]


def ckd_pub(K, c, i):
    assert i < HARD, "no public derivation of a hardened child"
    I = hmac.new(c, ser_p(K) + i.to_bytes(4, "big"), hashlib.sha512).digest()
    il = int.from_bytes(I[:32], "big"); assert il < N
    return ec_add(ec_mul(il), K), I[32:]


def path_indices(path):
    out = []
    for part in path.split("/")[1:]:
        h = part.endswith(("'", "h", "H"))
        out.append(int(part.rstrip("'hH")) + (HARD if h else 0))
    return out


def derive_priv(k, c, path):
    for i in path_indices(path): k, c = ckd_priv(k, c, i)
    return k, c


XPRV, XPUB = bytes.fromhex("0488ADE4"), bytes.fromhex("0488B21E")


def serialize_xprv(k, c, depth=0, parent_fp=b"\0\0\0\0", index=0):
    return b58check(XPRV + bytes([depth]) + parent_fp + index.to_bytes(4, "big") + c + b"\x00" + k.to_bytes(32, "big"))


def serialize_xpub(K, c, depth=0, parent_fp=b"\0\0\0\0", index=0):
    return b58check(XPUB + bytes([depth]) + parent_fp + index.to_bytes(4, "big") + c + ser_p(K))


def parse_extended(text):
    raw = b58check_decode(text)
    assert len(raw) == 78
    return dict(version=raw[:4], depth=raw[4], fp=raw[5:9], index=int.from_bytes(raw[9:13], "big"), chain=raw[13:45], key=raw[45:])


def fingerprint(K):
    return hash160(ser_p(K))[:4]


def derive_serialized(seed, path):
    """the xprv and xpub text at a path (as BIP32 test vectors list them)"""
    k, c = master(seed); depth = 0; fp = b"\0\0\0\0"; idx = 0
    for i in path_indices(path):
        fp = fingerprint(ec_mul(k)); k, c = ckd_priv(k, c, i); depth += 1; idx = i
    return serialize_xprv(k, c, depth, fp, idx), serialize_xpub(ec_mul(k), c, depth, fp, idx)


# ---------------- BIP380 descriptor checksum ----------------
INPUT_CHARSET = "0123456789()[],'/*abcdefgh@:$%{}IJKLMNOPQRSTUVWXYZ&+-.;<=>?!^_|~ijklmnopqrstuvwxyzABCDEFGH`#\"\\ "
CHECKSUM_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
GENERATOR = [0xf5dee51989, 0xa9fdca3312, 0x1bab10e32d, 0x3706b1677a, 0x644d626ffd]


def descsum_polymod(symbols):
    chk = 1
    for value in symbols:
        top = chk >> 35
        chk = (chk & 0x7ffffffff) << 5 ^ value
        for i in range(5):
            chk ^= GENERATOR[i] if ((top >> i) & 1) else 0
    return chk


def descsum_expand(s):
    groups = []; symbols = []
    for c in s:
        if c not in INPUT_CHARSET: return None
        v = INPUT_CHARSET.find(c)
        symbols.append(v & 31); groups.append(v >> 5)
        if len(groups) == 3:
            symbols.append(groups[0] * 9 + groups[1] * 3 + groups[2]); groups = []
    if len(groups) == 1: symbols.append(groups[0])
    elif len(groups) == 2: symbols.append(groups[0] * 3 + groups[1])
    return symbols


def descsum_check(s):
    if s[-9] != "#": return False
    if not all(x in CHECKSUM_CHARSET for x in s[-8:]): return False
    symbols = descsum_expand(s[:-9]) + [CHECKSUM_CHARSET.find(x) for x in s[-8:]]
    return descsum_polymod(symbols) == 1


def descsum_create(s):
    symbols = descsum_expand(s) + [0] * 8
    checksum = descsum_polymod(symbols) ^ 1
    return s + "#" + "".join(CHECKSUM_CHARSET[(checksum >> (5 * (7 - i))) & 31] for i in range(8))


# ---------------- a toy secret-sharing scheme (Shamir, over a prime field; NOT SLIP39, which works in GF(256)) ----------------
PRIME = 2**127 - 1


def shamir_split(secret, threshold, shares, coeffs, prime=PRIME):
    """coeffs: threshold-1 numbers standing in for the random coefficients (a real scheme draws them from a secure random source)"""
    poly = [secret] + list(coeffs)
    assert len(poly) == threshold
    return [(x, sum(c * pow(x, e, prime) for e, c in enumerate(poly)) % prime) for x in range(1, shares + 1)]


def shamir_combine(points, prime=PRIME):
    total = 0
    for j, (xj, yj) in enumerate(points):
        num = den = 1
        for m, (xm, _) in enumerate(points):
            if m != j: num = num * (-xm) % prime; den = den * (xj - xm) % prime
        total = (total + yj * num * pow(den, -1, prime)) % prime
    return total


# ---------------- gap limit scan (a small model) ----------------
def scan_with_gap(used, gap):
    """used: set of key indices that received a payment. Scan keys 0,1,2,... and stop after `gap` unused keys in a row;
    returns the sorted list of used indices found."""
    found = []; run = 0; i = 0
    while run < gap:
        if i in used: found.append(i); run = 0
        else: run += 1
        i += 1
    return found


# ---------------- extra demonstrations ----------------
def ckd_priv_uncompressed_input(k, c, i):
    """what a normal child derivation would give if the parent public key went into the hash in its 65-byte uncompressed form
    (the chapter says 'uncompressed key'; BIP32 serializes the compressed form): used only to show that the results differ"""
    assert i < HARD
    I = hmac.new(c, ser_uncompressed(ec_mul(k)) + i.to_bytes(4, "big"), hashlib.sha512).digest()
    return (int.from_bytes(I[:32], "big") + k) % N, I[32:]


def leak_parent_private_key(parent_pub, parent_chain, child_index, child_priv):
    """a normal child private key plus the parent's EXTENDED PUBLIC key reveals the parent private key: k_par = k_child - I_L mod n"""
    assert child_index < HARD
    I = hmac.new(parent_chain, ser_p(parent_pub) + child_index.to_bytes(4, "big"), hashlib.sha512).digest()
    return (child_priv - int.from_bytes(I[:32], "big")) % N


CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = (0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3); chk = 1
    for v in values:
        top = chk >> 25; chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if (top >> i) & 1 else 0
    return chk


def _convertbits(data, frm, to):
    acc = bits = 0; out = []; maxv = (1 << to) - 1
    for v in data:
        acc = (acc << frm) | v; bits += frm
        while bits >= to: bits -= to; out.append((acc >> bits) & maxv)
    if bits: out.append((acc << (to - bits)) & maxv)
    return out


def p2wpkh_address(pub33, hrp="bc"):
    """native segwit version 0 address of a compressed public key (bech32)"""
    data = [0] + _convertbits(hash160(pub33), 8, 5)
    values = [ord(c) >> 5 for c in hrp] + [0] + [ord(c) & 31 for c in hrp] + data
    pm = _polymod(values + [0] * 6) ^ 1
    return hrp + "1" + "".join(CHARSET[d] for d in data + [(pm >> 5 * (5 - i)) & 31 for i in range(6)])
