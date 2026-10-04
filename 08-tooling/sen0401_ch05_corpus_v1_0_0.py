#!/usr/bin/env python3
"""SEN0401 chapter 5 corpus, version 1.0.0: Wallet Recovery (chapter 5 of Mastering Bitcoin, 3rd edition), each concept explained in four to six
paragraphs of continuous prose (what it is, why it matters, where it is met, how it works, what to watch for), plus the concepts the explanations
rely on (the hash function, the SHA family, the digital signature, secret sharing, entropy, the key-stretching function, the salt, multisignature,
the output script, encryption, the Lightning Network ...), so that no term is used unexplained. The facet name at the start of a paragraph is only
the author's writing guide and is never printed.

Used by sen0401_chapter_build_v1_0_0.py (TBox/ABox/document). This is the chapter's first ontology: there was no earlier version, so every concept
identifier is new. The text is assembled from sen0401_ch05_text_a..h_v1_0_0.py and the shared parts in sen0401_ch05_common_v1_0_0.py; the executed
claims use sen0401_ch05_checklib_v1_0_0.py (source readers) and sen0401_ch05_wallet_lib_v1_1_0.py (the arithmetic and encodings of wallet recovery,
checked against published vectors by sen0401_ch05_verify_v1_1_0.py).

Sources actually read for this version, in this session, and saved in 08-tooling/ch05-evidence (every saved copy is re-read by a CHECKS entry):
the chapter's source (ch05_wallets.adoc of the bitcoinbook working copy, tag third_edition_print1) and, in the same book, the glossary, appendix C
and the sections of chapters 7 and 14 on multisignature and on payment channels; BIPs 32, 39, 43, 44, 49, 84, 86, 93, 329, 379, 380 and 389
(bitcoin/bips); SLIP-0039 and SLIP-0044 (satoshilabs/slips); the Electrum Seed Version System; lnd's aezeed README and its recovery document;
Muun's recovery tool README; BTCPay Server's README; Jameson Lopp's list of known physical attacks; the BIP39 test vectors of trezor/python-mnemonic;
RFC 2104 (HMAC), RFC 7914 (scrypt) and RFC 8018 (PBKDF2); the hashlib documentation of CPython 3.14.4; Bitcoin Core's doc/bips.md and
doc/descriptors.md and the wallet sources wallet.h, walletutil.h and scriptpubkeyman.h at commit 05bc2f5; the evidence files of the run of
Bitcoin Core 31.1 (08-tooling/ch05-evidence, made on 2026-10-02: descriptors, a fresh wallet, the BIP84 vector through deriveaddresses, and the
option and RPC help); and the owner's 2021 course notes Chapter_5_Wallets.pptx. Every number, hash, address, encoding or output quoted is executed
in CHECKS or in a worked example by the chapter builder (python 3.14); quotations are re-read from the saved copies by a CHECKS entry.
"""
__version__ = "1.0.0"
import sen0401_ch05_text_a_v1_0_0 as A
import sen0401_ch05_text_b_v1_0_0 as B
import sen0401_ch05_text_c_v1_0_0 as C
import sen0401_ch05_text_d_v1_0_0 as D
import sen0401_ch05_text_e_v1_0_0 as E
import sen0401_ch05_text_f_v1_0_0 as F
import sen0401_ch05_text_g_v1_0_0 as G
import sen0401_ch05_text_h_v1_0_0 as H
from sen0401_ch05_common_v1_0_0 import CL, WL, PROG, PBKDF2

CHAPTER = "05"
NODES = A.NODES_A + B.NODES_B + C.NODES_C + D.NODES_D + E.NODES_E + F.NODES_F + G.NODES_G + H.NODES_H
CHECKS = A.CHECKS_A + B.CHECKS_B + C.CHECKS_C + D.CHECKS_D + E.CHECKS_E + F.CHECKS_F + G.CHECKS_G + H.CHECKS_H

# claims that something fails (executed by the chapter builder)
RAISES = [
 ("bytes.fromhex('abc')", "ValueError"),
 ("int('zz', 16)", "ValueError"),
 ("int('', 2)", "ValueError"),
 ("(2 ** 32).to_bytes(4, 'big')", "OverflowError"),
 ("__import__('hashlib').pbkdf2_hmac('sha512', 'words', b'mnemonic', 2048)", "TypeError"),
 ("__import__('hmac').new('key', b'message', 'sha512')", "TypeError"),
 ("__import__('unicodedata').normalize('NFKX', 'e')", "ValueError"),
 ("pow(0, -1, 10)", "ValueError"),
 ("(lambda W: W.ckd_pub(W.ec_mul(5), bytes(32), 2 ** 31))(%s)" % WL(), "AssertionError"),
 ("(lambda W: W.entropy_to_mnemonic(bytes(10)))(%s)" % WL(), "AssertionError"),
 ("(lambda W: W.mnemonic_to_entropy('army van defense carry jealous true garbage claim echo media make notaword'))(%s)" % WL(), "ValueError"),
 ("(lambda W: W.b58check_decode('xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9d'))(%s)" % WL(), "AssertionError"),
 ("(lambda W: W.parse_extended('xprv9tyUQV64JT5qs'))(%s)" % WL(), "AssertionError"),
 ("(lambda W: W.shamir_split(5, 3, 5, [1]))(%s)" % WL(), "AssertionError"),
]

# a concept that is part of, or operates on, another concept of this chapter
OWNERS = [("Bip39Checksum", "Bip39Code"), ("WordList", "Bip39Code"), ("BitSegment", "Bip39Code"), ("Bip39Passphrase", "Bip39Code"),
          ("CodeLength", "Bip39Code"), ("WalletBirthday", "AezeedCode"), ("Salt", "Pbkdf2"), ("Pbkdf2", "KeyStretchingFunction"),
          ("MasterPrivateKey", "RootSeed"), ("MasterChainCode", "RootSeed"), ("ChainCode", "ExtendedKey"), ("KeyFingerprint", "ExtendedKey"),
          ("IndexNumber", "ChildKeyDerivation"), ("HardenedDerivation", "ChildKeyDerivation"), ("PrivateChildDerivation", "ChildKeyDerivation"),
          ("PublicChildDerivation", "ChildKeyDerivation"), ("DescriptorChecksum", "OutputScriptDescriptor"), ("KeyOrigin", "OutputScriptDescriptor"),
          ("MultipathDescriptor", "OutputScriptDescriptor"), ("GapLimit", "XpubDeployment"), ("StaticChannelBackup", "LightningNetwork"),
          ("AddressLabel", "WalletDatabase"), ("TransactionLabel", "WalletDatabase"), ("AccountBranch", "Bip44Structure"),
          ("ChangeBranch", "Bip44Structure"), ("AddressIndex", "Bip44Structure"), ("Bip43Purpose", "Bip44Structure")]

# an error condition of a concept: the expression, the error class and the start of its message, all executed
# an error condition of a concept: the expression, the error class and the start of its message, all executed. The page offers these programs as
# repair exercises in the reader's browser, so each one is self-contained: standard library only, no file access and no local module.
_E_WORD = PROG("words = 'abandon ability able about above absent'.split()\n"
               "word = 'notaword'\n"
               "assert word in words, 'the word is not in the list'\n"
               "result = words.index(word)")
_E_PUB = PROG("i = 2 ** 31\n"
              "assert i < 2 ** 31, 'no public derivation of a hardened child'\n"
              "result = i")
_E_B58 = PROG("import hashlib\n"
              "B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\n"
              "t = 'xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9d'\n"
              "n = 0\n"
              "for ch in t: n = n * 58 + B58.index(ch)\n"
              "raw = n.to_bytes(82, 'big')\n"
              "assert hashlib.sha256(hashlib.sha256(raw[:-4]).digest()).digest()[:4] == raw[-4:], 'checksum does not match'\n"
              "result = raw[:4].hex()")
_E_PB = PROG(PBKDF2 + "result = seed(b'army van defense', 'mnemonic')")   # the salt has to be bytes, not text
ERRORS = [("WordList", _E_WORD + " raises AssertionError: the word is not in the list"),
          ("PublicChildDerivation", _E_PUB + " raises AssertionError: no public derivation of a hardened child"),
          ("ExtendedKeyEncoding", _E_B58 + " raises AssertionError: checksum does not match"),
          ("Pbkdf2", _E_PB + " raises TypeError: can only concatenate str"),
          ("IndexNumber", "(2 ** 32).to_bytes(4, 'big') raises OverflowError: int too big to convert"),
          ("TextNormalization", "__import__('unicodedata').normalize('NFKX', 'e') raises ValueError: invalid normalization form"),
          ("BitSegment", "int('', 2) raises ValueError: invalid literal for int() with base 2"),
          ("HmacSha512", "__import__('hmac').new('key', b'message', 'sha512') raises TypeError: key: expected bytes or bytearray")]

CQS = ["What does a Bitcoin wallet actually contain, and which of its contents can be recomputed from a seed and which cannot?",
       "How is a BIP39 recovery code generated from entropy and turned into a seed, and can every number the chapter prints be reproduced?",
       "How does BIP32 make a tree of keys from one seed, and what can the holder of an extended public key do and not do?",
       "Which recovery code schemes are in use, what does each add over BIP39, and what does each cost its user?",
       "Which derivation paths does a wallet use, how are they recorded implicitly or explicitly, and what does a descriptor say that a seed cannot?",
       "Where do the chapter's statements differ from the standards and from Bitcoin Core 31.1, and what does each difference change?",
       "Which terms do the explanations of this chapter rely on, and is each one a concept of this chapter or of an earlier chapter?"]

PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 5 through the Stage 1 research record: the chapter's own sections and named terms "
              "first, then the standards it cites (BIP32, BIP39, BIP43, BIP44, BIP49, BIP84, BIP86, BIP93, BIP329, BIP379, BIP380, BIP389, SLIP-0039 and "
              "SLIP-0044), the documents of the wallets it names (Electrum, lnd's aezeed and recovery notes, Muun's recovery tool, BTCPay Server), the "
              "specifications of the functions it uses (RFC 2104, RFC 7914, RFC 8018), Bitcoin Core's documentation and wallet sources at commit 05bc2f5 "
              "with the evidence of a run of release 31.1, and the owner's 2021 course notes; the supporting concepts (the hash function, the SHA family, "
              "the digital signature, secret sharing, encryption, multisignature, the output script, the Lightning Network, data loss and the testing of a "
              "backup) were added because an audit of the explanations found them used without a concept of their own.")
TOOLING = "CPython 3.14.4"
DOC_TITLE = "Wallet recovery: chapter 5 of the 3rd edition recomputed from the standards and checked against Bitcoin Core 31.1"
DOC_ABOUT = "This document renews chapter 5 of the 3rd edition by recomputing every number, code, key and address it prints from the standards that define them and by comparing the result with what Bitcoin Core 31.1 and the wallets the chapter names actually do."
CHANGE = ("1.0.0 is the first ontology of chapter 5: 111 concepts in eight branches, each level 3 concept explained in four to six paragraphs of continuous "
          "prose and each level 1 or 2 group in three, with the terms the explanations rely on added as concepts of their own so that nothing is used "
          "unexplained; every quoted number, hash, code, key, address, encoding and output is executed by the chapter builder, and every quotation is "
          "re-read from a saved copy of its source by an executed claim.")


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
            bad.append((e[:160], x, got))
    for nd in NODES:
        if nd[4] and nd[4][2]:
            n += 1
            e, x = nd[4][2]
            try:
                got = ev(e)
            except BaseException as ex:
                got = "EXC %r" % (ex,)
            if got != x:
                bad.append((nd[0], x, got))
    for e, typ in RAISES:
        n += 1
        try:
            eval(e, {})
            bad.append((e[:120], typ, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != typ:
                bad.append((e[:120], typ, type(ex).__name__))
    for leaf, text in ERRORS:
        n += 1
        e, rest = text.split(" raises ", 1)
        et, msg = rest.split(": ", 1) if ": " in rest else (rest, "")
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
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", bad)
    ids = [x[0] for x in NODES]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    byid = {x[0]: x for x in NODES}
    for x in NODES:
        assert x[3] is None or x[3] in byid, x[0]
        assert (x[2] == 3) == (x[4] is not None), x[0]
        if x[3]:
            assert byid[x[3]][2] == x[2] - 1 and ids.index(x[3]) < ids.index(x[0]), x[0]
        assert (x[2] == 3 and 4 <= len(x[5]) <= 6) or (x[2] < 3 and 3 <= len(x[5]) <= 6), (x[0], len(x[5]))
        for f, t in x[5]:
            assert "[" not in t or "[" in t.replace("[0]", ""), (x[0], t[:80])
    for leaf, owner in OWNERS:
        assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, (leaf, owner)
    for leaf, t in ERRORS:
        assert leaf in byid and byid[leaf][2] == 3, leaf
    tops = [x[0] for x in NODES if x[2] == 1]
    print(len(NODES), "concepts;", len(tops), "branches;", sum(1 for x in NODES if x[2] == 2), "groups;",
          sum(1 for x in NODES if x[2] == 3), "concept sections;", sum(len(x[5]) for x in NODES), "paragraphs;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words;", len(CHECKS) + len(RAISES) + len(ERRORS), "checks;",
          sum(1 for x in NODES if x[4] and x[4][2]), "worked examples")
    print("branches:", ", ".join(tops))
