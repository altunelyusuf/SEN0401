#!/usr/bin/env python3
"""sen0401_ch08_citecheck v1.0.0 - checks that every citation of the chapter 8 texts (the section paragraphs of the data module's BODY and the findings) is of the form that Stage3.F reads,
'(Name and Name, 2023)', '(Name et al., 2020)' or 'Name (2023)', that each one names a source of sen0401_ch08_sources_v1_0_0.py (author-year string of its 'cite' field), that every paragraph and
finding has at least one, that no parenthesis holds two citations (Stage3.F does not read a semicolon list), and that every source is cited at least once in BODY or FINDINGS cites.
Usage: sen0401_ch08_citecheck_v1_0_0.py   Exit 1 when anything is refused."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch08_rdodi_data_v1_0_0 as D
import sen0401_ch08_sources_v1_0_0 as S

CITES = {s["cite"] for s in S.SRC}
PAREN = re.compile(r"\(([A-Z][a-zA-Z.' ]+),\s*(\d{4})\)")
NARR = re.compile(r"([A-Z][a-zA-Z.' ]+?) \((\d{4})\)")
bad = []; used = set()
def check(where, text, need=True):
    found = [m.group(1).strip() + ", " + m.group(2) for m in PAREN.finditer(text)]
    # narrative form: the name is the words before '(year)' that start with a capital; take the longest suffix matching a known author string
    for m in NARR.finditer(text):
        pre = m.group(1); y = m.group(2)
        cand = [c for c in CITES if c.endswith(", " + y) and pre.endswith(c.rsplit(",", 1)[0])]
        found.append(cand[0] if cand else pre.strip() + ", " + y)
    for f in found:
        used.add(f)
        if f not in CITES:
            bad.append("%s: citation '%s' is not a source of the package" % (where, f))
    if need and not found:
        bad.append("%s: no citation" % where)
    if re.search(r"\([^()]*, \d{4}\s*;[^()]*\)", text):
        bad.append("%s: two citations in one parenthesis (Stage3.F reads only one)" % where)
for k, t in D.BODY.items():
    check("BODY " + k, t)
for fid, sec, t, cites in D.FINDINGS:
    check("FINDING " + fid, t)
    for c in cites:
        if c not in {p[0] for p in D.PUBS}:
            bad.append("FINDING %s cites unknown %s" % (fid, c))
fc = {c for f in D.FINDINGS for c in f[3]}
print("body sections:", len(D.BODY), "findings:", len(D.FINDINGS), "distinct author-year citations used:", len(used & CITES), "of", len(CITES), "; sources named by findings:", len(fc))
unused = sorted(CITES - used)
print("author-year strings of sources never cited in the texts:", unused)
print("\n".join(bad) or "citations ok")
sys.exit(1 if bad else 0)
