#!/usr/bin/env python3
"""sen0401_lineage_fix897 v1_0_0 - one audit note on TK_Exam_Items5M_Build with the control results of Items5A, 5B, 5C and the merge decisions taken from the rules (read from 08-tooling/briefs/iter62/ADDENDUM_5M.txt); nothing is edited."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
note = open(os.path.join(M.REPO, "08-tooling/briefs/iter62/ADDENDUM_5M.txt"), encoding="utf-8").read().strip()
x = "TK_Exam_Items5M_Build"; i, j = T.blk(t, x); b = t[i:j].rstrip(); assert b.endswith(" ."), x
t = t[:i] + b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(note) + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Items5M: control results of 5A, 5B, 5C and the merge decisions added as an audit note.")))
