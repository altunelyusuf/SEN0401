#!/usr/bin/env python3
"""sen0401_lineage_res06 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the ten arc-check findings about the delivered chapter 5 deck (found with the new plan file, control of v0.383.0). A ChangeRequest ex:CR3_Ch05DeckFix with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS one story, ST_Ch05_DeckFix, into the NEW Iteration 33 (planned, not started). Same route as sen0401_lineage_res05. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_Ch05DeckFix"; REV = "ex:Revision_Lineage3_Scope17"
ACTIVE = ["ex:Out3_ScopeR17", "ex:Out3_GoalR17", "ex:Out3_ObjectiveR17", "ex:Out3_BacklogR19"]; NEWB = "ex:Out3_BacklogR20"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the executor of TK_Ch05_ArcPlan_Build (commits 635eed8, 67e8fc6) and confirmed by the lineage agent in the control of the plan (register v0.383.0): with the new plan file 08-tooling/ch05-deck/deck_plan_v3_2_0.json (68 slides, as many as the delivered deck v3_1_0, same order) the arc check v1_3_0 on chapter 5 prints 10 refusals, 0 warnings, exit 1, and no longer refuses a missing kind or section. The 10 refusals are findings about the delivered deck: "
        "(1) the last slide 68 is light (FAF6EF), not the dark closing slide; (2) the agenda range that starts at slide 65 does not start at a section slide (sections 7, 12, 19, 31, 43, 53, 57; slide 65 is the summary, 66 the check, 67 the resources); (3) six slides titled 'Everyday pictures' (15, 30, 40, 42, 51, 52) have no takeaway strip; (4) slide 66 'Check yourself' is not a summary slide; (5) the notes of slides 13, 21 and 65 are outside the limit of 2 to 4 sentences and 100 words (5, 5 and 6 sentences). "
        "None of these is an element of the criteria the chapter 5 deck was controlled on, so that control stays met; the findings are carried openly, not waived.")
TXT_DK = ("Make a NEW deck 03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_2_0.pptx and a NEW plan 08-tooling/ch05-deck/deck_plan_v3_3_0.json (the delivered deck v3_1_0 and the plans v3_1_0 and v3_2_0 stay byte-identical: SHA-256 before and after) that remove the ten refusals of the arc check v1_3_0 for the reasons it gives: (1) the last slide is the dark closing slide; (2) the summary slide comes before the check and the resources slide and the agenda range at the end starts at a section slide (the sections and the order of the content slides are otherwise as delivered); "
          "(3) each of the six 'Everyday pictures' slides (15, 30, 40, 42, 51, 52 of the delivered deck) carries a takeaway strip, written from the slide's own content; (4) the notes of slides 13, 21 and 65 are cut to 2 to 4 sentences within 100 words with the same facts. Nothing else of the content, the examples, the charts, the pictures and the story slides changes; the chapter-code manifest is unchanged in its examples and keeps its slide numbers if no example slide moves (if one moves, a NEW manifest file records the new numbers). Build with the deck engine and builder of the delivered deck (read them first). "
          "PROOF kept as logs: the arc check v1_3_0 on chapter 5 exits 0 with no refusal; deck standard check v1_1_0 (D1 to D12), deck overlap check v1_0_0, deck control check manifest:05, error-first scan, Deck chapter check v1_4_0 all exit 0; the slides changed are rendered and read; nochange (every file of your commits added). DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES: write each log once, after its run is complete, and commit it once. A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass.")
STS = [("ST_Ch05_DeckFix", "The chapter 5 deck is accepted by the arc check v1_3_0, as a new deck version", ["AC9_Ch05DeckFix"], ["TK_Ch05_DeckFix_Build", "TK_Ch05_DeckFix_Verify"], "SEN0401-I33-deck-ch05fix", TXT_DK, "Run the arc check v1_3_0 on the new deck and the five deck checks; render and read the changed slides; nochange.", [], 1, 1, 4.0)]
ITER = ("Iter_33", "Iteration 33: the arc-check findings of the chapter 5 deck (planned, not started)", "2026-11-05T12:00:00", "2026-11-06T12:00:00", "The chapter 5 deck is accepted by the arc check v1_3_0.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_Ch05DeckFix": ("The chapter 5 deck is accepted by the arc check v1_3_0 as a new version and stays met on its earlier checks", base + "Given the chapter 5 deck v3_1_0 delivered (unchanged) and the plan v3_2_0, when a NEW deck version and a NEW plan are made, then ALL of: (1) the arc check v1_3_0 on chapter 5 exits 0 with no refusal; (2) deck standard check v1_1_0, overlap check, deck control check manifest, error-first scan and Deck chapter check v1_4_0 exit 0; (3) the delivered deck, the plans v3_1_0 and v3_2_0 and every committed file are unchanged (nochange); results as printed; if any element fails the deck is named failing. " + FACT, "ex:TS_ArcCheck13", "arc check v1_3_0; deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_4_0 (system python3, python-pptx)")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the ten arc-check findings about the chapter 5 deck, as a new deck version and plan"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the story into Iteration 33."))
    ia = ('\nex:IA3_Ch05DeckFix a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 5 deck repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new deck and a new plan file. NOT AFFECTED: the controlled criteria of the decks (they stay met), the delivered deck, the old plans, every committed file. ESTIMATE (G120): 4.0 h plus 1.0 h verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the arc-check findings about the chapter 5 deck of the control of the plan (v0.383.0)."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the arc-check findings about the chapter 5 deck); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the arc-check findings about the chapter 5 deck"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch05DeckFix ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the arc-check findings about the chapter 5 deck: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 5 deck made to meet the arc check v1_3_0, as a new deck and plan"
    tx = "New files: the chapter 5 deck v3_2_0 and the plan v3_3_0. " + FACT
    L = ('\nex:Del3_Ch05DeckFix a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Ch05DeckFix ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the arc-check findings about the chapter 5 deck). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR18", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the arc-check findings about the chapter 5 deck: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR18", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Ch05DeckFix a backlog:Goal ;
    rdfs:label "The chapter 5 deck is accepted by the arc check"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR18 .
ex:G3_Ch05DeckFix rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch05DeckFix; the intent origin is therefore Derived."@en .
ex:Spec3I_Ch05DeckFix a backlog:Specification ;
    rdfs:label "What it is for the chapter 5 deck repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Ch05DeckFix ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR18 .
ex:Spec3I_Ch05DeckFix_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Ch05DeckFix ; backlog:hasScenarioText %s .
ex:Spec3I_Ch05DeckFix_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Ch05DeckFix ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR18", "Out3_ScopeR18"), "third lineage, Goal stage rebuilt for the arc-check findings about the chapter 5 deck: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR18", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Ch05DeckFix a backlog:Objective ; rdfs:label "The deck repair met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Ch05DeckFix ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Ch05DeckFix ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "1"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Ch05DeckFix ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR18 .
ex:Met3_Ch05DeckFix a backlog:Metric ; rdfs:label "chapter 5 deck repair whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Ch05DeckFix a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "1"^^xsd:decimal .
ex:ObsR25_Ch05DeckFix_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Ch05DeckFix ; backlog:observationFor ex:Obj3_Ch05DeckFix ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Ch05DeckFix rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch05DeckFix; the intent origin is therefore Derived."@en .
''' % (lit("Count of the repair story (ST_Ch05_DeckFix) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 5 plan on 2026-10-25: the new deck does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR18", "Out3_GoalR18"), "third lineage, Objective stage rebuilt for the arc-check findings about the chapter 5 deck: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR18", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR19"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch05DeckFix and the control of the plan (v0.383.0)."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Ch05DeckFix").replace("ex:Data3S_TC9_", "ex:Data3S_TC9F_").replace("ex:TC9_", "ex:TC9F_"))
    L = [x.replace("ex:TC9_", "ex:TC9F_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Ch05DeckFix", "Obj3_Ch05DeckFix", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 33 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Ch05DeckFix, ex:Spec3I_Ch05DeckFix_Pass, ex:Spec3I_Ch05DeckFix_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Ch05DeckFix backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Ch05DeckFix a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the arc-check findings about the chapter 5 deck"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch05DeckFix and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR20", "Out3_ObjectiveR18"), "third lineage, Backlog stage rebuilt: the chapter 5 deck repair admitted into the planned Iteration 33 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
