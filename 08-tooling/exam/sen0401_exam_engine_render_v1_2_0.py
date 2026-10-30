"""Print-safe renderer, answer key and answer-sheet specification of the SEN0401 exam engine, version 1.2.0 (new file; copy of v1.1.0 with the changes listed here; v1.0.0 and v1.1.0 stay as committed).
CHANGES against v1.1.0 (page-reduction and print-quality, found by reading the printed pages):
  1. The title block spans the full page width in its own frame; v1.1.0 put it in the left column and reserved a blank 26 mm band over BOTH columns of page 1.
  2. The answer sheet is drawn by a copy of the v1.0.0 sheet renderer in which rule 5 is split over two lines: in v1.0.0 rule 5 runs past the right margin and is cut at the page edge. Positions of every bubble and box are unchanged (same layout).
Same print rules as v1.0.0: white page, black ink, thin lines only, no fill and no colour; 10 point text, 9 point code (never wrapped); two columns on A4.
New in 1.1.0: the answer mode GridOnCover (the owner's decision: a separate bubble grid, one extra A4 page). In that mode the paper carries no answer boxes; every answer is a row of the
sheet (the sheet module of the answer-sheet task, imported unchanged), and the sheet pages are COUNTED in the page count of the paper (content pages + sheet pages).
  render(paper, path)        -> number of pages of the paper itself (pdfinfo)
  sheet_spec(paper)          -> the answer-sheet specification derived from the paper (one unit per answer place)
  render_sheet(paper, path)  -> (pages of the sheet, layout)
  answer_key(paper)          -> dict for the grader (no student data)"""
import json, os, subprocess, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle, KeepTogether, FrameBreak
import sen0401_exam_pagesave_measure_v1_0_0 as M  # registers the DejaVu fonts
import sen0401_exam_answersheet_v1_0_0 as A
import inspect

CHOICE = ('ChoiceFour', 'ChoiceFourCode')
GRID = 'GridOnCover'


def bank_code(position):
    """The two-digit code of a bank entry on the grid: its number (1 to 9) and the Damm check digit, so a slipped or swapped digit is caught by the reader."""
    return A.make_code(position, 1)


def bank_label(paper, position):
    return bank_code(position) if paper['params']['answer_mode'] == GRID else str(position)


def render(paper, path):
    P = paper['params']; W, H = A4; m = 15 * mm; cols = P['columns']; gap = 8 * mm; cw = (W - 2 * m - (cols - 1) * gap) / cols
    fs = P['font']; cfs = P['code_font']; grid = P['answer_mode'] == GRID
    st = ParagraphStyle('q', fontName='Sans', fontSize=fs, leading=fs * 1.25, spaceAfter=2)
    so = ParagraphStyle('o', parent=st, leftIndent=14, firstLineIndent=-14, spaceAfter=0)
    sb = ParagraphStyle('b', parent=st, fontName='SansB'); sc = ParagraphStyle('c', fontName='Mono', fontSize=cfs, leading=cfs * 1.2)
    hh = 22 * mm
    frames = [Frame(m + k * (cw + gap), m, cw, H - 2 * m, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f%d' % k) for k in range(cols)]
    head = Frame(m, H - m - hh, W - 2 * m, hh, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='head')
    first = [head] + [Frame(m + k * (cw + gap), m, cw, H - 2 * m - hh, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0) for k in range(cols)]
    def foot(c, d):
        c.setFont('Sans', 8); c.setFillColorRGB(0, 0, 0); c.drawCentredString(W / 2, 8 * mm, 'SEN0401 %s v%d  -  page %d' % (paper['kind'], paper['version'], d.page))
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=m, rightMargin=m, topMargin=m, bottomMargin=m, pageCompression=0)
    doc.addPageTemplates([PageTemplate(id='first', frames=first, onPage=foot, autoNextPageTemplate='rest'), PageTemplate(id='rest', frames=frames, onPage=foot)])
    story = []
    title = 'SEN0401 Special Topics: Blockchain - %s exam (version %d)' % ('Midterm' if paper['kind'] == 'midterm' else 'Make-up', paper['version'])
    how = ('Mark every answer on the separate answer sheet (the bubble grid); write nothing else on this paper that you want read. ONE answer per row unless the item says otherwise.' if grid
           else 'Circle the letter of ONE answer unless the item says otherwise. Name: ____________  Number: ________')
    story += [Paragraph(escape(title), sb), Paragraph(escape('Chapters %s. %d minutes. %s' % (', '.join(map(str, paper['chapters'])), P['sitting'], how)), st), FrameBreak()]
    esc = lambda t: escape(t).replace('\n', '<br/>')
    def code_block(code):
        t = Table([[Preformatted(code, sc)]], colWidths=[cw]); t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, (0, 0, 0)), ('LEFTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
        return t
    for it in paper['items']:
        n = it['position']; t = it['type']; fl = []
        if t in CHOICE:
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st))
            if it.get('code'): fl.append(code_block(it['code'])); fl.append(Spacer(1, 1.5 * mm))
            for k, o in enumerate(it['options']): fl.append(Paragraph('<b>%s.</b> %s' % ('ABCD'[k], esc(o)), so))
        elif t == 'Matching':
            if grid:
                fl.append(Paragraph('<b>%d.</b> Match each statement a) to %s) to its answer. On the answer sheet, in the rows %da to %s, fill the bubble of the answer letter. Two answers are not used.' %
                                    (n, 'abcdef'[len(it['premises']) - 1], n, '%d%s' % (n, 'abcdef'[len(it['premises']) - 1])), st))
                rows = [['', Paragraph(esc('%s) %s' % ('abcdef'[k], p['text'])), st)] for k, p in enumerate(it['premises'])]
                tb = Table(rows, colWidths=[2 * mm, cw - 2 * mm])
            else:
                fl.append(Paragraph('<b>%d.</b> Match each statement to its answer. Write the answer letter in the box. Two answers are not used.' % n, st))
                rows = [['[   ]', Paragraph(esc('%d) %s' % (k + 1, p['text'])), st)] for k, p in enumerate(it['premises'])]
                tb = Table(rows, colWidths=[11 * mm, cw - 11 * mm])
            tb.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('FONTNAME', (0, 0), (0, -1), 'Sans'), ('FONTSIZE', (0, 0), (0, -1), fs)]))
            fl.append(tb); fl.append(Spacer(1, 1.5 * mm))
            for k, r in enumerate(it['responses']): fl.append(Paragraph('<b>%s.</b> %s' % ('ABCDEFGH'[k], esc(r)), so))
        elif t == 'Ordering':
            if grid:
                fl.append(Paragraph('<b>%d.</b> Put the steps in the correct order. On the answer sheet, in the rows %da to %s, fill the bubble of the place (1 = first, %d = last) of each step.' %
                                    (n, n, '%d%s' % (n, 'abcdef'[len(it['steps']) - 1]), len(it['steps'])), st))
                for j, k in enumerate(it['display_order']): fl.append(Paragraph('<b>%s)</b>  %s' % ('abcdef'[j], esc(it['steps'][k])), so))
            else:
                fl.append(Paragraph('<b>%d.</b> Put the steps in the correct order. Write 1 for the first step, up to %d for the last, in the box.' % (n, len(it['steps'])), st))
                for k in it['display_order']: fl.append(Paragraph('[   ]  %s' % esc(it['steps'][k]), so))
        elif t == 'FillBlankGroup':
            ents = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']
            if grid:
                fl.append(Paragraph('<b>%d-%d.</b> Fill each blank with the CODE (two digits) of the matching entry of the bank. On the answer sheet fill one bubble in each of the two rows of the blank. Entries are used once; some are not used.' %
                                    (n, n + len(it['blanks']) - 1), st))
            else:
                fl.append(Paragraph('<b>%d-%d.</b> Fill each blank with the NUMBER of the matching entry of the bank. Entries are used once; some are not used.' % (n, n + len(it['blanks']) - 1), st))
            cells = sorted(range(len(ents)), key=lambda k: order.index(k))
            rows = [[Paragraph('<b>%s</b> %s' % (bank_label(paper, order.index(k) + 1), esc(ents[k])), st) for k in cells[j:j + 2]] + [''] * (2 - len(cells[j:j + 2])) for j in range(0, len(cells), 2)]
            tb = Table(rows, colWidths=[cw / 2] * 2); tb.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, (0, 0, 0)), ('VALIGN', (0, 0), (-1, -1), 'TOP')])); fl.append(tb); fl.append(Spacer(1, 1.5 * mm))
            for b, bl in enumerate(it['blanks']): fl.append(Paragraph('<b>%d.</b> %s' % (n + b, esc(bl['text'])), st))
        elif t == 'NumericAnswer':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st))
            fl.append(Paragraph(('Write the result on the answer sheet (row %d), one digit per box.  Unit: %s' % (n, esc(it['unit']))) if grid else 'Answer: [__________]  %s' % esc(it['unit']), st))
        elif t == 'CodeTrace':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st)); fl.append(code_block(it['code'])); fl.append(Spacer(1, 1.5 * mm))
            fl.append(Paragraph(('Write the printed result on the answer sheet (row %d), one digit per box.' % n) if grid else 'Printed result: ______________________', st))
        elif t == 'ShortAnswer':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st))
            for _ in range(it['lines']): fl.append(Paragraph('_' * 52, st))
        story.append(KeepTogether(fl + [Spacer(1, 2.5 * mm)]))
    doc.build(story)
    out = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int([l for l in out.splitlines() if l.startswith('Pages:')][0].split()[1])


def sheet_spec(paper):
    """One unit (a row, or a row pair, or a box) for every answer place of the paper."""
    units = []
    for it in paper['items']:
        n = it['position']; t = it['type']
        if t in CHOICE: units.append({'no': str(n), 'kind': 'choice', 'opts': 'ABCD'})
        elif t == 'Matching':
            for k in range(len(it['premises'])): units.append({'no': '%d%s' % (n, 'abcdef'[k]), 'kind': 'match', 'opts': 'ABCDEFGH'[:len(it['responses'])]})
        elif t == 'Ordering':
            for k in range(len(it['steps'])): units.append({'no': '%d%s' % (n, 'abcdef'[k]), 'kind': 'order', 'opts': '123456'[:len(it['steps'])]})
        elif t == 'FillBlankGroup':
            for b in range(len(it['blanks'])): units.append({'no': str(n + b), 'kind': 'bank', 'digits': 2})
        elif t in ('NumericAnswer', 'CodeTrace'): units.append({'no': str(n), 'kind': 'human', 'cells': 5})
        elif t == 'ShortAnswer': pass  # written on the paper itself
    kind = 'Midterm' if paper['kind'] == 'midterm' else 'MakeUp'
    return {'paper_kind': kind, 'paper_version': paper['version'], 'form_code': A.make_code(1000 + paper['version'] * 10 + (0 if kind == 'Midterm' else 1), 4), 'units': units}


def _sheet_render():
    src = inspect.getsource(A.render)
    old = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below. Numbers go in the boxes, one digit per box.',"
    new = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below.',\n                     '    Numbers go in the boxes, one digit per box.',"
    assert src.count(old) == 1
    ns = dict(A.__dict__); exec(src.replace(old, new), ns); return ns['render']


def render_sheet(paper, path):
    layout = A.build_layout(sheet_spec(paper)); _sheet_render()(layout, path)
    out = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int([l for l in out.splitlines() if l.startswith('Pages:')][0].split()[1]), layout


def answer_key(paper):
    grid = paper['params']['answer_mode'] == GRID
    key = dict(paper=paper['kind'], version=paper['version'], chapters=paper['chapters'], pages=paper.get('pageCount'), content_pages=paper.get('contentPages'), sheet_pages=paper.get('sheetPages'),
               answer_mode=paper['params']['answer_mode'], items=[], review_needed=[])
    for it in paper['items']:
        n = it['position']; t = it['type']; e = dict(position=n, type=t, chapters=it['chapters'], bloom=it['bloom'], kind=it['kind'], item_key=it['key'], seeds=it.get('seeds', []), critical_points=it.get('critical_points', []))
        if t in CHOICE: e['answer'] = 'ABCD'[it['answer']]
        elif t == 'Matching':
            e['answer'] = ({'%d%s' % (n, 'abcdef'[k]): 'ABCDEFGH'[it['responses'].index(p['match'])] for k, p in enumerate(it['premises'])} if grid
                           else {str(k + 1): 'ABCDEFGH'[it['responses'].index(p['match'])] for k, p in enumerate(it['premises'])})
        elif t == 'Ordering':
            if grid: e['answer'] = {'%d%s' % (n, 'abcdef'[j]): it['display_order'][j] + 1 for j in range(len(it['steps']))}   # the place of the step printed at label j
            else: e['answer'] = {it['steps'][k]: k + 1 for k in range(len(it['steps']))}
            e['shown_order'] = it['display_order']
        elif t == 'FillBlankGroup': e['answer'] = {str(n + b): (bank_label(paper, it['bank_order'].index(b) + 1)) for b in range(len(it['blanks']))}
        elif t == 'NumericAnswer': e['answer'] = dict(value=it['key_value'], unit=it['unit'], tolerance=it['tolerance'])
        elif t == 'CodeTrace': e['answer'] = it['output']
        elif t == 'ShortAnswer': e['answer'] = it['rubric']
        key['items'].append(e)
    return key
