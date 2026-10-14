# Building a SEN0401 chapter (8-14) to the SEN0414 chapter-24 standard - README_BUILD v1.0.0

Written 2026-10-14. Everything below was run, in a scratch copy of the repository, on chapter 7 and on a generated demonstration chapter 99. Nothing here edits
`03-materials`, `07-lineage` or any existing file. Book chapter N is course chapter N (8 Digital Signatures, 9 Transaction Fees, 10 The Bitcoin Network,
11 The Blockchain, 12 Mining and Consensus, 13 Bitcoin Security, 14 Second-Layer Applications); the legacy 2025 deck numbering differs.

## 1. Decision

(b) for research, deck checks and the page test; (a) for the page chain.

| Stage | SEN0401 ch06/07 (as built) | SEN0414 newest (ch24) | Decision |
|---|---|---|---|
| Research source | bespoke corpus (`sen0401_ch07_text_a..i`, 84 concepts, 4-6 paragraphs each, `research_gen`) | data module (`sen0414_ch24_rdodi_data`) + generic builder 1.2.0 | (b) data module + `sen0401_rdodi_build_v1_1_0.py`; `sen0401_chNN_corpus` is a 20-line bridge that derives NODES from the data module so research and deck cannot drift |
| Gates | `sen0401_rdodi_gates_v1_0_0.py` (needs exact AV, ecosystem as argument) | v1_1_1, pinned ecosystem, newest part per file | `sen0401_rdodi_gates_v1_2_0.py` (pin default, newest parts) |
| Claim execution | checks v1_0_0 (BEH) | checks v1_2_0 | v1_0_0 is the same contract; used unchanged |
| Deck engine | each chapter copies a 486-line `deck_build` | same, per chapter | `sen0401_deck_engine_v1_0_0.py` (helpers + all refusals), plan byte-identical to ch07's |
| Renderer | shared `deck_render_v1_0_0.js`; console rows NOT syntax-coloured | shared + chapter wrapper (`shapes`, `foot`, `cellMargin`) | `sen0401_deck_render_v1_0_0.js` adds `shapes`, `foot`, `cellMargin` and colours console statements |
| Deck checks | one chapter script (rows only) | deck/program/diagram/honesty/links/structure/layout/fit/notes/picture + 17 stale fixtures | `sen0401_deck_*_check`, `sen0401_story_check`, `sen0401_deck_fixtures` (13 refusals + control) |
| Page | builder 4.14.0 (generic, `NN`), template 9.44.0, test 9.32.0 | template 9.50.0, builder 4.17.0, test 9.34.0 | builder reused; test ported to `sen0401_page_test_v9_33_0.py` (11 transplants); template 9.45-9.50 transplant NOT done |

Evidence: ch07 deck plan rebuilt through the engine is byte-identical (`cmp`) to `ch07-deck/deck_plan_v1_0_0.json`; re-rendered through the wrapper, the ch07 deck gives the
same deck_check result (45 examples, 26 slides, 0 mismatches) and now passes the look-and-feel check (14 of 14 code slides syntax-coloured).

## 2. Commands (all from `08-tooling`; `SEN0401_ROOT` points at another checkout, `TMPDIR` should be the scratchpad)

```
python3 sen0401_chbuild_v1_0_0.py scaffold NN          # blank skeletons with TODO (the build refuses a TODO); add --demo ONLY for the pipeline proof (use 99)
# fill: sen0401_chNN_rdodi_data_v1_0_0.py, sen0401_chNN_stories_v1_0_0.py, chNN-deck/examples_v1_0_0.py, chNN-deck/deck_content_v1_0_0.py, assets in 03-materials/chNN/assets
python3 sen0401_chbuild_v1_0_0.py research NN          # five artefacts into 03-materials/chNN/rdodi
python3 sen0401_chbuild_v1_0_0.py checks NN /home/claude/venv314/bin/python     # claims + BEH + leaf coverage + HermiT: expect "0 mismatches"
python3 sen0401_chbuild_v1_0_0.py gates NN             # expect OVERALL: PASS (Stage1.A/B, 2.A/C, 3.A/F/B/E/src)
python3 sen0401_chbuild_v1_0_0.py examples NN /home/claude/venv314/bin/python
python3 sen0401_chbuild_v1_0_0.py plan NN              # engine refusals run here
python3 sen0401_chbuild_v1_0_0.py render NN            # node wrapper -> ooxml fix -> office stamp -> chNN-deck/sen0401_chNN_deck_v1_0_0.pptx
python3 sen0401_chbuild_v1_0_0.py deckchecks NN [--fixtures] [--python PY]   # nine checks; --python must be the interpreter of the recording
python3 sen0401_register_fragment_v1_0_0.py NN         # register entries from the files that exist (paste by the register's owner)
python3 sen0401_chbuild_v1_0_0.py pagetest NN          # key-substituted page test, about 15 minutes, never beside another browser job
```
Page chain, unchanged from chapter 7: `course_page_config_build_v2_10_0.py`, `sen0401_page_data_v2_11_0.py NN python`, `sen0401_page_build_v4_14_0.py NN`
(needs `SEN0401_BOOK_REPO`, default `/home/claude/mastering-bitcoin`, and `CME_REPO`), per-chapter inputs in `chNN-page` (quiz, objectives, resources, discussion, test_config,
stories_img) and `sen0401_chNN_diagrams_v*.py` (narrative diagrams, grounding at 0.8).

## 3. Expected results (chapter 7, measured)

| Step | Result |
|---|---|
| gates, own v1_0_0 and port v1_2_0 | same verdict: every gate PASS except Stage3.F (1 uncited claim, the document root); port reads the newest parts (378/684 triples vs 377/683 at 1.0.0 parts) |
| deck_check | 45 examples, 26 slides, 3 charts, 0 mismatches; the port also refuses a wrong interpreter (needs Python 3.14.6) |
| picture / links | 8 media parts identical, 0 refusals / 12 links < 400 |
| fixtures | 13 stale fixtures each refused for its own reason, control accepted (about 10 s) |
| page test | own 9.32.0: PASS, 372 features, 0 failed (key substitution proves page logic only, not the release step); port 9.33.0 on the same page: PASS, 372 features, 0 failed (identical) |
| demo chapter 99 | research, checks (6, 0 mismatches), gates PASS, examples, plan 26 slides, render, deck_check/structure/picture/links/honesty/lookfeel PASS; fit, story, arc FAIL for the demo content, as they should |

## 4. Pitfalls (from the SEN0414 lesson deposit, the builder reports and this port)

1. Stage3.F reads a citation only as `(Name and Name, 2023)` or `(Name et al., 2020)`: ONE comma before the year. `(Wuille, Nick and Ruffing, 2020)` is not seen and the claim is "uncited". Chapters 2-4 and 7 of SEN0401 fail this gate today for such reasons or an uncited root claim.
2. A console statement must be ONE line, free of newlines (the row is re-found on the slide by its text). The engine and the examples runner refuse a newline.
3. Diagram grounding reads only the first paragraph of a concept's explanation; put the diagram's labels there.
4. Layout and fit checks are exact formulas: title tiers 46/53 characters; Courier 0.60, Cambria 0.50, Calibri 0.48 of the point size; line factor 1.22. Fix text, do not argue with the check.
5. The two-column links renderer switches column once and never re-balances; keep the groups equal.
6. The ERD needs connectivity (every class reachable) for the page test; a search ranking cut-off makes the embedding test noisy; shared test-config defaults override a chapter's.
7. Run the deck check under the recorded interpreter (3.14.6); the recording and the check must agree.
8. The page key: the real instructor key is not in this checkout; `sen0401_page_key_substitute` swaps a test key into a COPY. Never publish that copy.
9. The register file name `sen0401_materials_v1_4_8.ttl` is written into the page data and configuration; a new register version needs a new configuration build.
10. pptxgenjs writes misplaced paragraph properties; `sen0401_deck_ooxml_fix` removes them (213 on the demo, 427 on ch07). The shipped ch07 deck was not passed through it (structure check refuses it).
11. Do not run two browser jobs at once on 2 CPUs; use `nohup` and poll. Never `pkill -f` a pattern that appears in your own command line.
12. Speaker notes: the owner's "short notes" and the ruling of 2026-10-08 (reader's prose, about 156 words) conflict; `sen0401_deck_arc_check` only warns above 120 words until the owner decides.

## 5. Checks the owner's preferences need beyond SEN0414

Already enforced by SEN0414 (ported): console rows re-run, charts native with data labels, pictures identical to assets, links open, honesty captions, no overflow, notes present.
New, written here: `sen0401_story_check` (5N1K fields, picture decoded, sha/licence/source, credit and date on a slide), `sen0401_deck_lookfeel_check` (CME tokens, fonts, `n / N`, syntax colours, data labels),
`sen0401_deck_arc_check` (26 slides, agenda ranges, questions, takeaways, 3+ stories, summary before one resources slide, Watch/Community links, notes length).
Not yet checked by anything: historical money pictures (`MONEY_PICTURES` is warned when empty), zoomable diagrams in the deck (native shapes need a `diagram_shapes` module), page text-size control, page/deck two-fold equality, "no scrolling" on the page.

## 6. Known gaps

Template 9.45.0-9.50.0 transplant and a builder 4.15.0; `diagram_shapes`/`diagram_check` for SEN0401; generic `lecture_export`; the book repository (private, no auth here) so `page_build` could not be re-run;
the Chapter-examples pane; the register has no ch06/07 entries; the ch07 deck fails structure and fit; Watch/Community resources are missing from ch06/07.
