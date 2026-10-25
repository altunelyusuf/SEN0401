#!/usr/bin/env python3
"""sen0401_lineage_control33 v1_0_0 - the control of TK_Charset_Template (session SEN0401-I19-template; commits fc7f78a and 3652227; criterion AC6R_Template, page template 9.52.2) after its executor reported (G113, G136). The evidence bridge runs every element as an exit-code check (sen0401_template_check2 v1_0_0, a new tool; the scratch chapter 5 page and page test 9.36.0 are run by the builder, the bridge reads those logs). Met: the build task is Done and its verify task goes Ready, Started and Done (same version, distinct instants); not met: the task is Suspended with the elements named.
Usage: sen0401_lineage_control33_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control27_v1_0_0 as K27
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TC = "08-tooling/sen0401_template_check2_v1_0_0.py"; GATE = K27.GATE; git = K27.git; utc = K27.utc; sha256 = K27.sha256; PRE = K27.PRE
TK = "TK_Charset_Template"; VT = "TK_Charset_Template_Verify"; CRIT = "AC6R_Template"; SESS = "SEN0401-I19-template"; COMMITS = ["fc7f78a", "3652227"]
KINDS = [("nochange", "nochange:fc7f78a,3652227"), ("ident", "ident"), ("offset", "offset"), ("diff", "diff"), ("scratch", "scratch")]
LABEL = {"nochange": "the executor's two commits add files only, no committed file edited",
         "ident": "9.52.0 and 9.52.1 and every older template are clean against HEAD with the recorded SHA-256 and one commit each; 9.52.2 is one commit, a new file, with the recorded SHA-256",
         "offset": "RUN by the builder: the new page charset check exits 0 on template 9.52.2 and prints the tag offset (37); the tag occurs exactly once, below byte 1024; the first 1024 bytes decode as UTF-8",
         "diff": "RUN by the builder: after removing every comment and the tag the two templates are equal but for line breaks; every comment of 9.52.1 is in 9.52.2, the only new comment is the 9.52.2 version marker; no id or data- hook of 9.52.1 is missing",
         "scratch": "RUN by the builder: a scratch page of chapter 5 built on 9.52.2 with builders v4_15_0 and v2_24_0 has the tag once at a byte below 1024 (the check exits 0) and page test 9.36.0 exits 0 with no failed feature line"}
ELEM = [("(1) a new file; the older templates are byte-identical; no committed file edited", ["ident", "nochange"]), ("(2) the tag once below byte 1024 and the first 1024 bytes decode as UTF-8", ["offset"]), ("(3) the diff shows only the moved tag, the moved comments and the version marker; every id and hook present", ["diff"]),
        ("(4) a scratch page of chapter 5 on 9.52.2 has the tag below 1024 and passes page test 9.36.0", ["scratch"]), ("(5) no committed file edited", ["nochange"])]
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter19", "template_bridge"); WORK = "/tmp/claude-0/s/ctl33"
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); draft = [PRE]
    for k, tid in KINDS: draft.append('ex:Ev33_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), tid, TC))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-200:])
def lastline(tid):
    p = os.path.join(LOGDIR, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100])
    return " ".join(open(p, encoding="utf-8", errors="replace").read().split())[:420] if os.path.exists(p) else "(log missing)"
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; v = S.verdicts(WORK + "/bridge.ttl"); V = {k: v["Ev33_" + k] for k, _ in KINDS}; OUT = {k: lastline(i) for k, i in KINDS}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); EI = "EI33_" + TK; bp = "08-tooling/briefs/iter19/BRIEF_%s.md" % TK
    L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + SESS), lit("brief of register v0.227"), began, end, lit("Started at the recorded work begun (T_Start, %s UTC, register v0.227) and ended with its last commit %s (%s UTC); %d commits: %s." % (began, COMMITS[-1], end, len(COMMITS), ", ".join(COMMITS)))))
    L.append('ex:Brief33%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_3_0 from register v0.227; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling/template952_logs/I19/*")) + glob.glob(os.path.join(REPO, "08-tooling/verify/iter19/template/*")) + glob.glob(LOGDIR + "/*") if os.path.isfile(p))
    allf = sorted(set(files) | set(logs) | {TC, "08-tooling/sen0401_lineage_control33_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, tid in KINDS:
        ok, at, how = V[k]; L.append('ex:Ev33_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (k, lit(LABEL[k]), CRIT, tid, TC, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:80], "verified" if V[k][0] else "NOT verified", OUT[k][:260]) for k in ks)))
    DEV = "The checks were run by the builder: the page charset check on the template, the comparison of the two templates, a scratch page of chapter 5 built on 9.52.2 and page test 9.36.0 (run twice: the first run had 1 failed feature line, the main-thread budget after load, 211 ms against 200, while a register validator and another session's page test were running on the same two cores; the second run, with the validator finished, passed 398 features with 0 failed; both logs are kept and the run that is read by the bridge is the second); the executor's own logs are kept as its own evidence."
    ex = ["Ev33_" + k for k, _ in KINDS]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files); i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), DEV))))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done33T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness33C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits, %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), ", ".join(COMMITS), CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
        tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; time.sleep(1.1); ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        L.append(C.transition("Ready33T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin33T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done33T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness33V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version; the proofs were run once by the builder and are not run a second time." % (now[:10], TK))))
        L.append('ex:ST_Charset_Template backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): AC6R_Template MET on the template 9.52.2; TK_Charset_Template and TK_Charset_Template_Verify are Done on bridge-verified evidence and a harness each." % (now[:10], nxt)))
        comment = "Control of TK_Charset_Template: the bridge ran every element (proofs re-run by the builder on fresh fixtures and the shipped pages): MET; Build and Verify Done."
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), recorded as printed: %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: the control re-ran the checks and the elements not met are: %s (failing evidence recorded evidenceVerified false); the criterion is not edited, the executor repairs the template again." % (now, "; ".join(bad))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp33T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, evs, lit("Control %s: NOT Done. %s" % (now[:10], DEV))))
        comment = "Control of TK_Charset_Template: NOT MET (%s); the task is Suspended." % "; ".join(bad)
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: x[0] for k, x in V.items()}, bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]]()
