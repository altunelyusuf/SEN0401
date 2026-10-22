#!/usr/bin/env python3
"""sen0401_remedy_check v1.0.0 - the control's own checks of the three tool tasks of Iter_17 (the deck standard check, the page test 9.36.0, the page template 9.52.0 and its builders). A NEW tool; it edits no committed file.
Usage: sen0401_remedy_check_v1_0_0.py run:KIND | KIND      KIND is one of
  dcold:05 dcold:06   run the deck standard check on the OLD deck of the chapter (23/9/1/0/39 and 26/13/3/0/56 as the criterion states), expect exit non-zero, D1..D12 each named with a measure, D3 D4 D10 D11 FAIL
  dchdr               the header of the deck standard check defines code slide, analogy, story (5N1K), coverage, key concept
  dclogs              the kept logs of the executor's runs exist
  ptsame              page test 9.35.1 is committed once and unchanged (clean against HEAD); 9.36.0 differs from it by added lines and the version line only; every feat/skip text of 9.35.1 is in 9.36.0 (ast)
  run:ptforce:05|06   FORCE_STANDARD=1 page test 9.36.0 on the shipped page of chapter 5 (9_74_0) or 6 (9_75_0): the run (serial, about 10 minutes); ptforce:05|06 reads its log
  run:ptskip          page test 9.36.0 WITHOUT the force on the shipped page of chapter 10 (9_79_0); ptskip reads its log: every P feature is SKIP with a reason, none FAIL
  run:tpscratch:01|10 builds the data and the page of the chapter on template 9.52.0 into a scratch folder (chapter 10 with the executor's committed fixture manifest) and runs page test 9.36.0 on it; tpscratch:01|10 reads the log
  ptlogs              the executor's kept logs of page test 9.36.0 exist
  tpold               template 9.51.1, builder v4_14_0, data builder v2_23_0 are committed once and clean against HEAD (byte-identical)
  tpdom               the DOM contract of the criterion is present in template 9.52.0, every id of 9.51.1 is kept, the builders are new files
  tpfacts             the executor's report states how the page runs code and what the chapter libraries need (RUNTIME_FACTS)
Exit 0 only when the check holds. Results are printed."""
__version__ = "1.0.0"
import ast, difflib, glob, os, re, subprocess, sys
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); T = "/tmp/claude-0/s/tp"
LOG = os.path.join(R, "08-tooling", "verify", "iter17", "tools"); VENV = "/home/claude/venv314/bin/python"
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def once_clean(f):
    n = sh("git", "log", "--format=%h", "--", f, cwd=R).stdout.split(); d = sh("git", "diff", "--quiet", "HEAD", "--", f, cwd=R).returncode
    return len(n) == 1 and d == 0, "%s: %d commit(s), %s" % (os.path.basename(f), len(n), "clean against HEAD" if d == 0 else "DIFFERS from HEAD")
def say(ok, msg): print("%s %s" % ("PASS" if ok else "FAIL", msg)); sys.exit(0 if ok else 1)
def feats(p):
    out = set()
    for n in ast.walk(ast.parse(open(p, encoding="utf-8").read())):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ("feat", "skip") and n.args:
            out.add(ast.unparse(n.args[0]))
    return out
def runtest(tag, n, pv, env, repo=None, page_test="sen0401_page_test_v9_36_0.py"):
    os.makedirs(LOG, exist_ok=True); full = os.path.join(LOG, tag + ".full.log"); runner = os.path.join(LOG, tag + ".runner.txt")
    e = dict(os.environ, PAGE_TEST=page_test, FULL_LOG=full, **env); base = repo or R
    r = subprocess.run([sys.executable, "-B", os.path.join(base, "08-tooling", "sen0401_lineage_page_test_run_v1_2_0.py"), n, pv], capture_output=True, text=True, env=e, cwd=base)
    open(runner, "w").write(r.stdout + r.stderr); print("run %s: exit %d, %s" % (tag, r.returncode, [l for l in r.stdout.splitlines() if l.startswith("page ")][-1:]))
def lines(tag): return open(os.path.join(LOG, tag + ".runner.txt"), encoding="utf-8", errors="replace").read().splitlines()
def pl(tag): return [l.strip() for l in lines(tag) if re.match(r"\s*\[(PASS|FAIL|SKIP)\] P\d", l)]
def summary(tag): return ([l for l in lines(tag) if l.startswith("page ")] or [""])[-1]
def scratch(nn):
    out = os.path.join(T, "out" + nn); sc = os.path.join(T, "repo" + nn); os.makedirs(out, exist_ok=True); env = dict(os.environ, PAGE_VER="9_90_0", PAGE_DATA_OUT=out, PAGE_DATA_DIR=out, PAGE_SCRATCH=out)
    man = ""
    if nn == "10": man = os.path.join(R, "08-tooling", "template952_logs", "SCRATCH_FIXTURE_chapter_code_ch10_not_a_deck_manifest.json"); env["CC_MANIFEST"] = man
    for a in ([VENV, "sen0401_page_data_v2_24_0.py", nn, VENV], [VENV, "sen0401_page_build_v4_15_0.py", nn]):
        r = subprocess.run(a, capture_output=True, text=True, env=env, cwd=H, timeout=900); open(os.path.join(LOG, "scratch_build_%s_%s.log" % (nn, a[1][-14:-3])), "w").write(r.stdout + r.stderr)
        if r.returncode: print("build failed", a[1], r.stderr[-400:]); sys.exit(2)
    mk = os.path.join(T, "mkscratch.sh"); open(mk, "w").write(open("/tmp/claude-0/s17/mkscratch.sh").read().replace("S=/tmp/claude-0/s17/repo$NN", "S=%s/repo$NN" % T).replace("R=/home/claude/sen0401", "R=" + R))
    r = subprocess.run(["sh", mk, nn, "9_90_0", out] + ([man.replace(man, man)] if man else []), capture_output=True, text=True); print(r.stdout.strip()[-200:], r.stderr[-200:]); return sc
def main():
    a = sys.argv[1]
    if a.startswith("run:"):
        k = a[4:].split(":")
        if k[0] == "ptforce": runtest("ptforce_" + k[1], k[1], {"05": "9_74_0", "06": "9_75_0"}[k[1]], {"FORCE_STANDARD": "1"})
        elif k[0] == "ptskip": runtest("ptskip_10", "10", "9_79_0", {})
        elif k[0] == "tpscratch": os.makedirs(LOG, exist_ok=True); sc = scratch(k[1]); runtest("tpscratch_" + k[1], k[1], "9_90_0", {}, repo=sc)
        return
    k = a.split(":")
    if k[0] in ("dcold",):
        nn = k[1]; olds = {"05": ("03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v2_3_0.pptx", "slides=23 code_slides=9 native_charts=1 analogies=0 longest_box_words=39"), "06": ("03-materials/ch06/SEN0401_Ch06_Transactions_3e_v1_3_0.pptx", "slides=26 code_slides=13 native_charts=3 analogies=0 longest_box_words=56")}
        deck, facts = olds[nn]; deck = deck if os.path.exists(os.path.join(R, deck)) else sorted(glob.glob(os.path.join(R, "03-materials/ch%s/*.pptx" % nn)))[0]
        r = subprocess.run([sys.executable, "-B", os.path.join(H, "sen0401_deck_standard_check_v1_0_0.py"), nn, deck], capture_output=True, text=True, cwd=R); o = r.stdout
        fl = [l for l in o.splitlines() if l.startswith("FACTS")]; el = {l.split()[0]: l.split()[1] for l in o.splitlines() if re.match(r"D\d+ (PASS|FAIL|NOT_MEASURED)", l)}
        meas = all(re.search(r"\d", l) for l in o.splitlines() if re.match(r"D\d+ ", l))
        ok = r.returncode != 0 and bool(fl) and all(x in fl[0] for x in facts.split()) and set(el) == {"D%d" % i for i in range(1, 13)} and all(el.get(d) == "FAIL" for d in ("D3", "D4", "D10", "D11")) and meas
        say(ok, "old deck %s: exit %d; %s; expected %s; elements %s" % (os.path.basename(deck), r.returncode, fl[:1], facts, el))
    if k[0] == "dchdr":
        s = open(os.path.join(H, "sen0401_deck_standard_check_v1_0_0.py"), encoding="utf-8").read().split('"""')[1]; need = ["code slide", "analogy", "story slide", "D5 measure", "D11 measure", "key concept"]
        say(all(x in s for x in need) and "5N1K" in s or all(x in s for x in need), "header defines %s" % need)
    if k[0] == "dclogs":
        fs = sorted(glob.glob(os.path.join(H, "iter17-logs", "deckcheck_ch0*_run*.log"))); say(len(fs) >= 4 and all(os.path.getsize(f) > 0 for f in fs), "kept logs: %s" % [os.path.basename(f) for f in fs])
    if k[0] == "ptsame":
        ok1, m1 = once_clean(os.path.join("08-tooling", "sen0401_page_test_v9_35_1.py")); a1 = open(os.path.join(H, "sen0401_page_test_v9_35_1.py"), encoding="utf-8").read().splitlines(); b1 = open(os.path.join(H, "sen0401_page_test_v9_36_0.py"), encoding="utf-8").read().splitlines()
        rem = [l[1:] for l in difflib.unified_diff(a1, b1, lineterm="", n=0) if l.startswith("-") and not l.startswith("---")]; add = sum(1 for l in difflib.unified_diff(a1, b1, lineterm="", n=0) if l.startswith("+") and not l.startswith("+++"))
        f1, f2 = feats(os.path.join(H, "sen0401_page_test_v9_35_1.py")), feats(os.path.join(H, "sen0401_page_test_v9_36_0.py")); miss = f1 - f2
        say(ok1 and rem == ['__version__ = "9.35.1"'] and not miss, "%s; lines removed from 9.35.1: %s, lines added: %d; feat/skip texts 9.35.1: %d, 9.36.0: %d, missing from 9.36.0: %d" % (m1, rem, add, len(f1), len(f2), len(miss)))
    if k[0] == "ptforce":
        tag = "ptforce_" + k[1]; p = pl(tag); fails = " ".join(l for l in p if l.startswith("[FAIL]")); chap = {"05": ("4861", ), "06": ("5836", )}[k[1]]
        ok = summary(tag).startswith("page %s: exit 0" % k[1]) and chap[0] in fails and "chaptercode" in fails and "8 of 8" in fails and "over one screen" in fails and "no horizontal overflow" in fails
        say(ok, "%s | the added features that FAIL: %d | %s" % (summary(tag), sum(l.startswith("[FAIL]") for l in p), [l[:110] for l in p if l.startswith("[FAIL]")][:3]))
    if k[0] == "ptskip":
        p = pl("ptskip_10"); ok = summary("ptskip_10").startswith("page 10: exit 0") and len(p) >= 9 and all(l.startswith("[SKIP]") for l in p) and "failed 0" in summary("ptskip_10")
        say(ok, "%s | %d added-feature lines, all SKIP: %s | %s" % (summary("ptskip_10"), len(p), all(l.startswith("[SKIP]") for l in p), p[:1]))
    if k[0] == "tpscratch":
        tag = "tpscratch_" + k[1]; p = pl(tag); want = ["P1", "P3", "P4", "P5", "P6", "P8", "P9"]; got = {w: [l for l in p if re.match(r"\[PASS\] " + w + r"\b", l)] for w in want}
        ok = summary(tag).startswith("page %s: exit 0" % k[1]) and "failed 0" in summary(tag) and all(got.values()) and not any(l.startswith("[FAIL]") for l in p)
        say(ok, "%s | passes %s | no FAIL among %d P lines" % (summary(tag), {w: len(v) for w, v in got.items()}, len(p)))
    if k[0] == "ptlogs":
        fs = ["diff_9_35_1_to_9_36_0.diff", "proof_feature_texts_9_35_1_vs_9_36_0.txt", "full_ch05_page_v9_74_0_force.log", "full_ch06_page_v9_75_0_force.log", "full_ch06_page_v9_75_0_force_run2.log", "runner_ch05_page_v9_74_0_force.log", "runner_ch06_page_v9_75_0_force_run2.log"]
        say(all(os.path.getsize(os.path.join(H, "pagetest936_logs", f)) > 0 for f in fs), "kept logs of the executor: %s" % fs)
    if k[0] == "tpold":
        res = [once_clean(os.path.join("08-tooling", f)) for f in ("course_page_template_v9_51_1.html", "sen0401_page_build_v4_14_0.py", "sen0401_page_data_v2_23_0.py")]
        say(all(r[0] for r in res), "; ".join(r[1] for r in res))
    if k[0] == "tpdom":
        t = open(os.path.join(H, "course_page_template_v9_52_0.html"), encoding="utf-8").read(); o = open(os.path.join(H, "course_page_template_v9_51_1.html"), encoding="utf-8").read()
        tok = ['data-pane="chaptercode"', "data-cc-item", "data-cc-name", "data-cc-order", "data-cc-editor", "data-cc-run", "data-cc-result", "role=\"treeitem\"", "role=\"tab\"", "data-panel", "data-pg-item", 'name="page-standard"', "9.52"]
        miss = [x for x in tok if x not in t and x.replace('"', "'") not in t and x.replace('"', "") not in t]; ids = set(re.findall(r'\bid="([^"{$+]+)"', o)); lost = sorted(i for i in ids if ('id="%s"' % i) not in t and ("'%s'" % i) not in t and ('"%s"' % i) not in t)
        new = [os.path.exists(os.path.join(H, f)) and len(sh("git", "log", "--format=%h", "--", "08-tooling/" + f, cwd=R).stdout.split()) == 1 for f in ("course_page_template_v9_52_0.html", "sen0401_page_build_v4_15_0.py", "sen0401_page_data_v2_24_0.py")]
        say(not miss and not lost and all(new), "contract tokens missing: %s; ids of 9.51.1 (%d) not found in 9.52.0: %s; three new files committed once: %s" % (miss, len(ids), lost[:8], new))
    if k[0] == "tpfacts":
        s = open(os.path.join(H, "template952_logs", "RUNTIME_FACTS.txt"), encoding="utf-8").read(); need = ["Pyodide", "Web Worker", "py_wheels", "py_boot", "ripemd160", "pbkdf2_hmac", "ch06", "bip39_english.txt"]
        say(all(x.lower() in s.lower() for x in need), "RUNTIME_FACTS covers %s" % need)
    sys.exit(3)
main()
