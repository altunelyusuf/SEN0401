#!/usr/bin/env python3
"""sen0401_research_cite_fix_ch5 v1.0.0 - repairs the 15 dangling Stage3.F citations of the chapter 5 Stage 3 document (2026-10-21).
Finding (checked first, not assumed): all 15 dangling claims cite '(Lightning Labs, 2026a)' or '(Lightning Labs, 2026b)' (20 and 18 markers). The research file DOES hold the sources: P20 (lnd aezeed README)
and P21 (lnd docs/recovery.md), verified 2026-10-04 and saved in 08-tooling/ch05-evidence. Their labels carry 'Lightning Labs, 2026a/2026b', but the validator v1.13.0 bridge reads a year as a standalone
4-digit token (\\b2026\\b), and '2026a' is not one, so no publication matched. The sources were re-fetched on 2026-10-21: SHA-256 identical to the saved copies. The label now also states the retrieval date
2026-10-04 (verifiedAt of the record), which carries the standalone year. No source added, none invented, the a/b distinction of the document is kept.
Reads the newest chapter 5 research file and writes the next version (1.1.1, PATCH: two labels). Never overwrites."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "03-materials", "ch05", "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
src = sorted(glob.glob(os.path.join(d, "sen0401_ch05_research_v*.ttl")), key=vk)[-1]
old = ".".join(map(str, vk(src))); assert old == "1.1.0", old
NEW = "1.1.1"
t = open(src, encoding="utf-8").read()
for p, y in (("P20", "2026a"), ("P21", "2026b")):
    m = re.search(r'(chx:%s a res:Publication ; rdfs:label ")([^"]*\(Lightning Labs, %s\))("@en)' % (p, y), t); assert m, p
    t = t[:m.start()] + m.group(1) + m.group(2) + ", retrieved 2026-10-04" + m.group(3) + t[m.end():]
assert t.count('owl:versionInfo "%s"' % old) == 1
t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % NEW)
v = 'owl:versionIRI <http://example.org/sen0401/ch05/research/%s>' % old
assert t.count(v) == 1
t = t.replace(v, 'owl:versionIRI <http://example.org/sen0401/ch05/research/%s> ;\n    owl:priorVersion <http://example.org/sen0401/ch05/research/%s> ;\n    prov:wasRevisionOf <http://example.org/sen0401/ch05/research/%s>' % (NEW, old, old))
t = t.replace('rdfs:comment "MINOR over 1.0.0', 'rdfs:comment "%s is PATCH over %s: the labels of the two held lnd publications P20 and P21 now also state the retrieval date 2026-10-04, so the standalone year the Stage3.F resolver reads is present for the 15 claims citing (Lightning Labs, 2026a) and (Lightning Labs, 2026b); both sources were re-fetched on 2026-10-21 and equal the saved copies by SHA-256; no publication is added or removed. Earlier note: MINOR over 1.0.0' % (NEW, old), 1)
t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-21"', t, count=1); assert k == 1, "modified"
t, k = re.subn(r'dcterms:identifier "sen0401_ch05_research_v[0-9_]+"', 'dcterms:identifier "sen0401_ch05_research_v%s"' % NEW.replace(".", "_"), t, count=1); print("identifier replaced:", k)
dst = os.path.join(d, "sen0401_ch05_research_v%s.ttl" % NEW.replace(".", "_"))
if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
open(dst, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst, ROOT))
