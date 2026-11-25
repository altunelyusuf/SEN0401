#!/usr/bin/env python3
"""Chapter 2 deck v3_2_0 -> v3_3_0 (deck standard v3.1.0, CME material check v1.2.0). Reads the committed v3_2_0, never edits it.
Changes: part-slide and short titles of four or more words; every everyday-analogy shape removed; monospace result, digit and
bit shapes drawn in Consolas (only the 'code N' boxes stay Courier New); 59 reader-facing notes of 60-140 words; the 5N1K
alt text of the three story slides; diagram shapes of slides without a picture, table or chart grouped as one diagram."""
__version__ = "1.0.0"
import re, sys, os
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
sys.path.insert(0, os.environ.get("NOTES_DIR", os.path.dirname(os.path.abspath(__file__))))
from sen0401_ch02_notes_v1_0_0 import NOTES
SRC, OUT = sys.argv[1], sys.argv[2]
RX = re.compile(r"(\b(it is like|(works|acts|behaves) like (a|an|the)|is like (a|an|the)|are like (a|an|the)|think of|imagine|just as|picture a|everyday (comparison|analogy|life)|analogy|wax seal|sealed envelope|cheque|(a|the|older|wax) seal|speed limit|road standard)\b)|((^|[.!?]\s+)like (a|an|the|two)\s)", re.I)
TITLES = {2: "Today's route through one payment", 5: "Part 2: Buying from an Online Store", 9: "Reading Bob's invoice link", 11: "Part 3: Bitcoin Transactions",
          12: "Inputs and outputs of one payment", 22: "Part 4: Coin Selection", 27: "Part 5: Constructing a Transaction",
          33: "Part 6: Adding the Transaction to the Blockchain", 48: "Part 7: Spending the Transaction"}
STORY = {7: ["when where", "who what why", "when what how", "who what how", "who when why"],
         45: ["when where", "who what when where", "who why how", "what how", "what why how"],
         51: ["when where", "what when", "what why how", "who when how", "who what why"]}
p = Presentation(SRC)
def walk(shs):
    for x in shs:
        yield x
        if x.shape_type == T.GROUP: yield from walk(x.shapes)
removed = 0
for i, s in enumerate(p.slides, 1):
    if i in TITLES:                                   # the first text box that is not the logo chip is the title
        for sh in s.shapes:
            if sh.has_text_frame and len(sh.text_frame.text.strip()) > 2:
                r0 = sh.text_frame.paragraphs[0].runs[0]; r0.text = TITLES[i]
                for r in sh.text_frame.paragraphs[0].runs[1:]: r.text = ""
                break
    for sh in list(walk(s.shapes)):
        if sh.has_text_frame and RX.search(sh.text_frame.text):
            if sh.name.startswith("story") or sh.name == "lesson": raise SystemExit("analogy in a story shape on slide %d" % i)
            sh._element.getparent().remove(sh._element); removed += 1
    if i == 50:                                       # the sudoku picture is an everyday comparison: its drawing, labels and card go
        for sh in list(s.shapes):
            if sh.name.startswith("sd ") or sh.name.endswith("SudokuAnalogy") or (sh.has_text_frame and sh.text_frame.text.startswith(("Hard to solve", "Empty cells are found"))):
                sh._element.getparent().remove(sh._element); removed += 1
            elif sh.has_text_frame and "sudoku picture" in sh.text_frame.text:
                sh.text_frame.paragraphs[0].runs[0].text = "Coinbase, reward and mining pools"
                for r in sh.text_frame.paragraphs[0].runs[1:]: r.text = ""
    names = {sh.name[8:] for sh in s.shapes if sh.name.startswith("concept ")}      # a card without its concept text is an empty frame
    for sh in list(s.shapes):
        if sh.name.startswith(("card ", "bar ")) and sh.name.split(" ", 1)[1] not in names:
            sh._element.getparent().remove(sh._element); removed += 1
    for sh in walk(s.shapes):
        if sh.has_text_frame and not sh.name.startswith("code"):
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.name == "Courier New": r.font.name = "Consolas"
    s.notes_slide.notes_text_frame.text = NOTES[i]
    if i in STORY:
        boxes = [sh for sh in s.shapes if sh.has_text_frame and sh.name.lower().startswith("story")]
        for sh, tags in zip(boxes, STORY[i]):
            sh._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", "5N1K: " + tags)
HEAD = ("card", "bar ", "concept", "number", "Rounded Rectangle 1", "TextBox 2", "TextBox 3", "TextBox 5", "TextBox 6", "Rectangle 4")
def has_vis(s):
    return any(sh.shape_type in (T.PICTURE, T.CHART, T.TABLE, T.GROUP) or (sh.has_text_frame and sh.name != "chip" and any(r.font.name == "Courier New" for pa in sh.text_frame.paragraphs for r in pa.runs)) for sh in s.shapes)
grouped = []
for i, s in enumerate(p.slides, 1):
    if has_vis(s) or i in (1, len(p.slides)) or TITLES.get(i, "").startswith("Part"): continue
    members = [sh for sh in s.shapes if sh.top >= 1150000 and sh.top < 4560000 and not sh.name.startswith(HEAD) and not (sh.name.startswith("TextBox") and sh.width > 7000000 and False)]
    if i in (2, 3): members = [sh for sh in s.shapes if sh.top >= 1150000 and sh.top < 4560000]
    if len(members) >= 3:
        g = s.shapes.add_group_shape(members); g.name = "diagram"; grouped.append(i)
p.save(OUT)
print("removed analogy shapes:", removed, "| grouped diagrams on slides:", grouped)
