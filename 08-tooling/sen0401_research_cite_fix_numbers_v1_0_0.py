#!/usr/bin/env python3
"""sen0401_research_cite_fix_numbers v1.0.0 - repairs the 19 dangling Stage3.F citations of the 'numbers' Stage 3 document (2026-10-20).
Finding (checked first, not assumed): every section cites '(Blockchain.com, 2026)'; the research file DOES hold the sources (P02 market price, P03 bitcoins in circulation, P04 hash rate, the
Blockchain.com charts API, verified 2026-09-25) but their labels carry no year, so the gate's resolver (a name and the year in the label) found nothing. The year 2026 is the year the records were read.
Verification repeated on 2026-10-20 and saved in 08-tooling/numbers-evidence (SHA-256 in sources_record_v1_0_0.json): the three endpoints answer HTTP 200 with the named series, the market price of
2026-08-26 is 78521.7 USD and the daily hash rate of 2026-08-28 is 825.5 EH/s, exactly the values research finding F2 states. No source is added and none invented.
Reads the newest numbers research file and writes the next version (1.1.0, MINOR: the labels of P02-P04 carry the author-year string; a saved copy and HTTP status are recorded). Never overwrites."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "03-materials", "numbers", "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
src = sorted(glob.glob(os.path.join(d, "sen0401_numbers_research_v*.ttl")), key=vk)[-1]
old = ".".join(map(str, vk(src))); assert old == "1.0.0", old
NEW = "1.1.0"
SAVED = {"P02": "08-tooling/numbers-evidence/blockchain_market-price_all_sampled_2026-10-20.json",
         "P03": "08-tooling/numbers-evidence/blockchain_total-bitcoins_all_sampled_2026-10-20.json",
         "P04": "08-tooling/numbers-evidence/blockchain_hash-rate_all_sampled_2026-10-20.json; 08-tooling/numbers-evidence/blockchain_hash-rate_90days_daily_2026-10-20.json"}
t = open(src, encoding="utf-8").read()
for p, f in SAVED.items():
    m = re.search(r'(chx:%s a res:Publication ; rdfs:label ")([^"]*)("@en)' % p, t); assert m, p
    t = t[:m.start()] + m.group(1) + m.group(2) + " (Blockchain.com, 2026)" + m.group(3) + t[m.end():]
    k = t.index("chx:%s a res:Publication" % p); e = t.index("res:hasVerificationStatus", k)
    t = t[:e] + 'sen0414:httpStatus 200 ; sen0414:savedCopy "%s (sha256 in 08-tooling/numbers-evidence/sources_record_v1_0_0.json)" ; ' % f + t[e:]
assert t.count('owl:versionInfo "%s"' % old) == 1
t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % NEW)
t = t.replace('owl:versionIRI <http://example.org/sen0401/numbers/research/%s>' % old, 'owl:versionIRI <http://example.org/sen0401/numbers/research/%s> ;\n    rdfs:comment "%s is MINOR over %s: the labels of the three Blockchain.com chart publications P02-P04 now carry the author-year string (Blockchain.com, 2026) that the Stage 3 document cites, because the Stage3.F resolver reads a citation by a name and a year in the label and found none for 19 sections; each source is saved with its SHA-256 (re-fetched and compared with finding F2 on 2026-10-20); no publication is added or removed."@en ;\n    owl:priorVersion <http://example.org/sen0401/numbers/research/%s> ;\n    prov:wasRevisionOf <http://example.org/sen0401/numbers/research/%s>' % (NEW, NEW, old, old, old))
t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-20"', t, count=1); assert k == 1
t, k = re.subn(r'dcterms:identifier "sen0401_numbers_research_v[0-9_]+"', 'dcterms:identifier "sen0401_numbers_research_v%s"' % NEW.replace(".", "_"), t, count=1); assert k == 1
dst = os.path.join(d, "sen0401_numbers_research_v%s.ttl" % NEW.replace(".", "_"))
if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
open(dst, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst, ROOT))
