#!/usr/bin/env python3
"""sen0401_register_make_v1_4_12 - writes 03-materials/sen0401_materials_v1_4_12.ttl from v1_4_11 (committed, untouched): adds the register entries (Deck, Doc, Ontology, Page) of chapter 11
(The Blockchain), each naming only files that exist on disk. Chapter 11 has no rendered .docx (only the document ontology, sen0401_ch11_document_v1_0_0.ttl), so its Doc entry names that file in the
Turtle format and says so; a .docx is not invented. The page it registers is 9.45.0 (template 9.46.0). Usage: sen0401_register_make_v1_4_12.py"""
__version__ = "1.0.0"
import glob, os, re, subprocess, zipfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials")
def one(pat):
    fs = sorted(glob.glob(os.path.join(M, "ch11", pat)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])
    if not fs: raise SystemExit("chapter 11 has no " + pat)
    return os.path.relpath(fs[-1], R)
deck = one("SEN0401_Ch11_*_3e_v*.pptx"); doct = one("rdodi/sen0401_ch11_document_v*.ttl")
ont = [one("rdodi/sen0401_ch11_%s_v*.ttl" % p) for p in ("research", "domain_tbox", "domain_abox", "domain_shacl")]
page = "03-materials/ch11/page/sen0401_ch11_page_v9_45_0.html"
n = len([x for x in zipfile.ZipFile(os.path.join(R, deck)).namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)])
cm = subprocess.run(["git", "-C", R, "log", "-1", "--format=%h", "--", deck], capture_output=True, text=True).stdout.strip()
rs = ("Registered in 1.4.12 from the deck file committed as %s: %d slides, read from the file on 2026-10-15; built for the third edition's chapter 11 (The Blockchain) with the chapter builder, to the CME materials "
      "look-and-feel standard v1.0.0 as that commit records. The register's author did not re-run the deck's checks. Slides 1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 19, 22 and 23 are marked Recorded (read from the record of the Bitcoin Core 31.1 "
      "nodes run on private chains), slides 19, 20, 21, 22 and 23 are marked NOT EXECUTED, and the pictures on slides 8, 21 and 23 are stand-ins and say so." % (cm, n))
add = '''
sen0401:Deck_Ch11_3e a schema:LearningResource ;
    dcterms:title "Chapter 11: The Blockchain - built for the third edition" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    cme:fileInPart "%(deck)s" ;
    cme:renewalStatus "%(rs)s" ;
    dcterms:source "%(o0)s; 08-tooling/sen0401_ch11_stories_v1_1_0.py (self-checked); 08-tooling/ch11-deck/examples_out_v1_0_0.json." ;
    cme:servesOutcome sen0401:LO6 .

sen0401:Doc_Ch11 a schema:LearningResource ;
    dcterms:title "The blockchain for an advanced course: RDODI document ontology for chapter 11 (no .docx was rendered)" ;
    dcterms:format "text/turtle" ;
    cme:fileInPart "%(doct)s" .

sen0401:Ontology_Ch11 a schema:LearningResource ;
    dcterms:title "Chapter 11 ontology package: research record and domain ontology" ;
    dcterms:format "text/turtle" ;
    cme:fileInPart %(parts)s ;
    cme:servesOutcome sen0401:LO6 .

sen0401:Page_Ch11 a schema:LearningResource ;
    dcterms:title "Chapter 11 interactive page, version 9.45" ;
    dcterms:format "text/html" ;
    cme:fileInPart "%(page)s" ;
    cme:servesOutcome sen0401:LO6 ;
    dcterms:source "%(o2)s" ;
    rdfs:comment "NO PAGE ABOX. The chapter's domain ABox is named as the source instead; a page ABox is not invented."@en .
''' % dict(deck=deck, rs=rs, o0=ont[0], o2=ont[2], doct=doct, page=page, parts=" ,\n                   ".join('"%s"' % p for p in ont))
s = open(os.path.join(M, "sen0401_materials_v1_4_11.ttl"), encoding="utf-8").read()
def rep(o, nw):
    global s
    assert s.count(o) == 1, o[:60]; s = s.replace(o, nw)
# 1.4.12 also corrects three titles that 1.4.11 gave chapter 10's entries with the wrong chapter number (9 instead of 10; the third is the title of chapter 10's ontology package); no other text of 1.4.11 is changed.
rep('"Chapter 9: The Bitcoin Network - built for the third edition"', '"Chapter 10: The Bitcoin Network - built for the third edition"')
rep('"Chapter 9 interactive page, version 9.44"', '"Chapter 10 interactive page, version 9.44"')
s = s.replace('sen0401:Ontology_Ch10 a schema:LearningResource ;\n    dcterms:title "Chapter 9 ontology package', 'sen0401:Ontology_Ch10 a schema:LearningResource ;\n    dcterms:title "Chapter 10 ontology package'); assert "Chapter 10 ontology package" in s
rep('owl:versionInfo "1.4.11" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.11> ;', 'owl:versionInfo "1.4.12" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.12> ;')
rep('prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.10> ;', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.11> ;')
rep('dcterms:identifier "sen0401_materials_v1_4_11" ;', 'dcterms:identifier "sen0401_materials_v1_4_12" ;')
rep("#  1.4.11 adds the register entries of chapter 10", "#  1.4.12 adds the register entries of chapter 11 (deck, document ontology, ontology package, page 9.45; no .docx exists for chapter 11) for the files that exist.\n#  1.4.11 adds the register entries of chapter 10")
s = s.rstrip("\n") + "\n" + add
open(os.path.join(M, "sen0401_materials_v1_4_12.ttl"), "w", encoding="utf-8").write(s)
import rdflib; print("triples", len(rdflib.Graph().parse(os.path.join(M, "sen0401_materials_v1_4_12.ttl"))))
