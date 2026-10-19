#!/usr/bin/env python3
"""The RDODI Stage 4 page ABox of a SEN0401 chapter (version 2), written from the chapter's published page data, its objectives and quiz, and the stored result of the
browser test of the page. Nothing is typed in by hand: every section, widget, objective and question comes from those files, and a widget is marked designTestPassed
only if its entry in the stored test result passed.
Usage: sen0401_page_abox_build_v2_0_0.py NN PAGEVER      (PAGEVER like 9_51_0)
Reads  08-tooling/chNN-page/page_data_vPAGEVER.json, objectives_v*.json, quiz_v*.json, test_results_abox_vPAGEVER.json
Writes 03-materials/chNN/page/sen0401_chNN_page_abox_v2_0_0.ttl
2.0.0 over 1.2.0: a section, a widget and a learning objective each carry a complete sentence of content (skos:definition) and the source it comes from (dcterms:source, the Stage 3 section
or the Stage 3 document), which the Stage 4 rules for coverage and substance (Stage4.cov, Stage4.sub, Stage4.src) measure; the 1.x builder wrote a label only, so those rules failed.
Built with rdflib, so text is escaped by the library."""
__version__ = "2.0.0"
import glob, hashlib, json, os, re, sys
from rdflib import Graph, Literal, Namespace, URIRef, RDF, RDFS, OWL, XSD
from rdflib.namespace import DCTERMS, SKOS, PROV

NUM, PV = sys.argv[1], sys.argv[2]
N = "ch%s" % NUM
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD = os.path.join(REPO, "08-tooling", "%s-page" % N)
vk = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
newest = lambda pat: sorted(glob.glob(pat), key=vk)[-1]
page_data = json.load(open(os.path.join(PD, "page_data_v%s.json" % PV)))
OBJ = json.load(open(newest(os.path.join(PD, "objectives_v*.json"))))
QUIZ = json.load(open(newest(os.path.join(PD, "quiz_v*.json"))))["items"]
TR = json.load(open(os.path.join(PD, "test_results_abox_v%s.json" % PV)))
page_file = os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, PV))
sha = hashlib.sha256(open(page_file, "rb").read()).hexdigest()
BASE = "http://example.org/sen0401/%s" % N
DOC = URIRef(BASE + "/document")
PG = Namespace(BASE + "/page#"); IPO = Namespace("http://example.org/rdodi/interactive-page-ontology#")
WP = Namespace("http://example.org/widget-primitives#"); LD = Namespace("http://example.org/rdodi/learning-design#")
MP = Namespace("http://example.org/rdodi/model-provenance#"); SEN = Namespace("http://example.org/sen0401#")
g = Graph()
for p, ns in (("ipo", IPO), ("wp", WP), ("ld", LD), ("mp", MP), ("sen0401", SEN), ("pg", PG), ("owl", OWL), ("rdfs", RDFS), ("xsd", XSD), ("dcterms", DCTERMS), ("skos", SKOS), ("prov", PROV)): g.bind(p, ns)
EN = lambda t: Literal(t, lang="en")
ONT = URIRef(BASE + "/page")
UNIT = "chapter %d" % int(NUM)
UP = UNIT[0].upper() + UNIT[1:]
nodes = page_data["nodes"]; byid = {n["id"]: n for n in nodes}
first_sentence = lambda t: re.split(r"(?<=[a-z\)\]])\.\s+(?=[A-Z])", " ".join(t.split()), maxsplit=1)[0].rstrip(".") + "."
lo = lambda t: t[0].lower() + t[1:]

g.add((ONT, RDF.type, OWL.Ontology)); g.add((ONT, RDFS.label, EN("SEN0401 %s - RDODI Stage 4 page ABox" % UNIT))); g.add((ONT, OWL.versionInfo, Literal("2.0.0")))
for p, o in ((DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")), (DCTERMS.rights, EN("Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0.")), (DCTERMS.rightsHolder, URIRef("http://example.org/rdodi/agent/YusufAltunel")),
             (DCTERMS.publisher, URIRef("http://example.org/rdodi/agent/IstanbulKulturUniversity")), (DCTERMS.creator, URIRef("http://example.org/rdodi/agent/YusufAltunel")),
             (DCTERMS.identifier, Literal("sen0401_%s_page_abox_v2_0_0" % N)), (PROV.wasGeneratedBy, URIRef("http://example.org/sen0401/activity/%s-rdodi-run" % N)), (PROV.wasAttributedTo, URIRef("http://example.org/rdodi/agent/YusufAltunel"))):
    g.add((ONT, p, o))
# dates are not stamped by hand: the page file's own modification date is not content, so the ABox states the page version it describes instead
g.add((ONT, SEN.describesPageVersion, Literal(PV.replace("_", "."))))

def item(iri, types, label, definition, source):
    g.add((iri, RDF.type, OWL.NamedIndividual))
    for t in types: g.add((iri, RDF.type, t))
    g.add((iri, RDFS.label, EN(label))); g.add((iri, SKOS.definition, EN(definition))); g.add((iri, DCTERMS.source, source))

# the page and its regions
top = [n for n in nodes if n["level"] == 1]
item(PG.Page, [IPO.Page, IPO.InteractiveLearningSurface], "%s interactive page" % UP,
     "This page teaches %s of the course book as an interactive surface with %d sections in a three-level outline, %d widgets that the browser test exercised, and a quiz of %d questions." % (UNIT, len(nodes), len(TR["widgets"]), len(QUIZ)), DOC)
g.add((PG.Page, IPO.hasSourceDocument, PG.SourceDocument)); g.add((PG.Page, IPO.hasLayoutPattern, PG.Layout))
for r in ("Header", "Sidebar", "Main", "Card"): g.add((PG.Page, IPO.hasSemanticRegion, PG[r]))
g.add((PG.Page, IPO.includesNavigationPattern, PG.TopMenu)); g.add((PG.Page, IPO.includesNavigationPattern, PG.SectionTree))
g.add((PG.Page, SEN.pythonUsed, Literal(page_data["python"])))
g.add((PG.Page, SEN.pageFileSha256, Literal(sha)))
g.add((PG.Page, SEN.testNote, EN("The browser test ran on a copy of the page in which the instructor's release key is replaced by a test key; the result proves the page's logic and not the release step.")))
item(PG.SourceDocument, [IPO.SourceDocument], "%s Stage 3 document" % UP, "The Stage 3 document of %s is the text this page renders, section for section." % UNIT, DOC)
g.add((PG.SourceDocument, DCTERMS.source, DOC))
item(PG.Layout, [IPO.LayoutPattern], "Explorer, main area and detail card",
     "The page puts the chapter explorer at the left, the main area in the centre and a detail card at the right that stays closed until the reader asks for a detail.", DOC)
item(PG.Header, [IPO.Header], "Header with the main menu", "The header at the top holds the main menu, whose items are %s." % ", ".join(re.findall(r"top menu: (.*)", TR["features"].get("one top menu; its tab row is the only row of tabs - sub-subjects are chosen from a breadcrumb", {}).get("detail", "")) or ["the top-level menu"]), DOC)
item(PG.Sidebar, [IPO.Sidebar], "Chapter explorer", "The explorer at the left shows the chapter's sections as a tree and keeps pace with the tabs of the main area.", DOC)
item(PG.Main, [IPO.MainContent], "Main area", "The main area shows the chapter content of the selected menu item, with the widgets of its sections inline.", DOC)
item(PG.Card, [IPO.Sidebar], "Detail card", "The detail card at the right opens only when the reader explicitly asks for the details of a concept.", DOC)
item(PG.TopMenu, [IPO.PrimaryNavigation], "Main menu", "The main menu is permanently visible at the top and lets the reader reach every top-level area without scrolling or opening anything first.", DOC)
item(PG.SectionTree, [IPO.TreeNavigation], "Section tree", "The section tree lists the sections of the chapter by their three levels, and choosing one opens that single section.", DOC)

# learning objectives (the chapter's own outcomes)
serves = OBJ.get("_serves")
cos = {k: v for k, v in OBJ.items() if not k.startswith("_")}
for k, (text, lvl) in cos.items():
    item(PG[k], [IPO.LearningObjective], text, "After this chapter the learner can %s." % lo(text).rstrip("."), DOC)
    g.add((PG[k], LD.bloomLevel, LD[lvl]))
    g.add((PG.SourceDocument, IPO.hasLearningObjective, PG[k])); g.add((PG.Page, IPO.coversLearningObjective, PG[k]))

# sections and widgets: one each per node of the outline
nbychild = {}
for n in nodes: nbychild.setdefault(n.get("parent"), []).append(n)
LEVEL = {1: "branch", 2: "group", 3: "concept"}
nrun = nrec = 0
for n in nodes:
    sec = PG["S_" + n["id"]]; wid = PG["W_" + n["id"]]; src = URIRef(n["section_iri"]); cls = URIRef(n["class_iri"])
    where = ("under %s" % byid[n["parent"]]["label"]) if n.get("parent") in byid else "at the top of the outline"
    d = n.get("definition") or first_sentence(n["body"])
    item(sec, [IPO.ChapterSection], n["label"], d, src)
    g.add((sec, SEN.outlineLevel, Literal(n["level"]))); g.add((sec, SEN.anchor, Literal("#" + n["id"]))); g.add((PG.Page, IPO.coversChapterSection, sec))
    t = TR["widgets"]["w-" + n["id"]]; det = t["detail"]
    if det.startswith("printed"):
        runs = True; nrun += 1
        wd = "This widget runs the worked example of the concept %s in the reader's browser on the chapter's own library, shows what it printed, and lets the reader edit the code so that the printed result changes." % n["label"]
    elif det.startswith("static"):
        nrec += 1
        wd = "This widget shows the worked example of the concept %s with the output the research recorded, and does not run it in the browser because the example reads a saved file that a browser does not have." % n["label"]
    elif det.startswith("grid"):
        k = len(nbychild.get(n["id"], []))
        wd = "This widget shows the %d concepts of the group %s in a grid, and choosing one opens its card." % (k, n["label"])
    elif det.startswith("overview"):
        wd = "This widget is the overview of the branch %s, and choosing one of its sub-subjects opens that sub-subject." % n["label"]
    else:
        sys.exit("REFUSED: the test result of widget %s reads %r, which this builder has no truthful sentence for" % (n["id"], det))
    item(wid, [IPO.InstructionalWidget], "Widget of %s" % n["label"], wd, src)
    g.add((wid, IPO.demonstratesSubject, cls)); g.add((wid, WP.demonstratesConcept, cls)); g.add((wid, SEN.placedInSection, sec))
    g.add((wid, WP.hasDesignTest, Literal("Exercised in headless Chromium by 08-tooling/sen0401_page_test_v%s.py on page %s: %s" % (TR.get("_test_version", "9_35_0").replace("_", "."), PV.replace("_", "."), det))))
    g.add((wid, WP.designTestPassed, Literal(bool(t["passed"]))))
    if det.startswith("printed"):
        g.add((wid, SEN.runsInBrowser, Literal(True)))
    elif det.startswith("static"):
        g.add((wid, SEN.runsInBrowser, Literal(False)))

# the quiz
for i, it in enumerate(QUIZ, 1):
    q = PG["Q%d" % i]; g.add((q, RDF.type, LD.AssessmentItem)); g.add((q, RDF.type, OWL.NamedIndividual)); g.add((q, RDFS.label, EN(it["q"])))
    for j, o in enumerate(it["options"]):
        g.add((q, LD.hasOption, PG["Q%d_O%d" % (i, j)])); g.add((PG["Q%d_O%d" % (i, j)], RDF.type, LD.AnswerOption)); g.add((PG["Q%d_O%d" % (i, j)], RDFS.label, EN(o)))
    g.add((q, LD.hasCorrectOption, PG["Q%d_O%d" % (i, it["answer"])])); g.add((q, LD.cognitiveLevel, LD[it["level"]])); g.add((q, LD.assessesObjective, PG[it["objective"]]))
    for r in it.get("rationales", []): g.add((q, LD.distractorRationale, Literal(r)))

out = os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_abox_v2_0_0.ttl" % N)
g.serialize(out, format="turtle")
print("page ABox written: %d sections, %d widgets (%d run in the browser, %d recorded, %d marked tested), %d questions, %d objectives" % (len(nodes), len(nodes), nrun, nrec, sum(1 for w in TR["widgets"].values() if w["passed"]), len(QUIZ), len(cos)))
