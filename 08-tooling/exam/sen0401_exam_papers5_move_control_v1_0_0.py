#!/usr/bin/env python3
"""sen0401_exam_papers5_move_control v1_0_0 - the lineage agent's own control of the midterm papers v5 that live in the private CME clone. Holds no question and no answer. Prints names and counts only.
P1 the three Word and PDF files exist and their SHA-256 start with the values the executor reported; P2 my own LibreOffice export of the two Word files gives the pages 6 (paper) and 3 (key), the sheet has 1; P3 the executor's papers control and sheet check re-run from the CME folder (exit 0); P4 every choice answer letter of the key is the letter under which the printed Word text holds the item's correct option (own docx read); P5 the leak search (check v1_2_1, mode leakscan) passes: nothing of the new form is tracked in the public tree."""
import hashlib, json, os, re, subprocess, sys, tempfile
CME = "/home/claude/CME/exams/SEN0401/08-tooling/exam"; D = CME + "/papers_midterm_v5"; P = "sen0401_exam_midterm_v5_0_0_"; res = []
def ok(n, c, d=""): res.append(bool(c)); print("%s  %s  %s" % ("PASS" if c else "FAIL", n, d))
h = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
for f, pre in (("paper.docx", "6be80b3a"), ("key.docx", "7dc6a4e7"), ("sheet.pdf", "9760f4cd")):
    ok("P1 %s hash starts with %s" % (f, pre), os.path.exists(D + "/" + P + f) and h(D + "/" + P + f).startswith(pre))
t = tempfile.mkdtemp(); subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", t, D + "/" + P + "paper.docx", D + "/" + P + "key.docx"], capture_output=True, timeout=300)
pg = lambda f: int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", f], capture_output=True, text=True).stdout).group(1))
ok("P2 own export: paper pages 6, key pages 3, sheet pages 1", (pg(t + "/" + P + "paper.pdf"), pg(t + "/" + P + "key.pdf"), pg(D + "/" + P + "sheet.pdf")) == (6, 3, 1), str((pg(t + "/" + P + "paper.pdf"), pg(t + "/" + P + "key.pdf"), pg(D + "/" + P + "sheet.pdf"))))
for nm, args in (("sen0401_exam_papers5_control_check_v1_0_0.py", ["/tmp/p5ctl_w2"]), ("sen0401_exam_answersheet_check_v5_0_0.py", ["papers_midterm_v5"])):
    r = subprocess.run([sys.executable, "-B", CME + "/" + nm] + args, capture_output=True, text=True, cwd=CME, timeout=1500); ok("P3 %s re-run from CME: exit 0, no FAIL line" % nm, r.returncode == 0 and not [l for l in r.stdout.splitlines() if l.startswith("FAIL")], r.stdout.strip().splitlines()[-1][:80] if r.stdout.strip() else "")
from docx import Document
k = json.load(open(D + "/" + P + "key.json")); it = {i["key"]: i for i in json.load(open(CME + "/private/sen0401_exam_items_midterm_v1_4_0.json"))["items"]}
d = Document(D + "/" + P + "paper.docx"); txt = [p.text for p in d.paragraphs]
for tb in d.tables:
    for r_ in tb.rows:
        for c in r_.cells: txt += [p.text for p in c.paragraphs]
bad = []; n = 0
for x in k["items"]:
    if x["type"] != "ChoiceFour": continue
    o = it[x["item_key"]]; corr = o["options"][o["answer"]][:45]; L = list(x["answer"].values())[0]; f = [p for p in txt if corr in p]; n += 1
    if not (f and re.match(r"^%s[\.\)\s\t]" % L, f[0].strip())): bad.append(x["label"])
ok("P4 choice letters of the key equal the printed letters of the correct options", n == 7 and not bad, "%d items, wrong %s" % (n, bad))
r = subprocess.run([sys.executable, "-B", "/home/claude/sen0401/08-tooling/exam/sen0401_exam_move_control_check_v1_2_1.py", "leakscan"], capture_output=True, text=True); ok("P5 the leak search of the public tree passes", r.returncode == 0)
print("RESULT " + ("PASS" if all(res) else "FAIL")); sys.exit(0 if all(res) else 1)
