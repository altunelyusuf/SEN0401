#!/usr/bin/env python3
"""sen0401_lineage_control21 v1_0_0 - the Verify task of chapter 10 (TK_SecLinks_Ch10_Verify), run by the builder session after TK_SecLinks_Ch10_Page is Done (G113, G136).
start    the task goes Proposed -> Ready (T_Refine) -> InProgress (T_Start) in one version, after the start gate (backlog_execution_ready) says READY; its dependency must be Done
prepare  the bridge runs every check of the task again, one after the other (sen0401_lineage_page_check v1_2_0, the Stage 4 runner, the chapter checks); the page-test elements read the logs of the control run of the same page files
record   the task goes Done (T_Complete) with its own bridge-verified evidence and a harness; the notes. Nothing else is started and no story is closed.
Usage: sen0401_lineage_control21_v1_0_0.py start|prepare|record"""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control20_v1_0_0 as K
lit = C.lit; WORK = "/tmp/claude-0/s/ctl21"; VT = K.VT; TK = K.TK
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"


def start():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); i, j = T.blk(t, VT); b = t[i:j]
    assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
    assert re.search(r"backlog:hasState backlog:Done", t[T.blk(t, TK)[0]:T.blk(t, TK)[1]]), TK + " is not Done"
    tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
    r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp")
    assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
    now = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
    ev = C.transition("Ready21T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the refinement ex:Refine_%s already names the checks, the page and what a passing result is. The start gate was asked right after (it answered READY)." % (ready, TK, cur, VT), VT + " ready")
    ev += C.transition("Begin21T_" + VT, VT, "T_Start", now, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s: the checks of the task run one after the other on the evidence bridge; nothing is changed or waived; every result is recorded as printed." % (now, it), VT + " started")
    t = X.set_status(t + "\n" + ev, "LS_InProgress")
    print(now, os.path.basename(M.write_new(src, t, nxt, cur, "Verify task %s made Ready and started at %s UTC (start gate READY, dependency %s Done)." % (VT, now, TK))))


def prepare():
    os.makedirs(WORK, exist_ok=True); draft = [K.PRE]
    for kind, spec, tid in K.KINDS:
        draft.append('ex:Ev21C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, lit("Verify run: %s, chapter 10, page 9.79.0" % K.LABEL[kind]), tid, spec))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    cmd = "python3 -B {spec} {id} > %s/bridge_verify_$(echo {id} | tr '/:' '__').log 2>&1" % K.LOGDIR
    r = subprocess.run([sys.executable, C.BRIDGE, d, "--workspace", K.REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-400:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); V = {k: v["Ev21C_" + k] for k, _, _ in K.KINDS}; L = []; OUT = {}
    for kind, spec, tid in K.KINDS:
        lg = os.path.join(K.LOGDIR, "bridge_verify_%s.log" % tid.replace("/", "_").replace(":", "_")); OUT[kind] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:200]
    bad = [k for k in V if not V[k][0]]; assert not bad, "a check is not verified: %s" % bad
    logs = sorted(os.path.relpath(p, K.REPO) for p in glob.glob(os.path.join(K.LOGDIR, "bridge_verify_*.log"))); ver = C.bridge_files(logs, now); assert all(x[1][0] for x in ver.values())
    for kind, spec, tid in K.KINDS:
        ok, at, how = V[kind]; crits = [K.CRIT] + ([K.TCRIT] if kind in K.AC3T else [])
        L.append('ex:Ev21C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            kind, lit("Verify run: %s, chapter 10, page 9.79.0" % K.LABEL[kind]), ", ".join("ex:" + c for c in crits), tid, spec, lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), K.CRIT, f, K.sha256(f), at))
    ex = ["Ev21C_" + k for k, _, _ in K.KINDS]
    i, j = T.blk(t, VT); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, VT
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), now, now), 1) + t[j:]
    L.append(C.transition("Done21T_" + VT, VT, "T_Complete", now, "Verification finished %s UTC: all %d checks ran one after the other on the bridge and are verified; recorded as printed." % (now, len(K.KINDS)), VT + " completed"))
    L.append('ex:Harness21C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
    L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, K.CRIT, ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + e for e, _ in ver.values()),
             lit("Done, recorded %s: the checks of the task ran one after the other on the bridge after the task started; results as printed: %s. The page-test elements read the logs of the builder's control run of the same page files on the same day (08-tooling/verify/iter16/ch10, the page and its SHA-256 are unchanged since); the page tests were not run a second time." % (now[:10], " | ".join("%s -> %s" % (k, OUT[k][:120]) for k in OUT)))))
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, "Verify task %s Done at %s UTC on bridge-verified evidence and a harness. ST_Section_Links and ST_Page_Template stay InProgress (chapter 11 open)." % (VT, now))))


if __name__ == "__main__":
    {"start": start, "prepare": prepare, "record": record}[sys.argv[1]]()
