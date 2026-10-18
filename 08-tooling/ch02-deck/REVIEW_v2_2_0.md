# Chapter 02 deck 2.2.0 - review (2026-10-19)

New version of deck 2.1.0, built by `sen0401_deck_rebuild_v1_0_0.py 2` on the same engine as decks 5 to 14 (renderer `sen0401_deck_render_v1_3_0.js`, OOXML fix, office stamp), from `deck_plan_v2_2_0.json`.
Nothing committed was edited; the plan, the deck, the recording and the lecture export are new files.

## What changed
- Every console and program was re-run under Python 3.14.6 and re-recorded (`examples_out_v1_3_0.json`); every caption says "run under Python 3.14.6" and the plan's `meta.python` and `meta.version` match.
- Speaker notes are short reader's prose: 2 to 4 sentences, at most 100 words, no presenter label, none repeated on another slide (2 notes replaced by hand, the rest rewritten by `sen0401_notes_rewrite_v1_0_0.py`).
- Layout: no text frame overflows or overlaps (fit check 0, layout check clean); chips, stat tiles, timelines, code blocks and captions were re-spaced in the plan patch `deck_patch_v2_2_0.py` and in the renderer wrapper.
- Honesty: `meta.honesty` lists recorded slides 12 and 21 and NOT EXECUTED slides none; each slide says so on its face.
- The console on slide 27 named Python 3.13.16; it now names the interpreter of the new recording.
- Stale fixtures were not refused before (none in `fixtures/`); now the stale expression and the stale chart are, and so are the other owners' fixtures.
- `deck_check_v1_3_0` and `deck_check_v1_0_0.py` wraps `sen0401_deck_check_v1_1_0.py`; `fixtures/` holds stale fixtures that it refuses; `sen0401_deck_fixtures_v1_1_0.py --run` makes every owner check refuse its own fixture for its own reason and accept the control.

## Status after (lineage `Deck/Ch02` with `sen0401_lineage_chapter_check_v1_2_0.py`: PASS)
| check | result |
|---|---|
| deck_check | PASS |
| structure | PASS |
| fit | PASS |
| picture | PASS (8 parts) |
| links | FAIL: the youtube video answers 429 from this machine |
| honesty | PASS |
| story | FAIL: 3 stories |
| arc | FAIL: stories on slides 6 and 21 lack a fact row field or picture; the resources slide has no standards or seminal group; no analogies list (warning) |
| lookfeel | PASS |

## What still fails and why
- links: not fixable in the deck; the links themselves are unchanged and answered when they were opened for the link job. They are blocked or rate-limited here.
- story: the story module (`sen0401_ch02_stories_v*.py`) has no picture, no ISO date and no 5N1K row in the form the story check reads; a fix needs a licensed picture per story with its provenance row, which this pass did not acquire.
- arc: stories on slides 6 and 21 lack a fact row field or picture; the resources slide has no standards or seminal group; no analogies list (warning).
- The page of this chapter still needs rebuilding from `ch02-page/lecture_v1_2_0.json`, and the register still names `sen0401_lineage_chapter_check_v1_1_0.py`, which passes for this chapter.

