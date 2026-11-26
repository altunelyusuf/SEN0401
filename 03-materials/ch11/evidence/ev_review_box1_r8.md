# Review 8, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent (earlier reviews not read). Material: deck 2.7.0 (43 slides), page 9.101.0, newest decks of chapters 1-10 and 12-14 (v3_7_0, v3_3_0, v3_3_1, v3_9_0, v3_8_0, v2_5_0, v2_7_0, v2_5_0, v2_2_0, v2_4_0, v3_1_0, v2_5_0, v2_2_0). Read with python-pptx 1.0.2 and by extracting the page's data, question bank, quiz, objectives and interface text. Nothing was changed except this file.

## Check 1, notes teach (DoD7_NotesTeach)

Slides read: 3, 6, 9, 12, 18, 20, 24, 28, 35, 37, 40, 43 (the draw) plus 38 and 41 (rewritten last). Slide 37 is both drawn and rewritten and is counted once, so the table has 14 distinct slides (the brief's "fifteen" counts 37 and the added 38 and 41 as the brief words it; with 37 once, 14). Slide 14 (also rewritten, used in Check 4) was read as well and passes the same test (yes, yes).

Rules measured: every note is within 60-140 words (opening, closing, divider 30-140): the longest is slide 41 at 138, slide 14 at 136, slide 38 at 133; none out of range. No note directs a presenter; the retell/compare/say-it-aloud sentences on slides 3, 6, 41, 43 and others are directions to the reader and allowed. No "think of". No analogy in the fifteen notes (but see Check 5, slide 10).

| Slide | Academician | Undergraduate | One line of why |
|---|---|---|---|
| 3 | yes | yes | The seven questions with the slide that answers each; slide numbers checked (9, 16-17, 18, 22, 24, 30-40, 32-33, 41) and correct. |
| 6 | yes | yes | Defines the four cards, says which example shows each. |
| 9 | yes | yes | Six fields, widths 4+32+32+3x4 = 80, cut points, bits 207fffff; the slide is about layout, the field meanings sit on slides 8 and 11. |
| 12 | yes | yes | Height, Core and Nakamoto defined; points to slide 17. |
| 14 | yes | yes | Blocks, identifiers, why equal bytes give equal names, what Core does, BIP 30 and BIP 34; times checked against the saved block files (17:59 and 21:04 UTC). |
| 18 | yes | yes | Nine links, one bit flipped, link at header 4 breaks, seven headers (3 to 9) re-mined: arithmetic correct. |
| 20 | yes | yes | Divider: previews the three columns and examples 9-12; patent date matches slide 25. |
| 24 | yes | yes | 4 hashes x 32 = 128 bytes; 320, 384, 448 bytes for 1,024, 4,096, 16,000 (10, 12, 14 hashes) correct. |
| 28 | yes | yes | Divider: previews the three columns and examples 13-17. |
| 35 | yes | yes | Prefix table matches the note; reason (wrong-chain address rejected) given. |
| 37 | yes | NO | The note uses "the four message-start bytes" and says a different challenge gives a different network, but never says what those bytes are or why they identify a chain; that is explained only in the note of slide 36. An undergraduate cannot teach the second half of the slide (magic bytes change with the script) from this note alone. |
| 38 | yes | NO | The slide states "2.27 times the book's listing" and "four magic bytes"; the note does not explain the 2.27 comparison (the book's 143,619 blocks appear only in the page story) nor what magic bytes are. The story itself (who, when, what, challenge, Core 0.21.0, height) is fully taught. |
| 40 | yes | yes | Halving at 150, six values at the six heights, match with Core's record; three halvings in 500 blocks correct. |
| 41 | yes | yes | Five lines restated with the slide order that proves each. |
| 43 | yes | yes | Four claims with slide ranges (7-16, 18-19, 22-27, 30-40), all correct. |

Result: two "no" (undergraduate, slides 37 and 38). Defects 1 and 2.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched the text and notes of all thirteen other decks and the page of chapter 11 for: Merkle, Ralph, patent 4,309,569, Stanford, 1979/1982; blocks 91722/91812/91842/91880, d5d27987, e3bf3d07, BIP 30, BIP 34, duplicate coinbase, November 2010; Lopp, griefing, Jahr, BIP 94, testnet3/testnet4, block storm, flood, vandal; signet, Alm, Towns, BIP 325, proof of authority, challenge script.

Counted as retellings: none. Counted as mentions, facts or code examples (not retellings):
- Chapter 12: "BIP 34 height push ... makes every coinbase different" (slides 17-18, notes only a rule and a code read); "BIP 34 activation", and "The BIP 94 branch / Testnet4 turns the BIP 94 branch on" (concept card, constants code example). Facts and code, no event told.
- Chapters 2, 3, 7, 10: "merkle root", "Merkle tree", "Merkle path" as concepts and a rebuild of one root in chapter 3. Concept explanations, not the Merkle patent story. Nobody else mentions Ralph Merkle, the patent or Stanford for the tree (chapter 4 names Stanford only for Diffie and Hellman 1976; chapter 8 tells the Schnorr patent, a different person and event).
- Chapters 4, 5, 6: testnet addresses, coin type 1, unspendable OP_RETURN: unrelated facts.
- Chapter 7 tells 28 July 2010 bugs shown on the test network, chapter 10 tells BIP 324 (Wuille among others, 8 March 2019), chapter 12 tells Taproot activation on 14 November 2021: other events, other years; the shared date of 14 November (2010 versus 2021) is a coincidence, not a repeat.
- Signet, Alm, Towns, BIP 325, Lopp, Jahr, BIP 94, blocks 91722-91880: found in no other deck.
- Inside chapter 11 the deck and the page tell the same four stories (by design) and other slides only point to them ("told on slide 25", "the repeat told on slide 14", "story on slide 33"); that is a mention.

Genesis-block headline (known and deliberate): I do NOT count slides 6, 12, 13 or the page's genesis nodes as a retelling. Reason under the counting rule: they give the headline as a code result (example 4, 69 characters, ten zeros), a fact of the header and a card meaning; none tells the event with person, place, reason and lesson as chapter 1 slide 7 does, and there is no picture, link or lesson on them. Two things I note for the owner without counting them: (a) slide 13 is a whole slide on the same 69 bytes that chapter 1 slide 8 already reads by code, so it is the same code example in two chapters (a code example is not a story, but it is the nearest thing to a repeat); (b) the page node "The Chancellor of the headline" adds new facts (Darling, Brown, The Times from 1785) and does not retell the event.

Result: no story appears twice. No defect.

## Check 3, evidence files

Hashes recomputed: deck sha256 3f03af1d1de838cf... and page sha256 e94ea6ef76af76e1... equal what every log header states.

| File | Header names deck 2.7.0 and page 9.101.0 | Content claimed | Found |
|---|---|---|---|
| ev_material_check_v1_3_0_deck_2_7_0.log | yes (title line, deck path, page path) | 9 of 9 PASS | nine checks listed, all PASS, "failed: 0" |
| ev_deck_standard_deck_2_7_0.log | yes | 12 of 12 PASS | D1-D12 all PASS, "PASS=12 FAIL=0" |
| ev_page_test_9_45_0_page_9_101_0.log | yes ("page 9.101.0 (deck 2.7.0)") | 0 failed, 91 of 91 widgets | "widgets: 91 tested, 91 passed; failing: []", "failed: 0", axe-core empty |
| ev_code_frames_run_deck_2_7_0.log | yes | 17 examples, 74 results, 0 failures | 74 "ok" lines, 17 examples, "failures 0", PASS |
| ev_verify_v1_0_3_deck_2_7_0.log | yes | no failures | "failures: []" |

Every file says it. Observations, not counted as defects: the last line of the code-frames log reads "manifest chapter_code_ch11_v1_2_0.json deck 2.5.0 ...", which is the deck the manifest was last changed for and which line 1 explains; it still reads oddly beside "deck 2.7.0". Several logs print their results twice (full and shortened). The links log (not in the brief) shows the links of slide 14 answering 200; I also fetched bips.dev 30, 94, 325 and the patent PDF: all 200.

Result: all five agree. No defect.

## Check 4, the new story and dates

Merkle date: slide 25 (text and note) and the page (story, concept "hash tree history", definition, question bank) all read: tree from 1979, patent 4,309,569 published 5 January 1982 (the 1980 paper is stated separately). Same on both. Slide 20's note "patent of 1982" agrees. OK.

New story (slide 14 and the page's first story, "The reward that was mined twice"):
- Helps understand and remember the chapter: yes. It gives the reason for the height in the coinbase (equal bytes, equal name, overwritten coins), ends on the lesson "Put the height in the coinbase and no two coinbases can be equal", and slide 17's note points back to it.
- Facts checked against the saved files: coinbase ids d5d27987 (blocks 91812 and 91842) and e3bf3d07 (91722 and 91880) correct; times 17:59 and 21:04 UTC on 14 November, 91722 at 08:37 UTC 14 November, 91880 at 00:36 UTC on 15 November; Core marks 91722 and 91812 unspendable and lets 91842 and 91880 through; BIP 30 Wuille, BIP 34 Andresen, 2012.
- 5N1K narrative with real names: yes (Wuille, Andresen, block numbers, ids, dates, source files); the miners are unnamed because the chain does not record them, and the page says so. On the slide the "why" is carried by the deck note and the page story, the slide itself gives who, what, when, how, lesson.
- Real free picture with credit: a labelled stand-in (see accepted (a)); credit line present on the slide and the page (author, MIT licence, Wikimedia Commons, 2012-02-21). I agree with the reason: no free picture of the events exists, and the stand-in is dated to the month BIP 30 was written, which the page states.
- Live link: yes, BIP 30 on bips.dev, answers 200.
- One no: both the slide and the page give only "14 November 2010" as the date of all four blocks, but block 91880 was mined at 00:36 UTC on 15 November (the brief and the story's own span are 14-15 November). Defect 4.

## Check 5, everyday analogy

Read all deck slide text, titles, subtitles, balloons, captions, credits and notes (slides 33, 37, 38 included) and the page: stories, concept bodies and definitions, findings, discussion, question bank, quiz, objectives, lecture notes, interface text. The automated check does not reach all of it; by hand I found two:
- Deck slide 10, note: "Only one child continues the family line, and that line is the active chain." This explains the active chain by a family line, an everyday picture. Defect 5. (Parent, child and descendant are the book's technical terms and are not counted.)
- Page, concept "The Chancellor of the headline": "The Times ... is a daily with a long record, a respectable witness for a date." The newspaper is explained as a witness. Defect 6.

Not counted, named so the owner can disagree: the idioms "flooded", "calm" and "invitation to vandals / free coins invite vandals" (slide 33, story, lecture note; Lopp's own word is griefing) are figures of speech for a technical event and not an everyday scene used to explain a mechanism; "Playground" is accepted (b); "faucet" is the crypto term; the SPARQL sentence "does for triples what SQL does for tables" compares two technologies, not an everyday thing. Picture credits, captions and balloons: none. Stories of slides 33, 37, 38 and the four page stories: none.

## Outside the brief (not counted)

The pictures of stories 33 and 38 are the generic Bitcoin logo, not a picture of the event, and are not labelled as stand-ins as slide 14's is.

DEFECTS FOUND: 6
1. Slide 37 note (undergraduate reader): "message-start bytes" are used and made the point of the slide but are not defined in this note; they are explained only on slide 36.
2. Slide 38 note (undergraduate reader): the slide's "2.27 times the book's listing" and "four magic bytes" are not explained in the note.
3. Slides 38 and 39 (slide text and slide 38 note) say Alm and Towns "wrote" BIP 325 on 20 March 2019; the BIP header says "Assigned: 2019-03-20" and the page story correctly says "assigned", so deck and page disagree and the deck overstates the source.
4. Slide 14 and the page story give only 14 November 2010; block 91880 was mined on 15 November 2010 (00:36 UTC), so the dates of the story are 14-15 November.
5. Slide 10 note: "the family line" is an everyday analogy.
6. Page concept "The Chancellor of the headline": "a respectable witness for a date" is an everyday analogy.
