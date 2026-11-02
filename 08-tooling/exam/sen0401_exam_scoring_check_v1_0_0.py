"""Check of the scoring rule file and the scoring module (new file). Holds no question and no answer: the fixtures are synthetic. Prints PASS / FAIL per check; exit 1 on any FAIL.
  S1 the rule file equals the table the module computes (nothing typed by hand)
  S2 exact arithmetic: choice of four p = 1/4 and penalty 1/3; for every type whose penalty is not zero the expected blind share under the derived penalty is exactly 0; the zero-penalty types are the negligible ones
  S3 fixtures of known answer: the score of hand-worked marks equals the hand-worked value (right, wrong, blank, two answers, per-mark penalty, tolerance, hand-marked bonus)
  S4 a perfect sheet scores 100 (synthetic key) and, when --key is given, the full points of that key
  S5 blind guesses simulated N times (default 20000) per item of every answer type average within 0.02 of ZERO of the item's points
  S6 control of the check itself: with the penalty set to 1/4 the choice item's blind mean is about 0.0625 and the S5 criterion would FAIL it (so the criterion can fail)
  S7 the resolve rule (sheet versus question page) on fixtures
  S8 the table of alternatives printed (no penalty, 1/4, 1/3, 1/2) per answer type, and for the real key when --key is given (points only)
Usage: check.py RULE.json [--key KEY.json] [--n 20000] [--seed 60001]"""
import argparse, fractions, json, os, random, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_scoring_v1_0_0 as S
F = fractions.Fraction
ap = argparse.ArgumentParser(); ap.add_argument('rule'); ap.add_argument('--key'); ap.add_argument('--n', type=int, default=20000); ap.add_argument('--seed', type=int, default=60001)
args = ap.parse_args(); res = []
def rep(name, ok, detail=''):
    res.append(bool(ok)); print('%s  %s %s' % ('PASS' if ok else 'FAIL', name, detail), flush=True)

def synth():
    """Synthetic key (letters and digits invented for the test; the items are not exam items). Total 100 points."""
    it = []
    for i, a in enumerate('ABC'): it.append(dict(label='c%d' % (i + 1), question=1, type='ChoiceFour', points=5, answer={'c%d' % (i + 1): a}))
    it.append(dict(label='m', question=2, type='Matching', points=20, points_per_part=5, answer={'m1': 'D', 'm2': 'B', 'm3': 'E', 'm4': 'F'}))
    it.append(dict(label='o', question=3, type='Ordering', points=20, points_per_part=4, answer={'o1': 1, 'o2': 2, 'o3': 4, 'o4': 5, 'o5': 3}))
    it.append(dict(label='b', question=4, type='FillBlankGroup', points=20, points_per_blank={'b1': 10, 'b2': 10}, answer={'b1': '45', 'b2': '37'}))
    it.append(dict(label='n1', question=5, type='NumericAnswer', points=5, answer={'n1': dict(value=7, unit='u', tolerance=0)}))
    it.append(dict(label='n2', question=5, type='NumericAnswer', points=5, answer={'n2': dict(value=42, unit='u', tolerance=0)}))
    it.append(dict(label='n3', question=5, type='NumericAnswer', points=5, answer={'n3': dict(value=174, unit='u', tolerance=0)}))
    it.append(dict(label='t1', question=5, type='CodeTrace', points=5, answer={'t1': '5'}))
    it.append(dict(label='t2', question=5, type='CodeTrace', points=5, answer={'t2': '15'}))
    it.append(dict(label='x', question=6, type='ShortExplanation', points=10, answer=None))
    return dict(items=it)
K = synth()
rule = json.load(open(args.rule)); calc = S.rule_table()
rep('S1 the rule file equals the table the module computes (%d answer types)' % len(calc['answer_types']), json.dumps(rule, sort_keys=True) == json.dumps(calc, sort_keys=True), '')
ok = True; why = []
ty = {t['id']: t for t in calc['answer_types']}
if not (ty['choice_four']['blind_chance_exact'] == '1/4' and ty['choice_four']['penalty_fraction_exact'] == '1/3'): ok = False; why.append('choice four is not 1/4 and 1/3')
zero = []
for t in calc['answer_types']:
    p = F(t['blind_chance_exact']); lam = F(t['penalty_fraction_exact'])
    if lam == 0: zero.append(t['id'])
    else:
        if S.expected_blind(p, lam) != 0: ok = False; why.append(t['id'])
        if lam != p / (1 - p): ok = False; why.append(t['id'] + ' lambda')
rep('S2 exact: choice of four p = 1/4, penalty 1/3; every non-zero penalty gives expected blind share exactly 0', ok, 'penalty fractions: ' + ', '.join('%s %s' % (t['id'], t['penalty_fraction_exact']) for t in calc['answer_types']) + '; ' + str(why))
rep('S2b the zero-penalty types are exactly those with p below %s (and the hand-marked type)' % S.NEGLIGIBLE_P, sorted(zero) == sorted(t['id'] for t in calc['answer_types'] if F(t['blind_chance_exact']) < F(S.NEGLIGIBLE_P).limit_denominator(10 ** 6)), str(sorted(zero)))
# S3 hand-worked fixtures (expected values worked by hand, as fractions)
marks = {'c1': 'A', 'c2': 'D', 'c3': None,                       # +5, wrong: -5/3, blank 0
         'm1': 'D', 'm2': 'B', 'm3': 'A', 'm4': None,            # +5 +5, wrong -5/5 = -1, blank
         'o1': '1', 'o2': '2', 'o3': '3', 'o4': '4', 'o5': '5',  # +4 +4, three wrong: 3 * -4/4 = -3
         'b1': '45', 'b2': '13',                                 # +10, wrong -10/3
         'n1': '8', 'n2': '41', 'n3': '175',                     # -5/9, -5/99, 0 (p = 1/1000 negligible)
         't1': S.DOUBLE, 't2': '15', 'x': 7}                     # double 0, +5, bonus 7
exp_total = F(5) - F(5, 3) + 0 + 5 + 5 - 1 + 4 + 4 - 3 + 10 - F(10, 3) - F(5, 9) - F(5, 99) + 0 + 0 + 5
r = S.score(marks, K)
rep('S3a hand-worked marks: total %s' % exp_total, abs(r['total'] - float(exp_total)) < 1e-9 and r['bonus'] == 7.0, 'module total %.6f, bonus %s, counts %s' % (r['total'], r['bonus'], r['counts']))
rep('S3b a blank sheet scores 0 and a sheet of only two-answer places scores 0', S.score({}, K)['total'] == 0 and S.score({l: S.DOUBLE for l in S.perfect_marks(K)}, K)['total'] == 0, '')
tolk = dict(items=[dict(label='z', question=1, type='NumericAnswer', points=4, answer={'z': dict(value=100, unit='u', tolerance=2)})])
rt = [S.score({'z': v}, tolk)['total'] for v in ('98', '102', '103', '97')]
mt = S.marks_of_key(tolk)[0]
rep('S3c tolerance 2 on a three-digit value: 98 and 102 right, 103 and 97 wrong; p = 5/1000, penalty %s' % mt['penalty'], rt[:2] == [4.0, 4.0] and abs(rt[2] - (-4.0 / 199)) < 1e-12 and abs(rt[3] - (-4.0 / 199)) < 1e-12 and mt['p'] == F(5, 1000), str(rt))
# S4
pm = S.perfect_marks(K); pr = S.score(pm, K)
rep('S4a a perfect synthetic sheet scores 100', pr['total'] == 100.0 and pr['max_total'] == 100.0, 'total %s of %s' % (pr['total'], pr['max_total']))
if args.key:
    rk = json.load(open(args.key)); pk = S.score(S.perfect_marks(rk), rk)
    rep('S4b a perfect sheet of the real key scores its full points (questions 1 to 4 = 100; the bonus is separate)', pk['total'] == pk['max_total'] == 100.0, 'total %s of %s, counts %s' % (pk['total'], pk['max_total'], pk['counts']))
# S5
def run_sim(key, label):
    sim = S.simulate(key, args.n, args.seed); worst = max(abs(m) for m, _ in sim.values())
    for k, (m, se) in sim.items(): print('       %-4s mean share of the item\'s points %+.4f  (standard error %.4f)' % (k, m, se))
    return sim, worst
sim, worst = run_sim(K, 'synthetic')
rep('S5a synthetic key: blind guesses of every type (%d runs each) average within 0.02 of zero of the item\'s points' % args.n, worst <= 0.02, 'largest |mean| %.4f over %d items' % (worst, len(sim)))
if args.key:
    sim2, worst2 = run_sim(rk, 'real')
    rep('S5b real key (%d items): same criterion' % len(sim2), worst2 <= 0.02, 'largest |mean| %.4f' % worst2)
# S6
orig = S.penalty_fraction
try:
    S.penalty_fraction = lambda p: F(1, 4)
    ck = dict(items=[K['items'][0]]); sim_c = S.simulate(ck, args.n, args.seed)
finally:
    S.penalty_fraction = orig
mc = sim_c['c1'][0]
rep('S6 control of the check: with the penalty 1/4 the blind mean of a choice item is about +0.0625 and the 0.02 criterion would FAIL it', abs(mc - 0.0625) < 0.02 and abs(mc) > 0.02, 'mean %+.4f' % mc)
# S7
page = {'c1': 'B', 'c2': 'C', 'c3': None, 'c4': S.DOUBLE}; sheet = {'c1': 'A', 'c2': 'C', 'c3': 'D', 'c4': 'A', 'c5': None}
m_, s_ = S.resolve(page, sheet)
rep('S7 resolve: page and sheet differ -> page; page empty -> sheet; page has two answers -> page (no answer, not the sheet); both empty -> none', m_ == {'c1': 'B', 'c2': 'C', 'c3': 'D', 'c4': S.DOUBLE, 'c5': None} and s_ == {'c1': 'page', 'c2': 'page', 'c3': 'sheet', 'c4': 'page', 'c5': 'none'}, str(s_))
# S8
print('S8 table of alternatives: expected score of ONE blind mark as a share of the mark\'s points (a wrong mark costs the stated fraction of its points)')
print('     %-48s %8s %9s %9s %9s %9s %9s' % ('answer type', 'p', 'derived', 'none', '1/4', '1/3', '1/2'))
for t in calc['answer_types']:
    e = t['expected_blind_share']; print('     %-48s %8.4f %9s %+9.4f %+9.4f %+9.4f %+9.4f' % (t['label'], t['blind_chance_p'], t['penalty_fraction_exact'], e['none'], e['1/4'], e['1/3'], e['1/2']))
if args.key:
    ft = S.form_table(rk)
    print('     whole real form, every mark guessed blind (points of 100): ' + ', '.join('%s %+.3f' % (k, ft[k]) for k in ('none', '1/4', '1/3', '1/2', 'derived')))
    for k, v in ft['by_type'].items(): print('       %-16s points %5.2f   none %+7.3f  1/4 %+7.3f  1/3 %+7.3f  1/2 %+7.3f  derived %+7.3f' % (k, v['points'], v['none'], v['1/4'], v['1/3'], v['1/2'], v['derived']))
rep('S8 the table is printed', True, '')
print('SUMMARY %d of %d checks PASS' % (sum(res), len(res)))
sys.exit(0 if all(res) else 1)
