# Executor briefs of the retrofit (change request CR3_Retro24; generated from sen0401_slides_lineage_v0_281_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_Template_9523_Build | SEN0401-I24-template | yes | 13.44 |
| 2 | TK_Ch01_Deck_Build_R24 | SEN0401-I24-deck-ch01 | yes | 0.8 |
| 3 | TK_Ch02_Deck_Build_R24 | SEN0401-I24-deck-ch02 | yes | 0.8 |
| 4 | TK_Ch03_Deck_Build_R24 | SEN0401-I24-deck-ch03 | yes | 0.8 |

Start the first three at once (at most three executors): SEN0401-I24-template, SEN0401-I24-deck-ch01, SEN0401-I24-deck-ch02. Start SEN0401-I24-deck-ch03 when one of them reports done. Then tell the lineage agent the real start instant of each so that work begun is recorded (tool sen0401_lineage_work_begun_v1_13_0.py TASK...).
Later briefs (the pages of Iterations 25 to 28 wait for TK_Template_9523_Verify and their deck Verify) are generated from the register when their tasks are startable: sen0401_lineage_brief_remedy_v1_7_0.py TASK[,TASK...] 08-tooling/briefs/iterNN.
