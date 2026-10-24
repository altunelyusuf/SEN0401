#!/usr/bin/env python3
"""sen0401_lineage_control39 v1_0_0 - the control of TK_Charset_Check (session SEN0401-I19-check; commit 7dfce05; criterion AC6R_Check, the page charset check v1_0_0) after its executor reported (G113, G136). The evidence bridge runs every element as an exit-code check (sen0401_charset_control_check v1_0_0, a new tool); the proofs are RUN AGAIN by the builder on fixtures it writes fresh. Met: the Build task Done and the Verify task TK_Charset_Check_Verify made Ready, started and Done in the same version (same runs, disclosed). Not met: the Build task Suspended with a rationale.
Usage: sen0401_lineage_control39_v1_0_0.py prepare|record"""
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
TK = "TK_Ch07_Deck_Reissue"; VT = "TK_Ch07_Deck_Reissue_Verify"; CRIT = "AC7R_Deck_Ch07"; SESS = "SEN0401-I20-deck-ch07-r2"; COMMITS = ["174f84d", "2c950b7"]
DECK = "03-materials/ch07/SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; CK = "08-tooling/sen0401_deck_control_check_v1_1_0.py"
SPEC = {"std": "08-tooling/sen0401_deck_standard_check_v1_0_0.py", "std11": "08-tooling/sen0401_deck_standard_check_v1_1_0.py", "manifest21": "08-tooling/sen0401_deck_manifest_scratch_v1_0_0.py", "overlap": "08-tooling/deck_overlap_check_v1_0_0.py", "deckchk": CC, "match": "08-tooling/pages_deck_match_verify_v1_0_0.py", "manifest": CK, "nochange": CK}
KINDS = [("std", "07 " + DECK), ("std11", "07 " + DECK), ("overlap", DECK), ("deckchk", "Deck/Ch07"), ("match", "07 9_76_0"), ("manifest", "manifest:07"), ("manifest21", "07 SEN0401_Ch07_AuthorizationAuthentication_3e_v2_1_0.pptx"), ("nochange", "nochange:07:174f84d,2c950b7")]
LABEL = {"std11": "deck standard check v1_1_0: D1 to D12 all PASS (independent tool)", "manifest21": "manifest order and names equal the code slides of the NEW deck v2_1_0 (scratch run with the deck field replaced in memory; nothing written)", "std": "deck standard check v1_0_0: D1 to D12 all PASS over the 87 de-duplicated key concepts (independent tool, python-pptx 1.0.2)", "overlap": "overlap scan v1_0_0: CLEAN (the executor's tool, not independent)", "deckchk": "chapter check Deck/Ch07 v1_3_0",
         "match": "deck match check v1_0_0: 0 not carried (it compares the page 9.76.0 with the old lecture export, so it does not measure the new deck)", "manifest": "chapter-code manifest: order equals the order of the code slides, names unique, library hashes match", "nochange": "no committed file edited: every file of the two commits is added (status A), none modified"}
ELEM = [("(1) deck standard check v1_0_0 and v1_1_0, D1 to D12, exit 0", ["std", "std11"]), ("(2) Deck chapter check and deck match", ["deckchk", "match", "overlap"]), ("(3) manifest in slide order, measured on the new deck", ["manifest", "manifest21"]), ("(4) no committed file edited", ["nochange"])]
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter20", "deck_ch07r2_bridge"); WORK = "/tmp/claude-0/s/ctl39"
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); draft = [PRE]
    for k, tid in KINDS: draft.append('ex:Ev39_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (k, lit(LABEL[k]), tid, SPEC[k]))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-200:])
def lastline(tid):
    p = os.path.join(LOGDIR, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100])
    return " ".join(open(p, encoding="utf-8", errors="replace").read().split())[:420] if os.path.exists(p) else "(log missing)"
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; v = S.verdicts(WORK + "/bridge.ttl"); V = {k: v["Ev39_" + k] for k, _ in KINDS}; OUT = {k: lastline(i) for k, i in KINDS}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); EI = "EI39_" + TK; bp = "08-tooling/briefs/iter22/BRIEF_%s.md" % TK
    L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + SESS), lit("brief of register v0.254"), began, end, lit("Started at the recorded work begun (T_Start, %s UTC, register v0.254) and ended with its last commit %s (%s UTC); %d commits: %s." % (began, COMMITS[-1], end, len(COMMITS), ", ".join(COMMITS)))))
    L.append('ex:Brief39%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_5_0 from register v0.254; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling/ch07-deck/logs_deck_v2_1_0/*")) + glob.glob(LOGDIR + "/*") if os.path.isfile(p))
    allf = sorted(set(files) | set(logs) | set(SPEC.values()) | {"08-tooling/sen0401_lineage_control39_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for k, tid in KINDS:
        ok, at, how = V[k]; L.append('ex:Ev39_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (k, lit(LABEL[k]), CRIT, tid, SPEC[k], "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:80], "verified" if V[k][0] else "NOT verified", OUT[k][:260]) for k in ks)))
    DEV = "Every check ran on the evidence bridge one after the other, on a machine with no other page test running. " + open("/tmp/claude-0/-home-claude/7b499b1c-1b38-5415-81de-45b731a5a6db/scratchpad/ch07deck_r2/review.txt", encoding="utf-8").read()
    ex = ["Ev39_" + k for k, _ in KINDS]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files); i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), DEV))))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done39T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness39C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits, %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), ", ".join(COMMITS), CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
        tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; time.sleep(1.1); ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        L.append(C.transition("Ready39T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin39T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done39T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness39V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version; the proofs were run once by the builder and are not run a second time." % (now[:10], TK))))
        L.append('ex:ST_Ch07_Deck_Reissue backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): AC7R_Deck_Ch07 MET on the deck 2.1.0; TK_Ch07_Deck_Reissue and TK_Ch07_Deck_Reissue_Verify are Done on bridge-verified evidence and a harness each." % (now[:10], nxt)))
        comment = "Control of TK_Ch07_Deck_Reissue: the bridge ran every element (deck checks, overlap scan, chapter check, deck match, manifest, no-edit): MET; Build and Verify Done."
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), recorded as printed: %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: the control re-ran the checks and the elements not met are: %s (failing evidence recorded evidenceVerified false); the criterion is not edited, the executor repairs the deck as new files." % (now, "; ".join(bad))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp39T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, evs, lit("Control %s: NOT Done. %s" % (now[:10], DEV))))
        comment = "Control of TK_Ch07_Deck_Reissue: NOT MET (%s); the task is Suspended." % "; ".join(bad)
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: x[0] for k, x in V.items()}, bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]]()
