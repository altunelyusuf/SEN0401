#!/usr/bin/env python3
"""sen0401_lineage_res25 v1_0_0 - records the owner's Bloom decision of 2026-10-30 about 10:30 Istanbul (relayed by the coordinator) through change management: ex:CR3_BloomRule (accepted) with ex:IA3_BloomRule; the not-started Items task and its criterion AC3E_Exam_Items are rewritten (G133 forbids it only while work runs). Usage: no arguments; writes one new register version."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
RULE = ("BLOOM RULE (owner's answer of 2026-10-30 about 10:30 Istanbul, relayed by the coordinator): 'higher level' means Apply and above (use it, and work out why); AND at least 6 items at Analyze or above (work out why) per 24-item paper. The owner's own minimum for the 30-item SEN0414 paper is 8; the 6 for 24 items is a DEFAULT derived proportionally (8/30 x 24 = 6.4, rounded down), NOT the owner's word, to be confirmed by the owner when he sees the items. The majority of items is therefore at Apply or above, and the report names the count at Analyze or above. Chapter 6 has no Analyze item in the banks (seeds cannot give them): write those items new.")
i, j = T.blk(t, "TK_Exam_Items_Build"); b = t[i:j]; assert "startedAt" not in b
old = "a majority of items at the higher Bloom level"; assert old in b
b = b.replace(old, "a majority of items at Apply or above, and at least 6 items at Analyze or above (a default derived from the owner's 8 of 30; see ex:CR3_BloomRule)", 1)
b = b.replace("REPORT for the midterm: the chapters, the types, the Bloom levels,", "REPORT for the midterm: the chapters, the types, the Bloom levels (with the count at Apply or above and at Analyze or above),", 1)
t = t[:i] + b + t[j:]
i, j = T.blk(t, "AC3E_Exam_Items"); b = t[i:j]
o2 = "(5) every term is found in the course corpus (EN08); the level, letter, weight and width conventions hold"; assert o2 in b
b = b.replace(o2, o2 + "; at least half plus one of the 24 items are at Apply or above and at least 6 at Analyze or above (the 6 is a default derived from the owner's 8 of 30, to be confirmed by the owner)", 1)
t = t[:i] + b + t[j:]
cr = '\nex:CR3_BloomRule a backlog:ChangeRequest ;\n    rdfs:label "Higher Bloom level means Apply and above, with a minimum at Analyze and above"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Accepted ; rdfs:seeAlso ex:IA3_BloomRule, ex:CR3_ExamMission ;\n    backlog:hasChangeRequestRationale %s .\n' % lit(RULE)
ia = '\nex:IA3_BloomRule a backlog:ImpactAssessment ;\n    rdfs:label "What the Bloom rule touches"@en ;\n    backlog:analyzesRequest ex:CR3_BloomRule ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n' % lit(RULE + " AFFECTED: the Items task and its criterion (not started; text rewritten, nothing waived); the Papers task reads the same rule through the engine. NOT AFFECTED: the engine (it already checks a Bloom majority), every committed file, the other stories. COST: none beyond the Items estimate; the chapter 6 Analyze items have no seed.")
print(os.path.basename(M.write_new(src, X.set_status(t + cr + ia, "LS_InProgress"), nxt, cur, "Owner's Bloom decision recorded (CR3_BloomRule accepted): higher level = Apply and above, at least 6 of 24 at Analyze or above (default derived from the owner's 8 of 30); Items task and criterion rewritten before any work began")))
