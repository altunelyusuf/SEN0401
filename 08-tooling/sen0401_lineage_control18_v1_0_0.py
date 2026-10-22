#!/usr/bin/env python3
"""sen0401_lineage_control18 v1_0_0 - the control of the two executor tasks of Iter_16 (G113, G136): TK_PageGates_Template and TK_PageGates_Test. The evidence bridge runs every element of AC3P_Template and AC3P_Test as an exit-code check
(sen0401_lineage_gate_check v1_0_0; the 9.35.1 runs of chapters 1 and 10 were run by the builder in 08-tooling/verify/iter16, serially, after the executors had reported) and verifies the delivered files by SHA-256.
The record: executor instances and briefs as links; the evidence per element; the criteria result element by element; the two tasks Done (T_Complete) with verified evidence and a harness; the click finding as a fact; a NEW sibling change request ex:CR3_PageClick with its impact
assessment and ONE plain owner question (a second change of the page tests); no execution task is created. Usage: sen0401_lineage_control18_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl18"; BRIDGE = C.BRIDGE; lit = C.lit
GC = "08-tooling/sen0401_lineage_gate_check_v1_0_0.py"
KINDS = [("tplnew", "tplnew"), ("tpldiff", "tpldiff"), ("overlap10", "overlap:10"), ("overlap11", "overlap:11"), ("clickfact", "clickfact"), ("nochangeT", "nochange:T"),
         ("testnew", "testnew"), ("testdiff", "testdiff"), ("testrun01", "testrun:01"), ("testrun10", "testrun:10"), ("nochangeS", "nochange:S")]
LABEL = {"tplnew": "template 9.51.1 is a new file, 9.51.0 byte-identical, version comment names 9.51.1", "tpldiff": "difference 9.51.0 to 9.51.1 limited to the version comment and the function rlUntangle",
         "overlap10": "chapter 10 concept map after drag and Untangle: no two boxes overlap on 9.51.1 (scratch build by the builder)", "overlap11": "chapter 11 concept map after drag and Untangle: no two boxes overlap on 9.51.1 (scratch build by the builder)",
         "clickfact": "the click timeout of chapter 11 is analysed as a fact: test sequence, control log and the executor's evidence", "nochangeT": "template task: no committed file edited (every file of its commit added)",
         "testnew": "tests 9.34.1 and 9.35.1 are new files, 9.34.0 and 9.35.0 byte-identical", "testdiff": "tests differ from the old only in version line, comments, HASMENT and the one assertion; feature texts equal",
         "testrun01": "test 9.35.1 on chapter 1 page 9.70.0 (builder's run): equal to the stored result", "testrun10": "test 9.35.1 on chapter 10 page 9.78.0 (builder's run): the mentioned-together assertion passes, no other failure than the template's overlap feature",
         "nochangeS": "test task: no committed file edited (every file of its commits added)"}
TASKS = {"TK_PageGates_Template": dict(crit="AC3P_Template", sess="SEN0401-I16-template", commits=["2654ae9"], kinds=["tplnew", "tpldiff", "overlap10", "overlap11", "clickfact", "nochangeT"],
                                      elems=[("(1) new file, old byte-identical", ["tplnew"]), ("(2) diff limited to the named layout code", ["tpldiff"]), ("(3) no overlap on chapters 10 and 11", ["overlap10", "overlap11"]), ("(4) click timeout analysed as a fact", ["clickfact"]), ("(5) nothing else changed", ["nochangeT"])]),
         "TK_PageGates_Test": dict(crit="AC3P_Test", sess="SEN0401-I16-test", commits=["a626896", "0cfd139", "aa9c24b"], kinds=["testnew", "testdiff", "testrun01", "testrun10", "nochangeS"],
                                   elems=[("(1) new files, old byte-identical", ["testnew"]), ("(2) diff limited to the one assertion", ["testdiff"]), ("(3) chapter 1 equal to stored, chapter 10 assertion passes", ["testrun01", "testrun10"]), ("(4) nothing else changed", ["nochangeS"])])}
START = "41280b4"
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter16")
QUESTION = ("May the new page-test versions 9.34.1 and 9.35.1 change a second thing: after dragging an entity in the ERD, the test clicks an entity that is not covered by another one (the first end of the first relationship that nothing lies on), so the chapter 11 page can be measured? (yes/no)")


def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True)
    draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
    for k, a in KINDS:
        draft.append('ex:Ev8C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), a, GC))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    cmd = "python3 -B {spec} {id} > %s/bridge_gate_$(echo {id} | tr '/:' '__').log 2>&1" % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-300:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); V = {k: v["Ev8C_" + k] for k, _ in KINDS}; OUT = {}
    for k, a in KINDS:
        lg = os.path.join(LOGDIR, "bridge_gate_%s.log" % a.replace("/", "_").replace(":", "_")); OUT[k] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:330] if os.path.exists(lg) else ""
    started = utc(START)
    for tk, d in TASKS.items():
        end = utc(d["commits"][-1]); d["end"] = end; bp = "08-tooling/briefs/iter16/BRIEF_%s.md" % tk; n = tk.split("_")[-1]
        L.append('ex:EI8_%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
            n, lit("Executor session " + d["sess"]), lit("brief of register v0.180, session " + d["sess"]), started, end,
            lit("Started after the push of v0.181 (commit %s, %s UTC), the earliest the session could begin; the register's start of the task (stamped 2026-10-22T06:54:06 UTC) precedes it by seconds and the framework's advisory on that stands, not waived. It ended with its last commit %s (%s UTC)." % (START, started, ", ".join(d["commits"]), end))))
        L.append('ex:Brief8_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI8_%s ;\n    rdfs:comment %s .\n' % (
            tk, lit("Brief of " + tk), tk, d["crit"], n, lit("Generated by sen0401_lineage_brief_gates_v1_0_0.py from register v0.180 and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = {tk: sorted({f for c in d["commits"] for f in git("show", "--name-only", "--format=", c).splitlines() if f}) for tk, d in TASKS.items()}
    logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "**", "*"), recursive=True) if os.path.isfile(p))
    allf = sorted({f for fs in files.values() for f in fs} | set(logs)); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, a in KINDS:
        ok, at, how = V[k]; crit = [d["crit"] for d in TASKS.values() if k in d["kinds"]][0]
        L.append('ex:Ev8C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            k, lit(LABEL[k]), crit, a, GC, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t: continue
        crits = [d["crit"] for tk, d in TASKS.items() if f in files[tk]] or ["AC3P_Test", "AC3P_Template"]
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), ", ".join("ex:" + c for c in crits), f, sha256(f), at))
    allmet = True
    for tk, d in TASKS.items():
        lines = []; bad = []
        for name, ks in d["elems"]:
            okk = all(V[k][0] for k in ks)
            if not okk: bad.append(name)
            lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[k][0] else "NOT verified", OUT[k][:240]) for k in ks)))
        d["met"] = not bad; allmet &= not bad
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (d["crit"], lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: %s." % (now[:10], nxt, " | ".join(lines), "MET: all elements are met" if not bad else "NOT MET: element(s) %s; nothing is waived" % ", ".join(bad)))))
        d["lines"] = lines
    FIND = ("FACT (measured by the executors SEN0401-I16-template and SEN0401-I16-test and confirmed by the control's check): the click timeout of the page of chapter 11 ('HeaderFields intercepts pointer events') is a TEST ARTEFACT, not the template layout. "
            "The test 9.35.0 (line 1261; 9.35.1 lines 1256-1263; 9.34.1 line 1259) drags the first ERD entity 120 px right and 70 px down over HeaderFields, GenesisQuirks and BackLinks, and then clicks the SAME entity (nth(_ti), the first end of the first relationship); HeaderFields, drawn later, covers it and intercepts the pointer. "
            "Before the drag no two entities overlap (16 entities, 0 pairs); the click works on chapter 10 because its first relationship starts at a different entity; template 9.51.1 gives the identical result, so no template change can remove it.")
    for tk, d in TASKS.items():
        i, j = T.blk(t, tk); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tk
        assert d["met"], tk + " criterion not met: not recorded Done"
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), d["end"], now), 1) + t[j:]
        evs = ["Ev8C_" + k for k in d["kinds"]]
        L.append(C.transition("Done8T_" + tk, tk, "T_Complete", d["end"], "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (d["commits"][-1], d["end"], nxt, now), tk + " completed"))
        L.append('ex:Harness8C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (tk, lit("Checks run for " + tk), tk, ", ".join("ex:" + e for e in evs)))
        extra = (" DONE WITH A FINDING: the text of this task asks to measure 'that the click no longer times out' on the scratch build; the premise (the timeout comes from the layout) is refuted by the measurement, so that sentence cannot be satisfied by a template; the criterion of the task, which asks the cause to be analysed and reported as a fact, is met. " + FIND) if tk == "TK_PageGates_Template" else \
                (" The assertion that the mentioned-together toggle removes relationships now applies by what the page has; on page 9.78.0 of chapter 10 it passes, and the one other failing feature is the concept-map overlap of the template 9.51.0, which the new template removes (control of TK_PageGates_Template). The chapter 11 page is still not measurable by 9.34.1 and 9.35.1 because of the click (see ex:CR3_PageClick).")
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (tk, d["crit"], ", ".join("ex:" + e for e in evs) + ", " + ", ".join("ex:" + ver[f][0] for f in files[tk] if ver[f][0]),
                 lit("Done, recorded %s: delivered by the executor session %s (commits %s); control run on the evidence bridge, serial, logs in 08-tooling/verify/iter16. Results as printed: %s.%s" % (now[:10], d["sess"], ", ".join(d["commits"]), " | ".join(d["lines"]), extra))))
    L.append('ex:TK_PageGates_Regression backlog:hasAuditNote %s .\n' % lit("Fact for the executor, found %s: stale temporary folders (/tmp/sen0401_page_test_* and /tmp/sen0401_fx_*) of earlier sessions filled the root disk to 28 MB free and crashed browser runs ('Target crashed', 'Page crashed') of the test task. Before each batch of runs, delete these folders when older than 60 minutes (find /tmp -maxdepth 1 -name 'sen0401_page_test_*' -mmin +60 and the same for sen0401_fx_*), check df, keep the logs. A crash with a full disk is not a result." % now[:10]))
    L.append('ex:ST_Page_Gates backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): TK_PageGates_Template and TK_PageGates_Test Done on bridge-verified evidence; AC3P_Template and AC3P_Test %s; AC3P_Regression waits for TK_PageGates_Regression. The story stays InProgress. %s" % (now[:10], nxt, "MET" if allmet else "not all met", FIND)))
    CR = "ex:CR3_PageClick"
    L.append('%s a backlog:ChangeRequest ;\n    rdfs:label "The page test clicks an entity it has just dragged under another one: may the new test versions change a second thing so the chapter 11 page can be measured?"@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_PageGates, ex:IA3_PageGates ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n' % (
        CR, lit("Found by the executors of Iter_16 and confirmed by the control %s. %s The owner's approval of ex:CR3_PageGates covers one change of the test (the assertion on mentioned-together relationships); this is a second, different change, so it is asked, not assumed. "
                "THE OWNER'S QUESTION: %s IF NO: the chapter 11 page cannot pass the page tests 9.34.1 and 9.35.1 (the run stops on the click), the criterion AC3L2_Ch11 stays unmet and the chapter 11 page stays as shipped (9.77.0). IF YES: new test versions 9.34.2 and 9.35.2 as new files beside 9.34.1 and 9.35.1 (which stay as built), a new task, a new criterion that the new versions differ from 9.34.1 and 9.35.1 only in that click and give them the same results on the regression pages, and the chapter 11 page then rebuilt and measured with them; the route is a revision from the Scope stage again (a test change is lifted by the owner one change at a time). Chapter 10 is not affected: its click works."
                % (now[:10], FIND, QUESTION))))
    L.append('ex:IA3_PageClick a backlog:ImpactAssessment ;\n    rdfs:label "What the second test change costs, measured before any decision"@en ;\n    backlog:analyzesRequest %s ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_PageGates ;\n    backlog:hasImpactStatement %s .\n' % (CR, lit(
        "Affected: AC3L2_Ch11 and, through it, TK_SecLinks_Ch11_Page and TK_SecLinks_Ch11_Verify, ST_Section_Links and ST_Page_Template (ex:AC3T_Ch11). Not affected: chapter 10 (its click works), the template 9.51.1, the tests 9.34.1 and 9.35.1 as built, the regression task TK_PageGates_Regression (which runs 9.34.1 and 9.35.1 on the other pages and may start now: no shipped page is a section-link page whose first relationship starts at a dragged entity that another covers; if one is, the regression reports it as a result), the Mission outcome, closureCommittedAt and the Achieved status of the third lineage. "
        "Cost of yes: a revision from the Scope stage (seven versions, about the cost of v0.174 to v0.180), one test task (two new files, one changed line each, one run each on chapters 1 and 11, about 20 minutes of machine time), a regression equality check of the new versions against the old on the regression pages (about 18 runs, 3 hours), then the chapter 11 page task. The ordering of the work in the iteration: the page tasks already wait for the regression task; the new test would be inserted before them. Cost of no: none in work; chapter 11's section links stay in the research but unmeasured on a page, and the ERD-label element of its criterion stays unmet. No execution task is created before the owner answers.")))
    comment = "Control of Iter_16, template and tests: the bridge ran every element of AC3P_Template and AC3P_Test; TK_PageGates_Template and TK_PageGates_Test Done on verified evidence and a harness; the click timeout of chapter 11 recorded as a fact (a test artefact, not the template); change request CR3_PageClick with impact assessment and one owner question; no execution task created. Mission outcome, closureCommittedAt and the Achieved status are untouched."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
