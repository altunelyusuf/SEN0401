#!/usr/bin/env python3
"""sen0401_lineage_page_check v1_1_0 (over 1.0.0: Iter_14, page 9.78.0, logs in verify/iter14; new kinds seclinks, abox, nochange; erd needs BOTH label features to report PASS in the final run with labels shown after Untangle at least 95 percent of before) - the exit-code form of each element of a page criterion of Iter_13 and Iter_14, so the evidence bridge can run it (the bridge treats exit 0 as a pass).
It prints what it found and exits 0 ONLY when the element is met as the criterion states it; 1 when it is not met, including when the element is skipped or not measured (a skip is not a pass).
Usage: sen0401_lineage_page_check_v1_0_0.py KIND:NN      KIND = markers | deck | link | test34 | test35 | counts34 | counts35 | erd
  markers   the page HTML contains 'const LBLRE=LBL.map' and 'function edVars()'
  deck/link pages_deck_match_verify / pages_link_verify report 0 not carried (run now)
  test34/35 the FINAL run of the control (08-tooling/verify/iter13/chNN, written by sen0401_lineage_verify_page) exited 0, with every widget passed and no [FAIL] line
  counts*   that run's widgets, features, gates are at least, and its skipped checks at most, the stored result of the page as it stood (the newest test_results_abox before 9.77.0)
  erd       the 9.35.0 feature 'on-choice labels mode ... Untangle' reports PASS in that run (a [SKIP] or no such line is not met)
"""
__version__ = "1.1.0"
import glob, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); PV = "9_78_0"


def final_log(nn, ver):
    d = os.path.join(H, "verify", "iter14", "ch" + nn)
    runs = sorted(glob.glob(os.path.join(d, "page_test_%s_run[0-9].log" % ver)), key=lambda p: int(re.search(r"run(\d)\.log", p).group(1)))
    return runs[-1], runs[-1].replace(".log", ".full.log"), len(runs)


def parse(full):
    t = open(full, encoding="utf-8", errors="replace").read()
    feats = {}
    for l in t.splitlines():
        s = l.strip()
        m = re.match(r"\[(PASS|FAIL)\]\s(.*)", s)
        if m:
            feats[m.group(2)[:140]] = m.group(1)
    skips = sorted({l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")})
    w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    gates = sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, gates


def stored(nn):
    fs = [f for f in glob.glob(os.path.join(H, "ch%s-page" % nn, "test_results_abox_v*.json")) if "9_77_0" in f]
    f = sorted(fs, key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]])[-1]
    d = json.load(open(f)); return os.path.basename(f), d


def main():
    kind, nn = sys.argv[1].split(":")
    page = os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v%s.html" % (nn, PV))
    if kind == "markers":
        h = open(page, encoding="utf-8").read(); a, b = "const LBLRE=LBL.map" in h, "function edVars()" in h
        print("const LBLRE=LBL.map:", a, "| function edVars():", b); sys.exit(0 if a and b else 1)
    if kind in ("deck", "link"):
        tool = "pages_deck_match_verify_v1_0_0.py" if kind == "deck" else "pages_link_verify_v1_0_0.py"
        o = subprocess.run([sys.executable, "-B", os.path.join(H, tool), nn, PV], capture_output=True, text=True).stdout; print(o.strip())
        sys.exit(0 if re.search(r"not carried: 0\b|, 0 not carried", o) else 1)
    if kind == "seclinks":
        o = subprocess.run([sys.executable, "-B", os.path.join(H, "sen0401_lineage_research_check_v1_0_0.py"), "seclinks:" + nn], capture_output=True, text=True).stdout; print(o.strip().splitlines()[-1] if o.strip() else "no output")
        sys.exit(0 if "RESULT: PASS" in o else 1)
    if kind == "nochange":
        import datetime
        cs = {"10": ["a52911a"], "11": ["7aaba8d", "2de9dcf"]}[nn]; st = []
        for c in cs:
            st += [l for l in subprocess.run(["git", "show", "--name-status", "--format=", c], cwd=R, capture_output=True, text=True).stdout.splitlines() if l.strip()]
        bad = [l for l in st if not l.startswith("A\t")]
        print("commits %s: %d file(s) added, %d changed or removed %s" % (", ".join(cs), len(st) - len(bad), len(bad), bad[:5])); sys.exit(0 if st and not bad else 1)
    ver = "9_34_0" if kind.endswith("34") or (kind == "erd" and False) else "9_35_0"
    if kind == "erd":
        ver = "9_35_0"
    log, full, n = final_log(nn, ver); feats, skips, w, gates = parse(full)
    out = open(log, encoding="utf-8").read(); ok_exit = "[exit 0," in out
    if kind in ("test34", "test35"):
        fails = [k for k, v in feats.items() if v == "FAIL"]
        print("%s: %d run(s) kept, final %s: exit-0=%s widgets=%s fails=%d" % (ver, n, os.path.basename(log), ok_exit, w, len(fails)))
        sys.exit(0 if ok_exit and w and w[0] == w[1] and not fails else 1)
    if kind in ("counts34", "counts35"):
        sf, st = stored(nn); feats_n = len(feats)
        cnt = lambda x: len(x) if isinstance(x, (list, dict)) else (x or 0)
        sk = cnt(st.get("skipped", 0)); st = {a: cnt(st.get(a)) for a in ("widgets", "features", "gates")}
        print("%s final run: widgets %s, features %d, gates %d, skipped %d | stored %s: widgets %s, features %s, gates %s, skipped %s" % (ver, w, feats_n, gates, len(skips), sf, st["widgets"], st["features"], st["gates"], sk))
        sys.exit(0 if w and w[0] >= st["widgets"] and feats_n >= st["features"] and gates >= st["gates"] and len(skips) <= sk else 1)
    if kind == "erd":
        k = [x for x in feats if "labels mode" in x and "Untangle" in x]; f2 = [x for x in feats if "filled ERD" in x]
        sk = [x for x in skips if "labels mode" in x or "Untangle" in x or "ERD" in x]
        t = open(full, encoding="utf-8", errors="replace").read(); m = re.search(r"labels shown (\d+) -> (\d+)", t)
        ratio = (int(m.group(2)) / int(m.group(1))) if m and int(m.group(1)) else None
        print("9.35.0 ERD label features, final run: on-choice labels mode PASS lines %s; filled ERD PASS lines %s; SKIP lines %s; labels shown after/before %s" % ([feats[x] for x in k], [feats[x] for x in f2], sk, ("%.2f" % ratio) if ratio is not None else "not printed (feature not reached)"))
        sys.exit(0 if k and f2 and all(feats[x] == "PASS" for x in k + f2) and not sk and ratio is not None and ratio >= 0.95 else 1)
    if kind == "abox":
        a = os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_abox_v%s.ttl" % (nn, PV)); b = os.path.join(H, "ch%s-page" % nn, "test_results_abox_v%s.json" % PV)
        print("Stage 4 page ABox %s: %s | stored page-test result %s: %s" % (os.path.relpath(a, R), os.path.exists(a), os.path.relpath(b, R), os.path.exists(b))); sys.exit(0 if os.path.exists(a) and os.path.exists(b) else 1)
    raise SystemExit(__doc__)


main()
