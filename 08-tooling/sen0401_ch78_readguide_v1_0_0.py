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
    code=["# L, the script library, hashes the word 'bitcoin'",
          "digest = L.sha256(b'bitcoin')",
          "# K, the helper library, hands out public key number 1",
          "key = K.pub(1)",
          "# len counts bytes; hex shows bytes as text",
          "facts = (len(digest), len(key), digest.hex()[:8])",
          "# A box ends by gathering its verdicts and printing them",
          "results = [facts]",
          "print(results)"],
    chips=[0, 1, 3, 7],
    balloons=["A line that starts with **#** is a comment: it says in words what the next lines do.",
              "**digest = L.sha256(...)** stores a value; read it from right to left: compute it, then name it.",
              "**K.pub(1)** asks library K for public key number 1; the letter before the dot names the library.",
              "A box ends with **results** and **print**; those values fill the result table."],
    libs=[("L", "The chapter's script library", "L.run(unlock, lock)"),
          ("K", "Ready-made spends and test keys", "K.pub(1), p2pkh(signer=2)"),
          ("Python", "Its own len, hex, bytes, sum, print", "len(lock), digest.hex()"),
          ("results", "The name every box ends with", "print(results)")],
    rows=["Digest length, in bytes", "Public key length, in bytes", "First hex digits of the digest"],
    boot="import sen0401_ch07_script_lib_v1_0_0 as L\nimport sen0401_ch07_deck_lib_v1_0_0 as K\n",
    library="sen0401_ch07_deck_lib_v1_0_0",
    line1="L and K are loaded once before every box",
    note=("From here on every code slide uses the same small set of tools, and this slide names them. Two libraries are loaded once before every box: "
          "L, the chapter's script library that assembles and runs Script programs, and K, which holds ready-made spends and test keys. "
          "The letter before a dot says which library a call belongs to, so L.sha256(...) asks L for a hash. "
          "Python's own len, hex and print need no library. A line that starts with # is a comment that says what the next lines do. "
          "A name followed by = stores a value, read from right to left. Every box ends by gathering its verdicts in results and printing them, "
          "and those values fill the result table beside the box. To remember: comments first, then the calls, then the table.")),
8: dict(
    code=["# K holds the chapter's fixed secret key and message",
          "secret_key, message = K.SK, K.MSG",
          "# L, the library, makes the public key and signs",
          "public_key = L.pubkey_create(secret_key)",
          "signature = L.ecdsa_sign(secret_key, message)",
          "# C, the signature library, builds a sample transaction",
          "tx = C.make_tx(1, 1)",
          "# len counts the bytes of each value",
          "facts = (len(public_key), len(signature), len(tx.vin))",
          "# A box ends by gathering its verdicts and printing them",
          "results = [facts]",
          "print(results)"],
    chips=[0, 3, 6, 10],
    balloons=["A line that starts with **#** is a comment: it says in words what the next lines do.",
              "**public_key = L.pubkey_create(...)** stores a value; read it from right to left: compute it, then name it.",
              "**C.make_tx(1, 1)** asks library C for a sample transaction; the letter before the dot names the library.",
              "A box ends with **results** and **print**; those values fill the result table."],
    libs=[("K", "The fixed secret key and message", "K.SK, K.MSG"),
          ("L", "The script library, as in Ch 7", "L.ecdsa_sign(sk, msg)"),
          ("C", "The signature library of Ch 8", "C.make_tx(1, 1)"),
          ("Python", "Its own len, hex, sum, max, zip", "len(sig), sig.hex()"),
          ("results", "The name every box ends with", "print(results)")],
    rows=["Public key length, in bytes", "Signature length, in bytes", "Inputs of the sample transaction"],
    boot="import sen0401_ch07_script_lib_v1_0_0 as L, sen0401_ch08_sig_lib_v1_0_0 as C, sen0401_ch08_claims_v1_0_0 as K\n",
    library="sen0401_ch08_sig_lib_v1_0_0",
    line1="L, C and K are loaded once before every box",
    note=("From here on every code slide uses the same small set of tools, and this slide names them. Three libraries are loaded once before every box: "
          "L, the script library already known from chapter 7, C, the signature library of this chapter, and K, which holds the fixed secret key and message. "
          "The letter before a dot says which library a call belongs to. "
          "Python's own len, hex and print need no library, and a few boxes import Counter, combinations or date from the standard library. "
          "A line that starts with # is a comment, and a name followed by = stores a value, read from right to left. Every box ends by gathering its "
          "verdicts in results and printing them, and those values fill the result table. To remember: comments first, then the calls, then the table.")),
}[ch]
TITLE = "How to read the code in this chapter"
SUB = "Libraries, names and conventions behind every box that follows"
TAKE = "Read the comments first, then the calls, then the result table"
EXNAME = "Reading the code: libraries, names and results"

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
    if t == "Scripts and the Script language (1 of 4)" or re.fullmatch(r"Chapter \d+ .*|.*\(1 of \d\)", t): settext(sh, TITLE)
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
    cy = by + 0.08 + li * LH + LH / 2 - 0.13
    chip = box(new, MSO_SHAPE.OVAL, 0.4, cy, 0.26, 0.26, ORANGE); chip.name = "Step %d" % k
    cn = new.shapes.add_textbox(Emu(int(0.4 * E)), Emu(int(cy * E)), Emu(int(0.26 * E)), Emu(int(0.26 * E))); cn.name = "Step number %d" % k
    tfc = cn.text_frame; tfc.vertical_anchor = MSO_ANCHOR.MIDDLE; tfc.margin_left = tfc.margin_right = tfc.margin_top = tfc.margin_bottom = 0
    pc = tfc.paragraphs[0]; pc.alignment = PP_ALIGN.CENTER; rc = pc.add_run(); rc.text = str(k); rc.font.size = Pt(11); rc.font.bold = True; rc.font.name = "Cambria"; rc.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
ry = by + bh + 0.04
rn = new.shapes.add_textbox(Emu(int(0.5 * E)), Emu(int(ry * E)), Emu(int(5.12 * E)), Emu(int(0.18 * E))); rn.name = "Run note"
tfr = rn.text_frame; tfr.margin_left = tfr.margin_right = tfr.margin_top = tfr.margin_bottom = 0; tfr.vertical_anchor = MSO_ANCHOR.MIDDLE
rr = tfr.paragraphs[0].add_run(); rr.text = "run under Python 3.14.6 - %s" % GUIDE["line1"]; rr.font.size = Pt(9); rr.font.italic = True; rr.font.name = "Calibri"; rr.font.color.rgb = RGBColor(0x6E, 0x65, 0x5C)
# left, below: where the names come from
ty = ry + 0.26; rowh = 0.215
lib_rows = [("Name", "What it is", "Used like")] + GUIDE["libs"]
table(new, 0.5, ty, [0.72, 2.28, 2.2], lib_rows, rowh, mono_col=2)
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
