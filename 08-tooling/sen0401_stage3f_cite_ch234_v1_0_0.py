#!/usr/bin/env python3
"""sen0401_stage3f_cite_ch234 v1.0.0 - new PATCH version of the Stage 3 document of chapters 2, 3 and 4 (Stage3.F repair, 2026-10-19).
Cause (read from the RDODI Stage 3.F reader, stage3f_ttl_bridge_v1_0_0): a section whose definition holds no '(Name and Name, Year)' / '(Name et al., Year)' / 'Name (Year)'
citation counts as an uncited claim. Chapter 2: the root section. Chapter 3: the root section, Computing foundations, Representation, Systems. Chapter 4: the root section and Semantics.
Fix: one sentence appended to each of those definitions, citing only sources the chapter's own research file already holds (Publication P-numbers named below), each of them a
page or file the research records as read: ch2 P01, P32 (Bitcoin Core, 2026); ch3 P01, P09, P57, P58, P52, P07, P91, P80, P83 ; ch4 P01, P02, P05, P08 and P23. Nothing else changes; no concept is added.
Usage: sen0401_stage3f_cite_ch234_v1_0_0.py  (reads the newest document of each chapter, writes the next patch version; never overwrites)"""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
ADD = {
 2: {"Document": " The chapter is chapter 2, How Bitcoin Works, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023), and the rules against which its transaction is recomputed, for example that the transaction identifier is the hash of the serialization, are those of Bitcoin Core's source at one pinned commit (Bitcoin Core, 2026)."},
 3: {"Document": " The chapter is chapter 3, Bitcoin Core: The Reference Implementation, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023), and the release it is checked against is Bitcoin Core 31.1, published in the project's release directory with signed checksums (Bitcoin Core, 2026).",
     "S_Computing": " The sources of the branch are the ones the chapter's evidence names: the byte and unit definitions in Bitcoin Core's source (Bitcoin Core, 2026), the list of files and directories in the project's own documentation (Bitcoin Core, 2026), and the data encodings that standards define (Josefsson, 2006).",
     "S_Representation": " The Base64 text form is defined by RFC 4648 (Josefsson, 2006), and the helpers that convert between bytes, units and hexadecimal text, and the source of random bytes, are read in Bitcoin Core's own files (Bitcoin Core, 2026).",
     "S_Systems": " The layout of the data directory is described in the project's file documentation (Bitcoin Core, 2026), the database that holds a wallet is described by its makers (SQLite, 2026), and the protocol through which a client speaks to the node is specified by the HTTP semantics standard (Fielding et al., 2022)."},
 4: {"Document": " The chapter is chapter 4, Keys and Addresses, of Mastering Bitcoin, third edition (Antonopoulos and Harding, 2023); the curve the keys live on is the one defined in the Standards for Efficient Cryptography (Certicom Research, 2010), and the release the results are compared with is Bitcoin Core 31.1 (Bitcoin Core, 2026).",
     "S_Semantics": " The standard named here is Decentralized Identifiers (DIDs) v1.0, a recommendation of the World Wide Web Consortium (World Wide Web Consortium, 2022), and the kind of name it builds on is the uniform resource identifier of RFC 3986 (Berners-Lee et al., 2005)."},
}
for n in (2, 3, 4):
    d = os.path.join(ROOT, "03-materials", "ch%02d" % n, "rdodi")
    src = sorted(glob.glob(os.path.join(d, "sen0401_ch%02d_document_v*.ttl" % n)), key=vk)[-1]
    a, b, c = vk(src); old = "%d.%d.%d" % (a, b, c); new = "%d.%d.%d" % (a, b, c + 1)
    dst = os.path.join(d, "sen0401_ch%02d_document_v%d_%d_%d.ttl" % (n, a, b, c + 1))
    if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
    t = open(src, encoding="utf-8").read()
    for sid, sent in ADD[n].items():
        i = t.index("chx:%s a doc:" % sid); j = t.index('skos:definition "', i) + len('skos:definition "')
        k = j
        while not (t[k] == '"' and t[k-1] != "\\"): k += 1
        assert k - i < 20000
        t = t[:k] + sent + t[k:]
    assert t.count('owl:versionInfo "%s"' % old) == 1
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new)
    a1 = 'owl:versionIRI <http://example.org/sen0401/ch%02d/document/%s> ; rdfs:comment "' % (n, old)
    assert t.count(a1) == 1
    t = t.replace(a1, 'owl:versionIRI <http://example.org/sen0401/ch%02d/document/%s> ; rdfs:comment "%s is a PATCH of %s: it appends to %d section definition(s) one sentence that cites, as (Author, Year), sources the chapter research file already holds, so that RDODI Stage 3.F reads a citation there; no concept and no other text changes. Note of %s: ' % (n, new, new, old, len(ADD[n]), old))
    t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-19"', t, count=1); assert k == 1
    t, k = re.subn(r'dcterms:identifier "sen0401_ch%02d_document_v[0-9_]+"' % n, 'dcterms:identifier "sen0401_ch%02d_document_v%d_%d_%d"' % (n, a, b, c + 1), t, count=1); assert k == 1
    t = re.sub(r'prov:wasRevisionOf <[^>]*>', 'prov:wasRevisionOf <http://example.org/sen0401/ch%02d/document/%s>' % (n, old), t, count=1)
    open(dst, "w", encoding="utf-8").write(t)
    print("wrote", os.path.relpath(dst, ROOT))
