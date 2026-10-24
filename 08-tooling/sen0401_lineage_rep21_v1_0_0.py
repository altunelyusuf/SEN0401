"""sen0401_lineage_rep21 v1_0_0 - change route (rulings G113, G120, G125, G127, G129, G133, G136) for the decisions that the lineage takes itself under the owner's standing rule of 2026-10-24 (relayed by the course coordinator): a lineage never waits on questions unrelated to its work; when the answerer is not a person, the lineage's agentic system decides without a handover; work the lineage enforces but the actual work misses must be dealt with; progress must not need expensive switch-overs.
Decisions: (1) the page criteria of chapters 7 and 8 are RESTATED on the page test 9.37.0 (the race of 9.36.0 on the 'Running...' placeholder is a defect of the gate, repaired by a new test file and controlled MET in v0.258.0; nothing is loosened; the old criteria stay as history and unmet) as new stories with new Build and Verify tasks: the page of chapter 7 is built on the re-issued deck, the page 9.85.0 of chapter 8 gets its checks, its stored result and its Stage 4 ABox as new files (it is not rebuilt); (2) the regression criterion of the tools story is restated on template 9.52.2 and carried; (3) the superseded items are withdrawn in the next version.
Same route as sen0401_lineage_rep20 (ChangeRequest + ImpactAssessment, StageRevision from the Scope stage, outputs rebuilt one per version, a last version fills the last commit).
Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_section_links_v1_0_0 as SL
import sen0401_lineage_ch78_rev_v1_0_0 as R
lit = G.lit
CR = "ex:CR3_Repair21"; IA = "ex:IA3_Repair21"; REV = "ex:Revision_Lineage3_Scope10"
ACTIVE = ["ex:Out3_ScopeR10", "ex:Out3_GoalR10", "ex:Out3_ObjectiveR10", "ex:Out3_BacklogR12"]; NEWB = "ex:Out3_BacklogR13"; R.NEWB = NEWB
ITN = "ex:Iter_23"; R.IT1 = ITN; ENDN = "2026-10-25T12:00:00"
WHEN = "Saturday 2026-10-24, decided by the lineage's own change route under the owner's standing rule of the same day (relayed by the course coordinator): a lineage never waits on questions unrelated to its work; when the answerer is not a person, the lineage's agentic system decides without a handover; work the lineage enforces but the actual work misses must be dealt with; progress must not need expensive switch-overs"
F_P37 = ("MEASURED (control of the page test 9.37.0, register v0.258.0, evidence bridge, logs in 08-tooling/verify/iter22/pagetest937 and pagetest937_bridge, every page run by the builder under flock /tmp/page_test.lock, one at a time): the page test 9.36.0 is byte-identical (SHA-256 85afebf6..., git log shows only d4880a3); the diff to 9.37.0 holds the version string, one comment and the P2 wait; fixture a (slow example with a visual) passes P2 under 9.37.0 and fails under 9.36.0 (the race); fixture b (text only) fails P2 under 9.37.0 with 'result is text, not a visualisation'; fixture c (never ends) fails P2 within the 90 s bound; "
         "the pages 9.83.0 of chapters 5 and 6 give 398 passed 0 failed under 9.37.0 (the same as under 9.36.0); the page 9.85.0 of chapter 8 gives 394 passed 0 failed under 9.37.0 and failed P2 on examples 17 and 18 under 9.36.0 (the root cause is recorded in AC7R_PageTest937: the placeholder 'Running...' read as a result after 300 ms). The race is a defect of the gate, not a waiver: the criteria are restated on 9.37.0 and every other element, threshold and the no-skip rule are kept.")
F_RULE = "RULE: " + WHEN + "."


def ac_page(t, old, new, label_old, nn):
    i, j = T.blk(t, old); b = t[i:j]; assert "9.36.0" in b
    b = b.replace("ex:" + old + " ", "ex:" + new + " ", 1)
    b = b.replace(label_old, label_old, 1)
    b = b.replace("TS_PageTest36", "TS_PageTest37").replace("page test 9.36.0 (Playwright 1.56.0)", "page test 9.37.0 (new file over 9.36.0, controlled in v0.258.0; Playwright 1.56.0)").replace("9.36.0", "9.37.0")
    b = b.replace("coveredByCase ex:TC3I_P_Passes, ex:TC3I_P_NotClaimed", "coveredByCase ex:TC8R_%s_Passes, ex:TC8R_%s_NotClaimed" % (nn, nn))
    pre = ("RESTATED by " + CR + " from ex:" + old + " (" + WHEN + "). The only changes: the page test named is 9.37.0 instead of 9.36.0 (" + F_P37 + ") ")
    if nn == "Ch07":
        old_g = "Given the rebuilt deck of chapter 7 with its manifest and the newest page of chapter 7"; assert old_g in b
        b = b.replace(old_g, "Given the RE-ISSUED deck of chapter 7 v2_1_0 (03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx, controlled MET in v0.257.0) with its manifest chapter_code_ch07_v1_1_0.json (a NEW file written first by the task: the same 15 examples in the same order and names as chapter_code_ch07_v1_0_0.json, whose deck field names v2_0_0, with the deck field naming v2_1_0) and the newest page of chapter 7")
        pre += "and the deck and its manifest are those of the re-issue (controlled MET in v0.257.0); nothing else is loosened. The old criterion stays as history and is not met."
    else:
        old_g = "Given the rebuilt deck of chapter 8 with its manifest and the newest page of chapter 8 (03-materials/ch08/page/sen0401_ch08_page_v9_77_0.html), when the page is rebuilt as a new file with the page version 9.85.0 on the template 9.52.2 with the builders v4_15_0 and v2_24_0, then ALL of:"
        assert old_g in b, "ch8 given"
        b = b.replace(old_g, "Given the deck of chapter 8 v2_0_0 with its manifest chapter_code_ch08_v1_0_0.json and the page 9.85.0 of chapter 8 (03-materials/ch08/page/sen0401_ch08_page_v9_85_0.html, built on the template 9.52.2 with the builders v4_15_0 and v2_24_0 by executor SEN0401-I20-page-ch08, commits 75e0a47 and 0e34361, and NOT edited: the control of v0.255.0 found only P2 failing), when its checks are run, its stored page-test result and its Stage 4 page ABox are written as new files, then ALL of:")
        pre += "and the page 9.85.0 is not rebuilt, because the control found nothing else failing; what the executor did not make (the stored page-test result and the Stage 4 page ABox) is made now as new files. The old criterion stays as history and is not met."
    b = b.replace('backlog:hasGherkinText "', 'backlog:hasGherkinText "' + pre.replace('"', "'").replace("\\", "") + " ", 1)
    b = re.sub(r'rdfs:label "[^"]*"@en', 'rdfs:label "The page of chapter %s meets the page standard on the page test 9.37.0 (restated), with its character set first"@en' % nn[2:].lstrip("0"), b, count=1)
    return b


TXT_REG = ("Owner-directed work (ex:CR3_Remedy56), RESTATED by " + CR + " from ex:AC4R_Regress (" + WHEN + "): the control set is built on the template that is now in use, 9.52.2, instead of 9.52.0 (replaced by 9.52.1 and 9.52.2, which the controls of Iterations 18 and 19 passed); nothing else is changed. Given the template 9.52.2, the builders v4_15_0 and v2_24_0 and the page tests 9.34.1 and 9.35.1, when the pages of chapters 1 and 10 are built into a scratch folder on the template 9.52.2 and the page tests 9.34.1 and 9.35.1 are run on each, serially, under flock /tmp/page_test.lock, then ALL of: "
           "(1) each of the 4 runs ends exit 0 with RESULT PASS, no [FAIL], and widgets, features and gates not below the stored result of the shipped page, skipped features not more and each of them one the stored result skips; (2) every run is kept as a log; (3) no committed file is edited, the scratch pages are not shipped; results as printed; if any element fails the template is named failing. "
           "Control set justified: the template is a new file used only by pages built from it; the shipped pages stay on their files, so their results cannot move. The old criterion stays as history and is not met; the task that carried it (TK_Remedy_Regress) is withdrawn because it named the template 9.52.0 that no page uses.")


def txt_ch8_task():
    return ("Finish the page 9.85.0 of chapter 8 without rebuilding it (the control of v0.255.0 found the page failing only the page test 9.36.0 on P2, a defect of the gate that the page test 9.37.0 repairs; the executor of the page stopped before it made the stored result and the Stage 4 ABox). "
            "WITH the page 9.85.0 as it is (03-materials/ch08/page/sen0401_ch08_page_v9_85_0.html, not edited): run the page charset check; run the page tests 9.37.0, 9.34.1 and 9.35.1 (the runner with PAGE_TEST, serially, each under `flock /tmp/page_test.lock`), keep every log; store the result as a NEW test_results file (as the pages of chapters 5 and 6 did) and build the Stage 4 page ABox with the Stage 4 builder as a NEW file; run the Stage 4 gate runner v1_1_0 for 8, the Research, Deck and Page chapter checks (the Page check runs the page test: use 9.37.0 via the check wrapper or state how it was run), the deck match check and the manifest check. "
            "If the page fails any feature other than P2 under 9.37.0, STOP and report it: the page is rebuilt then as a new page 9.86.0 by a further task, never edited. " + F_P37 + " " + R.NOEDIT + " Report every result as printed (PASS, FAIL, NOT_MEASURED, CANNOT_RUN); a skip is not a pass. The machine has 2 cores: browser tests run one at a time and no build runs beside them.")


def old_note(t, tid):
    i, j = T.blk(t, tid); b = t[i:j]; m = re.search(r'backlog:hasAuditNote "(.*)" \.\s*$', b, re.S); assert m, tid
    return m.group(1).replace('\\"', '"').replace("\\\\", "\\").split(" Planned session")[0]


def task_ch7(t):
    n = old_note(t, "TK_Ch07_Page_Build"); assert "9.36.0" in n and "chapter_code_ch07_v1_0_0.json" in n
    n = n.replace("the deck's NEW chapter-code manifest chapter_code_ch07_v1_0_0.json", "the NEW manifest chapter_code_ch07_v1_1_0.json (written first, see the start of this note)").replace("9.36.0", "9.37.0")
    pre = ("RESTATED page task of chapter 7 (it replaces TK_Ch07_Page_Build, withdrawn by the same route " + CR + ": the criterion now names the page test 9.37.0, which repairs the race of 9.36.0 on the placeholder 'Running...'; " + F_P37 + ") "
           "FIRST write the NEW manifest 03-materials/ch07/page/chapter_code_ch07_v1_1_0.json: a copy of chapter_code_ch07_v1_0_0.json (which stays unchanged) whose 'deck' field names SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx; its 15 examples, their order and their names are unchanged (measured equal to the code slides of the deck v2_1_0 in the control of v0.257.0). Run the deck control check v1_1_0 (manifest) against it and the deck v2_1_0 (if the check takes the manifest from the deck name alone, state how you ran it; do not edit the check). "
           "THEN build the page from the deck v2_1_0 (the lecture export and the stories made from it) and this manifest. ")
    return pre + n


def txt_ch7_verify():
    return ("Re-run serially, each browser run under `flock /tmp/page_test.lock`: the charset check and the page tests 9.37.0, 9.34.1 and 9.35.1, the Stage 4 gate runner v1_1_0, the Research, Deck and Page chapter checks, the deck match check and the manifest equality (the chapter-code tab equals the deck's code order, from chapter_code_ch07_v1_1_0.json); record every result as printed. " + F_P37)


def txt_ch8_verify():
    return ("Re-run serially, each browser run under `flock /tmp/page_test.lock`: the charset check and the page tests 9.37.0, 9.34.1 and 9.35.1 on the page 9.85.0, the Stage 4 gate runner v1_1_0 for 8, the Research, Deck and Page chapter checks, the deck match check and the manifest equality; check that the stored result and the Stage 4 ABox are new files and that no committed file is edited; record every result as printed. " + F_P37)


def txt_regress():
    return ("Build the pages of chapters 1 and 10 into a scratch folder on the template 9.52.2 (pass it with PAGE_TEMPLATE) with the page builder v4_15_0 and the page-data builder v2_24_0 and run the page tests 9.34.1 and 9.35.1 on each (serially, each under `flock /tmp/page_test.lock`, a run is about nine minutes, every run kept as a log): each result must equal or beat the stored result of the shipped page; the scratch pages are not shipped and no committed file is edited. Carried from TK_Remedy_Regress, which named the template 9.52.0; the criterion is restated on 9.52.2. A failing result is not worked around: the template is then named failing.")


def story_notes():
    return "Restated " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment " + IA + "."


def specs():
    return [("AC8R_Page_Ch07", "TC8R_Ch07"), ("AC8R_Page_Ch08", "TC8R_Ch08"), ("AC8R_Regress", "TC8R_Reg")]


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Page criteria of chapters 7 and 8 restated on the page test 9.37.0, and the regression criterion carried, by the lineage under the owner standing rule of 2026-10-24"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_Repair20 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit(F_RULE + " " + F_P37 + " The criteria of the pages of chapters 7 and 8 (ex:AC7_Page_Ch07, ex:AC7_Page_Ch08) name the page test 9.36.0, whose P2 wait is a defect; the question whether the criteria may name 9.37.0 was asked of the owner and is not awaited under the rule: the race is a defect in the gate, not a waiver. The change grows the scope by one deliverable: the restated page criteria with new stories, and the regression criterion on the current template; nothing existing is edited; the old criteria stay as history. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the restated page criteria cost and what they unblock, measured before they are started"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Repair20 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(F_P37 + " AFFECTED: ST_Ch07_Page and ST_Ch08_Page (their criteria name 9.36.0; the stories are withdrawn in the next version after their replacements exist), ST_Ch07_Deck (superseded by the re-issue), the three old stories of Iterations 17 and 18 (settled by the same route), ST_Remedy_Tools (its regression criterion is carried). NOT AFFECTED: the template, the builders, the tests 9.34.1, 9.35.1, 9.36.0 and 9.37.0 (no file edited), every other deck and page, the Mission outcome and the Achieved status. "
                    "PLAN (route as ex:CR3_Repair20, G127): a StageRevision from the Scope stage, seven versions; then one version for the withdrawals and the old stories, one for the ranking (BP-D10), one for work begun. New iteration Iter_23 (start at planning, proposed end Sunday 2026-10-25 12:00 UTC) with three stories and five tasks: the page of chapter 7 (about 1.5 h executor, 1.0 h verification), the finish of the page 9.85.0 of chapter 8 (about 1.0 h and 0.5 h), the regression on template 9.52.2 (about 1.0 h, builder). "
                    "COST: new files only; a failing criterion is named failing; nothing is waived. ORDER: the two page builds start at once (their dependencies are Done: the deck v2_1_0 and the page test 9.37.0 are controlled MET); browser runs are serialised by the lock."))
    return t + cr + ia, "ChangeRequest %s (Pending) with its ImpactAssessment: the page criteria of chapters 7 and 8 restated on the page test 9.37.0 and the regression criterion carried, decided by the lineage under the owner's standing rule of 2026-10-24." % CR


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (the restated page criteria and their stories); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its impact assessment " + IA + " were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the builder role under the owner's standing rule.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the page criteria of chapters 7 and 8 restated on 9.37.0"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the restated page criteria of chapters 7 and 8: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The page criteria of chapters 7 and 8 restated on the page test 9.37.0, the page of chapter 7 built on the re-issued deck, the page 9.85.0 of chapter 8 finished, and the regression criterion carried onto the current template"
    tx = ("The page of chapter 7 built as a new file on the re-issued deck v2_1_0 and its manifest v1_1_0, the page 9.85.0 of chapter 8 given its checks, stored result and Stage 4 ABox as new files, both measured by the page test 9.37.0 (a new file; 9.36.0 stays) with every other element of the old criteria kept; the regression of the template 9.52.2 on the old page tests measured on pages of chapters 1 and 10. " + F_P37 + " " + F_RULE)
    L = ('\nex:Del3_Repair21 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n'
         '    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Repair21 ; rdfs:seeAlso %s, %s .\n" % (CR, IA)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-24 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (the restated page criteria). No exclusion changes: new files only; the exclusion of changes to gates, tests and thresholds still holds (9.37.0 is a new test file; the criteria name it by this change route, no gate is loosened)." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR11", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the restated page criteria: one deliverable in the existing area."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR11", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Repair21 a backlog:Goal ;
    rdfs:label "The pages of chapters 7 and 8 are measured by a page test that waits for the end of an example, without loosening any element"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR11 .
ex:G3_Repair21 rdfs:comment "Drafted by the builder session on 2026-10-24 from the change request %s; the intent origin is therefore Derived."@en .
ex:Spec3I_Repair21 a backlog:Specification ;
    rdfs:label "What it is for a restated page criterion to be met"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Repair21 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR11 .
ex:Spec3I_Repair21_Pass a backlog:TestScenario ; rdfs:label "A page built or finished as new files passes its restated criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Repair21 ; backlog:hasScenarioText %s .
ex:Spec3I_Repair21_Fail a backlog:TestScenario ; rdfs:label "A page with a text-only example, or a committed file edited, is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Repair21 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request " + CR + ": the page criteria of chapters 7 and 8 measured with a page test (9.36.0) that reads the placeholder 'Running...' as a result; the repair is a new test file (9.37.0), controlled MET. " + F_P37 + " " + F_RULE),
       CR, lit("A restated page criterion is met when every element of it is measured on the evidence bridge as met under the page test 9.37.0, the output files are new, and no committed file is edited; a page whose example ends with text only still fails."),
       lit("Given the page of chapter 7 built on the re-issued deck, or the page 9.85.0 of chapter 8, when the checks and the page tests 9.37.0, 9.34.1 and 9.35.1 are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given a page whose chapter-code example ends with text only, or a task that edits a committed file, when the page test 9.37.0 or the nochange check is run, then P2 fails or the check prints status M, and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR11", "Out3_ScopeR11"), "third lineage, Goal stage rebuilt for the restated page criteria: one goal with a specification and two scenarios."


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR11", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Repair21 a backlog:Objective ; rdfs:label "Restated page criteria and the carried regression met on verified evidence: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Repair21 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Repair21 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Repair21 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR11 .
ex:Met3_Repair21 a backlog:Metric ; rdfs:label "restated criteria (page of chapter 7, page of chapter 8, regression) whose story is Done on verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Repair21 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the restated stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the three restated criteria, so the count is read from verified runs." ; backlog:expectedValue "3"^^xsd:decimal .
ex:ObsR21_Baseline a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Repair21 ; backlog:observationFor ex:Obj3_Repair21 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Repair21 rdfs:comment "Drafted by the builder session on 2026-10-24 from the change request %s; the intent origin is therefore Derived."@en .
''' % (lit("Count of the three restated criteria (page of chapter 7, page 9.85.0 of chapter 8, regression on template 9.52.2) whose story is Done on bridge-verified evidence."), now,
       lit("Baseline from the controls of 2026-10-24 (v0.255.0 and v0.258.0): none of the three restated criteria is met yet, so 0 of 3."), CR)
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR11", "Out3_GoalR11"), "third lineage, Objective stage rebuilt for the restated criteria: one objective (0 to 3) with metric, checkpoint and baseline reading."


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR11", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR12"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    nt7 = task_ch7(t)
    acs = {"AC8R_Page_Ch07": ac_page(t, "AC7_Page_Ch07", "AC8R_Page_Ch07", "", "Ch07"), "AC8R_Page_Ch08": ac_page(t, "AC7_Page_Ch08", "AC8R_Page_Ch08", "", "Ch08")}
    L = []
    for c, b in acs.items(): L.append("\n" + b)
    L.append('\nex:AC8R_Regress a backlog:AcceptanceCriterion ; rdfs:label "The template 9.52.2 gives the old page tests the stored result on a control set of pages built from it"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS_PageTemplateE, ex:TS_PageBuilder415, ex:TS_PageData224, ex:TS_PageTest34b, ex:TS_PageTest35b ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the logs of the runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC8R_Reg_Passes, ex:TC8R_Reg_NotClaimed .\n' % (lit(TXT_REG), lit("page template 9.52.2 (course_page_template_v9_52_2.html); page builder v4_15_0 and page-data builder v2_24_0; page tests 9.34.1 and 9.35.1; Playwright 1.56.0")))
    for c, k in specs():
        L.append('''ex:%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the restated criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(c)s ; backlog:coversScenario ex:Spec3I_Repair21_Pass ; backlog:runsOnData ex:Data3S_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion; they report no failure and exit 0." .
ex:%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the item that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(c)s ; backlog:coversScenario ex:Spec3I_Repair21_Fail ; backlog:runsOnData ex:Data3S_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks on the finding as measured (the page 9.85.0 under 9.36.0, a text-only fixture, a committed file with status M) and require that nothing is claimed for it." .
ex:Data3S_%(k)s_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3S_%(k)s_Failing a backlog:TestData ; rdfs:label "The finding that fails the checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The finding as measured on 2026-10-24 (ex:IA3_Repair21)." .
''' % dict(k=k, c=c))
    STORIES = [("ST_Ch07_Page_R", "The page of chapter 7 is built on the re-issued deck and meets the page standard on the page test 9.37.0", ["AC8R_Page_Ch07"], ["TK_Ch07_Page_Build_R", "TK_Ch07_Page_Verify_R"]),
               ("ST_Ch08_Page_R", "The page 9.85.0 of chapter 8 is finished and meets the page standard on the page test 9.37.0", ["AC8R_Page_Ch08"], ["TK_Ch08_Page_Finish", "TK_Ch08_Page_Finish_Verify"]),
               ("ST_Remedy_Regress_R", "The template 9.52.2 gives the old page tests the stored result on a control set of pages", ["AC8R_Regress"], ["TK_Remedy_Regress_R"])]
    D7 = ["TK_Ch07_Deck_Reissue_Verify", "TK_Charset_Template_Verify", "TK_Charset_Check_Verify", "TK_PageTest937_Verify"]
    TASKS = [("TK_Ch07_Page_Build_R", "Build the page of chapter 7 on the re-issued deck with the chapter-code tab", "Build", D7, "SEN0401-I23-page-ch07", "S", 1.5, "Ready", nt7),
             ("TK_Ch07_Page_Verify_R", "Verify the rebuilt page of chapter 7", "Verify", ["TK_Ch07_Page_Build_R"], "builder", "S+1.5h", 1.0, "Proposed", txt_ch7_verify()),
             ("TK_Ch08_Page_Finish", "Finish the page 9.85.0 of chapter 8: checks on the page test 9.37.0, stored result and Stage 4 ABox as new files", "Build", ["TK_Ch08_Deck_Verify", "TK_Charset_Template_Verify", "TK_Charset_Check_Verify", "TK_PageTest937_Verify"], "SEN0401-I23-page-ch08", "S", 1.0, "Ready", txt_ch8_task()),
             ("TK_Ch08_Page_Finish_Verify", "Verify the finished page 9.85.0 of chapter 8", "Verify", ["TK_Ch08_Page_Finish"], "builder", "S+1.0h", 0.5, "Proposed", txt_ch8_verify()),
             ("TK_Remedy_Regress_R", "Measure the template 9.52.2 against the old tests on a control set of pages built from it", "Verify", ["TK_Charset_Template_Verify", "TK_PageTest937_Verify"], "builder", "after the page builds", 1.0, "Ready", txt_regress())]
    for sid, title, crits, tks in STORIES:
        L.append(R.story_block(sid, title, "Del3_Repair21", "Obj3_Repair21", crits, tks, story_notes(), ITN, "Ready"))
    for tid, title, ttype, deps, sess, est, hrs, state, note in TASKS:
        L.append(R.task_block(tid, title, ttype, deps, sess, est, hrs, note, ITN, state, True))
    for sid, *_ in STORIES: L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for x in [s[0] for s in STORIES] + [x[0] for x in TASKS]:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, ITN, lit("Refined by the builder session from the change request %s and the measured facts of %s: acceptance criterion with tool and version, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, crits, tks in STORIES:
        L.append('ex:Plan3S_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 23"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Repair21, ex:Spec3I_Repair21_Pass, ex:Spec3I_Repair21_Fail .\n' % (sid, sid, now, ITN, sid, ", ".join("ex:" + x for x in tks)))
    L.append("ex:Obj3_Repair21 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STORIES))
    m3 = [s[0] for s in STORIES] + [x[0] for x in TASKS]
    L.append('%s a backlog:Iteration ; rdfs:label "Iteration 23: the pages of chapters 7 and 8 on the page test 9.37.0"@en ; backlog:hasIdentifier "Iter_23" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        ITN, now, ENDN, lit("Proposed by the builder session on 2026-10-24 under the owner's standing rule: the start is the instant of the planning ceremony ex:PC3_Iter_23; the proposed end is Sunday 2026-10-25 12:00 UTC. Justification (estimates, not measurements): the page of chapter 7 about 1.5 h build and 1.0 h verification, the finish of the page of chapter 8 about 1.0 h and 0.5 h, the regression about 1.0 h of serial browser time; the two executors work in parallel and every browser run is serialised by the lock."),
        lit("The page of chapter 7 is built on the re-issued deck and the page 9.85.0 of chapter 8 is finished, both measured by the page test 9.37.0 with every other element of the old criteria kept, verified by the evidence bridge; the regression of the template 9.52.2 is measured; nothing existing is edited. Frozen at the planning ceremony."), ", ".join("ex:" + x for x in m3)))
    L.append('ex:PB3S_Iter_23 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 23 when it was planned"@en ; backlog:baselineFor %s ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (ITN, now, now, ENDN))
    L.append('ex:PC3_Iter_23 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 23: the pages of chapters 7 and 8"@en ; backlog:ceremonyFor %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent %s ;\n    rdfs:comment %s@en .\n' % (ITN, now, ", ".join("ex:Plan3S_" + s[0] for s in STORIES), lit("Held %s by the builder session after the change request %s: three stories and five tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief." % (now, CR))))
    L.append('ex:SC3_Repair21 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the page criteria of chapters 7 and 8 restated on the page test 9.37.0"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STORIES), lit("Decided by the owner through his standing rule of 2026-10-24, which the builder role applied (" + WHEN + "). The decider recorded is the Owner because the rule is his decision; the builder role did the recording. The boundary moved outward by three stories; new files only; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Repair21 and the stories it admits; it was Pending before. Decided by the lineage under the owner standing rule of 2026-10-24; the coordinator tells the owner afterwards."@en .\n' % (CR, now[:10]))
    L.append('ex:AC7R_PageTest937 rdfs:seeAlso ex:AC8R_Page_Ch07, ex:AC8R_Page_Ch08 ;\n    backlog:hasAuditNote %s .\n' % lit("Disclosure %s (%s): the words of this criterion that the page test 9.37.0 'enters no criterion until the owner answers' and its clause (5) 'is NOT used in any other criterion' were conditions on the task TK_PageTest937_Build while the owner's question was open; the task was Done as controlled in v0.258.0 and is not edited (G125). The owner's standing rule of 2026-10-24 settles the question without a handover: ex:AC8R_Page_Ch07 and ex:AC8R_Page_Ch08 name 9.37.0 by the change route %s, with the race as the recorded defect of the gate and no element loosened." % (now[:10], WHEN, CR)))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR13", "Out3_ObjectiveR11"), "third lineage, Backlog stage rebuilt for the restated page criteria: Iteration 23 (three stories, five tasks, planned), criteria with tools and versions, the ScopeChange; the change request Accepted; the %d carried items are re-admitted, not re-dated." % n


def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__": main()
