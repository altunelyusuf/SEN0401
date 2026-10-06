# Chapter 1 deck v2.7.0 - the three-role review record

The owner's working method of 2026-10-06: an experienced blockchain academician prepares, an
expert faculty specialist in course materials and blockchain reviews, and an undergraduate
student reads for comprehension. This file records one full cycle over deck v2.7.0 (44 slides);
the same cycle applies to every later deck and page build.

## The academician's build notes
- Every fact on a slide traces to the chapter corpus, the executed examples, the story
  companion v1.1.0 (dated, sourced stories), or data fetched and verified in this build:
  block 0's 285 raw bytes (hash re-verified by double-SHA256 in the build script) and the
  live price (two independent APIs, 0.03% apart).
- Teaching arc: outcomes → chapter questions → concept map → origins stories → money (history,
  comparison, unit, supply, price, Pizza Day) → network → wallets → foundations → nature →
  resources → closing. Stories open each conceptual block because they anchor memory.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Slides numbered; one continuous warm-ivory theme; no dark-light switches | pass |
| Sentences allowed, paragraphs banned (20-word bullet gate, 26-word ledes) | pass, enforced by the builder |
| Every code block labelled, explained, and its executed result visualized | pass (bars, route, claims, chain, funnel, charts) |
| Every number on a slide asserted against corpus, examples, or build-time fetch | pass, builder refuses otherwise |
| Stories dated and sourced; external images carry licence credits on-slide | pass |
| Notes are cues (SAY/ASK/FULL TEXT), never prose | pass |
| Resources slide: live links, grouped, reachable set checked 2026-10-06 | pass |
| deck_check (12 examples re-run off the finished file) and layout check | 0 mismatches; clean |

## v2.5.0 round - the owner's review answered
- Charts are native PowerPoint chart objects now, never pictures; the log value axis is
  guaranteed by deck_chart_logaxis_v1_0_0.py (it refuses if it finds no log chart to fix).
- Museum artifacts (CC0) joined the money timeline: CMA's lion stater, the Met's barley tablet.
- Three new slides carry the argument the owner asked for: physical cash's limits, why digital
  money waited forty years (the copy problem, drawn), and how the public ledger kills the
  double-spend (drawn, with the refused copy visible).
- Every program slide now leads with numbered plain-language execution steps and the result
  visualization; the exact code remains, compact, labelled for later reading - nobody has to
  parse source in their head.
- Sentence gates relaxed to the owner's rule: as short as possible, hard stop only at
  paragraph length.

## v2.6.0 round - the owner's 5N1K ruling answered
- Every story slide carries a WHO / WHERE / WHEN / READ fact row; the READ chip is a live link.
  The fields live in the story companion v1.2.0 and its self-check refuses a story without them.
- The Mt. Gox slide names the company, the city, the CEO (Mark Karpeles) and the dated court
  filing on the slide itself, with the link - no more unattributed parable.
- A key-analogy slide maps house and car keys onto bitcoin keys: key grants access everywhere,
  but in Bitcoin the key is also the deed, so it must prove without being shown.
- Program code is syntax-coloured (keywords, strings, numbers, comments) and the builder now
  computes the font from the longest line and the line count, refusing any wrapping layout;
  long programs moved to full-width strips.

## v2.7.0 round - the payment-history synthesis
- The money arc now runs: history timeline with museum artifacts -> the three-kinds table ->
  physical cash's limits -> the dot-com payment race (Confinity 1998, X.com 1999, the 2000
  merger into PayPal, the 2001 deaths of Beenz and Flooz, eBay 2002) -> five documented
  when-money-stops cases (Kenya 2007, Cyprus 2013, Greece 2015, Venezuela 2018, Ukraine 2022,
  each card with its own READ link) -> the copy problem -> the double-spend solution.
- All new facts pass 5N1K: named founders, dated events, per-case links; the Ukraine case cites
  the official programme run by Deputy Minister Alex Bornyakov (~$35M in the first week).

## The undergraduate's read-through (full-deck contact sheets)
- v2.4.0 FOUND: closing-slide overlap - fixed. v2.5.0 FOUND: three program code boxes too small for
  their listings and one bar label off-slide - code boxes resized to their line counts (long programs
  get the full column), bars narrowed; layout check clean. LibreOffice render confirmed the log axis.
- The genesis hex dump reads: the orange bytes visibly spell the headline; the Times card beside
  it says what the bytes mean. Understandable without the notes.
- The comparison table answers "so what is different?" in one look; the timeline gives the
  5,000-year frame before the unit arithmetic starts.
- No slide now requires the speaker notes to be understood; the notes add delivery cues only.
