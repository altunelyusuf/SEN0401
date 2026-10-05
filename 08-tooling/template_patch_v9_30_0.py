#!/usr/bin/env python3
"""SEN0401 page template 9.30.0, from 9.29.0 - one change: the guide no longer answers a course-level question with a
sentence that is not true, and no longer leaves the student with nowhere to go.

WHAT CHANGES, AND WHY

 1. A QUESTION NO SUBJECT AGENT OWNS IS STILL A QUESTION THIS PAGE HAS MATERIAL FOR. Repair F-B1 of template 9.28.0
    restricted every subject agent's retrieval to the passages its own `covers` set reaches, which is the owner's
    standing rule and the audit's most serious finding. A course learning outcome, however, is a passage of the
    course ontology that belongs to no concept of this chapter, so after that repair it sits in no agent's slice -
    correctly, because handing a passage to an agent that does not own it is the defect that was repaired. The guide
    then fell through to its only other answer, "No agent here covers that - it lies outside this chapter's book,
    course and research material", which is false of exactly this case: the course ontology IS one of the nine files
    the page embeds, the outcome IS in the corpus, and the page-wide passage search finds it at once. A student who
    asked the guide which outcome a chapter serves was told the material does not exist.

    The guide now, when no agent's slice answers, runs the page-wide passage search - `rank` with an empty `covers`
    set, the same unrestricted search the page search box offers under "Also search the book, course and research
    passages" - and shows what it found: the matching passages, cited, each openable in the detail card, with a
    sentence saying why no agent was handed the question and where the same search lives in the page. It says
    nothing was found only when nothing was. The slice restriction is untouched: no agent is given a passage it does
    not own, and the guide still ranks only owners when there is an owner. No new threshold is introduced either -
    the relevance bar is the 0.33 the guide already applies to its best agent, applied to the best passage.

 2. THE VERSION MARKERS. The template, and the pages built from it, say 9.30.0.

The change is in the shared template, so it reaches all five SEN0401 chapter pages; chapters 2 to 5 must be rebuilt
to carry it. The same gap exists in SEN0414's own chain (its 9.24.0 base carries the identical `route`), and is
handed over rather than edited here: that repository is not this session's to change.

usage: template_patch_v9_30_0.py [IN.html OUT.html]"""
__version__ = "9.30.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_29_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_30_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1  the guide reaches course-level material instead of denying it exists ----------------------------------------
rep(":'No agent here covers that - it lies outside this chapter\\u2019s book, course and research material.'}",
    ":await routeUnowned(q)}",
    tag="guide no-owner branch asks the page-wide passage search")

rep("async function route(){",
    # 9.30.0 - a passage that belongs to no concept of this chapter (a course learning outcome, the course profile)
    # is in no agent's slice by design, and must not be handed to an agent that does not own it. Telling the student
    # the material does not exist is equally wrong: it is in the corpus, and the page-wide search reaches it. The
    # guide therefore searches the whole corpus itself, shows the passages it found, and names the search box where
    # the same search lives. The bar is the one the guide already uses for its best agent.
    "async function routeUnowned(q){const {top}=await rank({covers:[]},q,5);const rows=top.filter(x=>x.score>0);\n"
    " if(!(rows.length&&rows[0].score>=0.33))return 'No agent here covers that, and a search of every passage of the "
    "book, the course, this chapter and the research record finds nothing about it either.';\n"
    " return 'No single subject of this chapter owns that, so I will not hand it to an agent whose own material does "
    "not answer it. The course, the book and the research record this page carries do speak to it: these are the "
    "passages that match, and you can open any of them here. The same search is in the page search \\u2014 press "
    "Ctrl+K, type your question and choose \\u201cAlso search the book, course and research passages\\u201d.'"
    "+sourcesHtml(rows,'the page-wide passage search: every passage of the book, the course, this chapter, this page "
    "and the research record, ranked by meaning, with no agent\\u2019s slice applied - '+rows.length+' of '"
    "+KIT.chunks.length+' passages shown')}\n"
    "async function route(){",
    tag="routeUnowned helper")

# ---- 2  the version markers -----------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.29.0:",
    "<!-- course_page_template version 9.30.0: the guide answers a question no subject agent owns from the page-wide "
    "passage search over the book, the course and the research record, instead of saying the material does not "
    "exist. Earlier: -->"
    "<!-- course_page_template version 9.29.0:",
    tag="version comment")

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
