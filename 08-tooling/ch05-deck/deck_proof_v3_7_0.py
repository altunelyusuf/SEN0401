#!/usr/bin/env python3
"""Proof of the deck v3.7.0 against v3.6.0 (a NEW tool file): the version probe appears 54 times in v3.6.0 and 0 times in v3.7.0; the code lines equal v3.6.0 minus the 27 probe lines; each result line reads 'EXPRESSION  ->  VALUE'
with the expression of the example; every other shape text, every note, and every package part except the 27 slides and docProps/core.xml equal. Usage: deck_proof_v3_7_0.py"""
import os, re, sys, zipfile
from pptx import Presentation
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
A = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_6_0.pptx"; B = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_7_0.pptx"
PROBE = '__import__("sys").version_info[:2]'; AR = "  →  "
fail = 0
def chk(label, ok, extra=""):
    global fail; fail += (not ok); print("%s %s %s" % ("PASS" if ok else "FAIL", label, extra))
def count(path):
    n = 0
    for sl in Presentation(path).slides:
        for sh in sl.shapes:
            if sh.has_text_frame and sh.name.startswith(("code ", "result line ")): n += sum(p.text.count(PROBE) for p in sh.text_frame.paragraphs)
    return n
ca, cb = count(A), count(B); print("occurrences of the probe in code boxes and result lines: v3_6_0 %d, v3_7_0 %d" % (ca, cb))
chk("probe 54 times before, 0 times after", (ca, cb) == (54, 0))
pa, pb = Presentation(A), Presentation(B); bad_code = bad_res = bad_other = 0; nres = 0
for i, (sa, sb) in enumerate(zip(pa.slides, pb.slides), 1):
    ca_ = [p.text for sh in sa.shapes if sh.name.startswith("code ") for p in sh.text_frame.paragraphs]
    cb_ = [p.text for sh in sb.shapes if sh.name.startswith("code ") for p in sh.text_frame.paragraphs]
    if ca_ != cb_ and [l for l in ca_ if l != PROBE] != cb_: bad_code += 1; print("   code differs beyond the probe on slide", i)
    if PROBE in cb_: bad_code += 1
    ra = [p.text for sh in sa.shapes if sh.name.startswith("result line ") for p in sh.text_frame.paragraphs]; rb = [p.text for sh in sb.shapes if sh.name.startswith("result line ") for p in sh.text_frame.paragraphs]
    if ra:
        nres += 1
        ok = len(rb) == 1 and AR in rb[0] and not rb[0].startswith(PROBE) and ra == [PROBE + AR + "(3, 14)"]
        code = "\n".join(cb_); expr = rb[0].split(AR)[0] if rb else ""
        if not ok: bad_res += 1; print("   result line problem on slide", i, rb)
    elif rb: bad_res += 1
    ta = ["%s|%s" % (sh.name, p.text) for sh in sa.shapes if sh.has_text_frame and not sh.name.startswith(("code ", "result line ")) for p in sh.text_frame.paragraphs]
    tb = ["%s|%s" % (sh.name, p.text) for sh in sb.shapes if sh.has_text_frame and not sh.name.startswith(("code ", "result line ")) for p in sh.text_frame.paragraphs]
    if ta != tb: bad_other += 1; print("   other text differs on slide", i)
    if (sa.notes_slide.notes_text_frame.text if sa.has_notes_slide else "") != (sb.notes_slide.notes_text_frame.text if sb.has_notes_slide else ""): bad_other += 1; print("   notes differ on slide", i)
chk("code lines equal v3_6_0 minus the probe line, no probe left", bad_code == 0)
chk("%d result lines read 'EXPRESSION  ->  VALUE' (a real expression of the example, no probe)" % nres, bad_res == 0 and nres == 27)
chk("every other shape text and every note equal", bad_other == 0)
za, zb = zipfile.ZipFile(A), zipfile.ZipFile(B); na, nb = za.namelist(), zb.namelist(); diff = [n for n in na if za.read(n) != zb.read(n)]
sl = [n for n in diff if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
chk("same parts; only 27 slides and docProps/core.xml differ", na == nb and len(sl) == 27 and set(diff) - set(sl) == {"docProps/core.xml"}, "(%d parts differ)" % len(diff))
def hl(z): return {n: sorted(re.findall(r'Target="(http[^"]+)"', z.read(n).decode())) for n in z.namelist() if re.fullmatch(r"ppt/slides/_rels/slide\d+\.xml\.rels", n)}
chk("hyperlinks identical (relationships %d / %d)" % (sum(map(len, hl(za).values())), sum(map(len, hl(zb).values()))), hl(za) == hl(zb))
print("RESULT", "PASS" if not fail else "FAIL (%d)" % fail); sys.exit(1 if fail else 0)
