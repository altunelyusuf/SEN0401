# Handover to the next session: the interactive pages on the deck standard - SEN0401 done, SEN0414 next

**From:** the course-materials session of 2026-10-06 (cme-session), closed deliberately on the discipline's
handover alarm: its context had grown to 413,624 tokens per call from a measured floor of 119,595 (floor +
150,000 is the HANDOVER threshold of repo-tooling/oe_session_usage_v1_5_0.py), with 49.7 million of its 50.7
million billed tokens being cache reads of its own history. The measurement is the API's own, recorded on the
v0.40.0 publish.

**To:** the next session working on the SEN0401 and SEN0414 course materials (the CME session scope).

**Everything here was measured on the bytes; re-derive before acting on it, including these claims.**

---

## 1. Standing instruction, unchanged

Revive the OE discipline from the GitHub page first of all and never trust your memory or summaries. Proceed
under the strict OE discipline file latest version on
<https://github.com/altunelyusuf/Ontologies/tree/main/oe-method/04-documentation/> and the lineage discipline
file on <https://github.com/altunelyusuf/Ontologies/blob/main/backlog-roadmap-framework/04-documentation/> if
accessible, otherwise use local disk, and execute the ceremony first:

```
cd /home/claude/Ontologies && git pull --rebase && export OE_SESSION=cme-session && bash "$(ls repo-tooling/oe_ceremony_v*.sh|sort -V|tail -1)"
```

Clear every REFUSE before a governed action. Read the pending inbox (G39); items addressed to the OEE
governance session are not yours.

## 2. The owner's directive this handover serves (2026-10-06 13:42)

"Apply the same standards to other slides ... autonomously ... keep the look-and-feel matching the slides
and interactive html files to support the teachability, adaptation, and fire the remembering of the students
... use the visualizations and styling in two-folds. Let's finish the first 5 presentations for both courses
in the same standards and then switch to the interactive pages, again 5 chapters similarly." Then "Fine,
proceed." and "Proceed."

**State:** all ten decks shipped (SEN0401 v0.35.0-v0.39.0; SEN0414 v2.40.0-v2.43.0). SEN0401's five pages
shipped on the standard in v0.40.0 (this session). **SEN0414's five pages are the open unit.**

## 3. What v0.40.0 holds (SEN0401, commit 92b1226, tag sen0401-v0.40.0 cut by the workflow)

Read 08-tooling/PAGES_REVIEW_v9_37_0.md first: the version table, the verification records, and five
findings (LO-1 restored in outcomes 1.1.1; the exam key pair re-provisioned; three suite constants that
measured the two-core build machine and how the test now handles them; chapter 5's pre-existing book-check
item; the page ABox still at 9.4.2). Then the materials register's 1.4.4 header note.

The machinery, in the order a chapter cycle runs it (PAGE_VER=9_37_0 for this generation):
```
cd /home/claude/SEN0401/08-tooling
PAGE_VER=9_37_0 python3 sen0401_page_data_v2_7_0.py NN /root/.local/bin/python3.14   # Python 3.14.6; refuses a story companion that fails its own checks
PAGE_VER=9_37_0 python3 sen0401_page_build_v4_10_0.py NN                             # template 9.33.0 + configuration 2.6.0
PAGE_VER=9_37_0 python3 sen0401_page_test_v9_29_0.py NN                              # ~20 min on two cores; run NOTHING else meanwhile
PAGE_VER=9_37_0 python3 sen0401_page_smoke_v1_0_1.py NN
PAGE_VER=9_37_0 python3 sen0401_book_corpus_check_v1_1_1.py NN
```
Run the browser tests one at a time: the main-thread budget is a wall-clock measurement, and anything else
running on the machine (including your own probes) inflates it - measured, it turned 141 ms into 889 ms.

## 4. SEN0414: the exact plan, measured against its tree

SEN0414 (= altunelyusuf/advancedprogrammingwithpython, remote main 8aae06e = v2.43.0) has chapters 1-5 at
page 9.26.0 on its OWN template line, course_page_template_v9_25_0.html, which differs from SEN0401's
v9_32_0 by 57 lines once course names are normalised (SEN0401 took its 9.26-9.32 audit repairs; SEN0414 did
not, and importing them is a separate thread - do not fold it into this one). Chapters 6-9 are at 9.19.0 and
out of scope (five chapters).

Port the two-fold patch onto SEN0414's line, one subject per version, exactly as SEN0401 did:
1. `template_patch_v9_26_0.py` -> `course_page_template_v9_26_0.html`: copy SEN0401's
   `template_patch_v9_33_0.py`, keep every colour swap and the Stories pane, and RE-MEASURE every
   occurrence count on v9_25_0 before asserting it (SEN0401's counts will not all match: the patch refuses
   on the first drift, which is the point). The GROUPS.learn line, the lecture pane anchor
   (`'</div></div>';\nif(D.resources&&D.resources.length){const RKLAB`), `panes.innerHTML=P` and the
   `.edhl` token rules all exist in SEN0414's 9.25 template - verify with grep, do not assume.
2. `sen0414_page_data_v2_6_0.py` (over v2_5_0): the stories block of SEN0401's v2_7_0 verbatim, reading the
   newest `sen0414_chNN_stories_v*.py` (all five exist, v1_0_0, each with run_checks) and
   `chNN-page/stories_img_v1_0_0.json`. Write those mappings from each deck builder's own img() placements
   and the chapter's ASSETS_PROVENANCE (ch1 Guido - Daniel Stroud CC BY-SA 4.0; ch2 Boole PD; ch3 Gauss
   Jensen PD and Dijkstra Hamilton Richards CC BY-SA 3.0; ch4 EDSAC Cambridge CC BY 2.0; ch5 the moth
   logbook PD Navy and Kernighan Ben Lowe CC BY 2.0). Stories without a deck photograph carry none.
3. The exam key: `/home/claude/instructor_keys/sen0414_instructor_key_v1_0_0.json` and its public file were
   generated this session (mode 600, outside every repository) because the originals did not survive the
   environment move. SEN0414's configuration builder must pick the public half up the way SEN0401's
   v2_1_0 does (check `course_page_config_build_v1_3_x.py` for the same preference for the public-key file;
   if it lacks it, add it as the one change of the next builder version). Its desk and exam tests
   (sen0414_exam_test_v1_1_0.py, sen0414_desk_test_v2_2_0.py) read the key from that path.
4. `sen0414_page_build_v4_9_0.py`: default template v9_26_0; record "page 9.27.0 = template 9.26.0 +
   configuration 1.3.x" in its header, as the lineage does.
5. `sen0414_page_test_v9_26_0.py` (over v9_25_0): SEN0401's 9.29.0 additions - the live-token check, the
   Stories checks (functional checks early; the axe audit in the LATE batch, after the budget checkpoints),
   the environment-truth budget (`_loads`, medians, the shipped page's own spread as margin), the 400 s agent
   waits. SEN0414's test is the ancestor of SEN0401's (9.23 -> 9.24), so the insertion points match by
   text; verify each anchor with count==1 before replacing.
6. Materials register (only-latest: git mv sen0414_materials_v1_36_0.ttl -> v1_37_0): repoint Page_Ch01-05
   to the 9_27_0 files BEFORE building, because each page embeds the register that names it (the 9.36
   precedent in SEN0401); then rebuild the configuration so corpus.course lists v1_37_0; then data, build,
   test, smoke, book check per chapter, one at a time. Then VERSION 2.44.0, manifest regen
   (`python3 $SP/regen.py . 2.44.0` after `git add -A`, then `sed -i '1s/# sen0401-repo/# sen0414-repo/'`),
   verify, commit with the attribution trailer, publish with
   `OE_TARGET_REPO=altunelyusuf/advancedprogrammingwithpython OE_PACKAGE_AT_ROOT=1 bash repo-tooling/oe_publish_v1_12_1.sh "$GH_TOKEN" <export> sen0414`,
   check `git ls-remote --tags origin | grep sen0414-v2.44.0`, then `git fetch && git reset --hard origin/main`.

## 5. Open items, exactly as measured

- **Owner one-clicks still outstanding:** sen0414 Actions -> "OE tags" -> Run workflow with version 2.40.0;
  CME Actions -> "OE tags" dispatch 0.11.0; CME Actions -> "CME registry check" run.
- **Chapter 5 book-corpus item 4** (SEN0401): fails on the shipped 9.36 page and on 9.37 alike; the guide
  routes the book question to an agent whose slice holds no book passage. Agent-routing thread; records in
  ch05-page/book_corpus_check_v9_36_0.json and _v9_37_0.json.
- **The page ABox** (SEN0401 ch01 at 9.4.2; its builder reads record shapes the chain no longer writes):
  recorded debt in the register's Page_Ch01 comment, untouched.
- **Release codes minted with the lost private keys** no longer verify anywhere; pages built from v0.40.0
  (SEN0401) answer to the new key; SEN0414's pages will after step 3-6 above.
- **Midterm/Final outcome alignment** (SEN0401 SOURCES section "They are approved"): awaiting the owner.
- The two inbox items in oe-pack/07-handover-inbox/pending/ are OEE's (session-3 -> session-4 handover;
  rdodi-ecosystem's lineage-register ruling). Not ours.

## 6. Rules that this session learned the hard way (keep them)

- Never run a browser probe while a page test runs; never run two page tests at once.
- A versioned file whose bytes a built page embeds (the materials register, the outcomes part) is frozen
  the moment a page is built from it: a later edit breaks the embedded-block hash. Put narrative into the
  review file, not into the register, after the build.
- Count-asserted patches refuse on drift; when one refuses, measure the real count in context (CSS block
  versus JS strings - `:root` definitions are consumed by the root swap first) and never widen blindly.
- `pkill -f <pattern>` kills the shell that runs it when the pattern appears in its own command line; kill
  by pid.
