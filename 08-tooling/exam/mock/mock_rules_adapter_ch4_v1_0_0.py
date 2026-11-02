#!/usr/bin/env python3
"""Adapter v1.0.0 (no question or answer text inside): turns the mock bank of one chapter into the items-file shape of the exam tools
and runs readability v1.1.0 (R1, R2, R3, R4, R6) and clarity v1.0.1 (C1..C5) in items mode. The mock schema is not read by those tools, hence this adapter.
Letters appear only here, in the adapter, as keys of why_wrong that the clarity rule C3 asks for; the bank itself never holds a letter.
R6 is run item by item (each item alone), because a mock item must spell out its own abbreviations wherever it is drawn.
R4 needs answer-format lines; the mock bank holds none (the shell prints them): NOT_MEASURED.
Usage: mock_rules_adapter_ch4_v1_0_0.py [--bank FILE] [--workdir DIR]"""
import argparse, importlib.util, json, os, re, sys, tempfile
sys.dont_write_bytecode = True
EXAM = '/home/claude/sen0401/08-tooling/exam'
PRIV = '/home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts'

def load_mod(path, name):
    s = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

def convert(bank):
    out = []; L = 'ABCDE'
    for it in bank['items']:
        t = it['type']; k = it['id']
        if t == 'choice':
            a = it['answer']
            out.append(dict(key=k, type='ChoiceFive', q=it['stem'], tip=it['tip'], options=it['options'], answer=a,
                            solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong={L[int(i)]: v for i, v in it['why_wrong'].items()})))
        elif t == 'numeric':
            for j, ins in enumerate(it['instances'], 1):
                st = [dict(text=s, number=re.search(r'\d+', s).group(0)) for s in ins['steps']]
                out.append(dict(key='%s#%d' % (k, j), type='NumericAnswer', q=ins['stem'], tip=it['tip'], solution=dict(steps=st, why_right=ins['why_right'])))
        elif t == 'matching':
            out.append(dict(key=k, type='Matching', instruction=it['intro'], tip=it['tip'], premises=[dict(text=p) for p in it['premises']], responses=it['responses'],
                            solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'ordering':
            out.append(dict(key=k, type='Ordering', instruction=it['intro'], tip=it['tip'], steps=it['steps'],
                            solution=dict(steps=it['steps_solution'], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])})))
        elif t == 'fill':
            ans = [b['answer'] for b in it['blanks']]; dis = [i for i in range(len(it['bank'])) if i not in ans]
            ww = {str(j + 1): '; '.join(it['why_wrong_entries'][str(i)] for i in dis) for j in range(len(it['blanks']))}
            out.append(dict(key=k, type='FillBlankGroup', instruction=it['stem'], tip=it['tip'], blanks=[dict(text=b['sentence'], answer=it['bank'][b['answer']]) for b in it['blanks']],
                            distractors=[it['bank'][i] for i in dis], solution=dict(steps=it['steps'], why_right=it['why_right'], why_wrong=ww)))
    return out

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--bank', default=os.path.join(PRIV, 'mock_bank_ch4_v1_0_0.json')); ap.add_argument('--workdir', default=tempfile.mkdtemp(prefix='mockadapt_'))
    a = ap.parse_args()
    bank = json.load(open(a.bank, encoding='utf-8')); items = convert(bank)
    path = os.path.join(a.workdir, 'items_ch%d.json' % bank['chapter']); json.dump(dict(items=items), open(path, 'w', encoding='utf-8'))
    rd = load_mod(os.path.join(EXAM, 'sen0401_exam_readability_check_v1_1_0.py'), 'rd')
    cl = load_mod(os.path.join(EXAM, 'sen0401_exam_clarity_check_v1_0_1.py'), 'cl')
    rrule = rd.load_rule(os.path.join(EXAM, 'sen0401_exam_readability_rule_v1_1_0.json'))
    units, tips = rd.read_items(path, rrule)
    res = rd.run_source('mock bank chapter %d (%d units)' % (bank['chapter'], len(units)), units, None, tips, rrule, False)
    solo = []
    for u in units:
        f = rd.check_r6([u], rrule)
        if f: solo.append((u.tag(), '%d abbreviation(s) not spelled out inside the item' % sum(f.values())))
    res['R6'] = dict(status='MEASURED', fail=solo, checked=len(units))
    print('Readability v1.1.0 on the mock bank (items mode; R6 item by item; R5 and R4 NOT_MEASURED here)')
    rd.print_report('mock bank (%d units: %d choice items, numeric instances, matching, ordering, fill)' % (len(units), sum(1 for i in items if i['type'] == 'ChoiceFive')), res)
    crule = cl.load(os.path.join(EXAM, 'sen0401_exam_clarity_rule_v1_0_0.json'))
    cu = cl.read_items(path, crule); cr = cl.run_items(cu, crule)
    print('Clarity v1.0.1 on the mock bank (items mode)')
    cl.print_report('mock bank', cr)
    print('C4b  NOT_MEASURED  every option plausible, no trick wording (a human judgement)')
    nf = sum(len(res[r]['fail']) for r in ('R1', 'R2', 'R3', 'R6')) + sum(len(cr[r]['fail']) for r in cr)
    print('RESULT %s (%d failing unit-rule pair(s))' % ('PASS' if nf == 0 else 'FAIL', nf))
    return 0 if nf == 0 else 1

if __name__ == '__main__': sys.exit(main())
