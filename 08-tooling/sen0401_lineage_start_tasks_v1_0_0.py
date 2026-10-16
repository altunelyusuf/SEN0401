#!/usr/bin/env python3
"""sen0401_lineage_start_tasks v1_0_0 - records in ONE new register version that work on the named ExecutionTasks has begun (state InProgress, start time). Each task must first get READY from
backlog_execution_ready (exit 0); nothing else is started, nothing is Done.
Usage: sen0401_lineage_start_tasks_v1_0_0.py TK_A TK_B ...
"""
__version__ = "1.0.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
FW = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling"


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now = M.now()
    for tk in sys.argv[1:]:
        r = subprocess.run([sys.executable, os.path.join(FW, "backlog_execution_ready_v1_2_0.py"), src, "--lineage", "Lineage2", "--item", tk], capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout); raise SystemExit("not ready: " + tk)
        m = re.search(r"ex:%s a backlog:ExecutionTask.*?backlog:hasAuditNote [^\n]*\n" % re.escape(tk), t, re.S); b = m.group(0)
        assert "backlog:hasState backlog:Ready ;" in b, tk + " is not Ready"
        t = t.replace(b, b.replace("backlog:hasState backlog:Ready ;", "backlog:hasState backlog:InProgress ; backlog:startedAt \"%s\"^^xsd:dateTime ;" % now, 1))
    out = M.write_new(src, t, nxt, cur, "Work begun on %s after the start gate said READY for each (started %s UTC). Nothing else started, nothing Done." % (", ".join(sys.argv[1:]), now))
    print(os.path.basename(out))


main()
