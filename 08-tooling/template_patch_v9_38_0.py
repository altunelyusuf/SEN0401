#!/usr/bin/env python3
"""Patches course_page_template_v9_37_0.html into course_page_template_v9_38_0.html.

One subject, the owner's review of 2026-10-07 10:10, two sentences of it: "We have page fitting problem for the
content. Some of the text and visualizations are outside of the direct display and needing move up and down,
left and right." and "We need to optimize the top level spaces and menus."

Measured first, on the 9.38.0 chapter 1 page at 1366x768 (and 1280x720, 1536x864): the header is 113 px (title,
a 90-character sub-line about the interpreter and Pyodide, the menu row), the sub-tab row 39 px and the
breadcrumb row 58 px, so the first concept of a section begins 329 px down - 43 percent of the screen is chrome.
The Learn sections sit in a two-column card grid (513 px wide at 1366 px), so code panels and maps scroll sideways
inside their column. Every .diagram is 68vh tall with a 24rem floor, on top of a 270 px offset: 103 percent of the
viewport, so the map, the ontology views and the ERD always need scrolling to see their lower edge.

9.38.0: the header keeps the title on one line and the menu, and the sub-line moves to the Start pane (it is about
the page, not the chapter); the sub-tab and breadcrumb rows lose their margins; the Learn sections take the full
width (one concept per row, never a half column); every diagram is sized to the room below it
(calc(100vh - offset)) so its lower edge is on screen, with the resize handle kept for anyone who wants more.
"""
__version__ = "9.38.0"

SRC, DST = "course_page_template_v9_37_0.html", "course_page_template_v9_38_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

# header: one-line title, no sub-line, tighter menu
rep("header.top{background:var(--navy);color:#fff;padding:.5rem 1rem;flex:none}", "header.top{background:var(--navy);color:#fff;padding:.3rem 1rem;flex:none}", 1)
rep("header.top h1{margin:0;font:600 1.1rem Cambria,Georgia,serif}", "header.top h1{margin:0;font:600 1rem Cambria,Georgia,serif;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}", 1)
rep("header.top .sub{font-size:.8rem;color:#D8CFC2}", "header.top .sub{display:none}", 1)
rep("nav.groups{display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.35rem}", "nav.groups{display:flex;flex-wrap:wrap;gap:.3rem;margin-top:.2rem}", 1)
# the sub-line's content goes where it belongs: the Start pane
rep("Explore with the tree on the left, the subject tabs above, the concept map, the playground, and a <b>subject agent</b> for every part of the chapter.</p>",
    "Explore with the tree on the left, the subject tabs above, the concept map, the playground, and a <b>subject agent</b> for every part of the chapter.</p><p class=\"note\">Every computed result on this page was produced by __PY__; code you edit runs in a background thread with CPython (Pyodide).</p>", 1)
# the rows between the menu and the content
rep(".subtabs{display:flex;flex-wrap:wrap;gap:.3rem;margin:.6rem 0}", ".subtabs{display:flex;flex-wrap:wrap;gap:.3rem;margin:.3rem 0}", 1)
rep(".viewsub{position:static;margin:.2rem 0 .4rem}", ".viewsub{position:static;margin:.15rem 0 .2rem}", 1)
rep(".leafpick{display:flex;flex-wrap:wrap;gap:.3rem;margin:.35rem 0 .5rem}", ".leafpick{display:flex;flex-wrap:wrap;gap:.3rem;margin:.2rem 0 .3rem}", 1)
# Learn: one concept per row, full width
rep(".cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(20rem,1fr));gap:.7rem}", ".cards{display:grid;grid-template-columns:1fr;gap:.7rem}", 1)
# diagrams: sized to the room below them
rep(".diagram{position:relative;height:68vh;min-height:24rem;", ".diagram{position:relative;height:calc(100vh - 15rem);min-height:16rem;", 1)
rep("#graph .diagram{height:34rem;min-height:14rem;", "#graph .diagram{height:calc(100vh - 17rem);min-height:14rem;", 1)
rep(".onto{border:1px solid var(--line);border-radius:12px;min-height:30rem;background:var(--bg)}", ".onto{border:1px solid var(--line);border-radius:12px;min-height:16rem;background:var(--bg)}", 1)

rep("<!-- course_page_template version 9.37.0:",
    "<!-- course_page_template version 9.38.0: the page fits the screen - a one-line header with the sub-line moved to "
    "Start, tighter tab and breadcrumb rows, Learn sections at full width (one concept per row), and every diagram sized "
    "to the room below it so its lower edge is on screen. Earlier: --><!-- course_page_template version 9.37.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
