"""Check of the scoring rule file and the scoring module, version 1.1.0 (new file, a copy of sen0401_exam_scoring_check_v1_0_0.py, which stays unchanged; it checks the module and rule file v1.1.0). NEW: F1 to F9 prove the floor of the owner's ruling of 2026-11-02 16:52 Istanbul (the total of the paper is floored at 0, none inside a question), and B1 to B3 report the blind-sheet figures of the whole paper (raw mean, floored mean, share floored, 95th percentile) over --blind sheets (default 20000) on the key given with --key. Original docstring of v1.0.0:
Check of the scoring rule file and the scoring module (new file). Holds no question and no answer: the fixtures are synthetic. Prints PASS / FAIL per check; exit 1 on any FAIL.
  S1 the rule file equals the table the module computes (nothing typed by hand)
  S2 exact arithmetic: choice of four p = 1/4 and penalty 1/3; for every type whose penalty is not zero the expected blind share under the derived penalty is exactly 0; the zero-penalty types are the negligible ones
  S3 fixtures of known answer: the score of hand-worked marks equals the hand-worked value (right, wrong, blank, two answers, per-mark penalty, tolerance, hand-marked bonus)
  S4 a perfect sheet scores 100 (synthetic key) and, when --key is given, the full points of that key
  S5 blind guesses simulated N times (default 20000) per item of every answer type average within 0.02 of ZERO of the item's points
  S6 control of the check itself: with the penalty set to 1/4 the choice item's blind mean is about 0.0625 and the S5 criterion would FAIL it (so the criterion can fail)
  S7 the resolve rule (sheet versus question page) on fixtures
  S8 the table of alternatives printed (no penalty, 1/4, 1/3, 1/2) per answer type, and for the real key when --key is given (points only)
Usage: check.py RULE.json [--key KEY.json] [--n 20000] [--seed 60001] [--blind 20000] [--blind-seed 70001]"""
import argparse, fractions, json, math, os, random, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_scoring_v1_1_0 as S
F = fractions.Fraction
ap = argparse.ArgumentParser(); ap.add_argument('rule'); ap.add_argument('--key'); ap.add_argument('--n', type=int, default=20000); ap.add_argument('--seed', type=int, default=60001); ap.add_argument('--blind', type=int, default=20000); ap.add_argument('--blind-seed', type=int, default=70001)
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
rt = [S.score({'z': v}, tolk, floor_total=None)['total'] for v in ('98', '102', '103', '97')]      # v1.1.0: the raw total is read here, because this one-item key tests the penalty of a mark, not the floor of a paper
mt = S.marks_of_key(tolk)[0]
rep('S3c tolerance 2 on a three-digit value: 98 and 102 right, 103 and 97 wrong; p = 5/1000, penalty %s' % mt['penalty'], rt[:2] == [4.0, 4.0] and abs(rt[2] - (-4.0 / 199)) < 1e-12 and abs(rt[3] - (-4.0 / 199)) < 1e-12 and mt['p'] == F(5, 1000), str(rt))
# S4
pm = S.perfect_marks(K); pr = S.score(pm, K)
rep('S4a a perfect synthetic sheet scores 100', pr['total'] == 100.0 and pr['max_total'] == 100.0, 'total %s of %s' % (pr['total'], pr['max_total']))
if args.key:
    rk = json.load(open(args.key)); pk = S.score(S.perfect_marks(rk), rk)
    rep('S4b a perfect sheet of the real key scores its full points (questions 1 to 4 = 100; the bonus is separate)', pk['total'] == pk['max_total'] == 100.0, 'total %s of %s, counts %s' % (pk['total'], pk['max_total'], pk['counts']))

# F: the floor of the paper total (owner, 2026-11-02 16:52 Istanbul)
rep('F0 the rule file field total_floor carries the owner\'s decision and the module says version 1.1.0', rule['total_floor'] == 'DECIDED by the owner on 2026-11-02 16:52 Istanbul: the total of the whole paper is not below 0 (floor at 0 on the paper total, none inside a question)' and S.VERSION == '1.1.0' and rule['rule_version'] == '1.1.0' and S.TOTAL_FLOOR == 0.0, rule['total_floor'][:60])
neg = {l: v for l, v in S.perfect_marks(K).items()}
neg.update({'c1': 'D', 'c2': 'D', 'c3': 'D', 'm1': 'A', 'm2': 'A', 'm3': 'A', 'm4': 'A', 'n1': '0', 'n2': '0', 'b1': '99', 'b2': '99'})      # wrong in many places; the rest right is removed below
for l in ('o1', 'o2', 'o3', 'o4', 'o5', 'n3', 't1', 't2'): neg[l] = None
rn = S.score(neg, K); rraw = S.score(neg, K, floor_total=None)
rep('F1 a sheet whose raw total is below 0 gives total 0 (default floor) and the module reports the raw total', rn['raw_total'] < 0 and rn['total'] == 0 and rn['floored'] is True and rraw['total'] == rn['raw_total'], 'raw %.6f, total %s' % (rn['raw_total'], rn['total']))
rep('F2 the per-mark and per-question points of that sheet keep their signs (no floor inside a question)', any(v < 0 for v in rn['per_question'].values()) and all(abs(rn['per_mark'][l] - rraw['per_mark'][l]) < 1e-12 for l in rn['per_mark']) and abs(sum(rn['per_question'].values()) - rn['raw_total']) < 1e-9 and min(rn['per_mark'].values()) < 0, 'per question %s' % {k: round(v, 3) for k, v in rn['per_question'].items()})
# a sheet where one question is negative but the paper total is above 0: the question keeps its negative points, the total is the plain sum
mix = S.perfect_marks(K); mix.update({'c1': 'D', 'c2': 'D', 'c3': 'D'})
rm = S.score(mix, K)
rep('F3 a negative question inside a positive paper is NOT floored (question 1 negative, total the plain sum)', rm['per_question'][1] < 0 and rm['total'] == rm['raw_total'] and rm['total'] > 0 and not rm['floored'], 'question 1 %.4f, total %.4f' % (rm['per_question'][1], rm['total']))
hi = dict(marks); rh = S.score(hi, K)
rep('F4 a sheet above 0 is unchanged by the floor (hand-worked marks of S3a: same total with the floor and without it)', rh['total'] > 0 and rh['total'] == S.score(hi, K, floor_total=None)['total'] and not rh['floored'], 'total %.6f' % rh['total'])
rep('F5 a perfect sheet gives 100 (synthetic key)', pr['total'] == 100.0 and pr['raw_total'] == 100.0, '')
rep('F6 a blank sheet gives 0, and the floor does not turn 0 into a gain', S.score({}, K)['total'] == 0 and S.score({}, K)['raw_total'] == 0, '')
rb = S.score(dict(neg, x=7), K)
rep('F7 the bonus is added after the floor and is not a penalty: a floored sheet with a bonus of 7 has total 0 and bonus 7', rb['total'] == 0 and rb['bonus'] == 7.0, 'total %s bonus %s' % (rb['total'], rb['bonus']))
rep('F8 floor_total=None gives the raw total (the module can still show the raw figure)', rraw['total'] < 0, '')
# F9 control of the check: a module without the floor would fail F1
orig_s = S.score
try:
    S.score = lambda m, k, floor_total=None: orig_s(m, k, floor_total=None)
    broken = S.score(neg, K)
finally:
    S.score = orig_s
rep('F9 control of the check: a module that does not floor would give a negative total on the F1 sheet, so F1 can fail', broken['total'] < 0, 'total %.4f' % broken['total'])
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

# B: blind sheets of the whole paper, under the floor (the owner's ruling): every place marked at random
def blind_figures(key, n, seed, only=None):
    rng = random.Random(seed); raws = []; fl = []; nflo = 0
    for _ in range(n):
        mk = S.blind_marks(key, rng)
        if only is not None: mk = {l: v for l, v in mk.items() if l in only}
        r = S.score(mk, key); raws.append(r['raw_total']); fl.append(r['total']); nflo += r['floored']
    raws_s = sorted(raws); fl_s = sorted(fl)
    q95 = lambda a: a[min(len(a) - 1, int(math.ceil(0.95 * len(a))) - 1)]
    mean = lambda a: sum(a) / len(a)
    sd = math.sqrt(max(0.0, sum(x * x for x in raws) / len(raws) - mean(raws) ** 2))
    return dict(n=n, raw_mean=mean(raws), floored_mean=mean(fl), share_floored=nflo / n, raw_p95=q95(raws_s), floored_p95=q95(fl_s), raw_sd=sd, raw_se=sd / math.sqrt(n), floored_max=fl_s[-1], raw_min=raws_s[0])
def show_blind(tag, b):
    print('       %s: sheets %d  raw total mean %+.3f (standard error %.3f, sd %.3f)  floored total mean %+.3f  share of sheets floored %.1f percent  95th percentile raw %+.2f floored %+.2f  (raw min %+.2f, floored max %.2f)' %
          (tag, b['n'], b['raw_mean'], b['raw_se'], b['raw_sd'], b['floored_mean'], 100 * b['share_floored'], b['raw_p95'], b['floored_p95'], b['raw_min'], b['floored_max']))
# S6
orig = S.penalty_fraction
try:
    S.penalty_fraction = lambda p: F(1, 4)
    ck = dict(items=[K['items'][0]]); sim_c = S.simulate(ck, args.n, args.seed)
finally:
    S.penalty_fraction = orig
mc = sim_c['c1'][0]
rep('S6 control of the check: with the penalty 1/4 the blind mean of a choice item is about +0.0625 and the 0.02 criterion would FAIL it', abs(mc - 0.0625) < 0.02 and abs(mc) > 0.02, 'mean %+.4f' % mc)

# B1 to B3 on the real key
if args.key:
    ba = blind_figures(rk, args.blind, args.blind_seed)
    show_blind('B1 all places marked blind, real key', ba)
    rep('B1 blind sheets that mark every place (%d sheets, real key): floored mean >= raw mean, floored mean >= 0 by construction (the owner\'s ruling), raw mean near 0' % args.blind, args.blind >= 20000 and ba['floored_mean'] >= ba['raw_mean'] and ba['floored_mean'] >= 0 and abs(ba['raw_mean']) <= 4 * ba['raw_se'], 'raw %+.3f, floored %+.3f, floored share %.1f percent, 95th percentile raw %+.2f / floored %+.2f' % (ba['raw_mean'], ba['floored_mean'], 100 * ba['share_floored'], ba['raw_p95'], ba['floored_p95']))
    allm = [m for m in S.marks_of_key(rk) if m['guessable']]
    zero_pen = {m['label'] for m in allm if m['penalty'] == 0}; with_pen = {m['label'] for m in allm if m['penalty'] != 0}
    b2 = blind_figures(rk, args.blind, args.blind_seed + 1, only=zero_pen); show_blind('B2 only the places that cost nothing when wrong (%d places: numbers of three or more digits)' % len(zero_pen), b2)
    b3 = blind_figures(rk, args.blind, args.blind_seed + 2, only=with_pen); show_blind('B3 only the places that cost something when wrong (%d places), the others blank' % len(with_pen), b3)
    blank = S.score({}, rk)
    rep('B2 a student who answers blind only the places a guesser can answer without loss (a wrong answer costs nothing there): the floor changes nothing for him', b2['share_floored'] == 0 and abs(b2['floored_mean'] - b2['raw_mean']) < 1e-12 and b2['floored_mean'] >= 0, 'mean %+.3f, floored share %.1f percent' % (b2['floored_mean'], 100 * b2['share_floored']))
    rep('B3 the all-blank sheet scores 0 (raw 0, floored 0); blind answering of only the places that cost something is a gain only through the floor', blank['total'] == 0 and blank['raw_total'] == 0 and b3['floored_mean'] >= b3['raw_mean'], 'blank total %s; B3 raw %+.3f floored %+.3f' % (blank['total'], b3['raw_mean'], b3['floored_mean']))
    print('       STATED PLAINLY: under the owner\'s ruling of 2026-11-02 16:52 Istanbul the mean of the floored total of blind sheets is above 0 by construction (a sheet cannot score below 0, and some blind sheets score above 0). The per-mark penalty still makes a blind mark worth zero on average BEFORE the floor (raw mean %+.3f); the floor adds %+.3f points on average to a blind sheet.' % (ba['raw_mean'], ba['floored_mean'] - ba['raw_mean']))
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
