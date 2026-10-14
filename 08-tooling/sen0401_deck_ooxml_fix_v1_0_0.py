#!/usr/bin/env python3
"""sen0401_deck_ooxml_fix v1.0.0 - port of SEN0414's ch05-deck/ooxml_fix_v1_0_0.py, code unchanged. Run on the renderer's raw output, before office_stamp and the checks.
Repairs one structural fault pptxgenjs writes when a paragraph is built from several runs: a paragraph-properties element (a:pPr)
placed after a run. PowerPoint requires it to be the paragraph's first child and opens the file only after 'repair' otherwise.
The later a:pPr elements are dropped (the first one, or none, is kept); nothing else is changed. Usage: ooxml_fix_v1_0_0.py <in.pptx> <out.pptx>"""
__version__ = "1.0.0"
import sys, zipfile, re
from lxml import etree
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
src, dst = sys.argv[1], sys.argv[2]; fixed = 0
with zipfile.ZipFile(src) as zi, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        b = zi.read(it.filename)
        if re.match(r"ppt/(slides|notesSlides)/[^/]+\.xml$", it.filename):
            t = etree.fromstring(b); ch = False
            for p in t.iter("{%s}p" % A):
                kids = list(p)
                for k in kids[1:]:
                    if k.tag == "{%s}pPr" % A: p.remove(k); fixed += 1; ch = True
                if kids and kids[0].tag != "{%s}pPr" % A:
                    for k in list(p):
                        if k.tag == "{%s}pPr" % A: p.remove(k); p.insert(0, k); break
            if ch: b = etree.tostring(t, xml_declaration=True, encoding="UTF-8", standalone=True)
        zo.writestr(it, b)
print("ooxml_fix: %d misplaced paragraph-properties element(s) removed" % fixed)
