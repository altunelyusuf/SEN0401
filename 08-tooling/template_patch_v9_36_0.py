#!/usr/bin/env python3
"""Patches course_page_template_v9_35_0.html into course_page_template_v9_36_0.html.

One subject: the ontology graph's syntax and behaviour layers, after the owner's review of 2026-10-07:
"Ontology graph has no categorizations for syntactic, semantic, and behavioral categories."

Measured: the layers are computed by OG_PY (Python's ast over each concept's snippet) from `n.example`, the
worked-example label of the chapter ABox. For SEN0401 those labels are descriptions ("0.001 BTC equals 100000
satoshis"), not code, so ast.parse failed for every concept, no syntax or behaviour fact existed, and template
9.28.0 - correctly for what it was given - hid both layers and said the chapter's examples are not programs. But
42 of the chapter's 90 concepts DO carry executed Python (n.io.code, run by the build interpreter, re-run by
Pyodide in the page) - the extractor was simply never shown it.

9.36.0: the extractor is fed the executed code where a concept has one, and the example label only otherwise,
so the syntax layer draws the constructs each example is written with (calls, method calls, attribute access,
arithmetic, indexing ...) and the behaviour layer what it does (builds a new value, looks something up,
measures ...), each link carrying the piece of code it comes from, exactly as the layers already worked for
the Python course. One behaviour is added to the extractor's own list, because this chapter is built on it:
`hash` - a call to a hash function or digest (sha256, sha1, md5, blake2b, ripemd160, hexdigest, digest) -
labelled "computes a hash" beside the existing behaviours. The meaning layer is untouched.
"""
__version__ = "9.36.0"

SRC, DST = "course_page_template_v9_35_0.html", "course_page_template_v9_36_0.html"
t = open(SRC).read(); n0 = len(t)

def rep(old, new, n=1):
    global t
    c = t.count(old)
    assert c == n, "expected %d of %r, found %d" % (n, old[:70], c)
    t = t.replace(old, new)

rep("async function ogFacts(){if(OFACTS)return OFACTS;const sn={};D.nodes.forEach(n=>{if(n.level===3&&n.example)sn[n.id]=n.example});",
    "async function ogFacts(){if(OFACTS)return OFACTS;const sn={};D.nodes.forEach(n=>{if(n.level!==3)return;if(n.io&&n.io.code)sn[n.id]=n.io.code;else if(n.example)sn[n.id]=n.example});", 1)
rep("OG_BEH={inplace:'changes the value itself',", "OG_BEH={hash:'computes a hash',inplace:'changes the value itself',", 1)
rep("                if a in IOM: B('io', n)\n",
    "                if a in IOM: B('io', n)\n                if a in ('sha256', 'sha1', 'md5', 'blake2b', 'blake2s', 'ripemd160', 'sha3_256', 'hexdigest', 'digest'): B('hash', n)\n", 1)
rep("<!-- course_page_template version 9.35.0:",
    "<!-- course_page_template version 9.36.0: the ontology graph's syntax and behaviour layers are computed from each "
    "concept's executed code where it has one (SEN0401's examples are descriptions, its executed code was never shown "
    "to the extractor), and the extractor learns one behaviour this chapter is built on, computing a hash. Earlier: "
    "--><!-- course_page_template version 9.35.0:", 1)
open(DST, "w").write(t)
print("written %s (%d -> %d bytes)" % (DST, n0, len(t)))
