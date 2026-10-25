#!/usr/bin/env python3
"""sen0401_template_control_check v1_0_0 - the lineage agent's OWN check of the page template 9.52.3 (criterion AC9_Template). Usage: sen0401_template_control_check_v1_0_0.py sha | diff | probe | regr | nochange
sha: 9.52.2 is byte-identical to its first commit (git), and 9.52.3 has the SHA-256 the executor reported (44bcb3e7...564d).
diff: every line that differs between 9.52.2 and 9.52.3 is a rule of the Stories tab (a line with .simgrow, .story, or a @media block of those).
probe: scratch pages of chapters 5 to 8 are built from the present page data with the page builder v4_15_0 and PAGE_TEMPLATE=9.52.3 (into /tmp, not shipped) and the story layout probe v1_0_0 gives RESULT PASS on each (run by this check, under the caller's lock).
regr: the lineage agent's own runs (verify/iter32/ctl_template/regr_*.full.log, page test run on scratch pages built from 9.52.3 beside the real tree) each exit with every widget passed, no [FAIL] line, widgets >= and features >= and gates >= the stored result of the shipped page (test_results_abox_vPV.json) and skips <= stored.
nochange: no committed file is edited: the template 9.52.3 and its logs were only ADDED (git log --diff-filter=M over them is empty). Names every modification."""
import glob, hashlib, json, os, re, shutil, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout.strip()
P2 = "08-tooling/course_page_template_v9_52_2.html"; P3 = "08-tooling/course_page_template_v9_52_3.html"
def sha():
    first = git("log", "--diff-filter=A", "--format=%H", "--", P2).splitlines()[-1]; same = git("rev-parse", first + ":" + P2) == git("rev-parse", "HEAD:" + P2) and not git("log", "--diff-filter=M", "--format=%h", "--", P2)
    h = hashlib.sha256(open(os.path.join(R, P3), "rb").read()).hexdigest(); ok3 = h.startswith("44bcb3e7") and h.endswith("564d"); print("9.52.2 identical to its first commit:", same); print("9.52.3 SHA-256", h, "matches the reported 44bcb3e7...564d:", ok3); return same and ok3
def diff():
    a = open(os.path.join(R, P2)).read().splitlines(); b = open(os.path.join(R, P3)).read().splitlines(); import difflib
    ch = [l[1:] for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---")]; bad = [l[:120] for l in ch if not re.search(r"\.simgrow|\.story|figcaption|\.takeaway", l)]
    print(len(ch), "changed lines;", "not a story rule:", bad or "none"); return not bad
def probe():
    ok = True; S = "/tmp/claude-0/s/ctl57b"; shutil.rmtree(S, ignore_errors=True); os.makedirs(S + "/08-tooling"); shutil.copy(T + "/sen0401_story_layout_probe_v1_0_0.py", S + "/08-tooling/")
    for n, pv in (("05", "9_83_0"), ("06", "9_83_0"), ("07", "9_84_0"), ("08", "9_85_0")):
        out = S + "/03-materials/ch%s/page" % n; os.makedirs(out); env = dict(os.environ, PAGE_VER=pv, PAGE_TEMPLATE="course_page_template_v9_52_3.html", PAGE_SCRATCH=out)
        b = subprocess.run([sys.executable, "-B", T + "/sen0401_page_build_v4_15_0.py", n], capture_output=True, text=True, env=env, cwd=R)
        r = subprocess.run([sys.executable, "-B", S + "/08-tooling/sen0401_story_layout_probe_v1_0_0.py", n, pv], capture_output=True, text=True); lines = r.stdout.strip().splitlines(); print("chapter", n, "page", pv, "build exit", b.returncode, "|", " ".join(l for l in lines if l.startswith(("CHECKS", "RESULT")))); ok &= b.returncode == 0 and r.returncode == 0 and "RESULT: PASS" in r.stdout
    shutil.rmtree(S, ignore_errors=True); return ok
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = {l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")}; w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
def regr():
    D = os.path.join(T, "verify/iter32/ctl_template"); ok = True; runs = sorted(glob.glob(D + "/regr_ch*_page_*_test_*.full.log")); want = {("05", "9_83_0", "9_37_0"), ("05", "9_83_0", "9_34_1"), ("05", "9_83_0", "9_35_1"), ("01", "9_70_0", "9_34_1"), ("01", "9_70_0", "9_35_1"), ("10", "9_79_0", "9_34_1"), ("10", "9_79_0", "9_35_1")}; seen = set()
    for f in runs:
        n, pv, ver = re.match(r".*regr_ch(\d+)_page_([\d_]+)_test_([\d_]+)\.full\.log", f).groups(); seen.add((n, pv, ver)); feats, skips, w, gates = parse(open(f, errors="replace").read()); fails = [k for k, v in feats.items() if v == "FAIL"]
        cands = sorted(glob.glob(T + "/verify/iter19/pages/ch%s_page_%s_test_%s.full.log" % (n, pv, ver)) + glob.glob(T + "/page-gates-evidence/regression/R16_%s_ch%s_%s.full.log" % (ver, n, pv)) + glob.glob(T + "/page-gates-evidence/I16test_%s_ch%s_%s.full.log" % (ver, n, pv)))
        if cands: rf, rs, rw, rg = parse(open(cands[0], errors="replace").read()); ref = (rw[0] if rw else 0, len(rf), rg, len(rs)); src = os.path.relpath(cands[0], T)
        else:
            st0 = json.load(open(os.path.join(T, "ch%s-page" % n, "test_results_abox_v%s.json" % pv))); cnt = lambda x: len(x) if isinstance(x, (list, dict)) else (x or 0); ref = (cnt(st0.get("widgets")), cnt(st0.get("features")), cnt(st0.get("gates")), cnt(st0.get("skipped", 0))); src = "test_results_abox_v%s.json" % pv
        rw0 = int(w[0]) if w else 0; good = bool(w) and w[0] == w[1] and rw0 >= int(ref[0]) and not fails and len(feats) >= ref[1] and gates >= ref[2] and len(skips) <= ref[3]
        print("ch%s page %s test %s: widgets %s, features %d, gates %d, skips %d, FAIL %d | stored (%s): widgets %s, features %s, gates %s, skips %s -> %s" % (n, pv, ver, w, len(feats), gates, len(skips), len(fails), src, ref[0], ref[1], ref[2], ref[3], "ok" if good else "NOT OK")); ok &= good
    missing = want - seen; print("runs missing:", sorted(missing) or "none"); return ok and not missing
def nochange():
    mods = git("log", "--diff-filter=M", "--format=%h %s", "--", P3, "08-tooling/verify/iter24/template").splitlines()
    print("commits that MODIFIED a committed file of the template task:", len(mods)); [print("  ", m[:150]) for m in mods]; return not mods
a = sys.argv[1]; ok = {"sha": sha, "diff": diff, "probe": probe, "regr": regr, "nochange": nochange}[a](); print("RESULT %s: %s" % (a, "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
