#!/usr/bin/env python3
"""(1.2.0: also checks that at least 12 self-contained examples change their result when a whole number in them is changed, the way the page varies them; the corpus bridge is that of data module 1.2.0.)
Verify the chapter 8 signature library (sen0401_ch08_sig_lib_v1_0_0.py, on the chapter 7 script library) against evidence it did not write. Offline: no node and no network.

Run with python 3.14 and the standard library only:  python3.14 sen0401_ch08_verify_v1_0_0.py
It reads the saved copies in ch08-evidence (the BIP340 test vectors, Bitcoin Core's sighash.json, the BIP327 key aggregation vectors, RFC 6979, two mainnet transactions, the record of one
run of Bitcoin Core 31.1.0 on regtest, the record of the sources fetched) and prints one line per check with the measured count. Exit 1 when any check fails. The checks, in order:
  1. BIP340 test vectors: all verification results and all signing vectors of the saved CSV.
  2. Bitcoin Core src/test/data/sighash.json: the legacy signature hash of every vector.
  3. BIP327 key aggregation vectors (valid and error cases).
  4. RFC 6979 appendix A.2.5 (P-256, SHA-256, 'sample'): the nonce.
  5. The 75 signatures in the 25 transactions that Bitcoin Core 31.1 signed (4 address types x 6 flags + taproot default).
  6. The 300 signatures of one 300-input transaction signed by Bitcoin Core: all verify, all low R, lengths.
  7. Bitcoin Core's verdicts on the chapter's own altered signatures (policy and in-block), read from the record.
  8. Two real mainnet transactions: the signature printed in the book (block 277,316) and the first taproot key-path spend (block 709,635).
  9. Tampering: a flipped bit in a signature or in a segwit amount must fail.
 10. Sources: every saved copy has the SHA-256 recorded when it was fetched, and every passage is in it.
 11. The chapter's claims (sen0401_ch08_claims_v1_0_0.py): every function runs and the corpus bridge reports no failure."""
__version__ = "1.2.0"
import json, os, sys, hashlib
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sen0401_ch07_script_lib_v1_0_0 as L
import sen0401_ch08_sig_lib_v1_0_0 as C
import sen0401_ch08_claims_v1_0_0 as K
RESULTS = []
FAILED = []


def report(name, ok, total, extra=""):
    RESULTS.append((name, ok, total))
    if ok != total:
        FAILED.append(name)
    print("%-4s %-66s %5d / %-5d %s" % ("PASS" if ok == total else "FAIL", name, ok, total, extra))


v = K.bip340_vectors()
report("BIP340: verification results (19 rows)", v[1], v[0]); report("BIP340: signing vectors reproduce public key and signature", v[3], v[2])
a = K.sighash_json_vectors(); report("Bitcoin Core sighash.json: legacy signature hash", a[1], a[0], "(%d hash-type bytes)" % a[2])
k = K.musig2_keyagg_vectors(); report("BIP327 key aggregation vectors", k[1], k[0])
r = K.rfc6979_p256_vector(); report("RFC 6979 A.2.5 nonce", int(r[0]), 1, r[1])
f = K.core_flags_all_verify(); report("Core 31.1: 25 transactions, 4 types x 6 flags + default, every signature verifies", f[1], f[0])
l = K.core_lengths_all_verify(); report("Core 31.1: 300 signatures of one transaction verify", l[1], l[0])
lr = K.core_signatures_low_r(); report("Core 31.1: all 300 signatures have a low R", lr[0], lr[1])
sl = K.core_signature_lengths(); report("Core 31.1: lengths 70..71 bytes incl. hash type", int(sl[1] == 71 and sl[2] == 70), 1, "longest %d shortest %d of %d" % (sl[1], sl[2], sl[3]))
pv = K.core_policy_verdicts(); report("Core 31.1 policy: low-S allowed, high-S / non-minimal DER / other message refused", int(pv["valid_low_s"][0]) + sum(1 for x in ("high_s", "non_minimal_der", "signed_other_message") if not pv[x][0]), 4)
hs = K.core_high_s_consensus(); report("Core 31.1 in a block: high-S accepted, non-DER refused", int(hs[0]) + int(not hs[1]) + int(hs[2]), 3)
tv = K.core_taproot_verdicts(); report("Core 31.1 taproot: 64 and explicit-ALL allowed, 4 malformed refused", sum(1 for x in ("default_64", "explicit_all_65") if tv[x][0]) + sum(1 for x in ("explicit_zero_65", "short_63", "flipped_bit", "hash_type_mismatch") if not tv[x][0]), 6)
sb = K.core_refuses_single_bug_signature(); report("Core 31.1 will not sign SIGHASH_SINGLE without an output (control signs)", int(not sb[0]) + int(sb[1]), 2)
bm = K.book_sample_in_mainnet_tx(); bv = K.book_sample_verifies()
report("Mainnet: the book's DER signature is in tx 0627052b (block 277,316) and verifies", int(bm[0] and bm[1] == 277316) + int(bv[2]) + int(not bv[3]), 3)
tp = K.first_taproot_spend(); report("Mainnet: taproot key-path spend in block 709,635 verifies (BIP341)", int(tp[0] == 709635 and tp[2] == 64) + int(tp[3]), 2)

# tampering: one flipped bit in a signature, or one satoshi in a segwit amount, must make a real signature fail
rec = json.load(open(C.ev("core_regtest_record_v1_0_0.json")))
ok = 0; tot = 0
for t in rec["flags"]:
    if t["type"] != "bech32":
        continue
    tx = L.parse_tx(t["hex"]); sp = [(p["amount_sat"], bytes.fromhex(p["spk"])) for p in t["prevouts"]]
    sig, pk = tx.witness[0]; code = L.p2pkh_script(L.hash160(pk)); body = sig[:-1]
    good = L.ecdsa_verify(pk, L.sighash_v0(code, tx, 0, sig[-1], sp[0][0]), body)
    badsig = bytes([body[10] ^ 1]) + body[11:]; badsig = body[:10] + badsig
    try:
        a1 = L.ecdsa_verify(pk, L.sighash_v0(code, tx, 0, sig[-1], sp[0][0]), badsig)
    except Exception:
        a1 = False
    a2 = L.ecdsa_verify(pk, L.sighash_v0(code, tx, 0, sig[-1], sp[0][0] + 1), body)
    tot += 3; ok += int(good) + int(not a1) + int(not a2)
report("Tampering: good verifies, flipped bit fails, amount + 1 satoshi fails (6 flags)", ok, tot)

s = K.sources_record(); report("Sources: all fetched with HTTP 200 and every passage found", int(s[0] == s[1] and s[2] == s[3]), 1, "%d sources, %d passages" % (s[0], s[2]))
rs = K.sources_resaved(); report("Sources: every saved copy has the recorded SHA-256", int(not rs), 1, str(rs) if rs else "")
mp = K.all_passages_present(); report("Sources: every passage of the source list is in its saved copy", int(not mp), 1, str(mp[:3]) if mp else "")
pic = json.load(open(C.ev("pictures_record_v1_0_0.json")))
pok = 0
for key, d in pic.items():
    p = os.path.join(os.path.dirname(HERE), "03-materials", "ch08", "assets", d["file"])
    pok += os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == d["sha256"]
report("Pictures: each story picture has the recorded SHA-256", pok, len(pic))
import sen0401_ch08_corpus_v1_2_0 as CO
n, bad = CO.run_checks_inprocess(); report("Chapter claims: every executed leaf, claim and behaviour of the data module", n - len(bad), n)

# 1.2.0: examples whose numbers can be changed: a self-contained expression (no library of the chapter), a whole-number literal of at most 50 outside quotes, and a different result when it is changed by up to 3
import ast, re
def _ev(src):
    t_ = ast.parse(src); last = t_.body.pop(); ns = {}
    exec(compile(t_, "x", "exec"), ns)
    return repr(eval(compile(ast.Expression(last.value), "x", "eval"), ns))
_LIT = re.compile(r"(?<![\w.'\"])\d+(?![\w.'\"])")
varied = []
for row in CO.D.TAX:
    if not row[5] or "sen0401" in row[5][0]:
        continue
    code = row[5][0]; chg = False
    for m in _LIT.finditer(code):
        if int(m.group(0)) > 50:
            continue
        for d_ in (-2, -1, 1, 2, 3):
            c2 = code[:m.start()] + str(max(0, int(m.group(0)) + d_)) + code[m.end():]
            try:
                out = _ev(c2)
            except BaseException:
                continue
            if out != row[5][1] and len(out) <= 80:
                chg = True; break
        if chg: break
    if chg: varied.append(row[2])
report("Examples with changeable numbers (self-contained, result changes when a number is changed)", int(len(varied) >= 12), 1, "%d examples" % len(varied))
print("%d checks; %d failed" % (len(RESULTS), len(FAILED)))
print("failures:", FAILED)
sys.exit(1 if FAILED else 0)
