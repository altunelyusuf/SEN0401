#!/usr/bin/env python3
"""sen0401_lineage_ready_pages v1_1_0 (over ready_pages25 v1_0_0, which did chapters 5 to 8) - makes the page stories and Build tasks of the named chapters Ready by refinement events: the iterations 26 to 28 are open (ceremonies PC3_Iter_26 to 28), the template 9.52.4 is Done and every dependency of the Build tasks (the deck Verify tasks, the chapter 1 research and verify script) is Done. Usage: sen0401_lineage_ready_pages_v1_1_0.py CH,CH,..  (e.g. 01,02,03); one new register version."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
IT = {"01": 26, "02": 26, "03": 26, "04": 26, "09": 27, "10": 27, "11": 27, "12": 28, "13": 28, "14": 28}
for n in sys.argv[1].split(","):
    for x in ("ST_Ch%s_Page_R24" % n, "TK_Ch%s_Page_Build_R24" % n):
        i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
        t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
        L.append('ex:Refine26P_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_%d ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, IT[n], lit("Refined by the lineage agent after the template 9.52.4 was controlled Done (ex:ST_Template_9524): its dependency is closed; the brief is generated from the register; startable. Order: chapter order, one build at a time (the owner: return to all chapters starting with chapter 1).")))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Page stories and Build tasks of chapters %s made Ready (iterations 26 to 28 open, every dependency Done)." % sys.argv[1])))
