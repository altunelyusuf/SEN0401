# SEN0401 chapter pages on template 9.26.0 (port notes)

The SEN0401 chapter page is now built from SEN0414's newer template (paragraph text, multi-answer exam type, input rows, exam layer,
practice builder, agents, Playground / Code Lab). Nothing in SEN0414's repository was edited; every SEN0401 file below is new and the
old files (template 9.4.x, page 9.4.2, build 4.0.0, data 2.1.0, test 9.4.x) stay on disk.

## The chain

| step | file (in `08-tooling`) | note |
|---|---|---|
| base template | `course_page_template_v9_23_0.html` | byte-identical copy of SEN0414's 9.23.0 |
| template | `template_patch_v9_24_0.py` -> `_v9_25_0.py` -> `_v9_26_0.py` -> `course_page_template_v9_26_0.html` | each patch lists exactly what it changes (docstring) |
| configuration | `course_page_config_build_v2_2_0.py` -> `course_page_config_v2_2_0.json` | edit the builder, not the JSON; it runs every program in it, resolves the book pin and lists the course parts that exist |
| ontology (Stage 2+3) | `sen0401_chapter_build_v1_0_0.py` | corpus -> TBox, ABox, document |
| page data | `sen0401_page_data_v2_3_0.py` | ontology -> `chNN-page/page_data_v9_26_0.json` |
| page | `sen0401_page_build_v4_2_0.py` | -> `03-materials/chNN/page/sen0401_chNN_page_v9_26_0.html` |
| full test | `sen0401_page_test_v9_24_0.py` | SEN0414's 9.23.0 test, switches in `chNN-page/test_config_v*.json` |
| smoke test | `sen0401_page_smoke_v1_0_0.py` | 12 deterministic checks, a few minutes |
| book corpus check | `sen0401_book_corpus_check_v1_1_0.py` | the book block against the pinned bytes, the graph's triple counts, and a book-only question answered from a book passage |
| bank checker | `question_bank_check_v1_2_0.py` | one script for every chapter |
| exam release | `sen0401_exam_release_v1_0_0.py` | release codes with the SEN0401 instructor key |

What template 9.24.0 changes over 9.23.0 (all driven from `data.course`, i.e. the configuration): exam identity (SEN0401's own public key,
`sen0401-exam-release`, result/audit file names and PDF heading), Code Lab snippets, SPARQL samples, Step-through examples, Playground code
patterns (blockchain programs, standard library only, all run in the page's Pyodide), agent icons, and sentences of one-paragraph concepts
for the "several correct" question type. A SEN0414-style configuration (without these keys) still builds with the old behaviour.

**Instructor key.** `/home/claude/instructor_keys/sen0401_instructor_key_v1_0_0.json` (private, mode 600, outside every repository) was made
for this port; its public half is in the configuration. SEN0414's key does not release SEN0401 exams (the smoke test checks this). Replace
the pair when the owner wants their own: new key file, new `exam.public_key` in `course_page_config_build_v2_1_0.py`, rebuild.

## Build and test one chapter (NN = 01, 02, ...)

```
cd /home/claude/sen0401/08-tooling
export PAGE_VER=9_26_0
# 0 (only when the book pin, the course-level ontologies or a page program changed) the configuration
python3 course_page_config_build_v2_2_0.py
# 1 (only when the chapter's text changed) ontology from the corpus sen0401_chNN_corpus_vX_Y_Z.py  ->  03-materials/chNN/rdodi
python3 sen0401_chapter_build_v1_0_0.py NN NEWVER PRIORVER          # e.g. 02 1.2.0 1.1.1
# 2 page data, 3 page
python3 sen0401_page_data_v2_3_0.py NN /root/.local/bin/python3.14
python3 sen0401_page_build_v4_2_0.py NN
# 4 tests (run them one at a time: concurrent browsers make the page's 200 ms main-thread gate fail spuriously)
python3 sen0401_book_corpus_check_v1_1_0.py NN
python3 sen0401_page_smoke_v1_0_0.py NN
nohup python3 sen0401_page_test_v9_24_0.py NN > /tmp/t_chNN.log 2>&1 &   # about 15 minutes: poll it
```
The page needs, in `chNN-page/`: `quiz_v*.json`, `objectives_v*.json` (both exist for chapters 1-4), optionally `discussion_v*.json`,
`question_bank_v*.json`, `test_config_v*.json`, `playground_v*.json` (replaces the course Playground program), `visuals_v*.json`, `resources_v*.json`,
`lecture_v*.json`. The newest version of each is used.

## The corpus module (what the chapter builder reads)

`08-tooling/sen0401_chNN_corpus_vX_Y_Z.py`, same format as `sen0414_ch01_corpus_v1_2_0.py`. Attributes: `CHAPTER`, `NODES`, `CHECKS`, `RAISES`,
`OWNERS`, `ERRORS`, `CQS`, `PROVENANCE`, `TOOLING`, `CHANGE`, `DOC_TITLE`, `DOC_ABOUT`, `facet_text`. The full contract is the docstring of
`sen0401_chapter_build_v1_0_0.py`. Differences from SEN0414's builder:

* `INTERPRETERS` is now `TOOLING` (the old name still works): the label of what executed the claims, e.g. `"CPython 3.14.4"`.
* the builder executes every `CHECKS`, `RAISES`, `ERRORS` entry and every worked example (`io`) before writing, and stops if one does not hold
  (SEN0414's builder only counted them). `SKIP_CHECKS=1` skips; `CHECK_PY` picks the interpreter.
* SEN0401 conventions (read from chapters 1-4): prefix `chx:` (= `http://example.org/sen0401/chNN#`), concept individual `chx:X_<Id>`, worked
  example `chx:IO_<Id>` with `chx:input` / `chx:output`, section `chx:S_<Id>` with `dcterms:source <.../chNN#Id>`, identifiers `sen0401_chNN_tbox_vX_Y_Z`,
  files `sen0401_chNN_domain_tbox_v*.ttl`, `..._domain_abox_...`, `..._document_...`. Quotes in text are escaped, not turned into single quotes.
* Proof of equivalence: a corpus rebuilt from chapter 1's current files regenerates the TBox and the document triple-for-triple and the ABox
  except the `Env` description (the old one says "installed with uv", the new one lists what was checked).
* A concept's text is a list of `(facet, text)` paragraphs. What `facet_text(paras)` returns is the section text; it decides whether the
  facet label ("What it is: ...") is printed. The page splits paragraphs on a blank line and shows one `<p>` each.
* Env: `SEN0401_CORPUS_DIR` and `SEN0401_OUT_DIR` redirect input and output (scratch builds). The chapter's `..._domain_shacl_v*.ttl`, when
  present in the output folder, is applied to the new TBox+ABox (`pyshacl`). The Stage 1 research file and the SHACL file are not rewritten:
  copy/version them by hand if the chapter needs new ones; the page data takes the newest of each part. `sen0401_rdodi_docx_v1_0_0.py NN VER`
  writes the Word file from the document.

## Question bank (`chNN-page/question_bank_vX_Y_Z.json`)

Same shape as SEN0414's `ch01-page/question_bank_v1_1_0.json`: a JSON **list** of items

```json
{"concept": "ProofOfWork", "level": "Apply", "q": "What does this program print?", "code": "print(2 + 2)",
 "options": ["4", "22", "0", "Error"], "answer": 0, "why": "One-sentence reason the marked option is right."}
```
* `concept` is a concept id of the page (class name, e.g. `SupplyCap`); `level` is `Remember`, `Understand`, `Apply` or `Analyze`;
  `code` is optional (shown under the question; **its printed output must equal the marked option**, trimmed; an error is written as its
  class name, e.g. `ValueError`); exactly four distinct single-line options; no "all of the above"; `answer` is the index of the right one.
* No other keys. Do not repeat a question of the chapter's `quiz_v*.json`.
* A complete bank has at least one item for every concept, at least two for every concept with a worked example, one of them Apply with code,
  and each answer position (0-3) used by 20-30 percent of the items.
* Programs run in the page under Pyodide (CPython 3.13, no network, standard library only; `hashlib` has md5, sha1, sha2, sha3 and blake2 but **not ripemd160** (checked in the page), so Bitcoin's hash160 cannot be computed there - give such a value as data, or write RIPEMD-160 out);
  the checker also runs them under every older interpreter found here and requires the same output.
* Check: `python3 question_bank_check_v1_2_0.py NN` (add `--partial` for a bank still being written: coverage and balance are not required, every
  item present is still checked). When the bank is complete, remove `"bank_complete": false` from the chapter's `test_config`.
* Chapter 1 has a seed, `ch01-page/question_bank_v1_0_0.json` (8 items), only to prove the path: bank -> build -> "From the question bank"
  questions, mock exam and exercises; the page test and the smoke test re-run every bank program in the browser.

## test_config (`chNN-page/test_config_v*.json`)

Keys: `guide_q`, `agent`, `root` (a question for the guide that should hand over to `agent`; `root` is the agent's first question; choose an
agent that has an executed example and is not the largest) and the switches `corpus_kinds`, `course_outcomes`, `code_layers`, `bank_complete`
(see the comment above `CFG` in the test). A switch set to the "does not have" value turns the check that needs it into a listed SKIP
instead of a FAIL. As of the 9.26.0 rebuild `corpus_kinds` = **book, chapter, page, research**: the page now embeds the ontology of its own
chapter of Mastering Bitcoin, so the agents really do rank over book passages. `course_outcomes` is still false and `corpus_kinds` still has
no `course` entry - SEN0401's own course-level ontologies arrived after this rebuild and are not in the pages yet (see "Known gaps"). The
chapters' examples are not Python programs, so `code_layers` stays false.

## The book corpus (what the 9.26.0 rebuild fixed)

Configuration 2.1.0 declared an **empty** page corpus and said in its own note that "SEN0401 has no textbook ontology for Mastering Bitcoin".
That was false: the ontology of the 3rd edition, one file per chapter, is published in the Ontologies monorepo as `mastering-bitcoin-3e`. The
page template has carried a `book` corpus kind all along, so the only reason the agents, the taxonomy and the SPARQL console never saw a book
triple was the configuration saying there was nothing to embed. Fixed in configuration 2.2.0 (`corpus.book`, one entry per chapter with the
book's own chapter label, plus `book_pin_commit`) and page build 4.2.0, which reads the file with `git show <pin>:<path>` and embeds it as
`data-kind="book"`; a pin that does not resolve stops the build. Template 9.26.0 widened one query (`bookQ`) so the taxonomy's book layer
accepts this book's way of carrying a concept's own sentence.

**Course chapter N is book chapter N.** Verified mechanically for all 14 at the pin by the configuration builder (each file's own chapter
individual must carry inventory key `chNN` and part number N) and independently by concept-label overlap: every one of chapters 1-5 overlaps
its same-numbered book chapter two to four times more than any other.

## Known gaps

* **SEN0401's own course-level ontologies are not in the pages yet.** `00-course-profile/`, `01-outcomes/`, `02-textbook/` and
  `03-materials/sen0401_materials_v1_0_0.ttl` were written by a parallel worker while the 9.26.0 rebuild was running, so `corpus.course` in
  `course_page_config_v2_2_0.json` is still `[]`. The configuration builder globs those four folders, so re-running it picks them up with no
  edit; then rebuild the data and page steps, add a `course` entry to each chapter's `corpus_kinds` and set `course_outcomes` to true in a new
  `test_config`. Their textbook part pins the same commit this rebuild used, so the book block will not move.
* The numbers unit has no page of 9.26.0; it has `numbers-page/` inputs from the old chain. A named unit gets **no** book block by design
  (`corpus.book` is keyed by chapter number), and page build 4.2.0 says so in its manifest rather than failing.
* The page ABox / build record steps (`sen0401_page_record_v2_1_0.py`, `sen0401_page_abox_build_v1_2_0.py`) belong to the old chain; not rerun.
* `index.html` ("All chapters" link on the page) does not exist for SEN0401.
* `bonus_points` (10) in the configuration is SEN0414's value, kept until the owner sets SEN0401's.
