"""Checks of the exam engine, version 1.1.0 (new file). Prints PASS / FAIL / NOT_MEASURED per check; exit code 0 only when every check passes. The checks never edit a committed file.
Usage: check.py            (the run log is made by the caller: python3 check.py | tee sen0401_exam_engine_check_log_v1_1_0.txt; a log file is never appended to)
STATED BEFORE THE RUN (the method and its thresholds are in sen0401_exam_similarity_v1_1_0.py (v1.0.0 kept; see its HISTORY); the expected answers are in sen0401_exam_nocopy_pairs_v1_0_0.json and in
sen0401_exam_engine_fixtures_build_v1_1_0.py, committed before the first run):
C1  no committed file is edited or deleted (git); the new files of this work are listed
C2  the method and thresholds are printed; the page-visible set is measured (counts agree with the seed report); the threshold reasons in the module are reproduced on the page set
C3  FIXTURE OF KNOWN ANSWER: every pair of the pairs file (copies, near copies, different items on the same concept, paraphrases, guards, other item types) gives exactly the expected answer
C4  the three sweeps over the whole page-visible set give the expected answer for every item
C5  SHACL fixtures: EN11, EN12, EN13 and the conforming fixtures give exactly the expected answer; every new rule is broken by at least one fixture
C6  the rules of v1.0.0 still hold: its 43 fixtures give the expected answer under the shapes the v1.1.0 engine loads (R01-R22, EN01-EN10)
C7  engine run with defaults (chapters 1-6, 24 items per paper): both papers conform; letters, Bloom majority, quotas, disjoint items, every item authored, sheet counted in the pages
C8  the chapter list is a parameter (1-7 builds with chapter 7; 2,5 only those; 8 refused)
C9  versions increment; an existing file is never overwritten; a missing output folder is created
C10 refusals by the command line (exit code 2, nothing written): copy, near copy, option-only copy, bank item, matching premise copy, no authored file, unresolved links, and the v1.0.0 refusals
C11 papers are built from authored items only: bank composition cannot run (patched to fail) and no item carries a bank origin
C12 print safety on the PDFs (paper and answer sheet); page count equals paper pages plus sheet pages
C13 the answer key agrees with the paper graph; the answer sheet holds one unit for every answer place
C14 the banks, quiz files and pages are unchanged by the run
"""
import collections, glob, hashlib, itertools, json, os, re, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, RDF
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S
import sen0401_exam_engine_render_v1_1_0 as R
from sen0401_exam_engine_v1_1_0 import PR, EN, EX
ROOT = E.ROOT
res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail)); sys.stdout.flush()
def sha(f): return hashlib.sha256(open(f, 'rb').read()).hexdigest()
watch = sorted(glob.glob(ROOT + '/08-tooling/ch0*-page/question_bank_v*.json')) + sorted(glob.glob(ROOT + '/08-tooling/ch0*-page/quiz_v*.json')) + sorted(glob.glob(ROOT + '/08-tooling/ch0*-page/*.html'))
before = {f: sha(f) for f in watch}
SCR = tempfile.mkdtemp(prefix='sen0401_enginecheck_', dir=os.environ.get('SEN0401_ENGINE_TMP')); os.environ['SEN0401_ENGINE_TMP'] = SCR
AUTH = os.path.join(HERE, 'sen0401_exam_engine_fixture_authored_v1_1_0.json')
ENGINE = os.path.join(HERE, 'sen0401_exam_engine_v1_1_0.py')
NEW = ['sen0401_exam_similarity_v1_0_0.py', 'sen0401_exam_similarity_v1_1_0.py', 'sen0401_exam_nocopy_pairs_build_v1_0_0.py', 'sen0401_exam_nocopy_pairs_v1_0_0.json', 'sen0401_exam_engine_shapes_v1_1_0.ttl',
       'sen0401_exam_engine_render_v1_1_0.py', 'sen0401_exam_engine_v1_1_0.py', 'sen0401_exam_engine_authored_fixture_build_v1_1_0.py', 'sen0401_exam_engine_fixture_authored_v1_1_0.json',
       'sen0401_exam_engine_fixtures_build_v1_1_0.py', 'sen0401_exam_engine_fixtures_v1_1_0.ttl', 'sen0401_exam_engine_fixtures_expected_v1_1_0.json', 'sen0401_exam_engine_check_v1_1_0.py']

# ---------------------------------------------------------------- C1
g = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
added = subprocess.run(['git', '-C', ROOT, 'log', '--diff-filter=M', '--format=%h', '--', *['08-tooling/exam/' + f for f in NEW]], capture_output=True, text=True).stdout.split()
firsts = {f: subprocess.run(['git', '-C', ROOT, 'log', '--diff-filter=A', '--format=%h', '--', '08-tooling/exam/' + f], capture_output=True, text=True).stdout.split() for f in NEW}
print('     first commit of each new file (empty = not yet committed): ' + '; '.join('%s %s' % (f.replace('sen0401_exam_', ''), (v[-1] if v else '-')) for f, v in firsts.items()))
rep('C1 no committed file is edited or deleted', g.returncode == 0 and not bad, ' '.join(bad[:5]))

# ---------------------------------------------------------------- C2
pages, pkey = E.pages_for((1, 2, 3, 4, 5, 6))
cnt = collections.Counter((p['chapter'], p['source']) for p in pages)
sr = json.load(open(os.path.join(HERE, 'sen0401_exam_seedreport_v1_0_0.json'), encoding='utf8'))['chapters']
sr_bank = {c: sr[str(c)]['items'] for c in range(1, 7)}; sr_quiz = {c: sr[str(c)]['quiz_items_in_the_page'] for c in range(1, 7)}
ok2a = all(cnt[(c, 'bank')] == sr_bank[c] and cnt[(c, 'quiz')] == sr_quiz[c] for c in range(1, 7)) and sum(v for (c, s), v in cnt.items() if s == 'bank') == 1188 and sum(v for (c, s), v in cnt.items() if s == 'quiz') == 40
print('     METHOD (version %s): %s' % (S.VERSION, json.dumps(S.thresholds())))
print('     page-visible set, chapters %s: bank %s, quiz %s, total %d' % (list(pkey), {c: cnt[(c, 'bank')] for c in range(1, 7)}, {c: cnt[(c, 'quiz')] for c in range(1, 7)}, len(pages)))
rep('C2a page-visible set agrees with the seed report (1188 bank items, 40 quiz items, per chapter)', ok2a)
# reproduce the threshold reasons stated in the module
import numpy as np
PP = [p['p'] for p in pages]; chap = [p['chapter'] for p in pages]
j2 = []; nt = 0; both = 0; opt_unguarded = 0; opt_guarded = 0; comb = 0; ge60 = 0
for a, b in itertools.combinations(range(len(pages)), 2):
    if chap[a] != chap[b]: continue
    x, y = PP[a], PP[b]; ss = S.jaccard(x['sh'], y['sh']); n = min(x['n_opts'], y['n_opts'])
    if ss >= 0.60: ge60 += 1
    if n and len(x['opts'] & y['opts']) / n >= 0.75: opt_unguarded += 1
    og = (len(x['dist'] & y['dist']) / max(n, S.OPTIONS_MIN_SET)) if n else 0
    if og >= 0.75: opt_guarded += 1
    if ss >= S.COMBINED_STEM_J2 and og >= S.COMBINED_OPTIONS_SHARE: comb += 1
cmap = {}
for i, p in enumerate(pages):
    if p['source'] == 'bank':
        cmap.setdefault(p['file'], json.load(open(os.path.join(ROOT, p['file']), encoding='utf8')))
conc = {i: cmap[p['file']][p['index']]['concept'] for i, p in enumerate(pages) if p['source'] == 'bank'}
byc = collections.defaultdict(list)
for i, c in conc.items(): byc[(pages[i]['chapter'], c)].append(i)
sc = [S.jaccard(PP[a]['sh'], PP[b]['sh']) for v in byc.values() for a, b in itertools.combinations(v, 2)]
print('     MEASURED on the page set: same-chapter pairs %d; pairs of different items of the same concept %d, their largest stem share %.3f, 99th percentile %.3f (threshold %.2f)' %
      (sum(1 for a, b in itertools.combinations(range(len(pages)), 2) if chap[a] == chap[b]), len(sc), max(sc), float(np.quantile(sc, .99)), S.STEM_NEAR_J2))
print('     MEASURED: same-chapter pairs with stem share >= 0.60: %d; option share >= 0.75 without the distinctive guard: %d, with it: %d; combined test fires on %d pairs' % (ge60, opt_unguarded, opt_guarded, comb))
rep('C2b the threshold reasons of the module are reproduced (stem threshold above every same-concept pair; 22 / 70 / 3 / 4 as stated)', max(sc) < S.STEM_NEAR_J2 and (ge60, opt_unguarded, opt_guarded, comb) == (22, 70, 3, 4),
    'got %s' % ((ge60, opt_unguarded, opt_guarded, comb),))

# ---------------------------------------------------------------- C3
def raw_of(pg):
    d = json.load(open(os.path.join(ROOT, pg['file']), encoding='utf8')); return d[pg['index']] if pg['source'] == 'bank' else d['items'][pg['index']]
pf = json.load(open(os.path.join(HERE, 'sen0401_exam_nocopy_pairs_v1_0_0.json'), encoding='utf8'))
def judge(pair):
    hits = E.check_copies(pair['candidate'], pages); refs = {h[1] for h in hits}
    got = 'REFUSE' if hits else 'PASS'; exp = pair['expected']
    ok = got == exp['answer']
    if ok and got == 'REFUSE':
        kinds = {k for h in hits if h[1] == pair['page_ref'] for k in h[2]}
        ok = pair['page_ref'] in refs and set(exp['kinds_include']) <= kinds
    return ok, got, hits
bycls = collections.defaultdict(lambda: [0, 0]); wrong = []
for pr_ in pf['pairs'] + pf['special']:
    ok, got, hits = judge(pr_); bycls[pr_['cls']][0] += 1; bycls[pr_['cls']][1] += ok
    if not ok: wrong.append((pr_['id'], pr_['expected']['answer'], got, [(h[1], h[2], h[3], h[4]) for h in hits][:3]))
for c, (n, k) in sorted(bycls.items()): print('     class %-28s %2d pairs, %2d as expected' % (c, n, k))
for w in wrong: print('     WRONG %s expected %s got %s %s' % w)
rep('C3 every pair of the fixture of known answer gives exactly the expected answer', not wrong, '(%d pairs: %d to refuse, %d to pass; method of the module %s, pairs file written for %s)' % (len(pf['pairs']) + len(pf['special']),
    sum(1 for p in pf['pairs'] + pf['special'] if p['expected']['answer'] == 'REFUSE'), sum(1 for p in pf['pairs'] + pf['special'] if p['expected']['answer'] == 'PASS'), S.VERSION, pf['method_version']))

# ---------------------------------------------------------------- C4
def mid_word(q):
    t = q.split(' '); m = len(t) // 2
    for d in range(len(t)):
        for j in (m + d, m - d):
            if 0 < j < len(t) - 1 and t[j].isalpha() and t[j].lower() != 'other': t[j] = 'other'; return ' '.join(t)
    return None
w1 = w2 = w3 = 0; n1 = n2 = n3 = 0; bad4 = []
for pg in pages:
    r = raw_of(pg); stem = r['q'] + ('\n' + r['code'] if r.get('code') else '')
    cand = dict(type='ChoiceFourCode' if r.get('code') else 'ChoiceFour', q=r['q'], code=r.get('code'), options=r['options'])
    hit = E.check_copies(cand, pages); n1 += 1
    if any(h[1] == pg['ref'] for h in hit): w1 += 1
    else: bad4.append(('W1', pg['ref']))
    cand2 = dict(type='ChoiceFour', q='FIXTURE unrelated stem for the sweep that shares nothing with any page question', options=r['options'][1:] + r['options'][:1]); hit2 = E.check_copies(cand2, pages); n2 += 1
    want2 = len(pg['p']['dist']) >= 3; got2 = any(h[1] == pg['ref'] for h in hit2) if want2 else not hit2
    if got2: w2 += 1
    else: bad4.append(('W2', pg['ref'], want2, [(h[1], h[2]) for h in hit2][:2]))
    if pg['source'] == 'bank' and not r.get('code') and len(S.words(r['q'])) >= 10 and mid_word(r['q']):
        cand3 = dict(type='ChoiceFour', q=mid_word(r['q']), options=['FIXTURE option one', 'FIXTURE option two', 'FIXTURE option three', 'FIXTURE option four']); hit3 = E.check_copies(cand3, pages); n3 += 1
        if any(h[1] == pg['ref'] and 'STEM_NEAR' in h[2] for h in hit3): w3 += 1
        else: bad4.append(('W3', pg['ref'], r['q'][:70]))
print('     W1 copy of every page item refused: %d of %d; W2 stem replaced, options kept: %d of %d as expected; W3 one word changed: %d of %d refused' % (w1, n1, w2, n2, w3, n3))
for b in bad4[:6]: print('     SWEEP MISS', b)
rep('C4 the three sweeps over the whole page-visible set give the expected answer for every item', not bad4, '(W1 %d, W2 %d, W3 %d items)' % (n1, n2, n3))

# ---------------------------------------------------------------- C5
fx = Graph().parse(os.path.join(HERE, 'sen0401_exam_engine_fixtures_v1_1_0.ttl'))
exp5 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_engine_fixtures_expected_v1_1_0.json'))).items()}
byfid = collections.defaultdict(Graph); base = str(EX)
for s, p, o in fx:
    fid = str(s)[len(base):].split('/')[0] if str(s).startswith(base) else None
    if fid: byfid[fid].add((s, p, o))
wrong5 = []; seen5 = set()
for fid in sorted(exp5):
    got = {(r, s) for r, s, m in E.validate(byfid[fid])}; seen5 |= got
    print('     %s expected %s got %s' % (fid, sorted(exp5[fid]), sorted(got)))
    if got != exp5[fid]: wrong5.append(fid)
rep('C5a SHACL fixtures give exactly the expected answer', not wrong5, '(%d fixtures) wrong: %s' % (len(exp5), wrong5))
unc = [r for r in ('EN11', 'EN12', 'EN13') if (r, 'Violation') not in seen5]
rep('C5b every new rule EN11, EN12, EN13 is broken by at least one fixture', not unc, 'not exercised: %s' % unc if unc else '(3 of 3)')

# ---------------------------------------------------------------- C6
sh_ids = lambda gr: sorted({str(m).split()[0] for m in gr.objects(None, E.SH.message)})
allids = sh_ids(E.shapes_graph())
need = ['R%02d' % k for k in range(1, 23)] + ['EN%02d' % k for k in range(1, 14)]
print('     rule ids loaded by the engine: ' + ' '.join(i for i in allids if i in need))
fx0 = Graph().parse(os.path.join(HERE, 'sen0401_exam_engine_fixtures_v1_0_0.ttl'))
exp0 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_engine_fixtures_expected_v1_0_0.json'))).items()}
by0 = collections.defaultdict(Graph)
for s, p, o in fx0:
    fid = str(s)[len(base):].split('/')[0] if str(s).startswith(base) else None
    if fid: by0[fid].add((s, p, o))
old_rule = lambda r: re.fullmatch(r'R\d\d|EN(0\d|10)', r) is not None
wrong6 = []; seen6 = set()
for fid in sorted(exp0):
    got = {(r, s) for r, s, m in E.validate(by0[fid]) if old_rule(r)}; seen6 |= got
    if got != exp0[fid]: wrong6.append((fid, sorted(exp0[fid]), sorted(got)))
miss = [r for r in need if r not in allids]
rep('C6 all rules R01-R22 and EN01-EN13 are loaded; the 43 fixtures of v1.0.0 give the expected answer for R01-R22 and EN01-EN10 (the new facts of EN11-EN13 are absent from those old graphs and are not judged there)', not wrong6 and not miss,
    '(%d fixtures) missing ids %s wrong %s' % (len(exp0), miss, wrong6[:3]))

# ---------------------------------------------------------------- engine runs
def paper_facts(p):
    ch = [i for i in p['items'] if i['type'] in E.CHOICE]; ctr = collections.Counter('ABCD'[i['answer']] for i in ch)
    n = sum(E.units(i) for i in p['items']); hi = sum(E.units(i) for i in p['items'] if i['bloom'] >= p['params']['higher_from'])
    qc = collections.Counter()
    for i in p['items']: qc[i['primary']] += E.units(i)
    return dict(letters=dict(ctr), spread=(max(ctr.values()) - min(ctr.get(l, 0) for l in 'ABCD')) if ch else 0, items=n, higher=hi, quota_ok=dict(qc) == {c: v for c, v in p['quotas'].items() if v},
                chapters_used=sorted({c for i in p['items'] for c in i['chapters']}), pages=p.get('pageCount'), content=p.get('contentPages'), sheet=p.get('sheetPages'),
                types=dict(collections.Counter(i['type'] for i in p['items'])))
out1 = os.path.join(SCR, 'o1')                                 # NOT created: the engine must create the folder
mid, mk, warn = E.build_pair(E.Params(24, authored=AUTH, seed=4701), out1)
fm, fk = paper_facts(mid), paper_facts(mk)
keys_m = {i['key'] for i in mid['items']}; keys_k = {i['key'] for i in mk['items']}
print('     midterm %s' % fm); print('     makeup  %s' % fk); print('     warnings %s' % [w[2] for w in warn])
ok7 = all(f['spread'] <= 1 and f['higher'] * 2 > f['items'] and f['quota_ok'] and f['items'] == 24 and f['chapters_used'] == [1, 2, 3, 4, 5, 6] and f['pages'] == f['content'] + f['sheet'] and f['sheet'] >= 1 for f in (fm, fk)) and not (keys_m & keys_k)
okorig = all(i['origin'] == 'Authored' and not str(i['key']).startswith('bank:') for p in (mid, mk) for i in p['items'])
rep('C7 default engine run (chapters 1-6, 24 items per paper): conforms; letters, Bloom majority, quotas, disjoint items measured; every item authored; the sheet page is counted', ok7 and okorig,
    '(all item types present: %s)' % sorted(set(fm['types']) | set(fk['types'])))

# ---------------------------------------------------------------- C8
out7 = os.path.join(SCR, 'o7'); m7, k7, _ = E.build_pair(E.Params(21, chapters=(1, 2, 3, 4, 5, 6, 7), authored=AUTH, seed=11), out7)
out25 = os.path.join(SCR, 'o25'); m25, k25, _ = E.build_pair(E.Params(10, chapters=(2, 5), authored=AUTH), out25)
refused8 = None
try: E.build_pair(E.Params(10, chapters=(8,), authored=AUTH), os.path.join(SCR, 'o8'), write=False)
except E.ExamRefused as e: refused8 = e
c7used = sorted({c for i in m7['items'] for c in i['chapters']}); c25 = sorted({c for p in (m25, k25) for i in p['items'] for c in i['chapters']})
ok8 = 7 in c7used and set(c7used) <= set(range(1, 8)) and set(c25) <= {2, 5} and refused8 is not None and any(r == 'R02' for r, s, m in refused8.violations) and not os.path.exists(os.path.join(SCR, 'o8'))
rep('C8 chapter list is a parameter (1-7 builds with chapter 7 present; 2,5 builds only those; 8 refused)', ok8, 'chapters used 1-7: %s; 2,5: %s; chapter 8: %s' % (c7used, c25, sorted({(r, s) for r, s, m in refused8.violations if s == 'Violation'}) if refused8 else 'NOT REFUSED'))

# ---------------------------------------------------------------- C9
files_before = sorted(os.listdir(out1))
mid2, mk2, _ = E.build_pair(E.Params(24, authored=AUTH, seed=4701), out1)
files = sorted(os.listdir(out1))
det = [i['key'] for i in mid['items']] == [i['key'] for i in mid2['items']]
ow = None
try:
    os.makedirs(os.path.join(SCR, 'ow')); E.build_pair(E.Params(24, authored=AUTH, seed=4701), os.path.join(SCR, 'ow'))
    for f in glob.glob(os.path.join(SCR, 'ow', '*_v2_0_0*')): pass
    ow = 'ok'
except Exception as e: ow = repr(e)
ok9 = mid['version'] == 1 and mid2['version'] == 2 and mid2['previous'] == 1 and mk2['version'] == 2 and det and len([x for x in files if x.endswith('_v1_0_0.pdf')]) == 2 and len([x for x in files if x.endswith('_v2_0_0.pdf')]) == 2 \
    and all(os.path.exists(os.path.join(out1, f)) for f in files_before)
rep('C9 versions increment (1 then 2, previous 1), earlier files kept, same seed gives same items, the missing output folder was created', ok9 and os.path.isdir(out1), 'files %d: %s' % (len(files), ' '.join(files[:5]) + ' ...'))

# ---------------------------------------------------------------- C10
def cli(label, authored, items=24, extra=(), want=('EN11',), expect_exit=2):
    od = os.path.join(SCR, 'r_' + label)
    cmd = [sys.executable, ENGINE, 'build', '--items', str(items), '--outdir', od] + (['--authored', authored] if authored else []) + list(extra)
    p = subprocess.run(cmd, capture_output=True, text=True)
    written = os.listdir(od) if os.path.isdir(od) else []
    msg = (p.stdout + p.stderr).strip().splitlines()[-1][:230] if (p.stdout + p.stderr).strip() else ''
    ok = p.returncode == expect_exit and all(w in p.stdout for w in want) and not written
    print('     refusal %-34s exit %s written %d  %s' % (label, p.returncode, len(written), msg)); return ok
def variant(label, edit):
    a = json.load(open(AUTH, encoding='utf8')); edit(a['items']); f = os.path.join(SCR, label + '.json'); json.dump(a, open(f, 'w', encoding='utf8')); return f
def item(items, key): return [i for i in items if i['key'] == key][0]
pg0 = [p for p in pages if p['source'] == 'bank' and len(p['p']['w']) >= 12 and not raw_of(p).get('code') and len(p['p']['dist']) == 4][0]; r0 = raw_of(pg0)
def copy_edit(items):
    for i in items:
        if i['key'].startswith('fx:c1:choice'): i['q'] = r0['q']; i['options'] = list(r0['options']); i['answer'] = r0['answer']
def near_edit(items):
    for i in items:
        if i['key'].startswith('fx:c1:choice'): i['q'] = mid_word(r0['q'])
def opt_edit(items):
    for i in items:
        if i['key'].startswith('fx:c1:choice'): i['options'] = list(r0['options'])
def bank_edit(items):
    for i in items:
        if i['key'].startswith('fx:c1:choice'): i['key'] = 'bank:' + i['key']
def prem_edit(items):
    for i in items:
        if i['key'] in ('fx:m:match', 'fx:k:match'): i['premises'][0]['text'] = r0['q']
def blank_edit(items):
    for i in items:
        if i['key'] in ('fx:m:fill', 'fx:k:fill'): i['blanks'][0]['text'] = r0['q']
def seed_edit(items):
    for i in items: i['seeds'] = ['ch01/question_bank_v9_9_9.json#0'] if i.get('seeds') else []
def cp_edit(items):
    for i in items: i['critical_points'] = []
def reuse_edit(items):
    for i in items: i['papers'] = ['midterm', 'makeup']
oks = []
oks.append(cli('copy of a page question (all 4)', variant('copy', copy_edit)))
oks.append(cli('near copy: one word changed', variant('near', near_edit)))
oks.append(cli('options only', variant('opt', opt_edit)))
oks.append(cli('bank item (key bank:)', variant('bank', bank_edit)))
oks.append(cli('matching premise is a page question', variant('prem', prem_edit)))
oks.append(cli('fill-in blank is a page question', variant('blank', blank_edit)))
oks.append(cli('no authored file', None))
oks.append(cli('seed link unresolved', variant('seed', seed_edit), want=('EN12',)))
oks.append(cli('no critical point named', variant('cp', cp_edit), want=('EN12',)))
oks.append(cli('too many items for 60 min', AUTH, items=80, want=('R05',)))
ok_in = lambda **kw: E.Params(**kw)
def inproc(label, P, want, outdir=None):
    od = os.path.join(SCR, 'q_' + label)
    try: E.build_pair(P, od); got = None
    except E.ExamRefused as e: got = sorted({(r, s) for r, s, m in e.violations if s == 'Violation'})
    except Exception as e: got = [('EXCEPTION', repr(e)[:100])]
    written = os.listdir(od) if os.path.isdir(od) else []
    ok = got is not None and all(w in got for w in want) and not written
    print('     refusal %-34s expected %s got %s written %d' % (label, want, got, len(written))); return ok
tj = variant('badterm', lambda items: item(items, 'fx:m:num').update(terms=['zxqv unfindable coinword']))
oks.append(inproc('indirect not enabled', E.Params(24, authored=variant('ind', lambda items: item(items, 'fx:m:num').update(kind='indirect', indirect_form='consequence')), synthesis_min=0), [('EN03', 'Violation')]))
oks.append(inproc('term not in corpus', E.Params(24, authored=tj), [('EN08', 'Violation')]))
oks.append(inproc('synthesis minimum unmet', E.Params(24, authored=AUTH, synthesis_min=9), [('EN02', 'Violation')]))
oks.append(inproc('page limit 2 (sheet counted: 3)', E.Params(24, authored=AUTH, page_limit=2), [('R17', 'Violation')]))
oks.append(inproc('page limit 1', E.Params(24, authored=AUTH, page_limit=1), [('R17', 'Violation')]))
# the make-up never reuses a midterm item: when the authored items cannot fill a disjoint make-up the pair is refused; the owner may allow repeats explicitly
def only12(items):
    keep_ = set(); per = collections.Counter()
    for i in list(items):
        if i['type'] in ('ChoiceFour', 'ChoiceFourCode') and i['chapters'][0] in range(1, 7):
            per[i['chapters'][0]] += 1
            if per[i['chapters'][0]] > 4: items.remove(i)
        elif i['type'] != 'ChoiceFour' and i['type'] != 'ChoiceFourCode': items.remove(i)
fewf = variant('fewitems', only12)
oks.append(inproc('make-up cannot avoid midterm items', E.Params(24, authored=fewf, higher_from=3, higher_share=0.5), [('EN01', 'Violation')]))
rep('C10 each broken setting is refused (exit code 2 on the command line) with its rule and nothing is written', all(oks), '%d of %d' % (sum(oks), len(oks)))
try:
    E.build_pair(E.Params(24, authored=fewf, allow_repeat=True), os.path.join(SCR, 'rep'), write=False); rp = 'builds'
except E.ExamRefused as e: rp = 'refused %s' % sorted({(r, s) for r, s, m in e.violations if s == 'Violation'})
print('     with --allow-repeat the same too-small pool: %s (the owner has not allowed repeats; the default refuses)' % rp)

# ---------------------------------------------------------------- C11
src = open(ENGINE, encoding='utf8').read() + open(os.path.join(HERE, 'sen0401_exam_engine_render_v1_1_0.py'), encoding='utf8').read()
calls = re.findall(r'(?<![\w.])(?:E0\.)?(bank_pool|compose_matching)\(', re.sub(r'#.*', '', re.sub(r'""".*?"""', '', src, flags=re.S)))
saved = (E0.bank_pool, E0.compose_matching)
def boom(*a, **k): raise RuntimeError('bank composition was called')
E0.bank_pool = boom; E0.compose_matching = boom
try:
    mm, kk, _ = E.build_pair(E.Params(12, chapters=(1, 2, 3), authored=AUTH), os.path.join(SCR, 'o11'), write=False); ran = True
except Exception as e: ran = repr(e)
E0.bank_pool, E0.compose_matching = saved
rep('C11 papers are built from authored items only: no call of bank_pool or compose_matching in the v1.1.0 code, a build with both patched to fail succeeds, no item has a bank origin', not calls and ran is True and okorig,
    'static calls found: %s; patched run: %s' % (calls, ran))

# ---------------------------------------------------------------- C12, C13
from PIL import Image
pdfs = sorted(glob.glob(out1 + '/*_v1_0_0.pdf')); bad12 = []; info = []
pinfo = lambda f: int([l for l in subprocess.run(['pdfinfo', f], capture_output=True, text=True).stdout.splitlines() if l.startswith('Pages:')][0].split()[1])
for pdf in pdfs:
    d = os.path.join(SCR, 'png_' + os.path.basename(pdf)[:-4]); os.makedirs(d)
    subprocess.run(['pdftoppm', '-r', '50', '-png', pdf, d + '/p'], check=True)
    colour = 0; corner = True
    for pgf in sorted(glob.glob(d + '/p*.png')):
        im = Image.open(pgf).convert('RGB'); px = im.load(); w, h = im.size
        corner &= px[2, 2] == (255, 255, 255) and px[w - 3, h - 3] == (255, 255, 255)
        for y in range(0, h, 2):
            for x in range(0, w, 2):
                r, gg, b = px[x, y]
                if not (abs(r - gg) < 4 and abs(gg - b) < 4): colour += 1
    paper = mid if 'midterm' in pdf else mk
    is_sheet = pdf.endswith('_sheet.pdf')
    n = pinfo(pdf); info.append('%s: %d pages, colour pixels %d, white corners %s' % (os.path.basename(pdf), n, colour, corner))
    if colour or not corner: bad12.append(os.path.basename(pdf))
for paper, nm in ((mid, 'midterm'), (mk, 'makeup')):
    c = pinfo(os.path.join(out1, 'sen0401_exam_%s_v1_0_0.pdf' % nm)); s = pinfo(os.path.join(out1, 'sen0401_exam_%s_v1_0_0_sheet.pdf' % nm))
    txt = subprocess.run(['pdftotext', '-layout', os.path.join(out1, 'sen0401_exam_%s_v1_0_0.pdf' % nm), '-'], capture_output=True, text=True).stdout
    missing = [i['position'] for i in paper['items'] if not re.search(r'(^|\s)%d[\.-]' % i['position'], txt)]
    gg = Graph().parse(os.path.join(out1, 'sen0401_exam_%s_v1_0_0_paper.ttl' % nm)); pc = int(gg.value(None, PR.pageCount))
    info.append('%s: paper %d + sheet %d pages = %d; graph pageCount %d; positions missing %s' % (nm, c, s, c + s, pc, missing))
    if c + s != pc or c + s != paper['pageCount'] or missing: bad12.append(nm + ' pages')
print('     ' + '\n     '.join(info))
rep('C12 PDFs (paper and answer sheet) are white and grey-level only; every position is printed; the page count in the graph equals paper pages plus sheet pages', not bad12, ' '.join(bad12))

bad13 = []
for nm, paper in (('midterm', mid), ('makeup', mk)):
    key = json.load(open(os.path.join(out1, 'sen0401_exam_%s_v1_0_0_key.json' % nm))); gg = Graph().parse(os.path.join(out1, 'sen0401_exam_%s_v1_0_0_paper.ttl' % nm)); lay = json.load(open(os.path.join(out1, 'sen0401_exam_%s_v1_0_0_sheet_layout.json' % nm)))
    places = 0
    for e in key['items']:
        it = [i for i in gg.subjects(PR.position, E.I(e['position']))][0]; t = e['type']
        if t in E.CHOICE:
            places += 1; ks = [str(gg.value(o, PR.letter)) for o in gg.objects(it, PR.option) if str(gg.value(o, PR.isKey)) == 'true']
            if ks != [e['answer']]: bad13.append((nm, e['position'], ks, e['answer']))
        elif t == 'Matching':
            prem = sorted(gg.objects(it, PR.hasPremise), key=lambda x: str(x)); places += len(e['answer'])
            letters = sorted(str(gg.value(gg.value(pm_, PR.matchesTo), PR.letter)) for pm_ in prem)
            if sorted(e['answer'].values()) != letters: bad13.append((nm, e['position'], 'matching', letters, e['answer']))
        elif t == 'Ordering':
            places += len(e['answer'])
            if sorted(e['answer'].values()) != list(range(1, len(e['answer']) + 1)): bad13.append((nm, e['position'], 'ordering', e['answer']))
        elif t == 'FillBlankGroup':
            places += len(e['answer'])
            for b, (no, code) in enumerate(sorted(e['answer'].items(), key=lambda kv: int(kv[0]))):
                fi = [i for i in gg.subjects(PR.position, E.I(int(no)))][0]; lab = str(gg.value(gg.value(fi, PR.answerEntry), PR.label))
                if lab != code or not R.A.damm_valid(code): bad13.append((nm, no, 'bank', lab, code))
        elif t in ('NumericAnswer', 'CodeTrace'): places += 1
    units = sum(len(b['units']) for b in lay['blocks'])
    print('     %s: answer places %d, sheet units %d, sheet pages %d' % (nm, places, units, lay['pages']))
    if places != units: bad13.append((nm, 'units', places, units))
rep('C13 the answer key agrees with the paper graph (letters, matching, ordering, bank codes with a valid check digit); the sheet holds one unit for every answer place', not bad13, str(bad13[:3]))

# ---------------------------------------------------------------- C14
after = {f: sha(f) for f in watch}
g2 = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True)
bad2 = [l for l in g2.stdout.splitlines() if not l.startswith('??')]
rep('C14 banks, quiz files and pages are unchanged by the run; no committed file edited', before == after and not bad2, '%d files hashed' % len(before))
print('DISCLOSURES')
print('  1. FIXTURE ITEMS ONLY: the engine runs in this check were made from synthetic authored items (text FIXTURE, file sen0401_exam_engine_fixture_authored_v1_1_0.json). No real exam item exists yet; the Items task has not run.')
print('     The copy method was tested on page-visible items (real) against candidates made by rule (copies, option reversals, one word changed, stem replaced) and on %d hand-written pairs, never on a real authored exam item.' % (len(pf['pairs']) + len(pf['special'])))
print('  2. WHAT EN11 CANNOT SEE: a paraphrase of a page question (8 paraphrase pairs pass by design); a stem under 10 words with a word changed; options that are only truth values, numbers or tokens of 3 characters or less;')
print('     questions the pages build in the browser (the exam desk, xExamBuild: not in any file); older versions of a bank; any page text that is not a question item (explanations, worked examples, slides); a copy translated or renamed (identifiers in code).')
print('     EN11 also cannot judge whether a hand-written item asks the same idea: seed and critical-point links (EN12) record the origin, a person decides the idea.')
for d in (SCR,): shutil.rmtree(d, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
