# Review 4, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent, files read only. Deck 2.7.0 (43 slides) and page 9.101.0 read with python-pptx and a text dump. Other chapters: newest deck of each of chapters 01-10 and 12-14 (01 v3.7.0, 02 v3.3.0, 03 v3.3.1, 04 v3.9.0, 05 v3.8.0, 06 v2.5.0, 07 v2.7.0, 08 v2.5.0, 09 v2.2.0, 10 v2.4.0, 12 v3.1.0, 13 v2.5.0, 14 v2.2.0). The earlier reviews were not read.

## Check 1, notes teach (13 slides: 2, 3, 11, 13, 14, 17, 19, 20, 26, 28, 36, 40, 43)

All 13 notes are within 60-140 words (30-140 for slides 2, 20, 28, 43 as opening, divider and closing), contain no presenter direction and no "think of". The sentences "try each question", "say each claim aloud", "retell", "compare", "connect with" are reader directions and are allowed.

| Slide | Academician | Undergraduate | Why |
|---|---|---|---|
| 2 | yes | yes | Route and counts are all in the note. Defect D5 (consistency), not a teaching no. |
| 3 | yes | yes | All seven questions point to the right slides (9; 16-17; 18; 22; 24; 30-40; 32-33; 41), checked against the slide titles. |
| 11 | yes | NO | The note says "the easiest target has 224 bits" and "bits is a compact form of the target" but never says what is packed (exponent and mantissa) or why the easiest target is 224 bits long, so a reader cannot explain the 224 or the 1,180,923,195 (D1). |
| 13 | yes | yes | Headline, 69 characters, ten leading zeros, proof of work and the time field are all explained. |
| 14 | NO | NO | The note gives the events and the two BIPs but never says why the two coinbases were identical (nothing in a coinbase differs between blocks) and never says what the harm was (the later coinbase replaced the earlier one among the unspent outputs, so the earlier 50 coins were lost). It also says Core "lists the earlier two blocks as unspendable", which is wrong: Core lists the later two as exceptions (D2). |
| 17 | yes | yes | Encoding of 1-16 as an opcode, the length byte, little-endian, the 128 border and the 99/100 maturity result are all there. The little-endian detail is dense for a beginner but is stated. |
| 19 | yes | NO | The catch-up formula is given only in words: "a Poisson chance of mean z times q over p" is not explained, nor why one minus the sum is the answer. An undergraduate cannot teach it from the note (D4). The four result values are correct (they equal the white paper's table for q = 0.1). |
| 20 | yes | yes | Divider; previews the three columns, names the 1982 patent on slide 25, ends on what the header commits to. |
| 26 | yes | yes | The odd-level padding rule and the bad-txns-duplicate verdict are explained. Nit, not counted: "a list that already repeats its last ids, as the six transactions here become eight" is awkwardly worded. |
| 28 | yes | yes | Divider; the five chains, the three columns and "same rules, other constants" are stated. |
| 36 | yes | yes | Defines the three cards and the four magic bytes; 71 bytes is correct (1 + 34 + 34 + 1 + 1). |
| 40 | yes | yes | Halving at 150, the six heights and values, and the record of 500 blocks are covered. |
| 43 | yes | yes | Four claims with slide ranges (7-16, 18-19, 22-27, 30-40), all consistent with the slide titles. |

Nos: slide 11 undergraduate; slide 14 academician and undergraduate; slide 19 undergraduate.

Slide 2 (D5): the slide's subtitle says "Three parts", yet four numbered items are listed (the first is "Questions and the chapter map"), and the note uses the word "box" ("A first box covers ...") without saying what a box is. Slide 4 says "three parts".

## Check 2, no story repeated

Searched notes and slide text of all 13 other decks and the whole page text (stories, concept bodies, questions, sources) for the four stories.

Counted as a retelling (event told as a story): none outside chapter 11.
Counted as a mention, a fact or code (not a retelling):
- Merkle tree: ch2, ch3, ch7, ch10, ch12, ch13 define the tree, root and path and show code. Nobody tells Merkle, the 1979 tree or patent 4,309,569. Ch4 (Diffie and Hellman at Stanford, 1976), ch8 (Schnorr patent 1991; Shamir 1979) and ch13 (Shamir 1979) are different events.
- Coinbases mined twice: ch6 (null input, height first, maturity at 100), ch12 (the card "BIP 34 height push makes every coinbase differ", bad-cb-height, maturity, BIP 34 activation 750/950 in 1,000 blocks). All are facts or code. Nobody names blocks 91722 to 91880, d5d27987 or e3bf3d07, or BIP 30.
- Griefing the testnet: ch12 only has the "BIP 94 branch" card and the chainparams flags example (code and fact, no Lopp, no flood). Ch4 and ch5 mention testnet addresses and coin type 1. Ch7 tells a different 2010 event (script bugs shown on the test network, 28 July 2010).
- Signet: the word does not occur in any other deck.
- Inside chapter 11 and the page: the page's concept bodies mention Lopp's post of 4 May 2024, the block storms numbers, BIP 94 and BIP 325 and the 1979/1982 dates. These are source-cited facts in the concept explanations, not the story told again, so I count them as mentions. The page "Stories" tab holds each of the four once.

Genesis headline (chapter 1, slide 7): I do not count slides 6, 12 and 13 as a retelling. Slide 13 reads the message with code and states the fact and the proof of work; it has no actor, no occasion and no reason, which is what made it a story in chapter 1. On the page the nodes "Genesis quirks" and "The Chancellor of the headline" (Alistair Darling, Gordon Brown, The Times begun in 1785) are taxonomy facts. I would still watch the second one: it extends the headline subject with new facts and is the nearest thing to a repeat, but it tells no event. Slide 13's title "The first block quotes a newspaper" is the headline fact in one line; accepted.

Result: no story appears twice. Repeats found: 0.

## Check 3, evidence files

| File | Header names deck 2.7.0 and page 9.101.0 | Claim |
|---|---|---|
| ev_material_check_v1_3_0_deck_2_7_0.log | yes, with sha256 | 9 checks, all PASS, failed 0. Agrees, but see D16. |
| ev_deck_standard_deck_2_7_0.log | yes | PASS=12 FAIL=0. Agrees. |
| ev_page_test_9_45_0_page_9_101_0.log | yes ("page 9.101.0 (deck 2.7.0)") | 394 PASS, 0 FAIL, "widgets: 91 tested, 91 passed", "failed: 0". Agrees. Note: the body of the log is printed twice (lines 1-206 and 207-414) and only the first copy carries the widgets line. Not counted. |
| ev_code_frames_run_deck_2_7_0.log | yes | 74 "ok" lines, 17 examples, 74 shown results, failures 0. Agrees. The last line reads "manifest ... deck 2.5.0": it is the manifest's own version and the header explains that the manifest is unchanged. Not counted. |
| ev_verify_v1_0_2_deck_2_7_0.log | yes | failures: []. Agrees. |
| ev_links_deck_2_7_0.log (extra) | names deck 2.7.0 | 3 links, all 200; dated 2026-11-26 and not re-run by me. |

Every header names both versions. All logs say Python 3.13.18; the slides say 3.14.6 (accepted item b, I agree: the slide is about the page runtime).

D16: the material check line "no-analogy PASS failed 0/963" and deck-standard D4 "0 analogies" are true for the deck but the page contains several analogies (Check 5), so the checker does not cover the page text (its concept bodies) or misses them.

## Check 4, the new story and the date

Date: slide 25 reads "dates from 1979; on 5 January 1982 ... patent 4,309,569"; the page story reads 1979, patent published 5 January 1982; the concept "Hash tree history" reads 1979 and 1982. These agree. One page body (the block-chain history concept) says Merkle tree is "a structure from Ralph Merkle's work of 1980"; the 1980 date is the paper, but the sentence dates the structure to 1980 (D7).

Story of slide 14 and first page story ("The reward that was mined twice"):
- Helps to understand and remember slide 17: yes. The lesson "put the height in the coinbase and no two coinbases can be equal" is the reason for the height, and slide 17 refers back.
- Real names: partly. Pieter Wuille and Gavin Andresen are named only in the notes and on the page, not on slide 14 (the slide shows "BIP 30 (2012)" and "BIP 34" with no person), and the miners are anonymous (D6). No.
- 5N1K: what, when, where, how yes; who weak (see D6); why: no. Neither slide nor page says why the coinbases were equal or what was lost (D2). The page sentence "because the two coinbases of each pair were the same bytes" repeats the fact and is not a cause.
- Real free picture with credit: a labelled stand-in (accepted item a; I agree, the label and credit "Bitcoin-qt 0.5.2 ... MIT, Wikimedia Commons" are on slide and page, the stand-in is tied to the month BIP 30 was written).
- Live link: https://bips.dev/30/ answered 200 on 2026-11-26 per the link log.
- Factual inconsistency (D3): slide 14 says "Bitcoin Core still knows these four blocks by their hashes". Core's exemption list holds two (91842 and 91880), as the page and the notes themselves say. The slide sentence names four.

## Check 5, everyday analogies

Deck titles, subtitles, balloons, captions, credits, stories of slides 33, 37, 38: no analogy in titles, subtitles, captions or credits. Slides 33, 37 and 38 stories are free of analogies. Figurative wording that I did not count: "invitation to vandals" and "free coins invite vandals" (slide 33), "squeezes" (slide 20 note), "vouches" (slides 1, 25).

Counted analogies:
- D15 slide 41 takeaway "the code slide of its part carries the receipt" (and the same takeaway on the page, slide 41 record): a receipt is an everyday object.
- D8 page concept "Glacier core depth" (GlacierCoreAnalogy): ice core, topsoil, "an hour of snow", and "the same picture as a stack of newspapers in a cellar". The whole node is an analogy.
- D9 page "Hash leading zeros": "as when a lottery draws only the numbers below a limit ... tickets".
- D10 page "Block hash is double sha256": "A cryptographic hash is a fingerprint: change one bit of the finger and the print changes completely".
- D11 page (signet tip height note): "A number like this is a photograph of a growing child".
- D12 page (genesis block listing note): "A listing like this is a reference photograph".
- D13 page (target compact encoding): "like scientific notation on a pocket calculator".
- D14 page (field order and endianness): "Little-endian is like writing a date as day, month, year".
Not counted: "A block is a container" (page, concept "BlockContainer"), a label rather than a comparison.

## Defects

DEFECTS FOUND: 16
- D1 Slide 11 note: an undergraduate cannot teach it (what bits packs, why 224 bits).
- D2 Slide 14 note: academician and undergraduate cannot teach it; neither note, slide nor page story says why the coinbases were equal or what was lost; the note also says Core lists "the earlier two" as unspendable (it lists the later two).
- D3 Slide 14 text "Bitcoin Core still knows these four blocks by their hashes": Core names two blocks, as the page says.
- D4 Slide 19 note: an undergraduate cannot teach it (Poisson, q over p and the sum are left unexplained).
- D5 Slide 2: "Three parts" over four numbered items, and the note's "A first box" is undefined.
- D6 Slide 14 (and the slide-side of the page story): no person is named on the slide; the real names (Wuille, Andresen) are only in the notes and the page text; the miners are anonymous.
- D7 Page history concept: Merkle tree dated to "work of 1980", against 1979 on slide 25 and in the story.
- D8 Page: the "Glacier core depth" analogy node (ice core, snow, newspapers in a cellar).
- D9 Page: lottery analogy in "Hash leading zeros".
- D10 Page: fingerprint analogy in "Block hash is double sha256".
- D11 Page: "photograph of a growing child" in the signet tip-height note.
- D12 Page: "reference photograph" in the genesis block listing note.
- D13 Page: "scientific notation on a pocket calculator" in the compact target note.
- D14 Page: "writing a date as day, month, year" in the endianness note.
- D15 Slide 41 and the page takeaway: "carries the receipt".
- D16 The no-analogy check of ev_material_check_v1_3_0_deck_2_7_0.log passes with 0 of 963 while the page holds the analogies D8-D14 (the check does not reach them).
