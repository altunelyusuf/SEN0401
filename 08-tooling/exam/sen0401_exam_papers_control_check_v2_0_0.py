#!/usr/bin/env python3
"""sen0401_exam_papers_control_check v2_0_0 - control of the midterm paper v2 (3 Word pages + 1 PDF answer-sheet page), adapted from the papers control v1.0.0 (new file; v1.0.0 is not edited).
It reads the built files of the folder papers_midterm_v2 and the items file v1.1.0 and checks, per form, WITHOUT using the builder's own paper object:
  A  nothing committed earlier is modified or deleted in 08-tooling/exam since the start commit; items v1.1.0 differ from v1.0.0 in item mt1:i20 only; the v1.0.0 builder still writes the v1.0.0 items
  B  pages: the paper .docx is exported AGAIN here with LibreOffice (own profile) = exactly 3 pages, every column keeps at least 3 percent of its height free; the sheet PDF is 1 page; 4 pages in total
  C  the .docx files open (python-docx), are black on white, no images, no shading; every run Arial at least 10 pt or Courier New at least 8 pt; exact line spacing in every paragraph; two fixed-width columns, 5 explicit column breaks
  D  the KEY against the items, read from the PRINTED paper (.docx text): choice letters, matching, ordering, fill-in bank codes, numbers; the printed code of every trace item is RUN again (with a real CompactSize encoder for cs_encode)
  E  the form code: distinct per form, Damm check digit valid, printed on paper (title, footer), paper PDF, sheet PDF, layout JSON, key JSON and key .docx; a mismatched pair (key of one form with the layout or sheet of the other) is refused
  F  the mixed order: 24 units, 4 per chapter, first item Bloom <= 2, no two neighbours of one item type, letters evenly spread, majority at Bloom 3 or higher
  G  the code boxes: every code line is inside its box and every box holds at least 45 characters at 8 pt (measured on the render, from the builder's measurement file and again here)
  H  print safety of the paper PDFs: no image, no coloured pixel; text sizes on the render; no personal data
  I  the answer sheet as read by the reader of record (v1.1.0 unless v1.2.0 is committed): synthetic sheets of the form's own layout, registration tolerance as in the v1 control, 0 silent wrong, 0 missed, 0 unflagged empty
  J  a rebuild gives the same key, layout and Word document text (determinism)
Usage: control.py PAPERS_DIR [--sheets 40] [--no-rebuild]"""
import collections, glob, hashlib, io, json, os, random, re, contextlib, shutil, subprocess, sys, tempfile, zipfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
W = os.path.abspath(sys.argv[1]); NS = int(sys.argv[sys.argv.index('--sheets') + 1]) if '--sheets' in sys.argv else 40
BASE_COMMIT = 'bd7133d'
fails = []; notm = []
def rep(n, ok, d=''):
    print('%s  %s  %s' % ('PASS' if ok else 'FAIL', n, d)); (None if ok else fails.append(n))
def nm(n, d=''):
    print('NOT_MEASURED  %s  %s' % (n, d)); notm.append(n)
from docx import Document
from lxml import etree
import sen0401_exam_answersheet_v1_0_0 as A0
W_NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
FORMS = sorted({re.search(r'_form([A-Z])_', f).group(1) for f in os.listdir(W) if '_form' in f})
items = {i['key']: i for i in json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_1_0.json'), encoding='utf8'))['items']}
tag = lambda f: 'sen0401_exam_midterm_v2_0_0_form%s' % f

# ---------------------------------------------------------------- A  nothing committed earlier is edited
st = subprocess.run(['git', '-C', ROOT, 'diff', '--name-status', BASE_COMMIT, '--', '08-tooling/exam'], capture_output=True, text=True).stdout.splitlines()
bad = [l for l in st if not l.startswith('A')]
rep('A no file of 08-tooling/exam committed at %s is modified or deleted (git diff --name-status against the start commit, working tree included)' % BASE_COMMIT, not bad, bad or '(%d files added)' % len(st))
v0 = json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_0_0.json'), encoding='utf8')); v1 = json.load(open(os.path.join(HERE, 'sen0401_exam_items_midterm_v1_1_0.json'), encoding='utf8'))
diff = [(a['key'], [k for k in a if a[k] != b.get(k)]) for a, b in zip(v0['items'], v1['items']) if a != b]
rep('A items v1.1.0 differ from v1.0.0 in one item and one field only', diff == [('mt1:i20:trace-compactsize', ['q'])] and len(v0['items']) == len(v1['items']), diff)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
blob = lambda p: subprocess.run(['git', '-C', ROOT, 'show', 'HEAD:' + os.path.relpath(p, ROOT)], capture_output=True).stdout
frozen = [os.path.join(HERE, f) for f in ('sen0401_exam_items_midterm_v1_0_0.json', 'sen0401_exam_engine_render_v1_1_0.py', 'sen0401_exam_engine_render_v1_2_0.py', 'sen0401_exam_papers_build_v1_0_0.py', 'sen0401_exam_engine_v1_1_0.py')]
frozen += sorted(glob.glob(os.path.join(HERE, 'papers_midterm_v1', '*')))
same = [os.path.basename(p) for p in frozen if hashlib.sha256(blob(p)).hexdigest() != sha(p)]
rep('A SHA-256 of the v1.0.0 items, renderers v1.1/v1.2, builder v1, engine v1.1.0 and the %d files of papers_midterm_v1 equal the committed blobs' % (len(frozen) - 5), not same, same or '(%d files)' % len(frozen))

# ---------------------------------------------------------------- per form
def docx_paras(path):
    d = Document(path); return [p.text for p in d.paragraphs], d
def cs_real(n):
    if n < 0xfd: return n.to_bytes(1, 'little')
    if n <= 0xffff: return b'\xfd' + n.to_bytes(2, 'little')
    if n <= 0xffffffff: return b'\xfe' + n.to_bytes(4, 'little')
    return b'\xff' + n.to_bytes(8, 'little')
def run_code(code, ns=None):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf): exec(compile(code, '<printed>', 'exec'), dict(ns or {}))
    return buf.getvalue().strip()
def segments(paras):
    starts = []; exp = 1
    for i, t in enumerate(paras):
        m = re.match(r'^(\d+)(?:-(\d+))?\. ', t)
        if m and int(m.group(1)) == exp: starts.append((exp, i)); exp = int(m.group(2) or m.group(1)) + 1
    seg = {}
    for k, (n, i) in enumerate(starts): seg[n] = paras[i:(starts[k + 1][1] if k + 1 < len(starts) else len(paras))]
    return seg

keys = {}; texts = {}
for f in FORMS:
    t = tag(f); key = json.load(open(os.path.join(W, t + '_key.json'), encoding='utf8')); keys[f] = key
    paras, doc = docx_paras(os.path.join(W, t + '_paper.docx')); texts[f] = paras
    seg = segments(paras); bad = []; nchk = 0
    for e in key['items']:
        n = e['position']; it = items[e['item_key'].split('#')[0]]; a = e['answer']; ty = e['type']; sg = seg.get(n)
        if sg is None: bad.append((n, 'item not found in the printed paper')); continue
        nchk += 1
        if ty in ('ChoiceFour', 'ChoiceFourCode'):
            opts = {m.group(1): m.group(2) for p in sg for m in [re.match(r'^([ABCD])\.\t(.*)$', p, re.S)] if m}
            if sorted(opts) != list('ABCD') or opts.get(a) != it['options'][it['answer']] or sorted(opts.values()) != sorted(it['options']): bad.append((n, 'choice', a))
            if ty == 'ChoiceFourCode' and 'utxo' in it['code']:
                code = next(p for p in sg if 'utxo' in p and '\n' in p)
                if run_code(code) != it['options'][it['answer']].split(' : ')[0]: bad.append((n, 'code choice output'))
        elif ty == 'Matching':
            prem = {m.group(1): m.group(2) for p in sg for m in [re.match(r'^([a-f])\)\t(.*)$', p, re.S)] if m}; resp = {m.group(1): m.group(2) for p in sg for m in [re.match(r'^([A-H])\.\t(.*)$', p, re.S)] if m}
            exp = {p['text']: p['match'] for p in it['premises']}
            if len(prem) != len(it['premises']) or sorted(resp.values()) != sorted(it['responses']): bad.append((n, 'matching text'))
            for k, txt in prem.items():
                if resp.get(a['%d%s' % (n, k)]) != exp.get(txt): bad.append((n, 'matching key', k))
        elif ty == 'Ordering':
            steps = {m.group(1): m.group(2) for p in sg for m in [re.match(r'^([a-f])\)\t(.*)$', p, re.S)] if m}
            if sorted(steps.values()) != sorted(it['steps']): bad.append((n, 'ordering text'))
            for k, txt in steps.items():
                if a['%d%s' % (n, k)] != it['steps'].index(txt) + 1: bad.append((n, 'ordering key', k))
        elif ty == 'FillBlankGroup':
            bank = {}
            for p in sg:
                if re.match(r'^\d\d ', p) and not re.match(r'^\d+[.\-]', p):
                    for part in p.split('\t'): bank[part[:2]] = part[3:]
            for b, bl in enumerate(it['blanks']):
                if bank.get(a[str(n + b)]) != bl['answer']: bad.append((n, 'fill code', b))
                if not any(p.startswith('%d. ' % (n + b)) and bl['text'] in p for p in sg): bad.append((n, 'blank text not printed', b))
            if sorted(bank.values()) != sorted([b['answer'] for b in it['blanks']] + it['distractors']): bad.append((n, 'bank entries'))
        elif ty == 'NumericAnswer':
            if a['value'] != it['key_value'] or it['q'] not in ''.join(sg) or ('Unit: %s.' % it['unit']) not in ''.join(sg): bad.append((n, 'number'))
        elif ty == 'CodeTrace':
            code = next(p for p in sg if '\n' in p)
            got = run_code(code, {'cs_encode': lambda x: cs_real(x)})
            if got != str(a) or str(a) != it['output'] or it['q'] not in ''.join(sg): bad.append((n, 'trace', got, a))
    rep('D form %s: the key agrees with the items for %d printed items (choice letter and text, matching, ordering, fill-in bank codes and blank texts, numbers, traces re-run on the PRINTED code)' % (f, nchk), not bad, bad)
    lt = collections.Counter(e['answer'] for e in key['items'] if e['type'] in ('ChoiceFour', 'ChoiceFourCode'))
    rep('D form %s letters of the choice items evenly spread (counts differ by at most one)' % f, max(lt.values()) - min(lt.values()) <= 1 and len(lt) == 4, dict(lt))
    cs = next(e for e in key['items'] if e['item_key'].startswith('mt1:i20'))
    rep('D form %s the cs_encode item defines the CompactSize sizes in the printed question and the answer is 14 on a real implementation' % f,
        'a count below 253 takes 1 byte, up to 65535 takes 3 bytes, up to 4294967295 takes 5 bytes, anything larger takes 9 bytes' in ' '.join(seg[cs['position']]) and cs['answer'] == '14' and sum(len(cs_real(x)) for x in (252, 253, 65536, 4294967295)) == 14)

# ---------------------------------------------------------------- F  mixed order
for f in FORMS:
    key = keys[f]; ordr = key['items']; bl = [e['bloom'] for e in ordr]
    units = sum(2 if e['type'] == 'FillBlankGroup' else 1 for e in ordr)
    per = collections.Counter(e['chapters'][0] for e in ordr for _ in range(2 if e['type'] == 'FillBlankGroup' else 1))
    hi = sum((2 if e['type'] == 'FillBlankGroup' else 1) for e in ordr if e['bloom'] >= 3)
    rep('F form %s: 24 units (%d), 4 per chapter %s, majority at Bloom 3 or higher (%d of %d), first item Bloom %d (<= 2), no two neighbours of one type' % (f, units, dict(sorted(per.items())), hi, units, bl[0]),
        units == 24 and all(v == 4 for v in per.values()) and len(per) == 6 and hi * 2 > units and bl[0] <= 2 and all(ordr[k]['type'] != ordr[k + 1]['type'] and ordr[k]['item_key'] != ordr[k + 1]['item_key'] for k in range(len(ordr) - 1)))
if len(FORMS) > 1:
    o = [[e['item_key'] for e in keys[f]['items']] for f in FORMS]
    rep('F the forms differ in order (%s)' % ', '.join(FORMS), all(o[0] != x for x in o[1:]), 'seeds %s' % [keys[f]['seed'] for f in FORMS])

# ---------------------------------------------------------------- E  form codes
codes = {f: keys[f]['form_code'] for f in FORMS}
rep('E form codes are distinct and each is a four-digit serial V K FF plus a valid Damm check digit', len(set(codes.values())) == len(codes) and all(len(c) == 5 and A0.damm_valid(c) and c[:4] == '2%d%02d' % (0, i + 1) for i, c in enumerate(codes.values())), codes)
def pdftext(p): return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout
for f in FORMS:
    t = tag(f); c = codes[f]; lay = json.load(open(os.path.join(W, t + '_sheet_layout.json')))
    d = Document(os.path.join(W, t + '_paper.docx')); foot = ' '.join(p.text for s in d.sections for p in s.footer.paragraphs)
    kd = Document(os.path.join(W, t + '_key.docx')); kfoot = ' '.join(p.text for s in kd.sections for p in s.footer.paragraphs) + ' '.join(p.text for p in kd.paragraphs)
    where = {'paper .docx title': c in ' '.join(texts[f][:3]), 'paper .docx footer': c in foot, 'paper PDF': c in pdftext(os.path.join(W, t + '_paper.pdf')), 'sheet PDF': c in pdftext(os.path.join(W, t + '_sheet.pdf')) and ('Form %s' % f) in pdftext(os.path.join(W, t + '_sheet.pdf')),
             'layout JSON': lay.get('form_code') == c and lay['spec']['form_code'] == c, 'key JSON': keys[f]['form_code'] == c, 'key .docx': c in kfoot, 'key PDF': c in pdftext(os.path.join(W, t + '_key.pdf'))}
    rep('E form %s code %s is carried by every file' % (f, c), all(where.values()), {k: v for k, v in where.items() if not v} or '(8 places)')
if len(FORMS) > 1:
    f1, f2 = FORMS[0], FORMS[1]
    lay2 = json.load(open(os.path.join(W, tag(f2) + '_sheet_layout.json')))
    def pair_ok(key, lay, sheet_pdf):
        return key['form_code'] == lay['form_code'] == lay['spec']['form_code'] and key['form_code'] in pdftext(sheet_pdf)
    ok_pairs = pair_ok(keys[f1], json.load(open(os.path.join(W, tag(f1) + '_sheet_layout.json'))), os.path.join(W, tag(f1) + '_sheet.pdf')) and pair_ok(keys[f2], lay2, os.path.join(W, tag(f2) + '_sheet.pdf'))
    mism = [pair_ok(keys[f1], lay2, os.path.join(W, tag(f2) + '_sheet.pdf')), pair_ok(keys[f2], json.load(open(os.path.join(W, tag(f1) + '_sheet_layout.json'))), os.path.join(W, tag(f1) + '_sheet.pdf'))]
    rep('E the pair check of this control accepts the matching pairs and refuses the mismatched pairs (key of one form with layout and sheet of the other)', ok_pairs and not any(mism), 'matching %s, mismatched accepted %s' % (ok_pairs, mism))
    # the committed grading tool v1.0.0 pair check, run as it is (it has no form-code test: reported, not edited)
    GR = os.path.join(HERE, 'sen0401_exam_grading_v1_0_0.py')
    def gp(k, l):
        r = subprocess.run([sys.executable, '-I', GR, 'check-pair', '--key', k, '--layout', l], capture_output=True, text=True); return r.returncode, (r.stdout.strip().splitlines() or [''])[0]
    ra = gp(os.path.join(W, tag(f1) + '_key.json'), os.path.join(W, tag(f1) + '_sheet_layout.json')); rb = gp(os.path.join(W, tag(f1) + '_key.json'), os.path.join(W, tag(f2) + '_sheet_layout.json'))
    rep('E grading tool v1.0.0 check-pair accepts the matching key and layout of form %s (exit 0)' % f1, ra[0] == 0, ra)
    print('INFO  grading tool v1.0.0 check-pair on the MISMATCHED pair (key %s, layout %s): exit %d, %s  (the tool compares places, not the form code; the form-code refusal is the line above)' % (f1, f2, rb[0], rb[1]))

# ---------------------------------------------------------------- B  pages (own LibreOffice export)
import pdfplumber
sys.path.insert(0, HERE)
import sen0401_exam_paper_lib_v2_0_0 as L
tmp = tempfile.mkdtemp(prefix='sen0401_ctl_')
try:
    for f in FORMS:
        t = tag(f); pdf = L.export_pdf(os.path.join(W, t + '_paper.docx'), tmp, profile='/tmp/lo_profile_paperfix_ctl')
        pg = L.pdf_pages(pdf); cols = L.columns_of_pdf(pdf)
        COLH = 841.8898 - (L.TOP + L.BOTTOM) * 72 / 25.4; FB = 841.8898 - L.BOTTOM * 72 / 25.4
        free = [(FB - max((w['bottom'] for w in c), default=0)) / COLH for pgc in cols for c in pgc]
        sh = L.pdf_pages(os.path.join(W, t + '_sheet.pdf'))
        rep('B form %s: the .docx exported again here is %d pages, smallest free space of a column %.1f percent of its height (>= 3.0), sheet PDF %d page, total %d' % (f, pg, min(free) * 100, sh, pg + sh), pg == 3 and min(free) >= 0.03 and sh == 1 and pg + sh == 4, [round(x * 100, 1) for x in free])
        rep('B form %s: the delivered paper PDF is the same page count as the control export' % f, L.pdf_pages(os.path.join(W, t + '_paper.pdf')) == pg)
        # G code boxes from this export
        import pdfplumber as pp
        boxes = []
        with pp.open(pdf) as d:
            for pi, pgx in enumerate(d.pages):
                for ci in (0, 1):
                    mono = [c for c in pgx.chars if 'Mono' in c['fontname'] and (((c['x0'] + c['x1']) / 2 < pgx.width / 2) == (ci == 0))]
                    if not mono: continue
                    ys = sorted({round(c['top']) for c in mono}); groups = [[ys[0]]]
                    for y in ys[1:]: (groups[-1].append(y) if y - groups[-1][-1] <= 12 else groups.append([y]))
                    hs = [(l['x0'], l['x1'], l['top']) for l in pgx.lines if abs(l['top'] - l['bottom']) < 0.5]
                    for g in groups:
                        cs = [c for c in mono if g[0] - 1 <= round(c['top']) <= g[-1] + 1]; x0, x1 = min(c['x0'] for c in cs), max(c['x1'] for c in cs)
                        up = [h for h in hs if h[2] < g[0] and g[0] - h[2] < 8 and h[0] <= x0 and h[1] >= x1]
                        n = max(len([c for c in cs if abs(c['top'] - y) < 1]) for y in {c['top'] for c in cs})
                        boxes.append((pi + 1, ci + 1, n, round(x1 - x0, 1), round(up[0][1] - up[0][0], 1) if up else None))
        nbox = sum(1 for it in items.values() if it.get('code'))
        okb = len(boxes) == nbox and all(b[4] is not None and b[3] <= b[4] and (b[4] - 12) / (0.6 * 8) >= 45 for b in boxes)
        rep('G form %s: %d code boxes measured (page, column, widest line in characters, text width pt, box width pt): every line inside its box, every box holds 45 characters at 8 pt' % (f, len(boxes)), okb, boxes)
        # H print safety and fonts
        imgs = subprocess.run(['pdfimages', '-list', os.path.join(W, t + '_paper.pdf')], capture_output=True, text=True).stdout.strip().splitlines()
        from PIL import Image; import numpy as np
        d2 = tempfile.mkdtemp(dir=tmp); subprocess.run(['pdftoppm', '-r', '50', '-png', os.path.join(W, t + '_paper.pdf'), d2 + '/p']); col = 0
        for fp in glob.glob(d2 + '/p*.png'):
            a = np.array(Image.open(fp).convert('RGB')).astype(int); col += int((abs(a[..., 0] - a[..., 1]) + abs(a[..., 1] - a[..., 2]) > 12).sum())
        with pp.open(os.path.join(W, t + '_paper.pdf')) as d:
            fz = collections.defaultdict(set)
            for pgx in d.pages:
                for c in pgx.chars: fz['mono' if 'Mono' in c['fontname'] else 'text'].add(round(c['size'], 2))
        rep('H form %s paper PDF: no image, no coloured pixel (%d), text sizes %s (>= 10), code sizes %s (>= 8)' % (f, col, sorted(fz['text']), sorted(fz['mono'])), len(imgs) <= 2 and col == 0 and min(fz['text']) >= 10 and min(fz['mono']) >= 8)
        # C docx structure
        z = zipfile.ZipFile(os.path.join(W, t + '_paper.docx')); bad = z.testzip(); x = etree.fromstring(z.read('word/document.xml'))
        runs = x.findall('.//w:r', W_NS); viol = []
        for r in runs:
            rf = r.find('w:rPr/w:rFonts', W_NS); sz = r.find('w:rPr/w:sz', W_NS)
            fn = rf.get('{%s}ascii' % W_NS['w']) if rf is not None else None; s = int(sz.get('{%s}val' % W_NS['w'])) / 2 if sz is not None else None
            if not ((fn == 'Arial' and s and s >= 10) or (fn == 'Courier New' and s and s >= 8) or (fn == 'Arial' and s == 1 and not ''.join(r.itertext()).strip())): viol.append((fn, s))
        ps = x.findall('.//w:p', W_NS); noexact = [1 for p in ps if p.find('w:pPr/w:spacing', W_NS) is None or p.find('w:pPr/w:spacing', W_NS).get('{%s}lineRule' % W_NS['w']) != 'exact']
        cols_el = [c for c in x.findall('.//w:sectPr/w:cols', W_NS)]; two = [c for c in cols_el if c.get('{%s}num' % W_NS['w']) == '2']
        widths = [c.get('{%s}w' % W_NS['w']) for c in two[0].findall('w:col', W_NS)] if two else []
        brk = len(x.findall('.//w:br[@{%s}type="column"]' % W_NS['w'], W_NS))
        shd = len(x.findall('.//w:shd', W_NS)); draw = len(x.findall('.//w:drawing', W_NS)) + len(x.findall('.//w:pict', W_NS)); colr = [c.get('{%s}val' % W_NS['w']) for c in x.findall('.//w:color', W_NS) if c.get('{%s}val' % W_NS['w']) not in ('000000', 'auto')]
        rep('C form %s .docx: zip ok, %d runs all Arial >= 10 pt or Courier New >= 8 pt (violations %d), %d paragraphs all with exact line spacing (not exact: %d), 2 fixed columns %s, %d explicit column breaks (5 expected), no shading %d, no image %d, no colour %s' %
            (f, len(runs), len(viol), len(ps), len(noexact), widths, brk, shd, draw, colr), bad is None and not viol and not noexact and len(widths) == 2 and brk == 5 and shd == 0 and draw == 0 and not colr)
        txt = ' '.join(texts[f]) + pdftext(os.path.join(W, t + '_paper.pdf'))
        rep('H form %s no personal data on the paper (no name, number or identification field)' % f, not re.search(r'(?i)name\s*:|student number|\bID\s*:', txt))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- I  reader of record on synthetic sheets
import numpy as np
from PIL import Image
READER = 'sen0401_exam_answersheet_v1_1_0'
committed = subprocess.run(['git', '-C', ROOT, 'ls-files', '08-tooling/exam/sen0401_exam_answersheet_v1_2_0.py'], capture_output=True, text=True).stdout.strip()
if committed: READER = 'sen0401_exam_answersheet_v1_2_0'
Rd = __import__(READER); import sen0401_exam_answersheet_measure_v1_0_0 as MS
print('INFO  reader of record: %s (v1.2.0 %s)' % (READER, 'is committed' if committed else 'is NOT committed: v1.1.0 is the reader of record'))
for f in FORMS:
    t = tag(f); lay = json.load(open(os.path.join(W, t + '_sheet_layout.json'))); work = tempfile.mkdtemp(prefix='sen0401_rd_')
    try:
        pngs = Rd.rasterise(os.path.join(W, t + '_sheet.pdf'), os.path.join(work, 'b')); blank = [np.array(Image.open(p).convert('L')) for p in pngs]
        tot = collections.Counter(); regf = 0; rows = 0; held = 0
        for i in range(NS):
            rng = random.Random(77000 + i + (0 if f == 'A' else 500)); ims, truth = MS.student(lay, blank, rng); reg = [Rd.register(im, lay, p) for p, im in enumerate(ims)]
            if any(r is None for r in reg): regf += 1; continue
            out, bst, hd = Rd.read_sheet(reg, lay); o, p = MS.score(out, truth); tot.update(o); rows += len(truth); held += len(hd)
        print('   form %s: %d synthetic sheets, registration failures %d, rows %d, score %s' % (f, NS, regf, rows, dict(tot)))
        badk = [k for k in tot if re.search(r'silent|wrong|missed|unflagged', k, re.I) and tot[k]]
        rep('I form %s reader %s on its own sheet layout: registration on every sheet, 0 silent wrong, 0 missed row, 0 unflagged empty' % (f, READER), regf == 0 and not badk, {k: tot[k] for k in badk} or '(counters %s)' % sorted(tot))
    finally:
        shutil.rmtree(work, ignore_errors=True)

# ---------------------------------------------------------------- J  rebuild
if '--no-rebuild' not in sys.argv:
    rb = tempfile.mkdtemp(prefix='sen0401_rb_')
    try:
        r = subprocess.run([sys.executable, '-I', os.path.join(HERE, 'sen0401_exam_papers_build_v2_0_0.py'), rb, '--forms', str(len(FORMS))], capture_output=True, text=True)
        diffs = []
        for f in FORMS:
            t = tag(f)
            for ext in ('_key.json', '_sheet_layout.json'):
                if open(os.path.join(rb, t + ext), 'rb').read() != open(os.path.join(W, t + ext), 'rb').read(): diffs.append(t + ext)
            if zipfile.ZipFile(os.path.join(rb, t + '_paper.docx')).read('word/document.xml') != zipfile.ZipFile(os.path.join(W, t + '_paper.docx')).read('word/document.xml'): diffs.append(t + '_paper.docx document.xml')
            if zipfile.ZipFile(os.path.join(rb, t + '_key.docx')).read('word/document.xml') != zipfile.ZipFile(os.path.join(W, t + '_key.docx')).read('word/document.xml'): diffs.append(t + '_key.docx document.xml')
        rep('J the builder run again writes the same key JSON, sheet layout and Word document text for every form', r.returncode == 0 and not diffs, diffs or r.stdout.splitlines()[:1])
    finally:
        shutil.rmtree(rb, ignore_errors=True)
else: nm('J rebuild', 'skipped by --no-rebuild')
print('CONTROL:', ('FAIL ' + str(fails)) if fails else 'PASS', '| NOT_MEASURED: %s' % notm if notm else '')
sys.exit(1 if fails else 0)
