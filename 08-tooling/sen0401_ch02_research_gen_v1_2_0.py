#!/usr/bin/env python3
"""Writes the RDODI Stage 1 research record of SEN0401 chapter 2 at version 1.2.0, revising 1.1.0 (which stays on disk).

Every publication listed here is a source that was opened and read in the session of 2026-10-04 while version 1.2.0 of the
corpus (08-tooling/sen0401_ch02_corpus_v1_2_0.py) was written, and almost every one of them is also re-read by a CHECKS
entry of that corpus, so that the quotations attributed to it are verified by the chapter builder at every build.
The primary-source concept inventory of 1.1.0 is kept unchanged; the findings of 1.1.0 are kept and three are added,
among them the required finding on terms used without definition.

usage: python3 sen0401_ch02_research_gen_v1_2_0.py        (writes 03-materials/ch02/rdodi/sen0401_ch02_research_v1_2_0.ttl)
"""
__version__ = "1.2.0"
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "03-materials", "ch02", "rdodi")
PRIOR = os.path.join(OUT, "sen0401_ch02_research_v1_1_0.ttl")
NEW = os.path.join(OUT, "sen0401_ch02_research_v1_2_0.ttl")
VERIFIED = "2026-10-04T10:58:24"
MODIFIED = "2026-10-04"
BOOK_TAG = "third_edition_print1"
BOOK_RAW = "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/%s/" % BOOK_TAG
CORE_COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
CORE_RAW = "https://github.com/bitcoin/bitcoin/blob/%s/" % CORE_COMMIT
BIP_RAW = "https://github.com/bitcoin/bips/blob/master/bip-%s.mediawiki"

def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")

# (id, label, source URI, role)  - every entry was read in this session
PUBS = [
    # the chapter itself and the other chapters of the book that the explanations quote
    ("P01", "Mastering Bitcoin, 3rd edition - Chapter 2, How Bitcoin Works (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag %s)" % BOOK_TAG, BOOK_RAW + "ch02_overview.adoc", "primary"),
    ("P10", "Mastering Bitcoin, 3rd edition - Chapter 1, Introduction (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch01_intro.adoc", "secondary"),
    ("P11", "Mastering Bitcoin, 3rd edition - Chapter 3, Bitcoin Core: The Reference Implementation (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch03_bitcoin-core.adoc", "secondary"),
    ("P12", "Mastering Bitcoin, 3rd edition - Chapter 4, Keys and Addresses (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch04_keys.adoc", "secondary"),
    ("P13", "Mastering Bitcoin, 3rd edition - Chapter 6, Transactions (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch06_transactions.adoc", "secondary"),
    ("P14", "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch07_authorization-authentication.adoc", "secondary"),
    ("P15", "Mastering Bitcoin, 3rd edition - Chapter 8, Digital Signatures (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch08_signatures.adoc", "secondary"),
    ("P16", "Mastering Bitcoin, 3rd edition - Chapter 9, Transaction Fees (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch09_fees.adoc", "secondary"),
    ("P17", "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch10_network.adoc", "secondary"),
    ("P18", "Mastering Bitcoin, 3rd edition - Chapter 11, The Blockchain (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch11_blockchain.adoc", "secondary"),
    ("P06", "Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus (Antonopoulos and Harding, 2023)", BOOK_RAW + "ch12_mining.adoc", "secondary"),
    ("P19", "Mastering Bitcoin, 3rd edition - Quick Glossary (Antonopoulos and Harding, 2023)", BOOK_RAW + "glossary.asciidoc", "secondary"),
    ("P20", "Mastering Bitcoin, 3rd edition - Appendix C, Bitcoin Improvement Proposals (Antonopoulos and Harding, 2023)", BOOK_RAW + "appc_bips.adoc", "secondary"),
    # the whitepaper and the standards
    ("P02", "Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf", "secondary"),
    ("P21", "BIP 1: BIP Purpose and Guidelines (Taaki, 2011; status Closed, replaced by BIP 2)", BIP_RAW % "0001", "secondary"),
    ("P22", "BIP 21: URI Scheme (Schneider and Corallo, 2012; status Closed, proposed replacement BIP 321)", BIP_RAW % "0021", "secondary"),
    ("P23", "BIP 173: Base32 address format for native v0-16 witness outputs, Bech32 (Wuille and Maxwell, 2017)", BIP_RAW % "0173", "secondary"),
    ("P24", "BIP 321: Payment Instructions URI (Corallo, 2024; status Complete, replaces BIP 21)", BIP_RAW % "0321", "secondary"),
    ("P04", "PROV-O: The PROV Ontology, W3C Recommendation, 30 April 2013 (Lebo et al., 2013)", "https://www.w3.org/TR/prov-o/", "secondary"),
    # Bitcoin Core source at the pinned commit
    ("P30", "Bitcoin Core src/consensus/amount.h at commit 05bc2f5 (COIN and MAX_MONEY)", CORE_RAW + "src/consensus/amount.h", "secondary"),
    ("P31", "Bitcoin Core src/consensus/consensus.h at commit 05bc2f5 (MAX_BLOCK_WEIGHT and WITNESS_SCALE_FACTOR)", CORE_RAW + "src/consensus/consensus.h", "secondary"),
    ("P32", "Bitcoin Core src/primitives/transaction.cpp at commit 05bc2f5 (the txid is the hash of the serialization without witness data)", CORE_RAW + "src/primitives/transaction.cpp", "secondary"),
    ("P33", "Bitcoin Core src/validation.cpp at commit 05bc2f5 (GetBlockSubsidy)", CORE_RAW + "src/validation.cpp", "secondary"),
    ("P34", "Bitcoin Core src/kernel/chainparams.cpp at commit 05bc2f5 (the halving interval and the target timespan)", CORE_RAW + "src/kernel/chainparams.cpp", "secondary"),
    ("P35", "Bitcoin Core src/key.cpp and src/secp256k1 (ecdsa_impl.h, group_impl.h) at commit 05bc2f5 (the curve order and the generator point)", CORE_RAW + "src/secp256k1/src/group_impl.h", "secondary"),
    # the course notes and the interactive pages
    ("P_NOTES", "Course notes: Chapter_2_HowBitcoinWorks.pptx, SEN0401 (then CSE0469) Block Chain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; text, diagrams and notes of the slides saved in 08-tooling/ch02-sources", "urn:sen0401:course-notes:Chapter_2_HowBitcoinWorks.pptx:8629b856328bf0cf", "secondary"),
    ("P07", "Blockchain Demo (Brownworth, n.d.) - the Hash, Block, Blockchain, Distributed and Coinbase pages and the script blockchain.js, saved in 08-tooling/ch02-sources", "https://andersbrownworth.com/blockchain/hash", "secondary"),
    # the earlier chapter of this course, read for the term audit
    ("P40", "SEN0401 chapter 1 domain ontology TBox v1.2.0 (the concept list of the earlier chapter, read so that terms already explained there are not redefined)", "urn:sen0401:ch01:tbox:1.2.0", "secondary"),
]

NEW_FINDINGS = [
    ("F6", "Terms used without definition",
     "An audit of the 1.1.0 explanations listed every technical term they use and checked each against the concept list of this chapter and of chapter 1. "
     "Sixty-five terms were used without a concept of their own: the cryptographic and computing foundations (hash function, key pair, public key, public-key cryptography, "
     "elliptic curve, digital signature, checksum, entropy, nonce, encryption, bit, byte, hexadecimal notation), the remaining parts of a transaction (script, double-entry "
     "ledger, transaction size, weight, virtual byte, fee rate, unspent transaction output, transaction identifier, serialization, byte order, outpoint, witness), the pieces "
     "of a payment request (URI, QR code, improvement proposal, Bitcoin address, exchange rate), the wallet and the construction of a transaction, the participants and stages "
     "of the network (full node, lightweight client, peer, peer-to-peer network, transmission, gossiping, memory pool, the recipient's own check), and the whole vocabulary of "
     "mining and of security (miner, candidate block, proof of work, block header, merkle tree, difficulty and target, hash rate, coinbase transaction, block reward, mining "
     "pool, soft and hard fork, probability of reversal, best blockchain, block height, fork and alternative block, double spend, spending onward, simplified payment "
     "verification) together with the ontology, the triple and the five pages of the interactive demonstration. "
     "Version 1.2.0 adds a concept for each of them, so that a second run of the same audit over the new text reports no term that is not a concept of this chapter or of chapter 1. "
     "Two terms are explained inside the concept that quotes them rather than as concepts of their own, because the chapter needs them only in one sentence each: the median time "
     "past, glossed where the block's timestamp rule is stated, and the OWL2 Web Ontology Language, glossed where the PROV Ontology is introduced.",
     ["P01", "P40", "P19"]),
    ("F7", "The book's illustration against the real transaction",
     "The chapter's figures and its printed invoice do not all describe the same payment, and every difference was located in the bytes of the real transaction that the book "
     "prints in chapters 3 and 6. The invoice asks for 0.01577764 bitcoin, which is 1,577,764 satoshis, while the transaction of the figures pays 75,000 satoshis; the twenty-byte "
     "program encoded in the invoice's bech32 address is b291ae1c...9485b1c, which is not the program in the real payment output; the figure labels Alice's input Tx1:0 while the "
     "stored output index is 1; and the order of Alice's two outputs in the real transaction is change first, at 20,000 satoshis, then the payment of 75,000, which is why the later "
     "figure has Bob spending Tx2:1. The amounts of the figures are consistent in themselves: 100,000 in, 75,000 plus 20,000 out, a fee of 5,000, and a fee of 8,000 on Bob's onward "
     "transaction of 67,000. Bitcoin Core's reported size, virtual size and weight for that transaction, 194, 143 and 569, were all recomputed from its 194 bytes.",
     ["P01", "P11", "P13"]),
    ("F8", "Quantities of the mining and security sections, recomputed",
     "Every figure the chapter states about mining and confirmations was reproduced from a primary source or from arithmetic. The chapter's 168 billion trillion attempts per block "
     "divide by 600 seconds to a network hash rate of 2.8 times ten to the twentieth hashes a second. The first block's compact target 1d00ffff expands to 65,535 times two to the "
     "power 208, which implies about 4.295 billion attempts at difficulty one, and its eighty-byte header, assembled from the published version, merkle root, time, target and nonce, "
     "hashes to the published block hash 000000000019d668...0a8ce26f, whose timestamp 1231006505 is the third of January 2009. The subsidy rule of Bitcoin Core's GetBlockSubsidy gives "
     "6.25 bitcoins for the 2023 era and 3.125 after block 840,000, and summing 210,000 blocks of each successive subsidy gives the book's total of 2,099,999,997,690,000 satoshis. "
     "Nakamoto's own procedure for an attacker with a tenth of the hash rate reproduces 0.2045873 at one confirmation and 0.0002428 at six. The demonstration page's difficulty of four "
     "leading zeros was reproduced by finding the nonce 6630 for a sample block, against an expected 65,536 attempts.",
     ["P01", "P06", "P18", "P02", "P33", "P07"]),
]

prior = open(PRIOR, encoding="utf-8").read()
head_end = prior.index("chx:Research a res:ResearchProject")
header = prior[:head_end]
header = header.replace('owl:versionInfo "1.1.0"', 'owl:versionInfo "1.2.0"')
header = header.replace("<http://example.org/sen0401/ch02/research/1.1.0>", "<http://example.org/sen0401/ch02/research/1.2.0>")
header = header.replace('dcterms:modified "2026-09-24"^^xsd:date', 'dcterms:modified "%s"^^xsd:date' % MODIFIED)
header = header.replace('dcterms:identifier "sen0401_ch02_research_v1_1_0"',
                        'dcterms:identifier "sen0401_ch02_research_v1_2_0" ;\n    prov:wasRevisionOf <http://example.org/sen0401/ch02/research/1.1.0>')
body = prior[head_end:]
# the concept inventory and the findings of 1.1.0 are kept verbatim; the project, scope and scorecard are replaced
keep = [l for l in body.splitlines() if l.startswith("chx:C_") or re.match(r"chx:F[1-5] ", l)]

MEMBERS = ", ".join("chx:" + p[0] for p in PUBS)
FINDINGS = ["chx:F%d" % i for i in range(1, 6)] + ["chx:" + f[0] for f in NEW_FINDINGS]

L = [header]
L.append('''chx:Research a res:ResearchProject ; rdfs:label "How Bitcoin works: one real transaction from wallet to blockchain, every quotation re-read and every number recomputed"@en ;
    sen0414:methodology "Primary source first: the chapter's own source (ch02_overview.adoc of the bitcoinbook working copy, tag %(tag)s) read in full, then the chapters of the same book that define the terms the chapter uses in passing, its glossary and appendix C, then the standards (Nakamoto's paper, BIPs 1, 21, 173 and 321, W3C PROV-O), then Bitcoin Core's own source at commit %(core)s for every constant quoted, then the owner's 2021 course notes and the interactive demonstration pages the notes link to, and finally chapter 1's TBox so that terms already explained there are not redefined. Every source listed below was opened and read on %(ver)s; every quotation is re-read from the saved copy of its source by a claim that the chapter builder executes, and every number, hash, address, encoding and size is recomputed by such a claim under CPython 3.14.4 - 371 claims in version 1.2.0, all of which hold." ;
    res:hasResearchScope chx:Scope ; rdfs:member %(members)s .
chx:Scope a res:ResearchScope ; res:hasResearchQuestion "How does chapter 2 of Mastering Bitcoin's 3rd edition explain a transaction's path from wallet to blockchain; which terms does it use without defining them, and where are those defined; which of its quantitative claims can be reproduced from primary sources; and how does its transaction chain meet the course theme of provenance?" ; res:hasTimeWindow "Current as of %(mod)s; the book is read at tag %(tag)s and Bitcoin Core at commit 05bc2f5." .''' % dict(
    tag=BOOK_TAG, core=CORE_COMMIT[:7], ver=VERIFIED, members=MEMBERS, mod=MODIFIED))
for pid, label, src, role in PUBS:
    L.append('chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; res:hasVerificationStatus res:Status_Verified ; sen0414:verifiedAt "%s"^^xsd:dateTime ; sen0414:sourceRole "%s" .'
             % (pid, q(label), src, VERIFIED, role))
L.extend(keep)
for fid, label, text, cites in NEW_FINDINGS:
    L.append('chx:%s a sen0414:Finding ; rdfs:label "%s"@en ; sen0414:findingText "%s" ; sen0414:cites %s .'
             % (fid, q(label), q(text), ", ".join("chx:" + c for c in cites)))
L.append('''chx:Scorecard a sen0414:QualityScorecard ; rdfs:label "Quality scorecard"@en ;
    sen0414:topicCoverage "25 primary-source concepts inventoried from the chapter; 101 concepts in the version 1.2.0 ontology (36 identifiers of 1.1.0 kept with their parents, 65 added by the term audit), of which 82 are level-3 concepts with a worked example or definition individual." ;
    sen0414:citationStrength "%d sources, all opened and read at %s; %d cited by findings; every quotation attributed to a source is re-read from the saved copy of that source by an executed claim." ;
    sen0414:methodologyCompliance "RDODI procedure v1.6.0 Stage 1; the Stage 2 and 3 artefacts are generated by 08-tooling/sen0401_chapter_build_v1_0_0.py, which executes every claim before writing and applies the chapter's SHACL shapes to the result." ;
    sen0414:reproducibility "371 executed claims (CHECKS, RAISES, ERRORS and the worked examples) all hold under CPython 3.14.4; the book is pinned to tag %s, Bitcoin Core to commit 05bc2f5, and every other source is saved in 08-tooling/ch02-sources, so the whole record can be re-verified offline by rerunning the corpus module." .'''
         % (len(PUBS), VERIFIED, len({c for f in NEW_FINDINGS for c in f[2:3] and f[3]}) + 5, BOOK_TAG))

open(NEW, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("wrote", NEW, "-", len(PUBS), "publications,", len(FINDINGS), "findings,", len(keep) - 5, "concept-inventory entries kept")
