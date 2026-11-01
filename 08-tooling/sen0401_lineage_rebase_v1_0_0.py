#!/usr/bin/env python3
"""sen0401_lineage_rebase v1_0_0 - one new register version: the owner's decision (approved in this session, relayed by the coordinator 2026-11-01): the midterm files box ends 2026-11-10 and Ch7-8 are due 2026-11-15. Rebaseline records (as ex:Rebase3_Iter_12) move the planned ends of Iter_52, Iter_53 and Iter_54 to 2026-11-10T20:00:00 (the owner gave the date; the clock time of the earlier ends, 20:00 UTC, is kept); the Ch7-8 date is recorded as a decision with its carrier named. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
NEW = "2026-11-10T20:00:00"
RAT = ("Owner decision, approved in this session on 2026-11-01 and relayed by the coordinator: the midterm files box ends 2026-11-10 (the date is the owner's; the clock time 20:00 UTC of the earlier planned ends is kept, an assumption). The iteration is planned and not started (the ceremony is held when it starts), so the planned end moves and the earlier target is kept in this record.")
for it in ("Iter_52", "Iter_53", "Iter_54"):
    i, j = T.blk(t, it); b = t[i:j]; m = re.search(r'backlog:iterationEnd "([^"]+)"', b); old = m.group(1); assert old < NEW, (it, old)
    t = t[:i] + b.replace('backlog:iterationEnd "%s"' % old, 'backlog:iterationEnd "%s"' % NEW, 1) + t[j:]
    L.append('ex:Rebase3_%s_Nov10 a backlog:Rebaseline ; rdfs:label "%s: planned end moved to 2026-11-10 by the owner"@en ; backlog:rebaselines ex:%s ; backlog:hasPreviousTarget "%s" ; backlog:hasNewTarget "%s" ;\n    backlog:hasRebaselineRationale %s ; backlog:rebaselinedAt "%s"^^xsd:dateTime ; backlog:decidedBy backlog:Owner .\n' % (it, it, it, old, NEW, lit(RAT), now))
L.append('ex:Iter_54 rdfs:comment %s@en .\n' % lit("Owner decision of 2026-11-01 (relayed by the coordinator): Chapters 7 and 8 are due 2026-11-15. No iteration or story of this register carries that work: the earlier Chapter 7 and 8 deck and page stories are Cancelled or Done (Iter_20, Iter_25) and only ex:ST_Ch07_PageMeasure and ex:ST_Ch08_PageMeasure (Iter_49) are Proposed. The date is recorded here as the owner's decision so it does not drift; the work is planned as its own iteration, with its stories, when the midterm package is closed (no new scope is opened while the running mission is open)."))
print(os.path.basename(M.write_new(src, t + "\n" + "".join(L), nxt, cur, "Owner decision: planned ends of Iter_52, Iter_53 and Iter_54 moved to 2026-11-10 by Rebaseline records; Chapters 7 and 8 due 2026-11-15 recorded.")))
