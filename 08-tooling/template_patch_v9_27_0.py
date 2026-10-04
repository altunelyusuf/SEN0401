#!/usr/bin/env python3
"""SEN0401 page template 9.27.0, from 9.26.0.
One change: the About > Mission pane finds the course-learning-outcomes query by its name instead of by its
position in the sample list. It used to take SPARQL_SAMPLES[3], which is the outcomes query only in SEN0414's
default list; SEN0401 supplies its own samples from the course configuration, where position 3 is the research
findings query, so the pane asked the wrong question and never showed an outcome even once the course
ontologies were part of the corpus. It now takes the first sample whose name mentions learning outcomes and
falls back to position 3 when there is none, so both courses' lists work.
usage: template_patch_v9_27_0.py [IN.html OUT.html]"""
__version__ = "9.27.0"
import sys, os
here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_26_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_27_0.html")
h = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    assert h.count(a) == n, (a[:70], h.count(a))
    return h.replace(a, b)
h = rep("const rows=await sparql(SPARQL_SAMPLES[3][1]);",
        "const _lo=SPARQL_SAMPLES.find(s=>/learning outcome/i.test(s[0]))||SPARQL_SAMPLES[3];"
        "const rows=_lo?await sparql(_lo[1]):[];")
open(out, "w", encoding="utf-8").write(h)
print("wrote", os.path.basename(out), len(h), "bytes")
