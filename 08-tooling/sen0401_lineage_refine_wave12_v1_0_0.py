#!/usr/bin/env python3
"""sen0401_lineage_refine_wave12 v1_0_0 - one new register version: control note on the Ch01 Teach deck and the 9 pt rule for all text on the Teach Build tasks of chapters 1 to 4. Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
CTRL = ("CONTROL 2026-11-01 of the report of the executor session SEN0401-I52-deck04 (commit 69c8a1d, deck v3_6_0, 79 slides), by the lineage agent, own runs: smallest text 9.0 pt over 1501 sized runs; the 45 code boxes and 21 result shapes of v3_5_0 are found unchanged; 0 prompts, 0 label words; lambdas only on slides 11, 46 and 54 and slide 10 says what a lambda is; notes 40 to 60 words, none empty; story slides 8, 35 and 72 each with a picture and a live link; concept table 87 concepts, none without a slide; deck check v1.2.0 under Python 3.14.6 21 examples 0 mismatches; chapter check v1_7_0 Deck/Ch04 PASS; deck standard v1_3_1 11 PASS and D5 NOT_MEASURED (not a pass); 5 native charts (D6 PASS). NOT recorded Done: slide 13 carries a NEW code example that is not a code box of the code deck: the shape named 'code head' holds the heading 'How a key is drawn, in two lines' and the two lines 'import secrets / k = secrets.randbelow(K.N - 1) + 1' stand in the card text shape 'secrets card text'; (1) a heading named 'code head' is read by the code marker as a code box (the page code match would look for the heading as a code line) and must be named otherwise; (2) the two lines are code that no check runs and the page will not carry: make them a real code box and result shape under the marker (for example the result '1 <= k < K.N' giving True, so the deck check re-runs it and the page manifest carries it) or remove the lines from the slide. REPAIR in a new deck version v3_7_0 under this task; then I control again. The criterion element (2) 'the code, shape names and results do not change' holds for all 45 old code boxes.")
i, j = T.blk(t, "TK_Ch04_DeckTeach_Build"); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(CTRL)
t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Control of the Ch04 Teach deck v3_6_0 recorded as a note (not Done: new untested code and a heading named code head on slide 13).")))
