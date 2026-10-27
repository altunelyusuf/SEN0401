#!/usr/bin/env python3
"""sen0401_lineage_rank v1_20_0 - new dated RICE+DepFactor PriorityScore records (BP-D10, ruling G147: a repair re-ranks the open items) for the two stories admitted by ex:CR3_Ch13Ex12 (Iteration 40) and a re-run for the chapter 14 page story. A NEW tool file over v1_19_0 (unchanged).
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.20.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "63"
FACTS = ("FACTS: ex:CR3_Ch13Ex12: the page test 9.37.0 fails the chapter 13 page 9.81.0 on example 12, whose expected output carries the prefix Error: (executor commits 5c4806a, 36d86b7; the control reproduced 390 passed, 2 failed); the repair is a new deck v2_2_0 and manifest v1_1_0 and then a page rebuild 9.82.0; the chapter 14 page is not affected.")
ITEMS = [("ST_Deck13_Ex12", "Chapter 13 deck v2_2_0 and manifest v1_1_0: example 12 without the prefix Error:", 1, 2, 0.8, 3.0, 1, "Reach 1 chapter. Impact 2 (high): the failing page of chapter 13 cannot be rebuilt without it. Confidence 0.8. Effort 3.0 h: 2.0 h executor plus 1.0 h verification. DepFactor 1: no open prerequisite."),
         ("ST_Ch13_PageRebuild", "Chapter 13 page rebuilt on the deck v2_2_0", 1, 2, 0.8, 4.0, 0.5, "Reach 1 chapter. Impact 2 (high): the delivered page 9.81.0 fails the page test 9.37.0. Confidence 0.8. Effort 4.0 h: 3.0 h executor plus 1.0 h verification. DepFactor 0.5: its Build task waits for the Verify task of ST_Deck13_Ex12, which is not Done (0.5 is a stipulation).")]
ORDER = ["13"]
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
for sid in ("ST_Ch14_Page_R24",):
    recs = re.findall(r"^ex:Rank(\d+)_%s a " % sid, t, re.M); tag0 = max(int(x) for x in recs)
    blk = re.search(r"^ex:Rank%d_%s a .*?(?=^ex:\w+ a |\Z)" % (tag0, sid), t, re.S | re.M).group(0)
    g = lambda k: re.search(r'backlog:has%s "([\d.]+)"' % k, blk).group(1)
    R_, I_, C_, E_ = g("Reach"), g("Impact"), g("Confidence"), g("Effort"); v = round(float(R_) * float(I_) * float(C_) / float(E_), 2); D_ = 1
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (TAG, sid, lit("Re-ranking of " + sid + ", " + now[:10]), R_, I_, C_, E_, D_, v, now, lit("Re-ranked because of the repair ex:CR3_Ch13Ex12 (G147): Reach, Impact, Confidence and Effort are those of the live record Rank%d_%s (unchanged, no new judgement); the page does not depend on the new stories (the defect is in chapter 13 only), so the dependency factor stays 1. Score = %s x %s x %s / %s = %.2f; ordering key = %.2f. %s" % (tag0, sid, R_, I_, C_, E_, v, round(v * D_, 2), FACTS))))
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
rows.sort(reverse=True)
allrows = []
for m in re.finditer(r"^ex:(ST_\w+) a backlog:Story.*?(?=^ex:\w+ a )", t, re.S | re.M):
    sid = m.group(1); st = re.search(r"hasState backlog:(\w+)", m.group(0))
    if not st or st.group(1) not in ("Proposed", "Ready", "InProgress"): continue
    recs = re.findall(r"^ex:%s backlog:hasPriorityScore ex:Rank(\d+)_" % re.escape(sid), t + "".join(L), re.M)
    if not recs: continue
    tag = max(int(x) for x in recs); blk = re.search(r"^ex:Rank%d_%s a .*?(?=^ex:\w+ a |\Z)" % (tag, re.escape(sid)), t + "".join(L), re.S | re.M)
    if not blk: continue
    sv = re.search(r'hasScoreValue "([\d.]+)"', blk.group(0)); df = re.search(r'hasDepFactor "([\d.]+)"', blk.group(0))
    if sv and df: allrows.append((round(float(sv.group(1)) * float(df.group(1)), 2), sid))
allrows.sort(key=lambda x: (-x[0], x[1]))
order = "; ".join("%d. %s (%.2f)" % (k + 1, r[1], r[0]) for k, r in enumerate(allrows))
L.append("ex:Iter_40 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the newest records of each open story, ex:Rank%s_* for this one; ties break in chapter order, which these keys do not apply across kinds): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "New dated RICE+DepFactor PriorityScore records for the story admitted by ex:CR3_Ch13Ex12 (G147: a repair re-ranks the open items); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
