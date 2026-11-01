#!/usr/bin/env python3
"""Proof for the chapter 3 deck v3.2.0 (a NEW tool file; task TK_Ch03_DeckTeach_Build) against v3.1.0:
(1) SHA-256 of both decks; (2) every shape named code* keeps its name, text and size, in order (64 code lines); (3) every shape named result* keeps its name and its text (19), and none is below 10 pt;
(4) the smallest font size of every slide over ALL text runs (text boxes, shapes, table cells) and over the chart fonts; (5) the wrapped-line count of every code and result shape (Courier New, 0.6 of the size per character, room = box width minus margins,
a line break inside a paragraph starts a new line); (6) the hyperlink count; (7) the geometry of slide 24 (the gap between the code card and the result card).
Usage: python3 -B deck_teach_proof_v3_2_0.py OLD NEW   Exit 0 only when every statement holds."""
import hashlib, re, sys, zipfile
sys.dont_write_bytecode = True
from pptx import Presentation
old, new = sys.argv[1:3]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ok = True
def say(k, v, good=True):
    global ok; ok &= good; print(("PASS " if good else "FAIL ") + k + " | " + str(v))
po, pn = Presentation(old), Presentation(new)
say("old deck SHA-256", sha(old)); say("new deck SHA-256", sha(new))
def shapes(p, prefix):
    out = []
    for i, s in enumerate(p.slides, 1):
        for sh in s.shapes:
            if sh.name.startswith(prefix) and sh.has_text_frame:
                out.append((sh.name, sh.text_frame.text, tuple(sorted({r.font.size.pt for pa in sh.text_frame.paragraphs for r in pa.runs if r.font.size})), i, sh))
    return out
co, cn = shapes(po, "code "), shapes(pn, "code ")
say("code shapes: names, texts and sizes equal, in order", "%d vs %d" % (len(co), len(cn)), [x[:3] for x in co] == [x[:3] for x in cn])
lines = lambda L: [l for n, t, _, _, _ in L for l in t.split("\n")]
say("code lines old == new, in order", "%d vs %d" % (len(lines(co)), len(lines(cn))), lines(co) == lines(cn) and len(lines(co)) == 64)
say("no code line starts with '>>>' or '...'", sum(1 for l in lines(cn) if l.startswith((">>>", "..."))), not any(l.startswith((">>>", "...")) for l in lines(cn)))
ro, rn = shapes(po, "result "), shapes(pn, "result ")
say("result shapes: names and texts equal, in order", "%d vs %d" % (len(ro), len(rn)), [(n, t) for n, t, _, _, _ in ro] == [(n, t) for n, t, _, _, _ in rn] and len(ro) == 19)
small = [(i, n, s) for n, t, s, i, _ in rn if min(s) < 10]
say("every result shape at 10 pt or more", "smallest %.1f pt; below 10 pt: %s" % (min(min(s) for _, _, s, _, _ in rn), small or "none"), not small)
say("old result sizes (for the record)", sorted({x for _, _, s, _, _ in ro for x in s}))
# (4) smallest size per slide
def runs(sl):
    out = []
    for sh in sl.shapes:
        tfs = []
        if sh.has_text_frame: tfs.append(sh.text_frame)
        if getattr(sh, "has_table", False) and sh.has_table: tfs += [c.text_frame for r in sh.table.rows for c in r.cells]
        for tf in tfs:
            for pa in tf.paragraphs:
                for r in pa.runs:
                    out.append((r.font.size.pt if r.font.size is not None else None, sh.name, r.text[:30]))
    for rel in sl.part.rels.values():
        if "chart" in rel.reltype:
            for m in re.findall(r'sz="(\d+)"', rel.target_part.blob.decode("utf8")): out.append((int(m) / 100.0, "chart", ""))
    return out
below = []; nosize = []; per = []
for i, s in enumerate(pn.slides, 1):
    rs = runs(s); sizes = [x[0] for x in rs if x[0] is not None]
    nosize += [(i,) + x[1:] for x in rs if x[0] is None and x[2].strip()]
    below += [(i,) + x for x in rs if x[0] is not None and x[0] < 9.0]
    per.append((i, min(sizes) if sizes else None))
say("runs below 9 pt in the whole deck (text boxes, shapes, table cells, chart fonts)", "%d %s" % (len(below), below[:5]), not below)
say("runs without an explicit size (not counted above)", len(nosize), True)
for i, m in per: print("slide %d smallest run %s pt" % (i, "%.1f" % m if m else "none"))
print("smallest run of the whole deck: %.1f pt on slides %s" % (min(m for _, m in per if m), [i for i, m in per if m == min(m for _, m in per if m)]))
# (5) wrapped lines of code and result shapes
wrapped = []; U = 12700; sizes = set()
for n, t, s, i, sh in cn + rn:
    room = (sh.width - sh.text_frame.margin_left - sh.text_frame.margin_right) / U
    for pa in sh.text_frame.paragraphs:
        szs = [r.font.size.pt for r in pa.runs if r.font.size]
        if not szs: continue
        sz = min(szs); sizes.add(sz)
        for ln in pa._p.xpath("string(.)").split("\n") if False else ["".join(x.text for x in seg) for seg in _split(pa)] if False else [None]: pass
        # a:br splits a paragraph into lines
        segs = [[]]
        for ch in pa._p:
            tag = ch.tag.split("}")[1]
            if tag == "br": segs.append([])
            elif tag == "r": segs[-1].append("".join(x.text or "" for x in ch.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t")))
        for seg in segs:
            txt = "".join(seg)
            if len(txt) > int(room / (sz * 0.6)): wrapped.append((i, n, len(txt), int(room / (sz * 0.6))))
say("wrapped lines of code and result shapes (room / (0.6 x size) per line, line breaks honoured)", "%d %s; sizes present %s; smallest %.1f pt" % (len(wrapped), wrapped, sorted(sizes), min(sizes)), not wrapped)
# (6) hyperlinks
def links(path):
    z = zipfile.ZipFile(path); sl = [n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)]
    return sum(z.read(n).count(b"hlinkClick") for n in sl), sum(z.read(n).count(b'TargetMode="External"') for n in z.namelist() if n.startswith("ppt/slides/_rels/"))
lo, ln_ = links(old), links(new)
say("hyperlinks (hlinkClick, external relationships) old vs new", "%s vs %s" % (lo, ln_), ln_[0] >= lo[0] and ln_[1] >= lo[1])
# (7) slide 24
def g24(p):
    s = p.slides[23] if p is po else None
    return s
s_old = po.slides[23]; s_new = [s for s in pn.slides if any(sh.name == "code 2" and "json.loads(T.REPLY)" in sh.text_frame.text for sh in s.shapes)][0]
def gap(s):
    c = [sh for sh in s.shapes if sh.name == "code 2"][0]; r = [sh for sh in s.shapes if sh.name == "result 2"][0]
    back = [sh for sh in s.shapes if sh.name == "output backdrop"]
    cont = sorted([sh for sh in s.shapes if sh.shape_type == 1 and sh.name != "output backdrop" and sh.top <= c.top and sh.top + sh.height >= c.top + c.height], key=lambda x: x.height)
    cardbottom = (cont[0].top + cont[0].height) / 914400.0
    return (c.top + c.height) / 914400.0, r.top / 914400.0, (r.top - c.top - c.height) / 914400.0, cardbottom, (back[0].top / 914400.0 if back else None)
a, b, g, ca, ba = gap(s_old); c, d, h, cb, bb = gap(s_new)
say("slide 24 text gap before: code ends %.2f in, result text at %.2f in, gap %.2f in (old code card ends %.2f in, the result lies inside it); after: code ends %.2f in, result text at %.2f in, gap %.2f in; code card ends %.2f in, result card starts %.2f in, card gap %.2f in" % (a, b, g, ca, c, d, h, cb, bb, bb - cb), "", h < g and bb - cb < 0.15)
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
