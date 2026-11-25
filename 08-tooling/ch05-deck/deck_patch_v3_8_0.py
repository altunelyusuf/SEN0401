#!/usr/bin/env python3
"""deck_patch v3.8.0 (SEN0401 chapter 5): the deck 3.7.0 -> 3.8.0 under the owner rulings of 2026-11-14 and 2026-11-24 (the Chapter 7-14 standard). Never edits 3.7.0.
  * titles of at least four words (slides 2 and 65); a visual on every slide: the cards, rows and boxes of slides 2, 3, 14, 63, 66 and 67 are grouped into named visual groups;
  * result lines (the highlighted printed row) are no longer set in the code font, so only code counts as code; every code box parses on its own (statements are not cut between boxes, at most 30 words a box);
  * no everyday analogy: the eleven 'Everyday pictures' tables become concept guides (concept, slides that show it, meaning in the wallet), with new titles, subtitles and takeaways;
  * balloons are named 'Balloon note N'; story boxes are named 'Story Text N' and carry their 5N1K elements in the alt text (invisible); 
  * the notes of all 68 slides are written for the reader (60 to 140 words, no presenter direction).
Usage: python3 deck_patch_v3_8_0.py SRC.pptx OUT.pptx   (also writes deck_notes_v3_8_0.json beside this script)"""
__version__ = "3.8.0"
import ast, copy, importlib.util, json, os, sys
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = sys.argv[1], sys.argv[2]
NSA = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
p = Presentation(SRC); S = list(p.slides)
assert len(S) == 68
LOG = []
def say(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)

def load(name):
    sp = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py")); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
NOTES = {}; NOTES.update(load("deck_notes_v3_8_0_text_a").N); NOTES.update(load("deck_notes_v3_8_0_text_b").N)
assert sorted(NOTES) == list(range(1, 69))

def by_name(slide, name): return [s for s in slide.shapes if s.name == name]
def set_text(shape, text):
    """set the text of a shape or table cell frame: the first run keeps its formatting, the other runs and paragraphs go"""
    tf = shape.text_frame; para = tf.paragraphs[0]
    runs = para.runs
    runs[0].text = text
    for r in runs[1:]: r._r.getparent().remove(r._r)
    for pa in tf.paragraphs[1:]: pa._p.getparent().remove(pa._p)

# ------------------------------------------------------------------ 1. titles
set_text(S[1].shapes.title, "Today's route through seven parts")
set_text(S[64].shapes.title, "Check yourself against the code slides")

# ------------------------------------------------------------------ 2. the eleven concept guides (no everyday analogy)
GUIDE = {
 10: ("Concept guide for part 1", "Each concept, the slides that show it, and what it means in the wallet", "One seed and a rule replace a bag of separate keys.",
      ["7, 8", "7, 9", "7, 11", "7, 11", "7, 47", "8, 61", "1, 2", "4, 8"]),
 15: ("Concept guide for part 2, schemes", "Each scheme, the slides that show it, and what it adds", "Seven schemes; each one trades simplicity for another strength.",
      ["12, 13", "13, 19", "13, 17", "13", "13", "13, 18", "13, 17"]),
 16: ("Concept guide for part 2, choices", "Each choice, the slides that show it, and what it means for a backup", "A passphrase is a second secret: lose it, and the words alone open nothing.",
      ["12, 28", "14", "14", "12, 14", "14", "12, 13", "14, 28"]),
 29: ("Concept guide for part 3", "Each concept, the slides that show it, and what it does in the BIP39 stack", "Entropy, checksum, word list, stretching: that is a recovery code.",
      ["19, 21, 23", "21, 25", "21, 24", "19, 27", "27", "27", "19, 27"]),
 30: ("Concept guide for part 3, book sections", "Each section of the book, the slides that show it, and what it covers", "More entropy means more words; a passphrase adds a second secret.",
      ["19, 22", "21, 24", "26, 27", "23", "28"]),
 40: ("Concept guide for part 4, the tree", "Each concept, the slides that show it, and what it means in the tree", "A parent, a chain code and an index make a child key.",
      ["31, 33", "31, 33", "34, 35", "33, 34", "35, 39"]),
 41: ("Concept guide for part 4, extended keys", "Each concept, the slides that show it, and what it can do", "Give out the xpub, never the xprv.",
      ["38", "38", "37, 38", "35, 36"]),
 42: ("Concept guide for part 4, book sections", "Each section of the book, the slides that show it, and what it covers", "One tree, and a hardened step that protects the parent.",
      ["9, 32", "33", "34", "36", "38", "37", "35", "39"]),
 51: ("Concept guide for part 5", "Each concept, the slides that show it, and what it means for a backup", "A path names one key; a descriptor describes the whole wallet.",
      ["44", "44", "44, 45", "45, 48", "46, 48", "49, 50"]),
 52: ("Concept guide for part 5, book sections", "Each section of the book, the slides that show it, and what it covers", "Write the path down with the code, or the key cannot be found again.",
      ["48, 49", "44", "32, 44"]),
 64: ("Concept guide for parts 6 and 7", "Each concept, the slides that show it, and what it means for a backup", "Labels, channel state and scan limits each need their own backup or setting.",
      ["54", "54", "55", "59", "53, 55", "59", "58"]),
}
for n, (title, sub, take, slides) in GUIDE.items():
    s = S[n - 1]; tbl = by_name(s, "analogy table")[0]; t = tbl.table
    assert len(list(t.rows)) - 1 == len(slides), (n, len(list(t.rows)) - 1, len(slides))
    assert [c.text for c in t.rows[0].cells] == ["Concept", "In everyday life", "In the wallet"], n
    set_text(t.cell(0, 1), "Shown on slides")
    for k, v in enumerate(slides, 1): set_text(t.cell(k, 1), v)
    for c, w in zip(t.columns, (300, 150, 450)): c.width = Emu(w * 9144)
    tbl.name = "concept guide"
    set_text(s.shapes.title, title)
    set_text(by_name(s, "subtitle")[0], sub); set_text(by_name(s, "takeaway")[0], take)
say("concept guides rewritten:", len(GUIDE))

# ------------------------------------------------------------------ 3. visual groups
def group(slide, shapes, name):
    g = slide.shapes.add_group_shape(shapes=shapes); g.name = name; return g
def inside(c, o): 
    cx, cy = o.left + o.width / 2, o.top + o.height / 2
    return c.left <= cx <= c.left + c.width and c.top <= cy <= c.top + c.height
def pairs(slide, a, b, prefix):
    A = sorted(by_name(slide, a), key=lambda x: x.top); B = sorted(by_name(slide, b), key=lambda x: x.top)
    assert len(A) == len(B), (slide.slide_id, a, len(A), len(B))
    for k, (x, y) in enumerate(zip(A, B), 1): group(slide, [x, y], "%s %d" % (prefix, k))
pairs(S[1], "route number", "route row", "visual: route step")
for k, c in enumerate(sorted(by_name(S[1], "stat card"), key=lambda x: x.top), 1):
    mem = [c] + [x for x in S[1].shapes if x.name in ("stat number", "stat label") and inside(c, x)]
    assert len(mem) == 3, (k, len(mem)); group(S[1], mem, "visual: counter %d" % k)
pairs(S[2], "question number", "question", "visual: question")
for k, c in enumerate(sorted(by_name(S[13], "card"), key=lambda x: (x.top, x.left)), 1):
    mem = [c] + [x for x in S[13].shapes if x.name in ("card heading", "card text") and inside(c, x)]
    assert len(mem) == 3, (k, len(mem)); group(S[13], mem, "visual: card %d" % k)
group(S[62], by_name(S[62], "backup item") + by_name(S[62], "test step"), "visual: complete backup")
pairs(S[65], "line number", "summary line", "visual: summary line")
res = [x for x in S[66].shapes if x.name.startswith("resources ")]
group(S[66], res, "visual: resource groups")
say("visual groups added on slides 2, 3, 14, 63, 66, 67")

# ------------------------------------------------------------------ 4. result lines are not code
n_res = 0
for s in S:
    for sh in s.shapes:
        if sh.name.startswith("result line") and sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs: r.font.name = "Consolas"; n_res += 1
say("result-line runs moved to Consolas:", n_res)

# ------------------------------------------------------------------ 5. every code box parses on its own
def W(t): return len(t.split())
def lines_of(box): return list(box.text_frame._txBody.findall(NSA + "p"))
def ptext(pe): return "".join(t.text or "" for t in pe.iter(NSA + "t"))
n_fixed = 0
for i, s in enumerate(S, 1):
    boxes = sorted([x for x in s.shapes if x.has_text_frame and x.name.startswith("code ") and " (part" not in x.name], key=lambda x: x.top)
    if not boxes: continue
    bad = False
    for b in boxes:
        try: ast.parse(b.text_frame.text)
        except SyntaxError: bad = True
    if not bad: continue
    P = [pe for b in boxes for pe in lines_of(b)]; cnt = [len(lines_of(b)) for b in boxes]
    src = "\n".join(ptext(pe) for pe in P); tree = ast.parse(src)
    spans = [(st.lineno - 1, st.end_lineno - 1) for st in tree.body]
    bounds = [0]
    for k in range(len(boxes)): bounds.append(bounds[-1] + cnt[k])
    for k in range(1, len(boxes)):
        bd = bounds[k]
        for a, e in spans:
            if a < bd <= e: bd = a if a > bounds[k - 1] else e + 1
        bounds[k] = bd
    assert bounds == sorted(bounds), (i, bounds)
    old_tops = [b.top for b in boxes]; old_h = [b.height for b in boxes]; per = [h / max(1, c) for h, c in zip(old_h, cnt)]
    for k, b in enumerate(boxes):
        body = b.text_frame._txBody
        for pe in lines_of(b): body.remove(pe)
        for pe in P[bounds[k]:bounds[k + 1]]: body.append(pe)
    keep = [k for k in range(len(boxes)) if bounds[k + 1] > bounds[k]]
    merged = len(keep) < len(boxes)
    for k in range(len(boxes)):
        if k not in keep: boxes[k]._element.getparent().remove(boxes[k]._element)
    for k in keep: assert W(boxes[k].text_frame.text) <= 30 and ast.parse(boxes[k].text_frame.text), (i, k, boxes[k].text_frame.text)
    gaps = [old_tops[k + 1] - (old_tops[k] + old_h[k]) for k in range(len(boxes) - 1)]
    span = old_tops[-1] + old_h[-1] - old_tops[0]; g = int(sum(gaps) / max(1, len(gaps))) if gaps else 0
    nlines = sum(bounds[k + 1] - bounds[k] for k in keep); room = span - g * (len(keep) - 1)
    top = old_tops[0]
    for k in keep:
        b = boxes[k]; nl = bounds[k + 1] - bounds[k]; b.top = Emu(int(top)); b.height = Emu(int(room * nl / nlines)); top = b.top + b.height + g
    n_fixed += 1; say("slide %d: code boxes re-cut at statement boundaries %s" % (i, [bounds[k + 1] - bounds[k] for k in range(len(boxes))]))
say("slides with re-cut code boxes:", n_fixed)

# ------------------------------------------------------------------ 6. balloon names; story boxes
for i, s in enumerate(S, 1):
    bl = sorted(by_name(s, "explanation"), key=lambda x: (x.top, x.left))
    for k, b in enumerate(bl, 1): b.name = "Balloon note %d" % k
FIVE = {5: ("who what when where", "who when where why", "why how"), 20: ("who why", "when where what", "how"), 56: ("when who what where", "who where how", "why")}
for n, tags in FIVE.items():
    st = sorted([x for x in S[n - 1].shapes if x.name.startswith("story ")], key=lambda x: x.name)
    assert len(st) == 3, (n, len(st))
    for k, (b, tg) in enumerate(zip(st, tags), 1):
        b.name = "Story Text %d" % k
        b._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", tg)
say("story boxes named and tagged on slides 5, 20, 56")

# ------------------------------------------------------------------ 7. notes
out = {"meta": {"deck": "SEN0401 Chapter 5, deck 3.8.0", "rule": "notes of 60 to 140 words, full sentences, written for the reader; no presenter direction, no everyday analogy", "version": __version__}, "slides": []}
for i, s in enumerate(S, 1):
    t = " ".join(NOTES[i].split()); w = len(t.split()); assert 60 <= w <= 140, (i, w)
    s.notes_slide.notes_text_frame.text = t
    out["slides"].append({"slide": i, "title": s.shapes.title.text_frame.text, "words": w, "notes": t})
json.dump(out, open(os.path.join(HERE, "deck_notes_v3_8_0.json"), "w"), indent=1, ensure_ascii=False)
p.save(OUT)
say("written", OUT)
