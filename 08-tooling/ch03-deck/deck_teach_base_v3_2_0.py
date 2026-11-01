#!/usr/bin/env python3
"""Chapter 3 deck v3.2.0, part 1 (a NEW tool file; task TK_Ch03_DeckTeach_Build): helpers and the repairs of the 42 existing slides of v3.1.0.
(1) no text run below 9 pt: captions and the 8-column bit strip (slide 8) and the chart labels (slides 36, 39); results 10 pt;
(2) a result that does not fit its column in one line at 10 pt gets the full content width (x 50 to 950 units) under the code and the explanation; no expression is shortened;
(3) slide 24: the result card moves up under the code (the gap of 0.44 in is closed) and the right-hand flow becomes a row under the result;
(4) the three stories are told as sentences (no label words), the picture, the credit and the live source link stay.
Units: 1 unit = 1/100 inch (the slide is 1000 x 562.5 units). Reuses the chapter 6 Friday helpers (08-tooling/ch06-deck)."""
__version__ = "3.2.0"
import copy, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "ch06-deck"))
from deck_lib_v2_3_0 import *
from deck_enhance_v2_3_0 import P, R, T, A, settext, delete
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from lxml import etree

CHIP = "F2A860"
LAST = ("bold", "")


def by_name(s, name): return [sh for sh in s.shapes if sh.name == name]
def one(s, name):
    r = by_name(s, name); assert len(r) == 1, (name, len(r)); return r[0]
def u(v): return int(round(v * U))
def top(sh): return sh.top / U
def left(sh): return sh.left / U
def wid(sh): return sh.width / U
def hei(sh): return sh.height / U
def setgeo(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = Emu(u(x))
    if y is not None: sh.top = Emu(u(y))
    if w is not None: sh.width = Emu(u(w))
    if h is not None: sh.height = Emu(u(h))


def raise_runs(sh, minimum=9.0, to=None):
    """every explicit run size below the minimum becomes `to` (default the minimum); returns how many runs changed"""
    n = 0
    tfs = []
    if sh.has_text_frame: tfs.append(sh.text_frame)
    if getattr(sh, "has_table", False) and sh.has_table:
        for row in sh.table.rows:
            for c in row.cells: tfs.append(c.text_frame)
    for tf in tfs:
        for pa in tf.paragraphs:
            for r in pa.runs:
                if r.font.size is not None and r.font.size.pt < minimum:
                    r.font.size = Pt(to or minimum); n += 1
    return n


def set_all_runs(sh, size):
    for pa in sh.text_frame.paragraphs:
        for r in pa.runs: r.font.size = Pt(size)


def chart_min(chart, minimum=900):
    """every font size of a native chart below the minimum (hundredths of a point) is raised to it"""
    n = 0
    for el in chart._chartSpace.iter():
        sz = el.get("sz")
        if sz is not None and el.tag.endswith(("defRPr", "rPr")) and int(sz) < minimum:
            el.set("sz", str(minimum)); n += 1
    return n


def est_h(text, size, width_units, factor=0.5, lh=1.2):
    return est_lines(text, size, width_units, factor) * size * lh / 0.72 / 100 * 100  # in units


# ------------------------------------------------------------------------------------------------------------------------------------------------
# results
# ------------------------------------------------------------------------------------------------------------------------------------------------
def result_text_len(sh): return sum(len(r.text) for pa in sh.text_frame.paragraphs for r in pa.runs)


def fit_right_column(s, limit, keep_min_row=24):
    """shrink the tables (row heights) and charts of the right column so that everything there ends above `limit` units; the reading text below follows its visual"""
    right = sorted([sh for sh in s.shapes if left(sh) >= 635 and 185 <= top(sh) < 500 and not (sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()))], key=top)
    if not right: return
    est_bottom = max(top(sh) + (est_h(sh.text_frame.text, 11, 310, 0.5) + 6 if (sh.has_text_frame and not sh.has_chart) else hei(sh)) for sh in right)
    over = est_bottom - limit
    if over <= 0: return
    vis = [sh for sh in right if sh.has_chart or sh.has_table]
    room = 0
    for sh in vis:
        if sh.has_chart: room += max(0, hei(sh) - 160)
        else: room += sum(max(0, r.height / U - keep_min_row) for r in sh.table.rows)
    assert room >= over, ("cannot fit the right column", over, room)
    f = over / room; shift = 0.0
    for sh in right:
        sh.top = Emu(u(top(sh) - shift))
        if sh.has_chart:
            d = max(0, hei(sh) - 160) * f; sh.height = Emu(u(hei(sh) - d)); shift += d
        elif sh.has_table:
            d = 0
            for r in sh.table.rows:
                cut = max(0, r.height / U - keep_min_row) * f; r.height = Emu(u(r.height / U - cut)); d += cut
            sh.height = Emu(u(hei(sh) - d)); shift += d


def widen_long_results(prs, skip=(24,)):
    """a result whose line does not fit the 5.4 in column at 10 pt: the dark result card gets the full content width under the code and the explanation (x 50 to 950, y 450); the code card closes up around the code"""
    out = []
    for i, s in enumerate(prs.slides, 1):
        for rs in [sh for sh in s.shapes if sh.name.startswith("result ")]:
            set_all_runs(rs, 10)                                          # no result below 10 pt
            room = (rs.width - rs.text_frame.margin_left - rs.text_frame.margin_right) / 12700
            if result_text_len(rs) <= int(room / 6.0) or i in skip: continue
            codes = [sh for sh in s.shapes if sh.name.startswith("code ")]
            cards = [sh for sh in s.shapes if sh.name.startswith("Rounded Rectangle") and sh.fill.type is not None and left(sh) == 50 and abs(wid(sh) - 570) < 1 and top(sh) <= top(rs) <= top(sh) + hei(sh)]
            assert len(cards) == 1, (i, len(cards)); card = cards[0]
            row = hei(rs) + 0.0                                             # the result row that leaves the card
            gap = top(rs) - (top(codes[-1]) + hei(codes[-1]))
            drop = hei(rs) + gap
            setgeo(card, h=hei(card) - drop)
            for sh in s.shapes:                                           # explanation and stamp under the card move up by the freed height
                if left(sh) == 50 and top(sh) > top(card) + hei(card) and sh.name.startswith("TextBox") and not re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): setgeo(sh, y=top(sh) - drop)
            RY, RH = 450.0, 37.0
            back = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(u(50)), Emu(u(RY)), Emu(u(900)), Emu(u(RH))); back.name = "output backdrop"
            back.adjustments[0] = 0.12; back.fill.solid(); back.fill.fore_color.rgb = rgb(CODEBG); back.line.fill.background(); back.shadow.inherit = False
            s.shapes._spTree.remove(back._element); s.shapes._spTree.insert(list(s.shapes._spTree).index(card._element) + 1, back._element)
            setgeo(rs, x=66, y=RY + (RH - hei(rs)) / 2, w=868)
            fit_right_column(s, RY - 8)
            out.append(i)
    return out


def slide24(prs):
    """slide 24: the result card sits directly under the code (no gap), full width; the explanation of the reply stands at the right of the code; the call-and-reply flow becomes a row under the result"""
    s = prs.slides[23]
    card2 = one(s, "Rounded Rectangle 8"); code2 = one(s, "code 2"); rs = one(s, "result 2"); e2 = one(s, "TextBox 12"); stamp = one(s, "TextBox 13"); head = one(s, "TextBox 14")
    set_all_runs(rs, 10)
    setgeo(card2, h=top(code2) + hei(code2) + 10 - top(card2))                        # the code card closes around the code (ends 2.91 in)
    ry = top(card2) + hei(card2) + 6                                                  # 2.97
    back = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Emu(u(50)), Emu(u(ry)), Emu(u(900)), Emu(u(50))); back.name = "output backdrop"
    back.adjustments[0] = 0.1; back.fill.solid(); back.fill.fore_color.rgb = rgb(CODEBG); back.line.fill.background(); back.shadow.inherit = False
    s.shapes._spTree.remove(back._element); s.shapes._spTree.insert(list(s.shapes._spTree).index(card2._element) + 1, back._element)
    setgeo(rs, x=66, y=ry + 8, w=868, h=34)
    setgeo(e2, x=640, y=top(card2) + 4, w=310)                                         # beside the reply code
    setgeo(head, x=50, y=ry + 50 + 12, w=900)
    boxes = [one(s, n) for n in ("Rounded Rectangle 15", "Rounded Rectangle 17", "Rounded Rectangle 19")]
    fy = ry + 50 + 12 + 24; xs = [50, 320, 590]; ws = [250, 250, 360]
    for b, x, w in zip(boxes, xs, ws):
        setgeo(b, x=x, y=fy, w=w, h=58); raise_runs(b, 10)
    for old in (one(s, "Connector 16"), one(s, "Connector 18")): delete(old)
    A(s, "arrow call", 302, fy + 29, 318, fy + 29, ORANGE, 2.0); A(s, "arrow reply", 572, fy + 29, 588, fy + 29, ORANGE, 2.0)
    read = one(s, "TextBox 20"); setgeo(read, x=50, y=fy + 58 + 6, w=900, h=20)
    setgeo(stamp, x=50, y=fy + 58 + 6 + 26, w=900, h=16)
    return s


# ------------------------------------------------------------------------------------------------------------------------------------------------
# slide 8: the 32-bit strip becomes a full-width row so that its cells hold 11 pt without wrapping
# ------------------------------------------------------------------------------------------------------------------------------------------------
def slide8(prs):
    s = prs.slides[7]
    strip, facts, note = one(s, "Table 15"), one(s, "Table 16"), one(s, "TextBox 17")
    setgeo(strip, x=50, y=418, w=900)
    for c in strip.table.columns: c.width = Emu(u(112.5))
    for r in strip.table.rows: r.height = Emu(u(30))
    setgeo(strip, h=60)
    for row in strip.table.rows:
        for c in row.cells:
            for pa in c.text_frame.paragraphs:
                for r in pa.runs: r.font.size = Pt(11)
    for row in facts.table.rows:
        for c in row.cells:
            for pa in c.text_frame.paragraphs:
                for r in pa.runs: r.font.size = Pt(10.5)
    setgeo(facts, y=185)
    setgeo(note, y=top(facts) + hei(facts) + 10, w=310)
    return s


# ------------------------------------------------------------------------------------------------------------------------------------------------
# stories
# ------------------------------------------------------------------------------------------------------------------------------------------------
def story(prs, n, head, paras, lesson, *, lesson_under_picture=False, pic_w=None):
    s = prs.slides[n - 1]
    names = {sh.name: sh for sh in s.shapes}
    labels = [sh for sh in s.shapes if sh.has_text_frame and re.match(r"(WHO|WHAT|WHEN|WHERE|WHY|HOW)\b", sh.text_frame.text)]
    assert len(labels) == 6, (n, len(labels))
    for sh in labels: delete(sh)
    pic = [sh for sh in s.shapes if sh.shape_type == 13][0]
    cap = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("Picture:")][0]
    read = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("READ")][0]
    raise_runs(cap, 9.0); raise_runs(read, 10.0)
    if pic_w:                                                                    # a wide picture keeps its ratio
        ratio = hei(pic) / wid(pic); setgeo(pic, w=pic_w, h=pic_w * ratio); setgeo(cap, w=pic_w, y=top(pic) + hei(pic) + 4)
    tx = left(pic) + wid(pic) + 25; tw = 950 - tx
    hh0 = est_lines(head, 12, tw, 0.56) * 12 * 1.25 / 0.72 + 4
    T(s, "story head", tx, 135, tw, hh0, [P(head, 12, ORANGE, True)]); y = 135 + hh0 + 6
    for p in paras:
        hh = est_lines(p, 12, tw, 0.5) * 12 * 1.25 / 0.72 + 4
        T(s, "story", tx, y, tw, hh, [P(p, 12, INK)]); y += hh + 4
    if lesson_under_picture:
        ly = top(cap) + hei(cap) + 18
        R(s, "lesson", left(pic), ly, wid(pic), 90, fill=SOFT, line=TEAL, paras=[P(lesson, 12, INK, True)], inset=10)
        assert y <= 458, (n, y)
    else:
        ly = y + 4; lh = est_lines(lesson, 12, tw - 20, 0.5) * 12 * 1.25 / 0.72 + 20
        assert ly + lh <= 458, (n, ly, lh)
        R(s, "lesson", tx, ly, tw, lh, fill=SOFT, line=TEAL, paras=[P(lesson, 12, INK, True)], inset=10)
    setgeo(read, x=tx, y=464, w=tw, h=hei(read))
    return s
