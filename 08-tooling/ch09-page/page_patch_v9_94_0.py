#!/usr/bin/env python3
"""page_patch v9.94.0 (chapter 9) - makes the course page 9.94.0 from 9.93.0 (never edited): (1) the page carries the new wheel sen0401_ch09_lib-1.1.0 (library v1_1_0, whose rules name the Bitcoin Core function they follow;
the code is unchanged) and its boot imports sen0401_ch09_lib_v1_1_0; (2) the register embedded in the page is the real file 03-materials/sen0401_materials_v1_4_15.ttl under its own name and digest, byte for byte
(the earlier hand-removed clause is gone because the file itself no longer has it); (3) the embedded chapter document and domain ABox are the files sen0401_ch09_document_v1_0_2.ttl and sen0401_ch09_domain_abox_v1_0_2.ttl
(already byte-equal to the files). Run: python3 page_patch_v9_94_0.py"""
__version__ = "9.94.0"
import hashlib, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE)); M9 = os.path.join(ROOT, "03-materials", "ch09")
OLD = os.path.join(M9, "page", "sen0401_ch09_page_v9_93_0.html"); NEW = os.path.join(M9, "page", "sen0401_ch09_page_v9_94_0.html")
h = open(OLD, encoding="utf-8").read()
i = re.search(r'<script type="application/json" id="data">', h).end(); j = h.index("</script>", i)
D = json.loads(h[i:j]); assert json.dumps(D, ensure_ascii=False).replace("</", "<\\/") == h[i:j]
wb = open(os.path.join(M9, "assets", "sen0401_ch09_lib-1.1.0-py3-none-any.whl"), "rb").read()
assert len(D["py_wheels"]) == 1
D["py_wheels"][0] = {"name": "sen0401_ch09_lib-1.1.0-py3-none-any.whl", "hex": wb.hex()}
assert D["py_boot"].count("sen0401_ch09_lib_v1_0_1") == 1
D["py_boot"] = D["py_boot"].replace("sen0401_ch09_lib_v1_0_1", "sen0401_ch09_lib_v1_1_0")
D["chaptercode"]["file"] = "03-materials/ch09/page/chapter_code_ch09_v1_2_0.json"; D["chaptercode"]["version"] = "1.2.0"
D["_version"] = "9.94.0"
s = json.dumps(D, ensure_ascii=False).replace("</", "<\\/")
s = s.replace("03-materials/sen0401_materials_v1_4_14.ttl", "03-materials/sen0401_materials_v1_4_15.ttl").replace("the materials register is 1.4.14", "the materials register is 1.4.15")
out = h[:i] + s + h[j:]
reg = open(os.path.join(ROOT, "03-materials", "sen0401_materials_v1_4_15.ttl"), encoding="utf-8").read()
m = re.search(r'<script type="text/turtle" data-kind="course" data-name="sen0401_materials_v1_4_14\.ttl" data-sha256="\w+">', out); e = out.index("</script>", m.end())
out = out[:m.start()] + '<script type="text/turtle" data-kind="course" data-name="sen0401_materials_v1_4_15.ttl" data-sha256="%s">' % hashlib.sha256(reg.encode()).hexdigest()[:16] + reg + out[e:]
a = '<meta name="version" content="9.93.0">'; assert out.count(a) == 1; out = out.replace(a, '<meta name="version" content="9.94.0">')
open(NEW, "w", encoding="utf-8").write(out)
json.dump(D, open(os.path.join(HERE, "page_data_v9_94_0.json"), "w"), ensure_ascii=False, indent=1)
print("page written", NEW, len(out))
