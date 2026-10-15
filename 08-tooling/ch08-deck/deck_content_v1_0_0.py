#!/usr/bin/env python3
"""Chapter 8 (Digital Signatures) deck content, 26 slides, for the SEN0401 deck engine (sen0401_deck_engine_v1_0_0.py). Writes deck_plan_v1_0_0.json.

Every '>>>' row comes from examples_out_v1_0_0.json (executed by examples_v1_0_0.py under Python 3.14.6) and is re-run off the finished file by the deck check.
Every table and chart is built from those executed rows (parsed here and asserted), never typed. Rows that read the record of one run of Bitcoin Core 31.1.0 on
regtest are on slides that say Recorded; what the research marks NOT EXECUTED carries that label; the two pictures that show a platform and an era rather than the event
are labelled stand-in. Speaker notes are short reader's prose (2-4 sentences, at most 100 words, no presenter labels).
"""
import ast, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import sen0401_deck_engine_v1_0_0 as E

import datetime
E.init(8, HERE, assets=("ch08_schnorr.png", "ch08_android.png", "ch08_bitcoinlogo.png"))
C, G, LABEL, STORY = E.C, E.G, E.LABEL, E.STORY
D = C.D
NPUB, NFIND, NCLAIM = len(D.PUBS), len(D.FINDINGS), len(D.TAX) + len(D.CLAIMS) + len(D.BEH)
assert (NPUB, NFIND, NCLAIM) == (66, 20, 91), (NPUB, NFIND, NCLAIM)
OUT = lambda grp, i: ast.literal_eval(G[grp][i][1])
REC = "Recorded"
KEEP = {}          # key -> title, to find the slide numbers once the agenda has been inserted


def con(grp, x, y, w, h, label, fs=10, rows=None):
    return dict(E.code(grp, x, y, w, h, fs=fs, rows=rows), label=label)


def beats(x, y, w, h, items, fs=10.5):
    return {"t": "beats", "x": x, "y": y, "w": w, "h": h, "fs": fs, "items": items}


def foot(x, y, w, h, body, fs=11.5):
    return {"t": "foot", "x": x, "y": y, "w": w, "h": h, "fs": fs, "body": body}


def table(x, y, w, colW, rows, fs=8.5, rowH=None):
    return {"t": "table", "x": x, "y": y, "w": w, "colW": colW, "rows": rows, "fs": fs, "rowH": rowH or [0.2] * len(rows)}


def page(key, title, sub, items, notes, take, lede=None):
    KEEP[key] = title
    E.content(title, sub, items, notes, take=take, lede=lede)


def story(key, sid, photo, standin, beats_, grp, nrows, label, notes):
    st = STORY[sid]
    E.story_slide(sid, photo, (0.5, 1.4, 3.3, 2.45), beats_, grp, G[grp][:nrows] if nrows else G[grp], label, "", (4.1, 3.15, 5.4, 1.2), (4.1, 1.4, 5.4, 1.45))
    s = E.S[-1]
    s["notes"] = notes
    dt = datetime.date.fromisoformat(st["when"])
    s["sub"] = "The story of %d %s %d: who, where, when and what to read next" % (dt.day, dt.strftime("%B"), dt.year)
    for it in s["items"]:
        if it.get("t") == "factrow":
            it["x"], it["w"], it["y"] = 0.5, 9.0, 4.62
    if standin:
        s["items"].append(foot(0.5, 4.26, 3.3, 0.32, standin, fs=9))
    KEEP[key] = s["title"]


# ---------------------------------------------------------------------------------------------- 1-3 opening
E.slide("title", "Chapter 8: Digital Signatures", "What a signature commits to, how schnorr and ECDSA work, and what moved since print. Bitcoin Core 31.1.0 results are Recorded.", [],
        "This deck explains how a Bitcoin signature works and what it commits to. Every example runs under Python 3.14.6 on the chapter's own library, and Bitcoin Core 31.1.0 was run once on a test network, so its answers are Recorded and only read back here. The full text of every slide is in the research package for chapter 8.")

page("questions", "The questions this chapter answers", "Its own competency questions, and the numbers behind the answers",
     [{"t": "numlist", "x": 0.5, "y": 1.4, "w": 9.0, "h": 1.7, "fs": 13, "items": list(C.CQS)},
      {"t": "stat", "x": 0.5, "y": 3.3, "w": 9.0, "h": 1.6, "items": [
          {"n": str(NPUB), "label": "sources, opened and read on %s" % D.DATE},
          {"n": str(NCLAIM), "label": "claims, each recomputed by running code"},
          {"n": str(NFIND), "label": "findings, several of them corrections of the book"}]}],
     "The chapter asks two questions that this deck answers by computation: which of its statements can be reproduced, and which have changed since print. The three numbers below them are counted from the research package, which holds %d sources, %d findings and %d executed claims. Each slide that follows shows the computation behind its claim." % (NPUB, NFIND, NCLAIM), None)
E.S[-1].pop("take", None)

# ---------------------------------------------------------------------------------------------- part A
E.section("What a signature proves and signs", "Sign and verify, the two moduli and the SIGHASH flags. Think of a cheque: ALL fills in every line, NONE leaves the payee blank.",
          [{"label": "Sign, verify, break"}, {"label": "Moduli n and p"}, {"label": "Flags and commitments"}, {"label": "The SINGLE bug"}],
          "This part starts from the verification function, with three inputs and one answer. It then separates the two numbers that the book calls modulus, and shows how the SIGHASH flags choose what a signature covers. The cheque on the slide is the picture to keep: a signature is only as strong as the fields it covers.")
KEEP["secA"] = "What a signature proves and signs"

WAX = "Like a wax seal: anyone can compare it with the ring's pattern, but only the ring's owner can press a new one."
page("sign", "Anyone can verify a signature, no secret needed", "Three inputs go in and yes or no comes out; change any one and it turns to no",
     [{"t": "flow", "x": 0.5, "y": 1.4, "w": 9.0, "h": 0.62, "fs": 11.5, "steps": [
         {"label": "Message", "sub": "a hash of part of the transaction"},
         {"label": "Public key and signature", "sub": "published with the transaction"},
         {"label": "Verify", "sub": "answers yes or no", "hot": True}]},
      con("SignVerify", 0.5, 2.45, 5.7, 1.95, "executed: sign, verify, and two ways to break it"),
      beats(6.4, 2.15, 3.1, 2.3, ["Row 1: sign a message hash with the private key", "Row 2: verify with the public key: 70 bytes, True",
                                  "Row 3: flip one bit of the message: False", "Row 4: use the neighbour's public key: False", "Row 5: two inputs, two owners; swapping fails"]),
      foot(0.5, 4.7, 9.0, 0.3, WAX, fs=11)],
     "A signature check needs only a message, a public key and a signature, so any node can run it without a secret or a link to the signer. The console signs a message hash, verifies it, and then shows two ways to break it: a message changed by one bit and a neighbour's key. The last row shows that two owners can sign two inputs of one transaction independently, and that swapping their signatures fails.",
     "Anyone can verify a signature; only the owner of the key can make one")

CLOCK = "Like a clock: fifteen hours after noon reads three. A dial for points and a dial for scalars are different clocks with different sizes, p and n."
page("moduli", "Scalars live modulo n, coordinates modulo p", "The book says everything is modulo p; the signature equation needs the group order n",
     [con("Moduli", 0.5, 2.05, 5.5, 1.85, "executed: a clock, a toy, and the real curve"),
      beats(6.2, 1.75, 3.3, 2.5, ["Row 1: five divided by three leaves two; that is all modulus 3 means",
                                  "Row 2: plain integers, x 3, G 5, k 7, e 11: s is 40 and both sides give 200; dividing xG by G gives 3 back",
                                  "Row 3: on secp256k1, reduce s modulo n and the check holds; modulo p it fails",
                                  "Row 4: p exceeds n by more than 2 to the power 128; both have 256 bits"]),
      foot(0.5, 4.35, 9.0, 0.55, CLOCK)],
     "The book says the arithmetic is done modulo p, but the scalars of the signature equation are reduced modulo n, the order of the group. The console shows the toy equation with plain integers, where division would reveal the key, and then the real curve, where the equation holds modulo n and fails modulo p. The two numbers are different and both have 256 bits.",
     "Scalars wrap at the group order n; only the coordinates wrap at the prime p",
     lede="The equation sG = kG + eX holds only when s is reduced modulo n, the order of the group of points, and not modulo p.")

# flags: predicted and observed tables, built from the executed rows
pat = OUT("Flags", 0)
NAMES = {"0x1": "ALL", "0x2": "NONE", "0x3": "SINGLE", "0x81": "ALL+ACP", "0x82": "NONE+ACP", "0x83": "SINGLE+ACP"}
assert list(pat) == list(NAMES), pat
pred = [["Flag", "Others' outpoints", "Others' sequences", "Same-index output", "Other outputs", "Own sequence"]] + \
       [[NAMES[h]] + ["yes" if c == "Y" else "-" for c in p] for h, p in pat.items()]
assert pred[1][1:] == ["yes"] * 5 and pred[2][1:] == ["yes", "-", "-", "-", "yes"] and pred[3][1:] == ["yes", "-", "yes", "-", "yes"]


def yn_rows(i):
    out = {}
    for part in OUT("CoreFlags", i).split(" | "):
        k, v = part.rsplit(" ", 1)
        out[k] = v
    return out


surv, acp = yn_rows(0), yn_rows(1)
assert list(surv) == list(acp) and len(surv) == 6
KN = {"ALL": "ALL", "NONE": "NONE", "SINGLE": "SINGLE", "ALL|ANYONECANPAY": "ALL+ACP", "NONE|ANYONECANPAY": "NONE+ACP", "SINGLE|ANYONECANPAY": "SINGLE+ACP"}
obs = [["Flag", "Same-index output edited", "Other output edited", "Other input changed"]] + \
      [[KN[k], "valid" if surv[k][0] == "Y" else "broken", "valid" if surv[k][1] == "Y" else "broken", "valid" if acp[k] == "Y" else "broken"] for k in surv]
assert [r[1:] for r in obs[1:3]] == [["broken", "broken", "broken"], ["valid", "valid", "broken"]]
flags_rows = G["Flags"] + G["CoreFlags"]
page("flags", "A flag chooses what the signature commits to", "Only plain ALL covers other inputs' sequence numbers; ACP means ANYONECANPAY",
     [{"t": "text", "x": 0.5, "y": 1.32, "w": 4.6, "h": 0.25, "fs": 11, "bold": True, "color": "dark", "body": "Computed: which fields change the hash"},
      {"t": "text", "x": 5.2, "y": 1.32, "w": 4.3, "h": 0.25, "fs": 11, "bold": True, "color": "dark", "body": "%s: Core's own signatures, edited here" % REC},
      table(0.5, 1.6, 4.6, [0.95, 0.7, 0.7, 0.8, 0.75, 0.7], pred, fs=8, rowH=[0.4] + [0.19] * 6),
      table(5.2, 1.6, 4.3, [1.15, 1.05, 1.05, 1.05], obs, fs=8, rowH=[0.4] + [0.19] * 6),
      con("Flags", 0.5, 3.62, 9.0, 1.08, "executed: the fields per flag; Recorded: do Core's signatures survive an edit?", fs=9, rows=flags_rows)],
     "Each flag removes fields from the hash, and the left table shows which of five fields change it, found by changing one field at a time. The right table asks the same question of signatures that Bitcoin Core 31.1.0 made on a test network, which are Recorded here and edited and verified again on this machine. The two tables agree, and the book's wording about all inputs holds for outpoints but not for the other inputs' sequence numbers.",
     "NONE signs no outputs, SINGLE one, ALL all; ANYONECANPAY frees other inputs")

page("single", "SIGHASH_SINGLE with no matching output", "The book is silent: the legacy hash becomes the number 1, and Core 31.1 refuses to sign",
     [con("SingleBug", 0.5, 2.05, 6.0, 1.75, "executed on published vectors; the last row is Recorded", fs=10),
      beats(6.7, 1.75, 2.8, 2.5, ["Row 1: the legacy hash when input 1 has no output 1",
                                  "Row 2: it is the 32-byte number one, 01 then 31 zero bytes",
                                  "Row 3: Core's 500 published hash vectors reproduce here",
                                  "Row 4: Core refuses to sign (False), but signs when each input has an output (True)"], fs=10.5),
      {"t": "chips", "x": 0.5, "y": 4.2, "w": 9.0, "h": 0.4, "fs": 10.5, "items": ["legacy hash only", "500 of 500 vectors", "Core 31.1.0 refuses"]}],
     "The book does not say what SIGHASH_SINGLE signs when the input has no output with its index. In the legacy algorithm the value that is signed is then the number one, which the first rows print and which Core's own source marks as a bug. The last row is Recorded: Core 31.1.0 refuses to sign such an input, and signs the same transaction once each input has an output.",
     "SINGLE with no matching output signs the number one; Core refuses it",
     lede="Input 1 of a SINGLE signature has no output 1 to commit to, so the value that is signed is the constant one.")

# ---------------------------------------------------------------------------------------------- part B
E.section("Schnorr signatures", "From a proof of identity to the 64-byte signature of taproot, and what its linearity allows",
          [{"label": "Prove, then sign"}, {"label": "The patent story"}, {"label": "BIP340 in practice"}, {"label": "Keys that add up"}],
          "This part follows Schnorr's idea from a three-move proof of identity to the 64-byte signature that taproot uses. It then shows what the signature's linearity allows, from adding keys to sharing a secret among three people. A story about a patent explains why Bitcoin began with ECDSA instead.")
KEEP["secB"] = "Schnorr signatures"

page("fiat", "From a proof of identity to a signature", "The verifier's random challenge is replaced by a hash of the commitment, key and message",
     [{"t": "flow", "x": 0.5, "y": 1.72, "w": 9.0, "h": 0.7, "fs": 11.5, "steps": [
         {"label": "Commit", "sub": "prover sends kG"}, {"label": "Challenge", "sub": "verifier sends e"}, {"label": "Respond", "sub": "prover sends s = k + e x", "hot": True}]},
      con("Fiat", 0.5, 3.0, 5.6, 1.74, "executed: the toy, the curve, a cheat, a signature"),
      beats(6.3, 2.62, 3.2, 2.2, ["Row 1: toy numbers, s is 40 and sG equals kG + e xG", "Row 2: the round verifies; a response one too large fails",
                                  "Row 3: told the challenge first, a cheat passes without x", "Row 4: a hash for the verifier: the right message verifies, another fails"], fs=10.5)],
     "The prover commits to a nonce, the verifier answers with a random challenge, and the prover responds so that one equation can be checked. The console runs the toy numbers, the real curve round, a response that is wrong by one, and a cheat who is told the challenge in advance and passes without the key. Replacing the verifier by a hash of the commitment, the key and the message gives a signature that verifies for its own message and fails for another.",
     "A schnorr signature is a three-move proof in which a hash plays the verifier",
     lede="Commit, challenge, respond: the verifier checks sG = kG + eX, and a hash can play the verifier.")

story("patent", "SchnorrPatent", "ch08_schnorr.png", None,
      ["On 19 February 1991 the United States publishes patent 4,995,082 for Claus-Peter Schnorr's scheme, filed in 1990",
       "Cryptographers wanted a free alternative and built DSA and ECDSA, the only signature Bitcoin knew until 2021",
       "The term was the greater of 17 years from grant and 20 from filing; Wikipedia says it ended in February 2010"],
      "PatentStory", 2, "executed: both patent end dates, then the years to taproot",
      "On 19 February 1991 the United States published Claus-Peter Schnorr's patent 4,995,082, filed in 1990 for a scheme he had presented at Crypto 89. The patent kept the algorithm out of open standards, so ECDSA became the signature Bitcoin used from its first release until the taproot soft fork. The console computes both possible end dates, 19 February 2008 and 23 February 2010, and Wikipedia states that the patent expired in February 2010.")

page("bip340", "BIP340 in practice: 64 bytes, x-only keys", "Checked against the published vectors; the batch speed-up is NOT EXECUTED",
     [con("Bip340", 0.5, 1.75, 4.9, 2.45, "executed: the published vectors and the format", fs=10),
      beats(5.6, 1.45, 3.9, 2.75, ["Row 1: 19 published vectors; 19 verdicts match, and 8 secret keys reproduce key and signature",
                                   "Row 2: 64 bytes, or 65 with an explicit hash type; both verify",
                                   "Row 3: keys are 32 bytes; the signer negates the key when y is odd",
                                   "Row 4: default signing is deterministic; another aux value still verifies",
                                   "Row 5: without key prefixing a forgery works for P + aG; with it, it fails",
                                   "Row 6: nine valid signatures pass one equation; one swapped fails the batch"], fs=9.5),
      {"t": "text", "x": 0.5, "y": 4.5, "w": 9.0, "h": 0.45, "fs": 11, "bold": True, "color": "orange",
       "body": "NOT EXECUTED: the speed-up of batch verification. The equation is run; the library lists no batch interface, so nothing was timed."}],
     "BIP340 signatures are 64 bytes, public keys are 32 bytes, and the published test vectors all reproduce here. Signing is deterministic by default, and hashing the public key into the challenge stops a related-key forgery that works without it. A combined equation accepts nine valid signatures and rejects the batch when one is swapped, but the claimed speed-up is NOT EXECUTED because the library lists no batch interface.",
     "One equation checks one signature or a batch; the speed-up was not measured")
E.S[-1]["items"][0]["rows"] = [r for r in G["Bip340"] if "tagged_hash" not in r[0]]

PAINT = "Like mixing paints: anyone can add colours, but a partner who sees yours first can choose a colour that hides it."
page("agg", "Keys that add up, and the trap in it", "Adding keys gives one signature for two people; MuSig2 closes the cancellation hole",
     [con("KeyAgg", 0.5, 1.75, 4.5, 2.1, "executed: add keys, cancel a key, MuSig2", fs=10),
      beats(5.2, 1.45, 4.3, 2.45, ["Row 1: signing is linear in the key: additive and homogeneous",
                                   "Row 2: two keys and two responses added give one valid signature",
                                   "Row 3: Bob publishes zG minus yG; the sum is zG and Bob signs alone",
                                   "Row 4: BIP327's four published key aggregation vectors reproduce",
                                   "Row 5: the same attack on MuSig2 keys gives Bob no control"], fs=10),
      foot(0.5, 4.3, 9.0, 0.5, PAINT)],
     "Adding private keys adds public keys, and signing is linear, so two people can make one signature for a sum key. The naive protocol has a hole: a partner who sees your key first can publish a key that cancels it and then sign alone, which the console reproduces. MuSig2 weights each key by a hash, so the same attack no longer gives the attacker the aggregate, and its four published key vectors reproduce.",
     "Plain key addition invites cancellation; MuSig2 hashed weights stop it")

MAP = "Like a treasure map torn in three: any two pieces show the place, one piece shows nothing."
page("thr", "Threshold signatures: any two of three", "Shamir's line through points; no BIP for a threshold scheme has a number yet",
     [{"t": "flow", "x": 0.5, "y": 1.75, "w": 9.0, "h": 0.7, "fs": 11.5, "steps": [
         {"label": "Split", "sub": "a secret on a line, shares at x = 1, 2, 3"}, {"label": "Combine", "sub": "any two shares rebuild the secret"},
         {"label": "Hide", "sub": "one share fits every secret", "hot": True}]},
      con("Threshold", 0.5, 3.1, 5.0, 1.62, "executed: shares, secrecy, a trick, the BIP index", fs=9.5),
      beats(5.7, 2.65, 3.8, 2.2, ["Row 1: all three pairs rebuild 31337",
                                  "Row 2: one share is consistent with every secret",
                                  "Row 3: Bob tells each partner the other is away and collects both partial keys",
                                  "Row 4: the index has no FROST row, one use of the word threshold; Optech lists a FROST BIP"], fs=10)],
     "Shamir's scheme hides a secret as the point where a line crosses an axis, so any two of three shares rebuild it and one share shows nothing. The book's threshold protocol has a weakness that the console reproduces: a partner can tell each of the others that the other is away and collect both partial keys. The BIP index has no number for a threshold scheme, although Optech lists a FROST proposal.",
     "Any two of three shares rebuild the secret, and one share shows nothing",
     lede=MAP)

# ---------------------------------------------------------------------------------------------- part C
E.section("ECDSA, DER and the nonce", "The signature Bitcoin used until 2021: formulas, encoding, a real signature and the number that must never repeat",
          [{"label": "Formulas and low S"}, {"label": "A signature in a block"}, {"label": "Deterministic nonces"}, {"label": "Weak randomness"}],
          "This part is about ECDSA, the signature Bitcoin used until 2021. It covers the formulas, the two forms of one signature, the DER encoding and a real signature from the chain, and then the nonce, which must never repeat. Two stories belong here, one about a signature printed in the book and one about weak random numbers on Android.")
KEEP["secC"] = "ECDSA, DER and the nonce"

page("ecdsa", "ECDSA: the formulas, and two forms of one signature", "(R, s) and (R, n - s) both verify; the low form is the one the relay policy wants",
     [con("EcdsaMath", 0.5, 2.05, 5.5, 1.62, "executed: formulas, the second form, 200 signatures", fs=10),
      beats(6.2, 1.75, 3.3, 2.2, ["Row 1: the formulas verify (True), fail for another hash (False), and R is the x of kG (True)",
                                  "Row 2: the second form verifies too (True), and exactly one form is low (True)",
                                  "Row 3: 200 signatures: all strict DER, all low S; 70 or 71 bytes"], fs=10.5),
      {"t": "chips", "x": 0.5, "y": 3.95, "w": 9.0, "h": 0.5, "fs": 10, "items": ["30 sequence", "45 length", "02 21 R", "02 20 s", "01 SIGHASH_ALL"]},
      foot(0.5, 4.5, 9.0, 0.4, "The pieces of DER, from the book's example: the next slide splits the real bytes.", fs=11)],
     "ECDSA computes s from the hash, the key, the nonce and the point R, and the check recomputes R from s. The console verifies the book's formulas, shows that a second signature with s replaced by n minus s also verifies, and checks that 200 library signatures are low-S and strictly DER encoded. The two forms are the malleability that the low-S rule addresses.",
     "One signature has two valid forms; only the low form passes the relay policy",
     lede="ECDSA signs with s = k^-1 (hash + x R) mod n; replacing s by n - s gives a second valid signature.")

story("booksig", "BookSignature", "ch08_bitcoinlogo.png", "Stand-in picture: the Bitcoin logo, not the sender or the transaction.",
      ["27 December 2013, 23:11:54 UTC: block 277,316 holds the transaction whose signature the book prints",
       "Its 72 bytes split into nine DER elements, and Core's strict-encoding rule accepts them",
       "The legacy hash is recomputed: the signature verifies; with the flag changed to NONE it fails"],
      "BookSignature", 3, "executed on the saved transaction record",
      "The long signature that the book uses to explain DER is a real one, from block 277,316 on 27 December 2013. The console finds it in the saved transaction record, splits it into its nine elements, recomputes the legacy signature hash and verifies it against the 65-byte public key; the same check fails when the flag byte is changed to NONE. Its R value begins with 0x88, so a padding zero makes it 72 bytes, which Bitcoin Core avoids today by grinding for a small R.")
bs = E.S[-1]
bs["items"][2] = dict(E.code("BookSignature", 4.1, 3.15, 5.4, 1.2, fs=9, rows=[G["BookSignature"][1], G["BookSignature"][0], G["BookSignature"][2]]), label="executed on the saved transaction record")

nd_len = OUT("NonceDet", 4)
assert nd_len == {"71": 298, "70": 2} and sum(nd_len.values()) == 300
page("nonce", "Deterministic nonces and small signatures", "RFC 6979 removes the random number; Core also grinds R small",
     [con("NonceDet", 0.5, 1.75, 4.8, 2.25, "executed, and Recorded rows from Core 31.1.0", fs=9.5),
      {"t": "chart", "x": 5.5, "y": 1.4, "w": 4.0, "h": 2.6, "ctype": "bar", "title": "Recorded: 300 signatures by length (bytes)", "dataLabels": True, "dlFmt": "0", "dlFs": 10,
       "labels": ["70 bytes", "71 bytes"], "series": [{"name": "signatures", "data": [nd_len["70"], nd_len["71"]]}]},
      beats(0.5, 4.33, 9.0, 0.62, ["Rows 1 to 3: the standard's published nonce reproduces; one message signs the same way twice; Core does too",
                                   "Rows 4 to 6: unground library signatures are high-R about half the time; all 300 of Core's are low-R"], fs=10)],
     "The nonce can be derived from the key and the message with RFC 6979, so no random number generator is needed at signing time. The console reproduces the standard's published nonce, and the Recorded rows show that Bitcoin Core signs deterministically and grinds the nonce until R is small. All 300 signatures in one Core transaction are low-R, 298 of 71 bytes and 2 of 70, while about half of the library's unground signatures are not.",
     "A nonce derived from key and message needs no random generator")

story("android", "AndroidRandom", "ch08_android.png", "Stand-in picture: the platform, not the incident.",
      ["2013-08-11: Bitcoin.org warns of critical weaknesses in Android's secure random generator; four wallets are named",
       "14 August: Android engineer Alex Klyubin blames improper initialization of the generator",
       "Like a one-time pad used twice: two signatures under one nonce can be subtracted to leave the key"],
      "NonceReuse", 3, "executed: reuse a nonce, use two nonces, check RFC 6979",
      "On 11 August 2013 Bitcoin.org warned that Android's secure random number generator was weak, and four wallets were named. The sources say the generator was improperly initialized but not which flaw was exploited. The console shows why this is fatal for ECDSA: two signatures with one nonce give away the key, while two different nonces do not, and a deterministic nonce removes the dependence on randomness. The picture is the Android robot, a stand-in for the platform.")

# ---------------------------------------------------------------------------------------------- part D
E.section("Segwit, taproot and since the book", "What segwit changed in what is signed, how a node judges a signature, and what moved after print",
          [{"label": "Hashing and amounts"}, {"label": "Policy and consensus"}, {"label": "Taproot hash types"}, {"label": "Since the book"}],
          "This part covers what segwit changed in what is signed, how a node judges a signature and what has moved since the book was printed. It uses the Recorded answers of Bitcoin Core for policy and consensus, and the saved sources for the status of proposals. It closes with a plain list of what this deck did not run.")
KEEP["secD"] = "Segwit, taproot and since the book"

hb = OUT("Hashing", 0)
assert hb == [[10, 5150, 2670], [100, 420500, 25530]] and OUT("Hashing", 1) == [97.8, 10.0]
page("hash", "Segwit hashes less and signs amounts", "Legacy signing re-hashes the transaction per input; BIP143 and BIP341 commit to amounts",
     [con("Hashing", 0.5, 1.75, 4.8, 2.0, "executed: bytes hashed, amounts, a real taproot spend", fs=9.5),
      {"t": "chart", "x": 5.5, "y": 1.4, "w": 4.0, "h": 2.6, "ctype": "bar", "title": "Bytes hashed by all signatures of a transaction", "dataLabels": True, "dlFmt": "#,##0", "dlFs": 9,
       "labels": ["legacy, 10 inputs", "BIP143, 10 inputs", "legacy, 100 inputs", "BIP143, 100 inputs"],
       "series": [{"name": "bytes", "data": [hb[0][1], hb[0][2], hb[1][1], hb[1][2]]}]},
      beats(0.5, 4.1, 9.0, 0.85, ["Rows 1 and 2: ten times the inputs make legacy signing hash 97.8 times the bytes, BIP143 only 10.0 times",
                                  "Rows 3 to 5: a version 0 signature commits to the amount, taproot to all spent amounts unless ANYONECANPAY; block 709,635, saved here, holds the first taproot key-path spend, verified here"], fs=10)],
     "Legacy signing hashes a copy of the transaction for each input, so ten times the inputs cost almost a hundred times the bytes; BIP143 keeps the cost linear. The chart shows 10 and 100 inputs, and the console shows the growth factors, 97.8 and 10.0. A version 0 signature also commits to the amount being spent, and a taproot signature commits to all spent amounts unless ANYONECANPAY is used. Block 709,635 holds the first taproot key-path spend, which verifies here.",
     "Segwit signing cost grows with the inputs, not their square, and covers amounts")

pol = D.__dict__  # not used; the tables below read the executed rows
import sen0401_ch08_claims_v1_0_0 as K  # the same functions the console rows call, used here only to quote Core's own error text in the tables
short = lambda r: (r.split("(", 1)[1].rstrip(")") if r else "accepted")
pv = K.core_policy_verdicts()
assert "".join("Y" if v[0] else "." for v in pv.values()) == OUT("PolicyConsensus", 0) == "Y..."
tv = K.core_taproot_verdicts()
assert "".join("Y" if v[0] else "." for v in tv.values()) == OUT("TaprootTypes", 1) == "YY...."
assert OUT("PolicyConsensus", 1) == [True, False, True] and OUT("PolicyConsensus", 2) == [True, True, True]
pol_tbl = [["Signature variant", "Core's policy answer"]] + [[k.replace("_", " "), short(v[1])] for k, v in pv.items()]
tap_tbl = [["Taproot variant", "Core's answer"]] + [[k.replace("_", " "), short(v[1])] for k, v in tv.items()]
page("policy", "What a node accepts: policy, consensus, taproot", "%s: Core 31.1.0 on regtest. High S is policy; strict DER is consensus" % REC,
     [con("PolicyConsensus", 0.5, 1.7, 4.4, 1.22, "%s: policy, consensus, the two forms" % REC, fs=9.5),
      con("TaprootTypes", 5.1, 1.7, 4.4, 1.22, "%s: hash types and verdicts" % REC, fs=9.5),
      table(0.5, 3.28, 4.4, [1.5, 2.9], pol_tbl, fs=8, rowH=[0.22] * 5),
      table(5.1, 3.28, 4.4, [1.4, 3.0], tap_tbl, fs=8, rowH=[0.22] * 7)],
     "A node can accept a signature in a block that it would not relay. Core 31.1.0 on a test network refuses a high-S signature in its memory pool but mines it into a block, while a signature that is not strictly DER encoded makes the block invalid. For taproot, the explicit hash type byte 0x00 is invalid and the default is the absence of the byte; the tables show Core's own error for each case.",
     "Policy decides what is relayed, consensus what is valid")

page("since", "Since the book: what moved after print", "Status read from the saved BIP index; Core 30.0 and 31.0; libsecp256k1 0.8.0",
     [{"t": "chart", "x": 0.45, "y": 1.35, "w": 3.8, "h": 1.75, "ctype": "bar", "title": "BIPs of this chapter by status", "dataLabels": True, "dlFmt": "0", "dlFs": 10,
       "labels": ["Deployed", "Draft", "Complete", "Closed"], "series": [{"name": "BIPs", "data": [6, 4, 2, 1]}]},
      beats(4.5, 1.35, 5.0, 1.75, ["Core 30.0 caps legacy signature operations at 2,500 in policy; BIP54, Complete, would make it a rule",
                                   "MuSig2 is Deployed; Core supports the musig() descriptor from 30.0 and signing from 31.0",
                                   "BIP118 is still Draft, as are BIP461 and BIP361; libsecp256k1 0.8.0 renamed schnorrsig_sign",
                                   "NOT EXECUTED: ECDSA's full security proof, quantum attacks, any Core release but 31.1.0"], fs=9.5),
      con("SinceBook", 0.5, 3.44, 9.0, 1.28, "executed on the saved sources: BIP status, Core support, limits", fs=9)],
     "The book is a snapshot of 2023. Most of the proposals it names are Deployed, but BIP118 is still a Draft, BIP461 and BIP361 are new drafts, and Core 30.0 caps legacy signature operations at 2,500 in policy. Several things were not run here and are marked NOT EXECUTED on the slide: the security proof of ECDSA, quantum attacks and any Core release other than 31.1.0.",
     "The book is a snapshot; check the BIP index and Core's notes for changes")
cnt = OUT("SinceBook", 0)
assert [cnt[k] for k in ("Deployed", "Draft", "Complete", "Closed")] == [6, 4, 2, 1]

# ---------------------------------------------------------------------------------------------- summary, resources, closing
page("summary", "The chapter in five lines", "One line per part, each one provable from its slides",
     [{"t": "numlist", "x": 0.5, "y": 1.45, "w": 9.0, "h": 3.4, "fs": 12.5, "items": [
         "A signature is checked from a message, a public key and the signature itself, and its scalars live modulo n, not p",
         "A SIGHASH flag chooses what is signed, and SINGLE with no matching output signs the number one",
         "Schnorr turns a three-move proof into a 64-byte signature; linearity gives MuSig2 and threshold schemes, and key prefixing blocks related-key forgery",
         "ECDSA signatures have two forms, travel in DER and are only as safe as their nonce: reuse leaks the key, RFC 6979 removes the risk",
         "Segwit made signing linear and amount-aware; consensus bans bad DER, policy bans high S, and the status of proposals has moved since print"]}],
     "These five lines are the deck in miniature. Each can be traced to a part of the route on slide 2 and to computations that ran on its slides. A line that feels unproven should send the reader back to that part's consoles.",
     "If a line feels unproven, its part's consoles carry the receipt")

page("resources", "Where to go from here", "Opened on %s; every entry is a live link in this file" % D.DATE,
     [{"t": "links", "x": 0.5, "y": 1.5, "w": 9.0, "h": 3.45, "fs": 10, "groups": [
         {"head": "Read", "rows": [
             ["BIP 340, schnorr signatures", "https://bips.dev/340/"],
             ["Mastering Bitcoin, the book", "https://aantonop.com/books/mastering-bitcoin/"],
             ["Bitcoin Wiki, OP_CHECKSIG", "https://en.bitcoin.it/wiki/OP_CHECKSIG"]]},
         {"head": "Standards and papers", "rows": [
             ["BIP 327, MuSig2", "https://bips.dev/327/"],
             ["RFC 6979, deterministic nonces", "https://www.rfc-editor.org/rfc/rfc6979.txt"],
             ["Schnorr, 1991, the seminal paper", "https://link.springer.com/article/10.1007/BF00196725"]]},
         {"head": "Watch", "rows": [
             ["MIT OCW 15.S12, Blockchain and Money", "https://ocw.mit.edu/courses/15-s12-blockchain-and-money-fall-2018/"],
             ["Optech Schnorr Taproot workshop videos", "https://bitcoinops.org/en/schnorr-taproot-workshop/"]]},
         {"head": "Community", "rows": [
             ["Bitcoin Optech newsletters", "https://bitcoinops.org/en/newsletters/"],
             ["Delving Bitcoin, research forum", "https://delvingbitcoin.org/"],
             ["The bitcoin-dev group", "https://groups.google.com/g/bitcoindev"]]}]}],
     "Everything here is free to read or watch, and every link was opened on %s. A good start is the Optech workshop videos on schnorr and MuSig, then BIP340 read next to the chapter. The research package for chapter 8 lists all %d sources with the passages used." % (D.DATE, NPUB),
     "Watch the Optech workshop, then read BIP340 beside the chapter")

E.slide("closing", "What you should now be able to say", "And where each claim gets its proof",
        [{"t": "bullets", "x": 0.6, "y": 3.05, "w": 8.8, "h": 1.65, "fs": 16, "dark": True, "items": [
            "What a signature needs to be checked, and why scalars are modulo n",
            "What each SIGHASH flag commits to, and what SINGLE does with no match",
            "How schnorr, MuSig2 and ECDSA signatures are made, and why the nonce matters",
            "What a node accepts as policy and as consensus, and what moved since print"]}],
        "Four claims, each carried by computations that ran on slides of this deck. A reader who can say them and point to the slide that proves them has the chapter. The research package for chapter 8 holds the sources and the test vectors behind them.", bg="dark")

# ---------------------------------------------------------------------------------------------- agenda and plan meta
E.agenda(["The chapter's questions", "What a signature proves and signs", "Schnorr: proof, BIP340, MuSig2, threshold",
          "ECDSA: encoding, nonces, Android", "Segwit, taproot, policy, what moved since print"],
         "The route has four parts after the questions: what a signature proves and signs, schnorr signatures, ECDSA with its encoding and its nonce, and finally segwit, taproot and what moved since the book. Each part ends in a story or a correction of the book that a reader can check on the slide. The numbers in the list let a reader jump straight to a part.",
         "Four parts, three true stories, and a list of what was not run")
E.finish("Chapter 8: Digital Signatures", "1.0.0", "2026-10-15, first deck from the committed research package (commit 4102ded), to the CME look and feel; notes are short reader's prose")

# plan meta: honesty and analogies, with slide numbers found by title
planp = os.path.join(HERE, "deck_plan_v1_0_0.json")
plan = json.load(open(planp))
num = {k: [i + 1 for i, s in enumerate(plan["slides"]) if s["title"] == t][0] for k, t in KEEP.items()}
plan["meta"]["notes"] = "short reader's prose: 2-4 sentences, at most 100 words"
plan["meta"]["honesty"] = {
    "title": ["Bitcoin Core 31.1.0", REC],
    "recorded": [1, num["flags"], num["single"], num["nonce"], num["policy"]],
    "notExecuted": [num["bip340"], num["since"]],
    "standin": {str(num["booksig"]): ["Stand-in picture"], str(num["android"]): ["Stand-in picture"]},
    "vectors": [num["single"], num["bip340"], num["agg"], num["booksig"], num["nonce"], num["hash"], num["since"]],
}
plan["meta"]["analogies"] = [
    {"concept": "digital signature", "analogy": WAX, "slide": num["sign"]},
    {"concept": "modulus", "analogy": CLOCK, "slide": num["moduli"]},
    {"concept": "SIGHASH flags", "analogy": "Think of a cheque: ALL fills in every line, NONE leaves the payee blank.", "slide": num["secA"]},
    {"concept": "key aggregation", "analogy": PAINT, "slide": num["agg"]},
    {"concept": "Shamir sharing", "analogy": MAP, "slide": num["thr"]},
    {"concept": "nonce reuse", "analogy": "Like a one-time pad used twice: two signatures under one nonce can be subtracted to leave the key", "slide": num["android"]},
]
json.dump(plan, open(planp, "w"), indent=1)
print("meta: honesty and %d analogies written; slide numbers %s" % (len(plan["meta"]["analogies"]), num))
