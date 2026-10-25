#!/usr/bin/env python3
"""sen0401_lineage_note12 v1_0_0 - states openly in the register the status of the delivered chapter 12 deck v2_0_0 against the corrected research (control of v0.354.0): one audit note on the criterion ex:AC9_Deck_Ch12 and on the story ex:ST_Ch12_Deck_R24; nothing edited, one new version."""
__version__ = "1.0.0"
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now()
n = ("Status stated %s UTC by the lineage agent: the criterion was controlled MET against the research v1_0_1 (v0.329.0) and that record stands. Against the CORRECTED research v1_1_0 (control v0.354.0) the delivered deck v2_0_0 fails the deck standard check D4 (28 of 40 concepts with an analogy, 70.0 percent) and D11 (30 of 40 concepts on slides, 75.0 percent, target 90); ten concepts are on no slide. "
     "The deck stays delivered and unchanged; its repair is the new deck version v3_0_0 of ex:ST_Deck12_Revise, which has its own criterion ex:AC9_Ch12DeckRevise." % now[:16])
t += "\nex:AC9_Deck_Ch12 backlog:hasAuditNote %s .\nex:ST_Ch12_Deck_R24 backlog:hasAuditNote %s .\n" % (lit(n), lit(n))
print(os.path.basename(M.write_new(src, X.set_status(t, "LS_InProgress"), nxt, cur, "Status of the delivered chapter 12 deck against the corrected research stated on its criterion and story (D4 70.0 percent, D11 75.0 percent).")))
