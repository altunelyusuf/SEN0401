# Chapter 7 deck v1.0.0 - the three-role review record

Same method as chapters 1-6; first cycle over the chapter-7 classroom deck (26 slides), drawn by the shared renderer
(CME materials standard v1.0.0). Built under the notes standard of 2026-10-08 (reader's prose, no presenter labels;
`deck_notes_check_v1_0_0.py` run on the finished file). Built on 2026-10-08 without a Bitcoin Core node: every
spend on the slides runs in this course's own stdlib-only Python port of Bitcoin's script interpreter
(`sen0401_ch07_script_lib_v1_0_0.py`), which `sen0401_ch07_verify_v1_0_0.py` checks against Core's script_tests
(1,237 of 1,237), the sighash tests (500 of 500), the BIP341 vectors and every input of block 775,072 (1,022 of 1,022
accepted, 6 of 6 tampered inputs rejected). The slides say that no node was available.

## The academician's build notes
- Arc: scripts and the stack (a script run on a stack; a key-hash output spent, then broken twice; the OP_RETURN bug of
  2010 as a model of the joined script against today's engine) -> signatures, multisig and script hash (strict DER and
  the padded signature that passes without DERSIG; the 2015 fork; 2-of-3 in key order and the NULLDUMMY rule; the P2SH
  output, address and redeem script) -> time and flow control (OP_CHECKLOCKTIMEVERIFY and OP_CHECKSEQUENCEVERIFY on real
  spends, with the off-by-one of the lock time computed; the book's three-path company script spent through each path)
  -> witness programs and script trees (P2WPKH native and nested; the census of the 1,022 inputs of block 775,072 as a
  native chart; a Merkle tree of the three paths and the proof length for 3 to 1,048,576 scripts as a native chart) ->
  taproot and tapscript (output key and key path of 308 weight units; the script path of three leaves at 577, 617 and
  414 units against 585, 584 and 509 for the same contract as P2WSH, as a native chart; OP_CHECKSIGADD at 104 bytes
  against 105; the 87 OP_SUCCESS values).
- Three 5N1K stories with fact rows, live links and licensed photographs: the OP_RETURN bug of 28 July 2010
  (CVE-2010-5141; the bust of Satoshi Nakamoto in Budapest, CC BY-SA 4.0, Fekist); the strict-DER fork of 4 July 2015
  (a bitcoin mining farm, CC BY 2.0, Marko Ahtisaari, said on the page to be a general view and not of the 2015 pools); and
  the road from a patented signature to the taproot soft fork of 14 November 2021 (Claus-Peter Schnorr, Oberwolfach,
  1986, CC BY-SA 2.0 de, Konrad Jacobs). Chapter 6's four stories are not repeated.
- Everything executed: 17 consoles under Python 3.14.6 from `examples_v1_0_0.py` (16 groups, one per concept of the
  taxonomy), re-run off the finished file by `deck_check_v1_0_0.py`; the three charts take their series from the
  executed `BlockCensus`, `Mast` and `ScriptPathSpending` groups, and the build asserts them.
- Five book figures are used (mbc3_0701 on the title slide, 0702, 0703 and 0710 on section slides, 0705 on a content
  slide), each with its credit on the slide.
- Where the book and the sources differ, the slides show the computed fact: a lock time of 800,000 is first final in a
  block of height 800,001 (Core's IsFinalTx), which is stated on the timelock slide.
- The model on the OP_RETURN slide (`old_joined`) is a model of version 0.3.0's behaviour, labelled as such; the real
  0.3.0 source is saved in `ch07-evidence` and linked on the resources slide.

## The expert reviewer's checklist and findings
| check | command | result |
|---|---|---|
| Numbered slides, 20-26; warm-ivory; agenda with exact ranges; summary; takeaway strips | `python3 deck_build_v1_0_0.py` | 26 slides; agenda ranges 3-4, 5-7, 8-12, 13-15, 16-18, 19-26 computed by the build; 15 content slides carry a takeaway, the three story slides and the questions slide carry their own rows |
| Full sentences on slides; no bare code or numbers | build gates (lede <= 34 words, takeaway <= 24 words) and the contact sheets | pass: every console has a label line naming what it shows and a run-under caption |
| Every example executed, result shown; charts native with data labels, series from executed examples only | `python3 examples_run_v1_0_0.py /root/.local/bin/python3.14 examples_out_v1_0_0.json` -> 16 groups; `python3 deck_check_v1_0_0.py sen0401_ch07_deck_v1_0_0.pptx` | **45 examples re-run on 26 slides; 0 mismatch(es)**; 3 native charts (ppt/charts) with data labels; the build asserts the series against the parsed outputs (census sums to 1,022; weights [577, 617, 414] and [585, 584, 509]; proof lengths [2, 3, 10, 20]) |
| The check can fail | `python3 fixtures_make_v1_0_0.py sen0401_ch07_deck_v1_0_0.pptx fixtures` then `python3 deck_check_v1_0_0.py fixtures/fixture_stale_expr_v1_0_0.pptx` | fixture written from 2 slides; **2 mismatches, exit 1** (the key path weight 308 edited to 309 on slides 20 and 22 is refused) |
| Code never wraps; width AND height gates | `code()` in the build refuses a console under 7 pt | pass: the smallest console sets at 7.2 pt (slide 10, the DER fork); the next at 7.6 pt |
| Layout: no overflow, nothing outside the slide, notes on every slide | `python3 ../deck_layout_check_v1_0_0.py sen0401_ch07_deck_v1_0_0.pptx` | **clean** (0 overflowing frames, 0 shapes outside, 0 slides without notes) after five rounds: 29 items at the first run (long subtitles, labels and takeaways, chips rows that wrapped, a title too long for the title slide, link rows) were shortened or rebuilt |
| Speaker notes are reader's prose | `python3 ../deck_notes_check_v1_0_0.py sen0401_ch07_deck_v1_0_0.pptx` | **26 slides, 26 with notes written for the reader; VERDICT: PASS**; notes average 156 words (62 to 308); the build refuses a directive label before rendering |
| Stories 5N1K; licences on-slide and in ASSETS_PROVENANCE | `python3 ../sen0401_ch07_stories_v1_0_0.py` | 3 stories; self-check failures: 0; three photographs credited on the slide and in `03-materials/ch07/assets/ASSETS_PROVENANCE_v1_0_0.md` |
| Resources slide with live links | links group on slide 25 | 11 links, every one also in `ch07-page/resources_v1_0_0.json`, whose 34 entries answered 200 on 2026-10-08 (GitHub HTML is not reachable from this session, so raw.githubusercontent.com is linked; the chapter itself and Bitcoin Core's interpreter are on the page's resource list and not on the slide, because their long addresses did not fit a line) |
| No dark/light switching mid-deck | plan | 25 light slides and the dark closing, as chapters 1-6 |

## The undergraduate's read-through (contact sheets rendered with LibreOffice, slides 1-8, 10, 14, 17-26)
- FOUND and fixed: the third beat of two story slides ran into the console label beneath it (slides 7 and 22) and the
  console caption was hidden behind the fact row (slides 7, 10); beats were shortened, consoles moved, the fact row
  lowered. On slide 14 the chips ran under the takeaway strip and were removed; on slide 21 two chips wrapped and became
  two bullets. On slide 18 the figure's caption sat on the console label; the figure was made smaller and the console
  shortened to a one-line proof expression. On the section slides the image overlapped the title and the subtitle;
  the images were lowered and the subtitles shortened. The questions slide had cut each question at its first comma
  ("How do lock time?"); it now shows the seven questions in full.
- Slide 6 is the one that makes the chapter concrete: the same 25-byte lock is spent with a real signature, then
  refused for a wrong key and for an amount changed after signing, so "authorization" is something a reader can break.
- Slide 14 shows the one place where the book and Bitcoin Core differ by a block, as a computed pair (False, True).
- Slide 21 shows that revealing a script costs about what the old P2WSH script cost (577 against 585, 617 against 584,
  414 against 509) while the key path of the same output weighs 308.
- The fact rows truncate the WHO and WHERE cells at this width, as on chapters 1-6; the notes carry the full text.
- Not checked in PowerPoint itself: the contact sheets are LibreOffice renderings (fonts substitute for Cambria and
  Calibri), and only 20 of the 26 slides were looked at.
