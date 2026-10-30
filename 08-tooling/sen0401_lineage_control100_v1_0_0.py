#!/usr/bin/env python3
"""sen0401_lineage_control100 v1_0_0 - CASE deck (TK_Urgent_Ch06_Deck_Build, AC9_Urgent_Ch06_Deck) and CASE page (TK_Urgent_Ch06_Page_Build, AC9_Urgent_Ch06_Page), copied from control96. The elements are RUN by the evidence bridge; all verified: Build and Verify Done; else Build Suspended with the criterion untouched (nothing waived).
Usage: sen0401_lineage_control100_v1_0_0.py prepare CASE COMMITS | record CASE SESSION COMMITS     (COMMITS comma-separated, oldest first)"""
import glob, os, re, subprocess, sys, datetime, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control54_v1_0_0 as K
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TL = "08-tooling/"
GATE = '/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py'; git = K.git; utc = K.utc; sha256 = K.sha256; PRE = K.PRE
CCC = TL + "sen0401_urgent_control_check_v1_0_0.py"; DKC = TL + "sen0401_ch06_deck_control_check_v1_0_0.py"; MAT = TL + "sen0401_deck_page_code_match_v1_0_0.py"; PNL = TL + "sen0401_page_panels_test_v1_0_0.py"
M3 = "03-materials/ch06/"; CTL = REPO + "/" + TL + "verify/iter53/ctl/ctl_sen0401_page_test_v9_"
def deck(pre):
    return dict(crit="AC9_Urgent_Ch06_Deck", tk="TK_Urgent_Ch06_Deck_Build", vt="TK_Urgent_Ch06_Deck_Verify", brief="iter53", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("own", DKC, M3 + "SEN0401_Ch06_Transactions_3e_v2_3_0.pptx " + M3 + "SEN0401_Ch06_Transactions_3e_v2_2_0.pptx " + M3 + "page/chapter_code_ch06_v1_1_0.json"), ("match", MAT, "06")],
   label={"nochange": "the executor's commits leave every earlier committed file with the same content at the last commit (net; a file changed and restored counts as unchanged)",
          "own": "the control's own script on the deck v2_3_0 and the old deck v2_2_0: prompts, indentation, lambda, label shapes, 52 result rows re-run, code differences listed, the old deck byte-identical",
          "match": "the code match of the newest deck and page: every code line of the chapter-code manifest is on the deck and in the page"},
   elem=[("(1) no committed file is edited and the old deck is unchanged", ["nochange"]), ("(2) to (4) 0 prompts, 0 lambda, 0 label shapes, 0 unindented bodies, every result re-run equal, and the deck's code is the page's Chapter code examples", ["own", "match"])])
def page(pre):
    pt = lambda v, n: ("pt" + v, CCC, "logcheck " + v + " " + n)
    return dict(crit="AC9_Urgent_Ch06_Page", tk="TK_Urgent_Ch06_Page_Build", vt="TK_Urgent_Ch06_Page_Verify", brief="iter53", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("match", MAT, "06"), ("panels", CCC, "logcheck panels 100"), pt("38_0", "300"), pt("34_3", "300"), pt("35_3", "300"), pt("37_0", "300"), pt("34_2", "300")],
   label={"nochange": "the executor's commits leave every earlier committed file with the same content at the last commit (net)",
          "match": "the code match of the newest deck and page: 0 slide code lines found nowhere in the page",
          "panels": "the panel test run by the control on the page v9.89.0 (full screen and reader-set size): no FAIL line",
          "pt38_0": "the control's own run of the page test copy 9.38.0 on the page v9.89.0 (log read: no traceback, no FAIL, all widgets passed, at least 300 features)",
          "pt34_3": "the control's own run of the page test copy 9.34.3 on the page v9.89.0 (same reading)",
          "pt35_3": "the control's own run of the page test copy 9.35.3 on the page v9.89.0 (same reading)",
          "pt37_0": "the control's own run of the COMMITTED page test 9.37.0 on the page v9.89.0 (same reading)",
          "pt34_2": "the control's own run of the COMMITTED page test 9.34.2 on the page v9.89.0 (same reading)"},
   elem=[("(1)(6) no committed file is edited", ["nochange"]), ("(2) full screen and reader-set size in every panel kind", ["panels"]), ("(3)(4) slide examples first in the Playground, 0 slide code lines found nowhere", ["match"]),
         ("(5a) the page test copies 9.34.3, 9.35.3 and 9.38.0 give widgets and features, none failing", ["pt38_0", "pt34_3", "pt35_3"]), ("(5b) the committed page tests 9.34.2 and 9.37.0 named by the criterion give widgets, features and gates not below the old page's", ["pt37_0", "pt34_2"])])
def nocopy(pre):
    return dict(crit="AC3E_Exam_NoCopy", tk="TK_Exam_NoCopy_Build", vt="TK_Exam_NoCopy_Verify", brief="iter51", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines"), ("own", "08-tooling/exam/sen0401_exam_nocopy_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's five commits leave every earlier committed file with the same content (net); all exam files are new",
          "rerun": "the executor's check v1.1.1 re-run by the control (16 of 16 PASS) gives the same PASS and FAIL lines as the executor's log",
          "own": "the control's own check: own pairs with an own ground truth (difflib), the engine's command line, a static read for bank calls, and the byte identity of the 43 v1.0.0 files"},
   elem=[("(1) the engine v1.1.0 is new files and no committed file is edited", ["nochange"]), ("(2)(3) EN11 refuses a page copy with thresholds stated before the run, and the fixture of known answer gives the expected answer", ["rerun", "own"]), ("(4)(5) authored items only, and all rules of v1.0.0 and the owner's decisions still hold", ["rerun", "own"])])
def items(pre):
    return dict(crit="AC3E_Exam_Items", tk="TK_Exam_Items_Build", vt="TK_Exam_Items_Verify", brief="iter54b", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines items"), ("own", "08-tooling/exam/sen0401_exam_items_control_check_v1_0_0.py", "run")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file",
          "rerun": "the executor's check re-run by the control (all lines PASS, RESULT PASS) gives the same result lines as its committed log",
          "own": "the control's own check: units and chapters, seed keys and point ids resolved by my own loader, trace listings re-run (my own cs_encode supplied for one), the five number keys computed again from the stems, my own similarity of every component against 1236 page items (highest 0.560 on short ordering steps), letters, levels, report counts"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2) 24 units, authored, none a near copy by the engine rule EN11 and by the control's own method (and the nearest pairs read by a person)", ["rerun", "own"]), ("(3) every item names seeds or says none, enhancements, points, chapters, level, type and source, all resolving", ["rerun", "own"]), ("(4) computed keys re-run equal", ["rerun", "own"]), ("(5) terms found, conventions hold, the engine v1.1.0 accepts the midterm", ["rerun"]), ("(6) the report names the points tested and not tested", ["own"])])
def papers(pre):
    return dict(crit="AC3E_Exam_Papers", tk="TK_Exam_Papers_Build", vt="TK_Exam_Papers_Verify", brief="iter54d", pre=pre, ei="EI" + pre, n="00",
   kinds=lambda c: [("nochange", CCC, "nochange " + c), ("rerun", CCC, "samelines papers"), ("own", "08-tooling/exam/sen0401_exam_papers_control_check_v1_0_0.py", REPO + "/08-tooling/verify/iter54/ctl/papers_rebuilt")],
   label={"nochange": "the executor's commit adds only new files and edits no earlier committed file",
          "rerun": "the executor's papers check re-run by the control on the control's own rebuild (17 of 17 PASS) gives the same result lines as its committed log",
          "own": "the control's own check: the builder run again gives the same key, graph, layout and measurement files; the key agrees with the items for every keyed entry by my own reading of the graph and the printed steps; page counts by pdfinfo; no image and no colour in the rendered pages; the reader v1.1.0 on 40 synthetic sheets of each of the paper's own layouts"},
   elem=[("(1) every file is new and no committed file is edited", ["nochange"]), ("(2) the rendered pages were opened and read by the control, pages counted (7 in chapter order, 6 grouped by type), print safety, key and paper agree", ["rerun", "own"])])
CASES = {"deck": deck("Ev100ka"), "page": page("Ev100kb"), "nocopy": nocopy("Ev100kc"), "items": items("Ev100kd"), "papers": papers("Ev100ke")}
def setup(case):
    global CS, LOG, WORK, kinds, LABEL, ELEM
    CS = CASES[case]; LOG = os.path.join(REPO, TL, "verify/iter54/bridge_" + case); WORK = "/tmp/claude-0/s/ctl60_" + case; kinds = CS["kinds"]; LABEL = CS["label"]; ELEM = CS["elem"]
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
    files = sorted({f for x in cm for f in git("show", "--name-only", "--format=", x).splitlines() if f}); logs = sorted(os.path.relpath(os.path.join(dp, f), REPO) for dp, _, fs in os.walk(LOG) for f in fs)
    allf = sorted(set(files) | set(logs) | {TL + "sen0401_lineage_control100_v1_0_0.py", TL + "sen0401_lineage_work_begun_v1_17_0.py", TL + "sen0401_urgent_control_check_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values())
    L.append('ex:EI55 a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief of the register as generated" ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (lit("Executor session " + sess), began, end, lit("Started at the recorded work begun (%s UTC, as reported by the coordinator); retired at its commit %s (%s UTC)." % (began, c, end))))
    bp = "08-tooling/briefs/%s/BRIEF_%s.md" % (CS["brief"], TK)
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
    RN = lambda x: re.sub(r"(Ev|EI|Brief|Harness|Done|Begin|Ready|Susp)55", lambda m: m.group(1) + "100" + {"deck": "ka", "page": "kb", "nocopy": "kc", "items": "kd", "papers": "ke"}[case], x)
    print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + RN("".join(L)), "LS_InProgress"), nxt, cur, "Control of the urgent chapter 6 work (%s, %s): %s." % (TK, sess, "MET, Build and Verify Done" if not bad else "NOT MET: " + "; ".join(bad))))); print(bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]](*sys.argv[2:])
