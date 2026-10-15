"""SEN0401 chapter 14 (Second-Layer Applications): the teaching paragraphs of the leaves of subject 5 (what has changed since the book went to print, and the limits of the experiments), and the introductions of the five subjects (TOP) and of the thirteen groups (MID).
One paragraph per leaf, one line, full sentences, with an everyday comparison, and a citation in the form (Name and Name, 2023). Values from the test chains are single-run values."""
__version__ = "1.0.0"
D = {}

D["ChapterAnchorErratum"] = (
 "The AsciiDoc source of chapter 14 begins with the anchor [[ch12]], although the chapter is the fourteenth of the book and the file of chapter 12 begins with its own anchor [[mining]] (Antonopoulos and Harding, 2023). "
 "The anchor is the label that cross-references point to, so a reference written for chapter 12 would land in chapter 14; the same kind of left-over was found in the file of chapter 13, which begins with [[ch11]]. "
 "The errata appendix of the book concerns the Bitcoin whitepaper, not the book, and does not mention the anchor, so this is a candidate for a correction to report to the authors and not a known erratum (Antonopoulos and Harding, 2023). "
 "It is like a street sign left from the old numbering after the houses were renumbered: the houses are fine, but a visitor following the sign arrives at the wrong door.")

D["LightningNoLongerProposed"] = (
 "The chapter introduces the Lightning Network as a proposed routed network of bidirectional payment channels, which was true of a design in 2015 and is no longer true of a network in operation (Antonopoulos and Harding, 2023). "
 "Wikipedia says that Lightning Labs launched the network in 2018 (Wikipedia contributors, 2026), and the statistics page of mempool.space counted 32,518 channels and 16,225 nodes on 30 August 2026 (Mempool Space, 2026); the glossary of the book still calls it a proposed implementation (Antonopoulos and Harding, 2023). "
 "The word survives from the first edition's time, and a reader should read it as a historical remark. "
 "It is like a bridge that a guidebook describes as planned: today people drive over it every day, and the guidebook is out of date.")

D["WhitepaperDate"] = (
 "The book dates the first description of the network to February 2015 (Antonopoulos and Harding, 2023), and Wikipedia agrees, citing a copy of version 0.5 of the paper archived on 28 February 2015 (Wikipedia contributors, 2026). "
 "The paper that is kept at lightning.network today is the draft version 0.5.9.2 dated 14 January 2016, 320 days after that archive date (Poon and Dryja, 2016), and the same site keeps a summary of the idea as a short slide document (Poon and Dryja, 2015). "
 "So the book is right about the first version and the file one reads today is a later revision of the same draft, with the same two authors, Joseph Poon and Thaddeus Dryja. "
 "It is like a first-edition date on a book of which you hold the fourth printing: the date is right, and the pages are not the same.")

D["CsvDelayThousandVersus2016"] = (
 "The book's example uses a revocable delay of 1,000 blocks, and the hand-built channel of the test enforced exactly that: 999 confirmations were refused and 1000 accepted (Antonopoulos and Harding, 2023). "
 "The lnd channels on the test network reported a delay of 2016 blocks, two weeks at ten minutes a block, and a channel reserve of one percent of the capacity, 4,000,000 satoshis of a 400,000,000-satoshi channel; the delay is a parameter that the two nodes negotiate in the open message of BOLT 2 as to_self_delay and that BOLT 3 uses in the script (Lightning developers, 2026). "
 "A longer delay gives the wronged party more time to react to a breach, at the price of a longer wait for an honest unilateral close. "
 "It is like the notice period in a lease: a longer one protects the party who must react, and delays the one who wants to leave.")

D["BookFeeVersusNetworkFee"] = (
 "The book's fee of 0.001 for each of three hops is 0.3 percent of the payment, a teaching number chosen to make the arithmetic visible (Antonopoulos and Harding, 2023). "
 "The statistics page of the public network gave a median base fee of 500 millisatoshi and a median proportional fee of 100 parts per million on 30 August 2026, and with those medians a payment of 1 bitcoin over three hops would cost about 30,001 satoshis, 0.03 percent, ten times less than in the book (Mempool Space, 2026). "
 "The same page gives averages that are much higher, 904 millisatoshi and 823 parts per million, so a few expensive nodes pull the mean up and the median is the better guide to what a sender can find. "
 "It is like the price of a taxi ride in a city: the posted tariff is high, but most rides cost far less.")

D["TrucAndAnchors"] = (
 "A channel party who must publish a commitment in a time of high fees needs a way to add fee afterwards, and Bitcoin Core 28.0 gave it one: version-3 or TRUC transactions with topology limits, package relay for a child with its parents, and a standard pay-to-anchor output that anyone can spend (Bitcoin Core developers, 2024); (Zhao, 2024); (Sanders, 2025). "
 "On the test chain a version-3 parent of 123 virtual bytes with a zero-value anchor output and a fee of zero was refused alone for its minimum relay fee, and accepted together with a child of 151 virtual bytes through the submitpackage call, with an effective rate of about 10.9 satoshis per virtual byte; the anchor was spent with an empty witness, and both transactions were then confirmed (Bitcoin Core, 2026). "
 "Optech describes the ephemeral-anchor idea behind it (Bitcoin Optech, 2026). "
 "It is like a car that cannot start by itself and is towed by another: neither would pass the fee test alone, but the pair travels at the average speed.")

D["FullRbfIsStandard"] = (
 "BIP 125 defines replacement that is allowed only for a transaction that signalled its opt-in (Harding and Todd, 2015). "
 "Bitcoin Core 28.0 changed the default of the mempoolfullrbf option from 0 to 1 (Bitcoin Core developers, 2024), and the help of Bitcoin Core 31.1 no longer lists the option at all (Bitcoin Core developers, 2026): replacement is simply the rule. "
 "On the test chain the second payment of the same output with a higher fee replaced the first in the memory pool, whatever the first had signalled. "
 "For channels this means that a counterparty can try to replace a commitment, and it is one reason for the topology rules and anchors above. "
 "It is like an auction in which a higher bid always replaces the earlier one, without the earlier bidder having agreed to it.")

D["ProposalsStillDrafts"] = (
 "Several improvements that Lightning designers want are not in Bitcoin: the signature type of BIP 118 for eltoo-style updates, the template opcode of BIP 119, and the point time locked contracts that need schnorr adaptor signatures (Decker and Towns, 2017); (Rubin, 2020); (Bitcoin Optech, 2026). "
 "The saved BIP files of 118, 119, 431 and 433 all carry the status Draft, and Optech calls eltoo a proposed enforcement mechanism for the Lightning Network that would let a later state replace an earlier one without penalties. "
 "A reader should therefore treat any text that relies on them, including text about channel factories and PTLCs, as a plan, not as a feature. "
 "It is like a house with a drawing for an extension: the drawing is public and detailed, but one cannot yet sleep in the new room.")

D["OtherImplementations"] = (
 "The book says that at least five open source teams have implemented the Lightning Network and coordinate through the BOLT standards (Antonopoulos and Harding, 2023). "
 "The sources saved here name Core Lightning, a standard-compliant implementation in C (Core Lightning developers, 2026), Eclair, the Scala implementation of ACINQ (ACINQ, 2026), the Lightning Development Kit in Rust (Spiral, 2026), and lnd, the Go implementation that was the only one installed and run, in version 0.21.3-beta (Lightning Labs, 2026). "
 "The BOLTs are maintained as an open repository whose readme says the specifications are in progress (Lightning developers, 2026). "
 "The interoperability between implementations was not tested here. "
 "It is like several car makers building to the same road rules: each model drives on the same road, but we only drove one.")

D["LndDefaults"] = (
 "A recent lnd node advertises features that the chapter does not know: the node of the test reported 17 feature names, among them anchor commitments with zero-fee HTLC transactions and gossip queries, which are listed in the feature table of BOLT 9 (Lightning developers, 2026). "
 "Its sample configuration gives the defaults of the node, a base fee of 1000 millisatoshi, a timelock delta of 80 blocks and a minimum channel size of 20,000 satoshis (Lightning Labs, 2026), and its release notes record the changes of the 0.21 line, including fixes for taproot channels (Lightning Labs, 2026). "
 "Simple taproot channels use MuSig2 in the funding output, which Optech describes (Bitcoin Optech, 2026). "
 "It is like the options list of a modern car against the one printed in an old manual: the engine is the same idea and the dashboard has grown.")

D["WhatWasNotExecuted"] = (
 "Not everything in the chapter could be run in the sandbox, and the record lists ten items with their reasons: the public network, the other implementations, Taproot Assets and RGB software, a watchtower, an HTLC expiring on the chain, multipath and trampoline routing and offers, gossip on the public network, the transport between lnd nodes on the wire, the signature of the lnd release manifest, and a unilateral close with HTLCs pending. "
 "Each of them is either replaced by a hand-built or recomputed equivalent that is named in the leaves above, or marked as read from a source only (Lightning developers, 2026). "
 "The honest reading of the results is therefore: the mechanisms of the chapter work as described on a private chain, the numbers of the public network are a snapshot, and the behaviour under the load and the attacks of the real network was not tested; Optech describes channel jamming as an example of what a private test cannot show (Bitcoin Optech, 2026). "
 "It is like a test drive on a closed track: it proves that the car runs, and not how it behaves in traffic.")

TOP = {
 "PlatformGuarantees": "The chapter starts from the view that Bitcoin is a platform: a list of guarantees such as no double spend, immutability, accounting and non-expiration can be combined into applications, and the book names the notary and the crowdfunding transaction (Antonopoulos and Harding, 2023). Here each guarantee was tested on a private chain of Bitcoin Core 31.1, so that the claim is a result and not only a sentence.",
 "ColoredCoins": "Colored coins are the oldest application of the chapter: marking bitcoin to stand for other assets, in the beginning by writing data into transactions (Rosenfeld, 2012), and since the proposals of single-use seals by committing off the chain to contract terms that only the parties see (Todd, 2017). The chapter's three mechanisms, seals, pay to contract and client-side validation, are rebuilt here by hand on the test chain (Antonopoulos and Harding, 2023).",
 "PaymentChannels": "A payment channel moves many payments between two parties while the chain sees two transactions, the funding and the settlement, and the book builds it up in three steps: the one-way channel with refund timelocks, the asymmetric revocable commitment, and the hash time lock contract (Antonopoulos and Harding, 2023). The first public designs of such channels are described by the Bitcoin Wiki and by Decker and Wattenhofer (Bitcoin Wiki, 2026); (Decker and Wattenhofer, 2015).",
 "LightningNetwork": "The Lightning Network links channels into a routed network, first described by Joseph Poon and Thaddeus Dryja (Poon and Dryja, 2016) and specified today in the BOLT documents (Lightning developers, 2026). The chapter shows a payment from Alice to Eric through three intermediaries; here the same payment was made on five lnd nodes, and the cryptography of the transport, the onion and the invoice was recomputed from the published test vectors.",
 "SinceThePrint": "Between the print of the book and October 2026 the Lightning Network went into operation, Bitcoin Core gained package relay, version-3 transactions and pay to anchor, replacement became the default, and several details of the chapter turned out to differ from the real software (Bitcoin Core developers, 2024); (Mempool Space, 2026). This subject lists these changes, a candidate erratum in the source file, and the limits of what the sandbox could run.",
}
MID = {
 "ChainGuarantees": "The guarantees of the base system that the chapter lists are the bricks of every application, and four of them were run: a second spend of an output is refused, outputs cannot exceed inputs, a signed transaction does not expire, and the list itself has 18 entries (Antonopoulos and Harding, 2023).",
 "ComposedApplications": "Two applications of the chapter combine several guarantees: a proof of existence needs immutability and a timestamp, and a Lighthouse-style crowdfunding transaction needs integrity and atomicity, and both were built on the test chain (Antonopoulos and Harding, 2023). The first public purchase of goods for bitcoin, the pizzas of Laszlo Hanyecz in May 2010, is the old story behind the idea that bitcoin can be used for trade (Hanyecz, 2010).",
 "SealsAndContracts": "The three mechanisms of modern colored coins are an output that can be spent once, a public key that commits to a contract, and a receiver who checks the history, and each was built by hand and tested against the node (Antonopoulos and Harding, 2023); (Wuille et al., 2020).",
 "AssetProtocols": "RGB and Taproot Assets are the two protocols that combine the three mechanisms and that can ride on Lightning channels, and their sources are the first colored-coin overview of 2012 and the single-use-seal text of 2017 (Rosenfeld, 2012); (Todd, 2017); (RGB developers, 2026).",
 "OneWayChannel": "The one-way channel of Emma and Fabian shows the funding output, the signed commitments and the refund with a lock time, and the numbers of the book were reproduced and the contracts tested on the private chain (Antonopoulos and Harding, 2023); (Decker and Wattenhofer, 2015).",
 "RevocableCommitments": "The asymmetric revocable commitment replaces the ladder of lock times by a penalty: an output delayed by a relative lock time and a revocation key of which each party holds half, which together make cheating costly, as the book's exchanges Hitesh and Irene show (Antonopoulos and Harding, 2023); (Friedenbach et al., 2015).",
 "HashTimeLockContracts": "The hash time lock contract turns two parties' channel into a link of a chain: a secret opens it, a time closes it. The idea was discussed as atomic transfers between chains years before Lightning (Nolan, 2013) and is explained for the book in the Bitcoin Wiki (Bitcoin Wiki, 2026); here its two branches and its hash were tested on the node (Antonopoulos and Harding, 2023).",
 "RoutedPayment": "The routed payment of the book was run on five lnd nodes with the book's fees, and its amounts, timeouts and balances, the hold invoice and the invoice itself are compared with the book's steps (Antonopoulos and Harding, 2023); (Lightning developers, 2026).",
 "TransportAndOnion": "The privacy of Lightning rests on an encrypted transport and an onion of layered messages, and both were recomputed in Python from the published test vectors of BOLT 8, BOLT 4 and BOLT 11 (Lightning developers, 2026); (Danezis and Goldberg, 2009).",
 "ChannelOnChain": "What a channel looks like on the chain was read from real transactions of the test network: the funding output, a commitment with anchors, a cooperative close and a justice transaction after a breach, with the public network's size taken from a statistics page for comparison (Lightning developers, 2026); (Mempool Space, 2026).",
 "ErrataAndDrift": "Between the print and today several details of the chapter have drifted: the anchor in the source file, the word proposed for a network in operation, the date of the paper, the delay and the fees of real channels (Antonopoulos and Harding, 2023); (Poon and Dryja, 2016).",
 "NewMachinery": "New machinery in Bitcoin Core and in the Lightning ecosystem since the print is covered here: package relay and anchors, default replacement, proposals that are still drafts, the other implementations and the features of lnd (Bitcoin Core developers, 2024); (Harding and Todd, 2015); (Zhao, 2024).",
 "Limits": "A research record is only as good as its honesty about what was not done, and the ten items that the sandbox could not run are listed with their reasons (Lightning developers, 2026).",
}
