"""SEN0401 midterm paper library, version 7.0.0 (new file, a copy of sen0401_exam_paper_lib_v6_1_0.py, which stays unchanged). Holds no question and no answer.
WHAT IS NEW AGAINST v6 (owner redesign of 2026-11-02, 18:20 Istanbul; task TK_Exam_V7_PapersTool_Build):
  * NO deduction of any kind, NO floor, NO bonus: the scoring module is v2.0.0 (through the row-points adapter sen0401_exam_scoring_rows_v1_0_0.py, because the items carry whole-number row points that are not equal inside a unit);
    the cover and the question headings carry no penalty sentence; the legal-copy sentence and the rule 'two answers in one place count as no answer' stay.
  * FIVE alternatives in every closed unit (choice A-E, matching 5 responses, ordering places 1-5, fill-in bank of 5 entries lettered A-E); engine v1.2.0 and renderer v1.3.0 (five options).
  * NO tips page: the tip of an item (a string 'Tip: ...' of at most 12 words, field 'tip', flag 'needs_tip') is printed ONCE under the stem or the instruction, on the question itself.
  * The sheet is ONE page from the sheet module v7.0.0 (units_from_list): choice-type answers only; numbers and code traces are written by hand on the question pages.
  * The key carries a ONE-PAGE 'How to grade' section (page 1 of the key) and the exact blind figure; nothing to compute beyond adding points.
  * The structure file and the items file are PARAMETERS (a synthetic pair for the tooling run, the real pair from CME private for the real set). A SYNTHETIC pair is disclosed on the cover line, in the footer, in the key and in the sheet stamp.
THE FORM CODE: V K F F + the Damm check digit of the sheet module (V = paper version, K = 0 midterm, FF = form number)."""
import json, os, random, re, subprocess, sys, shutil
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_exam_engine_v1_2_0 as E
import sen0401_exam_engine_render_v1_3_0 as R
import sen0401_exam_answersheet_v1_0_0 as A
import sen0401_exam_cover_render_v1_0_0 as C
import sen0401_exam_scoring_v2_0_0 as SC
import sen0401_exam_scoring_rows_v1_0_0 as SR
import sen0401_exam_answersheet_v7_1_0 as SV
import sen0401_exam_answersheet_v7_build_v1_1_0 as SB
from sen0401_exam_engine_v1_2_0 import units, CHOICE
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_BREAK, WD_LINE_SPACING, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

VERSION = '7.2.0'
SOLUTIONS = '/home/claude/CME/exams/SEN0401/08-tooling/exam/private/sen0401_exam_key_solutions_v1_8_0.json'      # the worked solutions (private; one entry per item key, lines per label)
STRUCTURE = '/home/claude/CME/exams/SEN0401/08-tooling/exam/private/sen0401_exam_structure_v1_5_0.json'      # the real structure (CME private); the caller passes another path for the synthetic run
OUTCOMES = os.path.join(os.path.dirname(os.path.dirname(HERE)), '01-outcomes', 'sen0401_outcomes_v1_1_1.ttl')
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
            it = byk[sub['item']]
            if sub['type'] == 'FillBlankGroup' and sub['item'] in seen: seen[sub['item']]['sub'].append(sub); seen[sub['item']]['points'] += sub['points']; continue
            s = dict(q=qn_, kind=SLOT_KINDS[sub['type']], item=it, sub=[sub], points=sub['points'], chapters=list(it['chapters']), bloom=it['bloom'], type=sub['type'], skey=sub['key'])
            slots.append(s)
            if sub['type'] == 'FillBlankGroup': seen[sub['item']] = s
    return slots


def resolve_items_path(S, structure_path):
    p = S['items_file']
    if os.path.isabs(p): return p
    return os.path.join(os.path.dirname(os.path.abspath(structure_path)), os.path.basename(p))      # the items file sits beside the structure file


def make_form(form_no, seed=5701, version=7, kind='midterm', accept=None, structure=None, structure_path=None):
    """One form. Form 1 keeps the structure file's order of the sub-questions; other orders are drawn inside each question with random.Random(seed): neighbours are of different item type and primary chapter where the question allows it.
    accept(order_of_slots) is an optional layout test (the page packing). structure = the loaded structure dict (or structure_path to load it)."""
    sp_ = structure_path or STRUCTURE
    S = structure or load_structure(sp_); chapters = S['chapters']
    path = resolve_items_path(S, sp_)
    M = E.M
    P = E.Params(sum(units(i) for i in E.load_authored(path, M.parse_ch(','.join(map(str, chapters))))[0]), M.parse_ch(','.join(map(str, chapters))), None, 'GridOnCover', synthesis_min=0, higher_from=3,
                 indirect_enabled=False, seed=seed, sitting=60, columns=CFG['cols'], code_cap=45, page_limit=None, enable=[], allow_repeat=False, authored=path, order='mixed',
                 code_font=int(CFG['code']) if CFG['code'] == int(CFG['code']) else CFG['code'])
    auth, skipped = E.load_authored(path, P.chapters)
    byk = {i['key']: json.loads(json.dumps(i)) for i in auth}
    pages, pkey = E.pages_for(P.chapters)
    for i in byk.values():
        i['matches'] = E.check_copies(i, pages); i['checked_against'] = len(pages)
    base = _slots(S, byk); qnums = [q['number'] for q in S['questions']]
    rnd = random.Random(seed * 13 + 5); draws = 1
    if form_no == 1 and (accept is None or accept(base)):
        order = base[:]
    else:
        order = None
        for draws in range(1, 200001):
            o = []
            for qn_ in qnums:
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
            if ok and (accept is None or accept(o)): order = o; break
        if order is None: raise RuntimeError('no mixed order satisfies the constraints')
    # letters, positions, shuffles
    r2 = random.Random(seed * 7)
    for qn_ in qnums:
        letters = iter('abcdefgh')
        for s in [s for s in order if s['q'] == qn_]:
            s['letters'] = [next(letters) for _ in s['sub']]; s['label'] = s['letters'][0]
    choice_slots = [s for s in order if s['kind'] == 'choice']
    E.balance_letters([s['item'] for s in choice_slots], r2)
    pos = 0; items = []
    for s in order:
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
                 page_chapters=list(pkey), page_items=len(pages), structure=S, synthetic=bool(S.get('synthetic')), items_path=path,
                 form=dict(letter='', number=form_no, seed=seed, code=code, order_draws=draws,
                           order_rule=('form A: the sub-question order of the structure file') if (form_no == 1 and draws == 1) else
                           'shuffle of the sub-questions inside each question by random.Random(seed*13+5); neighbours of different item type and primary chapter where possible; and the layout test (the sub-questions pack into the planned columns with the planned free share)'))
    return paper


SYNTH_LINE = 'Synthetic input - invented placeholder wording, not a real exam, never delivered.'


# ------------------------------------------------------------------ plain directions (every sentence at most 25 words)
R4_VERBS = ('Write', 'Circle', 'Fill', 'Put', 'Match', 'Choose')
FORBIDDEN_WORDS = re.compile(r'penalt|deduct|minus|negative|costs?\b|lose|lost|taken away|subtract|bonus|floor', re.I)


def plain_how(sub, it=None):
    """The answer-format sentence of a sub-question: the structure's how_to_answer (or the item's), checked: starts with a verb, at most 25 words, no word about points taken away."""
    h = sub.get('how_to_answer') or (it or {}).get('how_to_answer')
    assert h and h.split()[0] in R4_VERBS and len(h.split()) <= 25 and not FORBIDDEN_WORDS.search(h), h
    return h


def tip_of(it):
    """The ONE tip line of an item: its 'tip' string ('Tip: ...', at most 12 words after the prefix) when the item has one; else None."""
    t = (it.get('tip') or '').strip()
    if not t: return None
    assert t.startswith('Tip: ') and len(t[5:].split()) <= 12, (it['key'], t)
    return t


def row_points_of(sub, it):
    rp = sub.get('row_points') or it.get('row_points')
    return list(rp) if rp else None


def points_phrase(pts, rows, what):
    """'(8 points in all.)' or, when every row scores the same, '(8 points; 2 for each correct pair.)'."""
    if rows and len(set(rows)) == 1: return '  (%s points; %s for each %s.)' % (_pts(pts), _pts(rows[0]), what)
    return '  (%s points in all.)' % _pts(pts)


# ------------------------------------------------------------------ the printable content of one slot
def _pts(p):
    return ('%g' % p) if abs(p - round(p)) < 1e-9 else ('%.2f' % p).rstrip('0')


def question_instruction(qd):
    """The direction under a question heading, in plain words (no penalty wording; checked)."""
    t = qd['instruction']
    assert not FORBIDDEN_WORDS.search(t), t
    return t


def heading_blocks(paper, qnum):
    qd = [q for q in paper['structure']['questions'] if q['number'] == qnum][0]
    return [dict(k='qh', runs=[('Question %d - %s (%d points)' % (qd['number'], qd['title'], qd['points']), True)]),
            dict(k='qi', runs=[(question_instruction(qd), False)])]


def slot_blocks(s, paper, first_of_question=False):
    """Paragraph specifications of one sub-question. kinds: qh, qi, q, tip (the ONE short tip line under the stem), opt, code, bank, line, how, ans, boxopt, boxq. v7: no tips page, five alternatives, no bonus."""
    B = []
    def q(runs, **kw): B.append(dict(k='q', runs=runs, **kw))
    def opt(label, text): B.append(dict(k='opt', runs=[(label, True), ('\t' + text, False)]))
    def tip(it):
        t = tip_of(it)
        if t: B.append(dict(k='tip', text=t, keep=True))
    if first_of_question:
        B += heading_blocks(paper, s['q'])
    t = s['type']; it = s['item']; n = it['label']; pts = s['points']; how = plain_how(s['sub'][0], it)
    if t in CHOICE:
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)], keep=True)
        tip(it)
        if it.get('code'): B.append(dict(k='code', text=it['code']))
        for k, o in enumerate(it['options']): opt('ABCDE'[k] + '.', o)
        B.append(dict(k='ans', boxes=1, text=how))
    elif t == 'Matching':
        sub = s['sub'][0]; rows = row_points_of(sub, it)
        q([('%s. ' % n, True), (it['q'], False), (points_phrase(pts, rows, 'correct pair'), False)], keep=True)
        tip(it)
        B.append(dict(k='how', text=how, keep=True))
        for k, p in enumerate(it['premises']): B.append(dict(k='boxopt', boxes=1, label='%d)' % (k + 1), text=p['text']))
        for k, r in enumerate(it['responses']): opt('ABCDE'[k] + '.', r)
    elif t == 'Ordering':
        sub = s['sub'][0]; rows = row_points_of(sub, it)
        q([('%s. ' % n, True), (it['q'], False), (points_phrase(pts, rows, 'step in the right place'), False)], keep=True)
        tip(it)
        B.append(dict(k='how', text=how, keep=True))
        for j, k in enumerate(it['display_order']): B.append(dict(k='boxopt', boxes=1, label='%d)' % (j + 1), text=it['steps'][k]))
    elif t == 'FillBlankGroup':
        ents = [b['answer'] for b in it['blanks']] + list(it['distractors']); order = it['bank_order']
        labs = ['%d%s' % (s['q'], l) for l in s['letters']]
        q([('%s-%s. ' % (labs[0], labs[-1]), True), (it['q'], False)], keep=True)
        tip(it)
        cells = sorted(range(len(ents)), key=lambda k: order.index(k))
        for k in cells:      # ONE bank entry per line (hanging indent)
            B.append(dict(k='bank', runs=[(R.bank_label(paper, order.index(k) + 1) + '.', True), ('\t' + ents[k], False)]))      # 'A.' + tab, as the options are written (the readability tool v1.1.0 reads that form as an option line)
        B.append(dict(k='how', text=how, keep=True))
        for b, bl in enumerate(it['blanks']): B.append(dict(k='boxq', boxes=1, runs=[('%s. ' % labs[b], True), (bl['text'], False), ('  (%s points)' % _pts(s['sub'][b]['points']), False)]))
    elif t == 'NumericAnswer':
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)], keep=True)
        tip(it)
        B.append(dict(k='ans', boxes=5, text=how))
    elif t == 'CodeTrace':
        q([('%s. ' % n, True), (it['q'], False), ('  (%s points)' % _pts(pts), False)], keep=True); tip(it); B.append(dict(k='code', text=it['code']))
        B.append(dict(k='ans', boxes=5, text=how))
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


BOX_FONT, BOX_NBSP, BOX_GAP_FONT = 14, 4, 10                   # an answer box: four no-break spaces at 14 point with a single border (about 15.6 pt wide, 16 pt high); boxes are separated by a space at 10 point
BOX_W = BOX_NBSP * 0.278 * BOX_FONT                            # Arial space width is 0.278 em
BOX_GAP = 0.278 * BOX_GAP_FONT


def _box(p, n):
    """n answer boxes in the paragraph p: each box is a run of no-break spaces with a single black border (rendered by Word and LibreOffice alike)."""
    for i in range(n):
        r = p.add_run('\u00a0' * BOX_NBSP); _font(r, FONT, BOX_FONT)
        b = OxmlElement('w:bdr'); b.set(qn('w:val'), 'single'); b.set(qn('w:sz'), '6'); b.set(qn('w:space'), '0'); b.set(qn('w:color'), '000000'); r._r.get_or_add_rPr().append(b)
        if i < n - 1: _font(p.add_run(' '), FONT, BOX_GAP_FONT)
    return n * BOX_W + (n - 1) * BOX_GAP


def _at_least(p, lead):
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.AT_LEAST; p.paragraph_format.line_spacing = Pt(lead)


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
        elif b['k'] == 'tip':
            _fmt(p, lead, after, keep_next=keep_next)
            _font(p.add_run(b['text']), FONT, txt, False)
            for r_ in p.runs: r_.font.italic = True
        elif b['k'] == 'opt':
            _fmt(p, lead, after, left=15, first=-15, keep_next=keep_next, tabs=(15,))
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
        elif b['k'] == 'bank':
            _fmt(p, lead, 0.0, keep_next=keep_next, tabs=(21,)); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(21); p.paragraph_format.first_line_indent = Pt(-18); p.paragraph_format.right_indent = Pt(3)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
            if last: p.paragraph_format.space_after = Pt(after)
        elif b['k'] == 'code':
            _fmt(p, clead, 3.0, keep_next=keep_next); _border(p, space=2)
            p.paragraph_format.left_indent = Pt(4); p.paragraph_format.right_indent = Pt(4)
            _font(p.add_run(b['text']), MONO, code)
        elif b['k'] == 'how':
            _fmt(p, lead, after, keep_next=keep_next)
            _font(p.add_run(b['text']), FONT, txt, False)
        elif b['k'] == 'ans':
            _fmt(p, lead, after, keep_next=keep_next); w = _box(p, b['boxes']); ind = w + 14
            p.paragraph_format.left_indent = Pt(ind); p.paragraph_format.first_line_indent = Pt(-ind); p.paragraph_format.tab_stops.add_tab_stop(Pt(ind)); _at_least(p, lead)
            _font(p.add_run('\t' + b['text']), FONT, txt, False)
        elif b['k'] == 'boxopt':
            _fmt(p, lead, after, keep_next=keep_next); w = _box(p, b['boxes']); ind = w + 6; ind2 = ind + 15
            p.paragraph_format.left_indent = Pt(ind2); p.paragraph_format.first_line_indent = Pt(-ind2); p.paragraph_format.tab_stops.add_tab_stop(Pt(ind)); p.paragraph_format.tab_stops.add_tab_stop(Pt(ind2)); _at_least(p, lead)
            _font(p.add_run('\t'), FONT, txt); _font(p.add_run(b['label']), FONT, txt, True); _font(p.add_run('\t' + b['text']), FONT, txt, False)
        elif b['k'] == 'boxq':
            _fmt(p, lead, after, keep_next=keep_next); w = _box(p, b['boxes']); ind = w + 6
            p.paragraph_format.left_indent = Pt(ind); p.paragraph_format.first_line_indent = Pt(-ind); p.paragraph_format.tab_stops.add_tab_stop(Pt(ind)); _at_least(p, lead)
            _font(p.add_run('\t'), FONT, txt)
            for t_, bold in b['runs']: _font(p.add_run(t_), FONT, txt, bold)
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
    """The cover page content: the facts the owner gave (course, title, term, duration, instructor) and the question table of the structure file; open fields stay marked. v7: no penalty sentence; the legal-copy sentence and the two-answers rule stay."""
    S = paper['structure']; qs = [(str(q['number']), q['points'], False) for q in S['questions']]
    outs = []
    for q in S['questions']:
        chs = sorted({c for sub in q['sub'] for c in sub['chapters']})
        outs.append(chs)                                   # learning outcome n is the outcome of chapter n (LO-1 to LO-6 name the chapters 1 to 6 as their source in the outcomes file)
    ins = [
        'The form code of this paper is %s. The same code is printed on your answer sheet. Write your name and student identity number above and on the sheet.' % paper['form']['code'],
        [('Write your answers on the question pages: ', False), ('these answers count', True), ('. Use the box or the lines printed next to each question, and a dark pen.', False)],
        [('The answer sheet is ', False), ('optional', True), (' and only makes reading faster. If the sheet and the question pages differ, the question pages count.', False)],
        'To change an answer, cross it out with an X and write or fill the new answer next to it. Do not use correction fluid.',
        [('Two answers in one place count as no answer. ', True), ('A right answer scores its points; every other answer scores 0.', False)],
        'Write each number in the boxes on the question page and copy it into the boxes of the answer sheet. The question pages count if they differ.',
        'Unclear writing, or writing outside the boxes, may not be read and will not be graded.',
        [('Allowed on the table: ', False), ('the question paper, the answer sheet, a pen and an eraser', True), (', and: ______________ (instructor to fill in). Clear everything else and do not share your belongings.', False)],
        [('Cell phones, laptops and other networked devices are ', False), ('FORBIDDEN', True), (': their use or presence is a ', False), ('cheating attempt', True), ('. Do not communicate with other students unless the instructor allows it.', False)],
    ]
    if paper.get('synthetic'): ins.insert(0, [(SYNTH_LINE, True)])
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
    _footer(sec, 'SEN0401 midterm v%d  -  form code %s%s' % (paper['version'], f['code'], '  -  SYNTHETIC' if paper.get('synthetic') else ''))
    two = CFG['cols'] == 2
    if not per_item_break:
        p = doc.add_paragraph(); _fmt(p, 15, 1.0, keep_next=True); _font(p.add_run('SEN0401 Special Topics: Blockchain - Midterm exam'), FONT, 13, True)
        p = doc.add_paragraph(); _fmt(p, CFG['lead'], 0.0, keep_next=True)
        _font(p.add_run('Form code %s.' % f['code']), FONT, CFG['txt'], True)
        if paper.get('synthetic'): _font(p.add_run(' ' + SYNTH_LINE), FONT, CFG['txt'], True)
        _font(p.add_run(' Chapters %s. %d minutes. Write each answer on the question pages: these answers count. The answer sheet is optional and only makes reading faster.' % (', '.join(map(str, paper['chapters'])), P['sitting'])), FONT, CFG['txt'])
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
    doc.core_properties.author = ''; doc.core_properties.title = 'SEN0401 midterm v%d%s' % (paper['version'], ' SYNTHETIC' if paper.get('synthetic') else ''); doc.core_properties.comments = SYNTH_LINE if paper.get('synthetic') else ''
    doc.save(path)


# ------------------------------------------------------------------ the key (Word)
def recompute_note(it):
    """The key is recomputed by running the code where the item is Python: a code trace's printed output must equal the output of running its code. Returns a short status string."""
    if it['type'] != 'CodeTrace': return None
    import contextlib, io
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): exec(it['code'], {})
    except Exception as e:
        return 'NOT_RECOMPUTED (the listing did not run as Python: %s)' % type(e).__name__
    got = buf.getvalue().strip()
    if got != str(it['output']).strip(): raise ValueError('item %s: running the code prints %r but the item says %r' % (it['key'], got, it['output']))
    return 'recomputed by running the code: %s' % got


def answer_key(paper):
    """The key of the form: one entry per sub-question, in the printed order, with the answer places of the sheet. v7: no bonus, five alternatives, row points per label, no tolerance."""
    S = paper['structure']; f = paper['form']
    key = dict(paper=paper['kind'], version=paper['version'], form='', form_code=f['code'], seed=f['seed'], chapters=paper['chapters'], total_points=S['total_points'], answer_mode='GridOnCover',
               synthetic=bool(paper.get('synthetic')), question_totals={str(q['number']): q['points'] for q in S['questions']}, items=[])
    for s in paper['slots']:
        it = s['item']; n = it['label']; t = it['type']; sub0 = s['sub'][0]
        e = dict(label=n, question=s['q'], type=t, points=s['points'], chapters=it['chapters'], bloom=it['bloom'], structure_key=[x['key'] for x in s['sub']], item_key=it['key'], position=it['position'],
                 critical_points=it.get('critical_points', []))
        if t in CHOICE: e['answer'] = {n: 'ABCDE'[it['answer']]}; e['n_options'] = len(it['options'])
        elif t == 'Matching':
            e['answer'] = {'%s%d' % (n, k + 1): 'ABCDE'[it['responses'].index(p['match'])] for k, p in enumerate(it['premises'])}; e['n_responses'] = len(it['responses'])
            rows = row_points_of(sub0, it); e['row_points'] = {lab: rows[k] for k, lab in enumerate(e['answer'])}
        elif t == 'Ordering':
            e['answer'] = {'%s%d' % (n, j + 1): it['display_order'][j] + 1 for j in range(len(it['steps']))}; e['correct_order_text'] = it['steps']
            rows = row_points_of(sub0, it)      # the rows are given in the order of the correct sequence (step 1 .. step 5); the printed row j shows the step whose place is answer[j]
            e['row_points'] = {'%s%d' % (n, j + 1): rows[it['display_order'][j]] for j in range(len(it['steps']))}
        elif t == 'FillBlankGroup':
            e['answer'] = {'%d%s' % (s['q'], s['letters'][b]): R.bank_label(paper, it['bank_order'].index(b) + 1) for b in range(len(it['blanks']))}
            e['points_per_blank'] = {'%d%s' % (s['q'], s['letters'][b]): s['sub'][b]['points'] for b in range(len(it['blanks']))}
            e['blank_meaning'] = {'%d%s' % (s['q'], s['letters'][b]): it['blanks'][b]['answer'] for b in range(len(it['blanks']))}
            e['bank_codes'] = [R.bank_label(paper, k + 1) for k in range(len(it['blanks']) + len(it['distractors']))]
        elif t == 'NumericAnswer': e['answer'] = {n: dict(value=it['key_value'], unit=it['unit'], tolerance=0)}
        elif t == 'CodeTrace': e['answer'] = {n: it['output']}; e['recomputed'] = recompute_note(it)
        if 'row_points' in e: assert sum(e['row_points'].values()) == e['points'], (n, e['row_points'], e['points'])
        key['items'].append(e)
    add_scoring(key, paper)
    return key


def add_scoring(key, paper, sim_sheets=5000, sim_seed=70001):
    """Scoring section: the module v2.0.0 (through the row-points adapter) gives the perfect total, the exact blind figure and a simulation of blind sheets. Nothing is typed by hand."""
    import random
    rt = SC.rule_table(); places = []
    for m in SR.marks_of_key(key):
        places.append(dict(label=m['label'], item=m['item'], question=m['question'], rule_type=m['rule_type'], points=float(m['points']), blind_chance=str(m['p']), alternatives=m['alternatives']))
    perfect = SR.score(SR.perfect_marks(key), key); eb = SR.expected_blind(key)
    rng = random.Random(sim_seed); tot = []
    for _ in range(sim_sheets): tot.append(SR.score(SR.blind_marks(key, rng), key)['total'])
    mean = sum(tot) / sim_sheets; sd = (sum((x - mean) ** 2 for x in tot) / sim_sheets) ** 0.5
    key['scoring'] = dict(module='sen0401_exam_scoring_v2_0_0.py', module_version=SC.VERSION, adapter='sen0401_exam_scoring_rows_v1_0_0.py (row points per label)', rule_version=rt['rule_version'], rule=rt['rule'],
                          penalty=rt['penalty'], floor=rt['floor'], bonus=rt['bonus'], perfect_sheet_total=perfect['total'], max_total=perfect['max_total'],
                          blind_total_exact=str(eb['total']), blind_total_exact_decimal=float(eb['total']), blind_closed_exact=str(eb['closed']), blind_number_and_trace_exact=str(eb['number_and_trace']),
                          closed_points=float(eb['closed_points']), max_points=float(eb['max_points']),
                          blind_simulation=dict(sheets=sim_sheets, seed=sim_seed, mean=round(mean, 4), sd=round(sd, 4), standard_error=round(sd / sim_sheets ** 0.5, 4), minimum=min(tot)), places=places)


def how_to_grade_lines(key):
    """The ONE-PAGE grading procedure in plain words: (heading, text) pairs. Nothing to compute beyond adding points."""
    qt = ', '.join('question %s: %s' % (q, p) for q, p in key['question_totals'].items())
    return [
        ('1. Take one student\'s question pages.', 'The answers written on the question pages are the legal copy. The answer sheet (letters, digits and the copied numbers) is only a faster way to read them.'),
        ('2. Read the closed answers.', 'Choice, matching, ordering and fill-in places hold a letter or a digit. Read it from the box on the question page; the sheet box is for fast reading. If both exist and differ, the question page counts. If the page place is empty, the sheet counts.'),
        ('3. Compare each place with the key.', 'A place that equals the key letter or digit scores the points printed in the key for that place. Anything else scores 0: another answer, an empty place, or two answers in one place.'),
        ('4. Read the numbers and program outputs.', 'The hand-written value is read from the question page; the sheet box is for fast reading, and the student copies the number to the sheet. Compare it with the key value. The exact value scores the full points of the place, else 0. No partial credit, no tolerance, no half points.'),
        ('5. Rows.', 'A matching premise, an ordering step and a fill-in blank each score the row points printed in the key. All rows of one unit score the same points (the key prints them); score each row on its own.'),
        ('6. Add the points of the right places.', 'This is the only calculation. There is no subtraction, no floor, no bonus and no scaling. A perfect paper scores %g. A student who answers every place blind scores %.4f points on average (exact %s), not 20: %g of the %g points are closed places.' % (key['total_points'], key['scoring']['blind_total_exact_decimal'], key['scoring']['blind_total_exact'], key['scoring']['closed_points'], key['total_points'])),
        ('7. Check by question.', 'Add the points of each question first, then add the question totals. The most a question can give: %s.' % qt),
        ('8. Unclear writing.', 'Writing that cannot be read, or lies outside the boxes, is not graded: that place scores 0 (the cover says so to the students). The numbers are copied to the sheet by the student; if page and sheet differ, the page counts.'),
        ('9. Do not decide alone.', 'If a written answer looks right but is not the key value, do not change the key. Put the paper aside and ask the instructor.'),
        ('10. Write the total.', 'Write the total in the grade box of the cover page. The question pages stay with the paper as the record.'),
    ]


def disclosures(paper, key):
    out = []
    if paper.get('synthetic'): out.append(SYNTH_LINE + ' Every question, option and answer in this key is an invented placeholder; this set is a test of the tooling and is never delivered.')
    sc = key['scoring']
    out.append('Where the answers on the question pages and on the answer sheet differ, the question pages count; where only the sheet holds an answer, the sheet counts until the marker has looked (scoring module %s, rule sheet_vs_question_page_rule).' % sc['module_version'])
    out.append('Blind chance, exact: a student who answers every place at random scores %s = %.4f points on average. The closed places (%g of %g points) give exactly one fifth of their points, %s = %.4f; the hand-written number and trace places add %s = %.6f. The blind total would be exactly 20 only if all %g points were closed places; here %g are closed, so it is lower.' %
               (sc['blind_total_exact'], sc['blind_total_exact_decimal'], sc['closed_points'], sc['max_points'], sc['blind_closed_exact'], float(sc['blind_closed_exact'].split('/')[0]) / float(sc['blind_closed_exact'].split('/')[1]) if '/' in sc['blind_closed_exact'] else float(sc['blind_closed_exact']),
                sc['blind_number_and_trace_exact'], float(sc['blind_number_and_trace_exact'].split('/')[0]) / float(sc['blind_number_and_trace_exact'].split('/')[1]) if '/' in sc['blind_number_and_trace_exact'] else float(sc['blind_number_and_trace_exact']), sc['max_points'], sc['closed_points']))
    b = sc['blind_simulation']
    out.append('Simulation of %d blind sheets (seed %d): mean %.4f, standard error %.4f, sd %.3f, minimum %g (never below 0).' % (b['sheets'], b['seed'], b['mean'], b['standard_error'], b['sd'], b['minimum']))
    out.append('Row points come from the key (%s); the scoring module v2.0.0 reads one number per unit, so the adapter %s supplies the row points.' % ('key field row_points', 'sen0401_exam_scoring_rows_v1_0_0.py'))
    rec = [e for e in key['items'] if e.get('recomputed')]
    if rec: out.append('Code traces recomputed by running the code: %d of %d (%s).' % (sum(1 for e in rec if e['recomputed'].startswith('recomputed')), len(rec), '; '.join('%s %s' % (e['label'], e['recomputed'].split(':')[0]) for e in rec)))
    prov = [e['label'] for e in key['items'] if (load_solutions().get(e['item_key']) or {}).get('provisional')]
    if prov: out.append('PROVISIONAL items (the author reading or a source note must be confirmed by the instructor, see the entry): %s.' % ', '.join(prov))
    out.append('DISCLOSED, NOT FIXED (readability rule R6, abbreviation spelled out at first use): in the fill-in group 4e-4f the abbreviation wtxid stands in a bank entry that is printed before the blank sentence 4e that expands it. The paper is unchanged; the owner decides separately.')
    out.append('Page counts are measured on the LibreOffice export; Word pagination is NOT_MEASURED and may differ.')
    return out


def load_solutions(path=None):
    d = json.load(open(path or SOLUTIONS, encoding='utf8'))
    return {e['key']: e for e in d['items']}


def printed_letter_lines(lines, orig_item, paper_item):
    """v7.2.2: the worked-solution lines of a choice item are written with the letters of the items file; the paper prints the options in another order (balance_letters). Map every item letter in 'Correct answer: X.' and 'Why X is wrong:' to the letter the same option text has on the paper; the 'Why' lines go in the order of the paper letters; every other line stays."""
    oo, po = orig_item['options'], paper_item['options']
    m = {'ABCDE'[i]: 'ABCDE'[po.index(t)] for i, t in enumerate(oo)}
    assert sorted(m.values()) == sorted('ABCDE'[:len(oo)]) and len(set(oo)) == len(oo)
    out, why = [], []
    for ln in lines:
        a = re.match(r'Correct answer: ([A-E])\.(.*)$', ln, re.S)
        w = re.match(r'Why ([A-E]) is wrong:(.*)$', ln, re.S)
        if a: out.append('Correct answer: %s.%s' % (m[a.group(1)], a.group(2)))
        elif w: why.append(('Why %s is wrong:%s' % (m[w.group(1)], w.group(2)), m[w.group(1)])); out.append(None)
        else: out.append(ln)
    ws = iter(sorted(why, key=lambda x: x[1]))
    return [next(ws)[0] if ln is None else ln for ln in out]


def original_items(paper):
    auth, _ = E.load_authored(paper['items_path'], paper['chapters'])
    return {i['key']: i for i in auth}


def write_key_docx(paper, key, path, note=''):
    SOL = load_solutions(); doc = Document(); f = paper['form']; ORIG = original_items(paper); PIT = {i['key']: i for i in paper['items']}
    st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(10); _set_fonts(st.element.get_or_add_rPr(), FONT)
    sec = doc.sections[0]; _page_setup(sec, 15.0); sec.top_margin = Mm(12)
    CFG_save = dict(CFG); set_cfg('compact10')
    _footer(sec, 'SEN0401 midterm v%d key  -  form code %s%s' % (paper['version'], f['code'], '  -  SYNTHETIC' if paper.get('synthetic') else ''))
    p = doc.add_paragraph(); _fmt(p, 14, 2.0); _font(p.add_run('SEN0401 midterm v%d - ANSWER KEY (for the grader, not for students)' % paper['version']), FONT, 12, True)
    if paper.get('synthetic'):
        p = doc.add_paragraph(); _fmt(p, 12, 3.0); _font(p.add_run(SYNTH_LINE), FONT, 10, True)
    p = doc.add_paragraph(); _fmt(p, 11.5, 4.0)
    _font(p.add_run('Form code %s. Seed %d. Chapters %s. %g points in all. %s' % (f['code'], f['seed'], ', '.join(map(str, paper['chapters'])), key['total_points'], note)), FONT, 10)
    p = doc.add_paragraph(); _fmt(p, 15, 5.0, keep_next=True); _font(p.add_run('How to grade'), FONT, 13, True)
    for head, text in how_to_grade_lines(key):
        p = doc.add_paragraph(); _fmt(p, 12.5, 5.0)
        _font(p.add_run(head + ' '), FONT, 10.5, True); _font(p.add_run(text), FONT, 10.5)
    p = doc.add_paragraph(); _fmt(p, 12, 0.0); p.add_run().add_break(WD_BREAK.PAGE)
    p = doc.add_paragraph(); _fmt(p, 14, 3.0, keep_next=True); _font(p.add_run('The answers, in the order of the printed paper'), FONT, 12, True)
    P = {pl['label']: pl for pl in key['scoring']['places']}
    for e in key['items']:
        p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=34, first=-34, tabs=(34,), keep_next=True)
        _font(p.add_run('%s' % e['label']), FONT, 10, True)
        _font(p.add_run('\t%s   %s points   chapters %s   Bloom %d   [%s]' % (e['type'], _pts(e['points']), ','.join(map(str, e['chapters'])), e['bloom'], e['item_key'])), FONT, 10)
        last = list(e['answer'])[-1]
        for k, v in e['answer'].items():
            if isinstance(v, dict): s_ = 'value %s %s (exact)' % (v['value'], v['unit'])
            else: s_ = str(v)
            if e['type'] in ('Matching', 'Ordering'): extra = '   (%s points)' % _pts(e['row_points'][k])
            elif e['type'] == 'FillBlankGroup': extra = '   (%s points; the entry: %s)' % (_pts(e['points_per_blank'][k]), e['blank_meaning'][k])
            else: extra = '   (%s points)' % _pts(e['points'])
            if e.get('recomputed') and k == last: extra += '   [%s]' % e['recomputed']
            p = doc.add_paragraph(); _fmt(p, 11.5, 0.0 if k != last else 2.0, left=100, first=-54, tabs=(100,), keep_next=True)
            _font(p.add_run('place %s\t' % k), FONT, 10); _font(p.add_run(s_), FONT, 10, True); _font(p.add_run(extra), FONT, 10)
        sol = SOL.get(e['item_key'])
        if sol is None: raise ValueError('no worked solution for item %s' % e['item_key'])
        if sol.get('provisional'):
            p = doc.add_paragraph(); _fmt(p, 11.5, 2.0, left=34, keep_next=True); _font(p.add_run('PROVISIONAL. ' + re.sub(r'^\s*PROVISIONAL\.\s*', '', sol.get('disclosure') or '')), FONT, 9.5, True)
        for lab in sol['lines_by_label']:
            if len(sol['lines_by_label']) > 1:
                p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=34, keep_next=True); _font(p.add_run('Worked solution, place %s' % lab), FONT, 9.5, True)
            else:
                p = doc.add_paragraph(); _fmt(p, 11.5, 1.0, left=34, keep_next=True); _font(p.add_run('Worked solution'), FONT, 9.5, True)
            ls = sol['lines_by_label'][lab]
            if e['type'] in CHOICE: ls = printed_letter_lines(ls, ORIG[e['item_key']], PIT[e['item_key']])
            for li, line in enumerate(ls):
                p = doc.add_paragraph(); _fmt(p, 11.0, 0.0 if li < len(ls) - 1 else 6.0, left=46, first=-12, tabs=(46,), keep_next=li < len(ls) - 1)
                _font(p.add_run('-\t' + line), FONT, 9.5)
    p = doc.add_paragraph(); _fmt(p, 14, 3.0, keep_next=True); _font(p.add_run('DISCLOSURES (for the grader and the instructor)'), FONT, 11, True)
    for line in disclosures(paper, key):
        p = doc.add_paragraph(); _fmt(p, 11.5, 3.0, left=12, first=-12, tabs=(12,)); _font(p.add_run('-\t' + line), FONT, 10)
    CFG.clear(); CFG.update(CFG_save)
    doc.core_properties.author = ''; doc.core_properties.title = 'SEN0401 midterm v%d key%s' % (paper['version'], ' SYNTHETIC' if paper.get('synthetic') else ''); doc.save(path)


# ------------------------------------------------------------------ LibreOffice export and measurement
def export_pdf(docx_path, outdir, profile='/tmp/lo_profile_papers7'):
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


# ------------------------------------------------------------------ the answer sheet (ONE page, choice-type answers only)
def sheet_units(paper):
    """The unit list of the sheet module v7.0.0 (units_from_list): the choice labels as one list (blocks of at most 5), then every matching, ordering and fill-in unit as its own entry, in printed order.
    Numbers and code traces are NOT on the sheet (written by hand on the question pages). The labels are the labels of the key's places."""
    key_labels = {}
    choice = []; others = []
    for s in paper['slots']:
        it = s['item']; n = it['label']; t = it['type']
        if t in CHOICE: choice.append(n)
        elif t == 'Matching': others.append({'type': 'matching', 'labels': ['%s%d' % (n, k + 1) for k in range(len(it['premises']))]})
        elif t == 'Ordering': others.append({'type': 'ordering', 'labels': ['%s%d' % (n, k + 1) for k in range(len(it['steps']))]})
        elif t == 'FillBlankGroup': others.append({'type': 'fill', 'labels': ['%d%s' % (s['q'], s['letters'][b]) for b in range(len(it['blanks']))]})
    return ([{'type': 'choice', 'labels': choice}] if choice else []) + others


def stamp_pdf(path, text, title):
    """A SYNTHETIC stamp in the top margin (between the registration marks, outside every bubble area) and the PDF title/subject; the page count stays 1."""
    import io
    from pypdf import PdfReader, PdfWriter
    from reportlab.pdfgen import canvas as cv
    from reportlab.lib.pagesizes import A4
    buf = io.BytesIO(); c = cv.Canvas(buf, pagesize=A4); c.setFont('Helvetica-Bold', 7); c.drawCentredString(A4[0] / 2, A4[1] - 3.2 * 72 / 25.4 - 5, text); c.save(); buf.seek(0)
    r = PdfReader(path); w = PdfWriter(); pg = r.pages[0]; pg.merge_page(PdfReader(buf).pages[0]); w.add_page(pg)
    w.add_metadata({'/Title': title, '/Subject': text, '/Author': ''})
    with open(path, 'wb') as fh: w.write(fh)


def render_sheet(paper, path, paper_docx):
    """The answer sheet from the sheet module v7.0.0: ONE page; choice, matching, ordering and fill-in answers only (five alternatives each). Returns (pages, layout)."""
    boxes = SB.boxes_from_paper(paper_docx, 2); spec = dict(paper_kind='Midterm' if paper['kind'] == 'midterm' else 'Makeup', paper_version=paper['version'], form_code=paper['form']['code'], units=SV.units_from_list(sheet_units(paper)), numbers=SV.numbers_from_list(boxes))
    paper['sheet_boxes_from_paper'] = boxes
    layout = SV.build_layout(spec)
    layout['form_code'] = paper['form']['code']; layout['form_letter'] = paper['form']['letter']
    SV.render(layout, path)
    if paper.get('synthetic'):
        layout['synthetic'] = True; layout['disclosure'] = SYNTH_LINE
        stamp_pdf(path, 'Synthetic input - not a real exam - never delivered', 'SEN0401 answer sheet v7 SYNTHETIC')
    return pdf_pages(path), layout
