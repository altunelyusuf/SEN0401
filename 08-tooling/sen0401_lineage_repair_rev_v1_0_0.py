#!/usr/bin/env python3
"""sen0401_lineage_repair_rev v1_0_0 - change route (rulings G125, G127, G133, G136) for the story-chip defect found on the chapter 5 page 9.80.0 (story GoxColdFind lands at 2064 px outside the 768 px viewport; the click handler of
template 9.52.0 scrolls before the pane is fitted). Events, one new file each: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV.
The StageRevision from the Scope stage is the same route as ex:CR3_Remedy56 (sen0401_lineage_remedy56_rev_v1_0_0, whose helpers are reused). New items: template 9.52.1 (a new file), and the rebuild of the chapter 5 and chapter 6 pages on it, as new stories
(the Done page story of chapter 6 is not edited, G125; the chapter 5 page task, whose criterion names template 9.52.0 and cannot be met, is suspended). Work begun is recorded at the real start of each executor session."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_remedy56_rev_v1_0_0 as RV
lit, esc = G.lit, M.esc
ITER = "ex:Iter_18"; REV = "ex:Revision_Lineage3_Scope6"; CR = "ex:CR3_ChipScroll"; IA = "ex:IA3_ChipScroll"
ACTIVE = ["ex:Out3_ScopeR6", "ex:Out3_GoalR6", "ex:Out3_ObjectiveR6", "ex:Out3_BacklogR8"]; NEWB = "ex:Out3_BacklogR9"; OLDB = "ex:Out3_BacklogR8"
RV.ITER = ITER; RV.NEWB = NEWB
WHEN = "Friday 2026-10-23, relayed by the course coordinator (the owner's standing direction of Thursday 2026-10-22 17:30 Istanbul: remedy the weaknesses and deliver the chapter 5 and 6 pages ready to use)"
FACT = ("MEASURED FACTS. The executor SEN0401-I17-page-ch05 reported the chapter 5 page 9.80.0 (commits c4002e1 to 0fb29ca, template 9.52.0, builders v4_15_0 and v2_24_0): the page tests 9.36.0, 9.35.1 and 9.34.1 each fail exactly one feature, 'a story chip on a concept opens that story in the Stories tab' (detail: story GoxColdFind, which lands at 2064 px, outside the 768 px viewport). "
        "Its diagnosis (confirmed by the builder session by reading template 9.52.0): the click handler of the story chips (the listener on the panes, button[data-story]) calls showTab('stories') and then scrollIntoView on the story at once; the pane height is fitted afterwards, so the scroll position is lost. "
        "The chapter 6 page 9.81.0 (executor SEN0401-I17-page-ch06, commits faf1b10 to ca2e510) passes all three tests, but it carries the same handler: the page tests click the first chip of the first concept that has one, and in chapter 6 that chip is the first story, which sits at the top of the pane and needs no scroll. "
        "So the defect is in template 9.52.0 and is latent in the chapter 6 page; the builder session re-ran the page tests on both pages on 2026-10-23 (results in the control version).")
STD1 = ("PAGE FEATURE (existing, from the page test 9.35.1 and kept in 9.36.0 and 9.34.1): a story chip on a concept opens that story in the Stories tab: after the click the Stories pane is visible and the story card is inside the viewport.")
VER = ("page template 9.52.1 (new file over 9.52.0, which stays byte-identical); page builder v4_15_0 and page-data builder v2_24_0 (unchanged; the template is passed by PAGE_TEMPLATE, a builder v4_16_0 only if the default must change); page test 9.36.0 (Playwright 1.56.0); page tests 9.34.1 and 9.35.1; "
       "Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_3_0; Playwright 1.56.0")
COMMON = RV.COMMON
STORIES = [("ST_Repair_Template", "The page template 9.52.1 scrolls a story into view after the pane is fitted, as a new file", "Del3_ChipScrollTemplate", "Obj3_ChipScroll", ["AC5R_Template"], ["TK_Repair_Template", "TK_Repair_Template_Verify"]),
           ("ST_Repair_Page_Ch05", "The page of chapter 5 is rebuilt on template 9.52.1 and every story chip opens its story in view", "Del3_ChipScrollPages", "Obj3_ChipScroll", ["AC5R_Page_Ch05"], ["TK_Repair_Page_Ch05_Build", "TK_Repair_Page_Ch05_Verify"]),
           ("ST_Repair_Page_Ch06", "The page of chapter 6 is rebuilt on template 9.52.1 and every story chip opens its story in view", "Del3_ChipScrollPages", "Obj3_ChipScroll", ["AC5R_Page_Ch06"], ["TK_Repair_Page_Ch06_Build", "TK_Repair_Page_Ch06_Verify"])]
def pagenote(nn):
    ch = nn.lstrip("0"); old = {"05": "9.80.0 (not delivered as ready: one failed feature)", "06": "9.81.0 (passes, with the latent defect)"}[nn]
    return ("Build the page of chapter %s again as a NEW file with a NEW page version (higher than the page %s) on the template 9.52.1 (course_page_template_v9_52_1.html, built by TK_Repair_Template; pass it with PAGE_TEMPLATE) with the page builder v4_15_0 and the page-data builder v2_24_0, from the same inputs as the earlier page "
            "(the deck's lecture export and stories, the chapter-code manifest chapter_code_ch%s_v1_1_0.json, the pywheels file). Everything of the earlier build stays valid; the change is the template. " % (ch, old, nn) +
            "Run the page tests 9.36.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST), serially, store the result as a new test_results file, and build the Stage 4 page ABox with the Stage 4 builder. " + FACT + " " + RV.STD_P + " " + RV.DOMC + " " + COMMON)
TASKS = [("TK_Repair_Template", "Make page template 9.52.1: the story chip scrolls its story into view after the pane is fitted", "Build", [], "SEN0401-I18-template", "T0", 1.0,
          "Write the NEW file 08-tooling/course_page_template_v9_52_1.html from course_page_template_v9_52_0.html (which stays byte-identical). The defect (from the control of the chapter 5 page 9.80.0, register v0.205.0): " + FACT + " "
          "THE CHANGE: in the click listener of the panes, run the scroll of the story after the pane height has been fitted (the template fits pane heights after showTab; defer the scroll until that fit is done, for example by calling it from the fit routine's completion or after two animation frames), and keep the highlight. "
          "Change nothing else: every id, hook, behaviour and the DOM contract of 9.52.0 stay (the unified diff against 9.52.0 must show only that handler and the version marker). If the builder's default template name has to change, write sen0401_page_build_v4_16_0.py as a new file over v4_15_0; otherwise leave the builders alone and name PAGE_TEMPLATE. "
          "PROOF to deliver and keep as logs: (1) the unified diff; (2) a scratch page of chapter 5 built on 9.52.1 (page data from the repository, outside the repository folders) passes the story-chip feature of the page test 9.35.1 for the story that failed (GoxColdFind), and the page tests 9.36.0 and 9.35.1 on it report no failure; "
          "(3) scratch pages of chapters 1 and 10 on 9.52.1 pass page test 9.36.0 P1, P3, P4, P5, P6, P8, P9 as they did on 9.52.0; (4) 9.52.0 is byte-identical (SHA-256 before and after). " + STD1 + " " + COMMON),
         ("TK_Repair_Template_Verify", "Verify page template 9.52.1 on the evidence bridge", "Verify", ["TK_Repair_Template"], "builder", "T0+1.5h", 0.7,
          "Re-run on the bridge: the old files byte-identical, the diff of 9.52.1 over 9.52.0 limited to the story-chip handler and the version marker, the DOM contract tokens and every id of 9.52.0 present, scratch pages of chapters 1, 5 and 10 built on 9.52.1 by the builder session and the page tests run serially; record every result as printed."),
         ("TK_Repair_Page_Ch05_Build", "Rebuild the page of chapter 5 on template 9.52.1", "Build", ["TK_Repair_Template", "TK_Repair_Template_Verify"], "SEN0401-I18-page-ch05", "T0+2.2h", 2.0, pagenote("05")),
         ("TK_Repair_Page_Ch05_Verify", "Verify the rebuilt page of chapter 5", "Verify", ["TK_Repair_Page_Ch05_Build"], "builder", "T0+4.5h", 1.0,
          "Re-run serially the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check, the link check and the manifest equality; record every result as printed."),
         ("TK_Repair_Page_Ch06_Build", "Rebuild the page of chapter 6 on template 9.52.1", "Build", ["TK_Repair_Template", "TK_Repair_Template_Verify"], "SEN0401-I18-page-ch06", "T0+2.2h", 2.0, pagenote("06")),
         ("TK_Repair_Page_Ch06_Verify", "Verify the rebuilt page of chapter 6", "Verify", ["TK_Repair_Page_Ch06_Build"], "builder", "T0+5.0h", 1.0,
          "Re-run serially the page tests 9.36.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check, the link check and the manifest equality; record every result as printed.")]
LAB = {"AC5R_Template": "The page template 9.52.1 is a new file that scrolls a story into view after the pane is fitted and changes nothing else",
       "AC5R_Page_Ch05": "The page of chapter 5 rebuilt on template 9.52.1 passes all three page tests, story chip included", "AC5R_Page_Ch06": "The page of chapter 6 rebuilt on template 9.52.1 passes all three page tests"}
def gh(c):
    if c == "AC5R_Template":
        return ("Owner-directed work (ex:CR3_ChipScroll). Given the template 9.52.0 (byte-identical after the task) and the defect measured on the chapter 5 page 9.80.0, when the NEW file course_page_template_v9_52_1.html is written, then ALL of: (1) the file is new and 9.52.0 is byte-identical; (2) the unified diff of 9.52.1 over 9.52.0 shows only the story-chip click handler and the version marker, and every id and hook of 9.52.0 and the DOM contract are present; "
                "(3) a scratch page of chapter 5 built on 9.52.1 with the builders v4_15_0 and v2_24_0 (PAGE_TEMPLATE) passes the feature 'a story chip on a concept opens that story in the Stories tab' of the page tests 9.35.1 and 9.36.0 for the story GoxColdFind and the tests report no failure; (4) scratch pages of chapters 1 and 10 on 9.52.1 pass page test 9.36.0 P1, P3, P4, P5, P6, P8, P9; "
                "(5) no committed file is edited, no gate, test or threshold changed; results as printed; if any element fails the template is named failing. " + FACT + " " + STD1)
    nn = c[-2:]; ch = nn.lstrip("0")
    return ("Owner-directed work (ex:CR3_ChipScroll). Given the page of chapter %s (the earlier page and its deck), when the page is rebuilt as a new file with a new page version on the template 9.52.1 with the builders v4_15_0 and v2_24_0, then ALL of: (1) the page test 9.36.0 runs all its added features with no skip and passes them (P1, P2, P3, P4, P5, P6, P8, P9, P11) and every other feature, exit 0; "
            "(2) the page tests 9.34.1 and 9.35.1 report no failure and widgets, features and gates not below the stored result of the page 9.74.0 (chapter 5) or 9.75.0 (chapter 6), skipped not more; (3) the chapter-code tab equals the deck's chapter-code manifest in names and order and each example runs in the page and shows its result; "
            "(4) the Stage 4 gate runner v1_1_0 for %s exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, the Research, Deck and Page chapter checks pass, the deck match check reports 0 not carried; (5) no committed file is edited, no gate, test or threshold changed; the Stage 4 page ABox and the stored page-test result are new files; "
            "results as printed; if any element fails the page is named failing and this criterion has no passing result. " % (ch, ch) + FACT + " " + RV.STD_P)
def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "A story chip does not bring its story into view on the chapter 5 page: may the template get a new version 9.52.1 and the chapter 5 and 6 pages be rebuilt on it?"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_Remedy56, ex:AC4R_Page_Ch05, ex:AC4R_Page_Ch06 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Requested " + WHEN + ". " + FACT + " The change grows the scope: a new template version, and new rebuilds of two pages that were delivered. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What repairing the story chip costs, measured before it is started"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Remedy56 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(FACT + " AFFECTED: TK_Remedy_Page_Ch05_Build (its criterion AC4R_Page_Ch05 names template 9.52.0 and the page 9.80.0 fails one feature of it, so the criterion cannot be met; the task is suspended, not edited, G125) and its Verify task; the chapter 6 page task (met on page 9.81.0, Done; not edited; its latent defect is carried by the new story); the template 9.52.0 (stays byte-identical; the Template task TK_Remedy_Template stays Done: its criterion was met as measured, and the defect is a finding beyond what the page tests measured). "
        "NOT AFFECTED: the decks, the page tests, the page-data builder, the pywheels files, the chapter-code manifests, every other chapter, the Mission outcome and the Achieved status. "
        "CHAPTER 6: the template change TOUCHES chapter 6, because the page 9.81.0 carries the same handler (it passes only because its first chip is the first story); the plan rebuilds the chapter 6 page on 9.52.1 so that both delivered pages are free of the defect; the rebuild is a separate story and task so it can be declined without blocking chapter 5. "
        "PLAN (route as ex:CR3_Remedy56, G127): a StageRevision from the Scope stage, seven versions; new iteration Iter_18 with three stories and six tasks: template 9.52.1 (executor, about 1 h) and its verification (builder, about 0.7 h); then the pages of chapters 5 and 6 rebuilt in parallel (executors, about 2 h each) and their verification (builder, about 1 h each, serial browser tests). "
        "Estimated from T0 (executor of the template starts at once): template ready about T0+1.5 h, page chapter 5 and chapter 6 about T0+4.5 h and T0+5 h; the machine has 2 cores, so browser tests queue. The proposed end is today Friday 2026-10-23 09:00 UTC (12:00 Istanbul), the owner's to decide. "
        "COST: new files only (one template, no new builder unless the default must change); old files byte-identical; no gate, test or threshold changes. A criterion that fails is named failing and its story is not Done; nothing is waived."))
    return t + cr + ia, "ChangeRequest %s (Pending) and ImpactAssessment %s for the story-chip defect of template 9.52.0 found on the chapter 5 page 9.80.0: facts, cause, affected items, chapter 6 touched (latent), plan and estimates." % (CR, IA)
def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds deliverables (a new template version and two page rebuilds, as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). "
              "The request and its impact assessment " + IA + " were recorded first. This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. "
              "The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the builder role.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the story chip repair (template 9.52.1 and the chapter 5 and 6 pages)"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the story chip repair: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."
def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Del3_ChipScrollTemplate a backlog:ScopeDeliverable ;
    rdfs:label "A page template 9.52.1 that brings a story into view after the pane is fitted, as a new file with 9.52.0 kept"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(tp)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Del3_ChipScrollPages a backlog:ScopeDeliverable ;
    rdfs:label "The pages of chapters 5 and 6 rebuilt on template 9.52.1 so that every story chip opens its story in view"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%(cl)s"^^xsd:string ;
    backlog:hasDeliverableText %(pg)s ;
    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope3 backlog:requiresDeliverable ex:Del3_ChipScrollTemplate, ex:Del3_ChipScrollPages ; rdfs:seeAlso %(cr)s, %(ia)s .
ex:Scope3 rdfs:comment %(sc)s@en .
''' % dict(cl=T.CLAUSE, cr=CR, ia=IA, tp=lit("The page template 9.52.1, a new file over 9.52.0 (which stays unchanged), whose story-chip click handler runs the scroll after the pane is fitted; every id, hook and behaviour of 9.52.0 stays. " + FACT + " " + STD1),
                  pg=lit("The pages of chapter 5 and chapter 6 rebuilt as new files on template 9.52.1 with the builders v4_15_0 and v2_24_0, passing the page test 9.36.0 and the page tests 9.34.1 and 9.35.1 with no failure, the Stage 4 gate runner and the chapter checks. " + RV.STD_P),
                  sc=lit("Revised 2026-10-23 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires ex:Del3_ChipScrollTemplate and ex:Del3_ChipScrollPages in the area ex:Area3_Remedy56. No exclusion changes: the new template is a new file named in the deliverable and the exclusion of changes to gates, tests and thresholds still holds." % (REV, CR, WHEN)))]
    t += "".join(L); return t + SL.out_new(t, "Scope", "Out3_ScopeR7", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the story chip repair: two deliverables (template 9.52.1; the pages of chapters 5 and 6 rebuilt on it) in the existing area."
def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR7", prev); t = X.set_status(t, "LS_Goaled")
    L = ['''
ex:G3_ChipScroll a backlog:Goal ;
    rdfs:label "On the chapter 5 and 6 pages every story chip brings its story into view"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %(r)s ;
    backlog:producedByStage ex:Out3_GoalR7 .
ex:G3_ChipScroll rdfs:comment "Drafted by the builder session on 2026-10-23 from the change request %(cr)s; the intent origin is therefore Derived."@en .
ex:Spec3C_P a backlog:Specification ;
    rdfs:label "What it is for a story chip to work"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_ChipScroll ;
    backlog:hasSpecificationText %(s)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR7 .
ex:Scen3C_Passes a backlog:TestScenario ; rdfs:label "A page on template 9.52.1 brings every story into view when its chip is clicked"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3C_P ;
    backlog:hasScenarioText "Given a page of chapter 5 or 6 built on template 9.52.1, when the page tests are run, then the story chip feature passes (the Stories pane is visible and the story is inside the viewport) and nothing else fails." .
ex:Scen3C_NotClaimed a backlog:TestScenario ; rdfs:label "A page on template 9.52.0 whose chip feature fails is named failing and not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3C_P ;
    backlog:hasScenarioText "Given the chapter 5 page 9.80.0 on template 9.52.0 (measured 2026-10-23), when the page tests are run, then the story chip feature fails for GoxColdFind and the page carries no passing result." .
''' % dict(cr=CR, r=lit("Derived from the revised scope and from the change request %s: the owner uses the pages in class; a story chip that scrolls to nowhere is a defect of the teaching material. %s" % (CR, FACT)), s=lit(STD1 + " " + FACT))]
    t += "".join(L); return t + SL.out_new(t, "Goal", "Out3_GoalR7", "Out3_ScopeR7"), "third lineage, Goal stage rebuilt for the story chip repair: one goal with its specification and a nominal and a rejection scenario."
def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR7", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    L = ['''
ex:Obj3_ChipScroll a backlog:Objective ; rdfs:label "Pages of chapters 5 and 6 on which the story chip feature of the page tests passes: from 1 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_ChipScroll ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_ChipScroll ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of the pages of chapters 5 and 6 whose page tests 9.36.0, 9.35.1 and 9.34.1 report no failure, read from the runs after the evidence bridge has run them on the newest pages." ;
    backlog:hasBaselineValue "1"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3C_ChipScroll ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR7 .
ex:Met3_ChipScroll a backlog:Metric ; rdfs:label "pages of chapters 5 and 6 with no failing page-test feature"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3C_ChipScroll a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the rebuilt pages are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria on the rebuilt pages, so the count is read from verified runs." ; backlog:expectedValue "2"^^xsd:decimal .
ex:Obs43_ChipScroll a backlog:MetricObservation ; rdfs:label "Baseline, before the repair"@en ;
    backlog:observesMetric ex:Met3_ChipScroll ; backlog:observationFor ex:Obj3_ChipScroll ; backlog:hasObservedValue "1"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod "Baseline from the control of the two pages on 2026-10-23: the chapter 6 page 9.81.0 passes the three page tests; the chapter 5 page 9.80.0 fails one feature of each (the story chip), so 1 of 2." .
ex:Obj3_ChipScroll rdfs:comment "Drafted by the builder session on 2026-10-23 from the change request %s; the intent origin is therefore Derived."@en .
''' % (now, CR)]
    t += "".join(L); return t + SL.out_new(t, "Objective", "Out3_ObjectiveR7", "Out3_GoalR7"), "third lineage, Objective stage rebuilt for the story chip repair: one objective (pages without a failing page-test feature, 1 to 2) with its metric, checkpoint and baseline reading."
def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR7", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput %s ;" % OLDB); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLDB, "backlog:admittedByOutput %s ;" % NEWB)
    L = ['ex:TS_PageTemplateD a backlog:ToolScript ; rdfs:label "page template 9.52.1 (new file over 9.52.0: the story chip scrolls after the pane is fitted)"@en ; backlog:scriptFileName "course_page_template_v9_52_1.html" ; backlog:acceptsGraphPath false .\n']
    tools_of = {"AC5R_Template": ["TS_PageTemplateD", "TS_PageTest36", "TS_PageTest35b", "TS_PageBuilder415", "TS_PageData224"], "AC5R_Page_Ch05": ["TS_PageTemplateD", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"] + RV.BASE, "AC5R_Page_Ch06": ["TS_PageTemplateD", "TS_PageBuilder415", "TS_PageData224", "TS_PageTest36"] + RV.BASE}
    for c, lab in LAB.items():
        k = "TC3C_T" if c == "AC5R_Template" else "TC3C_P"
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n' % (c, lit(lab), lit(gh(c)), ", ".join("ex:" + x for x in tools_of[c]), lit(VER), k, k))
    for tid, title, ttype, deps, sess, est, hrs, note in TASKS: L.append(RV.task_block(tid, title, ttype, deps, sess, est, hrs, note))
    for sid, title, deliv, obj, crits, tks in STORIES: L.append(RV.story_block(sid, title, deliv, obj, crits, tks, "Requested " + WHEN + " (" + CR + "). One criterion per unit (G133). The Done stories and tasks stay Done and are not edited (G125). " + FACT))
    for k in ("T", "P"):
        L.append('''
ex:TC3C_%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criteria on the new files and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3C_Passes ; backlog:runsOnData ex:Data3C_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the newest files; they report no failure and exit 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3C_%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the existing page that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion %(cr)s ; backlog:coversScenario ex:Scen3C_NotClaimed ; backlog:runsOnData ex:Data3C_%(k)s_Failing ;
    backlog:hasCaseText "Run the page tests over the chapter 5 page 9.80.0 (measured 2026-10-23); the story chip feature fails and the page carries no passing result." .
ex:Data3C_%(k)s_Passing a backlog:TestData ; rdfs:label "The rebuilt files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest rebuilt files, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3C_%(k)s_Failing a backlog:TestData ; rdfs:label "The chapter 5 page 9.80.0 whose story chip feature fails when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The page sen0401_ch05_page_v9_80_0.html on template 9.52.0 with the failing feature of ex:IA3_ChipScroll." .
''' % dict(k=k, cr=", ".join("ex:" + c for c in (["AC5R_Template"] if k == "T" else ["AC5R_Page_Ch05", "AC5R_Page_Ch06"]))))
    sid_all = [s[0] for s in STORIES]; tk_all = [x[0] for x in TASKS]
    for x in sid_all + tk_all:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, ITER, lit("Refined by the builder session from the change request %s and the measured facts of %s: acceptance criterion with tool and version, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, deliv, obj, crits, tks in STORIES:
        L.append('ex:Plan3C_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 18"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3C_P, ex:Scen3C_Passes, ex:Scen3C_NotClaimed .\n' % (sid, sid, now, ITER, sid, ", ".join("ex:" + x for x in tks)))
        L.append("ex:%s backlog:standsAlone true .\n" % sid)
    L.append("ex:Obj3_ChipScroll backlog:metricMovableBy ex:ST_Repair_Template, ex:ST_Repair_Page_Ch05, ex:ST_Repair_Page_Ch06 .\n")
    END = "2026-10-23T09:00:00"
    SG = ("The story chip of the chapter 5 and 6 pages brings its story into view on a new template 9.52.1, and both pages are rebuilt on it and pass the three page tests, verified by the evidence bridge; the new template and the rebuilt pages are new files and nothing existing is edited. Frozen at the planning ceremony.")
    DS = ("Proposed by the builder session on 2026-10-23: the start is the instant of the planning ceremony ex:PC3_Iter_18; the proposed end is Friday 2026-10-23 09:00 UTC (12:00 Istanbul); the owner decides the end. Justification (estimates, not measurements): the template change is one handler (about 1 h with scratch proof runs), its verification about 0.7 h; "
          "the two page rebuilds follow in parallel (about 2 h each with three serial page-test runs each, on 2 cores), their verification about 1 h each, serial. Critical path: template 1.0 h + verification 0.7 h + page 2.0 h + verification 1.0 h = about 4.7 h after the template executor starts; chapter 6 about 0.5 h later. The page of chapter 6 can be declined without blocking chapter 5.")
    L.append('ex:Iter_18 a backlog:Iteration ; rdfs:label "Iteration 18: the story chip repair, template 9.52.1 and the chapter 5 and 6 pages rebuilt"@en ; backlog:hasIdentifier "Iter_18" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (now, END, lit(DS), lit(SG), ", ".join("ex:" + x for x in sid_all + tk_all)))
    L.append('ex:PB3C_Iter_18 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 18 when it was planned"@en ; backlog:baselineFor ex:Iter_18 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (now, now, END))
    L.append('ex:PC3_Iter_18 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 18: the story chip repair"@en ; backlog:ceremonyFor ex:Iter_18 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (now, ", ".join("ex:Plan3C_" + s for s in sid_all), lit("Held %s by the builder session after the change request %s: three stories and six tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief." % (now, CR))))
    L.append('ex:SC3_ChipScroll a backlog:ScopeChange ;\n    rdfs:label "Scope grown by the story chip repair: template 9.52.1 and the chapter 5 and 6 pages rebuilt on it"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s for s in sid_all), lit("Requested " + WHEN + ". The boundary moved outward by three stories; new files only; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_ChipScroll and the three stories it admits; it was Pending before. The direction is the owner\'s standing direction of 2026-10-22 17:30 Istanbul as relayed by the course coordinator on 2026-10-23; the end of the iteration is still the owner\'s."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR9", "Out3_ObjectiveR7"), "third lineage, Backlog stage rebuilt for the story chip repair: three stories (template; pages of chapters 5 and 6) with six tasks and dependencies, three criteria with tools and versions, refinement and planning events, the new iteration Iter_18, and the ScopeChange that admits the stories; the change request is Accepted; the %d carried items are re-admitted, not re-dated." % n
def ev_fill(t, prev):
    return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)
def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))
if __name__ == "__main__": main()
