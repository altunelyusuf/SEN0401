#!/usr/bin/env python3
"""pages_deck_match_verify v1_0_0 (SEN0401 chapter pages 1 to 7). Usage: pages_deck_match_verify_v1_0_0.py NN PAGEVER (e.g. 01 9_70_0).
Checks the page data of the page against the deck's newest lecture export and stories module: every slide's READ card and resources-slide link (label, address, line of what the reader finds) is carried in the page's lecture;
every story of the stories module is a story card of the page with the same date, link, link label, picture and credit; every deck resources link is in the page's resource list; reports what is not carried."""
import glob, importlib, json, os, re, sys
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); NN, PV = sys.argv[1], sys.argv[2]; P = os.path.join(H, "ch%s-page" % NN)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
raw = sorted(glob.glob(os.path.join(P, "lecture_v*_0.json")), key=vk)[-1]; lec = json.load(open(raw))["slides"]
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV)))
mod = importlib.import_module(os.path.basename(sorted(glob.glob(os.path.join(H, "sen0401_ch%s_stories_v*.py" % NN)), key=vk)[-1])[:-3])
miss = []; n = 0
pl = {s["n"]: s for s in d["lecture"]}
for s in lec:
    ps = pl.get(s["n"])
    if ps is None: miss.append("slide %d missing" % s["n"]); continue
    if s.get("read"):
        n += 1
        if ps.get("read") != s["read"]: miss.append("slide %d READ differs: %r vs %r" % (s["n"], ps.get("read"), s["read"]))
    for l in s.get("links", []):
        n += 1
        if l not in ps.get("links", []): miss.append("slide %d link not carried: %s" % (s["n"], l["label"]))
res = {r["url"] for r in d["resources"]}
for l in [l for s in lec for l in s.get("links", [])]:
    if l["url"] not in res: miss.append("resource list lacks %s" % l["url"])
cards = {c["id"]: c for c in d["stories"]}
for s in mod.STORIES:
    c = cards.get(s["id"]); n += 1
    if c is None: miss.append("story %s not a card" % s["id"]); continue
    for k in ("when", "link", "linkLabel", "who", "where", "source"):
        if k in s and c.get(k) != s[k]: miss.append("story %s field %s differs" % (s["id"], k))
print("chapter %s page %s: %d items compared with %s and %s; not carried: %d" % (NN, PV, n, os.path.basename(raw), mod.__name__, len(miss)))
for m in miss: print("  ", m)
