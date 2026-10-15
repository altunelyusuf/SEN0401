# Chapter 8 deck v1.0.0 - the three-role review record

First cycle over the chapter-8 classroom deck (26 slides, Digital Signatures), built from the committed research package (commit 4102ded: 66 sources, 20 findings, 91 executed
claims) with the SEN0401 build port (`sen0401_chbuild_v1_1_0.py`), to the CME look and feel. Every console result was produced by running the statement under Python 3.14.6
(`examples_out_v1_0_0.json`); the notes are short reader's prose (43 to 86 words, mean 66).

## The academician's build notes
- Arc: questions -> A what a signature proves and signs (verify, modulus n against p, the SIGHASH flags with the Core signatures edited, the SINGLE bug) -> B Schnorr (Fiat-Shamir,
  the patent story, BIP340, key aggregation, threshold) -> C ECDSA (formulas, the two forms, the book's signature in block 277,316, nonces with a native chart, the Android story)
  -> D segwit, taproot, policy against consensus, and what moved since print -> summary, resources, closing.
- Book-correcting findings on slides: modulo n against p (6), the SIGHASH_SINGLE bug (8), high-S policy against non-DER consensus (22), the taproot hash type 0x00 (22).
- Three 5N1K stories: SchnorrPatent (19 Feb 1991, Schnorr, CC BY-SA 2.0 de), BookSignature (27 Dec 2013, block 277,316), AndroidRandom (11 Aug 2013, CC BY 3.0).

## Honesty
- Recorded (read from the one regtest run of Bitcoin Core 31.1.0): slides 1, 7, 8, 18, 22.
- NOT EXECUTED, labelled on the slide: slide 12 (batch verification speed-up), slide 23 (ECDSA security proof, quantum attacks, Core releases other than 31.1.0).
- Stand-in pictures, labelled on the slide: 17 (the Bitcoin logo; no free picture of the sender exists), 19 (the Android robot).

## The teacher's notes
- Short sentences, one idea per slide, one takeaway of 78 characters or fewer; every console row is explained by a beat or a caption; six everyday analogies (wax seal, clock, cheque,
  paints, treasure map, one-time pad).

## The student's notes
- Resources slide: Read, Standards and papers, Watch (MIT OCW 15.S12, Optech Schnorr Taproot workshop), Community (Optech newsletters, Delving Bitcoin, bitcoin-dev); 14 links opened.
- YouTube answered 429 from this machine, so no YouTube link is on the deck: a link not opened is not listed.

## Deviations (the owner can overrule)
1. `ch08-deck/post_render_v1_0_0.py` narrows the closing slide's 'Questions?' box (the shared renderer overlaps it with the page number; ch6 and ch7 decks have the same overlap and fail fit).
2. New versions instead of edits: `sen0401_ch08_stories_v1_1_0.py` and `ASSETS_PROVENANCE_v1_1_0.md` replace the MIT-licensed Bitcoin-qt screenshot (the story check accepts only CC BY, CC BY-SA, CC0 and public
   domain) by the public-domain Bitcoin logo, and add `bio` fields; `ch08_schnorr.png` is a lossless PNG of `ch08_schnorr.jpg` so that the picture check's re-encoding control can run.
3. Story slides carry a long-form date in the subtitle and the ISO date only in the WHEN chip, which the stale_date fixture needs.
4. The honesty `vectors` list omits slides 10 and 11 (they show no Core vector or saved block).
5. No chapter-7 lecture export exists in the repository; `ch08-page/lecture_v1_0_0.json` (slides n/title/say/concept) is new.
