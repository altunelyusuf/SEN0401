#!/usr/bin/env python3
"""sen0401_lineage_story_finish_fix v1_0_0 - ONE new register version that corrects the finish date of ST_Gap_Stage3F, recorded in v0.136 as 2026-10-21T01:16:33 (the last of the four tasks the story block lists) although the story
also decomposes into TK_Gap3F_Ch05_Build and TK_Gap3F_Ch05_Verify (declared in a later triple), the last of which finished 2026-10-21T02:02:01. A story finishes at its last task. Usage: no arguments."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M


def blk(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read()
    for sid in ("ST_Gap_Stage3F", "ST_Gap_Stage4"):
        tasks = set()
        for m in re.finditer(r"ex:%s [^\n]*?backlog:decomposesInto ([^;.\n]*)" % sid, t):
            tasks |= set(x.strip().replace("ex:", "") for x in m.group(1).split(","))
        i, j = blk(t, sid)
        for m in re.finditer(r"\n\s+backlog:decomposesInto ([^;.\n]*)", t[i:j]):
            tasks |= set(x.strip().replace("ex:", "") for x in m.group(1).split(","))
        fins = []
        for tk in tasks:
            a, z = blk(t, tk); b = t[a:z]
            assert "backlog:hasState backlog:Done" in b, tk
            fins.append(re.search(r'backlog:finishedAt "([^"]*)"', b).group(1))
        last = max(fins)
        cur_fin = re.search(r'backlog:finishedAt "([^"]*)"', t[i:j]).group(1)
        print(sid, len(tasks), "tasks, last finish", last, "recorded", cur_fin)
        if cur_fin != last:
            t = t[:i] + t[i:j].replace('backlog:finishedAt "%s"' % cur_fin, 'backlog:finishedAt "%s"' % last, 1) + t[j:]
            t += '\nex:%s backlog:hasAuditNote "Date correction %s: v0.136 recorded the finish as %s, the last of the four tasks listed in the story block; the story has %d tasks (the two chapter 5 tasks are declared in a later triple) and the last finished %s UTC. A story finishes at its last task; the finish is now %s." .\n' % (sid, M.now()[:10], cur_fin, len(tasks), last, last)
    out = M.write_new(src, t, nxt, cur, "Finish date of the gap stories corrected to the finish of their last task. Dates only.")
    print(os.path.basename(out))


main()
