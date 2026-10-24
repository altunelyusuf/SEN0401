#!/usr/bin/env python3
"""sen0401_lineage_rep20_withdraw v1_0_0 - closes the superseded tasks by the change route of ex:CR3_Repair20 (T_WithdrawSuspended, T_WithdrawProposed -> Cancelled, with a rationale), as sen0401_lineage_withdraw_old_ch5 did for ex:CR3_ChipScroll:
TK_Ch07_Deck_Build (Suspended) and TK_Ch07_Deck_Verify (Proposed) are superseded by TK_Ch07_Deck_Reissue and its Verify task; TK_SecLinks_Ch11_Page (Suspended) and TK_SecLinks_Ch11_Verify (Proposed) are superseded by TK_Ch11_Page_Build of Iteration 21 and TK_SecLinks_Ch11_Verify_R.
The stories ST_Ch07_Deck (its criterion stays unmet and unchanged) and ST_Section_Links are NOT touched here."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
W = [("TK_Ch07_Deck_Build", "T_WithdrawSuspended", "Suspended", "TK_Ch07_Deck_Reissue", "which re-issues the deck of chapter 7 as v2_1_0 in new files", "its result (deck v2_0_0: element (4) not met, the commit 27d36a5 edited files of ed03d15) stays in the register as history"),
     ("TK_Ch07_Deck_Verify", "T_WithdrawProposed", "Proposed", "TK_Ch07_Deck_Reissue_Verify", "which verifies the re-issued deck", "it never started"),
     ("TK_SecLinks_Ch11_Page", "T_WithdrawSuspended", "Suspended", "TK_Ch11_Page_Build", "of Iteration 21, which rebuilds the page of chapter 11 on template 9.52.2 with the section-link ERD", "its result (page 9.78.0 failing the page tests, suspended since 2026-10-22) stays in the register as history"),
     ("TK_SecLinks_Ch11_Verify", "T_WithdrawProposed", "Proposed", "TK_SecLinks_Ch11_Verify_R", "which verifies the section links and the ERD labels on that page", "it never started")]
for tk, via, frm, sup, what, hist in W:
    i, j = T.blk(t, tk); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, tk
    why = "Closed %s UTC by the change route of ex:CR3_Repair20 (v%s): the task is superseded by %s, %s; it is withdrawn, not Done, and %s." % (now, nxt, sup, what, hist)
    nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled", 1)
    nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
    nb = re.sub(r'backlog:lastAuditedAt "[^"]*"', 'backlog:lastAuditedAt "%s"' % now, nb, count=1) if "lastAuditedAt" in nb else nb
    t = t[:i] + nb + t[j:]; L.append(C.transition("Wd45T_" + tk, tk, via, now, why, tk + " withdrawn"))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, "Closed the superseded tasks of the deck of chapter 7 and of the section links of chapter 11 by the change route of ex:CR3_Repair20 (withdrawn, superseded by the repair tasks).")))
