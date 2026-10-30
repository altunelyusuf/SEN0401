#!/usr/bin/env python3
"""sen0401_lineage_res29 v1_0_0 - CORRECTION of the record of two earlier controls (appended, nothing edited): the reader repair control (AC3E_Exam_AnswerMethods_Repair, TK_Exam_AnswerMethods_Repair_Build) and the paper control (AC3E_Exam_Papers, TK_Exam_Papers_Build). Reported by the grading executor, reproduced by the lineage agent. Usage: no arguments."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now()
FACT = ("CORRECTION appended %s UTC (v%s), nothing above is edited: the grading executor (commit a575006) reported, and the lineage agent REPRODUCED with its own script 08-tooling/exam/sen0401_exam_reader_gap_control_v1_0_0.py (logs 08-tooling/verify/iter54/ctl/ctl_reader_gap_v1_1_0_reproduction.log), that the COMMITTED reader v1.1.0 ALONE, on sheets of the midterm paper's CHAPTER-ORDER layout (choice rows interleaved with other kinds), lets a skipped-row shift cross a gap without a flag: seeds 41000-41039: 17 rows accepted that should have been held (7 of 40 sheets); seeds 52000-52199: 91 rows on 28 of 200 sheets; the grouped-by-type layout gave 0 on both blocks and on 77000-77039. The earlier control statements 'no silent wrong answer, no missed row' of the reader repair (measured on the reader's own default layout, 600 sheets) and of the paper control (40 sheets of the paper's own layouts, seeds 77000-77039, only 8 sheets with a shift) are therefore true only for what was measured: the default layout, and a sample too small to meet the gap on the chapter layout. They do not hold for the reader on the chapter-order layout. The control script of the paper also had a counter name it did not match (empty_not_flagged); it did not hide the gap (the counter 'missed' was matched and was zero on that sample). The grading tool v1.0.0 adds two screens that hold the blocks across the gap and gave zero misses on my held-out block 63000-63099 and on 41000; the reader itself needs a new version (the repair story registered in the same version family) and the two orders need distinct form codes (both print 10100).")
L = []
for crit in ("AC3E_Exam_AnswerMethods_Repair", "AC3E_Exam_Papers"):
    assert ("ex:%s a " % crit) in t, crit
    L.append("\nex:%s backlog:hasAuditNote %s .\n" % (crit, lit(FACT % (now, nxt))))
for tk in ("TK_Exam_AnswerMethods_Repair_Build", "TK_Exam_Papers_Build"):
    assert ("ex:%s a " % tk) in t, tk
    L.append("\nex:%s backlog:hasAuditNote %s .\n" % (tk, lit("CORRECTION appended %s UTC (v%s): see the correction on its criterion: the control of this task did not meet the reader gap on the chapter-order layout (reproduced later); its other results stand as measured." % (now, nxt))))
print(os.path.basename(M.write_new(src, X.set_status(t + "".join(L), "LS_InProgress"), nxt, cur, "Correction appended to the records of the reader repair control and the paper control: the reader v1.1.0 alone misses skipped-row shifts on the chapter-order layout (reproduced)")))
