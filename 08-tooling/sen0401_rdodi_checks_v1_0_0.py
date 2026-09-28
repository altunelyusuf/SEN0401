#!/usr/bin/env python3
"""Checks a chapter's RDODI artefacts against execution, for what RDODI's validator does not implement.
1. Every input-output example of the chapter's taxonomy, and every extra claim, is executed under the given interpreter
   and its result compared with the one the artefact states.
2. Every individual the taxonomy defines exists in the ABox and every taxonomy class in the TBox (no leaf lost).
3. The TBox and ABox are consistent under HermiT (owlready2), when Java and owlready2 are present.
Usage: sen0401_rdodi_checks_v1_0_0.py <data-module> <python-interpreter>. Exits 1 on any mismatch."""
__version__ = "1.0.0"
# Forked from SEN0414 checks 1.0.0 (to be consolidated into CME): the behaviours come from the data module (BEH); names and paths are SEN0401's; the artefact version is the data module's VERSION.
import importlib, os, subprocess, sys
D = importlib.import_module(sys.argv[1]); PY = sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); N = "%02d" % D.CH; AV = getattr(D, "VERSION", "1_0_0")
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi")
WRAP = "import ast\nsrc = %r\nt = ast.parse(src)\nns = {}\nlast = t.body.pop()\nexec(compile(t, 'claim', 'exec'), ns)\nprint(repr(eval(compile(ast.Expression(last.value), 'claim', 'eval'), ns)))"
def run(expr):
    # a claim is an expression, or statements whose last line is the expression; run from the repository root so evidence files resolve
    r = subprocess.run([PY, "-c", WRAP % expr], capture_output=True, text=True, cwd=REPO)
    return r.stdout.strip() if r.returncode == 0 else "%s" % r.stderr.strip().splitlines()[-1]
bad = []; n = 0
for top, mid, leaf, ex, d, io in D.TAX:
    if io:
        n += 1; got = run(io[0])
        if got != io[1]: bad.append(("io", leaf, io[0], io[1], got))
for expr, want in getattr(D, "CLAIMS", []):
    n += 1; got = run(expr)
    if got != want: bad.append(("claim", "", expr, want, got))
# behaviours stated in prose, executed: the data module's BEH, when it has one
BEH = getattr(D, "BEH", [])
for what, code, want in BEH:
    n += 1; r = subprocess.run([PY, "-W", "ignore::SyntaxWarning", "-c", code], capture_output=True, text=True); got = r.stdout.strip() if r.returncode == 0 else r.stderr.strip().splitlines()[-1]
    if got != want: bad.append(("behaviour", what, code[:60], want, got))
import rdflib
from rdflib import RDF, OWL
T = rdflib.Graph().parse(os.path.join(RD, "sen0401_ch%s_domain_tbox_v%s.ttl" % (N, AV))); A = rdflib.Graph().parse(os.path.join(RD, "sen0401_ch%s_domain_abox_v%s.ttl" % (N, AV)))
CH = rdflib.Namespace("http://example.org/sen0401/ch%s#" % N)
classes = {t for row in D.TAX for t in row[:3]}; n += 1
missing = [c for c in classes if (CH[c], RDF.type, OWL.Class) not in T]
if missing: bad.append(("tbox", "classes", "", "all", str(missing)))
leaves = [row[2] for row in D.TAX]
missing = [l for l in leaves if (CH["X_" + l], RDF.type, CH[l]) not in A]
if missing: bad.append(("abox", "individuals", "", "all", str(missing)))
try:
    import owlready2, tempfile
    g = rdflib.Graph(); g += T; g += A; f = tempfile.NamedTemporaryFile(suffix=".owl", delete=False); g.serialize(f.name, format="xml")
    w = owlready2.get_ontology("file://" + f.name).load(); owlready2.sync_reasoner_hermit([w], infer_property_values=False); inc = list(owlready2.default_world.inconsistent_classes())
    print("HermiT: consistent" if not inc else "HermiT: INCONSISTENT %s" % inc)
    if inc: bad.append(("hermit", "", "", "consistent", str(inc)))
except Exception as e:
    print("HermiT not run: %s" % str(e).splitlines()[0][:100])
print("%d checks; %d mismatches" % (n, len(bad)))
for b in bad: print("  MISMATCH", b)
sys.exit(1 if bad else 0)
