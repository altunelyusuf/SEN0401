#!/usr/bin/env python3
"""sen0401_lineage_refine_wave5 v1_0_0 - one new register version: control note on the Ch01 Teach deck and the 9 pt rule for all text on the Teach Build tasks of chapters 1 to 4. Usage: no arguments."""
import os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_lineage_succession_v1_1_0 as M
import sen0401_lineage_succession3_v1_1_0 as X
import sen0401_lineage_template_revision_v1_0_0 as T
import sen0401_lineage_control_v1_0_0 as C
lit = C.lit; GATE = "/home/claude/Ontologies/backlog-roadmap-framework/03-tooling/backlog_execution_ready_v1_6_0.py"
src = M.newest(); t = open(src, encoding="utf-8").read(); nxt, cur = M.next_version(src); now = M.now(); L = []
NOTE = ("REQUIREMENT 2026-11-01 (lineage agent, from the owner's standing rule 'default text must not be small', measured on the newest decks): in the NEW deck of this task NO text run anywhere (notes aside) is below 9 pt, not only the result and code shapes; today's decks carry text below 9 pt: Ch01 v3_4_0 30 runs on slides 7, 9, 10, 14, 15, 17, 18, 26, 51, 75 (7.0, 7.5, 8.0 pt: the READ link boxes of the story slides and others), Ch02 v3_1_0 12 runs on 8 slides, Ch03 v3_1_0 10 runs on 6 slides, Ch05 v3_7_0 none, Ch06 v2_4_2 36 runs on 23 slides. Raise the size, widen or reflow the shape, never shorten the text, and report the smallest size of the whole deck as printed.")
CTRL = ("CONTROL 2026-11-01 of the report of the executor session SEN0401-I52-deck01 (commit 1507b80, deck v3_4_0, 76 slides), by the lineage agent, own runs: the earlier deck v3_3_0 equals its committed blob; slide count 62 -> 76; 31 code boxes and 15 result shapes identical in text; 0 prompts, 0 lambdas in code boxes, 0 five-N-one-K label words; code and result text 10 pt at the smallest; hyperlinks 26 -> 26; notes at most 56 words, none empty; the five story slides (7, 9, 10, 26, 51) each carry a picture and a live link; deck check v1.2.0 under Python 3.14.6 15 examples 0 mismatches; chapter check v1_6_0 and v1_7_0 Deck/Ch01 PASS; deck standard v1_3_1 11 PASS and D5 NOT_MEASURED (no story slide found by label words; not a pass); concept table 117 concepts, 0 without a slide (alias phrases are the executor's own and were not re-derived). NOT recorded Done: the deck carries 30 text runs below 9 pt (requirement above), and element (7) of the criterion has D5 NOT_MEASURED; the task stays InProgress for the size repair as a new deck version v3_5_0. The story layout probe, the page link check and the deck match were not run by the executor and belong to the page tasks.")
for tk in ("TK_Ch01_DeckTeach_Build",):
    i, j = T.blk(t, tk); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(CTRL)
    t = t[:i] + b + t[j:]
for tk in ("TK_Ch01_DeckTeach_Build", "TK_Ch02_DeckTeach_Build", "TK_Ch03_DeckTeach_Build", "TK_Ch04_DeckTeach_Build"):
    i, j = T.blk(t, tk); b = t[i:j].rstrip(); assert b.endswith(" ."); b = b[:-2] + ' ;\n    backlog:hasAuditNote %s .\n' % lit(NOTE)
    t = t[:i] + b + t[j:]
print(os.path.basename(M.write_new(src, X.set_status(t + "\n" + "".join(L), "LS_InProgress"), nxt, cur, "Control of the Ch01 Teach deck v3_4_0 recorded as a note (not Done: 30 runs below 9 pt, D5 NOT_MEASURED); the 9 pt rule for all text appended to the Teach Build tasks of chapters 1 to 4.")))
