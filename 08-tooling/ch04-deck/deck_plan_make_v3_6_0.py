#!/usr/bin/env python3
"""deck_plan_make v3.6.0 (a NEW tool file; task TK_Ch04_DeckTeach_Build): writes deck_plan_v3_6_0.json, the plan that describes the chapter 4 deck v3.6.0 for the arc check (which reads plan and file together).
DERIVED from the plan v3_5_0 (read, never written), the deck map (deck_v3_6_0_map.json) and the deck: the 42 earlier slides keep kind, items, takeaway and background; the 32 picture slides are content slides with a takeaway;
the story slides keep their fact row but lose the label beats; notes are read from the deck; the analogy slide numbers follow the new order.
Usage: deck_plan_make_v3_6_0.py DECK PLAN_OLD MAP PLAN_NEW"""
import copy, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_teach_specs_v3_6_0 as SL
from pptx import Presentation
deck_path, plan_old, mp, plan_new = sys.argv[1:5]
old = json.load(open(plan_old)); m = json.load(open(mp)); deck = Presentation(deck_path)
o2n = {int(k): v for k, v in m["old_to_new"].items()}; n2o = {v: k for k, v in o2n.items()}
spec = {s[1]: s for s in SL.SPECS}; newkey = {v: k for k, v in m["new"].items()}
slides = []
for i, s in enumerate(deck.slides, 1):
    notes = s.notes_slide.notes_text_frame.text
    if i in newkey:
        p = spec[newkey[i]]
        slides.append({"kind": "content", "title": p[2], "sub": p[3], "items": [{"t": "picture", "native": True}], "notes": notes, "bg": "light", "take": p[4]})
    else:
        sl = copy.deepcopy(old["slides"][n2o[i] - 1]); sl["notes"] = notes
        if any(it.get("t") == "factrow" for it in sl["items"]): sl["items"] = [it for it in sl["items"] if it.get("t") != "beats"]
        slides.append(sl)
meta = copy.deepcopy(old["meta"]); meta["version"] = "3.6.0"; meta["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"; meta["total"] = len(slides)
meta["sub"] = "SEN0401, third-edition chapter 4: every concept understandable from the slides, stories told as sentences, results as visuals"
for a in meta["analogies"]: a["slide"] = o2n[a["slide"]]
json.dump({"meta": meta, "slides": slides}, open(plan_new, "x"), indent=1, ensure_ascii=False)
print("written", plan_new, ":", len(slides), "slides")
