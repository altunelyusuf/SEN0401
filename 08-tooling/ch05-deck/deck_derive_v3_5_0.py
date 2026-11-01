#!/usr/bin/env python3
"""Chapter 5 deck v3.5.0 and deck plan v3.5.0 (NEW files; the deck v3.4.0 and the plan v3.4.0 are read, never written).
ONE kind of change: every code box ("code" shape) holds code only (the prompts '>>> ' and '... ' are removed; every code character after the prompt is kept), and the result row(s)
that stood as the last line(s) of the box stand in a separate result shape directly under the code box (same left, same width, no gap), in the deck's own palette
(fill 2F6D62 of the takeaway line, text FFFFFF, same Courier New 10.5 pt). Marker (ST_Code_Gate): a code box is a shape whose name starts with 'code', a result line a shape whose name
starts with 'result' placed directly under its code box. The box and its explanation keep their top; the explanation beside it grows to the height of code box plus result shape.
Every other package part stays byte for byte; docProps/core.xml names v3.5.0. Usage: deck_derive_v3_5_0.py"""
__version__ = "3.5.0"
import os, re, json, zipfile, copy
from lxml import etree
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch05/SEN0401_Ch05_WalletRecovery_3e_v3_5_0.pptx")
PSRC = os.path.join(ROOT, "08-tooling/ch05-deck/deck_plan_v3_4_0.json")
PDST = os.path.join(ROOT, "08-tooling/ch05-deck/deck_plan_v3_5_0.json")
NS = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
A = "{%s}" % NS["a"]; P = "{%s}" % NS["p"]
FILL, INK = "2F6D62", "FFFFFF"
PROMPTS = (">>> ", "... ")
INS = 36576          # code box top and bottom inset (unchanged)
RINS = 18288         # result shape inset

def ptext(p): return "".join(t.text or "" for t in p.iter(A + "t"))

def transform(xml):
    root = etree.fromstring(xml)
    tree = root.find(".//p:cSld/p:spTree", NS)
    sps = tree.findall("p:sp", NS)
    maxid = max(int(e.get("id")) for e in root.iter() if e.tag.endswith("}cNvPr"))
    k = 0
    for sp in list(sps):
        nv = sp.find("p:nvSpPr/p:cNvPr", NS)
        if nv.get("name") != "code": continue
        paras = sp.findall("p:txBody/a:p", NS)
        if not any(ptext(p).startswith(PROMPTS) for p in paras): continue
        k += 1
        nv.set("name", "code %d" % k)
        off = sp.find("p:spPr/a:xfrm/a:off", NS); ext = sp.find("p:spPr/a:xfrm/a:ext", NS)
        top, h, left, w = int(off.get("y")), int(ext.get("cy")), int(off.get("x")), int(ext.get("cx"))
        total = len(paras); res = []
        for p in paras:
            t = ptext(p)
            if t.startswith(PROMPTS):
                assert not res, "code line after a result row"
                r0 = p.find("a:r", NS); assert r0.find("a:t", NS).text in PROMPTS, r0.find("a:t", NS).text
                p.remove(r0)
            else:
                res.append(p)
        if not res: continue
        pl = (h - 2 * INS) / total
        ncode = total - len(res)
        h_code = int(round(ncode * pl + 2 * INS)); h_res = int(round(len(res) * pl + 2 * RINS))
        # result shape: copy of the code shape holding only the result paragraph(s)
        rs = copy.deepcopy(sp)
        for p in rs.findall("p:txBody/a:p", NS): rs.find("p:txBody", NS).remove(p)
        for p in res:
            sp.find("p:txBody", NS).remove(p)
            for rp in p.iter(A + "rPr"):
                for c in rp.findall("a:solidFill", NS): rp.remove(c)
                sf = etree.Element(A + "solidFill"); etree.SubElement(sf, A + "srgbClr").set("val", INK); rp.insert(0, sf)
            rs.find("p:txBody", NS).append(p)
        ext.set("cy", str(h_code))
        maxid += 1
        rnv = rs.find("p:nvSpPr/p:cNvPr", NS); rnv.set("id", str(maxid)); rnv.set("name", "result line %d" % k)
        roff = rs.find("p:spPr/a:xfrm/a:off", NS); rext = rs.find("p:spPr/a:xfrm/a:ext", NS)
        roff.set("y", str(top + h_code)); rext.set("cy", str(h_res))
        sfills = rs.find("p:spPr", NS).findall("a:solidFill", NS)
        sfills[0].find("a:srgbClr", NS).set("val", FILL)
        ln = rs.find("p:spPr/a:ln/a:solidFill/a:srgbClr", NS); ln.set("val", FILL)
        bp = rs.find("p:txBody/a:bodyPr", NS); bp.set("tIns", str(RINS)); bp.set("bIns", str(RINS))
        sp.addnext(rs)
        # the explanation beside this code box grows to code box plus result shape
        grow = h_code + h_res - h
        for other in sps:
            n2 = other.find("p:nvSpPr/p:cNvPr", NS).get("name")
            if n2 == "explanation":
                o = other.find("p:spPr/a:xfrm/a:off", NS); e = other.find("p:spPr/a:xfrm/a:ext", NS)
                if int(o.get("y")) == top and int(e.get("cy")) == h:
                    e.set("cy", str(h + grow))
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True), k

if __name__ == "__main__":
    zi = zipfile.ZipFile(SRC); changed = 0; boxes = 0
    with zipfile.ZipFile(DST, "w") as zo:
        for it in zi.infolist():
            data = zi.read(it.filename)
            if re.fullmatch(r"ppt/slides/slide\d+\.xml", it.filename) and b"&gt;&gt;&gt; " in data:
                data, k = transform(data); changed += 1; boxes += k
            elif it.filename == "docProps/core.xml":
                s = data.decode("utf-8"); assert "deck v3.4.0" in s
                data = s.replace("deck v3.4.0", "deck v3.5.0").encode("utf-8")
            zo.writestr(it, data, compress_type=it.compress_type)
    p = json.load(open(PSRC, encoding="utf-8")); p["meta"]["version"] = "3.5.0"
    json.dump(p, open(PDST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("slides changed %d, code boxes %d" % (changed, boxes)); print("written", DST); print("written", PDST)
