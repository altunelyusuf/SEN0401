# Handover to the SEN0401 session: Chapters 7 and 8 this week, in a fresh narrow lineage

**Date:** 2026-11-08. **To:** the new SEN0401 session. **Read this one file; it is self-contained.**
Keep the OE operating discipline and the BRSF lineage discipline exactly as the owner's standing instruction says: read the latest files from their GitHub folders each turn and read one in full only when its version changed. Do not trust memory or summaries.

## 1. What the owner wants, in his words and order

1. **This week is urgent: the Chapter 7 and Chapter 8 materials, each a deck (PPT) and an interactive HTML page, ready by the evening of 2026-11-12.** The midterm covered Chapters 1-6.
2. Then the other chapters, until the end of the semester.
3. Previous chapters are corrected only after the current work is finished. Do not touch Chapters 1-6 this week.
4. Course material development has been taking too much time and effort. Part of your job is to make it faster, not only to deliver.

## 2. Your lineage: a fresh, narrow one

The owner decided to open a fresh lineage for this course. He prefers simple narrow lineages whose mission is the smallest slice that can be closed, with the course-wide mission kept separate. Suggested mission, for you to settle in the Mission stage: *Chapters 7 and 8 of the third edition are taught with a deck and an interactive page, each produced from one owner-approved chapter draft, ready for the lecture of the week of 2026-11-12.* Later chapter pairs get their own narrow lineages; the retrofit of Chapters 1-6 is a later one.

The running lineage must end first, because the owner's rule is one lineage at a time and a lineage is closed by a closure report, not abandoned. Measured on 2026-11-08: it is `07-lineage/sen0401_slides_lineage_v0_1044_0.ttl`, 16.4 MB, 1,022 files in `07-lineage`; items: 502 Done, 115 Cancelled, 58 Suspended, 101 Proposed, 14 InProgress, 9 Ready. Its mission (every lecture renewed from the book, chapter by chapter) is not accomplished, so it ends as cancelled-by-narrowing: run the as-is fit-gap and impact analysis, write the closure report, carry the open chapter scope forward as the fresh lineage's scope, and archive in the next release. Do this in the same step as opening the fresh lineage; do not let it delay the chapter work.

Read before you carry anything forward: **all 14 InProgress items are exam-paper items** (the midterm set v7.2, the answer sheet v7.1, items v1.6-1.8, the clarity check, questions 1-4). The midterm was held with the owner-corrected paper (v8.0.2), and exam work is held outside this repository. Do not carry those items forward. Say so in the closure report.

## 3. The state of Chapters 7 and 8 (read from this repository on 2026-11-08)

They are not unbuilt. `03-materials/ch07` and `ch08` each hold a deck, a `page/` folder, an `assets/` folder and an `rdodi/` folder. Chapter 7 has seven deck versions and its page is at 9.85.0; Chapter 8 has three deck versions and its page is at 9.86.0. So the work is to check what exists against the owner's current teaching emphasis and standards and fix the gaps, not to start from nothing. Say plainly what you find stale or missing before you build.

An earlier check, dated 2026-10-14 and 2026-10-15, reported these open items; verify each against the current files before acting: speaker notes in Chapters 1-5 start lines with labels that the owner's 2026-10-08 ruling forbids; slide code does not always match one page tab in slide order (largest gaps Chapters 4-7, so Chapter 7 matters now); the instructor key has not reached the owner.

## 4. The way to work: the draft first

The slowness has one measured pattern: pages went through five full builds each (Chapter 7: 9.41, 9.64, 9.76, 9.84, 9.85), and Chapter 6 through thirteen deck versions, because layout was built before the content was settled. The owner agreed to this order:

1. Write one plain-text chapter draft: the story (5N1K as human storytelling with real names, a real picture source and a live link), the explanations, the slide outline, the page tabs in slide order, each code example with its executed result, the resources slide. The owner reads and approves it. Ask no question the draft can answer.
2. Only after approval, render the deck, the page and the document from that one draft.
3. A correction after approval goes to the draft and is re-rendered, never patched in one output.
Forecast, not a deadline: draft for the owner's reading by 2026-11-10, so that rendering and checking have two days.

A generic pipeline that does this for any course is being built elsewhere; do not wait for it. Do the same steps by hand with the current builders this week.

## 5. Version rule (the owner's ruling of 2026-11-08)

A file's version must not move because another file was released. Each deck, page and document continues from **its own** last version, with the step sized by the change: patch for a wording or value corrected, minor for something added, major for something removed or changed in meaning. Template, data and builder versions are recorded inside the page as inputs and are not counted in its number. No released file is renamed. This repository now holds `08-tooling/cme_version_check_v1_0_0.py` and `08-tooling/cme_version_baseline_SEN0401_v1_0_0.json`: run `python3 08-tooling/cme_version_check_v1_0_0.py . --baseline 08-tooling/cme_version_baseline_SEN0401_v1_0_0.json --declare <dir>=<size>` before each release. It refuses a file that is not one own step from its predecessor; whether the declared size fits the change is for the reviewer to read.

## 6. Your own questions

List only your own questions to the owner, one at a time, with options.
