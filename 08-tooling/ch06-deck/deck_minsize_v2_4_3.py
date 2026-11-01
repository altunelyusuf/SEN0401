#!/usr/bin/env python3
"""deck_minsize v2_4_3: makes the chapter 6 deck v2_4_3 from v2_4_2 (read only). Every text run below 9 pt is raised to 9 pt (the caption detail line of the 18 console slides from 8.5; the READ box of slides 11, 26, 41 and 50 from 7.5 and 7.0; the description lines of slide 70 from 8.0). No text is shortened or changed. Where the larger size needs room the box is reflowed: on slide 70 the rows become 34.9 pt tall (two lines of 9 pt under the 10 pt title) and the sections are re-spaced down each column, every bullet moving with its row. Nothing else changes. Usage: SRC DST CHANGELOG"""
import sys
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.util import Pt
src, dst, log = sys.argv[1:4]; pr = Presentation(src); out = []
MIN = Pt(9)
for n, s in enumerate(pr.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.font.size is not None and r.font.size < MIN:
                        out.append("slide %d | %s | %.1f -> 9.0 pt | %r" % (n, sh.name, r.font.size.pt, r.text[:50])); r.font.size = MIN
HEAD, ROW, PITCH, GAP, Y0 = 205000, 443000, 450000, 47000, 1190000
s70 = pr.slides[69]; sh70 = list(s70.shapes)
heads = [x for x in sh70 if x.has_text_frame and x.height == 274320]
rows = [x for x in sh70 if x.has_text_frame and x.height == 384048 and len(x.text_frame.paragraphs) == 2]
buls = [x for x in sh70 if x.width == 82296 and x.height == 82296]
for c in (0, 1):
    inc = lambda x: (x.left >= 4000000) == bool(c)
    items = sorted([("h", x) for x in heads if inc(x)] + [("r", x) for x in rows if inc(x)], key=lambda t: t[1].top)
    bs = sorted([x for x in buls if inc(x)], key=lambda x: x.top)
    rs_sorted = [x for k, x in items if k == "r"]; assert len(bs) == len(rs_sorted)
    pair = {id(r): b for r, b in zip(rs_sorted, bs)}
    y = Y0; first = True
    for k, x in items:
        if k == "h":
            if not first: y += GAP
            x.top = y; x.height = HEAD; y += HEAD
            out.append("slide 70 | heading %r moved to top %d" % (x.text_frame.text, x.top))
        else:
            x.top = y; x.height = ROW; pair[id(x)].top = y + 73152; y += PITCH
            out.append("slide 70 | row %r moved to top %d, height %d" % (x.text_frame.paragraphs[0].text[:40], x.top, x.height))
        first = False
    out.append("slide 70 | column %d ends at %d" % (c, y - (PITCH - ROW)))
pr.save(dst); open(log, "w").write("\n".join(out) + "\n"); print(len(out), "changes")
