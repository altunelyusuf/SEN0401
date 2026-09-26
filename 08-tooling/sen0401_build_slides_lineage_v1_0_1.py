#!/usr/bin/env python3
"""sen0401_build_slides_lineage v1_0_0 - the SEN0401 slide-renewal lineage, one stage per commit.

STAGES names how many stages are closed; COMMITS records the commit that closed each, filled in
from the publish result - never guessed. Times are read from the clock or from commits only.
"""
__version__ = "1.0.1"
import hashlib, os, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slides_lineage_mission_v1_0_1 import mission_block  # noqa: E402
import sen0401_slides_stages_v1_0_1 as st  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NS = "http://example.org/sen0401-slides-lineage#"
STAGES = int(os.environ.get("SLIDES_STAGES", "1"))
COMMITS = {"Mission": "PENDING", "Scope": "PENDING", "Goal": "PENDING", "Objective": "PENDING", "Backlog": "PENDING"}
for k in COMMITS:
    COMMITS[k] = os.environ.get("C_" + k.upper(), COMMITS[k])
ORDER = ["Mission", "Scope", "Goal", "Objective", "Backlog"]
STATUS = {1: "LS_Opened", 2: "LS_Scoped", 3: "LS_Goaled", 4: "LS_Objectived", 5: "LS_Backlogged", 6: "LS_InProgress"}
BASE_AT = os.environ.get("BASE_AT", "")

HEAD = """@prefix backlog: <http://example.org/backlog#> .
@prefix ex:      <%s> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix dcterms: <http://purl.org/dc/terms/> .

<http://example.org/sen0401-slides-lineage> a owl:Ontology ;
    rdfs:label "Delivery lineage for renewing the SEN0401 lecture decks"@en ;
    owl:versionInfo "%s" ; dcterms:identifier "sen0401_slides_lineage" .

ex:Lineage a backlog:Lineage ;
    rdfs:label "First lineage run for the SEN0401 decks"@en ;
    backlog:lineageForMission ex:Mission ; backlog:lineageOrdinal 1 ; backlog:lineageArchived false ;
    backlog:hasLineageStatus backlog:%s ;
    backlog:adoptsObligationSet backlog:OS_SDLC_v2 ; backlog:adoptionRecordedAtOpen true .
"""


def main():
    version = open(os.path.join(REPO, "VERSION.txt")).read().strip()
    t = HEAD % (NS, version, STATUS[STAGES]) + mission_block()
    if STAGES >= 2: t += st.scope_block()
    if STAGES >= 3: t += st.goal_block()
    if STAGES >= 4: t += st.objective_block(with_movers=STAGES >= 5).replace("__BASE_AT__", BASE_AT)
    if STAGES >= 5 or STAGES == 6:
        import sen0401_slides_backlog_v1_0_1 as bk
        t += bk.backlog_block()
    for n, name in enumerate(ORDER[:min(STAGES, 5)]):
        t += '\nex:Out_%s a backlog:StageOutput ;\n    rdfs:label "Closure of the %s stage"@en ;\n    backlog:belongsToLineage ex:Lineage ;\n    backlog:outputOfStage backlog:Stage_%s ;%s\n    backlog:hasStateDigest "__D_%s__" ;\n    backlog:closedAtCommit "%s" .\n' % (
            name, name, name, ("\n    backlog:consumesOutput ex:Out_%s ;" % ORDER[n - 1]) if n else "", name, COMMITS[name])
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    nt = g.serialize(format="nt").splitlines()
    for name in ORDER[:min(STAGES, 5)]:
        key = {"Mission": "Mission>", "Scope": "Scope>", "Goal": "G_", "Objective": "Obj_", "Backlog": "Backlog>"}[name]
        t = t.replace("__D_%s__" % name, hashlib.sha256("\n".join(sorted(l for l in nt if ("<%s%s" % (NS, key)) in l)).encode()).hexdigest())
    out = os.path.join(REPO, "07-lineage", "sen0401_slides_lineage_v%s.ttl" % version.replace(".", "_"))
    for old in os.listdir(os.path.join(REPO, "07-lineage")):
        os.remove(os.path.join(REPO, "07-lineage", old))
    open(out, "w").write(t)
    chk = rdflib.Graph(); chk.parse(out, format="turtle")
    print("%s: %d triples, %d stage(s)" % (os.path.basename(out), len(chk), STAGES))


if __name__ == "__main__":
    sys.exit(main())
