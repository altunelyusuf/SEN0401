#!/usr/bin/env python3
"""sen0401_lineage_owner_decision33 v1_0_0 - records the owner's ruling of 2026-10-30 00:51 Istanbul on the interactive page questions as seeds, not exam items. Comment on the change request and a note on the Items task; no stage content."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_gap_revision_v1_0_0 as G
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
q = ("Interactive page questions are accessible by the students before the exam. They are chapter subject specific questions, rarely cross-section. It is not wise to use them directly, but they can be a seed for better questions and enhancement iterations.")
d = ("OWNER RULING of 2026-10-30 00:51 Istanbul, relayed by the coordinator. The owner's words: '" + q + "' CONSEQUENCES, to be planned through change management: (1) no exam item may be a page item or a near copy of one; the engine gets a new rule, in SHACL, that refuses an item whose stem or option set matches a page-visible item, with a stated similarity method and a fixture of known answer (a new engine version as a new file, the old kept); "
     "(2) the page items serve as seeds: new, better items are built by enhancement iterations (change the situation, combine chapters, reverse the question, add a reasoning step, change the numbers), each new item linking its seed or seeds and the critical points it tests; (3) the bank report asks how many seeds exist per chapter and per critical point and what the seeds cannot give (cross-chapter, synthesis, calculation, reasoning); (4) all item types of the paper rules (matching, ordering, fill-in bank, number, trace) are authored items, not bank items. This replaces the earlier reading that the engine may compose papers from the bank items.")
t += "\nex:CR3_ExamMission rdfs:comment %s@en .\n" % G.lit(d)
t += "ex:TK_Exam_Items_Build backlog:hasAuditNote %s .\n" % G.lit("Note 2026-10-30: the owner ruled that the page questions are seeds and not exam items (see ex:CR3_ExamMission); the text of this task is revised by the change route that follows. It is Ready and not started.")
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner ruling of 2026-10-30 recorded: the interactive page questions are seeds for better questions, not exam items; consequences listed on the change request. A comment and a note; no stage content.")))
