#!/usr/bin/env python3
"""sen0401_research_cite_fix_ch34 v1.0.0 - repairs the real defects the research verify scripts of chapters 3 and 4 found (2026-10-19).
Chapter 3: publication P85 (JSON-RPC 2.0 Specification) is verified and used by the chapter (the JSON-RPC interface section quotes it), but its citation
'(JSON-RPC Working Group, 2013)' is not read by the verify script's citation pattern (the hyphen in JSON-RPC), and no finding cited P85. A finding F15 now records what
the chapter takes from it, each statement being one an executed claim of the corpus re-reads from the saved copy of the specification or of Bitcoin Core's
doc/JSON-RPC-interface.md (P25). -> research v1.3.0 (MINOR, additive).
Chapter 4: publication P17 (BIP 142) is verified and was read (the corpus's checks compare the book's sentence about BIP142 with the saved BIP), but nothing cited it. A finding F15 now
records the road the book mentions and BIP 173 replaced. The label of P17 named the wrong author: the saved BIP's preamble says Authors: Johnson Lau, so the label reads
(Lau, 2015). -> research v1.3.0 (MINOR).
Never overwrites; reads the newest research file of each chapter and writes the next version."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]

F3 = ('chx:F15 a sen0401:Finding ; rdfs:label "Comparative analysis"@en ; sen0401:findingText "The chapter calls the node through JSON-RPC, and the protocol has two versions that the chapter\'s example and the current release treat differently. '
      'The book\'s example request body declares the older version, with the member jsonrpc set to 1.0, the identifier curltest and the method getblockchaininfo; the JSON-RPC 2.0 specification, which describes the protocol as a stateless, light-weight remote procedure call protocol that is transport agnostic, '
      'requires that member to be exactly 2.0, defines a notification as a request without an id member, and requires the server to reply with the same id value that the request carried. Bitcoin Core\'s own documentation says that the server recognizes version 2.0 requests and responds accordingly and that otherwise the legacy version 1.1 '
      'protocol is followed, the only one available in release 27.0 and before. A student who copies the book\'s request therefore gets the legacy behaviour from release 31.1, and one who declares 2.0 gets the behaviour of the specification. '
      'Each of these statements is re-read from the saved copy of the specification or of the documentation by an executed claim, and the book\'s request body is rebuilt in Python and its method read back." ; sen0401:cites chx:P01, chx:P25, chx:P85 .\n')
F4 = ('chx:F15 a sen0401:Finding ; rdfs:label "Contemporary developments"@en ; sen0401:findingText "The chapter\'s account of why bech32 exists leaves out the first proposal, which the book names: at first, Bitcoin developers proposed BIP142, which would continue using base58check with a new version byte, similar to the P2SH upgrade. '
      'The saved copy of BIP 142, titled Address Format for Segregated Witness, defines such an address, a base58check string whose payload is a version byte, a witness-program version, a zero byte and the 20-byte or 32-byte hash, and its preamble gives the status Closed. '
      'BIP 173, the bech32 proposal, states that it replaces BIP142, and gives as the reasons for the change the weaknesses of base58 that the chapter lists: the space it needs in QR codes, its mixed case, and a checksum with no error-detection guarantee. '
      'The book sentence and the title of the BIP are compared by executed claims of the corpus; the status and the replacement statement were read from the saved copies of the two BIPs on 2026-10-19." ; sen0401:cites chx:P01, chx:P17, chx:P18 .\n')
JOBS = {3: (F3, "1.3.0", "the finding F15, which cites the JSON-RPC 2.0 specification (P85) for the version differences between the book's request and the current release, so that the verified source is cited"),
        4: (F4, "1.3.0", "the finding F15, which cites BIP 142 (P17) for the first address proposal that BIP 173 replaced, and the label of P17, which named the wrong author, now reads (Lau, 2015) as the saved BIP's preamble says")}

for n, (fnd, new, what) in JOBS.items():
    d = os.path.join(ROOT, "03-materials", "ch%02d" % n, "rdodi")
    src = sorted(glob.glob(os.path.join(d, "sen0401_ch%02d_research_v*.ttl" % n)), key=vk)[-1]
    old = ".".join(map(str, vk(src))); assert old == "1.2.0", old
    dst = os.path.join(d, "sen0401_ch%02d_research_v%s.ttl" % (n, new.replace(".", "_")))
    if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
    t = open(src, encoding="utf-8").read()
    assert "chx:F15 " not in t
    i = t.index("chx:Scorecard a "); t = t[:i] + fnd + t[i:]
    if n == 4:
        a = 'rdfs:label "BIP 142 (Wuille, 2015), bitcoin/bips,'; assert t.count(a) == 1
        t = t.replace(a, 'rdfs:label "BIP 142 (Lau, 2015), bitcoin/bips,')
    assert t.count('owl:versionInfo "%s"' % old) == 1
    t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % new)
    t = t.replace('owl:versionIRI <http://example.org/sen0401/ch%02d/research/%s>' % (n, old), 'owl:versionIRI <http://example.org/sen0401/ch%02d/research/%s>' % (n, new))
    a = 'rdfs:comment "'; j = t.index(a, t.index("owl:versionIRI")); t = t[:j + len(a)] + "%s is MINOR over %s, additive: %s. Note of %s: " % (new, old, what, old) + t[j + len(a):]
    t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-19"', t, count=1); assert k == 1
    t, k = re.subn(r'dcterms:identifier "sen0401_ch%02d_research_v[0-9_]+"' % n, 'dcterms:identifier "sen0401_ch%02d_research_v%s"' % (n, new.replace(".", "_")), t, count=1); assert k == 1
    t, k = re.subn(r'owl:priorVersion <[^>]*>', 'owl:priorVersion <http://example.org/sen0401/ch%02d/research/%s>' % (n, old), t, count=1); assert k == 1
    t, k = re.subn(r'prov:wasRevisionOf <[^>]*>', 'prov:wasRevisionOf <http://example.org/sen0401/ch%02d/research/%s>' % (n, old), t, count=1); assert k == 1
    open(dst, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst, ROOT))
