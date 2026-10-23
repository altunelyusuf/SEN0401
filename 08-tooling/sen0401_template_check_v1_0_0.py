#!/usr/bin/env python3
"""sen0401_template_check v1.0.0 - the control's own checks of TK_Repair_Template (page template 9.52.1; criterion AC5R_Template). A NEW tool; it edits no committed file.
Usage: sen0401_template_check_v1_0_0.py run:sc:NN | KIND
  run:sc:05|01|10   builds the data and the page of the chapter on template 9.52.1 (PAGE_TEMPLATE) into a scratch folder with builders v4_15_0 and v2_24_0 (chapter 10 with the executor's committed fixture manifest) and runs the page tests
                    (chapter 5: 9.36.0 then 9.35.1; chapters 1 and 10: 9.36.0), serially; logs in 08-tooling/verify/iter18/template
  ident             9.52.0 is committed once and unchanged (clean against HEAD); 9.52.1 is a new file whose SHA-256 equals the executor's recorded one
  diff              the diff of 9.52.1 over 9.52.0 is exactly two changed lines: the version comment and the line holding the story-chip click handler (the replaced text of that line contains data-story); every id and data- hook of 9.52.0 is in 9.52.1
  chip:05           the scratch page of chapter 5 embeds 9.52.1; the story chip feature is PASS for the story GoxColdFind in the runs of 9.36.0 and 9.35.1, no [FAIL] line, both runs exit 0
  pf:NN             the scratch page of chapter NN (01 or 10) on 9.52.1: page test 9.36.0 exits 0, no [FAIL], P1 P3 P4 P5 P6 P8 P9 PASS
  nochange:SHAS     every file of the commits (comma list) has git status A
Exit 0 only when the check holds. Results are printed."""
__version__ = "1.0.0"
import difflib, os, re, subprocess, sys, hashlib
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H); T = "/tmp/claude-0/s/tp18"; LOG = os.path.join(H, "verify", "iter18", "template"); VENV = "/home/claude/venv314/bin/python"
TP0 = os.path.join(H, "course_page_template_v9_52_0.html"); TP1 = os.path.join(H, "course_page_template_v9_52_1.html"); CHIP = "a story chip on a concept opens that story in the Stories tab"
def sh(*a, **k): return subprocess.run(list(a), capture_output=True, text=True, **k)
def say(ok, msg): print("%s %s" % ("PASS" if ok else "FAIL", msg)); sys.exit(0 if ok else 1)
def scratch(nn):
    out = os.path.join(T, "out" + nn); sc = os.path.join(T, "repo" + nn); os.makedirs(out, exist_ok=True); os.makedirs(LOG, exist_ok=True)
    env = dict(os.environ, PAGE_VER="9_91_0", PAGE_DATA_OUT=out, PAGE_DATA_DIR=out, PAGE_SCRATCH=out, PAGE_TEMPLATE="course_page_template_v9_52_1.html")
    if nn == "10": env["CC_MANIFEST"] = os.path.join(H, "template952_logs", "SCRATCH_FIXTURE_chapter_code_ch10_not_a_deck_manifest.json")
    for a in ([VENV, "sen0401_page_data_v2_24_0.py", nn, VENV], [VENV, "sen0401_page_build_v4_15_0.py", nn]):
        r = subprocess.run(a, capture_output=True, text=True, env=env, cwd=H, timeout=900); open(os.path.join(LOG, "build_%s_%s.log" % (nn, a[1][-14:-3])), "w").write(r.stdout + r.stderr)
        if r.returncode: print("build failed", a[1], r.stderr[-400:]); sys.exit(2)
    mk = os.path.join(T, "mkscratch.sh"); open(mk, "w").write(open("/tmp/claude-0/s17/mkscratch.sh").read().replace("S=/tmp/claude-0/s17/repo$NN", "S=%s/repo$NN" % T))
    r = subprocess.run(["sh", mk, nn, "9_91_0", out] + ([env["CC_MANIFEST"]] if nn == "10" else []), capture_output=True, text=True); print(r.stdout.strip()[-200:], r.stderr[-200:]); return sc
def runtest(tag, n, env, repo, test):
    full = os.path.join(LOG, tag + ".full.log"); runner = os.path.join(LOG, tag + ".runner.txt")
    e = dict(os.environ, PAGE_TEST=test, FULL_LOG=full, **env)
    r = subprocess.run([sys.executable, "-B", os.path.join(repo, "08-tooling", "sen0401_lineage_page_test_run_v1_2_0.py"), n, "9_91_0"], capture_output=True, text=True, env=e, cwd=repo)
    open(runner, "w").write(r.stdout + r.stderr); print("run %s: exit %d" % (tag, r.returncode))
def rd(tag, k): return open(os.path.join(LOG, "%s.%s.txt" % (tag, k) if k == "runner" else "%s.full.log" % tag), encoding="utf-8", errors="replace").read()
def ex(tag):
    t = rd(tag, "full"); r = rd(tag, "runner"); m = re.search(r"exit (\d+)", [l for l in r.splitlines() if l.startswith("page ")][-1] if any(l.startswith("page ") for l in r.splitlines()) else ""); w = re.search(r"widgets: (\d+) tested, (\d+) passed", t)
    fails = [l.strip()[:200] for l in t.splitlines() if l.strip().startswith("[FAIL]")]; return t, (m.group(1) if m else "?"), (w.groups() if w else None), fails
def main():
    a = sys.argv[1]
    if a.startswith("run:"):
        k = a[4:].split(":"); nn = k[1]; sc = scratch(nn)
        for ver in (["9_36_0", "9_35_1"] if nn == "05" else ["9_36_0"]): runtest("sc%s_%s" % (nn, ver), nn, {}, sc, "sen0401_page_test_v%s.py" % ver)
        return
    k = a.split(":")
    if k[0] == "ident":
        n = sh("git", "log", "--format=%h", "--", TP0, cwd=R).stdout.split(); d = sh("git", "diff", "--quiet", "HEAD", "--", TP0, cwd=R).returncode
        rec = dict(reversed(l.split()) for l in open(os.path.join(H, "template952_logs", "I18_template_sha256.txt")) if l.strip()); h1 = hashlib.sha256(open(TP1, "rb").read()).hexdigest(); h0 = hashlib.sha256(open(TP0, "rb").read()).hexdigest()
        c1 = sh("git", "log", "--format=%h", "--", TP1, cwd=R).stdout.split()
        say(len(n) == 1 and d == 0 and rec.get("course_page_template_v9_52_1.html") == h1 and rec.get("course_page_template_v9_52_0.html") == h0 and len(c1) == 1, "9.52.0: %d commit(s), %s, SHA-256 %s equals the recorded; 9.52.1: %d commit(s), SHA-256 %s equals the recorded" % (len(n), "clean against HEAD" if d == 0 else "DIFFERS", h0[:12], len(c1), h1[:12]))
    if k[0] == "diff":
        A = open(TP0, encoding="utf-8").read().splitlines(); B = open(TP1, encoding="utf-8").read().splitlines(); sm = difflib.SequenceMatcher(None, A, B, autojunk=False); ch = [o for o in sm.get_opcodes() if o[0] != "equal"]
        ok = len(ch) == 2 and all(o[0] == "replace" and o[2] - o[1] == 1 and o[4] - o[3] == 1 for o in ch)
        info = []
        if ok:
            ok1 = A[ch[0][1]].startswith("<!-- course_page_template version 9.52.0") and B[ch[0][3]].startswith("<!-- course_page_template version 9.52.1")
            cm = difflib.SequenceMatcher(None, A[ch[1][1]], B[ch[1][3]], autojunk=False); sp = [o for o in cm.get_opcodes() if o[0] != "equal"]; old = "".join(A[ch[1][1]][o[1]:o[2]] for o in sp); new = "".join(B[ch[1][3]][o[3]:o[4]] for o in sp)
            ok2 = "data-story" in A[ch[1][1]] and ("scrollIntoView" in new or "requestAnimationFrame" in new); ok = ok1 and ok2; info = ["version line %s" % ok1, "handler line (line %d): %d changed span(s), replaced %d chars by %d chars, scroll code in the new text %s" % (ch[1][1] + 1, len(sp), len(old), len(new), ok2)]
        ids = lambda s: set(re.findall(r'\bid="([^"]+)"', s)) | set(re.findall(r"\b(data-[a-z0-9-]+)", s)); i0 = ids("\n".join(A)); i1 = ids("\n".join(B)); miss = sorted(i0 - i1)
        say(ok and not miss, "9.52.1 over 9.52.0: %d changed hunk(s) %s; %d ids and data- hooks of 9.52.0, %d missing in 9.52.1 %s" % (len(ch), info, len(i0), len(miss), miss[:5]))
    if k[0] == "chip":
        res = {}; okall = True
        for ver in ("9_36_0", "9_35_1"):
            t, code, w, fails = ex("sc05_" + ver); feat = [l.strip() for l in t.splitlines() if l.strip().startswith("[PASS] " + CHIP[:40]) or l.strip().startswith("[FAIL] " + CHIP[:40])]
            res[ver] = (code, w, [f[:110] for f in feat[:1]], len(fails)); okall &= code == "0" and bool(w) and w[0] == w[1] and not fails and bool(feat) and feat[0].startswith("[PASS]") and "GoxColdFind" in t
        page = open(os.path.join(T, "out05", "sen0401_ch05_page_v9_91_0.html"), encoding="utf-8").read(); mine = "course_page_template version 9.52.1" in page
        say(okall and mine, "scratch page of chapter 5 embeds 9.52.1: %s | %s" % (mine, res))
    if k[0] == "pf":
        nn = k[1]; t, code, w, fails = ex("sc%s_9_36_0" % nn); got = {p: bool(re.search(r"\[PASS\] " + p + r"\b", t)) for p in ["P1", "P3", "P4", "P5", "P6", "P8", "P9"]}
        say(code == "0" and w and w[0] == w[1] and not fails and all(got.values()), "scratch page of chapter %s on 9.52.1, page test 9.36.0: exit %s, widgets %s, %d failed feature line(s), %s" % (nn, code, w, len(fails), got))
    if k[0] == "nochange":
        cs = k[1].split(","); st = []
        for c in cs: st += [(c, l) for l in sh("git", "show", "--name-status", "--format=", c, cwd=R).stdout.splitlines() if l.strip()]
        bad = [c + " " + l for c, l in st if not l.startswith("A\t")]; say(not bad, "commits %s: %d file(s) added, %d modified or removed %s" % (",".join(cs), len(st) - len(bad), len(bad), bad[:5]))
    raise SystemExit(__doc__)
main()
