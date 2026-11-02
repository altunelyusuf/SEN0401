# Plan and brief: SEN0401 mock exam in HTML (owner change request, 2026-11-03 00:45 Istanbul)

Status: DEFERRED. Do not launch an executor before the exam set v7.2.0 is delivered to the owner (2 cores, Papers2 and Papers2 control running). Owner wording: an HTML mock exam for the SEN0401 course, after the real exam if time allows, with the option to derive new mock exams again, never reusing a question of the real exams (midterm v7.x).

## Goal
One self-contained HTML file per mock exam. A student opens it offline, answers, sees the score and, per item, the intention, the worked solution and the common wrong choice. Same plain-language rules as v7.2 (stem <= 60 words, one Tip, "You are asked to" last sentence).

## Never reuse (rule, checkable)
1. Keep a private reuse index: normalised stems and answer values of items v1.8.0 and every earlier midterm items version, in CME private/ (not in this public repo).
2. A new mock item passes only if (a) its normalised stem has similarity below 0.6 to every indexed stem and (b) its given numbers differ from the indexed item of the same topic in at least one input. Report each item with its nearest indexed stem and score.
3. Each derived mock records the item ids of earlier mocks, so mocks do not repeat each other either.

## Steps
1. Generator (parametric): one template per topic of chapters 1 to 8, numbers drawn from a seed, solution computed by code, so a new mock = a new seed. The generator and templates hold no real-exam text.
2. Reuse check as above (script, own tests with a planted copy that must fail).
3. HTML builder: items, bubbles/number boxes, local scoring in JavaScript (right = points else 0, as scoring module v2.0.0), solutions revealed after submit, print stylesheet. No external requests.
4. Readability and clarity checks of v7.2 applied to the mock items.
5. Verify: open in a browser engine headless, answer a seeded sheet, compare the score with the Python scoring; view every screen; leak scan: public repo holds no questions/answers.
6. Derive: command `make_mock SEED` produces the next mock; reuse check must pass or the build stops.

## Register
Owner change request CR3_MockExamHtml recorded Deferred in v0.1017. On launch: change route G125 route 2 (accept, retract, backlog story/tasks Build+Verify, brief via the brief script).
