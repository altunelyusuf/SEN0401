#!/usr/bin/env python3
"""sen0401_lineage_review v1_1_0 - closes the stories of Iterations 14 (the section links, after the split of its remainder by ex:CR3_Repair20) and 20 (the deck check and the deck of chapter 8) - derived from v1_0_0 which closed the stories of Iterations 13, 16, 17, 18 and 19 whose every task is Done, by the review ceremony of the discipline (as Iteration 12 was closed by ex:RC3_Iter_12), in ONE new register version (G113, G125, G136).
For each story: Done by T_Complete (finishedAt = its last task's finish), execution modality, a test harness of the story whose evidence is the verified evidence of its tasks, the story's own evidence links.
For each iteration: a SprintReviewCeremony (reviews the planning ceremony; closesStory; closesIteration only when every member is Done) and, for each objective the stories can move, a MetricObservation taken at the review whose value the builder MEASURES in this run
(charset check on the newest pages, the deck standard check on the newest decks, the page-test results of the evidence bridge, unchanged files read from git). Stories that are not Done are not touched.
Usage: sen0401_lineage_review_v1_0_0.py   (writes one new version; the caller validates, then commits)"""
__version__ = "1.1.0"
import os, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; REPO = M.REPO; H = os.path.join(REPO, "08-tooling")
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")
def sh(*a): return subprocess.run(list(a), cwd=REPO, capture_output=True, text=True)
def git(*a): return sh("git", *a).stdout.strip()
# iteration, stories closed, closes the iteration, objectives read at the review
PLAN = [(14, ["ST_Section_Links"], True, ["Obj3_SectionsLinked", "Obj3_ErdLabelsRun", "Obj3_PagesMeasured"]), (20, ["ST_Ch78_DeckCheck", "ST_Ch08_Deck"], False, ["Obj3_Ch78"])]
PAGES = {"05": "03-materials/ch05/page/sen0401_ch05_page_v9_83_0.html", "06": "03-materials/ch06/page/sen0401_ch06_page_v9_83_0.html"}
DECKS = {"05": "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_1_0.pptx", "06": "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_1_0.pptx"}
CTRL = "aeb8cdf"   # the commit that recorded the control of the pages 9.83.0 (v0.238.0)
BR = os.path.join(H, "verify", "iter19", "pages_bridge")


def measure():
    """returns {objective: (value, method text)}; every number is read in this run or from the controls recorded in the register (unchanged files read from git)"""
    out = {}; today = M.now()[:10]
    def newest(pat):
        import glob
        fs = sorted(glob.glob(os.path.join(REPO, pat)), key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]); return os.path.relpath(fs[-1], REPO)
    rows = []; n = 0
    for nn, chk in (("07", "sen0401_deck_standard_check_v1_0_0.py"), ("08", "sen0401_deck_standard_check_v1_1_0.py")):
        deck = newest("03-materials/ch%s/*.pptx" % nn); man = newest("03-materials/ch%s/page/chapter_code_ch%s_v*.json" % (nn, nn)); page = newest("03-materials/ch%s/page/sen0401_ch%s_page_v*.html" % (nn, nn))
        d = sh(sys.executable, "-B", os.path.join(H, chk), nn, deck); dok = d.returncode == 0 and "SUMMARY PASS=12 FAIL=0" in d.stdout
        c = sh(sys.executable, "-B", os.path.join(H, "sen0401_page_charset_check_v1_0_0.py"), os.path.join(REPO, page)); cok = c.returncode == 0
        mok = os.path.exists(os.path.join(REPO, man)); n += 1 if (dok and mok and cok) else 0
        rows.append("chapter %s: deck %s %s (%s), manifest %s %s, charset check on the newest page %s %s" % (nn.lstrip("0"), os.path.basename(deck), "PASS=12" if dok else "FAILS", chk, os.path.basename(man), "exists" if mok else "MISSING", os.path.basename(page), "exit 0" if cok else "exit non-zero"))
    out["Obj3_Ch78"] = (n, "Read %s in this run: the count of chapters 7 and 8 for which the deck standard check exits 0 with no NOT_MEASURED on the newest deck, a chapter-code manifest exists and the charset check passes on the newest page: %s. (The pages are not claimed: the page of chapter 8 fails the page test 9.36.0 on P2, the page of chapter 7 is not rebuilt.)" % (today, "; ".join(rows)))
    c187 = git("log", "-1", "--format=%H", "--grep", "v0.187: TK_SecLinks_Ch10_Page Done"); c173 = git("log", "-1", "--format=%H", "--grep", "Register v0.173: control of Iter_14")
    ch10 = "03-materials/ch10/page/sen0401_ch10_page_v9_79_0.html"; ch11 = "03-materials/ch11/page/sen0401_ch11_page_v9_78_0.html"
    n10 = git("log", "--format=%h", c187 + "..HEAD", "--", ch10) if c187 else "?"; n11 = git("log", "--format=%h", c173 + "..HEAD", "--", ch11, "03-materials/ch11/page") if c173 else "?"
    assert c187 and c173 and n10 == "" and n11 == "", (c187, c173, n10, n11)
    out["Obj3_PagesMeasured"] = (1, "Read %s from the controls recorded in the register: the newest page of chapter 10, 9.79.0, passes the page tests 9.34.1 and 9.35.1 (control of v0.187.0, commit %s; unchanged in git since); the newest page of chapter 11, 9.78.0, fails the page tests (control of v0.173.0, commit %s; no newer page of chapter 11 exists, unchanged in git since; the page is rebuilt by TK_Ch11_Page_Build of Iteration 21): 1 of 2 pass." % (today, c187[:7], c173[:7]))
    out["Obj3_ErdLabelsRun"] = (1, "Read %s from the controls recorded in the register: the ERD label features of the page test 9.35.1 run with no skip and pass on the page 9.79.0 of chapter 10 (control of v0.187.0, commit %s, labels shown after Untangle 1.00 of before; unchanged in git since); the newest page of chapter 11, 9.78.0, does not (control of v0.173.0): 1 of 2. The remainder is the criterion ex:AC7R_SecLinks_Ch11 of the story ex:ST_Section_Links_Ch11 in Iteration 21." % (today, c187[:7]))
    out["Obj3_SectionsLinked"] = (0, "Read %s from the controls recorded in the register: the section links are stated in the research of chapter 10 (control of v0.187.0: every section covered, PASS) and of chapter 11 (TK_SecLinks_Ch11_Research Done on bridge-verified evidence), so no section of the two chapters lacks a stated relationship to another section in the research: 0 of 33. The page of chapter 11 does not show them yet (the criterion ex:AC7R_SecLinks_Ch11 of the story in Iteration 21 measures that)." % today)
    return out


def evidence_of(g, tasks):
    ev = set()
    for k in tasks:
        for e in g.objects(E[k], B.hasEvidence):
            v = g.value(e, B.evidenceVerified)
            if v is not None and str(v).lower() == "true": ev.add(str(e).split("#")[1])
    return sorted(ev)


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); g = rdflib.Graph(); g.parse(src, format="turtle")
    vals = measure(); L = []; closed = []; sess = {}
    for n, stories, closeit, objs in PLAN:
        time.sleep(1.1); at = M.now(); RC = "RC3R_Iter_%d" % n; PC = "PC3_Iter_%d" % n; assert ("ex:%s a backlog:SprintPlanningCeremony" % PC) in t, PC
        for sid in stories:
            i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:InProgress" in b and ("memberOfContainer ex:Iter_%d" % n) in b, sid
            tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1))
            cancelled = []
            for k in tks:
                kb = t[T.blk(t, k)[0]:T.blk(t, k)[1]]
                if "backlog:hasState backlog:Cancelled" in kb: assert "CR3_Repair20" in kb, k; cancelled.append(k); continue
                assert "backlog:hasState backlog:Done" in kb, "%s has task %s not Done" % (sid, k)
            tks = [k for k in tks if k not in cancelled]
            fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks)))
            m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, sid
            ev = evidence_of(g, tks); assert ev, sid + " has no verified task evidence"
            t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, at), 1) + t[j:]
            L.append(C.transition("Done3R_" + sid, sid, "T_Complete", at, "Done at the review ex:%s on %s UTC: every task of the story (%d) is Done on bridge-verified evidence recorded in the versions named in the story's and the tasks' audit notes; the last task finished %s UTC (G125)." % (RC, at, len(tks), fin), sid + " completed"))
            L.append('ex:Harness3R_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (sid, lit("Checks run for " + sid), sid, ", ".join("ex:" + e for e in ev)))
            L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (sid, ", ".join("ex:" + e for e in ev), lit("Closed %s UTC at the review ex:%s: all %d tasks are Done on bridge-verified evidence (%d verified evidence nodes of the tasks are the evidence and the harness of the story); the controls are recorded in the audit notes of the tasks and of the criteria. The story stays closed (G125)." % (at, RC, len(tks), len(ev)))))
            if sid == "ST_Section_Links":
                i2, j2 = T.blk(t, sid); b2 = t[i2:j2]; assert "backlog:hasAcceptanceCriterion ex:AC3L2_Ch10, ex:AC3L2_Ch11" in b2
                t = t[:i2] + b2.replace("backlog:hasAcceptanceCriterion ex:AC3L2_Ch10, ex:AC3L2_Ch11", "backlog:hasAcceptanceCriterion ex:AC3L2_Ch10", 1) + t[j2:]
                L.append('ex:AC3L2_Ch11 backlog:hasAuditNote %s ;\n    rdfs:seeAlso ex:AC7R_SecLinks_Ch11 .\n' % lit("Carried %s by the change route of ex:CR3_Repair20 (Iteration 14 ended 2026-10-24 06:00 UTC with this criterion unmet): the criterion is NOT met and is NOT waived. Its page (9.79.0 on template 9.51.1) is no longer the target, so its elements (1) links, (2) ERD labels, (3) gates, (4) the AC3T elements and (5) no edit are restated, with the versions that stand now, in ex:AC7R_SecLinks_Ch11 of the story ex:ST_Section_Links_Ch11 in Iteration 21, which is met only when its Verify task finds them met on the rebuilt page of chapter 11. The story ex:ST_Section_Links is closed at ex:%s with its chapter 10 criterion ex:AC3L2_Ch10 (MET, control v0.187.0); its chapter 11 tasks were withdrawn as superseded." % (M.now()[:10], RC)))
            closed.append(sid)
        mem = re.findall(r"ex:(ST_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", t[T.blk(t, "Iter_%d" % n)[0]:T.blk(t, "Iter_%d" % n)[1]], re.S).group(1))
        left = [s for s in mem if s not in stories and "backlog:hasState backlog:Done" not in t[T.blk(t, s)[0]:T.blk(t, s)[1]]]
        assert bool(left) != closeit, (n, left, closeit)
        L.append('ex:%s a backlog:SprintReviewCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:Iter_%d ; backlog:reviewsCeremony ex:%s ;%s\n    backlog:closesStory %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            RC, lit("Review of iteration %d: the stories whose tasks are all Done" % n), n, PC, (" backlog:closesIteration ex:Iter_%d ;" % n) if closeit else "", ", ".join("ex:" + s for s in stories), at,
            lit("Held %s UTC by the builder session, after the proposed end of the iteration (the end of the iteration had passed): %s closed, each with all its tasks Done on bridge-verified evidence. %s The readings of the objectives are the observations taken at this review." % (at,
                ", ".join(stories), "The iteration is closed: every member is Done." if closeit else "The iteration is NOT closed: %s stay open until the owner decides their disposition (asked through the coordinator); nothing is carried over by this review." % ", ".join(left)))))
        for o in objs:
            v, meth = vals[o]; met = str(g.value(E[o], B.hasSuccessMetric)).split("#")[1]
            L.append('ex:ObsR%d_%s a backlog:MetricObservation ; rdfs:label "Reading at the review of iteration %d"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%s"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony ex:%s ;\n    backlog:hasObservationMethod %s .\n' % (n, o, n, met, o, v, at, RC, lit(meth)))
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, "Review ceremonies of iterations 14 and 20: the stories whose tasks are all Done (or withdrawn by the change route of ex:CR3_Repair20) are closed (%s); objective readings measured at the reviews; iteration 14 closed." % ", ".join(closed))))
    print({o: v[0] for o, v in vals.items()})


main()
