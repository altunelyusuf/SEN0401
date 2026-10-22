#!/usr/bin/env python3
"""sen0401_lineage_work_resumed v1_0_0 - records in ONE new register version that a Suspended task of the third lineage is resumed by a NEW executor session (G113: T_Resume, Suspended -> In Progress, a recorded move with its instant).
The task keeps its first startedAt (the pause was recorded; a resume is not a new start). Order of the act: every dependency of the task is Done; a temporary copy with the task In Progress is put to the start gate (backlog_execution_ready) and must answer READY for
the lineage and for the task (the gate takes Ready or In Progress, never Suspended); only then the version is written with the clock (UTC) at the moment of writing. The TransitionEvent and the audit note NAME THE EXECUTOR SESSION and the brief file with its SHA-256.
Usage: sen0401_lineage_work_resumed_v1_0_0.py TASK SESSION BRIEF_FILE"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"


def lit(s):
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main():
    task, sess, brief = sys.argv[1:4]
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    i, j = T.blk(t, task); b = t[i:j]
    assert "backlog:hasState backlog:Suspended" in b, task + " is not Suspended"
    deps = re.findall(r"ex:(TK_\w+)", " ".join(re.findall(r"backlog:dependsOn ([^;]*);", b)))
    assert deps and all(re.search(r"backlog:hasState backlog:Done", t[T.blk(t, d)[0]:T.blk(t, d)[1]]) for d in deps), task + " has a dependency that is not Done"
    it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
    assert re.search(r'ex:%s a backlog:Iteration[^\n]*\n[^\n]*iterationStart "' % it, t), it + " has no start"
    new = t[:i] + b.replace("backlog:hasState backlog:Suspended", "backlog:hasState backlog:InProgress", 1) + t[j:]
    open(src + ".gate.tmp", "w").write(new)
    r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", task], capture_output=True, text=True)
    os.remove(src + ".gate.tmp")
    assert "VERDICT     : READY" in r.stdout, task + " is not READY: " + r.stdout[-300:]
    bp = os.path.join(M.REPO, brief); sha = hashlib.sha256(open(bp, "rb").read()).hexdigest()
    now = M.now()
    ev = ('ex:Resume9T_%s a backlog:TransitionEvent ; rdfs:label "%s resumed by executor session %s"@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:T_Resume ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
          '    backlog:hasTransitionNote %s .\n' % (task, task, sess, task, now, lit(
              "Resumed at %s UTC inside the started sprint ex:%s, after the start gate said READY. Executor session: %s, started with the brief %s (SHA-256 %s), generated from the register. All its dependencies are Done (%s). The builder session does not do this work. "
              "The first start of the task is unchanged; the pause (T_Suspend, with its rationale) and this resume are both on the record." % (now, it, sess, brief, sha, ", ".join(deps)))))
    note = 'ex:%s backlog:hasAuditNote %s .\n' % (task, lit("Resumed %s UTC by the executor session %s (transition ex:Resume9T_%s); brief %s, SHA-256 %s." % (now, sess, task, brief, sha)))
    t2 = X.set_status(new + "\n" + ev + note, "LS_InProgress")
    print(now, os.path.basename(M.write_new(src, t2, nxt, cur, "Work resumed at %s UTC: %s goes Suspended -> InProgress by T_Resume, naming the executor session %s and its brief; the start gate said READY; dependencies Done." % (now, task, sess))))


main()
