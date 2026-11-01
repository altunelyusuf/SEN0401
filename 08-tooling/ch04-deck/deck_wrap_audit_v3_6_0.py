#!/usr/bin/env python3
"""deck_wrap_audit v3.6.0 (a NEW tool file; task TK_Ch04_DeckTeach_Build): measures with real font metrics (Carlito = Calibri metrics, Liberation Mono = Courier New metrics) how many lines every text shape of a deck sets,
word-wrapping inside the shape's width minus its margins. Categories: code (name 'code ...'), result (name 'result ...'), caption (text begins 'Picture:' or 'Figure' or 'Photo' or 'Source'), stamp (begins 'run under'), read (begins 'READ'),
title (name TextBox 2 or left 125), other. Prints every shape of the categories code, result, caption, stamp, read, title that sets more than one line, and a count per category; 'other' shapes are listed only with --all.
Usage: python3 -B deck_wrap_audit_v3_6_0.py DECK [--all]    Exit 0 when no code, result, caption, stamp or read shape sets more than one line."""
import re, sys
sys.dont_write_bytecode = True
from PIL import ImageFont
from pptx import Presentation
FONTS = {}
def font(face, bold, size):
    key = (face, bold, size)
    if key not in FONTS:
        if face == "Courier New": path = "/usr/share/fonts/truetype/liberation/LiberationMono-%s.ttf" % ("Bold" if bold else "Regular")
        else: path = "/usr/share/fonts/truetype/crosextra/Carlito-%s.ttf" % ("Bold" if bold else "Regular")
        FONTS[key] = ImageFont.truetype(path, int(round(size * 20)))
    return FONTS[key]
def width_pt(text, face, bold, size): return font(face, bold, size).getlength(text) / 20.0
def para_lines(pa, avail):
    """lines of one paragraph (a:br starts a new line); words are kept whole"""
    segs = [[]]
    for ch in pa._p:
        tag = ch.tag.split("}")[1]
        if tag == "br": segs.append([])
        elif tag == "r":
            rpr = ch.find("{http://schemas.openxmlformats.org/drawingml/2006/main}rPr"); sz = float(rpr.get("sz", "1300")) / 100 if rpr is not None else 13.0
            bold = rpr is not None and rpr.get("b") == "1"
            lat = rpr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}latin") if rpr is not None else None
            face = lat.get("typeface") if lat is not None else "Calibri"
            t = "".join(x.text or "" for x in ch.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))
            segs[-1].append((t, face, bold, sz))
    n = 0; wmax = 0.0
    for seg in segs:
        words = []
        for t, face, bold, sz in seg:
            for w in re.findall(r"\S+\s*", t): words.append((w, face, bold, sz))
        line = 0.0; cnt = 1
        for w, face, bold, sz in words:
            ww = width_pt(w.rstrip(), face, bold, sz); wfull = width_pt(w, face, bold, sz)
            if line + ww > avail and line > 0: cnt += 1; line = 0.0
            line += wfull; wmax = max(wmax, line)
        n += cnt
    return n, wmax
def shape_lines(sh):
    tf = sh.text_frame
    avail = (sh.width - tf.margin_left - tf.margin_right) / 12700.0
    return sum(para_lines(pa, avail)[0] for pa in tf.paragraphs), avail
def cat(sh):
    t = sh.text_frame.text.strip()
    if sh.name.startswith("code "): return "code"
    if sh.name.startswith("result "): return "result"
    if re.match(r"(Picture|Figure|Photo|Source)\b", t): return "caption"
    if t.startswith("run under"): return "stamp"
    if t.startswith("READ"): return "read"
    if round(sh.left / 9144) == 125 and sh.top / 9144 < 40: return "title"
    return "other"
def main(path, show_all=False):
    prs = Presentation(path); counts = {}; bad = 0
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if not (sh.has_text_frame and sh.text_frame.text.strip()): continue
            c = cat(sh); n, avail = shape_lines(sh); one = n <= max(1, len(sh.text_frame.paragraphs))
            # one line per paragraph is the aim; the shapes of these categories are single-paragraph or one line per paragraph
            paras = len(sh.text_frame.paragraphs); wrapped = n > paras
            counts.setdefault(c, [0, 0]); counts[c][0] += 1; counts[c][1] += 1 if wrapped else 0
            if wrapped and (c != "other" or show_all):
                print("slide %d %s [%s] sets %d lines in %d paragraph(s), width %.0f pt: %s" % (i, sh.name, c, n, paras, avail, sh.text_frame.text.strip()[:70].replace("\n", " | ")))
                if c in ("code", "result", "caption", "stamp", "read"): bad += 1
    print("per category (shapes, wrapped):", {k: tuple(v) for k, v in sorted(counts.items())})
    print("wrapped code/result/caption/stamp/read shapes: %d" % bad)
    return 0 if bad == 0 else 1
if __name__ == "__main__":
    sys.exit(main(sys.argv[1], "--all" in sys.argv))
