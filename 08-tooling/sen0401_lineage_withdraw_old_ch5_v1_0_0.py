#!/usr/bin/env python3
"""sen0401_lineage_withdraw_old_ch5 v1_0_0 - closes the Suspended page task of chapter 5 of Iter_17 and its Proposed Verify task by the change route of ex:CR3_ChipScroll (T_WithdrawSuspended, T_WithdrawProposed -> Cancelled, with a rationale): the work they carried is carried by TK_Repair_Page_Ch05_Build and its Verify task. The story ST_Remedy_Page_Ch05 is NOT touched (open question for the owner)."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
for tk, via, frm, sup in [("TK_Remedy_Page_Ch05_Build", "T_WithdrawSuspended", "Suspended", "TK_Repair_Page_Ch05_Build"), ("TK_Remedy_Page_Ch05_Verify", "T_WithdrawProposed", "Proposed", "TK_Repair_Page_Ch05_Verify")]:
    i, j = T.blk(t, tk); b = t[i:j]; assert "backlog:hasState backlog:%s" % frm in b, tk
    why = "Closed %s UTC by the change route of ex:CR3_ChipScroll (v%s): the task is superseded by %s, which carries the rebuild of the chapter 5 page on template 9.52.1; it is withdrawn, not Done, and its earlier result (page 9.80.0 NOT MET on the story chip) stays in the register as history." % (now, nxt, sup)
    nb = b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled", 1)
    nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
    nb = re.sub(r'backlog:lastAuditedAt "[^"]*"', 'backlog:lastAuditedAt "%s"' % now, nb, count=1) if "lastAuditedAt" in nb else nb
    t = t[:i] + nb + t[j:]; L.append(C.transition("Wd30T_" + tk, tk, via, now, why, tk + " withdrawn"))
t2 = X.set_status(t + "\n" + "".join(L), "LS_InProgress"); print(os.path.basename(M.write_new(src, t2, nxt, cur, "Closed the Suspended chapter 5 page task of Iter_17 and its Verify task by the change route of ex:CR3_ChipScroll (withdrawn, superseded by the rebuild tasks of Iter_18).")))
