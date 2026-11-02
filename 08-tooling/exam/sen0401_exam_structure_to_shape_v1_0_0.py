#!/usr/bin/env python3
"""Turns a structure (v1.3.1) plus its items file into a key SHAPE for the scoring check (--shape): unit types, row counts, points, digit counts. Holds no answer: letters, orders and numbers are placeholders ('7' repeated for the digit count).
Usage: structure_to_shape.py STRUCTURE.json ITEMS.json OUT.json"""
import json, sys, collections
sys.dont_write_bytecode = True
st = json.load(open(sys.argv[1], encoding='utf8')); its = {i['key']: i for i in json.load(open(sys.argv[2], encoding='utf8'))['items']}
out = []; groups = collections.OrderedDict()
for q in st['questions']:
    for s in q['sub']:
        it = its[s['item']]; t = s['type']; lab = s['label']
        if t == 'ChoiceFour': out.append(dict(label=lab, question=q['number'], type='ChoiceFive', points=s['points'], answer={lab: 'A'}))
        elif t == 'Matching': out.append(dict(label=lab, question=q['number'], type=t, points=s['points'], points_per_part=s['points_per_part'], answer={'%s%d' % (lab, n + 1): 'A' for n in range(s['parts'])}))
        elif t == 'Ordering': out.append(dict(label=lab, question=q['number'], type=t, points=s['points'], points_per_part=s['points_per_part'], answer={'%s%d' % (lab, n + 1): n + 1 for n in range(s['parts'])}))
        elif t == 'FillBlankGroup':
            g = groups.setdefault(s['item'], dict(label=s['item'].split(':')[1], question=q['number'], type=t, points=0, points_per_blank={}, answer={}))
            g['points'] += s['points']; g['points_per_blank'][lab] = s['points']; g['answer'][lab] = '11'
        else:
            v = str(it['key_value'] if t == 'NumericAnswer' else it['output']); d = len(v.replace('-', '').replace('.', ''))
            out.append(dict(label=lab, question=q['number'], type=t, points=s['points'], answer={lab: (dict(value=int('7' * d), unit='u', tolerance=0) if t == 'NumericAnswer' else '7' * d)}))
out += list(groups.values())
json.dump(dict(items=out), open(sys.argv[3], 'w'), indent=1)
print('shape units', len(out), 'points', sum(i['points'] for i in out))
