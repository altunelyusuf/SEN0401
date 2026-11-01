#!/usr/bin/env python3
"""sen0401_deck_minfont_check v1_0_0 - no text run of the deck is below 9 pt; prints the smallest size, the sized runs, and the runs below 9 pt per slide. Usage: deck_minfont_check DECK. Exit 0 when none is below 9 pt."""
__version__ = "1.0.0"
import sys
from pptx import Presentation
p = Presentation(sys.argv[1]); low = []; n = 0; mn = 99
for i, s in enumerate(p.slides, 1):
    for sh in s.shapes:
        if sh.has_text_frame:
            for pa in sh.text_frame.paragraphs:
                for r in pa.runs:
                    if r.text.strip() and r.font.size:
                        n += 1; mn = min(mn, r.font.size.pt)
                        if r.font.size.pt < 9: low.append((i, r.font.size.pt))
print("smallest size %s pt over %d sized runs; runs below 9 pt: %d %s" % (mn, n, len(low), low[:10]))
print("RESULT", "FAIL" if low else "PASS"); sys.exit(1 if low else 0)
