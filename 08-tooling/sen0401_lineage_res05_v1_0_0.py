#!/usr/bin/env python3
"""sen0401_lineage_res05 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the gap the control of the chapter 14 deck (v0.361.0) found: the Deck chapter check leaves /tmp/sen0401_fx_* folders until the root disk is full. A ChangeRequest ex:CR3_TmpLeak with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS one story, ST_TmpCleanup, into the NEW Iteration 32 (planned, not started). Same route as sen0401_lineage_res04. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
CR = "ex:CR3_TmpLeak"; REV = "ex:Revision_Lineage3_Scope16"
ACTIVE = ["ex:Out3_ScopeR16", "ex:Out3_GoalR16", "ex:Out3_ObjectiveR16", "ex:Out3_BacklogR18"]; NEWB = "ex:Out3_BacklogR19"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the lineage agent while controlling the chapter 14 deck (register v0.361.0): the root disk had 0 MB free; the control run of the Deck chapter check v1_3_0 died in its fixture part with OSError 28 (No space left on device) and the first control run was discarded and rerun. Cause: 34 directories /tmp/sen0401_fx_* (1.7 GB), the output folders of the deck fixtures tool (sen0401_deck_fixtures_v1_2_0.py line 149, tempfile.mkdtemp, never removed), left by every run of the Deck chapter check; "
        "the same leak is named in the briefs' DISK paragraph for /tmp/sen0401_page_test_*. 16 folders older than 30 minutes were removed by the lineage agent to continue; 18 recent ones were left in case executors were running.")
TXT_TMP = ("Make NEW tool files so that the Deck chapter check leaves no temporary folder: (1) 08-tooling/sen0401_deck_fixtures_v1_3_0.py from v1_2_0 (which stays byte-identical, SHA-256 before and after): the output folder it creates with tempfile.mkdtemp is removed when it finishes, whatever the result, unless it is given an output folder or --keep; its refusals, messages and exit codes are unchanged; "
           "(2) 08-tooling/sen0401_lineage_chapter_check_v1_4_0.py from v1_3_0 (which stays byte-identical) that uses the fixtures v1_3_0 and removes the folders of its own HermiT part (prefix hermit_) as well; every check, message and exit code is otherwise unchanged. PROOF kept as logs: unified diffs; SHA-256 of v1_2_0 and v1_3_0 before and after; the count of /tmp/sen0401_fx_* and /tmp/hermit_* before and after one run of Deck/Ch09 and one of Research/Ch09 with the new versions (no new folder remains); the results of the old and the new chapter check on Deck/Ch09, Deck/Ch12 and Research/Ch09 are equal line by line except the version line; a fixture the check should refuse is still refused. " + R.NOEDIT + " " + R.COMMON)
STS = [("ST_TmpCleanup", "The Deck chapter check leaves no temporary folder, as new tool versions", ["AC9_TmpCleanup"], ["TK_TmpCleanup_Build", "TK_TmpCleanup_Verify"], "SEN0401-I32-tmpcleanup", TXT_TMP, "Run old and new on the same chapters and compare line by line; count /tmp folders before and after; byte-compare the old versions; nochange.", [], 14, 1, 2.0)]
ITER = ("Iter_32", "Iteration 32: the temporary-folder leak of the Deck chapter check (planned, not started)", "2026-11-04T12:00:00", "2026-11-05T12:00:00", "The Deck chapter check leaves no temporary folder.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_TmpCleanup": ("The Deck chapter check v1_4_0 leaves no temporary folder and changes nothing else", base + "Given the deck fixtures tool v1_2_0 and the chapter check v1_3_0 (both unchanged), when the NEW files fixtures v1_3_0 and chapter check v1_4_0 are made, then ALL of: (1) v1_2_0 and v1_3_0 are byte-identical (SHA-256 before and after); (2) after one run of Deck/Ch09 and one of Research/Ch09 no folder sen0401_fx_* or hermit_* is left that was not there before; (3) the old and the new chapter check print the same lines on Deck/Ch09, Deck/Ch12 and Research/Ch09 except the version line and exit with the same code; (4) a fixture that must be refused is still refused; (5) no committed file is edited; results as printed. " + FACT, "ex:TS_ChapterCheck", "Deck chapter check v1_4_0 (system python3, python-pptx), old v1_3_0 for the comparison")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the temporary-folder leak of the Deck chapter check, as new tool versions"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the three stories into Iteration 31."))
    ia = ('\nex:IA3_TmpLeak a backlog:ImpactAssessment ;\n    rdfs:label "What the temporary-folder repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: two new tool files (fixtures v1_3_0, chapter check v1_4_0). NOT AFFECTED: the controlled criteria of the decks (they stay met), the old tool versions, every committed file. ESTIMATE (G120): 2.0 h plus 1.0 h verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the temporary-folder leak of the Deck chapter check of the control of v0.361.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the temporary-folder leak of the Deck chapter check); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the temporary-folder leak of the Deck chapter check"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_TmpLeak ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the temporary-folder leak of the Deck chapter check: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The Deck chapter check made to leave no temporary folder, as new tool files"
    tx = "New files: the deck fixtures tool v1_3_0 and the chapter check v1_4_0. " + FACT
    L = ('\nex:Del3_Tmp a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Tmp ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the temporary-folder leak of the Deck chapter check). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR17", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the temporary-folder leak of the Deck chapter check: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR17", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Tmp a backlog:Goal ;
    rdfs:label "The Deck chapter check leaves no temporary folder"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR17 .
ex:G3_Tmp rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_TmpLeak; the intent origin is therefore Derived."@en .
ex:Spec3I_Tmp a backlog:Specification ;
    rdfs:label "What it is for the temporary-folder leak repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Tmp ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR17 .
ex:Spec3I_Tmp_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Tmp ; backlog:hasScenarioText %s .
ex:Spec3I_Tmp_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Tmp ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new tool files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR17", "Out3_ScopeR17"), "third lineage, Goal stage rebuilt for the temporary-folder leak of the Deck chapter check: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR17", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Tmp a backlog:Objective ; rdfs:label "The repair met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Tmp ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Tmp ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Tmp ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR17 .
ex:Met3_Tmp a backlog:Metric ; rdfs:label "temporary-folder repair whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Tmp a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "1"^^xsd:decimal .
ex:ObsR24_Tmp_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Tmp ; backlog:observationFor ex:Obj3_Tmp ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Tmp rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_TmpLeak; the intent origin is therefore Derived."@en .
''' % (lit("Count of the repair story (ST_TmpCleanup) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 14 deck on 2026-10-25 (v0.361.0): the repair does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR17", "Out3_GoalR17"), "third lineage, Objective stage rebuilt for the temporary-folder leak of the Deck chapter check: one objective (0 to 4) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR17", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR18"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_TmpLeak and the control of v0.361.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Tmp").replace("ex:Data3S_TC9_", "ex:Data3S_TC9E_").replace("ex:TC9_", "ex:TC9E_"))
    L = [x.replace("ex:TC9_", "ex:TC9E_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Tmp", "Obj3_Tmp", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 32 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Tmp, ex:Spec3I_Tmp_Pass, ex:Spec3I_Tmp_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Tmp backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Tmp a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the temporary-folder leak of the Deck chapter check"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Tmp and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR19", "Out3_ObjectiveR17"), "third lineage, Backlog stage rebuilt: the four arc-check repairs admitted into the planned Iteration 29 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
