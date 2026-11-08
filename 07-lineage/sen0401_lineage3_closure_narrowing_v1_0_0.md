# Lineage 3 — Closure by Narrowing, v1.0.0

**Date:** 2026-11-08. **Register measured:** `07-lineage/sen0401_slides_lineage_v0_1044_0.ttl` (16.4 MB; last
internal entry 0.1044.0, dated 2026-11-03).

## 1. Why this is a narrowing, not a G215 conclusion

G215 concludes a lineage only when every item is Done or Cancelled and every objective meets its target.
Lineage 3 is not in that state (measured against the live file):

| State | Count |
|---|---:|
| Done | 502 |
| Cancelled | 115 |
| Suspended | 58 |
| Proposed | 105 (handover's prior count of 101 is 4 low — drift noted, not chased) |
| InProgress | 14 |
| Ready | 9 |

This is the owner's standing wind-down-and-open-successor pattern (rulings of 2026-09-24): closed work
stays closed and committed; the unfinished part is recorded as a partial scope before closure and picked
up by a successor; the overall Mission picture is kept so satisfaction is re-checked across the chain.
Routed under G195(d): the owner's own dated instruction of 2026-11-08 (the handover) is the Owner ruling
that authorises this narrowing.

## 2. Fit-gap against Mission_V2 / Scope3

**Mission_V2** (unchanged, stays in force across the chain): every SEN0401 lecture teaches the third
edition chapter by chapter, with a deck, research and an interactive page, and the course assesses what
it teaches.

**Scope3** already lists `Del3_Ch78Decks` and `Del3_Ch78Pages` as required deliverables — Chapters 7–8
were already in scope, not a gap introduced now. What Lineage 3 does **not** reach this week:

- Chapters 9–14 (deck/research/page) — still Proposed under Scope3's original 14-chapter deliverable set.
- The Chapters 1–6 retrofit to the current deck/page standard — still open, explicitly excluded from this
  week's work by owner instruction.
- The remaining link-pass, page-template and gate-closure areas opened by Scope3's 30 stage revisions
  (`Area3_PageTemplate`, `Area3_SectionLinks`, `Area3_PageGates`, `Area3_Remedy56`, and others) — open,
  not cancelled; they are the inheritance a later lineage picks up, not abandoned work.
- **Verified by query (L-65):** all 14 InProgress items are exam-paper work (`ST_Exam_V7_*`,
  `TK_Exam_V72_Papers_Build`, `TK_Exam_V72_Papers2_Build`, and related). The midterm was printed from the
  owner-corrected paper v8.0.2 (register entry 0.1044.0); exam work now runs outside this repository
  (private CME). **These 14 items are not carried forward.**

## 3. Guards read again (G215's spirit, applied to a narrowing)

- No lesson/best-practice promise is broken by narrowing: BP-D62 (version-per-file) and the owner's
  2026-11-08 version ruling are carried into the successor as a standing rule, not reopened.
- No committed, Done work is touched. Chapters 1–6 are explicitly untouched this week.
- The exam work's closure (midterm v8.0.2 printed, make-up parked pending missing-student legal excuses)
  is an external fact, recorded here, not re-litigated by this lineage.

## 4. Disposition

- Lineage 3 / Scope3 is **wound down**, not archived yet. Per G215, setting a register down into the
  archive happens in a release, not inside a box; this closure report is that step's basis. Archival is
  deferred to the next release that touches this register file, so as not to block this week's chapter
  work (owner's explicit priority).
- The Chapters 7–8 deliverables (`Del3_Ch78Decks`, `Del3_Ch78Pages`) are carried forward into the fresh,
  narrow Lineage 4 (`sen0401_lineage4_charter_v1_0_0.md`), under the **same** Mission_V2 (unchanged,
  unwidened — no mission amendment needed since Lineage 4's mission is a slice already inside it).
- Every other open area of Scope3 (Ch9–14, Ch1–6 retrofit, link-pass/template/gate remnants) stays
  **queued**, not re-opened, pending a lineage of its own.

## 5. Disclosed gap (not silently dropped, per L-113/B6)

Encoding this closure as governed TTL individuals (a `LineageAdaptation`/closure record with its own
`StageOutput`, committed to the register) is **not done in this file** — only declared in prose, for the
owner's reading, so the week's chapter-draft deadline is not put behind a formal-encoding pass. The TTL
encoding is the first backlog item of Lineage 4's own governance category (per G215's "lineage
governance" category), to be done alongside, not before, the Chapter 7–8 draft work.
