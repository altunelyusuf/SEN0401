#!/usr/bin/env python3
"""pages_deck_links_make v1_1_0 (SEN0401 chapter pages 1 to 7). For one chapter NN:
(1) chNN-page/lecture_v1_1_1.json from lecture_v1_1_0.json (the deck export, untouched): the deck's one-line takeaway moves from "concept" to "takeaway", and a story slide's "concept" becomes the first concept of its
story (stories module sen0401_chNN_stories_v1_1_0 or 1_5_0, the slide found through READ in sen0401_links_v1_1_0.py) that is a concept of the page, because the page's Lecture tab wants a page concept id there;
(2) chNN-page/resources_v1_1_0.json from resources_v1_0_0.json: an entry whose address is one of the deck's resources rows takes the deck's label and its one line of what the reader finds; every other entry stays as it was
(the page's Resources list is longer than the deck's and was never the deck's list).
Usage: pages_deck_links_make_v1_1_0.py NN"""
__version__ = "1.1.0"
import glob, importlib, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); NN = sys.argv[1]; n = int(NN); P = os.path.join(H, "ch%s-page" % NN)
import sen0401_links_v1_1_0 as L
lec = json.load(open(os.path.join(P, "lecture_v1_1_0.json")))
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
nodes = {x["id"] for x in json.load(open(sorted(glob.glob(os.path.join(P, "page_data_v*.json")), key=vk)[-1]))["nodes"]}
mod = importlib.import_module(os.path.basename(sorted(glob.glob(os.path.join(H, "sen0401_ch%s_stories_v*.py" % NN)), key=vk)[-1])[:-3])
story = {s["id"]: s for s in mod.STORIES}
k = 0
for s in lec["slides"]:
    s["takeaway"] = s.pop("concept", "")
    if (n, s["n"]) in L.READ:
        sid = L.READ[(n, s["n"])][0]
        c = next((c for c in story[sid]["concepts"] if c in nodes), None)
        assert c, sid
        s["concept"] = c; k += 1
lec["_note"] = "lecture_v1_1_0.json (the deck export of the chapter %s deck, untouched) with the deck's takeaway as takeaway and, on each story slide, the first concept of the story that the page has as concept; made by pages_deck_links_make_v1_1_0.py" % NN
json.dump(lec, open(os.path.join(P, "lecture_v1_1_1.json"), "w"), indent=1, ensure_ascii=False)
old = json.load(open(os.path.join(P, "resources_v1_0_0.json"))); reg = json.load(open(os.path.join(H, "ch%s-deck" % NN, "link_register_v1_0_0.json")))
rows = {r["new_url"]: r for r in reg["links"] if r["place"].startswith("resources")}
fin = {l["url"]: l.get("finds", "") for s in lec["slides"] for l in s.get("links", [])}
out = []; m = 0
for l in old["links"]:
    l = dict(l)
    if l["url"] in rows:
        l["title"] = rows[l["url"]]["new_label"]; l["why"] = fin.get(l["url"]) or l["why"]; m += 1
    out.append(l)
old["links"] = out; old["_version"] = "1.1.0"
old["_note"] = (old.get("_note", "") + " 1.1.0: %d entr%s whose address is a row of the deck's resources slide carry the deck's label and its line of what the reader finds (deck link register 08-tooling/ch%s-deck/link_register_v1_0_0.json)." % (m, "y" if m == 1 else "ies", NN)).strip()
json.dump(old, open(os.path.join(P, "resources_v1_1_0.json"), "w"), indent=1, ensure_ascii=False)
print("chapter %s: lecture %d slides, %d with a concept; resources %d, %d relabelled" % (NN, len(lec["slides"]), k, len(out), m))
