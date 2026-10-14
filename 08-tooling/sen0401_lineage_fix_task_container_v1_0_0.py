#!/usr/bin/env python3
"""sen0401_lineage_fix_task_container v1_0_0 - new register version that moves the build and verify tasks of chapter 8 from the first lineage's Backlog container into the
second lineage's own iteration (Iter_4). Version 0.32.0 put them in the first lineage's container, which derived an open state there and failed the validator
(L1, a wound-down lineage's container is dissolved, never carried). Nothing else changes. Usage: sen0401_lineage_fix_task_container_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_0_0 as M
src = M.newest(); nxt, cur = M.next_version(src)
t = open(src, encoding="utf-8").read()
pat = re.compile(r'(ex:TK_(?:Research|Deck|Page)_Ch08_(?:Build|Verify) a backlog:ExecutionTask[^\n]*\n\s+backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer )ex:Backlog')
t2, n = pat.subn(r'\1ex:Iter_4', t); assert n == 6, n
print(os.path.basename(M.write_new(src, t2, nxt, cur, "The build and verify tasks of chapter 8 moved from the first lineage's Backlog container into the second lineage's Iter_4, which version 0.32.0 had left them out of; version 0.32.0 did not validate (L1). No other change.")))
