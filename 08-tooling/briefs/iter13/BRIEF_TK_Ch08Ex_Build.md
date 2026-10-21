# Brief for the executor session SEN0401-I13-ch08-examples

Generated from the register sen0401_slides_lineage_v0_150_0.ttl. Task TK_Ch08Ex_Build (state in the register: Ready).
Executor session name: **SEN0401-I13-ch08-examples**. The register's note on 'work begun' for this task names this session.

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
**Give chapter 8 real executable examples with numbers**

Write a new version of the chapter 8 research (and the document and page data that follow it) whose examples are real executable code with numbers the reader can edit, as chapter 13 did (research v1_0_2, commit 43886764, and an inputs maker, 08-tooling/ch08-page/inputs_make_v1_0_0.py exists for chapter 8 and is to be checked first). A committed file is not edited. No test, gate or threshold is changed; no citation or claim is removed only to pass. If the deck of chapter 8 has to carry the new examples for the page and the deck to stay equal (pages_deck_match_verify), that is stated and put to the coordinator, not done silently. Satisfies the criterion ex:AC3T_Ch08_Examples. Status correction 2026-10-21 (G113): the In Progress state of v0.146 (2026-10-21T07:05:34 UTC) was a status without work, a coordination error of the builder session; the item is Ready again by the recorded return ex:Return3T_TK_Ch08Ex_Build; the start is recorded only at the real start of an executor inside a started sprint.

Depends on: nothing

## The story it belongs to
**Chapter 8 has real executable examples with numbers**

As a SEN0401 instructor I want the examples of chapter 8 to be real executable code with numbers the reader can edit so that the page of chapter 8 passes the page test every other page passes, and its examples teach by being run and changed.

## The criterion it satisfies (AC3T_Ch08_Examples)
**Chapter 8 has real executable examples with numbers and its page passes page test 9.34.0**

Given the chapter 8 research and its page (page 9.51.0 fails page test 9.34.0: 113 pass, 1 fail, then a crash, because no chapter 8 example has a number in its code), when a new version of the chapter 8 research gives its examples real executable code with numbers the reader can edit (following chapter 13: research v1_0_2, commit 43886764, and an inputs maker) and the page is rebuilt from it, then the page test 9.34.0, unchanged, reports no failure and no crash on the chapter 8 page; the Stage 4 gate runner for 08 reports Stage3.F and Stage4.A, B, cov, sub and src PASS; the Research, Deck and Page chapter checks of chapter 8 pass; no test, gate or threshold is changed and no citation or claim is removed only to pass; if any fails the unit is named failing and this criterion has no passing result.

Satisfied by: the new chapter 8 research and page files cited by SHA-256, and the runs of the page test 9.34.0, the Stage 4 gate runner and the chapter checks, verified by the evidence bridge

## The written standard (Spec3T_C8)
Every chapter 8 example has a number in its code that the reader can edit, as chapter 13's do after research v1_0_2; the page test 9.34.0 reports no failure and no crash on the chapter 8 page; no test or gate is changed.

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
- `4388676` chapter 13 research v1.0.2: sixteen worked examples with changeable whole numbers (the precedent for chapter 8)
- `1b0b5b5` chapter 13 deck v1.2.0 from that research: the executed examples attached to slides. Chapter 13 changed its deck here; if chapter 8 needs the same, STOP and report what and why before you change a deck
- `5533071` chapter 13 page rebuilt from it
- `47e631f` chapter 13 Stage 4 page ABox
- `08-tooling/page_jobs_status.md` and `08-tooling/stage4_status.md` describe how the pages were built and checked.

## Facts measured on 2026-10-21 (coordinator)
Pages 8, 10, 11, 12 and 14 lack the template markers; page 8 fails page test 9.34.0 (113 pass, 1 fail, then a crash: no chapter 8 example has a number in its code); the pages' content matches the decks; their test counts do not change on template 9.51.0 (commit 0f7d21f).
