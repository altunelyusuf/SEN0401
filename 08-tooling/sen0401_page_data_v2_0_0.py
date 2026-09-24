#!/usr/bin/env python3
"""Data for a SEN0401 chapter page, version 2: everything the page shows, extracted from the chapter's
Stage 2 ontology and Stage 3 document, with every example executed and every code diagram built from
Python's own ast module under the given interpreter. Nothing is typed by hand except the agent names.
Usage: sen0401_page_data_v2_0_0.py <NN> <python>  ->  08-tooling/chNN-page/page_data_v2.json"""
import json, os, re, subprocess, sys
import rdflib
from rdflib import RDF, RDFS, OWL
N, PY = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi"); import glob
f = lambda p: sorted(glob.glob(os.path.join(RD, "sen0401_ch%s_%s_v*.ttl" % (N, p))), key=lambda x: [int(v) for v in x.rsplit("_v",1)[1][:-4].split("_")])[-1]
T = rdflib.Graph(); T.parse(f("domain_tbox"), format="turtle"); A = rdflib.Graph(); A.parse(f("domain_abox"), format="turtle")
D = rdflib.Graph(); D.parse(f("document"), format="turtle"); R = rdflib.Graph(); R.parse(f("research"), format="turtle")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#"); SK = rdflib.namespace.SKOS; DC = rdflib.namespace.DCTERMS
RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#"); RES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")
BASE = "http://example.org/sen0401/ch%s" % N; CH = rdflib.Namespace(BASE + "#")
pyver = subprocess.run([PY, "--version"], capture_output=True, text=True).stdout.strip()

EXEC = r'''
import ast, json, sys
expr = sys.argv[1]
def tree(n):
    kids = [tree(c) for c in ast.iter_child_nodes(n) if not isinstance(c, (ast.Load, ast.Store, ast.operator, ast.unaryop, ast.cmpop, ast.boolop))]
    if isinstance(n, ast.BinOp): lab = {ast.Add:"+",ast.Sub:"-",ast.Mult:"*",ast.Div:"/",ast.FloorDiv:"//",ast.Mod:"%",ast.Pow:"**"}.get(type(n.op), type(n.op).__name__)
    elif isinstance(n, ast.Constant): lab = repr(n.value)
    elif isinstance(n, ast.Name): lab = n.id
    elif isinstance(n, ast.Call): lab = "call"
    elif isinstance(n, ast.JoinedStr): lab = "f-string"
    elif isinstance(n, ast.FormattedValue): lab = "{ }"
    else: lab = type(n).__name__
    return {"label": lab, "kind": type(n).__name__, "children": kids}
t = ast.parse(expr, mode="eval").body
try: out = repr(eval(expr, {}))
except Exception as e: out = "%s: %s" % (type(e).__name__, e)
print(json.dumps({"out": out, "tree": tree(t)}))
'''
def ex(expr):
    r = subprocess.run([PY, "-c", EXEC, expr], capture_output=True, text=True, timeout=20)
    return json.loads(r.stdout)

label = lambda c: str(T.value(c, RDFS.label))
classes = list(T.subjects(RDF.type, OWL.Class))
parent = {str(c): str(T.value(c, RDFS.subClassOf)) if T.value(c, RDFS.subClassOf) else None for c in classes}
secs = {str(D.value(s, DC.source)): s for s in D.subjects(DOC.sectionTitle, None)}
order = sorted(classes, key=lambda c: int(D.value(secs[str(c)], DOC.sectionOrder)))
nodes = []
for c in order:
    s = secs[str(c)]; cid = str(c).split("#")[-1]
    X = next((x for x in A.subjects(RDF.type, c) if str(x).split("#")[-1].startswith("X_")), None)
    node = {"id": cid, "label": label(c), "level": int(D.value(s, DOC.hierarchyLevel)), "parent": parent[str(c)].split("#")[-1] if parent[str(c)] else None,
            "body": str(D.value(s, SK.definition)), "section_iri": str(s), "class_iri": str(c)}
    if X is not None:
        node["example"] = str(A.value(X, RDFS.label)); node["definition"] = str(A.value(X, SK.definition))
        io = A.value(X, RDN.hasIOExample)
        if io is not None:
            e = str(A.value(io, CH.input)); r = ex(e); node["io"] = {"code": e, "out": r["out"], "tree": r["tree"]}
        er = A.value(X, RDN.hasErrorCondition)
        if er is not None:
            e = str(A.value(er, RDFS.label)).split(" raises ")[0]; node["error"] = {"code": e, "out": ex(e)["out"]}
        own = A.value(X, CH.hasOwner)
        if own is not None: node["owner"] = str(own).split("#")[-1].replace("X_", "")
    nodes.append(node)
ids = {n["id"] for n in nodes}; bylabel = {n["label"].lower(): n["id"] for n in nodes}
# Relations, each with its evidence: stated in the ontology, or a co-mention the document itself makes.
rels = []
for n in nodes:
    if n["parent"]: rels.append({"source": n["id"], "target": n["parent"], "type": "is a kind of", "evidence": "rdfs:subClassOf in the chapter's domain TBox"})
    if n.get("owner"): rels.append({"source": n["id"], "target": n["owner"], "type": "operates on", "evidence": "hasOwner (a subproperty of RDODI's hasOwningConcept) in the chapter's domain ABox"})
for n in nodes:
    if n["level"] < 3: continue
    for m in nodes:
        if m is n or m["level"] < 3 or m["parent"] == n["parent"]: continue
        if re.search(r"\b%s\b" % re.escape(m["label"].lower()), n["body"].lower()):
            rels.append({"source": n["id"], "target": m["id"], "type": "mentions", "evidence": "the document's section on %s names %s" % (n["label"], m["label"])})
# Subjects and their agents: one per second-level subject, named for what it covers.
AGENT = {"Unit": "Units agent", "Supply": "Supply agent", "Price": "Price agent", "Consensus": "Consensus agent", "History": "History agent", "WalletPlatform": "Wallet agent", "NodeType": "Node agent", "KeyControl": "Keys agent", "Backup": "Recovery agent", "Address": "Address agent", "Transfer": "Payments agent", "SemanticBridge": "Semantic web agent", "NumericValue": "Numbers agent", "TextValue": "Text agent", "ArithmeticOperation": "Arithmetic agent", "TextOperation": "String agent",
         "BindingOperation": "Variables agent", "IOFunction": "Input-output agent", "ConversionFunction": "Conversion agent", "MeasurementFunction": "Measurement agent",
         "InteractiveEnvironment": "Shell agent", "InterpreterBuild": "Interpreter agent", "StringFormatting": "Formatting agent", "Tooling": "Tooling agent",
         "TruthValue": "Truth agent", "EqualityComparison": "Equality agent", "OrderingComparison": "Ordering agent", "LogicalOperator": "Logic agent",
         "Evaluation": "Evaluation agent", "ControlStructure": "Structure agent", "Branching": "Branching agent", "ExpressionForm": "Expression agent",
         "PatternMatching": "Matching agent", "Style": "Style agent"}
agents = [{"id": "agent-" + n["id"], "name": AGENT.get(n["id"], n["label"] + " agent"), "subject": n["id"],
           "covers": [m["id"] for m in nodes if m["parent"] == n["id"]] + [n["id"]]} for n in nodes if n["level"] == 2]
refs = sorted((str(R.value(p, RDFS.label)), str(R.value(p, DC.source))) for p in R.subjects(RDF.type, RES.Publication))
title = next(str(o) for s, o in D.subject_objects(RDFS.label) if str(s).endswith("#Document"))
data = {"research_file": os.path.basename(f("research")), "chapter": int(N), "title": title, "python": pyver, "nodes": nodes, "relations": rels, "agents": agents, "refs": refs}
out = os.path.join(REPO, "08-tooling", "ch%s-page" % N); os.makedirs(out, exist_ok=True)
json.dump(data, open(os.path.join(out, "page_data_v2.json"), "w"), indent=1)
print("chapter %s: %d concepts, %d relations (%d stated, %d co-mentions), %d agents, %d executed examples with ast trees, under %s" % (
    N, len(nodes), len(rels), sum(1 for r in rels if r["type"] != "mentions"), sum(1 for r in rels if r["type"] == "mentions"),
    len(agents), sum(1 for n in nodes if "io" in n), pyver))
