#!/usr/bin/env python3
"""sen0401_lineage_ready v1_1_0 (gate path moved to backlog_execution_ready_v1_6_0, a new file over v1_0_0) - makes named Proposed stories and tasks of an iteration that is ALREADY open Ready, by refinement events, after the start gate (backlog_execution_ready_v1_4_0) says READY for each task
(used when a prerequisite story is Done, e.g. ST_Deck12_Revise after the chapter 12 research control). Same refinement pattern as sen0401_lineage_open_iter. Usage: sen0401_lineage_ready_v1_0_0.py ITER ITEM,ITEM..   (one new register version)"""
__version__ = "1.1.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; IT = sys.argv[1]; ITEMS = sys.argv[2].split(",")
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
assert ("ex:PC3_%s a " % IT) in t, "iteration is not open"
for x in ITEMS:
    i, j = T.blk(t, x); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, x
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    if x.startswith("TK_"):
        open(src + ".gate.tmp", "w").write(t); r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", x], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, x + " is not READY: " + r.stdout[-300:]
    L.append('ex:RefineR_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, IT, lit("Refined by the lineage agent at %s UTC: the prerequisite is Done on bridge-verified evidence (the start gate says READY), the brief is generated from the register; startable." % now)))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "%s: %s made Ready by refinement after the start gate said READY." % (IT, ", ".join(ITEMS)))))
