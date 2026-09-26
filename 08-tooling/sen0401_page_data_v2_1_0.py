#!/usr/bin/env python3
"""Data for a SEN0401 chapter page, version 2: everything the page shows, extracted from the chapter's
Stage 2 ontology and Stage 3 document, with every example executed and every code diagram built from
Python's own ast module under the given interpreter. Nothing is typed by hand except the agent names.
Usage: sen0401_page_data_v2_1_0.py <NN> <python>  ->  08-tooling/chNN-page/page_data_vPV.json"""
__version__ = "2.1.0"
import json, os, re, subprocess, sys
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the version of the page they were produced for
import rdflib
from rdflib import RDF, RDFS, OWL
N, PY = sys.argv[1], sys.argv[2]
NUM = N; N = ("ch%s" % N) if N.isdigit() else N  # a numbered chapter, or a named supplement such as "numbers"
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(REPO, "03-materials", N, "rdodi"); import glob
f = lambda p: sorted(glob.glob(os.path.join(RD, "sen0401_%s_%s_v*.ttl" % (N, p))), key=lambda x: [int(v) for v in x.rsplit("_v",1)[1][:-4].split("_")])[-1]
T = rdflib.Graph(); T.parse(f("domain_tbox"), format="turtle"); A = rdflib.Graph(); A.parse(f("domain_abox"), format="turtle")
D = rdflib.Graph(); D.parse(f("document"), format="turtle"); R = rdflib.Graph(); R.parse(f("research"), format="turtle")
DOC = rdflib.Namespace("http://example.org/rdodi/document-ontology#"); SK = rdflib.namespace.SKOS; DC = rdflib.namespace.DCTERMS
RDN = rdflib.Namespace("http://example.org/rdodi/domain-ontology#"); RES = rdflib.Namespace("http://example.org/rdodi/research-ontology#")
BASE = "http://example.org/sen0401/%s" % N; CH = rdflib.Namespace(BASE + "#")
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
# evaluation steps: the innermost operation whose operands are already values is evaluated and replaced, until one value
# remains - every step computed by this interpreter, not written by hand
SAFE = {"int", "str", "float", "len", "round", "bool", "abs", "repr", "type", "min", "max"}
def reducible(n):
    if isinstance(n, ast.Call):
        return isinstance(n.func, ast.Name) and n.func.id in SAFE and not n.keywords and all(isinstance(a, ast.Constant) for a in n.args)
    if isinstance(n, ast.BoolOp) and isinstance(n.values[0], ast.Constant):
        # short-circuit: "and" stops at a false value, "or" at a true one, without evaluating the rest
        v = n.values[0].value
        if (isinstance(n.op, ast.And) and not v) or (isinstance(n.op, ast.Or) and v): return True
    if isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Compare, ast.BoolOp)):
        return all(isinstance(c, ast.Constant) for c in ast.iter_child_nodes(n) if isinstance(c, ast.expr))
    if isinstance(n, ast.IfExp):
        return isinstance(n.test, ast.Constant) and isinstance(n.body, ast.Constant) and isinstance(n.orelse, ast.Constant)
    if isinstance(n, ast.JoinedStr):
        return all(isinstance(v, ast.Constant) or (isinstance(v, ast.FormattedValue) and isinstance(v.value, ast.Constant) and v.format_spec is None) for v in n.values)
    return False
steps = []
try:
    whole = ast.parse(expr, mode="eval")
    for _ in range(40):
        # Python evaluates operands left to right, innermost first: post-order, and the first reducible node wins
        def post(n):
            if isinstance(n, ast.BoolOp):
                # operands left to right, stopping as soon as the operation can short-circuit
                for c in n.values:
                    yield from post(c)
                    if reducible(n): break
                yield n; return
            for c in ast.iter_child_nodes(n): yield from post(c)
            yield n
        cand = [n for n in post(whole.body) if reducible(n)]
        if not cand: break
        node = cand[0]
        before, focus = ast.unparse(whole.body), ast.unparse(node)
        try: val = eval(compile(ast.Expression(node), "<step>", "eval"), {})
        except Exception as e:
            steps.append({"expr": before, "focus": focus, "value": "%s: %s" % (type(e).__name__, e), "error": True}); break
        if not isinstance(val, (int, float, str, bool, type(None))): break
        steps.append({"expr": before, "focus": focus, "value": repr(val)})
        new = ast.Constant(val)
        for parent in ast.walk(whole):
            for f, v in ast.iter_fields(parent):
                if v is node: setattr(parent, f, new)
                elif isinstance(v, list): parent.__dict__[f] = [new if x is node else x for x in v]
        ast.fix_missing_locations(whole)
        if isinstance(whole.body, ast.Constant): break
except SyntaxError:
    steps = []
print(json.dumps({"out": out, "tree": tree(t), "steps": steps}))
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
            e = str(A.value(io, CH.input)); r = ex(e); node["io"] = {"code": e, "out": r["out"], "tree": r["tree"], "steps": r.get("steps", [])}
        er = A.value(X, RDN.hasErrorCondition)
        if er is not None:
            e = str(A.value(er, RDFS.label)).split(" raises ")[0]; node["error"] = {"code": e, "out": ex(e)["out"]}
        chart = A.value(X, rdflib.URIRef("http://example.org/sen0401#hasChartCanvas"))
        if chart is not None: node["chart"] = str(chart)
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
DISC = os.path.join(REPO, "08-tooling", "%s-page" % N, "discussion_v1_0_0.json")
EXTRA = os.path.join(REPO, "08-tooling", "%s-page" % N, "extra_v1_1_0.html")
data_extra = open(EXTRA).read() if os.path.exists(EXTRA) else ""
SEN = rdflib.Namespace("http://example.org/sen0401#")
findings = sorted(((str(R.value(f, RDFS.label)), str(R.value(f, SEN.findingText))) for f in R.subjects(RDF.type, SEN.Finding)), key=lambda x: x[0])
COURSE = json.load(open(os.path.join(REPO, "08-tooling", "course_page_config_v2_0_0.json")))
VIS = os.path.join(REPO, "08-tooling", "%s-page" % N, "visuals_v1_0_0.json")
data = {"_version": PV.replace("_", "."), "visuals": {k: v for k, v in (json.load(open(VIS)) if os.path.exists(VIS) else {}).items() if not k.startswith("_")}, "course": COURSE, "discussion": (lambda x: x["items"] if isinstance(x, dict) else x)(json.load(open(DISC))) if os.path.exists(DISC) else [], "research_file": os.path.basename(f("research")), "chapter": int(NUM) if NUM.isdigit() else None, "unit": json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "unit_v1_0_0.json"))) if not NUM.isdigit() else None, "title": title, "python": pyver, "nodes": nodes, "relations": rels, "agents": agents, "findings": findings, "refs": refs}
out = os.path.join(REPO, "08-tooling", "%s-page" % N); os.makedirs(out, exist_ok=True)
json.dump(data, open(os.path.join(out, "page_data_v%s.json" % PV), "w"), indent=1)
open(os.path.join(out, "extra_resolved_v%s.html" % PV), "w").write(data_extra)
print("chapter %s: %d concepts, %d relations (%d stated, %d co-mentions), %d agents, %d executed examples with ast trees, under %s" % (
    N, len(nodes), len(rels), sum(1 for r in rels if r["type"] != "mentions"), sum(1 for r in rels if r["type"] == "mentions"),
    len(agents), sum(1 for n in nodes if "io" in n), pyver))
