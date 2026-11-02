"""SEN0401 exam scoring module, version 2.0.0 (new file; the v1_0_0 and v1_1_0 files stay unchanged).
THE RULE (owner redesign of 2026-11-02, 18:20 Istanbul; rulings 1 and 3): ONE rule for every question.
  A right answer scores its points. A wrong answer, a blank and two answers in one place score 0.
  There is NO penalty of any kind, NO floor, NO bonus. The total is the sum of the points of the right places (100 on a perfect sheet).
  A unit with rows (matching premises, ordering steps, fill-in blanks) scores the points printed in the key for each right row.
  A number or a code trace is right only when its value equals the key value exactly: full points, else 0, no partial credit, no tolerance.
  The marker enters the numbers.
THE KEY IS READ, THE STRUCTURE'S PENALTY FIELDS NEVER ARE (guess_chance, penalty_fraction, scoring.* are ignored).
FIVE ALTERNATIVES in every closed unit: choice 5 options, matching 5 responses per premise, ordering a place 1..5 over 5 steps, fill-in banks of 5 entries.
  The counts are read from the key when it carries them (n_options, n_responses, bank_codes); otherwise the ruling's five applies (choice 5; matching 5; bank 5 entries).
Holds no question and no answer: the key is read from a file or built in memory by a test.
WHAT COUNTS: the answers written on the question pages are the legal copy; the answer sheet is an option for fast reading. resolve(page, sheet) keeps the v1.1.0 rule."""
import argparse, decimal, fractions, json, math, os, random, sys
sys.dont_write_bytecode = True
VERSION = '2.0.0'
DOUBLE = 'DOUBLE'
F = fractions.Fraction
ALTERNATIVES = 5               # ruling 3
MATCH_LETTERS = 'ABCDEFGH'
CHOICE_LETTERS = 'ABCDEFGH'


def key_digits(value):
    return len(str(value).replace('-', '').replace('.', '').replace(' ', ''))


def number_p(digits):
    """Chance that a blind digit string of the key value's length equals the key value: 1 / 10**digits."""
    return F(1, 10 ** digits)


def type_of(item):
    t = item['type']
    if t.startswith('Choice'): return 'choice'
    kind = {'Matching': 'matching', 'Ordering': 'ordering', 'FillBlankGroup': 'fill_bank', 'NumericAnswer': 'number_or_trace', 'CodeTrace': 'number_or_trace'}.get(t)
    if kind is None: raise ValueError('item %s: type %s has no place in the v7 scoring rule (the bonus and hand-marked items are removed)' % (item.get('label'), t))
    return kind


def _n_choice(it): return int(it.get('n_options', len(it['options']) if 'options' in it else ALTERNATIVES))
def _n_resp(it, n): return int(it.get('n_responses', len(it['responses']) if 'responses' in it else ALTERNATIVES))
def _n_bank(it, n): return len(it['bank_codes']) if 'bank_codes' in it else ALTERNATIVES


def marks_of_key(key):
    """One record per place: label, rule type, item, question, points (Fraction, exact), answer, blind chance p (Fraction, exact), alternatives."""
    out = []
    for it in key['items']:
        ty = type_of(it); t = it['type']; labels = list(it['answer'].keys()); n = len(labels)
        for lab in labels:
            ans = it['answer'][lab]
            if ty == 'choice': pts = F(str(it['points'])); alt = _n_choice(it); p = F(1, alt)
            elif ty == 'matching': pts = F(str(it['points_per_part'])); alt = _n_resp(it, n); p = F(1, alt)
            elif ty == 'ordering': pts = F(str(it['points_per_part'])); alt = n; p = F(1, alt)
            elif ty == 'fill_bank': pts = F(str(it['points_per_blank'][lab])); alt = _n_bank(it, n); p = F(1, alt)
            else:
                pts = F(str(it['points'])); ans = ans['value'] if isinstance(ans, dict) else ans
                alt = 10 ** key_digits(ans); p = number_p(key_digits(ans))
            out.append(dict(label=lab, rule_type=ty, item=it['label'], question=it['question'], points=pts, answer=ans, p=p, alternatives=alt))
    return out


def _num(s):
    try: return decimal.Decimal(str(s).strip())
    except decimal.InvalidOperation: return None


def right(m, v):
    """A place is right only on an exact match of the key value (letters ignoring case; numbers by numeric equality; other text exactly, trimmed)."""
    if v is None or v == DOUBLE: return False
    ty = m['rule_type']
    if ty in ('choice', 'matching'): return str(v).strip().upper() == str(m['answer']).strip().upper()
    if ty == 'ordering' or ty == 'number_or_trace':
        a, b = _num(v), _num(m['answer'])
        if a is not None and b is not None: return a == b
    return str(v).strip() == str(m['answer']).strip()


def score(marks, key):
    """marks: {label: value}; None, a missing label, an empty string or DOUBLE = no answer. Returns per_mark, per_question, total (a plain sum, never below 0), counts, max_total."""
    per = {}; cnt = {'right': 0, 'wrong': 0, 'blank': 0, 'double': 0}; pq = {}; ms = marks_of_key(key)
    for m in ms:
        v = marks.get(m['label'])
        if v is None or str(v).strip() == '': got = F(0); cnt['blank'] += 1
        elif v == DOUBLE: got = F(0); cnt['double'] += 1
        elif right(m, v): got = m['points']; cnt['right'] += 1
        else: got = F(0); cnt['wrong'] += 1
        per[m['label']] = float(got); pq[m['question']] = pq.get(m['question'], F(0)) + got
    total = sum(pq.values(), F(0))
    return dict(per_mark=per, per_question={q: float(v) for q, v in pq.items()}, total=float(total), total_exact=str(total), counts=cnt, max_total=float(sum(m['points'] for m in ms)))


def resolve(page_marks, sheet_marks):
    """The question page is the legal copy: a label with any answer on the page (a value, or DOUBLE) takes the page's answer; only a label the page leaves empty takes the sheet's. Returns (marks, source)."""
    out = {}; src = {}
    for lab in set(page_marks) | set(sheet_marks):
        pv = page_marks.get(lab); sv = sheet_marks.get(lab)
        if pv is not None and str(pv).strip() != '': out[lab] = pv; src[lab] = 'page'
        elif sv is not None and str(sv).strip() != '': out[lab] = sv; src[lab] = 'sheet'
        else: out[lab] = None; src[lab] = 'none'
    return out, src


def perfect_marks(key): return {m['label']: m['answer'] for m in marks_of_key(key)}


def blind_marks(key, rng):
    """One blind guesser answering EVERY place uniformly: choice over its options; matching and bank each response/entry used once; ordering as a permutation; numbers as uniform digit strings of the key's length."""
    marks = {}
    for it in key['items']:
        ty = type_of(it); labels = list(it['answer'].keys()); n = len(labels)
        if ty == 'choice': marks[labels[0]] = rng.choice(CHOICE_LETTERS[:_n_choice(it)])
        elif ty == 'matching':
            for lab, v in zip(labels, rng.sample(MATCH_LETTERS[:_n_resp(it, n)], n)): marks[lab] = v
        elif ty == 'ordering':
            for lab, v in zip(labels, rng.sample(range(1, n + 1), n)): marks[lab] = str(v)
        elif ty == 'fill_bank':
            codes = list(it['bank_codes']) if 'bank_codes' in it else [it['answer'][l] for l in labels] + ['x%d' % k for k in range(ALTERNATIVES - n)]
            for lab, v in zip(labels, rng.sample(codes, n)): marks[lab] = v
        else:
            lab = labels[0]; a = it['answer'][lab]; d = key_digits(a['value'] if isinstance(a, dict) else a)
            marks[lab] = str(rng.randrange(10 ** d)).zfill(d)
    return marks


def expected_blind(key):
    """Exact expected total of a sheet answered totally blind, in points (Fraction), with the split closed / number-and-trace."""
    ms = marks_of_key(key); closed = sum((m['points'] * m['p'] for m in ms if m['rule_type'] != 'number_or_trace'), F(0))
    num = sum((m['points'] * m['p'] for m in ms if m['rule_type'] == 'number_or_trace'), F(0))
    cp = sum((m['points'] for m in ms if m['rule_type'] != 'number_or_trace'), F(0))
    return dict(total=closed + num, closed=closed, number_and_trace=num, closed_points=cp, max_points=sum((m['points'] for m in ms), F(0)))


def rule_table():
    """The rule file content, computed here, nothing typed by hand: per answer type the blind chance with exact fractions."""
    def row(id_, label, p, how):
        return dict(id=id_, label=label, blind_chance_exact=str(p), blind_chance=float(p), how_p_is_computed=how, wrong_scores=0, blank_scores=0, two_answers_in_one_place_scores=0)
    types = [row('choice_5', 'Choice of five', F(1, 5), 'one right option among 5: p = 1/5'),
             row('matching_5', 'Matching, 4 premises, 5 responses (one unused)', F(1, 5), 'each premise: one right response among 5 (responses used once; the chance of one row is 1/5 whatever the other rows are): p = 1/5'),
             row('ordering_5', 'Ordering of five steps over places 1 to 5', F(1, 5), 'each step: one right place among 5 (places used once; the chance of one row is 1/5): p = 1/5'),
             row('fill_bank_5', 'Fill-in bank, 2 blanks, 5 entries (three unused)', F(1, 5), 'each blank: one right entry among 5 printed entries (entries used once): p = 1/5')]
    for d in range(1, 6): types.append(row('number_or_trace_%d_digits' % d, 'Number or code trace written by hand, key value of %d digit%s' % (d, '' if d == 1 else 's'), number_p(d), 'blind digit string of the key value\'s length: p = 1/10**%d' % d))
    return dict(rule_version=VERSION, holds_no_question_and_no_answer=True,
        rule='One rule for every question: a right answer scores its points; a wrong answer, a blank and two answers in one place score 0.',
        penalty='none of any kind', floor='none (the total is a plain sum and cannot be below 0)', bonus='none (removed); the total of a perfect sheet is 100',
        total='the sum of the points of the right places; a unit with rows scores the points printed in the key for each right row',
        number_and_trace_rule='right only when its value equals the key value exactly: full points, else 0, no partial credit, no tolerance; the marker enters the numbers',
        sheet_vs_question_page_rule='The question pages are the legal copy; where both exist and differ the question page counts; where only the sheet holds an answer the sheet counts.',
        key_fields_read='items[].type, answer, points, points_per_part, points_per_blank, and optionally n_options, n_responses, bank_codes; the guess-chance and penalty fields of the structure are never read',
        alternatives_per_closed_unit=ALTERNATIVES, answer_types=types,
        closed_units_blind_share_exact='1/5', closed_units_blind_note='every closed place has 5 alternatives, so the closed places together give exactly 1/5 of their points blind; the number and trace places add slightly more than their own near-zero chance. The blind total is exactly 20 only if all 100 points are closed.')


def main():
    a = argparse.ArgumentParser(); a.add_argument('cmd', choices=['write-rule', 'score', 'blind-figure']); a.add_argument('--out'); a.add_argument('--key'); a.add_argument('--marks')
    o = a.parse_args()
    if o.cmd == 'write-rule':
        txt = json.dumps(rule_table(), indent=1)
        if o.out:
            if os.path.exists(o.out): print('REFUSED: exists ' + o.out); sys.exit(2)
            open(o.out, 'w').write(txt + '\n')
        else: print(txt)
    elif o.cmd == 'blind-figure':
        e = expected_blind(json.load(open(o.key))); print({k: '%s = %.6f' % (v, float(v)) for k, v in e.items()})
    else: print(json.dumps(score(json.load(open(o.marks)), json.load(open(o.key))), indent=1))


if __name__ == '__main__': main()
