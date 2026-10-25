#!/usr/bin/env python3
"""sen0401_lineage_plan_later24 v1_0_0 - PlanningEvents for the stories of Iterations 25 to 28 admitted by ex:CR3_Retro24 (the validator's L2: a task must trace to a planning event). The iterations are planned, NOT started: no ceremony is held; the event
names the planned iteration, as ex:Plan3I_ST_Ch01_Deck did for Iteration 21. New file over the newest register; one event."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []; n = 0
for it in ("Iter_25", "Iter_26", "Iter_27", "Iter_28"):
    i, j = T.blk(t, it); mem = re.findall(r"ex:((?:ST|TK)_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", t[i:j], re.S).group(1))
    for s in [m for m in mem if m.startswith("ST_")]:
        b = t[T.blk(t, s)[0]:T.blk(t, s)[1]]; tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1)); assert all(k in mem for k in tks), s
        L.append('ex:Plan3L_%s a backlog:PlanningEvent ; rdfs:label "Planning of %s into iteration %s (planned, not started)"@en ; backlog:belongsToLineage ex:Lineage3 ;\n    backlog:plannedAt "%s"^^xsd:dateTime ; backlog:plannedBy backlog:Builder ; backlog:plannedInto ex:%s ;\n    backlog:plansItem ex:%s ; backlog:producesTask %s ;\n    backlog:refinementProduces ex:Spec3I_Retro24, ex:Spec3I_Retro24_Pass, ex:Spec3I_Retro24_Fail .\n' % (s, s, it[5:], now, it, s, ", ".join("ex:" + k for k in tks))); n += 1
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Planning events for the %d stories of Iterations 25 to 28 (planned, not started; no ceremony)." % n)))
