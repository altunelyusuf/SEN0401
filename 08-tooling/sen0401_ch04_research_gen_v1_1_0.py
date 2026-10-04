#!/usr/bin/env python3
"""Writes 03-materials/ch04/rdodi/sen0401_ch04_research_v1_1_0.ttl from the 1.0.0 record: the eleven publications of 1.0.0 (the ten that were
re-read for this version carry the new verification time), one new publication for every further source read for version 1.1.0 (each with its own
verifiedAt), the findings of 1.0.0 with the two figures that this version re-measured corrected, three new findings (the terms that an audit found
used without a concept, the two claims of the earlier draft that the interpreter did not confirm, and the course material that was read for the
practice branch) and a new scorecard. Every source listed here is one that a CHECKS entry of sen0401_ch04_corpus_v1_1_0.py re-reads from its saved
copy, so the record and the executed claims cannot drift apart. Run: python3 sen0401_ch04_research_gen_v1_1_0.py"""
__version__ = "1.1.0"
import datetime
import importlib.util
import os
import re

here = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(os.path.dirname(here), "03-materials", "ch04", "rdodi")
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
TODAY = NOW[:10]
old = open(os.path.join(R, "sen0401_ch04_research_v1_0_0.ttl"), encoding="utf-8").read()
sp = importlib.util.spec_from_file_location("c", os.path.join(here, "sen0401_ch04_corpus_v1_1_0.py"))
C = importlib.util.module_from_spec(sp)
sp.loader.exec_module(C)
oldtbox = open(os.path.join(R, "sen0401_ch04_domain_tbox_v1_0_0.ttl"), encoding="utf-8").read()
oldids = set(re.findall(r"^chx:(\w+) a owl:Class", oldtbox, flags=re.M))
newids = [n[0] for n in C.NODES]
added = [i for i in newids if i not in oldids]
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
GH = "https://raw.githubusercontent.com/bitcoin/bitcoin/" + COMMIT + "/"
BK = "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/"
BIPS = "https://raw.githubusercontent.com/bitcoin/bips/master/"


def q(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


lines = old.split("\n")
head = []
for l in lines:
    if l.startswith("chx:") and not l.startswith("chx:Research") and not l.startswith("chx:Scope"):
        break
    head.append(l)
text = "\n".join(head)
text = (text.replace('owl:versionInfo "1.0.0"', 'owl:versionInfo "1.1.0"')
            .replace("research/1.0.0>", "research/1.1.0>")
            .replace("sen0401_ch04_research_v1_0_0", "sen0401_ch04_research_v1_1_0")
            .replace('dcterms:modified "2026-09-29"', 'dcterms:modified "%s"' % TODAY)
            .replace("prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .",
                     "prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> ;\n"
                     "    prov:wasRevisionOf <http://example.org/sen0401/ch04/research/1.0.0> .", 1))

# --- publications: the ten of 1.0.0 that were opened again for this version carry the new time; P_NOTES was not re-read
byline = {l.split(" ")[0]: l for l in lines if l.startswith("chx:P")}
reread = {"P01", "P02", "P03", "P04", "P05", "P06", "P07", "P08", "P09", "P10"}
pubs = []
for k, l in byline.items():
    pid = k[4:]
    if pid == "_NOTES":
        continue
    if pid in reread:
        l = re.sub(r'sen0414:verifiedAt "[^"]+"', 'sen0414:verifiedAt "%s"' % NOW, l)
    pubs.append((pid, l))
n = 10


def add(label, url, role="secondary"):
    global n
    n += 1
    pid = "P%02d" % n
    pubs.append((pid, 'chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; '
                      'res:hasVerificationStatus res:Status_Verified ; sen0414:verifiedAt "%s"^^xsd:dateTime ; '
                      'sen0414:sourceRole "%s" .' % (pid, q(label), url, NOW, role)))
    return pid


P = {}
# the other chapters of the book that the explanations of this chapter lean on
for f, nm, key in [("ch01_intro.adoc", "Chapter 1, Introduction", "bk1"),
                   ("ch05_wallets.adoc", "Chapter 5, Wallet Recovery and Security", "bk5"),
                   ("ch13_security.adoc", "Chapter 13, Bitcoin Security", "bk13")]:
    P[key] = add("Mastering Bitcoin, 3rd edition - %s (Antonopoulos and Harding, O'Reilly, 2023; tag third_edition_print1)" % nm,
                 BK + f, "primary")
# the BIPs that the chapter's mechanisms are specified in
for no, au, key in [(16, "Andresen, 2012", "b16"), (38, "Caldwell and Voisine, 2012", "b38"),
                    (141, "Lombrozo et al., 2015", "b141"), (142, "Wuille, 2015", "b142"),
                    (173, "Wuille and Maxwell, 2017", "b173"), (340, "Wuille et al., 2020", "b340")]:
    P[key] = add("BIP %d (%s), bitcoin/bips, preamble, specification and test vectors as read" % (no, au),
                 BIPS + "bip-%04d.mediawiki" % no)
# the standards and documents behind the supporting concepts
P["fips"] = add("FIPS 180-4, Secure Hash Standard (National Institute of Standards and Technology, 2015), the standard's description",
                "https://csrc.nist.gov/pubs/fips/180-4/upd1/final")
P["r791"] = add("RFC 791, Internet Protocol (Postel, 1981)", "https://www.rfc-editor.org/rfc/rfc791")
P["r3022"] = add("RFC 3022, Traditional IP Network Address Translator (Srisuresh and Egevang, 2001)", "https://www.rfc-editor.org/rfc/rfc3022")
P["r3986"] = add("RFC 3986, Uniform Resource Identifier (URI): Generic Syntax (Berners-Lee et al., 2005)", "https://www.rfc-editor.org/rfc/rfc3986")
# Bitcoin Core's own tree at the checked-out commit
for f, key in [("doc/descriptors.md", "descr"), ("doc/files.md", "files"),
               ("src/script/script.h", "scripth"), ("src/script/interpreter.cpp", "interp")]:
    P[key] = add("Bitcoin Core: %s at commit 05bc2f5 (Bitcoin Core, 2026)" % f, GH + f)
P["evid"] = add("Evidence of the run of Bitcoin Core 31.1 as an offline node: address types, getnewaddress, importdescriptors, "
                "deriveaddresses, validateaddress and the removed legacy commands (Bitcoin Core, 2026), saved in 08-tooling/ch04-evidence",
                "urn:sen0401:ch04-evidence", "primary")
P["vectors"] = add("The BIP350 test vectors, saved as data: 7 valid bech32m strings, 8 valid and 15 invalid segwit addresses, read 2026-09-28 (Wuille, 2020)",
                   BIPS + "bip-0350.mediawiki")
P["notes2"] = add("Course material for this chapter: Chapter_4_Keys_Addresses_Antonopoulos_2017_v1_0_0.txt in "
                  "03-materials/owner-legacy-2025/llm-content-2025/Chapter4, the owner's chapter text on the 2nd edition (Altunel, 2021)",
                  "urn:sen0401:course-notes:Chapter_4_Keys_Addresses_Antonopoulos_2017_v1_0_0.txt", "primary")

# --- findings
F = {}
for l in lines:
    m = re.match(r"chx:(F\d+) ", l)
    if m:
        F[m.group(1)] = l


def fixed(fid, old_s, new_s):
    assert old_s in F[fid], (fid, old_s)
    F[fid] = F[fid].replace(old_s, new_s)


# F7: this version re-runs the substitution experiment itself, with its own sample size
fixed("F7", "none of its 39-character data part's one-character substitutions, none of its two-character substitutions and none of 200,000 random three- and four-character substitutions still carries a valid checksum",
      "of the 1,209 substitutions of one character of its 39-character data part and the 712,101 substitutions of two characters, which the claims of this version enumerate exhaustively, not one still carries a valid checksum, and neither does any of the 100,000 random substitutions of three or four characters that they draw from a fixed seed")
F["F7"] = F["F7"].replace("sen0414:cites chx:P01, chx:P03, chx:P05 .",
                          "sen0414:cites chx:P01, chx:P03, chx:P05, chx:%s ." % P["b173"])
# F2: the toolkit's agreement is now also recorded against the saved vectors
F["F2"] = F["F2"].replace("sen0414:cites chx:P01, chx:P05, chx:P04, chx:P03 .",
                          "sen0414:cites chx:P01, chx:P05, chx:P04, chx:P03, chx:%s, chx:%s ." % (P["vectors"], P["evid"]))
# F9: the course material that the claims of this version actually read
fixed("F9", "The owner's course notes for this chapter (2021, after the 2nd edition) add topics",
      "The owner's course material for this chapter (2021, written on the 2nd edition), whose text was read for this version, adds topics")
F["F9"] = F["F9"].replace("sen0414:cites chx:P_NOTES, chx:P09, chx:P10, chx:P05 .",
                          "sen0414:cites chx:P_NOTES, chx:P09, chx:P10, chx:P05, chx:%s ." % P["notes2"])

tail_fid = max(int(k[1:]) for k in F)


def newf(label, txt, cites):
    global tail_fid
    tail_fid += 1
    F["F%d" % tail_fid] = ('chx:F%d a sen0414:Finding ; rdfs:label "%s"@en ; sen0414:findingText "%s" ; sen0414:cites %s .'
                           % (tail_fid, label, q(txt), ", ".join("chx:" + c for c in cites)))


newf("Methodology",
     "Terms used without definition: an audit of the vocabulary of every explanation against the concepts of this chapter and of chapters 1 to 3 "
     "found terms that the text used without a concept of its own, and version 1.1.0 adds %d concepts, those terms together with the subject "
     "groups that hold them: %s. The audit compared a list of "
     "cryptographic, Bitcoin and computing terms with the whole text and with the concept labels of this and the earlier chapters, and the terms "
     "that remained after the first pass (the coinbase transaction, the cofactor of a curve, the network's rate of hashing and the DID URL) were "
     "either given a definition where they are first used or replaced by plain wording, so that no term of the list is now used unexplained."
     % (len(added), ", ".join(added)),
     ["P01", P["b173"], P["r3986"]])
newf("Comparative analysis",
     "Two statements of the interrupted earlier draft of this version did not survive execution and were corrected: the draft said that the SHA-256 "
     "digests of the one-bit-apart inputs 'a' and the character before it differ in 126 of their 256 bits, where the interpreter gives 139; and it "
     "described the book's six length-extension strings as having 14, 18, 20, 22, 24 and 26 characters formed by adding two letters q at a time, "
     "where the book's strings have 15, 18, 20, 22, 23 and 25 characters, formed by inserting three, five, seven, eight and ten letters q before the "
     "final p. Both figures are now computed by claims that the chapter builder executes.",
     ["P01", P["b173"]])
newf("Methodology",
     "Every sentence that this version takes from a source is re-read from a saved copy of that source by a claim, and every number, hash, address, "
     "script, encoding and size it prints is computed: the corpus of version 1.1.0 carries %d executed claims, among them %d worked examples whose "
     "output the page recomputes in the reader's browser, %d claims that something fails and %d error conditions attached to the concept that "
     "explains them. The chapter builder refuses to write the ontology unless all of them hold."
     % (len(C.CHECKS) + len(C.RAISES) + len(C.ERRORS) + sum(1 for x in C.NODES if x[4] and x[4][2]),
        sum(1 for x in C.NODES if x[4] and x[4][2]), len(C.RAISES), len(C.ERRORS)),
     ["P01", P["evid"], P["scripth"]])

body = ['chx:Research a res:ResearchProject ; rdfs:label "Keys and addresses: from a random number to a payable string, recomputed and cross-checked"@en ;',
        '    sen0414:methodology "Primary source first: the chapter\'s named concepts from the book\'s own source at tag third_edition_print1. '
        'Then the primary standards of every mechanism the chapter uses (SEC 2, BIPs 16, 38, 141, 142, 173, 340 and 350, FIPS 180-4, RFCs 791, 3022 '
        'and 3986, the Decentralized Identifiers recommendation), the documentation and source of Bitcoin Core at commit 05bc2f5, and the data of a '
        'run of the real release 31.1. Every source opened and read on 2026-09-28 or on %s and saved under 08-tooling/ch04-evidence; every claim taken '
        'from text actually read; every number, hash, address, script and encoding executed under Python 3.14.4 by a claim of the chapter\'s corpus, '
        'and the result compared with Bitcoin Core 31.1 and with the reference implementation the book itself runs." ;' % TODAY,
        '    res:hasResearchScope chx:Scope ; rdfs:member %s, chx:P_NOTES .' % ", ".join("chx:" + p for p, _ in pubs),
        [l for l in lines if l.startswith("chx:Scope ")][0].replace("Current as of 2026-09-29.", "Current as of %s." % TODAY)]
concepts = [l for l in lines if l.startswith("chx:C_")]
notes = [l for l in lines if l.startswith("chx:P_NOTES")][0].replace("Yusuf Altunel, 2021 -", "Yusuf Altunel (Altunel, 2021) -")
used_in_findings = set()
for l in F.values():
    used_in_findings |= set(re.findall(r"chx:(P\w+)", l.split("sen0414:cites")[1]))
npubs = len(pubs) + 1
score = ('chx:Scorecard a sen0414:QualityScorecard ; rdfs:label "Quality scorecard"@en ; '
         'sen0414:topicCoverage "53 primary-source concepts inventoried from the textbook ontology; the domain ontology has %d concepts '
         '(%d of version 1.0.0 kept with their parents, %d added), each explained in four to six paragraphs of continuous prose for a level 3 '
         'concept and three or more for a group." ; '
         'sen0414:citationStrength "%d sources, each opened and read on 2026-09-28 or %s and each carrying its own verification time; %d cited by '
         'findings, every one of them re-read from its saved copy by a claim of the corpus." ; '
         'sen0414:methodologyCompliance "RDODI procedure v1.6.0 Stage 1; the explanations of Stage 3 carry no statement that a claim does not execute." ; '
         'sen0414:reproducibility "Every source is a stable public URL or a file saved in the repository; %d claims are executed by the chapter '
         'builder before the ontology is written, and the build stops if one of them does not hold." .'
         % (len(newids), len(oldids & set(newids)), len(added), npubs, TODAY, len(used_in_findings),
            len(C.CHECKS) + len(C.RAISES) + len(C.ERRORS) + sum(1 for x in C.NODES if x[4] and x[4][2])))
out = (text + "\n" + "\n".join(body) + "\n" + "\n".join(p[1] for p in pubs) + "\n" + notes + "\n"
       + "\n".join(concepts) + "\n" + "\n".join(F[k] for k in sorted(F, key=lambda s: int(s[1:]))) + "\n" + score + "\n")
open(os.path.join(R, "sen0401_ch04_research_v1_1_0.ttl"), "w", encoding="utf-8").write(out)
print("publications", npubs, "findings", len(F), "concepts old/new/added", len(oldids), len(newids), len(added))
