#!/usr/bin/env python3
"""sen0401_lineage_review v1_0_0 - closes the stories of Iterations 13, 16, 17, 18 and 19 whose every task is Done, by the review ceremony of the discipline (as Iteration 12 was closed by ex:RC3_Iter_12), in ONE new register version (G113, G125, G136).
For each story: Done by T_Complete (finishedAt = its last task's finish), execution modality, a test harness of the story whose evidence is the verified evidence of its tasks, the story's own evidence links.
For each iteration: a SprintReviewCeremony (reviews the planning ceremony; closesStory; closesIteration only when every member is Done) and, for each objective the stories can move, a MetricObservation taken at the review whose value the builder MEASURES in this run
(charset check on the newest pages, the deck standard check on the newest decks, the page-test results of the evidence bridge, unchanged files read from git). Stories that are not Done are not touched.
Usage: sen0401_lineage_review_v1_0_0.py   (writes one new version; the caller validates, then commits)"""
__version__ = "1.0.0"
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
PLAN = [(13, ["ST_Page_Template"], True, []), (16, ["ST_Page_Gates"], True, ["Obj3_PagesMeasured"]),
        (17, ["ST_Remedy_Deck_Ch05", "ST_Remedy_Deck_Ch06", "ST_Remedy_Page_Ch06"], False, ["Obj3_Remedy56Decks", "Obj3_Remedy56Pages"]),
        (18, ["ST_Repair_Template", "ST_Repair_Page_Ch06"], False, ["Obj3_ChipScroll"]),
        (19, ["ST_Charset_Template", "ST_Charset_Check", "ST_Charset_Page_Ch05", "ST_Charset_Page_Ch06"], True, ["Obj3_Charset"])]
PAGES = {"05": "03-materials/ch05/page/sen0401_ch05_page_v9_83_0.html", "06": "03-materials/ch06/page/sen0401_ch06_page_v9_83_0.html"}
DECKS = {"05": "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_1_0.pptx", "06": "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_1_0.pptx"}
CTRL = "aeb8cdf"   # the commit that recorded the control of the pages 9.83.0 (v0.238.0)
BR = os.path.join(H, "verify", "iter19", "pages_bridge")


def measure():
    """returns {objective: (value, method text)}; every number is read in this run"""
    out = {}
    cs = {n: sh(sys.executable, "-B", os.path.join(H, "sen0401_page_charset_check_v1_0_0.py"), os.path.join(REPO, p)) for n, p in PAGES.items()}
    ok_cs = {n: r.returncode == 0 for n, r in cs.items()}
    tests = {}
    for n in PAGES:
        for tv in ("9_34_1", "9_35_1", "9_36_0"):
            f = [x for x in os.listdir(BR) if re.search(r"page_check_v1_5_0_py_test_%s_9_83_0_%s\.log$" % (n, tv), x) and not x.startswith("run")]
            assert len(f) == 1, (n, tv, f)
            last = open(os.path.join(BR, f[0]), encoding="utf-8").read().strip().splitlines()[-1]
            tests[(n, tv)] = ("failed 0" in last and "exit 0" in last, last[:120])
    unchanged = {n: git("log", "--format=%h", CTRL + "..HEAD", "--", PAGES[n]) == "" for n in PAGES}
    decks = {}
    for n in DECKS:
        r = sh(sys.executable, "-B", os.path.join(H, "sen0401_deck_standard_check_v1_0_0.py"), n, DECKS[n]); decks[n] = (r.returncode == 0 and "SUMMARY PASS=12 FAIL=0" in r.stdout, [l for l in r.stdout.splitlines() if l.startswith("SUMMARY")][:1])
    tprint = "; ".join("page %s: %s" % (n, ", ".join("%s %s" % (tv.replace("_", "."), "no failure" if tests[(n, tv)][0] else "FAILS") for tv in ("9_34_1", "9_35_1", "9_36_0"))) for n in PAGES)
    pages_pass = {n: all(tests[(n, tv)][0] for tv in ("9_34_1", "9_35_1", "9_36_0")) and unchanged[n] for n in PAGES}
    nstr = lambda d: sum(1 for v in d.values() if (v if isinstance(v, bool) else v[0]))
    today = M.now()[:10]
    out["Obj3_Charset"] = (sum(1 for n in PAGES if ok_cs[n] and pages_pass[n]), "Read %s in this run: the charset check v1_0_0 exits 0 on the newest pages 9.83.0 of chapters 5 and 6 (%s) and the page tests 9.36.0, 9.35.1 and 9.34.1 report no failure on each (the bridge logs of the control of v0.238.0, %s; the page files are unchanged in git since the commit %s of that control: %s)." % (today, ", ".join("chapter %s %s" % (n, "exit 0" if ok_cs[n] else "exit non-zero") for n in PAGES), tprint, CTRL, ", ".join("chapter %s %s" % (n, "unchanged" if unchanged[n] else "CHANGED") for n in PAGES)))
    out["Obj3_Remedy56Decks"] = (nstr({n: decks[n] for n in DECKS}), "Read %s in this run: the deck standard check v1_0_0 on the newest decks (%s; %s): chapter 5 %s, chapter 6 %s." % (today, ", ".join(DECKS.values()), "run now", decks["05"][1], decks["06"][1]))
    out["Obj3_Remedy56Pages"] = (sum(1 for n in PAGES if pages_pass[n]), "Read %s: the page tests 9.36.0, 9.35.1 and 9.34.1 report no failure on the newest pages 9.83.0 of chapters 5 and 6 (%s; the bridge logs of the control of v0.238.0; the page files are unchanged in git since %s)." % (today, tprint, CTRL))
    out["Obj3_ChipScroll"] = (sum(1 for n in PAGES if pages_pass[n]), "Read %s: the page tests 9.36.0, 9.35.1 and 9.34.1 report no failure on the newest pages 9.83.0 of chapters 5 and 6 (%s; the bridge logs of the control of v0.238.0; the page files are unchanged in git since %s)." % (today, tprint, CTRL))
    # chapters 10 and 11: from the controls recorded in the register, unchanged files read from git
    c187 = git("log", "-1", "--format=%H", "--grep", "v0.187: TK_SecLinks_Ch10_Page Done"); c173 = git("log", "-1", "--format=%H", "--grep", "Register v0.173: control of Iter_14")
    ch10 = "03-materials/ch10/page/sen0401_ch10_page_v9_79_0.html"; ch11 = "03-materials/ch11/page/sen0401_ch11_page_v9_78_0.html"
    n10 = git("log", "--format=%h", c187 + "..HEAD", "--", ch10) if c187 else "?"; n11 = git("log", "--format=%h", c173 + "..HEAD", "--", ch11, "03-materials/ch11/page") if c173 else "?"
    assert c187 and c173 and n10 == "" and n11 == "", (c187, c173, n10, n11)
    out["Obj3_PagesMeasured"] = (1, "Read %s from the controls recorded in the register: the newest page of chapter 10, 9.79.0, passes the page tests 9.34.1 and 9.35.1 (control of v0.187.0, commit %s; the file is unchanged in git since); the newest page of chapter 11, 9.78.0, fails the page tests (stops on a click timeout; control of v0.173.0, commit %s; no newer page of chapter 11 exists and the file is unchanged in git since; its task is Suspended until the owner answers ex:CR3_PageClick): 1 of 2 pass." % (today, c187[:7], c173[:7]))
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
            for k in tks:
                kb = t[T.blk(t, k)[0]:T.blk(t, k)[1]]; assert "backlog:hasState backlog:Done" in kb, "%s has task %s not Done" % (sid, k)
            fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in tks)))
            m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m, sid
            ev = evidence_of(g, tks); assert ev, sid + " has no verified task evidence"
            t = t[:i] + b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, at), 1) + t[j:]
            L.append(C.transition("Done3R_" + sid, sid, "T_Complete", at, "Done at the review ex:%s on %s UTC: every task of the story (%d) is Done on bridge-verified evidence recorded in the versions named in the story's and the tasks' audit notes; the last task finished %s UTC (G125)." % (RC, at, len(tks), fin), sid + " completed"))
            L.append('ex:Harness3R_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (sid, lit("Checks run for " + sid), sid, ", ".join("ex:" + e for e in ev)))
            L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (sid, ", ".join("ex:" + e for e in ev), lit("Closed %s UTC at the review ex:%s: all %d tasks are Done on bridge-verified evidence (%d verified evidence nodes of the tasks are the evidence and the harness of the story); the controls are recorded in the audit notes of the tasks and of the criteria. The story stays closed (G125)." % (at, RC, len(tks), len(ev)))))
            closed.append(sid)
        mem = re.findall(r"ex:(ST_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", t[T.blk(t, "Iter_%d" % n)[0]:T.blk(t, "Iter_%d" % n)[1]], re.S).group(1))
        left = [s for s in mem if s not in stories and "backlog:hasState backlog:Done" not in t[T.blk(t, s)[0]:T.blk(t, s)[1]]]
        assert bool(left) != closeit, (n, left, closeit)
        L.append('ex:%s a backlog:SprintReviewCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:Iter_%d ; backlog:reviewsCeremony ex:%s ;%s\n    backlog:closesStory %s ; backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            RC, lit("Review of iteration %d: the stories whose tasks are all Done" % n), n, PC, (" backlog:closesIteration ex:Iter_%d ;" % n) if closeit else "", ", ".join("ex:" + s for s in stories), at,
            lit("Held %s UTC by the builder session, after the proposed end of the iteration (the iteration ends of 2026-10-23 had passed): %s closed, each with all its tasks Done on bridge-verified evidence. %s The readings of the objectives are the observations taken at this review." % (at,
                ", ".join(stories), "The iteration is closed: every member is Done." if closeit else "The iteration is NOT closed: %s stay open until the owner decides their disposition (asked through the coordinator); nothing is carried over by this review." % ", ".join(left)))))
        for o in objs:
            v, meth = vals[o]; met = str(g.value(E[o], B.hasSuccessMetric)).split("#")[1]
            L.append('ex:ObsR_%s a backlog:MetricObservation ; rdfs:label "Reading at the review of iteration %d"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%s"^^xsd:decimal ;\n    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony ex:%s ;\n    backlog:hasObservationMethod %s .\n' % (o, n, met, o, v, at, RC, lit(meth)))
    t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t2, nxt, cur, "Review ceremonies of iterations 13, 16, 17, 18 and 19: the stories whose tasks are all Done are closed (%s); objective readings measured at the reviews; iterations 13, 16 and 19 closed." % ", ".join(closed))))
    print({o: v[0] for o, v in vals.items()})


main()
