#!/usr/bin/env python3
"""sen0401_lineage_charset_close v1_0_0 - sets the disposition of ex:CR3_CharsetOtherPages (Pending) to Accepted in a NEW register version, with a dated comment of the measured fact that the request is fulfilled: the lineage agent ran the page charset check v1_0_0 on the newest page of each of the chapters 1 to 14 (log 08-tooling/verify/iter43_charset_all_pages) and all 14 pass (the tag lies within the first 1024 bytes, at byte 37). The rebuilds of the later stories (R24 pages and the repairs after them) did it; no page is rebuilt for this request. A defect fix, decided from the rules; the coordinator ordered such findings decided, not asked. Usage: no arguments."""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now()
t, k = re.subn(r'(ex:CR3_CharsetOtherPages a backlog:ChangeRequest ;.*?backlog:hasDisposition )backlog:Disp_Pending', lambda m: m.group(1) + "backlog:Disp_Accepted", t, count=1, flags=re.S); assert k == 1
t += '\nex:CR3_CharsetOtherPages rdfs:comment %s@en .\n' % C.lit("Disposition set to Accepted on %s by the lineage agent (a defect fix, decided from the rules). MEASURED: the page charset check v1_0_0 passes on the newest page of every chapter 1 to 14 (the meta charset tag lies at byte 37, within the first 1024 bytes; log 08-tooling/verify/iter43_charset_all_pages/charset_check_newest_pages_ch01_14.txt, 14 of 14 PASS). The request asked whether the other pages may be rebuilt on a template that fixes this; the later page stories already did, so nothing is rebuilt for it and the defect is gone from the delivered pages." % now[:10])
print(os.path.basename(M.write_new(src, t, nxt, cur, "ex:CR3_CharsetOtherPages Accepted: the charset defect is gone from the newest page of every chapter 1 to 14 (measured, 14 of 14 PASS).")))
