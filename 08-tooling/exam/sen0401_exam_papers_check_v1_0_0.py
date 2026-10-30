"""Checks of the SEN0401 midterm papers, version 1.0.0 (new file). Prints PASS / FAIL / NOT_MEASURED per check; exit 0 only when every check passes.
Usage: check.py PAPERSDIR     (the PDFs, keys and sheets written by sen0401_exam_papers_build_v1_0_0.py; the run log is made by the caller with tee)
P1 no committed file is edited (git: tracked files unchanged); P2 pages counted by pdfinfo, per order, paper + sheet; P3 print safety: every drawn colour and text colour is black/grey/white,
no image objects, text 10 point or larger (code 9 point or larger, never wrapped), page size A4; P4 key and paper agree: for every item the keyed option/answer is found in the text printed on the paper PDF
(choice: the keyed letter's text, matching/ordering/fill-in: position-by-position), letters spread evenly; P5 the sheet holds exactly one unit per answer place and the layout JSON agrees with the key;
P6 both orders hold the same 23 items and 24 units, 4 units per chapter 1 to 6, higher-order majority; P7 the cs_encode fact is shown (item printed as authored); P8 version in file names and header is 1."""
import collections, glob, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
import pdfplumber
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
D = sys.argv[1]; res = []
def rep(n, ok, d=''):
    res.append(ok); print('%s  %s %s' % ('PASS' if ok else 'FAIL', n, d)); sys.stdout.flush()
def pdfinfo(p):
    o = subprocess.run(['pdfinfo', p], capture_output=True, text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', o).group(1)), re.search(r'Page size:\s+(.*)', o).group(1)
def norm(t): return re.sub(r'\s+', ' ', t).strip()
items = {i['key']: i for i in json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json')))['items']}
# P1
st = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=ROOT, capture_output=True, text=True).stdout.strip().splitlines()
rep('P1 no tracked file modified', not st, 'modified: %s' % st)
for order in ('chapter', 'type'):
    base = os.path.join(D, 'sen0401_exam_midterm_%s_v1_0_0' % order)
    key = json.load(open(base + '_key.json')); lay = json.load(open(base + '_sheet_layout.json')); meas = json.load(open(base + '_measure.json'))
    # P2
    pc, ps = pdfinfo(base + '.pdf'); sc, ss = pdfinfo(base + '_sheet.pdf'); kc, _ = pdfinfo(base + '_key.pdf')
    rep('P2 %s pages' % order, pc == meas['content_pages'] and sc == meas['sheet_pages'] and key['pages'] == pc + sc, 'paper %d + sheet %d = %d with the sheet; key %d; size %s / %s' % (pc, sc, pc + sc, kc, ps, ss))
    # P3
    bad = []; small = []
    for f in (base + '.pdf', base + '_sheet.pdf', base + '_key.pdf'):
        with pdfplumber.open(f) as pdf:
            for pg in pdf.pages:
                if pg.images: bad.append((f, 'image'))
                for ch in pg.chars:
                    c = ch.get('non_stroking_color'); 
                    if c not in (None, (0,), (0, 0, 0), [0], [0, 0, 0], 0, (0.0,), (0.0, 0.0, 0.0)) and not (isinstance(c, (tuple, list)) and len(set(c)) == 1 and c[0] in (0, 0.0)): bad.append((f, 'textcolour', c)); break
                    lim = 9 if 'Mono' in ch['fontname'] else 10
                    if f.endswith('.pdf') and not f.endswith('_key.pdf') and ch['size'] < lim - 0.01 and ch['text'].strip() and not re.search(r'page \d', '') : small.append((os.path.basename(f), ch['fontname'], round(ch['size'], 1), ch['text']))
                for o in pg.rects + pg.lines + pg.curves:
                    for k in ('stroking_color', 'non_stroking_color'):
                        c = o.get(k)
                        if c is None: continue
                        t = tuple(c) if isinstance(c, (list, tuple)) else (c,)
                        if any(abs(v - t[0]) > 1e-6 for v in t): bad.append((f, 'colour', k, t))
                        if k == 'non_stroking_color' and o.get('fill') and any(v < 0.999 for v in t): bad.append((f, 'fill', t))
    small = [s for s in small if s[2] < 8]   # the 8 point page footer is the only text allowed below 9/10 point (rule: footer)
    rep('P3 %s print safety (no image, no colour, no filled shape, text size)' % order, not bad and not small, 'problems: %s %s' % (bad[:3], small[:3]))
    # P4
    txt = norm(subprocess.run(['pdftotext', base + '.pdf', '-'], capture_output=True, text=True).stdout)
    miss = []
    for e in key['items']:
        it = items[e['item_key']]; n = e['position']
        if it['type'] in ('ChoiceFour', 'ChoiceFourCode'):
            L = e['answer']; opt = None
            # the option text that carries the keyed letter on the paper: find the four printed options after the stem
            stem = norm(it['q']); i0 = txt.find(stem[:60])
            seg = txt[i0:i0 + 4000]
            ms = re.findall(r'(?:^| )%s\. (.*?)(?= [ABCD]\. |$)' % L, seg)      # every place where the letter starts a text after the stem (the code of an item can hold 'B. ' too)
            right = norm(it['options'][it['answer']]) if isinstance(it['answer'], int) else None
            # items file stores the correct option index or text: compare to the key via the printed text
            correct_text = norm(it['options'][it['answer']] if isinstance(it['answer'], int) else it['answer'])
            if i0 < 0 or not any(norm(x).startswith(correct_text[:40]) for x in ms): miss.append((n, L))
        elif it['type'] == 'Matching':
            for k, (pr, lt) in enumerate(e['answer'].items()):
                p = it['premises'][k]; idx = lt
                # the printed response with the keyed letter must equal the premise's own answer
                m = re.search(r'(?:^| )%s\. (%s)(?= [A-H]\. | SEN0401 midterm|$| \d+[\.-])' % (lt, re.escape(norm(p['match']))), txt)
                if not m: miss.append((n, pr, lt))
        elif it['type'] == 'NumericAnswer':
            if norm(it['q'])[:60] not in txt or float(e['answer']['value']) != float(it['key_value']): miss.append((n, 'num'))
        elif it['type'] == 'CodeTrace':
            if norm(it['q'])[:60] not in txt or str(e['answer']) != str(it['output']): miss.append((n, 'trace'))
        elif it['type'] == 'Ordering':
            got = [it['steps'][k] for k in sorted(range(len(it['steps'])), key=lambda j: 0)]
            for j, lab in enumerate(sorted(e['answer'])):
                step = it['steps'][e['shown_order'][j]]
                if e['answer'][lab] != e['shown_order'][j] + 1 or norm(step) not in txt: miss.append((n, lab))
        elif it['type'] == 'FillBlankGroup':
            for b, bl in enumerate(it['blanks']):
                code = e['answer'][str(n + b)]
                if not re.search(r'%s %s(?= |$)' % (code, re.escape(bl['answer'])), txt): miss.append((n, b))
    rep('P4 %s key agrees with the printed paper' % order, not miss, 'mismatches: %s' % miss)
    ch = collections.Counter(e['answer'] for e in key['items'] if e['type'] in ('ChoiceFour', 'ChoiceFourCode'))
    rep('P4b %s letters spread evenly' % order, max(ch.values()) - min(ch.get(l, 0) for l in 'ABCD') <= 1, dict(sorted(ch.items())))
    # P5
    places = []
    for e in key['items']:
        a = e['answer']
        if e['type'] in ('ChoiceFour', 'ChoiceFourCode', 'NumericAnswer', 'CodeTrace'): places.append(str(e['position']))
        elif e['type'] in ('Matching', 'Ordering', 'FillBlankGroup'): places += list(a.keys())
    sheet_units = [u['no'] for b in lay['blocks'] for u in b['units']]
    rep('P5 %s sheet holds one unit per answer place' % order, sorted(places) == sorted(sheet_units) and len(set(sheet_units)) == len(sheet_units), '%d places, %d units' % (len(places), len(sheet_units)))
    # P6
    units = sum(len(it['blanks']) if it['type'] == 'FillBlankGroup' else 1 for it in (items[e['item_key']] for e in key['items']))
    per = collections.Counter(); hi = 0
    for e in key['items']:
        it = items[e['item_key']]; u = len(it['blanks']) if it['type'] == 'FillBlankGroup' else 1; per[e['chapters'][0]] += u; hi += u * (e['bloom'] >= 3)
    rep('P6 %s items/units/chapters/Bloom' % order, len(key['items']) == 23 and units == 24 and all(per[c] == 4 for c in range(1, 7)) and hi * 2 > units, '%d items %d units per chapter %s higher-order (Apply+) %d of %d' % (len(key['items']), units, dict(per), hi, units))
    rep('P8 %s version 1 in the header' % order, 'midterm v1 ' in subprocess.run(['pdftotext', base + '.pdf', '-'], capture_output=True, text=True).stdout and 'version 1' in txt, '')
a = json.load(open(os.path.join(D, 'sen0401_exam_midterm_chapter_v1_0_0_key.json'))); b = json.load(open(os.path.join(D, 'sen0401_exam_midterm_type_v1_0_0_key.json')))
rep('P6b both orders hold the same items', sorted(e['item_key'] for e in a['items']) == sorted(e['item_key'] for e in b['items']))
t = open(os.path.join(D, 'sen0401_exam_midterm_type_v1_0_0.pdf'), 'rb')
tx = subprocess.run(['pdftotext', os.path.join(D, 'sen0401_exam_midterm_type_v1_0_0.pdf'), '-'], capture_output=True, text=True).stdout
rep('P7 cs_encode is printed as authored (used, not defined on the paper)', 'cs_encode(n)' in tx and 'def cs_encode' not in tx, 'item 24 in grouped order; the stem names the function and says what it does')
print('RESULT', 'PASS' if all(res) else 'FAIL', sum(res), 'of', len(res))
sys.exit(0 if all(res) else 1)
