#!/usr/bin/env python3
"""lecture_make v1_1_1 (SEN0401 chapter 9 page). Writes lecture_v1_1_1.json from the deck agent's lecture_v1_1_0.json (committed, untouched) and the committed deck plan: each slide gets "labels", the honesty
labels the deck itself carries, so that the page's Lecture tab reproduces them. The slide numbers come from the deck's review record 08-tooling/ch09-deck/REVIEW_v1_0_0.md (Honesty): Recorded 1, 5, 6, 7, 9, 13, 14, 15, 16, 18, 19, 21, 22;
NOT EXECUTED 15, 20, 22, 23; stand-in pictures 11, 14, 20. The text of a NOT EXECUTED and of a stand-in label is the sentence printed on the slide (found in the deck plan; the tool refuses when it is not there)."""
__version__ = "1.1.1"
# The deck agent's lecture_v1_1_0.json carries in "concept" the slide's one-line takeaway (text). The page's Lecture tab wants in "concept" the id of the page concept the slide is about (a button
# "On the page: ..." jumps there), so this version keeps the text as "takeaway" and puts the concept id in "concept", from the table below (the page author's linking of each slide to the concept its
# own content is about; every id is checked against the chapter's page data).
LINK = {1: "WhoPaysTheFee", 2: "WhoPaysTheFee", 3: "WhoPaysTheFee", 4: "FeeAsDifference", 5: "FeeIsInputsMinusOutputs", 6: "WeightAndVirtualSize", 7: "MinRelayFee", 8: "EstimatorMechanics",
        9: "EstimateSmartFeeCall", 10: "BlockFeeCensus", 11: "FeesVsSubsidy", 12: "ReplacementRules", 13: "AbsoluteFeeRule", 14: "FullRbfDefault", 15: "ReplacementCycling", 16: "PackageFeeRate",
        17: "PinningAndAnchors", 18: "LargeChildPin", 19: "PayToAnchor", 20: "CarveOutRemoved", 21: "ClusterLimits", 22: "WalletLockTimeRule", 23: "UndercuttingAttack", 24: "WhoPaysTheFee",
        25: "FeeMarketOnMainnet", 26: "WhoPaysTheFee"}
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "..", "ch09-deck")
lec = json.load(open(os.path.join(H, "lecture_v1_1_0.json"))); plan = json.load(open(os.path.join(D, "deck_plan_v1_0_0.json")))["slides"]
rev = open(os.path.join(D, "REVIEW_v1_0_0.md"), encoding="utf-8").read()
def nums(pat):
    m = re.search(pat, rev); return [int(x) for x in re.findall(r"\d+", m.group(1))]
REC = nums(r"Recorded \(read from[^)]*\): slides ([\d, ]+)\."); NOTEX = nums(r"NOT EXECUTED, labelled on the slide: ([^\n]+)"); NOTEX = [x for x in NOTEX if x in (15, 20, 22, 23)]
STAND = nums(r"Stand-in pictures, labelled on the slide: ([^\n]+?)\. Slide 23")
STAND = [x for x in STAND if x in (11, 14, 20)]
def texts(i):
    out = []
    def walk(x):
        if isinstance(x, dict):
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
        elif isinstance(x, str): out.append(x)
    walk(plan[i - 1]); return out
def sentence(i, start):
    for t in texts(i):
        j = t.find(start)
        if j >= 0:
            e = t.find(". ", j); return t[j:(e + 1 if e > 0 else len(t))].strip()
    raise SystemExit("slide %d carries no text starting %r" % (i, start))
_ids = {n["id"] for n in json.load(open(sorted(__import__("glob").glob(os.path.join(H, "page_data_v*.json")))[-1]))["nodes"]}
for s in lec["slides"]:
    i = s["n"]; labs = []
    assert LINK[i] in _ids, LINK[i]
    s["takeaway"] = s["concept"]; s["concept"] = LINK[i]
    if i in REC: labs.append({"kind": "Recorded", "text": "The answers of Bitcoin Core 31.1 on this slide were produced by two runs of the program on a test network and are read back here; no node was started again, and this page does not start one: its examples measure the recorded data again."})
    if i in NOTEX: labs.append({"kind": "NOT EXECUTED", "text": re.sub(r"^NOT EXECUTED:\s*", "", sentence(i, "NOT EXECUTED:"))})
    if i in STAND: labs.append({"kind": "Stand-in picture", "text": re.sub(r"^Stand-in picture:\s*", "", sentence(i, "Stand-in picture:"))})
    if labs: s["labels"] = labs
lec["_note"] = "lecture_v1_1_0.json plus the deck's honesty labels per slide (labels), made by lecture_make_v1_1_1.py from the deck plan and the deck's review record; the slide text is unchanged; concept now holds the id of the page concept the slide is about (the deck's one-line takeaway is kept as takeaway)."
json.dump(lec, open(os.path.join(H, "lecture_v1_1_1.json"), "w"), indent=1, ensure_ascii=False)
print("labels: Recorded %s, NOT EXECUTED %s, stand-in %s" % (REC, NOTEX, STAND))
