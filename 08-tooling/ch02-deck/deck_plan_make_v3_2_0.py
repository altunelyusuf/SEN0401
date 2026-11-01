#!/usr/bin/env python3
"""deck_plan_make v3.2.0 (a NEW tool file): writes deck_plan_v3_2_0.json, the plan that describes the chapter 2 deck v3.2.0 (59 slides) for the arc and honesty checks.
It is DERIVED from deck_plan_v3_1_0.json (read, never written) and from the deck v3.2.0 (notes) and deck_teach_v3_2_0_logs/map.json (old slide -> new slide): the old slides keep their kind, items, takeaway and background;
the 24 concept slides are added as content slides with a takeaway; notes are read from the deck; slide numbers of the analogy list and of the honesty lists are mapped to the new order.
Usage: deck_plan_make_v3_2_0.py"""
import copy, json, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pptx import Presentation
import deck_teach_content_v3_2_0 as C
ROOT = os.path.dirname(os.path.dirname(HERE))
old = json.load(open(os.path.join(HERE, "deck_plan_v3_1_0.json")))
mp = json.load(open(os.path.join(HERE, "deck_teach_v3_2_0_logs", "map.json")))
o2n = {int(k): v for k, v in mp["old_to_new"].items()}; n2o = {v: k for k, v in o2n.items()}; newkey = {v: k for k, v in mp["new"].items()}
deck = Presentation(os.path.join(ROOT, "03-materials/ch02/SEN0401_Ch02_HowBitcoinWorks_3e_v3_2_0.pptx"))
info = {s[0]: s for s in C.SLIDES}
slides = []
for i, s in enumerate(deck.slides, 1):
    notes = s.notes_slide.notes_text_frame.text
    if i in n2o:
        sl = copy.deepcopy(old["slides"][n2o[i] - 1]); sl["n"] = i; sl["notes"] = notes
    else:
        t = info[newkey[i]]
        sl = {"kind": "content", "title": t[1], "sub": t[2], "items": [{"t": "picture", "native": True}], "notes": notes, "bg": "light", "take": t[3], "n": i}
    slides.append(sl)
assert len(slides) == 59
meta = copy.deepcopy(old["meta"]); meta["version"] = "3.2.0"; meta["total"] = len(slides)
for a in meta["analogies"]: a["slide"] = o2n[a["slide"]]
h = meta["honesty"]
for k in ("standin",):
    h[k] = {str(o2n[int(n)]): v for n, v in h[k].items()}
for k in ("notExecuted", "recorded", "vectors"):
    if isinstance(h.get(k), dict): h[k] = {str(o2n[int(n)]): v for n, v in h[k].items()}
    elif isinstance(h.get(k), list): h[k] = [o2n[x] if isinstance(x, int) else x for x in h[k]]
meta["v3_2_0"] = "teach build: 24 concept slides added, stories told as sentences, no run below 9 pt"
json.dump({"meta": meta, "slides": slides}, open(os.path.join(HERE, "deck_plan_v3_2_0.json"), "x"), indent=1, ensure_ascii=False)
print("written deck_plan_v3_2_0.json:", len(slides), "slides")
