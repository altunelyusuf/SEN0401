#!/usr/bin/env python3
"""Builds a SEN0401 page - a chapter, or a named unit such as "numbers" - from the course-neutral template shared
with SEN0414 (course_page_template_v9_4_2.html, byte-identical), with SEN0401's text from its course configuration.
The page embeds, as Turtle with file names and hashes, the corpus its agents search: the unit's RDODI ontology,
document and research record (SEN0401 has no textbook or course ontology yet). The unit's extras (the numbers
page's charts) are appended. Usage: sen0401_page_build_v4_0_0.py <NN|unit>"""
__version__ = "4.0.0"
import glob, hashlib, json, os, sys
import rdflib
PV = os.environ.get("PAGE_VER", "9_4_2")  # generated files carry the page version they were produced for
N = sys.argv[1]; N = ("ch%s" % N) if N.isdigit() else N
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = open(os.path.join(REPO, "08-tooling", os.environ.get("PAGE_TEMPLATE", "course_page_template_v9_4_2.html"))).read()
P = os.path.join(REPO, "08-tooling", "%s-page" % N)
d = json.load(open(os.path.join(P, "page_data_v%s.json" % PV))); C = d["course"]["corpus"]
safe = lambda o: json.dumps(o).replace("</", "<\\/")
vkey = lambda x: [int(v) for v in x.rsplit("_v", 1)[1].split(".")[0].split("_")]
latest = lambda pat: sorted(glob.glob(pat), key=vkey)[-1]
blocks, log = [], []
def add(kind, name, text):
    h = hashlib.sha256(text.encode()).hexdigest()[:16]
    blocks.append('<script type="text/turtle" data-kind="%s" data-name="%s" data-sha256="%s">%s</script>' % (kind, name, h, text.replace("</script", "<\\/script")))
    log.append("%s %s %s" % (kind, name, h))
for path in C.get("course", []): add("course", os.path.basename(path), open(os.path.join(REPO, path)).read())
RD = os.path.join(REPO, "03-materials", N, "rdodi")
for part, kind in (("domain_tbox", "chapter"), ("domain_abox", "chapter"), ("document", "chapter"), ("research", "research")):
    f = latest(os.path.join(RD, "sen0401_%s_%s_v*.ttl" % (N, part))); add(kind, os.path.basename(f), open(f).read())
LG = rdflib.Graph(); LG.parse(latest(os.path.join(REPO, "07-lineage", "*.ttl")), format="turtle")
BK = rdflib.Namespace("http://example.org/backlog#"); mis = next(LG.subjects(rdflib.RDF.type, BK.Mission), None)
d["mission"] = {"statement": str(LG.value(mis, BK.hasMissionStatement) or ""), "outcome": str(LG.value(mis, BK.hasMissionOutcome) or ""),
                "goals": sorted(str(LG.value(g, rdflib.RDFS.label)) for g in LG.subjects(rdflib.RDF.type, BK.Goal)),
                "objectives": sorted(str(LG.value(o, rdflib.RDFS.label)) for o in LG.subjects(rdflib.RDF.type, BK.Objective))}
unwrap = lambda x: x["items"] if isinstance(x, dict) and "items" in x else x
QUIZ = unwrap(json.load(open(latest(os.path.join(P, "quiz_v*.json"))))); OBJ = json.load(open(latest(os.path.join(P, "objectives_v*.json"))))
sub = d["unit"]["sub"] if d.get("unit") else d["course"]["chapter_sub"].replace("{n}", str(d["chapter"]))
h = (T.replace("__TITLE__", d["title"]).replace("__PAGEVERSION__", PV.replace("_", ".")).replace("__COURSE__", d["course"]["line"]).replace("__SUB__", sub)
      .replace("__PY__", d["python"]).replace("__DATA__", safe(d)).replace("__QUIZ__", safe(QUIZ)).replace("__OBJ__", safe(OBJ)).replace("__CORPUS__", "\n".join(blocks)))
X = os.path.join(P, "extra_resolved_v%s.html" % PV)
h = h.replace("</body></html>", (open(X).read() if os.path.exists(X) else "") + "</body></html>")
out = os.path.join(REPO, "03-materials", N, "page", "sen0401_%s_page_v%s.html" % (N, PV))
open(out, "w").write(h); json.dump({"_version": PV.replace("_", "."), "items": log}, open(os.path.join(P, "corpus_manifest_v%s.json" % PV), "w"), indent=1)
print("written", out, len(h), "bytes; corpus:", "; ".join(log))
