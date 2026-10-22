#!/usr/bin/env python3
"""sen0401_lineage_control22 v1_0_0 - the control of TK_Remedy_Deck_Ch05_Build after its executor (session SEN0401-I17-deck-ch05) reported deck v3_1_0 (commits 3fc6881, 6db1751, e5d7761) (G113, G136).
v3_0_0 is not controlled (the coordinator rendered it and found overlapping text; v3_1_0 replaces it). The evidence bridge runs every element of AC4R_Deck_Ch05 as an exit-code check:
the independent deck standard check v1_0_0 (D1 to D12), the Deck chapter check, the deck match check, the manifest order check and the no-committed-file-edited check (both new files of the control),
and the executor's overlap scan (its own tool, so not independent). The builder's own rendered review of all 68 slides (soffice, contact sheets, every slide type) is recorded as a note, not as a machine result.
TK_Remedy_Deck_Ch05_Build goes Done (T_Complete) with verified evidence and a harness. The Verify task is NOT made Ready here: it depends on TK_Remedy_DeckCheck, which is not Done yet. No story is closed.
Usage: sen0401_lineage_control22_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl22"; BRIDGE = C.BRIDGE; lit = C.lit
DECK = "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_1_0.pptx"; COMMITS = ["3fc6881", "6db1751", "e5d7761"]
CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; CK = "08-tooling/sen0401_deck_control_check_v1_0_0.py"
KINDS = [("std", "08-tooling/sen0401_deck_standard_check_v1_0_0.py", "05 " + DECK), ("overlap", "08-tooling/deck_overlap_check_v1_0_0.py", DECK), ("deckchk", CC, "Deck/Ch05"),
         ("match", "08-tooling/pages_deck_match_verify_v1_0_0.py", "05 9_74_0"), ("manifest", CK, "manifest:05"), ("nochange", CK, "nochange:05:" + ",".join(COMMITS))]
LABEL = {"std": "deck standard check v1_0_0: D1 to D12 all PASS (independent tool, python-pptx 1.0.2)", "overlap": "overlap scan v1_0_0: CLEAN (the executor's tool, not independent)", "deckchk": "chapter check Deck/Ch05 v1_3_0",
         "match": "deck match check v1_0_0: 0 not carried", "manifest": "chapter-code manifest: order equals the order of the code slides, names unique, library hashes match", "nochange": "no committed file edited (every file of the three commits added)"}
ELEM = [("(1) deck standard D1 to D12", ["std"]), ("(2) Deck chapter check and deck match", ["deckchk", "match"]), ("(3) manifest in slide order", ["manifest"]), ("(4) no committed file edited", ["nochange"])]
TK = "TK_Remedy_Deck_Ch05_Build"; CRIT = "AC4R_Deck_Ch05"; SESS = "SEN0401-I17-deck-ch05"
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter17", "deck_ch05")
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
PRE = "@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
def lg(tid): return "bridge_deck_%s.log" % re.sub(r"[^A-Za-z0-9]+", "_", tid)[:60]
def prepare():
    os.makedirs(WORK, exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); draft = [PRE]
    for kind, spec, tid in KINDS:
        draft.append('ex:Ev22C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, lit("%s, chapter 5 deck v3_1_0" % LABEL[kind]), tid, spec))
    d = os.path.join(WORK, "draft.ttl"); open(d, "w").write("".join(draft))
    open(os.path.join(WORK, "run.sh"), "w").write('#!/bin/bash\ncd /home/claude/sen0401\nL=%s\nid="$1"; spec="$2"\nout="$L/bridge_deck_$(echo "$spec $id" | tr -c "A-Za-z0-9" "_" | cut -c1-110).log"\npython3 -B $spec $id > "$out" 2>&1\n' % LOGDIR)
    cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-110).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge.ttl")], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(os.path.join(WORK, "bridge.out"), "w").write(r.stdout + r.stderr); print(r.stdout[-900:])
def lastline(kind, spec, tid):
    key = re.sub(r"[^A-Za-z0-9\n]", "_", "%s_%s" % (spec, tid))[:110]; p = os.path.join(LOGDIR, "bridge_%s.log" % key)
    if not os.path.exists(p): return "(log %s missing)" % key
    ls = [l for l in open(p, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()]
    return " ".join(l for l in ls if l.startswith(("RESULT", "SUMMARY", "manifest", "nochange", "PASS", "CLEAN", "FINDINGS", "OK")))[:300] or (ls[-1][:300] if ls else "")
def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
    v = S.verdicts(os.path.join(WORK, "bridge.ttl")); V = {k: v["Ev22C_" + k] for k, _, _ in KINDS}; OUT = {k: lastline(k, s, i) for k, s, i in KINDS}
    began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(COMMITS[-1]); bp = "08-tooling/briefs/iter17/BRIEF_%s.md" % TK
    L = ['ex:EI22_deck_ch05 a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
        lit("Executor session " + SESS), lit("brief of register v0.196, session " + SESS), began, end,
        lit("Started at the recorded work begun (T_Start, %s UTC, register v0.196) and ended with its last commit %s (%s UTC); %d commits: deck v3_0_0 (3fc6881), the overlap scan tool (6db1751) and deck v3_1_0 with its manifest (e5d7761). It reported deck v3_0_0 first; the coordinator rendered it and found overlapping text on slide 33 and others, so the executor produced v3_1_0 (overlap fixes on 12 slides). v3_0_0 was not controlled." % (began, COMMITS[-1], end, len(COMMITS))))]
    L.append('ex:Brief22_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI22_deck_ch05 ;\n    rdfs:comment %s .\n' % (
        TK, lit("Brief of " + TK), TK, CRIT, lit("Generated by sen0401_lineage_brief_remedy_v1_0_0 from register v0.195 and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = sorted({f for c in COMMITS for f in git("show", "--name-only", "--format=", c).splitlines() if f})
    logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "*")) if os.path.isfile(p))
    tools = [CK, "08-tooling/sen0401_lineage_control22_v1_0_0.py"]
    allf = sorted(set(files) | set(logs) | set(tools)); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for kind, spec, tid in KINDS:
        ok, at, how = V[kind]
        L.append('ex:Ev22C_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            kind, lit("%s, chapter 5 deck v3_1_0" % LABEL[kind]), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t: continue
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
    lines = []; bad = []
    for name, kinds in ELEM:
        okk = all(V[k][0] for k in kinds)
        if not okk: bad.append(name)
        lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[k][0] else "NOT verified", OUT[k][:240]) for k in kinds)))
    assert not bad, "criterion not met, not recorded Done: %s" % bad
    VIS = ("RENDERED REVIEW by the builder session (independent of the executor): the deck was rendered with soffice to PDF and PNG (68 pages) and every page was viewed in contact sheets of 9 slides; every slide type was seen (title, story with picture and 5N1K, dividers, code slides with explanation and result, tables, native charts, diagrams, analogy slides, resources, closing). "
           "Result: no text overlap, no clipped text, no empty slide found; slide 33 (the coordinator's finding on v3_0_0) is correct in v3_1_0. A review by eye is not a machine result and is not counted as evidence; it is recorded here. "
           "Observations, not failures: the dividers repeat a six-concept list beside a numbered 'How they fit together' panel; several table slides leave empty space below the table. "
           "DISCLOSED: (a) the criterion text names the manifest chapter_code_ch05_v1_0_0.json; the executor wrote v1_1_0 with the deck v3_1_0 (v1_0_0 is kept and belongs to v3_0_0); the control measured the newest manifest. (b) The criterion element 'the order equals the order of the code slides, measured by the deck check' is measured by a new control file sen0401_deck_control_check_v1_0_0.py because the deck standard check does not read the manifest. "
           "(c) The overlap scan is the executor's own tool; it is run as evidence but my render review is the independent part. (d) The Verify task TK_Remedy_Deck_Ch05_Verify waits for TK_Remedy_DeckCheck (Done not yet controlled); it is not made Ready.")
    L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), deck v3_1_0 of chapter 5, every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), VIS))))
    ex = ["Ev22C_" + k for k, _, _ in KINDS]
    i, j = T.blk(t, TK); b = t[i:j]
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
    t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
    L.append(C.transition("Done22T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (COMMITS[-1], end, nxt, now), TK + " completed"))
    L.append('ex:Harness22C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
    L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files),
             lit("Done, recorded %s: delivered by the executor session %s (%d commits %s to %s; deck v3_1_0, v3_0_0 not controlled). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], SESS, len(COMMITS), COMMITS[0], COMMITS[-1], CRIT, VIS))))
    L.append('ex:TK_Remedy_Deck_Ch05_Verify backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): its dependency %s is now Done; the other dependency TK_Remedy_DeckCheck is not Done yet, so the task is not startable and stays Proposed." % (now[:10], nxt, TK)))
    L.append('ex:ST_Remedy_Deck_Ch05 backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): TK_Remedy_Deck_Ch05_Build is Done (AC4R_Deck_Ch05 MET on deck v3_1_0). The story stays InProgress: its Verify task is not Done (G125)." % (now[:10], nxt)))
    comment = "Control of Iter_17, TK_Remedy_Deck_Ch05_Build: the bridge ran every element of AC4R_Deck_Ch05 on deck v3_1_0 (deck standard 12 of 12, Deck chapter check, deck match, manifest order, no committed file edited, overlap scan); the builder's rendered review of 68 slides found no overlap; the task is Done on verified evidence and a harness; executor instance and brief as links; the Verify task waits for TK_Remedy_DeckCheck."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: v[0] for k, v in V.items()})
if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
