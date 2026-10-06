# Chapter 4 deck v3.0.0 - the three-role review record

Same method as chapters 1-3; first cycle over the chapter-4 classroom redesign (25 slides),
drawn by the shared renderer (CME materials standard v1.0.0).

## The academician's build notes
- Arc: keys (the number, the curve checked live, the 13-line double-and-add that the checker
  REQUIRES verbatim because it computed every key shown, proof-without-showing) -> formats
  (Satoshi's base58 memo quoted from the pinned tree, WIF round trip, the checksum refusing a
  real typo) -> addresses (the full pipeline Core-validated, the burn address with live-fetched
  figures, segwit/bech32 with BIP-350 vectors and counted error-detection) -> practice
  (reuse counted, one-seed derivation as the chapter-5 hook).
- Three 5N1K stories with fact rows, live links, licensed pictures: the 1976 Diffie-Hellman
  paper (their Commons photo), the base58 design memo (the file's own copyright line names
  Satoshi), and 1BitcoinEater... - 13.41747849 BTC over 5,832 deposits, spent 0, fetched from
  blockstream.info during this build and pinned in the story companion's EATER table.
- deck_check_v2_0_0 re-ran 47 '>>>' examples off the finished file (0 mismatches) and verified
  the EC source on slide 9 equals the module the examples import. The builder now gates console
  HEIGHT as well as width, so a box too short for its statement+output lines refuses the build.

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory; agenda ranges; summary; takeaway strips | pass |
| Word gates; cue-style notes | pass |
| Every console labelled, steps alongside, results shown; errors shown as the run raised them | pass |
| No wrapped lines (three consoles moved to full-width strips during the round) | pass |
| Native-chart rule: no sourced series in this chapter, no decorative chart faked instead | pass |
| Stories 5N1K; licences on-slide and in ASSETS_PROVENANCE_v1_0_0.md | pass |
| deck_check (47 examples + EC-source gate) and layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 2, 6, 9, 12, 16, 18, 22)
- FOUND and fixed: four consoles sized for rows instead of statement+output lines (height gate
  added, boxes resized); one label hidden behind the EC panel; a takeaway duplicating its sub.
- The memo slide reads as intended: Satoshi explaining his own alphabet beats any paraphrase.
- The pipeline slide ends on the exact address the node validated - nothing left abstract.
