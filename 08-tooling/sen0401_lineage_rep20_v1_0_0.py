#!/usr/bin/env python3
"""sen0401_lineage_rep20 v1_0_0 - change route (rulings G113, G120, G125, G127, G129, G133, G136) for the three repairs ordered by the course coordinator on Saturday 2026-10-24 after the controls of the same day:
  (1) the deck of chapter 7 re-issued as v2_1_0 in NEW files (control v0.244.0: element (4) not met, 27d36a5 edited four files of ed03d15 in place);
  (2) the page test 9.37.0 as a new file (the P2 race of 9.36.0 on the 'Running...' placeholder, measured on the page 9.85.0 of chapter 8; it does not enter any criterion until the owner answers);
  (3) the remainder of ST_Section_Links (chapter 11 page, Iter_14 ended 2026-10-24 06:00 UTC) split into a story of Iter_21 whose Verify task waits for the retrofit page of chapter 11.
Same route as ex:CR3_Ch78 (sen0401_lineage_ch78_rev): ChangeRequest + ImpactAssessment, StageRevision from the Scope stage (G127), Scope, Goal, Objective and Backlog outputs rebuilt one per version, a last version fills the last commit.
The withdrawal of the superseded tasks, the ranking, the work begun and the briefs are separate versions (sen0401_lineage_rep20_after_v1_0_0.py, rank v1_2_0, work begun v1_11_0).
Usage: change | retract | scope PREV | goal PREV | objective PREV | backlog PREV | fill PREV    (one call = one new file = one event; the caller validates and commits each alone)"""
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
CR = "ex:CR3_Repair20"; IA = "ex:IA3_Repair20"; REV = "ex:Revision_Lineage3_Scope9"
ACTIVE = ["ex:Out3_ScopeR9", "ex:Out3_GoalR9", "ex:Out3_ObjectiveR9", "ex:Out3_BacklogR11"]; NEWB = "ex:Out3_BacklogR12"; R.NEWB = NEWB
IT3 = "ex:Iter_22"; R.IT1 = IT3; IT2 = "ex:Iter_21"; END3 = "2026-10-25T09:00:00"
WHEN = "Saturday 2026-10-24, the course coordinator's order after the controls of the same day (v0.244.0) and the owner's rule that repairs re-rank the open items"
F_DECK = ("MEASURED (control of 2026-10-24, register v0.244.0, logs in 08-tooling/verify/iter20/deck_ch07_bridge): the deck of chapter 7 v2_0_0 (61 slides, 15 examples, executor commits ed03d15 and 27d36a5): deck standard check D1 to D12 PASS=12 FAIL=0, overlap check clean, Deck chapter check PASS, manifest equals the 15 code slides, deck match check 0 not carried, every slide viewed zoomed; "
          "the element 'no committed file edited' is NOT MET: the commit 27d36a5 modified in place four files that the commit ed03d15 had added (03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_0_0.pptx, 08-tooling/ch07-deck/deck_build_v2_0_0.py, deck_plan_v2_0_0.json, sen0401_ch07_deck_v2_0_0.pptx; the nochange check prints status M for each).")
F_P2 = ("MEASURED (executor SEN0401-I20-page-ch08, commits 75e0a47 and 0e34361; builder's root-cause analysis 2026-10-24): the page 9.85.0 of chapter 8 fails the page test 9.36.0 on feature P2 only: examples 17 and 18 are judged 'result is text, not a visualisation'; the page tests 9.34.1 and 9.35.1 pass. "
        "ROOT CAUSE: the test waits for the result element to hold any non-empty text, the template 9.52.2 writes the placeholder 'Running...' into that element when an example starts, so the wait ends at once; the test then waits 300 ms and reads. Examples that take longer than about 0.3 s (17: 0.7 s, 18: 1.3 s on the machine) are read while the placeholder is still shown. The diagnostic log 08-tooling/ch08-page/iter20_logs/ch08_9_85_0_diag_p2_timing.log shows that both examples do show a visual when they finish. "
        "The pages of chapters 5 and 6 pass because all their examples finish within 0.3 s (one chapter 5 run failed once under load); the SEN0414 page test carries the same code. "
        "CHOICE by rule and fact: the template placeholder is correct behaviour for a reader and lighter example code would change the teaching content to suit the test; a defective gate is repaired by a new test file (the precedent of 9.34.1 and 9.35.1), so a new test file 9.37.0 is made. It enters no criterion until the owner answers the question that is asked.")
F_L4 = ("MEASURED: Iteration 14 ended at 2026-10-24T06:00 UTC; the story ST_Section_Links is open in it (chapter 10 delivered; TK_SecLinks_Ch11_Page Suspended since 2026-10-22, TK_SecLinks_Ch11_Verify Proposed), so the validator reports L4 on it ('split the remainder into a story that fits the next iteration'). The chapter 11 page is rebuilt anyway by TK_Ch11_Page_Build of Iteration 21 on template 9.52.2, which contains the section-link ERD, so the remainder is a Verify task that waits for that page.")


def txt_deck():
    return ("Owner-directed work (" + CR + ", " + WHEN + "). Given the deck of chapter 7 v2_0_0 (controlled 2026-10-24: all elements met except that 27d36a5 edited files of ed03d15 in place) and the chapter research, when the deck is RE-ISSUED as the NEW files "
            "03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx, 08-tooling/ch07-deck/deck_build_v2_1_0.py, deck_plan_v2_1_0.json and the shipped copy sen0401_ch07_deck_v2_1_0.pptx (the manifest chapter_code_ch07_v1_0_0.json stays; a changed order or name of the code slides needs a new manifest version), then ALL of: "
            "(1) the deck standard check reports every element D1 to D12 met and exits 0, no NOT_MEASURED; (2) the Deck chapter check v1_3_0 for Deck/Ch07 passes, the deck overlap check is clean and the deck match check reports 0 not carried; (3) the manifest lists the deck's code examples in slide order and the order equals the order of the code slides (deck control check v1_1_0); "
            "(4) every commit of the executor in this task adds files only (the nochange check over its commits prints status A for every file; no file of an earlier commit, the executor's own logs and the v2_0_0 files included, is modified; each log is written once, after its run is complete, and committed once); (5) results are reported as printed; if any element fails the deck is named failing and this criterion has no passing result. " + F_DECK + " " + R.STD_D)


def txt_test():
    return ("Owner-directed work (" + CR + ", " + WHEN + "). Given the page test 9.36.0 (byte-identical after the task) and the template 9.52.2, when the NEW file 08-tooling/sen0401_page_test_v9_37_0.py is written from sen0401_page_test_v9_36_0.py, changing ONLY the P2 wait: after a chapter-code example is run the test waits until the result element no longer shows the placeholder 'Running...' (and holds text or a visual), within the bound that the wait has today (90 s per example), then ALL of: "
            "(1) the file is new and v9_36_0 is byte-identical (SHA-256 before and after); (2) the unified diff against 9.36.0 is limited to that wait (and the version strings); every other feature, threshold and message is unchanged; "
            "(3) FIXTURES, built by the executor as new files in 08-tooling/page-test-937-fixtures/ and re-run by the builder on the bridge: (a) a page whose example takes 1.5 s and then shows a visual: 9.36.0 fails P2 on it (the race) and 9.37.0 passes it; (b) a page whose example ends with text only and no visual: 9.37.0 FAILS P2 with 'result is text, not a visualisation' (the gate is not weakened); (c) a page whose example never finishes: 9.37.0 fails P2 within the bound; "
            "(4) on the pages 9.83.0 of chapters 5 and 6, 9.37.0 gives for every feature the same result as 9.36.0; on the page 9.85.0 of chapter 8 the P2 result of 9.37.0 is reported as printed; "
            "(5) no committed file is edited (the executor's logs are written once), no gate, test or threshold other than the new file is changed, and 9.37.0 is NOT used in any other criterion; results are reported as printed; if any element fails the file is named failing. " + F_P2)


def txt_links():
    return ("Carried from the story ex:ST_Section_Links by " + CR + " (" + WHEN + "; its criterion ex:AC3L2_Ch11 names the page 9.79.0 on template 9.51.1, which no longer exists as the target; the elements are restated on the page that is built now). Given the research of chapter 11 (16 sections, section links Done) and the page of chapter 11 rebuilt by TK_Ch11_Page_Build on template 9.52.2 (Iteration 21), when the checks are run, then ALL of: "
            "(1) links: every one of the 16 sections is related to at least one other section by a stated link, and no relationship is stated as text only; (2) ERD: the page tests 9.34.1 and 9.35.1 run their ERD label features (the filled ERD overlap and labels-over-entity reading, and the on-choice labels mode) with no skip and pass them, labels shown after Untangle at least 95 percent of the grid's, and the run ends without a crash; "
            "(3) gates: the Stage 4 gate runner v1_1_0 for 11 (current validator v1.13.0) exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks v1_3_0 (pinned validator v1.6.0) pass; "
            "(4) the template markers, the deck match check with 0 not carried, the Stage 4 page ABox and the stored page-test result as new files; (5) no committed file is edited and no gate, test, threshold or criterion is changed; results as printed; if any element fails the chapter is named failing. " + F_L4)


CRITS = {"AC7R_Deck_Ch07": ("The deck of chapter 7 is re-issued as v2_1_0 in new files and meets the deck standard with no committed file edited", txt_deck, ["TS_DeckStdCheck", "TS_ChapterCheck", "TS_DeckMatch", "TS_RdodiValidatorPinned"], R.VER_D, "TC3R_D"),
         "AC7R_PageTest937": ("The page test 9.37.0 waits for the end of a chapter-code example, fails a text-only result and leaves 9.36.0 unchanged", txt_test, ["TS_PageTest36", "TS_PageTest37"], "page test 9.36.0 (unchanged) and 9.37.0 (new file), Playwright 1.56.0; page tests 9.34.1 and 9.35.1; page check wrapper v1_5_0", "TC3R_T"),
         "AC7R_SecLinks_Ch11": ("The section links of chapter 11 show on its rebuilt page with the ERD labels measured, as in the carried criterion", txt_links, ["TS_PageTemplateE", "TS_PageBuilder415", "TS_PageData224"] + R.RV.BASE, R.VER_P, "TC3R_L")}
STORIES = [("ST_Ch07_Deck_Reissue", "The deck of chapter 7 is re-issued as v2_1_0 in new files and meets the deck standard", "Del3_Repair20", "Obj3_Repair20", ["AC7R_Deck_Ch07"], ["TK_Ch07_Deck_Reissue", "TK_Ch07_Deck_Reissue_Verify"], IT3, "Ready"),
           ("ST_PageTest_937", "The page test 9.37.0 waits for the end of a chapter-code example, as a new file", "Del3_Repair20", "Obj3_Repair20", ["AC7R_PageTest937"], ["TK_PageTest937_Build", "TK_PageTest937_Verify"], IT3, "Ready"),
           ("ST_Section_Links_Ch11", "The section links of chapter 11 show on its rebuilt page (the remainder of the story of Iteration 14)", "Del3_Repair20", "Obj3_Repair20", ["AC7R_SecLinks_Ch11"], ["TK_SecLinks_Ch11_Verify_R"], IT2, "Proposed")]
TASKS = [("TK_Ch07_Deck_Reissue", "Re-issue the deck of chapter 7 as v2_1_0 in new files", "Build", [], "SEN0401-I20-deck-ch07-r2", "T0", 1.0, IT3, "Ready",
          "RE-ISSUE the deck of chapter 7 as v2_1_0: write the NEW files 03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx, 08-tooling/ch07-deck/deck_build_v2_1_0.py, deck_plan_v2_1_0.json and the shipped copy sen0401_ch07_deck_v2_1_0.pptx, with the content of v2_0_0 (the control viewed all 61 slides and found no overflow; the deck standard check, overlap, Deck chapter check, manifest and deck match check all passed on v2_0_0, so the content stays). "
          "THE DEFECT: your commit 27d36a5 edited in place four files that your commit ed03d15 had added (the v2_0_0 deck, its build script, its plan and its shipped copy); the criterion's element (4) allows no edit of a committed file, your own earlier commit included. "
          "Do it so that every commit of this task adds files only: build in a scratch folder, check there, then copy the finished files in ONE commit; write each log once, after its run is complete, and commit it once; never touch any v2_0_0 file, any file of ed03d15 or 27d36a5, or the manifest (a changed manifest is a new version v1_1_0, only if the order or names of the code slides change). "
          "Run the deck standard check, the deck overlap check, the Deck chapter check v1_3_0 and the manifest check on the new deck and report each as printed. " + F_DECK + " " + R.NOEDIT + " " + R.COMMON),
         ("TK_Ch07_Deck_Reissue_Verify", "Verify the re-issued deck of chapter 7 on the evidence bridge", "Verify", ["TK_Ch07_Deck_Reissue"], "builder", "T0+1.0h", 0.5, IT3, "Proposed",
          "Run on the bridge the deck standard check, the deck overlap check, the Deck chapter check, the deck match check, the manifest equality and the nochange check over the executor's commits (status A only); view every slide of the new deck zoomed; record every result as printed."),
         ("TK_PageTest937_Build", "Make the page test 9.37.0 as a new file, with fixtures", "Build", [], "SEN0401-I22-pagetest", "T0", 1.0, IT3, "Ready",
          "Write the NEW file 08-tooling/sen0401_page_test_v9_37_0.py from sen0401_page_test_v9_36_0.py (which stays byte-identical): the only change is the wait in the P2 step (about lines 1515 to 1534 of 9.36.0): after the click on the run button, wait until the element [data-cc-result] no longer shows the placeholder 'Running...' (the template 9.52.2 writes it as a p.note) and holds text or a visual, within the same 90 s bound, then read; everything else is unchanged. "
          "Build the three fixtures of the criterion as new files in 08-tooling/page-test-937-fixtures/ (a slow example with a visual, a text-only example, an example that never ends) and run 9.36.0 and 9.37.0 on them; run 9.37.0 and 9.36.0 on the pages 9.83.0 of chapters 5 and 6 and the page 9.85.0 of chapter 8 under `flock /tmp/page_test.lock`, serially. Keep the logs, the unified diff and the SHA-256 of 9.36.0 before and after. "
          "A failing result is not worked around; the file does not enter any other criterion. " + F_P2 + " " + R.NOEDIT + " " + R.COMMON),
         ("TK_PageTest937_Verify", "Verify the page test 9.37.0 and its fixtures on the evidence bridge", "Verify", ["TK_PageTest937_Build"], "builder", "T0+1.0h", 1.0, IT3, "Proposed",
          "Re-run on the bridge: 9.36.0 byte-identical, the diff limited to the P2 wait, the three fixtures under both tests (slow visual: 9.36.0 fails and 9.37.0 passes; text-only: 9.37.0 fails; never ends: 9.37.0 fails within the bound), and 9.37.0 against 9.36.0 on the pages of chapters 5, 6 and 8 under the lock; record every result as printed."),
         ("TK_SecLinks_Ch11_Verify_R", "Verify the section links and the ERD labels on the rebuilt page of chapter 11", "Verify", ["TK_Ch11_Page_Verify"], "builder", "after TK_Ch11_Page_Verify", 0.5, IT2, "Proposed",
          "Run, one after the other and as printed: the research link count (every one of 16 sections related to another); the page tests 9.34.1 and 9.35.1 on the page that TK_Ch11_Page_Build produced (the ERD label features run without a skip); the Stage 4 gate runner v1_1_0 for 11; the chapter checks v1_3_0; the template markers; the deck match check; the criterion ex:AC7R_SecLinks_Ch11. This task replaces TK_SecLinks_Ch11_Page and TK_SecLinks_Ch11_Verify of the story ex:ST_Section_Links (withdrawn by the same route): the page work is carried by TK_Ch11_Page_Build of Iteration 21. " + F_L4)]


def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "Three repairs found by the controls of 2026-10-24: the deck of chapter 7 re-issued, the page test 9.37.0, and the remainder of the section-links story split off"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ;\n    rdfs:seeAlso ex:CR3_Ch78 ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (
        CR, lit("Ordered " + WHEN + ". " + F_DECK + " " + F_P2 + " " + F_L4 + " The change grows the scope by one deliverable: three repairs, all new files; nothing existing is edited. Pending until the ScopeChange that admits the stories is recorded in the Backlog version."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the three repairs cost and what they unblock, measured before they are started"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Ch78 ;\n    backlog:hasImpactStatement %s .\n') % (
        IA, CR, lit(F_DECK + " " + F_P2 + " " + F_L4 + " AFFECTED: ST_Ch07_Deck (its Build task is Suspended, its Verify task withdrawn; its criterion stays unmet and unchanged; the story stays open for the owner's answer on superseded stories), TK_Ch07_Page_Build (now depends on the re-issued deck's Verify task), ST_Ch08_Page (its criterion measures with 9.36.0, which fails; unchanged until the owner answers whether 9.37.0 may be used), ST_Section_Links (closed by a review after its remainder is split). NOT AFFECTED: the template, the builders, tests 9.34.1, 9.35.1, 9.36.0 (new file only), every other deck and page, the Mission outcome and the Achieved status. "
                    "PLAN (route as ex:CR3_Ch78, G127): a StageRevision from the Scope stage, seven versions; then one version for the withdrawals, one for the ranking (repairs first, BP-D10), one for work begun. New iteration Iter_22 (start at planning, proposed end Sunday 2026-10-25 09:00 UTC, the owner's to decide) with two stories and four tasks (the deck re-issue about 1.0 h executor and 0.5 h verification, the test 9.37.0 about 1.0 h executor and 1.0 h verification with serial browser runs); one story and one Verify task in Iter_21. "
                    "COST: new files only; a failing criterion is named failing; nothing is waived. ORDER: repairs rank ahead of the page of chapter 7 (repair 9.37.0 first for the pages; the criterion of the pages uses 9.36.0 until the owner answers)."))
    return t + cr + ia, "ChangeRequest %s (Pending) with its ImpactAssessment for the three repairs ordered on 2026-10-24: the deck of chapter 7 re-issued, the page test 9.37.0, the split of the section-links remainder." % CR


def ev_retract(t):
    t = X.set_status(t, "LS_Opened")
    reason = ("The change request " + CR + " (" + WHEN + ") adds a deliverable (three repairs as new files); the lineage is in its closed Backlog stage, and a deliverable added to a closed scope statement is a revision from the Scope stage (ruling G127). The request and its impact assessment " + IA + " were recorded first. "
              "This version retracts the Scope, Goal, Objective and Backlog outputs and rebuilds nothing; the next four versions rebuild them one stage each, a sixth fills the last commit; the items already in the register, Done ones included, re-enter by admission and are not re-dated. The retracted outputs and their digests stay as history (L-112). The interim versions are the declared transition (G129). Recorded as decided by the builder role.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Scope stage: the three repairs of 2026-10-24"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Scope ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n') % (REV, CR, IA, lit(reason), ", ".join(ACTIVE))
    b += "".join("%s backlog:outputRetracted true .\n" % o for o in ACTIVE)
    return t + b, "StageRevision of the third lineage from the Scope stage (ruling G127) for the three repairs of 2026-10-24: the Scope, Goal, Objective and Backlog outputs are retracted; nothing is rebuilt in this version."


def ev_scope(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S); t = X.set_status(t, "LS_Scoped")
    lab = "The repairs found by the controls of Iteration 20 as new files: the deck of chapter 7 re-issued as v2_1_0, the page test 9.37.0, and the remainder of the section-links story carried to Iteration 21"
    tx = ("The deck of chapter 7 as v2_1_0 in new files meeting the deck standard with no committed file edited; the page test 9.37.0 as a new file that waits for the end of a chapter-code example (9.36.0 stays), proven by fixtures; the section links of chapter 11 verified on the page that Iteration 21 rebuilds. " + F_DECK + " " + F_P2 + " " + F_L4)
    L = ('\nex:Del3_Repair20 a backlog:ScopeDeliverable ;\n    rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:derivesFromMissionClause "%s"^^xsd:string ;\n    backlog:hasDeliverableText %s ;\n'
         '    backlog:deliverableForArea ex:Area3_Remedy56 ; backlog:hasScopeLayer backlog:Layer_Work ; backlog:hasProductScopeKind backlog:Kind_Functional .\n') % (lit(lab), T.CLAUSE, lit(tx))
    L += "ex:Scope3 backlog:requiresDeliverable ex:Del3_Repair20 ; rdfs:seeAlso %s, %s .\n" % (CR, IA)
    L += "ex:Scope3 rdfs:comment %s@en .\n" % lit("Revised 2026-10-24 by the stage revision %s on the change request %s (%s). The statement above is unchanged (L-112). It now also requires one deliverable in the area ex:Area3_Remedy56 (three repairs as new files). No exclusion changes: new files only; the exclusion of changes to gates, tests and thresholds still holds (9.37.0 is a new test file and enters no criterion until the owner answers)." % (REV, CR, WHEN))
    t += L; return t + SL.out_new(t, "Scope", "Out3_ScopeR10", "Out3_Mission"), "third lineage, Scope stage rebuilt by the stage revision for the three repairs of 2026-10-24: one deliverable in the existing area."


def ev_goal(t, prev):
    t = G.fill_re(t, "ex:Out3_ScopeR10", prev); t = X.set_status(t, "LS_Goaled")
    g = '''
ex:G3_Repair20 a backlog:Goal ;
    rdfs:label "The findings of the controls of Iteration 20 are repaired without editing a committed file or weakening a gate"@en ;
    backlog:belongsToLineage ex:Lineage3 ; backlog:derivesFromScope ex:Scope3 ; backlog:goalCoversArea ex:Area3_Remedy56 ;
    backlog:contributesToMission ex:Mission ; backlog:hasGoalFacing backlog:Facing_Mission ; backlog:hasGoalPriority backlog:Priority_Must ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ;
    backlog:hasGoalRationale %s ;
    backlog:producedByStage ex:Out3_GoalR10 .
ex:G3_Repair20 rdfs:comment "Drafted by the builder session on 2026-10-24 from the change request %s; the intent origin is therefore Derived."@en .
ex:Spec3I_Repair20 a backlog:Specification ;
    rdfs:label "What it is for a repair to be done"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:specifiesGoal ex:G3_Repair20 ;
    backlog:hasSpecificationText %s ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_GoalR10 .
ex:Spec3I_Repair20_Pass a backlog:TestScenario ; rdfs:label "A repair delivered as new files passes its criterion"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Nominal ; backlog:scenarioOf ex:Spec3I_Repair20 ; backlog:hasScenarioText %s .
ex:Spec3I_Repair20_Fail a backlog:TestScenario ; rdfs:label "A repair that edits a committed file or lets a text-only result pass is not claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:scenarioKind backlog:Scen_Rejection ; backlog:scenarioOf ex:Spec3I_Repair20 ; backlog:hasScenarioText %s .
''' % (lit("Derived from the revised scope and the change request " + CR + ": the controls of 2026-10-24 found a deck whose files were edited in place, a page test that reads a placeholder as a result, and a story whose iteration ended. " + F_DECK + " " + F_P2),
       CR, lit("A repair is done when every element of its criterion is measured on the evidence bridge as met, the files are new, the fixtures show the gate still rejects what it must reject, and no committed file is edited."),
       lit("Given the re-issued deck v2_1_0 and the page test 9.37.0, when the checks and the fixtures are run on the bridge, then every element passes and the nochange check prints status A only."),
       lit("Given the deck v2_0_0 (27d36a5 modified four files) or a fixture whose example ends with text only, when the nochange check or the page test 9.37.0 is run, then the first prints status M and the second fails P2, and nothing is claimed."))
    t += g; return t + SL.out_new(t, "Goal", "Out3_GoalR10", "Out3_ScopeR10"), "third lineage, Goal stage rebuilt for the three repairs of 2026-10-24: one goal with a specification and two scenarios."


def ev_objective(t, prev):
    t = G.fill_re(t, "ex:Out3_GoalR10", prev); t = X.set_status(t, "LS_Objectived"); now = M.now()
    o = '''
ex:Obj3_Repair20 a backlog:Objective ; rdfs:label "Findings of the controls of Iteration 20 repaired: from 0 to 3"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:contributesToGoal ex:G3_Repair20 ; backlog:fillsScope ex:Scope3 ; backlog:hasSuccessMetric ex:Met3_Repair20 ;
    backlog:hasMeasurementKind backlog:Meas_Counted ;
    backlog:hasMeasurementQuery %s ;
    backlog:hasBaselineValue "0"^^xsd:decimal ; backlog:hasTargetValue "3"^^xsd:decimal ; backlog:hasTargetDirection backlog:Dir_Increase ;
    backlog:hasCheckpoint ex:CP3I_Repair20 ;
    backlog:hasIntentOrigin backlog:IOrigin_Derived ; backlog:decidedBy backlog:Owner ; backlog:producedByStage ex:Out3_ObjectiveR10 .
ex:Met3_Repair20 a backlog:Metric ; rdfs:label "findings of the controls of Iteration 20 whose repair story is Done on verified evidence"@en ; backlog:belongsToLineage ex:Lineage3 .
ex:CP3I_Repair20 a backlog:ObjectiveCheckpoint ; rdfs:label "Reading after the repair stories are controlled"@en ;
    backlog:checkpointCondition "Taken after the evidence bridge has run the checks of the three repair criteria, so the count is read from verified runs." ; backlog:expectedValue "3"^^xsd:decimal .
ex:Obs45_Repair20 a backlog:MetricObservation ; rdfs:label "Baseline, before the work"@en ;
    backlog:observesMetric ex:Met3_Repair20 ; backlog:observationFor ex:Obj3_Repair20 ; backlog:hasObservedValue "0"^^xsd:decimal ;
    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony true ;
    backlog:hasObservationMethod %s .
ex:Obj3_Repair20 rdfs:comment "Drafted by the builder session on 2026-10-24 from the change request %s; the intent origin is therefore Derived."@en .
''' % (lit("Count of the three repair stories (deck of chapter 7 re-issued, page test 9.37.0, section links of chapter 11) whose criterion is measured met on the evidence bridge."), now,
       lit("Baseline from the controls of 2026-10-24 (v0.244.0 and the root-cause analysis of the page 9.85.0): none of the three findings is repaired, so 0 of 3."), CR)
    t += o; return t + SL.out_new(t, "Objective", "Out3_ObjectiveR10", "Out3_GoalR10"), "third lineage, Objective stage rebuilt for the three repairs: one objective (0 to 3) with metric, checkpoint and baseline reading."


def ev_backlog(t, prev):
    t = G.fill_re(t, "ex:Out3_ObjectiveR10", prev); t = X.set_status(t, "LS_Backlogged"); now = M.now()
    old = "ex:Out3_BacklogR11"; n = t.count("backlog:admittedByOutput %s ;" % old); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % old, "backlog:admittedByOutput %s ;" % NEWB)
    L = ['ex:TS_PageTest37 a backlog:ToolScript ; rdfs:label "page test 9.37.0 (new file over 9.36.0: the P2 step waits until the result no longer shows the placeholder Running...; every other feature unchanged)"@en ; backlog:scriptFileName "sen0401_page_test_v9_37_0.py" ; backlog:acceptsGraphPath false .\n']
    for c, (lab, fn, tools, ver, k) in CRITS.items():
        L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool %s ;\n    backlog:measuredWithVersion %s ;\n    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs, the diffs and the fixtures, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:%s_Passes, ex:%s_NotClaimed .\n' % (
            c, lit(lab), lit(fn()), ", ".join("ex:" + x for x in tools), lit(ver), k, k))
        L.append('''ex:%(k)s_Passes a backlog:TestCase ; rdfs:label "Run the checks of the criterion on the new files"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(c)s ; backlog:coversScenario ex:Spec3I_Repair20_Pass ; backlog:runsOnData ex:Data3R_%(k)s_Passing ;
    backlog:hasCaseText "Run the checks of the criterion over the new files; they report no failure and exit 0." .
ex:%(k)s_NotClaimed a backlog:TestCase ; rdfs:label "Run the checks on the file or fixture that fails and require that no pass is claimed"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:exercisesCriterion ex:%(c)s ; backlog:coversScenario ex:Spec3I_Repair20_Fail ; backlog:runsOnData ex:Data3R_%(k)s_Failing ;
    backlog:hasCaseText "Run the checks on the file or fixture that the control found failing (deck v2_0_0 with status M, a text-only fixture, the open story) and require that nothing is claimed for it." .
ex:Data3R_%(k)s_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .
ex:Data3R_%(k)s_Failing a backlog:TestData ; rdfs:label "The file or fixture that fails the checks"@en ; backlog:belongsToLineage ex:Lineage3 ;
    backlog:hasFixtureState "The finding as measured on 2026-10-24 (ex:IA3_Repair20)." .
''' % dict(k=k, c=c))
    for sid, title, deliv, obj, crits, tks, it, state in STORIES:
        L.append(R.story_block(sid, title, deliv, obj, crits, tks, "Requested " + WHEN + " (" + CR + "). One criterion per unit (G133). Done stories and tasks stay Done and are not edited (G125). MEASURED FACTS: see the impact assessment " + IA + ".", it, "Ready" if state == "Ready" else "Proposed"))
    for tid, title, ttype, deps, sess, est, hrs, it, state, note in TASKS:
        L.append(R.task_block(tid, title, ttype, deps, sess, est, hrs, note, it, state, True))
    for sid, *_ in STORIES: L.append("ex:%s backlog:standsAlone true .\n" % sid)
    for x in [s[0] for s in STORIES[:2]] + [x[0] for x in TASKS if x[7] == IT3]:
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, IT3, lit("Refined by the builder session from the change request %s and the measured facts of %s: acceptance criterion with tool and version, dependencies, estimated start, and a brief to be generated; startable when its dependencies are Done." % (CR, IA))))
    for sid, title, deliv, obj, crits, tks, it, state in STORIES:
        L.append('ex:Plan3R_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into %s"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Repair20, ex:Spec3I_Repair20_Pass, ex:Spec3I_Repair20_Fail .\n' % (sid, sid, "iteration 22" if it == IT3 else "iteration 21 (planned, not started)", now, it, sid, ", ".join("ex:" + x for x in tks)))
    L.append("ex:Obj3_Repair20 backlog:metricMovableBy %s .\n" % ", ".join("ex:" + s[0] for s in STORIES))
    m3 = [s[0] for s in STORIES if s[6] == IT3] + [x[0] for x in TASKS if x[7] == IT3]
    L.append('%s a backlog:Iteration ; rdfs:label "Iteration 22: the repairs found by the controls of Iteration 20"@en ; backlog:hasIdentifier "Iter_22" ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "%s"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember %s .\n' % (
        IT3, now, END3, lit("Proposed by the builder session on 2026-10-24: the start is the instant of the planning ceremony ex:PC3_Iter_22; the proposed end is Sunday 2026-10-25 09:00 UTC, about a day; the owner decides the end. Justification (estimates, not measurements): the deck re-issue about 1.0 h and its verification 0.5 h; the page test 9.37.0 about 1.0 h with serial browser runs and its verification about 1.0 h; the two executors work in parallel."),
        lit("The deck of chapter 7 is re-issued as v2_1_0 in new files and the page test 9.37.0 exists as a new file proven by fixtures, both verified by the evidence bridge; nothing existing is edited. Frozen at the planning ceremony."), ", ".join("ex:" + x for x in m3)))
    L.append('ex:PB3R_Iter_22 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 22 when it was planned"@en ; backlog:baselineFor %s ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "%s"^^xsd:dateTime .\n' % (IT3, now, now, END3))
    L.append('ex:PC3_Iter_22 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 22: the repairs of 2026-10-24"@en ; backlog:ceremonyFor %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3R_ST_Ch07_Deck_Reissue, ex:Plan3R_ST_PageTest_937 ;\n    rdfs:comment %s@en .\n' % (IT3, now, lit("Held %s by the builder session after the change request %s: two stories and four tasks are committed to this iteration, whose goal is frozen at its start. No executor has started in it; work begun is recorded at the real start of each executor session, with its brief." % (now, CR))))
    # the Verify task of the carried story joins Iteration 21 (planned, not started)
    t, k = re.subn(r"(ex:Iter_21 a backlog:Iteration .*?backlog:hasMember [^\n]*?) \.\n", lambda m: m.group(1) + ", ex:ST_Section_Links_Ch11, ex:TK_SecLinks_Ch11_Verify_R .\n", t, count=1, flags=re.S); assert k == 1
    # the page task of chapter 7 depends on the Verify task of the re-issued deck
    i, j = T.blk(t, "TK_Ch07_Page_Build"); b = t[i:j]; assert "ex:TK_Ch07_Deck_Verify" in b
    t = t[:i] + b.replace("ex:TK_Ch07_Deck_Verify", "ex:TK_Ch07_Deck_Reissue_Verify", 1) + t[j:]
    L.append('ex:Refine_TK_Ch07_Page_Build_R20 a backlog:RefinementEvent ; rdfs:label "Refinement of the page task of chapter 7: it waits for the re-issued deck"@en ;\n    backlog:refines ex:TK_Ch07_Page_Build ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_20 ;\n    backlog:hasRefinementOutcome %s .\n' % (now, lit("The dependency on TK_Ch07_Deck_Verify (its Build task Suspended after the control of 2026-10-24, to be withdrawn) is replaced by the dependency on TK_Ch07_Deck_Reissue_Verify of the repair story; no criterion, tool or threshold changes, the task is Ready and not Done (G125 does not apply). The page also waits for the owner's answer on the page test (9.36.0 or 9.37.0).")))
    L.append('ex:SC3_Repair20 a backlog:ScopeChange ;\n    rdfs:label "Scope grown: the three repairs of 2026-10-24"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem %s ;\n    backlog:hasScopeChangeRationale %s .\n' % (CR, ", ".join("ex:" + s[0] for s in STORIES), lit("Ordered " + WHEN + ". The boundary moved outward by three stories; new files only; nothing existing is edited or weakened.")))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange ex:SC3_Repair20 and the stories it admits; it was Pending before. The order is the course coordinator\'s; the end of Iteration 22 is still the owner\'s."@en .\n' % (CR, now[:10]))
    t += "\n" + "".join(L)
    return t + SL.out_new(t, "Backlog", "Out3_BacklogR12", "Out3_ObjectiveR10"), "third lineage, Backlog stage rebuilt for the three repairs: Iteration 22 (two stories, four tasks, planned), one story and one Verify task in Iteration 21, criteria with tools and versions, the ScopeChange; the change request Accepted; the %d carried items are re-admitted, not re-dated." % n


def ev_fill(t, prev): return G.fill_re(t, NEWB, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the revision is complete and no work is begun." % (NEWB, prev)


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "scope": lambda: ev_scope(t, sys.argv[2]), "goal": lambda: ev_goal(t, sys.argv[2]), "objective": lambda: ev_objective(t, sys.argv[2]), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__": main()
