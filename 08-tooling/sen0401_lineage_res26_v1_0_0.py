#!/usr/bin/env python3
"""sen0401_lineage_res26 v1_0_0 - records the owner's ruling of 2026-10-30 (relayed by the coordinator): the page-test copies 9.34.3, 9.35.3 and 9.38.0 are accepted as the page tests for pages whose Playground lists the slide examples first; the committed 9.34.2, 9.35.2 and 9.37.0 stay unchanged and keep their crashed result for the old layout. Change request ex:CR3_PageTestCopies (accepted) with ex:IA3_PageTestCopies; the not-started criterion AC9_Repair_Ch06_Lecture (element 4) carries the ruling. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
RULE = ("THE OWNER'S RULING (2026-10-30, relayed by the coordinator; answer to the question of the control of the urgent chapter 6 page): YES, the copies 9.34.3, 9.35.3 and 9.38.0 are accepted as the page tests for pages whose Playground lists the slide examples first; the old tests 9.34.2, 9.35.2 and 9.37.0 stay unchanged and keep their crashed result for the old layout (measured: 9.37.0 and 9.34.2 crash with StopIteration on page v9.89.0). Earlier controls are not re-judged: the cancelled story ST_Urgent_Ch06_Page keeps its recorded NOT MET on the committed tests; the ruling applies from now to the repair story and to later pages with that layout.")
i, j = T.blk(t, "AC9_Repair_Ch06_Lecture"); b = t[i:j]
o = "(4) the page tests 9.34.3, 9.35.3 and 9.38.0 pass, and the committed 9.34.2, 9.35.2 and 9.37.0 are reported as printed"; assert o in b
b = b.replace(o, o + " (the owner accepted the copies as the page tests for pages with the slide-example list, 2026-10-30; the committed ones keep their crashed result for the old layout)", 1); t = t[:i] + b + t[j:]
cr = '\nex:CR3_PageTestCopies a backlog:ChangeRequest ;\n    rdfs:label "The page-test copies are accepted as the page tests for pages with the slide-example list"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; backlog:hasDisposition backlog:Disp_Accepted ; rdfs:seeAlso ex:IA3_PageTestCopies, ex:CR3_Ch06Repairs ;\n    backlog:hasChangeRequestRationale %s .\n' % lit(RULE)
ia = '\nex:IA3_PageTestCopies a backlog:ImpactAssessment ;\n    rdfs:label "What accepting the page-test copies touches"@en ;\n    backlog:analyzesRequest ex:CR3_PageTestCopies ; backlog:identifiesAffectedLineage ex:Lineage3 ;\n    backlog:hasImpactStatement %s .\n' % lit(RULE + " AFFECTED: the criterion of ST_Repair_Ch06_Lecture (not started; element 4 states the ruling, nothing weakened); the later chapter pages with the slide-example list. NOT AFFECTED: every committed test and file, the exam work.")
print(os.path.basename(M.write_new(src, X.set_status(t + cr + ia, "LS_InProgress"), nxt, cur, "Owner's ruling recorded (CR3_PageTestCopies accepted): the page-test copies 9.34.3, 9.35.3 and 9.38.0 are the page tests for pages with the slide-example list; criterion of the Lecture repair carries it")))
