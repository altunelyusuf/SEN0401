#!/usr/bin/env python3
"""sen0401_lineage_closure_caveat v1_0_0 - ONE new register version that records, as a corrected caveat on the ClosureReport, the Stage 3.F and Stage 4 state of chapters 1 to 7 and the numbers page, measured on 2026-10-20 by
08-tooling/sen0401_stage4_gates_v1_1_0.py (RDODI's validator unchanged) and read against the tasks the register holds. The report states; it claims no pass. closureCommittedAt and the Mission outcome are not touched.
Usage: sen0401_lineage_closure_caveat_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

NOTE = ("Corrected caveat, %s (it replaces the seventh caveat of the summary, which named the gaps from the files and not from a run). Measured on this date with 08-tooling/sen0401_stage4_gates_v1_1_0.py, RDODI's validator unchanged, on main. "
 "Chapter 1: Stage3.F FAIL (1 external claim uncited), Stage4.cov FAIL (10 typed individuals lack label and content), Stage4.sub FAIL (116 individuals not substantive). "
 "Chapter 2: Stage3.F PASS, Stage4.cov FAIL (10), Stage4.sub FAIL (84). Chapter 3: Stage3.F PASS, Stage4.cov FAIL (10), Stage4.sub FAIL (108). Chapter 4: Stage3.F PASS, Stage4.cov FAIL (10), Stage4.sub FAIL (94). "
 "Numbers page: Stage3.F FAIL (19 dangling citations), Stage4.cov FAIL (10), Stage4.sub FAIL (58). "
 "Chapters 5, 6 and 7: the Stage 4 runner stops because there is no Stage 4 page ABox, so neither Stage 3.F nor Stage 4 was measured for them in this run; the build notes of 2026-10-14 name chapter 7 among those failing Stage3.F, and no run in this register shows it repaired. "
 "In every measured chapter Stage4.L, Cross.C, Stage3.E (concept coverage) are NOT_MEASURED and Cross.B is CANNOT_RUN; none is a pass. "
 "Read from the register: the tasks of this lineage on these gates are TK_Research_Ch02_Stage3F, TK_Research_Ch03_Stage3F and TK_Research_Ch04_Stage3F (Stage 3.F of chapters 2 to 4, Done) and the Stage 4 tasks of chapters 8 to 14 (TK_Research_Ch08_Stage4 to TK_Research_Ch14_Stage4, Done). "
 "The register holds no task, and no story, for Stage3.F of chapter 1, chapters 5 to 7 or the numbers page, nor for Stage4.cov or Stage4.sub of chapters 1 to 7 or the numbers page: these are not tasks of this lineage. "
 "None of the failures listed is claimed as passed; the connectedness agent's status file (branch connectedness-repair) lists the same failures as already on main.") 


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    assert "ex:CR_SEN0401 a backlog:ClosureReport" in t
    t += '\nex:CR_SEN0401 rdfs:comment "%s"@en .\n' % M.esc(NOTE % M.now()[:10])
    out = M.write_new(src, t, nxt, cur, "Corrected caveat on the ClosureReport: the measured Stage 3.F and Stage 4 state of chapters 1 to 7 and the numbers page, and which of them are tasks of this lineage. Notes only.")
    print(os.path.basename(out))


main()
