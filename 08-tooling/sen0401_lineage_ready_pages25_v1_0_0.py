#!/usr/bin/env python3
"""sen0401_lineage_ready_pages25 v1_0_0 - makes the page stories and Build tasks of chapters 5 to 8 (Iter_25, already open since ex:PC3_Iter_25) Ready by refinement events, after the template 9.52.4 was controlled Done. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for n in "5678":
    for x in ("ST_Ch0%s_Page_R24" % n, "TK_Ch0%s_Page_Build_R24" % n):
        i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
        t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
        L.append('ex:Refine25P_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_25 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent after the template 9.52.4 was controlled Done (ex:ST_Template_9524): its dependency is closed; the brief is generated from the register; startable. Order: chapter 5, 6, 7, 8, one build at a time (equal scores, chapter order).")))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Page stories and Build tasks of chapters 5 to 8 made Ready after the template 9.52.4 was controlled Done.")))
