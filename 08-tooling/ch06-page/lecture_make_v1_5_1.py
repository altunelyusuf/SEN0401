#!/usr/bin/env python3
"""lecture_make v1_5_1 (chapter 6): from lecture_v1_5_0.json (the deck export of v2_4_2, untouched) writes lecture_v1_5_1.json in the page's format, as pages_deck_links_make_v1_3_0 did for v1_3_1: the deck's takeaway moves from 'concept' to 'takeaway' and a story slide ('read' card) gets as 'concept' the first concept of its story that the page has. Nothing else changes. Resources are not touched."""
import glob, importlib, json, os, re, sys
H = "/home/claude/sen0401/08-tooling"; sys.path.insert(0, H); P = H + "/ch06-page"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
lec = json.load(open(P + "/lecture_v1_5_0.json"))
pd = json.load(open(sorted(glob.glob(P + "/page_data_v*.json"), key=vk)[-1])); nodes = {x["id"] for x in pd["nodes"]}
mod = importlib.import_module(os.path.basename(sorted(glob.glob(H + "/sen0401_ch06_stories_v*.py"), key=vk)[-1])[:-3]); k = 0
for s in lec["slides"]:
    s["takeaway"] = s.pop("concept", "")
    if s.get("read"):
        st = next((x for x in mod.STORIES if x["title"] == s["title"] or x.get("link") == s["read"]["url"]), None)
        if st is None: raise SystemExit("slide %d shows a story the stories module does not have: %r" % (s["n"], s["title"]))
        c = next((c for c in st["concepts"] if c in nodes), None); assert c; s["concept"] = c; k += 1
lec["_note"] = "lecture_v1_5_0.json (the deck export of the chapter 6 deck v2_4_2, untouched) with the deck's takeaway as takeaway and, on each story slide, the first concept of the story that the page has as concept; made by lecture_make_v1_5_1.py"
json.dump(lec, open(P + "/lecture_v1_5_1.json", "w"), indent=1, ensure_ascii=False); print("lecture_v1_5_1.json: %d slides, %d story slides with a concept" % (len(lec["slides"]), k))
