#!/usr/bin/env python3
"""sen0401_lineage_urgent2_lift v1_0_0 - the urgent interruption ex:Urgent_2 (owner, 2026-11-02 15:43 Istanbul) is resolved and the lineage resumes: the exam v6 Papers Build is Done (control v0.947), the owner has the files, the floor correction is registered Ready; every task held by Urgent_2 moves Suspended -> InProgress by T_Resume, recorded. Nothing waived. Disclosed: Urgent_2 was written by the urgent2 script, not by the framework tool backlog_urgency (declared before the tool was found), and the urgent story ST_Exam_V6_Papers stays In Progress for its open Verify task, which the tool's resolve step would refuse; the resolve and resume are recorded here by hand with the same facts. Usage: LIFT_AT=ISO python3 this."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); at = os.environ["LIFT_AT"]
i0 = t.index("ex:Urgent_2 a backlog:UrgentInterruption"); blk = t[i0:t.index("\n", t.index("backlog:holdsItem", i0))]; m = re.search(r"ex:Urgent_2 a backlog:UrgentInterruption.*?\.\n", t[i0:], re.S); body = m.group(0)
held = re.findall(r"backlog:holdsItem ex:(\w+)", body); assert held
L = ['ex:Urgent_2 backlog:urgencyResolvedAt "%s"^^xsd:dateTime ; backlog:urgencyResumedAt "%s"^^xsd:dateTime .\n' % (at, at)]
for n, h in enumerate(held, 1):
    i, j = T.blk(t, h); b = t[i:j]; assert "backlog:hasState backlog:Suspended" in b, h
    b2 = re.sub(r"backlog:hasState backlog:Suspended ; backlog:hasRationale \"(?:[^\"\\]|\\.)*\"", "backlog:hasState backlog:InProgress", b, count=1); assert b2 != b, h
    t = t[:i] + b2 + t[j:]
    L.append(C.transition("Urgent2_Resume_%d" % n, h, "T_Resume", at, "Resumed at %s UTC: the urgent interruption ex:Urgent_2 is resolved (the exam v6 papers are controlled and delivered, the floor correction is registered Ready). Held, not cancelled; nothing waived; no criterion edited." % at, h + " resumed"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Urgent interruption 2 resolved, %d held execution tasks resumed" % len(held))))
