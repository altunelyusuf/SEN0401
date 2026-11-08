# SEN0401 — Chapter 7 draft: Authorization and Authentication (Mastering Bitcoin, 3e)

**For your reading before any deck/page rendering — Lineage 4, story 1.** Carried from the existing
Chapter 7 deck (v2.2.0), which already passes the full deck standard D1–D12 this session (61 slides, 15
code slides, 3 native charts, 0 FAIL). This draft is the structure that deck already has, laid out for
your yes/no, not a rewrite from nothing. Say which parts to keep, cut or change; nothing renders until
you approve.

## 1. The story (5N1K), already in the deck, verified against primary sources

Three true stories carry the chapter, each with a real picture, a live link and all six of WHO/WHAT/WHEN/
WHERE/WHY/HOW (deck standard D5, measured PASS):

1. **2010-07-28 — the OP_RETURN bug.** WHO Satoshi Nakamoto · WHERE the Bitcoin test network · WHAT two
   bugs were shown that let a stranger spend coins that were not theirs · WHY the first software joined
   input and output script into one program and OP_RETURN jumped to the end with a true result · HOW an
   input script of `1` then `OP_RETURN` ended the run true; v0.3.5 fixed it by running the scripts apart
   · SO WHAT many unused opcodes are now `OP_SUCCESS` in tapscript. Picture: bust of Satoshi Nakamoto,
   Budapest (Fekist, CC BY-SA 4.0). Link: en.bitcoin.it.
2. **2015-07-04 — the BIP66 fork.** WHO Pieter Wuille and the miners who had not upgraded · WHERE block
   363,725 · WHAT strict DER signatures took effect and a six-block fork followed · WHY about half the
   hash rate was not fully validating · HOW the fork ran 02:10–03:50 UTC, no double spend shown · SO WHAT
   a rule you do not check protects nobody — Bitcoin Core 0.9.5+ was unaffected. Picture: a bitcoin mining
   farm, 2014 (Marko Ahtisaari, CC BY 2.0). Link: bitcoin.org.
3. **2021-11-14 — taproot activates.** WHO Claus-Peter Schnorr · WHERE block 709,632 · WHAT taproot and
   Schnorr signatures (BIP340–342) took effect · WHY Schnorr's patent kept his scheme out of open
   standards for two decades, so ECDSA was used instead · HOW BIP340 assigned January 2020, soft-forked
   in · SO WHAT a key-path spend is one 64-byte signature indistinguishable between one signer and a
   million. Picture: Claus-Peter Schnorr, 1986 (Konrad Jacobs, CC BY-SA 2.0 de). Link: mempool.space.

**Keep all three as-is, unless you want a different emphasis for this run of the course.**

## 2. The explanations (what each part teaches, in order)

Nine parts, 87 key concepts, each covered by an everyday analogy in the current deck (D4 measured 100%):

1. **Transaction scripts and the Script language** — stack-based, Turing-incomplete, stateless; a script
   succeeds when the stack's top value is true; input and output scripts run and are checked separately
   (the OP_RETURN story lives here).
2. **Locking a coin to a key** — pay-to-public-key, public-key hash, pay-to-public-key-hash, OP_CHECKSIG,
   the signature hash, DER encoding (the BIP66 story lives here).
3. **Scripted multisignatures** — the t-of-k script, the CHECKMULTISIG dummy-element quirk, signature
   check count.
4. **Pay to script hash** — hashing the redeem script, the P2SH address, what the hash changes, P2SH
   validation rules, the benefits (shorter outputs, flexible redeem logic revealed only at spend time).
5. **Data output and timelocks** — OP_RETURN as data carrier, absolute locktime, OP_CHECKLOCKTIMEVERIFY,
   relative timelock (sequence), OP_CHECKSEQUENCEVERIFY.
6. **Flow control and complex scripts** — OP_IF/VERIFY, scripts with several paths, the capital-account
   script example, a nod to Miniscript.
7. **Segregated witness scripts** — witness programs, P2WPKH, P2WSH, bech32 addresses, the
   backward-compatible (nested) upgrade path, the witness signature hash.
8. **Script trees and key tweaks** — MAST, tweaking keys, pay-to-contract, scriptless multisignature,
   threshold signature (the two ideas taproot combines).
9. **Taproot and tapscript** — the taproot output, key-path spending, script-path spending, control block,
   tapscript's changes (OP_CHECKSIGADD, OP_SUCCESS) — the taproot story lives here.

## 3. Slide outline, in deck order (dividers in **bold**, 61 slides total)

5 **Scripts and the Script language** · 6–9 stack, Turing-complete, the two scripts joined (2010 run-up)
· 10 *story: OP_RETURN bug* · 11–12 output/input script, stack, Turing-complete recap
13 **Locking a coin to a key** · 14–17 P2PK, P2PKH, sighash, DER · 18 *story: BIP66 fork*
19 **Scripted multisignatures** · 20–22 t-of-k, CHECKMULTISIG dummy element, sig-check count
23 **Pay to script hash** · 24–26 P2SH address, redeem script, benefits, validation rules
27 **Data and timelocks** · 28–32 OP_RETURN data, absolute/relative timelocks, CLTV/CSV
33 **Flow control and complex scripts** · 34–36 OP_IF/VERIFY, capital-account example
37 **Segregated witness scripts** · 38–44 P2WPKH/P2WSH, bech32, nested upgrade, witness sighash
45 **Script trees and key tweaks** · 46–49 MAST, membership proof, key tweak, threshold signature
50 **Taproot and tapscript** · 51–52 taproot output, key-path spend · 53 *story: taproot activation*
54–58 internal/output key, script-path spend, tapscript, OP_SUCCESS
59 five-line recap · 60 *resources* · 61 *closing claims*

**This is the existing deck's order — confirm it, or tell me what to move.**

## 4. Page tabs, same order as the slide outline above

The interactive page (currently v9.85.0) follows the same nine parts as tabs, each sub-divided by the
divider's own slide range above, so a page tab and its matching slide range stay in lock-step (the
2026-10-14/15 check flagged Chapters 4–7 as the largest gap on this point for the *old* page version; not
re-verified against 9.85.0 this session — flagged, not assumed clean, and checked before the page is
re-rendered from this draft, not before).

## 5. Code examples, with their executed result (15 code slides in the current deck)

Each is a running Script-interpreter or library example with its real output shown beside it (deck
standard D3, measured 100% — every code slide has both a plain-language explanation and a visual/executed
result). Carried as-is from the existing deck unless you want a different example:

- Stack trace of a simple output+input script run to `true`.
- The 2010 OP_RETURN exploit script, run and shown ending `true` on an unpatched interpreter.
- P2PK and P2PKH locking/unlocking scripts, hash160 shown step by step.
- A DER-encoded signature parsed into r/s with its hash type byte.
- A 2-of-3 CHECKMULTISIG script run, including the dummy OP_0 element.
- P2SH: hashing a redeem script, building the output, then redeeming it.
- OP_RETURN data carrier built and the relay-policy cap on its size.
- CLTV and CSV scripts run against a given block height / relative lock.
- The capital-account OP_IF example run down both branches.
- P2WPKH and P2WSH witness programs built and their bech32 address derived.
- A nested-segwit (P2SH-wrapped) output/redeem pair.
- A Merklized alternative script tree: leaf, sibling hashes, root.
- A key-tweak (pay-to-contract) computation, with and without the tweak.
- A taproot key-path spend: one 64-byte Schnorr signature verified against the output key.
- A taproot script-path spend: leaf script, control block, verified.

## 6. Resources (already live links, carried from the current deck's resources slide)

Bitcoin white paper (bitcoin.org) · Script, Bitcoin Wiki (en.bitcoin.it) · Optech topic: Taproot ·
Taproot, Bitcoin Wiki (en.bitcoin.it) · BIP66 (bips.dev) · BIP141 (bips.dev) · BIP341 (bips.dev) · BIP342
(bips.dev) · `script.cpp` of Bitcoin 0.3.0 (source) · CVE-2010-5141 (Bitcoin Wiki) · "Some Miners
Generating Invalid Blocks" alert (bitcoin.org) · Bitcoin Stack Exchange · Delving Bitcoin · Optech
workshop 1.1: Schnorr (video) · Optech workshop 2.3: Tapscript (video).

## Your call

1. Keep the three stories and nine-part structure as-is, or change the emphasis?
2. Approve the slide/page outline above as this run's teaching order, or move anything?
3. Any of the 15 code examples to swap, drop or add?

Reply with changes or "approved" and the deck/page render for Chapter 7 begins from this draft.
