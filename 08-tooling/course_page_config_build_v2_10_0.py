#!/usr/bin/env python3
"""Writes course_page_config_v2_10_0.json: the 2.9.0 configuration plus the CME standard the pages now read.

The owner's ruling of 2026-10-07 (14:46): a paragraph gets the diagram its narrative calls for, and the mapping from
narrative pattern to diagram type lives in the CME ontology so that every course reuses it. The mapping is a module
of CME's standards-adoption ontology - cme_standards_adoption_tbox_v1_1_0.ttl (the vocabulary) and
cme_standards_adoption_v1_3_0.ttl (ten patterns, eleven diagram types) in altunelyusuf/cme at 0.16.0 (commit e3a36ce). This configuration records where the two files are read from - the CME checkout named by
CME_REPO (default /home/claude/cme), its package version - and the SHA-256 of each file's bytes at configuration time,
so the data builder and the page build refuse a file that changed under the pin (the same discipline as the book
pin: the pages say exactly which bytes of the standard they were built from). The materials register moved to 1.4.8
(pages 9.41.0). The programs and everything else are 2.9.0's, imported.
"""
__version__ = "2.10.0"
import hashlib, json, os, sys, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
prev = importlib.import_module("course_page_config_build_v2_9_0")
CME_REPO = os.environ.get("CME_REPO", "/home/claude/cme")
CME_FOLDER = "cme"
STANDARD_FILES = ["00-standards/cme_standards_adoption_tbox_v1_1_0.ttl", "00-standards/cme_standards_adoption_v1_3_0.ttl"]

def standards():
    out = []
    for p in STANDARD_FILES:
        fp = os.path.join(CME_REPO, CME_FOLDER, p)
        if not os.path.exists(fp):
            raise SystemExit("the CME standard %s is not at %s; set CME_REPO to a checkout of altunelyusuf/cme that holds it" % (p, fp))
        out.append({"repository": "altunelyusuf/cme", "folder": CME_FOLDER, "path": p, "sha256": hashlib.sha256(open(fp, "rb").read()).hexdigest(),
                    "role": "CME standards adoption, carrying the narrative-to-diagram mapping module (the owner's ruling of 2026-10-07)"})
    return out

CFG = dict(prev.CFG)
CFG["_version"] = "2.10.0"
CFG["corpus"] = dict(prev.CFG["corpus"])
CFG["corpus"]["course"] = prev.course_parts()
CFG["corpus"]["standards"] = standards()
CFG["corpus"]["standards_package_version"] = open(os.path.join(CME_REPO, CME_FOLDER, "VERSION.txt")).read().strip()
CFG["corpus"]["standards_commit"] = __import__("subprocess").run(["git", "-C", CME_REPO, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
CFG["corpus"]["note"] = prev.CFG["corpus"]["note"] + (" Since 2.10.0 the page also embeds the CME narrative-to-diagram mapping (corpus.standards, read from a checkout of "
    "altunelyusuf/cme at the recorded file digests), which types the chapter's narrative diagrams.")

if __name__ == "__main__":
    interps = sys.argv[1:] or ["python3", "/root/.local/bin/python3.14"]
    bad = prev.base.run_checks(interps)
    print("%d programs x %d interpreters: %s" % (len(prev.base.PATTERNS) + len(prev.base.TRACE) + len(prev.base.CODELAB), len(interps), "all ran" if not bad else "FAILURES"))
    for b in bad: print(" -", b)
    if bad: sys.exit(1)
    print("course-level ontologies: %s" % ", ".join(CFG["corpus"]["course"]))
    for s in CFG["corpus"]["standards"]: print("standard %s sha256 %s (cme %s)" % (s["path"], s["sha256"][:16], CFG["corpus"]["standards_package_version"]))
    out = os.path.join(HERE, "course_page_config_v2_10_0.json")
    json.dump(CFG, open(out, "w"), indent=1, ensure_ascii=False); print("wrote", out)
