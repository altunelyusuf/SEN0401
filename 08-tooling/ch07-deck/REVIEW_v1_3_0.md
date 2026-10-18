# Chapter 7 deck 1.3.0 - review (2026-10-19)

New version of deck 1.2.0, built by `sen0401_deck_rebuild_v1_1_0.py 7` from `deck_plan_v1_3_0.json` with the plan patch `deck_patch_v1_3_0.py`. Nothing committed was edited.

## Before (deck 1.2.0): deck_check PASS, fit FAIL (overflows and overlaps), links PASS, story FAIL (the read link's host mempool.space on no slide), arc FAIL (no community group, no watch group, no video). Structure, picture, honesty and lookfeel PASS.

## What changed
- Geometry: console and program labels shortened so that their captions share the label row, long titles shortened, code boxes placed clear of what is above them; the fit check is clean.
- `sen0401_ch07_stories_v1_2_0.py`: bios added; the Schnorr credit shortened ("Claus-Peter Schnorr, 1986 - Konrad Jacobs, CC BY-SA 2.0 de") so that it fits under its picture. The pictures are unchanged (bust of Satoshi Nakamoto, Fekist, CC BY-SA 4.0; a bitcoin mining farm, Marko Ahtisaari, CC BY 2.0; Claus-Peter Schnorr, Konrad Jacobs, CC BY-SA 2.0 de); their rows in `ASSETS_PROVENANCE_v1_0_0.md` already carry the sha256.
- Fact rows of the three story slides are full width, which prints the read link's host (mempool.space on slide 22).
- Resources slide: Tools merged into "Read and explore"; a Community group (Stack Exchange, Delving Bitcoin) and a Watch group with two Bitcoin Optech workshop videos as embed URLs: `https://www.youtube.com/embed/wybiVFdknhg` (oEmbed title read: "Schnorr - Bitcoin Optech Taproot and Schnorr Workshop (1.1)") and `https://www.youtube.com/embed/nXGe9_M5pjk` (oEmbed title read: "Tapscript - Bitcoin Optech Taproot and Schnorr Workshop (2.3)"). "Checked" says 2026-10-19.
- Page chain: `ch07-page/lecture_v1_2_0.json` and `ch07-page/stories_img_v1_1_0.json`.

## Status after (`sen0401_deck_nine_v1_0_0.py 07 --fixtures`; lineage `Deck/Ch07`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason.

## Not done
- Nothing fails. The mining-farm photograph is a general view of 2014 hardware, not of the 2015 pools; the credit says so.
