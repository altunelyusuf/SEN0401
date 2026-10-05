#!/usr/bin/env python3
"""SEN0401 page template 9.32.0, from 9.29.0 - one subject: the guide reaches course-level material instead of
denying it exists, and its answer is still written in one go when the "finding the right person" bubble is replaced.

This version supersedes the two intermediate templates of the same session, 9.30.0 and 9.31.0, which are left on
disk as the record of how the repair was arrived at. They are not fit to ship: both put an `await` inside the
expression assigned to the bubble's `innerHTML` while the bubble's `typing` class had already been cleared on the
line before, so for the length of that await the guide's message read "finding the right person" while announcing
itself as finished - measured in the browser against the 9.32.0 page build, where the demonstration script read
exactly that text back. Anything watching for the end of the guide's turn, the page test included, would read an
empty answer. 9.32.0 keeps the repair and computes the whole answer before the bubble is touched.

WHAT THIS REPAIRS, AND WHY

Repair F-B1 of template 9.28.0 restricted every subject agent's retrieval to the passages its own `covers` set
reaches - the owner's standing rule, and the audit's most serious finding. A course learning outcome is a passage of
the course ontology belonging to no concept of the chapter, so after that repair it is in no agent's slice, which is
correct: an agent must not answer from material it does not own. Measured against chapter 1 (page 9.32.0, 21 agents,
the course question of test_config_v1_3_0.json): none of the twenty-one agents' slices reaches the LO-1 passage,
while the page-wide search - `rank` with an empty `covers` set, the unrestricted search the page search box offers
under "Also search the book, course and research passages" - returns it third of eight. The guide, however, offered
the student nothing of that:

  * three agents cleared the guide's own 0.33 relevance bar on book and research passages that merely mention one of
    their concepts (the Standards and openness agent on the book's appendix of improvement proposals), so the
    student was handed agents that cannot reach the outcome and told they "know most about that";
  * had no agent cleared the bar, the guide's only other sentence was "No agent here covers that - it lies outside
    this chapter's book, course and research material", which is false of this case: the course ontology is one of
    the nine files the page embeds and the outcome is in the corpus.

Two changes, in the guide alone:

 1. THE GUIDE SHOWS THE PAGE-WIDE PASSAGE SEARCH BESIDE THE AGENTS IT INTRODUCES. Under a sentence that says why -
    a question about the course itself belongs to no single subject of the chapter, so no agent owns it - the guide
    lists what the unrestricted search over the book, the course, this chapter, this page and the research record
    found for the same words, each passage cited and openable in the detail card, and names the page search (Ctrl+K)
    as the place the same search lives. No agent's ranking changes and no agent is given a passage outside its slice.
 2. WHEN NO AGENT QUALIFIES AT ALL, THE GUIDE ANSWERS FROM THAT SAME SEARCH instead of asserting the material is not
    here, and says nothing was found only when the search really found nothing. The relevance bar is the 0.33 the
    guide already applies to its best agent, applied to the best passage, so no new threshold is stipulated.

The change is in the shared template, so it reaches all five SEN0401 chapter pages: chapters 2 to 5 must be rebuilt
to carry it. SEN0414's own chain carries the identical `route` and the identical gap; that repository is not this
session's to edit, so it is a handover, not a change made here.

usage: template_patch_v9_32_0.py [IN.html OUT.html]"""
__version__ = "9.32.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_29_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_32_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1  the whole answer is computed before the bubble is touched ---------------------------------------------------
rep(" try{const g=(await routeScores(q)).filter(x=>x.best>0).slice(0,3);h.className='msg agent';\n"
    "  h.innerHTML=g.length&&g[0].best>=0.33?'These agents know most about that:'",
    # 9.32.0 - the bubble keeps its "finding the right person" text AND its typing class until the whole answer,
    # page-wide passages included, is ready: both are replaced in the same step, so nothing can read a finished
    # bubble that has not been written yet.
    " try{const g=(await routeScores(q)).filter(x=>x.best>0).slice(0,3);\n"
    "  const body=g.length&&g[0].best>=0.33?'These agents know most about that:'",
    tag="guide bubble written in one step")

rep("'</button></div>').join(''):'No agent here covers that - it lies outside this chapter\\u2019s book, course and "
    "research material.'}",
    "'</button></div>').join('')+await guidePassages(q,false):await guidePassages(q,true);\n"
    "  h.className='msg agent';h.innerHTML=body}",
    tag="guide answer reaches the page-wide passage search")

# ---- 2  the page-wide passage search the guide shows ----------------------------------------------------------------
rep("async function route(){",
    # 9.32.0 - one helper for both cases. alone=true is the case where no agent's slice qualified at all: the guide
    # answers from the page-wide search itself. alone=false is the ordinary case: the agents are introduced first and
    # these passages are offered beside them, because an agent can clear the guide's bar on a book or research
    # passage that merely mentions one of its concepts while the passage the student wants - a course learning
    # outcome, which belongs to no concept and so to no slice - sits just below it.
    "async function guidePassages(q,alone){const {top}=await rank({covers:[]},q,5);const rows=top.filter(x=>x.score>0);\n"
    " const ok=rows.length&&rows[0].score>=0.33;\n"
    " if(!ok)return alone?'No agent here covers that, and a search of every passage of the book, the course, this "
    "chapter and the research record finds nothing about it either.':'';\n"
    " const lead=alone?'No single subject of this chapter owns that, so I will not hand it to an agent whose own "
    "material does not answer it. The course, the book and the research record this page carries do speak to it, "
    "though: these are the passages that match, and you can open any of them here.'\n"
    "  :'Whichever of them you ask, these passages of the book, the course, this chapter and the research record "
    "match your words as well. A question about the course itself - one of its learning outcomes, for instance - "
    "belongs to no single subject of this chapter, so no agent owns it and it is found here rather than with an "
    "agent.';\n"
    " return '<p class=\"note\">'+lead+' Open a passage to read it; the page search (Ctrl+K) runs the same search "
    "over all of them.</p>'+sourcesHtml(rows,'the page-wide passage search: every passage of the book, the course, "
    "this chapter, this page and the research record, ranked by meaning, with no agent\\u2019s slice applied - '"
    "+rows.length+' of '+KIT.chunks.length+' passages shown')}\n"
    "async function route(){",
    tag="guidePassages helper")

# ---- 3  the version markers -----------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.29.0:",
    "<!-- course_page_template version 9.32.0: the guide shows the page-wide passage search over the book, the "
    "course, this chapter and the research record beside the agents it introduces, and answers from it when no "
    "agent's slice qualifies, so a question about the course itself reaches the course material; its bubble is "
    "replaced in one step. Earlier: -->"
    "<!-- course_page_template version 9.29.0:",
    tag="version comment")

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
