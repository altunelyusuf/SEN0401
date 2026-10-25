#!/usr/bin/env python3
"""sen0401_lineage_withdraw_ch14link v1_0_0 - withdraws ST_Deck14_StoryLink with its two tasks: the executor of the Build task (SEN0401-I36-deck-ch14link, begun 2026-10-25T16:49 UTC) STOPPED without committing, because the criterion ex:AC9_StoryLink_Ch14 element (2) (the arc check v1_3_0 still exits 0) is false for the delivered deck: the arc check v1_3_0 on chapter 14 refuses the notes of slides 22, 40 and 42 (5 sentences each). The lineage never measured the arc check on the chapter 14 deck before (no log of it exists in 08-tooling/arccheck_logs), and its brief wrongly said 'exits 0 as it did before': an error of the lineage agent, stated here.
The story is withdrawn (Cancelled), not Done; its criterion is not edited and not waived; a second story ST_Deck14_StoryLink2 whose criterion holds both the story link and the notes is admitted by the change route (ex:CR3_StoryLink2). Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
WHY = "the executor stopped without committing (nothing delivered): the criterion ex:AC9_StoryLink_Ch14 says the arc check v1_3_0 still exits 0, but on the delivered deck it refuses the notes of slides 22, 40 and 42 (5 sentences each, 52 to 54 words); the lineage had never measured the arc check on this deck and its brief wrongly said it exited 0 as before (an error of the lineage agent). A second story, ex:ST_Deck14_StoryLink2, whose criterion holds the story link and the notes, is admitted by the change route (ex:CR3_StoryLink2). The criterion is not edited and not waived"
for tk in ("TK_Deck14_StoryLink_Build", "TK_Deck14_StoryLink_Verify", "ST_Deck14_StoryLink"):
    i, j = T.blk(t, tk); b = t[i:j]; m = re.search(r"backlog:hasState backlog:(Proposed|Ready|InProgress)\b", b); assert m, tk; frm = m.group(1)
    why = "Closed %s UTC (v%s), decided by the lineage's own change route: %s. Withdrawn, not Done." % (now, nxt, WHY)
    nb = b.replace(m.group(0), "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why) + ' ; backlog:lastAuditedAt "%s"^^xsd:dateTime' % now, 1)
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("WdC14T_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " withdrawn"))
L.append("ex:AC9_StoryLink_Ch14 backlog:hasAuditNote %s .\n" % lit("Not carried (%s): its story is withdrawn, because element (2) is false for the delivered deck (the arc check refuses the notes of slides 22, 40 and 42); the criterion stands as written, not edited, not waived. Replaced by ex:AC9_StoryLink2_Ch14." % now[:10]))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Deck14_StoryLink withdrawn (the executor stopped without committing: the arc check refuses the notes of the delivered chapter 14 deck); replaced by ST_Deck14_StoryLink2.")))
