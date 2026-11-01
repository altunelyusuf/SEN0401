#!/usr/bin/env python3
"""deck_concept_table v3_4_0 (a NEW tool file; task TK_Ch01_DeckTeach_Build): every concept node of the page sen0401_ch01_page_v9_73_0.html (117) with its meaning, the slides of the deck v3.4.0 that carry it (the normalised label, or a named alias phrase that stands on
the slide, occurs in the slide text), the kinds of visual on those slides, and the page visualisation it matches. Nodes of level 1 and 2 are the branches and sections: they are carried by the divider and map slides.
Usage: deck_concept_table_v3_4_0.py DECK PAGE OUT_JSON OUT_CSV"""
import csv, json, re, sys
sys.dont_write_bytecode = True
from pptx import Presentation
deck, page, oj, oc = sys.argv[1:5]
t = open(page, encoding="utf8").read(); a = t.find(">", t.find('id="data"')) + 1; D = json.loads(t[a:t.find("</script>", a)])
pr = Presentation(deck)
def norm(s):
    s = re.sub(r"\(.*?\)", "", s.lower()); w = re.sub(r"[^a-z0-9]+", " ", s).split()
    return " ".join(x[:-1] if x.endswith("s") and len(x) > 3 else x for x in w)
ALIAS = {  # concept label -> phrases that stand on the slides and name the same concept (every phrase is checked against the slide text)
    "Bitcoin unit": ["satoshis", "bitcoin counted"], "Supply cap": ["21 million cap", "cap is just under 21 million"], "Block subsidy": ["subsidy"],
    "Deflation": ["deflationary"], "Central bank replacement": ["no central bank is needed"], "Byzantine Generals' Problem": ["byzantine generals"], "Digital currencies before Bitcoin": ["failed digital money", "ecash"],
    "Bitcoin Improvement Proposal (BIP)": ["bitcoin improvement proposal"], "Inputs and outputs": ["coins in, payment and change out", "inputs", "outputs"],
    "Offchain payment": ["offchain"], "Lightning Network": ["lightning network"], "Electronic payment": ["electronic payments"], "Irreversibility": ["irreversible", "reverse it"],
    "Decentralized identifier": ["decentralized identifier"], "Verifiable credential": ["verifiable credential"], "Buy from friend": ["buy from a friend", "buying from a friend"],
    "Earn bitcoin": ["earn it"], "Address reuse and privacy": ["one address per payer", "address reuse"], "Standards and openness": ["changes without a boss", "open standards"],
    "Keyed hash": ["keyed hash"], "Public-key cryptography": ["public-key cryptography"], "Peer and client": ["peer of the others"],
    "Wallet metadata": ["labels and history"], "Currency exchange": ["currency exchange"], "Identity verification": ["identity verification"],
}
def kinds(sl):
    k = set()
    for x in sl.shapes:
        if x.shape_type == 3: k.add("native chart")
        elif x.shape_type == 13: k.add("picture")
        elif x.shape_type == 19: k.add("table")
        elif x.name.startswith("code "): k.add("code")
    if not k: k.add("drawn shapes")
    return sorted(k)
txt = []
for s in pr.slides:
    tt = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame)
    for sh in s.shapes:
        if sh.has_table: tt += " " + " ".join(c.text for r in sh.table.rows for c in r.cells)
    txt.append(" " + norm(tt) + " ")
rows = []; missing = []
for n in D["nodes"]:
    keys = [norm(n["label"])] + [norm(x) for x in ALIAS.get(n["label"], [])]
    sl = sorted({i + 1 for i, x in enumerate(txt) if any(" " + k + " " in x for k in keys)})
    if n["level"] == 3 and not sl: missing.append(n["label"])
    vis = sorted({k for s in sl for k in kinds(pr.slides[s - 1])})
    pv = ["concept map node", "ontology graph node"]
    if n["id"] in D["panels"]: pv.append("panel " + n["id"])
    if n["id"] in D["visuals"]: pv.append("chapter visual " + n["id"])
    if isinstance(n.get("io"), dict) and "code" in n["io"]: pv.append("lab example")
    rows.append({"concept": n["label"], "level": n["level"], "meaning": n.get("definition") or (n.get("body") or "").split(". ")[0], "slides": sl, "slide_visual": vis, "page_visualisation": pv,
                 "carried_by": "slides" if sl else ("divider and map slides (branch or section node)" if n["level"] < 3 else "NONE")})
json.dump({"deck": deck.rsplit("/", 1)[-1], "page": page.rsplit("/", 1)[-1], "concepts": len(rows), "level3_without_slide": missing, "rows": rows}, open(oj, "w"), indent=1, ensure_ascii=False)
w = csv.writer(open(oc, "w", newline="", encoding="utf-8")); w.writerow(["concept", "level", "meaning", "slides", "slide visual", "page visualisation", "carried by"])
for r in rows: w.writerow([r["concept"], r["level"], r["meaning"], " ".join(map(str, r["slides"])), "; ".join(r["slide_visual"]), "; ".join(r["page_visualisation"]), r["carried_by"]])
print("concepts", len(rows), "| level-3 concepts without a slide:", len(missing), missing or "none", "| with a slide visual:", sum(1 for r in rows if r["slide_visual"]))
