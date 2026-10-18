"""Chapter 4 deck 3.2.0: the geometry corrections the fit check asked for (frames that overlap or that the shared renderer drew past their own box)."""
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
def patch(plan):
    item(plan, 1, "img").update(h=3.0)
    item(plan, 10, "numlist").update(t="beats", h=0.8)       # three long lines in 0.8 in: diamonds, not numbered circles that would stand on one another
    item(plan, 10, "code").update(h=1.35)
    item(plan, 10, "chips").update(y=4.05, h=0.75)
    item(plan, 12, "code").update(label="why keys start with 5 or K")
    item(plan, 14, "code").update(label="a real typo, a real refusal")
    item(plan, 16, "code").update(label="both hashes, compressed key")
    item(plan, 18, "numlist").update(h=1.65)
    item(plan, 18, "code").update(h=1.6)
    item(plan, 19, "numlist").update(t="beats", h=0.8)
    item(plan, 19, "code", 0).update(h=1.4)
    item(plan, 19, "code", 1).update(y=4.28, h=0.75)


NOTES = {
 3: "These are the questions the chapter answers, from how a private key becomes a public key to where its printed statements differ from the standards and from a run of Bitcoin Core 31.1. Each is taken up in turn on the slides that follow. If you can answer them, chapter 4 is yours.",
 18: "Segregated witness, or segwit, is an upgrade that moves signatures and scripts into a separate structure called the witness, committed to blocks apart from the tree of transactions (Lombrozo et al., 2015). The witness holds the data needed to check that a transaction is valid, but not the data that decides what the transaction does. Bech32 gives these outputs an alphabet without look-alike characters, so reading an address aloud no longer invites the old mistakes. The full explanation is on the course page, chapter 4, in Segwit upgrade and Bech32Address.",
 24: "Everything here is free. Open the eater address tonight and watch nothing move, because that standstill is this chapter's whole lesson about commitments. Ask yourself who could explain to a parent why bc1p addresses beat old 1-addresses for reading aloud. The full explanation is on the course page, chapter 4, in Practice.",
}
SUBS = {17: "Recorded: since 2011; balance fetched 2026-10-06"}
HONESTY = {"recorded": [17], "notExecuted": []}
def patch2(plan):
    for i, t in NOTES.items(): plan["slides"][i - 1]["notes"] = t
    for i, t in SUBS.items(): plan["slides"][i - 1]["sub"] = t
    plan["meta"]["honesty"] = HONESTY
    plan["meta"]["version"] = "3.2.0"
_p1 = patch
def patch(plan):
    _p1(plan); patch2(plan)
