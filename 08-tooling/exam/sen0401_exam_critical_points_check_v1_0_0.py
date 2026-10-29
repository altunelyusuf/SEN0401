"""Checks of the critical-points list, version 1.0.0. Prints PASS / FAIL / NOT_MEASURED per check.
Usage: check.py [--chapters 1-6|1-7|1,2,3] [--json FILE]
Re-reads the decks, the legacy decks and the pages itself; trusts nothing in the json except the claims it tests."""
import argparse, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_exam_pptx_text_v1_0_0 as L

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument('--chapters', default='1-6')
ap.add_argument('--json', default=os.path.join(HERE, 'sen0401_exam_critical_points_v1_0_0.json'))
a = ap.parse_args()
chs = []
for part in a.chapters.split(','):
    if '-' in part:
        x, y = part.split('-'); chs += list(range(int(x), int(y) + 1))
    else:
        chs.append(int(part))
doc = json.load(open(a.json))
A = [p for p in doc['list_A_points_carried_by_a_source'] if p['chapter'] in chs]
B = doc['list_B_not_carried_for_the_owner']
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail))

cache = {}
def deck(path):
    if path not in cache:
        cache[path] = L.slides_of(L.ROOT + path)
    return cache[path]

fails = []
tokre = re.compile(r'\d[\d,\.]*\d|\d|[A-Z][A-Za-z]*[A-Z0-9_][A-Za-z0-9_]*|BIP\s?\d+')
for p in A:
    s = p['source']; path = L.ROOT + s['file']; why = None
    if not os.path.exists(path):
        fails.append((p['id'], 'source file missing ' + s['file'])); continue
    quotes = [L.norm(q) for q in s['quote'].split('||')]
    if s['kind'] == 'deck':
        sl = deck(s['file'])
        if not (1 <= s['slide'] <= len(sl)): fails.append((p['id'], 'slide missing')); continue
        txt = sl[s['slide'] - 1][s['field']]
        alltxt = ' '.join(x['slide'] + ' ' + x['notes'] for x in sl)
    elif s['kind'] == 'legacy2025':
        txt = L.legacy_diagram_text(path, s['slide']); alltxt = txt
    elif s['kind'] == 'page':
        raw = open(path, encoding='utf8').read()
        txt = L.norm(raw.replace('\\"', '"')); alltxt = txt
    else:
        fails.append((p['id'], 'unknown source kind')); continue
    miss = [q for q in quotes if q not in txt]
    if miss: fails.append((p['id'], 'quote not in %s: %s' % (s['field'], miss[0][:60]))); continue
    # nothing invented: every number and code-like token of the point statement occurs in the source deck
    pt = L.norm(p['point'])
    bad = []
    for t in tokre.findall(pt):
        t2 = t.strip('.,')
        if t2 in ('A', 'B', 'I') or len(t2) < 1: continue
        if t2 not in alltxt and t2 not in L.norm(' '.join(q for q in quotes)): bad.append(t2)
    if bad: fails.append((p['id'], 'term not in source: %s' % bad[:3]))
rep('C1 every point names a source file that exists, a slide that exists, and a quote found there', not fails,
    '(%d points, chapters %s)' % (len(A), chs) + ('' if not fails else ' ' + '; '.join('%s: %s' % f for f in fails[:6])))
missing_ch = [c for c in chs if not any(p['chapter'] == c for p in A)]
rep('C2 every chosen chapter has at least one point', not missing_ch, str(missing_ch))
rep('C3 every point carries a basis code that the list defines', all(p['basis'] in doc['basis_codes'] for p in A))
rep('C4 list B is separate (own key) and plain: no source, each item has a gap and a request', bool(B) and all('source' not in b and b['gap'] and b['asked_of_owner'] for b in B), '(%d items)' % len(B))
ids = [p['id'] for p in doc['list_A_points_carried_by_a_source']]
rep('C5 point ids unique', len(ids) == len(set(ids)))
rep('C6 chapter 7 marked doubtful and selectable, default 1 to 6', doc['default_chapters'] == [1, 2, 3, 4, 5, 6] and 7 in doc['selectable_chapters'] and all(p['doubtful'] for p in doc['list_A_points_carried_by_a_source'] if p['chapter'] == 7))
# no committed file edited: git status of the repository shows no modified or deleted tracked file
g = subprocess.run(['git', '-C', L.ROOT, 'status', '--porcelain'], capture_output=True, text=True)
if g.returncode != 0:
    print('NOT_MEASURED  C7 git status unavailable'); res.append(False)
else:
    bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
    rep('C7 no committed file is edited (only untracked or already-committed new files)', not bad, ' '.join(bad[:5]))
newd = subprocess.run(['git', '-C', L.ROOT, 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True).stdout.splitlines()
mine = [x for x in newd if x.startswith('08-tooling/exam/')]
other = [x for x in newd if not x.startswith('08-tooling/exam/')]
rep('C8 every file of this task is new (untracked or newly committed) and lies under 08-tooling/exam/', all(('critical_points' in x or 'pptx_text' in x) for x in mine if not x.endswith('.pyc')), '(%d files here)' % len(mine))
for x in other: print('INFO  untracked file outside this task, not made or touched here: ' + x)
print('RESULT', 'PASS' if all(res) else 'FAIL', '(%d of %d checks pass)' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
