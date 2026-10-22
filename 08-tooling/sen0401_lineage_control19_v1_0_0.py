#!/usr/bin/env python3
"""sen0401_lineage_control19 v1_0_0 - the control of the regression task of Iter_16 (G113, G136): TK_PageGates_Regression. The evidence bridge runs every element of AC3P_Regression as an exit-code check
(sen0401_lineage_gate_check v1_1_0: the 36 kept runs against the stored results, written again from the criterion text; the rebuilt pages; no committed file of before the task edited; the control's own serial reruns of a sample) and verifies the delivered files by SHA-256.
The record: the executor instance and its brief as links; the evidence per element; the criterion result element by element; the task Done (T_Complete) with verified evidence and a harness; the story note. Nothing else is created or started.
Usage: sen0401_lineage_control19_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl19"; BRIDGE = C.BRIDGE; lit = C.lit
GC = "08-tooling/sen0401_lineage_gate_check_v1_1_0.py"
KINDS = [("reg35", "regress:9_35_1"), ("reg34", "regress:9_34_1"), ("rebuilt", "rebuilt"), ("nochange", "nochange:R"), ("rerun", "rerun")]
LABEL = {"reg35": "page test 9.35.1: the 14 shipped pages and the rebuilt chapters 1, 8, 12 and 14 (18 kept runs) each equal to or better than the stored result",
         "reg34": "page test 9.34.1: the same 18 pages (18 kept runs) each equal to or better than the stored result",
         "rebuilt": "chapters 1, 8, 12 and 14 rebuilt as 9.80.0 on template 9.51.1 with builder v4_14_0 (PAGE_TEMPLATE) in a scratch tree, none shipped",
         "nochange": "no file that existed before the task is edited, no gate, test, template, stored result or page differs, no 9.80.0 page in the repository (one own output appended to: disclosed)",
         "rerun": "the control's own serial reruns of a sample (chapter 13 and chapter 11 shipped pages, chapter 14 rebuilt) give the same widgets, features, skipped features and gates as the executor's runs and the stored results"}
ELEMS = [("(1) test 9.35.1 and (2) test 9.34.1 on the 14 shipped pages: equal to or better than the stored result, mentions identical in failed and skipped", ["reg35", "reg34"]),
         ("(3) chapters 1, 8, 12 and 14 rebuilt on template 9.51.1 with the builder v4_14_0, tested, equal to or better; scratch pages not shipped", ["rebuilt"]),
         ("(4) a committed file is never edited, nothing beyond the named new files", ["nochange"]),
         ("(5) the control's own reruns agree (a sample, serial)", ["rerun"])]
START = "02bc3a3"
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter16", "regress")
TK = "TK_PageGates_Regression"; CRIT = "AC3P_Regression"; SESS = "SEN0401-I16-regression"


def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True)
    draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for k, a in KINDS:
        draft.append('ex:Ev9C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), a, GC))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    cmd = "python3 -B {spec} {id} > %s/bridge_gate_$(echo {id} | tr '/:' '__').log 2>&1" % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-300:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); V = {k: v["Ev9C_" + k] for k, _ in KINDS}; OUT = {}
    for k, a in KINDS:
        lg = os.path.join(LOGDIR, "bridge_gate_%s.log" % a.replace("/", "_").replace(":", "_")); OUT[k] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:330] if os.path.exists(lg) else ""
    commits = git("rev-list", "--reverse", START + "..b903613").split(); started = utc(START); end = utc("b903613")
    bp = "08-tooling/briefs/iter16/BRIEF_%s.md" % TK
    L.append('ex:EI9_Regression a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
        lit("Executor session " + SESS), lit("brief of register v0.183, session " + SESS), started, end,
        lit("Started after the push of v0.183 (commit %s, %s UTC), the earliest the session could begin; the register's start of the task (stamped 2026-10-22T08:21:33 UTC) precedes it by seconds and the framework's advisory on that stands, not waived. It ended with its last commit b903613 (%s UTC); %d commits." % (START, started, end, len(commits)))))
    L.append('ex:Brief9_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI9_Regression ;\n    rdfs:comment %s .\n' % (
        TK, lit("Brief of " + TK), TK, CRIT, lit("Generated by sen0401_lineage_brief_gates from register v0.183 and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    evdir = "08-tooling/page-gates-evidence/regression/"
    files = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, evdir, "*")) if os.path.isfile(p))
    logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "**", "*"), recursive=True) if os.path.isfile(p))
    allf = sorted(set(files) | set(logs) | {GC}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, a in KINDS:
        ok, at, how = V[k]
        L.append('ex:Ev9C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            k, lit(LABEL[k]), CRIT, a, GC, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t: continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, ks in ELEMS:
        okk = all(V[k][0] for k in ks)
        if not okk: bad.append(name)
        lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[k][0] else "NOT verified", OUT[k][:240]) for k in ks)))
    assert not bad, "criterion not met: not recorded Done: %s" % bad
    DEV = ("DEVIATION disclosed, not waived: the executor appended the rows of the rebuilt chapters to its own table R16_table_9_35_1.md after committing it (commit b903613); the criterion says every output is a new file. The file is its own output of this task, "
           "not a gate, a test, a template, a stored result or a page, and the stop condition of the criterion names an edit 'beyond the named new files'; no result depends on it, because the control computed the comparison again from the kept logs (elements 1 to 3) and the earlier commit holds the table as first written.")
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met; %s Sample rerun: the control reran serially, by itself, chapter 13 page 9.69.0 with test 9.35.1, chapter 11 page 9.77.0 with test 9.34.1 and chapter 14 rebuilt as 9.80.0 with test 9.34.1; logs in 08-tooling/verify/iter16/regress. "
                                                    "Why a sample and not all 36: the criterion asks the executor to run, keep and compare; the control re-checks every kept run (36 of 36) by an independent comparison and re-executes the runs of the three classes in which the new test or template can differ from the old (a shipped page with mentions skipped, the chapter the pending change request is about, a page rebuilt on 9.51.1); the other shipped pages differ from the old runs by the test lines proved identical by AC3P_Test. Nothing is waived." % (now[:10], nxt, " | ".join(lines), DEV))))
    ex = ["Ev9C_" + k for k, _ in KINDS]
    i, j = T.blk(t, TK); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
    L.append(C.transition("Done9T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit b903613 (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (end, nxt, now), TK + " completed"))
    L.append('ex:Harness9C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
    L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files),
             lit("Done, recorded %s: delivered by the executor session %s (%d commits %s to b903613, 36 runs, all RESULT: PASS); control run on the evidence bridge, serial, logs in 08-tooling/verify/iter16/regress. Results as printed: %s. %s" % (now[:10], SESS, len(commits), commits[0], " | ".join(lines), DEV))))
    L.append('ex:ST_Page_Gates backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): TK_PageGates_Regression Done on bridge-verified evidence; AC3P_Template, AC3P_Test and AC3P_Regression are MET, so the template 9.51.1 and the tests 9.34.1 and 9.35.1 are proven for the page tasks. Chapter 11 remains unmeasurable by them (the click, ex:CR3_PageClick, pending). The story is not completed in this record." % (now[:10], nxt)))
    L.append('ex:ST_Section_Links backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): the page gates are proven (AC3P_Regression MET). TK_SecLinks_Ch10_Page can resume (T_Resume) on template 9.51.1 and tests 9.34.1/9.35.1 against AC3L2_Ch10. TK_SecLinks_Ch11_Page stays Suspended until the owner answers ex:CR3_PageClick." % (now[:10], nxt)))
    comment = "Control of Iter_16, regression: the bridge ran every element of AC3P_Regression (36 kept runs compared again, rebuilt pages, no edit of a committed file of before the task, the control's own serial reruns); TK_PageGates_Regression Done on verified evidence and a harness; the executor instance and brief as links; one disclosed deviation (an own output appended to). Nothing started; the Mission outcome, closureCommittedAt and the Achieved status are untouched."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
