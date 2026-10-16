#!/usr/bin/env python3
"""pages_deck_links_make v1_0_0 (SEN0401 chapter pages 8 to 14). For one chapter NN: (1) resources_v1_1_0.json in chNN-page, the page's Resources list rebuilt from the deck's resources slide in lecture_v1_1_0.json
(label, url, what it finds), keeping the kind and the concept each link had in resources_v1_0_0.json (matched by address; a link whose address changed is matched to the old link of the same kind of place);
(2) nothing else is written. Usage: pages_deck_links_make_v1_0_0.py NN"""
__version__ = "1.0.0"
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); NN = sys.argv[1]; P = os.path.join(H, "ch%s-page" % NN)
old = json.load(open(os.path.join(P, "resources_v1_0_0.json")))
lec = json.load(open(os.path.join(P, "lecture_v1_1_0.json"))); new = [s for s in lec["slides"] if s.get("links")][0]["links"]
reg = json.load(open(os.path.join(H, "ch%s-deck" % NN, "link_register_v1_0_0.json")))
COMPAT = {"Read": {"documentation", "corpus"}, "Standards and papers": {"standard", "seminal"}, "Watch": {"video"}, "Community": {"community"}}
byu = {l["url"]: l for l in old["links"]}; left = [l for l in old["links"] if l["url"] not in {n["url"] for n in new}]; out = []
for n in new:
    o = byu.get(n["url"])
    if o is None:
        o = next((l for l in left if l["kind"] in COMPAT[n["group"]]), None)
        if o is None: raise SystemExit("no old link for %s" % n["url"])
        left.remove(o)
    out.append({"kind": o["kind"], "title": n["label"], "url": n["url"], "source": n["url"].split("/")[2].replace("www.", ""), "why": n.get("finds") or o["why"], "concept": o["concept"]})
assert not left and len(out) == len(old["links"])
json.dump({"_version": "1.1.0", "checked": reg["checked"], "links": out, "_note": "The links of the chapter %s deck's resources slide as the deck v1.1.0 gives them (label, address and what each one finds; deck link register 08-tooling/ch%s-deck/link_register_v1_0_0.json, checked %s). Kind and concept are those of resources_v1_0_0.json." % (NN, NN, reg["checked"])}, open(os.path.join(P, "resources_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
print("resources", NN, len(out))
