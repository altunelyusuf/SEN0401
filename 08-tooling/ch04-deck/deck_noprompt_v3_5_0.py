#!/usr/bin/env python3
"""Chapter 4 deck 3.5.0 (task TK_Ch04_DeckCode_Build) over deck 3.4.0. Every code box holds code only (no '>>> ', no '... ') and is named 'code k'; the result of each example stands in its own
shape named 'result k' ('EXPRESSION  ->  VALUE', the marker of sen0401_code_marker_v1_0_0.py), in the deck's own palette at 10 pt, under the code box when the whole row fits ONE line of the
5.4 inch column (64 characters of Courier New 10 pt); a longer row gets the FULL content width (9 inch, x 0.5 to 9.5) in a band of its own above the footer, on one line, 10 pt, no expression
shortened; the left column closes the line the result leaves. Added rule of the owner (2026-11-01): no text run below 9 pt anywhere - the picture credits (8.5 pt) and the native charts' text (8 and 8.5 pt)
are raised to 9 pt, nothing else changes. Works on the zip: every part but the changed slides and charts is copied byte for byte; the old deck is only read.
Usage: deck_noprompt_v3_5_0.py OLD.pptx NEW.pptx LOG.json"""
import sys, re, json, zipfile, copy, hashlib
sys.dont_write_bytecode = True
from lxml import etree
A = "http://schemas.openxmlformats.org/drawingml/2006/main"; P = "http://schemas.openxmlformats.org/presentationml/2006/main"; NS = {"a": A, "p": P}
LINE, BASE, PAD = 152400, 18287, 182880
ARROW = "  →  "; CAP = 64
COL_W = 4937760                  # width of the code column
FULL_X, FULL_W = 457200, 8229600  # the content width of the deck: 0.5 in to 9.5 in
BAND_Y = 4230000                 # top of the full-width band (the footer text starts at 4599432)
def q(t): p, n = t.split(":"); return "{%s}%s" % (NS[p], n)
def ptext(p): return "".join(t.text or "" for t in p.iter(q("a:t")))
def sp_name(sp): return sp.find(".//" + q("p:cNvPr")).get("name")
def off_ext(sp):
    x = sp.find(".//" + q("a:xfrm")); return x.find(q("a:off")), x.find(q("a:ext"))
def run(src, text, color, bold):
    r = copy.deepcopy(src); r.find(q("a:t")).text = text; pr = r.find(q("a:rPr")); pr.set("b", "1" if bold else "0"); pr.find(".//" + q("a:srgbClr")).set("val", color); return r
def patch_slide(xml, log, no):
    root = etree.fromstring(xml); tree = root.find(".//" + q("p:spTree")); sps = tree.findall(q("p:sp"))
    boxes = [sp for sp in sps if sp.find(q("p:txBody")) is not None and any(ptext(p).startswith(">>> ") for p in sp.find(q("p:txBody")).findall(q("a:p")))]
    if not boxes: return None
    nid = max(int(c.get("id")) for c in root.iter(q("p:cNvPr")))
    for k, sp in enumerate(boxes, 1):
        body = sp.find(q("p:txBody")); o, e = off_ext(sp); top = int(o.get("y")); code, res, last = [], [], None
        for p in body.findall(q("a:p")):
            t = ptext(p)
            if t.startswith((">>> ", "... ")):
                r0 = p.find(q("a:r")); assert "".join(x.text or "" for x in r0.iter(q("a:t"))) == t[:4], (no, t); p.remove(r0); code.append(t[4:]); last = t[4:]
            else: res.append((last, t)); body.remove(p)
        assert len(res) <= 1
        log["code_lines"] += code; sp.find(".//" + q("p:cNvPr")).set("name", "code %d" % k)
        n = len(code); e.set("cy", str(BASE + LINE * n))
        if not res: continue
        expr, val = res[0]; log["results"].append([no, expr, val]); long_ = len(expr) + len(ARROW) + len(val) > CAP
        src = copy.deepcopy(sp.find(q("p:txBody")).find(q("a:p")).find(q("a:r")))
        newsp = copy.deepcopy(sp); nid += 1; c = newsp.find(".//" + q("p:cNvPr")); c.set("name", "result %d" % k); c.set("id", str(nid))
        no_, ne = off_ext(newsp); nb = newsp.find(q("p:txBody"))
        for p in nb.findall(q("a:p")): nb.remove(p)
        np_ = etree.SubElement(nb, q("a:p")); ppr = etree.SubElement(np_, q("a:pPr")); ppr.set("algn", "l")
        np_.append(run(src, expr, "E6EDF3", False)); np_.append(run(src, ARROW, "F2A860", True)); np_.append(run(src, val, "7EE787", False))
        for rp in np_.iter(q("a:rPr")): rp.set("sz", "1000")
        ne.set("cy", str(BASE + LINE))
        bd = [b for b in sps if sp_name(b).startswith("Rounded Rectangle") and int(off_ext(b)[0].get("x")) < int(o.get("x")) and int(off_ext(b)[1].get("cx")) > 4000000
              and int(off_ext(b)[0].get("y")) <= top <= int(off_ext(b)[0].get("y")) + int(off_ext(b)[1].get("cy"))][0]
        bo, be = off_ext(bd)
        if not long_:
            no_.set("y", str(top + LINE * n)); sp.addnext(newsp)          # the row keeps its line: the backdrop and everything below stay
        else:
            old_bottom = int(bo.get("y")) + int(be.get("cy")); be.set("cy", str(BASE + LINE * n + PAD))
            for s2 in sps:                                                  # the left column closes the line the result leaves
                if s2 is sp or s2 is bd: continue
                xo = s2.find(".//" + q("a:xfrm"))
                if xo is None: continue
                so = xo.find(q("a:off"))
                if int(so.get("x")) < 5600000 and old_bottom - 120000 <= int(so.get("y")) < 4500000: so.set("y", str(int(so.get("y")) - LINE))
            nd = copy.deepcopy(bd); nid += 1; nc = nd.find(".//" + q("p:cNvPr")); nc.set("id", str(nid)); nc.set("name", "Rounded Rectangle %d" % nid)
            do, de = off_ext(nd); do.set("x", str(FULL_X)); do.set("y", str(BAND_Y)); de.set("cx", str(FULL_W)); de.set("cy", str(BASE + LINE + PAD))
            no_.set("x", "603504"); no_.set("y", str(BAND_Y + 91440)); ne.set("cx", str(FULL_W - 2 * 146304))
            sp.addnext(nd); nd.addnext(newsp)
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
def main(old, new, logf):
    zi = zipfile.ZipFile(old); log = {"old_sha256": hashlib.sha256(open(old, "rb").read()).hexdigest(), "code_lines": [], "results": [], "slides": [], "slides_size": [], "charts_size": []}
    from pptx import Presentation
    order = {str(s.part.partname).lstrip("/"): i for i, s in enumerate(Presentation(old).slides, 1)}
    zo = zipfile.ZipFile(new, "w", zipfile.ZIP_DEFLATED)
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename in order:
            out = patch_slide(data, log, order[it.filename])
            if out is not None: data = out; log["slides"].append(order[it.filename])
            s = data.decode("utf8"); s2 = re.sub(r'sz="8[05]0"', 'sz="900"', s)
            if s2 != s: data = s2.encode("utf8"); log["slides_size"].append(order[it.filename])
        elif re.match(r"ppt/charts/chart\d+\.xml$", it.filename):
            s = data.decode("utf8"); s2 = re.sub(r'sz="8[05]0"', 'sz="900"', s)
            if s2 != s: data = s2.encode("utf8"); log["charts_size"].append(it.filename)
        zo.writestr(it, data, compress_type=it.compress_type)
    zo.close(); log["new_sha256"] = hashlib.sha256(open(new, "rb").read()).hexdigest(); json.dump(log, open(logf, "x"), indent=1, ensure_ascii=False)
    print("code slides", len(log["slides"]), "code lines", len(log["code_lines"]), "results", len(log["results"]), "slides raised to 9pt", log["slides_size"], "charts", log["charts_size"])
if __name__ == "__main__": main(*sys.argv[1:4])
