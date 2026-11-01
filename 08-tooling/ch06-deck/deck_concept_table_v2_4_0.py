#!/usr/bin/env python3
"""deck_concept_table v2_4_0: the concept table of the chapter 6 deck: every concept node of the page v9.89.0 (115) with its meaning, analogy, the slides of the deck that explain it (plan v2_3_0 analogies, which the slides carry), the visual kinds on those slides and the page visualisation it matches. Reads only. Usage: DECK PAGE PLAN OUT.json OUT.csv"""
import sys, json, csv
sys.dont_write_bytecode = True
from pptx import Presentation
deck, page, plan, oj, oc = sys.argv[1:6]
t = open(page, encoding="utf8").read(); a = t.find(">", t.find('id="data"')) + 1; D = json.loads(t[a:t.find("</script>", a)])
pr = Presentation(deck); pl = json.load(open(plan))
def kinds(i):
    k = set()
    for x in pr.slides[i - 1].shapes:
        if x.shape_type == 3: k.add("native chart")
        elif x.shape_type == 13: k.add("picture")
        elif x.shape_type == 19: k.add("table")
        elif x.name.startswith("code "): k.add("code")
    return sorted(k) or ["drawn shapes"]
by = {}
for x in pl["meta"]["analogies"]: by.setdefault(x["concept"], []).append(x)
rows = []; missing = []
for n in D["nodes"]:
    es = by.get(n["label"], [])
    sl = sorted({e["slide"] for e in es})
    if not sl: missing.append(n["label"])
    vis = sorted({k for s in sl for k in kinds(s)})
    pv = ["concept map node", "ontology graph node"]
    if n["id"] in D["panels"]: pv.append("panel " + n["id"])
    if n["id"] in D["visuals"]: pv.append("chapter visual " + n["id"])
    if "code" in (n["io"] if isinstance(n.get("io"), dict) else {}): pv.append("lab example")
    rows.append({"concept": n["label"], "level": n["level"], "meaning": n.get("definition") or (n.get("body") or "").split(". ")[0], "analogy": es[0]["analogy"] if es else "", "slides": sl, "slide_visual": vis, "page_visualisation": pv})
json.dump({"deck": deck.rsplit("/", 1)[-1], "page": page.rsplit("/", 1)[-1], "concepts": len(rows), "without_slide": missing, "rows": rows}, open(oj, "w"), indent=1, ensure_ascii=False)
w = csv.writer(open(oc, "w", newline="", encoding="utf-8")); w.writerow(["concept", "level", "meaning", "analogy", "slides", "slide visual", "page visualisation"])
for r in rows: w.writerow([r["concept"], r["level"], r["meaning"], r["analogy"], " ".join(map(str, r["slides"])), "; ".join(r["slide_visual"]), "; ".join(r["page_visualisation"])])
print("concepts", len(rows), "| without a slide:", missing or "none", "| with a slide visual:", sum(1 for r in rows if r["slide_visual"]))
