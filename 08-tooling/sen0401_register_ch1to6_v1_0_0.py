#!/usr/bin/env python3
"""Writes register 1.7.0 beside 1.6.0: registers the decks, pages and companion files of chapters 1 to 6 as renewed on 2026-11-25 to the standard of chapters 7 to 14
(owner request 2026-11-25: "finish the Chapters 1-6 now"). Records only (BP-D54 record set, BP-D62 MINOR: entries added, none removed). Never edits 1.6.0.
Usage: run in 03-materials."""
import re, os, glob, sys, subprocess
src = 'sen0401_materials_v1_6_0.ttl'; dst = 'sen0401_materials_v1_7_0.ttl'
if os.path.exists(dst): sys.exit('refuse: ' + dst + ' exists')
s = open(src, encoding='utf-8').read()
V = lambda f: tuple(map(int, re.search(r'_v(\d+)_(\d+)_(\d+)\.\w+$', f).groups()))
NAME = {1: 'Introduction', 2: 'How Bitcoin Works', 3: 'Bitcoin Core', 4: 'Keys and Addresses', 5: 'Wallet Recovery', 6: 'Transactions'}
CME = {1: '9 of 9', 2: '9 of 9', 3: '9 of 9', 4: '9 of 9, with the lambda taught on slide 10', 5: '9 of 9', 6: '9 of 9'}
NOPROMPT = {}
unt = subprocess.run(['git', 'show', '--name-only', '--diff-filter=A', '--pretty=format:', '335d322'], capture_output=True, text=True, cwd='..').stdout.split('\n')
unt = [l for l in unt if l]
new = []; notes = []
for c in range(1, 7):
    n = '%02d' % c
    deck = sorted(glob.glob('ch%s/*.pptx' % n), key=V)[-1]; page = sorted(glob.glob('ch%s/page/sen0401_ch%s_page_v*.html' % (n, n)), key=V)[-1]
    dv, pv = V(deck), V(page)
    prevdeck = 'Deck_Ch%s_3e' % n
    prevpage = sorted([x for x in re.findall(r'^sen0401:(Page_Ch%s_v[0-9_]+) a ' % n, s, re.M)], key=lambda x: tuple(map(int, re.findall(r'\d+', x.split('_v')[1]))))[-1]
    lo = re.search(r'sen0401:%s a .*?cme:servesOutcome (sen0401:LO\d+)' % prevdeck, s, re.S).group(1)
    new.append('''sen0401:Deck_Ch%s_3e_v%d_%d_%d a schema:LearningResource ;
    dcterms:title "Chapter %d: %s - deck %d.%d.%d" ;
    dcterms:format "application/vnd.openxmlformats-officedocument.presentationml.presentation" ;
    dcterms:replaces sen0401:%s ;
    cme:fileInPart "03-materials/%s" ;
    cme:servesOutcome %s ;
    rdfs:comment "Registered in 1.7.0. Measured on 2026-11-25 against the deck standard v3.1.0 (twelve of twelve elements) and the CME material check v1.3.0 (%s)."@en .
''' % (n, *dv, c, NAME[c], *dv, prevdeck, deck, lo, CME[c]))
    new.append('''sen0401:Page_Ch%s_v%d_%d_%d a schema:LearningResource ;
    dcterms:title "Chapter %d interactive page, version %d.%d" ;
    dcterms:format "text/html" ;
    dcterms:replaces sen0401:%s ;
    cme:fileInPart "03-materials/%s" ;
    cme:servesOutcome %s ;
    rdfs:comment "Registered in 1.7.0. Keeps the mock exam that opens its results; carries the chapter code with no prompts (book listings quoted inside the embedded book ontology are not page code and are not counted) and no lambda unless taught, the slide notes of the new deck, a top menu item that runs the slide examples in order, and the chapter library in a wheel that matches the library source (library match check: all match).%s"@en .
''' % (n, *pv, c, pv[0], pv[1], prevpage, page, lo, NOPROMPT.get(c, '')))
    comp = sorted(f for f in unt if f.startswith('03-materials/ch%s/' % n) and f not in ('03-materials/' + deck, '03-materials/' + page))
    comp += sorted(f for f in unt if re.match(r'08-tooling/sen0401_ch%s_lib_v[0-9_]+\.py$' % n, f))
    if comp:
        new.append('''sen0401:Companions_Ch%s_1_7_0 a schema:LearningResource ;
    dcterms:title "Chapter %d companion files of the 2026-11-25 renewal" ;
    dcterms:format "application/octet-stream" ;
    cme:fileInPart %s ;
    cme:servesOutcome %s ;
    rdfs:comment "Registered in 1.7.0. The chapter code manifest, the library wheel and source, and the new versions of the chapter ontology files that the page of chapter %d embeds, each beside the version it follows."@en .
''' % (n, c, ' ,\n                   '.join('"%s"' % f for f in comp), lo, c))
    notes.append((n, len(comp)))
s = s.replace('#  1.6.0 adds the register entries', '#  1.7.0 adds the register entries of the decks, pages and companion files of chapters 1 to 6 as renewed on 2026-11-25 to the standard of chapters 7 to 14 (owner request of 2026-11-25); nothing is withdrawn: MINOR.\n#  1.6.0 adds the register entries', 1)
s = s.replace('owl:versionInfo "1.6.0"', 'owl:versionInfo "1.7.0"').replace('materials/1.6.0>', 'materials/1.7.0>', 1)
s = s.replace('prov:wasRevisionOf <http://example.org/sen0401/materials/1.5.0>', 'prov:wasRevisionOf <http://example.org/sen0401/materials/1.6.0>', 1)
s = s.replace('dcterms:identifier "sen0401_materials_v1_6_0"', 'dcterms:identifier "sen0401_materials_v1_7_0"', 1)
s = s.rstrip('\n') + '\n\n' + '\n'.join(new)
open(dst, 'w', encoding='utf-8').write(s)
print(len(new), 'entries; companions per chapter', notes)
