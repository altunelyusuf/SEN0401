#!/usr/bin/env python3
"""Adapter: turns the chapter-2 mock bank into the items-file shape of the real exam tools (a numeric template becomes 8 numeric items) and runs
readability R1 R2 R3 R4 R6 (v1.1.0, items mode, via its run_source) and clarity C1 to C5 (v1.0.1 CLI). Holds no item text; prints keys only.
R5 (cover directions) and the paper reader are NOT applicable to a bank. Usage: mock_rules_adapter_ch2_v1_0_0.py BANK.json ITEMS_OUT.json TOOLDIR"""
import json, os, re, subprocess, sys, importlib.util
sys.dont_write_bytecode = True
bank_path, out_path, tooldir = sys.argv[1:4]
bank = json.load(open(bank_path, encoding='utf-8'))
L = 'ABCDE'
def tip(t): return 'Tip: ' + t
items = []
def add(d): items.append(d)
for it in bank['items']:
    t = it['type']; i = it['id']
    if t == 'choice':
        add(dict(key=i, type='ChoiceFour', q=it['stem'], tip=tip(it['tip']), options=it['options'], answer=it['answer'],
                 solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'], why_wrong={L[int(k)]: v for k, v in it['why_wrong'].items()})))
    elif t == 'numeric':
        for n, ins in enumerate(it['instances'], 1):
            add(dict(key='%s#%d' % (i, n), type='NumericAnswer', q=ins['stem'], tip=tip(it['tip']), unit=it['unit'],
                     solution=dict(steps=[dict(text=s, number=re.findall(r'\d[\d,]*', s)[0]) for s in ins['steps']], why_right=ins['why_right'])))
    elif t == 'matching':
        add(dict(key=i, type='Matching', instruction=it['intro'], tip=tip(it['tip']), premises=[dict(text=p) for p in it['premises']], responses=it['responses'],
                 solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'], why_wrong={str(k + 1): v for k, v in enumerate(it['why_wrong_rows'])})))
    elif t == 'ordering':
        add(dict(key=i, type='Ordering', instruction=it['intro'], tip=tip(it['tip']), steps=it['steps'],
                 solution=dict(steps=[dict(text=s) for s in it['steps_solution']], why_right=it['why_right'], why_wrong={str(k + 1): v for k, v in enumerate(it['why_wrong_rows'])})))
    elif t == 'fill':
        used = {b['answer'] for b in it['blanks']}
        ww = it['why_wrong_entries']
        add(dict(key=i, type='FillBlankGroup', instruction=it['stem'], tip=tip(it['tip']),
                 blanks=[dict(text=b['sentence'], answer=it['bank'][b['answer']]) for b in it['blanks']],
                 distractors=[it['bank'][k] for k in range(5) if k not in used],
                 solution=dict(steps=[dict(text=s) for s in it['steps']], why_right=it['why_right'],
                               why_wrong={str(n + 1): ww[str(k)] for n, k in enumerate(sorted(ww, key=int)[:2])})))
json.dump(dict(items=items), open(out_path, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('adapter: %d items written (shape of the exam items file)' % len(items))
# readability, items mode
spec = importlib.util.spec_from_file_location('rd', os.path.join(tooldir, 'sen0401_exam_readability_check_v1_1_0.py'))
rd = importlib.util.module_from_spec(spec); spec.loader.exec_module(rd)
rule = rd.load_rule(os.path.join(tooldir, 'sen0401_exam_readability_rule_v1_1_0.json'))
units, tips = rd.read_items(out_path, rule)
res = rd.run_source('items file (bank)', units, None, tips, rule, False)
print('Readability v1.1.0, items mode, units %d' % len(units))
for r in ('R1', 'R2', 'R3', 'R4', 'R6'):
    x = res[r]
    if x['status'] != 'MEASURED': print('  %-3s NOT_MEASURED (%s)' % (r, x.get('why'))); continue
    print('  %-3s %s  fail %d of %d' % (r, 'FAIL' if x['fail'] else 'PASS', len(x['fail']), x['checked']))
    for tag, d in x['fail']: print('       - %s (%s)' % (tag, d))
print('  R5  NOT_MEASURED (a bank has no cover)')
bad = sum(len(res[r]['fail']) for r in ('R1', 'R2', 'R3', 'R6'))
# clarity
p = subprocess.run([sys.executable, '-B', os.path.join(tooldir, 'sen0401_exam_clarity_check_v1_0_1.py'), 'check', '--items', out_path], capture_output=True, text=True)
print(p.stdout.rstrip()); 
if p.stderr.strip(): print(p.stderr.strip())
sys.exit(0 if (bad == 0 and p.returncode == 0) else 1)
