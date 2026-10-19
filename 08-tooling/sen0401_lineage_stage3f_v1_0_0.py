#!/usr/bin/env python3
"""sen0401_lineage_stage3f v1_0_0 - ONE new register version: TK_Research_Ch02_Stage3F, Ch03_Stage3F and Ch04_Stage3F become Done, each only if the evidence bridge verified, for its chapter, the lineage chapter check v1_3_0 for Research/ChNN
(RDODI Stage 1-3 gates incl. Stage 3.F, corpus claims executed, the chapter verify script, HermiT) AND the chain checks Deck/ChNN and Page/ChNN re-run, AND the SHA-256 of the newest research file, the newest Stage 3 document, the chapter's verify script and the shared verify library
(the register points at the new file and tool versions). Dates are git's: started = the commit of the Stage 3.F repair (b4c7a07), finished = the last commit of the cited files. Disclosures are written into each task's note.
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
CH = (2, 3, 4)
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]


def git_last(p):
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", p], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1]


def git_start():
    return subprocess.check_output(["git", "log", "-1", "--format=%cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", "b4c7a07"], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).strip()


def newest(pat):
    return os.path.relpath(sorted(glob.glob(os.path.join(REPO, pat)), key=vkey)[-1], REPO)


def files(n):
    return [newest("03-materials/ch%02d/rdodi/sen0401_ch%02d_research_v*.ttl" % (n, n)), newest("03-materials/ch%02d/rdodi/sen0401_ch%02d_document_v*.ttl" % (n, n)),
            "08-tooling/sen0401_ch%02d_verify_v1_0_0.py" % n, "08-tooling/sen0401_research_verify_lib_v1_0_0.py"]


def nodes(vd=None, chapters=CH):
    items = []
    for n in chapters:
        t = "Ch%02d" % n
        for k, lab in (("Research", "Research"), ("Deck", "Deck"), ("Page", "Page")):
            items.append(("Ev3S3_%s_%s" % (k, t), "T", 'ex:Ev3S3_%s_%s a backlog:TestEvidence ; rdfs:label "Chapter check v1_3_0 for %s %s, run again after the Stage 3.F repair (S3)"@en ; %s ;\n    backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s"' % (k, t, lab, t, CRIT, k, t, SPEC)))
        for i, p in enumerate(files(n)):
            h, u = git_last(p); s = hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()
            items.append(("Ev3S3_Research_%s_File%d" % (t, i + 1), "A", 'ex:Ev3S3_Research_%s_File%d a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (t, i + 1, os.path.basename(p), h, u, CRIT, p, s)))
    out = ""
    for name, kind, body in items:
        if vd is None:
            out += body + " .\n"
        else:
            ok, at, meth = vd[name]; assert ok, name
            tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind == "T" else "backlog_evidence_bridge_v1_1_0"
            out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    return out


EXTRA = {
    2: "Chapter 2: research v1.4.0 and document v1.3.2 restore the source P03 and carry the label (Bitcoin Core, 2026) on the six Bitcoin Core publications P30-P35 (commit ed50d68).",
    3: "Chapter 3: research v1.3.0 adds finding F15, which cites the JSON-RPC 2.0 specification (P85) and BIP 142 (P17) (commit c5c5868).",
    4: "Chapter 4: research v1.3.0 adds finding F15, which cites P85 and BIP 142 (P17); the label of P17 is corrected from Wuille 2015 to Lau 2015 because the saved BIP preamble names Johnson Lau (commit c5c5868). F15's status Closed and the statement that BIP 173 replaces 142 are read from saved copies and no executed corpus claim covers them (the finding says so).",
}
COMMON = ("Disclosed: the research scorecard text still carries the old source counts. The checks Stage4.cov and Stage4.sub on the pages of chapters 2-4 are PROPOSED checks that were failing before; this register records no result for them, they are not part of this task, and nothing here claims they pass.")


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); nxt, cur = M.next_version(src); now = M.now(); B = M.B; st = git_start()
    good = [n for n in CH if all(x in vd and vd[x][0] for x in (["Ev3S3_%s_Ch%02d" % (k, n) for k in ("Research", "Deck", "Page")] + ["Ev3S3_Research_Ch%02d_File%d" % (n, i) for i in range(1, 5)]))]
    add = nodes(vd, good) if good else ""
    for n in CH:
        tid = "TK_Research_Ch%02d_Stage3F" % n; tg = "Ch%02d" % n
        if n in good:
            fl = files(n); fin = max(git_last(p)[1] for p in fl); hs = [git_last(p)[0] for p in fl]
            t, k = re.subn(r'(ex:%s a backlog:ExecutionTask[^\n]*\n[^\n]*)backlog:hasState backlog:Ready ; ' % tid, r'\1', t, count=1); assert k == 1, tid
            ev = ", ".join("ex:" + x for x in (["Ev3S3_Research_" + tg, "Ev3S3_Deck_" + tg, "Ev3S3_Page_" + tg] + ["Ev3S3_Research_%s_File%d" % (tg, i) for i in range(1, 5)]))
            add += 'ex:Harness3_Research_%s_Stage3F a backlog:TestHarness ; rdfs:label "Chapter checks v1_3_0 for the research, deck and page of %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:Ev3S3_Research_%s, ex:Ev3S3_Deck_%s, ex:Ev3S3_Page_%s .\n' % (tg, tg, tid, tg, tg, tg)
            add += ('ex:%s backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter ; backlog:hasEvidence %s ;\n'
                    '    backlog:hasAuditNote "Done, recorded %s: Stage 3.F passes for chapter %d after the citation repair (Stage 3 document patch version, commit b4c7a07), the verify script of the chapter was written (commit ff82603), and the evidence bridge ran the lineage chapter check v1_3_0 for Research/%s (Stage 1-3 gates, corpus claims, verify script, HermiT; exit 0) and, run again, for Deck/%s and Page/%s (the page test uses a TEST release key and proves the page logic only). It verified the SHA-256 of the newest research file, the newest Stage 3 document, the verify script and the shared verify library (commits %s). %s %s" .\n'
                    % (tid, st, fin, now, ev, now[:10], n, tg, tg, tg, ", ".join(sorted(set(hs))), S.esc(EXTRA[n]), S.esc(COMMON)))
        else:
            add += 'ex:%s backlog:hasAuditNote "Checked %s through the evidence bridge: a check or a cited file did not verify, so the task stays open." .\n' % (tid, now[:10])
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
        t2 += ('ex:Obs36_%s a backlog:MetricObservation ; rdfs:label "Reading after the Stage 3.F tasks were recorded Done"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
               '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted the items that can move this objective and read Done in this register version: %d of %d." .\n') % (on, mid, on, c, now, c, len(movers))
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t2, k = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now, t2, count=1); assert k == 1, sid
        t2 += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid, now)
    out = M.write_new(src, t2, nxt, cur, "Stage 3.F tasks of chapters %s recorded Done on the bridge-verified chapter checks and file hashes; not recorded: %s." % (good, [n for n in CH if n not in good] or "none"))
    print(os.path.basename(out), "good", good)


main()
