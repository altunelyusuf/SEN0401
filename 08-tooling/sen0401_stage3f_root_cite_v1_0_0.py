#!/usr/bin/env python3
"""sen0401_stage3f_root_cite v1.0.0 - new PATCH version of the Stage 3 document of chapters 5, 6 and 7 (Stage3.F repair, 2026-10-14).
Cause: the only individual without a citation the Stage 3.F reader can see is the document's root section, whose definition describes the method
of the document and names no source. The reader takes only '(Name and Name, 2023)' / '(Name et al., 2020)' / 'Name (2023)' (no comma inside the author part).
Fix: one sentence appended to the root definition, citing two sources that the chapter's research file already holds and whose pages were opened on
2026-10-14: the book chapter (Antonopoulos and Harding, 2023; raw .adoc at the research file's own URL, first heading read) and Bitcoin Core (2026)
(chapter 5: the 31.1 release directory bitcoincore.org/bin/bitcoin-core-31.1/ with SHA256SUMS; chapters 6, 7: the source at the pinned commit 05bc2f5).
Nothing else changes. Usage: sen0401_stage3f_root_cite_v1_0_0.py   (reads the newest document of each chapter, writes the next patch version; never overwrites)"""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
SENT = {
 5: " The chapter is chapter 5, Wallet Recovery, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023), and the release it is compared with is Bitcoin Core 31.1, published in the project's release directory with signed checksums (Bitcoin Core, 2026).",
 6: " The chapter is chapter 6, Transactions, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023), and the code it is compared with is Bitcoin Core's source tree at one pinned commit (Bitcoin Core, 2026).",
 7: " The chapter is chapter 7, Authorization and Authentication, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023), and the interpreter and test data it is compared with are Bitcoin Core's own, at one pinned commit (Bitcoin Core, 2026).",
}
for n in (5, 6, 7):
    d = os.path.join(ROOT, "03-materials", "ch%02d" % n, "rdodi")
    src = sorted(glob.glob(os.path.join(d, "sen0401_ch%02d_document_v*.ttl" % n)), key=vk)[-1]
    a, b, c = vk(src); old = "%d.%d.%d" % (a, b, c); new = "%d.%d.%d" % (a, b, c + 1)
    dst = os.path.join(d, "sen0401_ch%02d_document_v%d_%d_%d.ttl" % (n, a, b, c + 1))
    if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
    t = open(src, encoding="utf-8").read()
    root = re.search(r'(chx:Document a doc:ReportSection ; rdfs:label "[^"]*"@en ; skos:definition ")([^"]*)(")', t)
    assert root and t.count("chx:Document a doc:ReportSection") == 1
    t = t[:root.start()] + root.group(1) + root.group(2) + SENT[n] + root.group(3) + t[root.end():]
    assert t.count('owl:versionInfo "%s"' % old) == 1
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new)
    a1 = 'owl:versionIRI <http://example.org/sen0401/ch%02d/document/%s> ; rdfs:comment "' % (n, old)
    assert t.count(a1) == 1
    t = t.replace(a1, 'owl:versionIRI <http://example.org/sen0401/ch%02d/document/%s> ; rdfs:comment "%s is a PATCH of %s: it appends to the root section one sentence naming the book chapter and Bitcoin Core, each as (Author, Year), so that RDODI Stage 3.F reads a citation there; no concept and no other text changes. Note of %s: ' % (n, new, new, old, old))
    t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-14"', t, count=1); assert k == 1
    t, k = re.subn(r'dcterms:identifier "sen0401_ch%02d_document_v[0-9_]+"' % n, 'dcterms:identifier "sen0401_ch%02d_document_v%d_%d_%d"' % (n, a, b, c + 1), t, count=1); assert k == 1
    t, k = re.subn(r'( ; )?prov:wasRevisionOf <[^>]*>', '', t, count=1)
    t = t.replace('dcterms:identifier "sen0401_ch%02d_document_v%d_%d_%d"' % (n, a, b, c + 1), 'dcterms:identifier "sen0401_ch%02d_document_v%d_%d_%d" ; prov:wasRevisionOf <http://example.org/sen0401/ch%02d/document/%s>' % (n, a, b, c + 1, n, old), 1)
    open(dst, "w", encoding="utf-8").write(t)
    print("wrote", os.path.relpath(dst, ROOT))
