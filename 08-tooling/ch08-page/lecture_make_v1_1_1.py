#!/usr/bin/env python3
"""lecture_make v1_1_1 (SEN0401 chapter 8 page). Writes lecture_v1_1_1.json from the deck agent's lecture_v1_1_0.json (committed, untouched) and the committed deck plan: each slide gets "labels", the honesty
labels the deck itself carries, so that the page's Lecture tab reproduces them. The slide numbers come from the deck's review record 08-tooling/ch08-deck/REVIEW_v1_0_0.md (Honesty): Recorded 1, 7, 8, 18, 22;
NOT EXECUTED 12 and 23; stand-in pictures 17 and 19. The text of a NOT EXECUTED and of a stand-in label is the sentence printed on the slide (found in the deck plan; the tool refuses when it is not there)."""
__version__ = "1.1.1"
# The deck agent's lecture_v1_1_0.json carries in "concept" the slide's one-line takeaway (text). The page's Lecture tab wants in "concept" the id of the page concept the slide is about (a button
# "On the page: ..." jumps there), so this version keeps the text as "takeaway" and puts the concept id in "concept", from the table below (the page author's linking of each slide to the concept its
# own content is about; every id is checked against the chapter's page data).
LINK = {1: "SignatureFoundations", 2: "SignatureFoundations", 3: "SignatureFoundations", 4: "SignatureRoles", 5: "VerifierInputs", 6: "ScalarModulus", 7: "Commitments", 8: "SingleBug",
        9: "SchnorrSignatures", 10: "IdentityProtocol", 11: "PatentDates", 12: "Bip340Format", 13: "KeyCancellation", 14: "ThresholdSharing", 15: "EcdsaSignatures", 16: "EcdsaMath",
        17: "BookSampleOnChain", 18: "DeterministicNonces", 19: "NonceReuse", 20: "SegwitSigning", 21: "ValueCommitment", 22: "ConsensusAndPolicy", 23: "SinceTheBook",
        24: "SignatureFoundations", 25: "SourcesRecord", 26: "SignatureFoundations"}
import json, os, re
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "..", "ch08-deck")
lec = json.load(open(os.path.join(H, "lecture_v1_1_0.json"))); plan = json.load(open(os.path.join(D, "deck_plan_v1_0_0.json")))["slides"]
rev = open(os.path.join(D, "REVIEW_v1_0_0.md"), encoding="utf-8").read()
def nums(pat):
    m = re.search(pat, rev); return [int(x) for x in re.findall(r"\d+", " ".join(m.groups()))]
REC = nums(r"Recorded \(read from[^)]*\): slides ([\d, ]+)\."); NOTEX = nums(r"NOT EXECUTED, labelled on the slide: slide (\d+) .*?slide (\d+) "); STAND = nums(r"Stand-in pictures, labelled on the slide: (\d+) \(.*?\), (\d+) \(")
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
    if i in REC: labs.append({"kind": "Recorded", "text": "The answers of Bitcoin Core 31.1.0 on this slide were produced by one run of the program on a test network and are read back here; they were not run again, and they are not run on this page."})
    if i in NOTEX: labs.append({"kind": "NOT EXECUTED", "text": re.sub(r"^NOT EXECUTED:\s*", "", sentence(i, "NOT EXECUTED:"))})
    if i in STAND: labs.append({"kind": "Stand-in picture", "text": re.sub(r"^Stand-in picture:\s*", "", sentence(i, "Stand-in picture:"))})
    if labs: s["labels"] = labs
lec["_note"] = "lecture_v1_1_0.json plus the deck's honesty labels per slide (labels), made by lecture_make_v1_1_1.py from the deck plan and the deck's review record; the slide text is unchanged; concept now holds the id of the page concept the slide is about (the deck's one-line takeaway is kept as takeaway)."
json.dump(lec, open(os.path.join(H, "lecture_v1_1_1.json"), "w"), indent=1, ensure_ascii=False)
print("labels: Recorded %s, NOT EXECUTED %s, stand-in %s" % (REC, NOTEX, STAND))
