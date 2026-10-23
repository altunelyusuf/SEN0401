#!/usr/bin/env python3
"""sen0401_lineage_rank v1_0_0 - applies the owner's instruction of Friday 2026-10-23 11:07 Istanbul ("Repairs should change the priority of the PBIs or the tasks") with the register's own ranking discipline, BP-D10 (RICE with a dependency factor, ex backlog:Method_RICE_DepFactor): total = Reach x Impact x Confidence / Effort (the stored score value, as the register's shape requires), and the ordering key is that score times the DepFactor.
Every open story that still has work to do gets a NEW dated PriorityScore (RICEScore) record with its inputs and the facts behind each input; no earlier record is edited. The ranking orders the executors' start. Scales (the method's): Impact 3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal; Confidence 1 / 0.8 / 0.5; Effort in hours (the tasks' estimates in the register); DepFactor 1 when every prerequisite is Done, 0.5 when one is not (the method names a multiplier below one, the value 0.5 is a stipulation).
Usage: sen0401_lineage_rank_v1_0_0.py   (writes one new register version and prints the ranking)"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_template_revision_v1_0_0 as T
lit = C.lit
FACTS = ("FACTS: the owner's archive holds 14 chapter pages built on the one template line, each with the charset tag behind byte 1024 (the coordinator's measure); the builder session measured the tag at byte 13578 in the pages 9.82.0 of chapters 5 and 6; the owner reported garbled labels on pages he uses in class (2026-10-23 09:32 Istanbul).")
# story, label, R, I, C, E, Dep, basis
ITEMS = [
 ("ST_Charset_Template", "Template 9.52.2: the character set declared first", 14, 2, 0.9, 1.0, 1, "Reach 14 pages: every later build and all 14 archived chapters take the template line. Impact 2 (high): it removes the cause of the garbled labels the owner reported. Confidence 0.9: the cause is measured on file bytes. Effort 1.0 h: executor 0.5 h plus builder verification 0.5 h (task estimates). DepFactor 1: no prerequisite."),
 ("ST_Charset_Check", "Charset check: measures the declaration on any page", 14, 1, 0.9, 1.0, 1, "Reach 14 pages: it measures every archived page. Impact 1 (medium): it measures, it does not fix. Confidence 0.9: the rule is stated in bytes. Effort 1.0 h: 0.5 h executor plus 0.5 h verification. DepFactor 1: no prerequisite."),
 ("ST_Charset_Page_Ch05", "Page of chapter 5 rebuilt on template 9.52.2", 1, 2, 0.8, 2.5, 0.5, "Reach 1 page. Impact 2 (high): the owner uses this page in class and sees garbled labels. Confidence 0.8: depends on the template and the check being right. Effort 2.5 h: 1.5 h executor plus 1.0 h verification. DepFactor 0.5: its prerequisites (template and check, with their verification) are not Done."),
 ("ST_Charset_Page_Ch06", "Page of chapter 6 rebuilt on template 9.52.2", 1, 2, 0.8, 2.5, 0.5, "Reach 1 page. Impact 2 (high): the owner uses this page in class and sees garbled labels. Confidence 0.8. Effort 2.5 h: 1.5 h executor plus 1.0 h verification. DepFactor 0.5: its prerequisites are not Done."),
 ("ST_Repair_Page_Ch05", "Chapter 5 page 9.82.0 task: the remainder is a log file written twice", 1, 0.5, 0.8, 1.5, 1, "Reach 1 page. Impact 0.5 (low): the page passes all three page tests; the one failing element is formal (an appended log file). Confidence 0.8: measured by the control of v0.216.0. Effort 1.5 h: redo the log commit 0.5 h plus control 1.0 h. DepFactor 1: no open prerequisite. It ships the same charset defect as the page it would deliver, so the owner's rule puts the charset repair above it."),
 ("ST_Remedy_Page_Ch05", "Chapter 5 page 9.80.0 story of Iteration 17 (superseded)", 1, 0.25, 0.8, 1.0, 1, "Reach 1 page. Impact 0.25 (minimal): its tasks are withdrawn and the rebuild tasks carry the work. Confidence 0.8. Effort 1.0 h (control). DepFactor 1. The open question of the owner on this story is unchanged."),
 ("ST_Remedy_Tools", "Regression run of the three tools of Iteration 17", 3, 0.5, 0.8, 1.0, 1, "Reach 3 tools (deck check, page test, template). Impact 0.5 (low): no defect seen in them. Confidence 0.8. Effort 1.0 h (builder, the task TK_Remedy_Regress). DepFactor 1: its tools are Done. Builder work: no executor waits for it."),
]
TAG = os.environ.get("RANK_TAG", "31"); SKIP = [x for x in os.environ.get("RANK_SKIP", "").split(",") if x]; AMEND = os.environ.get("RANK_AMEND") == "1"; WHY = os.environ.get("RANK_WHY", "")
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; rows = []
for sid, lab, R, I, Cf, E, D, basis in [x for x in ITEMS if x[0] not in SKIP]:
    if os.environ.get("RANK_PAGES_READY") == "1" and sid.startswith("ST_Charset_Page_"): D = 1; basis = basis.replace("DepFactor 0.5: its prerequisites (template and check, with their verification) are not Done.", "DepFactor 1: its prerequisites (template and check, with their verification) are Done.").replace("DepFactor 0.5: its prerequisites are not Done.", "DepFactor 1: its prerequisites (template and check, with their verification) are Done."); assert "DepFactor 1: its" in basis
    assert ("ex:%s a backlog:Story" % sid) in t, sid
    v = round(R * I * Cf / E, 2); key = round(v * D, 2); rows.append((key, sid, lab, R, I, Cf, E, D, v))
    i, j = T.blk(t, sid); b = t[i:j]; b2 = b if TAG != "31" else re.sub(r'\n?\s*backlog:notYetScoreable true ; backlog:hasScoreabilityReason "(?:[^"\\]|\\.)*" ;', '', b, count=1); assert TAG != "31" or b2 != b, sid
    t = t[:i] + b2 + t[j:]
    L.append('ex:Rank%s_%s a backlog:RICEScore ; rdfs:label %s@en ; backlog:scoredByMethod backlog:Method_RICE_DepFactor ;\n    backlog:hasReach "%s"^^xsd:decimal ; backlog:hasImpact "%s"^^xsd:decimal ; backlog:hasConfidence "%s"^^xsd:decimal ; backlog:hasEffort "%s"^^xsd:decimal ; backlog:hasDepFactor "%s"^^xsd:decimal ;\n    backlog:hasScoreValue "%.2f"^^xsd:decimal ; backlog:scoredAt "%s"^^xsd:dateTime ; backlog:isAveragedFromMembers false ;\n    backlog:hasScoreRationale %s .\n' % (
        TAG, sid, lit("Ranking of " + lab + ", " + now[:10]), R, I, Cf, E, D, v, now, lit("RICE with dependency factor (BP-D10): score = Reach x Impact x Confidence / Effort = %s x %s x %s / %s = %.2f; the dependency factor %s is recorded beside it and the ORDERING KEY is the score times the dependency factor = %.2f. %s %s Recorded on the owner's instruction 'Repairs should change the priority of the PBIs or the tasks'; a new dated record, no earlier score is edited." % (R, I, Cf, E, v, D, key, basis, FACTS) + (" " + WHY if WHY else ""))))
    if TAG != "31":
        t, k = re.subn(r"^ex:%s backlog:hasPriorityScore ex:Rank\d+_%s \.\n" % (sid, sid), "", t, flags=re.M); assert k >= 1, "no earlier score link for " + sid   # the item points to the live score only (rule L1); the earlier score record stays in the register, unedited
    L.append("ex:%s backlog:hasPriorityScore ex:Rank%s_%s .\n" % (sid, TAG, sid))
rows.sort(reverse=True)
order = "; ".join("%d. %s (ordering key %.2f)" % (k + 1, r[2], r[0]) for k, r in enumerate(rows))
L.append("ex:Iter_19 rdfs:comment %s@en .\n" % lit("Ranking of %s (BP-D10, RICE with dependency factor; the scores are the records ex:Rank%s_*): %s. The executors start in this order: the two repair tools first (they block the page rebuilds and the repair outranks the remaining Iteration 18 items and any new page build), then the page rebuilds when their prerequisites are Done. The inputs are stated in each record; the scale values (impact levels, the dependency factor 0.5) are stipulations of the method's scale and are disclosed as such." % (now, TAG, order)))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); out = "Re-ranked (BP-D11) after a completion: " + order if AMEND else "New dated RICE+DepFactor PriorityScore records for the open stories on the owner's instruction that repairs change priorities; no earlier record edited; ranking: " + order
if AMEND:
    open(src, "w", encoding="utf-8").write(t2); print(os.path.basename(src), "amended")
else: print(os.path.basename(M.write_new(src, t2, nxt, cur, out)))
for r in rows: print("%.2f  %s" % (r[0], r[2]))
