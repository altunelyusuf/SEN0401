# Review r5, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent; ev_review_box1.md to _r4.md not read. Files only were read. Deck notes and slide text were read with python-pptx 1.0.2 (deck 2.7.0, sha256 17b04eae... matches the evidence headers; page 9.101.0, sha256 236e14da... matches). The page's data blocks (nodes, stories, findings, lecture, qbank, quiz, refs, panels, agents, resources) were read as text; its Turtle blocks were not.

Word counts of the notes of the 14 slides below: 1:113, 2:109, 4:109, 6:110, 9:115, 11:114, 14:136, 19:140, 20:97, 22:94, 23:101, 36:96, 38:135, 42:102. All are inside 60-140 (30-140 for the opening, divider and closing slides 1, 20, 42). No note holds a presenter direction, "think of" or an everyday analogy. "Retell" and "compare" sentences are reader directions and are allowed.

Brief arithmetic: the seed list [1,4,6,9,11,20,22,23,38,42] plus [2,11,14,19,36] gives 14 distinct slides (11 is in both lists), not fifteen. All 14 were reviewed.

## Check 1, notes teach (DoD7_NotesTeach)

| Slide | Academician | Undergraduate | Why |
|---|---|---|---|
| 1 | yes | yes | States what the deck covers, that results are one recorded run, and where the examples are listed. |
| 2 | yes | yes | Gives the four parts, the counts and how the numbers map onto the page. |
| 4 | yes | yes | Gives the counts per part (17+7+17 = 41 concepts; 8+4+5 = 17 examples) and what each part contains. See defect 2 for the "three parts" wording. |
| 6 | yes | yes | Defines block, header, the two names and the genesis block, each with its example number. |
| 9 | yes | yes | Gives the six fields, the widths 4/32/32/4/4/4 = 80, the cut points and the result 207fffff. |
| 11 | yes | yes | Explains time, median time past, bits as exponent plus mantissa, and difficulty, with the three results. Arithmetic is correct (0xffff x 256^26 has 224 bits). |
| 14 | yes | yes | Gives who, what, when and why (no input, so equal bytes give an equal name), how Core treats it, and the two fixes. |
| 19 | yes | yes, but the closest call | The prose formula (Poisson count, (q/p)^(z-k) closing chance, one minus the sum) is complete and the four results are given. A student cannot compute it without a symbol, but can teach the fork and why the odds fall. I did not count this as a no. |
| 20 | yes | yes | Divider: previews the tree, the proof and the weakness with their example numbers. |
| 22 | yes | yes | Levels 4-2-1 and 3-2-1, the padding rule and why it leads to example 11. |
| 23 | yes | yes | Defines path, merkle path (same thing) and light client. |
| 36 | yes | yes | Defines the three terms and explains that the magic bytes come from the script's hash. |
| 38 | yes | yes | Who, when, what a challenge is, the 1-of-2 multisig, the magic bytes 0a03cf40, the trade-off and the Core version. |
| 42 | yes | yes | Closing slide: says what each group of links offers and how they were checked. |

Every no: none among the 14 notes. One consistency defect found while reading them:

Defect 2 (consistency of slides 2 and 4). Slide 2 and its note say the chapter has "four parts" (slides 3-4 questions and map, 5-19, 20-27, 28-43). Slide 4 is titled "One chapter, three parts" and its footer says "Three parts". A reader who retells the structure from the two notes gets two different answers.

Observations, not counted: (i) the slide 11 note says one wrong clock "cannot move" the median time past; one wrong timestamp can shift it to a neighbouring value, so "cannot" is slightly too strong. (ii) The slide 20 note calls "Ralph Merkle's patent of 1982" "the source of the idea", while slide 25 dates the tree from 1979; "source" is loose wording but the dates agree.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched: notes and slide text of ch01 v3.7.0, ch02 v3.3.0, ch03 v3.3.1, ch04 v3.9.0, ch05 v3.8.0, ch06 v2.5.0, ch07 v2.7.0, ch08 v2.5.0, ch09 v2.2.0, ch10 v2.4.0, ch12 v3.1.0, ch13 v2.5.0, ch14 v2.2.0, and the chapter 11 page (stories, nodes, findings, lecture, refs, qbank).

Result: no story of the four appears twice. No hit is a retelling.

Counted as mentions, not retellings:
- ch12: the "BIP 34 height push" card, the "BIP 34 activation" card (750/950 of 1,000 blocks) and the height 227,931 in the chainparams code slide. These are facts about the rule, not the 2010 duplicate-coinbase event. ch12 also has a different 2013 story (block 225,430, Gavin Andresen's BIP 50). Not a repeat.
- ch12: the "BIP 94 branch" cards and the code slide on enforce_BIP94 (a code example and a fact, no Lopp, no flood story).
- ch12 extra-nonce slide: the coinbase script counter, unrelated to blocks 91812/91842.
- ch10 and ch02/03/07: merkle path, merkle root, glossary lines. No Merkle 1979/1982 patent story anywhere else. The only patent stories elsewhere are Schnorr's (ch07, ch08), which is a different person, patent and event.
- ch07 has a 28 July 2010 testnet bug story: different event.
- ch11 itself: slides 17, 20, 33 and 38 point to the stories of slides 14, 25 and 33 ("told on slide 25", "the repeat told on slide 14"). Pointers, not retellings. The notes of the example slides about the minimum-difficulty rule (slide about example 14) say miners could flood testnet3, which is the result of the code example, not the Lopp narrative. The page repeats each story once in `stories` and once in `lecture` (the deck notes), which is the same story in the same chapter's two media, by design.

Genesis block headline (told in ch01 slide 7): I do not count slides 6, 12, 13 or the page taxonomy node as a retelling. Slide 13 is a code example whose result prints the message, its 69 characters, the time field and the ten zeros; slide 6 and 12 are definition cards ("quotes The Times"); the page node is a taxonomy entry. None tells who typed it, what he meant or the Chancellor's bailout as a narrative. The counting rule (a retelling tells the event as a story) holds. Caveat: slide 13's note is a full sentence with the headline, date and source, and its title is "The first block quotes a newspaper"; it is the nearest case to a repeat, but it describes the printed result and not the act, so I agree with the owner's ruling.

## Check 3, evidence files

All five headers name deck 2.7.0 and page 9.101.0, with sha256 prefixes that match the files on disk.

- ev_material_check_v1_3_0_deck_2_7_0.log: 9 checks, all PASS, "failed: 0" (9 of 9). Header names deck and page.
- ev_deck_standard_deck_2_7_0.log: "SUMMARY PASS=12 FAIL=0 NOT_MEASURED=0", "failed: 0". Header names deck and page.
- ev_page_test_9_45_0_page_9_101_0.log: "widgets: 91 tested, 91 passed; failing: []", 394 PASS lines, 0 FAIL, "failed: 0". Header names page 9.101.0 and deck 2.7.0.
- ev_code_frames_run_deck_2_7_0.log: 74 "ok" lines, 0 failures, 17 examples. Header names deck and page. Plain statement: its last line reads "manifest chapter_code_ch11_v1_2_0.json deck 2.5.0 examples 17 shown results 74 failures 0". The "deck 2.5.0" is the manifest's own recorded deck, and the first line of the file says the manifest is unchanged by 2.7.0; so the file agrees, but a reader who stops at the last line sees 2.5.0.
- ev_verify_v1_0_2_deck_2_7_0.log: "failures: []". Header names deck and page.

Stale files that still exist and name the older deck: ev_links.log (deck 2.6.0), ev_stories_v1_4_0.log (deck 2.6.0, page 9.100.0), and the *_deck_2_6_0 logs. Not among the files claimed, but there is no 2.7.0 version of the stories self-check, and ev_links_deck_2_7_0.log covers only three links (slide 14 and the page story link: bips.dev/30, mempool.space block, the Wikimedia file; all 200). The links of slide 42 were not re-run for 2.7.0.

## Check 4, the new story and the dates

Date of Merkle's tree: slide 25 and its note say "dates from 1979", patent published 5 January 1982 (US 4,309,569, Stanford). The page story, node "Hash tree history", finding 12, the lecture text and the question bank say the same. They also name Merkle's 1980 paper (a third date, a different work), which the slide does not mention. The dates read the same. No defect.

Story of slide 14 and the first story of the page ("The reward that was mined twice"):
- Helps to understand and remember the chapter: yes. It shows the problem (equal coinbase bytes give equal names, so one overwrites the other) before slide 17 gives the cure; slide 17's note points back to it. The lesson line is a good memory hook.
- 5N1K: who (Wuille BIP 30, Andresen BIP 34; the miners are named as unknown), what, when (14 November 2010; 91880 falls on 15 November by the page's own hours, not stated), where (blocks, Core's IsBIP30Repeat, bips repository), how (the fixes): yes. Real names: yes. Live link: yes, bips.dev/30 is a hyperlink on slide 14 and answered 200.
- Real free picture with credit: partly, see (a) below. A credit is printed on both.
- Defect 1 (why is missing on the page): the page story explains the cause by "because the two coinbases of each pair were the same bytes", which is the same fact restated. The reason (a coinbase has no input to make it differ, so equal script and reward give equal bytes, and a transaction is named by the hash of its bytes) is only in the deck note of slide 14, not in the page story or on the slide. The page reader who opens the story alone gets no "why".
- Observation, not counted: the slide title "Two blocks with one coinbase" fits one pair, while the story covers two pairs (four blocks).

(a) Stand-in picture: I accept it. The reason is sound since it is labelled on the slide ("Stand-in picture: the client of February 2012") and on the page, and the credit names the licence. One caution: it adds nothing to remembering the story, because the screen shows a wallet, not the blocks.

(b) "run under Python 3.14.6": I disagree with the reason as given. The page says its 69 examples run in the browser on Pyodide Python 3.13.2 (notice), and that "each result equals what the research recorded under Python 3.14.6". So 3.14.6 is the version of the research recording, not the runtime of the page, and the evidence logs and the page's data say Python 3.13.18 again. Three versions (3.14.6, 3.13.2, 3.13.18) are in play. Accepted by the owner; not counted.

## Check 5, no everyday analogy

Read: all text of the 43 slides (titles, subtitles, balloons, captions, picture credits, tables, notes) and the page text (concept bodies, definitions, examples, findings, refs, lecture, panels, resources, question bank, quiz, stories and credits, interface strings of the head and script). Searched for comparison phrases (like a, as if, imagine, think of, analogy, resembles, just as, the way a) and for everyday nouns. Slides 33, 37, 38 and the four page stories were read in full.

Found: none. Figures of speech that I did not count, because none explains a concept through an ordinary thing: "vouches for" (slide 25, the owner's lesson line), "invitation to vandals" and "flood" (slide 33, griefing and block flooding are the terms of the source), "stays calm" (slide 38), "bundles of transactions" (slide 12), "a race" (slide 19, Nakamoto's own term), "the way a database designer would draw it" (page ERD help text, a description of a notation). The automated no-analogy check (963 strings) agrees.

## Result

DEFECTS FOUND: 2
1. Page story "The reward that was mined twice" (and slide 14 text) gives no reason why the two coinbases were equal; the cause is only in the deck note of slide 14.
2. Slide 2 and its note say the chapter has four parts, slide 4 is titled "three parts".
