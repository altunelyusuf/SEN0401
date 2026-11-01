#!/usr/bin/env python3
"""sen0401_lineage_refine_wave19 v1_0_0 - one new register version: the Build notes of TK_Exam_Items4_Build, TK_Exam_Papers4_Build and TK_Repair_Ch03_Page_Build were written by the route scripts res38 and res40 with ONE character of the brief text (the brief table held a parenthesised string, not a tuple, so the first character was taken); this version adds the full brief text to each as a new audit note (the earlier notes are not edited). Usage: no arguments."""
import importlib.util, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
def load(f):
    sp = importlib.util.spec_from_file_location(f[:-3], os.path.join(os.path.dirname(os.path.abspath(__file__)), f)); m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
r38 = load("sen0401_lineage_res38_v1_0_0.py"); r40 = load("sen0401_lineage_res40_v1_0_0.py")
FULL = {"TK_Exam_Items4_Build": r38.BRIEFS["items4"], "TK_Exam_Papers4_Build": r38.BRIEFS["papers4"], "TK_Repair_Ch03_Page_Build": r40.BRIEFS["ch03page"]}
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
for tid, body in FULL.items():
    assert isinstance(body, str) and len(body) > 500, tid
    i, j = T.blk(t, tid); b = t[i:j].rstrip(); assert b.endswith(" ."), tid
    note = "THE FULL BRIEF TEXT (correction, 2026-11-01: the first note of this task holds one character because of a fault in the route script; this note is the task as written): " + body
    b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % C.lit(note); t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, t, nxt, cur, "Full brief text added to the Build notes of the items v1.3.0, papers v4 and chapter 3 page repair tasks (the route scripts had written one character).")))
