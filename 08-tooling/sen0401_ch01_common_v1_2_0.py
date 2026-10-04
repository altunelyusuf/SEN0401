"""Shared helpers of the SEN0401 chapter 1 corpus (version 1.2.0): the facet names (a writing guide, never printed), the citation tokens,
and the builders of the CHECKS expressions that re-read the saved copies of the sources in 08-tooling/ch01-sources."""
import os, re
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"
# author-year citation strings; each one occurs in the label of a publication of the research record (sen0401_ch01_research_v1_2_0.ttl)
CITES = {"[AH]": " (Antonopoulos and Harding, 2023)", "[NK]": " (Nakamoto, 2008)", "[BK]": " (Back, 2002)", "[BC]": " (Bitcoin Core, 2026)",
         "[B39]": " (Palatinus et al., 2013)", "[DID]": " (World Wide Web Consortium, 2022)", "[VC]": " (World Wide Web Consortium, 2025)",
         "[BW]": " (Bitcoin Wiki, 2026)", "[BS]": " (Blockstream, 2026)", "[SH]": " (Shirey, 2007)",
         "[MD]": " (Mozilla Developer Network, 2026)", "[OSI]": " (Open Source Initiative, 2026)", "[WP]": " (Wikipedia contributors, 2026)",
         "[EH]": " (Eastlake and Hansen, 2011)", "[LP]": " (Lamport et al., 1982)", "[B21]": " (Schneider and Corallo, 2012)",
         "[PK]": " (Moriarty et al., 2017)", "[JO]": " (Josefsson, 2006)", "[LN]": " (Poon and Dryja, 2016)", "[WC]": " (World Wide Web Consortium, 2026)",
         "[UR]": " (Berners-Lee et al., 2005)", "[HT]": " (Fielding et al., 2022)"}
def c(t):
    t = re.sub(r"\](?=\[[A-Za-z0-9]{2,4}\])", "] ", t)   # [NK][BK] -> [NK] [BK], so every token is preceded by a blank
    for k, v in CITES.items(): t = t.replace(" " + k, v)
    assert not any(k in t for k in CITES), t
    return t
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch01-sources") + "/"
_DEFS = r'''
import re
def N(t):
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("\xa0", " "), ("&#x27;", "'")): t = t.replace(a, b)
    t = re.sub(r"\(\(\(.*?\)\)\)", "", t, flags=re.S)
    t = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"'{2,}", "", t)
    t = re.sub(r"(?<!\w)_|_(?!\w)", "", t).replace("*", "")
    return " ".join(t.split())
def H(path, pieces):
    t = N(open(path, encoding="utf-8", errors="replace").read())
    return all(N(p) in t for p in pieces)
def M(path, pieces):
    t = N(open(path, encoding="utf-8", errors="replace").read())
    return [p for p in pieces if N(p) not in t]
'''
def has(name, *pieces):
    """True when every piece occurs in the saved source (index markup removed, quotes unified, white space collapsed): the text quotes only what it read"""
    return "(lambda g: (exec(%r, g), g['H'](%r, %r))[1])({})" % (_DEFS, SRC + name, tuple(pieces))
def missing(name, *pieces):
    g = {}; exec(_DEFS, g); return g["M"](SRC + name, pieces)
def rd(name): return "open(%r, encoding='utf-8').read()" % (SRC + name)
def js(name): return "__import__('json').load(open(%r))" % (SRC + name)
def prog(code, result="result"):
    """a small program (statements) evaluated as one expression: the value of its variable `result`"""
    return "(lambda g: (exec(%r, g), g[%r])[1])({})" % (code, result)
