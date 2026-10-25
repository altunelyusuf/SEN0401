#!/usr/bin/env python3
"""sen0401_ch01_research_control_check v1_0_0 - the lineage agent's OWN checks of the repaired chapter 1 research set (criterion AC9_Ch01Research), independent of the executor's scripts.
Usage (run under /home/claude/venv314/bin/python): sen0401_ch01_research_control_check_v1_0_0.py MODE   MODE = subset | p23 | count | hermit
subset: every triple of research v1_2_0 is in v1_3_0 except those of the version header and the scorecard (compared by local names); the new file only ADDS (printed counts)
p23: the publication P23 (RFC 3986) is the object of a citation by at least one finding of v1_3_0 and was cited by none in v1_2_0
count: the number of findings of v1_3_0 is at least the library minimum read from sen0401_research_verify_lib_v1_0_0.py; the old count is printed
hermit: HermiT consistency of v1_3_0 (owlready2), printed as consistent or not"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
D = "/home/claude/sen0401/03-materials/ch01/rdodi/"; OLD = D + "sen0401_ch01_research_v1_2_0.ttl"; NEW = D + "sen0401_ch01_research_v1_3_0.ttl"
LIB = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sen0401_research_verify_lib_v1_0_0.py")
def load(p): g = rdflib.Graph(); g.parse(p, format="turtle"); return g
ln = lambda x: re.split(r"[#/]", str(x))[-1] if isinstance(x, rdflib.URIRef) else ("L:" + str(x))
def tri(g): return {(ln(s), ln(p), ln(o)) for s, p, o in g if not isinstance(s, rdflib.BNode) and not isinstance(o, rdflib.BNode)}
def findings(g): return [s for s in g.subjects(rdflib.RDF.type, None) if ln(list(g.objects(s, rdflib.RDF.type))[0]) == "Finding"]
mode = sys.argv[1]; fail = []
if mode == "subset":
    a, b = tri(load(OLD)), tri(load(NEW)); missing = {t for t in a - b if t[0] not in ("Scorecard",) and t[1] not in ("versionInfo", "versionIRI", "comment", "modified", "identifier", "wasRevisionOf", "label", "member", "hasResearchScope") and "research" not in t[0].lower()}
    print("old triples %d, new triples %d, added %d, old triples not in new %d, of them outside the version header and scorecard %d" % (len(a), len(b), len(b - a), len(a - b), len(missing)))
    for t in sorted(missing)[:15]: print("MISSING", t)
    fail = list(missing)
elif mode == "p23":
    def cites(g):
        return sorted({(ln(s), ln(p)) for s, p, o in g if ln(o) == "P23" and ln(p) not in ("member",) and ln(s) not in ("P23",) and not ln(s).startswith("Scorecard")})
    o, n = cites(load(OLD)), cites(load(NEW)); print("P23 referenced in v1_2_0 by:", o); print("P23 referenced in v1_3_0 by:", n); fail = [] if (not o and any(s.startswith("F") for s, _ in n)) else ["P23 not cited by a finding, or cited before"]
elif mode == "count":
    m = re.search(r"(\d+)\s*(?:findings|F)\b|MIN_FINDINGS\s*=\s*(\d+)|findings.*?>=\s*(\d+)", open(LIB).read()); src = [l.strip() for l in open(LIB).read().splitlines() if re.search(r"\b8\b", l) and "find" in l.lower()]
    print("library lines naming 8:", src[:4]); no, nn = len(findings(load(OLD))), len(findings(load(NEW))); print("findings old %d, new %d, library minimum 8" % (no, nn)); fail = [] if nn >= 8 and no < 8 else ["findings count"]
elif mode == "hermit":
    import owlready2
    import tempfile; tf = tempfile.mkdtemp() + "/r.owl"; load(NEW).serialize(tf, format="xml")
    w = owlready2.World(); o = w.get_ontology("file://" + tf).load()
    with o: owlready2.sync_reasoner_hermit(w, infer_property_values=False)
    inc = list(w.inconsistent_classes()); print("HERMIT v1_3_0: consistent, inconsistent classes:", inc); fail = inc
print("RESULT", "FAIL %s" % fail if fail else "PASS"); sys.exit(1 if fail else 0)
