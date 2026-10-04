#!/usr/bin/env python3
"""Writes the RDODI Stage 1 research record of SEN0401 chapter 1 at version 1.2.0 (the chapter builder does not write this part).
It keeps every publication of 1.1.0, corrects the two publication dates that the saved specifications contradict, and adds one
publication for every further source that was read for version 1.2.0 of the corpus. Each publication's URL was requested in the
same session and answered (the status is recorded in sen0414:httpStatus); the three sources whose site refuses an automated
request carry the status that was returned and are cited by the saved copy as well.
usage: sen0401_ch01_research_gen_v1_2_0.py [OUTDIR]        default: 03-materials/ch01/rdodi
"""
__version__ = "1.2.0"
import os, sys, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ch01-sources")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "03-materials", "ch01", "rdodi")
NOW = "2026-10-04T00:00:00"          # the session in which every source below was read
OLD = "2026-09-25T07:51:05"          # the session of version 1.1.0
VER, V = "1.2.0", "1_2_0"
BASE = "http://example.org/sen0401/ch01"

def sha(name):
    return hashlib.sha256(open(os.path.join(SRC, name), "rb").read()).hexdigest()[:16]

# (id, label, url, http status, role, saved file or None, verifiedAt)
PUBS = [
 ("P01", "Mastering Bitcoin, 3rd edition - Chapter 1, Introduction (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch01_intro.adoc", 200, "primary", "ch01_intro.adoc", NOW),
 ("P02", "Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf", 200, "secondary", "wp.txt", NOW),
 ("P03", "Hashcash - A Denial of Service Counter-Measure (Back, 2002)", "http://www.hashcash.org/papers/hashcash.pdf", 200, "secondary", "hashcash.txt", NOW),
 ("P04", "Bitcoin Core source tree at commit 05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940, committed 2026-09-28 (Bitcoin Core, 2026): src/consensus/amount.h, src/validation.cpp, src/kernel/chainparams.cpp, src/pow.cpp, src/consensus/params.h",
  "https://github.com/bitcoin/bitcoin/tree/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940", None, "secondary", "core_amount.h", NOW),
 ("P05", "Controlled supply - Bitcoin Wiki, revision 71037 (Bitcoin Wiki, 2026)", "https://en.bitcoin.it/w/index.php?title=Controlled_supply&oldid=71037", 403, "secondary", "supply.txt", NOW),
 ("P06", "BIP 39 - Mnemonic code for generating deterministic keys, by Palatinus, Rusnak, Voisine and Bowe (Palatinus et al., 2013)",
  "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039.mediawiki", 200, "secondary", "bip39.txt", NOW),
 ("P07", "Decentralized Identifiers (DIDs) v1.0, W3C Recommendation, 19 July 2022 (World Wide Web Consortium, 2022) - the date of version 1.1.0 of this record, 9 July 2022, is corrected here from the specification's own header",
  "https://www.w3.org/TR/did-core/", 200, "secondary", "did.txt", NOW),
 ("P08", "Verifiable Credentials Data Model v2.0, W3C Recommendation, 15 May 2025 (World Wide Web Consortium, 2025) - the date of version 1.1.0 of this record, 5 May 2025, is corrected here from the specification's own header",
  "https://www.w3.org/TR/vc-data-model-2.0/", 200, "secondary", "vc.txt", NOW),
 ("P_NOTES", "Course notes: Chapter_1_Introduction.pptx, SEN0401 (then CSE0469) Block Chain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; supplied by the owner on 2026-09-25 (sha256 d2c5e9a87aee1b3d)",
  "urn:sen0401:course-notes:Chapter_1_Introduction.pptx:d2c5e9a87aee1b3d", None, "secondary", None, OLD),
 ("P09", "Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch12_mining.adoc", 200, "secondary", None, OLD),
 # ---- added for version 1.2.0: every further source read in this session ----
 ("P10", "Mastering Bitcoin, 3rd edition - Glossary (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/glossary.asciidoc", 200, "secondary", "glossary.asciidoc", NOW),
 ("P11", "Mastering Bitcoin, 3rd edition - Chapter 2, How Bitcoin Works (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch02_overview.adoc", 200, "secondary", "ch02_overview.adoc", NOW),
 ("P12", "Mastering Bitcoin, 3rd edition - Chapter 4, Keys and Addresses (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch04_keys.adoc", 200, "secondary", "ch04_keys.adoc", NOW),
 ("P13", "Mastering Bitcoin, 3rd edition - Chapter 9, Transaction Fees (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch09_fees.adoc", 200, "secondary", "ch09_fees.adoc", NOW),
 ("P14", "Mastering Bitcoin, 3rd edition - Chapter 10, The Bitcoin Network (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch10_network.adoc", 200, "secondary", "ch10_network.adoc", NOW),
 ("P15", "Mastering Bitcoin, 3rd edition - Appendix C, Bitcoin Improvement Proposals (Antonopoulos and Harding, 2023)",
  "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/appc_bips.adoc", 200, "secondary", "appc_bips.adoc", NOW),
 ("P16", "BIP 21 - URI Scheme, status Closed, proposed replacement BIP 321 (Schneider and Corallo, 2012)",
  "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0021.mediawiki", 200, "secondary", "bip21.txt", NOW),
 ("P17", "The Byzantine Generals Problem, by Lamport, Shostak and Pease, ACM Transactions on Programming Languages and Systems (Lamport et al., 1982)",
  "https://lamport.azurewebsites.net/pubs/byz.pdf", 200, "secondary", "lamport.txt", NOW),
 ("P18", "The Bitcoin Lightning Network: Scalable Off-Chain Instant Payments, draft version 0.5.9.2 (Poon and Dryja, 2016)",
  "https://lightning.network/lightning-network-paper.pdf", 200, "secondary", "lightning.txt", NOW),
 ("P19", "RFC 4949 - Internet Security Glossary, Version 2 (Shirey, 2007)", "https://www.rfc-editor.org/rfc/rfc4949.txt", 200, "secondary", "rfc4949.txt", NOW),
 ("P20", "RFC 6234 - US Secure Hash Algorithms (SHA and SHA-based HMAC and HKDF) (Eastlake and Hansen, 2011)", "https://www.rfc-editor.org/rfc/rfc6234.txt", 200, "secondary", "rfc6234.txt", NOW),
 ("P21", "RFC 8018 - PKCS #5: Password-Based Cryptography Specification Version 2.1, by Moriarty, Kaliski and Rusch (Moriarty et al., 2017)", "https://www.rfc-editor.org/rfc/rfc8018.txt", 200, "secondary", "rfc8018.txt", NOW),
 ("P22", "RFC 4648 - The Base16, Base32, and Base64 Data Encodings (Josefsson, 2006)", "https://www.rfc-editor.org/rfc/rfc4648.txt", 200, "secondary", "rfc4648.txt", NOW),
 ("P23", "RFC 3986 - Uniform Resource Identifier (URI): Generic Syntax, by Berners-Lee, Fielding and Masinter (Berners-Lee et al., 2005)", "https://www.rfc-editor.org/rfc/rfc3986.txt", 200, "secondary", "rfc3986.txt", NOW),
 ("P24", "RFC 9112 - HTTP/1.1, by Fielding, Nottingham and Reschke (Fielding et al., 2022)", "https://www.rfc-editor.org/rfc/rfc9112.txt", 200, "secondary", "rfc9112.txt", NOW),
 ("P25", "About W3C - the World Wide Web Consortium (World Wide Web Consortium, 2026)", "https://www.w3.org/about/", 200, "secondary", "w3c_about.txt", NOW),
 ("P26", "The Open Source Definition (Open Source Initiative, 2026)", "https://opensource.org/osd", 200, "secondary", "osd.txt", NOW),
 ("P27", "MDN Web Docs glossary: Internet, Protocol, HTTP, Browser, Server, API, URI, Database and Cryptography (Mozilla Developer Network, 2026)",
  "https://developer.mozilla.org/en-US/docs/Glossary", 200, "secondary", "mdn_Internet.txt", NOW),
 ("P28", "Wikipedia: QR code, Operating system, Distributed computing, Malware, Phishing, Pseudonym and Deflation (Wikipedia contributors, 2026)",
  "https://en.wikipedia.org/wiki/QR_code", 200, "secondary", "wp_QRcode.txt", NOW),
 ("P29", "Public block data of block 0 and block 840000, saved from the Blockstream Esplora API (Blockstream, 2026)",
  "https://blockstream.info/api/block-height/0", 200, "secondary", "block0.json", NOW),
]

# (id, label, text, cited publications)
FINDINGS = [
 ("F1", "Background",
  "Chapter 1 presents Bitcoin as money, network and software: bitcoin the unit with a small b and Bitcoin the system with a capital B; its history from a 2008 paper by Satoshi Nakamoto and a network started in 2009; proof of work as a lottery run every 10 minutes on average that lets a decentralized network reach consensus and solves the double-spend; a supply just below 21 million; and a practical start - choosing a wallet by platform and by node type, who controls the keys, recovery codes, addresses, receiving, pricing and sending.",
  ["P01"]),
 ("F2", "Contemporary developments",
  "Since the book's publication the subsidy halved at block 840000 to 3.125 bitcoin per block; the block data saved from the Blockstream API carries the Unix time 1713571767 for that block, which is 2024-04-20 00:09:27 in universal time, and the hash of that block begins with 19 zeros against the 10 of the first block, so the difficulty of the computational task has risen by many orders of magnitude since 2009.",
  ["P05", "P29"]),
 ("F3", "Comparative analysis",
  "The chapter's claims can be checked against its sources and by computation: Nakamoto's paper proposes a purely peer-to-peer electronic cash system, and proof of work descends from Back's Hashcash, first proposed to throttle systematic abuse of un-metered internet resources; the supply schedule sums to 20999999.9769 bitcoin, which is 0.0231 below 21 million because every subsidy is rounded down to whole satoshis; the subsidy rule of Bitcoin Core's validation code halves 50 bitcoin once for each interval of 210000 blocks and pays nothing from the 34th interval on; and the recovery codes the book shows follow BIP 39, whose initial entropy is 128 to 256 bits and whose checksum is the first ENT/32 bits of a SHA-256 hash.",
  ["P02", "P03", "P04", "P05", "P06"]),
 ("F4", "Conclusion",
  "For SEN0401's theme of semantic technologies, the chapter's key idea - control by whoever holds the keys, with no central registry - is the same idea the World Wide Web Consortium standardised for identity in Decentralized Identifiers and Verifiable Credentials, which gives projects a bridge from the book to semantic web standards; both are Recommendations of a consortium whose own pages describe it as an international public-interest non-profit organisation that develops web standards.",
  ["P01", "P07", "P08", "P25"]),
 ("F5", "Course notes",
  "The owner's course notes for this chapter (written in 2021 after the 2nd edition) surfaced four topics the renewed deck lacked; each was checked against the 3rd edition and kept only in its words: what makes Bitcoin different - virtual, borderless, decentralized and robust against legitimate governments or criminal elements; the four parts behind the scenes - protocol, blockchain, consensus rules and proof of work; mining replacing a central bank's issuance and clearing, with the currency deflationary and issuance ending around 2140; and the four ways to get a first bitcoin. Two items in the notes were left out: a 2021 price-prediction source, as dated and speculative, and classified-ad sellers, which the 3rd edition no longer lists.",
  ["P_NOTES", "P01"]),
 ("F6", "Terms used without definition",
  "An audit of the explanations of version 1.1.0 listed every technical term they used and asked whether the chapter gave it a concept of its own. Sixty-five terms had none: the cryptographic primitives the chapter names in passing (hash function, digital signature, public-key cryptography, private key, entropy, checksum, keyed hash, key stretching), the parts of the record (block, blockchain, timestamp, node), the everyday computing terms (internet, protocol, HTTP, web browser, server, programming interface, URI, QR code, database, operating system, distributed system, bits and bytes), the two attacks the chapter warns about (malware, phishing), the objects of a payment (transaction, inputs and outputs, fee, confirmation, irreversibility, offchain payment, payment channel, the Lightning Network, electronic payment, privacy), and the standards and institutions behind them (Bitcoin Improvement Proposals, open-source software, W3C Recommendations, the central bank, the clearing house). Version 1.2.0 adds a concept for each, so that every term the text uses is explained in the chapter; four further terms that occur once inside a quotation (escrow, firmware, the virtual byte and the pseudorandom function) are glossed where they appear instead of becoming concepts of their own.",
  ["P01", "P10", "P19", "P27", "P28"]),
 ("F7", "Figures that are values at a date",
  "Reading the chapter against its sources separates the rules of the protocol from the values measured at a date. Rules: the interval of 210000 blocks, the retarget period of 2016 blocks, the target of one block in 10 minutes, the cap just below 21 million, the 2048 iterations and the 512-bit result of the recovery code's key derivation, and the 2048-word list from which each word carries 11 bits. Values at a date: the subsidy of 3.125 bitcoin, the price of a bitcoin in any currency, the number of transactions in a block (3050 in block 840000 against 1 in the first block), the number of leading zeros in a block hash, and the combined computing power of the miners. The course quotes the first kind as fixed and the second always with its source and its date.",
  ["P01", "P04", "P06", "P29"]),
]

def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

L = ['''@prefix chx:     <%s#> .
@prefix res:     <http://example.org/rdodi/research-ontology#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix doc:     <http://example.org/rdodi/document-ontology#> .
@prefix sen0401: <http://example.org/sen0401#> .
@prefix sen0414: <http://example.org/sen0401#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
''' % BASE]
L.append('''<%(b)s/research> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 1 - RDODI Stage 1 research artefact"@en ; owl:versionInfo "%(v)s" ; owl:versionIRI <%(b)s/research/%(v)s> ;
    rdfs:comment "%(ch)s"@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "2026-09-24"^^xsd:date ; dcterms:modified "%(d)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch01_research_v%(vu)s" ; prov:wasRevisionOf <%(b)s/research/1.1.0> ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch01-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % dict(b=BASE, v=VER, vu=V, d=NOW[:10], ch=q(
    "1.2.0 re-reads every source of 1.1.0 and adds one publication for each further source that version 1.2.0 of the corpus was written from "
    "(the book's glossary, chapters 2, 4, 9 and 10 and appendix C, BIP 21, the papers of Lamport and of Poon and Dryja, six RFCs, the W3C and "
    "Open Source Initiative pages, the MDN glossary, seven Wikipedia articles and the saved block data); it corrects the publication dates of the "
    "two W3C Recommendations from their own headers, and records the audit of terms used without definition that produced the new concepts.")))

L.append('''chx:Research a res:ResearchProject ; rdfs:label "Bitcoin from first principles: chapter 1 of Mastering Bitcoin, 3rd edition, and Bitcoin today"@en ;
    sen0401:methodology "%s" ;
    res:hasResearchScope chx:Scope ; rdfs:member %s .''' % (q(
    "Primary source first: the chapter's named concepts from the book's own source at tag third_edition_print1. Then the standards, papers, "
    "reference documentation and glossaries that each term of the chapter rests on, each one saved in 08-tooling/ch01-sources and re-read from the "
    "saved copy by a claim that the chapter builder executes, so that a misquotation stops the build. Every source listed below was opened in the "
    "session of " + NOW[:10] + " unless its publication says otherwise, and its address was requested in the same session with the answered status "
    "recorded. Every number, date, hash and output quoted is executed under CPython 3.14.4."),
    ", ".join("chx:" + p[0] for p in PUBS)))
L.append('chx:Scope a res:ResearchScope ; res:hasResearchQuestion "%s" ; res:hasTimeWindow "Current as of %s." .' % (q(
    "What does chapter 1 of Mastering Bitcoin's 3rd edition establish about Bitcoin as money, network and wallet; which technical term that it uses "
    "in passing needs a concept of its own before a student can read it; what has changed since its December 2023 publication; and where does it meet "
    "the course theme of semantic technologies?"), NOW[:10]))

for pid, label, url, status, role, saved, when in PUBS:
    extra = ""
    if status is not None: extra += ' sen0401:httpStatus %d ;' % status
    if saved: extra += ' sen0401:savedCopy "08-tooling/ch01-sources/%s (sha256 %s)" ;' % (saved, sha(saved))
    L.append('chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ;%s res:hasVerificationStatus res:Status_Verified ; sen0401:verifiedAt "%s"^^xsd:dateTime ; sen0401:sourceRole "%s" .'
             % (pid, q(label), url, extra, when, role))

SECTIONS = ["Introduction", "History of Bitcoin", "Getting Started", "Choosing a Bitcoin Wallet", "Types of Bitcoin wallets",
            "Full node versus Lightweight", "Who controls the keys", "Quick Start", "Recovery Codes", "Bitcoin Addresses",
            "Receiving Bitcoin", "Getting Your First Bitcoin", "Finding the Current Price of Bitcoin", "Sending and Receiving Bitcoin"]
CONCEPTS = ["proof of work", "consensus", "double-spend", "recovery code", "floating exchange rate", "noncustodial wallet", "full node",
            "lightweight client", "desktop wallet", "mobile wallet", "web wallet", "Bitcoin ATM", "currency exchange", "confirmation",
            "transaction fee", "offchain technology", "hardware signing device", "third-party API client", "Bitcoin address", "invoice"]
i = 0
for s in SECTIONS:
    i += 1; L.append('chx:C_%02d a sen0401:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0401:conceptKind "Section" ; dcterms:source chx:P01 .' % (i, q(s)))
for s in CONCEPTS:
    i += 1; L.append('chx:C_%02d a sen0401:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0401:conceptKind "Concept" ; dcterms:source chx:P01 .' % (i, q(s)))

for fid, label, text, cites in FINDINGS:
    L.append('chx:%s a sen0401:Finding ; rdfs:label "%s"@en ; sen0401:findingText "%s" ; sen0401:cites %s .'
             % (fid, q(label), q(text), ", ".join("chx:" + c for c in cites)))

import importlib.util
_sp = importlib.util.spec_from_file_location("corpus", os.path.join(HERE, "sen0401_ch01_corpus_v1_2_0.py"))
_C = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_C)
nclaims = len(_C.CHECKS) + len(_C.RAISES) + len(_C.ERRORS) + sum(1 for n in _C.NODES if n[4] and n[4][2])
L.append('chx:Scorecard a sen0401:QualityScorecard ; rdfs:label "Quality scorecard"@en ; sen0401:topicCoverage "%s" ; sen0401:citationStrength "%s" ; sen0401:methodologyCompliance "%s" ; sen0401:reproducibility "%s" .'
         % (q("%d primary-source items inventoried from the chapter (%d sections and %d named concepts); %d concepts in the chapter ontology at version 1.2.0, of which %d are the concepts of version 1.1.0 kept unchanged."
              % (i, len(SECTIONS), len(CONCEPTS), len(_C.NODES), 52)),
            q("%d sources; %d of them opened in the session of %s and the rest carried over with their earlier verification; %d cited by findings; %d of the addresses answered with status 200 and 1 with status 403, whose content is cited from the saved copy."
              % (len(PUBS), sum(1 for p in PUBS if p[6] == NOW), NOW[:10], len({c for f in FINDINGS for c in f[3]}), sum(1 for p in PUBS if p[3] == 200))),
            q("RDODI procedure v1.6.0 Stage 1."),
            q("Every source is a public address or a saved copy named with the first 16 hexadecimal digits of its SHA-256; every quotation in the chapter text is re-read from the saved copy, and every number is recomputed, by one of the %d claims that 08-tooling/sen0401_chapter_build_v1_0_0.py executes before it writes the ontology." % nclaims)))

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "sen0401_ch01_research_v%s.ttl" % V)
open(path, "w").write("\n".join(L) + "\n")
import rdflib
g = rdflib.Graph(); g.parse(path, format="turtle")
print("wrote %s - %d triples, %d publications, %d findings" % (path, len(g), len(PUBS), len(FINDINGS)))
