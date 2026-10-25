#!/usr/bin/env python3
"""sen0401_lineage_rank v1_5_0 - new dated RICE+DepFactor PriorityScore records (BP-D10, ruling G147: a repair re-ranks the open items) for the stories admitted by ex:CR3_Retro24 (Iterations 24 to 28).
A NEW tool file over v1_4_0 (which stays unchanged): v1_4_0 ranked the items of Iteration 21 to 23; the stories ranked here are the restated retrofit stories, the template 9.52.3 and the chapter 1 verify script.
Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (0.5 is a stipulation).
The ordering key is the score times the DepFactor; ties break in the owner's chapter order (1, 2, 3, 4, 9 to 14). Usage: sen0401_lineage_rank_v1_5_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.5.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
TAG = "41"
FACTS = ("FACTS: the lineage agent's baseline of 2026-10-25 (08-tooling/verify/iter24/baseline and storylayout): chapters 5 to 8 pass the deck standard but their pages fail the owner's story-layout rule (cause: the template 9.52.2 has no height cap on story photographs); "
         "chapters 1 to 4 and 9 to 14 fail eight elements of the deck standard each and have no manifest and no chapter-code tab; the owner's order is chapter 1 first, urgent chapters before the retrofit; every page waits for the template 9.52.3.")
ORDER = ["01", "02", "03", "04", "09", "10", "11", "12", "13", "14"]
ITEMS = [("ST_Template_9523", "Template 9.52.3: every story's text on the first screen", 14, 3, 0.8, 2.5, 1,
          "Reach 14 pages: every rebuilt page takes the template. Impact 3 (massive): the owner's story rule is broken on the four urgent pages and the template is the cause, and every page of Iterations 25 to 28 waits for it. Confidence 0.8. Effort 2.5 h: 1.5 h executor plus 1.0 h verification. DepFactor 1: no open prerequisite.")]
ITEMS.append(("ST_Ch01_VerifyScript", "Chapter 1 research verify script", 1, 1, 0.8, 1.5, 1,
              "Reach 1 chapter. Impact 1 (medium): the Research chapter check crashes for chapter 1, which blocks the page of chapter 1. Confidence 0.8. Effort 1.5 h: 1.0 h executor plus 0.5 h verification. DepFactor 1: no open prerequisite."))
for nn in ["05", "06", "07", "08"]:
    ITEMS.append(("ST_Ch%s_Page_R24" % nn, "Story-layout repair: page of chapter %d on template 9.52.3" % int(nn), 1, 3, 0.8, 2.5, 0.5,
                  "Reach 1 page. Impact 3 (massive): urgent chapter used in class and its stories fail the owner's layout rule. Confidence 0.8. Effort 2.5 h: 1.5 h executor plus 1.0 h verification. DepFactor 0.5: the template 9.52.3 is not Done."))
for nn in ORDER:
    imp = 2 if nn in ("01", "02", "03", "04") else 1
    why = "the owner's order: return to all chapters starting with chapter 1" if imp == 2 else "retrofit after chapters 1 to 4"
    ITEMS.append(("ST_Ch%s_Deck_R24" % nn, "Retrofit: deck and manifest of chapter %d" % int(nn), 1, imp, 0.8, 2.0, 1,
                  "Reach 1 chapter. Impact %s: %s. Confidence 0.8. Effort 2.0 h: 1.5 h executor plus 0.5 h verification. DepFactor 1: no open prerequisite for the build." % ("2 (high)" if imp == 2 else "1 (medium)", why)))
    ITEMS.append(("ST_Ch%s_Page_R24" % nn, "Retrofit: page of chapter %d on template 9.52.3" % int(nn), 1, imp, 0.8, 2.5, 0.5,
                  "Reach 1 page. Impact %s: %s. Confidence 0.8. Effort 2.5 h: 1.5 h executor plus 1.0 h verification. DepFactor 0.5: its deck and the template 9.52.3 are not Done." % ("2 (high)" if imp == 2 else "1 (medium)", why)))
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
L.append("ex:Iter_24 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the records ex:Rank%s_*): %s. The scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
print(os.path.basename(M.write_new(src, t2, nxt, cur, "New dated RICE+DepFactor PriorityScore records for the stories admitted by ex:CR3_Retro24 (G147: a repair re-ranks the open items); no earlier record edited; ranking: " + order)))
for r in rows: print("%.2f  %s" % (r[0], r[3]))
