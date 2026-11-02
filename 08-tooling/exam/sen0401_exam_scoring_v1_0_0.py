"""SEN0401 exam scoring module, version 1.0.0 (new file). Applies the scoring rule of sen0401_exam_scoring_rule_v1_0_0.json to a set of marks and the key of a form.
Pure library plus a small command line. Holds no question and no answer: the key is read from a file or built in memory by a test.

THE PRINCIPLE (the owner's, 2026-11-02): a blind guess must be worth zero. With p the chance that a blind guess of one MARK is right, a right mark earns its points and a wrong mark costs
   lambda = p / (1 - p)   of that mark's points, because  p * 1 - (1 - p) * lambda = 0.   A blank mark costs nothing. Two answers in one place count as NO answer and cost nothing.
   Choice of four: p = 1/4, lambda = 1/3 (derived, not stipulated). The same formula gives the other types. Where p is negligible (below NEGLIGIBLE_P) lambda is 0 and the rule file says so.
THE UNIT OF PENALTY is the mark: an item with several marks (matching parts, ordering steps, bank blanks) is scored per mark, each mark with its own points.
MARKS: {label: value}; value None or missing = blank; DOUBLE = two answers; choice 'A'..; matching letter; ordering place '1'..; bank two-digit code; number digits; trace text.
WHAT COUNTS (owner point 2): the answers written on the question pages are the LEGAL copy; the answer sheet is an option for fast reading. resolve(page, sheet): where both exist and differ the question page counts;
where only the sheet holds an answer the sheet counts (the fast option)."""
import argparse, fractions, json, math, os, random, sys
sys.dont_write_bytecode = True
VERSION = '1.0.0'
DOUBLE = 'DOUBLE'
NEGLIGIBLE_P = 0.005          # below this chance of a blind hit the penalty is 0 (a number of three or more digits: 1/1000)
UNUSED_RESPONSES = 2          # matching: two responses that no premise takes
UNUSED_BANK_ENTRIES = 2       # fill-in bank: two entries that no blank takes
ALTERNATIVES = [('none', fractions.Fraction(0)), ('1/4', fractions.Fraction(1, 4)), ('1/3', fractions.Fraction(1, 3)), ('1/2', fractions.Fraction(1, 2))]
CHOICE_TYPES = ('ChoiceFour', 'ChoiceFourCase', 'ChoiceFourCode')


def penalty_fraction(p):
    """lambda = p / (1 - p) when p is not negligible, else 0. p is a Fraction or float."""
    p = fractions.Fraction(p).limit_denominator(10 ** 9)
    if p >= 1: raise ValueError('p must be below 1')
    if p < fractions.Fraction(NEGLIGIBLE_P).limit_denominator(10 ** 6): return fractions.Fraction(0)
    return p / (1 - p)


def expected_blind(p, lam):
    """Expected score of a blind guess of one mark, as a share of the mark's points, under a penalty fraction lam."""
    p = fractions.Fraction(p); lam = fractions.Fraction(lam)
    return p - (1 - p) * lam


def number_p(digits, tolerance=0):
    """Chance that a uniform guess over the digit boxes hits the value: (2*tolerance + 1) accepted whole numbers among 10**digits strings."""
    return fractions.Fraction(2 * int(tolerance) + 1, 10 ** digits)


def key_digits(value):
    s = str(value).replace('-', '').replace('.', '').replace(' ', '')
    return len(s)


def type_of(item):
    t = item['type']
    if t in CHOICE_TYPES: return 'choice_four'
    return {'Matching': 'matching', 'Ordering': 'ordering', 'FillBlankGroup': 'fill_bank', 'NumericAnswer': 'number_or_trace', 'CodeTrace': 'number_or_trace', 'ShortExplanation': 'hand_marked'}[t]


def marks_of_key(key):
    """The marks of a form, from its key (the format of the papers v5 key JSON). One record per mark: label, rule type, points, expected answer, chance p, penalty fraction."""
    out = []
    for it in key['items']:
        ty = type_of(it); t = it['type']
        if ty == 'hand_marked':
            out.append(dict(label=it['label'], rule_type=ty, item=it['label'], question=it['question'], points=it['points'], answer=None, p=fractions.Fraction(0), penalty=fractions.Fraction(0), guessable=False)); continue
        labels = list(it['answer'].keys()); n = len(labels)
        for lab in labels:
            ans = it['answer'][lab]
            if ty == 'choice_four': pts, p = it['points'], fractions.Fraction(1, 4)
            elif ty == 'matching': pts, p = it['points_per_part'], fractions.Fraction(1, n + UNUSED_RESPONSES)
            elif ty == 'ordering': pts, p = it['points_per_part'], fractions.Fraction(1, n)
            elif ty == 'fill_bank': pts, p = it['points_per_blank'][lab], fractions.Fraction(1, n + UNUSED_BANK_ENTRIES)
            else:
                pts = it['points']
                if t == 'NumericAnswer': p = number_p(key_digits(ans['value']), ans.get('tolerance', 0)); ans = ans['value']
                else: p = number_p(key_digits(ans), 0)
            out.append(dict(label=lab, rule_type=ty, item=it['label'], question=it['question'], points=pts, answer=ans, p=p, penalty=penalty_fraction(p), guessable=True,
                            tolerance=(it['answer'][lab].get('tolerance', 0) if t == 'NumericAnswer' else 0)))
    return out


def _right(m, v):
    if m['rule_type'] == 'number_or_trace' and m['tolerance'] is not None and not isinstance(m['answer'], str):
        try: return abs(float(str(v).strip()) - float(m['answer'])) <= float(m['tolerance'])
        except ValueError: return False
    if m['rule_type'] == 'ordering': return str(v).strip() == str(m['answer'])
    return str(v).strip().upper() == str(m['answer']).strip().upper() if m['rule_type'] in ('choice_four', 'matching') else str(v).strip() == str(m['answer']).strip()


def score(marks, key, floor_total=None):
    """marks: {label: value}. Returns a dict: per_mark {label: points}, per_question {q: points}, total (questions that are read from the sheet, the bonus excluded), bonus (hand-marked points, given in marks as a number), counts.
    A hand-marked label takes its points from marks (a number from 0 to the item's points, given by the marker); it never carries a penalty."""
    per = {}; cnt = {'right': 0, 'wrong': 0, 'blank': 0, 'double': 0}; bonus = 0.0
    for m in marks_of_key(key):
        v = marks.get(m['label'])
        if not m['guessable']:
            got = float(v) if v not in (None, DOUBLE) else 0.0
            if got < 0 or got > m['points']: raise ValueError('hand-marked points of %s out of range' % m['label'])
            bonus += got; per[m['label']] = got; continue
        if v is None or str(v).strip() == '': per[m['label']] = 0.0; cnt['blank'] += 1
        elif v == DOUBLE: per[m['label']] = 0.0; cnt['double'] += 1
        elif _right(m, v): per[m['label']] = float(m['points']); cnt['right'] += 1
        else: per[m['label']] = -float(m['points']) * float(m['penalty']); cnt['wrong'] += 1
    pq = {}
    for m in marks_of_key(key):
        if m['guessable']: pq[m['question']] = pq.get(m['question'], 0.0) + per[m['label']]
    total = sum(pq.values())
    if floor_total is not None: total = max(floor_total, total)
    return dict(per_mark=per, per_question=pq, total=total, bonus=bonus, counts=cnt, max_total=float(sum(m['points'] for m in marks_of_key(key) if m['guessable'])))


def resolve(page_marks, sheet_marks):
    """The rule of owner point 2. Returns (marks, source) where source[label] is 'page', 'sheet' or 'none'.
    The question page is the legal copy: a label with any answer on the page (a value, or DOUBLE) takes the page's answer, whatever the sheet says. Only a label the page leaves empty takes the sheet's answer (provisional until read by the marker)."""
    out = {}; src = {}
    for lab in set(page_marks) | set(sheet_marks):
        pv = page_marks.get(lab); sv = sheet_marks.get(lab)
        if pv is not None and str(pv).strip() != '': out[lab] = pv; src[lab] = 'page'
        elif sv is not None and str(sv).strip() != '': out[lab] = sv; src[lab] = 'sheet'
        else: out[lab] = None; src[lab] = 'none'
    return out, src


def perfect_marks(key):
    return {m['label']: m['answer'] for m in marks_of_key(key) if m['guessable']}


def blind_marks(key, rng):
    """One blind guesser: answers EVERY mark of every item, uniformly over the options of the type; matching and bank with each response used once; ordering as a permutation; numbers as uniform digit strings."""
    marks = {}
    for it in key['items']:
        ty = type_of(it)
        if ty == 'hand_marked': continue
        labels = list(it['answer'].keys()); n = len(labels)
        if ty == 'choice_four': marks[labels[0]] = rng.choice('ABCD')
        elif ty == 'matching':
            letters = 'ABCDEFGH'[:n + UNUSED_RESPONSES]; pick = rng.sample(letters, n)
            for lab, v in zip(labels, pick): marks[lab] = v
        elif ty == 'ordering':
            pick = rng.sample(range(1, n + 1), n)
            for lab, v in zip(labels, pick): marks[lab] = str(v)
        elif ty == 'fill_bank':
            codes = list(it['bank_codes']) if 'bank_codes' in it else [it['answer'][l] for l in labels] + ['wrong%d' % k for k in range(UNUSED_BANK_ENTRIES)]    # the printed entries of the bank (a key may carry them; otherwise the right entries plus never-right stand-ins for the unused ones)
            pick = rng.sample(codes, n)
            for lab, v in zip(labels, pick): marks[lab] = v
        else:
            lab = labels[0]; a = it['answer'][lab]; d = key_digits(a['value'] if isinstance(a, dict) else a)
            marks[lab] = str(rng.randrange(10 ** d)).zfill(d)
    return marks


def rule_table():
    """The rule file content: per answer type, p, lambda and the alternatives table. Everything is computed here, nothing is typed in."""
    def row(id_, label, p, how, per_mark_note):
        lam = penalty_fraction(p)
        if id_ == 'hand_marked':           # nothing is guessed blind here: a marker reads it, and there is no penalty under any alternative
            return dict(id=id_, label=label, blind_chance_p=0.0, blind_chance_exact='0', how_p_is_computed=how, penalty_fraction=0.0, penalty_fraction_exact='0', penalty_zero_because_p_negligible=False, unit_of_penalty=per_mark_note,
                        expected_blind_share={name: 0.0 for name, _ in ALTERNATIVES}, expected_blind_share_exact={name: '0' for name, _ in ALTERNATIVES}, expected_blind_share_under_derived_penalty=0.0)
        return dict(id=id_, label=label, blind_chance_p=float(p), blind_chance_exact=str(fractions.Fraction(p)), how_p_is_computed=how, penalty_fraction=float(lam), penalty_fraction_exact=str(lam),
                    penalty_zero_because_p_negligible=bool(lam == 0 and p > 0), unit_of_penalty=per_mark_note,
                    expected_blind_share={name: float(expected_blind(p, l)) for name, l in ALTERNATIVES}, expected_blind_share_exact={name: str(expected_blind(p, l)) for name, l in ALTERNATIVES},
                    expected_blind_share_under_derived_penalty=float(expected_blind(p, lam)))
    types = [
        row('choice_four', 'Choice of four', fractions.Fraction(1, 4), 'one right option among 4: p = 1/4', 'the item (one mark)'),
        row('matching_6', 'Matching, 4 premises, 6 responses (two unused)', fractions.Fraction(1, 6), 'each premise: one right response among 4 + 2 = 6 (responses used once; the chance of one mark is 1/6 whatever the others are): p = 1/6', 'each pair (its points_per_part)'),
        row('ordering_5', 'Ordering of five steps', fractions.Fraction(1, 5), 'each step: one right place among 5 (the places are used once; the chance of one mark is 1/5): p = 1/5', 'each step (its points_per_part)'),
        row('fill_bank_4', 'Fill-in bank, 2 blanks, 4 entries (two unused)', fractions.Fraction(1, 4), 'each blank: one right entry among 2 + 2 = 4 printed entries (entries used once): p = 1/4', 'each blank (its own points)'),
        row('number_1_digit', 'Number or code trace, one digit', number_p(1), 'uniform guess over the digit boxes: p = (2*tolerance+1) / 10**digits = 1/10', 'the item (one mark)'),
        row('number_2_digits', 'Number or code trace, two digits', number_p(2), 'p = 1/100', 'the item (one mark)'),
        row('number_3_digits', 'Number, three digits', number_p(3), 'p = 1/1000, below the negligible limit %s: penalty 0' % NEGLIGIBLE_P, 'the item (one mark)'),
        row('number_4_digits', 'Number, four digits', number_p(4), 'p = 1/10000: penalty 0', 'the item (one mark)'),
        row('number_5_digits', 'Number, five digits (the sheet has five boxes)', number_p(5), 'p = 1/100000: penalty 0', 'the item (one mark)'),
        row('hand_marked', 'Hand-marked explanation (bonus)', fractions.Fraction(0), 'not guessable: a marker reads it; p = 0 for the rule', 'none: the marker gives 0 to full points, no penalty'),
    ]
    return dict(rule_version=VERSION, holds_no_question_and_no_answer=True,
                principle='A blind guess must be worth zero (owner, 2026-11-02). With p the chance that a blind guess of one mark is right, a wrong mark costs lambda = p/(1-p) of that mark\'s points, because p*1 - (1-p)*lambda = 0. The one third for four options is DERIVED from this principle, not stipulated.',
                formula='penalty_fraction = p / (1 - p); expected blind share = p - (1 - p) * penalty_fraction', default_penalty='derived per answer type (choice of four: 1/3)',
                negligible_p=NEGLIGIBLE_P, negligible_rule='where the chance of a blind hit is below %s (a number of three or more digits) the penalty is 0, because no guesser gains from such a lottery; the rule file says so for each such type.' % NEGLIGIBLE_P,
                blank_rule='A blank mark scores 0 and costs nothing.', two_answers_in_one_place_rule='Two filled bubbles (or two written answers) in one place count as NO answer: 0 points, no penalty (sheet rule 3, unchanged). Marking two options therefore never gains.',
                sheet_vs_question_page_rule='The answers written on the question pages are the legal copy. The answer sheet is an option for fast reading. Where both exist and differ, the question pages count. Where only the sheet holds an answer, the sheet counts (provisionally, until the marker has looked).',
                unit_of_penalty='the mark: an item with several marks (matching pairs, ordering steps, bank blanks) is scored per mark, each wrong mark costing lambda of its own points',
                total_floor='NOT DECIDED (open question for the owner): the total is not raised to 0 here. A floor at 0 would give a blind guesser a positive expected score, which the principle forbids.',
                answer_types=types, alternatives_penalty_fractions={name: str(l) for name, l in ALTERNATIVES},
                alternatives_note='expected_blind_share is the expected score of one blind mark as a share of the mark\'s points, with a wrong mark costing the stated fraction of its points (none, 1/4, 1/3, 1/2) instead of the derived one.')


def form_table(key, penalties=None):
    """Expected blind score of a whole form (all marks guessed blind) in points, under the alternatives and under the derived rule. Computed from p and the points of the marks, nothing else."""
    ms = [m for m in marks_of_key(key) if m['guessable']]; out = {}
    for name, l in ALTERNATIVES: out[name] = float(sum(m['points'] * expected_blind(m['p'], l) for m in ms))
    out['derived'] = float(sum(m['points'] * expected_blind(m['p'], m['penalty']) for m in ms))
    out['max_points'] = float(sum(m['points'] for m in ms))
    by = {}
    for m in ms:
        d = by.setdefault(m['rule_type'], dict(points=0.0, **{name: 0.0 for name, _ in ALTERNATIVES}, derived=0.0))
        d['points'] += float(m['points'])
        for name, l in ALTERNATIVES: d[name] += float(m['points'] * expected_blind(m['p'], l))
        d['derived'] += float(m['points'] * expected_blind(m['p'], m['penalty']))
    out['by_type'] = by
    return out


def simulate(key, n=20000, seed=60001):
    """Blind guessers over every item of the key: mean score of each item as a share of the item's points, under the derived rule. Returns {item_label: (mean_share, standard_error)}."""
    rng = random.Random(seed); sums = {}; sq = {}
    items = {it['label']: it for it in key['items'] if type_of(it) != 'hand_marked'}
    mk = marks_of_key(key); by_item = {}
    for m in mk:
        if m['guessable']: by_item.setdefault(m['item'], []).append(m)
    pts = {k: float(sum(m['points'] for m in v)) for k, v in by_item.items()}
    for _ in range(n):
        marks = blind_marks(key, rng); r = score(marks, key)['per_mark']
        for k, v in by_item.items():
            s = sum(r[m['label']] for m in v); sums[k] = sums.get(k, 0.0) + s; sq[k] = sq.get(k, 0.0) + s * s
    out = {}
    for k in by_item:
        mean = sums[k] / n; var = max(0.0, sq[k] / n - mean * mean); out[k] = (mean / pts[k], math.sqrt(var / n) / pts[k])
    return out


def main():
    a = argparse.ArgumentParser(); a.add_argument('cmd', choices=['write-rule', 'form-table', 'score']); a.add_argument('--out'); a.add_argument('--key'); a.add_argument('--marks')
    o = a.parse_args()
    if o.cmd == 'write-rule':
        txt = json.dumps(rule_table(), indent=1, sort_keys=False)
        if o.out:
            if os.path.exists(o.out): print('REFUSED: exists ' + o.out); sys.exit(2)
            open(o.out, 'w').write(txt + '\n')
        else: print(txt)
    elif o.cmd == 'form-table': print(json.dumps(form_table(json.load(open(o.key))), indent=1))
    else: print(json.dumps(score(json.load(open(o.marks)), json.load(open(o.key))), indent=1))


if __name__ == '__main__': main()
