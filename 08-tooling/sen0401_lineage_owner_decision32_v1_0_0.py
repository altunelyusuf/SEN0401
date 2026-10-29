#!/usr/bin/env python3
"""sen0401_lineage_owner_decision32 v1_0_0 - records the owner's answers of 2026-10-30 on the number of items (owner question Q2, in part) and on the make-up reuse of midterm items (Q7). Comments on the change request; no stage content."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_gap_revision_v1_0_0 as G
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
a = ("OWNER DECISION of 2026-10-30, relayed by the coordinator (owner question Q2, the count only): one SEN0401 midterm has 24 questions (a 60-minute sitting: fewer, longer synthesis and code-trace items, more thinking time per question); the make-up has the same count. "
     "THE CHAPTER WEIGHTS ARE NOT DECIDED: the working default is equal weight per chapter (4 items for each of chapters 1 to 6), which is the engine default and needs no evidence; it is not the only grounded choice: the weight could follow the number of critical points per chapter (12, 14, 19, 13, 20, 23 in the list of 2026-10-29), which gives 3, 3, 5, 3, 5, 5 items; the register holds no evidence of teaching hours per chapter. The owner decides if the default should change.")
b = ("OWNER DECISION of 2026-10-30, relayed by the coordinator (owner question Q7): the make-up NEVER reuses a midterm item. The engine's no-repeat rule (EN05) stays and stays a REFUSAL, not a warning. "
     "Note for the papers task: the engine of commit e662771 has an option --allow-repeat which the owner's decision makes unused; it is not to be used, and a later engine version may drop it as a new file.")
t += "\nex:CR3_ExamMission rdfs:comment %s@en .\nex:CR3_ExamMission rdfs:comment %s@en .\n" % (G.lit(a), G.lit(b))
for tk in ("TK_Exam_Items_Build", "TK_Exam_Papers_Build"):
    t += "ex:%s backlog:hasAuditNote %s .\n" % (tk, G.lit("Note 2026-10-30: owner decisions: 24 questions per paper, the make-up the same count, equal chapter weight as the working default (not yet decided), and the make-up never reuses a midterm item (EN05 stays a refusal; do not use --allow-repeat). See ex:CR3_ExamMission."))
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner decisions of 2026-10-30 recorded: 24 questions per paper, make-up the same count, equal chapter weight as working default; the make-up never reuses a midterm item (refusal). Comments and notes; no stage content.")))
