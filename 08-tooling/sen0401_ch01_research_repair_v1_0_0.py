#!/usr/bin/env python3
"""sen0401_ch01_research_repair v1.0.0 - repairs the two structural findings the form of the chapter 2 verify script (sen0401_research_verify_lib_v1_0_0.py) found on the
chapter 1 research (change request CR3_Ch01Research, 2026-10-25): ('publication never cited', 'P23') and ('counts', 30, 7).
The research v1.2.0 stays unchanged; this writes research v1.3.0 (MINOR, additive): one new finding F8, "Identifiers: one syntax for three uses", which cites
P23 (RFC 3986), P16 (BIP 21) and P07 (Decentralized Identifiers v1.0). P23 is cited, not dropped: the chapter document already quotes it in the URI section and the
source checks of the chapter re-read two of its sentences from the saved copy, so the publication is used. The library's citation pattern does not match a
hyphenated name such as (Berners-Lee et al., 2005), which is why only a finding could show the library the citation. Every sentence of F8 is re-read from a saved copy
or computed by sen0401_ch01_verify_v1_1_0.py. The scorecard sentence '15 cited by findings' is updated to the new count.
Never overwrites; reads the newest chapter 1 research file and writes the next minor version."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "03-materials", "ch01", "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
src = sorted(glob.glob(os.path.join(d, "sen0401_ch01_research_v*.ttl")), key=vk)[-1]
old = ".".join(map(str, vk(src))); assert old == "1.2.0", old
new = "1.3.0"
dst = os.path.join(d, "sen0401_ch01_research_v1_3_0.ttl")
if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
t = open(src, encoding="utf-8").read()
FT = ("Reading the identifiers of the chapter against their specifications shows one syntax under three uses. RFC 3986 says that a URI provides a simple and extensible means for identifying a resource, "
      "and gives its generic syntax as URI = scheme \\\":\\\" hier-part [ \\\"?\\\" query ] [ \\\"#\\\" fragment ]. BIP 21 applies that syntax to a payment request: the scheme bitcoin, then an address, then optional parameters, "
      "as in bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=20.3&label=Luke-Jr, which a standard URI parser splits into the scheme bitcoin, the address as the path, and the parameters amount=20.3 and label=Luke-Jr; "
      "the saved copy of BIP 21 states that it has been superseded and replaced with BIP 321, so it is named here as the form the chapter's example follows, not as the current proposal. "
      "The W3C specification of Decentralized Identifiers defines a DID as a URI whose scheme is did: and calls the generic DID scheme a URI scheme conformant with RFC 3986. "
      "A web address, a request for a payment and the name of a subject are therefore written in the same grammar.")
F8 = 'chx:F8 a sen0401:Finding ; rdfs:label "Identifiers: one syntax for three uses"@en ; sen0401:findingText "%s" ; sen0401:cites chx:P07, chx:P16, chx:P23 .\n' % FT
i = t.index("chx:F7 a sen0401:Finding"); j = t.index("\n", i) + 1
t = t[:j] + F8 + t[j:]
assert t.count('owl:versionInfo "1.2.0"') == 1
t = t.replace('owl:versionInfo "1.2.0"', 'owl:versionInfo "1.3.0"')
t = t.replace('owl:versionIRI <http://example.org/sen0401/ch01/research/1.2.0>', 'owl:versionIRI <http://example.org/sen0401/ch01/research/1.3.0>')
a = 'rdfs:comment "'; k = t.index(a, t.index("owl:versionIRI")) + len(a)
t = t[:k] + ("1.3.0 is MINOR over 1.2.0, additive: the finding F8 (identifiers: one syntax for three uses) cites RFC 3986 (P23), BIP 21 (P16) and the W3C Decentralized Identifiers (P07), "
             "so that the publication P23, which the document already quotes in the URI section and the source checks re-read, is cited by a finding, and the findings reach eight; no publication, concept or other finding changes. Note of 1.2.0: ") + t[k:]
t, n = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-25"', t, count=1); assert n == 1
t, n = re.subn(r'dcterms:identifier "sen0401_ch01_research_v1_2_0"', 'dcterms:identifier "sen0401_ch01_research_v1_3_0"', t, count=1); assert n == 1
t, n = re.subn(r'prov:wasRevisionOf <http://example.org/sen0401/ch01/research/1\.1\.0>', 'prov:wasRevisionOf <http://example.org/sen0401/ch01/research/1.2.0>', t, count=1); assert n == 1
assert t.count("15 cited by findings") == 1
t = t.replace("15 cited by findings", "17 cited by findings")
open(dst, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst, ROOT))
