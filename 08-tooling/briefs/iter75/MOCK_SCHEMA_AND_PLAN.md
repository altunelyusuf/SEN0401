# SEN0401 mock exams in HTML - plan, bank design and data schema (owner order 2026-11-03 01:29 Istanbul, top priority)

## What the owner fixed
Scope chapters 1 to 6. Same four question formats and scoring as the real midterm: 5 alternatives, right = points, wrong or blank = 0, no deduction, no bonus. Every item NEW: never an item of any delivered exam (v7.2 and earlier). Each mock = one self-contained HTML file, local scoring, worked solution shown after submit, a "Derive a new mock" button, seeded generator. Stems in plain English, last sentence "You are asked to ...", Tip at most 12 words, print and phone friendly, no student personal data. Real items and answers never in a public repo or in the HTML. All mock files and the bank go to PRIVATE CME: /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/ . Public SEN0401 holds code and logs only (no stems, options, answers, solutions).

## A mock (same shape as the real exam, 100 points, 21 places)
- Q1 (25): 7 choice items, points 3,3,3,4,4,4,4 (order shuffled).
- Q2 (25): 8 numeric items (digits in boxes, at most five characters), points 3,3,3,3,3,3,3,4.
- Q3 (25): 3a matching 4 rows (3 points a row), 3b matching 4 rows (2 points a row), 3c ordering 5 steps (1 point a step).
- Q4 (25): 3 fill-in groups of two blanks (4+4, 4+4, 5+4 points).
Chapters 1 to 6 covered in every mock; no more than 2 choice items of one chapter in Q1.

## Bank (what one chapter executor writes, per chapter; 6 chapters)
| unit | per chapter | total | one mock uses |
|---|---|---|---|
| choice | 10 (4 of 3 points, 6 of 4 points) | 60 | 7 |
| numeric template (8 instances each, all different numbers and answers) | 4 | 24 templates, 192 instances | 8 instances |
| matching set (4 premises, 5 responses, one unused) | 3 | 18 | 2 |
| ordering set (5 steps) | 2 | 12 | 1 |
| fill-in group (bank of 5 entries, 2 blanks) | 4 | 24 | 3 |
Note numeric points: per chapter 4 templates, points 3,3,3,4 are NOT needed; the shell gives the 4-point place to the mock's last numeric draw, so every template carries "points": 3 and the shell raises one to 4 only if the template has "can_be_4": true (set it true on one template per chapter).
Fully disjoint mocks: choice 60/7 = 8, matching 18/2 = 9, ordering 12, fill 24/3 = 8, numeric instances 8 per template = 8 -> THE BANK SUPPORTS 8 MOCKS THAT NEVER SHARE AN ITEM. Mock number 9 and later reuse items of earlier mocks (never of the real exam); the page says so. (Numeric items count as different when any number in the stem and the answer differ.)

## Data schema (JSON, one file per chapter: mock/parts/mock_bank_ch{N}_v1_0_0.json). Letters are NEVER written in solutions: refer to options by index (the page prints the letters after it shuffles). Lesson from the real exam key (letters out of step with the paper).
{ "chapter": N, "items": [ ... ] } with
- choice: {"id":"c{N}_01","type":"choice","chapter":N,"points":3|4,"stem":"... You are asked to ...","tip":"<=12 words","options":[5 strings],"answer":0-4,"steps":["..."],"why_right":"...","why_wrong":{"<option index as string>":"..."} (the four wrong indices)}
- numeric: {"id":"n{N}_1","type":"numeric","chapter":N,"points":3,"can_be_4":bool,"unit":"...","tip":"...","instances":[8 x {"stem":"...You are asked to calculate ...","key_value":int,"steps":["... with numbers, 2 or more"],"why_right":"...","common_wrong":[{"value":int,"why":"..."} x3]}]}  (key_value non-negative integer of at most 5 digits; instances produced by a script in the same folder and recomputed by running code)
- matching: {"id":"m{N}_1","type":"matching","chapter":N,"intro":"... You are asked to match ... one response is not used.","tip":"...","premises":[4],"responses":[5],"answer":[4 response indices, distinct],"steps":["..."],"why_right":"...","why_wrong_rows":[4 x "why the other responses fail for this row"]}
- ordering: {"id":"o{N}_1","type":"ordering","chapter":N,"intro":"... You are asked to put ... in order ...","tip":"...","steps":[5 statements, in a DISPLAY order that is not the right order],"answer":[5 integers: the place (1..5) of each statement as displayed],"steps_solution":["..."],"why_right":"...","why_wrong_rows":[5 x "..."]}
- fill: {"id":"f{N}_1","type":"fill","chapter":N,"stem":"... You are asked to fill each blank with the bank entry that makes the sentence true.","tip":"...","bank":[5 entries],"blanks":[{"sentence":"... ____ ...","answer":idx},{"sentence":"... ____ ...","answer":idx}],"steps":["..."],"why_right":"...","why_wrong_entries":{"<bank index>":"why that entry fails"}}

## Rules every item meets (same as the real exam, rule files in 08-tooling/exam: readability v1.1.0 R1 to R6, clarity C1 to C5)
Stem at most 60 words; one Tip of at most 12 words; abbreviations spelled out at first use; no reference to something unexplained (story, above, as before); last sentence of a stem starts "You are asked to"; four wrong options of a choice item are plausible, distinct, similar length (longest at most 3 times the shortest), one right answer; solutions have ordered steps, why_right, why_wrong for every other option or row.
Content comes from the course corpus and chapters 1 to 6 of the course (slides, textbook ontology, critical points in 08-tooling/exam). No code-trace items (owner 2026-11-02). Where a fact is not in the corpus, use no real historic fact.

## NEW items only: the exclusion gate
Index (private, mock/exclusion/): normalised stems, options, premises, blanks and key values of EVERY delivered exam item: all CME private items files (sen0401_exam_items_*.json, v1.x to v1.8.0), all papers_midterm_v* folders (docx text of paper and key), and the real paper v7.2.0. A mock item passes only if (a) token 5-gram Jaccard similarity of its stem to every indexed stem is below 0.35 and word-level similarity below 0.6, (b) none of its options or premises equals an indexed one (normalised), (c) for numeric, its key_value with the same unit is not an indexed key value for a stem of similarity above 0.3. The report lists every item with its nearest indexed stem and score. Planted-copy fixture: a verbatim copy, a copy with numbers changed only, and a copy with two words changed must each FAIL; a genuinely new item must pass. The gate also runs on the finished HTML (reads the embedded bank).

## Work split (parallel executors) and clock
Start T. E1..E6: one chapter each (items for the chapter, own check script with the clarity rules, a Python generator and recomputation for numeric instances) - about 30 min. E7: HTML shell + derivation + scoring + exclusion gate tool + planted fixtures - about 35 min, works on a tiny sample bank. Then ASSEMBLY (E7 or me): merge six chapter files, run exclusion gate, clarity C1-C5 on the whole bank, scoring recomputed by code for 3 derived mocks, build the 8 disjoint mock HTML files plus the master (derive button) - about 20 min. Control by the lineage agent in parallel from T+30 min. Estimated first usable mock T+60 to T+75 min, all checks T+80 min. Fast path if the owner needs less: halve the bank (5 choice, 2 numeric templates, ...) = 4 disjoint mocks, about T+45 min; not chosen unless the owner says so.
Machine: 2 cores; authoring is light; browser tests under flock /tmp/page_test.lock; nice 10 for heavy runs.
