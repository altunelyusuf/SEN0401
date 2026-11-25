#!/usr/bin/env python3
"""Writes register 1.11.0 beside 1.10.0: registers the Chapter 4 deck 3.9.0 (code slides in the step-balloon layout), page 9.78 and chapter code 1.2.1. Records only (BP-D54, BP-D62 MINOR). Never edits 1.10.0. Usage: run in 03-materials."""
import os, sys
src = 'sen0401_materials_v1_10_0.ttl'; dst = 'sen0401_materials_v1_11_0.ttl'
if os.path.exists(dst): sys.exit('refuse: ' + dst + ' exists')
s = open(src, encoding='utf-8').read()
new = '''
sen0401:Deck_Ch04_3e_v3_9_0 a schema:LearningResource ;
    dcterms:title "Chapter 4: Keys and Addresses - deck 3.9.0" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    dcterms:replaces sen0401:Deck_Ch04_3e_v3_8_0 ;
    cme:fileInPart "03-materials/ch04/SEN0401_Ch04_KeysAndAddresses_3e_v3_9_0.pptx" ;
    cme:servesOutcome sen0401:LO4 ;
    rdfs:comment "Registered in 1.11.0. The 21 code slides carry a numbered step on each code box, a balloon with one sentence per step, the output line under the code and the result balloon, as in chapter 8; code, tables, charts and notes unchanged; the lambda stays taught on slide 10. Measured on 2026-11-26 against the deck standard v3.1.0 (twelve of twelve elements) and the CME material check v1.3.0 (9 of 9, lambda taught)."@en .

sen0401:Page_Ch04_v9_78_0 a schema:LearningResource ;
    dcterms:title "Chapter 4 interactive page, version 9.78" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:Page_Ch04_v9_77_0 ;
    cme:fileInPart "03-materials/ch04/page/sen0401_ch04_page_v9_78_0.html" ;
    cme:servesOutcome sen0401:LO4 ;
    rdfs:comment "Registered in 1.11.0. Follows the deck 3.9.0 through chapter code 1.2.1; code and mock exam are those of 9.77. The meta version of the page now equals its data version (9.77 had 9.75 in the meta tag)."@en .

sen0401:Companions_Ch04_1_11_0 a schema:LearningResource ;
    dcterms:title "Chapter 4 chapter code manifest 1.2.1" ;
    dcterms:format "application/json" ;
    cme:fileInPart "03-materials/ch04/page/chapter_code_ch04_v1_2_1.json" ;
    cme:servesOutcome sen0401:LO4 ;
    rdfs:comment "Registered in 1.11.0. The manifest of 1.2.0 with the deck reference changed to 3.9.0; the examples are unchanged."@en .
'''
c = '#  1.11.0 adds the register entries of the Chapter 4 deck 3.9.0 (step-balloon code slides), page 9.78 and chapter code 1.2.1; nothing is withdrawn: MINOR.\n'
a = '#  1.10.0 adds'; assert s.count(a) == 1; s = s.replace(a, c + a, 1)
s = s.replace('owl:versionInfo "1.10.0"', 'owl:versionInfo "1.11.0"').replace('materials/1.10.0>', 'materials/1.11.0>', 1)
s = s.replace('prov:wasRevisionOf <http://example.org/sen0401/materials/1.9.0>', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.10.0>', 1)
s = s.replace('dcterms:identifier "sen0401_materials_v1_10_0"', 'dcterms:identifier "sen0401_materials_v1_11_0"', 1)
open(dst, 'w', encoding='utf-8').write(s.rstrip('\n') + '\n' + new); print('wrote', dst)
