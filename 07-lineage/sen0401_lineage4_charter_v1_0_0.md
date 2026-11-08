# Lineage 4 — Charter, v1.0.0 (fresh, narrow)

Opened 2026-11-08, in the same step as Lineage 3's closure-by-narrowing
(`sen0401_lineage3_closure_narrowing_v1_0_0.md`). Profile: AAL (agentic adaptive), the default.

## Mission (settled, per the handover's suggestion — adopted verbatim)

> Chapters 7 and 8 of the third edition are taught with a deck and an interactive page, each produced
> from one owner-approved chapter draft, ready for the lecture of the week of 2026-11-12.

This is a slice of Mission_V2 (unchanged, in force across the chain) — not a new or widened mission, so
no mission amendment (G216) is needed.

## Scope (G194/G200: derived as a taxonomy, areas/deliverables/exclusions)

**Areas:** `Area4_Ch07`, `Area4_Ch08` (each: draft → deck → page).

**Deliverables (one goal will face each):**
- `Del4_Draft_Ch07`, `Del4_Draft_Ch08` — the owner-approved plain-text draft (story, slide outline, page
  tabs in slide order, code examples with executed results, resources list).
- `Del4_Deck_Ch07`, `Del4_Deck_Ch08` — rendered only after draft approval.
- `Del4_Page_Ch07`, `Del4_Page_Ch08` — rendered only after draft approval, from the same draft as the deck.

**Exclusions (each guarded by a goal of its own):**
- `Excl4_NoChapters1to6` — Chapters 1–6 are not touched this week (owner's explicit instruction).
- `Excl4_NoExam` — exam work stays outside this repository (held in CME; midterm already printed).
- `Excl4_NoOtherChapters` — Chapters 9–14 stay queued under the wound-down Lineage 3's open scope, not
  reopened here.
- `Excl4_NoRebuildWithoutDraft` — no deck or page is rendered or re-rendered before its chapter's draft
  is read and approved (the handover's "draft first" rule, section 4).

## Goals

- **G4_1** (faces `Area4_Ch07`, `Area4_Ch08`): A deck and an interactive page exist for Chapter 7 and for
  Chapter 8, each traceable to one owner-approved draft.
- **G4_2** (mission-facing, process quality — this is the "make it faster" instruction, point 4 of the
  handover): The draft-first order is followed exactly once per chapter — no five-build churn.
- **G4_3** (guards `Excl4_NoChapters1to6`, `Excl4_NoExam`, `Excl4_NoOtherChapters`): nothing outside the
  two chapters is touched by this lineage.

## Objectives (measured, forecast per the handover — forecasts, not deadlines, G186/G197)

| Objective | Baseline | Target | Forecast |
|---|---:|---:|---|
| Chapter drafts delivered for owner's reading | 0 | 2 | 2026-11-08 (this turn) |
| Chapter drafts owner-approved | 0 | 2 | 2026-11-10 |
| Decks + pages rendered from the approved draft | 0 | 4 (2 decks, 2 pages) | 2026-11-12 evening |

The existing Chapter 7 deck (v2.2.0) and Chapter 8 deck (v2.0.0) already pass the full deck standard
(D1–D12, measured this session, both PASS) — they are **not** rebuilt from nothing; the draft is written
to match what already works and only to change what the owner's current teaching emphasis requires.
Whichever of today's content survives into the approved draft is reused at render time, not re-typed.

## Backlog (G194: derived from the scope above, not from a list of gaps)

1. **Story: Draft Chapter 7** — Ready; delivered this turn.
2. **Story: Draft Chapter 8** — Ready; delivered this turn.
3. **Story: Render Chapter 7 deck + page** — Proposed; blocked on owner approval of the Chapter 7 draft.
4. **Story: Render Chapter 8 deck + page** — Proposed; blocked on owner approval of the Chapter 8 draft.
5. **Governance story: encode this charter as governed TTL (Mission/Scope/Goal/Objective/Backlog
   individuals, SHACL-validated, git-witnessed one commit per stage)** — Proposed; disclosed as not done
   in this charter (L-113/B6: named, not silently dropped) so it does not sit ahead of the chapter-draft
   deadline. Runs alongside story 3–4, not before them.

## Version rule carried forward (owner's ruling of 2026-11-08)

Each deck, page and document continues from its **own** last version; a release of one does not bump
another. `08-tooling/cme_version_check_v1_0_0.py` is run before each release, declaring the size of each
changed file against `08-tooling/cme_version_baseline_SEN0401_v1_0_0.json`.
