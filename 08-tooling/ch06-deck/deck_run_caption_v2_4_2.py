#!/usr/bin/env python3
"""deck_run_caption v2_4_2: makes the chapter 6 deck v2_4_2 from v2_4_1 (read only). On each of the 18 console slides the first line of the result block, 'RESULT  Python 3.14.6 · the chapter setup defines ...', becomes the run caption 'What the run printed (run under Python 3.14.6) · setup: ...' (the owner-side decision of the coordinator is the words 'What the run printed (python 3.14.6)'; the honesty check v1.1.0 reads the words 'run under Python <version>', so the caption carries both). The caption line grows to 12.4 pt, the lines under it and the result panel move down by the same amount. Nothing else changes. Usage: SRC DST CHANGELOG"""
import sys, re
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.util import Pt
src, dst, log = sys.argv[1:4]; pr = Presentation(src); out = []
for n, s in enumerate(pr.slides, 1):
    sh = list(s.shapes)
    hd = [x for x in sh if x.name.startswith("result") and x.has_text_frame and x.text_frame.text.startswith("RESULT  Python 3.14.6")]
    if not hd: continue
    h = hd[0]; old = h.text_frame.text; runs = h.text_frame.paragraphs[0].runs
    rest = re.sub(r"^RESULT  Python 3\.14\.6 · ", "", old).replace("the chapter setup defines ", "setup: ").replace(" and ", ", ")
    runs[0].text = "What the run printed (run under Python 3.14.6)"; runs[0].font.size = Pt(10)
    for r in runs[2:]: r._r.getparent().remove(r._r)
    runs[1].text = " · " + rest; runs[1].font.size = Pt(8.5)
    dh = Pt(12.4) - h.height
    bg = [x for x in sh if x.name.startswith("result") and x.shape_type == 1 and not x.has_text_frame or (x.name.startswith("result") and x.shape_type == 1 and not x.text_frame.text.strip())]
    for x in sh:
        if x.name.startswith("result") and x is not h and x.top > h.top and x.shape_type != 1: x.top = x.top + dh
    for x in bg: x.height = x.height + dh
    h.height = Pt(12.4)
    out.append("slide %d | old: %r | new: %r" % (n, old, h.text_frame.text))
pr.save(dst); open(log, "w").write("\n".join(out) + "\n"); print(len(out), "slides changed")
