# SEN0401 chapter pages 9.37.0 - the two-fold cycle, reviewed

The owner's rule of 2026-10-06 13:42: the decks and the interactive pages carry ONE look-and-feel and one
story discipline, "to support the teachability, adaptation, and fire the remembering of the students".
The ten chapter decks shipped first (CME materials look-and-feel v1.0.0); this cycle brings the five
SEN0401 chapter pages onto the same standard. Chapter 1 was the reference page; chapters 2-5 followed on
the same template, data builder and tests.

## What changed (versions, one subject each)
| piece | version | the one change |
|---|---|---|
| template | course_page_template_v9_33_0.html via template_patch_v9_33_0.py | the deck tokens on every pane (measured AA contrast, every colour swap count-asserted), the deck's code colours in the editor, the Stories tab under Learn with chip, photographs + credits, WHO/WHERE/WHEN/READ fact row, takeaway strip, source line and On-the-page jumps |
| page data | sen0401_page_data_v2_7_0.py | reads config 2.6.0; imports the chapter's story companion, runs ITS run_checks(), embeds stories with photographs (deck assets, downscaled, data URIs) from stories_img_v1_0_0.json per chapter |
| page build | sen0401_page_build_v4_10_0.py | default template 9.33.0; page 9.37.0 = template 9.33.0 + configuration 2.6.0 |
| configuration | course_page_config_build_v2_6_0.py / course_page_config_v2_6_0.json | the exam key pair re-provisioned (README_PORT procedure); lists outcomes 1.1.1 and materials 1.4.4 |
| page test | sen0401_page_test_v9_29_0.py | asserts the live tokens and the Stories tab; environment-truth main-thread budget; agent waits 400 s; Stories axe audit in the late batch |
| smoke test | sen0401_page_smoke_v1_0_1.py | agent waits 400 s |
| outcomes | 01-outcomes/sen0401_outcomes_v1_1_1.ttl | REPAIR: the LO-1 individual, lost in the 1.1.0 approval edit, restored (ten coded outcomes again) |
| materials | 03-materials/sen0401_materials_v1_4_4.ttl | the five pages repointed to 9.37.0; titles and version IRIs caught up |

## Verification records (beside each chapter's page data in 08-tooling/chNN-page/)
- test_results_v9_37_0.json - the full browser test: chapter 1 328 checks (164 features + 122 widgets +
  gates), chapters 2-5 likewise, 0 failures each; WCAG 2 A/AA (axe-core) clean over the whole document
  and over every audited pane including Stories; every Pyodide result equal to the build interpreter's
  (Python 3.14.6); 0 console errors.
- smoke_results_v9_37_0.json - 12 deterministic checks per chapter.
- book_corpus_check_v9_37_0.json - 7 checks per chapter; chapter 5's item 4 fails (see below).
- corpus_manifest_v9_37_0.json - every embedded block named and hashed; the materials block hash equals
  the file on disk (9acaab5667e41dec).

## Findings of the cycle - measured, recorded, none hidden
1. **LO-1 had vanished from the graph.** The 1.1.0 outcomes edit that added the owner's approval block
   deleted the line `sen0401:LO1 a case:dtCFItem ; case:humanCodingScheme "LO-1"`, so LO-1's statement
   hung off the document node and nine, not ten, coded outcomes existed. Found because the chapter 1 page's
   course-question check could not retrieve LO-1; the 9.36 rebuilds had run only the smoke test and missed
   it. Repaired in outcomes 1.1.1 - a serialization repair of approved content, no statement changed.
2. **The exam key pair.** The private half lives outside every repository (README_PORT.md) and did not
   survive the environment move. Re-provisioned per the documented procedure; the 9.37.0 pages answer to the
   new key; release codes minted with the lost key no longer exist anywhere.
3. **The build machine has two cores.** Three suite constants turned out to measure the machine: the 200 ms
   main-thread budget (the UNCHANGED shipped 9.36 page loads at 190-250 ms here against the 174 ms once
   recorded; post-load it stays at 141 ms), the 120 s agent-readiness waits (the shipped chapter 3 page needs
   136 s here, the new one 133 s, both error-free), and my own first placement of the Stories axe audit
   before the budget checkpoints (an axe.run costs up to ~900 ms of main thread here). The test now gates
   the load task against the shipped page measured in the same run (medians of several loads, the margin
   being the shipped page's own spread), keeps 200 ms absolute after load, waits 400 s for agents, and runs
   the Stories audit with the other audits after the checkpoints. Nothing about the pages was relaxed.
4. **Chapter 5, book-corpus check item 4 - PRE-EXISTING.** "A book-only question is answered from a book
   passage" fails on the new page AND identically on the shipped 9.36.0 page
   (ch05-page/book_corpus_check_v9_36_0.json, measured 2026-10-06): the guide routes "What does the book say
   about memorizing recovery codes?" to the Choices-behind-a-recovery-code agent, whose slice cites no book
   passage (at 9.26, before agent slicing, the Key-generation-methods agent answered with 3 of 6 book
   citations). It dates from the agent slicing of template 9.28.0 and belongs to the agent-routing thread;
   it is not a regression of this cycle and is left visible rather than worked around.
5. **The page ABox.** Still the one built for 9.4.2 (the register says so); its builder reads record shapes
   the current chain no longer writes. Left as the recorded debt it already was.

## The undergraduate's read-through (desktop 1400 px, phone 390 px)
- The Stories tab reads like the deck's story slides: date chip, the photograph with its credit, the four
  fact chips, the story, the orange-barred takeaway, the source. On a phone the chips stack and nothing
  scrolls sideways (the test's 320/360/390/768 px checks).
- The editor is the deck's dark panel with the deck's keyword/string/number/comment colours; the toolbar,
  menu pills and tabs are the deck orange on ivory; links and headings the deck slate.
- FOUND and fixed before shipping: fact-row and credit text sized under the phone gate's 14 px (raised to
  .85rem); a megabyte of base64 riding through innerHTML (the photographs are now assigned after the one
  parse); the Stories audit placed where it inflated the budget it was meant to leave alone.
