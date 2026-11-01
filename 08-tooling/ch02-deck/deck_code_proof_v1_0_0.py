#!/usr/bin/env python3
"""Proof of deck_code_v3_1_0.py (task TK_Ch02_DeckCode_Build): old deck v3_0_0 against new deck v3_1_0, printed as it measures.
(1) SHA-256 of the old deck; (2) the 50 code lines of the old deck, prompts stripped, equal the code lines of the new deck, in order, and no code box line starts with '>>> ' or '... ';
(3) every old result row equals the value of a result shape, in order; (4) every zip member other than the 14 changed slides is byte-identical; (5) per changed slide, the text outside code and result shapes is the same."""
import hashlib, re, sys, zipfile
from xml.dom import minidom
sys.dont_write_bytecode = True
OLD, NEW = sys.argv[1], sys.argv[2]
zo, zn = zipfile.ZipFile(OLD), zipfile.ZipFile(NEW)
print("SHA-256 old:", hashlib.sha256(open(OLD, "rb").read()).hexdigest())
no = lambda z: sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)), key=lambda n: int(re.findall(r"\d+", n)[0]))
def paras(z, n):
    d = minidom.parseString(z.read(n)); out = []
    for sp in d.getElementsByTagName("p:sp"):
        nm = sp.getElementsByTagName("p:cNvPr")[0].getAttribute("name")
        out.append((nm, ["".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in sp.getElementsByTagName("a:p")]))
    return out
ok = True
old_code, new_code, old_res, new_res, changed = [], [], [], [], []
for n in no(zo):
    po, pn = paras(zo, n), paras(zn, n)
    has_old = any(p and p[0].startswith(">>> ") for _, p in po)
    if not has_old:
        same = zo.read(n) == zn.read(n); ok &= same
        if not same: print("FAIL unchanged slide differs:", n)
        continue
    changed.append(n)
    for nm, p in po:
        if p and p[0].startswith(">>> "):
            rows = p
            for i, l in enumerate(rows):
                if l.startswith(">>> ") or l.startswith("... "): old_code.append(l[4:])
                else: old_res.append(l)
    for nm, p in pn:
        if nm.startswith("code"): new_code += p
        if nm.startswith("result"): new_res.append(p)
    rest_o = [(nm, p) for nm, p in po if not (p and p[0].startswith(">>> "))]
    rest_n = [(nm, p) for nm, p in pn if not (nm.startswith("code") or nm.startswith("result"))]
    if rest_o != rest_n: ok = False; print("FAIL other text differs on", n)
print("changed slides: %d" % len(changed))
print("code lines old (prompts stripped): %d, new: %d, equal in order: %s" % (len(old_code), len(new_code), old_code == new_code)); ok &= old_code == new_code
bad = [l for l in new_code if l.startswith(">>> ") or l.startswith("... ")]
print("new code lines that start with a prompt: %d" % len(bad)); ok &= not bad
vals = [r.split("  →  ", 1)[1] for r in ["\n".join(p) for p in new_res]]
print("old result rows: %d, result shapes: %d, values equal in order: %s" % (len(old_res), len(vals), old_res == vals)); ok &= old_res == vals
others_old = {n: zo.read(n) for n in zo.namelist() if n not in changed}; others_new = {n: zn.read(n) for n in zn.namelist() if n not in changed}
same_members = others_old == others_new
print("zip members: old %d, new %d; members other than the changed slides byte-identical: %s" % (len(zo.namelist()), len(zn.namelist()), same_members)); ok &= same_members
print("PROOF", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
