#!/usr/bin/env python3
"""sen0401_lineage_res09 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the ten arc-check findings about the delivered chapter 5 deck (found with the new plan file, control of v0.383.0). A ChangeRequest ex:CR3_Ch05DeckFix with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS one story, ST_Ch05_DeckFix, into the NEW Iteration 33 (planned, not started). Same route as sen0401_lineage_res05. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_Ch05DeckFix2"; REV = "ex:Revision_Lineage3_Scope19"
ACTIVE = ["ex:Out3_ScopeR19", "ex:Out3_GoalR19", "ex:Out3_ObjectiveR19", "ex:Out3_BacklogR21"]; NEWB = "ex:Out3_BacklogR22"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the lineage agent (register v0.404.0, after the executor of TK_Ch05_DeckFix_Build stopped without committing): (A) THE GATES CONTRADICT: the arc check v1_3_0 rule 1 refuses a last slide that is not the dark closing slide (it tests the plan's declaration kind closing and bg dark), and the deck standard check v1_1_0 element D9 (one background scheme, the owner's rule against switching dark and light) fails a deck with one dark slide among light ones (1 dark, 67 light, 1 switch). "
        "The decks of chapters 4, 6, 8, 12, 13 and 14 pass both only because their plans DECLARE bg dark for a last slide that is really light (FAF6EF); the plan of chapter 5 v3_2_0 declares it as it is (light), so the arc check refuses it. No deck can satisfy both gates with true declarations. A gate is not changed without the owner's explicit word (scope exclusion): the contradiction is recorded as the pending change request ex:CR3_GateArcDark and is carried, not worked around. "
        "(B) THE NEW PLAN BROKE ANOTHER CHECK: the plan file deck_plan_v3_2_0.json (control of TK_Ch05_ArcPlan_Build, register v0.384.0) is in the arc check's schema but dropped fields that the deck check, the picture check and the fixtures tool read from the NEWEST plan file (picture names, chart items, expressions): the Deck chapter check v1_4_0 on chapter 5 fails the part fixtures of every owner check refused (FAILED ok_image_reencoded, stale_chart, stale_expr, stale_image_swap; with the plan v3_2_0 hidden the same tool says every stale fixture refused, the control accepted). The control of that task did not run the chapter check; this is stated as a gap of the lineage's control and carried by this story. "
        "(C) THE REMAINING ARC FINDINGS (10 refusals with the plan v3_2_0): six slides without takeaway strip (15, 30, 40, 42, 51, 52), notes of slides 13, 21, 65 over the limit, the agenda range at slide 65 and the summary slide not immediately before the resources slide (the summary comes before the resources slide, after the check yourself slide).")
TXT_DK = ("Make a NEW deck 03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_2_0.pptx and a NEW plan 08-tooling/ch05-deck/deck_plan_v3_3_0.json (the delivered deck v3_1_0 and the plans v3_1_0 and v3_2_0 stay byte-identical: SHA-256 before and after). Do the work of the stopped session SEN0401-I33-deck-ch05fix, whose uncommitted files in the working tree are a start you may read but must rebuild and prove yourself: (1) each of the six 'Everyday pictures' slides (15, 30, 40, 42, 51, 52 of the delivered deck) carries a takeaway strip written from the slide's own content; (2) the notes of the slides 13, 21 and 65 are cut to 2 to 4 sentences within 100 words with the same facts; (3) the summary slide stands immediately before the resources slide (the check yourself slide comes before the summary; no example slide moves, so the chapter-code manifest and its slide numbers hold; if one moves, a NEW manifest file records it); "
          "(4) the last slide stays LIGHT like the rest of the deck and the plan v3_3_0 declares it as it is (kind closing, bg light): do NOT make it dark and do NOT write bg dark for a light slide - the deck standard check D9 and the owner's rule forbid a switch, and a false declaration is forbidden; the arc check v1_3_0 will therefore print exactly ONE refusal, 'the last slide is not the dark closing slide', which is the recorded gate contradiction ex:CR3_GateArcDark and is carried, not hidden; "
          "(5) THE PLAN v3_3_0 KEEPS EVERY FIELD THAT THE OTHER CHECKS READ FROM THE NEWEST PLAN FILE (take the fields of deck_plan_v3_1_0.json - picture names, chart items, expressions, fact rows, link groups - and ADD the arc check's kinds, takeaway and analogy fields to them; do not drop any). Build with the deck engine and builders of the delivered deck (read them first). "
          "PROOF kept as logs, each written once after its run is complete: the arc check v1_3_0 on chapter 5 (exactly one refusal, rule 1, exit 1); deck standard check v1_1_0 (D1 to D12 all PASS, exit 0); deck overlap check; deck control check manifest:05; error-first scan; the Deck chapter check v1_4_0 on Deck/Ch05 exits 0 (EVERY part, including fixtures of every owner check refused and control accepted, run with the NEWEST plan in the folder); the same chapter check run on the delivered deck v3_1_0 with the plan v3_3_0 beside it; the changed slides rendered and read; nochange (every file of your commits added). "
          "DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES: write each log once, after its run is complete, and commit it once. A committed file is never edited: every output is a new file with a new version number. No gate, test or threshold is edited or worked around. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. Commit your work to main (pull --rebase before push).")
STS = [("ST_Ch05_DeckFix2", "The chapter 5 deck is accepted by every check but the contradicting arc rule, as a new deck and plan", ["AC9_Ch05DeckFix2"], ["TK_Ch05_DeckFix2_Build", "TK_Ch05_DeckFix2_Verify"], "SEN0401-I35-deck-ch05fix2", TXT_DK, "Run the arc check v1_3_0 (one refusal, rule 1), the deck standard check, overlap, manifest, error-first scan and the Deck chapter check v1_4_0 on the new deck; render and read the changed slides; nochange.", [], 1, 1, 4.0)]
ITER = ("Iter_35", "Iteration 35: the chapter 5 deck findings, second attempt (planned, not started)", "2026-11-07T12:00:00", "2026-11-08T12:00:00", "The chapter 5 deck is accepted by every check except the contradicting arc rule 1, which is carried.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_Ch05DeckFix2": ("The chapter 5 deck v3_2_0 meets every check except the one arc rule that contradicts D9, which is carried; the plan v3_3_0 breaks no check", base + "Given the chapter 5 deck v3_1_0 delivered (unchanged) and the plans v3_1_0 and v3_2_0 (unchanged), when a NEW deck version and a NEW plan are made, then ALL of: (1) the arc check v1_3_0 on chapter 5 prints exactly one refusal, 'the last slide is not the dark closing slide', and no other (the contradiction with D9 is the pending change request ex:CR3_GateArcDark; it is carried, not waived, and the last slide is not made dark); (2) the plan v3_3_0 declares every slide as the deck shows it (the last slide bg light) and keeps every field that the deck check, the picture check and the fixtures tool read; (3) deck standard check v1_1_0 (D1 to D12), overlap check, deck control check manifest, error-first scan and the Deck chapter check v1_4_0 (every part, with the newest plan) exit 0; (4) the delivered deck, the plans v3_1_0 and v3_2_0 and every committed file are unchanged (nochange); results as printed; if any element fails the deck is named failing. " + FACT, "ex:TS_ArcCheck13", "arc check v1_3_0; deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_4_0 (system python3, python-pptx)")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Second attempt at the chapter 5 deck findings, with the contradiction of the gates and the broken plan named"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the story into Iteration 35."))
    ia = ('\nex:IA3_Ch05DeckFix2 a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 5 deck repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new deck and a new plan file. NOT AFFECTED: the controlled criteria of the decks (they stay met), the delivered deck, the old plans, every committed file. ESTIMATE (G120): 4.0 h plus 1.0 h verification. The first attempt (ST_Ch05_DeckFix) is withdrawn: its executor stopped without committing because its criterion could not be met as written."))
    gd = ('\nex:CR3_GateArcDark a backlog:ChangeRequest ;\n    rdfs:label "Gate defect: the arc check rule 1 (dark closing slide) contradicts the deck standard element D9 (one background scheme)"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso %s ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " DECISION NEEDED FROM THE OWNER (his explicit word, because a gate is changed only on it): which rule gives way - the arc check accepts a light closing slide (a new arc check version), or the deck standard allows one dark closing slide (a new standard check version). Until he says, no gate is changed, the plans of chapters 4, 6, 8, 12, 13 and 14 keep their declaration (bg dark for a last slide that is light) as a recorded false declaration, and the lineage does not wait."))
    return X.set_status(t + cr + ia + gd, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the chapter 5 deck findings, second attempt of the lineage agent in register v0.404.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the second attempt at the chapter 5 deck findings); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the second attempt at the chapter 5 deck findings"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch05DeckFix2 ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the second attempt at the chapter 5 deck findings: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 5 deck made to meet the arc check v1_3_0, as a new deck and plan"
    tx = "New files: the chapter 5 deck v3_2_0 and the plan v3_3_0. " + FACT
    L = ('\nex:Del3_Ch05DeckFix2 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Ch05DeckFix2 ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the chapter 5 deck findings, second attempt). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR20", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the chapter 5 deck findings, second attempt: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR20", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Ch05DeckFix2 a backlog:Goal ;
    rdfs:label "The chapter 5 deck is accepted by the arc check"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR20 .
ex:G3_Ch05DeckFix2 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch05DeckFix2; the intent origin is therefore Derived."@en .
ex:Spec3I_Ch05DeckFix2 a backlog:Specification ;
    rdfs:label "What it is for the chapter 5 deck repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Ch05DeckFix2 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR20 .
ex:Spec3I_Ch05DeckFix2_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Ch05DeckFix2 ; backlog:hasScenarioText %s .
ex:Spec3I_Ch05DeckFix2_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Ch05DeckFix2 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR20", "Out3_ScopeR20"), "third lineage, Goal stage rebuilt for the chapter 5 deck findings, second attempt: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR20", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Ch05DeckFix2 a backlog:Objective ; rdfs:label "The deck repair met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Ch05DeckFix2 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Ch05DeckFix2 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Ch05DeckFix2 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR20 .
ex:Met3_Ch05DeckFix2 a backlog:Metric ; rdfs:label "chapter 5 deck repair whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Ch05DeckFix2 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "1"^^xsd:decimal .
ex:ObsR27_Ch05DeckFix22_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Ch05DeckFix2 ; backlog:observationFor ex:Obj3_Ch05DeckFix2 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Ch05DeckFix2 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch05DeckFix2; the intent origin is therefore Derived."@en .
''' % (lit("Count of the repair story (ST_Ch05_DeckFix2) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 5 deck attempt on 2026-10-25: the new deck does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR20", "Out3_GoalR20"), "third lineage, Objective stage rebuilt for the chapter 5 deck findings, second attempt: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR20", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR21"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch05DeckFix2 and the lineage agent in register v0.404.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Ch05DeckFix2").replace("ex:Data3S_TC9_", "ex:Data3S_TC9F_").replace("ex:TC9_", "ex:TC9F_"))
    L = [x.replace("ex:TC9_", "ex:TC9F_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Ch05DeckFix2", "Obj3_Ch05DeckFix2", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 35 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Ch05DeckFix2, ex:Spec3I_Ch05DeckFix2_Pass, ex:Spec3I_Ch05DeckFix2_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Ch05DeckFix2 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Ch05DeckFix2 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the second attempt at the chapter 5 deck findings"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch05DeckFix2 and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR22", "Out3_ObjectiveR20"), "third lineage, Backlog stage rebuilt: the chapter 5 deck repair admitted into the planned Iteration 35 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
