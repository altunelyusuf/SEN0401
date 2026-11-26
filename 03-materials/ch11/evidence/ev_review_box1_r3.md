# Review 3, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent (did not read ev_review_box1.md or ev_review_box1_r2.md). Read-only apart from this file.
Material: deck SEN0401_Ch11_TheBlockchain_3e_v2_7_0.pptx (43 slides), page sen0401_ch11_page_v9_101_0.html, newest decks of chapters 1-10 and 12-14 (ch01 v3.7.0, ch02 v3.3.0, ch03 v3.3.1, ch04 v3.9.0, ch05 v3.8.0, ch06 v2.5.0, ch07 v2.7.0, ch08 v2.5.0, ch09 v2.2.0, ch10 v2.4.0, ch12 v3.1.0, ch13 v2.5.0, ch14 v2.2.0). Notes and slide text read with python-pptx.

## Check 1, notes teach (DoD7_NotesTeach)

Slides read: 1, 4, 7, 8, 14, 15, 17, 19, 24, 25, 26, 30, 36 (thirteen). All thirteen notes are inside the word limits (113, 109, 104, 112, 129, 102, 119, 140, 94, 108, 126, 97, 80 words); none directs a presenter, none says "think of", none uses an everyday analogy. The sentences "Compare with...", "Retell...", "Say each idea in your own words" are directions to the reader and are allowed.

| Slide | Academician | Undergraduate |
|---|---|---|
| 1 (opening) | yes: states scope, source of the numbers, and that a recorded run is one observation | yes: says what the deck covers and where the examples run |
| 4 (concept map) | yes: gives the three parts with their counts and how each part is built | yes: tells where to go when an idea is unclear |
| 7 | yes: header, count byte, 204-byte transaction, two independent sources as proof | yes: every part of the 285 is named |
| 8 | yes: defines the four cards, gives the hash-link consequence | yes: each term defined, examples named |
| 14 | yes: event, identifiers, why equal bytes mean equal name, Core's exception, BIP 30 and BIP 34 | yes: the chain of cause is clear (same bytes, same hash, cannot be told apart) |
| 15 | yes | yes |
| 17 | NO: the note says the eight heights were "chosen where the encoding of the height changes" but never states the encoding rule (a pushed little-endian number, why 16/17, 127/128, 255/256 are the edges). A teacher cannot explain why those eight values or what the code decodes. | yes: BIP 34 purpose and the 100-block wait are clear |
| 19 | yes: the white-paper model is written out with its numbers | NO: one long sentence packs the Poisson mean, the deficit and the sum of products with no plain statement of what it means, and the jump from "two blocks on one parent" to "a ten percent attacker" is never bridged; "Poisson chance" and "deficit" are undefined for a reader at this level. The note sits at exactly 140 words, so there is no room left to repair it without cutting. |
| 24 | yes | yes |
| 25 | yes: date, patent, assignee, idea, the block 277,315 case | yes |
| 26 | yes: odd-level pairing, six becomes eight, Core's verdict, why the defence works on content | yes |
| 30 | yes | yes |
| 36 | yes | NO: the key claim, "the four magic bytes come from its hash", rests on "magic bytes", which this note never explains; the reader of this slide alone cannot teach what they are or why a new script gives a new network (the term is only worked out later, on the signet code slide). |

Result: 10 of 13 slides are yes for both readers. The no answers: slide 17 (academician), slide 19 (undergraduate), slide 36 (undergraduate). Three defects.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched the notes and slide text of the thirteen other decks and the whole text of the chapter 11 page for: Ralph Merkle and the 1982 patent; blocks 91722/91812/91842/91880, the identifiers d5d27987 and e3bf3d07, BIP 30 and BIP 34 duplicate coinbases; Jameson Lopp, Fabian Jahr, griefing, testnet3 block storms, BIP 94; Karl-Johan Alm, Anthony Towns, BIP 325 signet.

Counted as retelling (event told as a story): none in any other chapter. Counted as mention (a name, a fact or a code example, not a retelling):
- ch12 slides on the coinbase and on soft forks name BIP 34 (height push; BIP 34 as the first soft fork by version count; activation at height 227,931) and BIP 94 (testnet4 retarget branch, regtest constants). Facts and code, not the 2010 event or the 2024 flood.
- ch02, ch03, ch07 and ch10 use merkle trees, roots and paths as a concept and code; ch10 slide on the light client (Merkle path). No Ralph Merkle, no patent, no 1982.
- ch04 slide 40 contrasts mainnet and testnet address bytes; no griefing, no Lopp, no Jahr.
- ch14 mentions a person called Fabian in a payment-channel example; unrelated.
- No other deck mentions signet, Alm or Towns at all.
- Inside chapter 11 each of the four stories is told once in the deck (slides 14, 25, 33, 38) and once in the page Stories tab (same four). The page also holds concept leaves with the same sources (HashTreeHistory, TestnetBlockStorms, SignetChallengeIsMultisig, and so on) and the research findings; I counted these as the factual record behind the stories, not as a second telling, because they define and evidence a concept and carry no narrative. Result: no story appears twice.

Genesis headline: told as a story in chapter 1 slide 7 (Satoshi Nakamoto mined block 0 on 3 January 2009, typed the headline). In chapter 11 slides 6 and 12 give it as a fact of the vocabulary, slide 13 as a code example (read the 69-character message, count ten leading zeros) and the page as taxonomy nodes. I do not count this as a retelling: nothing there tells the event or the person-and-event pair as a narrative, it uses the headline as data (message, time field, hash prefix). Two cautions, not counted as defects: the title of slide 13 ("The first block quotes a newspaper") and the first sentence of its note echo the chapter 1 slide, and the page node ChancellorOfTheHeadline (Alistair Darling, history of The Times, the headline as proof of the earliest date) goes beyond a code example into the background of the headline. Neither retells chapter 1's story, but both are the closest things to a repeat; if the owner wants them gone, slide 13's title and that node are the places.

Defects in this check: 0.

## Check 3, evidence files

SHA-256 prefixes in every header match the files on disk: deck d09324500dce906d (matches), page 8c86d0a61ee232c4 (matches).

| File | Claimed | Found | Header names deck and page |
|---|---|---|---|
| ev_material_check_v1_3_0_deck_2_7_0.log | 9 of 9 PASS | 9 PASS lines, "failed: 0" | yes, deck 2.7.0 and page 9.101.0 |
| ev_deck_standard_deck_2_7_0.log | 12 of 12 PASS | "SUMMARY PASS=12 FAIL=0", "failed: 0" | yes |
| ev_page_test_9_45_0_page_9_101_0.log | 0 failed, 91 of 91 widgets | "widgets: 91 tested, 91 passed; failing: []", 394 PASS lines, 0 FAIL, "failed: 0" | yes (page 9.101.0, deck 2.7.0) |
| ev_code_frames_run_deck_2_7_0.log | 17 examples, 74 results, 0 failures | 74 "ok" lines, "17 ... shown results 74 failures 0", RESULT PASS | yes; it also states the manifest chapter_code_ch11_v1_2_0.json is unchanged by deck 2.7.0 (the last line still prints "deck 2.5.0", the version the manifest was made for, which the header explains) |
| ev_verify_v1_0_2_deck_2_7_0.log | no failures | "failures: []", 4 stories, 91 classes | yes |

Every claim agrees. One observation, not counted: every slide with code says "run under Python 3.14.6" (and all other chapters say the same), while all five logs say they were run with Python 3.13.18. The recorded run is a different thing from the check run, but no log shows 3.14.6, so the claim on the slides is not evidenced by these files.

Defects in this check: 0.

## Check 4, the new story and dates

Date of the hash tree. Slide 25 and its note: tree dates from 1979, patent 4,309,569 published 5 January 1982. The page Stories tab (TheHashTreeOfRalphMerkle) and the body of the Hash tree history leaf agree with that wording. But the page still carries the older wording "patented it in 1979" in several places:
- the question bank item for HashTreeHistory ("Which of these sentences opens the explanation of 'Hash tree history'") offers the option "The hash tree is named after Ralph Merkle, who patented it in 1979; ...", which is no longer the sentence that opens the explanation (it now opens "whose tree dates from 1979");
- the embedded ontology holds the example label "patented in 1979", the definition "who patented it in 1979 (US patent 4309569 of 1982)", the section definition "who patented it in 1979", and the finding "Ralph Merkle patented the hash tree in 1979" (Conclusion) and "Merkle patented the hash tree in 1979" (the isEarlierThan annotation).
So the page does not read the same as slide 25 (slide: dates from 1979, published 1982; page: patented in 1979, and 1982 in the same breath). One defect.

The new story (slide 14 and the first story of the page, "The reward that was mined twice"). Does it help to understand and remember the chapter and the reason for the height in the coinbase (slide 17)? Yes. Slide 14's note ends with "Connect this with slide 17, where the height is read back"; slide 17's note names "the repeat told on slide 14"; the lesson line, "Put the height in the coinbase and no two coinbases can be equal", is exactly the reason for BIP 34. The page story ends on the same point (the height is read back from eight scripts in this chapter).
- 5N1K narrative with real names: yes. Who: Pieter Wuille (BIP 30), Gavin Andresen (BIP 34), the miners left unnamed because the chain does not record them. What: two pairs of identical coinbases. When: 14 November 2010 and the BIPs of 2012. Where: blocks 91722, 91812, 91842, 91880. Why: equal bytes give equal identifiers. How: BIP 30 forbids repeats, BIP 34 puts the height first. The 5N1K labels are not printed. (Small point: the page "when" field says 2010-11-14 while the brief gives 14-15 November for the span of the four blocks; the page story starts "On 14 November 2010" and says 91722 and 91880 were about sixteen hours apart, so it is consistent with a span into the 15th but never says so.)
- Live link: yes. bips.dev/30 is on slide 14 as a hyperlink and is the page story link; ev_links_deck_2_7_0.log shows HTTP 200 for it, for the mempool.space block page and for the Commons file page.
- Real free picture with credit: partly no. The picture is a real, free (MIT), credited screenshot, Bitcoin-qt 0.5.2 (Wikimedia Commons, recorded 2012-02-21), and slide 14 and the page both say plainly that it is a stand-in. But it shows nothing of the event: it is the client of February 2012, more than a year after the four blocks of November 2010, and not a block, a coinbase or a person from the story. I count that as a no for "a real picture" of the story. One defect.

## Further defect found while reading (outside the four checks, but the owner's ruling of 2026-11-24 bans everyday analogies in course materials)

The two new test-chain stories carry everyday analogies. Deck slide 33 is titled "When the sandbox was flooded" and the page story 3 uses a photograph of children in a sandpit (credited as "stand-in picture: a sandpit, not the testnet"); deck slide 38 and page story 4 are titled "A test network with a doorman", slide 37's subtitle is "The doorman's rule", and the page picture is a signet ring of Ramesses II (stand-in). Sandbox, sandpit and doorman are analogies for a test network and for signature checking. ev_deck_standard D4 and the material check no-analogy still pass, so those checks do not catch this. One defect.

## Summary of counts

Check 1: 3 (slide 17 academician, slide 19 undergraduate, slide 36 undergraduate). Check 2: 0. Check 3: 0. Check 4: 2 (page still says "patented in 1979"; slide 14 and page story 1 use a stand-in picture of 2012 for events of 2010). Outside the checks: 1 (analogy titles and stand-in pictures on the stories of slides 33, 37, 38 and the page).

DEFECTS FOUND: 6
1. Slide 17 notes: academician cannot teach the height encoding (rule behind the eight heights is not stated).
2. Slide 19 notes: undergraduate cannot follow the Poisson/deficit sentence or the bridge from fork to attacker model; note is at the 140-word limit.
3. Slide 36 notes: undergraduate cannot teach "magic bytes" (undefined in the note).
4. Page still says "patented in 1979" (question bank option for Hash tree history, ontology label and definitions, two findings) against slide 25 and the story: "dates from 1979, patent published 5 January 1982".
5. Slide 14 and page story 1: the picture is a stand-in (Bitcoin-qt 0.5.2, February 2012), not a real picture of the 2010 event.
6. Everyday analogies in the stories of slides 33 and 38 (titles "sandbox" and "doorman", slide 37 subtitle "The doorman's rule", sandpit and signet-ring stand-in pictures on the page), against the owner's ruling of 2026-11-24; the automated no-analogy checks do not see them.
