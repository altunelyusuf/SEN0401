# Chapter 2 deck 2.3.0 - review (2026-10-19)

New version of deck 2.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 2` from `deck_plan_v2_3_0.json` with the plan patch `deck_patch_v2_3_0.py`. Nothing committed was edited.

## Before (deck 2.2.0): deck_check, structure, fit, picture, honesty, lookfeel PASS; links FAIL (the YouTube watch URL answers 429), story FAIL (no picture, three stories), arc FAIL (slides 6 and 21 without a picture; no seminal/standards group on the resources slide).

## What changed
- `sen0401_ch02_stories_v1_2_0.py`: each of the three stories has an ISO date (2008-10-31, 2010-06-11, 2010-08-15), real names (Satoshi Nakamoto; Gavin Andresen; Jeff Garzik), a picture with credit and a bio. The faucet story's source named bitcointalk topic 141; the thread the deck links is topic 183 (read: posted 11 June 2010, 1,100 BTC, five per customer), so the source now says 183.
- Pictures (`ASSETS_PROVENANCE_v1_1_0.md`, sha256 per row): bust of Satoshi Nakamoto, Budapest (Fekist, CC BY-SA 4.0, copy of the chapter 7 asset); Gavin Andresen at Web Summit 2014 (Stephen McCarthy, CC BY 2.0); the Bitcoin logo (Grayliptrot, public domain) as an announced stand-in for the value overflow, for which no free photograph exists.
- Resources slide: a "Seminal papers" group (the white paper, Back's Hashcash paper from the Satoshi Nakamoto Institute's copy) and the video as `https://www.youtube.com/embed/bBC-nXj3Ng4` (oEmbed title read: "But how does bitcoin actually work?", 3Blue1Brown). The "Checked" date on the slide is 2026-10-19, the day the links were opened.
- Layout: story slides 6, 12 and 21 re-spaced; fact rows are full width so the read link's host is printed.

## Status after (`sen0401_deck_nine_v1_0_0.py 02 --fixtures`; lineage `Deck/Ch02`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- Nothing fails. The bust stands for the author of the white paper (whose face is unknown) and the Bitcoin logo for the overflow: neither shows the event.
