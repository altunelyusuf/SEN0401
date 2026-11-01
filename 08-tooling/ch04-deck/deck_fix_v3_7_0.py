#!/usr/bin/env python3
"""Ch04 deck v3.7.0 (a NEW tool file; task TK_Ch04_DeckTeach_Build, defect from the control of v3.6.0): on slide 13 the shape 'code head' only held a heading and the two lines of 'secrets card text' were neither a code box nor a result.
The heading is renamed 'draw head', the two lines and their card are removed, and the sentence below says in words what they did. Nothing else changes. Usage: deck_fix_v3_7_0.py OLD(v3.6.0) NEW(v3.7.0)"""
import hashlib, sys
sys.dont_write_bytecode = True
from pptx import Presentation
old, new = sys.argv[1:3]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
b = sha(old); print("SHA-256 v3.6.0 before:", b)
prs = Presentation(old); s = prs.slides[12]
for sh in list(s.shapes):
    if sh.name == "code head": sh.name = "draw head"; r = sh.text_frame.paragraphs[0].runs[0]; r.text = "How a key is drawn"
    elif sh.name in ("secrets card", "secrets card text"): sh._element.getparent().remove(sh._element)
rd = [sh for sh in s.shapes if sh.name == "reading" and sh.text_frame.text.startswith("randbelow")][0]
rd.text_frame.paragraphs[0].runs[0].text = "The secrets module draws the number: randbelow(m) gives 0 to m - 1, so adding 1 gives 1 to n - 1, the range of a private key."
head = [sh for sh in s.shapes if sh.name == "draw head"][0]; rd.top = head.top + head.height + 4
for r in rd.text_frame.paragraphs[0].runs: r.font.italic = False
rd.height = int(60 * 9144)
prs.save(new); print("SHA-256 v3.6.0 after: ", sha(old), "UNCHANGED" if sha(old) == b else "CHANGED"); print("wrote", new, sha(new))
