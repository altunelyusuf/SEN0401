#!/usr/bin/env python3
"""sen0401_lineage_gate_check v1_0_0 - the exit-code form of the elements of the criteria AC3P_Template and AC3P_Test (and, later, AC3P_Regression), so the evidence bridge can run them (exit 0 = the element is met as the criterion states it; 1 = not met; nothing is skipped).
Usage: sen0401_lineage_gate_check_v1_0_0.py KIND[:ARG]
  tplnew        template 9.51.1 exists as a new file, 9.51.0 is byte-identical to the recorded SHA-256, the version comment of 9.51.1 names 9.51.1
  tpldiff       the difference 9.51.0 -> 9.51.1 is the new version comment and lines inside the function rlUntangle, nothing else
  overlap:NN    a scratch build of the page 9.78.0 of chapter NN on 9.51.1 (built here, outside the repository) and on 9.51.0: after the drag and Untangle of the concept map, 0 overlapping boxes on 9.51.1 (the 9.51.0 count is printed)
  testnew       tests 9.34.1 and 9.35.1 exist as new files, 9.34.0 and 9.35.0 are byte-identical to the recorded SHA-256
  testdiff      each new test differs from its old one only in the version line, comment lines, the HASMENT line and the one assertion line; the sets of feature texts are equal
  testrun:NN    the 9.35.1 run of chapter NN kept in 08-tooling/verify/iter16/chNN: ch01 = exit 0, all widgets passed, no [FAIL]; ch10 = the mentioned-together feature PASSES and no other feature fails except the concept-map overlap feature of the template
"""
__version__ = "1.0.0"
import difflib, glob, hashlib, json, os, re, subprocess, sys, tempfile
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
OLD = {"course_page_template_v9_51_0.html": "cab2ab8809507acf42805ad67b0c1181ce73d65edcc05e864d0ca5ade2e543a4", "sen0401_page_test_v9_34_0.py": "545a7d9470c959e4a9d6a568370e6f51f4f7dcb45d84975aa1e6c8ecdcdd2675", "sen0401_page_test_v9_35_0.py": "a8a39cc9b943cdd99a43f66d755fc6c7c22015131211e43009436125e7e113bf"}
sha = lambda f: hashlib.sha256(open(os.path.join(H, f), "rb").read()).hexdigest()
rd = lambda f: open(os.path.join(H, f), encoding="utf-8").read().splitlines()


def changed(a, b):
    """(old line numbers removed, new lines added with their new line numbers)"""
    rem, add = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            rem += [(i + 1, a[i]) for i in range(i1, i2)]; add += [(j + 1, b[j]) for j in range(j1, j2)]
    return rem, add


def main():
    kind, _, arg = sys.argv[1].partition(":")
    if kind == "tplnew":
        n = "course_page_template_v9_51_1.html"; ok = os.path.exists(os.path.join(H, n)); o = sha("course_page_template_v9_51_0.html") == OLD["course_page_template_v9_51_0.html"]
        v = ok and "9.51.1" in "\n".join(rd(n)[:3])
        print("9.51.1 exists %s; 9.51.0 byte-identical to cab2ab88... %s; version comment names 9.51.1 %s; 9.51.1 sha256 %s" % (ok, o, v, sha(n) if ok else "-")); sys.exit(0 if ok and o and v else 1)
    if kind == "tpldiff":
        a = rd("course_page_template_v9_51_0.html"); b = rd("course_page_template_v9_51_1.html")
        s = next(i for i, l in enumerate(b) if l.startswith("function rlUntangle(")); e = next((i for i in range(s + 1, len(b)) if b[i].startswith("function ") or b[i].startswith("// ")), len(b))
        rem, add = changed(a, b)
        outside = [(n, l[:60]) for n, l in add if not (n <= 3 and "9.51.1" in l) and not (s < n <= e)]
        outside_rem = [(n, l[:60]) for n, l in rem if not (s <= n <= e) and not (n <= 3 and any(l in al for an, al in add if an <= 3))]   # the version comment line keeps the old text inside the new one
        print("rlUntangle spans lines %d-%d of 9.51.1; removed lines %d, added lines %d; added outside the version comment and rlUntangle: %s; removed outside rlUntangle: %s" % (s + 1, e, len(rem), len(add), outside, outside_rem))
        sys.exit(0 if not outside and not outside_rem and add else 1)
    if kind == "testnew":
        ok = all(os.path.exists(os.path.join(H, "sen0401_page_test_v9_3%d_1.py" % k)) for k in (4, 5)); o = all(sha(f) == h for f, h in OLD.items() if f.startswith("sen0401_page_test"))
        print("9.34.1 and 9.35.1 exist %s; 9.34.0 and 9.35.0 byte-identical to the recorded SHA-256 %s" % (ok, o)); sys.exit(0 if ok and o else 1)
    if kind == "testdiff":
        bad = []; sets = []
        for k in (4, 5):
            a = rd("sen0401_page_test_v9_3%d_0.py" % k); b = rd("sen0401_page_test_v9_3%d_1.py" % k); rem, add = changed(a, b)
            ok = lambda l: l.startswith("__version__") or l.lstrip().startswith("#") or "HASMENT" in l or "mentioned-together relationships on by default" in l
            bad += [("9.3%d.1" % k, n, l[:70]) for n, l in add if not ok(l)] + [("9.3%d.0" % k, n, l[:70]) for n, l in rem if not ok(l)]
            f = lambda L: re.findall(r'\b(?:feat|skip)\(\s*"((?:[^"\\]|\\.)*)"', "\n".join(L)); fa, fb = f(a), f(b); sets.append((k, len(fa), len(fb), fa == fb))
        print("lines changed outside version, comments, HASMENT and the one assertion: %s; feature texts (old, new, equal in order): %s" % (bad, sets)); sys.exit(0 if not bad and all(x[3] and x[1] > 0 for x in sets) else 1)
    if kind == "testrun":
        d = os.path.join(H, "verify", "iter16", "ch" + arg); lg = sorted(glob.glob(os.path.join(d, "page_test_9_35_1_*_run1.log")))[-1]; full = lg.replace(".log", ".full.log")
        t = open(full, encoding="utf-8", errors="replace").read(); ex = bool(re.search(r"\[exit 0\b", open(lg).read()))
        fails = sorted({re.sub(r"\s{2,}.*", "", l.strip()) for l in t.splitlines() if l.strip().startswith("[FAIL]")}); w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
        ment = [l.strip()[:120] for l in t.splitlines() if "mentioned-together" in l and l.strip().startswith("[")]
        print("%s: exit-0 %s widgets %s fails %s; mentioned-together lines %s" % (os.path.basename(lg), ex, w.groups() if w else None, [f[:150] for f in fails], sorted(set(ment))))
        if arg == "01":
            st = json.load(open(os.path.join(H, "ch01-page", "test_results_abox_v9_70_0.json"))); feats = {m.group(2)[:140] for m in (re.match(r"\[(PASS|FAIL)\]\s(.*)", l.strip()) for l in t.splitlines()) if m}
            print("distinct features %d (stored result of page 9.70.0 with test 9.35.0: %d), widgets %s (stored %d)" % (len(feats), len(st["features"]), w.groups() if w else None, len(st["widgets"])))
            sys.exit(0 if ex and w and w.group(1) == w.group(2) and int(w.group(1)) >= len(st["widgets"]) and len(feats) >= len(st["features"]) and not fails else 1)
        other = [f for f in fails if "mentioned-together" in f or "Untangle leaves no two boxes overlapping" not in f]
        sys.exit(0 if ment and all(x.startswith("[PASS]") for x in ment) and not other else 1)
    if kind == "clickfact":
        src = "\n".join(rd("sen0401_page_test_v9_35_1.py")); drag = re.search(r"g0 = .*#oerd \.oe-e.*", src); clk = re.search(r"#oerd \.oe-e\"\)\.nth\(_ti\)\.click\(\)", src)
        lg = open(os.path.join(H, "verify", "iter14", "ch11", "page_test_9_35_0_run1.full.log"), encoding="utf-8", errors="replace").read(); hit = "HeaderFields" in lg and "intercepts pointer events" in lg
        ev = open(os.path.join(H, "page-gates-evidence", "template_v9_51_1.md"), encoding="utf-8").read(); fact = "FACT" in ev and "test artefact" in ev
        print("test 9.35.1 drags the first ERD entity (found %s) and later clicks entity nth(_ti) (found %s); the control log of chapter 11 shows HeaderFields intercepting pointer events (%s); the executor's evidence states the cause as a test artefact (%s)" % (bool(drag), bool(clk), hit, fact))
        sys.exit(0 if drag and clk and hit and fact else 1)
    if kind == "nochange":
        cs = {"T": ["2654ae9"], "S": ["a626896", "0cfd139", "aa9c24b"]}[arg]; st = []
        for c in cs: st += [l for l in subprocess.run(["git", "show", "--name-status", "--format=", c], cwd=R, capture_output=True, text=True).stdout.splitlines() if l.strip()]
        bad = [l for l in st if not l.startswith("A\t")]; print("commits %s: %d file(s) added, %d changed or removed %s" % (", ".join(cs), len(st) - len(bad), len(bad), bad[:5])); sys.exit(0 if st and not bad else 1)
    if kind == "overlap":
        sys.exit(overlap(arg))
    raise SystemExit(__doc__)


def overlap(nn):
    ev = os.path.join(H, "page-gates-evidence"); probe = os.path.join(ev, "template_v9_51_1_map_probe.py"); rl = os.path.join(ev, "template_v9_51_1_map_probe_drag_target.js")
    res = {}
    for tpl in ("course_page_template_v9_51_0.html", "course_page_template_v9_51_1.html"):
        sc = tempfile.mkdtemp(prefix="sen0401_fx_gate_"); os.makedirs(os.path.join(sc, "08-tooling")); os.makedirs(os.path.join(sc, "03-materials", "ch" + nn))
        for f in os.listdir(H):
            if f == "ch%s-page" % nn:
                subprocess.run(["cp", "-r", os.path.join(H, f), os.path.join(sc, "08-tooling", f)])
            else:
                os.symlink(os.path.join(H, f), os.path.join(sc, "08-tooling", f))
        for f in os.listdir(os.path.join(R, "03-materials", "ch" + nn)):
            if f != "page": os.symlink(os.path.join(R, "03-materials", "ch" + nn, f), os.path.join(sc, "03-materials", "ch" + nn, f))
        os.makedirs(os.path.join(sc, "03-materials", "ch" + nn, "page"))
        for f in os.listdir(os.path.join(R, "03-materials")):
            if f != "ch" + nn: os.symlink(os.path.join(R, "03-materials", f), os.path.join(sc, "03-materials", f))
        for f in os.listdir(R):
            if f not in ("08-tooling", "03-materials") and not f.startswith(".git") and not os.path.exists(os.path.join(sc, f)): os.symlink(os.path.join(R, f), os.path.join(sc, f))
        r = subprocess.run([sys.executable, "-B", os.path.join(sc, "08-tooling", "sen0401_page_build_v4_14_0.py"), nn], cwd=sc, capture_output=True, text=True, env=dict(os.environ, PAGE_VER="9_78_0", PAGE_TEMPLATE=tpl))
        page = os.path.join(sc, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v9_78_0.html" % nn)
        if not os.path.exists(page):
            print("build failed for", tpl, (r.stdout + r.stderr)[-300:]); return 1
        p = subprocess.run([sys.executable, "-B", probe, page, rl], capture_output=True, text=True, timeout=600)
        m = re.search(r"AFTER UNTANGLE: boxes (\d+) overlaps (\d+)", p.stdout); res[tpl] = (int(m.group(1)), int(m.group(2))) if m else None
        subprocess.run(["rm", "-rf", sc])
    a, b = res["course_page_template_v9_51_0.html"], res["course_page_template_v9_51_1.html"]
    print("chapter %s concept map after drag and Untangle: template 9.51.0 boxes/overlaps %s; template 9.51.1 boxes/overlaps %s" % (nn, a, b))
    return 0 if b and b[1] == 0 else 1


main()
