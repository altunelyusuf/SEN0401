#!/usr/bin/env python3
"""sen0401_lineage_res04 v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the gaps the control of the arc check v1_3_0 (v0.343.0) found (the chapter 5 plan schema, the notes of the decks of chapters 12 and 13): a ChangeRequest ex:CR3_ArcFindings2 with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS two stories into the NEW Iteration 31 (planned, not started):
ST_Ch05_ArcPlan, ST_Deck13_ArcFix, ST_Deck12_ArcFix (the last depends on ST_Deck12_Revise). Same route as sen0401_lineage_res03. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_ArcFindings2"; REV = "ex:Revision_Lineage3_Scope15"
ACTIVE = ["ex:Out3_ScopeR15", "ex:Out3_GoalR15", "ex:Out3_ObjectiveR15", "ex:Out3_BacklogR17"]; NEWB = "ex:Out3_BacklogR18"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the executor of TK_ArcLookup_Build (commits 663e649, 0ec94c4) and confirmed by the lineage agent in the control (register v0.343.0): the arc check v1_3_0 on the delivered decks shows (a) chapter 5: 82 refusals because its plan file 08-tooling/ch05-deck/deck_plan_v3_1_0.json is in the remedy schema (slides without the kinds title, closing and section that the arc check reads), a plan-schema finding and not a finding about the deck; "
        "(b) chapter 13 deck v2_0_0: one notes refusal (notes of 5 sentences against the rule of 2 to 4); (c) chapter 12 deck v2_0_0: one notes refusal of the same kind. The decks of chapters 1, 7 and 10 are planned in Iteration 29 (ex:CR3_ArcFindings). None of these is an element of the criteria the decks were controlled on, so those stay met.")
TXT_PLAN = ("Make a NEW plan file for chapter 5 in the schema that the arc check reads, as 08-tooling/ch05-deck/deck_plan_v3_2_0.json (a new file above deck_plan_v3_1_0.json, which stays unchanged), derived from the delivered deck 03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_1_0.pptx and the existing plan: the same slides in the same order with the kinds title, section, content, closing, the takeaway and analogy fields and the fact rows and link groups that the arc check reads; "
            "the deck itself is NOT edited and not rebuilt. PROOF kept as logs: the arc check v1_3_0 run on chapter 5 after the new plan (its refusals listed, each with the rule that gives it; refusals that name the deck are findings about the deck and are carried, not hidden), the plan file's slide count equals the deck's, a written mapping from the old plan fields to the new ones, nochange. " + R.NOEDIT + " " + R.COMMON)
def txt_notes(nn, extra): return ("Make the arc check v1_3_0 pass on the chapter %d deck as a NEW deck version (a new .pptx above the newest in 03-materials/ch%s, and a new manifest version only if the examples change); the delivered deck stays unchanged. Repair: the speaker notes of every slide that the arc check lists are shortened to 2 to 4 sentences, at most 100 words, without losing their point%s. "
                                % (int(nn), nn, extra)) + "Everything the deck was controlled on stays met: deck standard check v1_1_0 12/0/0, overlap check, deck control check manifest, error-first scan, Deck chapter check v1_3_0 (examples re-run) all exit 0. PROOF kept as logs: arc check v1_3_0 with SEN0401_DECK set to the new deck exits 0; the five checks; nochange (every file added). " + R.NOEDIT + " " + R.COMMON
STS = [("ST_Ch05_ArcPlan", "The chapter 5 plan file is in the schema the arc check reads, as a new file", ["AC9_Ch05ArcPlan"], ["TK_Ch05_ArcPlan_Build", "TK_Ch05_ArcPlan_Verify"], "SEN0401-I31-arcplan-ch05", TXT_PLAN, "Run the arc check v1_3_0 on chapter 5; compare the new plan's slide order and count with the delivered deck read from the file; list every remaining refusal with its rule; nochange.", [], 1, 0.5, 2.0),
       ("ST_Deck13_ArcFix", "The chapter 13 deck is accepted by the arc check, as a new deck version", ["AC9_ArcFix_Ch13"], ["TK_Deck13_ArcFix_Build", "TK_Deck13_ArcFix_Verify"], "SEN0401-I31-deck-ch13-arcfix", txt_notes("13", ""), "Run arc check v1_3_0 on the new deck and the five deck checks; render and read the changed slides.", [], 1, 0.5, 1.5),
       ("ST_Deck12_ArcFix", "The revised chapter 12 deck is accepted by the arc check, as a new deck version", ["AC9_ArcFix_Ch12"], ["TK_Deck12_ArcFix_Build", "TK_Deck12_ArcFix_Verify"], "SEN0401-I31-deck-ch12-arcfix", txt_notes("12", " (it is made on the deck v3_0_0 of ST_Deck12_Revise, the newest in 03-materials/ch12 once that story is Done; if the revision has not finished this task is not started)"), "Run arc check v1_3_0 on the new deck and the five deck checks; render and read the changed slides.", ["TK_Deck12_Revise_Verify"], 1, 0.5, 1.5)]
ITER = ("Iter_31", "Iteration 31: the chapter 5 plan schema and the notes of the decks of chapters 12 and 13 (planned, not started)", "2026-11-03T12:00:00", "2026-11-04T12:00:00", "The arc check can read chapter 5 and the decks of chapters 12 and 13 are accepted by it.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    deck = lambda nn: ("The chapter %d deck is accepted by the arc check v1_3_0 as a new version and stays met on its earlier checks" % int(nn), base + "Given the chapter %d deck delivered (unchanged), when a NEW deck version is made, then ALL of: (1) arc check v1_3_0 on the new deck exits 0; (2) deck standard check v1_1_0, overlap check, deck control check manifest, error-first scan and Deck chapter check v1_3_0 exit 0; (3) the delivered deck and every committed file are unchanged (nochange); results as printed; if any element fails the deck is named failing. " % int(nn) + FACT,
                       "ex:TS_ArcCheck13, ex:TS_DeckStdCheck11, ex:TS_DeckOverlapCheck, ex:TS_ChapterCheck", "arc check v1_3_0; deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_3_0 (system python3, python-pptx)")
    return {"AC9_Ch05ArcPlan": ("The arc check v1_3_0 reads the chapter 5 plan in its schema and every remaining refusal is a stated rule", base + "Given the plan file deck_plan_v3_1_0.json (unchanged) and the delivered chapter 5 deck, when a NEW plan file deck_plan_v3_2_0.json is made, then ALL of: (1) the plan has as many slides as the deck file and in the same order; (2) the arc check v1_3_0 on chapter 5 refuses nothing for a missing kind or section, and every refusal that remains is listed with its rule; (3) the deck, the old plan and every committed file are unchanged (nochange); results as printed. " + FACT, "ex:TS_ArcCheck13", "arc check v1_3_0 (python-pptx)"),
            "AC9_ArcFix_Ch13": deck("13"), "AC9_ArcFix_Ch12": deck("12")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the arc-check findings of v1_3_0: the chapter 5 plan schema and the notes of the decks of chapters 12 and 13"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_ArcFindings, ex:CR3_ArcCheck, ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the three stories into Iteration 31."))
    ia = ('\nex:IA3_ArcFindings2 a backlog:ImpactAssessment ;\n    rdfs:label "What the arc-check findings of v1_3_0 cost to repair and what they touch"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: one new plan file (chapter 5) and two new deck versions (chapters 12 and 13; the chapter 12 one after the revision v3_0_0). NOT AFFECTED: the controlled criteria of the decks (they stay met), the arc check v1_3_0, every committed file. ESTIMATE (G120): 2.0 h plan, 1.5 h and 1.5 h decks, each plus verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the arc-check findings of v1_3_0 of the control of v0.343.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the arc-check findings of v1_3_0); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the arc-check findings of v1_3_0"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_ArcFindings2 ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the arc-check findings of v1_3_0: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 5 plan file in the arc check schema and the decks of chapters 12 and 13 accepted by the arc check, each as new files"
    tx = "A new chapter 5 plan file; new deck versions for chapters 12 and 13. " + FACT
    L = ('\nex:Del3_Arc2 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Arc2 ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the arc-check findings of v1_3_0). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR16", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the arc-check findings of v1_3_0: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR16", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Arc2 a backlog:Goal ;
    rdfs:label "The arc check reads chapter 5 and the decks of chapters 12 and 13 are accepted by it"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR16 .
ex:G3_Arc2 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_ArcFindings2; the intent origin is therefore Derived."@en .
ex:Spec3I_Arc2 a backlog:Specification ;
    rdfs:label "What it is for the arc-check findings repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Arc2 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR16 .
ex:Spec3I_Arc2_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Arc2 ; backlog:hasScenarioText %s .
ex:Spec3I_Arc2_Fail a backlog:TestScenario ; rdfs:label "A repair that hides a refusal, drops a note\'s point, or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Arc2 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new plan file or the new deck version, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a plan file that hides a refusal, or a deck whose notes lose their point, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR16", "Out3_ScopeR16"), "third lineage, Goal stage rebuilt for the arc-check findings of v1_3_0: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR16", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Arc2 a backlog:Objective ; rdfs:label "The three repairs met on verified evidence: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Arc2 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Arc2 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Arc2 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR16 .
ex:Met3_Arc2 a backlog:Metric ; rdfs:label "arc-check repairs (chapter 5 plan, decks of chapters 12 and 13) whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Arc2 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the three repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the three criteria." ; backlog:expectedValue "3"^^xsd:decimal .
ex:ObsR24_Arc2_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Arc2 ; backlog:observationFor ex:Obj3_Arc2 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Arc2 rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_ArcFindings2; the intent origin is therefore Derived."@en .
''' % (lit("Count of the three repair stories (ST_Ch05_ArcPlan, ST_Deck13_ArcFix, ST_Deck12_ArcFix) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the arc check v1_3_0 on 2026-10-25 (v0.343.0): none of the three repairs exists, so 0 of 3."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR16", "Out3_GoalR16"), "third lineage, Objective stage rebuilt for the arc-check findings of v1_3_0: one objective (0 to 4) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR16", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR17"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_ArcFindings2 and the control of v0.343.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Arc2").replace("ex:Data3S_TC9_", "ex:Data3S_TC9D_").replace("ex:TC9_", "ex:TC9D_"))
    L = [x.replace("ex:TC9_", "ex:TC9D_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Arc2", "Obj3_Arc2", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3B_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 31 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Arc2, ex:Spec3I_Arc2_Pass, ex:Spec3I_Arc2_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Arc2 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Arc2 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the arc-check findings of v1_3_0"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by three stories; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Arc2 and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR18", "Out3_ObjectiveR16"), "third lineage, Backlog stage rebuilt: the four arc-check repairs admitted into the planned Iteration 29 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
