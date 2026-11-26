# Review 6, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent (did not build the material; ev_review_box1.md and _r2 to _r5 were not read).
Material: deck SEN0401_Ch11_TheBlockchain_3e_v2_7_0.pptx (43 slides), page sen0401_ch11_page_v9_101_0.html, newest decks of chapters 1 to 10 and 12 to 14 (ch01 v3.7.0, ch02 v3.3.0, ch03 v3.3.1, ch04 v3.9.0, ch05 v3.8.0, ch06 v2.5.0, ch07 v2.7.0, ch08 v2.5.0, ch09 v2.2.0, ch10 v2.4.0, ch12 v3.1.0, ch13 v2.5.0, ch14 v2.2.0).
Method: python-pptx 1.0.2 for every slide's text, tables and notes; the page's embedded JSON (concepts, definitions, questions, findings, stories, lecture) and its script read as text. Nothing was changed except this file.

## Check 1. Notes teach (DoD7_NotesTeach)

Sample: 5, 6, 9, 10, 11, 13, 15, 16, 40, 43 (seed 20261201) plus 2, 4, 14, 19 = 14 distinct slides. The brief says fifteen, but 2, 4, 14 and 19 add four to ten drawn slides and none of them is among the ten, so the set has fourteen. I read 14 and found no fifteenth.

Rules: word counts are 60 to 140 (30 to 140 on opening, closing, dividers). Measured: 2=109, 4=109, 5=106, 6=110, 9=115, 10=107, 11=114, 13=95, 14=136, 15=102, 16=95, 19=140, 40=94, 43=108. All inside the limits (slide 19 sits exactly on 140). No direction to a presenter and no "think of" in any of the 43 notes; the only addresses to the reader are "retell", "compare", "use this slide to find", "say each claim aloud", which the owner allows.

| Slide | Academician | Undergraduate |
|---|---|---|
| 2 | yes, the route, the counts and where the examples run are all in the note | yes, same |
| 4 | yes, the 17, 7, 17 concepts and 8, 4, 5 examples add up (41 and 17); I checked them against the slides | yes |
| 5 | yes, divider; says what the three columns preview and the single idea (parent hash makes the chain) | yes |
| 6 | yes, all four terms defined | yes |
| 9 | yes, six fields, widths, cut points and the sum to 80 are all given | NO, see defect 3: "the private chain" and the "regtest record" are used without ever being said what they are, and 207fffff is read out but not explained until slide 11 |
| 10 | yes | yes |
| 11 | yes; 0xffff x 256^26, 224 bits and the difficulty ratio check out | yes (the phrase "three digit bytes" is awkward but the mantissa is understood) |
| 13 | yes | yes |
| 14 | yes: event, mechanism, what Core does, both BIPs; dates and hashes agree with the saved block files | yes |
| 15 | yes | yes |
| 16 | NO, see defect 1: the code reverses the bytes (`[::-1]`) and neither slide nor note says why | yes for the idea (hash twice, name starts with zeros); the reversal is unexplained for him as well |
| 19 | yes | NO, see defects 2 and 3 |
| 40 | yes | yes |
| 43 | yes, four claims each tied to slide numbers | yes |

Defects of check 1:
1. Slide 16, academician: not teachable from the note alone. The result 6dd6c5716cc8 and the name 000000000019 are both shown after `[::-1].hex()`, the display reversal of Bitcoin hashes, and nothing in the note, the slide or any other note of the chapter explains it (only slide 17's note mentions little-endian, for heights).
2. Slide 19, undergraduate: the note is the full Nakamoto catch-up formula read out in words ("one minus the sum, for k from 0 to z, of that chance times one minus the closing chance"), with the Poisson law and the deficit z minus k named but not shown. A reader without probability cannot teach it. The fork half of the slide is fine.
3. Slides 9 and 19 (also 7 and 18, not in the sample), undergraduate: "the private chain" and "its regtest record" appear from slide 7 on and are first explained on slides 28 and 31. A reader who meets slide 9 first cannot say what the chain is.

## Check 2. No story repeated (DoD7_StoryNotRepeated)

Searched the full text and notes of the 13 other decks and the whole page for: merkle, Stanford, patent, the block numbers 91722, 91812, 91842, 91880, the identifiers d5d27987 and e3bf3d07, BIP 30, BIP 34, duplicate or repeated coinbase, Lopp, Jahr, testnet4, BIP 94, griefing, flood, Karl-Johan Alm, Anthony Towns, BIP 325, signet, Ralph, Haber, Stornetta.

Result: no story appears twice.
- Ralph Merkle and the 1979/1982 patent: told only in chapter 11 (deck slide 25, page story). Other decks mention the merkle tree as a concept (ch02, ch03, ch07 MAST, ch10 SPV, ch12, ch13) and as a code subject: counted as mentions. The patents in ch07 slide 54 and ch08 slides 23 and 48 are the Schnorr patent, a different story. Ch04 slide 8 (Stanford, 1976) is Diffie and Hellman, a different story.
- The two coinbases mined twice (blocks 91722 to 91880): not found in any other deck. Ch12 slide 17 ("BIP 34 height push: every coinbase differs"), slide 40 ("BIP 34 activation") and slide 48 (heights in code) are facts and a code example: counted as mentions, not retellings.
- Griefing the testnet (Lopp, Jahr): not found elsewhere. Ch12 slides 26 and 31 name "the BIP 94 branch" of testnet4 as a retarget rule and a code constant: a mention.
- Signet (Alm, Towns, BIP 325): the word signet does not occur in any other deck.
- Genesis headline: told in chapter 1 slide 7 (and slide 8); in chapter 11 it stays on slides 6, 12 and 13. I do not count slides 6, 12 and 13 as a retelling: slide 6 is a card definition, slide 12 names Nakamoto, slide 13 is a code example plus the fact of ten zeros, and none of them narrates who, why and what it answered. On the page, concept bodies 29 ("Genesis coinbase message") and 35 ("The Chancellor of the headline") restate that the headline proves the earliest date and marks the crisis, which is the same point as chapter 1, but node 35 adds new matter (Alistair Darling, Gordon Brown, the history of The Times) found in no other chapter. I count them as a fact and a taxonomy node, not a repeat. I agree with the owner's reason, with the caution that node 29's second sentence is close to chapter 1's wording.
- Inside chapter 11 the deck and the page tell each story once each (a deck slide and a page story card for the same story are one pairing, not a repeat).

No defect.

## Check 3. Evidence files

All five logs name deck and page by their versions in the header (some by file name v2_7_0 and v9_101_0, some also as 2.7.0 and 9.101.0) and carry the sha256 prefixes a2c340b130b560e9 (deck) and fc500aff7b091e05 (page); I recomputed both from the files and they match.
- ev_material_check_v1_3_0_deck_2_7_0.log: nine checks, all PASS, failed: 0. Matches "9 of 9".
- ev_deck_standard_deck_2_7_0.log: D1 to D12, 12 PASS, 0 FAIL, 0 not measured. Matches.
- ev_page_test_9_45_0_page_9_101_0.log: "widgets: 91 tested, 91 passed; failing: []", "failed: 0", no [FAIL] or [SKIP] lines. Matches. Observation: the body of the log appears twice (lines 4 to 206 and 207 to 413) with one header; the second copy differs from the first only in one line's wording. Not a failure.
- ev_code_frames_run_deck_2_7_0.log: 17 examples, 74 "ok" results, "shown results 74 failures 0", RESULT PASS. Matches. Observation: its last summary line names the manifest as "deck 2.5.0" (the header says the manifest is unchanged by 2.7.0, which explains it).
- ev_verify_v1_0_3_deck_2_7_0.log: "failures: []". Matches.
- Extra: ev_links_deck_2_7_0.log (not one of the five) is dated 2026-11-26 in its text and names the deck only, not the page; its three links answer 200.
- The material check passed "no-analogy 0/963" while check 5 below finds two residues; the automated check does not reach them.

No defect.

## Check 4. The new story and the dates

Dates: slide 25 and the page agree. Slide 25 says the tree dates from 1979 and the patent was published on 5 January 1982; page story, page concept 55, the lecture entry and the slide 20 note say the same; the 1980 paper is kept apart as the paper of 1980. No clash.

Slide 14 and the first page story (TwoCoinbasesThatRepeated):
- Helps the chapter: yes. It gives the problem (same bytes, same identifier, earlier coins overwritten) that slide 17 answers (height first in the coinbase), and slide 17's note points back to it. The lesson line is the reason for the height.
- Facts: I checked block times in 08-tooling/ch11-evidence: 91812 at 17:59:48 UTC and 91842 at 21:04:51 UTC on 14 November 2010 (about three hours), 91722 at 08:37 on 14 November and 91880 at 00:36 on 15 November (about sixteen hours). The notes and the page are right.
- 5N1K: how, what, when, where, who and why are all covered between slide, note and page. Who is the weak part: the 2010 miners are unrecorded, so the named people are the 2012 authors Pieter Wuille and Gavin Andresen. This is stated honestly on the page ("whose names the chain does not record"). Accepted.
- Real free picture with credit: yes, Bitcoin-qt 0.5.2, MIT, Wikimedia Commons, labelled as a stand-in on the slide and in the page credit.
- Live link: yes, https://bips.dev/30/ is a real hyperlink on the slide and answers 200.
- Remark, not a defect: the slide's visible text does not say what was lost (the earlier 50 coins became unspendable); that is only in the notes and the page. A student who reads only the slide does not see the reason that makes the story memorable.
- On the known and accepted items: (a) I partly disagree with the reason. "No free picture of the events exists" is true of a photograph, but a picture of the data (the two coinbase transactions side by side, or the block-explorer view of block 91842) is real and could be self-made and credited, as chapter 1 does with its hex dump. A 2012 client screenshot says nothing about 2010. I accept it because the owner allows labelled stand-ins. (b) and (c) I agree with.
- Remark: the slide pictures carry the file path as their alt text (for example "../../03-materials/ch11/assets/photo_ralph_merkle.png"), which is not a description. Not part of this DoD.

No defect.

## Check 5. Everyday analogy

Read: all 43 slides (titles, subtitles, balloons, captions, picture credits, notes), the four page stories, the 91 concept bodies and definitions, question bank, quiz, findings, agents, lecture entries and the page script's own texts. Stories of slides 33, 37, 38 and the four page stories are clean ("Free coins invite vandals" and "stays calm" are plain wording for the attacks and the effect, not an analogy).

Named:
4. Slide 29, concept card title "Testnet: Bitcoin's Testing Playground". It is the book's heading, but a playground is an everyday place of play used as a picture for a test chain. It sits in a visible card title. (The page does not carry this title.)
5. Page: the concept whose id is GlacierCoreAnalogy (label "Chain depth and stability"; also listed in the agent coverage, the BackLinks panel list, the question bank's concept key and the embedded ontology). The body itself is clean, but the id names an analogy (a glacier core) and finding 14 still speaks of "the book's picture of stable layers". The id is an identifier, not shown as a label, so how often a reader sees it depends on the ontology view; the finding text is shown to readers.

Seen and not counted: "Only one child continues the family line" (slide 10 note) extends the parent and child terms that are the standard names of blocks; "vouches" and "faucet" are idioms and the standard term; I judge them not analogies but the owner may want "family line" replaced.

DEFECTS FOUND: 5
1. Slide 16 academician: byte reversal `[::-1]` in the code is not explained in note or slide.
2. Slide 19 undergraduate: the catch-up formula is only read out in words, not teachable.
3. Slides 9 and 19 undergraduate (term used from slide 7): "private chain" and "regtest record" are not explained before slides 28 and 31.
4. Slide 29: card title "Testnet: Bitcoin's Testing Playground" is a play metaphor.
5. Page: id GlacierCoreAnalogy and the finding text "the book's picture of stable layers" keep the glacier-core analogy.
