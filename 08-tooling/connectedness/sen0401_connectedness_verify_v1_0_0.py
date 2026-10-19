#!/usr/bin/env python3
"""sen0401_connectedness_verify v1_0_0 - read-only verification of one SEN0401 chapter T-Box after (or before) a connectedness repair.

Usage: sen0401_connectedness_verify_v1_0_0.py KEY [--repo DIR] [--json OUT]       KEY = 01..14 or numbers

Measures, on the newest domain T-Box of the chapter: classes, standing alone, islands (oe_connectedness, the same code CI Gate C runs), and the same
measure with the property chx:hasOwner left out of the graph (so that a repair cannot lean on a property whose domain and range are a union of
every type the data shows); runs RDODI's own pipeline validator (all gates, the chapter's Stage 4 page ABox included) on the newest file of each part;
and HermiT consistency of T-Box + ABox (owlready2 + Java). Nothing is written into the repository."""
__version__ = "1.0.0"
import argparse, glob, importlib.util, json, os, re, shutil, sys, tempfile
sys.dont_write_bytecode = True
ap = argparse.ArgumentParser(); ap.add_argument("key"); ap.add_argument("--repo", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))); ap.add_argument("--json")
a = ap.parse_args()
N = a.key; REPO = a.repo
TOOLS = os.environ.get("OE_REPO_TOOLING", "/home/claude/Ontologies/repo-tooling")
VD = os.environ.get("RDODI_VALIDATOR_DIR", "/home/claude/Ontologies/rdodi-ecosystem/02-gates")
VOC = os.environ.get("RDODI_VOCAB_DIR", "/home/claude/eco_pin/rdodi-ecosystem/01-stage-vocabularies")
vk = lambda p: [int(x) for x in re.search(r"_v(\d+)_(\d+)_(\d+)\.", p).groups()]
newest = lambda pat: sorted(glob.glob(pat), key=vk)[-1]
RD = os.path.join(REPO, "03-materials", "ch%s" % N if N != "numbers" else "numbers", "rdodi")
stem = "sen0401_%s" % (("ch" + N) if N != "numbers" else "numbers")
part = lambda p: newest(os.path.join(RD, "%s_%s_v*.ttl" % (stem, p)))
sys.path.insert(0, TOOLS)
import oe_connectedness_v1_0_0 as cm
from rdflib import Graph, URIRef
res = {"key": N}
tb = part("domain_tbox"); res["tbox"] = os.path.relpath(tb, REPO)
m = cm.measure(tb)
res["classes"] = m["classes"]; res["alone"] = len(m["alone"]); res["islands"] = len(m["islands"]); res["outward_only"] = len(m["outward_only"])
g = Graph(); g.parse(tb)
for t in list(g.triples((None, None, None))):
    if str(t[0]).endswith("#hasOwner") or str(t[2]).endswith("#hasOwner"): g.remove(t)
tmp = tempfile.mkdtemp(prefix="cn_"); p = os.path.join(tmp, "x_tbox_v1_0_0.ttl"); g.serialize(p, format="turtle")
m2 = cm.measure(p); res["alone_without_hasOwner"] = len(m2["alone"]); res["islands_without_hasOwner"] = len(m2["islands"])
shutil.rmtree(tmp, ignore_errors=True)
spec = importlib.util.spec_from_file_location("rdodi_validator", newest(os.path.join(VD, "rdodi_pipeline_validator_v*.py"))); v = importlib.util.module_from_spec(spec)
sys.path.insert(0, VD); spec.loader.exec_module(v)
pagedir = os.path.join(REPO, "03-materials", "ch%s" % N if N != "numbers" else "numbers", "page")
cfg = {"research": part("research"), "research_shacl": newest(os.path.join(VOC, "01-research", "research_ontology_shacl_v*.ttl")),
       "domain_tbox": tb, "domain_abox": part("domain_abox"), "domain_shacl": part("domain_shacl"), "document_ttl": part("document"),
       "rdodi_doc_tbox": newest(os.path.join(VOC, "03-document", "document_ontology_tbox_v*.ttl")), "rdodi_doc_shacl": newest(os.path.join(VOC, "03-document", "document_ontology_shacl_v*.ttl")),
       "page_ttl": (glob.glob(os.path.join(pagedir, "%s_page_abox_v*.ttl" % stem)) and newest(os.path.join(pagedir, "%s_page_abox_v*.ttl" % stem))) or None,
       "rdodi_page_tbox": newest(os.path.join(VOC, "04-interactive-page", "interactive_page_ontology_tbox_v*.ttl")), "rdodi_page_shacl": newest(os.path.join(VOC, "04-interactive-page", "interactive_page_ontology_shacl_v*.ttl"))}
if cfg["page_ttl"]:
    out = v.validate(cfg)
else:  # chapters 5-7 have no Stage 4 page ABox: the Stage 1-3 gates, as the chapter check runs them
    c = cfg; N_ = lambda *x: newest(os.path.join(VOC, *x))
    out = [v.gate_parse("Stage1.A", c["research"]), v.gate_shacl("Stage1.B", [c["research"]], c["research_shacl"]),
           v.gate_parse("Stage2.A", c["domain_tbox"]), v.gate_shacl("Stage2.C", [c["domain_tbox"], c["domain_abox"]], c["domain_shacl"]),
           v.gate_parse("Stage3.A", c["document_ttl"]), v.gate_reference_rule("Stage3.F", c["document_ttl"], c["research"]),
           v.gate_shacl("Stage3.B", [c["document_ttl"], c["domain_tbox"], c["domain_abox"]], c["rdodi_doc_shacl"]),
           v.gate_coverage_rule("Stage3.E.cov", c["document_ttl"], c["rdodi_doc_tbox"], c["rdodi_doc_shacl"], "document-ontology#"),
           v.gate_substance_rule("Stage3.E.sub", c["document_ttl"], c["rdodi_doc_tbox"], c["rdodi_doc_shacl"], "document-ontology#"),
           v.gate_source_validity("Stage3.src", c["document_ttl"])]
res["gates"] = {re.match(r"\[\s*\S+\s*\]\s*([^:]+):", str(r)).group(1).replace(" [PROPOSED]", ""): r.verdict for r in out}
try:
    import owlready2
    gg = Graph(); gg.parse(tb); gg.parse(cfg["domain_abox"])
    d = tempfile.mkdtemp(prefix="hermit_"); px = os.path.join(d, "o.owl"); gg.serialize(px, format="xml")
    onto = owlready2.get_ontology("file://" + px).load()
    try:
        with onto: owlready2.sync_reasoner_hermit(infer_property_values=False)
        res["hermit"] = "consistent"
    except owlready2.OwlReadyInconsistentOntologyError:
        res["hermit"] = "INCONSISTENT"
    shutil.rmtree(d, ignore_errors=True)
except Exception as e:
    res["hermit"] = "error: %s" % str(e)[:200]
print(json.dumps(res))
if a.json: json.dump(res, open(a.json, "w"), indent=1)
