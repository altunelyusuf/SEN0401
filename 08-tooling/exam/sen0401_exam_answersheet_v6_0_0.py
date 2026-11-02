"""Answer sheet module, version 6.0.0 (new file, a copy of the sheet module sen0401_exam_answersheet_v1_0_0.py in the manner of the v5 papers' sheet, which stays unchanged and is imported for its constants,
check digit, rasteriser and registration). Pure library (no output when imported). Holds no question and no answer: the caller gives the units, the tips and the bonus parts.
WHAT IS NEW AGAINST THE SHEET OF THE v5 PAPERS (owner corrections of 2026-11-02, points 1, 2, 5, 6):
 * TWO A4 pages. Page 1 is read by the reader; page 2 is the TIPS PAGE (each tip labelled by the question it helps; printed at 10.5 point; not read by any machine; no corner marks, no bubbles).
 * Point 1: every answer place has a place on the sheet. The hand-marked parts of the bonus question (5a, 5b) get ANSWER LINES on page 1 (layout['lines']; NOT in layout['blocks'], so the reader reads page 1 exactly as before).
 * Point 2: a printed sentence says in plain words which answers count: the answers on the question pages count; the sheet is for fast reading; if the two differ the question pages count.
 * Point 6: page 2 carries the plain statement of how points are counted (generated from the scoring rule of sen0401_exam_scoring_v1_0_0.py: nothing typed by hand), unless scoring_note is switched off.
 * To make room for the answer lines on page 1 the geometry packs tighter: two choice rows, two ordering rows and two number boxes share one printed line (each row keeps its own label, its own bubbles and its own 'left blank' bubble).
   Bubble size, bubble pitch, row height, the corner marks and the block types are the v1.0.0 ones, so the reader's thresholds apply unchanged. build_layout raises SheetOverflow when the units do not fit page 1 or the tips do not fit page 2 (nothing is clipped silently).
THE SPEC: {'paper_kind','paper_version','form_code','units':[{'no','kind','opts'|'digits'|'cells'}], 'bonus_parts':[{'no':'5a','points':5,'lines':4}], 'tips':[{'label':'5a','text':'...'}]}"""
import json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_0_0 as A0
from sen0401_exam_answersheet_v1_0_0 import (PW, PH, MM, MARG, FS, BR, PITCH, ROWH, FID_IN, FID_LEG, FID_W, COLW, COLGAP, HUMAN_H, damm_check, damm_valid, make_code, rasterise, register,
                                              bubble_features, classify, read_naive, FD)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
VERSION = '6.0.0'
BLOCK_MAX = {'choice': 5, 'match': 4, 'order': 5, 'bank': 2, 'human': 4}      # one printed sub-question is one block (the v5 papers' setting)
PER_LINE = {'choice': 2, 'order': 2, 'human': 2, 'match': 1, 'bank': 1}        # rows that share one printed line
SLOT_DX = 122.0                                                               # horizontal shift of the second row on a line
HEAD_LINE = 11.6                                                              # line pitch of the header text (10 point type)
LINE_PITCH = 13.5                                                             # pitch of an answer line
TIPS_FS, TIPS_LEAD = 10.5, 14.0                                               # tips page type size and leading (rule R01: 10 point or larger)
TOP_GAP = 8.0
BOTTOM = PH - MARG - 14


class SheetOverflow(Exception): pass


def wrap(text, font, size, width):
    words = text.split(); lines = []; cur = ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if pdfmetrics.stringWidth(t, font, size) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines


RULES = ['1  One row per answer. Fill the bubble of your answer completely, dark ink.',
         '2  To change an answer, draw a large X through the old bubble, then fill the new one.',
         '3  One filled bubble without an X per row; two filled bubbles count as no answer (0 points).',
         '4  After each block, fill the bubble of every number you left blank.',
         '5  Fill-in codes: two digits, one bubble in the upper row and one in the row below.',
         '    Numbers go in the boxes, one digit per box.',
         '6  Make no marks outside the bubbles, boxes and lines. Do not fold or tear the sheet.']
LEGAL = ('Which answers count: the answers you write on the question pages count. This sheet is only for fast reading. If the sheet and the question pages differ, the question pages count.')


def header_layout():
    """Returns (list of (text, bold) lines with their y offsets from the top margin, the y at which the blocks start)."""
    legal = wrap(LEGAL, 'SansB', FS, PW - 2 * MARG)
    y = 64.0; items = []
    for t in RULES: items.append((t, False, y)); y += HEAD_LINE
    y += 3.0
    for t in legal: items.append((t, True, y)); y += HEAD_LINE
    rule_y = y - 2.0
    return items, MARG + rule_y + TOP_GAP


def unit_lines(kind, n, pair):
    per = PER_LINE[kind] if pair else 1
    return math.ceil(n / per)


def block_h(kind, n, pair, rows_per_unit=1):
    if kind == 'human': body = unit_lines(kind, n, pair) * HUMAN_H
    else: body = unit_lines(kind, n, pair) * ROWH * rows_per_unit
    return 14 + body + 17 + 8


def build_layout(spec, block_max=None, pair=True):
    bm = dict(BLOCK_MAX); bm.update(block_max or {})
    blocks = []; cur = None
    for u in spec['units']:
        k = u['kind']
        if cur is None or cur['kind'] != k or len(cur['units']) >= bm[k]:
            cur = {'kind': k, 'units': []}; blocks.append(cur)
        cur['units'].append(u)
    _, top = header_layout()
    flow = []
    for bi, b in enumerate(blocks):
        rpu = 2 if b['kind'] == 'bank' else 1
        flow.append(dict(src=b, h=block_h(b['kind'], len(b['units']), pair, rpu), kind=b['kind'], rpu=rpu))
    for bp in spec.get('bonus_parts', []):
        flow.append(dict(src=bp, h=14 + bp.get('lines', 4) * LINE_PITCH + 8, kind='lines', rpu=1))
    placed = []; lines = []; col, y = 0, top
    for fi, f in enumerate(flow):
        if y + f['h'] > BOTTOM:
            col += 1; y = top
            if col >= 2: raise SheetOverflow('page 1 is full: block %d (%s) does not fit; the blocks need more than two columns of %.0f pt' % (fi, f['kind'], BOTTOM - top))
        x0 = MARG + col * (COLW + COLGAP)
        if f['kind'] == 'lines':
            bp = f['src']; n = bp.get('lines', 4)
            lines.append({'no': bp['no'], 'page': 0, 'col': col, 'x': x0, 'y': y, 'w': COLW, 'h': f['h'], 'n': n, 'points': bp.get('points'),
                          'ys': [y + 14 + (i + 1) * LINE_PITCH - 2 for i in range(n)]})
            y += f['h']; continue
        b = f['src']; per = PER_LINE[b['kind']] if pair else 1; nrows = f['rpu']
        pb = {'id': len(placed), 'kind': b['kind'], 'page': 0, 'col': col, 'x': x0, 'y': y, 'h': f['h'], 'per_line': per, 'units': [], 'closure': []}
        yy0 = y + 14
        for ui, u in enumerate(b['units']):
            line_i, slot = divmod(ui, per); dx = slot * SLOT_DX; ud = {'no': u['no'], 'kind': u['kind'], 'rows': [], 'slot': slot, 'dx': dx}
            if u['kind'] == 'human':
                yy = yy0 + line_i * HUMAN_H
                ud['box'] = {'x': x0 + 24 + (slot * 120 if per > 1 else 0), 'y': yy + 2, 'w': 18.0 * u.get('cells', 5), 'h': HUMAN_H - 6}
                ud['label_x'] = x0 + 20 + (slot * 120 if per > 1 else 0)
            else:
                yy = yy0 + line_i * ROWH * nrows
                for r in range(nrows):
                    opts = '0123456789' if u['kind'] == 'bank' else u['opts']
                    ud['rows'].append({'cy': yy + ROWH * r + ROWH / 2, 'opts': opts, 'cx': [x0 + dx + 26 + i * PITCH + BR for i in range(len(opts))]})
                ud['label_x'] = x0 + dx + 20
            pb['units'].append(ud)
        cy = yy0 + (unit_lines(b['kind'], len(b['units']), pair) * (HUMAN_H if b['kind'] == 'human' else ROWH * nrows)) + 8.5; cx = x0 + 62
        for ud in pb['units']:
            pb['closure'].append({'no': ud['no'], 'cx': cx + BR, 'cy': cy}); cx += 38
        placed.append(pb); y += f['h']
    fid = []
    for name, (cx, cy) in {'TL': (FID_IN, FID_IN), 'TR': (PW - FID_IN, FID_IN), 'BL': (FID_IN, PH - FID_IN), 'BR': (PW - FID_IN, PH - FID_IN)}.items():
        sx = 1 if cx < PW / 2 else -1; sy = 1 if cy < PH / 2 else -1
        fid.append({'page': 0, 'name': name, 'corner': (cx, cy), 'sx': sx, 'sy': sy, 'center': (cx + sx * FID_LEG / 2, cy + sy * FID_LEG / 2)})
    tips = tips_layout(spec)
    return {'version': VERSION, 'page_pt': [PW, PH], 'pages': 2, 'reader_pages': [0], 'tips_page': 1, 'bubble_r': BR, 'form_code': spec['form_code'], 'spec': spec, 'blocks': placed, 'lines': lines,
            'fiducials': fid, 'tips': tips, 'free_height_pt': {'page1_columns': 2 * (BOTTOM - top), 'page1_used': sum(f['h'] for f in flow)}}


def scoring_note_text():
    """The plain statement of how points are counted, generated from the scoring rule (nothing typed by hand)."""
    import sen0401_exam_scoring_v1_0_0 as S
    t = {x['id']: x for x in S.rule_table()['answer_types']}
    fr = lambda i: t[i]['penalty_fraction_exact']
    def word(f): return {'1/3': 'one third', '1/5': 'one fifth', '1/4': 'one quarter', '1/9': 'one ninth', '1/99': 'one ninety-ninth'}.get(f, f)
    return ('How points are counted. A right answer earns its points. A blank answer earns 0 and costs nothing. Two answers in one place count as no answer: 0 points. '
            'A wrong answer costs a part of the points of that answer, chosen so that a blind guess is worth zero on average: %s for a choice of four and for a fill-in blank, %s for a matching pair, '
            '%s for an ordering step, %s for a one-digit number. A number of three or more digits costs nothing extra when it is wrong. Leaving an answer blank is always safe.'
            % (word(fr('choice_four')), word(fr('matching_6')), word(fr('ordering_5')), word(fr('number_1_digit'))))


def tips_layout(spec, scoring_note=True):
    """Lays out page 2: returns {'lines': [(y, font, size, text)], 'used': pt, 'free': pt}. Raises SheetOverflow when the text does not fit."""
    width = PW - 2 * MARG; y = MARG + 14.0; out = []
    out.append((y, 'SansB', 13, 'SEN0401 tips page'))
    out.append((y, 'Sans', FS, 'form code %s' % spec['form_code'], 'right')); y += 17
    for t in wrap('This page is not read by a machine. Write no answers here. Each tip names the question it helps.', 'Sans', FS, width): out.append((y, 'Sans', FS, t)); y += HEAD_LINE
    y += 4
    out.append(('rule', y)); y += 10
    if spec.get('scoring_note', True):
        for t in wrap(scoring_note_text(), 'Sans', TIPS_FS, width): out.append((y, 'Sans', TIPS_FS, t)); y += TIPS_LEAD
        y += 4; out.append(('rule', y)); y += 12
    for tip in spec.get('tips', []):
        lab = 'Question %s.' % tip['label']; lw = pdfmetrics.stringWidth(lab + ' ', 'SansB', TIPS_FS)
        ls = wrap(tip['text'], 'Sans', TIPS_FS, width - lw)
        if not ls: continue
        out.append((y, 'SansB', TIPS_FS, lab, 'label'))
        for i, t in enumerate(ls): out.append((y, 'Sans', TIPS_FS, t, 'indent' if i == 0 else 'indent')); y += TIPS_LEAD
        y += 4
    limit = PH - MARG - 18
    if y > limit: raise SheetOverflow('the tips page is full: the text needs %.0f pt of %.0f pt' % (y - MARG, limit - MARG))
    return {'lines': out, 'end_y': y, 'limit_y': limit}


def render(layout, path):
    c = canvas.Canvas(path, pagesize=(PW, PH), invariant=1); c.setTitle('SEN0401 answer sheet v%s' % VERSION); c.setAuthor('')
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0)
    Y = lambda y: PH - y
    spec = layout['spec']
    # ---- page 1
    for f in layout['fiducials']:
        cx, cy = f['corner']; sx, sy = f['sx'], f['sy']
        c.setLineWidth(FID_W); c.setLineCap(0)
        c.line(cx - sx * FID_W / 2, Y(cy), cx + sx * FID_LEG, Y(cy)); c.line(cx, Y(cy - sy * FID_W / 2), cx, Y(cy + sy * FID_LEG))
    c.setLineWidth(0.6)
    c.setFont('SansB', 13); c.drawString(MARG, Y(MARG + 14), 'SEN0401 answer sheet - %s' % ('midterm' if spec['paper_kind'] == 'Midterm' else 'make-up exam'))
    c.setFont('Sans', FS); c.drawRightString(PW - MARG, Y(MARG + 14), 'form code %s' % spec['form_code'])
    c.drawString(MARG, Y(MARG + 34), 'Identification (as the instructor directs):'); c.rect(MARG + 215, Y(MARG + 42), 295, 20)
    items, top = header_layout()
    for t, bold, yo in items:
        c.setFont('SansB' if bold else 'Sans', FS); c.drawString(MARG, Y(MARG + yo), t)
    c.line(MARG, Y(top - TOP_GAP), PW - MARG, Y(top - TOP_GAP))
    c.setFont('Sans', FS); c.drawCentredString(PW / 2, Y(PH - MARG - 2), 'page 1 of 2 - answers (the tips are on page 2)')
    for b in layout['blocks']:
        x0, y0 = b['x'], b['y']
        c.setLineWidth(0.5); c.line(x0, Y(y0 + 1), x0 + COLW, Y(y0 + 1))
        if b['kind'] != 'human':
            for slot in range(b['per_line']):
                us = [u for u in b['units'] if u['slot'] == slot]
                if not us: continue
                r0 = us[0]['rows'][0]
                for ch, cx in zip(r0['opts'], r0['cx']): c.setFont('Sans', FS); c.drawCentredString(cx, Y(y0 + 11), ch)
        else:
            c.setFont('Sans', FS); c.drawString(x0 + 24, Y(y0 + 11), 'write the result, one digit per box')
        for u in b['units']:
            if u['kind'] == 'human':
                bx = u['box']; ncell = int(round(bx['w'] / 18))
                c.setFont('Sans', FS); c.drawRightString(u['label_x'], Y(bx['y'] + bx['h'] / 2 + 3.5), u['no'])
                for i in range(ncell): c.rect(bx['x'] + i * 18, Y(bx['y'] + bx['h']), 18, bx['h'])
                if b['per_line'] == 1: c.drawString(bx['x'] + bx['w'] + 6, Y(bx['y'] + bx['h'] / 2 + 3.5), u['no'])
                continue
            for ri, row in enumerate(u['rows']):
                cy = row['cy']; c.setFont('Sans', FS)
                if ri == 0: c.drawRightString(u['label_x'], Y(cy + 3.5), u['no'])
                for cx in row['cx']: c.circle(cx, Y(cy), BR, stroke=1, fill=0)
                if ri == 0:
                    lx = row['cx'][-1] + BR + 6; nxt = x0 + (u['slot'] + 1) * SLOT_DX + 20 - pdfmetrics.stringWidth(u['no'], 'Sans', FS)
                    if u['slot'] == b['per_line'] - 1 or b['per_line'] == 1 or lx + pdfmetrics.stringWidth(u['no'], 'Sans', FS) + 3 <= nxt: c.drawString(lx, Y(cy + 3.5), u['no'])   # the second label of a shared line is dropped when it would touch the next row's left label
        cl = b['closure']; cy = cl[0]['cy']
        c.setFont('Sans', FS); c.drawString(x0, Y(cy + 3.5), 'left blank:')
        for q in cl:
            c.circle(q['cx'], Y(q['cy']), BR, stroke=1, fill=0); c.drawString(q['cx'] + BR + 3, Y(q['cy'] + 3.5), q['no'])
    for ln in layout['lines']:
        x0, y0 = ln['x'], ln['y']
        c.setLineWidth(0.5); c.line(x0, Y(y0 + 1), x0 + COLW, Y(y0 + 1)); c.setFont('Sans', FS)
        c.drawString(x0, Y(y0 + 11), '%s%s - written answer, marked by hand' % (ln['no'], (' (%s points)' % ln['points']) if ln.get('points') else ''))
        c.setLineWidth(0.4)
        for yl in ln['ys']: c.line(x0, Y(yl), x0 + COLW, Y(yl))
    c.showPage()
    # ---- page 2: the tips page (no corner marks, no bubbles)
    tl = layout['tips']; width = PW - 2 * MARG
    for e in tl['lines']:
        if e[0] == 'rule':
            c.setLineWidth(0.5); c.line(MARG, Y(e[1]), PW - MARG, Y(e[1])); continue
        y, font, size, text = e[:4]; mode = e[4] if len(e) > 4 else 'left'
        c.setFont(font, size)
        if mode == 'right': c.drawRightString(PW - MARG, Y(y), text)
        elif mode == 'label': c.drawString(MARG, Y(y), text)
        elif mode == 'indent':
            lab = [x for x in tl['lines'] if len(x) > 4 and x[4] == 'label' and x[0] <= y]
            lw = pdfmetrics.stringWidth(lab[-1][3] + ' ', 'SansB', TIPS_FS) if lab else 0
            c.drawString(MARG + lw, Y(y), text)
        else: c.drawString(MARG, Y(y), text)
    c.setFont('Sans', FS); c.drawCentredString(PW / 2, Y(PH - MARG - 2), 'page 2 of 2 - tips')
    c.save()


def write_pair(layout, outdir, stem):
    pdf = os.path.join(outdir, stem + '.pdf'); js = os.path.join(outdir, stem + '_layout.json')
    render(layout, pdf); json.dump(layout, open(js, 'w'), indent=1)
    return pdf, js
