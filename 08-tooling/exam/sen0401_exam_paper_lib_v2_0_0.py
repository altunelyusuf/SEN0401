"""SEN0401 midterm paper library, version 2.0.0 (new file; the engine v1.1.0, the renderer v1.2.0 and the sheet modules are imported unchanged and never edited).
What it does
  make_form(...)      the midterm paper of ONE form from the authored items: all items of the chapter list, a seeded mixed order (rule below), letters balanced, bank/ordering/matching shuffles by the form seed
  item_blocks(...)    the printable content of one item as a list of paragraph specifications (shared by the Word writer and the measuring document)
  write_docx(...)     the paper as a Word (.docx) file: A4, 10 mm side margins, two columns of fixed width, Arial 10 pt / Courier New 8 pt, exact line spacing, explicit column breaks
  write_key_docx(...) the answer key as a Word file
  export_pdf(...)     PDF export with LibreOffice (own profile folder so that parallel sessions do not collide)
  measure_pdf(...)    per page and column: lowest text line, free space; code boxes; font sizes (from the PDF itself, with pdfplumber)
THE MIXED ORDER (one rule): the items are shuffled by random.Random(form seed); a draw is kept only when (a) the first item is of Bloom level 2 or lower (low difficulty), (b) no item stands next to itself
  (the two blanks of a fill-in group are ONE printed block and stay together: the only exemption), (c) no two neighbouring items are of the same item type, (d) a layout test: with the measured item heights the six columns (3 pages x 2) can be filled in this order with every column keeping the planned free share. Draws are counted and recorded.
THE FORM CODE (one rule): serial = four digits  V K F F  (V = paper version 1-9, K = 0 midterm / 1 make-up, FF = form number 01 = A, 02 = B ...), then the Damm check digit of the sheet module: five digits, e.g. 20011.
Print rules kept: white page, black ink, no fill, text 10 pt or larger, code 8 pt or larger and never wrapped, one or two columns."""
import json, os, random, re, subprocess, sys, shutil, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_render_v1_2_0 as R
import sen0401_exam_answersheet_v1_0_0 as A
from sen0401_exam_engine_v1_1_0 import units, CHOICE
from docx import Document
from docx.shared import Pt, Mm, Twips
from docx.enum.text import WD_BREAK, WD_LINE_SPACING
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

VERSION = '2.0.0'
FONT, MONO = 'Arial', 'Courier New'                       # Word names; LibreOffice substitutes the metric-compatible Liberation Sans / Liberation Mono
TXT, CODE = 10, 8                                         # point sizes (rule R01: text >= 10, code >= 8)
LEAD, CLEAD = 11.5, 9.6                                   # exact line spacing, points
GAP_AFTER = 4.0                                           # points between two items (explicit, never automatic)
SIDE, TOP, BOTTOM, FOOTER_DIST = 10.0, 10.0, 14.0, 4.0    # millimetres
COLGAP = 6.0                                              # millimetres
A4W, A4H = 210.0, 297.0
COLW = (A4W - 2 * SIDE - COLGAP) / 2                      # 92 mm
COLW_TW = int(round((A4W - 2 * SIDE - COLGAP) / 2 * 56.6929))   # twips (1 mm = 56.6929 twips)
GAP_TW = int(round(COLGAP * 56.6929))
KIND_ORDER = ['choice', 'match', 'order', 'bank', 'human']
TYPE_KIND = {'ChoiceFour': 'choice', 'ChoiceFourCode': 'choice', 'Matching': 'match', 'Ordering': 'order', 'FillBlankGroup': 'bank', 'NumericAnswer': 'human', 'CodeTrace': 'human'}


# ------------------------------------------------------------------ form code and mixed order
def form_code(version, kind, form_no):
    """Four-digit serial V K FF plus the Damm check digit of the answer-sheet module (valid for the sheet's check)."""
    return A.make_code('%d%d%02d' % (version, 0 if kind == 'midterm' else 1, form_no), 4)


def mixed_order(items, seed, accept=None):
    """Seeded permutation with the stated constraints. accept(order) is an optional layout test (the six-column packing). Returns (ordered list, number of draws)."""
    rnd = random.Random(seed * 13 + 5)
    for draw in range(1, 300001):
        o = items[:]; rnd.shuffle(o)
        if o[0]['bloom'] > 2: continue
        if any(o[k]['key'] == o[k + 1]['key'] or o[k]['type'] == o[k + 1]['type'] for k in range(len(o) - 1)): continue
        if accept is not None and not accept(o): continue
        return o, draw
    raise RuntimeError('no mixed order satisfies the constraints')


def make_form(items_path, chapters, seed, form_no, version=2, nitems=24, kind='midterm', accept=None):
    M = E.M
    P = E.Params(nitems, M.parse_ch(chapters), None, 'GridOnCover', synthesis_min=0, higher_from=3, indirect_enabled=False, seed=seed, sitting=60, columns=2, code_cap=45,
                 page_limit=None, enable=[], allow_repeat=False, authored=items_path, order='mixed', code_font=CODE)
    rnd = random.Random(seed * 7)
    auth, skipped = E.load_authored(items_path, P.chapters)
    pages, pkey = E.pages_for(P.chapters)
    pool = [i for i in auth if kind in i['papers']]
    picks, q = E.select(P, kind, pool, rnd)
    allit = [dict(i) for i in picks]
    for i in allit:
        i['matches'] = E.check_copies(i, pages); i['checked_against'] = len(pages)
    allit.sort(key=lambda i: (i['primary'], i['key']))                      # a fixed base order, so that the shuffle below is the only source of order
    allit, draws = mixed_order(allit, seed, accept)
    E.balance_letters([i for i in allit if i['type'] in CHOICE], rnd)
    pos = 0
    for i in allit:
        pos += 1; i['position'] = pos
        if i['type'] == 'FillBlankGroup':
            r = random.Random(seed * 31 + i['position']); nt = len(i['blanks']) + len(i['distractors'])
            for _ in range(200):
                o = list(range(nt)); r.shuffle(o)
                ap = [o.index(k) for k in range(len(i['blanks']))]
                if any(ap[a] > ap[b] for a in range(len(ap)) for b in range(a + 1, len(ap))): break
            i['bank_order'] = o; pos += len(i['blanks']) - 1
        if i['type'] == 'Ordering': i['display_order'] = E.order_of_steps(i['position'], len(i['steps']), seed)
        if i['type'] == 'Matching':
            i['responses'] = list(i['responses']); random.Random(seed * 17 + i['position']).shuffle(i['responses'])
    code = form_code(version, kind, form_no)
    return dict(kind=kind, version=version, previous=version - 1, chapters=list(P.chapters), quotas=q, params=P.snapshot(), items=allit, pool_size=len(pool), skipped=skipped,
                page_chapters=list(pkey), page_items=len(pages), form=dict(letter='ABCDEFGH'[form_no - 1], number=form_no, seed=seed, code=code, order_draws=draws,
                                                                          order_rule='shuffle by random.Random(seed*13+5); first item Bloom<=2; no item next to itself; no two neighbours of one item type; and (layout test) the six columns of 3 pages keep the stated free share')), P


# ------------------------------------------------------------------ content of the items
def item_blocks(it, paper):
    """List of paragraphs: dict(k=kind, runs=[(text, bold)], keep=bool). kinds: q (question line), opt (hanging lettered line), code, bank (boxed bank line), note."""
    n = it['position']; t = it['type']; B = []
    def q(runs): B.append(dict(k='q', runs=runs))
    def opt(label, text): B.append(dict(k='opt', runs=[(label, True), ('\t' + text, False)]))
    if t in CHOICE:
        q([('%d. ' % n, True), (it['q'], False)])
        if it.get('code'): B.append(dict(k='code', text=it['code']))
        for k, o in enumerate(it['options']): opt('ABCD'[k] + '.', o)
    elif t == 'Matching':
        last = 'abcdef'[len(it['premises']) - 1]
        q([('%d. ' % n, True), ('Match statements a) to %s) with the answers: sheet rows %da to %s%s, fill the answer letter. Two answers stay unused.' % (last, n, n, last), False)])
        for k, p in enumerate(it['premises']): opt('abcdef'[k] + ')', p['text'])
        for k, r in enumerate(it['responses']): opt('ABCDEFGH'[k] + '.', r)
    elif t == 'Ordering':
        last = 'abcdef'[len(it['steps']) - 1]
        q([('%d. ' % n, True), ('Put the steps in order: sheet rows %da to %s%s, fill the place (1 = first, %d = last) of each step.' % (n, n, last, len(it['steps'])), False)])
        for j, k in enumerate(it['display_order']): opt('abcdef'[j] + ')', it['steps'][k])
    elif t == 'FillBlankGroup':
        ents = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']
        q([('%d-%d. ' % (n, n + len(it['blanks']) - 1), True), ('Fill each blank with the two-digit CODE of the matching bank entry (sheet rows %d to %d). Each entry is used once; some stay unused.' % (n, n + len(it['blanks']) - 1), False)])
        cells = sorted(range(len(ents)), key=lambda k: order.index(k))
        for j in range(0, len(cells), 2):
            row = []
            for k in cells[j:j + 2]: row += [(R.bank_label(paper, order.index(k) + 1) + ' ', True), (ents[k], False), ('\t', False)]
            B.append(dict(k='bank', runs=row[:-1]))
        for b, bl in enumerate(it['blanks']): q([('%d. ' % (n + b), True), (bl['text'], False)])
    elif t == 'NumericAnswer':
        q([('%d. ' % n, True), (it['q'], False)])
        B.append(dict(k='q', runs=[('Sheet row %d, one digit per box. Unit: %s.' % (n, it['unit']), False)]))
    elif t == 'CodeTrace':
        q([('%d. ' % n, True), (it['q'], False)]); B.append(dict(k='code', text=it['code']))
        B.append(dict(k='q', runs=[('Printed result: sheet row %d, one digit per box.' % n, False)]))
    else: raise ValueError(t)
    return B


# ------------------------------------------------------------------ Word writer
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items(): e.set(qn(k.replace('_', ':', 1)), str(v))
    return e


def _set_fonts(run_or_style_rpr, name):
    rpr = run_or_style_rpr
    rf = rpr.find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'): rf.set(qn(a), name)


def _font(run, name, size, bold=False):
    run.font.name = name; run.font.size = Pt(size); run.font.bold = bold
    _set_fonts(run._r.get_or_add_rPr(), name)


def _fmt(p, lead, after=0.0, left=0.0, first=0.0, keep_next=False, tabs=()):
    f = p.paragraph_format
    f.space_before = Pt(0); f.space_after = Pt(after); f.line_spacing_rule = WD_LINE_SPACING.EXACTLY; f.line_spacing = Pt(lead)
    f.left_indent = Pt(left); f.first_line_indent = Pt(first); f.keep_together = True; f.keep_with_next = keep_next; f.widow_control = False
    for tpos in tabs: f.tab_stops.add_tab_stop(Pt(tpos))


def _border(p, space=2, indent_pt=None):
    ppr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr')
    for side in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + side); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), str(space)); e.set(qn('w:color'), '000000'); b.append(e)
    _insert_ppr(ppr, b)


PPR_AFTER_BDR = ('w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap', 'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd',
                 'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange')


def _insert_ppr(ppr, el, after=PPR_AFTER_BDR):
    """Insert a pPr child before the first existing child that the schema orders after it (Word is strict about the order)."""
    for ch in ppr:
        if ch.tag in [qn(t) for t in after]: ch.addprevious(el); return
    ppr.append(el)


def _setup_doc(doc, title_cols):
    st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(TXT); _set_fonts(st.element.get_or_add_rPr(), FONT)
    pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(0)
    # document language, no automatic hyphenation
    settings = doc.settings.element
    for tag in ('w:autoHyphenation',):
        e = settings.find(qn(tag))
        if e is not None: settings.remove(e)
    for cs in settings.iter(qn('w:compatSetting')):
        if cs.get(qn('w:name')) == 'compatibilityMode': cs.set(qn('w:val'), '15')          # Word 2013 and later layout; no compatibility-mode banner
    s = doc.sections[0]
    s.page_width, s.page_height = Mm(A4W), Mm(A4H)
    s.left_margin = s.right_margin = Mm(SIDE); s.top_margin = Mm(TOP); s.bottom_margin = Mm(BOTTOM); s.footer_distance = Mm(FOOTER_DIST); s.header_distance = Mm(4)
    return s


def _cols(section, n):
    sp = section._sectPr
    for c in sp.findall(qn('w:cols')): sp.remove(c)
    c = OxmlElement('w:cols'); c.set(qn('w:num'), str(n))
    if n == 2:
        c.set(qn('w:equalWidth'), '0'); c.set(qn('w:space'), str(GAP_TW))
        for _ in range(2):
            e = OxmlElement('w:col'); e.set(qn('w:w'), str(COLW_TW)); e.set(qn('w:space'), str(GAP_TW)); c.append(e)
        c[-1].attrib.pop(qn('w:space'))
    else:
        c.set(qn('w:space'), '0')
    # w:cols must come before w:docGrid / after w:pgMar: insert after pgMar
    pg = sp.find(qn('w:pgMar')); pg.addnext(c)


def _footer(section, text_left):
    f = section.footer; f.is_linked_to_previous = False
    p = f.paragraphs[0]; p.text = ''
    _fmt(p, LEAD)
    r = p.add_run(text_left + '  -  page '); _font(r, FONT, TXT)
    for instr in ('PAGE',):
        r2 = p.add_run(); _font(r2, FONT, TXT)
        for typ, txt in (('begin', None), (None, instr), ('end', None)):
            if typ: fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), typ); r2._r.append(fc)
            else: it_ = OxmlElement('w:instrText'); it_.set(qn('xml:space'), 'preserve'); it_.text = ' %s ' % txt; r2._r.append(it_)
    r3 = p.add_run(' of '); _font(r3, FONT, TXT)
    r4 = p.add_run(); _font(r4, FONT, TXT)
    for typ, txt in (('begin', None), (None, 'NUMPAGES'), ('end', None)):
        if typ: fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), typ); r4._r.append(fc)
        else: it_ = OxmlElement('w:instrText'); it_.set(qn('xml:space'), 'preserve'); it_.text = ' %s ' % txt; r4._r.append(it_)
    p.alignment = 1


def _emit(doc, blocks, last_gap=GAP_AFTER):
    """Write the paragraphs of one item; returns the first paragraph (to carry a column break)."""
    firstp = None; half = COLW / 25.4 * 72 / 2
    for bi, b in enumerate(blocks):
        last = bi == len(blocks) - 1; keep_next = not last; after = last_gap if last else 0.0
        p = doc.add_paragraph()
        if b['k'] == 'q':
            _fmt(p, LEAD, after, keep_next=keep_next)
            for txt, bold in b['runs']: _font(p.add_run(txt), FONT, TXT, bold)
        elif b['k'] == 'opt':
            _fmt(p, LEAD, after, left=14, first=-14, keep_next=keep_next, tabs=(14,))
            for txt, bold in b['runs']: _font(p.add_run(txt), FONT, TXT, bold)
        elif b['k'] == 'bank':
            _fmt(p, LEAD, 0.0, keep_next=keep_next, tabs=(half,)); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(3); p.paragraph_format.right_indent = Pt(3)
            for txt, bold in b['runs']: _font(p.add_run(txt), FONT, TXT, bold)
            if last: p.paragraph_format.space_after = Pt(after)
        elif b['k'] == 'code':
            _fmt(p, CLEAD, 3.0, keep_next=keep_next); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(4); p.paragraph_format.right_indent = Pt(4)
            r = p.add_run(b['text']); _font(r, MONO, CODE)
        if firstp is None: firstp = p
        # the paragraph before a code box or a bank gets a little air through the box's own space; nothing automatic
    return firstp


def _column_break_para(doc):
    p = doc.add_paragraph(); _fmt(p, 1.0)
    r = p.add_run(); _font(r, FONT, 1); r.add_break(WD_BREAK.COLUMN)
    return p


def write_docx(paper, path, breaks=(), per_item_break=False):
    """breaks: item positions (in paper['items']) that start a new column. per_item_break: a column break after EVERY item (the measuring document)."""
    doc = Document(); sec = _setup_doc(doc, 2)
    f = paper['form']; P = paper['params']
    _footer(sec, 'SEN0401 midterm v%d  -  Form %s  -  form code %s' % (paper['version'], f['letter'], f['code']))
    if not per_item_break:
        p = doc.add_paragraph(); _fmt(p, 14, 1.0, keep_next=True); _font(p.add_run('SEN0401 Special Topics: Blockchain - Midterm exam (version %d, Form %s)' % (paper['version'], f['letter'])), FONT, 12, True)
        p = doc.add_paragraph(); _fmt(p, LEAD, 0.0, keep_next=True)
        _font(p.add_run('Form code %s' % f['code']), FONT, TXT, True)
        _font(p.add_run(' (it must equal the form code printed on your answer sheet). Chapters %s. %d minutes. Mark every answer on the separate answer sheet (bubble grid); '
                        'ONE answer per row unless the item says otherwise.' % (', '.join(map(str, paper['chapters'])), P['sitting'])), FONT, TXT)
        s2 = doc.add_section(WD_SECTION.CONTINUOUS)
        sp = doc.paragraphs[-1]                       # the paragraph that carries the section break: one point high, so that it costs no line in Word either
        _fmt(sp, 1.0); mrk = OxmlElement('w:rPr'); sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '2'); mrk.append(sz); _insert_ppr(sp._p.get_or_add_pPr(), mrk, after=('w:sectPr', 'w:pPrChange'))
    else:
        s2 = sec
    _cols(s2, 2)
    if not per_item_break: _cols(doc.sections[0], 1)
    first_of_col = set(breaks)
    for idx, it in enumerate(paper['items']):
        blocks = item_blocks(it, paper)
        if idx in first_of_col: _column_break_para(doc)
        _emit(doc, blocks)
        if per_item_break: _column_break_para(doc)
    doc.core_properties.author = ''; doc.core_properties.title = 'SEN0401 midterm v%d form %s' % (paper['version'], f['letter']); doc.core_properties.comments = ''
    doc.save(path)


def write_key_docx(paper, key, path, measure_note=''):
    doc = Document(); sec = _setup_doc(doc, 1); f = paper['form']
    sec.left_margin = sec.right_margin = Mm(15); sec.top_margin = Mm(12); sec.bottom_margin = Mm(14)
    _footer(sec, 'SEN0401 midterm v%d key  -  Form %s  -  form code %s' % (paper['version'], f['letter'], f['code']))
    p = doc.add_paragraph(); _fmt(p, 14, 2.0); _font(p.add_run('SEN0401 midterm v%d, Form %s - ANSWER KEY (for the grader, not for students)' % (paper['version'], f['letter'])), FONT, 12, True)
    p = doc.add_paragraph(); _fmt(p, LEAD, 3.0); _font(p.add_run('Form code %s. Seed %d. Chapters %s. Answer letters and numbers are the rows of the answer sheet; numbers keep the stated tolerance; traces are the printed text. %s' %
                                                              (f['code'], f['seed'], ', '.join(map(str, paper['chapters'])), measure_note)), FONT, TXT)
    for e in key['items']:
        a = e['answer']
        if isinstance(a, dict) and 'value' in a: s = 'value %s %s (tolerance %s)' % (a['value'], a['unit'], a['tolerance'])
        elif isinstance(a, dict): s = '   '.join('%s = %s' % (k, v) for k, v in a.items())
        else: s = str(a)
        p = doc.add_paragraph(); _fmt(p, LEAD, 2.0, left=26, first=-26, tabs=(26,))
        _font(p.add_run('%d' % e['position']), FONT, TXT, True); _font(p.add_run('\t%s   ch %s   Bloom %d   [%s]   ' % (e['type'], ','.join(map(str, e['chapters'])), e['bloom'], e['item_key'])), FONT, TXT)
        _font(p.add_run(s), FONT, TXT, True)
    doc.core_properties.author = ''; doc.save(path)


# ------------------------------------------------------------------ LibreOffice export and measurement
def export_pdf(docx_path, outdir, profile='/tmp/lo_profile_paperfix'):
    cmd = ['soffice', '-env:UserInstallation=file://' + profile, '--headless', '--convert-to', 'pdf', '--outdir', outdir, docx_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(docx_path))[0] + '.pdf')
    if not os.path.exists(pdf): raise RuntimeError('LibreOffice export failed: ' + r.stdout + r.stderr)
    return pdf


def pdf_pages(path):
    o = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', o).group(1))


def columns_of_pdf(pdf):
    """Per page and column (0/1): list of text lines [(top, bottom, x0, x1, text, fontname, size)] using pdfplumber; the footer line (below the frame) is dropped."""
    import pdfplumber
    out = []
    with pdfplumber.open(pdf) as d:
        for pi, pg in enumerate(d.pages):
            ws = pg.extract_words(extra_attrs=['fontname', 'size'], keep_blank_chars=False, use_text_flow=False)
            fy = pg.height - BOTTOM * 72 / 25.4
            cols = [[], []]
            for w in ws:
                if w['bottom'] > fy + 0.5: continue
                c = 0 if (w['x0'] + w['x1']) / 2 < pg.width / 2 else 1
                cols[c].append(w)
            out.append(cols)
    return out


# ------------------------------------------------------------------ the answer sheet: grouped by answer kind, one page, form code and form letter printed
def sheet_spec(paper):
    """The sheet units of the paper, grouped by answer kind (choice rows, matching rows, ordering rows, bank rows, written boxes), inside a kind in paper order. With 23 items in a mixed order
    a block per item does not fit one page (every block costs a header row and a closure row); grouped by kind the blocks are the same as in the type-ordered sheet of the paper v1 (1 page).
    Every row carries the item number at both ends, so the sheet needs no paper order."""
    spec = R.sheet_spec(paper); f = paper['form']
    order = {'choice': 0, 'match': 1, 'order': 2, 'bank': 3, 'human': 4}
    spec['units'] = sorted(spec['units'], key=lambda u: order[u['kind']])   # sorted() is stable: paper order is kept inside a kind
    spec['form_code'] = f['code']; spec['form_letter'] = f['letter']; spec['paper_version'] = paper['version']
    return spec


def _sheet_render_v3():
    src = __import__('inspect').getsource(A.render)
    old5 = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below. Numbers go in the boxes, one digit per box.',"
    new5 = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below.',\n                     '    Numbers go in the boxes, one digit per box.',"
    oldc = "'form code %s' % spec['form_code']"
    newc = "'Form %s   form code %s' % (spec.get('form_letter', '?'), spec['form_code'])"
    assert src.count(old5) == 1 and src.count(oldc) == 1
    ns = dict(A.__dict__); exec(src.replace(old5, new5).replace(oldc, newc), ns); return ns['render']


def render_sheet(paper, path):
    spec = sheet_spec(paper); layout = A.build_layout(spec); layout['form_code'] = paper['form']['code']; layout['form_letter'] = paper['form']['letter']
    _sheet_render_v3()(layout, path)
    return pdf_pages(path), layout


def sheet_pages_in_paper_order(paper):
    """Measured only (the reason for the grouping): the pages the sheet would need if its blocks followed the paper order."""
    spec = R.sheet_spec(paper); return A.build_layout(spec)['pages']
