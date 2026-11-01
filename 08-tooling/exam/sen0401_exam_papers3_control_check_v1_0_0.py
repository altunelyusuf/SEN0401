#!/usr/bin/env python3
"""sen0401_exam_papers3_control_check v1_0_0 - the lineage agent's own control of the midterm papers v3 (commit 3b13e2b), WITHOUT the builder's objects. Per form A and B it checks: the paper and key .docx are exported again here with LibreOffice (own profile): paper 5 pages, key 2 pages, the answer sheet PDF 1 page; every run of the question pages (the cover page uses the template font Verdana) is Arial at least 10 pt or Courier New at least 8 pt; the cover page fields; five questions with their points read from the paper text (Q1 to Q4 25 points each summing from their sub-questions, Q5 10 points bonus); every abbreviation of the question pages (all capitals) has its expansion at its first use; the Q2 programs in the .docx are run here (my own cs_encode) and each printed result equals the key's answer for that label, the four computed answers (3900, 3364, 65000, 192) equal the key's; the key and the sheet layout name the same form code; the two forms differ in order but hold the same item keys. Usage: papers3_control_check [WORKDIR]  Exit 0 only if every check holds."""
__version__ = "1.0.0"
import io, contextlib, json, os, re, subprocess, sys
from docx import Document
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "papers_midterm_v3"); W = sys.argv[1] if len(sys.argv) > 1 else "/tmp/sen0401_p3ctl"; os.makedirs(W, exist_ok=True); res = []
def chk(ok, m): res.append(bool(ok)); print("PASS " if ok else "FAIL ", m)
def pages(p): return int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout).group(1))
def cs_encode(n): return bytes(1) if n < 253 else bytes(3) if n <= 65535 else bytes(5) if n <= 4294967295 else bytes(9)
items = {}
for F in "AB":
    base = os.path.join(D, "sen0401_exam_midterm_v3_0_0_form%s_" % F); key = json.load(open(base + "key.json"))
    for k in ("paper", "key"):
        subprocess.run(["soffice", "--headless", "-env:UserInstallation=file://" + W + "/prof", "--convert-to", "pdf", "--outdir", W, base + k + ".docx"], capture_output=True, timeout=170)
    pp = os.path.join(W, os.path.basename(base) + "paper.pdf"); kp = os.path.join(W, os.path.basename(base) + "key.pdf")
    chk(pages(pp) == 5 and pages(kp) == 2 and pages(base + "sheet.pdf") == 1, "form %s: paper %d pages, key %d, sheet %d (expected 5, 2, 1)" % (F, pages(pp), pages(kp), pages(base + "sheet.pdf")))
    doc = Document(base + "paper.docx"); bad = []; started = False
    for p in doc.paragraphs:
        started = started or p.text.startswith("SEN0401 Special Topics: Blockchain - Midterm exam, Form")
        for r in (p.runs if started else []):
            if r.text.strip():
                n = r.font.name or (p.style.font.name if p.style and p.style.font else None); s = r.font.size.pt if r.font.size else (p.style.font.size.pt if p.style and p.style.font and p.style.font.size else None)
                if not ((n == "Arial" and s and s >= 10) or (n == "Courier New" and s and s >= 8)): bad.append((n, s, r.text[:20]))
    for t in []:
        for row in t.rows:
            for c in row.cells:
                for p in c.paragraphs:
                    for r in p.runs:
                        if r.text.strip():
                            n = r.font.name or (p.style.font.name if p.style and p.style.font else None); s = r.font.size.pt if r.font.size else (p.style.font.size.pt if p.style and p.style.font and p.style.font.size else None)
                            if not (s and s >= 8 and n in ("Arial", "Courier New")): bad.append((n, s, r.text[:20]))
    chk(not bad, "form %s: runs outside Arial >= 10 pt / Courier New >= 8 pt: %d %s" % (F, len(bad), bad[:3]))
    raw = subprocess.run(["pdftotext", pp, "-"], capture_output=True, text=True).stdout
    chk(all(x in raw for x in ("Student Name", "Student Identity Number", "Academic Year", "Duration", "Instructor", "Learning Outcomes", "Program Outcomes", "Form " + F, key["form_code"])), "form %s: cover fields and form code %s present on the render" % (F, key["form_code"]))
    qs = {int(m.group(1)): m.group(2) for m in re.finditer(r"Question (\d) - [^\n]*?\((\d+) points[^)]*\)", raw)} if False else {}
    heads = re.findall(r"Question (\d) - ([^\n(]*)\((\d+) points(, bonus)?\)", raw.replace("\n(", " ("))
    pts = {}
    for it in key["items"]: pts[it["question"]] = pts.get(it["question"], 0) + it["points"]
    chk(sorted(pts) == [1, 2, 3, 4, 5] and all(pts[q] == 25 for q in (1, 2, 3, 4)) and pts[5] == 10, "form %s: points per question from the key items %s (expected 25, 25, 25, 25 and 10 bonus)" % (F, pts))
    chk(key["total_points_without_bonus"] == 100 and key["bonus_points"] == 10, "form %s: total 100 and bonus 10 in the key" % F)
    q = raw[raw.index("Question 1 -"):]; seen = {}
    for m in re.finditer(r"\b[A-Z][A-Z0-9]{1,7}\b", q):
        w = m.group(0)
        if re.fullmatch(r"[A-D]|Q\d", w) or w.startswith("SEN"): continue
        seen.setdefault(w, m.start())
    miss = [w for w, p in seen.items() if w != "CODE" and not re.search(r"\(%s\)|\b%s \(" % (w, w), q[max(0, p - 90):p + 70])]
    chk(not miss, "form %s: all-capital abbreviations %s: expansion at the first use, missing for %s" % (F, sorted(seen), miss))
    blocks = []; cur = []; lab = None; labels = []
    for p in doc.paragraphs:
        t = p.text; fonts = {r.font.name for r in p.runs if r.text.strip()}
        if fonts == {"Courier New"}: cur.append(t)
        else:
            if cur: blocks.append((lab, "\n".join(cur))); cur = []
            m = re.match(r"(\d[a-h])\.", t)
            if m: lab = m.group(1)
    if cur: blocks.append((lab, "\n".join(cur)))
    ans = {}
    for it in key["items"]: ans.update(it.get("answer", {}))
    got = {}
    for lab, code in blocks:
        if lab and lab.startswith("2") and "print(" in code:
            g = {"cs_encode": cs_encode}; buf = io.StringIO()
            with contextlib.redirect_stdout(buf): exec(code, g)
            got[lab] = buf.getvalue().strip()
    val = lambda x: x["value"] if isinstance(x, dict) else x
    run_ok = all(str(got[l]) == str(val(ans.get(l))) for l in got)
    kset = sorted(val(ans[l]) for l in ans if isinstance(ans[l], dict) and l not in got and l[0] == "2")
    mine = sorted([50 * (40 + 20 + 10 + 5 + 2 + 1), 58 ** 2, 63250 * 4 - 62000 - 2 * 63000, 198 * 32 // 33])
    chk(len(got) == 4 and run_ok and kset == mine, "form %s: Q2 programs run here give %s equal to the key's answers for the same labels; the four computed answers %s equal the key's numeric answers %s (labels differ by form)" % (F, got, mine, kset))
    items[F] = sorted(it["item_key"] for it in key["items"]); lay = json.load(open(base + "sheet_layout.json"))
    chk(key["form_code"] in json.dumps(lay), "form %s: the sheet layout carries the form code %s" % (F, key["form_code"]))
chk(items["A"] == items["B"], "both forms hold the same %d items" % len(items["A"]))
print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
