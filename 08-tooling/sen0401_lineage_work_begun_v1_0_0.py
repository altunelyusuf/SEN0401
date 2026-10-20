#!/usr/bin/env python3
"""sen0401_lineage_work_begun v1_0_0 - records in ONE new register version that work has begun on the READY Build tasks of the Stage 3.F and Stage 4 gap stories of the third lineage
(ex:ST_Gap_Stage3F, ex:ST_Gap_Stage4): each named task goes Ready -> InProgress with startedAt = the clock (UTC) at the moment of writing, taken after the start gate
(backlog_execution_ready) has answered READY for the lineage and for the task; the parent story goes InProgress with the same start (the first task's); the lineage status is LS_InProgress (G87).
Usage: sen0401_lineage_work_begun_v1_0_0.py TASK [TASK...]   (refuses a task the gate does not call READY)"""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"


def block(t, name):
    i = t.index("\nex:%s a backlog:" % name) + 1
    j = t.find("\nex:", i)
    return i, (len(t) if j < 0 else j)


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    tasks = sys.argv[1:]
    for k in tasks:
        r = subprocess.run([sys.executable, GATE, src, "--lineage", "Lineage3", "--item", k], capture_output=True, text=True)
        assert "VERDICT     : READY" in r.stdout, k + " is not READY: " + r.stdout[-300:]
    now = M.now()
    parents = {"ST_Gap_Stage3F": [], "ST_Gap_Stage4": []}
    for k in tasks:
        i, j = block(t, k); b = t[i:j]
        assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        parents["ST_Gap_Stage3F" if "Gap3F" in k else "ST_Gap_Stage4"].append(k)
    for s, ks in parents.items():
        if ks:
            i, j = block(t, s); b = t[i:j]
            assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, s
            t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
    t = X.set_status(t, "LS_InProgress")
    print(now, os.path.basename(M.write_new(src, t, nxt, cur, "Work begun on the READY Build tasks of ST_Gap_Stage3F and ST_Gap_Stage4 (start gate READY for the lineage and for each task); started %s UTC; the stories and the lineage are InProgress." % now)))


main()
