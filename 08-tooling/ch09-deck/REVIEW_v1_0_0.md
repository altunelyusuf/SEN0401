# Chapter 9 deck v1.0.0 - the three-role review record

First cycle over the chapter-9 classroom deck (26 slides, Transaction Fees), built from the committed research package (commit 2521ab3: 72 sources, 20 findings, 71 executed
claims, two runs of Bitcoin Core 31.1 on regtest, a census of two mainnet blocks) with the SEN0401 build port (`sen0401_chbuild_v1_1_0.py`), to the CME look and feel, by the method of
the chapter-8 deck (commit c682aac). Every console result was produced by running the statement under Python 3.14.6 (`examples_out_v1_0_0.json`); the notes are short reader's prose
(43 to 90 words, mean 69).

## The academician's build notes
- Arc: questions -> A who pays and how a fee is priced (a fee is a difference, virtual size and the fee rate, minimum fees and dust) -> B estimating and the market (the estimator, two
  mainnet blocks as a native chart, the halving block) -> C replace, bump, relay (the RBF rules, full RBF, the hazards, child pays for parent) -> D pinning, anchors, clusters, sniping
  (the pin as a native chart, anchors, the carve-out, the cluster mempool, fee sniping as a native chart, the instability paper) -> summary, resources, closing.
- Book-correcting findings on slides: the fee rate is fee over size, not size over weight (6); the relay floor is 0.1 sat/vB since Core 30.0 (7); fees against subsidy differ by block (10, 11);
  full RBF is the default since 28.0 and the option is removed (14); the carve-out extra child is 10,000 vB, not 1,000, and it is removed in 31.0 (20, 21); the mempool keeps 300 MB for 336 hours (21);
  the lock time rule is final when below the height (22).
- Four 5N1K stories: HalvingBlock (20 April 2024, CC BY 2.0), FullRbfPeering (12 December 2022, CC0), CarveOutProposal (29 November 2018, CC BY-SA 4.0), InstabilityPaper (21 October 2016, CC0).

## Honesty
- Recorded (read from the two regtest runs of Bitcoin Core 31.1): slides 1, 5, 6, 7, 9, 13, 14, 15, 16, 18, 19, 21, 22.
- NOT EXECUTED, labelled on the slide: 15 (replacement cycling), 20 (the carve-out removal on an older node), 22 (BIP 326), 23 (the undercutting model).
- Stand-in pictures, labelled on the slide: 11 (a mining farm), 14 (a shop sign), 20 (the Lightning logo). Slide 23 shows Nassau Hall, the university of the authors.

## The teacher's notes
- Short sentences, one idea per slide, one takeaway of 78 characters or fewer; every console row is explained by a beat; eight everyday analogies (change at a shop, postage by volume, a bus,
  an auction bid, a friend paying the fare, a lorry behind a car, a spare handle, a ledger page).

## The student's notes
- Resources slide: Read, Standards and papers, Watch (an Antonopoulos video, MIT OCW 15.S12), Community (Optech newsletters, Delving Bitcoin, bitcoin-dev); 15 links opened.
- YouTube watch pages answer 429 from this machine; the video is linked by its embed address, which answers 200, and its title was read through YouTube's oEmbed service
  ("Bitcoin Transaction Fees" - Andreas Antonopoulos, Bitcoin TV).

## Deviations (the owner can overrule)
1. `ch09-deck/post_render_v1_0_0.py` narrows the closing slide's 'Questions?' box, as in chapter 8 (the shared renderer overlaps it with the page number).
2. New versions instead of edits: `sen0401_ch09_stories_v1_1_0.py` (PNG pictures, bio fields, credits without the Commons date so that they fit under the picture, and a 'who' that names the Bitcoin Core rule for the
   pool story) and `ASSETS_PROVENANCE_v1_1_0.md` (sha256 rows, which v1.0.0 did not have); the two JPEG pictures are lossless PNG copies (same pixels).
3. Story slides carry a long-form date in the subtitle and the ISO date only in the WHEN chip, which the stale_date fixture needs.
4. The honesty `vectors` list names the slides that show a saved block, a saved source or a saved page; the claims counted on slide 3 are the 69 taxonomy leaves and 2 corpus checks (71), as the coordinator
   stated, without the four behaviour examples.
5. The chart on slide 10 is one series of four bars because the shared renderer draws no legend.
6. `ch09-page/lecture_v1_0_0.json` (slides n/title/say/concept) is new; there is no chapter-7 lecture export to follow.
