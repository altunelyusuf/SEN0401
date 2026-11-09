# SEN0401 — Chapter 7 draft: Authorization and Authentication (Mastering Bitcoin, 3e)

**v1.2.0 — over v1.1.0, which stays committed: the tension flagged there is now resolved, by the owner's
instruction. The live deck is rebuilt as `SEN0401_Ch07_AuthorizationAuthentication_3e_v2_3_0.pptx`: the
three story slides' WHO/WHERE/WHEN chips are gone, their facts folded into the narrative sentences
(Satoshi Nakamoto, Pieter Wuille now named in prose where they weren't before), and the WHAT/WHY/HOW/SO
WHAT boxes keep their sentences with the on-screen label stripped. The deck-standard checker is now
`sen0401_deck_standard_check_v2_0_0.py`: its D5 element finds a story slide by an invisible shape-name
marker instead of visible labels, reads 5N1K coverage from invisible alt-text tags, and now *fails* a
slide that shows a WHO/WHAT/WHEN/WHERE/WHY/HOW label on screen rather than requiring one. Both decks pass
D1–D12 clean under v2.0.0. Nothing else changed from v1.1.0.**

**For your reading before any deck/page rendering — Lineage 4, story 1.**

## 1. The story, as three narratives

**The bug that let a stranger spend your coins.** On 28 July 2010, two bugs surfaced on Bitcoin's test
network. In the software's earliest form, the input script and the output script hadn't yet been split
apart — they ran as one single program. That let someone craft an input script that was just the number
`1` followed by `OP_RETURN`: the `OP_RETURN` instruction jumped straight to the end of the combined
script and left `true` sitting on the stack, as if every check had passed. A stranger could spend coins
that weren't theirs. Satoshi Nakamoto's fix, in version 0.3.5, was to run the two scripts separately from
then on, so neither could reach into the other's territory. The long tail of that decision is still
visible today: many of the opcodes that were disabled in the aftermath — among them `OP_LSHIFT`, numbered
152 — now show up in tapscript simply as `OP_SUCCESS`, retired rather than reactivated.
*(Picture: the bust of Satoshi Nakamoto in Budapest, by Fekist, CC BY-SA 4.0. Further reading:
en.bitcoin.it.)*

**The afternoon half the network stopped validating.** By 2015, Pieter Wuille's BIP66 had set a rule:
every signature must be strict DER, no exceptions. The rule activated on 4 July 2015, the moment 950 of
the last 1,000 blocks were marked version 3 — which happened at block 363,725. About half of the
network's hash power, it turned out, was mining without fully validating blocks, and it kept building on
top of a block that had been mined by someone who hadn't upgraded and had broken the new rule. The result
was a six-block fork that ran from 02:10 to 03:50 UTC, with a second, smaller wobble of three blocks the
next day. No coins were double-spent in either case, but the lesson held: Bitcoin Core 0.9.5 and later
versions, which actually checked the rule rather than trusting the chain, sailed through unaffected. A
rule nobody checks for themselves protects nobody. *(Picture: a bitcoin mining farm, 2014, by Marko
Ahtisaari, CC BY 2.0. Further reading: bitcoin.org.)*

**A patent that outlived its usefulness by two decades.** Claus-Peter Schnorr discovered an elegant
signature scheme and patented it. For almost twenty years, that patent kept his design out of open
standards and open-source software — which is exactly why Bitcoin launched with ECDSA, the scheme that
cryptographers built instead while Schnorr's own idea sat behind a licence wall. Only once the patent had
run its course did the Bitcoin developers pick it back up: BIP340 was assigned in January 2020, formally
adapting Schnorr's scheme to the secp256k1 curve, and a soft fork carried taproot and tapscript onto the
running chain at block 709,632, mined on 14 November 2021. What makes a taproot key-path spend elegant is
that it is one 64-byte signature that looks exactly the same whether it came from one person or was
assembled by a million people acting together — the complexity is invisible from outside. *(Picture:
Claus-Peter Schnorr, 1986, by Konrad Jacobs, CC BY-SA 2.0 de. Further reading: mempool.space.)*

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
· 10 *story: the OP_RETURN bug* · 11–12 output/input script, stack, Turing-complete recap
13 **Locking a coin to a key** · 14–17 P2PK, P2PKH, sighash, DER · 18 *story: the BIP66 fork*
19 **Scripted multisignatures** · 20–22 t-of-k, CHECKMULTISIG dummy element, sig-check count
23 **Pay to script hash** · 24–26 P2SH address, redeem script, benefits, validation rules
27 **Data and timelocks** · 28–32 OP_RETURN data, absolute/relative timelocks, CLTV/CSV
33 **Flow control and complex scripts** · 34–36 OP_IF/VERIFY, capital-account example
37 **Segregated witness scripts** · 38–44 P2WPKH/P2WSH, bech32, nested upgrade, witness sighash
45 **Script trees and key tweaks** · 46–49 MAST, membership proof, key tweak, threshold signature
50 **Taproot and tapscript** · 51–52 taproot output, key-path spend · 53 *story: the patent and taproot*
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
4. **Resolved:** option (a) was taken — D5 now requires the narrative form and fails a visible label. The
   live deck and checker are both updated; nothing further to decide here.

Reply with changes or "approved" and the deck/page render for Chapter 7 begins from this draft.
