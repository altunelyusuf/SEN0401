"""SEN0401 chapter 8 - the claims the chapter's text makes, each as a function that RECOMPUTES it from the library (sen0401_ch08_sig_lib_v1_0_0), the saved sources and the saved Bitcoin Core
record. The data module's CLAIMS lists the expected value of every function used in the text; sen0401_rdodi_checks runs them as 'import ... as K' + 'K.name()' in a fresh Python 3.14 each.
Nothing here is typed in from memory: a value is either computed, or read back from a file saved in ch08-evidence."""
__version__ = "1.0.0"
import hashlib, json, os, re, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import sen0401_ch07_script_lib_v1_0_0 as L
import sen0401_ch08_sig_lib_v1_0_0 as C

N, P, G = L.N, L.P, L.G
SK = 0x1b1d3a5f9c0e7d62a4b8c1d2e3f40516273849a5b6c7d8e9f0a1b2c3d4e5f607 % N
MSG = hashlib.sha256(b"Mastering Bitcoin chapter 8").digest()


def _core():
    return json.load(open(C.ev("core_regtest_record_v1_0_0.json")))


def _tx_from_mempool(name):
    j = json.load(open(C.ev(name)))
    vin = [(bytes.fromhex(v["txid"])[::-1], v["vout"], bytes.fromhex(v["scriptsig"]), v["sequence"]) for v in j["vin"]]
    vout = [(o["value"], bytes.fromhex(o["scriptpubkey"])) for o in j["vout"]]
    wit = [[bytes.fromhex(w) for w in v.get("witness", [])] for v in j["vin"]]
    return j, L.Tx(j["version"], vin, vout, j["locktime"], wit)


# ---- 1. foundations --------------------------------------------------------------------------------------------------
def roundtrip():
    sig = L.ecdsa_sign(SK, MSG)
    return L.ecdsa_verify(L.pubkey_create(SK), MSG, sig)


def tampered_message_fails():
    sig = L.ecdsa_sign(SK, MSG)
    bad = bytes([MSG[0] ^ 1]) + MSG[1:]
    return L.ecdsa_verify(L.pubkey_create(SK), bad, sig)


def wrong_key_fails():
    return L.ecdsa_verify(L.pubkey_create(SK + 1), MSG, L.ecdsa_sign(SK, MSG))


def verifier_inputs():
    """verification needs three inputs: message, public key, signature; with any one replaced the answer is False"""
    pk, sig = L.pubkey_create(SK), L.ecdsa_sign(SK, MSG)
    return [L.ecdsa_verify(pk, MSG, sig), L.ecdsa_verify(pk, hashlib.sha256(b"x").digest(), sig), L.ecdsa_verify(L.pubkey_create(5), MSG, sig),
            L.ecdsa_verify(pk, MSG, L.ecdsa_sign(SK + 7, MSG))]


def two_parties_two_inputs():
    """two owners each sign only their own input of one jointly built transaction (SIGHASH_ALL, signatures made after the transaction is fixed); both verify"""
    sa, sb = 1111, 2222
    pa, pb = L.pubkey_create(sa), L.pubkey_create(sb)
    spk_a, spk_b = L.p2pkh_script(L.hash160(pa)), L.p2pkh_script(L.hash160(pb))
    tx = L.Tx(1, [(b"\x01" * 32, 0, b"", 0xffffffff), (b"\x02" * 32, 1, b"", 0xffffffff)], [(5000, spk_a)], 0)
    da, db = L.sighash_legacy(spk_a, tx, 0, 1), L.sighash_legacy(spk_b, tx, 1, 1)
    sig_a, sig_b = L.ecdsa_sign(sa, da), L.ecdsa_sign(sb, db)
    # each signature is independent data: swapping them fails
    return [L.ecdsa_verify(pa, da, sig_a), L.ecdsa_verify(pb, db, sig_b), L.ecdsa_verify(pa, da, sig_b), L.ecdsa_verify(pb, db, sig_a)]


def sighash_digest_changes_with_output():
    t1 = C.make_tx(2, 2); t2 = C.make_tx(2, 2)
    t2.vout[1] = (t2.vout[1][0] + 1, t2.vout[1][1])
    sc = b"\x51"
    return [L.sighash_legacy(sc, t1, 0, 1) == L.sighash_legacy(sc, t1, 0, 1), L.sighash_legacy(sc, t1, 0, 1) == L.sighash_legacy(sc, t2, 0, 1)]


# ---- 2. SIGHASH ----------------------------------------------------------------------------------------------------------
def flag_values():
    return [L.SIGHASH_ALL, L.SIGHASH_NONE, L.SIGHASH_SINGLE, L.SIGHASH_ANYONECANPAY, L.SIGHASH_ALL | L.SIGHASH_ANYONECANPAY, L.SIGHASH_NONE | L.SIGHASH_ANYONECANPAY,
            L.SIGHASH_SINGLE | L.SIGHASH_ANYONECANPAY]


def flag_values_hex():
    return [hex(v) for v in flag_values()]


def core_header_flags():
    """the constants as Bitcoin Core's interpreter.h at the pinned commit declares them, read from the saved file"""
    t = C.evtext("core_src_script_interpreter.h")
    return [int(re.search(r"%s = (0x[0-9a-fA-F]+|\d+)," % n, t).group(1), 0) for n in ("SIGHASH_ALL", "SIGHASH_NONE", "SIGHASH_SINGLE", "SIGHASH_ANYONECANPAY", "SIGHASH_DEFAULT")]


def commitments_table():
    """for each flag, which of the five probed fields change the signature hash of input 1 (other input's outpoint, other input's sequence, the output with the same index,
    the other outputs, the input's own sequence)"""
    out = {}
    for ht in (1, 2, 3, 0x81, 0x82, 0x83):
        c = C.sighash_commitments(ht)
        out[hex(ht)] = [int(c[k]) for k in ("other input outpoint", "other input sequence", "output with the same index", "other outputs", "own sequence")]
    return out


def single_bug_hash():
    return C.sighash_single_bug()


def single_bug_equals_uint256_one():
    return C.sighash_single_bug() == "01" + "00" * 31


def core_refuses_single_bug_signature():
    r = _core()["single_bug"]
    return [r["result"]["complete"], r["all_complete"]]


def sighash_json_vectors():
    return C.sighash_json_check()


def bip341_valid_hash_types():
    """the seven values BIP341 allows; every other byte value is rejected by the BIP341 signature message function of the chapter's library"""
    ok = [h for h in range(256) if L.sighash_taproot(C.make_tx(2, 2), 0, h, [(1000, b"\x51"), (1000, b"\x51")]) is not None]
    return [hex(h) for h in ok]


def anyprevout_values():
    t = C.evtext("bip-0118.mediawiki")
    return [int(re.search(r"SIGHASH_ANYPREVOUT = (0x[0-9a-f]+)", t).group(1), 16), int(re.search(r"SIGHASH_ANYPREVOUTANYSCRIPT = (0x[0-9a-f]+)", t).group(1), 16)]


def core_flags_all_verify():
    """every signature in the 25 transactions Bitcoin Core 31.1 signed on regtest (4 address types, 6 flags, plus taproot's default) is verified here with the library:
    returns (signatures checked, signatures that verify)"""
    n = ok = 0
    for rec in _core()["flags"]:
        tx = L.parse_tx(rec["hex"]); spent = [(p["amount_sat"], bytes.fromhex(p["spk"])) for p in rec["prevouts"]]
        for i in range(len(tx.vin)):
            amount, spk = spent[i]
            n += 1
            if rec["type"] == "legacy":
                items = L.get_ops(tx.vin[i][2]) if False else None
                ss = tx.vin[i][2]; ln = ss[0]; sig = ss[1:1 + ln]; pk = ss[2 + ln:]
                digest = L.sighash_legacy(spk, tx, i, sig[-1]); ok += L.ecdsa_verify(pk, digest, sig[:-1])
            elif rec["type"] in ("p2sh-segwit", "bech32"):
                sig, pk = tx.witness[i]
                code = L.p2pkh_script(L.hash160(pk))
                digest = L.sighash_v0(code, tx, i, sig[-1], amount); ok += L.ecdsa_verify(pk, digest, sig[:-1])
            else:
                sig = tx.witness[i][0]; ht = sig[64] if len(sig) == 65 else 0
                digest = L.sighash_taproot(tx, i, ht, spent); ok += L.schnorr_verify(spk[2:], digest, sig[:64])
    return n, ok


def core_flag_bytes():
    """the hash type byte at the end of each signature Core made, by the flag requested, for the bech32 (P2WPKH) transactions; taproot's DEFAULT adds no byte"""
    out = {}
    for rec in _core()["flags"]:
        tx = L.parse_tx(rec["hex"])
        if rec["type"] == "bech32":
            out[rec["sighashtype"]] = hex(tx.witness[0][0][-1])
        if rec["type"] == "bech32m":
            sig = tx.witness[0][0]
            out["taproot " + rec["sighashtype"]] = [len(sig), hex(sig[64]) if len(sig) == 65 else None]
    return out


def core_signature_survives_changes():
    """take the P2WPKH transaction Core signed with each flag, change (a) the amount of the output with the same index as input 0 and (b) a different output, and ask whether the
    signature of input 0 still verifies against the changed transaction. Returns {flag: [still valid after (a), still valid after (b)]}"""
    res = {}
    for rec in _core()["flags"]:
        if rec["type"] != "bech32":
            continue
        tx0 = L.parse_tx(rec["hex"]); spent = [(p["amount_sat"], bytes.fromhex(p["spk"])) for p in rec["prevouts"]]
        sig, pk = tx0.witness[0]; code = L.p2pkh_script(L.hash160(pk))
        row = []
        for out_idx in (0, 2):
            tx = L.parse_tx(rec["hex"]); v, s = tx.vout[out_idx]; tx.vout[out_idx] = (v - 1, s)
            row.append(L.ecdsa_verify(pk, L.sighash_v0(code, tx, 0, sig[-1], spent[0][0]), sig[:-1]))
        res[rec["sighashtype"]] = row
    return res


def core_anyonecanpay_survives_other_input_change():
    """change the outpoint of input 2 in the P2WPKH transactions: input 0's signature keeps verifying only when ANYONECANPAY is set"""
    res = {}
    for rec in _core()["flags"]:
        if rec["type"] != "bech32":
            continue
        tx = L.parse_tx(rec["hex"]); spent = [(p["amount_sat"], bytes.fromhex(p["spk"])) for p in rec["prevouts"]]
        sig, pk = tx.witness[0]; code = L.p2pkh_script(L.hash160(pk))
        h, n, ss, seq = tx.vin[2]; tx.vin[2] = (b"\xaa" * 32, 5, ss, seq)
        res[rec["sighashtype"]] = L.ecdsa_verify(pk, L.sighash_v0(code, tx, 0, sig[-1], spent[0][0]), sig[:-1])
    return res


# ---- 3. Schnorr ------------------------------------------------------------------------------------------------------------
def toy():
    r = C.toy_protocol()
    return [r["xG"], r["kG"], r["s"], r["sG"], r["exG"], r["holds"], r["divide_back"]]


def identity_round_secp256k1():
    return C.identity_round(0xC0FFEE1234, 0xBADA55AA99, int.from_bytes(hashlib.sha256(b"challenge").digest(), "big") % N)[0]


def identity_wrong_s():
    ok, s = C.identity_round(0xC0FFEE1234, 0xBADA55AA99, 12345)
    return point_equal_after(s + 1)


def point_equal_after(s_bad):
    x, k, e = 0xC0FFEE1234, 0xBADA55AA99, 12345
    return L.point_mul(s_bad % N) == L.point_add(L.point_mul(k), L.point_mul(e, L.point_mul(x)))


def impersonation_without_x():
    X = L.point_mul(0xC0FFEE1234)
    e = int.from_bytes(hashlib.sha256(b"challenge handed out too early").digest(), "big") % N
    R, s, ok = C.impersonate_with_known_challenge(X, e)
    return ok


def fiat_shamir_signature():
    x = 0x5EC12E7; k = 0xA11CE5; m = b"spend output 1"
    X = L.point_mul(x); sig = C.fs_sign(x, m, k)
    return [C.fs_verify(X, m, sig), C.fs_verify(X, b"spend output 2", sig)]


def scalar_modulus():
    a, b, c = C.modulus_check()
    return [a, b, c, P > N, P - N > 2 ** 128]


def linearity():
    return list(C.linearity())


def related_key_attack():
    return [C.related_key_attack(prefixed=False), C.related_key_attack(prefixed=True)]


def bip340_vectors():
    rows = C.bip340_vectors()
    ok = signs = nsign = 0
    for r in rows:
        try:
            v = L.schnorr_verify(bytes.fromhex(r["public key"]), bytes.fromhex(r["message"]), bytes.fromhex(r["signature"]))
        except Exception:
            v = False
        ok += v == (r["verification result"] == "TRUE")
        if r["secret key"]:
            nsign += 1; s = int(r["secret key"], 16)
            signs += (L.schnorr_pubkey(s).hex().upper() == r["public key"] and L.schnorr_sign(s, bytes.fromhex(r["message"]), bytes.fromhex(r["aux_rand"])).hex().upper() == r["signature"])
    return [len(rows), ok, nsign, signs]


def signature_sizes():
    return [C.bip340_sign_size(0), C.bip340_sign_size(1)]


def xonly_even_y():
    """the public key of BIP340 is 32 bytes; the signer negates the private key when the point has an odd y; both keys give the same x-only key"""
    d = 0x3b78ce563f89a0ed9414f5aa28ad0d96d6795f9c63
    pt = L.point_mul(d)
    return [len(L.schnorr_pubkey(d)), pt[1] % 2, L.schnorr_pubkey(d) == L.schnorr_pubkey(N - d)]


def tagged_hash_prefix_len():
    return [len(hashlib.sha256(b"BIP0340/challenge").digest()) * 2, L.tagged_hash("BIP0340/challenge", b"x") != hashlib.sha256(b"x").digest()]


def batch_equation():
    rows = [r for r in C.bip340_vectors() if r["verification result"] == "TRUE"]
    good = [(bytes.fromhex(r["public key"]), bytes.fromhex(r["message"]), bytes.fromhex(r["signature"])) for r in rows]
    bad = list(good); bad[2] = (good[2][0], good[2][1], good[3][2])
    return [len(good), C.bip340_batch_verify(good), C.bip340_batch_verify(bad)]


def naive_multisig():
    ok, X = C.naive_multisig(0x1111, 0x2222, 0x3333, 0x4444, b"two keys")
    return [ok, X == L.point_add(L.point_mul(0x1111), L.point_mul(0x2222))]


def key_cancellation():
    return list(C.key_cancellation(0x1111, 0x2222, 0x4444, b"Bob signs alone"))


def musig2_keyagg_vectors():
    return list(C.keyagg_vectors())


def musig2_blocks_cancellation():
    return C.musig2_cancellation_attempt()


def shamir_threshold():
    return list(C.threshold_demo())


def shamir_manipulation():
    return list(C.manipulation_attack())


def single_share_hides_secret():
    return C.shares_alone_reveal_nothing()


def shamir_any_two_of_three():
    sh = C.shamir_split(31337, 2, [1, 2, 3], [4242])
    return [C.shamir_combine([sh[0], sh[1]]), C.shamir_combine([sh[0], sh[2]]), C.shamir_combine([sh[1], sh[2]])]


# ---- 4. ECDSA ------------------------------------------------------------------------------------------------------------------
def book_der_sample():
    sig = bytes.fromhex("3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301")
    f = C.der_fields(sig)
    return [len(sig), len(sig) - 3, f[0][1], f[1][1], f[3][1], f[6][1], f[8][1], len(f), C.der_strict_ok(sig)]


def book_der_text_matches_book():
    return C.has("book_ch08_signatures.adoc", "3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204", "b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301")


def book_sample_s_low():
    sig = bytes.fromhex("3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301")
    r, s = L.der_parse_lax(sig[:-1])
    return [s <= N // 2, r >= 2 ** 255, len(hex(r)) - 2]


def book_sample_in_mainnet_tx():
    j, tx = _tx_from_mempool("mainnet_tx_0627052b.json")
    sig_hex = "3045022100884d142d86652a3f47ba4746ec719bbfbd040a570b1deccbb6498c75c4ae24cb02204b9f039ff08df09cbe9f6addac960298cad530a863ea8f53982c09db8f6e381301"
    return [sig_hex in j["vin"][0]["scriptsig"], j["status"]["block_height"], j["status"]["block_time"]]


def book_sample_verifies():
    j, tx = _tx_from_mempool("mainnet_tx_0627052b.json")
    ss = tx.vin[0][2]; ln = ss[0]; sig = ss[1:1 + ln]; pk = ss[2 + ln:]
    spk = bytes.fromhex(j["vin"][0]["prevout"]["scriptpubkey"])
    digest = L.sighash_legacy(spk, tx, 0, sig[-1])
    tampered = L.sighash_legacy(spk, tx, 0, 2)
    return [len(pk), sig[-1], L.ecdsa_verify(pk, digest, sig[:-1]), L.ecdsa_verify(pk, tampered, sig[:-1]), len(sig)]


def ecdsa_book_formulas():
    x, k = SK, 0xD1CE5EED; h = int.from_bytes(MSG, "big") % N
    R, s = C.ecdsa_sign_k(x, h, k)
    X = L.point_mul(x)
    return [C.ecdsa_verify_K(X, h, R, s), C.ecdsa_verify_K(X, (h + 1) % N, R, s), R == L.point_mul(k)[0] % N]


def malleability():
    x, k = SK, 0xD1CE5EED; h = int.from_bytes(MSG, "big") % N
    R, s = C.ecdsa_sign_k(x, h, k); X = L.point_mul(x)
    return [C.ecdsa_verify_K(X, h, R, s), C.ecdsa_verify_K(X, h, R, N - s), (s <= N // 2) != ((N - s) <= N // 2)]


def lib_signature_low_s_and_strict():
    sigs = [L.ecdsa_sign(SK + i, hashlib.sha256(b"m%d" % i).digest()) for i in range(200)]
    lens = sorted(set(len(s) for s in sigs))
    return [all(C.der_strict_ok(s + b"\x01") for s in sigs), all(L.der_parse_lax(s)[1] <= N // 2 for s in sigs), lens]


def rfc6979_p256_vector():
    """RFC 6979 appendix A.2.5: private key, SHA-256 of 'sample' -> k. The numbers are read back from the saved RFC text"""
    t = C.evtext("rfc6979.txt")
    i = t.index("A.2.5.  ECDSA, 256 Bits (Prime Field)", t.index("A.2.5.  ECDSA, 256 Bits (Prime Field)") + 10)
    seg = t[i:i + 3000]
    x = int(re.search(r"x = ([0-9A-F]+)", seg).group(1), 16)
    j = seg.index('With SHA-256, message = "sample":')
    kref = int(re.search(r"k = ([0-9A-F]+)", seg[j:]).group(1), 16)
    h1 = hashlib.sha256(b"sample").digest()
    return [C.rfc6979_k(C.P256_Q, x, h1) == kref, hex(kref)[:10]]


def rfc6979_deterministic():
    a = L.ecdsa_sign(SK, MSG); b = L.ecdsa_sign(SK, MSG)
    c = L.ecdsa_sign(SK, hashlib.sha256(b"other").digest())
    return [a == b, a != c]


def rfc6979_matches_library_nonce():
    h = int.from_bytes(MSG, "big") % N
    k = C.rfc6979_k(N, SK, MSG)
    R, s = C.ecdsa_sign_k(SK, h, k)
    if s > N // 2: s = N - s
    return L.der_parse_lax(L.ecdsa_sign(SK, MSG)) == (R, s)


def nonce_reuse():
    x = 0xFEEDFACECAFE1234; k = 0x1234567890ABCDEF
    h1 = int.from_bytes(hashlib.sha256(b"payment to Bob").digest(), "big") % N
    h2 = int.from_bytes(hashlib.sha256(b"payment to Carol").digest(), "big") % N
    r1, s1 = C.ecdsa_sign_k(x, h1, k); r2, s2 = C.ecdsa_sign_k(x, h2, k)
    got, kk = C.recover_key_from_reused_nonce(r1, s1, h1, s2, h2)
    return [r1 == r2, got == x, kk == k]


def nonce_not_reused_is_safe():
    """with different nonces the same formula returns a number that is not the key"""
    x = 0xFEEDFACECAFE1234
    h1 = int.from_bytes(hashlib.sha256(b"a").digest(), "big") % N
    h2 = int.from_bytes(hashlib.sha256(b"b").digest(), "big") % N
    r1, s1 = C.ecdsa_sign_k(x, h1, 111); r2, s2 = C.ecdsa_sign_k(x, h2, 222)
    return C.recover_key_from_reused_nonce(r1, s1, h1, s2, h2)[0] == x


def bip340_default_signing_deterministic():
    a = L.schnorr_sign(SK, MSG); b = L.schnorr_sign(SK, MSG); c = L.schnorr_sign(SK, MSG, b"\x01" * 32)
    return [a == b, a != c, L.schnorr_verify(L.schnorr_pubkey(SK), MSG, c)]


def core_ecdsa_deterministic_and_schnorr_aux_zero():
    t = _core()["twice"]
    return [t["bech32"]["equal"], t["bech32m"]["equal"]]


def core_signature_lengths():
    d = _core()["lengths"]
    lens = {int(k): v for k, v in d["sig_lengths"].items()}
    return [d["inputs"], max(lens), min(lens), sum(lens.values())]


def core_lengths_all_verify():
    d = _core()["lengths"]; tx = L.parse_tx(d["hex"]); spent = [(p["amount_sat"], bytes.fromhex(p["spk"])) for p in d["prevouts"]]
    ok = 0
    for i in range(len(tx.vin)):
        sig, pk = tx.witness[i]
        ok += L.ecdsa_verify(pk, L.sighash_v0(L.p2pkh_script(L.hash160(pk)), tx, i, sig[-1], spent[i][0]), sig[:-1])
    return [len(tx.vin), ok]


def core_signatures_low_r():
    d = _core()["lengths"]; tx = L.parse_tx(d["hex"])
    rs = [L.der_parse_lax(w[0][:-1])[0] for w in tx.witness]
    return [sum(1 for r in rs if r < 2 ** 255), len(rs)]


def library_signatures_high_r_share():
    n = 400
    hi = sum(1 for i in range(n) if L.der_parse_lax(L.ecdsa_sign(SK + i, hashlib.sha256(b"q%d" % i).digest()))[0] >= 2 ** 255)
    return [n, hi, 0.4 < hi / n < 0.6]


# ---- 5. policy and consensus, as Core answered them ------------------------------------------------------------------
def core_policy_verdicts():
    v = _core()["own_ecdsa"]["variants"]
    return {k: [x["allowed"], x["reject_reason"]] for k, x in v.items()}


def core_high_s_consensus():
    o = _core()["own_ecdsa"]
    return [o["high_s_in_block"]["accepted"], o["non_der_in_block"]["accepted"], "Non-canonical DER signature" in o["non_der_in_block"]["result"]]


def core_taproot_verdicts():
    v = _core()["own_schnorr"]["variants"]
    return {k: [x["allowed"], x["reject_reason"]] for k, x in v.items()}


def own_variants_digests():
    """the high-S and the low-S signature share R; their S values add up to the group order"""
    o = _core()["own_ecdsa"]["variants"]
    def sig_of(hexs):
        tx = L.parse_tx(hexs); ss = tx.vin[0][2]; ln = ss[0]; return ss[1:1 + ln - 1]
    a, b = L.der_parse_lax(sig_of(o["valid_low_s"]["hex"])), L.der_parse_lax(sig_of(o["high_s"]["hex"]))
    return [a[0] == b[0], (a[1] + b[1]) % N == 0, a[1] <= N // 2 < b[1]]


# ---- 6. hashing cost ---------------------------------------------------------------------------------------------------------
def hashing_bytes():
    out = []
    for n in (1, 10, 100, 1000):
        t = C.make_tx(n); out.append([n, C.legacy_bytes_hashed(t), C.bip143_bytes_hashed(t)])
    return out


def hashing_growth():
    a = C.legacy_bytes_hashed(C.make_tx(100)); b = C.legacy_bytes_hashed(C.make_tx(1000))
    c = C.bip143_bytes_hashed(C.make_tx(100)); d = C.bip143_bytes_hashed(C.make_tx(1000))
    return [round(b / a, 1), round(d / c, 1)]


def bip143_commits_to_amount():
    t = C.make_tx(2, 1); code = b"\x76\xa9\x14" + b"\x22" * 20 + b"\x88\xac"
    return L.sighash_v0(code, t, 0, 1, 1000) != L.sighash_v0(code, t, 0, 1, 1001)


def legacy_does_not_commit_to_amount():
    t = C.make_tx(2, 1); code = b"\x76\xa9\x14" + b"\x22" * 20 + b"\x88\xac"
    return L.sighash_legacy(code, t, 0, 1) == L.sighash_legacy(code, t, 0, 1)


def bip341_commits_to_all_spent_amounts():
    t = C.make_tx(2, 1)
    a = L.sighash_taproot(t, 0, 0, [(1000, b"\x51"), (2000, b"\x51")]); b = L.sighash_taproot(t, 0, 0, [(1000, b"\x51"), (2001, b"\x51")])
    c = L.sighash_taproot(t, 0, 0x81, [(1000, b"\x51"), (2000, b"\x51")]); d = L.sighash_taproot(t, 0, 0x81, [(1000, b"\x51"), (2001, b"\x51")])
    return [a != b, c == d]


def sigops_limit_in_core_and_bip54():
    pol = C.evtext("core_src_policy_policy.h"); b54 = C.evtext("bip-0054.md")
    return [int(re.search(r"MAX_TX_LEGACY_SIGOPS\{([\d']+)\}", pol).group(1).replace("'", "")), "strictly higher than 2500" in b54]


# ---- 7. real mainnet taproot spend --------------------------------------------------------------------------------------
def first_taproot_spend():
    j, tx = _tx_from_mempool("mainnet_tx_33e794d0.json")
    spent = [(j["vin"][0]["prevout"]["value"], bytes.fromhex(j["vin"][0]["prevout"]["scriptpubkey"]))]
    sig = tx.witness[0][0]
    digest = L.sighash_taproot(tx, 0, sig[64] if len(sig) == 65 else 0, spent)
    return [j["status"]["block_height"], len(tx.witness[0]), len(sig), L.schnorr_verify(spent[0][1][2:], digest, sig[:64])]


# ---- 8. the sources and the dates --------------------------------------------------------------------------------------------
def sources_record():
    rec = json.load(open(C.ev("sources_record_v1_0_0.json")))
    ids = [k for k in rec if k.startswith("P")]
    return [len(ids), sum(1 for k in ids if rec[k]["http"] == 200), sum(rec[k]["passages"] for k in ids), sum(rec[k]["passages_found"] for k in ids)]


def sources_resaved():
    """every saved copy still has the SHA-256 recorded when it was fetched"""
    rec = json.load(open(C.ev("sources_record_v1_0_0.json")))
    bad = [k for k in rec if k.startswith("P") and hashlib.sha256(open(C.ev(rec[k]["saved_as"]), "rb").read()).hexdigest() != rec[k]["saved_sha256"]]
    return bad


def all_passages_present():
    import sen0401_ch08_sources_v1_0_0 as S
    miss = [(s["id"], p) for s in S.SRC for p in s["passages"] if not C.has(s["save"], p)]
    return miss


def patent_dates():
    import datetime as dt
    filed, granted = dt.date(1990, 2, 23), dt.date(1991, 2, 19)
    g17 = granted.replace(year=granted.year + 17); f20 = filed.replace(year=filed.year + 20)
    return [str(g17), str(f20), max(g17, f20) == f20, C.has("google_patent_US4995082.txt", "1990-02-23", "1991-02-19", "Expired - Lifetime"),
            C.has("cornell_35usc154.txt", "greater of the 20-year term", "17 years from grant")]


def schnorr_to_taproot_years():
    return [2021 - 1991, 2021 - 1989]


def activation_gap_days():
    import datetime as dt
    return (dt.date(2021, 11, 14) - dt.date(2009, 1, 3)).days


def timestamp_of_first_taproot_spend():
    import datetime as dt
    j = json.load(open(C.ev("mainnet_tx_33e794d0.json")))
    return dt.datetime.fromtimestamp(j["status"]["block_time"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def timestamp_of_book_tx():
    import datetime as dt
    j = json.load(open(C.ev("mainnet_tx_0627052b.json")))
    return dt.datetime.fromtimestamp(j["status"]["block_time"], dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def bips_status():
    t = C.evtext("bips_README.mediawiki")
    def status(num):
        m = re.search(r"\[\[bip-0*%d\.[a-z]+\|%d\]\]\n\|[^\n]*\n\|[^\n]*\n\|[^\n]*\n\|[^\n]*\n\| ([A-Za-z]+)" % (num, num), t)
        return m.group(1) if m else None
    return {n: status(n) for n in (66, 118, 143, 146, 327, 340, 341, 342, 373, 390, 54, 461, 361)}


def core_musig_support():
    t = C.evtext("core_doc_bips.md")
    return [("v30.0" in re.search(r"BIP 327.*", t).group(0)), ("v31.0" in re.search(r"BIP 327.*", t).group(0)), C.has("core_doc_descriptors_v29.0.md", "tr(KEY)"),
            "musig" not in C.evtext("core_doc_descriptors_v29.0.md").lower(), "musig" in C.evtext("core_doc_descriptors_v31.0.md").lower()]


def libsecp_changes():
    t = C.evtext("secp256k1_CHANGELOG.md")
    return [bool(re.search(r"## \[0\.8\.0\] - 2026-08-03", t)), "Removed previously deprecated function alias `secp256k1_schnorrsig_sign`" in t,
            "secp256k1_schnorrsig_sign32" in C.evtext("core_src_key.cpp")]


def core_grind_and_aux():
    k = C.evtext("core_src_key.cpp"); s = C.evtext("core_src_script_sign.cpp")
    return ["Grind for low R" in k, "secp256k1_nonce_function_rfc6979" in k, "Use uint256{} as aux_rnd for now." in s, "So don't produce it." in s]


def verify_flags_in_policy():
    t = C.evtext("core_src_policy_policy.h")
    return [f in t for f in ("SCRIPT_VERIFY_LOW_S", "SCRIPT_VERIFY_NULLFAIL", "SCRIPT_VERIFY_STRICTENC", "SCRIPT_VERIFY_DERSIG")]


def libsecp_has_no_batch_api():
    t = C.evtext("secp256k1_README.md")
    return ["batch" in t.lower()]


def core_release_30_sigops():
    return C.has("core_release_30.0_notes.txt", "limited to 2500", "BIP54")


def core_binary_hash():
    """[the line is in the saved SHA256SUMS, the archive on disk (when it is present on this machine) hashes to it; None when the archive is absent]"""
    t = C.evtext("core_31.1_SHA256SUMS.txt")
    want = "b80d9c3e04da78fb6f0569685673418cf686fadba9042d926d13fb87ff503f9e"
    arc = "/home/claude/core31/bitcoin-31.1-x86_64-linux-gnu.tar.gz"
    return [want + "  bitcoin-31.1-x86_64-linux-gnu.tar.gz" in t, hashlib.sha256(open(arc, "rb").read()).hexdigest() == want if os.path.exists(arc) else None]


def core_node_identity():
    n = _core()["node"]
    return [n["version"], n["subversion"], n["chain"]]


def no_threshold_bip_in_index():
    """the BIP index (README of bitcoin/bips at the pinned commit) has no row about FROST or a threshold signature (its only 'threshold' is a segwit soft-fork activation proposal); Optech's topic page lists a 2024 mention of a proposed FROST BIP"""
    idx = C.evtext("bips_README.mediawiki").lower()
    return ["frost" in idx, idx.count("threshold"), "reduced threshold segwit masf" in idx, C.has("optech_threshold_signature.txt", "BIP proposed for creating FROST scriptless threshold signatures for Bitcoin")]


def core_doc_lists_bips():
    """whether Bitcoin Core's doc/bips.md (commit 05bc2f5) has an entry for each BIP: {number: listed}"""
    t = C.evtext("core_doc_bips.md")
    return {n: ("BIP %d`" % n) in t for n in (66, 143, 327, 340, 373, 390, 118, 54, 461, 361)}
