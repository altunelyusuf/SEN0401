#!/usr/bin/env python3
"""SEN0401 midterm items check, version 1.4.0 (new file; it holds no question text and no answer, so it may be committed; it prints item KEYS and counts, never a question, an option or a key value).

Checks the PRIVATE merged items file 08-tooling/exam/private/sen0401_exam_items_midterm_v1_4_0.json against the PRIVATE structure sen0401_exam_structure_v1_1_0.json (one form), the private topic map
and the engine v1.1.0. It is derived from check v1.3.0 (the checks F1 to F8 and G1 to G4 are ported; v1.3.0 itself is bound to its own builder and to the structure v1.0.0 and cannot be run on this file).
What differs from v1.3.0, stated plainly: G5 (no critical point lost against v1.1.0) cannot hold for a merge in which the parts replaced items, so it NAMES every critical point that lost its only holder and every
point recovered (as the task asks); the v1.3.0 checks H1 to H12 (bound to the three cases of that file) are replaced by the checks M1 to M12 below. Nothing is relaxed that the task still asks for.
Every line is printed as PASS, FAIL or NOT_MEASURED; the exit code is 0 only when no line is FAIL.

  L1  leak guard: the three files lie in private/, are git-ignored, untracked, never committed, not staged; this script holds no string of any item
  F1  no tracked file of 08-tooling/exam is modified; the items file is not tracked
  F2  24 units (a fill-in blank is one unit), 4 per chapter by primary chapter, midterm only, unique keys, suited types, no bank or quiz item
  F3  seeds, critical points, enhancements, chapters, level, kind, source and terms complete and resolving
  F4  every trace listing run again here gives its key; every number item recomputed here from its own data; the three owner cases recomputed from their printed text; the builders run again give the same files
  F5  EN08 terms found in the corpus     F6  EN11 no copy of a page-visible item     F7  conventions (Bloom, code size, answer length, options)
  F8  the engine v1.1.0 builds the midterm with no Violation (EN01-EN13, R01-R22), letters of the keys evenly spread
  G1  structure: four questions of 25 points and a bonus of 10, every item used once, blocks, hand-marked bonus
  G2  every abbreviation spelled out before first use     G3  a tip for every term     G4  no recall wording, every bank entry has its tip
  M1  structure v1.1.0 agrees with the items (type, chapters, Bloom level, parts, units, points) and its answer-block type of EVERY position equals the structure v1.0.0
  M2  chapter weights equal (4 per chapter by primary chapter) and at least two units per chapter    M3  Bloom levels and the type caps
  M4  option lengths: the correct option is neither the longest nor the shortest, near the mean of the others, the options within 20 percent; unused matching responses as long as the used ones
  M5  the Q3.a instruction is the item's own instruction     M6  the provisional items and their reasons
  M7  critical points: lost sole holders named, recovered, gained; the drops with the points that lose their only holder     M8  the critical-points tool
  M9  the topic map: every point of the newest owner file, status, item keys that resolve     M10 the paper library v3.0.0 accepts the structure with the items
Usage: sen0401_exam_items_midterm_check_v1_4_0.py [--items FILE] [--structure FILE] [--map FILE]
"""
import glob, json, os, re, subprocess, sys, tempfile, io, contextlib, itertools, math, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE)); PRIV = os.path.join(HERE, 'private')
ITEMS_FILE = os.path.join(PRIV, 'sen0401_exam_items_midterm_v1_4_0.json')
STRUCT_FILE = os.path.join(PRIV, 'sen0401_exam_structure_v1_1_0.json')
MAP_FILE = os.path.join(PRIV, 'sen0401_exam_topic_map_v1_4_0.json')
for a, n in (('--items', 'ITEMS_FILE'), ('--structure', 'STRUCT_FILE'), ('--map', 'MAP_FILE')):
    if a in sys.argv: globals()[n] = sys.argv[sys.argv.index(a) + 1]
BUILD_MERGE = os.path.join(PRIV, 'sen0401_exam_items_merge_build_v1_4_0.py'); BUILD_MAP = os.path.join(PRIV, 'sen0401_exam_topic_map_build_v1_4_0.py')
V13_FILE = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json'); S10_FILE = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
PARTS = [os.path.join(PRIV, 'sen0401_exam_items5%s_v1_0_0.json' % x) for x in 'abc']
BUILDER_PREV = os.path.join(HERE, 'sen0401_exam_items_midterm_build_v1_2_0.py')
ALLOWED_ENH = {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}
SUITED = {'ChoiceFour', 'ChoiceFourCode', 'Matching', 'Ordering', 'FillBlankGroup', 'NumericAnswer', 'CodeTrace'}
CAP = {'ChoiceFour': 4, 'ChoiceFourCode': 4, 'Matching': 3, 'Ordering': 3, 'FillBlankGroup': 2, 'NumericAnswer': 3, 'CodeTrace': 4}
fails = []


def say(status, name, detail=''):
    print('%-12s %s %s' % (status, name, detail))
    if status == 'FAIL': fails.append(name)


def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


def git(*a): return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True)


def strings_of(i):
    out = [i.get('q', ''), i.get('code', '')] + list(i.get('options', [])) + list(i.get('steps', [])) + list(i.get('responses', [])) + list(i.get('distractors', []))
    out += [p['text'] for p in i.get('premises', [])] + [b['text'] + ' ' + b['answer'] for b in i.get('blanks', [])]
    out += [x for t in i.get('tips', []) for x in t]
    return [s for s in out if s]


doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']; by = {i['key']: i for i in items}
st = json.load(open(STRUCT_FILE, encoding='utf8')); s10 = json.load(open(S10_FILE, encoding='utf8'))
v13 = json.load(open(V13_FILE, encoding='utf8'))['items']
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S
cp = E.cp_index()
Qs = st['questions']; main_q = [q for q in Qs if not q.get('bonus')]; bonus_q = [q for q in Qs if q.get('bonus')]
hand = [s for q in bonus_q for s in q['sub']]
subs = {s['key']: s for q in main_q for s in q['sub']}

# ------------------------------------------------------------------ L1 leak guard
for nm, p in (('items', ITEMS_FILE), ('structure', STRUCT_FILE), ('map', MAP_FILE)):
    rel = os.path.relpath(p, ROOT)
    inside = os.path.commonpath([os.path.abspath(p), PRIV]) == PRIV
    ign = git('check-ignore', '-q', rel).returncode == 0
    tr = git('ls-files', '--error-unmatch', rel).returncode == 0
    lg = git('log', '--oneline', '--', rel).stdout.split()
    say('PASS' if inside and ign and not tr and not lg else 'FAIL', 'L1 %s file: in private/, git-ignored, not tracked, never committed' % nm, '(inside %s, ignored %s, tracked %s, commits %d)' % (inside, ign, tr, len(lg)))
staged = [l for l in git('diff', '--cached', '--name-only').stdout.split() if '/exam/private/' in l]
tracked_private = git('ls-files', '--', os.path.relpath(PRIV, ROOT)).stdout.split()
say('PASS' if not staged and not tracked_private else 'FAIL', 'L1 nothing of private/ is staged or tracked', '(staged %d, tracked %d)' % (len(staged), len(tracked_private)))
me = open(os.path.abspath(__file__), encoding='utf8').read()
longs = {s for i in items for s in strings_of(i) if len(s) >= 25} | {s for b in hand for s in [b['prompt']] + list(b['rubric'])}
leaked = [s[:20] for s in longs if s in me]
say('PASS' if not leaked and longs else 'FAIL', 'L1 this script holds none of the %d printed strings (25 characters or longer) of the items and the bonus prompts' % len(longs), str(leaked))
others = [l for l in git('status', '--porcelain').stdout.splitlines() if l[:2].strip() in ('M', 'D')]
say('PASS', 'L1 notice: tracked files modified in the working tree by OTHER sessions (not by this task; listed by count, not judged)', '(%d files, none under 08-tooling/exam: %s)' % (len(others), not any('08-tooling/exam/' in l for l in others)))

# ------------------------------------------------------------------ F1
exam_mods = [l for l in git('status', '--porcelain', '--', '08-tooling/exam').stdout.splitlines() if l[:2].strip() in ('M', 'D', 'MM', 'AM', 'R', 'T')]
say('PASS' if not exam_mods else 'FAIL', 'F1 no tracked file under 08-tooling/exam is modified or deleted (a committed file is never edited)', str(exam_mods or 'none'))
for nm in ('v1_3_0', 'v1_2_0'):
    pth = os.path.join(HERE, 'sen0401_exam_items_midterm_%s.json' % nm)
    say('PASS' if git('diff', '--quiet', 'HEAD', '--', os.path.relpath(pth, ROOT)).returncode == 0 else 'FAIL', 'F1 items %s is byte-equal to its committed file' % nm)
say('PASS' if git('diff', '--quiet', 'HEAD', '--', os.path.relpath(S10_FILE, ROOT)).returncode == 0 else 'FAIL', 'F1 structure v1.0.0 is byte-equal to its committed file')

# ------------------------------------------------------------------ F2
n_units = sum(units(i) for i in items)
say('PASS' if n_units == 24 else 'FAIL', 'F2 24 items (units)', '(%d items, %d units)' % (len(items), n_units))
per = {c: sum(units(i) for i in items if i['chapters'][0] == c) for c in range(1, 7)}
say('PASS' if all(v == 4 for v in per.values()) else 'FAIL', 'F2 4 units per chapter by primary chapter', str(per))
say('PASS' if all(i['papers'] == ['midterm'] for i in items) else 'FAIL', 'F2 every item is for the midterm only (ONE form)')
bad = [i['key'] for i in items if str(i['key']).startswith('bank:') or 'question_bank' in i['source']['file'] or re.search(r'quiz_v\d', i['source']['file'])]
say('PASS' if not bad else 'FAIL', 'F2 no item is a bank item or a page quiz item (key and source file)', str(bad))
say('PASS' if len({i['key'] for i in items}) == len(items) else 'FAIL', 'F2 item keys are unique')
say('PASS' if all(i['type'] in SUITED for i in items) else 'FAIL', 'F2 every type is a suited type of the paper registry', str(sorted({i['type'] for i in items})))
say('PASS' if doc.get('one_form') is True and st.get('one_form') is True and st.get('forms') == 1 else 'FAIL', 'F2 ONE form in the items file and in the structure (no forms A and B)')

# ------------------------------------------------------------------ F3
pages = S.page_items((1, 2, 3, 4, 5, 6)); page_refs = {p['ref']: p for p in pages}
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
    if not enh or not set(enh) <= ALLOWED_ENH: problems.append((k, 'enhancement missing or not one of the five'))
    if i['kind'] not in ('direct', 'synthesis'): problems.append((k, 'kind must be direct or synthesis'))
    if i['kind'] == 'synthesis' and len(set(i['chapters'])) < 2: problems.append((k, 'synthesis item with one chapter'))
    if i['kind'] == 'direct' and len(set(i['chapters'])) > 1: problems.append((k, 'direct item with several chapters'))
    if not (1 <= i['bloom'] <= 6): problems.append((k, 'bloom'))
    f = i['source'].get('file'); loc = i['source'].get('locator')
    if not f or not os.path.exists(os.path.join(ROOT, f)) or not loc: problems.append((k, 'source file missing or no locator'))
    for sx in i.get('sources', []):
        if not os.path.exists(os.path.join(ROOT, sx['file'])): problems.append((k, 'extra source file missing: ' + sx['file']))
    if not i.get('terms'): problems.append((k, 'no terms'))
say('PASS' if not problems else 'FAIL', 'F3 seed links, point links, enhancements, chapters, level, kind, type, source and terms are complete and resolve', str(problems) if problems else '(%d items)' % len(items))
say('PASS', 'F3 share of items with a seed (measured, not a pass condition)', '(%d of %d items; the others carry their reason)' % (sum(1 for i in items if i.get('seeds')), len(items)))

# ------------------------------------------------------------------ F4
def run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<item>', 'exec'), {})
    return buf.getvalue().strip()


bad = []; nt = 0
for i in items:
    if i['type'] == 'CodeTrace':
        nt += 1
        try: got = run(i['code'])
        except Exception as e: got = 'ERROR ' + type(e).__name__
        if got != i['output']: bad.append(i['key'])
say('PASS' if not bad else 'FAIL', 'F4 trace items: the listing run again here prints the key (values not printed)', str(bad) if bad else '(%d trace items)' % nt)
# number items recomputed from their own data
def nums_in(q): return {int(x.replace(',', '')) for x in re.findall(r'\d[\d,]*', q)}
def recompute(i):
    d = i.get('data') or {}; m = d.get('model')
    if m == 'vanity_time': return d['base_minutes'] * d['symbols'] ** (d['letters_new'] - d['letters_old']) // d['speedup']
    if m == 'halving_claim': return d['claim'] - ((d['start'] >> (d['height'] // d['interval'])) + d['fees'])
    if m == 'greedy_fee':
        room = d['room']; tot = 0
        for n, size, fee, amt in sorted(d['txs'], key=lambda t: -t[2] / t[1]):
            if size <= room: room -= size; tot += fee
        return tot
    if m == 'vwap_value':
        vol = sum(c for c, p in d['trades']); day = sum(c * p for c, p in d['trades']) // vol
        return day * d['coins'] // d['divisor']
    if m == 'pool_wait': return d['interval'] * d['network_after'] // d['pool']
    if i['key'] == 'mt2:i17:words-to-entropy':
        w_, b_, c_ = [int(x) for x in re.search(r'has (\d+) words\. Each word carries (\d+) bits, and the checksum is one bit for every (\d+) bits', i['q']).groups()]
        return [e for e in range(0, w_ * b_ + 1) if e + e // c_ == w_ * b_ and e % c_ == 0][0]
    return None
bad = []; nn = 0
for i in items:
    if i['type'] == 'NumericAnswer':
        nn += 1; r = recompute(i)
        if r is None or str(r) != str(i['key_value']): bad.append(i['key'])
        d = i.get('data') or {}
        for k_, v in d.items():
            if isinstance(v, int) and not isinstance(v, bool) and v >= 10 and v not in nums_in(i['q']) and k_ not in ('base_minutes',) and v not in (1000000,):
                if str(v) not in i['q'] and format(v, ',') not in i['q']: bad.append((i['key'], 'data not printed: ' + k_))
say('PASS' if not bad else 'FAIL', 'F4 number items: the key recomputed here from the item\'s own data (models: vanity, halving claim, greedy fee, volume-weighted value, entropy) equals key_value; the data figures are printed in the stem', str(bad) if bad else '(%d number items; values not printed)' % nn)
# the three owner cases recomputed from their printed text
i06 = by['mt2:i06:order-wallet-to-block']; ref = {}
for stp in i06['steps']:
    t = re.match(r'Transaction (\w) ', stp).group(1)
    m = re.search(r'spends (?:\(names as an input\) )?(?:the output|output (\d)) of transaction (\w)', stp)
    ref[t] = [m.group(2)] if m else []
names_ = list(ref)
valid = [o for o in itertools.permutations(names_) if all(o.index(p) < o.index(t) for t, ps in ref.items() for p in ps)]
say('PASS' if len(valid) == 1 and list(valid[0]) == names_ and [t for t in ref if not ref[t]] == [names_[0]] and 'coinbase' in i06['steps'][0] and sorted(names_) != names_ else 'FAIL',
    'F4 C1 ordering: from the spending references printed in the steps exactly one of the %d orders is possible and it is the key order; one coinbase transaction; labels not alphabetical' % math.factorial(len(names_)), '(%d steps)' % len(names_))
i07 = by['mt3:i07:fill-mined-or-not']; txt = i07['blanks'][0]['text']
inblock = re.findall(r'(?:^|[.:] )(\w) is inside a block', txt); par = {}
for a_, b_ in re.findall(r'(\w) spends (?:\(names as an input\) )?an output(?: \(a coin[^)]*\))? of (\w)', txt): par.setdefault(a_, []).append(b_)
allt = sorted(set(par) | {p for v in par.values() for p in v}); states = []
for bits in itertools.product([0, 1], repeat=len(allt)):
    mined = {n for n, b_ in zip(allt, bits) if b_}
    if set(inblock) <= mined and all(set(par.get(t, [])) <= mined for t in mined): states.append(mined)
forced = sorted(set.intersection(*states)); free = sorted(set.union(*states) - set.intersection(*states))
ab1 = re.search(r'so (\w) and (\w) are ____', txt); ab2 = re.search(r'therefore (\w) and (\w) are ____', i07['blanks'][1]['text'])
ok = ab1 and ab2 and sorted([ab1.group(1), ab1.group(2)]) == [x for x in forced if x not in inblock] and sorted([ab2.group(1), ab2.group(2)]) == free and i07['blanks'][0]['answer'].startswith('mined (') and i07['blanks'][1]['answer'].startswith('not shown to be mined')
say('PASS' if ok else 'FAIL', 'F4 C2 mined or not: over all %d states the facts printed in the item force and leave open exactly the payments that the two blanks name' % (2 ** len(allt)), '(%d states agree with the facts)' % len(states))
i02 = by['mt2:i02:fee-not-written']; qn = [int(x.replace(',', '')) for x in re.findall(r'\d[\d,]*', i02['q'].split('Tips:')[0])]
ins_, pay_, fee_b = qn[:3], qn[3:5], qn[6]; left_ = sum(ins_) - sum(pay_); chg = left_ - fee_b; truth = []
for o in i02['options']:
    m1 = re.match(r'Change ([\d,]+); (.*)', o); c_ = int(m1.group(1).replace(',', '')); rest = m1.group(2)
    m2 = re.search(r'miner would collect all ([\d,]+) left over', rest)
    truth.append(bool(m2) and c_ == chg and int(m2.group(1).replace(',', '')) == left_)
say('PASS' if truth.count(True) == 1 and truth.index(True) == i02['answer'] and all(f % 1000 == 0 and f < 10 ** 6 for f in ins_ + pay_ + [left_, chg]) else 'FAIL',
    'F4 C3 full spending: recomputed from the printed amounts exactly one option is true and it is the key; every figure a whole thousand below one million (no calculator)', '(truth by option computed; values not printed)')
# builders run again give the same files
with tempfile.TemporaryDirectory(dir=PRIV) as td:
    r = subprocess.run([sys.executable, '-I', BUILD_MERGE, '--outdir', td], capture_output=True, text=True, cwd=PRIV)
    same = r.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_items_midterm_v1_4_0.json'), encoding='utf8')) == doc and json.load(open(os.path.join(td, 'sen0401_exam_structure_v1_1_0.json'), encoding='utf8')) == st
    say('PASS' if same else 'FAIL', 'F4 the merge builder, run again, writes the same items file and the same structure', '(exit %d)' % r.returncode)

# ------------------------------------------------------------------ F5, F6
unf = {i['key']: E0.unfound_terms(i) for i in items}; unf = {k: v for k, v in unf.items() if v}
say('PASS' if not unf else 'FAIL', 'F5 EN08 every term of every item is found in the course corpus', str(unf) if unf else '(%d terms)' % sum(len(i['terms']) for i in items))
hits = []
for i in items:
    for label, ref_, kinds, ss, os_ in E.check_copies(i, pages): hits.append((i['key'], label, ref_, kinds, ss, os_))
say('PASS' if not hits else 'FAIL', 'F6 EN11 no component of any item matches a page-visible item', '(checked against %d page items)' % len(pages) if not hits else str(hits))
best = []
for i in items:
    for label, stem, opts in S.components(i):
        c_ = S.prepare(stem, opts)
        for p in pages:
            kinds, ss, os_ = S.compare(c_, p['p']); best.append((ss, os_, i['key'], label, p['ref']))
best.sort(reverse=True)
say('PASS', 'F6 largest stem share found against any page item (measured; refusal at %.2f)' % S.STEM_NEAR_J2, '(%.3f: %s %s against %s)' % (best[0][0], best[0][2], best[0][3], best[0][4]))
bo = sorted(best, key=lambda x: -x[1])[0]
say('PASS', 'F6 largest option share found against any page item (measured; refusal at %.2f)' % S.OPTIONS_NEAR_SHARE, '(%.3f: %s %s against %s)' % (bo[1], bo[2], bo[3], bo[4]))

# ------------------------------------------------------------------ F7
ge3 = sum(units(i) for i in items if i['bloom'] >= 3); ge4 = sum(units(i) for i in items if i['bloom'] >= 4)
say('PASS' if ge3 * 2 > n_units else 'FAIL', 'F7 a majority at Apply or above', '(%d of %d)' % (ge3, n_units))
say('PASS' if ge4 >= 6 else 'FAIL', 'F7 at least 6 units at Analyze or above (the minimum is not relaxed)', '(%d of %d)' % (ge4, n_units))
bad = [i['key'] for i in items if i['bloom'] > CAP[i['type']]]
say('PASS' if not bad else 'FAIL', 'F7 no level above what the type can honestly reach (registry; NumericAnswer at most 3, rule R06)', str(bad))
cl = [(i['key'], max(len(l) for l in i['code'].split('\n')), len(i['code'].split('\n'))) for i in items if i.get('code')]
bad = [x for x in cl if x[1] > 45 or x[2] > 12]
say('PASS' if not bad else 'FAIL', 'F7 code lines at most 45 characters, at most 12 lines', str(bad) if bad else '(widest line %d characters, longest listing %d lines)' % (max(x[1] for x in cl), max(x[2] for x in cl)))
bad = [(i['key']) for i in items if i['type'] in ('NumericAnswer', 'CodeTrace') and len(str(i['key_value'] if i['type'] == 'NumericAnswer' else i['output'])) > 5]
say('PASS' if not bad else 'FAIL', 'F7 number and trace answers of at most 5 characters (the answer sheet gives five boxes)', str(bad))
refx = re.compile(r'\b(all|none|both) of the (above|options|choices)\b|\b(option|choice) [A-D]\b|\b[A-D] (and|or) [A-D]\b', re.I)
bad = [i['key'] for i in items if i['type'] in ('ChoiceFour', 'ChoiceFourCode') and (any(refx.search(o) for o in i['options']) or len(set(i['options'])) < 4 or len(i['options']) != 4)]
say('PASS' if not bad else 'FAIL', 'F7 four distinct options, none that refers to another option', str(bad))
bad = [i['key'] for i in items if i['type'] == 'FillBlankGroup' and len(i['blanks']) + len(i['distractors']) > 9]
say('PASS' if not bad else 'FAIL', 'F7 a fill-in bank has at most 9 entries (EN13)', str(bad))
bad = [i['key'] for i in items if i['type'] == 'Matching' and not (len(i['premises']) == 4 and len(i['responses']) == 6)]
say('PASS' if not bad else 'FAIL', 'F7 a matching item has 4 premises and 6 responses (two unused), as the sheet block', str(bad))
bad = [i['key'] for i in items if i['type'] == 'Ordering' and len(i['steps']) != 5]
say('PASS' if not bad else 'FAIL', 'F7 the ordering item has 5 steps (five rows on the sheet)', str(bad))

# ------------------------------------------------------------------ F8
P = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=ITEMS_FILE)
os.environ.setdefault('SEN0401_ENGINE_TMP', tempfile.gettempdir())
try:
    paper, g, p = E.make_and_check(P, 'midterm')
    viol = E.validate(g, P.chapters); v = [x for x in viol if x[1] == 'Violation']; w = [x for x in viol if x[1] != 'Violation']
    say('PASS' if not v else 'FAIL', 'F8 engine v1.1.0: the midterm built from these items has no Violation (EN01-EN13, R01-R22)', str(v) if v else '(pages with the answer sheet: %s, content pages %s, sheet pages %s)' % (paper.get('pageCount'), paper.get('contentPages'), paper.get('sheetPages')))
    for x in w: say('PASS', 'F8 non-violation notice (' + x[1] + ')', x[2])
    letters = {}
    for it in paper['items']:
        if it['type'] in ('ChoiceFour', 'ChoiceFourCode'): letters['ABCD'[it['answer']]] = letters.get('ABCD'[it['answer']], 0) + 1
    say('PASS' if letters and max(letters.values()) - min(letters.values()) <= 1 and len(letters) == 4 else 'FAIL', 'F8 answer letters of the choice items are evenly spread in the built paper', str(dict(sorted(letters.items()))))
    say('PASS' if paper['pool_size'] == len(items) and len(paper['items']) == len(items) else 'FAIL', 'F8 the paper holds all authored items (none chosen from a bank)', '(pool %d, paper items %d, skipped %s)' % (paper['pool_size'], len(paper['items']), paper['skipped']))
    say('PASS' if all(paper['quotas'][c] == 4 for c in range(1, 7)) else 'FAIL', 'F8 the quotas of the built paper (EN01, EN07): equal chapter weights hold, no weight had to be declared', str(paper['quotas']))
except E.ExamRefused as e:
    say('FAIL', 'F8 engine v1.1.0 refused the midterm', str(e))

# ------------------------------------------------------------------ G1
ALLOWED_BLOCKS = {'ChoiceFour', 'NumericAnswer', 'Ordering', 'Matching', 'FillBlankGroup'}
ok = len(main_q) == 4 and all(q['points'] == 25 and sum(s_['points'] for s_ in q['sub']) == 25 and q['sub'] for q in main_q) and len(bonus_q) == 1 and bonus_q[0]['points'] == 10 and sum(s_['points'] for s_ in bonus_q[0]['sub']) == 10 and bonus_q[0]['number'] == 5
say('PASS' if ok else 'FAIL', 'G1 structure: four questions of 25 points, each with sub-questions that add up, and a fifth bonus question of 10 points', '(points %s, bonus %s, total %s)' % ([q['points'] for q in main_q], [q['points'] for q in bonus_q], st['total_points_without_bonus']))
used = [s_['item'] for q in main_q for s_ in q['sub']]
blank_subs = [s_ for q in main_q for s_ in q['sub'] if s_['type'] == 'FillBlankGroup']
cover = all(k in by for k in used) and sorted(set(used)) == sorted(by) and len(used) - len(blank_subs) + len(set(s_['item'] for s_ in blank_subs)) == len(by) and len(blank_subs) == sum(len(i['blanks']) for i in items if i['type'] == 'FillBlankGroup')
say('PASS' if cover else 'FAIL', 'G1 every item is used exactly once in the main questions (each fill-in blank is a sub-question) and every sub-question key resolves', '(items %d, sub-questions %d)' % (len(by), sum(len(q['sub']) for q in main_q)))
blocks = {s_['block'] for q in main_q for s_ in q['sub']}
say('PASS' if blocks <= ALLOWED_BLOCKS and len(Qs) == 5 and len({q['format'] for q in Qs}) == 5 else 'FAIL', 'G1 five different formats; the answer sheet block types stay in the unchanged set', str(sorted(blocks)))
say('PASS' if hand and all(s_['hand_marked'] and not s_['machine_read'] and s_['rubric_points'] <= 3 and s_['block'].startswith('NONE') for s_ in hand) and bonus_q[0]['hand_marked'] and not bonus_q[0]['machine_read'] else 'FAIL',
    'G1 short explanation items are hand-marked, not machine-read, rubric of at most 3 points', '(%d prompts)' % len(hand))
bad = [(s_['key'], E0.unfound_terms({'terms': s_['terms']})) for s_ in hand if E0.unfound_terms({'terms': s_['terms']})]
say('PASS' if not bad else 'FAIL', 'G1 EN08 for the bonus prompts: every term is found in the course corpus', str(bad) if bad else '(%d terms)' % sum(len(s_['terms']) for s_ in hand))
bad = [s_['item'] for s_ in hand for src_ in s_['sources'] if not os.path.exists(os.path.join(ROOT, src_['file']))]
say('PASS' if not bad else 'FAIL', 'G1 the sources of the bonus prompts exist', str(bad))
bad = [(s_['key'], c) for s_ in hand for c in s_['critical_points'] if c not in cp]
say('PASS' if not bad else 'FAIL', 'G1 the critical points of the bonus prompts exist', str(bad))

# ------------------------------------------------------------------ G2 abbreviations
ABBRS = {'WIF': 'wallet import format', 'P2PKH': 'pay to public key hash', 'SegWit': 'segregated witness', 'SHA256': 'secure hash algorithm 256', 'BIP329': 'bitcoin improvement proposal 329',
         'txid': 'transaction identifier', 'wtxid': 'witness transaction identifier', 'UTXO': 'unspent transaction output', 'BIP': 'bitcoin improvement proposal', 'BTC': 'bitcoin', 'SHA-256': 'secure hash algorithm',
         'P2SH': 'pay to script hash', 'HD': 'hierarchical deterministic', 'RBF': 'replace-by-fee', 'RPC': 'remote procedure call', 'ASIC': 'application-specific integrated circuit', 'TL': 'turkish lira', 'YTL': 'new turkish lira'}
bad = []
for i in items:
    text_only = (i.get('q', '') + ' ' + ' '.join(i.get('options', [])) + ' ' + ' '.join(i.get('steps', [])) + ' ' + ' '.join(p_['text'] for p_ in i.get('premises', [])) + ' ' + ' '.join(i.get('responses', []))
                 + ' ' + ' '.join(b_['text'] for b_ in i.get('blanks', [])) + ' ' + ' '.join(i.get('distractors', [])) + ' ' + ' '.join(b_['answer'] for b_ in i.get('blanks', [])))
    tl = text_only.lower()
    for ab, full in ABBRS.items():
        m = re.search(r'(?<![A-Za-z0-9])' + re.escape(ab) + r'(?![A-Za-z0-9])', text_only, re.I if ab in ('txid', 'wtxid') else 0)
        if not m: continue
        j = tl.find(full)
        if j < 0 or j > m.start(): bad.append((i['key'], ab, 'first use at %d, full form at %d' % (m.start(), j)))
for s_ in hand:
    tl = (s_['prompt'] + ' ' + ' '.join(t[0] + ' ' + t[1] for t in s_['tips']) + ' ' + ' '.join(s_['rubric'])).lower()
    for ab, full in ABBRS.items():
        if re.search(r'(?<![a-z0-9])' + re.escape(ab.lower()) + r'(?![a-z0-9])', tl) and full not in tl: bad.append((s_['key'], ab, 'no full form'))
say('PASS' if not bad else 'FAIL', 'G2 every abbreviation of a list of %d is spelled out before its first use in the same item' % len(ABBRS), str(bad) if bad else '(list: %s)' % ', '.join(ABBRS))
others_ = {}
for i in items:
    tx = i.get('q', '') + ' ' + ' '.join(i.get('options', [])) + ' ' + ' '.join(p_['text'] for p_ in i.get('premises', [])) + ' ' + ' '.join(i.get('responses', [])) + ' ' + ' '.join(b_['text'] for b_ in i.get('blanks', [])) + ' ' + ' '.join(i.get('steps', []))
    for tok in re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,}[a-z]?|[A-Z][a-z]+[A-Z][A-Za-z]*)(?![A-Za-z0-9_])', tx):
        if tok not in ABBRS: others_.setdefault(tok, []).append(i['key'])
say('PASS', 'G2 other capital-letter tokens met in the printed text (listed for a human reader, not judged by the tool)', str({k: sorted(set(v)) for k, v in others_.items()}))

# ------------------------------------------------------------------ G3 tips
spec0 = importlib.util.spec_from_file_location('mtb12', BUILDER_PREV); mtb = importlib.util.module_from_spec(spec0); spec0.loader.exec_module(mtb); AUDIT = mtb.AUDIT
bad = []; unc = {}
for i in items:
    tx = ' \n '.join(strings_of(i)).lower()
    if i['type'] in ('ChoiceFour', 'ChoiceFourCode', 'NumericAnswer', 'CodeTrace'):
        if i['tips'] and 'tips:' not in i['q'].lower(): bad.append((i['key'], 'tips field not printed in the stem'))
        for t_ in i['tips']:
            if t_[0].lower() not in i['q'].lower() or t_[1].lower() not in i['q'].lower(): bad.append((i['key'], 'tip not in the stem: ' + t_[0]))
    else:
        for t_ in i['tips']:
            if t_[1].lower() not in tx and t_[0].lower() not in tx: bad.append((i['key'], 'tip not printed with the item: ' + t_[0]))
    if not i['tips'] and not all(AUDIT.get(k_, {}).get('verdict') == 'KEEP' for k_ in i.get('from_item', [])): bad.append((i['key'], 'no tips and the audit does not record a KEEP for the source item'))
    cov = ' '.join(t_[0].lower() + ' ' + t_[1].lower() for t_ in i['tips'])
    miss = [t for t in i['terms'] if t.lower() in tx and t.lower() not in cov and t.lower() not in ('fee', 'change', 'bit 31')]
    if miss: unc[i['key']] = miss
say('PASS' if not bad else 'FAIL', 'G3 every item with a stem prints its tips with the stem; every other item prints each tip with its sentences, steps, premises or bank entries; an item without tips is a recorded KEEP', str(bad) if bad else '(%d items, %d tips)' % (len(items), sum(len(i['tips']) for i in items)))
say('PASS', 'G3 MEASURED: course terms of the term lists that are printed in the item text but carry no tip of their own (a human reader judges them)', str(unc) if unc else '(none)')
nt_ = [i['key'] for i in items if not i['tips']]
say('PASS' if not nt_ else 'FAIL', 'G3 every item carries at least one tip', str(nt_))
bad = [s_['key'] for s_ in hand if not s_['tips']]
say('PASS' if not bad else 'FAIL', 'G3 every bonus prompt carries tips', str(bad))

# ------------------------------------------------------------------ G4 no recall wording
RECALL = re.compile(r"\b(what is the name|name the|what is it called|which term|what do we call|is called the|write the (word|term|name)|recall|from memory|define )", re.I)
bad = [i['key'] for i in items if RECALL.search(' \n '.join(strings_of(i)))] + [s_['key'] for s_ in hand if RECALL.search(s_['prompt'])]
say('PASS' if not bad else 'FAIL', 'G4 no item asks for a name, a term or a definition by wording (scan of the printed text for recall phrases; the judgement of the sense is the audit)', str(bad))
bad = [i['key'] for i in items if i['type'] == 'FillBlankGroup' and any(' (' not in a_ for a_ in [b_['answer'] for b_ in i['blanks']] + i['distractors'])]
say('PASS' if not bad else 'FAIL', 'G4 every bank entry carries its tip in brackets', str(bad))
bad = [i['key'] for i in items if not str(i.get('understanding', '')).split(':')[0] in ('use', 'importance', 'reason')]
say('PASS' if not bad else 'FAIL', 'G4 every item names what it asks about (use, importance or reason)', str(bad) if bad else str({i['key']: i['understanding'].split(':')[0] for i in items}))

# ------------------------------------------------------------------ M1 structure against items, and against the structure v1.0.0
bad = []
for k_, s_ in subs.items():
    it = by.get(s_['item'])
    if not it: bad.append((k_, 'item missing')); continue
    if s_['type'] != it['type']: bad.append((k_, 'type'))
    if s_['chapters'] != it['chapters'] or s_['bloom'] != it['bloom']: bad.append((k_, 'chapters or bloom'))
    if it['type'] == 'Ordering' and s_['parts'] != len(it['steps']): bad.append((k_, 'parts'))
    if it['type'] == 'Matching' and s_['parts'] != len(it['premises']): bad.append((k_, 'parts'))
nb = {i['key']: sum(1 for s_ in subs.values() if s_['item'] == i['key']) for i in items}
bad += [(i['key'], 'sub-questions %d, units %d' % (nb[i['key']], units(i))) for i in items if nb[i['key']] != units(i)]
for q in main_q:
    for s_ in q['sub']:
        if s_['type'] in ('Ordering', 'Matching') and abs(s_['points_per_part'] * s_['parts'] - s_['points']) > 1e-9: bad.append((s_['key'], 'points per part'))
say('PASS' if not bad else 'FAIL', 'M1 every sub-question of the structure v1.1.0 matches its item: type, chapters, Bloom level, parts, one sub-question per unit, points per part', str(bad) if bad else '(%d sub-questions)' % len(subs))
old = {s_['key']: s_ for q in s10['questions'] if not q.get('bonus') for s_ in q['sub']}
bad = [(k_, old[k_]['block'], subs[k_]['block']) for k_ in old if k_ in subs and old[k_]['block'] != subs[k_]['block']]
say('PASS' if not bad and sorted(old) == sorted(subs) else 'FAIL', 'M1 (task item 4) the answer-block type of EVERY position equals the structure v1.0.0, so the answer sheet needs no change', '(%d positions compared, keys equal: %s, differing: %s)' % (len(old), sorted(old) == sorted(subs), bad))
oldq = {q['number']: q['answer_block'] for q in s10['questions']}; newq = {q['number']: q['answer_block'] for q in Qs}
say('PASS' if oldq == newq else 'FAIL', 'M1 the answer block of every question equals the structure v1.0.0', str(newq))
bad = [(k_, 'units/points/parts') for k_ in old if k_ in subs and (old[k_]['units'] != subs[k_]['units'] or old[k_]['points'] != subs[k_]['points'] or old[k_].get('parts') != subs[k_].get('parts'))]
say('PASS' if not bad else 'FAIL', 'M1 units, points and parts of every position equal the structure v1.0.0 (the sheet rows are unchanged)', str(bad))
bad = [(k_, 'type') for k_ in old if k_ in subs and old[k_]['type'] != subs[k_]['type']]
say('PASS', 'M1 MEASURED (not a pass condition): positions whose item TYPE differs from structure v1.0.0 while the block is equal (the paper lib prints by type; the sheet by block)', str(bad))
say('PASS' if os.path.exists(os.path.join(HERE, st['items_file'])) and os.path.samefile(os.path.join(HERE, st['items_file']), ITEMS_FILE) else 'FAIL', 'M1 items_file of the structure names the items file correctly and resolves from the exam folder', st['items_file'])
say('PASS' if st['version'] == '1.1.0' and st['chapters'] == [1, 2, 3, 4, 5, 6] and doc['version'] == '1.4.0' else 'FAIL', 'M1 versions: structure 1.1.0, items 1.4.0, chapters 1 to 6')

# ------------------------------------------------------------------ M2 chapter weights
anyc = {c: sum(units(i) for i in items if c in i['chapters']) for c in range(1, 7)}
say('PASS' if all(v == 4 for v in per.values()) and all(v >= 2 for v in per.values()) and all(v >= 2 for v in anyc.values()) else 'FAIL', 'M2 equal chapter weights (4 machine-read units per chapter by primary chapter) and at least two units per chapter', 'primary %s ; any named chapter %s' % (per, anyc))

# ------------------------------------------------------------------ M3 Bloom
lv = {t: 0 for t in range(1, 7)}
for i in items: lv[i['bloom']] += units(i)
say('PASS', 'M3 units per Bloom level 1 to 6', str(lv))
say('PASS' if ge4 >= 6 else 'FAIL', 'M3 units at Analyze or above (minimum 6, rule not relaxed; the task expected exactly 6 with two numeric items at Bloom 3)', '(%d; levels recorded in structure v1.1.0: %s)' % (ge4, sorted({(s_['key'], s_['bloom']) for s_ in subs.values() if s_['bloom'] >= 4})))

# ------------------------------------------------------------------ M4 option lengths
bad = []; ranks = {}
for i in items:
    if i['type'] in ('ChoiceFour', 'ChoiceFourCode'):
        L = [len(o) for o in i['options']]; a_ = i['answer']; wr = [l for n, l in enumerate(L) if n != a_]; mw = sum(wr) / 3.0
        rank = sorted(L, reverse=True).index(L[a_]) + 1; ranks[i['key']] = rank
        if not (min(L) < L[a_] < max(L)): bad.append((i['key'], 'correct option is the longest or the shortest'))
        if abs(L[a_] - mw) > 0.06 * mw: bad.append((i['key'], 'correct option %.1f percent from the mean of the others' % (100 * (L[a_] - mw) / mw)))
        if (max(L) - min(L)) > 0.20 * min(L): bad.append((i['key'], 'spread %.0f percent' % (100.0 * (max(L) - min(L)) / min(L))))
    if i['type'] == 'Matching':
        used_ = {p['match'] for p in i['premises']}
        u = [len(r) for r in i['responses'] if r in used_]; n = [len(r) for r in i['responses'] if r not in used_]
        mu, mn = sum(u) / len(u), sum(n) / len(n)
        if abs(mn - mu) > 0.10 * mu: bad.append((i['key'], 'unused responses %.1f percent from the used ones' % (100 * (mn - mu) / mu)))
        if min(n) < 0.85 * min(u) or max(n) > 1.15 * max(u): bad.append((i['key'], 'an unused response lies outside the length range of the used ones'))
        a_, b_ = [len(p['text']) for p in i['premises']], [len(p['match']) for p in i['premises']]
        ma, mb = sum(a_) / 4.0, sum(b_) / 4.0
        den = math.sqrt(sum((x - ma) ** 2 for x in a_) * sum((y - mb) ** 2 for y in b_))
        if den and sum((x - ma) * (y - mb) for x, y in zip(a_, b_)) / den > 0.9: bad.append((i['key'], 'premise length and matched response length are strongly correlated'))
say('PASS' if not bad else 'FAIL', 'M4 option lengths (the addendum\'s finding: in 4 of 7 items of part A the correct option was the longest): no ChoiceFour or Matching item is recognisable by length', str(bad) if bad else '(%d choice items, ranks of the correct option by length (1 = longest): %s)' % (len(ranks), sorted(ranks.values())))
say('PASS' if len(set(ranks.values())) >= 2 and 1 not in ranks.values() and 4 not in ranks.values() else 'FAIL', 'M4 the rank of the correct option by length is not constant and never extreme', str(sorted(ranks.values())))
ban = []
for i in items:
    if i['type'] == 'FillBlankGroup':
        a_ = [len(b_['answer']) for b_ in i['blanks']]; d_ = [len(x) for x in i['distractors']]
        ban.append((i['key'].split(':')[1], a_, d_))
say('PASS', 'M4 MEASURED (not a pass condition; the task names ChoiceFour and Matching): fill-in bank entry lengths, answers against distractors', str(ban))

# ------------------------------------------------------------------ M5 Q3.a
q3a = subs['Q3.a']
say('PASS' if q3a['instruction'] == by[q3a['item']]['instruction'] and 'transaction' in q3a['instruction'].lower() and 'steps of one payment' not in q3a['instruction'] else 'FAIL',
    'M5 the Q3.a instruction printed by the structure is the instruction written in the item (it orders five transactions, not five steps of one payment)', '(old wording kept as instruction_old_v1_0_0: %s)' % bool(q3a.get('instruction_old_v1_0_0')))
say('PASS' if 'Partial credit is a rule for the owner to fix (open question P1): the points of a part divide equally over its steps or pairs.' in [q for q in Qs if q['number'] == 3][0]['instruction'] else 'FAIL', 'M5 the Q3 instruction still holds the sentence that the paper library replaces when it prints (so the library accepts it)')

# ------------------------------------------------------------------ M6 provisional
prov = {i['key']: i.get('provisional_reason', '') for i in items if i.get('provisional')}; provb = {s_['item']: s_.get('provisional_reason', '') for s_ in hand if s_.get('provisional')}
need = {'mt3:a5:old-notes-and-new-keys', 'mt3:i07:fill-mined-or-not', 'mt3:i15:fill-locking-unlocking'}
say('PASS' if set(prov) == need and all(len(r) > 80 for r in prov.values()) and set(provb) == {'mt3:b2:mining-pace'} and all(len(r) > 80 for r in provb.values()) else 'FAIL',
    'M6 provisional:true with a reason on exactly the items whose reading is the author\'s (L old currencies, C2 and T7 timing, N scripts) and on bonus Q5.b (part 3, point F)', '(items %s ; bonus %s)' % (sorted(prov), sorted(provb)))
say('PASS' if 'T7' in prov.get('mt3:i07:fill-mined-or-not', '') and 'C2' in prov.get('mt3:i07:fill-mined-or-not', '') and 'point L' in prov['mt3:a5:old-notes-and-new-keys'] and 'Point N' in prov['mt3:i15:fill-locking-unlocking'] else 'FAIL', 'M6 the reasons name T7, C2, L and N')

# ------------------------------------------------------------------ M7 critical points
def holders(its, bon):
    h = {}
    for i in its:
        for c in i['critical_points']: h.setdefault(c, set()).add(i['key'])
    for s_ in bon:
        for c in s_['critical_points']: h.setdefault(c, set()).add(s_['item'])
    return h
bonus_old = [s_ for q in s10['questions'] if q.get('bonus') for s_ in q['sub']]
before = holders(v13, bonus_old); after = holders(items, hand)
lost = sorted(c for c in before if c not in after); gained = sorted(c for c in after if c not in before)
print('NOTE         critical points of items v1.3.0 (with its bonus) that lost their only holder in v1.4.0, by name:')
for c in lost: print('NOTE           %s (chapter %d): %s | held before by %s' % (c, cp[c]['chapter'], cp[c]['point'][:110], sorted(k.split(':')[1] for k in before[c])))
say('PASS', 'M7 critical points held before (v1.3.0 and its bonus), held now, lost, gained (chapters 1 to 6)', '%d held before, %d held now, %d lost, %d gained' % (len(before), len(after), len(lost), len(gained)))
say('PASS', 'M7 lost (named above)', str(lost)); say('PASS', 'M7 gained', str(gained))
by_ch = {c: (len([x for x in before if cp[x]['chapter'] == c]), len([x for x in after if cp[x]['chapter'] == c])) for c in range(1, 7)}
say('PASS', 'M7 critical points per chapter (before, after)', str(by_ch))
parts_items = []
for pth in PARTS:
    if os.path.exists(pth): parts_items += json.load(open(pth, encoding='utf8'))['items']
if len(parts_items) == 21:
    ph = holders(parts_items, hand)
    partlost = sorted(c for c in before if c not in ph)
    say('PASS', 'M7 the three parts together (before the two replacements) lost', '%d points: %s' % (len(partlost), partlost))
    say('PASS', 'M7 recovered by the two replacements from items v1.3.0 (release tags, gap limit)', str(sorted(c for c in partlost if c in after)))
    say('PASS', 'M7 recovered by a truthful new link (the item asks it)', str(sorted(set(after) - set(ph) - set(c for c in partlost if c in after))))
    print('NOTE         the drops and their cost, computed over the 21 part items and the bonus: sole-held critical points of each single-unit item of chapters 2 and 6 (the candidates for the balance), and the owner points they alone hold')
    solo = {}
    for i in parts_items:
        solo[i['key']] = (sorted(c for c in i['critical_points'] if ph[c] == {i['key']}), i.get('owner_points'))
    for i in parts_items:
        if i['type'] != 'FillBlankGroup' and i['chapters'][0] in (2, 6):
            print('NOTE           %-45s chapter %d sole-held points %s ; owner points %s' % (i['key'], i['chapters'][0], solo[i['key']][0], solo[i['key']][1]))
else:
    say('NOT_MEASURED', 'M7 part files not found in private/ (21 items expected)', str(len(parts_items)))

# ------------------------------------------------------------------ M8 critical-points tool
r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'sen0401_exam_critical_points_check_v1_0_0.py')], capture_output=True, text=True)
last = [l for l in r.stdout.splitlines() if l.startswith('RESULT')]
print('--- critical points tool (sen0401_exam_critical_points_check_v1_0_0.py), exit %d, printed as it is:' % r.returncode)
print(r.stdout.rstrip())
say('PASS' if r.returncode == 0 and last and 'PASS' in last[0] else 'FAIL', 'M8 the critical-points tool passes (exit code 0)', last[0] if last else r.stderr[:200])

# ------------------------------------------------------------------ M9 topic map
tfs = sorted(glob.glob(os.path.join(HERE, 'sen0401_exam_owner_topics_v*.json')), key=lambda p: tuple(int(x) for x in re.search(r'_v(\d+)_(\d+)_(\d+)\.json$', p).groups()))
newest = tfs[-1]; T = json.load(open(newest, encoding='utf8'))
ids = [c['id'] for c in T['cases']] + [t['id'] for t in T['topics']] + [p['id'] for p in T['points']] + [p['id'] for p in T['points2']]
if os.path.exists(MAP_FILE):
    M = json.load(open(MAP_FILE, encoding='utf8')); rows = {r_['id']: r_ for r_ in M['rows']}
    keys_ok = all(x['item'] in by or x['item'] in {s_['item'] for s_ in hand} for r_ in M['rows'] for x in r_['items'])
    say('PASS' if M['owner_topics_file'] == os.path.basename(newest) and sorted(rows) == sorted(ids) and keys_ok and all(r_['items'] for r_ in M['rows']) else 'FAIL',
        'M9 the topic map was made from the NEWEST owner topics file (%s) and holds all %d points (C1-C3, T1-T9, A-F, G-P), each with item keys that resolve' % (os.path.basename(newest), len(ids)), '(files found: %s)' % [os.path.basename(x) for x in tfs])
    bad = [r_['id'] for r_ in M['rows'] if r_['status'] not in ('COVERED', 'PARTIAL', 'GAP') or r_['disposition'] not in ('BUILT', 'COVERED', 'DECLINED') or (r_['status'] != 'COVERED' and not r_['not_asked'])]
    say('PASS' if not bad else 'FAIL', 'M9 every point has a status (COVERED, PARTIAL, GAP) and a disposition (BUILT, COVERED, DECLINED); every point that is not fully covered says what is not asked', str(bad))
    say('PASS', 'M9 summary printed as it is', str(M['summary']))
    say('PASS' if sorted(x['item'] for x in M['provisional_items']) == sorted(list(prov) + list(provb)) else 'FAIL', 'M9 the map lists the provisional items exactly as the items and the structure mark them', str(sorted(x['item'] for x in M['provisional_items'])))
    with tempfile.TemporaryDirectory(dir=PRIV) as td:
        r2 = subprocess.run([sys.executable, '-I', BUILD_MAP, '--outdir', td], capture_output=True, text=True, cwd=PRIV)
        same = r2.returncode == 0 and json.load(open(os.path.join(td, 'sen0401_exam_topic_map_v1_4_0.json'), encoding='utf8')) == M
        say('PASS' if same else 'FAIL', 'M9 the map builder, run again, writes the same map', '(exit %d)' % r2.returncode)
else:
    say('NOT_MEASURED', 'M9 the topic map file does not exist', MAP_FILE)

# ------------------------------------------------------------------ M10 the paper library accepts structure and items
try:
    import sen0401_exam_paper_lib_v3_0_0 as PL
    pf = PL.make_form(1, structure=PL.load_structure(STRUCT_FILE))
    say('PASS' if len(pf['slots']) == 23 and len(pf['items']) == 21 and all(pf['quotas'][c] == 4 for c in range(1, 7)) else 'FAIL', 'M10 the paper library v3.0.0 makes form 1 from structure v1.1.0 and items v1.4.0 (slots, items, quotas)', '(slots %d, items %d, quotas %s)' % (len(pf['slots']), len(pf['items']), pf['quotas']))
except Exception as e:
    say('FAIL', 'M10 the paper library v3.0.0 refused the structure or the items', repr(e)[:300])

print('\nRESULT', 'FAIL (%s)' % '; '.join(fails) if fails else 'PASS')
sys.exit(1 if fails else 0)
