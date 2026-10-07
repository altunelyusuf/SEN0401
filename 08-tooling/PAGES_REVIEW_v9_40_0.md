# SEN0401 chapter pages 9.40.0 - the owner's review of 9.39.0 answered (template 9.41.0)

The owner's review of 2026-10-07 12:04, in his words, measured on the 9.39.0 chapter 1 page (Money > Unit >
Satoshi, 1366x768), and what it became. One template version: the reading area.

| the review said | measured | what the page now does |
|---|---|---|
| "keep the top the most valuable area and never spend it cheaply" | above the concept's first sentence: the sub-tab row, the breadcrumb row, a pill row, a name/previous/next/Show-all row, the section heading, a Mark-as-understood row, the section summary, and its whole text once "more" was open - the concept began mid-screen | one breadcrumb row (subject > section select > concept pills, Show all); the section's heading and text appear only in Show all; a focused concept's first paragraph begins 176 px from the top (test gate: 240 px) |
| "use tool tips instead of messages and accordions whenever possible" | each pane opened with a note paragraph (or a folded "About" accordion holding its legend and note); the map carried a two-line explanation and a zoom hint; the section overview was a "more" accordion | pane notes are a small (i) at the pane's top right: tooltip = first sentence, click = the full note in the right-hand card; legends stay as one visible line; map explanation and zoom hint are titles; no accordion remains in Learn |
| "the lastly added visualizations and interactions are mostly appended not merged" | the neighbourhood map sat under the run panel at the end of the concept | on screens over 900 px the map sits beside the paragraphs (text left, map right, sticky); on phones it follows them |
| "hidden content, only randomly clicking displays ... should never exist" | paragraphs after the first folded under their lead sentences; the chapter visual behind a "Visualise" button | every paragraph shown; every visual shown and run when its section is first revealed (sections, not only concepts) |
| "some tool tips are long paragraphs ... use the right branch cards instead" | the hover tooltip of a concept carried its whole first paragraph (about 90 words) | one sentence; the (i) and the card carry the rest |

Also: "Mark as understood" is a compact control at the right of the heading, not a row.

## Verification (08-tooling/chNN-page/, PAGE_VER 9_40_0)
sen0401_page_test_v9_31_0.py 356-358 checks per chapter, 0 failures (three 9.3x assertions updated to the new
rule: section text shown whole instead of a "more" accordion, pane introductions as (i)+card instead of folded
"About", the ontology-graph narrative read from the card; the visual-toggle clicks removed); smoke 1.0.1 12/12
x5; book-corpus check 7/7 x4, chapter 5 6/7 (pre-existing). Materials 1.4.7, configuration 2.9.0, data 2.10.0,
build 4.13.0.

## Found while building
- The page's own fitViews() sizes every .diagram to the viewport (it caused the side map to grow to 538 px); the
  side map now carries the `small` class that fitViews respects.
- Visuals of level-2 sections (e.g. chapter 2's "facts" visual) were never run once the toggle went; running on
  reveal now covers every visible section, not only concepts.
