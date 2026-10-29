#!/usr/bin/env python3
"""Data for a SEN0401 chapter page, version 2: everything the page shows, extracted from the chapter's
Stage 2 ontology and Stage 3 document, with every example executed and every code diagram built from
Python's own ast module under the given interpreter. Nothing is typed by hand except the agent names.
Usage: sen0401_page_data_v2_11_0.py <NN> <python>  ->  08-tooling/chNN-page/page_data_vPV.json"""
__version__ = "2.25.0"
# 2.25.0 (over 2.24.0; owner's words of 2026-10-30, no lambda unless the subject teaches lambda, ex:CR3_Remedy56 follow-up, task TK_Urgent_Ch06_Page_Build): with environment PLAIN_CODE=1 every worked example whose code holds a lambda is rewritten by
#   sen0401_plain_code_v1_0_0.py as plain statements (the wrapper (lambda g: (exec(...)))({}) becomes its source and a closing 'result'; an immediate lambda becomes assignments and its body; a helper 'name = lambda' becomes a def),
#   and the build STOPS unless the rewritten code prints the same result as the original under the given interpreter. Nothing else changed from 2.24.0.
# 2.24.0 (over 2.23.0; for page template 9.52.0, the owner's words of 2026-10-22 17:27 and 17:30 Istanbul, ex:CR3_Remedy56): the data gains
#   (a) "chaptercode": the chapter-code manifest 03-materials/chNN/page/chapter_code_chNN_v*.json (the newest version, or the file named by
#       env CC_MANIFEST), written by the deck task of the chapter: an ordered list of the deck's code examples, each with its order number
#       (the deck's slide order), a short NAME, the code that runs in the page with the chapter library the page defines (pywheels), the
#       expected result and, optionally, the slide number, a plain-language note and a hint for the result visual. The reader accepts the
#       list at the top level or under "examples"; per item the keys order|n, name|title, code, slide|slide_no, expected|expected_result|result|output,
#       note|explain|explanation, viz, and refuses a manifest whose orders repeat or run backwards, whose names repeat or are empty, or whose
#       code is empty. When no manifest file exists the page data carries no "chaptercode" and the template builds no chapter-code tab.
#   (b) "panels": for every group (level 2) the ordered list of its concept panels (level 3 ids, document order), so that one panel holds one
#       concept; the template builds one panel per entry (the structure comes from the chapter research through the nodes).
#   (c) environment PAGE_DATA_OUT: the folder the data and the resolved extra file are written to (default the chapter's 08-tooling folder),
#       so a scratch page can be built outside the repository.
#   Nothing else changed from 2.23.0.
# 2.23.0 (over 2.22.0; for the section links of the research, ruling G134: links, not text): a statement of the chapter's domain ABox (or, between two section classes, of the domain TBox) whose predicate is an owl:ObjectProperty declared in the domain TBox with kb:hasRelationshipCategory, and whose two ends belong to two DIFFERENT sections (an individual belongs to the section whose class it is an instance of), is a page relation of type 'operates on' (the template draws every type other than 'mentions' that way). Its evidence names the property (its label), its category (the RelationshipCategory_ individual) and the sentence the link carries (the owl:Axiom rdfs:comment of the statement), or says that it carries none. chx:hasOwner keeps its own reading; a statement is read once however many times it is stated. A chapter whose research has no such statement gets exactly the relations 2.22.0 gives (the relations are appended between the hasOwner relations and the co-mentions, in a fixed order). Nothing else changed.
# 2.22.0 (over 2.21.0): environment SEN0401_PIN, a comma list of name=version (lecture, resources, stories_img, stories, e.g. lecture=1_1_1,stories_img=1_0_0,stories=1_1_0), chooses those inputs by version instead of the newest, so that a page can be rebuilt from exactly the inputs of an earlier page (an engineering-only rebuild). Without it nothing changes.
# 2.21.0 (over 2.20.0; for the pages of chapters 1 to 7 that carry the deck v1.2.0 links): reads course_page_config_v2_16_0.json (materials register 1.4.14, which corrects the chapter 3 date). Nothing else changed.
# 2.20.0 (over 2.19.0): a story keeps its linkLabel (stories module 1.2.0: the deck's title and kind of the resource its link goes to) when it has one. Nothing else changed.
# 2.19.0 (over 2.18.0; for chapter 14): chapter 14's common first line is added to PRE_LINES (same form as chapters 12 and 13, with sen0401_ch14_lib_v1_0_0). Reads course_page_config_v2_15_0.json as before.
# 2.18.0 (over 2.17.0; for chapter 13): chapter 13's common first line is added to PRE_LINES (the same form as chapter 12's, with sen0401_ch13_lib_v1_0_0). Reads course_page_config_v2_15_0.json as before.
# 2.17.0 (over 2.16.0; for chapter 12): chapter 12's common first line is added to PRE_LINES ("import sys, math, hashlib, datetime; ...; import sen0401_ch12_lib_v1_0_0 as L; R = L.run(); "). Reads course_page_config_v2_15_0.json as 2.16.0 does (the materials register is not changed for this page).
# 2.16.0 (over 2.15.0; for the rebuilt chapter 9 page 9.46.0): reads course_page_config_v2_15_0.json (materials register 1.4.13). Nothing else changed.
# 2.15.0 (over 2.14.0; for chapter 11): reads course_page_config_v2_14_0.json (materials register 1.4.12); chapter 11's common first line is added to PRE_LINES ("import sys, hashlib, datetime; ...; import sen0401_ch11_lib_v1_0_0 as L; R = L.run(); ").
# 2.14.0 (over 2.13.0; for chapter 10): (a) reads course_page_config_v2_14_0.json (materials register 1.4.11). (b) The line that every worked example of a chapter begins with is known per chapter (PRE_LINES): chapter 9's as before, chapter 10's
#   "import sys; ...; import sen0401_ch10_lib_v1_0_0 as L; import sen0401_ch10_p2p_v1_0_0 as P; R = L.run(); " (the page's worker runs it once from the wheel and makes L, P and R available to every program).
# 2.13.0 (over 2.12.0; for chapter 9, (d) the Code Lab snippet that re-runs every example runs statements before the closing expression; whose worked examples are expressions over the recorded runs of Bitcoin Core, the saved sources and the chapter library): (a) reads course_page_config_v2_14_0.json (materials
#   register 1.4.10). (b) A worked example that begins with the chapter 9 line "import sys; ...; import sen0401_ch09_lib_v1_0_0 as L; R = L.run(); R2 = L.run2(); C = L.census(); " is shown and run as what follows
#   that line (the page's worker unpacks the library and the recorded data from the wheel at boot, runs the line once and makes L, R, R2 and C available to every program); its result is computed here by running
#   the whole line and the rest in the repository. (c) An example of several statements ending in an expression keeps its statements: they run first and the tree is that of the closing expression (no evaluation steps).
# 2.12.0 (over 2.11.0; for chapter 8, whose worked examples call the chapter's own library): (a) reads course_page_config_v2_11_0.json (materials register 1.4.9). (b) A worked example of the form
#   "import sys; sys.path.insert(0, '08-tooling'); import MODULE as K; K.name()" (the form the data-module research uses for a claim recomputed from the chapter's library) is shown and run as
#   the call "K.name()" (the page's Python worker imports the chapter's library from the wheel it unpacks at boot and makes K, L and C available to every program, pywheels_v*.json), its result is computed here by running the statement in the
#   repository under the given interpreter, and its parse tree is built from the call. (c) standin_v*.json (as in SEN0414 page data 2.14.0) names the concepts whose example needs a file a browser does not have
#   (the saved sources, the record of Bitcoin Core's run): the example is removed from the concept and its recorded output is added as a paragraph headed "Recorded, not run on this page", with the reason;
#   "notice" is shown at the top of the Overview and "markers"/"note" put a note above matching examples (template 9.45.0). (d) pywheels_v*.json: wheels are read from 03-materials/chNN/assets, checked against
#   their SHA-256 and embedded as hex in data["py_wheels"]; "boot_python" runs once after the wheels (data["py_boot"]). Nothing else changed.
# 2.11.0 (over 2.10.0), the owner's ruling of 2026-10-07 14:46 - a paragraph gets the diagram its narrative calls for,
#   and the mapping is kept in the CME ontology for reuse. (a) Reads course_page_config_v2_10_0.json (materials 1.4.8;
#   corpus.standards names the two CME mapping files with their digests). (b) The CME mapping is parsed from the CME
#   checkout (CME_REPO, default /home/claude/cme) and refused if a file's bytes differ from the recorded digest; the
#   page gets it as data["diagram_map"] - per narrative pattern its label, question, cue phrases, suggested diagram
#   types and the first type's notation. (c) The newest 08-tooling/sen0401_chNN_diagrams_v*.py is imported, its
#   run_checks(nodes, mapping) must pass (structure, grounding of every label in the concepts' explanations at 0.8 or
#   better, pattern known to the mapping), the diagram type is ASSIGNED from the mapping (never authored), and the
#   diagrams go under data["ndiag"]. (d) The same diagrams are written as cme:NarrativeDiagram individuals into a
#   Turtle block (data["ndiag_abox"], named sen0401_chNN_diagrams_abox_v<module version>.ttl) that the page build
#   embeds, so the page's own corpus states which pattern each diagram was recognised as and which passage it was
#   read from. The block is not written as a file: BP-D54 counts every Turtle file of the package against the
#   course's recorded ceiling (34 A files), and five more would be refused; the authored module and the page carry it.
# 2.10.0 (over 2.9.0): reads course_page_config_v2_9_0.json (materials register 1.4.7). No other change.
# 2.9.0 (over 2.8.0): reads course_page_config_v2_8_0.json (materials register 1.4.6). No other change.
# 2.8.0 (over 2.7.0): reads course_page_config_v2_7_0.json (materials register 1.4.5). No other change.
# 2.7.0 (over 2.6.0): two changes for the owner's two-fold rule (2026-10-06 13:42) - the decks and the pages carry
#   one look and one story discipline. (a) Reads course_page_config_v2_6_0.json (the re-provisioned exam key;
#   course_page_config_build_v2_6_0.py records why). (b) The chapter's 5N1K story companion joins the page data:
#   the newest 08-tooling/sen0401_chNN_stories_v*.py is imported, its OWN run_checks() must pass (the same gate the
#   deck build runs), and every story ships with its fields verbatim - title, when, who, where, link, story, lesson,
#   source, concepts - under data["stories"]. Photographs come from the chapter's existing deck assets through the
#   chapter's stories_img_v*.json mapping (file + credit per story, taken from the deck's own placements and
#   ASSETS_PROVENANCE); each is downscaled with Pillow (640px wide alone, 420px in a strip) and embedded as a data
#   URI so the page stays one self-contained file, with width, height and the credit carried beside the bytes. A
#   mapped file that does not exist stops the build; a story without a mapping simply has no photograph. A named
#   unit (the numbers page) has no story companion and gets no stories key.
# 2.6.0 (over 2.5.0): reads course_page_config_v2_5_0.json, which resolves the book package in its own
#   repository, altunelyusuf/mastering-bitcoin, at folder 3e, rather than in the Ontologies monorepo. No other
#   change: the same concepts, relations, agents, findings and references are extracted from the same chapter
#   ontology files, and the configuration is still read whole and carried into the page data unchanged.
# 2.5.0 (over 2.4.0): reads course_page_config_v2_4_0.json, which pins the book package at its 0.9.1 release and names each chapter's newest part. No other change.
# 2.4.0 (over 2.3.0): reads course_page_config_v2_4_0.json, which adds the course-learning-outcomes SPARQL sample. No other change.
# 2.3.0 (over 2.2.0): reads course_page_config_v2_4_0.json instead of course_page_config_v2_1_0.json - the only change.
# That configuration is the one that names the book ontology of each chapter (the corpus 2.1.0 wrongly declared empty),
# so the page data must carry it for the page build to find data.course.corpus.book. Nothing else in this step changes:
# the same concepts, relations, agents, findings and references are extracted from the same chapter ontology files.
# 2.2.0 (over 2.1.0; brings in what SEN0414's page data 2.5.0 has, for template 9.24.0): a document section may be several paragraphs, each opening with the
# question it answers ('What it is: ...'); the node keeps them as `paras` ([{facet, text}]) and its `body` is the first paragraph without the facet; the co-mention
# relations read all the paragraphs. The visuals file is the newest visuals_v*.json of the unit, a chapter may replace the course's playground program with
# playground_v*.json, and may carry resources_v*.json and lecture_v*.json (D.resources, D.resources_checked, D.lecture). Reads course_page_config_v2_1_0.json
# (exam identity, Code Lab / SPARQL / Step-through / Playground content for template 9.24.0). Named units (the numbers page) and chart canvases build as in 2.1.0.
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); from sen0401_plain_code_v1_0_0 import plain as _plain
PV = os.environ.get("PAGE_VER", "9_24_0")  # generated files carry the version of the page they were produced for
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
G = {}
if len(sys.argv) > 2: exec(sys.argv[2], G)
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
# 2.13.0: a worked example may be statements ending in an expression (x = ...; (x, ...)): the statements run first and the tree, the result and the steps are those of the closing expression
try: _mod = ast.parse(expr)
except SyntaxError as _e:
    print(json.dumps({"out": "SyntaxError: %s" % _e.msg, "tree": {"label": "SyntaxError", "kind": "SyntaxError", "children": []}, "steps": []})); sys.exit(0)
if _mod.body and isinstance(_mod.body[-1], ast.Expr) and len(_mod.body) > 1:
    _last = _mod.body.pop().value; _pre = _mod
    t = _last; expr = ast.unparse(_last)
    try:
        exec(compile(_pre, "<example>", "exec"), G)
        out = repr(eval(compile(ast.Expression(_last), "<example>", "eval"), G))
    except Exception as e: out = "%s: %s" % (type(e).__name__, e)
    t = _last
else:
    t = ast.parse(expr, mode="eval").body
    try: out = repr(eval(expr, G))
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
    for _ in range(0 if len(_mod.body) > 1 else 40):
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
def ex(expr, prelude=None):
    r = subprocess.run([PY, "-c", EXEC, expr] + ([prelude] if prelude else []), capture_output=True, text=True, timeout=120, cwd=REPO)
    return json.loads(r.stdout)
PRE9 = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch09_lib_v1_0_0 as L; R = L.run(); R2 = L.run2(); C = L.census(); "   # 2.13.0: chapter 9's examples all begin with this line
PRE10 = "import sys; sys.path.insert(0, '08-tooling'); import sen0401_ch10_lib_v1_0_0 as L; import sen0401_ch10_p2p_v1_0_0 as P; R = L.run(); "
PRE11 = "import sys, hashlib, datetime; sys.path.insert(0, '08-tooling'); import sen0401_ch11_lib_v1_0_0 as L; R = L.run(); "
PRE12 = "import sys, math, hashlib, datetime; sys.path.insert(0, '08-tooling'); import sen0401_ch12_lib_v1_0_0 as L; R = L.run(); "
PRE13 = "import sys, math, hashlib, datetime; sys.path.insert(0, '08-tooling'); import sen0401_ch13_lib_v1_0_0 as L; R = L.run(); "
PRE14 = "import sys, math, hashlib, datetime; sys.path.insert(0, '08-tooling'); import sen0401_ch14_lib_v1_0_0 as L; R = L.run(); "
PRE_LINES = {"ch09": PRE9, "ch10": PRE10, "ch11": PRE11, "ch12": PRE12, "ch13": PRE13, "ch14": PRE14}
_LIB = re.compile(r"^import sys; sys\.path\.insert\(0, '08-tooling'\); import (\w+) as K; (K\.\w+\(\))$")
def libform(e):
    """the chapter-library form of a worked example: (call shown and run in the page, prelude that makes the call computable here), or None"""
    for _pre in PRE_LINES.values():
        if e.startswith(_pre): return e[len(_pre):], _pre.replace("; ", "\n"), e[len(_pre):]
    m = _LIB.match(e)
    if not m: return None
    return m.group(2), "import sys; sys.path.insert(0, '08-tooling')\nimport sen0401_ch07_script_lib_v1_0_0 as L, sen0401_%s_sig_lib_v1_0_0 as C\nimport %s as K" % (N, m.group(1)), m.group(2)

label = lambda c: str(T.value(c, RDFS.label))
classes = list(T.subjects(RDF.type, OWL.Class))
parent = {str(c): str(T.value(c, RDFS.subClassOf)) if T.value(c, RDFS.subClassOf) else None for c in classes}
secs = {str(D.value(s, DC.source)): s for s in D.subjects(DOC.sectionTitle, None)}
order = sorted(classes, key=lambda c: int(D.value(secs[str(c)], DOC.sectionOrder)))
FACETS = ("What it is", "Why it matters", "Where you meet it", "How it works", "What changed", "Watch out")
def PARAS(t):
    out = []
    for p in t.split("\n\n"):
        m = re.match(r"^(%s): (.*)$" % "|".join(FACETS), p, re.S)
        out.append({"facet": m.group(1), "text": m.group(2)} if m else {"facet": "", "text": p})
    return out
nodes = []
for c in order:
    s = secs[str(c)]; cid = str(c).split("#")[-1]
    X = next((x for x in A.subjects(RDF.type, c) if str(x).split("#")[-1].startswith("X_")), None)
    node = {"id": cid, "label": label(c), "level": int(D.value(s, DOC.hierarchyLevel)), "parent": parent[str(c)].split("#")[-1] if parent[str(c)] else None,
            "body": PARAS(str(D.value(s, SK.definition)))[0]["text"], "paras": PARAS(str(D.value(s, SK.definition))) if "\n\n" in str(D.value(s, SK.definition)) else [], "section_iri": str(s), "class_iri": str(c)}
    if X is not None:
        node["example"] = str(A.value(X, RDFS.label)); node["definition"] = str(A.value(X, SK.definition))
        io = A.value(X, RDN.hasIOExample)
        if io is not None:
            e = str(A.value(io, CH.input)); lf = libform(e)
            if lf: r, e = ex(lf[0], lf[1]), lf[2]
            else:
                if os.environ.get("PLAIN_CODE") == "1" and "lambda" in e:
                    _e0 = e; e = _plain(e); r = ex(e); _r0 = ex(_e0)
                    if r["out"] != _r0["out"]: raise SystemExit("plain rewrite of %s changes the result: %r -> %r" % (cid, _r0["out"][:80], r["out"][:80]))
                    print("plain code:", cid, "(same result)")
                else: r = ex(e)
            if r["out"].startswith("SyntaxError"): r["out"] = str(A.value(io, CH.output))   # the ontology's text of this example is not valid Python (a quote was rewritten): its recorded output is the ontology's
            node["io"] = {"code": e, "out": r["out"], "tree": r["tree"], "steps": r.get("steps", [])}
        er = A.value(X, RDN.hasErrorCondition)
        if er is not None:
            e = str(A.value(er, RDFS.label)).split(" raises ")[0]
            if os.environ.get("PLAIN_CODE") == "1" and "lambda" in e:
                _e0 = e; e = _plain(e)
                if ex(e)["out"] != ex(_e0)["out"]: raise SystemExit("plain rewrite of the error example of %s changes the result" % cid)
                print("plain code (error example):", cid, "(same result)")
            node["error"] = {"code": e, "out": ex(e)["out"]}
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
# 2.23.0: the section links of the research, read as page relations
KB = rdflib.Namespace("http://example.org/knowledge-base#")
_cat = {p: o for p, o in T.subject_objects(KB.hasRelationshipCategory)}
_cat = {p: o for p, o in _cat.items() if (p, RDF.type, OWL.ObjectProperty) in T and p != CH.hasOwner}
_sec_of = lambda x: next((str(t).split("#")[-1] for t in A.objects(x, RDF.type) if str(t).split("#")[-1] in ids), None)
_sentence = {}
for ax in A.subjects(RDF.type, OWL.Axiom):
    _k = (A.value(ax, OWL.annotatedSource), A.value(ax, OWL.annotatedProperty), A.value(ax, OWL.annotatedTarget))
    _c = A.value(ax, RDFS.comment)
    if _c is not None: _sentence[_k] = str(_c)
_seen = set(); _links = []
for p, cat in sorted(_cat.items(), key=lambda x: str(x[0])):
    for s_, o_ in sorted(set(A.subject_objects(p)), key=lambda x: (str(x[0]), str(x[1]))):
        a, b = _sec_of(s_), _sec_of(o_)
        if a and b and a != b and (a, b, str(p)) not in _seen:
            _seen.add((a, b, str(p))); _links.append((a, b, p, cat, _sentence.get((s_, p, o_))))
    for s_, o_ in sorted(set(T.subject_objects(p)), key=lambda x: (str(x[0]), str(x[1]))):
        a, b = str(s_).split("#")[-1], str(o_).split("#")[-1]
        if a in ids and b in ids and a != b and (a, b, str(p)) not in _seen:
            _seen.add((a, b, str(p))); _links.append((a, b, p, cat, None))
for a, b, p, cat, snt in _links:
    rels.append({"source": a, "target": b, "type": "operates on", "evidence": "%s (%s, a relationship of category %s) in the chapter's research: %s" % (
        str(T.value(p, RDFS.label)), str(p).split("#")[-1], str(cat).split("RelationshipCategory_")[-1], snt if snt else "the link carries no sentence")})
for n in nodes:
    if n["level"] < 3: continue
    for m in nodes:
        if m is n or m["level"] < 3 or m["parent"] == n["parent"]: continue
        if re.search(r"\b%s\b" % re.escape(m["label"].lower()), " ".join([p["text"] for p in n["paras"]] if n["paras"] else [n["body"]]).lower()):
            rels.append({"source": n["id"], "target": m["id"], "type": "mentions", "evidence": "the document's section on %s names %s" % (n["label"], m["label"])})
# Subjects and their agents: one per second-level subject, named for what it covers.
AGENT = {"Unit": "Units agent", "Supply": "Supply agent", "Price": "Price agent", "Consensus": "Consensus agent", "History": "History agent", "WalletPlatform": "Wallet agent", "NodeType": "Node agent", "KeyControl": "Keys agent", "Backup": "Recovery agent", "Address": "Address agent", "Transfer": "Payments agent", "SemanticBridge": "Semantic web agent", "NumericValue": "Numbers agent", "TextValue": "Text agent", "ArithmeticOperation": "Arithmetic agent", "TextOperation": "String agent",
         "BindingOperation": "Variables agent", "IOFunction": "Input-output agent", "ConversionFunction": "Conversion agent", "MeasurementFunction": "Measurement agent",
         "InteractiveEnvironment": "Shell agent", "InterpreterBuild": "Interpreter agent", "StringFormatting": "Formatting agent", "Tooling": "Tooling agent",
         "TruthValue": "Truth agent", "EqualityComparison": "Equality agent", "OrderingComparison": "Ordering agent", "LogicalOperator": "Logic agent",
         "Evaluation": "Evaluation agent", "ControlStructure": "Structure agent", "Branching": "Branching agent", "ExpressionForm": "Expression agent",
         "PatternMatching": "Matching agent", "Style": "Style agent"}
AGENT["LockTimeDefense"] = "Lock time defense agent"
AGENT["Spv"] = "SPV agent"   # 2.14.0: chapter 10's label "Simplified payment verification (SPV)" would make a 43-character name   # 2.13.0: the label is 37 characters, the name made from it would be 43 (the agent roster keeps a name on one row, the page test checks it)
agents = [{"id": "agent-" + n["id"], "name": AGENT.get(n["id"], n["label"] + " agent"), "subject": n["id"],
           "covers": [m["id"] for m in nodes if m["parent"] == n["id"]] + [n["id"]]} for n in nodes if n["level"] == 2]
refs = sorted((str(R.value(p, RDFS.label)), str(R.value(p, DC.source))) for p in R.subjects(RDF.type, RES.Publication))
title = next(str(o) for s, o in D.subject_objects(RDFS.label) if str(s).endswith("#Document"))
DISC = os.path.join(REPO, "08-tooling", "%s-page" % N, "discussion_v1_0_0.json")
EXTRA = os.path.join(REPO, "08-tooling", "%s-page" % N, "extra_v1_1_0.html")
data_extra = open(EXTRA).read() if os.path.exists(EXTRA) else ""
SEN = rdflib.Namespace("http://example.org/sen0401#")
findings = sorted(((str(R.value(f, RDFS.label)), str(R.value(f, SEN.findingText))) for f in R.subjects(RDF.type, SEN.Finding)), key=lambda x: x[0])
COURSE = json.load(open(os.path.join(REPO, "08-tooling", "course_page_config_v2_16_0.json")))
PIN = dict(x.split("=") for x in os.environ.get("SEN0401_PIN", "").split(",") if x)
def _versions(pat):
    fs = sorted(glob.glob(os.path.join(REPO, "08-tooling", "%s-page" % N, pat)), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
    k = pat.split("_v")[0]
    return [f for f in fs if f.endswith("_v%s.json" % PIN[k])] if k in PIN else fs
# 2.13.0: the Code Lab snippet "Re-run every example on this page" evaluated a code with eval(); a code of several statements ending in an expression needs the statements run first, so the snippet runs the statements and evaluates the closing expression (a single expression behaves as before)
for _i, _sn in enumerate(COURSE["codelab_snippets"]):
    if _sn[0] == "Re-run every example on this page":
        COURSE["codelab_snippets"][_i] = [_sn[0], "import ast\ndef run(code):\n    t = ast.parse(code)\n    last = ast.Expression(t.body.pop().value)\n    ns = {}\n    exec(compile(t, '<example>', 'exec'), ns)\n    return eval(compile(last, '<example>', 'eval'), ns)\nfor n in PAGE['nodes']:\n    if n.get('io'):\n        got = repr(run(n['io']['code']))\n        print('same' if got == n['io']['out'] else 'DIFFERENT', '|', n['label'], '|', n['io']['code'], '->', got)"]
_vf = _versions("visuals_v*.json"); VIS = _vf[-1] if _vf else ""
_pf = _versions("playground_v*.json")
if _pf: COURSE["playground"] = {k: v for k, v in json.load(open(_pf[-1])).items() if not k.startswith("_")}
newest = lambda pat: (lambda fs: json.load(open(fs[-1])) if fs else None)(_versions(pat))
_res = newest("resources_v*.json"); _lec = newest("lecture_v*.json")
# ---- 2.7.0: the chapter's 5N1K stories, checked by their own module, photos from the deck's assets --------------
STORIES = None
if NUM is not None and NUM.isdigit():
    _sf = sorted(glob.glob(os.path.join(REPO, "08-tooling", "sen0401_%s_stories_v*.py" % N)),
                 key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-3].split("_")])
    if "stories" in PIN: _sf = [f for f in _sf if f.endswith("_v%s.py" % PIN["stories"])]
    if _sf:
        import base64, io, importlib.util
        from PIL import Image
        spec = importlib.util.spec_from_file_location("stories_mod", _sf[-1]); _sm = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_sm)
        _bad = _sm.run_checks()
        if _bad: raise SystemExit("story companion %s fails its own checks: %s" % (os.path.basename(_sf[-1]), _bad))
        _imap = {}
        _if = _versions("stories_img_v*.json")
        if _if: _imap = {k: v for k, v in json.load(open(_if[-1])).items() if not k.startswith("_")}
        ADIR = os.path.join(REPO, "03-materials", N, "assets")
        def _embed(fn, maxw):
            fp = os.path.join(ADIR, fn)
            if not os.path.exists(fp): raise SystemExit("stories_img maps %s, which is not in %s" % (fn, ADIR))
            im = Image.open(fp); im.load()
            if im.width > maxw: im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            if fn.lower().endswith(".png"): im.save(buf, "PNG", optimize=True); mime = "image/png"
            else: im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True); mime = "image/jpeg"
            return {"data": "data:%s;base64,%s" % (mime, base64.b64encode(buf.getvalue()).decode()), "w": im.width, "h": im.height}
        STORIES = []
        for s in _sm.STORIES:
            e = {k: s[k] for k in ("id", "title", "when", "who", "where", "link", "story", "lesson", "source")}
            if s.get("linkLabel"): e["linkLabel"] = s["linkLabel"]
            e["concepts"] = list(s.get("concepts", []))
            pics = _imap.get(s["id"], [])
            e["imgs"] = [dict(_embed(p["file"], 640 if len(pics) == 1 else 420), credit=p["credit"], file=p["file"]) for p in pics]
            STORIES.append(e)
        print("stories: %d from %s (%d with photographs, %d photographs embedded)" % (
            len(STORIES), os.path.basename(_sf[-1]), sum(1 for e in STORIES if e["imgs"]), sum(len(e["imgs"]) for e in STORIES)))
# ---- 2.11.0: the CME narrative-to-diagram mapping, and the chapter's authored diagrams typed by it ----------------
import hashlib
CME_REPO = os.environ.get("CME_REPO", "/home/claude/cme")
CMEN = rdflib.Namespace("http://example.org/cme#")
MAPG = rdflib.Graph()
for st in COURSE["corpus"].get("standards", []):
    fp = os.path.join(CME_REPO, st["folder"], st["path"]); b = open(fp, "rb").read()
    if hashlib.sha256(b).hexdigest() != st["sha256"]:
        raise SystemExit("the CME standard %s at %s does not match the digest recorded in the configuration; re-run course_page_config_build" % (st["path"], fp))
    MAPG.parse(data=b.decode(), format="turtle")
def _lab(s): return str(MAPG.value(s, RDFS.label) or "")
DMAP = {}
for p in MAPG.subjects(RDF.type, CMEN.NarrativePattern):
    types = [str(t).split("#")[1] for t in MAPG.objects(p, CMEN.suggestsDiagram)]
    DMAP[str(p).split("#")[1]] = {"label": _lab(p), "question": str(MAPG.value(p, CMEN.answersQuestion) or ""), "cues": sorted(str(c) for c in MAPG.objects(p, CMEN.cuePhrase)),
                                   "types": types, "notation": str(MAPG.value(CMEN[types[0]], CMEN.notation) or "") if types else "", "renderer": str(MAPG.value(CMEN[types[0]], CMEN.renderer) or "") if types else ""}
NDIAG = None; NDIAG_ABOX = None
if NUM is not None and NUM.isdigit():
    _df = sorted(glob.glob(os.path.join(REPO, "08-tooling", "sen0401_%s_diagrams_v*.py" % N)), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-3].split("_")])
    if _df:
        import importlib.util
        spec = importlib.util.spec_from_file_location("diagrams_mod", _df[-1]); _dm = importlib.util.module_from_spec(spec); spec.loader.exec_module(_dm)
        _bad = _dm.run_checks(nodes, DMAP)
        if _bad: raise SystemExit("diagram companion %s fails its checks: %s" % (os.path.basename(_df[-1]), _bad))
        NDIAG = [{k: d[k] for k in ("id", "pattern", "type", "title", "concepts", "read_from", "why", "data", "grounding")} for d in _dm.DIAGRAMS]
        # the diagrams as individuals of the CME vocabulary, beside the page
        def _tl(s): return '"' + s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ") + '"'
        ab = ["@prefix cme: <http://example.org/cme#> .", "@prefix chx: <http://example.org/sen0401/%s#> .", "@prefix owl: <http://www.w3.org/2002/07/owl#> .", "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .", "@prefix dcterms: <http://purl.org/dc/terms/> .", "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .", "",
              "<http://example.org/sen0401/%s/diagrams> a owl:Ontology ; rdfs:label \"SEN0401 %s narrative diagrams - ABox\"@en ; owl:versionInfo \"%s\" ; dcterms:identifier \"sen0401_%s_diagrams_abox_v%s\" ;" % (N, N, _dm.__version__, N, _dm.__version__.replace(".", "_")),
              "    rdfs:comment \"The chapter's authored diagrams as cme:NarrativeDiagram individuals: generated by sen0401_page_data_v2_11_0.py from sen0401_%s_diagrams_v%s.py, typed by the CME narrative-to-diagram mapping (a module of cme_standards_adoption_v1_3_0.ttl, CME 0.16.0).\"@en ; owl:imports <http://example.org/cme/narrative-diagram> ." % (N, _dm.__version__.replace(".", "_")), ""]
        ab[1] = ab[1] % N
        for d in NDIAG:
            ab.append("chx:Diagram_%s a cme:NarrativeDiagram ; rdfs:label %s@en ; cme:hasPattern cme:%s ; cme:hasDiagramType cme:%s ; cme:readFrom %s ; cme:elementCount %d ;" % (d["id"], _tl(d["title"]), d["pattern"], d["type"], _tl(d["read_from"]), len(_dm._labels(d))))
            ab.append("    " + " ; ".join("cme:accompanies %s" % _tl(c) for c in d["concepts"]) + " ; rdfs:comment %s@en ." % _tl(d["why"]))
        _abn = "sen0401_%s_diagrams_abox_v%s.ttl" % (N, _dm.__version__.replace(".", "_"))
        _abt = "\n".join(ab) + "\n"
        rdflib.Graph().parse(data=_abt, format="turtle")
        NDIAG_ABOX = {"name": _abn, "text": _abt}
        print("diagrams: %d from %s (%s), grounding %s; ABox block %s (embedded in the page, not a file: BP-D54 counts every Turtle file of the package, and the course's A-file ceiling is 34)" % (len(NDIAG), os.path.basename(_df[-1]), ", ".join("%s->%s" % (d["pattern"], d["type"]) for d in NDIAG), " ".join("%d/%d" % tuple(d["grounding"]) for d in NDIAG), _abn))
data = {"_version": PV.replace("_", "."), "visuals": {k: v for k, v in (json.load(open(VIS)) if os.path.exists(VIS) else {}).items() if not k.startswith("_")}, "course": COURSE, "discussion": (lambda x: x["items"] if isinstance(x, dict) else x)(json.load(open(DISC))) if os.path.exists(DISC) else [], "research_file": os.path.basename(f("research")), "chapter": int(NUM) if NUM.isdigit() else None, "unit": json.load(open(os.path.join(REPO, "08-tooling", "%s-page" % N, "unit_v1_0_0.json"))) if not NUM.isdigit() else None, "title": title, "python": pyver, "nodes": nodes, "relations": rels, "agents": agents, "findings": findings, "refs": refs}
_pw = newest("pywheels_v*.json")
if _pw:
    import hashlib as _h
    data["py_wheels"] = []
    for w in _pw["wheels"]:
        b = open(os.path.join(REPO, "03-materials", N, "assets", w["file"]), "rb").read()
        if _h.sha256(b).hexdigest() != w["sha256"]: raise SystemExit("wheel %s does not match its recorded SHA-256" % w["file"])
        data["py_wheels"].append({"name": w["file"], "hex": b.hex()})
    print("wheels: %s" % ", ".join(w["name"] for w in data["py_wheels"]))
    if _pw.get("boot_python"): data["py_boot"] = _pw["boot_python"]
    if _pw.get("pyodide_packages"): data["py_packages"] = list(_pw["pyodide_packages"])
_so = newest("standin_v*.json")
if _so:
    _k = 0
    for _n in nodes:
        if "io" in _n and any(_m in _n["io"]["code"] for _m in _so["markers"]): _n["io"]["note"] = _so["note"]; _k += 1
    if _so.get("notice"): data["notice"] = _so["notice"]
    for _id, _why in (_so.get("recorded") or {}).items():
        _n = next(x for x in nodes if x["id"] == _id)
        if "io" not in _n: raise SystemExit("recorded concept %s has no example" % _id)
        _t = "%s Recorded output, produced when the chapter was built under %s and not in your browser: %s" % (_why, data["python"], _n["io"]["out"])
        if _n["paras"]: _n["paras"].append({"facet": "Recorded, not run on this page", "text": _t})
        else: _n["body"] = _n["body"] + " " + _t
        del _n["io"]
    print("recorded, no runnable example: %d; examples that run in the browser: %d" % (len(_so.get("recorded") or {}), sum(1 for n in nodes if "io" in n)))
if STORIES is not None: data["stories"] = STORIES
data["diagram_map"] = DMAP
if NDIAG is not None: data["ndiag"] = NDIAG; data["ndiag_abox"] = NDIAG_ABOX
if _res: data["resources"] = _res["links"]; data["resources_checked"] = _res["checked"]
if _lec: data["lecture"] = _lec["slides"]
def _cc_manifest():
    """the deck's chapter-code manifest, validated and normalised, or None when the chapter has none"""
    f = os.environ.get("CC_MANIFEST") or ""
    if not f:
        fs = sorted(glob.glob(os.path.join(REPO, "03-materials", N, "page", "chapter_code_%s_v*.json" % N)), key=lambda x: [int(v) for v in x.rsplit("_v", 1)[1][:-5].split("_")])
        f = fs[-1] if fs else ""
    if not f: return None
    raw = json.load(open(f)); items = raw.get("examples", raw.get("items")) if isinstance(raw, dict) else raw
    if not isinstance(items, list) or not items: raise SystemExit("chapter-code manifest %s holds no list of examples" % f)
    pick = lambda it, *ks: next((it[k] for k in ks if k in it and it[k] is not None), None)
    out, seen_o, seen_n = [], set(), set()
    for i, it in enumerate(items):
        o = pick(it, "order", "n"); o = i + 1 if o is None else int(o)
        nm = str(pick(it, "name", "title") or "").strip(); code = pick(it, "code")
        if not nm: raise SystemExit("chapter-code manifest %s: example %d has no name" % (f, i + 1))
        if not isinstance(code, str) or not code.strip(): raise SystemExit("chapter-code manifest %s: example %r has no code" % (f, nm))
        if o in seen_o or (out and o < out[-1]["order"]): raise SystemExit("chapter-code manifest %s: order %d repeats or runs backwards at %r" % (f, o, nm))
        if nm.lower() in seen_n: raise SystemExit("chapter-code manifest %s: the name %r repeats" % (f, nm))
        seen_o.add(o); seen_n.add(nm.lower())
        e = {"order": o, "name": nm, "code": code}
        for k, ks in (("slide", ("slide", "slide_no")), ("expected", ("expected", "expected_result", "result", "output")), ("note", ("note", "explain", "explanation")), ("viz", ("viz",))):
            v = pick(it, *ks)
            if v is not None: e[k] = v if k == "slide" else str(v)
        out.append(e)
    return {"file": os.path.relpath(f, REPO), "version": (raw.get("_version") if isinstance(raw, dict) else None) or os.path.basename(f).rsplit("_v", 1)[1][:-5].replace("_", "."), "examples": out}
_cc = _cc_manifest()
if _cc: data["chaptercode"] = _cc; print("chapter code: %d examples from %s" % (len(_cc["examples"]), _cc["file"]))
else: print("chapter code: no manifest file for %s, so the page has no chapter-code tab" % N)
data["panels"] = {m["id"]: [n["id"] for n in nodes if n["parent"] == m["id"]] for m in nodes if m["level"] == 2}
print("panels: %d groups, %d concept panels (one concept each; the template adds the group and subject panels)" % (len(data["panels"]), sum(len(v) for v in data["panels"].values())))
out = os.environ.get("PAGE_DATA_OUT") or os.path.join(REPO, "08-tooling", "%s-page" % N); os.makedirs(out, exist_ok=True)
json.dump(data, open(os.path.join(out, "page_data_v%s.json" % PV), "w"), indent=1)
open(os.path.join(out, "extra_resolved_v%s.html" % PV), "w").write(data_extra)
print("chapter %s: %d concepts, %d relations (%d stated, %d co-mentions), %d agents, %d executed examples with ast trees, under %s" % (
    N, len(nodes), len(rels), sum(1 for r in rels if r["type"] != "mentions"), sum(1 for r in rels if r["type"] == "mentions"),
    len(agents), sum(1 for n in nodes if "io" in n), pyver))
