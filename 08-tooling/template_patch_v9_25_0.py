#!/usr/bin/env python3
"""SEN0401 page template 9.25.0, from 9.24.0.
One change: on a narrow screen the progress badge in the title bar no longer forces the bar wider than the
viewport. At 390 px with the reader's text size raised to 120-130% the badge ("v 12/117", three digits once a
chapter has 100 or more concepts) pushed the fixed-width row 3 px past the window, which showed as a sideways
scroll. Below 700 px the badge now takes a smaller type size and a smaller left margin, and it is allowed to
shrink and clip rather than push, so the row fits at every text size the control offers.
Chapters 1, 3 and 5 worked around this in their own extra stylesheet; those rules are now redundant but harmless.
usage: template_patch_v9_25_0.py [IN.html OUT.html]"""
__version__ = "9.25.0"
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_24_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_25_0.html")
h = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    assert h.count(a) == n, (a[:60], h.count(a))
    return h.replace(a, b)
h = rep("@media (max-width:340px){#progBadge{display:none}}",
        "@media (max-width:700px){#progBadge{margin-left:.25rem;font-size:.7rem;flex:0 1 auto;min-width:0;overflow:hidden}}\n"
        "@media (max-width:340px){#progBadge{display:none}}")
open(out, "w", encoding="utf-8").write(h)
print("wrote", os.path.basename(out), len(h), "bytes")
