#!/usr/bin/env python3
"""sen0401_engine_control_check v1_0_0 - the lineage agent's OWN control checks of TK_Exam_Engine_Build. They share no code with the executor's check.
Usage: KIND [COMMIT]   KIND: rerun | builds | answers | param | refuse | pdf | nochange COMMIT. Exit 0 only when met.
The control builds with its own seeds and sizes (not the executor's) into its own folder under /tmp/claude-0/s/en and removes it."""
import collections, glob, json, os, re, shutil, subprocess, sys
R = "/home/claude/sen0401/"; X = R + "08-tooling/exam/"; ENG = X + "sen0401_exam_engine_v1_0_0.py"; W = "/tmp/claude-0/s/en/ctl"
LV = {"Remember": 1, "Understand": 2, "Apply": 3, "Analyze": 4}
def build(name, *a):
    d = "%s/%s" % (W, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    r = subprocess.run(["python3", "-B", ENG, "build", "--outdir", d] + list(a), capture_output=True, text=True, cwd=R); return r, d
def keys(d, p): return json.load(open("%s/sen0401_exam_%s_v1_0_0_key.json" % (d, p)))
def rerun():
    r = subprocess.run(["python3", "-B", X + "sen0401_exam_engine_check_v1_0_0.py"], capture_output=True, text=True, cwd=R, env=dict(os.environ, SEN0401_ENGINE_TMP="/tmp/claude-0/s/en"))
    mine = [l[:70] for l in r.stdout.splitlines() if l[:5] in ("PASS ", "FAIL ")]; theirs = [l[:70] for l in open(X + "sen0401_exam_engine_check_log_v1_0_0.txt").read().splitlines() if l[:5] in ("PASS ", "FAIL ")]
    print("executor's check re-run: exit %d; %d PASS/FAIL lines; equal to the committed log lines: %s; %s" % (r.returncode, len(mine), mine == theirs, [l for l in r.stdout.splitlines() if l.startswith("SUMMARY")]))
    return r.returncode == 0 and mine == theirs and len(mine) == 11
def builds():
    ok = True
    for name, a in (("s1", ["--items", "20", "--seed", "11"]), ("s2", ["--items", "30", "--seed", "12", "--chapters", "1-6"]), ("s3", ["--items", "18", "--seed", "11"])):
        r, d = build(name, *a); r2, d2 = build(name + "b", *a)
        if r.returncode:
            print(name, "build exit", r.returncode, r.stdout[-200:], r.stderr[-300:]); ok = False; continue
        same = all(keys(d, p) == keys(d2, p) for p in ("midterm", "makeup")); n = int(a[1])
        m, k = keys(d, "midterm"), keys(d, "makeup"); both = {i["item_key"] for i in m["items"]} & {i["item_key"] for i in k["items"]}
        lets = collections.Counter(i["answer"] for i in m["items"] if i["type"].startswith("ChoiceFour")); spread = max(lets.values()) - min(lets.values()) if lets else 0
        hi = sum(i["bloom"] >= 3 for i in m["items"]); per = collections.Counter(i["chapters"][0] for i in m["items"]); chs = sorted(per)
        print("%s items %d: same seed gives same keys %s; midterm %d and make-up %d items; shared items %d; answer letters %s (spread %d); Bloom 3+ %d of %d; items per primary chapter %s" % (name, n, same, len(m["items"]), len(k["items"]), len(both), dict(sorted(lets.items())), spread, hi, n, dict(sorted(per.items()))))
        ok &= same and len(m["items"]) == n == len(k["items"]) and not both and spread <= 2 and hi * 2 > n and chs == [1, 2, 3, 4, 5, 6]
    return ok
def answers():
    bad = []; tot = 0
    banks = {}
    for n in range(1, 8):
        fs = sorted(glob.glob(R + "08-tooling/ch%02d-page/question_bank_v*.json" % n), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")]); banks[n] = json.load(open(fs[-1], encoding="utf8"))
    from rdflib import Graph, Namespace
    P = Namespace("http://example.org/sen0401/paperrules#")
    r, d = build("ans", "--items", "30", "--seed", "21", "--chapters", "1-7")
    if r.returncode: print("build failed", r.stderr[-300:]); return False
    for p in ("midterm", "makeup"):
        g = Graph().parse("%s/sen0401_exam_%s_v1_0_0_paper.ttl" % (d, p)); key = keys(d, p)
        for it in key["items"]:
            m = re.match(r"bank:ch(\d\d):(\w+):(\d+)$", it["item_key"])
            if not m: continue
            tot += 1; b = banks[int(m.group(1))][int(m.group(3))]
            node = [s for s in g.subjects(P.itemKey, None) if str(g.value(s, P.itemKey)) == it["item_key"]][0]
            opts = {str(g.value(o, P.letter)): (str(g.value(o, P.text)), str(g.value(o, P.isKey)).lower() == "true") for o in g.objects(node, P.option)}
            keyl = [l for l, (t, k) in opts.items() if k]
            ok = b["concept"] == m.group(2) and str(g.value(node, P.stem)) == b["q"] and len(opts) == 4 and keyl == [it["answer"]] and opts[it["answer"]][0] == b["options"][b["answer"]] and sorted(t for t, _ in opts.values()) == sorted(b["options"]) and LV[b["level"]] == it["bloom"]
            if not ok: bad.append((p, it["position"], it["item_key"]))
    print("control read the bank directly: %d bank items checked in both papers (stem, four options, the one marked key equals the bank's correct option, key letter, Bloom level); mismatches: %s" % (tot, bad)); return tot >= 40 and not bad
def param():
    r, d = build("p25", "--items", "10", "--seed", "5", "--chapters", "2,5"); ok = r.returncode == 0
    if ok:
        ch = {c for p in ("midterm", "makeup") for i in keys(d, p)["items"] for c in i["chapters"]}; print("chapters 2,5: chapters used %s" % sorted(ch)); ok &= ch <= {2, 5} and ch == {2, 5}
    else: print("chapters 2,5 build exit", r.returncode, r.stderr[-200:])
    r, d = build("p17", "--items", "28", "--seed", "6", "--chapters", "1-7")
    if r.returncode == 0:
        ch = {i["chapters"][0] for i in keys(d, "midterm")["items"]}; print("chapters 1-7: primary chapters %s" % sorted(ch)); ok &= 7 in ch
    else: print("1-7 build exit", r.returncode); ok = False
    r, d = build("p6", "--items", "24", "--seed", "7"); ch = {c for p in ("midterm", "makeup") for i in keys(d, p)["items"] for c in i["chapters"]}
    print("default chapters: chapters used %s (the owner's decision of 2026-10-30: 1 to 6, chapter 7 not in)" % sorted(ch)); ok &= r.returncode == 0 and ch == {1, 2, 3, 4, 5, 6}; return ok
def refuse():
    ok = True
    for name, a, why in (("r8", ["--items", "24", "--chapters", "1-8"], "chapter 8"), ("r0", ["--items", "0"], "zero items"), ("r999", ["--items", "999"], "too many items"), ("rpage", ["--items", "40", "--page-limit", "1"], "page limit 1")):
        r, d = build(name, *a); n = len(os.listdir(d)); print("%s: exit %d, files written %d" % (why, r.returncode, n)); ok &= r.returncode != 0 and n == 0
    return ok
def pdf():
    r, d = build("pdf", "--items", "26", "--seed", "31"); ok = r.returncode == 0
    for p in ("midterm", "makeup"):
        f = "%s/sen0401_exam_%s_v1_0_0.pdf" % (d, p); k = keys(d, p)
        pg = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
        txt = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True).stdout; nums = {int(x) for x in re.findall(r"(?:^|\s)(\d{1,2})[.)]\s", txt) if 1 <= int(x) <= 26}
        subprocess.run(["pdftoppm", "-r", "50", "-png", f, "%s/%s" % (d, p)]); from PIL import Image
        col = 0; wh = True
        for im in sorted(glob.glob("%s/%s-*.png" % (d, p))):
            I = Image.open(im).convert("RGB"); px = I.load(); w, h = I.size
            col += sum(1 for x in range(0, w, 2) for y in range(0, h, 2) if max(px[x, y]) - min(px[x, y]) > 8); wh &= all(min(px[x, y]) > 245 for x, y in ((1, 1), (w - 2, 1), (1, h - 2), (w - 2, h - 2)))
        print("%s: pdfinfo pages %d (engine record %d); positions found in text %d of 26; colour pixels %d; white corners %s" % (p, pg, k["pages"], len(nums), col, wh)); ok &= pg == k["pages"] and len(nums) == 26 and col == 0 and wh
    return ok
def nochange(c):
    st = [l for l in subprocess.run(["git", "-C", R, "show", "--name-status", "--format=", c], capture_output=True, text=True).stdout.split("\n") if l]
    notnew = [l for l in st if not l.startswith("A\t")]; out = [l for l in st if not l.split("\t")[1].startswith("08-tooling/exam/")]
    print("commit %s: %d files, all added: %s; all under 08-tooling/exam/: %s" % (c, len(st), not notnew, not out)); return bool(st) and not notnew and not out
k = sys.argv[1]
try: ok = {"rerun": rerun, "builds": builds, "answers": answers, "param": param, "refuse": refuse, "pdf": pdf, "nochange": lambda: nochange(sys.argv[2])}[k]()
finally: shutil.rmtree(W, ignore_errors=True) if k != "rerun" else None
print("RESULT", "MET" if ok else "NOT MET"); sys.exit(0 if ok else 1)
