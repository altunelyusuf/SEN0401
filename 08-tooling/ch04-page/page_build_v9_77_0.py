#!/usr/bin/env python3
"""page_build v9.77.0 (chapter 4): builds sen0401_ch04_page_v9_77_0.html from v9_76_0 (which stays as it is).
Changes (rulings of 2026-11-14 and 2026-11-24): the lecture (slide notes) is the notes of the deck v3_8_0, the takeaway lines carry no everyday analogy; the five book sentences of the page data that offered an
analogy or asked the reader to imagine a scene are rewritten, in the page data and in the new document file 1.2.2 (embedded in place of 1.2.1); the chapter code is chapter_code_ch04_v1_2_0.json (22 examples, the
library 1.1.0 and its wheel); 'Run slide code' is its own top menu item; the shared materials file is the unmodified v1_4_15 (v1_4_14 carried a key-analogy sentence).
Every replaced Turtle block is a byte-identical copy of a repository file under its real name, data-sha256 = first 16 hex characters of its SHA-256.
Usage: python3 page_build_v9_77_0.py"""
import re, json, os, hashlib
from pptx import Presentation
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PG = os.path.join(ROOT, "03-materials", "ch04", "page"); RD = os.path.join(ROOT, "03-materials", "ch04", "rdodi")
old = open(os.path.join(PG, "sen0401_ch04_page_v9_76_0.html"), encoding="utf-8", newline="").read()
man = json.load(open(os.path.join(PG, "chapter_code_ch04_v1_2_0.json")))
deck = Presentation(os.path.join(ROOT, "03-materials", "ch04", "SEN0401_Ch04_KeysAndAddresses_3e_v3_8_0.pptx"))
whl = os.path.join(ROOT, "03-materials", "ch04", "assets", "sen0401_ch04_lib-1.1.0-py3-none-any.whl")
REPL = [("since the key is long: imagine Bob reading the two 64-digit coordinates to Alice over the phone", "since the key is long: its two coordinates have 64 digits each, which is far too much to read to Alice over the phone"),
        ("The book offers an analogy: the difference is like that between the decimal numbers 100 and 99, where 100 is one digit longer", "The book shows the effect with decimal numbers: 100 is one digit longer than 99"),
        ("The book points out how long it is: imagine Bob reading the two 64-digit coordinates of his key to Alice over the telephone", "The book points out how long it is: each of the two coordinates has 64 digits, which Bob could hardly read to Alice over the telephone"),
        ("an output script that acts like a public key, and bitcoin spending is authorised by an input script that acts like a signature", "an output script that plays the role of a public key, and bitcoin spending is authorised by an input script that plays the role of a signature"),
        ("cases the implementer did not think of -", "cases the implementer did not anticipate -")]
hits = [0]
def clean(x):
    if isinstance(x, str):
        for a, b in REPL:
            if a in x: hits[0] += x.count(a); x = x.replace(a, b)
        return x
    if isinstance(x, dict): return {k: (v if k == "py_wheels" else clean(v)) for k, v in x.items()}
    if isinstance(x, list): return [clean(v) for v in x]
    return x
m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', old, re.S)
D = clean(json.loads(m.group(2)))
# lecture: notes of the deck, takeaway and title lines without analogy
NEW_TITLES = {2: "Today's route through the chapter", 5: "Part 2: Public Key Cryptography", 15: "A finite field: arithmetic that wraps at p", 24: "Part 3: Legacy Addresses",
              41: "Part 4: Script Hashes and Bech32", 58: "Part 5: Private Key Formats", 62: "Part 6: Advanced Keys and Addresses"}
assert len(D["lecture"]) == len(deck.slides) == 79
for e, s in zip(D["lecture"], deck.slides):
    e["say"] = s.notes_slide.notes_text_frame.text
    if e["n"] in NEW_TITLES: e["title"] = NEW_TITLES[e["n"]]
    if "Think of each row" in e.get("takeaway", ""): e["takeaway"] = "Each row names one concept and says what it means"
    e["takeaway"] = e.get("takeaway", "").replace("twenty-one examples", "twenty-two examples")
D["chaptercode"] = {"file": "03-materials/ch04/page/chapter_code_ch04_v1_2_0.json", "version": "1.2.0",
                    "examples": [{"order": e["order"], "name": e["name"], "code": e["code"], "slide": e["slide"]} for e in man["examples"]]}
D["py_wheels"] = [{"name": os.path.basename(whl), "hex": open(whl, "rb").read().hex()}]
D["_version"] = "9.77.0"
js = json.dumps(D, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
new = old[:m.start(2)] + js + old[m.end(2):]
# embedded Turtle: two blocks are replaced by real files
BLK = re.compile(r'<script type="text/turtle" data-kind="(\w+)" data-name="([^"]+)" data-sha256="(\w+)">(.*?)</script>', re.S)
SWAP = {"sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", os.path.join(ROOT, "03-materials", "sen0401_materials_v1_4_15.ttl")),
        "sen0401_ch04_document_v1_2_1.ttl": ("sen0401_ch04_document_v1_2_2.ttl", os.path.join(RD, "sen0401_ch04_document_v1_2_2.ttl"))}
done = []
def blk(mm):
    kind, name, sha, body = mm.groups()
    if name not in SWAP: return mm.group(0)
    nm, path = SWAP[name]; b = open(path, encoding="utf-8", newline="").read(); done.append(nm)
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, nm, hashlib.sha256(b.encode("utf-8")).hexdigest()[:16], b)
new = BLK.sub(blk, new); assert len(done) == 2, done
for a, b in (("sen0401_materials_v1_4_14", "sen0401_materials_v1_4_15"), ("sen0401_ch04_document_v1_2_1", "sen0401_ch04_document_v1_2_2"), ("sen0401_ch04_lib_v1_0_0", "sen0401_ch04_lib_v1_1_0")):
    new = new.replace(a, b)
# menu: 'Run slide code' is its own top item, no longer inside Learn
a = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"; assert new.count(a) == 1, "chapter code entry"
new = new.replace(a, "")
b = "const VIEWS=[['learn','📚 Learn'],"; c = "const VIEWS=[['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),"
if b in new: new = new.replace(b, c, 1)
else:
    b = b.replace("'", "\\'"); assert new.count(b) == 1, "VIEWS not found"; new = new.replace(b, c.replace("'", "\\'"), 1)
open(os.path.join(PG, "sen0401_ch04_page_v9_77_0.html"), "w", encoding="utf-8", newline="").write(new)
print("book sentences rewritten in the page data:", hits[0], "| blocks swapped:", done, "| wrote v9_77_0", len(new))
