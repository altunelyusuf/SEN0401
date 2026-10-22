#!/usr/bin/env python3
"""sen0401_lineage_control20 v1_0_0 - the control of TK_SecLinks_Ch10_Page after its executor (session SEN0401-I14-page-ch10-r2) reported page 9.79.0 on template 9.51.1 and tests 9.34.1/9.35.1 (G113, G136).
The evidence bridge runs every element of AC3L2_Ch10 (and the AC3T_Ch10 elements on the new page) as an exit-code check (sen0401_lineage_page_check v1_2_0, a new file: v1_1_0 is hard-coded to page 9_78_0 and is not edited; the Stage 4 runner; the chapter checks);
the page tests were re-run by the builder, serially, with sen0401_lineage_verify_page v1_2_0 (logs in 08-tooling/verify/iter16/ch10). The record: the executor instance and its brief as links; the evidence per element; the criteria result element by element;
TK_SecLinks_Ch10_Page Done (T_Complete) with verified evidence and a harness; the Verify task made Ready (its dependency is Done); the story notes. ST_Section_Links and ST_Page_Template are NOT closed (chapter 11 is open). Nothing else is started.
Usage: sen0401_lineage_control20_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl20"; BRIDGE = C.BRIDGE; lit = C.lit
CHK = "08-tooling/sen0401_lineage_page_check_v1_2_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
KINDS = [("markers", CHK, "markers:10"), ("deck", CHK, "deck:10"), ("link", CHK, "link:10"), ("seclinks", CHK, "seclinks:10"), ("erd", CHK, "erd:10"), ("test34", CHK, "test34:10"), ("test35", CHK, "test35:10"),
         ("counts34", CHK, "counts34:10"), ("counts35", CHK, "counts35:10"), ("abox", CHK, "abox:10"), ("nochange", CHK, "nochange:10"), ("stage4", S4, "10"), ("research", CC, "Research/Ch10"), ("deckchk", CC, "Deck/Ch10"), ("pagechk", CC, "Page/Ch10")]
LABEL = {"markers": "template markers in the page HTML", "deck": "deck match: 0 not carried", "link": "link check: 0 not carried", "seclinks": "section links declared between sections, every section covered",
         "erd": "page test 9.35.1: both ERD label features run with no skip and pass, labels shown after Untangle at least 95 percent", "test34": "page test 9.34.1: no failure", "test35": "page test 9.35.1: no failure",
         "counts34": "page test 9.34.1 counts against the stored result of page 9.77.0", "counts35": "page test 9.35.1 counts against the stored result of page 9.77.0", "abox": "Stage 4 page ABox and stored page-test result exist as new files for page 9.79.0",
         "nochange": "no committed file edited by the executor (every file of its five commits added)", "stage4": "Stage 4 gate runner v1_1_0 (current validator v1.13.0)", "research": "chapter check Research v1_3_0 (pinned validator v1.6.0)",
         "deckchk": "chapter check Deck", "pagechk": "chapter check Page"}
ELEM = [("(1) links", ["seclinks"]), ("(2) ERD", ["erd"]), ("(3) gates", ["stage4", "research", "deckchk", "pagechk"]), ("(4) AC3T elements", ["markers", "deck", "erd", "test34", "test35", "counts34", "counts35", "abox"]), ("(5) nothing changed", ["nochange"])]
AC3T = ["markers", "deck", "erd", "test34", "test35", "counts34", "counts35", "abox"]
COMMITS = ["b1943e7", "8386e4a", "2f2e9b7", "e8bdc14", "23e155f"]; TK = "TK_SecLinks_Ch10_Page"; VT = "TK_SecLinks_Ch10_Verify"; CRIT = "AC3L2_Ch10"; TCRIT = "AC3T_Ch10"; SESS = "SEN0401-I14-page-ch10-r2"
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter16", "ch10")
PRE = "@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"


def prepare():
    os.makedirs(WORK, exist_ok=True); draft = [PRE]
    for kind, spec, tid in KINDS:
        draft.append('ex:Ev20C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, lit("%s, chapter 10, page 9.79.0" % LABEL[kind]), tid, spec))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    cmd = "python3 -B {spec} {id} > %s/bridge_page_$(echo {id} | tr '/:' '__').log 2>&1" % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-400:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); V = {k: v["Ev20C_" + k] for k, _, _ in KINDS}; OUT = {}
    for kind, spec, tid in KINDS:
        lg = os.path.join(LOGDIR, "bridge_page_%s.log" % tid.replace("/", "_").replace(":", "_")); OUT[kind] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:300] if os.path.exists(lg) else ""
    resumed = re.search(r'ex:Resume9T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); bp = "08-tooling/briefs/iter16/BRIEF_%s.md" % TK
    L.append('ex:EI20_ch10 a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
        lit("Executor session " + SESS), lit("brief of register v0.185, session " + SESS), resumed, end,
        lit("Started at the resume of the task (T_Resume, %s UTC, register v0.185) and ended with its last commit %s (%s UTC); %d commits. It reported that the tests passed on the first run and that the wrapper sen0401_lineage_page_check_v1_1_0.py is hard-coded to 9_78_0, so it ran the underlying tools directly (a new wrapper version v1_2_0 is the builder's)." % (resumed, COMMITS[-1], end, len(COMMITS)))))
    L.append('ex:Brief20_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI20_ch10 ;\n    rdfs:comment %s .\n' % (
        TK, lit("Brief of " + TK + " for the resumed task"), TK, CRIT, lit("Generated by sen0401_lineage_brief_gates_v1_2_0 from register v0.184 and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f})
    logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "*")) if os.path.isfile(p))
    tools = ["08-tooling/sen0401_lineage_page_check_v1_2_0.py", "08-tooling/sen0401_lineage_verify_page_v1_2_0.py"]
    allf = sorted(set(files) | set(logs) | set(tools)); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for kind, spec, tid in KINDS:
        ok, at, how = V[kind]; crits = [CRIT] + ([TCRIT] if kind in AC3T else [])
        L.append('ex:Ev20C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            kind, lit("%s, chapter 10, page 9.79.0" % LABEL[kind]), ", ".join("ex:" + c for c in crits), tid, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t: continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, kinds in ELEM:
        okk = all(V[k][0] for k in kinds)
        if not okk: bad.append(name)
        lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[k][0] else "NOT verified", OUT[k][:200]) for k in kinds)))
    assert not bad, "criterion not met, not recorded Done: %s" % bad
    DEV = ("DEVIATION disclosed, not waived: the wrapper sen0401_lineage_page_check_v1_1_0.py is hard-coded to page 9_78_0, so the executor ran the underlying tools directly; the control wrote a new wrapper version v1_2_0 (page 9_79_0, tests 9.34.1 and 9.35.1) and ran every element through it on the bridge. "
           "The brief text carried the register's older sentence naming template 9.51.0 and tests 9.34.0/9.35.0 in the task note; the brief's own later lines name 9.51.1 and 9.34.1/9.35.1 and the executor followed them (template markers present, tests 9.34.1/9.35.1 run).")
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), page 9.79.0 of chapter 10, every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. The page tests 9.34.1 and 9.35.1 were re-run by the builder, serially, in 08-tooling/verify/iter16/ch10 (the executor's own runs: 370 passed, 0 failed each). %s" % (now[:10], nxt, " | ".join(lines), DEV))))
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (TCRIT, lit("Control %s (record v%s), the elements of this criterion measured on the NEW page 9.79.0 of chapter 10 (the criterion text names page 9.77.0 and the tests 9.34.0/9.35.0; the new tests differ from them only in the one named assertion, proved by AC3P_Test): %s. All are met on the new page. The criterion is not edited; the story ST_Page_Template stays InProgress because AC3T_Ch11 is not met." % (now[:10], nxt, " | ".join(l for l in lines if l.startswith("(4)"))))))
    ex = ["Ev20C_" + k for k, _, _ in KINDS]
    i, j = T.blk(t, TK); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
    L.append(C.transition("Done20T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
    L.append('ex:Harness20C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
    L.append('ex:%s backlog:hasAcceptanceCriterion ex:AC3L2_Ch10 ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files),
             lit("Done, recorded %s: delivered by the executor session %s (%d commits %s to %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), COMMITS[0], COMMITS[-1], CRIT, DEV))))
    ev = "Control %s (record v%s): TK_SecLinks_Ch10_Page is Done (AC3L2_Ch10 MET, AC3T_Ch10 elements met on page 9.79.0)." % (now[:10], nxt)
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (VT, lit("Control %s (record v%s): its dependency %s is now Done; the task becomes startable (it is made Ready and started in the next versions, after the start gate), and the verification it asks for is run by the bridge in its own run." % (now[:10], nxt, TK))))
    L.append('ex:ST_Section_Links backlog:hasAuditNote %s .\n' % lit(ev + " The story is NOT closed: it stays InProgress because AC3L2_Ch11 is not met (TK_SecLinks_Ch11_Page is Suspended until the owner answers ex:CR3_PageClick), and its Verify tasks are not Done (G125: Done only when every criterion is met)."))
    L.append('ex:ST_Page_Template backlog:hasAuditNote %s .\n' % lit(ev + " The story is NOT closed: criteria met are AC3T_Ch08, AC3T_Ch10 (on the new page), AC3T_Ch12, AC3T_Ch14; AC3T_Ch11 is not met, so by G125 it stays InProgress. The criteria are not edited."))
    comment = "Control of Iter_14, chapter 10 page 9.79.0: the bridge ran every element of AC3L2_Ch10 and the AC3T_Ch10 elements through the new wrapper v1_2_0; the page tests 9.34.1/9.35.1 re-run serially; all met; TK_SecLinks_Ch10_Page Done on verified evidence and a harness; the executor instance and brief as links; one disclosed deviation; ST_Section_Links and ST_Page_Template not closed (chapter 11 open). Mission outcome, closureCommittedAt and the Achieved status untouched."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
