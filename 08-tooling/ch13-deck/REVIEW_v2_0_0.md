# Chapter 13 deck v2.0.0 - the three-role review record (task TK_Ch13_Deck_Build_R24, 2026-10-25)

Built by `ch13-deck/deck_build_v2_0_0.py` from the research v1_0_2 (25 key concepts), the corpus v1_0_2 (six parts), the stories v1_3_0 (four stories) and the recorded executions `examples_out_v2_0_0.json`
(`examples_run_v2_0_0.py`, Python 3.14.6, run inside the unpacked wheel `sen0401_ch13_lib-1.1.0`). The deck 1.2.0 and every earlier file stay unchanged.

## The academician's build notes
- 55 slides: title, route, questions, map; six parts, each a divider, concept cards, code slides; four stories; one comparison (hot or cold); one table of what the run did not cover; summary, resources, closing.
- 28 code slides, each with a plain note beside every code frame and its executed result as a native chart (6) or a native table (22); the chapter-code manifest `03-materials/ch13/page/chapter_code_ch13_v1_0_0.json` lists the same 28 listings in slide order.
- 25 key concept cards, each with a meaning and an everyday analogy; every divider names its groups, a meaning line and an analogy per group, and holds a native table (the strip of parts).

## The teacher's notes
- Short sentences; the longest text box has 29 words; notes of at most 60 words; no listing wraps (one statement per line, at most 56 characters).
- Four 5N1K stories (Mt. Gox, Casascius, Shamir, Trezor) with a picture, the credit, a date and a live link; three pictures are stand-ins and say so on the slide (Mt. Gox letter, Casascius hologram, Trezor Model T).

## The student's notes
- Values read from `R` are the record of ONE run of Bitcoin Core 31.1 on regtest and the caption says so; `seen()` and `L.const` read saved sources carried in the wheel; every other value is computed.
- No example prints an error first: the refusals of the node are read as text and printed after a plain value.

## Honesty and deviations (the owner can overrule)
1. The deck 1.2.0 had 16 research examples that read files the page's wheel does not carry (mempool blocks, the BIP 39 word list and vectors, the 1979 paper, the table of all sources). The 28 examples of this deck use only
   what the committed wheel 1.1.0 carries, so each runs in the page; the claims that need the other files stay in the research package and on the page as recorded. Examples reproduced under Python 3.14 and 3.13.
2. The title picture is the public-domain Bitcoin logo, copied byte for byte as `assets/ch13_bitcoinlogo.png` (provenance `assets/ASSETS_PROVENANCE_v1_4_0.md`) because the picture check reads only the chapter's own assets.
3. The resources slide keeps the 11 links of the deck 1.2.0 (3 of them videos or community pages) and the 4 story links; all 14 answered HTTP 200 on 2026-10-25 from this machine.
4. The deck match check v1_0_0 compares the page 9_69_0 with the old lecture export; it does not read this deck. The page and its lecture export are rebuilt by the page task, not here.
