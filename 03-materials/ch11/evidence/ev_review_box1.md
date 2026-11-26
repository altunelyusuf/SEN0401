# Independent review, SEN0401 chapter 11, lineage 7 box 1

Reviewer read the deck (v2.5.0, 43 slides) with python-pptx, the page (v9.99.0) as text, the newest decks of chapters 1-10 and 12-14, and the five evidence logs. No file was changed except this one.

## Check 1, notes teach (DoD7_NotesTeach), slides 3, 6, 7, 15, 19, 21, 29, 31, 38, 40

Word counts of the ten notes: 113, 110, 104, 102, 105, 113, 94, 97, 106, 94. All are inside 60-140 (30-140 on opening/divider/closing). No presenter directions, no "think of", no everyday analogy found. Notes address the reader ("Retell...", "try each question") which is reader-facing, not presenter-facing.

| Slide | Academician | Undergraduate |
|---|---|---|
| 3 (seven questions) | yes: maps each question to the slide that answers it | yes (it is a map of the chapter, answers live on other slides; the note does not itself answer the seven questions) |
| 6 (concepts 1 of 5) | yes: all four definitions restated in full sentences | yes |
| 7 (genesis size, example 1) | yes: 80 + 1 + 204 = 285, compared with Core's own figure | yes |
| 15 (concepts 5 of 5) | yes | yes |
| 19 (fork, catch-up odds) | NO: the note says "the formula from the white paper" and gives four outputs, but states neither the formula nor its model (attacker share q, z blocks behind, random walk); the slide cannot be taught from the note alone | NO: "ever catches up" and "z blocks behind" are not explained, so the numbers 0.2045873, 0.0509779, 0.0002428 are reported but not understood |
| 21 (Merkle concepts 1 of 2) | yes | yes |
| 29 (test chains 1 of 5) | yes | yes |
| 31 (test chains 2 of 5) | yes | yes |
| 38 (signet story) | yes | NO: "challenge script", "one-of-two multisig" and "four magic bytes" are used without a meaning in the note; the story's mechanism is only named |
| 40 (regtest halving, example 17) | yes | yes |

Nos: slide 19 (both readers), slide 38 (undergraduate). Expected result (yes on all twenty answers) does not hold: 3 of 20 answers are no.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched notes and slide text (including tables) of the newest decks of chapters 1-10 and 12-14, and the chapter 11 page (v9.99.0).

Counting rule: a retelling is the same event or person-and-event pair narrated (who, when, what happened). A name, a date or a one-line pointer is a mention.

1. Headline in the genesis block (Satoshi Nakamoto, 2009-01-03). REPEATED.
   - Chapter 1 deck, slide 7 "A newspaper headline carved into block zero" (story slide, Satoshi Nakamoto, 3 January 2009, mined block 0, typed the Times headline "Chancellor on brink of second bailout for banks", it proves the block is not older and records the banking crisis, link to the block on mempool.space) and slide 8 "The headline inside block zero" (reads the same 69 bytes). Chapter 1 slide 3 also carries it as a beat.
   - Chapter 11 deck, slide 14 "The Times in the first block" tells the same event with the same point (date proof plus banking-crisis hint), slides 12-13 repeat the headline in a card and in code (example 4).
   - Counted as a retelling: Ch1 slide 7 (and slide 8 code) against Ch11 slide 14. Counted as mentions only: Ch2 slides 42-43 (genesis header hash, "mined on 3 January 2009"), Ch3, Ch13 slide 46 (hashing the genesis header), Ch1 slide 3 beat summary.
   - Chapter 11 page: carries the headline in the example "69 characters on 3 January 2009", the subject "The Chancellor of the headline" and the Stories tab. Counted as the same chapter's companion telling of its own story, not a cross-chapter repeat, but it does tell it a further time in the page alongside the deck.
2. Hash tree of Ralph Merkle (1982). Not repeated. No other deck names Ralph Merkle, patent 4,309,569 or the 1979/1982 dates. Other decks (Ch2 slides 43 and 54, Ch3 slides 46-47, Ch10 slides 118-127) teach the Merkle tree and Merkle path as a mechanism; counted as concept teaching, not the story. The page repeats it only as the chapter's own companion (Stories tab, "Hash tree history").
3. Griefing the testnet (Jameson Lopp, Fabian Jahr, 2024). Not repeated. Neither name nor "Griefing Bitcoin's Testnet" appears in any other deck. Ch12 slides 102-103 and 122-123 mention BIP 94 and testnet4 as a retarget branch only (counted as a mention of the rule, not the 2024 event).
4. Signet blocks need a signature (Karl-Johan Alm, Anthony Towns, 2019). Not repeated. No other deck names them or BIP 325.

Result: one story appears twice across chapters (the genesis headline: Chapter 1 slides 7-8 and Chapter 11 slide 14). Expected result does not hold.

## Check 3, evidence files in 03-materials/ch11/evidence/

- ev_material_check_v1_3_0.log: nine checks listed, all PASS (title-words, visual-present, notes-words, notes-labels, no-prompts, code-parses, no-lambda 0 occurrences, code-in-page, no-analogy). Says 9 of 9 PASS by count, though the file has no literal "9 of 9" summary line. OK.
- ev_deck_standard.log: "SUMMARY PASS=12 FAIL=0 NOT_MEASURED=0", RESULT PASS. OK. (Note: the file's own D5 line says 4 of 4 story slides complete, and D7 says all notes 60-140 words.)
- ev_code_frames_run.log: 74 "ok" lines, no non-ok line, final line "examples 17 shown results 74 failures 0", RESULT PASS. OK.
- ev_page_test_9_45_0.log: no FAIL line; 394 PASS lines (the run blocks appear twice in the file, so each check is listed twice); line "widgets: 91 tested, 91 passed; failing: []". It never prints the words "0 failed" and never names the page file tested (v9.99.0), the only version link being "manifest chapter_code_ch11_v1_2_0.json" and "page-standard 9.52". The claim "0 failed and 91 of 91 widgets" is supported in substance, but the log does not itself show which page version it ran against.
- ev_material_check_v1_0_0.log: still says no-lambda FAIL with page_occurrences=5. The file stays in the evidence folder with a FAIL and has no note saying it is superseded by 1.3.0. Not a claimed pass, but a reader opening the folder sees a FAIL.

Lambda claim, verified on the page: the chapter code manifest (chapter_code_ch11_v1_2_0.json) has 0 occurrences and the deck has 0. In the page, whole-word "lambda" occurs 8 times (the checker's 5 comes from a different match rule), and none is chapter code: (a) the keyword glossary entries "lambda: small unnamed function" and "lambda - a small unnamed function" (several copies in the embedded data); (b) the page's own code-analyser table mapping ast.Lambda to 'small unnamed function'; (c) the keyword list inside a JavaScript regex (highlighter); (d) one prose sentence of the page's data, "meets no lambda that nobody taught". The builder's claim is true that none is code, but "five keyword glossary entries" is imprecise: they are glossary entries, tool source (analyser and highlighter) and one prose sentence, not five glossary entries. No-lambda condition holds for code.

## Defects

DEFECTS FOUND: 5
1. Check 2: the genesis-block headline story is told in Chapter 1 (slides 7 and 8) and again in Chapter 11 (slide 14, with slides 12-13); a retelling, not a mention.
2. Check 1: slide 19 note is not self-sufficient for either reader (the catch-up formula and its meaning are not stated).
3. Check 1: slide 38 note is not self-sufficient for the undergraduate reader (challenge script, one-of-two multisig and magic bytes are not explained).
4. Check 3: ev_page_test_9_45_0.log does not name the page version it tested (v9.99.0) and has no "0 failed" line (only "failing: []" and no FAIL lines); the run blocks appear twice.
5. Check 3: ev_material_check_v1_0_0.log still shows no-lambda FAIL (page_occurrences=5) with no note that it is superseded; the builder's description of the five matches (glossary entries) is imprecise, though no lambda is in any code.
