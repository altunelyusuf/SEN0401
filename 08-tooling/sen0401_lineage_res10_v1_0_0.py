#!/usr/bin/env python3
"""sen0401_lineage_res10 v1_0_0 - change route for the gap the story check v1_0_0 found on the decks of chapters 10, 12 and 14 (the host of a story's READ link is on no slide). A ChangeRequest ex:CR3_StoryLink with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS three stories into the NEW Iteration 36 (planned, not started). Same route as sen0401_lineage_res09. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_StoryLink"; REV = "ex:Revision_Lineage3_Scope20"
ACTIVE = ["ex:Out3_ScopeR20", "ex:Out3_GoalR20", "ex:Out3_ObjectiveR20", "ex:Out3_BacklogR22"]; NEWB = "ex:Out3_BacklogR23"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the lineage agent (register v0.417.0, running the story check v1_0_0 on the decks of all fourteen chapters while controlling the chapter 10 deck): the story check refuses three delivered decks because the host of a story's READ link is on no slide, so the live further-reading link is not visible on the material itself (the owner's rule for stories: a live further-reading link on the material itself): "
        "chapter 10, story BloomFiltersLeak, host eprint.iacr.org; chapter 12, story HashcashBeforeBitcoin, host web.archive.org; chapter 14, story SpillmanChannels, host web.archive.org. The story check is not an element of the criteria these decks were controlled on, so those controls stay met; the finding is carried, not hidden. Chapter 1 shows a different refusal (StoneMoney: no slide carries the date and the picture credit together), which its retrofit story already covers.")
def txt(nn, deck, story, host):
    return ("Make a NEW deck of chapter %s (the next version above the newest, %s, which stays byte-identical: SHA-256 before and after) and a NEW plan file above the newest plan of 08-tooling/ch%s-deck, in which the story %s shows the host of its READ link (%s) on its story slide, in the story's link bar, as visible text beside the live link (read the story check's rule first: python3 -B 08-tooling/sen0401_story_check_v1_0_0.py %s). Nothing else of the content, the examples, the charts, the pictures and the notes changes; no slide is added, removed or moved, so the chapter-code manifest and its slide numbers hold. "
            "THE NEW PLAN KEEPS EVERY FIELD OF THE NEWEST PLAN (copy it and change only the story slide): the deck check, the picture check, the arc check and the fixtures tool read the NEWEST plan file, and a plan that drops a field breaks the Deck chapter check (it happened with the chapter 5 plan v3_2_0). PROOF kept as logs, each written once after its run is complete: the story check v1_0_0 on chapter %s prints no refusal for this story; the arc check v1_3_0 on chapter %s exits 0 as it did before; deck standard check v1_1_0 (D1 to D12), deck overlap check, deck control check manifest:%s, error-first scan, and the Deck chapter check v1_4_0 on Deck/Ch%s (every part, with the newest plan) exit 0; the changed slide rendered and read; nochange (every file of your commits added). "
            "DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES: write each log once, after its run is complete, and commit it once. A committed file is never edited: every output is a new file with a new version number. No gate, test or threshold is edited. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. Commit your work to main (pull --rebase before push)." % (nn, deck, nn, story, host, nn, nn, nn, nn, nn))
VT = "Run the story check v1_0_0, the arc check v1_3_0, the deck standard check, overlap, manifest, error-first scan and the Deck chapter check v1_4_0 on the new deck; render and read the changed slide; nochange."
STS = [("ST_Deck10_StoryLink", "The chapter 10 deck shows the host of every story's READ link on a slide, as a new deck version", ["AC9_StoryLink_Ch10"], ["TK_Deck10_StoryLink_Build", "TK_Deck10_StoryLink_Verify"], "SEN0401-I36-deck-ch10link", txt("10", "03-materials/ch10/SEN0401_Ch10_TheBitcoinNetwork_3e_v2_1_0.pptx", "BloomFiltersLeak", "eprint.iacr.org"), VT, [], 1, 1, 2.0),
       ("ST_Deck12_StoryLink", "The chapter 12 deck shows the host of every story's READ link on a slide, as a new deck version", ["AC9_StoryLink_Ch12"], ["TK_Deck12_StoryLink_Build", "TK_Deck12_StoryLink_Verify"], "SEN0401-I36-deck-ch12link", txt("12", "03-materials/ch12/SEN0401_Ch12_MiningAndConsensus_3e_v3_0_1.pptx", "HashcashBeforeBitcoin", "web.archive.org"), VT, [], 1, 1, 2.0),
       ("ST_Deck14_StoryLink", "The chapter 14 deck shows the host of every story's READ link on a slide, as a new deck version", ["AC9_StoryLink_Ch14"], ["TK_Deck14_StoryLink_Build", "TK_Deck14_StoryLink_Verify"], "SEN0401-I36-deck-ch14link", txt("14", "03-materials/ch14/SEN0401_Ch14_SecondLayerApplications_3e_v2_0_0.pptx", "SpillmanChannels", "web.archive.org"), VT, [], 1, 1, 2.0)]
ITER = ("Iter_36", "Iteration 36: the READ-link hosts on the story slides of the decks of chapters 10, 12 and 14 (planned, not started)", "2026-11-08T12:00:00", "2026-11-09T12:00:00", "The story check refuses no story of the decks of chapters 10, 12 and 14.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    out = {}
    for nn, deck in (("10", "v2_1_0"), ("12", "v3_0_1"), ("14", "v2_0_0")):
        out["AC9_StoryLink_Ch" + nn] = ("The chapter %s deck is accepted by the story check v1_0_0 as a new version and stays met on its earlier checks" % nn, base + "Given the chapter %s deck %s delivered (unchanged), when a NEW deck version and a NEW plan are made, then ALL of: (1) the story check v1_0_0 on chapter %s prints no refusal; (2) the arc check v1_3_0 still exits 0 and the deck standard check v1_1_0, overlap check, deck control check manifest, error-first scan and Deck chapter check v1_4_0 (every part, with the newest plan) exit 0; (3) the delivered deck and every committed file are unchanged (nochange); results as printed; if any element fails the deck is named failing. " % (nn, deck, nn) + FACT, "ex:TS_ArcCheck13, ex:TS_ChapterCheck, ex:TS_DeckStdCheck11", "story check v1_0_0; arc check v1_3_0; deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_4_0 (system python3, python-pptx)")
    return out
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The READ-link hosts missing on the story slides of the decks of chapters 10, 12 and 14"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the three stories into Iteration 36."))
    ia = ('\nex:IA3_StoryLink a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 5 deck repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new deck and a new plan file. NOT AFFECTED: the controlled criteria of the decks (they stay met), the delivered deck, the old plans, every committed file. ESTIMATE (G120): 4.0 h plus 1.0 h verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the story-link findings of the decks of chapters 10, 12 and 14 of the lineage agent in register v0.417.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the story-link findings); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the story-link findings"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_StoryLink ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the story-link findings: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 5 deck made to meet the arc check v1_3_0, as a new deck and plan"
    tx = "New files: the chapter 5 deck v3_2_0 and the plan v3_3_0. " + FACT
    L = ('\nex:Del3_StoryLink a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_StoryLink ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the story-link findings of the decks of chapters 10, 12 and 14). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR21", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the story-link findings of the decks of chapters 10, 12 and 14: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR21", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_StoryLink a backlog:Goal ;
    rdfs:label "The chapter 5 deck is accepted by the arc check"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR21 .
ex:G3_StoryLink rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_StoryLink; the intent origin is therefore Derived."@en .
ex:Spec3I_StoryLink a backlog:Specification ;
    rdfs:label "What it is for the chapter 5 deck repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_StoryLink ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR21 .
ex:Spec3I_StoryLink_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_StoryLink ; backlog:hasScenarioText %s .
ex:Spec3I_StoryLink_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_StoryLink ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR21", "Out3_ScopeR21"), "third lineage, Goal stage rebuilt for the story-link findings of the decks of chapters 10, 12 and 14: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR21", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_StoryLink a backlog:Objective ; rdfs:label "The story-link repairs met on verified evidence: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_StoryLink ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_StoryLink ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_StoryLink ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR21 .
ex:Met3_StoryLink a backlog:Metric ; rdfs:label "chapter 5 deck repair whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_StoryLink a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "3"^^xsd:decimal .
ex:ObsR28_StoryLink_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_StoryLink ; backlog:observationFor ex:Obj3_StoryLink ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_StoryLink rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_StoryLink; the intent origin is therefore Derived."@en .
''' % (lit("Count of the story-link stories (ST_Deck10_StoryLink, ST_Deck12_StoryLink, ST_Deck14_StoryLink) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 5 deck attempt on 2026-10-25: the new deck does not exist, so 0 of 3."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR21", "Out3_GoalR21"), "third lineage, Objective stage rebuilt for the story-link findings of the decks of chapters 10, 12 and 14: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR21", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR22"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_StoryLink and the lineage agent in register v0.417.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_StoryLink").replace("ex:Data3S_TC9_", "ex:Data3S_TC9H_").replace("ex:TC9_", "ex:TC9H_"))
    L = [x.replace("ex:TC9_", "ex:TC9H_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_StoryLink", "Obj3_StoryLink", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 36 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_StoryLink, ex:Spec3I_StoryLink_Pass, ex:Spec3I_StoryLink_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_StoryLink backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_StoryLink a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the story-link findings"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_StoryLink and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR23", "Out3_ObjectiveR21"), "third lineage, Backlog stage rebuilt: the chapter 5 deck repair admitted into the planned Iteration 36 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
