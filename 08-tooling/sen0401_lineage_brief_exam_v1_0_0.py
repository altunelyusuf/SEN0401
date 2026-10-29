#!/usr/bin/env python3
"""sen0401_lineage_brief_exam v1_0_0 - the executor brief of the exam tasks (TK_Exam_*) and the page-measurement tasks (TK_ChNN_PageMeasure_*) of the third lineage after the stage revision for the exam work (change request CR3_ExamMission); a NEW file over sen0401_lineage_brief_remedy_v1_7_0 (unchanged), which it copies and extends with an exam mode. (v1_7_0 doc: over v1_6_0: briefs of the retrofit tasks of Iterations 24 to 28 of the change request CR3_Retro24; the session and the criterion are read from the register; usage TASK[,TASK...]) -  generates the executor brief of ONE task of Iter_19 (the character set repair, change request CR3_Charset) from the register: the task, its story, its criterion with tools and versions, the owner's words, the measured facts,
the exclusions with the notes that lift them, the tools by version, and the rules of an executor. The coordinator passes a brief unedited; the register's note on 'work begun' names the same session. A brief is a rendering of the register at the version it names.
Usage (v1_6_0 adds the page tasks of Iter_23; v1_5_0 adds the repair tasks of Iter_22): sen0401_lineage_brief_remedy_v1_5_0.py TASK|ALL [OUTDIR]   (default 08-tooling/briefs/iter19; v1_1_0 over v1_0_0: adds the linked impediments of the task as a section and names the template, builders and page test that now exist)"""
__version__ = "1.0.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#"); REPO = M.REPO
SESS = {"TK_Ch78_DeckCheck": "SEN0401-I20-deckcheck", "TK_Ch07_Deck_Build": "SEN0401-I20-deck-ch07", "TK_Ch08_Deck_Build": "SEN0401-I20-deck-ch08", "TK_Ch07_Page_Build": "SEN0401-I20-page-ch07", "TK_Ch08_Page_Build": "SEN0401-I20-page-ch08"}
CRIT = {"TK_Ch78_DeckCheck": "AC7_DeckCheck", "TK_Ch07_Deck_Build": "AC7_Deck_Ch07", "TK_Ch08_Deck_Build": "AC7_Deck_Ch08", "TK_Ch07_Page_Build": "AC7_Page_Ch07", "TK_Ch08_Page_Build": "AC7_Page_Ch08"}
OWNER = "The owner, relayed by the coordinator, Friday 2026-10-23 16:06 Istanbul: chapters 6, 7 and 8 are urgent; chapters 7 and 8 need a deck, a chapter-code manifest and a page on the current standard (template 9.52.2, the character set declared first). After these, all chapters are retrofitted from chapter 1."
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The builder session writes it, records your start and runs the control through the evidence bridge after you report.
- A committed file is never edited: every output is a new file with a new version number. The only changes to gates, tests and templates that are allowed are the NEW files named in your task. No existing gate, test, threshold, template or criterion is edited or weakened.
- You never judge your own work with a tool you wrote: the deck check, the page test and the page tasks are separate sessions. A FAILING RESULT IS NEVER WORKED AROUND: no skipped feature, no raised timeout, no edited expected value. NOT_MEASURED, CANNOT_RUN and a skip are not passes.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a gate or a test beyond the named new files; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- Commit your work to main with a clear message (no force push; pull --rebase before push). Commit each verified step at once: the repository (committed and pushed work) is the only record if a container restarts.
- The machine has 2 cores shared with other sessions: run browser tests (page test runs take about nine minutes) one at a time, never a build beside a test; delete stale /tmp/sen0401_page_test_* and /tmp/sen0401_fx_* folders older than 60 minutes before a batch of runs (the root disk is small). A flaky main-thread budget failure (no [FAIL] feature line) may be run again up to three times, every run kept as a log; a [FAIL] line is a result.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed, if anything.
- Owner's standing teaching-material rules (they are the criteria, not decoration): full sentences are fine but no long paragraphs; explanation beside every code listing; the executed result of code shown as a visualization; an everyday analogy for each key concept; 5N1K stories with real names, real pictures and live links; native charts only; numbered slides; a resources slide; short speaker notes; no dark/light switching mid-deck; deck and page keep a matching look; pages: tabs are sub-menus of the selected item and never mixed with it, no third tab level, tabs and tree synchronised, uncrowded menu, no duplicated lists, content fits without scrolling, zoom on every diagram, default text not small and a text-size control, adaptive to phone and large screens, every term explained in full-sentence paragraphs, code that really runs."""
RULES += "\n- Browser tests (page tests and page checks) run ONLY under `flock /tmp/page_test.lock <command>`: they queue instead of overlapping with other sessions. Do not wait for a quiet machine by polling; take the lock."
TOOLS = [("Deck engine (existing)", "08-tooling/sen0401_deck_engine_v1_2_0.py", "the engine the earlier decks were built with; read it before writing a new generator"),
         ("Deck builders of the existing decks", "08-tooling/ch05-deck/deck_build_v2_0_0.py", "ch05; the same for 08-tooling/ch06-deck; the plans deck_plan_v2_3_0.json; REVIEW files hold the builder's own weak-spot list"),
         ("Existing decks", "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v2_3_0.pptx", "chapter 6: the newest .pptx in 03-materials/ch06 (read python-pptx 1.0.2 is installed in the system python3)"),
         ("Deck checks (existing)", "08-tooling/sen0401_deck_check_v1_1_0.py", "also deck_layout_check_v1_1_0.py, deck_notes_check_v1_1_0.py, sen0401_deck_arc_check_v1_1_0.py"),
         ("Chapter libraries", "08-tooling/ch05-page/ and 08-tooling/sen0401_ch05_wallet_lib_v1_1_0.py", "the functions the deck code calls (chapter 6: sen0401_ch06_tx_lib_v1_1_0.py); the page must define them to run the deck code"),
         ("Chapter research", "03-materials/ch05/rdodi/", "the research v1_1_x, the concept list (key concepts), the stories; chapter 6 the same under 03-materials/ch06/rdodi/"),
         ("Page template 9.52.2 (superseded for Iterations 24 to 28 by 9.52.3)", "08-tooling/course_page_template_v9_52_2.html", "Done and controlled; 9.52.1 (Done) is the newest template, whose character set tag lies at byte 13587; 9.52.2 (new file, made by TK_Charset_Template) is the template for the pages; 9.52.0 and 9.52.1 stay byte-identical; its DOM contract is in your criterion; the facts of how the page runs code are in 08-tooling/template952_logs/RUNTIME_FACTS.txt"),
         ("Page builder / page-data builder (newest)", "08-tooling/sen0401_page_build_v4_15_0.py and sen0401_page_data_v2_24_0.py", "v4_15_0 and v2_24_0 are the builders to use (Done and controlled; default template 9.52.0); the page version by PAGE_VER=...; the chapter-code manifest of the chapter is read from 03-materials/chNN/page (newest chapter_code_chNN_v*.json); PAGE_DATA_OUT / PAGE_SCRATCH send output to a scratch folder"),
         ("Page tests (newest)", "08-tooling/sen0401_page_test_v9_35_1.py and v9_34_1.py", "9.36.0 (Done and controlled, unchanged) measured the page standard before 9.37.0, which replaces it where your criterion names 9.37.0 (declare <meta name=\"page-standard\" content=\"9.52\">); also run 9.34.1 and 9.35.1; the runner is 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py NN PAGEVER with env PAGE_TEST=<file> and FULL_LOG=<path>"),
         ("Page charset check (new, made by TK_Charset_Check)", "08-tooling/sen0401_page_charset_check_v1_0_0.py", "python3 -B ... FILE...: exit 0 only when every file declares utf-8 within its first 1024 bytes and they decode as UTF-8"),
         ("Stage 4 gate runner", "08-tooling/sen0401_stage4_gates_v1_1_0.py", "python3 -B ... NN (reads the CURRENT validator v1.13.0)"),
         ("Lineage chapter check", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "Research/ChNN | Deck/ChNN | Page/ChNN (reads the PINNED validator v1.6.0)"),
         ("Stage 4 ABox builder", "08-tooling/sen0401_page_abox_build_v2_1_0.py", "builds the Stage 4 page ABox from the newest page; a new file"),
         ("Deck match check / link check", "08-tooling/pages_deck_match_verify_v1_1_0.py and pages_link_verify_v1_1_0.py", "0 'not carried' is required"),
         ("Existing pages", "03-materials/ch05/page/sen0401_ch05_page_v9_83_0.html and 03-materials/ch06/page/sen0401_ch06_page_v9_83_0.html", "the pages to remedy (not edited); their stored results are 08-tooling/ch05-page/ and ch06-page/test_results_abox_v9_74_0.json / v9_75_0.json")]
PRECEDENT = [("fd9152d", "the last resume of a page task, its brief and the executor's reporting"), ("7855fda", "the control of a regression, with the justification of a sample"), ("23e155f", "an executor's evidence logs for a page (chapter 10 page 9.79.0): the commit pattern to follow")]
SESS.update({"TK_Ch07_Deck_Reissue": "SEN0401-I20-deck-ch07-r2", "TK_PageTest937_Build": "SEN0401-I22-pagetest"})
CRIT.update({"TK_Ch07_Deck_Reissue": "AC7R_Deck_Ch07", "TK_PageTest937_Build": "AC7R_PageTest937"})
REPAIR = {"TK_Ch07_Deck_Reissue", "TK_PageTest937_Build"}
OWNER_R = "The course coordinator, Saturday 2026-10-24, after the controls of the builder session (register v0.244.0 and the root-cause analysis of the page 9.85.0): repairs rank first (the owner's rule that repairs re-rank the open items). Chapters 7 and 8 are urgent for the owner; their pages wait for these repairs."
PLAN_R = "Iteration 22 (the repairs, proposed end 2026-10-25 09:00 UTC, the owner decides): this task and the other repair task run in parallel; each is followed by a Verify task of the builder session, which has no executor. The pages of chapters 7 and 8 follow after the repairs. Browser tests run one at a time under the lock. Your estimate in the task text is an estimate; report a delay as soon as you know it."
SESS.update({"TK_Ch07_Page_Build_R": "SEN0401-I23-page-ch07", "TK_Ch08_Page_Finish": "SEN0401-I23-page-ch08"})
CRIT.update({"TK_Ch07_Page_Build_R": "AC8R_Page_Ch07", "TK_Ch08_Page_Finish": "AC8R_Page_Ch08"})
REPAIR21 = {"TK_Ch07_Page_Build_R", "TK_Ch08_Page_Finish"}
REPAIR = REPAIR | REPAIR21
OWNER_R21 = "The course coordinator, Saturday 2026-10-24, relaying the owner's standing rule of the same day (a lineage never waits on questions unrelated to its work; work the lineage enforces but the actual work misses must be dealt with) after the controls of the builder session (register v0.257.0 and v0.258.0): the page test 9.37.0 and the re-issued deck of chapter 7 are controlled MET, so the page criteria of chapters 7 and 8 are restated on 9.37.0 and the pages can proceed. Chapters 7 and 8 are urgent for the owner."
PLAN_R21 = "Iteration 23 (the pages of chapters 7 and 8, proposed end 2026-10-25 12:00 UTC): this task and the page task of the other chapter run in parallel; each is followed by a Verify task of the builder session, which has no executor. Every browser run (page tests, page checks) is serialised by the lock `flock /tmp/page_test.lock`, so two sessions never run a browser at once. Your estimate in the task text is an estimate; report a delay as soon as you know it."
TOOLS.insert(8, ("Page test 9.37.0 (new file, controlled MET in v0.258.0)", "08-tooling/sen0401_page_test_v9_37_0.py", "the page test your criterion names: the same features as 9.36.0, its P2 step waits until the result no longer shows the placeholder 'Running...'; run it with PAGE_TEST=<file> through the runner, under the lock; 9.36.0 stays unchanged and is not used for your page"))
OWNER_R24 = ("The owner's standing orders, relayed by the course coordinator: after the urgent chapters 5 to 8, return to ALL chapters starting with chapter 1 and bring each deck and page (and the research set and page ABox) to the course standard; the owner's teaching-material rules are the criteria: numbered slides, short sentences, explanation beside code, executed results as visualisations and native charts, analogies, 5N1K stories with real pictures and live links, a resources slide, short notes, a matching deck and page look; slide code is one chapter-code page tab (the manifest equals the deck's code boxes); "
             "the page fits without scrolling, has zoom for diagrams, adapts to phones, has a text-size control, and the text of every story is visible without scrolling past a full-height photograph (checked at 1366x768, 1400x900 and 390x844). Measured on 2026-10-25 by the lineage agent (impact assessment ex:IA3_Retro24 below).")
PLAN_R24 = ("Iteration 24 holds the decks of chapters 1, 2 and 3 and the template 9.52.3 (at most three executors at once; the template gates every page). Iteration 25: the story-layout repair of the pages of chapters 5 to 8, the deck of chapter 4, the chapter 1 verify script. Iteration 26: the pages of chapters 1 to 4. Iterations 27 and 28: chapters 9 to 14. Each Build is followed by a Verify task of the lineage agent, which has no executor and runs its own re-runs and the evidence bridge. "
            "Every browser run (page tests, the story layout probe) is serialised by the lock `flock /tmp/page_test.lock`, so two sessions never run a browser at once. Your estimate in the task text is an estimate; report a delay as soon as you know it.")
TOOLS.insert(3, ("Deck standard check v1_1_0 / overlap check / manifest control (the checks your deck is measured with)", "08-tooling/sen0401_deck_standard_check_v1_1_0.py, 08-tooling/deck_overlap_check_v1_0_0.py, 08-tooling/sen0401_deck_control_check_v1_1_0.py", "python3 -B <check> NN (the control check as `manifest:NN`); the overlap check takes the deck path; run all three on your deck until they pass; the baseline tool 08-tooling/sen0401_lineage_baseline_v1_0_0.py OUTDIR NN also scans a manifest for an example whose first output line starts with an error name"))
TOOLS.insert(4, ("Story layout probe (the owner's story rule, new)", "08-tooling/sen0401_story_layout_probe_v1_0_0.py", "python3 -B ... NN [PAGEVER] [LOGFILE] under `flock /tmp/page_test.lock`: for every story at 1366x768, 1400x900 and 390x844 the tallest photograph is shorter than the viewport and the narrative begins within the first screen"))
TOOLS.insert(5, ("Page template 9.52.3 (made by the task TK_Template_9523_Build of Iteration 24)", "08-tooling/course_page_template_v9_52_3.html", "the template for every page of Iterations 25 to 28; it caps the story photographs; not found until its task is Done"))
SUM = "briefs/iter47"
EXAM_OWNER = ("The owner's words of 2026-10-29, relayed by the coordinator and recorded in the register (ex:CR3_ExamMission, ex:Mission_V2): the course also assesses what it teaches. Build TWO printed exams for SEN0401, the midterm and a make-up exam over the same chapters, each a 60-minute sitting on physical printed paper. "
              "Use the interactive pages' exam engine as the starting point, but build a GENERAL engine for cross-chapter, synthesis and indirect questions (today's engines are chapter specific). Restrict question types and styles to those that suit a physical printed paper. Revive the critical points the owner explained in the course from the slides, notes, corpus and stories, and list plainly what could not be found. "
              "Find methods to reduce printed pages and mistakes in giving answers, and a reliable method to read, assess and grade each paper. Exam conventions: multiple-choice answer letters evenly distributed; fill-in option banks randomised; print-safe, white and line-based; no fabricated terms; items need course knowledge; a majority of items at the higher Bloom levels; versions incremented; light themes; no student personal data (synthetic stand-ins are allowed). "
              "THE CHAPTERS: 'The exact chapter content will be cleared tomorrow after the completion of the lectures. For SEN0401, we will be able to cover chapter 6 and all other chapters are in the scope of the exam. Possibly, we will not be able to finish Chapter 7.' The coordinator's reading: chapters 1 to 6 are in scope, chapter 7 is doubtful, the final list is due 2026-10-30. Make the chapter list a PARAMETER of everything you build (default chapters 1 to 6; chapter 7 selectable). Never decide what only the owner knows: put such questions to the coordinator plainly.")
EXAM_RULES_EXTRA = ("- Exam work goes in NEW files under 08-tooling/exam/ (create it if missing; paths and names with versions). The chapter banks and the interactive pages are read, never edited.\n"
                    "- Every claim about the repository is measured by you and printed; a gap is named plainly. Nothing is invented: every term in an item must appear in the course corpus, a slide, a speaker note, a page or the book (02-textbook).\n"
                    "- Synthetic stand-ins only: no real student name, number, paper or score.")
EXAM_TOOLS = [("Chapter question banks and their generators", "08-tooling/sen0401_ch0N_bank_gen_*.py and the pages in 03-materials/chNN/page", "1,453 single-answer four-option multiple-choice items over 8 chapters (measured 2026-10-29): Remember 322, Understand 413, Apply 483, Analyze 235; chapter 8 is all Remember; chapter 6 has no Analyze item; read them, never edit them"),
              ("Question bank structure check", "08-tooling/question_bank_check_v1_2_0.py", "checks structure only, not content"),
              ("Exam release code tool", "08-tooling/sen0401_exam_release_v1_0_0.py", "the screen exam mode of the pages (xExamStart etc.); the exam work is NOT screen delivery"),
              ("Assessment plan", "04-assessment/sen0401_assessment_v1_0_0.ttl", "the Midterm component is 30 percent"),
              ("Decks, speaker notes, research, stories", "03-materials/chNN/*.pptx (newest), 03-materials/chNN/rdodi/", "the sources of the critical points; the course outline is in 01-outcomes and 00-course-profile"),
              ("The book", "02-textbook", "Mastering Bitcoin, third edition (CC BY-SA 4.0): the reference for every term"),
              ("Exam Studio toolset", "NOT in this repository", "measured 2026-10-29: the renderer, the 19 gates, the grading pipeline and the CATS export are not here; build what you need as new files and say what you could not reuse")]
PAGE_TOOLS = [("Page tests (new, controlled)", "08-tooling/sen0401_page_test_v9_34_2.py, sen0401_page_test_v9_35_2.py, sen0401_page_test_v9_37_0.py", "the three tests of your task; never edit them"),
              ("Page test runner", "08-tooling/sen0401_lineage_page_test_run_v1_2_0.py NN PAGEVER", "with env PAGE_TEST=<file> and FULL_LOG=<path>; ALWAYS under `flock /tmp/page_test.lock`; each run takes about 9 to 19 minutes"),
              ("Pages", "03-materials/chNN/page/ (the newest sen0401_chNN_page_v*.html)", "read, never changed")]
EXAM_PLAN = {"Iter_47": "Iteration 47 (planned end 2026-10-30 20:00 UTC) and Iteration 48 (planned end 2026-11-01 12:00 UTC) hold the exam work; chapter work restarts on Sunday 2026-11-01. Each Build is followed by a Verify task of the lineage agent, which has no executor. The midterm is next week: report a delay as soon as you know it.",
             "Iter_48": "Iteration 48 (planned end 2026-11-01 12:00 UTC). Report a delay as soon as you know it.",
             "Iter_49": "Iteration 49 (from 2026-11-01 12:00 UTC, after the weekly usage limit resets): the pages of chapters 1 to 6 are measured first, chapters 7 and 8 only if time remains; chapter 11 and chapters 9 and above stay paused. Browser runs are serial under the lock."}



def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout.strip()


def one(g, ver, tid, out):
    t = E[tid]; assert (t, None, None) in g, tid
    story0 = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    sess = SESS.get(tid) or re.search(r"Planned session (SEN0401-[A-Za-z0-9-]+)", text(g, t, B.hasAuditNote)).group(1); crit = CRIT.get(tid) or str(next(g.objects(story0, B.hasAcceptanceCriterion))).split("#")[1]
    XM = tid.startswith("TK_Exam_") or "_PageMeasure_" in tid
    R24 = tid.endswith("_R24") or tid.startswith("TK_Template_9523") or tid.startswith("TK_Ch01_VerifyScript")
    deps = [str(x).split("#")[1] for x in g.objects(t, B.dependsOn)]; blocked = [d for d in deps if str(g.value(E[d], B.hasState)).split("#")[1] != "Done"]
    story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    c = E[crit]; tools = sorted(str(x).split("#")[1] for x in g.objects(c, B.measuredWithTool))
    excl = [x for x in g.objects(E.Scope3, B.hasScopeExclusion) if not XM or str(x).split("#")[1].startswith("Excl3_Exam")]
    ia = text(g, E.IA3_ExamMission if XM else E.IA3_Retro24 if R24 else E.IA3_Repair21 if tid in REPAIR21 else (E.IA3_Repair20 if tid in REPAIR else E.IA3_Ch78), B.hasImpactStatement)
    L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state in the register: %s)." % (ver, tid, str(g.value(t, B.hasState)).split("#")[1]),
         "Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % sess, "", "## Why this work exists (the owner's words)" if (tid not in REPAIR and not R24) else "## Why this work exists (the coordinator's order)", EXAM_OWNER if XM else OWNER_R24 if R24 else (OWNER_R21 if tid in REPAIR21 else OWNER_R) if tid in REPAIR else OWNER, "", "## Rules of an executor", ("\n".join(l for l in RULES.split("\n") if "teaching-material rules" not in l) + "\n" + EXAM_RULES_EXTRA) if XM else RULES, ""]
    if blocked:
        L += ["## Do not start until", "Task(s) %s are Done in the register (the builder session controls them and tells the coordinator)." % ", ".join(blocked), ""]
    imps = sorted(g.subjects(B.impedes, t), key=str)
    IL = []
    for im in imps:
        done = g.value(im, B.resolvedAt)
        IL += ["- **%s** (%s)" % (text(g, im, rdflib.RDFS.label), "CLEARED %s" % done if done else "OPEN: it blocks until your task handles it"), "  %s" % text(g, im, B.hasImpedimentStatement)]
    L += ["## The task", "**%s**" % text(g, t, rdflib.RDFS.label), "", text(g, t, B.hasAuditNote), "",
          "## Impediments and facts linked to this task in the register (register nodes, backlog:impedes)"] + (IL or ["- none"]) + ["", "Depends on: %s" % (", ".join(deps) or "nothing"), "",
          "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "", "## The criterion it satisfies (%s)" % crit, "**%s**" % text(g, c, rdflib.RDFS.label), "", text(g, c, B.hasGherkinText), "",
          "Measured with (register, G136): %s. Versions: %s" % (", ".join(tools), text(g, c, B.measuredWithVersion)), "", "## What the scope excludes (and what is lifted)"]
    for x in excl:
        L += ["- **%s**: %s" % (text(g, x, rdflib.RDFS.label), text(g, x, B.excludesConcern)), "  Notes: %s" % " | ".join(str(cm) for cm in g.objects(x, rdflib.RDFS.comment) if "2026-10-22" in str(cm))]
    L += ["", "## Tools and gates, by version"]
    for name, path, how in ((PAGE_TOOLS if "_PageMeasure_" in tid else EXAM_TOOLS) if XM else TOOLS):
        p0 = path.split(" and ")[0].split(" ")[0]
        L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(REPO, p0)) else " (**not found at this path now: it may be a file another task creates, or search for the committed file of that name**)", how))
    L += ["- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0; the chapter checks read the PINNED v1.6.0. Both must pass; they differ, so report each as printed.", "", "## Precedents in git (read them first)"]
    for sha, what in PRECEDENT:
        L.append("- `%s` %s%s" % (sha, what, "" if run("git", "cat-file", "-t", sha) == "commit" else " (**commit not found**)"))
    L += ["", ("## Measured facts, the cost of the route and the owner's statements (impact assessment ex:IA3_ExamMission and change request ex:CR3_ExamMission)" if XM else "## Measured facts and the written standard (impact assessment ex:IA3_Retro24, measured by the lineage agent on 2026-10-25)" if R24 else "## Measured facts and the written standard (impact assessment ex:IA3_Repair21, measured by the builder session on 2026-10-24)" if tid in REPAIR21 else "## Measured facts and the written standard (impact assessment ex:IA3_Ch78, measured by the builder session on 2026-10-23)"), ia, "",
          ("The change request (the owner's statements and the verified gaps G1 to G7): " + text(g, E.CR3_ExamMission, B.hasChangeRequestRationale)) if XM else "", "## Plan and the order of work", EXAM_PLAN[str(g.value(t, B.memberOfContainer)).split("#")[1]] if XM else PLAN_R24 if R24 else (PLAN_R21 if tid in REPAIR21 else PLAN_R) if tid in REPAIR else "Iteration 20 (urgent, until 2026-10-24 09:00): TK_Ch78_DeckCheck (the deck standard check v1_1_0 for chapters 8 to 14; a new file), TK_Ch07_Deck_Build and TK_Ch08_Deck_Build (may start at once, in parallel with it), then the page builds TK_Ch07_Page_Build and TK_Ch08_Page_Build after their deck Verify is Done. Each Build is followed by a Verify task of the builder session, which has no executor. Page tests run one at a time under the lock. Your own estimate in the task text is an estimate; report a delay as soon as you know it."]
    body = re.sub(r"SEN0401-I\d+-[a-z0-9-]+", lambda m: m.group(0) if m.group(0) == sess else "another executor session", "\n".join(L))   # a brief names no session but its recipient
    open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write(body)
    return sess, ("no, after %s" % ", ".join(blocked)) if blocked else "yes"


def rank_of(g, tid):
    st = next((s for s in g.subjects(B.decomposesInto, E[tid]) if (s, rdflib.RDF.type, B.Story) in g), None); best = None
    for sc in g.objects(st, B.hasPriorityScore):
        at = str(g.value(sc, B.scoredAt)); v = round(float(g.value(sc, B.hasScoreValue)) * float(g.value(sc, B.hasDepFactor) or 1), 2)
        if best is None or at > best[0]: best = (at, v)
    return best[1] if best else None


def main():
    ONLY = sys.argv[1]; out = os.path.join(REPO, sys.argv[2] if len(sys.argv) > 2 else SUM); os.makedirs(out, exist_ok=True)
    src = M.newest(); g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    ids = ONLY.split(",")
    idx = ["# Executor briefs of the exam work (change request CR3_ExamMission; generated from %s)\n" % ver, "The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.\n", "| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |", "|---|---|---|---|---|"]
    ids = sorted(ids, key=lambda x: -(rank_of(g, x) or 0))
    for k, tid in enumerate(ids):
        sess, can = one(g, ver, tid, out); idx.append("| %d | %s | %s | %s | %s |" % (k + 1, tid, sess, can, rank_of(g, tid)))
    open(os.path.join(out, "INDEX.md" if len(ids) > 1 else "INDEX_%s.md" % ONLY), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(ids), "briefs from", ver); print("\n".join(idx[4:]))


main()
