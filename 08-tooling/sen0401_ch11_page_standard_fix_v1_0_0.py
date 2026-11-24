#!/usr/bin/env python3
"""Chapter 11 page standard fix v1.0.0 (SEN0401). Reads the released page v9_96_0 (never edited) and the deck v2_5_0, writes page v9_97_0, page data v9_97_0 and chapter-code manifest v1_1_0.
Owner ruling of 2026-11-24: no everyday analogy in any deck or page text. What it does:
 1 every sentence of the page data that matches the analogy pattern of shape D4 (06-quality/sen0401_deck_standard_shapes_v1_1_0.ttl) is dropped; "Glacier core analogy" is relabelled "Glacier core depth";
   the example code of the node that quoted the book's topsoil sentence checks another sentence of the same book file instead (output unchanged);
 2 the lecture says are rewritten from the notes of the deck v2_5_0 (first sentences) and the takeaways that were analogies are replaced by plain ones;
 3 the chapter-code manifest is rebuilt from the code boxes of the deck v2_5_0 (all boxes of a slide joined, the last line, the printed result, removed);
 4 the menu entry becomes the top-level view '▶ Run slide code' (as in chapters 7 and 8)."""
import re, json, os, sys, glob
import rdflib
from pptx import Presentation
R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = R + "/03-materials/ch11/page/sen0401_ch11_page_v9_96_0.html"
DECK = R + "/03-materials/ch11/SEN0401_Ch11_TheBlockchain_3e_v2_5_0.pptx"
OLDM = R + "/03-materials/ch11/page/chapter_code_ch11_v1_0_0.json"
OUT = R + "/03-materials/ch11/page/sen0401_ch11_page_v9_97_0.html"
OUTM = R + "/03-materials/ch11/page/chapter_code_ch11_v1_1_0.json"
OUTD = R + "/08-tooling/ch11-page/page_data_v9_97_0.json"
h = open(SRC, encoding="utf-8").read()
m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', h, re.S)
d = json.loads(m.group(2).replace("<\\/", "</"))
g = rdflib.Graph(); g.parse(R + "/06-quality/sen0401_deck_standard_shapes_v1_1_0.ttl", format="turtle")
SH = rdflib.Namespace("http://www.w3.org/ns/shacl#")
rx = re.compile(str(next(g.objects(None, SH.pattern))), re.I)
mask = lambda s: re.sub(r"[0-9a-fA-F]{40,}", "", s)
RENAME = [("Glacier core analogy", "Glacier core depth")]
OLDQ, NEWQ = "The top six blocks are like a few inches of topsoil", "beyond six blocks, blocks are less and less likely to change"
log = {"dropped": 0, "left": []}
def fix(s, path):
    if s.startswith("data:") or len(s) > 20000 and "base64" in s[:200]: return s
    for a, b in RENAME: s = s.replace(a, b)
    s = s.replace(OLDQ, NEWQ)
    if not rx.search(mask(s)): return s
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"(])", s)
    keep = [p for p in parts if not rx.search(mask(p))]
    if not keep or len(keep) == len(parts): log["left"].append(path); return s
    log["dropped"] += len(parts) - len(keep)
    return " ".join(keep)
def walk(o, path):
    if isinstance(o, dict): return {k: walk(v, path + "." + k) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, path + "." + str(i)) for i, v in enumerate(o)]
    if isinstance(o, str): return fix(o, path)
    return o
d = walk(d, "")
assert not [x for x in log["left"] if not x.startswith(".lecture.")], log["left"]
log["left"] = []
# 2 lecture
prs = Presentation(DECK)
PLAIN = {5: "Each block is tied to the one before it by that block's hash", 20: "A merkle tree ends in one hash, the root, that stands for every transaction",
         28: "A test chain has its own rules, its own ports and no real money"}
CARD = "Each card gives one idea as one plain sentence"
def say(t):
    ss = re.split(r"(?<=[.!?])\s+", t.strip()); out = []
    for s in ss:
        if out and len(" ".join(out + [s]).split()) > 75: break
        out.append(s)
    return " ".join(out)
for i, s in enumerate(prs.slides, 1):
    e = d["lecture"][i - 1]; assert e["n"] == i
    e["say"] = say(s.notes_slide.notes_text_frame.text)
    if i in PLAIN: e["takeaway"] = PLAIN[i]
    elif e["takeaway"].startswith("Say each idea twice"): e["takeaway"] = CARD
    for k in ("say", "takeaway"): assert not rx.search(e[k]), (i, e[k])
# 3 manifest
man = json.load(open(OLDM))
for ex in man["examples"]:
    s = prs.slides[ex["slide"] - 1]
    bx = sorted([x for x in s.shapes if x.name.startswith("code")], key=lambda x: int(re.match(r"code (\d+)", x.name).group(1)))
    lines = "\n".join(x.text_frame.text for x in bx).split("\n")
    ex["code"] = "\n".join(lines[:-1])
    assert "lambda" not in ex["code"]
man["manifest"] = "chapter_code_ch11_v1_1_0"; man["deck"] = os.path.basename(DECK); man["deck_version"] = "2.5.0"
man["file"] = "03-materials/ch11/page/chapter_code_ch11_v1_1_0.json"; man["version"] = "1.1.0"
d["chaptercode"] = {"file": man["file"], "version": "1.1.0", "examples": man["examples"]}
d["_version"] = "9.97.0"
# 4 menu and page
html = h[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + h[m.end(2):]
# 4a the other embedded blocks: the question bank (JSON) and the turtle copies; literals are treated sentence by sentence, the sha shown in the provenance table is recomputed
import hashlib
KEYCLAUSE = ", a key-analogy slide maps house and car keys onto bitcoin keys"
def lit(mm):
    body = mm.group(1)
    body = body.replace(KEYCLAUSE, "")
    return '"' + fix(body, "ttl") + '"'
def block(mm):
    attrs, body = mm.group(1), mm.group(2)
    if 'id="qbank"' in attrs:
        j = json.loads(body.replace("<\\/", "</")); body = json.dumps(walk(j, ".qbank"), ensure_ascii=False).replace("</", "<\\/")
    elif "text/turtle" in attrs and any(k in attrs for k in ("materials", "domain_tbox", "domain_abox", "ch11_document")):
        body = re.sub(r'"((?:[^"\\\n]|\\.)*)"', lit, body)
        attrs = re.sub(r'data-sha256="\w+"', 'data-sha256="%s"' % hashlib.sha256(body.encode()).hexdigest()[:16], attrs)
    else: return mm.group(0)
    return "<script" + attrs + ">" + body + "</script>"
html = re.sub(r"<script([^>]*)>(.*?)</script>", block, html, flags=re.S)
a = "const VIEWS=[['learn','📚 Learn'],['maps','🗺 Maps']"
b = "const VIEWS=[['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps','🗺 Maps']"
c1 = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
assert html.count(a) == 1 and html.count(c1) == 1
html = html.replace(a, b).replace(c1, "")
html = html.replace("9.96.0", "9.97.0") if html.count("9.96.0") < 5 else html
open(OUT, "w", encoding="utf-8").write(html)
json.dump(man, open(OUTM, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(d, open(OUTD, "w", encoding="utf-8"), ensure_ascii=False)
print("dropped sentences", log["dropped"], "page", OUT)
