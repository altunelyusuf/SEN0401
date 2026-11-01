#!/usr/bin/env python3
"""Chapter 1 deck v3.5.0 (a NEW tool file): the deck v3.4.0 is read, never written (SHA-256 before and after). ONE kind of change: no text run below 9 pt.
The READ link boxes of the nine story slides get 11 pt for the word READ and 10 pt for the link text and its source; the resources slide (75) gets 9 pt for its 12 description lines, and its left-column boxes are widened
from 410 to 440 units so that no description wraps. Nothing else changes (text, notes, shapes, code and results are as in v3.4.0). Also writes deck_plan_v3_5_0.json (the plan of v3_4_0 with the version).
Usage: deck_size_v3_5_0.py OLD NEW PLAN_OLD PLAN_NEW"""
import hashlib, json, sys
from pptx import Presentation
from pptx.util import Pt, Emu
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
old, new, po, pn = sys.argv[1:5]; b = sha(old); print("SHA-256 old deck before:", b)
prs = Presentation(old); U = 9144; n = 0
for i, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        if not sh.has_text_frame: continue
        small = [r for pa in sh.text_frame.paragraphs for r in pa.runs if r.font.size and r.font.size.pt < 9]
        if not small: continue
        if i != 75 and sh.name == "Text 18":
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size and r.font.size.pt < 9: r.font.size = Pt(11 if r.text.strip() == "READ" else 10); n += 1
        else:
            for r in small: r.font.size = Pt(9); n += 1
            if i == 75 and sh.left // U == 72 and sh.width // U == 410: sh.width = Emu(440 * U)
prs.core_properties.version = "3.5.0"; prs.save(new)
a = sha(old); print("SHA-256 old deck after: ", a, "UNCHANGED" if a == b else "CHANGED"); assert a == b
print("runs raised:", n, "new", sha(new))
pl = json.load(open(po)); pl["meta"]["version"] = "3.5.0"; json.dump(pl, open(pn, "x"), indent=1, ensure_ascii=False)
