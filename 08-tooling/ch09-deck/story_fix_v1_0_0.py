#!/usr/bin/env python3
"""story_fix v1.0.0 (chapter 9 deck 2.2.0) - the D5 pattern of the deck standard applied to the four story slides of the generated deck, as the course deck 2.1.0 has it: the first three beat boxes are renamed
'Story Text 1..3' and tagged with their 5N1K coverage in the alt-text (p:cNvPr/@descr; the union of the three covers who, what, when, where, why and how), the 4th beat stays an ordinary text box, the WHO / WHERE / WHEN
chips (visible all-caps labels, banned) are deleted with their frames, and the READ chip is widened over the freed row. A story slide is found by its picture and its READ chip. Usage: story_fix_v1_0_0.py IN OUT"""
__version__ = "1.0.0"
import sys
from pptx import Presentation
from pptx.util import Inches

TAGS = {"A node that only listens to replacements": ["what when where who", "why", "how"],
        "A pre-signed payment cannot guess its fee": ["what when where who", "why", "how"],
        "Block 840,000: fees were nearly the reward": ["what when where who", "why", "how"],
        "What if nobody got a subsidy?": ["what when where who", "who why", "how"]}
# the beat boxes are found by their geometry: left 4.4 in, in the story column, in the order of their top
def main(a, b):
    prs = Presentation(a); n = 0
    for s in prs.slides:
        title = next((sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.name == "Text 2"), None)
        if title not in TAGS: continue
        boxes = sorted([sh for sh in s.shapes if sh.has_text_frame and abs(sh.left - Inches(4.4)) < 20000 and sh.name.startswith("Text")], key=lambda x: x.top)
        assert len(boxes) == 4, (title, len(boxes))
        for k, (sh, tg) in enumerate(zip(boxes[:3], TAGS[title]), 1):
            sh.name = "Story Text %d" % k; sh._element.nvSpPr.cNvPr.set("descr", tg)
        shapes = list(s.shapes); kill = []
        for i, sh in enumerate(shapes):
            if sh.has_text_frame and sh.text_frame.text.split(" ")[0] in ("WHO", "WHERE", "WHEN"):
                kill += [sh, shapes[i - 1]]
        for sh in kill: sh._element.getparent().remove(sh._element)
        read = [sh for sh in s.shapes if sh.has_text_frame and sh.text_frame.text.startswith("READ")][0]
        frame = [sh for sh in s.shapes if not sh.has_text_frame or (sh.shape_type == 1 and not sh.text_frame.text)][-1]
        frame = [sh for sh in s.shapes if sh.shape_type == 1 and not sh.text_frame.text and abs(sh.top - read.top) < 20000][0]
        frame.left, frame.width = Inches(0.5), Inches(9.0); read.left, read.width = Inches(0.6), Inches(8.84)
        n += 1
    prs.save(b); print("story_fix: %d story slides" % n)


if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
