#!/usr/bin/env python3
"""sen0401_template9524_control_check v1_0_0 - the lineage agent's OWN check of the page template 9.52.4 (criterion AC9_Template9524). Usage: sen0401_template9524_control_check_v1_0_0.py sha | nomod | pairs | probe | regr | nochange:COMMITS
sha: 9.52.2 and 9.52.3 are byte-identical to their present committed content (SHA-256 9089403f...73db, 44bcb3e7...564d) and 9.52.4 is byte-identical to 9.52.3.
nomod: 9.52.4 was added by exactly one commit and no commit modifies it.
pairs: scratch pages of chapters 1, 5, 6, 7, 8 and 10 (newest page version of each) built with the page builder v4_15_0 from 9.52.4 and from 9.52.3 are byte-identical in pairs.
probe: the story layout probe v1_0_0 on the 9.52.4 scratch pages of chapters 5 to 8 (copied beside a scratch tree) gives RESULT PASS on each (the caller holds the lock).
regr: the control's own page-test runs (verify/iter32/ctl_template9524/regr_*.full.log) on the chapter 5 scratch page built from 9.52.4: 9.37.0, 9.34.1, 9.35.1 each exit with every widget passed, no [FAIL], and widgets/features/gates at or above the stored results.
nochange:COMMITS: the commits only ADD files."""
import glob, hashlib, os, re, shutil, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T)
def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout.strip()
sh = lambda p: hashlib.sha256(open(os.path.join(R, p), "rb").read()).hexdigest()
P = lambda v: "08-tooling/course_page_template_v9_52_%d.html" % v
def sha():
    a, b, c = sh(P(2)), sh(P(3)), sh(P(4)); ok = a.startswith("9089403f") and a.endswith("73db") and b.startswith("44bcb3e7") and b.endswith("564d") and c == b; print("9.52.2", a); print("9.52.3", b); print("9.52.4", c); print("9.52.2 and 9.52.3 as expected, 9.52.4 equals 9.52.3:", ok); return ok
def nomod():
    add = git("log", "--diff-filter=A", "--format=%h", "--", P(4)).splitlines(); mod = git("log", "--diff-filter=M", "--format=%h", "--", P(4)).splitlines(); print("added by", add, "| modified by", mod); return len(add) == 1 and not mod
PAGES = (("01", "9_70_0"), ("05", "9_83_0"), ("06", "9_83_0"), ("07", "9_84_0"), ("08", "9_85_0"), ("10", "9_79_0"))
def build(n, pv, tpl, out):
    os.makedirs(out, exist_ok=True); r = subprocess.run([sys.executable, "-B", T + "/sen0401_page_build_v4_15_0.py", n], capture_output=True, text=True, env=dict(os.environ, PAGE_VER=pv, PAGE_TEMPLATE=tpl, PAGE_SCRATCH=out), cwd=R); return r.returncode
def pairs():
    ok = True; S = "/tmp/claude-0/s/ctl59p"; shutil.rmtree(S, ignore_errors=True)
    for n, pv in PAGES:
        r4 = build(n, pv, "course_page_template_v9_52_4.html", S + "/a%s" % n); r3 = build(n, pv, "course_page_template_v9_52_3.html", S + "/b%s" % n); f = "sen0401_ch%s_page_v%s.html" % (n, pv)
        h4 = hashlib.sha256(open(S + "/a%s/%s" % (n, f), "rb").read()).hexdigest(); h3 = hashlib.sha256(open(S + "/b%s/%s" % (n, f), "rb").read()).hexdigest(); print("chapter", n, pv, "builds exit", r4, r3, "| 9.52.4", h4[:16], "9.52.3", h3[:16], "equal:", h4 == h3); ok &= r4 == 0 and r3 == 0 and h4 == h3
    shutil.rmtree(S, ignore_errors=True); return ok
def probe():
    ok = True; S = "/tmp/claude-0/s/ctl59q"; shutil.rmtree(S, ignore_errors=True); os.makedirs(S + "/08-tooling"); shutil.copy(T + "/sen0401_story_layout_probe_v1_0_0.py", S + "/08-tooling/")
    for n, pv in PAGES[1:5]:
        out = S + "/03-materials/ch%s/page" % n; b = build(n, pv, "course_page_template_v9_52_4.html", out); r = subprocess.run([sys.executable, "-B", S + "/08-tooling/sen0401_story_layout_probe_v1_0_0.py", n, pv], capture_output=True, text=True); lines = r.stdout.strip().splitlines()
        print("chapter", n, "page", pv, "build exit", b, "|", " ".join(l for l in lines if l.startswith(("CHECKS", "RESULT")))); ok &= b == 0 and r.returncode == 0 and "RESULT: PASS" in r.stdout
    shutil.rmtree(S, ignore_errors=True); return ok
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = {l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")}; w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
def regr():
    D = T + "/verify/iter32/ctl_template9524"; ok = True; ref = {"9_37_0": (113, 199, 6, 0), "9_34_1": (113, 187, 6, 0), "9_35_1": (113, 187, 6, 0)}; seen = set()
    for v, (rw, rf, rg, rs) in ref.items():
        p = D + "/regr_ch05_page_9_83_0_test_%s.full.log" % v
        if not os.path.exists(p): print(v, "missing"); ok = False; continue
        feats, skips, w, g = parse(open(p, errors="replace").read()); fails = [k for k, x in feats.items() if x == "FAIL"]; good = bool(w) and w[0] == w[1] and w[0] >= rw and not fails and len(feats) >= rf and g >= rg and len(skips) <= rs
        print("ch05 9_83_0 test", v, ": widgets", w, "features", len(feats), "gates", g, "skips", len(skips), "FAIL", len(fails), "| stored", (rw, rf, rg, rs), "->", "ok" if good else "NOT OK"); ok &= good
    return ok
def nochange(cs):
    bad = []
    for c in cs.split(","): bad += [l for l in git("show", "--name-status", "--format=", c).splitlines() if not l.startswith("A")]
    print("commits", cs, "| files not added:", bad or "none"); return not bad
a = sys.argv[1]; ok = nochange(a.split(":", 1)[1]) if a.startswith("nochange:") else {"sha": sha, "nomod": nomod, "pairs": pairs, "probe": probe, "regr": regr}[a](); print("RESULT %s: %s" % (a.split(":")[0], "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
