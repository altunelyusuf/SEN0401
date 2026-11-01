#!/usr/bin/env python3
"""deck_concept_table v3_6_0 (chapter 5): every concept node of the page v9.84.0 (111: 8 branches, 18 groups, 85 concepts) with its meaning, its everyday analogy, the slides of the deck that carry it, the visual kinds on those slides
and the page visualisation it matches. A node finds its slides by its label as a whole word in the slide text (title, boxes, tables, groups, notes), the title first, then the concept and analogy rows; a branch or group takes the slides of its
children; 16 nodes whose label the slides word differently are mapped by hand (MANUAL, stated here). Reads only. Usage: deck_concept_table_v3_6_0.py DECK PAGE PLAN OUT.json OUT.csv"""
import sys, json, csv, re
sys.dont_write_bytecode = True
from pptx import Presentation
deck, page, plan, oj, oc = sys.argv[1:6]
t = open(page, encoding="utf8").read(); a = t.find(">", t.find('id="data"')) + 1; D = json.loads(t[a:t.find("</script>", a)])
pr = Presentation(deck); pl = json.load(open(plan))
MANUAL = {"Hierarchical deterministic key generation": [9, 32], "Using a derived child key": [36, 37], "Purpose level (BIP43)": [44, 51], "BIP44 structure": [44, 48], "Account branch": [44], "Change branch": [44], "Address index": [44],
          "BIP44 path for legacy scripts": [45, 48], "BIP49 path for nested segwit": [45, 48], "BIP84 path for native segwit": [45, 46, 48], "BIP86 path for single-key taproot": [45, 47, 48],
          "Label export format (BIP329)": [54], "SHA-256 and SHA-512": [22, 27, 33], "Secret sharing": [18], "Eleven-bit segment": [21, 24], "Output script descriptor": [43, 49, 51]}
def parts(s):
    title = s.shapes.title.text if s.shapes.title is not None else ""; body = []; rows = []
    for sh in s.shapes:
        if sh.has_text_frame: body.append(sh.text_frame.text)
        if sh.shape_type == 19:
            for r in sh.table.rows: rows.append(r.cells[0].text); body += [c.text for c in r.cells]
        if sh.shape_type == 6: body += [x.text_frame.text for x in sh.shapes if x.has_text_frame]
        if sh.name in ("concept",): rows.append(sh.text_frame.text)
    notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
    return title.lower(), " ".join(body + [notes]).lower(), [r.lower() for r in rows]
P = [parts(s) for s in pr.slides]
def kinds(i):
    k = set()
    for x in pr.slides[i - 1].shapes:
        if x.shape_type == 3: k.add("native chart")
        elif x.shape_type == 13: k.add("picture")
        elif x.shape_type == 19: k.add("table")
        elif x.name.startswith("code "): k.add("code")
    return sorted(k) or ["drawn shapes"]
def norm(l): return re.sub(r"\s*\(.*?\)", "", l).lower().strip()
by = {x["concept"].lower(): x for x in pl["meta"]["analogies"]}
N = {n["id"]: n for n in D["nodes"]}; kids = {}
for n in D["nodes"]: kids.setdefault(n.get("parent"), []).append(n["id"])
slides = {}
def find(n):
    if n["label"] in MANUAL: return sorted(MANUAL[n["label"]])
    l = norm(n["label"]); rx = re.compile(r"(?<![a-z0-9])" + re.escape(l) + r"(?![a-z0-9])")
    first = [i + 1 for i, (ti, bo, ro) in enumerate(P) if rx.search(ti)]
    second = [i + 1 for i, (ti, bo, ro) in enumerate(P) if i + 1 not in first and any(rx.search(r) for r in ro)]
    third = [i + 1 for i, (ti, bo, ro) in enumerate(P) if i + 1 not in first + second and rx.search(bo)]
    return sorted((first + second + third)[:6])
def resolve(nid):
    if nid in slides: return slides[nid]
    n = N[nid]
    s = set(find(n)) if n["level"] == 3 else set()
    for c in kids.get(nid, []): s |= set(resolve(c))
    slides[nid] = sorted(s); return slides[nid]
rows = []; missing = []
for n in D["nodes"]:
    sl = resolve(n["id"]); an = by.get(n["label"].lower()) or by.get(norm(n["label"]))
    if not sl: missing.append(n["label"])
    vis = sorted({k for s in sl for k in kinds(s)})
    pv = ["concept map node", "ontology graph node"]
    if n["id"] in D["panels"]: pv.append("panel " + n["id"])
    if n["id"] in D["visuals"]: pv.append("chapter visual " + n["id"])
    if isinstance(n.get("io"), dict) and n["io"].get("code"): pv.append("lab example")
    rows.append({"concept": n["label"], "level": n["level"], "meaning": n.get("definition") or (n.get("body") or "").split(". ")[0], "analogy": an["analogy"] if an else "", "slides": sl, "slide_visual": vis, "page_visualisation": pv})
json.dump({"deck": deck.rsplit("/", 1)[-1], "page": page.rsplit("/", 1)[-1], "concepts": len(rows), "without_slide": missing, "rows": rows}, open(oj, "w"), indent=1, ensure_ascii=False)
w = csv.writer(open(oc, "w", newline="", encoding="utf-8")); w.writerow(["concept", "level", "meaning", "analogy", "slides", "slide visual", "page visualisation"])
for r in rows: w.writerow([r["concept"], r["level"], r["meaning"], r["analogy"], " ".join(map(str, r["slides"])), "; ".join(r["slide_visual"]), "; ".join(r["page_visualisation"])])
print("concepts", len(rows), "| without a slide:", missing or "none", "| with a slide visual:", sum(1 for r in rows if r["slide_visual"]), "| with an analogy:", sum(1 for r in rows if r["analogy"]))
