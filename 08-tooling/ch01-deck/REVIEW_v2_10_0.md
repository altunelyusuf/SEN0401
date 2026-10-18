# Chapter 01 deck 2.10.0 - review (2026-10-19)

New version of deck 2.9.0, built by `sen0401_deck_rebuild_v1_0_0.py 1` on the same engine as decks 5 to 14 (renderer `sen0401_deck_render_v1_3_0.js`, OOXML fix, office stamp), from `deck_plan_v2_10_0.json`.
Nothing committed was edited; the plan, the deck, the recording and the lecture export are new files.

## What changed
- Every console and program was re-run under Python 3.14.6 and re-recorded (`examples_out_v1_2_0.json`); every caption says "run under Python 3.14.6" and the plan's `meta.python` and `meta.version` match.
- Speaker notes are short reader's prose: 2 to 4 sentences, at most 100 words, no presenter label, none repeated on another slide (9 notes replaced by hand, the rest rewritten by `sen0401_notes_rewrite_v1_0_0.py`).
- Layout: no text frame overflows or overlaps (fit check 0, layout check clean); chips, stat tiles, timelines, code blocks and captions were re-spaced in the plan patch `deck_patch_v2_10_0.py` and in the renderer wrapper.
- Honesty: `meta.honesty` lists recorded slides 7 and 24 and NOT EXECUTED slides 34; each slide says so on its face.
- Slide 27 said four peers and counted links; the program has seven peers and counts rounds of gossip: the slide now says so.
- Slides 12 and 13 had the same notes, slides 6 and 7, 25 and 27, 1 and 46 too: each now has its own.
- `deck_check_v1_2_0` and `deck_check_v1_0_0.py` wraps `sen0401_deck_check_v1_1_0.py`; `fixtures/` holds stale fixtures that it refuses; `sen0401_deck_fixtures_v1_1_0.py --run` makes every owner check refuse its own fixture for its own reason and accept the control.

## Status after (lineage `Deck/Ch01` with `sen0401_lineage_chapter_check_v1_2_0.py`: PASS)
| check | result |
|---|---|
| deck_check | PASS |
| structure | PASS |
| fit | PASS |
| picture | PASS (20 parts, the cases slide's five photographs counted by picture_check 1.1.0) |
| links | FAIL: 6 of 20 answer 4xx or nothing from this machine: sec.gov and cnbc.com and coingecko.com answer 403 to a script, two web.archive.org copies do not connect, youtube answers 429; none was changed |
| honesty | PASS |
| story | FAIL: 9 stories |
| arc | FAIL: stories on slides 9, 16 and 34 lack a fact row field or picture; no analogies list (warning) |
| lookfeel | PASS |

## What still fails and why
- links: not fixable in the deck; the links themselves are unchanged and answered when they were opened for the link job. They are blocked or rate-limited here.
- story: the story module (`sen0401_ch01_stories_v*.py`) has no picture, no ISO date and no 5N1K row in the form the story check reads; a fix needs a licensed picture per story with its provenance row, which this pass did not acquire.
- arc: stories on slides 9, 16 and 34 lack a fact row field or picture; no analogies list (warning).
- The page of this chapter still needs rebuilding from `ch01-page/lecture_v1_2_0.json`, and the register still names `sen0401_lineage_chapter_check_v1_1_0.py`, which passes for this chapter.

