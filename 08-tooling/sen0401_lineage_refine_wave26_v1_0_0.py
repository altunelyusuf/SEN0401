#!/usr/bin/env python3
"""sen0401_lineage_refine_wave26 v1_0_0 - one new register version: the exam move stories and Build task are made Ready (start gate READY first). Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Exam_V6_Read", "TK_Exam_V6_Read_Build", "ST_Exam_V6_Sheet", "TK_Exam_V6_Sheet_Build", "ST_Exam_V6_Items", "TK_Exam_V6_Items_Build", "ST_Exam_V6_Papers", "TK_Exam_V6_Papers_Build"):
    i, j = T.blk(t, x); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, x
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    if x.startswith("TK_"):
        open(src + ".gate.tmp", "w").write(t); r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", x], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, x + " is not READY: " + r.stdout[-300:]
    L.append('ex:RefineW26_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_54 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent at %s UTC: the owner ruled one form of the midterm on 2026-11-02 09:44 and the recorded coverage gaps are to be filled (ex:CR3_ExamOneForm); the inputs (items v1.3.0, structure v1.0.0, owner topics v1_0_0 to v1_2_0, the analysis, the papers v3 tools) are committed; the start gate says READY; startable (the merge starts after the three parts, Papers5 after the merge). The brief is generated from the register." % now)))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Exam midterm v6: stories and Build task made Ready.")))
