#!/usr/bin/env python3
"""sen0401_register_make_v1_4_14 - writes 03-materials/sen0401_materials_v1_4_14.ttl from v1_4_13 (committed, untouched): corrects the one date the chapter 3 deck entry carries - version 0.1 was announced on
the cryptography list on 8 January 2009 (list header Thu Jan 8 14:27:40 EST 2009, https://www.metzdowd.com/pipermail/cryptography/2009-January/014994.html), not on 9 January. Nothing else is changed: no
entry is added, withdrawn or repointed. Usage: sen0401_register_make_v1_4_14.py"""
__version__ = "1.0.0"
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); M = os.path.join(R, "03-materials")
s = open(os.path.join(M, "sen0401_materials_v1_4_13.ttl"), encoding="utf-8").read()
def rep(o, nw):
    global s
    assert s.count(o) == 1, o[:60]; s = s.replace(o, nw)
rep('owl:versionInfo "1.4.13" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.13> ;', 'owl:versionInfo "1.4.14" ;\n    owl:versionIRI <http://example.org/sen0401/materials/1.4.14> ;')
rep('prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.12> ;', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.13> ;')
rep('dcterms:identifier "sen0401_materials_v1_4_13" ;', 'dcterms:identifier "sen0401_materials_v1_4_14" ;')
rep("version 0.1 of 2009-01-09 drawn", "version 0.1 of 2009-01-08 drawn")
rep("#  1.4.13 adds the register entry", "#  1.4.14 corrects the date of the version 0.1 announcement in the chapter 3 deck entry (8 January 2009, the date in the list header, not 9 January); no other entry is changed: PATCH.\n#  1.4.13 adds the register entry")
open(os.path.join(M, "sen0401_materials_v1_4_14.ttl"), "w", encoding="utf-8").write(s)
import rdflib; print("triples", len(rdflib.Graph().parse(os.path.join(M, "sen0401_materials_v1_4_14.ttl"))))
