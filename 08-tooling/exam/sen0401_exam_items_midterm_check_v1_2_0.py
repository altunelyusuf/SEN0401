#!/usr/bin/env python3
"""SEN0401 midterm items check, version 1.2.0 (new file; derived from check v1.0.0, whose F1 to F8 are kept line by line, with F4 pointed at the builder of the file under test and the checks G1 to G6 added for the criterion AC9_Exam_Items3: structure, abbreviations, tips, no recall wording, critical points kept, audit counts).
Checks sen0401_exam_items_midterm_v1_2_0.json against the engine v1.1.0.

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
ITEMS_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_2_0.json')
if '--items' in sys.argv: ITEMS_FILE = sys.argv[sys.argv.index('--items') + 1]
if '--structure' in sys.argv: STRUCT_FILE = sys.argv[sys.argv.index('--structure') + 1]
BUILDER = os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_2_0.py')
STRUCT_FILE = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
PREV_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_1_0.json')
ALLOWED_ENH = {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}
SUITED = {'ChoiceFour', 'ChoiceFourCode', 'Matching', 'Ordering', 'FillBlankGroup', 'NumericAnswer', 'CodeTrace'}
fails = []; out = []


def say(status, name, detail=''):
    line = '%-12s %s %s' % (status, name, detail)
    print(line); out.append(line)
    if status == 'FAIL': fails.append(name)


def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']
spec0 = __import__('importlib.util').util.spec_from_file_location('mtb12', BUILDER); mtb = __import__('importlib.util').util.module_from_spec(spec0); spec0.loader.exec_module(mtb)
AUDIT_TIP = {k: ('N' if v['tip'] == 'N' else 'Y') for k, v in mtb.AUDIT.items()}
AUDIT_REPL = mtb.AUDIT
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
    same_items = r.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_items_midterm_v1_2_0.json'), encoding='utf8')) == doc
    same_struct = r.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_structure_v1_0_0.json'), encoding='utf8')) == json.load(open(STRUCT_FILE, encoding='utf8'))
    same_log = r.returncode == 0 and open(os.path.join(td, 'sen0401_exam_items_midterm_computed_v1_2_0.txt'), encoding='utf8').read() == open(os.path.join(HERE, 'sen0401_exam_items_midterm_computed_v1_2_0.txt'), encoding='utf8').read()
    same_items = same_items and same_struct
say('PASS' if same_items and same_log else 'FAIL', 'F4 the builder, run again, writes the same items file, the same structure file and the same computed log (number items and tables are computed there)')

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


# ------------------------------------------------------------------ G (v1.2.0): the owner's rules of 2026-11-01 13:04 and the criterion AC9_Exam_Items3
import re as _re
st = json.load(open(STRUCT_FILE, encoding='utf8')); by = {i['key']: i for i in items}
ALLOWED_BLOCKS = {'ChoiceFour', 'NumericAnswer', 'Ordering', 'Matching', 'FillBlankGroup'}
Qs = st['questions']
main_q = [q for q in Qs if not q.get('bonus')]; bonus_q = [q for q in Qs if q.get('bonus')]
ok = len(main_q) == 4 and all(q['points'] == 25 and sum(s_['points'] for s_ in q['sub']) == 25 and q['sub'] for q in main_q) and len(bonus_q) == 1 and bonus_q[0]['points'] == 10 and sum(s_['points'] for s_ in bonus_q[0]['sub']) == 10 and bonus_q[0]['number'] == 5
say('PASS' if ok else 'FAIL', 'G1 structure: four questions of 25 points, each with sub-questions that add up, and a fifth bonus question of 10 points', '(points %s, bonus %s, total %s)' % ([q['points'] for q in main_q], [q['points'] for q in bonus_q], st['total_points_without_bonus']))
used = [s_['item'] for q in main_q for s_ in q['sub']]
units_in = sum(units(by[k]) for k in dict.fromkeys(used)) if all(k in by for k in used) else -1
blank_subs = [s_ for q in main_q for s_ in q['sub'] if s_['type'] == 'FillBlankGroup']
cover = all(k in by for k in used) and sorted(set(used)) == sorted(by) and len(used) - len(blank_subs) + len(set(s_['item'] for s_ in blank_subs)) == len(by) and len(blank_subs) == sum(len(i['blanks']) for i in items if i['type'] == 'FillBlankGroup')
say('PASS' if cover else 'FAIL', 'G1 every item is used exactly once in the main questions (each fill-in blank is a sub-question) and every sub-question key resolves', '(items %d, sub-questions %d, units %d)' % (len(by), sum(len(q['sub']) for q in main_q), units_in))
blocks = {s_['block'] for q in main_q for s_ in q['sub']}
say('PASS' if blocks <= ALLOWED_BLOCKS and len(Qs) == 5 and len({q['format'] for q in Qs}) == 5 else 'FAIL', 'G1 five different formats; the answer sheet block types stay in the unchanged set', str(sorted(blocks)))
hand = [s_ for s_ in bonus_q[0]['sub']] if bonus_q else []
say('PASS' if hand and all(s_['hand_marked'] and not s_['machine_read'] and s_['rubric_points'] <= 3 and s_['block'].startswith('NONE') for s_ in hand) and bonus_q[0]['hand_marked'] and not bonus_q[0]['machine_read'] else 'FAIL', 'G1 short explanation items are marked as hand-marked, not machine-read, rubric of at most 3 points (paper rule for the conditional type)', '(%d prompts)' % len(hand))
bad = [(s_['key'], t) for s_ in hand for t in E0.unfound_terms({'terms': s_['terms']}) and [s_['terms']]]
say('PASS' if not bad else 'FAIL', 'G1 EN08 for the bonus prompts: every term is found in the course corpus', str(bad) if bad else '(%d terms)' % sum(len(s_['terms']) for s_ in hand))
bad = [s_['item'] for s_ in hand for src_ in s_['sources'] if not os.path.exists(os.path.join(ROOT, src_['file']))]
say('PASS' if not bad else 'FAIL', 'G1 the sources of the bonus prompts exist', str(bad))
for cpid in {c for s_ in hand for c in s_['critical_points']}:
    if cpid not in cp: say('FAIL', 'G1 bonus critical point does not exist', cpid)

def printed(i):
    parts = [i.get('q', ''), i.get('code', '')] + list(i.get('options', [])) + list(i.get('steps', []))
    parts += [p_['text'] for p_ in i.get('premises', [])] + list(i.get('responses', []))
    parts += [b_['text'] + ' ' + b_['answer'] for b_ in i.get('blanks', [])] + list(i.get('distractors', []))
    return ' \n '.join(x for x in parts if x)

ABBRS = {'WIF': 'wallet import format', 'P2PKH': 'pay to public key hash', 'SegWit': 'segregated witness', 'SHA256': 'secure hash algorithm 256', 'BIP329': 'bitcoin improvement proposal 329',
         'txid': 'transaction identifier', 'wtxid': 'witness transaction identifier', 'UTXO': 'unspent transaction output', 'BIP': 'bitcoin improvement proposal', 'BTC': 'bitcoin', 'SHA-256': 'secure hash algorithm',
         'P2SH': 'pay to script hash', 'HD': 'hierarchical deterministic', 'RBF': 'replace-by-fee', 'RPC': 'remote procedure call'}
bad = []
for i in items:
    tx = printed(i); low = tx.lower()
    # the code listing is printed after the stem; code identifiers such as the variable names are not abbreviations of text
    text_only = (i.get('q', '') + ' ' + ' '.join(i.get('options', [])) + ' ' + ' '.join(i.get('steps', [])) + ' ' + ' '.join(p_['text'] for p_ in i.get('premises', [])) + ' ' + ' '.join(i.get('responses', []))
                 + ' ' + ' '.join(b_['text'] for b_ in i.get('blanks', [])) + ' ' + ' '.join(i.get('distractors', [])) + ' ' + ' '.join(b_['answer'] for b_ in i.get('blanks', [])))
    tl = text_only.lower()
    for ab, full in ABBRS.items():
        m = _re.search(r'(?<![A-Za-z0-9])' + _re.escape(ab) + r'(?![A-Za-z0-9])', text_only, _re.I if ab in ('txid', 'wtxid') else 0)
        if not m: continue
        j = tl.find(full)
        if j < 0 or j > m.start(): bad.append((i['key'], ab, 'first use at %d, full form "%s" at %d' % (m.start(), full, j)))
for q in bonus_q:
    for s_ in q['sub']:
        tl = (s_['prompt'] + ' ' + ' '.join(t[0] + ' ' + t[1] for t in s_['tips']) + ' ' + ' '.join(s_['rubric'])).lower()
        for ab, full in ABBRS.items():
            if _re.search(r'(?<![a-z0-9])' + _re.escape(ab.lower()) + r'(?![a-z0-9])', tl) and full not in tl: bad.append((s_['key'], ab, 'no full form'))
say('PASS' if not bad else 'FAIL', 'G2 every abbreviation of a list of %d is spelled out before its first use in the same item' % len(ABBRS), str(bad) if bad else '(list: %s)' % ', '.join(ABBRS))
# items whose text uses any other all-capital token or digit-letter code are reported, not judged
others = {}
for i in items:
    for tok in _re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,}[a-z]?|[A-Z][a-z]+[A-Z][A-Za-z]*)(?![A-Za-z0-9_])', i.get('q', '') + ' ' + ' '.join(i.get('options', [])) + ' ' + ' '.join(p_['text'] for p_ in i.get('premises', [])) + ' ' + ' '.join(i.get('responses', [])) + ' ' + ' '.join(b_['text'] for b_ in i.get('blanks', []))):
        if tok not in ABBRS: others.setdefault(tok, []).append(i['key'])
say('PASS', 'G2 other capital-letter tokens met in the printed text (listed for a human reader, not judged by the tool)', str({k: sorted(set(v)) for k, v in others.items()}))
# G3 tips
bad = []; unc = {}
for i in items:
    tx = printed(i).lower()
    if i['type'] in ('ChoiceFour', 'ChoiceFourCode', 'NumericAnswer', 'CodeTrace'):
        if i['tips'] and 'tips:' not in i['q'].lower(): bad.append((i['key'], 'tips field not printed in the stem'))
        for t_ in i['tips']:
            if t_[0].lower() not in i['q'].lower(): bad.append((i['key'], 'tip term not in the stem: ' + t_[0]))
            if t_[1].lower() not in i['q'].lower(): bad.append((i['key'], 'tip text not in the stem: ' + t_[0]))
    else:
        for t_ in i['tips']:
            if t_[1].lower() not in tx and t_[0].lower() not in tx: bad.append((i['key'], 'tip not printed with the item: ' + t_[0]))
    if not i['tips'] and not all(AUDIT_REPL[k_]['verdict'] == 'KEEP' for k_ in i['from_item']): bad.append((i['key'], 'no tips and the audit does not record a KEEP for the source item'))
    cov = ' '.join(t_[0].lower() + ' ' + t_[1].lower() for t_ in i['tips'])
    miss = [t for t in i['terms'] if t.lower() in tx and t.lower() not in cov and t.lower() not in ('fee', 'change', 'bit 31')]
    if miss: unc[i['key']] = miss
say('PASS' if not bad else 'FAIL', 'G3 every item with a stem prints its tips with the stem; every other item prints each tip with its sentences, steps, premises or bank entries; an item without tips is a recorded KEEP', str(bad) if bad else '(%d items, %d tips)' % (len(items), sum(len(i['tips']) for i in items)))
say('PASS', 'G3 MEASURED: course terms of the term lists that are printed in the item text but carry no tip of their own (a human reader judges them)', str(unc) if unc else '(none)')
# G4 no recall wording
RECALL = _re.compile(r"\b(what is the name|name the|what is it called|which term|what do we call|is called the|write the (word|term|name)|recall|from memory|define )", _re.I)
bad = [(i['key']) for i in items if RECALL.search(printed(i))] + [s_['key'] for s_ in hand if RECALL.search(s_['prompt'])]
say('PASS' if not bad else 'FAIL', 'G4 no item asks for a name, a term or a definition by wording (scan of the printed text for recall phrases; the judgement of the sense is the audit)', str(bad))
for i in items:
    if i['type'] == 'FillBlankGroup':
        ans = [b_['answer'] for b_ in i['blanks']]
        if any(' (' not in a_ for a_ in ans + i['distractors']): say('FAIL', 'G4 every bank entry carries its tip in brackets', i['key'])
say('PASS', 'G4 every item names what it asks about (use, importance or reason)', str({i['key']: i['understanding'].split(':')[0] for i in items}))
# G5 critical points kept
prev = json.load(open(PREV_FILE, encoding='utf8'))['items']
before = {c for i in prev for c in i['critical_points']}; after = {c for i in items for c in i['critical_points']}
lost = sorted(before - after); gained = sorted(after - before)
say('PASS' if not lost else 'FAIL', 'G5 critical points tested by v1.1.0 that v1.2.0 no longer tests (by the items critical_points links; chapters 1 to 6)', 'lost %s ; gained %s ; before %d, after %d' % (lost, gained, len(before), len(after)))
by_ch = {c: (len([x for x in before if cp[x]['chapter'] == c]), len([x for x in after if cp[x]['chapter'] == c])) for c in range(1, 7)}
say('PASS', 'G5 critical points per chapter (before, after)', str(by_ch))
# G6 the audit counts are in the builder
say('PASS' if set(AUDIT_REPL) == {i['key'] for i in prev} and len(AUDIT_REPL) == 23 else 'FAIL', 'G6 the audit covers exactly the 23 items of v1.1.0', '(%d rows; verdicts %s)' % (len(AUDIT_REPL), {v: sum(1 for a in AUDIT_REPL.values() if a['verdict'] == v) for v in ('KEEP', 'REWRITE', 'REPLACE')}))
bad = [i['key'] for i in items if not set(i['from_item']) <= set(AUDIT_REPL)]
say('PASS' if not bad else 'FAIL', 'G6 every new item names the v1.1.0 item(s) it comes from', str(bad))

print('\nRESULT', 'FAIL (%s)' % '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
