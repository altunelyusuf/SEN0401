#!/usr/bin/env python3
"""SEN0401 mock bank -> rule tools adapter, chapter 6, version 1.0.0. Holds no question and no answer; prints item ids only.
The readability checker v1.1.0 and the clarity checker v1.0.1 read the items-file shape of the paper builder, not the mock schema.
This adapter turns a mock bank into that shape (written to a temporary file next to the bank, then deleted) and calls the two tools' own functions
(nothing is copied or weakened): readability R1, R2, R3, R4, R6 and clarity C1 to C5. R5 (cover directions) has no object in a bank and is NOT_MEASURED.
R4 (answer-format line) is measured on a format line that the adapter synthesises for numeric items ('Write the result in the boxes, in <unit>.'),
because the real line is printed by the HTML shell. R6 is run twice: over the whole chapter in reading order, and for every item alone (stricter,
because a derived mock may draw any item first).
Usage: mock_rules_adapter_ch6_v1_0_0.py --bank BANK.json --exam-dir DIR_OF_THE_TOOLS"""
import argparse, importlib.util, json, os, re, sys
sys.dont_write_bytecode = True


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def to_items(bank):
    out = []; k = 0
    def lab():
        nonlocal k
        s = 'Q%d.%s' % (k // 26 + 1, chr(97 + k % 26)); k += 1; return s
    for it in bank['items']:
        t = it['type']
        if t == 'choice':
            ww = {chr(65 + int(i)): v for i, v in it['why_wrong'].items()}
            out.append(dict(key=it['id'], type='Choice', sub_question=lab(), q=it['stem'], tip='Tip: ' + it['tip'], options=it['options'], answer=it['answer'],
                            solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong=ww)))
        elif t == 'numeric':
            for n, ins in enumerate(it['instances'], 1):
                steps = [dict(text=s, number=''.join(re.findall(r'\d+', s))) for s in ins['steps']]
                out.append(dict(key='%s#%d' % (it['id'], n), type='NumericAnswer', sub_question=lab(), q=ins['stem'], tip='Tip: ' + it['tip'], unit=it['unit'],
                                format_line='Write the result in the boxes, in %s.' % it['unit'],
                                solution=dict(steps=steps, why_right=ins['why_right'])))
        elif t == 'matching':
            out.append(dict(key=it['id'], type='Matching', sub_question=lab(), instruction=it['intro'], tip='Tip: ' + it['tip'],
                            premises=[dict(text=p) for p in it['premises']], responses=it['responses'],
                            solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'ordering':
            out.append(dict(key=it['id'], type='Ordering', sub_question=lab(), instruction=it['intro'], tip='Tip: ' + it['tip'], steps=it['steps'],
                            solution=dict(steps=it['steps_solution'], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'fill':
            wr = it['why_wrong_entries']; ans = [b['answer'] for b in it['blanks']]
            rows = {str(i + 1): wr[str(a)] for i, a in enumerate(ans)}
            out.append(dict(key=it['id'], type='FillBlankGroup', sub_question=lab(), instruction=it['stem'], tip='Tip: ' + it['tip'],
                            blanks=[dict(text=b['sentence'], answer=it['bank'][b['answer']]) for b in it['blanks']],
                            distractors=[e for j, e in enumerate(it['bank']) if j not in ans],
                            solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong=rows)))
    return dict(items=out)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--bank', required=True); ap.add_argument('--exam-dir', required=True); a = ap.parse_args()
    bank = json.load(open(a.bank, encoding='utf-8')); items = to_items(bank)
    tmp = os.path.join(os.path.dirname(os.path.abspath(a.bank)), '_adapter_tmp_items.json')
    json.dump(items, open(tmp, 'w', encoding='utf-8'))
    fails = 0
    try:
        rd = load(os.path.join(a.exam_dir, 'sen0401_exam_readability_check_v1_1_0.py'), 'rd'); rrule = rd.load_rule(os.path.join(a.exam_dir, 'sen0401_exam_readability_rule_v1_1_0.json'))
        cl = load(os.path.join(a.exam_dir, 'sen0401_exam_clarity_check_v1_0_1.py'), 'cl'); crule = cl.load(os.path.join(a.exam_dir, 'sen0401_exam_clarity_rule_v1_0_0.json'))
        units, _ = rd.read_items(tmp, rrule)
        print('Rule adapter v1.0.0  chapter %s  units %d (numeric instances count as units)' % (bank.get('chapter'), len(units)))
        print('READABILITY v1.1.0 (tool: sen0401_exam_readability_check_v1_1_0.py, functions called as they are)')
        for r, fn in (('R1', rd.check_r1), ('R2', rd.check_r2), ('R3', rd.check_r3), ('R4', rd.check_r4)):
            bad = [(u.tag(), d) for u in units for b, d in [fn(u, rrule)] if b]
            print('  %-3s %s  fail %d of %d' % (r, 'FAIL' if bad else 'PASS', len(bad), len(units)))
            for t, d in bad: print('         - %s (%s)' % (t.split(' [')[0], d))
            fails += len(bad)
        f6 = rd.check_r6(units, rrule)
        print('  R6  %s  chapter in reading order: unexpanded abbreviations in %d unit(s)' % ('FAIL' if f6 else 'PASS', len(f6)))
        for u, n in f6.items(): print('         - %s (%d)' % (u.key, n))
        fails += len(f6)
        solo = {}
        for u in units:
            x = rd.check_r6([u], rrule)
            if x: solo[u.key] = list(x.values())[0]
        print('  R6  %s  every unit alone: unexpanded abbreviations in %d unit(s)' % ('FAIL' if solo else 'PASS', len(solo)))
        for k, n in solo.items(): print('         - %s (%d)' % (k, n))
        fails += len(solo)
        print('  R5  NOT_MEASURED  no cover in a bank')
        cu = cl.read_items(tmp, crule)
        print('CLARITY v1.0.1 (tool: sen0401_exam_clarity_check_v1_0_1.py, functions called as they are)')
        res = cl.run_items(cu, crule)
        for r in cl.RULES:
            x = res[r]; print('  %-3s %s  fail %d of %d' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked']))
            for t, d in x['fail']: print('         - %s (%s)' % (t.split(' [')[0], d))
            fails += len(x['fail'])
        print('  C4b NOT_MEASURED  every option plausible, no trick wording (human judgement)')
    finally:
        if os.path.exists(tmp): os.remove(tmp)
    print('RESULT %s' % ('PASS' if fails == 0 else 'FAIL (%d failure line(s))' % fails))
    return 0 if fails == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
