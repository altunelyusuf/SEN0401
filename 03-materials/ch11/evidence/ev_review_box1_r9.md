# Review 9, SEN0401 chapter 11, lineage 7 box 1 (deck 2.7.0, page 9.101.0)

Independent reviewer. Read files only. Deck read with python-pptx 1.0.2 (all 43 slides, text and notes); page read from its embedded JSON (data, qbank, quiz, objectives: about 7,000 text fields) and its static HTML; the newest deck of each of chapters 01-10 and 12-14 read the same way.

## Check 1, notes teach (DoD7_NotesTeach)

Word counts of the deck notes: all 43 within 60-140 (slide 14 is exactly 140, slide 38 is 139; opening, closing and dividers 95-113). No direction to a presenter, no "think of", no analogy found in any note. Sentences such as "Retell...", "Compare with...", "Say each claim aloud" are directions to the reader and are allowed. Facts I re-derived and found correct in the notes: the widths 4+32+32+4+4+4=80; 0x1d00ffff = 0xffff x 256^26 (224 bits); the catch-up formula and its values 1.0, 0.2045873, 0.0509779, 0.0002428; proof sizes 128, 320, 384, 448 bytes (14 hashes for 16,000); 40 ids give six levels up; 91812/91842 and 91722/91880 with BIP 30 and BIP 34 as BIP 30 states them; 71-byte 1-of-2 challenge; 326,440 / 143,619 = 2.27; 3 halvings in 500 regtest blocks. Cross references in the notes (slides 3, 13/14, 17, 20, 26, 27, 29, 32/33, 43; example numbers 1-17; 17 concepts / 7 / 17 = 41) all point to the right slide or example.

Both readers answer "could I teach this slide from the note alone?" the same way:

| Slide | Academician | Undergraduate | Why (one line) |
|---|---|---|---|
| 1 | yes | yes | scope of the deck, where numbers come from, what a recorded run is |
| 2 | yes | yes | route, counts, where the examples live |
| 3 | yes | yes | seven questions each mapped to a slide |
| 4 | yes | yes | counts per part, what a concept card is |
| 5 | yes | yes | part preview with example numbers, parent-hash habit |
| 6 | yes | yes | four terms defined, each tied to an example |
| 7 | yes | yes | 80+1+204=285, regtest named, two sources agree |
| 8 | yes | yes | chain, parent, genesis defined; why a change breaks a link |
| 9 | yes | yes | six fields, widths, cut points, bits 207fffff |
| 10 | yes | yes | child, block, block hash; name never stored |
| 11 | yes | yes | time, median time past, compact bits, difficulty with the arithmetic |
| 12 | yes | yes | height, Core, Nakamoto; points to slide 17 |
| 13 | yes | yes | headline, ten zeros as proof of work, time field |
| 14 | yes | yes | the event, why equal bytes, how Core marks it, BIP 30 and 34 |
| 15 | yes | yes | three terms; BIP 34 reading a height from a coinbase |
| 16 | yes | yes | hash once versus twice, [::-1] explained, name recomputed |
| 17 | yes | yes | height encoding borders, maturity 99 versus 100 and why |
| 18 | yes | yes | nine links, bit flip, seven headers re-mined, why it protects |
| 19 | yes | yes | fork, formula with both factors explained, four values |
| 20 | yes | yes | divider: tree, proofs, weakness; header commits to the root |
| 21 | yes | yes | four tree terms with the padding rule |
| 22 | yes | yes | levels 4,2,1 and 3,2,1, padding causes example 11 |
| 23 | yes | yes | authentication path = merkle path, one idea |
| 24 | yes | yes | 4 x 32 = 128 bytes, logarithmic growth with three sizes |
| 25 | yes | yes | patent number, date, assignee, 1979 versus 1982, block 277,315 |
| 26 | yes | yes | six becomes eight, same pairs, Core verdict, defence on content |
| 27 | yes | yes | 5 hashes, 248 bytes, saving grows with block size |
| 28 | yes | yes | divider: same rules, other constants |
| 29 | yes | yes | four terms, flood reason, pointer to slide 33 |
| 30 | yes | yes | ports and chain sizes, one source file |
| 31 | yes | yes | signet, custom signet, regtest, development order |
| 32 | yes | yes | min-difficulty table, deprecation, testnet4 genesis |
| 33 | yes | yes | Lopp 4 May 2024, BIP 94, heights of 15 Oct 2026 |
| 34 | yes | yes | three terms, same rules versus constants |
| 35 | yes | yes | prefixes per chain and why a wallet can reject the wrong one |
| 36 | yes | yes | challenge script, magic bytes defined |
| 37 | yes | yes | 1-of-2 multisig, how magic is derived, 51 gives 54d26fbd |
| 38 | yes | yes | BIP 325, challenge, magic, trade-off, 2.27 times |
| 39 | yes | yes | regtest, BIP 325, mainnet; which activity on which chain |
| 40 | yes | yes | 150-block halving, six values, same rule as Core's record |
| 41 | yes | yes | five lines expanded and mapped to the slide groups |
| 42 | yes | yes | what each resource gives; Brownworth demo named |
| 43 | yes | yes | four claims with slide ranges |

Result on the deck: no "no" for either reader.

One "no" on the page, found while comparing (see D1): the page's Lecture tab shows a shortened copy of these notes, not the notes.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched the text and notes of the newest decks of chapters 01-10 and 12-14 (13 decks) for: Merkle, patent, Stanford, 1979/1982, coinbase, 91722/91842/91880, d5d27987, e3bf3d07, BIP 30, BIP 34, duplicate, overwrite, Wuille, Andresen, Lopp, Jahr, Griefing, testnet3, flood, BIP 94, signet, BIP 325, Karl-Johan, Towns, challenge. I also searched the stories and other text of the newest page of each of those chapters.

- Hash tree of Ralph Merkle: no other deck or page tells it. Counted as mentions only: chapter 2 slides 37, 42, 43 and 54, chapter 3 slides 44, 46, 47 and 59, chapter 10 slides 30, 32, 47 and 49 (the merkle tree and path as technique, no history, no person).
- Two coinbases mined twice (blocks 91722-91880): not told elsewhere. Counted as mentions only: chapter 12 slides 17-18 ("The BIP 34 height push makes every coinbase different", code of the Core coinbase) and slides 40 and 48 (BIP 34 as the first soft fork, activation height 227,931). These state a rule or a height; none narrates the duplicate event. Chapter 13's page contains the digits 91842 only inside base64 data.
- Griefing the testnet (Lopp, Jahr): no other deck or page. Chapter 12 names BIP 94 only as a retarget branch of the code, slides 26 and 31 (a code fact, mention). Lopp appears in chapters 5 and 8 pages as an author of unrelated items (a record of attacks, BIP 361), not this story.
- Signet blocks need a signature (Alm, Towns): no other deck or page. Anthony Towns appears in chapter 7 and 12 pages as an author of MAST naming and of BIP 341 (other facts, mention).
- Within chapter 11 the four stories are told once each (deck slides 14, 25, 33, 38; page Stories tab). No page concept body retells another story as a narrative.

Genesis headline (told in chapter 1, slide 7): I do not count it as a retelling in chapter 11. Slides 6, 12 and 13 use the headline text as a block-header example and as the proof that the hash starts with ten zeros; none says who wrote it, why, or what it answered, which is what chapter 1 narrates. The page keeps two taxonomy nodes (GenesisCoinbaseMessage, ChancellorOfTheHeadline) with new facts (Darling, The Times from 1785). One sentence in GenesisCoinbaseMessage ("proves the block cannot have been made before that day ... marks the moment of the financial crisis") repeats the two-point lesson of chapter 1 in a concept definition; I count it as a fact of the concept, not a story, but the owner may prefer to trim it. Not a defect.

Result: no story appears twice.

## Check 3, evidence files

All five headers name deck 2.7.0 (sha256 6d501912...) and page 9.101.0 (sha256 0cc0c3b9...).
- ev_material_check_v1_3_0_deck_2_7_0.log: 9 checks listed, each PASS, "failed 0" on each; "failed: 0". (The file does not print the words "9 of 9"; the nine PASS lines are there.) Agrees.
- ev_deck_standard_deck_2_7_0.log: SUMMARY PASS=12 FAIL=0 NOT_MEASURED=0, RESULT PASS. Agrees.
- ev_page_test_9_45_0_page_9_101_0.log: 394 PASS lines, 0 FAIL, "widgets: 91 tested, 91 passed; failing: []", "failed: 0". Agrees. It tests only that the Lecture tab has "one slide text per deck slide", not that the text equals the notes (see D1).
- ev_code_frames_run_deck_2_7_0.log: 17 examples, 74 "ok" lines each carrying "slide shows", "failures 0", RESULT PASS. Agrees. The last line says "manifest ... deck 2.5.0"; the header explains that the manifest is unchanged by 2.7.0. Not a defect.
- ev_verify_v1_0_3_deck_2_7_0.log: "failures: []". Agrees.
- Also ev_links_deck_2_7_0.log: three links of slide 14 and the page story all 200. The patent link of slide 25 and the links of slide 42 are not in this log (its scope line says slide 14 and the page story). Observation only.
- Python 3.13.18 in every header is the known, accepted case.

## Check 4, the new story and the dates

- Date of the hash tree: slide 25 text and note, the page story (when 1982-01-05, "dates from 1979 ... published on 5 January 1982"), the page concept HashTreeHistory and the page conclusion all read 1979 for the tree, 1982 for the patent, 1980 for the paper. Same everywhere. Yes.
- Story of slide 14 and the first page story: helps to understand and remember the reason for the height in the coinbase (slide 17)? Yes: its lesson line ("Put the height in the coinbase and no two coinbases can be equal") is the reason slide 17 gives, slide 17's note points back to slide 14, and slide 15 and the example 6 result carry the BIP 34 height.
- 5N1K narrative: yes (who: Wuille, Andresen, the unnamed miners; what; when with dates; where: blocks and Core's validation.cpp; why: no input so equal bytes; how: BIP 30 and BIP 34), no visible labels. Real names: yes. Picture with credit: yes, a labelled stand-in (accepted (a)); credit line gives author, licence and Wikimedia Commons. Live link: yes, https://bips.dev/30/ answers 200 and is a clickable link on slide 14. All "yes".

## Check 5, no everyday analogy

Read: all 43 slides' text and notes; page Stories, concept bodies and definitions (91 concepts), findings (25), question bank (91 items and options), quiz, discussion, agents, mission, lecture, resources, static HTML. Searched for like-a, as-if, imagine, think of, akin, metaphor and about 150 everyday nouns (vault, domino, recipe, library, fingerprint, race, game, family and so on). Hits were all technical: "looks like an inner node", "a number like this", "toy curve", "toy proof-of-work miner" (simplified model), "faucet", "twin list" (code name), "Playground" (accepted (b)), "parent/child/sibling" (the standard tree terms), "race" in slide 19's note (the attacker's catch-up in the white paper's own model).
Borderline, not counted: "Free coins invite vandals" (slide 33), "an invitation to vandals" (its note), the page lesson "rules against vandals", and "stays calm" (slides 31, 38); "vandal" is the figurative word for what the source calls griefing. If the owner reads that as an everyday comparison, replace it with "abuse" / "flooding".
No analogy found in titles, subtitles, balloons, captions, picture credits, or the stories of slides 14, 25, 33, 37, 38 and the page stories.

## Defect

D1. The Lecture tab of the page (data.lecture[i].say, rendered as the paragraph of each slide) is not the deck note. It differs from the note on all 43 slides and is a cut-off copy: the last sentences are missing. 16 slides fall under 60 words (2: 57, 8: 58, 9: 46, 11: 38, 12: 53, 15: 56, 16: 53, 19: 48, 21: 5, 26: 49, 30: 45, 33: 52, 36: 41, 38: 58, 41: 29; slide 28 is a divider at 49, allowed). Slide 21's text is "These cards define the tree." (5 words); slide 41 stops after line one of five; slide 19 stops before the formula and its values; slide 9 stops before the cut points and bits; slide 11 stops before the bits arithmetic and the difficulty; slide 14 stops before BIP 30 and BIP 34, so the reader of the page's lecture does not get the remedy of the story (it is on the Stories card). A reader of the page cannot teach these slides from that text. The page's own header says the notes of slides 14, 17, 19 and 26 were made to teach alone, and the page test checks only that one text exists per slide. Fix: make data.lecture[].say equal the deck notes of 2.7.0 and add a page-test check of equality.

DEFECTS FOUND: 1
1. D1: page Lecture text is a shortened copy of the deck notes (all 43 differ, 16 content slides under 60 words, slide 21 has 5 words), so the page cannot teach those slides alone.
