#!/usr/bin/env python3
"""Chapter 5 deck v3.1.0 - part 3 (the BIP39 stack) and part 4 (the HD wallet)."""
__version__ = "3.1.0"
from deck_part1_remedy_v3_1_0 import *

# =============================================================== PART 3: the BIP39 stack
part("The BIP39 stack")
divider("Part 3: The BIP39 stack", "Entropy in, twelve words out, then a seed",
        [("entropy", "the random bits the code is made from"),
         ("checksum", "a few bits that reveal a typo"),
         ("word list", "2,048 numbered words everyone shares"),
         ("key-stretching function", "repeated work that makes guessing slow"),
         ("PBKDF2 and salt", "the stretcher BIP39 uses, and its added string"),
         ("root seed", "the 512-bit result that starts the tree")],
        ["Entropy", "Checksum added", "Eleven-bit pieces", "Words", "PBKDF2 stretch", "512-bit seed"],
        "Part three follows BIP39 from random bits to a seed. First the code is generated: entropy, checksum, eleven-bit pieces, words. Then the code is stretched into a seed.",
        "BIP39 Recovery Codes", hot=(5,))

story_slide("Bip39Birth", [
    "Marek Palatinus and Pavol Rusnak (SatoshiLabs, makers of Trezor), with Aaron Voisine and Sean Bowe.",
    "BIP 39: a way to write entropy as ordinary words.",
    ("2013-09-10", " - BIP 39 was created."),
    "In the public bips repository on GitHub.",
    "Nobody transcribes 128 raw bits correctly.",
    "2,048 words of eleven bits each, a checksum folded in, and key stretching from words to seed."],
    "The team behind the first hardware signing device faced a human problem: nobody copies 128 bits without errors. Their answer, BIP 39, is the standard we run on the next slides.")

s = new_slide("Generating a recovery code", "Five steps from random bits to words", "Generating a recovery code",
              "Step one, generate entropy. Step two, hash it with SHA-256. Step three, append the first bits as a checksum. Step four, cut the result into eleven-bit pieces. Step five, look each piece up in the word list.")
g = group(s, "visual: 132 bits become 12 words")
gbox(g, 0.4, 1.35, 3.3, 0.55, "Entropy: 128 bits", 12, C["orange"], C["white"], True)
gbox(g, 3.75, 1.35, 0.6, 0.55, "4", 12, C["slate"], C["white"], True)
tb(s, 0.4, 1.93, 4.0, 0.28, "128 bits of entropy + a 4-bit checksum = 132 bits", 11, C["mute"], italic=True, name="figure label")
for i in range(12):
    r, c = divmod(i, 4)
    gbox(g, 0.4 + c * 1.02, 2.4 + r * 0.72, 0.94, 0.6, "11 bits\nword %d" % (i + 1), 10.5)
tb(s, 0.4, 4.52, 4.0, 0.3, "Twelve pieces of eleven bits, one word each", 11, C["slate"], bold=True, name="figure label")
steps = ["1  Generate entropy (128 bits for 12 words)", "2  Hash it with SHA-256", "3  Append the first 4 bits as the checksum",
         "4  Split the 132 bits into 12 pieces of 11 bits", "5  Look each piece up in the word list of 2,048"]
for i, t in enumerate(steps):
    box_text(s, 4.8, 1.3 + i * 0.66, 4.7, 0.58, t, 13, C["ink"], C["card"], name="step")
takeaway(s, "12 words x 11 bits = 132 bits = 128 of entropy + 4 of checksum.", 4.9)

code_slide("hash_avalanche", "Code 4: A hash function changes half its bits", "SHA-256, the tool inside BIP39", "BIP39 Recovery Codes",
           "A hash function turns any input into a fixed-size fingerprint. SHA-256 is one. Change a single letter and about half of the 256 output bits flip, so no output hints at its input.",
           lambda s, out, y, h: (
               chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, ["Bits that changed", "Bits unchanged"],
                     [("bits", [int(L(out, 0).split()[1]), int(L(out, 0).split()[0]) - int(L(out, 0).split()[1])])], 0.4, y, 5.0, h, numfmt="0", name="result chart", fs=11),
               box_text(s, 5.7, y + 0.1, 3.8, min(1.2, h - 0.2), "Two inputs differ by one letter; the outputs differ in %s of %s bits." % (L(out, 0).split()[1], L(out, 0).split()[0]), 13, C["ink"], C["card"], name="reading")),
           "A tiny change makes a huge difference.")

code_slide("entropy_sizes", "Code 5: How many words for how much entropy", "Code length and security strength", "How Much Entropy Do You Need?",
           "BIP39 allows five entropy sizes. More entropy means more words and more security strength. The checksum grows with it: one bit per 32 bits of entropy.",
           lambda s, out, y, h: (
               chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, ["%s bits" % a.split()[0] for a in L(out)], [("Words", [int(a.split()[1]) for a in L(out)])],
                     0.4, y, 6.0, h, numfmt="0", name="result chart", fs=11, axis_title="words"),
               box_text(s, 6.7, y + 0.1, 2.8, min(1.4, h - 0.2), "128 bits is 12 words; each extra 32 bits adds 3 words.", 13, C["ink"], C["card"], name="reading")),
           "More bits, more words, more security strength.")

def _words_table(s, out, y, h):
    words = NS["WORDS"].split()
    idx = ast.literal_eval(L(out, 1))
    rows = [["word"] + words[:6], ["position"] + [str(i) for i in idx[:6]], ["word"] + words[6:], ["position"] + [str(i) for i in idx[6:]]]
    table(s, 0.4, y, 9.2, rows, [1.2] + [1.3] * 6, 11.5, min(0.3, (h - 0.35) / 4), header=False, name="result table", bold_first=True)
    tb(s, 0.4, y + min(0.3, (h - 0.35) / 4) * 4 + 0.04, 9.2, 0.3, "Word number 1 is position %s: the eleven bits %s." % (idx[0], L(out, 2).split()[0]), 12, C["slate"], bold=True, name="reading")

code_slide("entropy_to_words", "Code 6: From entropy to twelve words", "Eleven-bit segments and the word list", "Generating a recovery code",
           "Each eleven-bit segment is a position in the BIP39 word list, 0 to 2047. The book's 128 bits of entropy become exactly the book's twelve words.",
           _words_table, "Every word is just an eleven-bit number.")

code_slide("checksum", "Code 7: The checksum catches a wrong word", "BIP39 checksum", "Generating a recovery code",
           "The last bits of a recovery code are a checksum of the entropy. Decoding recomputes it. Change one word and the check fails, so most typos are caught.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Recovery code", "Entropy decoded", "Checksum ok?"],
                                                       ["army van ... media make crunch", L(out, 0).split()[0], L(out, 0).split()[1]],
                                                       ["army van ... media make army (last word changed)", "not trusted", L(out, 1)]],
                                     [4.0, 3.6, 1.6], 12, min(0.36, h / 3), name="result table", mono_cols=(1,)),
           "A checksum turns a silent typo into a loud error.")

code_slide("normalisation", "Code 8: Text is normalised before stretching", "Text normalisation", "From recovery code to seed",
           "Computers can store the same letter in different ways. BIP39 first normalises the text, so a phrase gives one seed on every device and in every language setting.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Spelling of the word", "Characters", "Same seed?"],
                                                       ["as typed: e-acute is one character", L(out, 0).split()[0], "-"],
                                                       ["after normalising: e plus an accent", L(out, 0).split()[1], L(out, 1)]],
                                     [4.6, 2.0, 2.6], 12, min(0.36, h / 3), name="result table"),
           "Normalise first, so one phrase gives one seed.")

code_slide("pbkdf2_salt", "Code 9: PBKDF2 stretches the words with a salt", "Key-stretching, salt and the root seed", "From recovery code to seed",
           "A key-stretching function repeats work so each guess is slow for an attacker. BIP39 uses PBKDF2 with 2048 rounds and the word mnemonic as the salt. A different salt or round count gives an unrelated result.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Rounds", "Salt", "First 12 hex digits of the result"],
                                                       ["1", "mnemonic", L(out, 0)], ["2048 (BIP39)", "mnemonic", L(out, 1)], ["2048", "mnemonic1", L(out, 2)]],
                                     [2.0, 2.4, 4.8], 12, min(0.34, h / 4), name="result table", mono_cols=(2,)),
           "Slow on purpose: 2048 rounds make every guess costly.")

code_slide("passphrase_wallets", "Code 10: A passphrase opens a different wallet", "Optional passphrase in BIP39", "Optional passphrase in BIP39",
           "The passphrase is part of the salt. The same twelve words with another passphrase give a completely different wallet. That makes a decoy wallet possible, and it also means a forgotten passphrase loses the funds.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Passphrase", "First address of the wallet"],
                                                       ["(none)", L(out, 0)], ["SuperDuperSecret", L(out, 1)]],
                                     [2.6, 6.6], 12, min(0.36, h / 3), name="result table", mono_cols=(1,)),
           "A passphrase is a second secret to back up.")

analogy_slide("Everyday pictures for part 3", "Shuffling, check digits and kneading",
              [("entropy", "A deck shuffled so well nobody can guess it", "The random bits a code is made from"),
               ("checksum", "The check digit on a bank card number", "Bits that reveal a typo"),
               ("word list", "A numbered dictionary everyone shares", "2,048 words for eleven bits each"),
               ("key-stretching function", "Kneading dough again and again", "Repeated hashing that makes guessing slow"),
               ("PBKDF2", "A kneading machine set to 2,048 turns", "The stretcher BIP39 uses with HMAC-SHA512"),
               ("salt", "A pinch of spice that makes each dish unique", "A string that separates equal inputs"),
               ("root seed", "The first seed from which the garden grows", "The 512-bit seed that starts the tree")],
              "Entropy is the shuffled deck, the checksum the check digit, the word list the dictionary. Stretching is kneading: it takes effort, and effort is what slows an attacker.",
              "From recovery code to seed", "Shuffle, tag, name, knead: that is a recovery code.")

analogy_slide("Everyday pictures for part 3, the book's sections", "Padlocks, cards and dough",
              [("BIP39 Recovery Codes", "The shared dictionary and its spelling rules", "The standard that turns bits into words"),
               ("Generating a recovery code", "Shuffle the deck, then write the card order down", "Entropy, checksum, eleven-bit pieces, words"),
               ("From recovery code to seed", "Kneading the written card into dough", "Stretching the words into a 512-bit seed"),
               ("How Much Entropy Do You Need?", "How long a padlock combination should be", "128 to 256 bits: 12 to 24 words"),
               ("Optional passphrase in BIP39", "A second combination on the same padlock", "The passphrase mixed into the salt")],
              "Each section of the book gets a picture too. The padlock is the one to keep: more entropy is a longer combination, and a passphrase is a second combination on the same lock.",
              "BIP39 Recovery Codes")

# =============================================================== PART 4: the HD wallet
part("The HD wallet")
divider("Part 4: The HD wallet", "One seed, a tree of keys",
        [("master private key", "the first private key of the tree"),
         ("master chain code", "the 32 bytes that let the tree keep growing"),
         ("child key derivation", "a new key from a parent, a chain code and an index"),
         ("hardened derivation", "a step only the private parent key can take"),
         ("extended key", "a key and its chain code written as one string"),
         ("index number", "which child: 0 to 2^31-1 normal, then hardened")],
        ["Root seed", "HMAC-SHA512", "Master key + chain code", "Children by index", "Extended keys"],
        "Part four builds the tree. One HMAC of the seed gives the master key and chain code. Every child comes from a parent, its chain code and an index. Extended keys write the pair as text.",
        "Creating an HD Wallet from the Seed", hot=(2,))

s = new_slide("One seed, a tree of keys", "Every node is a key and a chain code", "Hierarchical Deterministic (HD) Key Generation (BIP32)",
              "The picture is the book's: a seed becomes a master key, the master key has children, and each child has grandchildren. Every node is two 32-byte values, the key and its chain code, so the tree never runs dry.")
g = group(s, "visual: the tree of keys")
gbox(g, 0.4, 2.55, 0.9, 0.7, "seed", 13, C["dark"], C["white"], True)
gbox(g, 1.75, 2.55, 1.15, 0.7, "master\nkey m", 12, C["orange"], C["white"], True)
garrow(g, 1.3, 2.9, 1.75, 2.9)
for r, yy in enumerate((1.5, 2.7, 3.9)):
    gbox(g, 3.25, yy, 0.95, 0.6, "m/%d" % r, 12, C["slate"], C["white"], True)
    garrow(g, 2.9, 2.9, 3.25, yy + 0.3)
    for q, dy in enumerate((-0.32, 0.32)):
        gbox(g, 4.55, yy + dy, 0.95, 0.5, "m/%d/%d" % (r, q), 11)
        garrow(g, 4.2, yy + 0.3, 4.55, yy + dy + 0.25)
tb(s, 0.4, 1.2, 5.2, 0.28, "Nodes are named by their paths", 11.5, C["slate"], bold=True, name="figure label")
cards(s, [("Master", "One HMAC of the seed gives the master key and chain code."),
          ("Children", "A parent, its chain code and an index make each child."),
          ("Every node", "32 bytes of key and 32 bytes of chain code.")],
      5.65, 1.3, 3.85, 3.4, cols=1, fs=12.5)
takeaway(s, "From one seed grows a tree that backs up as one secret.", 4.88)

code_slide("master_key", "Code 11: HMAC-SHA512 makes the master key", "Master private key and master chain code", "Creating an HD Wallet from the Seed",
           "HMAC-SHA512 mixes a secret key with data. Using the text Bitcoin seed as the key and the seed as data gives 64 bytes. The left half is the master private key, the right half the master chain code.",
           lambda s, out, y, h: (
               flow(s, 0.4, y + 0.05, 2.4, min(1.1, h - 0.5), ["Seed, 16 bytes"], name="visual: seed", size=12),
               (lambda g: (gbox(g, 3.2, y + 0.05, 3.0, min(1.1, h - 0.5), "Master private key  32 bytes  " + L(out, 2)[:10] + "...", 11.5, C["orange"], C["white"], True),
                           gbox(g, 6.4, y + 0.05, 3.1, min(1.1, h - 0.5), "Master chain code  32 bytes", 11.5, C["slate"], C["white"], True),
                           garrow(g, 2.8, y + 0.05 + min(1.1, h - 0.5) / 2, 3.2, y + 0.05 + min(1.1, h - 0.5) / 2)))(group(s, "visual: 64 bytes in two halves")),
               tb(s, 0.4, y + min(1.1, h - 0.5) + 0.12, 9.1, 0.3, "64 bytes in all = %s; both halves match the library: %s" % (" + ".join(L(out, 0).split()[1:]), L(out, 1)), 12, C["slate"], bold=True, name="reading")),
           "Half of the HMAC is the key, half the chain code.")

code_slide("child_keys", "Code 12: Child keys from a parent and an index", "Child key derivation, chain code and index", "Private child key derivation",
           "A child key needs the parent key, the parent chain code and an index number. The chain code is what makes children unpredictable. Each child gets its own new chain code, so the tree can keep growing.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Index", "Child private key (first 12 hex digits)", "Child chain code (first 12 hex)"]] +
                                      [[l.split()[0], l.split()[1][:12], l.split()[2][:12]] for l in L(out)],
                                      [1.0, 4.1, 4.1], 12, min(0.34, h / 4), name="result table", mono_cols=(1, 2)),
           "Three indexes, three unrelated children.")

code_slide("hardened", "Code 13: Hardened and normal children differ", "Hardened child key derivation", "Hardened child key derivation",
           "Indexes below 2 to the 31 are normal; from 2 to the 31 up they are hardened. A hardened child is derived from the private parent key, not its public key. In a path, the letter h means hardened.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Child index", "Kind", "Same key as child 0?"],
                                                       ["0", "normal", "-"], [L(out, 0).split()[0], "hardened (first one)", L(out, 0).split()[1]],
                                                       ["the path m/0h", "hardened", "its index is 2^31: " + L(out, 1)]],
                                     [3.0, 3.0, 3.2], 12, min(0.34, h / 4), name="result table"),
           "The letter h in a path is a security decision.")

code_slide("xpub_leak", "Code 14: Why hardened steps protect the parent", "Using derived child keys", "Using derived child keys",
           "A normal child private key plus the parent's extended public key reveals the parent private key. Subtract the hash value and the parent falls out. A hardened step cannot be undone this way, so account levels are hardened.",
           lambda s, out, y, h: (flow(s, 0.4, y + 0.05, 9.1, min(0.9, h - 0.5), ["Parent extended public key", "+ one normal child private key", "- the hash value", "= parent private key"], name="visual: the leak", hot=(3,), size=12),
                                 tb(s, 0.4, y + min(0.9, h - 0.5) + 0.12, 9.1, 0.3, "The run printed " + L(out, 0) + ": the parent private key was recovered.", 12, C["slate"], bold=True, name="reading")),
           "Normal child plus xpub exposes the parent; hardening stops it.")

code_slide("public_derivation", "Code 15: Public keys derived without private keys", "Public child key derivation", "Public Child Key Derivation",
           "Normal derivation works on public keys too. Route one derives the private child and then its public key. Route two never touches a private key. Both give the same public key.",
           lambda s, out, y, h: (lambda g, hh: (
               gbox(g, 0.4, y + 0.02, 2.6, hh, "Parent private key", 11.5), gbox(g, 3.4, y + 0.02, 2.6, hh, "Child private key", 11.5), gbox(g, 6.4, y + 0.02, 3.1, hh, "Child public key", 11.5, C["orange"], C["white"], True),
               garrow(g, 3.0, y + 0.02 + hh / 2, 3.4, y + 0.02 + hh / 2), garrow(g, 6.0, y + 0.02 + hh / 2, 6.4, y + 0.02 + hh / 2),
               gbox(g, 0.4, y + hh + 0.2, 2.6, hh, "Parent public key", 11.5), gbox(g, 6.4, y + hh + 0.2, 3.1, hh, "Same child public key: " + L(out, 0), 11.5, C["slate"], C["white"], True),
               garrow(g, 3.0, y + hh + 0.2 + hh / 2, 6.4, y + hh + 0.2 + hh / 2)))(group(s, "visual: two routes, one result"), min(0.55, (h - 0.25) / 2)),
           "Public keys alone can make the shop's addresses.")

code_slide("extended_keys", "Code 16: Extended keys, xprv and xpub", "Extended key encoding and key fingerprint", "Extended keys",
           "An extended key is a key plus its chain code, written in Base58Check. It starts with xprv for private and xpub for public, and is 111 characters long. A four-byte fingerprint names the key.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Item", "Starts with", "Length / value"],
                                                       ["Extended private key", L(out, 0).split()[0], L(out, 0).split()[1] + " characters"],
                                                       ["Extended public key", L(out, 0).split()[2], L(out, 0).split()[3] + " characters"],
                                                       ["Fingerprint of the master key", "-", L(out, 1)], ["Depth of the master key", "-", L(out, 2)]],
                                     [3.4, 2.4, 3.4], 12, min(0.32, h / 5), name="result table"),
           "xprv can spend; xpub can only watch.")

code_slide("index_space", "Code 17: 2 to the 31 children, normal and hardened", "Index numbers for normal and hardened derivation", "Index numbers for normal and hardened derivation",
           "The book says each parent can have 2,147,483,647 children. BIP32 says 2 to the 31 normal children and as many hardened ones. The book's figure is the largest normal index, not the count.",
           lambda s, out, y, h: (
               chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, ["Normal: 0 to 2^31-1", "Hardened: 2^31 to 2^32-1"], [("children, in billions", [int(v) / 1e9 for v in L(out, 1).split()])], 0.4, y, 5.6, h, numfmt="0.000", name="result chart", fs=11, axis_title="billions of children"),
               box_text(s, 6.2, y + 0.1, 3.3, min(1.5, h - 0.2), "The largest normal index is " + L(out, 0).split()[2] + "; the count is " + L(out, 0).split()[0] + ".", 12.5, C["ink"], C["card"], name="reading")),
           "The book's 2,147,483,647 is the last index, not the count.")

analogy_slide("Everyday pictures for part 4, the tree", "A family tree with secrets",
              [("master private key", "The ancestor's key at the top of the tree", "The first private key of the tree"),
               ("master chain code", "The ancestor's secret handshake", "The 32 bytes that let children be made"),
               ("child key derivation", "A child born from a parent and a birth number", "A new key from parent key, chain code and index"),
               ("chain code", "A family secret passed down each generation", "32 bytes that keep derivation unpredictable"),
               ("index number", "Birth order: first child, second child", "0 to 2^31-1 normal, then hardened")],
              "The family tree fits well. The ancestor holds the master key, each child is born from a parent and a birth number, and the chain code is the family secret that keeps children unpredictable.",
              "Creating an HD Wallet from the Seed")

analogy_slide("Everyday pictures for part 4, extended keys", "Notes stapled to a key",
              [("extended key", "A key with its family notes stapled on", "A key plus its chain code in one string"),
               ("extended private key", "The archive where every door opens", "xprv: it can spend and derive"),
               ("extended public key", "A guest list that greets visitors but opens no doors", "xpub: it derives public keys only"),
               ("hardened derivation", "A firewall between parent and children", "A step that needs the private parent key")],
              "An xprv is the whole archive; an xpub is the guest list. The firewall picture for hardened derivation is the one to remember: a leaked child must not open the parent.",
              "Extended keys", "Give out the guest list, never the archive.")

analogy_slide("Everyday pictures for part 4, the book's sections", "Family trees, firewalls and shelves",
              [("Hierarchical Deterministic (HD) Key Generation (BIP32)", "A family tree grown from one ancestor", "One seed, a tree of keys"),
               ("Creating an HD Wallet from the Seed", "Planting the first tree from a seed", "Seed to master key and chain code"),
               ("Private child key derivation", "A parent handing a child their own key", "A child private key from the parent private key"),
               ("Using derived child keys", "Giving each room its own key, not the master", "Hardened children never expose the parent"),
               ("Extended keys", "A key with its family notes stapled on", "A key plus a chain code, as xprv or xpub"),
               ("Public child key derivation", "Numbering doors without holding any key", "Public keys derived from a public key"),
               ("Hardened child key derivation", "A firewall between parent and child", "A step that needs the private parent key"),
               ("Index numbers for normal and hardened derivation", "Two numbered shelves, one ordinary, one locked", "0 to 2^31-1 normal; 2^31 and up hardened")],
              "The family tree is the main picture, and the rest follow from it. A parent hands a child a key, a firewall protects the parent, and two shelves hold the normal and the hardened children.",
              "Creating an HD Wallet from the Seed")
