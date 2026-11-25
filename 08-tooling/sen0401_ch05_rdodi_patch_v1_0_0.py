#!/usr/bin/env python3
"""sen0401_ch05_rdodi_patch v1.0.0 (course rulings of 2026-11-24: no lambda unless taught, no everyday comparison). Writes beside the committed files (which stay unchanged):
  03-materials/ch05/rdodi/sen0401_ch05_domain_abox_v1_1_1.ttl  = the ABox 1.1.0 with every worked example and error condition written without lambda (each input still evaluates to the same output; checked here);
  03-materials/ch05/rdodi/sen0401_ch05_document_v1_1_2.ttl      = the document 1.1.1 with four sentences reworded (they said 'think of', 'imagine', 'the right picture'); text of the book unchanged otherwise.
Both are PATCH versions: no concept, label, definition or result changes. The tbox and the research record have no finding and stay at their versions. Usage: python3 sen0401_ch05_rdodi_patch_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(HERE); R = os.path.join(REPO, "03-materials", "ch05", "rdodi")
def q(s): return s.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
def unq(s):
    out, i = [], 0
    while i < len(s):
        if s[i] == "\\":
            c = s[i + 1]; out.append({"n": "\n", "t": "\t", "r": "\r"}.get(c, c)); i += 2
        else: out.append(s[i]); i += 1
    return "".join(out)
PROG = re.compile(r"\(lambda g: \(exec\((?P<code>.*?), g\), g\[(?P<var>'[^']+')\]\)\[1\]\)\(\{\}\)", re.S)
FIXED = {
 "(lambda keys, size: (keys * size, round(keys * size / 1024, 1)))(1000, 32)": "(1000 * 32, round(1000 * 32 / 1024, 1))",
 "(lambda p, g, a, t: (((a + t) % p) * g % p, (a * g % p + t * g % p) % p))(17, 5, 9, 3)": "(((9 + 3) % 17) * 5 % 17, (9 * 5 % 17 + 3 * 5 % 17) % 17)",
 "(lambda passphrases: (len(passphrases), len(passphrases) + 1))(['holiday', 'decoy'])": "(len(['holiday', 'decoy']), len(['holiday', 'decoy']) + 1)",
 "(lambda h, a, b: sum(bin(x ^ y).count('1') for x, y in zip(h(a), h(b))))(lambda m: __import__('hashlib').sha256(m).digest(), b'pay Bob 1 BTC', b'pay Bob 2 BTC')":
 "sum(bin(x ^ y).count('1') for x, y in zip(__import__('hashlib').sha256(b'pay Bob 1 BTC').digest(), __import__('hashlib').sha256(b'pay Bob 2 BTC').digest()))",
}
def T(e):
    for a, b in FIXED.items(): e = e.replace(a, b)
    e = PROG.sub(lambda m: "[g := {}, exec(%s, g), g[%s]][-1]" % (m.group("code"), m.group("var")), e)
    m = re.fullmatch(r"\(lambda h: (?P<body>.*)\)\((?P<arg>__import__\('hashlib'\))\)", e, re.S)      # a one-parameter lambda applied once
    if m: e = "[h := %s, %s][-1]" % (m.group("arg"), m.group("body"))
    return e

# ------------------------------------------------------------------ the ABox
src = open(os.path.join(R, "sen0401_ch05_domain_abox_v1_1_0.ttl"), encoding="utf-8").read(); out = []; n_io = n_err = 0
for line in src.split("\n"):
    if "lambda" in line:
        if line.startswith("chx:IO_"):
            m = re.match(r'(chx:IO_\w+ a [^"]*?rdfs:label ")((?:[^"\\]|\\.)*)("@en ; chx:input ")((?:[^"\\]|\\.)*)(" ; chx:output ")((?:[^"\\]|\\.)*)(" \.)$', line)
            assert m, line[:120]
            old_in, outp = unq(m.group(4)), unq(m.group(6)); new_in = T(old_in); assert "lambda" not in new_in, new_in[:200]
            got = repr(eval(new_in, {})); assert got == outp, (m.group(1)[:30], got[:80], outp[:80])
            line = m.group(1) + q(new_in + " evaluates to " + outp) + m.group(3) + q(new_in) + m.group(5) + m.group(6) + m.group(7); n_io += 1
        elif line.startswith("chx:Err_"):
            m = re.match(r'(chx:Err_\w+ a [^"]*?rdfs:label ")((?:[^"\\]|\\.)*)("@en .*)$', line)
            assert m, line[:120]
            lab = unq(m.group(2)); expr, rest = lab.rsplit(" raises ", 1); new = T(expr); assert "lambda" not in new
            got = None
            try: eval(new, {})
            except Exception as e1: got = type(e1).__name__
            assert got == rest.split(":")[0], (got, rest, new[:80])
            line = m.group(1) + q(new + " raises " + rest) + m.group(3); n_err += 1
        else: raise SystemExit("an unexpected line with lambda: " + line[:100])
    out.append(line)
t = "\n".join(out); assert "lambda" not in t
t = t.replace('owl:versionInfo "1.1.0" ; owl:versionIRI <http://example.org/sen0401/ch05/abox/1.1.0> ; rdfs:comment "',
  'owl:versionInfo "1.1.1" ; owl:versionIRI <http://example.org/sen0401/ch05/abox/1.1.1> ; rdfs:comment "1.1.1 is a PATCH of 1.1.0 (2026-11-25): the worked examples and error conditions that were written as one-line unnamed functions are written with plain expressions, as the course ruling of 2026-11-24 asks; every input still evaluates to the output recorded in 1.1.0 (checked), and no concept, label, definition or result changes. ', 1)
t = t.replace('dcterms:modified "2026-10-05"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date', 1)
t = t.replace('dcterms:identifier "sen0401_ch05_abox_v1_1_0" ; prov:wasRevisionOf <http://example.org/sen0401/ch05/abox/1.0.0>', 'dcterms:identifier "sen0401_ch05_abox_v1_1_1" ; prov:wasRevisionOf <http://example.org/sen0401/ch05/abox/1.1.0>', 1)
assert t.count("1.1.1") >= 3 and "sen0401_ch05_abox_v1_1_1" in t
open(os.path.join(R, "sen0401_ch05_domain_abox_v1_1_1.ttl"), "w", encoding="utf-8").write(t)
print("ABox 1.1.1: worked examples rewritten %d, error conditions %d; no lambda left" % (n_io, n_err))

# ------------------------------------------------------------------ the document
REPL = [
 ("Seeing this removes the temptation to think of the words as independently meaningful,", "Seeing this removes the temptation to treat the words as independently meaningful,"),
 ("The chapter gives the right picture: think of an extended key as the root of a branch in the tree structure, with which the rest of the branch can be derived,", "The chapter states it precisely: an extended key is the root of a branch in the tree structure, from which the rest of the branch can be derived,"),
 ("The chapter asks the reader to imagine reviewing a bank or credit card statement from a year ago that had the date and amount of every transaction listed but a blank entry for the description field, and says that because address and transaction labels are stored only",
  "The chapter explains that, because address and transaction labels are stored only"),
 ("the first thing they lose and the last thing they think of.", "the first thing they lose and the last thing they remember to back up."),
]
d = open(os.path.join(R, "sen0401_ch05_document_v1_1_1.ttl"), encoding="utf-8").read()
for a, b in REPL:
    assert d.count(a) == 1, a[:60]; d = d.replace(a, b)
d = d.replace('owl:versionInfo "1.1.1" ; owl:versionIRI <http://example.org/sen0401/ch05/document/1.1.1> ; rdfs:comment "',
  'owl:versionInfo "1.1.2" ; owl:versionIRI <http://example.org/sen0401/ch05/document/1.1.2> ; rdfs:comment "1.1.2 is a PATCH of 1.1.1 (2026-11-25): four sentences are reworded because they compared the subject with something outside the chapter (course ruling of 2026-11-24); no concept, section or fact changes. ', 1)
d = d.replace('dcterms:modified "2026-10-14"^^xsd:date', 'dcterms:modified "2026-11-25"^^xsd:date', 1)
d = d.replace('dcterms:identifier "sen0401_ch05_document_v1_1_1" ; prov:wasRevisionOf <http://example.org/sen0401/ch05/document/1.1.0>', 'dcterms:identifier "sen0401_ch05_document_v1_1_2" ; prov:wasRevisionOf <http://example.org/sen0401/ch05/document/1.1.1>', 1)
assert "sen0401_ch05_document_v1_1_2" in d and 'versionInfo "1.1.2"' in d
open(os.path.join(R, "sen0401_ch05_document_v1_1_2.ttl"), "w", encoding="utf-8").write(d)
print("document 1.1.2: 4 sentences reworded")
import rdflib
for f in ("sen0401_ch05_domain_abox_v1_1_1.ttl", "sen0401_ch05_document_v1_1_2.ttl"):
    g = rdflib.Graph(); g.parse(os.path.join(R, f), format="turtle"); print(f, len(g), "triples parse")
