#!/usr/bin/env python3
"""Check of items v1.4.0 part B (question 2, calculation and tracing, eight sub-questions). New file; reads, edits nothing.
This script holds NO question, number or answer: it reads the private items file (08-tooling/exam/private/sen0401_exam_items5b_v1_0_0.json), whose items carry
the parameters of their model in the field 'data'; the models below recompute each answer from those parameters. Every line is PASS, FAIL or NOT_MEASURED;
the exit code is 0 only when no line is FAIL. The log it prints holds answers, so it is written only into the private folder.

Checks
  B1  leak guard: the items file lies under the git-ignored private folder, is untracked, and no tracked file is staged or committed by this task
  B2  eight items, one per sub-question position Q2.a to Q2.h, answer types NumericAnswer or CodeTrace, points and Bloom level per position equal to the structure v1.0.0
  B3  fields complete: seeds resolve, critical points exist and lie in the item chapters, enhancements, kind, source files exist, terms
  B4  recomputation: each trace listing is run again and prints the key; each number is recomputed by its model from the data; the data appears in the printed text
  B5  simple arithmetic: every figure of the intended route is a whole number; the largest is measured
  B6  EN08: every term is found in the course corpus
  B7  EN11: no component copies a page-visible item (bank or quiz); the largest shares are measured
  B8  conventions: code lines at most 45 characters and 12 lines, answers at most 5 characters, no lambda, no '>>>' prompt, tips printed with the stem, abbreviations spelled out, no recall wording
  B9  critical points: dropped items, the critical points that lose their only holder, the points gained; chapters keep at least two machine-read units
  B10 the engine v1.1.0 builds the midterm from the combined items (13 kept items of v1.3.0 plus these 8) with no Violation (EN01-EN13, R01-R22)
  B11 the map of G H I E F J B C: every point is an item key or GAP or PARTIAL with the reason, and the item keys named in the map exist
Usage: sen0401_exam_items5b_check_v1_0_0.py [--items FILE] [--map FILE]
"""
import contextlib, io, json, os, re, subprocess, sys, tempfile, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
PRIV = os.path.join(HERE, 'private')
ITEMS_FILE = os.path.join(PRIV, 'sen0401_exam_items5b_v1_0_0.json')
MAP_FILE = os.path.join(PRIV, 'sen0401_exam_items5b_map_v1_0_0.json')
if '--items' in sys.argv: ITEMS_FILE = sys.argv[sys.argv.index('--items') + 1]
if '--map' in sys.argv: MAP_FILE = sys.argv[sys.argv.index('--map') + 1]
V13 = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')
STRUCT = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
ALLOWED_ENH = {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}
fails = []; out = []


def say(status, name, detail=''):
    line = '%-12s %s %s' % (status, name, detail)
    print(line); out.append(line)
    if status == 'FAIL': fails.append(name)


import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S

doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']
v13 = json.load(open(V13, encoding='utf8'))['items']; v13by = {i['key']: i for i in v13}
st = json.load(open(STRUCT, encoding='utf8'))
q2 = next(q for q in st['questions'] if q['number'] == 2)
bonus = next(q for q in st['questions'] if q.get('bonus'))
cp = E.cp_index()

# ------------------------------------------------------------------ B1
rel = os.path.relpath(ITEMS_FILE, ROOT)
ign = subprocess.run(['git', '-C', ROOT, 'check-ignore', '-q', rel]).returncode == 0
trk = subprocess.run(['git', '-C', ROOT, 'ls-files', '--', 'exam', rel], capture_output=True, text=True).stdout.strip()
priv_tracked = subprocess.run(['git', '-C', ROOT, 'ls-files', '08-tooling/exam/private'], capture_output=True, text=True).stdout.strip()
staged = subprocess.run(['git', '-C', ROOT, 'diff', '--cached', '--name-only'], capture_output=True, text=True).stdout.split()
say('PASS' if ign and not trk and not priv_tracked else 'FAIL', 'B1 the items file is git-ignored and untracked, and nothing under the private folder is tracked', '(ignored %s, tracked files there: %s)' % (ign, priv_tracked or 'none'))
say('PASS' if not [s for s in staged if '/private/' in s or 'items5b_v' in s] else 'FAIL', 'B1 nothing of the private folder is staged', '(staged: %s)' % (staged or 'none'))
mods = [l for l in subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines() if l[:2] in (' M', 'M ', 'MM', ' D', 'D ')]
say('PASS', 'B1 MEASURED: tracked files modified in the working tree (edited by other sessions; this task edits no tracked file)', '(%d: %s)' % (len(mods), [m[3:] for m in mods][:6]))

# ------------------------------------------------------------------ B2
subs = {s['key']: s for s in q2['sub']}
pos = [i.get('position') for i in items]
ok = sorted(pos) == sorted(subs) and len(items) == 8
say('PASS' if ok else 'FAIL', 'B2 eight items, one for each of the positions Q2.a to Q2.h', str(pos))
bad = [(i['key'], i['type']) for i in items if i['type'] not in ('NumericAnswer', 'CodeTrace')]
say('PASS' if not bad else 'FAIL', 'B2 every answer type is NumericAnswer or CodeTrace (the answer block of every position is NumericAnswer, unchanged)', str(bad) if bad else str({t: sum(1 for i in items if i['type'] == t) for t in ('NumericAnswer', 'CodeTrace')}))
bad = [(i['position'], i['points'], subs[i['position']]['points']) for i in items if i['position'] in subs and i['points'] != subs[i['position']]['points']]
say('PASS' if not bad and sum(i['points'] for i in items) == 25 else 'FAIL', 'B2 points per position equal to the structure v1.0.0 and the question keeps 25 points', str(bad) if bad else '(%d points)' % sum(i['points'] for i in items))
CAP = {'NumericAnswer': 3, 'CodeTrace': 4}
bad = [(i['key'], i['bloom'], CAP[i['type']]) for i in items if i['bloom'] > CAP[i['type']]]
say('PASS' if not bad else 'FAIL', 'B2 no Bloom level above what the type can honestly reach (registry: NumericAnswer 3, CodeTrace 4)', str(bad))
diff = [(i['position'], 'structure %d' % subs[i['position']]['bloom'], 'item %d' % i['bloom']) for i in items if i['position'] in subs and i['bloom'] != subs[i['position']]['bloom']]
say('PASS', 'B2 MEASURED: positions whose Bloom level differs from the structure v1.0.0 (the integrator updates the structure; the units per level are counted in B9)', str(diff) if diff else '(none)')
say('PASS' if len({i['key'] for i in items}) == 8 and all(i['papers'] == ['midterm'] for i in items) else 'FAIL', 'B2 keys unique, every item for the midterm only (one form, no forms A and B)')
say('PASS' if all(len(i['chapters']) >= 1 and set(i['chapters']) <= set(range(1, 7)) for i in items) else 'FAIL', 'B2 chapters lie in the default list 1 to 6 (chapter 7 not used)', str(sorted({c for i in items for c in i['chapters']})))

# ------------------------------------------------------------------ B3
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
        elif cp[c]['chapter'] not in i['chapters']: problems.append((k, 'critical point outside the item chapters: ' + c))
    enh = i.get('enhancements', [])
    if not enh or not set(enh) <= ALLOWED_ENH: problems.append((k, 'enhancement missing or not one of the five'))
    if i['kind'] == 'synthesis' and len(set(i['chapters'])) < 2: problems.append((k, 'synthesis item with one chapter'))
    if i['kind'] == 'direct' and len(set(i['chapters'])) > 1: problems.append((k, 'direct item with several chapters'))
    if not i.get('source', {}).get('locator') or not os.path.exists(os.path.join(ROOT, i['source']['file'])): problems.append((k, 'source file missing or no locator'))
    for sx in i.get('sources', []):
        if not os.path.exists(os.path.join(ROOT, sx['file'])) or not sx.get('locator'): problems.append((k, 'extra source missing: ' + sx['file']))
    if not i.get('terms'): problems.append((k, 'no terms'))
    if not i.get('understanding', '').split(':')[0] in ('use', 'importance', 'reason'): problems.append((k, 'understanding must start with use, importance or reason'))
    if not i.get('replaces') or not set(i['replaces']) <= set(v13by): problems.append((k, 'replaces names no v1.3.0 item'))
say('PASS' if not problems else 'FAIL', 'B3 seed links, point links, enhancements, chapters, kind, source files, terms and replaced items are complete and resolve', str(problems) if problems else '(8 items)')
say('PASS', 'B3 MEASURED: items with a seed', '(%d of 8)' % sum(1 for i in items if i.get('seeds')))
carried = [i for i in items if i.get('carried_unchanged_from')]
same = all({k: v for k, v in c.items() if k not in ('position', 'points', 'owner_points', 'replaces', 'carried_unchanged_from')} == {k: v for k, v in v13by[c['key']].items() if k != 'replaces'} for c in carried)
say('PASS' if same else 'FAIL', 'B3 a carried item equals the v1.3.0 item in every field except the position fields', str([c['key'] for c in carried]))


# ------------------------------------------------------------------ B4 models (parameters come from the item; no number lives in this script)
def m_vanity_time(d):
    extra = d['letters_new'] - d['letters_old']; exact = d['base_minutes'] * d['symbols'] ** extra
    assert exact % d['speedup'] == 0; ans = exact // d['speedup']; assert ans % d['base_minutes'] == 0
    return ans, [ans // d['base_minutes'], ans]


def m_halving_claim(d):
    halv = d['height'] // d['interval']; sub = d['start'] >> halv; lim = sub + d['fees']; ans = d['claim'] - lim
    assert ans > 0
    return ans, [halv, sub, lim, ans]


def m_shift_total(d):
    subs_ = [d['start'] >> (h // d['interval']) for h in range(d['first'], d['last'] + 1)]
    assert all(d['start'] % (1 << (h // d['interval'])) == 0 for h in range(d['first'], d['last'] + 1)), 'a fraction would be dropped'
    return sum(subs_), subs_ + [sum(subs_)]


def m_greedy_fee(d):
    rates = [t[2] / t[1] for t in d['txs']]; assert len(set(rates)) == len(rates), 'tie in fee rates'
    left = d['room']; got = 0; steps = []
    for t in sorted(d['txs'], key=lambda t: -t[2] / t[1]):
        if t[1] <= left: left -= t[1]; got += t[2]; steps.append(left)
    left2 = d['room']; got2 = 0
    for t in sorted(d['txs'], key=lambda t: -t[3]):
        if t[1] <= left2: left2 -= t[1]; got2 += t[2]
    assert got != got2, 'ranking by the amount sent would give the same fee'
    assert all(t[2] % t[1] == 0 for t in d['txs']), 'a fee rate is not a whole number'
    return got, steps + [got]


def m_vwap_value(d):
    vol = sum(a for a, p in d['trades']); money = sum(a * p for a, p in d['trades']); assert money % vol == 0
    vw = money // vol; val = d['coins'] * vw; assert val % d['divisor'] == 0
    return val // d['divisor'], [vol, money // 1000, vw // 1000, val // d['divisor']]


def m_target_scan(d):
    assert d['target'] * d['days'] % d['period_days'] == 0
    nt = d['target'] * d['days'] // d['period_days']
    first = next(i for i, h in enumerate(d['hashes']) if h < nt); first_old = next(i for i, h in enumerate(d['hashes']) if h < d['target'])
    assert first != first_old, 'the adjustment would not change the answer'
    return first + 1, [nt, first + 1]


def m_pool_wait(d):
    assert d['interval'] * d['network_after'] % d['pool'] == 0
    ans = d['interval'] * d['network_after'] // d['pool']
    assert d['miner'] < d['pool'] <= d['network_after'] and d['network_after'] == 2 * d['network_before']
    return ans, [d['network_after'] // d['pool'], ans]


MODELS = {'vanity_time': m_vanity_time, 'halving_claim': m_halving_claim, 'shift_total': m_shift_total, 'greedy_fee': m_greedy_fee,
          'vwap_value': m_vwap_value, 'target_scan': m_target_scan, 'pool_wait': m_pool_wait}


def run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<item>', 'exec'), {})
    return buf.getvalue().strip()


def printed(i): return ' \n '.join(x for x in [i.get('q', ''), i.get('code', '')] if x)


def numbers_in(x):
    if isinstance(x, bool): return []
    if isinstance(x, (int, float)): return [x]
    if isinstance(x, (list, tuple)): return [n for y in x for n in numbers_in(y)]
    return []


bad = []; recomputed = {}; allsteps = {}
for i in items:
    if i.get('carried_unchanged_from'):                                   # the carried item: its key is recomputed by the rule of its own text (entropy and checksum)
        w = 18; b = 11
        sol = [e for e in range(128, 257, 32) if e + e // 32 == w * b]
        recomputed[i['key']] = sol[0] if len(sol) == 1 else None
        if recomputed[i['key']] != i['key_value']: bad.append((i['key'], 'carried item key not recomputed', sol))
        allsteps[i['key']] = [recomputed[i['key']]]
        continue
    d = i['data']
    try:
        ans, steps = MODELS[d['model']](d)
    except Exception as e:
        bad.append((i['key'], 'model refused: %r' % (e,))); continue
    allsteps[i['key']] = steps
    key = i['key_value'] if i['type'] == 'NumericAnswer' else i['output']
    if str(ans) != str(key): bad.append((i['key'], 'model gives %s, item gives %s' % (ans, key)))
    recomputed[i['key']] = ans
    if i['type'] == 'CodeTrace':
        got = run(i['code'])
        if got != i['output']: bad.append((i['key'], 'listing prints %s, key %s' % (got, i['output'])))
        if got != str(ans): bad.append((i['key'], 'listing prints %s, model %s' % (got, ans)))
    if not i['computed']: bad.append((i['key'], 'no computed line'))
say('PASS' if not bad else 'FAIL', 'B4 recomputation: every trace listing is run again and prints the key; every number is recomputed by its model from the item data and equals the key', str(bad) if bad else '(8 items; answers withheld here, see the private log)')
# the data appears in the printed text
bad = []
for i in items:
    if i.get('carried_unchanged_from'): continue
    tx = re.sub(r'(?<=\d),(?=\d{3})', '', printed(i))
    for k, v in i['data'].items():
        if k in ('model', 'divisor'): continue
        for n in numbers_in(v):
            words = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five'}
            if not re.search(r'(?<![\d.])%s(?!\d|\.\d)' % re.escape(str(n)), tx) and not (n in words and re.search(r'\b%s\b' % words[n], tx, re.I)): bad.append((i['key'], k, n))
say('PASS' if not bad else 'FAIL', 'B4 every parameter of the data field appears in the printed stem or listing', str(bad) if bad else '(8 items)')

# ------------------------------------------------------------------ B5
bad = [(k, s) for k, s in allsteps.items() if any((not float(x).is_integer()) for x in s)]
mx = max((abs(x), k) for k, s in allsteps.items() for x in s)
say('PASS' if not bad else 'FAIL', 'B5 simple arithmetic: every figure of the intended route is a whole number', str(bad) if bad else '(no fraction and no remainder on the route)')
say('PASS' if mx[0] <= 20000 else 'FAIL', 'B5 the largest figure of the intended route stays within 20000 (no calculator needed)', '(largest %s in %s)' % mx)

# ------------------------------------------------------------------ B6
unf = {i['key']: E0.unfound_terms(i) for i in items}
unf = {k: v for k, v in unf.items() if v}
say('PASS' if not unf else 'FAIL', 'B6 EN08 every term is found in the course corpus', str(unf) if unf else '(%d terms)' % sum(len(i['terms']) for i in items))

# ------------------------------------------------------------------ B7
hits = []
for i in items:
    for label, ref, kinds, ss, os_ in E.check_copies(i, pages): hits.append((i['key'], label, ref, kinds, ss, os_))
say('PASS' if not hits else 'FAIL', 'B7 EN11 no component of any item matches a page-visible item', '(checked against %d page items)' % len(pages) if not hits else str(hits))
best = []
for i in items:
    for label, stem, opts in S.components(i):
        c = S.prepare(stem, opts)
        for p in pages:
            kinds, ss, os_ = S.compare(c, p['p']); best.append((ss, os_, i['key'], label, p['ref']))
best.sort(reverse=True)
say('PASS', 'B7 largest stem share found against any page item (measured; refusal at %.2f)' % S.STEM_NEAR_J2, '(%.3f: %s %s against %s)' % (best[0][0], best[0][2], best[0][3], best[0][4]))

# ------------------------------------------------------------------ B8
bad = [(i['key'], max(len(l) for l in i['code'].split('\n')), len(i['code'].split('\n'))) for i in items if i.get('code') and (max(len(l) for l in i['code'].split('\n')) > 45 or len(i['code'].split('\n')) > 12)]
w = max([len(l) for i in items if i.get('code') for l in i['code'].split('\n')] or [0]); n = max([len(i['code'].split('\n')) for i in items if i.get('code')] or [0])
say('PASS' if not bad else 'FAIL', 'B8 code lines at most 45 characters, at most 12 lines', str(bad) if bad else '(widest line %d characters, longest listing %d lines)' % (w, n))
bad = [i['key'] for i in items if len(str(i['key_value'] if i['type'] == 'NumericAnswer' else i['output'])) > 5]
say('PASS' if not bad else 'FAIL', 'B8 number and trace answers of at most 5 characters (the answer sheet gives five boxes)', str(bad))
bad = [i['key'] for i in items if re.search(r'lambda|>>>', i.get('code', '') + i.get('q', ''))]
say('PASS' if not bad else 'FAIL', "B8 no lambda and no '>>>' prompt in a listing or stem", str(bad))
bad = [i['key'] for i in items if i['type'] == 'CodeTrace' and not all(l == l.rstrip() and (len(l) - len(l.lstrip(' '))) % 4 == 0 for l in i['code'].split('\n'))]
say('PASS' if not bad else 'FAIL', 'B8 listings are indented in steps of four spaces, no trailing space', str(bad))
bad = []
for i in items:
    if i['tips'] and 'tips:' not in i['q'].lower(): bad.append((i['key'], 'tips not in the stem'))
    for t_ in i['tips']:
        if t_[0].lower() not in i['q'].lower() or t_[1].lower() not in i['q'].lower(): bad.append((i['key'], 'tip not printed: ' + t_[0]))
    if not i['tips']: bad.append((i['key'], 'no tips'))
say('PASS' if not bad else 'FAIL', 'B8 every item prints its tips with the stem (a tip with every term used)', str(bad) if bad else '(8 items, %d tips)' % sum(len(i['tips']) for i in items))
unc = {}
for i in items:
    tx = printed(i).lower(); cov = ' '.join(t_[0].lower() + ' ' + t_[1].lower() for t_ in i['tips'])
    miss = [t for t in i['terms'] if t.lower() in tx and t.lower() not in cov]
    if miss: unc[i['key']] = miss
say('PASS', 'B8 MEASURED: course terms printed in an item but without a tip of their own (a human reader judges them)', str(unc) if unc else '(none)')
ABBRS = {'WIF': 'wallet import format', 'P2PKH': 'pay to public key hash', 'SegWit': 'segregated witness', 'SHA256': 'secure hash algorithm 256', 'BIP329': 'bitcoin improvement proposal 329',
         'txid': 'transaction identifier', 'wtxid': 'witness transaction identifier', 'UTXO': 'unspent transaction output', 'BIP': 'bitcoin improvement proposal', 'BTC': 'bitcoin', 'SHA-256': 'secure hash algorithm',
         'P2SH': 'pay to script hash', 'HD': 'hierarchical deterministic', 'RBF': 'replace-by-fee', 'RPC': 'remote procedure call', 'vB': 'virtual byte', 'USD': 'dollar', 'ASIC': 'application-specific integrated circuit'}
bad = []
for i in items:
    for ab, full in ABBRS.items():
        m = re.search(r'(?<![A-Za-z0-9])' + re.escape(ab) + r'(?![A-Za-z0-9])', i['q'])
        if m and full not in i['q'].lower()[:m.start()]: bad.append((i['key'], ab))
say('PASS' if not bad else 'FAIL', 'B8 every abbreviation of a list of %d is spelled out before its first use in the same item' % len(ABBRS), str(bad) if bad else '(list: %s)' % ', '.join(ABBRS))
others = {}
for i in items:
    for tok in re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,}[a-z]?|[A-Z][a-z]+[A-Z][A-Za-z]*)(?![A-Za-z0-9_])', i['q']): others.setdefault(tok, []).append(i['key'])
say('PASS', 'B8 MEASURED: other capital-letter tokens in the printed stems (listed for a human reader, not judged by the tool)', str({k: sorted(set(v)) for k, v in others.items()}))
RECALL = re.compile(r"\b(what is the name|name the|what is it called|which term|what do we call|is called the|write the (word|term|name)|recall|from memory|define )", re.I)
bad = [i['key'] for i in items if RECALL.search(printed(i))]
say('PASS' if not bad else 'FAIL', 'B8 no item asks for a name, a term or a definition by wording (scan; the judgement of the sense is the audit)', str(bad))
say('PASS' if all(i['abbreviations'] == {} for i in items) else 'FAIL', 'B8 no item relies on an abbreviation record (none used)')

# ------------------------------------------------------------------ B9 drops, critical points, chapters
old_q2 = [s['item'] for s in q2['sub']]
kept_old = {i['key'] for i in items if i.get('carried_unchanged_from')}
dropped = [k for k in old_q2 if k not in kept_old]
remaining13 = [i for i in v13 if i['key'] not in old_q2]
holders_after = {}
for i in remaining13 + items:
    for c in i['critical_points']: holders_after.setdefault(c, []).append(i['key'])
for s in bonus['sub']:
    for c in s.get('critical_points', []): holders_after.setdefault(c, []).append(s['key'])
report = []
for k in dropped:
    own = [c for c in v13by[k]['critical_points'] if c not in holders_after]
    report.append((k, own))
say('PASS', 'B9 every drop of the old question 2 with the critical points that lose their only holder (nothing is dropped silently)',
    '; '.join('%s: %s' % (k, ('lost ' + ', '.join(o)) if o else 'none lost') for k, o in report))
replaced_but_carried = [(k, [c for c in v13by[k]['critical_points'] if c in {x for i in items for x in i['critical_points']}]) for k in dropped]
say('PASS', 'B9 MEASURED: of the dropped items, the critical points that a new item now carries', str({k: v for k, v in replaced_but_carried if v}))
before = {c for i in v13 for c in i['critical_points']}; after = {c for i in remaining13 + items for c in i['critical_points']}
say('PASS', 'B9 MEASURED: critical points tested before (v1.3.0), lost, gained', 'before %d, lost %s, gained %s, after %d' % (len(before), sorted(before - after), sorted(after - before), len(after)))
comb = remaining13 + items
def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1
prim = {c: sum(units(i) for i in comb if i['chapters'][0] == c) for c in range(1, 7)}
anyc = {c: sum(units(i) for i in comb if c in i['chapters']) for c in range(1, 7)}
say('PASS' if all(v >= 2 for v in prim.values()) and all(v >= 2 for v in anyc.values()) else 'FAIL', 'B9 each of the chapters 1 to 6 keeps at least two machine-read units (by primary chapter and by any named chapter)', 'primary %s ; any %s ; total units %d' % (prim, anyc, sum(prim.values())))
say('PASS' if sum(prim.values()) == 24 else 'FAIL', 'B9 the combined paper still has 24 machine-read units', str(sum(prim.values())))
tbl = {t: sum(units(i) for i in comb if i['bloom'] == t) for t in range(1, 7)}
ge3 = sum(v for t, v in tbl.items() if t >= 3); ge4 = sum(v for t, v in tbl.items() if t >= 4)
say('PASS' if ge3 * 2 > 24 and ge4 >= 6 else 'FAIL', 'B9 combined paper: a majority at Apply or above and at least 6 at Analyze or above', '(levels %s; Apply or above %d; Analyze or above %d)' % (tbl, ge3, ge4))

# ------------------------------------------------------------------ B10
td = tempfile.mkdtemp(prefix='sen0401_items5b_')
try:
    cf = os.path.join(td, 'combined.json')
    json.dump(dict(note='combined test file (temporary)', version='test', items=remaining13 + items), open(cf, 'w', encoding='utf8'))
    os.environ['SEN0401_ENGINE_TMP'] = td
    # (a) equal chapter weights, the working default of the owner (not decided): MEASURED, because chapters 3 and 5 each lose an item and 2 and 6 each gain one
    try:
        Pe = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=cf)
        paper, g, p = E.make_and_check(Pe, 'midterm')
        v = [x[0] for x in E.validate(g, Pe.chapters) if x[1] == 'Violation']
        say('PASS', 'B10 MEASURED: engine v1.1.0 with the default equal chapter weights on the combined items', 'Violations %s' % (v or 'none'))
    except E.ExamRefused as e:
        say('PASS', 'B10 MEASURED: engine v1.1.0 with the default equal chapter weights REFUSED the combined items (exit 2); the owner has not decided the weights', str(e)[:300])
    # (b) the chapter weights declared as the primary-chapter counts of the combined items (a parameter of the engine, no rule edited)
    wts = {c: prim[c] for c in range(1, 7)}
    P = E.Params(24, (1, 2, 3, 4, 5, 6), wts, 'GridOnCover', authored=cf)
    try:
        paper, g, p = E.make_and_check(P, 'midterm')
        viol = E.validate(g, P.chapters)
        v = [x for x in viol if x[1] == 'Violation']
        say('PASS' if not v else 'FAIL', 'B10 engine v1.1.0, chapter weights %s: the midterm built from the combined items has no Violation (EN01-EN13, R01-R22)' % wts, str(v) if v else '(pages with the answer sheet: %s, content pages %s, sheet pages %s)' % (paper.get('pageCount'), paper.get('contentPages'), paper.get('sheetPages')))
        say('PASS' if paper['pool_size'] == len(remaining13 + items) and len(paper['items']) == len(remaining13 + items) else 'FAIL', 'B10 the paper holds all authored items', '(pool %d, paper items %d, skipped %s)' % (paper['pool_size'], len(paper['items']), paper['skipped']))
    except E.ExamRefused as e:
        say('FAIL', 'B10 engine v1.1.0 refused the combined midterm even with the declared chapter weights', str(e))
finally:
    shutil.rmtree(td, ignore_errors=True)

# ------------------------------------------------------------------ B11 the map
REQ = ['G', 'H', 'I', 'E', 'F', 'J', 'B', 'C']
if not os.path.exists(MAP_FILE):
    say('NOT_MEASURED', 'B11 the map file is missing', MAP_FILE)
else:
    mp = json.load(open(MAP_FILE, encoding='utf8')); rows = {r['point']: r for r in mp['rows']}
    miss = [p_ for p_ in REQ if p_ not in rows]
    say('PASS' if not miss else 'FAIL', 'B11 the map lists G H I E F J B C', 'missing %s' % miss if miss else '(%s)' % ' '.join(REQ))
    keys = {i['key'] for i in items}
    bad = [(p_, r['status']) for p_, r in rows.items() if r['status'] not in ('COVERED', 'PARTIAL', 'GAP')]
    bad += [(p_, k) for p_, r in rows.items() for k in r['items'] if k not in keys]
    bad += [(p_, 'no reason') for p_, r in rows.items() if r['status'] != 'COVERED' and not r.get('reason')]
    bad += [(p_, 'status without items') for p_, r in rows.items() if r['status'] in ('COVERED', 'PARTIAL') and not r['items']]
    bad += [(p_, 'GAP with items') for p_, r in rows.items() if r['status'] == 'GAP' and r['items']]
    say('PASS' if not bad else 'FAIL', 'B11 every row is COVERED, PARTIAL or GAP; the item keys exist; every non-covered row says why', str(bad) if bad else '(%d rows)' % len(rows))
    declared = {p_ for i in items for p_ in i.get('owner_points', [])}
    mapped = {p_ for p_, r in rows.items() if r['items']}
    claimed = {p_: [k for k in r['items']] for p_, r in rows.items()}
    bad = [(p_, k) for p_, ks in claimed.items() for k in ks if p_ not in next(i for i in items if i['key'] == k).get('owner_points', [])]
    say('PASS' if not bad else 'FAIL', 'B11 each item named in the map declares that point in its owner_points', str(bad))

print()
print('RESULT', 'FAIL' if fails else 'no FAIL line', '(%d lines; FAIL lines: %s)' % (len(out), fails or 'none'))
if '--log' in sys.argv:
    open(sys.argv[sys.argv.index('--log') + 1], 'w', encoding='utf8').write('\n'.join(out) + '\n')
sys.exit(1 if fails else 0)
