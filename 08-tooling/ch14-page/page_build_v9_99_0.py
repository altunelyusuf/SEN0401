#!/usr/bin/env python3
"""page_build v9.99.0 (chapter 14): builds sen0401_ch14_page_v9_99_0.html from v9_98_0 (which stays as it is).
Changes: the page embeds the library wheel 1.1.0 (Bitcoin Core references in the module sources, behaviour unchanged) and the chapter code manifest 1.2.0;
every embedded Turtle block is a byte-identical copy of a real repository file under its real name, data-sha256 = first 16 hex characters of the SHA-256 of the file.
Blocks: the shared materials file v1_4_15 unmodified; document 1.2.0, domain ABox 1.2.0, research 1.0.1 are new files beside the committed ones.
Usage: python3 page_build_v9_99_0.py"""
import re, json, os, hashlib
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PG = os.path.join(ROOT, "03-materials", "ch14", "page")
MB = "/home/claude/mastering-bitcoin/3e/01-ontologies/"
EMB = os.path.join(ROOT, "08-tooling", "ch14-page", "embedded")
RD = os.path.join(ROOT, "03-materials", "ch14", "rdodi")
SRC = {  # block name in v9_98_0 -> (new name, file path)
 "mastering_bitcoin_3e_ch14_v1_1_1.ttl@349e3db0": (None, MB + "mastering_bitcoin_3e_ch14_v1_1_1.ttl"),
 "sen0401_course_v1_2_0.ttl": (None, ROOT + "/00-course-profile/sen0401_course_v1_2_0.ttl"),
 "sen0401_outcomes_v1_1_1.ttl": (None, ROOT + "/01-outcomes/sen0401_outcomes_v1_1_1.ttl"),
 "sen0401_textbook_v1_2_0.ttl": (None, ROOT + "/02-textbook/sen0401_textbook_v1_2_0.ttl"),
 "sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", ROOT + "/03-materials/sen0401_materials_v1_4_15.ttl"),
 "sen0401_ch14_domain_tbox_v1_0_0.ttl": (None, RD + "/sen0401_ch14_domain_tbox_v1_0_0.ttl"),
 "sen0401_ch14_domain_abox_v1_1_0.ttl": ("sen0401_ch14_domain_abox_v1_2_0.ttl", RD + "/sen0401_ch14_domain_abox_v1_2_0.ttl"),
 "sen0401_ch14_document_v1_1_0.ttl": ("sen0401_ch14_document_v1_2_0.ttl", RD + "/sen0401_ch14_document_v1_2_0.ttl"),
 "sen0401_ch14_research_v1_0_0.ttl": ("sen0401_ch14_research_v1_0_1.ttl", RD + "/sen0401_ch14_research_v1_0_1.ttl"),
 "sen0401_ch14_diagrams_abox_v1_0_0.ttl": (None, RD + "/sen0401_ch14_diagrams_abox_v1_0_0.ttl"),
 "cme_standards_adoption_tbox_v1_1_0.ttl": (None, EMB + "/cme_standards_adoption_tbox_v1_1_0.ttl"),
 "cme_standards_adoption_v1_3_0.ttl": (None, EMB + "/cme_standards_adoption_v1_3_0.ttl"),
}
old = open(os.path.join(PG, "sen0401_ch14_page_v9_98_0.html"), encoding="utf-8").read()
BLK = re.compile(r'<script type="text/turtle" data-kind="(\w+)" data-name="([^"]+)" data-sha256="(\w+)">(.*?)</script>', re.S)
# 1 the blocks: real files, real names, real digests
def blk(m):
    kind, name, _, _ = m.groups(); new, path = SRC[name]
    body = open(path, encoding="utf-8", newline="").read()
    nm = (new or name)
    if "@" in name and new is None: nm = name
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, nm, hashlib.sha256(body.encode("utf-8")).hexdigest()[:16], body)
parts = []; pos = 0; out = []
for m in BLK.finditer(old):
    out.append(("t", old[pos:m.start()])); out.append(("b", blk(m))); pos = m.end()
out.append(("t", old[pos:]))
# 2 text outside the blocks: names, data
whl = os.path.join(ROOT, "03-materials", "ch14", "assets", "sen0401_ch14_lib-1.1.0-py3-none-any.whl")
hexw = open(whl, "rb").read().hex()
def fix_text(s):
    m = re.search(r'(<script type="application/json" id="data">)(.*?)(</script>)', s, re.S)
    if m:
        D = json.loads(m.group(2))
        D["py_wheels"] = [{"name": os.path.basename(whl), "hex": hexw}]
        D["_version"] = "9.99.0"
        D["chaptercode"]["file"] = "03-materials/ch14/page/chapter_code_ch14_v1_2_0.json"; D["chaptercode"]["version"] = "1.2.0"
        js = json.dumps(D, ensure_ascii=False, separators=(", ", ": ")).replace("</", "<\\/")
        s = s[:m.start(2)] + js + s[m.end(2):]
    for a, b in [("sen0401_ch14_lib_v1_0_0", "sen0401_ch14_lib_v1_1_0"), ("sen0401_ch14_crypto_v1_0_0", "sen0401_ch14_crypto_v1_1_0"),
                 ("sen0401_materials_v1_4_14", "sen0401_materials_v1_4_15"), ("sen0401_ch14_research_v1_0_0", "sen0401_ch14_research_v1_0_1")]:
        s = s.replace(a, b)
    return s
new = "".join(fix_text(x) if k == "t" else x for k, x in out)
open(os.path.join(PG, "sen0401_ch14_page_v9_99_0.html"), "w", encoding="utf-8", newline="").write(new)
print("wrote sen0401_ch14_page_v9_99_0.html", len(new))
