#!/usr/bin/env python3
"""Patches course_page_template_v9_38_0.html into course_page_template_v9_39_0.html.

One subject, the owner's review of 2026-10-07 10:10: "There are meta information about the work itself not the
subject, like those where, who, etc. My request is to use them as guidance not visualize them and their usages.
They are not necessary, even reduce the readability and takes unnecessary spaces."

What 9.34.0 had put at the top of every concept was a strip of chips - WHERE the concept sits in the chapter, WHO
(which agent) explains it, RUN (its executed example), LINKS (how many relations it has). Those are facts about
the page's own machinery, not about the subject; the breadcrumb already says where, the agent list already says
who, the run panel already shows the example. The strip is removed; the information stays available where it
belonged (breadcrumb, agents, the detail card). The worked-example card of 9.34.0 goes the same way: it repeated the
page's own EXAMPLE panel directly beneath it, and a list shown twice on one screen is the owner's standing no. The stories' WHO/WHERE/WHEN/READ rows are not touched: those are
the subject's own facts (who did what, where and when), which the owner's 5N1K rule requires on the material.
"""
__version__ = "9.39.0"

SRC, DST = "course_page_template_v9_38_0.html", "course_page_template_v9_39_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

rep("function richInner(n,tag){return secHead(n,tag)+cfacts(n)+bodyRich(n)+excard(n)+storychips(n)+", "function richInner(n,tag){return secHead(n,tag)+bodyRich(n)+storychips(n)+", 1)
# the worked-example card repeated the page's own EXAMPLE panel below it (the static example widget of 9.7.0); one copy stays
i = t.find(" function excard(n){"); j = t.find("'</div>':''}", i) + len("'</div>':''}")
assert i > 0 and j > i and t.count(" function excard(n){") == 1
t = t[:i] + t[j:]
rep(".excard{background:var(--band);border-left:4px solid var(--blue);border-radius:0 8px 8px 0;padding:.45rem .7rem;margin:.5rem 0}.excard b{color:#235A50}\n", "", 1)
# the function and its style rule leave with the strip
i = t.find(" function cfacts(n){"); j = t.find("'</div>'}", i) + len("'</div>'}")
assert i > 0 and j > i and t.count(" function cfacts(n){") == 1
t = t[:i] + t[j:]
rep(".cfacts{margin:.3rem 0 .5rem}\n", "", 1)
rep("<!-- course_page_template version 9.38.0:",
    "<!-- course_page_template version 9.39.0: the WHERE/WHO/RUN/LINKS strip leaves the concept sections - facts about "
    "the page's machinery, not the subject, already carried by the breadcrumb, the agent list and the run panel. "
    "Earlier: --><!-- course_page_template version 9.38.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
