#!/usr/bin/env python3
"""sen0401_lineage_res21 v1_0_0 - change route (G113, G125 route 2, G133, G134, G147) for the owner's ruling of 2026-10-30 00:51 Istanbul: the interactive page questions are SEEDS, not exam items.
A new story (engine v1.1.0 with a rule that refuses an item matching a page-visible item, authored items only), the Items story revised (not started: its text and criterion are rewritten for seed-based enhancement iterations), the dependency of Items on the new engine, planned into the new Iteration 51.
The measured facts are those of 08-tooling/exam/sen0401_exam_seedreport_v1_0_0.json. A StageRevision from the Backlog stage (a criterion is counted by the Backlog digest). Events, one new file each: change | retract | backlog PREV | fill PREV"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_gap_revision_v1_0_0 as G
import sen0401_lineage_template_revision_v1_0_0 as T
lit = G.lit
import glob, importlib.util
def _pv_newest():
    fw = X.FW; vk = lambda q: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.", q)[0]]
    spec = importlib.util.spec_from_file_location("pv", sorted(glob.glob(fw + "/03-tooling/backlog_pipeline_verify_v*.py"), key=vk)[-1])
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    m.STAGE_TYPES = m._load_stage_types(sorted(glob.glob(fw + "/01-ontologies/backlog_tbox_v*.ttl"), key=vk)[-1], table="v4")
    return m
X._pv = _pv_newest
REV = "ex:Revision_Lineage3_Backlog8"; OLD = "ex:Out3_BacklogR33"; NEW = "ex:Out3_BacklogR34"; ITER = "ex:Iter_51"
CR = "ex:CR3_PageSeeds"; IA = "ex:IA3_PageSeeds"; SC = "ex:SC3_PageSeeds"
SID = "ST_Exam_NoCopy"; BT = "TK_Exam_NoCopy_Build"; VT = "TK_Exam_NoCopy_Verify"; CRIT = "AC3E_Exam_NoCopy"; SESS = "SEN0401-I51-nocopy"
WHEN = "Friday 2026-10-30, after the owner's ruling of 00:51 Istanbul, as relayed by the course coordinator"
RULING = ("Interactive page questions are accessible by the students before the exam. They are chapter subject specific questions, rarely cross-section. It is not wise to use them directly, but they can be a seed for better questions and enhancement iterations.")
import json as _json
_R = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exam/sen0401_exam_seedreport_v1_0_0.json")))
_C = _R["chapters"]
FOUND = ("MEASURED by the seed report (08-tooling/exam/sen0401_exam_seedreport_v1_0_0.py, with a fixture of known answer; commit 0ebc134): the page-visible questions of chapters 1 to 6 are %d bank items (all four-option single-answer choice, %d with a code listing; embedded in the pages as JSON; generators: %s) and %d page quiz items; "
         "the pages also build their own exam desk (xExamBuild) from the concept tree, with kinds that are not enumerable as a list. The bank files were first committed on 2026-10-04 (chapters 1 to 5, commit 42764b2) and 2026-10-08 (chapter 6, 02da678); the generators write each item from a concept of the chapter ontology or a worked example whose program is run; no file of an earlier exam exists in the repository (the only files named exam, midterm or quiz outside the exam work are the page quiz files). "
         "Coverage of the 101 critical points of list A (chapters 1 to 6) by seed items, by a stated lexical method (two thresholds): %d points with at least one seed at the strict threshold and %d at the lenient one; per chapter strict %s of %s points. "
         "What the seeds are not: single-form (choice only; the banks hold no matching, ordering, fill-in, number or trace item), one concept each (every item comes from one concept of one chapter), and no item states a second chapter on purpose. The paper types of the page exam desk that suit paper: choice, matching, ordering, fill-in, trace; the desk's multi-select, true-or-false and run-code kinds do not. "
         "THE ENGINE OF COMMIT e662771 COMPOSES PAPERS FROM THE BANK ITEMS: under the owner's ruling that is what must not happen.") % (
    sum(c["items"] for c in _C.values()), sum(c["with_code"] for c in _C.values()), "chapters 1, 2, 4, 5, 6 one script each, chapter 3 none in 08-tooling", sum(c["quiz_items_in_the_page"] for c in _C.values()),
    sum(c["points_with_seed_strict"] for c in _C.values()), sum(c["points_with_seed_lenient"] for c in _C.values()), [c["points_with_seed_strict"] for c in _C.values()], [c["critical_points"] for c in _C.values()])
RULE = "the owner's ruling and the standing rules: gaps and changes go through change management in the active lineage; rulings are recorded in SHACL; nothing is waived"

def ev_change(t):
    cr = ('\n%s a backlog:ChangeRequest ;\n    rdfs:label "The page questions are seeds, not exam items: a rule that refuses a copy, and items built from seeds by enhancement iterations"@en ;\n'
          '    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_ExamMission, ex:IA3_ExamMission ;\n'
          '    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n') % (CR, lit(
        "Raised " + WHEN + ". THE OWNER'S WORDS: '" + RULING + "' " + FOUND + " WHAT CHANGES: (1) a NEW story ex:" + SID + " builds a new engine version (engine v1.1.0 as new files, v1.0.0 kept) with a new rule EN11 in SHACL that REFUSES any item whose stem or option set matches a page-visible item (the bank items and the page quiz items of the chapter list), with the similarity method and its thresholds stated before the run and a fixture of known answer; "
        "the engine builds papers from AUTHORED items only (no bank item is composed into a paper); all item types of the paper rules (choice, matching, ordering, fill-in bank, number, trace) are authored items; (2) the Items story is REVISED: it has not started, so its text and criterion are rewritten (G133 forbids that only while the work under a criterion runs): items are built from seeds by enhancement iterations (change the situation, combine chapters, reverse the question, add a reasoning step, change the numbers), and every item carries a link to its seed item(s) and to the critical point(s) it tests; "
        "(3) the seed report stays as the gap analysis the rules require before new work; (4) the Items Build task now waits for the new engine version, so that every item can be checked against EN11. "
        "A new criterion and rewritten text are counted by the Backlog digest, so the route is a revision from the Backlog stage (G125 route 2). Pending until the ScopeChange that admits the new story is recorded. Rules applied: " + RULE + "."))
    ia = ('\n%s a backlog:ImpactAssessment ;\n    rdfs:label "What the seed ruling costs and touches, measured before it is started"@en ;\n'
          '    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_ExamMission ;\n    backlog:hasImpactStatement %s .\n') % (IA, CR, lit(
        FOUND + " WHAT MOVES: the Backlog digest of the third lineage once (one more story, two tasks, one criterion, one iteration; the Items story, tasks and criterion rewritten; one dependency added); Scope, Goal and Objective digests do not move. "
        "NOT AFFECTED: every Done item, the engine v1.0.0 and its check (it stays as a committed file), the paper rules (R01 to R22 stay), the answer sheet and its reader, the critical points, the owner's decisions of 2026-10-30 (24 questions per paper, the make-up never reuses an item, the bubble grid, chapters 1 to 6). "
        "COST OF THE ROUTE: one executor session of about three hours for the engine version (before the Items session), which delays the Items session by that time; the items session itself grows: items are authored, not chosen. COST OF NOT ACTING: papers built from questions the students have seen. "
        "THE ITEMS WORK IS LARGER THAN BEFORE: 48 authored items (24 per paper), each with seed and critical-point links, of types that the banks do not hold; the executor may need more than one session; that is estimated by the executor from the seed report and reported, not assumed."))
    return t + cr + ia, "ChangeRequest ex:CR3_PageSeeds (Pending) and ImpactAssessment ex:IA3_PageSeeds: the owner's ruling that the page questions are seeds; the measured facts of the seed report; no stage changed."

def ev_retract(t):
    reason = (FOUND + " The new acceptance criterion and the rewritten Items story are counted by the Backlog digest, so the Backlog stage is revised (G125 route 2): this version retracts the Backlog output " + OLD + " and rebuilds nothing; the next version rebuilds it and a third fills the last commit; the items already in the register, Done ones included, re-enter by admission, not re-dated.")
    b = ('\n%s a backlog:StageRevision ;\n    rdfs:label "Revision of the third lineage from the Backlog stage: the page questions are seeds, not exam items"@en ;\n    backlog:revisesLineage ex:Lineage3 ; backlog:revisesFromStage backlog:Stage_Backlog ;\n'
         '    rdfs:seeAlso %s, %s ;\n    backlog:revisionReason %s ;\n    backlog:retractsOutput %s ; backlog:decidedBy backlog:Builder ;\n    backlog:revisedAtCommit "PENDING" .\n%s backlog:outputRetracted true .\n') % (REV, CR, IA, lit(reason), OLD, OLD)
    t = X.set_status(t, "LS_Objectived")
    return t + b, "StageRevision of the third lineage from the Backlog stage (G125 route 2): the Backlog output %s is retracted for the seed ruling; nothing is rebuilt here." % OLD.replace("ex:", "")

SEEDS = "08-tooling/ch0N-page/question_bank_v*.json (newest per chapter) and 08-tooling/ch0N-page/quiz_v1_0_0.json, N = 1 to 6"
BUILD_TXT = ("BUILD THE ENGINE VERSION 1.1.0 as NEW files under 08-tooling/exam/ (sen0401_exam_engine_v1_1_0.py and what it needs: a new SHACL file with the rule EN11, a similarity module, fixtures of known answer, a check v1.1.0, their logs); engine v1.0.0, its shapes, fixtures and check, and every committed file are NOT edited; your own log files are never appended to. "
             "THE OWNER'S RULING (2026-10-30): the interactive page questions are accessible to students before the exam; they are chapter specific and rarely cross-section; they must not be used directly but can seed better questions. REQUIREMENTS, all together: "
             "(1) A new rule EN11 in SHACL: REFUSE (a violation, exit 2, nothing written) any paper item whose stem or whose set of four options matches a PAGE-VISIBLE item. The page-visible set is: " + SEEDS + " (the bank items embedded in the pages and the page quiz items). "
             "(2) State the similarity method and its thresholds BEFORE the run, in the module and in the check: normalise (lower case, punctuation and spacing removed), then an exact test and a near test (for example the share of shared word shingles of the stem, and the share of equal options after normalisation); say why each threshold is where it is and what it cannot see (a paraphrase of the idea). "
             "(3) A fixture of known answer: copies, near copies (a word changed, an option order changed), and genuinely different items on the same concept, with the expected answer of each written BEFORE the first run; the control will measure with a method of its own on its own pairs. "
             "(4) The engine builds papers from AUTHORED items only: the bank items are NOT composed into papers any more (a bank item in a paper is refused by EN11 by construction); all item types of the paper rules (choice, matching, ordering, fill-in bank, number, trace) are authored items from an items file in the authored-items format of v1.0.0 (extend it as new files if you need a field: seed links and critical-point links). "
             "(5) Keep every rule of v1.0.0 (EN01 to EN10, R01 to R22), the refusals, the key, the PDF, the chapter list default 1 to 6, the 24 questions per paper, the make-up never reusing a midterm item (a refusal), and the answer sheet page counted in the page count. Also create the output folder if it is missing (a defect the control found in v1.0.0). "
             "(6) Disclose: what you tested with fixture items only; what EN11 cannot see. Report as printed. Free disk is about 1.3 GB: tell the coordinator at once if it falls under 0.9 GB. One build at a time.")
VERIFY_TXT = ("Re-run the executor's check; measure EN11 with the control's own similarity method on pairs the control makes (copies, near copies, same-concept different items drawn from the real seeds) and require refusal exit 2 and nothing written for the copies and acceptance for the different ones; confirm that no bank item can enter a paper; confirm the v1.0.0 files and every committed file are byte-identical.")
ITEMS_BUILD = ("WRITE THE ITEMS OF THE TWO EXAMS (24 for the midterm, 24 for the make-up, the make-up sharing none with the midterm) as AUTHORED items in a new items file under 08-tooling/exam/ in the format of the engine v1.1.0, as new files; the chapter banks, the page quizzes and every committed file are never edited. "
               "THE OWNER'S RULING (2026-10-30): page questions are SEEDS, not exam items: every item is NEW, built from one or more seed items by an enhancement iteration: change the situation, combine chapters, reverse the question, add a reasoning step, change the numbers. No item may be a page item or a near copy of one (the rule EN11 of engine v1.1.0 refuses it: run it on your items). "
               "READ FIRST the seed report 08-tooling/exam/sen0401_exam_seedreport_v1_0_0.json (and its method in the .py): per chapter, how many seed items exist for each critical point, which points have no seed (write those items from the source named for the point in the critical points list, not from a seed), and what the seeds cannot give: cross-chapter and synthesis items, calculation, reasoning steps, and every type except four-option choice. "
               "EACH ITEM RECORDS: its seed item key(s) (or 'none: written from the source of the point'), the enhancement(s) applied, the critical point(s) it tests (id and label from list A of 08-tooling/exam/sen0401_exam_critical_points_v1_0_0.json), its chapter(s), Bloom level, kind (direct or synthesis; 'indirect' is not defined by the owner and is not used), its type from the paper registry (suited types: choice, choice with code, matching, ordering, fill-in bank, number, trace; the conditional types only if the owner enables them), its source (file and locator) and the terms it uses (every term must be found in the course corpus: EN08). "
               "CONVENTIONS: the working default is equal weight per chapter (4 items per chapter per paper, chapters 1 to 6; the owner has not decided the weights); a majority of items at the higher Bloom level; answer letters evenly distributed; code lines not wider than 45 characters; items need course knowledge, not general knowledge. Code and numbers in trace and number items must be COMPUTED by a program you run and keep (the printed output is the key). "
               "REPORT per paper: the chapters, the types, the Bloom levels, which critical points are tested and which are not (named by label), and the share of items with a seed. If you cannot write an item that meets a convention, say so by name and STOP; do not lower a convention. Several sessions may be needed: write what you can in verified steps and report what is left. Free disk is about 1.3 GB: tell the coordinator at once if it falls under 0.9 GB. One build at a time.")
ITEMS_VERIFY = ("Check every item against the seed report and the banks with the control's own similarity method (no copy, no near copy), that every seed link names an existing seed and every critical-point link an existing point, that the items tested by computation give the key when re-run, every term is in the corpus, the level, letter and weight conventions hold, the two papers share no item, and both pass the engine v1.1.0 (EN01 to EN11, R01 to R22).")

def ev_backlog(t, prev):
    t = re.sub(r'(%s a backlog:StageRevision.*?backlog:revisedAtCommit )"PENDING"' % re.escape(REV), lambda m: m.group(1) + '"%s"' % prev, t, count=1, flags=re.S)
    t = X.set_status(t, "LS_Backlogged")
    n = t.count("backlog:admittedByOutput %s ;" % OLD); assert n >= 40, n
    t = t.replace("backlog:admittedByOutput %s ;" % OLD, "backlog:admittedByOutput %s ;" % NEW)
    now = M.now(); L = []
    note = "Admitted by the change request " + CR[3:] + " (" + WHEN + "). One criterion per unit (G133). Done and Suspended items stay as they are. " + RULE + "."
    gh = ("Given the engine of commit e662771 (it composes papers from the bank items, which the students can see on the pages) and the owner's ruling that page questions are seeds, when an engine version 1.1.0 is made as new files and its check is run, then ALL of: "
          "(1) every file is new and no committed file is edited; (2) a rule EN11 in SHACL refuses (exit 2, nothing written) a paper item whose stem or option set matches a page-visible item (bank items and page quiz items of the chapter list), by a similarity method and thresholds stated before the run; "
          "(3) a fixture of known answer (copies, near copies, different items on the same concept) gives exactly the expected answer for every pair; (4) papers are built from authored items only, a bank item cannot enter a paper, and every item type of the paper rules is an authored item; "
          "(5) all rules of v1.0.0 (EN01 to EN10, R01 to R22) and the owner's decisions (chapters 1 to 6 by default, 24 questions per paper, the make-up never reusing a midterm item, the answer sheet page counted) still hold; (6) results as printed: if any element fails the work is named failing.")
    L.append('\nex:%s a backlog:AcceptanceCriterion ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasGherkinText %s ;\n    backlog:measuredWithTool ex:TS_ChapterCheck ;\n    backlog:measuredWithVersion "checks written by the executor as new files, run by the control on the evidence bridge with the control\'s own pairs" ;\n'
             '    backlog:satisfiedByArtifact "the new files cited by SHA-256, the logs of the runs, verified by the evidence bridge" ;\n    backlog:coveredByCase ex:TC3E_NoCopy_Passes, ex:TC3E_NoCopy_NotClaimed .\n'
             'ex:TC3E_NoCopy_Passes a backlog:TestCase ; rdfs:label "Run the engine check and the control\'s pairs"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:%s ; backlog:coversScenario ex:Spec3I_Exam_Pass ; backlog:runsOnData ex:Data3E_NoCopy_Passing ;\n    backlog:hasCaseText "Run the check v1.1.0; it reports no failure and exits 0." .\n'
             'ex:TC3E_NoCopy_NotClaimed a backlog:TestCase ; rdfs:label "Offer a copied item and require a refusal"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:exercisesCriterion ex:%s ; backlog:coversScenario ex:Spec3I_Exam_Fail ; backlog:runsOnData ex:Data3E_NoCopy_Failing ;\n    backlog:hasCaseText "Offer a paper with a page item or a near copy; the engine must refuse it with exit 2 and write nothing." .\n'
             'ex:Data3E_NoCopy_Passing a backlog:TestData ; rdfs:label "The new files whose checks pass when run"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState "The new files of the task, for which every check of the criterion exits zero when the bridge runs it, and whose cited files equal their recorded SHA-256." .\n'
             'ex:Data3E_NoCopy_Failing a backlog:TestData ; rdfs:label "A paper with a copied page item"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:hasFixtureState "A paper whose item is a bank item or a near copy of one, for which EN11 must refuse." .\n' % (
        CRIT, lit("Criterion of the engine version that refuses copied page items"), lit(gh), CRIT, CRIT))
    title = "The exam engine refuses an item that copies a page question and builds papers from authored items only"
    L.append('\nex:%s a backlog:Story ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ;\n    backlog:hasInvestmentCategory backlog:Cat_NewCapability ;\n'
             '    backlog:asRole "SEN0401 instructor" ; backlog:wantsCapability %s ; backlog:soThat %s ;\n    backlog:satisfiesDeliverable ex:Del3_ExamEngine ; backlog:pursuesObjective ex:Obj3_Exam ; backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:coversEntity ex:DE3_Exam, ex:DE3_ExamItem ; backlog:coversStage backlog:Stage_Creation ;\n'
             '    backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasApplicableConcern backlog:Concern_Data ; backlog:responsible %s ;\n    backlog:decomposesInto ex:%s, ex:%s ;\n    backlog:hasState backlog:Proposed ;\n'
             '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored by the ranking step of the same change route." ;\n    backlog:hasAuditNote %s .\n' % (
        SID, lit(title), SID, lit(title), ITER, NEW, lit(title[0].lower() + title[1:]), lit("no exam question is one the students have already seen on the pages"), CRIT, G.EXEC, BT, VT, lit(note)))
    for tid, tt, ttype, dp, txt in ((BT, "Build: " + title, "Build", ["TK_Exam_Engine_Build"], BUILD_TXT), (VT, "Verify: " + title, "Verify", [BT], VERIFY_TXT)):
        full = txt + " Planned session %s (an estimate, G120: the real start is recorded at work begun); about %.1f hours." % (SESS if ttype == "Build" else "builder", 3.0 if ttype == "Build" else 1.0)
        L.append('\nex:%s a backlog:ExecutionTask ; rdfs:label %s@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle %s ;\n    backlog:belongsToLineage ex:Lineage3 ; backlog:memberOfContainer %s ; backlog:admittedByOutput %s ; backlog:responsible %s ;\n'
                 '    backlog:hasInvestmentCategory backlog:Cat_%s ; backlog:hasTaskType backlog:TaskType_%s ; backlog:effectiveDefinitionOfDone ex:DoD ; backlog:hasState backlog:Proposed ;\n    backlog:dependsOn %s ;\n'
                 '    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s state; scoring both would double-count." ;\n    backlog:hasAuditNote %s .\n' % (
            tid, lit(tt), tid, lit(tt), ITER, NEW, G.EXEC, "NewCapability" if ttype == "Build" else "Compliance", ttype, ", ".join("ex:" + d for d in dp), lit(full)))
    L.append("ex:%s backlog:standsAlone true .\n" % SID)
    L.append('ex:Plan3E_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration 51"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto %s ;\n    backlog:plansItem ex:%s ; backlog:producesTask ex:%s, ex:%s ;\n    backlog:refinementProduces ex:Spec3I_Exam, ex:Spec3I_Exam_Pass, ex:Spec3I_Exam_Fail .\n' % (SID, SID, now, ITER, SID, BT, VT))
    for x in (SID, BT):
        L.append('ex:Refine_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration %s ;\n    backlog:hasRefinementOutcome "Refined by the builder session from the owner\'s ruling (ex:IA3_PageSeeds); the criterion and the task text name the rule, the method, the fixture and what a passing result is." .\n' % (x, x, x, now, ITER))
    # rewrite the Items story's tasks and criterion (not started)
    for tk, txt, hrs in (("TK_Exam_Items_Build", ITEMS_BUILD, 6.0), ("TK_Exam_Items_Verify", ITEMS_VERIFY, 1.5)):
        i, j = T.blk(t, tk); b = t[i:j]; assert "startedAt" not in b, tk
        m = re.search(r'backlog:hasAuditNote "(?:[^"\\]|\\.)*"', b); assert m
        full = txt + " Planned session %s (an estimate, G120: the real start is recorded at work begun); about %.1f hours (the executor reports its own estimate)." % ("SEN0401-I48-items" if tk.endswith("Build") else "builder", hrs)
        b = b.replace(m.group(0), "backlog:hasAuditNote " + lit(full), 1)
        if tk.endswith("Build"):
            md = re.search(r"backlog:dependsOn ([^;]*);", b); assert "TK_Exam_NoCopy_Build" not in md.group(1)
            b = b.replace(md.group(0), "backlog:dependsOn %s, ex:%s ;" % (md.group(1).strip(), BT), 1)
        t = t[:i] + b + t[j:]
    ig = ("Given the owner's ruling that page questions are seeds, when the items of the two exams are authored as new files from seeds by enhancement iterations and the checks of this criterion are run on the evidence bridge, then ALL of: (1) every file is new and no committed file is edited; "
          "(2) 24 items per paper, the make-up sharing none with the midterm, every item authored (none is a bank item or a page quiz item), none a near copy of one by the engine rule EN11 and by the control's own method; "
          "(3) every item names its seed item key(s) or says it has none, the enhancement applied, the critical point(s) it tests (list A), its chapter(s), level, type and source; every seed key and every point id exists; "
          "(4) items whose key is computed (trace, number) give that key when the control re-runs the program; (5) every term is found in the course corpus (EN08); the level, letter, weight and width conventions hold; both papers pass the engine v1.1.0 (EN01 to EN11, R01 to R22); "
          "(6) the report names, per paper, the critical points tested and not tested; results as printed: if any element fails the work is named failing.")
    t, kk = re.subn(r'(ex:AC3E_Exam_Items a backlog:AcceptanceCriterion.*?backlog:hasGherkinText )"(?:[^"\\]|\\.)*"', lambda m: m.group(1) + lit(ig), t, count=1, flags=re.S); assert kk == 1
    L.append('ex:AC3E_Exam_Items backlog:hasAuditNote %s .\nex:ST_Exam_Items backlog:hasAuditNote %s .\n' % (lit("Rewritten %s before any work began (the story and its Build task are Ready and not started; G133 forbids a rewrite only while the work under a criterion runs), on the owner's ruling that page questions are seeds: see ex:CR3_PageSeeds." % now[:10]), lit("Text and criterion rewritten %s for authored, seed-based items (ex:CR3_PageSeeds); the Build task now also waits for ex:%s." % (now[:10], BT))))
    L.append('ex:Iter_51 a backlog:Iteration ; rdfs:label "Iteration 51: the exam engine refuses copied page items"@en ; backlog:hasIdentifier "Iter_51" ; backlog:belongsToLineage ex:Lineage3 ;\n'
             '    backlog:iterationStart "%s"^^xsd:dateTime ; backlog:iterationEnd "2026-11-01T12:00:00"^^xsd:dateTime ;\n    backlog:hasDurationSource %s ;\n    backlog:hasSprintGoal %s ;\n    backlog:hasMember ex:%s, ex:%s, ex:%s .\n' % (
        now, lit("Proposed by the lineage agent on %s: the start is the instant of the planning ceremony ex:PC3_Iter_51; the end is the end of ex:Iter_48 (2026-11-01T12:00:00 UTC, when chapter work restarts); one executor task of about three hours and one verification of about one hour, one executor at a time (disk). Why a new iteration: the goals of ex:Iter_48 and ex:Iter_50 are frozen at their start. The end is the owner's to decide. Estimates, not measurements (G120)." % now[:10]),
        lit("The exam engine version 1.1.0 refuses any item that matches a page-visible item and builds papers from authored items only, with a stated method and a fixture of known answer. Frozen at the iteration's start."), SID, BT, VT))
    L.append('ex:PB3_Iter_51 a backlog:PlanBaseline ; rdfs:label "Plan baseline of iteration 51 when it was planned"@en ; backlog:baselineFor ex:Iter_51 ; backlog:baselinedAt "%s"^^xsd:dateTime ; backlog:isCurrentBaseline true ; backlog:hasBaselineStart "%s"^^xsd:dateTime ; backlog:hasBaselineEnd "2026-11-01T12:00:00"^^xsd:dateTime .\n' % (now, now))
    L.append('ex:PC3_Iter_51 a backlog:SprintPlanningCeremony ; rdfs:label "Planning of iteration 51: the engine refuses copied page items"@en ; backlog:ceremonyFor ex:Iter_51 ; backlog:heldAt "%s"^^xsd:dateTime ;\n    backlog:includesPlanningEvent ex:Plan3E_%s ;\n    rdfs:comment %s@en .\n' % (
        now, SID, lit("Held %s by the lineage agent after the owner's ruling: the story %s is committed to this iteration, whose goal is frozen at its start. No executor has started; work begun is recorded at the real start of the session with its brief." % (now, SID))))
    L.append('%s a backlog:ScopeChange ;\n    rdfs:label "Backlog widened by the seed ruling"@en ;\n    backlog:fulfillsRequest %s ; backlog:changesScope ex:Scope3 ; backlog:decidedBy backlog:Owner ;\n    backlog:admitsItem ex:%s ;\n    backlog:hasScopeChangeRationale %s .\n' % (
        SC, CR, SID, lit("Decided by the owner in his ruling of 2026-10-30 00:51 Istanbul (the page questions are seeds, not exam items); applied by the lineage agent. " + FOUND)))
    t, kk = re.subn(r'(%s a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending' % re.escape(CR), lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert kk == 1
    L.append('%s rdfs:comment "Disposition set to Accepted on %s in the version that records the ScopeChange %s and the story it admits; it was Pending before. The owner\'s ruling is the decision."@en .\n' % (CR, now[:10], SC[3:]))
    t += "\n" + "".join(L)
    return t + ('\n%s a backlog:StageOutput ;\n    rdfs:label "Closure of the Backlog stage of the third lineage, rebuilt by the stage revision from the Backlog stage for the seed ruling"@en ;\n    backlog:belongsToLineage ex:Lineage3 ;\n'
                '    backlog:outputOfStage backlog:Stage_Backlog ;\n    backlog:consumesOutput ex:Out3_ObjectiveR30 ;\n    backlog:hasStateDigest "%s" ;\n    backlog:closedAtCommit "PENDING" .\n') % (NEW, X.digest(t, "Backlog")), \
        "third lineage, Backlog stage rebuilt for the seed ruling: story %s with Build and Verify tasks and criterion %s in the new Iteration 51, the Items story rewritten and dependent on the new engine, scope change %s, change request Accepted; %d items re-admitted, not re-dated." % (SID, CRIT, SC[3:], n)

def ev_fill(t, prev):
    return G.fill_re(t, NEW, prev), "closedAtCommit of the rebuilt Backlog output %s set to the commit that closed it (%s); the seed ruling is planned, no work begun." % (NEW.replace("ex:", ""), prev)

def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"change": lambda: ev_change(t), "retract": lambda: ev_retract(t), "backlog": lambda: ev_backlog(t, sys.argv[2]), "fill": lambda: ev_fill(t, sys.argv[2])}
    if ev not in fn: raise SystemExit(__doc__)
    nt, comment = fn[ev](); print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))

if __name__ == "__main__":
    main()
