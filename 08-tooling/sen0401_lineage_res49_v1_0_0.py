#!/usr/bin/env python3
"""sen0401_lineage_res49 v1_0_0 - repair of v0.916.0: the route script was given an empty commit id by a failed commit command (a wrong file glob), so the StageRevision of the exam move follow-up (ex:Revision_Lineage3_Backlog25) holds revisedAtCommit "fatal:". New version: it is set to the commit that holds the retraction (v0.915.0), f6196a9. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
assert t.count('backlog:revisedAtCommit "fatal:"') == 1
t = t.replace('backlog:revisedAtCommit "fatal:"', 'backlog:revisedAtCommit "f6196a9"')
print(os.path.basename(M.write_new(src, t, nxt, cur, "Repair of v0.916.0: the revisedAtCommit of Revision_Lineage3_Backlog25 is the commit f6196a9 that holds the retraction (it read fatal: because a commit command failed on a wrong file glob).")))
