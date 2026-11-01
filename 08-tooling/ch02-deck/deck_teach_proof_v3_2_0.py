#!/usr/bin/env python3
"""Proof of the chapter 2 deck v3.2.0 (a NEW tool file; task TK_Ch02_DeckTeach_Build). Prints, as measured:
 (1) the smallest text size per slide and the count of runs below 9 pt (runs, table cells, chart text);
 (2) for every code box and result shape of the 14 code slides: size, characters, width needed at the size (Courier New 0.6 em) against the room of the shape, wrapped lines;
 (3) the code lines and result texts of v3.1.0 against v3.2.0 (which differ, which stay), the shape names;
 (4) the concept table (every concept node of the page v9.72.0 with its slides, slide visual, page visualisation) as JSON and CSV;
 (5) external hyperlinks old and new.
Usage: deck_teach_proof_v3_2_0.py OLD NEW PAGE OUTDIR"""
import csv, json, os, re, sys, zipfile
sys.dont_write_bytecode = True
from pptx import Presentation
from pptx.oxml.ns import qn
old, new, page, out = sys.argv[1:5]
U = 9144
po, pn = Presentation(old), Presentation(new)


def sizes(s):
    v = []
    for el in s._element.iter(qn("a:rPr"), qn("a:endParaRPr"), qn("a:defRPr")):
        if el.get("sz"): v.append(int(el.get("sz")) / 100)
    for sh in s.shapes:
        if sh.has_chart:
            for el in sh.chart._chartSpace.iter(qn("a:rPr"), qn("a:defRPr"), qn("a:endParaRPr")):
                if el.get("sz"): v.append(int(el.get("sz")) / 100)
    return v


L = []
L.append("== (1) smallest text size per slide, runs below 9 pt")
below = 0; allmin = 99
for i, s in enumerate(pn.slides, 1):
    v = sizes(s); m = min(v) if v else None; b = sum(1 for x in v if x < 9); below += b
    if m is not None: allmin = min(allmin, m)
    L.append("slide %2d  smallest %s pt  runs below 9 pt: %d" % (i, m, b))
L.append("DECK smallest size %s pt; runs below 9 pt: %d" % (allmin, below))
L.append("old deck for comparison: runs below 9 pt: %d; slides: %s" % (sum(1 for s in po.slides for x in sizes(s) if x < 9), [i for i, s in enumerate(po.slides, 1) if any(x < 9 for x in sizes(s))]))

L.append("== (2) code boxes and result shapes: size, width needed, room, wrapped lines (Courier New: 0.6 em per character)")
tot_wrapped = 0; smallest = 99; n_shapes = 0; res_widths = []
for i, s in enumerate(pn.slides, 1):
    for sh in s.shapes:
        if not (sh.name.startswith("code ") or sh.name.startswith("result ")) or not sh.has_text_frame: continue
        tf = sh.text_frame
        room = (sh.width - tf.margin_left - tf.margin_right) / 12700.0
        for k, p in enumerate(tf.paragraphs):
            txt = "".join(r.text for r in p.runs)
            sz = max((r.font.size.pt for r in p.runs if r.font.size), default=10)
            need = len(txt) * 0.6 * sz; smallest = min(smallest, min(r.font.size.pt for r in p.runs)); wrapped = 1 if need > room + 0.01 else 0
            tot_wrapped += wrapped; n_shapes += 1
            L.append("slide %2d %-10s line %d: %3d chars at %.1f pt need %6.1f pt, room %6.1f pt, wrapped %d" % (i, sh.name, k + 1, len(txt), sz, need, room, wrapped))
        if sh.name.startswith("result "): res_widths.append((i, int(sh.width / U)))
L.append("CODE AND RESULT SHAPES: %d lines measured; smallest size %.1f pt; wrapped lines %d" % (n_shapes, smallest, tot_wrapped))
L.append("result card widths (slide, units of 1000): %s" % res_widths)
# result tables and charts beside the code: smallest size
tm = 99
for i, s in enumerate(pn.slides, 1):
    if not any(sh.name.startswith("code ") for sh in s.shapes): continue
    for el in s._element.iter(qn("a:rPr")):
        if el.get("sz"): tm = min(tm, int(el.get("sz")) / 100)
L.append("all runs of the 14 code slides: smallest %.1f pt" % tm)

L.append("== (3) code and results, v3.1.0 against v3.2.0")
def codes(prs):
    d = {}
    for i, s in enumerate(prs.slides, 1):
        for sh in s.shapes:
            if sh.name.startswith("code ") or sh.name.startswith("result "):
                d[sh.name] = (i, [p.text for p in sh.text_frame.paragraphs])
    return d
co, cn = codes(po), codes(pn)
same = [k for k in co if k in cn and co[k][1] == cn[k][1]]; diff = [k for k in co if k not in cn or co[k][1] != cn[k][1]]
L.append("shape names old %d new %d; same text %d; different: %s; names missing in new: %s" % (len(co), len(cn), len(same), diff, [k for k in co if k not in cn]))
for k in diff:
    L.append("  %s old: %s" % (k, co[k][1])); L.append("  %s new: %s" % (k, cn[k][1]))
L.append("every result text unchanged: %s" % all(co[k][1] == cn[k][1] for k in co if k.startswith("result ")))

L.append("== (5) external hyperlinks in slide rels")
def links(p):
    z = zipfile.ZipFile(p); n = 0
    for nm in z.namelist():
        if re.match(r"ppt/slides/_rels/slide\d+\.xml\.rels$", nm): n += len(re.findall(r'TargetMode="External"', z.read(nm).decode()))
    return n
L.append("old %d new %d" % (links(old), links(new)))

# (4) concept table
t = open(page, encoding="utf8").read(); a = t.find(">", t.find('id="data"')) + 1; D = json.loads(t[a:t.find("</script>", a)])
def kinds(s):
    k = set()
    for x in s.shapes:
        if x.shape_type == 3: k.add("native chart")
        elif x.shape_type == 13: k.add("picture")
        elif x.shape_type == 19: k.add("table")
        elif x.name.startswith("code "): k.add("code")
    ns = sum(1 for x in s.shapes if x.shape_type == 1 and x.has_text_frame and x.text_frame.text.strip())
    if ns >= 3 and not k: k.add("drawn diagram")
    elif ns >= 3: k.add("drawn shapes")
    return sorted(k) or ["text"]
norm = lambda x: re.sub(r"[^a-z0-9]+", " ", x.lower()).strip()
slide_text = [norm(" ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)) for s in pn.slides]
card = {}
for i, s in enumerate(pn.slides, 1):
    for sh in s.shapes:
        if sh.name.startswith("concept "): card.setdefault(sh.name[8:], []).append(i)
byid = {n["id"]: n for n in D["nodes"]}
kids = {}
for n in D["nodes"]:
    if n["parent"]: kids.setdefault(n["parent"], []).append(n["id"])
def slides_of(nid):
    sl = set(card.get(nid, []))
    n = byid[nid]; lab = norm(n["label"])
    for i, tx in enumerate(slide_text, 1):
        if len(lab) > 3 and re.search(r"(?<![a-z0-9])" + re.escape(lab) + r"(?![a-z0-9])", tx): sl.add(i)
    for c in kids.get(nid, []): sl |= slides_of(c)
    return sl
rows = []; missing = []
for n in D["nodes"]:
    sl = sorted(slides_of(n["id"]))
    if not sl: missing.append(n["label"])
    vis = sorted({k for i in sl for k in kinds(pn.slides[i - 1])})
    pv = ["concept map node", "ontology graph node"]
    if n["id"] in D["panels"]: pv.append("panel " + n["id"])
    if n["id"] in D["visuals"]: pv.append("chapter visual " + n["id"])
    if isinstance(n.get("io"), dict) and "code" in n["io"]: pv.append("lab example")
    own = sorted(card.get(n["id"], []))
    rows.append({"concept": n["label"], "id": n["id"], "level": n["level"], "own_card_slides": own, "slides": sl, "slide_visual": vis, "page_visualisation": pv})
json.dump({"deck": os.path.basename(new), "page": os.path.basename(page), "concepts": len(rows), "without_slide": missing, "rows": rows}, open(os.path.join(out, "concept_table.json"), "w"), indent=1)
w = csv.writer(open(os.path.join(out, "concept_table.csv"), "w", newline="", encoding="utf-8")); w.writerow(["concept", "level", "own card slides", "all slides", "slide visual", "page visualisation"])
for r in rows: w.writerow([r["concept"], r["level"], " ".join(map(str, r["own_card_slides"])), " ".join(map(str, r["slides"])), "; ".join(r["slide_visual"]), "; ".join(r["page_visualisation"])])
leaf = [r for r in rows if r["level"] == 3]
L.append("== (4) concept table: %d concept nodes (%d leaf); without any slide: %s; leaf concepts with their own card: %d of %d; with a slide visual: %d" % (len(rows), len(leaf), missing or "none", sum(1 for r in leaf if r["own_card_slides"]), len(leaf), sum(1 for r in rows if r["slide_visual"])))
print("\n".join(L))
