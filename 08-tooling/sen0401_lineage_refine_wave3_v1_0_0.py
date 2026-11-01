#!/usr/bin/env python3
"""sen0401_lineage_refine_wave3 v1_0_0 - one new register version: the Ch02 Teach story and Build task are made Ready (start gate READY first); the Teach Build tasks of chapters 1 to 4 get an appended audit note with the result-size requirement (owner rules: default text not small, code never wraps). Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Ch02_DeckTeach", "TK_Ch02_DeckTeach_Build"):
    i, j = T.blk(t, x); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, x
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    if x.startswith("TK_"):
        open(src + ".gate.tmp", "w").write(t); r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", x], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, x + " is not READY: " + r.stdout[-300:]
    L.append('ex:RefineW2_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_54 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent at %s UTC: the prerequisite deck (ST_Ch02_DeckCode, commit db1bf5c) is Done and controlled; the start gate says READY; startable. The brief is generated from the register." % now)))
NOTE = ("REQUIREMENT 2026-11-01 (coordinator, from the owner's standing rules 'code never wraps, widen the block' and 'default text must not be small'; found by the control of the Ch02 code deck: two result shapes, slides 9 and 30, 86 and 88 characters, are set at 7.5 pt): in the NEW deck of this task no result shape or code box is below 9 pt and none wraps; a long result is given the full content width of the slide (reflow the slide so that the result card sits full width under the code and the explanation); no expression is shortened and no gate is changed. Measure it for every result and code shape and report the smallest size and the count of wrapped lines as printed; any result below 9 pt is a defect.")
for tk in ("TK_Ch01_DeckTeach_Build", "TK_Ch02_DeckTeach_Build", "TK_Ch03_DeckTeach_Build", "TK_Ch04_DeckTeach_Build"):
    i, j = T.blk(t, tk); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(NOTE)
    t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Ch02 Teach story and Build task made Ready; result-size requirement appended to the Teach Build tasks of chapters 1 to 4.")))
