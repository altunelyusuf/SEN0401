#!/usr/bin/env python3
"""SEN0401 page template 9.29.0, from 9.28.0 - the four shared-template defects the page test of the 9.29.0 pages
found after the 9.28.0 repairs. Every change below is in the template, so it reaches all five SEN0401 chapter pages;
the same three changes that are not SEN0401-specific are applied to SEN0414's own chain by
advancedprogrammingwithpython/08-tooling/template_patch_v9_25_0.py, whose base (9.24.0) carries the identical code.

WHAT CHANGES, AND WHY

 1. THE RESOURCES PANE SHOWS EVERY RESOURCE, NOT ONLY THE PYTHON ONES. The pane grouped its links by kind and took
    the kinds from RKIND, a table that names only the five kinds the Python course uses - documentation, PEPs,
    interactive tools, videos and discussions. A link of any other kind was dropped silently: of chapter 1's twenty
    checked links the pane rendered the two 'documentation' ones and discarded eighteen (nine standards, five
    reference works, three papers and one data source), and the other four chapters lost between nine and fourteen
    each. The kind table now names every kind the two courses really use, each with its own heading, and a kind that
    is in the data but not in the table is still shown, under a heading built from the kind's own word, so no checked
    resource can ever be hidden by a missing table entry again. Nothing about the links themselves changes: each one
    still opens in a new tab with rel="noopener", and the pane still states the date they were opened and says
    plainly that the searches below are searches and not recommendations.
 2. THE TAXONOMY IS EXPLAINED IN ONE PARAGRAPH, NOT TWO NOTES. Repair 15 of 9.28.0 (the page explains its own
    vocabulary) added a one-sentence note saying what a taxonomy is, and put it above the paragraph that already
    explained the view - so the pane opened with two separate explanations of the same diagram, the first of them a
    single sentence. That is the shape the owner's own rule rejects: explanations are comprehensive, cohesive
    paragraphs, and a screen does not carry the same thing twice. The sentence is now the opening of the one
    narrative paragraph, which keeps the link to "Words we use" and keeps everything it already said about the root,
    the dashed book links, the layer boxes and Show all.
 3. A QUESTION'S STEM IS THE STEM ITS OWN BANK ITEM CARRIES. Repair 14 of 9.28.0 qualified a stem that several items
    share ("What does this program print?", which 42 of chapter 1's 161 items use) with the concept it asks about,
    but it did so only on the way out of qMake: the bank in memory still held the bare stem, so the page showed a
    question whose stem matched no item of its own bank. The page test says exactly that, by asking an item's concept
    for a bank question and requiring the result to match one of that concept's items on stem, correct answer and
    options; it failed for every concept whose draw landed on its code item. The qualification is now applied to the
    bank itself, once, as it is loaded, so the browser of questions, the generated question, the mock exam and the
    bank all read the same stem. bankStem stays and is unchanged in effect: asked again for an already-qualified
    stem it returns it untouched, so nothing is qualified twice. The bank file on disk is still not touched.
 4. THE VERSION MARKERS. The template, and the pages built from it, say 9.29.0.

usage: template_patch_v9_29_0.py [IN.html OUT.html]"""
__version__ = "9.29.0"
import os, sys

here = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_28_0.html")
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(here, "course_page_template_v9_29_0.html")
h = open(src, encoding="utf-8").read()
APPLIED = []


def rep(a, b, n=1, tag=""):
    global h
    assert h.count(a) == n, ("anchor not found %dx: %r (found %d)" % (n, a[:90], h.count(a)))
    h = h.replace(a, b)
    APPLIED.append(tag or a[:40])


# ---- 1  the resources pane shows every resource ---------------------------------------------------------------------
rep("RKIND={documentation:'\U0001F4D8 Documentation',pep:'\U0001F4DC PEPs',interactive:'\U0001F9EA Interactive tools',"
    "video:'\U0001F3A5 Videos',discussion:'\U0001F4AC Discussions'}",
    # 9.29.0 - every kind of resource the two courses really use has its own heading here, in the order the headings
    # are shown; a kind the data carries and this table does not is still rendered, under a heading made from its own
    # word, so a missing entry can hide nothing.
    "RKIND={documentation:'\U0001F4D8 Documentation',pep:'\U0001F4DC PEPs',"
    "standard:'\U0001F4D0 Standards and specifications',paper:'\U0001F4C4 Papers',"
    "reference:'\U0001F4DA Reference works',wiki:'\U0001F310 Community wikis',"
    "data:'\U0001F5C4 Data sources',tool:'\U0001F9F0 Tools',library:'\U0001F4E6 Libraries',"
    "interactive:'\U0001F9EA Interactive tools',video:'\U0001F3A5 Videos',discussion:'\U0001F4AC Discussions'}",
    tag="resources RKIND")

rep("const kinds=Object.keys(RKIND).filter(k=>D.resources.some(r=>r.kind===k));",
    "const RKLAB=k=>RKIND[k]||('\U0001F517 '+String(k).charAt(0).toUpperCase()+String(k).slice(1));\n"
    " const kinds=[...Object.keys(RKIND).filter(k=>D.resources.some(r=>r.kind===k)),"
    "...[...new Set(D.resources.map(r=>r.kind))].filter(k=>!RKIND[k])];",
    tag="resources kinds")

rep("kinds.map(k=>'<h3>'+RKIND[k]+'</h3>'+resList(D.resources.filter(r=>r.kind===k))).join('')",
    "kinds.map(k=>'<h3>'+RKLAB(k)+'</h3>'+resList(D.resources.filter(r=>r.kind===k))).join('')",
    tag="resources headings")

# ---- 2  the taxonomy is explained in one paragraph ------------------------------------------------------------------
rep("<h2>\U0001F333 Chapter taxonomy</h2><p class=\"note\">A taxonomy is the \\u201cis a kind of\\u201d part of the "
    "chapter\\u2019s ontology, drawn as one tree. '+WORDLINK+'</p><p class=\"legend\">",
    "<h2>\U0001F333 Chapter taxonomy</h2><p class=\"legend\">",
    tag="taxonomy duplicate note removed")

rep("<p class=\"note\">The chapter\\'s taxonomy as one tree, with its leaves. The root is the chapter;",
    "<p class=\"note\">A taxonomy is the \\u201cis a kind of\\u201d part of the chapter\\u2019s ontology, drawn here as "
    "one tree: the chapter\\'s taxonomy with its leaves. The root is the chapter;",
    tag="taxonomy narrative opening")

rep("A worked example is named by what it shows; its code is in the card on the right.</p>",
    "A worked example is named by what it shows; its code is in the card on the right. '+WORDLINK+'</p>",
    tag="taxonomy narrative words link")

# ---- 3  a question's stem is the stem its own bank item carries ------------------------------------------------------
rep("function bankStem(b){if((BSTEM[b.q]||0)<2)return b.q;const n=byId[b.concept];const k=b.q+'\\u0000'+b.concept;\n"
    " return b.q+(n?' \\u2014 '+n.label:'')+(BSEQ[k]>1?' ('+b._seq+')':'')}",
    "function bankStem(b){if((BSTEM[b.q]||0)<2)return b.q;const n=byId[b.concept];const k=b.q+'\\u0000'+b.concept;\n"
    " return b.q+(n?' \\u2014 '+n.label:'')+(BSEQ[k]>1?' ('+b._seq+')':'')}\n"
    "// 9.29.0 - the qualified stem is written into the bank itself, once, so every place that reads an item - the\n"
    "// browser of questions, a generated question, the mock exam - shows the stem the item carries. bankStem is\n"
    "// keyed on the stem it was given, so asked again for an already-qualified stem it returns it unchanged.\n"
    "BANK.forEach(b=>{b.q=bankStem(b)});",
    tag="bank stem written into the bank")

# ---- 4  the version markers -----------------------------------------------------------------------------------------
rep("<!-- course_page_template version 9.28.0:",
    "<!-- course_page_template version 9.29.0: the Resources pane shows every kind of checked resource, not only the "
    "five the Python course uses; the taxonomy is explained in one paragraph instead of a sentence above a paragraph; "
    "a question's stem is written into the bank itself, so the page and its own bank read alike. Earlier: -->"
    "<!-- course_page_template version 9.28.0:",
    tag="version comment")

open(out, "w", encoding="utf-8").write(h)
print("written", out, os.path.getsize(out), "bytes")
for t in APPLIED:
    print("   applied:", t)
