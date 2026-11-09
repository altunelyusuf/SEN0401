# Handover: proposing two course-material conventions as general CME rules

**From:** the SEN0401 session (Lineage 4, Chapters 7–8 draft work).
**To:** the CME session.
**Nature:** a proposal for CME to review and decide, not a mandate. Both conventions below are already
in effect for SEN0401's Chapter 7–8 drafts; nothing here asks CME to adopt them sight-unseen — the owner
asked that this be raised as a question for CME to consider generalizing, once settled for this course.

**Placement note:** this file lives in SEN0401's own `09-handovers-out/`, the established convention for
a session-to-session note addressed to a different package's session (see
`HANDOVER_session_to_next-session_cme-sen0401-sen0414-state_v1_0_0.md` in this same folder for precedent).
SEN0401 does not write into CME's own repository or lineage; CME's session picks this up and decides
whether, and how, to act on it.

---

## 1. Context

While drafting Chapters 7 and 8 (Lineage 4), the owner asked for the chapter stories to read as natural
narrative prose rather than labelled WHO/WHAT/WHEN/WHERE/WHY/HOW fields, while still using those six
elements internally to check that nothing is missing from a story. Separately, a review of the Chapter 8
draft caught a sentence that spoke as if the course chapter *were* the textbook ("Chapter 8's own earlier
sections had already shown...") rather than citing the textbook as its source. Both issues are generic to
any CME-governed course that tells stories and cites a source textbook, not specific to SEN0401 — hence
this handover.

## 2. Rule proposed: 5N1K as an internal pattern only

**What it says:** the 5N1K elements (who/what/when/where/why/how) are used to author and verify a story
— confirming nothing essential is missing — but must never surface as visible structure in audience-facing
material: no on-screen "WHO:"/"WHAT:"-style labels, and no prose that silently marches through the six
fields in a fixed, recognizable order. The audience sees one flowing narrative; the six-element check
happens only in drafting and review.

**Already applied:** SEN0401's Chapter 7–8 drafts (`v1.1.0`) rewrite all six story slides as narrative
prose with no field labels. A real tension remains open there: the *live decks* still show the labels
on-screen, and SEN0401's own deck-standard checker (its "D5" criterion) currently *requires* the six
labels to pass. That's flagged in both drafts for the owner's decision on timing — the rule is agreed, but
rolling it into the existing decks and the checker is separate follow-up work, not part of this proposal.

**For CME to decide:** whether to adopt this as a standing rule for every CME-governed course's storytelling
convention, and if so, whether course-level deck-standard checkers (where they exist) should be updated to
check for six-elements-present rather than six-labels-visible.

## 3. Rule proposed: cite the source textbook, don't narrate as it

**What it says:** course material may reference a source textbook's wording, worked examples, or
visualizations, but must not write as though the course material itself is that textbook's content. The
textbook is named in the sentence that draws on it, with a pinpoint to the textbook's own section title
(or page/section number, where stable ones exist) in parentheses — borrowed from ordinary academic
citation practice, adapted to be usable in a slide bullet as well as in flowing prose.

**Example, before/after (from the Chapter 8 draft, book: Antonopoulos & Harding, *Mastering Bitcoin*, 3rd
ed.):**

- Before: *"Chapter 8's own earlier sections had already shown, with small worked numbers, exactly what
  happens when a signing nonce repeats..."*
- After: *"...as Mastering Bitcoin shows with small worked numbers (3rd ed., ch. 8, 'Recovering a key from
  a reused nonce'), two signatures that share a nonce hand you two equations in two unknowns..."*

**Why this form:** it names the source every time it is used (no ambiguity about whose content it is), it
pinpoints precisely enough that a student can find the passage, and it needs no separate numbered
reference list or footnote apparatus to maintain across dozens of slides and an interactive page — useful
given how often a course chapter draws on its one textbook. Two other conventions (a numbered bracket
citation resolved in a references list; a full author–date parenthetical every time) were also considered
and set aside for SEN0401 as heavier than needed here, but either could suit a course that cites several
sources evenly rather than one dominant textbook.

**Already applied:** SEN0401's Chapter 8 draft, `v1.2.0`, rewrites the flagged sentence and one other
("...the one the chapter teaches next" → "...the one Mastering Bitcoin covers next (3rd ed., ch. 8, 'RFC
6979 test vector')...") using this convention, and keeps it for both the deck and the interactive page, on
the owner's instruction that the two should match.

**For CME to decide:** whether to adopt named-in-prose-plus-pinpoint as the default citation convention for
every CME-governed course that works from a primary source textbook, or to let each course choose from the
three conventions above depending on how many sources it draws on.

## 4. Disposition

Nothing in CME's own ontology, lineage, or tooling has been touched by this handover. Both items above are
descriptions of a decision already made for SEN0401, offered for CME's own session to judge on its own
timeline and its own package-wide view — per the standing rule that decisions about another package belong
to that package's own session. No reply is expected before SEN0401's Chapter 7–8 rendering work continues.
