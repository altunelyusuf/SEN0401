#!/usr/bin/env python3
"""sen0401_lecture_export v1.1.0 - writes chNN-page/lecture_v1_1_0.json from the newest deck plan: v1.0.0's fields (chapter, deck, slides with n, kind, title, say = the notes, concept = the takeaway or subtitle)
plus, on a story slide, "read": {label, url} (the READ card) and, on the resources slide, "links": [{group, label, url, finds}], so that the page chain carries the same labels as the deck.
Usage: sen0401_lecture_export_v1_1_0.py NN <deck file name>"""
__version__ = "1.1.0"
import glob, json, os, re, sys
n, deck = sys.argv[1], sys.argv[2]
T = os.path.dirname(os.path.abspath(__file__))
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
plan = json.load(open(sorted(glob.glob(os.path.join(T, "ch%s-deck" % n, "deck_plan_v*.json")), key=vk)[-1]))
out = {"chapter": int(n), "deck": deck, "slides": []}
for i, s in enumerate(plan["slides"], 1):
    d = {"n": i, "kind": s["kind"], "title": s["title"], "say": s.get("notes", ""), "concept": s.get("take") or s.get("sub", "")}
    for it in s["items"]:
        if it.get("t") == "factrow":
            d["read"] = {"label": it["linkText"], "url": it["link"]}
        if it.get("t") == "links":
            d["links"] = [{"group": g["head"], "label": r[0], "url": r[1], "finds": r[2] if len(r) > 2 else ""} for g in it["groups"] for r in g["rows"]]
    out["slides"].append(d)
os.makedirs(os.path.join(T, "ch%s-page" % n), exist_ok=True)
json.dump(out, open(os.path.join(T, "ch%s-page" % n, "lecture_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
print("lecture_v1_1_0.json: %d slides" % len(out["slides"]))
