#!/usr/bin/env python3
"""sen0401_research_cite_fix_ch8 v1.0.0 - repairs the 45 dangling Stage3.F citations of the chapter 8 Stage 3 document (2026-10-19).
Finding: every cited source IS in the research file (66 publications, all saved in 08-tooling/ch08-evidence with SHA-256 in sources_record_v1_0_0.json); no source is missing and none is invented.
The labels of 25 publications did not carry the author-year string ('Wuille et al., 2020') that the document cites and that sen0401_ch08_sources_v1_0_0.py holds as their 'cite' field, so the
gate's resolver (name in the label and year in the label) found nothing. Each addition below is checked against the saved copy before it is written:
  BIP 340/341/342 'Assigned: 2020-01-19', authors Wuille, Nick, Ruffing / Towns; BIP 327 'Assigned: 2022-03-22' (Nick, Ruffing, Jin); BIP 143 2016-01-03 and BIP 146 2016-08-16 (Lau, Wuille);
  BIP 118 2017-02-28 (Decker, Towns); BIP 32 2012-02-11 (Wuille); BIP 174 2017-07-12 (Chow); BIP 373 and BIP 390 2024-06-04 (Chow); BIP 54 2025-04-11 (Poinsot, Corallo); BIP 461 2026-08-12 (Gilligan);
  SEC 2 dated January 27, 2010, issued by the Standards for Efficient Cryptography Group; Schnorr, CRYPTO '89, LNCS 435 '(c) 1990 Springer-Verlag'; FROST 'First Online 21 July 2021';
  US patent 4,995,082 publication date 1991-02-19 (USPTO); Fiat and Shamir: CRYPTO 1986, the Springer proceedings volume is dated 1987 (the label now says both, the document's 1986 is the conference year);
  Cornell 35 USC 154, Lightning BOLT 3 and the two mempool.space records: web records read on 2026-10-15 (fetched time in sources_record), year 2026.
Reads the newest research file and writes the next version (1.1.0, MINOR: labels only, no publication added or removed). Never overwrites."""
__version__ = "1.0.0"
import glob, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = os.path.join(ROOT, "03-materials", "ch08", "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]
src = sorted(glob.glob(os.path.join(d, "sen0401_ch08_research_v*.ttl")), key=vk)[-1]
old = ".".join(map(str, vk(src))); assert old == "1.0.0", old
NEW = "1.1.0"
ADD = {"P03": "(Wuille et al., 2020)", "P04": "(Wuille et al., 2020)", "P05": "(Wuille et al., 2020)", "P06": "(Wuille et al., 2020)", "P07": "(Nick et al., 2022)",
       "P09": "(Lau and Wuille, 2016)", "P10": "(Lau and Wuille, 2016)", "P11": "(Decker and Towns, 2017)", "P12": "(Wuille, 2012)", "P13": "(Chow, 2017)", "P14": "(Chow, 2024)",
       "P15": "(Poinsot and Corallo, 2025)", "P16": "(Gilligan, 2026)", "P18": "(Chow, 2024)", "P36": "(SECG, 2010)", "P38": "(Schnorr, 1990)",
       "P39": "(Fiat and Shamir, 1986; CRYPTO 1986, proceedings volume dated 1987)", "P44": "(Komlo and Goldberg, 2021)", "P47": "(USPTO, 1991)",
       "P48": "(Cornell Legal Information Institute, 2026)", "P61": "(Lightning BOLTs, 2026)", "P65": "(Mempool Space, 2026)", "P66": "(Mempool Space, 2026)"}
t = open(src, encoding="utf-8").read()
for p, a in ADD.items():
    m = re.search(r'(chx:%s a res:Publication ; rdfs:label ")([^"]*)("@en)' % p, t); assert m, p
    assert a.split(";")[0].strip("(") .split(",")[0] not in ("",)
    t = t[:m.start()] + m.group(1) + m.group(2) + " " + a + m.group(3) + t[m.end():]
assert t.count('owl:versionInfo "%s"' % old) == 1
t = t.replace('owl:versionInfo "%s"' % old, 'owl:versionInfo "%s"' % NEW)
t = t.replace('owl:versionIRI <http://example.org/sen0401/ch08/research/%s>' % old, 'owl:versionIRI <http://example.org/sen0401/ch08/research/%s> ;\n    rdfs:comment "%s is MINOR over %s, labels only: the labels of %d publications now carry the author-year string that the Stage 3 document cites (each checked against the saved copy in ch08-evidence), because the Stage3.F resolver reads a citation by a name and a year in the label and found none for 45 sections; no publication is added or removed and every source was already held and verified."@en ;\n    owl:priorVersion <http://example.org/sen0401/ch08/research/%s> ;\n    prov:wasRevisionOf <http://example.org/sen0401/ch08/research/%s>' % (NEW, NEW, old, len(ADD), old, old))
t, k = re.subn(r'dcterms:modified "[^"]*"', 'dcterms:modified "2026-10-19"', t, count=1); assert k == 1
t, k = re.subn(r'dcterms:identifier "sen0401_ch08_research_v[0-9_]+"', 'dcterms:identifier "sen0401_ch08_research_v%s"' % NEW.replace(".", "_"), t, count=1); assert k == 1
dst = os.path.join(d, "sen0401_ch08_research_v%s.ttl" % NEW.replace(".", "_"))
if os.path.exists(dst): sys.exit("REFUSED: exists " + dst)
open(dst, "w", encoding="utf-8").write(t); print("wrote", os.path.relpath(dst, ROOT))
