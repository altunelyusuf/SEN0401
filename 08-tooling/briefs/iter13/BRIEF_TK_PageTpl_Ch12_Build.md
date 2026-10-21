# Brief for the executor session SEN0401-I13-page-ch12

Generated from the register sen0401_slides_lineage_v0_150_0.ttl. Task TK_PageTpl_Ch12_Build (state in the register: Ready).
Executor session name: **SEN0401-I13-page-ch12**. The register's note on 'work begun' for this task names this session.

## Rules of an executor
- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The builder session writes it; it records your start and runs the Verify task through the evidence bridge after you report.
- A committed file is never edited: every output is a new file with a new version number.
- No gate, test or threshold is changed (Stage 3.F, the Stage 4 gates, the chapter checks, the page tests 9.34.0 and 9.35.0, the deck match check); no citation or claim is removed only to make a check pass.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN. NOT_MEASURED and CANNOT_RUN are not passes. A page test with a TEST release key proves page logic only.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a test or a gate; the deck would have to change (state exactly what and why); a check fails and you cannot fix it by building the page or research again; or anything in this brief contradicts the repository.
- Commit your work to main with a clear message (no force push; pull --rebase before push). Do not wait for or ask for approvals nobody can give: tell the coordinator the exact command.
- If a container restart interrupts you, the repository (committed and pushed work) is the only record: commit each verified step at once.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran (the Stage 4 runner for the chapter, the chapter checks, the page tests, the deck match check, the template markers); say what failed, if anything.

## The task
**Rebuild the page of chapter 12 on the current template**

Build the page of chapter 12 as a new file with a new page version, on the page template 9.51.0, with the page builder that produced the pages of chapters 1 to 7, 9 and 13, from the chapter's existing page data, the deck's lecture export and stories (same content), and its stored objectives and quiz; run the page tests 9.34.0 and 9.35.0 unchanged and store the result; build the Stage 4 page ABox from the new page with the Stage 4 builder (a new file). A committed file is not edited. No test, gate or threshold is changed. Satisfies the criterion ex:AC3T_Ch12. Status correction 2026-10-21 (G113): the In Progress state of v0.146 (2026-10-21T07:05:34 UTC) was a status without work, a coordination error of the builder session; the item is Ready again by the recorded return ex:Return3T_TK_PageTpl_Ch12_Build; the start is recorded only at the real start of an executor inside a started sprint.

Depends on: nothing

## The story it belongs to
**The pages of chapters 8, 10, 11, 12 and 14 are rebuilt on the current page template and meet the written standard**

As a SEN0401 instructor I want the pages of chapters 8, 10, 11, 12 and 14 built on the current page template with the same content so that every page of the course loads, navigates and shows its ERD labels the same way, so a student meets one standard on every chapter.

## The criterion it satisfies (AC3T_Ch12)
**The page of chapter 12 is built on the current template and meets the written standard**

Owner's direction of 2026-10-19: "Keep the same standards with all other pages." Given the page of chapter 12 as it stands (page 9.55.0) and the newest pages of chapters 1 to 7, 9 and 13, when the page is rebuilt as a new file on the page template 9.51.0 with the same content and checked, then ALL of: (1) template: the page HTML contains 'const LBLRE=LBL.map' and 'function edVars()'; (2) content: pages_deck_match_verify reports 0 not carried for the page; (3) ERD: the page test 9.35.0 feature on the labels shown after Untangle reports pass (labels shown after Untangle at least 95 percent of the grid's), measured by the existing test, no new test; (4) tests: the page tests 9.34.0 and 9.35.0, unchanged, report no failure and counts equal to or better than the stored result of the page as it stands (86 widgets, 185 features, 6 gates, 0 skipped); (5) Stage 4: the page ABox is rebuilt from the new page as a new file and the Stage 4 gate runner v1_1_0 for 12 exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS, and the Research, Deck and Page chapter checks of the chapter pass; gates the runner reports as NOT_MEASURED or CANNOT_RUN are reported as such and not claimed; no gate, test or threshold changed; if any element fails the page is named failing and this criterion has no passing result.

Satisfied by: the page, its Stage 4 page ABox and the stored page-test results as new files cited by SHA-256, and the runs of the template markers, the deck match check, the page tests, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge

## The written standard (Spec3T_T)
The written standard of a page, each element a fact the page can be measured against and none a taste: (1) template: the page is built from the current page template, 9.51.0, the one the newest pages of chapters 1 to 7, 9 and 13 use; measured by the two code markers 'const LBLRE=LBL.map' and 'function edVars()' present in the page HTML; (2) content: the page carries the deck's lecture export and stories; measured by pages_deck_match_verify, 0 not carried; (3) ERD: the relationship labels are shown after Untangle; measured by the existing page test 9.35.0, the feature 'the on-choice labels mode ... Untangle finishes and leaves no more lines through unrelated entities than the grid had', which compares the labels shown after Untangle with the grid (at least 95 percent) - no new test is written, the template carries the fix; (4) tests: the page tests 9.34.0 and 9.35.0, unchanged, report no failure and counts equal to or better than the stored result of the page as it stands; (5) Stage 4: the page ABox is rebuilt from the new page as a new file and the Stage 4 gate runner v1_1_0 for the chapter exits 0 with Stage3.F, Stage4.A, B, cov, sub and src PASS; the Research, Deck and Page chapter checks of the chapter still pass. NOT part of the standard: the connectedness repair of the T-Box files; the concept-inventory gates (Stage1.C, Stage1.E, Stage3.E, Stage4.L, which the runner reports NOT_MEASURED because the research data holds no concept inventory) and Cross.B/Cross.C; any change to a gate, a test or a threshold; any change to the content, the decks or the research (except the chapter 8 examples); the owner's open rulings (load-time budget of the page of chapter 6, test-design ruling of chapter 13).

## What the scope excludes
- **The admission rebuilds nothing and decides nothing for the owner**: Any change to the decks or pages of chapters 1 to 14 made in order to admit them: they enter this register exactly as they stand in the course repository, and a deck or page that fails its check is admitted failing. Also the owner decisions the open items wait for (the licence questions, the load-time budget of the page of chapter 6, the test-design ruling of the page of chapter 13).
- **No deck follows the 2nd edition's chapter structure**: Decks organised by the 2nd edition's twelve chapters, including its Advanced Transactions and Scripting chapter as such.
- **The gaps are closed without changing a gate, a test or a threshold, and without the connectedness repair**: Any change to a gate, a test or a threshold in order to make a unit pass (Stage 3.F, the Stage 4 gates, the chapter checks, the page tests); a citation or a claim removed only to make a gate pass; the connectedness repair of the T-Box files, which the owner deferred on 2026-10-20 09:19 Istanbul to a later lineage; recording the Mission outcome and the Achieved status of this lineage, which wait for the owner's act after the gaps are closed.
- **The page standard does not include the connectedness repair, the concept-inventory gates, or any change to a gate, a test or a threshold**: Anything that changes a gate, a test or a threshold in order to make a page pass; the connectedness repair of the T-Box files (deferred by the owner on 2026-10-20 09:19 Istanbul); the concept-inventory gates Stage1.C, Stage1.E, Stage3.E, Stage4.L and Cross.B/Cross.C, which the runner reports NOT_MEASURED or CANNOT_RUN; a change of content, decks or research other than the chapter 8 examples; the owner's open rulings (load-time budget of the page of chapter 6, test-design ruling of chapter 13); recording the Mission outcome and the Achieved status of this lineage, which wait for the owner's act.

## Tools and gates, by version
- Stage 4 gate runner: `08-tooling/sen0401_stage4_gates_v1_1_0.py` - python3 -B 08-tooling/sen0401_stage4_gates_v1_1_0.py NN   (NN = 08, 10, ...; reads the CURRENT RDODI validator v1.13.0)
- Lineage chapter check: `08-tooling/sen0401_lineage_chapter_check_v1_3_0.py` - python3 -B 08-tooling/sen0401_lineage_chapter_check_v1_3_0.py Research/ChNN | Deck/ChNN | Page/ChNN   (reads the PINNED validator v1.6.0)
- Page test 9.35.0: `08-tooling/sen0401_page_test_v9_35_0.py` - the page test as committed; do not edit it
- Page test 9.34.0: `08-tooling/sen0401_page_test_v9_34_0.py` - the page test as committed; do not edit it
- Page template: `08-tooling/course_page_template_v9_51_0.html` - template 9.51.0, the one pages 1 to 7, 9 and 13 use; the markers are 'const LBLRE=LBL.map' and 'function edVars()'
- Page builder: `08-tooling/sen0401_page_build_v4_14_0.py` - the newest page builder; read how pages 9.70.0 to 9.76.0 were built in the precedent commits below
- Page data config: `08-tooling/course_page_config_v2_16_0.json` - the newest page configuration
- Stage 4 ABox builder: `08-tooling/sen0401_page_abox_build_v2_1_0.py` - builds the Stage 4 page ABox from the newest page; a new file, ABox version = page version
- Deck match check: `08-tooling/pages_deck_match_verify_v1_0_0.py` - 0 'not carried' is required
- Page link check: `08-tooling/pages_link_verify_v1_0_0.py` - run for the page as the precedent commits did
- Chapter 8 inputs maker (read first): `08-tooling/ch08-page/inputs_make_v1_0_0.py` - the chapter 13 counterpart is 08-tooling/ch13-page/inputs_make_v1_1_0.py; a new version is a new file
- Validators: the Stage 4 runner reads the CURRENT RDODI pipeline validator v1.13.0 (Ontologies checkout); the chapter checks read the PINNED v1.6.0 (/home/claude/eco_pin/rdodi-ecosystem). Both must pass; they differ (chapter 5 passed the pinned one and failed the current one on '2026a' source labels, which a standalone four-digit year resolves).

## Precedents in git (read them first)
- `ec0bccb` chapter 5 page 9.74.0 on template 9.51.0
- `886a611` chapter 1 page 9.70.0
- `175793e` chapter 6 page 9.75.0
- `58e9dad` chapter 7 page 9.76.0
- `5533071` chapter 13 page 9.69.0 (research 1.0.2)
- `47e631f` chapter 13 Stage 4 page ABox
- `08-tooling/page_jobs_status.md` and `08-tooling/stage4_status.md` describe how the pages were built and checked.

## Facts measured on 2026-10-21 (coordinator)
Pages 8, 10, 11, 12 and 14 lack the template markers; page 8 fails page test 9.34.0 (113 pass, 1 fail, then a crash: no chapter 8 example has a number in its code); the pages' content matches the decks; their test counts do not change on template 9.51.0 (commit 0f7d21f).
