#!/usr/bin/env python3
"""SEN0401 chapter 4 corpus, version 1.1.0: Keys and Addresses (chapter 4 of Mastering Bitcoin, 3rd edition), each concept explained in four to
six paragraphs of continuous prose (what it is, why it matters, where it is met, how it works, what to watch for), plus the concepts the
explanations rely on (the finite field, the elliptic curve, point addition, the generator point, the discrete logarithm, the hash function,
SHA256, RIPEMD-160, HASH160, bits and bytes, number bases, the QR code, the checksum, output and input scripts, the stack machine, the redeem
script, the three attacks on short hashes, the witness version and program, the BCH code, the deterministic wallet, the hardware signing device,
the test vectors, the URI ...), so that no term is used unexplained. The facet name at the start of a paragraph is only the author's writing
guide and is never printed.

Used by sen0401_chapter_build_v1_0_0.py (TBox/ABox/document). Every concept id of version 1.0.0 is kept with its parent; new concepts and new
subject groups are added. The text lives in sen0401_ch04_text_a..f_v1_1_0.py and the executed claims in sen0401_ch04_checks_a..f_v1_1_0.py,
which this module assembles and whose citation markers it resolves to author-year strings of the chapter's research record.

Sources actually read for this version and saved under 08-tooling/ch04-evidence: the chapter's own source (ch04_keys.adoc of the bitcoinbook
working copy, tag third_edition_print1) and, in the same book, chapters 1, 5 and 13; SEC 2 version 2.0 (Certicom Research), sections 2.4.1 and
2.4.2 and the parameter and status tables; BIPs 16, 38, 141, 142, 173, 340 and 350 from the BIPs repository, with their preamble lines, their
code snippets and the full BIP350 test vectors; FIPS 180-4's description; RFC 791, RFC 3022 and RFC 3986; the Decentralized Identifiers v1.0
recommendation of the World Wide Web Consortium; the source of Python's secrets module documentation at tag v3.14.4; Bitcoin Core's tree at the
checked-out commit (doc/descriptors.md, doc/files.md, src/script/script.h and the release notes of 30.0); the evidence of a run of Bitcoin Core
31.1 as an offline node (address types, getnewaddress, importdescriptors, deriveaddresses, validateaddress and the removed legacy commands);
the sipa/bech32 reference implementation that the book itself runs; and a third party's estimate of the network hash rate read on 2026-09-28.
Every number, hash, address, script, encoding, size or output quoted in the text is executed by the chapter builder (python 3.14), and every
sentence taken from a source carries a claim that re-reads the phrase from the saved copy of that source.
"""
__version__ = "1.1.0"
import os as _os
import sys as _sys
_HERE = _os.path.dirname(_os.path.abspath(__file__))
if _HERE not in _sys.path:
    _sys.path.insert(0, _HERE)

from sen0401_ch04_text_a_v1_1_0 import NODES_A
from sen0401_ch04_text_b_v1_1_0 import NODES_B
from sen0401_ch04_text_c_v1_1_0 import NODES_C
from sen0401_ch04_text_d_v1_1_0 import NODES_D
from sen0401_ch04_text_e_v1_1_0 import NODES_E
from sen0401_ch04_text_f_v1_1_0 import NODES_F
from sen0401_ch04_checks_a_v1_1_0 import CHECKS_A
from sen0401_ch04_checks_b_v1_1_0 import CHECKS_B
from sen0401_ch04_checks_c_v1_1_0 import CHECKS_C
from sen0401_ch04_checks_d_v1_1_0 import CHECKS_D
from sen0401_ch04_checks_e_v1_1_0 import CHECKS_E
from sen0401_ch04_checks_f_v1_1_0 import CHECKS_F
from sen0401_ch04_checkhelp_v1_1_0 import KT

CHAPTER = "04"

# ---- citations: each marker becomes an author-year string that resolves to a publication of the chapter's research record ----
_CITES = {
    "[BK]": " (Antonopoulos and Harding, 2023)",
    "[CORE]": " (Bitcoin Core, 2026)",
    "[SEC2]": " (Certicom Research, 2010)",
    "[B16]": " (Andresen, 2012)",
    "[B38]": " (Caldwell and Voisine, 2012)",
    "[B141]": " (Lombrozo et al., 2015)",
    "[B173]": " (Wuille and Maxwell, 2017)",
    "[B340]": " (Wuille et al., 2020)",
    "[B350]": " (Wuille, 2020)",
    "[DID]": " (World Wide Web Consortium, 2022)",
    "[W3C]": " (World Wide Web Consortium, 2022)",
    "[PSF]": " (Python Software Foundation, 2026)",
    "[FIPS]": " (National Institute of Standards and Technology, 2015)",
    "[R791]": " (Postel, 1981)",
    "[R3022]": " (Srisuresh and Egevang, 2001)",
    "[R3986]": " (Berners-Lee et al., 2005)",
    "[HR]": " (Mempool Space, 2026)",
    "[AL]": " (Altunel, 2021)",
}


def _c(t):
    t = t.replace("][", "] [")          # two markers written side by side are two citations
    for k, v in _CITES.items():
        t = t.replace(" " + k, v)
    assert not any(k in t for k in _CITES), t
    return t


NODES = NODES_A + NODES_B + NODES_C + NODES_D + NODES_E + NODES_F
NODES = [(n[0], n[1], n[2], n[3], n[4], [(f, _c(t)) for f, t in n[5]]) for n in NODES]

CHECKS = CHECKS_A + CHECKS_B + CHECKS_C + CHECKS_D + CHECKS_E + CHECKS_F

# ---- claims that something fails (executed by the chapter builder) ----
RAISES = [
    ("bytes.fromhex('abc')", "ValueError"),
    ("bytes.fromhex('0g')", "ValueError"),
    ("int('0O', 16)", "ValueError"),
    ("pow(0, -1, 17)", "ValueError"),
    ("__import__('hashlib').sha256('abc')", "TypeError"),
    ("__import__('hashlib').new('ripemd160', 'abc')", "TypeError"),
    ("(2 ** 256).to_bytes(32, 'big')", "OverflowError"),
    ("bytes([256])", "ValueError"),
    ("int.from_bytes('abc', 'big')", "TypeError"),
    ("%s.b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZz')" % KT, "AssertionError"),
    ("%s.b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoX0y')" % KT, "ValueError"),
    ("%s.decompress(bytes.fromhex('02' + '00' * 32))" % KT, "AssertionError"),
    ("%s.CHARSET.index('b')" % KT, "ValueError"),
    ("%s.wif(2 ** 256)" % KT, "OverflowError"),
    ("%s.segwit_decode('bc', 'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaef')[0]" % KT, "TypeError"),
]

# ---- the part a concept belongs to (chx:X_leaf chx:hasOwner chx:X_owner) ----
OWNERS = [
    ("GeneratorPoint", "Secp256k1"),
    ("PointMultiplication", "Secp256k1"),
    ("Hash160", "Commitment"),
    ("Checksum", "Base58Check"),
    ("VersionPrefix", "Base58Check"),
    ("Commitment", "P2pkhAddress"),
    ("RedeemScript", "P2shAddress"),
    ("MultisigScript", "RedeemScript"),
    ("WitnessVersion", "Bech32mAddress"),
    ("WitnessProgram", "Bech32mAddress"),
    ("HumanReadablePart", "Bech32mAddress"),
    ("BchCode", "Bech32Address"),
    ("OutputScript", "P2pk"),
    ("InputScript", "P2pk"),
]

# ---- error conditions, each attached to the concept that explains it (executed by the chapter builder) ----
ERRORS = [
    ("BitsAndBytes", "bytes.fromhex('abc') raises ValueError: fromhex() arg must contain an even number of hexadecimal digits"),
    ("NumberBase", "int('0O', 16) raises ValueError: invalid literal for int() with base 16"),
    ("FiniteField", "pow(0, -1, 17) raises ValueError: base is not invertible for the given modulus"),
    ("Sha256", "__import__('hashlib').sha256('abc') raises TypeError: Strings must be encoded before hashing"),
    ("Ripemd160", "__import__('hashlib').new('ripemd160', 'abc') raises TypeError: Strings must be encoded before hashing"),
    ("PrivateKey", "(2 ** 256).to_bytes(32, 'big') raises OverflowError: int too big to convert"),
    ("Checksum", "%s.b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZz') raises AssertionError: checksum does not match" % KT),
    ("Base58Check", "%s.b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoX0y') raises ValueError: substring not found" % KT),
    ("CompressedPublicKey", "%s.decompress(bytes.fromhex('02' + '00' * 32)) raises AssertionError: x is not on the curve" % KT),
    ("Bech32Address", "%s.CHARSET.index('b') raises ValueError: substring not found" % KT),
    ("WalletImportFormat", "%s.wif(2 ** 256) raises OverflowError: int too big to convert" % KT),
    ("ErrorDetection", "%s.segwit_decode('bc', 'bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaef')[0] raises TypeError: 'NoneType' object is not subscriptable" % KT),
]

CQS = [
    "How does a private key become a public key, which constants of the secp256k1 standard does the calculation use, and why can the calculation not be run backwards?",
    "Which encodings can one and the same key or commitment appear in, what does each encoding add, and which first characters does each produce?",
    "Which output script does each kind of address stand for, how is the script built from the address, and how does a node decide whether a spend of it is allowed?",
    "What does the checksum of each address format guarantee, which errors does it fail to catch, and what did the length extension weakness of bech32 change?",
    "Where do the statements and numbers of the 3rd edition's chapter 4 differ from the primary standards and from a run of Bitcoin Core 31.1, and what does each difference change?",
    "Which terms do the explanations of this chapter rely on, and is each one a concept of this chapter or of an earlier chapter?",
]

PROVENANCE = (
    "Concepts are corpus-derived from the 3rd edition's chapter 4 through the Stage 1 research record; the explanations were rewritten for version "
    "1.1.0 from the documents and files listed at the head of this module, each read for this version, and every quotation, number, address, script "
    "and encoding is re-checked by a claim that the chapter builder executes; the supporting concepts (the finite field, the elliptic curve, point "
    "addition, the generator point, the discrete logarithm, the cryptographic library, the hash function, SHA256, RIPEMD-160, HASH160, bits and bytes, "
    "number bases, the QR code, the checksum, the network selector, output and input scripts, the stack machine, the payment to an IP address, the "
    "redeem script, the multisignature script, the preimage, second preimage and collision attacks, the segregated witness upgrade, nested segwit, "
    "the witness version, the witness program, the human-readable part, the BCH code, the length extension weakness, the three witness output kinds, "
    "the deterministic wallet, address reuse, the hardware signing device, the test vectors, cross-checking and the uniform resource identifier) were "
    "added because an audit of the explanations found them used without a concept of their own."
)
TOOLING = "CPython 3.14.4"
DOC_TITLE = "Keys and addresses: chapter 4 of the 3rd edition recomputed from the standards and cross-checked against Bitcoin Core 31.1"
DOC_ABOUT = (
    "This document renews chapter 4 of the 3rd edition by deriving every key, commitment, script and address of the chapter from its own primary "
    "standards with a readable toolkit, and by comparing the result with Bitcoin Core 31.1 and with the reference implementation that the book itself "
    "runs, so that each number the chapter prints is explained, reproduced, and reported where the book and its sources disagree."
)
CHANGE = (
    "1.1.0 rewrites every explanation as four to six paragraphs of continuous prose, keeps every concept identifier of 1.0.0 with its parent, and adds "
    "the concepts the explanations needed (the arithmetic of the curve, the three hash functions, the representations of data, the scripts and the stack "
    "machine, the attacks on short hashes, the parts of a segwit address and the three witness output kinds, the modern practice of wallets, the test "
    "vectors and the uniform resource identifier) that an audit of the terms used found unexplained; it also corrects statements of 1.0.0 that the "
    "primary sources do not support, among them the origin of the secp256k1 curve, so MAJOR in the text and MINOR in the structure; numbered MINOR "
    "because no identifier was removed."
)


def run_checks_inprocess():
    bad = []
    n = 0

    def ev(e):
        return repr(eval(e, {}))

    for e, x in CHECKS:
        n += 1
        try:
            got = ev(e)
        except BaseException as ex:
            got = "EXC %r" % (ex,)
        if got != x:
            bad.append((e[:160], x, got[:200]))
    for nd in NODES:
        if nd[4] and nd[4][2]:
            n += 1
            e, x = nd[4][2]
            try:
                got = ev(e)
            except BaseException as ex:
                got = "EXC %r" % (ex,)
            if got != x:
                bad.append((nd[0], x, got[:200]))
    for e, typ in RAISES:
        n += 1
        try:
            eval(e, {})
            bad.append((e[:160], typ, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != typ:
                bad.append((e[:160], typ, type(ex).__name__))
    for leaf, text in ERRORS:
        n += 1
        e, rest = text.split(" raises ", 1)
        et, msg = rest.split(": ", 1)
        try:
            eval(e, {})
            bad.append((leaf, et, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != et or not str(ex).startswith(msg):
                bad.append((leaf, rest, "%s: %s" % (type(ex).__name__, ex)))
    return n, bad


if __name__ == "__main__":
    import sys
    n, bad = run_checks_inprocess()
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", len(bad))
    for b in bad:
        print("   ", b)
    ids = [x[0] for x in NODES]
    assert len(ids) == len(set(ids)), "duplicate ids: %s" % sorted({i for i in ids if ids.count(i) > 1})
    byid = {x[0]: x for x in NODES}
    for x in NODES:
        assert x[3] is None or x[3] in byid, x[0]
        assert (x[2] == 3) == (x[4] is not None), x[0]
        if x[3]:
            assert byid[x[3]][2] == x[2] - 1 and ids.index(x[3]) < ids.index(x[0]), x[0]
        assert (x[2] == 3 and 4 <= len(x[5]) <= 6) or (x[2] < 3 and 3 <= len(x[5]) <= 6), (x[0], len(x[5]))
        for f, t in x[5]:
            assert t.strip() and len(t.split()) >= 40, (x[0], f, len(t.split()))
    for leaf, owner in OWNERS:
        assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, (leaf, owner)
    for leaf, t in ERRORS:
        assert leaf in byid and byid[leaf][2] == 3, leaf
    print(len(NODES), "concepts;", sum(len(x[5]) for x in NODES), "paragraphs;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words;",
          len(CHECKS) + len(RAISES) + len(ERRORS) + sum(1 for x in NODES if x[4] and x[4][2]), "executed claims")
