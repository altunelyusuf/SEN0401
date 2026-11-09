# SEN0401 — Chapter 8 draft: Digital Signatures (Mastering Bitcoin, 3e)

**v1.3.0 — over v1.2.0, which stays committed: the D5/narrative tension flagged there is now resolved, by
the owner's instruction. The live deck is rebuilt as `SEN0401_Ch08_DigitalSignatures_3e_v2_1_0.pptx`: the
three story slides' WHO/WHERE/WHEN chips are gone, their facts folded into the narrative sentences (the
sender's anonymity is now stated in prose on slide 33's stand-in caption, the block number is now in the
HOW sentence), and the WHAT/WHY/HOW/SO WHAT boxes keep their sentences with the on-screen label stripped.
The deck-standard checker is now `sen0401_deck_standard_check_v2_0_0.py` — see the Chapter 7 draft's note
for how D5 changed. Both decks pass D1–D12 clean. Nothing else changed from v1.2.0.**

**For your reading before any deck/page rendering — Lineage 4, story 2.**

**Citation convention used below:** name the book in the sentence that uses its content, with a pinpoint
to its own section title in parentheses — e.g. *"as Mastering Bitcoin shows (3rd ed., ch. 8, 'Nonce
reuse')..."* — never a sentence that speaks as if this chapter *is* that section.

## 1. The story, as three narratives

**A patent that decided which signature Bitcoin would start with.** Claus-Peter Schnorr had presented an
efficient identification and signature scheme at the Crypto '89 conference, and on 19 February 1991 the
United States published his patent on it, number 4,995,082 — filed a year earlier, on 23 February 1990,
and claiming priority back to 24 February 1989. In the United States a patent's term is the longer of
seventeen years from grant or twenty from filing, which put its expiry at 23 February 2010. For as long as
it stood, the patent kept Schnorr's scheme out of open standards, so when Bitcoin needed a signature
algorithm it reached for ECDSA instead — the scheme the cryptographic community had built around in the
meantime. Only after the patent lapsed did Schnorr's original idea return: BIP340 is that same scheme,
fitted to the secp256k1 curve, and it went live bundled with taproot — thirty years, almost to the month,
after the paper that started it.

**The signature printed in the book is not an invented example.** The long hexadecimal string that the
book's DER section dissects, beginning `3045022100884d142d`, is a real signature. It sits in the input of
transaction `0627052b6f28912f2703066a912ea577f2ce4da4caa5a5fbd8a57286c345c2f2`, mined in block 277,316 at
23:11:54 UTC on 27 December 2013. That matters because a real example can be checked rather than just
read: the chapter recomputes the signature, and the key, the transaction and the signature all agree with
each other. Its R value happens to run 33 bytes, because its top bit is set and DER pads it with a zero
byte to keep the number unambiguously positive — a detail the book uses to explain DER's layout. Its S
value, on the other hand, is already in the low form, so the same signature would still be relayed by a
node today. *(No photograph of the sender exists, since nobody knows who they were; the slide uses the
Bitcoin logo as a stand-in — flag if you'd rather handle this differently.)*

**The night Android's randomness turned out not to be random.** On 11 August 2013, Bitcoin.org published
an alert: the component Android used to generate secure random numbers had critical weaknesses, and every
wallet whose keys had been generated on an affected phone was exposed. The danger wasn't abstract — as Mastering Bitcoin shows with small worked numbers (3rd ed., ch. 8,
"Recovering a key from a reused nonce"), two signatures that share a nonce hand you two equations in two
unknowns, and solving them hands over the private key. Three days later, Alex Klyubin at Google explained
the flaw in public, and wallets including Bitcoin Wallet, blockchain.info, BitcoinSpinner and Mycelium
shipped fixes; Bitcoin Wallet 3.15 went further and rotated affected keys automatically. The long-term fix
for the whole class of problem is the one Mastering Bitcoin covers next (3rd ed., ch. 8, "RFC 6979 test
vector"): RFC 6979 derives the nonce deterministically from the key and the message itself, so a weak
random-number generator can no longer leak anything through it.
*(Picture: the Android robot, designed by Irina Blok for Google, CC BY 3.0 — a stand-in for the platform,
not the incident itself.)*

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

1. Keep the three stories as narrative, or want anything in them reshaped — e.g. real incident photos
   sought for the book-signature and Android stories instead of the two stand-ins?
2. Approve the slide/page outline above as this run's teaching order, or move anything?
3. Any of the 20 code examples to swap, drop or add?
4. Resolved, same as Chapter 7's draft: the live deck no longer carries on-screen labels, and the checker
   now fails one if it did. Nothing further to decide here.

Reply with changes or "approved" and the deck/page render for Chapter 8 begins from this draft.
