#!/usr/bin/env python3
"""Chapter 6 deck v2.2.0 (a NEW tool file). The deck v2.1.0 is read, never written. One change: the native chart of slide 51 (ppt/charts/chart6.xml) shows its data labels
with the number format 0.## (at most two decimals) instead of General, so the five smallest bars (3.125 down to 0.195) carry short labels (3.13, 1.56, 0.78, 0.39, 0.2) that do not overlap.
The plotted values (the cached numbers and the sheet) and the chart type are untouched. The document properties part names version 2.2.0. Every other package part is copied byte for byte.
Usage: deck_derive_v2_2_0.py"""
__version__ = "2.2.0"
import os, re, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_1_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch06/SEN0401_Ch06_Transactions_3e_v2_2_0.pptx")
zi = zipfile.ZipFile(SRC)
assert b"chart6.xml" in zi.read("ppt/slides/_rels/slide51.xml.rels")
with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zo:
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename == "ppt/charts/chart6.xml":
            s = data.decode("utf-8")
            old = '<c:dLbls><c:numFmt formatCode="General" sourceLinked="0"/>'
            assert s.count(old) == 2
            data = s.replace(old, '<c:dLbls><c:numFmt formatCode="0.##" sourceLinked="0"/>').encode("utf-8")
        elif it.filename == "docProps/core.xml":
            s = data.decode("utf-8")
            s = s.replace("<cp:version>2.1.0</cp:version>", "<cp:version>2.2.0</cp:version>")
            s = re.sub(r"(<dcterms:modified[^>]*>)[^<]*", r"\g<1>2026-10-28T14:10:00Z", s)
            data = s.encode("utf-8")
        zo.writestr(it, data)
print("written", DST)
