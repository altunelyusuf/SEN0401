#!/usr/bin/env python3
"""sen0401_lineage_sprint_correction v1_0_0 - corrections ordered by the owner on 2026-10-21 10:14 Istanbul (quoted in OWNER): plan and decide first, execute and control later, run the work per sprint.
One call = one new register version; the caller validates, checks and commits each alone. Events, in order:
  owner      the owner's message recorded with the quote and the time (notes only)
  status     G113: the false 'work begun' of v0.146 (07:05:34 UTC) is moved back to Ready by recorded transitions (T_Return) with a dated note, and the start times removed
  sprint     Iter_12 is closed by a review ceremony (it holds only the gap work, all Done) and Iter_13 is planned for the template and chapter 8 work: sprint goal, start, proposed end, members (memberOfContainer and hasMember),
             planning events re-pointed, planning ceremony, plan baseline
  structure  the four stories: stand-alone declaration (no epic) with the reasons from the discipline, an explicit story dependency, the checks made
Usage: sen0401_lineage_sprint_correction_v1_0_0.py owner|status|sprint|structure"""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_gap_revision_v1_0_0 as G

lit, esc, blk = G.lit, M.esc, T.blk
WHEN = "Wednesday 2026-10-21 10:14 Istanbul (2026-10-21T07:14:00 UTC)"
OWNER = ('Owner\'s message, relayed by the course coordinator on %s, quoted: "I think you need to correct the stories appropriately and connect the tasks with the stories and run them per sprint rather than ad hoc initiation of the agents out of the lineage. '
         'It is a drift to find a solution to an issue after the happening. We have a clean discipline first to plan and decide, later execute and control. Your approach is to start unconditionally and find a way to deal with. This makes the progress much more complicated. '
         'Why don\'t you keep the lineage standards? If you can find the root-cause we can ask BRSF to build preventive measures against such cases." Recorded as owner-directed work: the corrections below follow it. No work agent had started on the template work; '
         'the root cause was written as a handover to the BRSF package (pending in its handover inbox, 2026-10-21).' % WHEN)
FALSE = ["TK_Ch08Ex_Build", "TK_PageTpl_Ch10_Build", "TK_PageTpl_Ch11_Build", "TK_PageTpl_Ch12_Build", "TK_PageTpl_Ch14_Build", "ST_Page_Template", "ST_Ch08_Examples"]
TEMPLATE_ITEMS = ["ST_Page_Template", "ST_Ch08_Examples", "TK_Ch08Ex_Build", "TK_Ch08Ex_Verify"] + ["TK_PageTpl_%s_%s" % (c, k) for c in ("Ch08", "Ch10", "Ch11", "Ch12", "Ch14") for k in ("Build", "Verify")]


def ev_owner(t):
    L = ['ex:%s rdfs:comment %s@en .\n' % (s, lit(x)) for s, x in (
        ("Lineage3", "Owner-directed corrections. " + OWNER),
        ("CR_SEN0401", "Before the closure act: " + OWNER),
        ("CR3_Pages", "Owner-directed corrections to the execution of this change: " + OWNER))]
    return t + "\n" + "".join(L), "The owner's message of 2026-10-21 10:14 Istanbul recorded as owner-directed work with the quote and time; notes only."


def ev_status(t):
    now = M.now(); L = []
    for k in FALSE:
        i, j = blk(t, k); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, k
        start = m.group(1)
        t = t[:i] + b.replace(m.group(0), "backlog:hasState backlog:Ready", 1) + t[j:]
        L.append('ex:Start3T_%s a backlog:TransitionEvent ; rdfs:label "%s start recorded in v0.146"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote "Recorded in v0.146 at the coordinator\'s request, before any executor had started: no work was begun. Kept as the record of what the register said; reversed by the return below." .\n' % (k, k, k, start))
        L.append('ex:Return3T_%s a backlog:TransitionEvent ; rdfs:label "%s returned to Ready"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Return ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote "Correction on %s (G113: every status change is an obligation, and a status must be the truth): the item was In Progress in v0.146 from %s UTC with no executor and no work; it is Ready again and its start time is withdrawn. A coordination error of the builder session, which recorded a start that had not happened instead of refusing it. Work begun is recorded again only at the real start of an executor, inside a started sprint, with the executor session named." .\n' % (k, k, k, now, now[:10], start))
        L.append('ex:%s backlog:hasAuditNote "Status correction %s (G113): the In Progress state of v0.146 (%s UTC) was a status without work, a coordination error of the builder session; the item is Ready again by the recorded return ex:Return3T_%s; the start is recorded only at the real start of an executor inside a started sprint." .\n' % (k, now[:10], start, k))
    return t + "\n" + "".join(L), "G113 status correction: the 7 items recorded In Progress in v0.146 (5 tasks and 2 stories) with no executor started are Ready again by recorded transitions (start, then return) with a dated note naming the coordination error of the builder session."


SPRINT_GOAL13 = ("The pages of chapters 8, 10, 11, 12 and 14 are built as new files on the current page template (9.51.0) with the same content and meet the written standard of ex:Spec3T_T, and chapter 8 has real executable examples with numbers so its page passes page test 9.34.0; "
                 "each unit whose check fails is named; then the Mission outcome stays the owner's act. Frozen at the iteration's start: work added later goes to a new iteration or to the owner's rebaseline.")


def ev_sprint(t):
    now = M.now(); L = []
    # (a) Iter_12: the extension of its goal and the template members are withdrawn; it is closed by a review
    t = t.replace(" Then (added 2026-10-21 on the owner's message): the pages of chapters 8, 10, 11, 12 and 14 are rebuilt on the current page template and meet the written standard, and chapter 8 has real examples with numbers, each unit that fails named.", "", 1)
    t, k1 = re.subn(r"\nex:Iter_12 backlog:hasMember ex:ST_Page_Template[^\n]*\n", "\n", t, count=1); assert k1 == 1
    t, k2 = re.subn(r"\nex:Iter_12 rdfs:comment \"Extended on 2026-10-21 by the stage revision[^\n]*\n", "\n", t, count=1); assert k2 == 1
    i, j = blk(t, "Iter_12"); b = t[i:j]
    b2 = b.replace('backlog:iterationEnd "2026-10-23T06:00:00"^^xsd:dateTime', 'backlog:iterationEnd "%s"^^xsd:dateTime' % now, 1); assert b2 != b
    b2 = re.sub(r'(backlog:hasDurationSource ")', lambda m: m.group(1) + "Closed ahead of its proposed end on %s by the review ex:RC3_Iter_12: every member is Done, the end is the instant of the review (the proposed end was 2026-10-23T06:00 UTC, the plan baseline keeps it). " % now[:10], b2, count=1)
    t = t[:i] + b2 + t[j:]
    L.append('ex:Rebase3_Iter_12 a backlog:Rebaseline ; rdfs:label "Iteration 12 closed ahead of its proposed end"@en ; backlog:rebaselines ex:Iter_12 ; backlog:hasPreviousTarget "2026-10-23T06:00:00" ; backlog:hasNewTarget "%s" ;\n'
             '    backlog:hasRebaselineRationale %s ; backlog:rebaselinedAt "%s"^^xsd:dateTime ; backlog:decidedBy backlog:Owner .\n' % (
                 now, lit("Owner direction relayed 2026-10-21 10:14 Istanbul: close Iter_12 properly with its gap work, all Done, and plan the template and chapter 8 work as a new iteration. The gap work finished before the proposed end of Friday 2026-10-23 06:00 UTC, so the end of Iter_12 is the instant of its review."), now))
    L.append('ex:Iter_12 rdfs:comment %s@en .\n' % lit("Corrections of %s, ordered by the owner (%s): the sprint goal is back to the gap work it was planned for (the sentence added mid-sprint for the template work is withdrawn: a sprint goal is not extended, a new iteration is planned), the template stories and tasks belong to ex:Iter_13, and this iteration, which holds only the gap work, is closed by a review ceremony. The planning ceremony ex:PC3_Iter_12 is recorded afterwards from the existing planning events." % (now[:10], WHEN)))
    L.append('ex:PC3_Iter_12 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 12, recorded afterwards from its planning events"@en ; backlog:ceremonyFor ex:Iter_12 ; backlog:heldAt "2026-10-20T16:04:32"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3G_ST_Gap_Stage3F, ex:Plan3G_ST_Gap_Stage4, ex:Plan3G_ST_Gap_Stage3F_Ch05 ;\n    rdfs:comment "Recorded on %s: the iteration was planned on 2026-10-20 without a planning ceremony record; this one names the existing planning events (the chapter 5 event was added to the open iteration on 2026-10-20 night)."@en .\n' % now[:10])
    L.append('ex:RC3_Iter_12 a backlog:SprintReviewCeremony ; rdfs:label "Review of iteration 12: the gap work, closed"@en ; backlog:ceremonyFor ex:Iter_12 ; backlog:reviewsCeremony ex:PC3_Iter_12 ; backlog:closesIteration ex:Iter_12 ;\n    backlog:closesStory ex:ST_Gap_Stage3F, ex:ST_Gap_Stage4 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment "Held %s: both stories and all 22 tasks of the iteration are Done with bridge-verified evidence (v0.134, v0.136, v0.137); the Stage 3.F and Stage 4 readings are 3 of 3 and 8 of 8 (v0.138 measurement of all 15 units; no file of those units changed since, read from git). Nothing is carried over: the template and chapter 8 work was never started and is planned into ex:Iter_13."@en .\n' % (now, now[:10]))
    # readings at the review, linked to it
    base = subprocess.run(["git", "-C", M.REPO, "diff", "--stat", "11eba86", "HEAD", "--", "03-materials"], capture_output=True, text=True).stdout.strip()
    changed = [l for l in base.splitlines() if "/ch0" in l and any("/ch0%d/" % n in l for n in range(1, 8)) or "numbers" in l]
    for obj, met, val, what in (("Obj3_Stage3FPass", "Met3_Stage3FPass", "3", "Stage 3.F passes for chapters 1 and 5 and Bitcoin in numbers: 3 of 3"), ("Obj3_Stage4Pass", "Met3_Stage4Pass", "8", "the Stage 4 gate run of chapters 1 to 7 and Bitcoin in numbers exits 0: 8 of 8")):
        L.append('ex:Obs40_%s a backlog:MetricObservation ; rdfs:label "Reading at the review that closed iteration 12"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%s"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony ex:RC3_Iter_12 ;\n    backlog:hasObservationMethod "Read %s from the measurement of v0.138 (the Stage 4 gate runner v1_1_0 for all 15 units, 2026-10-21): %s. Files of those units changed in git since the measurement: %s." .\n' % (obj, met, obj, val, now, now[:10], what, "none" if not changed else "; ".join(changed)))
    # (b) Iter_13
    mem = TEMPLATE_ITEMS
    for k in mem:
        i, j = blk(t, k); b = t[i:j]; assert "backlog:memberOfContainer ex:Iter_12" in b, k
        t = t[:i] + b.replace("backlog:memberOfContainer ex:Iter_12", "backlog:memberOfContainer ex:Iter_13", 1) + t[j:]
        t = t.replace("ex:Refine_%s a backlog:RefinementEvent ; rdfs:label \"Refinement that made %s ready\"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt" % (k, k, k), "ex:Refine_%s a backlog:RefinementEvent ; rdfs:label \"Refinement that made %s ready\"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt" % (k, k, k), 1)
        i, j = t.index("\nex:Refine_%s a backlog:RefinementEvent" % k) + 1, None
        j = t.find("\nex:", i + 5)
        rb = t[i:j]; rb2 = rb.replace("backlog:groomsForIteration ex:Iter_12", "backlog:groomsForIteration ex:Iter_13", 1); assert rb2 != rb, k
        t = t[:i] + rb2 + t[j:]
    for s in ("ST_Page_Template", "ST_Ch08_Examples"):
        i = t.index("\nex:Plan3T_%s a backlog:PlanningEvent" % s) + 1; j = t.find("\nex:", i + 5)
        pb = t[i:j]; pb2 = pb.replace("backlog:plannedInto ex:Iter_12", "backlog:plannedInto ex:Iter_13").replace("into iteration 12", "into iteration 13"); assert pb2 != pb
        t = t[:i] + pb2 + t[j:]
    L.append('ex:Iter_13 a backlog:Iteration ; rdfs:label "Iteration 13: rebuild the pages of chapters 8, 10, 11, 12 and 14 on the current template and give chapter 8 real examples"@en ; backlog:hasIdentifier "Iter_13" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-23T06:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
                 now, lit("Proposed by the builder session on %s: the start is the instant of the planning ceremony ex:PC3_Iter_13; the proposed end is Friday 2026-10-23 06:00 UTC (09:00 Istanbul), the end of the earlier iterations that the owner confirmed on 2026-10-19. The end is the owner's to decide: the plan stands whatever end he gives, and a story still open at the end shows as spillover (L4) until he rebaselines or recommits." % now[:10]),
                 lit(SPRINT_GOAL13), ", ".join("ex:" + x for x in mem)))
    L.append('ex:PB3T_Iter_13 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 13 when it was planned"@en ; backlog:baselineFor ex:Iter_13 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-23T06:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_13 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 13: the template pages and the chapter 8 examples"@en ; backlog:ceremonyFor ex:Iter_13 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3T_ST_Page_Template, ex:Plan3T_ST_Ch08_Examples ;\n    rdfs:comment %s@en .\n' % (now, lit("Held %s by the builder session, after the owner's message of %s (quoted in ex:CR3_Pages and ex:Lineage3): the stories ST_Page_Template and ST_Ch08_Examples and their 12 tasks are committed to this iteration, whose goal is frozen at its start. Their planning events of 2026-10-21, first placed into the closed gap iteration, are re-pointed here. No executor has started; work begun is recorded at the real start of each executor session." % (now, WHEN))))
    L.append("ex:Iter_13 rdfs:comment %s@en .\n" % lit("Corrected placement %s: the template and chapter 8 items were put into ex:Iter_12 by v0.145 (the sprint goal of that iteration was extended mid-sprint); they belong to this iteration by memberOfContainer and hasMember alike." % now[:10]))
    return t + "\n" + "".join(L), "Iter_12 closed by a review ceremony (gap work, all Done; its goal restored; the template items withdrawn) and Iter_13 planned for the template and chapter 8 work: sprint goal, start, proposed end 2026-10-23T06:00 UTC (the owner decides), 14 members, plan baseline, planning ceremony, planning events re-pointed."


STAND = ("Stands alone: this story has no epic. The discipline gives no rule that a story needs a parent, and the register is conformant with stories that stand alone (the link-pass stories ex:ST_Deck_LinkPass and ex:ST_Page_LinkPass of this lineage). "
         "A child added to an epic or initiative that is Done reopens it in effect (G130 Q4), and the epics EP_Deck, EP_Research, EP_Page and the initiative Init_Slides are Done with their children fixed (G125: a Done item stays Done); a new epic is an item of the Backlog stage, so a revision from the Backlog stage (about three versions) "
         "for a grouping the owner has not asked for. The tasks are tied to this story by decomposesInto (the inverse partOf is inferred), each Verify task dependsOn its Build task, and each task and the story belong to one iteration by memberOfContainer and hasMember.")


def ev_structure(t):
    now = M.now(); L = []
    for s in ("ST_Gap_Stage3F", "ST_Gap_Stage4", "ST_Page_Template", "ST_Ch08_Examples"):
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (s, lit("Structure checked %s (owner's message of %s): one deliverable (%s), one acceptance criterion per unit, every task decomposes from this story, Verify tasks depend on their Build tasks. %s" % (now[:10], WHEN, {"ST_Gap_Stage3F": "ex:Del3_Stage3FRepair", "ST_Gap_Stage4": "ex:Del3_Stage4PageAbox", "ST_Page_Template": "ex:Del3_PageTemplate", "ST_Ch08_Examples": "ex:Del3_Ch08Examples"}[s], STAND))))
    L.append("ex:ST_Page_Template backlog:dependsOn ex:ST_Ch08_Examples .\n")
    L.append('ex:ST_Page_Template backlog:hasAuditNote %s .\n' % lit("Dependency made explicit %s: the criterion of the page of chapter 8 (ex:AC3T_Ch08) includes page test 9.34.0, which the chapter 8 examples (ex:ST_Ch08_Examples) make pass; the page of chapter 8 is rebuilt after them (ex:TK_PageTpl_Ch08_Build dependsOn ex:TK_Ch08Ex_Build)." % now[:10]))
    return t + "\n" + "".join(L), "The four gap and template stories declared stand-alone with the reasons from the discipline (G125, G130 Q4), their structure checked, and the story dependency of the template story on the chapter 8 examples made explicit."


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"owner": ev_owner, "status": ev_status, "sprint": ev_sprint, "structure": ev_structure}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev](t)
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
