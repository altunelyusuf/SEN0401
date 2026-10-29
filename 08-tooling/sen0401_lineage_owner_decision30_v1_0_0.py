#!/usr/bin/env python3
"""sen0401_lineage_owner_decision30 v1_0_0 - records the owner's answer of 2026-10-30 on the chapter lists as a comment on ex:CR3_ExamMission (no stage content; the mission text is not touched)."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_gap_revision_v1_0_0 as G
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
txt = ("OWNER DECISION of 2026-10-30, relayed by the coordinator: the chapter lists keep the defaults. SEN0401: chapters 1 to 6 are the exam chapters; chapter 7 is NOT in. (The engine's chapter list stays a parameter with the default 1-6; chapter 7 stays selectable but is not used.) "
       "The decision for SEN0414 (chapters 1 to 8 without the chapter 5 debugging) belongs to that course's own register and is not recorded here. This closes the doubt about chapter 7 recorded in the owner statements above.")
t += "\nex:CR3_ExamMission rdfs:comment %s@en .\n" % G.lit(txt)
print(os.path.basename(M.write_new(src, t, nxt, cur, "Owner decision of 2026-10-30 recorded on the change request ex:CR3_ExamMission: SEN0401 exam chapters 1 to 6, chapter 7 not in (defaults kept). A comment; no stage content.")))
