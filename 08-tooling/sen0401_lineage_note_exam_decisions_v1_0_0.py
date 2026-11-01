#!/usr/bin/env python3
"""sen0401_lineage_note_exam_decisions v1_0_0 - appends (never edits) the two coordinator decisions of 2026-11-01 on the exam papers v3 to the Papers3 story and Build task. Usage: no arguments."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now()
note = ("DECISIONS ADDED %s (coordinator, from the owner's 13:04 wording '5th Question is 10 points and bonus'; stated as defaults, not as the owner's word on grading): (1) the short-explanation answer type is enabled for Question 5 only: it is hand-graded, the paper carries answer lines for it, the answer sheet does not read it; (2) partial credit for ordering and matching items is proportional per correct part (points_per_part). The task: cover page as page 1 (renderer v1.0.0, commit f60a817), the five questions of the structure v1_0_0 with items v1.2.0 (control: Done), Q5 answer lines, the answer sheet v3 (PDF, same block types so the reader v1.2.0 is unchanged), the key v3 (Word); page target 4 in total, else 6 with better readability; two forms by default. Open and marked as fill-ins on the cover: date and time, allowed materials, program outcome numbers." % now[:10])
L = "".join("ex:%s backlog:hasAuditNote %s .\n" % (k, C.lit(note)) for k in ("ST_Exam_Papers3", "TK_Exam_Papers3_Build"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + L, "LS_InProgress"), nxt, cur, "Decisions on the exam papers v3 recorded (appended): Q5 short explanation hand-graded, partial credit per correct part")))
