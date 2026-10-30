#!/usr/bin/env python3
"""sen0401_lineage_cancel_answermethods v1_0_0 - closes ST_Exam_AnswerMethods with TK_Exam_AnswerMethods_Build (Suspended) and TK_Exam_AnswerMethods_Verify (Proposed) as CANCELLED, superseded by ST_Exam_AnswerMethods_Repair (Done on the control, register v0.662.0). The owner's rule on cancelling is applied: an as-is fit-gap and impact analysis (accomplished, failed, in progress, due; an ImpactAssessment) and a closure report marked CANCELLED are recorded in the SAME version as the cancellation. The criterion is not edited and not waived. The Build tasks of the Papers and the Grading stories (not started) named the cancelled Build task as a prerequisite; the repair Build task, which they also name, carries it, so the dependency on the cancelled task is removed from them. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
ITEMS = ("TK_Exam_AnswerMethods_Verify", "TK_Exam_AnswerMethods_Build", "ST_Exam_AnswerMethods")
for tk in ITEMS:
    i, j = T.blk(t, tk); assert re.search(r"backlog:hasState backlog:(Proposed|Suspended)\b", t[i:j]), tk
FITGAP = ("AS-IS FIT-GAP AND IMPACT ANALYSIS of ex:ST_Exam_AnswerMethods (read from the register v%s; criterion AC3E_Exam_AnswerMethods; controls of 2026-10-29 and 2026-10-30). "
          "ACCOMPLISHED (met, measured): the answer sheet and the methods that reduce mistakes in giving answers exist as new files (commit 6e37b8e: one place per answer, a check digit, correction rules, a reader v1.0.0, a measurement on synthetic filled sheets); the owner decided the bubble grid answer sheet; the sheet is counted in the page count. "
          "FAILED (measured by the unit's own check C6 and by the control, register v0.647.0): the reader v1.0.0 did not detect one written box on the synthetic sheets, so the criterion of this unit was NOT MET; it was not waived. "
          "IN PROGRESS: nothing; the Build task is Suspended since the control and its Verify task was never started. "
          "DUE: nothing on this unit: what it was to deliver (a reader that gives no silent wrong reading) is carried by ex:ST_Exam_AnswerMethods_Repair (reader v1.1.0 with optical-density reading, no unflagged empty read of a faint mark, no silent wrong written box), Done on the control of the lineage agent on its own unnamed random blocks of 200 sheets (register v0.662.0, commit 4557301). "
          "IMPACT of the cancellation: the files and their commits stay unchanged; the criterion AC3E_Exam_AnswerMethods is not edited and not waived: it stays as the criterion this unit did not meet, and its measures are repeated by the criterion of the repair story. The Papers and Grading Build tasks (not started) lose the dependency on the cancelled Build task and keep the dependency on the repair Build task, which is Done. Nothing else changes.") 
L.append('\nex:IA3_AnswerMethodsCancel a backlog:ImpactAssessment ;\n    rdfs:label "As-is fit-gap and impact of cancelling the answering-methods story"@en ;\n    backlog:analyzesRequest ex:CR3_AnswerRepair ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n' % lit(FITGAP % cur))
L.append('\nex:ClosureRep3_AnswerMethods a backlog:ClosureReport ;\n    rdfs:label "Closure report of the answering-methods story: CANCELLED (superseded)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:reportGeneratedAt "%s"^^xsd:dateTime ; rdfs:seeAlso ex:ST_Exam_AnswerMethods, ex:IA3_AnswerMethodsCancel, ex:ST_Exam_AnswerMethods_Repair ;\n    backlog:hasClosureSummary %s .\n' % (now, lit("CLOSURE STATUS: CANCELLED (not Done, not forgotten). The story ex:ST_Exam_AnswerMethods with its tasks TK_Exam_AnswerMethods_Build (was Suspended) and TK_Exam_AnswerMethods_Verify (was Proposed) is cancelled on " + now + " UTC because its deliverable was superseded by ex:ST_Exam_AnswerMethods_Repair (controlled Done). The unit itself did not meet its criterion (check C6: one written box not detected); that is kept as the record and is not waived. Lessons: a reader must be measured on its hardest kind of mark (a faint or written box) before the paper is built on it, and a repair that supersedes a unit is recorded with a closure at the time, not later.")))
for tk in ITEMS:
    i, j = T.blk(t, tk); b = t[i:j]; m = re.search(r"backlog:hasState backlog:(Proposed|Suspended)\b", b); frm = m.group(1)
    why = "Cancelled %s UTC (v%s): superseded by ex:ST_Exam_AnswerMethods_Repair (Done on the control); the unit's own criterion was not met (check C6, see ex:IA3_AnswerMethodsCancel and ex:ClosureRep3_AnswerMethods, status CANCELLED). Criteria not edited, not waived." % (now, nxt)
    nb = b.replace(m.group(0), "backlog:hasState backlog:Cancelled", 1)
    nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', lambda _: "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("CxAM_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " cancelled"))
for tk in ("TK_Exam_Papers_Build", "TK_Exam_Grading_Build"):
    i, j = T.blk(t, tk); b = t[i:j]; assert "startedAt" not in b
    m = re.search(r"backlog:dependsOn ([^;]*?)( ;|\s*\.)", b); deps = [d.strip() for d in m.group(1).split(",")]; assert "ex:TK_Exam_AnswerMethods_Build" in deps and "ex:TK_Exam_AnswerMethods_Repair_Build" in deps
    nd = ", ".join(d for d in deps if d != "ex:TK_Exam_AnswerMethods_Build"); t = t[:i] + b.replace(m.group(0), "backlog:dependsOn " + nd + m.group(2), 1) + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Exam_AnswerMethods and its tasks cancelled (superseded by ST_Exam_AnswerMethods_Repair) with an as-is fit-gap and impact analysis and a closure report marked CANCELLED; the dependency of the not-started Papers and Grading Build tasks on the cancelled Build task removed (the repair Build task stays)")))
