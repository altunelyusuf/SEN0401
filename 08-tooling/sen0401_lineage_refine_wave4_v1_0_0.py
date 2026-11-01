#!/usr/bin/env python3
"""sen0401_lineage_refine_wave4 v1_0_0 - one new register version: the Ch03 Teach story and Build task are made Ready (start gate READY first); the Ch03 Teach Build task gets the 9 pt and slide 24 requirement. Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Ch03_DeckTeach", "TK_Ch03_DeckTeach_Build"):
    i, j = T.blk(t, x); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, x
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    if x.startswith("TK_"):
        open(src + ".gate.tmp", "w").write(t); r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", x], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, x + " is not READY: " + r.stdout[-300:]
    L.append('ex:RefineW4_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_54 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent at %s UTC: the prerequisite deck (ST_Ch03_DeckCode, commit 713d27b) is Done and controlled; the start gate says READY; startable. The brief is generated from the register." % now)))
NOTE = ("REQUIREMENT 2026-11-01 (coordinator and the control of the Ch03 code deck v3_1_0): (1) in the NEW deck no result or code shape is below 9 pt and none wraps; a long result gets the full content width (reflow so that the result card sits full width under the code and the explanation); no expression is shortened and no gate is changed: today the results on slide 27 (8.5 pt) and slide 34 (8.0 pt) are below 9 pt and seven more are at 9 to 9.5 pt; (2) slide 24 has a blank gap under the code (the result card sits at 3.25 in while the code ends at 2.81 in): close it by moving the card up under the code; report the smallest size, the wrapped-line count and a before and after picture of slide 24 as printed.")
i, j = T.blk(t, "TK_Ch03_DeckTeach_Build"); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(NOTE)
t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Ch03 Teach story and Build task made Ready; 9 pt and slide 24 requirement appended to the Ch03 Teach Build task.")))
