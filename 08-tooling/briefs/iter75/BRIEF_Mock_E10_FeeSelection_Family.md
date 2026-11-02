# Brief for executor E10: a family of fee-selection numeric templates for the SEN0401 mock bank (owner order 2026-11-03 01:57, printed 2e)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ (generator, bank, check, all stem-bearing files: PRIVATE; public repo /home/claude/sen0401 gets only code without item text and logs without item text). Do not read the real exam item; its numbers and key are in the launch message only, to be avoided.

## Course point (chapter 2 critical point CP2.08, deck chapter 2 slides "Size in virtual bytes and the fee rate" and the next slide)
A block has limited room, so miners pick the best fee rate first: fee divided by size, not the biggest fee. The term "virtual byte" (vbyte) is real and taught in the course (the size unit a block limit counts); the owner found the real question's list unclear and the term unexplained. So: write the first mention as "size units (virtual bytes)" and then use "size units" only; define it once in plain words ("the unit in which the room of a block is counted").

## Task
Write mock_bank_ch2x_v1_0_0.json {"chapter":2,"family":"fee_selection","items":[6 to 8 numeric templates]} in the numeric schema of the plan (ids n2x_1.., points 3, can_be_4 true on exactly one, 8 or more instances each with 8 different key values, field "why_question" = the fixed line, no prefix "Tip:" in tips). Generator mock_numeric_gen_ch2x_v1_0_0.py (--out PATH; values computed by code) and check mock_check_ch2x_v1_0_0.py with three planted defects that must fail. LAYOUT OF EVERY STEM: the transactions as labelled lines, one per line, written with line breaks in the stem string ("\n"), like
"Transaction A: size 100 size units, fee 3,000 satoshis"
(a satoshi is the smallest bitcoin unit, explain once per stem in the first sentence or in the tip). No table written as "A 100, 3,000". The stem says in plain words which number is the size and which the fee. At most 60 words counting the lines. Last sentence starts "You are asked to".
Templates (1 to 3 steps):
1 the fee rate (fee per size unit) of one named transaction (one step, exact),
2 the highest fee rate among 3 to 5 transactions (the value),
3 how many transactions fit in a block when the miner takes them from the best fee rate and every one fits,
4 the total fee when the block takes the best rates until it is full (no skipping needed),
5 the total fee when a transaction that no longer fits is skipped and a smaller one after it still fits (like the real item but with 4 or 5 transactions and the lines above),
6 how much more fee the block earns by choosing by fee rate than by choosing the biggest fees first,
7, 8 optional: the room left after the miner stops; the lowest fee rate that still gets in.
Numbers: exact divisions, sizes 20 to 400, block rooms 100 to 900, keys at most five digits, nothing trivial (key not 0). Avoid the real item's block room, transaction sizes and fees together and its key; no reuse of its wording ("takes the highest fee per virtual byte first, skipping any that no longer fits").
Worked solution: the rate of each transaction on its own line of the steps, the order, the filling with the room left after each step, the sum; why_right; three common_wrong with the mistake in one sentence (ranked by fee not rate, forgot to skip, stopped at the first that does not fit).

## Fixed line (why_question)
"Why this question: a block has limited room, so miners take the best fee for the room first. Comparing fee per size unit shows why the biggest fee is not always the best pick."

## Checks and report
The lineage agent's control (python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_control_v1_0_0.py bank FILE --gen GENERATOR [--avoid=...]; family mode reads "family"): findings 0, exclusion containment below 0.35, recompute equal, 8 different keys per template; the clarity rules if an adapter exists else NOT_MEASURED; regeneration identical. Commit public (code and logs only) with /tmp/cm.sh and private (git -C /home/claude/CME) and push private. Report hashes, counts, what is NOT measured. About 15 minutes.
