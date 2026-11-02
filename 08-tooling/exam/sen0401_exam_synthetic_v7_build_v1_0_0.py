#!/usr/bin/env python3
"""SEN0401 exam v7 SYNTHETIC items and structure generator, version 1.0.0 (new file).
SYNTHETIC INPUT: every question, option, step and tip written here is an invented placeholder ('Synthetic question N'). No real question, no real answer, no course content.
It writes ONE items file and ONE structure file with the SAME FIELD NAMES as the items v1.6.0 / structure v1.3.0 (five alternatives per closed unit, 'tip' string and 'needs_tip',
whole-number row points, no bonus, 100 points) so that the papers tooling v7 can be run before the real items exist. The files carry synthetic=true and are never delivered.
The code-trace outputs and the numbers are computed here by running the placeholder code (the same rule as the real items: every key recomputed by running the code).
Usage: sen0401_exam_synthetic_v7_build_v1_0_0.py OUTDIR [--seed 7001]   (refuses to overwrite)"""
import argparse, contextlib, io, json, os, random, sys
sys.dont_write_bytecode = True
VERSION = '1.0.0'
DISCLOSURE = 'SYNTHETIC INPUT: invented placeholder wording, not a real exam; never delivered.'
CHAPTERS = [1, 2, 3, 4, 5, 6]
LET = 'ABCDE'


def run(code):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(code, {})
    return buf.getvalue().strip()


def stem(n):
    return 'Synthetic question %d. This placeholder stem has filler words so that the layout measures a stem of realistic length; it asks for no course knowledge and its answer is only in the key.' % n


def tip(n): return 'Tip: Synthetic tip for question %d, nine words at most.' % n


def build(seed):
    rnd = random.Random(seed); items = []; n = 0
    def base(key, typ, chs, bloom, kind):
        return dict(key=key, type=typ, chapters=chs, bloom=bloom, kind=kind, source=dict(file='SYNTHETIC', locator='synthetic placeholder'), sources=[], critical_points=['CP%d.01' % chs[0]], seeds=[],
                    no_seed_reason='synthetic placeholder item: no page item is its seed', papers=['midterm'], terms=[], abbreviations={}, synthetic=True)
    # Q1: seven choice items, five options each
    q1_pts = [4, 4, 4, 4, 3, 3, 3]
    for i in range(7):
        n += 1; it = base('syn:c%d' % (i + 1), 'ChoiceFour', [CHAPTERS[i % 6], CHAPTERS[(i + 2) % 6]], [3, 4, 3, 4, 2, 3, 4][i], 'synthesis' if i % 2 else 'direct')
        opts = ['Synthetic option %s of question %d, with a few filler words to give a realistic option length for the layout.' % (LET[k], n) for k in range(5)]
        it.update(q=stem(n), options=opts, answer=rnd.randrange(5), n_options=5, tip=tip(n) if i % 3 != 2 else '', needs_tip=i % 3 != 2, sub_question='Q1.%s' % 'abcdefg'[i],
                  how_to_answer='Write the letter of the one correct statement in the box.')
        items.append((it, q1_pts[i]))
    # Q2: eight hand-written answers: numbers (N) and code traces (T)
    kinds = 'NNTNTNTN'; q2_pts = [3, 3, 3, 3, 3, 3, 4, 3]
    for i, kd in enumerate(kinds):
        n += 1
        if kd == 'N':
            it = base('syn:n%d' % (i + 1), 'NumericAnswer', [CHAPTERS[(i + 1) % 6]], 3, 'direct'); a, b = rnd.randrange(3, 40), rnd.randrange(3, 40)
            it.update(q='Synthetic question %d. A placeholder calculation with two given numbers, %d and %d, whose product is asked; the unit is in the answer line.' % (n, a, b), key_value=a * b, unit='units', tolerance=0,
                      data=dict(model='synthetic_product', a=a, b=b), how_to_answer='Write the answer in units, one digit in each box, starting from the right.')
        else:
            it = base('syn:t%d' % (i + 1), 'CodeTrace', [CHAPTERS[(i + 3) % 6]], 3, 'direct'); a, b = rnd.randrange(3, 20), rnd.randrange(3, 20)
            code = 'a = %d\nb = %d\nfor i in range(3):\n    a = a + b\nprint(a)' % (a, b)
            it.update(q='Synthetic question %d. Follow the placeholder program and give the number that it prints.' % n, code=code, output=run(code), how_to_answer='Write the number that the program prints, one digit in each box, starting from the right.')
        it.update(tip=tip(n), needs_tip=True, sub_question='Q2.%s' % 'abcdefgh'[i])
        items.append((it, q2_pts[i]))
    # Q3: one ordering (5 steps, rows 1,2,2,2,1) and two matchings (4 premises, 5 responses, rows 2,2,2,2 and 3,2,2,2)
    n += 1; it = base('syn:o1', 'Ordering', [2, 3], 3, 'direct')
    it.update(steps=['Synthetic step %s of the placeholder sequence, with filler words for length.' % 'ABCDE'[k] for k in range(5)], instruction='Put the five synthetic steps in the order of the key, from the first to the last.',
              row_points=[1, 2, 2, 2, 1], how_to_answer='Write in the box beside each step its place, 1 for the earliest and 5 for the latest.', tip=tip(n), needs_tip=True, sub_question='Q3.a')
    items.append((it, 8))
    for j, rows in enumerate(([2, 2, 2, 2], [3, 2, 2, 2])):
        n += 1; it = base('syn:m%d' % (j + 1), 'Matching', [4, 5, 6], 3, 'synthesis')
        it.update(premises=[dict(text='Synthetic premise %d of matching %d, with filler words.' % (k + 1, j + 1), match='Synthetic response %s of matching %d, with filler words.' % ('ABCD'[k], j + 1)) for k in range(4)],
                  responses=['Synthetic response %s of matching %d, with filler words.' % (c, j + 1) for c in 'ABCDE'], n_responses=5, instruction='Match each synthetic premise (left) with the response (right) that fits it. One response is not used.',
                  row_points=rows, how_to_answer='Write in the box beside each premise the letter of the response that fits it; one is not used.', tip=tip(n), needs_tip=True, sub_question='Q3.%s' % 'bc'[j])
        items.append((it, sum(rows)))
    # Q4: three fill-in groups, two blanks each, bank of five entries
    q4_pts = [(4, 4), (4, 4), (5, 4)]
    for g in range(3):
        n += 1; it = base('syn:f%d' % (g + 1), 'FillBlankGroup', [CHAPTERS[(g + 3) % 6], 2], 2, 'direct')
        it.update(blanks=[dict(text='Synthetic sentence %d of group %d with a gap ____ for the entry.' % (b + 1, g + 1), answer='synthetic entry %s of group %d' % ('PQ'[b], g + 1)) for b in range(2)],
                  distractors=['synthetic entry %s of group %d' % (c, g + 1) for c in 'RST'], instruction='Fill each synthetic blank with the entry of the synthetic bank that fits it.', bank_size=5, bank_letters='ABCDE',
                  how_to_answer='Write in the box beside each blank the letter of the bank entry that makes the sentence true.', tip=tip(n), needs_tip=True, sub_question='Q4.%s' % 'abc'[g])
        items.append((it, sum(q4_pts[g])))
    return items, q1_pts, q2_pts, q4_pts


def structure(items, q1_pts, q2_pts, q4_pts, items_file):
    by = {it['key']: it for it, _ in items}; qs = []
    def sub(q, label, it, pts, typ, **kw):
        s = dict(key='Q%d.%s' % (q, label), item=it['key'], type=typ, block=typ, points=pts, units=1, chapters=it['chapters'], bloom=it['bloom'], label='%d%s' % (q, label), how_to_answer=it['how_to_answer'],
                 chance='1/5' if typ not in ('NumericAnswer', 'CodeTrace') else '1/10', tip=it.get('tip') or None, tip_of_item_printed_under_label='%d%s' % (q, label))
        s.update(kw); return s
    q1 = [sub(1, 'abcdefg'[i], by['syn:c%d' % (i + 1)], q1_pts[i], 'ChoiceFour') for i in range(7)]
    q2 = []
    for i, kd in enumerate('NNTNTNTN'):
        it = by['syn:%s%d' % (kd.lower(), i + 1)]; q2.append(sub(2, 'abcdefgh'[i], it, q2_pts[i], it['type']))
    q3 = [sub(3, 'a', by['syn:o1'], 8, 'Ordering', parts=5, row_points=by['syn:o1']['row_points'], instruction=by['syn:o1']['instruction'])]
    for j in range(2): it = by['syn:m%d' % (j + 1)]; q3.append(sub(3, 'bc'[j], it, sum(it['row_points']), 'Matching', parts=4, row_points=it['row_points'], instruction=it['instruction']))
    q4 = []
    for g in range(3):
        it = by['syn:f%d' % (g + 1)]
        for b in range(2): q4.append(sub(4, 'abcdef'[2 * g + b], it, q4_pts[g][b], 'FillBlankGroup', blank=b + 1, points_per_blank=q4_pts[g][b]))
    Q = [dict(number=1, title='Reading and choice', points=25, instruction='Read each situation. Mark the one statement that is correct.', sub=q1),
         dict(number=2, title='Calculation and tracing', points=25, instruction='Work out each number, by calculation or by following the program. At most five characters.', sub=q2),
         dict(number=3, title='Ordering and matching', points=25, instruction='Put, match and write the answers in the boxes beside the parts.', sub=q3),
         dict(number=4, title='Fill in the sentence', points=25, instruction='Each group has its own bank of five entries. Choose for each blank the entry that makes the sentence true.', sub=q4)]
    for q in Q: assert sum(s['points'] for s in q['sub']) == q['points'], (q['number'], sum(s['points'] for s in q['sub']))
    return dict(version='7.0.0-synthetic', synthetic=True, disclosure=DISCLOSURE, items_file=items_file, one_form=True, forms=1, seed_for_sub_question_order=5701, chapters=CHAPTERS, questions_main=4, questions=Q, total_points=100,
                scoring_rule=dict(rule='a right answer scores its points; every other answer scores 0; no deduction, no floor, no bonus', total=100))


def main():
    a = argparse.ArgumentParser(); a.add_argument('outdir'); a.add_argument('--seed', type=int, default=7001); x = a.parse_args()
    os.makedirs(x.outdir, exist_ok=True)
    pi = os.path.join(x.outdir, 'sen0401_exam_items_SYNTHETIC_v7_0_0.json'); ps = os.path.join(x.outdir, 'sen0401_exam_structure_SYNTHETIC_v7_0_0.json')
    for p in (pi, ps):
        if os.path.exists(p): print('REFUSED: exists ' + p); sys.exit(2)
    items, q1, q2, q4 = build(x.seed)
    for it, _p in items: it['format_line'] = it['how_to_answer']
    for it, pts in items: it['points'] = pts if it['type'] in ('NumericAnswer', 'CodeTrace') else it.get('points', pts)
    st = structure(items, q1, q2, q4, pi)
    json.dump(dict(note=DISCLOSURE, version='7.0.0-synthetic', synthetic=True, chapters=CHAPTERS, one_form=True, items=[it for it, _ in items]), open(pi, 'w'), indent=1)
    json.dump(st, open(ps, 'w'), indent=1)
    print(DISCLOSURE); print('items', len(items), 'units', sum(len(i['blanks']) if i['type'] == 'FillBlankGroup' else 1 for i, _ in items), 'points', sum(q['points'] for q in st['questions'])); print(pi); print(ps)


if __name__ == '__main__': main()
