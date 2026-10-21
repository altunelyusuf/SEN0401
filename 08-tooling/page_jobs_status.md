# Page jobs status (SEN0401), 2026-10-19

Chapter 13 page 9.69.0 (template 9.51.0, page data 2.22.0)
- Verified: 9.34.0 368 pass, 0 fail; 9.35.0 368 pass, 0 fail. Link register 15 of 15. 84 concepts, 51 examples run in the browser, 11 Recorded. Check "code questions change the chapter's numbers": met (14 varied questions, 21 examples can be varied). Written question bank now 84 of 84 (inputs_make_v1_1_0.py; question maker unchanged).
- Open: template 9.51.0 not yet run on the latest pages of chapters 1-5 and 7-14 (counts must not change); that run was interrupted by a restart.

Chapter 9 page 9.68.0 (template 9.51.0): committed. 9.34.0 370 pass, 0 fail; 9.35.0 370 pass, 0 fail. 64 of 69 examples run in the browser, 5 Recorded (each reads a saved file without a clear redistribution licence). The page carries the course's own census (mainnet_fee_census_v2_0_0.json, CC BY 4.0, 20 blocks, cross-checked against blockstream.info: 20 of 20 blocks, 1236 of 1236 transactions equal); the old third-party census is no longer carried. bolt03 is stated as CC BY 4.0 in ASSETS_PROVENANCE_v1_5_0.md and the wheel carries the file; the page text has no CC0 wording. Note: the median fee computed by the course (205 and 0 sat/vB) differs from mempool.space's page figure (200 and 1); both are stored in the census file.
Chapter 6 page 9.67.0 (template 9.51.0, page data 2.22.0 with the content pinned to 9.63.0's): committed. Content identical to 9.63.0 (page data equal except the version; same widgets, same examples run and Recorded, 374 pass for both tests as before). Five runs each of 9.34.0 and 9.35.0: 10 of 10 pass, 374 pass, 0 fail. Load task median (ms), before on 9.63.0: 248, 216, 209, 234, 196, 169, 181, 189, 206, 195; after on 9.67.0: 104, 95, 110, 107, 129, 102, 102, 97, 108, 105. Link register 13 of 13.

Chapter 01 page 9.70.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_3_0.json): 9.34.0 372 pass, 0 fail; 9.35.0 372 pass, 0 fail.

Chapter 02 page 9.71.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_3_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Chapter 03 page 9.72.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_3_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Chapter 04 page 9.73.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_3_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Chapter 05 page 9.74.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_2_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Chapter 06 page 9.75.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_2_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Chapter 07 page 9.76.0 (template 9.51.0, rebuilt from the corrected deck's lecture export lecture_v1_2_0.json): 9.34.0 374 pass, 0 fail; 9.35.0 374 pass, 0 fail.

Template 9.51.0 regression, 9.34.0 and 9.35.0 on the latest committed pages with the 9.51.0 changes put in place of 9.50.0's text (no page replaced). Counts equal the committed ones for every page: ch01 372/0 and 372/0; ch02 374/0; ch03 374/0; ch04 374/0 (these four also as rebuilt pages above); ch05 374/0 both; ch07 374/0 both; ch08 9.34.0 113 pass and 1 fail (the known blank-question check), 9.35.0 370/0; ch10 368/0 both; ch11 9.35.0 368/0, 9.34.0 first run 366 pass and 2 fail (the main-thread budget: 304 ms after load over 3 long tasks while the load task was 85 ms against 115 shipped), rerun 368/0; ch12 370/0 both; ch14 370/0 both. No difference in counts.
Chapters 1 to 7 rebuilt from the corrected decks' exports: pages 9.70.0 to 9.76.0 (ch01 to ch07), each 9.34.0 and 9.35.0 clean (ch01 372; ch02 to ch07 374). The old deck link registers (link_register_v1_0_0.json, dated 2026-10-16) predate the corrections, so pages_link_verify reports their superseded entries as not carried: ch01 8 (four READ cards and four resources rows the deck replaced), ch02 1, ch03 1, ch04 1, ch05 3, ch06 1, ch07 0; pages_deck_match_verify_v1_0_0.py, which compares with the corrected exports and stories, reports 0 not carried on every page.

Chapter 08 page 9.77.0 (template 9.51.0, page data 2.22.0, research 1.2.0 with 18 new worked examples with changeable whole numbers): 9.34.0 370 pass, 0 fail, no crash (the 7th run; runs 1 to 6 failed only the main-thread budget check, 'after load' 219 to 922 ms, while other executors ran page tests in parallel, or lost the browser to an out-of-memory kill; logs kept in ch08-evidence); 9.35.0 370 pass, 0 fail. Page/Ch08 chapter check PASS (run with the venv314 interpreter). 127 concepts, 63 examples run in the browser, 34 Recorded. Deck unchanged (pages_deck_match_verify: 0 not carried).

Chapter 11 page 9.77.0 (template 9.51.0, rebuilt from lecture export lecture_v1_1_0.json and stories 1.2.0): 9.34.0 368 pass, 0 fail, 91 widgets, 184 features, 6 gates, 2 skipped; 9.35.0 368 pass, 0 fail, same counts (the ERD label features are skipped for this chapter: its research states no relationship between two sections); Page/Ch11 chapter check PASS on the third run (run 1 browser target crashed, run 2 main-thread budget under contention); logs in 08-tooling/ch11-evidence.
