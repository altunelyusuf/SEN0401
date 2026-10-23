#!/usr/bin/env python3
"""sen0401_lineage_brief_remedy v1_2_0 - generates the executor brief of ONE task of Iter_18 (the story chip repair, change request CR3_ChipScroll) from the register: the task, its story, its criterion with tools and versions, the owner's words, the measured facts,
the exclusions with the notes that lift them, the tools by version, and the rules of an executor. The coordinator passes a brief unedited; the register's note on 'work begun' names the same session. A brief is a rendering of the register at the version it names.
Usage: sen0401_lineage_brief_remedy_v1_2_0.py TASK|ALL [OUTDIR]   (default 08-tooling/briefs/iter18; v1_1_0 over v1_0_0: adds the linked impediments of the task as a section and names the template, builders and page test that now exist)"""
__version__ = "1.2.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#"); REPO = M.REPO
SESS = {"TK_Repair_Template": "SEN0401-I18-template", "TK_Repair_Page_Ch05_Build": "SEN0401-I18-page-ch05", "TK_Repair_Page_Ch06_Build": "SEN0401-I18-page-ch06"}
CRIT = {"TK_Repair_Template": "AC5R_Template", "TK_Repair_Page_Ch05_Build": "AC5R_Page_Ch05", "TK_Repair_Page_Ch06_Build": "AC5R_Page_Ch06"}
OWNER = ("The owner, relayed by the coordinator, Thursday 2026-10-22 17:30 Istanbul: \"I want you to remedy the weaknesses and provide me Chapter 5 and 6 PPT and Interactive pages ready to use.\" The owner uses the materials in class. Friday 2026-10-23: the chapter 5 page 9.80.0 fails one feature (a story chip on a concept does not bring its story into view: story GoxColdFind lands at 2064 px, outside the 768 px viewport); the cause is in page template 9.52.0 (the click handler scrolls before the pane height is fitted). This iteration repairs the template and rebuilds the two pages on it.")
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
TOOLS = [("Deck engine (existing)", "08-tooling/sen0401_deck_engine_v1_2_0.py", "the engine the earlier decks were built with; read it before writing a new generator"),
         ("Deck builders of the existing decks", "08-tooling/ch05-deck/deck_build_v2_0_0.py", "ch05; the same for 08-tooling/ch06-deck; the plans deck_plan_v2_3_0.json; REVIEW files hold the builder's own weak-spot list"),
         ("Existing decks", "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v2_3_0.pptx", "chapter 6: the newest .pptx in 03-materials/ch06 (read python-pptx 1.0.2 is installed in the system python3)"),
         ("Deck checks (existing)", "08-tooling/sen0401_deck_check_v1_1_0.py", "also deck_layout_check_v1_1_0.py, deck_notes_check_v1_1_0.py, sen0401_deck_arc_check_v1_1_0.py"),
         ("Chapter libraries", "08-tooling/ch05-page/ and 08-tooling/sen0401_ch05_wallet_lib_v1_1_0.py", "the functions the deck code calls (chapter 6: sen0401_ch06_tx_lib_v1_1_0.py); the page must define them to run the deck code"),
         ("Chapter research", "03-materials/ch05/rdodi/", "the research v1_1_x, the concept list (key concepts), the stories; chapter 6 the same under 03-materials/ch06/rdodi/"),
         ("Page template (newest)", "08-tooling/course_page_template_v9_52_0.html", "Done and controlled but with the story chip scroll defect named in your criterion; 9.52.1 (new file, made by TK_Repair_Template) is the template for the pages; 9.52.0 stays byte-identical; its DOM contract is in your criterion; the facts of how the page runs code are in 08-tooling/template952_logs/RUNTIME_FACTS.txt"),
         ("Page builder / page-data builder (newest)", "08-tooling/sen0401_page_build_v4_14_0.py and sen0401_page_data_v2_23_0.py", "v4_15_0 and v2_24_0 are the builders to use (Done and controlled; default template 9.52.0); the page version by PAGE_VER=...; the chapter-code manifest of the chapter is read from 03-materials/chNN/page (newest chapter_code_chNN_v*.json); PAGE_DATA_OUT / PAGE_SCRATCH send output to a scratch folder"),
         ("Page tests (newest)", "08-tooling/sen0401_page_test_v9_35_1.py and v9_34_1.py", "9.36.0 (Done and controlled) is the page test that measures the page standard (declare <meta name=\"page-standard\" content=\"9.52\">); also run 9.34.1 and 9.35.1; the runner is 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py NN PAGEVER with env PAGE_TEST=<file> and FULL_LOG=<path>"),
         ("Stage 4 gate runner", "08-tooling/sen0401_stage4_gates_v1_1_0.py", "python3 -B ... NN (reads the CURRENT validator v1.13.0)"),
         ("Lineage chapter check", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "Research/ChNN | Deck/ChNN | Page/ChNN (reads the PINNED validator v1.6.0)"),
         ("Stage 4 ABox builder", "08-tooling/sen0401_page_abox_build_v2_1_0.py", "builds the Stage 4 page ABox from the newest page; a new file"),
         ("Deck match check / link check", "08-tooling/pages_deck_match_verify_v1_1_0.py and pages_link_verify_v1_1_0.py", "0 'not carried' is required"),
         ("Existing pages", "03-materials/ch05/page/sen0401_ch05_page_v9_74_0.html and 03-materials/ch06/page/sen0401_ch06_page_v9_75_0.html", "the pages to remedy (not edited); their stored results are 08-tooling/ch05-page/ and ch06-page/test_results_abox_v9_74_0.json / v9_75_0.json")]
PRECEDENT = [("fd9152d", "the last resume of a page task, its brief and the executor's reporting"), ("7855fda", "the control of a regression, with the justification of a sample"), ("23e155f", "an executor's evidence logs for a page (chapter 10 page 9.79.0): the commit pattern to follow")]
SUM = "08-tooling/briefs/iter18"


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout.strip()


def one(g, ver, tid, out):
    t = E[tid]; assert (t, None, None) in g, tid
    sess = SESS[tid]; crit = CRIT[tid]
    deps = [str(x).split("#")[1] for x in g.objects(t, B.dependsOn)]; blocked = [d for d in deps if str(g.value(E[d], B.hasState)).split("#")[1] != "Done"]
    story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
    c = E[crit]; tools = sorted(str(x).split("#")[1] for x in g.objects(c, B.measuredWithTool))
    excl = [x for x in g.objects(E.Scope3, B.hasScopeExclusion)]
    ia = text(g, E.IA3_ChipScroll, B.hasImpactStatement)
    L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state in the register: %s)." % (ver, tid, str(g.value(t, B.hasState)).split("#")[1]),
         "Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % sess, "", "## Why this work exists (the owner's words)", OWNER, "", "## Rules of an executor", RULES, ""]
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
    for name, path, how in TOOLS:
        p0 = path.split(" and ")[0].split(" ")[0]
        L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(REPO, p0)) else " (**not found at this path now: it may be a file another task creates, or search for the committed file of that name**)", how))
    L += ["- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0; the chapter checks read the PINNED v1.6.0. Both must pass; they differ, so report each as printed.", "", "## Precedents in git (read them first)"]
    for sha, what in PRECEDENT:
        L.append("- `%s` %s%s" % (sha, what, "" if run("git", "cat-file", "-t", sha) == "commit" else " (**commit not found**)"))
    L += ["", "## Measured facts and the written standard (impact assessment ex:IA3_ChipScroll; the builder session re-ran the page tests on both pages on 2026-10-23)", ia, "",
          "## Plan and the order of work", "Tasks of the iteration, in dependency order: TK_Repair_Template (executor; may start at once), TK_Repair_Template_Verify (builder), then TK_Repair_Page_Ch05_Build and TK_Repair_Page_Ch06_Build (executors, together), each followed by its Verify (builder). The page tasks start only when the template Build and Verify are Done in the register; the builder session controls them and tells the coordinator. Your own estimate in the task text is an estimate; report a delay as soon as you know it."]
    open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L))
    return sess, ("no, after %s" % ", ".join(blocked)) if blocked else "yes"


def main():
    ONLY = sys.argv[1]; out = os.path.join(REPO, sys.argv[2] if len(sys.argv) > 2 else SUM); os.makedirs(out, exist_ok=True)
    src = M.newest(); g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    ids = list(SESS) if ONLY == "ALL" else [ONLY]
    idx = ["# Executor briefs of Iteration 17: the chapter 5 and 6 remedy (generated from %s)\n" % ver, "The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.\n", "| Task | Executor session | Can start |", "|---|---|---|"]
    for tid in ids:
        sess, can = one(g, ver, tid, out); idx.append("| %s | %s | %s |" % (tid, sess, can))
    open(os.path.join(out, "INDEX.md" if ONLY == "ALL" else "INDEX_%s.md" % ONLY), "w", encoding="utf-8").write("\n".join(idx) + "\n")
    print(out, len(ids), "briefs from", ver); print("\n".join(idx[4:]))


main()
