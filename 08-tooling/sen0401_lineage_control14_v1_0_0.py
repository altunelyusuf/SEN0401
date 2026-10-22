#!/usr/bin/env python3
"""sen0401_lineage_control14 v1_0_0 - the control of the two research tasks of Iter_14 (G113, G136): the evidence bridge runs the research checks of the criteria AC3L_Ch10 and AC3L_Ch11 one after the other and verifies the files the executors delivered by SHA-256;
records the executor instances and the briefs that were passed (links), the research tasks Done (T_Complete) with bridge-verified evidence and a harness, and the finding of the control (ch10: one property per class pair, links without their sentence).
  prepare   run the bridge for chapters 10 and 11 (logs in 08-tooling/verify/iter14/chNN; bridge output in /tmp/claude-0/s/ctl14)
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
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl14"; BRIDGE = C.BRIDGE; lit = C.lit
RC = "08-tooling/sen0401_lineage_research_check_v1_0_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
KINDS = [("stage4", S4, "%s"), ("research", CC, "Research/Ch%s"), ("seclinks", RC, "seclinks:%s"), ("annotated", RC, "annotated:%s"), ("linkdisc", RC, "linkdisc:%s"), ("kindrule", RC, "kindrule:%s"), ("singular", RC, "singular:%s")]
LABEL = {"stage4": "Stage 4 gate runner v1_1_0 (current validator v1.13.0)", "research": "chapter check Research v1_3_0 (pinned validator v1.6.0)", "seclinks": "section links declared, between sections, every section covered (sen0401_ch_seclinks_check v1_0_0)",
         "annotated": "every link annotated with the sentence that states it (sen0401_ch_seclinks_check v1_0_0 --evidence)", "linkdisc": "OE link discovery v1_1_0 (BP-D57, BP-D61 duplicate family): 0 beyond the baseline", "kindrule": "OE kind rule check v1_1_0 (BP-D58, BP-D59)",
         "singular": "one property per category and super-property (floor of BP-D61), sen0401_lineage_research_check v1_0_0"}
TASK = {"10": "TK_SecLinks_Ch10_Research", "11": "TK_SecLinks_Ch11_Research"}; CRIT = {"10": "AC3L_Ch10", "11": "AC3L_Ch11"}
SESS = {"10": "SEN0401-I14-research-ch10", "11": "SEN0401-I14-research-ch11"}
COMMIT = {"10": "d4dda4c", "11": "4a2f709"}
# the checks the TASK TEXT required (links, gates, discovery, kinds); annotated and singular were not in the task text and are recorded as found
REQ = {"10": ["stage4", "research", "seclinks", "linkdisc", "kindrule"], "11": ["stage4", "research", "seclinks", "linkdisc", "kindrule", "annotated", "singular"]}
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def prepare():
    os.makedirs(WORK, exist_ok=True)
    for nn in ("10", "11"):
        draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
        for kind, spec, tid in KINDS:
            draft.append('ex:Ev4C_%s_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, nn, lit("%s, chapter %s, research v1.1.0" % (LABEL[kind], nn)), tid % nn, spec))
        d = os.path.join(WORK, "draft_%s.ttl" % nn); open(d, "w").write("".join(draft))
        ld = os.path.join(REPO, "08-tooling", "verify", "iter14", "ch" + nn); os.makedirs(ld, exist_ok=True)
        cmd = "python3 -B {spec} {id} > %s/bridge_$(echo {id} | tr '/:' '__').log 2>&1" % ld
        r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge_%s.ttl" % nn)], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
        open(os.path.join(WORK, "bridge_%s.out" % nn), "w").write(r.stdout + r.stderr); print(nn, r.stdout[-200:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    pushed = utc("a2cf4f6"); V = {}; OUT = {}
    for nn in ("10", "11"):
        v = S.verdicts(os.path.join(WORK, "bridge_%s.ttl" % nn))
        for kind, spec, tid in KINDS:
            V[(kind, nn)] = v["Ev4C_%s_Ch%s" % (kind, nn)]
            lg = os.path.join(REPO, "08-tooling", "verify", "iter14", "ch" + nn, "bridge_%s.log" % (tid % nn).replace("/", "_").replace(":", "_"))
            OUT[(kind, nn)] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:300] if os.path.exists(lg) else ""
    # executor instances and the briefs that were passed (the files as committed in 000288a, before the brief was regenerated)
    for nn in ("10", "11"):
        sess = SESS[nn]; end = utc(COMMIT[nn]); tk = TASK[nn]; bp = "08-tooling/briefs/iter14/BRIEF_%s.md" % tk
        bsha = hashlib.sha256(subprocess.run(["git", "show", "000288a:" + bp], cwd=REPO, capture_output=True).stdout).hexdigest()
        L.append('ex:EI4_ch%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
            nn, lit("Executor session " + sess), lit("brief of register v0.161 (sen0401_lineage_brief_v1_1_0), session " + sess), pushed, end,
            lit("Started after the push of v0.162 (commit a2cf4f6, %s UTC); the start time is that push, the earliest the session could begin, not a clock reading of the session; the register's start of the task (stamped %s UTC) precedes it by seconds and the framework's advisory on that stands, not waived. It ended with its last commit %s, %s UTC." % (pushed, "23:42:23", COMMIT[nn], end))))
        L.append('ex:Brief4_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI4_ch%s ;\n    rdfs:comment %s .\n' % (
            tk, lit("Brief of " + tk), tk, CRIT[nn], nn, lit("Generated from register v0.161 by sen0401_lineage_brief_v1_1_0.py and passed unedited by the coordinator; file %s as committed in 000288a, SHA-256 %s." % (bp, bsha))))
    # evidence files
    files = {nn: sorted(f for f in git("show", "--name-only", "--format=", COMMIT[nn]).splitlines() if f) for nn in ("10", "11")}
    logs = {nn: sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling", "verify", "iter14", "ch" + nn, "*"))) for nn in ("10", "11")}
    allf = sorted({f for nn in files for f in files[nn] + logs[nn]})
    ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for nn in ("10", "11"):
        for kind, spec, tid in KINDS:
            ok, at, how = V[(kind, nn)]; eid = "Ev4C_%s_Ch%s" % (kind, nn)
            if kind not in REQ[nn]:   # a failed check that the task text did not require stays in the log and in the notes; it attests nothing
                assert not ok, (kind, nn); continue
            L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the test command" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
                eid, lit("%s, chapter %s, research v1.1.0" % (LABEL[kind], nn)), CRIT[nn], tid % nn, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        nns = [nn for nn in ("10", "11") if f in files[nn] or f in logs[nn]]
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), ", ".join("ex:" + CRIT[n] for n in nns) or "ex:AC3L_Ch10", f, sha256(f), at))
    for nn in ("10", "11"):
        tk = TASK[nn]; i, j = T.blk(t, tk); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tk
        fin = utc(COMMIT[nn])
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, now), 1) + t[j:]
        evs = ["Ev4C_%s_Ch%s" % (k, nn) for k in REQ[nn]]
        L.append(C.transition("Done4T_" + tk, tk, "T_Complete", fin, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMIT[nn], fin, nxt, now), tk + " completed"))
        L.append('ex:Harness4C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (tk, lit("Checks run for " + tk), tk, ", ".join("ex:" + e for e in evs)))
        line = "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[(k, nn)][0] else "NOT verified", OUT[(k, nn)][:160]) for k, _, _ in KINDS)
        extra = ""
        if nn == "10":
            extra = (" FINDING of the control (not an element of this task's text): (a) the research states one property per class pair, 26 properties for 28 links, with the same meaning stated more than once (five 'precedes' variants, six requirement variants, five comparison variants, two 'defend against an attack' variants): the owner's standing rule of 2026-10-21 is that real equals are one property with several labels (OE v2.27.0 BP-D61, v2.28.0 duplicate detector rule S6); "
                     "the OE link discovery passes because it compares definitions word for word and finds no identical one, so it does not see this; the floor check 'singular' fails (groups of 4, 2, 5, 6 and 5 properties in one category and super-property); (b) the links carry no sentence that states them (0 of 28 annotated, chapter 11: 32 of 32). Both are repaired by a new task in the change route of the next versions, not by editing this delivery. Cause on the builder side: the brief generated for this task did not carry BP-D61 or the singularity rule; the brief tool v1_1_0 omitted it.")
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (tk, CRIT[nn], ", ".join("ex:" + e for e in evs) + ", " + ", ".join("ex:" + ver[f][0] for f in files[nn]),
                 lit("Done, recorded %s: delivered by the executor session %s (commit %s); control run on the evidence bridge, serial, logs in 08-tooling/verify/iter14/ch%s. Results as printed: %s.%s" % (now[:10], SESS[nn], COMMIT[nn], nn, line, extra))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT[nn], lit("Control %s (record v%s), research v1.1.0 of chapter %s: elements run by the bridge: %s. The criterion is not met yet: its page elements wait for the page tasks; the story stays InProgress.%s" % (now[:10], nxt, nn, line, extra))))
    comment = "Control of Iter_14, research: the bridge ran the research checks of AC3L_Ch10 and AC3L_Ch11 serially; TK_SecLinks_Ch10_Research and TK_SecLinks_Ch11_Research Done with bridge-verified evidence and a harness; executor instances and passed briefs recorded as links; the ch10 finding (one property per class pair, links without their sentence) recorded for the change route."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment)))
    print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
