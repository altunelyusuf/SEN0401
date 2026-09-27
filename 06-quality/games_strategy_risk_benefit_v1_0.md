# Games: embedded in the chapter pages, or built on their own? — risk-benefit analysis

Version: 1.0

Prepared 2026-09-27 for the owner's decision. Evidence is measured from the owner's 2025 materials, imported
byte-identical into `03-materials/owner-legacy-2025/` (inventory: `legacy_inventory_v1_0_0.json`), and from this
repository's 2026 pages. Scores 1–5 (5 = better) are judgements resting on that evidence; weights are equal and
are the owner's to change.

## Strategies

- **A — Embedded:** each game written inside its chapter page (the 2025 approach).
- **B — Standalone:** each game its own HTML file, built, tested and versioned alone (the owner's 2026 plan).
- **C — Standalone on a shared shell, linked from the pages:** as B, but every game uses one small shared game
  shell (the page's design tokens, text-size control, score reporting); a chapter page shows a game card next to
  the concept it practises and opens the game in place.

## Evidence from 2025

- **The transactions page took 12 builds in about 13.5 hours** (12 Dec 16:41 → 13 Dec 06:15), growing from 83 KB to
  236 KB; five builds are named "FINAL", one "FIXED", one "DEBUG".
- **Games appear in the early pages and then disappear:** "game" occurs 36 times in the week 2 page (with 3 canvases
  and 3 animation loops), 35 times in chapter 3's and 12 times in chapter 4's, then 0–1 times in chapters 5, 6, 8 and 9.
- **Chapter 3's ten games were specified but not delivered as files:** the games index links ten game files
  (`game1_layer_builder.html` … `game10_node_sync_master.html`); none is in the upload.
- **A single game is small:** the standalone "Break the Chain" game is 16 KB, and its Gemini Python original 7 KB.
- **The 2026 pages are already large:** 217 KB, 240 KB and 300 KB, and each takes about five minutes to test in full.
- **The week 2 page runs its code examples with `eval`,** the pattern behind the 2026 Defender removal.

## Scores

| Criterion | A embedded | B standalone | C shared shell | Evidence |
|---|---|---|---|---|
| Generation reliability | 1 | 5 | 4 | 12 builds for one page; games vanish after chapter 4; one game is 16 KB |
| Testability | 2 | 5 | 5 | a page's full test already takes ~5 minutes; a game alone can be tested in seconds |
| Versioning (rename-on-change) | 1 | 5 | 4 | embedded: any game fix is a new page version, ABox and materials record |
| Page size and speed | 1 | 5 | 4 | pages are 217–300 KB before any game |
| Learning in context | 5 | 2 | 4 | a separate file loses the concept the game practises; C opens it beside the concept |
| Reuse across chapters and years | 1 | 4 | 5 | C's shell and ontology-driven content carry over |
| Security exposure | 2 | 4 | 4 | more script per page; `eval` in 2025 |
| Consistent look and controls | 4 | 2 | 5 | C inherits the page's design and text-size control |
| Progress and scores | 4 | 2 | 4 | C reports back to the page |
| **Total (equal weights)** | **21** | **34** | **39** | |

## Reading

B removes last year's failure — pages too large to generate and fix reliably — and C keeps that while adding what
B gives up: the game beside the concept it practises, one look, and scores the page can show. The difference
between B and C is one small shared shell, built once.
