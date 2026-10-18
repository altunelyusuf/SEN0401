# Chapter 3 deck 2.3.0 - review (2026-10-19)

New version of deck 2.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 3` from `deck_plan_v2_3_0.json` with the plan patch `deck_patch_v2_3_0.py`. Nothing committed was edited; the corrected date of the first release (8 January 2009) and every link label that stays are kept.

## Before (deck 2.2.0): deck_check, structure, fit, picture, honesty, lookfeel PASS; links FAIL (the 2014 Bitcoin Foundation post, via web.archive.org, which is blocked here), story FAIL (three stories without ISO dates for two of them and without pictures), arc FAIL (slide 14 without a picture; no standards group, no community group, no video).

## What changed
- `sen0401_ch03_stories_v1_2_0.py`: ISO dates 2014-04-07 (Andresen stepped down and named van der Laan, per the Bitcoin Wiki page that quotes his post of that date), 2009-01-08 (version 0.1), 2021-09-13 (Bitcoin Core 22.0, the first Guix-built release, read on bitcoincore.org); real names (Satoshi Nakamoto, Gavin Andresen, Wladimir van der Laan, Carl Dong), bios, pictures with credit.
- Pictures (`ASSETS_PROVENANCE_v1_1_0.md`, sha256 per row): Gavin Andresen at Web Summit 2014 (Stephen McCarthy, CC BY 2.0); bust of Satoshi Nakamoto, Budapest (Fekist, CC BY-SA 4.0); the GNU Guix logo (author GNU Guix, public domain text logo; replaces the project's own icon on slide 10, which is MIT licensed and therefore cannot be the story's picture).
- Link: the web.archive.org copy of the 2014 post is replaced by the Bitcoin Wiki page on Wladimir van der Laan (reachable), whose text carries the same fact and cites the post.
- Resources slide: groups Read (the history rows joined it), Verify & build (the RPC reference joined it), Standards and papers (BIP 1, the white paper), Community (Bitcoin Core PR Review Club, Delving Bitcoin, the bitcoin-dev list, Stack Exchange), Watch ("Tracing Bitcoin Core v23.0" as `https://www.youtube.com/embed/XuRnL393pSk`; oEmbed title read: "Tracing Bitcoin Core v23.0"). Every earlier link is still there; "Checked" now says 2026-10-19.
- Layout: story slides 6, 10 and 14 re-spaced; fact rows are full width.

## Status after (`sen0401_deck_nine_v1_0_0.py 03 --fixtures`; lineage `Deck/Ch03`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- Andresen's original post (bitcoinfoundation.org) cannot be read from here; the story's date rests on the Bitcoin Wiki page's statement of 7 April 2014 and Wikipedia gives 8 April for the day van der Laan took over. The Bitcoin Wiki date is used.
