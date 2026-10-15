#!/usr/bin/env python3
"""sen0401_lineage_note v1_0_0 - writes, in a NEW register version, dated audit notes on stories and changes nothing else (no state, no evidence). Use it to record a failing check on a story that
stays open, or a caveat on a Done story whose record is not edited.
Usage: env NOTE_<STORY>=text sen0401_lineage_note_v1_0_0.py "header comment" STORY [STORY...]
"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
t += "\n" + "".join('ex:%s backlog:hasAuditNote "%s" .\n' % (s, M.esc(os.environ["NOTE_" + s])) for s in sys.argv[2:])
print(os.path.basename(M.write_new(src, t, nxt, cur, sys.argv[1])))
