#!/usr/bin/env python3
"""Derives lecture_v1_4_1.json from lecture_v1_4_0.json exactly as step (1) of pages_deck_links_make_v1_3_0.py does (takeaway, story-slide concept); it does not write resources_v1_3_0.json (a committed file), the deck links being identical to those of lecture_v1_3_0.json."""
import importlib, json, os, sys
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H); P = os.path.join(H, "ch07-page")
lec = json.load(open(os.path.join(P, "lecture_v1_4_0.json")))
pd = json.load(open(os.path.join(P, "page_data_v9_84_0.json"))); nodes = {x["id"]: x for x in pd["nodes"]}
mod = importlib.import_module("sen0401_ch07_stories_v1_2_0"); k = 0
for s in lec["slides"]:
    s["takeaway"] = s.pop("concept", "")
    if s.get("read"):
        st = next((x for x in mod.STORIES if x["title"] == s["title"] or x.get("link") == s["read"]["url"]), None)
        if st is None: raise SystemExit("slide %d shows a story the stories module does not have" % s["n"])
        s["concept"] = next(c for c in st["concepts"] if c in nodes); k += 1
lec["_note"] = "lecture_v1_4_0.json (the deck export of the chapter 07 deck v2_2_0, untouched) with the deck's takeaway as takeaway and, on each story slide, the first concept of the story that the page has as concept; made by ch07-page/lecture_derive_v1_4_1.py"
json.dump(lec, open(os.path.join(P, "lecture_v1_4_1.json"), "w"), indent=1, ensure_ascii=False); print("lecture_v1_4_1.json: %d story slides with a concept" % k)
