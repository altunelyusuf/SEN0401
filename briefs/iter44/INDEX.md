# Executor briefs of the retrofit (change request CR3_Retro24; generated from sen0401_slides_lineage_v0_605_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_DeckStd_Dark_Build | SEN0401-I44-deckstd | yes | None |
| 2 | TK_PageTest_Click_Build | SEN0401-I44-pagetest | yes | None |
| 3 | TK_Ch05_DeckDark_Build | SEN0401-I44-deck05dark | no, after TK_DeckStd_Dark_Verify | None |
| 4 | TK_Ch11_PageMeasure_Build | SEN0401-I44-page11 | no, after TK_PageTest_Click_Verify | None |
