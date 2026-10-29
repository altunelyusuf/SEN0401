#!/usr/bin/env python3
"""sen0401_lineage_brief_urgent v1_0_0 - brief of an executor for an URGENT task, a rendering of the register at the version it names (task note, criterion, rules of an executor taken from sen0401_lineage_brief_exam v1_3_0, the tools by version). Usage: brief_urgent.py TASK[,TASK] OUTDIR"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_brief_exam_v1_3_0 as BX
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
TOOLS = {"TK_Urgent_Ch06_Deck_Build": [
  ("Deck measure script (interim gate)", "08-tooling/sen0401_deck_teach_measure_v1_0_0.py", "python3 ... --json FILE: prompts, indentation, one-line compounds, lambda, label shapes, notes words per deck"),
  ("Existing chapter 6 deck builder, plan and library", "08-tooling/ch06-deck/ and 08-tooling/sen0401_ch06_tx_lib_v1_1_0.py", "read the builder and plan of v2_2_0 first; the research set is 03-materials/ch06/rdodi/"),
  ("Deck engine", "08-tooling/sen0401_deck_engine_v1_2_0.py", "the engine the decks are built with"),
  ("Checks that exist", "08-tooling/sen0401_deck_check_v1_1_0.py, sen0401_deck_standard_check_v1_2_0.py, sen0401_deck_arc_check_v1_3_0.py, deck_overlap_check_v1_0_0.py", "they read prompts (deck check, standard check): report NOT_MEASURED plainly on a prompt-free deck, never edit them"),
  ("The page of chapter 6 (for the match of code and concepts)", "03-materials/ch06/page/sen0401_ch06_page_v9_84_0.html", "its Learn > Chapter code tab and its concept visualisations are the model for the slides"),
  ("Code findings measure", "08-tooling/sen0401_code_findings_measure_v1_0_0.py", "slide code against page strings")],
 "TK_Urgent_Ch06_Page_Build": [
  ("Page template 9.52.5 and builders", "08-tooling/course_page_template_v9_52_5.html (or the folder where it lives), 08-tooling/sen0401_page_build_v4_*.py, sen0401_page_data_v2_*.py (newest)", "make 9.52.6 and new builder versions as new files"),
  ("Page tests", "08-tooling/sen0401_page_test_v9_34_2.py, v9_35_2.py, v9_37_0.py and the runner sen0401_lineage_page_test_run_v1_2_0.py", "serially under flock /tmp/page_test.lock; PAGE_TEST names the test"),
  ("The chapter 6 page (the old one)", "03-materials/ch06/page/sen0401_ch06_page_v9_84_0.html", "not edited"),
  ("Code findings measure", "08-tooling/sen0401_code_findings_measure_v1_0_0.py", "run it on your page: 0 unmatched, 0 wrappers"),
  ("The new deck code (from the deck executor)", "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_3_0.pptx", "git pull until the deck executor's first commit holds it")]}
def main():
    tasks = sys.argv[1].split(","); out = os.path.join(M.REPO, sys.argv[2]); os.makedirs(out, exist_ok=True)
    src = M.newest(); ver = os.path.basename(src); g = rdflib.Graph(); g.parse(src, format="turtle")
    tx = lambda s, p: str(g.value(s, p) or "")
    for tid in tasks:
        t = E[tid]; story = next(s for s in g.subjects(B.decomposesInto, t)); crit = next(g.objects(story, B.hasAcceptanceCriterion))
        sess = re.search(r"Planned session (SEN0401-[A-Za-z0-9-]+)", tx(t, B.hasAuditNote)).group(1)
        L = ["# Brief for the executor session %s" % sess, "", "Generated from the register %s. Task %s (state: %s). Urgent interruption ex:Urgent_1 is open (the lineage is paused for this work)." % (ver, tid, str(g.value(t, B.hasState)).split("#")[-1]),
             "Executor session name: **%s**. Start it with a real `date -u` and tell the coordinator the instant; the builder session records it." % sess, "",
             "## Why this work exists (the owner's urgent word)", "Friday 2026-10-30 02:28 Istanbul, relayed by the coordinator: tomorrow the owner teaches SEN0401 chapter 6 Transactions at 09:00 Istanbul. The chapter 6 slides and the interactive page must be finished before 06:00 Istanbul (03:00Z) so that he has at least one hour to review. Other work stops. Two executors work in parallel, the deck executor and the page executor, on different files. Report by 02:30Z at the latest; a progress note after your first commit.", "",
             "## Rules of an executor", BX.RULES, "- Disk: about 1.2 GB free; stop under 0.9 GB. The deck executor builds with no browser; the page executor takes the lock for every browser run.", "",
             "## The task", "**%s**" % tx(t, rdflib.RDFS.label), "", tx(t, B.hasAuditNote), "",
             "## The criterion it satisfies (%s)" % str(crit).split("#")[-1], "**%s**" % tx(crit, rdflib.RDFS.label), "", tx(crit, B.hasGherkinText), "", "## Tools and gates, by version"]
        for name, path, how in TOOLS[tid]:
            p0 = path.split(" and ")[0].split(",")[0].split(" ")[0]
            L.append("- %s: `%s`%s - %s" % (name, path, "" if os.path.exists(os.path.join(M.REPO, p0)) else " (not found at this exact path: search for the committed file of that name)", how))
        L += ["", "## Precedents in git", "- `23e155f` an executor's evidence logs for a page: the commit pattern to follow", "- `e662771` and `4557301` executor commits that were controlled Done"]
        body = re.sub(r"SEN0401-I\d+-[a-z0-9-]+", lambda m: m.group(0) if m.group(0) == sess else "another executor session", "\n".join(L))
        open(os.path.join(out, "BRIEF_%s.md" % tid), "w", encoding="utf-8").write(body); print(sess, os.path.join(out, "BRIEF_%s.md" % tid))
main()
