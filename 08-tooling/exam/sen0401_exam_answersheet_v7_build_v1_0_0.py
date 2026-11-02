"""Builds the v7 answer sheet (ONE A4 page, choice-type answers only, five alternatives) from a unit list. New file; holds no question and no answer (labels only).
Usage: build.py --out OUTDIR --tag STEM --form-code CODE --paper-kind Midterm|Makeup (--units UNITS.json | --from-key-shape KEY.json) [--paper-version 7]
UNITS.json: [{"type": "choice|matching|ordering|fill", "labels": ["1a", ...]}, ...]  (sheet order; each entry is one printed sub-question = one block start).
--from-key-shape reads ONLY the labels and the item types of a key json (the proof shape: ChoiceFour -> choice, Matching -> matching, Ordering -> ordering, FillBlankGroup -> fill; number, code-trace and written items are not on the sheet); no answer is read."""
import argparse, json, os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v7_0_0 as V


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


def main():
    a = argparse.ArgumentParser(); a.add_argument('--out', required=True); a.add_argument('--tag', required=True); a.add_argument('--form-code', required=True)
    a.add_argument('--paper-kind', default='Midterm'); a.add_argument('--paper-version', type=int, default=7); a.add_argument('--units'); a.add_argument('--from-key-shape'); o = a.parse_args()
    ul = json.load(open(o.units)) if o.units else shape_from_key(o.from_key_shape)
    spec = dict(paper_kind=o.paper_kind, paper_version=o.paper_version, form_code=o.form_code, units=V.units_from_list(ul))
    lay = V.build_layout(spec); os.makedirs(o.out, exist_ok=True); pdf, js = V.write_pair(lay, o.out, o.tag)
    pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    print(pdf); print(js); print([l for l in pi.splitlines() if l.startswith(('Pages', 'Page size'))]); print(lay['free_height_pt'])


if __name__ == '__main__': main()
