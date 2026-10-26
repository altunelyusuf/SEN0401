#!/usr/bin/env python3
"""sen0401_lineage_correct_note_ch08page v1_0_0 - corrects one sentence of the control note of ex:AC9_Page_Ch08 (v0.460.0): the sentence 'Executor's own ... feature counts differ ... only in the order the tool prints them' was written without a measurement and is withdrawn. Measured: the control's runs give exactly the stored counts of the page 9.85.0 (127 widgets; 197 features for 9.37.0; 185 for 9.34.1 and 9.35.1; 6 gates; 0 skips). A committed register version is not edited; this is a new version. Usage: no arguments."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src)
n = "ex:AC9_Page_Ch08 backlog:hasAuditNote %s .\n" % C.lit("Correction %s (v%s) of the control note of v0.460.0: its last-but-one sentence, that the executor's feature counts differ from the stored numbers only in the order the tool prints them, was written without a measurement and is withdrawn. Measured by the control's own runs: 127 widgets, 197 features for 9.37.0 and 185 for 9.34.1 and 9.35.1, 6 gates, 0 skips, equal to the stored results of the page 9.85.0 (no difference of any kind). The element result is unchanged." % (M.now()[:10], nxt))
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + n, "LS_InProgress"), nxt, cur, "Correction of one unmeasured sentence in the control note of AC9_Page_Ch08.")))
