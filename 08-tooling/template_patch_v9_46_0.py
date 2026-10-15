#!/usr/bin/env python3
"""template_patch v9_46_0 - writes course_page_template_v9_46_0.html from SEN0401's course_page_template_v9_45_0.html (committed, untouched). Two changes, found on the chapter 9 page by the page test 9.34.0:
 1. the concept pills of a section's breadcrumb stay on the breadcrumb's one row and scroll sideways when they do not fit (the same rule as SEN0414's template 9.47.0, copied unchanged): a section whose
    concepts have long names ("Forgotten change becomes fee", "No fee field in transaction") wrapped them to a second row, which put a focused concept's first paragraph at 269 px, below the 240 px the test asks;
 2. NEW: Untangle of the entity-relationship diagram keeps two entities joined by a relationship far enough apart for the relationship's label: the swap cost gets a penalty (8 times the relationship's weight)
    for a pair that sits side by side or one above the other with less than 26 px between the boxes. On chapter 9's diagram Untangle had put "Package relay" directly above "Minimum rates" with a 2 px gap, so the
    line between them lay inside the gap and its label had no place that is over neither box (3 labels became 2; the page rule is to leave a label out rather than draw it over an entity).
SEN0414's templates 9.46.0 (exercise tokens outside helper functions), 9.48.0 (no number change in a while loop) and 9.49.0/9.50.0 (pictures in paragraphs; exec-wrapped codes) are NOT ported: chapter 9's
examples are plain expressions without helpers, loops or pictures in paragraphs. Refuses when a text to replace is not found exactly once."""
__version__ = "1.0.0"
import os
H = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(H, "course_page_template_v9_45_0.html"), encoding="utf-8").read()
def rep(o, n):
    global s
    if s.count(o) != 1: raise SystemExit("REFUSED: %d occurrences of %r" % (s.count(o), o[:80]))
    s = s.replace(o, n)
rep("<!-- course_page_template version 9.45.0:", "<!-- course_page_template version 9.46.0: (SEN0401) the concept pills of a section's breadcrumb stay on its one row and scroll sideways when they do not fit (SEN0414's 9.47.0 rule), and Untangle of the entity-relationship diagram keeps two related entities 26 px apart or more, so that the label of their relationship has a place; otherwise identical to 9.45.0. Earlier: --><!-- course_page_template version 9.45.0:")
rep(".leafpick{gap:.25rem;margin:0 .2rem}\n", ".leafpick{gap:.25rem;margin:0 .2rem}\n.crumbs .leafpick{flex:1 1 14rem;min-width:0;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:thin;padding-bottom:.1rem}.crumbs .leafpick button{flex:none;white-space:nowrap}\n")
rep("c+=w*(Math.abs(A.cx-Z.cx)+Math.abs(A.cy-Z.cy))/100;", "c+=w*(Math.abs(A.cx-Z.cx)+Math.abs(A.cy-Z.cy))/100;{const gx=Math.max(A.l-Z.r,Z.l-A.r),gy=Math.max(A.t-Z.b,Z.t-A.b);if((gy>=0&&gx<0&&gy<26)||(gx>=0&&gy<0&&gx<26))c+=8*w}")
open(os.path.join(H, "course_page_template_v9_46_0.html"), "w", encoding="utf-8").write(s)
print("wrote course_page_template_v9_46_0.html", len(s))
