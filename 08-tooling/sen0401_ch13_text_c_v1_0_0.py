"""SEN0401 chapter 13 (Bitcoin Security): the teaching paragraphs of the leaves of subject 3 (keeping access: seed words and wallet backups) and subject 4 (sharing control: multisignature and sharing a secret). One paragraph per leaf, one line, full sentences.
Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
C = {}

C["Bip39MnemonicChecksum"] = (
 "The book warns that the bigger risk is not theft but losing access, and the word list of BIP 39 is the everyday answer, because words are easier to write down and check than a long number (Antonopoulos and Harding, 2023). "
 "A phrase of 12 words is 132 bits, 128 of entropy and 4 of checksum cut from the SHA-256 of the entropy; the 16 zero bytes of the first test vector give abandon eleven times and about, the library reproduced it exactly, the list has 2,048 words, and replacing the last word by zoo or abandon makes the phrase invalid, so most single typing slips are caught (Palatinus et al., 2013); (Trezor developers, 2026). "
 "The checksum can only tell that a phrase is wrong, never that it is the right one, and a word that is wrong but gives a valid phrase would open a different, empty wallet. "
 "It is like the check digit at the end of a bank card number: it catches the slip of a finger and does not know whose card it is.")

C["Bip39SeedFromWords"] = (
 "From the words to the keys the path is a stretch and a tree: PBKDF2 turns the phrase into a seed, and BIP 32 turns the seed into a master key (Palatinus et al., 2013). "
 "The seed is HMAC-SHA512 with 2048 rounds over the words, with the salt mnemonic plus the optional passphrase; with the passphrase TREZOR the library reproduced the 64-byte seed and the master xprv of the Trezor test vector, and without the passphrase the seed begins 5eb00bbddcf06908, a completely different wallet (Trezor developers, 2026); (Moriarty et al., 2017). "
 "That is why a passphrase works as a hidden extra word: the phrase on the paper opens one wallet and the phrase plus the passphrase opens another, and nothing in the paper says which is the rich one, but the passphrase itself must then be backed up too. "
 "It is like a book code in which the page number is on the note and the book is in your head: lose either and the message is gone.")

C["Bip32MasterVector"] = (
 "A hierarchical deterministic wallet needs one secret to make all keys, and BIP 32 fixes how: the master key is the HMAC-SHA512 of the seed under the text Bitcoin seed, with the left half as the private key and the right half as the chain code (Wuille, 2012). "
 "For the seed 000102030405060708090a0b0c0d0e0f the library gave a private key beginning e8f32e723decf405 and a chain code of 32 bytes, and the Base58Check form xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi is the one printed in the specification, so the arithmetic is the same in every wallet that follows it. "
 "The practical meaning for security is that one backup of the seed covers all keys, past and future, which makes the seed the single most valuable and most dangerous piece of paper in the whole system (Antonopoulos and Harding, 2023). "
 "It is like the master key of a building: it opens every door, so it is kept in the safest drawer and copied with the greatest care.")

C["CoreHasNoMnemonics"] = (
 "A reader may expect that every wallet backs up with twelve words, but Bitcoin Core does not: none of seven saved Core files, the sources of the backup, wallet and encryption RPCs, the documents on managing wallets, descriptors and PSBTs and the command line help, mentions a mnemonic or BIP 39 (Bitcoin Core, 2026); (Bitcoin Core developers, 2026). "
 "Recovery in Core is by wallet file and descriptors, and since release 23.0 new wallets are descriptor wallets, while release 30.0 can no longer create or load the old Berkeley DB legacy wallets, which can only be migrated (Bitcoin Core developers, 2022); (Bitcoin Core developers, 2025). "
 "The book's chapter 5 does list BIP 39 and its successors such as SLIP39 among the recovery codes, so the two descriptions are compatible but not the same tool (Antonopoulos and Harding, 2023). "
 "This is a statement about the saved files only, not about every wallet program. "
 "It is like two keeps for the same castle: one written down as a list of words, the other as the architect's plan.")

C["RestoreGivesSameAddresses"] = (
 "A backup is useful if the restored wallet is the same wallet, and the node documents the whole round trip: backupwallet makes the file and restorewallet loads it under a new name (Bitcoin Core, 2026). "
 "In the test the source wallet and the restored copy both held 3.0 coins, the next new address of the restored wallet was the address the source handed out next, and the address far along the chain belonged to it, so a fresh backup restores addresses, coins and position in the sequence. "
 "The book says that a wallet can be backed up like any file and stored in several copies, and the point of the test is that the copy is only as good as it is recent (Antonopoulos and Harding, 2023). "
 "Bitcoin.org advises regular backups at several secure locations (Bitcoin.org, 2026). "
 "It is like a photocopy of your address book: it is complete on the day it was made.")

C["StaleBackupMissesFunds"] = (
 "A backup does not know what happens after it, and with a small keypool that can cost money (Bitcoin Core, 2026). "
 "On a node run with -keypool=3 the stale copy restored 1.0 coin of the 3.0, because the later 2.0 coins went to the tenth address, outside the stale range 0 to 2, while the up-to-date copy found everything; the help text of the option warns that smaller sizes may increase the risk of losing funds when restoring from an old backup, and the default size is 1000 (Bitcoin Core developers, 2026). "
 "A wallet that scans ahead 1000 addresses is rarely caught out, but an old backup and a busy wallet can still disagree, and after an encryption the backup is stale at once, as the earlier paragraph showed. "
 "It is like an old key ring for a building that has since added new rooms: the keys you have open the rooms that existed then.")

C["DescriptorIsPartOfBackup"] = (
 "The book's boxed warning says that to spend bitcoins you may need more than the seed, especially with multisignatures and complex scripts, because the output commits to conditions that the wallet must be able to reveal (Antonopoulos and Harding, 2023). "
 "The node shows it: a wallet that held one of the three keys had no idea of the multisignature address (balance 0.0), a wallet given the full descriptor again found the 2.0 coins, and the same three keys in a different order under multi gave another address and balance 0.0 (Wuille and Chow, 2021); (Bitcoin Core, 2026). "
 "That is the reason for output script descriptors, for the descriptors of segwit and tapscript, and for the wallet policies that hardware devices register, and also the reason that a backup of keys without the descriptor is incomplete (Wuille and Chow, 2024); (Ingala, 2023). "
 "The record of the old wallets matters too: release 23.0 made descriptor wallets the default (Bitcoin Core developers, 2022). "
 "It is like having the keys to three padlocks but not knowing on which of a thousand boxes they hang.")

C["LostSevenThousand"] = (
 "The book's example of the opposite risk is a well-known Bitcoin awareness and education project that in July 2011 lost almost 7,000 bitcoin by losing the encryption keys of its own complex backups, and its moral is that securing coins too well may make them unfindable, like money buried in the desert (Antonopoulos and Harding, 2023). "
 "Of the 77 saved sources only the book contains this sentence, so the event and the project are unconfirmed here, the name is not given by the book and we do not guess it, and the lesson, not the event, is what the table can support. "
 "The Bitcoin Wiki gives the same advice in the plain form that failed backups, mistyped letters and corrupted drives have lost many people their coins, and the only protection is redundancy (Bitcoin Wiki, 2026). "
 "Testing a restore before the money depends on it is the cheapest insurance, and the earlier tests of this chapter did exactly that. "
 "It is like a treasure map written in a code whose key was on the same map.")

C["TwoOfThreeSigning"] = (
 "The book recommends multisignature addresses for large amounts, with keys in different places and under different people, so that no one person can compromise the funds (Antonopoulos and Harding, 2023). "
 "In the test a 2-of-3 wallet needed two signers: the first key alone left the PSBT incomplete with one signature, the first and third together made it complete, it was finalized and accepted by the mempool, and its input had four witness items, an empty dummy, two signatures and the script, in 146 virtual bytes (Bitcoin Core, 2026); (Chow, 2017). "
 "The Bitcoin Wiki describes the same arrangement with keys spread across a desktop, laptop and smartphone, any two of which move the money (Bitcoin Wiki, 2026). "
 "Optech's separate page on scriptless multisignatures covers signatures made with several keys that look like one on the chain, which is a different technique from this script (Bitcoin Optech, 2026). "
 "It is like a bank vault with three keyholders and a rule that two must turn their keys together.")

C["SortedmultiOrder"] = (
 "Because a multisignature address depends on the set of keys, wallets must agree on their order, and BIP 67 solves it by sorting the public keys lexicographically by their binary form (Kerin et al., 2015). "
 "The three public keys in two orders gave the same address under sortedmulti and two different addresses under multi, the wallet's first address was the derived address 0, and the descriptor of the test was 436 characters long with three keys; the source of Bitcoin Core implements both functions (Bitcoin Core, 2026). "
 "A wallet that stores multi in the wrong order will not find its coins, which is the same error as the missing descriptor of the previous subject, and sortedmulti removes that source of loss. "
 "It is like lining up three people by height before taking a photograph: whichever way they arrive, the photo looks the same.")

C["KeyLossTolerance"] = (
 "The book notes that multisignature addresses can offer redundancy when a single person keeps several keys in different places (Antonopoulos and Harding, 2023). "
 "On the test chain, with one of the three keys lost, the other two still signed the PSBT to completion; with two lost, the remaining key left one signature and no complete transaction (Bitcoin Core, 2026). "
 "The Bitcoin Wiki says the same: in a 2-of-3 wallet the loss of one key does not lose the wallet, because the other two can recover the funds, and the redundancy of the backup is the point (Bitcoin Wiki, 2026). "
 "This holds only if the descriptor and at least two keys are kept, and a lost descriptor makes even three keys useless. "
 "It is like a car with three keys of which any two are needed to start it: losing one is an annoyance and losing two is a tow truck.")

C["OddsOfLossAndTheft"] = (
 "Whether a scheme of several keys is safer than a single key depends on whether one fears loss or theft, and the arithmetic of the binomial distribution shows the trade (Antonopoulos and Harding, 2023). "
 "If each key is lost with probability 0.1 and stolen with 0.05, independently, which is an assumption and not a measurement, one key is lost with 0.1 and stolen with 0.05; 2-of-3 is stuck with 0.028 and robbed with 0.00725; 1-of-3 is stuck with 0.001 but robbed with 0.14263; and at a loss chance of 0.5 the 2-of-3 stands where the single key does, at 0.5. "
 "So 2-of-3 improves both risks when each key is more reliable than a coin toss, whereas 1-of-3 trades theft for loss; real keys are not independent when they sit in the same drawer. "
 "It is like three alarm systems: with 'any one' you are never locked out but the burglar needs only one, with 'two of three' both the owner and the burglar have to work harder.")

C["MultisigCostsBytes"] = (
 "Safety has a price in bytes, and bytes are paid for in fees. "
 "The same one-input one-output payment took 110 virtual bytes from a single key and 146 from the 2-of-3 script, 36 more, a ratio of 1.33, which at 10 satoshis per virtual byte is 360 satoshis more for each such spend (Bitcoin Core, 2026). "
 "The extra bytes are the second signature, the three public keys in the script and the empty dummy item, and BIP 387 defines the multi_a descriptor for tapscript, another script type with its own sizes that was not measured here (Wuille and Chow, 2024). "
 "For a safe that is spent once in several years the premium is trivial. "
 "It is like paying for a second lock on the door: a small recurring cost for a large drop in risk.")

C["ShamirTwoOfThree"] = (
 "Multisignature splits control among keys, and secret sharing splits a single secret into pieces, a distinction the chapter does not draw (Shamir, 1979). "
 "Adi Shamir's scheme hides the secret as the constant term of a random polynomial: with a degree-1 polynomial over the prime 2 to the 127 minus 1, the secret 123456789 and the slope 987654321, the shares were 1111111110, 2098765431 and 3086419752, any two of them recovered the secret by Lagrange interpolation, and one share did not; the paper calls this a (k, n) threshold scheme (Shamir, 1979); (Wikipedia contributors, 2026). "
 "The weak point is the moment of recovery, when the whole secret exists again in one place, whereas in multisignature the keys never meet. "
 "It is like cutting a banknote into three pieces so that any two taped together are enough to show the serial number.")

C["OneShareRevealsNothing"] = (
 "The strength of a threshold scheme is that fewer than k shares tell nothing at all, which Shamir expresses by saying that any k minus 1 pieces leave the secret completely undetermined (Shamir, 1979). "
 "Over the small prime 257 the share (1, 100) fits 257 pairs of secret and slope, one for each of the 257 possible secrets and 257 different slopes, so an attacker who steals a share cannot even say which secrets are more likely. "
 "Shamir also pointed out that with n = 2k - 1 the key is recovered even when k - 1 pieces are lost or betrayed, a very robust key management scheme (Shamir, 1979). "
 "The computation here is a demonstration over a small field and says nothing about the security of any product. "
 "It is like a jigsaw puzzle in which every piece alone shows a perfectly random picture.")

C["Codex32AndSlip39"] = (
 "The chapter names multisignature and survivability but never secret sharing, and the word Shamir does not occur in it (Antonopoulos and Harding, 2023). "
 "The ecosystem has moved on: BIP 93, codex32, with the status Draft in the saved copy, splits a BIP 32 seed into up to 31 shares with a checksum that can be worked by hand, and the book's chapter 5 lists SLIP39 as a successor to BIP 39 that distributes one seed among several shares (Olsson Curr et al., 2023); (Antonopoulos and Harding, 2023). "
 "The Wikipedia article on Shamir's secret sharing says that the scheme was first developed by Adi Shamir in 1979 (Wikipedia contributors, 2026). "
 "None of these was run on a device in this chapter. "
 "It is like a family recipe split between three cousins: each holds a part, and the dish can only be cooked when enough of them get together.")
