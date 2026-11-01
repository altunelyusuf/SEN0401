#!/usr/bin/env python3
"""sen0401_deck_size_control_check v1_0_0 - the lineage agent's control of a deck whose only change is the type size: the old deck equals its committed blob; slide count, slide order, every slide's text, notes, shape names, code and result texts and hyperlinks are equal old to new; no text run of the new deck is below 9 pt (the smallest size is printed); layout check clean; notes check PASS. Usage: deck_size_control_check OLD.pptx NEW.pptx REF   (REF = the commit before the executor's first commit)"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
from pptx import Presentation
old, new, ref = sys.argv[1:4]; fails = 0
def out(ok, msg):
    global fails; fails += (not ok); print(("PASS  " if ok else "FAIL  ") + msg)
A, B = Presentation(old), Presentation(new)
blob = subprocess.run(["git", "show", "%s:%s" % (ref, os.path.relpath(old))], capture_output=True).stdout
out(hashlib.sha256(blob).hexdigest() == hashlib.sha256(open(old, "rb").read()).hexdigest(), "old deck equals its committed blob at %s" % ref)
out(len(A.slides) == len(B.slides), "slide count %d -> %d" % (len(A.slides), len(B.slides)))
txt = lambda s: [(sh.name, sh.text_frame.text) for sh in s.shapes if sh.has_text_frame]
nt = lambda s: s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
hl = lambda s: sorted(r.target_ref for r in s.part.rels.values() if r.is_external)
dt = dn = dh = ds = 0
for a, b in zip(A.slides, B.slides):
    dt += (txt(a) != txt(b)); dn += (nt(a) != nt(b)); dh += (hl(a) != hl(b)); ds += ([sh.name for sh in a.shapes] != [sh.name for sh in b.shapes])
out(dt == 0, "slides whose text (shape names and texts) differs: %d" % dt)
out(ds == 0, "slides whose shape names differ: %d" % ds)
out(dn == 0, "slides whose notes differ: %d" % dn)
out(dh == 0, "slides whose hyperlinks differ: %d" % dh)
sz = [(int(z) / 100, i) for i, s in enumerate(B.slides, 1) for sh in s.shapes if sh.has_text_frame for pa in sh.text_frame.paragraphs for r in pa.runs if r.text.strip() for z in ([r.font.size.pt * 100] if r.font.size else [])]
small = [x for x in sz if x[0] < 9]
out(not small, "text runs below 9 pt: %d; smallest size %s pt over %d sized runs" % (len(small), min(x[0] for x in sz) if sz else "-", len(sz)))
d = os.path.dirname(os.path.abspath(__file__))
r = subprocess.run([sys.executable, os.path.join(d, "deck_layout_check_v1_0_0.py"), new], capture_output=True, text=True).stdout
out("RESULT: clean" in r, "layout check: " + [l.strip() for l in r.splitlines() if "RESULT" in l or "outside" in l][-1])
r = subprocess.run([sys.executable, os.path.join(d, "deck_notes_check_v1_0_0.py"), new], capture_output=True, text=True).stdout
out("VERDICT: PASS" in r, "notes check: " + r.strip().splitlines()[-1].strip())
print("RESULT", "FAIL" if fails else "PASS"); sys.exit(1 if fails else 0)
