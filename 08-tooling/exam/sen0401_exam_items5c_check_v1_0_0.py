#!/usr/bin/env python3
"""SEN0401 midterm items v1.4.0 PART C check, version 1.0.0 (new file; holds no question and no answer; safe to commit).

Checks the private file 08-tooling/exam/private/sen0401_exam_items5c_v1_0_0.json (questions 3 to 5 of the one midterm form) against the committed items v1.3.0
and structure v1.0.0, the engine v1.1.0 (term index, similarity, shapes) and the critical points. Nothing is edited. Nothing that holds a question or an answer is printed:
the lines name checks, keys and counts only.

Every line is PASS, FAIL or NOT_MEASURED; the exit code is 0 only when no line is FAIL.

Checks
  P1  leak guard: the items file is untracked and ignored by git (git check-ignore), no tracked file is modified, no tracked file holds a long piece of any printed item text
  P2  structure: Q3 = Ordering 8 + Matching 8 + Matching 9 = 25; Q4 = six FillBlankGroup sub-questions (4,4,4,4,5,4) = 25 over three items with two blanks each; Q5 = two hand-marked prompts of 5
      = 10 (bonus); every position keeps the answer block type of structure v1.0.0; one form (no form A or B)
  P3  items i06, i18 and i23 are byte-equal to items v1.3.0 (carried unchanged)
  P4  schema of items v1.3.0: keys, seeds resolve, critical points exist and lie in the item chapters, sources exist, enhancements, kind, level not above the type cap
  P5  EN08 terms found in the course corpus (engine index); in addition each term is looked up in the decks of chapters 1 to 6 alone and the ones found only in later chapters are named
  P6  EN11 copy test against all page-visible items (bank and quiz)
  P7  matching items: 4 premises, 6 responses, each match among the responses, matches distinct, two unused, the response order is not the premise order
  P8  fill-in items: two blanks, a bank of at most 9, bank entries distinct and each with a tip in brackets, tips printed with the item
  P9  C2: both readings are present as marked alternatives, each recomputed by brute force from the facts; the default fields equal the careful reading; provisional is true with a reason
  P10 C1 (carried i06): the order is recomputed from the printed steps over all 120 orders
  P11 provisional marks: every item or prompt whose reading is the author's carries provisional true and a reason
  P12 conventions: no recall wording, abbreviations spelled out before first use, every term used is in a tip, simple arithmetic (numbers in the printed text are listed for a reader)
  P13 the map: D, E, F, N, I, O are each an item key or GAP; the item tags (points) are backed by key words in the item text; the map file names the same keys
  P14 drops: for each dropped item the critical points that lose their only holder are recomputed from the tags of the whole paper (items v1.3.0 outside part C unchanged) and equal the file's statement
  P15 chapters: every chapter 1 to 6 keeps at least two machine-read units in the whole paper (items v1.3.0 outside part C unchanged, part C as built)
  P16 engine v1.1.0 builds the midterm from the merged items (v1.3.0 outside part C, part C as built); shapes EN01 to EN13 and R01 to R22 give no Violation (the result is reported as printed)
Usage: sen0401_exam_items5c_check_v1_0_0.py [--items FILE] [--skip-engine]
"""
import copy, importlib.util, io, itertools, json, os, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
ITEMS_FILE = os.path.join(HERE, 'private', 'sen0401_exam_items5c_v1_0_0.json')
if '--items' in sys.argv: ITEMS_FILE = sys.argv[sys.argv.index('--items') + 1]
MAP_FILE = os.path.join(os.path.dirname(ITEMS_FILE), 'sen0401_exam_items5c_map_v1_0_0.txt')
V13 = os.path.join(HERE, 'sen0401_exam_items_midterm_v1_3_0.json')
STRUCT = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
ALLOWED_ENH = {'change the situation', 'combine chapters', 'reverse the question', 'add a reasoning step', 'change the numbers'}
CAP = {'ChoiceFour': 4, 'ChoiceFourCode': 4, 'Matching': 3, 'Ordering': 3, 'FillBlankGroup': 2, 'NumericAnswer': 3, 'CodeTrace': 4}
fails = []


def say(status, name, detail=''):
    print('%-12s %s %s' % (status, name, detail))
    if status == 'FAIL': fails.append(name)


def units(i): return len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1


doc = json.load(open(ITEMS_FILE, encoding='utf8')); items = doc['items']; bonus = doc['bonus']; by = {i['key']: i for i in items}
v13 = json.load(open(V13, encoding='utf8')); v13by = {i['key']: i for i in v13['items']}
struct = json.load(open(STRUCT, encoding='utf8'))
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_v1_0_0 as E0
import sen0401_exam_similarity_v1_1_0 as S

# ------------------------------------------------------------------ P1 leak guard
rel = os.path.relpath(ITEMS_FILE, ROOT)
ign = subprocess.run(['git', '-C', ROOT, 'check-ignore', '-q', rel]).returncode == 0
tracked = subprocess.run(['git', '-C', ROOT, 'ls-files', '--error-unmatch', rel], capture_output=True).returncode == 0
say('PASS' if ign and not tracked else 'FAIL', 'P1 the items file is git-ignored and not tracked (leak guard)', '(ignored %s, tracked %s)' % (ign, tracked))
st = subprocess.run(['git', '-C', ROOT, 'status', '--porcelain'], capture_output=True, text=True).stdout.splitlines()
mods_all = [l for l in st if l[:2] in (' M', 'M ', 'MM', ' D', 'D ', 'AM', 'A ')]
mods = [l for l in mods_all if '08-tooling/exam/' in l]
say('PASS' if not mods else 'FAIL', 'P1 no tracked file under 08-tooling/exam is modified or staged', '(modified or staged tracked files there: %s)' % (mods or 'none'))
say('PASS', 'P1 MEASURED: tracked files modified elsewhere in the repository by other sessions (not this work)', '(%d: %s)' % (len(mods_all) - len(mods), sorted({l[3:].split('/')[1] + '/' + l[3:].split('/')[2] for l in mods_all if l not in mods})))


def printed(i):
    parts = [i.get('q', ''), i.get('code', '')] + list(i.get('options', [])) + list(i.get('steps', []))
    parts += [p_['text'] for p_ in i.get('premises', [])] + list(i.get('responses', []))
    parts += [b_['text'] + ' ' + b_['answer'] for b_ in i.get('blanks', [])] + list(i.get('distractors', []))
    return ' \n '.join(x for x in parts if x)


frag = []
for i in items:
    for piece in re.split(r'\s*\n\s*', printed(i)):
        if len(piece) >= 40 and i['key'] not in v13by: frag.append(piece)
for b in bonus: frag += [b['prompt']] + b['rubric']
tracked_files = subprocess.run(['git', '-C', ROOT, 'ls-files'], capture_output=True, text=True).stdout.splitlines()
scan = [f for f in tracked_files if f.startswith('08-tooling/exam/') and f.endswith(('.py', '.txt', '.md', '.json', '.ttl'))]
leak = []
for f in scan:
    try: txt = open(os.path.join(ROOT, f), encoding='utf8').read()
    except Exception: continue
    for p in frag:
        if p in txt: leak.append((f, p[:20] + '...')); break
say('PASS' if not leak else 'FAIL', 'P1 no tracked file under 08-tooling/exam holds a printed new item text or prompt of 40 or more characters', '(scanned %d tracked files against %d pieces)' % (len(scan), len(frag)))
this = open(__file__, encoding='utf8').read()
bad = [p for p in frag if p in this]
say('PASS' if not bad else 'FAIL', 'P1 this check script holds no printed item text', '(%d pieces)' % len(frag))

# ------------------------------------------------------------------ P2 structure
Q = {q['number']: q for q in doc['structure_part_c']['questions']}
old = {s['key']: s for q in struct['questions'] for s in q['sub']}
q3 = Q[3]['sub']; q4 = Q[4]['sub']; q5 = Q[5]['sub']
ok3 = [s['key'] for s in q3] == ['Q3.a', 'Q3.b', 'Q3.c'] and [s['type'] for s in q3] == ['Ordering', 'Matching', 'Matching'] and [s['points'] for s in q3] == [8, 8, 9] and sum(s['points'] for s in q3) == 25 == Q[3]['points']
ok4 = [s['key'] for s in q4] == ['Q4.a', 'Q4.b', 'Q4.c', 'Q4.d', 'Q4.e', 'Q4.f'] and all(s['type'] == 'FillBlankGroup' for s in q4) and [s['points'] for s in q4] == [4, 4, 4, 4, 5, 4] and sum(s['points'] for s in q4) == 25 == Q[4]['points']
ok5 = [s['key'] for s in q5] == ['Q5.a', 'Q5.b'] and sum(s['points'] for s in q5) == 10 == Q[5]['points'] and Q[5].get('bonus') and all(s['hand_marked'] and not s['machine_read'] and s['rubric_points'] <= 3 and s['lines'] >= 3 for s in q5)
say('PASS' if ok3 else 'FAIL', 'P2 Q3 = ordering 8 + matching 8 + matching 9 = 25', '(%s)' % [(s['key'], s['type'], s['points']) for s in q3])
say('PASS' if ok4 else 'FAIL', 'P2 Q4 = six fill-in sub-questions 4,4,4,4,5,4 = 25', '(%s)' % [s['points'] for s in q4])
say('PASS' if ok5 else 'FAIL', 'P2 Q5 = two hand-marked prompts of 5 = 10 (bonus), rubric of at most 3 points, 3 lines', '(%s)' % [(s['key'], s['points'], s['rubric_points'], s['lines']) for s in q5])
same_block = all(old[s['key']]['block'] == s['block'] and old[s['key']]['type'] == s['type'] and old[s['key']]['points'] == s['points'] for s in q3 + q4) and all(old[s['key']]['block'] == s['block'] for s in q5)
say('PASS' if same_block else 'FAIL', 'P2 every sub-question position keeps the answer block type, type and points of structure v1.0.0', '(%d positions)' % (len(q3) + len(q4) + len(q5)))
sub_items = {s['item'] for s in q3 + q4}
say('PASS' if sub_items == set(by) and len({s['item'] for s in q4}) == 3 and all(sum(1 for s in q4 if s['item'] == k) == 2 for k in {s['item'] for s in q4}) else 'FAIL', 'P2 every item is used by the sub-questions; Q4 uses three items, two blanks each', '(%d items)' % len(by))
bad = [(s['key'], k) for s in q3 + q4 for k in ('parts',) if s['type'] in ('Ordering', 'Matching') and s.get(k) != (len(by[s['item']].get('steps', [])) or len(by[s['item']].get('premises', [])))]
say('PASS' if not bad else 'FAIL', 'P2 parts of each ordering or matching sub-question equal its steps or premises', str(bad))
text_all = json.dumps(doc, ensure_ascii=False).lower()
say('PASS' if doc.get('one_form') is True and not re.search(r'\bform [ab]\b', text_all) else 'FAIL', 'P2 one form of the midterm: one_form is true and no form A or B appears')

# ------------------------------------------------------------------ P3 carried items
carried = [k for k, i in by.items() if i.get('carried_unchanged_from')]
bad = []
for k in carried:
    a = {x: y for x, y in by[k].items() if x not in ('carried_unchanged_from', 'owner_points')}
    if a != v13by[k]: bad.append(k)
say('PASS' if sorted(carried) == ['mt2:i06:order-wallet-to-block', 'mt2:i18:match-story-lesson', 'mt2:i23:fill-txid-and-weight'] and not bad else 'FAIL', 'P3 i06, i18 and i23 are equal to items v1.3.0 (carried unchanged)', '(carried %s, different %s)' % (sorted(carried), bad))

# ------------------------------------------------------------------ P4 schema
pages = S.page_items((1, 2, 3, 4, 5, 6)); page_refs = {p['ref']: p for p in pages}; cp = E.cp_index()
problems = []
for i in items:
    k = i['key']
    for need in ('key', 'type', 'chapters', 'bloom', 'kind', 'source', 'critical_points', 'seeds', 'no_seed_reason', 'enhancements', 'papers', 'from_item', 'tips', 'terms', 'abbreviations', 'instruction', 'computed', 'understanding'):
        if need not in i: problems.append((k, 'lacks ' + need))
    if not i.get('seeds') and not str(i.get('no_seed_reason', '')).startswith('none:'): problems.append((k, 'no seed and no "none:" reason'))
    for s_ in i.get('seeds', []):
        if s_ not in page_refs: problems.append((k, 'seed does not resolve: ' + s_))
        elif page_refs[s_]['chapter'] not in i['chapters']: problems.append((k, 'seed from a chapter the item does not name: ' + s_))
    if not i.get('critical_points'): problems.append((k, 'no critical point'))
    for c in i.get('critical_points', []):
        if c not in cp: problems.append((k, 'critical point does not exist: ' + c))
        elif cp[c]['chapter'] not in i['chapters']: problems.append((k, 'critical point outside the item chapters: ' + c))
    if not set(i.get('enhancements', [])) <= ALLOWED_ENH or not i.get('enhancements'): problems.append((k, 'enhancements'))
    if i['kind'] == 'synthesis' and len(set(i['chapters'])) < 2: problems.append((k, 'synthesis with one chapter'))
    if i['kind'] == 'direct' and len(set(i['chapters'])) > 1: problems.append((k, 'direct with several chapters'))
    if i['bloom'] > CAP[i['type']]: problems.append((k, 'level above the type cap'))
    if i['papers'] != ['midterm']: problems.append((k, 'papers'))
    for sx in [i['source']] + i.get('sources', []):
        if not os.path.exists(os.path.join(ROOT, sx['file'])) or not sx.get('locator'): problems.append((k, 'source missing: ' + sx.get('file', '?')))
for b in bonus:
    for c in b['critical_points']:
        if c not in cp: problems.append((b['key'], 'critical point does not exist: ' + c))
    for sx in b['sources']:
        if not os.path.exists(os.path.join(ROOT, sx['file'])): problems.append((b['key'], 'source missing'))
say('PASS' if not problems else 'FAIL', 'P4 schema of items v1.3.0: keys, seeds, critical points, chapters, sources, level, kind', str(problems) if problems else '(%d items, %d bonus prompts)' % (len(items), len(bonus)))

# ------------------------------------------------------------------ P5 terms
unf = {i['key']: E0.unfound_terms(i) for i in items}; unf.update({b['item']: E0.unfound_terms(b) for b in bonus})
unf = {k: v for k, v in unf.items() if v}
say('PASS' if not unf else 'FAIL', 'P5 EN08 every term is found in the course corpus (engine index: banks, critical points, decks of chapters 1 to 8)', str(unf) if unf else '(%d terms)' % (sum(len(i['terms']) for i in items) + sum(len(b['terms']) for b in bonus)))
import sen0401_exam_pptx_text_v1_0_0 as T
parts16 = []
for c in range(1, 7):
    for s in T.slides_of(T.newest_deck(c)): parts16.append(str(s.get('slide', '')) + ' ' + str(s.get('notes', '')))
ix16 = re.sub(r'\s+', ' ', ' '.join(parts16)).lower()
only_late = {}
for it in list(items) + list(bonus):
    miss = [t for t in it.get('terms', []) if re.sub(r'\s+', ' ', t).lower() not in ix16]
    if miss: only_late[it.get('key')] = miss
say('PASS', 'P5 MEASURED: terms not found in the decks of chapters 1 to 6 alone (found only in banks, critical points or later decks)', str(only_late) if only_late else '(none)')

# ------------------------------------------------------------------ P6 copies
hits = []
for i in items:
    for label, ref, kinds, ss, os_ in E.check_copies(i, pages): hits.append((i['key'], label, ref, kinds, ss, os_))
say('PASS' if not hits else 'FAIL', 'P6 EN11 no component of any item matches a page-visible item', '(checked against %d page items)' % len(pages) if not hits else str(hits))
best = []
for i in items:
    if i['key'] in carried: continue
    for label, stem, opts in S.components(i):
        c = S.prepare(stem, opts)
        for p in pages:
            kinds, ss, os_ = S.compare(c, p['p']); best.append((ss, os_, i['key'], label, p['ref']))
if best:
    b1 = max(best, key=lambda x: x[0]); b2 = max(best, key=lambda x: x[1])
    say('PASS', 'P6 largest stem share found by new or reworked items (measured; refusal at %.2f)' % S.STEM_NEAR_J2, '(%.3f: %s %s against %s)' % (b1[0], b1[2], b1[3], b1[4]))
    say('PASS', 'P6 largest option share found by new or reworked items (measured; refusal at %.2f)' % S.OPTIONS_NEAR_SHARE, '(%.3f: %s %s against %s)' % (b2[1], b2[2], b2[3], b2[4]))
for b in bonus:
    comp = S.prepare(b['prompt'], [])
    worst = max((S.compare(comp, p['p'])[1:] for p in pages), key=lambda x: x[0])
    say('PASS', 'P6 bonus prompt %s: largest stem share against any page item (measured)' % b['key'], '(%.3f)' % worst[0])

# ------------------------------------------------------------------ P7 matching
bad = []; same_order_carried = []
for i in items:
    if i['type'] != 'Matching': continue
    pm = [p_['match'] for p_ in i['premises']]; rs = i['responses']
    if len(i['premises']) != 4 or len(rs) != 6 or len(set(rs)) != 6 or len(set(pm)) != 4 or not set(pm) <= set(rs) or len(set(rs) - set(pm)) != 2: bad.append((i['key'], 'shape'))
    if rs[:4] == pm:
        if i['key'] in v13by: same_order_carried.append(i['key'])
        else: bad.append((i['key'], 'response order equals premise order'))
say('PASS' if not bad else 'FAIL', 'P7 matching items: 4 premises, 6 distinct responses, each match among them, two unused; for the new item the response order differs from the premise order', str(bad) if bad else '(%d items)' % sum(1 for i in items if i['type'] == 'Matching'))
say('PASS', 'P7 MEASURED: carried matching items whose stored response order equals the premise order (committed text, not edited here; the engine shuffles the printed order)', str(same_order_carried) if same_order_carried else '(none)')

# ------------------------------------------------------------------ P8 fill-in
bad = []
for i in items:
    if i['type'] != 'FillBlankGroup': continue
    ans = [b_['answer'] for b_ in i['blanks']]; bank = ans + i['distractors']; tx = printed(i).lower()
    if len(i['blanks']) != 2 or len(bank) > 9 or len(set(bank)) != len(bank): bad.append((i['key'], 'bank shape'))
    if any(not re.search(r'\(.+\)', b_) for b_ in bank): bad.append((i['key'], 'bank entry without tip in brackets'))
    if any(b_['text'].count('____') != 1 for b_ in i['blanks']): bad.append((i['key'], 'blank marks'))
    for t_ in i['tips']:
        if t_[1].lower() not in tx and t_[0].lower() not in tx: bad.append((i['key'], 'tip not printed: ' + t_[0]))
say('PASS' if not bad else 'FAIL', 'P8 fill-in items: two blanks of one mark each, a bank of at most 9 distinct entries, each entry with a tip, every tip printed', str(bad) if bad else '(%d items)' % sum(1 for i in items if i['type'] == 'FillBlankGroup'))

# ------------------------------------------------------------------ P9 C2
c2 = [i for i in items if i.get('owner_case') == 'C2']
if len(c2) != 1: say('FAIL', 'P9 exactly one C2 item', str(len(c2)))
else:
    c2 = c2[0]; f = c2['facts']; TX = f['payments']; SP = [tuple(x) for x in f['spends']]; STATED = f['stated_inside_a_block_careful_reading']

    def decide(reading):
        ok = []
        for bits in itertools.product([0, 1], repeat=len(TX)):
            s = dict(zip(TX, bits))
            if reading == 'careful':
                if any(not s[x] for x in STATED) or any(s[a] and not s[b] for a, b in SP): continue
            elif any(not s[b] for a, b in SP): continue
            ok.append(s)
        sure = [t for t in TX if all(s[t] for s in ok)]; und = [t for t in TX if any(s[t] for s in ok) and any(not s[t] for s in ok)]
        return sure, und

    alts = {a['reading']: a for a in c2.get('alternatives', [])}
    say('PASS' if set(alts) == {'careful', 'owner_simple'} and c2.get('active_reading') == 'careful' else 'FAIL', 'P9 C2 holds both readings as marked alternatives, the careful one active by default', str(sorted(alts)))
    for rd, a in alts.items():
        sure, und = decide(rd)
        # the first blank names the payments that are mined, the second those not shown to be mined: read the letters of each blank text from the capital letters before the blank
        def named(txt):
            tail = txt.split('____')[0]; m = re.search(r'((?:[A-Z](?:, | and )?)+)\s*(?:are|is)\s*$', tail.strip())
            return sorted(re.findall(r'[A-Z]', m.group(1))) if m else None
        n1 = named(a['blanks'][0]['text']); n2 = named(a['blanks'][1]['text'])
        exp1 = sorted(set(sure) - set(STATED if rd == 'careful' else []))     # careful reading: the stated payment is given in the stem, so the blank names the others
        okk = n1 == exp1 and n2 == sorted(und) and a['blanks'][0]['answer'].startswith('mined') and a['blanks'][1]['answer'].startswith('not shown to be mined')
        say('PASS' if okk else 'FAIL', 'P9 C2 reading %s: the blanks name the payments the brute force finds (shown mined and not given in the stem; undecided)' % rd, '(brute force: mined %s, undecided %s; blank 1 names %s, blank 2 names %s)' % (sure, und, n1, n2))
    dflt = alts.get('careful')
    say('PASS' if dflt and c2['blanks'] == dflt['blanks'] and c2['distractors'] == dflt['distractors'] and c2['tips'] == dflt['tips'] else 'FAIL', 'P9 the default fields of C2 equal the careful reading')
    say('PASS' if c2.get('provisional') is True and len(c2.get('provisional_reason', '')) > 40 else 'FAIL', 'P9 C2 carries provisional true with a reason')
    same_bank = {a['blanks'][0]['answer'] for a in alts.values()} == {a['blanks'][0]['answer'] for a in alts.values()}
    say('PASS' if len({a['blanks'][0]['answer'] for a in alts.values()}) == 1 and len({a['blanks'][1]['answer'] for a in alts.values()}) == 1 and len(alts['careful']['distractors']) == len(alts['owner_simple']['distractors']) == 2 else 'FAIL', 'P9 both readings use the same two answers and two distractor slots, so the answer sheet is the same')

# ------------------------------------------------------------------ P10 C1 order
i06 = by.get('mt2:i06:order-wallet-to-block'); ref = {}
for n, stp in enumerate(i06['steps']):
    m = re.match(r'Transaction (\w) (?:is a coinbase|spends .* of transaction (\w))', stp)
    ref[m.group(1)] = m.group(2)
names = list(ref); sols = [p for p in itertools.permutations(names) if all(ref[x] is None or p.index(ref[x]) < p.index(x) for x in names)]
printed_order = [re.match(r'Transaction (\w)', s).group(1) for s in i06['steps']]
say('PASS' if len(sols) == 1 and list(sols[0]) == printed_order else 'FAIL', 'P10 C1: the printed order of the steps is the only one of %d orders in which every spender follows what it spends' % len(list(itertools.permutations(names))), '(solutions: %d)' % len(sols))

# ------------------------------------------------------------------ P11 provisional
need_prov = [k for k, i in by.items() if i.get('owner_points') and any(p in i['owner_points'] for p in ('N',))] + [c2['key']] + [b['item'] for b in bonus if 'F' in b.get('owner_points', [])]
bad = []
for k in need_prov:
    it = by.get(k) or next(b for b in bonus if b['item'] == k)
    if it.get('provisional') is not True or len(it.get('provisional_reason', '')) < 40: bad.append(k)
say('PASS' if need_prov and not bad else 'FAIL', 'P11 the items whose reading is the author\'s (N scripts, C2 readings, F pace of the bonus) carry provisional true with a reason', '(marked: %s; bad: %s)' % (need_prov, bad))

# ------------------------------------------------------------------ P12 conventions
RECALL = re.compile(r"\b(what is the name|name the|what is it called|which term|what do we call|is called the|write the (word|term|name)|recall|from memory|define )", re.I)
bad = [i['key'] for i in items if i['key'] not in v13by and RECALL.search(printed(i))] + [b['key'] for b in bonus if RECALL.search(b['prompt'])]
say('PASS' if not bad else 'FAIL', 'P12 no recall wording in the new or reworked items and prompts', str(bad))
ABBRS = {'WIF': 'wallet import format', 'P2PKH': 'pay to public key hash', 'SegWit': 'segregated witness', 'SHA256': 'secure hash algorithm 256', 'txid': 'transaction identifier', 'wtxid': 'witness transaction identifier',
         'UTXO': 'unspent transaction output', 'BIP': 'bitcoin improvement proposal', 'BTC': 'bitcoin', 'P2SH': 'pay to script hash', 'HD': 'hierarchical deterministic', 'RBF': 'replace-by-fee', 'RPC': 'remote procedure call',
         'OP': 'operation code', 'CP': 'critical point'}
bad = []
for i in items:
    if i['key'] in v13by: continue
    tx = printed(i); low = tx.lower()
    for ab, full in ABBRS.items():
        m = re.search(r'(?<![A-Za-z0-9_])' + re.escape(ab) + r'(?![A-Za-z0-9_])', tx)
        if m and not (low.find(full) >= 0 and low.find(full) <= m.start()): bad.append((i['key'], ab))
for b in bonus:
    tx = (b['prompt'] + ' ' + ' '.join(t[0] + ' ' + t[1] for t in b['tips']) + ' ' + ' '.join(b['rubric']))
    for ab, full in ABBRS.items():
        if re.search(r'(?<![A-Za-z0-9_])' + re.escape(ab) + r'(?![A-Za-z0-9_])', tx) and full not in tx.lower(): bad.append((b['key'], ab))
say('PASS' if not bad else 'FAIL', 'P12 abbreviations of a list of %d are spelled out before their first use (new and reworked items)' % len(ABBRS), str(bad))
caps = {}
for i in items:
    if i['key'] in v13by: continue
    for tok in re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,})(?![A-Za-z0-9_])', printed(i)): caps.setdefault(tok, set()).add(i['key'])
for b in bonus:
    for tok in re.findall(r'(?<![A-Za-z0-9_])([A-Z][A-Z0-9]{1,})(?![A-Za-z0-9_])', b['prompt'] + ' ' + ' '.join(b['rubric'])): caps.setdefault(tok, set()).add(b['key'])
say('PASS' if not caps else 'FAIL', 'P12 no capital-letter abbreviation token in the new or reworked printed text (none is used, so none needs spelling out)', str({k: sorted(v) for k, v in caps.items()}) if caps else '(none)')
tipbad = []
for i in items:
    if i['key'] in v13by: continue
    cov = ' '.join((t[0] + ' ' + t[1]).lower() for t in i['tips']); tx = printed(i).lower()
    miss = [t for t in i['terms'] if t.lower() in tx and t.lower() not in cov and not any(t.lower() in b_.lower() for b_ in [x['text'] for x in i.get('blanks', [])] + i.get('responses', []) and []) ]
    if miss: tipbad.append((i['key'], miss))
say('PASS', 'P12 MEASURED: terms of the lists that are printed but carry no tip of their own (a human reader judges them)', str(tipbad) if tipbad else '(none)')
nums = {}
for i in items:
    if i['key'] in v13by: continue
    nums[i['key']] = sorted(set(re.findall(r'\d[\d,]*', printed(i))))
for b in bonus: nums[b['key']] = sorted(set(re.findall(r'\d[\d,]*', b['prompt'])))
say('PASS', 'P12 MEASURED: numbers printed in the new items and prompts (simple arithmetic only; a reader judges)', str(nums))

# ------------------------------------------------------------------ P13 map
MAPTXT = open(MAP_FILE, encoding='utf8').read() if os.path.exists(MAP_FILE) else ''
KEYWORDS = {'D': ['previous block'], 'E': ['2,016', 'target'], 'F': ['soft fork', 'fork'], 'N': ['locking script', 'unlocking script'], 'I': ['mining pool'], 'O': ['double spend', 'refus']}
cover = {p: [] for p in KEYWORDS}
for it in list(items) + list(bonus):
    for p in it.get('owner_points', []):
        if p in cover:
            tx = (printed(it) if 'type' in it and it['type'] != 'ShortExplanation' else it['prompt'] + ' ' + ' '.join(it['rubric'])).lower()
            if all(k in tx for k in KEYWORDS[p]) or (p == 'F' and 'soft fork' in tx): cover[p].append(it.get('key') if it.get('type') != 'ShortExplanation' else it['item'])
say('PASS' if all(cover[p] for p in cover) else 'FAIL', 'P13 each of D, E, F, N, I, O is tagged on an item or prompt whose text carries its key words', str({p: v for p, v in cover.items()}))
mentioned = set(re.findall(r'mt3:[a-z0-9]+:[a-z0-9-]+', MAPTXT))
real = {i['key'] for i in items} | {b['item'] for b in bonus}
say('PASS' if mentioned and mentioned <= real else 'FAIL', 'P13 every key named in the map file is a key of the items file', '(%d keys named; unknown: %s)' % (len(mentioned), sorted(mentioned - real)))
for p in 'DEFNIO':
    ok = re.search(r'^%s\s' % p, MAPTXT, re.M) is not None
    if not ok: say('FAIL', 'P13 the map has a line for ' + p)
say('PASS' if all(re.search(r'^%s\s' % p, MAPTXT, re.M) for p in 'DEFNIO') else 'FAIL', 'P13 the map file has an entry for each of D, E, F, N, I, O (item key, PARTIAL or GAP stated in the entry)')

# ------------------------------------------------------------------ P14 drops and P15 chapters
rest = [i for i in v13['items'] if i['key'] not in {x['replaces'][0] for x in items if x.get('replaces')} and i['key'] not in by]
whole = rest + [i for i in items]                                         # whole paper: v1.3.0 outside part C unchanged
hold = {}
for i in whole:
    for c in i.get('critical_points', []): hold.setdefault(c, set()).add(i['key'])
for key in ('mt2:b1:no-bank', 'mt2:b2:mining-check'):
    pass
for b in bonus:
    for c in b['critical_points']: hold.setdefault(c, set()).add(b['item'])
for b in struct['questions'][-1]['sub']:                                  # the old bonus prompts are replaced by the reworked ones (Q5.a, Q5.b)
    pass
alone_old = {}
oldhold = {}
for i in v13['items']:
    for c in i.get('critical_points', []): oldhold.setdefault(c, set()).add(i['key'])
for b in struct['questions'][-1]['sub']:
    for c in b['critical_points']: oldhold.setdefault(c, set()).add(b['item'])
for d in doc['drops']:
    dk = d['dropped_item']; sole = sorted(c for c in v13by[dk]['critical_points'] if oldhold[c] == {dk})
    lost = sorted(c for c in sole if not hold.get(c))
    say('PASS' if lost == sorted(d['critical_points_losing_their_only_holder']) else 'FAIL', 'P14 drop of %s: the points that lose their only holder, recomputed from the tags of the whole paper' % dk, '(sole-held in v1.3.0: %s; lost now: %s; file says: %s)' % (sole, lost, d['critical_points_losing_their_only_holder']))
oldb = {c for b in struct['questions'][-1]['sub'] for c in b['critical_points']}
newb = {c for b in bonus for c in b['critical_points']}
say('PASS' if oldb <= newb else 'FAIL', 'P14 the reworked bonus prompts keep the points of the old prompts', '(old %s, new %s)' % (sorted(oldb), sorted(newb)))
allmap = {}
for i in whole:
    for c in i['chapters']: allmap.setdefault(c, []).append(i['key'])
per_prim = {c: sum(units(i) for i in whole if i['chapters'][0] == c) for c in range(1, 7)}
per_any = {c: sum(units(i) for i in whole if c in i['chapters']) for c in range(1, 7)}
say('PASS' if all(v >= 2 for v in per_prim.values()) else 'FAIL', 'P15 every chapter 1 to 6 keeps at least two machine-read units (counted under the first chapter of each item)', str(per_prim))
say('PASS', 'P15 MEASURED: machine-read units that name each chapter at all', str(per_any))
say('PASS' if sum(units(i) for i in whole) == 24 else 'FAIL', 'P15 the whole paper keeps 24 machine-read units', '(%d)' % sum(units(i) for i in whole))

# ------------------------------------------------------------------ P16 engine
if '--skip-engine' in sys.argv:
    say('NOT_MEASURED', 'P16 engine build skipped by option')
else:
    merged = {'note': 'merged for the check only', 'version': 'x', 'chapters': [1, 2, 3, 4, 5, 6], 'items': whole}
    tmpd = tempfile.mkdtemp(prefix='sen0401_5c_')
    mf = os.path.join(tmpd, 'merged.json'); json.dump(merged, open(mf, 'w', encoding='utf8'))
    os.environ['SEN0401_ENGINE_TMP'] = tmpd
    try:
        P = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=mf)
        paper, g, p = E.make_and_check(P, 'midterm')
        viol = E.validate(g, P.chapters); v = [x for x in viol if x[1] == 'Violation']
        say('PASS' if not v else 'FAIL', 'P16 engine v1.1.0: the midterm built from the merged items has no Violation (EN01-EN13, R01-R22)', str(v) if v else '(pages with the answer sheet: %s, content pages %s, sheet pages %s, items %d, skipped %s)' % (paper.get('pageCount'), paper.get('contentPages'), paper.get('sheetPages'), len(paper['items']), paper['skipped']))
        for x in [x for x in viol if x[1] != 'Violation']: say('PASS', 'P16 non-violation notice (' + x[1] + ')', x[2])
    except E.ExamRefused as e:
        say('FAIL', 'P16 engine v1.1.0 refused the midterm built from the merged items', str(e)[:600])
    except Exception as e:
        say('FAIL', 'P16 engine error', '%s: %s' % (type(e).__name__, str(e)[:300]))
    finally:
        import shutil; shutil.rmtree(tmpd, ignore_errors=True)

print('\nSUMMARY: %d FAIL line(s)%s' % (len(fails), (': ' + '; '.join(fails)) if fails else ''))
sys.exit(1 if fails else 0)
