#!/usr/bin/env python3
"""SEN0401 page template 9.31.0, from 9.30.0 - one change: the guide always offers the page-wide passage search
beside the agents it introduces, so a course-level question reaches the course material from the guide itself.

WHY THIS IS NEEDED ON TOP OF 9.30.0. Template 9.30.0 gave the guide a truthful answer for a question no agent's
slice can answer. Measured in the browser against the 9.31.0 page, the course question of chapter 1's test
configuration - "which course learning outcome is about explaining what Bitcoin is and the problems it was designed
to solve?" - never reaches that branch: three agents score above the guide's own 0.33 bar, because an agent owns a
book or research passage whose label merely contains one of its concept words (the Standards and openness agent
matched the book's appendix on improvement proposals). The guide therefore introduced three agents, none of which
can reach the learning outcome - the same measurement shows that none of the twenty-one agents' slices contains the
LO-1 passage, which is correct and is what the 9.28.0 slice repair is for. The student was handed a confident
answer about the wrong material.

WHAT CHANGES. The guide's answer now carries both halves: the agents it ranked, and, under a sentence that says
why, what the unrestricted page-wide passage search over the book, the course, this chapter, this page and the
research record found for the same words - each passage cited and openable in the detail card, with the page search
(Ctrl+K) named as the place the same search lives. Nothing about the ranking of agents changes, no agent is given a
passage outside its own slice, and the 9.30.0 answer for the case where no agent qualifies at all is untouched.

The change is in the shared template, so it reaches all five SEN0401 chapter pages; chapters 2 to 5 must be rebuilt
to carry it. SEN0414's own chain carries the identical `route` and is handed over rather than edited here.

usage: template_patch_v9_31_0.py [IN.html OUT.html]"""
__version__ = "9.31.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_30_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_31_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1  the guide offers the page-wide passage search beside the agents it introduces -------------------------------
rep(">Ask '+esc(x.a.name)+'</button></div>').join(''):await routeUnowned(q)}",
    ">Ask '+esc(x.a.name)+'</button></div>').join('')+await routeAlso(q):await routeUnowned(q)}",
    tag="guide appends the page-wide passage search")

rep("async function routeUnowned(q){",
    # 9.31.0 - an agent can rank above the guide's bar on a book or research passage that merely mentions one of its
    # own concepts, while the passage the student wants - a course learning outcome, which belongs to no concept of
    # the chapter and so to no agent's slice - sits just below it. The guide therefore shows the unrestricted
    # page-wide search as well, every time, so course-level material is one click from the guide instead of
    # unreachable through it.
    "async function routeAlso(q){const {top}=await rank({covers:[]},q,5);const rows=top.filter(x=>x.score>0);\n"
    " if(!rows.length)return '';\n"
    " return '<p class=\"note\">Whichever of them you ask, these passages of the book, the course, this chapter and "
    "the research record match your words as well. A question about the course itself - one of its learning "
    "outcomes, for instance - belongs to no single subject of this chapter, so no agent owns it and it is found "
    "here rather than with an agent. Open any passage to read it; the page search (Ctrl+K) runs the same search.</p>'"
    "+sourcesHtml(rows,'the page-wide passage search: every passage of the book, the course, this chapter, this page "
    "and the research record, ranked by meaning, with no agent\\u2019s slice applied - '+rows.length+' of '"
    "+KIT.chunks.length+' passages shown')}\n"
    "async function routeUnowned(q){",
    tag="routeAlso helper")

# ---- 2  the version markers -----------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.30.0:",
    "<!-- course_page_template version 9.31.0: the guide shows the page-wide passage search over the book, the "
    "course and the research record beside the agents it introduces, so a question about the course itself reaches "
    "the course material from the guide. Earlier: -->"
    "<!-- course_page_template version 9.30.0:",
    tag="version comment")

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
