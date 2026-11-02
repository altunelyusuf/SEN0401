#!/usr/bin/env python3
"""sen0401_lineage_fix910 v1_0_0 - one audit note on TK_Exam_Items5M_Build and on TK_Exam_Papers5_Build: where the exam artefacts are written after the owner decision of 2026-11-02 10:27 (read from 08-tooling/briefs/iter62/ADDENDUM_P5.txt); nothing is edited."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
note = open(os.path.join(M.REPO, "08-tooling/briefs/iter62/ADDENDUM_P5.txt"), encoding="utf-8").read().strip()
for x in ("TK_Exam_Papers5_Build",):
    i, j = T.blk(t, x); b = t[i:j].rstrip(); assert b.endswith(" ."), x
    t = t[:i] + b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(note) + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Papers5: inputs in CME, what to build, the real page count to measure and the disclosures after the control of the merged items.")))
