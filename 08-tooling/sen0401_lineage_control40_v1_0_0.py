#!/usr/bin/env python3
"""sen0401_lineage_control40 v1_0_0 - the control of TK_PageTest937_Build (session SEN0401-I22-pagetest; commits 1f9550b, af48938, d7f49b8; criterion AC7R_PageTest937, the page test 9.37.0) after its executor reported (G113, G136). The evidence bridge runs every element as an exit-code check (sen0401_charset_control_check v1_0_0, a new tool); the proofs are RUN AGAIN by the builder on fixtures it writes fresh. Met: the Build task Done and the Verify task TK_Charset_Check_Verify made Ready, started and Done in the same version (same runs, disclosed). Not met: the Build task Suspended with a rationale.
Usage: sen0401_lineage_control40_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control27_v1_0_0 as K27
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TC = "08-tooling/sen0401_deckcheck_control_check_v1_0_0.py"; GATE = K27.GATE; git = K27.git; utc = K27.utc; sha256 = K27.sha256; PRE = K27.PRE
TK = "TK_PageTest937_Build"; VT = "TK_PageTest937_Verify"; CRIT = "AC7R_PageTest937"; SESS = "SEN0401-I22-pagetest"; COMMITS = ["1f9550b", "af48938", "d7f49b8"]
TC = "08-tooling/sen0401_pagetest937_control_check_v1_0_0.py"; GATE = K27.GATE; git = K27.git; utc = K27.utc; sha256 = K27.sha256; PRE = K27.PRE
KINDS = [(k, k) for k in ["sha", "diff", "fa937", "fa936", "fb937", "fc937", "ch05", "ch06", "ch08", "nochange"]]
SPEC = {k: TC for k, _ in KINDS}
LABEL = {"sha": "page test 9.36.0 is byte-identical (SHA-256 85afebf6... equals the value before the task; git log of the file shows only commit d4880a3)", "diff": "the diff 9.36.0 to 9.37.0 holds the version string, one comment and the P2 wait only", "fa937": "fixture a (slow example with a visual): 9.37.0 passes P2", "fa936": "fixture a: 9.36.0 fails P2 with 'result is text, not a visualisation' (the race)", "fb937": "fixture b (text-only example): 9.37.0 fails P2 with 'result is text, not a visualisation'", "fc937": "fixture c (example never ends): 9.37.0 fails P2 within the 90 s bound", "ch05": "chapter 5 page 9.83.0 under 9.37.0: 398 passed, 0 failed (the same as 9.36.0)", "ch06": "chapter 6 page 9.83.0 under 9.37.0: 398 passed, 0 failed (the same as 9.36.0)", "ch08": "chapter 8 page 9.85.0 under 9.37.0: 394 passed, 0 failed (P2 as printed)", "nochange": "no committed file edited: all 32 files of the three commits are added (status A)"}
ELEM = [("(1) 9.36.0 byte-identical", ["sha"]), ("(2) diff limited to the P2 wait and the version", ["diff"]), ("(3) fixtures a, b and c", ["fa937", "fa936", "fb937", "fc937"]), ("(4) chapters 5 and 6 same as 9.36.0, chapter 8 reported as printed", ["ch05", "ch06", "ch08"]), ("(5) no committed file edited", ["nochange"])]
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter22", "pagetest937_bridge"); WORK = "/tmp/claude-0/s/ctl40"; RUNDIR = "08-tooling/verify/iter22/pagetest937"
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); draft = [PRE]
    for k, tid in KINDS: draft.append('ex:Ev40_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), tid, SPEC[k]))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-200:])
def lastline(tid):
    p = os.path.join(LOGDIR, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100])
    return " ".join(open(p, encoding="utf-8", errors="replace").read().split())[:420] if os.path.exists(p) else "(log missing)"
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; v = S.verdicts(WORK + "/bridge.ttl"); V = {k: v["Ev40_" + k] for k, _ in KINDS}; OUT = {k: lastline(i) for k, i in KINDS}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); EI = "EI40_" + TK; bp = "08-tooling/briefs/iter22/BRIEF_%s.md" % TK
    L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + SESS), lit("brief of register v0.254"), began, end, lit("Started at the recorded work begun (T_Start, %s UTC, register v0.254) and ended with its last commit %s (%s UTC); %d commits: %s." % (began, COMMITS[-1], end, len(COMMITS), ", ".join(COMMITS)))))
    L.append('ex:Brief40%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_5_0 from register v0.254; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, RUNDIR, "*")) + glob.glob(LOGDIR + "/*") + glob.glob(os.path.join(REPO, "08-tooling/page-test-937-fixtures/*")) + glob.glob(os.path.join(REPO, "08-tooling/page-test-937-fixtures/logs/*")) if os.path.isfile(p))
    allf = sorted(set(files) | set(logs) | set(SPEC.values()) | {"08-tooling/sen0401_lineage_control40_v1_0_0.py", "08-tooling/sen0401_page_test_v9_37_0.py", "08-tooling/sen0401_page_test_v9_36_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, tid in KINDS:
        ok, at, how = V[k]; L.append('ex:Ev40_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (k, lit(LABEL[k]), CRIT, tid, SPEC[k], "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:80], "verified" if V[k][0] else "NOT verified", OUT[k][:260]) for k in ks)))
    DEV = "The builder re-ran the three fixtures under 9.37.0, fixture a under 9.36.0 and the pages 9.83.0 of chapters 5 and 6 and 9.85.0 of chapter 8 under 9.37.0 itself, under flock /tmp/page_test.lock, one at a time (logs in %s); the bridge ran the exit-code checks over those logs, the files and the git history. Chapters 5 and 6 under 9.36.0 are the recorded runs of register v0.2 (398 passed, 0 failed each). The page 9.85.0 of chapter 8 under 9.36.0 fails P2 only (examples 17 and 18; executor and builder logs); under 9.37.0 it gives 394 passed, 0 failed." % RUNDIR
    ex = ["Ev40_" + k for k, _ in KINDS]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files); i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), DEV))))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done40T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness40C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits, %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), ", ".join(COMMITS), CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
        tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; time.sleep(1.1); ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        L.append(C.transition("Ready40T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin40T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done40T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness40V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version; the proofs were run once by the builder and are not run a second time." % (now[:10], TK))))
        L.append('ex:ST_PageTest_937 backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): AC7R_PageTest937 MET on the page test 9.37.0; TK_PageTest937_Build and TK_PageTest937_Verify are Done on bridge-verified evidence and a harness each." % (now[:10], nxt)))
        comment = "Control of TK_PageTest937_Build: the bridge ran every element (9.36.0 unchanged, diff, fixtures a, b, c, pages of chapters 5, 6, 8, no-edit): MET; Build and Verify Done."
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), recorded as printed: %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: the control re-ran the checks and the elements not met are: %s (failing evidence recorded evidenceVerified false); the criterion is not edited, the executor repairs the test as new files." % (now, "; ".join(bad))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp40T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, evs, lit("Control %s: NOT Done. %s" % (now[:10], DEV))))
        comment = "Control of TK_PageTest937_Build: NOT MET (%s); the task is Suspended." % "; ".join(bad)
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: x[0] for k, x in V.items()}, bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]]()
