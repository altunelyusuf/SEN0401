#!/usr/bin/env python3
"""Chapter 1 deck v3.3.0 (a NEW tool file; task TK_Ch01_DeckCode_Build). The deck v3.2.0 is read, never written; its SHA-256 is printed before and after.
ONE kind of change: every code box holds code only (the prompts '>>> ' are removed; the code characters are untouched) and the result of each example stands in its own
result shape directly under the last code box of the slide, in the deck's palette (white card, orange border, Courier New 10 pt, 'EXPRESSION  ->  VALUE' with the arrow U+2192, the form of
sen0401_code_marker_v1_0_0.py). Code shapes are named 'code N.k', result shapes 'result N' (N = the example's order on the chapter's code slides, k = the box on the slide).
Everything below the lowest code box of the left column moves down by the same amount; no other part of any other slide is touched (package parts are copied byte for byte, same order,
same compression, except the 15 code slides and docProps/core.xml whose cp:version becomes 3.3.0). Also writes deck_plan_v3_3_0.json (the plan of v3_1_0 with the new code geometry).
Usage: python3 -B deck_code_v3_3_0.py OLD NEW PLAN_OLD PLAN_NEW REPORT_JSON"""
__version__ = "3.3.0"
import copy, hashlib, json, re, sys, zipfile
from lxml import etree

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS = {"a": A, "p": P}
PT = 12700
GAP = 4 * PT
SLIDE_BOTTOM_LIMIT = 356 * PT      # the footer band starts near 362 pt
q = lambda t: "{%s}%s" % (NS[t[0]], t[2:])


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def sp_geom(sp):
    off = sp.find(".//a:xfrm/a:off", NS); ext = sp.find(".//a:xfrm/a:ext", NS)
    return off, ext


def para_text(p):
    return "".join(t.text or "" for t in p.iter(q("a:t")))


def result_shape(sid, name, left, top, width, height, expr, value):
    xml = f'''<p:sp xmlns:p="{P}" xmlns:a="{A}"><p:nvSpPr><p:cNvPr id="{sid}" name="{name}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
<p:spPr><a:xfrm><a:off x="{left}" y="{top}"/><a:ext cx="{width}" cy="{height}"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 11396"/></a:avLst></a:prstGeom>
<a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln w="12700"><a:solidFill><a:srgbClr val="D97A14"/></a:solidFill><a:prstDash val="solid"/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="109728" tIns="45720" rIns="109728" bIns="45720" rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr indent="0" marL="0"><a:buNone/></a:pPr>%s</a:p></p:txBody></p:sp>'''
    def run(t, color, bold):
        t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return (f'<a:r><a:rPr lang="en-US" sz="1000"{" b=\"1\"" if bold else ""} dirty="0"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
                '<a:latin typeface="Courier New" pitchFamily="34" charset="0"/><a:ea typeface="Courier New" pitchFamily="34" charset="-122"/>'
                '<a:cs typeface="Courier New" pitchFamily="34" charset="-120"/></a:rPr><a:t xml:space="preserve">' + t + '</a:t></a:r>')
    runs = run(expr, "6E655C", False) + run("  →  ", "D97A14", True) + run(value, "2B2622", True)
    return etree.fromstring((xml % runs).encode("utf-8"))


def convert_slide(data, ex_no):
    root = etree.fromstring(data)
    tree = root.find(".//p:cSld/p:spTree", NS)
    sps = list(tree.findall("p:sp", NS))
    texts = []
    for sp in sps:
        ps = sp.findall(".//a:p", NS)
        if ps and para_text(ps[0]).startswith(">>> "):
            texts.append(sp)
    assert texts, "no code box"
    # pitch of one code line (EMU) from the boxes of this deck: 14, 27, 40, 53 pt
    heights = {}
    for sp in texts:
        n = len(sp.findall(".//a:p", NS)); heights[n] = int(sp_geom(sp)[1].get("cy"))
    pitch = 165100            # 13 pt: the step the builder used between the one-, two-, three- and four-line boxes
    info = {"slide_boxes": len(texts), "codes": [], "result": None}
    last = texts[-1]
    # background shape of every box = the p:sp just before the text shape (a roundRect without text)
    for k, sp in enumerate(texts, 1):
        paras = sp.findall(".//a:p", NS)
        lines = []
        is_last = sp is last
        for pi, p in enumerate(paras):
            runs = p.findall("a:r", NS)
            t0 = runs[0].find("a:t", NS).text if runs and runs[0].find("a:t", NS) is not None else ""
            if t0 == ">>> ":
                code = "".join(r.find("a:t", NS).text or "" for r in runs[1:])
                lines.append(("code", code, p, runs))
            else:
                lines.append(("result", "".join(r.find("a:t", NS).text or "" for r in runs), p, runs))
        # a result row is the paragraph that follows a code row and is not a code row; only the last box may carry one
        res = [l for l in lines if l[0] == "result"]
        assert len(res) <= 1 and (not res or (is_last and lines[-1][0] == "result")), ("result row not at the end of the last box", ex_no)
        for kind, text, p, runs in lines:
            if kind == "code":
                p.remove(runs[0])
        if res:
            info["result"] = (lines[-2][1], res[0][1])
            sp.find("p:txBody", NS).remove(res[0][2])
        sp.find("p:nvSpPr/p:cNvPr", NS).set("name", "code %d.%d" % (ex_no, k))
        info["codes"].append([l[1] for l in lines if l[0] == "code"])
    assert info["result"], ("no result row", ex_no)
    # geometry: the last box loses one line; the result card follows; the left column below it moves down
    ti = sps.index(last); bg = sps[ti - 1]
    assert bg.find(".//p:txBody", NS) is None and bg.find(".//a:prstGeom", NS).get("prst") == "roundRect", "background of the last code box not found"
    bgo, bge = sp_geom(bg); to, te = sp_geom(last)
    old_bottom = int(bgo.get("y")) + int(bge.get("cy"))
    bge.set("cy", str(int(bge.get("cy")) - pitch)); te.set("cy", str(int(te.get("cy")) - pitch))
    new_bottom = int(bgo.get("y")) + int(bge.get("cy"))
    expr, value = info["result"]
    width_chars = (int(bge.get("cx")) - 2 * 109728) / PT / 6.0      # Courier New 10 pt: 6.0 pt per character
    n_lines = max(1, -(-len(expr + "  →  " + value) // int(width_chars)))
    rh = int((n_lines * 12.6 + 8) * PT)
    rtop = new_bottom + GAP
    shift = -pitch + GAP + rh
    ids = [int(x.get("id")) for x in root.iter(q("p:cNvPr"))]
    sid = max(ids) + 1
    rs = result_shape(sid, "result %d" % ex_no, int(bgo.get("x")), rtop, int(bge.get("cx")), rh, expr, value)
    last.addnext(rs)
    moved = []
    for el in tree:
        if el is rs or el is last or el is bg:
            continue
        x = el.find(".//a:xfrm/a:off", NS)
        if x is None:
            x = el.find(".//p:xfrm/a:off", NS)
        if x is None:
            continue
        top, left = int(x.get("y")), int(x.get("x"))
        if top >= old_bottom - PT and left < 440 * PT and top < 360 * PT and el.tag != q("p:pic"):
            x.set("y", str(top + shift)); moved.append(el.find(".//p:cNvPr", NS).get("name"))
            ext = el.find(".//a:xfrm/a:ext", NS)
            assert top + shift + int(ext.get("cy")) <= SLIDE_BOTTOM_LIMIT, ("moved element reaches the footer band", ex_no, moved[-1])
    info.update(shift_pt=shift / PT, result_top_pt=rtop / PT, result_h_pt=rh / PT, old_bottom_pt=old_bottom / PT, moved=moved, old_bg_bottom=old_bottom, new_bg_bottom=new_bottom, rtop=rtop, rh=rh, shift=shift)
    out = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    return out, info


def main(old, new, plan_old, plan_new, report):
    before = sha(old); print("SHA-256 old deck before:", before)
    zi = zipfile.ZipFile(old)
    code_slides = []
    for n in sorted((n for n in zi.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[0])):
        if b"&gt;&gt;&gt; " in zi.read(n):
            code_slides.append(n)
    assert len(code_slides) == 15, len(code_slides)
    rep = {"tool": __version__, "old_sha256_before": before, "slides": {}}
    with zipfile.ZipFile(new, "w") as zo:
        for info in zi.infolist():
            data = zi.read(info.filename)
            if info.filename in code_slides:
                no = code_slides.index(info.filename) + 1
                data, inf = convert_slide(data, no)
                rep["slides"][int(re.findall(r"\d+", info.filename)[0])] = {"example": no, "codes": inf["codes"], "result": inf["result"], "shift_pt": inf["shift_pt"], "result_top_pt": inf["result_top_pt"], "result_h_pt": inf["result_h_pt"], "moved": inf["moved"], "_g": {k: inf[k] for k in ("old_bg_bottom", "new_bg_bottom", "rtop", "rh", "shift")}}
            elif info.filename == "docProps/core.xml":
                assert data.count(b"<cp:version>3.2.0</cp:version>") == 1
                data = data.replace(b"<cp:version>3.2.0</cp:version>", b"<cp:version>3.3.0</cp:version>")
            zo.writestr(info, data, compress_type=info.compress_type)
    after = sha(old); print("SHA-256 old deck after: ", after, "UNCHANGED" if before == after else "CHANGED")
    assert before == after
    # the plan: the plan of v3_1_0 (= the plan of v3_2_0) with the prompt-free rows, the result and the geometry
    plan = json.load(open(plan_old))
    plan["meta"]["version"] = "3.3.0"
    plan["meta"]["code_form"] = "2026-11-01, task TK_Ch01_DeckCode_Build: code boxes hold code only (no '>>> '), rows are [code, ''], and each codeblocks item has 'result': [[expression, value, y, h]] directly under the last group; shapes are named 'code N.k' and 'result N' (marker of sen0401_code_marker_v1_0_0.py)"
    slide_idx = [int(re.findall(r"\d+", n)[0]) for n in code_slides]
    for sn, no in zip(slide_idx, range(1, 16)):
        g = rep["slides"][sn]["_g"]; sl = plan["slides"][sn - 1]
        for it in sl["items"]:
            if it.get("t") == "codeblocks":
                grp = it["groups"][-1]
                grp["rows"] = [[r[0], ""] for r in grp["rows"]]
                assert [r[0] for r in grp["rows"]] == rep["slides"][sn]["codes"][-1]
                for gg in it["groups"][:-1]:
                    gg["rows"] = [[r[0], ""] for r in gg["rows"]]
                e = 914400.0
                grp["h"] = round(grp["h"] - 13 / 72.0, 3)
                grp["result"] = [rep["slides"][sn]["result"][0], rep["slides"][sn]["result"][1], round(g["rtop"] / e, 3), round(g["rh"] / e, 3)]
                grp["ny"] = round(grp["ny"] + g["shift"] / e, 3)
                it["capy"] = round(it["capy"] + g["shift"] / e, 3)
    json.dump(plan, open(plan_new, "w"), ensure_ascii=False, indent=1)
    for v in rep["slides"].values():
        v.pop("_g")
    rep["new_sha256"] = sha(new)
    json.dump(rep, open(report, "w"), ensure_ascii=False, indent=1)
    print("wrote", new, rep["new_sha256"])
    for sn, v in rep["slides"].items():
        print("slide", sn, "ex", v["example"], "shift %.1f pt" % v["shift_pt"], "result", v["result"], "moved", v["moved"])


if __name__ == "__main__":
    main(*sys.argv[1:6])
