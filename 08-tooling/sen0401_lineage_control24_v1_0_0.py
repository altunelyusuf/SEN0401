#!/usr/bin/env python3
"""sen0401_lineage_control24 v1_0_0 - the control of the three tool tasks of Iter_17 after their executors reported (G113, G136): TK_Remedy_DeckCheck (session SEN0401-I17-deckcheck), TK_Remedy_PageTest (SEN0401-I17-pagetest),
TK_Remedy_Template (SEN0401-I17-template). The evidence bridge runs every element of the task's criterion as an exit-code check (sen0401_remedy_check v1_0_0, a new file; the deck control check v1_1_0); the page tests were RUN by the builder
(serially, logs in 08-tooling/verify/iter17/tools), not read from the executors' logs. Each task goes Done (T_Complete at its executor's last commit) with verified evidence and a harness.
Usage: sen0401_lineage_control24_v1_0_0.py prepare|record dc|pt|tp   (pt and tp may be given together as 'pt,tp')"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; BRIDGE = C.BRIDGE; lit = C.lit
RC = "08-tooling/sen0401_remedy_check_v1_0_0.py"; DC = "08-tooling/sen0401_deck_control_check_v1_1_0.py"
SPEC = {
 "dc": dict(tk="TK_Remedy_DeckCheck", crit="AC4R_DeckCheck", sess="SEN0401-I17-deckcheck", commits=["271ce28"], story="ST_Remedy_Tools",
   kinds=[("old05", RC, "dcold:05"), ("old06", RC, "dcold:06"), ("hdr", RC, "dchdr"), ("logs", RC, "dclogs"), ("nochange", DC, "nochange:05:271ce28")],
   label={"old05": "deck standard check on the OLD chapter 5 deck: 23 slides, 9 code slides, 1 native chart, 0 analogies, longest box 39 words; exit non-zero; D3 D4 D10 D11 fail; D1 to D12 each named with a number",
          "old06": "deck standard check on the OLD chapter 6 deck: 26 slides, 13 code slides, 3 native charts, 0 analogies, longest box 56 words; exit non-zero; D3 D4 D10 D11 fail; D1 to D12 each named with a number",
          "hdr": "the header defines code slide, analogy, story with 5N1K, coverage and key concept", "logs": "the logs of the executor's runs are kept", "nochange": "the commit adds files only, no committed file edited"},
   elem=[("(1) new file, nothing edited", ["nochange"]), ("(2) one named result per element D1 to D12 with its measure", ["old05", "old06"]), ("(3) existing decks' facts reproduced, failing elements named, exit non-zero", ["old05", "old06"]), ("(4) header defines the measures", ["hdr"]), ("(5) logs kept", ["logs"])],
   logdir="deckcheck", dev="The deck standard check run on the two NEW decks (D1 to D12 all PASS) is recorded in the controls of the two Build tasks (v0.197.0, v0.198.0)."),
 "pt": dict(tk="TK_Remedy_PageTest", crit="AC4R_PageTest", sess="SEN0401-I17-pagetest", commits=["d4880a3", "53df93a", "3ea8a53", "5f49fb8"], story="ST_Remedy_Tools",
   kinds=[("same", RC, "ptsame"), ("nochange", DC, "nochange:05:d4880a3,53df93a,3ea8a53,5f49fb8"), ("force05", RC, "ptforce:05"), ("force06", RC, "ptforce:06"), ("skip", RC, "ptskip"), ("declared01", RC, "tpscratch:01"), ("declared10", RC, "tpscratch:10"), ("logs", RC, "ptlogs")],
   label={"same": "page test 9.35.1 unchanged; 9.36.0 differs by added lines and the version line only; every feat/skip text of 9.35.1 is in 9.36.0", "nochange": "the four commits add files only, no committed file edited",
          "force05": "RUN by the builder: FORCE_STANDARD=1 on the shipped chapter 5 page 9.74.0 ends without a crash and fails the features naming the measured defects (select 4861 px, no chapter-code tab, 8 of 8 repeated labels, panels over one screen)",
          "force06": "RUN by the builder: FORCE_STANDARD=1 on the shipped chapter 6 page 9.75.0 ends without a crash and fails the features naming the measured defects (select 5836 px, no chapter-code tab, repeated labels, panels over one screen)",
          "skip": "RUN by the builder: without the force the added features are SKIP with their reason on a page that does not declare the standard (shipped chapter 10 page 9.79.0), none FAIL",
          "declared01": "RUN by the builder: on a scratch page of chapter 1 that declares the standard the added features apply and P1 P3 P4 P5 P6 P8 P9 pass", "declared10": "RUN by the builder: the same on a scratch page of chapter 10 with a manifest fixture (P2 and P11 apply and pass)", "logs": "the executor's logs are kept"},
   elem=[("(1) new file, 9.35.1 byte-identical", ["same", "nochange"]), ("(2) every feature text of 9.35.1 present, only added code", ["same"]), ("(3) P features apply to a declaring page, SKIP otherwise, FORCE applies to any", ["declared01", "declared10", "skip", "force05", "force06"]), ("(4) FORCE_STANDARD on chapters 5 and 6 fails the measured defects, no crash", ["force05", "force06"]), ("(5) logs kept", ["logs"])],
   logdir="tools", dev="The runs of the criterion's element (4) were repeated by the builder on the shipped pages (the executor's own runs of chapter 6 had one flaked run on a busy machine; its second run is kept)."),
 "tp": dict(tk="TK_Remedy_Template", crit="AC4R_Template", sess="SEN0401-I17-template", commits=["c62c579", "af9b390"], story="ST_Remedy_Tools",
   kinds=[("nochange", DC, "nochange:05:c62c579,af9b390"), ("old", RC, "tpold"), ("dom", RC, "tpdom"), ("facts", RC, "tpfacts"), ("scratch01", RC, "tpscratch:01"), ("scratch10", RC, "tpscratch:10")],
   label={"nochange": "the two commits add files only, no committed file edited, no gate, test or threshold changed", "old": "template 9.51.1, page builder v4_14_0 and page-data builder v2_23_0 byte-identical (committed once, clean against HEAD)",
          "dom": "the DOM contract hooks are in template 9.52.0, every id of 9.51.1 is kept, the template and both builders are new files", "facts": "the report states how the page runs code today and what runtime the chapter libraries need",
          "scratch01": "RUN by the builder: a scratch page of chapter 1 built on 9.52.0 declares the standard and page test 9.36.0 passes P1 P3 P4 P5 P6 P8 P9 (no manifest: the chapter-code features SKIP)",
          "scratch10": "RUN by the builder: a scratch page of chapter 10 built on 9.52.0 with the executor's fixture manifest passes P1 P3 P4 P5 P6 P8 P9 and the chapter-code features"},
   elem=[("(1) files new, old ones byte-identical", ["nochange", "old"]), ("(2) DOM contract kept, ids of 9.51.1 kept, runtime facts stated", ["dom", "facts"]), ("(3) scratch pages of chapters 1 and 10 pass the page-standard features", ["scratch01", "scratch10"]), ("(4) no gate, test or threshold changed", ["nochange"])],
   logdir="tools", dev="The scratch pages were BUILT AGAIN by the builder from the committed template and builders (not the executor's scratch pages). The chapter 10 scratch page uses the executor's committed fixture manifest, which is not a deck manifest; the chapter 5 and 6 pages carry the real manifests in their own tasks."),
}
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
PRE = "@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
LOGDIR = os.path.join(REPO, "08-tooling", "verify", "iter17", "bridge24")
def W(g): return os.path.join("/tmp/claude-0/s/ctl24", g)
def prepare(g):
    os.makedirs(W(g), exist_ok=True); os.makedirs(LOGDIR, exist_ok=True); sp = SPEC[g]; draft = [PRE]
    for kind, spec, tid in sp["kinds"]:
        draft.append('ex:Ev24%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (g, kind, lit(sp["label"][kind]), tid, spec))
    d = W(g) + "/draft.ttl"; open(d, "w").write("".join(draft))
    cmd = 'python3 -B {spec} {id} > %s/bridge_$(echo "{spec}_{id}" | tr -c "A-Za-z0-9\\n" "_" | cut -c1-110).log 2>&1' % LOGDIR
    r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", W(g) + "/bridge.ttl"], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
    open(W(g) + "/bridge.out", "w").write(r.stdout + r.stderr); print(g, r.stdout[-300:])
def lastline(spec, tid):
    p = os.path.join(LOGDIR, "bridge_%s.log" % re.sub(r"[^A-Za-z0-9\n]", "_", "%s_%s" % (spec, tid))[:110])
    if not os.path.exists(p): return "(log missing)"
    ls = [l for l in open(p, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()]; return (ls[-1] if ls else "")[:420]
def record(groups):
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; done = []
    for g in groups:
        sp = SPEC[g]; TK = sp["tk"]; CRIT = sp["crit"]; KINDS = sp["kinds"]; v = S.verdicts(W(g) + "/bridge.ttl"); V = {k: v["Ev24%s_%s" % (g, k)] for k, _, _ in KINDS}; OUT = {k: lastline(s, i) for k, s, i in KINDS}
        began = re.search(r'ex:Begin3T_%s a backlog:TransitionEvent.*?transitionedAt "([^"]*)"' % TK, t, re.S).group(1); end = utc(sp["commits"][-1]); bp = "08-tooling/briefs/iter17/BRIEF_%s.md" % TK; EI = "EI24%s_%s" % (g, TK)
        L.append('ex:%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (EI, lit("Executor session " + sp["sess"]), lit("brief of register v0.196, session " + sp["sess"]), began, end,
            lit("Started at the recorded work begun (T_Start, %s UTC, register v0.196) and ended with its last commit %s (%s UTC); %d commit(s): %s." % (began, sp["commits"][-1], end, len(sp["commits"]), ", ".join(sp["commits"])))))
        L.append('ex:Brief24%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:%s ;\n    rdfs:comment %s .\n' % (TK, lit("Brief of " + TK), TK, CRIT, EI, lit("Generated by sen0401_lineage_brief_remedy_v1_0_0 from register v0.195 and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
        files = sorted({f for c in sp["commits"] for f in git("show", "--name-only", "--format=", c).splitlines() if f})
        logs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling", "verify", "iter17", "tools", "*")) if os.path.isfile(p)) if g != "dc" else []
        blogs = sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR, "*")) if os.path.isfile(p) and any(kk in os.path.basename(p) for kk in [re.sub(r"[^A-Za-z0-9]", "_", i)[:20] for _, _, i in KINDS]))
        tools = [RC, DC, "08-tooling/sen0401_lineage_control24_v1_0_0.py"]; allf = sorted(set(files) | set(logs) | set(blogs) | set(tools)); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
        for kind, spec, tid in KINDS:
            ok, at, how = V[kind]
            L.append('ex:Ev24%s_%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (g, kind, lit(sp["label"][kind]), CRIT, tid, spec, "true" if ok else "false", lit(how[:600]), at))
        for f, (eid, (ok, at, how)) in ver.items():
            if ("ex:%s a backlog:ArtifactEvidence" % eid) in t or ("ex:%s a backlog:ArtifactEvidence" % eid) in "".join(L): continue
            L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion ex:%s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (eid, lit(os.path.basename(f)), CRIT, f, sha256(f), at))
        lines = []; bad = []
        for name, kinds in sp["elem"]:
            okk = all(V[k][0] for k in kinds)
            if not okk: bad.append(name)
            lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (sp["label"][k][:90], "verified" if V[k][0] else "NOT verified", OUT[k][:230]) for k in kinds)))
        assert not bad, "criterion not met, not recorded Done: %s" % bad
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT, lit("Control %s (record v%s), every element run by the evidence bridge and recorded as printed: %s. RESULT: MET: all elements are met. %s" % (now[:10], nxt, " | ".join(lines), sp["dev"]))))
        ex = ["Ev24%s_%s" % (g, k) for k, _, _ in KINDS]; i, j = T.blk(t, TK); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, TK
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), end, now), 1) + t[j:]
        L.append(C.transition("Done24T_" + TK, TK, "T_Complete", end, "Done on the executor's last commit %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (sp["commits"][-1], end, nxt, now), TK + " completed"))
        L.append('ex:Harness24C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (TK, lit("Checks run for " + TK), TK, ", ".join("ex:" + e for e in ex)))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ;\n    backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (TK, CRIT, ", ".join("ex:" + e for e in ex) + ", " + ", ".join("ex:" + ver[f][0] for f in files),
            lit("Done, recorded %s: delivered by the executor session %s (%d commit(s), %s). The checks and their results are those of the evidence nodes and the note of %s. %s" % (now[:10], sp["sess"], len(sp["commits"]), ", ".join(sp["commits"]), CRIT, sp["dev"]))))
        done.append(TK)
    L.append('ex:ST_Remedy_Tools backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): %s Done on bridge-verified evidence. The story stays InProgress: TK_Remedy_Regress (the builder's Verify task) is not Done (G125)." % (now[:10], nxt, ", ".join(done))))
    comment = "Control of Iter_17 tool tasks %s: the bridge ran every element of the criterion; Done on verified evidence and a harness; executor instances and briefs as links; ST_Remedy_Tools stays InProgress." % ", ".join(done)
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({g: {k: v[0] for k, v in S.verdicts(W(g) + "/bridge.ttl").items()} for g in groups})
if __name__ == "__main__":
    gs = sys.argv[2].split(",")
    if sys.argv[1] == "prepare": [prepare(g) for g in gs]
    else: record(gs)
