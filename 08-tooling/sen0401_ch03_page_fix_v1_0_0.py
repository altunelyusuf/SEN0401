#!/usr/bin/env python3
"""sen0401_ch03_page_fix v1_0_0: makes the chapter 3 page v9.77.0 from the released v9.76.0 (which stays untouched; the open-results patch of 9.76.0 is kept as it is).
Changes, each measured afterwards by cme_material_check_v1_2_0.py, lib_match_check_v1_0_0.py, /tmp/mt/test_page.py and /tmp/smoke_cc.py:
  - the top menu gets the item '> Run slide code' (VIEWS) and the group Learn no longer lists the chapter code (as the pages of chapters 7 to 14 do);
  - the embedded chapter code is chapter_code_ch03_v1_2_0.json (the code of deck v3.3.0: def instead of lambda on slide 39, no lambda in a show expression);
  - the lecture of the page equals the deck v3.3.0: new titles, the new reader-facing notes ('say') and the literal take-away lines (no analogy);
  - the embedded Turtle blocks are swapped for named files, byte for byte: sen0401_ch03_domain_abox_v1_3_0.ttl (no lambda in the worked examples), sen0401_ch03_document_v1_2_2.ttl (one phrase),
    sen0401_materials_v1_4_15.ttl (the course ruling on analogies applied to the chapter 1 entry); the wheel with the chapter library is the same as in 9.76.0 (the library did not change);
  - the one sentence 'behaves like a network request' of the node text reads 'runs as a network request'.
Usage: python3 sen0401_ch03_page_fix_v1_0_0.py   (writes 03-materials/ch03/page/sen0401_ch03_page_v9_77_0.html; refuses to overwrite)."""
__version__ = "1.0.0"
import hashlib, json, os, re, sys
from pptx import Presentation
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_ch03_deck_notes_v1_0_0 as N
REPO = os.path.dirname(HERE); M = os.path.join(REPO, "03-materials"); CH = os.path.join(M, "ch03")
SRC = os.path.join(CH, "page", "sen0401_ch03_page_v9_76_0.html"); OUT = os.path.join(CH, "page", "sen0401_ch03_page_v9_77_0.html")
if os.path.exists(OUT): raise SystemExit("refusing to overwrite " + OUT)
raw = open(SRC, encoding="utf-8").read()
DATA = re.compile(r'(<script type="application/json" id="data">)(.*?)(</script>)', re.S)
m = DATA.search(raw); s = m.group(2); D = json.loads(s)
dump = lambda d: json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
assert dump(D) == s

# ---- the lecture follows the deck v3.3.0 -----------------------------------------------------------------
def title_of(slide):
    for sh in slide.shapes:
        tx = sh.text_frame.text.strip() if sh.has_text_frame else ""
        if len(tx) > 2 and not re.match(r"^\d+\s*/\s*\d+$", tx) and not any(r.font.name == "Courier New" for p in sh.text_frame.paragraphs for r in p.runs): return tx.split("\n")[0]
old_t = [title_of(x) for x in Presentation(os.path.join(CH, "SEN0401_Ch03_BitcoinCore_3e_v3_2_0.pptx")).slides]
new_t = [title_of(x) for x in Presentation(os.path.join(CH, "SEN0401_Ch03_BitcoinCore_3e_v3_3_0.pptx")).slides]
TAKE = {(k[0], k[1]): v for k, v in N.REPL.items()}
TAKE[(38, "A lambda is a tiny function written where it is needed")] = "A def writes a small function once and names it for reuse"
lect = D["lecture"]; assert len(lect) == 61
chg = 0
for e in lect:
    n = e["n"]
    if new_t[n - 1] != old_t[n - 1]: e["title"] = new_t[n - 1]; chg += 1      # the deck title changed: the lecture follows it
    elif e["title"] != old_t[n - 1]: print("note: lecture title %d (%r) differs from the unchanged deck title %r; left as it was" % (n, e["title"], old_t[n - 1]))
    e["say"] = N.NOTES[n]
    if e.get("takeaway") and (n, e["takeaway"]) in TAKE: e["takeaway"] = TAKE[(n, e["takeaway"])]
print("lecture: 61 notes replaced, %d titles changed" % chg)

# ---- the chapter code --------------------------------------------------------------------------------------
cc = json.load(open(os.path.join(CH, "page", "chapter_code_ch03_v1_2_0.json"), encoding="utf-8"))
D["chaptercode"] = {"file": "03-materials/ch03/page/chapter_code_ch03_v1_2_0.json", "version": "1.2.0",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in cc["examples"]]}
# ---- one sentence, and the version ------------------------------------------------------------------------
def walk(o):
    if isinstance(o, dict):
        for k, v in list(o.items()):
            if isinstance(v, str) and "behaves like a network request" in v: o[k] = v.replace("behaves like a network request", "runs as a network request")
            else: walk(v)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, str) and "behaves like a network request" in v: o[i] = v.replace("behaves like a network request", "runs as a network request")
            else: walk(v)
walk(D); D["_version"] = "9.77.0"
raw = raw[:m.start(2)] + dump(D) + raw[m.end(2):]

# ---- three strings that the page took from its template and that the later template (9.52.11, as the page of chapter 8 has them) words without lambda ---------
for x, y in (("lambda:'lambda  lambda x: \u2026'", "lambda:'lambda  an unnamed one-line function'"),
             ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
             ("key=lambda x: len(x)", "key=len")):
    assert x in raw, x
    raw = raw.replace(x, y)
# ---- the question bank: the seven listings with lambda are written with def; each is run before and after and must print the same --------------------------
import contextlib, io
QB = re.compile(r'(<script type="application/json" id="qbank">)(.*?)(</script>)', re.S)
qm = QB.search(raw); Q = json.loads(qm.group(2)); assert dump(Q) == qm.group(2)
MAN = {"        return lambda *args: json.dumps({'version': '1.1', 'method': name, 'params': list(args), 'id': 1})": "        def call(*args):\n            return json.dumps({'version': '1.1', 'method': name, 'params': list(args), 'id': 1})\n        return call",
       "print(tips, max(tips, key=lambda b: blocks[b][1]))": "def height_of(b):\n    return blocks[b][1]\nprint(tips, max(tips, key=height_of))"}
def nolambda(code):
    for x, y in MAN.items(): code = code.replace(x, y)
    return re.sub(r"^(\w+) = lambda ([^:]+): (.+)$", lambda mm: "def %s(%s):\n    return %s" % (mm.group(1), mm.group(2), mm.group(3)), code, flags=re.M)
def printed(code):
    b = io.StringIO()
    with contextlib.redirect_stdout(b): exec(code, {})
    return b.getvalue()
nq = 0
for q in Q:
    if isinstance(q, dict) and "lambda" in q.get("code", ""):
        new = nolambda(q["code"]); assert "lambda" not in new, new
        assert printed(new) == printed(q["code"]), q["q"]; q["code"] = new; nq += 1
print("question bank: %d listings rewritten with def, each printing the same" % nq)
raw = raw[:qm.start(2)] + dump(Q) + raw[qm.end(2):]

# ---- the menu --------------------------------------------------------------------------------------------
a = "const VIEWS=[['learn','\U0001F4DA Learn'],['maps',"; b = "const VIEWS=[['learn','\U0001F4DA Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps',"
assert raw.count(a) == 1; raw = raw.replace(a, b)
g = "...(CC.length?[['chaptercode','\U0001F4BB Chapter code']]:[]),"; assert raw.count(g) == 1; raw = raw.replace(g, "")

# ---- the embedded Turtle blocks, byte for byte ------------------------------------------------------------
SWAP = {"sen0401_ch03_domain_abox_v1_2_0.ttl": os.path.join(CH, "rdodi", "sen0401_ch03_domain_abox_v1_3_0.ttl"),
        "sen0401_ch03_document_v1_2_1.ttl": os.path.join(CH, "rdodi", "sen0401_ch03_document_v1_2_2.ttl"),
        "sen0401_materials_v1_4_14.ttl": os.path.join(M, "sen0401_materials_v1_4_15.ttl")}
BLK = re.compile(r'<script type="text/turtle" data-kind="([a-z]+)" data-name="([^"]+)" data-sha256="[0-9a-f]+">(.*?)</script>', re.S)
parts = []; pos = 0; done = set()
for bm in BLK.finditer(raw):
    parts.append(("t", raw[pos:bm.start()]))
    if bm.group(2) in SWAP:
        data = open(SWAP[bm.group(2)], "rb").read().decode("utf-8"); nm = os.path.basename(SWAP[bm.group(2)]); done.add(bm.group(2))
        parts.append(("b", '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (bm.group(1), nm, hashlib.sha256(data.encode("utf-8")).hexdigest()[:16], data)))
    else: parts.append(("b", bm.group(0)))
    pos = bm.end()
parts.append(("t", raw[pos:])); assert done == set(SWAP), done
REN = {"sen0401_ch03_domain_abox_v1_2_0": "sen0401_ch03_domain_abox_v1_3_0", "sen0401_ch03_document_v1_2_1": "sen0401_ch03_document_v1_2_2", "sen0401_materials_v1_4_14": "sen0401_materials_v1_4_15",
       "chapter_code_ch03_v1_1_0": "chapter_code_ch03_v1_2_0"}
out = []
for kind, text in parts:
    if kind == "t":
        for x, y in REN.items(): text = text.replace(x, y)
    out.append(text)
raw = "".join(out)
note = ("<!-- page 9.77.0 over 9.76.0 (task: the chapter 3 materials to the course standard of 2026-11-24): the menu item 'Run slide code'; the chapter code, the lecture and the notes equal the deck 3.3.0 "
        "(def instead of lambda, literal wording, reader-facing notes); the embedded Turtle files are sen0401_ch03_domain_abox_v1_3_0.ttl, sen0401_ch03_document_v1_2_2.ttl and sen0401_materials_v1_4_15.ttl; "
        "the open-results patch of 9.76.0 and the chapter library wheel are unchanged. -->")
assert raw.count('<meta charset="utf-8">') == 1; raw = raw.replace('<meta charset="utf-8">', '<meta charset="utf-8">' + note, 1)
open(OUT, "w", encoding="utf-8").write(raw)
print("wrote", os.path.relpath(OUT, REPO), len(raw))
