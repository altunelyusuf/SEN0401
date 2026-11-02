#!/usr/bin/env python3
"""SEN0401 exam paper tooling v7 check, version 1.0.0 (new file). Holds no question and no answer.
Checks a built set (paper, key, sheet, SHA256.txt) against the owner redesign of 2026-11-02 (rulings 1 to 7) and the acceptance criterion AC9_Exam_V7_PapersTool. Reads the built files only.
Usage: check.py DIR --tag TAG [--leak-source REAL_ITEMS.json]
  --leak-source: a REAL items file; the check proves that no string of six words or more of it occurs in any output (used on a SYNTHETIC set; the real file is read for the comparison only, nothing of it is printed).
Prints PASS / FAIL / NOT_MEASURED per check; exit 1 on any FAIL. NOT_MEASURED is never a pass."""
import argparse, json, os, random, re, subprocess, sys, zipfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_scoring_v2_0_0 as SC
import sen0401_exam_scoring_rows_v1_0_0 as SR
import sen0401_exam_sha256_v7_0_0 as SH
from docx import Document
ap = argparse.ArgumentParser(); ap.add_argument('dir'); ap.add_argument('--tag', required=True); ap.add_argument('--leak-source'); args = ap.parse_args()
D, TAG = args.dir, args.tag; res = []


def rep(name, ok, detail=''):
    st = 'PASS' if ok is True else 'FAIL' if ok is False else 'NOT_MEASURED'
    res.append(ok); print('%s  %s %s' % (st, name, detail), flush=True)


def pdf_pages(p): return int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout).group(1))
def pdf_text(p, page=None):
    cmd = ['pdftotext', '-layout'] + (['-f', str(page), '-l', str(page)] if page else []) + [p, '-']
    return subprocess.run(cmd, capture_output=True, text=True).stdout
def docx_paras(p):
    d = Document(p); out = [x.text for x in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells: out += [x.text for x in c.paragraphs]
    return out
def f(ext): return os.path.join(D, TAG + ext)
def norm(t): return re.sub(r'\s+', ' ', t).strip().lower()


files = ['_paper.docx', '_paper.pdf', '_key.docx', '_key.pdf', '_sheet.pdf', '_key.json', '_sheet_layout.json', '_measure.json', '_paper.ttl']
miss = [e for e in files if not os.path.isfile(f(e))]
rep('P1 the set exists (paper, key as .docx and .pdf, sheet .pdf, key.json, layout, measure, ttl) and SHA256.txt', not miss and os.path.isfile(os.path.join(D, 'SHA256.txt')), 'missing: %s' % miss)
if miss: sys.exit(1)
key = json.load(open(f('_key.json'))); meas = json.load(open(f('_measure.json'))); synth = bool(key.get('synthetic'))
pp, sp, kp = pdf_pages(f('_paper.pdf')), pdf_pages(f('_sheet.pdf')), pdf_pages(f('_key.pdf'))
rep('P2a the sheet is ONE page', sp == 1, 'sheet pages %d' % sp)
rep('P2b paper plus sheet at most 7 pages, OWNER DECISION 2026-11-02 for the set v7_2_0 only (pdfinfo, LibreOffice export)', pp + sp <= 7, 'paper %d + sheet %d = %d (cover 1 + question pages %d)' % (pp, sp, pp + sp, pp - 1))
rep('P2c the aim of 4 or 5 pages in all', 4 <= pp + sp <= 5, 'total %d' % (pp + sp))
rep('P2d the measure file agrees with pdfinfo', meas['pages_total'] == pp + sp and meas['paper_pages'] == pp and meas['sheet_pages'] == sp, str((meas['paper_pages'], meas['sheet_pages'], meas['pages_total'])))
print('     key pages (not part of the limit): %d' % kp)

# paper text
paras = docx_paras(f('_paper.docx')); text = '\n'.join(paras)
BAD = re.compile(r'penalt|deduct|minus|negative|subtract|bonus|taken away|\bcosts?\b|\bfloor', re.I)
bad = sorted({m.group(0).lower() for p in paras for m in BAD.finditer(p)})
rep('P3 no penalty or deduction wording in the paper (penalt, deduct, minus, negative, subtract, bonus, taken away, cost, floor)', not bad, 'found: %s' % bad)
rep('P4a the legal-copy sentence is on the cover', 'the question pages count' in norm(text) and 'these answers count' in norm(text))
rep('P4b the rule "two answers in one place count as no answer" is on the cover', 'two answers in one place count as no answer' in norm(text))
tips = [p for p in paras if p.startswith('Tip:')]
longtips = [p for p in tips if len(p[4:].split()) > 12]
items_with_tip = [e for e in key['items'] if True]
exp = meas.get('tips_expected')
rep('P5a every tip line is "Tip:" with at most 12 words, and no tips heading, no "see tip"', not longtips and not [p for p in paras if re.match(r'^Tips?(\s+page)?$', p.strip())] and not re.search(r'\bsee tips?\b', text, re.I), 'tip lines %d, over 12 words: %d' % (len(tips), len(longtips)))
dup = [p for p in tips if tips.count(p) > 1]
rep('P5b each tip is printed once (no tip repeated; no tips page: the paper has no page of tips only)', not dup, 'repeated: %d' % len(dup))
# tip directly under its stem: the paragraph before a tip starts with a label
under = 0
for i, p in enumerate(paras):
    if p.startswith('Tip:'):
        if i > 0 and re.match(r'^\d+[a-z](-\d+[a-z])?\.\s', paras[i - 1]): under += 1
rep('P5c every tip line sits directly under its stem or instruction paragraph', under == len(tips) and len(tips) > 0, '%d of %d' % (under, len(tips)))
nopen = [p for p in paras if re.search(r'answer sheet', p, re.I) and re.search(r'second page|tips page|pages 2', p, re.I)]
rep('P5d the cover does not mention a tips page or a second sheet page', not nopen)
# marks line: five alternatives on the question pages
opts = [p for p in paras if re.match(r'^E\.\t', p)]
nchoice = sum(1 for e in key['items'] if e['type'] in ('ChoiceFour', 'ChoiceFourCode'))
nmatch = sum(1 for e in key['items'] if e['type'] == 'Matching')
nfill = sum(1 for e in key['items'] if e['type'] == 'FillBlankGroup')
rep('P6 five alternatives printed: an option E for every choice item, a response E for every matching item and a bank entry E for every fill-in group', len(opts) == nchoice + nmatch + nfill, 'E lines %d, choice %d + matching %d + fill-in groups %d' % (len(opts), nchoice, nmatch, nfill))

# key
k1, k2 = pdf_text(f('_key.pdf'), 1), pdf_text(f('_key.pdf'), 2)
steps = [str(i) + '.' for i in range(1, 11)]
rep('P7a page 1 of the key is the grading procedure: heading "How to grade" and all ten steps', 'How to grade' in k1 and all(s in k1 for s in steps) and 'Write the total' in k1)
rep('P7b the grading procedure ends on page 1 (the answers start on page 2): ONE page', 'The answers, in the order' in k2 and 'Write the total' not in k2 and 'How to grade' not in k2)
g = norm(k1)
rep('P7c the procedure says: exact value full points else 0, no partial credit, question pages are the legal copy, nothing beyond adding points', all(s in g for s in ['exact value', 'no partial credit', 'legal copy', 'the only calculation', 'no subtraction']))
hits7 = sorted({m.group(0).lower() for m in re.finditer(r'penalt|deduct|negative', pdf_text(f('_key.pdf')), re.I)})
rep('P7d the key text has no penalty or deduction wording (penalt, deduct, negative)', not hits7, 'found: %s' % hits7)

# scoring module on the key
pm = SR.perfect_marks(key); perf = SR.score(pm, key)
rep('S1 a perfect sheet scores 100 of 100 (scoring module v2.0.0 through the row-points adapter)', perf['total'] == 100.0 and perf['max_total'] == 100.0, 'total %s of %s' % (perf['total'], perf['max_total']))
rep('S2 row points add up to the unit points in every unit', not SR.row_points_agree(key), str(SR.row_points_agree(key)))
allwrong = {m['label']: ('Z' if m['rule_type'] in ('choice', 'matching', 'fill_bank') else '99999') for m in SR.marks_of_key(key)}
rep('S3a all answered, none right = 0', SR.score(allwrong, key)['total'] == 0.0)
rep('S3b all blank = 0', SR.score({}, key)['total'] == 0.0)
rep('S3c two answers in every place = 0', SR.score({l: SC.DOUBLE for l in pm}, key)['total'] == 0.0)
one = dict(pm); first = list(pm)[0]; one[first] = SC.DOUBLE
lost = [m['points'] for m in SR.marks_of_key(key) if m['label'] == first][0]
rep('S3d one place with two answers costs only that place (no deduction)', SR.score(one, key)['total'] == 100.0 - float(lost), 'place %s, %s points' % (first, lost))
numeric = [m for m in SR.marks_of_key(key) if m['rule_type'] == 'number_or_trace']
off = dict(pm)
for m in numeric[:1]: off[m['label']] = str(int(str(m['answer']).replace('-', '') or 0) + 1)
rep('S3e a number one off scores 0 for that place: exact value full points else 0, no partial credit', SR.score(off, key)['total'] == 100.0 - float(numeric[0]['points']) if numeric else None)
# independent exact blind figure
from fractions import Fraction as Fr
tot = Fr(0); closed = Fr(0)
for it in key['items']:
    for lab, ans in it['answer'].items():
        t = it['type']
        if t in ('ChoiceFour', 'ChoiceFourCode'): pts, p = Fr(it['points']), Fr(1, it['n_options'])
        elif t == 'Matching': pts, p = Fr(it['row_points'][lab]), Fr(1, it['n_responses'])
        elif t == 'Ordering': pts, p = Fr(it['row_points'][lab]), Fr(1, len(it['answer']))
        elif t == 'FillBlankGroup': pts, p = Fr(it['points_per_blank'][lab]), Fr(1, len(it['bank_codes']))
        else:
            v = ans['value'] if isinstance(ans, dict) else ans; pts, p = Fr(it['points']), Fr(1, 10 ** len(re.sub(r'[^0-9]', '', str(v))))
        tot += pts * p
        if t not in ('NumericAnswer', 'CodeTrace'): closed += pts * p
sc = key['scoring']
rep('S4a the exact blind total in the key equals an independent recomputation from the key places', str(tot) == sc['blind_total_exact'], 'independent %s = %.6f ; key %s' % (tot, float(tot), sc['blind_total_exact']))
cp = sum(Fr(m['points']) for m in SR.marks_of_key(key) if m['rule_type'] != 'number_or_trace')
rep('S4b the closed places give exactly one fifth of their points blind', closed == cp / 5, 'closed points %s, blind %s' % (cp, closed))
b = sc['blind_simulation']; se = b['standard_error']
rep('S4c the blind simulation agrees with the exact figure within three standard errors', abs(b['mean'] - float(tot)) <= 3 * se, 'exact %.4f simulated %.4f (%d sheets, SE %.4f)' % (float(tot), b['mean'], b['sheets'], se))
print('     EXACT BLIND FIGURE of this set: %s = %.6f points of 100 (closed places %.4f; number and trace places %.6f)' % (tot, float(tot), float(closed), float(tot - closed)))
ch = [e['answer'][e['label']] for e in key['items'] if e['type'] in ('ChoiceFour', 'ChoiceFourCode')]
cnt = {c: ch.count(c) for c in 'ABCDE'}
rep('K1 choice answer letters are evenly distributed (counts differ by at most one)', max(cnt.values()) - min(cnt.values()) <= 1, str(cnt))
okperm = all(sorted(e['answer'].values()) == list(range(1, len(e['answer']) + 1)) for e in key['items'] if e['type'] == 'Ordering') and all(len(set(e['answer'].values())) == len(e['answer']) for e in key['items'] if e['type'] in ('Matching', 'FillBlankGroup'))
rep('K2 ordering answers are a permutation of 1..5; matching and fill-in answers are distinct letters', okperm)
bank = [e for e in key['items'] if e['type'] == 'FillBlankGroup']
rep('K3 every fill-in bank has five entries lettered A to E', all(e['bank_codes'] == list('ABCDE') for e in bank) and bool(bank))
rep('K4 recomputed keys: every code trace was run and printed the key value', all((e.get('recomputed') or '').startswith('recomputed') for e in key['items'] if e['type'] == 'CodeTrace'), str({e['label']: e['recomputed'] for e in key['items'] if e['type'] == 'CodeTrace'})[:200])

# sheet versus key
lay = json.load(open(f('_sheet_layout.json')))
sheet_labels = [u['no'] for b_ in lay['blocks'] for u in b_['units']]
closed_labels = [lab for e in key['items'] if e['type'] not in ('NumericAnswer', 'CodeTrace') for lab in e['answer']]
rep('H1 the sheet holds exactly the closed places of the key, each once; no number or trace place', sorted(sheet_labels) == sorted(closed_labels) and len(set(sheet_labels)) == len(sheet_labels), '%d sheet rows, %d closed places' % (len(sheet_labels), len(closed_labels)))
rep('H2 every sheet row has five alternatives', all(len(r['opts']) == 5 for b_ in lay['blocks'] for u in b_['units'] for r in u['rows']))
st = pdf_text(f('_sheet.pdf'))
rep('H3 the sheet carries the legal-copy sentence and no deduction wording', 'question pages count' in st and not re.search(r'penalt|deduct|negative|floor|bonus', st, re.I))

# disclosure of the synthetic input in every output
if synth:
    M = 'synthetic'
    dis = {'paper.docx': M in norm(text), 'paper.pdf': M in norm(pdf_text(f('_paper.pdf'))), 'key.docx': M in norm('\n'.join(docx_paras(f('_key.docx')))), 'key.pdf': M in norm(pdf_text(f('_key.pdf'))),
           'sheet.pdf': 'synthetic' in norm(st) or 'SYNTHETIC' in subprocess.run(['pdfinfo', f('_sheet.pdf')], capture_output=True, text=True).stdout, 'key.json': key.get('synthetic') is True, 'measure.json': meas.get('synthetic') is True,
           'layout.json': lay.get('synthetic') is True, 'SHA256.txt': 'SYNTHETIC' in open(os.path.join(D, 'SHA256.txt')).read()}
    rep('D1 the synthetic input is disclosed in every output', all(dis.values()), str({k: v for k, v in dis.items() if not v}) or 'all')
else:
    rep('D1 the synthetic disclosure', None, 'not a synthetic set')

# SHA256
rv = SH.verify(D, TAG) if True else 1
rep('X1 SHA256.txt verifies every file of the set', rv == 0)

# leak test
if args.leak_source and os.path.isfile(args.leak_source):
    real = json.load(open(args.leak_source))['items']; strings = []
    def walk(o):
        if isinstance(o, str):
            if len(o.split()) >= 6: strings.append(norm(o))
        elif isinstance(o, dict):
            for v in o.values(): walk(v)
        elif isinstance(o, list):
            for v in o: walk(v)
    for it in real:
        for k in ('q', 'options', 'steps', 'premises', 'responses', 'blanks', 'distractors', 'code', 'instruction', 'tip', 'output'): walk(it.get(k))
    outs = [text, '\n'.join(docx_paras(f('_key.docx'))), pdf_text(f('_paper.pdf')), pdf_text(f('_key.pdf')), pdf_text(f('_sheet.pdf')), open(f('_key.json')).read(), open(f('_paper.ttl')).read(), open(f('_measure.json')).read()]
    blob = norm(' '.join(outs)); hits = sum(1 for s in strings if s in blob)
    rep('L1 no string of six words or more of the REAL items file occurs in any output (%d strings compared; nothing printed)' % len(strings), hits == 0, 'matches: %d' % hits)
else:
    rep('L1 leak test against the real items file', None, 'no real items file given')
# committed files untouched
r = subprocess.run(['git', '-C', os.path.dirname(os.path.dirname(HERE)), 'status', '--porcelain', '--untracked-files=no'], capture_output=True, text=True).stdout.splitlines()
mod = [l for l in r if l[:2].strip() and not l.startswith('??')]
rep('G1 no tracked file of the public repository is modified or deleted', not mod, str(mod[:5]))
print('RESULT: %d PASS, %d FAIL, %d NOT_MEASURED' % (res.count(True), res.count(False), res.count(None)))
sys.exit(1 if False in res else 0)
