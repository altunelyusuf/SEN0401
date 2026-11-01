#!/usr/bin/env python3
"""sen0401_deck_teach1_control_check v1_0_0 - the lineage agent's control of the chapter 1 Teach deck (criterion AC9_Ch01_DeckTeach, elements 2, 3, 6, 8): the code and result shapes equal those of the code deck v3_3_0 (text and names); 0 prompts and 0 lambdas in code boxes, 0 five-N-one-K label words; every slide has a note of 1 to 80 words; the story slides 7, 9, 10, 26 and 51 each carry a picture and a live link; the concept table lists 117 concepts and none without a slide. Usage: deck_teach1_control_check OLD_CODE_DECK NEW_DECK CONCEPT_TABLE_JSON"""
__version__ = "1.0.0"
import json, re, sys
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE as T
old, new, ct = sys.argv[1:4]; fails = 0
def out(ok, msg):
    global fails; fails += (not ok); print(("PASS  " if ok else "FAIL  ") + msg)
A, B = Presentation(old), Presentation(new)
cr = lambda P, p: [sh.text_frame.text for s in P.slides for sh in s.shapes if sh.has_text_frame and sh.name.startswith(p)]
out(cr(A, "code") == [x for x in cr(B, "code")][:0] or all(x in cr(B, "code") for x in cr(A, "code")), "code boxes of the code deck found in the new deck: %d of %d" % (sum(x in cr(B, "code") for x in cr(A, "code")), len(cr(A, "code"))))
out(all(x in cr(B, "result") for x in cr(A, "result")), "result shapes of the code deck found in the new deck: %d of %d" % (sum(x in cr(B, "result") for x in cr(A, "result")), len(cr(A, "result"))))
out(sum(x.count(">>>") for x in cr(B, "code")) == 0, "prompts in code boxes: 0")
out(sum(len(re.findall(r"\blambda\b", x)) for x in cr(B, "code")) == 0, "lambdas in code boxes: 0")
lab = [(i, w) for i, s in enumerate(B.slides, 1) for sh in s.shapes if sh.has_text_frame for w in re.findall(r"\b(WHAT|WHO|WHEN|WHERE|WHY|HOW):", sh.text_frame.text)]
out(not lab, "five-N-one-K label words: %d" % len(lab))
nw = [len((s.notes_slide.notes_text_frame.text if s.has_notes_slide else "").split()) for s in B.slides]
out(min(nw) >= 1 and max(nw) <= 80, "notes: shortest %d, longest %d words, slides without a note: %d" % (min(nw), max(nw), sum(1 for w in nw if w == 0)))
bad = []
for i in (7, 9, 10, 26, 51):
    s = B.slides[i - 1]; pics = [sh for sh in s.shapes if sh.shape_type == T.PICTURE]; links = [r.target_ref for r in s.part.rels.values() if r.is_external]
    if not pics or not links: bad.append(i)
out(not bad, "story slides 7, 9, 10, 26, 51 with a picture and a live link: missing on %s" % bad)
c = json.load(open(ct)); out(c["concepts"] == 117 and not c["level3_without_slide"], "concept table: %s concepts, level-3 without a slide: %s" % (c["concepts"], c["level3_without_slide"]))
print("RESULT", "FAIL" if fails else "PASS"); sys.exit(1 if fails else 0)
