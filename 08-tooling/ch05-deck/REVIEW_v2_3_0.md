# Chapter 5 deck 2.3.0 - review (2026-10-19)

New version of deck 2.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 5` from `deck_plan_v2_3_0.json` with the plan patch `deck_patch_v2_3_0.py`. Nothing committed was edited.

## Before (deck 2.2.0): deck_check FAIL (recorded under Python 3.14.4, the interpreter is 3.14.6), fit FAIL (15 or more overlaps), links FAIL (2 links), story FAIL (three stories without pictures, one without a name), arc FAIL (slide 18 without a picture; no watch group, no video). Honesty, structure, picture and lookfeel PASS.

## What changed
- The examples were re-recorded under Python 3.14.6 (`examples_v1_1_0.py`, `examples_out_v1_1_0.json`; every output equals the 3.14.4 recording) and the captions retagged.
- Geometry: shortened console and program labels so that their captions share the label row, and `sen0401_deck_geom_v1_0_0.py` places each code box clear of what is above it; the fit check is clean.
- `sen0401_ch05_stories_v1_2_0.py`: ISO dates 2021-01-12, 2013-09-10, 2014-03-21; real names (Stefan Thomas, Nathaniel Popper, Marek Palatinus, Pavol Rusnak, Aaron Voisine, Sean Bowe, Mark Karpeles, Simon Sharwood); bios; pictures with credit. The IronKey story no longer says "animated" (no source read says it; the 2011 reward was a video explaining bitcoin) and the Mt. Gox story now follows The Register's report of the statement (old-format wallets thought empty, one held 200,000 BTC).
- Pictures (`ASSETS_PROVENANCE_v1_1_0.md`, sha256 per row): Stefan Thomas (Lift Conference, CC BY 2.0), Trezor One devices (Gage Skidmore, CC BY-SA 3.0), the Mt. Gox logo (author not recorded on Commons, public domain text logo).
- Links: nytimes.com (403) -> the New York Times article's opening as republished by Business Standard (labelled "NYT via Business Standard"); learnmeabitcoin.com HD wallets (no connection) -> the Bitcoin Wiki page on deterministic wallets (label changed). Watch group: "BIP-39 mnemonic words" as `https://www.youtube.com/embed/hRXcY_tIlrw` (oEmbed title read: "Blockchain tutorial 28: Bitcoin Improvement Proposal 39 (BIP-39) mnemonic words", Mobilefish.com).

## Status after (`sen0401_deck_nine_v1_0_0.py 05 --fixtures`; lineage `Deck/Ch05`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- Business Standard shows only the opening of Popper's article; the 2011 video reward is in Finance Magnates (named in the story's source), not on the linked page.
- The Mt. Gox logo is a stand-in for the event.
