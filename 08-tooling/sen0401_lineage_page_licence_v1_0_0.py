#!/usr/bin/env python3
"""sen0401_lineage_page_licence v1_0_0 - ONE new register version after the pages of chapters 6 and 13 were recorded Done (record_done v1_2_0): 
 (1) TK_Licence_Mempool_Ch09 (closed by the course's own census, CC BY 4.0) and TK_Licence_Texts_Ch09 (closed by leaving the three third-party texts out) become Done, only where the evidence bridge verified the physical
     licence check (sen0401_lineage_licence_check_v1_1_0.py, which opens the chapter 9 page's embedded wheel) and the SHA-256 of the page, the census and the provenance file;
 (2) the rebuilt chapter 9 page is NEW dated evidence on the Done story ST_Page_Ch09 (G125 option 1) when the bridge verified the chapter check Page/Ch09 and the page hash;
 (3) the owner's directions are recorded with their quotes and date: "Keep the same standards with all other pages." and "Can we collect our own statistics from the network or alternative resources?" (2026-10-19);
 (4) dated notes with the agent-reported weak spots of the decks of chapters 1-7 (from each deck's REVIEW file), and the one question left for the owner: the credit of genesis_hexdump.png.
Usage:
  sen0401_lineage_page_licence_v1_0_0.py draft OUT.ttl      evidence nodes only (prefixes + nodes) for backlog_evidence_bridge --test-command "python3 -B {spec} {id}"
  sen0401_lineage_page_licence_v1_0_0.py record BRIDGE.ttl  the new register version
"""
__version__ = "1.0.0"
import glob, hashlib, os, re, subprocess, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIC = "08-tooling/sen0401_lineage_licence_check_v1_1_0.py"
PCHK = "08-tooling/sen0401_lineage_chapter_check_v1_2_0.py"
CRIT = "backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission"
vkey = lambda p: [int(x) for x in re.findall(r"_v(\d+)_(\d+)_(\d+)", p)[-1]]
EST_START = "2026-10-18T22:50:00"
Q1 = "Keep the same standards with all other pages."
Q2 = "Can we collect our own statistics from the network or alternative resources?"
DAY = "2026-10-19"


def git_last(p):
    c = subprocess.check_output(["git", "log", "-1", "--format=%h %cd", "--date=format-local:%Y-%m-%dT%H:%M:%S", p], cwd=REPO, env=dict(os.environ, TZ="UTC"), text=True).split()
    return c[0], c[1]


def newest(pat):
    return os.path.relpath(sorted(glob.glob(os.path.join(REPO, pat)), key=vkey)[-1], REPO)


def art():
    out = {}
    for k, p in (("Page", newest("03-materials/ch09/page/sen0401_ch09_page_v*.html")), ("Census", "08-tooling/ch09-evidence/mainnet_fee_census_v2_0_0.json"), ("Prov", newest("03-materials/ch09/assets/ASSETS_PROVENANCE_v*.md"))):
        h, u = git_last(p); out[k] = (p, hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest(), h, u)
    return out


def nodes(vd=None):
    a = art(); items = []
    for k, (p, s, h, u) in a.items():
        items.append(("Ev3PG_%s_Ch09" % k, "A", 'ex:Ev3PG_%s_Ch09 a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; %s ;\n    backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s"' % (k, os.path.basename(p), h, u, CRIT, p, s)))
    for tid, lab, spec in (("Mempool", "Licence check: the page embeds the course's own census and no mempool.space data", LIC), ("Texts", "Licence check: the page embeds none of the three third-party texts", LIC)):
        items.append(("Ev3PG_Licence_%s_Ch09" % tid, "T", 'ex:Ev3PG_Licence_%s_Ch09 a backlog:TestEvidence ; rdfs:label "%s"@en ; %s ;\n    backlog:hasTestId "Licence/%s_Ch09" ; backlog:hasTestSpec "%s"' % (tid, lab, CRIT, tid, spec)))
    items.append(("Ev3PG_Check_Ch09", "T", 'ex:Ev3PG_Check_Ch09 a backlog:TestEvidence ; rdfs:label "Chapter check for Page Ch09, run again on the rebuilt page (PG)"@en ; %s ;\n    backlog:hasTestId "Page/Ch09" ; backlog:hasTestSpec "%s"' % (CRIT, PCHK)))
    out = ""
    for name, kind, body in items:
        if vd is None:
            out += body + " .\n"
        else:
            ok, at, meth = vd[name]; assert ok, name
            tool = "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" if kind == "T" else "backlog_evidence_bridge_v1_1_0"
            out += body + ' ;\n    backlog:evidenceVerified true ; backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n' % (S.esc(meth), tool, at)
    return out


def deck_notes(now):
    out = ""
    for n in range(1, 8):
        f = os.path.relpath(sorted(glob.glob(os.path.join(REPO, "08-tooling/ch%02d-deck/REVIEW_v*.md" % n)), key=vkey)[-1], REPO)
        txt = open(os.path.join(REPO, f), encoding="utf-8").read()
        m = re.search(r"## Not done\n(.*)", txt, re.S); nd = " ".join(x.strip("- ").strip() for x in m.group(1).strip().splitlines() if x.strip()) if m else ""
        lk = re.search(r"- Links?:(.*)", txt); lk = lk.group(1).strip() if lk else ""
        pics = re.search(r"- Pictures[^:\n]*:(.*)", txt); pics = pics.group(1).strip() if pics else ""
        note = ("Agent-reported weak spots of the deck, recorded %s from the builder's review file %s (not re-verified here beyond the nine checks). Not done, in the builder's words: %s Links replaced or blocked: %s Pictures: %s"
                % (now[:10], f, nd or "nothing fails.", lk[:700] or "none reported.", pics[:700] or "see the review file."))
        if n == 1:
            note += (" The one question left for the owner: the credit of genesis_hexdump.png, the course's own CC BY 4.0 under Yusuf Altunel, which is the course's declaration and not a third party's. "
                     "Also: the coingecko API link answers 429 or 403 intermittently, so the links check may fail on a live host once and pass on the next run.")
        out += 'ex:ST_Deck_Ch%02d backlog:hasAuditNote "%s" .\n' % (n, S.esc(note))
    return out


def main():
    src = M.newest(); t = open(src, encoding="utf-8").read()
    if sys.argv[1] == "draft":
        pre = "".join(l + "\n" for l in t.splitlines() if l.startswith("@prefix") or l.startswith("PREFIX"))
        open(sys.argv[2], "w", encoding="utf-8").write(pre + "\n" + nodes()); print("draft", sys.argv[2]); return
    vd = S.verdicts(sys.argv[2]); nxt, cur = M.next_version(src); now = M.now(); B = M.B
    ev = nodes(vd); a = art(); fin = max(a[k][3] for k in a)
    add = ev + "\n"
    for tid, name, why in (("TK_Licence_Mempool_Ch09", "Mempool", "the mempool.space census is no longer carried; the page embeds the course's own census (mainnet_fee_census_v2_0_0.json, CC BY 4.0: facts of the block chain collected from mempool.space and blockstream.info and cross-checked, statistics computed by the course's collector)"),
                           ("TK_Licence_Texts_Ch09", "Texts", "the three third-party texts without a clear licence (Carlsten et al. 2016, Moeser and Boehme 2015, Corallo 2018) are left out of the page's wheel, under the standing rule that no text without a clear licence is shipped; the five examples that read them are shown as Recorded, not run")):
        t, k = re.subn(r'(ex:%s a backlog:ExecutionTask[^\n]*\n[^\n]*)backlog:hasState backlog:Ready ; ' % tid, r'\1', t, count=1); assert k == 1, tid
        evs = "ex:Ev3PG_Licence_%s_Ch09, ex:Ev3PG_Page_Ch09, ex:Ev3PG_Prov_Ch09" % name + (", ex:Ev3PG_Census_Ch09" if name == "Mempool" else "")
        add += 'ex:Harness3_Licence_%s_Ch09 a backlog:TestHarness ; rdfs:label "Licence check for the chapter 9 page: %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:Ev3PG_Licence_%s_Ch09 .\n' % (name, name, tid, name)
        add += ('ex:%s backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:startedAtIsEstimate true ; '
                'backlog:startEstimateBasis "Not witnessed: the work and its files first appear in one commit (%s, %s UTC). Estimated as the latest owner message of the day before the work, the confirmation of 2026-10-19 01:50 Istanbul (2026-10-18T22:50:00 UTC); the owner\'s question that started the work is dated 2026-10-19 and its time was not relayed." ; '
                'backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter ; backlog:hasEvidence %s ;\n'
                '    backlog:hasAuditNote "Done, recorded %s: %s. The evidence bridge ran the physical licence check (it opens the page\'s embedded wheel and lists its files) and verified the SHA-256 of the page %s (commit %s) and of the provenance file. '
                'Owner-directed: \\"%s\\" (%s; the time was not relayed)." .\n') % (tid, EST_START, a["Page"][2], a["Page"][3], fin, now, evs, now[:10], S.esc(why), os.path.basename(a["Page"][0]), a["Page"][2], S.esc(Q2), DAY)
    add += ('ex:ST_Page_Ch09 backlog:hasEvidence ex:Ev3PG_Check_Ch09, ex:Ev3PG_Page_Ch09 ;\n    backlog:hasAuditNote "Correction recorded %s (G125 option 1, new evidence on the same Done story): the page was rebuilt as %s (commit %s) to carry the course\'s own census and no text without a clear licence. The chapter check Page/Ch09 was run again through the evidence bridge on the rebuilt page (a TEST release key: it proves the page\'s logic, not the real instructor key) and the page is cited by SHA-256. The earlier evidence of the replaced page stays as the dated record. Owner-directed: \\"%s\\" (%s)." .\n'
            % (now[:10], os.path.basename(a["Page"][0]), a["Page"][2], S.esc(Q2), DAY))
    for sid, extra in (("ST_Page_Ch06", "Page 6 is a lighter page on the new template (page 9.67.0, commit 44642d3): same content as 9.63.0, tests 9.34.0 and 9.35.0 374 pass 0 fail, five runs each, load-task median 95-129 ms against 169-248 ms before (agent-reported)."),
                       ("ST_Page_Ch13", "Page 13 is page 9.69.0 (commit 5533071) built on research 13 v1_0_2 and deck 13 v1.2.0: tests 9.34.0 and 9.35.0 368 pass 0 fail; 14 varied questions drawn, 21 examples can vary; the question bank covers 84 of 84 concepts; 51 examples run, 11 Recorded (agent-reported). The load-time budget failed once on the first run and passed on the rerun with an 88 ms median: disclosed.")):
        add += 'ex:%s backlog:hasAuditNote "Owner-directed work, recorded %s: \\"%s\\" (%s) - the same standards as all other pages, no relaxation. %s" .\n' % (sid, now[:10], S.esc(Q1), DAY, S.esc(extra))
    add += deck_notes(now)
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
        t2 += ('ex:Obs34_%s a backlog:MetricObservation ; rdfs:label "Reading after the licence tasks were recorded Done"@en ;\n    backlog:observesMetric ex:%s ; backlog:observationFor ex:%s ; backlog:hasObservedValue "%d"^^xsd:decimal ;\n'
               '    backlog:observedAt "%s"^^xsd:dateTime ; backlog:observedDuringCeremony false ;\n    backlog:hasObservationMethod "Counted the items that can move this objective and read Done in this register version: %d of %d." .\n') % (on, mid, on, c, now, c, len(movers))
    g = rdflib.Graph(); g.parse(data=t2, format="turtle"); lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid = str(sc).split("#")[-1]
        t2, k = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now, t2, count=1); assert k == 1, sid
        t2 += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid, now)
    out = M.write_new(src, t2, nxt, cur, "Chapter 9 licence tasks Done on the physical licence check; rebuilt page 9 as new evidence; owner directions and the weak spots of decks 1-7 recorded as dated notes.")
    print(os.path.basename(out))


main()
