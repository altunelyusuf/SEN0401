#!/usr/bin/env python3
"""lecture_make v1_1_1 (SEN0401 chapter 11 page). Writes lecture_v1_1_1.json from the deck agent's lecture_v1_1_0.json (committed, untouched) and the committed deck plan: each slide gets "labels", the honesty
labels the deck itself carries, so that the page's Lecture tab reproduces them. The slide numbers come from the deck's review record 08-tooling/ch11-deck/REVIEW_v1_0_0.md (Honesty): Recorded 1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 19, 22, 23 (found in the deck plan by the tool); NOT EXECUTED 19, 20, 21, 22, 23; stand-in pictures 8, 21, 23. The text of a NOT EXECUTED and of a stand-in label is the sentence printed on the slide (found in the deck plan; the tool refuses when it is not there)."""
__version__ = "1.1.1"
# The deck agent's lecture_v1_1_0.json carries in "concept" the slide's one-line takeaway (text). The page's Lecture tab wants in "concept" the id of the page concept the slide is about (a button
# "On the page: ..." jumps there), so this version keeps the text as "takeaway" and puts the concept id in "concept", from the table below (the page author's linking of each slide to the concept its
# own content is about; every id is checked against the chapter's page data).
LINK = {1: "BlockStructure", 2: "BlockStructure", 3: "BlockStructure", 4: "BlockStructure", 5: "BlockContainer", 6: "HeaderIs80Bytes", 7: "MedianTimePast", 8: "GenesisCoinbaseMessage",
        9: "BlockHashIsDoubleSha256", 10: "HeightAndMaturity", 11: "TamperingBreaksDescendants", 12: "TwoChildrenOneParent", 13: "MerkleTrees", 14: "FourLeafTree", 15: "MerklePathOf16",
        16: "TreeFlaws", 17: "HashTreeHistory", 18: "TestBlockchains", 19: "SeveralChainsExist", 20: "Testnet4Replaces", 21: "TestnetBlockStorms", 22: "SignetChallengeIsMultisig",
        23: "SignetGenesisShared", 24: "BlockStructure", 25: "TestBlockchains", 26: "BlockStructure"}
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "..", "ch11-deck")
lec = json.load(open(os.path.join(H, "lecture_v1_1_0.json"))); plan = json.load(open(os.path.join(D, "deck_plan_v1_0_0.json")))["slides"]
rev = open(os.path.join(D, "REVIEW_v1_0_0.md"), encoding="utf-8").read()
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
def _find(marker):
    out = []
    for i in range(1, len(plan) + 1):
        if any(marker in t for t in texts(i)): out.append(i)
    return out
REC = _find("Recorded"); NOTEX = _find("NOT EXECUTED:"); STAND = _find("Stand-in picture:")
assert NOTEX == [19, 20, 21, 22, 23] and STAND == [8, 21, 23], (NOTEX, STAND)
assert REC == [1, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 19, 22, 23], REC
_ids = {n["id"] for n in json.load(open(sorted(__import__("glob").glob(os.path.join(H, "page_data_v*.json")))[-1]))["nodes"]}
for s in lec["slides"]:
    i = s["n"]; labs = []
    assert LINK[i] in _ids, LINK[i]
    s["takeaway"] = s["concept"]; s["concept"] = LINK[i]
    if i in REC: labs.append({"kind": "Recorded", "text": "The answers on this slide were read back from the recorded run of Bitcoin Core 31.1 on a regtest chain and from saved files (chainparams.cpp, block data); no node was started again, and this page does not start one: its examples measure the recorded data again."})
    if i in NOTEX: labs.append({"kind": "NOT EXECUTED", "text": re.sub(r"^NOT EXECUTED:\s*", "", sentence(i, "NOT EXECUTED:"))})
    if i in STAND: labs.append({"kind": "Stand-in picture", "text": re.sub(r"^Stand-in picture:\s*", "", sentence(i, "Stand-in picture:"))})
    if labs: s["labels"] = labs
lec["_note"] = "lecture_v1_1_0.json plus the deck's honesty labels per slide (labels), made by lecture_make_v1_1_1.py from the deck plan and the deck's review record; the slide text is unchanged; concept now holds the id of the page concept the slide is about (the deck's one-line takeaway is kept as takeaway)."
json.dump(lec, open(os.path.join(H, "lecture_v1_1_1.json"), "w"), indent=1, ensure_ascii=False)
print("labels: Recorded %s, NOT EXECUTED %s, stand-in %s" % (REC, NOTEX, STAND))
