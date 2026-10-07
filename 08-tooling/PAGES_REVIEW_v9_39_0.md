# SEN0401 chapter pages 9.39.0 - the owner's review of 9.38.0 answered

The owner's review of 2026-10-07 10:10, in his words, measured on the 9.38.0 chapter 1 page, and what each
sentence became. One template version per sentence, as before.

| the review said | measured (1366x768, 1280x720, 1536x864) | template | what the page now does |
|---|---|---|---|
| "page fitting problem ... text and visualizations are outside of the direct display and needing move up and down, left and right" | header 113 px + sub-tab row 39 + breadcrumb row 58: the first concept began 329 px down (43% of the screen); Learn sections in a two-column grid 513 px wide, so code panels and maps scrolled sideways; every diagram 68vh tall on a 270 px offset (103% of the viewport) | 9.38.0 | header 74 px (one-line title; the sub-line about the interpreter moved to Start, where it is about the page); tighter rows; one concept per row at full width (1038 px); diagrams sized to the room below them: map, ERD and taxonomy lower edges at 754 of 768 px, no element scrolls sideways |
| "meta information about the work itself not the subject, like those where, who ... use them as guidance not visualize them" | the WHERE/WHO/RUN/LINKS strip on every concept, and the worked-example card repeating the page's own EXAMPLE panel beneath it | 9.39.0 | both removed; where (breadcrumb), who (agent list) and the example (run panel) stay where they already were; the stories' WHO/WHERE/WHEN/READ rows stay - those are the subject's facts under the 5N1K rule |
| "optimize the top level spaces and menus" | as the first row | 9.38.0 | as the first row: 329 -> 280 px to the first concept, with the remaining 206 px being the section's own heading and summary |
| "ERD connections are missing" | the subjects view opened with 2 lines because the mentioned-together relationships were an opt-in toggle | 9.40.0 | on by default in both views (29 lines on chapter 1's subjects: 2 solid operates-on, 27 dashed mentioned-together, each counted), sections grouped and tinted by subject with a legend; the toggle now removes them |

## Verification (08-tooling/chNN-page/, PAGE_VER 9_39_0)
sen0401_page_test_v9_30_0.py 352-354 checks per chapter, 0 failures (the ERD toggle check inverted for 9.40.0);
smoke 1.0.1 12/12 x5; book-corpus check 7/7 for chapters 1-4, chapter 5 6/7 (the pre-existing routing item).
Materials 1.4.6, configuration 2.8.0, data 2.9.0, build 4.12.0.
