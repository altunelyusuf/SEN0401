#!/usr/bin/env python3
"""sen0401_lineage_page_check v1_5_0 (over v1_4_1; adds the charset kind and reads the runs of page 9_83_0 in verify/iter19/pages; v1_4_0 over v1_2_0, which is hard-coded to chapter 10 page 9_79_0; v1_3_0 takes the page version and reads the builder's own runs in 08-tooling/verify/iter17/pages; written for the control of Iter_17 and Iter_18, never run by an executor).
Prints what it found and exits 0 ONLY when the element is met as the criterion states it; 1 when it is not met, including when it is skipped or not measured (a skip is not a pass).
Usage: sen0401_lineage_page_check_v1_4_1.py KIND:NN:PV[:ARG]    PV like 9_80_0
  test:NN:PV:VER      the run of page test VER (9_36_0, 9_35_1, 9_34_1) on the page exited 0, every widget passed, no [FAIL] line (the runner's own line and the full log)
  chip:NN:PV          the feature 'a story chip on a concept opens that story in the Stories tab' is PASS in the runs of 9.36.0 and 9.35.1 and 9.34.1 (a FAIL, SKIP or missing line is not met)
  p36:NN:PV           the added features P1 P2 P3 P4 P5 P6 P8 P9 P11 of 9.36.0 all report PASS, none SKIP, none FAIL
  counts:NN:PV:VER    the run's widgets, features and gates are at least, and its skipped checks at most, the stored result of the earlier page (ARG2 = its version, default the newest before PV)
  deck / link:NN:PV   pages_deck_match_verify / pages_link_verify report 0 not carried
  abox:NN:PV          the Stage 4 page ABox and the stored page-test result of the page exist as new files
  charset:NN:PV       the page charset check v1_0_0 exits 0 on the page, the tag occurs once below byte 1024 and the page embeds template 9.52.2 (version marker)
  nochange:NN:SHAS    every file of the commits (comma list) has git status A (a modified or removed file is named)"""
__version__ = "1.5.0"
import glob, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); LOG17 = os.path.join(H, "verify", "iter17", "pages"); LOG18 = os.path.join(H, "verify", "iter18", "pages"); LOG19 = os.path.join(H, "verify", "iter19", "pages")
CHIP = "a story chip on a concept opens that story in the Stories tab"
LOG = None
def full(nn, pv, ver): return open(os.path.join(LOG, "ch%s_page_%s_test_%s.full.log" % (nn, pv, ver)), encoding="utf-8", errors="replace").read()
def runner(nn, pv, ver): return open(os.path.join(LOG, "ch%s_page_%s_test_%s.runner.txt" % (nn, pv, ver)), encoding="utf-8", errors="replace").read()
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\s*\[(PASS|FAIL)\]\s(.*)", l)
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = sorted({l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")})
    w = re.search(r"widgets: (\d+) tested, (\d+) passed", t); gates = sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, gates
def main():
    global LOG
    a = sys.argv[1].split(":"); kind, nn, pv = a[0], a[1], a[2] if len(a) > 2 else ""; LOG = LOG19 if pv == "9_83_0" else (LOG18 if pv == "9_82_0" else LOG17)
    if kind == "test":
        ver = a[3]; t = full(nn, pv, ver); r = runner(nn, pv, ver); feats, skips, w, gates = parse(t); fails = [k for k, v in feats.items() if v == "FAIL"]; line = ([l for l in r.splitlines() if l.startswith("page ")] or [""])[-1]
        print("%s on page %s: %s | widgets %s | %d failed feature(s) %s" % (ver, pv, line, w, len(fails), [f[:90] for f in fails][:3])); sys.exit(0 if "exit 0" in line and w and w[0] == w[1] and not fails and "RESULT: PASS" in r else 1)
    if kind == "chip":
        res = {}
        for ver in ("9_36_0", "9_35_1", "9_34_1"):
            feats, skips, w, g = parse(full(nn, pv, ver)); res[ver] = [v for k, v in feats.items() if k.startswith(CHIP[:40])] or ["missing"]
        print("story chip feature by test: %s" % res); sys.exit(0 if all(v and all(x == "PASS" for x in v) for v in res.values()) else 1)
    if kind == "p36":
        t = full(nn, pv, "9_36_0"); feats, skips, w, g = parse(t); P = {k: v for k, v in feats.items() if re.match(r"P\d+ ", k)}; sk = [s for s in skips if re.search(r"\] P\d+ ", s)]
        bad = {k[:60]: v for k, v in P.items() if v != "PASS"}; print("9.36.0 added features: %d PASS lines of %d, FAIL/other %s, SKIP %d" % (sum(v == "PASS" for v in P.values()), len(P), bad, len(sk))); sys.exit(0 if P and not bad and not sk and len({k[:3] for k in P}) >= 9 else 1)
    if kind == "counts":
        ver = a[3]; feats, skips, w, gates = parse(full(nn, pv, ver)); old = a[4] if len(a) > 4 else None
        fs = glob.glob(os.path.join(H, "ch%s-page" % nn, "test_results_abox_v*.json")); key = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
        cur = [int(x) for x in pv.split("_")]; fs = [f for f in fs if (key(f) < cur if not old else key(f) == [int(x) for x in old.split("_")])]; f = sorted(fs, key=key)[-1]; st = json.load(open(f)); cnt = lambda x: len(x) if isinstance(x, (list, dict)) else (x or 0)
        s = {k: cnt(st.get(k)) for k in ("widgets", "features", "gates")}; sk = cnt(st.get("skipped", 0))
        print("%s run: widgets %s, features %d, gates %d, skipped %d | stored %s: widgets %s, features %s, gates %s, skipped %s" % (ver, w, len(feats), gates, len(skips), os.path.basename(f), s["widgets"], s["features"], s["gates"], sk))
        sys.exit(0 if w and w[0] >= s["widgets"] and len(feats) >= s["features"] and gates >= s["gates"] and len(skips) <= sk else 1)
    if kind in ("deck", "link"):
        tool = "pages_deck_match_verify_v1_0_0.py" if kind == "deck" else "pages_link_verify_v1_0_0.py"
        o = subprocess.run([sys.executable, "-B", os.path.join(H, tool), nn, pv], capture_output=True, text=True).stdout; print(o.strip()[-300:]); sys.exit(0 if re.search(r"not carried: 0\b|, 0 not carried|0 not carried", o) else 1)
    if kind == "abox":
        x = os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_abox_v%s.ttl" % (nn, pv)); y = os.path.join(H, "ch%s-page" % nn, "test_results_abox_v%s.json" % pv)
        print("Stage 4 page ABox %s: %s | stored page-test result %s: %s" % (os.path.relpath(x, R), os.path.exists(x), os.path.relpath(y, R), os.path.exists(y))); sys.exit(0 if os.path.exists(x) and os.path.exists(y) else 1)
    if kind == "charset":
        pg = os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v%s.html" % (nn, pv)); b = open(pg, "rb").read(); tag = b'<meta charset="utf-8">'
        r = subprocess.run([sys.executable, "-B", os.path.join(H, "sen0401_page_charset_check_v1_0_0.py"), pg], capture_output=True, text=True); n = b.count(tag); off = b.find(tag); emb = b"course_page_template version 9.52.2" in b
        print("charset check exit %d: %s | tag %d time(s) at byte %d | embeds template 9.52.2: %s" % (r.returncode, (r.stdout + r.stderr).strip()[-160:], n, off, emb)); sys.exit(0 if r.returncode == 0 and n == 1 and 0 <= off < 1024 and emb else 1)
    if kind == "nochange":
        cs = a[2].split(","); st = []
        for c in cs: st += [(c, l) for l in subprocess.run(["git", "show", "--name-status", "--format=", c], cwd=R, capture_output=True, text=True).stdout.splitlines() if l.strip()]
        bad = [c + " " + l for c, l in st if not l.startswith("A\t")]; print("commits %s: %d file(s) added, %d modified or removed %s" % (",".join(cs), len(st) - len(bad), len(bad), bad[:5])); sys.exit(0 if st and not bad else 1)
    raise SystemExit(__doc__)
main()
