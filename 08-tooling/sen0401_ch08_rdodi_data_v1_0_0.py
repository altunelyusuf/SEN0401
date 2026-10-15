"""SEN0401 chapter 8 (Mastering Bitcoin 3rd edition, Digital Signatures) for the RDODI build.
Every source was fetched on 2026-10-15 and the passages the text relies on were found in the saved copies (08-tooling/ch08-evidence); every computation is a function of
sen0401_ch08_claims_v1_0_0.py that recomputes the claim from sen0401_ch08_sig_lib_v1_0_0.py (a library written for the chapter and checked against the 19 BIP340 vectors, Bitcoin
Core's 500 signature hash vectors, the BIP327 key aggregation vectors and the RFC 6979 vector) and from one run of Bitcoin Core 31.1.0 on regtest (core_regtest_record_v1_0_0.json).
The expected values are frozen in sen0401_ch08_expect_v1_0_0.py."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch08_text_meta_v1_0_0 as M
import sen0401_ch08_text_leaves_a_v1_0_0 as LA
import sen0401_ch08_text_leaves_b_v1_0_0 as LB
import sen0401_ch08_text_branches_v1_0_0 as BR
try:
    import sen0401_ch08_expect_v1_0_0 as X
    EXPECT = X.EXPECT
except ImportError:
    EXPECT = {}

CH = 8
DATE = "2026-10-15"
PYVER = "3.14.6"
VERSION = "1_0_0"
TITLE = "Digital signatures: SIGHASH, schnorr and ECDSA, recomputed against the standards and Bitcoin Core 31.1"
QUESTION = ("How do the signatures of chapter 8 of Mastering Bitcoin's 3rd edition work (what a signature commits to through the SIGHASH flags, how schnorr and ECDSA signatures are made, serialized and "
            "protected by their nonces, and what segwit changed), which of its examples, figures and statements can be reproduced from the standards and by Bitcoin Core 31.1, and where has the "
            "software or the state of the proposals moved since the book went to print?")
CQS = ("Which examples, figures and statements of the chapter can be reproduced by execution, by the standards' own test vectors and by Bitcoin Core, and what does the execution give?",
       "What in the chapter differs from the standards or from Bitcoin Core as it is now, or has changed status since the book went to print, and on what source?")
LABELS = BR.LABELS
PUBS = M.PUBS
CONCEPTS = M.CONCEPTS
FINDINGS = M.FINDINGS
KP = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch08_claims_v1_0_0 as K; "
LEAVES = LA.LEAVES_A + LB.LEAVES_B
TAX = []
BODY = {}
for top, mid, leaf, ex, d, kx, body in LEAVES:
    TAX.append((top, mid, leaf, ex, d, (KP + kx, EXPECT.get(kx, "?"))))
    BODY[leaf] = body
    BODY.setdefault(mid, BR.GROUP[mid]); BODY.setdefault(top, BR.BRANCH[top])
EXTRA = ["K.core_lengths_all_verify()", "K.core_signatures_low_r()", "K.book_der_text_matches_book()", "K.own_variants_digests()", "K.libsecp_has_no_batch_api()",
         "K.timestamp_of_first_taproot_spend()", "K.sources_resaved()", "K.all_passages_present()", "K.single_bug_hash()"]
CLAIMS = [(KP + e, EXPECT.get(e, "?")) for e in EXTRA]
BEH = [
 ("the book's remainder example: 5 divided by 3 leaves 2, which is what 'modulus 3' means", "print(5 % 3)", "2"),
 ("a DER integer is signed: the single byte 0x88 reads as a negative number, which is why a positive R with its top bit set needs a leading zero byte", "print(int.from_bytes(b'\\x88', 'big', signed=True), int.from_bytes(b'\\x00\\x88', 'big', signed=True))", "-120 136"),
 ("a line through two points is fixed, and the point where it crosses x = 0 is the secret in Shamir's 2-of-3 scheme (secret 7, slope 3, shares at x = 1 and 3 modulo 101)",
  "p = 101; s1, s3 = (7 + 3 * 1) % p, (7 + 3 * 3) % p; slope = (s3 - s1) * pow(3 - 1, -1, p) % p; print((s1 - slope * 1) % p)", "7"),
]
