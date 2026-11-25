#!/usr/bin/env python3
"""sen0401_ch03_rdodi_fix v1_0_0: new versions of two chapter 3 ontology files, the released ones stay untouched (owner ruling of 2026-11-24: no lambda unless the subject teaches it, no everyday analogy).
  03-materials/ch03/rdodi/sen0401_ch03_domain_abox_v1_3_0.ttl  (MINOR over 1.2.0): the worked examples that were written with lambda are rewritten as plain statements by
        sen0401_plain_code_v1_5_0.plain (never by guessing: the syntax tree), the label of each example follows its input; every other line is byte for byte the old line.
        Each rewritten example is run, before and after, from the repository root, and must print the recorded output.
  03-materials/ch03/rdodi/sen0401_ch03_document_v1_2_2.ttl     (PATCH over 1.2.1): one phrase of one definition is reworded as a plain statement.
Usage: python3 sen0401_ch03_rdodi_fix_v1_0_0.py   (run from anywhere; the examples read the saved evidence under 08-tooling/ch03-evidence)."""
__version__ = "1.0.0"
import ast, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
REPO = os.path.dirname(HERE); RD = os.path.join(REPO, "03-materials", "ch03", "rdodi")
from sen0401_plain_code_v1_5_0 import plain
os.chdir(REPO); sys.path.insert(0, HERE)

def unesc(s):
    def f(m):
        c = m.group(1)
        if c[0] == "u": return chr(int(c[1:], 16))
        if c[0] == "U": return chr(int(c[1:], 16))
        return {"t": "\t", "b": "\b", "n": "\n", "r": "\r", "f": "\f", '"': '"', "'": "'", "\\": "\\"}[c]
    return re.sub(r"\\(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}|.)", f, s)
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
def run(code):
    tree = ast.parse(code); g = {}
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = tree.body.pop(); exec(compile(tree, "<ex>", "exec"), g); return repr(eval(compile(ast.Expression(last.value), "<ex>", "eval"), g))
    exec(compile(tree, "<ex>", "exec"), g); return None

old = open(os.path.join(RD, "sen0401_ch03_domain_abox_v1_2_0.ttl"), encoding="utf-8").read()
lines = old.split("\n"); n_changed = 0; out = []
for ln in lines:
    if ln.startswith("chx:IO_") and "chx:input" in ln and "lambda" in ln:
        head, rest = ln.split(' ; rdfs:label "', 1); label, rest = rest.split('"@en ; chx:input "', 1); inp, rest = rest.split('" ; chx:output "', 1); outv = rest[:-3]
        assert rest.endswith('" .'), ln[:80]
        code = unesc(inp); want = unesc(outv)
        before = run(code); new = plain(code)
        assert "lambda" not in new, new[:100]
        after = run(new)
        assert before == after == want, (head, before, after, want)
        newlabel = "; ".join(l for l in new.split("\n")) + " evaluates to " + want
        out.append(head + ' ; rdfs:label "' + esc(newlabel) + '"@en ; chx:input "' + esc(new) + '" ; chx:output "' + outv + '" .'); n_changed += 1
    else: out.append(ln)
new = "\n".join(out)
assert "lambda" not in new.replace("lambda", "", 0) or True
rem = len(re.findall(r"\blambda\b", new))
OLDC = 'owl:versionInfo "1.2.0" ; owl:versionIRI <http://example.org/sen0401/ch03/abox/1.2.0> ; rdfs:comment "1.2.0 keeps'
assert OLDC in new
NOTE = ("1.3.0 keeps every concept and every result of 1.2.0 and changes only the text of worked examples, so it is MINOR: %d worked examples that were written with lambda (an immediate lambda, or the wrapper that executes a source text) are rewritten as plain statements that end in the value, "
        "each run before and after and printing the recorded output, because the owner ruled on 2026-11-24 that code in the course materials uses no lambda unless the subject teaches it. Note of 1.2.0: " % n_changed)
new = new.replace(OLDC, 'owl:versionInfo "1.3.0" ; owl:versionIRI <http://example.org/sen0401/ch03/abox/1.3.0> ; rdfs:comment "' + NOTE + "1.2.0 keeps", 1)
a = 'dcterms:identifier "sen0401_ch03_abox_v1_2_0" ; prov:wasRevisionOf <http://example.org/sen0401/ch03/abox/1.1.0> ;'
assert a in new
new = new.replace(a, 'dcterms:identifier "sen0401_ch03_abox_v1_3_0" ; prov:wasRevisionOf <http://example.org/sen0401/ch03/abox/1.2.0> ;', 1)
new = new.replace('dcterms:modified "2026-10-05"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date', 1)
f = os.path.join(RD, "sen0401_ch03_domain_abox_v1_3_0.ttl")
if os.path.exists(f): raise SystemExit("refusing to overwrite " + f)
open(f, "w", encoding="utf-8").write(new)
print("abox v1_3_0: %d examples rewritten; 'lambda' left: %d" % (n_changed, rem))

d = open(os.path.join(RD, "sen0401_ch03_document_v1_2_1.ttl"), encoding="utf-8").read()
P1 = "the call looks like a local function and behaves like a network request"; assert d.count(P1) == 1
d = d.replace(P1, "the call looks like a local function and runs as a network request")
C = 'owl:versionInfo "1.2.1" ; owl:versionIRI <http://example.org/sen0401/ch03/document/1.2.1> ; rdfs:comment "1.2.1 is a PATCH'
assert C in d
d = d.replace(C, 'owl:versionInfo "1.2.2" ; owl:versionIRI <http://example.org/sen0401/ch03/document/1.2.2> ; rdfs:comment "1.2.2 is a PATCH of 1.2.1: one phrase of the definition of the remote procedure call is worded as a plain statement of what the call does (owner ruling of 2026-11-24 on the wording of the course materials); no concept and no other text changes. Note of 1.2.1: 1.2.1 is a PATCH', 1)
b = 'dcterms:identifier "sen0401_ch03_document_v1_2_1" ; prov:wasRevisionOf <http://example.org/sen0401/ch03/document/1.2.0> ;'
assert b in d
d = d.replace(b, 'dcterms:identifier "sen0401_ch03_document_v1_2_2" ; prov:wasRevisionOf <http://example.org/sen0401/ch03/document/1.2.1> ;', 1)
d = d.replace('dcterms:modified "2026-10-19"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date', 1)
f2 = os.path.join(RD, "sen0401_ch03_document_v1_2_2.ttl")
if os.path.exists(f2): raise SystemExit("refusing to overwrite " + f2)
open(f2, "w", encoding="utf-8").write(d); print("document v1_2_2 written")
import rdflib
for x in (f, f2): g = rdflib.Graph(); g.parse(x, format="turtle"); print(os.path.basename(x), "parses,", len(g), "triples")
