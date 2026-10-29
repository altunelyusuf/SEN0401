#!/usr/bin/env python3
"""sen0401_answersheet_control_check v1_0_0 - the lineage agent's OWN control checks of TK_Exam_AnswerMethods_Build. They share no code with the executor's checker; the measurement is called only to re-run it on seeds the executor did not use.
Usage: KIND [COMMIT]   KIND: rerun | digit | sheets | c6 | faint | cost | nochange COMMIT.  Exit 0 only when met. `c6` applies the executor's C6 criteria as written in its checker to the committed seeds AND three held-out seed blocks; `faint` is the control's own element (not an executor criterion)."""
import collections, json, math, os, re, shutil, statistics, subprocess, sys, tempfile
R = "/home/claude/sen0401/"; X = R + "08-tooling/exam/"; sys.path.insert(0, X); sys.dont_write_bytecode = True
def rerun():
    r = subprocess.run([sys.executable, "-B", X + "sen0401_exam_answersheet_check_v1_0_0.py"], capture_output=True, text=True, cwd=R); out = r.stdout
    log = open(X + "sen0401_exam_answersheet_check_log_v1_0_0.txt").read()
    keys = lambda s: [l for l in s.splitlines() if l.startswith(("PASS", "FAIL", "SUMMARY"))]
    fails = [l.split()[1] for l in out.splitlines() if l.startswith("FAIL")]
    same = [re.sub(r"\s+", " ", l) for l in keys(out)] == [re.sub(r"\s+", " ", l) for l in keys(log)]
    num = lambda s: re.findall(r'"silent_wrong": \d+|"empty_not_flagged": \d+|held for a person \d+ \([\d.]+ percent\)', s)
    print("executor's check re-run by the control: exit %d, failing checks %s, summary %s; the PASS/FAIL lines equal the committed log: %s; measured numbers equal: %s %s" % (r.returncode, fails, [l for l in out.splitlines() if l.startswith("SUMMARY")], same, num(out) == num(log), num(out)[:6]))
    return r.returncode == 1 and fails == ["C6"] and same
def damm_ok():
    T = [[0,3,1,7,5,9,8,6,4,2],[7,0,9,2,1,5,4,8,6,3],[4,2,0,6,8,7,1,3,5,9],[1,7,5,0,9,8,3,4,2,6],[6,1,2,3,0,4,5,9,7,8],[3,6,7,4,2,0,9,5,8,1],[5,8,6,9,7,2,0,1,3,4],[8,9,4,5,3,6,2,0,1,7],[9,4,3,8,6,1,7,2,0,5],[2,5,8,1,4,3,6,7,9,0]]
    def valid(code):
        i = 0
        for ch in code: i = T[i][int(ch)]
        return i == 0
    return valid
def digit():
    valid = damm_ok(); import sen0401_exam_answersheet_v1_0_0 as A
    tot = {}; ok = True
    for L in (2, 3, 4):
        miss = n = 0; allvalid = True
        for serial in range(10 ** (L - 1)):
            code = A.make_code(serial, L - 1); allvalid &= valid(code)
            for i in range(L):
                for d in "0123456789":
                    if d != code[i]: n += 1; miss += valid(code[:i] + d + code[i + 1:])
            for i in range(L - 1):
                if code[i] != code[i + 1]: n += 1; miss += valid(code[:i] + code[i + 1] + code[i] + code[i + 2:])
        tot[L] = (n, miss, allvalid); ok &= miss == 0 and allvalid
    print("control's own Damm table: every printed code of 2 to 4 digits valid, and slips plus adjacent swaps tried / undetected: %s" % tot); return ok
def sheets():
    ok = True
    for nm in ("midterm", "makeup"):
        pdf = X + "sen0401_exam_answersheet_%s_v1_0_0.pdf" % nm; lay = json.load(open(X + "sen0401_exam_answersheet_%s_v1_0_0_layout.json" % nm))
        pg = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1)); pw, ph = lay["page_pt"]
        pts = [(b["page"], cx, r["cy"]) for b in lay["blocks"] for u in b["units"] for r in u["rows"] for cx in r["cx"]]
        gap = min(math.hypot(a[1] - b[1], a[2] - b[2]) for i, a in enumerate(pts) for b in pts[i + 1:] if a[0] == b[0]); rr = lay["bubble_r"]
        inside = all(rr + 20 <= x <= pw - rr - 20 and rr + 20 <= y <= ph - rr - 20 for _, x, y in pts)
        bb = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True).stdout
        hs = [float(m.group(2)) - float(m.group(1)) for m in re.finditer(r'yMin="([\d.]+)" xMax="[\d.]+" yMax="([\d.]+)"', bb)]
        tmp = tempfile.mkdtemp(prefix="ascs_", dir="/tmp/claude-0/s"); subprocess.run(["pdftoppm", "-r", "50", "-png", pdf, tmp + "/p"], capture_output=True)
        from PIL import Image
        import numpy as np
        im = np.asarray(Image.open(tmp + "/p-1.png").convert("RGB")).astype(int); colour = int((np.abs(im[..., 0] - im[..., 1]).max() + np.abs(im[..., 1] - im[..., 2]).max()) > 12); white = bool(im[2, 2].min() > 250); shutil.rmtree(tmp, ignore_errors=True)
        raster = "Image" in subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True).stdout.split("\n", 2)[-1]
        print("%s sheet: pages %d, %d bubbles, smallest gap between centres %.1f pt, all inside a 20 pt margin %s, smallest text box %.1f pt, coloured pixels %s, white page %s, raster images %s" % (nm, pg, len(pts), gap, inside, min(hs), bool(colour), white, raster))
        ok &= pg == 1 and gap >= 14 and inside and min(hs) >= 8.9 and not colour and white and not raster
    return ok
def blocks():
    import sen0401_exam_answersheet_measure_v1_0_0 as MS
    return [(sb, MS.run(200, sb, samples=None)) for sb in (9000, 30000, 40000, 50000)]
def c6():
    """The executor's C6 criteria exactly as fixed before its run (read from its checker): no registration failure; no silent wrong answer; no missed ambiguous row; every slip and swap detected; the reader without the methods does worse; held share at most 25 percent."""
    ok = True
    for sb, r in blocks():
        w = r["with_methods"]; n = r["naive_reader"]; pk = r["per_kind_with_methods"]; held = 100 * r["recoverable_rows_held_by_a_flag"] / r["recoverable_rows"]; slip = pk.get("code_slip", {}); swap = pk.get("code_swap", {})
        crit = {"no registration failure": r["registration_failures"] == 0, "no silent wrong answer": w.get("silent_wrong", 0) == 0, "no missed ambiguous row": w.get("missed", 0) == 0, "every code slip detected": slip.get("detected", 0) == sum(slip.values()), "every code swap detected": swap.get("detected", 0) == sum(swap.values()),
                "the reader without the methods does worse": n.get("silent_wrong", 0) + n.get("missed", 0) > 0, "held share at most 25 percent": held <= 25}
        bad = [k for k, v in crit.items() if not v]; ok &= not bad
        print("seed block %d%s: %d rows, silent wrong %d, missed %d, naive silent wrong %d and missed %d, held %.1f percent; C6 criteria not met: %s" % (sb, " (the executor's evaluation block)" if sb == 9000 else " (held out, not used by the executor)", r["rows_scored"], w.get("silent_wrong", 0), w.get("missed", 0), n.get("silent_wrong", 0), n.get("missed", 0), held, bad))
    return ok
def faint():
    """The control's OWN element, NOT a criterion of the executor: no mark may be read as empty without a flag (a student's answer silently becomes a blank)."""
    ok = True; tot = 0
    for sb, r in blocks():
        e = r["with_methods"].get("empty_not_flagged", 0); tot += e; ok &= e == 0
        print("seed block %d: marks read as empty without a flag %d (by kind %s)" % (sb, e, {k: v["empty_not_flagged"] for k, v in r["per_kind_with_methods"].items() if v.get("empty_not_flagged")}))
    print("in all four blocks: %d" % tot); return ok
def cost():
    m = json.load(open(X + "sen0401_exam_pagesave_measure_v1_0_0.json")); log = open(X + "sen0401_exam_answersheet_check_log_v1_0_0.txt").read()
    ok = "5 with the sheet" in log and "4 pages without a sheet" in log and m["pages_baseline"] == 9
    print("the sheet adds one page to the 4-page sample paper (5 with it; 3 sheets of paper printed on both sides against 2): %s" % ok); return ok
def nochange(c):
    st = [l for l in subprocess.run(["git", "-C", R, "show", "--name-status", "--format=", c], capture_output=True, text=True).stdout.split("\n") if l]
    notnew = [l for l in st if not l.startswith("A\t")]; out = [l for l in st if not l.split("\t")[1].startswith("08-tooling/exam/")]
    print("commit %s: %d files, all added: %s; all under 08-tooling/exam/: %s" % (c, len(st), not notnew, not out)); return bool(st) and not notnew and not out
k = sys.argv[1]; ok = {"rerun": rerun, "digit": digit, "sheets": sheets, "c6": c6, "faint": faint, "cost": cost, "nochange": lambda: nochange(sys.argv[2])}[k]()
print("RESULT", "MET" if ok else "NOT MET"); sys.exit(0 if ok else 1)
