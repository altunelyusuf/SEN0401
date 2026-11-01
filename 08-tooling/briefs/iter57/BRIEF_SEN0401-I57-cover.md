# Brief for the executor session SEN0401-I57-cover

Task: Exam cover page renderer
Mode: file-only, independent, start now. Estimated agent-hours: 3.
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

Source: the owner's cover page template /home/claude/exam_cover_template/IKU_exam_cover_page_template_source.docx (from another course). Read it fully first (header, tables, fonts, spacing).
Build `08-tooling/exam/sen0401_exam_cover_render_v1_0_0.py` (a NEW file) with a function `cover(doc, course_code, course_name, exam_title, term, year, date_time, duration, instructor, questions, outcomes, instructions)` that writes the cover page into a python-docx Document starting from the template's look (copy the template's styles, do not invent a new look). Fill:
- Department of Computer Engineering; course SEN0401 Special Topics: Blockchain (and the SEN0414 variant); Exam title 'Midterm Exam'; Academic Year 2026-2027; Term Fall; Duration 60 minutes; Instructor Dr. Yusuf ALTUNEL.
- Date and Time: a clearly marked fill-in line ('____ / ____ / 2026   __:__'), because the owner has not given it.
- Question/grade table: Q1-Q4 each /25, Q5 /10 (bonus), Total /100 plus bonus.
- Instructions adapted to our exam: a separate answer sheet that is machine-read (pen rules, fill the marks fully), what is allowed (state it neutrally; if unknown leave a marked fill-in), no phones.
- Learning-outcome rows per question: take the outcomes from `08-tooling/exam/` outcomes source `sen0401_outcomes_v1_1_1.ttl` (find its path with Glob); never use the other course's numbers. Spell out every abbreviation at first use.
- Keep the cheating WARNING block of the template, translated only if the template is Turkish-English mixed: keep the template's language.
Also write a demo `sen0401_exam_cover_demo_v1_0_0.docx` and a render check: convert to PDF with LibreOffice, rasterize page 1, confirm it is ONE page and the table fits. Run that check and report verbatim. Do not touch the paper builders; another session integrates your function.

