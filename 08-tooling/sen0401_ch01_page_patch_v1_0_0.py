#!/usr/bin/env python3
"""sen0401_ch01_page_patch v1.0.0 (SEN0401 chapter 1 page, owner rulings of 2026-11-14 and 2026-11-24). Writes the page 9.76.0 beside the committed 9.75.0 (which stays unchanged); the mock exam of 9.75.0 (exam and results as two views) is kept:
  * the chapter-code tab lists the 15 examples of the deck 3.6.0 (chapter_code_ch01_v1_2_0.json); the top menu item is 'Run slide code' (as chapters 7 to 14);
  * the wheel of the page is the library 1.1.0 (Bitcoin Core references in the module docstring, no lambda) and py_boot imports sen0401_ch01_lib_v1_1_0 (the pbkdf2 shim of the page 9.72.0 is kept);
  * the lecture tab carries the titles, notes (60 to 140 words, no analogy) and takeaways of the deck 3.6.0;
  * no everyday analogy anywhere in the page: every sentence that the ruling pattern of the deck standard (shape D4) finds is deleted from the page data;
  * the embedded Turtle blocks that changed are the byte-exact content of repository files under their real names (document 1.3.0, domain abox 1.3.0, register 1.4.15), data-sha256 recomputed;
  * no lambda in the page text (the Python keyword list, the exercise 'Sort with a key') and no prompt line.
Writes: 03-materials/ch01/page/sen0401_ch01_page_v9_76_0.html, 08-tooling/ch01-page/page_data_v9_76_0.json, pywheels_v1_2_0.json, lecture_v2_0_0.json, patch_v9_76_0_report.txt, patch_v9_76_0_removed.txt.
Usage: python3 sen0401_ch01_page_patch_v1_0_0.py"""
__version__ = "1.0.0"
import hashlib, json, os, re, sys
import rdflib
from pptx import Presentation
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); PH = os.path.join(H, "ch01-page")
PG = os.path.join(REPO, "03-materials", "ch01", "page"); AS = os.path.join(REPO, "03-materials", "ch01", "assets"); RD = os.path.join(REPO, "03-materials", "ch01", "rdodi")
SRC = os.path.join(PG, "sen0401_ch01_page_v9_75_0.html"); DST = os.path.join(PG, "sen0401_ch01_page_v9_76_0.html")
OLDDECK = os.path.join(REPO, "03-materials", "ch01", "SEN0401_Ch01_Introduction_3e_v3_5_0.pptx"); NEWDECK = os.path.join(REPO, "03-materials", "ch01", "SEN0401_Ch01_Introduction_3e_v3_6_0.pptx")
assert not os.path.exists(DST), DST
NEWV = "9.76.0"; REPORT = []

def say(*a):
    s = " ".join(str(x) for x in a); REPORT.append(s); print(s)

t0 = open(SRC, encoding="utf-8", newline="").read()
tag = '<script type="application/json" id="data">'; a = t0.index(tag) + len(tag); b = t0.index("</script>", a)
blob = t0[a:b]; D = json.loads(blob)
assert json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/") == blob, "the data blob does not round-trip"
assert D["_version"] == "9.75.0"

# ------------------------------------------------------------------ the ruling pattern of the deck standard (D4)
g = rdflib.Graph(); g.parse(os.path.join(REPO, "06-quality", "sen0401_deck_standard_shapes_v1_1_0.ttl"), format="turtle")
RX = re.compile(str(next(g.objects(None, rdflib.Namespace("http://www.w3.org/ns/shacl#").pattern))), re.I)
EXTRA = r"like a web browser|like a recipe|like a time capsule|like a ring of keys|like a first driving lesson|like two rivers|like a banknote|like layers"
RX = re.compile(RX.pattern + "|" + EXTRA, re.I)
ENDS = re.compile(r"""[.!?](?=["'”)\]]*(?:\s+["'“(]?[A-Z0-9]|\s*$))""")

def sentence_span(s, m):
    st = 0
    if s[m.start()] in ".!?" and m.group(0)[0] in ".!?": st = m.start() + 1
    else:
        for e in ENDS.finditer(s):
            if e.end() <= m.start(): st = e.end()
    while st < len(s) and s[st] in " ”\"')]": st += 1
    e = ENDS.search(s, m.end())
    en = e.end() if e else len(s)
    while en < len(s) and s[en] in "\"'”)]": en += 1
    return st, en

REMOVED = []
def strip_analogies(s):
    out = s
    for _ in range(40):
        m = RX.search(out)
        if not m: break
        st, en = sentence_span(out, m)
        piece = out[st:en]; lead = ""
        if st > 0 and out[st - 1] == " ": lead = " "; st -= 1
        elif en < len(out) and out[en] == " ": en += 1
        REMOVED.append((lead + piece if lead else piece, out[max(0, st - 70):st], out[en:en + 90]))
        out = out[:st] + out[en:]
    return out

def walk(o, fn):
    if isinstance(o, dict): return {k: walk(v, fn) for k, v in o.items()}
    if isinstance(o, list): return [walk(v, fn) for v in o]
    if isinstance(o, str): return fn(o)
    return o

# ------------------------------------------------------------------ chapter code, wheel, boot
man = json.load(open(os.path.join(PG, "chapter_code_ch01_v1_2_0.json")))
assert man["deck"] == os.path.basename(NEWDECK)
D["chaptercode"] = {"file": "03-materials/ch01/page/chapter_code_ch01_v1_2_0.json", "version": "1.2.0",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
assert len(D["chaptercode"]["examples"]) == 15
WH = "sen0401_ch01_lib-1.1.0-py3-none-any.whl"; wb = open(os.path.join(AS, WH), "rb").read()
assert hashlib.sha256(wb).hexdigest() == man["library"]["sha256"], "the wheel differs from the manifest's hash"
old_boot = D["py_boot"]; old_setup = json.load(open(os.path.join(PG, "chapter_code_ch01_v1_1_0.json")))["setup"]["code"]
assert old_boot.startswith("import builtins\n") and old_setup in old_boot
shim = old_boot[len("import builtins\n"):old_boot.index(old_setup)]; tail = old_boot[old_boot.index(old_setup) + len(old_setup):]
assert "pbkdf2_hmac" in shim
D["py_wheels"] = [{"name": WH, "hex": wb.hex()}]
boot = "import builtins\n" + shim + man["setup"]["code"] + tail
assert "v1_0_0" not in boot and "lambda" not in boot and "sen0401_ch01_lib_v1_1_0" in boot
D["py_boot"] = boot
json.dump({"_version": "1.2.0", "wheels": [{"file": WH, "sha256": man["library"]["sha256"]}], "pyodide_packages": [], "boot_python": boot,
           "_note": "As pywheels_v1_1_0.json (the boot prefix that defines hashlib.pbkdf2_hmac when the page's Pyodide lacks it), with the wheel of the library 1.1.0 (Bitcoin Core references in the module docstring, no lambda) and the setup of chapter_code_ch01_v1_2_0.json."},
          open(os.path.join(PH, "pywheels_v1_2_0.json"), "w"), indent=1)

# ------------------------------------------------------------------ lecture: the titles, notes and takeaways of the deck 3.6.0
def texts(prs):
    out = []
    for s in prs.slides:
        ts = []
        for sh in s.shapes:
            if sh.has_text_frame and len(sh.text_frame.text.strip()) > 2 and not re.fullmatch(r"\d+\s*/\s*\d+", sh.text_frame.text.strip()) \
                    and not any(r.font.name == "Courier New" for p_ in sh.text_frame.paragraphs for r in p_.runs): ts.append(sh.text_frame.text.strip())
        notes = s.notes_slide.notes_text_frame.text if s.has_notes_slide else ""
        out.append((ts[0].split("\n")[0] if ts else "", ts[1].split("\n")[0] if len(ts) > 1 else "", notes))
    return out
OLD, NEW = texts(Presentation(OLDDECK)), texts(Presentation(NEWDECK))
assert len(D["lecture"]) == len(NEW) == 76
new_lec = []; n_tk = 0
for old, (ot, osub, _), (nt, nsub, nn) in zip(D["lecture"], OLD, NEW):
    e = dict(old); e["title"] = nt; e["say"] = nn
    if old.get("takeaway") == osub and nsub: e["takeaway"] = nsub; n_tk += 1
    new_lec.append(e)
D["lecture"] = new_lec
say("lecture entries", len(new_lec), "takeaways taken over from the new subtitles:", n_tk)
json.dump({"chapter": 1, "deck": os.path.basename(NEWDECK), "slides": new_lec,
           "_note": "The lecture entries of the page 9.75.0 with the titles, notes and takeaways of the deck 3.6.0 (notes of 60 to 140 words written for the reader); concept, read, links and labels unchanged."},
          open(os.path.join(PH, "lecture_v2_0_0.json"), "w"), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ texts of the deck that changed and that the page quotes
SWAP = [("Block 0 is a dated receipt and a message at once, and anyone can read it on a block explorer today.", "Block 0 carries a verifiable date and a message at once, and anyone can read it on a block explorer today."),
        ("A coin is spent whole, like a banknote, and the change returns as a new output.", "A coin is spent whole, and the change returns as a new output."),
        ("its code slide carries the receipt", "its code slide carries the evidence"),
        ("Say each idea twice: once as the meaning, once as the everyday comparison", "Each idea is defined once here and shown at work on the slides of this part"),
        ("Each card: the meaning in a few words, then something you already know", "Each card gives the meaning of one idea in a few words"),
        ("Bitcoin combines old parts, like a recipe of familiar ingredients.", "Bitcoin combines parts that existed before it."),
        ("A wallet holds keys, not coins, like a ring of keys to many safes.", "A wallet holds keys, not coins."),
        ("From an empty wallet to a first payment, like a first driving lesson.", "From an empty wallet to a first payment."),
        ("Two old solved problems, joined into one system, like two rivers.", "Two old solved problems, joined into one system.")]
def swap(s):
    for o, n in SWAP: s = s.replace(o, n)
    return s

# ------------------------------------------------------------------ no everyday analogy in any text of the data
D["_version"] = NEWV
D = walk(D, lambda s: strip_analogies(swap(s)) if (len(s) < 200000 and not s.startswith("hex")) else s)
say("sentences removed from the data:", len(REMOVED))
raw = json.dumps(D, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
H2 = t0[:a] + raw + t0[b:]
json.dump(D, open(os.path.join(PH, "page_data_v9_76_0.json"), "w"), indent=None, ensure_ascii=False)


# ------------------------------------------------------------------ the other JSON blocks of the page: quiz, qbank, objectives
def json_block(h, id_, fn):
    m = re.search(r'(<script type="application/json" id="%s">)(.*?)(</script>)' % id_, h, re.S)
    J = json.loads(m.group(2)); assert json.dumps(J, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/") == m.group(2), id_
    J = fn(J); raw2 = json.dumps(J, ensure_ascii=True, separators=(", ", ": ")).replace("</", "<\\/")
    return h[:m.start(2)] + raw2 + h[m.end(2):]
OPT = (("A bank transfer, a cheque, a payment in cash, and a gift card", "A bank transfer, a postal order, a payment in cash, and a gift card"),
       ("To settle all transactions at regular intervals, like a traditional bank", "To settle all transactions at regular intervals"))
def opt(sx):
    for o, n in OPT: sx = sx.replace(o, n)
    return sx
def qb(J):
    gone = [q for q in J if q["q"] == "Why does the chapter compare a Bitcoin wallet with a web browser?" or q.get("why") == "The chapter likens Bitcoin and its wallets to HTTP and its browsers."]
    assert len(gone) == 2, len(gone)
    say("questions removed from the bank (they test the wallet-browser comparison):", len(gone), "->", len(J) - 2, "left")
    J = [q for q in J if q not in gone]
    return walk(J, lambda sx: strip_analogies(swap(opt(sx))))
H2 = json_block(H2, "qbank", qb)
H2 = json_block(H2, "quiz", lambda J: walk(J, lambda sx: strip_analogies(swap(opt(sx)))))
H2 = json_block(H2, "objectives", lambda J: walk(J, lambda sx: strip_analogies(swap(opt(sx)))))

# ------------------------------------------------------------------ lambda text of the page scripts
for old, new in (("lambda  lambda x: …", "lambda  an unnamed one-line function"),
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ("key=lambda x: len(x))", "key=len)")):
    say("replace", old[:40], H2.count(old)); assert old in H2; H2 = H2.replace(old, new)

# ------------------------------------------------------------------ the menu: 'Run slide code' is a top-level item (as chapters 7 to 14)
v_old = "const VIEWS=[['learn','\U0001F4DA Learn'],['maps','\U0001F5FA Maps']"
v_new = "const VIEWS=[['learn','\U0001F4DA Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps','\U0001F5FA Maps']"
g_old = "...(CC.length?[['chaptercode','\U0001F4BB Chapter code']]:[]),"
assert H2.count(v_old) == 1 and H2.count(g_old) == 1, (H2.count(v_old), H2.count(g_old))
H2 = H2.replace(v_old, v_new).replace(g_old, "")
assert H2.count('<meta name="version" content="9.74.0">') == 1
H2 = H2.replace('<meta name="version" content="9.74.0">', '<meta name="version" content="%s">' % NEWV)
H2 = H2.replace('<meta charset="utf-8"><!-- page 9.75.0 over 9.74.0', '<meta charset="utf-8"><!-- page 9.76.0 over 9.75.0 (owner rulings of 2026-11-14 and 2026-11-24): the chapter code, library 1.1.0 and lecture follow the deck 3.6.0; no comparison with everyday things, no lambda; the Turtle files embedded are repository files. -->\n<!-- page 9.75.0 over 9.74.0', 1)

# ------------------------------------------------------------------ embedded Turtle files: byte-exact repository files under their real names
FILES = {"sen0401_ch01_document_v1_2_1.ttl": ("sen0401_ch01_document_v1_3_0.ttl", RD), "sen0401_ch01_domain_abox_v1_2_0.ttl": ("sen0401_ch01_domain_abox_v1_3_0.ttl", RD),
         "sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", os.path.join(REPO, "03-materials"))}
changed = 0
def rep(m):
    global changed
    k, name, sha, body = m.group(1), m.group(2), m.group(3), m.group(4); base = name.split("@")[0]
    assert hashlib.sha256(body.encode()).hexdigest()[:len(sha)] == sha, "the committed page's own hash did not match: " + name
    if base not in FILES: return m.group(0)
    new, d = FILES[base]
    oldtxt = open(os.path.join(d, base) if os.path.exists(os.path.join(d, base)) else os.path.join(REPO, "03-materials", "ch01", "rdodi", base), encoding="utf-8", newline="").read()
    assert oldtxt == body, "the embedded %s is not the repository file %s" % (name, base)
    txt = open(os.path.join(d, new), encoding="utf-8", newline="").read()
    changed += 1; say("embedded Turtle replaced:", name, "->", new)
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (k, new, hashlib.sha256(txt.encode()).hexdigest()[:16], txt)
H2 = re.sub(r'<script type="text/turtle" data-kind="([^"]*)" data-name="([^"]*)" data-sha256="([0-9a-f]+)">(.*?)</script>', rep, H2, flags=re.S)
parts = re.split(r'(<script type="text/turtle".*?</script>)', H2, flags=re.S)
for i in range(0, len(parts), 2):
    for o, n in (("sen0401_materials_v1_4_14.ttl", "sen0401_materials_v1_4_15.ttl"), ("sen0401_ch01_document_v1_2_1.ttl", "sen0401_ch01_document_v1_3_0.ttl"), ("sen0401_ch01_domain_abox_v1_2_0.ttl", "sen0401_ch01_domain_abox_v1_3_0.ttl")):
        parts[i] = parts[i].replace(o, n)
H2 = "".join(parts)
open(DST, "w", encoding="utf-8", newline="").write(H2)
open(os.path.join(PH, "patch_v9_76_0_report.txt"), "w").write("\n".join(REPORT) + "\n")
with open(os.path.join(PH, "patch_v9_76_0_removed.txt"), "w") as f:
    for piece, before, after in REMOVED: f.write("REMOVED: %r\n   before: %r\n   after : %r\n" % (piece[:400], before, after))
say("written", DST, len(H2), "bytes; embedded Turtle files replaced:", changed)
