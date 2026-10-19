#!/usr/bin/env python3
"""sen0401_research_cite_fix_ch2 v1.0.0 - repairs the real defects the chapter 2 research verify script (sen0401_ch02_verify_v1_0_0.py) found (2026-10-19).
1. Finding F2 cites chx:P03 (Bitcoin Core releases), which research v1.3.0 does not hold: it existed in v1.1.0 and v1.2.0 and was lost when the files were
   consolidated into the three-file structure. P03 is restored as it was (same label, source, status, verification time, role; only the prefix is the
   proper sen0401: of the same IRI, as in v1.3.0) and is a member of the research project again. -> research v1.4.0 (MINOR, additive).
2. Six sections cite '(Bitcoin Core, 2026)' but no publication carried that label. The six publications P30-P35 are Bitcoin Core files at one pinned commit; each
   now carries the label '(Bitcoin Core, 2026)', which is what the sections name: TransactionSize -> P31 (MAX_BLOCK_WEIGHT, WITNESS_SCALE_FACTOR), TransactionIdentifier and
   Witness (and the root section) -> P32 (txid = hash of the serialization without witness data), Satoshi and ConsensusRules -> P30 (COIN, MAX_MONEY).
   P33 (GetBlockSubsidy), P34 (halving interval) and P35 (generator point and order) are used in the text of BlockReward and EllipticCurve but those paragraphs cited
   only the book; the document gets one added citation in each. -> document v1.3.2 (PATCH, citations only).
Never overwrites; reads the newest file of each part and writes the next version."""
__version__ = "1.0.0"
import glob, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "03-materials", "ch02", "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
newest = lambda part: sorted(glob.glob(os.path.join(d, "sen0401_ch02_%s_v*.ttl" % part)), key=vk)[-1]
P03 = ('chx:P03 a res:Publication ; rdfs:label "Bitcoin Core releases (Bitcoin Core project)"@en ; dcterms:source "https://bitcoincore.org/en/releases/"^^xsd:anyURI ; '
       'res:hasVerificationStatus res:Status_Verified ; sen0401:verifiedAt "2026-09-25T07:51:05"^^xsd:dateTime ; sen0401:sourceRole "secondary" .\n')

def bump(t, kind, old, new, note):
    assert t.count('owl:versionInfo "%s"' % old) == 1
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new)
    t = t.replace('owl:versionIRI <http://example.org/sen0401/ch02/%s/%s>' % (kind, old), 'owl:versionIRI <http://example.org/sen0401/ch02/%s/%s>' % (kind, new))
    a = 'rdfs:comment "'; i = t.index(a, t.index("owl:versionIRI")); t = t[:i + len(a)] + note + " Note of " + old + ": " + t[i + len(a):]
    t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-19"', t, count=1); assert k == 1
    t, k = re.subn(r'dcterms:identifier "sen0401_ch02_%s_v[0-9_]+"' % kind, 'dcterms:identifier "sen0401_ch02_%s_v%s"' % (kind, new.replace(".", "_")), t, count=1); assert k == 1
    t, k = re.subn(r'owl:priorVersion <[^>]*>', 'owl:priorVersion <http://example.org/sen0401/ch02/%s/%s>' % (kind, old), t, count=1)
    t, k = re.subn(r'prov:wasRevisionOf <[^>]*>', 'prov:wasRevisionOf <http://example.org/sen0401/ch02/%s/%s>' % (kind, old), t, count=1); assert k == 1
    return t

# ---- research
src = newest("research"); old = ".".join(map(str, vk(src))); assert old == "1.3.0"
t = open(src, encoding="utf-8").read()
assert "chx:P03 a " not in t
t = t.replace("chx:P02, chx:P21, chx:P22", "chx:P02, chx:P03, chx:P21, chx:P22", 1)
i = t.index("chx:P21 a res:Publication"); t = t[:i] + P03 + t[i:]
for p in ("P30", "P31", "P32", "P33", "P34", "P35"):
    m = re.search(r'(chx:%s a res:Publication ; rdfs:label ")([^"]*)("@en)' % p, t); assert m
    t = t[:m.start()] + m.group(1) + m.group(2) + " (Bitcoin Core, 2026)" + m.group(3) + t[m.end():]
t = bump(t, "research", old, "1.4.0", "1.4.0 is MINOR over 1.3.0, additive: the publication chx:P03 (Bitcoin Core releases), which finding F2 cites and which was lost when the research file was consolidated into the three-file structure, is restored exactly as v1.1.0 and v1.2.0 held it, and is a member of the research project again; and the six Bitcoin Core source publications P30 to P35, all read at one pinned commit, carry the label (Bitcoin Core, 2026) that the document's sections cite.")
dst_r = os.path.join(d, "sen0401_ch02_research_v1_4_0.ttl")
if os.path.exists(dst_r): sys.exit("REFUSED: exists " + dst_r)
open(dst_r, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst_r, ROOT))

# ---- document
src = newest("document"); old = ".".join(map(str, vk(src))); assert old == "1.3.1"
t = open(src, encoding="utf-8").read()
R = [("returning zero once there have been sixty-four of them (Antonopoulos and Harding, 2023).",
      "returning zero once there have been sixty-four of them (Antonopoulos and Harding, 2023) (Bitcoin Core, 2026)."),
     ("since the remainder of y squared minus x cubed minus 7 is 0.",
      "since the remainder of y squared minus x cubed minus 7 is 0; the generator point and the order n are the constants that the libsecp256k1 source inside Bitcoin Core defines (Bitcoin Core, 2026).")]
for a, b in R:
    assert t.count(a) == 1, a; t = t.replace(a, b)
t = bump(t, "document", old, "1.3.2", "1.3.2 is a PATCH of 1.3.1: it adds the citation (Bitcoin Core, 2026) to the two paragraphs whose text rests on Bitcoin Core's source (the block subsidy and halving interval in the block reward, the generator point and the order in the elliptic curve), so that the research publications for those files (P33, P34, P35) are cited by the document; no concept and no other text changes.")
dst_d = os.path.join(d, "sen0401_ch02_document_v1_3_2.ttl")
if os.path.exists(dst_d): sys.exit("REFUSED: exists " + dst_d)
open(dst_d, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst_d, ROOT))
