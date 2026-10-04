#!/usr/bin/env python3
"""Helpers for the executed claims of the SEN0401 chapter 5 corpus (python standard library only).

Source readers: has_book / has_ev / has_src / has_core say whether every phrase occurs (white space collapsed, the book's index markup
((( ... ))) removed) in a chapter of the book (/home/claude/src/bitcoinbook), in a source saved in 08-tooling/ch05-evidence, in a source saved
for another chapter (08-tooling/chNN-sources), or in a file of Bitcoin Core at the commit pinned for this course. Every saved copy of
ch05-evidence was compared on 2026-10-02 with its upstream URL (byte-identical at that time; the URLs are in the research record)."""
__version__ = "1.0.0"
import os, re, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/home/claude/src/bitcoinbook"
CORE = "/home/claude/src/bitcoin"
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
EV = os.path.join(HERE, "ch05-evidence")

def _norm(t):
    t = re.sub(r"\(\(\(.*?\)\)\)", "", t, flags=re.S)
    return " ".join(t.split())
def _read(path): return open(path, encoding="utf-8", errors="replace").read()
def book_text(name): return _norm(_read(os.path.join(BOOK, name)))
def ev_text(name): return _norm(_read(os.path.join(EV, name)))
def src_text(chdir, name): return _norm(_read(os.path.join(HERE, chdir, name)))
def core_text(path):
    r = subprocess.run(["git", "-c", "gc.auto=0", "-C", CORE, "show", "%s:%s" % (COMMIT, path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    return _norm(r.stdout)
def _all(t, phrases, where):
    ok = True
    for p in phrases:
        if _norm(p) not in t:
            ok = False
            if os.environ.get("CH5_DEBUG"): print("MISSING in %s: %r" % (where, p))
    return ok
def has_book(name, *phrases): return _all(book_text(name), phrases, name)
def has_ev(name, *phrases): return _all(ev_text(name), phrases, name)
def has_src(chdir, name, *phrases): return _all(src_text(chdir, name), phrases, name)
def has_core(path, *phrases): return _all(core_text(path), phrases, path)
def ev_json(name): return json.load(open(os.path.join(EV, name), encoding="utf-8"))
def ev_raw(name): return _read(os.path.join(EV, name))
def book_raw(name): return _read(os.path.join(BOOK, name))

def pptx_text(rel):
    """all text of the slides of a .pptx (a zip of XML files), white space collapsed"""
    import zipfile
    z = zipfile.ZipFile(os.path.join(HERE, rel)); parts = []
    for n in sorted(z.namelist()):
        if re.match(r"ppt/slides/slide\d+\.xml$", n): parts += re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8"))
    return _norm(" ".join(parts))
def has_pptx(rel, *phrases): return _all(pptx_text(rel), phrases, rel)
