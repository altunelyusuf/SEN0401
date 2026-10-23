# Executor briefs of Iteration 20: chapters 7 and 8 (deck check, decks with manifests, pages) (generated from sen0401_slides_lineage_v0_238_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Start order (by ranking) | Task | Executor session | Can start | Ordering key (BP-D10: RICE score x dependency factor) |
|---|---|---|---|---|
| 1 | TK_Ch78_DeckCheck | SEN0401-I20-deckcheck | yes | 16.8 |
| 2 | TK_Ch07_Deck_Build | SEN0401-I20-deck-ch07 | yes | 1.2 |
| 3 | TK_Ch08_Deck_Build | SEN0401-I20-deck-ch08 | yes | 1.2 |
| 4 | TK_Ch07_Page_Build | SEN0401-I20-page-ch07 | no, after TK_Ch07_Deck_Verify | 0.48 |
| 5 | TK_Ch08_Page_Build | SEN0401-I20-page-ch08 | no, after TK_Ch08_Deck_Verify | 0.48 |
