#!/usr/bin/env python3
"""sen0401_lineage_extend v1_0_0 - writes the next version of the SEN0401 slide lineage from the newest one on disk, never editing the old file.
Mechanical conformance only (ported from sen0414_lineage_extend_v1_0_0, whose steps 1 and 3 it repeats):
  1. aligns the register header with BP-D7: owl:versionIRI + owl:priorVersion (validator L1 refused the previous version for lacking them);
  2. names the Executor (ex:Executor_ClaudeCodeSession) on every open item that has none (validator L2).
It admits no chapter, changes no scope, records nothing started or Done.
"""
__version__ = "1.0.0"
import glob, os, re, sys
import rdflib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIN = os.path.join(REPO, "07-lineage")
BASE = "http://example.org/sen0401-slides-lineage"
B = rdflib.Namespace("http://example.org/backlog#")
EX = rdflib.Namespace(BASE + "#")
EXEC = "ex:Executor_ClaudeCodeSession"


def ver(p):
    return [int(v) for v in re.search(r"_v(\d+)_(\d+)_(\d+)\.ttl$", p).groups()]


def main():
    src = sorted(glob.glob(os.path.join(LIN, "sen0401_slides_lineage_v*.ttl")), key=ver)[-1]
    v = ver(src)
    cur = "%d.%d.%d" % tuple(v)
    nxt = "%d.%d.0" % (v[0], v[1] + 1)
    out = os.path.join(LIN, "sen0401_slides_lineage_v%s.ttl" % nxt.replace(".", "_"))
    if os.path.exists(out):
        sys.exit("refusing to overwrite " + out)
    t = open(src, encoding="utf-8").read()
    t, n = re.subn(r'owl:versionInfo "%s" ;' % re.escape(cur),
                   'owl:versionInfo "%s" ; owl:versionIRI <%s/%s> ; owl:priorVersion <%s/%s> ;' % (nxt, BASE, nxt, BASE, cur), t, count=1)
    assert n == 1, "header not found"
    comment = ("%s: mechanical conformance only. The header now carries owl:versionIRI and owl:priorVersion (validator L1 refused %s for lacking them) and every open item "
               "names its Executor (validator L2, also refused in %s). No chapter is admitted, no scope changed, nothing recorded started or Done. DISCLOSED, NOT FIXED: chapters 5-7 "
               "exist in the course repository but were built before this register planned them, so their stories here still read Proposed; recording them is a separate, later event." % (nxt, cur, cur))
    t = t.replace('dcterms:identifier "sen0401_slides_lineage" ;', 'dcterms:identifier "sen0401_slides_lineage" ;\n    rdfs:comment "%s"@en ;' % comment.replace('"', "'"), 1)
    ex = ('\nex:Executor_ClaudeCodeSession a owl:NamedIndividual , backlog:Executor_SingleAgent ;\n    rdfs:label "Claude Code session - the AI-agent executor of this course package\'s own work"@en ;\n'
          '    rdfs:comment "One non-human executing party with no standing team membership, the same identity the framework\'s own A-Box calls its default AI-agent Executor (DefaultExecutor); the owner approves and teaches, the session performs the build." ;\n'
          '    rdfs:seeAlso <http://example.org/fixture-autofix#DefaultExecutor> .\n')
    g = rdflib.Graph(); g.parse(data=t + ex, format="turtle")
    opn = set()
    for st in (B.Proposed, B.Ready, B.InProgress):
        opn |= set(g.subjects(B.hasState, st))
    L = ["\n# Open items name their Executor (validator L2)\n"]
    for s in sorted(opn, key=str):
        if str(s).startswith(str(EX)) and not list(g.objects(s, B.responsible)):
            L.append("<%s> backlog:responsible %s .\n" % (s, EXEC))
    body = t + ex + "".join(L)
    g2 = rdflib.Graph(); g2.parse(data=body, format="turtle")
    open(out, "w", encoding="utf-8").write(body)
    print("%s: %d triples; %d open items now name an Executor" % (os.path.basename(out), len(g2), len(L) - 1))


if __name__ == "__main__":
    main()
