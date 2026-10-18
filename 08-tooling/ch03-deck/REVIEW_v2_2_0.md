# Chapter 03 deck 2.2.0 - review (2026-10-19)

New version of deck 2.1.0, built by `sen0401_deck_rebuild_v1_0_0.py 3` on the same engine as decks 5 to 14 (renderer `sen0401_deck_render_v1_3_0.js`, OOXML fix, office stamp), from `deck_plan_v2_2_0.json`.
Nothing committed was edited; the plan, the deck, the recording and the lecture export are new files.

## What changed
- Every console and program was re-run under Python 3.14.6 and re-recorded (`examples_out_v1_2_0.json`); every caption says "run under Python 3.14.6" and the plan's `meta.python` and `meta.version` match.
- Speaker notes are short reader's prose: 2 to 4 sentences, at most 100 words, no presenter label, none repeated on another slide (1 notes replaced by hand, the rest rewritten by `sen0401_notes_rewrite_v1_0_0.py`).
- Layout: no text frame overflows or overlaps (fit check 0, layout check clean); chips, stat tiles, timelines, code blocks and captions were re-spaced in the plan patch `deck_patch_v2_2_0.py` and in the renderer wrapper.
- Honesty: `meta.honesty` lists recorded slides 13, 15, 17 and 19 and NOT EXECUTED slides 9 and 11; each slide says so on its face.
- The old chapter check refused the merkle_root function as shown; the new check compares every example with the new recording instead. The corrected date of the Bitcoin 0.1 release (8 January 2009) and all link labels are kept.
- `deck_check_v1_2_0.py` wraps `sen0401_deck_check_v1_1_0.py`; `fixtures/` holds stale fixtures that it refuses; `sen0401_deck_fixtures_v1_1_0.py --run` makes every owner check refuse its own fixture for its own reason and accept the control.

## Status after (lineage `Deck/Ch03` with `sen0401_lineage_chapter_check_v1_2_0.py`: PASS)
| check | result |
|---|---|
| deck_check | PASS |
| structure | PASS |
| fit | PASS |
| picture | PASS (4 parts) |
| links | FAIL: web.archive.org copy of the 2014 Bitcoin Foundation page does not connect from this machine |
| honesty | PASS |
| story | FAIL: 3 stories |
| arc | FAIL: story slide 14 lacks a fact row field or picture; the resources slide has no standards or community group and no video link (a video cannot be verified from this machine); no analogies list (warning) |
| lookfeel | PASS |

## What still fails and why
- links: not fixable in the deck; the links themselves are unchanged and answered when they were opened for the link job. They are blocked or rate-limited here.
- story: the story module (`sen0401_ch03_stories_v*.py`) has no picture, no ISO date and no 5N1K row in the form the story check reads; a fix needs a licensed picture per story with its provenance row, which this pass did not acquire.
- arc: story slide 14 lacks a fact row field or picture; the resources slide has no standards or community group and no video link (a video cannot be verified from this machine); no analogies list (warning).
- The page of this chapter still needs rebuilding from `ch03-page/lecture_v1_2_0.json`, and the register still names `sen0401_lineage_chapter_check_v1_1_0.py`, which cannot pass for this chapter, because the chapter's committed deck_check_v1_0_0.py is frozen to the old deck.

