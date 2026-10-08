#!/usr/bin/env python3
"""SEN0401 chapter 6 corpus, version 1.0.0: Transactions (chapter 6 of Mastering Bitcoin, 3rd edition), each concept explained in four
paragraphs of continuous prose (what it is, why it matters, how it works, what to watch for) and each group and branch in three or
four, plus the concepts the explanations rely on (the hash function, double SHA-256, the txid and wtxid, relay policy, the consensus
rule, the satoshi, the digest ...), so that no term is used unexplained. The facet name at the start of a paragraph is only the
author's writing guide and is never printed.

Used by sen0401_chapter_build_v1_0_1.py (TBox/ABox/document). This is the chapter's first ontology: there was no earlier version, so
every concept identifier is new. The text is assembled from sen0401_ch06_text_a..h_v1_0_0.py and the shared parts in
sen0401_ch06_common_v1_0_0.py; the executed claims use sen0401_ch06_checklib_v1_0_0.py (source readers) and
sen0401_ch06_tx_lib_v1_0_0.py (the serialization, the identifiers, the weight, the sequence, lock time, dust and subsidy
arithmetic, checked against the chapter's own transaction and against Bitcoin Core's sources by sen0401_ch06_verify_v1_0_0.py).

Sources actually read for this version, in this session, and saved in 08-tooling/ch06-evidence (every saved copy is re-read by a
CHECKS entry): the chapter's source (ch06_transactions.adoc of the bitcoinbook working copy at commit 275c4eb8, the commit the
textbook ontology pins) and, in the same book, chapters 2 and 3 and the glossary; BIPs 30, 34, 62, 65, 68, 112, 113, 125, 141, 143,
144, 174, 370 and 431 (bitcoin/bips); Bitcoin Core's sources at commit 05bc2f5 (consensus.h, amount.h, tx_check.cpp, tx_verify.cpp,
validation.h, transaction.h, policy.h, policy.cpp, rbf.h, script.h, serialize.h, validation.cpp, chain.h, chainparams.cpp) and its
doc/bips.md; and, because no Bitcoin Core node is available in this environment, the raw bytes and the explorer records of four
transactions from mempool.space fetched on 2026-10-08 - Alice's transaction of the chapter, the transaction it spends, the first
bitcoin transaction and the pizza transaction. Every number, identifier, encoding or output quoted is executed in CHECKS or in a
worked example by the chapter builder (python 3.14); quotations are re-read from the saved copies by a CHECKS entry. Where the book
quotes a running node (the weight 569 that bitcoin-cli returned), the course recomputes the figure from the serialization and
compares it with the explorer's record, and says so.
"""
__version__ = "1.0.0"
import sen0401_ch06_text_a_v1_0_0 as A
import sen0401_ch06_text_b_v1_0_0 as B
import sen0401_ch06_text_c_v1_0_0 as C
import sen0401_ch06_text_d_v1_0_0 as D
import sen0401_ch06_text_e_v1_0_0 as E
import sen0401_ch06_text_f_v1_0_0 as F
import sen0401_ch06_text_g_v1_0_0 as G
import sen0401_ch06_text_h_v1_0_0 as H
from sen0401_ch06_common_v1_0_0 import CL, TL, PROG, ALICE

CHAPTER = "06"
NODES = A.NODES_A + B.NODES_B + C.NODES_C + D.NODES_D + E.NODES_E + F.NODES_F + G.NODES_G + H.NODES_H
CHECKS = A.CHECKS_A + B.CHECKS_B + C.CHECKS_C + D.CHECKS_D + E.CHECKS_E + F.CHECKS_F + G.CHECKS_G + H.CHECKS_H

# claims that something fails (executed by the chapter builder)
RAISES = [
 ("bytes.fromhex('zz')", "ValueError"),
 ("int('', 16)", "ValueError"),
 ("(2 ** 63).to_bytes(8, 'little', signed=True)", "OverflowError"),
 ("(0xffffffff + 1).to_bytes(4, 'little')", "OverflowError"),
 ("bytes(36)[36]", "IndexError"),
 ("(lambda T: T.cs_encode(2 ** 64))(%s)" % TL(), "AssertionError"),
 ("(lambda T: T.cs_encode(-1))(%s)" % TL(), "AssertionError"),
 ("(lambda T: T.parse_tx('01000000' + '00' + '00000000'))(%s)" % TL(), "AssertionError"),   # a count of zero inputs
 ("(lambda T: T.parse_tx(%r + '00'))(%s)" % (ALICE, TL()), "AssertionError"),                 # a trailing byte
 ("(lambda T: T.sequence_for(blocks=65536))(%s)" % TL(), "AssertionError"),
 ("(lambda T: T.sequence_for(seconds=65536 * 512))(%s)" % TL(), "AssertionError"),
 ("(lambda T: T.push_encodings(17))(%s)" % TL(), "AssertionError"),
 ("(lambda T: T.with_witness_item(%r, '00', index=1))(%s)" % (ALICE, TL()), "IndexError"),
]

# a concept that is part of, or operates on, another concept of this chapter
OWNERS = [("MarkerByte", "ExtendedFormat"), ("FlagByte", "ExtendedFormat"), ("PreviousTxid", "Outpoint"), ("OutputIndex", "Outpoint"),
          ("InternalByteOrder", "Digest"), ("DisplayByteOrder", "Digest"), ("LengthPrefix", "InputScript"),
          ("Bip125Signal", "OptInRbf"), ("TypeFlag", "Bip68Timelock"), ("DisableFlag", "Bip68Timelock"), ("TimelockMask", "Bip68Timelock"),
          ("Satoshi", "AmountField"), ("AmountRange", "AmountField"), ("DustLimit", "UneconomicalOutput"), ("DataCarrierOutput", "DustLimit"),
          ("PushEncoding", "ThirdPartyMalleability"), ("WitnessProgram", "Segwit"), ("WitnessStructure", "Segwit"),
          ("WitnessStack", "WitnessStructure"), ("WitnessItem", "WitnessStack"), ("LegacyInputWitness", "WitnessStack"),
          ("HeightLock", "LockTimeField"), ("TimeLock", "LockTimeField"), ("MedianTimePast", "TimeLock"),
          ("NullOutpoint", "Coinbase"), ("CoinbaseField", "Coinbase"), ("BlockSubsidy", "BlockReward"), ("MaturityRule", "Coinbase"),
          ("Vbyte", "Weight"), ("WeightFactor", "Weight"), ("Digest", "HashFunction"), ("DoubleSha256", "HashFunction"),
          ("Txid", "DoubleSha256"), ("Wtxid", "DoubleSha256")]

# an error condition of a concept: the expression, the error class and the start of its message, all executed. The page offers these
# programs as repair exercises in the reader's browser, so each one is self-contained: standard library only, no file access and no
# local module.
_E_CS = PROG("def cs(n):\n"
             "    assert 0 <= n <= 0xffffffffffffffff, 'compactSize holds 0 to 2 ** 64 - 1'\n"
             "    return bytes([n]) if n <= 252 else b'\\xfd' + n.to_bytes(2, 'little')\n"
             "result = cs(2 ** 64).hex()")
_E_MARK = PROG("tx = bytes.fromhex('0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000')\n"
               "assert tx[4] == 0 and tx[5] != 0, 'not the extended format: no marker and flag'\n"
               "result = tx[6]")
_E_MASK = PROG("blocks = 65536\n"
               "assert blocks <= 0xffff, 'a relative timelock holds at most 65535 blocks'\n"
               "result = blocks & 0xffff")
_E_CB = PROG("field = bytes.fromhex('03e0e60b') + b'/' + b'x' * 100\n"
             "assert 2 <= len(field) <= 100, 'the coinbase field must be 2 to 100 bytes'\n"
             "result = len(field)")
_E_AMT = PROG("value = 21_000_000 * 100_000_000 + 1\n"
              "assert 0 <= value <= 21_000_000 * 100_000_000, 'the amount is outside the consensus range'\n"
              "result = value")
_E_SEG = PROG("script = bytes.fromhex('0014' + '00' * 20)\n"
              "version = script[0] if script[0] == 0 else script[0] - 0x50\n"
              "assert version == 1, 'expected a segwit version 1 program'\n"
              "result = version")
ERRORS = [("CompactSize", _E_CS + " raises AssertionError: compactSize holds 0 to 2 ** 64 - 1"),
          ("MarkerByte", _E_MARK + " raises AssertionError: not the extended format: no marker and flag"),
          ("TimelockMask", _E_MASK + " raises AssertionError: a relative timelock holds at most 65535 blocks"),
          ("CoinbaseField", _E_CB + " raises AssertionError: the coinbase field must be 2 to 100 bytes"),
          ("AmountRange", _E_AMT + " raises AssertionError: the amount is outside the consensus range"),
          ("WitnessProgram", _E_SEG + " raises AssertionError: expected a segwit version 1 program"),
          ("OutputIndex", "(0xffffffff + 1).to_bytes(4, 'little') raises OverflowError: int too big to convert"),
          ("AmountField", "(2 ** 63).to_bytes(8, 'little', signed=True) raises OverflowError: int too big to convert"),
          ("InputCount", "int('', 16) raises ValueError: invalid literal for int() with base 16"),
          ("PreviousTxid", "bytes.fromhex('zz') raises ValueError: non-hexadecimal number found in fromhex() arg"),
          ("DisplayByteOrder", "{'4ac54180': 'display'}['eb3ae38f'] raises KeyError: 'eb3ae38f'"),
          ("WitnessStack", "bytes.fromhex('0141')[2 + 65] raises IndexError: index out of range")]

CQS = ["What does a Bitcoin transaction ask full nodes to do, and which of its fields carries the pointer, the proof and the new assignment of value?",
       "How is a transaction serialized in the extended and the legacy format, and can every byte of the chapter's example transaction be read back into a named field?",
       "What do the version, the marker and the flag decide about the bytes that follow them, and why are new constraints tied to new version numbers?",
       "Which three meanings has the sequence field carried, and how does BIP68's encoding of a relative timelock work bit by bit?",
       "Why did placing witnesses in the input script make the transaction identifier malleable, and how does segregated witness fix it without a hard fork?",
       "How are weight and vbytes computed, and does the chapter's figure of 569 for Alice's transaction reproduce from the bytes?",
       "Where do the chapter's statements differ from the standards, from Bitcoin Core's sources and from an independent explorer, and what does each difference change?"]

PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 6 through the Stage 1 research record: the chapter's own sections and named terms "
              "first, then the standards it cites (BIP30, BIP34, BIP62, BIP65, BIP68, BIP112, BIP113, BIP125, BIP141, BIP143, BIP144, BIP174, BIP370 and BIP431), "
              "Bitcoin Core's consensus, policy, primitives, script and validation sources at commit 05bc2f5 with its list of implemented proposals, and the raw "
              "bytes and explorer records of four transactions fetched from mempool.space on 2026-10-08; the supporting concepts (the ownership record, the byte "
              "map, the digest and its two byte orders, the satoshi, the hash function, double SHA-256, the txid and wtxid, relay policy and the consensus rule) "
              "were added because an audit of the explanations found them used without a concept of their own.")
TOOLING = "CPython 3.14.6"
DOC_TITLE = "Transactions: chapter 6 of the 3rd edition read byte by byte and recomputed from the standards and Bitcoin Core's sources"
DOC_ABOUT = "This document renews chapter 6 of the 3rd edition by parsing the chapter's own example transaction field by field with the standard library, recomputing every identifier, weight, encoding and limit it prints from the standards and from Bitcoin Core's sources at a pinned commit, and comparing the result with the book's text and with an independent explorer's record."
CHANGE = ("1.0.0 is the first ontology of chapter 6: 115 concepts in eight branches, each level 3 concept explained in four paragraphs of continuous prose and "
          "each level 1 or 2 group in three or four, with the terms the explanations rely on added as concepts of their own so that nothing is used unexplained; "
          "every quoted number, identifier, encoding and output is executed by the chapter builder, and every quotation is re-read from a saved copy of its "
          "source by an executed claim.")


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
