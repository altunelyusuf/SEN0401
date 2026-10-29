"""Answer sheet for the printed SEN0401 paper, version 1.0.0: layout, renderer, reader and the check-digit code.
Pure library (no output when imported). Command line:  answersheet.py build OUTDIR [--spec FILE] [--kind Midterm|MakeUp]
One place per answer: every unit (item, premise, step, blank) has its own row of empty bubbles; the position number is printed at both ends.
Mistake methods built in: AM1 one place per answer, AM2 row guard (number at both ends), AM3 block closure (the student ticks the units left
blank; the reader compares with the blank rows), AM4 strike rule (an X through a bubble voids it), AM5 check digit (Damm) on the bank codes of
fill-in blanks, AM6 three-state reading (filled / faint / empty) with a hold for a person, AM7 fiducial corners so a skewed scan is read right.
Everything is black line art on white; text is 10 point or larger."""
import collections, json, math, os, subprocess, sys, tempfile
sys.dont_write_bytecode = True
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

VERSION = '1.0.0'
FD = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('Sans', FD + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('SansB', FD + 'DejaVuSans-Bold.ttf'))
PW, PH = 595.2756, 841.8898          # A4 in points (the paper size is the owner's decision; A4 is the default)
MM = 72 / 25.4
MARG = 15 * MM
FS = 10                               # body point size (rule R01: 10 point or larger)
BR = 5.5                              # bubble radius, pt
PITCH = 19.0                          # bubble pitch, pt
ROWH = 15.5                           # row height, pt
FID_IN, FID_LEG, FID_W = 7 * MM, 8 * MM, 1.2 * MM
COLW, COLGAP = 245.0, 20.0
BLOCK_MAX = {'choice': 5, 'match': 5, 'order': 5, 'bank': 3, 'human': 4}
HUMAN_H = 26.0

# ---------------------------------------------------------------- the check digit (Damm: catches every single-digit slip and every adjacent swap)
DAMM = ['0317598642', '7092154863', '4206871359', '1750983426', '6123045978', '3674209581', '5869720134', '8945362017', '9438617205', '2581436790']
def damm_check(digits):
    t = 0
    for ch in digits: t = int(DAMM[t][int(ch)])
    return str(t)                     # the digit that makes the whole code come out to 0
def damm_valid(code):
    t = 0
    for ch in code: t = int(DAMM[t][int(ch)])
    return t == 0
def make_code(serial, width):
    s = str(serial).zfill(width); return s + damm_check(s)
def serial_width(n_entries): return len(str(n_entries))

# ---------------------------------------------------------------- the specification of a sheet
def default_spec(kind='Midterm', version_seq=1):
    """A demonstration paper (NOT the owner's exam: the number and mix of items are his decision, Q2). Units are the places for answers."""
    units = []
    for k in range(1, 25): units.append({'no': str(k), 'kind': 'choice', 'opts': 'ABCD'})
    for k, c in enumerate('abcd'): units.append({'no': '25' + c, 'kind': 'match', 'opts': 'ABCDEFG'})
    for k in range(3): units.append({'no': '26' + 'abc'[k], 'kind': 'order', 'opts': '123'})
    for k in range(27, 31): units.append({'no': str(k), 'kind': 'bank', 'digits': 2})
    for k in (31, 32, 33): units.append({'no': str(k), 'kind': 'human', 'cells': 5})
    return {'paper_kind': kind, 'paper_version': version_seq, 'form_code': make_code(1000 + version_seq * 10 + (0 if kind == 'Midterm' else 1), 4), 'units': units}

# ---------------------------------------------------------------- layout: blocks flowed into two columns per page
def block_height(kind, n, rows_per_unit=1):
    body = n * (HUMAN_H if kind == 'human' else ROWH * rows_per_unit)
    return 14 + body + 17 + 8          # header row, rows, closure row, gap

def build_layout(spec):
    # group consecutive units of one kind into blocks, and keep the units of one printed item (same leading number) together when they fit
    blocks = []; cur = None
    for u in spec['units']:
        k = u['kind']
        if cur is None or cur['kind'] != k or len(cur['units']) >= BLOCK_MAX[k]:
            cur = {'kind': k, 'units': []}; blocks.append(cur)
        cur['units'].append(u)
    top = MARG + 175                  # header zone above the blocks (title, form code, identification, rules)
    bottom = PH - MARG - 14
    cells = []; humans = []; closures = []; placed = []
    page, col, y = 0, 0, top
    for bi, b in enumerate(blocks):
        rows = [2 if (u['kind'] == 'bank') else 1 for u in b['units']]
        h = 14 + (sum(rows) * ROWH if b['kind'] != 'human' else len(b['units']) * HUMAN_H) + 17 + 8
        if y + h > bottom:
            col += 1; y = top if page == 0 else MARG + 10
            if col == 2: page += 1; col = 0; y = MARG + 10
        x0 = MARG + col * (COLW + COLGAP)
        pb = {'id': bi, 'kind': b['kind'], 'page': page, 'col': col, 'x': x0, 'y': y, 'h': h, 'units': [], 'closure': []}
        yy = y + 14
        for u, nr in zip(b['units'], rows):
            ud = {'no': u['no'], 'kind': u['kind'], 'rows': []}
            if u['kind'] == 'human':
                ud['box'] = {'x': x0 + 24, 'y': yy + 2, 'w': 18.0 * u.get('cells', 5), 'h': HUMAN_H - 6}
                yy += HUMAN_H
            else:
                for r in range(nr):
                    if u['kind'] == 'bank': opts = '0123456789'
                    else: opts = u['opts']
                    row = {'cy': yy + ROWH / 2, 'opts': opts, 'cx': [x0 + 26 + i * PITCH + BR for i in range(len(opts))]}
                    ud['rows'].append(row); yy += ROWH
            pb['units'].append(ud)
        # closure row: one bubble per unit of the block, labelled with the unit number
        cy = yy + 8.5; cx = x0 + 62
        for ud in pb['units']:
            pb['closure'].append({'no': ud['no'], 'cx': cx + BR, 'cy': cy}); cx += 38
        placed.append(pb); y += h
    pages = (max(p['page'] for p in placed) + 1) if placed else 1
    fid = []
    for pg in range(pages):
        for name, (cx, cy) in {'TL': (FID_IN, FID_IN), 'TR': (PW - FID_IN, FID_IN), 'BL': (FID_IN, PH - FID_IN), 'BR': (PW - FID_IN, PH - FID_IN)}.items():
            sx = 1 if cx < PW / 2 else -1; sy = 1 if cy < PH / 2 else -1
            fid.append({'page': pg, 'name': name, 'corner': (cx, cy), 'sx': sx, 'sy': sy,
                        'center': (cx + sx * FID_LEG / 2, cy + sy * FID_LEG / 2)})       # centre of the L's bounding box
    return {'version': VERSION, 'page_pt': [PW, PH], 'pages': pages, 'bubble_r': BR, 'spec': spec, 'blocks': placed, 'fiducials': fid}

# ---------------------------------------------------------------- rendering (black lines on white, no fill, no images)
def render(layout, path, bank_labels=None):
    c = canvas.Canvas(path, pagesize=(PW, PH), invariant=1); c.setTitle('SEN0401 answer sheet v%s' % VERSION); c.setAuthor('')
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0)
    Y = lambda y: PH - y
    spec = layout['spec']
    for pg in range(layout['pages']):
        for f in layout['fiducials']:
            if f['page'] != pg: continue
            cx, cy = f['corner']; sx, sy = f['sx'], f['sy']
            c.setLineWidth(FID_W); c.setLineCap(0)
            c.line(cx - sx * FID_W / 2, Y(cy), cx + sx * FID_LEG, Y(cy)); c.line(cx, Y(cy - sy * FID_W / 2), cx, Y(cy + sy * FID_LEG))
        c.setLineWidth(0.6)
        if pg == 0:
            c.setFont('SansB', 13); c.drawString(MARG, Y(MARG + 14), 'SEN0401 answer sheet - %s' % ('midterm' if spec['paper_kind'] == 'Midterm' else 'make-up exam'))
            c.setFont('Sans', FS); c.drawRightString(PW - MARG, Y(MARG + 14), 'form code %s' % spec['form_code'])
            c.drawString(MARG, Y(MARG + 34), 'Identification (as the instructor directs):'); c.rect(MARG + 215, Y(MARG + 42), 295, 20)
            rules = ['1  One row per answer. Fill the bubble of your answer completely, dark ink.',
                     '2  To change an answer, draw a large X through the old bubble, then fill the new one.',
                     '3  Exactly one filled bubble without an X per row; two filled bubbles count as no answer.',
                     '4  After each block, fill the bubble of every number you left blank.',
                     '5  Fill-in codes: two digits, one bubble in the upper row and one in the row below. Numbers go in the boxes, one digit per box.',
                     '6  Make no marks outside the bubbles and boxes. Do not fold or tear the sheet.']
            for i, t in enumerate(rules): c.drawString(MARG, Y(MARG + 64 + i * 12.5), t)
            c.line(MARG, Y(MARG + 150), PW - MARG, Y(MARG + 150))
        c.setFont('Sans', FS); c.drawCentredString(PW / 2, Y(PH - MARG - 2), 'page %d of %d' % (pg + 1, layout['pages']))
        for b in layout['blocks']:
            if b['page'] != pg: continue
            x0, y0 = b['x'], b['y']
            c.setLineWidth(0.5); c.line(x0, Y(y0 + 1), x0 + COLW, Y(y0 + 1))
            # header
            if b['kind'] != 'human':
                u0 = b['units'][0]['rows'][0]
                for ch, cx in zip(u0['opts'], u0['cx']): c.setFont('Sans', FS); c.drawCentredString(cx, Y(y0 + 11), ch)
            else:
                c.setFont('Sans', FS); c.drawString(x0 + 24, Y(y0 + 11), 'write the result, one digit per box')
            for u in b['units']:
                if u['kind'] == 'human':
                    bx = u['box']; ncell = int(round(bx['w'] / 18))
                    c.setFont('Sans', FS); c.drawRightString(x0 + 20, Y(bx['y'] + bx['h'] / 2 + 3.5), u['no'])
                    for i in range(ncell): c.rect(bx['x'] + i * 18, Y(bx['y'] + bx['h']), 18, bx['h'])
                    c.drawString(bx['x'] + bx['w'] + 6, Y(bx['y'] + bx['h'] / 2 + 3.5), u['no'])
                    continue
                for ri, row in enumerate(u['rows']):
                    cy = row['cy']
                    c.setFont('Sans', FS)
                    if ri == 0: c.drawRightString(x0 + 20, Y(cy + 3.5), u['no'])
                    else: c.drawRightString(x0 + 20, Y(cy + 3.5), '')
                    for cx in row['cx']: c.circle(cx, Y(cy), BR, stroke=1, fill=0)
                    if ri == 0: c.drawString(row['cx'][-1] + BR + 6, Y(cy + 3.5), u['no'])
            # closure row
            cl = b['closure']; cy = cl[0]['cy']
            c.setFont('Sans', FS); c.drawString(x0, Y(cy + 3.5), 'left blank:')
            for q in cl:
                c.circle(q['cx'], Y(q['cy']), BR, stroke=1, fill=0); c.drawString(q['cx'] + BR + 3, Y(q['cy'] + 3.5), q['no'])
        if pg < layout['pages'] - 1: c.showPage()
    c.save()

def write_pair(layout, outdir, stem):
    pdf = os.path.join(outdir, stem + '.pdf'); js = os.path.join(outdir, stem + '_layout.json')
    render(layout, pdf)
    json.dump(layout, open(js, 'w'), indent=1)
    return pdf, js

# ---------------------------------------------------------------- reading: rasterise, register on the corner marks, classify every bubble
DPI = 150; S = DPI / 72.0
def rasterise(pdf, outprefix):
    subprocess.run(['pdftoppm', '-r', str(DPI), '-gray', '-png', pdf, outprefix], check=True)
    import glob
    return sorted(glob.glob(outprefix + '*.png'))

def register(img, layout, page):
    """Finds the four corner marks, fits a similarity transform, returns the image in nominal sheet coordinates."""
    import numpy as np, cv2
    from scipy import ndimage as ndi
    obs = []; nom = []
    win = int(60 * S)
    for f in layout['fiducials']:
        if f['page'] != page: continue
        cx, cy = f['corner']
        x_lo = 0 if cx < PW / 2 else img.shape[1] - win; y_lo = 0 if cy < PH / 2 else img.shape[0] - win
        sub = img[y_lo:y_lo + win, x_lo:x_lo + win] < 128
        lab, n = ndi.label(sub)
        if n == 0: return None
        sizes = ndi.sum(sub, lab, range(1, n + 1)); k = int(np.argmax(sizes)) + 1
        ys, xs = np.nonzero(lab == k)
        obs.append(((xs.min() + xs.max()) / 2 + x_lo, (ys.min() + ys.max()) / 2 + y_lo)); nom.append((f['center'][0] * S, f['center'][1] * S))
    if len(obs) < 3: return None
    M, _ = cv2.estimateAffinePartial2D(np.array(obs, np.float32), np.array(nom, np.float32))
    if M is None: return None
    return cv2.warpAffine(img, M, (int(round(PW * S)), int(round(PH * S))), flags=cv2.INTER_LINEAR, borderValue=255)

def _masks():
    import numpy as np
    h = int(math.ceil(8.5 * S)); yy, xx = np.mgrid[-h:h + 1, -h:h + 1] / S
    d = np.sqrt(xx ** 2 + yy ** 2)
    inner = d <= 0.7 * BR                                       # inside the printed ring
    corner = (d >= 8.0) & (np.abs(xx) <= 8.5) & (np.abs(yy) <= 8.5)   # outside any fill, inside the cell square
    quad = [corner & (xx < 0) & (yy < 0), corner & (xx > 0) & (yy < 0), corner & (xx < 0) & (yy > 0), corner & (xx > 0) & (yy > 0)]
    return h, inner, quad
_M = None
def bubble_features(img, cx, cy):
    global _M
    import numpy as np
    if _M is None: _M = _masks()
    h, inner, quad = _M
    px, py = int(round(cx * S)), int(round(cy * S))
    cell = img[py - h:py + h + 1, px - h:px + h + 1] < 140
    if cell.shape != inner.shape: return 0.0, 0
    fin = cell[inner].mean()
    corners = sum(1 for q in quad if cell[q].mean() > T_CORNER_INK)
    return float(fin), corners

T_FILLED, T_FAINT, T_CORNERS, T_CORNER_INK = 0.50, 0.12, 3, 0.08
def classify(fin, corners):
    if corners >= T_CORNERS: return 'struck'
    if fin >= T_FILLED: return 'filled'
    if fin >= T_FAINT: return 'faint'
    return 'empty'

T_HUMAN = 0.02
def human_ink(img, bx):
    """The largest share of dark pixels inside any one digit box, with 3 pt kept off the printed lines."""
    best = 0.0
    for i in range(int(round(bx['w'] / 18))):
        x1, x2 = int((bx['x'] + i * 18 + 3) * S), int((bx['x'] + i * 18 + 15) * S); y1, y2 = int((bx['y'] + 3) * S), int((bx['y'] + bx['h'] - 3) * S)
        best = max(best, float((img[y1:y2, x1:x2] < 140).mean()))
    return best

def read_row(img, row):
    st = [classify(*bubble_features(img, cx, row['cy'])) for cx in row['cx']]
    filled = [i for i, s in enumerate(st) if s == 'filled']; faint = [i for i, s in enumerate(st) if s == 'faint']
    if len(filled) == 1 and not faint: return row['opts'][filled[0]], None
    if len(filled) >= 2: return None, 'double'
    if faint: return None, 'faint'
    return None, 'blank'                                          # blank is not a flag by itself

def read_sheet(imgs, layout, check_digits=True, closure=True):
    """imgs: list of registered page images. Returns {unit_no: {'value', 'flag'}} and the list of blocks held."""
    out = {}; blockstate = []
    region_of = {}; r = -1; prev = None
    for b in layout['blocks']:
        if b['kind'] != prev: r += 1; prev = b['kind']
        region_of[b['id']] = r
    region_answered = collections.defaultdict(bool)
    for b in layout['blocks']:
        img = imgs[b['page']]
        for u in b['units']:
            if u['kind'] == 'human': region_answered[region_of[b['id']]] |= human_ink(img, u['box']) > T_HUMAN
            else: region_answered[region_of[b['id']]] |= any(read_row(img, row)[1] != 'blank' for row in u['rows'])
    for b in layout['blocks']:
        img = imgs[b['page']]; blank = set(); res = {}
        for u in b['units']:
            if u['kind'] == 'human':
                ink = human_ink(img, bx := u['box']); written = ink > T_HUMAN
                res[u['no']] = {'value': 'WRITTEN' if written else None, 'flag': None if written else 'blank', 'ink': ink}
                if not written: blank.add(u['no'])
                continue
            vals = []; flags = []
            for row in u['rows']:
                v, fl = read_row(img, row); vals.append(v); flags.append(fl)
            if u['kind'] == 'bank':
                if all(f == 'blank' for f in flags): res[u['no']] = {'value': None, 'flag': 'blank'}; blank.add(u['no'])
                elif any(f in ('double', 'faint') for f in flags): res[u['no']] = {'value': None, 'flag': [f for f in flags if f and f != 'blank'][0]}
                elif any(f == 'blank' for f in flags): res[u['no']] = {'value': None, 'flag': 'incomplete'}
                else:
                    code = ''.join(vals)
                    if check_digits and not damm_valid(code): res[u['no']] = {'value': code, 'flag': 'check-digit'}
                    else: res[u['no']] = {'value': code, 'flag': None}
            else:
                v, fl = vals[0], flags[0]
                res[u['no']] = {'value': v, 'flag': None if fl in (None, 'blank') else fl}
                if fl == 'blank': blank.add(u['no'])
        declared = set()
        for q in b['closure']:
            fin, cor = bubble_features(img, q['cx'], q['cy'])
            if classify(fin, cor) in ('filled',): declared.add(q['no'])
        reg_id = region_of[b['id']]
        declared_filled = declared - blank          # the student says blank, the row is not: the signature of a skipped item whose row was used
        undeclared_blank = (blank - declared) if region_answered[reg_id] else set()   # in a region where nothing was answered, blank rows are untouched rows, not a mismatch. A blank row the student did not declare: the landing place of a shifted run, or a forgotten tick
        blockstate.append({'id': b['id'], 'blank': sorted(blank), 'declared': sorted(declared), 'declared_filled': sorted(declared_filled),
                           'undeclared_blank': sorted(undeclared_blank), 'mismatch': bool(closure and (declared_filled or undeclared_blank))})
        for no, r in res.items(): out[no] = r
    # hold: a mismatching block is held whole; from a block with a declared-but-filled row up to the next block with an undeclared blank row
    # (the landing of the shift) every block of the same kind in between is held too, because a shifted run moves the answers of all of them.
    held = set()
    if closure:
        for i, st in enumerate(blockstate):
            if st['mismatch']: held.add(i)
            if st['declared_filled']:
                for j in range(i + 1, len(blockstate)):
                    if layout['blocks'][j]['kind'] != layout['blocks'][i]['kind']: break
                    held.add(j)
                    if blockstate[j]['undeclared_blank']: break
        # end of a run of same-kind blocks: an undeclared blank in its last unit is where a run shifted from an earlier block lands, and nothing says where it began
        for i, st in enumerate(blockstate):
            if st['undeclared_blank'] and layout['blocks'][i]['units'][-1]['no'] in st['undeclared_blank'] and (i + 1 == len(blockstate) or layout['blocks'][i + 1]['kind'] != layout['blocks'][i]['kind']):
                j = i
                while j >= 0 and layout['blocks'][j]['kind'] == layout['blocks'][i]['kind']: held.add(j); j -= 1
    for i in held:
        for u in layout['blocks'][i]['units']:
            r = out[u['no']]
            if r['flag'] is None: r['flag'] = 'held-block'
    return out, blockstate, sorted(held)

def read_naive(imgs, layout):
    """The reader without the methods: the darkest bubble of a row if it is dark enough; no strike rule, no closure, no check digit, no flags."""
    out = {}
    for b in layout['blocks']:
        img = imgs[b['page']]
        for u in b['units']:
            if u['kind'] == 'human':
                out[u['no']] = 'WRITTEN' if human_ink(img, u['box']) > T_HUMAN else None; continue
            vals = []
            for row in u['rows']:
                fs = [bubble_features(img, cx, row['cy'])[0] for cx in row['cx']]
                m = max(fs); vals.append(row['opts'][fs.index(m)] if m >= 0.3 else None)
            out[u['no']] = (''.join(vals) if None not in vals else None) if u['kind'] == 'bank' else vals[0]
    return out

def main():
    import argparse
    a = argparse.ArgumentParser(); a.add_argument('cmd'); a.add_argument('outdir'); a.add_argument('--kind', default='Midterm'); a.add_argument('--spec')
    o = a.parse_args()
    spec = json.load(open(o.spec)) if o.spec else default_spec(o.kind)
    os.makedirs(o.outdir, exist_ok=True)
    lay = build_layout(spec); print(write_pair(lay, o.outdir, 'sen0401_exam_answersheet_%s_v1_0_0' % o.kind.lower()))
if __name__ == '__main__': main()
