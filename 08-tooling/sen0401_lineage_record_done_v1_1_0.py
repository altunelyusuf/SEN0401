#!/usr/bin/env python3
"""v1.1.0 over 1.0.0: re-runs the open scores that predate a completion (L3), writes the second readings of the second lineage objectives in the same version, and can keep a story open on purpose (STORY=REASON).
sen0401_lineage_record_done v1_1_0 - records, in a NEW register version, the admitted stories of chapters 5-7 that are still open as Done, only where the
evidence bridge verified their chapter check (exit 0) and every cited file's SHA-256 AND every story they depend on is Done. Nothing else changes; the committed
version stays. Dates are git's: started = the earliest commit that added any version of the story's files, finished = the last commit of the cited files
(the repaired or rebuilt file's commit, not the day of this record).

Dates: finished = the later of the story own files last commit and the last commit of every story it depends on (a page whose file did not change is Done only once its research is in its final form).
Usage:
  sen0401_lineage_record_done_v1_1_0.py draft FACTS.json OUT.ttl      the evidence nodes before the bridge (no verdict), for backlog_evidence_bridge
  sen0401_lineage_record_done_v1_1_0.py record FACTS.json BRIDGE.ttl LOGDIR [STORY=REASON ...]   (STORY=REASON keeps that story open on purpose, the reason becoming its audit note)   the new register version (a story whose check failed stays open, with the reason as its audit note)
"""
__version__ = "1.1.0"
import json, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S
import sen0401_lineage_observe_v1_1_0 as O

S.CHECK = "08-tooling/sen0401_lineage_chapter_check_v1_1_0.py"
B = S.B


def main():
    ev, facts_p = sys.argv[1], sys.argv[2]
    facts = json.load(open(facts_p))
    if ev == "draft":
        open(sys.argv[3], "w", encoding="utf-8").write(S.evidence_draft(facts, M.ADMIT_STORIES)); return
    bridge_p = sys.argv[3]; logdir = sys.argv[4] if len(sys.argv) > 4 else None
    held = dict(x.split("=", 1) for x in sys.argv[5:])
    src = M.newest(); nxt, cur = M.next_version(src)
    t = open(src, encoding="utf-8").read()
    g0 = rdflib.Graph(); g0.parse(data=t, format="turtle")
    vd = S.verdicts(bridge_p)
    open_now = [s for s in M.ADMIT_STORIES if (rdflib.URIRef(str(S.EXN[s])), B.hasState, B.Done) not in g0]
    verified = {}
    for sid in M.ADMIT_STORIES:
        te, files = S.ev_ids(sid, len(facts["stories"][sid]["artifacts"]))
        verified[sid] = te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files) and sid not in held
    own_fail = [s for s in open_now if not verified[s]]
    deps = {sid: re.findall(r"backlog:dependsOn ex:(\w+)", S.story_block(t, sid).group(0)) for sid in M.ADMIT_STORIES}
    changed = True
    while changed:
        changed = False
        for sid in M.ADMIT_STORIES:
            if verified[sid] and any(d in verified and not verified[d] for d in deps[sid]):
                verified[sid] = False; changed = True
    done, add, now_iso = [], [], M.now()
    for sid in open_now:
        f = facts["stories"][sid]; te, files = S.ev_ids(sid, len(f["artifacts"])); kind, ch = sid.split("_")[1], sid.split("_")[2]
        m = S.story_block(t, sid); blk = m.group(0)
        if verified[sid]:
            nb = blk.replace("backlog:hasState backlog:Proposed ;", "backlog:hasState backlog:Done ;", 1)
            nb = nb.replace('backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Scored when its own iteration is planned." .',
                            'backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Admitted as finished: this story was never planned, so it is not scored." .', 1)
            assert "backlog:Done" in nb and "never planned" in nb, sid
            t = t.replace(blk, nb); done.append(sid); aud = vd[te][1]
            fin = max([f["finished"]] + [facts["stories"][d]["finished"] for d in deps[sid] if d in facts["stories"]])   # Done only once what it depends on was in its final form
            add.append('ex:%s backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ;\n    backlog:hasEvidence %s .\n'
                       % (sid, f["started"], fin, aud, ", ".join("ex:" + x for x in [te] + files)))
            add.append('ex:Harness2_%s a backlog:TestHarness ; rdfs:label "Chapter check for %s %s"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:%s .\n' % (sid[3:], kind, ch, sid, te))
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "%s" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (te, kind, ch, kind, ch, S.CHECK, S.esc(vd[te][2]) + (" (the page test ran against a copy of the page carrying a TEST release key: it proves the page logic, not the instructor's real key)" if kind == "Page" else ""),
                          "backlog_evidence_bridge_v1_1_0 with the course repository as workspace", aud))
            for i, a in enumerate(f["artifacts"]):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                           '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                           % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], S.esc(vd[files[i]][2]), vd[files[i]][1]))
        else:
            why = ""
            if sid in own_fail and logdir:
                lg = os.path.join(logdir, sid[3:].replace("_Ch", "_Ch") + ".log")
                if os.path.exists(lg):
                    L = [l.strip() for l in open(lg, errors="ignore") if "FAIL" in l]
                    why = " Failing lines of the run: " + " | ".join(x[:200] for x in L[:4])
            if sid in held:
                t = t.replace(blk, blk.rstrip("\n").rstrip(" .") + " ;\n    backlog:hasAuditNote \"%s\" .\n\n" % S.esc(held[sid]), 1); continue
            reason = ("Not recorded Done on %s: " % now_iso[:10] + ("its chapter check exited non-zero when the evidence bridge ran it." + why if sid in own_fail else "a story it depends on is not Done.")
                      + " It stays admitted and open; the owner decides how it is closed.")
            t = t.replace(blk, blk.rstrip("\n").rstrip(" .") + " ;\n    backlog:hasAuditNote \"%s\" .\n\n" % S.esc(reason), 1)
    t += "\n" + "".join(add)
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    t += S.lineage1_readings(g, done, now_iso, "22")
    # an open item's score may not predate a completion in the register (L3, BP-D11): the WSJF of the planned chapters is re-run (same components, same values) and dated now
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    rescored = []
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items):
            continue
        at = str(g.value(sc, B.scoredAt))
        if at < lastfin:
            sid = str(sc).split("#")[-1]
            t, n = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid), r'\g<1>"%s"' % now_iso, t, count=1)
            assert n == 1, sid
            t += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version (%s), which changed nothing about this item."@en .\n' % (sid, now_iso[:10], ", ".join(done[:3]) + (", ..." if len(done) > 3 else ""))
            rescored.append(sid)
    blk, vals, _ = O.block(t, "22")
    t += "\n" + blk
    names = ", ".join(done) or "none"
    out = M.write_new(src, t, nxt, cur, "Recorded Done through the evidence bridge (chapter check exit 0 and every cited file's SHA-256 verified, dependencies Done): %s. Open after the run: %s. The open scores of the planned chapter were re-run, unchanged (%s). Second readings of the second lineage's objectives written." % (names, ", ".join(s for s in open_now if s not in done) or "none", ", ".join(rescored) or "none"))
    print(os.path.basename(out), "done:", done, "open:", [s for s in open_now if s not in done])


main()
