#!/usr/bin/env python3
"""sen0401_lineage_work_begun v1_2_0 - records in ONE new register version that an executor session has really started on READY Build tasks of the third lineage, inside a started sprint (G113):
each task goes Ready -> InProgress with startedAt = the clock (UTC) at the moment of writing, taken after the start gate (backlog_execution_ready) answered READY for the lineage and for the task;
a TransitionEvent (T_Start) is recorded for it, and its note and the task's audit note NAME THE EXECUTOR SESSION (from the brief tool, the same names as briefs/iter14/INDEX.md). The parent story goes
InProgress with the first start, with its own TransitionEvent; the lineage status is LS_InProgress (G87). v1.1.0 over v1.0.0: the session is named; TransitionEvents are recorded; refuses a task whose sprint has no start.
Usage: sen0401_lineage_work_begun_v1_1_0.py TASK [TASK...]"""
__version__ = "1.2.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
SESSIONS = {"TK_SecLinks_Ch10_Research": "SEN0401-I14-research-ch10", "TK_SecLinks_Ch11_Research": "SEN0401-I14-research-ch11", "TK_SecLinks_PageData": "SEN0401-I14-pagedata", "TK_SecLinks_Ch10_Page": "SEN0401-I14-page-ch10", "TK_SecLinks_Ch11_Page": "SEN0401-I14-page-ch11"}


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    tasks = sys.argv[1:]; assert tasks
    assert re.search(r'ex:Iter_14 a backlog:Iteration[^\n]*\n[^\n]*iterationStart "', t), "Iter_14 has no start"
    for k in tasks:
        assert k in SESSIONS, k
        r = subprocess.run([sys.executable, GATE, src, "--lineage", "Lineage3", "--item", k], capture_output=True, text=True)
        assert "VERDICT     : READY" in r.stdout, k + " is not READY: " + r.stdout[-300:]
    now = M.now(); L = []; parents = {}
    for k in tasks:
        i, j = T.blk(t, k); b = t[i:j]
        assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b and "memberOfContainer ex:Iter_14" in b, k
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        s = SESSIONS[k]
        L.append('ex:Begin3T_%s a backlog:TransitionEvent ; rdfs:label "%s started by executor session %s"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (k, k, s, k, now, lit("Work begun at %s UTC inside the started sprint ex:Iter_14, after the start gate said READY. Executor session: %s, started with the brief generated from the register (08-tooling/briefs/iter14/BRIEF_%s.md). The builder session does not do this work." % (now, s, k))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, lit("Work begun %s UTC by the executor session %s (transition ex:Begin3T_%s)." % (now, s, k))))
        parents.setdefault("ST_Section_Links", []).append(k)
    for sid, ks in parents.items():
        i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        L.append('ex:Begin3T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first task"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (sid, sid, sid, now, lit("The story starts with the real start of its first task(s) %s at %s UTC." % (", ".join(ks), now))))
    t = X.set_status(t, "LS_InProgress")
    print(now, os.path.basename(M.write_new(src, t + "\n" + "".join(L), nxt, cur, "Work begun at %s UTC inside the started sprint Iter_14 on %s; each start is a recorded T_Start naming its executor session; the stories and the lineage are InProgress." % (now, ", ".join(tasks)))))


main()
