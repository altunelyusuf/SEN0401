#!/usr/bin/env python3
"""Writes course_page_config_v2_14_0.json: the 2.11.0 configuration with the course-level ontologies re-read from disk, which now include the materials register 1.4.12 (it adds the entries of chapter 11
and its page 9.45). Nothing else changes: the exam identity and key, the playground, Code Lab, SPARQL samples, the CME standard digests and the programs are 2.11.0's, imported unchanged."""
__version__ = "2.14.0"
import json, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
prev = importlib.import_module("course_page_config_build_v2_13_0")
CFG = json.loads(json.dumps(prev.CFG))
CFG["_version"] = "2.14.0"
CFG["exam"] = json.load(open(os.path.join(HERE, "course_page_config_v2_13_0.json")))["exam"]   # the committed exam identity and public key, never re-derived (the builder of the key would make a new one on a machine without the instructor's)
CFG["corpus"]["course"] = prev.prev.prev.prev.prev.course_parts()
CFG["corpus"]["note"] = prev.CFG["corpus"]["note"] + " Since 2.14.0 the materials register is 1.4.12, which also registers the chapter 11 deck, document ontology, ontology package and page."
if __name__ == "__main__":
    out = os.path.join(HERE, "course_page_config_v2_14_0.json")
    json.dump(CFG, open(out, "w"), indent=1, ensure_ascii=False); print("course-level ontologies: %s" % ", ".join(CFG["corpus"]["course"])); print("wrote", out)
