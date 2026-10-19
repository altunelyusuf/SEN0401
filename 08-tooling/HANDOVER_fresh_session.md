# SEN0401 handover for a fresh session (2026-10-19)

Start: run the ceremony (`OE_TARGET_REPO=altunelyusuf/Ontologies bash repo-tooling/oe_ceremony_v1_0_6.sh` in /home/claude/Ontologies), read the OE and lineage discipline files; trust no summary.

## State
- Register head: v0.113 (e177fe1), CONFORMANT; pipeline_verify passes per lineage (Lineage, Lineage2, Lineage3); order check passes.
- All 45 stories Done. EP_Deck, EP_Page, EP_Research, Init_Slides Proposed (child work open).
- 11 tasks not Done (executor Executor_ClaudeCodeSession): TK_Deck_Ch14_StaleFixtures (In Progress); TK_Research_Ch02/03/04_Stage3F (Ready); TK_Research_Ch08..Ch14_Stage4 (Ready).
- Decks 1-14 pass the nine checks. Pages 1-7 are 9.70.0-9.76.0 on template 9.51.0; pages 8-14 are on older templates (counts unchanged on 9.51.0 regression, not rebuilt).

## Known disclosures
- Page 8 fails test 9.34.0 (113 pass, 1 fail, then crash); 9.35.0 passes. Test not changed.
- Page tests use the test key only.
- pages_link_verify still compares against old deck link registers for ch1-6 (superseded entries reported as not carried).
- Stand-in pictures (Bitcoin logo, Mt. Gox logo, Satoshi bust); PayPal S-1 403 with Wikipedia substitute; ch3 date source discrepancy; census median-fee gap.

## Open for the owner
- Chapter 1 picture credit for genesis_hexdump.png ("the course's own CC BY 4.0").
- Latest pages (1-7 rebuilds, ch6/9/13) and decks are not yet re-packaged as zips.

## Rules
Lineage requirements are never bypassed, waived or deferred; no digest re-recording without a sanctioned route; lineage questions go to BRSF; no sleep-and-wake; status reports short.
