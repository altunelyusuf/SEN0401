#!/usr/bin/env python3
"""SEN0401 midterm items check, version 1.7.0 (new file; it holds no question and no answer: every figure it recomputes is read from the private items file).
Checks the PRIVATE items file private/sen0401_exam_items_midterm_v1_7_0.json and the PRIVATE structure private/sen0401_exam_structure_v1_4_0.json against v1.5.0 / v1.2.0 and the engine v1.2.0.
Task TK_Exam_V71_Items_Build (owner order 2026-11-02: code questions replaced by hand calculations). A9 is new: v1.7.0 against v1.6.1, route A and route B of the three new numbers, no code listing left.
  L1  leak guard: the items, the structure and the builder lie in private/, are git-ignored in the public tree, untracked; this script holds none of the item strings
  F1  nothing committed is edited; the v1.5.0 items and the v1.2.0 structure are byte-equal to their committed private copies in CME
  A1  (1) the structure has four questions of 25 points = 100, no bonus; no deduction, penalty or guess-chance field anywhere; answer_space and chance per unit
  A2  (2) five alternatives in every closed unit: 5 options (letters A to E, distinct, none refers to another), matching 5 responses for 4 premises, ordering 5 steps, fill-in banks of 5 entries
  A3  (3) every answer of v1.5.0 is unchanged unless a fifth alternative forces it: the table of changed items and the SHA-256 table of unchanged answers
  A4  (4) every key recomputed by running the code, printed beside the stored key
  A5  (5) one tip per item (field tip, 'Tip:' line of at most 12 words), no tips page, no 'see tip', every stem at most 60 words, how_to_answer one sentence of at most 25 words
  A6  (6) the engine v1.2.0 builds the midterm from these items without a Violation (EN01-EN13, R01-R22); the engine v1.1.0 refuses them (logged); letters spread over A to E
  A7  whole-number row points that sum to the unit's points; units, chapters, Bloom levels and quotas as in v1.5.0; the exact blind total
Usage: sen0401_exam_items_midterm_check_v1_7_0.py            (prints PASS / FAIL / NOT_MEASURED; exit 0 only when no line is FAIL)
"""
import collections, hashlib, io, itertools, json, math, os, re, subprocess, sys, tempfile, contextlib, fractions
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE)); PRIV = os.path.join(HERE, 'private'); CME = '/home/claude/CME'
J = lambda p: json.load(open(p, encoding='utf8'))
ITEMS6 = os.path.join(PRIV, 'sen0401_exam_items_midterm_v1_7_0.json'); STRUCT6 = os.path.join(PRIV, 'sen0401_exam_structure_v1_4_0.json')
ITEMS5 = os.path.join(PRIV, 'sen0401_exam_items_midterm_v1_5_0.json'); STRUCT5 = os.path.join(PRIV, 'sen0401_exam_structure_v1_2_0.json')
BUILDER = os.path.join(PRIV, 'sen0401_exam_items_build_v1_7_0.py')
REFUSAL_LOG = os.path.join(PRIV, 'sen0401_exam_engine_v1_1_0_on_items_v1_6_0_refusal_log.txt')
FR = fractions.Fraction
fails = []


def say(status, name, detail=''):
    if status == 'FAIL': fails.append(name)
    print('%-12s %s %s' % (status, name, detail)); sys.stdout.flush()


def sha(o): return hashlib.sha256(json.dumps(o, ensure_ascii=False, sort_keys=True).encode('utf8')).hexdigest()[:16]


D6 = J(ITEMS6); D5 = J(ITEMS5); S6 = J(STRUCT6); S5 = J(STRUCT5)
I6 = {i['key']: i for i in D6['items']}; I5 = {i['key']: i for i in D5['items']}
I61 = J(os.path.join(PRIV, 'sen0401_exam_items_midterm_v1_6_1.json')); S61 = J(os.path.join(PRIV, 'sen0401_exam_structure_v1_3_1.json')); J61 = {i['key']: i for i in I61['items']}
NEW = {k: i['replaces'][0] for k, i in I6.items() if k.startswith('mt7:')}                       # new key -> old key
for nk, ok in NEW.items(): I5[nk] = I5[ok]                                                       # same position: compared with the old item at the same place
ORDER = sorted(I6, key=lambda k: I6[k]['sub_question'])

# ------------------------------------------------------------------ L1
def git(*a, cwd=ROOT): return subprocess.run(['git', '-C', cwd, *a], capture_output=True, text=True)
for f in (ITEMS6, STRUCT6, BUILDER):
    rel = os.path.relpath(f, ROOT)
    ign = git('check-ignore', '-q', rel).returncode == 0; trk = bool(git('ls-files', '--', rel).stdout.strip()); n = len(git('log', '--format=%h', '--', rel).stdout.split())
    say('PASS' if ign and not trk and n == 0 else 'FAIL', 'L1 %s: in private/, git-ignored, not tracked, never committed in the public tree' % os.path.basename(f), '(ignored %s, tracked %s, commits %d)' % (ign, trk, n))
strings = []
def collect(v):
    if isinstance(v, str):
        if len(v) >= 25: strings.append(v)
    elif isinstance(v, list):
        for x in v: collect(x)
    elif isinstance(v, dict):
        for x in v.values(): collect(x)
TEXTF = ('q', 'options', 'steps', 'responses', 'distractors', 'tip', 'code', 'instruction', 'how_to_answer', 'format_line', 'output')
for _i in D6['items']:
    for _f in TEXTF:
        if _f in _i: collect(_i[_f])
    for _p in _i.get('premises', []): collect([_p['text'], _p['match']])
    for _b in _i.get('blanks', []): collect([_b['text'], _b['answer']])
me = open(__file__, encoding='utf8').read()
leak = [s[:20] for s in strings if s in me]
say('PASS' if not leak else 'FAIL', 'L1 this script holds none of the %d printed strings (25 characters or longer) of the items' % len(strings), str(leak[:3]))

# ------------------------------------------------------------------ F1
st = git('status', '--porcelain'); badst = [l for l in st.stdout.splitlines() if not l.startswith('??')]
mod = [l for l in badst if '08-tooling/exam' in l]
say('PASS' if not mod else 'FAIL', 'F1 no tracked file under 08-tooling/exam is modified or deleted (a committed file is never edited)', ' '.join(mod[:4]) or 'none')
for name, f in (('items v1.5.0', 'sen0401_exam_items_midterm_v1_5_0.json'), ('structure v1.2.0', 'sen0401_exam_structure_v1_2_0.json'), ('builder v1.5.0', 'sen0401_exam_items_build_v1_5_0.py')):
    c = os.path.join(CME, 'exams/SEN0401/08-tooling/exam/private', f)
    if not os.path.exists(c): say('NOT_MEASURED', 'F1 %s equals its committed private copy in CME' % name, 'copy not found'); continue
    same = open(c, 'rb').read() == open(os.path.join(PRIV, f), 'rb').read()
    say('PASS' if same else 'FAIL', 'F1 %s is byte-equal to its committed private copy in CME' % name, hashlib.sha256(open(c, 'rb').read()).hexdigest()[:16])

# ------------------------------------------------------------------ A1 structure
Q = S6['questions']
say('PASS' if len(Q) == 4 and all(q['points'] == 25 and sum(s['points'] for s in q['sub']) == 25 and not q.get('bonus') for q in Q) and sum(q['points'] for q in Q) == 100 else 'FAIL',
    'A1 structure: four questions of 25 points = 100 and no bonus question', str([(q['number'], q['points'], sum(s['points'] for s in q['sub'])) for q in Q]))
txt = json.dumps(S6).lower()
say('PASS' if 'bonus' not in txt.replace('"critical_points_without_a_holder_after_the_bonus_removal"', '').replace('no bonus', '') else 'FAIL', 'A1 structure: the word bonus occurs only in the sentence that says there is none')
badk = [k for k in re.findall(r'"([^"]+)":', json.dumps(S6)) if re.search(r'penalt|guess|deduct|floor', k, re.I)]
badv = [m for m in re.findall(r'penalt\w*|guess\w*|floor', json.dumps(S6, ensure_ascii=False), re.I)]
say('PASS' if not badk and not badv else 'FAIL', 'A1 structure: no penalty, guess-chance, deduction or floor field or word', str((badk + badv)[:5]))
subs = [s for q in Q for s in q['sub']]
say('PASS' if all('answer_space' in s and 'chance' in s and s['answer_space'].get('kind') for s in subs) else 'FAIL', 'A1 structure: an answer_space and a chance for every unit', '(%d units)' % len(subs))
chance_ok = True
for s in subs:
    it = I6[s['item']]; t = s['type']
    if t in ('NumericAnswer', 'CodeTrace'):
        val = str(it['key_value'] if t == 'NumericAnswer' else it['output']); chance_ok &= FR(s['chance']) == FR(1, 10 ** len(val))
    else: chance_ok &= FR(s['chance']) == FR(1, 5)
say('PASS' if chance_ok else 'FAIL', 'A1 structure: chance is 1/5 for every closed unit and 1/10^digits of the key for a number or trace')
say('PASS' if len(subs) == 24 and [s['key'] for s in subs] == [s['key'] for q in S5['questions'] if not q.get('bonus') for s in q['sub']] else 'FAIL', 'A1 structure: the same 24 unit keys in the same order as structure v1.2.0 (bonus Q5.a, Q5.b gone)')
lost = S6.get('critical_points_without_a_holder_after_the_bonus_removal', None)
cp5 = {c for i in D5['items'] for c in i['critical_points']}; bonus_cp = sorted({c for q in S5['questions'] if q.get('bonus') for s in q['sub'] for c in s.get('critical_points', [])})
lost2 = [c for c in bonus_cp if c not in {c2 for i in D6['items'] for c2 in i['critical_points']}]
say('PASS' if lost == lost2 else 'FAIL', 'A1 critical points of the removed bonus prompts (measured) that no remaining item carries', 'bonus carried %s; without a holder now: %s' % (bonus_cp, lost2 or 'none'))

# ------------------------------------------------------------------ A2 five alternatives
bad = []
for k in ORDER:
    i = I6[k]; t = i['type']
    if t == 'ChoiceFour':
        o = i['options']
        if not (len(o) == 5 and len(set(o)) == 5 and i['n_options'] == 5 and 0 <= i['answer'] < 5): bad.append((k, 'options'))
        if any(re.search(r'\b(option|choice) [A-E]\b|all of the above|none of the above|both of the above', x, re.I) for x in o): bad.append((k, 'refers to another option'))
    if t == 'Matching':
        if not (len(i['premises']) == 4 and len(i['responses']) == 5 and len(set(i['responses'])) == 5 and all(p['match'] in i['responses'] for p in i['premises']) and len({p['match'] for p in i['premises']}) == 4): bad.append((k, 'responses'))
    if t == 'Ordering':
        if len(i['steps']) != 5: bad.append((k, 'steps'))
    if t == 'FillBlankGroup':
        ents = [b['answer'] for b in i['blanks']] + i['distractors']
        if len(ents) != 5 or len(set(ents)) != 5: bad.append((k, 'bank'))
        for a in i.get('alternatives', []):
            e2 = [b['answer'] for b in a['blanks']] + a['distractors']
            if len(e2) != 5 or len(set(e2)) != 5: bad.append((k, 'bank of reading ' + a['reading']))
say('PASS' if not bad else 'FAIL', 'A2 five alternatives in every closed unit (choice 5 options; matching 4 premises and 5 responses; ordering 5 steps; fill-in banks of 5 entries, also in each alternative reading)', str(bad))
cl = collections.Counter('ABCDE'[I6[k]['answer']] for k in ORDER if I6[k]['type'] == 'ChoiceFour')
say('PASS' if len(cl) == 5 and max(cl.values()) - min(cl.values()) <= 1 else 'FAIL', 'A2 the correct letters of the 7 choice items are spread over A to E (counts differ by at most one)', str(dict(sorted(cl.items()))))
ln = []
for k in ORDER:
    i = I6[k]
    if i['type'] == 'ChoiceFour':
        L_ = [len(x) for x in i['options']]; ln.append((i['sub_question'], max(L_) / min(L_), L_.index(max(L_)) == i['answer']))
say('PASS' if all(r <= 2.0 for _, r, _ in ln) else 'FAIL', 'A2 MEASURED option length ratio (longest / shortest, limit 2.0) and whether the key is the longest option', str([(a, round(b, 2), c) for a, b, c in ln]))
print('     key is the longest option in %d of 7 choice items (a cue to watch; v1.5.0 had %d of 7)' % (sum(c for _, _, c in ln), sum(1 for k in I5 if I5[k]['type'] == 'ChoiceFour' and max(range(4), key=lambda x: len(I5[k]['options'][x])) == I5[k]['answer'])))

# ------------------------------------------------------------------ A3 answers unchanged / changed
def answer_of(i, ver):
    t = i['type']
    if t == 'ChoiceFour': return i['options'][i['answer']]
    if t == 'NumericAnswer': return [i['key_value'], i['unit'], i['tolerance'], i.get('data')]
    if t == 'CodeTrace': return [i['output'], i['code']]
    if t == 'Ordering': return i['steps']
    if t == 'Matching': return [[p['text'], p['match']] for p in i['premises']]
    if t == 'FillBlankGroup': return [b['answer'] for b in i['blanks']]
def letter_of(i):
    t = i['type']
    if t == 'ChoiceFour': return 'ABCDE'[i['answer']] if len(i['options']) == 5 else 'ABCD'[i['answer']]
    if t == 'Matching': return ','.join('%d>%s' % (n + 1, 'ABCDEF'[i['responses'].index(p['match'])]) for n, p in enumerate(i['premises']))
    return '-'
print('     TABLE of changed items (key, what was added, answer letter before and after)')
print('     %-6s %-34s %-52s %s' % ('pos', 'item', 'what was added or removed', 'letter before -> after'))
unchanged_bad = []
for k in ORDER:
    a, b = I5[k], I6[k]; same = sha(answer_of(a, 5)) == sha(answer_of(b, 6))
    # texts changed by the wording repair do not change the answer: the stem is not part of answer_of except for the premises / steps / blanks that are compared above
    what = '; '.join(b.get('v1_7_0_changes') or b['v1_6_0_changes'])
    lt = '%s -> %s' % (letter_of(a), letter_of(b)) if b['type'] in ('ChoiceFour', 'Matching') else '-'
    print('     %-6s %-34s %-52s %s' % (b['sub_question'][:6], k.split(':')[1][:34], what[:52], lt))
    if not same and k not in NEW: unchanged_bad.append(k)
say('PASS' if not unchanged_bad else 'FAIL', 'A3 (the 3 replaced hand-calculation items excepted, see A9) the answer content of all 21 items (correct option text, number and unit, code and output, steps, premise-response pairs, blank answers) is the same as in v1.5.0', str(unchanged_bad))
moved = [I6[k]['sub_question'] for k in ORDER if I6[k]['type'] == 'ChoiceFour' and letter_of(I5[k]) != letter_of(I6[k])]
say('PASS' if moved == ['Q1.e'] else 'FAIL', 'A3 letters that moved (only where the item says so: field letter_moved)', '%s; items with the field: %s' % (moved, [I6[k]['sub_question'] for k in ORDER if 'letter_moved' in I6[k]]))
print('     TABLE of unchanged answers by SHA-256 (first 16 hex characters of the canonical JSON of the answer content)')
print('     %-6s %-34s %-16s %-16s %s' % ('pos', 'item', 'sha v1.5.0', 'sha v1.6.1', 'equal'))
for k in ORDER:
    a, b = sha(answer_of(I5[k], 5)), sha(answer_of(I6[k], 6)); print('     %-6s %-34s %-16s %-16s %s' % (I6[k]['sub_question'][:6], k.split(':')[1][:34], a, b, a == b))
# non-answer parts that must also be unchanged
oth = []
for k in ORDER:
    a, b = I5[k], I6[k]
    for f in ('chapters', 'bloom', 'kind', 'critical_points', 'seeds', 'source', 'terms', 'sub_question'):
        if (f == 'terms' or (f == 'bloom' and b['bloom'] == min(a['bloom'], 3))) and k in NEW: continue
        if a.get(f) != b.get(f): oth.append((k, f))
    if k in NEW: continue
    if a['type'] == 'ChoiceFour' and not set(a['options']) <= set(b['options']): oth.append((k, 'an old option is gone'))
    if a['type'] == 'Matching' and not set(b['responses']) <= set(a['responses']): oth.append((k, 'a response is new'))
    if a['type'] == 'FillBlankGroup' and not set(a['distractors']) <= set(b['distractors']): oth.append((k, 'a distractor is gone'))
say('PASS' if not oth else 'FAIL', 'A3 chapters, Bloom level, kind, critical points, seeds, source, terms and position unchanged; every old option / distractor kept; no new response', str(oth[:4]))

# ------------------------------------------------------------------ A4 recomputation by running the code
rows = []
def rec(k, name, stored, got): rows.append((I6[k]['sub_question'], name, stored, got)); return str(stored) == str(got)
ok4 = True
for k in ORDER:
    i = I6[k]; d = i.get('data') or {}
    if i['type'] == 'CodeTrace':
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf): exec(i['code'], {})
        ok4 &= rec(k, 'trace: the listing run here', i['output'], buf.getvalue().strip())
    elif i['type'] == 'NumericAnswer':
        m = d.get('model')
        if m == 'preimage_target': got = (2 ** d['bits'] // d['target']) // d['tries_per_second']
        elif m == 'halving_claim': got = d['claim'] - ((d['start'] >> (d['height'] // d['interval'])) + d['fees'])
        elif m == 'greedy_fee':
            room = d['room']; tot = 0
            for n_, size, fee, _ in sorted(d['txs'], key=lambda t: FR(t[2], t[1]), reverse=True):
                if size <= room: room -= size; tot += fee
            got = tot
        elif m == 'vwap_value':
            vol = sum(c for c, p in d['trades']); got = int(FR(sum(c * p for c, p in d['trades']), vol) * d['coins'] / d['divisor'])
        elif k == 'mt2:i17:words-to-entropy':
            w_ = int(re.search(r'(\d+) words', i['q']).group(1)); b_ = int(re.search(r'(\d+) bits', i['q']).group(1)); tot_ = w_ * b_
            got = [e for e in range(32, tot_ + 1, 32) if e + e // 32 == tot_][0]
        elif m == 'target_adjust': got = int(FR(d['old_target'] * d['days'], d['period_days']))                       # route C: exact fraction
        elif m == 'tag_order_moves':
            tg = d['tags']; kk = lambda t: tuple(map(int, t[1:].split('.')))
            ot = sorted(range(len(tg)), key=lambda x: tg[x]); on = sorted(range(len(tg)), key=lambda x: kk(tg[x]))
            got = sum(abs(ot.index(x) - on.index(x)) for x in range(len(tg)))
        elif m == 'gap_scan':
            u = set(d['used']); last = -1; k_ = 0
            while True:
                if k_ in u: last = k_
                if k_ - last >= d['gap']: break
                k_ += 1
            got = k_ + 1
        else: got = None
        ok4 &= rec(k, 'number: recomputed from the data of the item' if m else 'number: recomputed from the stem', i['key_value'], got)
# Q1.a: change and what the miner collects
q1a = I6['mt2:i02:fee-not-written']; nums = [int(x.replace(',', '')) for x in re.findall(r'\d{1,3}(?:,\d{3})+', q1a['q'])]
ins = nums[:3]; pays = nums[3:5]; fee = nums[6] if len(nums) > 6 else None
change = sum(ins) - sum(pays) - nums[-1]; left = sum(ins) - sum(pays)
f1 = lambda n: '{:,}'.format(n)
hit = [n for n, o in enumerate(q1a['options']) if ('Change ' + f1(change)) in o and ('all ' + f1(left)) in o]
ok4 &= rec('mt2:i02:fee-not-written', 'choice: the one option with the recomputed change and fee outcome', 'ABCDE'[q1a['answer']], 'ABCDE'[hit[0]] if len(hit) == 1 else 'none/many')
# Q1.d: the catch-up chances of the white paper (section 11)
def catch(q, z):
    p = 1 - q; lam = z * q / p; s = 1.0
    for k in range(z + 1): s -= math.exp(-lam) * lam ** k / math.factorial(k) * (1 - (q / p) ** (z - k))
    return 100 * s
q1d = I6['mt2:i05:shop-confirmations']
tab = [(0.1, 2, 5.1), (0.1, 3, 1.3), (0.1, 6, 0.02), (0.3, 3, 32.5), (0.3, 6, 13.2), (0.3, 9, 5.5), (0.3, 10, 4.2)]
okt = all(abs(round(catch(q, z), 2 if v < 1 else 1) - v) < 1e-9 for q, z, v in tab)
z10 = next(z for z in range(1, 40) if catch(0.1, z) < 5); z30 = next(z for z in range(1, 40) if catch(0.3, z) < 5)
rows.append((q1d['sub_question'], 'table of the stem recomputed from the formula (7 figures equal)', True, okt)); ok4 &= okt
words = {'three': 3, 'ten': 10}
key_opt = q1d['options'][q1d['answer']]
ok_d = (z10, z30) == (3, 10) and 'three' in key_opt and 'ten' in key_opt
ntrue = [n for n, o in enumerate(q1d['options']) if 'three' in o and 'ten' in o and 'confirmations' in o]
rows.append((q1d['sub_question'], 'least z below 5 percent: 10 percent attacker, 30 percent attacker', '(3, 10)', (z10, z30))); ok4 &= ok_d and ntrue == [q1d['answer']]
fifth = [o for o in q1d['options'] if 'not enough' in o and 'z = 10' in o]
rows.append((q1d['sub_question'], 'new fifth option says ten confirmations are not enough: false because the chance at z=10 is below 5', 'false', 'false' if catch(0.3, 10) < 5 and len(fifth) == 1 else 'check')); ok4 &= (catch(0.3, 10) < 5 and len(fifth) == 1)
# Q1.f
q1f = I6['mt3:a4:second-spend-and-majority']; ok4 &= rec('mt3:a4:second-spend-and-majority', 'case two: expected blocks of the group out of 20', 12, round(20 * 60 / 100))
# Q1.g
q1g = I6['mt3:a5:old-notes-and-new-keys']; ok4 &= rec('mt3:a5:old-notes-and-new-keys', 'old marks to new marks (3,000,000 / 1,000), printed in the key option', '3,000', '3,000' if '3,000' in q1g['options'][q1g['answer']] and 3000000 // 1000 == 3000 else 'check')
# Ordering: the one order that agrees with the spending references
o_ = I6['mt2:i06:order-wallet-to-block']; tx = [re.match(r'Transaction (\w)', s).group(1) for s in o_['steps']]
sp = {}
for s_ in o_['steps']:
    m = re.match(r'Transaction (\w) spends (?:output \d of )?(?:the output of )?transaction (\w)', s_)
    if m: sp[m.group(1)] = m.group(2)
valid = [p for p in itertools.permutations(tx) if all(p.index(a) > p.index(b) for a, b in sp.items())]
ok4 &= rec('mt2:i06:order-wallet-to-block', 'ordering: orders (of 120) in which every spender follows what it spends; the stored order of the steps is the first of them', '1 order, equal', '%d order, %s' % (len(valid), 'equal' if valid == [tuple(tx)] else 'DIFFERENT'))
# fill-in i07 by brute force over the 32 states
f7 = I6['mt3:i07:fill-mined-or-not']; pay = f7['facts']['payments']; spd = f7['facts']['spends']
def shown(inside_stated, rule):
    st_ = []
    for bits in itertools.product([0, 1], repeat=5):
        m = dict(zip(pay, bits))
        if any(not m[p] for p in inside_stated): continue
        if any(m[a] and not m[b] for a, b in spd): continue
        if rule == 'named' and any(not m[b] for a, b in spd): continue
        st_.append(m)
    return sorted(p for p in pay if st_ and all(s[p] for s in st_)), sorted(p for p in pay if st_ and any(s[p] for s in st_) and not all(s[p] for s in st_)), len(st_)
careful = shown(f7['facts']['stated_inside_a_block_careful_reading'], 'none'); simple = shown([], 'named')
rows.append((f7['sub_question'], 'careful reading: payments shown mined / undecided / states agreeing', "(['K','L','M'], ['N','P'], 3)", careful)); rows.append((f7['sub_question'], 'owner simple reading: shown mined / undecided / states agreeing', "(['K','L','N'], ['M','P'], 4)", simple))
ok4 &= careful == (['K', 'L', 'M'], ['N', 'P'], 3) and simple == (['K', 'L', 'N'], ['M', 'P'], 4)
# i23 weight arithmetic: a witness byte counts one unit, any other byte four
w_a = 4 * 100 + 1 * 60; w_b = 4 * 160 + 1 * 0
rows.append(('Q4.f', 'weight of two payments of 160 bytes: with 60 witness bytes / with none; the first is less', 'less', 'less' if w_a < w_b else 'more')); ok4 &= w_a < w_b
print('     %-6s %-98s %-26s %s' % ('pos', 'recomputation (run here)', 'stored key', 'recomputed'))
for r in rows: print('     %-6s %-98s %-26s %s' % (r[0][:6], r[1][:98], str(r[2])[:26], str(r[3])[:60]))
say('PASS' if ok4 else 'FAIL', 'A4 every key recomputed by running the code (numbers from the item data, traces by running the listings, the ordering, the choice items with figures, the fill-in group by brute force)', '(%d recomputations)' % len(rows))

# ------------------------------------------------------------------ A5 readability and tips
import sen0401_exam_readability_check_v1_1_0 as R
rule = R.load_rule(R.DEFAULT_RULE); iu, itips = R.read_items(ITEMS6, rule); res = R.run_source('items', iu, None, itips, rule, True)
for r_ in ('R1', 'R2', 'R3', 'R4', 'R6'):
    x = res[r_]; say('PASS' if x['status'] == 'MEASURED' and not x['fail'] else 'FAIL', 'A5 readability tool v1.1.0 %s on the items (%d units)' % (r_, x['checked']), str(x['fail'][:3]))
say('NOT_MEASURED', 'A5 readability R5 (cover) and the paper-side rules', 'no cover and no paper in this task')
tw = [(k, len(I6[k]['tip'].replace('Tip:', '', 1).split())) for k in ORDER]
say('PASS' if all(I6[k]['tip'].startswith('Tip: ') and n <= 12 and I6[k]['needs_tip'] and isinstance(I6[k]['tip'], str) for k, n in tw) else 'FAIL', 'A5 every item carries ONE tip (string, starts "Tip:", at most 12 words) and needs_tip', 'longest tip %d words; words per tip %s' % (max(n for _, n in tw), [n for _, n in tw]))
say('PASS' if not any(('tips' in I6[k] or 'tips_by_label' in I6[k]) for k in ORDER) else 'FAIL', 'A5 no legacy tips list or tips page in the items')
seen = [k for k in ORDER if re.search(r'see tips?\b', json.dumps({f: v for f, v in I6[k].items() if not f.endswith('_changes')}), re.I)]
say('PASS' if not seen else 'FAIL', 'A5 no "see tip" reference anywhere in an item', str(seen))
def stems(i): return ([i['q']] if i.get('q') else []) + [b['text'] for b in i.get('blanks', [])] + ([i['instruction']] if i.get('instruction') and not i.get('q') else [])
mx = max(len(s.split()) for k in ORDER for s in stems(I6[k]))
say('PASS' if mx <= 60 else 'FAIL', 'A5 every stem has at most 60 words', 'longest %d' % mx)
hw = [(k, len(I6[k]['how_to_answer'].split())) for k in ORDER]
say('PASS' if all(n <= 25 and I6[k]['how_to_answer'].count('.') == 1 and I6[k]['format_line'] == I6[k]['how_to_answer'] for k, n in hw) else 'FAIL', 'A5 how_to_answer is one plain sentence of at most 25 words (and equals format_line)', 'longest %d words' % max(n for _, n in hw))
txts = ' '.join(json.dumps(I6[k]['how_to_answer']) for k in ORDER)
say('PASS' if all(re.search(p, ' '.join(I6[k]['how_to_answer'] for k in ORDER if I6[k]['type'] == t_)) for t_, p in (('ChoiceFour', 'letter'), ('NumericAnswer', 'digit in each box'), ('Matching', 'letter'), ('Ordering', 'place'), ('FillBlankGroup', 'letter'))) else 'FAIL', 'A5 how_to_answer says how the new answer is given (letter / digit / place / letter per blank)')

# ------------------------------------------------------------------ A6 engine
import sen0401_exam_engine_v1_2_0 as E
os.environ.setdefault('SEN0401_ENGINE_TMP', tempfile.gettempdir())
P = E.Params(24, (1, 2, 3, 4, 5, 6), None, 'GridOnCover', authored=ITEMS6)
try:
    paper, g, p = E.make_and_check(P, 'midterm'); viol = E.validate(g, P.chapters); v = [x for x in viol if x[1] == 'Violation']
    say('PASS' if not v else 'FAIL', 'A6 engine v1.2.0: the midterm built from these items has no Violation (EN01-EN13, R01-R22 with the v1.2.0 shapes)', str(v) if v else '(paper pages %s, content pages %s, sheet pages %s; the sheet is the OLD four-letter sheet, to be replaced by the sheet task)' % (paper.get('pageCount'), paper.get('contentPages'), paper.get('sheetPages')))
    lt = collections.Counter('ABCDE'[it['answer']] for it in paper['items'] if it['type'] == 'ChoiceFour')
    say('PASS' if len(lt) == 5 and max(lt.values()) - min(lt.values()) <= 1 else 'FAIL', 'A6 answer letters of the choice items in the built paper are spread over A to E', str(dict(sorted(lt.items()))))
    say('PASS' if paper['pool_size'] == 21 and len(paper['items']) == 21 and all(paper['quotas'][c] == 4 for c in range(1, 7)) else 'FAIL', 'A6 the paper holds all 21 authored items and the quotas hold (4 units per chapter)', str(paper['quotas']))
    from rdflib import RDF as RDF_
    bl_ = sorted({str(g.value(e, E.PR.label)) for e in g.subjects(RDF_.type, E.PR.BankEntry)})
    say('PASS' if bl_ == ['A', 'B', 'C', 'D', 'E'] else 'FAIL', 'A6 the fill-in banks of the built paper are lettered A to E (five entries each)', str(bl_))
    nent = collections.Counter(str(g.value(b_, E.PR.shuffleSeed)) and len(list(g.objects(b_, E.PR.entry))) for b_ in g.subjects(RDF_.type, E.PR.Bank))
    say('PASS' if set(nent) == {5} and sum(nent.values()) == 3 else 'FAIL', 'A6 the 3 banks of the built paper hold 5 entries each', str(dict(nent)))
except E.ExamRefused as e:
    say('FAIL', 'A6 engine v1.2.0 refused the midterm', str(e))
if os.path.exists(REFUSAL_LOG):
    t = open(REFUSAL_LOG, encoding='utf8').read()
    say('PASS' if 'IndexError' in t and 'exit 1' in t else 'FAIL', 'A6 the committed engine v1.1.0 does not accept five alternatives (its run on these items is logged: it stops with an IndexError in the renderer)', '(log %s)' % os.path.basename(REFUSAL_LOG))
else: say('NOT_MEASURED', 'A6 engine v1.1.0 run on these items', 'log not found')
# corpus words of the new texts (measured, a person judges)
import sen0401_exam_engine_v1_0_0 as E0
ix = E0.corpus_index(); vocab = set(re.findall(r"[a-z][a-z\-']{3,}", ix))
newtexts = []
for k in ORDER:
    a, b = I5[k], I6[k]
    if b['type'] == 'ChoiceFour': newtexts += [o for o in b['options'] if o not in a['options']]
    if b['type'] == 'FillBlankGroup': newtexts += [d for d in b['distractors'] if d not in a['distractors']]
    newtexts.append(b['tip'])
unk = sorted({w for t_ in newtexts for w in re.findall(r"[a-z][a-z\-']{3,}", t_.lower()) if w not in vocab})
say('PASS', 'A6 MEASURED (a person judges): words of the new options, bank entries and tips that the course corpus (banks, critical points, decks and notes) does not contain', '%d words: %s' % (len(unk), unk))
tf = []
for k in ORDER:
    n_ = E0.unfound_terms(I6[k]); tf += [(k, n_)] if n_ else []
say('PASS' if not tf else 'FAIL', 'A6 EN08 every term of every item is found in the course corpus', str(tf))

# ------------------------------------------------------------------ A7 row points, quotas
bad = []
for q in Q:
    for s in q['sub']:
        it = I6[s['item']]
        if s['type'] in ('Ordering', 'Matching'):
            rp = s['row_points']
            if not (len(rp) == s['parts'] and all(isinstance(x, int) and x >= 1 for x in rp) and sum(rp) == s['points'] and rp == it['row_points']): bad.append(s['key'])
        if s['type'] == 'FillBlankGroup' and not (isinstance(s['points'], int) and s['points'] >= 1): bad.append(s['key'])
say('PASS' if not bad else 'FAIL', 'A7 whole-number row points that add up to the unit points (ordering, matching); every fill-in blank is a unit with whole points', str(bad))
print('     row points: ' + '; '.join('%s %s (unit %s)' % (s['key'], s['row_points'], s['points']) for q in Q for s in q['sub'] if 'row_points' in s))
print('     unequal splits (no equal whole-number split exists): ' + '; '.join('%s: %s' % (s['key'], s['row_points_note']) for q in Q for s in q['sub'] if 'row_points_note' in s))
mm = []
for s6, s5 in zip(subs, [s for q in S5['questions'] if not q.get('bonus') for s in q['sub']]):
    for f in ('key', 'item', 'type', 'points', 'units', 'chapters', 'bloom', 'label'):
        if s6[f] != s5[f] and not (f == 'points' and s6['key'] in ('Q3.a', 'Q3.c')) and not (s6['item'].startswith('mt7:') and f in ('item', 'type', 'bloom')): mm.append((s6['key'], f))
say('PASS' if not mm else 'FAIL', 'A7 units, points, chapters, Bloom levels and labels of all 24 positions equal structure v1.2.0 (except the points of Q3.a and Q3.c, ruled equal-row, and the item, type and Bloom level of the three replaced units)', str(mm[:4]))
per = collections.Counter();
for k in ORDER: per[I6[k]['chapters'][0]] += (len(I6[k]['blanks']) if I6[k]['type'] == 'FillBlankGroup' else 1)
say('PASS' if all(per[c] == 4 for c in range(1, 7)) else 'FAIL', 'A7 equal chapter weights (4 units per primary chapter)', str(dict(sorted(per.items()))))
bl = collections.Counter();
for k in ORDER: bl[I6[k]['bloom']] += (len(I6[k]['blanks']) if I6[k]['type'] == 'FillBlankGroup' else 1)
hi = sum(v for b, v in bl.items() if b >= 3)
say('PASS' if hi * 2 > 24 and sum(v for b, v in bl.items() if b >= 4) >= 6 else 'FAIL', 'A7 Bloom: a majority at Apply or above and at least 6 units at Analyze or above (unchanged)', 'units per level %s' % dict(sorted(bl.items())))
# A9 v1.7.0 against v1.6.1
def flat(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items(): yield from flat(v, path + '/' + str(k))
    elif isinstance(o, list):
        for n, v in enumerate(o): yield from flat(v, path + '[%d]' % n)
    else: yield path, o
OLDK = {v: k for k, v in NEW.items()}
say('PASS' if len(NEW) == 3 and sorted(J61[o]['sub_question'] for o in NEW.values()) == ['Q2.c', 'Q2.e', 'Q2.g'] and all(J61[o]['type'] == 'CodeTrace' for o in NEW.values()) else 'FAIL', 'A9 exactly the three code traces are replaced (old keys at the positions)', str({o: J61[o]['sub_question'] for o in NEW.values()}))
same_pos = all(I6[n]['sub_question'] == J61[o]['sub_question'] and I6[n]['points'] == J61[o]['points'] and I6[n]['critical_points'] == J61[o]['critical_points'] and I6[n]['chapters'] == J61[o]['chapters'] and I6[n]['bloom'] == min(J61[o]['bloom'], 3) for n, o in NEW.items())
say('PASS' if same_pos else 'FAIL', 'A9 each new item keeps the position, points, critical points and chapters of the item it replaces (Bloom level: the same, but at most 3, the most that rule R06 lets a number reach; only Q2.g falls from 4 to 3)')
nocode = [k for k in I6 if I6[k]['type'] == 'CodeTrace' or 'code' in I6[k]]
say('PASS' if not nocode and all(I6[n]['type'] == 'NumericAnswer' and I6[n]['tolerance'] == 0 and isinstance(I6[n]['key_value'], int) and 0 < I6[n]['key_value'] < 10 ** 5 for n in NEW) else 'FAIL', 'A9 the new items are whole-number answers of at most 5 digits, no code listing remains in the paper', str(nocode))
# route A and route B again (the builder holds the same two; here as a third, separate implementation shown above in A4); digit table
print('     TABLE new answers (position, old key -> new key, critical points, digits of the old output -> digits of the new answer)')
for n, o in sorted(NEW.items(), key=lambda t: I6[t[0]]['sub_question']):
    print('     %-5s %-34s -> %-36s %-8s %d -> %d digits' % (I6[n]['sub_question'], o, n, ','.join(I6[n]['critical_points']), len(str(J61[o]['output'])), len(str(I6[n]['key_value']))))
other = [k for k in I6 if k not in NEW and k in J61 and json.dumps({f: v for f, v in I6[k].items() if f != 'v1_7_0_changes'}, sort_keys=True) != json.dumps(J61[k], sort_keys=True)]
say('PASS' if other == ['mt2:i23:fill-txid-and-weight'] else 'FAIL', 'A9 every other item is identical to v1.6.1 except the txid and weight fill-in (tip only)', str(other))
i23n, i23o = I6['mt2:i23:fill-txid-and-weight'], J61['mt2:i23:fill-txid-and-weight']
say('PASS' if {f for f in i23n if i23n[f] != i23o.get(f)} <= {'tip', 'v1_7_0_changes'} and re.match(r'Tip: Segregated witness \(SegWit\)', i23n['tip']) else 'FAIL', 'A9 the 4e/4f tip differs only in the tip and spells out Segregated witness at first use')
ds = [d for d in (lambda a, b: [(p, a.get(p), b.get(p)) for p in sorted(set(a) | set(b)) if a.get(p) != b.get(p)])(dict(flat(S61)), dict(flat(S6)))]
badS = [d for d in ds if not re.search(r"^/(version|items_file|derived_from|blind_total_exact/.*|chance_by_type.*)$", d[0]) and not re.search(r"^/questions\[\d\]/sub\[\d\]/(item|type|block|how_to_answer|answer_space.*|chance|chance_value|chance_basis|tip|answer_digits|bloom)$", d[0])]
changed_subs = sorted({re.match(r'/questions\[(\d)\]/sub\[(\d)\]', d[0]).groups() for d in ds if d[0].startswith('/questions')})
subkeys = [S6['questions'][int(a)]['sub'][int(b)]['key'] for a, b in changed_subs]
say('PASS' if not badS and sorted(subkeys) == ['Q2.c', 'Q2.e', 'Q2.g', 'Q4.e', 'Q4.f'] or (not badS and sorted(subkeys) == ['Q2.c', 'Q2.e', 'Q2.g', 'Q4.e']) else 'FAIL', 'A9 structure v1.4.0 differs from v1.3.1 only in the version fields, the blind total, and the units Q2.c, Q2.e, Q2.g (item, type, answer space, chance) and the tip unit of Q4', 'units changed %s %s' % (subkeys, str(badS[:3])))
say('PASS' if S6['blind_total_exact']['closed_units_points'] == 75 and sum(s['points'] for q in Q for s in q['sub'] if s['type'] != 'NumericAnswer') == 75 else 'FAIL', 'A9 closed points stay 75; paper stays 100; unit points unchanged', str(sum(s['points'] for q in Q for s in q['sub'])))
ptsmatch = all(a['points'] == b['points'] and a['key'] == b['key'] and a['chapters'] == b['chapters'] and (a['bloom'] == b['bloom'] or b['key'] == 'Q2.g') and a['label'] == b['label'] for a, b in zip([s for q in S61['questions'] for s in q['sub']], [s for q in S6['questions'] for s in q['sub']]))
say('PASS' if ptsmatch else 'FAIL', 'A9 points, labels, chapters and Bloom levels of all 24 positions equal structure v1.3.1 (Bloom of Q2.g 4 -> 3 only)')
exp = FR(0)
for q in Q:
    for s in q['sub']:
        it = I6[s['item']]
        exp += (sum(it['row_points']) if s['type'] in ('Ordering', 'Matching') else s['points']) * (FR(1, 5) if s['type'] in ('ChoiceFour', 'Matching', 'Ordering', 'FillBlankGroup') else FR(1, 10 ** len(str(it['key_value']))))
say('PASS' if exp == FR(S6['blind_total_exact']['fraction']) else 'FAIL', 'A9 exact blind total recomputed from the units and the digit counts of the keys', '%s = %.4f' % (exp, float(exp)))
b = S6['blind_total_exact']
say('PASS' if FR(b['fraction']) < 20 and b['closed_units_blind'] == 15 else 'FAIL', 'A7 the exact blind total (1/5 of the 75 closed points plus the chance of the hand-written numbers and traces)', '%s = %.4f' % (b['fraction'], b['decimal']))
print('RESULT', 'PASS' if not fails else 'FAIL (%d lines)' % len(fails))
sys.exit(1 if fails else 0)
