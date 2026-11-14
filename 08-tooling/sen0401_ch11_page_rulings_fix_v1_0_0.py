#!/usr/bin/env python3
"""sen0401_ch11_page_rulings_fix v1.0.0 - corrects the chapter 11 page to the owner's material rulings of 2026-11-14 (urgent lineage 7, story ST7_Ch11_Page).
Reads page v9.94.0 and its page_data, writes v9.95.0 of each. Changes: the deck's two lambda examples (slides 18, 19) and example 15 use def;
the editor's starter snippet and keyword hints no longer show lambda; the one source-listing line that began with three dots uses an ellipsis sign."""
import os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
H = os.path.join(R, "03-materials", "ch11", "page", "sen0401_ch11_page_v9_94_0.html")
J = os.path.join(R, "08-tooling", "ch11-page", "page_data_v9_94_0.json")
NL = "\\n"   # JSON/turtle escape, as written in the files
SUB = [
 ("link = lambda x, y: y['prev'] == x['hash']", "def link(x, y): return y['prev'] == x['hash']"),
 ("cu = lambda z: round(L.catchup(0.1, z), 7)", "def cu(z): return round(L.catchup(0.1, z), 7)"),
 ("R = L.run(); f = lambda a: (", "R = L.run()" + NL + "def f(a):" + NL + "    return ("),
 ("\"code\": \"f = lambda a: (", "\"code\": \"def f(a):" + NL + "    return ("),
 ("); c = R['b9_chains']; (", ")" + NL + "c = R['b9_chains']" + NL + "("),
 ("key=lambda x: len(x)", "key=len"),
 ("lambda x: expression - a small unnamed function", "lambda - a small unnamed function"),
 ("'lambda  lambda x: …'", "'small unnamed function'"),
 ("\n  ...,\n", "\n  …,\n"),
 ("\\n  ...,\\n", "\\n  …,\\n"),
]
def patch(t):
    for a, b in SUB:
        t = t.replace(a, b)
    return t
def bump(p, new):
    d, f = os.path.split(p); n = re.sub(r"v9_94_0", "v9_95_0", f)
    return os.path.join(d, n)
for p in (H, J):
    t = open(p, encoding="utf-8").read()
    n = patch(t).replace('"_version": "9.94.0"', '"_version": "9.95.0"')
    q = bump(p, "9_95_0"); assert not os.path.exists(q), q
    open(q, "w", encoding="utf-8").write(n); print(os.path.basename(q), len(t) - len(n))
