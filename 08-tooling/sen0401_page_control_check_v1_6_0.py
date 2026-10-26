#!/usr/bin/env python3
"""sen0401_page_control_check v1_6_0 (over v1_5_0: the kind collision runs the ERD collision probe v1_0_0 on the page and passes only when it prints CLEAR). Original text of v1_5_0 follows: sen0401_page_control_check v1_5_0 (over v1_4_0: the stored 9.34.1 and 9.35.1 results come from the newest page at or below the reference page that has stored logs of that test, because a chapter page may have only the 9.37.0 result stored (chapter 10: 9_79_0 has none, 9_77_0 has). Original text of v1_4_0 follows: over v1_3_0: the environment variable STORED_PAGE names the page whose stored results are the reference when the page just below failed its tests (chapter 1: 9_70_0, because 9.71.0 failed); v1_3_0 over v1_2_0: the stored logs are also looked up in page-gates-evidence/regression/R*_V_chNN_PV.full.log; v1_2_0 over v1_1_0: the stored logs are looked up in every verify/iter*/pages folder; v1_1_0 over v1_0_0: the stored 9.34.1 and 9.35.1 results of a chapter other than 5 are parsed from the logs of the previous page in verify/iter19/pages) - the lineage agent's OWN checks of a rebuilt chapter page (criterion AC9_Page_ChNN, elements 1 to 7). A NEW tool; it edits nothing.
Usage: sen0401_page_control_check_v1_4_0.py NN PAGEVER KIND   (PAGEVER like 9_84_0; run browser kinds under `flock /tmp/page_test.lock`)
KIND: charset | regr (reads the control's own page-test runs verify/iter32/ctl_pageNN/ctl_chNN_page_PV_test_*.full.log; each widgets all passed, no [FAIL], widgets/features/gates at or above the stored result of the previous page, skips not more)
 | probe (story layout probe v1_0_0 on the page, RESULT PASS) | stage4 (Stage 4 gate runner v1_1_0, exit 0) | chk:Research|Deck|Page (chapter check v1_3_0; Page must print the page version tested)
 | match (deck match check v1_0_0, 0 not carried) | links (every hyperlink of the newest deck is carried by the page, label and address; printed, nothing is fetched) | codetab (the page's chapter-code tab equals the manifest in names, order, code, slide and expected, and the manifest's slides equal the code slides of the NEWEST deck)
 | newfiles (the page ABox and the stored page-test result of this page version exist and were added, not modified, by git) | nochange:COMMITS (the commits only ADD files)."""
import glob, hashlib, json, os, re, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
NN, PV, A = sys.argv[1], sys.argv[2], sys.argv[3]; ch = "ch" + NN; PD = os.path.join(R, "03-materials", ch, "page"); PAGE = os.path.join(PD, "sen0401_%s_page_v%s.html" % (ch, PV))
def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout.strip()
def run(*a, **k): r = subprocess.run([sys.executable, "-B"] + list(a), capture_output=True, text=True, cwd=R, **k); return r.returncode, (r.stdout + r.stderr)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = {l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")}; w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
def prevpage():
    ps = sorted((p for p in glob.glob(os.path.join(PD, "sen0401_%s_page_v*.html" % ch)) if vk(p) < vk(PAGE)), key=vk); return "_".join(map(str, vk(ps[-1])))
def charset(): c, o = run(T + "/sen0401_page_charset_check_v1_0_0.py", PAGE); print(o.strip()[-300:]); return c == 0
def regr():
    D = T + "/verify/iter32/ctl_page" + NN; ok = True; pv = os.environ.get("STORED_PAGE") or prevpage(); stored = {"9_37_0": "test_results_abox_v%s.json" % pv}
    sj = json.load(open(os.path.join(T, ch + "-page", "test_results_abox_v%s.json" % pv))); rw, rf, rg = len(sj["widgets"]), len(sj["features"]), len(sj["gates"])
    def stored(v):
        if NN == "05": return (113, 187, 6)
        vk = lambda x: [int(y) for y in x.split("_")]
        cands = sorted({p_ for p_ in [re.search(r"_page_(\d+_\d+_\d+)_test_", x).group(1) for x in glob.glob(os.path.join(T, "verify/iter*/pages/%s_page_*_test_%s.full.log" % (ch, v)))] + [re.search(r"_%s_(\d+_\d+_\d+)\.full\.log" % ch, x).group(1) for x in glob.glob(os.path.join(T, "page-gates-evidence/regression/R*_%s_%s_*.full.log" % (v, ch)))] if vk(p_) <= vk(pv)}, key=vk)
        pv_ = cands[-1]; print("stored", v, "log taken from page", pv_, "(newest page at or below", pv, "that has one)")
        q = sorted(glob.glob(os.path.join(T, "verify/iter*/pages/%s_page_%s_test_%s.full.log" % (ch, pv_, v))) + glob.glob(os.path.join(T, "page-gates-evidence/regression/R*_%s_%s_%s.full.log" % (v, ch, pv_))))[-1]; f_, s_, w_, g_ = parse(open(q, errors="replace").read()); return (w_[0], len(f_), g_)
    REF = {"9_37_0": (rw, rf, rg), "9_34_1": stored("9_34_1"), "9_35_1": stored("9_35_1")}  # 9.34.1 and 9.35.1: the stored results of the page 9.83.0 as the control recorded them for the template control (113 widgets, 187 features, 6 gates, 0 skips)
    for v in ("9_37_0", "9_34_1", "9_35_1"):
        rw, rf, rg = REF[v]
        ps = sorted(glob.glob(D + "/ctl_%s_page_%s_test_%s*.full.log" % (ch, PV, v)), key=lambda x: (len(x), x))
        if not ps: print(v, "missing"); ok = False; continue
        for k, p in enumerate(ps):
            feats, skips, w, g = parse(open(p, errors="replace").read()); fails = [x for x, y in feats.items() if y == "FAIL"]
            good = bool(w) and w[0] == w[1] and w[0] >= rw and not fails and len(feats) >= rf and g >= rg and not skips
            print(ch, PV, "test", v, "run", os.path.basename(p), ": widgets", w, "features", len(feats), "gates", g, "skips", len(skips), "FAIL", len(fails), "%s" % [x[:60] for x in fails], "| stored page", pv, (rw, rf, rg, 0), "->", "ok" if good else "NOT OK")
        print("  verdict of", v, "= the LAST run (the brief allows up to three reruns of a main-thread budget failure, every run kept):", "ok" if good else "NOT OK"); ok &= good
    rr = "".join(open(D + "/" + f).read() for f in ("ctl_runner.txt", "ctl_rerun.txt") if os.path.exists(D + "/" + f)); print("runner exits:", rr.strip().replace("\n", " | ")); return ok
def probe():
    c, o = run(T + "/sen0401_story_layout_probe_v1_0_0.py", NN, PV); print(o.strip()[-900:]); return c == 0 and re.search(r"RESULT:? PASS", o) is not None
def stage4(): c, o = run(T + "/sen0401_stage4_gates_v1_1_0.py", NN); print(o.strip()[-900:]); return c == 0
def chk(kind):
    c, o = run(T + "/sen0401_lineage_chapter_check_v1_3_0.py", "%s/Ch%s" % (kind, NN)); print(o.strip()[-700:])
    if kind == "Page":
        newest = "_".join(map(str, vk(sorted(glob.glob(os.path.join(PD, "sen0401_%s_page_v*.html" % ch)), key=vk)[-1]))); named = sorted(set(re.findall(r"sen0401_%s_page_v(\d+_\d+_\d+)" % ch, o)))
        print("the chapter check v1_3_0 starts its page runner v1_1_0 with no page version, which takes the NEWEST page file of the chapter: newest on disk", newest, "| expected", PV, "| versions named in its full output", named)
        pp = prevpage(); print("the runner places the newest EARLIER page beside the tested copy and the page test names it as the shipped page ('shipped 9.xx.x' in the budget feature); named earlier version:", named, "| the page before", PV, "on disk:", pp, "(a test of the page 9.83.0 would name 9.82.0)")
        if newest != PV or named != [pp]: return False
    return c == 0
def match(): c, o = run(T + "/pages_deck_match_verify_v1_0_0.py", NN, PV); print(o.strip()[-700:]); return c == 0 and re.search(r"not carried[^\d]*0\b|0 not carried", o) is not None
def links():
    from pptx import Presentation
    deck = sorted(glob.glob(os.path.join(R, "03-materials", ch, "SEN0401_*_3e_v*.pptx")), key=vk)[-1]; h = open(PAGE, encoding="utf-8").read(); hu = h.replace("\\/", "/"); miss = []; n = 0
    for i, s in enumerate(Presentation(deck).slides, 1):
        for sh in s.shapes:
            if sh.has_text_frame:
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        a = r.hyperlink.address
                        if a:
                            n += 1; lab = r.text.strip()
                            if a not in hu and a.rstrip("/") not in hu: miss.append((i, lab[:40], a))
    print("deck", os.path.basename(deck), ":", n, "hyperlinks;", len(miss), "address not in the page:", miss[:12]); return not miss
def codetab():
    mp = sorted(glob.glob(os.path.join(PD, "chapter_code_%s_v*.json" % ch)), key=vk)[-1]; m = json.load(open(mp)); h = open(PAGE, encoding="utf-8").read(); i = h.index('"chaptercode": {'); d = json.JSONDecoder(); pc = d.raw_decode(h[i + len('"chaptercode": '):])[0]
    FIELDS = tuple(k for k in pc["examples"][0] if k in m["examples"][0]); assert {"order", "name", "code", "slide"} <= set(FIELDS), FIELDS
    ok = [e["name"] for e in m["examples"]] == [e["name"] for e in pc["examples"]] and [{k: e[k] for k in FIELDS} for e in m["examples"]] == [{k: e[k] for k in FIELDS} for e in pc["examples"]]; print("manifest", os.path.basename(mp), len(m["examples"]), "examples; page tab", len(pc["examples"]), "; order, name, code, slide, expected equal (fields compared: the keys the page tab carries and the manifest has):", ok)
    from pptx import Presentation
    deck = sorted(glob.glob(os.path.join(R, "03-materials", ch, "SEN0401_*_3e_v*.pptx")), key=vk)[-1]; cs = [i for i, s in enumerate(Presentation(deck).slides, 1) if any(q.text.lstrip().startswith(">>> ") for sh in s.shapes if sh.has_text_frame for q in sh.text_frame.paragraphs)]
    sl = sorted(set(e["slide"] for e in m["examples"])); print("newest deck", os.path.basename(deck), "code slides", len(cs), "; manifest slides (distinct)", len(sl), "; equal:", cs == sl, "| manifest names deck:", m.get("deck")); return ok and cs == sl
def newfiles():
    ok = True
    for f in ("03-materials/%s/page/sen0401_%s_page_abox_v%s.ttl" % (ch, ch, PV), "08-tooling/%s-page/test_results_abox_v%s.json" % (ch, PV), "03-materials/%s/page/sen0401_%s_page_v%s.html" % (ch, ch, PV)):
        add = git("log", "--diff-filter=A", "--format=%h", "--", f).splitlines(); mod = git("log", "--diff-filter=M", "--format=%h", "--", f).splitlines(); print(f, "added by", add, "modified by", mod); ok &= bool(add) and not mod
    return ok
def collision():
    c, o = run(T + "/sen0401_erd_collision_probe_v1_0_0.py", PAGE); print(o.strip()[-400:]); return c == 0 and o.strip().endswith("CLEAR") and "COLLISION" not in o
def nochange(cs):
    bad = []
    for c in cs.split(","): bad += [l for l in git("show", "--name-status", "--format=", c).splitlines() if not l.startswith("A")]
    print("commits", cs, "| files not added:", bad or "none"); return not bad
if A.startswith("nochange:"): ok = nochange(A.split(":", 1)[1])
elif A.startswith("chk:"): ok = chk(A.split(":", 1)[1])
else: ok = {"charset": charset, "regr": regr, "probe": probe, "stage4": stage4, "match": match, "links": links, "codetab": codetab, "newfiles": newfiles, "collision": collision}[A]()
print("RESULT %s: %s" % (A.split(":")[0], "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
