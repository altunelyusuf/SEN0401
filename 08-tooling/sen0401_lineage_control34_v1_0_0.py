#!/usr/bin/env python3
"""sen0401_lineage_control34 v1_0_0 - the control of the two page rebuild tasks of Iter_19 (TK_Charset_Page_Ch05_Build, session SEN0401-I18-page-ch05; TK_Charset_Page_Ch06_Build, session SEN0401-I18-page-ch06; page 9.83.0 on template 9.52.2; criteria AC6R_Page_Ch05 and AC6R_Page_Ch06) (G113, G136). The three page tests are RUN by the builder on each page, serially per page (logs in 08-tooling/verify/iter19/pages); every other element is run by the bridge. A chapter whose elements are all met: Build Done and the Verify task Ready, started, Done in the same version; otherwise the Build task is Suspended with a rationale.
Usage: sen0401_lineage_control34_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; PC = "08-tooling/sen0401_lineage_page_check_v1_5_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"; DC = "08-tooling/sen0401_deck_control_check_v1_1_0.py"
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
CH = {"05": dict(pv="9_83_0", pvd="9.83.0", old="9_74_0", sess="SEN0401-I19-page-ch05", commits=["48df70c", "6b80ea7", "a4b12aa", "384d11c"]),
      "06": dict(pv="9_83_0", pvd="9.83.0", old="9_75_0", sess="SEN0401-I19-page-ch06", commits=["218cad8", "234674e", "fe37d0e"])}
CHS = [c for c in sys.argv[2:] if c in ("05", "06")]
def kinds(nn):
    c = CH[nn]; pv = c["pv"]; n = nn.lstrip("0")
    return [("charset", PC, "charset:%s:%s" % (nn, pv)), ("t36", PC, "test:%s:%s:9_36_0" % (nn, pv)), ("t35", PC, "test:%s:%s:9_35_1" % (nn, pv)), ("t34", PC, "test:%s:%s:9_34_1" % (nn, pv)), ("chip", PC, "chip:%s:%s" % (nn, pv)), ("p36", PC, "p36:%s:%s" % (nn, pv)),
            ("c35", PC, "counts:%s:%s:9_35_1:%s" % (nn, pv, c["old"])), ("c34", PC, "counts:%s:%s:9_34_1:%s" % (nn, pv, c["old"])), ("deck", PC, "deck:%s:%s" % (nn, pv)), ("abox", PC, "abox:%s:%s" % (nn, pv)),
            ("stage4", S4, nn), ("research", CC, "Research/Ch%s" % nn), ("deckchk", CC, "Deck/Ch%s" % nn), ("pagechk", CC, "Page/Ch%s" % nn), ("manifest", DC, "manifest:%s" % nn), ("nochange", PC, "nochange:%s:%s" % (nn, ",".join(c["commits"])))]
LABEL = {"charset": "the page charset check exits 0 on the page: the tag once below byte 1024, the first 1024 bytes decode as UTF-8, the page embeds template 9.52.2", "t36": "RUN by the builder: page test 9.36.0 on the page: exit 0, every widget passed, no [FAIL]", "t35": "RUN by the builder: page test 9.35.1 on the page: no failure", "t34": "RUN by the builder: page test 9.34.1 on the page: no failure",
         "chip": "the feature 'a story chip on a concept opens that story in the Stories tab' passes in the runs of the three page tests", "p36": "page test 9.36.0: the added features P1 P2 P3 P4 P5 P6 P8 P9 P11 all PASS, none SKIP",
         "c35": "page test 9.35.1 widgets, features and gates not below the stored result of the earlier page, skipped not more", "c34": "page test 9.34.1 widgets, features and gates not below the stored result of the earlier page, skipped not more",
         "deck": "deck match check: 0 not carried", "abox": "the Stage 4 page ABox and the stored page-test result are new files", "stage4": "Stage 4 gate runner v1_1_0 (current validator v1.13.0)", "research": "chapter check Research v1_3_0 (pinned validator v1.6.0)",
         "deckchk": "chapter check Deck", "pagechk": "chapter check Page", "manifest": "the chapter-code manifest equals the order of the deck's code slides (names unique, library files exist)", "nochange": "no committed file is edited (every file of the executor's commits added)"}
ELEM = [("(1) the charset check exits 0 on the page", ["charset"]), ("(2a) page test 9.36.0: every added feature passes, exit 0", ["t36", "p36"]), ("(2b) page tests 9.34.1 and 9.35.1: no failure, counts not below the stored result, story chip included", ["t35", "t34", "c35", "c34", "chip"]),
        ("(3) chapter-code tab equals the deck's manifest, examples run (page test and manifest check)", ["p36", "manifest"]), ("(4) Stage 4 runner, Research/Deck/Page chapter checks, deck match", ["stage4", "research", "deckchk", "pagechk", "deck"]), ("(5) no committed file edited; ABox and stored result new files", ["nochange", "abox"])]
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
PRE = "@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter19", "pages_bridge"); WORK = "/tmp/claude-0/s/ctl34"
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True)
    for nn in CHS:
        draft = [PRE]
        for kind, spec, tid in [k for k in kinds(nn) if not os.environ.get("ONLY") or k[0] in os.environ["ONLY"].split(",")]: draft.append('ex:Ev34c%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (nn, kind, lit("%s, chapter %s page %s" % (LABEL[kind], nn.lstrip("0"), CH[nn]["pvd"])), tid, spec))
        d = "%s/draft%s.ttl" % (WORK, nn); open(d, "w").write("".join(draft))
        cmd = 'python3 -B {spec} {id} > %s/bridge_%s_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % (LOGDIR, nn)
        r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", "%s/bridge%s%s.ttl" % (WORK, nn, "_re" if os.environ.get("ONLY") else "")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(nn, r.stdout[-160:])
def lastline(nn, spec, tid):
    p = os.path.join(LOGDIR, "bridge_%s_%s.log" % (nn, re.sub(r"[^A-Za-z0-9\n]", "_", "%s_%s" % (spec, tid))[:100]))
    if not os.path.exists(p): return "(log missing)"
    ls = [l for l in open(p, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()]
    return " ".join(l for l in ls if l.startswith(("RESULT", "SUMMARY", "manifest", "9.3", "9_3", "story chip", "commits", "Stage 4", "chapter", "deck", "page ", "PASS", "FAIL")))[:340] or (ls[-1][:340] if ls else "")
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; res = {}
    for nn in CHS:
        c = CH[nn]
        K = kinds(nn); TK = "TK_Charset_Page_Ch%s_Build" % nn; VT = "TK_Charset_Page_Ch%s_Verify" % nn; CRIT = "AC6R_Page_Ch%s" % nn; v = S.verdicts("%s/bridge%s.ttl" % (WORK, nn)); v.update(S.verdicts("%s/bridge%s_re.ttl" % (WORK, nn)) if os.path.exists("%s/bridge%s_re.ttl" % (WORK, nn)) else {}); V = {k: v["Ev34c%s_%s" % (nn, k)] for k, _, _ in K}; OUT = {k: lastline(nn, s, i) for k, s, i in K}
        began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(c["commits"][-1]); EI = "EI34c%s" % nn; bp = "08-tooling/briefs/iter19/BRIEF_%s.md" % TK
        L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + c["sess"]), lit("brief of register v0.230"), began, end, lit("Started at the recorded work begun (T_Start, %s UTC, register v0.230) and ended with its last commit %s (%s UTC); %d commits: %s." % (began, c["commits"][-1], end, len(c["commits"]), ", ".join(c["commits"])))))
        L.append('ex:Brief34%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_3_0 from register v0.230; file %s, SHA-256 %s." % (bp, sha256(bp)))))
        files = sorted({f for cm in c["commits"] for f in git("show", "--name-only", "--format=", cm).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling/verify/iter19/pages/ch%s_page_%s_*" % (nn, c["pv"]))))
        tools = [PC, "08-tooling/sen0401_lineage_control34_v1_0_0.py"]; allf = sorted(set(files) | set(logs) | set(tools)); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
        for kind, spec, tid in K:
            ok, at, how = V[kind]
            L.append('ex:Ev34c%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (nn, kind, lit("%s, chapter %s page %s" % (LABEL[kind], nn.lstrip("0"), c["pvd"])), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
        for f, (eid, (ok, at, how)) in ver.items():
            if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
        lines = []; bad = []
        for name, ks in ELEM:
            okk = all(V[k][0] for k in ks)
            if not okk: bad.append(name)
            lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:80], "verified" if V[k][0] else "NOT verified", OUT[k][:260]) for k in ks)))
        ex = ["Ev34c%s_%s" % (nn, k) for k, _, _ in K]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files)
        DEV = "The page tests 9.36.0, 9.35.1 and 9.34.1 were RUN by the builder session on this page, serially, on 2026-10-23 (logs in 08-tooling/verify/iter19/pages), not read from the executor's logs. The link check (pages_link_verify) is not an element of the criterion; it exits 1 with 6 register links not carried, the same 6 lines as for the page 9.82.0 (printed in the executor's log link_verify_page_v9_83_0.log); this is disclosed, not waived."
        res[nn] = (bad, lines)
        if not bad:
            L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), page %s of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, c["pvd"], nn.lstrip("0"), " | ".join(lines), DEV))))
            i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
            t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
            L.append(C.transition("Done34T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (c["commits"][-1], end, nxt, now), TK + " completed"))
            L.append('ex:Harness34C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
            L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits %s to %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], c["sess"], len(c["commits"]), c["commits"][0], c["commits"][-1], CRIT, DEV))))
            # the Verify task: Ready, started and Done on the same runs
            i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
            tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
            r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
            import time; time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
            t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
            L.append(C.transition("Ready34T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
            L.append(C.transition("Begin34T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
            L.append(C.transition("Done34T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified; the page tests are the builder's runs of the control, not run a second time; recorded as printed." % fin, VT + " completed"))
            L.append('ex:Harness34V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
            L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version; the page tests 9.36.0, 9.35.1 and 9.34.1 were run once by the builder, serially, on 2026-10-23 and are not run a second time (the precedent of the chapter 10 Verify task). Manifest equality: %s." % (now[:10], TK, OUT["manifest"]))))
        else:
            L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), page %s of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: NOT MET: %s. A unit whose element fails is named failing and is not Done (the criterion is not edited). %s" % (now[:10], nxt, c["pvd"], nn.lstrip("0"), " | ".join(lines), "; ".join(bad), DEV))))
            why = ("Paused %s UTC, not Done: the control re-ran the three page tests and the checks on the page %s; elements not met: %s (the failing evidence is recorded evidenceVerified false, nothing is waived). The criterion %s is not edited. The task is paused, not cancelled; the repair is a new rebuild of the page as a new file by the change route. The Verify task stays Proposed." % (now, c["pvd"], "; ".join(bad), CRIT))
            i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
            t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
            L.append(C.transition("Susp34T_" + TK, TK, "T_Suspend", now, why, TK + " suspended"))
            L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, evs, lit("Control %s: NOT Done. Delivered by the executor session %s (%d commits %s to %s). Facts measured by this control: the three page tests were run on page 9.83.0; failing checks are recorded evidenceVerified false; the element notes are in %s. %s" % (now[:10], c["sess"], len(c["commits"]), c["commits"][0], c["commits"][-1], CRIT, DEV))))
    stat = {nn: ("MET" if not res[nn][0] else "NOT MET (%s)" % "; ".join(res[nn][0])) for nn in CHS}
    for nn in CHS:
        if not res[nn][0]: L.append('ex:ST_Charset_Page_Ch%s backlog:hasAuditNote %s .\n' % (nn, lit("Control %s (record v%s): AC6R_Page_Ch%s MET on page 9.83.0; TK_Charset_Page_Ch%s_Build and TK_Charset_Page_Ch%s_Verify are Done on bridge-verified evidence and a harness each." % (now[:10], nxt, nn, nn, nn))))
        else: L.append('ex:ST_Charset_Page_Ch%s backlog:hasAuditNote %s .\n' % (nn, lit("Control %s (record v%s): AC6R_Page_Ch%s %s on page 9.83.0. The story stays InProgress (G125); TK_Charset_Page_Ch%s_Build is Suspended, not Done." % (now[:10], nxt, nn, stat[nn], nn))))
    comment = "Control of Iter_19, the page rebuilds on template 9.52.2: the bridge ran every element on page 9.83.0 of chapter 5 and of chapter 6, with the three page tests re-run by the builder; chapter 5 %s; chapter 6 %s." % (stat["05"], stat["06"])
    res_ = res; t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({nn: res[nn][0] for nn in res})
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]]()
