#!/usr/bin/env python3
"""sen0401_lineage_work_begun v1_10_0 (over 1.6.0: briefs of the page tasks regenerated in briefs/iter20; over 1.5.0: the sessions of Iter_17, the chapter 5 and 6 remedy; briefs in briefs/iter20) - records in ONE new register version that an executor session has really started on READY Build tasks of the third lineage, inside a started sprint (G113):
each task goes Ready -> InProgress with startedAt = the clock (UTC) at the moment of writing, taken after the start gate (backlog_execution_ready) answered READY for the lineage and for the task;
a TransitionEvent (T_Start) is recorded for it, and its note and the task's audit note NAME THE EXECUTOR SESSION (from the brief tool, the same names as briefs/iter16/INDEX.md). The parent story goes
InProgress with the first start, with its own TransitionEvent; the lineage status is LS_InProgress (G87). v1.1.0 over v1.0.0: the session is named; TransitionEvents are recorded; refuses a task whose sprint has no start.
Usage: sen0401_lineage_work_begun_v1_9_0.py TASK [TASK...]"""
__version__ = "1.10.0"
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
SESSIONS = {"TK_Ch78_DeckCheck": "SEN0401-I20-deckcheck", "TK_Ch07_Deck_Build": "SEN0401-I20-deck-ch07", "TK_Ch08_Deck_Build": "SEN0401-I20-deck-ch08", "TK_Ch07_Page_Build": "SEN0401-I20-page-ch07", "TK_Ch08_Page_Build": "SEN0401-I20-page-ch08"}


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    tasks = sys.argv[1:]; assert tasks
    refined = []
    for k in tasks:
        i, j = T.blk(t, k); b = t[i:j]
        if "backlog:hasState backlog:Proposed" in b:
            deps = re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b)))
            assert deps and all(re.search(r"backlog:hasState backlog:Done", t[T.blk(t, d)[0]:T.blk(t, d)[1]]) for d in deps), k + " has a dependency that is not Done"
            t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; refined.append(k)
    open(src + ".gate.tmp", "w").write(t)
    for k in tasks:
        assert k in SESSIONS, k
        d0 = re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", t[T.blk(t, k)[0]:T.blk(t, k)[1]])))
        assert all(re.search(r"backlog:hasState backlog:Done", t[T.blk(t, d)[0]:T.blk(t, d)[1]]) for d in d0), k + " has a dependency that is not Done"
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", k], capture_output=True, text=True)
        assert "VERDICT     : READY" in r.stdout, k + " is not READY: " + r.stdout[-300:]
    now = M.now(); L = []; parents = {}
    for k in tasks:
        i, j = T.blk(t, k); b = t[i:j]
        assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b and "memberOfContainer ex:Iter_" in b, k
        it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        assert re.search(r'ex:%s a backlog:Iteration[^\n]*\n[^\n]*iterationStart "' % it, t), it + " has no start"
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        s = SESSIONS[k]
        L.append('ex:Begin3T_%s a backlog:TransitionEvent ; rdfs:label "%s started by executor session %s"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (k, k, s, k, now, lit("Work begun at %s UTC inside the started sprint ex:%s, after the start gate said READY. Executor session: %s, started with the brief generated from the register (08-tooling/briefs/iter20/BRIEF_%s.md). The builder session does not do this work." % (now, it, s, k))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (k, lit("Work begun %s UTC by the executor session %s (transition ex:Begin3T_%s)." % (now, s, k))))
        par = next(x for x in re.findall(r"\nex:(ST_\w+) a backlog:Story", t) if re.search(r"decomposesInto[^;]*ex:%s\b" % k, t[T.blk(t, x)[0]:T.blk(t, x)[1]])); parents.setdefault(par, []).append(k)
    for sid, ks in parents.items():
        i, j = T.blk(t, sid); b = t[i:j]
        if "backlog:hasState backlog:InProgress" in b: continue
        assert "backlog:hasState backlog:Ready" in b, sid
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        L.append('ex:Begin3T_%s a backlog:TransitionEvent ; rdfs:label "%s started with its first task"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Start ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
                 '    backlog:hasTransitionNote %s .\n' % (sid, sid, sid, now, lit("The story starts with the real start of its first task(s) %s at %s UTC." % (", ".join(ks), now))))
    t = X.set_status(t, "LS_InProgress")
    print(now, os.path.basename(M.write_new(src, t + "\n" + "".join(L), nxt, cur, "Work begun at %s UTC inside the started sprint of the task on %s; each start is a recorded T_Start naming its executor session; the stories and the lineage are InProgress." % (now, ", ".join(tasks)))))


main()
