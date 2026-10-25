#!/usr/bin/env python3
"""sen0401_lineage_withdraw_ch05fix v1_0_0 - withdraws ST_Ch05_DeckFix with its two tasks: the executor of the Build task (SEN0401-I33-deck-ch05fix, begun 2026-10-25T16:33 UTC) STOPPED without committing, because the criterion ex:AC9_Ch05DeckFix element (1) (the arc check v1_3_0 on chapter 5 prints no refusal) cannot be met without breaking the deck standard element D9 or declaring a false background in the plan; and the brief ordered the summary before the check yourself slide, which the arc check refuses.
The story is withdrawn (Cancelled), not Done; its criterion is not edited and not waived; a second story ST_Ch05_DeckFix2 with a criterion that names the contradiction is admitted by the change route (ex:CR3_Ch05DeckFix2). Pattern of sen0401_lineage_withdraw_arcfix12. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
WHY = "the executor stopped without committing (nothing delivered): the criterion ex:AC9_Ch05DeckFix cannot be met as written, because the arc check v1_3_0 rule 1 (dark closing slide) contradicts the deck standard element D9 (one background scheme), and the brief ordered the summary slide before the check yourself slide, which the arc check refuses. A second story, ex:ST_Ch05_DeckFix2, with a criterion that names the contradiction, is admitted by the change route (ex:CR3_Ch05DeckFix2). The criterion is not edited and not waived"
for tk in ("TK_Ch05_DeckFix_Build", "TK_Ch05_DeckFix_Verify", "ST_Ch05_DeckFix"):
    i, j = T.blk(t, tk); b = t[i:j]; m = re.search(r"backlog:hasState backlog:(Proposed|Ready|InProgress)\b", b); assert m, tk; frm = m.group(1)
    why = "Closed %s UTC (v%s), decided by the lineage's own change route: %s. Withdrawn, not Done." % (now, nxt, WHY)
    nb = b.replace(m.group(0), "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why) + ' ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("WdC5T_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " withdrawn"))
L.append("ex:AC9_Ch05DeckFix backlog:hasAuditNote %s .\n" % lit("Not carried (%s): its story is withdrawn, because element (1) cannot be met without breaking D9 or declaring a false background; the criterion stands as written, not edited, not waived. Replaced by ex:AC9_Ch05DeckFix2." % now[:10]))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Ch05_DeckFix withdrawn (the executor stopped without committing: its criterion contradicts the deck standard D9); replaced by ST_Ch05_DeckFix2.")))
