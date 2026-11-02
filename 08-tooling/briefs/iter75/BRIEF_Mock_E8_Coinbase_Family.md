# Brief for executor E8: a family of coinbase-claim numeric templates for the SEN0401 mock bank (owner order 2026-11-03 01:43 and 01:45)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder: /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ . Public repo /home/claude/sen0401: code and logs only, no item text. Do not read the real exam item this family imitates; its numbers are given below only to be avoided.

## Task
Write a file mock_bank_ch6x_v1_0_0.json: {"chapter":6,"family":"coinbase_claim","items":[6 or more numeric templates]} in the NUMERIC schema of the plan (id n6x_1.., type numeric, chapter 6, points 3, can_be_4 true on exactly one, unit, tip, 8 or more instances each; instances with stem, key_value, steps, why_right, common_wrong x3). Add to every template the field "why_question": the fixed line below. At least 6 templates, 48 instances. A generator script mock_numeric_gen_ch6x_v1_0_0.py (same rules as chapter 6: --out PATH, every key, step and wrong value computed by code from the numbers) and a check script mock_check_ch6x_v1_0_0.py with three planted defects that must fail; run and save logs.
The family: a toy chain whose block subsidy follows a halving schedule (start subsidy S, a halving every G blocks, fractions dropped), plus fees F, plus a claim C by the miner of block B. Templates (one each, different question, same chain of steps):
1 how many coins the claim exceeds the most the miner may claim (claim larger than the allowed maximum; exact answer a positive integer),
2 the most the miner may claim in block B (subsidy plus fees),
3 the subsidy in block B (several halvings),
4 how many coins the subsidy of blocks 0 to B-1 has created in total (all blocks of one group have the same subsidy; B a multiple of G or stated),
5 the first block number whose subsidy is 0 (fractions dropped),
6 the smallest fee that makes a given claim valid (claim minus subsidy, never below 0 - choose numbers so the answer is positive).
Add more templates if time allows (up to 8). Instances differ in G (2 to 12), S (a power of two or any positive integer 6 to 120), B, F and C; every instance has its own key_value; key_value an integer of at most five digits and not 0; the answer must not depend on a trick (no instance where the answer is 0 by accident).
Real item to AVOID (numbers and key): S 8, G 5, B 33, F 4, C 7, key 3. No instance may use the combination (S 8, G 5, B 33) with any F or C, and no stem may reuse the wording of that item: do not write "a toy-chain miner claims", use fresh situations ("a small test network", "a classroom chain", ...). Keep stems at most 60 words, plain English, last sentence "You are asked to ...", Tip at most 12 words, no prefix "Tip:", abbreviations spelled out; state the rule fully in the stem (each full group of G blocks halves the subsidy; block numbers start at 0; the miner may claim at most subsidy plus fees) so no hidden rule is needed.
Worked solution of every instance: ordered steps with the numbers (how many full groups: B divided by G rounded down; the subsidy after each halving; subsidy plus fees; the comparison), why_right, and for each common wrong value the mistake in one sentence (e.g. counted groups from 1, forgot the fees, halved once, used the claim as the limit).

## The fixed line (field why_question, identical in every template; the result view shows it)
"Why this question: the first transaction of a block, the coinbase, may claim at most the block subsidy plus the fees of the block. The subsidy is cut in half on a fixed schedule. Working it step by step shows why no miner can create more bitcoin than the rule allows, and why new coins become rarer."
(If the course corpus words the rule differently, keep this meaning and use the corpus words; do not add a fact the corpus lacks. Bitcoin's real schedule - halving every 210,000 blocks - may be named in one worked-solution step as the real case, only if the corpus says so.)

## Checks
Run the exclusion check of the plan on the family (the lineage agent's script: python3 -I /home/claude/sen0401/08-tooling/exam/sen0401_mock_control_v1_0_0.py bank FILE --gen GENERATOR; it expects 23 items per chapter file, so run it with the family flag when present, else report its structure line only and your own check), the clarity rules, and recompute by running the generator again. Commit public (code and logs, no item text) with /tmp/cm.sh and private (git -C /home/claude/CME). Report hashes, counts and what is NOT measured. About 15 minutes.
