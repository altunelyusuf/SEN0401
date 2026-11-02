#!/usr/bin/env python3
"""Adapter v1.0.2 (lineage agent): turns the instances of a mock family file (numeric templates) into the items-file shape and runs readability v1.1.0 (items mode, R1 R2 R3 R4 R6) and clarity v1.0.1 (C1 C2 C3 C5 items mode) on them. No item text is printed or stored in the repo.
Usage: python3 -I sen0401_mock_family_readability_adapter_v1_0_0.py FAMILY.json OUTDIR"""
import sys, json, os, subprocess
src, out = sys.argv[1], sys.argv[2]; os.makedirs(out, exist_ok=True)
d = json.load(open(src)); items = []
FMT = None
for it in d['items']:
    for k, x in enumerate(it['instances']):
        items.append({'key': '%s#%d' % (it['id'], k + 1), 'sub_question': 'Q2.a', 'type': 'NumericAnswer', 'chapters': [d['chapter']], 'points': it.get('points', 3),
                      'q': x['stem'], 'tip': 'Tip: ' + it['tip'].replace('Tip: ', '', 1) if it.get('tip') else None, 'needs_tip': True, 'format_line': 'Write the answer in %s, one digit in each box, starting from the right.' % (it.get('unit') or 'numbers'), 'how_to_answer': 'Write the answer in %s, one digit in each box, starting from the right.' % (it.get('unit') or 'numbers'),
                      'key_value': x['key_value'], 'unit': it.get('unit', ''), 'abbreviations': {}, 'intent': '',
                      'solution': {'steps': [{'text': t, 'number': (__import__('re').findall(r'\d[\d,]*', t) or [''])[0]} for t in x['steps']], 'why_right': x['why_right'], 'why_wrong': {}}})
p = os.path.join(out, 'family_items_shape.json'); json.dump({'items': items}, open(p, 'w'))
H = os.path.dirname(os.path.abspath(__file__))
import importlib.util
def load(n):
    sp = importlib.util.spec_from_file_location(n, os.path.join(H, n + '.py')); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
R = load('sen0401_exam_readability_check_v1_1_1'); rule = R.load_rule(os.path.join(H, 'sen0401_exam_readability_rule_v1_1_0.json'))
units, _ = R.read_items(p, rule)
for r, fn in (('R1', R.check_r1), ('R2', R.check_r2), ('R3', R.check_r3), ('R4', R.check_r4)):
    bad = [u.tag() for u in units if fn(u, rule)[0]]
    print('  %s  %s  fail %d of %d' % (r, 'FAIL' if bad else 'PASS', len(bad), len(units)), bad[:3] if bad else '')
f6 = R.check_r6(units, rule); print('  R6  %s  fail %d of %d' % ('FAIL' if f6 else 'PASS', len(f6), len(units)), list(f6)[:3] if f6 else '')
r = subprocess.run([sys.executable, '-I', os.path.join(H, 'sen0401_exam_clarity_check_v1_0_1.py'), 'check', '--items', p], capture_output=True, text=True)
print(''.join(l + '\n' for l in r.stdout.split('\n') if l.startswith(('  C', 'RESULT'))))
