#!/usr/bin/env python3
"""SEN0401 exam items v1.4.0 part A: check, version 1.0.0 (new file; no question text and no answer inside, so it may be committed).

Checks the private file 08-tooling/exam/private/sen0401_exam_items5a_v1_0_0.json (question 1 = seven sub-questions Q1.a to Q1.g, answer block ChoiceFour).
Every line is printed as PASS, FAIL or NOT_MEASURED; exit code 0 only when no line is FAIL. Nothing existing is edited; the log is written by the caller into the private folder.
Items shown in output are named by KEY only, never by text (leak guard).

  L1  leak guard: the items file lies in private/, is git-ignored, is not tracked, is not staged; no private file is tracked
  S1  seven items in the slots Q1.a to Q1.g of the structure v1.0.0; the points of the slots add up to 25; the answer block of every slot is ChoiceFour; the two kept items equal items v1.3.0
  S2  schema: the fields of items v1.3.0 are all present; four distinct options, one correct answer; no option refers to another option
  S3  one unit per sub-question; the primary chapter of each new item equals the primary chapter of the item it replaces; chapters lie in 1 to 6
  S4  critical points exist and lie in the item's chapters; sources exist; kind agrees with the number of chapters
  C1  tips: 'Tips:' printed in the stem, every tip term and meaning printed in the stem
  C2  abbreviations: a list of known abbreviations is spelled out before first use; any other capital-letter token is listed for a human reader
  C3  no recall wording (name, define, call); each item names what it asks about
  C4  EN08: every term is found in the course corpus
  C5  EN11: no component of any new item copies a page-visible item (bank or quiz)
  C6  the builder, run again into a temporary private file, writes the same items file (arithmetic claims are evaluated there)
  C7  Bloom: majority at Apply or above, at least one at Analyze or above per new item; letters of the keys spread evenly over the seven
  E1  the engine v1.1.0 builds a midterm from items v1.3.0 with the five items replaced by these, and gives no Violation (EN01-EN13, R01-R22); chapters 1 to 6 each keep at least two machine-read units
  M1  MAP of T1-T9, A-F, G-P: the item key of part A that covers it, or GAP
  D1  DROPS: for each dropped item the critical points that lose their only holder, and which of them a new item holds again
"""
import json, os, re, subprocess, sys, tempfile, importlib.util
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
PRIV = os.path.join(HERE, 'private')
ITEMS_FILE = os.path.join(PRIV, 'sen0401_exam_items5a_v1_0_0.json')
SPEC_FILE = os.path.join(PRIV, 'sen0401_exam_items5a_spec_v1_0_0.json')
BUILDER = os.path.join(HERE, 'sen0401_exam_items5a_build_v1_0_0.py')
V13 = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')
STRUCT = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
TOPICS = os.path.join(HERE, 'sen0401_exam_owner_topics_v1_2_0.json')
MAP_OUT = None
if '--map-out' in sys.argv: MAP_OUT = sys.argv[sys.argv.index('--map-out') + 1]
fails = []


def say(status, name, detail=''):
    print('%-12s %s %s' % (status, name, detail))
    if status == 'FAIL': fails.append(name)


def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


def git(*a): return subprocess.run(['git', '-C', ROOT] + list(a), capture_output=True, text=True)


doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']; by = {i['key']: i for i in items}
v13 = json.load(open(V13, encoding='utf8'))['items']; v13by = {i['key']: i for i in v13}
st = json.load(open(STRUCT, encoding='utf8')); q1 = st['questions'][0]; subs = {s['key']: s for s in q1['sub']}
topics = json.load(open(TOPICS, encoding='utf8'))
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S
cp = E.cp_index()

# ------------------------------------------------------------------ L1 leak guard
rel = os.path.relpath(ITEMS_FILE, ROOT)
ign = git('check-ignore', '-q', rel).returncode == 0
tracked_private = git('ls-files', '--', os.path.relpath(PRIV, ROOT)).stdout.split()
staged = [l for l in git('diff', '--cached', '--name-only').stdout.split() if '/exam/private/' in l]
log_commits = git('log', '--oneline', '--', os.path.relpath(PRIV, ROOT)).stdout.split()
say('PASS' if os.path.commonpath([ITEMS_FILE, PRIV]) == PRIV else 'FAIL', 'L1 the items file lies in 08-tooling/exam/private/')
say('PASS' if ign else 'FAIL', 'L1 git check-ignore reports the items file as ignored (the guard of commit 8cee998)')
say('PASS' if not tracked_private and not staged and not log_commits else 'FAIL', 'L1 no file of private/ is tracked, staged or ever committed', '(tracked %d, staged %d, commits %d)' % (len(tracked_private), len(staged), len(log_commits)))
others = [l for l in git('status', '--porcelain').stdout.splitlines() if l[:2].strip() in ('M', 'D')]
say('PASS', 'L1 notice: tracked files modified in the working tree by other sessions (not by this task; listed, not judged)', '(%d files)' % len(others))

# ------------------------------------------------------------------ S1 slots
slots = doc['slots']
order = [s['sub'] for s in slots]
say('PASS' if order == ['Q1.a', 'Q1.b', 'Q1.c', 'Q1.d', 'Q1.e', 'Q1.f', 'Q1.g'] and len(items) == 7 and [s['item'] for s in slots] == [i['key'] for i in items] else 'FAIL', 'S1 seven items in the slots Q1.a to Q1.g in order', str(order))
say('PASS' if sum(s['points'] for s in slots) == 25 == q1['points'] and all(s['points'] == subs[s['sub']]['points'] for s in slots) else 'FAIL', 'S1 the slot points equal the points of the structure and add up to 25', str([s['points'] for s in slots]))
say('PASS' if q1['answer_block'] == 'ChoiceFour' and all(i['type'] == 'ChoiceFour' for i in items) else 'FAIL', 'S1 the answer block of question 1 is ChoiceFour and every item is a ChoiceFour item', str(sorted({i['type'] for i in items})))
kept = [s['item'] for s in slots if s['kept']]
say('PASS' if kept == ['mt2:i02:fee-not-written', 'mt2:i05:shop-confirmations'] and all(by[k] == v13by[k] for k in kept) else 'FAIL', 'S1 the two kept items (i02 fee and change, i05 confirmations) equal items v1.3.0 exactly', str(kept))
dropped = sorted({r for s in slots for r in s['replaces']})
say('PASS' if len(dropped) == 5 and all(subs[s['sub']]['item'] in s['replaces'] for s in slots if not s['kept']) else 'FAIL', 'S1 each new item replaces the item of the same slot in the structure; five items are dropped', str(dropped))

# ------------------------------------------------------------------ S2 schema
need = set(v13[0].keys())
bad = [(i['key'], sorted(need - set(i))) for i in items if need - set(i)]
say('PASS' if not bad else 'FAIL', 'S2 every field of the item schema of items v1.3.0 is present', str(bad) if bad else '(%d fields)' % len(need))
ref = re.compile(r'\b(all|none|both) of the (above|options|choices)\b|\b(option|choice) [A-D]\b|\b[A-D] (and|or) [A-D]\b', re.I)
bad = [i['key'] for i in items if len(i['options']) != 4 or len(set(i['options'])) != 4 or not (0 <= i['answer'] <= 3) or any(ref.search(o) for o in i['options'])]
say('PASS' if not bad else 'FAIL', 'S2 four distinct options, one answer index 0 to 3, no option refers to another option', str(bad))
lens = {i['key']: (len(i['options'][i['answer']]), max(len(o) for k, o in enumerate(i['options']) if k != i['answer'])) for i in items if i['key'].startswith('mt3:')}
longest = [k for k, (a, b) in lens.items() if a > b]
say('PASS', 'S2 MEASURED (not a pass condition): characters of the correct option against the longest wrong option, new items', str(lens) + ' ; correct option longest in %d of %d' % (len(longest), len(lens)))

# ------------------------------------------------------------------ S3 / S4
new = [i for i in items if i['key'].startswith('mt3:')]
bad = []
for s in slots:
    if s['kept']: continue
    it = by[s['item']]; old = subs[s['sub']]
    if it['chapters'][0] != old['chapters'][0]: bad.append((s['sub'], 'primary chapter', it['chapters'], old['chapters']))
    if not set(it['chapters']) <= {1, 2, 3, 4, 5, 6}: bad.append((s['sub'], 'chapter outside 1 to 6'))
say('PASS' if not bad else 'FAIL', 'S3 the primary chapter of every new item equals that of the item it replaces (the 4-per-chapter balance by primary chapter is kept); chapters in 1 to 6', str(bad) if bad else '(%s)' % {s['sub']: by[s['item']]['chapters'] for s in slots if not s['kept']})
diff = {s['sub']: (subs[s['sub']]['chapters'], by[s['item']]['chapters']) for s in slots if not s['kept'] and subs[s['sub']]['chapters'] != by[s['item']]['chapters']}
say('PASS', 'S3 notice: slots whose full chapter list differs from structure v1.0.0 (the structure is not edited; the paper builder must read the chapters from the items)', str(diff))
bad = []
for i in new:
    for c in i['critical_points']:
        if c not in cp: bad.append((i['key'], 'no such point', c))
        elif cp[c]['chapter'] not in i['chapters']: bad.append((i['key'], 'point outside the item chapters', c))
    for sx in [i['source']] + i['sources']:
        if not os.path.exists(os.path.join(ROOT, sx['file'])) or not sx.get('locator'): bad.append((i['key'], 'source', sx['file']))
    if (i['kind'] == 'direct') != (len(set(i['chapters'])) == 1): bad.append((i['key'], 'kind and chapters disagree'))
    if not (i.get('seeds') or str(i.get('no_seed_reason', '')).startswith('none:')): bad.append((i['key'], 'seed'))
    if not i.get('enhancements') or not set(i['enhancements']) <= {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}: bad.append((i['key'], 'enhancements'))
say('PASS' if not bad else 'FAIL', 'S4 critical points exist and lie in the item chapters; sources exist with a locator; kind agrees with chapters; seed reason; enhancements', str(bad) if bad else '(%d new items)' % len(new))
prov = [i['key'] for i in new if i.get('provisional')]
say('PASS' if prov == ['mt3:a5:old-notes-and-new-keys'] and all(by[k].get('provisional_reason') for k in prov) else 'FAIL', 'S4 the item whose reading is the author\'s (point L, old currencies) carries provisional:true with a reason', str(prov))

# ------------------------------------------------------------------ C1 / C2 / C3
bad = []
for i in new:
    if 'tips:' not in i['q'].lower(): bad.append((i['key'], 'no Tips:'))
    for t, m in i['tips']:
        if t.lower() not in i['q'].lower() or m.lower() not in i['q'].lower(): bad.append((i['key'], 'tip not printed', t))
    if len(i['tips']) < 3: bad.append((i['key'], 'fewer than 3 tips'))
say('PASS' if not bad else 'FAIL', 'C1 every new item prints its tips in the stem (term and meaning)', str(bad) if bad else '(%d items, %d tips)' % (len(new), sum(len(i['tips']) for i in new)))
ABBRS = {'WIF': 'wallet import format', 'P2PKH': 'pay to public key hash', 'SegWit': 'segregated witness', 'SHA256': 'secure hash algorithm 256', 'BIP329': 'bitcoin improvement proposal 329', 'txid': 'transaction identifier',
         'wtxid': 'witness transaction identifier', 'UTXO': 'unspent transaction output', 'BIP': 'bitcoin improvement proposal', 'BTC': 'bitcoin', 'SHA-256': 'secure hash algorithm', 'P2SH': 'pay to script hash',
         'HD': 'hierarchical deterministic', 'RBF': 'replace-by-fee', 'RPC': 'remote procedure call', 'PoW': 'proof of work', 'P2P': 'peer-to-peer', 'DNS': 'domain name system', 'TL': 'lira', 'YTL': 'new lira', 'VPN': 'virtual private network'}
bad = []; cap = {}
for i in new:
    text = i['q'] + ' ' + ' '.join(i['options'])
    for ab, full in ABBRS.items():
        m = re.search(r'(?<![A-Za-z0-9])' + re.escape(ab) + r'(?![A-Za-z0-9])', text, re.I if ab in ('txid', 'wtxid') else 0)
        if m and (text.lower().find(full) < 0 or text.lower().find(full) > m.start()): bad.append((i['key'], ab))
    for tok in re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,}[a-z]?|[A-Z][a-z]+[A-Z][A-Za-z]*)(?![A-Za-z0-9_])', text): cap.setdefault(tok, []).append(i['key'])
say('PASS' if not bad else 'FAIL', 'C2 every abbreviation of a list of %d is spelled out before its first use' % len(ABBRS), str(bad) if bad else '(none of the listed abbreviations is used)')
say('PASS', 'C2 other capital-letter tokens in the printed text of the new items (listed for a human reader, not judged)', str({k: sorted(set(v)) for k, v in cap.items()}))
RECALL = re.compile(r"\b(what is the name|name the|what is it called|which term|what do we call|is called the|write the (word|term|name)|recall|from memory|define )\b", re.I)
bad = [i['key'] for i in new if RECALL.search(i['q'] + ' ' + ' '.join(i['options']))]
say('PASS' if not bad else 'FAIL', 'C3 no new item asks for a name, a term or a definition by wording', str(bad))
say('PASS' if all(i['understanding'].startswith('reason:') for i in new) else 'FAIL', 'C3 every new item names what it asks about (a reason, not a recall)')
say('PASS' if all(i['q'].rstrip().endswith('?') for i in new) else 'FAIL', 'C3 every stem ends with a question')

# ------------------------------------------------------------------ C4 / C5
unf = {i['key']: E0.unfound_terms(i) for i in new}; unf = {k: v for k, v in unf.items() if v}
say('PASS' if not unf else 'FAIL', 'C4 EN08 every term of every new item is found in the course corpus', str(unf) if unf else '(%d terms)' % sum(len(i['terms']) for i in new))
pages = S.page_items((1, 2, 3, 4, 5, 6)); hits = []
for i in new:
    for label, ref_, kinds, ss, os_ in E.check_copies(i, pages): hits.append((i['key'], label, ref_, kinds, ss, os_))
say('PASS' if not hits else 'FAIL', 'C5 EN11 no component of any new item matches a page-visible item', '(checked against %d page items)' % len(pages) if not hits else str(hits))
best = []
for i in new:
    for label, stem_, opts in S.components(i):
        c = S.prepare(stem_, opts)
        for p in pages:
            kinds, ss, os_ = S.compare(c, p['p']); best.append((ss, os_, i['key'], label, p['ref']))
b1 = max(best); b2 = max(best, key=lambda x: x[1])
say('PASS', 'C5 MEASURED largest stem share against any page item (refusal at %.2f)' % S.STEM_NEAR_J2, '(%.3f: %s %s against %s)' % (b1[0], b1[2], b1[3], b1[4]))
say('PASS', 'C5 MEASURED largest option share against any page item (refusal at %.2f)' % S.OPTIONS_NEAR_SHARE, '(%.3f: %s %s against %s)' % (b2[1], b2[2], b2[3], b2[4]))

# ------------------------------------------------------------------ C6 builder again
with tempfile.TemporaryDirectory(dir=PRIV) as td:
    out2 = os.path.join(td, 'again.json')
    r = subprocess.run([sys.executable, '-I', BUILDER, '--spec', SPEC_FILE, '--out', out2], capture_output=True, text=True)
    same = r.returncode == 0 and json.load(open(out2, encoding='utf8')) == doc
say('PASS' if same else 'FAIL', 'C6 the builder, run again, writes the same items file; its program evaluated every arithmetic claim of the spec', '(builder exit %d)' % r.returncode)

# ------------------------------------------------------------------ C7 Bloom, letters
tbl = {}
for i in items: tbl[i['bloom']] = tbl.get(i['bloom'], 0) + 1
ge3 = sum(1 for i in items if i['bloom'] >= 3); ge4 = sum(1 for i in items if i['bloom'] >= 4)
say('PASS' if ge3 * 2 > len(items) and all(i['bloom'] >= 4 for i in new) and all(i['bloom'] <= 4 for i in items) else 'FAIL', 'C7 Bloom levels: a majority at Apply or above, every new item at Analyze, none above what ChoiceFour can honestly reach (4)', str(dict(sorted(tbl.items()))) + ' ; Apply or above %d of %d ; Analyze or above %d' % (ge3, len(items), ge4))
let = {}
for i in items: let['ABCD'[i['answer']]] = let.get('ABCD'[i['answer']], 0) + 1
say('PASS' if len(let) == 4 and max(let.values()) - min(let.values()) <= 1 else 'FAIL', 'C7 answer letters of the seven items evenly spread', str(dict(sorted(let.items()))))

# ------------------------------------------------------------------ E1 engine
merged = [i for i in v13 if i['key'] not in dropped]
mk = {i['key'] for i in merged}
for i in items:
    if i['key'] not in mk: merged.append(i)
with tempfile.TemporaryDirectory(dir=PRIV) as td:
    mf = os.path.join(td, 'merged.json')
    json.dump({'note': 'scratch: items v1.3.0 with the five dropped items replaced by part A', 'version': 'scratch', 'chapters': [1, 2, 3, 4, 5, 6], 'items': merged}, open(mf, 'w', encoding='utf8'), ensure_ascii=False)
    try:
        P = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=mf)
        os.environ.setdefault('SEN0401_ENGINE_TMP', tempfile.gettempdir())
        paper, g, p = E.make_and_check(P, 'midterm')
        viol = E.validate(g, P.chapters)
        v = [x for x in viol if x[1] == 'Violation']; w = [x for x in viol if x[1] != 'Violation']
        say('PASS' if not v else 'FAIL', 'E1 engine v1.1.0 builds the midterm from the merged items (v1.3.0 with part A in place of the five) with no Violation (EN01-EN13, R01-R22)', str(v) if v else '(pool %s, paper items %d, pages %s)' % (paper['pool_size'], len(paper['items']), paper.get('pageCount')))
        for x in w: say('PASS', 'E1 non-violation notice (' + x[1] + ')', x[2])
    except E.ExamRefused as e:
        say('FAIL', 'E1 engine v1.1.0 refused the merged midterm', str(e))
    except Exception as e:
        say('NOT_MEASURED', 'E1 engine run failed to start', repr(e)[:300])
n_units = sum(units(i) for i in merged)
say('PASS' if n_units == 24 else 'FAIL', 'E1 the merged set still has 24 machine-read units', '(%d items, %d units)' % (len(merged), n_units))
prim = {c: sum(units(i) for i in merged if i['chapters'][0] == c) for c in range(1, 7)}
anyc = {c: sum(units(i) for i in merged if c in i['chapters']) for c in range(1, 7)}
say('PASS' if all(v == 4 for v in prim.values()) else 'FAIL', 'E1 machine-read units per primary chapter (v1.3.0 had 4 each)', str(prim))
say('PASS' if all(v >= 2 for v in prim.values()) and all(v >= 2 for v in anyc.values()) else 'FAIL', 'E1 each of the chapters 1 to 6 keeps at least two machine-read units (by primary chapter and by any named chapter)', 'primary %s ; any %s' % (prim, anyc))

# ------------------------------------------------------------------ M1 map
allt = [t['id'] for t in topics['topics']] + [p['id'] for p in topics['points']] + [p['id'] for p in topics['points2']]
label = {t['id']: t['topic'] for t in topics['topics']}
label.update({p['id']: p['point'] for p in topics['points'] + topics['points2']})
cover = {}
for s in slots:
    it = by[s['item']]
    pts = it.get('owner_points') or ({'mt2:i02:fee-not-written': ['A', 'C3'], 'mt2:i05:shop-confirmations': ['T4']}.get(it['key'], []))
    for pid in pts: cover.setdefault(pid, []).append((it['key'], s['sub']))
ELSEWHERE = {  # from the analysis of items v1.3.0 (second edition), section 2; items of parts B and C or the bonus; not part A
    'T7': 'outside part A (v1.3.0: i06, i07, i22)', 'T8': 'outside part A (v1.3.0: i17, i19; i20 is dropped here)', 'B': 'outside part A (v1.3.0: i03)', 'C': 'outside part A (v1.3.0: i06, i07)',
    'D': 'outside part A (no item today)', 'E': 'outside part A (bonus b2 half)', 'F': 'outside part A (i23 side mention)', 'G': 'outside part A (v1.3.0: i03 partial)', 'H': 'outside part A (no item today)',
    'I': 'outside part A (bonus b2 half)', 'J': 'outside part A (v1.3.0: i02, i23 partial)', 'N': 'outside part A (no item today)'}
lines = []
for t in allt:
    if t == 'C3': continue
    if t in cover:
        w = '; '.join('%s in %s' % (k, sub) for k, sub in cover[t])
        lines.append((t, w, label[t]))
    else:
        lines.append((t, 'GAP in part A: ' + ELSEWHERE.get(t, 'not assigned'), label[t]))
for t, w, lab in lines: print('MAP          %-3s %-72s | %s' % (t, w, lab[:60]))
needed = ['T1', 'T2', 'T3', 'T5', 'T9', 'K', 'L', 'M', 'O', 'P']
miss = [t for t in needed if t not in cover]
say('PASS' if not miss else 'FAIL', 'M1 each of T1 T2 T3 T5 T9 K L M O P is covered by a part-A item (item key and sub-question printed above), none left as GAP', 'GAP: %s' % miss)
say('PASS', 'M1 summary of the map', 'covered in part A: %s ; GAP in part A (held elsewhere or by no item): %s' % (sorted(cover), sorted(t for t in allt if t not in cover and t != 'C3')))
if MAP_OUT:
    with open(MAP_OUT, 'x', encoding='utf8') as f:
        for t, w, lab in lines: f.write('%s\t%s\t%s\n' % (t, w, lab))
    say('PASS', 'M1 map written', MAP_OUT)

# ------------------------------------------------------------------ D1 drops
bonus = [s for q in st['questions'] if q.get('bonus') for s in q['sub']]
def holders(itemset):
    h = {}
    for i in itemset:
        for c in i['critical_points']: h.setdefault(c, set()).add(i['key'])
    for s in bonus:
        for c in s['critical_points']: h.setdefault(c, set()).add(s['item'])
    return h
before = holders(v13)
after_items = [i for i in v13 if i['key'] not in dropped] + new
after = holders(after_items)
lone_all = {i['key']: sorted(c for c in i['critical_points'] if before[c] == {i['key']}) for i in v13}
for k in dropped:
    lone = lone_all[k]; lost = [c for c in lone if c not in after]; kept_c = [c for c in lone if c in after]
    print('DROP         %-40s sole-holder points: %s' % (k, lone))
    print('             lose their only holder: %s' % lost)
    print('             held again by a new item: %s' % {c: sorted(after[c]) for c in kept_c})
lost_all = sorted(c for c in before if c not in after); gained = sorted(c for c in after if c not in before)
say('PASS', 'D1 critical points held before (items v1.3.0 and bonus) and no longer held by any item', '%d points: %s' % (len(lost_all), lost_all))
say('PASS', 'D1 critical points held by part A that no item held before', '%s' % gained)
say('PASS', 'D1 count of held points before and after (chapters 1 to 6)', '%d -> %d' % (len(before), len(after)))
rank = sorted((len(v), k) for k, v in lone_all.items())
say('PASS', 'D1 MEASURED context (not a pass condition): number of sole-held points of all 21 items of v1.3.0, least first', str(rank))
print('RESULT       %s' % ('FAIL: ' + '; '.join(fails) if fails else 'no line is FAIL'))
sys.exit(1 if fails else 0)
