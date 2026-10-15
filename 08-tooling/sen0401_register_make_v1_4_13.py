#!/usr/bin/env python3
"""sen0401_register_make_v1_4_13 - writes 03-materials/sen0401_materials_v1_4_13.ttl from v1_4_12 (committed, untouched): adds the register entry of the chapter 9 page 9.46.0 (Page_Ch09_v9_46), which
supersedes the entry Page_Ch09 (page 9.43.0, commit 2b43edc). The new page is built from research package v1_0_1 (ef4a8d5) and its wheel carries no text whose terms of redistribution are unclear. Nothing else
in 1.4.12 is changed. Usage: sen0401_register_make_v1_4_13.py"""
__version__ = "1.0.0"
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials")
page = "03-materials/ch09/page/sen0401_ch09_page_v9_46_0.html"; abox = "03-materials/ch09/rdodi/sen0401_ch09_domain_abox_v1_0_1.ttl"
assert os.path.exists(os.path.join(R, abox))  # the page file itself is built after the register (the page embeds the register), so its existence is checked by the caller
add = '''
sen0401:Page_Ch09_v9_46 a schema:LearningResource ;
    dcterms:title "Chapter 9 interactive page, version 9.46 (rebuilt)" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:Page_Ch09 ;
    cme:fileInPart "%s" ;
    cme:servesOutcome sen0401:LO6 ;
    dcterms:source "%s" ;
    rdfs:comment "Registered in 1.4.13. Supersedes the page 9.43.0 of commit 2b43edc: built from the research package v1_0_1 (the nine example texts whose quotes the first package had rewritten are valid again, two examples that were recorded now run) and on a wheel that does not carry the full text of Carlsten et al. 2016, Moeser and Boehme 2015, the Corallo post of 2018 or the mempool.space market data (terms of redistribution not clear); the examples that read them are shown as recorded. NO PAGE ABOX. The chapter's domain ABox is named as the source instead; a page ABox is not invented."@en .
''' % (page, abox)
s = open(os.path.join(M, "sen0401_materials_v1_4_12.ttl"), encoding="utf-8").read()
def rep(o, nw):
    global s
    assert s.count(o) == 1, o[:60]; s = s.replace(o, nw)
rep('owl:versionInfo "1.4.12" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.12> ;', 'owl:versionInfo "1.4.13" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.13> ;')
rep('prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.11> ;', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.12> ;')
rep('dcterms:identifier "sen0401_materials_v1_4_12" ;', 'dcterms:identifier "sen0401_materials_v1_4_13" ;')
rep("#  1.4.12 adds the register entries of chapter 11", "#  1.4.13 adds the register entry of the rebuilt chapter 9 page 9.46 (Page_Ch09_v9_46), which supersedes the entry of page 9.43 (commit 2b43edc); no other entry is changed.\n#  1.4.12 adds the register entries of chapter 11")
s = s.rstrip("\n") + "\n" + add
open(os.path.join(M, "sen0401_materials_v1_4_13.ttl"), "w", encoding="utf-8").write(s)
import rdflib; print("triples", len(rdflib.Graph().parse(os.path.join(M, "sen0401_materials_v1_4_13.ttl"))))
