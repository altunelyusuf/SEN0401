#!/usr/bin/env python3
"""sen0401_ch01_ontology_copies v1.0.0 - writes the chapter 1 Turtle files that the page 9.76.0 embeds, as NEW files beside the committed ones (which stay unchanged):
  03-materials/ch01/rdodi/sen0401_ch01_document_v1_3_0.ttl     = sen0401_ch01_document_v1_2_1.ttl with every sentence deleted that the ruling pattern of the deck standard (shape D4, 2026-11-24) finds;
  03-materials/ch01/rdodi/sen0401_ch01_domain_abox_v1_3_0.ttl  = sen0401_ch01_domain_abox_v1_2_0.ttl with the eleven input/output examples written without lambda (the exec wrapper
                                                                (lambda g: (exec(code, g), g['result'])[1])({}) becomes (exec(code, g := {}), g['result'])[1]; three formulas are written out);
every example is evaluated before and after and must give its stated output. Usage: python3 sen0401_ch01_ontology_copies_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
import rdflib
H = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(H); R = os.path.join(REPO, "03-materials", "ch01", "rdodi")
g = rdflib.Graph(); g.parse(os.path.join(REPO, "06-quality", "sen0401_deck_standard_shapes_v1_1_0.ttl"), format="turtle")
RX = re.compile(str(next(g.objects(None, rdflib.Namespace("http://www.w3.org/ns/shacl#").pattern))), re.I)
ENDS = re.compile(r"""[.!?](?=["'\u201d)\]]*(?:\s+["'\u201c(]?[A-Z0-9]|\s*$))""")

def sentence_span(s, m):
    st = 0
    if s[m.start()] in ".!?" and m.group(0)[0] in ".!?": st = m.start() + 1
    else:
        for e in ENDS.finditer(s):
            if e.end() <= m.start(): st = e.end()
    while st < len(s) and s[st] in " \u201d\"')]": st += 1
    e = ENDS.search(s, m.end()); en = e.end() if e else len(s)
    while en < len(s) and s[en] in "\"'\u201d)]": en += 1
    return st, en
def strip_analogies(s):
    out = s
    for _ in range(40):
        m = RX.search(out)
        if not m: break
        st, en = sentence_span(out, m)
        if st > 0 and out[st - 1] == " ": st -= 1
        elif en < len(out) and out[en] == " ": en += 1
        out = out[:st] + out[en:]
    return out
UN = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "'": "'"}
def unesc(x): return re.sub(r"\\(.)", lambda m: UN[m.group(1)], x)
def esc(x): return x.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t").replace("\r", "\\r")
LIT = re.compile(r'"((?:[^"\\]|\\.)*)"')

# ---------------------------------------------------------------- the document
src = open(os.path.join(R, "sen0401_ch01_document_v1_2_1.ttl"), encoding="utf-8", newline="").read()
n = 0
def lit(m):
    global n
    v = unesc(m.group(1))
    if not RX.search(v): return m.group(0)
    new = strip_analogies(v)
    assert "\\u" not in m.group(1)
    n += 1
    return '"' + esc(new) + '"'
doc = LIT.sub(lit, src)
assert not RX.search("\n".join(unesc(x) for x in LIT.findall(doc))), "an analogy is left"
f = os.path.join(R, "sen0401_ch01_document_v1_3_0.ttl")
assert not os.path.exists(f); open(f, "w", encoding="utf-8", newline="").write(doc); print("document: literals changed", n, "->", os.path.relpath(f, REPO))

# ---------------------------------------------------------------- the domain abox
def examples(text):
    gg = rdflib.Graph(); gg.parse(data=text, format="turtle"); out = {}
    inp = [p for p in set(gg.predicates()) if str(p).endswith("#input") or str(p).endswith("/input")][0]
    outp = [p for p in set(gg.predicates()) if str(p).endswith("#output") or str(p).endswith("/output")][0]
    for s, _, i in gg.triples((None, inp, None)):
        out[str(s)] = (str(i), str(next(gg.objects(s, outp))))
    return out
a = open(os.path.join(R, "sen0401_ch01_domain_abox_v1_2_0.ttl"), encoding="utf-8", newline="").read()
before = examples(a)
for k, (i, o) in before.items(): assert repr(eval(i)) == o, k
SPECIAL = {
 "Confirmation": ("(exec(\"m = __import__('math')\\nq, z = 0.1, 6\\np = 1 - q\\nl = z * q / p\\nresult = round(1 - sum(m.exp(-l) * l**k / m.factorial(k) * (1 - (q / p)**(z - k)) for k in range(z + 1)), 7)\", g := {}), g['result'])[1]", "0.0002428"),
 "DigitalSignature": ("(pow(65, 2753, 3233), pow(pow(65, 2753, 3233), 17, 3233) == 65, pow(pow(65, 2753, 3233), 17, 3233) == 66)", "(588, True, False)"),
 "Uri": ("((u := __import__('urllib.parse', fromlist=['parse']).urlsplit('bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=20.3&label=Luke-Jr')).scheme, u.path, u.query)", "('bitcoin', '175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W', 'amount=20.3&label=Luke-Jr')"),
}
for name, (inp, outv) in SPECIAL.items():
    m = re.search(r"^chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label .*$" % name, a, re.M); assert m, name
    line = 'chx:IO_%s a owl:NamedIndividual, rd:IOExample ; rdfs:label "%s evaluates to %s"@en ; chx:input "%s" ; chx:output "%s" .' % (name, esc(inp), esc(outv), esc(inp), esc(outv))
    a = a[:m.start()] + line + a[m.end():]
c1 = a.count("(lambda g: (exec("); c2 = a.count(", g), g['result'])[1])({})")
a = a.replace("(lambda g: (exec(", "(exec(").replace(", g), g['result'])[1])({})", ", g := {}), g['result'])[1]")
print("exec wrappers rewritten:", c1, c2); assert c1 == c2 == 16, (c1, c2)
assert "lambda" not in a
after = examples(a)
assert set(after) == set(before)
for k, (i, o) in after.items():
    assert repr(eval(i)) == o, (k, i[:80])
    assert o == before[k][1], k
f = os.path.join(R, "sen0401_ch01_domain_abox_v1_3_0.ttl")
assert not os.path.exists(f); open(f, "w", encoding="utf-8", newline="").write(a); print("abox: examples", len(after), "all evaluate to their stated output ->", os.path.relpath(f, REPO))
