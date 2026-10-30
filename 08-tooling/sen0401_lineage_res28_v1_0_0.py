#!/usr/bin/env python3
"""sen0401_lineage_res28 v1_0_0 - after the control of the midterm items (v0.708.0): the not-started Papers task note carries the findings that bear on the paper (item order and page count, the cs_encode listing, the draft status until the owner confirms the items). Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
i, j = T.blk(t, "TK_Exam_Grading_Build"); b = t[i:j]; assert "startedAt" not in b
ADD = (" WHAT EXISTS FOR THIS TASK (control of the midterm paper, 2026-10-30, register v0.715.0): the midterm paper in two orders in 08-tooling/exam/papers_midterm_v1/ (sen0401_exam_midterm_chapter_v1_0_0 and sen0401_exam_midterm_type_v1_0_0, each with _key.json (the answer key of the grader: choice letters, matching and ordering letters per row, fill-in codes, numbers with unit and tolerance, trace results), _sheet_layout.json (the layout the reader needs), _sheet.pdf, _paper.ttl); the reader v1.1.0 (08-tooling/exam/sen0401_exam_answersheet_v1_1_0.py) read 40 synthetic sheets of each of these layouts in my control with no silent wrong answer, no missed row and no unflagged empty read, and held 5.7 percent of rows (chapter order, 2 sheet pages) and 16.3 percent (grouped order, 1 sheet page) for review. The paper is a DRAFT until the owner confirms the items and the order: build the grading on the key and layout files by their format, for either order, and never on a position that only one order has. Synthetic sheets only; no real student data; the reader was never run on a real scan: say so in your report.")
m = re.search(r'(hasAuditNote ")((?:[^"\\]|\\.)*)"', b); nb = b[:m.end(2)] + ADD.replace('"', '\\"') + b[m.end(2):]
t = t[:i] + nb + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Grading task note (not started) names the midterm paper files and the reader results it builds on")))
