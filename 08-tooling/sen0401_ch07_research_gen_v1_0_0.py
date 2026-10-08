#!/usr/bin/env python3
"""Writes 03-materials/ch07/rdodi/sen0401_ch07_research_v1_0_0.ttl, the RDODI Stage 1 record of chapter 7, and the chapter's SHACL
shapes sen0401_ch07_domain_shacl_v1_0_0.ttl. Chapter 7 had no earlier record, so both are written from scratch on the model of
chapter 6's (sen0401_ch06_research_gen_v1_0_0.py): one publication per source actually read for this version (the list in
sen0401_ch07_common_v1_0_0.py, each with its verification time), the chapter's own sections and named terms as primary-source
concepts, the findings that the reading and the executed claims support, and a quality scorecard. The shapes are chapter 5's four,
unchanged in content, written under this chapter's namespace.
Run: python3 sen0401_ch07_research_gen_v1_0_0.py   (the system python, which has rdflib; the claims the corpus executes are run by the chapter builder under python3.14)"""
__version__ = "1.0.0"
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch07_common_v1_0_0 import SOURCES
import sen0401_ch07_corpus_v1_0_0 as CORPUS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "03-materials", "ch07", "rdodi")
NOW = os.environ.get("CH7_VERIFIED_AT", "2026-10-08T17:40:00")
TODAY = NOW[:10]


def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ---- the chapter's own sections, in the order of its source ----
SECTIONS = ["Transaction Scripts and Script Language", "Turing Incompleteness", "Stateless Verification", "Script Construction", "The script execution stack",
            "A simple script", "Separate execution of output and input scripts", "Pay to Public Key Hash", "Scripted Multisignatures",
            "An Oddity in CHECKMULTISIG Execution", "Pay to Script Hash", "P2SH Addresses", "Benefits of P2SH", "Redeem Script and Validation",
            "Data Recording Output (OP_RETURN)", "Transaction Lock Time Limitations", "Check Lock Time Verify (OP_CLTV)", "Relative Timelocks",
            "Relative Timelocks with OP_CSV", "Scripts with Flow Control (Conditional Clauses)", "Conditional Clauses with VERIFY Opcodes",
            "Using Flow Control in Scripts", "Complex Script Example", "Segregated Witness Output and Transaction Examples",
            "Pay to witness public key hash (P2WPKH)", "Wallet construction of P2WPKH", "Pay to witness script hash (P2WSH)",
            "Differentiating between P2WPKH and P2WSH", "Upgrading to Segregated Witness", "Embedding segregated witness inside P2SH",
            "Nested pay to witness public key hash", "Nested pay to witness script hash", "Merklized Alternative Script Trees (MAST)",
            "Pay to Contract (P2C)", "Scriptless Multisignatures and Threshold Signatures", "Taproot", "Tapscript"]
TERMS = ["script", "stack", "Turing complete", "stateless verification", "output script", "input script", "scriptSig", "scriptPubKey", "OP_RETURN",
         "pay to public key hash", "public key hash", "OP_CHECKSIG", "signature hash", "hash type", "DER", "multisignature", "OP_CHECKMULTISIG",
         "dummy element", "pay to script hash", "redeem script", "P2SH address", "data carrier output", "lock time", "OP_CHECKLOCKTIMEVERIFY",
         "relative timelock", "sequence", "OP_CHECKSEQUENCEVERIFY", "OP_IF", "conditional clause", "OP_VERIFY", "Miniscript", "segregated witness",
         "witness program", "P2WPKH", "P2WSH", "bech32", "nested segregated witness", "soft fork", "MAST", "merkle root", "membership proof",
         "pay to contract", "key tweak", "scriptless multisignature", "threshold signature", "partial public key", "taproot", "keypath spending",
         "scriptpath spending", "taproot internal key", "taproot output key", "leaf script", "tapscript", "OP_CHECKSIGADD", "schnorr signature",
         "OP_SUCCESS", "mutual satisfaction"]

# ---- findings, each supported by a source read and, where it states a number, by an executed claim ----
F = []


def finding(label, text, cites):
    F.append((label, text, cites))


P = {s[0]: "P%02d" % (i + 1) for i, s in enumerate(SOURCES)}
finding("Background",
        "Chapter 7 explains how a Bitcoin output asks for authorization and how a spender authenticates. It presents the script language and the stack on which "
        "it runs, the input and output scripts and their separate execution, pay to public key hash, scripted multisignatures and the oddity of "
        "OP_CHECKMULTISIG, pay to script hash, data recording with OP_RETURN, absolute and relative timelocks, flow control and a three-path example, "
        "segregated witness in its native and nested forms, and the three ideas that taproot combines - a Merklized tree of scripts, pay to contract and "
        "scriptless multisignatures - followed by taproot and tapscript.",
        [P["AH"]])
finding("Comparative analysis",
        "The statements of the chapter were checked by running them. A Bitcoin Script interpreter written with the Python standard library, faithful to the "
        "interpreter of Bitcoin Core at the pinned commit, accepts all 1,237 script tests of Core's script_tests.json, reproduces all 500 legacy signature "
        "hashes of sighash.json and the 7 signature hash and key path vectors of BIP341's wallet vectors, accepts all 1,022 inputs of the first 599 "
        "non-coinbase transactions of block 775,072 under today's consensus rules and under every policy flag it implements, rejects each tampered "
        "input, and reproduces the BIP340 test vectors. Every worked example of the chapter's page is a program that runs on this interpreter or on "
        "the standard library alone.",
        [P["BCJ"], P["BCW"], P["B340"], P["BCI"], P["MP"]])
finding("Comparative analysis",
        "The first 599 non-coinbase transactions of block 775,072 hold 1,022 inputs and 1,668 outputs. By input type: P2WPKH 626, P2PKH 194, P2SH-wrapped "
        "P2WPKH 95, P2WSH 57 (all multisignatures), P2SH-wrapped P2WSH 34, P2SH multisignatures 10, taproot key path 5 and taproot script path 1; by "
        "output type: P2WPKH 754, P2SH 490, P2PKH 314, P2WSH 69, P2TR 33 and data outputs 8. Segregated witness inputs are 812 of 1,022, about 79 percent. "
        "None of the 91 witness scripts contains a timelock or conditional opcode; the one tapscript is an inscription that begins OP_FALSE OP_IF.",
        [P["MP"], P["BCI"]])
finding("Comparative analysis",
        "The chapter states the lock time rule as an equal-or-higher comparison. Bitcoin Core's IsFinalTx tests whether the lock time is less than the block "
        "height (or the median time past), so a transaction with lock time N is first final in block N plus one; the difference is one block and changes "
        "no conclusion, but an example that sets a lock time to the next block's height is off by one under the source.",
        [P["AH"], P["BCT"], P["BCX"]])
finding("Comparative analysis",
        "The chapter gives three months as 12,960 blocks or 7,760,000 seconds. Twelve thousand nine hundred and sixty blocks of ten minutes are exactly 90 "
        "days, and 90 days are 7,776,000 seconds; the second figure is 16,000 seconds short. The error does not affect the opcode.",
        [P["AH"]])
finding("Comparative analysis",
        "The chapter says that BIP68 and BIP112 were activated in May 2016. The BIPs record that the voting period started on 1 May 2016, and Bitcoin "
        "Core's chainparams puts the first block under the rules at height 419,328, which the explorer dates 4 July 2016.",
        [P["AH"], P["B68"], P["B112"], P["BCL"], P["MA"]])
finding("Comparative analysis",
        "The chapter describes OP_CHECKMULTISIG as comparing the signatures with the keys starting from the first key listed. Bitcoin Core's interpreter "
        "starts from the key at the top of the stack, which is the last key listed; the signatures are matched in the same order and the worst case, "
        "as many checks as keys for a one-signature spend, is the same.",
        [P["AH"], P["BCI"]])
finding("Comparative analysis",
        "The chapter says that the spend of its three-script tree uses 383 bytes against 412 bytes without the tree, saving 29. The sizes of the keys, "
        "signatures and scripts of the figure are not given, so the figures cannot be derived; the saving of the structure is computed instead, one "
        "32-byte commitment for each doubling of the number of scripts. The same paragraph says that four commitments would cost the same as three; the "
        "arithmetic supports four conditions, not four commitments.",
        [P["AH"]])
finding("Comparative analysis",
        "The standards' figures reproduce with the interpreter: a 2-of-3 multisignature script of 105 bytes against 104 bytes as a tapscript with "
        "OP_CHECKSIGADD; the largest control block of 33 plus 32 times 128 bytes; 87 OP_SUCCESS opcode values in BIP342 and in Bitcoin Core's IsOpSuccess; the "
        "taproot activation block 709,632 on 14 November 2021 with a warning height of 711,648 one confirmation window later; and, for the contract "
        "of the chapter's three-path example rebuilt as a taproot tree, spending weights of 577, 617 and 414 weight units by script path and 308 by key "
        "path, against 585, 584 and 509 for the P2WSH script.",
        [P["B341"], P["B342"], P["BCI"], P["BCL"], P["MA"]])
finding("Contemporary developments",
        "Several policy details have moved since the chapter was written. The default budget for OP_RETURN data in Bitcoin Core is now 100,000 vbytes shared by "
        "all the data outputs of a transaction, a figure the chapter does not quote; the relay policy no longer requires the redeem script of a "
        "P2SH output to be standard and caps its signature operations at 15; and Bitcoin Core's descriptors accept key aggregation with musig() from "
        "release 30.0 and signing from release 31.0, so the scriptless multisignatures the chapter describes as future work have a standard (BIP327) "
        "and an implementation.",
        [P["AH"], P["BCP"], P["BCQ"], P["BCD"], P["B327"]])
finding("Contemporary developments",
        "Two stories of the chapter come from sources that are not the book. The OP_RETURN bug of 28 July 2010 (CVE-2010-5141) is recorded by the Bitcoin Wiki and "
        "is visible in the difference between the sources of Bitcoin 0.3.0 and 0.3.7; the fork of 4 July 2015 after the activation of BIP66 is recorded by the "
        "network alert of that day, which names the 950-of-1,000 threshold, a fork of 6 blocks and about half of the hash rate mining without validating.",
        [P["CVE"], P["O0"], P["O7"], P["BA"], P["B66"]])
finding("Terms used without definition",
        "An audit of the explanations written for this chapter listed every technical term they use and compared it with the concepts of chapters 1 to 6 "
        "and of this chapter. The terms used without a concept of their own were the stack and its execution, the truth of a script, the public key "
        "hash, the DER encoding, the dummy element, the count of signature checks, the redeem script, the witness program and the sigops of a script hash. "
        "Each was added as a concept of this chapter, so that no term in the document is used before it is explained.",
        [P["AH"], P["AH6"], P["AH8"], P["AH4"], P["AHG"]])
finding("Conclusion",
        "For the course, the chapter's lesson is that authorization is a program, and that each upgrade of Bitcoin's scripts is a way of making the program "
        "cheaper to show and harder to see: a hash instead of a script, a witness instead of an input script, a tree instead of a list, and at the end "
        "a single signature that stands for any of them. The second lesson is that the scripts run in the same way on every node because the language "
        "is stateless and bounded, and that every figure of the chapter can be checked by running it.",
        [P["AH"], P["B341"]])

# ---- the record ----
L = ['@prefix chx:     <http://example.org/sen0401/ch07#> .',
     '@prefix res:     <http://example.org/rdodi/research-ontology#> .',
     '@prefix rd:      <http://example.org/rdodi/domain-ontology#> .',
     '@prefix doc:     <http://example.org/rdodi/document-ontology#> .',
     '@prefix sen0401: <http://example.org/sen0401#> .',
     '@prefix owl:     <http://www.w3.org/2002/07/owl#> .',
     '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .',
     '@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .',
     '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .',
     '@prefix dcterms: <http://purl.org/dc/terms/> .',
     '@prefix prov:    <http://www.w3.org/ns/prov#> .',
     '@prefix sh:      <http://www.w3.org/ns/shacl#> .',
     '',
     '''<http://example.org/sen0401/ch07/research> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 7 - RDODI Stage 1 research artefact"@en ; owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0401/ch07/research/1.0.0> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%(day)s"^^xsd:date ; dcterms:modified "%(day)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch07_research_v1_0_0" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch07-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''' % dict(day=TODAY)]

PIDS = ["P%02d" % (i + 1) for i in range(len(SOURCES))]
L.append('''
chx:Research a res:ResearchProject ; rdfs:label "Authorization and authentication: every script, signature check, timelock, multisignature, segregated witness and taproot spend of the chapter run through an interpreter and checked against the standards and Bitcoin Core's tests"@en ;
    sen0401:methodology "Primary source first: the chapter's own sections and named terms from the book's source at the commit the textbook ontology pins (275c4eb8). Then the proposal that defines each mechanism the chapter names, Bitcoin Core's consensus, policy, primitives, script and validation sources at the commit pinned for this course (05bc2f5) with its list of implemented proposals, and - because no node is available in this environment - the raw bytes and explorer records of 599 transactions of block 775,072 and of three landmark transactions, and the six activation blocks, fetched from mempool.space; the script rules themselves are run by a Bitcoin Script interpreter written with the standard library and checked against Bitcoin Core's own test data. Every source read for this version was opened and read at %(now)s; every quotation is re-read from its saved copy by an executed claim; every number, identifier, encoding and output is recomputed under CPython 3.14.6 before the ontology states it." ;
    res:hasResearchScope chx:Scope ; rdfs:member %(members)s .
chx:Scope a res:ResearchScope ; res:hasResearchQuestion "How does chapter 7 of Mastering Bitcoin's 3rd edition describe the scripts, signature checks, timelocks, multisignatures, segregated witness and taproot by which an output asks for authorization, which of its statements and figures can be reproduced by running them through an interpreter checked against Bitcoin Core's tests, and where do the standards and the software differ from the text?" ; res:hasTimeWindow "Current as of %(day)s." .''' % dict(
    now=NOW, day=TODAY, members=", ".join("chx:" + p for p in PIDS)))

for pid, src in zip(PIDS, SOURCES):
    marker, cite, label, url, role, where = src
    L.append('chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; res:hasVerificationStatus res:Status_Verified ; '
             'sen0401:verifiedAt "%s"^^xsd:dateTime ; sen0401:sourceRole "%s" ; sen0401:savedAs "%s" .'
             % (pid, q(label), url, NOW, role, q(where)))

n = 0
for s in SECTIONS:
    n += 1
    L.append('chx:C_%02d a sen0401:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0401:conceptKind "Section" ; dcterms:source chx:P01 .' % (n, q(s)))
for t in TERMS:
    n += 1
    L.append('chx:C_%02d a sen0401:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0401:conceptKind "Concept" ; dcterms:source chx:P01 .' % (n, q(t)))

for i, (label, text, cites) in enumerate(F, 1):
    L.append('chx:F%d a sen0401:Finding ; rdfs:label "%s"@en ; sen0401:findingText "%s" ; sen0401:cites %s .'
             % (i, q(label), q(text), ", ".join("chx:" + c for c in cites)))

nchecks = len(CORPUS.CHECKS) + len(CORPUS.RAISES) + len(CORPUS.ERRORS)
nios = sum(1 for x in CORPUS.NODES if x[4] and x[4][2])
L.append('''chx:Scorecard a sen0401:QualityScorecard ; rdfs:label "Quality scorecard"@en ;
    sen0401:topicCoverage "%d primary-source items inventoried from the chapter: %d sections and %d named terms; the domain ontology built from them has %d concepts in %d branches." ;
    sen0401:citationStrength "%d sources, every one opened and read at %s and every one re-read from its saved copy by an executed claim; %d cited by findings." ;
    sen0401:methodologyCompliance "RDODI procedure v1.6.0 Stage 1; the chapter's claims are executed by 08-tooling/sen0401_chapter_build_v1_0_1.py before the ontology is written." ;
    sen0401:reproducibility "%d executed claims and %d worked examples, all under CPython 3.14.6; every source is a stable public URL or a saved evidence file named in the publication." .'''
         % (len(SECTIONS) + len(TERMS), len(SECTIONS), len(TERMS), len(CORPUS.NODES), sum(1 for x in CORPUS.NODES if x[2] == 1),
            len(SOURCES), NOW, len({c for _, _, cs in F for c in cs}), nchecks, nios))

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "sen0401_ch07_research_v1_0_0.ttl")
open(path, "w").write("\n".join(L) + "\n")

SHACL = '''@prefix chx:     <http://example.org/sen0401/ch07#> .
@prefix res:     <http://example.org/rdodi/research-ontology#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix doc:     <http://example.org/rdodi/document-ontology#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
<http://example.org/sen0401/ch07/shacl> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 7 domain ontology - shapes"@en ; owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0401/ch07/shacl/1.0.0> ;
    rdfs:comment "The four shapes of chapter 5 (version 1.0.1), written for chapter 7 under its own namespace and unchanged in content: every individual carries a label, a defined individual cites its source, an I/O example has exactly one input and one output, and a concept individual with a worked example carries exactly one definition. This is the chapter's first shapes file; it declares no prefix it does not use."@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%(day)s"^^xsd:date ; dcterms:modified "%(day)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch07_shacl_v1_0_0" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch07-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
chx:ExemplarShape a sh:NodeShape ; sh:targetClass owl:NamedIndividual ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "Every individual needs a label." ] .
chx:ExemplarSourcedShape a sh:NodeShape ; sh:targetSubjectsOf skos:definition ;
    sh:property [ sh:path dcterms:source ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "A defined individual must cite its source." ] .
chx:IOShape a sh:NodeShape ; sh:targetClass rd:IOExample ;
    sh:property [ sh:path chx:input ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one input." ] ;
    sh:property [ sh:path chx:output ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one output." ] .
chx:DefinitionShape a sh:NodeShape ; sh:targetSubjectsOf rd:hasIOExample ;
    sh:property [ sh:path skos:definition ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "A concept individual with a worked example needs exactly one definition." ] .
''' % dict(day=TODAY)
spath = os.path.join(OUT, "sen0401_ch07_domain_shacl_v1_0_0.ttl")
open(spath, "w").write(SHACL)

import rdflib
g = rdflib.Graph(); g.parse(path, format="turtle")
g2 = rdflib.Graph(); g2.parse(spath, format="turtle")
print("wrote %s: %d triples, %d publications, %d primary-source concepts, %d findings; %s: %d triples" % (
    os.path.basename(path), len(g), len(SOURCES), len(SECTIONS) + len(TERMS), len(F), os.path.basename(spath), len(g2)))
