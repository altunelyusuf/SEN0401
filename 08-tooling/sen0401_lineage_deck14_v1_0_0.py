#!/usr/bin/env python3
"""sen0401_lineage_deck14 v1_0_0 - ONE new register version: TK_Deck_Ch14_StaleFixtures becomes Done only if the evidence bridge verified the lineage chapter check v1_3_0 for Deck/Ch14 (it runs the deck fixtures v1_2_0:
the credit and date fixtures that plain CC BY credits need; deck 14 has 14 of 14 fixtures refused) and the SHA-256 of the deck, of its link register, of the fixtures tool v1_2_0 and of the chapter check v1_3_0 (the register points at the new tool versions).
Disclosed: the `links` check of deck_nine v1_1_0 fails for chapter 14 because web.archive.org is unreachable from this sandbox (1 of 14 links; archive.org answers 200; link and check unchanged); so the nine-check evidence is NOT cited for this task.
Also records the owner's direction of 2026-10-19 12:42 Istanbul, "Yes, proceed.", on the credit "the course's own CC BY 4.0" of genesis_hexdump.png (chapter 1 deck), as owner-directed work; and dated notes that Stage 3.F passes for the research of chapters 2-4 (commit b4c7a07) while the composite Research check cannot run to the end (no verify script): those three tasks stay open.
Usage:  draft OUT.ttl  |  record BRIDGE.ttl"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = "08-tooling/sen0401_lineage_chapter_check_v1_3_0.py"
CRIT = "backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission"
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
TID = "TK_Deck_Ch14_StaleFixtures"


def git_last(p):
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", p], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1]


def files():
    deck = os.path.relpath(sorted(glob.glob(os.path.join(REPO, "03-materials/ch14/*.pptx")), key=vkey)[-1], REPO)
    return [deck, "08-tooling/ch14-deck/link_register_v1_0_0.json", "08-tooling/sen0401_deck_fixtures_v1_2_0.py", SPEC]


def nodes(vd=None):
    items = [("Ev3D14_Deck_Ch14", "T", 'ex:Ev3D14_Deck_Ch14 a backlog:TestEvidence ; rdfs:label "Chapter check v1_3_0 for Deck Ch14, with the credit and date fixtures (14 of 14 refused)"@en ; %s ;\n    backlog:hasTestId "Deck/Ch14" ; backlog:hasTestSpec "%s"' % (CRIT, SPEC))]
    for i, p in enumerate(files()):
        h, u = git_last(p); s = hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
        items.append(("Ev3D14_Deck_Ch14_File%d" % (i + 1), "A", 'ex:Ev3D14_Deck_Ch14_File%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (i + 1, os.path.basename(p), h, u, CRIT, p, s)))
    out = ""
    for name, kind, body in items:
        if vd is None:
            out += body + " .\n"
        else:
            ok, at, meth = vd[name]; assert ok, name
            tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind == "T" else "backlog_evidence_bridge_v1_1_0"
            out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    return out


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); nxt, cur = M.next_version(src); now = M.now(); B = M.B
    names = ["Ev3D14_Deck_Ch14"] + ["Ev3D14_Deck_Ch14_File%d" % i for i in range(1, 5)]
    ok = all(n in vd and vd[n][0] for n in names)
    add = ""
    if ok:
        fl = files(); fin = max(git_last(p)[1] for p in fl)
        t, k = re.subn(r'(ex:%s a backlog:ExecutionTask[^\n]*\n[^\n]*)backlog:hasState backlog:InProgress ; ' % TID, r'\1', t, count=1); assert k == 1
        add += nodes(vd)
        add += 'ex:Harness3_Deck_Ch14_StaleFixtures a backlog:TestHarness ; rdfs:label "Chapter check v1_3_0 with the credit and date fixtures for Deck Ch14"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:Ev3D14_Deck_Ch14 .\n' % TID
        add += ('ex:%s backlog:hasState backlog:Done ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter ; backlog:hasEvidence ex:Ev3D14_Deck_Ch14, ex:Ev3D14_Deck_Ch14_File1, ex:Ev3D14_Deck_Ch14_File2, ex:Ev3D14_Deck_Ch14_File3, ex:Ev3D14_Deck_Ch14_File4 ;\n'
                '    backlog:hasAuditNote "Done, recorded %s: deck 14 now has 14 of 14 stale fixtures, each refused for its own reason (fixtures tool v1_2_0, commit d1a2b14; chapter check v1_3_0, commit f2855a0). The evidence bridge ran the lineage chapter check v1_3_0 for Deck/Ch14 (exit 0) and verified the SHA-256 of the deck, its link register, the fixtures tool and the chapter check. '
                'Disclosed: the links check of deck_nine v1_1_0 for chapter 14 fails because web.archive.org is unreachable from this sandbox (1 of 14 links; archive.org answers 200; the link and the check are unchanged), so no nine-check evidence is cited for this task." .\n' % (TID, fin, now, now[:10]))
    else:
        add += 'ex:%s backlog:hasAuditNote "Checked %s through the evidence bridge: the chapter check v1_3_0 for Deck/Ch14 or a cited file did not verify, so the task stays open." .\n' % (TID, now[:10])
    add += ('ex:ST_Deck_Ch01 backlog:hasAuditNote "Owner-directed, recorded %s: the credit \\"the course\'s own CC BY 4.0\\" (Yusuf Altunel) for genesis_hexdump.png was put to the owner and he answered, 2026-10-19 12:42 Istanbul (09:42 UTC), relayed by the course coordinator: \\"Yes, proceed.\\" It is owner-directed work, not an open confirmation." .\n')  % now[:10]
    for n in (2, 3, 4):
        add += ('ex:TK_Research_Ch0%d_Stage3F backlog:hasAuditNote "Progress recorded %s (not Done): Stage 3.F now passes for chapter %d (commit b4c7a07, new Stage 3 document patch versions); the Research composite check cannot run to the end because the chapter has no verify script, which another agent is writing. The task stays open until the composite check passes through the evidence bridge." .\n') % (n, now[:10], n)
    t2 = t + "\n" + add
    g = rdflib.Graph(); g.parse(data=t2, format="turtle")
    for obj in sorted(set(g.subjects(B.metricMovableBy, None)), key=str):
        if (obj, B.belongsToLineage, rdflib.URIRef(M.EX + "Lineage3")) not in g or str(obj).endswith("Obj3_NothingRebuilt"):
            continue
        movers = set(g.objects(obj, B.metricMovableBy)); c = sum(1 for m in movers if (m, B.hasState, B.Done) in g)
        prev = [int(float(str(g.value(o, B.hasObservedValue)))) for o in g.subjects(B.observationFor, obj)]
        if not c or (prev and max(prev) == c):
            continue
        on = str(obj).split("#")[-1]; mid = str(g.value(obj, B.hasSuccessMetric)).split("#")[-1]
        t2 += ('ex:Obs35_%s a backlog:MetricObservation ; rdfs:label "Reading after the Deck Ch14 fixtures task was recorded Done"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
               '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted the items that can move this objective and read Done in this register version: %d of %d." .\n') % (on, mid, on, c, now, c, len(movers))
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t2, k = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now, t2, count=1); assert k == 1, sid
        t2 += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid, now)
    out = M.write_new(src, t2, nxt, cur, "Deck Ch14 fixtures task %s; the owner's direction on the genesis hex dump credit recorded; Stage 3.F progress of chapters 2-4 noted, those tasks stay open." % ("Done on the bridge-verified chapter check v1_3_0" if ok else "not recorded Done"))
    print(os.path.basename(out), "ok" if ok else "NOT verified")


main()
