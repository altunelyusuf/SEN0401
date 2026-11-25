#!/usr/bin/env python3
"""sen0401_ch01_deck_patch v1.0.0 - writes the chapter 1 deck 3.6.0 beside the committed 3.5.0 (which stays unchanged), to the standard of chapters 7 to 14
(deck standard v3.1.0, CME material check v1.2.0; owner rulings of 2026-11-14 and 2026-11-24). The slide count stays 76.
  * notes: the reader notes of ch01-deck/deck_notes_v3_6_0.json (60 to 140 full sentences' worth of words, no presenter directions, no analogy) on every slide;
  * no everyday analogy on any slide: every 'Think of' line, every analogy sentence, the analogy column of three tables, the house picture of the key slide, the caption 'Say each idea twice ...';
  * titles of at least four words; the concept-card slides carry the part strip of their part (a table) in place of the analogy lines; the diagrams are grouped into one figure each;
  * the result frames and the tile examples are no longer Courier New code frames (they are results, not code), so every Courier frame parses; explanations are named 'Balloon note N';
  * the nine story slides carry the 5N1K coverage in the alt text of their story boxes (invisible), the story text is unchanged.
Usage: python3 sen0401_ch01_deck_patch_v1_0_0.py   (run from anywhere; reads and writes under the repository)"""
__version__ = "1.0.0"
import copy, json, os, re, sys
import rdflib
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T

H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H)
SRC = os.path.join(REPO, "03-materials", "ch01", "SEN0401_Ch01_Introduction_3e_v3_5_0.pptx")
DST = os.path.join(REPO, "03-materials", "ch01", "SEN0401_Ch01_Introduction_3e_v3_6_0.pptx")
if os.path.exists(DST): raise SystemExit("refusing to overwrite " + DST)
NOTES = {int(k): v for k, v in json.load(open(os.path.join(H, "ch01-deck", "deck_notes_v3_6_0.json")))["notes"].items()}
assert sorted(NOTES) == list(range(1, 77))
E = 914400
g = rdflib.Graph(); g.parse(os.path.join(REPO, "06-quality", "sen0401_deck_standard_shapes_v1_1_0.ttl"), format="turtle")
RX = re.compile(str(next(g.objects(None, rdflib.Namespace("http://www.w3.org/ns/shacl#").pattern))), re.I)
ENDS = re.compile(r"""[.!?](?=["'”)\]]*(?:\s+["'“(]?[A-Z0-9]|\s*$))""")

p = Presentation(SRC)
assert len(p.slides) == 76


def S(i): return p.slides[i - 1]
def tx(sh): return sh.text_frame.text if sh.has_text_frame else ""
def delete(sh): sh._element.getparent().remove(sh._element)
def set_text(sh, new):
    ps = sh.text_frame.paragraphs; runs = ps[0].runs
    runs[0].text = new
    for r in runs[1:]: r._r.getparent().remove(r._r)
    for q in ps[1:]: q._p.getparent().remove(q._p)
def by_name(s, name): return [x for x in s.shapes if x.name == name]
def by_text(s, start): return [x for x in s.shapes if x.has_text_frame and tx(x).strip().startswith(start)]
def sentence_cut(s, m):
    st = 0
    for e in ENDS.finditer(s):
        if e.end() <= m.start(): st = e.end()
    while st < len(s) and s[st] == " ": st += 1
    e = ENDS.search(s, m.end()); en = e.end() if e else len(s)
    if st > 0 and s[st - 1] == " ": st -= 1
    elif en < len(s) and s[en] == " ": en += 1
    return s[:st] + s[en:]

LOG = []
def say(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)

# ---------------------------------------------------------------- titles of four words or more
TITLE = {2: "Today's route through six parts", 5: "Origins: three beats of the story", 6: "Origins: the key concepts", 12: "Money and price in three beats",
         28: "The network in three beats", 42: "Wallets and keys in three beats", 55: "A first payment in three beats", 64: "Foundations in three beats",
         70: "Foundations: the key concepts", 49: "The key alone proves ownership", 40: "Each confirmation makes a payment safer"}
for i, t in TITLE.items():
    sh = by_name(S(i), "Text 2")[0]; say("title", i, repr(tx(sh)), "->", repr(t)); set_text(sh, t)

# ---------------------------------------------------------------- overview slides: the analogy lines become the slide ranges that tell each beat
REFS = {5: ["Slides 7 and 8", "Slide 9", "Slides 10 and 11"], 12: ["Slides 14 to 19", "Slides 20 to 23", "Slides 24 to 27"],
        28: ["Slides 29 and 30", "Slides 31 to 38", "Slides 39 to 41"], 42: ["Slides 44 to 46", "Slides 47 and 48", "Slides 49 to 54"],
        55: ["Slides 61 and 62", "Slides 57 to 60", "Slides 61 and 63"], 64: ["Slides 65 to 69", "Slides 70 to 72", "Slide 73"]}
SUBT = {5: "Bitcoin combines parts that existed before it.", 42: "A wallet holds keys, not coins.", 55: "From an empty wallet to a first payment.",
        64: "Two old solved problems, joined into one system."}
for i, refs in REFS.items():
    th = by_text(S(i), "Think of"); assert len(th) == 3, (i, len(th))
    for sh, r in zip(th, refs): set_text(sh, "See %s for this beat." % (r[0].lower() + r[1:]))
for i, t in SUBT.items(): set_text(by_name(S(i), "Text 3")[0], t)

# ---------------------------------------------------------------- concept-card slides: no analogy lines; the part strip (a table) of the part below the cards
CARDS = {6: 5, 13: 12, 30: 28, 39: 28, 44: 42, 45: 42, 47: 42, 53: 42, 56: 55, 61: 55, 70: 64}
def strip_of(src):
    for sh in S(src).shapes:
        if sh.has_table: return sh
for i, src in CARDS.items():
    s = S(i)
    for sh in by_text(s, "Think of"): delete(sh)
    for sh in by_text(s, "Say each idea twice"): set_text(sh, "Each idea is defined once here and shown at work on the slides of this part")
    for sh in s.shapes:
        if sh.has_text_frame and tx(sh).startswith("Each card:"): set_text(sh, "Each card gives the meaning of one idea in a few words")
    tb = strip_of(src); el = copy.deepcopy(tb._element)
    nid = max(int(x) for x in s._element.xpath("//p:cNvPr/@id")) + 1
    el.xpath(".//p:cNvPr")[0].set("id", str(nid)); el.xpath(".//p:cNvPr")[0].set("name", "Part strip")
    hs = [int(h) for h in el.xpath(".//a:tr/@h")]
    ext = el.xpath("./p:xfrm/a:ext")[0]; ext.set("cy", str(sum(hs)))
    s.shapes._spTree.append(el)

# ---------------------------------------------------------------- tables: the analogy column goes
def drop_last_col(tbl_shape):
    t = tbl_shape._element.xpath(".//a:tbl")[0]
    cols = t.xpath("./a:tblGrid/a:gridCol"); total = sum(int(c.get("w")) for c in cols)
    cols[-1].getparent().remove(cols[-1])
    for tr in t.xpath("./a:tr"):
        tcs = tr.xpath("./a:tc"); tr.remove(tcs[-1])
    cols = t.xpath("./a:tblGrid/a:gridCol"); keep = sum(int(c.get("w")) for c in cols)
    acc = 0
    for k, c in enumerate(cols):
        w = round(int(c.get("w")) * total / keep) if k < len(cols) - 1 else total - acc
        c.set("w", str(w)); acc += w
for i, nm in ((46, "wallet table"), (62, "first bitcoin table"), (68, "computing table")):
    tb = by_name(S(i), nm)[0]
    assert [c.text for c in tb.table.rows[0].cells][-1] == "Think of", i
    drop_last_col(tb)

# ---------------------------------------------------------------- the key slide: a registry against the key; the house pictures go
s = S(49)
set_text(by_name(s, "Text 3")[0], "A registry names the owner; in Bitcoin the key does both jobs")
set_text(by_text(s, "your house")[0], "a registered asset")
set_text(by_text(s, "One key opens it")[0], "A key opens it, but a registry records who owns it. Lose the key and the registry still names you.")
set_text(by_text(s, "The key IS the deed")[0], "No registry exists. Signing with the key is the only proof of ownership there is.")
for nm in ("Shape 5", "Shape 6", "Shape 13", "Shape 14"): delete(by_name(s, nm)[0])
for nm in ("Shape 7", "Shape 8", "Shape 9", "Shape 15", "Shape 16", "Shape 17"):
    sh = by_name(s, nm)[0]; sh.left = sh.left - int(1.1 * E)

# ---------------------------------------------------------------- other analogy wording
set_text(by_text(S(7), "Block 0 is a dated receipt")[0], "Block 0 carries a verifiable date and a message at once, and anyone can read it on a block explorer today.")
sh = by_text(S(63), "A coin is spent whole")[0]; set_text(sh, "A coin is spent whole, and the change returns as a new output.")
for sh in by_text(S(74), "If a line feels unproven"): set_text(sh, "If a line feels unproven, its code slide carries the evidence")

# every remaining analogy: a shape that is only the analogy goes, otherwise the sentence goes
def walk(shs):
    for x in shs:
        if x.shape_type == T.GROUP: yield from walk(x.shapes)
        else: yield x
for i, s in enumerate(p.slides, 1):
    for sh in list(walk(s.shapes)):
        if not sh.has_text_frame: continue
        t = tx(sh)
        if sh.name == "tile analogy" or re.match(r"^\s*(▪\s*)?Think of", t): say("delete", i, sh.name, repr(t[:50])); delete(sh); continue
        m = RX.search(t)
        if m and len(sh.text_frame.paragraphs) == 1:
            new = sentence_cut(t, m); say("cut", i, sh.name, repr(t[:70]), "->", repr(new[:70])); set_text(sh, new)

# ---------------------------------------------------------------- results are results, not code frames; explanations are balloon notes
for i, s in enumerate(p.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame and (sh.name.startswith("result ") or sh.name == "tile example"):
            for q in sh.text_frame.paragraphs:
                for r in q.runs:
                    if r.font.name == "Courier New": r.font.name = "Consolas"
    seq = list(s.shapes); k = 0
    if any(x.name.startswith("code ") for x in seq):
        for a, b in zip(seq, seq[1:]):
            if a.has_text_frame and re.fullmatch(r"\d", tx(a).strip()) and b.has_text_frame and len(tx(b).split()) >= 6 and b.name.startswith("Text"):
                k += 1; b.name = "Balloon note %d" % k

# ---------------------------------------------------------------- story slides: 5N1K in the alt text of the story boxes (invisible)
TAGS = {"story head": "when where who", "lesson": "why"}
n_story = 0
for i, s in enumerate(p.slides, 1):
    st = [x for x in s.shapes if x.name == "story"]
    if not st: continue
    n_story += 1
    for x in s.shapes:
        if x.name == "story head": x._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", "when where who")
    for x, tag in zip(st, ("what", "how", "why")): x._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", tag)
    assert len(st) == 3, (i, len(st))
say("story slides", n_story)

# ---------------------------------------------------------------- the diagrams are one figure each
GROUP = [2, 3, 4, 11, 24, 29, 34, 35, 40, 43, 48, 49, 50, 52, 57, 65, 66, 67, 73, 74, 75]
for i in GROUP:
    s = S(i)
    mem = [x for x in s.shapes if 1.2 * E <= x.top < 4.98 * E and x.name != "Part strip"]
    assert len(mem) >= 4, (i, len(mem))
    grp = s.shapes.add_group_shape(shapes=mem); grp.name = "Figure"
    say("group", i, len(mem))

# ---------------------------------------------------------------- notes
for i, s in enumerate(p.slides, 1):
    s.notes_slide.notes_text_frame.text = NOTES[i]
p.save(DST)
open(os.path.join(H, "ch01-deck", "deck_patch_v1_0_0_report.txt"), "w").write("\n".join(LOG) + "\n")
print("written", DST)
