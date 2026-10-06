# Chapter 2 deck v2.0.0 - the three-role review record

The owner's working method: an experienced blockchain academician prepares, an expert faculty
specialist in course materials and blockchain reviews, and an undergraduate student reads for
comprehension. This file records the first full cycle over the chapter-2 classroom redesign
(30 slides), which jumps chapter 2 straight to the chapter-1 v2.8.0 standard - recorded as the
CME materials look-and-feel standard v1.0.0 - and is drawn by the SHARED renderer
08-tooling/deck_render_v1_0_0.js, so chapters carry one look.

## The academician's build notes
- One payment, followed all the way: Alice pays Bob opens the Transactions part (the textbook's
  own double-entry figure), then UTXOs, change, and byte-priced fees; the network part carries
  it by gossip to every mempool; the blockchain part buries it under proof-of-work and prices
  its safety; semantics and practice close with the course page's own triple store and three
  take-home consoles.
- Every number shown is asserted against the chapter corpus, the executed examples
  (examples_out_v1_2_0.json), or the story companion's pinned sources; the builder refuses
  anything else. The whitepaper's section-11 table is not quoted: examples group
  AttackerSuccess reruns the paper's procedure (the chapter research record matched its q=0.1
  column to seven decimals) and the chart draws only what it returned.
- Three 5N1K stories anchor the three hard ideas: the 2008-10-31 whitepaper announcement (The
  Cryptography List card + the abstract's first sentence), Gavin Andresen's 1,100-BTC faucet of
  2010-06-11 (his CC BY 2.0 photo, credit on-slide), and the 184-billion-BTC value-overflow
  block 74,638 of 2010-08-15 (its forged outputs drawn as refused claims). Each carries a
  WHO/WHERE/WHEN/READ fact row with a live link.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Slides numbered; warm-ivory theme; agenda with exact ranges; summary before resources | pass |
| Short sentences only; word gates enforced by the builder | pass |
| Every console labelled, led by plain-language steps, result visualized (bars, funnel, claims, chips, stat) | pass |
| Code syntax-coloured; no line wraps (width gates; long consoles moved to full-width strips) | pass |
| Native chart with data labels on a true log axis; series = the executed example only | pass |
| Stories 5N1K with real pictures and on-slide licences/credits | pass |
| Notes are cues (SAY/ASK/FULL TEXT) | pass |
| deck_check_v1_2_0 (18 examples re-run off the finished file) and layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 2, 6, 7, 9, 12, 17, 21, 23)
- FOUND and fixed: the fee-rate stat tiles and the Block ratio console were a few points too
  short for the pessimistic height model; the Gavin Andresen photo caption's second line grazed
  the takeaway strip (photo shortened).
- The attacker chart reads at a glance: two labelled lines, 0.2046 falling to 0.0002 against
  1-6 confirmations - the "six confirmations" rule stops being folklore.
- The change slide answers the first question students actually ask (where did the rest of my
  coin go?) with three labelled bars and the arithmetic chip.
- No slide requires the speaker notes to be understood; the notes add delivery cues only.
