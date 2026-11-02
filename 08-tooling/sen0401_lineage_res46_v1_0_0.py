#!/usr/bin/env python3
"""sen0401_lineage_res46 v1_0_0 - repair of v0.889.0 (res45 backlog step wrote the rebuilt Backlog output under the old name ex:Out3_BacklogR50, a second definition of the retracted output, by a hard-coded name in the route script, instead of ex:Out3_BacklogR51, which the re-admitted items already name). New version: the last PENDING block is renamed to R51. Usage: no arguments."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
k = t.rindex("ex:Out3_BacklogR50 a backlog:StageOutput ;"); assert 'closedAtCommit "PENDING"' in t[k:] and t.count("ex:Out3_BacklogR50 a backlog:StageOutput") == 2
t = t[:k] + "ex:Out3_BacklogR51 a backlog:StageOutput ;" + t[k + len("ex:Out3_BacklogR50 a backlog:StageOutput ;"):]
print(os.path.basename(M.write_new(src, t, nxt, cur, "Repair of v0.889.0: the rebuilt Backlog output of the combined-run proof is named Out3_BacklogR51 (the items already name it); v0.889.0 wrote a second definition of Out3_BacklogR50 by a hard-coded name in the route script.")))
