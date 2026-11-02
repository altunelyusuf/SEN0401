"""Builds the v6 answer sheet (two A4 pages) for a form whose v5 sheet layout and key exist (new file; holds no question and no answer: the tips and the bonus parts are read from the key at run time and written only to OUTDIR).
Usage: build.py --layout V5_SHEET_LAYOUT.json --key KEY.json --out OUTDIR --tag STEM [--tips TIPS.json] [--lines 4] [--no-scoring-note]
The units, the form code and the paper kind are the v5 sheet's own; the bonus parts (hand-marked) come from the key; the tips come from --tips (a list of {label, text}) or, when absent, from the key's own tip pairs of the bonus parts."""
import argparse, json, os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v6_0_0 as V
a = argparse.ArgumentParser(); a.add_argument('--layout', required=True); a.add_argument('--key', required=True); a.add_argument('--out', required=True); a.add_argument('--tag', required=True)
a.add_argument('--tips'); a.add_argument('--lines', type=int, default=4); a.add_argument('--no-scoring-note', action='store_true'); o = a.parse_args()
old = json.load(open(o.layout))['spec']; key = json.load(open(o.key))
bonus = [dict(no=e['label'], points=e['points'], lines=o.lines) for e in key['items'] if e['type'] == 'ShortExplanation']
if o.tips: tips = json.load(open(o.tips))
else: tips = [dict(label=e['label'], text='; '.join('%s: %s' % (x, y) for x, y in e['tips']) + '.') for e in key['items'] if e['type'] == 'ShortExplanation' and e.get('tips')]
spec = dict(paper_kind=old['paper_kind'], paper_version=old['paper_version'], form_code=old['form_code'], units=old['units'], bonus_parts=bonus, tips=tips, scoring_note=not o.no_scoring_note)
lay = V.build_layout(spec)
os.makedirs(o.out, exist_ok=True); pdf, js = V.write_pair(lay, o.out, o.tag)
pi = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
print(pdf); print(js); print([l for l in pi.splitlines() if l.startswith(('Pages', 'Page size'))]); print(lay['free_height_pt'])
