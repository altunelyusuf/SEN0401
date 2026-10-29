#!/usr/bin/env python3
"""sen0401_pageclick_control_check v1.0.0 - the control's OWN checks of the page tests 9.34.2 and 9.35.2 (story ST_PageTest_Click, criterion AC9_PageTest_Click). A NEW tool; it edits nothing.
Usage: sen0401_pageclick_control_check_v1_0_0.py KIND [COMMITS]
  sha      9.34.1, 9.35.1 and 9.37.0 have the same SHA-256 in the commit before the executor's work as now, and no later commit touches them
  diff     each new test against its predecessor: the removed lines are only the version line and the one click line; the added lines are only the version line, header comment lines and the new tap (and the line that continues after it, equal to the rest of the removed line)
  regr     the control's own runs of 9.34.2 and 9.35.2 on the chapter 10 page 9.80.0 (verify/iter32/bridge_pgclick/runs): widgets all passed, no [FAIL], no skip, widgets/features/gates at or above the stored results (the stored result of page 9.80.0 and the stored 9.34.1/9.35.1 logs of page 9.77.0)
  fixture  the control's own runs on a COPY of the chapter 10 page with the fixture script injected: 9.34.1 and 9.35.1 exit non-zero with a failing line about the click, 9.34.2 and 9.35.2 exit 0 with every widget passed, no [FAIL], and the fixture script was injected in every run; the predecessors print the line "intercepts pointer events" (an entity drawn later covers the dragged one), the new tests print the feature line of the drag and tap as PASS with {'card': True}
  nochange every file of the executor's commits was added (none modified or deleted)
Exit 0 only when the kind holds."""
__version__ = "1.0.0"
import glob, hashlib, json, os, re, subprocess, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); T = os.path.join(R, "08-tooling"); PARENT = "d5ce9bd"; RUNS = os.path.join(T, "verify/iter32/bridge_pgclick/runs")
def git(*a): return subprocess.run(["git", "-C", R] + list(a), capture_output=True, text=True).stdout
def done(ok, kind): print("RESULT " + ("PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = [l for l in t.splitlines() if l.strip().startswith("[SKIP]")]; w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
def k_sha():
    ok = True
    for n in ("9_34_1", "9_35_1", "9_37_0"):
        rel = "08-tooling/sen0401_page_test_v%s.py" % n; b = subprocess.run(["git", "-C", R, "show", "%s:%s" % (PARENT, rel)], capture_output=True).stdout; a = open(os.path.join(R, rel), "rb").read()
        same = len(b) > 0 and hashlib.sha256(b).digest() == hashlib.sha256(a).digest(); ch = git("log", "--format=%h", "%s..HEAD" % PARENT, "--", rel).split(); print("%s before(%s) %s after %s later commits %s" % (n, PARENT, hashlib.sha256(b).hexdigest()[:16], hashlib.sha256(a).hexdigest()[:16], ch)); ok &= same and not ch
    done(ok, "sha")
def k_diff():
    import difflib; ok = True
    for n in ("34", "35"):
        a = open(os.path.join(T, "sen0401_page_test_v9_%s_1.py" % n)).read().splitlines(); b = open(os.path.join(T, "sen0401_page_test_v9_%s_2.py" % n)).read().splitlines(); rem = []; add = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag != "equal": rem += a[i1:i2]; add += b[j1:j2]
        click = [l for l in rem if '.nth(_ti).click()' in l]; other = [l for l in rem if l not in click and not l.startswith("__version__")]
        rest = click[0].split(".click();", 1)[1].strip() if click else None; cont = [l for l in add if rest and l.strip().endswith(rest)]
        newl = [l for l in add if not l.startswith("__version__") and not l.lstrip().startswith("# 9.%s.2" % n) and l not in cont]
        print("9.%s: removed %d lines (version line 1, click line %d, other %d); added %d (new tap lines %d, continuation of the removed line %d)" % (n, len(rem), len(click), len(other), len(add), len(newl), len(cont)))
        for l in newl: print("   +", l.strip()[:170])
        good = len(click) == 1 and not other and len(cont) == 1 and 2 <= len(newl) <= 5 and all(re.search(r"_tp|mouse\.click|feat\(", l) for l in newl); print("   ->", "ok" if good else "NOT OK"); ok &= good
    done(ok, "diff")
def stored(v):
    q = sorted(glob.glob(os.path.join(T, "page-gates-evidence/regression/R*_%s_ch10_9_77_0.full.log" % v)))[-1]; f, s, w, g = parse(open(q, errors="replace").read()); return w[0], len(f), g, os.path.basename(q)
def k_regr():
    sj = json.load(open(os.path.join(T, "ch10-page/test_results_abox_v9_80_0.json"))); rw, rf, rg = len(sj["widgets"]), len(sj["features"]), len(sj["gates"]); print("stored result of page 9.80.0 (json): widgets %d features %d gates %d" % (rw, rf, rg)); ok = True
    for v in ("9_34_2", "9_35_2"):
        p = os.path.join(RUNS, "ctl_ch10_page_9_80_0_test_%s.full.log" % v)
        if not os.path.exists(p): print(v, "log missing"); ok = False; continue
        f, s, w, g = parse(open(p, errors="replace").read()); fails = [x for x, y in f.items() if y == "FAIL"]; pw, pf, pg, nm = stored(v.replace("_2", "_1")); rr = open(os.path.join(RUNS, "ctl_ch10_%s.runner.txt" % v)).read()
        good = bool(w) and w[0] == w[1] and w[0] >= max(rw, pw) and not fails and len(f) >= max(pf, 0) and g >= pg and not s and "RESULT: PASS" in rr
        print("9.%s run: widgets %s features %d gates %d skips %d FAIL %d | stored 9.80.0 (%d,%d,%d) and predecessor log %s (%d,%d,%d) | runner: %s -> %s" % (v.replace("_", ".")[2:], w, len(f), g, len(s), len(fails), rw, rf, rg, stored(v.replace("_2", "_1"))[3], pw, pf, pg, [l for l in rr.splitlines() if l.startswith("page 10")], "ok" if good else "NOT OK")); ok &= good
    done(ok, "regr")
def k_fixture():
    ok = True
    for v in ("9_34_1", "9_35_1", "9_34_2", "9_35_2"):
        p = os.path.join(RUNS, "ctl_fixture_%s.full.log" % v); r = os.path.join(RUNS, "ctl_fixture_%s.runner.txt" % v)
        if not (os.path.exists(p) and os.path.exists(r)): print(v, "missing"); ok = False; continue
        t = open(p, errors="replace").read(); rr = open(r).read(); f, s, w, g = parse(t); fails = [x for x, y in f.items() if y == "FAIL"]; moved = 1; tapok = bool(re.search(r"\[PASS\] an entity dragged by pointer moves.*'card': True", t)); inj = "fixture script injected" in rr; passed = "RESULT: PASS" in rr
        if v.endswith("_1"):
            clk = [x for x in fails if re.search(r"click|tap|drag|card|intercept", x, re.I)] + [l.strip()[:200] for l in t.splitlines() if re.search(r"intercepts pointer events", l)][:1]
            good = (not passed) and inj and bool([l for l in t.splitlines() if "intercepts pointer events" in l])
            print("9.%s on the fixture: runner %s; FAIL lines %d %s; click intercepted lines %s; fixture script injected %s -> %s" % (v[2:].replace("_", "."), "FAIL" if not passed else "PASS", len(fails), [x[:90] for x in fails[:3]], bool([l for l in t.splitlines() if "intercepts pointer events" in l]), moved, "ok (fails as the criterion says)" if good else "NOT OK"))
        else:
            good = passed and inj and tapok and bool(w) and w[0] == w[1] and not fails and not s
            print("9.%s on the fixture: runner %s; widgets %s features %d FAIL %d skips %d; drag-and-tap line PASS with the card opened: %s -> %s" % (v[2:].replace("_", "."), "PASS" if passed else "FAIL", w, len(f), len(fails), len(s), tapok, "ok" if good else "NOT OK"))
        ok &= good
    done(ok, "fixture")
def k_nochange(commits):
    bad = []
    for c in commits.split(","):
        for l in git("show", "--name-status", "--format=", c).splitlines():
            if l and not l.startswith("A"): bad.append(l)
    print("commits %s: files not added: %s" % (commits, bad)); done(not bad, "nochange")
if __name__ == "__main__":
    k = sys.argv[1]; c = sys.argv[2] if len(sys.argv) > 2 else ""
    {"sha": k_sha, "diff": k_diff, "regr": k_regr, "fixture": k_fixture, "nochange": lambda: k_nochange(c)}[k]()
