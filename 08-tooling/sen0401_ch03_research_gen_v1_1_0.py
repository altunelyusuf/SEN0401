#!/usr/bin/env python3
"""Writes 03-materials/ch03/rdodi/sen0401_ch03_research_v1_1_0.ttl from the 1.0.0 record: the same sixteen publications and the course notes (re-read
ones carry the new verification time), one new publication for every further source read for version 1.1.0 (each with its verifiedAt), the findings of
1.0.0 corrected where a source read now says otherwise, four new findings (the re-run of the release check, the registry query of 2026-10-02, the
differences between the book's printed outputs and release 31.1, and the terms used without a concept) and a new scorecard.
Every source is one that a CHECKS entry of sen0401_ch03_corpus_v1_1_0.py re-reads from its saved copy. Run: python3 sen0401_ch03_research_gen_v1_1_0.py"""
import re, datetime, importlib.util, os
here = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(os.path.dirname(here), "03-materials", "ch03", "rdodi")
NOW = datetime.datetime.now().replace(microsecond=0).isoformat(); TODAY = NOW[:10]
old = open(os.path.join(R, "sen0401_ch03_research_v1_0_0.ttl"), encoding="utf-8").read()
sp = importlib.util.spec_from_file_location("c", os.path.join(here, "sen0401_ch03_corpus_v1_1_0.py")); C = importlib.util.module_from_spec(sp); sp.loader.exec_module(C)
oldtbox = open(os.path.join(R, "sen0401_ch03_domain_tbox_v1_0_0.ttl"), encoding="utf-8").read()
oldids = set(re.findall(r"^chx:(\w+) ", oldtbox, flags=re.M)); newids = [n[0] for n in C.NODES]
added = [i for i in newids if i not in oldids]
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"; GH = "https://raw.githubusercontent.com/bitcoin/bitcoin/" + COMMIT + "/"
BK = "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/"
def q(s): return s.replace("\\", "\\\\").replace('"', '\\"')
lines = old.split("\n")
# --- header
head = []
for l in lines:
    if l.startswith("chx:") and not l.startswith("chx:Research") and not l.startswith("chx:Scope"): break
    head.append(l)
text = "\n".join(head)
text = text.replace('owl:versionInfo "1.0.0"', 'owl:versionInfo "1.1.0"').replace("research/1.0.0>", "research/1.1.0>").replace("sen0401_ch03_research_v1_0_0", "sen0401_ch03_research_v1_1_0")
text = text.replace('dcterms:modified "2026-09-29"', 'dcterms:modified "%s"' % TODAY)
text = text.replace("prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .", "prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> ;\n    prov:wasRevisionOf <http://example.org/sen0401/ch03/research/1.0.0> .", 1)
# --- publications: (id, label, url, role)
byline = {l.split(" ")[0]: l for l in lines if l.startswith("chx:P")}
reread = {"P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10", "P11", "P13", "P15", "P16"}
pubs = []
for k, l in byline.items():
    pid = k[4:]
    if pid in reread: l = re.sub(r'sen0414:verifiedAt "[^"]+"', 'sen0414:verifiedAt "%s"' % NOW, l)
    pubs.append((pid, l))
n = 16
def add(label, url, role="primary", ident=None):
    global n
    n += 1; pid = "P%02d" % n
    pubs.append((pid, 'chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; res:hasVerificationStatus res:Status_Verified ; sen0414:verifiedAt "%s"^^xsd:dateTime ; sen0414:sourceRole "%s" .' % (pid, q(label), url, NOW, role)))
    return pid
P = {}
P["registry"] = add("Package-registry release data for the toolkits the book lists: npm, PyPI, the Go module proxy, crates.io, Maven Central and NuGet, queried 2026-10-02 (Package registries, 2026)", "https://registry.npmjs.org/bcoin", "secondary")
P["sums"] = add("SHA256SUMS and SHA256SUMS.asc of Bitcoin Core 31.1, saved, hashed and verified again on 2026-10-02 (Bitcoin Core, 2026)", "https://bitcoincore.org/bin/bitcoin-core-31.1/SHA256SUMS", "primary")
P["verify"] = add("Bitcoin Core: contrib/verify-binaries/README.md and contrib/guix/README.md at commit 05bc2f5 (Bitcoin Core, 2026)", GH + "contrib/verify-binaries/README.md")
P["rp"] = add("Bitcoin Core: doc/release-process.md at commit 05bc2f5 (Bitcoin Core, 2026)", GH + "doc/release-process.md")
for f in ["README.md", "doc/bips.md", "doc/bitcoin-conf.md", "doc/descriptors.md", "doc/JSON-RPC-interface.md", "doc/managing-wallets.md", "contrib/init/bitcoind.service", "share/rpcauth/rpcauth.py"]:
    add("Bitcoin Core: %s at commit 05bc2f5 (Bitcoin Core, 2026)" % f, GH + f)
add("Bitcoin Core 28.0 and 31.0 release notes (Bitcoin Core, 2026)", GH + "doc/release-notes/release-notes-31.0.md")
for f in ["src/arith_uint256.cpp", "src/chain.cpp", "src/chain.h", "src/chainparamsbase.cpp", "src/clientversion.cpp", "src/clientversion.h", "src/consensus/amount.h", "src/consensus/consensus.h",
          "src/httprpc.cpp", "src/index/txindex.h", "src/init.cpp", "src/kernel/caches.h", "src/kernel/chainparams.cpp", "src/kernel/mempool_options.h", "src/kernel/warning.h", "src/net.h",
          "src/node/caches.cpp", "src/node/kernel_notifications.cpp", "src/node/protocol_version.h", "src/node/warnings.cpp", "src/pow.cpp", "src/protocol.h", "src/random.h",
          "src/rpc/blockchain.cpp", "src/rpc/net.cpp", "src/rpc/rawtransaction.cpp", "src/rpc/request.cpp", "src/util/byte_units.h", "src/util/strencodings.cpp", "src/validation.h"]:
    add("Bitcoin Core source: %s at commit 05bc2f5 (Bitcoin Core, 2026)" % f, GH + f)
for ch, nm in [("ch01_intro.adoc", "Chapter 1, Introduction"), ("ch06_transactions.adoc", "Chapter 6, Transactions"), ("ch10_network.adoc", "Chapter 10, The Bitcoin Network"),
               ("ch11_blockchain.adoc", "Chapter 11, The Blockchain"), ("ch12_mining.adoc", "Chapter 12, Mining and Consensus"), ("glossary.asciidoc", "Glossary"), ("appc_bips.adoc", "Appendix C, Bitcoin Improvement Proposals"),
               ("code/rpc_example.py", "the code file rpc_example.py")]:
    add("Mastering Bitcoin, 3rd edition - %s (Antonopoulos and Harding, O'Reilly, 2023; tag third_edition_print1)" % nm, BK + ch)
for no, au in [(2, "Dashjr, 2016"), (3, "Murch, 2025"), (9, "Wuille et al., 2015"), (34, "Andresen, 2012"), (90, "Daftuar, 2016"), (113, "Kerin and Friedenbach, 2015"),
               (141, "Lombrozo et al., 2015"), (144, "Lombrozo and Wuille, 2016"), (159, "Schnelli, 2017"), (380, "Wuille and Chow, 2021")]:
    add("BIP %d (%s), bitcoin/bips" % (no, au), "https://github.com/bitcoin/bips/blob/master/bip-%04d.mediawiki" % no)
add("Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)", "https://bitcoin.org/bitcoin.pdf")
add("RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format (Bray, 2017)", "https://www.rfc-editor.org/rfc/rfc8259", "secondary")
add("RFC 9110, HTTP Semantics (Fielding et al., 2022)", "https://www.rfc-editor.org/rfc/rfc9110", "secondary")
add("RFC 9580, OpenPGP (Wouters et al., 2024)", "https://www.rfc-editor.org/rfc/rfc9580", "secondary")
add("RFC 6234, US Secure Hash Algorithms (SHA and SHA-based HMAC and HKDF) (Eastlake and Hansen, 2011)", "https://www.rfc-editor.org/rfc/rfc6234", "secondary")
add("RFC 4648, The Base16, Base32, and Base64 Data Encodings (Josefsson, 2006)", "https://www.rfc-editor.org/rfc/rfc4648", "secondary")
add("RFC 7617, The 'Basic' HTTP Authentication Scheme (Reschke, 2015)", "https://www.rfc-editor.org/rfc/rfc7617", "secondary")
add("JSON-RPC 2.0 Specification (JSON-RPC Working Group, 2013)", "https://www.jsonrpc.org/specification", "secondary")
add("PROV-O: The PROV Ontology, W3C Recommendation, 30 April 2013 (Lebo et al., 2013)", "https://www.w3.org/TR/prov-o/", "secondary")
add("The Open Source Definition (Open Source Initiative, 2026)", "https://opensource.org/osd", "secondary")
add("The MIT License (Open Source Initiative, 2026)", "https://opensource.org/license/mit", "secondary")
add("Pro Git, What is Git? (Chacon and Straub, 2014)", "https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F", "secondary")
add("git-clone and git-tag documentation (Git project, 2026)", "https://git-scm.com/docs/git-clone", "secondary")
add("About SQLite (SQLite, 2026)", "https://www.sqlite.org/about.html", "secondary")
add("CMake command-line tools reference manual (Kitware, 2026)", "https://cmake.org/cmake/help/latest/manual/cmake.1.html", "secondary")
add("curl manual (Stenberg, 2026)", "https://curl.se/docs/manpage.html", "secondary")
add("Blockstream Esplora API: block 1000 header (Blockstream, 2026)", "https://blockstream.info/api/block-height/1000", "secondary")
add("python-bitcoinlib 0.12.2: rpc.py and package metadata (Todd, 2023)", "https://pypi.org/project/python-bitcoinlib/0.12.2/", "secondary")
add("Evidence of the run of Bitcoin Core 31.1: descriptors, wallet, start-up log, help texts, datadir, block data (Bitcoin Core, 2026), made on 2026-09-28 and 2026-10-02, saved in 08-tooling/ch03-evidence", "urn:sen0401:ch03-evidence", "primary")
# --- findings
F = {}
for l in lines:
    m = re.match(r"chx:(F\d+) ", l)
    if m: F[m.group(1)] = l
def fixed(fid, old_s, new_s):
    assert old_s in F[fid], (fid, old_s); F[fid] = F[fid].replace(old_s, new_s)
fixed("F7", "registries show releases in 2026 for bitcoinjs-lib, btcd, the Rust bitcoin crate, pycoin and bitcoinj;", "the registries queried on 2026-10-02 show releases within the previous year for bitcoinjs-lib, btcd, the Rust bitcoin crate and pycoin, while bitcoinj's latest on Maven Central is dated 2025-02-21 (the earlier query of 2026-09-28 had read it as 2026, which this query does not reproduce);")
F["F7"] = F["F7"].replace("sen0414:cites chx:P14, chx:P13 .", "sen0414:cites chx:P14, chx:P13, chx:%s ." % P["registry"])
fixed("F8", "this shows the download matches the published record", "recomputed on 2026-10-02 the archive has the size 90293352 bytes and the same SHA-256, the signature file holds 11 signature blocks and the check reports 11 good signatures with 38 builder keys imported; this shows the download matches the published record")
F["F8"] = F["F8"].replace("sen0414:cites chx:P09, chx:P15 .", "sen0414:cites chx:P09, chx:P15, chx:%s, chx:%s, chx:%s ." % (P["sums"], P["verify"], P["rp"]))
tail_fid = max(int(k[1:]) for k in F)
def newf(label, txt, cites):
    global tail_fid
    tail_fid += 1; F["F%d" % tail_fid] = 'chx:F%d a sen0414:Finding ; rdfs:label "%s"@en ; sen0414:findingText "%s" ; sen0414:cites %s .' % (tail_fid, label, q(txt), ", ".join("chx:" + c for c in cites))
newf("Comparative analysis", "The book's printed outputs for the status commands differ from release 31.1 in ways that the explanations now state: getnetworkinfo printed relayfee 0.00001000, which is 1 satoshi per virtual byte, whereas 31.1 returns 1e-06, which is 0.1 satoshi per virtual byte; the local services printed as 0x409 (NETWORK, WITNESS, NETWORK_LIMITED) are 0xc09 in 31.1 because the version 2 transport P2P_V2 is added; the start-up log line of 125 automatic connections is reproduced by 31.1 although the newest source defines a default of 200 connections; getblockchaininfo returns its warnings as an array. Each figure is read from the saved output and recomputed by a claim.", ["P01", "P09", "P06"])
newf("Comparative analysis", "The source of the reward figure and of the block header are re-derived without a node: block 123456's header hashes to its printed identifier and block 1000's header, saved from a block explorer's API, hashes to its identifier; a transaction parser written with the python standard library reproduces the txid, the wtxid, the size 194, the 125 bytes without witness and the weight 569 of Alice's transaction; the Merkle root of block 123456 follows from its 13 transaction identifiers; and the difficulty of block 123456, 157416.40184364893, follows from its bits 1a6a93b3.", ["P01", "P12", "P09"])
newf("Methodology", "An audit of the vocabulary of the explanations against the concepts of this chapter and of chapters 1 and 2 found terms used without a concept of their own, which are now concepts: %s. The audit compared every term of a list of computing and Bitcoin terms with the text of all explanations and with the concept labels, and the added concepts were checked in turn for further gaps until none of the listed terms remained undefined." % ", ".join(i for i in added if C.__dict__ and i in ("Byte", "BitShift", "UnixTime", "RandomNumber", "Base64", "FileAndDirectory", "Process", "Library", "Database", "Platform", "NetworkProtocol", "SoftwareTesting", "PackageManager", "Salt", "Hmac", "Fork", "OutputType", "ProgrammingLanguage", "Checksum", "OpenPgpSignature", "ReproducibleBuild", "PackageRegistry", "Iri")), ["P01", "P17"])
body = ["chx:Research a res:ResearchProject ; rdfs:label \"Bitcoin Core: the reference implementation, run and checked against the book\"@en ;",
        "    sen0414:methodology \"Primary source first: the chapter's named concepts from the book's own source at tag third_edition_print1. Then the official documentation and source of Bitcoin Core at commit 05bc2f5, the standards the chapter's topics touch, and the data of the real release 31.1. Every source opened and read on 2026-09-28 or on %s; every claim taken from text actually read and saved in 08-tooling/ch03-sources or ch03-evidence; every number, hash and output executed under Python 3.14.4 by a claim of the chapter's corpus.\" ;" % TODAY,
        "    res:hasResearchScope chx:Scope ; rdfs:member %s, chx:P_NOTES ." % ", ".join("chx:" + p for p, _ in pubs if p != "P_NOTES"),
        [l for l in lines if l.startswith("chx:Scope ")][0].replace("Current as of 2026-09-29.", "Current as of %s." % TODAY)]
concepts = [l for l in lines if l.startswith("chx:C_")]
notes = [l for l in lines if l.startswith("chx:P_NOTES")][0].replace("Yusuf Altunel, 2021 -", "Yusuf Altunel (Altunel, 2021) -")
used_in_findings = set()
for l in F.values(): used_in_findings |= set(re.findall(r"chx:(P\w+)", l.split("sen0414:cites")[1]))
npubs = len(pubs) + 1
score = 'chx:Scorecard a sen0414:QualityScorecard ; rdfs:label "Quality scorecard"@en ; sen0414:topicCoverage "42 primary-source concepts inventoried from the textbook ontology; the domain ontology has %d concepts (%d of version 1.0.0 kept, %d added)." ; sen0414:citationStrength "%d sources, each opened and read on 2026-09-28 or %s, each with its verification time; %d cited by findings, the others by the claims of the corpus." ; sen0414:methodologyCompliance "RDODI procedure v1.6.0 Stage 1." ; sen0414:reproducibility "Every source is a stable public URL or a file saved in the repository; every claim names its sources and is executed." .' % (len(newids), len(oldids & set(newids)), len(added), npubs, TODAY, len(used_in_findings))
out = text + "\n" + "\n".join(body) + "\n" + "\n".join(p[1] for p in pubs) + "\n" + notes + "\n" + "\n".join(concepts) + "\n" + "\n".join(F[k] for k in sorted(F, key=lambda s: int(s[1:]))) + "\n" + score + "\n"
open(os.path.join(R, "sen0401_ch03_research_v1_1_0.ttl"), "w", encoding="utf-8").write(out)
print("publications", npubs, "findings", len(F), "concepts old/new/added", len(oldids), len(newids), len(added))
