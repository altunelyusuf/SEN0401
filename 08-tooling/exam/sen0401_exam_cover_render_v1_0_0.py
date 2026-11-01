"""SEN0401 exam cover page renderer, version 1.0.0.

Fills the Istanbul Kultur University exam cover page (the owner's template) for SEN0401 and SEN0414 midterm and make-up exams.
The look is the TEMPLATE'S OWN: the renderer deep-copies the template's body (logo, name boxes, information table, floating grade table,
instruction list, outcome table, cheating warning) and changes only text and the number of rows and columns. No new style is invented.

    cover(doc, course_code, course_name, exam_title, term, year, date_time, duration, instructor, questions, outcomes, instructions)

  doc           a python-docx Document (use new_document() for a stand-alone cover, or any Document: missing styles and the bullet
                numbering are copied from the template)
  date_time     text, or None / '' for the marked fill-in line (the owner has not given the date)
  questions     list of (label, points, is_bonus), e.g. [('1', 25, False), ..., ('5', 10, True)]
  outcomes      list, one entry per question, of learning-outcome numbers (ints) taken from the course's outcomes ontology file;
                pass outcomes_ttl=PATH to check every number against that file (unknown number -> ValueError)
  instructions  list of items (str, or list of (text, bold) pairs); None gives default_instructions()
  Keyword options: program_outcomes (list per question, default marked fill-in blanks: the program outcome numbers of our courses are
  not in our sources, so none is invented), own_section (True: the cover becomes its own section with the template's page margins, for
  a cover placed in front of a paper with other margins), template (path).

The template's cheating WARNING is copied unchanged (the template is English, so it stays English).
Run this file directly to see a self-test (no file written).  Word itself is not available here: the page count is measured on LibreOffice.
"""
import copy, os, re, sys
import docx
from docx.oxml.ns import qn
from lxml import etree

VERSION = '1.0.0'
TEMPLATE = '/home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx'
W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
# body indexes of the template's elements (checked at run time against the texts)
I_DEPT, I_COURSE, I_TITLE, I_NAMES, I_INFO, I_INSTR_HEAD = 0, 1, 2, 4, 6, 7
I_LIST_FIRST, I_LIST_LAST, I_OUTCOME, I_WARN = 9, 14, 15, 16


def default_instructions():
    b = lambda *p: list(p)
    return [
        'Write your name and your student identity number in the boxes above and on the answer sheet before starting the test.',
        b(('The answers are given on the ', False), ('separate answer sheet, which is read by a machine', True),
          ('. Use a dark (black or blue) pen and ', False), ('fill each chosen mark completely', True),
          ('. To cancel an answer, cross its mark out with an X, then fill the mark you now choose. Do not use correction fluid.', False)),
        'Write only inside the boxes and marks of the answer sheet. You may use the blank areas of the question pages for scratch work; do not use any additional scratch paper.',
        b(('Writing that is unclear or outside the boxes ', False), ('may not be read and will not be graded', True), ('.', False)),
        b(('Allowed on the table: ', False), ('the question paper, the answer sheet, a pen and an eraser', True),
          (', and: ______________________________ (instructor to fill in, for example a calculator, a note sheet, or nothing). '
           'Everything else should be cleared. ', False), ('Do not share your belongings', True), (' with other students during the exam.', False)),
        b(('Be particularly aware that the ', False), ('use or the presence', True), (' of cell phones, laptops, or other networked devices is ', False),
          ('FORBIDDEN', True), (' and will be considered a ', False), ('cheating attempt', True), ('.', False)),
        b(('You are ', False), ('not allowed to communicate with other students', True),
          (' even for requesting stationery material such as pen, pencil, eraser, etc., unless authorized explicitly by the instructor.', False)),
    ]


def load_outcome_numbers(ttl_path):
    """{number: full statement} from an outcomes file (CASE items with humanCodingScheme "LO-n"). Read only."""
    txt = open(ttl_path, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'humanCodingScheme\s+"LO-(\d+)"\s*;.*?case:fullStatement\s+"((?:[^"\\]|\\.)*)"', txt, re.S):
        out[int(m.group(1))] = m.group(2)
    return out


def new_document(template=TEMPLATE):
    """A Document that starts from the template (styles, numbering, page setup, logo part), with the body emptied."""
    d = docx.Document(template)
    body = d.element.body
    for el in list(body):
        if el.tag != qn('w:sectPr'):
            body.remove(el)
    return d


# ---------------------------------------------------------------- helpers on the XML
def _w(tag): return '{%s}%s' % (W, tag)


def _rpr_of(p):
    r = p.find('.//' + _w('r'))
    rp = r.find(_w('rPr')) if r is not None else None
    return copy.deepcopy(rp) if rp is not None else etree.Element(_w('rPr'))


def _set_bold(rpr, bold):
    for t in ('b', 'bCs'):
        for e in rpr.findall(_w(t)): rpr.remove(e)
    if bold:
        # schema order: rFonts first, then b, bCs
        pos = 1 if rpr.find(_w('rFonts')) is not None else 0
        rpr.insert(pos, etree.Element(_w('bCs')))
        rpr.insert(pos, etree.Element(_w('b')))


def set_text(p, segments, rpr=None):
    """Replace all runs of paragraph p by runs holding segments [(text, bold)], run properties copied from the paragraph's first run."""
    if isinstance(segments, str): segments = [(segments, None)]
    base = rpr if rpr is not None else _rpr_of(p)
    for e in list(p):
        if e.tag != _w('pPr'): p.remove(e)
    for text, bold in segments:
        r = etree.SubElement(p, _w('r'))
        rp = copy.deepcopy(base)
        if bold is not None: _set_bold(rp, bold)
        r.append(rp)
        t = etree.SubElement(r, _w('t'))
        t.text = text
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')


def _ptext(el): return el.xpath('string(.)')


def _cells(tr): return tr.findall(_w('tc'))


def _cell_p(tc): return tc.find(_w('p'))


def _row_set_height(tr, h):
    trpr = tr.find(_w('trPr'))
    th = trpr.find(_w('trHeight')) if trpr is not None else None
    if th is not None: th.set(_w('val'), str(h))


def _ensure_styles_and_numbering(doc, tdoc):
    have = {s.get(_w('styleId')) for s in doc.styles.element.findall(_w('style'))}
    for s in tdoc.styles.element.findall(_w('style')):
        sid = s.get(_w('styleId'))
        if sid in ('TableGrid', 'ListParagraph', 'NormalWeb') and sid not in have:
            doc.styles.element.append(copy.deepcopy(s))
    # document defaults and the Normal style, so that a cover placed in a foreign document keeps its spacing and fonts
    tdef, ddef = tdoc.styles.element.find(_w('docDefaults')), doc.styles.element.find(_w('docDefaults'))
    if tdef is not None and ddef is not None and etree.tostring(tdef) != etree.tostring(ddef):
        ddef.getparent().replace(ddef, copy.deepcopy(tdef))
    tn_, dn_ = [[x for x in d_.styles.element.findall(_w('style')) if x.get(_w('styleId')) == 'Normal'] for d_ in (tdoc, doc)]
    if tn_ and dn_ and etree.tostring(tn_[0]) != etree.tostring(dn_[0]):
        dn_[0].getparent().replace(dn_[0], copy.deepcopy(tn_[0]))
    # bullet numbering: numId 31 of the template
    try:
        dn = doc.part.numbering_part.element
    except Exception:
        dn = None
    tn = tdoc.part.numbering_part.element
    tnum = [n for n in tn.findall(_w('num')) if n.get(_w('numId')) == '31'][0]
    if dn is not None and any(n.get(_w('numId')) == '31' for n in dn.findall(_w('num'))):
        return '31'
    if dn is None:
        return None
    tabs = [a for a in tn.findall(_w('abstractNum')) if a.get(_w('abstractNumId')) == tnum.find(_w('abstractNumId')).get(_w('val'))][0]
    used = [int(a.get(_w('abstractNumId'))) for a in dn.findall(_w('abstractNum'))]
    usedn = [int(n.get(_w('numId'))) for n in dn.findall(_w('num'))]
    new_abs, new_num = (max(used) + 1 if used else 1), (max(usedn) + 1 if usedn else 1)
    a = copy.deepcopy(tabs); a.set(_w('abstractNumId'), str(new_abs))
    for nsid in a.findall(_w('nsid')) + a.findall(_w('tmpl')): a.remove(nsid)
    first_num = dn.find(_w('num'))
    (first_num.addprevious(a) if first_num is not None else dn.append(a))
    n = copy.deepcopy(tnum); n.set(_w('numId'), str(new_num)); n.find(_w('abstractNumId')).set(_w('val'), str(new_abs))
    dn.append(n)
    return str(new_num)


# ---------------------------------------------------------------- the renderer
def cover(doc, course_code, course_name, exam_title, term, year, date_time, duration, instructor,
          questions, outcomes, instructions=None, program_outcomes=None, own_section=False,
          template=TEMPLATE, outcomes_ttl=None, dept='Department of Computer Engineering'):
    if len(outcomes) != len(questions):
        raise ValueError('outcomes needs one entry per question (%d questions, %d entries)' % (len(questions), len(outcomes)))
    if outcomes_ttl:
        known = load_outcome_numbers(outcomes_ttl)
        for q, los in zip(questions, outcomes):
            for n in los:
                if n not in known:
                    raise ValueError('learning outcome %s (question %s) is not in %s' % (n, q[0], outcomes_ttl))
    tdoc = docx.Document(template)
    tb = [e for e in tdoc.element.body if e.tag != qn('w:sectPr')]
    sect = tdoc.element.body.find(qn('w:sectPr'))
    # guard: the template must still be the page this renderer was written for
    assert 'Department of Computer Engineering' in _ptext(tb[I_DEPT]) and _ptext(tb[I_INSTR_HEAD]).strip() == 'INSTRUCTIONS' \
        and _ptext(tb[I_WARN]).startswith('WARNING'), 'template layout is not the expected one'
    els = [copy.deepcopy(e) for e in tb]
    numid = _ensure_styles_and_numbering(doc, tdoc)

    # logo: re-point the picture to an image part of the target document
    blip = els[I_DEPT].find('.//{http://schemas.openxmlformats.org/drawingml/2006/main}blip')
    if blip is not None:
        blob = tdoc.part.related_parts[blip.get('{%s}embed' % R)].blob
        rid, _img = doc.part.get_or_add_image(io_bytes(blob))
        blip.set('{%s}embed' % R, rid)
    for p in els[I_DEPT].findall('.//' + _w('p')):
        if _ptext(p).strip() == 'Department of Computer Engineering': set_text(p, dept)
    set_text(els[I_COURSE], '%s %s' % (course_code, course_name))
    set_text(els[I_TITLE], exam_title)

    # student boxes (spelled out: identity number)
    rows = els[I_NAMES].findall(_w('tr'))
    set_text(_cell_p(_cells(rows[1])[0]), [('Student Identity Number   :', None)])

    # information table
    info = els[I_INFO]
    irows = info.findall(_w('tr'))
    fill = '____ / ____ / %s   ____ : ____  (fill in)' % year.split('-')[0]
    values = {'Academic Year': year, 'Term': term, 'Date & Time': date_time or fill,
              'Duration': duration, 'Instructor': instructor}
    for tr in irows:
        cs = _cells(tr)
        label = _ptext(cs[0]).strip()
        if label in values:
            p = _cell_p(cs[2]); rpr = _rpr_of(p)
            set_text(p, values[label], rpr)
    # the template's information table is 675 twips wider than the text width (it overhangs the right margin on the render):
    # take the excess from the value column so that every table stays inside the margins
    info.find(_w('tblPr')).find(_w('tblW')).set(_w('w'), '9639')
    info.find(_w('tblGrid')).findall(_w('gridCol'))[2].set(_w('w'), '4276')
    for tr in irows:
        _cells(tr)[2].find(_w('tcPr')).find(_w('tcW')).set(_w('w'), '4276')
    # keep the floating grade table (and its thick border) inside the right margin
    tp = info.find('.//' + _w('tblpPr'))
    if tp is not None: tp.set(_w('tblpX'), str(int(tp.get(_w('tblpX'))) - 140))
    # grade table (nested in the first row's last cell): header, one row per question, total
    nested = info.findall('.//' + _w('tbl'))[0]
    grows = nested.findall(_w('tr'))
    head, qrow_t, total = grows[0], grows[2], grows[4]
    for e in grows[1:]: nested.remove(e)
    maxsum = sum(p for _l, p, b in questions if not b)
    bonus = sum(p for _l, p, b in questions if b)
    for label, pts, is_bonus in questions:
        tr = copy.deepcopy(qrow_t); _row_set_height(tr, 330)
        c = _cells(tr)
        set_text(_cell_p(c[0]), '%s (bonus)' % label if is_bonus else label)
        set_text(_cell_p(c[1]), '           /%d' % pts)
        nested.append(tr)
    tr = copy.deepcopy(total); _row_set_height(tr, 480)
    c = _cells(tr)
    set_text(_cell_p(c[1]), '/%d%s' % (maxsum, ' + bonus' if bonus else ''))
    nested.append(tr)
    # widen the label column a little so that '5 (bonus)' fits
    grid = nested.find(_w('tblGrid')).findall(_w('gridCol'))
    grid[0].set(_w('w'), '1319'); grid[1].set(_w('w'), '1658')
    for tr in nested.findall(_w('tr')):
        cs = _cells(tr); cs[0].find(_w('tcPr')).find(_w('tcW')).set(_w('w'), '1319'); cs[1].find(_w('tcPr')).find(_w('tcW')).set(_w('w'), '1658')

    # instructions: reuse the template's list paragraphs as models
    models = [els[i] for i in range(I_LIST_FIRST, I_LIST_LAST + 1)]
    model = models[0]
    items = instructions if instructions is not None else default_instructions()
    new_items = []
    for k, it in enumerate(items):
        p = copy.deepcopy(model)
        set_text(p, it, _rpr_of(model))
        if numid and numid != '31':
            p.find(_w('pPr')).find(_w('numPr')).find(_w('numId')).set(_w('val'), numid)
        ppr = p.find(_w('pPr'))
        sp = ppr.find(_w('spacing'))
        if sp is not None: sp.set(_w('line'), '252')
        new_items.append(p)
    # the last item keeps the template's spacing after the list
    sp = new_items[-1].find(_w('pPr')).find(_w('spacing'))
    if sp is not None: sp.set(_w('after'), '120')

    # outcome table: header, learning outcomes, program outcomes (marked fill-in), n question columns
    ot = els[I_OUTCOME]
    orows = ot.findall(_w('tr'))
    nq = len(questions)
    total_w, label_w = 9200, 2300
    qw = (total_w - label_w) // nq
    ot.find(_w('tblPr')).find(_w('tblW')).set(_w('w'), str(label_w + qw * nq))
    g = ot.find(_w('tblGrid'))
    for e in list(g): g.remove(e)
    for w in [label_w] + [qw] * nq:
        e = etree.SubElement(g, _w('gridCol')); e.set(_w('w'), str(w))
    hdr_t, po_t, lo_t = orows[0], orows[1], orows[2]
    def build_row(tmpl, label, vals, first_label_bold=None):
        tr = copy.deepcopy(tmpl)
        cs = _cells(tr)
        first, qcell = cs[0], cs[1]
        for c in cs[1:]: tr.remove(c)
        # drop any page break the template carries in a cell (it would split the page in Word)
        for br in first.findall('.//' + _w('br')):
            if br.get(_w('type')) == 'page': br.getparent().getparent().remove(br.getparent())
        first.find(_w('tcPr')).find(_w('tcW')).set(_w('w'), str(label_w))
        set_text(_cell_p(first), label, _rpr_of(_cell_p(qcell)) if not _ptext(first).strip() else None) if label else None
        for v in vals:
            c = copy.deepcopy(qcell); c.find(_w('tcPr')).find(_w('tcW')).set(_w('w'), str(qw))
            set_text(_cell_p(c), v, _rpr_of(_cell_p(qcell)))
            tr.append(c)
        return tr
    for e in orows: ot.remove(e)
    ot.append(build_row(hdr_t, 'Question (Q)', ['Q%s' % q[0] for q in questions]))
    ot.append(build_row(lo_t, 'Learning Outcomes', [', '.join(str(n) for n in los) for los in outcomes]))
    po = program_outcomes or [None] * nq
    ot.append(build_row(po_t, 'Program Outcomes', [', '.join(str(n) for n in x) if x else '____' for x in po]))
    wind = els[I_WARN].find(_w('pPr')).find(_w('ind'))
    wind.set(_w('right'), '150')   # the warning's frame sat 4 points outside the right margin
    seq = els[0:9] + new_items + [ot, els[I_WARN]]
    sec = doc.element.body.find(qn('w:sectPr'))
    for e in seq: sec.addprevious(e)
    if own_section:
        p = etree.Element(_w('p')); ppr = etree.SubElement(p, _w('pPr'))
        sp = etree.SubElement(ppr, _w('spacing')); sp.set(_w('before'), '0'); sp.set(_w('after'), '0'); sp.set(_w('line'), '20'); sp.set(_w('lineRule'), 'exact')
        sc = copy.deepcopy(sect)
        for e in sc.findall(_w('footerReference')) + sc.findall(_w('headerReference')): sc.remove(e)
        ppr.append(sc)
        sec.addprevious(p)
    return doc


def io_bytes(b):
    import io
    return io.BytesIO(b)


if __name__ == '__main__':
    d = new_document()
    qs = [('1', 25, False), ('2', 25, False), ('3', 25, False), ('4', 25, False), ('5', 10, True)]
    cover(d, 'SEN0401', 'Special Topics: Blockchain', 'Midterm Exam', 'Fall', '2026-2027', None, '60 Minutes', 'Dr. Yusuf ALTUNEL', qs,
          [[1], [2], [3], [4], [5]])
    print('self-test: body elements', len(d.element.body))
