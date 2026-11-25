#!/usr/bin/env python3
"""Writes register 1.8.0 beside 1.7.0: registers the Chapter 3 deck 3.3.1, page 9.78, and the files that carry the pointers to Bitcoin Core (library 1.1.0 and its wheel, chapter code 1.2.1).
Records only (BP-D54 record set, BP-D62 MINOR: entries added, none removed). Never edits 1.7.0. Usage: run in 03-materials."""
import os, sys
src = 'sen0401_materials_v1_7_0.ttl'; dst = 'sen0401_materials_v1_8_0.ttl'
if os.path.exists(dst): sys.exit('refuse: ' + dst + ' exists')
s = open(src, encoding='utf-8').read()
new = '''
sen0401:Deck_Ch03_3e_v3_3_1 a schema:LearningResource ;
    dcterms:title "Chapter 3: Bitcoin Core - deck 3.3.1" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    dcterms:replaces sen0401:Deck_Ch03_3e_v3_3_0 ;
    cme:fileInPart "03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_3_1.pptx" ;
    cme:servesOutcome sen0401:LO3 ;
    rdfs:comment "Registered in 1.8.0. Only the module name of the library changes on the five code slides. Measured on 2026-11-25 against the deck standard v3.1.0 (twelve of twelve elements) and the CME material check v1.3.0 (9 of 9)."@en .

sen0401:Page_Ch03_v9_78_0 a schema:LearningResource ;
    dcterms:title "Chapter 3 interactive page, version 9.78" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:Page_Ch03_v9_77_0 ;
    cme:fileInPart "03-materials/ch03/page/sen0401_ch03_page_v9_78_0.html" ;
    cme:servesOutcome sen0401:LO3 ;
    rdfs:comment "Registered in 1.8.0. Embeds library 1.1.0 and chapter code 1.2.1; the 19 slide examples run and match their slides; the mock exam keeps opening its results."@en .

sen0401:Companions_Ch03_1_8_0 a schema:LearningResource ;
    dcterms:title "Chapter 3 library and chapter code with the pointers to Bitcoin Core" ;
    dcterms:format "application/octet-stream" ;
    cme:fileInPart "03-materials/ch03/assets/sen0401_ch03_lib-1.1.0-py3-none-any.whl" ,
                   "03-materials/ch03/page/chapter_code_ch03_v1_2_1.json" ,
                   "08-tooling/sen0401_ch03_core_lib_v1_1_0.py" ;
    cme:servesOutcome sen0401:LO3 ;
    rdfs:comment "Registered in 1.8.0. The library names, in its docstring, the Bitcoin Core source file and function each helper follows (each read in the source tree at commit 079437c); its behaviour is unchanged from 1.0.0."@en .
'''
c = '#  1.8.0 adds the register entries of the Chapter 3 deck 3.3.1, page 9.78 and the library, wheel and chapter code with the pointers to Bitcoin Core; nothing is withdrawn: MINOR.\n'
a = '#  1.7.0 adds'; assert s.count(a) == 1
s = s.replace(a, c + a, 1)
s = s.replace('owl:versionInfo "1.7.0"', 'owl:versionInfo "1.8.0"').replace('materials/1.7.0>', 'materials/1.8.0>', 1)
s = s.replace('prov:wasRevisionOf <http://example.org/sen0401/materials/1.6.0>', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.7.0>', 1)
s = s.replace('dcterms:identifier "sen0401_materials_v1_7_0"', 'dcterms:identifier "sen0401_materials_v1_8_0"', 1)
open(dst, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + new)
print('wrote', dst)
