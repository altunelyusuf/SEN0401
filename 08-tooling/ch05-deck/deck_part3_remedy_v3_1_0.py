#!/usr/bin/env python3
"""Chapter 5 deck v3.1.0 - part 5 (paths and descriptors), part 6 (data that is not keys), part 7 (deploying and testing), closing."""
__version__ = "3.1.0"
from deck_part2_remedy_v3_1_0 import *

# =============================================================== PART 5: paths and descriptors
part("Paths and descriptors")
divider("Part 5: Paths and descriptors", "Which key is which, and how to write it down",
        [("HD wallet path", "numbers from the master key down to one key"),
         ("BIP43 and BIP44", "the first number names the scheme; BIP44 fixes five levels"),
         ("implicit paths", "paths fixed by a standard, so not recorded"),
         ("explicit paths", "paths written down next to the recovery code"),
         ("output script descriptors", "text that names the script and the keys behind it"),
         ("key origin", "the bracket naming a key's parent fingerprint and path")],
        ["Recovery code", "Path m/84h/0h/0h", "Descriptor text", "Addresses"],
        "Part five answers the question: given a recovery code, which keys does the wallet use? A path names a key. Standards fix common paths. A descriptor writes down both script and path.",
        "Backing Up Key Derivation Paths", hot=(2,))

code_slide("key_path", "Code 18: Reading a key path level by level", "HD wallet path, BIP43 and BIP44", "HD wallet key identifier (path)",
           "A path is a list of child numbers below the master key m. The first number, the purpose, names the scheme. BIP44 then fixes coin, account, change and address index. A trailing h marks a hardened step.",
           lambda s, out, y, h: (lambda g, hh: (
               gbox(g, 0.4, y + 0.1, 0.8, hh, "m", 14, C["dark"], C["white"], True),
               [(gbox(g, 1.5 + i * 1.62, y + 0.1, 1.45, hh,
                      "%s\n%s" % (l.split()[0], (str(int(l.split()[1]) - 2 ** 31) + "h") if l.split()[2] == "True" else l.split()[1]), 11.5,
                      C["orange"] if l.split()[2] == "True" else C["card"], C["white"] if l.split()[2] == "True" else C["ink"], True),
                 garrow(g, (1.2 if i == 0 else 1.5 + (i - 1) * 1.62 + 1.45), y + 0.1 + hh / 2, 1.5 + i * 1.62, y + 0.1 + hh / 2)) for i, l in enumerate(L(out))],
               tb(s, 0.4, y + 0.1 + hh + 0.08, 9.1, 0.3, "Orange levels are hardened: purpose, coin type and account. Change and index are normal.", 12, C["slate"], bold=True, name="reading")))(
               group(s, "visual: the five path levels"), min(0.85, h - 0.5)),
           "Purpose, coin, account, change, index.")

code_slide("standard_paths", "Code 19: Four standard paths, four address types", "Implicit paths and output scripts", "Backing Up Key Derivation Paths",
           "Standards fix the purpose number: 44, 49, 84 and 86. A wallet that follows one needs no written path, an implicit path. The same recovery code gives four different kinds of address.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Purpose", "Address type", "First address of the BIP84 test code"]] +
                                      [[p, t, a] for (p, t), a in zip([("44 (BIP44)", "legacy"), ("49 (BIP49)", "nested segwit"), ("84 (BIP84)", "native segwit"), ("86 (BIP86)", "taproot")], L(out))],
                                      [1.5, 1.6, 6.1], 11, min(0.32, h / 5), name="result table", mono_cols=(2,), mono_fs=10),
           "One recovery code, four kinds of address.", need=1.6)

code_slide("bip84_vector", "Code 20: Our address equals the standard's own", "Explicit paths and the standard's test vector", "Backing Up Key Derivation Paths",
           "To trust a library, compare it with a published answer. BIP84 prints the first address of its test recovery code, and Bitcoin Core derives the same one. If a path is not standard, write it down: an explicit path.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Source", "First address at m/84h/0h/0h/0/0"],
                                                       ["Our code, in this run", "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"],
                                                       ["BIP84 and Bitcoin Core publish", "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu"],
                                                       ["Equal?", L(out, 0)]], [3.4, 5.8], 12, min(0.34, h / 4), name="result table", mono_cols=(1,)),
           "Check your code against the published vector.")

code_slide("key_tweak", "Code 21: A key tweak makes the taproot key", "Key tweak and BIP86", "Backing Up Key Derivation Paths",
           "A key tweak is a number added to a key to make a related key. Taproot adds a hash-derived tweak to the internal key. The address encodes the tweaked output key, not the internal one.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Item", "Value"], ["Internal key (BIP86 path), first 12 hex", L(out, 0).split()[0]],
                                                       ["Output key after the tweak, first 12 hex", L(out, 0).split()[1]], ["Taproot address", L(out, 1)]],
                                     [3.2, 6.0], 12, min(0.34, h / 4), name="result table", mono_cols=(1,), mono_fs=10.5),
           "Add a number to a key and you get a related key.", need=1.55)

s = new_slide("Implicit and explicit paths", "Which paths need writing down?", "Backing Up Key Derivation Paths",
              "A standard path needs no record because everyone knows it: that is implicit. A custom path must be written with the code: that is explicit. The book's table uses coin type one for BIP49, which is the testnet type.")
cards(s, [("Implicit path", "Fixed by a standard such as BIP44, so the wallet does not record it."),
          ("Explicit path", "Written down with the recovery code, usually in descriptor notation.")],
      0.5, 1.3, 9.0, 1.15, cols=2, fs=12.5)
table(s, 0.5, 2.6, 9.0, [["Purpose", "Standard", "Path in the book", "Note"],
                         ["44", "BIP44", "m/44'/0'/0'", "legacy scripts"], ["49", "BIP49", "m/49'/1'/0'", "coin type 1 is testnet in SLIP-0044"],
                         ["84", "BIP84", "m/84'/0'/0'", "native segwit"], ["86", "BIP86", "m/86'/0'/0'", "single-key taproot"]],
      [1.2, 1.5, 2.3, 4.0], 12, 0.36, name="path table")
takeaway(s, "Know which paths are implicit and write down the rest.")

code_slide("descriptor", "Code 22: A descriptor with its checksum and origin", "Output script descriptors, checksum and key origin", "Backing Up Key Derivation Paths",
           "A descriptor is text that names an output script and the keys behind it. BIP380 adds an eight-character checksum. The bracket at the start is the key origin: a fingerprint and the hardened path.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Part", "What the run printed"],
                                                       ["Checksum of the wpkh descriptor", L(out, 0)],
                                                       ["Key origin: fingerprint, hardened steps", L(out, 1)],
                                                       ["A 2-of-3 multisignature descriptor with its checksum", L(out, 2)]],
                                     [4.4, 4.8], 12, min(0.36, h / 4), name="result table", mono_cols=(1,)),
           "One line of text can rebuild the wallet's structure.", need=1.55)

s = new_slide("Multisignature, multipath and miniscript", "Three ways descriptors grow", "Backing Up Key Derivation Paths",
              "Multisignature needs several keys: two of three is the usual example. A multipath descriptor writes the receiving and change branches once. Miniscript is a structured language for scripts that tools can analyse.")
g = group(s, "visual: two of three keys")
gbox(g, 0.5, 1.4, 1.4, 0.5, "Key A", 12); gbox(g, 0.5, 2.05, 1.4, 0.5, "Key B", 12); gbox(g, 0.5, 2.7, 1.4, 0.5, "Key C", 12)
gbox(g, 3.0, 1.9, 3.0, 0.75, "wsh(multi(2,A,B,C))", 12, C["orange"], C["white"], True, font=MONO)
gbox(g, 7.0, 1.9, 2.4, 0.75, "Any two sign", 12, C["slate"], C["white"], True)
for yy in (1.65, 2.3, 2.95):
    garrow(g, 1.9, yy, 3.0, 2.27)
garrow(g, 6.0, 2.27, 7.0, 2.27)
cards(s, [("Multisignature", "Spending needs signatures from at least a threshold of the listed keys."),
          ("Multipath descriptor", "One path step holds a tuple, such as receiving and change, in one descriptor."),
          ("Miniscript", "A language for a subset of scripts that supports analysis and generic signing.")],
      0.5, 3.4, 9.0, 1.4, cols=3, fs=11.5)
takeaway(s, "Descriptors keep the wallet's rules in one line of text.", 4.9)

analogy_slide("Everyday pictures for part 5", "Street addresses and recipe cards",
              [("HD wallet path", "A street address: country, city, street, house", "A list of numbers from the master key to one key"),
               ("BIP43", "A postal rule: the first number picks the scheme", "The purpose number below the master key"),
               ("BIP44", "A house numbering scheme everyone adopted", "Five levels: purpose, coin, account, change, index"),
               ("implicit paths", "A standard everyone knows without being told", "A path fixed by a standard, not recorded"),
               ("explicit paths", "The address written on the envelope", "A path written down with the backup"),
               ("output script descriptors", "A recipe card naming the dish and its ingredients", "Text that names the script and the keys")],
              "A path is a street address down the tree. Implicit paths are the streets everyone knows; explicit paths are addresses you write on the envelope. A descriptor is the whole recipe card.",
              "Backing Up Key Derivation Paths")

analogy_slide("Everyday pictures for part 5, the book's sections", "Addresses inside a building",
              [("Backing Up Key Derivation Paths", "Writing the street address down with the key", "Paths or descriptors saved with the code"),
               ("HD wallet key identifier (path)", "The address of one room in a building", "m/84h/0h/0h/0/0 names exactly one key"),
               ("Navigating the HD wallet tree structure", "Walking down a family tree by birth order", "Levels: purpose, coin, account, change, index")],
              "A path is the address of one room in a building, and navigating the tree is walking down the floors. Write the address down with the key, or the key may be found but never matched to its room.",
              "Backing Up Key Derivation Paths")

# =============================================================== PART 6: data that is not keys
part("Data that is not keys")
divider("Part 6: Data that is not keys", "A recovery code is not the whole backup",
        [("label", "a note that names an address or a transaction"),
         ("BIP329", "a standard file format for exporting labels"),
         ("Lightning Network", "payments off the blockchain, with their own state"),
         ("static channel backups", "a one-time backup that helps recover channel funds"),
         ("encryption", "readable data turned into data only a key holder reads"),
         ("encrypted wallet backup", "the whole database, encrypted by a key from the seed")],
        ["Keys from the seed", "Labels", "Protocol data", "Encrypted backup"],
        "Part six is about what a recovery code does not hold. Labels, protocol data such as Lightning channels, and the full database are not in the seed. They need their own backups.",
        "Backing Up Nonkey Data", hot=(3,))

code_slide("labels", "Code 23: Labels exported in the BIP329 format", "Address label, transaction label, BIP329", "Backing Up Nonkey Data",
           "Labels are notes such as rent or salary. They are not derivable from the seed, so losing them loses your bookkeeping. BIP329 stores one JSON object per line, readable by any program.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["type", "reference (first 14 characters)", "label"]] +
                                      [[json.loads(l)["type"], json.loads(l)["ref"][:14] + "...", json.loads(l)["label"]] for l in L(out)],
                                      [1.2, 5.2, 2.8], 12, min(0.36, h / 3), name="result table", mono_cols=(1,)),
           "Labels are data too: export them.")

s = new_slide("Channels and encrypted backups", "Two answers to data that keys cannot rebuild", "Backing Up Nonkey Data",
              "The Lightning Network keeps payment state off the blockchain. A static channel backup is saved once, when a channel opens, and helps recovery after data loss, but cannot guarantee results. An encrypted wallet backup stores everything, encrypted with a key from the seed.")
flow(s, 0.5, 1.3, 9.0, 0.7, ["Channel opens", "Static channel backup saved once", "Data is lost", "Backup helps close the channel"], name="visual: static channel backup", hot=(1,), size=12)
flow(s, 0.5, 2.3, 9.0, 0.7, ["Wallet database: keys, labels, protocol data", "Encrypted with a key from the seed", "Stored copy", "Restore: seed decrypts it"], name="visual: encrypted wallet backup", hot=(1,), size=12)
cards(s, [("Static channel backups", "A one-time backup for the off-chain pool; it cannot guarantee results."),
          ("Encrypted wallet backup", "Complete backups made often and automatically, encrypted by a key derived from the seed.")],
      0.5, 3.25, 9.0, 1.5, cols=2, fs=12.5)
takeaway(s, "Keys come back from the seed; the rest needs its own copy.", 4.9)

story_slide("GoxColdFind", [
    "Mark Karpeles, chief executive of Mt. Gox; reporter Simon Sharwood, The Register.",
    "Found about 200,000 BTC in an old-format wallet file.",
    ("2014-03-21", " - three weeks after the bankruptcy filing."),
    "An old-format wallet file the exchange thought held nothing.",
    "The company believed its old wallets were empty and had not checked them.",
    "A file made by software two generations older still held spendable keys."],
    "In March 2014, three weeks into its bankruptcy, Mt. Gox said it had found about 200,000 bitcoin in an old-format wallet it thought was empty. Backups do not expire, and an untested file is not an empty one.")

# =============================================================== PART 7: deploying and testing
part("Deploying and testing")
divider("Part 7: Deploying and testing", "Keys at work, and a backup you have tested",
        [("extended public key deployment", "an xpub placed where it makes addresses"),
         ("payment processor", "software that turns an xpub into a working shop"),
         ("gap limit", "how many unused addresses in a row a scan checks"),
         ("cold storage", "keys kept where no connected computer can read them"),
         ("written backup", "the recovery code written on a physical medium"),
         ("testing a backup", "a restore drill before you need it")],
        ["Extended public key on the shop", "Customer pays", "Keys stay cold", "Restore drill"],
        "Part seven puts keys to work. A shop holds only an extended public key. Cold storage keeps keys offline. And the chapter ends with the most important habit: test the backup before you need it.",
        "Using an Extended Public Key on a Web Store", hot=(3,))

code_slide("xpub_shop", "Code 24: A web shop that holds no private key", "Extended public key on a web store", "Using an Extended Public Key on a Web Store",
           "A shop can generate a fresh address per customer from an extended public key. The payment processor, such as BTCPay Server, does this. The shop never sees a private key, so a hacked server cannot spend.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Customer", "Fresh address made from the xpub"]] + [[l.split()[0], l.split()[1]] for l in L(out)],
                                      [1.6, 7.6], 12, min(0.34, h / 4), name="result table", mono_cols=(1,)),
           "Publish the xpub; the keys never touch the internet.")

code_slide("gap_limit", "Code 25: The gap limit decides how far a scan looks", "Mind the Gap", "Mind the Gap",
           "A recovery scan stops after a number of unused addresses in a row: the gap limit. If you used key 25 but skipped many keys, a small gap misses it. A bigger gap finds it.",
           lambda s, out, y, h: (
               chart(s, XL_CHART_TYPE.COLUMN_CLUSTERED, ["gap %s" % l.split()[0] for l in L(out)], [("used keys found", [int(l.split()[1]) for l in L(out)])], 0.4, y, 6.0, h, numfmt="0", name="result chart", fs=11, axis_title="used keys found"),
               box_text(s, 6.7, y + 0.1, 2.8, min(1.5, h - 0.2), "The wallet used keys 0, 3 and 25. Only gap 30 reaches key 25.", 12.5, C["ink"], C["card"], name="reading")),
           "A scan that stops too early misses your money.")

code_slide("signature", "Code 26: A digital signature fails if the message changes", "Digital signature and the hardware signing device", "Using an Extended Public Key on a Web Store",
           "A signing device signs the hash of a transaction with a private key. Anyone can verify with the public key. The signature is valid only for the message that was signed. This is a toy version, not for real money.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Check", "Verifies?"], ["The message that was signed", L(out, 0)], ["Another message with the same signature", L(out, 1)]],
                                     [6.0, 3.2], 12, min(0.36, h / 3), name="result table"),
           "A signature binds one key to one message.")

s = new_slide("Cold storage and the hardware signing device", "Keep keys where nothing connected can read them", "Backing Up Key Derivation Paths",
              "Cold storage keeps a reserve offline. A hardware signing device holds keys and signs without revealing them. A written backup of the recovery code is the last line of defence, kept apart from the device.")
flow(s, 0.5, 1.3, 9.0, 0.75, ["Wallet on a connected computer: watch-only", "Unsigned transaction", "Signing device offline signs", "Signed transaction returns"], name="visual: offline signing", hot=(2,), size=12)
cards(s, [("Cold storage", "Keys created and stored offline; the book advises it for any significant holding."),
          ("Hardware signing device", "Signs transactions and never shows the private keys."),
          ("Written backup", "The recovery code on paper or metal, stored apart from the device.")],
      0.5, 2.3, 9.0, 2.4, cols=3, fs=14)
takeaway(s, "Offline keys, a device that signs, and a code on paper.", 4.9)

code_slide("restore_drill", "Code 27: The restore drill, a typo opens another wallet", "Testing a backup", "Wallet Recovery",
           "A backup counts only after a successful restore. Write down the first address when the wallet is created, then restore from your written code and compare. One wrong word does not give an error, it gives a different, empty wallet.",
           lambda s, out, y, h: table(s, 0.4, y, 9.2, [["Restore from", "Same first address as noted?"],
                                                       ["the right recovery code", L(out, 0)], ["the code with one word changed", L(out, 1)]],
                                     [5.0, 4.2], 12, min(0.36, h / 3), name="result table"),
           "Test the restore, not your luck.")

s = new_slide("What a complete backup holds", "The chapter's closing list", "Wallet Recovery",
              "Data loss is perhaps the leading cause of lost bitcoin. A complete backup is a list: the recovery code, the passphrase if used, the paths or descriptors, other signers' public keys, and data that is not keys. Then test it.")
items = ["Recovery code", "Passphrase, if used", "Paths or descriptors", "Other signers' public keys", "Labels and protocol data"]
for i, t in enumerate(items):
    box_text(s, 0.5 + i * 1.82, 1.4, 1.7, 1.2, t, 13, C["ink"], C["card"], bold=True, align=PP_ALIGN.CENTER, name="backup item", font=HF)
box_text(s, 0.5, 2.9, 9.0, 0.8, "Then restore from the backup alone, and check the first address.", 16, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="test step", font=HF)
tb(s, 0.5, 3.9, 9.0, 0.6, "Data loss is nobody's fault but cannot be reversed: the holder makes the backups and tests them.", 13, C["mute"], italic=True, name="closing remark")
takeaway(s, "A backup is complete when a restore drill succeeds.", 4.9)

analogy_slide("Everyday pictures for parts 6 and 7", "Sticky notes, photocopies and mailboxes",
              [("label", "A sticky note on a drawer", "Text naming an address or a transaction"),
               ("BIP329", "A filing format so notes move between programs", "One JSON line per label"),
               ("static channel backups", "A photocopy of a contract made once", "Helps recover channel funds; no guarantee"),
               ("gap limit", "Checking mailboxes until a set number in a row are empty", "How many unused addresses in a row a scan checks"),
               ("Backing Up Nonkey Data", "Photocopying your notes and contracts", "Labels and protocol data kept apart from the seed"),
               ("Mind the Gap", "Looking down the street for the next used mailbox", "The gap limit of a recovery scan"),
               ("Using an Extended Public Key on a Web Store", "Handing the shop a guest list, not the archive", "The xpub makes a fresh address per customer")],
              "Labels are sticky notes, and they are not in the seed. A static channel backup is a photocopy: it helps but guarantees nothing. The gap limit is a patient postman who stops after a set number of empty mailboxes.",
              "Mind the Gap", "Notes, copies and mailboxes: each needs its own backup or setting.")

# =============================================================== closing
s = new_slide("The chapter in five lines", "One line per part", "Wallet Recovery",
              "Five lines carry the chapter. Wallets derive keys from a seed. A recovery code is entropy in words. A seed is stretched slowly. The tree hands every purpose a numbered key. And a backup counts only once it has been restored.")
five = ["Wallets stopped storing keys and started deriving them: one seed, backed up once.",
        "A recovery code is entropy in words: 11 bits a word, checksum included.",
        "Words become a 512-bit seed by deliberate slowness; a passphrase forks the wallet.",
        "The HD tree gives every purpose a numbered key; hardened steps protect the parent.",
        "Beyond keys: paths, labels, channels, and a backup counts only once it is restored."]
for i, t in enumerate(five):
    box_text(s, 0.5, 1.3 + i * 0.68, 0.5, 0.58, str(i + 1), 16, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="line number", font=HF)
    box_text(s, 1.1, 1.3 + i * 0.68, 8.4, 0.58, t, 13.5, C["ink"], C["card"], name="summary line")
takeaway(s, "If a line feels unproven, its part's code slides carry the receipt.", 4.9)

s = new_slide("Check yourself", "Six questions, then the slides that answer them", "Wallet Recovery",
              "Try each question aloud before you look at the slide. If you hesitate, go back to the slide named on the right. These are the questions the exam will build on.")
table(s, 0.5, 1.3, 9.0, [["Question", "Look again at"],
                         ["Why is one seed better than many loose keys?", "Code 1"],
                         ["How many words does 256 bits of entropy make?", "Code 5"],
                         ["What does the checksum protect against?", "Code 7"],
                         ["Why does a passphrase change the wallet?", "Code 10"],
                         ["Why are account levels hardened?", "Code 14"],
                         ["How do you know a backup works?", "Code 27"]], [6.4, 2.6], 13, 0.46, name="question table")
takeaway(s, "Answer without looking, then check the code slide.", 4.9)

RES = [("Read", "Mastering Bitcoin, ch. 5: Wallets", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/develop/ch05_wallets.adoc"),
       ("Read", "NYT via Business Standard (news)", STORY["IronKey"]["link"]),
       ("Read", "MtGox finds 200,000 Bitcoin (The Register)", STORY["GoxColdFind"]["link"]),
       ("Standards", "BIP 39: Mnemonic code", "https://bips.dev/39/"),
       ("Standards", "BIP 32: HD wallets", "https://bips.dev/32/"),
       ("Standards", "BIP 84: P2WPKH derivation", "https://bips.dev/84/"),
       ("Standards", "BIP 380: Output script descriptors", "https://bips.dev/380/"),
       ("Seminal work", "Bitcoin: A Peer-to-Peer Electronic Cash System", "https://bitcoin.org/bitcoin.pdf"),
       ("Tools", "Ian Coleman's BIP39 tool (use offline)", "https://iancoleman.io/bip39/"),
       ("Tools", "BTCPay Server (the book's web store)", "https://btcpayserver.org"),
       ("Tutorial", "Bitcoin Wiki: Deterministic wallet", "https://en.bitcoin.it/wiki/Deterministic_wallet"),
       ("Community", "Bitcoin Stack Exchange", "https://bitcoin.stackexchange.com"),
       ("Community", "Bitcoin Optech topics", "https://bitcoinops.org/en/topics/"),
       ("Course corpus", "SEN0401 course repository", "https://github.com/altunelyusuf/SEN0401"),
       ("Watch", "BIP-39 mnemonic words (video, Mobilefish.com)", "https://www.youtube.com/watch?v=hRXcY_tIlrw")]
s = new_slide("Where to go from here", "Every entry is a live link; the course page holds the same code", "Wallet Recovery",
              "These are the places to read, check and ask. Start with the book chapter and the three BIPs. Use the tool only offline. The same code examples are on the course page, in the same order as the slides.")
groups = {}
for g, lab, url in RES:
    groups.setdefault(g, []).append((lab, url))
pos = {"Read": (0.5, 1.28, 4.4, 1.0), "Standards": (5.1, 1.28, 4.4, 1.28), "Seminal work": (0.5, 2.38, 4.4, 0.62), "Tools": (0.5, 3.1, 4.4, 0.78),
       "Tutorial": (0.5, 3.98, 4.4, 0.62), "Community": (5.1, 2.66, 4.4, 0.78), "Course corpus": (5.1, 3.54, 4.4, 0.62), "Watch": (5.1, 4.26, 4.4, 0.62)}
for g, items in groups.items():
    x, y, w, hh = pos[g]
    card(s, x, y, w, hh, C["card"], "resource group")
    paras = [[(g, {"bold": True, "color": C["orange"], "font": HF, "size": 12})]] + [[(lab, {"link": url, "color": C["slate"], "bold": True, "size": 11})] for lab, url in items]
    tb(s, x + 0.08, y + 0.02, w - 0.16, hh - 0.04, paras, 11, name="resources " + g)
takeaway(s, "Twelve words on paper beat every password you have ever memorised.", 4.9)

s = new_slide("What you should now be able to say", "And where each claim gets its proof", "Wallet Recovery",
              "Thank you. You should now be able to say why one seed replaced bags of keys, what twelve words carry, which path your wallet walks, and what a tested backup is. Questions are welcome.")
for i, t in enumerate(["Why one seed replaced bags of keys", "What twelve words carry and how they become a tree", "Which path your wallet walks, and who else can walk it", "What a tested backup is"]):
    box_text(s, 0.8, 1.35 + i * 0.75, 8.4, 0.62, t, 15, C["ink"], C["card"], name="outcome")
box_text(s, 3.0, 4.35, 4.0, 0.55, "Questions?", 22, C["white"], C["orange"], bold=True, align=PP_ALIGN.CENTER, name="questions", font=HF)
