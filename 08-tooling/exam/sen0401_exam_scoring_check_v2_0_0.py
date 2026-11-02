"""Check of the scoring rule file and the scoring module, version 2.0.0 (new file; the v1_0_0 and v1_1_0 checks stay). Holds no question and no answer: every fixture is synthetic.
Usage: check.py RULE.json --shape V6KEY.json [--blind 20000] [--seed 80001]
  --shape reads ONLY the shape of the v6 key (unit types, row counts, points, digit counts of the number places); the bonus units are dropped, the closed units become five-way units, number and trace values are replaced by synthetic values of the same digit count. No answer of the v6 key is copied or printed.
Prints PASS / FAIL per check; exit 1 on any FAIL."""
import argparse, fractions, json, math, os, random, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_scoring_v2_0_0 as S
F = fractions.Fraction
ap = argparse.ArgumentParser(); ap.add_argument('rule'); ap.add_argument('--shape', required=True); ap.add_argument('--blind', type=int, default=20000); ap.add_argument('--seed', type=int, default=80001)
args = ap.parse_args(); res = []
def rep(name, ok, detail=''):
    res.append(bool(ok)); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)

def synth():
    """Synthetic key of 100 points, five-way closed units."""
    it = []
    for i, a in enumerate('ACE'): it.append(dict(label='c%d' % (i + 1), question=1, type='ChoiceFive', points=5, answer={'c%d' % (i + 1): a}))
    it.append(dict(label='m', question=2, type='Matching', points=20, points_per_part=5, answer={'m1': 'D', 'm2': 'B', 'm3': 'E', 'm4': 'A'}))
    it.append(dict(label='o', question=3, type='Ordering', points=20, points_per_part=4, answer={'o1': 1, 'o2': 2, 'o3': 4, 'o4': 5, 'o5': 3}))
    it.append(dict(label='b', question=4, type='FillBlankGroup', points=20, points_per_blank={'b1': 10, 'b2': 10}, bank_codes=['45', '37', '21', '12', '58'], answer={'b1': '45', 'b2': '37'}))
    for l, v in (('n1', 7), ('n2', 42), ('n3', 174)): it.append(dict(label=l, question=5, type='NumericAnswer', points=5, answer={l: dict(value=v, unit='u', tolerance=5)}))
    it.append(dict(label='t1', question=5, type='CodeTrace', points=5, answer={'t1': '5'}))
    it.append(dict(label='t2', question=5, type='CodeTrace', points=5, answer={'t2': '15'}))
    return dict(items=it)
K = synth()

# S1 rule file equals the module's table, and carries no penalty arithmetic
rule = json.load(open(args.rule)); calc = S.rule_table()
rep('S1 the rule file equals the table the module computes (%d answer types)' % len(calc['answer_types']), json.dumps(rule, sort_keys=True) == json.dumps(calc, sort_keys=True))
txt = json.dumps(rule).lower()
rep('S1b the rule file has no penalty fraction, floor or bonus field (penalty/floor/bonus are all stated as none)', 'penalty_fraction' not in txt and 'lambda' not in txt and rule['penalty'].startswith('none') and rule['floor'].startswith('none') and rule['bonus'].startswith('none'))
# S2 exact chances
ty = {t['id']: F(t['blind_chance_exact']) for t in rule['answer_types']}
ok = ty['choice_5'] == ty['matching_5'] == ty['ordering_5'] == ty['fill_bank_5'] == F(1, 5) and all(ty['number_or_trace_%d_digits' % d] == F(1, 10 ** d) for d in range(1, 6))
rep('S2 exact blind chances: choice, matching row, ordering place, fill-in blank each 1/5; number or trace 1/10^digits', ok, ', '.join('%s %s' % (k, v) for k, v in ty.items()))

# S3 fixtures of known answer
pm = S.perfect_marks(K); allwrong = {'c1': 'B', 'c2': 'B', 'c3': 'B', 'm1': 'A', 'm2': 'A', 'm3': 'A', 'm4': 'C', 'o1': 2, 'o2': 1, 'o3': 5, 'o4': 3, 'o5': 4, 'b1': '37', 'b2': '45', 'n1': 8, 'n2': 41, 'n3': 175, 't1': '6', 't2': '16'}
rp = S.score(pm, K); rb = S.score({}, K); rw = S.score(allwrong, K); rd = S.score({l: S.DOUBLE for l in pm}, K)
rep('S3a all right = 100 (of %s)' % rp['max_total'], rp['total'] == 100.0 and rp['max_total'] == 100.0 and rp['counts']['right'] == len(pm), str(rp['counts']))
rep('S3b all blank = 0', rb['total'] == 0.0 and rb['counts']['blank'] == len(pm), str(rb['counts']))
rep('S3c all wrong = 0 (every place answered, none right; nothing is negative)', rw['total'] == 0.0 and rw['counts']['wrong'] == len(pm) and all(v == 0.0 for v in rw['per_mark'].values()), str(rw['counts']))
rep('S3d two answers in every place = 0', rd['total'] == 0.0 and rd['counts']['double'] == len(pm))
one = dict(pm); one['c1'] = S.DOUBLE; one['m2'] = S.DOUBLE
rep('S3e two answers in one place cost only that place: two double places give 100 - 5 - 5 = 90, no penalty', S.score(one, K)['total'] == 90.0)
# hand-worked mixed sheet: c1 right 5; c2 wrong 0; c3 blank; m1 m2 right 10, m3 wrong, m4 blank; o1 o2 o3 right 12, o4 o5 swapped; b1 right 10, b2 wrong; n1 right 5, n2 wrong, n3 right 5; t1 DOUBLE 0; t2 right 5
mixed = {'c1': 'A', 'c2': 'D', 'c3': None, 'm1': 'D', 'm2': 'B', 'm3': 'A', 'm4': None, 'o1': '1', 'o2': '2', 'o3': '4', 'o4': '3', 'o5': '5', 'b1': '45', 'b2': '12', 'n1': '7', 'n2': '41', 'n3': '174', 't1': S.DOUBLE, 't2': '15'}
rm = S.score(mixed, K); hand = 5 + 10 + 12 + 10 + 5 + 5 + 5
rep('S3f one hand-worked mixed sheet: 5 + 10 + 12 + 10 + 5 + 5 + 5 = %d' % hand, rm['total'] == float(hand) == 52.0, 'module %s, counts %s' % (rm['total'], rm['counts']))
rep('S3g numbers are exact: 174 right, 175 and 173 and 17 wrong, "174.0" equals 174, the tolerance field of the key (5) is not read', [S.score({'n3': v}, K)['total'] for v in ('174', '175', '173', '17', '174.0')] == [5.0, 0.0, 0.0, 0.0, 5.0])
K2 = json.loads(json.dumps(K))
for it in K2['items']: it.update(guess_chance=0.9, penalty_fraction=0.9)
K2['scoring'] = dict(penalty_fraction='1/3', total_floor=0)
rep('S3h the structure\'s penalty fields are never read: the same sheets score the same with guess_chance and penalty_fraction set to 0.9', all(S.score(m, K2)['total'] == S.score(m, K)['total'] for m in (mixed, allwrong, pm, {})))
try: S.score({}, dict(items=[dict(label='x', question=1, type='ShortExplanation', points=5, answer=None)])); bonus_ok = False
except ValueError: bonus_ok = True
rep('S3i a bonus or hand-marked item is refused (the bonus is removed)', bonus_ok)
pg, sh = {'c1': 'B', 'c2': None, 'c3': S.DOUBLE}, {'c1': 'A', 'c2': 'C', 'c3': 'E'}
mr, src = S.resolve(pg, sh)
rep('S3j the question page is the legal copy: page answer or two-answer on the page wins, a place the page leaves empty takes the sheet', mr == {'c1': 'B', 'c2': 'C', 'c3': S.DOUBLE} and src == {'c1': 'page', 'c2': 'sheet', 'c3': 'page'})

# S4 the v6 shape key -> synthetic five-way key
v6 = json.load(open(args.shape)); items = []; shape = {}
letters = 'ABCDE'; ci = 0
for it in v6['items']:
    t = it['type']
    if t == 'ShortExplanation': continue
    labs = list(it['answer'].keys()); n = len(labs); shape[t] = shape.get(t, 0) + 1
    if t.startswith('Choice'): items.append(dict(label=it['label'], question=it['question'], type='ChoiceFive', points=it['points'], answer={labs[0]: letters[ci % 5]})); ci += 1
    elif t == 'Matching': items.append(dict(label=it['label'], question=it['question'], type=t, points=it['points'], points_per_part=it['points_per_part'], answer={l: 'ABCDE'[(i * 2 + 1) % 5] for i, l in enumerate(labs)}))
    elif t == 'Ordering': items.append(dict(label=it['label'], question=it['question'], type=t, points=it['points'], points_per_part=it['points_per_part'], answer={l: i + 1 for i, l in enumerate(labs)}))
    elif t == 'FillBlankGroup': codes = ['11', '22', '33', '44', '55']; items.append(dict(label=it['label'], question=it['question'], type=t, points=it['points'], points_per_blank=dict(it['points_per_blank']), bank_codes=codes, answer={l: codes[i] for i, l in enumerate(labs)}))
    else:
        a = it['answer'][labs[0]]; d = S.key_digits(a['value'] if isinstance(a, dict) else a); v = '7' * d
        items.append(dict(label=it['label'], question=it['question'], type=t, points=it['points'], answer={labs[0]: (dict(value=int(v), unit='u', tolerance=0) if t == 'NumericAnswer' else v)}))
V = dict(items=items); ms = S.marks_of_key(V); digs = sorted(S.key_digits(m['answer']) for m in ms if m['rule_type'] == 'number_or_trace')
rep('S4a synthetic key of the v6 shape: %d units %s, %d places, %s points, digit counts of the number and trace places %s' % (len(items), dict(sorted(shape.items())), len(ms), sum((m['points'] for m in ms), F(0)), digs), sum((m['points'] for m in ms), F(0)) == 100 and len(items) == len(v6['items']) - sum(1 for i in v6['items'] if i['type'] == 'ShortExplanation'))
rep('S4b a perfect sheet of the shaped key = 100; a blank = 0', S.score(S.perfect_marks(V), V)['total'] == 100.0 and S.score({}, V)['total'] == 0.0)

# S5 exact blind figure
e = S.expected_blind(V)
print('     closed points %s = %.6f; closed units blind: %s = %.6f (exactly 1/5 of the closed points: %s)' % (e['closed_points'], float(e['closed_points']), e['closed'], float(e['closed']), e['closed'] == e['closed_points'] / 5))
print('     number and trace places blind: %s = %.10f' % (e['number_and_trace'], float(e['number_and_trace'])))
print('     EXACT EXPECTED BLIND TOTAL: %s = %.10f of %s' % (e['total'], float(e['total']), e['max_points']))
rep('S5a the closed units alone give exactly 1/5 of their points blind', e['closed'] == e['closed_points'] / 5)
rep('S5b the exact blind total is the closed fifth plus the number and trace chance, and is below 20 because only 75 of 100 points are closed: %s < 20' % ('%.6f' % float(e['total'])), e['total'] == e['closed'] + e['number_and_trace'] and e['total'] < 20 and e['total'] > e['closed'])
# S6 simulation
rng = random.Random(args.seed); n = args.blind; tot = []; cl = []; mn = 1e9
closed_labels = [m['label'] for m in ms if m['rule_type'] != 'number_or_trace']
for _ in range(n):
    r = S.score(S.blind_marks(V, rng), V); tot.append(r['total']); cl.append(sum(r['per_mark'][l] for l in closed_labels)); mn = min(mn, r['total'])
def stat(x): m = sum(x) / len(x); sd = math.sqrt(sum((v - m) ** 2 for v in x) / (len(x) - 1)); return m, sd / math.sqrt(len(x)), sd
mt, se, sd = stat(tot); mc, sec, _ = stat(cl)
print('     simulation of %d blind sheets (seed %d): mean total %.4f, standard error %.4f, sd %.3f, min %.2f' % (n, args.seed, mt, se, sd, mn))
dz = abs(mt - float(e['total'])) / se
rep('S6a simulated mean total agrees with the exact figure within three standard errors (%.2f SE)' % dz, n >= 20000 and dz <= 3, 'exact %.4f, simulated %.4f' % (float(e['total']), mt))
dc = abs(mc - float(e['closed'])) / sec
rep('S6b simulated closed-unit mean agrees with exactly 1/5 of the closed points within three standard errors (%.2f SE)' % dc, dc <= 3, 'exact %.4f, simulated %.4f' % (float(e['closed']), mc))
rep('S6c no blind sheet scored below 0', mn >= 0)
# S7 control of the check itself: the 3 SE test can fail
wrong_claim = 20.0
rep('S7 control: claiming a blind total of exactly 20 for this shape would FAIL the three-standard-error test (%.1f SE)' % (abs(mt - wrong_claim) / se), abs(mt - wrong_claim) / se > 3)
print('RESULT: %d of %d checks PASS' % (sum(res), len(res))); sys.exit(0 if all(res) else 1)
