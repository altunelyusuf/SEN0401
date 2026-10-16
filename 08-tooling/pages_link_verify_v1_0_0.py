#!/usr/bin/env python3
"""pages_link_verify v1_0_0 (SEN0401 chapter pages 8 to 14). Usage: pages_link_verify_v1_0_0.py NN PAGEVER
Checks that every READ card and resource of the chapter's deck link register (chNN-deck/link_register_v1_0_0.json: new_label, new_url) is carried by the page: the label and the address together in the page's story
(linkLabel, link), lecture (read, links) or resources (title, url) data, and the label and the address both present in the built page file. Prints the entries it cannot match."""
import json, os, sys
H = os.path.dirname(os.path.abspath(__file__)); NN, PV = sys.argv[1], sys.argv[2]
reg = json.load(open(os.path.join(H, "ch%s-deck" % NN, "link_register_v1_0_0.json")))
d = json.load(open(os.path.join(H, "ch%s-page" % NN, "page_data_v%s.json" % PV)))
html = open(os.path.join(H, "..", "03-materials", "ch%s" % NN, "page", "sen0401_ch%s_page_v%s.html" % (NN, PV))).read()
pairs = {(s.get("linkLabel"), s.get("link")) for s in d["stories"]} | {(r["title"], r["url"]) for r in d["resources"]}
for s in d["lecture"]["slides"] if isinstance(d["lecture"], dict) and "slides" in d["lecture"] else d["lecture"]:
    if s.get("read"): pairs.add((s["read"]["label"], s["read"]["url"]))
    for l in s.get("links") or []: pairs.add((l["label"], l["url"]))
bad = 0
for e in reg["links"]:
    ok = (e["new_label"], e["new_url"]) in pairs; inpage = e["new_label"].replace("&", "&amp;") in html or e["new_label"] in html
    if not (ok and inpage and e["new_url"] in html): bad += 1; print("NOT CARRIED", e["slide"], e["place"], e["new_label"], e["new_url"], ok, inpage)
print("chapter %s: %d register entries, %d not carried" % (NN, len(reg["links"]), bad)); sys.exit(1 if bad else 0)
