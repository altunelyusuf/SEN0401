"""Chapter 2 deck 2.2.0: the geometry corrections the fit check asked for (frames that overlap or that the shared renderer drew past their own box)."""
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
def patch(plan):
    item(plan, 8, "numlist").update(h=1.65)
    item(plan, 9, "bars").update(w=5.0, h=1.4)
    item(plan, 9, "img").update(h=1.2)
    for s in (17, 19):
        item(plan, s, "numlist").update(h=1.75)
        item(plan, s, "funnel").update(h=1.6)
    item(plan, 18, "img").update(h=3.0)
    item(plan, 18, "numlist").update(h=1.55)
    item(plan, 18, "chips").update(y=3.15, h=0.7, fs=10)
    item(plan, 18, "code").update(y=4.2, h=0.8, label="80 bytes carry a 4 MB body: 1 to 50,000")


NOTES = {
 3: "Each question on this slide is one the chapter answers, from the parts of a transaction to what a confirmation buys. We return to every one of them as the chapter proceeds. If you can answer them at the end, the chapter is yours.",
 6: "On 31 October 2008 a pseudonymous author posted nine pages to a cryptography mailing list. Section 11 does something unusual for a systems paper, because it computes the attacker's odds. For an attacker with ten percent of the power, the paper's table gives about 0.2046 at one confirmation and 0.0002428 at six, and the example group AttackerSuccess reruns both. The sources are Nakamoto's 2008 paper and the announcement on the metzdowd cryptography list.",
}
SUBS = {12: "Recorded: 2010-06-11, from the bitcointalk announcement", 21: "Recorded: 2010-08-15, from the bitcointalk reports"}
HONESTY = {"recorded": [12, 21], "notExecuted": []}
def patch2(plan):
    for i, t in NOTES.items(): plan["slides"][i - 1]["notes"] = t
    for i, t in SUBS.items(): plan["slides"][i - 1]["sub"] = t
    plan["meta"]["honesty"] = HONESTY
    plan["meta"]["version"] = "2.2.0"
_p1 = patch
def patch(plan):
    _p1(plan); patch2(plan); patch3(plan)

def patch3(plan):
    item(plan, 10, "stat").update(y=3.9, h=1.15)
