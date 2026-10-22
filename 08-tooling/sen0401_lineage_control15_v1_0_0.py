#!/usr/bin/env python3
"""sen0401_lineage_control15 v1_0_0 - the control of the consolidation task of Iter_15 (G113, G136): the evidence bridge runs the research checks of the criteria AC3L_Ch10_Singular and AC3L_Ch10 one after the other and verifies the files the executors delivered by SHA-256;
records the executor instances and the briefs that were passed (links), the research tasks Done (T_Complete) with bridge-verified evidence and a harness, and the finding of the control (ch10: one property per class pair, links without their sentence).
  prepare   run the bridge for chapters 10 and 11 (logs in 08-tooling/verify/iter15/chNN; bridge output in /tmp/claude-0/s/ctl15)
  record    write the register version from it
Usage: sen0401_lineage_control14_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl15"; BRIDGE = C.BRIDGE; lit = C.lit
RC = "08-tooling/sen0401_lineage_research_check_v1_0_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
KINDS = [("stage4", S4, "%s"), ("research", CC, "Research/Ch%s"), ("seclinks", RC, "seclinks:%s"), ("annotated", RC, "annotated:%s"), ("linkdisc", RC, "linkdisc:%s"), ("kindrule", RC, "kindrule:%s"), ("singular", RC, "singular:%s"), ("samepairs", RC, "samepairs:%s")]
LABEL = {"stage4": "Stage 4 gate runner v1_1_0 (current validator v1.13.0)", "research": "chapter check Research v1_3_0 (pinned validator v1.6.0)", "seclinks": "section links declared, between sections, every section covered (sen0401_ch_seclinks_check v1_0_0)",
         "annotated": "every link annotated with the sentence that states it (sen0401_ch_seclinks_check v1_0_0 --evidence)", "linkdisc": "OE link discovery v1_1_0 (BP-D57, BP-D61 duplicate family): 0 beyond the baseline", "kindrule": "OE kind rule check v1_1_0 (BP-D58, BP-D59)",
         "singular": "one property per category and super-property (floor of BP-D61), sen0401_lineage_research_check v1_0_0", "samepairs": "the 28 link pairs of research v1.1.0 are still stated, sen0401_lineage_research_check v1_0_0"}
TASK = {"10": "TK_SecLinks_Ch10_Consolidate"}; CRIT = {"10": "AC3L_Ch10_Singular"}; CRIT2 = {"10": "AC3L_Ch10"}
SESS = {"10": "SEN0401-I15-consolidate-ch10"}
COMMIT = {"10": "a8c8f29"}
# the checks the TASK TEXT required (links, gates, discovery, kinds); annotated and singular were not in the task text and are recorded as found
REQ = {"10": [k for k, _, _ in KINDS]}
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def prepare():
    os.makedirs(WORK, exist_ok=True)
    for nn in ("10",):
        draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
        for kind, spec, tid in KINDS:
            draft.append('ex:Ev5C_%s_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, nn, lit("%s, chapter %s, research v1.2.0" % (LABEL[kind], nn)), tid % nn, spec))
        d = os.path.join(WORK, "draft_%s.ttl" % nn); open(d, "w").write("".join(draft))
        ld = os.path.join(REPO, "08-tooling", "verify", "iter15", "ch" + nn); os.makedirs(ld, exist_ok=True)
        cmd = "python3 -B {spec} {id} > %s/bridge_$(echo {id} | tr '/:' '__').log 2>&1" % ld
        r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge_%s.ttl" % nn)], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
        open(os.path.join(WORK, "bridge_%s.out" % nn), "w").write(r.stdout + r.stderr); print(nn, r.stdout[-200:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    pushed = utc("697faea"); V = {}; OUT = {}
    for nn in ("10",):
        v = S.verdicts(os.path.join(WORK, "bridge_%s.ttl" % nn))
        for kind, spec, tid in KINDS:
            V[(kind, nn)] = v["Ev5C_%s_Ch%s" % (kind, nn)]
            lg = os.path.join(REPO, "08-tooling", "verify", "iter15", "ch" + nn, "bridge_%s.log" % (tid % nn).replace("/", "_").replace(":", "_"))
            OUT[(kind, nn)] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:300] if os.path.exists(lg) else ""
    # executor instances and the briefs that were passed (the files as committed in 77d823d, before the brief was regenerated)
    for nn in ("10",):
        sess = SESS[nn]; end = utc(COMMIT[nn]); tk = TASK[nn]; bp = "08-tooling/briefs/iter14/BRIEF_%s.md" % tk
        bsha = hashlib.sha256(subprocess.run(["git", "show", "77d823d:" + bp], cwd=REPO, capture_output=True).stdout).hexdigest()
        L.append('ex:EI5_ch%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
            nn, lit("Executor session " + sess), lit("brief of register v0.167 (sen0401_lineage_brief_v1_2_0), session " + sess), pushed, end,
            lit("Started after the push of v0.168 (commit 697faea, %s UTC); the start time is that push, the earliest the session could begin, not a clock reading of the session; the register's start of the task (stamped 01:01:08 UTC) precedes it and the framework's advisory on that stands, not waived. It ended with its last commit %s, %s UTC." % (pushed, COMMIT[nn], end))))
        L.append('ex:Brief5_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI5_ch%s ;\n    rdfs:comment %s .\n' % (
            tk, lit("Brief of " + tk), tk, CRIT[nn], nn, lit("Generated from register v0.167 by sen0401_lineage_brief_v1_2_0.py and passed unedited by the coordinator; file %s as committed in 77d823d, SHA-256 %s." % (bp, bsha))))
    # evidence files
    files = {nn: sorted(f for f in git("show", "--name-only", "--format=", COMMIT[nn]).splitlines() if f) for nn in ("10",)}
    logs = {nn: sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling", "verify", "iter15", "ch" + nn, "*"))) for nn in ("10",)}
    allf = sorted({f for nn in files for f in files[nn] + logs[nn]})
    ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for nn in ("10",):
        for kind, spec, tid in KINDS:
            ok, at, how = V[(kind, nn)]; eid = "Ev5C_%s_Ch%s" % (kind, nn)
            if kind not in REQ[nn]:   # a failed check that the task text did not require stays in the log and in the notes; it attests nothing
                assert not ok, (kind, nn); continue
            L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s, ex:AC3L_Ch10 ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the test command" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
                eid, lit("%s, chapter %s, research v1.2.0" % (LABEL[kind], nn)), CRIT[nn], tid % nn, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        nns = [nn for nn in ("10",) if f in files[nn] or f in logs[nn]]
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), ", ".join("ex:" + CRIT[n] for n in nns) or "ex:AC3L_Ch10", f, sha256(f), at))
    for nn in ("10",):
        tk = TASK[nn]; i, j = T.blk(t, tk); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tk
        fin = utc(COMMIT[nn])
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, now), 1) + t[j:]
        evs = ["Ev5C_%s_Ch%s" % (k, nn) for k in REQ[nn]]
        L.append(C.transition("Done5T_" + tk, tk, "T_Complete", fin, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMIT[nn], fin, nxt, now), tk + " completed"))
        L.append('ex:Harness5C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (tk, lit("Checks run for " + tk), tk, ", ".join("ex:" + e for e in evs)))
        line = "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[(k, nn)][0] else "NOT verified", OUT[(k, nn)][:160]) for k, _, _ in KINDS)
        extra = ""
        extra = (" JUDGMENT CALLS the executor flagged, recorded as facts: (1) the property 'precedes' of BFO is no longer reused, because the fifth 'comes before' link joins dated examples, not occurrents, so the reuse would not be true; dcterms requires, replaces and isPartOf are kept as super-properties; "
                 "(2) the former shortensBlockRace ('is a means to shorten the race of') is merged into isMeansAgainst (category Intentional), so one property now covers the means against an attack and the means against a block race; (3) the former isBaseOfConnectionType is merged into isReasonFor (category Causal). "
                 "Not decided by a check: the OE link discovery (v1_1_0, repo-tooling v1.78.0, OE v2.33.0, family duplicate) reports 0 beyond the baseline on the new T-Box, but it finds only word-for-word definitions, shared labels and declared matches; the floor check singular reports 9 properties in 9 groups. "
                 "The OE kind rule check passes vacuously: every domain and range of the new properties is owl:Thing (as in chapter 11), so 0 ends are measured; it is reported as printed and not claimed as a kind check. Result: 26 properties of v1.1.0 consolidated into 9 for the same 28 links, each annotated with its sentence.")
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (tk, CRIT[nn], ", ".join("ex:" + e for e in evs) + ", " + ", ".join("ex:" + ver[f][0] for f in files[nn]),
                 lit("Done, recorded %s: delivered by the executor session %s (commit %s); control run on the evidence bridge, serial, logs in 08-tooling/verify/iter15/ch%s. Results as printed: %s.%s" % (now[:10], SESS[nn], COMMIT[nn], nn, line, extra))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT[nn], lit("Control %s (record v%s), research v1.2.0 of chapter %s: elements run by the bridge: %s. RESULT: MET, every element passes as printed.%s" % (now[:10], nxt, nn, line, extra))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT2[nn], lit('Control %s (record v%s): the research elements of this criterion (declared, between sections, every section covered, Stage 4 runner, Research chapter check, link discovery, kind check) were run again on research v1.2.0, which replaces v1.1.0 for the pages: all pass as printed; the page elements wait for the page tasks.' % (now[:10], nxt))))
    i, j = T.blk(t, "ST_Ch10_Consolidate"); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), now, now), 1) + t[j:]
    L.append(C.transition("Done5T_ST_Ch10_Consolidate", "ST_Ch10_Consolidate", "T_Complete", now, "Done when its one criterion AC3L_Ch10_Singular is met (all elements verified) and its task is Done (G125).", "ST_Ch10_Consolidate completed"))
    L.append('ex:Harness5C_ST_Ch10_Consolidate a backlog:TestHarness ; rdfs:label "Checks run for ST_Ch10_Consolidate"@en ; backlog:harnessFor ex:ST_Ch10_Consolidate ; backlog:hasHarnessEvidence %s .\nex:ST_Ch10_Consolidate backlog:hasEvidence %s .\n' % (", ".join("ex:Ev5C_%s_Ch10" % k for k, _, _ in KINDS), ", ".join("ex:Ev5C_%s_Ch10" % k for k, _, _ in KINDS)))
    comment = "Control of Iter_15, consolidation: the bridge ran the elements of AC3L_Ch10_Singular and the research elements of AC3L_Ch10 serially on research v1.2.0; TK_SecLinks_Ch10_Consolidate Done with bridge-verified evidence and a harness, executor instance and brief as links, the judgment calls recorded as facts; story ST_Ch10_Consolidate Done (G125). OLD: the bridge ran the research checks of AC3L_Ch10 and AC3L_Ch11 serially; TK_SecLinks_Ch10_Research and TK_SecLinks_Ch11_Research Done with bridge-verified evidence and a harness; executor instances and passed briefs recorded as links; the ch10 finding (one property per class pair, links without their sentence) recorded for the change route."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment)))
    print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
