#!/usr/bin/env python3
"""sen0401_stage3f_cite_ch01 v1.0.0 - new PATCH version of the chapter 1 Stage 3 document (Stage3.F repair, 2026-10-20).
Cause (read from the RDODI Stage 3.F reader, stage3f_ttl_bridge_v1_3_0): the one section whose definition holds no '(Name and Name, Year)' citation is the root section (chx:Document); every other
section of the document already cites.
Fix, as for chapters 2-4 (b4c7a07): one sentence appended to that definition, citing only a source the chapter research file already holds - P01, Mastering Bitcoin 3rd edition chapter 1
(Antonopoulos and Harding, 2023; tag third_edition_print1), saved in 08-tooling/ch01-sources/ch01_intro.adoc. Nothing else changes; no concept is added.
Usage: sen0401_stage3f_cite_ch01_v1_0_0.py  (reads the newest chapter 1 document, writes the next patch version; never overwrites)"""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
n = 1
ADD = {"Document": " The chapter renewed here is chapter 1, Introduction, of Mastering Bitcoin, third edition, as published at the tag third_edition_print1 (Antonopoulos and Harding, 2023)."}
d = os.path.join(ROOT, "03-materials", "ch01", "rdodi")
src = sorted(glob.glob(os.path.join(d, "sen0401_ch01_document_v*.ttl")), key=vk)[-1]
a, b, c = vk(src); old = "%d.%d.%d" % (a, b, c); new = "%d.%d.%d" % (a, b, c + 1)
dst = os.path.join(d, "sen0401_ch01_document_v%d_%d_%d.ttl" % (a, b, c + 1))
if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
t = open(src, encoding="utf-8").read()
for sid, sent in ADD.items():
    i = t.index("chx:%s a doc:" % sid); j = t.index('skos:definition "', i) + len('skos:definition "')
    k = j
    while not (t[k] == '"' and t[k-1] != "\\"): k += 1
    assert k - i < 20000
    t = t[:k] + sent + t[k:]
assert t.count('owl:versionInfo "%s"' % old) == 1
t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new)
a1 = 'owl:versionIRI <http://example.org/sen0401/ch01/document/%s> ; rdfs:comment "' % old
assert t.count(a1) == 1
t = t.replace(a1, 'owl:versionIRI <http://example.org/sen0401/ch01/document/%s> ; rdfs:comment "%s is a PATCH of %s: it appends to the root section definition one sentence that cites, as (Author, Year), a source the chapter research file already holds (P01), so that RDODI Stage 3.F reads a citation there; no concept and no other text changes. Note of %s: ' % (new, new, old, old))
t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-20"', t, count=1); assert k == 1
t, k = re.subn(r'dcterms:identifier "sen0401_ch01_document_v[0-9_]+"', 'dcterms:identifier "sen0401_ch01_document_v%d_%d_%d"' % (a, b, c + 1), t, count=1); assert k == 1
t, k = re.subn(r'prov:wasRevisionOf <[^>]*>', 'prov:wasRevisionOf <http://example.org/sen0401/ch01/document/%s>' % old, t, count=1); assert k == 1
open(dst, "w", encoding="utf-8").write(t)
print("wrote", os.path.relpath(dst, ROOT))
