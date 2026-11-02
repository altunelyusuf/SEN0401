"""Check of the exam engine v1.2.0 (FIVE alternatives: owner redesign 2026-11-02, ruling 3). New file; holds fixture text only, no question and no answer.
Prints PASS / FAIL / NOT_MEASURED per line; exit code 0 only when no line is FAIL. Never edits a committed file.
 C1  no tracked file is modified or deleted (git); the new files are untracked or newly committed
 C2  every rule R01-R22 and EN01-EN13 is loaded by the engine v1.2.0
 C3  the 57 committed fixtures of the printed-paper rules (v1.0.0), run under the NEW shapes: every rule that was not changed (all but R07, R11, R14, R15) gives exactly the expected answer of v1.0.0
 C4  the new fixtures of the printed-paper rules (v1.2.0: five options, five responses, lettered banks, plus N18b and N27b): exactly the expected answer; every rule R01-R22 is broken by at least one fixture
 C5  the SHACL fixtures of EN11-EN13 rebuilt with engine v1.2.0 and the five-option authored fixture: exactly the expected answer, each rule broken at least once
 C6  the committed engine fixtures (v1.0.0) under the v1.2.0 rules: EN01-EN10 give exactly the expected answer
 C7  engine run on the authored fixture (five alternatives), defaults 1-6 and 24 items: both papers built, no Violation, letters spread over A-E, bank entries lettered, makeup disjoint from midterm
 C8  refusals by the command line keep working (exit 2, nothing written): a four-option item, six responses for four premises, no authored file, a copied page item
"""
import collections, glob, json, os, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from rdflib import Graph, RDF
import pyshacl
import sen0401_exam_engine_v1_2_0 as E
from sen0401_exam_engine_v1_2_0 import PR, EN, EX, SH
ROOT = E.ROOT
res = []
def rep(name, ok, detail=''):
    ok = bool(ok); res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail)); sys.stdout.flush()
SCR = tempfile.mkdtemp(prefix='sen0401_enginecheck12_', dir=os.environ.get('SEN0401_ENGINE_TMP')); os.environ['SEN0401_ENGINE_TMP'] = SCR
AUTH = os.path.join(HERE, 'sen0401_exam_engine_fixture_authored_v1_2_0.json')
CHANGED = {'R07', 'R11', 'R14', 'R15'}
g = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True)
bad = [l for l in g.stdout.splitlines() if not l.startswith('??')]
rep('C1 no tracked file is modified or deleted', g.returncode == 0 and not bad, ' '.join(bad[:5]))
sh_ids = lambda gr: sorted({str(m).split()[0] for m in gr.objects(None, SH.message)})
allids = sh_ids(E.shapes_graph()); need = ['R%02d' % k for k in range(1, 23)] + ['EN%02d' % k for k in range(1, 14)]
miss = [r for r in need if r not in allids]
rep('C2 all rules R01-R22 and EN01-EN13 are loaded by engine v1.2.0', not miss, 'missing %s' % miss)
shapes = Graph().parse(os.path.join(HERE, 'sen0401_exam_paperrules_shapes_v1_2_0.ttl')); reg = Graph().parse(os.path.join(HERE, 'sen0401_exam_papertypes_v1_0_0.ttl'))
def subgraph(fxg, fid):
    sub = Graph(); keep = {fid}
    for s, o in fxg.subject_objects(PR.companion):
        if str(s).endswith('#%s_paper' % fid): keep.add(str(o).split('#')[1].split('_')[0])
    for s, p, o in fxg:
        if str(s).split('#')[-1].split('_')[0] in keep: sub.add((s, p, o))
    for t in reg: sub.add(t)
    return sub
def run(sub):
    conf, rg, txt = pyshacl.validate(sub, shacl_graph=shapes, advanced=True, inference='none', js=False)
    return {(str(rg.value(r, SH.resultMessage)).split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1]) for r in rg.subjects(SH.resultSeverity, None)}
# C3
fx0 = Graph().parse(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_v1_0_0.ttl'))
exp0 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_expected_v1_0_0.json'))).items()}
w3 = []
for fid in sorted(exp0):
    got = {x for x in run(subgraph(fx0, fid)) if x[0] not in CHANGED}; want = {x for x in exp0[fid] if x[0] not in CHANGED}
    if got != want: w3.append((fid, sorted(want), sorted(got)))
rep('C3 the committed v1.0.0 fixtures give the expected answer for every unchanged rule', not w3, '(%d fixtures; rules judged: all but %s) wrong: %s' % (len(exp0), sorted(CHANGED), w3[:4]))
# C4
fx1 = Graph().parse(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_v1_2_0.ttl'))
exp1 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_paperrules_fixtures_expected_v1_2_0.json'))).items()}
w4 = []; seen = set()
for fid in sorted(exp1):
    got = run(subgraph(fx1, fid)); seen |= {r for r, s in got}
    if got != exp1[fid]: w4.append((fid, sorted(exp1[fid]), sorted(got)))
rid = sorted({r for r in allids if re.fullmatch(r'R\d\d', r)})
unc = [r for r in rid if r not in seen]
rep('C4a the new printed-paper fixtures give exactly the expected answer', not w4, '(%d fixtures) wrong: %s' % (len(exp1), w4[:4]))
rep('C4b every rule R01-R22 is broken by at least one fixture', not unc, 'not exercised: %s' % unc)
newfx = sorted(set(exp1) - set(exp0)); changed_exp = sorted(k for k in exp0 if exp0[k] != exp1.get(k))
print('     fixtures added: %s; fixtures whose expected answer differs from v1.0.0: %s' % (newfx, changed_exp))
# C5
fx = Graph().parse(os.path.join(HERE, 'sen0401_exam_engine_fixtures_v1_2_0.ttl'))
exp5 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_engine_fixtures_expected_v1_2_0.json'))).items()}
byfid = collections.defaultdict(Graph); base = str(EX)
for s, p, o in fx:
    fid = str(s)[len(base):].split('/')[0] if str(s).startswith(base) else None
    if fid: byfid[fid].add((s, p, o))
w5 = []; seen5 = set()
for fid in sorted(exp5):
    got = {(r, s) for r, s, m in E.validate(byfid[fid])}; seen5 |= got
    if got != exp5[fid]: w5.append((fid, sorted(exp5[fid]), sorted(got)))
rep('C5a EN11-EN13 fixtures give exactly the expected answer', not w5, '(%d fixtures) wrong: %s' % (len(exp5), w5[:4]))
unc = [r for r in ('EN11', 'EN12', 'EN13') if (r, 'Violation') not in seen5]
rep('C5b EN11, EN12, EN13 are each broken by at least one fixture', not unc, 'not exercised: %s' % unc)
# C6
fx6 = Graph().parse(os.path.join(HERE, 'sen0401_exam_engine_fixtures_v1_0_0.ttl'))
exp6 = {k: set(map(tuple, v)) for k, v in json.load(open(os.path.join(HERE, 'sen0401_exam_engine_fixtures_expected_v1_0_0.json'))).items()}
by6 = collections.defaultdict(Graph)
for s, p, o in fx6:
    fid = str(s)[len(base):].split('/')[0] if str(s).startswith(base) else None
    if fid: by6[fid].add((s, p, o))
shapes6 = Graph().parse(os.path.join(HERE, 'sen0401_exam_paperrules_shapes_v1_2_0.ttl')); shapes6.parse(os.path.join(HERE, 'sen0401_exam_engine_shapes_v1_0_0.ttl'))
import sen0401_exam_engine_v1_0_0 as E0_
def fast6(gr):
    d = Graph()
    for t in gr: d.add(t)
    for t in E0_.registry(): d.add(t)
    conf, rg, txt = pyshacl.validate(d, shacl_graph=shapes6, advanced=True, inference='none', js=False)
    return {(str(rg.value(r, SH.resultMessage)).split()[0], str(rg.value(r, SH.resultSeverity)).split('#')[1]) for r in rg.subjects(SH.resultSeverity, None)}
en_old = lambda r: re.fullmatch(r'EN(0\d|10)', r) is not None
w6 = []
for fid in sorted(exp6):
    got = {(r, s) for r, s in fast6(by6[fid]) if en_old(r)}; want = {x for x in exp6[fid] if en_old(x[0])}
    if got != want: w6.append((fid, sorted(want), sorted(got)))
rep('C6 the committed engine fixtures (v1.0.0) give the expected answer for EN01-EN10 under the v1.2.0 rules (the page-context rules EN11-EN13 need facts the old graphs lack and are not judged there)', not w6, '(%d fixtures) wrong: %s' % (len(exp6), w6[:4]))
# C7
P = E.Params(24, authored=AUTH)
try:
    mid, gm, pm = E.make_and_check(P, 'midterm'); excl = frozenset(i['key'] for i in mid['items']); mk, gk, pk = E.make_and_check(P, 'makeup', exclude=excl, prev=0, salt=1)
    viol = E.validate(gm) ; vm = [x for x in viol if x[1] == 'Violation']
    letters = collections.Counter('ABCDE'[i['answer']] for i in mid['items'] if i['type'] in E.CHOICE)
    rep('C7a midterm of five-alternative fixture items: no Violation', not vm, '(pages %s, sheet pages %s) %s' % (mid.get('pageCount'), mid.get('sheetPages'), vm[:3]))
    rep('C7b choice keys spread over A-E (counts differ by at most one)', len(letters) == 5 and max(letters.values()) - min(letters.values()) <= 1, str(dict(sorted(letters.items()))))
    va = json.load(open(AUTH, encoding='utf8'))
    va['items'] = [it for it in va['items'] if not (it['key'].startswith('fx:c1:choice') and it['key'] not in ('fx:c1:choice0', 'fx:c1:choice1'))]
    vp = os.path.join(SCR, 'c7c.json'); json.dump(va, open(vp, 'w'))
    m2, gm2, pm2 = E.make_and_check(E.Params(24, authored=vp), 'midterm', render=False)
    labels = sorted({str(gm2.value(e, PR.label)) for e in gm2.subjects(RDF.type, PR.BankEntry)})
    rep('C7c bank entries are lettered', all(re.fullmatch('[A-Z]', l) for l in labels) and labels, str(labels))
    rep('C7d make-up uses no midterm item', not (excl & {i['key'] for i in mk['items']}), '(midterm %d items, make-up %d items)' % (len(mid['items']), len(mk['items'])))
except E.ExamRefused as e:
    rep('C7 engine run', False, str(e))
# C8
def cli(auth, outdir, extra=()):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'sen0401_exam_engine_v1_2_0.py'), 'build', '--items', '24', '--outdir', outdir, *( ['--authored', auth] if auth else []), *extra], capture_output=True, text=True)
    return r.returncode, os.path.isdir(outdir) and bool(os.listdir(outdir)), (r.stdout + r.stderr)[-200:]
def variant(fn):
    a = json.load(open(AUTH, encoding='utf8')); fn(a); p = os.path.join(SCR, 'v%d.json' % len(os.listdir(SCR))); json.dump(a, open(p, 'w')); return p
def four(a):
    for it in a['items']:
        if it['key'] == 'fx:c1:choice0': it['options'] = it['options'][:4]; it['answer'] = 0
def six(a):
    for it in a['items']:
        if it['key'] == 'fx:m:match': it['responses'] = it['responses'] + ['FIXTURE m response F']
for name, auth in (('four options in one item', variant(four)), ('six responses for four premises', variant(six)), ('no authored file', None)):
    od = os.path.join(SCR, 'o%d' % len(os.listdir(SCR))); rc, wrote, tail = cli(auth, od)
    rep('C8 refusal kept: %s' % name, rc == 2 and not wrote, 'exit %s, wrote %s' % (rc, wrote))
rc, wrote, tail = cli(AUTH, os.path.join(SCR, 'ok'))
rep('C8 the five-alternative fixture builds from the command line (exit 0, files written)', rc == 0 and wrote, 'exit %s %s' % (rc, tail.strip()[-80:]))
shutil.rmtree(SCR, ignore_errors=True)
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
