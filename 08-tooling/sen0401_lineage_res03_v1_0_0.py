#!/usr/bin/env python3
"""sen0401_lineage_res03 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the gap the control of the chapter 12 deck (v0.329.0) found (the research set of chapter 12 holds the concepts of chapter 11): a ChangeRequest ex:CR3_Ch12Research with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS two stories into the NEW Iteration 30 (planned, not started):
ST_Ch12_Research_R24 (research corrected as new files) and ST_Deck12_Revise (chapter 12 deck v3_0_0 without the borrowed part; its build depends on the research verification). Same route as sen0401_lineage_arcfix. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_Ch12Research"; REV = "ex:Revision_Lineage3_Scope14"
ACTIVE = ["ex:Out3_ScopeR14", "ex:Out3_GoalR14", "ex:Out3_ObjectiveR14", "ex:Out3_BacklogR16"]; NEWB = "ex:Out3_BacklogR17"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the executor of TK_Ch12_Deck_Build_R24 (commits 40fac1a, c9d1985) and confirmed by the lineage agent in the control (register v0.329.0): the 41 primary-source concepts of 03-materials/ch12/rdodi/sen0401_ch12_research_v1_0_1.ttl are identical by label to the 41 of the chapter 11 research (41 of 41); no other pair of chapters overlaps (scan of chapters 1 to 14). "
        "The deck standard check reads these concepts for D4 and D11, so the chapter 12 deck v2_0_0 shows eight slides titled From chapter 11 (slides 43 to 50) that teach none of chapter 12 and cover only 39 real chapter 12 concepts; the criterion AC9_Deck_Ch12 names the checks and is MET, the defect is a gap of the research set, not of that criterion.")
TXT_RES = ("Correct the research set of chapter 12 as NEW files (the research files of 03-materials/ch12/rdodi stay unchanged; new versions above the newest): the primary-source concepts are those of chapter 12 (Mining and Consensus), read from the chapter text and the saved sources, each with a label, a comment in a complete sentence and a citation, none taken from the chapter 11 research; the other parts of the research (publications, findings, stories, scorecard) are kept unless a statement is wrong, and every change is listed in a version note. "
           "After the repair: the Research chapter check v1_3_0 for Research/Ch12 exits 0; the Stage 4 gate runner v1_1_0 for 12 exits 0 (NOT_MEASURED items listed as such, not as passes); the chapter 12 verify script, if one exists, is not edited and a new version is made only where its checks need the new file; no concept equals a concept of the chapter 11 research by label unless chapter 12 itself teaches it (list the shared ones with the reason); HermiT consistent. " + R.NOEDIT + " " + R.COMMON)
TXT_DECK = ("Make the chapter 12 deck v3_0_0 as a NEW deck version (a new .pptx above v2_0_0 in 03-materials/ch12, and a new manifest version only if the examples change) that teaches the CORRECTED chapter 12 concepts and carries no part From chapter 11: every key concept of the corrected research is shown with an everyday analogy (D4, D11 at 100 percent), the eight borrowed slides are gone, the arc of the deck stays the standard's. Everything the deck v2_0_0 was controlled on stays met: deck standard check v1_1_0 12/0/0, overlap check, deck control check manifest, error-first scan, Deck chapter check v1_3_0 (examples re-run) all exit 0; the notes stay short reader's prose; the arc check v1_2_0 with SEN0401_DECK set to the new deck is run and its refusals listed. "
            "The delivered deck v2_0_0 stays unchanged. " + R.NOEDIT + " " + R.COMMON)
STS = [("ST_Ch12_Research_R24", "The research set of chapter 12 holds the concepts of chapter 12, as new files", ["AC9_Ch12Research"], ["TK_Ch12_Research_Build_R24", "TK_Ch12_Research_Verify_R24"], "SEN0401-I30-research-ch12", TXT_RES, "Run, as printed: the Research chapter check v1_3_0 for Research/Ch12 (venv314), the Stage 4 gate runner v1_1_0 for 12, my own concept scan against chapter 11 and every other chapter, HermiT, nochange; read the new concepts against the chapter text.", [], 25, 1, 3.0),
       ("ST_Deck12_Revise", "The chapter 12 deck teaches the corrected concepts and carries no borrowed part, as a new deck version", ["AC9_Ch12DeckRevise"], ["TK_Deck12_Revise_Build", "TK_Deck12_Revise_Verify"], "SEN0401-I30-deck-ch12-revise", TXT_DECK, "Run the five deck checks and the arc check on the new deck; render and read every slide; links; nochange.", ["TK_Ch12_Research_Verify_R24"], 1, 1, 2.5)]
ITER = ("Iter_30", "Iteration 30: the repair of the chapter 12 research set and the chapter 12 deck revision (planned, not started)", "2026-11-02T12:00:00", "2026-11-03T12:00:00", "The research set of chapter 12 holds the concepts of chapter 12 and the chapter 12 deck teaches them without a borrowed part.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_Ch12Research": ("The research set of chapter 12 holds the concepts of chapter 12 and passes the research checks, as new files", base + "Given the chapter 12 research v1_0_1 (unchanged), when the research is corrected as new files, then ALL of: (1) the primary-source concepts are those of chapter 12 and none equals a chapter 11 concept by label without a stated reason (the lineage agent's own scan against every other chapter); (2) the Research chapter check for Research/Ch12 exits 0; (3) the Stage 4 gate runner for 12 exits 0 and lists its NOT_MEASURED items as such; (4) HermiT is consistent; (5) no committed file is edited; results as printed; if any element fails the research is named failing. " + FACT,
                                "ex:TS_ResearchCheck, ex:TS_ChapterCheck, ex:TS_Stage4Gates, ex:TS_RdodiValidatorCurrent, ex:TS_RdodiValidatorPinned", "Research chapter check v1_3_0 (venv314) reading the PINNED RDODI validator v1.6.0; Stage 4 gate runner v1_1_0 reading the CURRENT validator; own concept scan"),
            "AC9_Ch12DeckRevise": ("The chapter 12 deck teaches the corrected concepts without a borrowed part and stays met on its earlier checks", base + "Given the corrected research of chapter 12 and the deck v2_0_0 (unchanged), when a NEW deck version is made, then ALL of: (1) deck standard check v1_1_0 12/0/0 reading the corrected research, with no slide titled From chapter 11; (2) overlap check, deck control check manifest, error-first scan and Deck chapter check v1_3_0 exit 0; (3) the arc check v1_2_0 on the new deck is run and its refusals are listed; (4) no committed file is edited; results as printed. " + FACT,
                                    "ex:TS_DeckStdCheck11, ex:TS_DeckOverlapCheck, ex:TS_ChapterCheck", "deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_3_0 (system python3, python-pptx); arc check v1_2_0")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the chapter 12 research set (it holds the concepts of chapter 11) and the chapter 12 deck revision without the borrowed part"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_ArcFindings, ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the two stories into Iteration 30."))
    ia = ('\nex:IA3_Ch12Research a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 12 research repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: new research files of chapter 12 (new versions, the old stay) and a new chapter 12 deck version (v3_0_0) with its manifest if the examples change. NOT AFFECTED: the chapter 12 deck criterion AC9_Deck_Ch12 (it stays met), the research of the other chapters (scan: no other overlap), every committed file. ESTIMATE (G120): 3.0 h research, 2.5 h deck, each plus verification. The deck revision depends on the research repair."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the chapter 12 research gap of the control of v0.329.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the chapter 12 research set and the deck revision); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the chapter 12 research set and the deck revision"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch12Research ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the chapter 12 research set and the deck revision: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The research set of chapter 12 corrected and the chapter 12 deck revised without the borrowed part, each as new files"
    tx = "New research files of chapter 12 holding the concepts of chapter 12; a new chapter 12 deck version that teaches them. " + FACT
    L = ('\nex:Del3_Res12 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Res12 ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the chapter 12 research gap). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR15", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the chapter 12 research gap: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR15", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Res12 a backlog:Goal ;
    rdfs:label "The chapter 12 research set holds the concepts of chapter 12 and the deck teaches them"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR15 .
ex:G3_Res12 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch12Research; the intent origin is therefore Derived."@en .
ex:Spec3I_Res12 a backlog:Specification ;
    rdfs:label "What it is for the chapter 12 research repair and deck revision to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Res12 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR15 .
ex:Spec3I_Res12_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Res12 ; backlog:hasScenarioText %s .
ex:Spec3I_Res12_Fail a backlog:TestScenario ; rdfs:label "A repair that keeps the borrowed concepts, hides them in the deck, or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Res12 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new research files or the new deck version, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given research that keeps a chapter 11 concept without reason, or a deck that keeps the borrowed part, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR15", "Out3_ScopeR15"), "third lineage, Goal stage rebuilt for the chapter 12 research gap: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR15", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Res12 a backlog:Objective ; rdfs:label "The two repairs met on verified evidence: from 0 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Res12 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Res12 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Res12 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR15 .
ex:Met3_Res12 a backlog:Metric ; rdfs:label "chapter 12 repairs (research set, deck revision) whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Res12 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the two repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the two criteria." ; backlog:expectedValue "2"^^xsd:decimal .
ex:ObsR24_Res12_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Res12 ; backlog:observationFor ex:Obj3_Res12 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Res12 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_Ch12Research; the intent origin is therefore Derived."@en .
''' % (lit("Count of the two repair stories (ST_Ch12_Research_R24, ST_Deck12_Revise) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 12 deck on 2026-10-25 (v0.329.0): neither repair exists, so 0 of 2."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR15", "Out3_GoalR15"), "third lineage, Objective stage rebuilt for the chapter 12 research gap: one objective (0 to 4) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR15", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR16"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch12Research and the control of v0.329.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Res12").replace("ex:Data3S_TC9_", "ex:Data3S_TC9C_").replace("ex:TC9_", "ex:TC9C_"))
    L = [x.replace("ex:TC9_", "ex:TC9C_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Res12", "Obj3_Res12", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3R_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 30 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Res12, ex:Spec3I_Res12_Pass, ex:Spec3I_Res12_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Res12 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Res12 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the chapter 12 research set and the deck revision"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by two stories; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Res12 and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR17", "Out3_ObjectiveR15"), "third lineage, Backlog stage rebuilt: the four arc-check repairs admitted into the planned Iteration 29 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
