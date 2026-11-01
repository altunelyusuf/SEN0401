#!/usr/bin/env python3
"""Chapter 3 deck 3.1.0 (task TK_Ch03_DeckCode_Build): ONE change over deck 3.0.0. Every code box holds code only (no '>>> ' and no '... '), and the result of each example
stands in its own shape named 'result k' directly under the code box ('EXPRESSION  ->  VALUE', the marker of sen0401_code_marker_v1_0_0.py). Code boxes are named 'code k'.
A result longer than one line breaks softly (a:br) after the arrow in a frame with wrap none, so that no shown line wraps; the expression text stays exactly the recorded code line. Works on the zip: every part except the changed slides is copied byte for byte. The old deck is only read. Usage: deck_noprompt_v3_1_0.py OLD.pptx NEW.pptx LOG.json"""
import os, sys, re, json, zipfile, copy, textwrap, hashlib
sys.dont_write_bytecode = True
from lxml import etree
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"a": A, "p": P}
OFFS = json.loads(os.environ.get("RESULT_OFFSETS", "{\"24\": 420624}"))   # slide -> EMU the result shape sits lower than the code box bottom (found once by the build log, see build json)
LINE = 152400          # one 10 pt line in this deck's text boxes (cy = 18287 + n * 152400)
BASE = 18287
PAD = 182880           # backdrop height minus text box height
ARROW = "  →  "
CAP = 62               # characters of Courier New 10 pt that fit the 5.4 inch box, with a margin
def q(t): p, n = t.split(":"); return "{%s}%s" % (NS[p], n)
def ptext(p): return "".join(t.text or "" for t in p.iter(q("a:t")))
def sp_name(sp): return sp.find(".//" + q("p:cNvPr")).get("name")
def off_ext(sp):
    x = sp.find(".//" + q("a:xfrm")); o = x.find(q("a:off")); e = x.find(q("a:ext")); return o, e
def run(src_run, text, color, bold):
    r = copy.deepcopy(src_run); r.find(q("a:t")).text = text
    pr = r.find(q("a:rPr")); pr.set("b", "1" if bold else "0"); pr.find(".//" + q("a:srgbClr")).set("val", color); return r
WIDE = 4937760         # the width of the code box, which lies inside its backdrop
MINSZ = 8.0
def plan_row(expr, val):
    """(font size pt, lines, width EMU, wrap) of the result shape: 10 pt in the code box width when 'expr  ->  value' fits one line; else the largest size (down to 8 pt, steps of 0.5)
    at which it fits ONE line in the wider frame; else (10 pt, 2, wrap none): a soft line break (a:br) after the arrow, each shown line fits the column, the checks read the text without it"""
    n = len(expr) + len(ARROW) + len(val)
    if n <= CAP: return 10.0, 1, 4937760, "square"
    sz = int(WIDE * 0.995 / (n * 0.6 * 12700) * 2) / 2.0
    if sz >= MINSZ: return min(sz, 10.0), 1, WIDE, "square"
    assert len(expr) + len(ARROW) <= CAP and len(val) <= CAP, (expr, val)
    return 10.0, 2, 7600000, "none"
def patch_slide(xml, log, slide_no):
    root = etree.fromstring(xml); tree = root.find(".//" + q("p:spTree")); sps = tree.findall(q("p:sp"))
    boxes = [sp for sp in sps if sp.find(q("p:txBody")) is not None and any(ptext(p).startswith(">>> ") for p in sp.find(q("p:txBody")).findall(q("a:p")))]
    if not boxes: return None
    for k, sp in enumerate(boxes, 1):
        body = sp.find(q("p:txBody")); paras = body.findall(q("a:p")); o, e = off_ext(sp); top, cy = int(o.get("y")), int(e.get("cy"))
        code, results, last = [], [], None
        for p in paras:
            t = ptext(p)
            if t.startswith(">>> ") or t.startswith("... "):
                r0 = p.find(q("a:r")); assert ptext_run(r0) == t[:4], (slide_no, t)   # the prompt is a run of its own
                p.remove(r0); code.append(t[4:]); last = t[4:]
            else:
                results.append((last, t)); body.remove(p)
        assert len(results) <= 1 and (not results or paras[-1] is not None)
        log["code_lines"] += code
        sp.find(".//" + q("p:cNvPr")).set("name", "code %d" % k)
        n = len(code); e.set("cy", str(BASE + LINE * n))
        if not results: continue
        expr, val = results[0]; log["results"].append([slide_no, expr, val])
        SZ, L, W, WRAP = plan_row(expr, val); off = int(OFFS.get(str(slide_no), 0)); extra_emu = (L - 1) * LINE + off
        newsp = copy.deepcopy(sp); newsp.find(".//" + q("p:cNvPr")).set("name", "result %d" % k); newsp.find(".//" + q("p:cNvPr")).set("id", str(max(int(c.get("id")) for c in root.iter(q("p:cNvPr"))) + 1))
        no, ne = off_ext(newsp); no.set("y", str(top + LINE * n + off)); ne.set("cy", str(BASE + LINE * L))
        nb = newsp.find(q("p:txBody"))
        for p in nb.findall(q("a:p")): nb.remove(p)
        src = copy.deepcopy(sp.find(q("p:txBody")).find(q("a:p")).find(q("a:r")))
        np_ = etree.SubElement(nb, q("a:p")); ppr = etree.SubElement(np_, q("a:pPr")); ppr.set("algn", "l")
        np_.append(run(src, expr, "E6EDF3", False)); np_.append(run(src, ARROW, "F2A860", True))
        if L == 2:
            br = etree.SubElement(np_, q("a:br")); br.append(copy.deepcopy(src.find(q("a:rPr"))))
        np_.append(run(src, val, "7EE787", False))
        for rp in np_.iter(q("a:rPr")): rp.set("sz", str(int(SZ * 100)))
        bp = nb.find(q("a:bodyPr")); bp.set("wrap", WRAP); ne.set("cx", str(W))
        if WRAP == "none":   # a fixed frame: the text stays at the left edge (no auto-fit that re-centres the frame)
            for c in list(bp): bp.remove(c)
            etree.SubElement(bp, q("a:noAutofit"))
        sp.addnext(newsp)
        # the backdrop of this box grows by the extra result lines; what lies below it in the left column moves down by the same
        for b in sps:
            if sp_name(b).startswith("Rounded Rectangle"):
                bo, be = off_ext(b)
                if int(bo.get("y")) == top - 91440 and int(bo.get("x")) < top and int(be.get("cx")) > 4000000:
                    old_bottom = int(bo.get("y")) + int(be.get("cy")); be.set("cy", str(BASE + LINE * (n + L) + PAD + off))
                    if extra_emu:
                        for s2 in sps:
                            if s2 is sp or s2 is b: continue
                            xo = s2.find(".//" + q("a:xfrm"))
                            if xo is None: continue
                            so = xo.find(q("a:off"))
                            if int(so.get("x")) < 5600000 and old_bottom - 120000 <= int(so.get("y")) < 4500000:
                                so.set("y", str(int(so.get("y")) + extra_emu))
                        for gf in tree.findall(q("p:graphicFrame")):
                            pass
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
def ptext_run(r): return "".join(t.text or "" for t in r.iter(q("a:t")))
def main(old, new, logf):
    zi = zipfile.ZipFile(old); log = {"old_sha256": hashlib.sha256(open(old, "rb").read()).hexdigest(), "code_lines": [], "results": [], "slides": []}
    order = {}
    from pptx import Presentation
    for i, s in enumerate(Presentation(old).slides, 1): order[str(s.part.partname).lstrip("/")] = i
    zo = zipfile.ZipFile(new, "w", zipfile.ZIP_DEFLATED)
    for it in zi.infolist():
        data = zi.read(it.filename)
        if it.filename in order:
            out = patch_slide(data, log, order[it.filename])
            if out is not None: data = out; log["slides"].append(order[it.filename])
        zo.writestr(it, data, compress_type=it.compress_type)
    zo.close()
    log["new_sha256"] = hashlib.sha256(open(new, "rb").read()).hexdigest(); json.dump(log, open(logf, "w"), indent=1, ensure_ascii=False)
    print("slides changed", len(log["slides"]), "code lines", len(log["code_lines"]), "results", len(log["results"]))
if __name__ == "__main__": main(*sys.argv[1:4])
