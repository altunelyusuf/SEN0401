#!/usr/bin/env python3
"""Proof for the chapter 1 deck v3.4.0 (new file): on the 15 code slides every shape named code*/result* keeps its name, text and font size, and every other shape of those slides is unchanged except the slide number;
the code lines (62) and result rows (15) are equal in order; smallest font size and wrapped-line count of all code and result shapes (Courier New, 0.6 of the size per character); hyperlink counts.
Usage: python3 -B deck_teach_proof_v3_4_0.py OLD NEW"""
import re, sys, zipfile
from pptx import Presentation
old, new = sys.argv[1:3]
po, pn = Presentation(old), Presentation(new)
def codeshapes(p):
    out = []
    for i, s in enumerate(p.slides, 1):
        for sh in s.shapes:
            if sh.name.startswith(("code ", "result ")): out.append((sh.name, sh.text_frame.text, tuple(sorted({r.font.size.pt for pa in sh.text_frame.paragraphs for r in pa.runs}))))
    return out
a, b = codeshapes(po), codeshapes(pn)
lines = lambda L: [l for n, t, _ in L if n.startswith("code ") for l in t.split("\n")]
print("code and result shapes old %d new %d; identical name, text, size, in order: %s" % (len(a), len(b), a == b))
print("code lines old %d new %d equal: %s" % (len(lines(a)), len(lines(b)), lines(a) == lines(b)))
print("result rows old %d new %d equal: %s" % (sum(n.startswith("result ") for n, _, _ in a), sum(n.startswith("result ") for n, _, _ in b), [t for n, t, _ in a if n.startswith("result ")] == [t for n, t, _ in b if n.startswith("result ")]))
print("prompt rows left:", sum(1 for l in lines(b) if l.startswith((">>>", "..."))))
sizes = set(); wrapped = []; U = 12700
for i, s in enumerate(pn.slides, 1):
    for sh in s.shapes:
        if sh.name.startswith(("code ", "result ")):
            room = (sh.width - sh.text_frame.margin_left - sh.text_frame.margin_right) / U
            for pa in sh.text_frame.paragraphs:
                szs = [r.font.size.pt for r in pa.runs if r.font.size]; sizes |= set(szs); sz = min(szs)
                txt = "".join(r.text for r in pa.runs)
                if len(txt) > int(room / (sz * 0.6)): wrapped.append((i, sh.name, len(txt)))
print("smallest font size of code and result shapes: %.1f pt; sizes present %s; wrapped lines (room / (0.6 x size)): %d %s" % (min(sizes), sorted(sizes), len(wrapped), wrapped))
def code_slide_text(p):
    out = []
    for s in p.slides:
        if any(sh.name.startswith("code ") for sh in s.shapes):
            out.append([(sh.name, sh.left, sh.top, sh.width, sh.height, re.sub(r"\d+ / \d+", "N", sh.text_frame.text) if sh.has_text_frame else "") for sh in s.shapes])
    return out
co, cn = code_slide_text(po), code_slide_text(pn); moved = 0
for x, y in zip(co, cn):
    dx = {n: g for n, *g in x}; dy = {n: g for n, *g in y}
    moved += sum(1 for n in dx if n in dy and dx[n] != dy[n])
print("15 code slides: %d / %d; shapes with changed geometry or text (incl. the one result widened on the Pizza slide): %d" % (len(co), len(cn), moved))
def links(path):
    z = zipfile.ZipFile(path); sl = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    h = sum(z.read(n).count(b"hlinkClick") for n in sl)
    e = sum(z.read(n).count(b'TargetMode="External"') for n in z.namelist() if n.startswith("ppt/slides/_rels/"))
    return h, e
print("hyperlinks old (hlinkClick, external rels):", links(old), "new:", links(new))
