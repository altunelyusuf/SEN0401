#!/usr/bin/env python3
"""sen0401_lineage_control16 v1_0_0 - the control of the page-data builder task of Iter_14 (G113, G136): the evidence bridge runs, serially, the comparison of the builder v2_23_0 with v2_22_0 on all 14 chapters
(sen0401_lineage_pagedata_check cmp:NN) and verifies the delivered file by SHA-256; records the executor instance and the brief that was passed (links) and TK_SecLinks_PageData Done (T_Complete) with a harness.
Usage: sen0401_lineage_control16_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl16"; BRIDGE = C.BRIDGE; lit = C.lit
SPEC = "08-tooling/sen0401_lineage_pagedata_check_v1_0_0.py"; TASK = "TK_SecLinks_PageData"; COMMIT = "a29bf2b"; SESS = "SEN0401-I14-pagedata"
CHS = ["10", "11"] + ["%02d" % i for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14)]
FILES = ["08-tooling/sen0401_page_data_v2_23_0.py"]
git = lambda *a: subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
utc = lambda sha: datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")


def prepare():
    os.makedirs(WORK, exist_ok=True); ld = os.path.join(REPO, "08-tooling", "verify", "iter14", "pagedata"); os.makedirs(ld, exist_ok=True)
    draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for nn in CHS:
        draft.append('ex:Ev6C_cmp_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "cmp:%s" ; backlog:hasTestSpec "%s" .\n' % (nn, lit("page-data builder v2_23_0 against v2_22_0, chapter %s" % nn), nn, SPEC))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    cmd = "python3 -B {spec} {id} > %s/bridge_$(echo {id} | tr '/:' '__').log 2>&1" % ld
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-200:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); ld = os.path.join(REPO, "08-tooling", "verify", "iter14", "pagedata"); V = {}; OUT = {}
    for nn in CHS:
        V[nn] = v["Ev6C_cmp_Ch%s" % nn]; lg = os.path.join(ld, "bridge_cmp_%s.log" % nn)
        OUT[nn] = " | ".join(l.strip()[:150] for l in open(lg).read().strip().splitlines()[-4:] if l.strip()) if os.path.exists(lg) else ""
    assert all(x[0] for x in V.values()), "a comparison is not verified"
    pushed = utc("dd33f7a"); end = utc(COMMIT)
    bp = "08-tooling/briefs/iter14/BRIEF_%s.md" % TASK; bsha = hashlib.sha256(subprocess.run(["git", "show", "77d823d:" + bp], cwd=REPO, capture_output=True).stdout).hexdigest()
    L.append('ex:EI6_pagedata a backlog:ExecutorInstance ; rdfs:label "Executor session %s"@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief of register v0.167 (sen0401_lineage_brief_v1_2_0), session %s" ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
        SESS, SESS, pushed, end, lit("Started after the push of v0.170 (commit dd33f7a, %s UTC); the start time is that push, the earliest the session could begin, not a clock reading of the session; the register's start of the task precedes it and the framework's advisory on that stands, not waived. It ended with its last commit %s, %s UTC." % (pushed, COMMIT, end))))
    L.append('ex:Brief6_%s a backlog:ExecutorBrief ; rdfs:label "Brief of %s"@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:AC3L_Ch10 ; backlog:briefedExecutorInstance ex:EI6_pagedata ;\n    rdfs:comment %s .\n' % (
        TASK, TASK, TASK, lit("Generated from register v0.167 by sen0401_lineage_brief_v1_2_0.py and passed unedited by the coordinator; file %s as committed in 77d823d, SHA-256 %s." % (bp, bsha))))
    allf = FILES + sorted(os.path.relpath(p, REPO) for p in [os.path.join(ld, x) for x in os.listdir(ld)])
    ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values())
    for nn in CHS:
        ok, at, how = V[nn]
        L.append('ex:Ev6C_cmp_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:AC3L_Ch10, ex:AC3L_Ch11 ;\n    backlog:hasTestId "cmp:%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the test command" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            nn, lit("page-data builder v2_23_0 against v2_22_0, chapter %s" % nn), nn, SPEC, lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:AC3L_Ch10, ex:AC3L_Ch11 ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), f, C.sha(f), at))
    i, j = T.blk(t, TASK); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
    evs = ["Ev6C_cmp_Ch%s" % nn for nn in CHS]
    L.append(C.transition("Done6T_" + TASK, TASK, "T_Complete", end, "Done on the executor's commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMIT, end, nxt, now), TASK + " completed"))
    L.append('ex:Harness6C_%s a backlog:TestHarness ; rdfs:label "Checks run for %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TASK, TASK, TASK, ", ".join("ex:" + e for e in evs)))
    lines = "; ".join("%s: %s" % (nn, OUT[nn][-110:]) for nn in CHS[:2])
    L.append('ex:%s backlog:hasAcceptanceCriterion ex:AC3L_Ch10, ex:AC3L_Ch11 ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TASK, ", ".join("ex:" + e for e in evs) + ", " + ", ".join("ex:" + ver[f][0] for f in FILES),
             lit("Done, recorded %s: delivered by the executor session %s (commit %s, new file 08-tooling/sen0401_page_data_v2_23_0.py; v2_22_0 not edited). Control run on the evidence bridge, serial, all 14 chapters, comparison of the builder v2_23_0 with v2_22_0 (sen0401_lineage_pagedata_check v1_0_0): every comparison PASS; chapter 10 relations 79 -> 107 (28 added, 'operates on', each with property, category and the link's sentence), chapter 11 85 -> 117 (32 added); the other chapters have identical relations; every other key of the data equal (only the builder's version label differs). Logs in 08-tooling/verify/iter14/pagedata. Details: %s." % (now[:10], SESS, COMMIT, lines))))
    comment = "Control of Iter_14, page-data builder: the bridge compared the builder v2_23_0 with v2_22_0 serially on all 14 chapters; TK_SecLinks_PageData Done with bridge-verified evidence and a harness; executor instance and passed brief recorded as links."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment)))


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
