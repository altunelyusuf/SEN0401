#!/usr/bin/env python3
"""sen0401_ch12_page_fix v1.1.0 - closes the chapter 12 gaps after page 9.96.0 (never edits an existing version): the library 1.1.0 wheel (Bitcoin Core references), the chapter-code manifest 1.4.0, and the Turtle copies:
every Turtle block of page 9.97.0 is byte-identical to a file of the repository (the new files sen0401_ch12_domain_tbox/abox/document_v1_0_2.ttl and sen0401_ch12_diagrams_abox_v1_0_0.ttl, written here from the edited
copies of 9.96.0; the course register sen0401_materials_v1_4_15.ttl; the unchanged files; the book file of the mastering-bitcoin repository). Chapter 12 only.
Usage: python3 sen0401_ch12_page_fix_v1_1_0.py"""
__version__ = "1.1.0"
import glob, hashlib, json, os, re, sys
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); PD = os.path.join(REPO, "03-materials", "ch12", "page"); RD = os.path.join(REPO, "03-materials", "ch12", "rdodi")
SRC = os.path.join(PD, "sen0401_ch12_page_v9_96_0.html"); DST = os.path.join(PD, "sen0401_ch12_page_v9_97_0.html"); DATA_OUT = os.path.join(REPO, "08-tooling", "ch12-page", "page_data_v9_97_0.json")
MAN = os.path.join(PD, "chapter_code_ch12_v1_4_0.json"); WHL = os.path.join(REPO, "03-materials", "ch12", "assets", "sen0401_ch12_lib-1.1.0-py3-none-any.whl")
MAT = os.path.join(REPO, "03-materials", "sen0401_materials_v1_4_15.ttl"); BOOK = os.path.join(os.path.dirname(REPO), "..", "mastering-bitcoin", "3e", "01-ontologies", "mastering_bitcoin_3e_ch12_v1_1_1.ttl")
for p in (DST, DATA_OUT):
    assert not os.path.exists(p), p
H = open(SRC, encoding="utf-8").read()
BLK = re.compile(r'<script type="text/turtle"( data-kind="[^"]*") data-name="([^"]*)" data-sha256="([^"]*)">(.*?)</script>', re.S)
blocks = {m.group(2): m for m in BLK.finditer(H)}
def sha(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()[:16]
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s):
    assert not os.path.exists(p), p; open(p, "w", encoding="utf-8", newline="").write(s)

# ---- 1. the new Turtle files from the edited copies of page 9.96.0
def bump(body, kind, old="1.0.1", new="1.0.2"):
    iri = "http://example.org/sen0401/ch12/%s" % kind
    for a, b in (('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new), ("<%s/%s>" % (iri, old), "<%s/%s>" % (iri, new)),
                 ('dcterms:identifier "sen0401_ch12_%s_v%s"' % (kind, old.replace(".", "_")), 'dcterms:identifier "sen0401_ch12_%s_v%s"' % (kind, new.replace(".", "_")))):
        assert body.count(a) == 1, a; body = body.replace(a, b)
    a = 'dcterms:modified "2026-10-15"^^xsd:date'; assert body.count(a) == 1; body = body.replace(a, 'dcterms:modified "2026-11-24"^^xsd:date')
    a = '    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch12-rdodi-run> ;'; assert body.count(a) == 1
    return body.replace(a, '    prov:wasRevisionOf <%s/%s> ;\n' % (iri, old) + a)
new_files = {}
tb = bump(blocks["sen0401_ch12_domain_tbox_v1_0_1.ttl"].group(4), "tbox")
ab = bump(blocks["sen0401_ch12_domain_abox_v1_0_1.ttl"].group(4), "abox")
dc = bump(blocks["sen0401_ch12_document_v1_0_1.ttl"].group(4), "document")
n_lib = ab.count("sen0401_ch12_lib_v1_0_0"); ab = ab.replace("sen0401_ch12_lib_v1_0_0", "sen0401_ch12_lib_v1_1_0")
bad = "R = L.run(); def f(n, w='w'): return "; n_def = ab.count(bad); assert n_def >= 1
ab = ab.replace(bad, "R = L.run()\\ndef f(n, w='w'): return ")      # a def cannot follow a semicolon: the program is two lines
assert "Dice analogy" not in tb.replace('chx:DiceAnalogy', '') and "Dice analogy" not in ab and "Dice analogy" not in dc
dg = blocks["sen0401_ch12_diagrams_abox_v1_0_0.ttl"].group(4)
new_files = {"sen0401_ch12_domain_tbox_v1_0_2.ttl": tb, "sen0401_ch12_domain_abox_v1_0_2.ttl": ab, "sen0401_ch12_document_v1_0_2.ttl": dc}
for n, b in new_files.items(): wr(os.path.join(RD, n), b)
wr(os.path.join(RD, "sen0401_ch12_diagrams_abox_v1_0_0.ttl"), dg)      # embedded since 9.78.0, never a repository file before
print("ttl files written; library name replaced in the abox", n_lib, "times; def split in", n_def, "labels")

# ---- 2. the page
mf = json.load(open(MAN, encoding="utf-8")); wh = open(WHL, "rb").read(); assert hashlib.sha256(wh).hexdigest() == mf["library"]["sha256"]
tag = '<script type="application/json" id="data">'; a = H.index(tag) + len(tag); b = H.index("</script>", a); data = json.loads(H[a:b])
data["_version"] = "9.97.0"
assert data["py_wheels"][0]["name"] == "sen0401_ch12_lib-1.0.1-py3-none-any.whl"
data["py_wheels"] = [{"name": os.path.basename(WHL), "hex": wh.hex()}]
assert data["py_boot"].count("sen0401_ch12_lib_v1_0_0") == 1
data["py_boot"] = data["py_boot"].replace("sen0401_ch12_lib_v1_0_0", "sen0401_ch12_lib_v1_1_0")
assert mf["setup"]["code"].strip() in data["py_boot"], "the boot snippet must contain the manifest's setup"
cc = data["chaptercode"]; assert len(cc["examples"]) == len(mf["examples"])
for e, me in zip(cc["examples"], mf["examples"]): assert e["slide"] == me["slide"] and e["code"] == me["code"]
cc["file"] = "03-materials/ch12/page/" + os.path.basename(MAN); cc["version"] = "1.4.0"
raw = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
assert raw.count("sen0401_materials_v1_4_14.ttl") == 2
raw = raw.replace("sen0401_materials_v1_4_14.ttl", "sen0401_materials_v1_4_15.ttl")
H2 = H[:a] + raw + H[b:]
H2 = H2.replace('<meta name="version" content="9.96.0">', '<meta name="version" content="9.97.0">'); assert 'content="9.97.0"' in H2
# turtle blocks: the replacement text is the content of a repository file
repl = {"sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", rd(MAT)),
        "sen0401_ch12_domain_tbox_v1_0_1.ttl": ("sen0401_ch12_domain_tbox_v1_0_2.ttl", tb), "sen0401_ch12_domain_abox_v1_0_1.ttl": ("sen0401_ch12_domain_abox_v1_0_2.ttl", ab),
        "sen0401_ch12_document_v1_0_1.ttl": ("sen0401_ch12_document_v1_0_2.ttl", dc)}
def sub(m):
    n = m.group(2)
    if n not in repl: return m.group(0)
    nn, body = repl[n]; return '<script type="text/turtle"%s data-name="%s" data-sha256="%s">%s</script>' % (m.group(1), nn, sha(body), body)
H2 = BLK.sub(sub, H2)
book = rd(BOOK); bm = blocks["mastering_bitcoin_3e_ch12_v1_1_1.ttl@349e3db0"]; assert bm.group(4) == book, "the book block differs from the file of the mastering-bitcoin repository"
open(DST, "w", encoding="utf-8", newline="").write(H2); json.dump(data, open(DATA_OUT, "w", encoding="utf-8"), ensure_ascii=False)
print(os.path.basename(DST), len(H2), "bytes")
