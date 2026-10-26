#!/usr/bin/env python3
"""sen0401_lineage_res12 v1_0_0 - change route for the chapter 1 page: the four deck hyperlinks of slide 19 that the page 9.72.0 does not carry. A ChangeRequest ex:CR3_Ch01PageLinks, then a StageRevision from the Scope stage that ADMITS ST_Ch01_PageLinks into the NEW Iteration 38 (planned, not started). Same route as sen0401_lineage_res11. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_Ch01PageLinks"; REV = "ex:Revision_Lineage3_Scope22"
ACTIVE = ["ex:Out3_ScopeR22", "ex:Out3_GoalR22", "ex:Out3_ObjectiveR22", "ex:Out3_BacklogR24"]; NEWB = "ex:Out3_BacklogR25"; R.NEWB = NEWB
WHEN = "Monday 2026-10-26, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders and said no question to the owner is needed; nothing is waived)"
FACT = ("MEASURED 2026-10-26 by the lineage agent in the control of the chapter 1 page 9.72.0 (register v0.474.0), with the control's own deck-link check (sen0401_page_control_check_v1_4_0.py ... links): the newest chapter 1 deck v3_1_0 carries 26 hyperlinks; 4 of them are NOT in the page 9.72.0: the Source links of the Kenya, Cyprus, Greece and Venezuela cases on slide 19 "
        "(https://en.wikipedia.org/wiki/M-Pesa, https://en.wikipedia.org/wiki/2012%E2%80%932013_Cypriot_financial_crisis, https://en.wikipedia.org/wiki/Greek_government-debt_crisis, https://en.wikipedia.org/wiki/Hyperinflation_in_Venezuela); the fifth (Ukraine, nbclosangeles.com) is carried. The same links were not in the page 9.70.0 either and slide 19 held them in the deck v3_0_0, so the gap is old, not a regression. "
        "The deck match check v1_0_0 compares the READ cards and the resources slide only, so it cannot see it; the criterion AC9_Page_Ch01 does not name it, so the page 9.72.0 stays Done on its criterion. The chapters 2 and 5 to 8 pages carry every deck hyperlink (13 of 13, 18, 14, 18 and 14).")
TXT = ("Make a NEW page of chapter 1 with a page version above 9.72.0 (9.73.0), as new files only, on the template 9.52.4 with the builders v4_15_0 and v2_24_0 and the same chapter-code manifest, in which the page carries the four Source links of the deck v3_1_0 slide 19 that it lacks (the Kenya, Cyprus, Greece and Venezuela cases; addresses in the criterion) as live links beside the case texts, in the way the page carries the Ukraine source of the same slide (the lecture data of that slide: derive them from the deck, do not type them by hand; a new lecture or data file with a new version number is allowed, the page 9.72.0 and every committed file stay unchanged). "
       "Nothing else of the content changes. PROOF kept as logs written into the repository (not /tmp), each written once after its run is complete: the charset check; the page tests 9.37.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST, serially, each under `flock /tmp/page_test.lock`; a main-thread budget failure may be rerun up to three times, every run kept); the story layout probe under the lock; the Stage 4 gate runner v1_1_0; the chapter checks Research, Deck and Page (the Page check under the lock); the deck match check v1_0_0; and a count of the deck's hyperlinks against the page (all 26 addresses of deck v3_1_0 present in the page); nochange (every file of your commits added). "
       "STATE which page version each check tested. DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES. No gate, test or threshold is edited. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. Commit your work to main (pull --rebase before push). The browser runs ONLY under the lock.")
VT = "Run the page tests, the story layout probe, the Stage 4 gates, the chapter checks and the deck match on the new page under the lock; count the deck's 26 hyperlinks against the page; read the page; nochange."
STS = [("ST_Ch01_PageLinks", "The page of chapter 1 carries every hyperlink of its deck, as a new page version", ["AC9_PageLinks_Ch01"], ["TK_Ch01_PageLinks_Build", "TK_Ch01_PageLinks_Verify"], "SEN0401-I38-page-ch01links", TXT, VT, [], 1, 1, 2.0)]
ITER = ("Iter_38", "Iteration 38: the chapter 1 page carries every hyperlink of its deck (planned, not started)", "2026-11-10T12:00:00", "2026-11-11T12:00:00", "The page of chapter 1 carries all 26 hyperlinks of its deck and passes the page tests again.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_PageLinks_Ch01": ("The page of chapter 1 carries every hyperlink of its deck v3_1_0 and passes the page tests, the story layout and the checks of its first criterion, as a new page version", base + "Given the chapter 1 page 9.72.0 delivered (unchanged) and the deck v3_1_0, when a NEW page version above 9.72.0 is built as new files on the template 9.52.4 with the builders v4_15_0 and v2_24_0, then ALL of: (1) the charset check v1_0_0 exits 0; (2) the page tests 9.37.0, 9.34.1 and 9.35.1 exit 0 with no FAIL, no skip, widgets, features and gates not below the stored results of the page 9.72.0; (3) the story layout probe prints RESULT PASS; (4) every hyperlink address of the deck v3_1_0 (26) is in the page, counted by the control's deck-link check; (5) the Stage 4 gate runner v1_1_0 for 01 exits 0, the chapter checks Research, Deck and Page pass, the deck match check v1_0_0 reports 0 not carried; (6) the page ABox and the stored result are new files; (7) no committed file is edited, no gate, test or threshold changed; results as printed; if any element fails the page is named failing. " + FACT, "ex:TS_PageTest37, ex:TS_PageTest34b, ex:TS_PageTest35b, ex:TS_StoryLayoutProbe, ex:TS_Stage4Gates, ex:TS_ChapterCheck, ex:TS_DeckMatch, ex:TS_PageCharsetCheck", "page template 9.52.4; page builder v4_15_0 and page-data builder v2_24_0; page charset check v1_0_0; page tests 9.37.0, 9.34.1 and 9.35.1; story layout probe v1_0_0; Stage 4 gate runner v1_1_0; chapter check v1_3_0; deck match check v1_0_0; page control check v1_4_0 (links)")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The chapter 1 page: the four deck hyperlinks of slide 19 that it does not carry"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the story into Iteration 38."))
    ia = ('\nex:IA3_Ch01PageLinks a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 1 page follow-up costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new deck and a new plan file. NOT AFFECTED: the controlled criteria of the decks (they stay met), the delivered deck, the old plans, every committed file. ESTIMATE (G120): 2.0 h plus 1.0 h verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the missing deck hyperlinks of the chapter 1 page found by the lineage agent in register v0.474.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the chapter 1 page follow-up); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the chapter 1 page follow-up"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch01PageLinks ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the chapter 1 page follow-up: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 1 page made to carry every hyperlink of its deck, as a new page version"
    tx = "New files: the chapter 1 page 9.73.0, its page data, ABox and stored result. " + FACT
    L = ('\nex:Del3_Ch01PageLinks a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Ch01PageLinks ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-26 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the chapter 1 page follow-up). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR23", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the chapter 1 page follow-up: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR23", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Ch01PageLinks a backlog:Goal ;
    rdfs:label "The chapter 1 page carries every hyperlink of its deck"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR23 .
ex:G3_Ch01PageLinks rdfs:comment "Drafted by the lineage agent on 2026-10-26 from the change request ex:CR3_Ch01PageLinks; the intent origin is therefore Derived."@en .
ex:Spec3I_Ch01PageLinks a backlog:Specification ;
    rdfs:label "What it is for the chapter 1 page follow-up to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Ch01PageLinks ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR23 .
ex:Spec3I_Ch01PageLinks_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Ch01PageLinks ; backlog:hasScenarioText %s .
ex:Spec3I_Ch01PageLinks_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Ch01PageLinks ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR23", "Out3_ScopeR23"), "third lineage, Goal stage rebuilt for the chapter 1 page follow-up: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR23", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Ch01PageLinks a backlog:Objective ; rdfs:label "The page follow-ups met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Ch01PageLinks ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Ch01PageLinks ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Ch01PageLinks ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR23 .
ex:Met3_Ch01PageLinks a backlog:Metric ; rdfs:label "chapter 1 page follow-up whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Ch01PageLinks a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "1"^^xsd:decimal .
ex:ObsR29_Ch01PageLinks_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Ch01PageLinks ; backlog:observationFor ex:Obj3_Ch01PageLinks ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Ch01PageLinks rdfs:comment "Drafted by the lineage agent on 2026-10-26 from the change request ex:CR3_Ch01PageLinks; the intent origin is therefore Derived."@en .
''' % (lit("Count of the story ST_Ch01_PageLinks whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 1 page 9.72.0 on 2026-10-26: the page 9.73.0 does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR23", "Out3_GoalR23"), "third lineage, Objective stage rebuilt for the chapter 1 page follow-up: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR23", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR24"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch01PageLinks and the lineage agent in register v0.428.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Ch01PageLinks").replace("ex:Data3S_TC9_", "ex:Data3S_TC9K_").replace("ex:TC9_", "ex:TC9K_"))
    L = [x.replace("ex:TC9_", "ex:TC9K_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Ch01PageLinks", "Obj3_Ch01PageLinks", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 37 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Ch01PageLinks, ex:Spec3I_Ch01PageLinks_Pass, ex:Spec3I_Ch01PageLinks_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-26, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Ch01PageLinks backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Ch01PageLinks a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the chapter 1 page follow-up"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch01PageLinks and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR25", "Out3_ObjectiveR23"), "third lineage, Backlog stage rebuilt: the chapter 1 page follow-up admitted into the planned Iteration 38 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
