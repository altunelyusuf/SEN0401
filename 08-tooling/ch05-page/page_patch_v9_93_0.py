#!/usr/bin/env python3
"""page_patch v9.93.0 (SEN0401 chapter 5 page; course rulings of 2026-11-14 and 2026-11-24). Writes the next page beside the committed 9.92.0 (unchanged), keeping its open-results mock-exam code:
  chapter-code tab = the 27 examples of the deck 3.8.0 (manifest 1.3.0), top menu item 'Run slide code'; wheel = library 1.2.0 (no lambda, Bitcoin Core references), boot snippet from pywheels_v1_2_0.json;
  lecture tab = titles, notes and takeaways of the deck 3.8.0; no everyday analogy and no lambda in any text of the page; embedded Turtle copies equal the repo files (ABox 1.1.1, document 1.1.2, register 1.6.0).
Usage: python3 page_patch_v9_93_0.py"""
__version__ = "9.93.0"
import glob, hashlib, json, os, re
import rdflib
from pptx import Presentation
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); REPO = os.path.dirname(T)
PG = os.path.join(REPO, "03-materials", "ch05", "page"); AS = os.path.join(REPO, "03-materials", "ch05", "assets"); RD = os.path.join(REPO, "03-materials", "ch05", "rdodi")
SRC = os.path.join(PG, "sen0401_ch05_page_v9_92_0.html"); DST = os.path.join(PG, "sen0401_ch05_page_v9_93_0.html"); assert not os.path.exists(DST)
NEWV = "9.93.0"; REPORT = []
def say(*a):
    s = " ".join(str(x) for x in a); REPORT.append(s); print(s)
t0 = open(SRC, encoding="utf-8").read(); tag = '<script type="application/json" id="data">'; a = t0.index(tag) + len(tag); b = t0.index("</script>", a)
blob = t0[a:b]; D = json.loads(blob)
assert json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/") == blob and D["_version"] == "9.92.0"
g = rdflib.Graph(); g.parse(os.path.join(REPO, "06-quality", "sen0401_deck_standard_shapes_v1_1_0.ttl"), format="turtle")
RX = re.compile(str(next(g.objects(None, rdflib.Namespace("http://www.w3.org/ns/shacl#").pattern))), re.I)
ENDS = re.compile(r"""[.!?](?=["'”)\]]*(?:\s+["'“(]?[A-Z0-9]|\s*$))""")
def span(s, m):
    st = 0
    for e in ENDS.finditer(s):
        if e.end() <= m.start(): st = e.end()
    while st < len(s) and s[st] in " ”\"')]": st += 1
    e = ENDS.search(s, m.end()); en = e.end() if e else len(s)
    while en < len(s) and s[en] in "\"'”)]": en += 1
    return st, en
REMOVED = []
def strip(s):
    out = s
    for _ in range(40):
        m = RX.search(out)
        if not m: break
        st, en = span(out, m); piece = out[st:en]
        if st > 0 and out[st - 1] == " ": st -= 1
        elif en < len(out) and out[en] == " ": en += 1
        REMOVED.append(piece); out = out[:st] + out[en:]
    return out
REPL = [("think of the words as independently meaningful", "treat the words as independently meaningful"),
 ("The chapter gives the right picture: think of an extended key as the root of a branch in the tree structure, with which the rest of the branch can be derived,", "The chapter states it precisely: an extended key is the root of a branch in the tree structure, from which the rest of the branch can be derived,"),
 ("The chapter asks the reader to imagine reviewing a bank or credit card statement from a year ago that had the date and amount of every transaction listed but a blank entry for the description field, and says that because address and transaction labels are stored only", "The chapter explains that, because address and transaction labels are stored only"),
 ("the first thing they lose and the last thing they think of.", "the first thing they lose and the last thing they remember to back up."),
 (", a key-analogy slide maps house and car keys onto bitcoin keys, and program code", ", and program code"),
 ("key=lambda x: len(x)", "key=len"), ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'), ("lambda  lambda x: …", "lambda  an unnamed one-line function")]
def rep(s):
    for x, y in REPL: s = s.replace(x, y)
    return s
def walk(o, fn):
    if isinstance(o, dict): return {k: walk(v, fn) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, fn) for v in o]
    if isinstance(o, str): return fn(o)
    return o
# chapter code, wheel, boot
man = json.load(open(os.path.join(PG, "chapter_code_ch05_v1_3_0.json"))); pw = json.load(open(os.path.join(H, "pywheels_v1_2_0.json")))
WH = pw["wheels"][0]["file"]; wb = open(os.path.join(AS, WH), "rb").read(); assert hashlib.sha256(wb).hexdigest() == pw["wheels"][0]["sha256"]
assert len(man["examples"]) == 27
D["chaptercode"] = {"file": "03-materials/ch05/page/chapter_code_ch05_v1_3_0.json", "version": "1.3.0", "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
D["py_wheels"] = [{"name": WH, "hex": wb.hex()}]; boot = pw["boot_python"]; assert "lambda" not in boot and "v1_1_0" not in boot; D["py_boot"] = boot
# lecture from the deck
prs = Presentation(os.path.join(REPO, "03-materials", "ch05", "SEN0401_Ch05_WalletRecovery_3e_v3_8_0.pptx")); notes = json.load(open(os.path.join(T, "ch05-deck", "deck_notes_v3_8_0.json")))["slides"]
assert len(prs.slides) == len(D["lecture"]) == len(notes) == 68
lec = []; kept = 0
for old, sl, nt in zip(D["lecture"], prs.slides, notes):
    e = dict(old); ti = [s for s in sl.shapes if s.is_placeholder and s.placeholder_format.type in (1, 3)]
    tk = [s for s in sl.shapes if s.name == "takeaway" and s.has_text_frame]
    assert nt["slide"] == old["n"]; e["title"] = ti[0].text_frame.text.strip() if ti else old["title"]; e["say"] = nt["notes"]
    if tk: e["takeaway"] = tk[0].text_frame.text.strip()
    else: kept += 1
    lec.append(e)
D["lecture"] = lec; say("lecture: 68 slides; takeaway kept from the old page on", kept)
json.dump({"chapter": 5, "deck": "SEN0401_Ch05_WalletRecovery_3e_v3_8_0.pptx", "slides": lec}, open(os.path.join(H, "lecture_v2_3_0.json"), "w"), indent=1, ensure_ascii=False)
D["_version"] = NEWV; D = walk(D, lambda s: s if (len(s) > 200000 or s[:3] == "hex") else strip(rep(s)))
say("sentences removed from the data:", len(REMOVED))
for r in REMOVED: say("  removed:", r[:160])
raw = json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
H2 = t0[:a] + raw + t0[b:]; json.dump(D, open(os.path.join(H, "page_data_v9_93_0.json"), "w"), ensure_ascii=False)
# page script text
head, tail = H2[:a + len(raw)], H2[a + len(raw):]
for x, y in REPL:
    if x in tail: say("script text replaced:", x[:40], tail.count(x)); tail = tail.replace(x, y)
H2 = head + tail
# menu
v_old = "const VIEWS=[['learn','\U0001F4DA Learn'],['maps','\U0001F5FA Maps']"; v_new = "const VIEWS=[['learn','\U0001F4DA Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps','\U0001F5FA Maps']"
g_old = "...(CC.length?[['chaptercode','\U0001F4BB Chapter code']]:[]),"; assert H2.count(v_old) == 1 and H2.count(g_old) == 1
H2 = H2.replace(v_old, v_new).replace(g_old, "")
H2, n = re.subn(r'<meta name="version" content="[^"]+">', '<meta name="version" content="%s">' % NEWV, H2); assert n == 1
# embedded turtle = repo files
FILES = {"sen0401_materials_v1_4_14.ttl": os.path.join(REPO, "03-materials", "sen0401_materials_v1_6_0.ttl"),
         "sen0401_ch05_domain_abox_v1_1_0.ttl": os.path.join(RD, "sen0401_ch05_domain_abox_v1_1_1.ttl"),
         "sen0401_ch05_document_v1_1_1.ttl": os.path.join(RD, "sen0401_ch05_document_v1_1_2.ttl")}
ren = {k: os.path.basename(v) for k, v in FILES.items()}
def emb(m):
    attrs, body = m.group(1), m.group(2); nm = re.search(r'data-name="([^"]+)"', attrs).group(1)
    if nm in FILES:
        body = open(FILES[nm], encoding="utf-8").read(); s = re.search(r'data-sha256="([0-9a-f]+)"', attrs).group(1)
        attrs = attrs.replace(nm, ren[nm]).replace(s, hashlib.sha256(body.encode()).hexdigest()[:len(s)]); say("embedded:", ren[nm])
    else:
        nb = strip(rep(body))
        if nb != body:
            s = re.search(r'data-sha256="([0-9a-f]+)"', attrs).group(1); body = nb; attrs = attrs.replace(s, hashlib.sha256(body.encode()).hexdigest()[:len(s)]); say("embedded, sentences removed:", nm)
    return '<script type="text/turtle"' + attrs + ">" + body + "</script>"
H2 = re.sub(r'<script type="text/turtle"([^>]*)>(.*?)</script>', emb, H2, flags=re.S)
for k, v in ren.items(): H2 = H2.replace(k, v)
open(DST, "w", encoding="utf-8").write(H2); open(os.path.join(H, "patch_v9_93_0_report.txt"), "w").write("\n".join(REPORT) + "\n"); say("written", DST, len(H2))
