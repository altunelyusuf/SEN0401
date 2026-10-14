#!/usr/bin/env python3
"""sen0401_deck_structure_check v1.0.0 - port of SEN0414's ch05-deck/structure_check_v1_0_0.py, code unchanged, so that SEN0401 needs nothing from SEN0414's repository. SEN0401's decks (chapters 1-7) were never put through it or through ooxml_fix.
Refuses a deck whose paragraphs are in an order PowerPoint would 'repair': a:pPr not first, a:endParaRPr not last. Usage: structure_check_v1_0_0.py <deck.pptx>"""
__version__ = "1.0.0"
import sys, zipfile, re
from lxml import etree
A = "http://schemas.openxmlformats.org/drawingml/2006/main"; bad = []
with zipfile.ZipFile(sys.argv[1]) as z:
    for n in z.namelist():
        if re.match(r"ppt/(slides|notesSlides)/[^/]+\.xml$", n):
            for p in etree.fromstring(z.read(n)).iter("{%s}p" % A):
                tags = [etree.QName(k).localname for k in p]
                if "pPr" in tags[1:] or ("endParaRPr" in tags and tags.index("endParaRPr") != len(tags) - 1): bad.append((n, tags[:6]))
print("%d paragraph(s) in an order PowerPoint would repair" % len(bad))
for b in bad[:5]: print("  REFUSED", b)
sys.exit(1 if bad else 0)
