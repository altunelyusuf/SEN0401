#!/usr/bin/env python3
"""RDODI Stages 2 and 3 for one SEN0401 chapter, from its corpus file (sen0401_chNN_corpus_vX_Y_Z.py, the newest one in this folder).
Writes the domain TBox and ABox and the document (one section per concept, the paragraphs of a concept joined by a blank line) at the
version given, and states the version it revises. The SHACL shapes and the Stage 1 research record are not rewritten here.
Generalised from SEN0414's sen0414_chapter_build_v1_0_0.py to SEN0401's ontology conventions (read from the existing files in
03-materials/ch01..ch04/rdodi):
  * the chapter's own terms use the prefix chx: = <http://example.org/sen0401/chNN#> (SEN0414 used chNN:), the ontology IRIs are
    http://example.org/sen0401/chNN/{tbox,abox,document,research}, the run is http://example.org/sen0401/activity/chNN-rdodi-run,
    the vendor namespace is http://example.org/sen0401# (prefix written sen0401:; the older files wrote it sen0414:, the same IRI);
  * a concept's individual is chx:X_<Id>, its worked example chx:IO_<Id> (chx:input / chx:output literals), a document section chx:S_<Id>
    with dcterms:source <.../chNN#Id>; the ontology identifiers are sen0401_chNN_tbox_vX_Y_Z, ..._abox_..., ..._document_...
  * the document sections sit under chx:Document with the same section vocabulary as before (doc:TaxonomicSection for levels 1-2,
    doc:ConceptSection for level 3).
usage: sen0401_chapter_build_v1_0_0.py NN NEWVERSION PRIORVERSION [DATE]      e.g.  02 1.2.0 1.1.1
Environment (all optional): SEN0401_CORPUS_DIR (where sen0401_chNN_corpus_v*.py is looked for; default this folder), SEN0401_OUT_DIR (where
the three .ttl files are written; default 03-materials/chNN/rdodi - set it to build a scratch copy), CHECK_PY (interpreter that executes
the corpus claims; default python3.14 when present, else the running one), SKIP_CHECKS=1 (do not execute the claims), SHACL_FILE.

THE CORPUS MODULE supplies (module attributes):
  CHAPTER      "02" - must equal NN
  NODES        list of (id, label-or-None, level, parent-or-None, leaf, paras): level 1 = main subject, 2 = subject (it gets an agent), 3 = concept;
               leaf is None for levels 1 and 2 and (example label, definition, io-or-None) for level 3, io = (expression, expected repr) or None;
               paras is a list of (facet, text) - the facet ("What it is", "Why it matters", ...) is a writing guide that facet_text() may print or not.
               A node's order is the document's order (depth first); a label of None is made from the camel-case id.
  facet_text   facet_text(paras) -> the section text ("\\n\\n".join of the texts, with or without the facet); optional, the plain join is the default
  CHECKS       [(python expression, expected repr)] - every number or output the text quotes; executed by this builder (SKIP_CHECKS=1 to skip)
  RAISES       [(python statement or expression, ExceptionClassName)] - claims that something fails; executed by this builder
  OWNERS       [(leaf id, owning leaf id)]                            optional  - chx:X_leaf chx:hasOwner chx:X_owner
  ERRORS       [(leaf id, "expr raises ErrorType: message start")]    optional  - chx:Err_leaf; executed by this builder
  CQS          [competency question, ...]
  PROVENANCE   one sentence on where the concepts come from
  TOOLING      the label of the environment that executed the claims, e.g. "CPython 3.14.4" (SEN0414 called it INTERPRETERS; that name is still
               accepted. A blockchain chapter's claims are Python expressions - hashlib, integer arithmetic - so the version rarely matters,
               but the ontology records what ran them.)
  CHANGE       what this version changes and why it is MAJOR, MINOR or PATCH (goes into the ontology comments)
  DOC_TITLE, DOC_ABOUT   the document's title and its one-sentence introduction
Every io expression of a leaf, every CHECKS and RAISES entry and every ERRORS entry is executed by this builder before anything is written;
a claim that does not hold stops the build (the ontology must never state what the interpreter does not give)."""
__version__ = "1.0.0"
import datetime, glob, importlib.util, json, os, re, subprocess, sys
import rdflib
from rdflib import RDF, RDFS, OWL

NN, NEW, PRIOR = sys.argv[1], sys.argv[2], sys.argv[3]
MODIFIED = sys.argv[4] if len(sys.argv) > 4 else datetime.date.today().isoformat()
V = NEW.replace(".", "_"); here = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(here)
vkey = lambda f: [int(x) for x in re.search(r"_v(\d+_\d+_\d+)\.(?:py|ttl)$", f).group(1).split("_")]
CDIR = os.environ.get("SEN0401_CORPUS_DIR", here)
cands = sorted(glob.glob(os.path.join(CDIR, "sen0401_ch%s_corpus_v*.py" % NN)), key=vkey)
assert cands, "no corpus file sen0401_ch%s_corpus_v*.py in %s" % (NN, CDIR)
_sp = importlib.util.spec_from_file_location("corpus", cands[-1]); CORPUS = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(CORPUS)
assert str(CORPUS.CHAPTER) == NN, "the corpus says chapter %r, the command says %r" % (CORPUS.CHAPTER, NN)
OUT = os.environ.get("SEN0401_OUT_DIR", os.path.join(REPO, "03-materials", "ch" + NN, "rdodi")); os.makedirs(OUT, exist_ok=True)
P = "ch" + NN
BASE = "http://example.org/sen0401/" + P
RESEARCH = BASE + "/research"
TOOLING = getattr(CORPUS, "TOOLING", None) or getattr(CORPUS, "INTERPRETERS")
facet_text = getattr(CORPUS, "facet_text", None) or (lambda paras: "\n\n".join(t for f, t in paras))
NODES = [(n[0], n[1], n[2], n[3], n[4], ([("", n[5])] if isinstance(n[5], str) else n[5])) for n in CORPUS.NODES]
OWNERS, ERRORS = getattr(CORPUS, "OWNERS", []), getattr(CORPUS, "ERRORS", [])

# ---- the shape of NODES, checked before anything is written ----
byid = {n[0]: n for n in NODES}
assert len(byid) == len(NODES), "duplicate concept ids: %s" % sorted({n[0] for n in NODES if [m[0] for m in NODES].count(n[0]) > 1})
for i, n in enumerate(NODES):
    nid, lab, lv, par, leaf, paras = n
    assert re.fullmatch(r"[A-Za-z][A-Za-z0-9]*", nid), "id %r must be letters and digits" % nid
    assert lv in (1, 2, 3), "%s: level must be 1, 2 or 3" % nid
    assert (par is None) == (lv == 1), "%s: a level 1 concept has no parent, any other has one" % nid
    if par is not None:
        assert par in byid and byid[par][2] == lv - 1, "%s: parent %r must be a level %d concept" % (nid, par, lv - 1)
        assert [m[0] for m in NODES].index(par) < i, "%s: its parent must come earlier in NODES" % nid
    assert (lv == 3) == (leaf is not None), "%s: only level 3 concepts carry (example, definition, io)" % nid
    assert paras and all(isinstance(p, (tuple, list)) and len(p) == 2 and p[1].strip() for p in paras), "%s: paras must be non-empty (facet, text) pairs" % nid
    if leaf is not None: assert len(leaf) == 3 and leaf[0].strip() and leaf[1].strip() and (leaf[2] is None or len(leaf[2]) == 2), "%s: leaf is (example, definition, io-or-None)" % nid
for leaf, owner in OWNERS: assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, "OWNERS: %s/%s must be level 3 concepts" % (leaf, owner)
for leaf, text in ERRORS: assert leaf in byid and byid[leaf][2] == 3 and " raises " in text, "ERRORS: %s needs a level 3 concept and 'expr raises Type: message'" % leaf

# ---- the claims, executed ----
def check_claims():
    py = os.environ.get("CHECK_PY") or next((p for p in ("/root/.local/bin/python3.14", "python3.14") if os.path.exists(p) or subprocess.run(["which", p], capture_output=True).returncode == 0), sys.executable)
    ios = [(n[0], n[4][2][0], n[4][2][1]) for n in NODES if n[4] and n[4][2]]
    errs = [(leaf, *text.split(" raises ", 1)) for leaf, text in ERRORS]
    prog = r'''
import json, sys
jobs = json.loads(sys.stdin.read()); bad = []
def run_stmt(e):
    if "=" in e.replace("==", "").replace("!=", "").replace("<=", "").replace(">=", "") or ";" in e or e.startswith(("import ", "from ")): return exec(e, {})
    return eval(e, {})
for kind, tag, e, x in jobs:
    try:
        if kind in ("check", "io"):
            got = repr(eval(e, {}))
            if got != x: bad.append((kind, tag, e, "expected %r got %r" % (x, got)))
        elif kind == "raise":
            try: run_stmt(e); bad.append((kind, tag, e, "no error, expected " + x))
            except BaseException as ex:
                if type(ex).__name__ != x: bad.append((kind, tag, e, "raised %s, expected %s" % (type(ex).__name__, x)))
        elif kind == "error":
            et, msg = x.split(": ", 1) if ": " in x else (x, "")
            try: run_stmt(e); bad.append((kind, tag, e, "no error, expected " + et))
            except BaseException as ex:
                if type(ex).__name__ != et or not str(ex).startswith(msg): bad.append((kind, tag, e, "raised %s: %s" % (type(ex).__name__, ex)))
    except BaseException as ex:
        bad.append((kind, tag, e, "%s: %s" % (type(ex).__name__, ex)))
print(json.dumps({"bad": bad, "n": len(jobs)}))
'''
    jobs = [("check", "", e, x) for e, x in CORPUS.CHECKS] + [("raise", "", e, x) for e, x in CORPUS.RAISES] + [("io", i, e, x) for i, e, x in ios] + [("error", i, e.strip(), x.strip()) for i, e, x in errs]
    r = subprocess.run([py, "-c", prog], input=json.dumps(jobs), capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, "claims runner failed under %s: %s" % (py, r.stderr[-400:])
    res = json.loads(r.stdout)
    assert not res["bad"], "claims that do not hold under %s:\n  %s" % (py, "\n  ".join(map(str, res["bad"])))
    print("claims executed under %s: %d, all hold" % (subprocess.run([py, "--version"], capture_output=True, text=True).stdout.strip(), res["n"]))
if not os.environ.get("SKIP_CHECKS"): check_claims()

# ---- text ----
old = sorted(glob.glob(os.path.join(OUT, "sen0401_%s_tbox_v*.ttl" % P)) + glob.glob(os.path.join(OUT, "sen0401_%s_domain_tbox_v*.ttl" % P)), key=vkey)
m = re.search(r'dcterms:created "([0-9-]+)"', open(old[0]).read()) if old else None
CREATED = m.group(1) if m else MODIFIED   # the first version's date stays
PFX = '''@prefix chx:     <%s#> .
@prefix res:     <http://example.org/rdodi/research-ontology#> .
@prefix rd:      <http://example.org/rdodi/domain-ontology#> .
@prefix doc:     <http://example.org/rdodi/document-ontology#> .
@prefix sen0401: <http://example.org/sen0401#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix prov:    <http://www.w3.org/ns/prov#> .
@prefix sh:      <http://www.w3.org/ns/shacl#> .
''' % BASE
def q(s):
    """a Turtle string body: backslash, double quote and line breaks escaped, nothing else changed (SEN0414's builder turned a double quote into a single one)"""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
def header(part, iri, label, ident):
    return '''<%s> a owl:Ontology ;
    rdfs:label "%s"@en ; owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; rdfs:comment "%s"@en ;
    dcterms:license <https://creativecommons.org/licenses/by/4.0/> ;
    dcterms:rights "Copyright (c) 2026 Yusuf Altunel. Licensed CC BY 4.0."@en ;
    dcterms:rightsHolder <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:publisher <http://example.org/rdodi/agent/IstanbulKulturUniversity> ;
    dcterms:creator <http://example.org/rdodi/agent/YusufAltunel> ;
    dcterms:created "%s"^^xsd:date ; dcterms:modified "%s"^^xsd:date ;
    dcterms:identifier "%s" ; prov:wasRevisionOf <%s/%s> ;
    prov:wasGeneratedBy <http://example.org/sen0401/activity/%s-rdodi-run> ;
    prov:wasAttributedTo <http://example.org/rdodi/agent/YusufAltunel> .
''' % (iri, q(label), NEW, iri, NEW, q(CORPUS.CHANGE), CREATED, MODIFIED, ident, iri, PRIOR, P)
def top(i):
    while byid[i][3]: i = byid[i][3]
    return i
TAX = [(top(n[0]), n[3], n[0], n[4][0], n[4][1], n[4][2]) for n in NODES if n[2] == 3]
LABELS = {n[0]: n[1] for n in NODES if n[1]}
def label_of(c): return LABELS.get(c) or "".join(" " + ch.lower() if ch.isupper() and i else ch for i, ch in enumerate(c)).strip()

def tbox():
    L = [PFX, header("tbox", BASE + "/tbox", "SEN0401 chapter %d domain ontology - TBox" % int(NN), "sen0401_%s_tbox_v%s" % (P, V))]
    seen = set()
    for n in NODES:   # classes in NODES order, so the file reads like the document
        c = n[0]
        if c in seen: continue
        seen.add(c); lab = label_of(c)
        L.append('chx:%s a owl:Class ; rdfs:label "%s"@en ;%s rdfs:isDefinedBy <%s/tbox> .' % (c, q(lab[0].upper() + lab[1:]), (" rdfs:subClassOf chx:%s ;" % n[3]) if n[3] else "", BASE))
    tops = sorted({t[0] for t in TAX}, key=[n[0] for n in NODES].index)
    for i, a in enumerate(tops):
        for b in tops[i + 1:]: L.append("chx:%s owl:disjointWith chx:%s ." % (a, b))
    if OWNERS: L.append('chx:hasOwner a owl:ObjectProperty ; rdfs:label "owned by"@en ; rdfs:subPropertyOf rd:hasOwningConcept .')
    return "\n".join(L) + "\n"

def abox():
    L = [PFX, header("abox", BASE + "/abox", "SEN0401 chapter %d domain ontology - ABox" % int(NN), "sen0401_%s_abox_v%s" % (P, V))]
    for t, mid, leaf, ex, d, io in TAX:
        L.append('chx:X_%s a owl:NamedIndividual, chx:%s ; rdfs:label "%s"@en ; skos:definition "%s"@en ; dcterms:source <%s> .' % (leaf, leaf, q(ex), q(d), RESEARCH))
        if io:
            L.append('chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; chx:input "%s" ; chx:output "%s" .' % (leaf, q(io[0]), q(io[1]), q(io[0]), q(io[1])))
            L.append("chx:X_%s rd:hasIOExample chx:IO_%s ." % (leaf, leaf))
    for leaf, owner in OWNERS: L.append("chx:X_%s chx:hasOwner chx:X_%s ." % (leaf, owner))
    for leaf, text in ERRORS:
        L.append('chx:Err_%s a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label "%s"@en .' % (leaf, q(text)))
        L.append("chx:X_%s rd:hasErrorCondition chx:Err_%s ." % (leaf, leaf))
    cq = ["chx:CQ%d" % (i + 1) for i in range(len(CORPUS.CQS))]
    L.append('''
chx:Artifact a owl:NamedIndividual, rd:DomainOntologyArtifact ; rdfs:label "SEN0401 chapter %(n)d domain ontology"@en ;
    rd:derivedFromResearchSubject <%(r)s> ; rd:hasCompetencyQuestion chx:CQs ; rd:hasSourceProvenance chx:Provenance ;
    rd:hasReusabilityScope rd:RS_SubjectSpecific ; rd:hasResolutionEnvironment chx:Env .
chx:CQs a owl:NamedIndividual, rd:CompetencyQuestionSet ; rdfs:label "Chapter %(n)d competency questions"@en ; rd:containsCompetencyQuestion %(cq)s .''' % dict(n=int(NN), r=RESEARCH, cq=", ".join(cq)))
    for c, text in zip(cq, CORPUS.CQS): L.append('%s a owl:NamedIndividual, rd:CompetencyQuestion ; rdfs:label "%s"@en .' % (c, q(text)))
    L.append('''chx:Provenance a owl:NamedIndividual, rd:ResearchSubjectInput ; rdfs:label "Derived from the chapter %(n)d research artefact"@en ;
    skos:definition "%(prov)s"@en ;
    dcterms:source <%(r)s> .
chx:Env a owl:NamedIndividual, rd:ResolutionEnvironment ; rdfs:label "%(env)s"@en ;
    skos:definition "Every input-output example and error condition, and every quoted result in the chapter text (%(k)d checks listed in %(cf)s), executed under %(env)s."@en ;
    dcterms:source "The execution run of this ontology's build, 08-tooling/sen0401_chapter_build_v1_0_0.py, over the claims in 08-tooling/%(cf)s" .
''' % dict(n=int(NN), prov=q(CORPUS.PROVENANCE), r=RESEARCH, env=q(TOOLING), k=len(CORPUS.CHECKS) + len(CORPUS.RAISES) + len(ERRORS) + sum(1 for t in TAX if t[5]), cf=os.path.basename(cands[-1])))
    return "\n".join(L) + "\n"

def document():
    T = rdflib.Graph(); T.parse(os.path.join(OUT, "sen0401_%s_domain_tbox_v%s.ttl" % (P, V)), format="turtle")
    CH = rdflib.Namespace(BASE + "#")
    BODY = {n[0]: facet_text(n[5]) for n in NODES}; BO = list(BODY); ORDER = []
    def walk(c, level, parent):
        ORDER.append((c, level, parent))
        for k in sorted(T.subjects(RDFS.subClassOf, c), key=lambda k: BO.index(str(k).split('#')[-1])): walk(k, level + 1, c)
    for t in sorted([c for c in T.subjects(RDF.type, OWL.Class) if not list(T.objects(c, RDFS.subClassOf))], key=lambda c: BO.index(str(c).split('#')[-1])): walk(t, 1, None)
    assert len(ORDER) == len(NODES), "the TBox and the corpus disagree on the concepts"
    D = BASE + "/document"
    L = [PFX, header("document", D, "SEN0401 chapter %d - RDODI Stage 3 document" % int(NN), "sen0401_%s_document_v%s" % (P, V)),
         'chx:Document a doc:ReportSection ; rdfs:label "%s"@en ; skos:definition "%s" ; dcterms:source <%s> ;' % (q(getattr(CORPUS, "DOC_TITLE", "SEN0401 chapter %d" % int(NN))), q(getattr(CORPUS, "DOC_ABOUT", "")), RESEARCH),
         '    doc:hasSection ' + ", ".join("chx:S_%s" % str(c).split('#')[-1] for c, lv, p in ORDER if lv == 1) + ' .']
    for n, (c, lv, p) in enumerate(ORDER, 1):
        name = str(c).split('#')[-1]; title = str(T.value(c, RDFS.label)); kind = "doc:TaxonomicSection" if lv < 3 else "doc:ConceptSection"
        L.append('chx:S_%s a %s ; rdfs:label "%s"@en ; doc:sectionTitle "%s" ; doc:hierarchyLevel %d ; doc:sectionOrder %d ;' % (name, kind, q(title), q(title), lv, n))
        if p is not None: L.append('    doc:hasParentSection chx:S_%s ;' % str(p).split('#')[-1])
        L.append('    skos:definition "%s" ; dcterms:source <%s#%s> .' % (q(BODY[name]), BASE, name))
    open(os.path.join(OUT, "sen0401_%s_document_v%s.ttl" % (P, V)), "w").write("\n".join(L) + "\n"); return len(ORDER)

for name, fn in (("tbox", tbox), ("abox", abox)):
    open(os.path.join(OUT, "sen0401_%s_domain_%s_v%s.ttl" % (P, name, V)), "w").write(fn())
n_sections = document()
# ---- the new files must parse, and satisfy the chapter's shapes when there are some ----
G = {}
for part in ("domain_tbox", "domain_abox", "document"):
    f = os.path.join(OUT, "sen0401_%s_%s_v%s.ttl" % (P, part, V)); G[part] = rdflib.Graph(); G[part].parse(f, format="turtle")
shapes = os.environ.get("SHACL_FILE") or (sorted(glob.glob(os.path.join(OUT, "sen0401_%s_domain_shacl_v*.ttl" % P)), key=vkey) or [None])[-1]
if shapes:
    import pyshacl
    data = G["domain_tbox"] + G["domain_abox"]
    ok, _, txt = pyshacl.validate(data, shacl_graph=rdflib.Graph().parse(shapes, format="turtle"), inference="none")
    assert ok, "the chapter's SHACL shapes (%s) are violated:\n%s" % (os.path.basename(shapes), txt[:1500])
    print("SHACL %s: conforms" % os.path.basename(shapes))
print("chapter %s ontology %s (revises %s) - %d classes, %d concept individuals, %d sections, written to %s" % (
    NN, NEW, PRIOR, len(NODES), len(TAX), n_sections, OUT))
