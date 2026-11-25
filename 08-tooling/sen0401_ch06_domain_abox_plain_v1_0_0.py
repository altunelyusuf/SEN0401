#!/usr/bin/env python3
"""Chapter 6 domain ABox v1.0.0 -> v1.1.0 (owner's ruling 'no lambda unless the subject teaches lambda'): every rd:IOExample input and every rd:ErrorCondition label that holds a lambda is rewritten
by sen0401_plain_code_v1_5_0.plain() as plain statements; each rewritten example is executed here and must give its stated output (an ErrorCondition must raise its stated error). The label of an IOExample stays
'INPUT evaluates to OUTPUT'. Reads the committed v1_0_0, never edits it. Usage: python3 sen0401_ch06_domain_abox_plain_v1_0_0.py IN.ttl OUT.ttl"""
__version__ = "1.0.0"
import ast, json, re, sys
import sen0401_plain_code_v1_5_0 as P
IN, OUT = sys.argv[1:3]
t = open(IN, encoding="utf-8").read()
LIT = r'"((?:[^"\\]|\\.)*)"'
def unesc(s): return json.loads('"' + s.replace("\\'", "'") + '"')
def esc(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
def run(code):
    mod = ast.parse(code); last = mod.body[-1]; g = {}
    if isinstance(last, ast.Expr):
        exec(compile(ast.Module(mod.body[:-1], []), "x", "exec"), g)
        return eval(compile(ast.Expression(last.value), "x", "eval"), g)
    exec(code, g); return g.get("result")
n_io = n_err = 0
def io(m):
    global n_io
    name, lab, inp, out = m.group(1), unesc(m.group(2)), unesc(m.group(3)), unesc(m.group(4))
    if "lambda" not in inp: return m.group(0)
    new = P.plain(inp); v = run(new)
    assert repr(v) == out or str(v) == out, (name, repr(v)[:80], out[:80])
    n_io += 1
    return '%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s"@en ; chx:input "%s" ; chx:output "%s" .' % (name, esc(new + " evaluates to " + out), esc(new), esc(out))
t2 = re.sub(r'(chx:IO_\w+) a owl:NamedIndividual, rd:IOExample ; rdfs:label ' + LIT + r'@en ; chx:input ' + LIT + r' ; chx:output ' + LIT + r' \.', io, t)
def er(m):
    global n_err
    name, lab = m.group(1), unesc(m.group(2))
    if "lambda" not in lab: return m.group(0)
    code, _, tail = lab.rpartition(" raises ")
    new = P.plain(code); etype = tail.split(":")[0].strip()
    try: run(new); raise SystemExit("no error raised: " + name)
    except Exception as e:
        assert type(e).__name__ == etype, (name, type(e).__name__, etype)
    n_err += 1
    return '%s a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label "%s"@en .' % (name, esc(new + " raises " + tail))
t2 = re.sub(r'(chx:Err_\w+) a owl:NamedIndividual, rd:ErrorCondition ; rdfs:label ' + LIT + r'@en \.', er, t2)
assert "lambda" not in t2.replace("lambda - a", ""), [x for x in re.findall(r".{40}lambda.{40}", t2)][:3]
# header: the next minor version (new content in the examples, same classes and individuals)
for a, b in (('owl:versionInfo "1.0.0"', 'owl:versionInfo "1.1.0"'), ('/ch06/abox/1.0.0>', '/ch06/abox/1.1.0>'),
             ('dcterms:modified "2026-10-08"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date'),
             ('dcterms:identifier "sen0401_ch06_abox_v1_0_0"', 'dcterms:identifier "sen0401_ch06_abox_v1_1_0" ;\n    prov:wasRevisionOf <http://example.org/sen0401/ch06/abox/1.0.0>')):
    assert t2.count(a) == 1, a; t2 = t2.replace(a, b)
a = 'rdfs:comment "1.0.0 is the first ontology of chapter 6:'
assert t2.count(a) == 1; t2 = t2.replace(a, 'rdfs:comment "1.1.0 rewrites the 45 worked examples and 6 error conditions that held a lambda as plain statements (no lambda unless the subject teaches lambda); each rewritten example was executed and gives its stated output. 1.0.0 is the first ontology of chapter 6:')
open(OUT, "w", encoding="utf-8").write(t2)
print("IO examples rewritten", n_io, "error conditions rewritten", n_err, "bytes", len(t), "->", len(t2))
