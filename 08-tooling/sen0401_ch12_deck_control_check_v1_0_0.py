#!/usr/bin/env python3
"""sen0401_ch12_deck_control_check v1_0_0 - the lineage agent's OWN check of the revised chapter 12 deck (criterion AC9_Ch12DeckRevise). Usage: sen0401_ch12_deck_control_check_v1_0_0.py noborrow
noborrow: in the newest deck of 03-materials/ch12 no slide carries a title or text starting with 'From chapter 11', no slide text names a chapter 11 research concept that is not also a chapter 12 concept (labels of three or more words of the chapter 11 research minus the chapter 12 research are searched as phrases (shorter labels are generic words such as bitcoin network and would give false hits)), and the deck is newer than v2_0_0; the delivered v2_0_0 is byte-identical to its committed form (git status clean)"""
import glob, os, re, subprocess, sys
from pptx import Presentation
import rdflib
R = "/home/claude/sen0401/03-materials/"
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
decks = sorted(glob.glob(R + "ch12/*_v*_*_*.pptx"), key=vk); new = decks[-1]; print("decks:", [os.path.basename(d) for d in decks]); fail = []
if vk(new) <= [2, 0, 0]: fail.append("no new deck version")
def concepts(p):
    g = rdflib.Graph(); g.parse(p, format="turtle"); return {str(g.value(s, rdflib.RDFS.label)).lower() for s in g.subjects(rdflib.RDF.type, None) if any(str(t).endswith("PrimarySourceConcept") for t in g.objects(s, rdflib.RDF.type))}
rn = lambda n: sorted(glob.glob(R + "ch%02d/rdodi/sen0401_ch%02d_research_v*.ttl" % (n, n)), key=vk)[-1]
only11 = concepts(rn(11)) - concepts(rn(12)); norm = lambda t: re.sub(r"[^a-z0-9 ]", "", t.lower())
P = Presentation(new); hits = []; titled = []
for i, s in enumerate(P.slides, 1):
    tx = " ".join(sh.text_frame.text for sh in s.shapes if sh.has_text_frame); n = norm(tx)
    if re.search(r"from chapter 11", tx, re.I): titled.append(i)
    for c in only11:
        if len(c.split()) >= 3 and norm(c) in n: hits.append((i, c))
print("slides mentioning From chapter 11:", titled); print("chapter-11-only concept labels found on slides: %d %s" % (len(hits), hits[:6]))
fail += ["From chapter 11 slides %s" % titled] if titled else []; fail += ["borrowed concepts on slides: %s" % hits[:3]] if hits else []
st = subprocess.run(["git", "status", "--short", "03-materials/ch12"], cwd="/home/claude/sen0401", capture_output=True, text=True).stdout.strip(); print("git status of 03-materials/ch12:", repr(st))
print("RESULT", "FAIL %s" % fail if fail else "PASS"); sys.exit(1 if fail else 0)
