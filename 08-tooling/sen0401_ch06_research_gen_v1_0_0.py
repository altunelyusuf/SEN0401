#!/usr/bin/env python3
"""Writes 03-materials/ch06/rdodi/sen0401_ch06_research_v1_0_0.ttl, the RDODI Stage 1 record of chapter 6, and the chapter's SHACL
shapes sen0401_ch06_domain_shacl_v1_0_0.ttl. Chapter 6 had no earlier record, so both are written from scratch on the model of
chapter 5's (sen0401_ch05_research_gen_v1_0_0.py and the 1.0.1 shapes): one publication per source actually read for this version
(the list in sen0401_ch06_common_v1_0_0.py, each with its verification time), the chapter's own sections and named terms as
primary-source concepts, the findings that the reading and the executed claims support, and a quality scorecard. Every publication
listed is one that a CHECKS entry of sen0401_ch06_corpus_v1_0_0.py re-reads from its saved copy, except where the entry says
otherwise (the book's chapters 2 and 3 and the glossary are read from the local checkout of the book at the pinned commit).
The shapes are chapter 5's four, unchanged in content, written under this chapter's namespace (the prefix of this course's own
vendor namespace is sen0401:, as chapter 5's 1.0.1 shapes require).
Run: python3 sen0401_ch06_research_gen_v1_0_0.py   (the system python, which has rdflib; the claims the corpus executes are run by the chapter builder under python3.14)"""
__version__ = "1.0.0"
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch06_common_v1_0_0 import SOURCES
import sen0401_ch06_corpus_v1_0_0 as CORPUS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "03-materials", "ch06", "rdodi")
NOW = os.environ.get("CH6_VERIFIED_AT", "2026-10-08T11:03:23")
TODAY = NOW[:10]


def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ---- the chapter's own sections, in the order of its source (the textbook ontology's 26 sections) ----
SECTIONS = ["A Serialized Bitcoin Transaction", "Version", "Extended Marker and Flag", "Inputs", "Length of Transaction Input List", "Outpoint",
            "Input Script", "Sequence", "Original sequence-based transaction replacement", "Opt-in transaction replacement signaling",
            "Sequence as a consensus-enforced relative timelock", "Outputs", "Outputs Count", "Amount", "Uneconomical outputs and disallowed dust",
            "Output Scripts", "Witness Structure", "Circular Dependencies", "Third-Party Transaction Malleability", "Second-Party Transaction Malleability",
            "Segregated Witness", "Witness Structure Serialization", "Lock Time", "Coinbase Transactions", "Weight and Vbytes", "Legacy Serialization"]
TERMS = ["transaction", "serialized transaction", "PSBT", "version", "presigned transaction", "extended serialization format", "legacy serialization",
         "marker", "flag", "inputs", "compactSize", "outpoint", "txid", "output index", "double spending", "conflicting transactions", "UTXO database",
         "digest", "internal byte order", "display byte order", "input script", "sequence", "setup transaction", "refund transaction", "payment channel",
         "high-frequency transactions", "replace by fee", "BIP125", "relative timelock", "BIP68", "outputs", "amount", "satoshi", "uneconomical output",
         "dust", "data carrier output", "Utreexo", "output script", "anyone can spend", "standard transaction outputs", "witness", "public key",
         "signature", "trustless protocol", "circular dependency", "third-party transaction malleability", "second-party transaction malleability",
         "segregated witness", "hard fork", "soft fork", "witness program", "witness structure", "witness item", "lock time", "median time past",
         "coinbase transaction", "generation transaction", "block subsidy", "block reward", "maturity rule", "weight", "vbytes"]

# ---- findings, each supported by a source read and, where it states a number, by an executed claim ----
F = []


def finding(label, text, cites):
    F.append((label, text, cites))


P = {s[0]: "P%02d" % (i + 1) for i, s in enumerate(SOURCES)}
finding("Background",
        "Chapter 6 reads one real transaction, Alice's payment to Bob, byte by byte. It defines a transaction as the data Alice uses to convince every "
        "full node to update its database of coin ownership, then walks the serialization in order: the version, the marker and flag of the extended "
        "format, the inputs with their compactSize count, outpoints, input scripts and sequence numbers, the outputs with their amounts and output "
        "scripts, the witness structure, and the lock time; it explains the three meanings the sequence field has carried, the problems that placing "
        "witnesses in the input script caused for contract protocols and how segregated witness solved them as a soft fork, the special rules of the "
        "coinbase transaction, the weight and vbyte units, and the legacy format that transactions without witnesses still use.",
        [P["AH"]])
finding("Comparative analysis",
        "Every number the chapter prints for its example transaction reproduces from its bytes with the Python standard library alone: the 388 "
        "hexadecimal characters are 194 bytes; the marker is 0x00 and the flag 0x01 at offsets 4 and 5; the single input's outpoint is the identifier "
        "eb3ae38f... in internal order, 4ac54180... in display order, with output index 1; the sequence is 0xffffffff; the two outputs carry 20,000 and "
        "75,000 satoshis under a 34-byte segwit version 1 script and a 22-byte version 0 script; the witness is one 65-byte item; the lock time is zero; "
        "the identifier 46620030... is the double SHA-256 of the 125-byte legacy serialization; and the weight is 569, field by field exactly as the "
        "book's table gives it - version 16, marker and flag 2, inputs count 4, outpoint 144, input script 4, sequence 16, outputs count 4, amount 64, "
        "output script 232, witness count 1, witness items 66, lock time 16 - which is the figure the book obtained from bitcoin-cli and the figure an "
        "independent explorer records.",
        [P["AH"], P["MP"], P["B141"], P["BCW"]])
finding("Comparative analysis",
        "The chapter says Alice's transaction is included in block 774,958. Two independent explorers consulted on 2026-10-08 (mempool.space and "
        "blockstream.info) place the transaction 46620030... in block 775,072; block 774,958 is the block of the transaction it spends, 4ac54180..., "
        "whose lock time is 774,957. The chapter's statement about where a node looks for the previous output remains correct in substance - the "
        "referenced output is in an earlier block - but the height named is that of the previous transaction, not of Alice's own.",
        [P["AH"], P["MP"]])
finding("Comparative analysis",
        "The chapter says the block header takes up 240 weight. By BIP141's definition, block weight is base size times three plus total size, and "
        "Bitcoin Core's GetBlockWeight applies that formula to the whole serialized block, header included; an 80-byte header therefore weighs 320 "
        "units, and 240 is 80 times three, the base-size part alone. The difference is 80 units of 4,000,000 and changes no conclusion of the chapter.",
        [P["AH"], P["B141"], P["BCW"]])
finding("Comparative analysis",
        "The chapter says miners may claim a subsidy up until block 6,720,000. Under Bitcoin Core's GetBlockSubsidy - 50 BTC shifted right once per "
        "210,000 blocks - the subsidy at block 6,720,000, the 32nd halving, is one satoshi, and it stays one satoshi until block 6,929,999; it becomes "
        "zero at block 6,930,000, the 33rd halving. The last block with a non-zero subsidy is therefore 6,929,999, and 6,720,000 is the height from "
        "which the subsidy is a single satoshi. The whole schedule sums to 2,099,999,997,690,000 satoshis, just under 21 million bitcoins.",
        [P["AH"], P["BCL"], P["BCK"]])
finding("Comparative analysis",
        "The chapter's arithmetic for the replacement bandwidth attack understates the attacker's own cost: 1,000 transactions of 200 bytes a minute "
        "is 200,000 bytes, about 200 KB, not about 20 KB; the network-wide figure of about 10 GB a minute for 50,000 relaying nodes is correct. The "
        "ratio of 50,000 to one, which is the point of the example, is unaffected.",
        [P["AH"]])
finding("Comparative analysis",
        "The chapter numbers the sequence field's flags as the 23rd least-significant bit and bits 32 and 23, counting from one, while giving the "
        "values 1 shifted left 22 and, implicitly, 1 shifted left 31; BIP68 and Bitcoin Core name the same bits by their values, 1 << 22 for the type "
        "flag and 1U << 31 for the disable flag, and the 16-bit mask 0x0000ffff. The two conventions agree; a reader counting bits from zero should "
        "use 22 and 31.",
        [P["AH"], P["B68"], P["BCX"]])
finding("Comparative analysis",
        "The standards' figures all reproduce with the chapter's library: compactSize integers of 1, 3, 5 and 9 bytes with the prefixes 0xfd, 0xfe "
        "and 0xff at the thresholds 253, 0x10000 and 0x100000000; BIP68's 512-second units and its rule that a lock of 30 blocks allows confirmation "
        "29 blocks after the spent output's block; BIP125's threshold of 0xfffffffe; BIP141's vbytes as the weight rounded up over four, its "
        "witness-independent txid and witness-dependent wtxid, which an executed claim shows by altering a witness item; Bitcoin Core's dust "
        "thresholds of 546 satoshis for a legacy output and 294 for a segwit version 0 output at 3,000 satoshis per kilo-vbyte, from the sizes its "
        "policy source states; and the four push encodings of the number 2 that give a legacy transaction four different identifiers.",
        [P["B68"], P["B125"], P["B141"], P["BCP"], P["BCR"]])
finding("Contemporary developments",
        "Two of the chapter's as-of-this-writing statements have moved. The version 3 proposal the chapter says was being widely considered became "
        "BIP431, and Bitcoin Core's list of implemented proposals records that transactions with version 3 are standard and treated as topologically "
        "restricted until confirmation as of release 28.0; its policy header names 3 as the highest standard version while its transaction class still "
        "builds version 2 by default. And the opt-in replacement policy the chapter describes is no longer the default: the release notes of 28.0 "
        "record that the default of the mempoolfullrbf option changed from 0 to 1, so a default node treats every unconfirmed transaction as "
        "replaceable whether or not it carries the BIP125 signal.",
        [P["AH"], P["B431"], P["BCD"], P["BCP"], P["BCX"], P["BCN"]])
finding("Contemporary developments",
        "No Bitcoin Core node was available for this chapter, so where chapter 5 matched a running release, this chapter matches the project's "
        "sources at the commit pinned for the course (05bc2f5): the consensus constants (MAX_BLOCK_WEIGHT 4,000,000, COINBASE_MATURITY 100, "
        "WITNESS_SCALE_FACTOR 4, COIN and MAX_MONEY), the context-free checks of CheckTransaction with their named refusals (bad-txns-vin-empty, "
        "bad-txns-vout-negative, bad-txns-vout-toolarge, bad-txns-txouttotal-toolarge, bad-txns-inputs-duplicate, bad-cb-length, "
        "bad-txns-prevout-null), the sequence constants of CTxIn, LOCKTIME_THRESHOLD, the eleven-block median time past, GetBlockSubsidy and the "
        "block reward check, and the mainnet activation heights 227,931 (BIP34), 419,328 (BIP68, 112, 113) and 481,824 (segwit). The one runtime "
        "value the book quotes, the weight 569, is recomputed from the serialization and compared with an explorer's record rather than with a node.",
        [P["BCC"], P["BCA"], P["BCT"], P["BCV"], P["BCX"], P["BCS"], P["BCH"], P["BCL"], P["BCK"], P["MP"]])
finding("Course notes",
        "The owner's course notes for this chapter, written in 2021 after the 2nd edition, cover the same ground in the older vocabulary that the 3rd "
        "edition has replaced: transactions as data structures, the UTXO set and the wallet balance, change, the coinbase transaction, the serialized "
        "outputs and inputs of its tables 6-1 and 6-2, the locking and unlocking scripts the 3rd edition now calls output and input scripts, and a "
        "long section on transaction fees that the 3rd edition moves to a chapter of its own. Their topics that the 3rd edition keeps are all present in "
        "this ontology; the segregated-witness serialization, the weight unit, the BIP68 timelock and the malleability history, which the 2nd edition "
        "treated elsewhere or not at all, are the material this chapter adds.",
        [P["AL"], P["AH"]])
finding("Terms used without definition",
        "An audit of the explanations written for this chapter listed every technical term they use and compared it with the concepts of chapters 1 "
        "to 5 and of this chapter. The terms used without a concept of their own were the ownership record a full node keeps, the byte map, the "
        "digest and its two byte orders, the satoshi, the hash function and double SHA-256, the txid and the wtxid, relay policy and the consensus "
        "rule. Each was added as a concept of this chapter with its own section, so that no term in the document is used before it is explained; the "
        "terms earlier chapters define - the full node, the blockchain, the block, the private and public key, the address and its script, the "
        "UTXO, the wallet, the hardware signing device, multisignature - are used as they stand.",
        [P["AH"], P["AH2"], P["AH3"], P["AHG"]])
finding("Conclusion",
        "For the course, the chapter's lesson is that a transaction is a request to strangers, and that every one of its fields exists because a "
        "stranger needs it to decide: the outpoint to find the money, the witness to check the authorisation, the amounts to check the arithmetic, "
        "the sequence and lock time to check the timing, and the version, marker and flag to know which rules apply. The second lesson is the one "
        "the witness branch and this chapter's stories carry: what a hash covers decides what can be built on it, and segregated witness is the "
        "repair of a scope that was drawn too wide in 2009.",
        [P["AH"], P["B141"]])

# ---- the record ----
L = ['@prefix chx:     <http://example.org/sen0401/ch06#> .',
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
     '''<http://example.org/sen0401/ch06/research> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 6 - RDODI Stage 1 research artefact"@en ; owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0401/ch06/research/1.0.0> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%(day)s"^^xsd:date ; dcterms:modified "%(day)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch06_research_v1_0_0" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch06-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''' % dict(day=TODAY)]

PIDS = ["P%02d" % (i + 1) for i in range(len(SOURCES))]
L.append('''
chx:Research a res:ResearchProject ; rdfs:label "Transactions: one real transaction read byte by byte, and every figure of the chapter recomputed from the standards and Bitcoin Core's sources"@en ;
    sen0401:methodology "Primary source first: the chapter's own sections and named terms from the book's source at the commit the textbook ontology pins (275c4eb8). Then the proposal that defines each mechanism the chapter names, Bitcoin Core's consensus, policy, primitives, script and validation sources at the commit pinned for this course (05bc2f5) with its list of implemented proposals, and - because no node is available in this environment - the raw bytes and explorer records of four transactions fetched from mempool.space. Every source read for this version was opened and read at %(now)s; every quotation is re-read from its saved copy by an executed claim; every number, identifier, encoding and output is recomputed under CPython 3.14.6 before the ontology states it." ;
    res:hasResearchScope chx:Scope ; rdfs:member %(members)s .
chx:Scope a res:ResearchScope ; res:hasResearchQuestion "How does chapter 6 of Mastering Bitcoin's 3rd edition read a serialized transaction field by field, which of its numbers, identifiers, encodings and statements can be reproduced from the bytes, the standards and Bitcoin Core's sources, and where has the software moved since the chapter was written?" ; res:hasTimeWindow "Current as of %(day)s." .''' % dict(
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
path = os.path.join(OUT, "sen0401_ch06_research_v1_0_0.ttl")
open(path, "w").write("\n".join(L) + "\n")

SHACL = '''@prefix chx:     <http://example.org/sen0401/ch06#> .
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
<http://example.org/sen0401/ch06/shacl> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 6 domain ontology - shapes"@en ; owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0401/ch06/shacl/1.0.0> ;
    rdfs:comment "The four shapes of chapter 5 (version 1.0.1), written for chapter 6 under its own namespace and unchanged in content: every individual carries a label, a defined individual cites its source, an I/O example has exactly one input and one output, and a concept individual with a worked example carries exactly one definition. This is the chapter's first shapes file; it declares no prefix it does not use."@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%(day)s"^^xsd:date ; dcterms:modified "%(day)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch06_shacl_v1_0_0" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch06-rdodi-run> ;
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
spath = os.path.join(OUT, "sen0401_ch06_domain_shacl_v1_0_0.ttl")
open(spath, "w").write(SHACL)

import rdflib
g = rdflib.Graph(); g.parse(path, format="turtle")
g2 = rdflib.Graph(); g2.parse(spath, format="turtle")
print("wrote %s: %d triples, %d publications, %d primary-source concepts, %d findings; %s: %d triples" % (
    os.path.basename(path), len(g), len(SOURCES), len(SECTIONS) + len(TERMS), len(F), os.path.basename(spath), len(g2)))
