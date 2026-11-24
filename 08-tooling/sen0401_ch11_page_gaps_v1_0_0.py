#!/usr/bin/env python3
"""Chapter 11 page gaps v1.0.0 (SEN0401). Reads the committed page v9_97_0 (never edited) and writes page v9_98_0 and the new source files it embeds:
 1 the chapter's tbox, abox and document ontologies as the page showed them (analogy label, lambdas as def) become repo files v1_2_0 (only the version fields and the modified date differ from the page's copy); the page embeds exactly these files;
 2 the materials register is embedded as the repo file sen0401_materials_v1_4_15.ttl, unmodified; 3 the book file is embedded as a real file of the book repository, unmodified: the new version v1_1_1 written beside v1_1_0 (one listing line '...,' of the book's quoted JSON becomes the single character), so the page's copy is a real file and its recorded SHA-256 prefix is true;
 4 the library wheel 1.1.0 (Bitcoin Core references) with its boot snippet and the chapter-code manifest v1_2_0 replace the 1.0.0 ones; the data version becomes 9.98.0.
The research file and the diagrams ABox are embedded as before (the research is byte-equal to its repo file; the diagrams ABox is embedded only, by the course's A-file ceiling)."""
import re, json, os, hashlib
R = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = R + "/03-materials/ch11/page/sen0401_ch11_page_v9_97_0.html"; OUT = R + "/03-materials/ch11/page/sen0401_ch11_page_v9_98_0.html"
RD = R + "/03-materials/ch11/rdodi/"; BOOK = "/home/claude/mastering-bitcoin/3e/01-ontologies/sen0401_ch11_book_extract_v1_0_0.ttl"
h = open(SRC, encoding="utf-8").read()
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()[:16]
blocks = {m.group(2): m for m in re.finditer(r'<script type="text/turtle" data-kind="(\w+)" data-name="([^"]+)" data-sha256="([0-9a-f]+)">(.*?)</script>', h, re.S)}
new = {}   # old name -> (kind, new name, body)
for kind in ("tbox", "abox", "document"):
    old = "sen0401_ch11_domain_%s_v1_1_0.ttl" % kind if kind != "document" else "sen0401_ch11_document_v1_1_0.ttl"; nn = old.replace("v1_1_0", "v1_2_0")
    body = blocks[old].group(4)
    for a, b in (('owl:versionInfo "1.1.0"', 'owl:versionInfo "1.2.0"'), ("/1.1.0>", "/1.2.0>"), ("_v1_1_0\"", "_v1_2_0\""), ('dcterms:modified "2026-10-22"', 'dcterms:modified "2026-11-24"')):
        assert body.count(a) == 1, (old, a, body.count(a)); body = body.replace(a, b)
    open(RD + nn, "w", encoding="utf-8", newline="").write(body)
    new[old] = (blocks[old].group(1), nn, body)
mat = open(R + "/03-materials/sen0401_materials_v1_4_15.ttl", encoding="utf-8").read(); new["sen0401_materials_v1_4_14.ttl"] = ("course", "sen0401_materials_v1_4_15.ttl", mat)
book = open(BOOK, encoding="utf-8").read(); bn = "sen0401_ch11_book_extract_v1_0_0.ttl"; bk = [k for k in blocks if k.startswith("mastering_bitcoin_3e_ch11")][0]
bk2 = bk.replace("v1_1_0", "v1_1_1"); new[bk] = (blocks[bk].group(1), bk2, book)
def sub(m):
    nm = m.group(2)
    if nm not in new: return m.group(0)
    kind, nn, body = new[nm]
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, nn, sha(body), body)
html = re.sub(r'<script type="text/turtle" data-kind="(\w+)" data-name="([^"]+)" data-sha256="([0-9a-f]+)">(.*?)</script>', sub, h, flags=re.S)
# the data block
m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', html, re.S)
d = json.loads(m.group(2).replace("<\\/", "</"))
pw = json.load(open(R + "/08-tooling/ch11-page/pywheels_v1_2_0.json")); man = json.load(open(R + "/03-materials/ch11/page/chapter_code_ch11_v1_2_0.json"))
wf = R + "/03-materials/ch11/assets/" + pw["wheels"][0]["file"]; wb = open(wf, "rb").read(); assert hashlib.sha256(wb).hexdigest() == pw["wheels"][0]["sha256"] == man["library"]["sha256"]
d["py_wheels"] = [{"name": pw["wheels"][0]["file"], "hex": wb.hex()}]; d["py_boot"] = pw["boot_python"]
import zipfile; nev = len([n for n in zipfile.ZipFile(wf).namelist() if n.startswith("ch11-evidence/")])
assert "(31 files:" in d["notice"]; d["notice"] = d["notice"].replace("(31 files:", "(%d files:" % nev)
d["chaptercode"] = {"file": man["file"], "version": man["version"], "examples": man["examples"]}
s = json.dumps(d, ensure_ascii=False).replace("sen0401_materials_v1_4_14.ttl", "sen0401_materials_v1_4_15.ttl").replace("3e/01-ontologies/mastering_bitcoin_3e_ch11_v1_1_0.ttl", "3e/01-ontologies/sen0401_ch11_book_extract_v1_0_0.ttl")
d = json.loads(s); d["_version"] = "9.98.0"
html = html[:m.start(2)] + json.dumps(d, ensure_ascii=False).replace("</", "<\\/") + html[m.end(2):]
open(OUT, "w", encoding="utf-8").write(html)
json.dump(d, open(R + "/08-tooling/ch11-page/page_data_v9_98_0.json", "w", encoding="utf-8"), ensure_ascii=False)
print("page", OUT, os.path.getsize(OUT))
