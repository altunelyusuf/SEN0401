# Chapter 6 deck v1.0.0 - the three-role review record

Same method as chapters 1-5; first cycle over the chapter-6 classroom deck (26 slides), drawn by the shared
renderer (CME materials standard v1.0.0). First chapter built under the notes standard of 2026-10-08 (reader's
prose, no presenter labels; `deck_notes_check_v1_0_0.py` run on the finished file). Built on 2026-10-08 without a
Bitcoin Core node: every figure the book took from a running node (the weight 569) is recomputed from the bytes
and compared with an explorer's saved record, and the slides say so.

## The academician's build notes
- Arc: a transaction, byte by byte (Alice's 194 bytes parsed by the chapter's own library; the outpoint read in both
  byte orders; the book's fold-tac pipeline in Python) -> sequence and lock time (the three meanings of the field
  decided bit by bit with BIP68's constants and BIP125's threshold; lock time against the median of eleven blocks) ->
  outputs (amounts and the fee as a difference; the 2010 overflow reproduced as a signed 64-bit wrap and refused by
  the range check; dust thresholds as a NATIVE bar chart drawn only from the executed DustLimit example) ->
  witnesses (four push encodings, four identifiers for the first bitcoin transaction; Alice's txid unchanged and
  her wtxid changed when her whole witness is replaced; the soft fork as a two-column rule) -> the coinbase and the
  weight (the subsidy per halving as a native chart; the book's twelve-row weight table as a native chart, recomputed
  from the byte spans and summing to 569 three ways).
- Four 5N1K stories with fact rows, live links and licensed photographs where one could be verified: the first
  transaction to spend an output, 10 BTC to Hal Finney in block 170 (his 1972 newspaper photo, public domain);
  Pizza Day, 10,000 BTC in a 131-input transaction (the plaque at the Jacksonville Papa John's, CC0); the value
  overflow of block 74,638 (Gavin Andresen at Web Summit 2014, CC BY 2.0); and Mt. Gox blaming malleability, drawn
  from the Decker-Wattenhofer figures because no free-licence photograph of the exchange could be verified.
- Everything executed: 21 consoles under Python 3.14.6 from `examples_v1_0_0.py` (24 groups, one per concept of
  the taxonomy), re-run off the finished file by `deck_check_v1_0_0.py`; the three charts take their series from
  the executed `DustLimit`, `BlockSubsidy` and `WeightUnits` groups and from nowhere else.
- Two places where the book and the sources differ are on the slides as computed facts rather than as remarks:
  the subsidy ends at block 6,929,999 (the book says up until 6,720,000, which is where it becomes one satoshi),
  and the header weighs 320 by BIP141's formula (the book says 240).

## The expert reviewer's checklist and findings
| check | command | result |
|---|---|---|
| Numbered slides, 20-26; warm-ivory; agenda with exact ranges; summary; takeaway strips | `python3 deck_build_v1_0_0.py` | 26 slides; agenda ranges 3-5, 6-10, 11-13, 14-17, 18-26 checked by the build; 20 content slides carry a takeaway, the four story slides and the CQ slide carry their own rows |
| Full sentences on slides; no bare code or numbers | build gates (lede <= 34 words, takeaway <= 24 words, bullets <= 30 words) and the contact sheets | pass: every console has a label line naming what it shows and a run-under caption; every number sits in a sentence, a label or a chart title |
| Every example executed, result shown; charts native with data labels, series from executed examples only | `python3 examples_run_v1_0_0.py /root/.local/bin/python3.14 examples_out_v1_0_0.json` -> 24 groups; `python3.14 deck_check_v1_0_0.py sen0401_ch06_deck_v1_0_0.pptx` | **44 examples re-run on 26 slides; 0 mismatch(es)**; the build asserts the chart series against the parsed outputs (dust = [546, 294, 330, 0]; subsidy[0] = 50.0, subsidy[4] = 3.125; weight rows sum to 569) |
| The check can fail | `python3 fixtures_make_v1_0_0.py sen0401_ch06_deck_v1_0_0.pptx fixtures` then `python3.14 deck_check_v1_0_0.py fixtures/fixture_stale_expr_v1_0_0.pptx` | fixture written from 1 slide; **1 mismatch, exit 1** (the recomputed identifier edited by one character on slide 18 is refused) |
| Code never wraps; width AND height gates | `code()` in the build refuses a console under 7 pt | pass: the smallest console sets at 7.1 pt (the push-encodings console of slide 18); eleven consoles were widened or split during the build to clear the gate |
| Layout: no overflow, nothing outside the slide, notes on every slide | `python3 ../deck_layout_check_v1_0_0.py sen0401_ch06_deck_v1_0_0.pptx` | **clean** (0 overflowing frames, 0 shapes outside, 0 slides without notes) after three rounds: labels shortened, three chips rows trimmed, ledes kept clear of the consoles by a new build gate (nothing may start above 1.68 in under a lede) |
| Speaker notes are reader's prose: no SAY/ASK/STORY/FULL TEXT, two or more sentences, every line ends a sentence, no bare URL | `python3 ../deck_notes_check_v1_0_0.py sen0401_ch06_deck_v1_0_0.pptx` | **26 slides, 26 with notes written for the reader; VERDICT: PASS**; notes average 123 words (53 to 276); the build refuses a directive label before rendering |
| Stories 5N1K; licences on-slide and in ASSETS_PROVENANCE | `python3 ../sen0401_ch06_stories_v1_0_0.py` | 4 stories; self-check failures: 0; three photographs credited on the slide and in `03-materials/ch06/assets/ASSETS_PROVENANCE_v1_0_0.md`; the four links answered 200 on 2026-10-08 |
| Resources slide with live links | links group on slide 25 | 9 links; every URL in `ch06-page/resources_v1_0_0.json` (26) answered 200 on 2026-10-08 (GitHub HTML answers 403 to this session, so raw.githubusercontent.com is linked) |
| Facts on slides come from the corpus, the outputs or a story | `assert_fact()` on the stat tiles | 302,000 BTC, 1,811 BTC and 850,000 BTC are found in the story text |
| No dark/light switching mid-deck | plan | 25 light slides and the dark closing, as chapters 1-5 |

## The undergraduate's read-through (contact sheets rendered with LibreOffice, slides 6, 7, 8, 9, 11, 15, 16, 19, 22, 23)
- FOUND and fixed: on four slides the one-line lede ran into the console label beneath it (slides 7, 16, 22, 23),
  and on three story slides the last beat sat on the console label; the ledes were shortened to one line, the
  consoles moved down, and the build now refuses an item that starts under a lede. The chips row of slide 7 wrapped
  under the takeaway strip and was cut to three chips; the chips of slides 8 and 20 likewise.
- Slide 8 (the outpoint read both ways round) is the one that settles the byte-order confusion: the reversed
  string in the second console equals the identifier the library computes in the third line, so the reversal is
  not a convention to memorise but a check to run.
- Slide 18 is the whole chapter in two booleans: `(True, False)` - the same transaction with a different witness
  keeps its txid and changes its wtxid. A reader who understands that line understands why Mt. Gox's claim on the
  next slide was a claim about the legacy format.
- Slide 23 ends on 569 three ways, the third being the explorer's record rather than a node's, and the lede says
  why; this is the honest replacement for the chapter-5 move of matching Bitcoin Core's own output.
- The fact rows truncate the WHO and WHERE cells at this width, as on chapters 1-5; the notes carry the full text.
