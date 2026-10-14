#!/usr/bin/env python3
"""Runs RDODI's own pipeline validator (rdodi_pipeline_validator, Stages 1-4) on a SEN0401 chapter's RDODI artefacts, for any chapter, against any ecosystem checkout.
Usage: sen0401_rdodi_gates_v1_2_0.py <NN> [<rdodi-ecosystem-dir>] [<artefact-version, e.g. 1_0_2>]
Exits 1 when any gate fails. Gates the validator does not implement are checked by sen0401_rdodi_checks_v1_0_0.py.
1.2.0 (over SEN0401's 1.0.0, which forked SEN0414's 1.1.0): (a) the ecosystem directory defaults to the pinned checkout /home/claude/eco_pin/rdodi-ecosystem (the pin SEN0414's chapters
13-25 were gated against; environment RDODI_ECO overrides); (b) with no version given, the NEWEST file of each part is used, as SEN0414's 1.1.1 does, so a chapter whose parts moved
separately (chapter 7: research 1.0.0, ontology and document 1.1.0) is gated as it stands; with a version, every part must exist at that version, exactly as 1.0.0 did; (c) SEN0401_ROOT
points the gates at a scratch copy of the repository; (d) the chosen files and the validator are printed, so a gate result can be tied to bytes."""
__version__ = "1.2.0"
import glob, importlib.util, os, sys
N = sys.argv[1]; ECO = sys.argv[2] if len(sys.argv) > 2 else os.environ.get("RDODI_ECO", "/home/claude/eco_pin/rdodi-ecosystem"); AV = sys.argv[3] if len(sys.argv) > 3 else None
REPO = os.environ.get("SEN0401_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RD = os.path.join(REPO, "03-materials", "ch%s" % N, "rdodi")
vk = lambda p: [int(x) for x in os.path.splitext(p.rsplit("_v", 1)[1])[0].split("_")]
def newest(pattern):
    return sorted(glob.glob(pattern), key=vk)[-1]
V = newest(os.path.join(ECO, "02-gates", "rdodi_pipeline_validator_v*.py"))
spec = importlib.util.spec_from_file_location("rdodi_validator", V); m = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.join(ECO, "02-gates")); spec.loader.exec_module(m)
SV = os.path.join(ECO, "01-stage-vocabularies")
def part(p):
    if AV:
        f = os.path.join(RD, "sen0401_ch%s_%s_v%s.ttl" % (N, p, AV))
        if not os.path.exists(f): sys.exit("REFUSED: %s does not exist (artefact version %s asked for)" % (f, AV))
        return f
    return newest(os.path.join(RD, "sen0401_ch%s_%s_v*.ttl" % (N, p)))
pg = glob.glob(os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0401_ch%s_page_abox_v*.ttl" % N))
cfg = {"research": part("research"), "research_shacl": newest(os.path.join(SV, "01-research", "research_ontology_shacl_v*.ttl")),
       "domain_tbox": part("domain_tbox"), "domain_abox": part("domain_abox"), "domain_shacl": part("domain_shacl"), "document_ttl": part("document"),
       "rdodi_doc_tbox": newest(os.path.join(SV, "03-document", "document_ontology_tbox_v*.ttl")), "rdodi_doc_shacl": newest(os.path.join(SV, "03-document", "document_ontology_shacl_v*.ttl")),
       "page_ttl": newest(os.path.join(REPO, "03-materials", "ch%s" % N, "page", "sen0401_ch%s_page_abox_v*.ttl" % N)) if pg else "",
       "rdodi_page_tbox": newest(os.path.join(SV, "04-interactive-page", "interactive_page_ontology_tbox_v*.ttl")), "rdodi_page_shacl": newest(os.path.join(SV, "04-interactive-page", "interactive_page_ontology_shacl_v*.ttl"))}
out = []
out.append(m.gate_parse("Stage1.A", cfg["research"])); out.append(m.gate_shacl("Stage1.B", [cfg["research"]], cfg["research_shacl"]))
out.append(m.gate_parse("Stage2.A", cfg["domain_tbox"])); out.append(m.gate_shacl("Stage2.C", [cfg["domain_tbox"], cfg["domain_abox"]], cfg["domain_shacl"]))
out.append(m.gate_parse("Stage3.A", cfg["document_ttl"])); out.append(m.gate_reference_rule("Stage3.F", cfg["document_ttl"], cfg["research"]))
out.append(m.gate_shacl("Stage3.B", [cfg["document_ttl"], cfg["domain_tbox"], cfg["domain_abox"]], cfg["rdodi_doc_shacl"]))
out.append(m.gate_coverage_rule("Stage3.E.cov", cfg["document_ttl"], cfg["rdodi_doc_tbox"], cfg["rdodi_doc_shacl"], "document-ontology#"))
out.append(m.gate_substance_rule("Stage3.E.sub", cfg["document_ttl"], cfg["rdodi_doc_tbox"], cfg["rdodi_doc_shacl"], "document-ontology#"))
out.append(m.gate_source_validity("Stage3.src", cfg["document_ttl"]))
if cfg["page_ttl"]:
    out.append(m.gate_parse("Stage4.A", cfg["page_ttl"])); out.append(m.gate_shacl("Stage4.B", [cfg["page_ttl"], cfg["document_ttl"]], cfg["rdodi_page_shacl"]))
    out.append(m.gate_coverage_rule("Stage4.cov", cfg["page_ttl"], cfg["rdodi_page_tbox"], cfg["rdodi_page_shacl"], "interactive-page-ontology#"))
    out.append(m.gate_substance_rule("Stage4.sub", cfg["page_ttl"], cfg["rdodi_page_tbox"], cfg["rdodi_page_shacl"], "interactive-page-ontology#"))
    out.append(m.gate_source_validity("Stage4.src", cfg["page_ttl"])); out.append(m.gate_provenance("Cross.B", cfg["page_ttl"], cfg["document_ttl"], cfg["domain_tbox"]))
print("validator:", os.path.basename(V), "| ecosystem:", ECO)
for k in ("research", "domain_tbox", "domain_abox", "domain_shacl", "document_ttl", "page_ttl"):
    if cfg[k]: print("  %s: %s" % (k, os.path.basename(cfg[k])))
for r in out: print(r)
bad = [r for r in out if r.verdict == "FAIL"]
print("OVERALL:", "PASS" if not bad else "FAIL (%d)" % len(bad)); sys.exit(1 if bad else 0)
