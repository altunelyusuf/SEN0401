"""SEN0401 midterm paper library, version 3.0.0 (new file, derived from sen0401_exam_paper_lib_v2_0_0.py; the engine v1.1.0, renderer v1.2.0, answer-sheet v1.0.0 and the cover renderer v1.0.0 are imported unchanged).
What is new against v2.0.0 (the owner's rules of 2026-11-01 13:04, recorded in the structure file sen0401_exam_structure_v1_0_0.json):
  * page 1 is the cover page of the owner's template (cover renderer v1.0.0, function cover()); the question pages follow, then the answer sheet;
  * FIVE questions in the structure file's numbering: Q1 reading and choice, Q2 calculation and tracing, Q3 ordering and matching, Q4 fill in the sentence (25 points each, machine-read),
    Q5 short explanation (10-point bonus, written on lines of the paper, marked by hand, NOT on the answer sheet);
  * sub-questions are labelled 1a, 1b ... (the label is the row label of the answer sheet); the printed order of the sub-questions inside a question is the form's mixed order;
  * the points of every sub-question are printed with it; the tips of every term are part of the item text (items v1.2.0) and, for question 5, printed under the prompt;
  * the layout is a configuration (font size, line height, columns) so that the page budget can be MEASURED for several readability settings; nothing is shortened to fit.
Rows of the answer sheet (same block types as the sheet module: choice, match, order, bank, human, so the reader v1.2.0 reads them unchanged):
  choice '1a' ; human '2a' ; ordering '3a2' (sub-question a, step 2) ; matching '3b1' (sub-question b, statement 1) ; bank '4a' (blank a of question 4).
THE FORM CODE: V K F F + the Damm check digit of the sheet module (V = paper version, K = 0 midterm, FF = form number)."""
import json, os, random, re, subprocess, sys, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_engine_v1_1_0 as E
import sen0401_exam_engine_render_v1_2_0 as R
import sen0401_exam_answersheet_v1_0_0 as A
import sen0401_exam_cover_render_v1_0_0 as C
from sen0401_exam_engine_v1_1_0 import units, CHOICE
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

VERSION = '3.0.0'
STRUCTURE = os.path.join(HERE, 'sen0401_exam_structure_v1_0_0.json')
OUTCOMES = '/home/claude/sen0401/01-outcomes/sen0401_outcomes_v1_1_1.ttl'
FONT, MONO = 'Arial', 'Courier New'
A4W, A4H = 210.0, 297.0
TOP, BOTTOM, FOOTER_DIST = 10.0, 14.0, 4.0                  # millimetres
SLOT_KINDS = {'ChoiceFour': 'choice', 'ChoiceFourCode': 'choice', 'Matching': 'match', 'Ordering': 'order', 'FillBlankGroup': 'bank', 'NumericAnswer': 'human', 'CodeTrace': 'human'}

# ------------------------------------------------------------------ layout configurations (measured, never assumed)
CONFIGS = {
    'compact10':  dict(txt=10.0, lead=11.5, code=8.0, clead=9.6, cols=2, side=10.0, colgap=6.0, qline=17.0, head=11.0, gap=4.0),     # the size of paper v2
    'air10c':     dict(txt=10.0, lead=11.9, code=8.0, clead=9.8, cols=2, side=10.0, colgap=6.0, qline=18.0, head=11.5, gap=5.0),
    'air10b':     dict(txt=10.0, lead=12.2, code=8.0, clead=10.0, cols=2, side=10.0, colgap=6.0, qline=19.0, head=11.5, gap=6.0),
    'air10a':     dict(txt=10.0, lead=12.6, code=8.0, clead=10.2, cols=2, side=10.0, colgap=6.0, qline=20.0, head=12.0, gap=7.0),
    'read105':    dict(txt=10.5, lead=12.4, code=8.5, clead=10.2, cols=2, side=10.0, colgap=6.0, qline=19.0, head=11.5, gap=5.0),
    'read11':     dict(txt=11.0, lead=13.0, code=9.0, clead=10.8, cols=2, side=10.0, colgap=6.0, qline=20.0, head=12.0, gap=6.0),
    'single11':   dict(txt=11.0, lead=13.4, code=9.0, clead=11.0, cols=1, side=15.0, colgap=0.0, qline=21.0, head=12.5, gap=7.0),
}
CFG = dict(CONFIGS['compact10'])


def set_cfg(name):
    CFG.clear(); CFG.update(CONFIGS[name]); CFG['name'] = name


def geom():
    side, gap, n = CFG['side'], CFG['colgap'], CFG['cols']
    colw_mm = (A4W - 2 * side - (n - 1) * gap) / n
    return dict(colw_mm=colw_mm, colw_pt=colw_mm / 25.4 * 72, colw_tw=int(round(colw_mm * 56.6929)), gap_tw=int(round(gap * 56.6929)),
                frame_top=TOP / 25.4 * 72, frame_bottom=A4H / 25.4 * 72 - BOTTOM / 25.4 * 72)


# ------------------------------------------------------------------ form code, structure, forms
def form_code(version, kind, form_no):
    return A.make_code('%d%d%02d' % (version, 0 if kind == 'midterm' else 1, form_no), 4)


def load_structure(path=STRUCTURE):
    return json.load(open(path, encoding='utf8'))


def _slots(S, byk):
    """The slots of the paper in the structure's order: a slot is one printed sub-question (a fill-in group counts as ONE slot with its blanks)."""
    slots = []
    for q in S['questions']:
        qn_ = q['number']; seen = {}
        for sub in q['sub']:
            if q['number'] == 5:
                slots.append(dict(q=qn_, kind='explain', sub=[sub], points=sub['points'], chapters=list(sub['chapters']), bloom=None, type='ShortExplanation', skey=sub['key']))
                continue
            it = byk[sub['item']]
            if sub['type'] == 'FillBlankGroup' and sub['item'] in seen: seen[sub['item']]['sub'].append(sub); seen[sub['item']]['points'] += sub['points']; continue
            s = dict(q=qn_, kind=SLOT_KINDS[sub['type']], item=it, sub=[sub], points=sub['points'], chapters=list(it['chapters']), bloom=it['bloom'], type=sub['type'], skey=sub['key'])
            slots.append(s)
            if sub['type'] == 'FillBlankGroup': seen[sub['item']] = s
    return slots


def make_form(form_no, seed=5701, version=3, kind='midterm', accept=None, structure=None):
    """One form. Form 1 (A) keeps the structure file's order of the sub-questions (that order was drawn with seed_for_sub_question_order); the other forms draw their own
    order inside each question with random.Random(seed): neighbours are of different item type and of different primary chapter where the question allows it, and the order differs from form A's.
    accept(order_of_slots) is an optional layout test (the page packing)."""
    S = structure or load_structure(); chapters = S['chapters']
    path = os.path.join(HERE, S['items_file'])
    M = E.M
    P = E.Params(sum(units(i) for i in E.load_authored(path, M.parse_ch(','.join(map(str, chapters))))[0]), M.parse_ch(','.join(map(str, chapters))), None, 'GridOnCover', synthesis_min=0, higher_from=3,
                 indirect_enabled=False, seed=seed, sitting=60, columns=CFG['cols'], code_cap=45, page_limit=None, enable=[], allow_repeat=False, authored=path, order='mixed',
                 code_font=int(CFG['code']) if CFG['code'] == int(CFG['code']) else CFG['code'])
    auth, skipped = E.load_authored(path, P.chapters)
    byk = {i['key']: json.loads(json.dumps(i)) for i in auth}
    pages, pkey = E.pages_for(P.chapters)
    for i in byk.values():
        i['matches'] = E.check_copies(i, pages); i['checked_against'] = len(pages)
    base = _slots(S, byk)
    rnd = random.Random(seed * 13 + 5); draws = 1
    if form_no == 1 and (accept is None or accept(base)):
        order = base[:]
    else:
        order = None
        for draws in range(1, 200001):
            o = []
            for qn_ in range(1, 6):
                part = [s for s in base if s['q'] == qn_]; rnd.shuffle(part); o += part
            ok = (o != base) if form_no > 1 else True
            qs = {}
            for s in o: qs.setdefault(s['q'], []).append(s)
            for qn_, part in qs.items():
                cnt = {}
                for s in part: cnt[s['type']] = cnt.get(s['type'], 0) + 1
                kinds = cnt if max(cnt.values()) <= (len(part) + 1) // 2 and len(cnt) > 1 else {}      # the type rule applies only where it can be met
                for a, b in zip(part, part[1:]):
                    if kinds and a['type'] == b['type'] and draws < 150000: ok = False
                    if a['chapters'][0] == b['chapters'][0] and draws < 100000 and len({s['chapters'][0] for s in part}) > 1: ok = False
            if form_no > 1 and qs[1][0]['skey'] == [s for s in base if s['q'] == 1][0]['skey'] and draws < 50000: ok = False      # question 1 does not open with the same item as form A
            if ok and (accept is None or accept(o)): order = o; break
        if order is None: raise RuntimeError('no mixed order satisfies the constraints')
    # letters, positions, shuffles
    r2 = random.Random(seed * 7)
    for qn_ in range(1, 6):
        letters = iter('abcdefgh')
        for s in [s for s in order if s['q'] == qn_]:
            s['letters'] = [next(letters) for _ in s['sub']]; s['label'] = s['letters'][0]
    choice_slots = [s for s in order if s['kind'] == 'choice']
    E.balance_letters([s['item'] for s in choice_slots], r2)
    pos = 0; items = []
    for s in order:
        if s['kind'] == 'explain': s['position'] = None; continue
        it = s['item']; pos += 1; it['position'] = pos; s['position'] = pos; it['label'] = '%d%s' % (s['q'], s['label'])
        if it['type'] == 'FillBlankGroup':
            r = random.Random(seed * 31 + pos); nt = len(it['blanks']) + len(it['distractors'])
            for _ in range(200):
                o = list(range(nt)); r.shuffle(o)
                ap = [o.index(k) for k in range(len(it['blanks']))]
                if any(ap[a] > ap[b] for a in range(len(ap)) for b in range(a + 1, len(ap))): break
            it['bank_order'] = o; pos += len(it['blanks']) - 1
        if it['type'] == 'Ordering': it['display_order'] = E.order_of_steps(it['position'], len(it['steps']), seed)
        if it['type'] == 'Matching':
            it['responses'] = list(it['responses']); random.Random(seed * 17 + it['position']).shuffle(it['responses'])
        items.append(it)
    quotas = {c: sum(units(i) for i in items if i['primary'] == c) for c in P.chapters}
    code = form_code(version, kind, form_no)
    paper = dict(kind=kind, version=version, previous=version - 1, chapters=list(P.chapters), quotas=quotas, params=P.snapshot(), items=items, slots=order, pool_size=len(auth), skipped=skipped,
                 page_chapters=list(pkey), page_items=len(pages), structure=S,
                 form=dict(letter='ABCDEFGH'[form_no - 1], number=form_no, seed=seed, code=code, order_draws=draws,
                           order_rule=('form A: the sub-question order of the structure file (drawn with seed_for_sub_question_order %d)' % S['seed_for_sub_question_order']) if (form_no == 1 and draws == 1) else
                           'shuffle of the sub-questions inside each question by random.Random(seed*13+5); neighbours of different item type and primary chapter where possible; (forms after A) differs from form A and question 1 opens differently; and the layout test (the sub-questions pack into the planned columns with the planned free share)'))
    return paper


# ------------------------------------------------------------------ the printable content of one slot
def _pts(p):
    return ('%g' % p) if abs(p - round(p)) < 1e-9 else ('%.2f' % p).rstrip('0')


def question_instruction(qd):
    """The instruction of the structure file as the student reads it: the notes that are for the instructor (the open question about partial credit, the machine-read remark) are not printed."""
    t = qd['instruction']
    if qd['number'] == 3:
        a = 'Partial credit is a rule for the owner to fix (open question P1): the points of a part divide equally over its steps or pairs.'
        assert a in t; t = t.replace(a, 'The points of a part divide equally over its steps or pairs: every correct step or pair earns its share.')
    if qd['number'] == 5:
        a = 'BONUS, marked by hand, NOT read by the machine. '
        assert a in t; t = t.replace(a, 'Bonus question, marked by hand. ')
    return t


def heading_blocks(paper, qnum):
    qd = [q for q in paper['structure']['questions'] if q['number'] == qnum][0]
    return [dict(k='qh', runs=[('Question %d - %s (%d points%s)' % (qd['number'], qd['title'], qd['points'], ', bonus' if qd.get('bonus') else ''), True)]),
            dict(k='qi', runs=[(question_instruction(qd), False)])]


def slot_blocks(s, paper, first_of_question=False):
    """Paragraph specifications of one sub-question. kinds: qh (question heading), qi (question instruction), q, opt, code, bank, line, note."""
    B = []; S = paper['structure']; qd = [q for q in S['questions'] if q['number'] == s['q']][0]
    def q(runs, **kw): B.append(dict(k='q', runs=runs, **kw))
    def opt(label, text): B.append(dict(k='opt', runs=[(label, True), ('\t' + text, False)]))
    if first_of_question:
        B += heading_blocks(paper, s['q'])
    t = s['type']
    if s['kind'] == 'explain':
        sub = s['sub'][0]; lab = '%d%s' % (s['q'], s['label'])
        q([('%s. ' % lab, True), (sub['prompt'], False), ('  (%s points)' % _pts(sub['points']), False)], keep=True)
        tips = '; '.join('%s: %s' % (a, b) for a, b in sub['tips'])
        q([('Tips. ', True), (tips + '.', False)])
        for _ in range(sub['lines'] + 3): B.append(dict(k='line'))
        return B
    it = s['item']; n = it['label']; pts = s['points']
    if t in CHOICE:
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)])
        if it.get('code'): B.append(dict(k='code', text=it['code']))
        for k, o in enumerate(it['options']): opt('ABCD'[k] + '.', o)
    elif t == 'Matching':
        sub = s['sub'][0]; ppp = sub['points_per_part']; last = len(it['premises'])
        q([('%s. ' % n, True), (sub['instruction'], False), ('  (%s points; %s for each correct pair.) On the answer sheet, rows %s1 to %s%d: fill the letter of the answer.' % (_pts(pts), _pts(ppp), n, n, last), False)])
        for k, p in enumerate(it['premises']): opt('%d)' % (k + 1), p['text'])
        for k, r in enumerate(it['responses']): opt('ABCDEFGH'[k] + '.', r)
    elif t == 'Ordering':
        sub = s['sub'][0]; ppp = sub['points_per_part']; ns = len(it['steps'])
        q([('%s. ' % n, True), (sub['instruction'], False), ('  (%s points; %s for each step in the right place.) The steps are numbered 1) to %d) as printed. On the answer sheet, rows %s1 to %s%d: for each step fill the place (1 = first, %d = last) at which it happens.' % (_pts(pts), _pts(ppp), ns, n, n, ns, ns), False)])
        for j, k in enumerate(it['display_order']): opt('%d)' % (j + 1), it['steps'][k])
    elif t == 'FillBlankGroup':
        ents = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']; nb = len(it['blanks'])
        labs = ['%d%s' % (s['q'], l) for l in s['letters']]
        q([('%s-%s. ' % (labs[0], labs[-1]), True), ('Fill each blank with the two-digit CODE of the matching bank entry (sheet rows %s to %s). Each entry is used once; some stay unused.' % (labs[0], labs[-1]), False)], keep=True)
        cells = sorted(range(len(ents)), key=lambda k: order.index(k))
        for j in range(0, len(cells), 2):
            row = []
            for k in cells[j:j + 2]: row += [(R.bank_label(paper, order.index(k) + 1) + ' ', True), (ents[k], False), ('\t', False)]
            B.append(dict(k='bank', runs=row[:-1]))
        for b, bl in enumerate(it['blanks']): q([('%s. ' % labs[b], True), (bl['text'], False), ('  (%s points)' % _pts(s['sub'][b]['points']), False)])
    elif t == 'NumericAnswer':
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)])
        B.append(dict(k='q', runs=[('Sheet row %s, one digit per box. Unit: %s.' % (n, it['unit']), False)]))
    elif t == 'CodeTrace':
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)]); B.append(dict(k='code', text=it['code']))
        B.append(dict(k='q', runs=[('Printed result: sheet row %s, one digit per box.' % n, False)]))
    else: raise ValueError(t)
    return B


# ------------------------------------------------------------------ Word writer
def _set_fonts(rpr, name):
    rf = rpr.find(qn('w:rFonts'))
    if rf is None: rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'): rf.set(qn(a), name)


def _font(run, name, size, bold=False):
    run.font.name = name; run.font.size = Pt(size); run.font.bold = bold; _set_fonts(run._r.get_or_add_rPr(), name)


def _fmt(p, lead, after=0.0, left=0.0, first=0.0, keep_next=False, tabs=()):
    f = p.paragraph_format
    f.space_before = Pt(0); f.space_after = Pt(after); f.line_spacing_rule = WD_LINE_SPACING.EXACTLY; f.line_spacing = Pt(lead)
    f.left_indent = Pt(left); f.first_line_indent = Pt(first); f.keep_together = True; f.keep_with_next = keep_next; f.widow_control = False
    for tpos in tabs: f.tab_stops.add_tab_stop(Pt(tpos))


PPR_AFTER_BDR = ('w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap', 'w:overflowPunct', 'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd',
                 'w:snapToGrid', 'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc', 'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap',
                 'w:outlineLvl', 'w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange')


def _insert_ppr(ppr, el, after=PPR_AFTER_BDR):
    for ch in ppr:
        if ch.tag in [qn(t) for t in after]: ch.addprevious(el); return
    ppr.append(el)


def _border(p, space=2, sides=('top', 'left', 'bottom', 'right')):
    ppr = p._p.get_or_add_pPr(); b = OxmlElement('w:pBdr')
    for side in sides:
        e = OxmlElement('w:' + side); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), '4'); e.set(qn('w:space'), str(space)); e.set(qn('w:color'), '000000'); b.append(e)
    _insert_ppr(ppr, b)


def _cols(section, n):
    g = geom(); sp = section._sectPr
    for c in sp.findall(qn('w:cols')): sp.remove(c)
    c = OxmlElement('w:cols'); c.set(qn('w:num'), str(n))
    if n == 2:
        c.set(qn('w:equalWidth'), '0'); c.set(qn('w:space'), str(g['gap_tw']))
        for _ in range(2):
            e = OxmlElement('w:col'); e.set(qn('w:w'), str(g['colw_tw'])); e.set(qn('w:space'), str(g['gap_tw'])); c.append(e)
        c[-1].attrib.pop(qn('w:space'))
    else:
        c.set(qn('w:space'), '0')
    sp.find(qn('w:pgMar')).addnext(c)


def _page_setup(section, side):
    section.page_width, section.page_height = Mm(A4W), Mm(A4H)
    section.left_margin = section.right_margin = Mm(side); section.top_margin = Mm(TOP); section.bottom_margin = Mm(BOTTOM)
    section.footer_distance = Mm(FOOTER_DIST); section.header_distance = Mm(4)


def _field(p, instr):
    """A complex field in five runs (begin, instruction, separate, result, end), each with the font set, so that the result is not drawn in the document default font."""
    def run():
        r = p.add_run(); _font(r, FONT, CFG['txt']); return r
    r = run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'begin'); r._r.append(fc)
    r = run(); it_ = OxmlElement('w:instrText'); it_.set(qn('xml:space'), 'preserve'); it_.text = ' %s ' % instr; r._r.append(it_)
    r = run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'separate'); r._r.append(fc)
    r = run(); tt = OxmlElement('w:t'); tt.text = '1'; r._r.append(tt)
    r = run(); fc = OxmlElement('w:fldChar'); fc.set(qn('w:fldCharType'), 'end'); r._r.append(fc)


def _footer(section, text_left):
    f = section.footer; f.is_linked_to_previous = False
    p = f.paragraphs[0]
    for r in list(p.runs): r._r.getparent().remove(r._r)
    _fmt(p, CFG['lead']); _font(p.add_run(text_left + '  -  page '), FONT, CFG['txt']); _field(p, 'PAGE'); _font(p.add_run(' of '), FONT, CFG['txt']); _field(p, 'NUMPAGES'); p.alignment = 1


def _emit(doc, blocks, last_gap=None):
    last_gap = CFG['gap'] if last_gap is None else last_gap
    g = geom(); firstp = None; txt, lead, code, clead = CFG['txt'], CFG['lead'], CFG['code'], CFG['clead']
    half = g['colw_pt'] / 2
    for bi, b in enumerate(blocks):
        last = bi == len(blocks) - 1; keep_next = (not last) or b['k'] in ('qh', 'qi'); after = last_gap if last else 0.0
        if b.get('keep'): keep_next = True
        p = doc.add_paragraph()
        if b['k'] == 'qh':
            _fmt(p, CFG['head'] + 3, 1.0, keep_next=True)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, CFG['head'], True)
        elif b['k'] == 'qi':
            _fmt(p, lead, 3.0, keep_next=True)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, False)
        elif b['k'] == 'q':
            _fmt(p, lead, after, keep_next=keep_next)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
        elif b['k'] == 'opt':
            _fmt(p, lead, after, left=15, first=-15, keep_next=keep_next, tabs=(15,))
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
        elif b['k'] == 'bank':
            _fmt(p, lead, 0.0, keep_next=keep_next, tabs=(half,)); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(3); p.paragraph_format.right_indent = Pt(3)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
            if last: p.paragraph_format.space_after = Pt(after)
        elif b['k'] == 'code':
            _fmt(p, clead, 3.0, keep_next=keep_next); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(4); p.paragraph_format.right_indent = Pt(4)
            _font(p.add_run(b['text']), MONO, code)
        elif b['k'] == 'line':
            _fmt(p, CFG['qline'], after, keep_next=keep_next)
            p.paragraph_format.tab_stops.add_tab_stop(Pt(g['colw_pt']), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.LINES)   # leader line across the column
            _font(p.add_run('\t'), FONT, txt)
        if firstp is None: firstp = p
    return firstp


def _break_para(doc):
    p = doc.add_paragraph(); _fmt(p, 1.0)
    r = p.add_run(); _font(r, FONT, 1); r.add_break(WD_BREAK.COLUMN if CFG['cols'] == 2 else WD_BREAK.PAGE)
    return p


def cover_args(paper, date_time=None):
    """The cover page content: the facts the owner gave (course, title, term, duration, instructor) and the question table of the structure file; open fields stay marked."""
    S = paper['structure']; qs = [(str(q['number']), q['points'], bool(q.get('bonus'))) for q in S['questions']]
    outs = []
    for q in S['questions']:
        chs = sorted({c for sub in q['sub'] for c in sub['chapters']})
        outs.append(chs)                                   # learning outcome n is the outcome of chapter n (LO-1 to LO-6 name the chapters 1 to 6 as their source in the outcomes file)
    ins = C.default_instructions()
    ins[1] = [('Questions 1 to 4 are answered on the ', False), ('separate answer sheet, which is read by a machine', True),
              ('. Use a dark (black or blue) pen and ', False), ('fill each chosen mark completely', True),
              ('. To cancel an answer, cross its mark out with an X, then fill the mark you now choose. Do not use correction fluid. ', False),
              ('Question 5 (the bonus) is answered with a pen on the lines of the question pages and is marked by hand.', True)]
    ins[2] = 'Write only inside the boxes and marks of the answer sheet, and on the lines of Question 5. You may use the blank areas of the question pages for scratch work; do not use any additional scratch paper.'
    ins.insert(0, 'Check that the form letter and the form code printed on the question pages are the same as those printed on your answer sheet (Form %s, form code %s).' % (paper['form']['letter'], paper['form']['code']))
    return dict(questions=qs, outcomes=outs, instructions=ins, date_time=date_time)


def write_docx(paper, path, breaks=(), per_item_break=False, blocks_override=None, cover=True):
    """breaks: slot positions (indexes into paper['slots']) that start a new column (or page when single column). per_item_break: a break after every slot (the measuring document, no cover)."""
    S = paper['structure']; f = paper['form']; P = paper['params']
    if per_item_break or not cover: doc = Document()
    else: doc = C.new_document()
    if per_item_break or not cover:
        st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(CFG['txt']); _set_fonts(st.element.get_or_add_rPr(), FONT)
        st.paragraph_format.space_before = Pt(0); st.paragraph_format.space_after = Pt(0)
    else:
        a = cover_args(paper)
        C.cover(doc, 'SEN0401', 'Special Topics: Blockchain', 'Midterm Exam', 'Fall', '2026-2027', a['date_time'], '60 Minutes', 'Dr. Yusuf ALTUNEL', a['questions'], a['outcomes'],
                instructions=a['instructions'], own_section=True, outcomes_ttl=OUTCOMES)
    settings = doc.settings.element
    for tag in ('w:autoHyphenation',):
        e = settings.find(qn(tag))
        if e is not None: settings.remove(e)
    for cs in settings.iter(qn('w:compatSetting')):
        if cs.get(qn('w:name')) == 'compatibilityMode': cs.set(qn('w:val'), '15')
    sec = doc.sections[-1]
    for ref in sec._sectPr.findall(qn('w:footerReference')) + sec._sectPr.findall(qn('w:headerReference')): sec._sectPr.remove(ref)
    for e in sec._sectPr.findall(qn('w:rtlGutter')) + sec._sectPr.findall(qn('w:type')): sec._sectPr.remove(e)
    _page_setup(sec, CFG['side']); _cols(sec, 1)
    _footer(sec, 'SEN0401 midterm v%d  -  Form %s  -  form code %s' % (paper['version'], f['letter'], f['code']))
    two = CFG['cols'] == 2
    if not per_item_break:
        p = doc.add_paragraph(); _fmt(p, 15, 1.0, keep_next=True); _font(p.add_run('SEN0401 Special Topics: Blockchain - Midterm exam, Form %s' % f['letter']), FONT, 13, True)
        p = doc.add_paragraph(); _fmt(p, CFG['lead'], 0.0, keep_next=True)
        _font(p.add_run('Form code %s' % f['code']), FONT, CFG['txt'], True)
        _font(p.add_run(' (it must equal the form code printed on your answer sheet). Chapters %s. %d minutes. Questions 1 to 4 (25 points each) are answered on the separate answer sheet; '
                        'Question 5 is a 10-point bonus, written on the lines below it. Give ONE answer per row unless the question says otherwise.' % (', '.join(map(str, paper['chapters'])), P['sitting'])), FONT, CFG['txt'])
        if two:
            doc.add_section(WD_SECTION.CONTINUOUS)
            sp = doc.paragraphs[-1]; _fmt(sp, 1.0); mrk = OxmlElement('w:rPr'); sz = OxmlElement('w:sz'); sz.set(qn('w:val'), '2'); mrk.append(sz); _insert_ppr(sp._p.get_or_add_pPr(), mrk, after=('w:sectPr', 'w:pPrChange'))
            _cols(doc.sections[-1], 2)
    else:
        if two: _cols(sec, 2)
    brk = set(breaks); firsts = set()
    seenq = set()
    for idx, s in enumerate(paper['slots']):
        if s['q'] not in seenq: seenq.add(s['q']); firsts.add(idx)
    for idx, s in enumerate(paper['slots']):
        blocks = blocks_override[idx] if blocks_override else slot_blocks(s, paper, first_of_question=idx in firsts)
        if idx in brk: _break_para(doc)
        _emit(doc, blocks)
        if per_item_break: _break_para(doc)
    doc.core_properties.author = ''; doc.core_properties.title = 'SEN0401 midterm v%d form %s' % (paper['version'], f['letter']); doc.core_properties.comments = ''
    doc.save(path)


# ------------------------------------------------------------------ the key (Word)
def answer_key(paper):
    """The key of the form: one entry per sub-question, in the printed order, with the answer places of the sheet; question 5 carries its rubric (hand-graded)."""
    S = paper['structure']; f = paper['form']
    key = dict(paper=paper['kind'], version=paper['version'], form=f['letter'], form_code=f['code'], seed=f['seed'], chapters=paper['chapters'], total_points_without_bonus=S['total_points_without_bonus'],
               bonus_points=S['bonus_points'], answer_mode='GridOnCover', items=[])
    for s in paper['slots']:
        sub0 = s['sub'][0]
        if s['kind'] == 'explain':
            e = dict(label='%d%s' % (s['q'], s['label']), question=s['q'], type='ShortExplanation', points=sub0['points'], chapters=s['chapters'], structure_key=sub0['key'], item_key=sub0['item'], hand_marked=True,
                     prompt=sub0['prompt'], tips=sub0['tips'], rubric=sub0['rubric'], rubric_statements=sub0['rubric_points'], critical_points=sub0.get('critical_points', []), sources=sub0.get('sources', []))
            key['items'].append(e); continue
        it = s['item']; n = it['label']; t = it['type']
        e = dict(label=n, question=s['q'], type=t, points=s['points'], chapters=it['chapters'], bloom=it['bloom'], structure_key=[x['key'] for x in s['sub']], item_key=it['key'], position=it['position'],
                 critical_points=it.get('critical_points', []))
        if t in CHOICE: e['answer'] = {n: 'ABCD'[it['answer']]}
        elif t == 'Matching':
            e['answer'] = {'%s%d' % (n, k + 1): 'ABCDEFGH'[it['responses'].index(p['match'])] for k, p in enumerate(it['premises'])}; e['points_per_part'] = s['sub'][0]['points_per_part']
        elif t == 'Ordering':
            e['answer'] = {'%s%d' % (n, j + 1): it['display_order'][j] + 1 for j in range(len(it['steps']))}; e['points_per_part'] = s['sub'][0]['points_per_part']
            e['correct_order_text'] = it['steps']
        elif t == 'FillBlankGroup':
            e['answer'] = {'%d%s' % (s['q'], s['letters'][b]): R.bank_label(paper, it['bank_order'].index(b) + 1) for b in range(len(it['blanks']))}
            e['points_per_blank'] = {'%d%s' % (s['q'], s['letters'][b]): s['sub'][b]['points'] for b in range(len(it['blanks']))}
            e['blank_meaning'] = {'%d%s' % (s['q'], s['letters'][b]): it['blanks'][b]['answer'] for b in range(len(it['blanks']))}
        elif t == 'NumericAnswer': e['answer'] = {n: dict(value=it['key_value'], unit=it['unit'], tolerance=it['tolerance'])}
        elif t == 'CodeTrace': e['answer'] = {n: it['output']}
        key['items'].append(e)
    return key


def write_key_docx(paper, key, path, note=''):
    doc = Document(); f = paper['form']
    st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(10); _set_fonts(st.element.get_or_add_rPr(), FONT)
    sec = doc.sections[0]; _page_setup(sec, 15.0); sec.top_margin = Mm(12)
    CFG_save = dict(CFG); set_cfg('compact10')
    _footer(sec, 'SEN0401 midterm v%d key  -  Form %s  -  form code %s' % (paper['version'], f['letter'], f['code']))
    p = doc.add_paragraph(); _fmt(p, 14, 2.0); _font(p.add_run('SEN0401 midterm v%d, Form %s - ANSWER KEY (for the grader, not for students)' % (paper['version'], f['letter'])), FONT, 12, True)
    p = doc.add_paragraph(); _fmt(p, 11.5, 3.0)
    _font(p.add_run('Form code %s. Seed %d. Chapters %s. Questions 1 to 4: 25 points each (100 in all), read from the answer sheet. Question 5: bonus, 10 points, hand-graded from the lines of the paper. '
                    'Letters, digits and codes are the rows of the answer sheet; a number keeps the stated tolerance; a trace is the printed text. Partial credit for ordering and matching is proportional per correct part. %s' %
                    (f['code'], f['seed'], ', '.join(map(str, paper['chapters'])), note)), FONT, 10)
    for e in key['items']:
        p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=34, first=-34, tabs=(34,), keep_next=True)
        _font(p.add_run('%s' % e['label']), FONT, 10, True)
        if e['type'] == 'ShortExplanation':
            _font(p.add_run('\tBONUS, %s points, chapters %s, hand-graded   [%s]' % (_pts(e['points']), ','.join(map(str, e['chapters'])), e['item_key'])), FONT, 10)
            p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=34); _font(p.add_run('Prompt: ' + e['prompt']), FONT, 10)
            for r in e['rubric']:
                p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=46, first=-12, tabs=(46,)); _font(p.add_run('-\t' + r), FONT, 10)
            p = doc.add_paragraph(); _fmt(p, 11.5, 4.0, left=34)
            _font(p.add_run('Marking: %d rubric statements, %s points in all; how the points split between the statements is for the instructor (open). The answer sheet has no place for this answer.' % (e['rubric_statements'], _pts(e['points']))), FONT, 10)
            continue
        _font(p.add_run('\t%s   %s points   chapters %s   Bloom %d   [%s]' % (e['type'], _pts(e['points']), ','.join(map(str, e['chapters'])), e['bloom'], e['item_key'])), FONT, 10)
        for k, v in e['answer'].items():
            if isinstance(v, dict): s_ = 'value %s %s (tolerance %s)' % (v['value'], v['unit'], v['tolerance'])
            else: s_ = str(v)
            extra = ''
            if e['type'] == 'Matching' or e['type'] == 'Ordering': extra = '   (%s points)' % _pts(e['points_per_part'])
            if e['type'] == 'FillBlankGroup': extra = '   (%s points; the entry: %s)' % (_pts(e['points_per_blank'][k]), e['blank_meaning'][k])
            p = doc.add_paragraph(); _fmt(p, 11.5, 0.0 if k != list(e['answer'])[-1] else 4.0, left=46, first=-12, tabs=(46,), keep_next=k != list(e['answer'])[-1])
            _font(p.add_run('row %s\t' % k), FONT, 10); _font(p.add_run(s_), FONT, 10, True); _font(p.add_run(extra), FONT, 10)
    CFG.clear(); CFG.update(CFG_save)
    doc.core_properties.author = ''; doc.save(path)


# ------------------------------------------------------------------ LibreOffice export and measurement
def export_pdf(docx_path, outdir, profile='/tmp/lo_profile_papers3'):
    cmd = ['soffice', '-env:UserInstallation=file://' + profile, '--headless', '--convert-to', 'pdf', '--outdir', outdir, docx_path]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    pdf = os.path.join(outdir, os.path.splitext(os.path.basename(docx_path))[0] + '.pdf')
    if not os.path.exists(pdf): raise RuntimeError('LibreOffice export failed: ' + r.stdout + r.stderr)
    return pdf


def pdf_pages(path):
    o = subprocess.run(['pdfinfo', path], capture_output=True, text=True).stdout
    return int(re.search(r'Pages:\s+(\d+)', o).group(1))


def columns_of_pdf(pdf, skip=0):
    """Per page (after `skip` pages) and column (0/1): the words of the column; the footer line is dropped. In single-column mode column 0 holds everything."""
    import pdfplumber
    out = []; n = CFG['cols']
    with pdfplumber.open(pdf) as d:
        for pg in d.pages[skip:]:
            ws = pg.extract_words(extra_attrs=['fontname', 'size'], keep_blank_chars=False, use_text_flow=False)
            fy = pg.height - BOTTOM * 72 / 25.4; cols = [[], []]
            for w in ws:
                if w['bottom'] > fy + 0.5: continue
                c = 0 if n == 1 or (w['x0'] + w['x1']) / 2 < pg.width / 2 else 1
                cols[c].append(w)
            out.append(cols)
    return out


# ------------------------------------------------------------------ the answer sheet
def sheet_spec(paper):
    """Units in question order. Same block types as the sheet module; BLOCK_MAX is set so that one sub-question is one block (matching 4, bank 2 = one group)."""
    units_ = []
    # Question 3 on the sheet: the matching blocks first, the ordering block after them, whatever the printed order (every row carries its own label; the blocks then fill the page - with the ordering block first the
    # fourth block of the first column would not fit and the sheet would need a second page). Everything else follows the printed order.
    slots_ = sorted([s for s in paper['slots'] if s['kind'] != 'explain'], key=lambda s: (s['q'], 0 if s['kind'] == 'match' else 1 if s['q'] == 3 else 0))
    for s in slots_:
        it = s['item']; n = it['label']; t = it['type']
        if t in CHOICE: units_.append({'no': n, 'kind': 'choice', 'opts': 'ABCD'})
        elif t == 'Matching':
            for k in range(len(it['premises'])): units_.append({'no': '%s%d' % (n, k + 1), 'kind': 'match', 'opts': 'ABCDEFGH'[:len(it['responses'])]})
        elif t == 'Ordering':
            for k in range(len(it['steps'])): units_.append({'no': '%s%d' % (n, k + 1), 'kind': 'order', 'opts': '123456'[:len(it['steps'])]})
        elif t == 'FillBlankGroup':
            for b in range(len(it['blanks'])): units_.append({'no': '%d%s' % (s['q'], s['letters'][b]), 'kind': 'bank', 'digits': 2})
        else: units_.append({'no': n, 'kind': 'human', 'cells': 5})
    f = paper['form']
    return {'paper_kind': 'Midterm', 'paper_version': paper['version'], 'form_code': f['code'], 'form_letter': f['letter'], 'units': units_}


def _sheet_render_v3():
    src = __import__('inspect').getsource(A.render)
    old5 = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below. Numbers go in the boxes, one digit per box.',"
    new5 = "'5  Fill-in codes: two digits, one bubble in the upper row and one in the row below.',\n                     '    Numbers go in the boxes, one digit per box.',"
    oldc = "'form code %s' % spec['form_code']"
    newc = "'Form %s   form code %s' % (spec.get('form_letter', '?'), spec['form_code'])"
    assert src.count(old5) == 1 and src.count(oldc) == 1
    ns = dict(A.__dict__); exec(src.replace(old5, new5).replace(oldc, newc), ns); return ns['render']


def _sheet_layout_v3():
    """build_layout of the sheet module with ONE number changed: the header zone above the first blocks is 165 pt, not 175 pt (the header text ends at 139 pt and its rule is at 150 pt), so that the nine blocks of this paper
    keep one page without a closure row running out of its column. The layout JSON has the same fields and block types, so the reader v1.2.0 reads it unchanged."""
    src = __import__('inspect').getsource(A.build_layout); old = 'top = MARG + 175'
    assert src.count(old) == 1
    ns = dict(A.__dict__); exec(src.replace(old, 'top = MARG + 165'), ns); return ns['build_layout']


def render_sheet(paper, path):
    saved = dict(A.BLOCK_MAX)
    A.BLOCK_MAX.update({'match': 4, 'bank': 2})                  # one sub-question per block (runtime setting of the sheet module's table; the module file is unchanged)
    try:
        spec = sheet_spec(paper); layout = _sheet_layout_v3()(spec)
    finally:
        A.BLOCK_MAX.clear(); A.BLOCK_MAX.update(saved)
    layout['form_code'] = paper['form']['code']; layout['form_letter'] = paper['form']['letter']
    _sheet_render_v3()(layout, path)
    return pdf_pages(path), layout
