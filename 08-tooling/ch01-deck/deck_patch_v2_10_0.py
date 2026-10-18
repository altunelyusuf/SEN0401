"""Chapter 1 deck 2.10.0: the geometry corrections the fit check asked for (frames that overlap or that the shared renderer drew past their own box)."""
def item(plan, slide, t, nth=0):
    return [it for it in plan["slides"][slide - 1]["items"] if it["t"] == t][nth]
def patch(plan):
    item(plan, 7, "img").update(h=2.55)
    item(plan, 7, "news").update(y=1.35, h=2.4)
    item(plan, 7, "beats").update(y=3.78, h=0.6)
    item(plan, 8, "img").update(h=2.9)
    item(plan, 11, "beats").update(h=1.1)
    item(plan, 11, "ledger").update(y=2.6, h=1.7)
    item(plan, 11, "factrow").update(y=4.55)
    item(plan, 12, "img", 0).update(y=1.5, h=1.1)
    item(plan, 12, "img", 1).update(y=1.5, h=1.1)
    item(plan, 12, "timeline").update(y=3.05, h=1.2)
    item(plan, 12, "factrow").update(y=4.5)
    item(plan, 16, "text").update(h=0.25)
    item(plan, 16, "factrow").update(y=4.6)
    item(plan, 18, "numlist").update(w=3.1)
    item(plan, 18, "dsolve").update(x=3.7, w=5.8)
    item(plan, 21, "numlist").update(t="beats", h=0.9)       # three long lines in 0.9 in: diamonds, not numbered circles that would stand on one another
    item(plan, 23, "stat").update(h=1.4)
    item(plan, 23, "img").update(y=3.05, h=1.45)
    item(plan, 29, "img").update(h=1.4)
    # slides whose picture and program share the page: the picture is drawn smaller so that the program, whose lines are the point of the slide, has the room it needs
    item(plan, 11, "beats").update(h=1.2, y=1.45)
    item(plan, 27, "numlist").update(h=1.5)
    item(plan, 27, "img").update(h=1.3)
    item(plan, 27, "stat").update(h=1.4)
    item(plan, 35, "numlist").update(t="beats", y=1.5, h=1.55)
    item(plan, 35, "funnel").update(y=1.5, h=1.5)
    item(plan, 35, "prog").update(x=0.5, y=3.4, w=9.0, fs=7.4)
    item(plan, 36, "flow").update(y=1.4, h=0.8)
    item(plan, 36, "bars").update(y=2.3, h=1.32)
    item(plan, 36, "numlist").update(t="beats", y=2.3, h=1.3)
    item(plan, 36, "prog").update(x=0.5, y=3.95, w=9.0, fs=7.4)
    for s_ in (40, 43):
        item(plan, s_, "numlist").update(t="beats", y=1.45, h=1.2)
        item(plan, s_, {40: "chainviz", 43: "route"}[s_]).update(y=1.4, h=1.35)
        item(plan, s_, "prog").update(y=3.05, fs=7.0)
    # programs: the result inside the box (compact), the box as tall as its lines need (the fit check's own measure of a line), the caption on the label's row when both fit on the box's width
    for i, s in enumerate(plan["slides"], 1):
        for it in s["items"]:
            if it["t"] == "prog":
                it["compact"] = True
                capw = min(it["w"] * 0.62, max(1.8, len(it.get("cap", "")) * 0.062 + 0.15))
                top = bool(it.get("cap") and it.get("label") and len(it["cap"]) * 0.062 + 0.15 <= it["w"] * 0.62 and len(it["label"]) * 0.085 + capw + 0.1 <= it["w"])
                it["h"] = round(0.26 + (0 if top else 0.22) + (len(it["lines"]) + (1 if it.get("out") not in (None, "") else 0)) * it.get("fs", 8) * 0.0192 + 0.03, 2)
                print("  prog on slide %d: y %.2f h %.2f ends %.2f caption %s" % (i, it["y"], it["h"], it["y"] + it["h"], "on the label row" if top else "inside"))


NOTES = {
 1: "This deck follows the chapter's own concept taxonomy: ninety concepts in six branches, of which forty-two carry a worked example. The worked examples are re-run by the build under the interpreter named in each console caption, and the deck is refused if one stops agreeing. Figures that come from outside that run say Recorded or NOT EXECUTED on their own slide. The text is Mastering Bitcoin, third edition, chapter 1 (Antonopoulos and Harding, 2023), free under CC BY-SA 4.0.",
 6: "Three stories explain why Bitcoin looks the way it does: a newspaper headline carved into the first block, the first purchase made with bitcoin, and forty years of failed attempts at digital money. Each story is dated and sourced on its own slide.",
 9: "Bitcoin was not the first attempt at digital money. David Chaum's blind-signature ecash of the 1980s ended with the bankruptcy of his company DigiCash, and Adam Back's Hashcash of 1997 priced email spam with proof of work. Wei Dai's b-money and Nick Szabo's bit gold, both of 1998, were never built because neither could agree on a history without a leader. The sources are Nakamoto's 2008 paper and the original text of each author.",
 11: "On the island of Yap, wealth was held in rai, limestone discs up to four metres wide and far too heavy to move. When a stone changed owners it stayed where it lay, and only the community's shared memory of who owned it changed. That is a ledger without a bank, the idea Bitcoin rebuilds. The sources are Furness, The Island of Stone Money (1910), and Milton Friedman's Hoover working paper of 1991 with the same title.",
 12: "Money has changed form many times: grain-ledger entries in Mesopotamia, the first struck coins in Lydia around 600 BCE, paper notes in Song-dynasty China, and goldsmiths' receipts that became bank money. In 1971 the dollar's last tie to gold was cut, leaving pure fiat money. Bitcoin is the next step in that sequence, money that exists only as digital records. The sources are standard monetary histories and chapter 1 of Mastering Bitcoin, third edition.",
 13: "The table compares traditional cash, digital money held at banks and cryptocurrency on who issues it, where it exists and who keeps the ledger. The remaining rows ask what sets the supply and how a payment settles. Read down a column to see one kind of money, and across a row to see which property changes. The difference in who keeps the ledger is the subject of this course.",
 27: "One peer starts out knowing two neighbours, and in each round it asks the peers it has just found for their neighbours. The program counts the rounds of gossip until all seven peers are known, and it reports four. No server or registry is involved, which is why the network needs no directory.",
 34: "The exchange Mt Gox of Tokyo, led by Mark Karpeles, was once the largest bitcoin exchange in the world. In February 2014 it halted withdrawals, filed for bankruptcy and admitted that about 850,000 bitcoins were gone. Customers had balances on a website, but the keys, and therefore the coins, had been in someone else's hands all along. The figure comes from the Tokyo District Court filing of 28 February 2014 and is reported here, not recomputed.",
 46: "These are the claims you should now be able to make: what a bitcoin is and how far it divides, why twenty-one million is arithmetic and not a promise, and what replaces the bank in the middle. Each claim is proved in a later chapter, and the last box on the slide names the chapter that opens each branch we drew. If you cannot yet say one of them in your own words, return to its branch.",
}
SUBS = {7: "Recorded: 3 January 2009", 24: "Recorded: documented milestones; the last point fetched for this deck",
        34: "NOT EXECUTED: Tokyo, February 2014 - figures from the court filing, not recomputed"}
HONESTY = {"recorded": [7, 24], "notExecuted": [34]}

def patch2(plan):
    for i, t in NOTES.items(): plan["slides"][i - 1]["notes"] = t
    for i, t in SUBS.items(): plan["slides"][i - 1]["sub"] = t
    plan["meta"]["honesty"] = HONESTY
    plan["meta"]["version"] = "2.10.0"
    s = plan["slides"][26]
    s["items"][0]["items"] = ["One peer starts, knowing two neighbours", "Each round it asks the peers just found for THEIR neighbours", "Rounds are counted until all seven peers are known: 4"]
    s["items"][2]["items"][0]["label"] = "rounds of gossip until every peer is known - no server, no registry"
    for it in plan["slides"][6]["items"]:
        if it["t"] == "img": it["cap"] = "Recorded: block 0's real 285 bytes, fetched from the live chain for this deck; its hash re-verified in the build"
_p1 = patch
def patch(plan):
    _p1(plan); patch2(plan); patch3(plan)

def patch3(plan):
    item(plan, 11, "beats").update(fs=12)
    item(plan, 28, "prog").update(h=1.22)
