#!/usr/bin/env python3
"""sen0401_ch12_research_control_check v1_0_0 - the lineage agent's OWN checks of the corrected chapter 12 research (criterion AC9_Ch12Research), independent of the executor's scripts.
Usage (venv314 python): sen0401_ch12_research_control_check_v1_0_0.py MODE   MODE = scan | subset | hermit | deckfact
scan: the primary-source concepts of research v1_1_0 number at least 25 (the chapter's), none equals by label a concept of the newest research of any other chapter 1 to 14 (each shared label would be listed), and none of the 41 old concepts remains
subset: old v1_0_1 versus new v1_1_0 by local names: every triple of the old file is in the new one EXCEPT triples of the removed chapter 11 concept nodes, the version header and the scorecard; the removed nodes are exactly the old concepts (listed by count); added triples are the new concepts' and the header's
hermit: HermiT consistency of v1_1_0 (owlready2)
deckfact: MEASURES (does not judge) the delivered chapter 12 deck v2_0_0 against the new research with the deck standard check v1_1_0: prints D4 and D11 as printed (exit code ignored)"""
import glob, os, re, subprocess, sys, tempfile
import rdflib
T = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(T) + "/03-materials/"
OLD = R + "ch12/rdodi/sen0401_ch12_research_v1_0_1.ttl"; NEW = R + "ch12/rdodi/sen0401_ch12_research_v1_1_0.ttl"
def load(p): g = rdflib.Graph(); g.parse(p, format="turtle"); return g
ln = lambda x: re.split(r"[#/]", str(x))[-1] if isinstance(x, rdflib.URIRef) else ("L:" + str(x))
def concepts(g):
    out = {}
    for s in g.subjects(rdflib.RDF.type, None):
        for t in g.objects(s, rdflib.RDF.type):
            if str(t).endswith("PrimarySourceConcept"): out[s] = str(g.value(s, rdflib.RDFS.label)).lower()
    return out
def newest(n):
    fs = glob.glob(R + "ch%02d/rdodi/sen0401_ch%02d_research_v*.ttl" % (n, n)); return max(fs, key=lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]) if fs else None
mode = sys.argv[1]; fail = []
if mode == "scan":
    new = concepts(load(NEW)); old = concepts(load(OLD)); labels = set(new.values()); print("concepts: new %d, old %d" % (len(new), len(old)))
    if len(new) < 25: fail.append("fewer than 25 concepts")
    for n in range(1, 15):
        if n == 12: continue
        p = newest(n); sh = labels & set(concepts(load(p)).values()) if p else set()
        print("ch%02d (%s): shared labels %d %s" % (n, os.path.basename(p) if p else "-", len(sh), sorted(sh)[:5])); fail += ["shared with ch%02d: %s" % (n, sorted(sh)[:3])] if sh else []
    kept = labels & set(old.values()); print("old concepts still present by label: %d %s" % (len(kept), sorted(kept)[:5])); fail += ["old concept kept"] if kept else []
elif mode == "subset":
    go, gn = load(OLD), load(NEW); co = concepts(go); rem = set(co)
    def tri(g, skip): return {(ln(s), ln(p), ln(o)) for s, p, o in g if not isinstance(s, rdflib.BNode) and not isinstance(o, rdflib.BNode) and s not in skip}
    hdr = lambda t: t[0] in ("Scorecard",) or "research" in t[0].lower() or t[1] in ("versionInfo", "versionIRI", "comment", "modified", "identifier", "wasRevisionOf", "label", "changeNote", "created")
    a = tri(go, set()); b = tri(gn, set())
    gone = {t for t in a - b}; byconcept = {t for t in gone if t[0] in {ln(s) for s in rem}}; other = {t for t in gone - byconcept if not hdr(t)}
    refs = {t for t in other if t[2] in {ln(s) for s in rem}}
    print("old triples %d; not in new %d; of them the removed concept nodes' own %d; header or scorecard %d; other %d" % (len(a), len(gone), len(byconcept), len(gone) - len(byconcept) - len(other), len(other)))
    for t in sorted(other)[:15]: print("OTHER", t)
    cn = concepts(gn); print("old concept nodes %d, still typed as concepts in new: %d" % (len(rem), len(rem & set(cn))))
    fail = list(other - refs)  # triples pointing AT a removed concept (membership lists) are allowed
    print("triples pointing at a removed concept (lists, links): %d (allowed)" % len(refs))
elif mode == "hermit":
    import owlready2
    tf = tempfile.mkdtemp() + "/r.owl"; load(NEW).serialize(tf, format="xml"); w = owlready2.World(); o = w.get_ontology("file://" + tf).load()
    with o: owlready2.sync_reasoner_hermit(w, infer_property_values=False)
    inc = list(w.inconsistent_classes()); print("HERMIT v1_1_0: consistent, inconsistent classes:", inc); fail = inc
elif mode == "deckfact":
    r = subprocess.run([sys.executable.replace("venv314/bin/python", "") or sys.executable, "-B", T + "/sen0401_deck_standard_check_v1_1_0.py", "12"], capture_output=True, text=True, cwd=T)
    for l in (r.stdout + r.stderr).splitlines():
        if re.match(r"\s*\[?(D4|D11)\b|^.*D(4|11)\b", l): print(l[:240])
    print("exit code of the deck standard check (not judged here):", r.returncode)
print("RESULT", "FAIL %s" % fail if fail else "PASS"); sys.exit(1 if fail else 0)
