#!/usr/bin/env python3
"""sen0401_lineage_refine_wave2 v1_0_0 - one new register version: the Ch01 Teach story and Build task are made Ready (start gate READY first), and the suspended honesty Build task gets an appended audit note for the rework (honesty check v1_2_0, chapter check v1_7_0). Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
for x in ("ST_Ch01_DeckTeach", "TK_Ch01_DeckTeach_Build"):
    i, j = T.blk(t, x); b = t[i:j]; assert "backlog:hasState backlog:Proposed" in b, x
    t = t[:i] + b.replace("backlog:hasState backlog:Proposed", "backlog:hasState backlog:Ready", 1) + t[j:]
    if x.startswith("TK_"):
        open(src + ".gate.tmp", "w").write(t); r = subprocess.run([sys.executable, GATE, src + ".gate.tmp", "--lineage", "Lineage3", "--item", x], capture_output=True, text=True); os.remove(src + ".gate.tmp")
        assert "VERDICT     : READY" in r.stdout, x + " is not READY: " + r.stdout[-300:]
    L.append('ex:RefineW2_%s a backlog:RefinementEvent ; rdfs:label "Refinement that made %s ready"@en ;\n    backlog:refines ex:%s ; backlog:addressesConcern backlog:Concern_Data ; backlog:refinedAt "%s"^^xsd:dateTime ;\n    backlog:refinedBy backlog:Builder ; backlog:groomsForIteration ex:Iter_54 ;\n    backlog:hasRefinementOutcome %s .\n' % (x, x, x, now, lit("Refined by the lineage agent at %s UTC: the prerequisite deck (ST_Ch01_DeckCode) is Done and controlled; the start gate says READY; startable. The brief is generated from the register." % now)))
NOTE = ("REWORK 2026-11-01 (lineage agent, after the control of the first delivery, commit a3f9719, found element (2)(3)(4) NOT MET): the honesty check v1_1_0 knows only the caption 'run under Python 3.14.6', but the newest decks (Ch05 v3_7_0, Ch06 v2_4_2) caption their results 'What the run printed (python 3.14.6)'. Make NEW files (v1_1_0 stays as delivered): `sen0401_deck_honesty_check_v1_2_0.py` that accepts BOTH caption forms and refuses a stale one (a caption naming a Python version other than the one that ran), its fixtures `sen0401_deck_fixtures_v1_5_0.py` (stale_caption for both forms; every fixture agrees with its expected verdict, 0 wrong), and the chapter check successor `sen0401_lineage_chapter_check_v1_7_0.py` which differs from v1_6_0 only in calling honesty v1_2_0 and fixtures v1_5_0 (a disclosed scope extension of this task: the chapter check v1_6_0 would otherwise keep calling v1_1_0; no gate is edited, the old files stay). Run the new check on the Ch01 (d19e038), Ch05 v3_7_0 and Ch06 v2_4_2 decks and on one old prompt-containing deck (equal to the old check). Report every result as printed.")
i, j = T.blk(t, "TK_Code_Honesty_Build"); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(NOTE)
t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Ch01 Teach story and Build task made Ready; honesty Build task: rework note (honesty v1_2_0, chapter check v1_7_0) appended.")))
