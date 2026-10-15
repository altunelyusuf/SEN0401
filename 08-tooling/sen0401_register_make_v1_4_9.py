#!/usr/bin/env python3
"""sen0401_register_make_v1_4_9 - writes 03-materials/sen0401_materials_v1_4_9.ttl from v1_4_8 (committed, untouched): adds the register entries (Deck, Doc, Ontology, Page) of chapters 6, 7 and 8, each
naming only files that exist on disk (the newest of each, found as sen0401_register_fragment_v1_0_0.py finds them); chapter 8's page is the one this version registers (page 9.42, template 9.45.0).
Usage: sen0401_register_make_v1_4_9.py"""
__version__ = "1.0.0"
import glob, os, re, subprocess, zipfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials")
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def newest(n, pat):
    fs = sorted(glob.glob(os.path.join(M, "ch" + n, pat)), key=vk)
    return os.path.relpath(fs[-1], R) if fs else None
def slides(p): return len([x for x in zipfile.ZipFile(os.path.join(R, p)).namelist() if re.match(r"ppt/slides/slide\d+\.xml$", x)])
def commit(p): return subprocess.run(["git", "-C", R, "log", "-1", "--format=%h", "--", p], capture_output=True, text=True).stdout.strip()
TITLES = {"06": ("Transactions", "Transactions for an advanced course: RDODI document for chapter 6"), "07": ("Authorization and Authentication", "Authorization and authentication for an advanced course: RDODI document for chapter 7"),
          "08": ("Digital Signatures", "Digital signatures for an advanced course: RDODI document for chapter 8")}
def entry(n):
    c = int(n); t, dt = TITLES[n]
    deck = newest(n, "SEN0401_Ch%s_*_3e_v*.pptx" % n); docx = newest(n, "rdodi/sen0401_ch%s_document_v*.docx" % n); doct = newest(n, "rdodi/sen0401_ch%s_document_v*.ttl" % n)
    ont = [newest(n, "rdodi/sen0401_ch%s_%s_v*.ttl" % (n, p)) for p in ("research", "domain_tbox", "domain_abox", "domain_shacl")]
    page = "03-materials/ch08/page/sen0401_ch08_page_v9_42_0.html" if n == "08" else newest(n, "page/sen0401_ch%s_page_v*.html" % n)
    for k, v in (("deck", deck), ("docx", docx), ("doct", doct), ("research", ont[0]), ("tbox", ont[1]), ("abox", ont[2]), ("shacl", ont[3])):
        if not v: raise SystemExit("chapter %s has no %s" % (n, k))
    if n != "08" and not os.path.exists(os.path.join(R, page)): raise SystemExit("no page for chapter " + n)
    pv = ".".join(re.findall(r"_v(\d+)_(\d+)_(\d+)", page)[-1][:2])
    stories = "08-tooling/sen0401_ch%s_stories_v1_0_0.py" % n if n != "08" else "08-tooling/sen0401_ch08_stories_v1_1_0.py"
    ex = "08-tooling/ch%s-deck/examples_out_v1_0_0.json" % n
    rs = ("Registered in 1.4.9 from the deck file committed as %s: %d slides, read from the file on 2026-10-15; built for the third edition's chapter %d (%s) with the chapter builder, to the CME materials look-and-feel standard v1.0.0 as that commit records. "
          "The register's author did not re-run the deck's checks." % (commit(deck), slides(deck), c, t))
    if n == "08": rs += (" Slides 1, 7, 8, 18 and 22 are marked Recorded (read from one run of Bitcoin Core 31.1.0 on a test network), slides 12 and 23 are marked NOT EXECUTED, and the pictures on slides 17 and 19 are stand-ins and say so.")
    out = '''sen0401:Deck_Ch%(n)s_3e a schema:LearningResource ;
    dcterms:title "Chapter %(c)d: %(t)s - built for the third edition" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    cme:fileInPart "%(deck)s" ;
    cme:renewalStatus "%(rs)s" ;
    dcterms:source "%(ont0)s; %(stories)s (self-checked); %(ex)s." ;
    cme:servesOutcome sen0401:LO6 .

sen0401:Doc_Ch%(n)s a schema:LearningResource ;
    dcterms:title "%(dt)s" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;
    cme:fileInPart "%(docx)s" ;
    dcterms:source "%(doct)s" .

sen0401:Ontology_Ch%(n)s a schema:LearningResource ;
    dcterms:title "Chapter %(c)d ontology package: research record and domain ontology" ;
    dcterms:format "text/turtle" ;
    cme:fileInPart %(parts)s ;
    cme:servesOutcome sen0401:LO6 .

sen0401:Page_Ch%(n)s a schema:LearningResource ;
    dcterms:title "Chapter %(c)d interactive page, version %(pv)s" ;
    dcterms:format "text/html" ;
    cme:fileInPart "%(page)s" ;
    cme:servesOutcome sen0401:LO6 ;
    dcterms:source "%(ont2)s" ;
    rdfs:comment "NO PAGE ABOX. The chapter's domain ABox is named as the source instead; a page ABox is not invented."@en .
''' % dict(n=n, c=c, t=t, dt=dt, deck=deck, rs=rs, ont0=ont[0], ont2=ont[2], stories=stories, ex=ex, docx=docx, doct=doct, pv=pv, page=page, parts=" ,\n                   ".join('"%s"' % p for p in ont))
    return out
s = open(os.path.join(M, "sen0401_materials_v1_4_8.ttl"), encoding="utf-8").read()
def rep(o, n):
    global s
    assert s.count(o) == 1, o[:60]; s = s.replace(o, n)
rep('owl:versionInfo "1.4.8" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.8> ;\n    prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.7> ;\n    dcterms:identifier "sen0401_materials_v1_4_8" ;',
    'owl:versionInfo "1.4.9" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.9> ;\n    prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.8> ;\n    dcterms:identifier "sen0401_materials_v1_4_9" ;')
rep('dcterms:modified "2026-10-07"^^xsd:date ;', 'dcterms:modified "2026-10-15"^^xsd:date ;')
rep("#  1.4.8 repoints the five interactive pages", "#  1.4.9 adds the register entries of chapters 6, 7 and 8 (deck, document, ontology package, page) for the files that exist: chapters 6 and 7 were built\n#  before the register named them (their pages are the 9.41.0 files, their decks the v1_1_0 files), and chapter 8 is new (research commit 4102ded, deck commit\n#  c682aac, page 9.42 on template 9.45.0). No existing entry is changed: MINOR.\n#  1.4.8 repoints the five interactive pages")
s = s.rstrip("\n") + "\n\n" + "\n".join(entry(n) for n in ("06", "07", "08"))
open(os.path.join(M, "sen0401_materials_v1_4_9.ttl"), "w", encoding="utf-8").write(s)
import rdflib; print("triples", len(rdflib.Graph().parse(os.path.join(M, "sen0401_materials_v1_4_9.ttl"))))
