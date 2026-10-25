#!/usr/bin/env python3
"""sen0401_lineage_control59 v1_0_0 - the control of ONE Build/Verify pair of Iteration 31 (CASE t9524: the page template 9.52.4, AC9_Template9524; CASE sl10 / sl12: the story-link deck repair of that chapter, AC9_StoryLink_ChNN; G113, G136): the elements are RUN by the evidence bridge. All verified: Build and Verify Done; else Build Suspended.
Usage: sen0401_lineage_control59_v1_0_0.py prepare CASE COMMITS | record CASE SESSION COMMITS     (COMMITS comma-separated, oldest first)"""
import glob, os, re, subprocess, sys, datetime, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control54_v1_0_0 as K
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TL = "08-tooling/"
GATE = K.GATE; git = K.git; utc = K.utc; sha256 = K.sha256; PRE = K.PRE
def storylink(nn, pre):
    return dict(crit="AC9_StoryLink_Ch" + nn, tk="TK_Deck%s_StoryLink_Build" % nn, vt="TK_Deck%s_StoryLink_Verify" % nn, brief="iter36", pre=pre, ei="EI" + pre, n=nn,
   kinds=lambda c: [("story", TL + "sen0401_story_check_v1_0_0.py", nn), ("arc", TL + "sen0401_deck_arc_check_v1_3_0.py", nn), ("std", TL + "sen0401_deck_standard_check_v1_1_0.py", nn), ("overlap", TL + "deck_overlap_check_v1_0_0.py", K.deckfile(nn)), ("manifest", TL + "sen0401_deck_control_check_v1_1_0.py", "manifest:" + nn),
                    ("errfirst", TL + "sen0401_manifest_errfirst_scan_v1_0_0.py", nn), ("deckchk", TL + "sen0401_lineage_chapter_check_v1_4_0.py", "Deck/Ch" + nn), ("nochange", TL + "sen0401_deck_control_check_v1_1_0.py", "nochange:%s:%s" % (nn, c))],
   label={"story": "story check v1_0_0 on the new deck of chapter %s: exit 0, no refusal" % nn.lstrip("0"), "arc": "arc check v1_3_0: exit 0, no refusal", "std": "deck standard check v1_1_0: every element D1 to D12 met, exit 0", "overlap": "deck overlap check v1_0_0: exit 0", "manifest": "deck control check v1_1_0 manifest: order, names, library files, hashes", "errfirst": "error-first scan: no manifest example starts with an error name",
          "deckchk": "Deck chapter check v1_4_0 (every part, with the newest plan)", "nochange": "no committed file is edited (every file of the executor's commits added)"},
   elem=[("(1) story check v1_0_0 prints no refusal", ["story"]), ("(2) arc check, deck standard, overlap, manifest, error-first scan and Deck chapter check", ["arc", "std", "overlap", "manifest", "errfirst", "deckchk"]), ("(3) the delivered deck and every committed file unchanged", ["nochange"])])
TC = TL + "sen0401_template9524_control_check_v1_0_0.py"
CASES = {"sl10": storylink("10", "Ev59g"), "sl12": storylink("12", "Ev59h"), "sl14": storylink("14", "Ev59i"),
 "t9524": dict(crit="AC9_Template9524", tk="TK_Template_9524_Build", vt="TK_Template_9524_Verify", brief="iter34", pre="Ev59f", ei="EI59f", n="",
   kinds=lambda c: [("sha", TC, "sha"), ("nomod", TC, "nomod"), ("pairs", TC, "pairs"), ("probe", TC, "probe"), ("regr", TC, "regr"), ("nochange", TC, "nochange:" + c)],
   label={"sha": "9.52.2 and 9.52.3 unchanged by content, 9.52.4 byte-identical to 9.52.3", "nomod": "9.52.4 added by one commit and modified by none", "pairs": "scratch pages of chapters 1, 5, 6, 7, 8, 10 built from 9.52.4 and from 9.52.3 are byte-identical in pairs (built by the control)", "probe": "story layout probe v1_0_0 PASS on the 9.52.4 scratch pages of chapters 5 to 8 (built and run by the control)",
          "regr": "page tests 9.37.0, 9.34.1, 9.35.1 on the chapter 5 scratch page built from 9.52.4 give the stored results or better (the control's own runs under the lock)", "nochange": "the executor's commits only add files"},
   elem=[("(1) 9.52.2 and 9.52.3 unchanged, 9.52.4 equal to 9.52.3", ["sha"]), ("(2) 9.52.4 added in one commit and never modified", ["nomod"]), ("(3) scratch pages built from 9.52.4 equal those of 9.52.3, probe PASS, page tests at the stored results", ["pairs", "probe", "regr"]), ("(4) no committed file is edited", ["nochange"])])}
def setup(case):
    global CS, LOG, WORK, kinds, LABEL, ELEM
    CS = CASES[case]; LOG = os.path.join(REPO, TL, "verify/iter32/bridge_" + case); WORK = "/tmp/claude-0/s/ctl56_" + case; kinds = CS["kinds"]; LABEL = CS["label"]; ELEM = CS["elem"]
def prepare(case, c):
    setup(case)
    os.makedirs(LOG, exist_ok=True); os.makedirs(WORK, exist_ok=True); draft = [PRE]
    for kind, spec, tid in kinds(c): draft.append('ex:Ev55_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, lit(LABEL[kind]), tid, spec))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft)); cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOG
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(r.stdout[-300:])
def last(tid):
    tid = tid[0] + "_" + tid[1]
    p = os.path.join(LOG, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", tid)[:100]); ls = [l for l in open(p, errors="replace").read().splitlines() if l.strip()] if os.path.exists(p) else []
    return " ".join(ls)[:300] if ls else "(log missing)"
def record(case, sess, c):
    setup(case)
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; TK = CS["tk"]; VT = CS["vt"]; CRIT = CS["crit"]
    v = S.verdicts(WORK + "/bridge.ttl"); K_ = kinds(c); V = {k: v["Ev55_" + k] for k, _, _ in K_}; OUT = {k: last((sp, i)) for k, sp, i in K_}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); cm = c.split(","); end = utc(cm[-1])
    files = sorted({f for x in cm for f in git("show", "--name-only", "--format=", x).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(LOG + "/*") + glob.glob(os.path.join(REPO, TL, "verify/iter32/ctl_template9524/*")) + glob.glob(os.path.join(REPO, TL, "template9524_logs/*")))
    allf = sorted(set(files) | set(logs) | {TL + "sen0401_lineage_control59_v1_0_0.py", TL + "sen0401_lineage_work_begun_v1_16_0.py", TL + "sen0401_lineage_control59_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values())
    L.append('ex:EI55 a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief of the register as generated" ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (lit("Executor session " + sess), began, end, lit("Started at the recorded work begun (%s UTC, as reported by the coordinator); retired at its commit %s (%s UTC)." % (began, c, end))))
    bp = "briefs/%s/BRIEF_%s.md" % (CS["brief"], TK)
    L.append('ex:Brief55 a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI55 ;\n    rdfs:comment %s .\n' % (lit("Brief of " + TK), TK, CRIT, lit("File %s, SHA-256 %s." % (bp, sha256(bp)))))
    for kind, spec, tid in K_:
        ok, at, how = V[kind]
        L.append('ex:Ev55_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (kind, lit(LABEL[kind]), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, _) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), now))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]; lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s -> %s" % ("verified" if V[k][0] else "NOT verified", OUT[k][:200]) for k in ks)))
    ex = ["Ev55_" + k for k, _, _ in K_]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files)
    DEV = os.environ.get("CTL_EXTRA", "")
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET. %s" % (now[:10], nxt, " | ".join(lines), DEV))))
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done55T_" + TK, TK, "T_Complete", end, "Done on the executor's commit %s (%s UTC), recorded in v%s on %s once the control run gave it bridge-verified evidence." % (c, end, nxt, now), TK + " completed"))
        L.append('ex:Harness55_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (commit %s). Results are those of the evidence nodes and the note of %s. %s" % (now[:10], sess, c, CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert ("backlog:hasState backlog:Proposed" in b or "backlog:hasState backlog:Ready" in b) and "startedAt" not in b, VT
        wasprop = "backlog:hasState backlog:Proposed" in b
        tmp = (t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]) if wasprop else t; ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed" if wasprop else "backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        if wasprop: L.append(C.transition("Ready55T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin55T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the lineage agent after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done55T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness55_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements are those of the control of %s in the same version." % (now[:10], TK))))
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s): %s. RESULT: NOT MET: %s. %s" % (now[:10], nxt, " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: elements not met: %s (nothing waived, the criterion is not edited)." % (now, "; ".join(bad))
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp55T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s .\n' % (TK, evs))
    RN = lambda x: re.sub(r"(Ev|EI|Brief|Harness|Done|Begin|Ready|Susp)55", lambda m: m.group(1) + "56" + {"sl10": "g", "sl12": "h", "sl14": "i", "t9524": "f"}[case], x)
    print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + RN("".join(L)), "LS_InProgress"), nxt, cur, "Control of the temporary-folder repair (%s, %s): %s." % (TK, sess, "MET, Build and Verify Done" if not bad else "NOT MET: " + "; ".join(bad))))); print(bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]](*sys.argv[2:])
