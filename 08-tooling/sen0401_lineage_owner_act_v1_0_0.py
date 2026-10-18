#!/usr/bin/env python3
"""sen0401_lineage_owner_act v1_0_0 - records, in ONE new register version, the owner's dated answers of 2026-10-19 (local 00:42 Istanbul, 2026-10-18T21:42:00 UTC) in his own words, as relayed by the course coordinator,
and the decisions that follow from them. The course session only records them: it re-affirms nothing itself (G14). Notes only: no state, evidence, digest or output changes.
It also records, as a correction of its own, that the Scope, Goal and Objective elements of the second and third lineage carry the intent origin "owner stated" although the session drafted them (G14).
Usage: sen0401_lineage_owner_act_v1_0_0.py
"""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M

WHEN = "2026-10-19 00:42 Istanbul (2026-10-18T21:42:00 UTC)"
SRC = "relayed by the course coordinator, recorded by the course session"


def main():
    src = M.newest(); nxt, cur = M.next_version(src); t = open(src, encoding="utf-8").read(); L = []
    c = lambda s, txt: L.append('ex:%s rdfs:comment "%s"@en .\n' % (s, M.esc(txt)))
    n = lambda s, txt: L.append('ex:%s backlog:hasAuditNote "%s" .\n' % (s, M.esc(txt)))
    c("Mission", "Owner's act, %s (%s): the owner re-affirmed this Mission himself (G14), in his words: \"OK. I do.\" The course session recorded it and did not re-affirm it." % (WHEN, SRC))
    c("Lineage3", "Owner's act, %s (%s): the owner confirmed the succession from the second lineage to this lineage and re-affirmed the Mission, in his words: \"OK. I do.\"" % (WHEN, SRC))
    c("Succession_Lineage2_3", "Owner's act, %s (%s): confirmed by the owner, in his words: \"OK. I do.\"" % (WHEN, SRC))
    for i in range(4, 12):
        c("Iter_%d" % i, "Owner's act, %s (%s): the proposed iteration dates were confirmed by the owner, in his words: \"Confirming the dates\" (this iteration ends %s)." % (WHEN, SRC, {4: "2026-10-16", 5: "2026-10-23", 6: "2026-10-30", 7: "2026-11-06", 8: "2026-11-13", 9: "2026-11-20", 10: "2026-11-27", 11: "2026-10-23"}[i]))
    n("TK_Licence_BOLT_Ch09", "Owner's decision, %s (%s): the BOLT text is licensed \"CC BY 4.0\" (not CC0). The task stays open until the provenance of page 9 is corrected to this and the correction is verified by the evidence bridge." % (WHEN, SRC))
    rule = "Owner's decision, %s (%s): \"Keep the same standards with all other pages.\" No relaxation: this page must pass the same checks as the other pages. %s"
    n("ST_Page_Ch06", rule % (WHEN, SRC, "The work is a lighter page for chapter 6. The story stays open until the bridge verifies it."))
    n("ST_Page_Ch13", rule % (WHEN, SRC, "The work is honest numeric examples for chapter 13. The story stays open until the bridge verifies it."))
    for x in ("ST_Deck_LinkPass",):
        n(x, "Owner's decision, %s (%s) on the decks of chapters 1 to 4 and the page of chapter 13: \"You tell me if they are failing or needing corrections and update.\" Status: they ARE failing their checks (reasons in this note's story) and need corrections; the corrections run as separate work (tasks of the carried follow-up) and nothing is recorded Done until the evidence bridge verifies it." % (WHEN, SRC))
    for tk in ("TK_Deck_Ch01_CheckFix", "TK_Deck_Ch02_CheckFix", "TK_Deck_Ch03_CheckFix", "TK_Deck_Ch04_CheckFix", "TK_Page_Ch13_Build", "TK_Page_Ch13_Verify"):
        n(tk, "Owner's decision, %s (%s): \"You tell me if they are failing or needing corrections and update.\" This item is failing its check and the correction is wanted; it is Done only when the evidence bridge verifies it." % (WHEN, SRC))
    corr = ("Correction recorded by the course session, 2026-10-19 (G14): this element was drafted by the session but carries the intent origin owner stated and the decision by the owner. "
            "The owner's answer of %s covers the succession and the Mission only; he did not review the text of this element." % WHEN)
    for s in ("Scope2", "G2_FinishedAdmitted", "G2_EveryAdmittedChapterProven", "G2_DatesAreGitsDates", "G2_NothingRebuilt", "G2_RemainingChaptersTeachTheBook", "Obj2_AdmittedDone", "Obj2_EvidenceVerified", "Obj2_DatesFromGit", "Obj2_NothingRebuilt", "Obj2_DecksRemaining", "Obj2_ResearchRemaining", "Obj2_PagesRemaining",
              "Scope3", "G3_LinksNameTheirResource", "G3_LinkPassesProven", "G3_FailuresStayVisible", "G3_NothingRebuilt", "G3_OpenWorkCarried", "Obj3_LinkPassesDone", "Obj3_EvidenceVerified", "Obj3_DatesFromGit", "Obj3_FailuresNamed", "Obj3_NothingRebuilt", "Obj3_OpenWorkFinished"):
        c(s, corr)
    out = M.write_new(src, t + "\n" + "".join(L), nxt, cur, "The owner's answers of 2026-10-19 recorded as his dated act (succession and Mission confirmed, iteration dates confirmed, BOLT licence CC BY 4.0, same standards for the pages of chapters 6 and 13, status of the chapters 1-4 decks and the chapter 13 page); the intent-origin correction of the second and third lineage elements. Notes only.")
    print(os.path.basename(out))


main()
