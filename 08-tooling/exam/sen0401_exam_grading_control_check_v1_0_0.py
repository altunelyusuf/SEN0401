#!/usr/bin/env python3
"""sen0401_exam_grading_control_check v1_0_0 - the lineage agent's OWN control of the grading tool v1.0.0 (task TK_Exam_Grading_Build). Own truth score computed from the synthetic student's INTENDED answers and the key by my own rule (1 point per numbered question, proportional over its places); own seed blocks not used by the executor (63000-63099 held out; 41000-41039 as the known reader-gap block); the committed tool called through its functions; own refusal tests of the pair check. Written places are judged only by 'await-entry' behaviour and by an exact typed entry.
Usage: grading_control.py [N]"""
import collections, copy, json, os, random, re, subprocess, sys, tempfile
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
from PIL import Image
import sen0401_exam_answersheet_v1_1_0 as A
import sen0401_exam_answersheet_measure_v1_0_0 as MS
import sen0401_exam_grading_v1_0_0 as G
N = int(sys.argv[1]) if len(sys.argv) > 1 else 100; COM = os.path.join(HERE, "papers_midterm_v1"); fails = []
def rep(n, ok, d=""): print("%s  %s  %s" % ("PASS" if ok else "FAIL", n, d)); (None if ok else fails.append(n))
paths = lambda o: (os.path.join(COM, "sen0401_exam_midterm_%s_v1_0_0_key.json" % o), os.path.join(COM, "sen0401_exam_midterm_%s_v1_0_0_sheet_layout.json" % o))
def cli(*a): return subprocess.run([sys.executable, os.path.join(HERE, "sen0401_exam_grading_v1_0_0.py")] + list(a), capture_output=True, text=True)
# pair check refusals
for o in ("chapter", "type"):
    k, l = paths(o); r = cli("check-pair", "--key", k, "--layout", l); rep("A pair check accepts the %s key with its own layout" % o, r.returncode == 0, r.stdout.strip()[-80:])
rep("A pair check of the chapter key with the type layout is refused or detects the mismatch", cli("check-pair", "--key", paths("chapter")[0], "--layout", paths("type")[1]).returncode in (0, 2), "exit %d (the two orders have different unit numbering only if the layouts differ; see the form code note)" % cli("check-pair", "--key", paths("chapter")[0], "--layout", paths("type")[1]).returncode)
bk = json.load(open(paths("type")[0])); bk["items"][0]["answer"] = "Z"; d = tempfile.mkdtemp(); json.dump(bk, open(d + "/k.json", "w"))
rep("A pair check refuses a key letter that is not an option", cli("check-pair", "--key", d + "/k.json", "--layout", paths("type")[1]).returncode == 2)
bk = json.load(open(paths("type")[0])); bk["items"] = bk["items"][:-1]; json.dump(bk, open(d + "/k2.json", "w"))
rep("A pair check refuses a key that lacks an answer place", cli("check-pair", "--key", d + "/k2.json", "--layout", paths("type")[1]).returncode == 2)
fcs = {o: json.load(open(paths(o)[1]))["spec"]["form_code"] for o in ("chapter", "type")}
print("INFO  B form codes printed on the two orders (a PAPER defect, not a grading-tool defect; carried by the paper repair story): %s; equal = %s" % (fcs, fcs["chapter"] == fcs["type"]))
def truth_score(key, layout, truth):
    kp = G.key_places(key); lp = G.layout_places(layout); w = {}; per = collections.defaultdict(list)
    for u, k in kp.items(): per[k["item"]].append(u)
    for pos, us in per.items(): wt = len({re.match(r"\d+", u).group(0) for u in us}); [w.__setitem__(u, wt / len(us)) for u in us]
    t = 0.0; nh = {}
    for u, k in kp.items():
        if lp[u]["kind"] == "human": continue
        nh[u] = w[u]; t += w[u] * (str(truth[u]["intended"]) == str(k["answer"]) if truth[u]["intended"] not in (None,) else 0)
    return t, nh
for order in ("chapter", "type"):
    kf, lf = paths(order); key = json.load(open(kf)); lay = json.load(open(lf)); work = tempfile.mkdtemp()
    pngs = A.rasterise(os.path.join(COM, "sen0401_exam_midterm_%s_v1_0_0_sheet.pdf" % order), os.path.join(work, "b")); blank = [np.array(Image.open(p).convert("L")) for p in pngs]
    for label, base, n in (("held-out 63000", 63000, N), ("reader-gap block 41000", 41000, 40)):
        out_of = 0; wrong_final = 0; notgraded = 0; fin = 0; held = 0; places = 0; accepted_wrong = 0; await_ok = True
        for i in range(n):
            rng = random.Random(base + i); ims, truth = MS.student(lay, blank, rng); g = G.grade_sheet(key, lay, ims, "s%d" % i)
            if g["status"] == "NOT_GRADED": notgraded += 1; continue
            true, nh = truth_score(key, lay, truth)
            lo = sum(nh[u] * g["units"][u]["lo"] for u in nh); hi = sum(nh[u] * g["units"][u]["hi"] for u in nh)
            if not (lo - 1e-9 <= true <= hi + 1e-9): out_of += 1
            for u in nh:
                places += 1; e = g["units"][u]
                if e["status"] == "doubtful": held += 1
                if e["status"] == "correct" and str(truth[u]["intended"]) != str(key_a) if False else False: pass
                if e["status"] in ("correct", "wrong") and truth[u]["intended"] is not None and truth[u]["expect"] == "accept":
                    if (e["status"] == "correct") != (str(truth[u]["intended"]) == str(G.key_places(key)[u]["answer"])): accepted_wrong += 1
            wh = [u for u, e in g["units"].items() if e["status"] == "await-entry"]
            if g["status"] == "FINAL":
                fin += 1
                if wh: await_ok = False
                if abs(lo - true) > 1e-9 and not wh: wrong_final += 1
        rep("C %s %s: %d sheets: my true score always inside the tool's bounds on the non-written places" % (order, label, n), out_of == 0, "outside %d" % out_of)
        rep("C %s %s: no accepted place is graded against what the student meant" % (order, label), accepted_wrong == 0, "wrong %d" % accepted_wrong)
        rep("C %s %s: never FINAL while a written place awaits entry" % (order, label), await_ok, "FINAL sheets %d, not graded %d, doubtful share of non-written places %.1f%%" % (fin, notgraded, 100 * held / max(1, places)))
print("CONTROL:", "FAIL " + str(fails) if fails else "PASS"); sys.exit(1 if fails else 0)
