#!/usr/bin/env python3
"""ch10 page 9.94.0 -> 9.95.0: every embedded Turtle block that was edited is replaced by the byte-exact content of a real repository file under its real name
(register 1.4.15, chapter abox/document 1.3.0, book extract 1.0.0), data-sha256 recomputed. Run from the repository root."""
import re, hashlib
P = "03-materials/ch10/page/"; R = "03-materials/ch10/rdodi/"
p = open(P + "sen0401_ch10_page_v9_94_0.html", encoding="utf-8", newline="").read()
files = {"mastering_bitcoin_3e_ch10_v1_1_0.ttl": ("sen0401_ch10_book_extract_v1_0_0.ttl", R), "sen0401_materials_v1_4_14.ttl": ("sen0401_materials_v1_4_15.ttl", "03-materials/"),
        "sen0401_ch10_domain_abox_v1_2_0.ttl": ("sen0401_ch10_domain_abox_v1_3_0.ttl", R), "sen0401_ch10_document_v1_2_0.ttl": ("sen0401_ch10_document_v1_3_0.ttl", R)}
def rep(m):
    k, name, body = m.group(1), m.group(2), m.group(4); base = name.split("@")[0]
    if base not in files: return m.group(0)
    new, d = files[base]; txt = open(d + new, encoding="utf-8", newline="").read()
    return '<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (k, new, hashlib.sha256(txt.encode()).hexdigest()[:16], txt)
p2 = re.sub(r'<script type="text/turtle" data-kind="([^"]*)" data-name="([^"]*)" data-sha256="([0-9a-f]+)">(.*?)</script>', rep, p, flags=re.S)
p2 = p2.replace('content="9.94.0"', 'content="9.95.0"').replace('"_version": "9.94.0"', '"_version": "9.95.0"')
parts = re.split(r'(<script type="text/turtle".*?</script>)', p2, flags=re.S)
for i in range(0, len(parts), 2):
    parts[i] = parts[i].replace("03-materials/sen0401_materials_v1_4_14.ttl", "03-materials/sen0401_materials_v1_4_15.ttl").replace("3e/01-ontologies/mastering_bitcoin_3e_ch10_v1_1_0.ttl", "03-materials/ch10/rdodi/sen0401_ch10_book_extract_v1_0_0.ttl")
open(P + "sen0401_ch10_page_v9_95_0.html", "w", encoding="utf-8", newline="").write("".join(parts)); print("wrote 9.95.0")
