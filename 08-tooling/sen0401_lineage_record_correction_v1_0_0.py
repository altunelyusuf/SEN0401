#!/usr/bin/env python3
"""sen0401_lineage_record_correction v1_0_0 - when the files a Done story cites are CORRECTED by a later version, the Done record is not edited: a NEW register version adds
(1) new evidence nodes (the chapter check run again by the evidence bridge, and one ArtifactEvidence with the SHA-256 of each file of the corrected version) and
(2) a dated note on the story, both linked to the story beside the older evidence, which stays and still verifies against the older files kept in git history.

Usage:
  sen0401_lineage_record_correction_v1_0_0.py draft FACTS.json OUT.ttl TAG STORY[,STORY...]
  sen0401_lineage_record_correction_v1_0_0.py record FACTS.json BRIDGE.ttl TAG STORY[,STORY...]      env NOTE_<STORY>=text, the dated note of that story
TAG names the correction (e.g. C1): new evidence ids are Ev3<TAG>_<Kind>_<Ch>[_FileN].
"""
__version__ = "1.0.0"
import json, os, sys
import rdflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_successor_stages_v1_1_0 as S

S.CHECK = "08-tooling/sen0401_lineage_chapter_check_v1_1_0.py"


def main():
    ev, facts_p = sys.argv[1], sys.argv[2]
    facts = json.load(open(facts_p))
    tag = sys.argv[-2] if ev == "draft" else sys.argv[4]
    stories = sys.argv[-1].split(",") if ev == "draft" else sys.argv[5].split(",")
    S.ev_ids = lambda sid, k: ("Ev3%s_%s" % (tag, sid[3:]), ["Ev3%s_%s_File%d" % (tag, sid[3:], i + 1) for i in range(k)])
    if ev == "draft":
        open(sys.argv[3], "w", encoding="utf-8").write(S.evidence_draft(facts, stories)); return
    vd = S.verdicts(sys.argv[3])
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); add = []
    for sid in stories:
        f = facts["stories"][sid]; te, files = S.ev_ids(sid, len(f["artifacts"])); kind, ch = sid.split("_")[1], sid.split("_")[2]
        assert te in vd and vd[te][0] and all(x in vd and vd[x][0] for x in files), sid + ": the bridge did not verify the corrected files; no correction is recorded"
        aud = vd[te][1]
        add.append('ex:%s a backlog:TestEvidence ; rdfs:label "Chapter check for %s %s, run again on the corrected files (%s)"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                   '    backlog:evidenceVerified true ; backlog:hasTestId "%s/%s" ; backlog:hasTestSpec "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0 with the course repository as workspace" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                   % (te, kind, ch, tag, kind, ch, S.CHECK, S.esc(vd[te][2]), aud))
        for i, a in enumerate(f["artifacts"]):
            add.append('ex:%s a backlog:ArtifactEvidence ; rdfs:label "%s, committed %s (last change %s UTC), corrected version"@en ; backlog:belongsToLineage ex:Lineage2 ; backlog:attestsCriterion ex:AC_Chapter, ex:AC2_Admission ;\n'
                       '    backlog:evidenceVerified true ; backlog:hasArtifactPath "%s" ; backlog:hasArtifactSHA256 "%s" ;\n    backlog:hasVerificationMethod "%s" ;\n    backlog:verifiedByTool "backlog_evidence_bridge_v1_1_0" ;\n    backlog:verifiedAt "%s"^^xsd:dateTime .\n'
                       % (files[i], os.path.basename(a["path"]), a["last_commit"], a["last_commit_utc"], a["path"], a["sha256"], S.esc(vd[files[i]][2]), vd[files[i]][1]))
        add.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote "%s" .\n' % (sid, ", ".join("ex:" + x for x in [te] + files), S.esc(os.environ["NOTE_" + sid])))
    out = M.write_new(src, t + "\n" + "".join(add), nxt, cur, "Corrected research files recorded for %s as new evidence and a dated note; the Done records and the older evidence are untouched." % ", ".join(stories))
    print(os.path.basename(out))


main()
