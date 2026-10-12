# Handover to the next session: CME, SEN0401 and SEN0414 course-materials state

**From:** the course-materials session active through 2026-10-12.
**To:** the next session working under CME with access to SEN0401 and SEN0414.

**Covers three repositories.** This file lives in SEN0401's own `09-handovers-out/` (the same location the prior
cross-course handover used — see `HANDOVER_session_to_next-session_course-materials_v1_0_0.md` in this same
folder, now superseded by this file for anything it covered that changed below) because that is the established
convention for a session-to-session note that spans more than one course package. Everything it says about
SEN0414 and CME is equally current; a copy is also handed to the owner directly for download.

Earlier narrower note: a prior reply in this session produced a SEN0414-only handover and sent it to the owner
as a scratchpad download, not committed to any repository. That file described only SEN0414 and was wrong in
both scope (the switch is CME-wide, covering SEN0401 too) and placement (a session handover belongs in a
repository's `09-handovers-out/`, following the convention below, not only in a chat download). This file
replaces it as the authoritative one.

---

## 1. Standing instruction, unchanged

Revive the OE discipline from the GitHub page first of all and never trust memory or summaries. Proceed under
the strict OE discipline file's latest version on
<https://github.com/altunelyusuf/Ontologies/tree/main/oe-method/04-documentation/> and the lineage discipline
file on <https://github.com/altunelyusuf/Ontologies/blob/main/backlog-roadmap-framework/04-documentation/> if
accessible, otherwise use local disk, and execute the ceremony first, before any governed action.

Run the ceremony by resolving the latest version on disk rather than naming one, since the script itself gets
renewed:

    cd /home/claude/Ontologies && git pull -q --rebase; rm -rf repo-tooling/__pycache__
    export OE_SESSION=cme-session PYTHONDONTWRITEBYTECODE=1
    bash "$(ls repo-tooling/oe_ceremony_v*.sh | sort -V | tail -1)"

Expect `VERDICT: PROCEED`. At this handover: repo-tooling v1.47.0, `OE_Operating_Discipline_v2_17_1.md` and
`LINEAGE_OPERATING_DISCIPLINE_v74_0_0.md` both byte-identical to GitHub (verified through the authenticated
`gh api`, not the public web page — the web page 404s on a private repo because the request carries no
credential, not because of robots.txt). Handover inbox showed 2 pending items at last check, both judged
irrelevant to SEN0401/SEN0414 work (an OEE-governance-only handover and a placeholder README) — re-check them
yourself; G39 says read the inbox before working regardless.

## 2. State, verified against the remotes at handover time

| repository | branch | head | clean / behind |
|---|---|---|---|
| altunelyusuf/Ontologies | main | `ce353573` | clean, 0 behind |
| altunelyusuf/sen0401 | main | `f3cac95` | clean, 0 behind |
| altunelyusuf/AdvancedProgrammingWithPython (SEN0414) | main | `4977518` | clean, 0 behind |
| altunelyusuf/CME | main | `e3a36ce` | not independently re-verified this session — re-check before trusting |

## 3. SEN0414 — detailed state

Chapters 1-12 built to the CME pipeline standard (document TTL with fresh prose, 5N1K stories, grounded
diagrams, executed corpus programs, deck build, full `page_data`→`page_build`→`page_test` to 0 failures,
registered, committed, pushed). **Chapter 13 is next, not started** — do not begin it without the owner's
go-ahead.

- Materials register: `03-materials/sen0414_materials_v1_39_0.ttl` (chapters 7-12 present, verified by direct
  grep). Live config `08-tooling/course_page_config_v1_5_0.json` points at it; the page-data script's filename
  constant (`08-tooling/sen0414_page_data_v2_8_0.py`, line ~183) was bumped to match. **Known pitfall:** that
  constant is hardcoded, not version-glob-discovered — bumping the register alone does nothing live.
- Lineage: `07-lineage/sen0414_slides_lineage_v2_40_0.ttl` is current (v2_39_0 kept, untouched, beside it). Two
  scope exclusions were lifted by the owner's 2026-10-12 ruling, recorded as a dated amendment appended to each
  exclusion's existing rationale text (original text preserved, not deleted): chapter 12 (`ex:Excl_CommandLine`)
  and chapters 15-18/20-23 (`ex:Excl_Untaught`). Both are now in scope.
- **Open, not blocking:** `backlog:ScopeExclusion` has no modeled retraction/supersession property in BRSF's
  TBox (checked directly, `backlog_tbox_v1_124_0.ttl` line 1461). A formal handover proposing the vocabulary
  (`ScopeExclusionStatus`, `liftedBy`, `hasLiftRationale`) is filed at
  `Ontologies/backlog-roadmap-framework/07-handover-inbox/HANDOVER_sen0414-slides-lineage_to_backlog-roadmap-framework_no-retraction-vocabulary-for-scopeexclusion_v1_0_0.md`
  (commit `7843c973` in `Ontologies`). **Status: unanswered.** No action needed unless/until that owning
  session responds — do not re-raise or re-investigate it.
- Lesson deposit: `09-lesson-deposits/sen0414_lesson_deposit_v1_0_0.ttl` (commit `4977518`) records 7
  build-pitfall lessons from chapters 8-12 (diagram grounding scope, console-row newline rendering,
  layout/fit-check exact formulas, two-column link-layout overflow, ERD-connectivity test requirements,
  embedding-rank search-cutoff noise, shared test-config default overrides), each typed `a kb:LessonsLearned,
  owl:NamedIndividual` as this package's own local `pkg:` individuals — zero new `kb:`-namespace IRIs minted —
  following the precedent at
  `Ontologies/backlog-roadmap-framework/06-package-provenance/registrant-deposit-snapshot/backlog_framework_lesson_deposit_v2_1_0.ttl`.
  Verified with an rdflib parse before commit (57 triples, 7 subjects). Read the file itself for the lesson text
  before rediscovering any of these the slow way on a new chapter.
- There is also a separate, outbound, cross-package handover unrelated to the above:
  `09-handovers-out/HANDOVER_sen0414_to_mastering-bitcoin-3e_asciidoc-index-entity-leak_v1_0_0.md` — pre-existing,
  not touched this session.

## 4. SEN0401 — detailed state

Chapters 1-7 are present on disk (`03-materials/ch01` … `ch07`); chapters 6 and 7 were most recently built at
the CME standard (commit `02da678`), followed by a UTF-8 BOM fix across every chapter's current page (`f3cac95`,
current HEAD). **This session did not re-verify each chapter against the full CME pipeline standard the way
SEN0414's chapters were just re-verified — re-check chapter-by-chapter before trusting completeness, rather than
assuming parity with SEN0414's documented state above.**

- Materials register: `03-materials/sen0401_materials_v1_4_8.ttl`.
- Lineage: `07-lineage/sen0401_slides_lineage_v0_21_0.ttl`.
- Outcomes: `01-outcomes/sen0401_outcomes_v1_1_1.ttl` — **approved**, all ten outcomes, by the owner on
  2026-10-05 (acted on 2026-10-05T14:32:54 UTC). This closes open item #6 of the prior cross-course handover
  (`HANDOVER_session_to_next-session_course-materials_v1_0_0.md` in this same folder), which described the
  outcomes as an unapproved draft — that description is now stale; do not re-open it.
- **Next chapter: 8**, not started.
- The prior cross-course handover (section 3 of that file) also listed open items specific to SEN0401 at that
  time (a manifest FAIL from stowaway files, chapter 1 content gaps from an adversarial audit, a chapter 3
  main-thread budget overrun). **None of these were re-checked this session** — treat them as open until a
  session actually re-verifies each against the current files, not from this note or that one.

## 5. CME — state

Head `e3a36ce` ("cme v0.16.0"), not independently re-verified beyond the earlier prior handover's reading. CME
owns the shared standards, ontologies, SHACL safeguards and tooling both course packages register against
(`00-standards/`, `01-ontologies/`, `02-shacl-safeguards/`, `03-tooling/`); its own `07-handover-inbox/` is
where cross-package proposals to CME itself would be filed. Nothing in this session's work required a change to
CME; re-verify its head and manifest before relying on that statement past this handover.

## 6. How the owner works (standing, unchanged)

Minimal output during development — files and code, not commentary; continuous execution; decisions resting on
rules, regulations or provable facts, asking only where they genuinely don't, and never over every detail; human
labels rather than internal identifiers when discussing ontology elements; explicit `git add <file>...` never
`-A`/`.`; lineage-safe versioning — never edit an already-committed file's content in place, a new version file
with the old one kept and a dated amendment appended instead; for interactive course HTML pages and lecture
decks, the full standing interface and materials conventions recorded in the owner's own preferences (every
term explained in full teaching paragraphs, zoomable diagrams, synchronized explorer and tabs, no third level of
sub-tabs, native PPT chart objects, 5N1K-grounded stories, matching look-and-feel across deck and page, and the
rest as stated there — read the owner's preferences directly rather than this paraphrase).

For a package session specifically: stay on that package's own subjects, don't narrate OEE-scope matters, route
lineage questions to BRSF unless they concern ontology metadata or rules, and surface only the questions this
session itself actually has.
