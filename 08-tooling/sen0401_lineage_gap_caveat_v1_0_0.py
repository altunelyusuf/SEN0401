#!/usr/bin/env python3
"""sen0401_lineage_gap_caveat v1_0_0 - ONE new register version (notes only): the disclosure of the pinned-versus-current validator difference on ST_Gap_Stage3F and ST_Gap_Stage4 (audit notes), and the corrected
caveat on the ClosureReport CR_SEN0401 (rdfs:comment; it supersedes the caveat of v0.121, which said the register holds no task for these gaps). Measured by the Stage 4 runner v1_1_0 inside the evidence bridge run of
2026-10-20T23:5x to 2026-10-21T01:16 UTC. The report states; it claims no pass for NOT_MEASURED or CANNOT_RUN gates. closureCommittedAt, the Mission outcome and Lineage3 Achieved are not touched.
Usage: sen0401_lineage_gap_caveat_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

VAL = ("Two validators are in play and they are not the same. The Stage 4 runner (08-tooling/sen0401_stage4_gates_v1_1_0.py) reads the CURRENT RDODI pipeline validator (v1.13.0, Ontologies checkout); the lineage chapter check "
       "(08-tooling/sen0401_lineage_chapter_check_v1_3_0.py) reads the PINNED validator (v1.6.0, eco_pin). A chapter can therefore pass the chapter check and fail the runner: chapter 5 passes Research/Ch05 under v1.6.0 and fails Stage 3.F under v1.13.0 (15 dangling citations).")
S3F = ("Disclosure, %s. " + VAL + " Under the current validator, in the run recorded in v0.134, chapter 1 and the numbers page now pass Stage 3.F (30 and 6 citations verified); only chapter 5 fails it, and its repair is the open criterion AC3G_3F_Ch05 (TK_Gap3F_Ch05_Build in progress, TK_Gap3F_Ch05_Verify proposed). "
       "The story stays open until AC3G_3F_Ch05 is satisfied. The Research chapter check of chapter 1 could not complete (it exits with an error, because the check has no verify script for chapter 1; its evidence is unverified and is not claimed); the numbers page has no chapter check.")
S4 = ("Disclosure, %s. " + VAL + " Stage 4 per unit under the current validator, from the runner run in v0.134: chapters 1, 2, 3, 4, 6, 7 and the numbers page pass Stage4.A, B, cov, sub and src, and their Verify tasks are Done. "
      "Chapter 5: the runner exits non-zero because Stage 3.F fails (15 dangling citations), although its Stage 4 gates pass; TK_GapS4_Ch05_Verify therefore stays open and is not claimed. "
      "Stage4.L, Cross.C, Stage1.C, Stage1.E and Stage3.E are NOT_MEASURED and Cross.B is CANNOT_RUN in every unit: none is claimed as a pass. The page tests ran with a TEST release key and prove page logic only. "
      "Timing noise on the page checks of chapters 3 and 7 occurred in earlier runs; in the bridge run of v0.134 they passed. The story stays open until the chapter 5 criterion is satisfied.")
CAV = ("Corrected caveat, %s (it supersedes the caveat of v0.121, which said the register holds no task for these gaps: it now holds them, as stories ST_Gap_Stage3F and ST_Gap_Stage4 with Build and Verify tasks). "
       "State at v0.134 by the Stage 4 runner v1_1_0 under the CURRENT validator (v1.13.0): Stage 3.F passes for chapters 1, 2, 3, 4, 6, 7 and the numbers page (chapter 1 and numbers were repaired by the gap tasks) and FAILS for chapter 5 only (15 dangling citations; the repair is in progress, TK_Gap3F_Ch05_Build). "
       "Stage 4 (A, B, cov, sub, src) passes for chapters 1 to 7 and the numbers page, with Verify tasks Done except TK_GapS4_Ch05_Verify, which stays open. The lineage chapter checks read the PINNED validator v1.6.0, under which chapter 5 passes: the two validators differ and both are disclosed. "
       "Stage4.L, Cross.C, Stage1.C, Stage1.E and Stage3.E are NOT_MEASURED and Cross.B is CANNOT_RUN; none is a pass. The page tests used a TEST release key (page logic only). The Research chapter check of chapter 1 could not complete (no verify script for chapter 1) and the numbers page has no chapter check. "
       "Timing noise on the page checks of chapters 3 and 7 occurred in earlier runs; they passed in the bridge run of v0.134. Neither the Mission outcome, nor closureCommittedAt, nor Lineage3 Achieved is touched: they wait for the chapter 5 criterion and the owner.")


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    d = M.now()[:10]
    t += '\nex:ST_Gap_Stage3F backlog:hasAuditNote "%s"@en .\n' % M.esc(S3F % d)
    t += 'ex:ST_Gap_Stage4 backlog:hasAuditNote "%s"@en .\n' % M.esc(S4 % d)
    t += 'ex:CR_SEN0401 rdfs:comment "%s"@en .\n' % M.esc(CAV % d)
    out = M.write_new(src, t, nxt, cur, "Disclosure of the pinned (v1.6.0) versus current (v1.13.0) validator difference on the two gap stories and a corrected caveat on the ClosureReport. Notes only.")
    print(os.path.basename(out))


main()
