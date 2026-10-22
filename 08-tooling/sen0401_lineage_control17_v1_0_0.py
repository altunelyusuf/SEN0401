#!/usr/bin/env python3
"""sen0401_lineage_control17 v1_0_0 - the control of the two page tasks of Iter_14 (G113, G136) after the executors stopped with failing page tests.
The evidence bridge runs every element of AC3L_Ch10 and AC3L_Ch11 (and the AC3T elements on page 9.78.0) as an exit-code check (sen0401_lineage_page_check v1_1_0, the Stage 4 runner, the chapter checks); the page tests were run by
sen0401_lineage_verify_page v1_1_0 (logs in 08-tooling/verify/iter14/chNN). The record: executor instances and briefs as links; the evidence per element (failing checks evidenceVerified false); the criteria NOT MET element by element;
the two Build tasks NOT Done (T_Suspend, with a rationale: their text asks for stored page-test results and the Stage 4 page ABox, and a unit whose gate fails is named failing and is not Done); the Verify tasks unchanged (their dependency is not Done);
ST_Section_Links stays InProgress; the root cause as facts; the change request with its impact assessment and ONE owner question. No execution task is created.
Usage: sen0401_lineage_control17_v1_0_0.py prepare|record"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys, datetime, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl17"; BRIDGE = C.BRIDGE; lit = C.lit
CHK = "08-tooling/sen0401_lineage_page_check_v1_1_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
KINDS = [("markers", CHK, "markers:%s"), ("deck", CHK, "deck:%s"), ("link", CHK, "link:%s"), ("seclinks", CHK, "seclinks:%s"), ("erd", CHK, "erd:%s"), ("test34", CHK, "test34:%s"), ("test35", CHK, "test35:%s"),
         ("counts34", CHK, "counts34:%s"), ("counts35", CHK, "counts35:%s"), ("abox", CHK, "abox:%s"), ("nochange", CHK, "nochange:%s"), ("stage4", S4, "%s"), ("research", CC, "Research/Ch%s"), ("deckchk", CC, "Deck/Ch%s"), ("pagechk", CC, "Page/Ch%s")]
LABEL = {"markers": "template markers in the page HTML", "deck": "deck match: 0 not carried", "link": "link check: 0 not carried", "seclinks": "section links declared between sections, every section covered",
         "erd": "page test 9.35.0: both ERD label features run with no skip and pass, labels shown after Untangle at least 95 percent", "test34": "page test 9.34.0: no failure", "test35": "page test 9.35.0: no failure",
         "counts34": "page test 9.34.0 counts against the stored result of page 9.77.0", "counts35": "page test 9.35.0 counts against the stored result of page 9.77.0", "abox": "Stage 4 page ABox and stored page-test result exist as new files for page 9.78.0",
         "nochange": "no committed file edited by the executor (every file of its commits added)", "stage4": "Stage 4 gate runner v1_1_0 (current validator v1.13.0)", "research": "chapter check Research v1_3_0 (pinned validator v1.6.0)",
         "deckchk": "chapter check Deck", "pagechk": "chapter check Page"}
ELEM = [("(1) links", ["seclinks"]), ("(2) ERD", ["erd"]), ("(3) gates", ["stage4", "research", "deckchk", "pagechk"]), ("(4) AC3T elements", ["markers", "deck", "erd", "test34", "test35", "counts34", "counts35", "abox"]), ("(5) nothing changed", ["nochange"])]
AC3T = ["markers", "deck", "erd", "test34", "test35", "counts34", "counts35", "abox"]
CRIT = {"10": "AC3L_Ch10", "11": "AC3L_Ch11"}; TCRIT = {"10": "AC3T_Ch10", "11": "AC3T_Ch11"}
TASK = {"10": "TK_SecLinks_Ch10_Page", "11": "TK_SecLinks_Ch11_Page"}; SESS = {"10": "SEN0401-I14-page-ch10", "11": "SEN0401-I14-page-ch11"}
COMMITS = {"10": ["a52911a"], "11": ["7aaba8d", "2de9dcf"]}; START = "099124d"
def git(*a): return subprocess.run(["git"] + list(a), cwd=REPO, capture_output=True, text=True).stdout.strip()
def utc(sha): return datetime.datetime.fromisoformat(git("log", "-1", "--format=%cI", sha)).astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
sha256 = lambda p: hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
LOGDIR = lambda nn: os.path.join(REPO, "08-tooling", "verify", "iter14", "ch" + nn)


def prepare():
    os.makedirs(WORK, exist_ok=True)
    for nn in ("10", "11"):
        draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
        for kind, spec, tid in KINDS:
            draft.append('ex:Ev7C_%s_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, nn, lit("%s, chapter %s, page 9.78.0" % (LABEL[kind], nn)), tid % nn, spec))
        d = os.path.join(WORK, "draft_%s.ttl" % nn); open(d, "w").write("".join(draft))
        cmd = "python3 -B {spec} {id} > %s/bridge_page_$(echo {id} | tr '/:' '__').log 2>&1" % LOGDIR(nn)
        r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge_%s.ttl" % nn)], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
        open(os.path.join(WORK, "bridge_%s.out" % nn), "w").write(r.stdout + r.stderr); print(nn, r.stdout[-200:])


def record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    V = {}; OUT = {}
    for nn in ("10", "11"):
        v = S.verdicts(os.path.join(WORK, "bridge_%s.ttl" % nn))
        for kind, spec, tid in KINDS:
            V[(kind, nn)] = v["Ev7C_%s_Ch%s" % (kind, nn)]
            lg = os.path.join(LOGDIR(nn), "bridge_page_%s.log" % (tid % nn).replace("/", "_").replace(":", "_"))
            OUT[(kind, nn)] = [l for l in open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() if l.strip()][-1][:300] if os.path.exists(lg) else ""
    pushed = utc(START)
    for nn in ("10", "11"):
        tk = TASK[nn]; end = utc(COMMITS[nn][-1]); bp = "08-tooling/briefs/iter14/BRIEF_%s.md" % tk
        L.append('ex:EI7_ch%s a backlog:ExecutorInstance ; rdfs:label %s@en ; backlog:instanceOf ex:Executor_ClaudeCodeSession ;\n    backlog:instantiatedFromVersion %s ; backlog:instantiatedAt "%s"^^xsd:dateTime ; backlog:retiredAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s .\n' % (
            nn, lit("Executor session " + SESS[nn]), lit("brief of register v0.161 as regenerated for v0.172, session " + SESS[nn]), pushed, end,
            lit("Started after the push of v0.172 (commit %s, %s UTC), the earliest the session could begin, not a clock reading of the session. It ended with its last commit %s (%s UTC), stopping because the page tests failed, as its brief ordered." % (START, pushed, ", ".join(COMMITS[nn]), end))))
        L.append('ex:Brief7_%s a backlog:ExecutorBrief ; rdfs:label %s@en ; backlog:briefFor ex:%s ; backlog:briefCriterion ex:%s ; backlog:briefedExecutorInstance ex:EI7_ch%s ;\n    rdfs:comment %s .\n' % (
            tk, lit("Brief of " + tk), tk, CRIT[nn], nn, lit("Generated by sen0401_lineage_brief_v1_2_0.py and passed by the coordinator; file %s, SHA-256 %s." % (bp, sha256(bp)))))
    files = {nn: sorted({f for c in COMMITS[nn] for f in git("show", "--name-only", "--format=", c).splitlines() if f}) for nn in ("10", "11")}
    logs = {nn: sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(LOGDIR(nn), "*")) if os.path.isfile(p)) for nn in ("10", "11")}
    allf = sorted({f for nn in files for f in files[nn] + logs[nn]}); ver = C.bridge_files(allf, now); assert all(x[1][0] for x in ver.values()), "a file is not verified"
    for nn in ("10", "11"):
        for kind, spec, tid in KINDS:
            ok, at, how = V[(kind, nn)]
            crits = [CRIT[nn]] + ([TCRIT[nn]] if kind in AC3T else [])
            L.append('ex:Ev7C_%s_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
                kind, nn, lit("%s, chapter %s, page 9.78.0" % (LABEL[kind], nn)), ", ".join("ex:" + c for c in crits), tid % nn, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        if ("ex:%s a backlog:ArtifactEvidence" % eid) in t: continue   # already recorded by an earlier control with the same hash
        nns = [nn for nn in ("10", "11") if f in files[nn] or f in logs[nn]]
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), ", ".join("ex:" + CRIT[n] for n in nns) or "ex:AC3L_Ch10", f, sha256(f), at))
    res = {}
    for nn in ("10", "11"):
        lines = []; bad = []
        for name, kinds in ELEM:
            okk = all(V[(k, nn)][0] for k in kinds)
            if not okk: bad.append(name)
            lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[(k, nn)][0] else "NOT verified", OUT[(k, nn)][:200]) for k in kinds)))
        res[nn] = (not bad, bad, lines)
    FACT = {"10": "Facts measured by this control (page 9.78.0, template 9.51.0, tests 9.34.0 and 9.35.0, one run each, 366 passed and 4 failed in each: two distinct features, each reported twice): (A) the feature 'the ERD's sections choice draws one entity per section with the mentioned-together relationships on by default (the toggle removes them)' fails: sections 17, relations 23 -> 23 with mentions off; the page has 0 'mentions' relations because the new links are all 'operates on'-type links stated in the research, and the test requires the mentions toggle to remove at least one relation; (B) the feature 'relocate on the concept map ... Untangle leaves no two boxes overlapping' fails: 24 boxes, 2 overlap; the ERD label features themselves run and PASS (labels shown 23 -> 23, overlaps 0/0).",
            "11": "Facts measured by this control (page 9.78.0, template 9.51.0, tests 9.34.0 and 9.35.0, one run each): both runs stopped before their end with a click timeout ('HeaderFields intercepts pointer events': the SVG rect of the box HeaderFields sits over the element the test clicks), 161 features passed and 1 failed, widgets not reported; the feature (A) 'the ERD's sections choice ... mentioned-together relationships on by default' fails: sections 16, relations 32 -> 32 with mentions off, 0 'mentions' relations; the filled-ERD label feature PASSES (32 labels, 0 overlapping pairs); the on-choice labels feature was NOT reached in these runs. The executor's earlier run crashed the same way, so the crash is seen in three runs of three; the executor's force-click diagnostic (kept as a log, not a result) reported the same two failing features as chapter 10, including 4 of 22 boxes overlapping after Untangle; that overlap count is the executor's, not measured by this control. The first run of each test is the only run: a [FAIL] line is a result, not a budget failure, so no re-run was due."}
    ROOT = ("ROOT CAUSE as facts. (1) The page test 9.35.0 asserts that any page whose chapter has relations between two sections shows 'mentioned-together' relations that the toggle removes (rels r2 > r3); the page-data builder derives 'mentions' only where another section's text names a concept label, and the new section links of chapters 10 and 11 are all links stated in the research, none a mention, so the assertion has nothing to remove; the old pages passed only because the test skipped that feature for them (NOREL: no relation between two sections). This is a test-design gap of the same family as the owner's open ruling on the chapter 13 test design. (2) The template 9.51.0 Untangle layout leaves boxes overlapping when many edges connect the section boxes (2 of 24 in chapter 10; the click crash in chapter 11 is an overlapped box). Changing either means a new test version or a new template version, which the written standard excludes; the executors correctly stopped, and no test, template, gate or threshold was changed.")
    for nn in ("10", "11"):
        ok, bad, lines = res[nn]
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT[nn], lit("Control %s (record v%s), page 9.78.0 of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: NOT MET: element(s) %s; by its own text, if any element fails the chapter is named failing and this criterion has no passing result; nothing is waived and the criterion is not edited. %s" % (now[:10], nxt, nn, " | ".join(lines), ", ".join(bad), FACT[nn]))))
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (TCRIT[nn], lit("Control %s (record v%s), the elements of this criterion measured on the NEW page 9.78.0 of chapter %s (the criterion text names page 9.77.0; the Iter_14 criterion repeats its elements for the new page): %s. They are not met on the new page, so this criterion stays NOT MET on element 3 and the story ST_Page_Template stays InProgress; the page 9.77.0 stands as the shipped page." % (now[:10], nxt, nn, " | ".join(l for l in lines if l.startswith("(4)"))))))
    for nn in ("10", "11"):
        tk = TASK[nn]; i, j = T.blk(t, tk); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tk
        why = ("Paused %s UTC, not Done: the executor delivered the page %s and stopped on failing page tests as its brief ordered. The text of this task asks for the page tests run and their result stored, and the Stage 4 page ABox built; the tests fail (see the note of %s) and neither the stored result nor the ABox exists, so the task's own criterion is not met and a unit whose gate fails is named failing and is not Done. It is paused, not cancelled: it resumes (T_Resume) when the owner has decided the change request ex:CR3_PageGates; nothing is waived." % (now, "ch%s/page/sen0401_ch%s_page_v9_78_0.html" % (nn, nn), CRIT[nn]))
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Suspended ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasRationale %s' % (m.group(1), now, lit(why)), 1) + t[j:]
        L.append(C.transition("Susp5T_" + tk, tk, "T_Suspend", now, why, tk + " suspended"))
        L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (tk, ", ".join("ex:" + e for e in ["Ev7C_%s_Ch%s" % (k, nn) for k, _, _ in KINDS]) + ", " + ", ".join("ex:" + ver[f][0] for f in files[nn]),
                 lit("Control %s: NOT Done. Delivered by the executor session %s (commits %s). The checks and their results are those of the evidence nodes and the note of %s; failing checks are recorded evidenceVerified false. %s" % (now[:10], SESS[nn], ", ".join(COMMITS[nn]), CRIT[nn], FACT[nn]))))
    vtxt = "Control %s: this task cannot start, its dependency %s is not Done; it stays Proposed. The control measurement of the criterion is attached to the criteria as evidence." 
    for nn in ("10", "11"):
        L.append('ex:TK_SecLinks_Ch%s_Verify backlog:hasAuditNote %s .\n' % (nn, lit(vtxt % (now[:10], TASK[nn]))))
    L.append('ex:ST_Section_Links backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s): AC3L_Ch10 NOT MET (elements %s); AC3L_Ch11 NOT MET (elements %s). The story is Done only when every criterion is met (G125): it stays InProgress. TK_SecLinks_Ch10_Page and TK_SecLinks_Ch11_Page are Suspended, not Done. Research (links, consolidation) and PageData are Done and unaffected. %s The change request ex:CR3_PageGates is open; no execution task is created until the owner decides." % (now[:10], nxt, ", ".join(res["10"][1]), ", ".join(res["11"][1]), ROOT)))
    Q = "Do you approve building a new page template version and a new page-test version as NEW files (the old ones kept for comparison), so that the section-link pages of chapters 10 and 11 can be rebuilt and measured: the template with an Untangle fix for dense section edges, and the test with the 'mentioned-together relations' assertion applying only to a page that has such relations (yes or no)? If no, the pages 9.77.0 stay, the ERD-label element for chapters 10 and 11 is recorded as unmeasurable and accepted by you."
    L.append('ex:CR3_PageGates a backlog:ChangeRequest ;\n    rdfs:label %s@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Grow ; rdfs:seeAlso ex:CR3_PageErd, ex:ST_Section_Links ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n' % (
        lit("The pages of chapters 10 and 11 with section links fail page test 9.35.0 (a hard-coded assertion) and template 9.51.0 (Untangle overlaps): new test and template versions, or keep the old pages?"),
        lit("Found by the control %s. %s OPTION A (recommended by the coordinator): a new template version (an Untangle fix for dense section edges) and a new page-test version in which the assertion on mentioned-together relations applies only when the page has them, both as new files, with the old test and template kept as comparison; then ch10 and ch11 are rebuilt (new page versions), measured again, and the criteria can be met. OPTION B: keep the pages 9.77.0 of chapters 10 and 11; the section links stay in the research; the ERD-label element is recorded as unmeasurable and accepted by the owner. THE OWNER'S QUESTION: %s" % (now[:10], ROOT, Q))))
    L.append('ex:IA3_PageGates a backlog:ImpactAssessment ;\n    rdfs:label "What the failing page tests cost, measured before any decision"@en ;\n    backlog:analyzesRequest ex:CR3_PageGates ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_PageErd ;\n    backlog:hasImpactStatement %s .\n' % lit(
        "Affected: AC3L_Ch10 and AC3L_Ch11 (NOT MET), AC3T_Ch10 and AC3T_Ch11 (element 3 waiting on the new pages), ST_Section_Links and ST_Page_Template (stay InProgress), Iter_13 and Iter_14 (stay open; their ends are the owner's). Not affected: the research of chapters 10 and 11 (links and consolidation Done), the page data builder, the passing chapters 8, 12 and 14, the Mission outcome, closureCommittedAt and the Achieved status of the third lineage, which this record does not touch. The same test-design gap is likely to meet any other chapter later given section links (chapters 13, 8, 9, 12, 14; the earlier open owner question on extending the section links). Cost of A: one template version, one test version (the test and template are code of the shared tooling, so every later page test uses them; the old ones stay), a rebuild and control of two pages (about the cost of this iteration's page tasks plus a new Verify), and the chapters 8, 12, 14 pages need no change. Cost of B: no page work; ERD-label stays unmeasurable for two chapters with an owner acceptance recorded; the section links in the research are then shown on no page."))
    comment = "Control of Iter_14, pages: the bridge ran every element of AC3L_Ch10 and AC3L_Ch11 on page 9.78.0 (page tests re-measured); both criteria NOT MET, recorded element by element; the Build page tasks are Suspended with a rationale, not Done; the Verify tasks stay Proposed; ST_Section_Links stays InProgress; root cause recorded as facts; change request CR3_PageGates with impact assessment and one owner question; no execution task created. Mission outcome, closureCommittedAt and the Achieved status are untouched."
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment))); print({k: v[0] for k, v in V.items()})


if __name__ == "__main__":
    {"prepare": prepare, "record": record}[sys.argv[1]]()
