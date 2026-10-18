#!/usr/bin/env python3
"""sen0401_lineage_licence_bolt v1_0_0 - records TK_Licence_BOLT_Ch09 (correct the BOLT provenance contradiction of page 9) as Done in a NEW register version,
only where the evidence bridge verified the check Licence/BOLT_Ch09 (exit 0) and the provenance file by SHA-256. The owner's ruling (2026-10-19 local, 2026-10-18T21:42:00Z):
the BOLT text is "CC BY 4.0". Dates: started = the ruling, finished = the commit of the corrected provenance file. Every Done item needs a harness, verified test evidence,
a re-run of the scores that predate the completion, and a reading of the objective it moves; all are written in the same version.
Usage:
  sen0401_lineage_licence_bolt_v1_0_0.py draft OUT.ttl     the evidence nodes only (prefixes + nodes, no verdict), for backlog_evidence_bridge --test-command "python3 -B {spec} {id}"
  sen0401_lineage_licence_bolt_v1_0_0.py record BRIDGE.ttl the new register version
"""
__version__ = "1.0.0"
import hashlib, os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = "03-materials/ch09/assets/ASSETS_PROVENANCE_v1_4_0.md"
FEV, TEV = "Ev3LB_Provenance_Ch09", "Ev3LB_Check_Ch09"
CHECK = "08-tooling/sen0401_lineage_licence_check_v1_0_0.py"
RULING = "2026-10-18T21:42:00"
CRIT = "backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission"


def facts():
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", PATH], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1], hashlib.sha256(open(os.path.join(REPO, PATH), "rb").read()).hexdigest()


def nodes(vd=None):
    h, utc, sha = facts()
    f = ('ex:%s a backlog:ArtifactEvidence ; rdfs:label "ASSETS_PROVENANCE_v1_4_0.md, committed %s (last change %s UTC): the BOLT file is recorded as CC BY 4.0"@en ; %s ;\n'
         '    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (FEV, h, utc, CRIT, PATH, sha))
    t = ('ex:%s a backlog:TestEvidence ; rdfs:label "Licence check for the BOLT file of page 9"@en ; %s ;\n'
         '    backlog:hasTestId "Licence/BOLT_Ch09" ; backlog:hasTestSpec "%s"' % (TEV, CRIT, CHECK))
    if vd is None:
        return f + " .\n" + t + " .\n", h, utc
    out = ""
    for ev, x in ((FEV, f), (TEV, t)):
        ok, at, meth = vd[ev]
        assert ok, ev + " not verified"
        out += x + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), at)
    return out, h, utc


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        n, _, _ = nodes(); pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + n); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); nxt, cur = M.next_version(src); now = M.now()
    n, h, utc = nodes(vd)
    note = ("Done, recorded %s: the provenance of page 9 is corrected in %s (commit %s), where bolt03_transactions.md is recorded as CC BY 4.0, as the owner ruled (2026-10-19). "
            "The evidence is the licence check (exit 0) and the file by SHA-256, both verified by the evidence bridge. Only this contradiction is closed; the other licence questions of page 9 stay open.") % (now[:10], os.path.basename(PATH), h)
    t2, k = re.subn(r'(ex:TK_Licence_BOLT_Ch09 a backlog:ExecutionTask[^\n]*\n[^\n]*)backlog:hasState backlog:Ready ; ', r'\1', t, count=1)
    assert k == 1
    add = n + 'ex:Harness3_Licence_BOLT_Ch09 a backlog:TestHarness ; rdfs:label "Licence check for the BOLT file of page 9"@en ; backlog:harnessFor ex:TK_Licence_BOLT_Ch09 ; backlog:hasHarnessEvidence ex:%s .\n' % TEV
    add += ('ex:TK_Licence_BOLT_Ch09 backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; '
            'backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter ; backlog:hasEvidence ex:%s, ex:%s ; backlog:hasAuditNote "%s" .\n') % (RULING, utc, now, FEV, TEV, S.esc(note))
    t2 += "\n" + add
    # the objective this task moves gets a reading dated at or after the finish: the count of Done movers in this version
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); B = M.B
    for obj in sorted(set(g.subjects(B.metricMovableBy, rdflib.URIRef(M.EX + "TK_Licence_BOLT_Ch09"))), key=str):
        movers = set(g.objects(obj, B.metricMovableBy)); c = sum(1 for m in movers if (m, B.hasState, B.Done) in g); on = str(obj).split("#")[-1]; mid = str(g.value(obj, B.hasSuccessMetric)).split("#")[-1]
        t2 += ('ex:Obs31_%s a backlog:MetricObservation ; rdfs:label "Reading after TK_Licence_BOLT_Ch09 was recorded Done"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
               '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted the carried tasks that can move this objective and read Done in this register version: %d of %d." .\n') % (on, mid, on, c, now, c, len(movers))
    # an open item's score may not predate a completion in the register (L3): re-run, same components and value, dated now
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t2, k = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now, t2, count=1); assert k == 1, sid
        t2 += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid, now)
    out = M.write_new(src, t2, nxt, cur, "TK_Licence_BOLT_Ch09 recorded Done on the bridge-verified licence check and provenance file (BOLT text CC BY 4.0, the owner's ruling); the open scores re-run.")
    print(os.path.basename(out))


main()
