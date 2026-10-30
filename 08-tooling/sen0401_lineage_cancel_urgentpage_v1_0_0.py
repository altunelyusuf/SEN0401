#!/usr/bin/env python3
"""sen0401_lineage_cancel_urgentpage v1_0_0 - closes ST_Urgent_Ch06_Page with TK_Urgent_Ch06_Page_Build (Suspended on the control, NOT MET on element 5b) and TK_Urgent_Ch06_Page_Verify (Proposed) as CANCELLED, so that the urgent interruption can be resolved (the owner of 2026-10-30 07:45 Istanbul: return to the exams). Superseded by ST_Repair_Ch06_Lecture (a new page after v9.89.0 whose criterion carries the page-test copies and the report of the committed tests as printed). The owner's rule on cancelling is applied: an as-is fit-gap and impact analysis and a closure report with status CANCELLED. Nothing is waived: the criterion AC9_Urgent_Ch06_Page is not edited and stays recorded as not met on element (5b).
Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
ITEMS = ("TK_Urgent_Ch06_Page_Verify", "TK_Urgent_Ch06_Page_Build", "ST_Urgent_Ch06_Page")
FROM = {}
for tk in ITEMS:
    i, j = T.blk(t, tk); m = re.search(r"backlog:hasState backlog:(Proposed|Suspended|InProgress)\b", t[i:j]); assert m, tk; FROM[tk] = m.group(1)
FITGAP = ("AS-IS FIT-GAP AND IMPACT ANALYSIS of ex:ST_Urgent_Ch06_Page (read from the register v%s; criterion AC9_Urgent_Ch06_Page; own control of 2026-10-30, record v0.696.0). "
          "ACCOMPLISHED (met, run by the evidence bridge): the page v9.89.0 and the template 9.52.9 exist as new files; no committed file is edited (net, 149 files added); full screen and a reader-set size work in every panel kind (panel test 182 PASS, 0 FAIL, 0 CANNOT_RUN); the Playground lists the 18 slide examples first; 0 slide code lines are found nowhere in the page (108 manifest lines on the deck and in the page); the page test copies 9.38.0 (398 features), 9.34.3 (374) and 9.35.3 (374) pass with 121 of 121 widgets. "
          "FAILED (printed, not weakened): element (5b): the COMMITTED page tests 9.34.2 and 9.37.0 named by the criterion crash with StopIteration on the new page (27 features before the crash, no widgets line), because they pick the first Playground example by position and the Playground now starts with the slide examples; the test files are committed and are not edited. Also found: the Lecture tab of the page lists the 62 slides of the old deck, not the 71 of the delivered deck. "
          "IN PROGRESS: nothing; the Build task is Suspended since the control and its Verify task was never started. "
          "DUE: the Lecture tab and the owner's ruling on the page test copies are carried by ex:ST_Repair_Ch06_Lecture (a new page after v9.89.0; its criterion lists the copies 9.34.3, 9.35.3 and 9.38.0 as the tests that must pass and the committed 9.34.2, 9.35.2 and 9.37.0 reported as printed). "
          "IMPACT of the cancellation: the page v9.89.0 and all commits stay as they are and the page remains the page to use; the criterion AC9_Urgent_Ch06_Page is not edited and not waived, it stays as the criterion this unit did not fully meet; the urgent interruption can be resolved and the exam work resumed.")
L.append('\nex:IA3_UrgentPageCancel a backlog:ImpactAssessment ;\n    rdfs:label "As-is fit-gap and impact of cancelling the urgent chapter 6 page story"@en ;\n    backlog:analyzesRequest ex:CR3_PanelView ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n' % lit(FITGAP % cur))
L.append('\nex:ClosureRep3_UrgentPage a backlog:ClosureReport ;\n    rdfs:label "Closure report of the urgent chapter 6 page story: CANCELLED (carried by the repair story)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:reportGeneratedAt "%s"^^xsd:dateTime ; rdfs:seeAlso ex:ST_Urgent_Ch06_Page, ex:IA3_UrgentPageCancel, ex:ST_Repair_Ch06_Lecture ;\n    backlog:hasClosureSummary %s .\n' % (now, lit("Status CANCELLED, not Done. The page v9.89.0 was delivered and is the page to use, but the criterion was not met on element (5b): the committed page tests named by it crash on the new page. Nothing was waived and no test was edited. The remaining work (Lecture tab on the 71-slide deck, the owner's ruling on the test copies) is the story ST_Repair_Ch06_Lecture. See ex:IA3_UrgentPageCancel.")))
for tk in ITEMS:
    i, j = T.blk(t, tk); b = t[i:j]; frm = FROM[tk]
    why = "Cancelled %s UTC (v%s): the urgent interruption is over (owner 2026-10-30 07:45 Istanbul: back to the exams); the unit's criterion was not met on element (5b) and is carried by ex:ST_Repair_Ch06_Lecture (see ex:IA3_UrgentPageCancel and ex:ClosureRep3_UrgentPage, status CANCELLED). Criteria not edited, not waived." % (now, nxt)
    nb = b.replace("backlog:hasState backlog:" + frm, "backlog:hasState backlog:Cancelled", 1)
    nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', lambda _: "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("CxUP_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " cancelled"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Urgent_Ch06_Page and its tasks cancelled (the committed page tests named by the criterion crash on the new page; the remainder is carried by ST_Repair_Ch06_Lecture) with an as-is fit-gap and impact analysis and a closure report marked CANCELLED, so that the urgent interruption can be resolved")))
