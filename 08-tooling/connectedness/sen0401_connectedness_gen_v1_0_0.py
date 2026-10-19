#!/usr/bin/env python3
"""sen0401_connectedness_gen v1_0_0 - writes the NEW MINOR version of one chapter's domain T-Box from its spec (spec_KEY.py), never touching the committed file.
Usage: sen0401_connectedness_gen_v1_0_0.py KEY        KEY = 01..14 | numbers
The new file = the newest committed T-Box, byte for byte, plus (1) a header that names the new version (versionInfo, versionIRI, identifier, owl:priorVersion,
prov:wasRevisionOf, modified, a skos:changeNote), (2) domain and range for chx:hasOwner where the file declares it (the union of every type the A-Box shows,
BP-D57 step 3), (3) chx:input and chx:output declared as datatype properties of rd:IOExample, (4) the spec's object properties, each with label, comment (the
claim and its basis in the chapter) and one domain and one range class. Nothing else changes: no class is added, removed or renamed."""
__version__ = "1.0.0"
import glob, importlib.util, os, re, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE))
KEY = sys.argv[1]; TODAY = "2026-10-19"
spec = importlib.util.spec_from_file_location("spec", os.path.join(HERE, "spec_%s.py" % KEY)); S = importlib.util.module_from_spec(spec); spec.loader.exec_module(S)
sub = "ch%s" % KEY if KEY != "numbers" else "numbers"; stem = "sen0401_%s" % sub
RD = os.path.join(REPO, "03-materials", sub, "rdodi")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
old = sorted(glob.glob(os.path.join(RD, stem + "_domain_tbox_v*.ttl")), key=vk)[-1]
ov = ".".join(map(str, vk(old))); nvv = vk(old); nv = "%d.%d.0" % (nvv[0], nvv[1] + 1)
new = os.path.join(RD, "%s_domain_tbox_v%s.ttl" % (stem, nv.replace(".", "_")))
assert not os.path.exists(new), "refusing to overwrite " + new
t = open(old, encoding="utf-8").read()
base = "http://example.org/sen0401/%s/tbox" % sub
assert ('<%s/%s>' % (base, ov)) in t or ('owl:versionInfo "%s"' % ov) in t
# header
t = t.replace('owl:versionInfo "%s"' % ov, 'owl:versionInfo "%s"' % nv, 1)
t = t.replace('owl:versionIRI <%s/%s>' % (base, ov), 'owl:versionIRI <%s/%s>' % (base, nv), 1)
idl = re.search(r'dcterms:identifier "%s_tbox_v%s" ;[^\n]*\n' % (stem, ov.replace(".", "_")), t)
assert idl, "identifier line"
line = idl.group(0)
rest = re.sub(r'prov:wasRevisionOf <[^>]*> ;', '', line.split(";", 1)[1]).strip()
note = S.NOTE.replace('"', "'")
newline = ('dcterms:identifier "%s_tbox_v%s" ;\n    owl:priorVersion <%s/%s> ; prov:wasRevisionOf <%s/%s> ;\n    skos:changeNote "%s"@en ;\n' % (stem, nv.replace(".", "_"), base, ov, base, ov, note))
if rest: newline += "    " + rest + "\n"
t = t.replace(line, newline, 1)
t = re.sub(r'(dcterms:modified )"[^"]*"(\^\^xsd:date)', r'\1"%s"\2' % TODAY, t, count=1)
# hasOwner
if "chx:hasOwner a owl:ObjectProperty" in t:
    from rdflib import Graph, RDF, OWL
    ab = sorted(glob.glob(os.path.join(RD, stem + "_domain_abox_v*.ttl")), key=vk)[-1]
    a = Graph(); a.parse(ab)
    P = [p for p in set(a.predicates()) if str(p).endswith("#hasOwner")][0]
    ty = lambda x: {str(u).split("#")[-1] for u in a.objects(x, RDF.type) if u != OWL.NamedIndividual}
    D, R = set(), set()
    for s_, o_ in a.subject_objects(P): D |= ty(s_); R |= ty(o_)
    un = lambda xs: "[ a owl:Class ; owl:unionOf ( %s ) ]" % " ".join("chx:" + x for x in sorted(xs))
    m = re.search(r'chx:hasOwner a owl:ObjectProperty ;[^\n]*\.\n', t); assert m
    l0 = m.group(0).rstrip()[:-1].rstrip()
    l1 = l0 + ' ;\n    rdfs:comment "A concept owned by the concept it belongs to, as the chapter\'s examples use it between typed things; domain and range are the union of every type the A-Box shows on the two sides (BP-D57 step 3)."@en ;\n    rdfs:domain %s ;\n    rdfs:range %s ;\n    rdfs:isDefinedBy <%s> .\n' % (un(D), un(R), base)
    t = t.replace(m.group(0), l1, 1)
# appended block
out = ["\n#################################################################\n# Connectedness repair (discipline v2.19.0, BP-D56 and BP-D57), %s.\n# The datatype properties the A-Box uses and nothing declared, then the relations\n# between the chapter's subject branches that the chapter's own sources state.\n#################################################################\n" % TODAY]
out.append('chx:input a owl:DatatypeProperty ; rdfs:label "input expression"@en ; rdfs:comment "The expression an input/output example evaluates."@en ; rdfs:domain rd:IOExample ; rdfs:range xsd:string ; rdfs:isDefinedBy <%s> .\n' % base)
out.append('chx:output a owl:DatatypeProperty ; rdfs:label "output value"@en ; rdfs:comment "The value that evaluating the example expression gives."@en ; rdfs:domain rd:IOExample ; rdfs:range xsd:string ; rdfs:isDefinedBy <%s> .\n' % base)
def cls(x): return "chx:" + x if isinstance(x, str) else "[ a owl:Class ; owl:unionOf ( %s ) ]" % " ".join("chx:" + y for y in x)
for p in S.PROPS:
    c = p["why"].replace('"', "'")
    out.append('chx:%s a owl:ObjectProperty ; rdfs:label "%s"@en ;\n    rdfs:comment "%s"@en ;\n    rdfs:domain %s ; rdfs:range %s ; rdfs:isDefinedBy <%s> .\n' % (p["id"], p["label"], c, cls(p["dom"]), cls(p["rng"]), base))
if not t.endswith("\n"): t += "\n"
t += "".join(out)
open(new, "w", encoding="utf-8").write(t)
print(os.path.relpath(new, REPO))
# decisions file next to the T-Box
sys.path.insert(0, "/home/claude/Ontologies/repo-tooling")
import oe_connectedness_v1_0_0 as cm
b, n_ = cm.measure(old), cm.measure(new)
from rdflib import Graph
g2 = Graph(); g2.parse(new)
for tr in list(g2.triples((None, None, None))):
    if str(tr[0]).endswith("#hasOwner") or str(tr[2]).endswith("#hasOwner"): g2.remove(tr)
import tempfile, shutil
td = tempfile.mkdtemp(); pp = os.path.join(td, "x_tbox_v1_0_0.ttl"); g2.serialize(pp, format="turtle"); n2 = cm.measure(pp); shutil.rmtree(td)
nvu = nv.replace(".", "_")
md = ["# SEN0401 %s - connectedness and link decisions for the domain T-Box %s\n" % (sub, nv),
      "Written %s by the connectedness repair of the branch connectedness-repair. The committed T-Box %s is untouched; %s is the new version (MINOR: no class added, removed or renamed).\n" % (TODAY, ov, nv),
      "## Measured (oe_connectedness, discipline v2.18.0 BP-D56)\n",
      "| | classes | standing alone | islands |\n|---|---|---|---|\n| before (%s) | %d | %d | %d |\n| after (%s) | %d | %d | %d |\n| after, with chx:hasOwner left out of the graph | %d | %d | %d |\n" % (ov, b["classes"], len(b["alone"]), len(b["islands"]), nv, n_["classes"], len(n_["alone"]), len(n_["islands"]), n2["classes"], len(n2["alone"]), len(n2["islands"])),
      "The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.\n",
      "## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)\n",
      "| property | label | domain | range | basis |\n|---|---|---|---|---|"]
for p in S.PROPS:
    md.append("| chx:%s | %s | %s | %s | %s |" % (p["id"], p["label"], p["dom"], p["rng"], p["why"].split("Basis:")[-1].strip().replace("|", "/")))
md.append("\n## Classes for which no honest relation was found\n")
md.append("\n".join("- %s: %s" % x for x in S.NO_RELATION) if getattr(S, "NO_RELATION", None) else "None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.")
md.append("\n## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate\n")
md.append("| candidate | trust | decision | reason |\n|---|---|---|---|")
dec = []
if "chx:hasOwner a owl:ObjectProperty" in t:
    dec.append(("SEM-1 hasOwner", "high", "set", "domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3)"))
dec.append(("SYN-2 input, output", "high", "declare", "chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment"))
dec += list(getattr(S, "DECISIONS", []))
for d_ in dec: md.append("| %s | %s | %s | %s |" % d_)
open(os.path.join(RD, "%s_connectedness_decisions_v%s.md" % (stem, nvu)), "w", encoding="utf-8").write("\n".join(md) + "\n")
tsv = [x for x in getattr(S, "REJECTED", [])]
if tsv:
    open(os.path.join(RD, "%s_link_decisions_v%s.tsv" % (stem, nvu)), "w", encoding="utf-8").write("".join("\t".join(x) + "\n" for x in tsv))
print("before", len(b["alone"]), len(b["islands"]), "after", len(n_["alone"]), len(n_["islands"]), "without hasOwner", len(n2["alone"]), len(n2["islands"]))
