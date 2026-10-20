#!/usr/bin/env python3
"""sen0401_lineage_closure_report v1_0_0 - ONE new register version that adds the ClosureReport of the Mission (G71, G95/G96). It is committed BEFORE the Mission outcome and the Lineage3 status change,
so the report precedes the outcome it justifies; closureCommittedAt is filled by a later version once this commit exists. This version does NOT set the Mission outcome or Lineage3 Achieved: that waits for the owner's act.
The caveats are the ones the register notes and the status files (08-tooling/stage4_status.md, 08-tooling/page_jobs_status.md, 08-tooling/README_BUILD_v1_1_0.md) state, read from them on the day of writing.
Usage: sen0401_lineage_closure_report_v1_0_0.py"""
__version__ = "1.0.0"
import os, sys
import rdflib
from rdflib import Namespace, RDF
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
B = Namespace("http://example.org/backlog#"); EX = Namespace("http://example.org/sen0401-slides-lineage#")
ln = lambda x: str(x).split("#")[-1]

CAVEATS = [
 "The page tests ran against a copy of each page carrying a TEST release key: they prove the page logic, not the instructor's real key.",
 "Stand-in pictures remain on the decks named in their audit notes (chapters 2, 4, 5, 6, 8, 9, 10, 11, 12, 13 and 14) where no free picture of the event exists (for example the Bitcoin logo, the Satoshi bust, the Mt. Gox logo, a Trezor Model T for the Safe 5); each note names its slides.",
 "Stage4.L, Cross.C, Stage1.C and Stage1.E report NOT_MEASURED (the research files carry no concept inventory) and Cross.B reports CANNOT_RUN (the Stage 3 documents record a section's concept in dcterms:source, not prov:wasDerivedFrom); none of these is a pass and none is claimed as one (08-tooling/stage4_status.md).",
 "The page of chapter 8 keeps its known result under the older page test 9.34.0 (113 pass, 1 fail, then a crash); the recorded check runs the newest test 9.35.0 and does not show it; it is unchanged and not claimed to pass.",
 "The pages of chapters 8, 10, 11, 12 and 14 are on templates older than 9.51.0 (their page files are v9.51.0, v9.53.0, v9.54.0, v9.55.0 and v9.57.0); the pages of chapters 1 to 7, 9 and 13 are on 9.51.0 (08-tooling/page_jobs_status.md).",
 "web.archive.org is unreachable from the build sandbox (the chapter 14 deck links check fails for 1 of 14 links; sec.gov, cnbc.com and coingecko.com also answer 403 or no connection), so those links were not verified by the builders.",
 "Stage 4 page ABoxes of the current pipeline exist for chapters 8 to 14 only; the page ABoxes of chapters 1 to 4 and of the numbers page are earlier versions (v9.4.2 and v1.0.0) and chapters 5 to 7 have none. Stage 3.F was repaired for chapters 2 to 4 and 8; the build notes of 2026-10-14 name chapter 7 among those failing it and this register records no repair for it. The register's notes name no gap on chapter 1 or the numbers page, and none is claimed absent.",
 "The connectedness findings on 15 research T-Box files (OE v2.18.0 BP-D56 and v2.19.0 BP-D57, shipped after those stories were Done) are not repaired in this lineage: the owner's direction of 2026-10-20 09:19 Istanbul deferred quality and cleaning work, and ruling G133 routes the repair to new work by the change route in a later lineage.",
]
PRACTICE = [
 "Read a stage's obligations before writing and satisfy them in the same step; a waiver is drift. The class-model debt of the Backlog stage was paid by a stage revision, not waived.",
 "Work on the deliverable of a Done story is a story of its own (G125); a task hung under a finished story makes the parent's finish contradict its child.",
 "Record Done only what the evidence bridge verifies, and never claim a NOT_MEASURED or CANNOT_RUN gate as a pass.",
 "Count what an objective measures, not the stories that read Done: two readings in this register counted Done stories and were corrected forward.",
 "Audit status, dates and parent-child agreement before closing: 84 inconsistencies were found in one audit and repaired by sanctioned routes.",
 "Record work that follows from an owner's direction as owner-directed, with the quoted direction and its time.",
]


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); now = M.now()
    g = rdflib.Graph(); g.parse(data=t, format="turtle")
    assert not list(g.subjects(RDF.type, B.ClosureReport)), "a report exists"
    objs = sorted(g.subjects(RDF.type, B.Objective), key=str); finds = sorted(g.subjects(RDF.type, B.RetrospectiveFinding), key=str)
    nt = sum(1 for _ in g.subjects(RDF.type, B.ExecutionTask)); ns = sum(1 for _ in g.subjects(RDF.type, B.Story))
    assert all((x, B.hasState, B.Done) in g for c in ("ExecutionTask", "Story", "Epic", "Initiative") for x in g.subjects(RDF.type, B[c]))
    summary = ("Closure report of the Mission 'Teach SEN0401 from the edition students can now read for free', written %s for the third lineage, after the first two lineages achieved their own scopes. "
               "Achieved: for each of the 14 chapters of Mastering Bitcoin 3rd edition the research, the lecture deck and the interactive page are recorded Done with evidence the evidence bridge verified; the supplementary numbers page is Done; the two link passes over all decks and pages are Done; "
               "all %d stories, %d tasks, the 3 epics and the initiative read Done; all %d objectives are at target (Obj3_FailuresNamed was corrected forward to 5 on 2026-10-20); the register validates CONFORMANT and every lineage's digests reproduce. "
               "NOT achieved or not claimed: " % (now[:10], ns, nt, len(objs))
               + " ".join("(%d) %s" % (i + 1, c) for i, c in enumerate(CAVEATS))
               + " This report does not set the Mission outcome or the status of the third lineage; both wait for the owner's act.")
    L = ['ex:CR_SEN0401 a backlog:ClosureReport ; rdfs:label "Closure report of the SEN0401 slides Mission"@en ; backlog:belongsToLineage ex:Lineage3 ; backlog:closesForMission ex:Mission ;',
         '    backlog:reportGeneratedAt "%s"^^xsd:dateTime ;' % now,
         '    backlog:hasClosureSummary "%s" ;' % M.esc(summary),
         "    backlog:reportsOnObjective " + ", ".join("ex:" + ln(o) for o in objs) + " ;",
         "    backlog:citesFinding " + ", ".join("ex:" + ln(f) for f in finds) + " ;",
         "    backlog:statesBestPractice " + " , ".join('"%s"' % M.esc(p) for p in PRACTICE) + " ."]
    t += "\n" + "\n".join(L) + "\n"
    out = M.write_new(src, t, nxt, cur, "The ClosureReport of the Mission added (summary, %d objectives, %d retrospective findings, %d caveats, %d practices). The Mission outcome and the status of the third lineage are NOT changed: they wait for the owner's act." % (len(objs), len(finds), len(CAVEATS), len(PRACTICE)))
    print(os.path.basename(out), len(objs), len(finds))


main()
