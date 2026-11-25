#!/usr/bin/env python3
"""Writes register 1.6.0 beside 1.5.0: registers the 14 chapter page versions that open the mock exam's results (owner request 2026-11-24).
Usage: run in 03-materials. Records only (BP-D54 record set, BP-D62 MINOR: entries added, none removed). Never edits 1.5.0."""
import re, os, glob, sys
src = 'sen0401_materials_v1_5_0.ttl'; dst = 'sen0401_materials_v1_6_0.ttl'
if os.path.exists(dst): sys.exit('refuse: ' + dst + ' exists')
s = open(src, encoding='utf-8').read()
ver = lambda f: tuple(map(int, re.search(r'_v(\d+)_(\d+)_(\d+)\.html$', f).groups()))
LO = {}
new = []
for c in range(1, 15):
    n = '%02d' % c
    files = sorted(glob.glob('ch%s/page/sen0401_ch%s_page_v*.html' % (n, n)), key=ver)
    f = files[-1]; v = ver(f); vs = '%d_%d_%d' % v
    sub = [x for x in re.findall(r'^sen0401:(Page_Ch%s(?:_v[0-9_]+)?) a ' % n, s, re.M)]
    prev = sorted(sub, key=lambda x: (len(x), x))[-1] if sub else None
    # the replaced entry is the one the register points at now: the highest-numbered Page_ChNN entry
    cand = [x for x in sub if x != 'Page_Ch%s' % n]
    if cand:
        prev = sorted(cand, key=lambda x: tuple(map(int, re.findall(r'\d+', x.split('_v')[1]))) if '_v' in x else (0,))[-1]
        prev = [x for x in cand if x.startswith('Page_Ch%s_v' % n)]
        prev = sorted(prev, key=lambda x: tuple(map(int, re.findall(r'\d+', x.split('_v')[1]))))[-1]
    else:
        prev = 'Page_Ch%s' % n
    lo = re.search(r'sen0401:%s a .*?cme:servesOutcome (sen0401:LO\d+)' % prev, s, re.S).group(1)
    new.append('''sen0401:Page_Ch%s_v%s a schema:LearningResource ;
    dcterms:title "Chapter %d interactive page, version %d.%d" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:%s ;
    cme:fileInPart "03-materials/%s" ;
    cme:servesOutcome %s ;
    rdfs:comment "Registered in 1.6.0. The mock exam opens its score, the correct answers and the corrections as soon as the student finishes (no release code); the exam and the results are two views; the same exam can be retaken as often as wished and every attempt is kept in the student's browser."@en .
''' % (n, vs, c, v[0], v[1], prev, f, lo))
s = s.replace('#  1.5.0 adds the register entries', '#  1.6.0 adds the register entries of the chapter pages 1 to 14 that open the mock exam results (owner request of 2026-11-24); nothing is withdrawn: MINOR.\n#  1.5.0 adds the register entries', 1)
s = s.replace('owl:versionInfo "1.5.0"', 'owl:versionInfo "1.6.0"').replace('materials/1.5.0>', 'materials/1.6.0>', 1)
s = s.replace('prov:wasRevisionOf <http://example.org/sen0401/materials/1.4.15>', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.5.0>', 1)
s = s.replace('dcterms:identifier "sen0401_materials_v1_5_0"', 'dcterms:identifier "sen0401_materials_v1_6_0"', 1)
s = s.replace('dcterms:modified "2026-10-15"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date', 1)
s = s.rstrip('\n') + '\n\n' + '\n'.join(new)
open(dst, 'w', encoding='utf-8').write(s)
print(len(new), 'entries')
