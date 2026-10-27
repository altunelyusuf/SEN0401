# Executor briefs of the retrofit (change request CR3_Retro24; generated from sen0401_slides_lineage_v0_529_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_Deck13_Ex12_Build | SEN0401-I40-deck13fix | yes | 0.53 |
| 2 | TK_Ch13_PageRebuild_Build | SEN0401-I40-page-ch13b | no, after TK_Deck13_Ex12_Verify | 0.2 |
