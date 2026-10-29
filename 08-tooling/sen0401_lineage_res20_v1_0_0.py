#!/usr/bin/env python3
"""sen0401_lineage_res20 v1_0_0 - change route (G113, G125 route 2, G133, G134, G147) for the finding of the control of TK_Exam_AnswerMethods_Build (register v0.647): the executor's own check C6 FAILS
(1 written number box not detected: a silent wrong answer) and the control found that faint marks are read as empty without a flag (19 in four seed blocks; 8 in the executor's own run, which its criterion does not count).
The suspended task stays Suspended and its criterion is not edited (G125, G133); the repair is a NEW story with a NEW Build and Verify task and a NEW criterion that keeps the C6 criteria and every threshold unchanged,
planned into a NEW iteration (Iter_50: the goal of Iter_48 is frozen at its start). An acceptance criterion is counted by the Backlog digest, so the route is a StageRevision from the Backlog stage (as chapter 5 and ST_Ch10_Consolidate).
Events, one new file each: change | retract | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
lit = G.lit
REV = "ex:Revision_Lineage3_Backlog7"; OLD = "ex:Out3_BacklogR32"; NEW = "ex:Out3_BacklogR33"; ITER = "ex:Iter_50"
CR = "ex:CR3_AnswerRepair"; IA = "ex:IA3_AnswerRepair"; SC = "ex:SC3_AnswerRepair"
SID = "ST_Exam_AnswerMethods_Repair"; BT = "TK_Exam_AnswerMethods_Repair_Build"; VT = "TK_Exam_AnswerMethods_Repair_Verify"; CRIT = "AC3E_Exam_AnswerMethods_Repair"; SESS = "SEN0401-I50-answer-repair"
WHEN = "Friday 2026-10-30, after the control of TK_Exam_AnswerMethods_Build (register v0.647), as relayed by the course coordinator at the owner's standing rule that a repair is registered through change management"
FOUND = ("Found by the control of 2026-10-29 (register v0.647; logs in 08-tooling/verify/iter32/bridge_answering): the executor's own check C6 of the answer sheet and methods (commit 6e37b8e) FAILS on its own evaluation seeds (block 9000): "
         "one written number box is not detected as written, so the reader gives a silent wrong answer (criterion: none allowed); and eight faint marks are read as empty without a flag (its check prints the count but its criterion does not test it). "
         "The control re-ran the measurement with the executor's own C6 criteria on three seed blocks the executor did not use: no silent wrong answer there, so the written-box error is rare and seed-bound; but unflagged empty reads of faint marks occur in all four blocks (8, 4, 6 and 1: 19 in all), so that defect is systematic. "
         "A faint mark read as empty becomes a blank answer for a student without anyone being told, which is the same kind of harm as a silent wrong answer. Held share is 21 to 23 percent against the limit of 25 percent, so there is little room. "
         "The check digit, the sheet geometry, the one-page cost and the executor's own log all reproduced; the failure is in the reader and its measurement only.")
RULE = ("the standing rules: a repair is registered through change management in the active lineage and re-ranks the open items; nothing is waived; a gate, test, threshold or criterion changes only on the owner's explicit word")

def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Answer sheet reader: no silent wrong answer and no faint mark read as empty, found by the control of the answering-methods task"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_ExamMission, ex:IA3_ExamMission ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(
        "Raised " + WHEN + ". " + FOUND + " Rules applied: " + RULE + ". The task ex:TK_Exam_AnswerMethods_Build stays Suspended and its criterion ex:AC3E_Exam_AnswerMethods is not rewritten (G125, G133); the repair is a NEW story ex:" + SID + " with a new Build task, a new Verify task and a new criterion. "
        "THE NEW CRITERION KEEPS THE EXECUTOR'S C6 CRITERIA AND EVERY THRESHOLD UNCHANGED (no registration failure, no silent wrong answer, no missed ambiguous row, every code slip and swap detected, at most 25 percent of recoverable rows held for a person); it adds the requirement that no mark is read as empty without a flag, which the check prints but never tested. "
        "The repair is evaluated on the original seed block 9000 and on held-out blocks that the control chooses at control time and does not name in advance, so that the reader cannot be tuned on the evaluation seeds (calibration stays on the seeds 1000 to 1099 or on a new calibration block the executor names before the run). "
        "If the 25 percent limit cannot be met together with the other criteria, the result is reported as printed and the repair is named failing; the limit is not raised (it changes only on the owner's word). "
        "A new criterion is counted by the Backlog digest, so the route is a revision from the Backlog stage (G125 route 2). Pending until the ScopeChange that admits the new story is recorded."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the repair of the answer sheet reader costs, measured before it is started"@en ;\n'
          '    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_ExamMission ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(
        FOUND + " WHAT MOVES: the Backlog digest of the third lineage once, when the stage is closed again (one more story, two tasks, one criterion, one planning event, one iteration); Scope, Goal and Objective digests do not move. "
        "NEW ITEMS: the story ex:" + SID + " (it satisfies ex:Del3_ExamPapers and pursues ex:Obj3_Exam like the story it repairs), the tasks ex:" + BT + " and ex:" + VT + ", the criterion ex:" + CRIT + ", planned into the NEW iteration ex:Iter_50 (the goal of ex:Iter_48 is frozen at its start). "
        "The new files are a reader v1.1.0, a measurement and a check v1.1.0, as new files; the files of v1.0.0 are not edited. DEPENDENCIES CORRECTED: ex:TK_Exam_Papers_Build and ex:TK_Exam_Grading_Build read the sheet and the reader, so they now also wait for the repair Build task. "
        "THE SUSPENDED TASK: ex:TK_Exam_AnswerMethods_Build stays Suspended; how it reaches Done (a control over its own files together with the repair's files, against its own criterion unchanged) is decided at the control of the repair; nothing is waived. "
        "COST OF WAITING: papers whose answer sheets are read with a silent error and blank answers that no one is told about. COST OF ACTING: three register versions and one executor session of about three hours; the executor runs one at a time (disk), so the repair follows the engine executor, which is Done. Not affected: every Done item, the engine, the paper rules, the critical points, the committed files, the owner's questions Q1 to Q16."))
    return t + cr + ia, "ChangeRequest ex:CR3_AnswerRepair (Pending) and ImpactAssessment ex:IA3_AnswerRepair: the control of the answering-methods task found a silent wrong answer in the executor's own C6 run and faint marks read as empty without a flag; the C6 criteria and thresholds stay unchanged; no stage changed."

def ev_retract(t):
    t = X.set_status(t, "LS_Opened") if False else t
    reason = (FOUND + " The new acceptance criterion of the new story ex:" + SID + " is counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit; the items already in the register, Done ones included, re-enter by admission, not re-dated.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the repair of the answer sheet reader found by the control"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    t = X.set_status(t, "LS_Objectived")
    return t + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the repair of the answer sheet reader; nothing is rebuilt here." % OLD.replace("ex:", "")

BUILD_TXT = ("REPAIR the answer sheet reader, as NEW files (reader v1.1.0 of sen0401_exam_answersheet_v1_0_0.py, a measurement and a check v1.1.0, their logs); the v1.0.0 files and every committed file are not edited, and your own log files are never appended to. "
             "WHAT THE CONTROL FOUND (register v0.647): (a) on your evaluation block (seeds 9000 and up) ONE written number box is not detected as written, which is a silent wrong answer (your own C6 criterion allows none); the control found none in three other seed blocks, so it is rare and seed-bound; "
             "(b) FAINT MARKS ARE READ AS EMPTY WITHOUT A FLAG: your check prints the count (8 on your block) but your criterion does not test it; the control found 8, 4, 6 and 1 in four blocks (19), so it is systematic. A faint mark that the reader cannot call must be held for a person with a flag, never read as empty and never as an answer. "
             "REQUIREMENTS, all together: (1) the C6 criteria of your v1.0.0 check, UNCHANGED and with the same thresholds: no registration failure, no silent wrong answer, no missed ambiguous row, every code slip and swap detected, the reader without the methods still makes at least one silent wrong answer or misses one, and AT MOST 25 PERCENT of recoverable rows held for a person; "
             "(2) NEW: zero marks read as empty without a flag, counted in the criterion; (3) find the root cause of (a) and (b) by looking at the failing rows (print them) before changing the reader; do not widen a tolerance to make the count go to zero without showing why the rows are right; "
             "(4) CALIBRATE ONLY on the seeds 1000 to 1099 or on a new calibration block that you name BEFORE the run; evaluate on the original block 9000 AND on a held-out block of your choosing that you did not use for calibration, named before the run; the control will evaluate on further blocks that it does not name, so tuning on any evaluation seed will be found out; "
             "(5) if the 25 percent limit cannot be met together with the others, STOP and report the numbers as printed: the limit, a threshold, a test or a criterion is NOT changed by you, it changes only on the owner's explicit word; "
             "(6) report as printed, including every disclosure: what was tuned, on which seeds, what is still unmeasured; synthetic marks only, say so; the owner's questions Q11 to Q16 stay as they are. Free disk is about 1.6 GB: tell the coordinator at once if it falls under 0.9 GB. One build at a time.")
VERIFY_TXT = ("Re-run the executor's new check; compute on the control's own seed blocks (not named in advance) the C6 criteria and the unflagged-empty count with the repaired reader and with the v1.0.0 reader; confirm that no tuning seed is among them; confirm the v1.0.0 files and every committed file are byte-identical; read the printed rows of the former failures.")

def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged")
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEW)
    now = M.now(); L = []
    note = "Admitted by the change request " + CR[3:] + " (" + WHEN + "). One criterion per unit (G133). Done and Suspended items stay as they are and are not edited (G125). " + RULE + "."
    gh = ("Given the answer sheet and the reader of commit 6e37b8e (the reader gives a silent wrong answer on one written number box in the evaluation block 9000 and reads faint marks as empty without a flag: 8 in that block, 19 in four blocks), when a reader v1.1.0 is made as new files and its check is run, then ALL of: "
          "(1) every file is new and no committed file is edited; (2) the C6 criteria of the check v1.0.0 hold UNCHANGED with the same thresholds, on the original block 9000, on the executor's named held-out block and on the control's blocks that are not named in advance: no registration failure, no silent wrong answer, no missed ambiguous row, every code slip and swap detected, the reader without the methods still fails at least once, at most 25 percent of recoverable rows held for a person; "
          "(3) no mark is read as empty without a flag, over every block; (4) the calibration seeds are named before the run and are not among the evaluation seeds; no criterion, threshold or test is edited; (5) results as printed: if any element fails the repair is named failing. Source: the control of register v0.647.")
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS_ChapterCheck ;\n    backlog:measuredWithVersion "checks written by the executor as new files, run by the control on the evidence bridge with the control\'s own seed blocks" ;\n'
             '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3E_AnswerRepair_Passes, ex:TC3E_AnswerRepair_NotClaimed .\n'
             'ex:TC3E_AnswerRepair_Passes a backlog:TestCase ; rdfs:label "Run the repaired reader on the original and held-out seed blocks"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:%s ; backlog:coversScenario ex:Spec3I_Exam_Pass ; backlog:runsOnData ex:Data3E_AnswerRepair_Passing ;\n    backlog:hasCaseText "Run the check v1.1.0; it reports no failure and exits 0." .\n'
             'ex:TC3E_AnswerRepair_NotClaimed a backlog:TestCase ; rdfs:label "Run the check on the unrepaired reader and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:%s ; backlog:coversScenario ex:Spec3I_Exam_Fail ; backlog:runsOnData ex:Data3E_AnswerRepair_Failing ;\n    backlog:hasCaseText "Run the new criteria on the reader of v1.0.0: it must fail them (a silent wrong answer on block 9000 and unflagged empty reads)." .\n'
             'ex:Data3E_AnswerRepair_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .\n'
             'ex:Data3E_AnswerRepair_Failing a backlog:TestData ; rdfs:label "The unrepaired reader that fails the criteria"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState "The reader of commit 6e37b8e, which has a silent wrong answer on block 9000 and unflagged empty reads, for which the new criteria must fail." .\n' % (
        CRIT, lit("Criterion of the repair of the answer sheet reader"), lit(gh), CRIT, CRIT))
    title = "Repair the answer sheet reader: no silent wrong answer and no faint mark read as empty"
    L.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
             '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n    backlog:satisfiesDeliverable ex:Del3_ExamPapers ; backlog:pursuesObjective ex:Obj3_Exam ; backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:coversEntity ex:DE3_AnswerSheet ; backlog:coversStage backlog:Stage_Creation ;\n'
             '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n    backlog:decomposesInto ex:%s, ex:%s ;\n    backlog:hasState backlog:Proposed ;\n'
             '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored by the ranking step of the same change route." ;\n    backlog:hasAuditNote %s .\n' % (
        SID, lit(title), SID, lit(title), ITER, NEW, lit(title[0].lower() + title[1:]), lit("a student's answer is never silently changed or lost when the paper is read, and the instructor can grade the papers"), CRIT, G.EXEC, BT, VT, lit(note)))
    for tid, tt, ttype, dp, txt in ((BT, "Build: " + title, "Build", ["TK_Exam_PaperRules_Build"], BUILD_TXT), (VT, "Verify: " + title, "Verify", [BT], VERIFY_TXT)):
        full = txt + " Planned session %s (an estimate, G120: the real start is recorded at work begun); about %.1f hours." % (SESS if ttype == "Build" else "builder", 3.0 if ttype == "Build" else 1.0)
        L.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
                 '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Proposed ;\n    backlog:dependsOn %s ;\n'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
            tid, lit(tt), tid, lit(tt), ITER, NEW, G.EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, ", ".join("ex:" + d for d in dp), lit(full)))
    L.append("ex:%s backlog:standsAlone true .\n" % SID)
    L.append('ex:Plan3E_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 50"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec3I_Exam, ex:Spec3I_Exam_Pass, ex:Spec3I_Exam_Fail .\n' % (SID, SID, now, ITER, SID, BT, VT))
    for x in (SID, BT):
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the finding of the control (ex:IA3_AnswerRepair); the criterion and the task text name the criteria, the seeds rule and what a passing result is." .\n' % (x, x, x, now, ITER))
    # dependencies of the tasks that read the sheet
    for tk in ("TK_Exam_Papers_Build", "TK_Exam_Grading_Build"):
        i, j = T.blk(t, tk); b = t[i:j]; m = re.search(r"backlog:dependsOn ([^;]*);", b); assert m, tk
        assert "ex:" + BT not in m.group(1)
        t = t[:i] + b.replace(m.group(0), "backlog:dependsOn %s, ex:%s ;" % (m.group(1).strip(), BT), 1) + t[j:]
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (tk, lit("Dependency corrected %s (ex:IA3_AnswerRepair): this task reads the answer sheet and its reader, so it also waits for the repair of the reader (ex:%s)." % (now[:10], BT))))
    L.append('ex:TK_Exam_AnswerMethods_Build backlog:hasAuditNote %s .\n' % lit("Note %s: stays Suspended (C6 not met, recorded in v0.647); the repair is the new story ex:%s (ex:CR3_AnswerRepair). How this task reaches Done is decided at the control of the repair, against its criterion unchanged; nothing is waived." % (now[:10], SID)))
    L.append('ex:Iter_50 a backlog:Iteration ; rdfs:label "Iteration 50: repair the answer sheet reader found by the control"@en ; backlog:hasIdentifier "Iter_50" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-11-01T12:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember ex:%s, ex:%s, ex:%s .\n' % (
        now, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony ex:PC3_Iter_50; the end is the end of ex:Iter_48 (2026-11-01T12:00:00 UTC, when chapter work restarts); one executor task of about three hours and one verification of about one hour, one executor at a time (disk). Why a new iteration: the goal of ex:Iter_48 is frozen at its start. The end is the owner's to decide. Estimates, not measurements (G120)." % now[:10]),
        lit("The answer sheet reader gives no silent wrong answer and reads no faint mark as empty without a flag, on the original and held-out seed blocks, with the C6 criteria and thresholds unchanged. Frozen at the iteration's start."), SID, BT, VT))
    L.append('ex:PB3_Iter_50 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 50 when it was planned"@en ; backlog:baselineFor ex:Iter_50 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-11-01T12:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_50 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 50: the repair of the answer sheet reader"@en ; backlog:ceremonyFor ex:Iter_50 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3E_%s ;\n    rdfs:comment %s@en .\n' % (
        now, SID, lit("Held %s by the lineage agent after the control of the answering-methods task: the story %s is committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of the session with its brief." % (now, SID))))
    L.append('%s a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the repair of the answer sheet reader"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Builder ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        SC, CR, SID, lit("A repair of delivered work found by the control, registered under the standing rules (" + RULE + "). " + FOUND)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange %s and the story it admits; it was Pending before. The owner\'s standing rule is the decision: repairs are registered through change management and re-rank the open items."@en .\n' % (CR, now[:10], SC[3:]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt by the stage revision from the Backlog stage for the repair of the answer sheet reader"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR30 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt for the repair of the answer sheet reader: story %s with Build and Verify tasks and criterion %s in the new Iteration 50, dependencies of the papers and grading tasks corrected, scope change %s, change request Accepted; %d items re-admitted, not re-dated." % (SID, CRIT, SC[3:], n)

def ev_fill(t, prev):
    return G.fill_re(t, NEW, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the repair is planned, no work begun." % (NEW.replace("ex:", ""), prev)

def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    if ev not in fn: raise SystemExit(__doc__)
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))

if __name__ == "__main__":
    main()
