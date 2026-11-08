# SEN0401 — Chapter 8 draft: Digital Signatures (Mastering Bitcoin, 3e)

**For your reading before any deck/page rendering — Lineage 4, story 2.** Carried from the existing
Chapter 8 deck (v2.0.0), which already passes the full deck standard D1–D12 this session (51 slides, 20
code slides, 7 native charts, 0 FAIL). Structure from that deck, laid out for your yes/no; nothing
renders until you approve.

## 1. The story (5N1K), already in the deck, verified against primary sources

Three true stories, each with all six of WHO/WHAT/WHEN/WHERE/WHY/HOW, a picture and a live link (D5
measured PASS):

1. **1991-02-19 — Schnorr's patent.** WHO Claus-Peter Schnorr · WHERE the United States patent office ·
   WHAT patent 4,995,082 published, for the scheme from his Crypto '89 paper · WHY the patent kept it out
   of open standards, so ECDSA was Bitcoin's only signature until 2021 · HOW term = longer of 17 years
   from grant / 20 from filing, so it ended 2010-02-23 · SO WHAT BIP340 is Schnorr fitted to secp256k1,
   live with taproot 30 years after the paper. Picture: Claus-Peter Schnorr, Oberwolfach 1986 (Konrad
   Jacobs, CC BY-SA 2.0 de). Link: Schnorr's patent US 4,995,082 (image-ppubs.uspto.gov).
2. **2013-12-27 — the book's own signature is a real payment.** WHO the unnamed sender of a mined payment
   · WHERE block 277,316 · WHAT the long DER hex the book dissects (`3045022100884d142d...`) is tx
   `0627052b...c345c2f2`'s real signature, not invented · WHY a real example can be checked end to end ·
   HOW mined 23:11:54 UTC, R is 33 bytes (top bit set) · SO WHAT its S is already low-form, so a node
   would still relay it today. Link: the signed payment in block 277,316 (mempool.space). *(No picture of
   the sender exists — a stand-in, the Bitcoin logo, is used; flag if you want this handled differently.)*
3. **2013-08-11 — Android's weak randomness.** WHO Alex Klyubin (Google), Android wallet users · WHERE
   Android phones worldwide · WHAT Bitcoin.org warned Android's RNG was weak, exposing wallets built on it
   · WHY a weak generator can repeat/leak a signing nonce, which hands over the private key · HOW Klyubin
   explained the flaw 3 days later; Bitcoin Wallet and others shipped fixes · SO WHAT RFC 6979's
   deterministic nonce is why Core no longer needs a good RNG for signing. Picture: the Android robot
   (Google/Irina Blok, CC BY 3.0). Link: Bitcoin.org Android alert. *(Stand-in: the platform, not the
   incident — same flag as above.)*

**Two of the three stories use a stand-in picture rather than a picture of the actual event/person — say
if you want real incident photos sought instead, or keep the stand-ins.**

## 2. The explanations (what each part teaches, in order)

Seven parts, 45 key concepts, each with an everyday analogy (D4 measured 100%):

1. **Foundations of digital signatures** — what a signature proves (integrity + binding to a key),
   verification inputs, curve arithmetic (scalars mod n), the sign/verify round trip.
2. **Signature hash flags (SIGHASH)** — the one-byte flag appended to a signature, ALL/NONE/SINGLE ×
   ANYONECANPAY, what each commits to, the SIGHASH_SINGLE bug and how Core refuses it, ANYPREVOUT
   (BIP118).
3. **Schnorr signatures** — from Fiat–Shamir identity proof to signature, BIP340's format, x-only keys,
   tagged hashes, linearity/batch verification, key aggregation (MuSig2) and the key-cancellation attack
   it defeats, Shamir secret sharing for threshold signing.
4. **ECDSA signatures** — the ECDSA equations, signature malleability, the low-S rule, DER serialization
   (the book's own real signature lives here).
5. **Randomness and signature size** — nonce reuse recovers the key (worked with small numbers),
   deterministic nonces (RFC 6979), low-R grinding (the Android story lives here).
6. **Segwit signing** — the old algorithm's quadratic hashing cost vs. BIP143/BIP341 amount commitments.
7. **Since the book went to print** — standards/BIP status update, library/Core release support,
   patent-term arithmetic (the Schnorr-patent story lives here, closing the loop opened in part 1).

## 3. Slide outline, in deck order (dividers in **bold**, 51 slides total)

5 **Foundations of digital signatures** · 6–10 what a signature proves, verification, curve arithmetic,
sign/verify
11 **Signature hash flags (SIGHASH)** · 12–16 flag byte, commitments matrix, the SINGLE bug
17 **Schnorr signatures** · 18–21 toy protocol, Fiat–Shamir, BIP340 format
22 *story: Schnorr's patent* · 23–27 x-only keys, tagged hashes, linearity, MuSig2, key cancellation
28 **ECDSA signatures** · 29–32 ECDSA equations, malleability, DER layout
33 *story: the book's own signature* · 34–35 the sample verifies, low-S rule
36 **Randomness and signature size** · 37–38 nonce reuse recovers the key
39 *story: Android's weak RNG* · 40–41 RFC 6979, low-R grinding
42 **Segwit signing** · 43–45 quadratic hashing, amount commitments
46 **Since the book went to print** · 47–48 patent-term dates, standards/BIP status
49 five-line recap · 50 *resources* · 51 *closing claims*

**This is the existing deck's order — confirm it, or tell me what to move.**

## 4. Page tabs, same order as the slide outline above

The interactive page (currently v9.86.0) follows the same seven parts as tabs, sub-divided by the
divider's own slide range above. Not independently re-verified against 9.86.0 this session — flagged,
checked before the page is re-rendered from this draft, not before.

## 5. Code examples, with their executed result (20 code slides in the current deck)

Carried as-is from the existing deck (each has a plain-language explanation beside it and a native
chart/table/diagram as the executed result — D3 measured 100%), unless you want a different example:

- Verification equation worked over the curve, with a wrong-key case shown failing.
- SIGHASH flag byte decoded for a real signature; the commitments matrix for ALL/NONE/SINGLE × ACP.
- The SIGHASH_SINGLE "no output" bug reproduced, then shown refused by Core's test vectors.
- Fiat–Shamir identity round with small numbers, honest vs. forged response.
- BIP340 test vector verified; signature size compared (64 bytes) against DER's variable length.
- Naive multisig key addition attacked by key cancellation; MuSig2 shown resisting it.
- Shamir secret sharing with small numbers (mod 101): any two of three shares reconstruct, one alone does not.
- ECDSA sign/verify with small numbers; the "other valid S" shown for the malleability point.
- The book's own DER signature (block 277,316) parsed byte by byte, R's padding zero explained.
- Nonce reuse: two signatures, same nonce, two equations — the private key recovered.
- RFC 6979 test vector: deterministic nonce reproduced, matching the standard and Core.
- Low-R grinding: chance of a low R by trial, grinding shown shortening the signature.
- Quadratic-hashing cost measured for a transaction with a growing number of inputs.
- BIP143/BIP341 amount commitment compared against the pre-segwit signature hash.
- A first real taproot key-path spend verified end to end.

## 6. Resources (already live links, carried from the current deck's resources slide)

BIP340 (bips.dev) · Mastering Bitcoin 3e, ch. 8 AsciiDoc source (GitHub) · OP_CHECKSIG, Bitcoin Wiki
(en.bitcoin.it) · BIP327: MuSig2 (bips.dev) · RFC 6979 · Schnorr, "Efficient signature generation" (1991,
Journal of Cryptology) · MIT 15.S12 Blockchain and Money lectures (ocw.mit.edu) · Optech Schnorr/Taproot
workshop · Bitcoin Optech newsletters · Delving Bitcoin · bitcoin-dev mailing list.

## Your call

1. Keep the three stories as-is (including the two stand-in pictures), or want real incident photos
   sought for the book-signature and Android stories?
2. Approve the slide/page outline above as this run's teaching order, or move anything?
3. Any of the 20 code examples to swap, drop or add?

Reply with changes or "approved" and the deck/page render for Chapter 8 begins from this draft.
