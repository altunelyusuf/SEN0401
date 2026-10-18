"""Chapter 3 deck 2.2.0: the geometry corrections the fit check asked for (frames that overlap or that the shared renderer drew past their own box)."""
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
def patch(plan):
    item(plan, 5, "img").update(h=2.6)
    item(plan, 11, "flow").update(h=1.0)
    item(plan, 11, "code").update(h=0.62)
    item(plan, 13, "numlist").update(h=1.65)
    item(plan, 15, "code").update(h=0.95)
    item(plan, 15, "stat").update(y=3.9, h=1.1)
    item(plan, 17, "numlist").update(t="beats", h=1.0)      # three long lines: diamonds, not numbered circles that would stand on one another
    item(plan, 17, "code").update(y=2.78, h=0.58)
    item(plan, 17, "prog").update(y=3.72, h=1.28)
    item(plan, 19, "code").update(w=3.5, label="six fields, summed")
    item(plan, 19, "prog").update(y=3.1, h=1.85)
    item(plan, 20, "prog").update(y=2.85, h=1.25)


NOTES = {
 3: "These questions are the chapter's own: which programs Bitcoin Core consists of, which files decide how a node runs, and how a download is checked before it is trusted. Each one is answered on a later slide, and the chapter closes by returning to them. If you can answer them, chapter 3 is yours.",
}
SUBS = {9: "NOT EXECUTED: the git commands are shown, not run", 11: "NOT EXECUTED: the build commands are shown, not run",
        13: "Recorded: a real 31.1 startup, captured for this chapter", 15: "Recorded: one protocol under every interface, answers captured from a node",
        17: "Recorded: the node explains Alice's payment back to us", 19: "Recorded: block 123,456's root, recomputed from its saved transactions"}
HONESTY = {"recorded": [13, 15, 17, 19], "notExecuted": [9, 11]}
def patch2(plan):
    for i, t in NOTES.items(): plan["slides"][i - 1]["notes"] = t
    for i, t in SUBS.items(): plan["slides"][i - 1]["sub"] = t
    plan["meta"]["honesty"] = HONESTY
    plan["meta"]["version"] = "2.2.0"
_p1 = patch
def patch(plan):
    _p1(plan); patch2(plan)
