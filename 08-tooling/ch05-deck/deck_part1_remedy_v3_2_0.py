#!/usr/bin/env python3
"""Chapter 5 deck v3.2.0 - opening and part 1 (keys in wallets), part 2 (recovery codes). Slide order is the file order."""
__version__ = "3.2.0"
import ast
from deck_types_remedy_v3_2_0 import *

NS = {}
exec("import hashlib\n" + X.PRELUDE, NS)          # the sample data names (WORDS, ENT, TV, ...) for the result visuals
FIG = "Figure: Mastering Bitcoin 3e, CC BY-SA 4.0"
PARTS = []                                          # (title, first slide index) recorded by dividers


def part(title):
    PARTS.append((title, len(SLIDES) + 1))


def L(out, i=None):
    ls = [l for l in out.splitlines() if l.strip()]
    return ls if i is None else ls[i]


def branch_counts():
    byname = {n[0]: n for n in CORPUS.NODES}
    root = lambda n: n if n[2] == 1 else root(byname[n[3]])
    counts = {}
    for n in CORPUS.NODES:
        r = root(n)
        counts[r[0]] = counts.get(r[0], 0) + (0 if n[2] == 1 else 1)
    return [(byname[k][1], v) for k, v in counts.items()]


# ------------------------------------------------------------------ 1 title
title_slide("Chapter 5: Wallet Recovery", "One seed, twelve words, and every key you will ever need back",
            "SEN0401 Special Topics in Software Engineering: Block Chain  -  Fall 2026  -  Yusuf Altunel, PhD  -  Istanbul Kultur University",
            "mbc3_0504.png", FIG,
            "Welcome to chapter five. A wallet is not a bag of coins but a bag of keys, and keys can be lost. Today we learn how one seed, written as twelve words, brings every key back.",
            "Wallet Recovery")

# 2 the route slide is created here (slide file 2) and filled by the builder once every slide number is known
ROUTE = new_slide("Today's route", "Seven parts; every number is a slide you can jump to", "Wallet Recovery",
                  "Today has seven parts, and every part opens with a divider. The numbers are slide numbers, so you can jump back to any part. The code slides are numbered in order and match the course page.")

# ------------------------------------------------------------------ 3 questions
s = new_slide("The questions this chapter answers", "Seven questions; each one is answered by a part of the deck", "Wallet Recovery",
              "These seven questions are the chapter's own competency questions. If you can answer them at the end, you own the chapter. Keep them in mind as we move through the parts.")
qs = ["What does a Bitcoin wallet actually contain?", "How does a recovery code turn into a seed?", "How does one seed make a whole tree of keys?",
      "Which recovery code schemes are in use?", "Which derivation paths does a wallet use?", "Where does the book differ from the standards?",
      "What must you back up, and how do you test it?"]
for i, q in enumerate(qs):
    y = 1.3 + i * 0.5
    box_text(s, 0.5, y, 0.5, 0.42, str(i + 1), 15, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="question number", font=HF)
    box_text(s, 1.1, y, 8.4, 0.42, q, 15, C["ink"], C["card"], name="question")
takeaway(s, "If you can answer these seven, chapter 5 is yours.")

# ------------------------------------------------------------------ 4 map (native chart)
s = new_slide("One chapter, eight branches", "How many concepts the course page explains in each branch", "A Wallet Technology Stack in Detail",
              "The chapter is a tree of eight branches. The bars count the concepts in each branch of the course ontology. Today we walk the spine: keys, codes, the BIP39 stack, the HD tree, paths, non-key data and deployment.")
bc = branch_counts()
chart(s, XL_CHART_TYPE.BAR_CLUSTERED, [b for b, _ in bc][::-1], [("Concepts", [v for _, v in bc][::-1])], 0.4, 1.25, 6.0, 3.55,
      numfmt="0", name="concept count chart", fs=11, gap=40)
card(s, 6.6, 1.3, 2.9, 3.4, C["card"], "reading guide")
tb(s, 6.75, 1.38, 2.6, 0.3, "How to read the deck", 14, C["orange"], bold=True, font=HF, name="guide heading")
tb(s, 6.75, 1.78, 2.65, 2.85, ["Seven parts follow the branches.", "Every part opens with a divider.", "Code slides show the code, a note beside it, and the result."],
   12.5, C["ink"], name="guide text")
takeaway(s, "Today's spine: keys, codes, the tree, paths, backups.")

# ------------------------------------------------------------------ 5 story: IronKey
story_slide("IronKey", [
    "Stefan Thomas, programmer and former Ripple technology chief; reporter Nathaniel Popper, New York Times.",
    "Locked out of an IronKey drive that holds the keys to 7,002 BTC; eight of ten password guesses used.",
    ("2021-01-12", " - the story ran; the 7,002 BTC was paid in 2011."),
    "An IronKey USB drive in a safe, and the front page of the New York Times.",
    "The password was on a paper he lost; memory was his only backup.",
    "The drive locks forever after ten wrong guesses. A tested recovery code is the alternative."],
    "Stefan Thomas was paid 7,002 bitcoin in 2011 and locked the keys on an encrypted drive. He lost the password and has two guesses left. This chapter is the discipline that makes the story impossible to repeat.")

# ------------------------------------------------------------------ 6 library and sample data
s = new_slide("The tools we run today", "One small Python library, written for reading", "Wallet Recovery",
              "Every code slide uses the same small chapter library, written for reading and checked against the standards' test vectors. It is not for real money. The sample data names on the right are reused on every slide.")
table(s, 0.4, 1.3, 5.2, [["Function", "What it does"],
                         ["entropy_to_mnemonic", "random bits to recovery words"],
                         ["mnemonic_to_seed", "words to a 512-bit seed"],
                         ["master, ckd_priv, ckd_pub", "seed to master key, parent to child"],
                         ["keys_at", "a key at a path below a code"],
                         ["p2wpkh_address", "a public key to a bc1q address"],
                         ["descsum_create", "a descriptor checksum"],
                         ["shamir_split, scan_with_gap", "split a secret, scan addresses"]], [2.3, 2.9], 11, 0.4, name="library table")
table(s, 5.8, 1.3, 3.8, [["Name", "Sample data"],
                         ["ENT, WORDS", "the book's 128 bits and its 12 words"],
                         ["TV", "BIP32 test seed"],
                         ["B84", "BIP84 test recovery code"],
                         ["DESC", "a descriptor Core made"],
                         ["BOOK_XPUB", "the book's extended public key"]], [1.4, 2.4], 11, 0.4, name="sample data table")
takeaway(s, "Same library, same data, every code slide: only the idea changes.")

# =============================================================== PART 1: keys in wallets
part("Keys in wallets")
divider("Part 1: Keys in wallets", "From a bag of keys to one recoverable seed",
        [("wallet database", "the file where a wallet keeps its keys and notes"),
         ("independent key generation", "every key made alone, so every key needs a backup"),
         ("deterministic key generation", "every key follows from one seed by a rule"),
         ("seed", "the one secret all the keys come from"),
         ("key tweak", "a number added to a key to make a related key"),
         ("hardware signing device", "a small computer that signs and never shows its keys")],
        ["Seed", "A rule", "Key 0", "Key 1", "Key 2"],
        "Part one asks what a wallet really holds and why one seed beats a bag of keys. Six concepts open the part. The picture shows the idea: one seed and a rule give every key.",
        "Independent Key Generation", hot=(0,))

s = new_slide("What a wallet really holds", "A wallet application, its database, and who signs", "A Wallet Technology Stack in Detail",
              "A wallet database mostly holds keys. Some databases hold only public keys, so the application can watch funds but not spend them. Then an external signer, such as a hardware signing device, makes the signature.")
flow(s, 0.5, 1.3, 9.0, 0.75, ["Wallet application prepares a payment", "Wallet database supplies the keys", "Signing device signs", "Network receives it"], name="visual: who does what", hot=(2,), size=12)
cards(s, [("Wallet database", "The file where a wallet application keeps its keys and its notes."),
          ("Wallet with public keys only", "It can see funds sent to its keys and show them, but it cannot spend."),
          ("External signing", "One program prepares the transaction; another program or device signs it."),
          ("Hardware signing device", "A small computer that holds private keys and signs without revealing them.")],
      0.5, 2.25, 9.0, 2.5, cols=2, fs=12.5)
takeaway(s, "Keys are the wallet; everything else can be rebuilt from them.")

s = new_slide("Three ways to make keys", "Loose, deterministic, hierarchical", "Hierarchical Deterministic (HD) Key Generation (BIP32)",
              "Independent keys are made one by one and each needs its own backup. A deterministic wallet derives every key from one seed. A hierarchical wallet adds a tree, so one seed also gives organised branches. A key tweak is the small step between keys.")
picture(s, "mbc3_0502.png", 0.4, 1.3, 4.3, 2.9, FIG)
picture(s, "mbc3_0503.png", 5.0, 1.3, 4.4, 2.9, FIG)
tb(s, 0.4, 4.52, 4.3, 0.3, "Deterministic: one seed, keys k0 to kn", 12, C["slate"], bold=True, name="figure label", align=PP_ALIGN.CENTER)
tb(s, 5.0, 4.52, 4.4, 0.3, "Hierarchical: a tree of keys below the seed", 12, C["slate"], bold=True, name="figure label", align=PP_ALIGN.CENTER)
takeaway(s, "Independent keys: a backup for each. Seed-based keys: one backup.", 4.86)

analogy_slide("Everyday pictures for part 1", "A key ring, a recipe and a notary",
              [("wallet database", "A key ring in a drawer, with a notebook beside it", "The file that stores a wallet's keys and notes"),
               ("independent key generation", "Cutting a new, unrelated key for every door", "Each key is made alone, so each needs its own backup"),
               ("deterministic key generation", "A recipe: the same ingredients give the same dish", "One seed and a rule always give the same keys"),
               ("seed", "The master recipe card kept in a safe", "The one secret every key comes from"),
               ("key tweak", "A copy of a key filed down by a fixed amount", "A number added to a key to make a related key"),
               ("hardware signing device", "A notary who stamps letters and never hands over the stamp", "A device that signs and never reveals its keys"),
               ("Wallet Recovery", "Getting back into a locked house with a spare key", "Chapter 5: how a wallet is restored after a loss"),
               ("A Wallet Technology Stack in Detail", "A workshop manual showing every layer of a machine", "The layers: keys, codes, paths, backups")],
              "Each term gets one everyday picture. The recipe is the best one: ingredients are the seed, the recipe is the rule, and the dish is a key. Say the picture first, then the wallet meaning.",
              "A Wallet Technology Stack in Detail", "A seed is a recipe: keep the card, and you can cook every key again.")

code_slide("loose_vs_seed", "Code 1: Loose keys versus one seed", "Deterministic key generation, run", "Deterministic Key Generation",
           "Here is deterministic generation in four lines. One secret and a rule give key number i. Asking again gives the same keys, which is why one backup of the seed is enough.",
           lambda s, out, y, h: (
               table(s, 0.4, y, 5.4, [["Key number", "First 8 characters"]] + [[str(i), k] for i, k in enumerate(ast.literal_eval(L(out, 0)))] + [["Same keys on a second run", L(out, 1)]],
                     [2.6, 2.8], 12, min(0.3, h / 5), name="result table"),
               flow(s, 6.1, y, 3.4, min(0.9, h), ["1 seed to back up", "all keys follow"], name="visual: one backup", hot=(0,), size=12)),
           "One seed, one backup, every key.")

# =============================================================== PART 2: recovery codes
part("Recovery codes")
divider("Part 2: Recovery codes", "Seeds written down so a human can keep them",
        [("recovery code", "words or characters that stand for the seed"),
         ("BIP39", "words from a list of 2,048, with a checksum"),
         ("Electrum v2, Aezeed, Muun", "rival schemes with versions, dates or encryption"),
         ("SLIP39 and codex32", "one secret split into shares you can recombine"),
         ("recovery code passphrase", "an extra secret that changes the wallet"),
         ("brainwallet", "words you chose yourself: not a recovery code")],
        ["Entropy", "Recovery code", "Written on paper", "Restored later"],
        "Part two is about recovery codes. A code is the seed written for human hands. The book names several schemes and one important choice: the passphrase.",
        "Seeds and Recovery Codes", hot=(1,))

s = new_slide("Six recovery code schemes", "What each one adds", "Seeds and Recovery Codes",
              "BIP39 is the common scheme, and Electrum version two avoids a global word list. Aezeed adds versions and a wallet birthday, and Muun uses a non-word code. SLIP39 splits a seed into shares. Codex32 can be made by hand.")
table(s, 0.4, 1.3, 9.2, [["Scheme", "What it adds", "Source"],
                         ["BIP39 recovery code", "Words from a list of 2,048, a checksum, an optional passphrase", "BIP39 standard"],
                         ["Electrum version 2 recovery code", "No global word list; a version number inside the code", "Electrum wallet 2.0+"],
                         ["Aezeed cipher seed", "Two version numbers and a wallet birthday", "lnd wallet"],
                         ["Muun recovery code", "A non-word code that decrypts the keys in a separate document", "Muun wallet"],
                         ["SLIP39 share set", "One seed split into several codes, for example five made, three needed", "SLIP-0039"],
                         ["codex32 recovery code", "Shares made and checked by hand with paper and a pen", "BIP93 (draft)"]],
      [2.6, 5.0, 1.6], 11.5, 0.5, name="scheme table", bold_first=True)
takeaway(s, "Same goal, different trade-offs: reliability, privacy, splitting.")

s = new_slide("Why words, and what can go wrong", "Memory, imitation and coercion", "Recovery Code Passphrases",
              "Words were chosen so a code is easy to remember, but the book urges writing it down. A brainwallet is a phrase you invented, which is not random. Coercion is real: the list of attacks has grown, so the book's count is a floor.")
cards(s, [("Memorising a recovery code", "Words make a code easy to remember, yet the book strongly urges writing it down."),
          ("Brainwallet", "Words you chose yourself. A recovery code is random and made by the wallet."),
          ("Coercion and physical risk", "Someone who thinks you remember a code may force you. The book cites over 100 attacks; the 2026 copy of the list has 364 rows."),
          ("Wallet birthday", "A date stored in the code, so a restore need not scan the whole blockchain.")],
      0.5, 1.3, 9.0, 3.45, cols=2, fs=13)
takeaway(s, "Write it down, make it random, and do not depend on memory.")

analogy_slide("Everyday pictures for part 2, schemes", "Notes, dictionaries and torn maps",
              [("recovery code", "A spare-key note you can write by hand", "Words that stand for the seed"),
               ("BIP39", "A shared dictionary of 2,048 numbered words", "The most common recovery code scheme"),
               ("Electrum v2", "A notebook that stamps its own version", "No global list; a version inside the code"),
               ("Aezeed", "A sealed letter carrying its own date", "Versions and a wallet birthday"),
               ("Muun", "A safe-deposit key opened with a paper from the bank", "A code that decrypts a separate document"),
               ("SLIP39", "A map torn in five: any three pieces show the treasure", "Shares of one seed with a threshold"),
               ("Codex32", "A crossword you can check by hand", "Shares and checksums made with paper and a pen")],
              "Seven schemes, seven pictures. The torn map is the key image for SLIP39: three of five pieces reveal the treasure and two reveal nothing.",
              "Seeds and Recovery Codes", "Seven schemes, seven pictures; the torn map is the one to remember.")

analogy_slide("Everyday pictures for part 2, choices", "A second lock, a decoy and a date",
              [("recovery code passphrase", "A second lock on the safe", "An extra secret mixed into the seed"),
               ("plausible deniability", "A decoy purse with a little cash", "A wallet that looks genuine and holds little"),
               ("duress wallet", "The purse you hand over under threat", "A decoy wallet opened by another passphrase"),
               ("brainwallet", "A password you invented, not a random one", "Words you chose yourself: easy to guess"),
               ("wallet birthday", "The date the safe was bought", "The creation date stored in the code"),
               ("Seeds and Recovery Codes", "A master recipe written on a card", "Writing the seed as words a person can keep"),
               ("Recovery Code Passphrases", "A second lock on the recipe box", "Adding a secret word to the recovery code")],
              "The passphrase is a second lock: lose it and the first lock is not enough. A decoy purse is how plausible deniability works. A brainwallet is the weak opposite of a random code.",
              "Recovery Code Passphrases", "A passphrase is a second lock: lose it, and the words alone open nothing.")

code_slide("other_schemes", "Code 2: Codes check themselves differently", "codex32 and Electrum, run", "Seeds and Recovery Codes",
           "Different schemes protect against typos in different ways. codex32 uses a long checksum that can be checked by hand. Electrum marks a seed with a version that is a prefix of an HMAC.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Scheme", "How it checks itself", "What the run printed"],
                                                       ["codex32", "A checksum over the whole string", "valid: " + L(out, 0)],
                                                       ["Electrum v2", "Version = the first digits of an HMAC", "seed number %s starts with %s" % tuple(L(out, 1).split())],
                                                       ["BIP39", "Checksum bits taken from SHA-256", "see the checksum slide"]],
                                     [1.8, 4.2, 3.2], 12, min(0.34, h / 4), name="result table"),
           "Every scheme has its own safety net.")

code_slide("shamir", "Code 3: Three of five shares recover the secret", "SLIP39's idea, run on a small model", "Seeds and Recovery Codes",
           "Secret sharing splits one secret into shares. Any three of five rebuild it; two reveal nothing. This is a small model, not SLIP39 itself, which works in a different field.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Shares used", "Which ones", "Secret recovered?"],
                                                       ["3 of 5", "shares 1, 2, 3", L(out, 0)], ["3 of 5", "shares 2, 3, 4", L(out, 1)], ["2 of 5", "shares 1, 2", L(out, 2)]],
                                     [2.2, 3.5, 3.5], 12, min(0.34, h / 4), name="result table"),
           "Any three recover; two learn nothing.")
