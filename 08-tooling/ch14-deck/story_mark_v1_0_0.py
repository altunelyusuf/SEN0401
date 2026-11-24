#!/usr/bin/env python3
"""story_mark v1.0.0 (chapter 14 deck 2.2.0): names the narrative beat boxes of the four story slides 'Story beat N' removes the visible WHO/WHERE/WHEN chips (READ widened), and gives each its 5N1K tags in the alt text (invisible metadata, ruling of 2026-11-09). Usage: story_mark_v1_0_0.py IN OUT"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pptx import Presentation
from pptx.util import Inches
import sen0401_deck_story_fix_v1_0_0 as F
TAGS = [["what", "when", "who"], ["why", "where"], ["how"], ["what", "why", "how"]]
STORY_SLIDES = [8, 23, 34, 37]
p = Presentation(sys.argv[1])
for n in STORY_SLIDES:
    s = p.slides[n - 1]
    boxes = [sh for sh in s.shapes if sh.has_text_frame and sh.name.startswith("Text ") and 40 < len(sh.text_frame.text) < 400 and not sh.text_frame.text.startswith(("WHO", "WHERE", "WHEN", "READ", "Picture"))]
    boxes = sorted(boxes, key=lambda b: (b.top, b.left))[:4]
    for k, b in enumerate(boxes):
        b.name = "Story beat %d" % (k + 1)
        b._element.xpath("./p:nvSpPr/p:cNvPr")[0].set("descr", "5N1K " + " ".join(TAGS[k]))
    chips = F.find_chip_shapes(s)
    left0 = min(r[0].left for r in chips.values()); right0 = max(r[0].left + r[0].width for r in chips.values())
    for lab in ("WHO", "WHERE", "WHEN"):
        for sh in chips[lab]: sh._element.getparent().remove(sh._element)
    rr, rt = chips["READ"]; rr.left = left0; rr.width = right0 - left0; rt.left = left0 + Inches(0.1); rt.width = right0 - left0 - Inches(0.16)
    print("slide", n, "story boxes", len(boxes))
p.save(sys.argv[2])
