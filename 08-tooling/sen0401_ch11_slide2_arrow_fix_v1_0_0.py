#!/usr/bin/env python3
"""sen0401_ch11_slide2_arrow_fix v1.0.0 - removes the one arrow on slide 2 that ran from the route boxes into the number boxes (a fault of sen0401_ch11_rulings_fix v1.0.0). Reads deck v2.3.0, writes v2.4.0."""
import os
from pptx import Presentation
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(R, "03-materials", "ch11")
src = os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v2_3_0.pptx"); dst = os.path.join(D, "SEN0401_Ch11_TheBlockchain_3e_v2_4_0.pptx")
assert not os.path.exists(dst)
p = Presentation(src); s = p.slides[1]; E = 914400; n = 0
for sh in list(s.shapes):
    if sh.name.startswith("Connector") and sh.left + sh.width > 6.0 * E:
        sh._element.getparent().remove(sh._element); n += 1
print("removed", n); p.save(dst)
