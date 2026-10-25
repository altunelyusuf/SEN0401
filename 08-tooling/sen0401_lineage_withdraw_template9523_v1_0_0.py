#!/usr/bin/env python3
"""sen0401_lineage_withdraw_template9523 v1_0_0 - withdraws ST_Template_9523 with its Build (Suspended) and Verify (Proposed) tasks: the template 9.52.3 was delivered with an in-place edit of a committed file (element 5 not met, Suspended); its content is carried byte-identical by the template 9.52.4, which the lineage controlled Done (ST_Template_9524). Withdrawn (Cancelled), not Done; criteria not edited, not waived. Usage: no arguments; one new register version."""
__version__ = "1.0.0"
import os, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); L = []; now = M.now()
WHY = "superseded by the template 9.52.4 (ex:ST_Template_9524, controlled Done by the lineage): 9.52.3 was delivered with an in-place edit of a committed file, so its element 5 was not met; 9.52.4 is a new file of byte-identical content with the regression run by the lineage under the lock. Criteria not edited, not waived"
for tk in ("TK_Template_9523_Build", "TK_Template_9523_Verify", "ST_Template_9523"):
    i, j = T.blk(t, tk); b = t[i:j]; m = re.search(r"backlog:hasState backlog:(Proposed|Ready|InProgress|Suspended)\b", b); assert m, tk; frm = m.group(1)
    why = "Closed %s UTC (v%s), by the lineage's change route: %s. Withdrawn, not Done." % (now, nxt, WHY)
    nb = b.replace(m.group(0), "backlog:hasState backlog:Cancelled", 1)
    nb = re.sub(r'backlog:hasRationale "(?:[^"\\]|\\.)*"', lambda _: "backlog:hasRationale " + lit(why), nb, count=1) if "backlog:hasRationale" in nb else nb.replace("backlog:hasState backlog:Cancelled", "backlog:hasState backlog:Cancelled ; backlog:hasRationale " + lit(why), 1)
    nb = re.sub(r'backlog:lastAuditedAt "[^"]*"', 'backlog:lastAuditedAt "%s"' % now, nb, count=1) if "lastAuditedAt" in nb else nb
    t = t[:i] + nb + t[j:]; time.sleep(1.1); at = M.now(); L.append(C.transition("Wd9523_" + tk, tk, "T_Withdraw" + frm, at, why, tk + " withdrawn"))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "ST_Template_9523 and its tasks withdrawn, superseded by the Done template 9.52.4.")))
