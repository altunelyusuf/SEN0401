#!/usr/bin/env python3
"""Proof of the chapter 3 deck 3.1.0 against 3.0.0 (task TK_Ch03_DeckCode_Build): the old deck's SHA-256, the 64 code lines (prompts stripped) equal the new code lines in order,
no line starts with '>>> ' or '... ', every old result row stands in a result shape with the same text, every other slide part is byte-identical, the hyperlink count is unchanged.
Usage: deck_proof_v3_1_0.py OLD.pptx NEW.pptx   Exit 0 only when all hold."""
import sys, zipfile, hashlib, re
sys.dont_write_bytecode = True
sys.path.insert(0, "/home/claude/sen0401/08-tooling")
import sen0401_code_marker_v1_0_0 as M
from xml.dom import minidom
old, new = sys.argv[1:3]; zo, zn = zipfile.ZipFile(old), zipfile.ZipFile(new); ok = True
def say(k, v, good=True):
    global ok; ok &= good; print(("PASS " if good else "FAIL ") + k + " | " + str(v))
def slides(z): return sorted((n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)), key=lambda n: int(re.findall(r"\d+", n)[-1]))
def paras(z, n):
    d = minidom.parseString(z.read(n)); out = []
    for sp in d.getElementsByTagName("p:sp"):
        nm = sp.getElementsByTagName("p:cNvPr")[0].getAttribute("name")
        out.append((nm, ["".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in sp.getElementsByTagName("a:p")]))
    return out
oc, orr, nc, nr, same, diff = [], [], [], [], 0, []
for n in slides(zo):
    if zo.read(n) == zn.read(n): same += 1; continue
    diff.append(n)
    last = None
    for nm, ps in paras(zo, n):
        for p in ps:
            if p.startswith((">>> ", "... ")): oc.append(p[4:]); last = p[4:]
            elif last is not None and any(q.startswith(">>> ") for q in ps): orr.append((last, p))
    for sh in M.xml_shapes(minidom.parseString(zn.read(n))):
        if M.is_code_name(sh["name"]): nc += sh["paras"]
        if M.is_result_name(sh["name"]):
            r = M.split_result("\n".join(sh["paras"]))
            if r: nr.append(r)
say("old deck SHA-256", hashlib.sha256(open(old, "rb").read()).hexdigest())
say("new deck SHA-256", hashlib.sha256(open(new, "rb").read()).hexdigest())
say("slides changed / unchanged byte for byte", "%d / %d" % (len(diff), same), len(diff) == 19)
say("code lines old (prompts stripped) == new, in order", "%d vs %d" % (len(oc), len(nc)), oc == nc and len(oc) == 64)
say("no code line starts with '>>> ' or '... '", sum(1 for l in nc if l.startswith((">>> ", "... "))), not any(l.startswith((">>> ", "... ")) for l in nc))
say("old result rows == new result shapes (expression and text)", "%d vs %d" % (len(orr), len(nr)), orr == nr and len(orr) == 19)
parts_same = all(zo.read(i.filename) == zn.read(i.filename) for i in zo.infolist() if i.filename not in diff) and [i.filename for i in zo.infolist()] == [i.filename for i in zn.infolist()]
say("every part other than the 19 changed slides byte-identical, same part list", parts_same, parts_same)
def links(z): return sum(len(re.findall(rb"<Relationship [^>]*Type=\"[^\"]*/hyperlink\"", z.read(n))) for n in z.namelist() if n.endswith(".rels"))
say("hyperlink relationships old vs new", "%d vs %d" % (links(zo), links(zn)), links(zo) == links(zn))
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
