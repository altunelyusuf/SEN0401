# Chapter 4 deck 3.3.0 - review (2026-10-19)

New version of deck 3.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 4` from `deck_plan_v3_3_0.json` with the plan patch `deck_patch_v3_3_0.py`. Nothing committed was edited.

## Before (deck 3.2.0): links FAIL (learnmeabitcoin.com keys guide answers 403), story FAIL (three stories without a licence-clear picture, credit and ISO date), arc FAIL (slides 12 and 17 incomplete; no watch group, no video). Others PASS.

## What changed
- `sen0401_ch04_stories_v1_2_0.py`: ISO dates, 5N1K fields, pictures and credits for the three stories. Diffie and Hellman: 1976-06-03, the manuscript-received date read in the Stanford PDF (the November issue date stays in the story text). Base58Design: 2009-01-08, the announcement of version 0.1 (the day the memo was written is not recorded). Bitcoin Eater: 2026-10-06, the day of the live fetch.
- Pictures (`ASSETS_PROVENANCE_v1_1_0.md`, sha256 per row): Whitfield Diffie, 2017 (Duncan Hull, CC BY-SA 4.0, a 500 px copy of Commons File:Whitfield Diffie Royal Society.jpg, which replaces the unusable GFDL composite on slide 6); bust of Satoshi Nakamoto, Budapest (Fekist, CC BY-SA 4.0); Bitcoin logo (Grayliptrot, public domain, a stand-in: an address has no picture).
- Layout: slides 6, 12, 17 give the picture room beside the text; the fact rows run full width; slide 22's second console keeps its earlier geometry.
- Links: learnmeabitcoin.com keys guide (403) -> Bitcoin Wiki "Technical background of version 1 Bitcoin addresses" (label changed). Watch group: "Elliptic Curves - Computerphile" as `https://www.youtube.com/embed/NF1pwjL9-DE` (oEmbed title read). The "Checked" date on the resources slide is 2026-10-19.
- Page chain: `ch04-page/lecture_v1_3_0.json`, `ch04-page/stories_img_v1_1_0.json`.

## Status after (`sen0401_deck_nine_v1_0_0.py 04 --fixtures`; lineage `Deck/Ch04`: PASS)
All nine checks PASS; every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- The Bitcoin logo and the Satoshi bust are stand-ins.
