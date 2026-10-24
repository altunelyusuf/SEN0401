#!/usr/bin/env python3
"""sen0401_lineage_settle21 v1_0_0 - settles the items that the change route of ex:CR3_Repair21 supersedes (decided by the lineage under the owner's standing rule of 2026-10-24, relayed by the course coordinator: a lineage never waits on questions unrelated to its work; work the lineage enforces but the actual work misses must be dealt with):
 (1) tasks withdrawn (T_WithdrawReady / Proposed / Suspended -> Cancelled, with a rationale): the page tasks of chapters 7 and 8 (replaced by the restated tasks of Iteration 23), the regression task (replaced by TK_Remedy_Regress_R) and the two open tasks of ST_Repair_Page_Ch05 (the page is delivered by ST_Charset_Page_Ch05, Done);
 (2) stories withdrawn (T_WithdrawInProgress / Ready): ST_Ch07_Deck, ST_Ch07_Page, ST_Ch08_Page, ST_Remedy_Page_Ch05, ST_Repair_Page_Ch05 - not Done, their criteria are not met and are not waived: each is restated or carried or delivered under the named criterion;
 (3) ST_Remedy_Tools: its regression criterion is carried (AC8R_Regress); the story is closed Done on its other three tasks, as ST_Section_Links was closed (review ceremony);
 (4) review ceremonies close Iterations 17, 18 and 20 (every member Done or Cancelled); no iteration end is moved: nothing open is left in them.
Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rdflib
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
B = rdflib.Namespace("http://example.org/backlog#"); E = rdflib.Namespace("http://example.org/sen0401-slides-lineage#")


def evidence_of(g, tasks):
    ev = set()
    for k in tasks:
        for e in g.objects(E[k], B.hasEvidence):
            v = g.value(e, B.evidenceVerified)
            if v is not None and str(v).lower() == "true": ev.add(str(e).split("#")[1])
    return sorted(ev)


lit = C.lit; CR = "ex:CR3_Repair21"
RULE = "the owner's standing rule of 2026-10-24 (relayed by the course coordinator): a lineage never waits on questions unrelated to its work; when the answerer is not a person, the lineage's agentic system decides without a handover; work the lineage enforces but the actual work misses must be dealt with"
TASKS = [("TK_Ch07_Page_Build", "T_WithdrawReady", "Ready", "TK_Ch07_Page_Build_R", "which builds the page of chapter 7 on the re-issued deck under the criterion restated on the page test 9.37.0", "it never started"),
         ("TK_Ch07_Page_Verify", "T_WithdrawProposed", "Proposed", "TK_Ch07_Page_Verify_R", "which verifies that page", "it never started"),
         ("TK_Ch08_Page_Build", "T_WithdrawSuspended", "Suspended", "TK_Ch08_Page_Finish", "which finishes the page 9.85.0 of chapter 8 (checks on the page test 9.37.0, stored result and Stage 4 ABox as new files)", "its result (the page 9.85.0, commits 75e0a47 and 0e34361, failing only the page test 9.36.0 on P2; the control of v0.255.0) stays in the register as history"),
         ("TK_Ch08_Page_Verify", "T_WithdrawProposed", "Proposed", "TK_Ch08_Page_Finish_Verify", "which verifies the finished page", "it never started"),
         ("TK_Remedy_Regress", "T_WithdrawProposed", "Proposed", "TK_Remedy_Regress_R", "which carries the regression on the template 9.52.2 (this task names the template 9.52.0, which no page uses)", "it never started"),
         ("TK_Repair_Page_Ch05_Build", "T_WithdrawSuspended", "Suspended", "TK_Charset_Page_Ch05_Build", "of ST_Charset_Page_Ch05 (Done), which rebuilt the page of chapter 5 on template 9.52.2 (page 9.83.0, controlled MET)", "its result (the page 9.80.0 failing the story-chip feature) stays in the register as history"),
         ("TK_Repair_Page_Ch05_Verify", "T_WithdrawProposed", "Proposed", "TK_Charset_Page_Ch05_Verify", "of ST_Charset_Page_Ch05 (Done)", "it never started")]
STORIES = [("ST_Ch07_Deck", "T_WithdrawInProgress", "InProgress", "AC7_Deck_Ch07", "ST_Ch07_Deck_Reissue and its criterion AC7R_Deck_Ch07 (MET in v0.257.0)", "the deck v2_0_0 passed every element but 'no committed file edited' (control of v0.244.0)"),
           ("ST_Ch07_Page", "T_WithdrawReady", "Ready", "AC7_Page_Ch07", "ST_Ch07_Page_R and its criterion AC8R_Page_Ch07 (the same elements on the page test 9.37.0)", "it never started"),
           ("ST_Ch08_Page", "T_WithdrawInProgress", "InProgress", "AC7_Page_Ch08", "ST_Ch08_Page_R and its criterion AC8R_Page_Ch08 (the same elements on the page test 9.37.0)", "the page 9.85.0 failed only the page test 9.36.0 on P2 (control of v0.255.0)"),
           ("ST_Remedy_Page_Ch05", "T_WithdrawInProgress", "InProgress", "AC4R_Page_Ch05", "ST_Charset_Page_Ch05 (Done) and its criterion AC6R_Page_Ch05 (MET): the page of chapter 5 is delivered on template 9.52.2 and measured by the later criterion; both tasks of this story were already withdrawn", "its page was rebuilt twice since"),
           ("ST_Repair_Page_Ch05", "T_WithdrawInProgress", "InProgress", "AC5R_Page_Ch05", "ST_Charset_Page_Ch05 (Done) and its criterion AC6R_Page_Ch05 (MET)", "its page 9.80.0 was replaced by 9.83.0")]
ITERS = [(17, "RC3S_Iter_17", ["ST_Remedy_Tools"]), (18, "RC3S_Iter_18", []), (20, "RC3S_Iter_20", [])]
def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
    for tk, via, frm, sup, what, hist in TASKS:
        i, j = T.blk(t, tk); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, (tk, frm)
        why = "Closed %s UTC by the change route of %s (v%s), decided by the lineage under %s: the task is superseded by %s, %s; it is withdrawn, not Done, and %s." % (now, CR, nxt, RULE, sup, what, hist)
        nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled", 1)
        nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
        nb = re.sub(r'backlog:lastAuditedAt "[^"]*"', 'backlog:lastAuditedAt "%s"' % now, nb, count=1) if "lastAuditedAt" in nb else nb.replace("backlog:hasState backlog:Cancelled", 'backlog:hasState backlog:Cancelled ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
        t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("Wd46T_" + tk, tk, via, at, why, tk + " withdrawn"))
    for sid, via, frm, crit, sup, hist in STORIES:
        i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, (sid, frm)
        tks = re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1))
        for k in tks: assert "backlog:hasState backlog:Cancelled" in t[T.blk(t, k)[0]:T.blk(t, k)[1]], (sid, k)
        why = "Closed %s UTC by the change route of %s (v%s), decided by the lineage under %s: the story is superseded by %s; it is withdrawn, not Done: its criterion ex:%s is NOT met and is NOT waived (it is restated or delivered under the criterion named, with every element kept); %s." % (now, CR, nxt, RULE, sup, crit, hist)
        nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled", 1)
        nb = nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
        nb = re.sub(r'backlog:lastAuditedAt "[^"]*"\^\^xsd:dateTime', 'backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, nb, count=1)
        if "lastAuditedAt" not in nb: nb = nb.replace("backlog:hasState backlog:Cancelled", 'backlog:hasState backlog:Cancelled ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
        t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("Wd46T_" + sid, sid, via, at, why, sid + " withdrawn"))
        L.append("ex:%s backlog:hasAuditNote %s .\n" % (crit, lit("Not met, not waived (%s): the story that carried this criterion is withdrawn by the change route of %s because it is superseded by %s." % (now[:10], CR, sup))))
    # ST_Remedy_Tools: the regression criterion is carried, the story is closed on its three other tasks
    sid = "ST_Remedy_Tools"; i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:InProgress" in b and "backlog:hasAcceptanceCriterion ex:AC4R_DeckCheck, ex:AC4R_PageTest, ex:AC4R_Template, ex:AC4R_Regress" in b
    g = rdflib.Graph(); g.parse(src, format="turtle"); done = ["TK_Remedy_DeckCheck", "TK_Remedy_PageTest", "TK_Remedy_Template"]
    for k in done: assert "backlog:hasState backlog:Done" in t[T.blk(t, k)[0]:T.blk(t, k)[1]], k
    fin = max(re.findall(r'finishedAt "([^"]*)"', "".join(t[T.blk(t, k)[0]:T.blk(t, k)[1]] for k in done))); ev = evidence_of(g, done); assert ev
    m = re.search(r'backlog:hasState backlog:InProgress ; backlog:startedAt "([^"]*)"\^\^xsd:dateTime', b); assert m
    time.sleep(1.1); at = M.now(); RC = "RC3S_Iter_17"
    nb = b.replace(m.group(0), 'backlog:hasState backlog:Done ; backlog:startedAt "%s"^^xsd:dateTime ; backlog:finishedAt "%s"^^xsd:dateTime ; backlog:lastAuditedAt "%s"^^xsd:dateTime ; backlog:hasExecutionModality backlog:Mode_Hybrid' % (m.group(1), fin, at), 1)
    nb = nb.replace("backlog:hasAcceptanceCriterion ex:AC4R_DeckCheck, ex:AC4R_PageTest, ex:AC4R_Template, ex:AC4R_Regress", "backlog:hasAcceptanceCriterion ex:AC4R_DeckCheck, ex:AC4R_PageTest, ex:AC4R_Template", 1)
    t = t[:i] + nb + t[j:]
    L.append(C.transition("Done46T_" + sid, sid, "T_Complete", at, "Done at the review ex:%s on %s UTC: its three tasks that carry criteria AC4R_DeckCheck, AC4R_PageTest and AC4R_Template are Done on bridge-verified evidence; the fourth, TK_Remedy_Regress, is withdrawn and its criterion AC4R_Regress is carried, not waived, as AC8R_Regress of ex:ST_Remedy_Regress_R (G125)." % (RC, at), sid + " completed"))
    L.append('ex:Harness46_%s a backlog:TestHarness ; rdfs:label %s@en ; backlog:harnessFor ex:%s ; backlog:hasHarnessEvidence %s .\n' % (sid, lit("Checks run for " + sid), sid, ", ".join("ex:" + e for e in ev)))
    L.append('ex:%s backlog:hasEvidence %s ;\n    backlog:hasAuditNote %s .\n' % (sid, ", ".join("ex:" + e for e in ev), lit("Closed %s UTC at the review ex:%s by the lineage under %s: the criteria AC4R_DeckCheck, AC4R_PageTest and AC4R_Template are met on bridge-verified evidence recorded in the tasks' audit notes; the criterion AC4R_Regress is detached from the story and carried by the change route %s as ex:AC8R_Regress (template 9.52.2 instead of the replaced 9.52.0) in ex:ST_Remedy_Regress_R. It is NOT waived." % (at, RC, RULE, CR))))
    L.append("ex:AC4R_Regress backlog:hasAuditNote %s ;\n    rdfs:seeAlso ex:AC8R_Regress .\n" % lit("Carried %s by the change route of %s: the criterion is NOT met and is NOT waived. It names the template 9.52.0, which was replaced by 9.52.1 and 9.52.2; it is restated on 9.52.2 as ex:AC8R_Regress with every other element kept." % (now[:10], CR)))
    # review ceremonies closing the iterations
    t2 = t + "\n" + "".join(L); L2 = []
    for n, rc, stories in ITERS:
        time.sleep(1.1); at = M.now(); I = "Iter_%d" % n; i, j = T.blk(t2, I); blk = t2[i:j]
        mem = re.findall(r"ex:((?:ST|TK)_\w+)", re.search(r"backlog:hasMember ([^.]*)\.", blk, re.S).group(1))
        bad = [x for x in mem if not re.search(r"hasState backlog:(Done|Cancelled)", t2[T.blk(t2, x)[0]:T.blk(t2, x)[1]])]
        assert not bad, (n, bad)
        flag = [x for x in mem if x.startswith("ST_") and "backlog:hasState backlog:Done" not in t2[T.blk(t2, x)[0]:T.blk(t2, x)[1]]]
        L2.append('ex:%s a backlog:SprintReviewCeremony ; rdfs:label %s@en ; backlog:ceremonyFor ex:%s ; backlog:reviewsCeremony ex:PC3_Iter_%d ; backlog:closesIteration ex:%s ;%s%s backlog:heldAt "%s"^^xsd:dateTime ;\n    rdfs:comment %s@en .\n' % (
            rc, lit("Review of iteration %d: the items superseded by the change route of the same day are withdrawn, the iteration is closed" % n), I, n, I, (" backlog:closesStory " + ", ".join("ex:" + s for s in stories) + " ;") if stories else "", (" backlog:flagsForCarryOver " + ", ".join("ex:" + s for s in flag) + " ;") if flag else "", at,
            lit("Held %s UTC by the builder session under %s: every member of the iteration is Done or withdrawn (Cancelled) by the change route %s, so no end is moved and the withdrawn stories (%s) are flagged for carry-over: their criteria are carried, not waived, by the stories and criteria named in their rationales (AC7R_Deck_Ch07, AC8R_Page_Ch07, AC8R_Page_Ch08, AC8R_Regress, AC6R_Page_Ch05). The readings of the objectives are those of the earlier review of the iteration." % (at, RULE, CR, ", ".join(flag) or "none"))))
        t2 += "".join(L2[-1:])
    t3 = X.set_status(t2, "LS_InProgress")
    print(os.path.basename(M.write_new(src, t3, nxt, cur, "Superseded items settled by the lineage under the owner's standing rule of 2026-10-24 (change route %s): page tasks and stories of chapters 7 and 8, the regression task, the old stories of chapter 5 and the deck story of chapter 7 are withdrawn (not Done, criteria restated or carried, none waived); ST_Remedy_Tools closed on its three other tasks; Iterations 17, 18 and 20 closed without moving an end." % CR)))
if __name__ == "__main__": main()
