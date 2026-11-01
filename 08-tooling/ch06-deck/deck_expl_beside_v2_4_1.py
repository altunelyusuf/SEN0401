#!/usr/bin/env python3
"""deck_expl_beside v2_4_1: makes the chapter 6 deck v2_4_1 from v2_4_0 (read only). On every code slide the left column is re-stacked as code box 1, its explanation, code box 2, its explanation, ..., then the result block, so that every code listing has its plain-language explanation within 0.6 inch (deck standard D3). Only the top of shapes changes (the result block moves as one piece); text, code, results, notes, pictures, links, widths and sizes are untouched. Usage: SRC DST CHANGELOG"""
import sys
sys.dont_write_bytecode = True
from pptx import Presentation
src, dst, log = sys.argv[1:4]; pr = Presentation(src); out = []
IN = 914400
for n, s in enumerate(pr.slides, 1):
    c = sorted([x for x in s.shapes if x.name.startswith("code ")], key=lambda x: x.top)
    if not c: continue
    e = sorted([x for x in s.shapes if x.name.startswith("explanation")], key=lambda x: x.top)
    r = [x for x in s.shapes if x.name.startswith("result")]
    assert len(c) == len(e), n
    y0 = min(x.top for x in c); end = max(x.top + x.height for x in e + r + c)
    rt = min(x.top for x in r); rb = max(x.top + x.height for x in r); rh = rb - rt
    used = sum(x.height for x in c + e) + rh
    gap = min(int(0.05 * IN), max(0, (end - y0 - used) // (len(c) * 2)))
    y = y0; before = {id(x): x.top for x in c + e + r}
    for a, b in zip(c, e):
        a.top = y; y += a.height + gap
        b.top = y; y += b.height + gap
    d = y - rt
    for x in r: x.top = x.top + d
    out.append("slide %d: %d listings re-stacked code/explanation pairs from %.2f in, result block now at %.2f-%.2f in (was %.2f), lowest edge %.2f in (was %.2f)" % (n, len(c), y0 / IN, (rt + d) / IN, (rb + d) / IN, rt / IN, (rb + d) / IN, end / IN))
pr.save(dst); open(log, "w").write("\n".join(out) + "\n"); print("\n".join(out))
