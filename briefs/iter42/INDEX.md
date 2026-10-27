# Executor briefs of the retrofit (change request CR3_Retro24; generated from sen0401_slides_lineage_v0_557_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_SecLinks_Ch13_Build | SEN0401-I42-seclinks13 | yes | 0.4 |
| 2 | TK_Ch13_PageRebuild2_Build | SEN0401-I42-page-ch13c | no, after TK_SecLinks_Ch13_Verify | 0.2 |
