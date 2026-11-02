"""Builds the v7.1 answer sheet (a copy of sen0401_exam_answersheet_v7_build_v1_0_0.py, which stays unchanged; module v7.1.0: adds the digit boxes of Question 2 from the box counts printed on the question pages, read from the PAPER .docx with --boxes-from-paper; no key digit is read).
Was: Builds the v7 answer sheet (ONE A4 page, choice-type answers only, five alternatives) from a unit list. New file; holds no question and no answer (labels only).
Usage: build.py --out OUTDIR --tag STEM --form-code CODE --paper-kind Midterm|Makeup (--units UNITS.json | --from-key-shape KEY.json) [--paper-version 7]
UNITS.json: [{"type": "choice|matching|ordering|fill", "labels": ["1a", ...]}, ...]  (sheet order; each entry is one printed sub-question = one block start).
--from-key-shape reads ONLY the labels and the item types of a key json (the proof shape: ChoiceFour -> choice, Matching -> matching, Ordering -> ordering, FillBlankGroup -> fill; number, code-trace and written items are not on the sheet); no answer is read."""
import argparse, json, os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import re
import sen0401_exam_answersheet_v7_1_0 as V


def shape_from_key(path):
    key = json.load(open(path)); order = {'ChoiceFour': 'choice', 'Matching': 'matching', 'Ordering': 'ordering', 'FillBlankGroup': 'fill'}
    out = []; choice = []
    for e in key['items']:
        t = order.get(e['type'])
        if t is None: continue
        labs = list(e['answer'].keys())
        if t == 'choice': choice += labs
        else: out.append({'type': t, 'labels': labs})
    return ([{'type': 'choice', 'labels': choice}] if choice else []) + out


BORDER_RUN = 'w:bdr'


def boxes_from_paper(docx_path, question=2):
    """The digit boxes printed on the question pages: [{'no': '2a', 'cells': n}] in paper order, counted from the bordered no-break-space runs of the paper .docx
    (a place is a paragraph that starts '<question><letter>. ' followed by the box paragraph that carries more than one bordered run). Reads no key and no answer."""
    from docx import Document
    from docx.oxml.ns import qn
    d = Document(docx_path); cur = None; out = []; pat = re.compile(r'^(%d[a-z])\.\s' % question)
    for p in d.element.body.iter(qn('w:p')):
        txt = ''.join(t.text or '' for t in p.iter(qn('w:t')))
        m = pat.match(txt.replace('\u00a0', ' ').strip())
        if m: cur = m.group(1)
        n = sum(1 for r in p.iter(qn('w:r')) if r.find(qn('w:rPr')) is not None and r.find(qn('w:rPr')).find(qn('w:bdr')) is not None and ''.join(t.text or '' for t in r.iter(qn('w:t'))) and set(''.join(t.text or '' for t in r.iter(qn('w:t')))) == {'\u00a0'})
        if n > 1 and cur is not None and not any(o['no'] == cur for o in out): out.append({'no': cur, 'cells': n})
    return out


def number_labels_from_key(path, question=2):
    """The labels (only) of the hand-written places of the key; no answer is read."""
    key = json.load(open(path)); out = []
    for e in key['items']:
        if e['type'] in ('NumericAnswer', 'CodeTrace') and e.get('question') == question: out.append(e['label'])
    return out


def main():
    a = argparse.ArgumentParser(); a.add_argument('--out', required=True); a.add_argument('--tag', required=True); a.add_argument('--form-code', required=True)
    a.add_argument('--paper-kind', default='Midterm'); a.add_argument('--paper-version', type=int, default=7); a.add_argument('--units'); a.add_argument('--from-key-shape'); a.add_argument('--boxes-from-paper', required=True, help='the paper .docx whose printed answer boxes of Question 2 give the box counts'); a.add_argument('--question', type=int, default=2); o = a.parse_args()
    ul = json.load(open(o.units)) if o.units else shape_from_key(o.from_key_shape)
    spec = dict(paper_kind=o.paper_kind, paper_version=o.paper_version, form_code=o.form_code, units=V.units_from_list(ul), numbers=V.numbers_from_list(boxes_from_paper(o.boxes_from_paper, o.question)))
    lay = V.build_layout(spec); os.makedirs(o.out, exist_ok=True); pdf, js = V.write_pair(lay, o.out, o.tag)
    pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    print(pdf); print(js); print([l for l in pi.splitlines() if l.startswith(('Pages', 'Page size'))]); print(lay['free_height_pt'])


if __name__ == '__main__': main()
