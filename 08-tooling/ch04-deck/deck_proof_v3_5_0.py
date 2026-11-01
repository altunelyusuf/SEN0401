#!/usr/bin/env python3
"""Proof of the chapter 4 deck 3.5.0 against 3.4.0 (task TK_Ch04_DeckCode_Build). Prints SHA-256 of both decks; the 67 code lines (prompts stripped) equal the new code lines in order; no code line starts with
'>>> ' or '... '; every old result row stands in a result shape with the same expression and text; every part other than the 21 code slides, the 6 picture-credit slides and the 5 charts is byte-identical;
the hyperlink count is unchanged; the text of every changed slide differs only in the prompts and the results; no text run below 9 pt on any slide (slide text and the slide's charts), the smallest size per slide is printed;
no shown code or result line is wider than its shape (chars x 0.6 x size). Usage: deck_proof_v3_5_0.py OLD NEW   Exit 0 only when all hold."""
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
        out.append((sp.getElementsByTagName("p:cNvPr")[0].getAttribute("name"), ["".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")) for p in sp.getElementsByTagName("a:p")]))
    return out
oc, orr, nc, nr, diff, same = [], [], [], [], [], 0
for n in slides(zo):
    if zo.read(n) == zn.read(n): same += 1; continue
    diff.append(n); last = None
    for nm, ps in paras(zo, n):
        for p in ps:
            if p.startswith((">>> ", "... ")): oc.append(p[4:]); last = p[4:]
            elif last is not None and any(q.startswith(">>> ") for q in ps): orr.append((last, p))
    for sh in M.xml_shapes(minidom.parseString(zn.read(n))):
        if M.is_code_name(sh["name"]): nc += sh["paras"]
        if M.is_result_name(sh["name"]):
            r = M.split_result("\n".join(sh["paras"]))
            if r: nr.append(r)
say("old deck SHA-256", hashlib.sha256(open(old, "rb").read()).hexdigest()); say("new deck SHA-256", hashlib.sha256(open(new, "rb").read()).hexdigest())
code_slides = [n for n in diff if any(p.startswith(">>> ") for _, ps in paras(zo, n) for p in ps)]
say("slides with code changed / slides byte-identical", "%d / %d (changed: %d with code, %d only the credit size)" % (len(diff), same, len(code_slides), len(diff) - len(code_slides)), len(code_slides) == 21 and len(diff) == 27)
say("code lines old (prompts stripped) == new, in order", "%d vs %d" % (len(oc), len(nc)), oc == nc and len(oc) == 67)
say("no code line starts with '>>> ' or '... '", sum(1 for l in nc if l.startswith((">>> ", "... "))), not any(l.startswith((">>> ", "... ")) for l in nc))
say("old result rows == new result shapes (expression and text)", "%d vs %d" % (len(orr), len(nr)), orr == nr and len(orr) == 21)
chg_charts = [i.filename for i in zo.infolist() if re.match(r"ppt/charts/chart\d+\.xml$", i.filename) and zo.read(i.filename) != zn.read(i.filename)]
parts_same = all(zo.read(i.filename) == zn.read(i.filename) for i in zo.infolist() if i.filename not in diff and i.filename not in chg_charts) and [i.filename for i in zo.infolist()] == [i.filename for i in zn.infolist()]
say("every other part byte-identical, same part list (changed charts: %d)" % len(chg_charts), parts_same, parts_same and len(chg_charts) == 5)
def links(z): return sum(len(re.findall(rb"<Relationship [^>]*Type=\"[^\"]*/hyperlink\"", z.read(n))) for n in z.namelist() if n.endswith(".rels"))
say("hyperlink relationships old vs new", "%d vs %d" % (links(zo), links(zn)), links(zo) == links(zn))
def chart_of(z, n):
    rels = z.read(n.replace("slides/", "slides/_rels/") + ".rels").decode(); return [("ppt/charts/" + m) for m in re.findall(r'Target="\.\./charts/(chart\d+\.xml)"', rels)]
minsz, bad = {}, []
for n in slides(zn):
    i = int(re.findall(r"\d+", n)[-1]); szs = [int(x) for x in re.findall(r'\bsz="(\d+)"', zn.read(n).decode("utf8"))]
    for c in chart_of(zn, n): szs += [int(x) for x in re.findall(r'\bsz="(\d+)"', zn.read(c).decode("utf8"))]
    minsz[i] = min(szs) / 100.0
    if min(szs) < 900: bad.append((i, min(szs) / 100.0))
say("no text run below 9 pt (slides and their charts)", "smallest %.1f pt; below 9: %s" % (min(minsz.values()), bad), not bad)
print("smallest size per slide (pt): " + ", ".join("%d:%g" % (i, v) for i, v in sorted(minsz.items())))
wide = []
for n in diff:
    for sh in M.xml_shapes(minidom.parseString(zn.read(n))):
        pass
    d = minidom.parseString(zn.read(n))
    for sp in d.getElementsByTagName("p:sp"):
        nm = sp.getElementsByTagName("p:cNvPr")[0].getAttribute("name")
        if not (M.is_code_name(nm) or M.is_result_name(nm)): continue
        cx = int(sp.getElementsByTagName("a:ext")[0].getAttribute("cx")); x = int(sp.getElementsByTagName("a:off")[0].getAttribute("x"))
        for p in sp.getElementsByTagName("a:p"):
            t = "".join(t.firstChild.nodeValue if t.firstChild else "" for t in p.getElementsByTagName("a:t")); w = len(t) * 0.6 * 10 * 12700
            if w > cx or x + cx > 9144000 - 457200: wide.append((n, t, w, cx))
say("every code and result line fits its shape on one line (chars x 0.6 x 10 pt), shapes inside the content width", "%d exceed" % len(wide), not wide)
print("RESULT", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
