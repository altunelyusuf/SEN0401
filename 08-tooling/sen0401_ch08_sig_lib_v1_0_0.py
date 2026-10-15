#!/usr/bin/env python3
"""Signature library for chapter 8 (Digital Signatures) of Mastering Bitcoin, 3rd edition - version 1.0.0.

Standard library only (hashlib, hmac, struct, json, os). The curve arithmetic, the ECDSA and BIP340 signers, the legacy, BIP143 and BIP341
signature hashes and the transaction parser are those of sen0401_ch07_script_lib_v1_0_0 (which sen0401_ch07_verify_v1_0_0.py checks against Bitcoin
Core's own test data); this file adds what only chapter 8 needs, each piece written from the text of the chapter or of the proposal it names:
  * the toy integer protocol of the book's sidebar, the interactive Schnorr identity protocol on secp256k1, the Fiat-Shamir signature in the chapter's
    simplified form (full point R), the impersonation that follows from giving the challenge before the nonce, the scalar-versus-field modulus check;
  * ECDSA with the book's two formulas written out (signing with an explicit nonce, verification as a point K), nonce reuse and the private key it gives away,
    RFC 6979 for any group order (checked against the RFC's own appendix), strict DER of BIP66 as Bitcoin Core's IsValidSignatureEncoding reads it;
  * the naive scriptless multisignature of the chapter, the key cancellation attack, Shamir secret sharing, the chapter's 2-of-3 scriptless threshold
    protocol and the manipulation attack;
  * counting the bytes hashed per signature check by the legacy algorithm and by BIP143, and finding which fields of a transaction each SIGHASH type commits to.
Every function is pure; nothing here reads the network. ev(name) resolves a file saved in 08-tooling/ch08-evidence, wherever the caller's working directory is."""
__version__ = "1.0.0"
import hashlib, hmac, json, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sen0401_ch07_script_lib_v1_0_0 as L

P, N, G = L.P, L.N, L.G
EVDIR = os.path.join(HERE, "ch08-evidence")
point_mul, point_add, lift_x = L.point_mul, L.point_add, L.lift_x


def ev(name):
    """absolute path of a saved evidence file"""
    return os.path.join(EVDIR, name)


def evtext(name):
    return open(ev(name), encoding="utf-8", errors="replace").read()


def norm(s):
    """whitespace-normalised text, as the passage checks compare it"""
    return " ".join(s.split())


def has(name, *pieces):
    """True when every piece occurs, whitespace-normalised, in the saved copy"""
    t = norm(evtext(name))
    return all(norm(p) in t for p in pieces)


def neg(pt):
    return None if pt is None else (pt[0], (P - pt[1]) % P)


def sub(a, b):
    return point_add(a, neg(b))


def h256int(*parts):
    return int.from_bytes(hashlib.sha256(b"".join(parts)).digest(), "big")


def b32(n):
    return n.to_bytes(32, "big")


# ----------------------------------------------------------------------------------------------------------------------
# the toy protocol of the sidebar "Schnorr Identity Protocol with Integers Instead of Points"
# ----------------------------------------------------------------------------------------------------------------------
def toy_protocol(x=3, G_=5, k=7, e=11):
    xG = x * G_; kG = k * G_
    s = k + e * x
    return {"xG": xG, "kG": kG, "s": s, "sG": s * G_, "exG": e * xG, "holds": s * G_ == kG + e * xG,
            "divide_back": xG // G_}                         # with plain integers anybody can divide by G and read the private key


# ----------------------------------------------------------------------------------------------------------------------
# the interactive identity protocol on secp256k1 (points), then the Fiat-Shamir signature in the chapter's simplified form
# ----------------------------------------------------------------------------------------------------------------------
def identity_round(x, k, e):
    X = point_mul(x); K = point_mul(k)
    s = (k + e * x) % N
    return point_mul(s) == point_add(K, point_mul(e, X)), s


def fs_sign(x, m, k):
    """the chapter's simplified signature: R = kG (full point), e = hash(R || X || m), s = k + e x (mod n)"""
    X = point_mul(x); R = point_mul(k)
    e = h256int(L.pubkey_serialize(R), L.pubkey_serialize(X), m) % N
    return R, (k + e * x) % N


def fs_verify(X, m, sig):
    R, s = sig
    e = h256int(L.pubkey_serialize(R), L.pubkey_serialize(X), m) % N
    return point_mul(s) == point_add(R, point_mul(e, X))


def impersonate_with_known_challenge(X, e, s_choice=123456789):
    """a cheat who is told the challenge e BEFORE committing to a nonce picks s, sets R = sG - eX and passes the check without knowing x"""
    R = sub(point_mul(s_choice), point_mul(e, X))
    return R, s_choice, point_mul(s_choice) == point_add(R, point_mul(e, X))


def modulus_check(x=0xC0FFEE, k=0xBADA55, e=0x1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890ABCDEF):
    """the book writes that operations are performed modulus p; the scalar s = k + e x lives modulo the curve order n. Returns whether the equation
    sG = kG + eX holds when s is reduced modulo n (it does) and when it is reduced modulo p (it does not, as p is not the group order)"""
    X = point_mul(x); K = point_mul(k)
    s_n = (k + e * x) % N; s_p = (k + e * x) % P
    return point_mul(s_n) == point_add(K, point_mul(e, X)), point_mul(s_p) == point_add(K, point_mul(e, X)), P != N


def linearity(x=11, y=22, z=33, a=44):
    """additivity f(x+y+z) = f(x)+f(y)+f(z) and homogeneity f(a*x) = a*f(x), with f(v) = v*G"""
    add = point_mul(x + y + z) == point_add(point_add(point_mul(x), point_mul(y)), point_mul(z))
    hom = point_mul(a * x) == point_mul(a, point_mul(x))
    return add, hom


# ----------------------------------------------------------------------------------------------------------------------
# BIP340 pieces used by the chapter's "serialization" paragraph
# ----------------------------------------------------------------------------------------------------------------------
def bip340_vectors():
    import csv
    return list(csv.DictReader(open(ev("bip-0340_test-vectors.csv"), encoding="utf-8")))


def bip340_sign_size(hashtype=0):
    sk = 0x3b78ce563f89a0ed9414f5aa28ad0d96d6795f9c63
    msg = hashlib.sha256(b"ch08").digest()
    sig = L.schnorr_sign(sk, msg) + (bytes([hashtype]) if hashtype else b"")
    return len(sig), L.schnorr_verify(L.schnorr_pubkey(sk), msg, sig[:64])


# ----------------------------------------------------------------------------------------------------------------------
# ECDSA, written as the chapter writes it
# ----------------------------------------------------------------------------------------------------------------------
def ecdsa_sign_k(x, m_hash, k):
    """s = k^-1 (Hash(m) + x R) mod n, R the x coordinate of K = kG; returns (R, s) without normalising s"""
    K = point_mul(k); R = K[0] % N
    s = pow(k, -1, N) * (m_hash + R * x) % N
    return R, s


def ecdsa_verify_K(X, m_hash, R, s):
    """K = s^-1 Hash(m) G + s^-1 R X; the signature is valid when the x coordinate of K equals R"""
    w = pow(s, -1, N)
    K = point_add(point_mul(w * m_hash % N), point_mul(w * R % N, X))
    return K is not None and K[0] % N == R


def recover_key_from_reused_nonce(r, s1, h1, s2, h2):
    """two signatures with the same nonce k (same R): k = (h1 - h2)/(s1 - s2), x = (s1 k - h1)/R"""
    k = (h1 - h2) * pow(s1 - s2, -1, N) % N
    return (s1 * k - h1) * pow(r, -1, N) % N, k


def rfc6979_k(q, x, h1, hashfn=hashlib.sha256):
    """RFC 6979 section 3.2 for a group of order q and the hash hashfn (steps a to h; the first candidate in range)"""
    qlen = q.bit_length(); rlen = (qlen + 7) // 8; hlen = hashfn().digest_size
    def bits2int(b):
        v = int.from_bytes(b, "big"); bl = 8 * len(b)
        return v >> (bl - qlen) if bl > qlen else v
    def int2octets(v): return v.to_bytes(rlen, "big")
    def bits2octets(b):
        z1 = bits2int(b); z2 = z1 - q
        return int2octets(z1 if z2 < 0 else z2)
    V = b"\x01" * hlen; K = b"\x00" * hlen
    K = hmac.new(K, V + b"\x00" + int2octets(x) + bits2octets(h1), hashfn).digest(); V = hmac.new(K, V, hashfn).digest()
    K = hmac.new(K, V + b"\x01" + int2octets(x) + bits2octets(h1), hashfn).digest(); V = hmac.new(K, V, hashfn).digest()
    while True:
        T = b""
        while len(T) * 8 < qlen:
            V = hmac.new(K, V, hashfn).digest(); T += V
        k = bits2int(T)
        if 1 <= k < q: return k
        K = hmac.new(K, V + b"\x00", hashfn).digest(); V = hmac.new(K, V, hashfn).digest()


# NIST P-256, the curve of the RFC 6979 appendix A.2.5 vectors (used only to check rfc6979_k against the RFC)
P256_Q = 0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551


def der_strict_ok(sig):
    """Bitcoin Core's IsValidSignatureEncoding (BIP66) over signature || hashtype byte, ported line by line from src/script/interpreter.cpp"""
    s = bytes(sig)
    if len(s) < 9 or len(s) > 73: return False
    if s[0] != 0x30: return False
    if s[1] != len(s) - 3: return False
    lenR = s[3]
    if 5 + lenR >= len(s): return False
    lenS = s[5 + lenR]
    if lenR + lenS + 7 != len(s): return False
    if s[2] != 0x02: return False
    if lenR == 0: return False
    if s[4] & 0x80: return False
    if lenR > 1 and s[4] == 0x00 and not (s[5] & 0x80): return False
    if s[lenR + 4] != 0x02: return False
    if lenS == 0: return False
    if s[lenR + 6] & 0x80: return False
    if lenS > 1 and s[lenR + 6] == 0x00 and not (s[lenR + 7] & 0x80): return False
    return True


def der_fields(sig_with_hashtype):
    """the nine elements the chapter lists, as (name, hex) pairs"""
    s = bytes(sig_with_hashtype)
    lr = s[3]; ls = s[5 + lr]
    return [("0x30 sequence", "%02x" % s[0]), ("sequence length", "%02x" % s[1]), ("0x02 integer", "%02x" % s[2]), ("R length", "%02x" % s[3]),
            ("R", s[4:4 + lr].hex()), ("0x02 integer", "%02x" % s[4 + lr]), ("S length", "%02x" % s[5 + lr]), ("S", s[6 + lr:6 + lr + ls].hex()),
            ("hash type", "%02x" % s[-1])]


# ----------------------------------------------------------------------------------------------------------------------
# multisignature, naive (the chapter's protocol with its warning) and the key cancellation attack
# ----------------------------------------------------------------------------------------------------------------------
def naive_multisig(y, z, a, b, m):
    Y = point_mul(y); Z = point_mul(z); X = point_add(Y, Z)
    A = point_mul(a); B = point_mul(b); K = point_add(A, B)
    e = h256int(L.pubkey_serialize(K), L.pubkey_serialize(X), m) % N
    q = (a + e * y) % N; r = (b + e * z) % N; s = (q + r) % N
    return fs_verify(X, m, (K, s)), X


def key_cancellation(y, z, b, m):
    """Alice publishes yG honestly; Bob, who has seen it, publishes zG - yG. The aggregate is zG, so Bob alone signs for 'both'"""
    Y = point_mul(y); Zb = sub(point_mul(z), Y)
    X = point_add(Y, Zb)                                       # = zG
    K = point_mul(b)
    e = h256int(L.pubkey_serialize(K), L.pubkey_serialize(X), m) % N
    s = (b + e * z) % N
    return X == point_mul(z), fs_verify(X, m, (K, s))


# ----------------------------------------------------------------------------------------------------------------------
# Shamir secret sharing and the chapter's 2-of-3 scriptless threshold protocol
# ----------------------------------------------------------------------------------------------------------------------
def shamir_split(secret, t, xs, coeffs):
    """polynomial of degree t-1 with constant term secret and the given higher coefficients; shares are (x, f(x)) mod n"""
    assert len(coeffs) == t - 1
    return [(x, (secret + sum(c * pow(x, i + 1, N) for i, c in enumerate(coeffs))) % N) for x in xs]


def shamir_combine(shares):
    """Lagrange interpolation at 0 modulo n"""
    total = 0
    for i, (xi, yi) in enumerate(shares):
        num = den = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                num = num * (-xj) % N; den = den * (xi - xj) % N
        total = (total + yi * num * pow(den, -1, N)) % N
    return total


def threshold_demo(dA=1001, dB=2002, dC=3003, cA=77, cB=88, cC=99, m=b"spend"):
    """Alice, Bob and Carol each hold a partial private key; each splits it with a degree-1 polynomial and gives one share to each of the others.
    Alice and Bob rebuild Carol's partial key from the two shares they hold and sign as if all three had; the signature verifies for the aggregate key.
    Returns (rebuilt equals Carol's key, signature verifies, signature verifies with the key 'dA+dB+dC')"""
    xs = {"A": 1, "B": 2, "C": 3}
    sh = {n: dict(zip(("A", "B", "C"), shamir_split(d, 2, [1, 2, 3], [c]))) for n, d, c in (("A", dA, cA), ("B", dB, cB), ("C", dC, cC))}
    rebuilt = shamir_combine([sh["C"]["A"], sh["C"]["B"]])
    X = point_add(point_add(point_mul(dA), point_mul(dB)), point_mul(dC))
    a, b = 0x1111, 0x2222; c = 0x3333                           # nonces of the three, Carol's nonce is not needed once her key is rebuilt: they pick a nonce for her too
    K = point_add(point_add(point_mul(a), point_mul(b)), point_mul(c))
    e = h256int(L.pubkey_serialize(K), L.pubkey_serialize(X), m) % N
    s = ((a + e * dA) + (b + e * dB) + (c + e * rebuilt)) % N
    return rebuilt == dC, fs_verify(X, m, (K, s)), X == point_mul((dA + dB + dC) % N)


def manipulation_attack(dA=1001, dB=2002, dC=3003, cA=77, cB=88, cC=99):
    """Bob tells Alice that Carol is unavailable (they rebuild dC), then tells Carol that Alice is unavailable (they rebuild dA). Bob now holds all three"""
    sh = {n: dict(zip(("A", "B", "C"), shamir_split(d, 2, [1, 2, 3], [c]))) for n, d, c in (("A", dA, cA), ("B", dB, cB), ("C", dC, cC))}
    got_dC = shamir_combine([sh["C"]["A"], sh["C"]["B"]])          # Alice's share of Carol's polynomial and Bob's
    got_dA = shamir_combine([sh["A"]["B"], sh["A"]["C"]])          # Bob's share of Alice's polynomial and Carol's
    return got_dC == dC, got_dA == dA, (got_dA + dB + got_dC) % N == (dA + dB + dC) % N


def shares_alone_reveal_nothing(secret=424242, c1=555, c2=666):
    """a single share of a 2-of-3 degree-1 sharing is consistent with every possible secret"""
    s = shamir_split(secret, 2, [1], [c1])[0]
    other = 999999
    c_other = (s[1] - other) * pow(1, -1, N) % N               # the coefficient that would make 'other' the secret with the same share at x = 1
    return shamir_split(other, 2, [1], [c_other])[0] == s


# ----------------------------------------------------------------------------------------------------------------------
# what each SIGHASH type commits to, found by changing one field at a time
# ----------------------------------------------------------------------------------------------------------------------
def _sample_tx():
    ins = [(bytes([i + 1]) * 32, i, b"", 0xfffffffe) for i in range(3)]
    outs = [(1000 * (j + 1), b"\x00\x14" + bytes([j]) * 20) for j in range(3)]
    return L.Tx(2, ins, outs, 0)


def sighash_commitments(hashtype, nin=1):
    """which fields change the legacy signature hash of input nin: other inputs' outpoints, other inputs' sequences, the output at the same index, the other outputs"""
    base = L.sighash_legacy(b"\x51", _sample_tx(), nin, hashtype)
    def changed(mod):
        t = _sample_tx(); mod(t)
        return L.sighash_legacy(b"\x51", t, nin, hashtype) != base
    def other_in(t): t.vin[2] = (b"\xee" * 32, 9, b"", t.vin[2][3])
    def other_seq(t): t.vin[2] = (t.vin[2][0], t.vin[2][1], b"", 1)
    def same_out(t): t.vout[nin] = (t.vout[nin][0] + 1, t.vout[nin][1])
    def other_out(t): t.vout[2] = (t.vout[2][0] + 1, t.vout[2][1])
    def own_seq(t): t.vin[nin] = (t.vin[nin][0], t.vin[nin][1], b"", 1)
    return {"other input outpoint": changed(other_in), "other input sequence": changed(other_seq), "output with the same index": changed(same_out),
            "other outputs": changed(other_out), "own sequence": changed(own_seq)}


def sighash_single_bug():
    """SIGHASH_SINGLE on an input whose index has no output returns the number one (Core's comment: 'the bug')"""
    t = _sample_tx(); t.vout = t.vout[:1]
    return L.sighash_legacy(b"\x51", t, 2, 3).hex()


# ----------------------------------------------------------------------------------------------------------------------
# the cost of hashing: bytes passed to SHA-256 per signature check
# ----------------------------------------------------------------------------------------------------------------------
def make_tx(n_in, n_out=1, script_len=0):
    ins = [(hashlib.sha256(b"in%d" % i).digest(), 0, b"\x00" * script_len, 0xffffffff) for i in range(n_in)]
    outs = [(1000, b"\x76\xa9\x14" + b"\x11" * 20 + b"\x88\xac") for _ in range(n_out)]
    return L.Tx(1, ins, outs, 0)


def legacy_bytes_hashed(tx):
    """total bytes entering SHA-256 when every input is signed with SIGHASH_ALL by the original algorithm: one full serialization per input"""
    total = 0
    for i in range(len(tx.vin)):
        sc = b"\x76\xa9\x14" + b"\x22" * 20 + b"\x88\xac"
        out = struct.pack("<i", tx.version) + L.cs_encode(len(tx.vin))
        for j, (h, n, _, seq) in enumerate(tx.vin):
            out += h + struct.pack("<I", n) + (L.cs_encode(len(sc)) + sc if i == j else b"\x00") + struct.pack("<I", seq)
        out += L.cs_encode(len(tx.vout)) + b"".join(struct.pack("<q", v) + L.cs_encode(len(s)) + s for v, s in tx.vout)
        out += struct.pack("<I", tx.locktime) + struct.pack("<I", 1)
        total += len(out) * 1 + 32                                  # double SHA-256: the second pass hashes 32 bytes
    return total


def bip143_bytes_hashed(tx):
    """the same count for BIP143: hashPrevouts, hashSequence and hashOutputs once, then a fixed-size-plus-script preimage per input"""
    sc = b"\x19\x76\xa9\x14" + b"\x22" * 20 + b"\x88\xac"
    once = len(b"".join(h + struct.pack("<I", n) for h, n, _, _ in tx.vin)) + 32 + len(b"".join(struct.pack("<I", s) for *_, s in tx.vin)) + 32 + \
        len(b"".join(struct.pack("<q", v) + L.cs_encode(len(s)) + s for v, s in tx.vout)) + 32
    per_input = 4 + 32 + 32 + 36 + len(sc) + 8 + 4 + 32 + 4 + 4 + 32
    return once + per_input * len(tx.vin)


# ----------------------------------------------------------------------------------------------------------------------
# Bitcoin Core's own data: sighash.json at the pinned commit
# ----------------------------------------------------------------------------------------------------------------------
def sighash_json_check():
    rows = [r for r in json.load(open(ev("core_src_test_data_sighash.json"))) if len(r) == 5]
    ok = 0; kinds = {}
    for raw, script, nin, ht, want in rows:
        tx = L.parse_tx(raw)
        got = L.sighash_legacy(bytes.fromhex(script), tx, nin, ht & 0xffffffff)[::-1].hex()
        ok += got == want
        k = ht & 0x1f if (ht & 0x1f) in (1, 2, 3) else 0
        kinds[(k, bool(ht & 0x80))] = kinds.get((k, bool(ht & 0x80)), 0) + 1
    return ok, len(rows), len(kinds)


# ----------------------------------------------------------------------------------------------------------------------
# key prefixing: the related-key attack that BIP340 prevents by hashing the public key into the challenge
# ----------------------------------------------------------------------------------------------------------------------
def related_key_attack(x=0xABCDEF, k=0x13579B, a=0x2468AC, m=b"pay", prefixed=False):
    """Schnorr without key prefixing (e = hash(R || m)): from a valid (R, s) for P anybody makes (R, s + a e) valid for P + aG, which is the key BIP32 derives for tweak a.
    With key prefixing (e = hash(R || P || m)) the same transformation fails. Returns whether the forged signature verifies"""
    P_ = point_mul(x); R = point_mul(k)
    def chal(Pt): return h256int(L.pubkey_serialize(R), *( [L.pubkey_serialize(Pt)] if prefixed else []), m) % N
    s = (k + chal(P_) * x) % N
    P2 = point_add(P_, point_mul(a))
    s2 = (s + a * chal(P_)) % N                                  # what the attacker can compute from public data only
    return point_mul(s2) == point_add(R, point_mul(chal(P2), P2))


# ----------------------------------------------------------------------------------------------------------------------
# batch verification: one combined equation for many BIP340 signatures (random linear combination)
# ----------------------------------------------------------------------------------------------------------------------
def bip340_batch_verify(items, seed=b"batch"):
    """items: [(pub32, msg32, sig64)]. Checks sum(a_i (s_i G - R_i - e_i P_i)) == 0 with a_1 = 1 and the other a_i derived by hashing; True or False"""
    acc = None; first = True
    for i, (pub, msg, sig) in enumerate(items):
        P_ = lift_x(int.from_bytes(pub, "big")); Rx = int.from_bytes(sig[:32], "big"); s = int.from_bytes(sig[32:], "big")
        R_ = lift_x(Rx)
        if P_ is None or R_ is None or s >= N: return False
        e = int.from_bytes(L.tagged_hash("BIP0340/challenge", sig[:32] + pub + msg), "big") % N
        a = 1 if first else int.from_bytes(hashlib.sha256(seed + bytes([i])).digest(), "big") % N
        first = False
        term = sub(sub(point_mul(a * s % N), point_mul(a, R_)), point_mul(a * e % N, P_))
        acc = point_add(acc, term)
    return acc is None


# ----------------------------------------------------------------------------------------------------------------------
# BIP327 key aggregation (MuSig2): Q = sum a_i P_i with a_i = hash(L || pk_i), the second distinct key weighted 1
# ----------------------------------------------------------------------------------------------------------------------
def musig2_keyagg(pks33):
    Lh = L.tagged_hash("KeyAgg list", b"".join(pks33))
    pk2 = next((p for p in pks33 if p != pks33[0]), bytes(33))
    Q = None
    for pk in pks33:
        a = 1 if pk == pk2 else int.from_bytes(L.tagged_hash("KeyAgg coefficient", Lh + pk), "big") % N
        Q = point_add(Q, point_mul(a, L.pubkey_parse(pk)))
    return Q


def keyagg_vectors():
    d = json.load(open(ev("bip-0327_key_agg_vectors.json")))
    ok = 0
    for c in d["valid_test_cases"]:
        Q = musig2_keyagg([bytes.fromhex(d["pubkeys"][i]) for i in c["key_indices"]])
        ok += Q[0].to_bytes(32, "big").hex().upper() == c["expected"]
    return ok, len(d["valid_test_cases"])


def musig2_cancellation_attempt(y=0x1111, z=0x2222):
    """Bob publishes zG - yG after seeing Alice's yG, as in the naive protocol; with BIP327's coefficients the aggregate is not zG, so Bob alone cannot sign"""
    Y = L.pubkey_create(y); Zb = L.pubkey_serialize(sub(point_mul(z), point_mul(y)))
    Q = musig2_keyagg([Y, Zb])
    return Q == point_mul(z)


if __name__ == "__main__":
    print("sen0401_ch08_sig_lib", __version__, "ok" if toy_protocol()["holds"] else "FAIL")
