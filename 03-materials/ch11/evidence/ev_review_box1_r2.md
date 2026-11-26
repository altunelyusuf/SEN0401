# Independent review 2, SEN0401 chapter 11, lineage 7 box 1
Deck 2.7.0 (43 slides), page 9.101.0. Read-only review under REVIEW_BRIEF_r2. Method: python-pptx for all notes and slide text of ch11 and of the newest deck of each other chapter (ch01 v3.7.0, ch02 v3.3.0, ch03 v3.3.1, ch04 v3.9.0, ch05 v3.8.0, ch06 v2.5.0, ch07 v2.7.0, ch08 v2.5.0, ch09 v2.2.0, ch10 v2.4.0, ch12 v3.1.0, ch13 v2.5.0, ch14 v2.2.0); text search of the page file and of the evidence logs. ev_review_box1.md was not opened.

All 43 notes are 80 to 139 words (opening/closing/divider within 30 to 140), no presenter directions, no "think of", no analogy found. Sentences that ask the reader to retell or compare (slides 3, 10, 16, 19) were treated as allowed.

## Check 1, notes teach (slides 3, 10, 11, 16, 17, 19, 20, 26, 35, 38)

| Slide | Academician | Undergraduate | Why |
|---|---|---|---|
| 3 | yes | yes | Seven questions each mapped to a named slide; complete. |
| 10 | yes | yes | Defines child block, block, header hash and says which example shows each. |
| 11 | yes | yes | Time field, median time past, bits vs difficulty and the four result values are all stated. |
| 16 | yes | yes | Hash once vs twice, what the first digits show, why the name is never stored. |
| 17 | NO | NO | See defect 1. |
| 19 | yes | NO | See defect 3. |
| 20 | yes | yes | Divider; three columns tied to examples 9 to 12 and the patent story. |
| 26 | yes | NO | See defect 2. |
| 35 | yes | yes | Prefixes and version bytes of all five chains, and why a wrong-chain address is refused. |
| 38 | yes | yes | Signet, challenge, 1-of-2 multisig, magic bytes, Core 0.21.0 and the dated height. |

Defect 1 (slide 17, both readers): the note says that the coinbase script starts with the height and that maturity is 100, but never says why the height is put there (so that no two coinbases can be equal, the point of slide 14 and of the chapter's new story). It also does not say why the eight heights 1, 16, 17, 127, 128, 255, 256, 500 were chosen (the encoding changes between 16/17, 127/128 and 255/256) or how a height is packed into script bytes. A reader could repeat the result but not teach the reason. The note links forward to slide 19 only and not back to slide 14.

Defect 2 (slide 26, undergraduate): the note states that repeating the last two ids gives the same root, but not why (an odd level is completed by repeating its last hash, so the copy hashes to the same parent). It points to "the padding rule on slide 22" instead of saying it. The note also moves from six ids (slide code) to a block of three transactions mutated to four (Core result) without saying that both are the same rule.

Defect 3 (slide 19, undergraduate): the note names the Poisson distribution and "adding these chances" but does not state the sum (terms for k blocks found, 1 if the attacker has already reached z, otherwise (q/p) to the power z minus k). An undergraduate can repeat 1.0, 0.2045873, 0.0509779, 0.0002428 but cannot reproduce them from the note.

## Check 2, no story repeated

Searched notes and slide text of the 13 other chapters' newest decks, and the ch11 page, for the four stories (Merkle 1982; blocks 91722-91880 coinbases; Lopp/Jahr testnet griefing; Alm/Towns signet).
- Merkle: ch02 (slides on merkle tree), ch03 (example on block 123,456), ch10 (light client Merkle path), ch12 (merkle root rule, extra nonce), ch13 (header fields) mention the tree as a concept or code example. No other chapter mentions Merkle the person, the patent, Stanford or 1982 as Merkle (ch01's 1982 is Chaum and the Byzantine generals; ch04's Stanford is Diffie and Hellman). Counted as mentions of a fact, not retellings.
- Repeated coinbases: ch12 names BIP 34 (height push, "makes every coinbase different", first soft fork by version counting, activation height 227,931). Counted as a fact, not a retelling: no blocks 91722 to 91880, no November 2010, no duplicate-identifier event. No other chapter mentions BIP 30 or the four blocks.
- Testnet griefing: ch12 mentions testnet4 and BIP 94 as a retarget-code branch (a code example). No Lopp, no Jahr, no testnet3 block storm. Counted as a mention.
- Signet: no mention of signet, BIP 325, Alm or Towns in any other chapter.
- Inside ch11: each story is told once in the deck (slides 14, 25, 33, 38) and once as a story card on the page (4 cards). Deck-to-page is the same material in two media, not a repeat. Slide 3 and 42 only name them.
- Genesis headline: told in ch01 slide 7 (Nakamoto, 3 January 2009, the headline, why it dates the block). In ch11 it is on slide 6 (a concept card), slide 12 (a Nakamoto card), slide 13 (code example 4: message, ten zeros, time field) and on the page as concept sections (GenesisCoinbaseMessage, a "Chancellor of the headline" section with Alistair Darling's term, the byline constant in code frames). I do NOT count this as a retelling: each place states a fact of the header or runs code, and none of them tells the event as a story (who mined it, why he wrote it, what it answers). One caution only: the page definition "which proves that the block was not made earlier" repeats the point of ch01's story in one clause; I count it as a fact, not a story.

Result: no story appears twice. Repeats found: 0.

## Check 3, evidence files

All five files say, in the header, "deck 2.7.0" and "page 9.101.0" with the file paths and sha256 prefixes d84d71ec99ad0ff2 (deck) and 774c05bd74e124f5 (page); the page-test log also says "page 9.101.0 (deck 2.7.0)".
- ev_material_check_v1_3_0_deck_2_7_0.log: 9 checks all PASS, "failed: 0". Agrees with the claim.
- ev_deck_standard_deck_2_7_0.log: D1 to D12 all PASS, "PASS=12 FAIL=0". Agrees.
- ev_page_test_9_45_0_page_9_101_0.log: "widgets: 91 tested, 91 passed; failing: []", "failed: 0". Agrees.
- ev_code_frames_run_deck_2_7_0.log: 74 "ok" lines over 17 examples, last line "examples 17 shown results 74 failures 0", RESULT PASS. Agrees. Remark only: the manifest named in the last line records deck 2.5.0 and the header says it is unchanged by 2.7.0, which is stated openly in the header.
- ev_verify_v1_0_2_deck_2_7_0.log: "failures: []". Agrees.
No file fails to name the versions. (ev_links_deck_2_7_0.log, not asked for, also names deck 2.7.0 and shows 200 for the three links of slide 14.)

## Check 4, the new story (slide 14 and the first story card of the page)

- Helps to understand the reason for the height in the coinbase: yes. Slide 14 states the problem (two equal coinbases cannot be told apart because a transaction is named by the hash of its bytes), the rule (BIP 30) and the fix (BIP 34 height first, "put the height in the coinbase and no two coinbases can be equal"). The note on slide 14 points forward to slide 17. The reverse link is missing (see defect 1).
- 5N1K with real names: yes. Real names and facts that I checked against the saved explorer data: blocks 91812 at 2010-11-14 17:59 UTC, 91842 at 21:04 UTC, 91722 on 14 November, 91880 on 15 November 00:36 UTC; ids d5d27987 and e3bf3d07; Pieter Wuille (BIP 30), Gavin Andresen (BIP 34, page). The slide names only Wuille by implication (the slide text says "BIP 30 (2012)" and the note does not name him; the names appear on the page). The miners are honestly said to be unrecorded.
- Real free picture with credit: yes, with a limit. Bitcoin-qt 0.5.2 screenshot, "the Bitcoin developers, MIT, Wikimedia Commons", labelled "Stand-in picture: the client of February 2012". It is real, free and credited, but it does not show the event (none exists); the label says so.
- Live link: yes. https://bips.dev/30/ returns 200, as do the explorer link and the picture page (ev_links_deck_2_7_0.log).
Defect 4 (date inconsistency, page and deck): the page story card says "Ralph Merkle patented the hash tree in 1979" and the same text says the patent was published on 5 January 1982; a page paragraph also says "Merkle's work of 1980" and a concept example says "patented in 1979 (US patent 4309569 of 1982)". Slide 25 says more carefully "the hash tree dates from 1979; patent published 1982". "Patented in 1979" (filing year) against "published 1982" is not wrong but is stated as a grant in 1979 and will confuse a reader; the page should say "filed" or "dates from 1979".
Defect 5 (slide 14 note names no person): the story card of slide 14 says who wrote the BIPs only on the page; the slide and its note name no person at all (BIP 30 is credited to Wuille and BIP 34 to Andresen only on the page). The brief asks for real names in the story; the deck story has none besides the block numbers.

DEFECTS FOUND: 5
1. Slide 17 note does not teach the reason for the height in the coinbase (nor why those eight heights, nor the encoding) and has no link back to slide 14; fails for both readers.
2. Slide 26 note does not explain why a repeated last hash gives the same root; fails for the undergraduate.
3. Slide 19 note does not state the catch-up sum; fails for the undergraduate.
4. Page: Merkle "patented in 1979" against patent published 1982 (and "work of 1980") is inconsistent with slide 25.
5. Slide 14 and its note name no person (Wuille, Andresen appear only on the page).
