#!/usr/bin/env python3
"""Runs RDODI's own pipeline validator (the newest in the Ontologies checkout, all of its gates, Stage4.A-L, Cross.B-C included) on one SEN0401 chapter's RDODI artefacts and its Stage 4 page ABox.
Usage: sen0401_stage4_gates_v1_0_0.py NN [validator-dir [vocabulary-dir]]
The validator and its gates are used as they stand; nothing is changed, relaxed or re-implemented here. The stage vocabularies (research, document, interactive-page ontologies and
their SHACL) are read from the pinned ecosystem checkout, because the Ontologies checkout carries the validator but not the vocabulary files. Exit 1 when any gate fails."""
__version__ = "1.1.0"
# v1.1.0 over 1.0.0: N may be "numbers" (the supplementary page), whose folder and file names carry no "ch" prefix.
import glob, importlib.util, os, sys
N = sys.argv[1]
VD = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("RDODI_VALIDATOR_DIR", "/home/claude/Ontologies/rdodi-ecosystem/02-gates")
VOC = sys.argv[3] if len(sys.argv) > 3 else os.environ.get("RDODI_VOCAB_DIR", "/home/claude/eco_pin/rdodi-ecosystem/01-stage-vocabularies")
REPO = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = N if N == "numbers" else "ch" + N
RD = os.path.join(REPO, "03-materials", K, "rdodi")
vk = lambda p: [int(x) for x in os.path.splitext(p.rsplit("_v", 1)[1])[0].split("_")]
newest = lambda pat: sorted(glob.glob(pat), key=vk)[-1]
V = newest(os.path.join(VD, "rdodi_pipeline_validator_v*.py"))
sys.path.insert(0, VD)
spec = importlib.util.spec_from_file_location("rdodi_validator", V); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
part = lambda p: newest(os.path.join(RD, "sen0401_%s_%s_v*.ttl" % (K, p)))
cfg = {"research": part("research"), "research_shacl": newest(os.path.join(VOC, "01-research", "research_ontology_shacl_v*.ttl")),
       "domain_tbox": part("domain_tbox"), "domain_abox": part("domain_abox"), "domain_shacl": part("domain_shacl"), "document_ttl": part("document"),
       "rdodi_doc_tbox": newest(os.path.join(VOC, "03-document", "document_ontology_tbox_v*.ttl")), "rdodi_doc_shacl": newest(os.path.join(VOC, "03-document", "document_ontology_shacl_v*.ttl")),
       "page_ttl": newest(os.path.join(REPO, "03-materials", K, "page", "sen0401_%s_page_abox_v*.ttl" % K)),
       "rdodi_page_tbox": newest(os.path.join(VOC, "04-interactive-page", "interactive_page_ontology_tbox_v*.ttl")), "rdodi_page_shacl": newest(os.path.join(VOC, "04-interactive-page", "interactive_page_ontology_shacl_v*.ttl"))}
print("validator:", os.path.basename(V))
for k in ("research", "domain_tbox", "domain_abox", "domain_shacl", "document_ttl", "page_ttl"): print("  %s: %s" % (k, os.path.basename(cfg[k])))
out = m.validate(cfg)
for r in out: print(r)
bad = [r for r in out if r.verdict == "FAIL"]
print("OVERALL:", "PASS" if not bad else "FAIL (%d)" % len(bad)); sys.exit(1 if bad else 0)
