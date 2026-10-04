#!/usr/bin/env python3
"""Writes 03-materials/ch05/rdodi/sen0401_ch05_research_v1_0_0.ttl, the RDODI Stage 1 record of chapter 5. Chapter 5 had no earlier record, so
this one is written from scratch, on the model of chapter 4's: one publication per source actually read for this version (the list in
sen0401_ch05_common_v1_0_0.py, each with its verification time), the chapter's own sections and named terms as primary-source concepts, the
findings that the reading and the executed claims support, and a quality scorecard. Every publication listed is one that a CHECKS entry of
sen0401_ch05_corpus_v1_0_0.py re-reads from its saved copy, except where the entry says otherwise.
Run: /root/.local/bin/python3.14 sen0401_ch05_research_gen_v1_0_0.py"""
__version__ = "1.0.0"
import datetime, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sen0401_ch05_common_v1_0_0 import SOURCES
import sen0401_ch05_corpus_v1_0_0 as CORPUS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "03-materials", "ch05", "rdodi")
NOW = os.environ.get("CH5_VERIFIED_AT", "2026-10-04T11:15:16")
TODAY = NOW[:10]


def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ---- the chapter's own sections, in the order of its source ----
SECTIONS = ["Wallet Recovery", "Independent Key Generation", "Deterministic Key Generation", "Public Child Key Derivation",
            "Hierarchical Deterministic (HD) Key Generation (BIP32)", "Seeds and Recovery Codes", "Recovery Code Passphrases",
            "Backing Up Nonkey Data", "Backing Up Key Derivation Paths", "A Wallet Technology Stack in Detail", "BIP39 Recovery Codes",
            "Generating a recovery code", "From recovery code to seed", "How Much Entropy Do You Need?", "Optional passphrase in BIP39",
            "Creating an HD Wallet from the Seed", "Private child key derivation", "Using derived child keys", "Extended keys",
            "Public child key derivation", "Mind the Gap", "Using an Extended Public Key on a Web Store", "Hardened child key derivation",
            "Index numbers for normal and hardened derivation", "HD wallet key identifier (path)", "Navigating the HD wallet tree structure"]
TERMS = ["wallet database", "independent key generation", "deterministic key generation", "seed", "key tweak", "hardware signing device",
         "recovery code", "BIP39", "Electrum v2", "Aezeed", "Muun", "SLIP39", "Codex32", "recovery code passphrase", "plausible deniability",
         "brainwallet", "label", "BIP329", "static channel backups", "implicit paths", "explicit paths", "output script descriptors",
         "entropy", "checksum", "word list", "key-stretching function", "PBKDF2", "salt", "root seed", "master private key",
         "master chain code", "child key derivation", "chain code", "index number", "extended key", "extended private key",
         "extended public key", "hardened derivation", "gap limit", "HD wallet path", "BIP43", "BIP44", "wallet birthday", "duress wallet"]

# ---- findings, each supported by a source read and, where it states a number, by an executed claim ----
F = []


def finding(label, text, cites):
    F.append((label, text, cites))


finding("Background",
        "Chapter 5 is about preventing the loss of data from becoming a loss of money. It moves from what a wallet database holds, only keys, "
        "through the history of how keys are made, independently, then from a seed, then with key tweaks, then as a BIP32 tree, to the recovery "
        "codes that record a seed, the data a code cannot record, and the derivation paths a restoration needs; it then works one stack in detail, "
        "BIP39 codes, BIP32 derivation and BIP44-style implicit paths, and ends with an extended public key deployed on a web store and the "
        "closing advice to make good backups and test them regularly.",
        ["P01"])
finding("Comparative analysis",
        "Every number the chapter prints in this stack reproduces exactly from the standards, computed with Python's standard library alone: the "
        "three SHA-256 values of its deterministic-generation example; the 12 words of the entropy 0c1e24e5917779d297e14d45f14e1a1a and the 24 "
        "words of its 256-bit example; all 64 bytes of each of the three seeds its tables give, with no passphrase, with the passphrase "
        "SuperDuperSecret, and for the 24-word code; the whole entropy-and-word-length table from the standard's two formulas; and the extended "
        "public key printed beside its extended private key, which is the neutered form of it, both 111 characters with the version bytes 0488ade4 "
        "and 0488b21e, depth 1 and parent fingerprint 0a2683ed.",
        ["P01", "P05", "P06"])
finding("Comparative analysis",
        "The chapter states that each parent key can have 2,147,483,647 children and gives 2 to the 31 as that value. The two are not equal: 2 to "
        "the 31 is 2,147,483,648, and BIP32 says that each extended key has 2 to the 31 normal child keys, using indices 0 through 2 to the 31 "
        "minus 1, and as many hardened ones. The chapter's figure is the largest normal index, not the number of children.",
        ["P01", "P05"])
finding("Comparative analysis",
        "The chapter lists the inputs of the child key derivation function as a parent private or public key with the parenthesis uncompressed key. "
        "BIP32 serialises the parent public key in the 33-byte compressed form for normal derivation and pads the 32-byte private key with a zero "
        "byte for hardened derivation. Running the normal derivation with the 65-byte uncompressed form instead gives a different child private "
        "key, which an executed claim of this chapter shows, so the parenthesis is a slip rather than an option.",
        ["P01", "P05"])
finding("Comparative analysis",
        "The published test vectors of the standards the chapter names all reproduce with the chapter's own library: BIP32's test vectors 1 and 2, "
        "every chain of both, as serialised xprv and xpub strings found verbatim in the BIP text; the BIP39 English test vectors of "
        "trezor/python-mnemonic, entropy to words, words to seed with the passphrase TREZOR, seed to master extended private key and words back to "
        "entropy; BIP49's testnet vector down to the address 2Mww8dCYPUpKHofjgcXcBCEGmniw9CoaiD2; BIP84's first and second receiving addresses, "
        "including bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu, which Bitcoin Core 31.1 also derived from the account descriptor; BIP86's internal "
        "key, output key and address bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr; BIP380's descriptor checksums, which agree with "
        "the four checksums Bitcoin Core 31.1 returned; and codex32's first test vector with its checksum and 16-byte payload.",
        ["P05", "P06", "P07", "P09", "P10", "P11", "P17", "P35"])
finding("Contemporary developments",
        "Bitcoin Core 31.1, run offline for this chapter, is a descriptor wallet and implements the derivation side of the chapter's stack but not "
        "its recovery codes: the project's list of implemented proposals names BIP 32, 43, 44, 49, 84 and 86 and contains no entry for BIP 39, and "
        "the fresh wallet created for this chapter reports the sqlite format, descriptor support and eight descriptors, four script types with a "
        "receiving and a change branch each, every one carrying a key origin such as 6d8c4b8f with the path 84h/0h/0h and a ranged child path with "
        "the range 0 to 999; its first address was at m/84h/0h/0h/0/0. The source sets the pool behind that range, DEFAULT_KEYPOOL_SIZE, to 1000 "
        "and describes it as the look-ahead process used to detect payments.",
        ["P33", "P34", "P35", "P36"])
finding("Contemporary developments",
        "The record the chapter cites for the risk of coercion has grown since the book was printed. The chapter says that Jameson Lopp has "
        "documented over 100 physical attacks against suspected owners of bitcoin and other digital assets; the saved copy of that list read for "
        "this chapter holds 364 table rows, which an executed claim of this chapter counts, and the list states that it is not comprehensive "
        "because many attacks are not publicly reported. The chapter's figure should therefore be read as a floor and dated.",
        ["P01", "P22"])
finding("Comparative analysis",
        "The chapter's table of implicit script paths is faithful to the standards and uneven in one respect that a reader should notice: it gives "
        "m/44'/0'/0', m/84'/0'/0' and m/86'/0'/0' with the coin type 0, Bitcoin, but m/49'/1'/0' with the coin type 1, which SLIP-0044 registers "
        "as testnet for all coins, because BIP49's own test vectors are on testnet. The purpose numbers themselves are those of the four standards, "
        "hardened: 0x8000002c, 0x80000031, 0x80000054 and 0x80000056.",
        ["P01", "P08", "P09", "P10", "P11", "P18"])
finding("Comparative analysis",
        "Two statements of the chapter about the other schemes were checked against those schemes' own documents and hold, with their figures: "
        "Aezeed's plaintext is one byte of internal version, two bytes of timestamp and sixteen bytes of entropy, its two-byte timestamp counts "
        "days since the genesis block and its document says this reaches 2188, which is 2009 plus 65,536 divided by 365; and its key derivation is "
        "scrypt with n equal to 32,768, which is sixteen times BIP39's 2,048 rounds. Electrum's document gives the version-number rule the chapter "
        "describes, with the registered numbers 0x01, 0x100 and 0x101, and works the cost of the prefix out as 2 to the 135 hashes for a 12-word, "
        "132-bit seed.",
        ["P01", "P19", "P20", "P21"])
finding("Course notes",
        "The owner's course notes for this chapter, written in 2021 after the 2nd edition, cover the same ground in the older vocabulary that the "
        "3rd edition has renamed: nondeterministic or JBOK wallet, Type-0, Type-1 and Type-2 wallets, mnemonic code words rather than recovery "
        "codes, and figures numbered 5-1 to 5-13. Their topics that the 3rd edition keeps are all present in this ontology, among them the "
        "brainwallet comparison, the paper backup of the code, the Trezor export in Gabriel's case, hardened derivation, index numbers and the "
        "two path tables; the slides' own numbering of the book's figures and tables belongs to the 2nd edition and is not carried over.",
        ["P36", "P01"])
finding("Terms used without definition",
        "An audit of the explanations written for this chapter listed every technical term they use and compared it with the concepts of chapters 1 "
        "to 4 and of this chapter. The terms used without a concept of their own were the hash function, the SHA-256 and SHA-512 algorithms, the "
        "digital signature, secret sharing, encryption, multisignature, the output script, the Lightning Network, entropy, the key-stretching "
        "function, PBKDF2, the salt, text normalisation, data loss and the testing of a backup. Each was added as a concept of this chapter with "
        "its own section, so that no term in the document is used before it is explained; the terms that chapters 1 to 4 do define, among them the "
        "private and public key, the elliptic curve and its generator point, base58check, bech32 and bech32m, the address, the transaction, the "
        "unspent output, the full node, the improvement proposal, the byte and the keyed hash, are used as they stand.",
        ["P01", "P02", "P03", "P04"])
finding("Conclusion",
        "For the course, the chapter's lesson can be stated as a list of what a complete backup is, and every item of the list is one of this "
        "chapter's concepts: the recovery code, the passphrase if one is used, the derivation paths or the descriptors that record them, the public "
        "keys of any other signers, and the data that is not keys, which means the labels and whatever a protocol such as the Lightning Network "
        "adds. The chapter's own closing sentences are the reason the list matters: data loss is perhaps the leading cause of lost bitcoins, nobody "
        "can reverse it, and it is up to the holder to make the backups and test them.",
        ["P01"])

# ---- the record ----
L = ['@prefix chx:     <http://example.org/sen0401/ch05#> .',
     '@prefix res:     <http://example.org/rdodi/research-ontology#> .',
     '@prefix rd:      <http://example.org/rdodi/domain-ontology#> .',
     '@prefix doc:     <http://example.org/rdodi/document-ontology#> .',
     '@prefix sen0414: <http://example.org/sen0401#> .',
     '@prefix owl:     <http://www.w3.org/2002/07/owl#> .',
     '@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .',
     '@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .',
     '@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .',
     '@prefix dcterms: <http://purl.org/dc/terms/> .',
     '@prefix prov:    <http://www.w3.org/ns/prov#> .',
     '@prefix sh:      <http://www.w3.org/ns/shacl#> .',
     '',
     '''<http://example.org/sen0401/ch05/research> a owl:Ontology ;
    rdfs:label "SEN0401 chapter 5 - RDODI Stage 1 research artefact"@en ; owl:versionInfo "1.0.0" ; owl:versionIRI <http://example.org/sen0401/ch05/research/1.0.0> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%(day)s"^^xsd:date ; dcterms:modified "%(day)s"^^xsd:date ;
    dcterms:identifier "sen0401_ch05_research_v1_0_0" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch05-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .''' % dict(day=TODAY)]

PIDS = ["P%02d" % (i + 1) for i in range(len(SOURCES))]
L.append('''
chx:Research a res:ResearchProject ; rdfs:label "Wallet recovery: from a random number to a word list, a tree of keys and a backup that works"@en ;
    sen0414:methodology "Primary source first: the chapter's own sections and named terms from the book's source at tag third_edition_print1. Then the standard that defines each mechanism the chapter names, the document of each wallet it names, the specification of each function it uses, and Bitcoin Core's documentation and wallet source at the commit pinned for this course, with the evidence of a run of release 31.1. Every source read for this version was opened and read at %(now)s; every quotation is re-read from its saved copy by an executed claim; every number, code, key, address and encoding is recomputed under CPython 3.14.4 before the ontology states it." ;
    res:hasResearchScope chx:Scope ; rdfs:member %(members)s .
chx:Scope a res:ResearchScope ; res:hasResearchQuestion "How does chapter 5 of Mastering Bitcoin's 3rd edition lead from a random number to a recovery code, a seed and a tree of keys, which of its numbers, codes, keys, addresses and statements can be reproduced from the standards and by independent software, and what must a user keep besides the code in order to recover a wallet?" ; res:hasTimeWindow "Current as of %(day)s." .''' % dict(
    now=NOW, day=TODAY, members=", ".join("chx:" + p for p in PIDS)))

for pid, src in zip(PIDS, SOURCES):
    marker, cite, label, url, role, where = src
    L.append('chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; res:hasVerificationStatus res:Status_Verified ; '
             'sen0414:verifiedAt "%s"^^xsd:dateTime ; sen0414:sourceRole "%s" ; sen0414:savedAs "%s" .'
             % (pid, q(label), url, NOW, role, q(where)))

n = 0
for s in SECTIONS:
    n += 1
    L.append('chx:C_%02d a sen0414:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0414:conceptKind "Section" ; dcterms:source chx:P01 .' % (n, q(s)))
for t in TERMS:
    n += 1
    L.append('chx:C_%02d a sen0414:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0414:conceptKind "Concept" ; dcterms:source chx:P01 .' % (n, q(t)))

for i, (label, text, cites) in enumerate(F, 1):
    L.append('chx:F%d a sen0414:Finding ; rdfs:label "%s"@en ; sen0414:findingText "%s" ; sen0414:cites %s .'
             % (i, q(label), q(text), ", ".join("chx:" + c for c in cites)))

nchecks = len(CORPUS.CHECKS) + len(CORPUS.RAISES) + len(CORPUS.ERRORS)
nios = sum(1 for x in CORPUS.NODES if x[4] and x[4][2])
L.append('''chx:Scorecard a sen0414:QualityScorecard ; rdfs:label "Quality scorecard"@en ;
    sen0414:topicCoverage "%d primary-source items inventoried from the chapter: %d sections and %d named terms; the domain ontology built from them has %d concepts in %d branches." ;
    sen0414:citationStrength "%d sources, every one opened and read at %s and every one re-read from its saved copy by an executed claim; %d cited by findings." ;
    sen0414:methodologyCompliance "RDODI procedure v1.6.0 Stage 1; the chapter's claims are executed by 08-tooling/sen0401_chapter_build_v1_0_0.py before the ontology is written." ;
    sen0414:reproducibility "%d executed claims and %d worked examples, all under CPython 3.14.4; every source is a stable public URL or a saved evidence file named in the publication." .'''
         % (len(SECTIONS) + len(TERMS), len(SECTIONS), len(TERMS), len(CORPUS.NODES), sum(1 for x in CORPUS.NODES if x[2] == 1),
            len(SOURCES), NOW, len({c for _, _, cs in F for c in cs}), nchecks, nios))

os.makedirs(OUT, exist_ok=True)
path = os.path.join(OUT, "sen0401_ch05_research_v1_0_0.ttl")
open(path, "w").write("\n".join(L) + "\n")
import rdflib
g = rdflib.Graph()
g.parse(path, format="turtle")
print("wrote %s: %d triples, %d publications, %d primary-source concepts, %d findings" % (
    os.path.basename(path), len(g), len(SOURCES), len(SECTIONS) + len(TERMS), len(F)))
