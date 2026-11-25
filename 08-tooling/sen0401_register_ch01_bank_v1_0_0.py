#!/usr/bin/env python3
"""Writes register 1.8.0 beside 1.7.0: registers the Chapter 3 deck 3.3.1, page 9.78, and the files that carry the pointers to Bitcoin Core (library 1.1.0 and its wheel, chapter code 1.2.1).
Records only (BP-D54 record set, BP-D62 MINOR: entries added, none removed). Never edits 1.7.0. Usage: run in 03-materials."""
import os, sys
src = 'sen0401_materials_v1_8_0.ttl'; dst = 'sen0401_materials_v1_9_0.ttl'
if os.path.exists(dst): sys.exit('refuse: ' + dst + ' exists')
s = open(src, encoding='utf-8').read()
new = '''
sen0401:Page_Ch01_v9_77_0 a schema:LearningResource ;
    dcterms:title "Chapter 1 interactive page, version 9.77" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:Page_Ch01_v9_76_0 ;
    cme:fileInPart "03-materials/ch01/page/sen0401_ch01_page_v9_77_0.html" ;
    cme:servesOutcome sen0401:LO1 ;
    rdfs:comment "Registered in 1.9.0. The question bank holds 160 questions: the section Computing has again one question (about what a protocol fixes), which replaces the one removed with the wallet-and-browser comparison; answer positions are balanced 40/40/40/40. The 15 slide examples run and match their slides; the mock exam keeps opening its results."@en .

sen0401:Companions_Ch01_1_9_0 a schema:LearningResource ;
    dcterms:title "Chapter 1 question bank 1.2.0" ;
    dcterms:format "application/json" ;
    cme:fileInPart "08-tooling/ch01-page/question_bank_v1_2_0.json" ,
                   "08-tooling/sen0401_ch01_bank_v1_2_0_build_v1_0_0.py" ;
    cme:servesOutcome sen0401:LO1 ;
    rdfs:comment "Registered in 1.9.0. The bank of 159 questions on page 9.76 plus one question without an analogy for the section Computing."@en .
'''
c = '#  1.9.0 adds the register entries of the Chapter 1 page 9.77 and question bank 1.2.0; nothing is withdrawn: MINOR.\n'
a = '#  1.8.0 adds'; assert s.count(a) == 1
s = s.replace(a, c + a, 1)
s = s.replace('owl:versionInfo "1.8.0"', 'owl:versionInfo "1.9.0"').replace('materials/1.8.0>', 'materials/1.9.0>', 1)
s = s.replace('prov:wasRevisionOf <http://example.org/sen0401/materials/1.7.0>', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.8.0>', 1)
s = s.replace('dcterms:identifier "sen0401_materials_v1_8_0"', 'dcterms:identifier "sen0401_materials_v1_9_0"', 1)
open(dst, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + new)
print('wrote', dst)
