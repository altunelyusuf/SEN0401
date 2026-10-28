#!/usr/bin/env python3
"""sen0401_lineage_rank v1_28_0 - new dated RICE+DepFactor PriorityScore records (BP-D10, ruling G147: a repair re-ranks the open items) for the four stories admitted by the owner's words of 2026-10-29 (Iteration 42) and a re-run for the chapter 14 page story. A NEW tool file over v1_27_0 (unchanged).
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.28.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "72"
FACTS = ("FACTS: the owner's words of 2026-10-29 on ex:CR3_GateArcDark (the deck standard D9 gives way to one dark closing slide; the arc check stays; the chapter 5 deck is the only deck that changes) and on ex:CR3_PageClick (new page tests 9.34.2 and 9.35.2 may change the click; the earlier failure is a test fault; then the chapter 11 page is measured).")
ITEMS = [("ST_DeckStd_Dark", "Deck standard check v1_2_0 and its SHACL shapes", 14, 2, 0.8, 4.0, 1, "Reach 14 chapters (every deck is measured by the standard). Impact 2 (high): the two gates contradict and block the chapter 5 deck. Confidence 0.8. Effort 4.0 h: 3.0 h executor plus 1.0 h verification. DepFactor 1: no open prerequisite."),
         ("ST_PageTest_Click", "Page tests 9.34.2 and 9.35.2: the click after the drag", 14, 1, 0.8, 4.0, 1, "Reach 14 pages (every page is measured by these tests). Impact 1 (medium): the fault shows only where a later entity covers the dragged one. Confidence 0.8. Effort 4.0 h: 3.0 h executor plus 1.0 h verification. DepFactor 1: no open prerequisite."),
         ("ST_Ch05_DeckDark", "Chapter 5 deck v3_4_0 with the dark closing slide", 1, 2, 0.8, 4.0, 0.5, "Reach 1 chapter. Impact 2 (high): the delivered deck is refused by the arc check. Confidence 0.8. Effort 4.0 h: 3.0 h executor plus 1.0 h verification. DepFactor 0.5: its Build task waits for the Verify task of ST_DeckStd_Dark, which is not Done (0.5 is a stipulation of the method's scale)."),
         ("ST_Ch11_PageMeasure", "Chapter 11 page measured with the new page tests", 1, 2, 0.8, 4.0, 0.5, "Reach 1 chapter. Impact 2 (high): the page was never measured with 9.34.x and 9.35.x on its own. Confidence 0.8. Effort 4.0 h: 3.0 h executor plus 1.0 h verification. DepFactor 0.5: its Build task waits for the Verify task of ST_PageTest_Click, which is not Done (0.5 is a stipulation).")]
ORDER = ["05", "11"]
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; rows = []
def chapter_rank(sid):
    m = re.search(r"Ch(\d\d)", sid); return ORDER.index(m.group(1)) if m and m.group(1) in ORDER else -1
for sid, lab, R, I, Cf, E, D, basis in ITEMS:
    assert ("ex:%s a backlog:Story" % sid) in t, sid
    v = round(R * I * Cf / E, 2); key = round(v * D, 2); rows.append((key, -chapter_rank(sid), sid, lab))
    i, j = T.blk(t, sid); b = t[i:j]; b2 = re.sub(r'\n?\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "(?:[^"\\]|\\.)*" ;', '', b, count=1); assert b2 != b, sid
    t = t[:i] + b2 + t[j:]
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        TAG, sid, lit("Ranking of " + lab + ", " + now[:10]), R, I, Cf, E, D, v, now, lit("RICE with dependency factor (BP-D10): score = Reach x Impact x Confidence / Effort = %s x %s x %s / %s = %.2f; the dependency factor %s is recorded beside it and the ORDERING KEY is the score times the dependency factor = %.2f (ties break in chapter order of the list ORDER). %s %s A repair re-ranks the open items (G147); a new dated record, no earlier score is edited." % (R, I, Cf, E, v, D, key, basis, FACTS))))
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
L.append("ex:Iter_44 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the newest records of each open story, ex:Rank%s_* for this one; ties break in chapter order, which these keys do not apply across kinds): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "New dated RICE+DepFactor PriorityScore records for the four stories admitted by the owner's words of 2026-10-29 (G147: a repair re-ranks the open items); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
