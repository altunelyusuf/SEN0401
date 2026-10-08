#!/usr/bin/env python3
"""Helpers for the executed claims of the SEN0401 chapter 6 corpus (python standard library only).

Adapted from chapter 5's sen0401_ch05_checklib_v1_0_0.py for this chapter: the evidence folder is 08-tooling/ch06-evidence,
and three readers are added for what this chapter's evidence holds and chapter 5's did not - a raw transaction saved as hex
(ev_hex), an explorer's JSON record of a transaction (ev_json, the same name as before) and a line count of a saved source
(ev_lines); has_pptx reads the owner's legacy slides as chapter 5's did. Nothing else changes: has_book / has_ev / has_core say whether every phrase occurs (white space collapsed, the
book's index markup ((( ... ))) removed) in a chapter of the book (/home/claude/src/bitcoinbook at the commit the textbook
ontology pins, 275c4eb8), in a source saved in ch06-evidence, or in a file of Bitcoin Core at the commit pinned for this
course (05bc2f5). Every saved copy of ch06-evidence was fetched on 2026-10-08 from the URL the evidence script names."""
__version__ = "1.0.0"
import os, re, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = "/home/claude/src/bitcoinbook"
CORE = "/home/claude/src/bitcoin"
COMMIT = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
EV = os.path.join(HERE, "ch06-evidence")

def _norm(t):
    t = re.sub(r"\(\(\(.*?\)\)\)", "", t, flags=re.S)
    return " ".join(t.split())
def _read(path): return open(path, encoding="utf-8", errors="replace").read()
def book_text(name): return _norm(_read(os.path.join(BOOK, name)))
def ev_text(name): return _norm(_read(os.path.join(EV, name)))
def core_text(path):
    r = subprocess.run(["git", "-c", "gc.auto=0", "-C", CORE, "show", "%s:%s" % (COMMIT, path)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[:200]
    return _norm(r.stdout)
def _all(t, phrases, where):
    ok = True
    for p in phrases:
        if _norm(p) not in t:
            ok = False
            if os.environ.get("CH6_DEBUG"): print("MISSING in %s: %r" % (where, p))
    return ok
def has_book(name, *phrases): return _all(book_text(name), phrases, name)
def has_ev(name, *phrases): return _all(ev_text(name), phrases, name)
def has_core(path, *phrases): return _all(core_text(path), phrases, path)
def ev_json(name): return json.load(open(os.path.join(EV, name), encoding="utf-8"))
def ev_hex(name): return _read(os.path.join(EV, name)).strip()
def ev_raw(name): return _read(os.path.join(EV, name))
def ev_lines(name): return len(_read(os.path.join(EV, name)).splitlines())
def book_raw(name): return _read(os.path.join(BOOK, name))

def pptx_text(rel):
    """all text of the slides of a .pptx (a zip of XML files), white space collapsed"""
    import zipfile
    z = zipfile.ZipFile(os.path.join(HERE, rel)); parts = []
    for n in sorted(z.namelist()):
        if re.match(r"ppt/slides/slide\d+\.xml$", n): parts += re.findall(r"<a:t>([^<]*)</a:t>", z.read(n).decode("utf-8"))
    return _norm(" ".join(parts))
def has_pptx(rel, *phrases): return _all(pptx_text(rel), phrases, rel)
