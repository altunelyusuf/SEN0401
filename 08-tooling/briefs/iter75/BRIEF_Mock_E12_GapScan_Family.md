# Brief for executor E12: a family of wallet-scan numeric templates for the SEN0401 mock bank (owner order 2026-11-03 02:06, printed 2g)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ (every stem-bearing file PRIVATE; the public repo /home/claude/sen0401 gets only code without item text and logs without item text). Do not read the real exam item; its used keys, gap limit and key are in the launch message only, to be avoided.

## Course point (chapter 5, critical point CP5.20, deck chapter 5 slide "Code 25: The gap limit decides how far a scan looks"; outcome LO-5)
A wallet rebuilt from its recovery code checks its keys in order and stops after a set number of unused keys in a row (the gap limit). A payment that arrived on a key after a longer stretch of unused keys is not found. The owner found the real question hard to follow, its logic a trap, and asked how it relates to the course. So: the rule stands as its own line, the data as its own line, and each template asks ONE plain thing; no hidden stop inside a gap unless the question asks plainly which payments are missed.

## Task
Write mock_bank_ch5x_v1_0_0.json {"chapter":5,"family":"gap_scan","items":[6 to 8 numeric templates]} in the numeric schema (ids n5x_1.., points 3, can_be_4 on exactly one, 8 or more instances each with 8 different key values, field "why_question", tips without the prefix "Tip:", steps each containing a number). Generator mock_numeric_gen_ch5x_v1_0_0.py (--out PATH; values computed by code) and check mock_check_ch5x_v1_0_0.py with three planted defects that must fail. STEM LAYOUT (line breaks "\\n"): first line the situation in one sentence, then "Rule: the scan stops after 20 unused keys in a row (the gap limit)." with the gap limit varying between instances (5 to 30), then "Keys that received a payment: 0, 9, 26" as its own line; keys are numbered from 0; "unused key" = a key that has received no payment, said once. At most 60 words, last sentence "You are asked to ...", tip at most 12 words.
Templates (1 to 3 steps):
1 (one step) the key number where the scan stops when it has seen the gap limit of unused keys after the last used key K (K plus the gap limit),
2 (one step) the longest run of unused keys between two used keys in the list,
3 (one step) how many keys in all the scan checks if it stops right after the gap limit of unused keys following the last used key, counting key 0,
4 (two steps) how many of the listed payments the scan finds when every run between used keys is shorter than the gap limit (count them) - choose lists so that a long run exists and the answer needs the stop,
5 (two steps) how many listed payments are NOT found (a payment after a run of the gap limit or more),
6 (three steps, like a real recovery) the number of keys the scan checks when the scan stops inside a long run (stated plainly, list and rule on their own lines),
7 the smallest gap limit that would find every listed payment (longest run plus one),
8 optional: the key number of the last payment the scan finds.
Numbers: exact integers, keys 0 to 400, key values at most five digits, not 0 except where the answer is truly 0 (avoid). Avoid the real item's used keys together with its gap limit and its key; do not reuse its wording ("A wallet rebuilt from its recovery code checks keys 0, 1, 2 and so on").
Worked solution: the unused runs written one per step with their lengths, the comparison with the gap limit, the stop, the count; why_right; three common_wrong with the mistake in one sentence (forgot key 0, counted to the next used key, used the gap limit as the count).

## Fixed line (why_question)
"Why this question: a wallet rebuilt from its recovery code looks only a limited distance ahead, so a payment that came after a long stretch of unused keys is not found. Working it step by step shows why a backup should note how far the wallet used its keys."

## Checks and report
The lineage agent's control (python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_control_v1_0_0.py bank FILE --gen GENERATOR --avoid=...) findings 0; the family adapter (python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_family_readability_adapter_v1_0_2.py FILE OUTDIR): R1 R2 R3 R4 R6 and C1 to C5 all PASS; regeneration identical; commit public (code and logs only) with /tmp/cm.sh, private with git -C /home/claude/CME and push private. About 15 minutes.
