#!/usr/bin/env python3
"""Proof of the deck v3.6.0 against v3.5.0 (a NEW tool file): code lines equal except the four named slides (11, 45, 54, 60), shape names, results (old row after the arrow), every other slide text equal except the named
slides and the story cards, notes (none over 80 words, all replaced), differing package parts, media/charts byte-identical, hyperlinks. Usage: deck_proof_v3_6_0.py"""
import os, re, sys, zipfile, difflib
from pptx import Presentation
R = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
A = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_5_0.pptx"; B = R + "/03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_6_0.pptx"
fail = 0
def chk(label, ok, extra=""):
    global fail; fail += (not ok); print("%s %s %s" % ("PASS" if ok else "FAIL", label, extra))
pa, pb = Presentation(A), Presentation(B)
def shapes(sl): return [sh for sh in sl.shapes]
code_a, code_b, res_a, res_b, names_a, names_b = {}, {}, {}, {}, [], []
other_diff = []
for i, (sa, sb) in enumerate(zip(pa.slides, pb.slides), 1):
    ca = [p.text for sh in shapes(sa) if sh.name.startswith("code ") for p in sh.text_frame.paragraphs]
    cb = [p.text for sh in shapes(sb) if sh.name.startswith("code ") for p in sh.text_frame.paragraphs]
    code_a[i], code_b[i] = ca, cb
    res_a[i] = [p.text for sh in shapes(sa) if sh.name.startswith("result line ") for p in sh.text_frame.paragraphs]
    res_b[i] = [p.text for sh in shapes(sb) if sh.name.startswith("result line ") for p in sh.text_frame.paragraphs]
    names_a.append([sh.name for sh in shapes(sa) if sh.name.startswith(("code ", "result line "))]); names_b.append([sh.name for sh in shapes(sb) if sh.name.startswith(("code ", "result line "))])
    ta = ["%s|%s" % (sh.name, p.text) for sh in shapes(sa) if sh.has_text_frame and not sh.name.startswith(("code ", "result line ", "5N1K")) for p in sh.text_frame.paragraphs]
    tb = ["%s|%s" % (sh.name, p.text) for sh in shapes(sb) if sh.has_text_frame and not sh.name.startswith(("code ", "result line ", "story")) for p in sh.text_frame.paragraphs]
    if ta != tb: other_diff.append(i)
changed_code = [i for i in code_a if code_a[i] != code_b[i]]
print("slides whose code lines differ:", changed_code)
chk("code lines equal on every slide except 11, 45, 54, 60", changed_code == [11, 45, 54, 60])
for i in changed_code:
    for l in difflib.unified_diff(code_a[i], code_b[i], lineterm="", n=0):
        if not l.startswith(("---", "+++", "@@")): print("   slide %d %s" % (i, l))
chk("code and result shape names unchanged", names_a == names_b)
chk("each result line is 'EXPRESSION  ->  old result row'", all(res_b[i] == ['__import__("sys").version_info[:2]  →  ' + res_a[i][0]] for i in res_a if res_a[i]) and all(bool(res_a[i]) == bool(res_b[i]) for i in res_a))
print("slides with a result line: %d" % sum(1 for i in res_a if res_a[i]))
print("other slide text differs on slides:", other_diff)
READ = {11, 17, 18, 25, 26, 27, 28, 34, 35, 37, 38, 45, 46, 47, 49, 54, 58, 60, 62}
chk("text outside code and results differs exactly on slides 2, 5, 20, 56 (counter label, stories) and the 19 new readings", other_diff == sorted({2, 5, 20, 56} | READ))
za, zb = zipfile.ZipFile(A), zipfile.ZipFile(B); na, nb = za.namelist(), zb.namelist()
chk("same part list and order", na == nb)
diff = [n for n in na if za.read(n) != zb.read(n)]
kinds = {"slides": [n for n in diff if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)], "notes": [n for n in diff if n.startswith("ppt/notesSlides/")], "other": [n for n in diff if not n.startswith(("ppt/slides/slide", "ppt/notesSlides/"))]}
print("parts differing: slides %d, notes %d, other %s" % (len(kinds["slides"]), len(kinds["notes"]), kinds["other"]))
chk("only slides, notes and docProps/core.xml differ (media, charts, rels, layouts byte-identical)", kinds["other"] == ["docProps/core.xml"])
words = [len((s.notes_slide.notes_text_frame.text if s.has_notes_slide else "").split()) for s in pb.slides]
chk("notes: 68 slides, none over 80 words", len(words) == 68 and max(words) <= 80, "(min %d, max %d, mean %.1f)" % (min(words), max(words), sum(words) / 68))
chk("every note replaced", all((a.notes_slide.notes_text_frame.text != b.notes_slide.notes_text_frame.text) for a, b in zip(pa.slides, pb.slides)))
def hl(z):
    out = {}
    for n in z.namelist():
        m = re.fullmatch(r"ppt/slides/_rels/slide(\d+)\.xml\.rels", n)
        if m: out[int(m.group(1))] = sorted(re.findall(r'Target="(http[^"]+)"', z.read(n).decode()))
    return out
ha, hb = hl(za), hl(zb)
print("hyperlink relationships old %d new %d, distinct %d / %d" % (sum(map(len, ha.values())), sum(map(len, hb.values())), len({x for v in ha.values() for x in v}), len({x for v in hb.values() for x in v})))
chk("hyperlinks identical per slide", ha == hb)
chk("picture count equal", sum(1 for s in pa.slides for sh in s.shapes if sh.shape_type == 13) == sum(1 for s in pb.slides for sh in s.shapes if sh.shape_type == 13))
print("RESULT", "PASS" if not fail else "FAIL (%d)" % fail); sys.exit(1 if fail else 0)
