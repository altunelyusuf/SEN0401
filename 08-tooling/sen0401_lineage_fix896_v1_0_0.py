#!/usr/bin/env python3
"""sen0401_lineage_fix896 v1_0_0 - correction note: the control114 record of 2026-11-02 named the executor sessions SEN0401-I65-items5a, I66-items5b, I67-items5c; the sessions named in the briefs are SEN0401-I62-items5a, -items5b, -items5c. One new audit note on each Build task; nothing is edited."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
for p, wrong in (("A", "I65"), ("B", "I66"), ("C", "I67")):
    x = "TK_Exam_Items5%s_Build" % p; i, j = T.blk(t, x); b = t[i:j].rstrip(); assert b.endswith(" ."), x
    note = "CORRECTION: the Done note above names the executor session SEN0401-%s-items5%s by a typing error of the control script; the session named in the brief of this task is SEN0401-I62-items5%s. The commit, the evidence and the result are unchanged." % (wrong, p.lower(), p.lower())
    t = t[:i] + b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(note) + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Correction of the executor session names in the Done notes of Items5A, 5B and 5C.")))
