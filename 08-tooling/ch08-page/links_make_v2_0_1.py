#!/usr/bin/env python3
"""links_make v2_0_1 (chapter 8, adapted copy of pages_deck_links_make_v1_3_0, which is unchanged) (SEN0401 chapter pages 1 to 7, after the decks were corrected: new story pictures, new links, new watch videos, stories v1.2.0).
For one chapter NN, from the deck agent's NEWEST lecture export chNN-page/lecture_vX_Y_0.json (committed, untouched; the deck named inside it) and the newest stories module:
(1) chNN-page/lecture_vX_Y_1.json: as pages_deck_links_make_v1_1_0 did for the older export - the deck's one-line takeaway moves from "concept" to "takeaway", and a story slide ("read" card) gets as "concept" the first concept
    of its story (the story whose title or link the slide shows) that is a concept of the page. Nothing else is changed; the deck's links, labels and honesty fields are carried as the export has them.
(2) chNN-page/resources_v1_2_0.json from resources_v1_1_0.json: an entry whose address is a link of the deck's resources slide takes the deck's label and line of what the reader finds; an entry whose address the deck has
    replaced (the old deck address is in the previous export) takes the replacing link of the deck (same group, found by label or, when the group has one replacement, by group); a link of the deck's resources slide that the page
    list does not yet have is added (kind from the deck's group, source from the address, why from the deck's line, concept from the label or the chapter's first concept). Every other entry stays as it was.
Usage: ch08 links_make_v2_0_1.py NN"""
__version__ = "1.3.0"
import glob, importlib, json, os, re, sys
from urllib.parse import urlparse
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, H); NN = sys.argv[1]; P = os.path.join(H, "ch%s-page" % NN)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
raws = [p for p in glob.glob(os.path.join(P, "lecture_v*_0.json"))]; raw = sorted(raws, key=vk)[-1]; v = vk(raw)
lec = json.load(open(raw)); prev = json.load(open(os.path.join(P, "lecture_v1_1_1.json")))
pd = json.load(open(sorted(glob.glob(os.path.join(P, "page_data_v*.json")), key=vk)[-1])); nodes = {x["id"]: x for x in pd["nodes"]}
mod = importlib.import_module(os.path.basename(sorted(glob.glob(os.path.join(H, "sen0401_ch%s_stories_v*.py" % NN)), key=vk)[-1])[:-3])
k = 0
for s in lec["slides"]:
    s["takeaway"] = s.pop("concept", "")
    if s.get("read"):
        st = next((x for x in mod.STORIES if x["title"] == s["title"] or x.get("link") == s["read"]["url"]), None)
        if st is None: raise SystemExit("slide %d shows a story the stories module does not have: %r" % (s["n"], s["title"]))
        c = next((c for c in st["concepts"] if c in nodes), None); assert c, st["id"]; s["concept"] = c; k += 1
lec["_note"] = "%s (the deck export of the chapter %s deck, untouched) with the deck's takeaway as takeaway and, on each story slide, the first concept of the story that the page has as concept; made by ch08 links_make_v2_0_1.py" % (os.path.basename(raw), NN)
out_l = os.path.join(P, "lecture_v%d_%d_1.json" % (v[0], v[1])); json.dump(lec, open(out_l, "w"), indent=1, ensure_ascii=False)
links = lambda L: [l for s in L["slides"] for l in s.get("links", [])]
new = links(lec); old = links(prev); nu = {l["url"]: l for l in new}; ou = {l["url"]: l for l in old}
res = json.load(open(os.path.join(P, "resources_v1_1_0.json")))
KIND = lambda g, u: "video" if "youtube" in u else "standard" if re.search(r"standard|bip", g, re.I) or "bips.dev" in u else "seminal" if re.search(r"seminal|papers", g, re.I) else "community" if re.search(r"communit", g, re.I) else "documentation"
out = []; relabel = repl = added = 0; have = set()
for r in res["links"]:
    r = dict(r)
    if r["url"] in nu:
        d = nu[r["url"]]; r["title"] = d["label"]; r["why"] = d.get("finds") or r["why"]; relabel += 1
    elif r["url"] in ou:
        o = ou[r["url"]]
        cand = [l for u, l in nu.items() if u not in ou and (l["label"].split(":")[-1].strip() == o["label"].split(":")[-1].strip() or l["group"] == o["group"])]
        if len(cand) == 1:
            d = cand[0]; r["url"] = d["url"]; r["title"] = d["label"]; r["why"] = d.get("finds") or r["why"]; r["source"] = urlparse(d["url"]).netloc.replace("www.", ""); repl += 1
        else: print("  deck address replaced but not matched uniquely:", o["label"], [c["label"] for c in cand])
    have.add(r["url"]); out.append(r)
root = pd["nodes"][0]["id"]
def concept_for(lbl):
    w = [x for x in re.findall(r"[A-Za-z]{4,}", lbl.lower()) if x not in ("bitcoin", "guide", "news", "spec", "video", "text")]
    for nid, n in nodes.items():
        if any(x in n["label"].lower() for x in w): return nid
    return root
for l in new:
    if l["url"] in have: continue
    out.append({"kind": KIND(l["group"], l["url"]), "title": l["label"], "url": l["url"], "source": urlparse(l["url"]).netloc.replace("www.", ""), "why": l.get("finds", ""), "concept": concept_for(l["label"])}); have.add(l["url"]); added += 1
res["links"] = out; res["_version"] = "1.2.0"
res["_note"] = (res.get("_note", "") + " 1.2.0 (after the chapter 8 deck 2.0.0 rebuild, from %s): %d entries carry the deck's label and line, %d replaced addresses follow the deck, %d deck links added that the list did not have." % (os.path.basename(raw), relabel, repl, added))
json.dump(res, open(os.path.join(P, "resources_v1_2_0.json"), "w"), indent=1, ensure_ascii=False)
print("chapter %s: %s -> %s: %d story slides with a concept; resources %d (relabelled %d, replaced %d, added %d)" % (NN, os.path.basename(raw), os.path.basename(out_l), k, len(out), relabel, repl, added))
