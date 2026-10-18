#!/usr/bin/env python3
"""SEN0401 chapter 13 verify script (1.0.2: also checks that at least 12 self-contained examples change their result when a whole number in them is changed, the way the page varies them): the research package's own consistency checks that need no network and no node.
1 every source of the table was fetched (HTTP 200, sha256 recorded); 2 every passage used is found in the saved copy;
3 the stories' facts, links and pictures; 4 every class of the taxonomy has a cited paragraph (Stage 3.F form); 5 the regtest record is complete;
6 the findings cite only sources of the table and every source is cited by a finding or a paragraph. Exit 0 and 'failures: []' when all hold."""
__version__ = "1.0.2"
import os, re, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sen0401_ch13_lib_v1_0_0 as L
import sen0401_ch13_stories_v1_0_0 as ST
import sen0401_ch13_sources_v1_0_0 as SRC
import sen0401_ch13_rdodi_data_v1_0_2 as D
fail = []
n, ok, notok = L.index_report()
if notok or n != ok: fail.append(("index", notok))
ns, nf, bad, missing = L.quotes_report()
if bad or missing: fail.append(("quotes", bad[:3], missing[:3]))
fail += [("stories", b) for b in ST.run_checks()]
CITE = re.compile(r"[A-Z][a-zA-Z\.\' ]+\(\d{4}\)|\([A-Z][a-zA-Z\.\' ]+,\s*\d{4}\)")
classes = {c for row in D.TAX for c in row[:3]}
for c in classes:
    if c not in D.BODY or not CITE.search(D.BODY[c]): fail.append(("body", c))
ids = {r[0] for r in SRC.S}
for f in D.FINDINGS:
    if not set(f[3]) <= ids: fail.append(("finding cites", f[0]))
    if not CITE.search(f[2]): fail.append(("finding form", f[0]))
if len(D.PUBS) < 50 or len(D.FINDINGS) < 15: fail.append(("counts", len(D.PUBS), len(D.FINDINGS)))
for fn in ("regtest_run_v1_0_0.json",):
    r = json.load(open(os.path.join(HERE, "ch13-evidence", fn)))
    if not r: fail.append(("record empty", fn))
LAB = {r[1] for r in SRC.S}
for k, v in D.BODY.items():
    for c in re.findall(r"\(([A-Z][a-zA-Z\.' ]+, \d{4})\)", v):
        if c not in LAB: fail.append(("body cites an unknown label", k, c))
cited = {c for v in list(D.BODY.values()) + [f[2] for f in D.FINDINGS] for c in re.findall(r"\(([A-Z][a-zA-Z\.' ]+, \d{4})\)", v)}
fail += [("source label never cited", l) for l in LAB - cited]
if len(D.PUBS) < 60 or len(D.FINDINGS) < 18 or len(ST.STORIES) < 4: fail.append(("counts", len(D.PUBS), len(D.FINDINGS), len(ST.STORIES)))
# 1.0.1: every io expression is a valid, double-quote-free one-liner, and the ABox literal compiles and equals it
import ast
_abox = os.path.join(HERE, "..", "03-materials", "ch13", "rdodi", "sen0401_ch13_domain_abox_v%s.ttl" % D.VERSION)
if os.path.exists(_abox):
    _in = {m.group(1): m.group(2).replace("\\\\", "\\") for m in re.finditer(r'chx:IO_(\w+) a [^\n]*?chx:input "((?:[^"\\]|\\.)*)"', open(_abox, encoding="utf-8").read())}
    for row in D.TAX:
        if row[5] and _in.get(row[2]) != row[5][0]: fail.append(("ABox input differs", row[2]))
    _out = {m.group(1): m.group(2).replace("\\\\", "\\") for m in re.finditer(r'chx:IO_(\w+) a [^\n]*?chx:output "((?:[^"\\]|\\.)*)"', open(_abox, encoding="utf-8").read())}
    for row in D.TAX:
        if row[5] and _out.get(row[2]) != row[5][1]: fail.append(("ABox output differs from the executed repr", row[2], _out.get(row[2]), row[5][1]))
        if row[5] and '"' in row[5][1]: fail.append(("double quote in expected output", row[2]))
    if len(_in) != sum(1 for r in D.TAX if r[5]): fail.append(("ABox io count", len(_in)))
else:
    fail.append(("ABox missing", _abox))

# 1.0.2: examples whose numbers can be changed: a self-contained expression (no library of the chapter), a whole-number literal of at most 50 outside quotes, and a different result when it is changed by up to 3
import ast
def _ev(src):
    t = ast.parse(src); last = t.body.pop(); ns = {}
    exec(compile(t, "x", "exec"), ns)
    return repr(eval(compile(ast.Expression(last.value), "x", "eval"), ns))
_LIT = re.compile(r"(?<![\w.'\"])\d+(?![\w.'\"])")
varied = []
for row in D.TAX:
    if not row[5] or "sen0401" in row[5][0]:
        continue
    code = row[5][0]
    chg = False
    for m in _LIT.finditer(code):
        if int(m.group(0)) > 50:
            continue
        for d in (-2, -1, 1, 2, 3):
            v = max(0, int(m.group(0)) + d)
            c2 = code[:m.start()] + str(v) + code[m.end():]
            try:
                out = _ev(c2)
            except BaseException:
                continue
            if out != row[5][1] and len(out) <= 80:
                chg = True; break
        if chg: break
    if chg: varied.append(row[2])
if len(varied) < 12: fail.append(("examples with changeable numbers", len(varied), varied))
print("sources %d fetched %d; passages %d in %d sources; stories %d; classes %d; findings %d; examples with changeable numbers %d" % (n, ok, nf, ns, len(ST.STORIES), len(classes), len(D.FINDINGS), len(varied)))
print("failures:", fail)
sys.exit(1 if fail else 0)
