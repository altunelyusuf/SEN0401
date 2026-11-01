#!/usr/bin/env python3
"""sen0401_lineage_refine_mid v1_0_0 - refinement of the two exam repair stories and their Build tasks (reader v1.2.0, paper v2 in Word) to Ready in the open Iter_54, before any executor is launched. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Ch06_DeckCode", "TK_Ch06_DeckCode_Build", "ST_Ch05_DeckCode", "TK_Ch05_DeckCode_Build"):
    i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
    t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    L.append('ex:Refine54b_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, re.search(r'memberOfContainer ex:(Iter_\d+)', bb).group(1), lit("Refined by the lineage agent in the open Iter_54 after the simplification of the midterm scope (v0.753.0) and the re-rank (tag 88); disclosed: recorded at the real instant of this step, after the launch of the sessions (2026-11-01T09:35:33Z and 09:35:34Z), because the coordinator's launch order arrived before the refinement; no dependency is open; startable.")))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Ch06_DeckCode, ST_Ch05_DeckCode and their Build tasks refined to Ready (disclosed: after the launch)")))
