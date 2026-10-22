#!/usr/bin/env python3
"""sen0401_lineage_control25 v1_0_0 - the two deck Verify tasks of Iter_17 (TK_Remedy_Deck_Ch05_Verify, TK_Remedy_Deck_Ch06_Verify), run by the builder session after the Build task and TK_Remedy_DeckCheck are Done (G113, G136).
start    each task goes Proposed -> Ready (T_Refine) -> InProgress (T_Start) after the start gate says READY; both dependencies must be Done
prepare  the bridge runs every check of the task again (deck standard check, overlap scan, Deck chapter check, deck match, manifest order, no file edited), logs in 08-tooling/verify/iter17/deck_verify
record   each task goes Done (T_Complete) with its own bridge-verified evidence and a harness; the three-role reading is recorded as a reading, not as a tool result
Usage: sen0401_lineage_control25_v1_0_0.py start|prepare|record"""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
import sen0401_lineage_control22_v1_0_0 as K5
import sen0401_lineage_control23_v1_0_0 as K6
lit = C.lit; REPO = M.REPO; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_2_0.py"
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter17", "deck_verify"); WORK = "/tmp/claude-0/s/ctl25"
CH = {"05": dict(K=K5, vt="TK_Remedy_Deck_Ch05_Verify", bt="TK_Remedy_Deck_Ch05_Build", crit="AC4R_Deck_Ch05", slides=68, code=27, charts=5, tag="c5"),
      "06": dict(K=K6, vt="TK_Remedy_Deck_Ch06_Verify", bt="TK_Remedy_Deck_Ch06_Build", crit="AC4R_Deck_Ch06", slides=62, code=18, charts=7, tag="c6")}
PRE = K5.PRE; DC = "TK_Remedy_DeckCheck"
def start():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); ev = ""; names = []
    for nn, c in CH.items():
        VT = c["vt"]; i, j = T.blk(t, VT); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b and "startedAt" not in b, VT
        for dep in (c["bt"], DC): assert re.search(r"backlog:hasState backlog:Done", t[T.blk(t, dep)[0]:T.blk(t, dep)[1]]), dep + " is not Done"
        tmp = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]; ready = M.now(); open(src + ".gate.tmp", "w").write(tmp)
        r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", VT], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, VT + " is not READY: " + r.stdout[-300:]
        now = M.now(); it = re.search(r"memberOfContainer ex:(Iter_\d+)", b).group(1)
        t = t[:i] + b.replace("backlog:hasState backlog:Proposed", 'backlog:hasState backlog:InProgress ; backlog:startedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
        ev += C.transition("Ready25T_" + VT, VT, "T_Refine", ready, "Ready at %s UTC: its dependencies %s and %s are Done on bridge-verified evidence (v%s)." % (ready, c["bt"], DC, cur), VT + " ready")
        ev += C.transition("Begin25T_" + VT, VT, "T_Start", now, "Verification begun %s UTC by the builder session after the start gate said READY, inside the started sprint ex:%s." % (now, it), VT + " started"); names.append(VT)
    t = X.set_status(t + "\n" + ev, "LS_InProgress")
    print(os.path.basename(M.write_new(src, t, nxt, cur, "Verify tasks %s made Ready and started (start gate READY, dependencies Done)." % ", ".join(names))))
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True)
    for nn, c in CH.items():
        K = c["K"]; draft = [PRE]
        for kind, spec, tid in K.KINDS: draft.append('ex:Ev25%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (c["tag"], kind, lit("Verify run: " + K.LABEL[kind]), tid, spec))
        d = "%s/draft%s.ttl" % (WORK, nn); open(d, "w").write("".join(draft))
        cmd = 'python3 -B {spec} {id} > %s/bridge_%s_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-110).log 2>&1' % (LOGDIR, nn)
        r = subprocess.run([sys.executable, C.BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", "%s/bridge%s.ttl" % (WORK, nn)], capture_output=True, text=True, env=dict(os.environ, TZ="UTC")); print(nn, r.stdout[-120:])
def lastline(nn, spec, tid):
    p = os.path.join(LOGDIR, "bridge_%s_%s.log" % (nn, re.sub(r"[^A-Za-z0-9\n]", "_", "%s_%s" % (spec, tid))[:110]))
    if not os.path.exists(p): return "(log missing)"
    ls = [l for l in open(p, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()]
    return " ".join(l for l in ls if l.startswith(("RESULT", "SUMMARY", "manifest", "nochange", "PASS", "CLEAN", "FINDINGS")))[:300] or (ls[-1][:300] if ls else "")
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    for nn, c in CH.items():
        K = c["K"]; VT = c["vt"]; tag = c["tag"]; v = S.verdicts("%s/bridge%s.ttl" % (WORK, nn)); V = {k: v["Ev25%s_%s" % (tag, k)] for k, _, _ in K.KINDS}; OUT = {k: lastline(nn, s, i) for k, s, i in K.KINDS}
        bad = [k for k in V if not V[k][0]]; assert not bad, "%s not verified: %s" % (nn, bad)
        logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "bridge_%s_*.log" % nn))); ver = C.bridge_files(logs, now); assert all(x[1][0] for x in ver.values())
        for kind, spec, tid in K.KINDS:
            ok, at, how = V[kind]
            L.append('ex:Ev25%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (tag, kind, lit("Verify run: " + K.LABEL[kind]), c["crit"], tid, spec, lit(how[:600]), at))
        for f, (eid, (ok, at, how)) in ver.items():
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), c["crit"], f, K.sha256(f), at))
        ex = ["Ev25%s_%s" % (tag, k) for k, _, _ in K.KINDS]; i, j = T.blk(t, VT); b = t[i:j]; m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, VT
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), now, now), 1) + t[j:]
        L.append(C.transition("Done25T_" + VT, VT, "T_Complete", now, "Verification finished %s UTC: the %d checks ran one after the other on the bridge and are verified; recorded as printed." % (now, len(K.KINDS)), VT + " completed"))
        L.append('ex:Harness25C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (VT, lit("Checks run for " + VT), VT, ", ".join("ex:" + e for e in ex)))
        read = ("READING (not a tool result; by the builder session, after the rendered review of the Build control, from the three roles of the owner's preference). Teaching academician: the deck follows the chapter's parts in order, each part opens with a divider that names its concepts, shows a map strip and gives the way the concepts fit together; every code slide pairs the listing with a plain-language note beside each line group and an executed result as a chart, table or diagram; stories carry 5N1K, a real picture and a live link. "
                "Reviewing faculty specialist: the code results are those the chapter library printed (the examples were re-run by the Deck chapter check and the manifest holds the expected values); the %d slides, %d code slides and %d native charts are the measured facts of the deck standard check. Student: every concept card gives the meaning and an everyday comparison; slides are numbered; the closing slides summarise and point to practice. Findings kept: %s" % (c["slides"], c["code"], c["charts"], "slide 51 chart labels crowd on the five smallest bars (recorded as a defect task of the chapter 6 deck, the coordinator decides)" if nn == "06" else "none beyond empty space on some table slides"))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (VT, c["crit"], ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + e for e, _ in ver.values()),
            lit("Done, recorded %s: the checks of the task ran one after the other on the bridge after the task started; results as printed: %s. %s" % (now[:10], " | ".join("%s: %s" % (K.LABEL[k][:70], OUT[k][:200]) for k in V), read))))
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, "Verify tasks of the decks of chapters 5 and 6 Done on bridge-verified evidence and a harness; the three-role reading recorded as a reading.")))
if __name__ == "__main__": {"start": start, "prepare": prepare, "record": record}[sys.argv[1]]()
