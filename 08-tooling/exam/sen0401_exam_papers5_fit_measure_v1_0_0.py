#!/usr/bin/env python3
"""sen0401_exam_papers5_fit_measure v1_0_0 - NEW FILE (executor SEN0401-I62-papers5). Measures, on the LibreOffice render of the paper v5 (the paper PDF exported by the builder), whether any text overflows or is cut:
  F1 every word of the question pages of the .docx (python-docx text, cover and footer excluded) appears in the render, the same number of times (nothing cut, nothing lost);
  F2 no word of a question page crosses the right edge of its column (+0.5 pt) or the page margin;
  F3 every sub-question lies in ONE column of ONE page (no split across columns), found by its printed label;
  F4 for the owner cases C2 (the fill group 4a-4b, item mt3:i07) and C3 (item 1a, mt2:i02) and for the longest sub-question of the paper by line count: page, column, number of lines, widest line right edge against the column edge, lowest line against the bottom of the frame.
Usage: fit_measure DIR  (reads sen0401_exam_midterm_v5_0_0_paper.docx / _paper.pdf / _measure.json in DIR; prints; exit 0 only if F1 to F3 hold)"""
import collections, json, os, re, sys
sys.dont_write_bytecode = True
import pdfplumber
from docx import Document
D = sys.argv[1]; T = 'sen0401_exam_midterm_v5_0_0'
meas = json.load(open(os.path.join(D, T + '_measure.json'))); cfg = meas['cfg']
A4W, A4H = 210.0, 297.0; PT = 72 / 25.4
side, gap, n = cfg['side'], cfg['colgap'], cfg['cols']; colw = (A4W - 2 * side - (n - 1) * gap) / n * PT
left = [side * PT, (side + (A4W - 2 * side - gap) / 2 + gap) * PT]; right = [l + colw for l in left]
frame_top = 10.0 * PT; frame_bottom = (A4H - 14.0) * PT
ok = True
def rep(name, good, detail):
    global ok; ok &= bool(good); print('PASS ' if good else 'FAIL ', name, detail)
doc = Document(os.path.join(D, T + '_paper.docx')); paras = [p.text for p in doc.paragraphs]
start = [i for i, t in enumerate(paras) if t.startswith('SEN0401 Special Topics: Blockchain - Midterm exam')][0]
dw = collections.Counter(w for t in paras[start:] for w in t.replace('\t', ' ').split() if w.strip() and not set(w) <= {'_'})
with pdfplumber.open(os.path.join(D, T + '_paper.pdf')) as pdf:
    pages = len(pdf.pages); pw = collections.Counter(); cols = {}
    for pi, pg in enumerate(pdf.pages):
        if pi == 0: continue
        ws = pg.extract_words(extra_attrs=['size'], keep_blank_chars=False, use_text_flow=False)
        for w in ws:
            if w['bottom'] > frame_bottom + 0.5: continue                    # the footer line
            c = 0 if (w['x0'] + w['x1']) / 2 < pg.width / 2 else 1
            cols.setdefault((pi + 1, c + 1), []).append(w); pw[w['text']] += 1
    # the full-width title lines sit in the first page's columns; the leader lines of Question 5 are tab leaders (no words)
    pw = collections.Counter({w: c for w, c in pw.items() if not set(w) <= {'_'}})            # the leader lines of Question 5 are drawn as runs of underscores (tab leaders): not words
    miss = {w: c - pw.get(w, 0) for w, c in dw.items() if pw.get(w, 0) < c}; extra = {w: c - dw.get(w, 0) for w, c in pw.items() if c > dw.get(w, 0)}
    rep('F1 words of the question pages in the .docx against the render: %d in the docx, %d on the render' % (sum(dw.values()), sum(pw.values())), not miss, 'missing on the render %s; extra on the render %s' % (dict(list(miss.items())[:8]), dict(list(extra.items())[:8])))
    over = []; title_bottom = frame_top + meas['title_height_pt'] + 2          # the title block of the first question page spans both columns (a one-column section)
    for (p, c), ws in cols.items():
        for w in ws:
            if p == 2 and w['top'] < title_bottom:
                if w['x1'] > 210 * PT - side * PT + 0.5 or w['x0'] < side * PT - 0.5: over.append((p, c, w['text'], 'title block beyond the page margin'))
                continue
            if w['x1'] > right[c - 1] + 0.5 or w['x0'] < left[c - 1] - 0.5: over.append((p, c, w['text'], round(w['x0'], 1), round(w['x1'], 1)))
    rep('F2 no word crosses the edge of its column (columns x %.1f-%.1f and %.1f-%.1f pt)' % (left[0], right[0], left[1], right[1]), not over, 'words over %s' % over[:6])
    lab = re.compile(r'^(\d[a-h])\.$|^(\d[a-h])-(\d[a-h])\.$')
    found = {}; q5 = []
    for (p, c), ws in sorted(cols.items()):
        ws = sorted(ws, key=lambda w: (round(w['top']), w['x0']))
        for i, w in enumerate(ws):
            m = lab.match(w['text'])
            pass
    keyj = json.load(open(os.path.join(D, T + '_key.json'))); labels = [e['label'] for e in keyj['items']]
    # a sub-question = from its label to the next label (or the next 'Question' heading) in the same column
    spans = {}
    for (p, c), ws in sorted(cols.items()):
        ws = sorted(ws, key=lambda w: (round(w['top']), w['x0'])); cur = None
        for w in ws:
            m = lab.match(w['text']); first = w['x0'] < left[c - 1] + 2
            if m and first and (m.group(1) or m.group(2)) in labels and cur != (m.group(1) or m.group(2)): cur = m.group(1) or m.group(2); spans.setdefault(cur, []).append([ (p, c), []])
            if w['text'] == 'Question' and first and w['size'] > 10.5: cur = None
            if cur: spans[cur][-1][1].append(w)
    split = {k: [(pc) for pc, _ in v] for k, v in spans.items() if len({pc for pc, _ in v}) != 1}
    rep('F3 every sub-question (%d labels of the key) starts once and lies in one column of one page' % len(labels), set(spans) == set(labels) and not split and all(len(v) == 1 for v in spans.values()), 'labels not found %s; split %s' % (sorted(set(labels) - set(spans)), split))
    def info(k):
        (pc, ws) = spans[k][0]; c = pc[1]; lines = sorted({round(w['top']) for w in ws})
        return dict(label=k, page=pc[0], column=c, lines=len(lines), widest_right_pt=round(max(w['x1'] for w in ws), 1), column_right_pt=round(right[c - 1], 1), margin_to_column_edge_pt=round(right[c - 1] - max(w['x1'] for w in ws), 1),
                    lowest_pt=round(max(w['bottom'] for w in ws), 1), frame_bottom_pt=round(frame_bottom, 1), words=len(ws))
    byitem = {e['item_key']: e['label'] for e in keyj['items']}           # the printed labels follow the form's mixed order: the owner cases are found by item key
    sel = [byitem['mt2:i02:fee-not-written'], byitem['mt3:i07:fill-mined-or-not']]; longest = max(spans, key=lambda k: info(k)['lines'])
    print('F4 the owner cases and the longest sub-question (lines counted on the render):')
    for k in sel + ([longest] if longest not in sel else []):
        if k in spans: print('   ', json.dumps(info(k)))
    print('   C3 = item mt2:i02 (label %s); C2 = item mt3:i07 (fill group, one block, label %s); the longest by line count: %s' % (sel[0], sel[1], longest))
print('pages of the paper on the render:', pages); print('RESULT', 'PASS' if ok else 'FAIL'); sys.exit(0 if ok else 1)
