# Brief for the executor session SEN0401-I57-papers

Task: Papers v3, key v3, sheet v3
Mode: file-only; starts AFTER cover and items report. Estimated agent-hours: 6.
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

Depends on: the cover renderer (SEN0401-I57-cover) and items v1.2.0 plus the structure file (SEN0401-I57-items), both committed.
Build NEW files: `sen0401_exam_papers_build_v3_0_0.py` from v2_0_0 and `sen0401_exam_paper_lib_v3_0_0.py` from v2_0_0. Forms A and B as before (mixed order, different codes). Page 1 of each paper is the cover page (function from the cover renderer), then the 5 questions in the structure file's numbering. Page budget: 4 pages in total including the cover if it fits; otherwise 6 pages with better formatting and readability; never shorten an item to fit, and say which you chose and why. Tips printed with their terms. Key v3 (Word). Answer sheet v3: PDF, position-exact, adapted to the new numbering, same block types so reader v1.2.0 stays unchanged; run `sen0401_exam_answersheet_check_v1_1_0.py`-style checks on the new layout (new copies, old tools unchanged) and the reader measure `sen0401_exam_answersheet_measure_v1_2_0.py` on 40 synthetic sheets per form. Report every result verbatim. Output dir `08-tooling/exam/papers_midterm_v3/`.

