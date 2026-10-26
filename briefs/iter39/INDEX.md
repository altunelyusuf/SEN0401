# Executor briefs of the retrofit (change request CR3_Retro24; generated from sen0401_slides_lineage_v0_508_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_Template_9525_Build | SEN0401-I39-template9525 | yes | 5.6 |
| 2 | TK_Ch11_PageRebuild_Build | SEN0401-I39-page-ch11b | no, after TK_Template_9525_Verify | 0.2 |
