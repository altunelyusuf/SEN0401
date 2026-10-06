# Chapter 3 deck v2.0.0 - the three-role review record

Same method as chapters 1 and 2 (academician prepares, expert faculty specialist reviews,
undergraduate reads); first full cycle over the chapter-3 classroom redesign (23 slides), drawn
by the shared renderer so chapters 1-3 now carry one look (CME materials standard v1.0.0).

## The academician's build notes
- Arc: what the node is (postures, the real architecture figure) -> from source to binary
  (tags, reproducible builds, the build with chapter 1's subsidy staircase as its unit test) ->
  running and talking to it (a REAL 31.1 startup log line, the systemd unit's own flags read
  from the pinned source tree, JSON-RPC with the captured getblockchaininfo) -> the chain as
  data (block 123,456's Merkle root recomputed; Alice's real transaction decoded, its txid and
  wtxid derived from her raw bytes).
- Three 5N1K stories with fact rows and live links: v0.1 of 2009-01-09 (The Cryptography List
  front page; the 'set in stone' sentence correctly attributed to Satoshi's 2010-06-17 forum
  post), the maintainer handoffs of 2011 and 2014, and reproducible builds with the guix.sigs
  attestation repository.
- Long chapter programs appear as HONEST EXCERPTS: the caption says 'lines a to b of n' and
  deck_check verifies each excerpt against the full program; a new COMPACT panel mode draws the
  result and caption inside the code panel, so program slides keep clear of the takeaway strip.
  Every block's result is on the deck (the serialization and malleability tuples ride the
  decode slide's numlist, captioned from the programs' own field names).

## The expert reviewer's checklist and findings
| check | result |
|---|---|
| Numbered slides; warm-ivory theme; agenda with exact ranges; summary before resources | pass |
| Short sentences; word gates; notes are cues | pass |
| Every console/program labelled, steps alongside, result shown (compact panels, stats, funnels) | pass |
| No wrapped code lines (width gates; three layouts widened during the round) | pass |
| Stories 5N1K, pictures licensed (owner's deck art, MIT project icon and GUI, CC BY-SA figure) | pass |
| deck_check (17 examples re-run off the finished file) and layout check | 0 mismatches; clean |

## The undergraduate's read-through (contact sheets of slides 2, 4, 6, 10, 11, 13, 16, 17, 19, 20)
- FOUND and fixed: three consoles too narrow for their longest line (widened to full strips);
  program result lines below panels collided with the takeaway strip (compact mode added);
  one stat row too short for its figures; a label glued to the panel above it.
- The reproducible-builds funnel plus the 22.0 tile makes 'verify, don't trust' concrete.
- The recomputed 0e60651a... root against a REAL block is the slide students will remember.
