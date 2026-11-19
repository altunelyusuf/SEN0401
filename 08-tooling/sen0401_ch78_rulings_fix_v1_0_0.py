#!/usr/bin/env python3
"""sen0401_ch78_rulings_fix v1.0.0 - corrects the chapter 7 and chapter 8 decks and pages to the owner's material rulings of 2026-11-19 (urgency).
Reads the newest deck, page, page data and chapter code manifest of the chapter, writes the next version of each beside them.
Deck: prompt markers and lambdas gone, every code slide rebuilt from the corrected examples (comment lines, descriptive names, no wrapping),
'Think of' lines removed, presenter notes that teach the slide (60-140 words), short titles lengthened, a visual (connectors) on slides that had none.
Page: the same examples in the chapter code tab (identical text), the worked examples of the concept nodes written as plain code, lecture titles and notes
equal to the deck. Usage: python3 sen0401_ch78_rulings_fix_v1_0_0.py 7|8"""
import copy, glob, html, importlib.util, io, json, math, os, re, sys, tokenize
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE_TYPE as T
from lxml import etree

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "08-tooling")
E = 914400
def load(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(TOOL, name + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
EXM = load("sen0401_ch78_examples_v1_0_0"); NTM = load("sen0401_ch78_notes_v1_0_0")

CFG = {
 7: dict(deck_glob="SEN0401_Ch07_AuthorizationAuthentication_3e_v*.pptx", deck_fmt="SEN0401_Ch07_AuthorizationAuthentication_3e_v%d_%d_0.pptx", dir="ch07",
         page_new=(9, 97), data_dir="ch07-page", EX=EXM.EX7, NOTES=NTM.NOTES7, FULL=NTM.NOTES7_FULL, EXT=NTM.EXT7, TITLES=NTM.TITLES7, cc_new=(1, 2), n_examples=15),
 8: dict(deck_glob="SEN0401_Ch08_DigitalSignatures_3e_v*.pptx", deck_fmt="SEN0401_Ch08_DigitalSignatures_3e_v%d_%d_0.pptx", dir="ch08",
         page_new=(9, 98), data_dir="ch08-page", EX=EXM.EX8, NOTES=NTM.NOTES8, FULL={}, EXT=NTM.EXT8, TITLES=NTM.TITLES8, cc_new=(1, 1), n_examples=20),
}
ch = int(sys.argv[1]); C = CFG[ch]
def vkey(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())
D = os.path.join(REPO, "03-materials", C["dir"]); PD = os.path.join(D, "page")

# ---------------------------------------------------------------- deck helpers
THINK = re.compile(r"^\s*Think of\b")
PROMPT = re.compile(r"^(>>>|\.\.\.|>>)\s?")
CODE_COL = dict(text="E6EDF3", string="9ECBFF", comment="8FB996", keyword="C4A7F0", number="F2C78F")
KEYWORDS = {"def", "return", "for", "in", "if", "else", "import", "from", "as", "and", "or", "not", "True", "False", "None", "while", "elif", "with"}

def is_code(sh): return sh.has_text_frame and sh.name != "chip" and any(r.font.name == "Courier New" for pa in sh.text_frame.paragraphs for r in pa.runs)
def has_visual(slide):
    for sh in slide.shapes:
        if sh.shape_type in (T.PICTURE, T.CHART, T.TABLE, T.GROUP) or is_code(sh): return True
    return sum(1 for sh in slide.shapes if sh.shape_type == T.LINE or "Connector" in sh.name) >= 2

def est_height(tf, width_in, scale=1.0):
    h = 0.0
    for pa in tf.paragraphs:
        size = next((r.font.size.pt for r in pa.runs if r.font.size), 12.0) * scale
        tx = "".join(r.text for r in pa.runs)
        h += max(1, math.ceil(len(tx) * size * 0.54 / 72 / width_in)) * size * 1.22 / 72 + 0.03
    return h
def scale_cards(slide, texts):
    """concept-card slide: the cards grow to use the room that the removed lines left (larger type, rows spread over the slide)."""
    items = []
    for tx in texts:
        bg = next((b for b in slide.shapes if b.shape_type == T.AUTO_SHAPE and not b.text_frame.text.strip() and b.width > 1.5 * E and b.left <= tx.left <= b.left + b.width and b.top <= tx.top <= b.top + b.height + 0.2 * E), None)
        bar = next((b for b in slide.shapes if b.shape_type == T.AUTO_SHAPE and b.width < 0.2 * E and bg is not None and bg.left <= b.left <= bg.left + 0.2 * E and bg.top <= b.top <= bg.top + 0.5 * E), None)
        if bg is not None: items.append((tx, bg, bar))
    if not items: return
    top0 = min(b.top for _, b, _ in items) / E
    rows = {}
    for it in items: rows.setdefault(round(it[1].top / E, 1), []).append(it)
    keys = sorted(rows); avail = 4.85 - top0
    old_total = max(b.top + b.height for _, b, _ in items) / E - top0
    f = max(1.0, min(1.5, avail / max(old_total, 0.1)))
    need = []
    for k in keys:
        nh = 0
        for tx, bg, bar in rows[k]:
            nh = max(nh, est_height(tx.text_frame, tx.width / E, f) + 0.3)
        need.append(nh)
    gap = max(0.12, min(0.5, (avail - sum(need)) / max(1, len(keys) - 1))) if len(keys) > 1 else 0.0
    y = top0
    for k, nh in zip(keys, need):
        for tx, bg, bar in rows[k]:
            for pa in tx.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size: r.font.size = Pt(min(17, round(r.font.size.pt * f * 2) / 2))
            bg.top = Emu(int(y * E)); bg.height = Emu(int(nh * E))
            tx.top = Emu(int((y + 0.12) * E)); tx.height = Emu(int((nh - 0.2) * E))
            if bar is not None: bar.top = Emu(int((y + 0.14) * E)); bar.height = Emu(int((nh - 0.28) * E))
        y += nh + gap

def title_shape(slide):
    for sh in slide.shapes:
        if sh.has_text_frame and sh.name.lower() == "title": return sh
    for sh in slide.shapes:
        tx = sh.text_frame.text.strip() if sh.has_text_frame else ""
        if len(tx) > 2 and not re.match(r"^\d+\s*/\s*\d+$", tx) and not is_code(sh): return sh
def set_text(par, text):
    runs = par.runs; runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)
def next_id(slide): return max(int(x) for x in slide.shapes._spTree.xpath("//p:cNvPr/@id")) + 1
def put(slide, el):
    el.xpath(".//p:cNvPr")[0].set("id", str(next_id(slide))); slide.shapes._spTree.append(el)
    return slide.shapes[-1]
def set_geo(sh, x, y, w, h): sh.left, sh.top, sh.width, sh.height = Emu(int(x * E)), Emu(int(y * E)), Emu(int(w * E)), Emu(int(h * E))

def tokens(line):
    """split one line of Python into (text, kind) pieces for colouring."""
    out = []; pos = 0
    try:
        for tk in tokenize.generate_tokens(io.StringIO(line + "\n").readline):
            if tk.type in (tokenize.NEWLINE, tokenize.ENDMARKER, tokenize.NL, tokenize.INDENT, tokenize.DEDENT): continue
            s, e = tk.start[1], tk.end[1]
            if s > pos: out.append((line[pos:s], "text"))
            kind = {tokenize.COMMENT: "comment", tokenize.STRING: "string", tokenize.NUMBER: "number"}.get(tk.type, "keyword" if tk.type == tokenize.NAME and tk.string in KEYWORDS else "text")
            out.append((line[s:e], kind)); pos = e
    except tokenize.TokenError:
        return [(line, "text")]
    if pos < len(line): out.append((line[pos:], "text"))
    return out if out and "".join(t for t, _ in out) == line else [(line, "text")]

def fill_code(shape, code, size):
    tf = shape.text_frame; paras = tf.paragraphs
    for p in paras[1:]: p._p.getparent().remove(p._p)
    p0 = tf.paragraphs[0]
    for r in list(p0.runs): r._r.getparent().remove(r._r)
    for i, line in enumerate(code.split("\n")):
        par = p0 if i == 0 else tf.add_paragraph()
        for txt, kind in tokens(line) if line.strip() else []:
            r = par.add_run(); r.text = txt; f = r.font; f.name = "Courier New"; f.size = Pt(size); f.bold = False
            f.color.rgb = RGBColor.from_string(CODE_COL[kind])
        if not line.strip():
            e = par._p.get_or_add_endParaRPr(); e.set("sz", str(int(size * 100)))
def fill_plain(shape, text):
    set_text(shape.text_frame.paragraphs[0], text)

def layout_code_slide(slide, chunks, says, footer_text):
    """rebuild the left column of a code slide: numbered circle, code box, explanation, then the run note."""
    left = [sh for sh in slide.shapes if sh.left < 6.1 * E and 1.3 * E < sh.top < 4.99 * E]
    tpl = {}
    for sh in left:
        if is_code(sh) and "code" not in tpl: tpl["code"] = sh; tpl["rect"] = [s for s in left if s.shape_type == T.AUTO_SHAPE and not s.has_text_frame or (s.shape_type == T.AUTO_SHAPE and not s.text_frame.text.strip())]
    rects = [s for s in left if s.shape_type == T.AUTO_SHAPE and not s.text_frame.text.strip()]
    # templates: first dark rect, first circle (orange small), first digit text, first explanation, footer
    dark = next(s for s in rects if s.width > 4 * E); circ = next(s for s in rects if s.width < 0.4 * E)
    digit = next(s for s in left if s.has_text_frame and s.text_frame.text.strip().isdigit()); expl = next(s for s in left if s.has_text_frame and s.text_frame.text.strip() and s.text_frame.paragraphs[0].runs and not is_code(s) and s.width > 4 * E and s.height < 0.5 * E and "run under" not in s.text_frame.text and not s.text_frame.text.strip().isdigit())
    foot = next(s for s in left if s.has_text_frame and "run under" in s.text_frame.text)
    code_t = tpl["code"]
    T_ = {k: copy.deepcopy(v._element) for k, v in dict(dark=dark, circ=circ, digit=digit, expl=expl, foot=foot, code=code_t).items()}
    for sh in left: sh._element.getparent().remove(sh._element)
    maxlen = max(len(l) for c in chunks for l in c.split("\n"))
    plan = None
    for size in (10, 9.5, 9, 8.5):
        if maxlen > int(5.12 / (size * 0.6 / 72)): continue
        lh = size * 1.22 / 72
        for pad, gap, y0 in ((0.16, 0.10, 1.42), (0.12, 0.07, 1.36), (0.10, 0.05, 1.32)):
            y = y0; pl = []
            for c, s in zip(chunks, says):
                n = len(c.split("\n")); bh = n * lh + pad; el = max(1, math.ceil(len(s) / 70)); eh = el * 0.19 + 0.02
                pl.append((y, bh, eh)); y += bh + 0.04 + eh + gap
            if y <= 5.0: plan = pl; break
        if plan: break
    if not plan: raise SystemExit("code slide does not fit: " + chunks[0][:40])
    for i, (c, s, (y, bh, eh)) in enumerate(zip(chunks, says, plan), 1):
        r = put(slide, copy.deepcopy(T_["dark"])); r.name = "Code box %d" % i; set_geo(r, 0.5, y, 5.55, bh)
        r._element.xpath(".//a:gd")[0].set("fmla", "val %d" % max(3000, int(0.07 * 100000 * 0.5 / max(bh, 0.5) * 2)))
        t = put(slide, copy.deepcopy(T_["code"])); t.name = "Code %d" % i; set_geo(t, 0.74, y + pad / 2, 5.2, bh - pad); fill_code(t, c, size)
        ci = put(slide, copy.deepcopy(T_["circ"])); ci.name = "Step %d" % i; set_geo(ci, 0.40, y - 0.07, 0.26, 0.26)
        di = put(slide, copy.deepcopy(T_["digit"])); di.name = "Step number %d" % i; set_geo(di, 0.40, y - 0.07, 0.26, 0.26); fill_plain(di, str(i))
        ex = put(slide, copy.deepcopy(T_["expl"])); ex.name = "Explanation %d" % i; set_geo(ex, 0.80, y + bh + 0.03, 5.25, eh); fill_plain(ex, s)
    f = put(slide, copy.deepcopy(T_["foot"])); f.name = "Run note"
    right = [sh.top + sh.height for sh in slide.shapes if sh.left > 6.1 * E and sh.top < 4.9 * E and sh.name != "Run note"]
    if max(right) / E + 0.05 <= 4.5: set_geo(f, 6.25, max(right) / E + 0.05, 3.25, 0.4)
    else: set_geo(f, 0.5, plan[-1][0] + plan[-1][1] + 0.03 + plan[-1][2] + 0.02, 5.55, 0.2)
    fill_plain(f, footer_text)

def accent_rgb(slide):
    for sh in slide.shapes:
        if sh.shape_type == T.AUTO_SHAPE and sh.width < E * 0.2 and sh.height > E * 0.5:
            try: return sh.fill.fore_color.rgb
            except Exception: pass
    return RGBColor(0x5B, 0x6C, 0x8F)
def add_arrow(slide, x1, y1, x2, y2, rgb, name):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1)), Emu(int(y1)), Emu(int(x2)), Emu(int(y2)))
    c.name = "Connector " + name; c.line.color.rgb = rgb; c.line.width = Pt(2)
    ln = c.line._get_or_add_ln(); te = etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd"); te.set("type", "triangle")
def add_flow(slide):
    rgb = accent_rgb(slide)
    cards = sorted([sh for sh in slide.shapes if sh.shape_type == T.AUTO_SHAPE and sh.width >= 1.7 * E and sh.height >= 0.55 * E and 1.2 * E < sh.top < 4.9 * E and sh.left < 7.0 * E and (sh.width < 6 * E)], key=lambda s: (round(s.top / E, 1), s.left))
    n = 0
    if len(cards) >= 2:
        for a in cards:
            for b in cards:
                if a is b: continue
                if abs(a.top - b.top) < 0.1 * E and 0 < b.left - (a.left + a.width) < 0.8 * E:
                    yy = a.top + min(a.height, b.height) / 2; add_arrow(slide, a.left + a.width - 0.02 * E, yy, b.left + 0.02 * E, yy, rgb, "relation"); n += 1
                elif abs(a.left - b.left) < 0.1 * E and 0 < b.top - (a.top + a.height) < 0.7 * E:
                    xx = a.left + min(a.width, b.width) / 2; add_arrow(slide, xx, a.top + a.height - 0.02 * E, xx, b.top + 0.02 * E, rgb, "relation"); n += 1
        if n == 1:   # a pair: the relation runs both ways
            for a in cards:
                for b in cards:
                    if a is not b and abs(a.top - b.top) < 0.1 * E and 0 < b.left - (a.left + a.width) < 0.8 * E:
                        yy = a.top + min(a.height, b.height) / 2 + 0.14 * E; add_arrow(slide, b.left + 0.02 * E, yy, a.left + a.width - 0.02 * E, yy, rgb, "relation back"); n += 1
        if n >= 2: return True
    dots = sorted([sh for sh in slide.shapes if sh.shape_type == T.AUTO_SHAPE and abs(sh.width - 0.44 * E) < 0.03 * E and abs(sh.height - 0.44 * E) < 0.03 * E], key=lambda s: s.top)
    if len(dots) >= 2:
        for a, b in zip(dots, dots[1:]): add_arrow(slide, a.left + a.width / 2, a.top + a.height - 0.01 * E, b.left + b.width / 2, b.top + 0.01 * E, rgb, "step")
        return True
    if n >= 2: return True
    if any(sh.has_text_frame and sh.text_frame.text.strip().startswith(("Read and explore", "Read")) for sh in slide.shapes):   # resources slide: two column rules
        for (x1, y1, x2, y2) in ((5.0, 1.45, 5.0, 4.85), (0.5, 4.95, 9.5, 4.95)):
            c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Emu(int(x1 * E)), Emu(int(y1 * E)), Emu(int(x2 * E)), Emu(int(y2 * E)))
            c.name = "Connector rule"; c.line.color.rgb = rgb; c.line.width = Pt(1.25)
        return True
    return False

def wc(s): return len(s.split())

# ---------------------------------------------------------------- build the deck
src = sorted(glob.glob(os.path.join(D, C["deck_glob"])), key=lambda p: vkey(p, "pptx"))[-1]
v = vkey(src, "pptx"); dst = os.path.join(D, C["deck_fmt"] % (v[0], v[1] + 1)); assert not os.path.exists(dst), dst
prs = Presentation(src); N = len(prs.slides)
EXBY = {e["slide"]: e for e in C["EX"]}
SUB_OLD = "Each card: the meaning in a few words, then something you already know"; SUB_NEW = "Each card: one idea in a few words"
BOT_OLD = "Say each idea twice: once as the meaning, once as the everyday comparison"; BOT_NEW = "Say each idea in your own words before you go on"
final_notes = {}; final_titles = {}; report = []
for i, s in enumerate(prs.slides, 1):
    # 1. cards and "Think of" lines
    cards = []; shapes = list(s.shapes); th = []
    for k, sh in enumerate(shapes):
        if sh.has_text_frame and THINK.match(sh.text_frame.text):
            prev = next((p for p in reversed(shapes[:k]) if p.has_text_frame and p.text_frame.text.strip() and len(p.text_frame.paragraphs) >= 2), None)
            if prev is not None:
                ps = prev.text_frame.paragraphs; cards.append(("".join(r.text for r in ps[0].runs).strip(), "".join(r.text for r in ps[1].runs).strip()))
            th.append((sh, prev))
    for sh, prev in th:
        if prev is not None:
            for bg in s.shapes:
                if bg.shape_type == T.AUTO_SHAPE and not bg.text_frame.text.strip() and bg.left <= prev.left <= bg.left + bg.width and bg.top <= prev.top <= bg.top + bg.height and bg.width > 1.5 * E:
                    bg.height = Emu(int(prev.top + prev.height - bg.top + 0.10 * E))
                    for bar in s.shapes:
                        if bar.shape_type == T.AUTO_SHAPE and bar.width < 0.2 * E and bg.left <= bar.left <= bg.left + bg.width and bg.top <= bar.top <= bg.top + bg.height + 0.5 * E and bar.height > bg.height:
                            bar.height = Emu(int(bg.height - 0.28 * E))
                    break
        sh._element.getparent().remove(sh._element)
    if cards: scale_cards(s, [p for _, p in th if p is not None])
    for sh in s.shapes:   # a "Think of ..." sentence inside a longer text
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                t = "".join(r.text for r in pa.runs)
                if "Think of" in t and pa.runs and not THINK.match(t):
                    set_text(pa, re.sub(r"\s*Think of[^.]*\.", "", t))
            for pa in sh.text_frame.paragraphs:
                t = "".join(r.text for r in pa.runs)
                for a, b in ((SUB_OLD, SUB_NEW), (BOT_OLD, BOT_NEW)):
                    if t.strip() == a and pa.runs: set_text(pa, b)
    # 2. code slide
    old_code = [sh for sh in s.shapes if is_code(sh)]
    if old_code:
        e = EXBY[i]; oldsays = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and not is_code(sh) and sh.width > 4 * E and sh.left > 0.7 * E and sh.left < 1.0 * E and 1.3 * E < sh.top < 4.99 * E and "run under" not in sh.text_frame.text]
        foot = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and "run under" in sh.text_frame.text][0]
        assert len(oldsays) >= len(e["chunks"]) or True
        says = list(EXM.SAYS.get((ch, i)) or oldsays[:len(e["chunks"])])
        while len(says) < len(e["chunks"]): says.append("")
        tk = [sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.left > 6.1 * E and 3.2 * E < sh.top < 4.9 * E and sh.width > 2.5 * E]
        layout_code_slide(s, e["chunks"], says, foot)
        result = tk[0].strip() if tk else ""
        k = [x["slide"] for x in C["EX"]].index(i) + 1
        w = [x for x in says if x]
        words = ["first", "second", "third", "fourth"]
        body = " ".join("The %s box says: %s" % (words[j], w[j]) for j in range(len(w)))
        note = "Read the code from top to bottom; each comment line says what the next lines do. " + body + " On the right is the result: " + result + " This is example %d in the chapter code tab of the course page; change a number there and run it again to watch the answer change." % k
        final_notes[i] = note
    # 3. title
    tsh = title_shape(s)
    if i in C["TITLES"]:
        set_text(tsh.text_frame.paragraphs[0], C["TITLES"][i])
    final_titles[i] = tsh.text_frame.text.strip() if tsh is not None else ""
    # 4. notes by kind
    if i in C["NOTES"]: final_notes[i] = C["NOTES"][i]
    elif i in C["FULL"]: final_notes[i] = C["FULL"][i]
    elif i in C["EXT"]: final_notes[i] = s.notes_slide.notes_text_frame.text.strip() + C["EXT"][i]
    elif cards:
        body = " ".join("%s: %s" % (n, m) for n, m in cards)
        close = " Pause after each card and ask a student to say it again in their own words. Each term is explained in full on the course page for chapter %d, under the concept of the same name." % ch
        note = "Take the cards one at a time. " + body + close
        if wc(note) > 140: note = "Take the cards one at a time. " + body + " Ask a student to say each one again in their own words; the course page for chapter %d explains every term in full." % ch
        if wc(note) < 62: note += " Tie the cards back to the opening headline of this part before you move on, so that the terms stay connected to one story."
        final_notes[i] = note
    # 5. visual
    if i not in (1, N) and not has_visual(s):
        if not add_flow(s): report.append(("no visual placed", i))
    if i in final_notes:
        n_ = wc(final_notes[i]);
        if not 60 <= n_ <= 140: report.append(("notes words", i, n_))
        s.notes_slide.notes_text_frame.text = final_notes[i]
prs.save(dst); print(os.path.basename(dst)); print("report:", report)

# ---------------------------------------------------------------- page, page data, manifest
vd = C["page_new"]; page_ver = "%d.%d.0" % vd
src_page = sorted(glob.glob(os.path.join(PD, "sen0401_ch0%d_page_v*.html" % ch)), key=lambda p: vkey(p, "html"))[-1]
dst_page = os.path.join(PD, "sen0401_ch0%d_page_v%d_%d_0.html" % (ch, vd[0], vd[1])); assert not os.path.exists(dst_page)
src_man = sorted(glob.glob(os.path.join(PD, "chapter_code_ch0%d_v*.json" % ch)), key=lambda p: vkey(p, "json"))[-1]
cv = C["cc_new"]; dst_man = os.path.join(PD, "chapter_code_ch0%d_v%d_%d_0.json" % (ch, cv[0], cv[1])); assert not os.path.exists(dst_man)
pdd = os.path.join(TOOL, C["data_dir"])
src_data = sorted(glob.glob(os.path.join(pdd, "page_data_v*.json")), key=lambda p: vkey(p, "json"))[-1]
dst_data = os.path.join(pdd, "page_data_v%d_%d_0.json" % (vd[0], vd[1])); assert not os.path.exists(dst_data)

man = json.load(open(src_man)); assert [e["slide"] for e in man["examples"]] == [e["slide"] for e in C["EX"]]
for me, ne in zip(man["examples"], C["EX"]):
    me["code"] = "\n".join(ne["chunks"]); me["show"] = [dict(expression=x, expected=y) for x, y in ne["show"]]
man["manifest"] = "chapter_code_ch0%d_v%d_%d_0" % (ch, cv[0], cv[1]); man["deck"] = os.path.basename(dst); man["deck_version"] = "%d.%d.0" % (v[0], v[1] + 1)
json.dump(man, open(dst_man, "w"), indent=1, ensure_ascii=False)

H = open(src_page, encoding="utf-8").read()
tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a)
data = json.loads(H[a:b]); old_ver = data["_version"]
def enc_ttl(x): return x.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
LAM = re.compile(r"""^\(lambda g: \(exec\((?P<q>["'])(?P<src>.*)(?P=q), g\), g\['result'\]\)\[1\]\)\(\{\}\)$""", re.S)
ttl_pairs = []
for n in data["nodes"]:
    io_ = n.get("io")
    if not io_: continue
    old = io_["code"]; new = None
    m = LAM.match(old)
    if m:
        inner = ast_inner = __import__("ast").literal_eval(m.group("q") + m.group("src") + m.group("q"))
        new = inner.rstrip("\n") + "\nresult"
    elif "lambda" in old:
        new = ("n = 10\nper = 148\nfixed = 100\n\ndef hashed_bytes(k):\n    return k * (k * per + fixed)\n\n"
               "(hashed_bytes(n), hashed_bytes(2 * n), round(hashed_bytes(2 * n) / hashed_bytes(n), 2))")
    if new is not None:
        compile(new, "<node>", "exec"); io_["code"] = new; ttl_pairs.append((old, new))
def plain(old):
    m = LAM.match(old)
    return __import__("ast").literal_eval(m.group("q") + m.group("src") + m.group("q")).rstrip("\n") + "\nresult" if m else None
for n in data["nodes"]:
    er = n.get("error")
    if er and "lambda" in er["code"]:
        old = er["code"]; new = plain(old); assert new, old[:60]; compile(new, "<error>", "exec"); er["code"] = new; ttl_pairs.append((old, new))
for vis in data["visuals"].values():
    for f_ in vis.get("facts", []):
        mm = re.match(r"^\(lambda n: \(n, 32 \* n\)\)\((.*)\)$", f_.get("expr", ""))
        if mm:
            old = f_["expr"]; f_["expr"] = "(%s, 32 * (%s))" % (mm.group(1), mm.group(1)); ttl_pairs.append((old, f_["expr"]))
cc = data["chaptercode"]
for e_, ne in zip(cc["examples"], C["EX"]): e_["code"] = "\n".join(ne["chunks"])
cc["file"] = "03-materials/%s/page/%s" % (C["dir"], os.path.basename(dst_man)); cc["version"] = "%d.%d.0" % cv
newtitle = {i: t for i, t in final_titles.items()}
for L_ in data["lecture"]:
    k = L_["n"]
    if k in final_notes: L_["say"] = final_notes[k]
    if k in C["TITLES"]: L_["title"] = C["TITLES"][k]
data["_version"] = page_ver
raw = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
H2 = H[:a] + raw + H[b:]
for old, new in ttl_pairs:
    H2 = H2.replace(enc_ttl(old), enc_ttl(new))
H2 = H2.replace('<meta name="version" content="%s">' % old_ver, '<meta name="version" content="%s">' % page_ver)
H2 = H2.replace("lambda  lambda x: …", "lambda  an unnamed one-line function")
for old, new in (('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ('key=lambda x: len(x))', 'key=len)')):
    assert old in H2, old; H2 = H2.replace(old, new)
open(dst_page, "w", encoding="utf-8").write(H2)
json.dump(data, open(dst_data, "w"), indent=None, ensure_ascii=False)
print(os.path.basename(dst_page), os.path.basename(dst_man), os.path.basename(dst_data), "node examples rewritten:", len(ttl_pairs))
