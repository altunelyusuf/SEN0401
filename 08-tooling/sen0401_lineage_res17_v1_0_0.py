#!/usr/bin/env python3
"""sen0401_lineage_res17 v1_0_0 - change route for the three deck gaps of chapters 1, 5 and 6 (ex:CR3_Ch01DeckCheck, ex:CR3_Ch05DeckCheck, ex:CR3_DeckCh06Slide51): a StageRevision from the Scope stage that ADMITS three deck stories into the NEW Iteration 43 (planned, not started). Same route as sen0401_lineage_res16. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_retro24_v1_0_0 as RT
R = RT.R; lit = G.lit
CRS = ["ex:CR3_Ch01DeckCheck", "ex:CR3_Ch05DeckCheck", "ex:CR3_DeckCh06Slide51"]; REV = "ex:Revision_Lineage3_Scope27"
ACTIVE = ["ex:Out3_ScopeR27", "ex:Out3_GoalR27", "ex:Out3_ObjectiveR27", "ex:Out3_BacklogR29"]; NEWB = "ex:Out3_BacklogR30"; R.NEWB = NEWB
WHEN = "Wednesday 2026-10-28, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator ordered the route for the chapter 1 and chapter 5 deck gaps and decided that the chapter 6 chart label finding is a defect fix and not an owner decision; the check is not weakened; nothing is waived)"
FACT = ("MEASURED 2026-10-28 by the lineage agent on its own re-runs of the deck check v1_1_0 under Python 3.14.6 on the delivered decks of chapters 1 to 8 (logs kept by the runs): chapters 2, 3, 4, 6, 7 and 8 print 0 mismatches. "
        "CHAPTER 1, deck v3_1_0: 8 mismatches, all one kind: the 8 plotted values of the cumulative supply chart (10.5, 15.75, 18.375, 19.6875, 20.3438, 20.6719, 20.8359, 20.918) are in no executed output (provenance). "
        "CHAPTER 5, deck v3_2_0 (68 slides): 106 examples re-run, 32 mismatches: 27 example rows are 'not a recorded row with this result' (the recording in 08-tooling/ch05-deck is that of the older deck) and 5 chart mismatches (the plan has 5 chart items, the file 1 chart part). "
        "CHAPTER 6, deck v2_1_0: the deck check passes, but the native chart on slide 51 'The subsidy, halving by halving' has crowded data labels on its five smallest bars (3.125 down to 0.195) that overlap and cannot be read; no check measures chart label collisions (found 2026-10-22 by the builder session's rendered review; the coordinator decided on 2026-10-28 that it is a defect fix). "
        "BELONGS TO THE MISSION: every lecture deck of chapters 1 to 8 meets the written standard (charts are native objects whose values come from code that ran and whose labels can be read) and the midterm exam of chapters 1 to 8 (queued) draws on these decks, so they come first. FIT: each repair is a new deck version as new files; no check is weakened. The arc check refusal of the chapter 5 closing slide is the pending owner decision ex:CR3_GateArcDark and is NOT touched here; nothing is waived.")
COMMON = ("DO NOT EDIT OR APPEND TO ANY FILE COMMITTED EARLIER, INCLUDING YOUR OWN LOG FILES, AND DO NOT EDIT THE CHECKS OR THEIR THRESHOLDS. A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate or a threshold, or if the only way changes the code shown on the slides of a chapter whose page is controlled (then the page manifest would change: report, do not decide). Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. The machine has 2 cores and little disk (about 1.2 GB free, stop at 0.9): run one build at a time, remove only the temporary folders your own runs created and name them in your report. Commit your work to main (pull --rebase before push).")
TXT1 = ("Make the NEW deck file SEN0401_Ch01_Introduction_3e_v3_2_0.pptx (03-materials/ch01) from the committed deck v3_1_0 (never edited; SHA-256 before and after) so that the deck check v1_1_0 (unchanged) under Python 3.14.6 prints 0 mismatches and exits 0. The 8 plotted values of the cumulative supply chart (millions after each halving: 10.5, 15.75, 18.375, 19.6875, 20.3438, 20.6719, 20.8359, 20.918) must each equal, as a number, a number printed by an executed output of the chapter, or equal a recorded chart expression of the recording, whichever way the check accepts. PREFERRED: record the chart's expression in a NEW recording (08-tooling/ch01-deck, new version numbers for the examples file and the recording) so that no new example appears on any slide. The chart type, title, labels and plotted values stay; every other slide, note, link and picture stays; the 15 examples still re-run with the same results. "
        "PROOF kept as logs written into the repository (not /tmp), each written once after its run is complete: SHA-256 of the deck v3_1_0 before and after; the diff of slide text and notes (none, or only what you state); the differing package parts; the deck check v1_1_0 on the new deck (0 mismatches, exit 0); the deck standard check v1_1_0, the overlap check, the arc check v1_3_0, the chapter check Deck/Ch01 and the manifest check; the count of the deck's hyperlinks against v3_1_0; nochange (the commit only adds files). " + COMMON)
TXT5 = ("Make the NEW deck file with the next deck version above v3_2_0 (v3_3_0) of chapter 5 (03-materials/ch05) from the committed deck v3_2_0 (never edited; SHA-256 before and after) so that the deck check v1_1_0 (unchanged) under Python 3.14.6, run on the new deck, prints 0 mismatches and exits 0. Two findings: (1) the recording of the chapter (08-tooling/ch05-deck/examples_out) is that of an older deck, so 27 of the 106 example rows on the deck are 'not a recorded row with this result': make a NEW examples file and a NEW recording (new version numbers) that hold every row the deck shows, recorded by running the examples under Python 3.14.6, with the results the slides show (a result the slides show that the code does not print is a deck error to correct on the slide, state each); (2) the plan has 5 chart items and the file 1 chart part: establish from the plan, the deck and the chapter's review which state is intended; the standard says charts are native objects whose values come from code that ran and every chart has data labels, so build the charts the plan intends if they are missing (native chart objects, not pictures) or, only where the plan itself is stale, say so and make the NEW plan state what the deck has; STOP and report if the intent is not clear from the files. The closing slide stays as it is: the arc check refusal for the light closing slide is the owner's pending decision (ex:CR3_GateArcDark) and is not to be worked around. "
        "PROOF kept as logs written into the repository (not /tmp), each written once after its run is complete: SHA-256 of the deck v3_2_0 before and after; the slide text and notes diff against v3_2_0 (state every difference); the deck check v1_1_0 on the new deck; the deck standard check v1_1_0, the overlap check, the chapter check Deck/Ch05, the manifest check, the arc check v1_3_0 (its only refusal may be the closing slide); the count of hyperlinks; nochange. " + COMMON)
TXT6 = ("Make the NEW deck file SEN0401_Ch06_Transactions_3e_v2_2_0.pptx (03-materials/ch06) from the committed deck v2_1_0 (never edited; SHA-256 before and after) with ONE change: the native chart on slide 51 'The subsidy, halving by halving' has data labels that can be read, the five smallest bars (3.125 down to 0.195) included, for example by fewer decimals, a smaller font size or labels only where they fit; the chart stays a native chart object with data labels (the deck check requires them), the plotted values and the chart type stay. Show it by rendering slide 51 of the new deck (soffice) to a picture kept in the repository, and count overlapping label pairs on it by a method you state. No other slide, example, link, note or picture changes. "
        "PROOF kept as logs written into the repository (not /tmp), each written once after its run is complete: SHA-256 of the deck v2_1_0 before and after; the slide text and notes diff (none); the differing package parts (the chart part of slide 51 and the properties part only); the rendered slide 51 and the overlap count; the deck check v1_1_0 (0 mismatches, exit 0), the deck standard check v1_1_0, the overlap check, the arc check v1_3_0, the chapter check Deck/Ch06 and the manifest check; the hyperlink count; nochange. " + COMMON)
VT1 = "Compare the SHA-256 of the deck v3_1_0; read the slide text diff and the differing package parts; run the deck check v1_1_0 under Python 3.14.6 on the new deck; run the deck standard, overlap, arc, chapter and manifest checks; count the hyperlinks; nochange."
VT5 = "Compare the SHA-256 of the deck v3_2_0; read the slide diff; run the deck check v1_1_0 under Python 3.14.6 on the new deck (0 mismatches); run the deck standard, overlap, chapter and manifest checks and the arc check (only the closing slide may be refused); count the charts and the hyperlinks; nochange."
VT6 = "Compare the SHA-256 of the deck v2_1_0; read the differing package parts; render slide 51 and look at the five smallest bars; run the deck check v1_1_0 under Python 3.14.6, the deck standard, overlap, arc, chapter and manifest checks; count the hyperlinks; nochange."
STS = [("ST_Deck01_Charts", "The chapter 1 deck v3_2_0: every plotted chart value comes from code that ran, as new files", ["AC9_Deck01_Charts"], ["TK_Deck01_Charts_Build", "TK_Deck01_Charts_Verify"], "SEN0401-I43-deck01", TXT1, VT1, 2.0),
       ("ST_Deck05_Examples", "The chapter 5 deck v3_3_0: every example row is a recorded row and the charts match the plan, as new files", ["AC9_Deck05_Examples"], ["TK_Deck05_Examples_Build", "TK_Deck05_Examples_Verify"], "SEN0401-I43-deck05", TXT5, VT5, 4.0),
       ("ST_Deck06_Labels", "The chapter 6 deck v2_2_0: the data labels of the subsidy chart on slide 51 can be read, as a new file", ["AC9_Deck06_Labels"], ["TK_Deck06_Labels_Build", "TK_Deck06_Labels_Verify"], "SEN0401-I43-deck06", TXT6, VT6, 2.0)]
ITER = ("Iter_43", "Iteration 43: the decks of chapters 1, 5 and 6 repaired (planned, not started)", "2026-11-22T12:00:00", "2026-11-23T12:00:00", "The decks of chapters 1, 5 and 6 exist as new files and the deck check v1_1_0 prints 0 mismatches for them, the label collision on slide 51 of chapter 6 is gone.")
def crit():
    base = "Owner-directed work (" + ", ".join(CRS) + ", " + WHEN + "). "
    tl = "deck check v1_1_0 (Python 3.14.6); deck standard check v1_1_0; chapter check v1_4_0; arc check v1_3_0"
    mk = lambda ch, old, new, body: ("The chapter %s deck %s is a new file that the deck check v1_1_0 accepts and that changes nothing else" % (ch, new), base + "Given the deck %s (unchanged) and the deck check v1_1_0 as a gate (unchanged), when the NEW deck %s is made, then ALL of: (1) the deck %s is byte-identical (SHA-256 before and after); %s (last) no committed file is edited, no gate, test or threshold changed; results as printed; if any element fails the repair is named failing. " % (old, new, old, body) + FACT, "ex:TS_ChapterCheck, ex:TS_DeckMatch", tl)
    return {"AC9_Deck01_Charts": mk("1", "v3_1_0", "v3_2_0", "(2) the deck check v1_1_0 under Python 3.14.6 on it prints 0 mismatches and exits 0, with the 15 examples re-run as before; (3) the slide text and notes differ from v3_1_0 only as the log states; (4) the deck standard check v1_1_0, the overlap check, the arc check v1_3_0, the chapter check Deck/Ch01 and the manifest check pass; (5) the hyperlink addresses of v3_1_0 are all kept;"),
            "AC9_Deck05_Examples": mk("5", "v3_2_0", "v3_3_0", "(2) the deck check v1_1_0 under Python 3.14.6 on it prints 0 mismatches and exits 0; (3) every slide difference from v3_2_0 is stated in the log; (4) the deck standard check v1_1_0, the overlap check, the chapter check Deck/Ch05 and the manifest check pass and the arc check refuses nothing but the closing slide (the pending owner decision); (5) the hyperlink addresses are all kept; (6) the charts of the file equal the charts the plan declares;"),
            "AC9_Deck06_Labels": mk("6", "v2_1_0", "v2_2_0", "(2) the slide text and notes are identical and the differing package parts are the chart part of slide 51 and the properties part only; (3) a rendering of slide 51 shows no overlapping data labels (count 0 by the method the log states); (4) the deck check v1_1_0 under Python 3.14.6 prints 0 mismatches and exits 0, and the deck standard check v1_1_0, the overlap check, the arc check v1_3_0, the chapter check Deck/Ch06 and the manifest check pass; (5) the hyperlink addresses are all kept;")}
IAS = [("IA3_Ch01DeckCheck", "ex:CR3_Ch01DeckCheck", "AFFECTED: a new chapter 1 deck v3_2_0 and the recording or expressions that make its chart values come from code; the chapter 1 page 9.73.0 is NOT affected unless the code shown on a slide changes (STOP and report in that case). ESTIMATE (G120): 2.0 h plus 1.0 h verification."),
       ("IA3_Ch05DeckCheck", "ex:CR3_Ch05DeckCheck", "AFFECTED: a new chapter 5 deck v3_3_0, a new recording of its examples and, only if the plan is stale, a new plan; the closing slide and the pending ex:CR3_GateArcDark are NOT touched; the chapter 5 page 9.84.0 is NOT affected unless code shown on a slide changes (STOP and report). ESTIMATE (G120): 4.0 h plus 1.0 h verification."),
       ("IA3_DeckCh06Slide51", "ex:CR3_DeckCh06Slide51", "AFFECTED: a new chapter 6 deck v2_2_0 whose slide 51 chart part is the only changed content; the chapter 6 page is NOT affected. ESTIMATE (G120): 2.0 h plus 1.0 h verification.")]
def ev_change(t):
    out = ""
    for ia, cr, aff in IAS:
        out += ('\nex:%s a backlog:ImpactAssessment ;\n    rdfs:label "What the repair of %s costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (ia, cr[3:], cr, lit(FACT + " " + aff + " NOT AFFECTED: every controlled criterion of the decks (they stay met), every committed file."))
    return t + out, "Three ImpactAssessments for the deck gaps of chapters 1, 5 and 6 (change requests ex:CR3_Ch01DeckCheck, ex:CR3_Ch05DeckCheck, ex:CR3_DeckCh06Slide51); the requests were recorded first."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change requests " + ", ".join(CRS) + " (" + WHEN + ") add three deliverables (the decks of chapters 1, 5 and 6 repaired as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The requests and their assessments were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the decks of chapters 1, 5 and 6 repaired"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_Ch01DeckCheck, ex:IA3_Ch05DeckCheck, ex:IA3_DeckCh06Slide51 ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, ", ".join(CRS), lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the deck repairs of chapters 1, 5 and 6: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The decks of chapters 1, 5 and 6 repaired as new files so that the deck check accepts them and the chapter 6 chart labels can be read"
    tx = "New files: the chapter 1 deck v3_2_0, the chapter 5 deck v3_3_0 with its recording, the chapter 6 deck v2_2_0, with their logs. " + FACT
    L = ('\nex:Del3_DeckGaps a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_DeckGaps ; rdfs:seeAlso %s .\n" % ", ".join(CRS)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-28 by the stage revision %s on the change requests %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the decks of chapters 1, 5 and 6 repaired). No exclusion changes: new files only." % (REV, ", ".join(CRS), WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR28", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the deck repairs of chapters 1, 5 and 6: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR28", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_DeckGaps a backlog:Goal ;
    rdfs:label "The decks of chapters 1 to 8 are accepted by the deck check and their chart labels can be read"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR28 .
ex:G3_DeckGaps rdfs:comment "Drafted by the lineage agent on 2026-10-28 from the change requests of the deck gaps; the intent origin is therefore Derived."@en .
ex:Spec3I_DeckGaps a backlog:Specification ;
    rdfs:label "What it is for the deck repairs of chapters 1, 5 and 6 to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_DeckGaps ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR28 .
ex:Spec3I_DeckGaps_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_DeckGaps ; backlog:hasScenarioText %s .
ex:Spec3I_DeckGaps_Fail a backlog:TestScenario ; rdfs:label "A repair that weakens a check, leaves a folder or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_DeckGaps ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change requests: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new files, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a check whose threshold was changed, or a folder left behind, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR28", "Out3_ScopeR28"), "third lineage, Goal stage rebuilt for the deck repairs of chapters 1, 5 and 6: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR28", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_DeckGaps a backlog:Objective ; rdfs:label "The deck follow-ups met on verified evidence: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_DeckGaps ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_DeckGaps ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_DeckGaps ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR28 .
ex:Met3_DeckGaps a backlog:Metric ; rdfs:label "chapter 1, 5 and 6 deck repair stories Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_DeckGaps a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria." ; backlog:expectedValue "3"^^xsd:decimal .
ex:ObsR34_DeckGaps_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_DeckGaps ; backlog:observationFor ex:Obj3_DeckGaps ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_DeckGaps rdfs:comment "Drafted by the lineage agent on 2026-10-28 from the change requests of the deck gaps; the intent origin is therefore Derived."@en .
''' % (lit("Count of the stories ST_Deck01_Charts, ST_Deck05_Examples and ST_Deck06_Labels whose story is Done on bridge-verified evidence."), now, lit("Baseline from the lineage agent's re-runs of 2026-10-28: the decks v3_2_0 (chapter 1), v3_3_0 (chapter 5) and v2_2_0 (chapter 6) do not exist, so 0 of 3."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR28", "Out3_GoalR28"), "third lineage, Objective stage rebuilt for the deck repairs of chapters 1, 5 and 6: one objective (0 to 3) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR28", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR29"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = []; note = "Admitted " + WHEN + " (" + ", ".join(CRS) + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessments and the lineage agent's re-runs of 2026-10-28."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_DeckGaps").replace("ex:Data3S_TC9_", "ex:Data3S_TC9P_").replace("ex:TC9_", "ex:TC9P_"))
    L = [x.replace("ex:TC9_", "ex:TC9P_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_DeckGaps", "Obj3_DeckGaps", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", [], sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 43 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_DeckGaps, ex:Spec3I_DeckGaps_Pass, ex:Spec3I_DeckGaps_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-28, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_DeckGaps backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_DeckGaps a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the decks of chapters 1, 5 and 6 repaired"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (", ".join(CRS), ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by three stories; new files only.")))
    cr = "ex:CR3_DeckCh06Slide51"
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(cr), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_DeckGaps and the stories it admits; it was Pending before (the coordinator decided on 2026-10-28 that it is a defect fix, not an owner decision)."@en .\n' % (cr, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR30", "Out3_ObjectiveR28"), "third lineage, Backlog stage rebuilt: the deck repairs of chapters 1, 5 and 6 admitted into the planned Iteration 43 with criteria, tasks, planning events and the ScopeChange; ex:CR3_DeckCh06Slide51 Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
