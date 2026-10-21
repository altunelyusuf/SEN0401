# Stage 4 status (page ABox of chapters 8-14 and the numbers page), 2026-10-20

Method: 08-tooling/sen0401_page_abox_build_v2_0_0.py writes the page ABox from the chapter's page data, objectives, quiz and the stored browser-test result (page test 9.35.0 on the newest page); 08-tooling/sen0401_stage4_gates_v1_0_0.py runs RDODI's newest pipeline validator (1.13.0) unchanged on it. No gate, check, test or threshold was edited.
Standing gaps, same for every chapter: Stage4.L, Cross.C and Stage1.C/E are NOT_MEASURED (the research files carry no concept inventory); Cross.B is CANNOT_RUN (the Stage 3 documents record a section's concept in dcterms:source, not prov:wasDerivedFrom, so no page region can chain through them); Stage4.B reports 3 advisory warnings.

## Chapter 8 - achieved
Page ABox 03-materials/ch08/page/sen0401_ch08_page_abox_v2_0_0.ttl for page 9.51.0 (109 sections, 109 widgets all design-tested, 6 objectives, 12 questions). Stage4.A, B, cov (233 individuals), sub (233), src (233) PASS. Research/Ch08, Deck/Ch08, Page/Ch08 chapter checks PASS. Gate output: 08-tooling/ch08-page/stage4_gates_v2_0_0.txt.
Not achieved: Stage3.F fails on the chapter's Stage 3 document (45 dangling citations); this is a Stage 3 matter that exists without the page ABox and is not changed here.

## Chapter 9 - achieved
Page ABox 03-materials/ch09/page/sen0401_ch09_page_abox_v2_0_0.ttl for page 9.68.0 (96 sections, 96 widgets all design-tested, 6 objectives, 13 questions). Stage4.A, B, cov (207 individuals), sub (207), src (207) PASS; Stage3.F PASS. Research/Ch09, Deck/Ch09, Page/Ch09 chapter checks PASS. Gate output: 08-tooling/ch09-page/stage4_gates_v2_0_0.txt.

## Chapter 10 - achieved
Page ABox 03-materials/ch10/page/sen0401_ch10_page_abox_v2_0_0.ttl for page 9.53.0 (86 sections, 86 widgets all design-tested, 6 objectives, 12 questions). Stage4.A, B, cov (187 individuals), sub (187), src (187) PASS; Stage3.F PASS. Research/Ch10, Deck/Ch10, Page/Ch10 chapter checks PASS. Gate output: 08-tooling/ch10-page/stage4_gates_v2_0_0.txt.

## Chapter 11 - achieved
Page ABox 03-materials/ch11/page/sen0401_ch11_page_abox_v2_0_0.ttl for page 9.54.0 (91 sections, 91 widgets all design-tested, 6 objectives, 10 questions). Stage4.A, B, cov (197 individuals), sub (197), src (197) PASS; Stage3.F PASS. Research/Ch11, Deck/Ch11, Page/Ch11 chapter checks PASS. Gate output: 08-tooling/ch11-page/stage4_gates_v2_0_0.txt.

## Chapter 12 - achieved
Page ABox 03-materials/ch12/page/sen0401_ch12_page_abox_v2_0_0.ttl for page 9.55.0 (86 sections, 86 widgets all design-tested, 6 objectives, 10 questions). Stage4.A, B, cov (187 individuals), sub (187), src (187) PASS; Stage3.F PASS. Research/Ch12, Deck/Ch12, Page/Ch12 chapter checks PASS. Gate output: 08-tooling/ch12-page/stage4_gates_v2_0_0.txt.

## Chapter 13 - achieved
Page ABox 03-materials/ch13/page/sen0401_ch13_page_abox_v2_0_0.ttl for page 9.69.0 (84 sections, 84 widgets all design-tested, 6 objectives, 10 questions). Stage4.A, B, cov (183 individuals), sub (183), src (183) PASS; Stage3.F PASS. Research/Ch13, Deck/Ch13, Page/Ch13 chapter checks PASS. Gate output: 08-tooling/ch13-page/stage4_gates_v2_0_0.txt.
Note: the first browser-test run of page 14 was killed by the machine's memory limit (playwright driver, 4 GB) after 127 checks; a rerun alone passed 370/0. No test was changed.

## Chapter 14 - achieved
Page ABox 03-materials/ch14/page/sen0401_ch14_page_abox_v2_0_0.ttl for page 9.57.0 (68 sections, 68 widgets all design-tested, 6 objectives, 9 questions). Stage4.A, B, cov (151 individuals), sub (151), src (151) PASS; Stage3.F PASS. Research/Ch14, Deck/Ch14, Page/Ch14 chapter checks PASS. Gate output: 08-tooling/ch14-page/stage4_gates_v2_0_0.txt.

## Chapter 1 - Stage 3.F achieved (2026-10-20)
Stage 3 document v1.2.1 (commit 3e664d2): the root section cites P01 (Antonopoulos and Harding, 2023); Stage3.F PASS (30 citations), Stage 1-3 gates and the 351 corpus claims pass, Deck/Ch01 PASS.
Not achieved: the chapter 1 Stage 4 page ABox (Stage4.cov, sub fail on the old label-only v9_4_2 ABox; another agent builds it). The Research/Ch01 chapter check cannot complete because chapter 1 has no verify script.

## Numbers page (Bitcoin in numbers, supplement to chapters 1 and 2) - achieved
Stage 3.F: research v1.1.0 (the labels of the held Blockchain.com chart sources P02-P04 now carry (Blockchain.com, 2026); the three endpoints were re-fetched on 2026-10-20 and saved with SHA-256 in 08-tooling/numbers-evidence, and the price of 2026-08-26 and the hash rate of 2026-08-28 equal research finding F2). 19 dangling citations -> 0.
Stage 4: builder 08-tooling/sen0401_page_abox_build_v2_1_0.py (new version: accepts 'numbers', truthful sentences for the stored results 'chart drawn' and 'second step revealed'; chapters 8 and 14 rebuilt with it are byte-identical to the committed v2.0.0 output). Page ABox 03-materials/numbers/page/sen0401_numbers_page_abox_v9_4_3.ttl for page 9.4.2 (23 sections, 23 widgets all design-tested, 4 objectives, 5 questions); it is numbered 9.4.3 because the older label-only ABox v9_4_2 stays committed and the gate reads the newest file by version. Stage4.A, B, cov (59 individuals), sub (59), src (59) PASS; Stage3.F PASS. Gate output: 08-tooling/numbers-page/stage4_gates_v2_1_0.txt.
There is no chapter check (Research/Deck/Page) for the numbers page. The stored browser-test result is the one committed with the page (page test 9.4.2, 23/23 widgets passed); it was not re-run.

## Chapter 2 - achieved
Page ABox 03-materials/ch02/page/sen0401_ch02_page_abox_v9_71_0.ttl for page 9.71.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 101 sections, 101 widgets (82 run in the browser, 0 recorded, 103 marked tested), 5 questions, 4 objectives. Stage4.A, B, cov (215 individuals), sub (215), src (215) PASS; Stage3.F PASS. Research/Ch02, Deck/Ch02, Page/Ch02 chapter checks PASS. Gate output: 08-tooling/ch02-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch02-page/test_results_abox_v9_71_0.json.

## Chapter 3 - achieved
Page ABox 03-materials/ch03/page/sen0401_ch03_page_abox_v9_72_0.ttl for page 9.72.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 115 sections, 115 widgets (87 run in the browser, 3 recorded, 117 marked tested), 7 questions, 4 objectives. Stage4.A, B, cov (243 individuals), sub (243), src (243) PASS; Stage3.F PASS. Research/Ch03, Deck/Ch03, Page/Ch03 chapter checks PASS. Gate output: 08-tooling/ch03-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch03-page/test_results_abox_v9_72_0.json.

## Chapter 4 - achieved
Page ABox 03-materials/ch04/page/sen0401_ch04_page_abox_v9_73_0.ttl for page 9.73.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 87 sections, 87 widgets (68 run in the browser, 1 recorded, 90 marked tested), 7 questions, 4 objectives. Stage4.A, B, cov (187 individuals), sub (187), src (187) PASS; Stage3.F PASS. Research/Ch04, Deck/Ch04, Page/Ch04 chapter checks PASS. Gate output: 08-tooling/ch04-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch04-page/test_results_abox_v9_73_0.json.

## Chapter 5 - achieved
Page ABox 03-materials/ch05/page/sen0401_ch05_page_abox_v9_74_0.ttl for page 9.74.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 111 sections, 111 widgets (76 run in the browser, 9 recorded, 113 marked tested), 8 questions, 5 objectives. Stage4.A, B, cov (236 individuals), sub (236), src (236) PASS. Research/Ch05, Deck/Ch05, Page/Ch05 chapter checks PASS. Gate output: 08-tooling/ch05-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch05-page/test_results_abox_v9_74_0.json. Stage3.F (2026-10-21): research v1.1.1 (commit 76d6083); the 15 dangling citations all cited (Lightning Labs, 2026a/2026b); the held lnd sources P20/P21 were in the research file but their labels held '2026a'/'2026b', which the validator v1.13.0 does not read as a year; labels now also state the retrieval date 2026-10-04; sources re-fetched, SHA-256 equal to the saved copies (08-tooling/ch05-evidence/lnd_sources_sha256_2026-10-21.txt). Stage3.F PASS (36 citations), Stage4.A/B/cov/sub/src PASS; document and page ABox unchanged. Gate output: 08-tooling/ch05-page/stage4_gates_v1_1_0_after_research_v1_1_1.txt.

## Chapter 6 - achieved
Page ABox 03-materials/ch06/page/sen0401_ch06_page_abox_v9_75_0.ttl for page 9.75.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 115 sections, 115 widgets (85 run in the browser, 0 recorded, 121 marked tested), 8 questions, 5 objectives. Stage4.A, B, cov (244 individuals), sub (244), src (244) PASS; Stage3.F PASS. Research/Ch06, Deck/Ch06, Page/Ch06 chapter checks PASS. Gate output: 08-tooling/ch06-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch06-page/test_results_abox_v9_75_0.json.

## Chapter 7 - achieved
Page ABox 03-materials/ch07/page/sen0401_ch07_page_abox_v9_76_0.ttl for page 9.76.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 83 sections, 83 widgets (55 run in the browser, 0 recorded, 89 marked tested), 10 questions, 6 objectives. Stage4.A, B, cov (181 individuals), sub (181), src (181) PASS; Stage3.F PASS. Research/Ch07, Deck/Ch07, Page/Ch07 chapter checks PASS. Gate output: 08-tooling/ch07-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch07-page/test_results_abox_v9_76_0.json.

## Chapter 1 - achieved
Page ABox 03-materials/ch01/page/sen0401_ch01_page_abox_v9_70_0.ttl for page 9.70.0 (builder 2.1.0 with the ABox version set to the page version, because the older ABox v9_4_x is named by a higher version number and the gates read the newest). 117 sections, 117 widgets (42 run in the browser, 48 recorded, 122 marked tested), 5 questions, 4 objectives. Stage4.A, B, cov (247 individuals), sub (247), src (247) PASS; Stage3.F PASS. Deck/Ch01, Page/Ch01 chapter checks PASS; Research/Ch01 cannot complete (chapter 1 has no verify script, so the chapter check stops at that step; its Stage 1-3 gates PASS and 351 corpus claims execute with no failure). Gate output: 08-tooling/ch01-page/stage4_gates_v1_1_0.txt. Browser test 9.35.0 run alone on the page: result stored in 08-tooling/ch01-page/test_results_abox_v9_70_0.json.

## Chapter 8 - achieved (page 9.77.0, research 1.2.0)
Page ABox 03-materials/ch08/page/sen0401_ch08_page_abox_v9_77_0.ttl for page 9.77.0 (127 sections, 127 widgets (63 run in the browser, 34 recorded, 127 marked tested), 12 questions, 6 objectives). Stage3.F, Stage4.A, B, cov (269 individuals), sub (269), src (269) PASS. Research/Ch08, Deck/Ch08, Page/Ch08 chapter checks PASS. Gate output: 08-tooling/ch08-page/stage4_gates_v1_1_0.txt.
