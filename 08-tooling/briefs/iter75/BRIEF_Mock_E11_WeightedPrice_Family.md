# Brief for executor E11: a family of weighted-price numeric templates for the SEN0401 mock bank (owner order 2026-11-03 01:59, printed 2f)

Read ONLY this brief and MOCK_SCHEMA_AND_PLAN.md (same folder). Private output folder /home/claude/CME/exams/SEN0401/08-tooling/exam/mock/parts/ (all stem-bearing files PRIVATE; public repo gets only code without item text and logs without item text). Do not read the real exam item; its numbers and key are in the launch message only, to be avoided.

## Course point (chapter 1 critical points CP1.11 and CP1.02, deck chapter 1 slides "Two pizzas for ten thousand bitcoin" and the next)
A price is discovered by trades; a day figure is a volume-weighted average: each trade counts in proportion to how much was traded. A big trade moves the figure more than a small one, which is why it is not the plain average of the prices. The owner found the real question's sentence ("2 bitcoin traded at 60,000 dollars each and 3 at 70,000 dollars each") unclear and the extra conversion needless. So: every stem lists the trades as labelled lines ("Trade 1: 2 bitcoin sold at 60,000 dollars for each bitcoin"), no story needed (a one-line pizza or coffee frame is allowed only if it adds no step), and each template asks ONE thing.

## Task
Write mock_bank_ch1x_v1_0_0.json {"chapter":1,"family":"weighted_price","items":[6 to 8 numeric templates]} in the numeric schema (ids n1x_1.., points 3, can_be_4 on exactly one, 8 or more instances each with 8 different key values, field "why_question", tips without the prefix "Tip:"). Generator mock_numeric_gen_ch1x_v1_0_0.py (--out PATH; all values computed) and check mock_check_ch1x_v1_0_0.py with three planted defects that must fail. Stems at most 60 words counting the lines, line breaks "\n" between trade lines, last sentence "You are asked to ...". Define in the stem, in plain words, "the total dollars of a trade = bitcoin times dollars for each bitcoin" where the template needs it, and "the weighted price = total dollars of all trades divided by total bitcoin of all trades".
Templates (1 to 3 steps, ordered from simplest):
1 the total dollars of one trade (one step),
2 the total bitcoin of all trades and the total dollars of all trades: ask the total dollars (2 or 3 trades),
3 the weighted price of two trades (two steps, exact division),
4 the weighted price of three trades,
5 how much higher the weighted price is than the plain average of the trade prices (exact), 
6 the weighted price, then the value of N bitcoin in thousand dollars at that price (like the real item but with the unit said in the question and the trades on lines),
7, 8 optional: the price a new trade of a given size must have so that the weighted price becomes a given value (exact); how many bitcoin the second trade must be for a given weighted price.
Numbers: integers, exact divisions, prices 1,000 to 90,000 (round to thousands), bitcoin 1 to 12, keys at most five digits and not 0. Avoid the real item's two trades together and its key; no reuse of its wording.
Worked solution: every trade's total dollars on its own step, the totals, the division, the check against the plain average where useful; why_right; three common_wrong with the mistake in one sentence (took the plain average, forgot the sizes, divided by the number of trades).

## Fixed line (why_question)
"Why this question: a market price is not set by one person: it is found by trades, and a day figure counts each trade in proportion to its size. Working the weighted price step by step shows why a big trade moves the figure more than a small one."

## Checks and report
As in the brief for E10 (control script with --avoid when the launch message gives numbers; findings 0; 8 different keys per template; recompute equal; clarity NOT_MEASURED if no adapter; commit public code and logs only, private with git -C /home/claude/CME and push private). About 15 minutes.
