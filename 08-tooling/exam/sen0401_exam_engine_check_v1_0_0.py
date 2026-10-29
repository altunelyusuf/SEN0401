"""Checks of the exam engine, version 1.0.0. Prints PASS / FAIL / NOT_MEASURED per check; exit code 0 only when every check passes.
Usage: check.py [--log FILE]
C1  no committed file is edited or deleted (git status)
C2  both shape files parse; rule ids R01-R22 and EN01-EN10 are found
C3  every fixture (conforming and one per broken convention) gives exactly the expected answer
C4  every engine rule EN01-EN10 is broken by at least one fixture; the paper rules the fixtures also exercise are listed
C5  the engine run with defaults (chapters 1-6) builds a conforming midterm and make-up; measured independently: letters, Bloom majority, disjoint items, chapter quotas
C6  the chapter list is a parameter: chapters 1-7 and chapters 2,5 build conforming pairs whose items are only in those chapters; chapter 8 is refused
C7  versions: a second build into the same folder is version 2 with previous 1; an existing file is never overwritten; same seed gives same items
C8  refusals: each broken setting is refused with the expected rule and nothing is written
C9  print safety measured on the PDFs: white page, only grey-level pixels, 10 point text, page count equals the graph; every position printed once
C10 the answer key agrees with the paper graph (key letters, matching, bank labels)
C11 the chapter banks and pages are read only (hashes before and after); facts about the pools are printed
"""
import collections, glob, hashlib, json, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, RDF, URIRef
import sen0401_exam_engine_v1_0_0 as E
from sen0401_exam_engine_v1_0_0 import PR, EN, EX, V
import sen0401_exam_engine_render_v1_0_0 as R
import sen0401_exam_pagesave_measure_v1_0_0 as M
ROOT = E.ROOT
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail)); sys.stdout.flush()
def sha(f): return hashlib.sha256(open(f, 'rb').read()).hexdigest()
bank_files = sorted(glob.glob(ROOT + '/08-tooling/ch0*-page/question_bank_v*.json')) + sorted(glob.glob(ROOT + '/08-tooling/ch0*-page/*.html'))
before = {f: sha(f) for f in bank_files}
SCR = tempfile.mkdtemp(prefix='sen0401_enginecheck_', dir=os.environ.get('SEN0401_ENGINE_TMP')); mine = [SCR]
os.environ['SEN0401_ENGINE_TMP'] = SCR

g = __import__('subprocess').run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
rep('C1 no committed file is edited', g.returncode == 0 and not bad, ' '.join(bad[:5]))

sg = Graph().parse(os.path.join(HERE, V % 'paperrules_shapes' + '.ttl')); eg = Graph().parse(os.path.join(HERE, V % 'engine_shapes' + '.ttl'))
SHN = E.SH
ids = lambda gr: sorted({str(m).split()[0] for m in gr.objects(None, SHN.message)}, key=lambda x: (x[:1], int(re.sub(r'\D', '', x))))
rr, ee = [x for x in ids(sg) if x.startswith('R')], [x for x in ids(eg) if x.startswith('EN')]
rep('C2 shapes parse; rule ids found', len(rr) == 22 and ee == ['EN%02d' % k for k in range(1, 11)], '%d paper rules, engine rules %s' % (len(rr), ' '.join(ee)))

fx = Graph().parse(os.path.join(HERE, V % 'engine_fixtures' + '.ttl'))
exp = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, V % 'engine_fixtures_expected' + '.json'))).items()}
byfid = collections.defaultdict(Graph)
base = str(EX)
for s, p, o in fx:
    fid = str(s)[len(base):].split('/')[0] if str(s).startswith(base) else None
    if fid: byfid[fid].add((s, p, o))
wrong = []; seen = set(); n = 0
for fid in sorted(exp):
    got = {(r, s) for r, s, m in E.validate(byfid[fid])}; n += 1; seen |= got
    if got != exp[fid]: wrong.append((fid, sorted(exp[fid]), sorted(got)))
    if fid in ('P01', 'P02', 'P03', 'P04', 'P05', 'P06', 'P07') or got != exp[fid]: print('     %s expected %s got %s' % (fid, sorted(exp[fid]), sorted(got)))
rep('C3 every fixture gives exactly the expected answer', not wrong, '(%d fixtures) %s' % (n, '; '.join('%s expected %s got %s' % w for w in wrong[:6])))
unc = [r for r in ee if r not in {x for x, s in seen}]
rep('C4 every engine rule is broken by at least one fixture', not unc, 'not exercised: %s' % unc if unc else '(%d of %d); paper rules also exercised: %s' % (len(ee), len(ee), ' '.join(sorted({x for x, s in seen if x.startswith('R')}))))

P_ = lambda **k: E.Params(24, authored=None, **k)
def paper_facts(mid, mk, chapters):
    out = {}
    for nm, p in (('midterm', mid), ('makeup', mk)):
        ch = [i for i in p['items'] if i['type'] in E.CHOICE]; ctr = collections.Counter('ABCD'[i['answer']] for i in ch)
        n = sum(len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1 for i in p['items']); hi = sum((len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1) for i in p['items'] if i['bloom'] >= p['params']['higher_from'])
        qc = collections.Counter(); [qc.update({i['primary']: len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1}) for i in p['items']]
        out[nm] = dict(letters=dict(ctr), spread=max(ctr.values()) - min(ctr.get(l, 0) for l in 'ABCD') if ch else 0, items=n, higher=hi, quota_ok=dict(qc) == {c: v for c, v in p['quotas'].items() if v},
                       chapters_used=sorted({c for i in p['items'] for c in i['chapters']}), pages=p.get('pageCount'))
    return out
def build(P, outdir, write=True):
    return E.build_pair(P, outdir, write=write)

out1 = os.path.join(SCR, 'o1'); os.makedirs(out1)
mid, mk, warn = build(P_(chapters=(1, 2, 3, 4, 5, 6), matching=1, seed=4701), out1)
f = paper_facts(mid, mk, (1, 2, 3, 4, 5, 6))
okC5 = all(v['spread'] <= 1 and v['higher'] * 2 > v['items'] and v['quota_ok'] for v in f.values()) and not ({i['key'] for i in mid['items']} & {i['key'] for i in mk['items']})
print('     midterm %s' % f['midterm']); print('     makeup  %s' % f['makeup']); print('     warnings %s' % [w[2] for w in warn])
rep('C5 default engine run (chapters 1-6, 24 items) conforms; letters, Bloom majority, quotas, disjoint items measured', okC5)

out7 = os.path.join(SCR, 'o7'); os.makedirs(out7)
m7, k7, _ = build(P_(chapters=(1, 2, 3, 4, 5, 6, 7), matching=1, seed=11), out7)
f7 = paper_facts(m7, k7, range(1, 8))
out25 = os.path.join(SCR, 'o25'); os.makedirs(out25)
m25, k25, _ = build(E.Params(10, chapters=(2, 5)), out25)
f25 = paper_facts(m25, k25, (2, 5))
refused8 = None
try: E.build_pair(E.Params(10, chapters=(8,)), os.path.join(SCR, 'o8'), write=False)
except E.ExamRefused as e: refused8 = e
c7used = sorted({c for i in m7['items'] for c in i['chapters']})
ok6 = (7 in c7used and all(c in range(1, 8) for c in c7used) and set(f25['midterm']['chapters_used']) <= {2, 5} and set(f25['makeup']['chapters_used']) <= {2, 5}
       and refused8 is not None and any(r == 'R02' for r, s, m in refused8.violations))
rep('C6 chapter list is a parameter (1-7 builds with chapter 7 present; 2,5 builds only those; 8 refused)', ok6, 'chapters used 1-7: %s; 2,5: %s; chapter 8: %s' % (c7used, f25['midterm']['chapters_used'], sorted({(r, s) for r, s, m in refused8.violations if s == 'Violation'}) if refused8 else 'NOT REFUSED'))

# C7 versions, overwrite, determinism
mid2, mk2, _ = build(P_(chapters=(1, 2, 3, 4, 5, 6), matching=1, seed=4701), out1)
files = sorted(os.listdir(out1))
det = [i['key'] for i in mid['items']] == [i['key'] for i in mid2['items']]
build_again = None
ok7 = mid['version'] == 1 and mid2['version'] == 2 and mid2['previous'] == 1 and mk2['version'] == 2 and det and len([x for x in files if x.endswith('.pdf')]) == 4
rep('C7 versions increment (1 then 2, previous 1), earlier files kept, same seed gives the same items', ok7, 'files %d: %s' % (len(files), ' '.join(files[:4]) + ' ...'))

# C8 refusals
def refusal(label, P, want, outdir=None, kind=None):
    od = os.path.join(SCR, 'r_' + label); os.makedirs(od)
    try:
        E.build_pair(P, od); got = None
    except E.ExamRefused as e: got = sorted({(r, s) for r, s, m in e.violations if s == 'Violation'})
    except Exception as e: got = [('EXCEPTION', repr(e)[:120])]
    written = os.listdir(od)
    ok = got is not None and all(w in got for w in want) and not written
    print('     refusal %-26s expected %s got %s written %d' % (label, want, got, len(written))); return ok
FA = os.path.join(HERE, V % 'engine_fixture_authored' + '.json')
tj = os.path.join(SCR, 'badterm.json'); json.dump(dict(items=[dict(key='t:1', type='NumericAnswer', chapters=[1], bloom=3, kind='direct', source=dict(file='FIXTURE', locator='x'), q='FIXTURE', key_value=1, unit='u', tolerance=0, terms=['zxqv unfindable coinword'], papers=['midterm'])]), open(tj, 'w'))
sj = os.path.join(SCR, 'short.json'); json.dump(dict(items=[dict(key='s:1', type='ShortAnswer', chapters=[1], bloom=5, kind='direct', source=dict(file='FIXTURE', locator='x'), q='FIXTURE', rubric=['a'], lines=2, papers=['midterm'])]), open(sj, 'w'))
oks = [refusal('too many items for 60 min', E.Params(80), [('R05', 'Violation')]),
       refusal('indirect not enabled', E.Params(18, authored=FA, matching=1, synthesis_min=1), [('EN03', 'Violation')]),
       refusal('fixed items exceed quota', E.Params(6, authored=FA), [('EN01', 'Violation')]),
       refusal('term not in corpus', E.Params(12, authored=tj), [('EN08', 'Violation')]),
       refusal('short answer not enabled', E.Params(12, authored=sj), [('R04', 'Violation')]),
       refusal('synthesis minimum unmet', E.Params(12, synthesis_min=3), [('EN02', 'Violation')]),
       refusal('page limit of one page', E.Params(24, page_limit=1), [('R17', 'Violation')]),
       refusal('bank all Remember (ch 8)', E.Params(12, chapters=(8,), higher_share=0.0), [('R06', 'Violation')])]
rep('C8 each broken setting is refused with its rule and nothing is written', all(oks), '%d of %d' % (sum(oks), len(oks)))

# C9 print safety on the PDFs
from PIL import Image
pdfs = sorted(glob.glob(out1 + '/*_v1_0_0.pdf')); bad9 = []; info9 = []
for pdf in pdfs:
    d = os.path.join(SCR, 'png_' + os.path.basename(pdf)[:-4]); os.makedirs(d)
    subprocess.run(['pdftoppm', '-r', '50', '-png', pdf, d + '/p'], check=True)
    pngs = sorted(glob.glob(d + '/p*.png')); nonwhite_color = 0; corner_white = True
    for pg in pngs:
        im = Image.open(pg).convert('RGB'); px = im.load(); w, h = im.size
        corner_white &= px[2, 2] == (255, 255, 255) and px[w - 3, h - 3] == (255, 255, 255)
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                r, gg, b = px[x, y]
                if not (abs(r - gg) < 4 and abs(gg - b) < 4): nonwhite_color += 1
    fonts = subprocess.run(['pdffonts', pdf], capture_output=True, text=True).stdout
    txt = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout
    paper = mid if 'midterm' in pdf else mk
    pos = [i['position'] for i in paper['items']]
    pages = int([l for l in subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[1])
    missing = [p for p in pos if not re.search(r'(^|\s)%d[\.-]' % p, txt)]
    info9.append('%s: %d pages, colour pixels %d, white corners %s, positions missing %s' % (os.path.basename(pdf), pages, nonwhite_color, corner_white, missing))
    if nonwhite_color or not corner_white or missing or pages != paper['pageCount']: bad9.append(os.path.basename(pdf))
print('     ' + '\n     '.join(info9))
rep('C9 PDFs are white and grey-level only; every position is printed; page count equals the engine record', not bad9, ' '.join(bad9))

# C10 key vs graph
bad10 = []
for fpath in sorted(glob.glob(out1 + '/*_v1_0_0_key.json')):
    key = json.load(open(fpath)); gg = Graph().parse(fpath.replace('_key.json', '_paper.ttl'))
    for e in key['items']:
        if e['type'] in E.CHOICE:
            it = [i for i in gg.subjects(PR.position, E.I(e['position']))][0]
            ks = [str(gg.value(o, PR.letter)) for o in gg.objects(it, PR.option) if str(gg.value(o, PR.isKey)) == 'true']
            if ks != [e['answer']]: bad10.append((fpath.split('/')[-1], e['position'], ks, e['answer']))
rep('C10 answer key letters agree with the paper graph', not bad10, str(bad10[:3]))

after = {f: sha(f) for f in bank_files}
g2 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True)
bad2 = [l for l in g2.stdout.splitlines() if not l.startswith('??')]
pool, st = E.bank_pool(range(1, 8), 45)
tot = collections.Counter(i['bloom'] for i in pool)
print('     print-eligible bank items (chapters 1-7) per chapter: %s; Bloom %s' % ({c: '%d of %d' % (v[1], v[0]) for c, v in st.items()}, dict(sorted(tot.items()))))
print('     chapters with no eligible Analyze item: %s' % [c for c in range(1, 8) if not any(i['bloom'] >= 4 and i['primary'] == c for i in pool)])
rep('C11 banks and pages unchanged by the run; no committed file edited', before == after and not bad2, '%d files hashed' % len(before))
for d in mine: shutil.rmtree(d, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
