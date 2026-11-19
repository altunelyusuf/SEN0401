"""SEN0401 Ch7/Ch8: one reader slide 'How to read the code in this chapter' (slide 7, before the first code slide),
and the same guide on the page (a lecture entry and the first runnable example of the Chapter code tab).

usage: python3 sen0401_ch78_readguide_v1_0_0.py 7|8
  READ_OUT=/tmp/x.pptx  -> preview: writes only the deck there
Versioning: the deck, the manifest and the page of the chapter are UNRELEASED drafts (one step above their released
predecessor), so they are rewritten in place; no version is counted up here.
Renumbering: every slide from 7 on moves one place; every 'slide N' reference, every 'N / T' label, the page lecture
numbers and the example slide numbers move with it. The run notes 'as on slide 7' stay: slide 7 is now the setup slide.
"""
import sys, os, re, glob, json, copy, importlib, subprocess
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from lxml import etree

E = 914400
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); TOOL = os.path.join(REPO, "08-tooling")
ch = int(sys.argv[1]); POS = 7                                  # the new slide takes place 7
INK = RGBColor(0x2B, 0x26, 0x22); ORANGE = RGBColor(0xD9, 0x7A, 0x14); EDGE = "DFD6C7"
BAL = RGBColor(0xFF, 0xFB, 0xEF); BEDGE = RGBColor(0xE8, 0xB8, 0x78); VOICE = "Trebuchet MS"
CODE_COL = dict(text="E6EDF3", string="9ECBFF", comment="8FB996", keyword="C4A7F0", number="F2C78F")
KEYWORDS = {"def", "return", "for", "in", "if", "else", "import", "from", "as", "and", "or", "not", "True", "False", "None", "while", "elif", "with"}
WARN = []

# ----------------------------------------------------------------------------------------------- the content, per chapter
GUIDE = {
7: dict(
    code=["# L: this course's own script library, after Bitcoin Core",
          "digest = L.sha256(b'bitcoin')",
          "# K: this course's helpers, with toy keys 12, 13, 14 ...",
          "key = K.pub(1)",
          "# len and hex are Python's own; no library is needed",
          "facts = (len(digest), len(key), digest.hex()[:8])",
          "results = [facts]",
          "print(results)"],
    chips=[0, 1, 2, 3],
    balloons=["**L** is not an installed package: it is this course's own pure-Python script library, written for the chapter.",
              "It follows **Bitcoin Core's** script interpreter and is checked against Core's test data; it is not Core itself.",
              "**K** is course-written too: ready-made spends signed with toy keys that must never hold real coins.",
              "**K.pub(1)** is a toy key's public key; helpers like **old_joined** replay history and are invented to teach."],
    libs=[("L", "Script interpreter, signing, hashes", "Course-written, after Bitcoin Core"),
          ("K", "Ready-made spends and toy keys", "Course-written, for this chapter"),
          ("Python", "len, hex, bytes, sum, print", "Built in; nothing to install"),
          ("results", "Name each box ends with", "Convention: fills the result table")],
    refs="Reference code: github.com/bitcoin/bitcoin (src/script/interpreter.cpp) and github.com/bitcoin/bips.",
    rows=["Digest length, in bytes", "Public key length, in bytes", "First hex digits of the digest"],
    library="sen0401_ch07_deck_lib_v1_0_0",
    line1="L and K are the course's own libraries, loaded before every box",
    sub="Where L and K come from, what is real in them and what is invented",
    take="L and K are the course's own code, checked against Bitcoin Core",
    note=("L and K are not packages you install from the internet. Both are written for this course and kept in its 08-tooling folder, so the same code runs "
          "in the lecture, in the chapter builder and in the page's Python. L is a pure-Python Bitcoin Script interpreter that follows Bitcoin Core's own "
          "interpreter and is checked by a verify script against Core's test data and real mainnet transactions. It is not Bitcoin Core, which stays the reference: "
          "github.com/bitcoin/bitcoin, with the rules in github.com/bitcoin/bips. K builds ready-made spends with toy keys 12, 13 and on, which must never hold "
          "real coins. Helpers such as old_joined are invented for teaching: they replay the 2010 bug. Python's own len, hex and print need no library.")),
8: dict(
    code=["# K: this course's claims module; it recomputes the text",
          "secret_key, message = K.SK, K.MSG",
          "# L: the course's script library from chapter 7",
          "public_key = L.pubkey_create(secret_key)",
          "signature = L.ecdsa_sign(secret_key, message)",
          "# C: the course's signature library for this chapter",
          "tx = C.make_tx(1, 1)",
          "facts = (len(public_key), len(signature), len(tx.vin))",
          "results = [facts]",
          "print(results)"],
    chips=[0, 1, 2, 5],
    balloons=["**K** is course-written: it recomputes the chapter's claims from the library and from saved evidence.",
              "**K.SK** is a fixed toy key kept in the course repository: never use it for real coins.",
              "**L** is the course's script library from chapter 7, not an installed package; it follows Bitcoin Core.",
              "**C** is written for this chapter from the book, the BIPs and RFC 6979; it is not part of Bitcoin Core."],
    libs=[("K", "Toy key, message and claims", "Course-written, for this chapter"),
          ("L", "Script and signature library", "Course-written (Ch 7), after Bitcoin Core"),
          ("C", "Signing, hashes, attack demos", "Course-written, from book, BIPs, RFCs"),
          ("Python", "len, hex, sum, max, zip", "Built in; a few boxes import more"),
          ("results", "Name each box ends with", "Convention: fills the result table")],
    refs="Reference code: github.com/bitcoin/bitcoin (src/script/interpreter.cpp) and github.com/bitcoin/bips.",
    rows=["Public key length, in bytes", "Signature length, in bytes", "Inputs of the sample transaction"],
    library="sen0401_ch08_sig_lib_v1_0_0",
    line1="L, C and K are the course's own libraries, loaded before every box",
    sub="Where L, C and K come from, what is real in them and what is invented",
    take="L, C and K are the course's own code; L is checked against Bitcoin Core",
    note=("L, C and K are not packages you install from the internet. All three are written for this course and kept in its 08-tooling folder. L is the "
          "pure-Python Bitcoin Script and signature library of chapter 7, which follows Bitcoin Core's interpreter and is checked against Core's test data and "
          "real transactions; Core stays the reference at github.com/bitcoin/bitcoin, with the rules in github.com/bitcoin/bips. C adds what only this chapter "
          "needs, written from the book, the BIPs and RFC 6979, and it also holds teaching constructions, such as the toy protocol and the simplified signature, "
          "that are invented to explain and are not Bitcoin's real protocol. K holds a fixed toy key, never to be used for real coins.")),
}[ch]
TITLE = "Where the code's libraries come from"
SUB = GUIDE["sub"]
TAKE = GUIDE["take"]
EXNAME = "Where the libraries come from: L, K and the results"

# ----------------------------------------------------------------------------------------------- helpers
def plain(t): return t.replace("**", "")
def nlines(t, size, w):
    cw = size * 0.54 * 1.03 / 72.0; avail = w - 0.22; lines = 1; cur = 0.0
    for word in plain(t).split():
        L_ = (len(word) + 1) * cw
        if cur + L_ > avail + cw and cur > 0: lines += 1; cur = L_
        else: cur += L_
    return lines
def need_h(t, size, w): return nlines(t, size, w) * size * 1.2 / 72.0 + 0.08
def fit(t, w, h, sizes):
    for sz in sizes:
        if need_h(t, sz, w) <= h: return sz
    WARN.append("text does not fit (%.2f x %.2f): %s" % (w, h, plain(t)[:50])); return sizes[-1]
def box(s, shape, x, y, w, h, fill, line=None, lw=0.9):
    b = s.shapes.add_shape(shape, Emu(int(x * E)), Emu(int(y * E)), Emu(int(w * E)), Emu(int(h * E)))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    if line is None: b.line.fill.background()
    else: b.line.color.rgb = line; b.line.width = Pt(lw)
    b.shadow.inherit = False; return b
def text(b, t, size, font=VOICE, bold=False, anchor=MSO_ANCHOR.MIDDLE, m=0.1, color=INK, align=PP_ALIGN.LEFT):
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Emu(int(m * E)); tf.margin_top = tf.margin_bottom = Emu(int(0.03 * E))
    pa = tf.paragraphs[0]; pa.alignment = align
    for i, p in enumerate(t.split("**")):
        if not p: continue
        r = pa.add_run(); r.text = p; r.font.size = Pt(size); r.font.name = font; r.font.bold = bold or (i % 2 == 1); r.font.color.rgb = color
def balloon(s, x, y, w, h, t, sizes, tail=False, name="Balloon"):
    if tail:
        b = box(s, MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT, x, y, w, h, BAL, BEDGE); b.adjustments[0] = -0.56 if w > 4 else -0.6; b.adjustments[1] = 0.0; b.adjustments[2] = 0.16667
    else: b = box(s, MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h, BAL, BEDGE)
    text(b, t, fit(t, w, h, sizes), anchor=MSO_ANCHOR.MIDDLE); b.name = name; return b

def cell_borders(cell):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        ln = etree.SubElement(tcPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}" + tag[2:], w="6350", cap="flat", cmpd="sng", algn="ctr")
        sf = etree.SubElement(ln, "{http://schemas.openxmlformats.org/drawingml/2006/main}solidFill")
        etree.SubElement(sf, "{http://schemas.openxmlformats.org/drawingml/2006/main}srgbClr", val=EDGE)
    # borders must precede the fill in tcPr
    fills = [c for c in tcPr if c.tag.endswith("solidFill") or c.tag.endswith("noFill")]
    for f in fills: tcPr.remove(f); tcPr.append(f)
def table(s, x, y, widths, rows, rowh, head=True, mono_col=None, size=9):
    gf = s.shapes.add_table(len(rows), len(widths), Emu(int(x * E)), Emu(int(y * E)), Emu(int(sum(widths) * E)), Emu(int(rowh * len(rows) * E)))
    t = gf.table
    tblPr = t._tbl.tblPr
    for a in list(tblPr.attrib): del tblPr.attrib[a]
    for c in list(tblPr): tblPr.remove(c)
    for i, w in enumerate(widths): t.columns[i].width = Emu(int(w * E))
    for r, row in enumerate(rows):
        t.rows[r].height = Emu(int(rowh * E))
        for c, val in enumerate(row):
            cell = t.cell(r, c); cell.margin_left = cell.margin_right = Emu(91440); cell.margin_top = cell.margin_bottom = Emu(18288)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame; tf.word_wrap = True; run = tf.paragraphs[0].add_run(); run.text = val
            run.font.size = Pt(size); run.font.name = "Courier New" if (mono_col is not None and c == mono_col and r > 0) else "Calibri"
            if head and r == 0:
                run.font.bold = True; run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF); cell.fill.solid(); cell.fill.fore_color.rgb = INK
            else:
                run.font.color.rgb = INK; cell.fill.background()
                if c == 0: run.font.bold = True
            cell_borders(cell)
    return gf
TOK = re.compile(r"(#.*)|(b?'[^']*')|(\d+)|([A-Za-z_]\w*)|(\s+)|(.)")
def code_runs(pa, line, size=9.5):
    for m in TOK.finditer(line):
        txt = m.group(0)
        if m.group(1): col = CODE_COL["comment"]
        elif m.group(2): col = CODE_COL["string"]
        elif m.group(3): col = CODE_COL["number"]
        elif m.group(4) and txt in KEYWORDS: col = CODE_COL["keyword"]
        else: col = CODE_COL["text"]
        r = pa.add_run(); r.text = txt; r.font.size = Pt(size); r.font.bold = False; r.font.name = "Courier New"; r.font.color.rgb = RGBColor.from_string(col)

# slide-number references: every number from POS on moves one place
GROUP = re.compile(r"(?i)\b(slides?\s+)(\d+(?:\s*(?:,|and|to|-|–)\s*\d+)*)")
def mv(n): return n + 1 if n >= POS else n
def remap(t): return GROUP.sub(lambda m: m.group(1) + re.sub(r"\d+", lambda k: str(mv(int(k.group()))), m.group(2)), t)

def vk(p, ext): return tuple(int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.%s$" % ext, p).groups())
def newest(pat, ext): return sorted(glob.glob(pat), key=lambda p: vk(p, ext))[-1]
D = os.path.join(REPO, "03-materials", "ch0%d" % ch); PD = os.path.join(D, "page"); DD = os.path.join(TOOL, "ch0%d-page" % ch)
deck = newest(os.path.join(D, "SEN0401_Ch0%d_*_3e_v*.pptx" % ch), "pptx"); page = newest(os.path.join(PD, "sen0401_ch0%d_page_v*.html" % ch), "html"); man = newest(os.path.join(PD, "chapter_code_ch0%d_v*.json" % ch), "json")
data_json = newest(os.path.join(DD, "page_data_v*.json"), "json")

# the example really runs: the expected result is computed, not typed
sys.path.insert(0, TOOL)
ns = {}
for mod, alias in ([("sen0401_ch07_script_lib_v1_0_0", "L"), ("sen0401_ch07_deck_lib_v1_0_0", "K")] if ch == 7 else
                   [("sen0401_ch07_script_lib_v1_0_0", "L"), ("sen0401_ch08_sig_lib_v1_0_0", "C"), ("sen0401_ch08_claims_v1_0_0", "K")]):
    ns[alias] = importlib.import_module(mod)
CODE = "\n".join(GUIDE["code"])
exec(compile(CODE, "<guide>", "exec"), ns)
RES = ns["results"]; FACTS = RES[0]
RESULT_ROWS = [(GUIDE["rows"][i], str(FACTS[i])) for i in range(3)]
EXPECTED = repr(RES)
print("example result:", EXPECTED)

# ----------------------------------------------------------------------------------------------- the deck
P = Presentation(deck); total0 = len(P.slides._sldIdLst); ex0 = {7: 15, 8: 20}[ch]
assert total0 == {7: 61, 8: 51}[ch], "the deck already has the reading slide? %d slides" % total0
TOTAL = total0 + 1

# 1. renumber the references on every slide and its notes (the setup run notes 'as on slide 7' stay)
changed = 0
for s in P.slides:
    def shapes(sh_list):
        for sh in sh_list:
            if sh.shape_type == 6: yield from shapes(sh.shapes)
            else: yield sh
    for sh in shapes(s.shapes):
        if not sh.has_text_frame or sh.name == "Run note": continue
        for pa in sh.text_frame.paragraphs:
            full = "".join(r.text for r in pa.runs); want = remap(full)
            if want == full: continue
            for r in pa.runs: r.text = remap(r.text)
            got = "".join(r.text for r in pa.runs)
            if got != want: WARN.append("a reference is split across runs: %r" % full[:60])
            changed += 1
    if s.has_notes_slide:
        nt = s.notes_slide.notes_text_frame.text; nn = remap(nt)
        if nn != nt: s.notes_slide.notes_text_frame.text = nn; changed += 1
print("references moved in", changed, "places")

# 2. the first code slide (old 7, now 8) points to the setup slide like all others
old7 = P.slides[POS - 1]
for sh in old7.shapes:
    if sh.name == "Run note":
        for r in sh.text_frame.paragraphs[0].runs:
            if "names as in the chapter setup" in r.text:
                r.text = r.text.replace("names as in the chapter setup", "%s and the chapter setup as on slide %d" % (GUIDE["line1"].split(" are ")[0], POS))

# 3. the new slide: header and footer copied from slide 6, content built here
src = P.slides[POS - 2]
new = P.slides.add_slide(src.slide_layout)
for ph in list(new.placeholders): ph._element.getparent().remove(ph._element)
keep = [sh for sh in src.shapes if sh.shape_type != 6]
for sh in keep: new.shapes._spTree.append(copy.deepcopy(sh._element))
byname = {sh.name: sh for sh in new.shapes}
def settext(sh, t):
    runs = sh.text_frame.paragraphs[0].runs; runs[0].text = t
    for r in runs[1:]: r.text = ""
for sh in new.shapes:
    if not sh.has_text_frame: continue
    t = sh.text_frame.text
    if re.fullmatch(r".*\(1 of \d\)", t): settext(sh, TITLE)
    elif t == "What each term means, in plain words": settext(sh, SUB)
    elif t == "Say each idea in your own words before you go on": settext(sh, TAKE)
    elif re.fullmatch(r"\d+ / \d+", t): settext(sh, "%d / %d" % (POS, TOTAL))
hd = [sh.text_frame.text for sh in new.shapes if sh.has_text_frame and sh.text_frame.text.strip()]
assert TITLE in hd and SUB in hd and TAKE in hd, ("header not replaced", hd)

# left: the annotated code box
LH = 11.5 / 72.0; n = len(GUIDE["code"]); bx, by, bw = 0.5, 1.32, 5.2; bh = n * LH + 0.16
cb = box(new, MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, bh, RGBColor(0x23, 0x27, 0x2E), RGBColor(0x23, 0x27, 0x2E)); cb.adjustments[0] = 0.05; cb.name = "Code box 1"
ct = new.shapes.add_textbox(Emu(int((bx + 0.24) * E)), Emu(int((by + 0.08) * E)), Emu(int((bw - 0.3) * E)), Emu(int((bh - 0.12) * E))); ct.name = "Code 1"
tf = ct.text_frame; tf.word_wrap = False; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0; tf.vertical_anchor = MSO_ANCHOR.TOP
for i, line in enumerate(GUIDE["code"]):
    pa = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); pa.line_spacing = Pt(11.5); code_runs(pa, line)
    if len(line) > 60: WARN.append("code line of %d characters: %s" % (len(line), line))
for k, li in enumerate(GUIDE["chips"], 1):
    cy = by + 0.08 + li * LH + LH / 2 - 0.085
    chip = box(new, MSO_SHAPE.OVAL, 0.42, cy, 0.17, 0.17, ORANGE); chip.name = "Step %d" % k
    cn = new.shapes.add_textbox(Emu(int(0.42 * E)), Emu(int(cy * E)), Emu(int(0.17 * E)), Emu(int(0.17 * E))); cn.name = "Step number %d" % k
    tfc = cn.text_frame; tfc.vertical_anchor = MSO_ANCHOR.MIDDLE; tfc.margin_left = tfc.margin_right = tfc.margin_top = tfc.margin_bottom = 0
    pc = tfc.paragraphs[0]; pc.alignment = PP_ALIGN.CENTER; rc = pc.add_run(); rc.text = str(k); rc.font.size = Pt(8); rc.font.bold = True; rc.font.name = "Cambria"; rc.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
ry = by + bh + 0.04
rn = new.shapes.add_textbox(Emu(int(0.5 * E)), Emu(int(ry * E)), Emu(int(5.12 * E)), Emu(int(0.18 * E))); rn.name = "Run note"
tfr = rn.text_frame; tfr.margin_left = tfr.margin_right = tfr.margin_top = tfr.margin_bottom = 0; tfr.vertical_anchor = MSO_ANCHOR.MIDDLE
rr = tfr.paragraphs[0].add_run(); rr.text = "run under Python 3.14.6 - %s" % GUIDE["line1"]; rr.font.size = Pt(9); rr.font.italic = True; rr.font.name = "Calibri"; rr.font.color.rgb = RGBColor(0x6E, 0x65, 0x5C)
# left, below: where the names come from
ty = ry + 0.26; rowh = 0.215
lib_rows = [("Name", "What it is", "Where it comes from")] + GUIDE["libs"]
table(new, 0.5, ty, [0.7, 2.0, 2.5], lib_rows, rowh)
rf = new.shapes.add_textbox(Emu(int(0.5 * E)), Emu(int((ty + rowh * len(lib_rows) + 0.05) * E)), Emu(int(5.2 * E)), Emu(int(0.32 * E))); rf.name = "References"
rf.text_frame.word_wrap = True; rf.text_frame.margin_left = rf.text_frame.margin_right = rf.text_frame.margin_top = rf.text_frame.margin_bottom = 0
rq = rf.text_frame.paragraphs[0].add_run(); rq.text = GUIDE["refs"]; rq.font.size = Pt(8.5); rq.font.italic = True; rq.font.name = "Calibri"; rq.font.color.rgb = RGBColor(0x6E, 0x65, 0x5C)
if ty + rowh * len(lib_rows) > 5.0: WARN.append("the library table ends at %.2f in" % (ty + rowh * len(lib_rows)))

# right: four balloons, then the result table of this box
RX, RW = 5.95, 3.55; y = 1.32; bhh = 0.56
for i, t in enumerate(GUIDE["balloons"]):
    balloon(new, RX, y, RW, bhh, t, [10, 9.5, 9, 8.5], tail=(i == 0), name="Story balloon %d" % (i + 1)); y += bhh + 0.08
lab = box(new, MSO_SHAPE.ROUNDED_RECTANGLE, RX, y + 0.02, RW, 0.24, BAL, BEDGE); lab.name = "Result label"; text(lab, "Result: the three facts of this box", 9.5, bold=True)
table(new, RX, y + 0.32, [2.35, 1.2], [("Fact", "Result")] + RESULT_ROWS, 0.2, size=9)
end_r = y + 0.32 + 0.2 * 4
if end_r > 5.0: WARN.append("the result table ends at %.2f in" % end_r)

# notes
note = GUIDE["note"]; wc = len(note.split())
if not 60 <= wc <= 140: WARN.append("the note has %d words" % wc)
new.notes_slide.notes_text_frame.text = note

# 4. move it to place 7, then number every slide again and fix the totals on slide 2
lst = P.slides._sldIdLst; el = list(lst)[-1]; lst.remove(el); lst.insert(POS - 1, el)
for i, s in enumerate(P.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame and re.fullmatch(r"\d+ / \d+", sh.text_frame.text.strip()): settext(sh, "%d / %d" % (i, TOTAL))
NUMW = {15: "fifteen", 20: "twenty", 16: "sixteen", 21: "twenty-one"}
s2 = P.slides[1]
for sh in s2.shapes:
    if not sh.has_text_frame: continue
    t = sh.text_frame.text.strip()
    if t == str(total0): settext(sh, str(TOTAL)); print("slide 2 total ->", TOTAL)
    elif t == str(ex0): settext(sh, str(ex0 + 1)); print("slide 2 runs ->", ex0 + 1)
    elif NUMW[ex0] in t:
        for r in sh.text_frame.paragraphs[0].runs: r.text = r.text.replace(NUMW[ex0], NUMW[ex0 + 1])
        print("slide 2 line ->", sh.text_frame.text)
print("slides:", len(P.slides._sldIdLst)); print("\n".join(WARN) if WARN else "no layout or note warnings")
OUT = os.environ.get("READ_OUT")
if OUT: P.save(OUT); print("preview", OUT); sys.exit(0)
P.save(deck)

# ----------------------------------------------------------------------------------------------- manifest and page
M = json.load(open(man)); assert len(M["examples"]) == ex0
for e in M["examples"]: e["order"] += 1; e["slide"] = mv(e["slide"])
M["examples"].insert(0, {"order": 1, "id": "ex00", "name": EXNAME, "slide": POS, "branch": "How to read the code", "library": GUIDE["library"], "needs": ["setup"],
                         "code": CODE, "show": [{"expression": "results", "expected": EXPECTED}], "result_picture": "table"})
json.dump(M, open(man, "w"), indent=1, ensure_ascii=False)
H = open(page, encoding="utf-8").read(); tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a)
data = json.loads(H[a:b]); assert len(data["lecture"]) == total0
for L_ in data["lecture"]:
    L_["say"] = remap(L_["say"])
    if L_["n"] >= POS: L_["n"] += 1
data["lecture"].insert(POS - 1, {"n": POS, "kind": "content", "title": TITLE, "say": " ".join(plain(t) for t in GUIDE["balloons"]) + "\n\n" + note, "takeaway": TAKE})
for e in data["chaptercode"]["examples"]: e["order"] += 1; e["slide"] = mv(e["slide"])
data["chaptercode"]["examples"].insert(0, {"order": 1, "name": EXNAME, "code": CODE, "slide": POS})
H2 = H[:a] + json.dumps(data, ensure_ascii=False).replace("</", "<\\/") + H[b:]
open(page, "w", encoding="utf-8").write(H2); json.dump(data, open(data_json, "w"), ensure_ascii=False)
print("written:", os.path.basename(deck), os.path.basename(page), os.path.basename(man), os.path.basename(data_json))
