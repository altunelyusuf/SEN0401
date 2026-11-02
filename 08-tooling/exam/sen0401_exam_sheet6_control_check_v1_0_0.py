#!/usr/bin/env python3
"""Control of the v6 sheet and scoring work (new file v1.0.0). Holds no question and no answer.
Checks: hashes of the 8 public and 4 CME files as reported; my own derivation of every penalty p/(1-p) as an exact fraction
(zero expected gain for a blind mark) compared with the rule file; scoring check re-run (13 of 13); sheet check re-run on the
CME sheet (22 of 22, new log in a temp folder); the sheet PDF has 2 A4 pages; leak search of the public tree."""
import hashlib, json, os, subprocess, sys, tempfile
from fractions import Fraction as F
E = "/home/claude/sen0401/08-tooling/exam/"; S = "/home/claude/CME/exams/SEN0401/08-tooling/exam/"; Z = S + "sheet_v6/"; K = S + "papers_midterm_v5/sen0401_exam_midterm_v5_0_0_key.json"
H = {E + "sen0401_exam_scoring_rule_v1_0_0.json": "8c9e54d29731c5ac2e857a378abbda1cfa8cdef54c46dd4f8c4e9902ae40891a", E + "sen0401_exam_scoring_v1_0_0.py": "0b348bd19f5bb8cd8674120b5590f38d871e497bd4f0f956c94b6f3c457c2855",
 E + "sen0401_exam_scoring_check_v1_0_0.py": "fb35e9d7611a0213dcad0e36d632d4e55055c2a69dd3bc1ea7f51655c5b3dd0d", E + "sen0401_exam_answersheet_v6_0_0.py": "408041adfa9c2c5ff62332de21caeaea6914c01e6ac39255d51d15480075e4d5",
 E + "sen0401_exam_answersheet_v6_build_v1_0_0.py": "7cbce1072c0f2d760c0dcab5da7169292de80a4219286ab4c16c3f66eb71e4e1", E + "sen0401_exam_answersheet_v1_3_0.py": "f6f8b0d272e466f469bf054317a8fddcfa7a3873a111b68acf084c019c5f298a",
 E + "sen0401_exam_answersheet_measure_v6_0_0.py": "3763da4419570d922b1079eedf88a39dd79edddf15604a830c9eb8875e4e7e3d", E + "sen0401_exam_answersheet_check_v6_0_0.py": "bfd7ebcf3a7f53d6ca0bd817fc2672ed11dbc06be1589c41a6dfcbcd7e314163",
 Z + "sen0401_exam_midterm_v5form_sheet_v6_0_0.pdf": "a805535cb0edf73abeed7b4b2aaaf749849141e155541ecf5563935451cff1d3", Z + "sen0401_exam_midterm_v5form_sheet_v6_0_0_layout.json": "00ac8d56570d4cd4672ea333ada560863daf1f1dec0ce2cd779b9e722d99967b",
 Z + "sen0401_exam_answersheet_check_log_v6_0_0.txt": "cc8b6fcfce059714894d46f6c641c0a5dcfa8e63d5a2e91d780a0cc85348f485", Z + "sen0401_exam_scoring_check_log_v1_0_0.txt": "86fba650481375bf39066e6879d5c0f055666f2c876b31cc1ace31ce463eb903"}
bad = []
def ok(n, c, m=""):
    print(("PASS " if c else "FAIL ") + n + (" " + m if m else ""))
    if not c: bad.append(n)
def run(*a): return subprocess.run([sys.executable, "-B", *a], capture_output=True, text=True)
for p, h in H.items(): ok("H " + os.path.basename(p), hashlib.sha256(open(p, "rb").read()).hexdigest() == h)
rule = open(E + "sen0401_exam_scoring_rule_v1_0_0.json").read(); ok("P0 rule file text holds no key letter table (no 'answer' key)", '"answer"' not in rule and '"key"' not in rule)
exp = {"choice4": (F(1, 4), F(1, 3)), "match": (F(1, 6), F(1, 5)), "order5": (F(1, 5), F(1, 4)), "bank": (F(1, 4), F(1, 3)), "num1": (F(1, 10), F(1, 9)), "num2": (F(1, 100), F(1, 99))}
ok("P1 own derivation q = p/(1-p) gives zero expected blind gain for each", all(p - (1 - p) * q == 0 and q == p / (1 - p) for p, q in exp.values()))
for frag in ("1/3", "1/5", "1/4", "1/9", "1/99"): ok("P2 the rule file states " + frag, frag in rule)
r = run(E + "sen0401_exam_scoring_check_v1_0_0.py", E + "sen0401_exam_scoring_rule_v1_0_0.json", "--key", K); ok("C1 scoring check re-run", r.returncode == 0 and "SUMMARY 13 of 13 checks PASS" in r.stdout)
w = tempfile.mkdtemp(); r = run(E + "sen0401_exam_answersheet_check_v6_0_0.py", Z, "--tag", "sen0401_exam_midterm_v5form_sheet_v6_0_0", "--key", K, "--log", w + "/l.txt")
ok("C2 sheet check re-run", r.returncode == 0 and "SUMMARY 22 of 22 checks PASS" in r.stdout)
pi = subprocess.run(["pdfinfo", Z + "sen0401_exam_midterm_v5form_sheet_v6_0_0.pdf"], capture_output=True, text=True).stdout; ok("C3 pdfinfo: 2 pages, A4", "Pages:           2" in pi and "595.276 x 841.89" in pi)
r4 = run(E + "sen0401_exam_move_control_check_v1_2_1.py", "leakscan"); ok("S1 leak search of the public tree", "RESULT PASS" in r4.stdout)
print("CONTROL " + ("PASS" if not bad else "FAIL " + ",".join(bad))); sys.exit(1 if bad else 0)
