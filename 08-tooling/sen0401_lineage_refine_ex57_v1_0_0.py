#!/usr/bin/env python3
"""sen0401_lineage_refine_ex57 v1_0_0 - refinement of the exam cover, items and honesty stories, the Ch05 Teach repair task and the Ch02-04 code stories to Ready in the open Iter_54, before any executor is launched. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Exam_Cover","TK_Exam_Cover_Build","ST_Exam_Items3","TK_Exam_Items3_Build","ST_Code_Honesty","TK_Code_Honesty_Build","TK_Repair_Ch05_DeckTeach_Build","ST_Ch02_DeckCode","TK_Ch02_DeckCode_Build","ST_Ch03_DeckCode","TK_Ch03_DeckCode_Build","ST_Ch04_DeckCode","TK_Ch04_DeckCode_Build"):
    i, j = T.blk(t, x); bb = t[i:j]; assert "backlog:hasState backlog:Proposed" in bb, x
    t = t[:i] + bb.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    L.append('ex:Refine54e_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:%s ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, re.search(r'memberOfContainer ex:(Iter_\d+)', bb).group(1), lit("Refined by the lineage agent in the open Iter_54 after the 13:04 exam change request (Backlog rebuilt as Out3_BacklogR44) and before the launch; no dependency is open; startable. The papers story stays Proposed until the cover and items Build tasks are Done.")))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Exam cover, items, honesty successor, Ch05 repair and Ch02-04 code stories and Build tasks refined to Ready")))
