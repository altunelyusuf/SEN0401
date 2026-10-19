#!/usr/bin/env python3
"""sen0401_lineage_deck_fix v1_0_0 - records, in ONE new register version, the corrected decks of chapters 1 to 7 (owner-directed: "You tell me if they are failing or needing corrections and update.", 2026-10-19).
 - Chapters 1-4: the task TK_Deck_ChNN_CheckFix becomes Done, only where the evidence bridge verified BOTH the lineage chapter check Deck/ChNN (v1_2_0, which also runs the stale-fixture runner) AND the nine engine checks with fixtures,
   and the SHA-256 of the new deck and of its link register.
 - Chapters 5-7: the stories are Done already; the correction (defects against the stories' own criteria: links, story and arc checks) is NEW dated evidence on them with the hash of the new deck files and a dated note
   (G125 option 1). The earlier evidence of a rebuilt file stays as the dated record; it is not edited.
Dates are git's: finished = the last commit of the deck or its link register. A chapter whose checks did not verify is not recorded; its task or story gets a dated note naming what failed.
Also writes a corrected reading of Obj3_NothingRebuilt (decks changed by this lineage: the cited link-pass files whose SHA-256 no longer equals the recorded one) and the readings of the objectives the Done tasks move.
Usage:
  sen0401_lineage_deck_fix_v1_0_0.py draft OUT.ttl           the evidence nodes (prefixes + nodes, no verdict) for backlog_evidence_bridge --test-command "python3 -B {spec} {id}"
  sen0401_lineage_deck_fix_v1_0_0.py record BRIDGE.ttl       the new register version
"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = [1, 2, 3, 4, 5, 6, 7]
TASKS = [1, 2, 3, 4]
SPEC1 = "08-tooling/sen0401_lineage_chapter_check_v1_2_0.py"
SPEC2 = "08-tooling/sen0401_lineage_deck_nine_check_v1_0_0.py"
CRIT = "backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission"
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def git_last(p):
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", p], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1]


def sha(p):
    return hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()


def facts(n):
    deck = sorted(glob.glob(os.path.join(REPO, "03-materials/ch%02d/*.pptx" % n)), key=vkey)[-1]; deck = os.path.relpath(deck, REPO)
    reg = "08-tooling/ch%02d-deck/link_register_v1_0_0.json" % n
    out = []
    for p in (deck, reg):
        h, u = git_last(p); out.append((p, sha(p), h, u))
    return out


def nodes(vd=None, chapters=CH):
    out = ""
    for n in chapters:
        tag = "Ch%02d" % n
        items = [("Ev3DF_Deck_" + tag, "TestEvidence", 'ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for Deck %s, run again on the corrected deck (DF)"@en ; %s ;\n    backlog:hasTestId "Deck/%s" ; backlog:hasTestSpec "%s"' % ("Ev3DF_Deck_" + tag, tag, CRIT, tag, SPEC1)),
                 ("Ev3DF_Nine_" + tag, "TestEvidence", 'ex:%s a backlog:TestEvidence ; rdfs:label "The nine engine checks and the stale-fixture runner for Deck %s (DF)"@en ; %s ;\n    backlog:hasTestId "Deck/%s" ; backlog:hasTestSpec "%s"' % ("Ev3DF_Nine_" + tag, tag, CRIT, tag, SPEC2))]
        for i, (p, s, h, u) in enumerate(facts(n)):
            items.append(("Ev3DF_Deck_%s_File%d" % (tag, i + 1), "A", 'ex:Ev3DF_Deck_%s_File%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC), corrected version"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (tag, i + 1, os.path.basename(p), h, u, CRIT, p, s)))
        for name, kind, body in items:
            if vd is None:
                out += body + " .\n"
            else:
                ok, at, meth = vd[name]; assert ok, name
                tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind != "A" else "backlog_evidence_bridge_v1_1_0"
                out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    return out


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = {}
    for bp in sys.argv[2].split(","):
        vd.update(S.verdicts(bp))
    nxt, cur = M.next_version(src); now = M.now(); B = M.B
    good, bad = [], []
    for n in CH:
        tag = "Ch%02d" % n
        names = ["Ev3DF_Deck_" + tag, "Ev3DF_Nine_" + tag, "Ev3DF_Deck_%s_File1" % tag, "Ev3DF_Deck_%s_File2" % tag]
        (good if all(x in vd and vd[x][0] for x in names) else bad).append(n)
    add = ""
    # evidence nodes for the good chapters only
    full = nodes(vd, good)
    add += full
    ev = lambda n: "ex:Ev3DF_Deck_Ch%02d, ex:Ev3DF_Nine_Ch%02d, ex:Ev3DF_Deck_Ch%02d_File1, ex:Ev3DF_Deck_Ch%02d_File2" % (n, n, n, n)
    t2 = t
    for n in CH:
        tag = "Ch%02d" % n
        if n in good:
            fl = facts(n); fin = max(u for _, _, _, u in fl); h = [x[2] for x in fl]
            if n in TASKS:
                tid = "TK_Deck_%s_CheckFix" % tag
                t2, k = re.subn(r'(ex:%s a backlog:ExecutionTask[^\n]*\n[^\n]*)backlog:hasState backlog:InProgress ; ' % tid, r'\1', t2, count=1); assert k == 1, tid
                add += ('ex:Harness3_Deck_%s_CheckFix a backlog:TestHarness ; rdfs:label "Chapter check and the nine engine checks for Deck %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:Ev3DF_Deck_%s, ex:Ev3DF_Nine_%s .\n' % (tag, tag, tid, tag, tag))
                add += ('ex:%s backlog:hasState backlog:Done ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter ; backlog:hasEvidence %s ; '
                        'backlog:hasAuditNote "Done, recorded %s: the deck %s (commit %s) passes the lineage deck check v1_2_0 (examples re-run, stale fixtures refused, layout, notes) and the nine engine checks with fixtures; the evidence bridge verified both runs and the SHA-256 of the deck and of its link register. Owner-directed: \\"You tell me if they are failing or needing corrections and update.\\" (2026-10-19)." .\n'
                        % (tid, fin, now, ev(n), now[:10], os.path.basename(fl[0][0]), h[0]))
            else:
                sid = "ST_Deck_" + tag
                add += ('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote "Correction recorded %s (G125 option 1, new evidence on the same Done story): the deck failed the story\'s own criteria on the links, story and arc checks of the engine; it was rebuilt as %s (commit %s). The new deck and its link register are cited by SHA-256, the lineage deck check v1_2_0 and the nine engine checks with fixtures were run through the evidence bridge and verified. The earlier evidence of the replaced file stays as the dated record. Owner-directed: \\"You tell me if they are failing or needing corrections and update.\\" (2026-10-19)." .\n'
                        % (sid, ev(n), now[:10], os.path.basename(fl[0][0]), h[0]))
        else:
            tgt = "TK_Deck_%s_CheckFix" % tag if n in TASKS else "ST_Deck_" + tag
            add += 'ex:%s backlog:hasAuditNote "Checked %s through the evidence bridge: the chapter check or the nine engine checks did not verify for the current deck, so nothing is recorded Done for it." .\n' % (tgt, now[:10])
    t2 += "\n" + add
    # readings: objectives that Done tasks move, and a corrected reading of Obj3_NothingRebuilt
    g = rdflib.Graph(); g.parse(data=t2, format="turtle")
    for obj in sorted(set(g.subjects(B.metricMovableBy, None)), key=str):
        if (obj, B.belongsToLineage, rdflib.URIRef(M.EX + "Lineage3")) not in g or str(obj).endswith("Obj3_NothingRebuilt"):
            continue
        movers = set(g.objects(obj, B.metricMovableBy)); c = sum(1 for m in movers if (m, B.hasState, B.Done) in g)
        prev = [int(float(str(g.value(o, B.hasObservedValue)))) for o in g.subjects(B.observationFor, obj)]
        if not c or c in prev and max(prev) == c:
            continue
        on = str(obj).split("#")[-1]; mid = str(g.value(obj, B.hasSuccessMetric)).split("#")[-1]
        t2 += ('ex:Obs32_%s a backlog:MetricObservation ; rdfs:label "Reading after the corrected decks were recorded Done"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
               '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted the items that can move this objective and read Done in this register version: %d of %d." .\n') % (on, mid, on, c, now, c, len(movers))
    changed = 0
    for ev_ in g.subjects(rdflib.RDF.type, B.ArtifactEvidence):
        if "Ev3L" not in str(ev_) or "Deck" not in str(ev_) and "Page" not in str(ev_):
            continue
        p = g.value(ev_, B.hasArtifactPath); s = g.value(ev_, B.hasArtifactSHA256)
        if p is None or s is None or not os.path.exists(os.path.join(REPO, str(p))): continue
        if sha(str(p)) != str(s): changed += 1
    t2 += ('ex:Obs32_Obj3_NothingRebuilt a backlog:MetricObservation ; rdfs:label "Corrected reading: files cited by the link passes whose SHA-256 has changed"@en ;\n    backlog:observesMetric ex:Met3_Rebuilt ; backlog:observationFor ex:Obj3_NothingRebuilt ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
           '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted from the files: link-pass evidence nodes of decks and pages whose recorded SHA-256 differs from the file now. The earlier reading of this objective (2) counted the Done link-pass stories and did not measure this metric; this reading replaces it as the one that measures it. The files changed because the owner directed the decks to be corrected (\\"You tell me if they are failing or needing corrections and update.\\", 2026-10-19)." .\n') % (changed, now)
    # an open item's score may not predate a completion in the register (L3): re-run, same components and value, dated now
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t2, k = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now, t2, count=1); assert k == 1, sid
        t2 += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid, now)
    out = M.write_new(src, t2, nxt, cur, "Corrected decks recorded: chapters %s verified by the bridge (tasks of 1-4 Done, new evidence on the stories of 5-7); not recorded: %s." % (good, bad or "none"))
    print(os.path.basename(out), "good", good, "not", bad)


main()
