#!/usr/bin/env python3
"""sen0401_lineage_retro24_withdraw v1_0_0 - withdraws the items of Iteration 21 that the change route of ex:CR3_Retro24 supersedes (decided by the lineage under the owner's standing orders): the 20 retrofit stories ST_ChNN_Deck / ST_ChNN_Page of chapters 1 to 4 and 9 to 14 with their 40 tasks,
and ST_Section_Links_Ch11 with TK_SecLinks_Ch11_Verify_R (the section-link ERD is carried by the restated page task of chapter 11). All are Proposed: none started, none Done. Tasks first (T_WithdrawProposed -> Cancelled, with a rationale), then stories; a criterion of a withdrawn story is NOT met and NOT waived: it is restated as AC9_*.
Same pattern as sen0401_lineage_settle21 and sen0401_lineage_rep20_withdraw. Usage: no arguments; writes one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; CR = "ex:CR3_Retro24"
RULE = "the owner's standing orders (retrofit all chapters starting with chapter 1; repairs re-rank the open items; a lineage never waits on unrelated questions)"
CH = ["01", "02", "03", "04", "09", "10", "11", "12", "13", "14"]
def main():
    src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
    tasks = []; stories = []
    for nn in CH:
        for k in ("Deck", "Page"):
            for s in ("Build", "Verify"):
                tasks.append(("TK_Ch%s_%s_%s" % (nn, k, s), "TK_Ch%s_%s_%s_R24" % (nn, k, s), "Proposed"))
            stories.append(("ST_Ch%s_%s" % (nn, k), "ST_Ch%s_%s_R24" % (nn, k), "AC7_%s_Ch%s" % (k, nn), "Proposed"))
    tasks.append(("TK_SecLinks_Ch11_Verify_R", "TK_Ch11_Page_Verify_R24", "Proposed")); stories.append(("ST_Section_Links_Ch11", "ST_Ch11_Page_R24", "AC7R_SecLinks_Ch11", "Proposed"))
    tasks.append(("TK_Remedy_Regress_R", "TK_Template_9523_Verify", "Ready")); stories.append(("ST_Remedy_Regress_R", "ST_Template_9523", "AC8R_Regress", "Ready"))   # the regression is carried, restated on 9.52.3, as element (4) of AC9_Template
    for tk, sup, frm in tasks:
        i, j = T.blk(t, tk); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, tk
        assert ("ex:%s a backlog:ExecutionTask" % sup) in t, sup
        why = "Closed %s UTC by the change route of %s (v%s), decided by the lineage under %s: the task is superseded by %s, which carries the same work under the criterion restated on the measured standard of 2026-10-25; it is withdrawn, not Done, and it never started." % (now, CR, nxt, RULE, sup)
        nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
        assert "lastAuditedAt" not in nb
        nb = nb.replace("backlog:hasState backlog:Cancelled", 'backlog:hasState backlog:Cancelled ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
        t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("Wd24T_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " withdrawn"))
    for sid, sup, crit, frm in stories:
        i, j = T.blk(t, sid); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, sid
        assert ("ex:%s a backlog:Story" % sup) in t, sup
        for k in re.findall(r"ex:(TK_\w+)", re.search(r"backlog:decomposesInto ([^;]*);", b).group(1)):
            assert "backlog:hasState backlog:Cancelled" in t[T.blk(t, k)[0]:T.blk(t, k)[1]], (sid, k)
        why = "Closed %s UTC by the change route of %s (v%s), decided by the lineage under %s: the story is superseded by %s; it is withdrawn, not Done: its criterion ex:%s is NOT met and is NOT waived (it is restated as the criterion of %s with every earlier element kept and the owner's later rules added); it never started." % (now, CR, nxt, RULE, sup, crit, sup)
        nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why) + ' ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
        t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("Wd24T_" + sid, sid, "T_Withdraw" + frm, at, why, sid + " withdrawn"))
        L.append("ex:%s backlog:hasAuditNote %s .\n" % (crit, lit("Not met, not waived (%s): the story that carried this criterion is withdrawn by the change route of %s because it is superseded by %s." % (now[:10], CR, sup))))
    L.append("ex:Iter_21 rdfs:comment %s@en .\n" % lit("Every retrofit member of this planned iteration (20 stories, 40 tasks) and the section-link remainder of chapter 11 are withdrawn by the change route of %s on %s: none started, none Done; the work is planned in Iterations 24 to 28 under restated criteria. The iteration was planned and never started, no ceremony was held." % (CR, now[:10])))
    t3 = X.set_status(t + "\n" + "".join(L), "LS_InProgress")
    print(os.path.basename(M.write_new(src, t3, nxt, cur, "Iteration 21 retrofit items withdrawn by the change route of %s (22 stories and 42 tasks, none started, criteria restated as AC9_*, none waived)." % CR)))
if __name__ == "__main__": main()
