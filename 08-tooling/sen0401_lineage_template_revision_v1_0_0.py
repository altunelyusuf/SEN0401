#!/usr/bin/env python3
"""sen0401_lineage_template_revision v1_0_0 - change route (rulings G104, G125, G127, G133) for the owner's message of 2026-10-21 about the pages built on older templates (pages 8, 10, 11, 12, 14), quoted in OWNER_ACT.
The deliverable (pages rebuilt on the current page template with the same content, and real executable examples with numbers for chapter 8) is new and the third lineage is in its closed Backlog stage, so the route is a
StageRevision from the Scope stage (G127). One call = one new file = one event; the caller validates, checks and commits each alone. Events, in order:
  change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | begin PREV TASK...
(begin = fills the rebuilt Backlog output's commit and records work begun on the named READY Build tasks after the start gate answers READY for the lineage and for each task)
Digests from the framework's own state_digest (table v4, scoped to the third lineage); times from the clock (UTC). Nothing is waived and no recorded digest is rewritten."""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G

lit, esc = G.lit, M.esc
EXEC = G.EXEC; ITER = G.ITER
REV = "ex:Revision_Lineage3_Scope2"
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
WHEN = "Wednesday 2026-10-21 08:12 Istanbul (2026-10-21T05:12:00 UTC)"
QUOTE = ('"Do we have any solutions for older template pages? Do we have work items for these chapters? If they are not matching with the standards how can we say the mission is reached? Is it about a gap in the goals or mission? '
         'If you think it is better to close the current lineage and start a new one for those quality enhancements, we can consider on that. But my current feeling tells me to finish them first before the final closure. What do you say?"')
OWNER_ACT = ("Owner's message of %s, relayed by the course coordinator and recorded by the builder session, quoted: %s He asked what we say; the coordinator and the builder session answered to finish before the closure, which is his own stated lean, "
             "and this plan follows that lean and that recommendation. Under the standing rule that work following the owner's direction is recorded as owner-directed, it is not listed as an open owner confirmation. His earlier direction of 2026-10-19 00:42 Istanbul, quoted: "
             "\"Keep the same standards with all other pages.\" is the origin of the standard written below." % (WHEN, QUOTE))
CLAUSE = G.CLAUSE
DIRECTION = '"Keep the same standards with all other pages."'

# page, label, page version, stored browser-test result of the page as it stands (widgets, features, gates, skipped)
PAGES = [("Ch08", "chapter 8", "08", "9.51.0", 109, 185, 6, 3), ("Ch10", "chapter 10", "10", "9.53.0", 86, 184, 6, 2), ("Ch11", "chapter 11", "11", "9.54.0", 91, 184, 6, 2),
         ("Ch12", "chapter 12", "12", "9.55.0", 86, 185, 6, 0), ("Ch14", "chapter 14", "14", "9.57.0", 68, 185, 6, 0)]
FACTS = ("Measured 2026-10-21 (coordinator; strings re-checked by the builder session in the newest page HTML of each chapter): pages 8, 10, 11, 12 and 14 (page versions 9.51.0, 9.53.0, 9.54.0, 9.55.0, 9.57.0) do not contain the code of the page template 9.50.0/9.51.0 "
         "('const LBLRE=LBL.map' and 'function edVars()' are present in the pages of chapters 1 to 7, 9 and 13 and absent in these five): they lack the label-aware ERD untangle of 9.50.0 (the defect that left 6 labels out on chapter 3 under 9.48) and the faster load of 9.51.0 "
         "(the stability fix for the load-time budget; noisy first runs happened on chapters 11 and 13 and a chapter 11 test hung). Their content matches the decks (pages_deck_match_verify: 0 not carried on all five); the regression (evidence commit 0f7d21f) showed their test counts do not change on 9.51.0. "
         "Page 8 also fails page test 9.34.0 (113 pass, 1 fail, then a crash): no chapter 8 example has a number in its code; chapter 13 solved the same check by research v1_0_2 examples with editable numbers (commit 43886764) and a new inputs maker. The register had no work item for any of this.")
STANDARD = ("The written standard of a page, each element a fact the page can be measured against and none a taste: "
            "(1) template: the page is built from the current page template, 9.51.0, the one the newest pages of chapters 1 to 7, 9 and 13 use; measured by the two code markers 'const LBLRE=LBL.map' and 'function edVars()' present in the page HTML; "
            "(2) content: the page carries the deck's lecture export and stories; measured by pages_deck_match_verify, 0 not carried; "
            "(3) ERD: the relationship labels are shown after Untangle; measured by the existing page test 9.35.0, the feature 'the on-choice labels mode ... Untangle finishes and leaves no more lines through unrelated entities than the grid had', which compares the labels shown after Untangle with the grid (at least 95 percent) - no new test is written, the template carries the fix; "
            "(4) tests: the page tests 9.34.0 and 9.35.0, unchanged, report no failure and counts equal to or better than the stored result of the page as it stands; "
            "(5) Stage 4: the page ABox is rebuilt from the new page as a new file and the Stage 4 gate runner v1_1_0 for the chapter exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS; the Research, Deck and Page chapter checks of the chapter still pass. "
            "NOT part of the standard: the connectedness repair of the T-Box files; the concept-inventory gates (Stage1.C, Stage1.E, Stage3.E, Stage4.L, which the runner reports NOT_MEASURED because the research data holds no concept inventory) and Cross.B/Cross.C; "
            "any change to a gate, a test or a threshold; any change to the content, the decks or the research (except the chapter 8 examples); the owner's open rulings (load-time budget of the page of chapter 6, test-design ruling of chapter 13).")


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def out_new(t, stage, name, consumes):
    return ('\nex:%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage of the third lineage, rebuilt by the stage revision for the pages of older templates"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
            '    backlog:outputOfStage backlog:Stage_%s ;\n    backlog:consumesOutput ex:%s ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (name, stage, stage, consumes, X.digest(t, stage))


INTENT = ('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-21 from the owner\'s message of ' + WHEN + ' (quoted in the change request ex:CR3_Pages) and from his direction of 2026-10-19; the intent origin is therefore Derived. '
          'The owner leaned to finish the work first; he did not review the wording of this element."@en .\n')


def ev_change(t):
    cr = ('\nex:CR3_Pages a backlog:ChangeRequest ;\n    rdfs:label "Rebuild the pages of chapters 8, 10, 11, 12 and 14 on the current page template, and give chapter 8 real examples with numbers, before the Mission is closed"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR_SEN0401 ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % lit(
        OWNER_ACT + " " + FACTS + " The change grows the scope: the third lineage's scope admits the two link passes, the 20 carried tasks and the Stage 3.F and Stage 4 gap closure, and names no page rebuild (its exclusion ex:Excl3_NoRebuild excludes rebuilding a page in order to admit it; this rebuild is not for admission, it is the owner's direction, and the new files stand beside the old ones). "
        "Pending until the ScopeChange that admits the stories is recorded in the Backlog version.")
    ia = ('\nex:IA3_Pages a backlog:ImpactAssessment ;\n    rdfs:label "What rebuilding the five pages and giving chapter 8 its examples costs, measured before it is started"@en ;\n'
          '    backlog:analyzesRequest ex:CR3_Pages ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:CR3_Gaps, ex:CR_SEN0401 ;\n    backlog:hasImpactStatement %s .\n') % lit(
        FACTS + " Answers to the owner's questions, from the register: (1) Do the goals and the Mission cover the standard? They ask for existence (G_PageForEveryDeck: every renewed deck has its interactive page; the Mission outcome: a deck, an interactive page and the sources for each chapter); the five pages exist and pass the chapter check (AC_Chapter). "
        "No goal, objective, criterion or Done story states a template or a uniform standard; the owner's direction of 2026-10-19 \"Keep the same standards with all other pages.\" is recorded only as notes on the stories of the pages of chapters 6 and 13. So it is a gap in the stated standard (goals and criteria), not a contradiction of the Mission. "
        "(2) Route: a standard added after a story is Done does not reach into it (G133); the work is a story of its own (G125); it is a new deliverable, so a StageRevision from the Scope stage (G127), which rebuilds the Scope, Goal, Objective and Backlog stages once and lets a goal for the standard be added in the same revision. "
        "Cost: the earlier Scope revision of this lineage took eight versions to work begun (v0.122 to v0.129); this one takes seven (change, retraction, four stages, work begun). (3) Closing now and a successor taking the work (G125 route 3) costs about ten versions plus the owner's closure act with the gap on record; finishing first costs seven plus the recording of Done and a refreshed caveat, and leaves the Mission outcome unrecorded, which is the owner's stated lean. "
        "What moves: the digests of the Scope, Goal, Objective and Backlog stages of the third lineage move once, when the stages are closed again; the first and second lineages are not touched; no Done story is re-dated or re-opened. "
        "New work, planned in the Backlog version: a story for the five pages with one acceptance criterion per page (G133) and a story for chapter 8 with one criterion, 12 execution tasks (a build and a verify task per page, a build and a verify task for the chapter 8 examples). "
        "Iteration: the work is planned into the twelfth iteration of the third lineage, ex:Iter_12, which ends 2026-10-23T06:00 UTC (09:00 Istanbul), the owner's own confirmed end date; about 48 hours remain. The end does not have to move for the plan to be valid; if a story is still open when the iteration ends, the register shows it as spillover (L4) until the owner rebaselines the iteration or recommits the story, and only the owner decides that. "
        "Risks: the chapter 8 examples are new research content, so the deck of chapter 8 may have to carry them for the page and the deck to stay equal (pages_deck_match_verify); if so that is stated and decided, not hidden; a unit whose gate fails is named failing and is not Done. "
        "Not in the standard: " + STANDARD.split("NOT part of the standard: ")[1] + " Cost of waiting: the Mission outcome stays unrecorded; cost of acting: one change request, one assessment, one stage revision (retraction and four rebuilt stages, one commit each), two stories, 12 tasks. Nothing is waived and no digest is re-recorded outside the revision.")
    return t + cr + ia, "ChangeRequest ex:CR3_Pages (Pending) and ImpactAssessment ex:IA3_Pages for the owner's message of 2026-10-21 08:12 Istanbul on the pages of older templates; no stage changed in this version."


ACTIVE = ["ex:Out3_ScopeR2", "ex:Out3_GoalR2", "ex:Out3_ObjectiveR2", "ex:Out3_BacklogR3"]


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = (OWNER_ACT + " The work adds two deliverables to the scope of the third lineage (pages rebuilt on the current template; chapter 8 examples); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The change request ex:CR3_Pages and the impact assessment ex:IA3_Pages were recorded first, in the previous version. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; they are rebuilt one stage and one commit at a time, each consuming the last unretracted output above it; "
              "the goals, objectives, stories and tasks already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). "
              "The revision is recorded as decided by the builder role: the route is what the owner's direction needs; the stage revision itself he did not decide.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the pages of older templates are rebuilt before the Mission outcome is recorded"@en ;\n'
         '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso ex:CR3_Pages, ex:IA3_Pages ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the pages of older templates: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Area3_PageTemplate a backlog:ScopeArea ;
    rdfs:label "The pages of chapters built on older page templates"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "03-materials: the page folders of chapters 8, 10, 11, 12 and 14 (the pages, the page ABoxes) and the research folder of chapter 8; the page builder and the Stage 4 builder in 08-tooling" ;
    backlog:areaMeasure "14 chapter pages of which 9 carry the code of the page template 9.51.0 today; after the work all 14 do" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_PageTemplate a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 8, 10, 11, 12 and 14 are rebuilt on the current page template with the same content, the tests unchanged"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_PageTemplate ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_Ch08Examples a backlog:ScopeDeliverable ;
    rdfs:label "Chapter 8 has real executable examples with numbers, so its page passes page test 9.34.0"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_PageTemplate ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Excl3_NoConceptGates a backlog:ScopeExclusion ;
    rdfs:label "The page standard does not include the connectedness repair, the concept-inventory gates, or any change to a gate, a test or a threshold"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:excludesConcern %s ;
    backlog:hasExclusionRationale "A standard made of facts the pages can be measured against stays measurable only if the measures are not changed to fit; the concept-inventory gates report NOT_MEASURED for every unit because the research holds no inventory, which is a research-design matter the owner has not asked for; the connectedness repair was deferred by the owner on 2026-10-20 09:19 Istanbul." ;
    backlog:decidedBy backlog:Owner ; backlog:hasScopeLayer backlog:Layer_Work .
ex:Scope3 backlog:requiresDeliverable ex:Del3_PageTemplate, ex:Del3_Ch08Examples ;
    backlog:coversArea ex:Area3_PageTemplate ; backlog:hasScopeExclusion ex:Excl3_NoConceptGates ;
    rdfs:seeAlso ex:CR3_Pages, ex:IA3_Pages .
ex:Scope3 rdfs:comment %s@en .
''' % (CLAUSE, lit("The pages of chapters 8, 10, 11, 12 and 14 rebuilt as new files on the page template 9.51.0 with the same content (the deck's lecture export and stories), the page tests 9.34.0 and 9.35.0 unchanged and reporting counts equal to or better than the stored result of each page, a Stage 4 page ABox rebuilt from each new page that passes the Stage 4 gate run. " + STANDARD),
       CLAUSE, lit("A new version of the chapter 8 research with real executable examples that have numbers in their code (editable inputs), following chapter 13 (research v1_0_2, commit 43886764, and an inputs maker); the chapter 8 Stage 3.F and Stage 4 gates re-run clean, the Research, Deck and Page chapter checks pass, and the chapter 8 page passes page test 9.34.0 (now 113 pass, 1 fail, then a crash); no test or gate is changed. " + FACTS),
       lit("Anything that changes a gate, a test or a threshold in order to make a page pass; the connectedness repair of the T-Box files (deferred by the owner on 2026-10-20 09:19 Istanbul); the concept-inventory gates Stage1.C, Stage1.E, Stage3.E, Stage4.L and Cross.B/Cross.C, which the runner reports NOT_MEASURED or CANNOT_RUN; a change of content, decks or research other than the chapter 8 examples; the owner's open rulings (load-time budget of the page of chapter 6, test-design ruling of chapter 13); recording the Mission outcome and the Achieved status of this lineage, which wait for the owner's act."),
       lit("Revised 2026-10-21 by the stage revision ex:Revision_Lineage3_Scope2 on the owner's message of %s (quoted in the change request ex:CR3_Pages). The statement above is unchanged (L-112). It now also requires ex:Del3_PageTemplate and ex:Del3_Ch08Examples, covers the area ex:Area3_PageTemplate and carries the exclusion ex:Excl3_NoConceptGates. The exclusion ex:Excl3_NoRebuild stands: it excludes rebuilding in order to admit; these rebuilds are the owner's direction and are new files beside the old ones." % WHEN))]
    t += "".join(L)
    return t + out_new(t, "Scope", "Out3_ScopeR3", "Out3_Mission"), \
        "third lineage, Scope stage rebuilt by the stage revision for the pages of older templates: two deliverables (pages rebuilt on the current template; chapter 8 examples), their area and an exclusion (no connectedness repair, no concept-inventory gates, no gate, test or threshold changed)."


# ------------------------------------------------------------------------------------------------ goal
GOALS = [("G3_PagesSameStandard", "Every chapter page meets the same written standard as the others", "Facing_Mission", ""),
         ("G3_Ch08ExamplesRun", "The examples of chapter 8 have numbers and run", "Facing_Scope", ""),
         ("G3_StandardNotMoved", "The standard is met without changing a gate, a test or a threshold and without the concept-inventory gates", "Facing_Exclusion", "\n    backlog:guardsExclusion ex:Excl3_NoConceptGates ;")]


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR3", prev); t = X.set_status(t, "LS_Goaled")
    L = []
    for i, label, f, g in GOALS:
        L.append('\nex:%s a backlog:Goal ;\n    rdfs:label "%s"@en ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_PageTemplate ;\n'
                 '    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:%s ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;%s\n'
                 '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n'
                 '    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR3 .\n' % (
                     i, label, f, g, lit("Derived from the revised scope of the third lineage (ex:Del3_PageTemplate, ex:Del3_Ch08Examples, ex:Excl3_NoConceptGates), from the owner's direction of 2026-10-19, quoted: %s and from his message of %s (quoted in ex:CR3_Pages): the Mission asks for a page for every chapter, and the owner's standard is that all pages are alike in what they are checked against." % (DIRECTION, WHEN))))
    L.append("".join(INTENT % i for i, *_ in GOALS))
    for k, goal, what, ctx, text in (
            ("T", "G3_PagesSameStandard", "a page meets the written standard", "the five checks of the written standard (template markers, pages_deck_match_verify, the page tests 9.34.0 and 9.35.0, the Stage 4 gate runner and the chapter checks)", STANDARD),
            ("C8", "G3_Ch08ExamplesRun", "the chapter 8 examples have numbers and run", "the page test 9.34.0 on the chapter 8 page, the Stage 4 gate runner for 08 and the chapter checks of chapter 8",
             "Every chapter 8 example has a number in its code that the reader can edit, as chapter 13's do after research v1_0_2; the page test 9.34.0 reports no failure and no crash on the chapter 8 page; no test or gate is changed.")):
        L.append('''
ex:Spec3T_%(k)s a backlog:Specification ;
    rdfs:label "What it is for %(what)s"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:%(g)s ;
    backlog:hasSpecificationText %(text)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR3 .
ex:Scen3T_%(k)s_Passes a backlog:TestScenario ; rdfs:label "A page's checks report the standard met (%(k)s)"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3T_%(k)s ;
    backlog:hasScenarioText "Given the newest files of a page in the course repository, when %(ctx)s are run, then they report no failure and the run exits 0." .
ex:Scen3T_%(k)s_NotClaimed a backlog:TestScenario ; rdfs:label "A page that does not meet the standard is not claimed as meeting it (%(k)s)"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3T_%(k)s ;
    backlog:hasScenarioText "Given a page for which a check fails or stops, when the story is to be recorded Done, then the criterion of that page has no passing result and the story is not Done; the page is named with the failing check." .
''' % dict(k=k, g=goal, what=esc(what), ctx=esc(ctx), text=lit(text)))
    L.append('''
ex:Model3T_UseCase a backlog:ModelArtifact ; rdfs:label "Who uses the rebuilt pages and their standard"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_UseCaseDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A student opens the page of a chapter on any device and meets the same navigation, the same ERD with its relationship labels and the same fast load as on every other chapter; the instructor teaches from the page and the deck, which carry the same content; a work agent rebuilds a page on the current template and runs the page tests, the deck match check and the Stage 4 gates without changing them; the evidence bridge verifies the runs; the owner reads the register to see which pages meet the standard before the Mission outcome is recorded." ;
    backlog:describesItem ex:G3_PagesSameStandard .
''')
    t += "".join(L)
    return t + out_new(t, "Goal", "Out3_GoalR3", "Out3_ScopeR3"), "third lineage, Goal stage rebuilt for the pages of older templates: goals for the same standard, the chapter 8 examples and the unmoved standard; two specifications (the written standard, the chapter 8 examples) with a nominal and a rejection scenario each; the use case model."


# ------------------------------------------------------------------------------------------------ objective
OBJS = [("Obj3_PagesOnTemplate", "G3_PagesSameStandard", "Met3_PagesOnTemplate", "chapter pages (of 14) that carry the code of the page template 9.51.0", 9, 14, "Dir_Increase",
         "Baseline measured 2026-10-21 by the code markers 'const LBLRE=LBL.map' and 'function edVars()' in the newest page HTML of each chapter: present in chapters 1 to 7, 9 and 13, absent in 8, 10, 11, 12 and 14: 9 of 14."),
        ("Obj3_Ch08Page34", "G3_Ch08ExamplesRun", "Met3_Ch08Page34", "failing checks of page test 9.34.0 on the chapter 8 page", 1, 0, "Dir_Decrease",
         "Baseline reported by the coordinator on 2026-10-21: page test 9.34.0 on the chapter 8 page, 113 pass, 1 fail (no chapter 8 example has a number in its code), then a crash: 1 failing check.")]


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR3", prev); t = X.set_status(t, "LS_Objectived")
    now = M.now(); L = []
    for i, g, m, what, b, tg, d, basis in OBJS:
        L.append('''
ex:%(i)s a backlog:Objective ; rdfs:label "%(Wh)s: from %(b)d to %(tg)d"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:%(g)s ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from the course repository and from this register after the evidence bridge has run the checks." ;
    backlog:hasBaselineValue "%(b)d"^^xsd:decimal ; backlog:hasTargetValue "%(tg)d"^^xsd:decimal ; backlog:hasTargetDirection backlog:%(d)s ;
    backlog:hasCheckpoint ex:CP3T_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR3 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3T_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the stories of the pages are recorded"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of every page named by the criteria, so the count is read from verified runs." ;
    backlog:expectedValue "%(tg)d"^^xsd:decimal .
ex:Obs39_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the pages"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "%(b)d"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "%(basis)s" .
''' % dict(i=i, g=g, m=m, what=esc(what), Wh=esc(what[0].upper() + what[1:]), b=b, tg=tg, d=d, now=now, basis=esc(basis)))
    L.append("".join(INTENT % i for i, *_ in OBJS))
    L.append('''
ex:Model3T_Activity a backlog:ModelArtifact ; rdfs:label "How one page is rebuilt on the current template"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ActivityDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "Per page, in order: read the page's data and the deck's lecture export; build the page as a new file on the current template with the page builder, never editing a committed file; run the page tests 9.34.0 and 9.35.0 unchanged and compare the counts with the stored result of the page as it stands - BRANCH: a failing check leaves the page failing and it is named; build the Stage 4 page ABox from the new page and run the Stage 4 gate runner; run the deck match check and the chapter checks; record the runs against the page's criterion; the evidence bridge verifies the runs and the file hashes." ;
    backlog:describesItem ex:Obj3_PagesOnTemplate .
ex:Model3T_Class a backlog:ModelArtifact ; rdfs:label "How a page story, its criteria and its evidence are stored"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Analysis ;
    backlog:declaresState "A Story (the pages rebuilt; the chapter 8 examples) is planned into the twelfth iteration by a PlanningEvent that produces its ExecutionTasks (a build and a verify task per page). It has an AcceptanceCriterion per page, each covered by a TestCase of the nominal and of the rejection scenario. Done is recorded only with a TestHarness, a TestEvidence per check that passed and an ArtifactEvidence per new file (path and SHA-256); a page whose check fails is named in the story and carries no test evidence." ;
    backlog:describesItem ex:Obj3_PagesOnTemplate .
ex:Model3T_ClassDesign a backlog:ModelArtifact ; rdfs:label "Design of the stored page story, its harness and its evidence"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasModelKind backlog:Kind_ClassDiagram ; backlog:hasModelLevel backlog:Level_Design ;
    backlog:declaresState "Classes: Story (identifier, title, state, startedAt, finishedAt, lastAuditedAt, executionModality, admittedByOutput, memberOfContainer) with associations to AcceptanceCriterion (one per page; coveredByCase), ExecutionTask (decomposesInto; dependsOn between a verify task and its build task and, for chapter 8, the examples build task), PlanningEvent (plansItem, plannedInto, producesTask), RefinementEvent (refines, addressesConcern), TestHarness (harnessFor the story), TestEvidence and ArtifactEvidence (attestsCriterion, evidenceVerified, verifiedAt); a StageOutput (hasStateDigest, closedAtCommit) admits the story." ;
    backlog:describesItem ex:Obj3_Ch08Page34 .
''')
    t += "".join(L)
    return t + out_new(t, "Objective", "Out3_ObjectiveR3", "Out3_GoalR3"), "third lineage, Objective stage rebuilt for the pages of older templates: objectives (pages on the current template 9 to 14; failing checks of page test 9.34.0 on chapter 8, 1 to 0) with metric, checkpoint and a baseline reading of 2026-10-21; the activity and class models."


# ------------------------------------------------------------------------------------------------ backlog
def gh_page(nm, label, num, pv, w, f, g, sk):
    return ("Owner's direction of 2026-10-19: \"Keep the same standards with all other pages.\" Given the page of %s as it stands (page %s) and the newest pages of chapters 1 to 7, 9 and 13, when the page is rebuilt as a new file on the page template 9.51.0 with the same content and checked, then ALL of: "
            "(1) template: the page HTML contains 'const LBLRE=LBL.map' and 'function edVars()'; (2) content: pages_deck_match_verify reports 0 not carried for the page; "
            "(3) ERD: the page test 9.35.0 feature on the labels shown after Untangle reports pass (labels shown after Untangle at least 95 percent of the grid's), measured by the existing test, no new test; "
            "(4) tests: the page tests 9.34.0 and 9.35.0, unchanged, report no failure and counts equal to or better than the stored result of the page as it stands (%d widgets, %d features, %d gates, %d skipped%s); "
            "(5) Stage 4: the page ABox is rebuilt from the new page as a new file and the Stage 4 gate runner v1_1_0 for %s exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks of the chapter pass; "
            "gates the runner reports as NOT_MEASURED or CANNOT_RUN are reported as such and not claimed; no gate, test or threshold changed; if any element fails the page is named failing and this criterion has no passing result."
            % (label, pv, w, f, g, sk, "; the page test 9.34.0 also reports no failure, which the chapter 8 criterion owes" if nm == "Ch08" else "", num))


def gh_ch08():
    return ("Given the chapter 8 research and its page (page 9.51.0 fails page test 9.34.0: 113 pass, 1 fail, then a crash, because no chapter 8 example has a number in its code), when a new version of the chapter 8 research gives its examples real executable code with numbers the reader can edit "
            "(following chapter 13: research v1_0_2, commit 43886764, and an inputs maker) and the page is rebuilt from it, then the page test 9.34.0, unchanged, reports no failure and no crash on the chapter 8 page; the Stage 4 gate runner for 08 reports Stage3.F and Stage4.A, B, cov, sub and src PASS; "
            "the Research, Deck and Page chapter checks of chapter 8 pass; no test, gate or threshold is changed and no citation or claim is removed only to pass; if any fails the unit is named failing and this criterion has no passing result.")


def task_block(tid, title, ttype, note, deps=()):
    return G.task_block(tid, title, ttype, note, deps).replace("ex:Out3_BacklogR2", "ex:Out3_BacklogR4")


def story_block(sid, title, want, sothat, deliv, obj, cat, criteria, tasks, note):
    return G.story_block(sid, title, want, sothat, deliv, obj, cat, criteria, tasks, note).replace("ex:Out3_BacklogR2", "ex:Out3_BacklogR4").replace(
        "Not scored: the owner decided on 2026-10-20 10:42 Istanbul that the gaps are closed first, so there is no ranking left to compute.", "Not scored: the owner's lean of 2026-10-21 08:12 Istanbul is to finish this before the closure, so there is no ranking left to compute.")


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR3", prev); t = X.set_status(t, "LS_Backlogged")
    now = M.now()
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR3 ;")
    assert n >= 40, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR3 ;", "backlog:admittedByOutput ex:Out3_BacklogR4 ;")
    L = []; crit, tk = [], []
    for nm, label, num, pv, w, f, g, sk in PAGES:
        c = "AC3T_" + nm; crit.append(c)
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:satisfiedByArtifact "the page, its Stage 4 page ABox and the stored page-test results as new files cited by SHA-256, and the runs of the template markers, the deck match check, the page tests, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3T_T_Passes, ex:TC3T_T_NotClaimed .\n'
                 % (c, lit("The page of %s is built on the current template and meets the written standard" % label), lit(gh_page(nm, label, num, pv, w, f, g, sk))))
        b, v = "TK_PageTpl_%s_Build" % nm, "TK_PageTpl_%s_Verify" % nm; tk += [b, v]
        L.append(task_block(b, "Rebuild the page of %s on the current template" % label, "Build",
                            "Build the page of %s as a new file with a new page version, on the page template 9.51.0, with the page builder that produced the pages of chapters 1 to 7, 9 and 13, from the chapter's existing page data, the deck's lecture export and stories (same content), and its stored objectives and quiz; run the page tests 9.34.0 and 9.35.0 unchanged and store the result; build the Stage 4 page ABox from the new page with the Stage 4 builder (a new file). "
                            "A committed file is not edited. No test, gate or threshold is changed.%s Satisfies the criterion ex:%s." % (label, " This page waits for the chapter 8 examples (TK_Ch08Ex_Build): its page test 9.34.0 must pass." if nm == "Ch08" else "", c),
                            ("TK_Ch08Ex_Build",) if nm == "Ch08" else ()))
        L.append(task_block(v, "Verify the page of %s on the current template" % label, "Verify",
                            "Check the template markers in the page HTML, run pages_deck_match_verify for the chapter, the page tests 9.34.0 and 9.35.0 (compare the counts with the stored result of the page as it stood: %d widgets, %d features, %d gates, %d skipped), the Stage 4 gate runner v1_1_0 for %s and the Research, Deck and Page chapter checks; record every result as reported (PASS, FAIL, NOT_MEASURED, CANNOT_RUN). Criterion ex:%s." % (w, f, g, sk, num, c), (b,)))
    c8 = "AC3T_Ch08_Examples"
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:satisfiedByArtifact "the new chapter 8 research and page files cited by SHA-256, and the runs of the page test 9.34.0, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3T_C8_Passes, ex:TC3T_C8_NotClaimed .\n' % (c8, lit("Chapter 8 has real executable examples with numbers and its page passes page test 9.34.0"), lit(gh_ch08())))
    L.append(task_block("TK_Ch08Ex_Build", "Give chapter 8 real executable examples with numbers", "Build",
                        "Write a new version of the chapter 8 research (and the document and page data that follow it) whose examples are real executable code with numbers the reader can edit, as chapter 13 did (research v1_0_2, commit 43886764, and an inputs maker, 08-tooling/ch08-page/inputs_make_v1_0_0.py exists for chapter 8 and is to be checked first). "
                        "A committed file is not edited. No test, gate or threshold is changed; no citation or claim is removed only to pass. If the deck of chapter 8 has to carry the new examples for the page and the deck to stay equal (pages_deck_match_verify), that is stated and put to the coordinator, not done silently. Satisfies the criterion ex:%s." % c8))
    L.append(task_block("TK_Ch08Ex_Verify", "Verify the chapter 8 examples and page test 9.34.0", "Verify",
                        "Run Stage 3.F and the Stage 4 gate runner v1_1_0 for 08, the Research, Deck and Page chapter checks of chapter 8 and the page test 9.34.0 on the rebuilt page; record every result as reported. Criterion ex:%s." % c8, ("TK_Ch08Ex_Build", "TK_PageTpl_Ch08_Build")))
    tk += ["TK_Ch08Ex_Build", "TK_Ch08Ex_Verify"]
    tkp = [x for x in tk if x.startswith("TK_PageTpl")]
    note_o = "Created by the stage revision ex:Revision_Lineage3_Scope2 on the owner's message of %s (quoted in ex:CR3_Pages), which follows his stated lean. " % WHEN
    L.append(story_block("ST_Page_Template", "The pages of chapters 8, 10, 11, 12 and 14 are rebuilt on the current page template and meet the written standard",
                         "the pages of chapters 8, 10, 11, 12 and 14 built on the current page template with the same content", "every page of the course loads, navigates and shows its ERD labels the same way, so a student meets one standard on every chapter",
                         "Del3_PageTemplate", "Obj3_PagesOnTemplate", "Cat_Compliance", crit, tkp,
                         note_o + "One criterion per page (G133). " + STANDARD))
    L.append(story_block("ST_Ch08_Examples", "Chapter 8 has real executable examples with numbers",
                         "the examples of chapter 8 to be real executable code with numbers the reader can edit", "the page of chapter 8 passes the page test every other page passes, and its examples teach by being run and changed",
                         "Del3_Ch08Examples", "Obj3_Ch08Page34", "Cat_NewCapability", [c8], ["TK_Ch08Ex_Build", "TK_Ch08Ex_Verify"],
                         note_o + FACTS))
    for k, nm, crits in (("T", "page standard", crit), ("C8", "chapter 8 example", [c8])):
        L.append('''
ex:TC3T_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the %(nm)s checks on a page whose files pass and require no failure"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3T_%(k)s_Passes ; backlog:runsOnData ex:Data3T_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files of a page; they report no failure and exit 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3T_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the %(nm)s checks on a page whose files fail and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3T_%(k)s_NotClaimed ; backlog:runsOnData ex:Data3T_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks over a page for which one fails (for example the page of chapter 8 under page test 9.34.0, measured 2026-10-21); the page carries no verified test evidence for the criterion and the story names it failing." .
ex:Data3T_%(k)s_Passing a backlog:TestData ; rdfs:label "A page whose %(nm)s checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest files of a page for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3T_%(k)s_Failing a backlog:TestData ; rdfs:label "A page whose %(nm)s checks fail when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The files of a page for which a check reports FAIL or stops, as measured on 2026-10-21 for the pages named in the criteria." .
''' % dict(k=k, nm=nm, cr=", ".join("ex:" + c for c in crits)))
    prod = {"ST_Page_Template": (tkp, ["Spec3T_T", "Scen3T_T_Passes", "Scen3T_T_NotClaimed", "Model3T_Class", "Model3T_ClassDesign", "Model3T_Activity"]),
            "ST_Ch08_Examples": (["TK_Ch08Ex_Build", "TK_Ch08Ex_Verify"], ["Spec3T_C8", "Scen3T_C8_Passes", "Scen3T_C8_NotClaimed"])}
    for s, (tks, pr) in prod.items():
        for x in [s] + tks:
            L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the owner\'s message of %s (quoted in ex:CR3_Pages) and from the facts in ex:IA3_Pages; the criterion and the task text name the checks, the page and what a passing result is." .\n'
                     % (x, x, x, now, ITER, WHEN))
        L.append('ex:Plan3T_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 12"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces %s .\n'
                 % (s, s, now, ITER, s, ", ".join("ex:" + x for x in tks), ", ".join("ex:" + x for x in pr)))
    allnew = ["ST_Page_Template", "ST_Ch08_Examples"] + tk
    L.append("ex:Iter_12 backlog:hasMember %s .\n" % ", ".join("ex:" + x for x in allnew))
    L.append('ex:Iter_12 rdfs:comment %s@en .\n' % lit("Extended on %s by the stage revision ex:Revision_Lineage3_Scope2: the stories ST_Page_Template and ST_Ch08_Examples and their %d tasks are planned into this iteration, which still ends at the owner's own confirmed 2026-10-23T06:00 UTC (09:00 Istanbul); nothing about the end or the plan baseline is changed. If a story is open at the end, the register shows spillover (L4) until the owner rebaselines or recommits; only the owner decides that." % (now[:10], len(tk))))
    L.append("ex:Obj3_PagesOnTemplate backlog:metricMovableBy ex:ST_Page_Template .\nex:Obj3_Ch08Page34 backlog:metricMovableBy ex:ST_Ch08_Examples .\n")
    L.append('ex:SC3_Pages a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the pages rebuilt on the current template and the chapter 8 examples"@en ;\n    backlog:fulfillsRequest ex:CR3_Pages ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:ST_Page_Template, ex:ST_Ch08_Examples ;\n    backlog:hasScopeChangeRationale %s .\n' %
             lit(OWNER_ACT + " The boundary moved outward by two stories because the owner leaned to finish this before the Mission outcome is recorded. It is paid for by running the work inside the twelfth iteration, which ends at the owner's own confirmed date, by building new files beside the old ones, and by leaving every gate, test and threshold as it stands."))
    t, k = re.subn(r'(ex:CR3_Pages a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
    L.append('ex:CR3_Pages rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Pages and the stories it admits; it was Pending before. The owner\'s message of %s is the direction, and his stated lean to finish first is the decision."@en .\n' % (now[:10], WHEN))
    # the Iter_12 sprint goal names the new work
    i, j = blk(t, "Iter_12"); b = t[i:j]
    m = re.search(r'(backlog:hasSprintGoal ")([^"]*)(")', b); assert m
    b = b.replace(m.group(0), m.group(1) + m.group(2) + " Then (added 2026-10-21 on the owner's message): the pages of chapters 8, 10, 11, 12 and 14 are rebuilt on the current page template and meet the written standard, and chapter 8 has real examples with numbers, each unit that fails named." + m.group(3), 1)
    t = t[:i] + b + t[j:]
    t += "\n" + "".join(L)
    return t + out_new(t, "Backlog", "Out3_BacklogR4", "Out3_ObjectiveR3"), ("third lineage, Backlog stage rebuilt for the pages of older templates: two stories (the five pages with one criterion per page; chapter 8 examples) with 12 tasks, refinement and planning events into the twelfth iteration, test cases and the ScopeChange that admits them; "
                                                                           "the change request is Accepted; the %d carried items are re-admitted by the rebuilt output, not re-dated." % n)


# ------------------------------------------------------------------------------------------------ begin
def ev_begin(t, prev, tasks):
    t = G.fill_re(t, "ex:Out3_BacklogR4", prev)
    tmp = M.newest() + ".gate.tmp"; open(tmp, "w").write(t)
    try:
        for k in tasks:
            r = subprocess.run([sys.executable, GATE, tmp, "--lineage", "Lineage3", "--item", k], capture_output=True, text=True)
            assert "VERDICT     : READY" in r.stdout, k + " " + r.stdout[-400:]
    finally:
        os.remove(tmp)
    now = M.now()
    parents = set()
    for k in tasks:
        i, j = blk(t, k); b = t[i:j]; assert "hasState backlog:Ready" in b and "startedAt" not in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        parents.add("ST_Ch08_Examples" if "Ch08Ex" in k else "ST_Page_Template")
    for s in parents:
        i, j = blk(t, s); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b, s
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
    t = X.set_status(t, "LS_InProgress")
    print("STARTED", now)
    return t, "closedAtCommit of the rebuilt Backlog output ex:Out3_BacklogR4 filled; work begun at %s UTC (start gate READY for the lineage and for each task) on %s; the stories and the lineage are InProgress." % (now, ", ".join(tasks))


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]),
          "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "begin": lambda: ev_begin(t, sys.argv[2], sys.argv[3:])}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev]()
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
