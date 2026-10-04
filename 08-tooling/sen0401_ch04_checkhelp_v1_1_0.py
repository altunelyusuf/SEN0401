"""Helpers that build the expressions of CHECKS of sen0401_ch04_corpus_v1_1_0.py. Each expression is evaluated alone, in a fresh namespace, by the
chapter builder (python 3.14), so every expression is self-contained: it reads a saved source file or imports the chapter's own toolkit by path.
The saved sources are in 08-tooling/ch04-evidence (src_v1_1_0, src_v1_2_0, src_v1_3_0 and the files of the run of Bitcoin Core 31.1)."""
__version__ = "1.1.0"
import os
HERE = os.path.dirname(os.path.abspath(__file__))
EVD = os.path.join(HERE, "ch04-evidence") + "/"
S1, S2, S3 = EVD + "src_v1_1_0/", EVD + "src_v1_2_0/", EVD + "src_v1_3_0/"
BOOKD = "/home/claude/src/bitcoinbook/"
COREDIR = "/home/claude/src/bitcoin"
RDODI = os.path.join(os.path.dirname(HERE), "03-materials")
def rd(path): return "open(%r, encoding='utf-8').read()" % path
def ev(name): return rd(EVD + name)
def js(path): return "__import__('json').load(open(%r))" % path
def evj(name): return js(EVD + name)
def core(path):   # text of a file of Bitcoin Core's tree at the checked-out commit
    return "__import__('subprocess').run(['git', '-C', %r, 'show', 'HEAD:%s'], capture_output=True, text=True).stdout" % (COREDIR, path)
def norm(expr): return "' '.join((%s).split())" % expr
def has(expr, *pieces): return "all(p in %s for p in %r)" % (norm(expr), tuple(' '.join(p.split()) for p in pieces))
def book(name):   # a chapter file of the book with the index markup (((...))) removed
    return "__import__('re').sub(r'\\({3}.*?\\){3}', '', %s, flags=__import__('re').S)" % rd(BOOKD + name)
def prev(ch):     # the text of the newest document of an earlier chapter of this course (Stage 3 file)
    import glob, re
    fs = sorted(glob.glob(os.path.join(RDODI, "ch%s" % ch, "rdodi", "sen0401_ch%s_document_v*.ttl" % ch)), key=lambda f: [int(x) for x in re.search(r"_v(\d+_\d+_\d+)\.ttl$", f).group(1).split("_")])
    return rd(fs[-1])
KT = "(__import__('sys').path.insert(0, %r) or __import__('sen0401_ch04_keys_v1_1_0'))" % HERE
CL = "(__import__('sys').path.insert(0, %r) or __import__('sen0401_ch04_checklib_v1_1_0'))" % HERE
def X(s, **kw):
    """expression text with the tokens $T (the toolkit), $CL (the check library) and $NAME (any keyword given) replaced; no % formatting, so % can be used in the expression"""
    s = s.replace("$T", KT).replace("$CL", CL)
    for k, v in sorted(kw.items(), key=lambda kv: -len(kv[0])): s = s.replace("$" + k, v)
    return s
