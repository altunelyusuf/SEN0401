#!/usr/bin/env python3
"""SEN0401 chapter 1 verify script: executes the claims of the chapter 1 research that can be executed, with no network and no node.
Three parts, each reported as printed and each a failure when it does not hold:
 1 numbers   every (expression, expected) pair of the chapter's numbers module (sen0401_ch01_numchecks) is evaluated and must give exactly its value
 2 sources   every quotation of the chapter's source-check modules (sen0401_ch01_srcchecks_a/b/c) must occur in the saved source file
 3 examples  every IO individual of the newest chapter 1 domain ABox is executed under the running interpreter and must give exactly its recorded output
Exit 0 and 'failures: []' when all hold. Run: python3.14 sen0401_ch01_verify_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys, ast, importlib
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
n = 1
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
print(os.path.basename(ab))
print("source quotations %d; numbers %d; examples %d, executed %d" % (nsrc, nnum, len(ios), nexec))
print("failures:", fail)
sys.exit(1 if fail else 0)
