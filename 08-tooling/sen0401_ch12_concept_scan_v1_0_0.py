#!/usr/bin/env python3
"""Scan: primary-source concept labels of the chapter 12 research (newest) against those of every other chapter's research (every version, same normalisation as the deck standard check).
Prints the labels shared with each chapter. Usage: python3 -B sen0401_ch12_concept_scan_v1_0_0.py"""
import re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def norm(t):
    t = re.sub(r"\([^)]*\)", " ", t.lower()); t = re.sub(r"[^a-z0-9]+", " ", t).split()
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") else w for w in t)
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
def labs(f):
    return re.findall(r"a sen04(?:01|14):PrimarySourceConcept\s*;\s*rdfs:label\s+\"((?:[^\"\\]|\\.)*)\"", open(f, encoding="utf-8").read())
fs = sorted(glob.glob(os.path.join(ROOT, "03-materials/ch12/rdodi/sen0401_ch12_research_v*.ttl")), key=vk)
print("chapter 12 research read:", os.path.relpath(fs[-1], ROOT))
mine = {norm(l): l for l in labs(fs[-1])}
print("concepts:", len(labs(fs[-1])), "distinct by normalised label:", len(mine))
total = 0
for n in range(1, 15):
    if n == 12: continue
    allf = sorted(glob.glob(os.path.join(ROOT, "03-materials/ch%02d/rdodi/sen0401_ch%02d_research_v*.ttl" % (n, n))), key=vk)
    if not allf: print("chapter %02d: no research file" % n); continue
    new = {norm(l) for l in labs(allf[-1])}; anyv = set()
    for f in allf: anyv |= {norm(l) for l in labs(f)}
    sh = [mine[k] for k in mine if k in anyv]; total += len(sh)
    print("chapter %02d: newest %s has %d concepts; shared with chapter 12 (newest): %s; (any version): %s" % (n, os.path.basename(allf[-1]), len(new), [mine[k] for k in mine if k in new], sh))
print("TOTAL shared labels:", total)
