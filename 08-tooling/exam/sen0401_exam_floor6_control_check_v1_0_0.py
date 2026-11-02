#!/usr/bin/env python3
"""Control of the floor-at-0 correction (new file v1.0.0). Holds no question and no answer (reads the key from CME at run time).
F1 SHA-256 of the 3 public and the 7 CME files as reported; F2 paper.docx and sheet.pdf equal their e8efedb blobs and the reported hashes; F3 the scoring check v1_1_0 re-run (26 of 26);
F4 my own floor test on the module v1_1_0 with my own marks: a sheet whose raw total is below 0 gives total 0 and keeps negative per-question points, a sheet above 0 is equal to the raw total, a perfect sheet 100, a blank sheet 0, the bonus is added after the floor;
F5 my own blind simulation (5000 sheets): the mean of the floored total is above the mean of the raw total and about 3.6, raw near 0; F6 the v1_0_0 module still gives the unfloored total; F7 the rule file says the floor is decided and no longer says not decided;
F8 the new key.json carries the same items as the key v6.0.0 (equal) and no 'not raised to 0' sentence; F9 the key.docx text says the floor; F10 the leak search of the public tree passes."""
import hashlib, json, os, random, re, subprocess, sys, statistics as S
sys.dont_write_bytecode = True
E = "/home/claude/sen0401/08-tooling/exam/"; C = "/home/claude/CME/exams/SEN0401/08-tooling/exam/"; V = C + "papers_midterm_v6/"; Fd = C + "floor_v6/"; sys.path.insert(0, E)
H = {E + "sen0401_exam_scoring_v1_1_0.py": "f3b25dac", E + "sen0401_exam_scoring_rule_v1_1_0.json": "f6913a03", E + "sen0401_exam_scoring_check_v1_1_0.py": "61bfb27b",
 Fd + "sen0401_exam_midterm_v6_1_0_key.docx": "8e732dcd", Fd + "sen0401_exam_midterm_v6_1_0_key.pdf": "0ea12902", Fd + "sen0401_exam_midterm_v6_1_0_key.json": "fba87c18", Fd + "sen0401_exam_scoring_check_log_v1_1_0.txt": "c92b0a66",
 Fd + "sen0401_exam_key_floor_build_log_v1_0_0.txt": "4d06b9f9", C + "sen0401_exam_key_floor_build_v1_0_0.py": "76f20b0d", C + "sen0401_exam_paper_lib_v6_1_0.py": "a16f42b4"}
bad = []
def ok(n, c, m=""):
    print(("PASS " if c else "FAIL ") + n + (" " + m if m else ""))
    if not c: bad.append(n)
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
for p, x in H.items(): ok("F1 " + os.path.basename(p), os.path.exists(p) and h(p).startswith(x))
for f, x in (("sen0401_exam_midterm_v6_0_0_paper.docx", "a0551543"), ("sen0401_exam_midterm_v6_0_0_sheet.pdf", "e3de7bba")):
    blob = subprocess.run(["git", "-C", "/home/claude/CME", "show", "e8efedb:exams/SEN0401/08-tooling/exam/papers_midterm_v6/" + f], capture_output=True).stdout
    ok("F2 %s equals its e8efedb blob and starts with %s" % (f, x), hashlib.sha256(blob).hexdigest() == h(V + f) and h(V + f).startswith(x))
r = subprocess.run([sys.executable, "-B", E + "sen0401_exam_scoring_check_v1_1_0.py", E + "sen0401_exam_scoring_rule_v1_1_0.json", "--key", V + "sen0401_exam_midterm_v6_0_0_key.json"], capture_output=True, text=True); ok("F3 scoring check v1_1_0 re-run", r.returncode == 0 and "SUMMARY 26 of 26 checks PASS" in r.stdout)
import sen0401_exam_scoring_v1_1_0 as N, sen0401_exam_scoring_v1_0_0 as O
key = json.load(open(V + "sen0401_exam_midterm_v6_0_0_key.json")); mk = [m for m in N.marks_of_key(key) if m["guessable"]]
wrong = lambda m: "__wrong__"
neg = {m["label"]: (N.DOUBLE if False else "zzz") for m in mk}   # every place answered with a value that is never right
rn = N.score(neg, key); ro = O.score(neg, key)
ok("F4a an all-wrong sheet: raw total %.2f below 0, floored total %s, a question below 0 kept" % (rn.get("raw_total", ro["total"]), rn["total"]), rn["total"] == 0 and ro["total"] < 0 and min(rn["per_question"].values()) < 0)
perfect = N.perfect_marks(key); ok("F4b perfect sheet 100 and equal to the old module", abs(N.score(perfect, key)["total"] - 100) < 1e-6 and abs(O.score(perfect, key)["total"] - 100) < 1e-6)
ok("F4c blank sheet 0", N.score({}, key)["total"] == 0)
mixed = dict(perfect); first = mk[0]["label"]; mixed[first] = "zzz"; a, b = N.score(mixed, key)["total"], O.score(mixed, key)["total"]; ok("F4d a sheet above 0 is unchanged (%.4f = %.4f)" % (a, b), abs(a - b) < 1e-9 and a > 0)
bon = dict(neg); [bon.__setitem__(m["label"], 2.0) for m in N.marks_of_key(key) if not m["guessable"]]; rb = N.score(bon, key); ok("F4e bonus added after the floor: total %s bonus %s" % (rb["total"], rb["bonus"]), rb["total"] == 0 and rb["bonus"] > 0)
rng = random.Random(4242); raw = []; fl = []
for _ in range(5000):
    m = N.blind_marks(key, rng); raw.append(O.score(m, key)["total"]); fl.append(N.score(m, key)["total"])
ok("F5 my blind simulation: raw mean %.3f, floored mean %.3f, share floored %.3f" % (S.mean(raw), S.mean(fl), sum(1 for x in raw if x < 0) / 5000.0), abs(S.mean(raw)) < 0.6 and 3.0 < S.mean(fl) < 4.4 and 0.45 < sum(1 for x in raw if x < 0) / 5000.0 < 0.6)
ok("F6 v1_0_0 still unfloored (all-wrong total %.2f)" % ro["total"], ro["total"] < 0)
rule = open(E + "sen0401_exam_scoring_rule_v1_1_0.json").read(); ok("F7 rule file: floor decided, 'NOT DECIDED' gone", "DECIDED by the owner" in rule and "NOT DECIDED" not in rule)
k1 = json.load(open(Fd + "sen0401_exam_midterm_v6_1_0_key.json")); ok("F8 key.json items equal the key v6.0.0 and no 'not raised to 0'", k1["items"] == key["items"] and "not raised to 0" not in json.dumps(k1))
from docx import Document
d = Document(Fd + "sen0401_exam_midterm_v6_1_0_key.docx"); tx = " ".join(p.text for p in d.paragraphs); ok("F9 key.docx states the floor and not the old sentence", re.search(r"floor", tx, re.I) is not None and "not raised to 0" not in tx)
r = subprocess.run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_2.py", "leakscan"], capture_output=True, text=True); ok("F10 leak search of the public tree", r.returncode == 0 and "RESULT PASS" in r.stdout)
print("CONTROL " + ("PASS" if not bad else "FAIL " + ",".join(bad))); sys.exit(1 if bad else 0)
