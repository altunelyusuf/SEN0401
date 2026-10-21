#!/usr/bin/env python3
"""sen0401_lineage_control_result v1_0_0 - records, in ONE new register version, the result of the control run of Iter_13 (logs in 08-tooling/verify/iter13/chNN, made by sen0401_lineage_verify_page):
the evidence bridge runs every element of every page criterion as an exit-code check (sen0401_lineage_page_check, the Stage 4 runner, the three chapter checks) and verifies the cited files by SHA-256;
each Build and Verify task goes Done (T_Complete) with that evidence and a harness; the result of each criterion is written element by element as printed, a criterion with an element not met is named NOT MET and nothing is waived;
a story is Done only when every criterion of it is met (G125); the readings of the objectives; and, where an element could not be measured, the change request with its impact assessment and the owner's question.
Usage: sen0401_lineage_control_result_v1_0_0.py [prepare|record]   prepare = run the bridge and keep its output in /tmp/claude-0/s/ctl (long); record = write the version from it."""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
H = C.H; REPO = M.REPO; WORK = "/tmp/claude-0/s/ctl"; BRIDGE = C.BRIDGE
lit = C.lit; transition = C.transition
CHAPS = ["08", "10", "11", "12", "14"]
CHK = "08-tooling/sen0401_lineage_page_check_v1_0_0.py"; CC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"; S4 = "08-tooling/sen0401_stage4_gates_v1_1_0.py"
KINDS = [("markers", CHK, "markers:%s"), ("deck", CHK, "deck:%s"), ("link", CHK, "link:%s"), ("erd", CHK, "erd:%s"), ("test34", CHK, "test34:%s"), ("test35", CHK, "test35:%s"),
         ("counts34", CHK, "counts34:%s"), ("counts35", CHK, "counts35:%s"), ("stage4", S4, "%s"), ("research", CC, "Research/Ch%s"), ("deckchk", CC, "Deck/Ch%s"), ("pagechk", CC, "Page/Ch%s")]
LABEL = {"markers": "template markers in the page HTML", "deck": "deck match: 0 not carried", "link": "link check: 0 not carried", "erd": "page test 9.35.0: labels shown after Untangle", "test34": "page test 9.34.0: no failure",
         "test35": "page test 9.35.0: no failure", "counts34": "page test 9.34.0 counts against the stored result", "counts35": "page test 9.35.0 counts against the stored result", "stage4": "Stage 4 gate runner v1_1_0",
         "research": "chapter check Research", "deckchk": "chapter check Deck", "pagechk": "chapter check Page"}
ELEM = [("(1) template", ["markers"]), ("(2) content", ["deck"]), ("(3) ERD labels", ["erd"]), ("(4) tests", ["test34", "test35", "counts34", "counts35"]), ("(5) Stage 4 and chapter checks", ["stage4", "research", "deckchk", "pagechk"])]
CRIT = {"08": "AC3T_Ch08", "10": "AC3T_Ch10", "11": "AC3T_Ch11", "12": "AC3T_Ch12", "14": "AC3T_Ch14"}
EX_KINDS = ["test34", "stage4", "research", "deckchk", "pagechk"]
FILES = {k: v[4] for k, v in C.BUILD.items()}


def prepare():
    os.makedirs(WORK, exist_ok=True)
    for nn in CHAPS:
        draft = ["@prefix backlog: <http://example.org/backlog#> .\n@prefix ex: <http://example.org/sen0401-slides-lineage#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"]
        for kind, spec, tid in KINDS:
            draft.append('ex:Ev3C_%s_Ch%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" .\n' % (kind, nn, lit("%s, chapter %s, page 9.77.0" % (LABEL[kind], nn)), tid % nn, spec))
        d = os.path.join(WORK, "draft_%s.ttl" % nn); open(d, "w").write("".join(draft))
        ld = os.path.join(REPO, "08-tooling", "verify", "iter13", "ch" + nn); os.makedirs(ld, exist_ok=True)
        cmd = "python3 -B {spec} {id} > %s/bridge_$(echo {id} | tr '/:' '__').log 2>&1" % ld
        r = subprocess.run([sys.executable, BRIDGE, d, "--workspace", REPO, "--test-command", cmd, "-o", os.path.join(WORK, "bridge_%s.ttl" % nn)], capture_output=True, text=True, env=dict(os.environ, TZ="UTC"))
        open(os.path.join(WORK, "bridge_%s.out" % nn), "w").write(r.stdout + r.stderr); print(nn, r.stdout[-200:])


def main_record():
    now = M.now(); src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []
    V = {}; OUT = {}
    for nn in CHAPS:
        v = S.verdicts(os.path.join(WORK, "bridge_%s.ttl" % nn))
        for rr in sorted(glob.glob(os.path.join(WORK, "bridge_%s_rerun*.ttl" % nn))):
            v.update(S.verdicts(rr))   # a check run again after a main-thread budget failure: the later run counts, the earlier log stays cited
        for kind, spec, tid in KINDS:
            eid = "Ev3C_%s_Ch%s" % (kind, nn); V[(kind, nn)] = v[eid]
            lg = os.path.join(REPO, "08-tooling", "verify", "iter13", "ch" + nn, "bridge_%s.log" % (tid % nn).replace("/", "_").replace(":", "_"))
            for suf in ("_run2", "_run3"):
                alt = lg.replace("bridge_Page_Ch", "bridge_Page_Ch").replace("bridge_Page_Ch%s.log" % nn, "bridge_Page_Ch%s%s.log" % (nn, suf)) if kind == "pagechk" else lg
                if os.path.exists(alt) and alt != lg: lg = alt
            OUT[(kind, nn)] = (open(lg, encoding="utf-8", errors="replace").read().strip().splitlines() or [""])[-1][:300] if os.path.exists(lg) else ""
    # file evidence: delivered files and the logs of the control run
    logs = {nn: sorted(os.path.relpath(p, REPO) for p in glob.glob(os.path.join(REPO, "08-tooling", "verify", "iter13", "ch" + nn, "*"))) for nn in CHAPS}
    allf = sorted({f for v in FILES.values() for f in v} | {f for nn in CHAPS for f in logs[nn]})
    ver = C.bridge_files(allf, now)
    assert all(x[1][0] for x in ver.values()), "a file is not verified"
    # nodes of the test evidence
    for nn in CHAPS:
        for kind, spec, tid in KINDS:
            ok, at, how = V[(kind, nn)]; eid = "Ev3C_%s_Ch%s" % (kind, nn)
            crits = [CRIT[nn]] + (["AC3T_Ch08_Examples"] if nn == "08" and kind in EX_KINDS else [])
            L.append('ex:%s a backlog:TestEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ;\n    backlog:hasTestId "%s" ; backlog:hasTestSpec "%s" ;\n    backlog:evidenceVerified %s ; backlog:hasVerificationMethod %s ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
                eid, lit("%s, chapter %s, page 9.77.0" % (LABEL[kind], nn)), ", ".join("ex:" + c for c in crits), tid % nn, spec, "true" if ok else "false", lit(how[:600]), at))
    for f, (eid, (ok, at, how)) in ver.items():
        nns = [nn for nn in CHAPS if ("ch%s" % nn) in f or ("ch%s-" % nn) in f or f in logs[nn]]
        crits = sorted({CRIT[nn] for nn in nns} | ({"AC3T_Ch08_Examples"} if "ch08" in f else set()))
        L.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label %s@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:attestsCriterion %s ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "artifact exists and hash matches" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ; backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (
            eid, lit(os.path.basename(f)), ", ".join("ex:" + c for c in crits) or "ex:AC3T_Ch08", f, C.sha(f), at))
    # element-by-element result of each criterion
    res = {}
    notmet = {}
    for nn in CHAPS:
        lines = []; bad = []
        for name, kinds in ELEM:
            okk = all(V[(k, nn)][0] for k in kinds)
            if not okk: bad.append(name)
            lines.append("%s: %s [%s]" % (name, "MET" if okk else "NOT MET", "; ".join("%s: %s -> %s" % (LABEL[k], "verified" if V[(k, nn)][0] else "NOT verified", OUT[(k, nn)][:230]) for k in kinds)))
        res[nn] = (not bad, bad, lines)
    FL = {}
    for nn in CHAPS:
        for fl in sorted(glob.glob(os.path.join(REPO, "08-tooling", "verify", "iter13", "ch" + nn, "*_run1_*fail*.log"))):
            bad = [l.strip()[:230] for l in open(fl, encoding="utf-8", errors="replace") if l.strip().startswith("[FAIL]")][:1]
            FL.setdefault(nn, []).append("%s failed on its first run (%s); it was run again, as the control plan allows up to three runs, and the later run counts; the failing log stays cited as evidence" % (os.path.basename(fl), bad[0] if bad else "see the log"))
    exok = all(V[(k, "08")][0] for k in EX_KINDS)
    ex_line = "; ".join("%s: %s" % (LABEL[k], "verified" if V[(k, "08")][0] else "NOT verified") for k in EX_KINDS)
    for nn in CHAPS:
        ok, bad, lines = res[nn]
        L.append('ex:%s backlog:hasAuditNote %s .\n' % (CRIT[nn], lit("Control %s (record v%s), page 9.77.0 of chapter %s, every element run by the evidence bridge and recorded as printed: %s. RESULT: %s. (Link check, reported beside the criterion: %s.)" % (
            now[:10], nxt, nn, " | ".join(lines), ("MET: all five elements are met" + ("; RE-RUN DISCLOSED: " + " | ".join(FL[nn]) if nn in FL else "")) if ok else "NOT MET: element(s) %s; by its own text, if any element fails the page is named failing and this criterion has no passing result; nothing is waived and the criterion is not edited" % ", ".join(bad), "verified" if V[("link", nn)][0] else "NOT verified"))))
    L.append('ex:AC3T_Ch08_Examples backlog:hasAuditNote %s .\n' % lit("Control %s (record v%s), chapter 8 research v1.2.0 and page 9.77.0: %s. RESULT: %s." % (now[:10], nxt, ex_line, "MET" if exok else "NOT MET")))
    # tasks: Build and Verify Done
    def ev_of(task, nn, ex=False):
        kinds = EX_KINDS if ex else [k for k, _, _ in KINDS]
        return ["Ev3C_%s_Ch%s" % (k, nn) for k in kinds]
    tasks = {"TK_Ch08Ex_Build": ("08", True, "AC3T_Ch08_Examples"), "TK_Ch08Ex_Verify": ("08", True, "AC3T_Ch08_Examples"), "TK_PageTpl_Ch08_Build": ("08", False, "AC3T_Ch08"), "TK_PageTpl_Ch08_Verify": ("08", False, "AC3T_Ch08")}
    for nn in CHAPS[1:]:
        tasks["TK_PageTpl_Ch%s_Build" % nn] = (nn, False, CRIT[nn]); tasks["TK_PageTpl_Ch%s_Verify" % nn] = (nn, False, CRIT[nn])
    starts = {}
    for tk, (nn, ex, crit) in tasks.items():
        i, j = T.blk(t, tk); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, tk
        is_build = tk.endswith("_Build")
        fin = C.BUILD[tk][2] if is_build else now
        new = 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, now)
        t = t[:i] + b.replace(m.group(0), new, 1) + t[j:]; starts[tk] = fin
        evs = ev_of(tk, nn, ex) + ([ver[f][0] for f in FILES[tk]] if is_build else [ver[f][0] for f in logs[nn]])
        L.append(transition("Done3T_" + tk, tk, "T_Complete", fin, ("Done on the executor's last commit(s) %s (%s UTC), recorded in v%s on %s by the builder session once the control run gave it bridge-verified evidence." % (C.BUILD[tk][3], fin, nxt, now)) if is_build else
                            ("Control run finished %s UTC; every check of the criterion ran and is recorded as printed in the note of %s; the task is Done as a verification, whatever the result for the criterion." % (now, crit)), tk + " completed"))
        L.append('ex:Harness3C_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (tk, lit("Checks run for " + tk), tk, ", ".join("ex:" + e for e in ev_of(tk, nn, ex))))
        L.append('ex:%s backlog:hasAcceptanceCriterion ex:%s ; backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (tk, crit, ", ".join("ex:" + e for e in evs),
                 lit(("Done, recorded %s: delivered by the executor session (commits %s)." % (now[:10], C.BUILD[tk][3]) if is_build else "Done, recorded %s: the control run of %s, serial on a quiet machine; logs in 08-tooling/verify/iter13/ch%s; page tests re-run up to three times when only the main-thread budget failed, every run kept." % (now[:10], crit, nn)) + " The checks and their results are those of the evidence nodes of the criterion; whether the criterion is met is in the note of the criterion.")))
    # story ST_Ch08_Examples
    if exok:
        i, j = T.blk(t, "ST_Ch08_Examples"); b = t[i:j]
        m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
        t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), now, now), 1) + t[j:]
        L.append(transition("Done3T_ST_Ch08_Examples", "ST_Ch08_Examples", "T_Complete", now, "Done when its one criterion AC3T_Ch08_Examples is met and both its tasks are Done (G125).", "ST_Ch08_Examples completed"))
        L.append('ex:Harness3C_ST_Ch08_Examples a backlog:TestHarness ; rdfs:label "Checks run for ST_Ch08_Examples"@en ; backlog:harnessFor ex:ST_Ch08_Examples ; backlog:hasHarnessEvidence %s .\nex:ST_Ch08_Examples backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (
            ", ".join("ex:" + e for e in ev_of("", "08", True)), ", ".join("ex:" + e for e in ev_of("", "08", True)), lit("Done, recorded %s, G125: its only criterion AC3T_Ch08_Examples is met (%s) and both tasks are Done." % (now[:10], ex_line))))
        L.append('ex:Obs41_Obj3_Ch08Page34 a backlog:MetricObservation ; rdfs:label "Reading after the chapter 8 examples were verified"@en ;\n    backlog:observesMetric ex:Met3_Ch08Page34 ; backlog:observationFor ex:Obj3_Ch08Page34 ; backlog:hasObservedValue "0"^^xsd:decimal ; backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (now, lit("Measured %s: failing checks of page test 9.34.0 on page 9.77.0 of chapter 8, final run of the control: 0 (evidence node Ev3C_test34_Ch08; logs in 08-tooling/verify/iter13/ch08)." % now[:10])))
    # story ST_Page_Template stays open unless all five criteria are met
    allok = all(res[nn][0] for nn in CHAPS)
    pages = {}
    for nn in ["%02d" % k for k in range(1, 15)]:
        fs = sorted(glob.glob(os.path.join(REPO, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v*.html" % nn)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)\.html", p)[-1]])
        h = open(fs[-1], encoding="utf-8").read(); pages[nn] = ("const LBLRE=LBL.map" in h and "function edVars()" in h)
    n_t = sum(pages.values())
    L.append('ex:Obs41_Obj3_PagesOnTemplate a backlog:MetricObservation ; rdfs:label "Reading after the control run of the page criteria"@en ;\n    backlog:observesMetric ex:Met3_PagesOnTemplate ; backlog:observationFor ex:Obj3_PagesOnTemplate ; backlog:hasObservedValue "%d"^^xsd:decimal ; backlog:observedAt "%s"^^xsd:dateTime ;\n    backlog:hasObservationMethod %s .\n' % (n_t, now, lit("Measured %s: the newest page of each of the 14 chapters contains both template markers: %d of 14 (%s). This objective counts the code of the template only; it does not say that every page meets every element of the written standard (see the notes of the criteria)." % (now[:10], n_t, ", ".join(k for k, v in pages.items() if not v) or "all"))))
    L.append('ex:ST_Page_Template backlog:hasAuditNote %s .\n' % lit("Control %s: criteria met: %s; not met: %s. The story is Done only when every criterion of it is met (G125), so it stays InProgress; the criteria are not edited and nothing is waived." % (now[:10], ", ".join(CRIT[nn] for nn in CHAPS if res[nn][0]) or "none", ", ".join("%s (elements %s)" % (CRIT[nn], ", ".join(res[nn][1])) for nn in CHAPS if not res[nn][0]) or "none")))
    # change route for an element that cannot be measured
    erd_bad = [nn for nn in CHAPS if not V[("erd", nn)][0]]
    if erd_bad:
        sk = {nn: json.load(open(os.path.join(REPO, "08-tooling", "verify", "iter13", "ch" + nn, "summary.json")))["page_test_9_35_0"][-1].get("skips", []) for nn in erd_bad}
        L.append('ex:CR3_PageErd a backlog:ChangeRequest ;\n    rdfs:label %s@en ;\n    backlog:requestsChangeTo ex:Scope3 ; backlog:hasChangeDirection backlog:Direction_Shrink ; rdfs:seeAlso ex:CR3_Pages ;\n    backlog:hasChangeRequestRationale %s ;\n    backlog:hasDisposition backlog:Disp_Pending .\n' % (
            lit("Element 3 (ERD labels after Untangle) of the page criteria of chapters %s cannot be measured: what measures it where the research states no relationship?" % ", ".join(erd_bad)),
            lit("Found by the control run %s. The page test 9.35.0 skips its feature on the labels shown after Untangle on the pages of chapters %s, because the chapter research states no relationship between two sections, so there is nothing to label (skip lines as printed: %s). The skips equal the stored result of the pages as they stood (2 skipped each), so nothing got worse; but element 3 of their criteria asks that feature to report pass, and a skipped feature is not a pass. The criteria are therefore NOT MET on element 3 and are not edited or waived. THE OWNER'S QUESTION: for a page whose chapter states no relationship between two sections, what measures that the relationship labels are readable: (a) element 3 does not apply to such a page (the criterion for chapters %s then says so, a Shrink of the written standard), or (b) the chapter research states at least one relationship between two sections so the existing feature can run (a change of the research, which the standard excluded), or (c) another measure he names?" % (now[:10], ", ".join(erd_bad), json.dumps(sk, ensure_ascii=False)[:900], ", ".join(erd_bad)))))
        L.append('ex:IA3_PageErd a backlog:ImpactAssessment ;\n    rdfs:label "What the unmeasurable element 3 costs, measured before any decision"@en ;\n    backlog:analyzesRequest ex:CR3_PageErd ; backlog:identifiesAffectedLineage ex:Lineage3 ; rdfs:seeAlso ex:IA3_Pages ;\n    backlog:hasImpactStatement %s .\n' % lit("Affected: criteria %s and, through them, ST_Page_Template (stays InProgress until the owner decides and the criteria are met or changed by a recorded route). Not affected: the pages themselves (every other element is recorded), the Mission outcome, closureCommittedAt and the Achieved status of the third lineage, which this record does not touch. Cost of (a): one criterion revision by the change route, no page work. Cost of (b): a new research version per chapter, new pages and checks, the pages rebuilt (about the cost of this iteration for two chapters). Cost of (c): depends on the measure." % ", ".join(CRIT[nn] for nn in erd_bad)))
    comment = "Control of Iter_13, result: the bridge ran every element of the five page criteria and the chapter 8 examples criterion; Build and Verify tasks Done with verified evidence; criteria results element by element; criteria met: %s; not met: %s; the change request for the unmeasurable element 3 is opened where needed. Mission outcome, closureCommittedAt and the Achieved status are untouched." % (", ".join(CRIT[nn] for nn in CHAPS if res[nn][0]) or "none", ", ".join(CRIT[nn] for nn in CHAPS if not res[nn][0]) or "none")
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, comment)))
    print({nn: (res[nn][0], res[nn][1]) for nn in CHAPS}, "ex ok", exok)


if __name__ == "__main__":
    {"prepare": prepare, "record": main_record}[sys.argv[1]]()
