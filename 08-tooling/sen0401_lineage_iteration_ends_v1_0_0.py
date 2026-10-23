#!/usr/bin/env python3
"""sen0401_lineage_iteration_ends v1_0_0 - records the owner's decision (relayed by the course coordinator, Friday 2026-10-23) to move the end of Iterations 13, 16, 17 and 18 to today 23:59 UTC. The proposed ends were the builder's (the register said the owner decides the end); the plan baselines keep the ends as planned, so the overrun stays visible. Only backlog:iterationEnd of the four iterations changes; a comment on each names the decision. The time the owner wrote the answer is not known to the builder session; the recording instant is stamped from the clock."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; NEW = "2026-10-23T23:59:00"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for n in (13, 16, 17, 18):
    m = re.search(r'(\nex:Iter_%d a backlog:Iteration;?[^\n]*\n(?:(?!\nex:)[^\n]*\n)*?[^\n]*?iterationEnd )"([^"]*)"' % n, t); assert m, n
    old = m.group(2); t = t.replace(m.group(0), m.group(1) + '"%s"' % NEW, 1)
    L.append('ex:Rebaseline31_Iter_%d a backlog:Rebaseline ; rdfs:label "End of Iteration %d moved to 2026-10-23T23:59:00 UTC on the owner\'s decision"@en ;\n    backlog:rebaselines ex:Iter_%d ; backlog:hasPreviousTarget "%s" ; backlog:hasNewTarget "%s" ; backlog:rebaselinedAt "%s"^^xsd:dateTime ; backlog:decidedBy backlog:Owner ;\n    backlog:hasRebaselineRationale %s .\n' % (n, n, n, old, NEW, now, lit("Owner's decision of Friday 2026-10-23, relayed by the course coordinator in answer to the builder session's question: the end was the builder's proposal and the stories of this iteration were still open when it passed; the end moves to 2026-10-23T23:59:00 UTC. The time at which the owner wrote the answer is not known to the builder session; the recording instant is stamped from the clock. The plan baseline of the iteration keeps the end as planned (%s)." % old)))
    L.append("ex:Iter_%d rdfs:comment %s@en .\n" % (n, lit("End moved %s UTC (recorded in v%s) from %s to %s on the owner's decision of Friday 2026-10-23, relayed by the course coordinator in answer to the builder session's question (the time at which the owner wrote it is not known to the builder session). The end was the builder's proposal; the plan baseline keeps the end as planned (%s), so the overrun stays visible. Reason: the stories of this iteration are still open when the proposed end passed." % (now, nxt, old, NEW, old))))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, "Owner's decision recorded: the end of Iterations 13, 16, 17 and 18 moved to 2026-10-23T23:59:00 UTC; the plan baselines keep the planned ends.")))
