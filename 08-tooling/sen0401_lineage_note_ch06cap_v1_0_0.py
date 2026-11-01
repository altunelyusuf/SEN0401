#!/usr/bin/env python3
"""sen0401_lineage_note_ch06cap v1_0_0 - appends (never edits) a requirement note to the Chapter 6 deck tasks: the coordinator's decision of 2026-11-01 after the honesty check v1_1_0 (commit a3f9719) refused deck v2_4_1: the 18 console slides get the caption 'What the run printed (python 3.14.6)' as Chapter 5 v3_7_0 has, in the next Chapter 6 deck version. Usage: no arguments."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now()
note = ("REQUIREMENT ADDED %s (coordinator's decision, relayed; the owner's 'bring to the Friday level' and consistency with Chapter 5): the honesty check v1_1_0 refuses the Chapter 6 deck v2_4_1 on its 18 console slides because they carry no run caption; the next Chapter 6 deck version puts the caption 'What the run printed (python 3.14.6)' on those 18 slides as Chapter 5 v3_7_0 does, changing nothing else, and the honesty check v1_1_0 must then accept it." % now[:10])
L = "".join("ex:%s backlog:hasAuditNote %s .\n" % (k, C.lit(note)) for k in ("TK_Ch06_DeckTeach_Build", "TK_Repair_Ch06_DeckLayout_Build"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + L, "LS_InProgress"), nxt, cur, "Requirement note on the Chapter 6 deck tasks: run caption on the 18 console slides (appended)")))
