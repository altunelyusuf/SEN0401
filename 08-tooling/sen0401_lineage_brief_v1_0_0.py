#!/usr/bin/env python3
"""sen0401_lineage_brief v1_0_0 - generates the executor brief of each READY Build task of the template iteration FROM THE REGISTER (task text, its story, the criterion it satisfies, the exclusions of the scope, the written
standard) plus the tools and gates by version, the precedents and the rules of an executor, and names the executor session. The coordinator passes a brief unedited; the register's note on 'work begun' names the same session.
A brief is a rendering of the register at the version it names: if the register changes, the brief is generated again.
Usage: sen0401_lineage_brief_v1_0_0.py [OUTDIR]   (default 08-tooling/briefs/iter13)"""
__version__ = "1.0.0"
import os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
REPO = M.REPO
SESSIONS = {"TK_Ch08Ex_Build": "SEN0401-I13-ch08-examples", "TK_PageTpl_Ch08_Build": "SEN0401-I13-page-ch08", "TK_PageTpl_Ch10_Build": "SEN0401-I13-page-ch10",
            "TK_PageTpl_Ch11_Build": "SEN0401-I13-page-ch11", "TK_PageTpl_Ch12_Build": "SEN0401-I13-page-ch12", "TK_PageTpl_Ch14_Build": "SEN0401-I13-page-ch14"}
BLOCKED = {"TK_PageTpl_Ch08_Build": "TK_Ch08Ex_Build"}
TOOLS = [("Stage 4 gate runner", "08-tooling/sen0401_stage4_gates_v1_1_0.py", "python3 -B 08-tooling/sen0401_stage4_gates_v1_1_0.py NN   (NN = 08, 10, ...; reads the CURRENT RDODI validator v1.13.0)"),
         ("Lineage chapter check", "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py", "python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Research/ChNN | Deck/ChNN | Page/ChNN   (reads the PINNED validator v1.6.0)"),
         ("Page test 9.35.0", "08-tooling/sen0401_page_test_v9_35_0.py", "the page test as committed; do not edit it"),
         ("Page test 9.34.0", "08-tooling/sen0401_page_test_v9_34_0.py", "the page test as committed; do not edit it"),
         ("Page template", "08-tooling/course_page_template_v9_51_0.html", "template 9.51.0, the one pages 1 to 7, 9 and 13 use; the markers are 'const LBLRE=LBL.map' and 'function edVars()'"),
         ("Page builder", "08-tooling/sen0401_page_build_v4_14_0.py", "the newest page builder; read how pages 9.70.0 to 9.76.0 were built in the precedent commits below"),
         ("Page data config", "08-tooling/course_page_config_v2_16_0.json", "the newest page configuration"),
         ("Stage 4 ABox builder", "08-tooling/sen0401_page_abox_build_v2_1_0.py", "builds the Stage 4 page ABox from the newest page; a new file, ABox version = page version"),
         ("Deck match check", "08-tooling/pages_deck_match_verify_v1_0_0.py", "0 'not carried' is required"),
         ("Page link check", "08-tooling/pages_link_verify_v1_0_0.py", "run for the page as the precedent commits did"),
         ("Chapter 8 inputs maker (read first)", "08-tooling/ch08-page/inputs_make_v1_0_0.py", "the chapter 13 counterpart is 08-tooling/ch13-page/inputs_make_v1_1_0.py; a new version is a new file")]
PRECEDENT_PAGE = [("ec0bccb", "chapter 5 page 9.74.0 on template 9.51.0"), ("886a611", "chapter 1 page 9.70.0"), ("175793e", "chapter 6 page 9.75.0"), ("58e9dad", "chapter 7 page 9.76.0"), ("5533071", "chapter 13 page 9.69.0 (research 1.0.2)"), ("47e631f", "chapter 13 Stage 4 page ABox")]
PRECEDENT_C8 = [("4388676", "chapter 13 research v1.0.2: sixteen worked examples with changeable whole numbers (the precedent for chapter 8)"), ("1b0b5b5", "chapter 13 deck v1.2.0 from that research: the executed examples attached to slides. Chapter 13 changed its deck here; if chapter 8 needs the same, STOP and report what and why before you change a deck"), ("5533071", "chapter 13 page rebuilt from it"), ("47e631f", "chapter 13 Stage 4 page ABox")]
RULES = """- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The builder session writes it; it records your start and runs the Verify task through the evidence bridge after you report.
- A committed file is never edited: every output is a new file with a new version number.
- No gate, test or threshold is changed (Stage 3.F, the Stage 4 gates, the chapter checks, the page tests 9.34.0 and 9.35.0, the deck match check); no citation or claim is removed only to make a check pass.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN. NOT_MEASURED and CANNOT_RUN are not passes. A page test with a TEST release key proves page logic only.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a test or a gate; the deck would have to change (state exactly what and why); a check fails and you cannot fix it by building the page or research again; or anything in this brief contradicts the repository.
- Commit your work to main with a clear message (no force push; pull --rebase before push). Do not wait for or ask for approvals nobody can give: tell the coordinator the exact command.
- If a container restart interrupts you, the repository (committed and pushed work) is the only record: commit each verified step at once.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran (the Stage 4 runner for the chapter, the chapter checks, the page tests, the deck match check, the template markers); say what failed, if anything."""


def text(g, s, p):
    return " ".join(str(o) for o in g.objects(s, p))


def run(*a):
    return subprocess.run(a, cwd=REPO, capture_output=True, text=True).stdout.strip()


def main():
    out = os.path.join(REPO, sys.argv[1] if len(sys.argv) > 1 else "08-tooling/briefs/iter13"); os.makedirs(out, exist_ok=True)
    src = M.newest(); g = rdflib.Graph(); g.parse(src, format="turtle"); ver = os.path.basename(src)
    scope = E.Scope3
    excl = [x for x in g.objects(scope, B.hasScopeExclusion)]
    index = ["# Executor briefs of iteration 13 (generated from %s)\n" % ver, "| Task | Executor session | Can start |", "|---|---|---|"]
    for tid, sess in SESSIONS.items():
        t = E[tid]
        assert (t, None, None) in g, tid
        note = text(g, t, B.hasAuditNote); title = text(g, t, rdflib.RDFS.label)
        story = next(s for s in g.subjects(B.decomposesInto, t) if (s, rdflib.RDF.type, B.Story) in g)
        crit = re.findall(r"ex:(AC\w+)", note)[0]; c = E[crit]
        deps = [str(x).split("#")[1] for x in g.objects(t, B.dependsOn)]
        state = str(g.value(t, B.hasState)).split("#")[1]
        spec = E.Spec3T_C8 if "Ch08Ex" in tid else E.Spec3T_T
        L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state in the register: %s)." % (ver, tid, state),
             "Executor session name: **%s**. The register's note on 'work begun' for this task names this session." % sess, "",
             "## Rules of an executor", RULES, ""]
        if tid in BLOCKED:
            L += ["## Do not start until", "Task %s is Done (the builder session will tell the coordinator). This page needs the chapter 8 examples first." % BLOCKED[tid], ""]
        L += ["## The task", "**%s**" % title, "", note, "", "Depends on: %s" % (", ".join(deps) or "nothing"), "",
              "## The story it belongs to", "**%s**" % text(g, story, B.hasTitle), "", "As a %s I want %s so that %s." % (text(g, story, B.asRole), text(g, story, B.wantsCapability), text(g, story, B.soThat)), "",
              "## The criterion it satisfies (%s)" % crit, "**%s**" % text(g, c, rdflib.RDFS.label), "", text(g, c, B.hasGherkinText), "", "Satisfied by: %s" % text(g, c, B.satisfiedByArtifact), "",
              "## The written standard (%s)" % str(spec).split("#")[1], text(g, spec, B.hasSpecificationText), "", "## What the scope excludes"]
        for x in excl:
            L += ["- **%s**: %s" % (text(g, x, rdflib.RDFS.label), text(g, x, B.excludesConcern))]
        L += ["", "## Tools and gates, by version"]
        for name, path, how in TOOLS:
            L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(REPO, path)) else " (**not found at this path: search for the committed file of that name before you start**)", how))
        L += ["- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0 (Ontologies checkout); the chapter checks read the PINNED v1.6.0 (/home/claude/eco_pin/rdodi-ecosystem). Both must pass; they differ (chapter 5 passed the pinned one and failed the current one on '2026a' source labels, which a standalone four-digit year resolves)."]
        L += ["", "## Precedents in git (read them first)"]
        for sha, what in (PRECEDENT_C8 if "Ch08Ex" in tid else PRECEDENT_PAGE):
            L.append("- `%s` %s%s" % (sha, what, "" if run("git", "cat-file", "-t", sha) == "commit" else " (**commit not found**)"))
        L += ["- `08-tooling/page_jobs_status.md` and `08-tooling/stage4_status.md` describe how the pages were built and checked.", "",
              "## Facts measured on 2026-10-21 (coordinator)", "Pages 8, 10, 11, 12 and 14 lack the template markers; page 8 fails page test 9.34.0 (113 pass, 1 fail, then a crash: no chapter 8 example has a number in its code); the pages' content matches the decks; their test counts do not change on template 9.51.0 (commit 0f7d21f).", ""]
        open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write("\n".join(L))
        index.append("| %s | %s | %s |" % (tid, sess, "no, after %s" % BLOCKED[tid] if tid in BLOCKED else "yes"))
    open(os.path.join(out, "INDEX.md"), "w", encoding="utf-8").write("\n".join(index) + "\n")
    print(out, len(SESSIONS), "briefs from", ver)


main()
