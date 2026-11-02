#!/usr/bin/env python3
"""Control of the readability tool (new file, v1.0.0). Holds no question and no answer.
Checks: (1) SHA-256 of the four public files and the two CME baseline files as reported; (2) the fixtures re-run
(RESULT PASS, 0 rows wrong, and the table lines equal the committed log); (3) a mutation: one expectation changed in a copy
must give RESULT FAIL; (4) the baseline re-run on the v5 paper and items equals the CME baseline text; (5) my own word
count of the 15 item stems that hold a plain q field (all above 60) agrees with the tool's R1 failure count (at least 15, 17 reported);
(6) the fixtures hold no 40-character string from the private items; (7) the public leak search passes."""
import hashlib, json, os, re, subprocess, sys, tempfile
R = "/home/claude/sen0401"; E = R + "/08-tooling/exam/"; CME = "/home/claude/CME/exams/SEN0401/08-tooling/exam/"
TOOL = E + "sen0401_exam_readability_check_v1_0_0.py"; FX = E + "sen0401_exam_readability_fixtures_v1_0_0.json"
H = {E + "sen0401_exam_readability_check_v1_0_0.py": "12cf484d0e7ddc4fd7ce48e9b4789ccf036644f5c57c4776d18cf907b14bbb9a",
     E + "sen0401_exam_readability_rule_v1_0_0.json": "0148f259acc07c2a9a2deacf66bc2d1519b300bddafeea6b808fb07352bea59d",
     FX: "a0d5ce547cd4032db2296212f2977e164f16f929923f3f84130320235ba69677",
     E + "sen0401_exam_readability_fixtures_log_v1_0_0.txt": "c79450801273276793c3c14e78a1bdd32aebfe7fa5303ce5a0e3d6d8b3fe46f2",
     CME + "sen0401_exam_readability_baseline_v5_v1_0_0.txt": "e0223d4e175776b0fa1516b791bf4c2e3ae6ebd6f5138e5024e3fa3c41675231",
     CME + "sen0401_exam_readability_baseline_v5_v1_0_0.json": "50d62c9dd8115d013b340887665f52f9851fc26647a8b2a3efbf0bea5170e21e"}
bad = []
def ok(n, c, m=""):
    print(("PASS " if c else "FAIL ") + n + (" " + m if m else "")); 
    if not c: bad.append(n)
def run(*a): return subprocess.run([sys.executable, "-B", *a], capture_output=True, text=True)
for p, h in H.items(): ok("H " + os.path.basename(p), hashlib.sha256(open(p, "rb").read()).hexdigest() == h)
w = tempfile.mkdtemp(); r = run(TOOL, "fixtures", "--spec", FX, "--workdir", w)
ok("F1 fixtures RESULT PASS", "RESULT PASS  (0 row(s) answered wrongly)" in r.stdout and r.returncode == 0)
log = open(E + "sen0401_exam_readability_fixtures_log_v1_0_0.txt").read()
rows = [l for l in r.stdout.splitlines() if re.match(r"^[FD]\d\d ", l)]
ok("F2 table rows (%d) all in the committed log" % len(rows), len(rows) >= 27 and all(l in log for l in rows))
d = json.load(open(FX)); c = d["cases"]; k = next(x for x in c if not x["expect"]); k["expect"] = {"R1": "F"}
m = w + "/mut.json"; json.dump(d, open(m, "w")); r2 = run(TOOL, "fixtures", "--spec", m, "--workdir", w)
ok("F3 mutated expectation gives RESULT FAIL", "RESULT FAIL" in r2.stdout)
nf = len([x for x in c]); ok("F4 22 stems and 5 directions", len(c) == 22 and len(d["directions"]) == 5)
P = CME + "papers_midterm_v5/sen0401_exam_midterm_v5_0_0_paper.docx"; I = CME + "private/sen0401_exam_items_midterm_v1_4_0.json"
r3 = run(TOOL, "check", "--items", I, "--paper", P)
ok("B1 baseline re-run equals the CME baseline text", r3.stdout == open(CME + "sen0401_exam_readability_baseline_v5_v1_0_0.txt").read() and r3.returncode == 1, "exit %d" % r3.returncode)
items = json.load(open(I))["items"]; long_ = [i for i in items if isinstance(i.get("q"), str) and len(i["q"].split()) > 60]
n1 = int(re.search(r"R1\s+FAIL\s+fail (\d+) of 21", r3.stdout).group(1))
ok("B2 own count of stems above 60 words: %d of the 15 with a plain q; tool says %d of 21" % (len(long_), n1), len(long_) == 15 and n1 >= 15)
priv = [s for i in items for s in re.split(r"(?<=[.?!])\s+", str(i.get("q", ""))) if len(s) >= 40]; ft = open(FX).read()
ok("S1 no private sentence of 40+ characters (%d tried) in the fixtures" % len(priv), not any(s in ft for s in priv))
r4 = run(R + "/08-tooling/exam/sen0401_exam_move_control_check_v1_2_1.py", "leakscan"); ok("S2 leak search of the public tree", "RESULT PASS" in r4.stdout)
print("CONTROL " + ("PASS" if not bad else "FAIL " + ",".join(bad))); sys.exit(1 if bad else 0)
