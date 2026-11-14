# Handover: the owner's rulings on decks and pages, and what the check finds on this course today (v1.1.0, 2026-11-14)

**To:** the next session of this course. **Kind:** rulings to apply, with a measured baseline. Nothing in this repository's chapters was changed; one tool was added to `08-tooling`. This version replaces v1.0.0: it asks for corrections of chapters already released as done.

## What the owner said (2026-11-14, 11:54)
The newly built slides keep the old habits. Slides are not meaningful or informative. Code is not always in the HTML file. The HTML keeps lambda-based code that complicates it for no reason. Presenter notes are insufficient. `>>` stays in code snippets. He asked for rulings.

## The six rulings, in plain words
1. **Every slide teaches one thing.** The title says what the slide teaches (at least 4 words, not a bare topic). The slide shows one thing to look at: a picture, a native chart, a diagram, a table, or code with its result. A student who has only the slide and its notes can say its point in one sentence, and the point ties to a learning outcome of the chapter.
2. **Presenter notes carry the lecture.** 60 to 140 words per content slide (at least 30 on title, part and resources slides), in full sentences; no label prefixes; a code slide's notes say what to point at and what the result shows; the notes lead into the next slide. Short sentences stay; thin notes go. This replaces the earlier "notes are cues".
3. **Slide code lives in one page tab.** Every code example on a slide appears unchanged and in slide order in one dedicated tab named **Slide code**, and the tab runs it. The Code Lab stays separate. This settles the open decision about which tab carries the slides' code.
4. **Code is plain code.** No `>>>`, `...` or `>>` before any line, in a deck or a page. No decorative prompt chip on slides. The printed result is shown beside the code, never inside it.
5. **Only taught Python.** An example uses only what this chapter or an earlier one teaches. `lambda` is not used unless the chapter teaches it; write a named function for a key or callback.
6. **Checks before release.** A deck or page is released only when every automatic condition passes on it and every reviewed condition (the three reviewer roles: academician, faculty reviewer, undergraduate reader) has a recorded verdict. Chapters in progress come first; earlier chapters are corrected after the current work is finished, as the owner ordered on 2026-11-08.

## What the check finds today

Tool: `08-tooling/cme_material_check_v1_0_0.py DECK.pptx PAGE.html` (reads only; it tests 8 automatic conditions; two named conditions, the feature register and the page running the Slide code tab, are not built yet and are not read as passes).

| chapter | slides | code frames | title 4+ words | something to look at | notes 60-140 words | no prompt markers | parses as shown | no lambda | code found in page |
|---|---|---|---|---|---|---|---|---|---|
| chapter 7 | 61 | 43 | 7/59 fail | 31/59 fail | 59/61 fail | 43/43 fail | 43/43 fail | 0/43 fail; page 198 | 0/43 fail |
| chapter 8 | 51 | 59 | 6/49 fail | 18/49 fail | 49/51 fail | 59/59 fail | 59/59 fail | 8/59 fail; page 18 | 0/59 fail |
Reading the numbers: "failed a of b" counts slides, code frames or checks. A pass on "code in page" means each frame's first line was found anywhere in the page; the one-tab rule is not yet tested.

## What is asked: corrections now
The owner's complaint is about the chapters just built, so they are corrected first, before any other chapter. In scope: SEN0401 chapters 7 and 8 (both released as done).

1. Chapter 7 deck: rewrite the notes of 59 slides and give the 31 slides that have nothing to look at a diagram, picture, chart or table; lengthen the 7 short titles; remove the `>>>` from all 43 code frames.
2. Chapter 8 deck: the same, for 49 notes, 18 slides without a visual, 6 titles and 59 code frames; replace the `lambda` in 8 frames with named functions.
3. Both pages: add the **Slide code** tab (every slide example, unchanged, in slide order, running, result beside it), and remove `lambda` from the page code unless the chapter teaches it (198 occurrences in chapter 7, 18 in chapter 8).

After the correction: run `08-tooling/cme_material_check_v1_0_0.py DECK.pptx PAGE.html` on each deck and page and expect every automatic check to pass; record the three roles' verdicts (academician, faculty reviewer, undergraduate reader) on the reviewed conditions (teach-back, notes for code slides, links between slides, the result beside the code). Version each corrected file by the own-version rule (the size of the change sets the step; the build inputs are not counted). Earlier chapters are corrected only after this work is finished, as the owner ordered on 2026-11-08. Report back simply: which chapters now pass and which do not.
