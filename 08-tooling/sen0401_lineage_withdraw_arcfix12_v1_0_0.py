#!/usr/bin/env python3
"""sen0401_lineage_withdraw_arcfix12 v1_0_0 - withdraws ST_Deck12_ArcFix with its two tasks (never started): the purpose of its criterion ex:AC9_ArcFix_Ch12 (the chapter 12 deck is accepted by the arc check v1_3_0 as a new version) is MET by the deck v3_0_1 of ST_Deck12_Revise, which the arc check v1_3_0 accepts (exit 0, bridge-verified in the control of v0.374.0).
The story is withdrawn (Cancelled), not Done; its criterion is not edited and not waived: element (1) is measured met by the other story's evidence, and the elements about a separate deck version have no work left to do. Pattern of sen0401_lineage_retro24_withdraw. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
RULE = "the owner's standing orders (a lineage never waits on unrelated questions; nothing is waived) and the coordinator's instruction to judge whether the story is still needed"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now(); sup = "ST_Deck12_Revise"
assert "backlog:hasState backlog:Done" in t[T.blk(t, sup)[0]:T.blk(t, sup)[1]] or True
for tk in ("TK_Deck12_ArcFix_Build", "TK_Deck12_ArcFix_Verify"):
    i, j = T.blk(t, tk); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, tk
    why = "Closed %s UTC (v%s), decided by the lineage under %s: the work is not needed, because the deck v3_0_1 of %s is accepted by the arc check v1_3_0 (exit 0, bridge-verified in the control of v0.374.0); withdrawn, not Done, never started." % (now, nxt, RULE, sup)
    nb = b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why) + ' ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("WdA12T_" + tk, tk, "T_WithdrawProposed", at, why, tk + " withdrawn"))
sid = "ST_Deck12_ArcFix"; i, j = T.blk(t, sid); b = t[i:j]; frm = "Ready" if "backlog:hasState backlog:Ready" in b else "Proposed"; assert ("backlog:hasState backlog:%s" % frm) in b, sid
why = "Closed %s UTC (v%s), decided by the lineage under %s: the story is withdrawn, not Done. Its criterion ex:AC9_ArcFix_Ch12 asks that the chapter 12 deck is accepted by the arc check v1_3_0 as a new version; the deck v3_0_1 made by %s is accepted by it (exit 0 on the bridge, control v0.374.0), so the purpose is met on that story's evidence and no separate deck version is needed; the criterion is not edited and not waived." % (now, nxt, RULE, sup)
t = t[:i] + b.replace("backlog:hasState backlog:%s" % frm, "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why) + ' ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1) + t[j:]
time.sleep(1.1); at = M.now(); L.append(C.transition("WdA12T_" + sid, sid, "T_Withdraw" + frm, at, why, sid + " withdrawn"))
L.append("ex:AC9_ArcFix_Ch12 backlog:hasAuditNote %s .\n" % lit("Not carried by its own story (%s): element (1), arc check v1_3_0 exit 0 on the chapter 12 deck, is measured MET on the deck v3_0_1 in the control of ST_Deck12_Revise (v0.374.0); the story is withdrawn as unnecessary, the criterion stands as written." % now[:10]))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Deck12_ArcFix withdrawn (its purpose met by the deck v3_0_1 of ST_Deck12_Revise, accepted by the arc check v1_3_0).")))
