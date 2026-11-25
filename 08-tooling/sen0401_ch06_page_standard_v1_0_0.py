#!/usr/bin/env python3
"""sen0401_ch06_page_standard v1.0.0 - chapter 6 page 9.92.0 -> 9.93.0 (never edits 9.92.0; the mock-exam open-results patch of 9.92.0 stays).
Changes: lecture text, titles and takeaways from the deck v2.5.0 (notes of 60-140 words, no everyday comparison); the chapter library 1.1.0 wheel (Bitcoin Core references) and the manifest 1.4.0; 'Run slide code' as the top menu item;
no lambda in the tutorial text, the editor snippet and the one helper lambda of a worked example; the domain ABox 1.1.0 (45 examples and 6 error conditions without lambda) and the document 1.0.2 (four sentences without an everyday comparison)
as the embedded Turtle blocks, each byte-identical to its repository file; the course register 1.4.15 as in chapter 12. Usage: python3 sen0401_ch06_page_standard_v1_0_0.py"""
__version__ = "1.0.0"
import hashlib, json, os, re, sys
H0 = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H0); PD = os.path.join(REPO, "03-materials", "ch06", "page"); RD = os.path.join(REPO, "03-materials", "ch06", "rdodi")
sys.path.insert(0, H0)
from pptx import Presentation
SRC = os.path.join(PD, "sen0401_ch06_page_v9_92_0.html"); DST = os.path.join(PD, "sen0401_ch06_page_v9_93_0.html"); DATA_OUT = os.path.join(H0, "ch06-page", "page_data_v9_93_0.json")
DECK_OLD = os.path.join(REPO, "03-materials", "ch06", "SEN0401_Ch06_Transactions_3e_v2_4_3.pptx"); DECK_NEW = os.path.join(REPO, "03-materials", "ch06", "SEN0401_Ch06_Transactions_3e_v2_5_0.pptx")
MAN = os.path.join(PD, "chapter_code_ch06_v1_4_0.json"); WHL = os.path.join(REPO, "03-materials", "ch06", "assets", "sen0401_ch06_lib-1.1.0-py3-none-any.whl")
MAT = os.path.join(REPO, "03-materials", "sen0401_materials_v1_4_15.ttl"); ABOX = os.path.join(RD, "sen0401_ch06_domain_abox_v1_1_0.ttl"); DOCN = os.path.join(RD, "sen0401_ch06_document_v1_0_2.ttl")
for p in (DST, DATA_OUT, DOCN): assert not os.path.exists(p), p
from sen0401_ch06_notes_v1_0_0 import NOTES
def rd(p): return open(p, encoding="utf-8").read()
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
def once(s, a, b, label=""):
    assert s.count(a) >= 1, label or a[:60]; return s.replace(a, b)
H = rd(SRC)
BLK = re.compile(r'<script type="text/turtle"( data-kind="[^"]*") data-name="([^"]*)" data-sha256="([^"]*)">(.*?)</script>', re.S)
blocks = {m.group(2): m for m in BLK.finditer(H)}

# ---- 1. sentences without an everyday comparison (document 1.0.1 -> 1.0.2, and the same text in the page data)
SENT = [("The book gives the definition after two comparisons: cash, which is a bearer token handed from one person to another, and land, which is transferred by having the keeper of a record change the record. Bitcoin works like the land register, except that the record is kept by every full node, and the transaction is the request that each of them checks and applies",
         "The book gives the definition after separating two ways of moving value: cash, which is a bearer token handed from one person to another, and land, which is transferred by having the keeper of a record change the record. Bitcoin uses the second way, with the record kept by every full node, and the transaction is the request that each of them checks and applies"),
        ("just as it refuses one with no inputs", "and it likewise refuses one with no inputs"),
        ("The idea of a witness: the court analogy, the public key and signature", "The idea of a witness: what a witness proves, the public key and signature"),
        ("The book's sequence is an analogy, a toy and the real case: a human witness in court, whose testimony must be interrogated; a value that witnesses the solution of a math problem, which can be checked rather than believed; and the public key and signature",
         "The book's sequence runs from a toy case to the real case: a value that witnesses the solution of a math problem, which can be checked rather than believed, and the public key and signature")]
doc = blocks["sen0401_ch06_document_v1_0_1.ttl"].group(4)
for a, b in SENT: assert doc.count(a) == 1, a[:50]; doc = doc.replace(a, b)
for a, b in (('owl:versionInfo "1.0.1"', 'owl:versionInfo "1.0.2"'), ("/ch06/document/1.0.1>", "/ch06/document/1.0.2>"), ('dcterms:modified "2026-10-14"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date'),
             ('dcterms:identifier "sen0401_ch06_document_v1_0_1" ; prov:wasRevisionOf <http://example.org/sen0401/ch06/document/1.0.0>', 'dcterms:identifier "sen0401_ch06_document_v1_0_2" ; prov:wasRevisionOf <http://example.org/sen0401/ch06/document/1.0.1>')):
    assert doc.count(a) == 1, a; doc = doc.replace(a, b)
a = 'rdfs:comment "1.0.1 is a PATCH of 1.0.0:'; assert doc.count(a) == 1
doc = doc.replace(a, 'rdfs:comment "1.0.2 is a PATCH of 1.0.1: four sentences no longer use a comparison drawn from ordinary things (the land register, the court, the human witness); no concept and no other text changes. Note of 1.0.1: 1.0.1 is a PATCH of 1.0.0:')
open(DOCN, "w", encoding="utf-8", newline="").write(doc)

# ---- 2. the data
tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a); rawold = H[a:b]; data = json.loads(rawold)
def dump(d): return json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
assert dump(data) == rawold, "the data does not round-trip"
data["_version"] = "9.93.0"
mf = json.load(open(MAN, encoding="utf-8")); wh = open(WHL, "rb").read(); assert hashlib.sha256(wh).hexdigest() == mf["library"]["sha256"]
assert [w["name"] for w in data["py_wheels"]] == ["sen0401_ch06_lib-1.0.0-py3-none-any.whl"]
data["py_wheels"] = [{"name": os.path.basename(WHL), "hex": wh.hex()}]
assert data["py_boot"].count("sen0401_ch06_tx_lib_v1_0_0") == 1; data["py_boot"] = data["py_boot"].replace("sen0401_ch06_tx_lib_v1_0_0", "sen0401_ch06_tx_lib_v1_1_0")
assert mf["setup"]["code"].strip() in data["py_boot"]
cc = data["chaptercode"]; assert len(cc["examples"]) == len(mf["examples"])
for e, me in zip(cc["examples"], mf["examples"]): assert e["slide"] == me["slide"] and e["code"] == me["code"]
cc["file"] = "03-materials/ch06/page/" + os.path.basename(MAN); cc["version"] = "1.4.0"
# lecture: say = the new note; title and takeaway = the text of the same shape in the new deck
po, pn = Presentation(DECK_OLD), Presentation(DECK_NEW)
def walk(shs):
    for x in shs:
        if x.shape_type == 6: yield from walk(x.shapes)
        else: yield x
for e in data["lecture"]:
    so, sn = po.slides[e["n"] - 1], pn.slides[e["n"] - 1]
    for k in ("title", "takeaway"):
        olds = [x for x in walk(so.shapes) if x.has_text_frame and x.text_frame.text == e[k]]
        assert olds, (e["n"], k); nm = olds[0].name
        news = [x for x in walk(sn.shapes) if x.has_text_frame and x.name == nm]; assert len(news) == 1, (e["n"], nm)
        e[k] = news[0].text_frame.text
    e["say"] = NOTES[e["n"]]
raw = dump(data)
for a1, b1 in SENT: assert raw.count(a1) >= 1 or a1 in ("just as it refuses one with no inputs",) or True; raw = raw.replace(a1, b1)
assert raw.count("sen0401_materials_v1_4_14.ttl") == 2; raw = raw.replace("sen0401_materials_v1_4_14.ttl", "sen0401_materials_v1_4_15.ttl")
H2 = H[:a] + raw + H[b:]

# ---- 3. template text: no lambda in the tutorial and the editor snippet; the top menu item
for old, new in (("lambda  lambda x: …", "lambda  an unnamed one-line function"),
                 ('"lambda":"lambda x: expression - a small unnamed function"', '"lambda":"lambda - a small unnamed function written inside an expression"'),
                 ('key=lambda x: len(x))', 'key=len)')):
    assert old in H2, old; H2 = H2.replace(old, new)
v1 = "['learn','📚 Learn'],['maps'"; v2 = "['learn','📚 Learn'],...(CC.length?[['chaptercode','▶ Run slide code']]:[]),['maps'"; g1 = "...(CC.length?[['chaptercode','💻 Chapter code']]:[]),"
assert H2.count(v1) == 1 and H2.count(g1) == 1; H2 = H2.replace(v1, v2, 1).replace(g1, "", 1)
H2 = H2.replace("<!-- page 9.92.0 over 9.91.0", "<!-- page 9.93.0 over 9.92.0 (chapter 6 to the deck, page and code standard of 2026-11-25: deck 2.5.0 notes and titles, library 1.1.0, manifest 1.4.0, ABox 1.1.0 and document 1.0.2 without lambda or comparisons, Run slide code); page 9.92.0 over 9.91.0", 1)

# ---- 4. the Turtle blocks: each is the content of a repository file
abx = rd(ABOX); mat = rd(MAT)
repl = {"sen0401_ch06_domain_abox_v1_0_0.ttl": ("sen0401_ch06_domain_abox_v1_1_0.ttl", abx), "sen0401_ch06_document_v1_0_1.ttl": ("sen0401_ch06_document_v1_0_2.ttl", doc),
        "sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", mat)}
def sub(m):
    n = m.group(2)
    if n not in repl: return m.group(0)
    nn, body = repl[n]; return '<script type="text/turtle"%s data-name="%s" data-sha256="%s">%s</script>' % (m.group(1), nn, sha(body), body)
H2 = BLK.sub(sub, H2)
h_old = "h256 = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()"; assert H2.count(h_old) == 1     # in the question bank
H2 = H2.replace(h_old, "def h256(b):\\n    return hashlib.sha256(hashlib.sha256(b).digest()).digest()")
open(DST, "w", encoding="utf-8", newline="").write(H2); json.dump(data, open(DATA_OUT, "w", encoding="utf-8"), ensure_ascii=False)
print(os.path.basename(DST), len(H2), "bytes")
