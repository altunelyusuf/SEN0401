#!/usr/bin/env python3
"""sen0401_lineage_item_check v1_0_0 - the check of a parent work item (an epic or an initiative) that the evidence bridge runs. A parent is complete when all of its
constituent work is complete, so the check reads the committed register named in its id and tests, for the item and everything below it (decomposesInto, transitively):
  1. the item has descendants, and every one of them reads Done in that register version;
  2. every Done descendant carries a startedAt and a finishedAt, and no finish precedes its start;
  3. every story and task below it carries at least one evidence node that the evidence bridge verified (evidenceVerified true);
  4. every ArtifactEvidence node of those descendants names a file that exists in the workspace and whose SHA-256 is the recorded one (physical, not read from the register).
It prints the earliest start and the latest finish of the descendants, which are the dates a parent takes.
Exit 0 only when all four hold.
Usage: sen0401_lineage_item_check_v1_0_0.py ITEM:vN_M_0      (e.g. EP_Deck:v0_117_0; run from the workspace root, the course repository)"""
__version__ = "1.0.0"
import hashlib, os, sys
import rdflib
from rdflib import Namespace, RDF

B = Namespace("http://example.org/backlog#"); EX = Namespace("http://example.org/sen0401-slides-lineage#")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    item, ver = sys.argv[1].split(":")
    reg = os.path.join(ROOT, "07-lineage", "sen0401_slides_lineage_%s.ttl" % ver)
    g = rdflib.Graph(); g.parse(reg, format="turtle")
    top = EX[item]; fails = []
    desc, todo = [], [top]
    while todo:
        x = todo.pop()
        for c in g.objects(x, B.decomposesInto):
            if c not in desc:
                desc.append(c); todo.append(c)
    if not desc:
        fails.append("%s has no descendants" % item)
    starts, fins, arts, nev = [], [], 0, 0
    for d in desc:
        n = d.split("#")[-1]
        if (d, B.hasState, B.Done) not in g:
            fails.append("%s is not Done" % n)
        sa, fa = g.value(d, B.startedAt), g.value(d, B.finishedAt)
        if sa is None or fa is None:
            fails.append("%s lacks a start or a finish" % n); continue
        if str(fa) < str(sa):
            fails.append("%s finishes before it starts" % n)
        starts.append(str(sa)); fins.append(str(fa))
        if any((d, RDF.type, B[c]) in g for c in ("Story", "ExecutionTask")):
            ev = list(g.objects(d, B.hasEvidence))
            if not any(str(g.value(e, B.evidenceVerified)).lower() == "true" for e in ev):
                fails.append("%s carries no bridge-verified evidence" % n)
            for e in ev:
                p, h = g.value(e, B.hasArtifactPath), g.value(e, B.hasArtifactSHA256)
                if p is None or h is None:
                    continue
                nev += 1; f = os.path.join(ROOT, str(p))
                if not os.path.isfile(f):
                    fails.append("%s: %s is missing" % (e.split("#")[-1], p)); continue
                if hashlib.sha256(open(f, "rb").read()).hexdigest() != str(h):
                    fails.append("%s: %s no longer matches its recorded SHA-256" % (e.split("#")[-1], p))
                arts += 1
    print("item %s in %s: %d descendants, %d artifact files re-hashed" % (item, ver, len(desc), arts))
    if starts:
        print("earliest start %s, latest finish %s" % (min(starts), max(fins)))
    for f in fails[:40]:
        print("FAIL", f)
    print("RESULT", "FAIL" if fails else "PASS")
    sys.exit(1 if fails else 0)


main()
