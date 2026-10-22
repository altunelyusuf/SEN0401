#!/usr/bin/env python3
"""sen0401_lineage_brief_gates v1_1_0 (over 1.0.0: writes only the briefs of tasks not yet started or resumed, so a brief already passed is not changed; the facts of the control of 2026-10-22 v0.182: the click timeout is a test artefact, template 9.51.1 and tests 9.34.1/9.35.1 exist, disk cleaning) - generates the executor brief of each executor task of the page gates (iteration 16 and the resumed page tasks of iteration 14) FROM THE REGISTER (task text, its story, the criteria it satisfies with tools and versions,
the exclusions of the scope with the notes that lift them, the facts), plus the rules of an executor and the precedents. The coordinator passes a brief unedited; the register's note on 'work begun' names the same session.
A brief is a rendering of the register at the version it names; if the register changes, it is generated again. Usage: sen0401_lineage_brief_gates_v1_0_0.py [OUTDIR]   (default 08-tooling/briefs/iter16)"""
__version__ = "1.1.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
REPO = M.REPO
TASKS = {  # task: (session, criteria, blocked until)
    "TK_PageGates_Template": ("SEN0401-I16-template", ["AC3P_Template"], []),
    "TK_PageGates_Test": ("SEN0401-I16-test", ["AC3P_Test"], []),
    "TK_PageGates_Regression": ("SEN0401-I16-regression", ["AC3P_Regression"], ["TK_PageGates_Template", "TK_PageGates_Test"]),
    "TK_SecLinks_Ch10_Page": ("SEN0401-I14-page-ch10-r2", ["AC3L2_Ch10"], ["TK_PageGates_Template", "TK_PageGates_Test", "TK_PageGates_Regression"]),
    "TK_SecLinks_Ch11_Page": ("SEN0401-I14-page-ch11-r2", ["AC3L2_Ch11"], ["TK_PageGates_Template", "TK_PageGates_Test", "TK_PageGates_Regression"])}
OWNER = ('"Yes, proceed." (the owner, relayed by the coordinator, Thursday 2026-10-22 08:35 Istanbul), answering: "Do you approve building a new page template version and a new page-test version as NEW files (the old ones kept for comparison), so that the section-link pages of chapters 10 and 11 can be rebuilt and measured: '
         'the template with an Untangle fix for dense section edges, and the test with the \'mentioned-together relations\' assertion applying only to a page that has such relations (yes or no)?" The earlier owner direction stands: the relationships between sections are stated in the research as links and the pages show them.')
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The builder session writes it; it records your start and runs the control through the evidence bridge after you report.
- A committed file is never edited: every output is a new file with a new version number. The ONLY changes to gates, tests and templates that the owner has approved are the new files named in your task (template 9.51.1; page tests 9.34.1 and 9.35.1). No other gate, test, threshold or template is changed (Stage 3.F, the Stage 4 gates, the chapter checks, the deck match check, every other assertion of the page tests); no citation or claim is removed only to make a check pass.
- A FAILING RESULT IS NEVER WORKED AROUND: no force-click, no changed click target, no raised timeout, no skipped feature, no edited expected value makes a result. If a click times out, analyse why and report the cause as a fact with measurements. NOT_MEASURED, CANNOT_RUN and a skip are not passes. A page test with a TEST release key proves page logic only.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a gate or a test beyond the named new files; the deck would have to change; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- Commit your work to main with a clear message (no force push; pull --rebase before push). Do not wait for or ask for approvals nobody can give: tell the coordinator the exact command.
- If a container restart interrupts you, the repository (committed and pushed work) is the only record: commit each verified step at once.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed, if anything.
- Page-test runs take about nine minutes each; run them one after the other (they share the machine); a flaky main-thread budget failure (no [FAIL] feature line) may be run again up to three times, every run kept as a log; a [FAIL] line is a result."""
TOOLS = [("Page template (old, comparison)", "08-tooling/course_page_template_v9_51_0.html", "template 9.51.0, byte-identical forever; concept-map Untangle = function rlUntangle (from line 684), ERD layout = erdUntangle (from line 1536); markers 'const LBLRE=LBL.map' and 'function edVars()'"),
         ("Page test 9.35.0 (old, comparison)", "08-tooling/sen0401_page_test_v9_35_0.py", "the assertion to change is the feature \"the ERD's sections choice draws one entity per section with the mentioned-together relationships on by default ...\" (line 1245); NOREL at line 153"),
         ("Page test 9.34.0 (old, comparison)", "08-tooling/sen0401_page_test_v9_34_0.py", "the same feature at line 1241"),
         ("Page test runner for the lineage", "08-tooling/sen0401_lineage_page_test_run_v1_2_0.py", "python3 -B 08-tooling/sen0401_lineage_page_test_run_v1_2_0.py NN PAGEVER with env PAGE_TEST=<file name of the test> (default: the newest test) and FULL_LOG=<path> ; runs the test on a key-substituted TEST copy"),
         ("Page builder", "08-tooling/sen0401_page_build_v4_14_0.py", "the newest page builder; the template is a default inside it or an argument: read it and state exactly how you passed template 9.51.1"),
         ("Page-data builder (new)", "08-tooling/sen0401_page_data_v2_23_0.py", "reads the section links of the new research as page relations"),
         ("Stage 4 gate runner", "08-tooling/sen0401_stage4_gates_v1_1_0.py", "python3 -B 08-tooling/sen0401_stage4_gates_v1_1_0.py NN (reads the CURRENT validator v1.13.0)"),
         ("Lineage chapter check", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "Research/ChNN | Deck/ChNN | Page/ChNN (reads the PINNED validator v1.6.0)"),
         ("Stage 4 ABox builder", "08-tooling/sen0401_page_abox_build_v2_1_0.py", "builds the Stage 4 page ABox from the newest page; a new file"),
         ("Deck match check", "08-tooling/pages_deck_match_verify_v1_0_0.py", "0 'not carried' is required"),
         ("Page link check", "08-tooling/pages_link_verify_v1_0_0.py", "as the precedent commits ran it"),
         ("Page check wrapper", "08-tooling/sen0401_lineage_page_check_v1_1_0.py", "KIND:NN, the exit-code form of each element, as the builder's bridge runs it (kinds markers, deck, link, seclinks, erd, test34, test35, counts34, counts35, abox, nochange)")]
PRECEDENT = [("a52911a", "chapter 10 page 9.78.0 (research v1.2.0, page data 2.23.0, template 9.51.0): the build and the failing page tests; logs in 08-tooling/ch10-evidence"),
             ("7aaba8d", "chapter 11 page 9.78.0 built; 2de9dcf its crash log and the force-click diagnostic (a diagnostic, never a result)"),
             ("2a20df6", "chapter 10 page 9.77.0 on template 9.51.0 (the shipped page)")]
FACTS = ["Control of 2026-10-22 on the bridge (register v0.173; logs in 08-tooling/verify/iter14/ch10 and ch11): page 9.78.0 of chapter 10 fails 4 of 370 features in each of the tests 9.34.0 and 9.35.0, which are 2 distinct features: (A) the ERD sections-choice feature with the mentioned-together relations (sections 17, relations 23 -> 23 with mentions off; the assertion r2 > r3 assumes any page with a relation between two sections has 'mentions'; the page data holds 0 'mentions', the new section links are all 'operates on'); (B) the concept-map feature 'Untangle leaves no two boxes overlapping' (24 boxes, 2 overlap; template function rlUntangle).",
         "Page 9.78.0 of chapter 11 stops in both tests, in the first run of each, on a click timeout (HeaderFields intercepts pointer events). ESTABLISHED as a fact by the executors of Iter_16 and confirmed by the builder: it is a TEST ARTEFACT, not the template layout. The test drags the first ERD entity 120 px right and 70 px down over HeaderFields, GenesisQuirks and BackLinks and then clicks the SAME entity (9.35.1 lines 1256-1263); HeaderFields, drawn later, intercepts the pointer; template 9.51.1 gives the identical result. Chapter 10's click works (it clicks a different entity). The owner has been asked whether the test may change that click (change request CR3_PageClick, pending); until he answers, the chapter 11 page cannot pass the page tests 9.34.1 and 9.35.1 and no task works around it: no force-click, no changed click target.",
         "Iter_16 delivered (controlled, register v0.182): template course_page_template_v9_51_1.html (Untangle separation pass in rlUntangle; the concept-map overlaps after Untangle are 2 -> 0 on chapter 10 and 4 -> 0 on chapter 11) and the page tests sen0401_page_test_v9_34_1.py and v9_35_1.py (only the mentioned-together assertion changed; test 9.35.1 on chapter 1 page 9.70.0 equals the stored result of 9.35.0, 372 passed, 0 failed). Read their evidence in 08-tooling/page-gates-evidence/.",
         "DISK: stale temporary folders (/tmp/sen0401_page_test_* and /tmp/sen0401_fx_*) of earlier sessions filled the root disk to 28 MB free and crashed browser runs ('Target crashed', 'Page crashed') of the test task. Before each batch of page-test runs delete those folders when older than 60 minutes (find /tmp -maxdepth 1 -name 'sen0401_page_test_*' -mmin +60 -exec rm -rf {} + ; the same for 'sen0401_fx_*'), check df -h /, keep the logs. A crash with a full disk is not a result.",
         "The ERD label features themselves run and pass on both pages (chapter 10: labels shown 23 -> 23, overlaps 0/0; the filled ERD of chapter 11: 32 labels, 0 overlapping pairs). The shipped pages 9.77.0 of chapters 10 and 11 passed because the test skipped assertion (A) for them (NOREL: no relation between two sections)."]


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout.strip()


def main():
    out = os.path.join(REPO, sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/iter16"); os.makedirs(out, exist_ok=True)
    src = M.newest(); g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    excl = [x for x in g.objects(E.Scope3, B.hasScopeExclusion)]
    index = ["# Executor briefs of the page gates (generated from %s)\n" % ver, "The Verify tasks (TK_SecLinks_Ch10_Verify, TK_SecLinks_Ch11_Verify) have no executor: the builder session controls and runs the evidence bridge after the executors report. "
             "The earlier briefs of the page tasks (08-tooling/briefs/iter14/BRIEF_TK_SecLinks_Ch1[01]_Page.md) are superseded by the ones here.\n", "| Task | Executor session | Can start |", "|---|---|---|"]
    for tid, (sess, crits, blocked) in TASKS.items():
        t = E[tid]; assert (t, None, None) in g, tid
        if str(g.value(t, B.hasState)).split("#")[1] in ("InProgress", "Done"):
            index.append("| %s | %s | begun or done: brief passed earlier (not regenerated) |" % (tid, sess)); continue
        blocked = [b for b in blocked if str(g.value(E[b], B.hasState)).split("#")[1] != "Done"]   # only what is not Done yet blocks
        note = text(g, t, B.hasAuditNote); title = text(g, t, rdflib.RDFS.label)
        story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
        deps = [str(x).split("#")[1] for x in g.objects(t, B.dependsOn)]; state = str(g.value(t, B.hasState)).split("#")[1]
        L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state in the register: %s)." % (ver, tid, state),
             "Executor session name: **%s**. The register's note on 'work begun' (or on the resume of a paused task) for this task names this session." % sess, "",
             "## Why this work exists (the owner's answer)", OWNER, "", "## Rules of an executor", RULES, ""]
        if blocked:
            L += ["## Do not start until", "Task(s) %s are Done in the register (the builder session controls them and tells the coordinator)." % ", ".join(blocked), ""]
        L += ["## The task", "**%s**" % title, "", note, "", "Depends on: %s" % (", ".join(deps) or "nothing"), "",
              "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "", "As a %s I want %s so that %s." % (text(g, story, B.asRole), text(g, story, B.wantsCapability), text(g, story, B.soThat)), ""]
        for crit in crits:
            c = E[crit]; tools = sorted(str(x).split("#")[1] for x in g.objects(c, B.measuredWithTool))
            L += ["## The criterion it satisfies (%s)" % crit, "**%s**" % text(g, c, rdflib.RDFS.label), "", text(g, c, B.hasGherkinText), "",
                  "Measured with (register, G136): %s. Versions: %s" % (", ".join(tools), text(g, c, B.measuredWithVersion)), "", "Satisfied by: %s" % text(g, c, B.satisfiedByArtifact), ""]
        L += ["## What the scope excludes (and what the owner lifted)"]
        for x in excl:
            L += ["- **%s**: %s" % (text(g, x, rdflib.RDFS.label), text(g, x, B.excludesConcern)), "  Notes: %s" % " | ".join(str(c) for c in g.objects(x, rdflib.RDFS.comment) if "2026-10-22" in str(c))]
        L += ["", "## Tools and gates, by version"]
        for name, path, how in TOOLS:
            L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(REPO, path)) else " (**not found at this path now: it may be a file another task creates, or search for the committed file of that name**)", how))
        L += ["- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0; the chapter checks read the PINNED v1.6.0. Both must pass; they differ, so report each as printed.", "", "## Precedents in git (read them first)"]
        for sha, what in PRECEDENT:
            L.append("- `%s` %s%s" % (sha, what, "" if run("git", "cat-file", "-t", sha) == "commit" else " (**commit not found**)"))
        L += ["- `08-tooling/verify/iter14/ch10/` and `ch11/` hold the builder's control logs of 2026-10-22 (page tests, Stage 4 runner, chapter checks).", "", "## Facts measured on 2026-10-22 (builder session)"] + FACTS + [""]
        if tid in ("TK_SecLinks_Ch10_Page", "TK_SecLinks_Ch11_Page"):
            L += ["## How to build (resumed task)", "The page 9.78.0 you find (a52911a; 7aaba8d) and its page data (08-tooling/chNN-page/page_data_v9_78_0.json, extra_resolved, corpus manifest) were built on template 9.51.0 and are NOT edited. Build the NEW page version 9.79.0 as new files from the same research and page data on the template 9.51.1, with the page builder v4_14_0 (state how you passed the template), "
                  "run the page tests 9.34.1 and 9.35.1 with the runner (PAGE_TEST=sen0401_page_test_v9_34_1.py and v9_35_1.py), store the result as test_results_abox_v9_79_0.json beside the earlier ones, and build the Stage 4 page ABox sen0401_chNN_page_abox_v9_79_0.ttl with the Stage 4 builder. Run the Stage 4 runner, the three chapter checks, the deck match check, the link check and the template markers on it. If the template and test tasks left any result you cannot reconcile with this brief, STOP and report.", ""]
        open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L))
        index.append("| %s | %s | %s |" % (tid, sess, "no, after %s" % ", ".join(blocked) if blocked else "yes"))
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    print(out, len(TASKS), "briefs from", ver)


main()
