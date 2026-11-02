# Brief for executor E9: a family of hash-search numeric templates for the SEN0401 mock bank (owner order 2026-11-03 01:50, printed 2d)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder: /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ . Public repo /home/claude/sen0401: code and logs only, no item text. Do not read the real exam item this family imitates; its numbers and key are in the launch message only, to be avoided.

## Course point (chapter 2 critical point CP2.12, deck chapter 4 slide "Second preimage: matching a given hash")
Mining is a search that nobody can shortcut but anyone can check with one hash. A hash of n bits has 2 to the n possible results, so finding one given result takes about 2 to the n tries; if the search accepts k results, it takes about 2 to the n divided by k tries; the time is the tries divided by the tries per second. The owner found the real question hard to understand and the arithmetic needless: so this family teaches the idea in plain steps, from ONE step up to two or three.

## Task
Write mock_bank_ch4x_v1_0_0.json: {"chapter":4,"family":"hash_search","items":[6 or more numeric templates]} in the NUMERIC schema of the plan (ids n4x_1.., type numeric, chapter 4, points 3, can_be_4 true on exactly one, unit, tip, 8 or more instances each; instance = stem, key_value, steps, why_right, common_wrong x3). Every template carries the field "why_question" = the fixed line below. At least 6 templates, 48 instances. Generator mock_numeric_gen_ch4x_v1_0_0.py (--out PATH; every value computed by code) and a check script mock_check_ch4x_v1_0_0.py with three planted defects that must fail; run and save logs.
Templates, ordered from the simplest:
1 (one step) how many tries it takes on average to find one given result of a hash with n bits (2 to the n; n from 3 to 15),
2 (one step) how many results a hash of n bits has / how many bits give N results (answer n),
3 (one step) how many seconds a machine needs for a given number of tries at a given speed,
4 (two steps) the average tries when the search accepts k results out of the 2 to the n,
5 (two steps) the seconds for finding one given result of an n-bit hash at a given speed,
6 (three steps, like the real item but with a clear stem) the seconds for a search that accepts k results of an n-bit hash at a given speed.
Up to 8 templates if time allows. Every instance has its own numbers and key_value (positive integer, at most five digits, exact: choose numbers so that every division is exact).
Stem rules: state every definition in plain words inside the stem ("A hash with 12 bits has 4,096 possible results" - compute it for the student only where the template is not about that step; do not write "target 16" and "16 results" together; say "the search accepts any result in a set of k results" instead of a target value). At most 60 words, last sentence starts "You are asked to", Tip at most 12 words with no prefix "Tip:" and not the real tip, abbreviations spelled out. Avoid the real item's combination of bits, accepted results and speed, and its key; do not reuse its wording ("A toy hash has ...", "A second search accepts ...").
Worked solution of every instance: ordered steps with the numbers (2 to the n, then the division by the accepted results, then the division by the speed), why_right, and for each common wrong value the mistake in one sentence (forgot to divide by the accepted results, gave tries instead of seconds, multiplied instead of divided).

## Fixed line (field why_question, identical in every template)
"Why this question: mining is a search that nobody can shorten except by accepting more results, and anyone can check an answer with one hash. Counting the tries shows why a bigger target makes mining faster and a smaller one slower."
(Adapt to the course wording; keep the meaning; add no fact the corpus lacks.)

## Checks
Run the lineage agent's control (python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_control_v1_0_0.py bank FILE --gen GENERATOR; it expects 23 items, so for the family file report its exclusion and recompute lines plus your own check), the clarity rules, and recompute by running the generator again. Commit public (code and logs only) with /tmp/cm.sh and private (git -C /home/claude/CME). Report hashes, counts, what is NOT measured. About 15 minutes.
