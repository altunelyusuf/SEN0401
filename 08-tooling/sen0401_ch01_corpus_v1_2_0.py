#!/usr/bin/env python3
"""SEN0401 chapter 1 corpus, version 1.2.0: the Introduction (chapter 1 of Mastering Bitcoin, 3rd edition), with every concept explained in
four to six paragraphs of continuous prose (what it is, why it matters, where it is met, how it works, what to watch for), plus the concepts
the explanations rely on (hash function, digital signature, public-key cryptography, private key, entropy, checksum, key stretching, block,
blockchain, timestamp, node, internet, protocol, HTTP, browser, server, API, URI, QR code, database, operating system, distributed system,
bits and bytes, malware, phishing, transaction, inputs and outputs, fee, confirmation, irreversibility, offchain payment, payment channel,
the Lightning Network, electronic payment, privacy, the block subsidy, difficulty adjustment, mining, Hashcash, the Byzantine Generals'
Problem, the central bank, the clearing house, identity verification, the volume-weighted average, W3C Recommendations and others), so that
no term the chapter uses is left without a concept of its own. The facet name at the head of a paragraph tuple is only the author's writing
guide and is never printed.

Read by sen0401_chapter_build_v1_0_0.py (TBox, ABox, document). Every concept identifier of version 1.1.0 is kept with its parent; the new
concepts and the new subject groups are added beside them.

Sources actually read for this version, in this session, and saved in 08-tooling/ch01-sources: the chapter's own source
(ch01_intro.adoc of the bitcoinbook working copy) and, in the same book, chapters 2, 4, 9 and 10, the glossary and appendix C (the BIP list);
Nakamoto's paper (appendix A and the PDF from bitcoin.org); Back's Hashcash paper; Lamport, Shostak and Pease on the Byzantine Generals'
Problem; Poon and Dryja on the Lightning Network; BIP 21 and BIP 39 (bitcoin/bips); the Bitcoin wiki page on the controlled supply; the
Bitcoin Core source files amount.h, validation.cpp, chainparams.cpp, pow.cpp and params.h at the checked-out commit; RFC 4949 (the Internet
Security Glossary), RFC 6234 (SHA), RFC 8018 (PBKDF2), RFC 4648 (base 16, 32 and 64), RFC 3986 (URI) and RFC 9112 (HTTP/1.1); the W3C
Recommendations Decentralized Identifiers v1.0 and Verifiable Credentials Data Model v2.0 and the W3C 'About' page; the Open Source
Definition (opensource.org); the Mozilla Developer Network glossary entries for the internet, protocols, HTTP, browsers, servers, APIs,
URIs, databases and cryptography; Wikipedia articles on QR codes, operating systems, distributed systems, malware, phishing, pseudonyms,
deflation, hashes and the World Wide Web Consortium; and the public block data of block 0 and block 840000 saved from the Blockstream API.
Every number, hash, date, encoding or output quoted is executed by the chapter builder, and every sentence quoted from a source is re-read
from the saved copy by a check, so a wrong figure or a misquotation stops the build.
"""
__version__ = "1.2.0"
import os, re, ast, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sen0401_ch01_common_v1_2_0 import W, Y, E, H, K, c as _c, has as _has, rd as _rd, js as _js, prog as _prog, SRC as _SRC
from sen0401_ch01_text_a_v1_2_0 import NODES_A
from sen0401_ch01_text_b_v1_2_0 import NODES_B
from sen0401_ch01_text_c_v1_2_0 import NODES_C
from sen0401_ch01_text_d_v1_2_0 import NODES_D
from sen0401_ch01_text_e_v1_2_0 import NODES_E
from sen0401_ch01_srcchecks_a_v1_2_0 import SRC_A
from sen0401_ch01_srcchecks_b_v1_2_0 import SRC_B
from sen0401_ch01_srcchecks_c_v1_2_0 import SRC_C
from sen0401_ch01_numchecks_v1_2_0 import NUM

CHAPTER = "01"

# ---------------------------------------------------------------------------------------------------------------------
# the concepts, in document order: Money, Network, Wallet, Usage, Foundations, Nature
# (id, label or None for the camel-case label, level, parent, leaf, paras); leaf = (example label, definition, io or None)
# ---------------------------------------------------------------------------------------------------------------------
NODES = NODES_A + NODES_B + NODES_C + NODES_D + NODES_E

# ---- the worked examples run in the reader's browser as well as here, so a program that reads a file of this computer
# ---- gets the text of that file put into the program itself: the page and the builder then run the same program.
_OPENJ = re.compile(r"__import__\('json'\)\.load\(open\((%s)\)\)" % r"'[^']*'")
def _inline(code):
    def f(m):
        return "__import__('json').loads(%r)" % open(ast.literal_eval(m.group(1)), encoding="utf-8").read()
    return _OPENJ.sub(f, code)
NODES = [(n[0], n[1], n[2], n[3],
          (n[4][0], n[4][1], (_inline(n[4][2][0]), n[4][2][1])) if n[4] and n[4][2] else n[4],
          n[5]) for n in NODES]
# the citation tokens become the author-year strings that the research record resolves
NODES = [(n[0], n[1], n[2], n[3], n[4], [(f, _c(t)) for f, t in n[5]]) for n in NODES]

# ---------------------------------------------------------------------------------------------------------------------
# the claims: every sentence quoted from a source, re-read from the saved copy, and every number the prose states
# ---------------------------------------------------------------------------------------------------------------------
CHECKS = [(_has(f, *pieces), "True") for node, f, pieces in SRC_A + SRC_B + SRC_C] + list(NUM)

RAISES = [
 ("bytes.fromhex('abc')", "ValueError"),                                   # a hash is an even number of hexadecimal digits
 ("bytes.fromhex('0g')", "ValueError"),
 ("__import__('hashlib').sha256('abc')", "TypeError"),                     # a hash function takes bytes, not text
 ("int('21,000,000')", "ValueError"),                                      # an amount with thousands separators is not a number
 ("__import__('decimal').Decimal('zero')", "InvalidOperation"),
 ("(50 * 10**8) >> -1", "ValueError"),                                      # a halving count is never negative
 ("__import__('json').loads('{')", "JSONDecodeError"),
 ("'nephew dog crane'.split()[11]", "IndexError"),                          # a recovery code of three words has no twelfth word
 ("__import__('hashlib').pbkdf2_hmac('sha512', 'abandon', b'mnemonic', 2048)", "TypeError"),
 ("(2 ** 32).to_bytes(4, 'little')", "OverflowError"),                      # a block time does not fit in four bytes for ever
]

OWNERS = [("SatoshiUnit", "BitcoinUnit"), ("Halving", "SupplyCap"), ("BlockSubsidy", "Halving"),
          ("VolumeWeightedAverage", "FloatingExchangeRate"), ("ProofOfWork", "Mining"), ("DifficultyAdjustment", "Mining"),
          ("Checksum", "RecoveryCode"), ("KeyStretching", "RecoveryCode"), ("Entropy", "RecoveryCode"), ("KeyedHash", "KeyStretching"),
          ("PrivateKey", "BitcoinAddress"), ("DigitalSignature", "Transaction"), ("InputsAndOutputs", "Transaction"),
          ("TransactionFee", "Transaction"), ("Block", "Confirmation"), ("Timestamp", "Block"),
          ("HashFunction", "Blockchain"), ("QrCode", "Invoice"), ("Uri", "Invoice"),
          ("PaymentChannel", "OffchainPayment"), ("LightningNetwork", "PaymentChannel"),
          ("Phishing", "RecoveryCode"), ("Malware", "RecoveryCode"), ("IdentityVerification", "CurrencyExchange")]

ERRORS = [
 ("BitsAndBytes", "bytes.fromhex('abc') raises ValueError: fromhex() arg must contain an even number of hexadecimal digits"),
 ("HashFunction", "__import__('hashlib').sha256('abc') raises TypeError: Strings must be encoded before hashing"),
 ("SatoshiUnit", "int('21,000,000') raises ValueError: invalid literal for int() with base 10"),
 ("Halving", "(50 * 10**8) >> -1 raises ValueError: negative shift count"),
 ("RecoveryCode", "'nephew dog crane'.split()[11] raises IndexError: list index out of range"),
 ("KeyStretching", "__import__('hashlib').pbkdf2_hmac('sha512', 'abandon', b'mnemonic', 2048) raises TypeError: a bytes-like object is required"),
 ("Timestamp", "(2 ** 32).to_bytes(4, 'little') raises OverflowError: int too big to convert"),
 ("Database", "{'addr1': 'Alice'}['addr3'] raises KeyError: 'addr3'"),
]

CQS = [
 "What is the unit of Bitcoin's currency, how far can it be divided, how much of it will ever exist, and which rule produces that total?",
 "Who creates new bitcoin, on what schedule, and in what sense does the arrangement replace the functions of a central bank?",
 "Which problem of earlier digital money does Bitcoin solve, and which of its four parts answers which part of that problem?",
 "How can a wallet be classified by platform, by autonomy and by the control of keys, and what does each choice cost its user?",
 "What happens, step by step and object by object, between the moment Joe presses Send and the moment Alice's payment is confirmed?",
 "Which technical terms does the chapter use without defining them, and what is the smallest correct explanation of each?",
 "Which figures of the chapter are rules of the protocol and which are values at a date, and how can each be recomputed?",
]

PROVENANCE = ("Concepts are corpus-derived from the 3rd edition's chapter 1 through the Stage 1 research record; the explanations were rewritten for "
              "version 1.2.0 from the documents and files listed at the head of this module, each read for this version, with every quotation re-read "
              "from its saved copy and every number recomputed by a claim that the builder executes; the supporting concepts (the cryptographic "
              "primitives, the parts of the chain, the everyday computing terms, the two threats, the objects of a payment and the standards bodies) "
              "were added because an audit of the terms used in the explanations found them used without a concept of their own.")

TOOLING = "CPython 3.14.4"
DOC_TITLE = "Introduction to Bitcoin: chapter 1 of the 3rd edition, with its terms explained and its figures recomputed"
DOC_ABOUT = ("This document renews chapter 1 of the 3rd edition by explaining each of its concepts in continuous prose, by adding a concept for every "
             "technical term the chapter uses in passing, and by recomputing every number, date and hash it quotes from the sources that state them.")
CHANGE = ("1.2.0 rewrites every explanation as four to six paragraphs of continuous prose, keeps every concept identifier of 1.1.0 with its parent, and "
          "adds the concepts the explanations needed (the two new subject branches Foundations and Standards among them, with the cryptographic "
          "primitives, the parts of the chain, the everyday computing terms, the threats, the objects of a payment, the newer offchain payment "
          "techniques and the standards bodies), found by an audit of the terms used; it also replaces the figures of 1.1.0 with values recomputed "
          "from the saved sources, so MAJOR in the text and MINOR in the structure; numbered MINOR because no identifier was removed.")


def run_checks_inprocess():
    bad = []; n = 0
    def ev(e): return repr(eval(e, {}))
    for e, x in CHECKS:
        n += 1
        try: got = ev(e)
        except BaseException as ex: got = "EXC %r" % (ex,)
        if got != x: bad.append((e[:160], x, got))
    for nd in NODES:
        if nd[4] and nd[4][2]:
            n += 1; e, x = nd[4][2]
            try: got = ev(e)
            except BaseException as ex: got = "EXC %r" % (ex,)
            if got != x: bad.append((nd[0], x, got))
    for e, typ in RAISES:
        n += 1
        try: eval(e, {}); bad.append((e, typ, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != typ: bad.append((e, typ, type(ex).__name__))
    for leaf, text in ERRORS:
        n += 1; e, rest = text.split(" raises ", 1); et, msg = rest.split(": ", 1)
        try: eval(e, {}); bad.append((e, et, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != et or not str(ex).startswith(msg): bad.append((e, rest, "%s: %s" % (type(ex).__name__, ex)))
    return n, bad


if __name__ == "__main__":
    n, bad = run_checks_inprocess()
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", len(bad))
    for b in bad: print("   ", b)
    ids = [x[0] for x in NODES]; assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    byid = {x[0]: x for x in NODES}
    for x in NODES:
        assert x[3] is None or x[3] in byid, x[0]
        assert (x[2] == 3) == (x[4] is not None), x[0]
        if x[3]: assert byid[x[3]][2] == x[2] - 1 and ids.index(x[3]) < ids.index(x[0]), x[0]
        assert (x[2] == 3 and 4 <= len(x[5]) <= 6) or (x[2] < 3 and 3 <= len(x[5]) <= 6), (x[0], len(x[5]))
    for leaf, owner in OWNERS: assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, (leaf, owner)
    for leaf, t in ERRORS: assert leaf in byid and byid[leaf][2] == 3, leaf
    old = ("Money Unit BitcoinUnit Supply SupplyCap Halving Price FloatingExchangeRate Network Consensus ProofOfWork DoubleSpend History Whitepaper "
           "ReferenceImplementation Wallet WalletPlatform DesktopWallet MobileWallet WebWallet NodeType FullNode LightweightClient KeyControl "
           "NoncustodialWallet Backup RecoveryCode Usage Address BitcoinAddress Transfer SendingAndReceiving SemanticBridge DecentralizedIdentity "
           "Nature Characteristic Virtual Borderless Decentralized Robust Architecture PeerToPeerProtocol PublicJournal ConsensusRuleSet Issuance "
           "CentralBankReplacement Deflation Acquisition BuyFromFriend EarnBitcoin BitcoinATM CurrencyExchange").split()
    assert not [o for o in old if o not in byid], [o for o in old if o not in byid]
    print(len(NODES), "concepts (%d of 1.1.0 kept);" % len(old), sum(len(x[5]) for x in NODES), "paragraphs;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words;", len(CHECKS) + len(RAISES) + len(ERRORS) + sum(1 for x in NODES if x[4] and x[4][2]), "executed claims")
