#!/usr/bin/env python3
"""Proof of the deck v3.5.0 against v3.4.0 (a NEW tool file): the 163 code lines (prompts stripped) equal the new code lines in order; no prompt in any code box or anywhere in the deck;
every old result row stands byte for byte in a result shape directly under its code box; all other slide text and notes equal; differing package parts; hyperlink counts. Usage: deck_proof_v3_5_0.py"""
import os, re, sys, zipfile
from pptx import Presentation
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
A = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx"; B = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_5_0.pptx"
PR = (">>> ", "... ")
fail = 0
def chk(label, ok, extra=""):
    global fail; fail += (not ok); print("%s %s %s" % ("PASS" if ok else "FAIL", label, extra))
pa, pb = Presentation(A), Presentation(B)
oc, orr, nc, nr, other_a, other_b = [], [], [], [], [], []
for i, (sa, sb) in enumerate(zip(pa.slides, pb.slides), 1):
    for sh in sa.shapes:
        if not sh.has_text_frame: continue
        ps = [p.text for p in sh.text_frame.paragraphs]
        if any(t.startswith(PR) for t in ps):
            oc += [(i, t[4:]) for t in ps if t.startswith(PR)]; orr += [(i, t) for t in ps if not t.startswith(PR)]
        else: other_a += ["s%d|%s|%s" % (i, sh.name, t) for t in ps]
    shb = list(sb.shapes)
    for j, sh in enumerate(shb):
        if not sh.has_text_frame: continue
        ps = [p.text for p in sh.text_frame.paragraphs]
        if sh.name.startswith("code "):
            nc += [(i, t) for t in ps]
            # result shape directly under
            nxt = shb[j + 1] if j + 1 < len(shb) else None
            if nxt is not None and nxt.name.startswith("result line ") and nxt.name.split()[-1] == sh.name.split()[-1]:
                nr += [(i, p.text) for p in nxt.text_frame.paragraphs]
                chk("slide %d %s: result shape directly under (gap %d EMU, same left/width)" % (i, sh.name, nxt.top - (sh.top + sh.height)),
                    nxt.top == sh.top + sh.height and nxt.left == sh.left and nxt.width == sh.width)
        elif sh.name.startswith("result line "): pass
        else: other_b += ["s%d|%s|%s" % (i, sh.name, t) for t in ps]
    na = sa.notes_slide.notes_text_frame.text if sa.has_notes_slide else None
    nb = sb.notes_slide.notes_text_frame.text if sb.has_notes_slide else None
    if na != nb: chk("notes of slide %d equal" % i, False)
print("old code lines (prompts stripped):", len(oc), "| new code lines:", len(nc), "| old result rows:", len(orr), "| new result texts:", len(nr))
chk("the %d code lines equal the new code lines, in order (slide and text)" % len(oc), oc == nc)
chk("no code box line starts with '>>> ' or '... '", not any(t.startswith(PR) for _, t in nc))
chk("the result texts equal the old result rows, in order", orr == nr)
chk("every other shape text equals (shape names and texts outside code and result shapes)", other_a == other_b, "%d lines" % len(other_a))
chk("no prompt in any slide text of the new deck", not any(p.text.startswith(PR) for s in pb.slides for sh in s.shapes if sh.has_text_frame for p in sh.text_frame.paragraphs))
za, zb = zipfile.ZipFile(A), zipfile.ZipFile(B)
na_, nb_ = za.namelist(), zb.namelist()
print("package parts only in old:", sorted(set(na_) - set(nb_)), "only in new:", sorted(set(nb_) - set(na_)))
chk("same part order", na_ == nb_)
diff = sorted(n for n in na_ if n in nb_ and za.read(n) != zb.read(n))
print("parts with different bytes:", len(diff))
sl = [n for n in diff if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)]
chk("different parts are 27 slides and docProps/core.xml only", len(sl) == 27 and set(diff) - set(sl) == {"docProps/core.xml"})
def hl(z):
    out = {}
    for n in z.namelist():
        m = re.fullmatch(r"ppt/slides/_rels/slide(\d+)\.xml\.rels", n)
        if m: out[int(m.group(1))] = sorted(re.findall(r'Target="(http[^"]+)"', z.read(n).decode()))
    return out
ha, hb = hl(za), hl(zb)
print("hyperlink relationships old %d new %d, distinct addresses old %d new %d" % (sum(map(len, ha.values())), sum(map(len, hb.values())), len({x for v in ha.values() for x in v}), len({x for v in hb.values() for x in v})))
chk("hyperlinks identical per slide", ha == hb)
print("RESULT", "PASS" if not fail else "FAIL (%d)" % fail); sys.exit(1 if fail else 0)
