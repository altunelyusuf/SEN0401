# Addendum to the brief of TK_Exam_V6_Papers_Build (read it as part of the brief)

Written by the lineage agent after the control of the Read, Sheet and Items builds (register v0.935, v0.936, v0.937).
It holds no question and no answer.

## Rule: penalties come from the scoring module
- The paper builder takes every penalty fraction, and every sentence about penalties that is printed on the paper, the key and the sheet, from the scoring module `08-tooling/exam/sen0401_exam_scoring_v1_0_0.py` and its rule file `sen0401_exam_scoring_rule_v1_0_0.json` (read only, public).
- For number and code-trace places, the structure v1.2.0 fields `guess_chance` and `penalty_fraction` (0, from five digit boxes) are NOT used. The module takes the guess chance from the digits of the key: a one-digit key costs 1/9, a two-digit key 1/99, three digits or more cost nothing extra (limit p below 0.005).
- For choice, matching, ordering and fill-in places the structure and the module agree (1/3, 1/5, 1/4, 1/3). Print the module's values.
- The printed directions must say the same as the module: one plain sentence for the rule, as the brief requires. Do not print a rule the key's scoring does not apply.
- The key file lists, per place, the penalty fraction the module gives, and the key's score for a sheet is computed with the module (a perfect sheet gives 100; a blind sheet gives about 0 on average).

## Also, from the Sheet and Items controls
- The sheet module `sen0401_exam_answersheet_v6_0_0.py` needs tips as a list of `{label, text}` pairs: take them from the tips of items v1.5.0 (`tips_by_label`), not from the stems.
- The answer lines for 5a and 5b on the sheet are 4 lines; the question pages give 6. Say so in the report.
- The sheet's page-2 note is longer than one sentence; the one plain sentence of the rule belongs in the paper's directions.
- Word pagination is NOT_MEASURED; say so.
- Run the readability tool (`sen0401_exam_readability_check_v1_0_0.py check`) on the finished paper and print its result as it stands; do not edit the tool or its rule.
