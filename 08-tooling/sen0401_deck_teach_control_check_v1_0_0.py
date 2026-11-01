#!/usr/bin/env python3
"""sen0401_deck_teach_control_check v1_0_0 - control of the chapter 5 Teach repair deck v3_7_0 against v3_6_0: the only differences are the removed version probe (27 code boxes and 27 result rows, 54 occurrences), no probe left, 0 prompts, 0 lambdas, 0 label shapes, layout clean, notes unchanged. Usage: run"""
import subprocess, sys, re, os
from pptx import Presentation
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(H, "..", "03-materials", "ch05"); OLD = os.path.join(D, "SEN0401_Ch05_WalletRecovery_3e_v3_6_0.pptx"); NEW = os.path.join(D, "SEN0401_Ch05_WalletRecovery_3e_v3_7_0.pptx")
res = []
def chk(ok, m): res.append(ok); print("PASS " if ok else "FAIL ", m)
def sh(f):
    o = []
    for n, s in enumerate(Presentation(f).slides, 1):
        for x in s.shapes:
            if x.has_text_frame: o.append((n, x.name, x.text_frame.text))
    return o
a, b = sh(OLD), sh(NEW)
def probes(l): return sum(t.count("__import__") for _, _, t in l)
chk(probes(a) == 54 and probes(b) == 0, "probe occurrences old %d, new %d" % (probes(a), probes(b)))
def noprobe(l): return [(n, nm, "\n".join(x for x in t.split("\n") if "__import__" not in x and "version_info" not in x)) for n, nm, t in l if "__import__" not in t or t.replace("\n", "").strip()]
ob = {(n, nm) for n, nm, t in a if "__import__" in t and nm.startswith("result line")}
rest_old = [t for n, nm, t in a if "__import__" not in t and not nm.startswith("slide number")]; rest_new = [t for n, nm, t in b if not nm.startswith("slide number")]
miss = [t for t in rest_old if t not in rest_new]
chk(not miss, "every shape of the old deck without the probe is on the new deck (missing %d)" % len(miss))
o = lambda k: subprocess.run([sys.executable, os.path.join(H, "sen0401_deck_%s_check_v1_0_0.py" % k), NEW], capture_output=True, text=True).stdout
chk("prompt_rows=0" in o("prompt"), "0 prompts"); chk("code_lines_with_lambda=0" in o("lambda"), "0 lambdas"); chk("label_shapes=0" in o("label_words"), "0 label shapes")
na = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else "" for s in Presentation(OLD).slides]; nb = [s.notes_slide.notes_text_frame.text if s.has_notes_slide else "" for s in Presentation(NEW).slides]
chk(na == nb, "notes of all %d slides unchanged" % len(na))
print("RESULT", "PASS" if all(res) else "FAIL"); sys.exit(0 if all(res) else 1)
