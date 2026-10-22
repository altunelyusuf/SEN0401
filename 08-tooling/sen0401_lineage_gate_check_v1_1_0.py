#!/usr/bin/env python3
"""sen0401_lineage_gate_check v1_1_0 - the exit-code form of the elements of the criterion AC3P_Regression (v1_0_0 holds the elements of AC3P_Template and AC3P_Test and is not edited).
A kind exits 0 only when the element is met as the criterion states it; 1 when not; nothing is skipped. The comparison is written here again from the criterion text, not taken from the executor's comparison tool.
Usage: sen0401_lineage_gate_check_v1_1_0.py KIND[:ARG]
  regress:9_35_1 | regress:9_34_1   the kept run of that test on each of the 14 shipped pages (the newest page of each chapter; chapters 10 and 11: 9.77.0) and on the pages of chapters 1, 8, 12 and 14 rebuilt as 9.80.0: 36 runs in all for the two tests.
                  Per run: the log names that test and that page version, exit 0, RESULT: PASS, widgets tested = passed and not fewer than the stored result, distinct features not fewer, gates not fewer, skipped features
                  not more and each of them one the stored result skips, no [FAIL]. The verdict per page is printed (equal or better); any worse page exits 1.
  rebuilt         the four rebuilt pages: the command record names builder v4_14_0 and template 9.51.1 with PAGE_TEMPLATE, each build log reports the written page, each page of the scratch tree carries the template version 9.51.1, none is in the repository
  nochange:R      the executor's commits since the start of the task add files only, all of them under 08-tooling/page-gates-evidence/regression/; nothing outside it differs from the record before the task; no 9.80.0 page is in the repository tree
  rerun           the control's own runs (08-tooling/verify/iter16/regress): each has exit 0, RESULT: PASS, no [FAIL], and the same widgets, features and skipped features as the executor's run of the same page and test and as the stored result
"""
__version__ = "1.1.0"
import glob, json, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
EVD = os.path.join(H, "page-gates-evidence", "regression"); RER = os.path.join(H, "verify", "iter16", "regress")
SHIPPED = {"01": "9_70_0", "02": "9_71_0", "03": "9_72_0", "04": "9_73_0", "05": "9_74_0", "06": "9_75_0", "07": "9_76_0", "08": "9_77_0", "09": "9_68_0", "10": "9_77_0", "11": "9_77_0", "12": "9_77_0", "13": "9_69_0", "14": "9_77_0"}
REBUILT = {"01": "9_70_0", "08": "9_77_0", "12": "9_77_0", "14": "9_77_0"}      # chapter: the stored result it is compared with
SCRATCH = "/tmp/claude-0/-home-claude/7b499b1c-1b38-5415-81de-45b731a5a6db/scratchpad/scratchrepo"
START = "02bc3a3"
rd = lambda p: open(p, encoding="utf-8", errors="replace").read()


def parse(t):
    feats = {}
    for l in t.splitlines():
        m = re.match(r"\[(PASS|FAIL)\]\s(.*)", l.strip())
        if m: feats[m.group(2)[:140]] = m.group(1)
    skips = {l.strip()[len("[SKIP]"):].strip()[:100] for l in t.splitlines() if l.strip().startswith("[SKIP]")}
    w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    gates = sum(1 for l in t.splitlines() if re.match(r"  (longest main-thread task|Stage4\.[CDEF]|WCAG 2 AA)", l))
    return feats, skips, (int(w.group(1)), int(w.group(2))) if w else None, gates


def stored(nn, pv):
    st = json.load(open(os.path.join(H, "ch%s-page" % nn, "test_results_abox_v%s.json" % pv)))
    return len(st["widgets"]), len(st["features"]), len(st["gates"]), {k[:100] for k in st.get("skipped", {})}


def judge(nn, label, full, summ, test, pv, spv):
    """(verdict, text) for one kept run against the stored result of page spv"""
    sw, sf, sg, ss = stored(nn, spv)
    if not os.path.exists(full) or not os.path.exists(summ): return "MISSING", "%s: log files missing" % label
    t = rd(full); s = rd(summ)
    named = ("page test: sen0401_page_test_v%s.py on page version %s" % (test, pv)) in t + s
    exit0 = "[exit 0]" in s; res = "RESULT: PASS" in s
    feats, skips, w, gates = parse(t); fails = sorted(k for k, v in feats.items() if v == "FAIL")
    ok = named and exit0 and res and w and w[0] == w[1] and w[0] >= sw and len(feats) >= sf and gates >= sg and all(any(x.startswith(k[:60]) for k in ss) for x in skips) and len(skips) <= len(ss) and not fails
    better = ok and (w[0] > sw or len(feats) > sf or len(skips) < len(ss))
    txt = "%s widgets %s/%s features %d/%s gates %d/%s skipped %d/%d%s" % (label, w[0] if w else None, sw, len(feats), sf, gates, sg, len(skips), len(ss), "" if ok else " [named %s exit0 %s PASS %s fails %s]" % (named, exit0, res, fails[:2]))
    return ("better" if better else "equal") if ok else "WORSE", txt


def regress(test):
    rows = []; bad = 0
    for nn, pv in sorted(SHIPPED.items()):
        newest = sorted(glob.glob(os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v*.html" % nn)), key=lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()])
        nv = "_".join(re.search(r"_v(\d+)_(\d+)_(\d+)\.", newest[-1]).groups()) if newest else None
        if nn not in ("10", "11") and nv != pv: rows.append("ch%s: the newest shipped page is %s, the run is on %s" % (nn, nv, pv)); bad += 1; continue
        b = os.path.join(EVD, "R16_%s_ch%s_%s" % (test, nn, pv)); v, txt = judge(nn, "ch%s %s" % (nn, pv.replace("_", ".")), b + ".full.log", b + ".summary.log", test, pv, pv)
        rows.append("%s %s" % (v, txt)); bad += v not in ("equal", "better")
    for nn, spv in sorted(REBUILT.items()):
        b = os.path.join(EVD, "R16_%s_ch%s_9_80_0" % (test, nn)); v, txt = judge(nn, "ch%s 9.80.0 (rebuilt, stored %s)" % (nn, spv.replace("_", ".")), b + ".full.log", b + ".summary.log", test, "9_80_0", spv)
        rows.append("%s %s" % (v, txt)); bad += v not in ("equal", "better")
    print("test %s: %d runs checked, %d not equal or better:\n  %s" % (test, len(rows), bad, "\n  ".join(rows))); return 1 if bad or len(rows) != 18 else 0


def rebuilt():
    cmd = rd(os.path.join(EVD, "R16_rebuild_commands.md")); ok = True; out = []
    c1 = "sen0401_page_build_v4_14_0.py" in cmd and "PAGE_TEMPLATE=course_page_template_v9_51_1.html" in cmd and "PAGE_VER=9_80_0" in cmd; ok &= c1
    out.append("command record names builder v4_14_0, template 9.51.1 by PAGE_TEMPLATE and PAGE_VER 9_80_0: %s" % c1)
    for nn in REBUILT:
        lg = os.path.join(EVD, "R16_build_ch%s_9_80_0_template_9_51_1.log" % nn); w = os.path.exists(lg) and rd(lg).lstrip().startswith("written ") and ("sen0401_ch%s_page_v9_80_0.html" % nn) in rd(lg)[:400]
        pg = os.path.join(SCRATCH, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v9_80_0.html" % nn); has = os.path.exists(pg) and "9.51.1" in open(pg, encoding="utf-8", errors="replace").read(2000)
        ship = os.path.exists(os.path.join(R, "03-materials", "ch" + nn, "page", "sen0401_ch%s_page_v9_80_0.html" % nn))
        out.append("ch%s: build log reports the written page %s; scratch page carries 9.51.1 %s; page in the repository %s" % (nn, w, has, ship)); ok &= bool(w and has and not ship)
    print("; ".join(out)); return 0 if ok else 1


def git(*a): return subprocess.run(["git"] + list(a), cwd=R, capture_output=True, text=True).stdout


def nochange():
    """Files that existed before the task are never edited, a gate, a test, a template, a stored result or a page is untouched, and the task adds files under its folder only. An output of the task itself that was
    appended to after its own commit is printed as a deviation: the criterion stops the task only for an edit beyond the named new files, but it also says every output is a new file."""
    commits = [c for c in git("rev-list", "--reverse", START + "..HEAD").split()]; st = []
    for c in commits: st += [l for l in git("show", "--name-status", "--format=", c).splitlines() if l.strip()]
    before = set(git("ls-tree", "-r", "--name-only", START).split())
    bad = [l for l in st if l.split("\t", 1)[1] in before or "08-tooling/page-gates-evidence/regression/" not in l]
    own = sorted({l.split("\t", 1)[1] for l in st if not l.startswith("A\t") and l.split("\t", 1)[1] not in before})
    other = [l for l in git("diff", "--name-status", START, "HEAD").splitlines() if "08-tooling/page-gates-evidence/regression/" not in l]
    tree = [l for l in git("ls-files").splitlines() if re.search(r"_page_v9_80_0\.html$", l)]
    print("%d commits since %s: %d change(s) in the regression folder, %d touching a file that existed before the task or lying outside the folder %s; differing outside the folder: %s; 9.80.0 pages in the tree: %s; "
          "DEVIATION, own output edited after its commit (disclosed, not hidden): %s" % (len(commits), START, len(st), len(bad), bad[:3], other[:3], tree, own))
    return 0 if commits and st and not bad and not other and not tree else 1


def rerun():
    logs = sorted(glob.glob(os.path.join(RER, "ch*", "page_test_*_rerun.full.log"))); bad = 0; out = []
    if not logs: print("no rerun logs"); return 1
    for f in logs:
        m = re.search(r"ch(\d\d)[/\\]page_test_(9_3[45]_1)_(\d+_\d+_\d+)_rerun", f); nn, test, pv = m.groups(); summ = f.replace(".full.log", ".log"); built = pv == "9_80_0"
        spv = REBUILT.get(nn) if built else pv; v, txt = judge(nn, "ch%s %s %s" % (nn, test, pv.replace("_", ".")), f, summ, test, pv, spv)
        e = os.path.join(EVD, "R16_%s_ch%s_%s" % (test, nn, pv)); ef, es, ew, eg = parse(rd(e + ".full.log")); rf, rs, rw, rg = parse(rd(f))
        same = (ew, len(ef), es, eg) == (rw, len(rf), rs, rg)
        out.append("%s %s; equal to the executor's run (widgets, features, skipped, gates): %s" % (v, txt, same)); bad += (v not in ("equal", "better")) + (not same)
    print("%d rerun(s):\n  %s" % (len(logs), "\n  ".join(out))); return 1 if bad else 0


def main():
    kind, _, arg = sys.argv[1].partition(":")
    sys.exit({"regress": lambda: regress(arg), "rebuilt": rebuilt, "nochange": nochange, "rerun": rerun}.get(kind, lambda: sys.exit(__doc__))())


main()
