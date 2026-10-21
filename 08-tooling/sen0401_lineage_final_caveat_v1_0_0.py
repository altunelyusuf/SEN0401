#!/usr/bin/env python3
"""sen0401_lineage_final_caveat v1_0_0 - ONE new register version, notes and labels only, before the owner is asked for the Mission act:
(1) a corrected caveat on the ClosureReport, from a fresh measurement of every unit (01-14 and numbers) by 08-tooling/sen0401_stage4_gates_v1_1_0.py (logs read from the directory given), which supersedes the caveat of v0.135
(that one still said chapter 5 fails Stage 3.F); (2) the label, measurement query and metric label of Obj3_Stage3FPass and the sprint goal of Iter_12 name chapter 5 (the third document), by a label edit in this new version
(a label is not in the stage digests, which are over subject IRIs; the pipeline verifier confirms) with a dated note. Usage: sen0401_lineage_final_caveat_v1_0_0.py LOGDIR"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

UNITS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "numbers"]


def gate(txt, g):
    m = re.search(r"^\[(\w+) *\] %s[^:]*:" % re.escape(g), txt, re.M)
    return m.group(1) if m else "absent"


def main():
    d = sys.argv[1]; src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    rows, nm, fails = [], set(), 0
    for u in UNITS:
        x = open(os.path.join(d, u + ".log"), encoding="utf-8").read()
        rows.append("%s: Stage3.F %s, Stage4.cov %s, Stage4.sub %s, Stage4.src %s" % ("numbers page" if u == "numbers" else "chapter " + u.lstrip("0"), gate(x, "Stage3.F"), gate(x, "Stage4.cov"), gate(x, "Stage4.sub"), gate(x, "Stage4.src")))
        fails += len(re.findall(r"^\[FAIL", x, re.M))
        nm |= set(re.findall(r"^\[(?:NOT_MEASURED|CANNOT_RUN) *\] ([A-Za-z0-9.]+)", x, re.M))
    day = M.now()[:10]
    cav = ("Corrected caveat, %s (it supersedes the caveats of v0.121 and v0.135; v0.135 still said that chapter 5 fails Stage 3.F, which the register no longer holds). Measured on this date, after research v1.1.1 of chapter 5 (commit 76d6083), with 08-tooling/sen0401_stage4_gates_v1_1_0.py "
           "for all fifteen units, RDODI's validator unchanged (the current one, v1.13.0), on main: every run exits 0 and reports %d failing gates. Per unit: %s. "
           "Chapter 5 failed Stage 3.F until 2026-10-21 (15 dangling citations, because the validator's resolver reads only a standalone four-digit year from a source label and the labels 'Lightning Labs, 2026a' and '2026b' carry none); the labels now state the retrieval date; no source was added, no citation or claim removed. "
           "Chapter 1 and the numbers page (Stage 3.F and Stage 4) and chapters 2 to 7 (Stage 4 page ABox) were repaired or built by the gap tasks of the third lineage; chapter 5 also by its Stage 3.F task; chapters 8 to 14 pass without a gap task. "
           "Not claimed: the gates %s are NOT_MEASURED or CANNOT_RUN in the units that report them (no concept inventory in the research data; no hybrid chains) and are not passes. "
           "The two validators differ: the Stage 4 runner reads the current validator (v1.13.0) and the lineage chapter checks read the pinned one (v1.6.0); both now pass for chapter 5. "
           "Items the evidence bridge could not verify and the register does not claim: the Research chapter check of chapter 1 (the check has no verify script for chapter 1; the Stage 1 to 3 gates of the runner pass) and the first bridge run of the Stage 4 runner for chapter 5 in v0.134 (it failed Stage 3.F then; the rerun of v0.136 verified). "
           "The numbers page has no chapter check. The page tests use a TEST release key and prove page logic only. Timing noise on the page checks of chapters 3 and 7 occurred in earlier runs. "
           "The other caveats of the summary stand unchanged. Neither the Mission outcome, nor closureCommittedAt, nor the achievement of the third lineage is recorded: they are the owner's.") % (day, fails, "; ".join(rows), ", ".join(sorted(nm)))
    assert "ex:CR_SEN0401 a backlog:ClosureReport" in t
    t += '\nex:CR_SEN0401 rdfs:comment "%s"@en .\n' % M.esc(cav)
    reps = [("(chapter 1, Bitcoin in numbers) whose Stage 3.F gate passes: from 0 to 3", "(chapters 1 and 5, Bitcoin in numbers) whose Stage 3.F gate passes: from 0 to 3"),
            ("Count of Stage 3 documents (chapter 1, Bitcoin in numbers)", "Count of Stage 3 documents (chapters 1 and 5, Bitcoin in numbers)"),
            ('rdfs:label "Stage 3 documents (chapter 1, Bitcoin in numbers) whose Stage 3.F gate passes"@en', 'rdfs:label "Stage 3 documents (chapters 1 and 5, Bitcoin in numbers) whose Stage 3.F gate passes"@en')]
    for a, b in reps:
        n = t.count(a); assert n >= 1, a
        # only the objective and metric blocks, not the historical change records
        for blkname in ("Obj3_Stage3FPass", "Met3_Stage3FPass"):
            i = t.index("\nex:%s a backlog:" % blkname) + 1; j = t.find("\nex:", i)
            t = t[:i] + t[i:j].replace(a, b) + t[j:]
    i = t.index("\nex:Iter_12 a backlog:Iteration") + 1; j = t.find("\nex:", i)
    g = "The Stage 3 documents of chapter 1 and Bitcoin in numbers pass Stage 3.F"
    assert g in t[i:j]
    t = t[:i] + t[i:j].replace(g, "The Stage 3 documents of chapters 1 and 5 and Bitcoin in numbers pass Stage 3.F") + t[j:]
    note = ("Label correction %s: chapter 5 became a third Stage 3 document of the Stage 3.F objective (the scope change of v0.132, target 2 to 3), but this label, the measurement query and the metric label, and the sprint goal of Iter_12, still named chapter 1 and the numbers page. "
            "They now name chapters 1 and 5 and the numbers page. A label edit in a new version was used, not a StageRevision: labels are not in the stage digests (subject IRIs only), so no digest moves; the pipeline verifier confirms it. The Stage 4 objective needs no change: chapters 1 to 7 and the numbers page are 8 units, from 0 to 8. "
            "The historical records (change request, impact assessment, scope and deliverable texts) keep the wording of the moment they were decided.") % day
    for n in ("Obj3_Stage3FPass", "Iter_12"):
        t += 'ex:%s backlog:hasAuditNote "%s" .\n' % (n, M.esc(note)) if n != "Iter_12" else 'ex:Iter_12 rdfs:comment "%s"@en .\n' % M.esc(note)
    out = M.write_new(src, t, nxt, cur, "Corrected ClosureReport caveat from a fresh measurement of all units, and the labels of the Stage 3.F objective and the sprint goal of Iter_12 name chapter 5. Notes and labels only.")
    print(os.path.basename(out))


main()
