"""deck_kit v3.0.0 (chapter 3) - the drawing kit of the chapter 3 deck 3.0.0 (the same kit as chapter 2's deck 3.0.0, copied as a new file of this chapter): python-pptx only (1.0.2), one smooth light colour scheme (the look of the course page and of the decks of
chapters 5 to 8: cream ground, ink text, orange and teal accents, dark code cards), every text box fitted by the same greedy wrap estimate the deck overlap check uses, refusals
BEFORE the file is written: no text box over 30 words (D2), no code line over 62 characters (D12). A NEW file; nothing earlier is edited."""
__version__ = "3.0.0"
import re
from lxml import etree
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION, XL_LEGEND_POSITION
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

BG, INK, MUTED, ORANGE, TEAL, LINE, CARD, CODE, CODE_TXT, CODE_OR, CODE_OUT, WHITE, SOFT, C_STR, C_NUM = (
    "FAF6EF", "2B2622", "6E655C", "D97A14", "2F6D62", "DFD6C7", "F2ECE1", "23272E", "E6EDF3", "F2A860", "7EE787", "FFFFFF", "EFE6D6", "9ECBFF", "FFD28A")   # the CME palette: band EFE6D6; code colours keyword F2A860, string 9ECBFF, number FFD28A, result 7EE787
SERIF, SANS, MONO = "Cambria", "Calibri", "Courier New"
W_IN, H_IN = 10.0, 5.625
CTX = {"slide": 0}
rgb = lambda h: RGBColor.from_string(h)
words = lambda t: len(t.split())


def est(paras, w, default=12.0, mono=False):
    """height in inches of the paragraphs in a frame w inches wide, the way deck_overlap_check_v1_0_0 estimates it (greedy wrap, 0.5 em proportional / 0.6 em monospace, line 1.2 em)"""
    tot = 0.0
    for p in paras:
        runs = [(p, {})] if isinstance(p, str) else p
        size = max([o.get("size", default) for _, o in runs] or [default]); text = "".join(t for t, _ in runs)
        a = (0.60 if mono else 0.50) * size / 72.0
        lines, cur = 1, 0.0
        if text:
            for wd in text.split(" "):
                wl = len(wd) * a
                if cur == 0: cur = wl
                elif cur + a + wl <= w: cur += a + wl
                else: lines += 1; cur = wl
        tot += lines * size * 1.2 / 72.0
    return tot


class Deck:
    def __init__(self):
        self.prs = Presentation(); self.prs.slide_width = Emu(9144000); self.prs.slide_height = Emu(5143500)
        self.blank = self.prs.slide_layouts[6]

    def new(self, notes):
        s = self.prs.slides.add_slide(self.blank)
        s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(BG)
        CTX["slide"] = len(self.prs.slides)
        self.last_notes = notes; nw = words(notes)
        if nw > 55 or not 2 <= len(re.findall(r"[.!?](?:\s|$)", notes)) <= 4: raise SystemExit("REFUSED: slide %d notes: %d words or fewer than two sentences" % (CTX["slide"], nw))
        s.notes_slide.notes_text_frame.text = notes
        return s


def _runs(p, runs, base):
    for t, o in runs:
        r = p.add_run(); r.text = t; f = r.font
        f.name = o.get("font", base["font"]); f.size = Pt(o.get("size", base["size"])); f.bold = o.get("bold", base["bold"]); f.italic = o.get("italic", base["italic"])
        f.color.rgb = rgb(o.get("color", base["color"]))
        if o.get("link"):
            r.hyperlink.address = o["link"]; f.underline = True


def text(s, x, y, w, h, paras, size=12, font=SANS, color=INK, bold=False, italic=False, align="l", anchor="t", shape=None, fill=None, line=None, pad=0.0, radius=None, space=0):
    """a text box (or an auto shape carrying text) with explicit insets; paras = [str | [(text, opts)]]; refuses a box over 30 words or one whose text does not fit"""
    base = dict(size=size, font=font, color=color, bold=bold, italic=italic)
    if shape is None:
        sh = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    else:
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if fill: sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
        else: sh.fill.background()
        if line: sh.line.color.rgb = rgb(line); sh.line.width = Pt(1)
        else: sh.line.fill.background()
        sh.shadow.inherit = False
        if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE: sh.adjustments[0] = radius
    tf = sh.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(pad); tf.margin_top = tf.margin_bottom = Inches(pad * 0.6)
    tf.vertical_anchor = {"t": MSO_ANCHOR.TOP, "m": MSO_ANCHOR.MIDDLE, "b": MSO_ANCHOR.BOTTOM}[anchor]
    plain = []
    for i, pr in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER, "r": PP_ALIGN.RIGHT}[align]
        if space and i: p.space_before = Pt(space)
        runs = [(pr, {})] if isinstance(pr, str) else pr
        _runs(p, runs, base); plain.append("".join(t for t, _ in runs))
    n = words(" ".join(plain))
    if n > 30: raise SystemExit("REFUSED slide %d: a text box of %d words (D2): %s" % (CTX["slide"], n, plain[0][:50]))
    need = est(paras, w - 2 * pad, size, mono=(font == MONO)) + (pad * 1.2 if pad else 0) + (space / 72.0) * max(0, len(paras) - 1)
    if need > h + 0.05: raise SystemExit("REFUSED slide %d: text needs %.2f in, the box has %.2f in: %s" % (CTX["slide"], need, h, plain[0][:60]))
    return sh


def rect(s, x, y, w, h, fill, line=None, rounded=True, radius=0.12):
    sh = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = rgb(fill)
    if line: sh.line.color.rgb = rgb(line); sh.line.width = Pt(1)
    else: sh.line.fill.background()
    sh.shadow.inherit = False
    if rounded: sh.adjustments[0] = radius
    tx = sh._element.find(qn("p:txBody"))        # a card carries no text: no empty paragraph for the deck check's row reader to trip over
    if tx is not None: sh._element.remove(tx)
    return sh


def arrow(s, x1, y1, x2, y2, color=MUTED, width=1.75):
    c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color); c.line.width = Pt(width)
    ln = c.line._get_or_add_ln(); t = etree.SubElement(ln, qn("a:tailEnd")); t.set("type", "triangle")
    return c


def frame(d, s, k, n, title, sub=None, take=None):
    """the brand mark, the title, the subtitle, the takeaway line and the slide number of a content slide"""
    text(s, 0.5, 0.38, 0.62, 0.42, ["₿"], size=18, bold=True, color=WHITE, align="c", anchor="m", shape=MSO_SHAPE.ROUNDED_RECTANGLE, fill=ORANGE, radius=0.2)
    tsz = 28 if len(title) <= 34 else (24 if len(title) <= 42 else 21)
    text(s, 1.25, 0.26, 8.25, 0.62, [title], size=tsz, font=SERIF, anchor="m")
    if sub: text(s, 1.25, 0.88, 8.25, 0.32, [sub], size=13, italic=True, color=MUTED, anchor="m")
    if take:
        rect(s, 0.5, 5.07, 0.1, 0.34, ORANGE, rounded=False)
        text(s, 0.72, 5.03, 7.7, 0.42, [take], size=13, font=SERIF, anchor="m")
    number(s, k, n)


def number(s, k, n):
    text(s, 8.6, 5.08, 0.95, 0.34, ["%d / %d" % (k, n)], size=11, color=MUTED, align="r", anchor="m")


def picture(s, path, x, y, w, h, alt, mode="cover", focus=0.5):
    """a real picture in a w x h box: 'cover' crops to fill (focus = where the crop is centred on the long side), 'fit' keeps the whole picture inside the box, centred; returns the shape"""
    from PIL import Image
    iw, ih = Image.open(path).size
    if mode == "fit":
        sc = min(w / iw, h / ih); pw, ph = iw * sc, ih * sc
        pic = s.shapes.add_picture(path, Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))
    else:
        pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
        ar_box, ar_img = w / h, iw / ih
        if ar_img > ar_box:
            cut = 1 - ar_box / ar_img; pic.crop_left = cut * 0.5; pic.crop_right = cut * 0.5
        else:
            cut = 1 - ar_img / ar_box; pic.crop_top = cut * max(0.0, min(1.0, focus)); pic.crop_bottom = cut * (1 - max(0.0, min(1.0, focus)))
    pic._element.nvPicPr.cNvPr.set("descr", alt)
    if re.search(r"chart|graph|plot|histogram", alt + " " + pic.name, re.I): raise SystemExit("REFUSED: picture text would read as a chart picture (D6): " + alt)
    return pic


def table(s, x, y, w, colw, rows, size=10, rowh=0.3, head=True, hot=None, align=None):
    """a native table; rows[0] is the header when head; colw sum = w; hot = set of body row indices drawn in the soft accent"""
    assert abs(sum(colw) - w) < 0.011, (colw, w)
    gf = s.shapes.add_table(len(rows), len(colw), Inches(x), Inches(y), Inches(w), Inches(rowh * len(rows)))
    tb = gf.table
    for j, cw in enumerate(colw): tb.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        tb.rows[i].height = Inches(rowh)
        for j, v in enumerate(r):
            c = tb.cell(i, j); c.margin_left = c.margin_right = Inches(0.06); c.margin_top = c.margin_bottom = Inches(0.03)
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            is_head = head and i == 0
            c.fill.solid(); c.fill.fore_color.rgb = rgb(TEAL if is_head else (SOFT if (hot and (i - (1 if head else 0)) in hot) else (WHITE if i % 2 else CARD)))
            p = c.text_frame.paragraphs[0]; r_ = p.add_run(); r_.text = str(v)
            f = r_.font; f.size = Pt(size); f.name = SANS; f.bold = is_head; f.color.rgb = rgb(WHITE if is_head else INK)
            p.alignment = {"l": PP_ALIGN.LEFT, "r": PP_ALIGN.RIGHT, "c": PP_ALIGN.CENTER}[(align[j] if align else "l")]
    return gf


def chart(s, x, y, w, h, kind, labels, series, colors=None, fmt="#,##0", pointcolors=None, log=False, size=9, legend=False):
    """a native chart (bar = clustered columns, line = line with markers) with data labels on every point (the deck check requires them)"""
    cd = CategoryChartData(); cd.categories = [str(l) for l in labels]
    for nm, vals in series: cd.add_series(nm, [float(v) for v in vals])
    ct = XL_CHART_TYPE.COLUMN_CLUSTERED if kind == "bar" else XL_CHART_TYPE.LINE_MARKERS
    gf = s.shapes.add_chart(ct, Inches(x), Inches(y), Inches(w), Inches(h), cd); ch = gf.chart
    ch.has_title = False; ch.font.size = Pt(size); ch.font.name = SANS; ch.font.color.rgb = rgb(INK)
    ch.has_legend = legend
    if legend: ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(size)
    pl = ch.plots[0]
    if kind == "bar": pl.gap_width = 60; pl.vary_by_categories = False
    pl.has_data_labels = True; dl = pl.data_labels; dl.show_value = True; dl.number_format = fmt; dl.number_format_is_linked = False; dl.font.size = Pt(size)
    dl.position = XL_LABEL_POSITION.OUTSIDE_END if kind == "bar" else XL_LABEL_POSITION.ABOVE
    for e in dl._element.iter(qn("c:showVal")): e.set("val", "1")
    cols = colors or [ORANGE, TEAL]
    for i, se in enumerate(pl.series):
        if kind == "bar":
            se.format.fill.solid(); se.format.fill.fore_color.rgb = rgb(cols[i % len(cols)])
            if pointcolors:
                for j, pc in enumerate(pointcolors): pt = se.points[j]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = rgb(pc)
        else:
            se.format.line.color.rgb = rgb(cols[i % len(cols)]); se.format.line.width = Pt(2.25); se.smooth = False
            se.marker.format.fill.solid(); se.marker.format.fill.fore_color.rgb = rgb(cols[i % len(cols)]); se.marker.format.line.color.rgb = rgb(cols[i % len(cols)])
    va, ca = ch.value_axis, ch.category_axis
    va.has_major_gridlines = True; va.major_gridlines.format.line.color.rgb = rgb(LINE); va.format.line.fill.background()
    va.tick_labels.font.size = Pt(size); va.tick_labels.number_format = fmt; va.tick_labels.number_format_is_linked = False
    ca.tick_labels.font.size = Pt(size); ca.format.line.color.rgb = rgb(MUTED)
    if kind == "bar" and not log: va.minimum_scale = 0
    if log:
        sc = va._element.find(qn("c:scaling")); lb = etree.Element(qn("c:logBase")); lb.set("val", "10"); sc.insert(0, lb); va.minimum_scale = 1
    return gf


KEYWORDS = {"lambda", "for", "in", "if", "not", "and", "or", "else", "True", "False", "None"}
TOKEN = re.compile(r"""('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")|(\b0x[0-9a-fA-F]+\b|\b\d[\d_]*(?:\.\d+)?\b)|(\b[A-Za-z_]\w*\b)""")


def code_runs(line):
    """one code line as coloured runs: the prompt and the keywords in F2A860 (bold), strings 9ECBFF, numbers FFD28A, the rest E6EDF3 (the CME code colouring)"""
    runs, pos = [(">>> ", {"color": CODE_OR, "bold": True})], 0
    for m in TOKEN.finditer(line):
        if m.start() > pos: runs.append((line[pos:m.start()], {"color": CODE_TXT}))
        if m.group(1): runs.append((m.group(0), {"color": C_STR}))
        elif m.group(2): runs.append((m.group(0), {"color": C_NUM}))
        elif m.group(3) in KEYWORDS: runs.append((m.group(0), {"color": CODE_OR, "bold": True}))
        else: runs.append((m.group(0), {"color": CODE_TXT}))
        pos = m.end()
    if pos < len(line): runs.append((line[pos:], {"color": CODE_TXT}))
    merged = []
    for tx, o in runs:
        if merged and merged[-1][1] == o: merged[-1] = (merged[-1][0] + tx, o)
        else: merged.append((tx, o))
    return merged
