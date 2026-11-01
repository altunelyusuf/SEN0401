# Brief for the executor session SEN0401-I57-items

Task: Items v2: audit and rewrite for understanding, 5-question structure
Mode: file-only, parallel with cover. Estimated agent-hours: 6.
Note: this brief was written by hand by the lineage agent for an urgent launch; the register entry for it is appended afterwards (disclosed). The executor does not touch the register.

## Rules of an executor
- You are an EXECUTOR session. You do the one task below. You do not start, finish or record any other task.
- You do NOT touch the register (07-lineage). The builder session writes it, records your start and runs the control through the evidence bridge after you report.
- A committed file is never edited: every output is a new file with a new version number. The only changes to gates, tests and templates that are allowed are the NEW files named in your task. No existing gate, test, threshold, template or criterion is edited or weakened.
- You never judge your own work with a tool you wrote: the deck check, the page test and the page tasks are separate sessions. A FAILING RESULT IS NEVER WORKED AROUND: no skipped feature, no raised timeout, no edited expected value. NOT_MEASURED, CANNOT_RUN and a skip are not passes.
- Report every result exactly as the tool prints it: PASS, FAIL, NOT_MEASURED, CANNOT_RUN.
- STOP and report to the coordinator, without working around it, if: the task cannot be satisfied without editing a committed file, a gate or a test beyond the named new files; a check fails and you cannot fix it within your task; or anything in this brief contradicts what you find.
- Commit your work to main with a clear message (no force push; pull --rebase before push). Commit each verified step at once: the repository (committed and pushed work) is the only record if a container restarts.
- The machine has 2 cores shared with other sessions: run browser tests (page test runs take about nine minutes) one at a time, never a build beside a test; delete stale /tmp/sen0401_page_test_* and /tmp/sen0401_fx_* folders older than 60 minutes before a batch of runs (the root disk is small). A flaky main-thread budget failure (no [FAIL] feature line) may be run again up to three times, every run kept as a log; a [FAIL] line is a result.
- Your final report to the coordinator: the commit SHAs, the new files, and the verbatim output of every check you ran; say what failed, if anything.
- Owner's standing teaching-material rules (they are the criteria, not decoration): full sentences are fine but no long paragraphs; explanation beside every code listing; the executed result of code shown as a visualization; an everyday analogy for each key concept; 5N1K stories with real names, real pictures and live links; native charts only; numbered slides; a resources slide; short speaker notes; no dark/light switching mid-deck; deck and page keep a matching look; pages: tabs are sub-menus of the selected item and never mixed with it, no third tab level, tabs and tree synchronised, uncrowded menu, no duplicated lists, content fits without scrolling, zoom on every diagram, default text not small and a text-size control, adaptive to phone and large screens, every term explained in full-sentence paragraphs, code that really runs.
- Git: run every add, commit, pull --rebase and push under `flock /tmp/sen0401_git.lock <command>` (one commit lane); commit only your own files by path.
- Browser tests (page tests and page checks) run ONLY under `flock /tmp/page_test.lock <command>`: they queue instead of overlapping with other sessions. Do not wait for a quiet machine by polling; take the lock.


## The task

Owner's new rules (13:04, 2026-11-01, verbatim sense): never ask memorising questions; never require students to recall a specific term; if a term is used, print a short tip (what it is) with it; every abbreviation is spelled out in full at first use; ask about USE, IMPORTANCE and the REASON things exist in Bitcoin, not what a script type is called. Items of the cs_encode type may stay if the rule is given inside the question.
Input: `08-tooling/exam/sen0401_exam_items_midterm_v1_1_0.json` (23 items), its build script `..._build_v1_1_0.py` and its check log. NEW files only.
1. AUDIT (report as a table, per item key): memorisation Y/N, unexpanded abbreviation Y/N (e.g. WIF, SHA256, SegWit, BIP329, P2PKH, CompactSize appear), term without tip Y/N, verdict KEEP / REWRITE / REPLACE. Count by chapter. Read every item in full; do not use a name heuristic.
2. REWRITE to v1.2.0 (new JSON, new build script, new check log): items rewritten for understanding, with tips and expanded abbreviations; do not invent terms or facts; keep each item's chapter-critical points covered (re-run the critical-points tool) and keep seeds/answers consistent (computed fields recomputed by the tool, not by hand).
3. STRUCTURE: group items into 5 question formats, 4 questions of 25 points and a 5th of 10 points (bonus), each with sub-questions. Formats must print well and stay machine-readable via the answer sheet: reading/choice, ordering, calculation, matching, fill-in, short explanation (short explanation items are marked by hand: mark them clearly as not machine-read). Output `sen0401_exam_structure_v1_0_0.json` with question numbers, sub-question keys, points. Keep the answer sheet block types unchanged (ChoiceFour, NumericAnswer, Ordering, Matching, FillBlankGroup) unless you stop and report.
Run the existing item checks on the new file and report verbatim. Do not change the paper builders or the sheet.

