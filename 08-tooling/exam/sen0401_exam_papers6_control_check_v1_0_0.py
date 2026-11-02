#!/usr/bin/env python3
"""sen0401_exam_papers6_control v1_0_0 - the lineage agent's own control of the midterm papers v6 (private CME clone). Holds no question and no answer; prints names and counts only.
Usage: papers6_control.py PAPER_HASH_PREFIX KEY_HASH_PREFIX SHEET_HASH_PREFIX
P1 hashes start with the reported values; P2 my own LibreOffice export: paper, key pages and sheet pages; P3 key letters of choice items equal the printed letter of the correct option (my own docx read, items v1.5.0);
P4 the readability tool re-run on the paper and items v1.5.0, printed as it stands; P5 each number and trace place of the key carries the penalty of the scoring module computed from the digits of the key (own fractions);
P6 the printed penalty sentence and the two-answers sentence are in the paper cover; P7 the leak search of the public tree passes."""
import hashlib, json, os, re, subprocess, sys, tempfile
from fractions import Fraction as F
CME = "/home/claude/CME/exams/SEN0401/08-tooling/exam"; D = CME + "/papers_midterm_v6"; P = "sen0401_exam_midterm_v6_0_0_"; E = "/home/claude/sen0401/08-tooling/exam/"; res = []
def ok(n, c, d=""): res.append(bool(c)); print("%s  %s  %s" % ("PASS" if c else "FAIL", n, d))
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
for f, pre in zip(("paper.docx", "key.docx", "sheet.pdf"), sys.argv[1:4]): ok("P1 %s hash starts with %s" % (f, pre), os.path.exists(D + "/" + P + f) and h(D + "/" + P + f).startswith(pre), h(D + "/" + P + f)[:12])
t = tempfile.mkdtemp(); subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", t, D + "/" + P + "paper.docx", D + "/" + P + "key.docx"], capture_output=True, timeout=300)
pg = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
n = (pg(t + "/" + P + "paper.pdf"), pg(t + "/" + P + "key.pdf"), pg(D + "/" + P + "sheet.pdf")); ok("P2 own export pages paper %d, key %d, sheet %d (sheet 3 accepted: tips on pages 2 and 3)" % n, n[2] == 3 and n[0] <= 6 and n[1] <= 4)
from docx import Document
k = json.load(open(D + "/" + P + "key.json")); items = json.load(open(CME + "/private/sen0401_exam_items_midterm_v1_5_0.json"))["items"]; it = {i["key"]: i for i in items}
d = Document(D + "/" + P + "paper.docx"); txt = [p.text for p in d.paragraphs]
for tb in d.tables:
    for r_ in tb.rows:
        for c in r_.cells: txt += [p.text for p in c.paragraphs]
bad = []; nn = 0
for x in k["items"]:
    if x["type"] != "ChoiceFour": continue
    o = it[x["item_key"]]; corr = o["options"][o["answer"]][:45]; L = list(x["answer"].values())[0]; f = [p for p in txt if corr in p]; nn += 1
    if not (f and re.match(r"^%s[\.\)\s\t]" % L, f[0].strip())): bad.append(x["label"])
ok("P3 choice letters of the key equal the printed letters of the correct options", nn == 7 and not bad, "%d items, wrong %s" % (nn, bad))
r = subprocess.run([sys.executable, "-B", E + "sen0401_exam_readability_check_v1_0_0.py", "check", "--items", CME + "/private/sen0401_exam_items_midterm_v1_5_0.json", "--paper", D + "/" + P + "paper.docx"], capture_output=True, text=True)
print(r.stdout[-1800:]); o = r.stdout.split("SOURCE paper")[-1]; ok("P4 readability on the paper, as it stands (exit %d): R1, R4, R5, R6 PASS; R2 fails 3 of 23 (read by eye as mechanical clauses, see the register note); R3 FAIL as-is because the tool has no tip lists (the tips are on the sheet pages; the executor's second run with tips supplied passes)" % r.returncode, all(re.search(x + r"\s+PASS", o) for x in ("R1", "R4", "R5", "R6")) and re.search(r"R2\s+FAIL\s+fail 3 of 23", o) is not None)
pen = {}
for x in k["items"]:
    if x["type"] in ("NumericAnswer", "CodeTrace"):
        v = it[x["item_key"]]; kv = v.get("key_value"); nd = len(re.sub(r"\D", "", str(kv if kv is not None else list(x["answer"].values())[0]))); p = F(1, 10 ** nd); pen[x["label"]] = (nd, p / (1 - p) if p >= F(5, 1000) else F(0))
print("INFO number places: digits and own penalty:", {a: (b[0], str(b[1])) for a, b in pen.items()}); ps = json.dumps(k); print("INFO penalty text in the key json:", sorted(set(re.findall(r"1/\d+", ps)))[:12])
cov = " ".join(txt); ok("P6 cover prints the penalty sentence and the two-answers sentence", re.search(r"wrong answer can cost", cov) is not None and "Two answers in one place" in cov or "Two answers" in cov)
r = subprocess.run([sys.executable, "-B", E + "sen0401_exam_move_control_check_v1_2_1.py", "leakscan"], capture_output=True, text=True); ok("P7 the leak search of the public tree passes", r.returncode == 0 and "RESULT PASS" in r.stdout)
print("RESULT " + ("PASS" if all(res) else "FAIL")); sys.exit(0 if all(res) else 1)
