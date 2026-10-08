#!/usr/bin/env python3
"""Shared parts of the SEN0401 chapter 6 corpus (version 1.0.0): the writing-guide facets, the citation markers, the
source list (one entry per source read; the research record is generated from it) and the builders of the executed
claims. Used by sen0401_ch06_text_*_v1_0_0.py and sen0401_ch06_corpus_v1_0_0.py. Python standard library only.
Follows chapter 5's sen0401_ch05_common_v1_0_0.py; the sources are this chapter's."""
__version__ = "1.0.0"
import os
HERE = os.path.dirname(os.path.abspath(__file__))
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"

GH = "https://raw.githubusercontent.com/"
CORE_C = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
BOOK_C = "275c4eb8eab8800c6adc39f8def8e8f8fa356a57"
_core = lambda f: GH + "bitcoin/bitcoin/" + CORE_C + "/" + f
# (marker, author-year string, label of the publication, url, role, saved copy, one entry per source read)
SOURCES = [
 ("AH", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 6, Transactions (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8)", GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/ch06_transactions.adoc", "primary", "ev:book_ch06_transactions.adoc"),
 ("AH2", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 2, How Bitcoin Works: Alice's payment to Bob, the UTXO and the transaction chain (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/ch02_overview.adoc", "secondary", "book:ch02_overview.adoc"),
 ("AH3", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 3, Bitcoin Core: exploring and decoding transactions with getrawtransaction (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/ch03_bitcoin-core.adoc", "secondary", "book:ch03_bitcoin-core.adoc"),
 ("AHG", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)", GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/glossary.asciidoc", "secondary", "book:glossary.asciidoc"),
 ("B30", "Wuille, 2012", "BIP30, Duplicate transactions, the BIPs repository (Wuille, 2012), status Final", GH + "bitcoin/bips/master/bip-0030.mediawiki", "secondary", "ev:bip-0030.mediawiki"),
 ("B34", "Andresen, 2012", "BIP34, Block v2, Height in Coinbase, the BIPs repository (Andresen, 2012), status Final", GH + "bitcoin/bips/master/bip-0034.mediawiki", "secondary", "ev:bip-0034.mediawiki"),
 ("B62", "Wuille, 2014", "BIP62, Dealing with malleability, the BIPs repository (Wuille, 2014), status Closed", GH + "bitcoin/bips/master/bip-0062.mediawiki", "secondary", "ev:bip-0062.mediawiki"),
 ("B65", "Todd, 2014", "BIP65, OP_CHECKLOCKTIMEVERIFY, the BIPs repository (Todd, 2014), status Final", GH + "bitcoin/bips/master/bip-0065.mediawiki", "secondary", "ev:bip-0065.mediawiki"),
 ("B68", "Friedenbach et al., 2015", "BIP68, Relative lock-time using consensus-enforced sequence numbers, the BIPs repository (Friedenbach, BtcDrak, Dorier and kinoshitajona, 2015), status Final", GH + "bitcoin/bips/master/bip-0068.mediawiki", "secondary", "ev:bip-0068.mediawiki"),
 ("B112", "BtcDrak et al., 2015", "BIP112, CHECKSEQUENCEVERIFY, the BIPs repository (BtcDrak, Friedenbach and Lombrozo, 2015), status Final", GH + "bitcoin/bips/master/bip-0112.mediawiki", "secondary", "ev:bip-0112.mediawiki"),
 ("B113", "Lombrozo, 2015", "BIP113, Median time-past as endpoint for lock-time calculations, the BIPs repository (Lombrozo, 2015), status Final", GH + "bitcoin/bips/master/bip-0113.mediawiki", "secondary", "ev:bip-0113.mediawiki"),
 ("B125", "Harding and Todd, 2015", "BIP125, Opt-in Full Replace-by-Fee Signaling, the BIPs repository (Harding and Todd, 2015), status Final", GH + "bitcoin/bips/master/bip-0125.mediawiki", "secondary", "ev:bip-0125.mediawiki"),
 ("B141", "Lombrozo et al., 2015", "BIP141, Segregated Witness (Consensus layer), the BIPs repository (Lombrozo, Lau and Wuille, 2015), status Final", GH + "bitcoin/bips/master/bip-0141.mediawiki", "secondary", "ev:bip-0141.mediawiki"),
 ("B143", "Lau and Wuille, 2016", "BIP143, Transaction Signature Verification for Version 0 Witness Program, the BIPs repository (Lau and Wuille, 2016), status Final", GH + "bitcoin/bips/master/bip-0143.mediawiki", "secondary", "ev:bip-0143.mediawiki"),
 ("B144", "Lombrozo and Wuille, 2016", "BIP144, Segregated Witness (Peer Services), the BIPs repository (Lombrozo and Wuille, 2016), status Final", GH + "bitcoin/bips/master/bip-0144.mediawiki", "secondary", "ev:bip-0144.mediawiki"),
 ("B174", "Chow, 2017", "BIP174, Partially Signed Bitcoin Transaction Format, the BIPs repository (Chow, 2017), status Final", GH + "bitcoin/bips/master/bip-0174.mediawiki", "secondary", "ev:bip-0174.mediawiki"),
 ("B370", "Chow, 2021", "BIP370, PSBT Version 2, the BIPs repository (Chow, 2021), status Draft", GH + "bitcoin/bips/master/bip-0370.mediawiki", "secondary", "ev:bip-0370.mediawiki"),
 ("B431", "Zhao and Garlick, 2024", "BIP431, Topology Restrictions for Pinning, the BIPs repository (Zhao and Garlick, 2024), status Draft", GH + "bitcoin/bips/master/bip-0431.mediawiki", "secondary", "ev:bip-0431.mediawiki"),
 ("BCC", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/consensus/consensus.h, the consensus constants (block weight, coinbase maturity, witness scale factor) (Bitcoin Core, 2026)", _core("src/consensus/consensus.h"), "secondary", "ev:core_src_consensus_consensus.h"),
 ("BCA", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/consensus/amount.h, COIN and MAX_MONEY (Bitcoin Core, 2026)", _core("src/consensus/amount.h"), "secondary", "ev:core_src_consensus_amount.h"),
 ("BCT", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/consensus/tx_check.cpp, CheckTransaction - the context-free rules of a transaction (Bitcoin Core, 2026)", _core("src/consensus/tx_check.cpp"), "secondary", "ev:core_src_consensus_tx_check.cpp"),
 ("BCV", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/consensus/tx_verify.cpp, IsFinalTx, CalculateSequenceLocks and the maturity check (Bitcoin Core, 2026)", _core("src/consensus/tx_verify.cpp"), "secondary", "ev:core_src_consensus_tx_verify.cpp"),
 ("BCX", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/primitives/transaction.h, CTxIn, CTxOut, CTransaction and the sequence constants (Bitcoin Core, 2026)", _core("src/primitives/transaction.h"), "secondary", "ev:core_src_primitives_transaction.h"),
 ("BCP", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/policy/policy.h and policy.cpp, the relay policy - dust, standardness, version limits (Bitcoin Core, 2026)", _core("src/policy/policy.cpp"), "secondary", "ev:core_src_policy_policy.cpp"),
 ("BCS", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/script/script.h, LOCKTIME_THRESHOLD, MAX_SCRIPT_SIZE and the opcodes (Bitcoin Core, 2026)", _core("src/script/script.h"), "secondary", "ev:core_src_script_script.h"),
 ("BCL", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/validation.cpp, GetBlockSubsidy and the block reward check (Bitcoin Core, 2026)", _core("src/validation.cpp"), "secondary", "ev:core_src_validation.cpp"),
 ("BCW", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/consensus/validation.h, GetTransactionWeight and GetBlockWeight (Bitcoin Core, 2026)", _core("src/consensus/validation.h"), "secondary", "ev:core_src_consensus_validation.h"),
 ("BCH", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/chain.h, GetMedianTimePast over eleven blocks (Bitcoin Core, 2026)", _core("src/chain.h"), "secondary", "ev:core_src_chain.h"),
 ("BCK", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/kernel/chainparams.cpp, the mainnet activation heights and the halving interval (Bitcoin Core, 2026)", _core("src/kernel/chainparams.cpp"), "secondary", "ev:core_src_kernel_chainparams.cpp"),
 ("BCR", "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: src/serialize.h, the compactSize reader and writer (Bitcoin Core, 2026)", _core("src/serialize.h"), "secondary", "ev:core_src_serialize.h"),
 ("BCD", "Bitcoin Core, 2026", "Bitcoin Core documentation: doc/bips.md at commit 05bc2f5, the proposals the project implements and when (Bitcoin Core, 2026)", _core("doc/bips.md"), "secondary", "ev:core_doc_bips.md"),
 ("BCN", "Bitcoin Core, 2026", "Bitcoin Core documentation: doc/release-notes/release-notes-28.0.md at commit 05bc2f5, the release that made full replace-by-fee the default and version 3 transactions standard (Bitcoin Core, 2026)", _core("doc/release-notes/release-notes-28.0.md"), "secondary", "ev:core_doc_release-notes_release-notes-28.0.md"),
 ("AL", "Altunel, 2021", "Course notes: Chapter_6_Transactions.pptx, SEN0401 (then CSE0469) Blockchain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; the owner's file in 03-materials/owner-legacy-2025 (sha256 6e3641bffec0c7ee)", "urn:sen0401:course-notes:Chapter_6_Transactions.pptx:6e3641bffec0c7ee", "secondary", "file:../03-materials/owner-legacy-2025/slides-2025/Chapter_6_Transactions_v1_0_0.pptx"),
 ("MP", "mempool.space, 2026", "mempool.space, an open-source block explorer: the raw hex and the JSON record of Alice's transaction, of the transaction it spends, of the first bitcoin transaction and of the pizza transaction, fetched 2026-10-08 (mempool.space, 2026)", "https://mempool.space/api/tx/466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177", "secondary", "ev:mempool_tx_466200308696215b_v1_0_0.json"),
]
CITE = {s[0]: s[1] for s in SOURCES}
_MARK = dict(CITE); _MARK.update({"AH2": CITE["AH"], "AH3": CITE["AH"], "AHG": CITE["AH"]})
def c(t):
    for k in sorted(_MARK, key=len, reverse=True): t = t.replace(" [" + k + "]", " (" + _MARK[k] + ")")
    import re
    bad = re.findall(r" \[[A-Z0-9]{2,5}\]", t)
    assert not bad, (bad, t[:120])
    return t
def P(*items):
    """paragraph list: items are (facet, text) pairs; markers are resolved"""
    return [(f, c(t)) for f, t in items]

# ---- builders of the executed claims (each result is an expression the chapter builder evaluates alone in a fresh interpreter) ----
_LIBS = "__import__('sys').path.insert(0, %r)" % HERE
def _CL(): return "(%s or __import__('sen0401_ch06_checklib_v1_0_0'))" % _LIBS
def _TL(): return "(%s or __import__('sen0401_ch06_tx_lib_v1_0_0'))" % _LIBS
def Qb(name, *phrases): return ("%s.has_book(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")      # phrases in a chapter of the book
def Qe(name, *phrases): return ("%s.has_ev(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")        # phrases in a source saved in ch06-evidence
def Qc(path, *phrases): return ("%s.has_core(%r%s)" % (_CL(), path, "".join(", %r" % p for p in phrases)), "True")        # in a file of Bitcoin Core at the pinned commit
def X(expr, expected):
    """an executed claim: expr is evaluated with T = the chapter 6 transaction library and C = the check library"""
    return ("(lambda T, C: %s)(%s, %s)" % (expr, _TL(), _CL()), expected if isinstance(expected, str) else repr(expected))
CL, TL = _CL, _TL
def Pp(name, *phrases): return ("%s.has_pptx(%r%s)" % (_CL(), "../03-materials/owner-legacy-2025/slides-2025/" + name, "".join(", %r" % p for p in phrases)), "True")   # the owner's 2021 slides
def PROG(code, var="result"):
    """a small program (several statements) as one expression: its variable `result`. The page runs a worked example in the
    reader's browser, so such a program uses the standard library only and reads no files."""
    return "(lambda g: (exec(%r, g), g[%r])[1])({})" % (code, var)

# the chapter's own transaction (Alice's payment to Bob, the book's listing), as the book prints it and as the explorer returned it
ALICE = ("01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba"
         "4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe"
         "2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000")
ALICE_TXID = "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"
PREV_INTERNAL = "eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a"
PREV_DISPLAY = "4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb"
LEGACY_INPUT_SCRIPT = ("483045022100a6cc4e8cd0847951a71fad3bc9b14f24d44ba59d19094e0a8cfa2580bb664b020220366060ea8203d766722ed0a02d1599b99d3c95b97dab8e"
                       "41d3e4d3fe33a5706201210369e03e2c91f0badec46c9c903d9e9edae67c167b9ef9b550356ee791c9a40896")   # the book's 107-byte example, after its 0x6b prefix
# a compact double-SHA-256 and a compactSize reader, written out so that a worked example can run in the browser without the library
H256 = "import hashlib\nh256 = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()\n"
CSREAD = ("def cs(b, p):\n"
          "    f = b[p]\n"
          "    if f <= 252: return f, 1\n"
          "    n = {0xfd: 2, 0xfe: 4, 0xff: 8}[f]\n"
          "    return int.from_bytes(b[p + 1:p + 1 + n], 'little'), 1 + n\n")
