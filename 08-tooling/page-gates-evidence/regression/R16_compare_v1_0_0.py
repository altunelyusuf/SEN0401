#!/usr/bin/env python3
"""R16 regression comparison (task TK_PageGates_Regression): new page-test logs against the stored test_results_abox of the page.
Counts as the page check wrapper v1.1.0 counts them: widgets, unique feature lines, gates lines, skipped lines. Usage: R16_compare_v1_0_0.py TESTVER(9_35_1) [TAG]"""
import glob, json, os, re, sys
H = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, H)
def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\[(PASS|FAIL)\]\s(.*)", l.strip())
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = sorted({l.strip()[:150] for l in t.splitlines() if l.strip().startswith("[SKIP]")})
    w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    gates = sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, gates
cnt = lambda x: len(x) if isinstance(x, (list, dict)) else (x or 0)
T = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else ""
D = os.path.dirname(os.path.abspath(__file__))
rows = []
for f in sorted(glob.glob(os.path.join(D, "R16_%s_ch*%s.done" % (T, tag)))):
    b = f[:-5]; m = re.search(r"_ch(\d\d)_(\d+_\d+_\d+)" + tag + "$", b); nn, pv = m.group(1), m.group(2)
    runs = sorted(glob.glob(b + "*.full.log")); full = [r for r in runs if "_retry" not in r.replace(b, "", 1)] and runs
    last = sorted(runs, key=lambda p: (len(p), p))[-1]
    feats, skips, w, gates = parse(open(last, encoding="utf-8", errors="replace").read())
    st = json.load(open(os.path.join(H, "ch%s-page" % nn, "test_results_abox_v%s.json" % pv.replace("_9", "_9") if False else "test_results_abox_v%s.json" % pv)))
    S = dict(w=cnt(st.get("widgets")), f=cnt(st.get("features")), g=cnt(st.get("gates")), s=cnt(st.get("skipped", 0)))
    fails = sorted(k for k, v in feats.items() if v == "FAIL")
    ok = w and w[0] >= S["w"] and len(feats) >= S["f"] and gates >= S["g"] and len(skips) <= S["s"] and not fails and w[0] == w[1]
    better = ok and (w[0] > S["w"] or len(feats) > S["f"] or len(skips) < S["s"])
    rows.append((nn, pv, S, (w, len(feats), len(fails), len(skips), gates), len(runs), "better" if better else "equal" if ok else "WORSE", fails))
print("| page | stored widgets/features/failed/skipped/gates | new run widgets/features/failed/skipped/gates | runs kept | verdict |\n|---|---|---|---|---|")
for nn, pv, S, N, nr, v, fl in rows:
    print("| ch%s %s | %d/%d/0/%d/%d | %s/%d/%d/%d/%d | %d | %s |" % (nn, pv.replace("_", "."), S["w"], S["f"], S["s"], S["g"], N[0][0] if N[0] else None, N[1], N[2], N[3], N[4], nr, v))
    for x in fl: print("    FAIL:", x)
