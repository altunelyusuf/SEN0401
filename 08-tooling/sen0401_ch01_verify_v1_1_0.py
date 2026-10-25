#!/usr/bin/env python3
"""SEN0401 chapter 1 verify script v1.1.0: adopts the form of the chapter 2 verify script (the shared library sen0401_research_verify_lib_v1_0_0.py, six parts) and keeps
every check of v1.0.0. Five parts, each reported as printed and each a failure when it does not hold:
 1 numbers    every (expression, expected) pair of the chapter's numbers module (sen0401_ch01_numchecks) is evaluated and must give exactly its value
 2 sources    every quotation of the chapter's source-check modules (sen0401_ch01_srcchecks_a/b/c) must occur in the saved source file
 3 examples   every IO individual of the newest chapter 1 domain ABox is executed under the running interpreter and must give exactly its recorded output
 4 finding F8 the new finding of research v1.3.0 is re-read from the saved copies of RFC 3986, BIP 21 and the DID specification, and the BIP 21 example is split by a standard URI parser
 5 library    sen0401_research_verify_lib_v1_0_0.run(1): sources recorded, saved evidence intact, stories, classes-sections-citations, every ABox example executed, findings and sources citing each other
Exit 0 and 'failures: []' when all hold. Run: python3.14 sen0401_ch01_verify_v1_1_0.py"""
__version__ = "1.1.0"
import os, sys, ast, re
from urllib.parse import urlsplit, parse_qs
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_research_verify_lib_v1_0_0 as L
import sen0401_ch01_corpus_v1_2_0 as C
fail = []
# 1 numbers and 2 sources: the corpus module's own CHECKS list is SRC_A + SRC_B + SRC_C quotations followed by NUM
nsrc = len(C.SRC_A) + len(C.SRC_B) + len(C.SRC_C); nnum = len(C.NUM)
for idx, (e, x) in enumerate(C.CHECKS):
    try: got = repr(eval(e, {}))
    except BaseException as ex: got = "EXC %r" % (ex,)
    if got != x: fail.append(("source quotation" if idx < nsrc else "number", e[:100], x, got[:60]))
# 3 examples
rd = os.path.join(L.REPO, "03-materials", "ch01", "rdodi")
ab = L.newest(os.path.join(rd, "sen0401_ch01_domain_abox_v*.ttl"))
ios = {}
for s, t in L.statements(ab):
    if s.startswith("chx:IO_"):
        i = L.re.search(r"chx:input " + L.LIT, t); o = L.re.search(r"chx:output " + L.LIT, t)
        ios[s[7:]] = (L.unesc(i.group(1)) if i else None, L.unesc(o.group(1)) if o else None)
os.chdir(L.REPO); nexec = 0
for k, (i, o) in sorted(ios.items()):
    if i is None or o is None: fail.append(("example without input or output", k)); continue
    try:
        t = ast.parse(i); last = t.body.pop() if t.body and isinstance(t.body[-1], ast.Expr) else None
        ns = {"__name__": "__verify__"}; exec(compile(t, k, "exec"), ns)
        got = repr(eval(compile(ast.Expression(last.value), k, "eval"), ns)) if last else repr(None)
    except BaseException as e:
        got = "EXC %r" % (e,)
    nexec += 1
    if got != o: fail.append(("example result differs", k, o[:60], got[:60]))
if nsrc < 1 or nnum < 1 or len(ios) < 1: fail.append(("nothing to check", nsrc, nnum, len(ios)))
# 4 finding F8 (research v1.3.0): sentences re-read from the saved copies, the example computed
src = os.path.join(L.HERE, "ch01-sources")
norm = lambda f: re.sub(r"\s+", " ", open(os.path.join(src, f), encoding="utf-8", errors="replace").read())
F8 = [("rfc3986.txt", ["provides a simple and extensible means for identifying a resource", 'URI = scheme ":" hier-part [ "?" query ] [ "#" fragment ]']),
      ("bip21.txt", ["bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=20.3&label=Luke-Jr", "This BIP has been superseded and replaced with BIP 321"]),
      ("did.txt", ["is a URI composed of three parts: the scheme did:", "The generic DID scheme is a URI scheme conformant with [ RFC3986 ]"])]
nf8 = 0
for f, qs in F8:
    txt = norm(f)
    for q in qs:
        nf8 += 1
        if q not in txt: fail.append(("F8 quotation not in the saved copy", f, q[:70]))
u = urlsplit("bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=20.3&label=Luke-Jr")
if (u.scheme, u.path, parse_qs(u.query)) != ("bitcoin", "175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W", {"amount": ["20.3"], "label": ["Luke-Jr"]}):
    fail.append(("F8 URI split differs", u.scheme, u.path, u.query))
print(os.path.basename(ab))
print("source quotations %d; numbers %d; examples %d, executed %d; F8 quotations %d and one URI split" % (nsrc, nnum, len(ios), nexec, nf8))
print("failures (parts 1 to 4):", fail)
# 5 the shared library (prints its own line and 'failures:', then exits)
code = 0
try:
    L.run(1)
except SystemExit as e:
    code = e.code or 0
sys.exit(1 if (fail or code) else 0)
