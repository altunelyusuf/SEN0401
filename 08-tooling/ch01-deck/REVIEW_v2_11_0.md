# Chapter 1 deck 2.11.0 - review (2026-10-19)

New version of deck 2.10.0, built by `sen0401_deck_rebuild_v1_1_0.py 1` from `deck_plan_v2_11_0.json` with the plan patch `deck_patch_v2_11_0.py`. Nothing committed was edited.

## What changed
- Stories: `sen0401_ch01_stories_v1_6_0.py` gives each of the nine stories an ISO date, a who with real names, a where of three words or more, a story of three sentences or more (what, why, how), a licence-clear picture with its credit, and a read link that answers here. The slide of each story shows the picture with that credit and the ISO date in its fact row; the page's `stories_img_v1_1_0.json` names the same files.
- Pictures added (all in `03-materials/ch01/assets`, rows with sha256 in `ASSETS_PROVENANCE_v1_3_0.md`): David Chaum 2018 (Harry Murphy / Web Summit, CC BY 2.0), Mt. Gox logo (author not recorded on Commons, public domain text logo), Hal Finney 1972 (Daily News-Post, public domain), Papa John's plaque (Sanjev Rajaram, CC0), Fedorov (U.S. Embassy Kyiv, public domain; a 720 px copy, because the deck's case card already uses the original and a deck may not carry one file twice). The other stories keep their pictures (rai stone, Cleveland stater, PayPal logo, genesis hex dump) with new short credits.
- Links: sec.gov (PayPal S-1), cnbc.com, coingecko.com and web.archive.org answer 403 or no connection here. Replaced by reachable pages of the same resource or event: PayPal story -> encyclopedia article on PayPal; Ukraine story and card -> CNBC's own article of 2022-03-03 as republished at nbclosangeles.com (the first CNBC article is not republished there; this one is the same reporter's report of the donations); CoinGecko price page -> CoinGecko's own data feed (api.coingecko.com); Hashcash and b-money -> the Satoshi Nakamoto Institute's copies (cdn.nakamotoinstitute.org); the YouTube watch link -> its embed URL (oEmbed title read: "But how does bitcoin actually work?", 3Blue1Brown). Labels are kept where the resource is the same; four were changed because the host or the resource changed.
- Layout: story slides 8, 9, 11, 12, 15, 16, 23 and 34 re-spaced for the pictures and a full-width fact row (the row prints the read link's host only when it has the width).

## Status after (`sen0401_deck_nine_v1_0_0.py 01 --fixtures`; lineage `Deck/Ch01` with `sen0401_lineage_chapter_check_v1_2_0.py`: PASS)
All nine checks PASS and every fixture, including stale_credit and stale_date, is refused for its own reason. The links check depends on live hosts: it failed once of five runs on one link that answered on the next run.

## Not done
- The PayPal Form S-1 of 2001 (sec.gov, 403) has no reachable copy: no mirror other than web.archive.org, which is blocked here.
- The `genesis_hexdump.png` licence (CC BY 4.0, the course's own licence under Yusuf Altunel) is the course's declaration, not a third party's; the owner may want to confirm it.
- The StoneMoney date is the release date of the free ebook (2024-01-30), the only day-precise date of that story; the visit (1903) is in the subtitle.
