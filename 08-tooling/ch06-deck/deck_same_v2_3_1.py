#!/usr/bin/env python3
"""deck_same v2_3_1: compares two decks: per slide the text of every shape (by shape name+order), notes, hyperlinks, picture hashes, shape names, prompt/lambda counts. Prints DIFF lines; geometry and font-size are not compared. Usage: A B"""
import sys, hashlib
sys.dont_write_bytecode = True
from pptx import Presentation
def facts(p):
    out = []
    for i, s in enumerate(p.slides, 1):
        sh = []
        for x in s.shapes:
            t = x.text_frame.text if x.has_text_frame else ""
            h = []
            if x.has_text_frame:
                for pa in x.text_frame.paragraphs:
                    for r in pa.runs:
                        if r.hyperlink.address: h.append(r.hyperlink.address)
            if x.has_text_frame and x.click_action.hyperlink.address: h.append(x.click_action.hyperlink.address)
            pic = hashlib.sha1(x.image.blob).hexdigest() if x.shape_type == 13 else ""
            sh.append((x.name, t, tuple(h), pic))
        n = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        out.append((sh, n))
    return out
a, b = facts(Presentation(sys.argv[1])), facts(Presentation(sys.argv[2])); d = 0
print("slides", len(a), len(b))
for i, (x, y) in enumerate(zip(a, b), 1):
    if x != y: d += 1; print("DIFF slide", i)
la = sum(len(s[2]) for x in a for s in x[0]); lb = sum(len(s[2]) for x in b for s in x[0])
txt = "\n".join(s[1] for x in b for s in x[0])
print("hyperlinks", la, lb, "| prompts", txt.count(">>> "), "| lambda", txt.count("lambda"))
print("SAME" if d == 0 and len(a) == len(b) else "DIFFERENT (%d slides)" % d)
