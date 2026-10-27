#!/usr/bin/env python3
"""sen0401_lineage_res15 v1_0_0 - change route for the chapter 13 deck gaps found in the control of v2_2_0: the chart of slide 21 has no data labels (deck check v1_1_0 REFUSED) and slide 24 says a cut message its code no longer prints. A ChangeRequest ex:CR3_Ch13Chart, then a StageRevision from the Scope stage that ADMITS ST_Deck13_Charts into the NEW Iteration 41 (planned, not started) and re-points the not yet started page rebuild items to the deck v2_3_0. Same route as sen0401_lineage_res14. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_Ch13Chart"; REV = "ex:Revision_Lineage3_Scope25"
ACTIVE = ["ex:Out3_ScopeR25", "ex:Out3_GoalR25", "ex:Out3_ObjectiveR25", "ex:Out3_BacklogR27"]; NEWB = "ex:Out3_BacklogR28"; R.NEWB = NEWB
WHEN = "Tuesday 2026-10-27, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders and the coordinator's order to fill the gap through change management without weakening the check; no question to the owner is needed; nothing is waived)"
FACT = ("MEASURED 2026-10-27: the control of the chapter 13 deck v2_2_0 (register v0.531.0, story ST_Deck13_Ex12 Done) ran the deck check v1_1_0 (sen0401_deck_check_v1_1_0.py, under Python 3.14.6 as it requires) on the deck v2_2_0 and on the deck v2_1_0: both print REFUSED ('chart ppt/charts/chart2.xml', 'has no data labels'), the chart of slide 21 (example 10); the same check run on the newest decks of chapters 12 and 14 prints 0 mismatches. The defect is therefore in the chapter 13 deck, older than the work of the executor, and byte-identical in v2_2_0 (found by the executor of ST_Deck13_Ex12 and confirmed by the control). "
        "SECOND GAP, found by the control in the text diff: the body text of slide 24 still says that the wrong passphrase gives the cut text The wallet passphrase entered wa, while the code of example 12 now prints the whole message The wallet passphrase entered was incorrect. (the slide must say what its code prints). "
        "BELONGS TO THE MISSION: the mission is teaching material of every chapter that meets the written standard (charts are native objects with explained values; what a slide says must be what its code prints); the deck check is the standard's executable form and passes the other chapters. FIT: the repair is a new deck v2_3_0 (and a manifest v1_2_0 that names it, code unchanged); no check is weakened, no owner decision is needed. "
        "ORDER: the not yet started page rebuild ST_Ch13_PageRebuild would otherwise be built from a deck that is replaced at once, so its items name the deck v2_3_0 and the manifest v1_2_0 and wait for the Verify task of the new story; the chapter 14 page is not affected. The page 9.81.0 is delivered and failing; nothing is waived.")
TXT_D = ("Make the NEW deck file SEN0401_Ch13_BitcoinSecurity_3e_v2_3_0.pptx (in 03-materials/ch13) from the committed deck v2_2_0 (never edited; SHA-256 before and after) with TWO changes only: (1) the native chart ppt/charts/chart2.xml on slide 21 (example 10) carries data labels, as every chart of the standard does, so that the deck check v1_1_0 stops refusing it; the plotted values and the chart type stay as they are, and the five other charts keep their labels; (2) the body text of slide 24 says what the code of example 12 prints: the wrong passphrase gives The wallet passphrase entered was incorrect. (the whole message, not a cut). No other slide, example, link, note or picture changes. New files: the deck plan v2_3_0, the deck builder files that must change (new version numbers), the example files your builder needs, and the deck file. "
         "Also make the NEW chapter-code manifest 03-materials/ch13/page/chapter_code_ch13_v1_2_0.json from v1_1_0 (never edited) with ONLY the fields manifest, deck and deck_version changed to name the new files (chapter_code_ch13_v1_2_0, the deck v2_3_0, 2.3.0); every example, code, expected output and the setup stay byte-identical in content. "
         "PROOF kept as logs written into the repository (not /tmp), each written once after its run is complete: SHA-256 of deck v2_2_0 and manifest v1_1_0 before and after; the diff of the extracted slide text and notes of v2_2_0 against v2_3_0 (only slide 24, only that sentence) and the list of differing package parts (only the chart part, slide 21 and 24 parts, the properties part); the deck check v1_1_0 under Python 3.14.6 on v2_3_0: 28 examples, 0 mismatches, exit 0 (the check is NOT edited or weakened); the run of all 28 examples of the manifest v1_2_0 on the stored results (28 of 28, every output equal to its expected output, none with Error: in its first 160 characters); the deck standard check v1_1_0, the overlap check, the arc check, the chapter check Deck/Ch13 and the manifest check; the count of the deck's hyperlinks (14 distinct addresses, all kept); the manifest differs from v1_1_0 only in the three fields; nochange (the commit only adds files). "
         "DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES, AND DO NOT EDIT THE PAGE TESTS, THE CHECKS OR THEIR THRESHOLDS. A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate, a test or a threshold. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. The machine has 2 cores and little disk: remove only the temporary folders your own runs created and name them in your report. Commit your work to main (pull --rebase before push).")
VT_D = "Compare the SHA-256 of the deck v2_2_0 and the manifest v1_1_0; read the slide text diff and the differing package parts; run the deck check v1_1_0 under Python 3.14.6 on the new deck; run the 28 examples of the manifest v1_2_0; run the deck standard, overlap, arc, chapter and manifest checks; count the deck hyperlinks; compare the manifest fields; nochange."
STS = [("ST_Deck13_Charts", "The chapter 13 deck v2_3_0 and manifest v1_2_0: every chart carries data labels and slide 24 says what its code prints, as new files", ["AC9_Deck13_Charts"], ["TK_Deck13_Charts_Build", "TK_Deck13_Charts_Verify"], "SEN0401-I41-deck13charts", TXT_D, VT_D, [], 14, 2, 2.0)]
ITER = ("Iter_41", "Iteration 41: the chapter 13 deck v2_3_0, its chart labels and slide 24 sentence repaired (planned, not started)", "2026-11-18T12:00:00", "2026-11-19T12:00:00", "The deck v2_3_0 and the manifest v1_2_0 exist as new files, the deck check v1_1_0 prints 0 mismatches for chapter 13, and slide 24 says what its code prints.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    return {"AC9_Deck13_Charts": ("The chapter 13 deck v2_3_0 and the manifest v1_2_0 are new files whose charts all carry data labels and whose slide 24 says what its code prints, and change nothing else", base + "Given the deck v2_2_0 and the manifest v1_1_0 (unchanged) and the deck check v1_1_0 as a gate (unchanged), when the NEW deck v2_3_0 and the NEW manifest v1_2_0 are made, then ALL of: (1) the deck v2_2_0 and the manifest v1_1_0 are byte-identical (SHA-256 before and after); (2) the slide text and notes of v2_2_0 against v2_3_0 differ only in the body sentence of slide 24, and the differing package parts are only the chart part of slide 21, the slide 21 and 24 parts and the properties part; (3) the deck check v1_1_0 under Python 3.14.6 on v2_3_0 prints 28 examples re-run, 0 mismatches and exits 0; (4) the manifest v1_2_0 differs from v1_1_0 only in the fields manifest, deck and deck_version, its 28 examples run 28 of 28 on the stored results with every output equal to its expected output and none carrying Error: in its first 160 characters; (5) the 14 hyperlink addresses are kept, the deck standard check v1_1_0, the overlap check, the arc check v1_3_0, the chapter check Deck/Ch13 and the manifest check pass; (6) no committed file is edited, no gate, test or threshold changed; results as printed; if any element fails the repair is named failing. " + FACT, "ex:TS_ChapterCheck, ex:TS_DeckMatch", "deck check v1_1_0 (Python 3.14.6); deck standard check v1_1_0; chapter check v1_4_0; deck control check v1_1_0; deck13 control check v1_0_0")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The chapter 13 deck v2_2_0: the chart on slide 21 has no data labels and the body text of slide 24 contradicts what its code prints"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the story into Iteration 41."))
    ia = ('\nex:IA3_Ch13Chart a backlog:ImpactAssessment ;\n    rdfs:label "What the chapter 13 deck chart labels and slide 24 sentence repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: a new chapter 13 deck file v2_3_0 and manifest v1_2_0, and the not yet started page rebuild ST_Ch13_PageRebuild, whose texts name the deck v2_3_0 and which waits for the new deck story; the chapter 14 page is NOT affected. NOT AFFECTED: the controlled criteria of the decks (they stay met), the delivered deck, the old plans, every committed file. ESTIMATE (G120): 2.0 h plus 1.0 h verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the deck check v1_1_0 refuses the chart on slide 21 of the chapter 13 deck (no data labels), and the body text of slide 24 contradicts its code, found in the control of the deck v2_2_0 (register v0.531.0)."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the chapter 13 deck chart labels and slide 24 sentence repair); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the chapter 13 deck chart labels and slide 24 sentence repair"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch13Chart ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the chapter 13 deck chart labels and slide 24 sentence repair: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The chapter 13 deck with example 12 shown without the Error: prefix, and the chapter 13 page rebuilt on it, as new files"
    tx = "New files: the chapter 13 deck v2_3_0 (chart labels of slide 21, one sentence of slide 24), its deck plan and the chapter-code manifest v1_2_0. " + FACT
    L = ('\nex:Del3_Ch13Chart a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Ch13Chart ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-27 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the chapter 13 deck chart labels and slide 24 sentence repair). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR26", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the chapter 13 deck chart labels and slide 24 sentence repair: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR26", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Ch13Chart a backlog:Goal ;
    rdfs:label "The chapter 13 deck meets the deck check v1_1_0 (every chart carries data labels) and says on slide 24 what its code prints"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR26 .
ex:G3_Ch13Chart rdfs:comment "Drafted by the lineage agent on 2026-10-27 from the change request ex:CR3_Ch13Chart; the intent origin is therefore Derived."@en .
ex:Spec3I_Ch13Chart a backlog:Specification ;
    rdfs:label "What it is for the chapter 13 deck chart labels and slide 24 sentence repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Ch13Chart ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR26 .
ex:Spec3I_Ch13Chart_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Ch13Chart ; backlog:hasScenarioText %s .
ex:Spec3I_Ch13Chart_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Ch13Chart ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal or an exit code, or leaves a folder, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR26", "Out3_ScopeR26"), "third lineage, Goal stage rebuilt for the chapter 13 deck chart labels and slide 24 sentence repair: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR26", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Ch13Chart a backlog:Objective ; rdfs:label "The page follow-ups met on verified evidence: from 0 to 1"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Ch13Chart ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Ch13Chart ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Ch13Chart ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR26 .
ex:Met3_Ch13Chart a backlog:Metric ; rdfs:label "chapter 13 deck repair story Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Ch13Chart a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair story is controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criterion." ; backlog:expectedValue "2"^^xsd:decimal .
ex:ObsR32_Ch13Chart_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Ch13Chart ; backlog:observationFor ex:Obj3_Ch13Chart ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Ch13Chart rdfs:comment "Drafted by the lineage agent on 2026-10-27 from the change request ex:CR3_Ch13Chart; the intent origin is therefore Derived."@en .
''' % (lit("Count of the story ST_Deck13_Charts whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the chapter 13 page 9.81.0 on 2026-10-27: the deck v2_3_0 does not exist, so 0 of 1."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR26", "Out3_GoalR26"), "third lineage, Objective stage rebuilt for the chapter 13 deck chart labels and slide 24 sentence repair: one objective (0 to 1) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR26", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR27"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    extra = []
    for m in ("ST_Ch13_PageRebuild", "TK_Ch13_PageRebuild_Build", "TK_Ch13_PageRebuild_Verify", "AC9_PageRebuild_Ch13"):
        i, j = T.blk(t, m); b = t[i:j]; stt = re.findall(r"hasState backlog:(\w+)", b)
        assert not stt or stt[0] in ("Proposed", "Ready"), (m, stt)
        b2 = b.replace("v2_2_0", "v2_3_0").replace("2.2.0", "2.3.0").replace("manifest v1_1_0", "manifest v1_2_0").replace("ST_Deck13_Ex12 must be Done first", "ST_Deck13_Charts must be Done first").replace("(the deck story ST_Deck13_Ex12", "(the deck story ST_Deck13_Charts")
        if m == "TK_Ch13_PageRebuild_Build": b2 = b2.replace("backlog:dependsOn ex:TK_Deck13_Ex12_Verify ;", "backlog:dependsOn ex:TK_Deck13_Ex12_Verify, ex:TK_Deck13_Charts_Verify ;"); assert "TK_Deck13_Charts_Verify" in b2
        assert b2 != b, m
        t = t[:i] + b2 + t[j:]
        extra.append("ex:%s backlog:hasAuditNote %s .\n" % (m, lit("Deck reference corrected " + M.now()[:10] + ": the control of the deck v2_2_0 found two gaps (ex:CR3_Ch13Chart); this item names the deck v2_3_0 and the manifest v1_2_0 and waits for the Verify task of ST_Deck13_Charts. Text and dependency only; the unit is not started and has no evidence, and no criterion changes in meaning.")))
    L = []; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_Ch13Chart and the control of the chapter 13 deck v2_2_0 (register v0.531.0)."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Ch13Chart").replace("ex:Data3S_TC9_", "ex:Data3S_TC9O_").replace("ex:TC9_", "ex:TC9O_"))
    L = [x.replace("ex:TC9_", "ex:TC9O_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, deps, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Ch13Chart", "Obj3_Ch13Chart", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", deps, sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 41 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Ch13Chart, ex:Spec3I_Ch13Chart_Pass, ex:Spec3I_Ch13Chart_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-27, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Ch13Chart backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Ch13Chart a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the chapter 13 deck chart labels and slide 24 sentence repair"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by one story; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Ch13Chart and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L) + "".join(extra)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR28", "Out3_ObjectiveR26"), "third lineage, Backlog stage rebuilt: the chapter 13 deck chart labels and slide 24 sentence repair admitted into the planned Iteration 41 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
