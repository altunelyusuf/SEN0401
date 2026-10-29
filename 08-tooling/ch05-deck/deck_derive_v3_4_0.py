#!/usr/bin/env python3
"""Chapter 5 deck v3.4.0 and deck plan v3.4.0 (NEW files; the deck v3.3.0 and the plan v3.3.0 are read, never written). ONE kind of change: the closing slide (the last slide, slide68.xml)
gets a dark background and light text in the deck's own palette (dark 23272E and light E6EDF3 of the code panels, muted 8A9B94, accent D97A14 kept); text, notes, shapes, links and every other
package part stay byte for byte; the document-properties title names v3.4.0. The plan v3.4.0 declares the last slide kind closing, bg dark. Usage: deck_derive_v3_4_0.py"""
__version__ = "3.4.0"
import os, re, json, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_3_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx")
PSRC = os.path.join(ROOT, "08-tooling/ch05-deck/deck_plan_v3_3_0.json")
PDST = os.path.join(ROOT, "08-tooling/ch05-deck/deck_plan_v3_4_0.json")
BG, INK, MUTED, CARD = "23272E", "E6EDF3", "8A9B94", "2B3139"
LAST = "ppt/slides/slide68.xml"

def recolour(x):
    n = x.count('<a:srgbClr val="FAF6EF"/>')
    assert n == 1, n
    x = x.replace('<p:bg><p:bgPr><a:solidFill><a:srgbClr val="FAF6EF"/>', '<p:bg><p:bgPr><a:solidFill><a:srgbClr val="%s"/>' % BG)
    # text colours: ink 2B2622 -> light; muted 6E655C -> muted on dark; cards F2ECE1 -> dark card (only shape fills named outcome)
    x = re.sub(r'(<a:rPr[^>]*><a:solidFill><a:srgbClr val=")2B2622(")', r'\g<1>%s\2' % INK, x)
    x = re.sub(r'(<a:rPr[^>]*><a:solidFill><a:srgbClr val=")6E655C(")', r'\g<1>%s\2' % MUTED, x)
    x = x.replace('<a:solidFill><a:srgbClr val="F2ECE1"/></a:solidFill><a:ln><a:solidFill><a:srgbClr val="F2ECE1"/></a:solidFill></a:ln>',
                  '<a:solidFill><a:srgbClr val="%s"/></a:solidFill><a:ln><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % (CARD, CARD))
    return x

zi = zipfile.ZipFile(SRC)
with zipfile.ZipFile(DST, "w") as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename == LAST:
            data = recolour(data.decode("utf-8")).encode("utf-8")
        elif it.filename == "docProps/core.xml":
            s = data.decode("utf-8"); assert "deck v3.3.0" in s
            data = s.replace("deck v3.3.0", "deck v3.4.0").encode("utf-8")
        zo.writestr(it, data, compress_type=it.compress_type)
p = json.load(open(PSRC, encoding="utf-8"))
p["meta"]["version"] = "3.4.0"
last = p["slides"][-1]; assert last["kind"] == "closing"
last["bg"] = "dark"
for i in last["items"]: i["dark"] = True
json.dump(p, open(PDST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("written", DST); print("written", PDST)
