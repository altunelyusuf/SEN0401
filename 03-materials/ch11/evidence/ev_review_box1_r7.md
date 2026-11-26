# Review 7, SEN0401 chapter 11, lineage 7 box 1

Reviewer: independent (did not read ev_review_box1.md or _r2 to _r6). Files only read; this file is the only thing written.
Material: deck SEN0401_Ch11_TheBlockchain_3e_v2_7_0.pptx (43 slides), page sen0401_ch11_page_v9_101_0.html, newest decks of chapters 01 to 10 and 12 to 14 (ch01 3.7.0, ch02 3.3.0, ch03 3.3.1, ch04 3.9.0, ch05 3.8.0, ch06 2.5.0, ch07 2.7.0, ch08 2.5.0, ch09 2.2.0, ch10 2.4.0, ch12 3.1.0, ch13 2.5.0, ch14 2.2.0). Decks read with python-pptx 1.0.2 (slide text, grouped shapes, tables, notes). Page read from its JSON data blocks (nodes, definitions, stories, lecture, findings, question bank, quiz, agents, mission, resources, notice) and its script strings.

## Check 1, notes teach (DoD7_NotesTeach)

The fifteen slides are 1, 7, 9, 11, 16, 19, 20, 29, 31, 33, 35, 37, 40, 41, 42 (drawn set plus 7, 9, 16, 19, 29, each counted once).
Words per note: 1:113, 7:129, 9:121, 11:114, 16:116, 19:131, 20:97, 29:94, 31:97, 33:107, 35:97, 37:83, 40:94, 41:100, 42:102. All inside 60 to 140 (30 to 140 for slides 1, 20 and 42). No presenter directions and no "think of" in any of the 43 notes. The only imperatives are "Retell ..." and "Compare ..." addressed to the reader, which the owner allows. No everyday analogy in these notes.

| Slide | Academician | Undergraduate |
|---|---|---|
| 1 | yes: names the four topics, the evidence rule and the order of the seventeen examples | yes: same |
| 7 | yes: 80 + 1 + 204 = 285 and the Core comparison are all in the note, regtest is defined | yes |
| 9 | yes: six fields, widths, cut points, bits 207fffff | yes (layout is the point of the slide; what each field is for comes on later slides) |
| 11 | yes: epoch seconds, median of eleven, bits as exponent and coefficient, difficulty ratio, the three results | yes, with a small remark: the step from exponent 1d to the power 26 (29 minus 3) is not shown, and the median-time value comes from the private chain without the note saying so |
| 16 | yes: hash once vs twice, reversed byte order, name not stored | yes |
| 19 | yes: formula, q and p, lambda, the four probabilities | yes (the Poisson term is named, which is enough for the slide) |
| 20 | yes | yes |
| 29 | yes | yes (cards are echoed; faucet and minimum-difficulty rule are met again on slide 33) |
| 31 | yes | yes (challenge script is defined on slide 37) |
| 33 | yes | yes |
| 35 | yes | yes |
| 37 | NO | NO |
| 40 | yes | yes |
| 41 | NO | NO |
| 42 | yes (the Chainlink Merkle-tree video of the slide is the only entry the note leaves out) | yes |

Item D1, slide 37, both readers: the note says the four message-start bytes "are the first four bytes of the hash of that script". A reader who teaches this and recomputes it gets a different value. The library (L.signet_magic, sen0401_ch11_lib_v1_1_0.py line 197) hashes the challenge with its length byte in front: sha256d(bytes.fromhex('51'))[:4] gives 953ccfa5, while sha256d(bytes.fromhex('0151'))[:4] gives 54d26fbd, the value on the slide. The note (and the slide's own sentence "the start of the hash of that script") omit the length prefix, and the undergraduate additionally is not told what message-start bytes are for. The same omission stands in: slide 37 slide text (item 2 and the takeaway), slide 38 slide text (item 3) and note ("first four bytes of the double SHA-256 hash of that script"), the page story SignetBlocksNeedASignature, the page lecture entries for slides 37 and 38, and page finding 24. The page concept node (signet magic body) is right ("with its length in front"), so deck and page disagree with each other.

Item D2, slide 41, both readers: the note only says where each of the five lines is proven (genesis and header slides, broken chain and fork, merkle path, weakness slide, test chain slides). It never states the five lines (double hash name, 80-byte six-field header, linked parents and the longer branch, merkle root and path, the repeated-last-hash weakness and Core refusing the copy, three test chains with the same rules and other constants). A reader with only the note cannot teach or even say what the chapter claims; the note explains the order of proof, not the slide's wording.

## Check 2, no story repeated (DoD7_StoryNotRepeated)

Searched all notes and slide text of the thirteen other decks, and the whole ch11 page text, for: Merkle 1982 patent / Stanford / 4,309,569; blocks 91722, 91812, 91842, 91880, d5d27987, e3bf3d07, BIP 30, duplicate or repeated coinbase; Lopp, Jahr, griefing, BIP 94, testnet3 flood; Alm, Towns, BIP 325, signet, signed test network.

Result: no story appears twice. Counted as mentions, not retellings:
- Merkle tree appears in ch02 (slides on block header, merkle tree, SPV), ch03 (rebuilding a merkle root of block 123,456, code), ch07 (definition cards), ch10 (light client merkle path), ch12 (merkle root checks, extra nonce), ch13 (merkle root of the first block). All are concept or code; none tells Merkle, 1979 to 1982, the patent or Stanford. Ch04 tells Diffie and Hellman at Stanford (1976), ch08 the Schnorr patent, ch13 Shamir 1979: different persons and events.
- BIP 34 and BIP 94 appear in ch12 (cards "BIP 34 height push", "BIP 34 activation", "The BIP 94 branch", constants code, heights 227,931 for BIP 34): facts and code, no coinbase-repeat story and no flood story. No other deck contains the words signet, Lopp, Jahr, Alm, Towns, testnet3, 91842, 91812, 91722, 91880 or BIP 30.
- Inside the ch11 page, each story is told once as its story card. The deck note of its slide is mirrored in the page lecture panel (same telling shown in two views, not a second telling). Concept bodies carry the same facts (node on the hash tree history: 1979, patent number, 5 January 1982; testnet4 and block-storm nodes; signet nodes; BIP 34 node), stated as facts of a concept, not told as an event. Counted as mentions.

Genesis block headline: still on ch11 slides 6 (card), 12 (nakamoto card) and 13 (code slide, full headline quoted, hash zeros, time field) and in page nodes (message, Alistair Darling and The Times background). I do not count it as a retelling. Chapter 1 slide 7 tells it as an event (who, when, why: a typed headline that dates the block and records the banking crisis). Chapter 11 reads the 69 bytes as a code example and a header fact, with no who-why narrative, and slide 13's note ends by pointing forward to the coinbase story. The chapter 1 deck itself also has the same headline as a code slide (its slide 8), which confirms the pattern: story once, code example elsewhere. Slide 13 is the nearest to the line (its title is "The first block quotes a newspaper" and the note quotes the full headline), but it adds nothing narrative.

## Check 3, evidence files

All five files name deck 2.7.0 and page 9.101.0 (headers give the file paths with versions and sha256 prefixes b1ce38eba01f417f for the deck and 795c1e7eebb5660b for the page; I recomputed both from the files and they match).
- ev_material_check_v1_3_0_deck_2_7_0.log: nine checks, nine PASS, failed 0. Matches 9 of 9.
- ev_deck_standard_deck_2_7_0.log: D1 to D12, SUMMARY PASS=12 FAIL=0. Matches 12 of 12.
- ev_page_test_9_45_0_page_9_101_0.log: "widgets: 91 tested, 91 passed; failing: []", no FAIL line, final "failed: 0", header names page 9.101.0 and deck 2.7.0. Matches.
- ev_code_frames_run_deck_2_7_0.log: 17 examples, 74 "ok" lines, "examples 17 shown results 74 failures 0", RESULT PASS. Matches. The closing line quotes the manifest's own recorded deck (2.5.0), which the header explains (the manifest is unchanged by 2.7.0); no defect.
- ev_verify_v1_0_3_deck_2_7_0.log: "failures: []". Matches.
No file fails to name the versions. (ev_links_deck_2_7_0.log, not in the brief, is dated 2026-11-26 and lists bips.dev/30 and the Wikimedia page as 200.)

## Check 4, the new story and the dates

- Date of the hash tree of Ralph Merkle: slide 25 ("dates from 1979; on 5 January 1982 ... patent 4,309,569") and its note, the page story ("dates from 1979 ... published on 5 January 1982"), the page concept node, lecture panel, findings and question bank, and slide 20's note ("patent of 1982") read the same. No conflicting date found. Yes.
- Story of slide 14 and first page story (TwoCoinbasesThatRepeated): helps the chapter and is memorable: it sets up the reason for the height in the coinbase (slide 17, which the note of slide 14 points to), with a one-line lesson. I checked the facts against the saved block files in 08-tooling/ch11-evidence: 91812 at 17:59:48 UTC and 91842 at 21:04:51 UTC on 14 November (three hours), 91722 at 08:37 on 14 November and 91880 at 00:36 on 15 November (about sixteen hours): all as written. Real names: Pieter Wuille (BIP 30), Gavin Andresen (BIP 34); the 2010 miners are stated to be unrecorded, which is honest. Picture: the labelled stand-in, with credit (Bitcoin developers, MIT, Wikimedia Commons, 2012-02-21). Live link: BIP 30 at bips.dev, a hyperlink on slide 14, answered 200. 5N1K is complete and unlabelled. Answers: yes on all. No "no" to name.
- Stand-in (a): accepted. I agree, the credit says plainly that it is a stand-in and its date (February 2012) matches the month BIP 30 was written.
- Remark, not counted: neither slide 14 nor the page says that block 91880 was mined on 15 November UTC (the brief says 14 to 15 November); they write "On 14 November" only for 91812 and 91842 and say the other two "did the same".
- Remark, not counted: the page story of Merkle opens with "Go back to Stanford University in California." which reads as an instruction to the reader and echoes chapter 4's Stanford setting. It is not a repeat of that story.

## Check 5, everyday analogy

Searched all deck text and notes, picture credits, and the page text (concept bodies and definitions, notes, question bank, quiz, findings, lecture panel, stories, agents, resources, mission, UI strings) with a broad list of comparison markers (like a, as if, imagine, think of, resembles, analogy, everyday objects and places, and many typical blockchain analogies such as fingerprint, seal, puzzle, lottery, ledger, notebook, treasure, vault, post). No everyday analogy found. Wording I considered and did not count, because each names the real behaviour and compares it to no everyday situation: "bundles of transactions" (slide 10 and its lecture entry), "squeezes thousands of transactions into one hash" (slide 20), "vouches" (slide 25), "invite vandals" and "invitation to vandals" and the lesson "rules against vandals" (slide 33, page story), "stays calm" (slides 31 and 38, page). If the owner reads vandals as a comparison with property damage, it would be one item (slide 33 text and note, page story GriefingTheTestnet, its lesson). The Playground menu item (b) is accepted.

Reason (d): I disagree with its reasoning, not its outcome. The page's own notice says its browser runtime is Pyodide, Python 3.13.2, and that the results equal what the research recorded under Python 3.14.6; its header says 3.13.18. So 3.14.6 is the interpreter of the recorded research run, not of the page that runs the code. The code slides' footer "run under Python 3.14.6 - L is the chapter library of the page, R its regtest record" can therefore be read as the page running 3.14.6. Three interpreter versions on one page (3.13.18, 3.13.2, 3.14.6) are worth one sentence of explanation. Not counted.

## Result

DEFECTS FOUND: 2
1. Slide 37 note (both readers): signet magic bytes described as the start of the hash of the script; the length byte is missing, a reader gets 953ccfa5 instead of 54d26fbd. Same wording in slide 37 text, slide 38 text and note, the page signet story, the page lecture entries for 37 and 38 and finding 24 (the page concept node is right).
2. Slide 41 note (both readers): states where each line is proven but never states the five lines, so the slide cannot be taught from the note alone.
