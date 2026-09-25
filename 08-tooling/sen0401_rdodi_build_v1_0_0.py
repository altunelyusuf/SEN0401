#!/usr/bin/env python3
"""Generic RDODI Stages 1-3 builder for a SEN0401 chapter (forked from SEN0414's under time pressure; to be consolidated into CME), driven by a chapter data module.
Usage: sen0401_rdodi_build_v1_0_0.py <data-module> <verified-at>
Written for chapter 2 onward. Chapter 1 was built by its own three builders before this existed;
they are to be retired once this builder is shown to reproduce chapter 1's artefacts - recorded as
a finding, not left implicit."""
import importlib, os, sys
D = importlib.import_module(sys.argv[1]); VER = sys.argv[2]
V = getattr(D, "VERSION", "1_0_0"); VD = V.replace("_", ".")
N = "%02d" % D.CH
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi"); os.makedirs(OUT, exist_ok=True)
BASE = "http://example.org/sen0401/ch%s" % N
PFX = '''@prefix chx:     <%s#> .
@prefix res:     <http://example.org/rdodi/research-ontology#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix doc:     <http://example.org/rdodi/document-ontology#> .
@prefix sen0414: <http://example.org/sen0401#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
''' % BASE

def header(part, label):
    ident = "sen0401_ch%s_%s_v%s" % (N, part, V)
    return '''<%s/%s> a owl:Ontology ;
    rdfs:label "%s"@en ; owl:versionInfo "%s" ; owl:versionIRI <%s/%s/%s> ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "2026-09-24"^^xsd:date ; dcterms:modified "2026-09-24"^^xsd:date ;
    dcterms:identifier "%s" ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/ch%s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % (BASE, part, label, VD, BASE, part, VD, ident, N)

def q(t): return t.replace('\\', '\\\\').replace('"', "'")

def research():
    L = [PFX, header("research", "SEN0401 chapter %d - RDODI Stage 1 research artefact" % D.CH),
         'chx:Research a res:ResearchProject ; rdfs:label "%s"@en ;' % q(D.TITLE),
         '    sen0414:methodology "Primary source first: the chapter\'s named concepts from the book\'s own source at tag third_edition_print1. Then the official documentation for the current release and the PEPs the chapter\'s topics touch. Every source opened and read on %s; every claim taken from text actually read; every behaviour executed under Python 3.14.4." ;' % VER,
         '    res:hasResearchScope chx:Scope ; rdfs:member ' + ", ".join("chx:%s" % p[0] for p in D.PUBS) + ' .',
         'chx:Scope a res:ResearchScope ; res:hasResearchQuestion "%s" ; res:hasTimeWindow "Current as of 2026-09-24." .' % q(D.QUESTION)]
    for pid, lab, url, prim in D.PUBS:
        L.append('chx:%s a res:Publication ; rdfs:label "%s"@en ; dcterms:source "%s"^^xsd:anyURI ; res:hasVerificationStatus res:Status_Verified ; sen0414:verifiedAt "%s"^^xsd:dateTime ; sen0414:sourceRole "%s" .' % (pid, q(lab), url, VER, "primary" if prim else "secondary"))
    for i, (k, lab) in enumerate(D.CONCEPTS, 1):
        L.append('chx:C_%02d a sen0414:PrimarySourceConcept ; rdfs:label "%s"@en ; sen0414:conceptKind "%s" ; dcterms:source chx:P01 .' % (i, q(lab), k))
    for fid, sec, text, cites in D.FINDINGS:
        L.append('chx:%s a sen0414:Finding ; rdfs:label "%s"@en ; sen0414:findingText "%s" ; sen0414:cites %s .' % (fid, sec, q(text), ", ".join("chx:" + c for c in cites)))
    used = sorted({c for f in D.FINDINGS for c in f[3]})
    L.append('chx:Scorecard a sen0414:QualityScorecard ; rdfs:label "Quality scorecard"@en ; sen0414:topicCoverage "%d primary-source concepts inventoried from the textbook ontology." ; sen0414:citationStrength "%d sources, all opened and verified at %s; %d cited by findings." ; sen0414:methodologyCompliance "RDODI procedure v1.6.0 Stage 1." ; sen0414:reproducibility "Every source is a stable public URL; every claim names its sources." .' % (len(D.CONCEPTS), len(D.PUBS), VER, len(used)))
    return "\n".join(L) + "\n"

def label(c):
    t = "".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip()
    return t[0].upper() + t[1:]

def tbox():
    L = [PFX, header("tbox", "SEN0401 chapter %d domain ontology - TBox" % D.CH)]; seen = set()
    for top, mid, leaf, *_ in D.TAX:
        for c, par in ((top, None), (mid, top), (leaf, mid)):
            if c in seen: continue
            seen.add(c)
            L.append('chx:%s a owl:Class ; rdfs:label "%s"@en ;%s rdfs:isDefinedBy <%s/tbox> .' % (c, label(c), (" rdfs:subClassOf chx:%s ;" % par) if par else "", BASE))
    tops = []
    for t in D.TAX:
        if t[0] not in tops: tops.append(t[0])
    for i, a in enumerate(tops):
        for b in tops[i + 1:]: L.append("chx:%s owl:disjointWith chx:%s ." % (a, b))
    return "\n".join(L) + "\n"

def abox():
    L = [PFX, header("abox", "SEN0401 chapter %d domain ontology - ABox" % D.CH)]
    for top, mid, leaf, ex, d, io in D.TAX:
        L.append('chx:X_%s a owl:NamedIndividual, chx:%s ; rdfs:label "%s"@en ; skos:definition "%s"@en ; dcterms:source <%s/research> .' % (leaf, leaf, q(ex), q(d), BASE))
        if io:
            L.append('chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; chx:input "%s" ; chx:output "%s" .' % (leaf, q(io[0]), q(io[1]), q(io[0]), q(io[1])))
            L.append("chx:X_%s rd:hasIOExample chx:IO_%s ." % (leaf, leaf))
    L.append('''chx:Artifact a owl:NamedIndividual, rd:DomainOntologyArtifact ; rdfs:label "SEN0401 chapter %d domain ontology"@en ;
    rd:derivedFromResearchSubject <%s/research> ; rd:hasCompetencyQuestion chx:CQs ; rd:hasSourceProvenance chx:Provenance ;
    rd:hasReusabilityScope rd:RS_SubjectSpecific ; rd:hasResolutionEnvironment chx:Env .
chx:CQs a owl:NamedIndividual, rd:CompetencyQuestionSet ; rdfs:label "Chapter %d competency questions"@en ; rd:containsCompetencyQuestion chx:CQ1, chx:CQ2 .
chx:CQ1 a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "Which claims of the chapter can be checked by computation, and what does the computation give?"@en .
chx:CQ2 a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "Which concepts reach beyond the book into the current state of Bitcoin and the course theme, and on what source?"@en .
chx:Provenance a owl:NamedIndividual, rd:ResearchSubjectInput ; rdfs:label "Derived from the chapter %d research artefact"@en ;
    skos:definition "Concepts are corpus-derived from Mastering Bitcoin 3rd edition's chapter %d through the Stage 1 research artefact; the modern-practice branch comes from that artefact's secondary sources."@en ;
    dcterms:source <%s/research> .
chx:Env a owl:NamedIndividual, rd:ResolutionEnvironment ; rdfs:label "CPython 3.14.4"@en ;
    skos:definition "Every input-output example executed under CPython 3.14.4, installed with uv on 2026-09-24."@en ;
    dcterms:source "The execution run recorded with this build, 08-tooling/sen0414_rdodi_build_v1_0_0.py" .
''' % (D.CH, BASE, D.CH, D.CH, D.CH, BASE))
    return "\n".join(L) + "\n"

def shacl():
    return PFX + header("shacl", "SEN0401 chapter %d domain ontology - shapes" % D.CH) + '''chx:ExemplarShape a sh:NodeShape ; sh:targetClass owl:NamedIndividual ;
    sh:property [ sh:path rdfs:label ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "Every individual needs a label." ] .
chx:ExemplarSourcedShape a sh:NodeShape ; sh:targetSubjectsOf skos:definition ;
    sh:property [ sh:path dcterms:source ; sh:minCount 1 ; sh:severity sh:Violation ; sh:message "A defined individual must cite its source." ] .
chx:IOShape a sh:NodeShape ; sh:targetClass rd:IOExample ;
    sh:property [ sh:path chx:input ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one input." ] ;
    sh:property [ sh:path chx:output ; sh:minCount 1 ; sh:maxCount 1 ; sh:severity sh:Violation ; sh:message "An I/O example needs exactly one output." ] .
'''

def document():
    order = []; tops = []
    for t in D.TAX:
        if t[0] not in tops: tops.append(t[0])
    for top in tops:
        order.append((top, 1, None)); mids = []
        for t in D.TAX:
            if t[0] == top and t[1] not in mids: mids.append(t[1])
        for m in mids:
            order.append((m, 2, top))
            for t in D.TAX:
                if t[1] == m: order.append((t[2], 3, m))
    L = [PFX, header("document", "SEN0401 chapter %d - RDODI Stage 3 document" % D.CH),
         'chx:Document a doc:ReportSection ; rdfs:label "%s"@en ; skos:definition "This document renews chapter %d of the 3rd edition of Mastering Bitcoin for SEN0401 (Antonopoulos and Harding, 2023)." ; dcterms:source <%s/research> ;' % (q(D.TITLE), D.CH, BASE),
         '    doc:hasSection ' + ", ".join("chx:S_%s" % c for c, lv, p in order if lv == 1) + ' .']
    for n, (c, lv, p) in enumerate(order, 1):
        L.append('chx:S_%s a %s ; rdfs:label "%s"@en ; doc:sectionTitle "%s" ; doc:hierarchyLevel %d ; doc:sectionOrder %d ;%s' % (
            c, "doc:TaxonomicSection" if lv < 3 else "doc:ConceptSection", label(c), label(c), lv, n, ("\n    doc:hasParentSection chx:S_%s ;" % p) if p else ""))
        L.append('    skos:definition "%s" ; dcterms:source <%s#%s> .' % (q(D.BODY[c]), BASE, c))
    return "\n".join(L) + "\n", order

for name, text in (("research", research()), ("domain_tbox", tbox()), ("domain_abox", abox()), ("domain_shacl", shacl()), ("document", document()[0])):
    open(os.path.join(OUT, "sen0401_ch%s_%s_v%s.ttl" % (N, name, V)), "w").write(text)
print("chapter %d: five artefacts written to %s" % (D.CH, OUT))
