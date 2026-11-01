#!/usr/bin/env python3
"""deck_plan_make v3.4.0 (a NEW tool file; task TK_Ch01_DeckTeach_Build): writes deck_plan_v3_4_0.json, the plan that describes the chapter 1 deck v3.4.0 for the arc check (which reads plan and file together).
DERIVED from the plan v3_3_0 (read, never written) and from the deck v3.4.0: the 62 earlier slides keep their kind, items, takeaway and background; the 14 picture slides are added as content slides with a takeaway;
the story slides keep their fact row (the same facts now stand in the story sentences) but lose the label beats; the notes of every slide are read from the deck; the analogy slide numbers follow the new order.
Usage: deck_plan_make_v3_4_0.py DECK PLAN_OLD PLAN_NEW"""
import copy, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import deck_teach_v3_4_0 as B
from pptx import Presentation
deck_path, plan_old, plan_new = sys.argv[1:4]
old = json.load(open(plan_old)); deck = Presentation(deck_path)
new_titles = {p[2]: p for p in B.PICS}
slides = []; oldpos = {}; k = 0
for i, s in enumerate(deck.slides, 1):
    title = next((sh.text_frame.text for sh in s.shapes if sh.has_text_frame and sh.left // 9144 == 125 and sh.top // 9144 == 26), "")
    notes = s.notes_slide.notes_text_frame.text
    if title in new_titles:
        p = new_titles[title]
        slides.append({"kind": "content", "title": title, "sub": p[3], "items": [{"t": "picture", "native": True}], "notes": notes, "bg": "light", "take": p[4]})
    else:
        sl = copy.deepcopy(old["slides"][k]); oldpos[k + 1] = i; k += 1
        sl["notes"] = notes
        if any(it.get("t") == "factrow" for it in sl["items"]):
            sl["items"] = [it for it in sl["items"] if it.get("t") != "beats"]
        slides.append(sl)
assert k == 62, k
meta = copy.deepcopy(old["meta"]); meta["version"] = "3.4.0"; meta["total"] = len(slides)
meta["sub"] = "SEN0401, third-edition chapter 1: every concept understandable from the slides, stories told as sentences, results as visuals"
for a in meta["analogies"]: a["slide"] = oldpos[a["slide"]]
json.dump({"meta": meta, "slides": slides}, open(plan_new, "x"), indent=1, ensure_ascii=False)
print("written", plan_new, ":", len(slides), "slides")
