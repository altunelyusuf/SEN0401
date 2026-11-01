#!/usr/bin/env python3
"""sen0401_lineage_refine_wave15 v1_0_0 - one new register version: an audit note on TK_Exam_Items4_Build for the owner's six added points (21:23) and the coverage control. Usage: no arguments."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
NOTE = ("Added input 2026-11-01 21:23 Istanbul (owner, relayed by the coordinator, sent also directly to the executor SEN0401-I59-items4 begun 18:14:51Z): six content points A to F, recorded as `08-tooling/exam/sen0401_exam_owner_topics_v1_1_0.json` (v1_0_0 unchanged): A inputs versus outputs with and without a fee; B block reward by height, halving interval, legal versus illegal coinbase, toy numbers, halving ends at 1 satoshi, the names satoshi and bitcoin are given not recorded on chain; C all coins minted by miners, inputs trace to a coinbase; D each block links to the previous so miners restart; E hash trials unpredictable, value below a difficulty target, adjusted after a fixed number of blocks; F the 10-minute rule and soft forks. CONTROL (lineage agent): the coverage of ALL of T1-T9 and A-F is checked as an item key or GAP against the executor's topic map and against the items file itself; a GAP is reported, not hidden; the criterion is not edited (the points are inputs to elements (2) and (5)).")
i, j = T.blk(t, "TK_Exam_Items4_Build"); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(NOTE)
t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner's six added exam points (A-F) recorded on the items v1.3.0 Build task; coverage control stated.")))
