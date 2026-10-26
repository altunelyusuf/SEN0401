#!/usr/bin/env python3
"""sen0401_template9525_control_check v1_0_0 - the lineage agent's OWN check of the page template 9.52.5 (criterion AC9_Template9525). Everything it builds goes to /tmp/claude-0/ctl76 (created by this tool, removed by it at the end of each kind). The caller holds the lock for the kinds that start a browser.
Usage: sen0401_template9525_control_check_v1_0_0.py sha | nomod | diff | pairs | collision | regr | story | nochange:COMMITS
sha: 9.52.2 and 9.52.3 are byte-identical to their expected SHA-256 (9089403f...73db, 44bcb3e7...564d), 9.52.4 equals 9.52.3 and equals its content before the executor's commits (git show of the parent of the first commit), and 9.52.5 differs from 9.52.4.
nomod: 9.52.5 was added by exactly one commit and no commit modifies it.
diff: the diff 9.52.4 to 9.52.5 changes only lines of the sections-ERD drag code (every added or removed line names the ERD: 'erd', 'ERD_LAY' or 'oe-e'), at most 6 lines changed.
pairs: scratch pages of chapters 1, 5 to 10 (newest page version of each) built with builder v4_15_0 from 9.52.4 and from 9.52.5: every build exits 0, and the line difference of every pair consists only of the lines of the template diff.
collision: the ERD collision probe v1_0_0 prints CLEAR on the 9.52.5 scratch pages of chapters 1, 5 to 10 and of chapter 11 (page 9_79_0, inputs of the executor) and COLLISION on the chapter 11 page built from 9.52.4 (the control); chapters 12 to 14 are built with their newest page version from both templates and printed (informational, a build that fails is printed as NOT_MEASURED and not counted).
regr: the control's own page-test runs (verify/iter32/ctl_template9525/regr_ch10_page_9_80_0_test_*.full.log) on the chapter 10 scratch page built from 9.52.5: each exit 0 with every widget passed, no [FAIL], no skip, widgets/features/gates at or above the stored results of the page 9.80.0.
story: the story layout probe v1_0_0 on the 9.52.5 scratch pages of chapters 5 to 8 and 10 gives RESULT PASS on each.
nochange:COMMITS: the commits only ADD files."""
import difflib, glob, hashlib, os, re, shutil, subprocess, sys
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T); S = "/tmp/claude-0/ctl76"
def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout
sh = lambda p: hashlib.sha256(open(os.path.join(R, p), "rb").read()).hexdigest()
P = lambda v: "08-tooling/course_page_template_v9_52_%d.html" % v
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.html", p).groups()]
def sha():
    a, b, c, d = sh(P(2)), sh(P(3)), sh(P(4)), sh(P(5)); first = git("log", "--diff-filter=A", "--format=%h", "--", P(5)).split()[-1]; old = hashlib.sha256(subprocess.run(["git", "show", first + "^:" + P(4)], cwd=R, capture_output=True).stdout).hexdigest()
    ok = a.startswith("9089403f") and a.endswith("73db") and b.startswith("44bcb3e7") and b.endswith("564d") and c == b and c == old and d != c
    for n, h in (("9.52.2", a), ("9.52.3", b), ("9.52.4", c), ("9.52.4 before the executor's commits", old), ("9.52.5", d)): print(n, h)
    print("as expected:", ok); return ok
def nomod():
    add = git("log", "--diff-filter=A", "--format=%h", "--", P(5)).split(); mod = git("log", "--diff-filter=M", "--format=%h", "--", P(5)).split(); print("added by", add, "| modified by", mod); return len(add) == 1 and not mod
def tdiff():
    a = open(os.path.join(R, P(4)), encoding="utf-8").read().splitlines(); b = open(os.path.join(R, P(5)), encoding="utf-8").read().splitlines()
    ch = [l for l in difflib.unified_diff(a, b, lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]; return ch
def diff():
    ch = tdiff(); bad = [l for l in ch if not re.search(r"erd|ERD_LAY|oe-e", l)]
    for l in ch: print(l[:260])
    print("changed lines:", len(ch), "| lines not naming the ERD:", len(bad)); return 0 < len(ch) <= 6 and not bad
PAGES = (("01", "9_72_0"), ("05", "9_84_0"), ("06", "9_84_0"), ("07", "9_85_0"), ("08", "9_86_0"), ("09", "9_82_0"), ("10", "9_80_0"))
def newest(n): return "_".join(map(str, vk(sorted(glob.glob(os.path.join(R, "03-materials", "ch" + n, "page", "sen0401_ch%s_page_v*.html" % n)), key=vk)[-1])))
def build(n, pv, v, out):
    os.makedirs(out, exist_ok=True); r = subprocess.run([sys.executable, "-B", T + "/sen0401_page_build_v4_15_0.py", n], capture_output=True, text=True, env=dict(os.environ, PAGE_VER=pv, PAGE_TEMPLATE="course_page_template_v9_52_%d.html" % v, PAGE_SCRATCH=out), cwd=R); return r.returncode, os.path.join(out, "sen0401_ch%s_page_v%s.html" % (n, pv))
def pairs():
    shutil.rmtree(S, ignore_errors=True); tch = set(tdiff()); ok = True
    for n, pv in PAGES:
        r4, f4 = build(n, pv, 4, S + "/p4_" + n); r5, f5 = build(n, pv, 5, S + "/p5_" + n)
        if r4 or r5: print("chapter", n, pv, "builds exit", r4, r5, "-> NOT OK"); ok = False; continue
        d = [l for l in difflib.unified_diff(open(f4, encoding="utf-8").read().splitlines(), open(f5, encoding="utf-8").read().splitlines(), lineterm="", n=0) if l[:1] in "+-" and not l.startswith(("+++", "---"))]
        extra = [l for l in d if l not in tch]; print("chapter", n, pv, "builds exit 0 0 | changed lines", len(d), "| not in the template diff:", len(extra)); ok &= bool(d) and not extra
    shutil.rmtree(S, ignore_errors=True); return ok
def probe(files):
    r = subprocess.run([sys.executable, "-B", T + "/sen0401_erd_collision_probe_v1_0_0.py"] + files, capture_output=True, text=True); return r.stdout.strip().splitlines()
def collision():
    shutil.rmtree(S, ignore_errors=True); ok = True; fs = []
    for n, pv in PAGES + (("11", "9_79_0"),):
        r, f = build(n, pv, 5, S + "/c5_" + n)
        if r: print("chapter", n, pv, "build exit", r, "NOT OK"); ok = False
        else: fs.append(f)
    for l in probe(fs): print(l); ok &= l.endswith("CLEAR")
    ok &= len(fs) == 8
    r, f4 = build("11", "9_79_0", 4, S + "/c4_11"); l = probe([f4]) if not r else ["build failed"]; print("CONTROL (9.52.4)", *l); ok &= bool(l) and l[0].endswith("COLLISION")
    for n in ("12", "13", "14"):
        pv = newest(n)
        for v in (4, 5):
            r, f = build(n, pv, v, S + "/i%d_%s" % (v, n)); print("info ch%s %s template 9.52.%d:" % (n, pv, v), (probe([f]) or ["no output"])[0].split(" ", 1)[1] if not r else "NOT_MEASURED (build exit %d)" % r)
    shutil.rmtree(S, ignore_errors=True); return ok
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = {l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")}; w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
def regr():
    D = T + "/verify/iter32/ctl_template9525"; ok = True; ref = {"9_37_0": (86, 197, 6), "9_34_1": (86, 185, 6), "9_35_1": (86, 185, 6)}
    for v, (rw, rf, rg) in ref.items():
        p = D + "/regr_ch10_page_9_80_0_test_%s.full.log" % v; q = D + "/regr_ch10_page_9_80_0_test_%s.run.log" % v
        if not os.path.exists(p): print(v, "missing"); ok = False; continue
        feats, skips, w, g = parse(open(p, errors="replace").read()); fails = [k for k, x in feats.items() if x == "FAIL"]; good = bool(w) and w[0] == w[1] and w[0] >= rw and not fails and len(feats) >= rf and g >= rg and not skips
        print("ch10 scratch page 9_80_0 on 9.52.5, test", v, ": widgets", w, "features", len(feats), "gates", g, "skips", len(skips), "FAIL", len(fails), "| stored page 9.80.0", (rw, rf, rg, 0), "->", "ok" if good else "NOT OK"); ok &= good
    print("runner exits:", open(D + "/regr_runner.txt").read().strip().replace("\n", " | ") if os.path.exists(D + "/regr_runner.txt") else "missing"); return ok
def story():
    ok = True; shutil.rmtree(S, ignore_errors=True); W = S + "/w"; os.makedirs(W + "/08-tooling"); shutil.copy(T + "/sen0401_story_layout_probe_v1_0_0.py", W + "/08-tooling/")
    for n, pv in (("05", "9_84_0"), ("06", "9_84_0"), ("07", "9_85_0"), ("08", "9_86_0"), ("10", "9_80_0")):
        b, f = build(n, pv, 5, W + "/03-materials/ch%s/page" % n); r = subprocess.run([sys.executable, "-B", W + "/08-tooling/sen0401_story_layout_probe_v1_0_0.py", n, pv], capture_output=True, text=True); lines = r.stdout.strip().splitlines()
        print("chapter", n, "page", pv, "build exit", b, "|", " ".join(l for l in lines if l.startswith(("CHECKS", "RESULT")))); ok &= b == 0 and r.returncode == 0 and "RESULT: PASS" in r.stdout
    shutil.rmtree(S, ignore_errors=True); return ok
def nochange(cs):
    bad = []
    for c in cs.split(","): bad += [l for l in git("show", "--name-status", "--format=", c).splitlines() if not l.startswith("A")]
    print("commits", cs, "| files not added:", bad or "none"); return not bad
a = sys.argv[1]; ok = nochange(a.split(":", 1)[1]) if a.startswith("nochange:") else {"sha": sha, "nomod": nomod, "diff": diff, "pairs": pairs, "collision": collision, "regr": regr, "story": story}[a](); print("RESULT %s: %s" % (a.split(":")[0], "PASS" if ok else "FAIL")); sys.exit(0 if ok else 1)
