#!/usr/bin/env python3
"""SEN0401 mock bank, chapter 5: adapter + readability v1.1.0 (R1 R2 R3 R4 R6) + clarity v1.0.1 (C1-C5) runner v1.0.0.
Turns the mock schema into the items-file shape (adapter, letters for the clarity why_wrong keys only, solutions in the bank stay index-based),
runs the two official checks unchanged on the whole chapter, and runs R6 again per item (every item is read alone, so every abbreviation must be spelled out inside the item).
Output holds item keys and counts only. The adapter file holds item text: private."""
import importlib.util, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
EXAM = '/home/claude/sen0401/08-tooling/exam'
BANK = os.path.join(HERE, 'mock_bank_ch5_v1_0_0.json')
ADAPTER = os.path.join(HERE, 'mock_items_adapter_ch5_v1_0_0.json')
RD = os.path.join(EXAM, 'sen0401_exam_readability_check_v1_1_0.py'); RDR = os.path.join(EXAM, 'sen0401_exam_readability_rule_v1_1_0.json')
CL = os.path.join(EXAM, 'sen0401_exam_clarity_check_v1_0_1.py'); CLR = os.path.join(EXAM, 'sen0401_exam_clarity_rule_v1_0_0.json')


def num(s):
    m = re.search(r'\d[\d,]*', s); return m.group(0) if m else ''


def adapt(bank):
    out = []; k = 0
    def add(**kw):
        nonlocal k; k += 1
        kw['sub_question'] = 'Q%d.%s' % (1 + (k - 1) // 26, chr(97 + (k - 1) % 26)); out.append(kw)
    for it in bank['items']:
        t = it['type']; tip = 'Tip: ' + it['tip']
        if t == 'choice':
            add(key=it['id'], type='ChoiceFive', q=it['stem'], tip=tip, options=it['options'], answer=it['answer'],
                solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'], why_wrong={chr(65 + int(i)): v for i, v in it['why_wrong'].items()}))
        elif t == 'numeric':
            for n, x in enumerate(it['instances'], 1):
                add(key='%s#%d' % (it['id'], n), type='NumericAnswer', q=x['stem'], tip=tip,
                    solution=dict(steps=[dict(text=s, number=num(s)) for s in x['steps']], why_right=x['why_right']))
        elif t == 'matching':
            add(key=it['id'], type='Matching', instruction=it['intro'], tip=tip, premises=[dict(text=p) for p in it['premises']], responses=it['responses'],
                solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])}))
        elif t == 'ordering':
            add(key=it['id'], type='Ordering', instruction=it['intro'], tip=tip, steps=it['steps'],
                solution=dict(steps=[dict(text=s) for s in it['steps_solution']], why_right=it['why_right'], why_wrong={str(i + 1): v for i, v in enumerate(it['why_wrong_rows'])}))
        elif t == 'fill':
            used = {b['answer'] for b in it['blanks']}
            add(key=it['id'], type='FillBlankGroup', instruction=it['stem'], tip=tip,
                blanks=[dict(text=b['sentence'], answer=it['bank'][b['answer']]) for b in it['blanks']],
                distractors=[e for i, e in enumerate(it['bank']) if i not in used],
                solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'],
                              why_wrong={str(i + 1): ' '.join(it['why_wrong_entries'].values()) for i in range(len(it['blanks']))}))
    return out


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def main():
    bank = json.load(open(BANK, encoding='utf-8'))
    items = adapt(bank)
    json.dump(dict(items=items), open(ADAPTER, 'w', encoding='utf-8'), ensure_ascii=False)
    print('Adapter: %d units (10 choice + 32 numeric instances + 3 matching + 2 ordering + 4 fill = %d); the mock schema has no format line, so R4 is NOT_MEASURED by the tool' % (len(items), len(items)))
    rc = 0
    # readability: the official CLI needs a paper; the official functions are called on the items file alone (same code path as the 'items file' source of the CLI)
    print('=' * 20, 'READABILITY v1.1.0 (whole chapter, official functions of the tool on the items file; no paper exists for a mock)')
    rd = load(RD, 'rd110'); rule = rd.load_rule(RDR); units, tips = rd.read_items(ADAPTER, rule)
    res = rd.run_source('items file', units, None, tips, rule, False)
    rd.print_report('items file', res)
    nf = sum(len(res[r]['fail']) for r in ('R1', 'R2', 'R3', 'R6')); print('RESULT %s' % ('PASS' if nf == 0 else 'FAIL')); rc |= nf > 0
    print('=' * 20, 'CLARITY v1.0.1 (whole chapter, official tool, CLI)')
    r = subprocess.run(['nice', '-n', '10', sys.executable, '-I', CL, 'check', '--items', ADAPTER, '--rule', CLR], capture_output=True, text=True)
    print(r.stdout.rstrip()); print(r.stderr.rstrip()) if r.stderr.strip() else None
    print('exit code', r.returncode); rc |= (r.returncode != 0)
    print('=' * 20, 'R6 per item (each item read alone)')
    bad = []
    for u in units:
        f = rd.check_r6([u], rule)
        if f: bad.append((u.key, f[u]))
    print('R6 per item: %s  fail %d of %d' % ('FAIL' if bad else 'PASS', len(bad), len(units)))
    for k, n in bad: print('   -', k, n, 'abbreviation(s) not spelled out')
    rc |= bool(bad)
    return rc


if __name__ == '__main__': sys.exit(main())
