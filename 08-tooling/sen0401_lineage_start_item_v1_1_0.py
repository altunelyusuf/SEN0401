#!/usr/bin/env python3
"""sen0401_lineage_start_item v1_1_0 - records, in a NEW version of the SEN0401 slides lineage register, that work on ONE planned story has begun: the story and its build
task read InProgress and carry the start time. v1.1.0: it also refuses to start a story while a story it depends on is not Done (a deck is not started before its research is recorded Done).
It first requires backlog_execution_ready to say READY for the item (exit 0); it records nothing else and
never marks anything Done. The committed version stays.

Usage: sen0401_lineage_start_item_v1_1_0.py ST_Research_Ch08
"""
__version__ = "1.1.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

FW = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling"


def main():
    sid = sys.argv[1]
    src = M.newest(); nxt, cur = M.next_version(src)
    r = subprocess.run([sys.executable, os.path.join(FW, "backlog_execution_ready_v1_2_0.py"), src, "--lineage", "Lineage2", "--item", sid], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout + r.stderr); raise SystemExit("not ready: the start gate refused " + sid)
    t = open(src, encoding="utf-8").read(); now = M.now()
    for d in set(re.findall(r"backlog:dependsOn ex:(ST_\w+)", re.search(r"ex:%s a backlog:Story.*?\n\n" % re.escape(sid), t, re.S).group(0))):
        if not re.search(r"ex:%s a backlog:Story.*?backlog:hasState backlog:Done" % d, t, re.S) or "backlog:hasState backlog:Done" not in re.search(r"ex:%s a backlog:Story.*?\n\n" % d, t, re.S).group(0):
            raise SystemExit("not started: %s depends on %s, which is not Done" % (sid, d))
    m = re.search(r"ex:%s a backlog:Story.*?\n\n" % re.escape(sid), t, re.S); blk = m.group(0)
    assert "backlog:hasState backlog:Ready ;" in blk, sid + " is not Ready"
    tk = "TK_" + sid[3:] + "_Build"
    m2 = re.search(r"ex:%s a backlog:ExecutionTask.*?backlog:hasAuditNote [^\n]*\n" % tk, t, re.S); tb = m2.group(0)
    assert "backlog:hasState backlog:Proposed ;" in tb, tk + " is not Proposed"
    t = t.replace(blk, blk.replace("backlog:hasState backlog:Ready ;", "backlog:hasState backlog:InProgress ; backlog:startedAt \"%s\"^^xsd:dateTime ;" % now, 1))
    t = t.replace(tb, tb.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:InProgress ; backlog:startedAt \"%s\"^^xsd:dateTime ;" % now, 1))
    out = M.write_new(src, t, nxt, cur, "Work on %s begun (the story and its build task InProgress, started %s UTC) after the start gate said READY for it. Nothing else started, nothing Done." % (sid, now))
    print(os.path.basename(out))


main()
