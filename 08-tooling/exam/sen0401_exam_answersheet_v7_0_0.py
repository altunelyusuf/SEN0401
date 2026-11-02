"""Answer sheet module, version 7.0.0 (new file, a copy of sen0401_exam_answersheet_v6_1_0.py, which stays unchanged; the v1.0.0 module is imported unchanged for its constants, rasteriser and registration).
Pure library (no output when imported). Holds no question and no answer: the caller gives the unit list.
WHAT IS NEW (owner redesign of 2026-11-02, 18:20 Istanbul, rulings 5 and 7):
 * ONE A4 page. No tips page, no scoring note, no bonus lines, no number boxes: the sheet holds choice-type answers only.
 * Every place has FIVE alternatives: a choice unit A-E, a matching row A-E, an ordering row 1-5, a fill-in blank A-E (kind 'fill'; the bank entries are lettered).
   Number and code-trace answers are NOT on the sheet (they are written on the question pages); a unit of kind 'human' or 'bank' is refused (SheetError).
 * The printed sentences are plain, at most 25 words each; none is about points taken away.
 * A unit may carry a 'group' value: a new block starts when the group changes (one printed sub-question is one block); inside a group a block holds at most BLOCK_MAX units.
 * units_from_list(): builds the units from a unit list [{'type': 'choice'|'matching'|'ordering'|'fill', 'labels': [...]}], so the papers builder can call the sheet with the final key.
 Bubble size, bubble pitch, row height, the corner marks and the block-closure row are the v1.0.0 / v6.1.0 ones, so the reader's thresholds apply unchanged (the reader is sen0401_exam_answersheet_v1_4_0.py).
 build_layout raises SheetOverflow when the units do not fit the page (nothing is clipped silently) and SheetError for a unit the sheet does not carry.
THE SPEC: {'paper_kind','paper_version','form_code','units':[{'no','kind':'choice'|'match'|'order'|'fill','opts','group'}]}"""
import json, math, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_answersheet_v1_0_0 as A0
from sen0401_exam_answersheet_v1_0_0 import (PW, PH, MM, MARG, FS, BR, PITCH, ROWH, FID_IN, FID_LEG, FID_W, COLW, COLGAP, damm_check, damm_valid, make_code, rasterise, register,
                                              bubble_features, classify, read_naive, FD)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
VERSION = '7.0.0'
OPTS = {'choice': 'ABCDE', 'match': 'ABCDE', 'order': '12345', 'fill': 'ABCDE'}
TYPE_KIND = {'choice': 'choice', 'matching': 'match', 'ordering': 'order', 'fill': 'fill'}
BLOCK_MAX = {'choice': 5, 'match': 4, 'order': 5, 'fill': 2}                  # one printed sub-question is one block
PER_LINE = {'choice': 2, 'order': 2, 'match': 2, 'fill': 2}                   # rows that share one printed line
SLOT_DX = 124.0                                                               # horizontal shift of the second row on a line (five bubbles need 113 pt)
HEAD_LINE = 11.6
TOP_GAP = 8.0
BOTTOM = PH - MARG - 14


class SheetOverflow(Exception): pass
class SheetError(Exception): pass


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


RULES = ['1  One row per answer. Fill the bubble of your answer completely, in dark ink.',
         '2  To change an answer, draw a large X through the old bubble, then fill the new one.',
         '3  After each block, fill the bubble of every question you left blank.',
         '4  Make no marks outside the bubbles. Do not fold or tear the sheet.',
         '5  Numbers and code results are written on the question pages, not on this sheet.']
LEGAL = ['The answers written on the question pages count. This sheet is only for fast reading.',
         'If the sheet and the question pages differ, the question pages count.',
         'Two filled bubbles in one place count as no answer.']
PRINTED_SENTENCES = RULES + LEGAL


def header_layout():
    """Returns (list of (text, bold, y offset from the top margin), the y at which the blocks start)."""
    y = 64.0; items = []
    for t in RULES: items.append((t, False, y)); y += HEAD_LINE
    y += 3.0
    for t in LEGAL: items.append((t, True, y)); y += HEAD_LINE
    rule_y = y - 2.0
    return items, MARG + rule_y + TOP_GAP


def units_from_list(unit_list):
    """unit_list: [{'type': 'choice'|'matching'|'ordering'|'fill', 'labels': ['1a', ...]}] in sheet order -> units. Each list entry is one group (a new block starts at its first unit)."""
    units = []
    for gi, e in enumerate(unit_list):
        if e['type'] not in TYPE_KIND: raise SheetError('the sheet carries choice, matching, ordering and fill only; refused unit type: %r' % e['type'])
        k = TYPE_KIND[e['type']]
        for lab in e['labels']: units.append({'no': lab, 'kind': k, 'opts': OPTS[k], 'group': gi})
    return units


def check_units(units):
    seen = set()
    for u in units:
        if u['kind'] not in OPTS: raise SheetError('unit %s: kind %r is not carried by the sheet (choice-type answers only)' % (u.get('no'), u['kind']))
        if u.get('opts', OPTS[u['kind']]) != OPTS[u['kind']]: raise SheetError('unit %s: %r is not the five alternatives %r' % (u['no'], u.get('opts'), OPTS[u['kind']]))
        if u['no'] in seen: raise SheetError('unit label %s occurs twice' % u['no'])
        seen.add(u['no'])


def unit_lines(n, pair): return math.ceil(n / (2 if pair else 1))


def block_h(n, pair): return 14 + unit_lines(n, pair) * ROWH + 17 + 8


def build_layout(spec, pair=True):
    check_units(spec['units'])
    blocks = []; cur = None; per = 2 if pair else 1
    for u in spec['units']:
        k = u['kind']; g = u.get('group')
        if cur is None or cur['kind'] != k or cur['group'] != g or len(cur['units']) >= BLOCK_MAX[k]:
            cur = {'kind': k, 'group': g, 'units': []}; blocks.append(cur)
        cur['units'].append(u)
    _, top = header_layout()
    placed = []; col, y = 0, top
    for bi, b in enumerate(blocks):
        h = block_h(len(b['units']), pair)
        if y + h > BOTTOM:
            col += 1; y = top
            if col >= 2: raise SheetOverflow('the page is full: block %d (%s) does not fit; the blocks need more than two columns of %.0f pt' % (bi, b['kind'], BOTTOM - top))
        x0 = MARG + col * (COLW + COLGAP)
        pb = {'id': len(placed), 'kind': b['kind'], 'page': 0, 'col': col, 'x': x0, 'y': y, 'h': h, 'per_line': per, 'units': [], 'closure': []}
        yy0 = y + 14
        for ui, u in enumerate(b['units']):
            line_i, slot = divmod(ui, per); dx = slot * SLOT_DX
            yy = yy0 + line_i * ROWH; opts = OPTS[u['kind']]
            ud = {'no': u['no'], 'kind': u['kind'], 'slot': slot, 'dx': dx, 'label_x': x0 + dx + 20,
                  'rows': [{'cy': yy + ROWH / 2, 'opts': opts, 'cx': [x0 + dx + 26 + i * PITCH + BR for i in range(len(opts))]}]}
            pb['units'].append(ud)
        cy = yy0 + unit_lines(len(b['units']), pair) * ROWH + 8.5; cx = x0 + 62
        for ud in pb['units']:
            pb['closure'].append({'no': ud['no'], 'cx': cx + BR, 'cy': cy}); cx += 38
        placed.append(pb); y += h
    fid = []
    for name, (cx, cy) in {'TL': (FID_IN, FID_IN), 'TR': (PW - FID_IN, FID_IN), 'BL': (FID_IN, PH - FID_IN), 'BR': (PW - FID_IN, PH - FID_IN)}.items():
        sx = 1 if cx < PW / 2 else -1; sy = 1 if cy < PH / 2 else -1
        fid.append({'page': 0, 'name': name, 'corner': (cx, cy), 'sx': sx, 'sy': sy, 'center': (cx + sx * FID_LEG / 2, cy + sy * FID_LEG / 2)})
    return {'version': VERSION, 'page_pt': [PW, PH], 'pages': 1, 'reader_pages': [0], 'bubble_r': BR, 'form_code': spec['form_code'], 'spec': spec, 'blocks': placed, 'lines': [],
            'fiducials': fid, 'free_height_pt': {'page_columns': 2 * (BOTTOM - top), 'page_used': sum(block_h(len(b['units']), pair) for b in blocks)}}


def render(layout, path):
    c = canvas.Canvas(path, pagesize=(PW, PH), invariant=1); c.setTitle('SEN0401 answer sheet v%s' % VERSION); c.setAuthor('')
    c.setStrokeColorRGB(0, 0, 0); c.setFillColorRGB(0, 0, 0)
    Y = lambda y: PH - y
    spec = layout['spec']
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
    c.setFont('Sans', FS); c.drawCentredString(PW / 2, Y(PH - MARG - 2), 'page 1 of 1 - answers')
    for b in layout['blocks']:
        x0, y0 = b['x'], b['y']
        c.setLineWidth(0.5); c.line(x0, Y(y0 + 1), x0 + COLW, Y(y0 + 1))
        for slot in range(b['per_line']):
            us = [u for u in b['units'] if u['slot'] == slot]
            if not us: continue
            r0 = us[0]['rows'][0]
            for ch, cx in zip(r0['opts'], r0['cx']): c.setFont('Sans', FS); c.drawCentredString(cx, Y(y0 + 11), ch)
        for u in b['units']:
            row = u['rows'][0]; cy = row['cy']; c.setFont('Sans', FS)
            c.drawRightString(u['label_x'], Y(cy + 3.5), u['no'])
            for cx in row['cx']: c.circle(cx, Y(cy), BR, stroke=1, fill=0)
        cl = b['closure']; cy = cl[0]['cy']
        c.setFont('Sans', FS); c.drawString(x0, Y(cy + 3.5), 'left blank:')
        for q in cl:
            c.circle(q['cx'], Y(q['cy']), BR, stroke=1, fill=0); c.drawString(q['cx'] + BR + 3, Y(q['cy'] + 3.5), q['no'])
    c.showPage(); c.save()


def write_pair(layout, outdir, stem):
    pdf = os.path.join(outdir, stem + '.pdf'); js = os.path.join(outdir, stem + '_layout.json')
    render(layout, pdf); json.dump(layout, open(js, 'w'), indent=1)
    return pdf, js
