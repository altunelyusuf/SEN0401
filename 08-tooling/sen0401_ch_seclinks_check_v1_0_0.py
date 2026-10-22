#!/usr/bin/env python3
"""sen0401_ch_seclinks_check v1_0_0: do the newest domain TBox and ABox of a chapter state how its sections relate, as links (ruling G134)?
Usage: sen0401_ch_seclinks_check_v1_0_0.py NN [--evidence]     (NN = chapter number; --evidence also requires the annotation of each link with the sentence that states it)
A section is a second-level class of the chapter's taxonomy (the document's sections of hierarchy level 2); the example (X_ individual) of a third-level class belongs to the section above it.
Checks, each printed as PASS or FAIL:
  1 declared      every property that carries kb:hasRelationshipCategory is an owl:ObjectProperty with rdfs:label, rdfs:domain, rdfs:range, and its category is an individual of the OEE governance ABox
  2 links         every ABox triple X_ p X_ with such a property joins two different sections
  3 covered       every section is an end of at least one link (a section that is not is named)
  4 annotated     (with --evidence) every link carries an owl:Axiom annotation with rdfs:comment
  5 one type      (informational) the number of link types between the same two sections
Exit 0 only when 1 to 3 (and 4 with --evidence) hold."""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib
from rdflib import RDF, RDFS, OWL, Namespace

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = Namespace("http://example.org/knowledge-base#"); DOC = Namespace("http://example.org/rdodi/document-ontology#"); DC = Namespace("http://purl.org/dc/terms/")
OEE = os.environ.get("OEE_ROOT", "/home/claude/Ontologies")
vkey = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]


def newest(pattern):
    fs = glob.glob(pattern)
    return sorted(fs, key=vkey)[-1] if fs else None


def main(argv):
    if not argv or not argv[0].isdigit():
        print(__doc__); return 2
    n = int(argv[0]); evidence = "--evidence" in argv
    rd = os.path.join(REPO, "03-materials", "ch%02d" % n, "rdodi")
    part = lambda p: newest(os.path.join(rd, "sen0401_ch%02d_%s_v*.ttl" % (n, p)))
    tb, ab, dc = part("domain_tbox"), part("domain_abox"), part("document")
    gov = newest(os.path.join(OEE, "oe-method", "09-governance", "oegov_abox_v*.ttl"))
    print("files:", os.path.basename(tb), os.path.basename(ab), os.path.basename(dc), "| categories from", os.path.basename(gov))
    T = rdflib.Graph(); T.parse(tb); A = rdflib.Graph(); A.parse(ab); D = rdflib.Graph(); D.parse(dc); G = rdflib.Graph(); G.parse(gov)
    ok = True
    # sections: level-2 classes; the class of a leaf -> its section
    lvl = {}; parent = {}
    for s in D.subjects(DOC.sectionTitle, None):
        c = D.value(s, DC.source); lvl[c] = int(D.value(s, DOC.hierarchyLevel))
    for c in lvl: parent[c] = T.value(c, RDFS.subClassOf)
    sections = [c for c in lvl if lvl[c] == 2]
    sec_of = lambda cls: cls if lvl.get(cls) == 2 else (parent.get(cls) if lvl.get(cls) == 3 else None)
    ind_sec = {}
    for x in A.subjects(RDF.type, OWL.NamedIndividual):
        if "#X_" not in str(x): continue
        for c in A.objects(x, RDF.type):
            if c in lvl: ind_sec[x] = sec_of(c)
    print("sections (second-level classes): %d; examples mapped to a section: %d" % (len(sections), len(ind_sec)))
    # 1 declared
    props = sorted(set(T.subjects(KB.hasRelationshipCategory, None)), key=str)
    bad = []
    for p in props:
        cat = T.value(p, KB.hasRelationshipCategory)
        miss = [nm for nm, v in (("object property", (p, RDF.type, OWL.ObjectProperty) in T), ("label", T.value(p, RDFS.label)), ("domain", T.value(p, RDFS.domain)), ("range", T.value(p, RDFS.range)),
                                 ("category in the OEE governance ABox", (cat, RDF.type, KB.RelationshipCategory) in G)) if not v]
        if miss: bad.append((str(p).split("#")[-1], miss))
    print("%s 1 declared: %d properties carry a relationship category%s" % ("PASS" if props and not bad else "FAIL", len(props), "" if not bad else "; incomplete: %s" % bad))
    ok &= bool(props) and not bad
    # 2 links
    links = []; same = []
    for p in props:
        for a, b in A.subject_objects(p):
            if a in ind_sec and b in ind_sec:
                (same if ind_sec[a] == ind_sec[b] else links).append((a, p, b))
            else:
                same.append((a, p, b))
    print("%s 2 links: %d links join two different sections; %d do not (same section or an end that is not an example)" % ("PASS" if links and not same else "FAIL", len(links), len(same)))
    for a, p, b in same: print("      not between two sections:", str(a).split("#")[-1], str(p).split("#")[-1], str(b).split("#")[-1])
    ok &= bool(links) and not same
    # 3 covered
    ends = {}
    for a, p, b in links:
        for x in (a, b): ends.setdefault(ind_sec[x], set()).add((str(p).split("#")[-1]))
    unc = [c for c in sections if c not in ends]
    print("%s 3 covered: %d of %d sections are an end of a link%s" % ("PASS" if not unc else "FAIL", len(sections) - len(unc), len(sections), "" if not unc else "; not related: " + ", ".join(str(c).split("#")[-1] for c in unc)))
    ok &= not unc
    # 4 annotated
    if evidence:
        ann = {(s, p, o) for ax in A.subjects(RDF.type, OWL.Axiom) for s, p, o in [(A.value(ax, OWL.annotatedSource), A.value(ax, OWL.annotatedProperty), A.value(ax, OWL.annotatedTarget))] if A.value(ax, RDFS.comment)}
        miss = [l for l in links if l not in ann]
        print("%s 4 annotated: %d of %d links carry the sentence that states them" % ("PASS" if not miss else "FAIL", len(links) - len(miss), len(links)))
        ok &= not miss
    # 5 one type
    pair = {}
    for a, p, b in links: pair.setdefault(frozenset((ind_sec[a], ind_sec[b])), set()).add(str(p).split("#")[-1])
    multi = {tuple(sorted(str(c).split("#")[-1] for c in k)): sorted(v) for k, v in pair.items() if len(v) > 1}
    print("INFO 5 one type: %d pairs of sections are linked, %d of them by more than one type %s" % (len(pair), len(multi), multi if multi else ""))
    print("by property:", {str(p).split("#")[-1]: sum(1 for l in links if l[1] == p) for p in props})
    print("by section (distinct link types at its ends):", {str(c).split("#")[-1]: len(v) for c, v in sorted(ends.items(), key=lambda kv: str(kv[0]))})
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
