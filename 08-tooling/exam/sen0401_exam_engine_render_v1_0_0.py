"""Print-safe renderer and answer key of the SEN0401 exam engine, version 1.0.0.
White page, black ink, thin lines only, no fill and no colour; 10 point text, 9 point code (never wrapped); circle-the-letter answer mode; two columns on A4.
render(paper, path) -> page count (counted with pdfinfo); answer_key(paper) -> dict (the grader's key; contains no student data)."""
import subprocess, sys, os
sys.dont_write_bytecode = True
from xml.sax.saxutils import escape
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle, KeepTogether, CondPageBreak
import sen0401_exam_pagesave_measure_v1_0_0 as M  # registers the DejaVu fonts


def render(paper, path):
    P = paper['params']; W, H = A4; m = 15 * mm; cols = P['columns']; gap = 8 * mm; cw = (W - 2 * m - (cols - 1) * gap) / cols
    fs = P['font']; cfs = P['code_font']
    st = ParagraphStyle('q', fontName='Sans', fontSize=fs, leading=fs * 1.25, spaceAfter=2)
    so = ParagraphStyle('o', parent=st, leftIndent=14, firstLineIndent=-14, spaceAfter=0)
    sb = ParagraphStyle('b', parent=st, fontName='SansB'); sc = ParagraphStyle('c', fontName='Mono', fontSize=cfs, leading=cfs * 1.2)
    hh = 26 * mm
    frames = [Frame(m + k * (cw + gap), m, cw, H - 2 * m, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id='f%d' % k) for k in range(cols)]
    first = [Frame(m + k * (cw + gap), m, cw, H - 2 * m - hh, leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0) for k in range(cols)]
    def foot(c, d):
        c.setFont('Sans', 8); c.setFillColorRGB(0, 0, 0); c.drawCentredString(W / 2, 8 * mm, 'SEN0401 %s v%d  -  page %d' % (paper['kind'], paper['version'], d.page))
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=m, rightMargin=m, topMargin=m, bottomMargin=m, pageCompression=0)
    doc.addPageTemplates([PageTemplate(id='first', frames=first, onPage=foot, autoNextPageTemplate='rest'), PageTemplate(id='rest', frames=frames, onPage=foot)])
    story = []
    title = 'SEN0401 Special Topics: Blockchain - %s exam (version %d)' % ('Midterm' if paper['kind'] == 'midterm' else 'Make-up', paper['version'])
    story += [Paragraph(escape(title), sb), Paragraph(escape('Chapters %s. %d minutes. Circle the letter of ONE answer unless the item says otherwise. Name: ____________  Number: ________' %
                                                           (', '.join(map(str, paper['chapters'])), P['sitting'])), st), Spacer(1, 4 * mm)]
    esc = lambda t: escape(t).replace('\n', '<br/>')
    def code_block(code):
        t = Table([[Preformatted(code, sc)]], colWidths=[cw]); t.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, (0, 0, 0)), ('LEFTPADDING', (0, 0), (-1, -1), 3), ('TOPPADDING', (0, 0), (-1, -1), 2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
        return t
    for it in paper['items']:
        n = it['position']; t = it['type']; fl = []
        if t in ('ChoiceFour', 'ChoiceFourCode'):
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st))
            if it.get('code'): fl.append(code_block(it['code'])); fl.append(Spacer(1, 1.5 * mm))
            for k, o in enumerate(it['options']): fl.append(Paragraph('<b>%s.</b> %s' % ('ABCD'[k], esc(o)), so))
        elif t == 'Matching':
            fl.append(Paragraph('<b>%d.</b> Match each statement to its answer. Write the answer letter in the box. Two answers are not used.' % n, st))
            rows = [['[   ]', Paragraph(esc('%d) %s' % (k + 1, p['text'])), st)] for k, p in enumerate(it['premises'])]
            tb = Table(rows, colWidths=[11 * mm, cw - 11 * mm]); tb.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('FONTNAME', (0, 0), (0, -1), 'Sans'), ('FONTSIZE', (0, 0), (0, -1), fs)]))
            fl.append(tb); fl.append(Spacer(1, 1.5 * mm))
            for k, r in enumerate(it['responses']): fl.append(Paragraph('<b>%s.</b> %s' % ('ABCDEFGH'[k], esc(r)), so))
        elif t == 'Ordering':
            fl.append(Paragraph('<b>%d.</b> Put the steps in the correct order. Write 1 for the first step, up to %d for the last, in the box.' % (n, len(it['steps'])), st))
            for k in it['display_order']: fl.append(Paragraph('[   ]  %s' % esc(it['steps'][k]), so))
        elif t == 'FillBlankGroup':
            ents = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']
            fl.append(Paragraph('<b>%d-%d.</b> Fill each blank with the NUMBER of the matching entry of the bank. Entries are used once; some are not used.' % (n, n + len(it['blanks']) - 1), st))
            cells = sorted(range(len(ents)), key=lambda k: order.index(k))
            rows = [[Paragraph('<b>%d</b> %s' % (order.index(k) + 1, esc(ents[k])), st) for k in cells[j:j + 2]] + [''] * (2 - len(cells[j:j + 2])) for j in range(0, len(cells), 2)]
            tb = Table(rows, colWidths=[cw / 2] * 2); tb.setStyle(TableStyle([('BOX', (0, 0), (-1, -1), 0.5, (0, 0, 0)), ('VALIGN', (0, 0), (-1, -1), 'TOP')])); fl.append(tb); fl.append(Spacer(1, 1.5 * mm))
            for b, bl in enumerate(it['blanks']): fl.append(Paragraph('<b>%d.</b> %s' % (n + b, esc(bl['text'])), st))
        elif t == 'NumericAnswer':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st)); fl.append(Paragraph('Answer: [__________]  %s' % esc(it['unit']), st))
        elif t == 'CodeTrace':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st)); fl.append(code_block(it['code'])); fl.append(Spacer(1, 1.5 * mm))
            fl.append(Paragraph('Printed result: ______________________', st))
        elif t == 'ShortAnswer':
            fl.append(Paragraph('<b>%d.</b> %s' % (n, esc(it['q'])), st))
            for _ in range(it['lines']): fl.append(Paragraph('_' * 52, st))
        story.append(KeepTogether(fl + [Spacer(1, 2.5 * mm)]))
    doc.build(story)
    out = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int([l for l in out.splitlines() if l.startswith('Pages:')][0].split()[1])


def answer_key(paper):
    key = dict(paper=paper['kind'], version=paper['version'], chapters=paper['chapters'], pages=paper.get('pageCount'), items=[], review_needed=[])
    for it in paper['items']:
        n = it['position']; t = it['type']; e = dict(position=n, type=t, chapters=it['chapters'], bloom=it['bloom'], kind=it['kind'], item_key=it['key'])
        if t in ('ChoiceFour', 'ChoiceFourCode'): e['answer'] = 'ABCD'[it['answer']]
        elif t == 'Matching': e['answer'] = {str(k + 1): 'ABCDEFGH'[it['responses'].index(p['match'])] for k, p in enumerate(it['premises'])}
        elif t == 'Ordering': e['answer'] = {it['steps'][k]: k + 1 for k in range(len(it['steps']))}; e['shown_order'] = it['display_order']
        elif t == 'FillBlankGroup':
            e['answer'] = {str(n + b): str(it['bank_order'].index(b) + 1) for b in range(len(it['blanks']))}
        elif t == 'NumericAnswer': e['answer'] = dict(value=it['key_value'], unit=it['unit'], tolerance=it['tolerance'])
        elif t == 'CodeTrace': e['answer'] = it['output']
        elif t == 'ShortAnswer': e['answer'] = it['rubric']
        if it.get('machine_assembled'): e['machine_assembled'] = True; key['review_needed'].append(n)
        key['items'].append(e)
    return key
