#!/usr/bin/env python3
"""deck_layout_fix v2_3_1 - makes the chapter 6 deck v2_3_1 from v2_3_0 (read only): only box geometry (height/top) of text frames the deck layout check v1_0_0 estimates as overflowing is changed, by growing the box into free space beside/above/below it; where there is no free space the font size is lowered in 0.5 pt steps (floor 9 pt). Text, notes, pictures, links, code and results are not touched. Usage: deck_layout_fix_v2_3_1.py SRC DST CHANGELOG"""
import sys, importlib.util
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.util import Emu, Pt
spec = importlib.util.spec_from_file_location("lc", "/home/claude/sen0401/08-tooling/deck_layout_check_v1_0_0.py")
lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
src, dst, log = sys.argv[1:4]
pr = Presentation(src); out = []
def box(s): return Emu(s.left).pt, Emu(s.top).pt, Emu(s.left + s.width).pt, Emu(s.top + s.height).pt
for n, slide in enumerate(pr.slides, 1):
    shapes = list(slide.shapes)
    for sh in lc.frames(slide):
        need, have, _ = lc.estimate(sh)
        if need <= have + 0.5: continue
        l, t, r, b = box(sh)
        above, below = 0.0, 1e9
        ab = [0.0]; be = [380.0]
        for o in shapes:
            if o is sh: continue
            ol, ot, orr, ob = box(o)
            if min(r, orr) - max(l, ol) < 2: continue
            if ot <= t - 0.5 and ob >= b + 0.5: continue  # container
            if ob <= t + 1.0: ab.append(ob)
            elif ot >= b - 1.0: be.append(ot)
        up_room = max(0.0, t - max(ab)); down_room = max(0.0, min(be) - b)
        grow = need - have + 0.2
        old = (round(t, 1), round(b - t, 1), None)
        d = min(grow, down_room); u = min(grow - d, up_room)
        if d + u >= grow - 1e-6:
            sh.top = Emu(int(sh.top - Pt(u))); sh.height = Emu(int(sh.height + Pt(d + u)))
            how = "box grown %.1f pt down, %.1f pt up" % (d, u)
        else:
            sh.top = Emu(int(sh.top - Pt(u))); sh.height = Emu(int(sh.height + Pt(d + u)))
            fs0 = None
            for _ in range(8):
                nd, hv, _w = lc.estimate(sh)
                if nd <= hv + 0.5: break
                for p in sh.text_frame.paragraphs:
                    for rr in p.runs:
                        if rr.font.size and rr.font.size.pt > 9:
                            fs0 = fs0 or rr.font.size.pt; rr.font.size = Pt(rr.font.size.pt - 0.5)
            how = "box grown %.1f down, %.1f up; font lowered from %s pt" % (d, u, fs0)
        nd, hv, _w = lc.estimate(sh)
        out.append("slide %d | %r | was top %.1f height %.1f | now top %.1f height %.1f | %s | check now %s" % (n, sh.text_frame.text[:50].replace("\n", " "), old[0], old[1], Emu(sh.top).pt, Emu(sh.height).pt, how, "ok" if nd <= hv + 0.5 else "STILL OVER (%.1f in %.1f)" % (nd, hv)))
pr.save(dst); open(log, "w").write("\n".join(out) + "\n"); print("\n".join(out)); print(len(out), "frames changed")
