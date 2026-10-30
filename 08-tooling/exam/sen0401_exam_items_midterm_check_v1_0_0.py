#!/usr/bin/env python3
"""SEN0401 midterm items check, version 1.0.0 (new file). Checks sen0401_exam_items_midterm_v1_0_0.json against the criterion AC3E_Exam_Items (midterm only) and the engine v1.1.0.

Every line is printed as PASS, FAIL or NOT_MEASURED; the exit code is 0 only when no line is FAIL. Nothing is edited: the check reads the items file, the critical points, the page items
(through the similarity module of the engine) and the course corpus (through the engine v1.0.0 term index), and re-runs the programs of the trace items.

Checks
  F1  the items file is a new file and no tracked file of the repository is modified (git)
  F2  24 authored items for the MIDTERM only (units: a fill-in blank counts as one), 4 per chapter of 1 to 6, none a bank item or a page quiz item
  F3  every item names its seed items or says 'none: ...'; every seed key resolves to a page item of the same chapter list; every critical point id exists and lies in chapters 1 to 6;
      every item names its enhancement(s) (from the five of the owner's ruling), chapters, level, kind (direct or synthesis), type (suited), source (file exists, locator), terms
  F4  trace items: the listing is run again here and must print the key; number items: the builder is run again into a temporary folder and must write the same file
  F5  EN08: every term of every item is found in the course corpus
  F6  EN11: the similarity method of the engine finds no page-visible item that any component of any item copies
  F7  conventions: at least half plus one of the 24 at Apply or above, at least 6 at Analyze or above, code lines at most 45 characters and 12 lines, number and trace answers of at most
      5 characters, no option that refers to another option, options of one item distinct, the letter of the keys evenly spread in the built paper
  F8  the engine v1.1.0 builds the midterm from these items and the shapes EN01 to EN13 and R01 to R22 give no Violation
Usage: sen0401_exam_items_midterm_check_v1_0_0.py [--items FILE]
"""
import glob, json, os, re, subprocess, sys, tempfile, io, contextlib
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
ITEMS_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json')
if '--items' in sys.argv: ITEMS_FILE = sys.argv[sys.argv.index('--items') + 1]
BUILDER = os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_0_0.py')
ALLOWED_ENH = {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}
SUITED = {'ChoiceFour', 'ChoiceFourCode', 'Matching', 'Ordering', 'FillBlankGroup', 'NumericAnswer', 'CodeTrace'}
fails = []; out = []


def say(status, name, detail=''):
    line = '%-12s %s %s' % (status, name, detail)
    print(line); out.append(line)
    if status == 'FAIL': fails.append(name)


def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S

# ------------------------------------------------------------------ F1
rel = os.path.relpath(ITEMS_FILE, ROOT)
tracked = subprocess.run(['git', '-C', ROOT, 'ls-files', '--error-unmatch', rel], capture_output=True, text=True).returncode == 0
committed_new = subprocess.run(['git', '-C', ROOT, 'log', '--oneline', '--', rel], capture_output=True, text=True).stdout.strip().splitlines()
mods = [l for l in subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines() if l[:2].strip() in ('M', 'D', 'MM', 'AM', 'R', 'T') or l[:2] in (' M', ' D')]
say('PASS' if not mods else 'FAIL', 'F1 no tracked file is modified', '(modified or deleted tracked files: %s)' % (mods or 'none'))
say('PASS' if len(committed_new) <= 1 else 'FAIL', 'F1 the items file has at most one commit (a committed file is never edited)', '(commits touching it: %d)' % len(committed_new))

# ------------------------------------------------------------------ F2
n_units = sum(units(i) for i in items)
say('PASS' if n_units == 24 else 'FAIL', 'F2 24 items (units)', '(%d items, %d units)' % (len(items), n_units))
per = {c: sum(units(i) for i in items if i['chapters'][0] == c) for c in range(1, 7)}
say('PASS' if all(v == 4 for v in per.values()) else 'FAIL', 'F2 4 items per chapter by primary chapter', str(per))
say('PASS' if all(i['papers'] == ['midterm'] for i in items) else 'FAIL', 'F2 every item is for the midterm only')
bad = [i['key'] for i in items if str(i['key']).startswith('bank:') or 'question_bank' in i['source']['file'] or re.search(r'quiz_v\d', i['source']['file'])]
say('PASS' if not bad else 'FAIL', 'F2 no item is a bank item or a page quiz item (key and source file)', str(bad))
say('PASS' if len({i['key'] for i in items}) == len(items) else 'FAIL', 'F2 item keys are unique')
say('PASS' if all(i['type'] in SUITED for i in items) else 'FAIL', 'F2 every type is a suited type of the paper registry', str(sorted({i['type'] for i in items})))

# ------------------------------------------------------------------ F3
pages = S.page_items((1, 2, 3, 4, 5, 6)); page_refs = {p['ref']: p for p in pages}
cp = E.cp_index()
problems = []
for i in items:
    k = i['key']
    if not i.get('seeds') and not str(i.get('no_seed_reason', '')).startswith('none:'): problems.append((k, 'no seed and no "none:" reason'))
    for s_ in i.get('seeds', []):
        if s_ not in page_refs: problems.append((k, 'seed does not resolve: ' + s_))
        elif page_refs[s_]['chapter'] not in i['chapters']: problems.append((k, 'seed from a chapter the item does not name: ' + s_))
    if not i.get('critical_points'): problems.append((k, 'no critical point'))
    for c in i.get('critical_points', []):
        if c not in cp: problems.append((k, 'critical point does not exist: ' + c))
        elif cp[c]['chapter'] not in range(1, 7) or cp[c]['chapter'] not in i['chapters']: problems.append((k, 'critical point outside the item chapters: ' + c))
    enh = i.get('enhancements', [])
    if not enh or not set(enh) <= ALLOWED_ENH: problems.append((k, 'enhancement missing or not one of the five: %s' % enh))
    if i['kind'] not in ('direct', 'synthesis'): problems.append((k, 'kind must be direct or synthesis'))
    if i['kind'] == 'synthesis' and len(set(i['chapters'])) < 2: problems.append((k, 'synthesis item with one chapter'))
    if i['kind'] == 'direct' and len(set(i['chapters'])) > 1: problems.append((k, 'direct item with several chapters'))
    if not (1 <= i['bloom'] <= 6): problems.append((k, 'bloom'))
    f = i['source'].get('file'); loc = i['source'].get('locator')
    if not f or not os.path.exists(os.path.join(ROOT, f)) or not loc: problems.append((k, 'source file missing or no locator: %s' % f))
    for sx in i.get('sources', []):
        if not os.path.exists(os.path.join(ROOT, sx['file'])): problems.append((k, 'extra source file missing: ' + sx['file']))
    if not i.get('terms'): problems.append((k, 'no terms'))
say('PASS' if not problems else 'FAIL', 'F3 seed links, point links, enhancements, chapters, level, kind, type, source and terms are complete and resolve', str(problems) if problems else '(%d items)' % len(items))
with_seed = sum(1 for i in items if i.get('seeds'))
say('PASS', 'F3 share of items with a seed (measured, not a pass condition)', '(%d of %d items; %d without a seed, each with its reason)' % (with_seed, len(items), len(items) - with_seed))

# ------------------------------------------------------------------ F4
def run(code, ns=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<item>', 'exec'), dict(ns or {}))
    return buf.getvalue().strip()


sys.path.insert(0, HERE)
import importlib.util
spec = importlib.util.spec_from_file_location('mtbuild', BUILDER); mt = importlib.util.module_from_spec(spec); spec.loader.exec_module(mt)
bad = []
for i in items:
    if i['type'] == 'CodeTrace':
        got = run(i['code'], {'cs_encode': mt.cs_encode})
        if got != i['output']: bad.append((i['key'], got, i['output']))
    if i['type'] == 'ChoiceFourCode' and 'print(' in i['code'] and 'utxo' in i['code']:
        got = run(i['code'])
        if got != i['options'][i['answer']].split(' : ')[0]: bad.append((i['key'], got, i['options'][i['answer']]))
say('PASS' if not bad else 'FAIL', 'F4 trace items and the code choice item: the listing printed again gives the key', str(bad) if bad else '(%d trace items, outputs: %s)' % (sum(1 for i in items if i['type'] == 'CodeTrace'), [i['output'] for i in items if i['type'] == 'CodeTrace']))
with tempfile.TemporaryDirectory() as td:
    r = subprocess.run([sys.executable, '-I', BUILDER, '--outdir', td], capture_output=True, text=True)
    same_items = r.returncode == 0 and json.load(open(os.path.join(td, os.path.basename(ITEMS_FILE)), encoding='utf8')) == doc if os.path.basename(ITEMS_FILE).startswith('sen0401_exam_items_midterm_v1_0_0') else False
    same_log = r.returncode == 0 and open(os.path.join(td, 'sen0401_exam_items_midterm_computed_v1_0_0.txt'), encoding='utf8').read() == open(os.path.join(HERE, 'sen0401_exam_items_midterm_computed_v1_0_0.txt'), encoding='utf8').read()
say('PASS' if same_items and same_log else 'FAIL', 'F4 the builder, run again, writes the same items file and the same computed log (number items and tables are computed there)')

# ------------------------------------------------------------------ F5
unf = {i['key']: E0.unfound_terms(i) for i in items}
unf = {k: v for k, v in unf.items() if v}
say('PASS' if not unf else 'FAIL', 'F5 EN08 every term is found in the course corpus', str(unf) if unf else '(%d terms)' % sum(len(i['terms']) for i in items))

# ------------------------------------------------------------------ F6
hits = []
for i in items:
    for label, ref, kinds, ss, os_ in E.check_copies(i, pages): hits.append((i['key'], label, ref, kinds, ss, os_))
say('PASS' if not hits else 'FAIL', 'F6 EN11 no component of any item matches a page-visible item', '(checked against %d page items)' % len(pages) if not hits else str(hits))
# the largest shares, for the record (measured, not a condition)
best = []
for i in items:
    for label, stem, opts in S.components(i):
        c = S.prepare(stem, opts)
        for p in pages:
            kinds, ss, os_ = S.compare(c, p['p'])
            best.append((ss, os_, i['key'], label, p['ref']))
best.sort(reverse=True)
say('PASS', 'F6 largest stem share found against any page item (measured; refusal at %.2f)' % S.STEM_NEAR_J2, '(%.3f: %s %s against %s)' % (best[0][0], best[0][2], best[0][3], best[0][4]))
bo = sorted(best, key=lambda x: -x[1])[0]
say('PASS', 'F6 largest option share found against any page item (measured; refusal at %.2f)' % S.OPTIONS_NEAR_SHARE, '(%.3f: %s %s against %s)' % (bo[1], bo[2], bo[3], bo[4]))

# ------------------------------------------------------------------ F7
ge3 = sum(units(i) for i in items if i['bloom'] >= 3); ge4 = sum(units(i) for i in items if i['bloom'] >= 4)
say('PASS' if ge3 * 2 > n_units else 'FAIL', 'F7 a majority at Apply or above', '(%d of %d)' % (ge3, n_units))
say('PASS' if ge4 >= 6 else 'FAIL', 'F7 at least 6 at Analyze or above', '(%d of %d)' % (ge4, n_units))
tbl = {t: 0 for t in range(1, 7)}
for i in items: tbl[i['bloom']] += units(i)
say('PASS', 'F7 levels (units per Bloom level 1 to 6)', str(tbl))
cap = {'ChoiceFour': 4, 'ChoiceFourCode': 4, 'Matching': 3, 'Ordering': 3, 'FillBlankGroup': 2, 'NumericAnswer': 3, 'CodeTrace': 4}
bad = [i['key'] for i in items if i['bloom'] > cap[i['type']]]
say('PASS' if not bad else 'FAIL', 'F7 no level above what the type can honestly reach (registry)', str(bad))
bad = [(i['key'], max(len(l) for l in i['code'].split('\n')), len(i['code'].split('\n'))) for i in items if i.get('code') and (max(len(l) for l in i['code'].split('\n')) > 45 or len(i['code'].split('\n')) > 12)]
say('PASS' if not bad else 'FAIL', 'F7 code lines at most 45 characters, at most 12 lines', str(bad) if bad else '(widest line %d characters, longest listing %d lines)' % (max(len(l) for i in items if i.get('code') for l in i['code'].split('\n')), max(len(i['code'].split('\n')) for i in items if i.get('code'))))
bad = [(i['key'], len(str(i['key_value'] if i['type'] == 'NumericAnswer' else i['output']))) for i in items if i['type'] in ('NumericAnswer', 'CodeTrace') and len(str(i['key_value'] if i['type'] == 'NumericAnswer' else i['output'])) > 5]
say('PASS' if not bad else 'FAIL', 'F7 number and trace answers of at most 5 characters (the answer sheet gives five boxes)', str(bad))
ref = re.compile(r'\b(all|none|both) of the (above|options|choices)\b|\b(option|choice) [A-D]\b|\b[A-D] (and|or) [A-D]\b', re.I)
bad = [i['key'] for i in items if i['type'] in ('ChoiceFour', 'ChoiceFourCode') and (any(ref.search(o) for o in i['options']) or len(set(i['options'])) < 4 or len(i['options']) != 4)]
say('PASS' if not bad else 'FAIL', 'F7 four distinct options, none that refers to another option', str(bad))
bad = [i['key'] for i in items if i['type'] == 'FillBlankGroup' and len(i['blanks']) + len(i['distractors']) > 9]
say('PASS' if not bad else 'FAIL', 'F7 a fill-in bank has at most 9 entries (EN13)', str(bad))

# ------------------------------------------------------------------ F8
P = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=ITEMS_FILE)
os.environ.setdefault('SEN0401_ENGINE_TMP', tempfile.gettempdir())
try:
    paper, g, p = E.make_and_check(P, 'midterm')
    viol = E.validate(g, P.chapters)
    v = [x for x in viol if x[1] == 'Violation']; w = [x for x in viol if x[1] != 'Violation']
    say('PASS' if not v else 'FAIL', 'F8 engine v1.1.0: the midterm built from these items has no Violation (EN01-EN13, R01-R22)', str(v) if v else '(pages with the answer sheet: %s, content pages %s, sheet pages %s)' % (paper.get('pageCount'), paper.get('contentPages'), paper.get('sheetPages')))
    for x in w: say('PASS', 'F8 non-violation notice (' + x[1] + ')', x[2])
    letters = {}
    for it in paper['items']:
        if it['type'] in ('ChoiceFour', 'ChoiceFourCode'): letters['ABCD'[it['answer']]] = letters.get('ABCD'[it['answer']], 0) + 1
    say('PASS' if letters and max(letters.values()) - min(letters.values()) <= 1 and len(letters) == 4 else 'FAIL', 'F8 answer letters of the choice items are evenly spread in the built paper', str(dict(sorted(letters.items()))))
    say('PASS' if paper['pool_size'] == len(items) and len(paper['items']) == len(items) else 'FAIL', 'F8 the paper holds all authored items (none chosen from a bank)', '(pool %d, paper items %d, skipped %s)' % (paper['pool_size'], len(paper['items']), paper['skipped']))
except E.ExamRefused as e:
    say('FAIL', 'F8 engine v1.1.0 refused the midterm', str(e))

print('\nRESULT', 'FAIL (%s)' % '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
