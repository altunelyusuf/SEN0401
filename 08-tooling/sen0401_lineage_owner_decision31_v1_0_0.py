#!/usr/bin/env python3
"""sen0401_lineage_owner_decision31 v1_0_0 - records the owner's answer of 2026-10-30 on the answer mode (owner questions Q8 and Q16) as comments on the change requests and notes on the tasks that count pages. No stage content."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_gap_revision_v1_0_0 as G
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
d = ("OWNER DECISION of 2026-10-30, relayed by the coordinator (owner questions Q8 and Q16): the answer mode is the SEPARATE BUBBLE GRID, one extra A4 page per student, machine-readable. "
     "Consequences: the answer sheet, its reader and the repair of the reader (ex:ST_Exam_AnswerMethods_Repair) stay in scope; the page cost of one more A4 page per student must be counted in every page count of the papers (the paper-rules page counts and any page limit include the sheet); circle-on-item is not the mode.")
t += "\nex:CR3_ExamMission rdfs:comment %s@en .\nex:CR3_AnswerRepair rdfs:comment %s@en .\n" % (G.lit(d), G.lit(d))
for tk in ("TK_Exam_Papers_Build", "TK_Exam_Grading_Build", "TK_Exam_AnswerMethods_Repair_Build"):
    t += "ex:%s backlog:hasAuditNote %s .\n" % (tk, G.lit("Note 2026-10-30: the owner decided the answer mode is the separate bubble grid (one extra A4 page per student, machine-readable). The pages of a paper are counted with that sheet; the reader and its repair stay in scope. See ex:CR3_ExamMission."))
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner decision of 2026-10-30 recorded: the answer mode is the separate bubble grid (one extra A4 page per student); the answer sheet, its reader and the repair stay in scope; page counts include the sheet. Comments and notes; no stage content.")))
