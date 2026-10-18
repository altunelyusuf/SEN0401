# Chapter 6 deck 1.3.0 - review (2026-10-19)

New version of deck 1.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 6` from `deck_plan_v1_3_0.json` with the plan patch `deck_patch_v1_3_0.py`. Nothing committed was edited.

## Before (deck 1.2.0): deck_check PASS, fit FAIL (5 overflows and many overlaps), links FAIL (1: learnmeabitcoin.com answers 403), story FAIL (all four stories without a picture), arc FAIL (slide 19 without a picture; no watch group, no video). Structure, picture, honesty and lookfeel PASS.

## What changed
- Geometry: console and program labels shortened so that their captions share the label row, long titles shortened, code boxes placed clear of what is above them by `sen0401_deck_geom_v1_0_0.py`; the fit check is clean.
- `sen0401_ch06_stories_v1_2_0.py`: pictures and credits added to the four stories, bios added; the Mt. Gox story's source now names its stand-in picture.
- Pictures (`ASSETS_PROVENANCE_v1_1_0.md`, sha256 per row): Hal Finney, 1972 (Daily News-Post, public domain); the plaque at Papa John's, Jacksonville (Sanjev Rajaram, CC0); the bust of Satoshi Nakamoto, Budapest (Fekist, CC BY-SA 4.0, copy of the chapter 7 asset: it replaces the Andresen photograph on the value-overflow slide, because Satoshi wrote the patch; it is also the credit the fixtures tool needs to make stale_credit and stale_date); the Mt. Gox logo (author not recorded on Commons, public domain text logo, a stand-in).
- Links: learnmeabitcoin.com transaction guide (403) -> Bitcoin Wiki "Transaction" page (label changed). Watch group: "Blockchain tutorial 26: Bitcoin transaction" as `https://www.youtube.com/embed/PrcJD4rznyA` (oEmbed title read; Mobilefish.com). The "Checked" date on the resources slide is 2026-10-19.
- Page chain: `ch06-page/lecture_v1_2_0.json` and `ch06-page/stories_img_v1_1_0.json` (the story check requires the page's story pictures file to name the same files).

## Status after (`sen0401_deck_nine_v1_0_0.py 06 --fixtures`; lineage `Deck/Ch06`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- The Mt. Gox logo and the Satoshi bust are stand-ins for the event and the patch author; no free photograph of either exists.
