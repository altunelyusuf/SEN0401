#!/usr/bin/env python3
"""Chapter 2 deck v3.1.0 (a NEW tool file; task TK_Ch02_DeckCode_Build, owner's word relayed 2026-10-30 and 2026-11-01: slide code without the prompts '>>> ' and '... ',
the result of each example shown apart, directly under its code box). The deck v3.0.0 is read, never written; its SHA-256 is printed before and after.
ONE kind of change, made on the XML of the 14 code slides only (every other part of the package is copied byte for byte):
  - every code box (a text box whose paragraphs start with '>>> ') keeps its code lines, byte for byte, without the prompt; the box is named 'code <slide>-<k>' and shrinks by the result rows it held;
  - each result row (the line printed after the last '>>> ' row) leaves the box and stands in its own shape named 'result <slide>', directly under the code frame, reading
    'EXPRESSION  ->  VALUE' (a long one on two paragraphs: the expression, then the arrow and the value) (the marker of sen0401_code_marker_v1_0_0.py), in the deck's palette (white card, teal rule, grey expression, orange arrow, ink value);
  - the shapes of the left column below the code are moved down by exactly the room the result shape needs; nothing else changes.
It also writes the deck plan deck_plan_v3_1_0.json (the plan of v3.0.0 with the new version) and the change log deck_code_v3_1_0_log.json.
Usage: deck_code_v3_1_0.py"""
__version__ = "3.1.0"
import copy, hashlib, json, os, re, sys, zipfile
sys.dont_write_bytecode = True
from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SRC = os.path.join(ROOT, "03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx")
DST = os.path.join(ROOT, "03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_1_0.pptx")
PLAN_OLD = os.path.join(HERE, "deck_plan_v3_0_0.json")
PLAN_NEW = os.path.join(HERE, "deck_plan_v3_1_0.json")
LOG = os.path.join(HERE, "deck_code_v3_1_0_log.json")
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
ns = {"a": A, "p": P}
q = lambda pre, t: "{%s}%s" % (ns[pre], t)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

PITCH = 152400            # one 10 pt code line, as the deck draws it
FRAME_PAD = 182880        # the dark frame is the text box plus 0.1 inch above and below
GAP = 18288               # between the code frame and the result shape
RES_PAD = 109728          # the result shape: its lines plus this
MINGAP = 36576            # the least gap kept between two shapes of the left column when they are pushed down
LEFT_COL_RIGHT = 5700000  # shapes of the left column end before this x
MUTE, ORANGE, INK, TEAL = "6E655C", "D97A14", "2B2622", "2F6D62"
INSET = 36576            # left and right inset of the result card
WRAP_AT = 60              # characters of 'EXPR  ->  VALUE' that fit one 10 pt Courier line of the result shape


def gx(sp):
    x = sp.find("p:spPr/a:xfrm", ns)
    o, e = x.find("a:off", ns), x.find("a:ext", ns)
    return x, o, e


def geom(sp):
    x, o, e = gx(sp)
    return int(o.get("x")), int(o.get("y")), int(e.get("cx")), int(e.get("cy"))


def para_text(p):
    return "".join(t.text or "" for t in p.iter(q("a", "t")))


def run_el(text, color, bold, sz=1000):
    r = etree.Element(q("a", "r"))
    rp = etree.SubElement(r, q("a", "rPr"), sz=str(sz), b="1" if bold else "0", i="0")
    sf = etree.SubElement(rp, q("a", "solidFill")); etree.SubElement(sf, q("a", "srgbClr"), val=color)
    etree.SubElement(rp, q("a", "latin"), typeface="Courier New")
    t = etree.SubElement(r, q("a", "t")); t.text = text
    return r


def result_size(text, w):
    """the largest size (hundredths of a point, steps of 0.5 pt, at most 10 pt) at which the whole 'EXPRESSION  ->  VALUE' line stands on ONE line of the card: the deck standard D12 (no code line wraps)
    measures characters x 0.6 x size against the width minus the insets, and the marker needs the line in one paragraph"""
    room = (w - 2 * INSET) / 12700.0
    for sz in range(1000, 0, -50):
        if len(text) * 0.6 * (sz / 100.0) <= room:
            return sz
    raise ValueError(text)


def result_shape(sid, name, x, y, w, expr, value):
    text = expr + "  →  " + value
    sz = result_size(text, w)
    k = 1
    h = k * PITCH + RES_PAD
    sp = etree.fromstring(
        '<p:sp xmlns:p="%s" xmlns:a="%s"><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>'
        '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 6000"/></a:avLst></a:prstGeom><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>'
        '<a:ln w="15875"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln><a:effectLst/></p:spPr>'
        '<p:txBody><a:bodyPr wrap="square" lIns="%d" rIns="%d" tIns="45720" bIns="45720" anchor="ctr"><a:noAutofit/></a:bodyPr><a:lstStyle/><a:p><a:pPr algn="l"/></a:p></p:txBody></p:sp>'
        % (P, A, sid, name, x, y, w, h, TEAL, INSET, INSET))
    p = sp.find("p:txBody/a:p", ns)
    p.append(run_el(expr, MUTE, False, sz)); p.append(run_el("  →  ", ORANGE, True, sz)); p.append(run_el(value, INK, True, sz))
    return sp, h, sz


def process_slide(xml, slide_no):
    root = etree.fromstring(xml)
    tree = root.find("p:cSld/p:spTree", ns)
    sps = [s for s in tree if s.tag == q("p", "sp")]
    boxes = []
    for sp in sps:
        paras = sp.findall("p:txBody/a:p", ns)
        if paras and para_text(paras[0]).startswith(">>> "):
            boxes.append(sp)
    boxes.sort(key=lambda s: (geom(s)[1], geom(s)[0]))
    max_id = max(int(c.get("id")) for c in root.iter(q("p", "cNvPr")))
    code_old, code_new, results, edits = [], [], [], []
    for k, tb in enumerate(boxes, 1):
        paras = tb.findall("p:txBody/a:p", ns)
        texts = [para_text(p) for p in paras]
        x, y, w, h = geom(tb)
        assert abs(h - (len(paras) * PITCH + 18287)) < 3, (slide_no, k, h, len(paras))
        # its dark frame: the autoshape 0.1 inch around the text box
        frame = [s for s in sps if s is not tb and abs(geom(s)[0] - (x - 146304)) < 3 and abs(geom(s)[1] - (y - 91440)) < 3 and abs(geom(s)[2] - (w + 274320)) < 3 and abs(geom(s)[3] - (h + FRAME_PAD)) < 3]
        assert len(frame) == 1, (slide_no, k, len(frame))
        frame = frame[0]
        keep, res = [], []
        for i, (p, t) in enumerate(zip(paras, texts)):
            if t.startswith(">>> ") or t.startswith("... "):
                code_old.append(t)
                first = p.find("a:r", ns); ft = first.find("a:t", ns)
                if ft.text in (">>> ", "... "):
                    p.remove(first)
                else:
                    ft.text = ft.text[4:]
                code_new.append(para_text(p)); keep.append(p)
            else:
                assert keep, (slide_no, "result row before any code row")
                res.append((code_new[-1], t)); p.getparent().remove(p)
        assert code_new and all(para_text(p) == c for p, c in zip(keep, code_new[-len(keep):]))
        tb.find("p:nvSpPr/p:cNvPr", ns).set("name", "code %d-%d" % (slide_no, k))
        if not res:
            continue
        assert len(res) == 1 and k == len(boxes), (slide_no, "one result row, in the last box: the shape of this deck", res)
        freed = PITCH * len(res)
        old_frame_bottom = geom(frame)[1] + geom(frame)[3]
        for el, newh in ((tb, h - freed), (frame, h - freed + FRAME_PAD)):
            gx(el)[2].set("cy", str(newh))
        fx, fy, fw, fh = geom(frame)
        max_id += 1
        expr, value = res[0]
        sp, rh, rsz = result_shape(max_id, "result %d" % slide_no, fx, fy + fh + GAP, fw, expr, value)
        tb.addnext(sp)
        # push the shapes of the left column below the code down, only as far as they would otherwise touch (gaps kept, down to MINGAP)
        items = []
        for o in tree:
            if o is tb or o is frame or o is sp or o.tag not in (q("p", "sp"), q("p", "pic"), q("p", "graphicFrame")):
                continue
            xf = o.find("p:xfrm", ns) if o.tag == q("p", "graphicFrame") else o.find("p:spPr/a:xfrm", ns)
            of, ex = xf.find("a:off", ns), xf.find("a:ext", ns)
            ox, oy, ow, oh = int(of.get("x")), int(of.get("y")), int(ex.get("cx")), int(ex.get("cy"))
            if ox + ow <= LEFT_COL_RIGHT and oy >= old_frame_bottom - 1:
                items.append((oy, ox, ow, oh, of, o))
        items.sort(key=lambda t: (t[0], t[1]))
        placed = [(fx, fx + fw, old_frame_bottom, fy + fh + GAP + rh)]
        moved = []
        for oy, ox, ow, oh, of, o in items:
            top = oy
            for x0, x1, ob, nb in placed:
                if ox < x1 and ox + ow > x0 and ob <= oy + 1:
                    top = max(top, nb + min(oy - ob, MINGAP))
            if top != oy:
                of.set("y", str(top)); moved.append((o.find("p:nvSpPr/p:cNvPr", ns).get("name") if o.tag == q("p", "sp") else o.tag.split("}")[1], top - oy))
            placed.append((ox, ox + ow, oy + oh, top + oh))
        delta = max((m[1] for m in moved), default=0)
        results.append((expr, value)); edits.append({"box": k, "result_size_pt": rsz / 100.0, "moved_down_emu_max": delta, "moved": moved})
    out = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)
    return out, code_old, code_new, results, edits


def main():
    before = sha(SRC)
    zin = zipfile.ZipFile(SRC)
    log = {"tool": "deck_code_v3_1_0.py", "src": os.path.basename(SRC), "dst": os.path.basename(DST), "sha256_src_before": before, "slides": {}}
    order = [n for n in zin.namelist()]
    code_old_all, code_new_all, res_all = [], [], []
    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        for info in zin.infolist():
            data = zin.read(info.filename)
            m = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", info.filename)
            if m and b"&gt;&gt;&gt; " in data:
                no = int(m.group(1))
                data, co, cn, rs, ed = process_slide(data, no)
                code_old_all += [(no, l) for l in co]; code_new_all += [(no, l) for l in cn]; res_all += [(no, e, v) for e, v in rs]
                log["slides"][str(no)] = {"code_lines": len(co), "results": [{"expression": e, "value": v} for e, v in rs], "edits": ed}
            zi = zipfile.ZipInfo(info.filename, date_time=info.date_time); zi.compress_type = info.compress_type; zi.external_attr = info.external_attr
            zout.writestr(zi, data)
    log["code_lines_old"] = len(code_old_all); log["code_lines_new"] = len(code_new_all)
    assert [(n, l[4:]) for n, l in code_old_all] == code_new_all
    log["sha256_src_after"] = sha(SRC); log["sha256_dst"] = sha(DST)
    plan = json.load(open(PLAN_OLD))
    plan["meta"]["version"] = "3.1.0"; plan["meta"]["sub"] = "SEN0401, third-edition deck 3.1.0"
    plan["meta"]["v3_1_0"] = "2026-11-01, task TK_Ch02_DeckCode_Build: every code box holds code only (no '>>> ' or '... ' prompt), the result of each example stands in its own 'result' shape under the code; nothing else changed"
    json.dump(plan, open(PLAN_NEW, "w"), indent=1, ensure_ascii=False)
    json.dump(log, open(LOG, "w"), indent=1, ensure_ascii=False)
    print("SHA-256 of v3_0_0 before:", before); print("SHA-256 of v3_0_0 after: ", log["sha256_src_after"]); print("SHA-256 of v3_1_0:      ", log["sha256_dst"])
    print("code lines old/new: %d / %d; result shapes: %d; slides changed: %d" % (len(code_old_all), len(code_new_all), len(res_all), len(log["slides"])))


if __name__ == "__main__":
    main()
