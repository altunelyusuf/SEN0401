#!/usr/bin/env python3
"""sen0401_lineage_page_gates v1_0_0 - change route (rulings G113, G125, G127, G133, G134, G136) for the owner's answer of 2026-10-22 to the change request ex:CR3_PageGates ("Yes, proceed.", option A):
a NEW page-template version (the Untangle fix for dense section edges) and NEW page-test versions (the assertion on mentioned-together relationships applies to a page that has such relations), both as new files with the old ones kept,
then the pages of chapters 10 and 11 rebuilt and measured with them. The scope excludes any change to a gate, a test or a threshold (ex:Excl3_NoGateChange, ex:Excl3_NoConceptGates), and the deliverable is new, so the route is a StageRevision
from the Scope stage (G127), as for the section links. The work is planned into a NEW iteration, ex:Iter_16 (the goal of ex:Iter_15 and ex:Iter_14 is frozen at its start).
Events, one new file each: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import hashlib, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL

lit, esc = G.lit, M.esc
ITER = "ex:Iter_16"; REV = "ex:Revision_Lineage3_Scope4"; CR = "ex:CR3_PageGates"; IA = "ex:IA3_PageGates"
ACTIVE = ["ex:Out3_ScopeR4", "ex:Out3_GoalR4", "ex:Out3_ObjectiveR4", "ex:Out3_BacklogR6"]; NEWB = "ex:Out3_BacklogR7"
WHEN = "Thursday 2026-10-22 08:35 Istanbul (05:35 UTC), as relayed by the course coordinator; the time at which the owner wrote it is not known to the builder session"
QUOTE = '"Yes, proceed."'
QUESTION = ("Do you approve building a new page template version and a new page-test version as NEW files (the old ones kept for comparison), so that the section-link pages of chapters 10 and 11 can be rebuilt and measured: the template with an Untangle fix for dense section edges, "
            "and the test with the 'mentioned-together relations' assertion applying only to a page that has such relations (yes or no)?")
OWNER_ACT = ("Owner's answer of %s to the question of ex:CR3_PageGates (%s), relayed by the course coordinator and recorded by the builder session, quoted: %s This is option A of the request. Under the standing rule that work following the owner's direction is recorded as owner-directed, "
             "it is not listed as an open owner confirmation." % (WHEN, QUESTION, QUOTE))
sha = lambda p: hashlib.sha256(open(os.path.join(M.REPO, "08-tooling", p), "rb").read()).hexdigest()
H = {"tpl": sha("course_page_template_v9_51_0.html"), "t34": sha("sen0401_page_test_v9_34_0.py"), "t35": sha("sen0401_page_test_v9_35_0.py")}
FACTS = ("Facts measured by the control of 2026-10-22 (register v0.173; logs in 08-tooling/verify/iter14/ch10 and ch11): page 9.78.0 of chapter 10 fails 4 of 370 features in each of the tests 9.34.0 and 9.35.0, which are 2 distinct features: (A) the ERD sections choice with the mentioned-together relations on by default "
         "(sections 17, relations 23 -> 23 with mentions off: the assertion r2 > r3 of line 1245 of 9.35.0 assumes that any page with a relation between two sections has 'mentions'; the page data holds 0 'mentions', because the builder derives them only where another section's text names a concept label, and the new section links are all 'operates on'); "
         "(B) the concept-map Untangle leaves 2 of 24 boxes overlapping (template 9.51.0, function rlUntangle). Page 9.78.0 of chapter 11 stops in both tests on a click timeout ('HeaderFields intercepts pointer events': the rect of the entity HeaderFields lies over the element the test clicks) after 161 passed features, "
         "fails the same assertion (A) (sections 16, relations 32 -> 32), and the executor's force-click diagnostic (a log, not a result) found 4 of 22 boxes overlapping; whether the crash comes from the layout (overlapping entities) or from the test is a fact the executor of the template task must establish. "
         "The ERD label features themselves run and pass on both pages (chapter 10: labels 23 -> 23, overlaps 0/0). Old pages (9.77.0) passed because the test skipped assertion (A) for them (no relation between two sections).")
TOOLS = [("TS_PageTest34b", "sen0401_page_test_v9_34_1.py", "page test 9.34.1 (new file, over 9.34.0: the one assertion only)"), ("TS_PageTest35b", "sen0401_page_test_v9_35_1.py", "page test 9.35.1 (new file, over 9.35.0: the one assertion only)"),
         ("TS_PageTemplateB", "course_page_template_v9_51_1.html", "page template 9.51.1 (new file, over 9.51.0: the Untangle fix)"),
         ("TS_GateCheck", "sen0401_lineage_gate_check_v1_0_0.py", "gate check v1_0_0 (the exit-code form of the elements of the criteria of the page gates: new files, byte-identical old files, only-the-named-lines diffs, regression equality; written by the builder session before the control run, never run by an executor)"),
         ("TS_PageCheck2", "sen0401_lineage_page_check_v1_1_0.py", "page check wrapper v1_1_0 (links, ERD labels, tests, counts, Stage 4 page ABox, nothing edited; page 9.79.0 and later by argument)")]
VERS_PAGE = ("page tests 9.34.1 and 9.35.1 (new files; identical to 9.34.0 and 9.35.0 in every feature except the one named assertion, proved by AC3P_Test); page template 9.51.1 (new file; identical to 9.51.0 except the named layout code, proved by AC3P_Template); "
             "Stage 4 gate runner v1_1_0 reading the CURRENT RDODI validator v1.13.0; chapter check v1_3_0 reading the PINNED RDODI validator v1.6.0; deck match check v1_0_0; page check wrapper v1_1_0; research check v1_0_0")


def ev_change(t):
    i, j = T.blk(t, "CR3_PageGates"); b = t[i:j]
    b = b.rstrip().rstrip(".") + (' ;\n    rdfs:comment %s@en .\n' % lit("Owner's answer recorded 2026-10-22: " + OWNER_ACT + " Disposition stays Pending until the ScopeChange that admits the story is recorded in the Backlog version (G127 route)."))
    t = t[:i] + b + t[j:]
    i, j = T.blk(t, "IA3_PageGates"); b = t[i:j]
    b = b.rstrip().rstrip(".") + (' ;\n    rdfs:comment %s@en .\n' % lit(
        "Impact assessment after the owner's answer (2026-10-22). " + FACTS + " Route: the scope excludes any change to a gate, a test or a threshold (ex:Excl3_NoGateChange, ex:Excl3_NoConceptGates) and a new template and new test versions are a new deliverable, so a StageRevision from the Scope stage (G127), "
        "seven versions (this one, the retraction, four stages, the fill), against the 'keep the old pages' alternative (option B), which costs no page work and leaves the ERD label element unmeasurable. "
        "Planned structure (not begun): a new story ST_Page_Gates in a NEW iteration ex:Iter_16 with T1 template (new version 9.51.1), T2 page tests (new versions 9.34.1 and 9.35.1), in parallel, and T3 regression (depends on T1 and T2; the new tests on the 14 shipped pages and on the pages of chapters 1, 8, 12 and 14 rebuilt on the new template); "
        "the existing tasks of ST_Section_Links in ex:Iter_14 then continue: T4 and T5 (the page tasks of chapters 10 and 11, now also depending on T1, T2 and T3, resumed after T_Suspend) and T6 (their Verify tasks). "
        "Why a new iteration: the goals of ex:Iter_14 and ex:Iter_15 are frozen at their start and adding work to them is the mid-sprint extension the owner ruled out on 2026-10-21 10:14 Istanbul; the tasks T4 to T6 stay in ex:Iter_14 with their story (a story is planned into one iteration only, L4). "
        "Disclosed consequence: the sprint goal of ex:Iter_14 says 'on the gates as they stand'; the owner's decision changes the test and the template, so that goal cannot be met as worded and the review of ex:Iter_14 will record it so; a rebaseline is the owner's. "
        "The criteria AC3L_Ch10 and AC3L_Ch11 name the tests 9.34.0 and 9.35.0 'unchanged'; they are not edited. Their successors AC3L2_Ch10 and AC3L2_Ch11 name the same five elements with the new test and template versions; the story ST_Section_Links points to the successors, the old criteria stay as history with their recorded result NOT MET. "
        "AC3T_Ch10 and AC3T_Ch11 (ex:Iter_13) name the same tests; their element 4 will be measured with the new test versions, justified by AC3P_Test (identical but for the named assertion); the note on each says so and nothing in them is edited. "
        "Not affected: the research of chapters 10 and 11 (Done), the passing chapters unless the regression shows a change, the Mission outcome, closureCommittedAt and the Achieved status of the third lineage. "
        "Risks: the template fix may change the layout of another page (the regression set rebuilds chapters 1, 8, 12 and 14 on the new template and runs the new tests: results equal to or better than stored); the new test must give the same result as the old on every page that has mentions (all 14 shipped pages run: old stored result against new run). "
        "Cost: about 11 hours of serial machine time (a page test run is about nine minutes; 14 shipped pages plus 4 rebuilt pages plus the two section-link pages), spread over one to two days."))
    t = t[:i] + b + t[j:]
    return t, "The owner's answer of 2026-10-22 ('Yes, proceed.') recorded on the change request CR3_PageGates (option A) and its impact assessment; disposition still Pending; no stage changed in this version."


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = (OWNER_ACT + " The work adds a deliverable (new template and test versions) and lifts, for the named changes only, the exclusions of any change to a gate or test; the lineage is in its closed Backlog stage, and a deliverable that is new is a StageRevision from the Scope stage (G127). "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each; the goals, objectives, stories and tasks already in the register, Done ones included, re-enter by admission and are not re-dated. "
              "The change request and its impact assessment were completed first. The interim versions are the declared transition (G129). Recorded as decided by the builder role: the route is what the owner's direction needs; the stage revision itself he did not decide.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: a new page template version and new page test versions, then the section-link pages rebuilt"@en ;\n'
         '    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (
        REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the new template and test versions: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Scoped")
    L = ['''
ex:Area3_PageGates a backlog:ScopeArea ;
    rdfs:label "The page template and the page tests as they meet pages whose chapters state section relationships"@en ;
    backlog:belongsToLineage ex:Lineage3 ;
    backlog:areaLocation "08-tooling: the page template (course_page_template_v9_51_0.html) and the page tests 9.34.0 and 9.35.0, as new files beside them; the pages of chapters 10 and 11" ;
    backlog:areaMeasure "pages of chapters 10 and 11 with section links that pass the page tests: 0 of 2 today; after the work 2" ;
    backlog:hasScopeLayer backlog:Layer_Work .
ex:Del3_PageGates a backlog:ScopeDeliverable ;
    rdfs:label "A page template version and page test versions that measure pages with section links, and the pages of chapters 10 and 11 rebuilt on them"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:derivesFromMissionClause "%s"^^xsd:string ;
    backlog:hasDeliverableText %s ;
    backlog:deliverableForArea ex:Area3_PageGates ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .
ex:Scope3 backlog:requiresDeliverable ex:Del3_PageGates ;
    backlog:coversArea ex:Area3_PageGates ;
    rdfs:seeAlso ex:CR3_PageGates, ex:IA3_PageGates .
ex:Scope3 rdfs:comment %s@en .
ex:Excl3_NoGateChange rdfs:comment %s@en .
ex:Excl3_NoConceptGates rdfs:comment %s@en .
''' % (T.CLAUSE,
       lit("(1) A NEW page template file (version 9.51.1, over 9.51.0 which stays unchanged) whose concept-map Untangle leaves no two boxes overlapping on the pages of chapters 10 and 11 with section links, and in which the executor has established as a fact whether the click timeout of the page of chapter 11 ('HeaderFields intercepts pointer events') comes from the layout or from the test; "
           "(2) NEW page test files (9.34.1 over 9.34.0 and 9.35.1 over 9.35.0, which stay unchanged) that differ in exactly one assertion: the one on the mentioned-together relationships applies to a page that has such relationships, so that a page whose section relationships are all stated links is measured instead of failed by an assumption; every other assertion identical; "
           "(3) a regression measurement: the new tests give the stored result on the 14 shipped pages, and pages of chapters 1, 8, 12 and 14 rebuilt on the new template give a result equal to or better than the stored one; "
           "(4) the pages of chapters 10 and 11 rebuilt on the new template and measured with the new tests. " + FACTS),
       lit("Revised 2026-10-22 by the stage revision %s on the owner's answer of %s (quoted in the change request ex:CR3_PageGates). The statement above is unchanged (L-112). It now also requires ex:Del3_PageGates and covers the area ex:Area3_PageGates." % (REV.replace("ex:", ""), WHEN)),
       lit("Note 2026-10-22: the exclusion of any change to a gate, a test or a threshold is lifted for exactly two named changes by the owner's answer of %s (ex:CR3_PageGates, option A): a new page-template file with an Untangle fix, and new page-test files that differ in one assertion; both as new files with the old ones kept, and measured against the stored results of the shipped pages. It stands for every other change: Stage 3.F, the Stage 4 gates, the chapter checks, the deck match check, every other assertion and threshold of the page tests." % WHEN),
       lit("Note 2026-10-22: the exclusion of a change of any test is lifted for the one named assertion by the owner's answer of %s (ex:CR3_PageGates); the other parts of this exclusion stand." % WHEN))]
    t += "".join(L)
    return t + SL.out_new(t, "Scope", "Out3_ScopeR5", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the page gates: a deliverable (new template and test versions as new files, regression, the two pages rebuilt), its area, and the two exclusions lifted for the named changes only."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR5", prev); t = X.set_status(t, "LS_Goaled")
    intent = ('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-22 from the owner\'s answer of ' + WHEN + ' (quoted in the change request ex:CR3_PageGates); the intent origin is therefore Derived. The owner gave the direction; he did not review the wording of this element."@en .\n')
    L = ['\nex:G3_PagesMeasurable a backlog:Goal ;\n    rdfs:label "A page whose chapter states section relationships is measured by the page tests on what it has, and the pages of chapters 10 and 11 pass"@en ;\n'
         '    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_PageGates ;\n    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalOrigin backlog:GoalOrigin_New ;\n'
         '    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;\n    backlog:hasGoalRationale %s ;\n    backlog:producedByStage ex:Out3_GoalR5 .\n' % lit("Derived from the revised scope (ex:Del3_PageGates) and from the owner's answer of %s, quoted: %s" % (WHEN, QUOTE)),
         intent % "G3_PagesMeasurable"]
    L.append('''
ex:Spec3P_G a backlog:Specification ;
    rdfs:label "What it is for the page template and the page tests to measure a page with section links"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_PagesMeasurable ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR5 .
ex:Scen3P_G_Passes a backlog:TestScenario ; rdfs:label "A page whose section relationships are all stated links is measured by the new tests and passes when it is right"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3P_G ;
    backlog:hasScenarioText "Given the page of chapter 10 or 11 rebuilt on the new template, when the new tests 9.34.1 and 9.35.1 run, then no two concept-map boxes overlap after Untangle, the ERD assertion on mentioned-together relationships is judged on what the page has, and the run ends without a crash." .
ex:Scen3P_G_Unchanged a backlog:TestScenario ; rdfs:label "A page that has mentions gets the same result from the new tests as from the old"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3P_G ;
    backlog:hasScenarioText "Given any of the 14 shipped pages, when the new tests run, then the result equals the stored result of the old tests; a difference is a regression and the new versions are named failing." .
''' % lit("The page template and the page tests measure a page by what it has: the Untangle of the concept map leaves no two boxes overlapping when many edges join the section boxes, and the assertion that the mentioned-together toggle removes relationships applies to a page that has such relationships. "
       "The old template and old tests stay unchanged as files and as comparison; the new ones differ from them only in the named parts; every shipped page gets from the new tests the result the old tests stored."))
    t += "".join(L)
    return t + SL.out_new(t, "Goal", "Out3_GoalR5", "Out3_ScopeR5"), "third lineage, Goal stage rebuilt for the page gates: one goal (a page with section links is measured by what it has, and the pages of chapters 10 and 11 pass) with a specification and a nominal and a rejection scenario."


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR5", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    i, m, what, b, tg = "Obj3_PagesMeasured", "Met3_PagesMeasured", "pages among chapters 10 and 11 whose page tests of the standard pass with their section links", 0, 2
    L = ['''
ex:%(i)s a backlog:Objective ; rdfs:label "Pages among chapters 10 and 11 that pass the page tests with their section links: from 0 to 2"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_PagesMeasurable ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:%(m)s ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery "Count of %(what)s, read from the runs of the new page tests on the newest pages after the evidence bridge has run the checks." ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "2"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3P_%(i)s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR5 .
ex:%(m)s a backlog:Metric ; rdfs:label "%(what)s"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3P_%(i)s a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the page gates are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the criteria of chapters 10 and 11 on the rebuilt pages, so the count is read from verified runs." ;
    backlog:expectedValue "2"^^xsd:decimal .
ex:Obs42_%(i)s a backlog:MetricObservation ; rdfs:label "Baseline, before any work on the page gates"@en ;
    backlog:observesMetric ex:%(m)s ; backlog:observationFor ex:%(i)s ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%(now)s"^^xsd:dateTime ;
    backlog:hasObservationMethod "Baseline measured by the control of 2026-10-22 (register v0.173; logs in 08-tooling/verify/iter14): the page 9.78.0 of chapter 10 fails 4 features of 370 in each test and the page 9.78.0 of chapter 11 stops on a click timeout and fails the same assertion: 0 of 2 pass." .
''' % dict(i=i, m=m, what=esc(what), now=now)]
    L.append(('ex:%s rdfs:comment "Drafted by the builder session on 2026-10-22 from the owner\'s answer of ' + WHEN + ' (ex:CR3_PageGates); the intent origin is therefore Derived."@en .\n') % i)
    t += "".join(L)
    return t + SL.out_new(t, "Objective", "Out3_ObjectiveR5", "Out3_GoalR5"), "third lineage, Objective stage rebuilt for the page gates: one objective (pages of chapters 10 and 11 that pass the page tests with their section links, 0 to 2) with metric, checkpoint and a baseline reading of 2026-10-22."


def gh_template():
    return ("Owner's answer of %s: %s to the question: %s Given the page template 9.51.0 (SHA-256 %s) whose concept-map Untangle (function rlUntangle, from line 684 of the file) leaves boxes overlapping on pages with dense section edges (chapter 10: 2 of 24 boxes; chapter 11: 4 of 22 per the executor's diagnostic), "
            "when a NEW template file course_page_template_v9_51_1.html is made, then ALL of: (1) the file is new, the file 9.51.0 is byte-identical to the SHA-256 above, and the version comment names 9.51.1 and its reason; "
            "(2) the difference between 9.51.0 and 9.51.1 is limited to the layout code the executor names (the function rlUntangle and, only if the analysis of (4) shows it is the cause, erdUntangle), with the line ranges and the reason for each hunk stated in the report; no other function, text, style or threshold differs; "
            "(3) on the pages of chapters 10 and 11 rebuilt on 9.51.1, the concept-map Untangle leaves no two boxes overlapping, measured as the page test measures it (24 boxes and 22 boxes, overlaps 0); "
            "(4) the click timeout of the page of chapter 11 ('HeaderFields intercepts pointer events') is analysed and reported as a FACT with its measurements - whether it is the template layout (overlapping entities, one intercepting the pointer events) or a test artefact; a force-click, a changed click target or any workaround is never part of a result; "
            "(5) no gate, no test, no threshold and no criterion is changed by this task; results are reported as printed; if any element fails the template is named failing." % (WHEN, QUOTE, QUESTION, H["tpl"]))


def gh_test():
    return ("Owner's answer of %s: %s to the question: %s Given the page tests 9.34.0 (SHA-256 %s) and 9.35.0 (SHA-256 %s), whose assertion 'the ERD's sections choice draws one entity per section with the mentioned-together relationships on by default (the toggle removes them), and the page's schema stays the third choice' (9.35.0 line 1245; 9.34.0 the same feature) "
            "requires r2 > r3 on every page that has a relation between two sections, when NEW test files sen0401_page_test_v9_34_1.py and sen0401_page_test_v9_35_1.py are made, then ALL of: (1) the files are new and 9.34.0 and 9.35.0 are byte-identical to the SHA-256 above; "
            "(2) the difference from 9.34.0 and from 9.35.0 is limited to the version lines and comments and to that one assertion: on a page that has 'mentions' relations the assertion is unchanged (r2 > r3); on a page that has relations between two sections but no 'mentions' the assertion is r2 == r3 and r2 > 0 (the toggle has nothing to remove); the NOREL branch is unchanged; "
            "every other feature, skip, threshold and line is textually identical, shown by a diff and by the set of feature texts being equal; (3) the new tests are run on one page that has mentions (chapter 1, page 9.77.0 or the newest) and on the page 9.78.0 of chapter 10: the first gives the stored result, the second no longer fails on that assertion; "
            "(4) no gate, threshold or other test is changed; results are reported as printed; if any element fails the tests are named failing." % (WHEN, QUOTE, QUESTION, H["t34"], H["t35"]))


def gh_regress():
    return ("Owner's answer of %s: %s. Given the new template 9.51.1 (task TK_PageGates_Template) and the new page tests 9.34.1 and 9.35.1 (task TK_PageGates_Test), when they are measured against the stored results of the pages, then ALL of: "
            "(1) the new tests 9.34.1 and 9.35.1 run on each of the 14 shipped pages (the newest page of each chapter as it stands; chapters 10 and 11: 9.77.0) give the result the old tests stored: widgets, features passed, failed, skipped and gates equal or better, and on a page that has mentions identical in failed and skipped; "
            "(2) the pages of chapters 1, 8, 12 and 14 are rebuilt (to a scratch folder, not shipped) on the template 9.51.1 with the page builder v4_14_0 and the page-data builder that built them, and the new tests give for each a result equal to or better than its stored result; "
            "(3) each run is kept as a log; a main-thread budget failure is run again up to three times, every run kept; a [FAIL] is a result; "
            "(4) no gate, test, threshold or committed file is changed; results are reported as printed; if any page differs the new versions are named failing and the differing features are listed." % (WHEN, QUOTE))


def gh_page(label, num, nsec, w):
    return ("Owner's answer of %s (change request ex:CR3_PageGates): %s. Given the research of %s (%d sections, section links Done) and the page 9.78.0 (failing the page tests 9.34.0 and 9.35.0 on the assertion on mentions and on the Untangle overlap), when the page is rebuilt as a new page version (9.79.0) on the template 9.51.1 and the tests 9.34.1 and 9.35.1 are run, then ALL of: "
            "(1) links: every one of the %d sections is related to at least one other section by a stated link, and no relationship is stated as text only; "
            "(2) ERD: the page tests 9.34.1 and 9.35.1 run their ERD label features (the filled ERD overlap and labels-over-entity reading, and the on-choice labels mode) with no skip and pass them, labels shown after Untangle at least 95 percent of the grid's, and the run ends without a crash; "
            "(3) gates: the Stage 4 gate runner v1_1_0 for %s (reading the current validator v1.13.0) exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks v1_3_0 (reading the pinned validator v1.6.0) pass; "
            "(4) the five elements of the criterion AC3T_Ch%s are measured on the new page and all pass: the template markers, pages_deck_match_verify with 0 not carried, the page tests 9.34.1 and 9.35.1 with counts equal to or better than the stored result of 9.77.0, the Stage 4 page ABox rebuilt as a new file and the stored page-test result as a new file; "
            "(5) no committed file is edited and no gate, test, threshold or criterion is changed beyond the two new test files and the new template file of this iteration; results are reported as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN) and a skip is not a pass; "
            "if any element fails the chapter is named failing and this criterion has no passing result." % (WHEN, QUOTE, label, nsec, nsec, num, w))


def block_note(t, tid, add):
    i, j = T.blk(t, tid); return i, j


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR5", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    n = t.count("backlog:admittedByOutput ex:Out3_BacklogR6 ;"); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput ex:Out3_BacklogR6 ;", "backlog:admittedByOutput %s ;" % NEWB)
    L = []
    for ts, fn, what in TOOLS:
        L.append('ex:%s a backlog:ToolScript ; rdfs:label %s@en ; backlog:scriptFileName "%s" ; backlog:acceptsGraphPath false .\n' % (ts, lit(what), fn))
    base = ["TS_Stage4Gates", "TS_ChapterCheck", "TS_DeckMatch", "TS_RdodiValidatorCurrent", "TS_RdodiValidatorPinned"]
    newt = [x[0] for x in TOOLS]
    crits = {"AC3P_Template": ("The page template 9.51.1 is a new file that differs from 9.51.0 only in the Untangle layout code, and the concept map of the pages with section links leaves no two boxes overlapping", gh_template(), newt + ["TS_PageTest35", "TS_PageTest34"], 
                               "template 9.51.0 and tests 9.34.0 and 9.35.0 as comparison (SHA-256 recorded in the text); template 9.51.1; gate check v1_0_0; page check wrapper v1_1_0"),
             "AC3P_Test": ("The page tests 9.34.1 and 9.35.1 are new files that differ from 9.34.0 and 9.35.0 only in the assertion on mentioned-together relationships", gh_test(), newt + ["TS_PageTest35", "TS_PageTest34"],
                           "tests 9.34.0 and 9.35.0 as comparison (SHA-256 recorded in the text); tests 9.34.1 and 9.35.1; gate check v1_0_0; page check wrapper v1_1_0"),
             "AC3P_Regression": ("The new template and tests give every shipped page the result its stored result has, and the pages of chapters 1, 8, 12 and 14 rebuilt on the new template an equal or better one", gh_regress(), newt + ["TS_PageTest35", "TS_PageTest34"],
                                 "tests 9.34.1 and 9.35.1; template 9.51.1; page builder v4_14_0; stored results test_results_abox of the shipped pages; gate check v1_0_0; page check wrapper v1_1_0")}
    for c, (lab, gt, tools, ver) in crits.items():
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the new template or test files cited by SHA-256, the logs of the runs and the diffs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3P_G_Passes, ex:TC3P_G_Unchanged .\n' % (c, lit(lab), lit(gt), ", ".join("ex:" + x for x in tools), lit(ver)))
    for nm, label, num, nsec in (("Ch10", "chapter 10", "10", 17), ("Ch11", "chapter 11", "11", 16)):
        L.append('\nex:AC3L2_%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n'
                 '    backlog:satisfiedByArtifact "the page, its Stage 4 page ABox and the stored page-test results as new files cited by SHA-256, and the runs of the template markers, the deck match check, the page tests, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3P_G_Passes, ex:TC3P_G_Unchanged ;\n    rdfs:seeAlso ex:AC3L_%s .\n'
                 % (nm, lit("The research of %s states how its sections relate as links, and its page, rebuilt on the new template, shows them with the ERD labels measured by the new page tests" % label), lit(gh_page(label, num, nsec, "AC3L_" + nm)),
                    ", ".join("ex:" + x for x in newt + base + ["TS_LinkDiscovery"]), lit(VERS_PAGE), nm))
    # tasks
    COMMON = ("A committed file is never edited: every output is a new file with a new version number. STOP and report if the task cannot be satisfied without editing a committed file, a gate or a test beyond the named new files. Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN).")
    tk1, tk2, tk3 = "TK_PageGates_Template", "TK_PageGates_Test", "TK_PageGates_Regression"
    L.append(G.task_block(tk1, "Make a new page template version 9.51.1 whose Untangle leaves no two boxes overlapping on pages with dense section edges", "Build",
        "Write the NEW file 08-tooling/course_page_template_v9_51_1.html from course_page_template_v9_51_0.html (which stays byte-identical, SHA-256 %s). The failing layout code is the concept map's Untangle, function rlUntangle (the force-directed relocation, from line 684 of the 9.51.0 file: repulsion within two box-lengths, springs along edges, a pull to the centre, chunks), "
        "which on the pages 9.78.0 of chapter 10 (2 of 24 boxes overlap after Untangle) and of chapter 11 (4 of 22 per the executor's force-click diagnostic) leaves boxes overlapping when many edges join the section boxes; the ERD's own layout is erdUntangle (line 1536). "
        "FIRST establish as a FACT, with measurements (positions of the overlapping rects, the entity HeaderFields on the page of chapter 11, which element is intercepted, which template function placed the boxes), whether the click timeout of the page of chapter 11 ('HeaderFields intercepts pointer events') comes from the template layout (entities overlapping so that one intercepts the pointer events: probably the same layout cause) or from the test; write the finding into your report; a force-click, a changed click target or any workaround is not allowed in a result. "
        "THEN change only the layout code the finding names (rlUntangle and, if it is the cause, erdUntangle), keeping the drawn shape, the Reset, the drag behaviour and the speed; no other function, text, style or threshold differs. The page builder v4_14_0 takes the template by argument or default: state how you built the pages (the template path you passed). "
        "Build scratch copies of the pages of chapters 10 and 11 (page 9.78.0 data, template 9.51.1) in a folder outside the repository and measure that no two concept-map boxes overlap after Untangle (the measure of the page test: boxes and overlaps), and that the click no longer times out; do NOT run the full page tests (the regression task does). Commit the new template file and a short evidence file (08-tooling/page-gates-evidence/template_v9_51_1.md) with the diff summary (functions, line ranges, reason) and the finding. %s Satisfies the criterion ex:AC3P_Template." % (H["tpl"], COMMON), ()).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1))
    L.append(G.task_block(tk2, "Make new page test versions 9.34.1 and 9.35.1 whose assertion on mentioned-together relationships applies to a page that has such relationships", "Build",
        "Write the NEW files 08-tooling/sen0401_page_test_v9_34_1.py and sen0401_page_test_v9_35_1.py from 9.34.0 and 9.35.0 (which stay byte-identical, SHA-256 %s and %s). The assertion is the feature \"the ERD's sections choice draws one entity per section with the mentioned-together relationships on by default (the toggle removes them), and the page's schema stays the third choice\" (9.35.0 line 1245): "
        "it requires r2 > r3 (relations drawn with mentions on against off) on any page that has a relation between two sections, which assumes such a page has 'mentions'; the page data of chapters 10 and 11 holds 0 'mentions' (the new section links are all 'operates on'). Change it so that: a page that has 'mentions' relations (type mentions between two different sections in the page data, counted as NOREL counts sections) keeps r2 > r3; "
        "a page that has relations between two sections but no 'mentions' requires r2 == r3 and r2 > 0; the NOREL branch is unchanged. Every other feature, skip, threshold and line stays textually identical except the version line, the version comment (state the owner's decision and the reason) and the lines this one assertion needs. "
        "Show it: a unified diff of each new file against its old file, and the proof that the set of feature texts (feat/skip calls) is equal. Run the new test 9.35.1 once on a scratch rebuild or the shipped page of chapter 1 (a page with mentions: result equal to its stored result) and once on page 9.78.0 of chapter 10 (the assertion passes; other features as they were); about nine minutes per run. Commit the new files and a short evidence file (08-tooling/page-gates-evidence/tests_v9_34_1_v9_35_1.md). %s Satisfies the criterion ex:AC3P_Test." % (H["t34"], H["t35"], COMMON), ()).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1))
    L.append(G.task_block(tk3, "Measure the new template and the new page tests against the stored results of the existing pages", "Verify",
        "After the template (TK_PageGates_Template) and the tests (TK_PageGates_Test) are Done: (1) run the new tests 9.34.1 and 9.35.1 on each of the 14 shipped pages (the newest page of each chapter as it stands, key-substituted TEST copy by sen0401_lineage_page_test_run_v1_2_0.py with PAGE_TEST set; chapters 10 and 11: page 9.77.0) and compare with the stored result of that page (test_results_abox of its folder): equal or better; on a page that has mentions identical in failed and skipped; "
        "(2) rebuild the pages of chapters 1, 8, 12 and 14 into a scratch folder on the template 9.51.1 with the page builder v4_14_0 and the page-data builder that built each shipped page, run the new tests on each and compare with the stored result: equal to or better. Keep every run as a log under 08-tooling/page-gates-evidence/regression/ (a main-thread budget failure may be run again up to three times, every run kept; a [FAIL] is a result); do not ship the scratch pages. "
        "Report a table: page, stored widgets/features/failed/skipped, new run, equal/better/worse. If any page is worse, report it and stop: the versions are named failing. About 18 runs at nine minutes, run serially. %s Satisfies the criteria ex:AC3P_Regression (and, with the other two, ex:AC3P_Template and ex:AC3P_Test)." % COMMON, (tk1, tk2)).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1))
    sid = "ST_Page_Gates"
    L.append(G.story_block(sid, "The page template and page tests measure a page with section links by what it has, as new versions with the old ones kept",
                            "a new page template version and new page test versions that differ from the old only in the named parts, shown equal on the shipped pages",
                            "the pages of chapters 10 and 11 with section links can be rebuilt and measured by the page tests without a test assumption that does not hold and without overlapping boxes, and no shipped page changes its result",
                            "Del3_PageGates", "Obj3_PagesMeasured", "Cat_NewCapability", list(crits), [tk1, tk2, tk3], OWNER_ACT + " One criterion per unit (G133). " + FACTS).replace("ex:Out3_BacklogR2", NEWB).replace(G.ITER, ITER, 1).replace("Not scored: the owner decided on 2026-10-20 10:42 Istanbul that the gaps are closed first, so there is no ranking left to compute.", "Not scored: the owner directed this work on 2026-10-22, so there is no ranking left to compute."))

    L.append("ex:%s backlog:standsAlone true .\nex:Obj3_PagesMeasured backlog:metricMovableBy ex:%s, ex:ST_Section_Links .\n" % (sid, sid))
    L.append('''
ex:TC3P_G_Passes a backlog:TestCase ; rdfs:label "Run the page gate checks on the new files and the rebuilt pages and require no failure and no skip"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:AC3P_Template, ex:AC3P_Test, ex:AC3P_Regression, ex:AC3L2_Ch10, ex:AC3L2_Ch11 ; backlog:coversScenario ex:Scen3P_G_Passes ; backlog:runsOnData ex:Data3P_G_Passing ;
    backlog:hasCaseText "Run the checks of the criteria over the new template, the new tests and the rebuilt pages; they report no failure, the ERD label features run and pass, and the run exits 0 (the bridge runs recorded in this register are these runs)." .
ex:TC3P_G_Unchanged a backlog:TestCase ; rdfs:label "Run the new tests on a shipped page that has mentions and require the stored result"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:AC3P_Test, ex:AC3P_Regression ; backlog:coversScenario ex:Scen3P_G_Unchanged ; backlog:runsOnData ex:Data3P_G_Shipped ;
    backlog:hasCaseText "Run the tests 9.34.1 and 9.35.1 on the shipped pages; each equals its stored result; a difference names the new versions failing." .
ex:Data3P_G_Passing a backlog:TestData ; rdfs:label "The new template and test files and the pages of chapters 10 and 11 rebuilt on them"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest template, test and page files, for which every check of the criteria exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3P_G_Shipped a backlog:TestData ; rdfs:label "The 14 shipped pages as they stand on 2026-10-22 and their stored results"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The newest page of each chapter 1 to 14 in the course repository and the test_results_abox file stored beside it." .
''')
    # existing story and tasks
    old = "backlog:hasAcceptanceCriterion ex:AC3L_Ch10, ex:AC3L_Ch11 ;"
    i, j = T.blk(t, "ST_Section_Links"); b = t[i:j]; assert old in b
    t = t[:i] + b.replace(old, "backlog:hasAcceptanceCriterion ex:AC3L2_Ch10, ex:AC3L2_Ch11 ;", 1) + t[j:]
    for tk, ch, dep in (("TK_SecLinks_Ch10_Page", "10", "backlog:dependsOn ex:TK_SecLinks_Ch10_Research, ex:TK_SecLinks_Ch10_Consolidate, ex:TK_SecLinks_PageData ;"), ("TK_SecLinks_Ch11_Page", "11", "backlog:dependsOn ex:TK_SecLinks_Ch11_Research, ex:TK_SecLinks_PageData ;")):
        i, j = T.blk(t, tk); b = t[i:j]; assert dep in b, tk
        t = t[:i] + b.replace(dep, dep[:-2] + ", ex:%s, ex:%s, ex:%s ;" % (tk1, tk2, tk3), 1) + t[j:]
    for ch in ("10", "11"):
        L.append('ex:TK_SecLinks_Ch%s_Page backlog:hasAuditNote %s .\nex:TK_SecLinks_Ch%s_Verify backlog:hasAcceptanceCriterion ex:AC3L2_Ch%s ;\n    backlog:hasAuditNote %s .\nex:AC3L_Ch%s backlog:hasAuditNote %s .\nex:AC3T_Ch%s backlog:hasAuditNote %s .\n' % (
            ch, lit("Plan %s (change request ex:CR3_PageGates, owner's answer %s): this task is Suspended since v0.173 and is not begun again until %s, %s and %s are Done; when it resumes (T_Resume, with a new executor and a new brief) it rebuilds the page as a new page version 9.79.0 on the template 9.51.1 and runs the tests 9.34.1 and 9.35.1, and its criterion is ex:AC3L2_Ch%s. The text above that says 'unchanged tests' and 'template 9.51.0' is the text of the earlier plan and is read with these versions; a click-force workaround is never part of a result." % (now[:10], QUOTE, tk1, tk2, tk3, ch)),
            ch, ch, lit("Plan %s: the measure of the page of chapter %s on the new template and tests is the criterion ex:AC3L2_Ch%s; the elements of ex:AC3T_Ch%s are measured in the same run with the new test versions." % (now[:10], ch, ch, ch)),
            ch, lit("Note %s: replaced in ST_Section_Links by ex:AC3L2_Ch%s by the owner's decision on ex:CR3_PageGates (the tests named 'unchanged' here are changed by a new version, which the owner approved). This criterion is not edited. Its recorded result at v0.173 stays: NOT MET on page 9.78.0 (elements as printed there). It is history; the story no longer points to it." % (now[:10], ch)),
            ch, lit("Note %s: element 4 names the page tests 9.34.0 and 9.35.0. After the owner's decision on ex:CR3_PageGates (%s) it is measured with the new test versions 9.34.1 and 9.35.1, which differ from the old only in the one named assertion (proved by ex:AC3P_Test) and give the stored result on every shipped page (ex:AC3P_Regression). If that proof fails, the element stays NOT MET. The criterion is not edited." % (now[:10], QUOTE))))
    L.append('ex:ST_Section_Links backlog:hasAuditNote %s .\n' % lit("Plan %s (ex:CR3_PageGates, owner: %s): the story keeps its Done research and page-data tasks; its criteria are now ex:AC3L2_Ch10 and ex:AC3L2_Ch11 (the earlier AC3L_Ch10 and AC3L_Ch11, recorded NOT MET, stay as history and are not edited); its page tasks wait for the tasks of ST_Page_Gates in ex:Iter_16. The sprint goal of ex:Iter_14, frozen, says 'on the gates as they stand'; that cannot be met as worded after the owner's decision and the review of ex:Iter_14 records it." % (now[:10], QUOTE)))
    for x in [sid, tk1, tk2, tk3]:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n'
                 % (x, x, x, now, ITER, lit("Refined by the builder session from the owner's answer of %s (ex:CR3_PageGates): acceptance criteria with tools and versions, dependencies, and a brief to be generated; the task is startable when its dependencies are Done." % WHEN)))
    L.append('ex:Plan3P_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 16"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3P_G, ex:Scen3P_G_Passes, ex:Scen3P_G_Unchanged .\n'
             % (sid, sid, now, ITER, sid, ", ".join("ex:" + x for x in [tk1, tk2, tk3])))
    L.append('ex:Iter_16 a backlog:Iteration ; rdfs:label "Iteration 16: a new page template version and new page test versions, measured against the shipped pages"@en ; backlog:hasIdentifier "Iter_16" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-10-23T06:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        now, lit("Proposed by the builder session on 2026-10-22: the start is the instant of the planning ceremony ex:PC3_Iter_16; the proposed end is Friday 2026-10-23 06:00 UTC (09:00 Istanbul), the same end as ex:Iter_15. Justification: the critical path of this iteration is the template task and the test task in parallel (each one to two hours with its own scratch runs), then the regression task: 14 shipped pages and 4 rebuilt pages, about 18 page-test runs at nine minutes, serially about 3 hours, "
                    "plus the builder's control of each task and the bridge runs; about 8 to 10 hours of machine time in all, so the work started in the morning of 2026-10-22 ends the same day if nothing fails; 24 hours leave the margin for one repeat of a task. The tasks T4 to T6 (pages of chapters 10 and 11 and their Verify) follow in ex:Iter_14 (end 2026-10-24 06:00 UTC). The end is the owner's to decide; the plan stands whatever end he chooses."),
        lit("The new page template version 9.51.1 and the new page test versions 9.34.1 and 9.35.1 exist as new files with the old ones kept and byte-identical, differ from them only in the named parts, and give every shipped page the result its stored result has, and the pages of chapters 1, 8, 12 and 14 rebuilt on the new template an equal or better one, on the gates as they stand otherwise, each unit that fails named; then the pages of chapters 10 and 11 are rebuilt on them in ex:Iter_14. Frozen at the planning ceremony."),
        ", ".join("ex:" + x for x in [sid, tk1, tk2, tk3])))
    L.append('ex:PB3P_Iter_16 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 16 when it was planned"@en ; backlog:baselineFor ex:Iter_16 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-10-23T06:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_16 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 16: the page gates"@en ; backlog:ceremonyFor ex:Iter_16 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3P_%s ;\n    rdfs:comment %s@en .\n' % (
        now, sid, lit("Held %s by the builder session, after the owner's answer of %s (ex:CR3_PageGates): the story %s and its three tasks are committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of each executor session, with its brief." % (now, WHEN, sid))))
    L.append('ex:SC3_PageGates a backlog:ScopeChange ;\n    rdfs:label "Scope grown by a new page template version and new page test versions"@en ;\n    backlog:fulfillsRequest ex:CR3_PageGates ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        sid, lit(OWNER_ACT + " The boundary moved outward by one story; the exclusion of any change to a gate or a test is lifted for exactly the two named changes, as new files beside the old ones, measured against the stored results of the shipped pages.")))
    t, kk = re.subn(r'(ex:CR3_PageGates a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('ex:CR3_PageGates rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_PageGates and the story it admits; it was Pending before. Accepted for option A by the owner\'s answer of %s."@en .\n' % (now[:10], WHEN))
    L.append("ex:Iter_14 backlog:containerDependsOn ex:Iter_16 ; backlog:derivedContainerDependency ex:Iter_16 .\n")
    t += "\n" + "".join(L)
    # Iter_14 keeps its members; nothing changes there
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR7", "Out3_ObjectiveR5"), ("third lineage, Backlog stage rebuilt for the page gates: story ST_Page_Gates with three tasks (template, tests, regression) and three criteria measured with named tools and versions, the successor criteria AC3L2_Ch10 and AC3L2_Ch11, "
                                                                           "dependencies of the page tasks of chapters 10 and 11 extended, the new iteration Iter_16 with sprint goal, plan baseline and ceremony, the ScopeChange that admits the story, the change request Accepted; %d carried items re-admitted, not re-dated." % n)


def ev_fill(t, prev):
    t = G.fill_re(t, NEWB, prev)
    return t, "closedAtCommit of the rebuilt Backlog output ex:Out3_BacklogR7 set to the commit that closed it (%s); the revision is complete and no work is begun." % prev


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
