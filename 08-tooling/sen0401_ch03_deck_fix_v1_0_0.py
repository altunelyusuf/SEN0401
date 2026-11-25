#!/usr/bin/env python3
"""sen0401_ch03_deck_fix v1_0_0: makes the chapter 3 deck v3.3.0 from the released v3.2.0 (which stays untouched), without adding a slide.
What changes (all of it measured by sen0401_deck_standard_check_v3_1_0.py and cme_material_check_v1_2_0.py afterwards):
  - notes: all 61 notes are rewritten as reader-facing text of 60 to 140 words (sen0401_ch03_deck_notes_v1_0_0.NOTES);
  - D4 / no-analogy: every text block that compared a concept with an everyday thing now states the concept literally (REPL, DROP_SENTENCE); the 'Think of' columns of slides 57 and 58 are removed;
  - slides 38 and 39 teach and use def instead of lambda (no lambda in slide code);
  - titles of at least four words (slides 2, 7, 35; the part dividers carry 'Part N:' as the agenda numbers them);
  - a visual on every slide: arrows on slides 2, 3, 18, 21 and 36, a table on slide 10, a native chart on slide 49;
  - D5: the story shapes of slides 6, 16 and 28 carry the 5N1K in their alt text (never visible);
  - frames that are not code (results, labels, tiles) use Consolas instead of Courier New, so only real code is a code frame.
Usage: sen0401_ch03_deck_fix_v1_0_0.py   (writes 03-materials/ch03/SEN0401_Ch03_BitcoinCore_3e_v3_3_0.pptx; refuses to overwrite)."""
__version__ = "1.0.0"
import ast, copy, os, re, sys
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
from pptx.util import Emu, Pt
from lxml import etree
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_ch03_deck_notes_v1_0_0 as N
REPO = os.path.dirname(HERE)
SRC = os.path.join(REPO, "03-materials", "ch03", "SEN0401_Ch03_BitcoinCore_3e_v3_2_0.pptx")
OUT = os.path.join(REPO, "03-materials", "ch03", "SEN0401_Ch03_BitcoinCore_3e_v3_3_0.pptx")
if os.path.exists(OUT): raise SystemExit("refusing to overwrite " + OUT)
A = "http://schemas.openxmlformats.org/drawingml/2006/main"; P = "http://schemas.openxmlformats.org/presentationml/2006/main"
prs = Presentation(SRC); S = list(prs.slides); assert len(S) == 61
ARROW = None
for sh in S[7].shapes:
    if sh.name == "arrow 1": ARROW = sh._element
assert ARROW is not None

def walk(shs):
    for x in shs:
        if x.shape_type == T.GROUP: yield from walk(x.shapes)
        else: yield x
def norm(t): return re.sub(r"\s+", " ", t).strip()
def set_text(sh, text):
    tf = sh.text_frame; p0 = tf.paragraphs[0]
    runs = p0.runs; assert runs, sh.name
    runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)
    for br in p0._p.findall("{%s}br" % A): p0._p.remove(br)
    for p in tf.paragraphs[1:]: p._p.getparent().remove(p._p)
def next_id(slide): return max(int(i) for i in slide.shapes._spTree.xpath(".//p:cNvPr/@id")) + 1
def add_arrow(slide, x1, y1, x2, y2, name):
    el = copy.deepcopy(ARROW)
    el.find(".//{%s}cNvPr" % P).set("id", str(next_id(slide))); el.find(".//{%s}cNvPr" % P).set("name", name)
    xf = el.find(".//{%s}xfrm" % A); off = xf.find("{%s}off" % A); ext = xf.find("{%s}ext" % A)
    off.set("x", str(min(x1, x2))); off.set("y", str(min(y1, y2))); ext.set("cx", str(abs(x2 - x1))); ext.set("cy", str(abs(y2 - y1)))
    if x2 < x1: xf.set("flipH", "1")
    if y2 < y1: xf.set("flipV", "1")
    slide.shapes._spTree.append(el)
def shape_by_name(slide, name, nth=0):
    hit = [s for s in slide.shapes if s.name == name]; return hit[nth]
def add_table(slide, name, x, y, widths, rows, sz=1000, head="2B2622", body="FFFFFF", ink="2B2622", rh=210000):
    gf = slide.shapes.add_table(len(rows), len(widths), Emu(x), Emu(y), Emu(sum(widths)), Emu(rh * len(rows)))
    gf.name = name; tbl = gf.table
    for i, w in enumerate(widths): tbl.columns[i].width = Emu(w)
    for ri, row in enumerate(rows):
        tbl.rows[ri].height = Emu(rh)
        for ci, txt in enumerate(row):
            c = tbl.cell(ri, ci); c.margin_top = Emu(30000); c.margin_bottom = Emu(30000); c.margin_left = Emu(54864); c.margin_right = Emu(54864)
            c.fill.solid(); c.fill.fore_color.rgb = RGBColor.from_string(head if ri == 0 else body)
            tf = c.text_frame; tf.text = txt; r = tf.paragraphs[0].runs[0]
            r.font.size = Emu(sz * 127); r.font.name = "Calibri"; r.font.bold = (ri == 0 or ci == 0)
            r.font.color.rgb = RGBColor.from_string("FFFFFF" if ri == 0 else ink)
    return gf

# ---- 1. text replacements (analogies, the 5N1K word on slide 2) -----------------------------------------
REPL = dict(N.REPL); REPL[(2, "true stories, each told by 5N1K")] = "true stories, each with a photograph and a source link"
used = set()
for i, s in enumerate(S, 1):
    for sh in walk(s.shapes):
        if not sh.has_text_frame: continue
        t = norm(sh.text_frame.text)
        for (n, old), new in REPL.items():
            if n == i and norm(old) == t:
                set_text(sh, new); used.add((n, old)); break
        else:
            d = N.DROP_SENTENCE.get(i)
            if d and d in sh.text_frame.text and i not in (38,):
                set_text(sh, sh.text_frame.text.replace(d, "")); used.add(("drop", i))
missing = [k for k in REPL if k not in used]
if missing: raise SystemExit("not found: %r" % missing[:5])

# ---- 2. titles ------------------------------------------------------------------------------------------
def title_shape(slide):
    for sh in slide.shapes:
        tx = sh.text_frame.text.strip() if sh.has_text_frame else ""
        if len(tx) > 2 and not re.match(r"^\d+\s*/\s*\d+$", tx) and not any(r.font.name == "Courier New" for p in sh.text_frame.paragraphs for r in p.runs): return sh
for n, t in list(N.TITLES.items()) + list(N.PART_TITLES.items()):
    set_text(title_shape(S[n - 1]), t)

# ---- 3. slide 38 and 39: def instead of lambda ----------------------------------------------------------
s38 = S[37]
set_text(shape_by_name(s38, "TextBox 3"), "The helper that the next code uses, written with def")
set_text(shape_by_name(s38, "TextBox 5"), "A def writes a small function once and names it for reuse")
tiles = [sh for sh in s38.shapes if sh.name.startswith("tile ") and sh.name != "tile label"]
labels = [sh for sh in s38.shapes if sh.name == "tile label"]
new_tiles = [("def", "starts a function and gives it a name"), ("sat", "the name, used later to call it"), ("(v):", "the one input in brackets, then a colon"), ("return round(v * 10**8)", "the value it hands back")]
assert len(tiles) == 4 and len(labels) == 4
for sh, lb, (a, b) in zip(tiles, labels, new_tiles):
    set_text(sh, a); set_text(lb, b); sh.name = "tile " + a
for sh in s38.shapes:
    if sh.name == "lambda table": sh.name = "def table"
set_text(shape_by_name(s38, "def head"), "The whole function, written with def")
rd = [sh for sh in s38.shapes if sh.name == "reading"]
for sh, t in zip(rd, ["▪  A def writes a function once, so that it can be used wherever the job repeats; the lines under it are indented.",
                      "▪  Here sat turns bitcoin into satoshis: sat(0.0002) gives 20,000, and the next slide calls it for each output.",
                      "▪  The word return hands back the value; the name sat stands for the whole function."]): set_text(sh, t)
s39 = S[38]
c1 = shape_by_name(s39, "code 1"); p = c1.text_frame.paragraphs
assert p[1].text.startswith("sat = lambda")
# the second paragraph becomes the two lines of the def; every run keeps the font of the paragraph
p1 = p[1]._p; rpr = copy.deepcopy(p1.find("{%s}r" % A).find("{%s}rPr" % A))
for r in p1.findall("{%s}r" % A): p1.remove(r)
def run(par, text):
    r = etree.SubElement(par, "{%s}r" % A); r.append(copy.deepcopy(rpr)); t = etree.SubElement(r, "{%s}t" % A); t.text = text
run(p1, "def sat(v):")
p2 = copy.deepcopy(p1)
for r in p2.findall("{%s}r" % A): p2.remove(r)
run(p2, "    return round(v * 10**8)"); p1.addnext(p2)
line = 161543
c1.height = Emu(c1.height + line)
for sh in s39.shapes:
    if sh.name == "Rounded Rectangle 7": sh.height = Emu(sh.height + line)
    elif sh.left < 5800000 and sh.top >= 1800000: sh.top = Emu(sh.top + line)

# ---- 4. slides 57 and 58: the 'Think of' column goes ----------------------------------------------------
for n in (57, 58):
    for sh in S[n - 1].shapes:
        if sh.has_table:
            tbl = sh.table; assert tbl.cell(0, 3).text_frame.text == "Think of"
            cw = int(tbl.columns[3].width)
            for tr in tbl._tbl.tr_lst: tr.remove(tr.tc_lst[3])
            grid = tbl._tbl.tblGrid; grid.remove(grid.findall("{%s}gridCol" % A)[3])
            tbl.columns[1].width = Emu(int(tbl.columns[1].width) + cw // 2); tbl.columns[2].width = Emu(int(tbl.columns[2].width) + cw - cw // 2)

# ---- 5. a visual on every slide -------------------------------------------------------------------------
s2 = S[1]
rr = [sh for sh in s2.shapes if sh.name.startswith("Rounded Rectangle") and sh.has_text_frame and re.match(r"^\d\. ", sh.text_frame.text)]
assert len(rr) == 9
for row in range(3):
    for col in range(2):
        a = rr[row * 3 + col]; b = rr[row * 3 + col + 1]
        y = a.top + a.height // 2; add_arrow(s2, a.left + a.width, y, b.left, y, "route arrow %d" % (row * 2 + col + 1))
s3 = S[2]
ov = [sh for sh in s3.shapes if sh.name.startswith("Oval")]; assert len(ov) == 6
for k in range(5):
    x = ov[k].left + ov[k].width // 2; add_arrow(s3, x, ov[k].top + ov[k].height, x, ov[k + 1].top, "question arrow %d" % (k + 1))
s10 = S[9]
for sh in list(s10.shapes):
    if sh.name == "reading": sh._element.getparent().remove(sh._element)
add_table(s10, "fork table", 457200, 3640000, [1600200, 1211580, 1211580],
          [["Change", "Old nodes", "New nodes"], ["Soft fork: tighter rules", "keep following", "follow the chain"], ["Incompatible change", "stay on the old chain", "move to the new chain"]])
s18 = S[17]
tt = [sh for sh in s18.shapes if sh.name.startswith("trust title")]; assert len(tt) == 3
for k in range(2):
    y = tt[k].top + tt[k].height // 2; add_arrow(s18, tt[k].left + tt[k].width, y, tt[k + 1].left, y, "check arrow %d" % (k + 1))
s21 = S[20]
src = [shape_by_name(s21, "source %d" % k) for k in range(3)]
x = src[0].left + src[0].width // 2
add_arrow(s21, x, src[2].top, x, src[1].top + src[1].height, "overrides arrow 1"); add_arrow(s21, x, src[1].top, x, src[0].top + src[0].height, "overrides arrow 2")
s36 = S[35]
cards = [sh for sh in s36.shapes if sh.name.startswith("call card")]; ro = shape_by_name(s36, "read only"); assert len(cards) == 2
for k, c in enumerate(cards):
    x = c.left + c.width // 2; add_arrow(s36, x, c.top + c.height, x, ro.top, "read-only arrow %d" % (k + 1))
s49 = S[48]
bars = [sh for sh in s49.shapes if sh.name == "subsidy chart bar"]; colour = bars[0].fill.fore_color.rgb
for sh in list(s49.shapes):
    if sh.name.startswith("subsidy chart"): sh._element.getparent().remove(sh._element)
cd = CategoryChartData(); cd.categories = ["0", "210,000", "420,000", "630,000", "840,000", "1,050,000", "1,260,000"]
cd.add_series("Block subsidy in bitcoins", [50, 25, 12.5, 6.25, 3.125, 1.5625, 0.78125])
gf = s49.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Emu(457200), Emu(1481328), Emu(4389120), Emu(1790000), cd); gf.name = "subsidy chart"
ch = gf.chart; ch.has_legend = False; ch.has_title = False
pl = ch.plots[0]; pl.gap_width = 60; pl.has_data_labels = True
dl = pl.data_labels; dl.font.size = Pt(9); dl.font.name = "Calibri"; dl.number_format = "General"; dl.number_format_is_linked = False; dl.position = XL_LABEL_POSITION.OUTSIDE_END
pl.series[0].format.fill.solid(); pl.series[0].format.fill.fore_color.rgb = colour
ch.value_axis.visible = False; ch.value_axis.has_major_gridlines = False
ch.category_axis.tick_labels.font.size = Pt(8); ch.category_axis.tick_labels.font.name = "Calibri"

# ---- 6. the 5N1K of the three stories, in the alt text of the story shapes (never on the slide) ------------
STORY = {
6: ["WHEN and WHERE: 8 January 2009, on the metzdowd.com cryptography mailing list, with the program on SourceForge",
    "WHO and WHAT: Satoshi Nakamoto announced Bitcoin 0.1 on the mailing list",
    "HOW: a Windows program that anyone could download and run, five days after the first block was mined",
    "WHY: only running software could start the network, so the program came before any written rule",
    "WHAT followed: Satoshi wrote that the core design was set in stone once 0.1 was out"],
16: ["WHEN and WHERE: 13 September 2021, in the guix.sigs repository beside bitcoin/bitcoin on GitHub",
     "WHO and WHAT: Bitcoin Core released version 22.0, the first release built with Guix, a build system that Carl Dong wrote",
     "HOW: anyone can rebuild the program from the tagged source and get the same file, bit for bit",
     "HOW and WHO: each independent builder signs the hashes of what they built, and the signatures are collected in guix.sigs",
     "WHY: a download is checked against many builders and not against one person's word"],
28: ["WHEN and WHERE: 7 April 2014, in the public bitcoin/bitcoin repository on GitHub",
     "WHO and WHAT: Gavin Andresen passed the lead-maintainer role of Bitcoin Core to Wladimir van der Laan",
     "WHY: Andresen wanted to focus on protocol work, and a reference implementation cannot wait for one person",
     "HOW: every change is reviewed in the open on GitHub, whoever holds the role",
     "WHAT it shows: the reference implementation is an institution, not a person"]}
for n, texts in STORY.items():
    boxes = [sh for sh in S[n - 1].shapes if sh.has_text_frame and sh.name.lower().startswith("story")]
    assert len(boxes) >= 5, (n, len(boxes))
    for sh, d in zip(boxes, texts): sh._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", d)

# ---- 7. frames that are not code do not use the code font -----------------------------------------------
changed = 0
for s in S:
    for sh in walk(s.shapes):
        if not sh.has_text_frame or sh.name == "chip" or sh.name.startswith("code"): continue
        runs = [r for p in sh.text_frame.paragraphs for r in p.runs]
        if not any(r.font.name == "Courier New" for r in runs): continue
        try: ast.parse(sh.text_frame.text); continue
        except SyntaxError: pass
        for r in runs:
            if r.font.name == "Courier New": r.font.name = "Consolas"
        changed += 1

# ---- 8. notes -------------------------------------------------------------------------------------------
for i, s in enumerate(S, 1):
    nw = len(N.NOTES[i].split()); assert 60 <= nw <= 140, (i, nw)
    s.notes_slide.notes_text_frame.text = N.NOTES[i]
prs.core_properties.version = "3.3.0"
prs.save(OUT)
print("wrote", os.path.relpath(OUT, REPO), "| non-code frames moved to Consolas:", changed)
