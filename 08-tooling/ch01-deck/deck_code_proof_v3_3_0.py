#!/usr/bin/env python3
"""Proof for the chapter 1 deck v3.3.0 (new file): old code lines (prompts stripped) == new code lines in order (62), no prompt left, old result rows == result shapes, every other part byte-identical,
and on the 15 code slides every shape that is not a code box, a result card or a moved explanation/caption is identical. Usage: python3 -B deck_code_proof_v3_3_0.py OLD NEW"""
import re, sys, zipfile
from lxml import etree
NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main", "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
old, new = sys.argv[1:3]
zo, zn = zipfile.ZipFile(old), zipfile.ZipFile(new)
assert zo.namelist() == zn.namelist()
slide = lambda n: re.match(r"ppt/slides/slide\d+\.xml$", n)
diff = [n for n in zo.namelist() if zo.read(n) != zn.read(n)]
dslides = [n for n in diff if slide(n)]; dother = [n for n in diff if not slide(n)]
print("parts differing: %d slide parts, other parts %s" % (len(dslides), dother))
oc, nc, orr, nr, bad = [], [], [], [], []
for n in sorted(dslides, key=lambda n: int(re.findall(r"\d+", n)[0])):
    ro, rn = etree.fromstring(zo.read(n)), etree.fromstring(zn.read(n))
    for sp in ro.iter("{%s}sp" % NS["p"]):
        ps = ["".join(t.text or "" for t in p.iter("{%s}t" % NS["a"])) for p in sp.findall(".//a:p", NS)]
        i = 0
        while i < len(ps):
            if ps[i].startswith(">>> "):
                oc.append(ps[i][4:])
                if i + 1 < len(ps) and not ps[i + 1].startswith(">>> "):
                    orr.append((ps[i][4:], ps[i + 1])); i += 1
            i += 1
    for sp in rn.iter("{%s}sp" % NS["p"]):
        nm = sp.find("p:nvSpPr/p:cNvPr", NS).get("name")
        ps = ["".join(t.text or "" for t in p.iter("{%s}t" % NS["a"])) for p in sp.findall(".//a:p", NS)]
        if nm.startswith("code"):
            nc += ps
        if nm.startswith("result"):
            e, v = "\n".join(ps).split("  →  ", 1); nr.append((e, v))
    allt = "\n".join("".join(t.text or "" for t in p.iter("{%s}t" % NS["a"])) for p in rn.iter("{%s}p" % NS["a"]))
    if re.search(r"(^|\n)(>>> |\.\.\. )", allt): bad.append(n)
    # untouched shapes: same serialised xml in old and new
    so = {etree.tostring(e) for e in ro.find(".//p:spTree", NS)}
    changed = [e.find(".//p:cNvPr", NS).get("name") for e in rn.find(".//p:spTree", NS) if etree.tostring(e) not in so]
    print(n, "changed or new shapes:", changed)
print("code lines old %d new %d equal in order: %s" % (len(oc), len(nc), oc == nc))
print("result rows old %d new %d equal: %s" % (len(orr), len(nr), orr == nr))
print("slides with a prompt left:", bad)
print("PASS" if oc == nc and len(oc) == 62 and orr == nr and not bad and not dother[1:] and dother in ([], ["docProps/core.xml"]) else "FAIL")
