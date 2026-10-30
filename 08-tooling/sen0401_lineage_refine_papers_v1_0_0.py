#!/usr/bin/env python3
"""sen0401_lineage_refine_papers v1_0_0 - refinement of ST_Exam_Papers and TK_Exam_Papers_Build to Ready in the already open Iter_48 (their dependency, the Items task, became Done in v0.709.0). Missed by the lineage agent before the executor was launched; recorded at the real instant of this step, which is after the launch. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Exam_Papers", "TK_Exam_Papers_Build"):
    i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
    t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    L.append('ex:Refine48b_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_48 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent in the open Iter_48 after the Items task was Done on the control (v0.709.0). Disclosed: this was missed before the executor was launched (launch 2026-10-30T08:55:39Z); the refinement is recorded at the real instant of this step, after the launch, and the work begun follows it.")))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Exam_Papers and TK_Exam_Papers_Build refined to Ready in Iter_48 (missed before the launch of the executor, disclosed)")))
