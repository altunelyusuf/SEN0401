#!/usr/bin/env python3
"""Writes ch05-page/question_bank_v1_0_0.json, the question bank of SEN0401 chapter 5: at least one item for every concept of the chapter, at
least two for every concept with a worked example, one of those two an Apply item whose program prints the marked option. The items are kept here
as tuples (concept, level, question, options with the RIGHT one first, why, code or None); this script rotates the right option to a position that
cycles 0, 1, 2, 3 through the bank, so that each position carries a quarter of the items, and writes the JSON the page reads.
Every program uses the standard library only and no file access, because the page runs it in the reader's browser (Pyodide, CPython 3.13, no
ripemd160), and the checker re-runs each one under every interpreter on this machine.
Run: python3 sen0401_ch05_bank_gen_v1_0_0.py        then: python3 question_bank_check_v1_2_0.py 05"""
__version__ = "1.0.0"
import json, os

MN12 = "army van defense carry jealous true garbage claim echo media make crunch"
ENT12 = "0c1e24e5917779d297e14d45f14e1a1a"
SEED1 = "000102030405060708090a0b0c0d0e0f"
I = []     # (concept, level, q, [right, wrong, wrong, wrong], why, code)


def q(concept, level, question, options, why, code=None):
    I.append((concept, level, question, options, why, code))


# ============================== 1 WALLET KEYS ==============================
q("WalletKeys", "Understand", "What does this first branch of the chapter say a Bitcoin wallet is for?",
  ["Holding the keys that prove control of bitcoins recorded on the blockchain",
   "Holding the bitcoins themselves, as a purse holds cash",
   "Holding a copy of the blockchain so balances can be read",
   "Holding the addresses of the people a user has paid"],
  "The branch opens by correcting the purse intuition: a wallet database contains only keys, and the coins are outputs on the blockchain.")
q("WalletContents", "Understand", "Why does the chapter separate the wallet database from the wallet application?",
  ["Because the data can be backed up and the program can be reinstalled, and only one of the two is irreplaceable",
   "Because the application is the only part that holds keys",
   "Because the database is stored on the blockchain and the application is not",
   "Because only applications can be encrypted"],
  "The distinction tells the reader which part has to be backed up: the program can be downloaded again, the keys cannot.")
q("WalletDatabase", "Remember", "What did Bitcoin Core 31.1 report as the format of the wallet created for this chapter?",
  ["sqlite", "berkeleydb", "json", "leveldb"],
  "The evidence file of the fresh wallet reports the format sqlite and descriptor support.")
q("WalletDatabase", "Understand", "A user keeps a copy of the wallet application's installer but not of the wallet file or the recovery code. What have they backed up?",
  ["Nothing that can recover their money",
   "Their keys, because the application can regenerate them",
   "Their labels, but not their keys",
   "Their public keys only"],
  "The keys are in the database or derivable from the seed; the program alone recovers nothing.")
q("PublicKeyOnlyWallet", "Understand", "What can a wallet database that holds only public keys do?",
  ["Recognise payments and give out addresses, but not sign a spending transaction",
   "Sign transactions but not recognise payments",
   "Neither receive nor recognise payments",
   "Everything a full wallet can do, more slowly"],
  "Public keys suffice to make addresses and to watch for payments; spending needs the private key.")
q("ExternalSigning", "Understand", "In external signing, which part holds the private keys?",
  ["The hardware device or the other signers, not the wallet application",
   "The wallet application, which passes them to the device",
   "Both, so that either can sign alone",
   "The blockchain, which releases them on request"],
  "The application builds the transaction and the external party, holding the keys, returns the signature.")
q("KeyGenerationMethods", "Remember", "In which order does the chapter present the ways of making wallet keys?",
  ["Independently, then from a seed, then with key tweaks, then as a tree",
   "As a tree, then from a seed, then independently",
   "From a seed, then independently, then as a tree",
   "With key tweaks, then independently, then from a seed"],
  "The group follows the history, from one random key at a time to the hierarchical deterministic tree.")
q("IndependentKeyGeneration", "Understand", "Why did independent key generation force a backup after almost every payment?",
  ["Because each new key was unrelated to the others, so a backup went out of date as soon as one was made",
   "Because the wallet file grew too large to copy",
   "Because the keys expired after one use",
   "Because the blockchain had to be rescanned"],
  "Nothing could recompute an independently generated key, so every key had to be saved on its own.")
q("IndependentKeyGeneration", "Apply", "At the chapter's figure of about 32 bytes per key, how many bytes must be backed up for 1,000 independently generated keys?",
  ["32000", "1032", "32", "320"],
  "A thousand keys at 32 bytes each is 32,000 bytes, plus overhead.", "print(32 * 1000)")
q("Seed", "Understand", "What makes a seed a sufficient backup of a deterministic wallet?",
  ["Every key is a function of the seed, so the same seed and algorithm give the same keys again",
   "The seed is stored on the blockchain and can be fetched again",
   "The seed is a copy of the wallet database in short form",
   "The seed is signed by the wallet, so it proves ownership"],
  "Determinism is the whole point: the keys need not be saved because they can be recomputed.")
q("Seed", "Apply", "How many bits are in the chapter's example seed f1cc3bc0...fd97bb73, which is 64 hexadecimal digits?",
  ["256", "64", "128", "512"],
  "Sixty-four hexadecimal digits are 32 bytes, that is 256 bits.",
  "print(len(bytes.fromhex('f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73')) * 8)")
q("DeterministicKeyGeneration", "Apply", "The chapter hashes its seed followed by a counter. What are the first eight hexadecimal digits for the counter 0?",
  ["50b18e0b", "a965dbcd", "19580c97", "f1cc3bc0"],
  "The chapter's own shell example prints 50b18e0b... for the first derived value.",
  "import hashlib\nprint(hashlib.sha256(('f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73 + 0' + chr(10)).encode()).hexdigest()[:8])")
q("DeterministicKeyGeneration", "Analyze", "Two wallets use the same seed but one hashes the seed with a counter and the other uses BIP32. What follows?",
  ["They produce different keys, so the algorithm is part of the backup",
   "They produce the same keys, because the seed is the same",
   "Neither can produce keys without the other's software",
   "The second wallet cannot use a seed at all"],
  "A seed is a backup only together with a reference to the deterministic algorithm used.")
q("KeyTweak", "Understand", "What is a key tweak?",
  ["A value added to a public key, and to its private key, so a child public key can be made without the private key",
   "A small change to the curve used by a wallet",
   "A random number that replaces a lost private key",
   "The checksum appended to a recovery code"],
  "Because adding a value to both sides of the equation keeps the pair matching, the public side can be derived alone.")
q("HdKeyGeneration", "Apply", "How many children can one extended key have in all, normal and hardened together?",
  ["4294967296", "2147483647", "2147483648", "65536"],
  "Two ranges of 2 to the 31 make 2 to the 32, which is 4,294,967,296.", "print(2 ** 31 + 2 ** 31)")
q("HdKeyGeneration", "Understand", "What does the tree structure of BIP32 add over a single deterministic sequence?",
  ["Any key can be the parent of further keys, so branches can be shared or kept separate",
   "The keys become shorter",
   "The seed no longer has to be backed up",
   "Public keys can no longer be derived separately"],
  "A single chain can only be shared all or nothing; a tree allows selective sharing.")

# ============================== 2 RECOVERY CODES ==============================
q("RecoveryCodes", "Understand", "What is a recovery code?",
  ["The written form of a wallet's seed, from which every key can be computed again",
   "A password that unlocks a wallet application",
   "A code issued by a wallet provider to reset an account",
   "The identifier of the user's first transaction"],
  "A code encodes the seed, usually as words; it is not a password and is not chosen by the user.")
q("CodeSchemes", "Remember", "Which five schemes does the chapter name as in wide use?",
  ["BIP39, Electrum version 2, Aezeed, Muun and SLIP39",
   "BIP32, BIP39, BIP43, BIP44 and BIP49",
   "BIP39, SLIP39, codex32, Muun and BIP329",
   "Electrum version 1, Electrum version 2, Aezeed, Muun and codex32"],
  "Those are the five the chapter lists; codex32 is added in a note as a new proposal.")
q("Bip39Code", "Apply", "How many words does a BIP39 code have for 128 bits of entropy?",
  ["12", "11", "15", "24"],
  "128 bits plus a 4-bit checksum is 132 bits, and 132 divided by 11 bits a word is 12 words.", "print((128 + 128 // 32) // 11)")
q("Bip39Code", "Analyze", "Which shortcoming does BIP39 itself list that a version number would have removed?",
  ["Software cannot tell which derivation a code belongs to, so it may show an empty wallet",
   "The code is too long to write down",
   "The checksum covers the passphrase and so cannot be checked",
   "The word list changes with every release"],
  "The standard lists the absence of a versioning scheme; Electrum version 2 and Aezeed add one.")
q("ElectrumV2Code", "Apply", "Electrum version 2 uses 132 bits of entropy with an 11-bit word list. How many words is that?",
  ["12", "13", "11", "24"],
  "132 divided by 11 is exactly 12 words, with no checksum bits of its own.", "print(132 // 11)")
q("ElectrumV2Code", "Understand", "How does an Electrum version 2 phrase carry its version number?",
  ["It is the leading digits of an HMAC-SHA512 of the normalised phrase under the key 'Seed version'",
   "It is the first word of the phrase",
   "It is appended to the phrase as a number",
   "It is stored in the wallet file beside the phrase"],
  "Generation enumerates a nonce until the hash begins with a registered prefix, so the prefix is both version and integrity check.")
q("AezeedCode", "Apply", "Aezeed's plaintext is one version byte, a two-byte timestamp and sixteen bytes of entropy. How many bytes is that?",
  ["19", "18", "24", "33"],
  "1 plus 2 plus 16 is 19 bytes, which the cipher turns into 33 bytes and then 24 words.", "print(1 + 2 + 16)")
q("AezeedCode", "Analyze", "Aezeed authenticates its passphrase. What does the chapter say that costs?",
  ["Plausible deniability, because a wrong passphrase now returns an error",
   "The ability to change the passphrase",
   "The wallet birthday, which can no longer be stored",
   "Compatibility with the BIP39 word list"],
  "Authentication adds error detection and proof of disclosure and removes deniability.")
q("MuunCode", "Understand", "Why is the Muun recovery code not enough on its own?",
  ["It is not the seed; it decrypts the private keys held in a separate printed kit",
   "It is only half of a two-part seed, the other half being memorised",
   "It expires after a year",
   "It needs Muun's servers to be redeemed"],
  "The code and the kit are two objects that are useless apart, which is why the tool asks for the kit's path.")
q("Slip39Code", "Apply", "A SLIP39 share of a 128-bit secret is 200 bits in a word list of 1,024 words. How many words is one share?",
  ["20", "13", "24", "33"],
  "Ten bits a word for 200 bits is 20 words, which is what the standard's table gives.", "print(200 // 10)")
q("Slip39Code", "Analyze", "Three of five SLIP39 shares are kept in different places and two are destroyed. What is the position?",
  ["The seed can still be recovered, because the threshold was three",
   "The seed is lost, because all five shares are needed",
   "The seed is lost, because the two destroyed shares held part of it",
   "Only three fifths of the keys can be recovered"],
  "Any threshold-many shares define the secret; fewer than the threshold reveal nothing about it.")
q("Codex32Code", "Apply", "How many characters are in codex32's first test vector ms10testsxxxxxxxxxxxxxxxxxxxxxxxxxx4nzvca9cmczlw?",
  ["48", "47", "50", "44"],
  "Three for the prefix, one threshold, four identifier, one share index, 26 data and 13 checksum characters make 48.",
  "print(len('ms10testsxxxxxxxxxxxxxxxxxxxxxxxxxx4nzvca9cmczlw'))")
q("Codex32Code", "Understand", "What does codex32 give up in order to be computable by hand?",
  ["Passphrases and key hardening", "Error correction", "Secret sharing", "A fixed length"],
  "The standard says plainly that it does not support passphrases or key hardening, because hand computation must be possible.")
q("CodeTradeoffs", "Understand", "Why does the chapter present the choices behind a code as trade-offs rather than rules?",
  ["Because users and developers disagree, and each choice helps in one situation and hurts in another",
   "Because the standards have not yet been published",
   "Because wallets do not implement the options",
   "Because the choices make no practical difference"],
  "The chapter says it expects the debate over deniability and error detection to continue as long as codes are used.")
q("RecoveryPassphrase", "Apply", "The program compares the seeds of the same twelve words with and without the passphrase. What does it print?",
  ["False", "True", "None", "ValueError"],
  "The passphrase is part of the salt, so the two seeds differ and the comparison is false.",
  "import hashlib, hmac\ndef seed(words, salt, rounds=2048):\n    u = hmac.new(words, salt + b'\\x00\\x00\\x00\\x01', hashlib.sha512).digest()\n    out = bytearray(u)\n    for _ in range(rounds - 1):\n        u = hmac.new(words, u, hashlib.sha512).digest()\n        out = bytearray(a ^ b for a, b in zip(out, u))\n    return bytes(out)\nw = b'army van defense carry jealous true garbage claim echo media make crunch'\nprint(seed(w, b'mnemonic') == seed(w, b'mnemonicSuperDuperSecret'))")
q("RecoveryPassphrase", "Analyze", "A user mistypes their passphrase during a restoration. What does the wallet show?",
  ["A valid but empty wallet, with no warning that anything is wrong",
   "An error, because the checksum covers the passphrase",
   "The right balance, since the passphrase is only a second factor",
   "A warning that the passphrase may be wrong"],
  "In BIP39 every passphrase is valid; there is no wrong one, so nothing can be detected.")
q("PlausibleDeniability", "Analyze", "Why does the chapter call plausible deniability dangerous as well as useful?",
  ["Because nothing can prove that everything has been revealed, so coercion may continue",
   "Because the second wallet is easier to brute force",
   "Because a duress wallet cannot hold any funds",
   "Because the passphrase becomes part of the checksum"],
  "The chapter states both sides: a thief who leaves may be detected, while an attacker who stays has no reason to stop.")
q("Brainwallet", "Apply", "How many bits of entropy does a uniformly chosen 12-word BIP39 code carry, counting the checksum bits?",
  ["132", "128", "121", "144"],
  "2,048 to the twelfth power is 2 to the 132, of which 128 bits are entropy and 4 are checksum.", "print((2048 ** 12).bit_length() - 1)")
q("Brainwallet", "Understand", "Why is a phrase a user invents not a recovery code?",
  ["Because humans are poor sources of randomness, so the phrase can be guessed",
   "Because the words would not be in the BIP39 list",
   "Because a user-chosen phrase has no checksum",
   "Because wallets refuse to accept typed words"],
  "The chapter's tip separates the two for exactly this reason; the wallet's randomness is what makes a code strong.")
q("Memorization", "Understand", "In which case does the chapter grant that memorising a code is a powerful feature?",
  ["When physical belongings cannot be carried without being seized or inspected",
   "When the user has no paper available",
   "When the wallet uses a passphrase",
   "When the code is shorter than twelve words"],
  "That is the one situation the chapter names; otherwise it very strongly encourages writing the code down.")
q("PhysicalCoercion", "Remember", "Which figure does the chapter cite from the list of physical attacks it points to?",
  ["Over 100 attacks, including at least three deaths",
   "Exactly 364 attacks, including seventeen deaths",
   "About a dozen attacks, with no deaths",
   "Over 1,000 attacks against exchanges"],
  "The chapter cites over 100 documented attacks; the saved copy of the list read for this course now holds 364 rows.")
q("WalletBirthday", "Apply", "Aezeed stores the wallet's age as days since the genesis block in two bytes. Which year does that reach, counting from 2009?",
  ["2188", "2096", "2265", "2041"],
  "Two bytes hold 65,536 days, which is 179 years, and 2009 plus 179 is 2188, the figure the document gives.", "print(2009 + 2 ** 16 // 365)")
q("WalletBirthday", "Understand", "What does a wallet birthday save during a restoration?",
  ["Scanning the blockchain from the beginning, because the wallet knows when to start looking",
   "Deriving the keys, because they are stored with the date",
   "Entering the passphrase, because the date replaces it",
   "Checking the checksum of the code"],
  "Without a birthday a wallet must rescan back to the genesis block, which is costly for a lightweight client.")

# ============================== 3 THE BIP39 STACK ==============================
q("Bip39Stack", "Remember", "Which three technologies make up the stack the chapter works through in detail?",
  ["BIP39 recovery codes, BIP32 key derivation and BIP44-style implicit paths",
   "BIP39 codes, SLIP39 shares and output script descriptors",
   "BIP32 derivation, BIP329 labels and Electrum version 2 codes",
   "BIP43 purposes, BIP84 paths and Aezeed seeds"],
  "The chapter names those three and says all of them date from 2014 or earlier.")
q("CodeGeneration", "Apply", "In which order are the first steps of BIP39 carried out?",
  ["Entropy, then checksum appended, then split into 11-bit groups, then words",
   "Words chosen, then entropy computed, then checksum appended",
   "Entropy, then split into 11-bit groups, then checksum appended to the words",
   "Checksum computed from the words, then entropy derived from it"],
  "The chapter's six steps run from the random sequence through the checksum to the word list.")
q("Entropy", "Apply", "How many bits of entropy are in the chapter's example input 0c1e24e5917779d297e14d45f14e1a1a?",
  ["128", "132", "256", "64"],
  "Sixteen bytes of eight bits each are the 128 bits the chapter's table labels entropy input.",
  "print(len(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a')) * 8)")
q("Entropy", "Analyze", "Why does the chapter say there is no apparent benefit to more than 128 bits of entropy?",
  ["Because the security strength of a Bitcoin public key is 128 bits",
   "Because BIP39 cannot encode more than 128 bits",
   "Because a seed is only 128 bits long",
   "Because the word list has only 2,048 words"],
  "An attacker needs about 2 to the 128 curve operations, so extra entropy in the seed buys nothing against that attack.")
q("Bip39Checksum", "Apply", "What are the four checksum bits of the chapter's 128-bit entropy, taken from the start of its SHA-256 hash?",
  ["0111", "0101", "1110", "0011"],
  "The first byte of the hash written in binary and cut to four digits is 0111.",
  "import hashlib\nprint(bin(hashlib.sha256(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a')).digest()[0])[2:].zfill(8)[:4])")
q("Bip39Checksum", "Analyze", "BIP39 calls its checksum short. What is the consequence the standard states?",
  ["About one random error in 256 is missed and no correction is possible",
   "The checksum cannot be computed without the passphrase",
   "Codes of 24 words have no checksum at all",
   "Two different codes always share a checksum"],
  "The standard lists the modest odds of catching random errors among BIP39's shortcomings.")
q("WordList", "Apply", "Why does the BIP39 word list hold exactly 2,048 words?",
  ["2048", "1024", "4096", "2000"],
  "The list holds 2 to the 11 words, so one word encodes exactly 11 bits.", "print(2 ** 11)")
q("WordList", "Understand", "Why does BIP39 strongly discourage non-English word lists?",
  ["Because the seed is derived from the words, so another list gives a different seed",
   "Because other lists have fewer than 2,048 words",
   "Because the checksum only works in English",
   "Because the standard defines no other list"],
  "The conversion hashes the sentence rather than the entropy, so translating a code changes the seed.")
q("BitSegment", "Apply", "What is the value of the first 11-bit segment of the entropy 0c1e24e5917779d297e14d45f14e1a1a?",
  ["96", "12", "1929", "423"],
  "The first eleven bits are 00001100000, which is 96, the index of the word army.",
  "b = bin(int.from_bytes(bytes.fromhex('0c1e24e5917779d297e14d45f14e1a1a'), 'big'))[2:].zfill(128)\nprint(int(b[:11], 2))")
q("BitSegment", "Analyze", "How many bits of entropy does the last word of a 12-word code carry?",
  ["7, together with the 4 checksum bits",
   "11, like every other word",
   "4, the rest being checksum",
   "0, because the last word is only a checksum"],
  "Eleven segments use 121 of the 128 entropy bits, so 7 remain and the 4 checksum bits complete the twelfth.")
q("CodeLength", "Apply", "How many words does a 256-bit BIP39 code have?",
  ["24", "21", "22", "32"],
  "256 bits plus an 8-bit checksum is 264 bits, which divided by 11 gives 24 words.", "print((256 + 256 // 32) // 11)")
q("CodeLength", "Understand", "Why do BIP39 codes grow in steps of three words?",
  ["Because the entropy is a multiple of 32 bits, so the total is a multiple of 33 bits",
   "Because the word list is sorted in groups of three",
   "Because three words are needed for the checksum",
   "Because 11 divides 3"],
  "Entropy of 32k bits plus k checksum bits is 33k bits, which 11 divides, so the word count rises by three.")
q("TextNormalization", "Apply", "How many code points does the character e with an acute accent have after compatibility decomposition?",
  ["2", "1", "3", "0"],
  "Normalisation form compatibility decomposition splits it into a plain e and a combining accent.",
  "import unicodedata\nprint(len(unicodedata.normalize('NFKD', '\\u00e9')))")
q("TextNormalization", "Understand", "Why does BIP39 require a normalisation form for its text?",
  ["So that two spellings a person cannot tell apart give the same bytes and so the same seed",
   "So that the words can be sorted",
   "So that accents can be removed from the word list",
   "So that the checksum can be computed without the list"],
  "The seed is derived by hashing the text, and a hash of different bytes is a different seed.")
q("SeedDerivation", "Remember", "Which three things does BIP39 give to its key-stretching function?",
  ["The words as the password, the constant mnemonic with the passphrase as the salt, and 2,048 iterations",
   "The entropy, the word list and the checksum",
   "The seed, the chain code and the index",
   "The passphrase as the password and the words as the salt"],
  "Those are steps seven to nine of the standard, with HMAC-SHA512 as the pseudorandom function.")
q("KeyStretchingFunction", "Apply", "Aezeed uses 32,768 rounds where BIP39 uses 2,048. How many times the work is that?",
  ["16", "8", "15", "30720"],
  "32,768 divided by 2,048 is 16 times as many rounds.", "print(32768 // 2048)")
q("KeyStretchingFunction", "Analyze", "Against which attacker does the chapter say BIP39's stretching helps least?",
  ["An attacker with special-purpose hardware",
   "An attacker who has seen half of the code",
   "An attacker guessing a whole 128-bit code",
   "An attacker with the user's passphrase"],
  "The chapter says special-purpose hardware is not significantly affected by the 2,048 rounds.")
q("Pbkdf2", "Apply", "What are the first sixteen hexadecimal digits of the seed of the chapter's twelve words with no passphrase?",
  ["5b56c417303faa3f", "3b5df16df2157104", "3269bce2674acbd1", "f1cc3bc03ef51cb4"],
  "PBKDF2 with HMAC-SHA512, the salt mnemonic and 2,048 iterations reproduces the chapter's first table.",
  "import hashlib, hmac\ndef seed(words, salt, rounds=2048):\n    u = hmac.new(words, salt + b'\\x00\\x00\\x00\\x01', hashlib.sha512).digest()\n    out = bytearray(u)\n    for _ in range(rounds - 1):\n        u = hmac.new(words, u, hashlib.sha512).digest()\n        out = bytearray(a ^ b for a, b in zip(out, u))\n    return bytes(out)\nprint(seed(b'army van defense carry jealous true garbage claim echo media make crunch', b'mnemonic').hex()[:16])")
q("Pbkdf2", "Understand", "Which function does PBKDF2 repeat 2,048 times in BIP39?",
  ["HMAC-SHA512", "SHA-256", "scrypt", "RIPEMD-160"],
  "The standard names HMAC-SHA512 as the pseudorandom function and 512 bits as the derived key length.")
q("Salt", "Apply", "What is BIP39's salt when no passphrase is used?",
  ["mnemonic", "an empty string", "the first word of the code", "eight random bytes"],
  "The salt is the constant string mnemonic, with the passphrase appended when one is used.",
  "print('mnemonic' + '')")
q("Salt", "Analyze", "A classical salt is random and stored beside the derived key. How does BIP39's salt differ?",
  ["It is a fixed constant, so every passphrase-free wallet uses the same salt",
   "It is secret, so it adds entropy to the seed",
   "It is derived from the words, so it differs per code",
   "It is eight random bytes chosen by the wallet"],
  "The protection against precomputation comes from the 128 bits in the words, not from the salt.")
q("RootSeed", "Apply", "How many bytes is the 512-bit seed BIP39 produces?",
  ["64", "32", "128", "16"],
  "512 bits divided by 8 is 64 bytes, the length of one HMAC-SHA512 output.", "print(512 // 8)")
q("RootSeed", "Analyze", "A wallet asks for a seed in hexadecimal and the user types their twelve words. Why does that fail?",
  ["The words are not the seed; the seed is the stretched output and the mapping is one-way",
   "The words are the seed, but in the wrong base",
   "The wallet needs the entropy, which the words do not encode",
   "The seed must be 256 bits and the words give 512"],
  "BIP39 notes that the conversion from a sentence to a seed is one-way only.")
q("Bip39Passphrase", "Apply", "What are the first sixteen hexadecimal digits of the seed of the same twelve words with the passphrase SuperDuperSecret?",
  ["3b5df16df2157104", "5b56c417303faa3f", "3269bce2674acbd1", "7cb305fd619db8de"],
  "Appending the passphrase to the salt gives the chapter's second table, which begins 3b5df16d.",
  "import hashlib, hmac\ndef seed(words, salt, rounds=2048):\n    u = hmac.new(words, salt + b'\\x00\\x00\\x00\\x01', hashlib.sha512).digest()\n    out = bytearray(u)\n    for _ in range(rounds - 1):\n        u = hmac.new(words, u, hashlib.sha512).digest()\n        out = bytearray(a ^ b for a, b in zip(out, u))\n    return bytes(out)\nprint(seed(b'army van defense carry jealous true garbage claim echo media make crunch', b'mnemonicSuperDuperSecret').hex()[:16])")
q("Bip39Passphrase", "Understand", "How many valid seeds can one BIP39 code produce?",
  ["As many as there are possible passphrases, since every passphrase gives a valid seed",
   "Exactly one, since the code determines the seed",
   "Two, one with and one without a passphrase",
   "None until a wallet registers the code"],
  "The chapter says every passphrase leads to a different seed and there is essentially no wrong passphrase.")
q("SecurityStrength", "Apply", "Which three numbers does the chapter's sidebar use for extended keys, private keys and the curve's strength?",
  ["[512, 256, 128]", "[256, 128, 64]", "[512, 256, 256]", "[264, 132, 128]"],
  "An extended private key holds 512 bits, a private key 256, and the public key's strength is 128 bits.",
  "print([(2 ** 512).bit_length() - 1, (2 ** 256).bit_length() - 1, (2 ** 128).bit_length() - 1])")
q("SecurityStrength", "Analyze", "What is the one benefit of more entropy the chapter names, and does it recommend relying on it?",
  ["A partly seen code is harder to complete, and no, it does not recommend relying on it",
   "Faster derivation, and yes",
   "A shorter code, and no",
   "A stronger checksum, and yes"],
  "The chapter prefers keeping codes safe or distributing them with a scheme such as SLIP39.")

# ============================== 4 HD WALLET ==============================
q("HdWallet", "Understand", "What is a hierarchical deterministic wallet?",
  ["A wallet whose keys form a tree, every node of which is computed from one seed",
   "A wallet that stores its keys in a sorted file",
   "A wallet that keeps a copy of the blockchain",
   "A wallet whose keys expire in a fixed order"],
  "The book's glossary calls it a wallet using BIP32's key creation and transfer protocol, which derives child keys from parent keys in a hierarchy.")
q("MasterKeys", "Understand", "What does the single keyed hash of the seed produce?",
  ["The master private key and the master chain code",
   "The master private key and the first address",
   "The recovery code and the seed",
   "The account key and its fingerprint"],
  "The left half of HMAC-SHA512 is the master private key and the right half is the master chain code.")
q("HmacSha512", "Apply", "What are the first sixteen hexadecimal digits of HMAC-SHA512 over BIP32's first test seed under the key 'Bitcoin seed'?",
  ["e8f32e723decf405", "873dff81c02f5256", "edb2e14f9ee77d26", "47fdacbd0f109704"],
  "That is the start of the 64-byte output whose left half becomes the master private key.",
  "import hashlib, hmac\nprint(hmac.new(b'Bitcoin seed', bytes.fromhex('000102030405060708090a0b0c0d0e0f'), hashlib.sha512).hexdigest()[:16])")
q("HmacSha512", "Understand", "Which argument of the derivation's keyed hash is the chain code?",
  ["The key, while the key material is part of the message",
   "The message, while the private key is the key",
   "Neither; the chain code is hashed separately",
   "Both, since it is used twice"],
  "BIP32 calls HMAC-SHA512 with the parent chain code as the key and the key bytes with the index as the data.")
q("MasterPrivateKey", "Apply", "How many hexadecimal digits long is the master private key read out of that hash?",
  ["64", "32", "128", "66"],
  "The left 32 bytes are 64 hexadecimal digits, read as a 256-bit number.",
  "import hashlib, hmac\nprint(len(hmac.new(b'Bitcoin seed', bytes.fromhex('000102030405060708090a0b0c0d0e0f'), hashlib.sha512).hexdigest()[:64]))")
q("MasterPrivateKey", "Analyze", "Why does the chapter recommend hardened derivation for the level-1 children of the master keys?",
  ["Because a leak below a normal child could be used to recover the master key",
   "Because level-1 keys are used most often",
   "Because the master key cannot derive normal children",
   "Because hardened keys are shorter"],
  "BIP32 gives the same reason: a leak of account-level or lower keys should never risk the master.")
q("MasterChainCode", "Apply", "What are the first sixteen hexadecimal digits of the master chain code of BIP32's first test seed?",
  ["873dff81c02f5256", "e8f32e723decf405", "47fdacbd0f109704", "0a2683ed00000000"],
  "The chain code is the right 32 bytes of the same hash, which begin 873dff81.",
  "import hashlib, hmac\nprint(hmac.new(b'Bitcoin seed', bytes.fromhex('000102030405060708090a0b0c0d0e0f'), hashlib.sha512).hexdigest()[64:][:16])")
q("MasterChainCode", "Understand", "Why is the chain code a secret even though it is not a key?",
  ["Because with a leaked child private key it reveals the other children and the parent",
   "Because it can be used to sign transactions",
   "Because it contains the seed in compressed form",
   "Because it is the same as the fingerprint"],
  "BIP32 calls this the weakness that may not be immediately obvious.")
q("ChildDerivation", "Remember", "Which of the four possible derivations does BIP32 say is not possible?",
  ["From a public parent key to a private child key",
   "From a private parent key to a public child key",
   "From a public parent key to a public child key",
   "From a private parent key to a private child key"],
  "The standard answers that case with one line: this is not possible.")
q("ChildKeyDerivation", "Apply", "The derivation hash is 512 bits. How many bits and bytes is each half?",
  ["(256, 32)", "(256, 64)", "(128, 16)", "(512, 64)"],
  "Each half is 256 bits, that is 32 bytes: one becomes key material, the other the child chain code.",
  "print((512 // 2, 512 // 2 // 8))")
q("ChildKeyDerivation", "Understand", "How is the left half of the hash turned into the child private key?",
  ["It is added to the parent private key, modulo the order of the curve",
   "It is used as the child private key directly",
   "It is multiplied by the parent private key",
   "It is hashed again with the index"],
  "BIP32 changed from multiplication to addition in 2013 for speed and ease of implementation.")
q("ChainCode", "Apply", "How many bits is a chain code?",
  ["256", "128", "512", "160"],
  "A chain code is 32 bytes, that is 256 bits, and travels beside the key.",
  "print(len(bytes.fromhex('873dff81c02f525623fd1fe5167eac3a55a049de3d314bb42ee227ffed37d508')) * 8)")
q("ChainCode", "Analyze", "A user keeps a child private key but not its chain code. What can they do?",
  ["Spend what was paid to that key, but derive no grandchildren",
   "Derive the whole branch below it",
   "Recover the parent key",
   "Nothing at all"],
  "The chapter says both the child private key and the child chain code are needed to start a new branch.")
q("IndexNumber", "Apply", "What is the first hardened index in hexadecimal?",
  ["0x80000000", "0x7fffffff", "0xffffffff", "0x00000000"],
  "Hardened indices run from 2 to the 31, which is 0x80000000, to 2 to the 32 minus 1.", "print(hex(2 ** 31))")
q("IndexNumber", "Understand", "What does the index 2 with a prime, written 2h, mean?",
  ["2 plus 2 to the 31, that is 2147483650",
   "The second hardened key of the second account",
   "2 multiplied by 2 to the 31",
   "The index 2 of a public branch"],
  "The chapter says that an index i with a prime means 2 to the 31 plus i.")
q("PrivateChildDerivation", "Apply", "Which arithmetic produces a child private key from the parent and the left half of the hash?",
  ["Addition modulo the order of the curve",
   "Multiplication modulo the order of the curve",
   "Exclusive-or of the two 32-byte values",
   "Concatenation of the two values"],
  "BIP32 says the child key is the left half plus the parent key, taken modulo n.",
  "n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141\nprint('Addition modulo the order of the curve' if (5 + 7) % n == 12 else 'no')")
q("PrivateChildDerivation", "Analyze", "The chapter writes that the derivation combines a parent key described as an uncompressed key. What do the standards do?",
  ["They serialise the parent public key in compressed form, 33 bytes",
   "They serialise it uncompressed, 65 bytes, as the chapter says",
   "They use the private key for normal derivation too",
   "They omit the parent key altogether"],
  "An executed claim of this chapter shows that the uncompressed form gives a different child key, so the chapter's parenthesis is a slip.")
q("HardenedDerivation", "Apply", "What are the first eighteen characters of the hardened child private key at m/0h of BIP32's first test vector, written in hexadecimal with its 0x prefix?",
  ["0xedb2e14f9ee77d26", "0xe8f32e723decf405", "0x3c6cb8d0f6a264c9", "0x873dff81c02f5256"],
  "Hashing a zero byte, the parent key and the index 2 to the 31, then adding the left half to the parent key, gives this key.",
  "import hashlib, hmac\nN = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141\nI = hmac.new(b'Bitcoin seed', bytes.fromhex('000102030405060708090a0b0c0d0e0f'), hashlib.sha512).digest()\nk, c = int.from_bytes(I[:32], 'big'), I[32:]\nJ = hmac.new(c, b'\\x00' + k.to_bytes(32, 'big') + (2 ** 31).to_bytes(4, 'big'), hashlib.sha512).digest()\nprint(hex((int.from_bytes(J[:32], 'big') + k) % N)[:18])")
q("HardenedDerivation", "Understand", "What does hardened derivation feed into the hash that normal derivation does not?",
  ["The parent private key, padded with a zero byte",
   "The parent public key, uncompressed",
   "The child index twice",
   "The seed"],
  "Because the message now contains a secret, no holder of the extended public key can compute it.")
q("PublicChildDerivation", "Apply", "On a small curve, is the point for a sum of two numbers the same as the sum of their points?",
  ["True", "False", "Only for hardened indices", "Only for even numbers"],
  "That identity is why a child public key can be derived from a parent public key alone.",
  "p = 97\ndef add(P, Q):\n    if P is None: return Q\n    if Q is None: return P\n    if P[0] == Q[0] and (P[1] + Q[1]) % p == 0: return None\n    m = (3 * P[0] * P[0] * pow(2 * P[1], -1, p) if P == Q else (Q[1] - P[1]) * pow(Q[0] - P[0], -1, p)) % p\n    x = (m * m - P[0] - Q[0]) % p\n    return (x, (m * (P[0] - x) - P[1]) % p)\ndef mul(n, P):\n    R = None\n    while n:\n        if n & 1: R = add(R, P)\n        P = add(P, P); n >>= 1\n    return R\nG = (1, 28)\nprint(add(mul(13, G), mul(7, G)) == mul(20, G))")
q("PublicChildDerivation", "Analyze", "Why is public derivation defined only for normal children?",
  ["Because a hardened child's hash needs the parent private key",
   "Because hardened children have no chain code",
   "Because hardened children are not on the curve",
   "Because the index would overflow 32 bits"],
  "BIP32's public derivation function returns failure for an index of 2 to the 31 or more.")
q("ChildKeyIndependence", "Apply", "How many other normal children does a parent key have, besides any one of them?",
  ["2147483647", "2147483648", "4294967295", "2147483646"],
  "There are 2 to the 31 normal children, so any one of them has 2 to the 31 minus 1 siblings.", "print(2 ** 31 - 1)")
q("ChildKeyIndependence", "Understand", "What can a child private key on its own be used for?",
  ["Making its public key and address and signing to spend what was paid there",
   "Deriving its siblings",
   "Recovering its parent key",
   "Deriving its own children"],
  "The chapter answers its own question: a public key, an address and signatures, and nothing else.")
q("ExtendedKeys", "Understand", "What are the two parts of an extended key?",
  ["A key and its chain code", "A public key and a private key", "A key and its index", "A key and its fingerprint"],
  "The chapter calls the key and the chain code the two essential ingredients, stored as the two concatenated.")
q("ExtendedKey", "Apply", "How many bytes is BIP32's serialised extended key before the checksum is added?",
  ["78", "74", "82", "64"],
  "Four version, one depth, four fingerprint, four child number, 32 chain code and 33 key bytes make 78.",
  "print(4 + 1 + 4 + 4 + 32 + 33)")
q("ExtendedKey", "Analyze", "Why are the private and public serialised forms the same length?",
  ["Because the private key is padded with a leading zero byte to the 33 bytes of a compressed public key",
   "Because the chain code is omitted from the private form",
   "Because both carry two keys",
   "Because the checksum differs in length"],
  "BIP32 prescribes 33 bytes of key data in both cases.")
q("ExtendedPrivateKey", "Apply", "Which version bytes does the chapter's example extended private key carry?",
  ["0488ade4", "0488b21e", "043587cf", "04b2430c"],
  "Decoding the string shows the mainnet private version bytes, which produce the prefix xprv.",
  "import hashlib\nB58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\nt = 'xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9c'\nn = 0\nfor ch in t: n = n * 58 + B58.index(ch)\nprint(n.to_bytes(82, 'big')[:4].hex())")
q("ExtendedPrivateKey", "Analyze", "The chapter's example xprv has depth 1 and a non-zero parent fingerprint. What does that tell a reader?",
  ["It is a level-1 child, not a master key",
   "It is a master key with a random fingerprint",
   "It belongs to a testnet wallet",
   "It carries no chain code"],
  "A master node has depth zero and a parent fingerprint of four zero bytes.")
q("ExtendedPublicKey", "Apply", "How many characters long is a mainnet extended key in base58check?",
  ["111", "112", "108", "128"],
  "BIP32 says the encoding is exactly 111 characters.",
  "print(len('xpub67xpozcx8pe95XVuZLHXZeG6XWXHpGq6Qv5cmNfi7cS5mtjJ2tgypeQbBs2UAR6KECeeMVKZBPLrtJunSDMstweyLXhRgPxdp14sk9tJPW9'))")
q("ExtendedPublicKey", "Analyze", "A merchant gives an auditor the account's extended public key. What has the auditor gained?",
  ["Sight of every payment of that account, in and out, and no power to spend",
   "The power to spend from the account",
   "Sight of the receiving addresses only",
   "Nothing, since the key is public"],
  "BIP32 lists audits among its use cases for exactly this sharing.")
q("ExtendedKeyEncoding", "Apply", "Which version bytes does the chapter's example extended public key carry?",
  ["0488b21e", "0488ade4", "04b24746", "049d7cb2"],
  "The mainnet public version bytes produce the prefix xpub.",
  "import hashlib\nB58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'\nt = 'xpub67xpozcx8pe95XVuZLHXZeG6XWXHpGq6Qv5cmNfi7cS5mtjJ2tgypeQbBs2UAR6KECeeMVKZBPLrtJunSDMstweyLXhRgPxdp14sk9tJPW9'\nn = 0\nfor ch in t: n = n * 58 + B58.index(ch)\nprint(n.to_bytes(82, 'big')[:4].hex())")
q("ExtendedKeyEncoding", "Understand", "Why do BIP43 and BIP380 argue against prefixes such as zpub?",
  ["Because the script type should not be carried by the key's version bytes",
   "Because base58check cannot encode them",
   "Because they make the string longer",
   "Because they are not registered with any standard"],
  "BIP380 calls it a layer violation: key derivation should be separate from script type meaning.")
q("KeyFingerprint", "Apply", "How many bits is a key fingerprint?",
  ["32", "160", "64", "8"],
  "It is the first 32 bits, that is four bytes, of the 160-bit identifier of an extended key.", "print(len('0a2683ed') * 4)")
q("KeyFingerprint", "Analyze", "Why does BIP32 say software must be willing to deal with collisions of fingerprints?",
  ["Because four bytes are not an identity, only a fast lookup hint",
   "Because the fingerprint is random rather than derived",
   "Because two keys may share a chain code",
   "Because the fingerprint of a master key is always zero"],
  "The standard adds that the full 160-bit identifier could be used internally.")
q("TreeNavigation", "Understand", "What problem do BIP43 and BIP44 solve that BIP32 leaves open?",
  ["They fix what the levels of the tree mean, so wallets can read each other's trees",
   "They make the derivation function faster",
   "They add a checksum to the path",
   "They allow deeper trees"],
  "BIP43 says BIP32 offers implementers too many degrees of freedom.")
q("KeyPath", "Apply", "What are the five indices of the path m/84h/0h/0h/0/2?",
  ["[2147483732, 2147483648, 2147483648, 0, 2]",
   "[84, 0, 0, 0, 2]",
   "[2147483732, 2147483648, 2147483648, 2147483648, 2]",
   "[2147483648, 2147483732, 2147483648, 0, 2]"],
  "The three hardened steps add 2 to the 31 to 84, 0 and 0; the last two are normal.",
  "print([int(p.rstrip('h')) + (2 ** 31 if p.endswith('h') else 0) for p in 'm/84h/0h/0h/0/2'.split('/')[1:]])")
q("KeyPath", "Understand", "What does the capital M at the head of a path mean?",
  ["The key named is the public key of that position",
   "The path belongs to a different tree",
   "Every step of the path is hardened",
   "The path names a master key"],
  "Private keys derived from m are written m/..., public keys from M are written M/...")
q("Bip43Purpose", "Apply", "What is the purpose index of BIP44 in hexadecimal?",
  ["0x8000002c", "0x0000002c", "0x80000031", "0x8000002b"],
  "BIP43 gives 44 with a prime, or 0x8000002C, as the purpose for BIP44.", "print(hex(2 ** 31 + 44))")
q("Bip43Purpose", "Understand", "Why is the purpose level hardened?",
  ["So that nothing above it can be reached from a shared extended public key",
   "So that the number can exceed 2 to the 31",
   "So that the purpose can be read from an xpub",
   "So that the level can be skipped"],
  "BIP43's pattern is m / purpose' / , and the apostrophe marks hardened derivation.")
q("Bip44Structure", "Apply", "How many levels does BIP44 define below the master key?",
  ["5", "4", "6", "3"],
  "Purpose, coin type, account, change and address index make five.",
  "print(len('m / purpose / coin_type / account / change / address_index'.split(' / ')) - 1)")
q("Bip44Structure", "Analyze", "Which levels of a BIP44 path are hardened and which are not?",
  ["Purpose, coin type and account are hardened; change and index are not",
   "All five are hardened",
   "Only the purpose is hardened",
   "Change and index are hardened; the first three are not"],
  "The change level uses normal derivation so that an account's extended public key can be exported.")
q("AccountBranch", "Apply", "What is the path of the second Bitcoin account of a BIP44 wallet?",
  ["m/44h/0h/1h", "m/44h/1h/0h", "m/44h/0h/2h", "m/44h/0h/1"],
  "Accounts are numbered from zero at the third level, so the second account is index 1, hardened.", "print('m/44h/0h/%dh' % 1)")
q("AccountBranch", "Understand", "What does BIP44 say an account level is for?",
  ["Splitting the key space into independent identities that never mix coins",
   "Separating one currency from another",
   "Separating receiving from change addresses",
   "Numbering the addresses of a wallet"],
  "Coin type separates currencies, the change level separates receiving from change, and the index numbers addresses.")
q("ChangeBranch", "Apply", "Which path is the fifteenth change address of the fourth Bitcoin account, as a public key?",
  ["M/44h/0h/3h/1/14", "M/44h/0h/4h/1/15", "M/44h/0h/3h/0/14", "m/44h/0h/3h/1/14"],
  "Accounts and indices count from zero and the change branch is 1, which is the chapter's own table row.",
  "print('M/44h/0h/%dh/%d/%d' % (3, 1, 14))")
q("ChangeBranch", "Understand", "Which constant does BIP44 use for the external chain?",
  ["0", "1", "2", "44"],
  "0 is the external chain, whose addresses are given out, and 1 is the internal chain for change.")
q("AddressIndex", "Apply", "Which path is the third receiving address of the primary Bitcoin account, as a public key?",
  ["M/44h/0h/0h/0/2", "M/44h/0h/0h/0/3", "M/44h/0h/0h/1/2", "m/44h/0h/0h/0/2"],
  "Indices count from zero, so the third address is index 2 of the external branch.", "print('M/44h/0h/0h/0/%d' % (3 - 1))")
q("AddressIndex", "Analyze", "Why can a restored wallet not tell how far the address index had advanced?",
  ["Because nothing in an address shows its position, so the wallet must scan and guess",
   "Because the index is stored only on the blockchain",
   "Because the index is hardened",
   "Because indices are random rather than sequential"],
  "This is why scanning stops after a run of unused indices, which is the gap limit.")

# ============================== 5 PATH BACKUP ==============================
q("PathBackup", "Understand", "Why is a recovery code alone not always enough to recover a wallet?",
  ["Because it does not say which paths of the tree the wallet used",
   "Because it does not contain the seed",
   "Because the keys expire",
   "Because the checksum cannot be verified without the wallet"],
  "The tree is too large to search, so the paths must be standard or recorded.")
q("PathConventions", "Analyze", "Which kind of wallet does the chapter say increasingly uses explicit paths?",
  ["Wallets for multiple signatures or other advanced scripts",
   "Wallets for single signatures only",
   "Lightweight clients",
   "Wallets without a recovery code"],
  "Single-signature wallets have long used implicit paths; advanced scripts need descriptors.")
q("ImplicitPath", "Understand", "What is an implicit path?",
  ["A standardised path a wallet uses without being told, so nothing has to be recorded",
   "A path the user writes down with the recovery code",
   "A path derived from the user's passphrase",
   "A path chosen at random by the wallet"],
  "BIP44, BIP49, BIP84 and BIP86 each define one, which is why a code alone often suffices.")
q("ImplicitPath", "Analyze", "What is the disadvantage of implicit paths the chapter names?",
  ["A wallet must derive and scan every path it supports, which is wasteful and still may miss funds",
   "They require the user to keep extra information",
   "They cannot be used with a passphrase",
   "They only work for multisignature wallets"],
  "The chapter calls their inflexibility the disadvantage, with the version-number problem as its sharpest form.")
q("ExplicitPath", "Understand", "What does the chapter say almost all wallets with explicit paths use to record them?",
  ["Output script descriptors", "A text file of paths", "BIP329 label exports", "The extended key's version bytes"],
  "The chapter names BIPs 380 to 386 and 389, the descriptor standards.")
q("ExplicitPath", "Analyze", "What does the chapter say the extra information of an explicit path costs?",
  ["It must be backed up, and although it rarely compromises security it can reduce privacy",
   "It must be kept as secret as the recovery code",
   "It makes the recovery code longer",
   "It prevents the use of standard paths"],
  "A descriptor holds public data, so it needs some protection but not the protection of a seed.")
q("StandardPath44", "Apply", "Which account path does BIP44 define for pay-to-public-key-hash keys?",
  ["m/44h/0h/0h", "m/44h/1h/0h", "m/0h/44h/0h", "m/44h/0h/0h/0"],
  "The chapter's table gives m/44'/0'/0' for P2PKH, which it calls a legacy address.", "print('m/%dh/0h/0h' % 44)")
q("StandardPath44", "Understand", "What does the chapter call the address type of the BIP44 path?",
  ["A legacy address", "A segwit address", "A taproot address", "A nested segwit address"],
  "Pay-to-public-key-hash is the legacy form that chapter 4 of the book described.")
q("StandardPath49", "Apply", "What is BIP49's purpose index in hexadecimal?",
  ["0x80000031", "0x8000002c", "0x80000054", "0x80000049"],
  "49 hardened is 2 to the 31 plus 49, which is 0x80000031.", "print(hex(2 ** 31 + 49))")
q("StandardPath49", "Analyze", "Why did BIP49 give nested segwit its own account rather than adding addresses to a BIP44 account?",
  ["So that an incompatible wallet finds nothing instead of finding part of the funds",
   "So that the addresses would be shorter",
   "Because BIP44 accounts were already full",
   "Because nested segwit needs a different curve"],
  "The standard says its approach fails in a more visible way: either the account shows up or it does not at all.")
q("StandardPath84", "Apply", "What is the first receiving address of BIP84's test vector?",
  ["bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu",
   "bc1qnjg0jd8228aq7egyzacy8cys3knf9xvrerkf9g",
   "bc1q8c6fshw2dlwun7ekn9qwf37cu2rn755upcp6el",
   "2Mww8dCYPUpKHofjgcXcBCEGmniw9CoaiD2"],
  "Encoding the key hash of the vector's first public key as bech32 gives the address the standard prints.",
  "CHARSET = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'\ndef polymod(values):\n    gen = (0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3); chk = 1\n    for v in values:\n        top = chk >> 25; chk = (chk & 0x1ffffff) << 5 ^ v\n        for i in range(5): chk ^= gen[i] if (top >> i) & 1 else 0\n    return chk\ndef convertbits(data):\n    acc = bits = 0; out = []\n    for v in data:\n        acc = (acc << 8) | v; bits += 8\n        while bits >= 5: bits -= 5; out.append((acc >> bits) & 31)\n    return out\ndata = [0] + convertbits(bytes.fromhex('c0cebcd6c3d3ca8c75dc5ec62ebe55330ef910e2'))\nvalues = [ord(c) >> 5 for c in 'bc'] + [0] + [ord(c) & 31 for c in 'bc'] + data\npm = polymod(values + [0] * 6) ^ 1\nprint('bc1' + ''.join(CHARSET[d] for d in data + [(pm >> 5 * (5 - i)) & 31 for i in range(6)]))")
q("StandardPath84", "Understand", "Which script type does the BIP84 path belong to?",
  ["Native pay-to-witness-public-key-hash", "Nested pay-to-witness-public-key-hash", "Pay-to-public-key-hash", "Single-key pay-to-taproot"],
  "The chapter's table gives m/84'/0'/0' for P2WPKH, the bech32 addresses that begin bc1q.")
q("StandardPath86", "Apply", "What are the first sixteen hexadecimal digits of the taproot tweak of BIP86's test vector internal key?",
  ["2ca01ed85cf6b652", "a60869f0dbcf1dc6", "cc8a4bc64d897bdd", "5120a60869f0dbcf"],
  "The tagged hash of the internal key under the tag TapTweak begins 2ca01ed8.",
  "import hashlib\ntag = hashlib.sha256(b'TapTweak').digest()\nprint(hashlib.sha256(tag + tag + bytes.fromhex('cc8a4bc64d897bddc5fbc2f670f7a8ba0b386779106cf1223c6fc5d7cd6fc115')).hexdigest()[:16])")
q("StandardPath86", "Analyze", "Why does BIP86 exist, given that descriptors can record paths explicitly?",
  ["Because many wallets and signers still back up only a seed, with no path or script information",
   "Because taproot keys cannot appear in a descriptor",
   "Because BIP84 paths cannot be hardened",
   "Because taproot needs a different word list"],
  "The standard says so in its own motivation, while granting that descriptors obviate fixed paths.")
q("Multisignature", "Apply", "In how many ways can two of three signers meet a two-of-three condition?",
  ["3", "2", "6", "9"],
  "There are three pairs out of three keys, which is the number of combinations of three taken two at a time.",
  "import math\nprint(math.comb(3, 2))")
q("Multisignature", "Analyze", "Why can a two-of-three participant not restore the arrangement from their own seed alone?",
  ["Because they need the other two public keys to recognise the joint funds",
   "Because their own key is not derived from their seed",
   "Because the funds are held by the other two",
   "Because the threshold is stored on the blockchain"],
  "The chapter's Alice, Bob and Carol example is the reason implicit paths are not enough.")
q("Descriptors", "Understand", "What does a descriptor describe?",
  ["A set of output scripts together with the keys or key paths used with them",
   "A wallet's balance and transaction history",
   "The recovery code of a wallet",
   "The blocks a wallet has scanned"],
  "BIP380 calls descriptors a simple language for describing collections of output scripts.")
q("OutputScript", "Apply", "How many bytes is a native segwit output script, a zero, a push of twenty and a twenty-byte key hash?",
  ["22", "20", "25", "21"],
  "Two bytes of prefix and twenty of key hash make 22.", "print(len(bytes.fromhex('0014' + 'c0cebcd6c3d3ca8c75dc5ec62ebe55330ef910e2')))")
q("OutputScript", "Understand", "Why does BIP380 say that private keys alone are an insufficient backup?",
  ["Because a restored wallet cannot know which kinds of output script and address to produce",
   "Because private keys cannot be written as words",
   "Because keys expire with each soft fork",
   "Because output scripts contain the keys"],
  "That is the standard's own motivation, sharpened by the arrival of segregated witness.")
q("OutputScriptDescriptor", "Apply", "What is the function name at the start of the descriptor wpkh([6d8c4b8f/84h/0h/0h]xpub.../0/*)?",
  ["wpkh", "pkh", "sh", "tr"],
  "The function names the script type; wpkh is a native segwit key hash output.",
  "d = 'wpkh([6d8c4b8f/84h/0h/0h]xpub.../0/*)'\nprint(d[:d.index('(')])")
q("OutputScriptDescriptor", "Analyze", "Which part of a descriptor says that the scripts form a whole family rather than one script?",
  ["The final wildcard after the key's path",
   "The eight-character checksum",
   "The bracketed key origin",
   "The function name"],
  "A ranged descriptor ends in a star, and Bitcoin Core reports such a descriptor as ranged with a range of indices.")
q("DescriptorChecksum", "Apply", "How many characters is a descriptor checksum?",
  ["8", "6", "4", "13"],
  "A descriptor ends in a hash sign and eight characters of the bech32 alphabet.",
  "print(len('raw(deadbeef)#89f8spxm'.split('#')[1]))")
q("DescriptorChecksum", "Understand", "What does BIP380 guarantee about one symbol error in a descriptor?",
  ["It is always detected", "It is always corrected", "It is detected in short descriptors only", "It is undetectable"],
  "Any one symbol error is always detected, and two or three in a descriptor of ordinary length as well.")
q("KeyOrigin", "Apply", "What are the fingerprint and the path of the key origin [6d8c4b8f/84h/0h/0h]?",
  ["('6d8c4b8f', [84, 0, 0])", "('6d8c4b8f', [2147483732, 0, 0])", "('84h', [6, 8, 13])", "('6d8c4b8f', [])"],
  "The bracket holds eight hexadecimal characters of fingerprint and the path from the master key to the key that follows.",
  "import re\nd = 'wpkh([6d8c4b8f/84h/0h/0h]xpub.../0/*)'\nm = re.search(r\"\\[([0-9a-f]{8})((?:/[0-9]+[h'])*)\\]\", d)\nprint((m.group(1), [int(p.rstrip(\"h'\")) for p in m.group(2).split('/')[1:]]))")
q("KeyOrigin", "Understand", "Whose key does the fingerprint in a key origin identify?",
  ["The master key where the derivation starts",
   "The key that follows the bracket",
   "The wallet application",
   "The first address of the branch"],
  "BIP380 says it is the fingerprint of the key where the derivation starts, so descriptors from one seed share it.")
q("MultipathDescriptor", "Apply", "Into how many descriptors does a multipath element of two values expand?",
  ["2", "1", "4", "3"],
  "A tuple of two values stands for the receive and the change descriptor.",
  "d = 'wpkh([6d8c4b8f/84h/0h/0h]xpub.../<0;1>/*)'\nhead, rest = d.split('<')\nchoices, tail = rest.split('>')\nprint(len([head + c + tail for c in choices.split(';')]))")
q("MultipathDescriptor", "Understand", "Why does BIP389 exist?",
  ["Because a wallet's receive and change descriptors differ in only one derivation step",
   "Because descriptors could not express hardened paths",
   "Because checksums had to cover several descriptors",
   "Because wallets needed more than two branches"],
  "The standard says it is useful to write both as one descriptor with a tuple in that step.")
q("Miniscript", "Apply", "A decaying policy starts as four of four and loses one signer at each of three later heights. Which thresholds does it pass through?",
  ["[4, 3, 2, 1]", "[4, 3, 2]", "[1, 2, 3, 4]", "[4, 4, 4, 4]"],
  "Bitcoin Core's documentation describes exactly that decay, from four-of-four to one-of-four.",
  "print([4 - i for i in range(4)])")
q("Miniscript", "Understand", "What is miniscript for?",
  ["Writing a subset of Bitcoin scripts in a structured way that can be analysed and signed for",
   "Compressing descriptors so they fit on paper",
   "Encoding a seed as words",
   "Replacing the derivation function of BIP32"],
  "Its specification lists the questions about raw script that are otherwise hard to answer.")

# ============================== 6 NON-KEY BACKUP ==============================
q("NonkeyBackup", "Understand", "What does the chapter say a seed-only restoration shows of a user's history?",
  ["A list of approximate times and amounts with no descriptions",
   "Nothing at all until the labels are imported",
   "The full history, since labels are on the blockchain",
   "Only the payments the user received"],
  "The chapter compares it with a bank statement whose description field is blank.")
q("WalletNotes", "Understand", "Why are labels private in a way keys are not?",
  ["Because they are stored only in the user's own wallet and never shared with the network",
   "Because they are encrypted by the seed",
   "Because the blockchain stores them in hashed form",
   "Because only the wallet application can read them"],
  "The chapter notes that this protects privacy and keeps personal data off the blockchain, and is why they are easy to lose.")
q("AddressLabel", "Understand", "Why does Bob label an address when he sends Alice an invoice?",
  ["So that he can tell her payment apart from the others he receives",
   "So that Alice can find the address again",
   "So that the network can route the payment",
   "So that the address can be reused safely"],
  "The label is a private note on his own address, which is the bookkeeping that fresh addresses require.")
q("TransactionLabel", "Apply", "Alice's history shows a receipt of 0.00100 and a payment of 0.00075 bitcoin. What is left?",
  ["0.00025", "0.00175", "0.0025", "0.00075"],
  "The two rows of the chapter's table leave 0.00025 bitcoin.", "print(round(0.00100 - 0.00075, 5))")
q("TransactionLabel", "Understand", "Which field of a Bitcoin transaction holds the user's description of it?",
  ["None; the description exists only in the wallet",
   "The label field of the output",
   "The memo field of the input",
   "The coinbase field"],
  "The chapter notes that the only metadata a receiver chooses are the amount and the address.")
q("LabelExportFormat", "Apply", "Which three keys does a BIP329 address record carry, in alphabetical order?",
  ["label, ref, type", "address, name, date", "type, value, origin", "ref, amount, label"],
  "Each line is a JSON object with a type, a reference and, optionally, a label, an origin or a spendable flag.",
  "import json\nprint(', '.join(sorted(json.loads(json.dumps({'type': 'addr', 'ref': 'bc1q', 'label': 'Bob'})))))")
q("LabelExportFormat", "Understand", "Why does BIP329 use one JSON object per line?",
  ["So that a document can be split or streamed and one bad line cannot invalidate the import",
   "So that labels can be sorted alphabetically",
   "So that the file can be encrypted line by line",
   "So that the file is smaller than JSON"],
  "The standard chooses the JSON lines format for exactly those reasons.")
q("OtherProtocolData", "Analyze", "Why is losing a Lightning wallet's data worse than losing a Bitcoin wallet's labels?",
  ["Because the other party may be able to take the funds of the channel",
   "Because the keys cannot be derived from the seed",
   "Because the channel's funds are not on the blockchain at all",
   "Because the recovery code changes with every payment"],
  "The chapter warns that a node which realises data has been lost may be able to steal bitcoins.")
q("LightningNetwork", "Understand", "Where do a Lightning channel's funds sit?",
  ["In an output that both parties must sign to spend",
   "In a wallet file on each party's computer",
   "In a separate blockchain",
   "In an output only the channel's opener controls"],
  "The lnd documentation describes off-chain funds as living in a two-of-two multisignature output.")
q("StaticChannelBackup", "Understand", "Why is a static channel backup called static?",
  ["Because it is taken once, when the channel is created, and holds until the channel closes",
   "Because it never changes the channel's balance",
   "Because it is stored on the blockchain",
   "Because it cannot be encrypted"],
  "The document contrasts it with copying the channel database, where one never knows if the state is the latest.")
q("StaticChannelBackup", "Analyze", "What does a static channel backup let a user recover?",
  ["The funds fully settled in the channel, not those in payments still in flight",
   "Every payment the channel ever routed",
   "The channel itself, which reopens automatically",
   "Nothing without the other party's backup"],
  "The backup is made when the channel is created, so it cannot describe later payments.")
q("Encryption", "Apply", "A note is combined with a key derived from a seed and then combined with it again. What comes back?",
  ["Paid Bob for podcast", "An error", "Random bytes", "An empty string"],
  "Applying the same exclusive-or twice returns the original text, which is the shape of a decryption.",
  "import hashlib\nkey = hashlib.sha256(bytes.fromhex('5b56c417303faa3f') + b'backup').digest()\nnote = b'Paid Bob for podcast'\nhidden = bytes(a ^ b for a, b in zip(note, key))\nprint(bytes(a ^ b for a, b in zip(hidden, key)).decode())")
q("Encryption", "Understand", "Why can an encrypted backup be stored on a computer the user does not trust?",
  ["Because only someone who can generate the seed can open it",
   "Because the file is signed by the wallet",
   "Because the storage provider cannot copy it",
   "Because the backup holds no keys"],
  "The chapter says this makes cloud hosting or even random network peers safe places for the file.")
q("EncryptedWalletBackup", "Apply", "What are the first eight hexadecimal digits of a backup key derived by hashing a seed prefix with the purpose string backup?",
  ["8d9a0a67", "5b56c417", "ddfb6303", "47fdacbd"],
  "The derivation is one hash, so the key need never be stored: it is recomputed from the seed.",
  "import hashlib\nprint(hashlib.sha256(bytes.fromhex('5b56c417303faa3f') + b'backup').hexdigest()[:8])")
q("EncryptedWalletBackup", "Analyze", "What does an encrypted wallet backup concentrate on the seed?",
  ["The user's whole history and labels as well as their money",
   "Only the keys, as before",
   "Only the labels, since the keys are derived anyway",
   "Nothing extra, because the backup is public data"],
  "A leaked seed now exposes the transaction history too, which is a privacy loss on top of a financial one.")

# ============================== 7 WALLET DEPLOYMENT ==============================
q("WalletDeployment", "Understand", "What does the chapter's web store example demonstrate?",
  ["That a server can give out fresh addresses while holding no power to spend",
   "That a shop must preload addresses from a secure server",
   "That hardware devices can export private keys",
   "That a single address is enough for a small shop"],
  "Gabriel loads an extended public key, which derives addresses and cannot spend.")
q("WebStore", "Analyze", "What problem did Gabriel have before he used an extended public key?",
  ["All orders paid one address, so orders and payments could not be matched",
   "His wallet ran out of keys",
   "His customers could not reach his server",
   "His hardware device refused to export keys"],
  "The chapter adds that it also weakened the privacy of Gabriel, his clients and the people he paid.")
q("XpubDeployment", "Apply", "Which three paths does a server derive for the first three orders of a BIP84 account's receive branch?",
  ["['M/84h/0h/0h/0/0', 'M/84h/0h/0h/0/1', 'M/84h/0h/0h/0/2']",
   "['M/84h/0h/0h/1/0', 'M/84h/0h/0h/1/1', 'M/84h/0h/0h/1/2']",
   "['M/84h/0h/0h/0/1', 'M/84h/0h/0h/0/2', 'M/84h/0h/0h/0/3']",
   "['m/84h/0h/0h/0/0', 'm/84h/0h/0h/0/1', 'm/84h/0h/0h/0/2']"],
  "The receive branch is 0 and indices count from zero; the capital M marks public derivation.",
  "print(['M/84h/0h/0h/0/%d' % i for i in range(3)])")
q("XpubDeployment", "Analyze", "A shop's server is taken over. What does the chapter say the attacker can and cannot steal?",
  ["Future payments only, not those already received",
   "Everything the account ever received",
   "Nothing, because the key is public",
   "The account's private keys"],
  "The server holds no private keys, so past funds are out of reach.")
q("GapLimit", "Apply", "A branch received payments at the indices 0, 3 and 25. Which does a scan with a gap limit of 20 find, and where does it stop?",
  ["([0, 3], 24)", "([0, 3, 25], 46)", "([0, 3], 20)", "([0, 3, 25], 24)"],
  "After index 3 the scan sees twenty unused indices and stops at 24, missing the payment at 25.",
  "used = {0, 3, 25}\nfound = []; run = 0; i = 0\nwhile run < 20:\n    if i in used: found.append(i); run = 0\n    else: run += 1\n    i += 1\nprint((found, i))")
q("GapLimit", "Analyze", "Which of the three choices for a wallet at its gap limit keeps privacy but risks a restoration?",
  ["Generating keys beyond the limit",
   "Refusing further requests",
   "Handing out keys it has already given away",
   "Lowering the limit"],
  "Other software with the same extended public key will not see payments received after the extended gap.")
q("PaymentProcessor", "Understand", "What does BTCPay Server describe itself as?",
  ["A free and open-source, self-hosted Bitcoin payment processor",
   "A custodial payment provider with low fees",
   "A hardware signing device",
   "A wallet application for phones"],
  "The chapter names it as the kind of software Gabriel's extended public key is loaded into.")
q("OfflineKeys", "Understand", "What stays online in the chapter's cold-storage arrangement?",
  ["The extended public key", "The extended private key", "The recovery code", "Nothing at all"],
  "The private side is on paper or a device; the public side creates receive addresses at will.")
q("ColdStorage", "Understand", "What does the book's glossary mean by cold storage?",
  ["Keeping a reserve of bitcoin offline, with keys created and stored in a secure offline environment",
   "Keeping a wallet file in an encrypted archive",
   "Keeping the seed in a bank's safe deposit box only",
   "Keeping a node switched off between payments"],
  "The glossary adds that online computers are vulnerable and should not hold a significant amount.")
q("HardwareSigningDevice", "Understand", "Why does the chapter call hardware wallet a confusing name for a signing device?",
  ["Because the device holds keys and signs, while the wallet is the database and the application",
   "Because the device cannot hold a wallet file",
   "Because the device is not hardware",
   "Because the name belongs to a trademark"],
  "The chapter's first branch separates the database, the application and the device for this reason.")
q("HardwareSigningDevice", "Analyze", "What does the chapter say most hardware signing devices will never do?",
  ["Export private keys", "Export public keys", "Sign more than one transaction", "Derive hardened children"],
  "Gabriel exports an extended public key from his device; the private keys always remain on it.")
q("WrittenBackup", "Apply", "The same 128 bits are printed as hexadecimal digits and as words. How many of each?",
  ["(32, 12)", "(16, 12)", "(32, 24)", "(64, 12)"],
  "Thirty-two hexadecimal digits against twelve English words, which is the comparison the chapter prints.",
  "print((len('0c1e24e5917779d297e14d45f14e1a1a'), len('army van defense carry jealous true garbage claim echo media make crunch'.split())))")
q("WrittenBackup", "Understand", "What does the chapter very strongly encourage, even for codes designed to be memorised?",
  ["Writing the code down", "Memorising it twice", "Splitting it with SLIP39", "Adding a passphrase"],
  "Memory fails, cannot be inherited and can be coerced, so paper is recommended beside it.")

# ============================== 8 FOUNDATIONS ==============================
q("Foundations", "Understand", "Why does this chapter define the hash function, the SHA family, the signature and secret sharing itself?",
  ["Because its explanations use them and no earlier chapter of the course defines them",
   "Because the standards require them to be redefined",
   "Because the earlier chapters' definitions are wrong",
   "Because the page needs one concept per agent"],
  "An audit of the terms used found them relied on without a concept of their own.")
q("CryptographicPrimitives", "Understand", "Which property of the hash function makes a child key useless for finding its parent?",
  ["That it cannot be run backwards", "That it is keyed", "That its output is 512 bits", "That it is repeatable"],
  "Repeatability makes a seed a backup; the one-way direction is what protects the parent.")
q("HashFunction", "Apply", "What are the first eight hexadecimal digits of the SHA-256 hash of the three letters abc?",
  ["ba7816bf", "248d6a61", "a665a459", "ddaf35a1"],
  "That is the standard's own best-known test value for SHA-256.",
  "import hashlib\nprint(hashlib.sha256(b'abc').hexdigest()[:8])")
q("HashFunction", "Understand", "Which two properties of a hash function does the chapter name when it introduces deterministic key generation?",
  ["The same input always gives the same output, and a changed input gives an unpredictable one",
   "The output is shorter than the input, and collisions are impossible",
   "It can be reversed with the key, and it is fast",
   "It is keyed, and its output is 512 bits long"],
  "Those two sentences are the whole basis of deterministic derivation.")
q("ShaAlgorithm", "Apply", "How many bytes do SHA-256 and SHA-512 produce?",
  ["(32, 64)", "(64, 128)", "(16, 32)", "(256, 512)"],
  "256 and 512 bits are 32 and 64 bytes, which fixes the sizes of a chain code and of a BIP39 seed.",
  "import hashlib\nprint((len(hashlib.sha256(b'').digest()), len(hashlib.sha512(b'').digest())))")
q("ShaAlgorithm", "Analyze", "Why is a BIP32 chain code 32 bytes and a BIP39 seed 64?",
  ["Because HMAC-SHA512 produces 64 bytes, which BIP32 splits in half and BIP39 keeps whole",
   "Because the standards chose round decimal numbers",
   "Because a chain code is half a private key",
   "Because base58check can encode no more"],
  "The choice of hash function fixes every one of those sizes.")
q("DigitalSignature", "Understand", "What does a digital signature prove?",
  ["That the holder of the private key authorised that particular message",
   "That the message was encrypted",
   "That the public key is valid",
   "That the transaction has been confirmed"],
  "The keys of the whole chapter exist to produce signatures, which is why losing one loses the ability to spend.")
q("SecretSharing", "Apply", "Five shares are made of a secret with a threshold of three. Do any three of them recover it, and do two?",
  ["Three recover it and two do not",
   "Any two recover it",
   "All five are needed",
   "Only the first three recover it"],
  "Any threshold-many points define the polynomial; fewer leave every candidate possible.",
  "prime = 2 ** 127 - 1\nsecret, coeffs = 123456789, [11, 22]\nshares = [(x, (secret + coeffs[0] * x + coeffs[1] * x * x) % prime) for x in (1, 2, 3, 4, 5)]\ndef combine(points):\n    total = 0\n    for j, (xj, yj) in enumerate(points):\n        num = den = 1\n        for m, (xm, _) in enumerate(points):\n            if m != j: num = num * (-xm) % prime; den = den * (xj - xm) % prime\n        total = (total + yj * num * pow(den, -1, prime)) % prime\n    return total\nprint('Three recover it and two do not' if combine(shares[2:5]) == secret and combine(shares[:2]) != secret else 'no')")
q("SecretSharing", "Understand", "Which two schemes of this chapter are built on secret sharing?",
  ["SLIP39 and codex32", "BIP39 and Aezeed", "Muun and Electrum version 2", "BIP32 and BIP44"],
  "Both split one secret into shares with a threshold; codex32 adds hand computation.")
q("RecoveryPractice", "Analyze", "What does the chapter name as perhaps the leading cause of lost bitcoins?",
  ["Data loss", "Theft by hackers", "Exchange failures", "Software bugs"],
  "Its closing paragraph says many people focus on theft while data loss may be the leading cause.")
q("DataLoss", "Understand", "Why can nobody reverse a data loss in Bitcoin?",
  ["Because no authority can reissue a key or undo a payment",
   "Because the blockchain deletes unspendable outputs",
   "Because the keys are stored only on the user's device",
   "Because wallets refuse to reissue addresses"],
  "The chapter says plainly that nobody can get the bitcoins back for you.")
q("BackupTesting", "Understand", "What does the chapter ask a reader to do regularly?",
  ["Test their backups", "Change their recovery code", "Move their funds to new addresses", "Export their labels"],
  "Its last sentence is that it is up to the reader to make good backups and regularly test them.")
q("BackupTesting", "Analyze", "Which of these does only an attempted recovery reveal?",
  ["That the code, the passphrase, the paths and the labels are together sufficient",
   "That the code's checksum is valid",
   "That the descriptor is intact",
   "That the seed is 512 bits"],
  "Each of the others checks one part; the test exercises all of them at once.")

# (concept, old distractor) -> longer distractor, for the items where the right option was conspicuously the longest
EXTEND = {
 ("WalletContents", "Because the database is stored on the blockchain and the application is not"):
   "Because the wallet database is published on the blockchain while the wallet application stays on the user's own computer",
 ("PublicKeyOnlyWallet", "Everything a full wallet can do, more slowly"):
   "Everything a full wallet can do, signing included, though it needs longer to find the matching private key",
 ("IndependentKeyGeneration", "Because the wallet file grew too large to copy"):
   "Because the wallet file grew so large after a few hundred keys that copying it to digital media became impractical",
 ("Seed", "The seed is stored on the blockchain and can be fetched again"):
   "The seed is stored on the blockchain in encrypted form, so a wallet application can fetch it again at any time",
 ("KeyTweak", "A random number that replaces a lost private key"):
   "A random number the wallet keeps so that a lost private key can be replaced by another of the same sequence without changing the address",
 ("HdKeyGeneration", "Public keys can no longer be derived separately"):
   "Public keys can no longer be derived without the private keys, so a branch of the tree is safer to share",
 ("ElectrumV2Code", "It is stored in the wallet file beside the phrase"):
   "It is stored in the wallet file beside the phrase, so that a later version of the software knows which derivation to use",
 ("CodeTradeoffs", "Because the standards have not yet been published"):
   "Because the standards that would settle the questions have not yet been published or widely implemented by wallets",
 ("PlausibleDeniability", "Because the passphrase becomes part of the checksum"):
   "Because the passphrase becomes part of the checksum, so an attacker can tell a duress wallet from the real one",
 ("Memorization", "When the code is shorter than twelve words"):
   "When the code is shorter than twelve words and the wallet holds only a small amount of money",
 ("WalletBirthday", "Deriving the keys, because they are stored with the date"):
   "Deriving the keys, because the wallet stores each of them alongside the date on which it was first used",
 ("WordList", "Because other lists have fewer than 2,048 words"):
   "Because the other lists the standard publishes hold fewer than 2,048 words and so cannot encode eleven bits",
 ("CodeLength", "Because the word list is sorted in groups of three"):
   "Because the word list is sorted in groups of three, so that a code can be read aloud three words at a time",
 ("TextNormalization", "So that the checksum can be computed without the list"):
   "So that the checksum can be computed without the word list, which is what Electrum's own document asks for",
 ("SeedDerivation", "The passphrase as the password and the words as the salt"):
   "The passphrase as the password, the words as the salt and 2,048 iterations of HMAC-SHA512 over both of them",
 ("Bip39Passphrase", "Exactly one, since the code determines the seed"):
   "Exactly one, since the code together with the standard's constant salt determines the seed completely",
 ("SecurityStrength", "A stronger checksum, and yes"):
   "A stronger checksum over the words, and yes, the chapter recommends relying on it for safety",
 ("HdWallet", "A wallet that stores its keys in a sorted file"):
   "A wallet that stores its keys in a sorted file, so that the newest key can always be found first",
 ("MasterChainCode", "Because it contains the seed in compressed form"):
   "Because it contains the seed in compressed form and can be used to recompute the master private key",
 ("ChildKeyIndependence", "Deriving its own children"):
   "Deriving its own children, for which the child's chain code is also required",
 ("ExtendedKey", "Because the chain code is omitted from the private form"):
   "Because the chain code is omitted from the private form, which leaves room for the longer private key",
 ("ExtendedPublicKey", "Sight of the receiving addresses only"):
   "Sight of the receiving addresses only, since the change addresses hang from another branch",
 ("TreeNavigation", "They make the derivation function faster"):
   "They make the derivation function faster by fixing the depth of the tree in advance",
 ("AccountBranch", "Separating receiving from change addresses"):
   "Separating the addresses a wallet gives out from the addresses that receive its change",
 ("AddressIndex", "Because the index is stored only on the blockchain"):
   "Because the index of each address is recorded only on the blockchain and not in the wallet",
 ("ImplicitPath", "A path the user writes down with the recovery code"):
   "A path that the user writes down and keeps beside the recovery code, in case the wallet forgets it",
 ("ImplicitPath", "They require the user to keep extra information"):
   "They require the user to keep extra information beside the code, which may reduce their privacy as well",
 ("ExplicitPath", "It must be kept as secret as the recovery code"):
   "It must be kept as secret as the recovery code, because it contains the extended private key itself",
 ("StandardPath49", "Because nested segwit needs a different curve"):
   "Because nested segwit keys need a different curve from the one that BIP44 keys are derived on",
 ("StandardPath86", "Because taproot keys cannot appear in a descriptor"):
   "Because taproot keys cannot appear in a descriptor at all, so only a fixed path can describe them",
 ("Descriptors", "A wallet's balance and transaction history"):
   "A wallet's balance and its transaction history, as a watching wallet would see them",
 ("OutputScript", "Because private keys cannot be written as words"):
   "Because private keys cannot be written as words once segregated witness output types are in use",
 ("MultipathDescriptor", "Because descriptors could not express hardened paths"):
   "Because descriptors could not otherwise express a hardened derivation step in a key expression",
 ("Miniscript", "Compressing descriptors so they fit on paper"):
   "Compressing descriptors so that they fit on a sheet of paper for a written backup of a wallet",
 ("WalletNotes", "Because only the wallet application can read them"):
   "Because only the wallet application that wrote them is able to read them back afterwards",
 ("LabelExportFormat", "So that the file can be encrypted line by line"):
   "So that each line of the file can be encrypted separately before it leaves the wallet application",
 ("StaticChannelBackup", "Because it never changes the channel's balance"):
   "Because it never changes the balance the channel records for either of the two parties involved",
 ("StaticChannelBackup", "The channel itself, which reopens automatically"):
   "The channel itself, which the protocol reopens automatically once a recovery has finished",
 ("WebStore", "His hardware device refused to export keys"):
   "His hardware device refused to export the extended public key he needed for the shop",
 ("ColdStorage", "Keeping the seed in a bank's safe deposit box only"):
   "Keeping the seed in a bank's safe deposit box and nowhere else, so that no copy exists in the home of the user",
 ("HardwareSigningDevice", "Because the device cannot hold a wallet file"):
   "Because the device cannot hold a wallet file, only the keys that the application asks it to sign with",
 ("Foundations", "Because the earlier chapters' definitions are wrong"):
   "Because the definitions the earlier chapters give are wrong and have to be corrected here",
 ("ShaAlgorithm", "Because the standards chose round decimal numbers"):
   "Because the standards chose round decimal numbers that are easy for a reader to remember",
 ("DigitalSignature", "That the transaction has been confirmed"):
   "That the transaction has already been confirmed by the nodes of the network",
 ("BackupTesting", "That the code's checksum is valid"):
   "That the checksum of the recovery code is valid and that its words are in the list",
}

for (_c, _old), _new in EXTEND.items():
    _hit = 0
    for _k, _it in enumerate(I):
        if _it[0] == _c and _old in _it[3]:
            _o = list(_it[3]); _o[_o.index(_old)] = _new; I[_k] = (_it[0], _it[1], _it[2], _o, _it[4], _it[5]); _hit += 1
    assert _hit == 1, (_c, _old, _hit)

QREWRITE = {
 "What does this first branch of the chapter say a Bitcoin wallet is for?": "What is a Bitcoin wallet for?",
 "Why does the chapter separate the wallet database from the wallet application?": "Why are the wallet database and the wallet application treated as two different things?",
 "What did Bitcoin Core 31.1 report as the format of the wallet created for this chapter?": "What did Bitcoin Core 31.1 report as the format of the wallet created for this course?",
 "In which order does the chapter present the ways of making wallet keys?": "In which order did the ways of making wallet keys appear in practice?",
 "At the chapter's figure of about 32 bytes per key, how many bytes must be backed up for 1,000 independently generated keys?": "At about 32 bytes per key, how many bytes must be backed up for 1,000 independently generated keys?",
 "How many bits are in the chapter's example seed f1cc3bc0...fd97bb73, which is 64 hexadecimal digits?": "How many bits are in the seed f1cc3bc0...fd97bb73, which is 64 hexadecimal digits?",
 "The chapter hashes its seed followed by a counter. What are the first eight hexadecimal digits for the counter 0?": "A seed is hashed with a counter after it. What are the first eight hexadecimal digits of the result for the counter 0?",
 "Which five schemes does the chapter name as in wide use?": "Which five recovery code schemes are named as being in wide use?",
 "Aezeed authenticates its passphrase. What does the chapter say that costs?": "Aezeed authenticates its passphrase. What does that cost?",
 "Why does the chapter present the choices behind a code as trade-offs rather than rules?": "Why are the choices behind a recovery code trade-offs rather than rules?",
 "Why does the chapter call plausible deniability dangerous as well as useful?": "Why is plausible deniability dangerous as well as useful?",
 "In which case does the chapter grant that memorising a code is a powerful feature?": "In which case is memorising a code a powerful feature?",
 "Which figure does the chapter cite from the list of physical attacks it points to?": "Which figure is cited from the published list of physical attacks?",
 "Which three technologies make up the stack the chapter works through in detail?": "Which three technologies make up the wallet stack worked through in detail?",
 "How many bits of entropy are in the chapter's example input 0c1e24e5917779d297e14d45f14e1a1a?": "How many bits of entropy are in the input 0c1e24e5917779d297e14d45f14e1a1a?",
 "Why does the chapter say there is no apparent benefit to more than 128 bits of entropy?": "Why is there no apparent benefit to more than 128 bits of entropy?",
 "What are the four checksum bits of the chapter's 128-bit entropy, taken from the start of its SHA-256 hash?": "What are the four checksum bits of the entropy 0c1e24e5917779d297e14d45f14e1a1a, taken from the start of its SHA-256 hash?",
 "Against which attacker does the chapter say BIP39's stretching helps least?": "Against which attacker does BIP39's key stretching help least?",
 "What are the first sixteen hexadecimal digits of the seed of the chapter's twelve words with no passphrase?": "What are the first sixteen hexadecimal digits of the seed of the twelve words beginning army van defense, with no passphrase?",
 "Which three numbers does the chapter's sidebar use for extended keys, private keys and the curve's strength?": "Which three numbers describe extended keys, private keys and the strength of the curve?",
 "What is the one benefit of more entropy the chapter names, and does it recommend relying on it?": "What is the one benefit of more entropy, and should a user rely on it?",
 "Why does the chapter recommend hardened derivation for the level-1 children of the master keys?": "Why is hardened derivation recommended for the level-1 children of the master keys?",
 "The chapter writes that the derivation combines a parent key described as an uncompressed key. What do the standards do?": "One account of the derivation describes the parent key as an uncompressed key. What does BIP32 actually serialise?",
 "Which version bytes does the chapter's example extended private key carry?": "Which version bytes does the extended private key beginning xprv9tyUQ carry?",
 "The chapter's example xprv has depth 1 and a non-zero parent fingerprint. What does that tell a reader?": "An xprv has depth 1 and a parent fingerprint that is not zero. What does that tell a reader?",
 "Which version bytes does the chapter's example extended public key carry?": "Which version bytes does the extended public key beginning xpub67xpo carry?",
 "Which kind of wallet does the chapter say increasingly uses explicit paths?": "Which kind of wallet increasingly uses explicit paths?",
 "What is the disadvantage of implicit paths the chapter names?": "What is the disadvantage of implicit paths?",
 "What does the chapter say almost all wallets with explicit paths use to record them?": "What do almost all wallets with explicit paths use to record them?",
 "What does the chapter say the extra information of an explicit path costs?": "What does the extra information of an explicit path cost its user?",
 "What does the chapter call the address type of the BIP44 path?": "What is the address type of the BIP44 path called?",
 "What does the chapter say a seed-only restoration shows of a user's history?": "What does a seed-only restoration show of a user's history?",
 "What does the chapter's web store example demonstrate?": "What does the web store of Gabriel's case demonstrate?",
 "A shop's server is taken over. What does the chapter say the attacker can and cannot steal?": "A shop's server is taken over. What can the attacker steal, and what not?",
 "What stays online in the chapter's cold-storage arrangement?": "What stays online in a cold-storage arrangement?",
 "What does the book's glossary mean by cold storage?": "What does cold storage mean?",
 "Why does the chapter call hardware wallet a confusing name for a signing device?": "Why is hardware wallet a confusing name for a signing device?",
 "What does the chapter say most hardware signing devices will never do?": "What will most hardware signing devices never do?",
 "What does the chapter very strongly encourage, even for codes designed to be memorised?": "What is very strongly encouraged, even for codes designed to be memorised?",
 "Why does this chapter define the hash function, the SHA family, the signature and secret sharing itself?": "Why are the hash function, the SHA family, the signature and secret sharing defined here rather than taken for granted?",
 "Which two properties of a hash function does the chapter name when it introduces deterministic key generation?": "Which two properties of a hash function make deterministic key generation possible?",
 "Which two schemes of this chapter are built on secret sharing?": "Which two of the recovery code schemes are built on secret sharing?",
 "What does the chapter name as perhaps the leading cause of lost bitcoins?": "What is perhaps the leading cause of lost bitcoins?",
 "What does the chapter ask a reader to do regularly?": "What should the holder of a backup do regularly?",
}
AREWRITE = {
 "Because its explanations use them and no earlier chapter of the course defines them":
   "Because the explanations here use them and no earlier part of the course defines them",
}

_n = 0
for _k, _it in enumerate(I):
    _q = QREWRITE.get(_it[2], _it[2]); _o = [AREWRITE.get(x, x) for x in _it[3]]
    if _q != _it[2] or _o != list(_it[3]): _n += 1
    I[_k] = (_it[0], _it[1], _q, _o, _it[4], _it[5])
import re as _re
# the page's question drawer skips any bank item whose question or marked option talks about the chapter, the section or the book
_XMETA = _re.compile(r'\b(chapter|section|the book|the author|this text|sweigart)\b|\bfirst program\b', _re.I)
assert _n == len(QREWRITE), (_n, len(QREWRITE))
for _it in I:
    assert not _XMETA.search(_it[2]) and not _XMETA.search(_it[3][0]), _it[2]

# ============================== the file ==============================
items = []
for k, (concept, level, question, options, why, code) in enumerate(I):
    pos = k % 4
    opts = options[1:1 + pos] + [options[0]] + options[1 + pos:]
    assert opts[pos] == options[0] and sorted(opts) == sorted(options), (concept, question)
    it = {"concept": concept, "level": level, "q": question, "options": opts, "answer": pos, "why": why}
    if code:
        it = {"concept": concept, "level": level, "q": question, "code": code, "options": opts, "answer": pos, "why": why}
    items.append(it)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch05-page", "question_bank_v1_0_0.json")
json.dump(items, open(out, "w"), indent=1)
import collections
print("wrote %s: %d items, %d concepts covered, %d with code" % (os.path.basename(out), len(items),
      len({i['concept'] for i in items}), sum(1 for i in items if 'code' in i)))
print("positions:", dict(sorted(collections.Counter(i["answer"] for i in items).items())))
