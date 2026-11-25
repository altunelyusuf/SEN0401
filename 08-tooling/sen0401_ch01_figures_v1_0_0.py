#!/usr/bin/env python3
"""sen0401_ch01_figures v1.0.0: Chapter 1 deck 3.6.0 -> 3.7.0. Slides 2, 3 and 74 carried a grouped list of cards as their figure; they now carry real figures built from native shapes: slide 2 a route line with one station per part and a bar whose length is the number of slides of the part; slide 3 the six questions joined by arrows to the part that answers each; slide 74 a chain of six stations (the six lines of the summary). Texts and notes are unchanged. Refuses to overwrite. Usage: run in the repository root."""
__version__ = "1.0.0"
import os, sys, copy
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
SRC = "03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_6_0.pptx"; DST = "03-materials/ch01/SEN0401_Ch01_Introduction_3e_v3_7_0.pptx"
if os.path.exists(DST): sys.exit("refuse: " + DST + " exists")
OR, CARD, EDGE, INK, GREY, WHITE = "D97A14", "F2ECE1", "DFD6C7", "2B2622", "6E655C", "FFFFFF"
rgb = lambda h: RGBColor.from_string(h)
p = Presentation(SRC)
def fig(slide):
    return [s for s in slide.shapes if s.shape_type == 6 and s.name == "Figure"][0]
def clear(g, keep=()):
    for i, c in reversed(list(enumerate(list(g.shapes)))):
        if i not in keep: g.shapes._spTree.remove(c._element)
def box(g, shp, x, y, w, h, fill=None, line=None, jump=None):
    s = g.shapes.add_shape(shp, Emu(x), Emu(y), Emu(w), Emu(h))
    if fill: s.fill.solid(); s.fill.fore_color.rgb = rgb(fill)
    else: s.fill.background()
    if line: s.line.color.rgb = rgb(line); s.line.width = Pt(1)
    else: s.line.fill.background()
    s.shadow.inherit = False
    return s
def text(g, x, y, w, h, parts, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.MIDDLE):
    t = g.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h)); f = t.text_frame; f.word_wrap = True
    f.margin_left = f.margin_right = f.margin_top = f.margin_bottom = 0; f.vertical_anchor = anchor
    for i, (s, sz, bold, col, face) in enumerate(parts):
        para = f.paragraphs[0] if i == 0 else f.add_paragraph(); para.alignment = align
        r = para.add_run(); r.text = s; r.font.size = Pt(sz); r.font.bold = bold; r.font.color.rgb = rgb(col); r.font.name = face
    return t
def line(g, x1, y1, x2, y2, col=EDGE, w=2.25, arrow=False):
    c = g.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(x1), Emu(y1), Emu(x2), Emu(y2))
    c.line.color.rgb = rgb(col); c.line.width = Pt(w)
    if arrow:
        ln = c.line._get_or_add_ln(); from lxml import etree
        ln.append(etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd", type="triangle", w="med", len="med"))
    return c
def dot(g, cx, cy, d, n):
    box(g, MSO_SHAPE.OVAL, cx - d // 2, cy - d // 2, d, d, OR, OR)
    text(g, cx - d // 2, cy - d // 2, d, d, [(str(n), 12, True, WHITE, "Cambria")], PP_ALIGN.CENTER)
PARTS = [("Questions and the chapter map", 3, 4), ("Origins", 5, 11), ("Money and price", 12, 27), ("The network", 28, 41),
         ("Wallets and keys", 42, 54), ("A first payment", 55, 63), ("Foundations", 64, 73), ("Summary, resources and close", 74, 76)]
# ---------------- slide 2: route line
s2 = p.slides[1]; g = fig(s2); clear(g, keep=range(16, 25))
x0, y0, pitch, d = 457200, 1280160, 400000, 250000
cx = x0 + d // 2
line(g, cx, y0 + pitch // 2, cx, y0 + pitch * 7 + pitch // 2, EDGE, 3)
for i, (name, a, b) in enumerate(PARTS):
    cy = y0 + pitch * i + pitch // 2; n = b - a + 1
    dot(g, cx, cy, d, i + 1)
    text(g, 880000, cy - 170000, 2750000, 340000, [(name, 11, True, INK, "Calibri")])
    bar = box(g, MSO_SHAPE.ROUNDED_RECTANGLE, 3700000, cy - 95000, n * 108000, 190000, OR, OR)
    text(g, 3700000 + n * 108000 + 70000, cy - 140000, 900000, 280000, [("slides %d-%d" % (a, b), 10, False, GREY, "Calibri")])
# ---------------- slide 3: question -> part that answers it
s3 = p.slides[2]; g = fig(s3); qs = [c.text_frame.text for c in g.shapes if c.has_text_frame and len(c.text_frame.text) > 3]
assert len(qs) == 6, qs
clear(g)
ans = PARTS[1:7]; y0, pitch = 1280160, 520000
text(g, 457200, y0 - 130000, 5300000, 200000, [("Question", 10, True, GREY, "Calibri")]); text(g, 6350000, y0 - 130000, 2300000, 200000, [("Answered in", 10, True, GREY, "Calibri")])
for i, q in enumerate(qs):
    cy = y0 + 330000 + pitch * i
    dot(g, 457200 + 140000, cy, 280000, i + 1)
    text(g, 880000, cy - 220000, 4800000, 440000, [(q, 12, False, INK, "Calibri")])
    line(g, 5800000, cy, 6280000, cy, OR, 2.25, True)
    name, a, b = ans[i]
    box(g, MSO_SHAPE.ROUNDED_RECTANGLE, 6350000, cy - 210000, 2300000, 420000, CARD, EDGE)
    text(g, 6430000, cy - 210000, 2140000, 420000, [(name, 11, True, INK, "Calibri"), ("slides %d-%d" % (a, b), 10, False, GREY, "Calibri")], PP_ALIGN.CENTER)
# ---------------- slide 74: chain of six stations
s74 = p.slides[73]; g = fig(s74); ls = [c.text_frame.text for c in g.shapes if c.has_text_frame and len(c.text_frame.text) > 8]
assert len(ls) == 6, ls
clear(g)
W = 8229600 // 6; ly = 1800000
line(g, 457200 + W // 2, ly, 457200 + W * 5 + W // 2, ly, OR, 3, False)
for i, t in enumerate(ls):
    cx = 457200 + W * i + W // 2
    text(g, cx - W // 2 + 30000, 1330000, W - 60000, 300000, [(ans[i][0], 11, True, INK, "Calibri")], PP_ALIGN.CENTER, MSO_ANCHOR.BOTTOM)
    dot(g, cx, ly, 280000, i + 1)
    text(g, cx - W // 2 + 50000, 2100000, W - 100000, 2300000, [(t, 12, False, INK, "Calibri")], PP_ALIGN.LEFT, MSO_ANCHOR.TOP)
p.save(DST); print("wrote", DST)
