#!/usr/bin/env python3
"""sen0401_lineage_observe v1_1_0 - writes, in a NEW version of the SEN0401 slides lineage register, the first readings of the seven objectives of the second
lineage after its Backlog stage is closed. Every value is counted here from the register and the files, not typed (ported from sen0414_lineage_outscope_observe):
  Obj2_AdmittedDone      stories of chapters 5-7 that read Done in the register
  Obj2_EvidenceVerified  of those, stories with bridge-verified test evidence and every cited file verified
  Obj2_DatesFromGit      of those, stories carrying a start and a finish
  Obj2_NothingRebuilt    cited files whose current SHA-256 differs from the recorded one
  Obj2_Decks/Research/PagesRemaining   stories of that kind among chapters 8-14 that read Done
v1.1.0: the reading is a function (block) so another script can add it to the version it writes; the tag of the observation names is a parameter (Obs21 first reading, Obs22 second).
Usage: sen0401_lineage_observe_v1_1_0.py [TAG]   (default TAG 21)
"""
__version__ = "1.1.0"
import hashlib, os, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_0_0 as M

B, EX = M.B, M.EX


def block(t, tag="21"):
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    isdone = lambda s: (EX[s], B.hasState, B.Done) in g
    done = [s for s in M.ADMIT_STORIES if isdone(s)]
    ver = lambda e: g.value(e, B.evidenceVerified) is not None and bool(g.value(e, B.evidenceVerified).toPython())
    verified, dated, changed = [], [], 0
    for s in done:
        evs = list(g.objects(EX[s], B.hasEvidence))
        if evs and all(ver(e) for e in evs): verified.append(s)
        if g.value(EX[s], B.startedAt) is not None and g.value(EX[s], B.finishedAt) is not None: dated.append(s)
    for e in set(g.subjects(B.hasArtifactPath, None)):
        if str(e).split("#")[-1].startswith("Ev2_"):
            p = os.path.join(M.REPO, str(g.value(e, B.hasArtifactPath)))
            if hashlib.sha256(open(p, "rb").read()).hexdigest() != str(g.value(e, B.hasArtifactSHA256)): changed += 1
    rem = lambda k: sum(1 for n in M.REMAIN if isdone("ST_%s_Ch%02d" % (k, n)))
    vals = {"Obj2_AdmittedDone": len(done), "Obj2_EvidenceVerified": len(verified), "Obj2_DatesFromGit": len(dated), "Obj2_NothingRebuilt": changed,
            "Obj2_DecksRemaining": rem("Deck"), "Obj2_ResearchRemaining": rem("Research"), "Obj2_PagesRemaining": rem("Page")}
    now = M.now(); blk = ""
    for o, v in vals.items():
        mid = str(g.value(EX[o], B.hasSuccessMetric)).split("#")[-1]
        blk += ('ex:Obs%s_%s a backlog:MetricObservation ; rdfs:label "Reading after the Backlog stage of the second lineage"@en ;\n'
                '    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
                '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n'
                '    backlog:hasObservationMethod "Counted by sen0401_lineage_observe_v1_1_0 from this register and from the cited files (SHA-256 compared with the recorded one)." .\n') % (tag, o, mid, o, v, now)
    return blk, vals, (len(done), len(verified), len(dated), changed)


def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else "21"
    src = M.newest(); t = open(src, encoding="utf-8").read()
    blk, vals, (nd, nv, ndt, ch) = block(t, tag)
    nxt, cur = M.next_version(src)
    out = M.write_new(src, t + "\n" + blk, nxt, cur, "first readings of the second lineage's objectives: admitted Done %d of 9, evidence verified %d, dates from git %d, cited files changed %d; chapters 8-14 Done: decks %d, research %d, pages %d."
                      % (nd, nv, ndt, ch, vals["Obj2_DecksRemaining"], vals["Obj2_ResearchRemaining"], vals["Obj2_PagesRemaining"]))
    print(os.path.basename(out), vals)


if __name__ == "__main__":
    main()
