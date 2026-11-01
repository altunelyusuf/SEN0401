#!/usr/bin/env python3
"""sen0401_lineage_refine_wave16 v1_0_0 - one new register version: an audit note on TK_Exam_Items4_Build for the owner's six added points (21:23) and the coverage control. Usage: no arguments."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
NOTE = ("Added input 2026-11-01 21:49 Istanbul (owner, relayed by the coordinator): ten more content points G to P (coinbase amounts, the first spend and the pizza, hash capacity and pools, choice by fee per size, why digital money failed, old currencies, lost keys, input and output scripts, who confirms and fake transactions, the 51 percent attack), recorded as `08-tooling/exam/sen0401_exam_owner_topics_v1_2_0.json` (v1_0_0 and v1_1_0 unchanged). The owner's answer on the gaps: analyse the current exam with his emphasised concepts at the end; no item is dropped yet and Papers4 does not start. The analysis (second edition, `08-tooling/exam/analysis_v1_3_0/sen0401_exam_analysis_v1_3_0_b.md` and .docx, commit cedbf9e) gives each point as covered, partial or GAP with the chapter slot that could host it. Any later change is a new items version.")
i, j = T.blk(t, "TK_Exam_Items4_Verify"); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(NOTE)
t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner's six added exam points (A-F) recorded on the items v1.3.0 Verify task; coverage control stated.")))
