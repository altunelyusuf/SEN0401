#!/usr/bin/env python3
"""sen0401_lineage_control28 v1_0_0 - the control of TK_Repair_Template (session SEN0401-I18-template; commits a99c4ab, d9c1b9e, 5c0da3a, 5fd840e; criterion AC5R_Template, page template 9.52.1) after its executor reported (G113, G136).
The evidence bridge runs every element as an exit-code check (sen0401_template_check v1_0_0, a new tool). The scratch pages of chapters 5, 1 and 10 on template 9.52.1 were BUILT and TESTED AGAIN by the builder (logs in 08-tooling/verify/iter18/template),
not read from the executor's logs. Met: the Build task Done and the Verify task TK_Repair_Template_Verify made Ready, started and Done in the same version (same runs, disclosed). Not met: the Build task Suspended with a rationale.
Usage: sen0401_lineage_control28_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control27_v1_0_0 as K27
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TC = "08-tooling/sen0401_template_check_v1_0_0.py"; GATE = K27.GATE; git = K27.git; utc = K27.utc; sha256 = K27.sha256; PRE = K27.PRE
TK = "TK_Repair_Template"; VT = "TK_Repair_Template_Verify"; CRIT = "AC5R_Template"; SESS = "SEN0401-I18-template"; COMMITS = ["a99c4ab", "d9c1b9e", "5c0da3a", "5fd840e"]
KINDS = [("nochange", "nochange:" + ",".join(COMMITS)), ("ident", "ident"), ("diff", "diff"), ("chip", "chip:05"), ("pf01", "pf:01"), ("pf10", "pf:10")]
LABEL = {"nochange": "the executor's four commits add files only, no committed file edited, no gate, test or threshold changed", "ident": "template 9.52.0 byte-identical (committed once, clean against HEAD, SHA-256 as recorded); template 9.52.1 a new file with the recorded SHA-256",
         "diff": "the diff of 9.52.1 over 9.52.0 is the version line and the story-chip click handler line only; every id and data- hook of 9.52.0 is in 9.52.1",
         "chip": "RUN by the builder: a scratch page of chapter 5 built on 9.52.1 with builders v4_15_0 and v2_24_0 passes the story chip feature (story GoxColdFind) in page tests 9.36.0 and 9.35.1, exit 0, no [FAIL] line",
         "pf01": "RUN by the builder: a scratch page of chapter 1 on 9.52.1 passes page test 9.36.0 P1 P3 P4 P5 P6 P8 P9", "pf10": "RUN by the builder: a scratch page of chapter 10 on 9.52.1 (executor's fixture manifest) passes page test 9.36.0 P1 P3 P4 P5 P6 P8 P9"}
ELEM = [("(1) new file, 9.52.0 byte-identical", ["ident", "nochange"]), ("(2) diff is the story-chip handler and the version marker only, ids and hooks present", ["diff"]), ("(3) scratch page of chapter 5: story chip passes in 9.36.0 and 9.35.1, no failure", ["chip"]),
        ("(4) scratch pages of chapters 1 and 10 pass P1 P3 P4 P5 P6 P8 P9", ["pf01", "pf10"]), ("(5) no committed file edited, no gate, test or threshold changed", ["nochange"])]
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter18", "template_bridge"); WORK = "/tmp/claude-0/s/ctl28"
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); draft = [PRE]
    for k, tid in KINDS: draft.append('ex:Ev28_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), tid, TC))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-200:])
def lastline(tid):
    p = os.path.join(LOGDIR, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100])
    return " ".join(open(p, encoding="utf-8", errors="replace").read().split())[:420] if os.path.exists(p) else "(log missing)"
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; v = S.verdicts(WORK + "/bridge.ttl"); V = {k: v["Ev28_" + k] for k, _ in KINDS}; OUT = {k: lastline(i) for k, i in KINDS}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); EI = "EI28_" + TK; bp = "08-tooling/briefs/iter18/BRIEF_%s.md" % TK
    L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + SESS), lit("brief of register v0.212"), began, end, lit("Started at the recorded work begun (T_Start, %s UTC, register v0.213) and ended with its last commit %s (%s UTC); %d commits: %s." % (began, COMMITS[-1], end, len(COMMITS), ", ".join(COMMITS)))))
    L.append('ex:Brief28%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_2_0 from register v0.212; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling/verify/iter18/template/*")) + glob.glob(LOGDIR + "/*") if os.path.isfile(p))
    allf = sorted(set(files) | set(logs) | {TC, "08-tooling/sen0401_lineage_control28_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, tid in KINDS:
        ok, at, how = V[k]; L.append('ex:Ev28_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (k, lit(LABEL[k]), CRIT, tid, TC, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:80], "verified" if V[k][0] else "NOT verified", OUT[k][:260]) for k in ks)))
    DEV = "The scratch pages of chapters 5, 1 and 10 were built and tested again by the builder (logs 08-tooling/verify/iter18/template); the executor's first run of page test 9.35.1 had a main-thread budget failure with the story chip PASS, its second run is kept and the builder's own run is the evidence."
    ex = ["Ev28_" + k for k, _ in KINDS]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files); i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), DEV))))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done28T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness28C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits, %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), ", ".join(COMMITS), CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
        tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; time.sleep(1.1); ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        L.append(C.transition("Ready28T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin28T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done28T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness28V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version; the scratch pages were built and tested once by the builder and are not tested a second time. Not measured here: the chapter 6 page on 9.52.1 (rebuild story ST_Repair_Page_Ch06)." % (now[:10], TK))))
        L.append('ex:ST_Repair_Template backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): AC5R_Template MET on template 9.52.1; TK_Repair_Template and TK_Repair_Template_Verify are Done on bridge-verified evidence and a harness each." % (now[:10], nxt)))
        comment = "Control of TK_Repair_Template: the bridge ran every element on template 9.52.1 (scratch pages of chapters 5, 1 and 10 built and tested again by the builder): MET; Build and Verify Done."
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), recorded as printed: %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: the control re-ran the checks and the elements not met are: %s (failing evidence recorded evidenceVerified false); the criterion is not edited, the executor repairs the template again." % (now, "; ".join(bad))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp28T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, evs, lit("Control %s: NOT Done. %s" % (now[:10], DEV))))
        comment = "Control of TK_Repair_Template: NOT MET (%s); the task is Suspended." % "; ".join(bad)
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: x[0] for k, x in V.items()}, bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]]()
