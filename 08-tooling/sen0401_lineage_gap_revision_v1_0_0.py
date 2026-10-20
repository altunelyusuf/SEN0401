#!/usr/bin/env python3
"""sen0401_lineage_gap_revision v1_0_0 - records, in NEW versions of the SEN0401 slides lineage register, the change route (rulings G104, G125, G127, G133) for the owner's direction of
2026-10-20 10:42 Istanbul, quoted: "No, fill the gaps first." The gaps are the Stage 3.F failures of the Stage 3 documents of chapter 1 and of Bitcoin in numbers and the Stage 4 page ABoxes of
chapters 1 to 7 and of Bitcoin in numbers (the table of the corrected caveat note on the closure report). The third lineage is in its closed Backlog stage, and a deliverable added to a closed scope
is a StageRevision from the Scope stage (G127). One call = one new file = one event; the caller validates, checks and commits each alone. Events, in order:
  change             ChangeRequest and ImpactAssessment (the owner decision quoted), before any stage is touched
  retract            the StageRevision from the Scope stage; the Scope, Goal, Objective and Backlog outputs are marked retracted; nothing is rebuilt
  scope PREV         fills revisedAtCommit; the Scope stage is rebuilt (new area, deliverables, exclusion, blueprint entities and gaps) -> Out3_ScopeR2
  goal PREV          fills the Scope output's commit; goals, specifications, scenarios, use case model -> Out3_GoalR2
  objective PREV     fills the Goal output's commit; objectives with metric, checkpoint and baseline reading, activity and sequence models -> Out3_ObjectiveR2
  backlog PREV       fills the Objective output's commit; two stories (one criterion per file, G133), their tasks, refinement and planning events, test cases, the class models, the ScopeChange;
                     the same carried items are re-admitted by admission and are not re-dated -> Out3_BacklogR2
  fill PREV          fills the Backlog output's commit
Digests come from the framework's own state_digest (table v4, scoped to the third lineage); times from the clock (UTC); commits from git. Nothing is waived and no recorded digest is rewritten.
Usage: sen0401_lineage_gap_revision_v1_0_0.py change|retract|scope PREV|goal PREV|objective PREV|backlog PREV|fill PREV
"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X

esc = M.esc
EXEC = "ex:Executor_ClaudeCodeSession"
ITER = "ex:Iter_12"
REV = "ex:Revision_Lineage3_Scope"
OWNER_WHEN = "2026-10-20 10:42 Istanbul (2026-10-20T07:42:00 UTC)"
QUOTE = '"No, fill the gaps first."'
OWNER_ACT = ("Owner's decision of %s, relayed by the coordinator and recorded by the builder session. The question put to him was whether the Mission outcome and the Achieved status of the third lineage "
             "are to be recorded now; his answer, quoted: %s That is, the Mission outcome is not recorded now, and the gaps named in the corrected caveat note on the closure report are closed first." % (OWNER_WHEN, QUOTE))
CLAUSE = "the research behind it and an interactive page"

M3F = ("Stage 3.F of the Stage 3 documents, measured on 2026-10-20 with the lineage chapter check v1_3_0 (Research/ChNN) and the Stage 4 gate runner v1_1_0: chapter 1 FAIL (1 external claim uncited); Bitcoin in numbers FAIL (19 dangling citations); "
       "chapters 2 to 14 PASS (every claim cited, every citation verified; chapters 5, 6 and 7 with 36, 34 and 55 citations, and the whole chapter check PASS for each). The build notes of 2026-10-14 that name chapter 7 as failing, and the stage-4 status note that names chapter 8 "
       "(45 dangling citations), are out of date: both chapters pass today.")
MS4 = ("Stage 4 page ABox, measured on 2026-10-20 with the Stage 4 gate runner v1_1_0: chapters 1, 2, 3, 4 and Bitcoin in numbers have an older ABox that FAILS Stage4.cov (10 typed individuals lack label and content, in each) and Stage4.sub "
       "(116, 84, 108, 94 and 58 individuals not substantive); chapters 5, 6 and 7 have no Stage 4 page ABox, so the runner stops with an IndexError; chapters 8 to 14 have one that passes.")

UNITS = [("Ch01", "chapter 1", "01"), ("Ch02", "chapter 2", "02"), ("Ch03", "chapter 3", "03"), ("Ch04", "chapter 4", "04"), ("Ch05", "chapter 5", "05"),
         ("Ch06", "chapter 6", "06"), ("Ch07", "chapter 7", "07"), ("Numbers", "Bitcoin in numbers", "numbers")]
OLD = {"Ch01": "an older ABox (page 9.4.2) that fails Stage4.cov and Stage4.sub", "Ch02": "an older ABox (page 9.4.2) that fails Stage4.cov and Stage4.sub",
       "Ch03": "an older ABox (page 1.0.0 on page 9.4.3) that fails Stage4.cov and Stage4.sub", "Ch04": "an older ABox (page 1.0.0 on page 9.4.4) that fails Stage4.cov and Stage4.sub",
       "Numbers": "an older ABox (page 9.4.2) that fails Stage4.cov and Stage4.sub", "Ch05": "no ABox", "Ch06": "no ABox", "Ch07": "no ABox"}
F3 = [("Ch01", "chapter 1", "01", "1 external claim uncited"), ("Numbers", "Bitcoin in numbers", "numbers", "19 dangling citations")]


def lit(s):
    return '"%s"' % esc(s)


def set_status(t, s):
    return X.set_status(t, s)


def fill_re(t, name, commit):
    pat = re.compile(r'(%s a backlog:StageOutput ;.*?backlog:closedAtCommit )"PENDING"' % re.escape(name), re.S)
    assert pat.search(t), "no PENDING on " + name
    return pat.sub(lambda m: m.group(1) + '"%s"' % commit, t, count=1)


def out_r2(t, stage, consumes):
    return ('\nex:Out3_%sR2 a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage, rebuilt by the stage revision from the Scope stage"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (stage, stage, stage, consumes, X.digest(t, stage))


INTENT = ('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-20 from the owner\'s direction of 2026-10-20 10:42 Istanbul (quoted in the change request ex:CR3_Gaps) and from the table of the corrected caveat note on the closure report; the intent origin is therefore Derived. '
          'The owner decided that the gaps are closed first; he did not review the wording of this element."@en .\n')


# ------------------------------------------------------------------------------------------------ change
def ev_change(t):
    cr = ('\nex:CR3_Gaps a backlog:ChangeRequest ;\n    rdfs:label "Close the Stage 3.F and Stage 4 gaps of the chapter materials before the Mission is closed"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR_SEN0401 ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % lit(
        OWNER_ACT + " The gaps are those of the table in the corrected caveat note of 2026-10-20 on the closure report (v0.121): (1) Stage 3.F of the Stage 3 documents: chapter 1 and Bitcoin in numbers fail; (2) Stage 4: the page ABoxes of chapters 1 to 4 and of "
        "Bitcoin in numbers fail Stage4.cov and Stage4.sub and chapters 5, 6 and 7 have none. " + M3F + " " + MS4 + " None of this work is in the scope of the third lineage as it stands: the scope admits the two link passes and the 20 open tasks of the second lineage, and "
        "none of those tasks names a Stage 4 ABox of chapters 1 to 7 or the Stage 3.F of chapter 1 or of Bitcoin in numbers. The change grows the scope. It is recorded as Pending and becomes Accepted in the version that records the ScopeChange admitting the stories, "
        "because a ScopeChange must name what it admits and the stories exist only when the Backlog stage is rebuilt. Not in this change: the connectedness repair of the T-Box files (deferred by the owner on 2026-10-20 09:19 Istanbul), and any change to a gate, a test or a threshold.")
    ia = ('\nex:IA3_Gaps a backlog:ImpactAssessment ;\n    rdfs:label "What closing the Stage 3.F and Stage 4 gaps costs, measured before any of it is started"@en ;\n'
          '    backlog:analyzesRequest ex:CR3_Gaps ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:CR_SEN0401 ;\n    backlog:hasImpactStatement %s .\n') % lit(
        "Measured before the work, 2026-10-20: " + M3F + " " + MS4 + " "
        "Route (rulings G125, G127, G133): the work has criteria of its own, so it is stories of its own; a deliverable added to a closed scope statement is a revision from the Scope stage, not a scope change alone. What moves: the digests of the Scope, Goal, Objective and Backlog stages of the third "
        "lineage move once, when the stages are closed again; the first and second lineages are not touched. What does not move: no Done story is re-dated or re-opened, the two link passes and the 20 carried tasks are re-admitted by admission, and the Mission and its stage stand. "
        "New work, planned in the Backlog version: two stories, as G133 asks one story with one acceptance criterion per file, and not one story per chapter: the story for Stage 3.F carries 2 criteria (chapter 1, Bitcoin in numbers) and the story for the Stage 4 page ABox 8 criteria "
        "(chapters 1 to 7, Bitcoin in numbers), each with its own result; 20 execution tasks (a build and a verify task per unit). Chapters 5, 6 and 7 need no Stage 3.F task: they were measured and pass, which corrects the stale build notes that name chapter 7 as failing. "
        "Iteration: the work is planned into a new twelfth iteration of the third lineage, proposed to end at the same time as the eleventh, 2026-10-23T06:00 UTC (Friday 09:00 Istanbul, the end the owner confirmed for the eleventh on 2026-10-19), because the owner wants the lineage finished as soon as possible; the end is the owner's own confirmed end date of the eleventh iteration (accepted for this iteration by the coordinator on 2026-10-20) and the owner may move it. "
        "The eleventh iteration was considered and not used: it belongs to the second lineage, which is Achieved, and a container the successor cannot carry (the validator refuses a lineage recorded Achieved while a container of it holds open items, and refuses a wound-down lineage's container left open once the successor's Backlog stage has closed); the successor builds sprints of its own. "
        "If a story is still open when the iteration ends, the register shows it as spillover (L4) until the owner rebaselines the iteration or recommits the story; nothing is moved here. "
        "Risk: the Stage 4 builder v2.0.0 reads a chapter number and not the unit named numbers, so Bitcoin in numbers may need a new version of the builder (a new tool version is allowed; a gate change is not). "
        "Cost of waiting: the Mission outcome and the Achieved status stay unrecorded, as the owner decided. Cost of acting: one change request, one assessment, one stage revision (the retraction and the four rebuilt stages, one commit each), two stories, 20 tasks and a new iteration; enforcement value forgone: none. "
        "Nothing is waived and no digest is re-recorded outside the revision.")
    return t + cr + ia, "ChangeRequest ex:CR3_Gaps (disposition Pending) and ImpactAssessment ex:IA3_Gaps for the owner's direction of 2026-10-20 10:42 Istanbul, \"No, fill the gaps first.\": the Stage 3.F and Stage 4 gaps are to be closed before the Mission outcome is recorded; no stage is changed in this version."


# ------------------------------------------------------------------------------------------------ retract
OUTS = ["ex:Out3_Scope", "ex:Out3_Goal", "ex:Out3_ObjectiveR", "ex:Out3_BacklogR"]
REASON = ("%s " % OWNER_ACT +
          "The work that closes the gaps adds two deliverables to the scope of the third lineage (the Stage 3.F repair of two Stage 3 documents and the Stage 4 page ABox of eight units); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage "
          "(ruling G127). The change request ex:CR3_Gaps and the impact assessment ex:IA3_Gaps were recorded first, in the previous version. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the outputs are rebuilt one stage and one commit at a time, each consuming the "
          "last unretracted output above it; the goals, objectives and stories already in the register re-enter by admission and are not re-dated. The retracted outputs and their digests stay in the register as history (L-112). The interim versions are the declared transition (G129): the items "
          "admitted by the retracted Backlog output keep their exemption while the revision is under way. The revision is recorded as decided by the builder role: the owner decided that the gaps are closed first, and the revision is the route that decision needs; the stage revision itself he did not decide.")


def ev_retract(t):
    t = set_status(t, "LS_Opened")
    blk = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the Stage 3.F and Stage 4 gaps are closed before the Mission outcome is recorded"@en ;\n'
           '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso ex:CR3_Gaps, ex:IA3_Gaps ;\n    backlog:revisionReason %s ;\n'
           '    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, lit(REASON), ", ".join(OUTS))
    blk += "".join("%s backlog:outputRetracted true .\n" % o for o in OUTS)
    return t + blk, ("StageRevision of the third lineage from the Scope stage (ruling G127): the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version. "
                     "The change request and impact assessment are in the previous version; the owner's direction of 2026-10-20 10:42 Istanbul is quoted in both.")


# ------------------------------------------------------------------------------------------------ scope
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = set_status(t, "LS_Scoped")
    L = ['''
ex:Area3_GapClosure a backlog:ScopeArea ;
    rdfs:label "The Stage 3.F and Stage 4 gaps of the chapter materials"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "03-materials: the rdodi folders of chapter 1 and of Bitcoin in numbers (Stage 3) and the page folders of chapters 1 to 7 and of Bitcoin in numbers (Stage 4); the runners and the builder in 08-tooling" ;
    backlog:areaMeasure "2 Stage 3 documents that pass Stage 3.F (chapter 1, Bitcoin in numbers) and 8 Stage 4 page ABoxes that pass the Stage 4 gate run (chapters 1 to 7, Bitcoin in numbers)" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_Stage3FRepair a backlog:ScopeDeliverable ;
    rdfs:label "The Stage 3 documents of chapter 1 and Bitcoin in numbers pass Stage 3.F"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_GapClosure ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_Stage4PageAbox a backlog:ScopeDeliverable ;
    rdfs:label "A Stage 4 page ABox for chapters 1 to 7 and Bitcoin in numbers that passes the Stage 4 gate run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_GapClosure ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl3_NoGateChange a backlog:ScopeExclusion ;
    rdfs:label "The gaps are closed without changing a gate, a test or a threshold, and without the connectedness repair"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:excludesConcern "Any change to a gate, a test or a threshold in order to make a unit pass (Stage 3.F, the Stage 4 gates, the chapter checks, the page tests); a citation or a claim removed only to make a gate pass; the connectedness repair of the T-Box files, which the owner deferred on 2026-10-20 09:19 Istanbul to a later lineage; recording the Mission outcome and the Achieved status of this lineage, which wait for the owner's act after the gaps are closed." ;
    backlog:hasExclusionRationale "A gate that is changed to pass proves nothing; a unit that fails stays reported as failing until it passes unchanged gates. The owner deferred quality and cleaning work until after this lineage and decided on 2026-10-20 10:42 Istanbul that the gaps are closed before the Mission outcome is recorded, not that the outcome is recorded first." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Scope3 backlog:requiresDeliverable ex:Del3_Stage3FRepair, ex:Del3_Stage4PageAbox ;
    backlog:coversArea ex:Area3_GapClosure ; backlog:hasScopeExclusion ex:Excl3_NoGateChange ;
    rdfs:seeAlso ex:CR3_Gaps, ex:IA3_Gaps .
ex:Scope3 rdfs:comment %s@en .
ex:Blueprint3 backlog:hasDomainEntity ex:DE3_Stage3Document, ex:DE3_PageAbox .
ex:DE3_Stage3Document a backlog:DomainEntity ; rdfs:label "Stage 3 document - the RDODI document of a chapter, checked by Stage 3.F"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:DE3_PageAbox a backlog:DomainEntity ; rdfs:label "Stage 4 page ABox - the RDODI instance data of a chapter's interactive page"@en ; backlog:belongsToLineage ex:Lineage3 .
''' % (CLAUSE, lit("The Stage 3 documents of chapter 1 and of Bitcoin in numbers pass the Stage 3.F gate unchanged: every external claim is cited and every citation resolves to a source of the research file. " + M3F),
       CLAUSE, lit("A Stage 4 page ABox, built by the Stage 4 builder from the newest page, its objectives, its quiz and its stored browser-test result, for chapters 1 to 7 and for Bitcoin in numbers, that passes the Stage 4 gate run unchanged; the older ABoxes of chapters 1 to 4 and of Bitcoin in numbers stay as the record. " + MS4),
       lit("Revised 2026-10-20 by the stage revision ex:Revision_Lineage3_Scope on the owner's direction of %s, quoted: %s. The statement above is unchanged (L-112). It now also requires the deliverables ex:Del3_Stage3FRepair and ex:Del3_Stage4PageAbox, covers the area ex:Area3_GapClosure and carries the exclusion ex:Excl3_NoGateChange. IN, added: the Stage 3.F repair of the Stage 3 documents of chapter 1 and Bitcoin in numbers, and a Stage 4 page ABox that passes the gate run for chapters 1 to 7 and Bitcoin in numbers. OUT, added: any change to a gate, a test or a threshold, and the connectedness repair. The exclusion ex:Excl3_NoRebuild stands: nothing is rebuilt to admit it, and these deliverables are new files beside the old ones." % (OWNER_WHEN, QUOTE)))]
    L.append("".join('ex:Gap3G_%s_%s a backlog:BlueprintGap ; rdfs:label "No coverage yet for the %s at the %s stage"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:gapForEntity ex:DE3_%s ; backlog:gapForStage backlog:Stage_%s ; backlog:hasGapReason "The entity is covered by the earlier lineages up to the check that fails; this lineage closes the gap of that check and nothing else of its life cycle." .\n'
                     % (e, st, h, human, e, st)
                     for e, h in (("Stage3Document", "Stage 3 document"), ("PageAbox", "Stage 4 page ABox"))
                     for st, human in (("Creation", "creation"), ("ActiveUse", "active use"), ("SuspensionException", "suspension or exception"), ("Termination", "termination"))))
    t += "".join(L)
    return t + out_r2(t, "Scope", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision: two deliverables (the Stage 3.F repair and the Stage 4 page ABox), their area, an exclusion (no gate, test or threshold changed; no connectedness repair) and two domain entities with their gaps."


# ------------------------------------------------------------------------------------------------ goal
GOALS = [("G3_Stage3FPasses", "The Stage 3 documents of chapter 1 and Bitcoin in numbers pass Stage 3.F", "Facing_Mission", ""),
         ("G3_Stage4Passes", "Every page of chapters 1 to 7 and Bitcoin in numbers has a Stage 4 ABox that passes the gate run", "Facing_Scope", ""),
         ("G3_GatesUnchanged", "No gate, test or threshold is changed to make a unit pass", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl3_NoGateChange ;")]


def ev_goal(t, prev):
    t = fill_re(t, "ex:Out3_ScopeR2", prev); t = set_status(t, "LS_Goaled")
    L = []
    for i, label, f, g in GOALS:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_GapClosure ;\n'
                 '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;%s\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n'
                 '    backlog:hasGoalRationale "Derived from the revised scope of the third lineage (ex:Del3_Stage3FRepair, ex:Del3_Stage4PageAbox, ex:Excl3_NoGateChange) and from the owner\'s direction of 2026-10-20 10:42 Istanbul, quoted: %s" ;\n'
                 '    backlog:producedByStage ex:Out3_GoalR2 .\n' % (i, label, f, g, esc(QUOTE)))
    L.append("".join(INTENT % i for i, *_ in GOALS))
    for k, goal, what, ctx in (("3F", "G3_Stage3FPasses", "Stage 3.F passes for a Stage 3 document", "the chapter check and the Stage 4 gate runner, run on the newest research and document files of the unit"),
                               ("S4", "G3_Stage4Passes", "a Stage 4 page ABox passes the gate run", "the Stage 4 gate runner, run on the newest research, document and page ABox files of the unit")):
        L.append('''
ex:Spec3G_%(k)s a backlog:Specification ;
    rdfs:label "What it is for %(what)s"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:%(g)s ;
    backlog:hasSpecificationText "%(what)s when %(ctx)s reports PASS for the gate or gates named by the unit's criterion, with the gate, the test and the threshold exactly as they stand in the course repository; a gate the runner reports as NOT_MEASURED or CANNOT_RUN is reported as such and is not claimed as passed. A unit that fails is named with the failing gate and is not Done." ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR2 .
ex:Scen3G_%(k)s_Passes a backlog:TestScenario ; rdfs:label "A unit's gate run reports PASS on unchanged gates (%(k)s)"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3G_%(k)s ;
    backlog:hasScenarioText "Given the newest files of a unit in the course repository, when %(ctx)s is run, then the gate or gates of the criterion report PASS and the run exits 0 for that gate." .
ex:Scen3G_%(k)s_NotClaimed a backlog:TestScenario ; rdfs:label "A unit whose gate still fails is not claimed as passing (%(k)s)"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3G_%(k)s ;
    backlog:hasScenarioText "Given a unit whose gate reports FAIL, or whose run stops, when the story is to be recorded Done, then the criterion of that unit has no passing result and the story is not Done." .
''' % dict(k=k, g=goal, what=esc(what), ctx=esc(ctx)))
    L.append('''
ex:Model3G_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the closing of the Stage 3.F and Stage 4 gaps"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The owner reads the register to learn which units still fail which gate before the Mission outcome is recorded; a work agent builds the new files of a unit and runs its gates; the Stage 4 builder writes the page ABox from the page data and the stored browser-test result; the gate runner and the chapter check report PASS or FAIL per gate without changing a gate; the evidence bridge verifies the runs and the file hashes; the framework's order check, digest verifier and validator read the chain." ;
    backlog:describesItem ex:G3_Stage4Passes .
''')
    t += "".join(L)
    return t + out_r2(t, "Goal", "Out3_ScopeR2"), "third lineage, Goal stage rebuilt by the stage revision: goals for the Stage 3.F repair, the Stage 4 page ABox and the unchanged gates; two specifications with a nominal and a rejection scenario each; the use case model."


# ------------------------------------------------------------------------------------------------ objective
OBJS = [("Obj3_Stage3FPass", "G3_Stage3FPasses", "Met3_Stage3FPass", "Stage 3 documents (chapter 1, Bitcoin in numbers) whose Stage 3.F gate passes", 0, 2, "Dir_Increase",
         "Baseline measured 2026-10-20: chapter 1 FAIL (1 external claim uncited), Bitcoin in numbers FAIL (19 dangling citations): 0 of 2 pass."),
        ("Obj3_Stage4Pass", "G3_Stage4Passes", "Met3_Stage4Pass", "Stage 4 page ABoxes (chapters 1 to 7, Bitcoin in numbers) whose Stage 4 gate run reports no failing gate", 0, 8, "Dir_Increase",
         "Baseline measured 2026-10-20: chapters 1 to 4 and Bitcoin in numbers FAIL Stage4.cov and Stage4.sub, chapters 5 to 7 have no ABox: 0 of 8 pass."),
        ("Obj3_GatesUnchanged", "G3_GatesUnchanged", "Met3_GatesChanged", "gates, tests and thresholds changed by this work", 0, 0, "Dir_Hold",
         "Baseline 2026-10-20: none changed; read from git as the changes of the gate runner, the chapter check and the page test files, which this work does not touch.")]


def ev_objective(t, prev):
    t = fill_re(t, "ex:Out3_GoalR2", prev); t = set_status(t, "LS_Objectived")
    now = M.now(); L = []
    for i, g, m, what, b, tg, d, basis in OBJS:
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(Wh)s: from %(b)d to %(tg)d"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from this register after the evidence bridge has run the gates against the course repository." ;
    backlog:hasBaselineValue "%(b)d"^^xsd:decimal ; backlog:hasTargetValue "%(tg)d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%(d)s ;
    backlog:hasCheckpoint ex:CP3G_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR2 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3G_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the stories of the gaps are recorded"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the gates of every unit named by the criteria, so the count is read from verified runs." ;
    backlog:expectedValue "%(tg)d"^^xsd:decimal .
ex:Obs35_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the gaps"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "%(b)d"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "%(basis)s" .
''' % dict(i=i, g=g, m=m, what=esc(what), Wh=esc(what[0].upper() + what[1:]), b=b, tg=tg, d=d, now=now, basis=esc(basis)))
    L.append("".join(INTENT % i for i, *_ in OBJS))
    L.append('''
ex:Model3G_Activity a backlog:ModelArtifact ; rdfs:label "How one unit's gap is closed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per unit, in order: run the gate that fails and read what it reports; build the new files (a new version of the research and document files for Stage 3.F; the page ABox from the newest page, its stored test result, its objectives and its quiz for Stage 4), never editing a committed file; run the gates again on the unchanged gates - BRANCH: a gate that still fails leaves the unit failing and it is named in the story; a gate the runner reports as NOT_MEASURED or CANNOT_RUN is reported as such; record the result against the unit's criterion; the evidence bridge verifies the run and the file hashes." ;
    backlog:describesItem ex:Obj3_Stage4Pass .
ex:Model3G_Sequence a backlog:ModelArtifact ; rdfs:label "Who asks whom when a unit's gate is run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_SequenceDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "The work agent asks the builder for the page ABox of a unit and the research tooling for the new research and document files; it asks the gate runner for the verdict of each gate; the evidence bridge runs the gate command and hashes the files; the register records the bridge's verdict against the criterion of the unit; the order check, the digest verifier and the validator read the register." ;
    backlog:describesItem ex:Obj3_Stage4Pass .
''')
    # the class models the Backlog stage owes are met in the Objective stage, where the digest table v4 counts a model artifact (as in the first revision)
    L.append('''
ex:Model3G_Class a backlog:ModelArtifact ; rdfs:label "How a gap story, its criteria and its evidence are stored"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A Story (the Stage 3.F repair or the Stage 4 page ABox) is planned into the twelfth iteration (the third lineage's own) by a PlanningEvent that produces its ExecutionTasks (a build and a verify task per unit). It has an AcceptanceCriterion per unit, each covered by a TestCase of the nominal and of the rejection scenario. Done is recorded only with a TestHarness, a TestEvidence per unit whose gate passed (hasTestId, hasTestSpec, evidenceVerified) and an ArtifactEvidence per new file (path and SHA-256); a unit whose gate fails is named in the story and carries no test evidence." ;
    backlog:describesItem ex:Obj3_Stage3FPass .
ex:Model3G_ClassDesign a backlog:ModelArtifact ; rdfs:label "Design of the stored gap story, its harness and its evidence"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "Classes: Story (identifier, title, state, startedAt, finishedAt, lastAuditedAt, executionModality, admittedByOutput, memberOfContainer) with associations to AcceptanceCriterion (one per unit; coveredByCase), ExecutionTask (decomposesInto; dependsOn between a verify task and its build task and, for chapter 1 and Bitcoin in numbers, the Stage 3.F build task), PlanningEvent (plansItem, plannedInto, producesTask), RefinementEvent (refines, addressesConcern), TestHarness (harnessFor the story), TestEvidence and ArtifactEvidence (attestsCriterion, evidenceVerified, verifiedAt); a StageOutput (hasStateDigest, closedAtCommit) admits the story." ;
    backlog:describesItem ex:Obj3_Stage4Pass .
''')
    t += "".join(L)
    return t + out_r2(t, "Objective", "Out3_GoalR2"), "third lineage, Objective stage rebuilt by the stage revision: three objectives (Stage 3.F passes, Stage 4 page ABoxes pass, gates unchanged) with metric, checkpoint and a baseline reading measured on 2026-10-20; the activity and sequence models."


# ------------------------------------------------------------------------------------------------ backlog
def gherkin_3f(label, nm, measured):
    return ("Given the Stage 3 document of %s and its research data, when the Stage 3.F gate is run on them by the lineage chapter check for Research/%s and by the Stage 4 gate runner for %s, "
            "then Stage3.F reports PASS (measured on 2026-10-20: FAIL, %s) with no gate, test or threshold changed and no citation or claim removed only to pass; "
            "if it still reports FAIL the unit is named failing and this criterion has no passing result." % (label, nm, "Bitcoin in numbers" if nm == "Numbers" else nm.lower(), measured))


def gherkin_s4(label, nm, key):
    old = OLD[nm]
    return ("Given the newest page of %s with its objectives, quiz and stored browser-test result (the unit has %s), when the Stage 4 gate runner is run for the unit on its newest research, document and page ABox data, "
            "then every gate it measures (Stage4.A, Stage4.B, Stage4.cov, Stage4.sub, Stage4.src and Stage3.F) reports PASS and its OVERALL line reports PASS, with the gates the runner reports as NOT_MEASURED or CANNOT_RUN reported as such and not claimed, and no gate, test or threshold changed; "
            "if any measured gate reports FAIL, or the runner stops, the unit is named failing and this criterion has no passing result." % (label, old))


def story_block(sid, title, role_want, sothat, deliv, obj, cat, criteria, tasks, deps_note):
    return ('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput ex:Out3_BacklogR2 ;\n'
            '    backlog:hasInvestmentCategory backlog:%s ;\n'
            '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n'
            '    backlog:satisfiesDeliverable ex:%s ; backlog:pursuesObjective ex:%s ; backlog:hasAcceptanceCriterion %s ;\n'
            '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n'
            '    backlog:decomposesInto %s ;\n'
            '    backlog:hasState backlog:Ready ;\n'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Not scored: the owner decided on 2026-10-20 10:42 Istanbul that the gaps are closed first, so there is no ranking left to compute." ;\n'
            '    backlog:hasAuditNote %s .\n') % (sid, lit(title), sid, lit(title), ITER, cat, lit(role_want), lit(sothat), deliv, obj,
                                                 ", ".join("ex:" + c for c in criteria), EXEC, ", ".join("ex:" + x for x in tasks), lit(deps_note))


def task_block(tid, title, ttype, note, deps=()):
    return ('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n'
            '    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput ex:Out3_BacklogR2 ; backlog:responsible %s ;\n'
            '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:%s ;\n%s'
            '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n'
            '    backlog:hasAuditNote %s .\n') % (tid, lit(title), tid, lit(title), ITER, EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, "Ready" if ttype == "Build" else "Proposed",
                                                 ("    backlog:dependsOn %s ;\n" % ", ".join("ex:" + d for d in deps)) if deps else "", lit(note))


PRODUCES = {"ST_Gap_Stage3F": ["Spec3G_3F", "Scen3G_3F_Passes", "Scen3G_3F_NotClaimed", "Model3G_Class"],
            "ST_Gap_Stage4": ["Spec3G_S4", "Scen3G_S4_Passes", "Scen3G_S4_NotClaimed", "Model3G_ClassDesign", "Model3G_Activity", "Model3G_Sequence"]}


def ev_backlog(t, prev):
    t = fill_re(t, "ex:Out3_ObjectiveR2", prev); t = set_status(t, "LS_Backlogged")
    now = M.now()
    # (a) the carried items are re-admitted by the rebuilt output, not re-dated
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR ;")
    assert n >= 22, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR ;", "backlog:admittedByOutput ex:Out3_BacklogR2 ;")
    L = []
    crit3, crit4, tk3, tk4 = [], [], [], []
    # (b) Stage 3.F: one story, one criterion per document
    for nm, label, key, measured in F3:
        c = "AC3G_3F_" + nm; crit3.append(c)
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:satisfiedByArtifact "the Stage3.F line of the chapter check and of the Stage 4 gate runner, verified by the evidence bridge, and the new research and document files cited by SHA-256" ;\n    backlog:coveredByCase ex:TC3G_3F_Passes, ex:TC3G_3F_NotClaimed .\n'
                 % (c, lit("Stage 3.F passes for the Stage 3 document of %s" % label), lit(gherkin_3f(label, nm, measured))))
        b, v = "TK_Gap3F_%s_Build" % nm, "TK_Gap3F_%s_Verify" % nm; tk3 += [b, v]
        fix = ("Cite the one external claim that Stage 3.F reports uncited, to a source of the research file, in new versions of the research and document files" if nm == "Ch01" else
               "Resolve the 19 dangling citations that Stage 3.F reports: each citation must point to a source of the research file, the missing sources being added to the research file with their record, in new versions of the research and document files; a citation or a claim is not removed only to pass")
        L.append(task_block(b, "Repair Stage 3.F of the Stage 3 document of %s" % label, "Build", "%s. A committed file is not edited. No gate, test or threshold is changed. Satisfies the criterion ex:%s." % (fix, c)))
        L.append(task_block(v, "Verify Stage 3.F for the Stage 3 document of %s" % label, "Verify",
                            "Run Research/%s with the chapter check v1_3_0 and %s with the Stage 4 gate runner v1_1_0, record what they report (Stage3.F and the rest, as measured), and confirm that Research, Deck and Page chapter checks of the unit still pass. Report a gate that fails as failing. Criterion ex:%s." % (nm, key, c), (b,)))
    # (c) Stage 4: one story, one criterion per unit
    for nm, label, key in UNITS:
        c = "AC3G_S4_" + nm; crit4.append(c)
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:satisfiedByArtifact "the Stage 4 gate run of the unit, verified by the evidence bridge, and the new page ABox file cited by SHA-256" ;\n    backlog:coveredByCase ex:TC3G_S4_Passes, ex:TC3G_S4_NotClaimed .\n'
                 % (c, lit("A Stage 4 page ABox of %s passes the Stage 4 gate run" % label), lit(gherkin_s4(label, nm, key))))
        b, v = "TK_GapS4_%s_Build" % nm, "TK_GapS4_%s_Verify" % nm; tk4 += [b, v]
        build = ("Build the Stage 4 page ABox of %s as a new file with the Stage 4 builder (08-tooling/sen0401_page_abox_build_v2_0_0.py) from the newest page, its objectives, its quiz and its stored browser-test result; the stored result is produced for the newest page as it was for chapters 8 to 14 if it is absent." % label)
        if nm == "Numbers":
            build += " The builder v2.0.0 reads a chapter number; if it does not accept the unit named numbers, a new version of the builder is written (a new tool version is allowed; a gate is not changed)."
        if OLD[nm] != "no ABox":
            build += " The older ABox stays as the record."
        L.append(task_block(b, "Build the Stage 4 page ABox of %s" % label, "Build", "%s Satisfies the criterion ex:%s." % (build, c)))
        deps = (b, "TK_Gap3F_%s_Build" % nm) if nm in ("Ch01", "Numbers") else (b,)
        L.append(task_block(v, "Verify the Stage 4 page ABox of %s" % label, "Verify",
                            "Run the Stage 4 gate runner v1_1_0 for %s and the Research, Deck and Page chapter checks of the unit; record every gate as the runner reports it (PASS, FAIL, NOT_MEASURED, CANNOT_RUN). %s Criterion ex:%s." %
                            (key, "The Stage 3.F line of this unit is part of the run, so it waits for the Stage 3.F repair of the unit." if nm in ("Ch01", "Numbers") else "", c), deps))
    # stories
    L.append(story_block("ST_Gap_Stage3F", "Stage 3.F passes for the Stage 3 documents of chapter 1 and Bitcoin in numbers",
                         "the Stage 3 documents of chapter 1 and of Bitcoin in numbers to pass the Stage 3.F gate", "every external claim the two documents make is cited and every citation resolves, so no claim of the course rests on an unchecked source",
                         "Del3_Stage3FRepair", "Obj3_Stage3FPass", "Cat_Compliance", crit3, tk3,
                         "Created by the stage revision ex:Revision_Lineage3_Scope on the owner's direction of %s, quoted: %s. One criterion per document (G133). Chapters 5, 6 and 7 were measured and pass Stage 3.F; they need no work. " % (OWNER_WHEN, QUOTE) + M3F))
    L.append(story_block("ST_Gap_Stage4", "A Stage 4 page ABox that passes the gate run for chapters 1 to 7 and Bitcoin in numbers",
                         "a Stage 4 page ABox for each of chapters 1 to 7 and for Bitcoin in numbers that passes the Stage 4 gate run", "every page of the course is backed by RDODI instance data that carries a label, a complete sentence and a source for each section, widget and objective",
                         "Del3_Stage4PageAbox", "Obj3_Stage4Pass", "Cat_NewCapability", crit4, tk4,
                         "Created by the stage revision ex:Revision_Lineage3_Scope on the owner's direction of %s, quoted: %s. One criterion per unit (G133). " % (OWNER_WHEN, QUOTE) + MS4 +
                         " The Stage 4 gate run of chapter 1 and of Bitcoin in numbers includes Stage 3.F, so the verify tasks of those two units depend on the Stage 3.F build tasks."))
    # scenarios' cases and data
    for k, nm, crits in (("3F", "Stage 3.F", crit3), ("S4", "Stage 4", crit4)):
        L.append('''
ex:TC3G_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the %(nm)s gate on a unit whose files pass and require PASS"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3G_%(k)s_Passes ; backlog:runsOnData ex:Data3G_%(k)s_Passing ;
    backlog:hasCaseText "Run the gate command of the criterion over the newest files of a unit; the gate reports PASS and the run exits 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3G_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the %(nm)s gate on a unit whose files fail and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3G_%(k)s_NotClaimed ; backlog:runsOnData ex:Data3G_%(k)s_Failing ;
    backlog:hasCaseText "Run the gate command over a unit whose gate reports FAIL (for example the older ABox of chapter 1, measured 2026-10-20); the unit carries no verified test evidence for the criterion and the story names it failing." .
ex:Data3G_%(k)s_Passing a backlog:TestData ; rdfs:label "A unit whose %(nm)s gate passes when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest files of a unit for which the gate command exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3G_%(k)s_Failing a backlog:TestData ; rdfs:label "A unit whose %(nm)s gate fails when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The files of a unit for which the gate command reports FAIL or stops, as measured on 2026-10-20 for the units named in the criteria." .
''' % dict(k=k, nm=nm, cr=", ".join("ex:" + c for c in crits)))
    # refinement and planning events
    items = [("ST_Gap_Stage3F", tk3), ("ST_Gap_Stage4", tk4)]
    for s, tks in items:
        for x in [s] + tks:
            L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the owner\'s direction of %s (quoted in ex:CR3_Gaps) and from the measured state in ex:IA3_Gaps; the criterion or criteria and the task text name the gate, the unit and what a passing result is." .\n'
                     % (x, x, x, now, ITER, OWNER_WHEN))
        L.append('ex:Plan3G_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 12"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces %s .\n'
                 % (s, s, now, ITER, s, ", ".join("ex:" + x for x in tks), ", ".join("ex:" + x for x in PRODUCES[s])))
    L.append('%s a backlog:Iteration ; rdfs:label "Iteration 12: close the Stage 3.F and Stage 4 gaps of chapters 1 to 7 and Bitcoin in numbers"@en ; backlog:hasIdentifier "Iter_12" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-23T06:00:00"^^xsd:dateTime ;\n'
             '    backlog:hasDurationSource %s ;\n'
             '    backlog:hasSprintGoal "The Stage 3 documents of chapter 1 and Bitcoin in numbers pass Stage 3.F and the Stage 4 page ABox of chapters 1 to 7 and Bitcoin in numbers passes the Stage 4 gate run, each on the gates as they stand, each unit that fails named; then the owner records the Mission outcome." ;\n'
             '    backlog:hasMember ex:ST_Gap_Stage3F, ex:ST_Gap_Stage4, %s .\n' % (ITER, now, lit("Proposed by the builder session on 2026-10-20 after the owner's direction of %s (quoted in ex:CR3_Gaps): the end is that of the eleventh iteration, Friday 2026-10-23 06:00 UTC (09:00 Istanbul), which the owner confirmed on 2026-10-19; the start is the time of planning. The end is the owner's own confirmed end date (2026-10-19), accepted for this iteration by the coordinator on 2026-10-20; the owner may move it." % OWNER_WHEN), ", ".join("ex:" + x for x in tk3 + tk4)))
    L.append('ex:PB3G_Iter_12 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 12 when it was planned"@en ; backlog:baselineFor %s ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-23T06:00:00"^^xsd:dateTime .\n' % (ITER, now, now))
    # objectives' movers, ScopeChange and disposition
    L.append("ex:Obj3_Stage3FPass backlog:metricMovableBy ex:ST_Gap_Stage3F .\nex:Obj3_Stage4Pass backlog:metricMovableBy ex:ST_Gap_Stage4 .\n")
    L.append('ex:SC3_Gaps a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the Stage 3.F repair and the Stage 4 page ABox of eight units"@en ;\n    backlog:fulfillsRequest ex:CR3_Gaps ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Gap_Stage3F, ex:ST_Gap_Stage4 ;\n    backlog:hasScopeChangeRationale %s .\n' %
             lit(OWNER_ACT + " The boundary moved outward by two stories because the owner decided that the gaps are closed before the Mission outcome is recorded. It is paid for by running the work inside the twelfth iteration, proposed to end with the eleventh (the end the owner confirmed), by building new files beside the old ones, and by leaving every gate, test and threshold as it stands."))
    t, k = re.subn(r'(ex:CR3_Gaps a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S)
    assert k == 1
    L.append('ex:CR3_Gaps rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Gaps and the stories it admits; it was Pending in the version that recorded the change request, because a ScopeChange must name what it admits. The owner\'s decision of %s (quoted above) is the decision."@en .\n' % (now[:10], OWNER_WHEN))
    t += "\n" + "".join(L)
    return t + out_r2(t, "Backlog", "Out3_ObjectiveR2"), ("third lineage, Backlog stage rebuilt by the stage revision: two stories (Stage 3.F of two Stage 3 documents; the Stage 4 page ABox of eight units, one acceptance criterion per unit) with 20 execution tasks, refinement and planning events into the eleventh iteration, "
                                                      "test cases, the class models and the ScopeChange that admits them; the change request is Accepted; the %d carried items are re-admitted by the rebuilt output, not re-dated." % n)


def ev_fill(t, prev):
    t = fill_re(t, "ex:Out3_BacklogR2", prev)
    return t, "closedAtCommit of the rebuilt Backlog output of the third lineage set to the commit that closed it."


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]),
          "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
