#!/usr/bin/env python3
"""sen0401_lineage_res27 v1_0_0 - after the control of the midterm items (v0.708.0): the not-started Papers task note carries the findings that bear on the paper (item order and page count, the cs_encode listing, the draft status until the owner confirms the items). Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
i, j = T.blk(t, "TK_Exam_Papers_Build"); b = t[i:j]; assert "startedAt" not in b
ADD = (" FINDINGS OF THE CONTROL OF THE ITEMS (2026-10-30, register v0.708.0) THAT BEAR ON THE PAPER: (1) the paper is built from the 23 items (24 units) of sen0401_exam_items_midterm_v1_0_0.json; it is a DRAFT until the owner confirms the items (the Bloom labels are the executor's own and the minimum of 6 items at Analyze or above is a default derived from the owner's 8 of 30): a change of an item is a new items version and a rebuilt paper, nothing is printed before he confirms. (2) PAGE COUNT: the items executor measured 7 pages in chapter order (5 content + 2 of answer sheet) and 1 answer-sheet page only if the items are grouped by type across chapters; the owner's goal is fewer printed pages, so build BOTH orders, report both page counts as printed, and take the grouped order as the proposal unless it breaks a rule; the owner rules on the order when he sees both. (3) The trace item mt1:i20 calls cs_encode, which its listing does not define: report how the paper shows it (a definition on the paper is a change of the item and needs a new items version, not an edit). (4) Ordering, matching and fill-in items print no stem (the engine renders a generic instruction): check that the paper reads clearly. (5) number and trace keys are capped at 5 characters.")
m = re.search(r'(hasAuditNote ")((?:[^"\\]|\\.)*)"', b); nb = b[:m.end(2)] + ADD.replace('"', '\\"') + b[m.end(2):]
t = t[:i] + nb + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Papers task note (not started) carries the findings of the control of the midterm items that bear on the paper")))
