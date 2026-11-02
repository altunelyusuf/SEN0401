#!/usr/bin/env python3
"""sen0401_lineage_urgent2 v1_0_0 - the owner's urgent word of 2026-11-02 15:43 Istanbul (relayed by the coordinator): stop all work and finish the exams within one to two hours, the owner prints them today. Registers ex:Urgent_2 (UrgentInterruption), urgent items ST_Exam_V6_Papers and its Build task; every other InProgress execution task is Suspended (held, not cancelled, nothing waived, no criterion edited). Usage: URGENT_AT=ISO python3 this; writes one new register version."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); at = os.environ["URGENT_AT"]
REASON = "Owner's urgent word of 2026-11-02 15:43 Istanbul, relayed by the coordinator: stop all work and finish the exams within one to two hours because the owner prints them today; the paper, key and sheet v6 of SEN0401 are the urgent items, all other work is held"
KEEP = {"TK_Exam_V6_Papers_Build"}
held = []
for m in re.finditer(r"^ex:(TK_\w+) a backlog:ExecutionTask.*?(?=^ex:\w+ a )", t, re.S | re.M):
    if m.group(1) in KEEP or "backlog:hasState backlog:InProgress" not in m.group(0): continue
    held.append(m.group(1))
L = ['ex:Urgent_2 a backlog:UrgentInterruption ; rdfs:label "Urgent interruption 2"@en ; backlog:interruptsLineage ex:Lineage3 ; backlog:decidedBy backlog:Owner ;\n    backlog:urgencyDeclaredAt "%s"^^xsd:dateTime ; backlog:urgencyReason %s ;\n    backlog:urgentItem ex:ST_Exam_V6_Papers ; backlog:urgentItem ex:TK_Exam_V6_Papers_Build' % (at, lit(REASON)) + "".join(' ;\n    backlog:holdsItem ex:' + h for h in held) + " .\n"]
for n, h in enumerate(held, 1):
    i, j = T.blk(t, h); b = t[i:j]; why = "Held at %s UTC by the urgent interruption ex:Urgent_2: %s. Suspended, not cancelled; nothing waived; no criterion edited." % (at, REASON)
    b2 = b.replace("backlog:hasState backlog:InProgress", "backlog:hasState backlog:Suspended ; backlog:hasRationale %s" % lit(why), 1); t = t[:i] + b2 + t[j:]
    L.append(C.transition("Urgent2_Hold_%d" % n, h, "T_Suspend", at, why, h + " held"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Urgent interruption 2 (owner, 2026-11-02 15:43 Istanbul): exams first, %d execution tasks held" % len(held)))); print(held)
