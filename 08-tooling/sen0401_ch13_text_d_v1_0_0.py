"""SEN0401 chapter 13 (Bitcoin Security): the teaching paragraphs of the leaves of subject 5 (custody cases) and subject 6 (survivability), then the introductions of the six subjects (TOP) and of the sixteen sections (MID).
One paragraph per leaf, one line, full sentences. Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
D = {}

D["MtGoxLoss"] = (
 "The book says that many early exchanges kept all user funds in one hot wallet on one server and that many of them were hacked, and Mt. Gox is the largest case (Antonopoulos and Harding, 2023). "
 "The exchange, based in Shibuya, Tokyo, handled over 70% of all bitcoin transactions by early 2014 and then closed after losing 744,408 bitcoins in a theft that went undetected for years, while the Bitcoin Wiki gives the loss as 640 thousand; the count of 850,000 fell to 650,000 when 199,999.99 bitcoins turned up in an old wallet, and in June 2011 fraudulent trades had already pushed its quoted price down to one cent (Wikipedia contributors, 2026); (Bitcoin Wiki, 2026). "
 "The Wikipedia article names its hot wallet, which fits the book's warning that centralizing the keys in a single system removes control from users and concentrates the risk. "
 "No server was attacked in this chapter, so the case is read from the pages and not run. "
 "It is like a bank that keeps the contents of every safe deposit box in one cash drawer by the front door, and then finds that the drawer has been emptied for years.")

D["BitfinexSegregatedWallets"] = (
 "A custodian's design can fail even when it is sold as secured, and the Bitfinex exchange shows it (Wikipedia contributors, 2026). "
 "In 2015 Bitfinex partnered with BitGo to offer secured wallets, in May 2015 a hack took 1,500 bitcoins, and in August 2016 it announced a breach in which 119,756 bitcoin were stolen from the users' segregated wallets, after which the trading price fell by 20% (Wikipedia contributors, 2026). "
 "The page does not say how the keys were arranged, so we do not claim a technical cause; the lesson that is supported is the book's, that the customers had to trust the operators' security design, a trust that Bitcoin's own model does not ask for (Antonopoulos and Harding, 2023). "
 "It is like leaving your valuables with a guard who says the rooms are separate: the separation helps only if the guard's own keys are safe.")

D["CasasciusHologram"] = (
 "Physical bitcoin makes the book's point about physical security tangible: Casascius coins were metal coins with a private key on paper hidden under a tamper-evident hologram (Bitcoin Wiki, 2026). "
 "Mike Caldwell of Sandy, Utah sold them until 26 November 2013 in 1, 10, 25, 100 and 1000 BTC sizes; reading the key without destroying the hologram was difficult or impossible, and FinCEN told him that minting physical bitcoins made him a money transmitter, which led him to suspend the sales (Bitcoin Wiki, 2026). "
 "The coins show the strengths and weaknesses of a bearer instrument: anyone who sees an intact hologram knows the key has not been read, and anyone who is given a coin has to trust the maker never to have copied the key. "
 "The book speaks of printed paper and metal plates; a coin with a hologram is a nicer package of the same idea (Antonopoulos and Harding, 2023). "
 "It is like a sealed envelope of cash with a sticker that tears when opened.")

D["HeirWaitsTenBlocks"] = (
 "The book says that the families of Bitcoin users are often unaware of the funds and suggests sharing access with a trusted relative or lawyer and, for a more complex scheme, multisignature access and estate planning (Antonopoulos and Harding, 2023). "
 "A script can build a delayed path for an heir: with or(owner, and(heir, older 10)) the owner's spend was accepted at once, the heir's spend with sequence 10 was refused as non-BIP68-final at 1 and at 9 confirmations and accepted at 10, and the heir without the sequence set could not even finish signing (Bitcoin Core, 2026). "
 "The relative timelock comes from BIP 68 and BIP 112, and Optech's topics on timelocks and miniscript describe the tools that make such a policy readable and checkable (Friedenbach et al., 2015); (BtcDrak et al., 2015); (Bitcoin Optech, 2026). "
 "In real life the owner must move the coins before the delay ends to keep the heir waiting, and the lawyer, the court and the family were not part of this run. "
 "It is like a letter to be opened after ten days: if the owner turns up in time he collects it, and if he does not, the heir may.")

D["OlderSixtyFiveThousand"] = (
 "A timelock is only as good as the number it is written with, and BIP 68 reads only the low 16 bits of the sequence, so a wait is at most 65,535 blocks, about 455.1 days, or 65,535 units of 512 seconds, 33,553,920 seconds or 388.4 days (Friedenbach et al., 2015). "
 "The descriptor parser of Bitcoin Core 31.1 accepted both older(65535) and older(65536), but the heir whose key was behind older(65536) could spend with 1 confirmation, because 65536 has no bits in the low 16 and so means no wait at all, a trap that the parser does not warn about (Bitcoin Core, 2026); (BtcDrak et al., 2015). "
 "This is a single run, and it is the reason to test a recovery plan on a test chain before the real money is put behind it. "
 "For waits longer than a year the owner has to refresh the coins to restart the clock, which is a duty and not an accident. "
 "It is like a timer on an oven that counts in 16-bit seconds: set it to one more than the largest value and it silently starts from zero.")

D["WhatWasNotExecuted"] = (
 "A security chapter must say what the experiments did not do, because a claim about a device that was never touched is a claim from a page and not from a run (Antonopoulos and Harding, 2023). "
 "The record lists ten things that were not run, each with its reason: the hardware device, a true air gap, paper and metal backups, an exchange breach, estate planning with a lawyer, mainnet funds, Shamir in a wallet, BIP 39 recovery in Core, a good gpg verification and BIP 324 on the wire (Bitcoin Core, 2026). "
 "What was run is a set of private nodes on regtest, one record of one run, and every value read from it is a single-run value that a rerun will change in its hashes and times but not in its verdicts. "
 "The stories of Mt. Gox, Bitfinex and Casascius are read from the saved pages (Wikipedia contributors, 2026); (Bitcoin Wiki, 2026). "
 "It is like a crash test: the dummy and the wall are real, the family car's insurance claim is not.")

TOP = {}
TOP["SecurityModel"] = ("The first subject is the security model of the chapter: why a payment can be public, why the network may be open, which single block a node takes on trust, and how a user checks the software before running it (Antonopoulos and Harding, 2023). "
 "Each statement was run on a private chain of Bitcoin Core 31.1 or read from its source (Bitcoin Core, 2026).")
TOP["ProtectingKeys"] = ("The second subject is how a key is protected where it lives: offline, behind a passphrase, inside a device, on paper or in a memory (Antonopoulos and Harding, 2023). "
 "The watch-only wallet, the PSBT through a cold node and the encrypted wallet were run on test nodes, and the device, paper and brain cases were read from pages and computed (Bitcoin Core, 2026).")
TOP["KeepingAccess"] = ("The third subject is the opposite risk to theft, losing access: the seed words and the arithmetic behind them, the backup file, the stale backup and the descriptor that completes it (Antonopoulos and Harding, 2023). "
 "The word list and the key tree were recomputed against published test vectors (Palatinus et al., 2013).")
TOP["SharingControl"] = ("The fourth subject is control shared among keys and among people: multisignature signing and key loss, the odds of loss and theft, the bytes a script costs, and secret sharing, which the chapter does not mention (Antonopoulos and Harding, 2023). "
 "The signing was run, and the sharing scheme was computed (Shamir, 1979).")
TOP["CustodyHistory"] = ("The fifth subject is the history of custody: an exchange that held a country's worth of coins, another that called its wallets secured, and a coin with a sticker (Antonopoulos and Harding, 2023). "
 "These are read from the saved pages and their facts were checked against them (Wikipedia contributors, 2026).")
TOP["Survivability"] = ("The sixth subject is availability after the key holder is gone: an heir path behind a timelock, the number that silently breaks it, and what this chapter did not run (Antonopoulos and Harding, 2023). "
 "The script and its timelock were run on a test chain (Bitcoin Core, 2026).")

MID = {}
MID["TransactionsPublishable"] = ("This section is about what a signed payment reveals and what happens when it is changed or sent again (Antonopoulos and Harding, 2023).")
MID["TransportEncryption"] = ("This section is about the encrypted transport between nodes, how it differs from the book's statement and how it can be bypassed (Mehta et al., 2019).")
MID["RootOfTrust"] = ("This section is about the single block that a node trusts, the check that it applies to its own blocks and the second anchor of the software (Bitcoin Core, 2026).")
MID["VerifyingTheSoftware"] = ("This section is about the check of the program before it is run: the hash, the signatures and the reproducible build (Bitcoin Core release signers, 2026).")
MID["ColdStorage"] = ("This section is about keeping the keys on a machine that does not go online, and the PSBT that carries a payment to it and back (Chow, 2017).")
MID["WalletEncryption"] = ("This section is about the passphrase of the wallet: its errors, its timeout, its parameters and its effect on the seed (Bitcoin Core, 2026).")
MID["SigningDevices"] = ("This section is about devices that hold the keys: the signer interface of the node, the limit of what a device can protect and the PIN wait (Bitcoin Wiki, 2026).")
MID["PaperAndMemory"] = ("This section is about two old ways of keeping a key, on paper and in the head, and why both have lost favour (Bitcoin Wiki, 2026).")
MID["SeedWords"] = ("This section is about the words, the seed and the master key that follow from them, tested against the published vectors (Palatinus et al., 2013).")
MID["WalletBackups"] = ("This section is about the backup file, its age, its completeness and the book's story of a backup that could not be opened (Bitcoin Core, 2026).")
MID["Multisig"] = ("This section is about several keys for one payment: the signing, the order of keys, the loss of keys, the odds and the cost in bytes (Bitcoin Wiki, 2026).")
MID["SharingASecret"] = ("This section is about splitting a secret into shares, from Shamir's paper of 1979 to the formats of today (Shamir, 1979).")
MID["ExchangeFailures"] = ("This section is about custodians that lost customer coins and what the book draws from them (Wikipedia contributors, 2026).")
MID["PhysicalCoins"] = ("This section is about bitcoin made physical, with a key under a hologram (Bitcoin Wiki, 2026).")
MID["Heirs"] = ("This section is about a delayed path for an heir and the numbers that limit the delay (Friedenbach et al., 2015).")
MID["Limits"] = ("This section is about what the experiments did not do (Bitcoin Core, 2026).")
