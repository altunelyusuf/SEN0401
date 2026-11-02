# Brief for executor E8: a family of release-tag-order numeric templates for the SEN0401 mock bank (owner order 2026-11-03 01:43 to 01:46, corrected)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder: /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ . Public repo /home/claude/sen0401: code and logs only, no item text. Do not read the real exam item this family imitates; its list and key are given in the launch message only, to be avoided.

## Course point (chapter 3, critical point CP3.03, deck slide "Release tags sort by number, not by letters")
A software version is a sequence of numbers, not a word. A tool that sorts text compares characters from the left, so v10 lands before v9; sorting by number puts v9 first. The drill: list both orders, find each tag's two places, and measure how far the two orders differ.

## Task
Write mock_bank_ch3x_v1_0_0.json: {"chapter":3,"family":"release_tags","items":[6 or more numeric templates]} in the NUMERIC schema of the plan (ids n3x_1.., type numeric, chapter 3, points 3, can_be_4 true on exactly one, unit, tip, 8 or more instances each; instance = stem, key_value, steps, why_right, common_wrong x3). Every template carries the field "why_question" = the fixed line below. At least 6 templates, 48 instances. Generator mock_numeric_gen_ch3x_v1_0_0.py (as chapter 3: --out PATH; every order, place, move and key computed by code from the tag list) and a check script mock_check_ch3x_v1_0_0.py with three planted defects that must fail; run and save the logs.
Templates (one question each, same chain: text order, number order, places, gaps):
1 the sum of the moves of all tags (a move = the gap between a tag's place in the two orders),
2 the move of one named tag,
3 how many tags change place,
4 the place of one named tag in the text order (or the tag at a given place in the number order),
5 the largest move among the tags,
6 how many pairs of tags stand in a different relative order in the two orders.
Up to 8 templates if time allows. Instances: 4 to 7 tags each, different lists (use two-digit and one-digit majors, and some with minor numbers like v4.10 against v4.9), tags written as v<major>.<minor>; every instance's two orders must differ (key not 0), key_value at most five digits, each instance with its own list. NOT the real list and not a list that gives the real key with the same tag count; no stem may reuse the real wording ("Six release tags ... A tag's move is the gap ..."): write the definition of a move in your own words and state it fully so no hidden rule is needed.
Stem at most 60 words, plain English, last sentence starts "You are asked to", Tip at most 12 words with no prefix "Tip:" and not the real tip's wording (for example "Text order compares one character at a time from the left."), abbreviations spelled out.
Worked solution of every instance: the text order written out, the number order written out, each tag's two places and its gap, then the asked value; plus why_right and for each common wrong value the mistake in one sentence (e.g. counted only the tags that change place, summed one direction only, ranked by text twice).

## Fixed line (field why_question, identical in every template; the result view shows it)
"Why this question: a software version is a sequence of numbers, not a word. A tool that sorts text puts v10 before v9, so someone who trusts text order picks the wrong release. Listing both orders step by step shows how far they differ."
(Adapt to the course's own wording on the slide if it differs; keep the meaning and add no fact the corpus lacks.)

## Checks
Run the lineage agent's control (python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_control_v1_0_0.py bank FILE --gen GENERATOR; it expects 23 items; for the family file report its exclusion and recompute lines and your own check), the clarity rules, and recompute by running the generator again. Commit public (code and logs only) with /tmp/cm.sh and private (git -C /home/claude/CME). Report hashes, counts, what is NOT measured. About 15 minutes.
