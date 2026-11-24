#!/usr/bin/env python3
"""Ch8 deck v2_4_0 -> v2_5_0 (deck standard v3.1.0): code boxes named 'code N', story-marker name freed from balloons, code boxes of at most 30 words,
an explanation of at least 8 words beside every code box, and the slide-7 background. Reads the committed v2_4_0, never edits it."""
__version__ = "1.0.0"
import copy, subprocess, sys
from pptx import Presentation
from pptx.util import Emu
from lxml import etree
SRC = "../03-materials/ch08/SEN0401_Ch08_DigitalSignatures_3e_v2_4_0.pptx"
OUT = "../03-materials/ch08/SEN0401_Ch08_DigitalSignatures_3e_v2_5_0.pptx"
p = Presentation(SRC)
for s in p.slides:
    for sh in s.shapes:
        if sh.name.startswith("Story balloon"): sh.name = sh.name.replace("Story balloon", "Balloon note")
        elif sh.name.startswith("Code ") and not sh.name.startswith("Code box"): sh.name = "code " + sh.name[5:]
W = lambda t: len(t.split())

def split_box(slide, sh):
    paras = list(sh.text_frame.paragraphs)
    if W(sh.text_frame.text) <= 30: return
    groups, cur, cw = [], [], 0
    for pa in paras:
        t = pa.text
        if t.strip() == "":
            if cur: cur.append(pa)
            continue
        w = W(t)
        if cur and cw + w > 30:
            k0 = len(cur)
            if t[:1] in (" ", "\t"):               # never cut inside an indented block: go back to the last unindented line
                k0 = max([j for j, x in enumerate(cur) if j > 0 and x.text[:1] not in (" ", "\t") and x.text.strip() != ""] or [len(cur)])
            head, cur = cur[:k0], cur[k0:]
            while head and head[-1].text.strip() == "": head.pop()
            while cur and cur[0].text.strip() == "": cur.pop(0)
            groups.append(head); cw = sum(W(x.text) for x in cur)
        cur.append(pa); cw += w
    while cur and cur[-1].text.strip() == "": cur.pop()
    if cur: groups.append(cur)
    nl = sum(len(g) for g in groups); top, h = sh.top, sh.height
    base = sh._element; ns = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
    made = []
    for k, g in enumerate(groups):
        el = base if k == 0 else copy.deepcopy(base)
        keep = {id(x._p) for x in g}
        body = el.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}txBody")
        for pe in list(body.findall(ns + "p")):
            if id(pe) not in keep and not (k > 0 and False): pass
        made.append((el, g))
    # rebuild paragraph sets by index (deepcopy changes identities)
    idx = [[paras.index(x) for x in g] for g in groups]
    done = 0
    for k, (el, g) in enumerate(made):
        body = el.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}txBody")
        pes = body.findall(ns + "p")
        for j, pe in enumerate(pes):
            if j not in idx[k]: body.remove(pe)
        if k > 0:
            base.addnext(el) if k == 1 else made[k - 1][0].addnext(el)
            nm = el.find(".//{http://schemas.openxmlformats.org/presentationml/2006/main}cNvPr"); nm.set("name", sh.name + " (part %d)" % (k + 1))
            nm.set("id", str(max(int(x) for x in slide._element.xpath("//p:cNvPr/@id")) + 1))
        sp = el.find(".//" + ns.replace("a}", "a}") + "xfrm") if False else None
    # geometry
    done = 0
    for k, (el, g) in enumerate(made):
        off = el.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}off"); ext = el.find(".//{http://schemas.openxmlformats.org/drawingml/2006/main}ext")
        off.set("y", str(int(top + h * done / nl))); ext.set("cy", str(int(h * len(g) / nl))); done += len(g)

for i in (7, 22, 39):
    s = p.slides[i - 1]
    for sh in [x for x in s.shapes if x.has_text_frame and x.name.startswith("code ")]:
        t0, h0, n = sh.top, sh.height, sh.name[5:]
        if W(sh.text_frame.text) > 30:
            split_box(s, sh)
            for b in s.shapes:
                if i != 7 and b.name == "Balloon note " + n:       # the explanation spans every part of the split box
                    b.top = min(b.top, t0); b.height = max(b.height, t0 + h0 - b.top)

# slide 41: explanation of at least eight words beside the second code box
for sh in p.slides[40].shapes:
    if sh.name == "Balloon note 2":
        r = sh.text_frame.paragraphs[0].runs
        r[0].text = "Next, another message gives another nonce, because the hash of the message goes into it."
        for x in r[1:]: x.text = ""
# slide 7 background as on the other slides
bg = copy.deepcopy(p.slides[0]._element.xpath("./p:cSld/p:bg")[0])
cs = p.slides[6]._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}cSld")
cs.insert(0, bg)
p.core_properties.version = "2.5.0"
p.save(OUT); print("wrote", OUT)
