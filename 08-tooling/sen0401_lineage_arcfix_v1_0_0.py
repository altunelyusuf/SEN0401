#!/usr/bin/env python3
"""sen0401_lineage_arcfix v1_0_0 - change route (G104, G125, G127, G129, G133, G136) for the gaps the control of the arc check (v0.314.0) found: a ChangeRequest ex:CR3_ArcFindings with its ImpactAssessment, then a StageRevision from the Scope stage that ADMITS four stories into the NEW Iteration 29 (planned, not started):
ST_ArcCheck_Lookup (tool v1_3_0: the check finds the newest deck of the chapter in 03-materials and refuses a plan/file disagreement instead of crashing), ST_Deck01_ArcFix, ST_Deck07_ArcFix, ST_Deck10_ArcFix (new deck versions that the arc check accepts).
Same route as sen0401_lineage_res01. Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
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
CR = "ex:CR3_ArcFindings"; REV = "ex:Revision_Lineage3_Scope13"
ACTIVE = ["ex:Out3_ScopeR13", "ex:Out3_GoalR13", "ex:Out3_ObjectiveR13", "ex:Out3_BacklogR15"]; NEWB = "ex:Out3_BacklogR16"; R.NEWB = NEWB
WHEN = "Sunday 2026-10-25, decided by the lineage's own change route (gaps found are filled through change management in the active lineage; the coordinator relayed the owner's standing orders; nothing is waived)"
FACT = ("MEASURED 2026-10-25 by the control of the arc check v1_2_0 (register v0.314.0, logs 08-tooling/verify/iter24/bridge_arccheck28): (a) for chapter 5 the check reads 08-tooling/ch05-deck, whose newest deck file is a stale 23-slide deck against a 68-slide plan (80 refusals) while the delivered deck is 03-materials/ch05 v3_1_0; "
        "(b) for chapter 3 it crashes with IndexError (a plan and a deck of different lengths) in v1_1_0 and v1_2_0; (c) chapter 1 deck v3_0_0: 3 refusals (agenda ranges end at slide 59 of 62, two resources slides 19 and 61, one notes slide outside the 2 to 4 sentence rule); (d) chapter 7 deck: 1 notes refusal (slide 35); "
        "(e) chapter 10 deck v2_0_0: 9 of 49 slides have notes of 5 sentences against the rule of 2 to 4. None of these is an element of the criteria the decks were controlled on (AC9_Deck_Ch01, _Ch10), so those stay met; the arc check's own rule is the written standard they now fail.")
TXT_LOOK = ("Make the NEW file 08-tooling/sen0401_deck_arc_check_v1_3_0.py from v1_2_0 (which stays byte-identical, SHA-256 before and after): (1) the deck to check is the newest deck of the chapter in 03-materials/chNN (by version in the file name) when SEN0401_DECK is not set, falling back to 08-tooling/chNN-deck only when 03-materials has none; "
            "(2) when the plan and the deck disagree in length, or any slide index of the plan is not in the deck, the check REFUSES with a message that names both lengths and exits 1; it never raises an IndexError; every other rule and message is unchanged. PROOF kept as logs: unified diff; SHA-256 of v1_2_0 before and after; v1_3_0 on chapters 1 to 14 (list the refusals, none lost that v1_2_0 gave for the same deck file); chapter 3 and chapter 5 now give a refusal or pass, never a crash or a stale-deck verdict; fixtures: a plan/deck length mismatch is refused. " + R.NOEDIT + " " + R.COMMON)
def txt_deck(nn, what): return ("Make the arc check v1_2_0 pass on the chapter %d deck as a NEW deck version (a new .pptx above the newest in 03-materials/ch%s, and a new manifest version only if the examples change); the delivered deck stays unchanged. Repair: %s. Everything the deck was controlled on stays met: deck standard check v1_1_0 12/0/0, overlap check, deck control check manifest, error-first scan, Deck chapter check v1_3_0 (examples re-run) all exit 0; the notes stay short reader's prose (2 to 4 sentences, at most 100 words). "
                                % (int(nn), nn, what)) + "PROOF kept as logs: arc check v1_2_0 with SEN0401_DECK set to the new deck exits 0; the five checks above; nochange (every file added). " + R.NOEDIT + " " + R.COMMON
STS = [("ST_ArcCheck_Lookup", "The deck arc check finds the delivered deck of a chapter and refuses a plan/deck mismatch instead of crashing, as a new tool version", ["AC9_ArcLookup"], ["TK_ArcLookup_Build", "TK_ArcLookup_Verify"], "SEN0401-I29-arclookup", TXT_LOOK, "Run v1_3_0 on chapters 1 to 14 and the fixture; byte-compare v1_2_0; nochange; judge that no refusal v1_2_0 gave on the same deck is lost.", 14, 0.5, 2.5),
       ("ST_Deck01_ArcFix", "The chapter 1 deck is accepted by the arc check, as a new deck version", ["AC9_ArcFix_Ch01"], ["TK_Deck01_ArcFix_Build", "TK_Deck01_ArcFix_Verify"], "SEN0401-I29-deck-ch01-arcfix", txt_deck("01", "the agenda ranges run contiguously to the last slide (they end at 59 of 62), there is one resources slide (slides 19 and 61 both carry links), and the notes slide that breaks the 2 to 4 sentence rule is shortened"), "Run arc check v1_2_0 on the new deck and the five deck checks; render and read the changed slides.", 1, 1, 2.0),
       ("ST_Deck07_ArcFix", "The chapter 7 deck is accepted by the arc check, as a new deck version", ["AC9_ArcFix_Ch07"], ["TK_Deck07_ArcFix_Build", "TK_Deck07_ArcFix_Verify"], "SEN0401-I29-deck-ch07-arcfix", txt_deck("07", "the notes of slide 35 are shortened to the rule"), "Run arc check v1_2_0 on the new deck and the deck checks; render and read slide 35.", 1, 0.5, 1.0),
       ("ST_Deck10_ArcFix", "The chapter 10 deck is accepted by the arc check, as a new deck version", ["AC9_ArcFix_Ch10"], ["TK_Deck10_ArcFix_Build", "TK_Deck10_ArcFix_Verify"], "SEN0401-I29-deck-ch10-arcfix", txt_deck("10", "the notes of slides 7, 10, 15, 16, 18, 22, 27, 35 and 36 are shortened to 2 to 4 sentences without losing the point"), "Run arc check v1_2_0 on the new deck and the deck checks; render and read the nine slides.", 1, 0.5, 1.5)]
ITER = ("Iter_29", "Iteration 29: the repairs of the arc-check findings (planned, not started)", "2026-11-01T12:00:00", "2026-11-02T12:00:00", "The arc check finds the delivered decks and never crashes; the decks of chapters 1, 7 and 10 are accepted by it.")
def crit():
    base = "Owner-directed work (" + CR + ", " + WHEN + "). "
    deck = lambda nn, w: ("The chapter %d deck is accepted by the arc check v1_2_0 as a new version and stays met on its earlier checks" % int(nn), base + "Given the chapter %d deck delivered (unchanged), when a NEW deck version is made, then ALL of: (1) arc check v1_2_0 on the new deck exits 0; (2) deck standard check v1_1_0, overlap check, deck control check manifest, error-first scan and Deck chapter check v1_3_0 exit 0; (3) the delivered deck and every committed file are unchanged (nochange); results as printed; if any element fails the deck is named failing. REPAIR: %s. " % (int(nn), w) + FACT,
                          "ex:TS_ArcCheck12, ex:TS_DeckStdCheck11, ex:TS_DeckOverlapCheck, ex:TS_ChapterCheck", "arc check v1_2_0; deck standard check v1_1_0; deck overlap check v1_0_0; deck control check v1_1_0; Deck chapter check v1_3_0 (system python3, python-pptx)")
    return {"AC9_ArcLookup": ("The arc check v1_3_0 finds the delivered deck and refuses a plan/deck mismatch without crashing, and changes nothing else", base + "Given the arc check v1_2_0 (unchanged), when the NEW file v1_3_0 is made, then ALL of: (1) v1_2_0 is byte-identical (SHA-256 before and after); (2) the diff is limited to the deck lookup and the mismatch refusal; (3) on chapters 1 to 14 no refusal that v1_2_0 gives for the same deck file is lost, and chapters 3 and 5 give no crash and no stale-deck verdict; (4) a plan/deck mismatch fixture is refused with exit 1 and a message naming both lengths; (5) no committed file is edited; results as printed. " + FACT, "ex:TS_ArcCheck13", "arc check v1_3_0 (python-pptx); v1_2_0 byte-identical"),
            "AC9_ArcFix_Ch01": deck("01", "agenda ranges to the last slide, one resources slide, notes of the one slide shortened"), "AC9_ArcFix_Ch07": deck("07", "notes of slide 35 shortened"), "AC9_ArcFix_Ch10": deck("10", "notes of nine slides shortened")}
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Repair of the arc-check findings: the check finds the delivered deck and never crashes, and the decks of chapters 1, 7 and 10 are accepted by it"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_ArcCheck, ex:CR3_Retro24 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(FACT + " Gaps are said openly and are not waived; they are filled through change management in the active lineage. Pending until the ScopeChange of the revision that admits the four stories into Iteration 29."))
    ia = ('\nex:IA3_ArcFindings a backlog:ImpactAssessment ;\n    rdfs:label "What the arc-check findings repair costs and what it touches"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n') % (CR, lit(FACT + " AFFECTED: one new tool file (arc check v1_3_0) and three new deck versions (chapters 1, 7, 10, each with the manifest unchanged unless the examples change). NOT AFFECTED: the controlled criteria of the decks (they stay met), every committed file. ESTIMATE (G120): 2.5 h tool, 2.0 h + 1.0 h + 1.5 h decks, each plus verification."))
    return X.set_status(t + cr + ia, "LS_InProgress"), "ChangeRequest " + CR + " (Pending) with its ImpactAssessment: the arc-check findings of the control of v0.314.0."
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the repair of the arc-check findings); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its assessment were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated (L-112). The interim versions are the declared transition (G129).")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the repair of the arc-check findings"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, ex:IA3_ArcFindings ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the repair of the arc-check findings: the four outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The arc check repaired (deck lookup, no crash) and the decks of chapters 1, 7 and 10 accepted by it, each as new files"
    tx = "The arc check v1_3_0 as a new file that finds the delivered deck and refuses a plan/deck mismatch; new deck versions for chapters 1, 7 and 10 that the arc check accepts. " + FACT
    L = ('\nex:Del3_Arc a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Arc ; rdfs:seeAlso %s .\n" % CR
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-25 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the arc-check findings). No exclusion changes: new files only." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR14", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the arc-check findings: one deliverable in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR14", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Arc a backlog:Goal ;
    rdfs:label "The arc check finds the delivered decks and the delivered decks are accepted by it"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Should ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR14 .
ex:G3_Arc rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_ArcFindings; the intent origin is therefore Derived."@en .
ex:Spec3I_Arc a backlog:Specification ;
    rdfs:label "What it is for the arc-check findings repair to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Arc ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR14 .
ex:Spec3I_Arc_Pass a backlog:TestScenario ; rdfs:label "The repair, built as new files, passes its checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Arc ; backlog:hasScenarioText %s .
ex:Spec3I_Arc_Fail a backlog:TestScenario ; rdfs:label "A repair that loses a refusal, shortens a note by dropping its point, or edits a committed file is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Arc ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request: " + FACT), lit("A repair is met when every element of its criterion is measured on the evidence bridge as met, the output files are new, and no committed file is edited."),
       lit("Given the new tool version or the new deck version, when the checks of the criterion are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a tool version that loses a refusal v1_2_0 gave, or a deck whose notes lose their point, or an edit of a committed file, when the checks run, then the named check fails and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR14", "Out3_ScopeR14"), "third lineage, Goal stage rebuilt for the arc-check findings: one goal with a specification and two scenarios."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR14", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Arc a backlog:Objective ; rdfs:label "The four repairs met on verified evidence: from 0 to 4"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Arc ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Arc ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "4"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Arc ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR14 .
ex:Met3_Arc a backlog:Metric ; rdfs:label "arc-check repairs (tool lookup, decks of chapters 1, 7, 10) whose story is Done on bridge-verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Arc a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the four repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the four criteria." ; backlog:expectedValue "4"^^xsd:decimal .
ex:ObsR24_Arc_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Arc ; backlog:observationFor ex:Obj3_Arc ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Arc rdfs:comment "Drafted by the lineage agent on 2026-10-25 from the change request ex:CR3_ArcFindings; the intent origin is therefore Derived."@en .
''' % (lit("Count of the four repair stories (ST_ArcCheck_Lookup, ST_Deck01_ArcFix, ST_Deck07_ArcFix, ST_Deck10_ArcFix) whose story is Done on bridge-verified evidence."), now, lit("Baseline from the control of the arc check on 2026-10-25 (v0.314.0): none of the four repairs exists, so 0 of 4."))
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR14", "Out3_GoalR14"), "third lineage, Objective stage rebuilt for the arc-check findings: one objective (0 to 4) with metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR14", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR15"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = ['\nex:TS_ArcCheck12 a backlog:ToolScript ; rdfs:label "deck arc check v1_2_0 (reads the deck length; accepts a closing summary part)"@en ; backlog:scriptFileName "sen0401_deck_arc_check_v1_2_0.py" ; backlog:acceptsGraphPath false .\nex:TS_ArcCheck13 a backlog:ToolScript ; rdfs:label "deck arc check v1_3_0 (finds the delivered deck; refuses a plan/deck mismatch)"@en ; backlog:scriptFileName "sen0401_deck_arc_check_v1_3_0.py" ; backlog:acceptsGraphPath false .\n']; note = "Admitted " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment ex:IA3_ArcFindings and the control of v0.314.0."
    for aid, (label, gh, tl, ver) in crit().items():
        L.append(RT.ac_block(aid, label, gh, tl, ver, aid[4:])); L.append(RT.case_blocks(aid[4:], aid).replace("Spec3I_Retro24", "Spec3I_Arc").replace("ex:Data3S_TC9_", "ex:Data3S_TC9A_").replace("ex:TC9_", "ex:TC9A_"))
    L = [x.replace("ex:TC9_", "ex:TC9A_") for x in L]
    itid, lab, st, en, goal = ITER; mem = []
    for sid, title, crits, tks, sess, txt, vtxt, reach, imp, hrs in STS:
        mem += [sid] + tks
        L.append(R.story_block(sid, title, "Del3_Arc", "Obj3_Arc", crits, tks, note, "ex:" + itid, "Proposed"))
        L.append(R.task_block(tks[0], "Build: " + title, "Build", [], sess, "S", hrs, txt, "ex:" + itid, "Proposed", True))
        L.append(R.task_block(tks[1], "Verify: " + title, "Verify", [tks[0]], "builder", "S+%.1fh" % hrs, 1.0, vtxt, "ex:" + itid, "Proposed", True))
        L.append('ex:Plan3A_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 29 (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Arc, ex:Spec3I_Arc_Pass, ex:Spec3I_Arc_Fail .\n' % (sid, sid, now, itid, sid, ", ".join("ex:" + k for k in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    dur = "Planned by the lineage agent on 2026-10-25, NOT started: the start and the end are planned instants (%s to %s UTC); the ceremony is held when the iteration starts. Estimates, not measurements (G120)." % (st, en)
    L.append('ex:%s a backlog:Iteration ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (itid, lit(lab), itid, st, en, lit(dur), lit(goal + " PLANNED, not started: no ceremony is held, no executor is briefed."), ", ".join("ex:" + x for x in mem)))
    L.append("ex:Obj3_Arc backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STS))
    L.append('ex:SC3_Arc a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the repair of the arc-check findings"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STS), lit("Decided by the owner through his standing orders (gaps are filled through change management in the active lineage; nothing is waived), relayed by the coordinator and applied by the lineage agent (" + WHEN + "). The boundary moved outward by four stories; new files only.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Arc and the stories it admits; it was Pending before."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR16", "Out3_ObjectiveR14"), "third lineage, Backlog stage rebuilt: the four arc-check repairs admitted into the planned Iteration 29 with criteria, tasks, planning events and the ScopeChange; the change request Accepted; %d carried items re-admitted." % n
def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
