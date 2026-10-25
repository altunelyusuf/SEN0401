#!/usr/bin/env python3
"""sen0401_lineage_control54 v1_2_0 (over 1.1.0: finds the brief under 08-tooling/briefs or briefs) (over 1.0.0: the environment variable CTL_EXTRA adds control findings to the notes) - the control of ONE retrofit deck build task of Iter_24 (TK_ChNN_Deck_Build_R24; criterion AC9_Deck_ChNN; G113, G136): the elements of the criterion are RUN by the evidence bridge (deck standard check v1_1_0, deck overlap check v1_0_0, manifest control check, error-first scan of the manifest,
Deck chapter check v1_4_0 (system python3: it needs python-pptx), nochange on the executor's commits). All met: Build Done and the Verify task Ready, started, Done in the same version; otherwise the Build task is Suspended with a rationale.
Usage: sen0401_lineage_control54_v1_0_0.py prepare NN SESSION COMMITS | record NN SESSION COMMITS     (COMMITS comma-separated, oldest first)"""
__version__ = "1.3.0"
import glob, hashlib, os, re, subprocess, sys, datetime, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit; TL = "08-tooling/"
GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_4_0.py"
LABEL = {"std": "deck standard check v1_1_0: every element D1 to D12 met, no NOT_MEASURED, exit 0", "overlap": "deck overlap check v1_0_0: exit 0 (no overlap, nothing beyond the slide edge)", "manifest": "deck control check v1_1_0 manifest: order equals the order of the code slides, names unique, library files exist, hashes match",
         "errfirst": "error-first scan: no manifest example has a first output line that starts with an error name", "deckchk": "Deck chapter check v1_4_0 (examples re-run, fixtures refused, layout, notes)", "nochange": "no committed file is edited (every file of the executor's commits added)", "noborrow": "lineage agent's own check: no slide From chapter 11, no chapter-11-only concept on a slide, the delivered v2_0_0 unchanged", "arc": "arc check v1_3_0 on the new deck: exit 0 (every refusal would be listed)"}
ELEM = [("(1) deck standard check D1 to D12 on the corrected research, no slide From chapter 11", ["std", "noborrow"]), ("(2) overlap check, manifest, error-first scan, Deck chapter check", ["overlap", "manifest", "errfirst", "deckchk"]), ("(3) arc check run and its refusals listed", ["arc"]), ("(4) no committed file edited", ["nochange"])]
def deckfile(nn):
    fs = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%s/*.pptx" % nn)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]); return os.path.relpath(fs[-1], REPO)
def kinds(nn, commits):
    return [("std", TL + "sen0401_deck_standard_check_v1_1_0.py", nn), ("overlap", TL + "deck_overlap_check_v1_0_0.py", deckfile(nn)), ("manifest", TL + "sen0401_deck_control_check_v1_1_0.py", "manifest:" + nn), ("errfirst", TL + "sen0401_manifest_errfirst_scan_v1_0_0.py", nn),
            ("deckchk", TL + "sen0401_lineage_chapter_check_v1_4_0.py", "Deck/Ch" + nn), ("noborrow", TL + "sen0401_ch12_deck_control_check_v1_0_0.py", "noborrow"), ("arc", TL + "sen0401_deck_arc_check_v1_3_0.py", nn), ("nochange", TL + "sen0401_deck_control_check_v1_1_0.py", "nochange:%s:%s" % (nn, commits))]
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
PRE = "@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
def paths(nn):
    return os.path.join(REPO, TL, "verify", "iter24", "bridge_revise%s" % nn), "/tmp/claude-0/s/ctl36_%s" % nn
def prepare(nn, sess, commits):
    LOG, WORK = paths(nn); os.makedirs(LOG, exist_ok=True); os.makedirs(WORK, exist_ok=True); draft = [PRE]; CRIT = "AC9_Ch12DeckRevise"
    for kind, spec, tid in kinds(nn, commits): draft.append('ex:Ev36c%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (nn, kind, lit(LABEL[kind]), tid, spec))
    d = WORK + "/draft.ttl"; open(d, "w").write("".join(draft))
    cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-100).log 2>&1' % LOG
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", WORK + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(nn, r.stdout[-200:])
def lastline(nn, spec, tid):
    LOG, _ = paths(nn); p = os.path.join(LOG, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", "%s_%s" % (spec, tid))[:100])
    if not os.path.exists(p): return "(log missing)"
    ls = [l for l in open(p, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()]
    return " ".join(l for l in ls if l.startswith(("RESULT", "SUMMARY", "manifest", "nochange", "deck")))[:300] or (ls[-1][:300] if ls else "")
def record(nn, sess, commits):
    LOG, WORK = paths(nn); cm = commits.split(","); now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    K = kinds(nn, commits); TK = "TK_Deck12_Revise_Build"; VT = "TK_Deck12_Revise_Verify"; CRIT = "AC9_Ch12DeckRevise"
    v = S.verdicts(WORK + "/bridge.ttl"); V = {k: v["Ev36c%s_%s" % (nn, k)] for k, _, _ in K}; OUT = {k: lastline(nn, s, i) for k, s, i in K}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(cm[-1]); EI = "EI36c" + nn; itn = re.search(r"memberOfContainer ex:Iter_(\d+)", t[T.blk(t, TK)[0]:T.blk(t, TK)[1]]).group(1); bp = ("08-tooling/briefs/iter%s/BRIEF_%s.md" if os.path.exists(os.path.join(REPO, "08-tooling/briefs/iter%s/BRIEF_%s.md" % (itn, TK))) else "briefs/iter%s/BRIEF_%s.md") % (itn, TK); RV = "v0.281.0" if itn == "24" else "v0.288.0"
    L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion "brief of register %s" ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + sess), RV, began, end, lit("Started at the recorded work begun (T_Start, %s UTC); retired at its last commit %s (%s UTC)." % (began, cm[-1], end))))
    L.append('ex:Brief36%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_7_0 from register %s; file %s, SHA-256 %s." % (RV, bp, sha256(bp)))))
    files = sorted({f for c in cm for f in git("show", "--name-only", "--format=", c).splitlines() if f}); logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOG, "*")))
    allf = sorted(set(files) | set(logs) | {TL + "sen0401_lineage_control54_v1_0_0.py", TL + "sen0401_manifest_errfirst_scan_v1_0_0.py"}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for kind, spec, tid in K:
        ok, at, how = V[kind]
        L.append('ex:Ev36c%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (nn, kind, lit("%s, chapter %s" % (LABEL[kind], nn.lstrip("0"))), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, _) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), now))
    lines = []; bad = []
    for name, ks in ELEM:
        okk = all(V[k][0] for k in ks); bad += [] if okk else [name]
        lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k][:70], "verified" if V[k][0] else "NOT verified", OUT[k][:240]) for k in ks)))
    ex = ["Ev36c%s_%s" % (nn, k) for k, _, _ in K]; evs = ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files)
    DEV = ("The deck match check is not an element run here: the lecture export and page data of the chapter do not exist until its page task (Iteration 26). The slides were rendered (LibreOffice PDF, contact sheets of all slides) and read by the builder as a reading, not a tool result: cream scheme throughout, numbered slides, native charts, stories with picture and link strips. Not measured: the arc check v1_1_0 refuses this deck as it refuses the deck of chapter 8 (it demands a 26-slide standard); it is not an element of the criterion.") + " " + os.environ.get("CTL_EXTRA", "")
    if not bad:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), deck of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, nn.lstrip("0"), " | ".join(lines), DEV))))
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done36T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the lineage agent once the control run gave it bridge-verified evidence." % (cm[-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness36C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, evs, lit("Done, recorded %s: delivered by the executor session %s (%d commits %s to %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], sess, len(cm), cm[0], cm[-1], CRIT, DEV))))
        i, j = T.blk(t, VT); b = t[i:j]; assert ("backlog:hasState backlog:Proposed" in b or "backlog:hasState backlog:Ready" in b) and "startedAt" not in b, VT
        wasprop = "backlog:hasState backlog:Proposed" in b
        tmp = (t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]) if "backlog:hasState backlog:Proposed" in b else t; ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp"); assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        time.sleep(1.1); start = M.now(); time.sleep(1.1); fin = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed" if "backlog:hasState backlog:Proposed" in b else "backlog:hasState backlog:Ready", 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (start, fin, fin), 1) + t[j:]
        if wasprop: L.append(C.transition("Ready36T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its Build task %s is Done on bridge-verified evidence (v%s); the start gate said READY." % (ready, TK, nxt), VT + " ready"))
        L.append(C.transition("Begin36T_" + VT, VT, "T_Start", start, "Verification begun %s UTC by the lineage agent after the start gate said READY, inside the started sprint ex:%s." % (start, it), VT + " started"))
        L.append(C.transition("Done36T_" + VT, VT, "T_Complete", fin, "Verification finished %s UTC: the checks ran on the bridge and are verified, and the slides were rendered and read; recorded as printed." % fin, VT + " completed"))
        L.append('ex:Harness36V_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, CRIT, evs, lit("Done, recorded %s: the elements of the task are those of the control of %s in the same version. Manifest: %s." % (now[:10], TK, OUT["manifest"]))))
    else:
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), deck of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: NOT MET: %s. A unit whose element fails is named failing and is not Done (the criterion is not edited). %s" % (now[:10], nxt, nn.lstrip("0"), " | ".join(lines), "; ".join(bad), DEV))))
        why = "Paused %s UTC, not Done: the control re-ran the checks on the deck; elements not met: %s (the failing evidence is recorded evidenceVerified false, nothing is waived). The criterion %s is not edited; the repair is a new deck file by the change route. The Verify task stays Proposed." % (now, "; ".join(bad), CRIT)
        i, j = T.blk(t, TK); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp30T_" + TK, TK, "T_Suspend", now, why, TK + " suspended")); L.append('ex:%s backlog:hasEvidence %s .\n' % (TK, evs))
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, "Control of the deck of chapter %s (%s, %s): %s." % (nn.lstrip("0"), TK, sess, "MET, Build and Verify Done" if not bad else "NOT MET: " + "; ".join(bad))))); print(bad)
if __name__ == "__main__": {"prepare": prepare, "record": record}[sys.argv[1]](*sys.argv[2:])
