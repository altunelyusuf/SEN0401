# Executor briefs of Iteration 17: the chapter 5 and 6 remedy (generated from sen0401_slides_lineage_v0_195_0.ttl)

The Verify and Regress tasks have no executor: the builder session controls them and runs the evidence bridge after the executors report.

| Task | Executor session | Can start |
|---|---|---|
| TK_Remedy_DeckCheck | SEN0401-I17-deckcheck | yes |
| TK_Remedy_PageTest | SEN0401-I17-pagetest | yes |
| TK_Remedy_Template | SEN0401-I17-template | yes |
| TK_Remedy_Deck_Ch05_Build | SEN0401-I17-deck-ch05 | yes |
| TK_Remedy_Deck_Ch06_Build | SEN0401-I17-deck-ch06 | yes |
| TK_Remedy_Page_Ch05_Build | SEN0401-I17-page-ch05 | no, after TK_Remedy_Template, TK_Remedy_PageTest, TK_Remedy_Deck_Ch05_Verify |
| TK_Remedy_Page_Ch06_Build | SEN0401-I17-page-ch06 | no, after TK_Remedy_Template, TK_Remedy_PageTest, TK_Remedy_Deck_Ch06_Verify |
