#!/usr/bin/env python3
"""SEN0401 midterm items check, version 1.3.0 (new file; derived line by line from check v1.2.0, every check F1 to F8 and G1 to G6 kept as it was, with F4 pointed at the builder v1.3.0 and the checks H1 to H9 added for the criterion AC9_Exam_Items4: only the three owner cases changed, the structure unchanged, the arithmetic and the orders recomputed, simple numbers, a tip for every term, the topic map, the critical points tool).
Checks sen0401_exam_items_midterm_v1_3_0.json against the engine v1.1.0.

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
ITEMS_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')
if '--items' in sys.argv: ITEMS_FILE = sys.argv[sys.argv.index('--items') + 1]
if '--structure' in sys.argv: STRUCT_FILE = sys.argv[sys.argv.index('--structure') + 1]
BUILDER = os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_3_0.py')
BUILDER_PREV = os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_2_0.py')      # its AUDIT table of the 23 items of v1.1.0 and its cs_encode are reused unchanged
PREV12_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_2_0.json')
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
spec0 = __import__('importlib.util').util.spec_from_file_location('mtb12', BUILDER_PREV); mtb = __import__('importlib.util').util.module_from_spec(spec0); spec0.loader.exec_module(mtb)
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
spec = importlib.util.spec_from_file_location('mtbuild', BUILDER_PREV); mt = importlib.util.module_from_spec(spec); spec.loader.exec_module(mt)
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
    same_items = r.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_items_midterm_v1_3_0.json'), encoding='utf8')) == doc
    same_struct = r.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_items_midterm_topic_map_v1_3_0.json'), encoding='utf8')) == json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_topic_map_v1_3_0.json'), encoding='utf8'))
    same_log = r.returncode == 0 and open(os.path.join(td, 'sen0401_exam_items_midterm_computed_v1_3_0.txt'), encoding='utf8').read() == open(os.path.join(HERE, 'sen0401_exam_items_midterm_computed_v1_3_0.txt'), encoding='utf8').read()
    same_items = same_items and same_struct and open(os.path.join(td, 'sen0401_exam_items_midterm_new_points_map_v1_3_0.txt'), encoding='utf8').read() == open(os.path.join(HERE, 'sen0401_exam_items_midterm_new_points_map_v1_3_0.txt'), encoding='utf8').read()
say('PASS' if same_items and same_log else 'FAIL', 'F4 the builder v1.3.0, run again, writes the same items file, the same topic map and the same computed log (the arithmetic and the orders of the three cases are computed there)')

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
prev = json.load(open(PREV_FILE, encoding='utf8'))['items']      # v1.1.0, as in check v1.2.0
before = {c for i in prev for c in i['critical_points']}; after = {c for i in items for c in i['critical_points']}
lost = sorted(before - after); gained = sorted(after - before)
say('PASS' if not lost else 'FAIL', 'G5 critical points tested by v1.1.0 that this file no longer tests (by the items critical_points links; chapters 1 to 6)', 'lost %s ; gained %s ; before %d, after %d' % (lost, gained, len(before), len(after)))
by_ch = {c: (len([x for x in before if cp[x]['chapter'] == c]), len([x for x in after if cp[x]['chapter'] == c])) for c in range(1, 7)}
say('PASS', 'G5 critical points per chapter (before, after)', str(by_ch))
# G6 the audit counts are in the builder
say('PASS' if set(AUDIT_REPL) == {i['key'] for i in prev} and len(AUDIT_REPL) == 23 else 'FAIL', 'G6 the audit covers exactly the 23 items of v1.1.0', '(%d rows; verdicts %s)' % (len(AUDIT_REPL), {v: sum(1 for a in AUDIT_REPL.values() if a['verdict'] == v) for v in ('KEEP', 'REWRITE', 'REPLACE')}))
bad = [i['key'] for i in items if not set(i['from_item']) <= set(AUDIT_REPL)]
say('PASS' if not bad else 'FAIL', 'G6 every new item names the v1.1.0 item(s) it comes from', str(bad))
#H_MARK

# ------------------------------------------------------------------ H (v1.3.0): the criterion AC9_Exam_Items4 (the owner's three cases and the owner's topic list)
import glob as _glob, itertools as _it
prev12 = json.load(open(PREV12_FILE, encoding='utf8'))['items']; p12 = {i['key']: i for i in prev12}
CASES = {'C1': 'mt2:i06:order-wallet-to-block', 'C2': 'mt2:i07:fill-fee-rate-and-set', 'C3': 'mt2:i02:fee-not-written'}
KEPT = ['mt2:i05:shop-confirmations', 'mt2:i23:fill-txid-and-weight']
BREWORK = {'B': 'mt2:i03:toy-chain-supply'}                  # the owner's block-reward point of 21:23, a same-type slot reworked
ALLCH = dict(CASES, **BREWORK)
# H1 only the three cases changed, in the same places
same_keys = [i['key'] for i in items] == [i['key'] for i in prev12]
diff = [i['key'] for i in items if i != p12.get(i['key'])]
say('PASS' if same_keys and sorted(diff) == sorted(ALLCH.values()) else 'FAIL', 'H1 against items v1.2.0 the same 21 keys in the same order, and exactly the three case items and the reworked block-reward item differ', '(differ: %s)' % diff)
say('PASS' if all(by[k] == p12[k] for k in KEPT) else 'FAIL', 'H1 the two kept items are byte-equal to v1.2.0', str(KEPT))
bad = [k for k in ALLCH.values() if by[k]['type'] != p12[k]['type'] or by[k]['chapters'] != p12[k]['chapters'] or by[k]['bloom'] != p12[k]['bloom'] or units(by[k]) != units(p12[k])]
say('PASS' if not bad else 'FAIL', 'H1 each case item keeps the type, chapters, Bloom level and number of units of the item it replaces', str(bad))
say('PASS' if all(by[k].get('replaces') == [k] and by[k].get('owner_case') == c for c, k in ALLCH.items()) else 'FAIL', 'H1 each case item names the owner case and the item it replaces')
say('PASS' if os.path.exists(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')) and not [m for m in mods if 'v1_3_0' in m] else 'FAIL', 'H1 the items file is new (version 1.3.0)')
# H2 structure v1.0.0 unchanged and still consistent with the items
srel = os.path.relpath(STRUCT_FILE, ROOT)
sdiff = subprocess.run(['git', '-C', ROOT, 'diff', '--quiet', 'HEAD', '--', srel]).returncode
s_commits = subprocess.run(['git', '-C', ROOT, 'log', '--oneline', '--', srel], capture_output=True, text=True).stdout.strip().splitlines()
say('PASS' if sdiff == 0 and len(s_commits) == 1 else 'FAIL', 'H2 the structure v1.0.0 file is unchanged (no difference to the committed file; one commit)', '(commits touching it: %d)' % len(s_commits))
subs = {s_['key']: s_ for q in main_q for s_ in q['sub']}
bad = []
for k_, s_ in subs.items():
    it = by.get(s_['item'])
    if not it: bad.append((k_, 'item missing')); continue
    if s_['type'] != it['type'] and not (s_['type'] == 'ChoiceFourCode' and it['type'] == 'ChoiceFourCode'): bad.append((k_, 'type'))
    if s_['chapters'] != it['chapters'] or s_['bloom'] != it['bloom']: bad.append((k_, 'chapters or bloom'))
    if it['type'] == 'Ordering' and s_['parts'] != len(it['steps']): bad.append((k_, 'parts %s steps %d' % (s_['parts'], len(it['steps']))))
nb = {i['key']: sum(1 for s_ in subs.values() if s_['item'] == i['key']) for i in items}
bad += [(i['key'], 'sub-questions %d, units %d' % (nb[i['key']], units(i))) for i in items if nb[i['key']] != units(i)]
say('PASS' if not bad else 'FAIL', 'H2 every sub-question of the structure still matches its item: type, chapters, Bloom level, number of steps and one sub-question per unit', str(bad) if bad else '(%d sub-questions)' % len(subs))
pts = [q['points'] for q in main_q]
say('PASS' if pts == [25, 25, 25, 25] and bonus_q[0]['points'] == 10 and st['total_points_without_bonus'] == 100 and units_in == 24 else 'FAIL', 'H2 structure 25/25/25/25 + 10, 24 units, one unit per sub-question', '(points %s + %s)' % (pts, bonus_q[0]['points']))
lv = {t: 0 for t in range(1, 7)}
for i in items: lv[i['bloom']] += units(i)
lv12 = {t: 0 for t in range(1, 7)}
for i in prev12: lv12[i['bloom']] += units(i)
say('PASS' if lv == lv12 else 'FAIL', 'H2 units per Bloom level equal to v1.2.0', '(%s)' % lv)

# H3 C1: the order is recomputed from the printed steps
i06 = by[CASES['C1']]; ref = {}; outs_n = {}
for stp in i06['steps']:
    t = _re.match(r'Transaction (\w) ', stp).group(1)
    m = _re.search(r'spends (?:\(names as an input\) )?(?:the output|output (\d)) of transaction (\w)', stp)
    ref[t] = [m.group(2)] if m else []
    outs_n[t] = 1 if 'makes one output' in stp else 2
names_ = list(ref)
valid = [o for o in _it.permutations(names_) if all(o.index(p) < o.index(t) for t, ps in ref.items() for p in ps)]
cb = [t for t in ref if not ref[t]]
say('PASS' if len(valid) == 1 and list(valid[0]) == names_ and len(cb) == 1 and 'coinbase' in i06['steps'][0] and sorted(names_) != names_ else 'FAIL', 'H3 C1 ordering: from the spending references printed in the steps, exactly one of the 120 orders is possible; it is the key order; one coinbase transaction; the letters are not in alphabetical order', '(order %s)' % ' < '.join(valid[0]) if valid else str(valid))
say('PASS' if len(i06['steps']) == 5 and all(max(len(x) for x in [stp]) <= 190 for stp in i06['steps']) else 'FAIL', 'H3 C1 five steps of at most 190 characters (the answer sheet ordering block has five rows)', '(longest %d)' % max(len(x) for x in i06['steps']))
# H4 C2: the answers are recomputed from the printed facts
i07 = by[CASES['C2']]; txt = i07['blanks'][0]['text']
inblock = _re.findall(r'(?:^|[.:] )(\w) is inside a block', txt)
par = {}
for a_, b_ in _re.findall(r'(\w) spends (?:\(names as an input\) )?an output(?: \(a coin: an amount with a lock\))? of (\w)', txt): par.setdefault(a_, []).append(b_)
allt = sorted(set(par) | {p for v in par.values() for p in v})
states = []
for bits in _it.product([0, 1], repeat=len(allt)):
    mined = {n for n, b_ in zip(allt, bits) if b_}
    if set(inblock) <= mined and all(set(par.get(t, [])) <= mined for t in mined): states.append(mined)
forced = sorted(set.intersection(*states)); free = sorted(set.union(*states) - set.intersection(*states))
ab1 = _re.search(r'so (\w) and (\w) are ____', txt); ab2 = _re.search(r'therefore (\w) and (\w) are ____', i07['blanks'][1]['text'])
ok4 = ab1 and ab2 and sorted([ab1.group(1), ab1.group(2)]) == [x for x in forced if x not in inblock] and sorted([ab2.group(1), ab2.group(2)]) == free and i07['blanks'][0]['answer'].startswith('mined (') and i07['blanks'][1]['answer'].startswith('not shown to be mined')
say('PASS' if ok4 else 'FAIL', 'H4 C2 mined or not: from the printed facts, over all %d states, the transactions shown to be mined are %s and the undecided ones are %s; the two blank answers say exactly that' % (2 ** len(allt), forced, free), '(%d states agree with the facts)' % len(states))
say('PASS' if len(i07['distractors']) == 2 and all(' (' in x for x in i07['distractors'] + [b_['answer'] for b_ in i07['blanks']]) and len({b_['answer'] for b_ in i07['blanks']} | set(i07['distractors'])) == 4 else 'FAIL', 'H4 C2 bank: two answers and two distractors, all different, each with its tip in brackets')
# H5 C3: the arithmetic and the key are recomputed from the printed numbers
i02 = by[CASES['C3']]; qn = [int(x.replace(',', '')) for x in _re.findall(r'\d[\d,]*', i02['q'].split('Tips:')[0])]
ins_ = qn[:3]; pay_ = qn[3:5]; fee_a, fee_b = qn[5], qn[6]
left_ = sum(ins_) - sum(pay_); chg = left_ - fee_b
truth = []
for o in i02['options']:
    m1 = _re.match(r'Change ([\d,]+); (.*)', o); c_ = int(m1.group(1).replace(',', '')); rest = m1.group(2)
    if 'miner would collect all' in rest or 'miner would collect' in rest: nmb = int(_re.search(r'collect (?:all )?([\d,]+)', rest).group(1).replace(',', '')); ok_ = c_ == chg and nmb == left_
    else: ok_ = False
    truth.append(ok_)
say('PASS' if truth.count(True) == 1 and truth.index(True) == i02['answer'] else 'FAIL', 'H5 C3: inputs %s (sum %d), payments %s (sum %d), left over %d, fee %d, change %d; with no change output the miner collects %d; exactly one option is true and it is the key' % (ins_, sum(ins_), pay_, sum(pay_), left_, fee_b, chg, left_), '(truth of the options A-D: %s; key %s)' % (truth, 'ABCD'[i02['answer']]))
say('PASS' if chg < left_ - 0 and left_ - fee_a > chg else 'FAIL', 'H5 C3: the higher fee leaves less change (first fee %d leaves %d, raised fee %d leaves %d)' % (fee_a, left_ - fee_a, fee_b, chg))
# H6 simple arithmetic
figs = ins_ + pay_ + [fee_a, fee_b, sum(ins_), sum(pay_), left_, chg, left_ - fee_a]
say('PASS' if all(f % 1000 == 0 and f < 10 ** 6 for f in figs) and len(ins_) <= 3 and len(pay_) <= 2 and max(len(str(f)) for f in figs) <= 6 else 'FAIL', 'H6 simple arithmetic: every figure a whole thousand below one million, at most three numbers added or two subtracted in a step, no calculator needed', '(figures %s)' % sorted(set(figs)))
say('PASS' if not _re.search(r'\d', ' '.join(i06['steps'])) or all(len(x) == 1 for x in _re.findall(r'\d+', ' '.join(i06['steps']))) else 'FAIL', 'H6 C1 needs no arithmetic (only output numbers 0 and 1)')
# H7 a tip for every term, printed with the item
bad = []
for k_ in ALLCH.values():
    i = by[k_]; pr = printed(i).lower(); body = (i.get('q', '') + ' ' + ' '.join(i.get('steps', [])) + ' ' + ' '.join(b_['text'] for b_ in i.get('blanks', [])) + ' ' + ' '.join(b_['answer'] for b_ in i.get('blanks', [])) + ' ' + ' '.join(i.get('distractors', []))).lower()
    for t_ in i['tips']:
        if t_[1].lower() not in pr: bad.append((k_, 'tip text not printed: ' + t_[0]))
    for t in i['terms']:
        tl = t.lower()
        if tl in body.replace(' '.join(x[1].lower() for x in i['tips']), ''):
            if not any(tl in x[0].lower() or x[0].lower() in tl for x in i['tips']): bad.append((k_, 'term printed with no tip: ' + t))
say('PASS' if not bad else 'FAIL', 'H7 in the four case items every course term that is printed has a tip, and every tip is printed with the item (stem tips in the stem; step, sentence and bank tips in brackets)', str(bad) if bad else '(tips: %s)' % {k_: [x[0] for x in by[k_]['tips']] for k_ in ALLCH.values()})
# H8 abbreviations and synthetic data
bad = []
for k_ in ALLCH.values():
    pr = printed(by[k_])
    for tok in _re.findall(r'(?<![A-Za-z0-9])[A-Z]{2,}[A-Za-z0-9]*(?![A-Za-z0-9])', pr): bad.append((k_, 'capital token: ' + tok))
    if _re.search(r'\b[0-9a-fA-F]{16,}\b', pr) or _re.search(r'0x', pr): bad.append((k_, 'hexadecimal string'))
    if by[k_].get('abbreviations'): bad.append((k_, 'abbreviations field not empty'))
say('PASS' if not bad else 'FAIL', 'H8 the four case items use no abbreviation (no capital-letter token of two or more letters, no hexadecimal string); single capital letters are transaction labels A to J; names are the stand-ins Ana and Ben', str(bad))
# H11 B: the block reward case is recomputed from the printed numbers
i03 = by[BREWORK['B']]; qq = i03['q'].split('Tips:')[0]
nums = [int(x) for x in _re.findall(r'\d+', qq)]
sub0_, intv_, h_, fee_, claim_ = nums[0], nums[2], nums[3], nums[4], nums[5]
sub_ = sub0_ >> (h_ // intv_); exc_ = claim_ - (sub_ + fee_)
say('PASS' if exc_ == i03['key_value'] and exc_ > 0 and len(str(i03['key_value'])) <= 5 and i03['unit'] == 'coins' else 'FAIL', 'H11 B block reward: subsidy %d at height 0, halved every %d blocks; height %d lies in interval %d so the subsidy is %d; fees %d; the legal limit is %d; the claim %d is illegal and too large by %d = the key' % (sub0_, intv_, h_, h_ // intv_, sub_, fee_, sub_ + fee_, claim_, exc_), '(key %s)' % i03['key_value'])
say('PASS' if all(x < 100 for x in nums) and (h_ // intv_) <= 3 else 'FAIL', 'H11 B simple arithmetic: every number below 100, at most three halvings, no calculator needed', str(nums))
# H12 the owner's new points A to F (21:23), as printed by the builder
print('\nNEW POINTS MAP (as printed by the builder):')
print(open(os.path.join(HERE, 'sen0401_exam_items_midterm_new_points_map_v1_3_0.txt'), encoding='utf8').read())
# H9 owner topics: the newest file is read, and the map holds all nine topics
tfs = sorted(_glob.glob(os.path.join(HERE, 'sen0401_exam_owner_topics_v*.json')), key=lambda p: tuple(int(x) for x in _re.search(r'_v(\d+)_(\d+)_(\d+)\.json$', p).groups()))
newest = tfs[-1]; tdoc = json.load(open(newest, encoding='utf8'))
tm = json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_topic_map_v1_3_0.json'), encoding='utf8'))
okmap = tm['owner_topics_file'] == os.path.basename(newest) and [r['id'] for r in tm['rows']] == [t['id'] for t in tdoc['topics']] and all(r['item_keys'] == 'GAP' or all(k in by for k in r['item_keys']) for r in tm['rows'])
okcases = [c['id'] for c in tdoc['cases']] == list(CASES) and all(c['suggested_replaces'].startswith(CASES[c['id']].split(':')[0] + ':' + CASES[c['id']].split(':')[1]) and c['block'] == {'C1': 'Ordering', 'C2': 'FillBlankGroup', 'C3': 'ChoiceFour'}[c['id']] for c in tdoc['cases']) and tdoc['kept_by_the_lineage_agent'] == KEPT
say('PASS' if okmap else 'FAIL', 'H9 the topic map was made from the NEWEST owner topics file (%s, %d topics) and gives every topic an item key or GAP' % (os.path.basename(newest), len(tdoc['topics'])), '(files found: %s)' % [os.path.basename(x) for x in tfs])
say('PASS' if okcases else 'FAIL', 'H9 the three cases sit on the blocks and the items the owner file suggests; the two kept items are the ones the owner file names')
print('\nTOPIC MAP (as printed by the builder):')
print(open(os.path.join(HERE, 'sen0401_exam_items_midterm_topic_map_v1_3_0.txt'), encoding='utf8').read())
# H10 critical points: the links of the three cases, G5 against v1.2.0, and the critical-points tool
b12 = {c for i in prev12 for c in i['critical_points']}; a13 = {c for i in items for c in i['critical_points']}
say('PASS' if not (b12 - a13) else 'FAIL', 'H10 critical points of v1.2.0 that v1.3.0 no longer links', 'lost %s ; gained %s ; before %d, after %d' % (sorted(b12 - a13), sorted(a13 - b12), len(b12), len(a13)))
held_only = sorted(c for c in b12 if not any(c in p12[k_]['critical_points'] for k_ in p12 if k_ not in ALLCH.values()))
print('NOTE         points that v1.2.0 held ONLY through the four replaced or reworked items, and the case item that links each now (a person judges how strong each link is):')
for c in held_only: print('NOTE           %s -> %s' % (c, [k_.split(':')[1] for k_ in ALLCH.values() if c in by[k_]['critical_points']]))
r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'sen0401_exam_critical_points_check_v1_0_0.py')], capture_output=True, text=True)
last = [l for l in r.stdout.splitlines() if l.startswith('RESULT')]
print('--- critical points tool (sen0401_exam_critical_points_check_v1_0_0.py), exit %d, printed as it is:' % r.returncode)
print(r.stdout.rstrip())
say('PASS' if r.returncode == 0 and last and 'PASS' in last[0] else 'FAIL', 'H10 the critical-points tool passes (exit code 0)', last[0] if last else r.stderr[:200])
# H11 notes for the papers task (measured, not judged)
st_ins = subs['Q3.a']['instruction']
print('NOTE         Q3.a instruction printed by the paper from the structure v1.0.0 (unchanged): "%s"' % st_ins)
print('NOTE         Q3.a instruction written in the item: "%s"' % i06['instruction'])
print('NOTE         text lengths (characters of q or steps): C3 %d (v1.2.0 %d); C1 steps %d (v1.2.0 %d); C2 blanks %d (v1.2.0 %d)' % (len(i02['q']), len(p12[CASES['C3']]['q']), sum(len(x) for x in i06['steps']), sum(len(x) for x in p12[CASES['C1']]['steps']), sum(len(b_['text']) for b_ in i07['blanks']), sum(len(b_['text']) for b_ in p12[CASES['C2']]['blanks'])))
print('NOTE         the structure file still names items_file = %s (a data field of the unchanged structure); the papers task reads the items file named by its own argument or a new structure file' % st['items_file'])

print('\nRESULT', 'FAIL (%s)' % '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
