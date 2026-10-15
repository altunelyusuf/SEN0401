#!/usr/bin/env python3
"""SEN0401 chapter 14 (Second-Layer Applications): the cryptography that the Lightning specification (the BOLTs) names, written in plain Python 3 so that the chapter's claims can recompute
the published test vectors without any package. Standard library only (hashlib, hmac, struct).
* secp256k1: point addition and multiplication, compressed encoding, ECDSA with RFC 6979 nonces (low S) and verification
* ChaCha20, Poly1305 and the AEAD of RFC 8439, HMAC-SHA256 and HKDF
* bech32 (BIP 173) decoding without the 90-character limit, as BOLT 11 invoices need
* the transport handshake of BOLT 8 (Noise_XK_secp256k1_ChaChaPoly_SHA256), the onion packet of BOLT 4 (Sphinx), the keys and secrets of BOLT 3
* the legacy and segwit signature hashes and a transaction serializer, enough to build and sign the contracts of the chapter on a private chain
Slow on purpose (no tables, no C): each multiplication takes a few milliseconds."""
__version__ = "1.0.0"
import hashlib, hmac, re, struct

# ------------------------------------------------------------------------------------------------ secp256k1
P = 2 ** 256 - 2 ** 32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def padd(a, b):
    if a is None:
        return b
    if b is None:
        return a
    if a[0] == b[0]:
        if (a[1] + b[1]) % P == 0:
            return None
        l = 3 * a[0] * a[0] * pow(2 * a[1], -1, P) % P
    else:
        l = (b[1] - a[1]) * pow(b[0] - a[0], -1, P) % P
    x = (l * l - a[0] - b[0]) % P
    return (x, (l * (a[0] - x) - a[1]) % P)


def pmul(k, pt=G):
    k %= N
    r = None
    while k:
        if k & 1:
            r = padd(r, pt)
        pt = padd(pt, pt)
        k >>= 1
    return r


def pneg(pt):
    return (pt[0], (-pt[1]) % P)


def ser(pt):
    return bytes([2 + (pt[1] & 1)]) + pt[0].to_bytes(32, "big")


def parse(b):
    x = int.from_bytes(b[1:33], "big")
    y = pow((x ** 3 + 7) % P, (P + 1) // 4, P)
    if (y & 1) != (b[0] & 1):
        y = P - y
    assert (y * y - x ** 3 - 7) % P == 0
    return (x, y)


def pub(secret):
    return ser(pmul(int.from_bytes(secret, "big") if isinstance(secret, bytes) else secret))


sha256 = lambda b: hashlib.sha256(b).digest()
sha256d = lambda b: sha256(sha256(b))
hmac256 = lambda k, m: hmac.new(k, m, hashlib.sha256).digest()


def ripemd160(b):
    try:
        return hashlib.new("ripemd160", b).digest()
    except ValueError:
        return _ripemd160(b)


def hash160(b):
    return ripemd160(sha256(b))


def _ripemd160(data):          # RFC-style RIPEMD-160 for interpreters whose OpenSSL has no legacy provider
    rol = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    r1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8, 3, 10, 14, 4, 9, 15, 8, 1, 2, 7, 0, 6, 13, 11, 5, 12, 1, 9, 11, 10, 0, 8, 12, 4, 13, 3, 7, 15, 14, 5, 6, 2, 4, 0, 5, 9, 7, 12, 2, 10, 14, 1, 3, 8, 11, 6, 15, 13]
    r2 = [5, 14, 7, 0, 9, 2, 11, 4, 13, 6, 15, 8, 1, 10, 3, 12, 6, 11, 3, 7, 0, 13, 5, 10, 14, 15, 8, 12, 4, 9, 1, 2, 15, 5, 1, 3, 7, 14, 6, 9, 11, 8, 12, 2, 10, 0, 4, 13, 8, 6, 4, 1, 3, 11, 15, 0, 5, 12, 2, 13, 9, 7, 10, 14, 12, 15, 10, 4, 1, 5, 8, 7, 6, 2, 13, 14, 0, 3, 9, 11]
    s1 = [11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8, 7, 6, 8, 13, 11, 9, 7, 15, 7, 12, 15, 9, 11, 7, 13, 12, 11, 13, 6, 7, 14, 9, 13, 15, 14, 8, 13, 6, 5, 12, 7, 5, 11, 12, 14, 15, 14, 15, 9, 8, 9, 14, 5, 6, 8, 6, 5, 12, 9, 15, 5, 11, 6, 8, 13, 12, 5, 12, 13, 14, 11, 8, 5, 6]
    s2 = [8, 9, 9, 11, 13, 15, 15, 5, 7, 7, 8, 11, 14, 14, 12, 6, 9, 13, 15, 7, 12, 8, 9, 11, 7, 7, 12, 7, 6, 15, 13, 11, 9, 7, 15, 11, 8, 6, 6, 14, 12, 13, 5, 14, 13, 13, 7, 5, 15, 5, 8, 11, 14, 14, 6, 14, 6, 9, 12, 9, 12, 5, 15, 8, 8, 5, 12, 9, 12, 5, 14, 6, 8, 13, 6, 5, 15, 13, 11, 11]
    K1 = [0, 0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xA953FD4E]
    K2 = [0x50A28BE6, 0x5C4DD124, 0x6D703EF3, 0x7A6D76E9, 0]
    f = [lambda x, y, z: x ^ y ^ z, lambda x, y, z: (x & y) | (~x & z), lambda x, y, z: (x | ~y) ^ z, lambda x, y, z: (x & z) | (y & ~z), lambda x, y, z: x ^ (y | ~z)]
    m = bytearray(data) + b"\x80"
    while len(m) % 64 != 56:
        m += b"\0"
    m += struct.pack("<Q", len(data) * 8)
    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    for off in range(0, len(m), 64):
        X = struct.unpack("<16I", m[off:off + 64])
        a1, b1, c1, d1, e1 = h
        a2, b2, c2, d2, e2 = h
        for j in range(80):
            rnd = j // 16
            t = (rol((a1 + f[rnd](b1, c1, d1) + X[r1[j]] + K1[rnd]) & 0xFFFFFFFF, s1[j]) + e1) & 0xFFFFFFFF
            a1, e1, d1, c1, b1 = e1, d1, rol(c1, 10), b1, t
            t = (rol((a2 + f[4 - rnd](b2, c2, d2) + X[r2[j]] + K2[rnd]) & 0xFFFFFFFF, s2[j]) + e2) & 0xFFFFFFFF
            a2, e2, d2, c2, b2 = e2, d2, rol(c2, 10), b2, t
        t = (h[1] + c1 + d2) & 0xFFFFFFFF
        h = [t, (h[2] + d1 + e2) & 0xFFFFFFFF, (h[3] + e1 + a2) & 0xFFFFFFFF, (h[4] + a1 + b2) & 0xFFFFFFFF, (h[0] + b1 + c2) & 0xFFFFFFFF]
    return struct.pack("<5I", *h)


def tagged_hash(tag, msg):
    th = sha256(tag.encode())
    return sha256(th + th + msg)


# ------------------------------------------------------------------------------------------------ ECDSA (RFC 6979, low S)
def rfc6979(secret, digest):
    x = secret.to_bytes(32, "big")
    h1 = digest
    v = b"\x01" * 32
    k = b"\x00" * 32
    k = hmac256(k, v + b"\x00" + x + h1)
    v = hmac256(k, v)
    k = hmac256(k, v + b"\x01" + x + h1)
    v = hmac256(k, v)
    while True:
        v = hmac256(k, v)
        c = int.from_bytes(v, "big")
        if 1 <= c < N:
            return c
        k = hmac256(k, v + b"\x00")
        v = hmac256(k, v)


def _der_int(i):
    b = i.to_bytes((i.bit_length() + 7) // 8 or 1, "big")
    if b[0] & 0x80:
        b = b"\x00" + b
    return b"\x02" + bytes([len(b)]) + b


def sign(secret, digest):
    """DER signature, low S, deterministic (RFC 6979 with SHA-256)"""
    d = secret if isinstance(secret, int) else int.from_bytes(secret, "big")
    k = rfc6979(d, digest)
    r = pmul(k)[0] % N
    s = pow(k, -1, N) * (int.from_bytes(digest, "big") + r * d) % N
    if s > N // 2:
        s = N - s
    body = _der_int(r) + _der_int(s)
    return b"\x30" + bytes([len(body)]) + body


def verify(pt, digest, der):
    r_len = der[3]
    r = int.from_bytes(der[4:4 + r_len], "big")
    s = int.from_bytes(der[6 + r_len:6 + r_len + der[5 + r_len]], "big")
    w = pow(s, -1, N)
    u1, u2 = int.from_bytes(digest, "big") * w % N, r * w % N
    q = padd(pmul(u1), pmul(u2, pt))
    return q is not None and q[0] % N == r


# ------------------------------------------------------------------------------------------------ ChaCha20, Poly1305, AEAD (RFC 8439)
def _qr(s, a, b, c, d):
    r = lambda x, n: ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF; s[d] = r(s[d] ^ s[a], 16)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF; s[b] = r(s[b] ^ s[c], 12)
    s[a] = (s[a] + s[b]) & 0xFFFFFFFF; s[d] = r(s[d] ^ s[a], 8)
    s[c] = (s[c] + s[d]) & 0xFFFFFFFF; s[b] = r(s[b] ^ s[c], 7)


def chacha20_block(key, counter, nonce):
    st = list(struct.unpack("<4I", b"expand 32-byte k")) + list(struct.unpack("<8I", key)) + [counter & 0xFFFFFFFF] + list(struct.unpack("<3I", nonce))
    w = st[:]
    for _ in range(10):
        _qr(w, 0, 4, 8, 12); _qr(w, 1, 5, 9, 13); _qr(w, 2, 6, 10, 14); _qr(w, 3, 7, 11, 15)
        _qr(w, 0, 5, 10, 15); _qr(w, 1, 6, 11, 12); _qr(w, 2, 7, 8, 13); _qr(w, 3, 4, 9, 14)
    return struct.pack("<16I", *[(w[i] + st[i]) & 0xFFFFFFFF for i in range(16)])


def chacha20_stream(key, nonce, n, counter=0):
    out = b""
    while len(out) < n:
        out += chacha20_block(key, counter, nonce)
        counter += 1
    return out[:n]


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def poly1305(key, msg):
    r = int.from_bytes(key[:16], "little") & 0x0ffffffc0ffffffc0ffffffc0fffffff
    s = int.from_bytes(key[16:], "little")
    acc = 0
    for i in range(0, len(msg), 16):
        blk = msg[i:i + 16]
        acc = (acc + int.from_bytes(blk + b"\x01", "little")) * r % (2 ** 130 - 5)
    return ((acc + s) % 2 ** 128).to_bytes(16, "little")


def _pad16(b):
    return b + b"\0" * (-len(b) % 16)


def aead_encrypt(key, nonce, aad, pt):
    otk = chacha20_block(key, 0, nonce)[:32]
    ct = xor(pt, chacha20_stream(key, nonce, len(pt), 1))
    tag = poly1305(otk, _pad16(aad) + _pad16(ct) + struct.pack("<QQ", len(aad), len(ct)))
    return ct + tag


def aead_decrypt(key, nonce, aad, ct_tag):
    ct, tag = ct_tag[:-16], ct_tag[-16:]
    otk = chacha20_block(key, 0, nonce)[:32]
    if poly1305(otk, _pad16(aad) + _pad16(ct) + struct.pack("<QQ", len(aad), len(ct))) != tag:
        raise ValueError("bad tag")
    return xor(ct, chacha20_stream(key, nonce, len(ct), 1))


def hkdf2(salt, ikm):
    prk = hmac256(salt, ikm)
    t1 = hmac256(prk, b"\x01")
    t2 = hmac256(prk, t1 + b"\x02")
    return t1, t2


# ------------------------------------------------------------------------------------------------ BOLT 8: Noise_XK_secp256k1_ChaChaPoly_SHA256
def ecdh(priv, pubkey):
    """BOLT 8: the SHA-256 of the compressed shared point, not its x coordinate"""
    return sha256(ser(pmul(int.from_bytes(priv, "big") if isinstance(priv, bytes) else priv, parse(pubkey))))


def _nonce(n):
    return b"\0" * 4 + struct.pack("<Q", n)


def noise_initiator(ls_priv, e_priv, rs_pub, act2):
    """The initiator side of the handshake with fixed ephemeral key (test vectors): returns act one, act three, (sk, rk), and the handshake values"""
    proto = b"Noise_XK_secp256k1_ChaChaPoly_SHA256"
    h = sha256(proto)
    ck = h
    h = sha256(h + b"lightning")
    h = sha256(h + rs_pub)
    e_pub = pub(e_priv)
    h = sha256(h + e_pub)
    es = ecdh(e_priv, rs_pub)
    ck, k1 = hkdf2(ck, es)
    c = aead_encrypt(k1, _nonce(0), h, b"")
    h = sha256(h + c)
    act1 = b"\x00" + e_pub + c
    assert act2[0] == 0
    re, c2 = act2[1:34], act2[34:50]
    h = sha256(h + re)
    ee = ecdh(e_priv, re)
    ck, k2 = hkdf2(ck, ee)
    aead_decrypt(k2, _nonce(0), h, c2)
    h = sha256(h + c2)
    ls_pub = pub(ls_priv)
    c3 = aead_encrypt(k2, _nonce(1), h, ls_pub)
    h = sha256(h + c3)
    se = ecdh(ls_priv, re)
    ck, k3 = hkdf2(ck, se)
    t = aead_encrypt(k3, _nonce(0), h, b"")
    sk, rk = hkdf2(ck, b"")
    return {"act1": act1, "act3": b"\x00" + c3 + t, "sk": sk, "rk": rk, "ck": ck}


def transport_message(sk, ck, n, msg):
    """BOLT 8 message encryption: a 2-byte length (encrypted, 16-byte tag) and the body (encrypted, 16-byte tag); the key rotates every 1000 nonces. Returns the bytes and the new (sk, ck, n)."""
    out = b""
    ln = struct.pack(">H", len(msg))
    for part in (ln, msg):
        out += aead_encrypt(sk, _nonce(n), b"", part)
        n += 1
        if n == 1000:
            ck, sk = hkdf2(ck, sk)
            n = 0
    return out, sk, ck, n


# ------------------------------------------------------------------------------------------------ BOLT 4: Sphinx onion packet
def _gen_key(name, secret):
    return hmac256(name.encode(), secret)


def sphinx_packet(session_key, hops, assoc):
    """hops: list of (pubkey bytes, payload bytes including its length prefix). Returns the 1366-byte onion packet of BOLT 4 (version 0)."""
    ROUTING = 1300
    n = len(hops)
    ephem = int.from_bytes(session_key, "big")
    secrets, pubs = [], []
    for pk, _ in hops:
        e_pub = ser(pmul(ephem))
        ss = ecdh(ephem, pk)
        secrets.append(ss)
        pubs.append(e_pub)
        ephem = ephem * int.from_bytes(sha256(e_pub + ss), "big") % N
    filler = b""
    for i in range(n - 1):
        shift = len(hops[i][1]) + 32
        stream = chacha20_stream(_gen_key("rho", secrets[i]), b"\0" * 12, 2 * ROUTING)
        filler = xor(filler + b"\0" * shift, stream[ROUTING - len(filler):ROUTING + shift])
    routing = chacha20_stream(_gen_key("pad", session_key), b"\0" * 12, ROUTING)
    hmac_next = b"\0" * 32
    for i in range(n - 1, -1, -1):
        payload = hops[i][1]
        routing = (payload + hmac_next + routing)[:ROUTING]
        routing = xor(routing, chacha20_stream(_gen_key("rho", secrets[i]), b"\0" * 12, ROUTING))
        if i == n - 1:
            routing = routing[:ROUTING - len(filler)] + filler
        hmac_next = hmac256(_gen_key("mu", secrets[i]), routing + assoc)
    return b"\x00" + pubs[0] + routing + hmac_next


# ------------------------------------------------------------------------------------------------ BOLT 3: keys and secrets
def flip_bit(b, k):
    ba = bytearray(b)
    ba[k // 8] ^= 1 << (k % 8)
    return bytes(ba)


def shachain(seed, index):
    """generate_from_seed of BOLT 3: the per-commitment secret of the given index"""
    p = seed
    for bit in range(47, -1, -1):
        if (index >> bit) & 1:
            p = sha256(flip_bit(p, bit))
    return p


def pubkey_from_basepoint(basepoint, per_commitment_point):
    """BOLT 3: localpubkey = basepoint + SHA256(per_commitment_point || basepoint) * G"""
    t = int.from_bytes(sha256(per_commitment_point + basepoint), "big")
    return ser(padd(parse(basepoint), pmul(t)))


def revocation_pubkey(revocation_basepoint, per_commitment_point):
    a = int.from_bytes(sha256(revocation_basepoint + per_commitment_point), "big")
    b = int.from_bytes(sha256(per_commitment_point + revocation_basepoint), "big")
    return ser(padd(pmul(a, parse(revocation_basepoint)), pmul(b, parse(per_commitment_point))))


def revocation_privkey(base_secret, per_commitment_secret):
    bp = pub(base_secret)
    pcp = pub(per_commitment_secret)
    a = int.from_bytes(sha256(bp + pcp), "big")
    b = int.from_bytes(sha256(pcp + bp), "big")
    return ((int.from_bytes(base_secret, "big") * a + int.from_bytes(per_commitment_secret, "big") * b) % N).to_bytes(32, "big")


# ------------------------------------------------------------------------------------------------ bech32 (BIP 173) without the length limit
B32 = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"


def _polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5):
            chk ^= gen[i] if (b >> i) & 1 else 0
    return chk


def bech32_decode(s):
    """returns (hrp, 5-bit data without the checksum) or None when the checksum is wrong"""
    s = s.lower()
    pos = s.rfind("1")
    hrp, data = s[:pos], [B32.index(c) for c in s[pos + 1:]]
    if _polymod([ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp] + data) != 1:
        return None
    return hrp, data[:-6]


def convertbits(data, frm, to, pad=True):
    acc, bits, out = 0, 0, []
    for v in data:
        acc = (acc << frm) | v
        bits += frm
        while bits >= to:
            bits -= to
            out.append((acc >> bits) & ((1 << to) - 1))
    if pad and bits:
        out.append((acc << (to - bits)) & ((1 << to) - 1))
    return out


def bolt11(s):
    """Parse a BOLT 11 invoice: human-readable part, amount in millisatoshi (or None), timestamp, tagged fields {p: payment hash, s: payment secret, d: description, x: expiry, c: min final cltv, ...}, signature (65 bytes)"""
    d = bech32_decode(s)
    if d is None:
        return None
    hrp, data = d
    sig5, body = data[-104:], data[:-104]
    sig = bytes(convertbits(sig5, 5, 8, False))
    ts = 0
    for v in body[:7]:
        ts = ts * 32 + v
    fields, i = {}, 7
    while i < len(body):
        t, ln = B32[body[i]], body[i + 1] * 32 + body[i + 2]
        raw = body[i + 3:i + 3 + ln]
        fields.setdefault(t, []).append(raw)
        i += 3 + ln
    mm = re.match(r"^ln(bcrt|bc|tbs|tb|sb)(\d+)?([munp])?$", hrp)
    msat = None
    if mm and mm.group(2):
        mult = {None: 10 ** 11, "m": 10 ** 8, "u": 10 ** 5, "n": 10 ** 2, "p": 0.1}[mm.group(3)]      # 1 BTC = 10^11 msat
        msat = int(int(mm.group(2)) * mult)
    return {"hrp": hrp, "msat": msat, "timestamp": ts, "fields": fields, "sig": sig}


def field_int(raw):
    v = 0
    for x in raw:
        v = v * 32 + x
    return v


def field_bytes(raw):
    return bytes(convertbits(raw, 5, 8, False))
