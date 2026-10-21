#!/usr/bin/env python3
"""sen0401_lineage_control v1_0_0 - the control of Iter_13 in the register, by the routes of the discipline (G113 every status change is a recorded transition; G136 plan, then execute, then control).
  plan    the executor instances and the briefs they received (links), the Build tasks Done with their finish, transitions and bridge-verified file evidence, the Verify tasks Ready (T_Refine),
          the stand-alone declarations of the four stories (standsAlone true), and the disclosures (start recorded before the executors started; the chapter 8 page built inside the chapter 8 examples task)
  start   the Verify tasks InProgress at the real clock (start gate READY for each), T_Start recorded
  result  (separate event, reads 08-tooling/verify/iter13/results.json) the Verify tasks Done with evidence, the criteria results, the change request for criterion element 3 of chapters 10 and 11
Usage: sen0401_lineage_control_v1_0_0.py plan|start|result"""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
H = os.path.dirname(os.path.abspath(__file__)); REPO = M.REPO
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
BRIDGE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_evidence_bridge_v1_1_0.py"
lit = T.lit if hasattr(T, "lit") else (lambda s: '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"')
# session, retired (last commit of the session, UTC), build task, files cited
SESS = {"ch08": ("SEN0401-I13-ch08-examples", "2026-10-21T12:10:35"), "ch10": ("SEN0401-I13-page-ch10", "2026-10-21T13:51:21"), "ch11": ("SEN0401-I13-page-ch11", "2026-10-21T15:51:48"),
        "ch12": ("SEN0401-I13-page-ch12", "2026-10-21T15:07:03"), "ch14": ("SEN0401-I13-page-ch14", "2026-10-21T12:10:03")}
REAL_START = "2026-10-21T08:33:00"
RESEARCH_DONE = "2026-10-21T08:42:32"   # commit 2956f32, chapter 8 research v1.2.0
BUILD = {  # task: (session key, criterion, finish UTC, commits, files)
    "TK_Ch08Ex_Build": ("ch08", "AC3T_Ch08_Examples", "2026-10-21T12:10:35", "2956f32 (research 1.2.0, 08:42 UTC), 7202593 (page 9.77.0), e11b877 (page test 9.34.0), e0e6057 (status notes)",
                        ["03-materials/ch08/rdodi/sen0401_ch08_research_v1_2_0.ttl", "03-materials/ch08/rdodi/sen0401_ch08_document_v1_2_0.ttl", "08-tooling/sen0401_ch08_verify_v1_2_0.py", "08-tooling/sen0401_ch08_rdodi_data_v1_2_0.py"]),
    "TK_PageTpl_Ch08_Build": ("ch08", "AC3T_Ch08", "2026-10-21T12:10:35", "7202593, e11b877, e0e6057 of the chapter 8 examples session",
                              ["03-materials/ch08/page/sen0401_ch08_page_v9_77_0.html", "03-materials/ch08/page/sen0401_ch08_page_abox_v9_77_0.ttl", "08-tooling/ch08-page/page_data_v9_77_0.json"]),
    "TK_PageTpl_Ch10_Build": ("ch10", "AC3T_Ch10", "2026-10-21T13:51:21", "2a20df6", None),
    "TK_PageTpl_Ch11_Build": ("ch11", "AC3T_Ch11", "2026-10-21T15:51:48", "8273751, e11eff8, 0fd3ba4", None),
    "TK_PageTpl_Ch12_Build": ("ch12", "AC3T_Ch12", "2026-10-21T15:07:03", "8bba5a6, a2cc373, 2d5939f, 78f7991, aa823d3", None),
    "TK_PageTpl_Ch14_Build": ("ch14", "AC3T_Ch14", "2026-10-21T12:10:03", "6ae28f9, b33f8dc", None)}
for k, v in list(BUILD.items()):
    if v[4] is None:
        n = v[0][2:]
        BUILD[k] = v[:4] + (["03-materials/ch%s/page/sen0401_ch%s_page_v9_77_0.html" % (n, n), "03-materials/ch%s/page/sen0401_ch%s_page_abox_v9_77_0.ttl" % (n, n), "08-tooling/ch%s-page/page_data_v9_77_0.json" % n],)
VERIFY = {"TK_Ch08Ex_Verify": ("TK_Ch08Ex_Build", "AC3T_Ch08_Examples"), "TK_PageTpl_Ch08_Verify": ("TK_PageTpl_Ch08_Build", "AC3T_Ch08"), "TK_PageTpl_Ch10_Verify": ("TK_PageTpl_Ch10_Build", "AC3T_Ch10"),
          "TK_PageTpl_Ch11_Verify": ("TK_PageTpl_Ch11_Build", "AC3T_Ch11"), "TK_PageTpl_Ch12_Verify": ("TK_PageTpl_Ch12_Build", "AC3T_Ch12"), "TK_PageTpl_Ch14_Verify": ("TK_PageTpl_Ch14_Build", "AC3T_Ch14")}
STORIES = ["ST_Gap_Stage3F", "ST_Gap_Stage4", "ST_Page_Template", "ST_Ch08_Examples"]
sha = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def tev(eid, label, item, kind_nodes):
    return ""


def transition(tid, item, via, at, note, label):
    return ('ex:%s a backlog:TransitionEvent ; rdfs:label %s@en ; backlog:transitionedItem ex:%s ;\n    backlog:viaTransition backlog:%s ; backlog:transitionedAt "%s"^^xsd:dateTime ; backlog:transitionedBy backlog:Builder ;\n'
            '    backlog:hasTransitionNote %s .\n' % (tid, lit(label), item, via, at, lit(note)))


def bridge_files(paths, now):
    """ArtifactEvidence nodes for the files, verified by the evidence bridge (SHA-256 against the file); returns {path: (id, verified)}"""
    draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    ids = {}
    for i, p in enumerate(sorted(set(paths))):
        eid = "Ev3C_File_%s" % hashlib.sha1(p.encode()).hexdigest()[:10]; ids[p] = eid
        draft.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" .\n' % (eid, lit(os.path.basename(p) + ", committed by the executor session"), p, sha(p)))
    d = tempfile.mkdtemp(); a = os.path.join(d, "draft.ttl"); b = os.path.join(d, "bridge.ttl"); open(a, "w").write("".join(draft))
    r = subprocess.run([sys.executable, BRIDGE, a, "--workspace", REPO, "-o", b], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-300:])
    import sen0401_lineage_successor_stages_v1_1_0 as S
    v = S.verdicts(b)
    return {p: (ids[p], v[ids[p]]) for p in ids}


def ev_plan(t):
    now = M.now(); L = []
    briefs = sorted(glob.glob(os.path.join(REPO, "08-tooling", "briefs", "iter13", "BRIEF_*.md")))
    # executor instances: one per session
    for key, (sess, retired) in SESS.items():
        L.append('ex:EI3_%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n'
                 '    rdfs:comment %s .\n' % (key, lit("Executor session " + sess), lit("brief of register v0.150 (sen0401_lineage_brief_v1_0_0), session " + sess), REAL_START, retired,
                 lit("Started after the commit of v0.151 (pushed 2026-10-21T08:32:56 UTC); the start time %s UTC is the coordinator's 'about 08:33', not a clock reading of the session itself; the first commit of the session is at most 08:34:03 UTC. It ended with its last commit, %s UTC. Named by the register's note on work begun and by the brief." % (REAL_START, retired))))
    # briefs: the five that were passed
    for tk in ["TK_Ch08Ex_Build", "TK_PageTpl_Ch10_Build", "TK_PageTpl_Ch11_Build", "TK_PageTpl_Ch12_Build", "TK_PageTpl_Ch14_Build"]:
        key, crit = BUILD[tk][0], BUILD[tk][1]; bp = "08-tooling/briefs/iter13/BRIEF_%s.md" % tk
        L.append('ex:Brief3_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI3_%s ;\n    rdfs:comment %s .\n' % (
            tk, lit("Brief of " + tk), tk, crit, key, lit("Generated from register v0.150 by sen0401_lineage_brief_v1_0_0.py and passed unedited by the coordinator; file %s, SHA-256 %s." % (bp, sha(bp)))))
    # the chapter 8 page task was never started in the register: its work is recorded as begun, afterwards, at the end of the research it needed
    i, j = T.blk(t, "TK_PageTpl_Ch08_Build"); bb = t[i:j]; assert "backlog:hasState backlog:Ready" in bb and "startedAt" not in bb
    t = t[:i] + bb.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % RESEARCH_DONE, 1) + t[j:]
    L.append(transition("Begin3T_TK_PageTpl_Ch08_Build", "TK_PageTpl_Ch08_Build", "T_Start", RESEARCH_DONE, "Recorded afterwards in v0.152 (%s UTC), as the control step found it: the page was built by the session SEN0401-I13-ch08-examples inside TK_Ch08Ex_Build, after its research v1.2.0 (commit 2956f32, %s UTC), because the page test 9.34.0 of the chapter needs the page on template 9.51.0. The task was not started in the register before the work, and its brief (generated, not passed) names no session." % (now, RESEARCH_DONE), "TK_PageTpl_Ch08_Build work recorded as begun afterwards"))
    # Verify tasks Ready (T_Refine)
    for vk, (bk, crit) in VERIFY.items():
        i, j = T.blk(t, vk); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, vk
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
        L.append(transition("Ready3T_" + vk, vk, "T_Refine", now, "Ready on %s: its Build task %s is finished by its executor (still InProgress in the register until the control run gives it test evidence: a Done task needs bridge-verified test evidence and a harness); the control run is planned before it starts: the machine is quiet, the checks run one after the other, a flaky budget failure is run again up to three times with every run kept, nothing is waived, no test, gate or threshold is changed, and every result is recorded as printed." % (now, bk), vk + " ready"))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s .\n' % (vk, crit))
    for s in STORIES:
        L.append('ex:%s backlog:standsAlone true .\n' % s)
    # disclosures
    for tk in ["TK_Ch08Ex_Build", "TK_PageTpl_Ch10_Build", "TK_PageTpl_Ch11_Build", "TK_PageTpl_Ch12_Build", "TK_PageTpl_Ch14_Build"]:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (tk, lit("Disclosure %s: the start of this task was recorded in v0.151 at 2026-10-21T08:24:15 UTC, but the executor session %s began about %s UTC after the commit of v0.151 (pushed 08:32:56 UTC); the register's start precedes the executor's by about 9 minutes. The framework's check (vi) of release 1.412.0 advises on this, and the advisory is left standing, not waived. The cause: the builder session took the instant of writing the version for the start and the coordinator started the sessions after the commit." % (now[:10], SESS[BUILD[tk][0]][0], REAL_START))))
    L.append('ex:TK_PageTpl_Ch08_Build backlog:hasAuditNote %s .\n' % lit("Decision %s on the overlap: the page of chapter 8 on template 9.51.0 (page 9.77.0, with its Stage 4 page ABox) was built by the session SEN0401-I13-ch08-examples inside TK_Ch08Ex_Build, because the page test 9.34.0 of that task needs it. The text of this task (a new page file on template 9.51.0 from the existing page data and the deck, tests run unchanged, Stage 4 page ABox built, nothing committed edited, no gate or test changed) is satisfied by that page, so this task is recorded Done on those commits and no second page is built. The brief of this task was generated and not passed; the one page serves both tasks and both criteria (AC3T_Ch08, AC3T_Ch08_Examples), each with its own Verify task." % now[:10]))
    T_ = t + "\n" + "".join(L)
    for s in STORIES[:0]:
        pass
    return X.set_status(T_, "LS_InProgress"), "Control of Iter_13, plan: executor instances and briefs recorded as links; the chapter 8 page task recorded as begun afterwards inside the chapter 8 examples session (overlap disclosed); Verify tasks Ready; stand-alone declarations as links; start-before-executor disclosed."


def ev_start(t):
    now = M.now()
    tmp = M.newest() + ".gate.tmp"; open(tmp, "w").write(t)
    try:
        for vk in VERIFY:
            r = subprocess.run([sys.executable, GATE, tmp, "--lineage", "Lineage3", "--item", vk], capture_output=True, text=True)
            assert "VERDICT     : READY" in r.stdout, vk + " " + r.stdout[-400:]
    finally:
        os.remove(tmp)
    L = []
    for vk in VERIFY:
        i, j = T.blk(t, vk); b = t[i:j]; assert "backlog:hasState backlog:Ready" in b and "startedAt" not in b, vk
        t = t[:i] + b.replace("backlog:hasState backlog:Ready", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        L.append(transition("Begin3T_" + vk, vk, "T_Start", now, "Control run begun %s UTC by the builder session, after the start gate said READY: the machine is quiet (no browser or test process), the checks of the criterion run one after the other, logs are kept in 08-tooling/verify/iter13/." % now, vk + " started"))
    print("STARTED", now)
    return t + "\n" + "".join(L), "Control of Iter_13, start: the Verify tasks InProgress at %s UTC after the start gate said READY for each; T_Start recorded." % now


def main():
    ev = sys.argv[1]; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    fn = {"plan": ev_plan, "start": ev_start}
    if ev not in fn:
        raise SystemExit(__doc__)
    nt, comment = fn[ev](t)
    print(os.path.basename(M.write_new(src, nt, nxt, cur, comment)))


if __name__ == "__main__":
    main()
