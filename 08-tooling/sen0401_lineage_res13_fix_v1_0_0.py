#!/usr/bin/env python3
"""sen0401_lineage_res13_fix v1_0_0 - corrects ONE value of the register version v0.501_0 as a NEW version: the StageRevision ex:Revision_Lineage3_Scope23 got revisedAtCommit "sen0401_slides_lineage_v0_500_0.ttl" (a file name, passed by mistake by the lineage agent's shell helper in place of the commit) instead of the commit 7ad0132 that retracted the outputs (the same field of the earlier revisions holds the retract commit). No other change."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
old = 'backlog:revisedAtCommit "sen0401_slides_lineage_v0_500_0.ttl"'; assert t.count(old) == 1
t = t.replace(old, 'backlog:revisedAtCommit "7ad0132"')
print(os.path.basename(M.write_new(src, t, nxt, cur, "Correction of the revisedAtCommit of ex:Revision_Lineage3_Scope23: the commit 7ad0132 that retracted the outputs (a file name had been written by mistake in v0.501.0).")))
