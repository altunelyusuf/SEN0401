#!/usr/bin/env python3
"""The Stage 4 page ABox for a SEN0401 chapter, written from the build record and the browser test
results: a widget is marked designTestPassed only if its test in test_results.json passed."""
import json, os, sys
N = sys.argv[1]; REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rec = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "build_record.json")))
OBJ = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "objectives.json")))
tr = json.load(open(os.path.join(REPO, "08-tooling", "ch%s-page" % N, "test_results.json")))
BASE = "http://example.org/sen0401/ch%s" % N
q = lambda t: t.replace("\\", "\\\\").replace('"', "'")
L = ['''@prefix ipo:     <http://example.org/rdodi/interactive-page-ontology#> .
@prefix wp:      <http://example.org/widget-primitives#> .
@prefix ds:      <http://example.org/rdodi/discourse-selection#> .
@prefix pg:      <%s/page#> .
@prefix sen0401: <http://example.org/sen0401#> .
@prefix ld:      <http://example.org/rdodi/learning-design#> .
@prefix mp:      <http://example.org/rdodi/model-provenance#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .

<%s/page> a owl:Ontology ; rdfs:label "SEN0401 chapter %d - RDODI Stage 4 page ABox"@en ; owl:versionInfo "1.0.0" ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ; dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ; dcterms:created "2026-09-24"^^xsd:date ; dcterms:modified "2026-09-24"^^xsd:date ;
    dcterms:identifier "sen0401_ch%s_page_abox_v1_0_0" ; prov:wasGeneratedBy <http://example.org/sen0401/activity/ch%s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .

pg:Page a ipo:Page, ipo:InteractiveLearningSurface ; rdfs:label "Chapter %d interactive page"@en ;
    dcterms:source <%s/document> ; ipo:hasSourceDocument pg:SourceDocument ;
    ipo:satisfiesHeuristic ipo:RecognitionRatherThanRecall, ipo:ConsistencyAndStandards, ipo:AestheticAndMinimalistDesign,
        ipo:ShneidermanRule_OfferInformativeFeedback, ipo:ShneidermanRule_PermitEasyReversalOfActions, ipo:HelpAndDocumentation ;
    ipo:hasLayoutPattern pg:Layout ; ipo:hasSemanticRegion pg:Header, pg:Sidebar, pg:Main ;
    ipo:includesNavigationPattern pg:GroupedTopBar, pg:SectionTree ;
    ipo:coversLearningObjective %(cos)s ;
    sen0401:navigationRule "BP-D34: %d sections falls in 26-50, so a grouped permanent top bar with a sub-section sidebar; the named single flowing anchor-page variation of procedure v1.6.0 section 5.3." ;
    sen0401:pythonUsed "%s" .
pg:Layout a ipo:SplitLayout ; rdfs:label "Sidebar and main content"@en .
pg:Header a ipo:Header ; rdfs:label "Sticky header with grouped section bar"@en .
pg:Sidebar a ipo:Sidebar ; rdfs:label "Section tree"@en .
pg:Main a ipo:MainContent ; rdfs:label "Chapter content with inline widgets"@en .
pg:GroupedTopBar a ipo:PrimaryNavigation ; rdfs:label "Grouped permanent top bar"@en .
pg:SectionTree a ipo:TreeNavigation ; rdfs:label "Sub-section sidebar tree"@en .
pg:SourceDocument a ipo:SourceDocument ; rdfs:label "Chapter %d Stage 3 document"@en ; dcterms:source <%s/document> ;
    ipo:hasLearningObjective %(cos)s .
''' .replace('%(cos)s', ', '.join('pg:' + k for k in OBJ)) % (BASE, BASE, int(N), N, N, int(N), BASE, len(rec["sections"]), rec["python"], int(N), BASE)]
for k, (text, lvl) in OBJ.items():
    L.append('pg:%s a ipo:LearningObjective, owl:NamedIndividual ; rdfs:label "%s"@en ; ld:bloomLevel ld:%s  .' % (k, q(text), lvl))
for n, it in enumerate(rec['quiz'], 1):
    opts = ', '.join('pg:Q%d_O%d' % (n, j) for j in range(len(it['options'])))
    L.append('pg:Q%d a ld:AssessmentItem, owl:NamedIndividual ; rdfs:label "%s"@en ; ld:hasOption %s ; ld:hasCorrectOption pg:Q%d_O%d ; ld:cognitiveLevel ld:%s ; ld:assessesObjective pg:%s ;' % (n, q(it['q']), opts, n, it['answer'], it['level'], it['objective']))
    L.append('    ' + ' ; '.join('ld:distractorRationale "%s"' % q(r) for r in it['rationales']) + ' .')
    for j, o in enumerate(it['options']): L.append('pg:Q%d_O%d a ld:AnswerOption ; rdfs:label "%s" .' % (n, j, q(o)))
for o, lv, t, sid, s in rec["sections"]:
    L.append('pg:%s a ipo:ChapterSection ; rdfs:label "%s"@en ; dcterms:source <%s> ; sen0401:anchor "#%s" .' % (sid.replace("-", "_"), q(t), s, sid))
    L.append('pg:Page ipo:coversChapterSection pg:%s .' % sid.replace("-", "_"))
for w in rec["widgets"]:
    r = tr["widgets"][w["id"]]; wid = w["id"].replace("-", "_")
    numeric = w["kind"] in ("predict", "toggle")
    L.append('pg:%s a ipo:InstructionalWidget%s ; rdfs:label "%s widget for %s"@en ; ipo:demonstratesSubject <%s> ;' % (wid, ", ipo:CoupledVariableDemonstrator" if numeric else "", w["kind"], w["cls"].split("#")[-1], w["cls"]))
    if numeric:
        L.append('    ipo:enforcesDomainConstraint <%s> ;' % w["cls"])
        L.append('    mp:numericModelStatus mp:Validated ; mp:hasValidationDerivation "Every value the widget reveals was produced by executing the expression under %s at build time, not typed" ; mp:hasConformanceTest "The browser design test requires the revealed value to equal the executed one" ;' % rec["python"])
    L.append('    wp:instantiatesPrimitive wp:%s ; ds:selectionWarrant "%s" ;' % (w["prim"], q(w["warrant"])))
    L.append('    wp:demonstratesConcept <%s> ; dcterms:source <%s> ;' % (w["cls"], w["cls"].replace("#", "/document#S_") if False else "%s/document" % BASE))
    L.append('    wp:hasDesignTest "Exercised in headless Chromium by 08-tooling/sen0401_page_test_v1_0_0.py: %s" ; wp:designTestPassed %s .' % (q(r["detail"]), "true" if r["passed"] else "false"))
open(os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0401_ch%s_page_abox_v1_0_0.ttl" % N), "w").write("\n".join(L) + "\n")
print("page ABox written: %d sections, %d widgets (%d marked tested)" % (len(rec["sections"]), len(rec["widgets"]), sum(1 for w in rec["widgets"] if tr["widgets"][w["id"]]["passed"])))
