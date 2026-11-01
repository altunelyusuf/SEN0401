#!/usr/bin/env python3
"""sen0401_exam_cover_control_check v1_0_0 - the control's own check of the cover renderer (commit f60a817): both demo covers exported by LibreOffice here are exactly 1 page, carry the required fields as text, do not carry the template's other course name, the renderer fails with a clear error when the template path is missing, and the template is not committed in the repository. Usage: run"""
import os, re, subprocess, sys, tempfile, shutil
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(os.path.dirname(H)); res = []
def chk(ok, m): res.append(bool(ok)); print("PASS " if ok else "FAIL ", m)
sys.path.insert(0, H)
tmp = tempfile.mkdtemp()
def txt(p): return subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout
from docx import Document
tpl = "\n".join(p.text for p in Document("/home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx").paragraphs)
other = [l.strip() for l in tpl.splitlines() if re.search(r"\b[A-Z]{3}\s?\d{3,4}\b", l)]
for n, code in (("sen0401_exam_cover_demo_v1_0_0.docx", "SEN0401"), ("sen0401_exam_cover_demo_sen0414_v1_0_0.docx", "SEN0414")):
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, os.path.join(H, n)], capture_output=True, timeout=240)
    p = os.path.join(tmp, n.replace(".docx", ".pdf")); info = subprocess.run(["pdfinfo", p], capture_output=True, text=True).stdout; pages = int(re.search(r"Pages:\s+(\d+)", info).group(1)); t = txt(p)
    chk(pages == 1, "%s: %d page on the control's own LibreOffice export" % (code, pages))
    need = [code, "Midterm", "2026", "Fall", "60", "Altunel", "Question", "Bonus", "Total", "Date"]
    miss = [w for w in need if w.lower() not in t.lower()]; chk(not miss, "%s: required fields present as text (missing %s)" % (code, miss))
    chk(not any(o and o in t for o in other), "%s: no other-course code from the template in the text (%s)" % (code, other[:2]))
import importlib
c = importlib.import_module("sen0401_exam_cover_render_v1_0_0")
try:
    d = c.new_document(template="/nonexistent/template.docx"); ok = False; msg = "no error"
except Exception as e:
    ok = True; msg = (type(e).__name__ + ": " + str(e))[:120]
chk(ok, "a missing template path fails with an error: " + msg)
tracked = subprocess.run(["git", "-C", R, "ls-files"], capture_output=True, text=True).stdout
chk("IKU_exam_cover_page_template" not in tracked, "the template file is not tracked in the repository")
shutil.rmtree(tmp); print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
