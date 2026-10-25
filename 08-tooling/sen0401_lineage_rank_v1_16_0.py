#!/usr/bin/env python3
"""sen0401_lineage_rank v1_16_0 - new dated RICE+DepFactor PriorityScore records (BP-D10, ruling G147: a repair re-ranks the open items) for the story admitted by ex:CR3_StoryLink2 (Iteration 37).
A NEW tool file over v1_4_0 (which stays unchanged): v1_4_0 ranked the items of Iteration 21 to 23; the stories ranked here are the restated retrofit stories, the template 9.52.3 and the chapter 1 verify script.
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.16.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "59"
FACTS = ("FACTS: ex:CR3_StoryLink2: the first chapter 14 story was withdrawn because the arc check v1_3_0 refuses the notes of slides 22, 40 and 42 of the delivered deck; the story check refuses the READ-link host of SpillmanChannels.")
ITEMS = [("ST_Deck14_StoryLink2", "Chapter 14 deck accepted by the story check and the arc check", 1, 0.5, 0.8, 3.5, 1, "Reach 1 chapter. Impact 0.5 (low): the deck meets its criterion; one story shows no link host and three notes are over the limit. Confidence 0.8. Effort 3.5 h: 2.5 h executor plus 1.0 h verification. DepFactor 1: no open prerequisite.")]
ORDER = ["01"]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; rows = []
def chapter_rank(sid):
    m = re.search(r"Ch(\d\d)", sid); return ORDER.index(m.group(1)) if m and m.group(1) in ORDER else -1
for sid, lab, R, I, Cf, E, D, basis in ITEMS:
    assert ("ex:%s a backlog:Story" % sid) in t, sid
    v = round(R * I * Cf / E, 2); key = round(v * D, 2); rows.append((key, -chapter_rank(sid), sid, lab))
    i, j = T.blk(t, sid); b = t[i:j]; b2 = re.sub(r'\n?\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "(?:[^"\\]|\\.)*" ;', '', b, count=1); assert b2 != b, sid
    t = t[:i] + b2 + t[j:]
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        TAG, sid, lit("Ranking of " + lab + ", " + now[:10]), R, I, Cf, E, D, v, now, lit("RICE with dependency factor (BP-D10): score = Reach x Impact x Confidence / Effort = %s x %s x %s / %s = %.2f; the dependency factor %s is recorded beside it and the ORDERING KEY is the score times the dependency factor = %.2f (ties break in the owner's chapter order). %s %s A repair re-ranks the open items (G147); a new dated record, no earlier score is edited." % (R, I, Cf, E, v, D, key, basis, FACTS))))
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
rows.sort(reverse=True)
order = "; ".join("%d. %s (ordering key %.2f)" % (k + 1, r[3], r[0]) for k, r in enumerate(rows))
L.append("ex:Iter_37 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the records ex:Rank%s_*): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "New dated RICE+DepFactor PriorityScore records for the story admitted by ex:CR3_StoryLink2 (G147: a repair re-ranks the open items); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
