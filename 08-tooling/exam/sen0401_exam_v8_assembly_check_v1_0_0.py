#!/usr/bin/env python3
"""SEN0401 midterm v8.0.0, X3a assembly check (new file). Holds no question and no answer; it prints labels, item keys, counts and PASS/FAIL only.
Usage: check.py BUILD_DIR --tag TAG --structure STRUCT.json --order-from V7_MEASURE.json --v7-key V7_KEY.json --map ASSEMBLY_MAP.json --items-dir ITEMS_DIR [--deliver DIR]
Checks (each PASS / FAIL, NOT_MEASURED is never a pass):
  A1 pages: paper + sheet at most 7, sheet exactly 1 (pdfinfo)         A2 the printed order (labels and structure keys) equals the recorded order of v7.2.2
  A3 total points 100, per-question totals and the points of every printed label equal the v7.2.0 key;  option counts (choice 5, matching responses 5, fill-in bank 5) equal
  A4 key letters equal printed letters: for every closed place the letter of the key is the letter printed in the extracted paper PDF text in front of the option / response / bank entry that is the right one
  A5 every numeric key is RECOMPUTED by running the code of its controlled item file and equals the key.json value and the value in the key docx
  A6 sheet labels equal paper labels (unit labels of the sheet layout = the closed unit labels printed on the paper docx; rows = places of the key)
  A7 the folder to deliver (if --deliver) holds exactly paper docx, paper pdf, key docx, sheet pdf, MANIFEST_SHA256 and `sha256sum -c` passes"""
import argparse, json, os, re, subprocess, sys, zipfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from docx import Document
ap = argparse.ArgumentParser(); ap.add_argument('build'); ap.add_argument('--tag', required=True); ap.add_argument('--structure', required=True); ap.add_argument('--order-from', required=True)
ap.add_argument('--v7-key', required=True); ap.add_argument('--map', required=True); ap.add_argument('--items-dir', required=True); ap.add_argument('--deliver'); x = ap.parse_args()
D, TAG = x.build, x.tag; f = lambda e: os.path.join(D, TAG + e); res = []
def rep(name, ok, detail=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok is True else 'FAIL' if ok is False else 'NOT_MEASURED', name, detail), flush=True)
norm = lambda t: re.sub(r'\s+', ' ', t.replace(' ', ' ')).strip()
pages = lambda p: int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1))
key = json.load(open(f('_key.json'))); k7 = json.load(open(x.v7_key)); meas = json.load(open(f('_measure.json'))); m7 = json.load(open(x.order_from))
pp, sp = pages(f('_paper.pdf')), pages(f('_sheet.pdf'))
rep('A1 pages: paper %d + sheet %d = %d (at most 7, sheet exactly 1)' % (pp, sp, pp + sp), pp + sp <= 7 and sp == 1)
rep('A2 printed order (label, structure key, type) equals the recorded order of v7.2.2: %d positions' % len(m7['order']), [tuple(o) for o in meas['order']] == [tuple(o) for o in m7['order']])
lab = lambda k: {e['label']: e for e in k['items']}; a, b = lab(key), lab(k7)
okp = set(a) == set(b) and all(a[l]['points'] == b[l]['points'] and a[l]['type'] == b[l]['type'] and a[l]['question'] == b[l]['question'] for l in a)
rep('A3a total %s = %s; question totals %s = %s' % (key['total_points'], k7['total_points'], key['question_totals'], k7['question_totals']), key['total_points'] == k7['total_points'] == 100 and key['question_totals'] == k7['question_totals'] and sum(e['points'] for e in key['items']) == 100)
rep('A3b points, type and question of every printed label equal v7.2.0 (%d labels)' % len(a), okp)
cnt = lambda e: e.get('n_options') or e.get('n_responses') or len(e.get('bank_codes') or []) or len(e['answer'])
rep('A3c option / response / bank / row counts of every label equal v7.2.0', all(cnt(a[l]) == cnt(b[l]) for l in a if a[l]['type'] != 'NumericAnswer'))
rep('A3d row points per place equal v7.2.0', all(a[l].get('row_points') == b[l].get('row_points') and a[l].get('points_per_blank') == b[l].get('points_per_blank') for l in a))
rep('A3e item keys that changed: %s' % sorted(l for l in a if a[l]['item_key'] != b[l]['item_key']), True)
# A4 printed letters
txt = norm(subprocess.run(['pdftotext', f('_paper.pdf'), '-'], capture_output=True, text=True).stdout)
import sen0401_exam_paper_lib_v8_0_0 as L
L.set_cfg(meas['config'])
paper = L.make_form(1, 5701, structure_path=os.path.abspath(x.structure), fixed_skeys=[o[1] for o in m7['order']])
PI = {i['label']: i for i in paper['items']}
def seen(prefix, label_text):
    return norm(prefix) + ' ' + norm(label_text)[:38] in txt or norm(prefix) + norm(label_text)[:38] in txt
bad = []; n = 0
for l, e in a.items():
    it = PI[l]; t = e['type']
    for p, ans in e['answer'].items():
        if t == 'NumericAnswer': continue
        n += 1
        if t == 'ChoiceFour':
            opt = it['options']['ABCDE'.index(ans)]
            if not seen(ans + '.', opt): bad.append((p, 'option'))
        elif t == 'Matching':
            k = int(p[len(l):]) - 1; resp = it['responses']['ABCDE'.index(ans)]
            if it['responses'].index(it['premises'][k]['match']) != 'ABCDE'.index(ans): bad.append((p, 'key'))
            if not seen(ans + '.', resp) or not seen('%d)' % (k + 1), it['premises'][k]['text']): bad.append((p, 'printed'))
        elif t == 'Ordering':
            j = int(p[len(l):]) - 1; step = it['steps'][it['display_order'][j]]
            if it['display_order'][j] + 1 != ans or not seen('%d)' % (j + 1), step): bad.append((p, 'printed'))
        elif t == 'FillBlankGroup':
            ents = [bk["answer"] for bk in it["blanks"]] + list(it["distractors"])
            idx = [i2 for i2, s_ in enumerate(paper['slots']) if s_['item']['label'] == l][0]; s = paper['slots'][idx]; b_ = s['letters'].index(p[len(str(s['q'])):])
            if not seen(ans + '.', ents[b_]): bad.append((p, 'bank'))
rep('A4 key letters / places equal the letters printed in the extracted PDF text: %d closed places, %d mismatches %s' % (n, len(bad), bad[:6]), not bad and n > 0)
# key.docx letters
kd = '\n'.join(p.text for p in Document(f('_key.docx')).paragraphs)
rep('A4b every "Correct answer: X" line of the key docx for a choice item names the key place letter', all(re.search(r'Correct answer: %s\.' % a[l]['answer'][l], kd) for l in a if a[l]['type'] == 'ChoiceFour'))
# A5 recompute
mp = json.load(open(x.map))['items']; okn = []; badn = []
for m in mp:
    if m['kind'] != 'numeric': continue
    nf = json.load(open(os.path.join(x.items_dir, m['file']))); ns = {}
    if 'recompute' in nf: exec(nf['recompute'], ns); r = ns['recompute']()
    else: exec(nf['recompute_python'], ns); r = ns['recompute'](nf['data'])
    ent = [e for e in key['items'] if e['item_key'] == m['new']][0]; kv = list(ent['answer'].values())[0]['value']
    (okn if r == kv == m['key_value'] and ('%s' % kv) in re.sub(r'[,\s]', '', kd) else badn).append((ent['label'], m['new'], r, kv))
rep('A5 numeric keys recomputed by running the item code = key.json = key docx: %d of 8 %s' % (len(okn), [(o[0], o[2]) for o in okn]), len(okn) == 8 and not badn, str(badn))
# A6 sheet labels
lay = json.load(open(f('_sheet_layout.json'))); slab = [u['no'] for b_ in lay['blocks'] for u in b_['units']]
pl = [p.text for p in Document(f('_paper.docx')).paragraphs]
plabs = set(re.match(r'(\d[a-h])(?:-\d[a-h])?\. ', t).group(1) for t in pl if re.match(r'\d[a-h](?:-\d[a-h])?\. ', t))
closed = [pl_ for e in key['items'] if e['type'] != 'NumericAnswer' for pl_ in e['answer']]
rep('A6 sheet rows = closed places of the key (%d), each once; every sheet unit label is printed on the paper' % len(closed), sorted(slab) == sorted(closed) and len(set(slab)) == len(slab))
unitlabs = {e['label'] for e in key['items'] if e['type'] != 'NumericAnswer'}
rep('A6b every closed unit label of the key is printed on the paper docx (%d units); numeric labels also (%d)' % (len(unitlabs), len([e for e in key['items'] if e['type'] == 'NumericAnswer'])), unitlabs <= plabs and {e['label'] for e in key['items']} <= plabs)
if x.deliver:
    names = sorted(os.listdir(x.deliver)); want = sorted([TAG + e for e in ('_paper.docx', '_paper.pdf', '_key.docx', '_sheet.pdf')] + ['MANIFEST_SHA256'])
    rep('A7a delivery folder holds exactly %s' % want, names == want, str(names))
    r = subprocess.run(['sha256sum', '-c', 'MANIFEST_SHA256'], cwd=x.deliver, capture_output=True, text=True); print(r.stdout.strip())
    rep('A7b sha256sum -c MANIFEST_SHA256', r.returncode == 0 and r.stdout.count(': OK') == 4)
print('RESULT: %d PASS, %d FAIL, %d NOT_MEASURED' % (res.count(True), res.count(False), res.count(None)))
sys.exit(1 if False in res else 0)
