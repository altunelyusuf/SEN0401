#!/usr/bin/env python3
"""page_patch v9.94.0 (SEN0401 chapter 10 page, owner rulings of 2026-11-14 and 2026-11-24). Writes the next version of the page beside the committed 9.93.0 (which stays unchanged):
  * the chapter-code tab lists the 22 examples of the deck 2.4.0 (chapter_code_ch10_v1_1_0.json): comment-led groups, one statement per line, no prompt, no lambda; the top menu item is 'Run slide code' (as chapters 7 and 8);
  * the wheel of the page is the library 1.1.0 (no lambda, Bitcoin Core references in the module docstrings) and py_boot imports its modules; the lab code and the page carry the same files (lib_match_check);
  * the lecture tab carries the titles, notes and takeaways of the deck 2.4.0 (60 to 140 words, no analogy);
  * no everyday analogy anywhere in the page: every sentence that the ruling pattern of the deck standard (shape D4) finds is deleted from the concept texts, the findings and the embedded copies of the Turtle files
    (the data-sha256 of an embedded file that changed is recomputed over the new text; the committed Turtle files are not edited);
  * no lambda and no prompt line in the page text (the Python keyword list, the exercise 'Sort with a key', the two '...' of a quoted JSON sample of the book).
Writes: 03-materials/ch10/page/sen0401_ch10_page_v9_94_0.html, page_data_v9_94_0.json, lecture_v2_3_0.json, pywheels_v1_2_0.json, patch_v9_94_0_report.txt. Usage: python3 page_patch_v9_94_0.py"""
__version__ = "9.94.0"
import glob, hashlib, html as htmllib, json, os, re, sys, zipfile
import rdflib
H = os.path.dirname(os.path.abspath(__file__)); T = os.path.dirname(H); REPO = os.path.dirname(T)
PG = os.path.join(REPO, "03-materials", "ch10", "page"); AS = os.path.join(REPO, "03-materials", "ch10", "assets")
SRC = os.path.join(PG, "sen0401_ch10_page_v9_93_0.html"); DST = os.path.join(PG, "sen0401_ch10_page_v9_94_0.html")
assert not os.path.exists(DST), DST
NEWV = "9.94.0"; REPORT = []

def say(*a):
    s = " ".join(str(x) for x in a); REPORT.append(s); print(s)

t0 = open(SRC, encoding="utf-8").read()
tag = '<script type="application/json" id="data">'; a = t0.index(tag) + len(tag); b = t0.index("</script>", a)
blob = t0[a:b]; D = json.loads(blob)
assert json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/") == blob, "the data blob does not round-trip"
assert D["_version"] == "9.93.0"

# ------------------------------------------------------------------ the ruling pattern of the deck standard (D4)
g = rdflib.Graph(); g.parse(os.path.join(REPO, "06-quality", "sen0401_deck_standard_shapes_v1_1_0.ttl"), format="turtle")
RX = re.compile(str(next(g.objects(None, rdflib.Namespace("http://www.w3.org/ns/shacl#").pattern))), re.I)
# further everyday comparisons that the D4 pattern does not catch (found by reading the page text)
EXTRA = r"like a menu card|like a private motorway|librarian|as if the shop receipt|like a recipe passed|the postcard became|postcard|like a house that is only on a private road"
RX = re.compile(RX.pattern + "|" + EXTRA, re.I)
LBL_OLD, LBL_NEW = "the old transport reads like a postcard", "the old transport sends its bytes in the clear"
ENDS = re.compile(r"""[.!?](?=["'\u201d)\]]*(?:\s+["'\u201c(]?[A-Z0-9]|\s*$))""")

def sentence_span(s, m):
    st = 0
    if s[m.start()] in ".!?" and RX.pattern and m.group(0)[0] in ".!?": st = m.start() + 1   # the match opens with the full stop of the sentence before
    else:
        for e in ENDS.finditer(s):
            if e.end() <= m.start(): st = e.end()
    while st < len(s) and s[st] in " \u201d\"')]": st += 1
    e = ENDS.search(s, m.end())
    en = e.end() if e else len(s)
    while en < len(s) and s[en] in "\"'\u201d)]": en += 1
    return st, en

REMOVED = []   # (plain text of the removed sentence with its leading space)
def strip_analogies(s):
    out = s
    for _ in range(40):
        m = RX.search(out)
        if not m: break
        st, en = sentence_span(out, m)
        piece = out[st:en]; lead = ""
        if st > 0 and out[st - 1] == " ": lead = " "; st -= 1
        elif en < len(out) and out[en] == " ": en += 1
        nxt = out[en:en + 90]
        REMOVED.append((lead + piece if lead else piece, out[max(0, st - 70):st], nxt))
        out = out[:st] + out[en:]
    return out

def walk(o, fn):
    if isinstance(o, dict): return {k: walk(v, fn) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, fn) for v in o]
    if isinstance(o, str): return fn(o)
    return o

# ------------------------------------------------------------------ chapter code, wheel, boot
man = json.load(open(os.path.join(PG, "chapter_code_ch10_v1_1_0.json")))
D["chaptercode"] = {"file": "03-materials/ch10/page/chapter_code_ch10_v1_1_0.json", "version": "1.1.0",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
WH = "sen0401_ch10_lib-1.1.0-py3-none-any.whl"; wb = open(os.path.join(AS, WH), "rb").read()
assert hashlib.sha256(wb).hexdigest() == man["library"]["sha256"], "the wheel differs from the manifest's hash"
D["py_wheels"] = [{"name": WH, "hex": wb.hex()}]
setup = man["setup"]["code"]
boot = "import builtins\n" + setup + "\nfor _n in [k for k in list(globals()) if not k.startswith('_') and k != 'builtins']: setattr(builtins, _n, globals()[_n])\n"
assert "v1_0_0" not in boot and "lambda" not in boot
D["py_boot"] = boot
json.dump({"_version": "1.2.0", "wheels": [{"file": WH, "sha256": man["library"]["sha256"]}], "pyodide_packages": [], "boot_python": boot,
           "_note": "The wheel holds the chapter 10 library 1.1.0 and protocol module (standard library only; no lambda; Bitcoin Core references in the module docstrings) and the saved files the worked examples read, byte for byte as in the 1.0.0 wheel. The boot snippet runs the setup of the chapter-code manifest chapter_code_ch10_v1_1_0.json once."},
          open(os.path.join(H, "pywheels_v1_2_0.json"), "w"), indent=1)

# ------------------------------------------------------------------ lecture: the titles, notes and takeaways of the deck 2.4.0
plan = json.load(open(os.path.join(T, "ch10-deck", "deck_plan_v2_4_0.json")))["slides"]
assert len(plan) == len(D["lecture"]) == 49
new_lec = []
for old, s in zip(D["lecture"], plan):
    e = dict(old); e["title"] = s["title"]; e["say"] = s["notes"]; e["takeaway"] = s.get("take") or s["sub"]; new_lec.append(e)
D["lecture"] = new_lec
json.dump({"chapter": 10, "deck": "SEN0401_Ch10_TheBitcoinNetwork_3e_v2_4_0.pptx", "slides": new_lec,
           "_note": "lecture_v2_2_1.json with the titles, notes and takeaways of the deck 2.4.0 (notes of 60 to 140 words written for the reader); concept, read, links and labels unchanged."}, open(os.path.join(H, "lecture_v2_3_0.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ no everyday analogy in any text of the data
D["_version"] = NEWV
D = walk(D, lambda s: strip_analogies(s.replace(LBL_OLD, LBL_NEW)) if (len(s) < 200000 and "hex" not in s[:3]) else s)
say("sentences removed from the data:", len(REMOVED))
raw = json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
H2 = t0[:a] + raw + t0[b:]
json.dump(D, open(os.path.join(H, "page_data_v9_94_0.json"), "w"), indent=None, ensure_ascii=False)

# the same sentences stand in the embedded copies of the Turtle files and in the page script (text with Turtle escapes)
def enc_ttl(x): return x.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
head, tail = H2[:a + len(raw)], H2[a + len(raw):]
n_ttl = 0
for piece, _, _ in sorted(set((p, x, y) for p, x, y in REMOVED), key=lambda z: -len(z[0])):
    e = enc_ttl(piece)
    c = tail.count(e)
    if c: tail = tail.replace(e, ""); n_ttl += c
say("sentence copies removed from the embedded Turtle text:", n_ttl)
tail = tail.replace(LBL_OLD, LBL_NEW)
H2 = head + tail
# fragments of the course materials Turtle
for old, new in ((", a key-analogy slide maps house and car keys onto bitcoin keys, and program code", ", and program code"),):
    say("fragment", old[:40], H2.count(old)); H2 = H2.replace(old, new)

# ------------------------------------------------------------------ lambda and prompt lines
for old, new in (("lambda  lambda x: \u2026", "lambda  an unnamed one-line function"),
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ("key=lambda x: len(x))", "key=len)")):
    say("replace", old[:40], H2.count(old)); assert old in H2; H2 = H2.replace(old, new)
for old, new in (("{\\n      ...\\n    }", "{\\n      \u2026\\n    }"),):
    say("replace JSON sample dots", H2.count(old)); H2 = H2.replace(old, new)

# ------------------------------------------------------------------ the menu: 'Run slide code' is a top-level item (as chapters 7 and 8)
v_old = "const VIEWS=[['learn','\U0001F4DA Learn'],['maps','\U0001F5FA Maps']"
v_new = "const VIEWS=[['learn','\U0001F4DA Learn'],...(CC.length?[['chaptercode','\u25B6 Run slide code']]:[]),['maps','\U0001F5FA Maps']"
g_old = "...(CC.length?[['chaptercode','\U0001F4BB Chapter code']]:[]),"
assert H2.count(v_old) == 1 and H2.count(g_old) == 1, (H2.count(v_old), H2.count(g_old))
H2 = H2.replace(v_old, v_new).replace(g_old, "")
H2 = H2.replace('<meta name="version" content="9.93.0">', '<meta name="version" content="%s">' % NEWV)

# ------------------------------------------------------------------ embedded Turtle files: the hash of a changed file is recomputed over its text
def fix_ttl(m):
    attrs, body = m.group(1), m.group(2)
    s = re.search(r'data-sha256="([0-9a-f]+)"', attrs).group(1)
    old_ok = hashlib.sha256(body0.get(attrs, body).encode()).hexdigest()[:len(s)] == s
    return m.group(0)
body0 = {}
for m in re.finditer(r'<script type="text/turtle"([^>]*)>(.*?)</script>', t0, re.S): body0[m.group(1)] = m.group(2)
changed = 0
def sha_fix(m):
    global changed
    attrs, body = m.group(1), m.group(2)
    old_body = body0[attrs]
    s = re.search(r'data-sha256="([0-9a-f]+)"', attrs).group(1)
    if body == old_body: return m.group(0)
    assert hashlib.sha256(old_body.encode()).hexdigest()[:len(s)] == s, "the committed page's own hash did not match: " + attrs[:80]
    ns = hashlib.sha256(body.encode()).hexdigest()[:len(s)]
    changed += 1; say("embedded Turtle changed:", re.search(r'data-name="([^"]+)"', attrs).group(1), s, "->", ns)
    return '<script type="text/turtle"' + attrs.replace(s, ns) + ">" + body + "</script>"
H2 = re.sub(r'<script type="text/turtle"([^>]*)>(.*?)</script>', sha_fix, H2, flags=re.S)
open(DST, "w", encoding="utf-8").write(H2)
open(os.path.join(H, "patch_v9_94_0_report.txt"), "w").write("\n".join(REPORT) + "\n")
with open(os.path.join(H, "patch_v9_94_0_removed.txt"), "w") as f:
    for piece, before, after in REMOVED: f.write("REMOVED: %r\n   before: %r\n   after : %r\n" % (piece[:400], before, after))
say("written", DST, len(H2), "bytes; embedded Turtle files changed:", changed)
