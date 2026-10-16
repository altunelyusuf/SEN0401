#!/usr/bin/env python3
"""sen0401_lineage_followup_pages v1_0_0 - records the page link pass (pages of chapters 1 to 14 rebuilt with the deck link labels) as one ExecutionTask per chapter under the
existing page story (ruling G117: no story added). A task is Done only when the evidence bridge verified the chapter check Page/ChNN and the SHA-256 of the page; the others
get no task; the reason is a dated note on the story, which stays as it was. The task's start and finish are the commit time of the page (one commit is the whole work step). The Done records of the stories stay untouched.
Usage: sen0401_lineage_followup_pages_v1_0_0.py FACTS.json BRIDGE.ttl[,BRIDGE2.ttl: a later file overrides an earlier verdict]      (env REASON_ST_Page_ChNN for a chapter whose check did not verify; NOTE_ST_Page_ChNN extra disclosure)
"""
__version__ = "1.0.0"
import json, os, re, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

S.CHECK = "08-tooling/sen0401_lineage_chapter_check_v1_1_0.py"
TAG = "PL"


def main():
    facts = json.load(open(sys.argv[1])); vd = {}
    for bp in sys.argv[2].split(","):
        vd.update(S.verdicts(bp))
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); add = []; done = []; open_ = []; members = []; planned = []
    for sid, f in facts["stories"].items():
        ch = sid.split("_")[2]; n = ch[2:]; tid = "TK_Page_%s_LinkPass" % ch; te = "Ev3%s_%s" % (TAG, sid[3:]); files = ["%s_File%d" % (te, i + 1) for i in range(len(f["artifacts"]))]
        a = f["artifacts"][0]; ok = te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files)
        note = "Page link pass of chapter %s: the page %s (commit %s) rebuilt with the deck link labels." % (n, os.path.basename(a["path"]), a["last_commit"]) + os.environ.get("NOTE_" + sid, "")
        if ok:
            add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for Page %s, link pass"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasTestId "Page/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (te, ch, ch, S.CHECK, S.esc(vd[te][2]), vd[te][1]))
            for i, fl in enumerate(files):
                add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                           '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                           % (fl, os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], S.esc(vd[fl][2]), vd[fl][1]))
            state = 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid ; backlog:hasAcceptanceCriterion ex:AC_Chapter' % (f["finished"], f["finished"], vd[te][1]); ev = "    backlog:hasEvidence %s ;\n" % ", ".join("ex:" + x for x in [te] + files); done.append(ch); planned.append("ex:" + tid)
            add.append('ex:Harness3_Page_%s_LinkPass a backlog:TestHarness ; rdfs:label "Chapter check for Page %s, link pass"@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence ex:%s .\n' % (ch, ch, tid, te))
        else:
            open_.append(ch); add.append('ex:%s backlog:hasAuditNote "%s" .\n' % (sid, S.esc(note + " NOT recorded Done, no task: " + os.environ.get("REASON_" + sid, "the bridge did not verify the chapter check") + ".")))
            continue
        add.append('ex:%s a backlog:ExecutionTask ; rdfs:label "Page for %s: link pass"@en ; backlog:hasIdentifier "%s" ; backlog:hasTitle "Link pass of the page for %s" ;\n    backlog:belongsToLineage ex:Lineage2 ; backlog:memberOfContainer ex:Iter_11 ; backlog:preLineageItem true ; backlog:admittedByOutput ex:Out2_Backlog ; %s ; backlog:responsible ex:Executor_ClaudeCodeSession ;\n'
                   '    backlog:hasInvestmentCategory backlog:Cat_NewCapability ; backlog:hasTaskType backlog:TaskType_Build ; backlog:effectiveDefinitionOfDone ex:DoD ;\n%s    backlog:notYetScoreable true ; backlog:hasScoreabilityReason "Ranked by its story\'s score; scoring both would double-count." ;\n    backlog:hasAuditNote "%s" .\n'
                   % (tid, ch, tid, ch, state, ev, S.esc(note)))
        add.append("ex:%s backlog:decomposesInto ex:%s .\n" % (sid, tid)); members.append("ex:" + tid)
    add.append("ex:Iter_11 backlog:hasMember %s .\n" % ", ".join(members))
    add.append("ex:Plan_Page_Followup backlog:producesTask %s .\n" % ", ".join(planned))
    t += "\n" + "".join(add); add = []
    # an open item's score may not predate a completion in the register (L3): re-run, same components and value, dated now
    g = rdflib.Graph(); g.parse(data=t, format="turtle"); B = M.B; now_iso = M.now()
    lastfin = max(str(x) for x in g.objects(None, B.finishedAt))
    for sc in sorted(set(g.subjects(rdflib.RDF.type, B.PriorityScore)), key=str):
        items = list(g.subjects(B.hasPriorityScore, sc))
        if not items or any((i, B.hasState, B.Done) in g or (i, B.hasState, B.Cancelled) in g for i in items) or str(g.value(sc, B.scoredAt)) >= lastfin:
            continue
        sid2 = str(sc).split("#")[-1]
        t, n = re.subn(r'(ex:%s a backlog:PriorityScore[^\n]*\n[^\n]*backlog:scoredAt )"[^"]*"' % re.escape(sid2), r'\g<1>"%s"' % now_iso, t, count=1)
        assert n == 1, sid2
        t += 'ex:%s rdfs:comment "Re-run %s: the components and the value are unchanged; it had to be dated after the completions recorded in this version, which changed nothing about this item."@en .\n' % (sid2, now_iso[:10])
    out = M.write_new(src, t, nxt, cur, "Page link pass recorded as one task per chapter under the existing page stories: Done for %s (bridge-verified); not Done for %s." % (", ".join(done), ", ".join(open_) or "none"))
    print(os.path.basename(out), "done", done, "open", open_)


main()
