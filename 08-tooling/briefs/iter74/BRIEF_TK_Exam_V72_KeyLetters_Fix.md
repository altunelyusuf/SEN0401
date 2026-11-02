# Brief: key letters fix for the exam set v7.2.0 (key only; paper and sheet stay as they are)

Found by the control: in the key, the worked solutions of the seven choice items 1a to 1g use the letters of the items file, but the paper prints the options in another order (the builder spreads the right letters over A to E). Example 1a: the key says "place 1a A" and then "Correct answer: B" and "Why A is wrong" about the option that is C on the paper. A grader cannot follow it. This is the owner's complaint (key and question must match).

Do, in this order:
1. New lib/builder/render copies v7_2_2 (committed files are not edited). In the key writer, for each ChoiceFour item, map every item letter in its worked-solution lines ("Correct answer: X.", "Why X is wrong:") to the letter the option has on the paper (map by option text, from paper['items'][i]['options'] against the items file); print the "Why L is wrong" lines in the order of the paper letters; leave every other line as it is.
2. Rebuild ONLY the key (docx and pdf, same seed 5701, form code 70017). The paper docx/pdf and sheet pdf must stay byte-identical: sha256 of the five existing files for paper and sheet must equal the values in SHA256.txt; a new SHA256.txt lists the new key files. Do not rebuild the paper.
3. Also in the key: print the word PROVISIONAL once, not twice, in each provisional note ("PROVISIONAL. PROVISIONAL." today).
4. Add a check (new script, own tests: a planted wrong letter must fail): for each of the seven choice items, the letter after "Correct answer:" equals the key place letter, the text after it equals the printed option with that letter, and for every "Why L is wrong" the letter L is a printed letter that is not the correct one and each of the four wrong letters appears once. Run it on the new key.
5. Re-run on the new key: how-to-grade on page 1, the page count (13 expected, report if it changes), PROVISIONAL flags Q4.a/b, Q4.c/d, Q1.g, leak scan, view every key page.
6. Commit CME private and public (code and logs only, no question or answer text) and report: the hashes, the check results, what was NOT done.
Not part of this task: the R6 case of the paper (wtxid in the bank before its expansion); the owner decides about it separately.
