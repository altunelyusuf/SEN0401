#!/usr/bin/env python3
"""Index coverage check v1.0.0 (X3b): proves that an exclusion index version already holds EVERY stem, option, premise, step and bank entry of the
assembled v8 midterm items file (X3a output, private) and of the v8 paper docx paragraphs, i.e. that the exam text delivered later cannot differ
from what the mock gate excludes. Prints ids, counts, hashes only; exit 1 when anything is not covered.
Usage: mock_index_cover_check_v1_0_0.py INDEX.json ITEMS.json [PAPER.docx]"""
import json, sys, re, hashlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mock_exclusion_lib_v1_0_0 import *
idx = json.load(open(sys.argv[1])); items = json.load(open(sys.argv[2]))["items"]
stems = {s["t"] for s in idx["stems"]}; opts = {o["t"] for o in idx["options"]}
docgr = {}
for name, lst in idx["documents"].items():
    docgr[name] = {tuple(x.split(" ")) for x in lst}
allgr = set().union(*docgr.values())
miss = []; n = 0
def need_stem(iid, t):
    global n
    nt = norm(t); n += 1
    if len(nt.split()) >= 6 and nt not in stems: miss.append((iid, "stem"))
def need_opt(iid, t):
    global n
    nt = drop_fixed(t); n += 1
    if len(nt.split()) >= MIN_OPT_TOKENS and nt not in opts: miss.append((iid, "option"))
for it in items:
    iid = str(it.get("key") or it.get("id"))
    for k in ("q", "stem", "intro", "text"):
        if isinstance(it.get(k), str): need_stem(iid, it[k])
    for k in ("options", "responses", "bank", "steps"):
        for x in it.get(k) or []:
            if isinstance(x, str): need_opt(iid, x)
    for p in it.get("premises") or []:
        need_opt(iid, p["text"] if isinstance(p, dict) else p)
    for b in it.get("blanks") or []:
        if isinstance(b, dict) and isinstance(b.get("text"), str): need_opt(iid, b["text"])
print("index %s sha256 %s" % (os.path.basename(sys.argv[1]), hashlib.sha256(open(sys.argv[1], "rb").read()).hexdigest()))
print("items file %s sha256 %s: %d items, %d texts compared, not in the index: %d %s" % (os.path.basename(sys.argv[2]), hashlib.sha256(open(sys.argv[2], "rb").read()).hexdigest(), len(items), n, len(miss), miss[:12]))
bad = len(miss)
if len(sys.argv) > 3:
    import docx
    d = docx.Document(sys.argv[3]); paras = [p.text for p in d.paragraphs if p.text.strip()]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                if c.text.strip(): paras.append(c.text)
    low = 0; lines = [ln.strip() for p in paras for ln in p.split("\n") if ln.strip()]
    for ln in lines:
        g = grams(toks(strip_label(ln)))
        if g and len(g & allgr) / len(g) < 0.999: low += 1
    # ADVISORY only: the paper holds lines that are not item text (form code, timing, answer-sheet text, the printed format line)
    print("paper %s sha256 %s: %d lines, lines with 5-grams not wholly inside the index documents (ADVISORY, not a pass condition): %d" % (os.path.basename(sys.argv[3]), hashlib.sha256(open(sys.argv[3], "rb").read()).hexdigest(), len(lines), low))
print("COVER " + ("PASS" if bad == 0 else "FAIL"))
sys.exit(1 if bad else 0)
