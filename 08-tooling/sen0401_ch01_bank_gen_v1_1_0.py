#!/usr/bin/env python3
"""Writes ch01-page/question_bank_v1_1_0.json: one item for every concept of the chapter 1 ontology at version 1.2.0, and for every
concept with a worked example a second item at the Apply level whose program is run here and whose printed output is the marked option.
Each item is written as (concept, level, question, [correct, wrong, wrong, wrong], why, code-or-None); the generator moves the correct
option to a rotating position so that the four positions are used about equally, and it then runs every program and checks the match.
The programs use only the standard library and no input, no files and no network, because the page runs them again in Pyodide."""
__version__ = "1.1.0"
import collections, glob, json, os, subprocess, sys

R, U, A, N = "Remember", "Understand", "Apply", "Analyze"
Q = "What does this program print?"
ITEMS = []
def it(concept, level, q, opts, why, code=None):
    ITEMS.append((concept, level, q, opts, why, code))

# ===================================================================================== MONEY
it("Money", U, "Why does the chapter explain Bitcoin's monetary rules before its technical machinery?",
   ["Because every mechanism of the system exists to protect one of those rules",
    "Because the monetary rules of a currency are far easier to change later than the software that enforces them",
    "Because the price of bitcoin determines how mining works",
    "Because a central bank publishes the rules the network follows"],
   "The branch is put first because each later mechanism serves a monetary rule.")
it("Unit", R, "What two things does the Unit section of the chapter fix?",
   ["The name of the currency and the smallest amount that can be recorded",
    "The exchange rate against the dollar and the hours during which the market for it is open",
    "The block interval and the difficulty of mining",
    "The address format and the invoice format"],
   "The section settles the vocabulary: bitcoin and Bitcoin, and the satoshi.")
it("BitcoinUnit", R, "How does the book distinguish bitcoin from Bitcoin?",
   ["bitcoin with a small b is the unit of currency, Bitcoin with a capital B is the system",
    "bitcoin is the network and Bitcoin is the unit of currency",
    "bitcoin names the whole coin, and Bitcoin names the smallest part of it that a block is able to record",
    "The two spellings are interchangeable in the book"],
   "The book's tip sets the convention: the unit is bitcoin, the system is Bitcoin.")
it("BitcoinUnit", U, "What does the pair BTC/USD in a price quotation name?",
   ["The currency pair whose exchange rate is being quoted",
    "A wallet format for United States users",
    "The fee rate charged by an exchange",
    "A standard of the Bitcoin Improvement Proposals that fixes how finely a bitcoin may be divided"],
   "BTC is the abbreviation of the unit, so BTC/USD is the pair bitcoin against the US dollar.")
it("SatoshiUnit", U, "Why does Bitcoin software count amounts in whole satoshis rather than in fractions of a bitcoin?",
   ["Because whole numbers of the smallest unit avoid the rounding errors of fractions",
    "Because the satoshi is the only unit that a wallet application is permitted to display to its user",
    "Because the protocol forbids amounts smaller than one bitcoin",
    "Because exchanges quote their prices in satoshis"],
   "The smallest recordable unit is the satoshi, so amounts are integers and no fraction is lost.")
it("SatoshiUnit", A, Q, ["100000", "1000", "10000000", "0.001"],
   "One bitcoin is 10**8 satoshis, so 0.001 bitcoin is 100000 of them.",
   "from decimal import Decimal\nprint(int(Decimal('0.001') * 10**8))")
it("Supply", R, "What does the supply schedule of Bitcoin fix?",
   ["How much new bitcoin each block may create and therefore the total that will ever exist",
    "How many transactions may be put into one block",
    "How often the difficulty of mining is recalculated",
    "How many of the nodes on the network must agree with one another before a payment counts as accepted"],
   "The schedule gives the subsidy per block, and the sum of all subsidies is the total supply.")
it("SupplyCap", U, "Why is the total supply described as just below 21 million rather than exactly 21 million?",
   ["Because each era's subsidy is rounded down to whole satoshis",
    "Because some bitcoin has been lost by its owners",
    "Because the first block created no bitcoin at all",
    "Because the cap written into the software is lowered a little at each of the halvings of the subsidy"],
   "Integer arithmetic on satoshis loses the fractions, so the sum falls short by 0.0231 bitcoin.")
it("SupplyCap", A, Q, ["20999999.9769", "21000000.0", "20999999.0", "20999999.97690"],
   "Summing the subsidy of all 33 paying eras in satoshis and converting gives 20999999.9769 bitcoin.",
   "print(sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8)")
it("Halving", R, "After how many blocks does the block subsidy halve?",
   ["210000", "2016", "840000", "21000000"],
   "The constant for the halving interval on the main network is 210000 blocks.")
it("Halving", A, Q, ["3.125", "6.25", "12.5", "1.5625"],
   "Block 840000 is four halvings after the start, so 50 bitcoin shifted right four times is 3.125.",
   "print((50 * 10**8 >> 840000 // 210000) / 10**8)")
it("BlockSubsidy", U, "What is the block subsidy, as distinct from the transaction fees of a block?",
   ["The new bitcoin that the block is allowed to create for whoever produced it",
    "The total of the amounts that the senders of all the transactions in the block have paid",
    "The deposit a miner must lock up before mining",
    "The cost of the electricity used to find the block"],
   "The subsidy is newly created money; the fees come from the senders of the transactions.")
it("BlockSubsidy", A, Q, ["[50.0, 25.0, 12.5, 6.25, 3.125]", "[50.0, 25.0, 12.5, 6.25, 3.0]",
                          "[50, 25, 12, 6, 3]", "[50.0, 25.0, 12.5, 6.25, 3.12500]"],
   "At the first block of each of the first five eras the subsidy is halved once more.",
   "print([(50 * 10**8 >> h // 210000) / 10**8 for h in (0, 210000, 420000, 630000, 840000)])")
it("Price", R, "According to the chapter, who sets the price of bitcoin?",
   ["Markets, through the trades that buyers and sellers make",
    "The developers who maintain the reference implementation of the protocol",
    "The miners, through the fees they accept",
    "An international committee of exchanges"],
   "The chapter answers the common question in one line: the price is set by markets.")
it("FloatingExchangeRate", U, "What does it mean that bitcoin has a floating exchange rate?",
   ["Its value against another currency moves with supply and demand in each market",
    "Its value is pegged to a fixed amount of gold",
    "Its value is recalculated once a day by a pricing service and published for all markets",
    "Its value is the same in every market by protocol rule"],
   "A floating rate is not fixed by anyone; it follows the trades in the markets.")
it("FloatingExchangeRate", A, Q, ["60.0", "600.0", "6.0", "60"],
   "At 60000 dollars per bitcoin, 0.001 bitcoin is worth 60.0 dollars.",
   "print(round(0.001 * 60000, 2))")
it("VolumeWeightedAverage", U, "Why does a pricing service weight each trade's price by its volume?",
   ["So that a large trade influences the published rate more than a small one",
    "So that the oldest trade of the day sets the rate",
    "So that the rate can never fall",
    "So that every market in the world contributes exactly one price to the published figure"],
   "Weighting by volume makes the average represent the money actually traded.")
it("VolumeWeightedAverage", A, Q, ["101.0", "102.0", "104.0", "100.0"],
   "Three units at 100 and one at 104 give (300 + 104) / 4, which is 101.0.",
   "trades = [(100, 3), (104, 1)]\nprint(sum(p * v for p, v in trades) / sum(v for p, v in trades))")
it("Issuance", U, "What does the chapter mean by saying that mining decentralizes currency issuance?",
   ["New money is created by a rule that every participant checks instead of by one institution",
    "Every user may print as much bitcoin as they wish",
    "The miners of the network vote once a year on how much new bitcoin may be created",
    "An exchange issues bitcoin when a customer deposits cash"],
   "Issuance follows the consensus rules, which every node enforces, with no central issuer.")
it("CentralBank", R, "What does a central bank do that Bitcoin's rules do instead?",
   ["It controls how much of the national currency exists",
    "It stores the private keys of every account holder in the country it serves",
    "It writes the software that banks run",
    "It sets the fee for every electronic payment"],
   "A central bank controls the monetary base; in Bitcoin a fixed schedule does.")
it("ClearingHouse", U, "What did earlier digital currencies use a central clearing house for?",
   ["To settle all transactions at regular intervals, like a traditional bank",
    "To generate the private keys of their users",
    "To publish the exchange rate of the currency against every other currency",
    "To mine the new units of the currency"],
   "The chapter's sidebar says they cleared all transactions through a central clearinghouse.")
it("CentralBankReplacement", N, "Which two functions of a central bank does mining take over, according to the chapter?",
   ["Currency issuance and the clearing of transactions",
    "Printing the banknotes of a country and setting the interest rate for its banks",
    "Lending to banks and holding foreign reserves",
    "Identity verification and fraud investigation"],
   "The chapter says mining decentralizes the currency-issuance and clearing functions.")
it("Deflation", U, "Why does the chapter call the bitcoin currency deflationary over the long term?",
   ["Because the rate at which new bitcoin is issued keeps falling and finally stops",
    "Because every halving destroys half of the existing bitcoin",
    "Because the price of bitcoin must fall as more is mined",
    "Because the transaction fees of each block are burned rather than paid out to its miner"],
   "Issuance diminishes by rule, so the growth of the supply tends to zero.")
it("Deflation", A, Q, ["2140-10-08", "2009-01-03", "2035-01-01", "2140-01-03"],
   "6930000 blocks of 600 seconds after the first block's time falls on 2140-10-08.",
   "import datetime\nstart = datetime.datetime(2009, 1, 3, 18, 15, 5)\nprint((start + datetime.timedelta(seconds=6_930_000 * 600)).date())")

# ===================================================================================== NETWORK
it("Network", R, "Which three things is the word Bitcoin also the name of, besides the system as a whole?",
   ["A protocol, a peer-to-peer network and a distributed computing innovation",
    "A company, a currency and a bank",
    "A shared database, a web service for wallets and an operating system for nodes",
    "A wallet, an exchange and a mining pool"],
   "The chapter lists exactly these three behind the scenes.")
it("Consensus", U, "What does consensus mean in Bitcoin?",
   ["That the participants agree, without a leader, on one history of transactions",
    "That a majority of users vote on each payment",
    "That the developers of the reference implementation agree on the content of the next release",
    "That every node stores the same wallet file"],
   "Consensus is agreement on the state of transactions reached without a central authority.")
it("ProofOfWork", U, "Why is proof of work hard to produce but easy to check?",
   ["Finding an input whose hash has the required form needs many tries, but one hash verifies it",
    "The hash function is secret, so only miners can compute it",
    "Verification is carried out by a central server that keeps a list of all the answers found so far",
    "The work is encrypted and only nodes hold the key"],
   "The whitepaper notes the average work is exponential in the zero bits while one hash verifies.")
it("ProofOfWork", A, Q, ["15083", "0", "65536", "4"],
   "The loop counts numbers until the hash of the text starts with four zeros; 15083 is the first.",
   "import hashlib\nn = 0\nwhile not hashlib.sha256(f'SEN0401-{n}'.encode()).hexdigest().startswith('0000'):\n    n += 1\nprint(n)")
it("DoubleSpend", R, "What is the double-spend problem?",
   ["That the same unit of digital money could be spent twice",
    "That two people could own the same private key",
    "That one transaction could pay two different addresses belonging to the same person",
    "That a miner could claim two block subsidies"],
   "It is the possibility of spending one unit of digital money more than once.")
it("DoubleSpend", A, Q, ["[True, False]", "[True, True]", "[False, False]", "[False, True]"],
   "The first spend of the coin is accepted and the second is refused, because it is already in the set.",
   "spent = set()\nresult = []\nfor coin in ('coin7', 'coin7'):\n    result.append(coin not in spent)\n    spent.add(coin)\nprint(result)")
it("Mining", U, "What does a miner actually repeat while mining?",
   ["A computation over a header that refers to a list of recent transactions",
    "A request to a central server for the next block",
    "A fresh signature over every unconfirmed transaction waiting in the memory pool",
    "A download of the whole blockchain"],
   "Mining is the repeated computational task that references recent transactions.")
it("Mining", A, Q, ["144", "10", "600", "2016"],
   "At one block every 10 minutes, a day of 24 * 60 minutes holds 144 blocks.",
   "print(24 * 60 // 10)")
it("DifficultyAdjustment", U, "What does the difficulty adjustment keep constant?",
   ["The average time between blocks, whatever the total computing power",
    "The number of transactions that may be placed in each block of the chain",
    "The subsidy that each block pays",
    "The number of nodes on the network"],
   "The difficulty moves so that one block is found about every 10 minutes.")
it("DifficultyAdjustment", A, Q, ["2016", "210000", "144", "1209600"],
   "Two weeks of seconds divided by a ten-minute target gives 2016 blocks per period.",
   "print(14 * 24 * 60 * 60 // (10 * 60))")
it("ByzantineGeneralsProblem", N, "What makes the Byzantine Generals' Problem hard?",
   ["The participants have no leader and the network may be unreliable or compromised",
    "The participants are too many to be counted",
    "The messages are too large to be transmitted",
    "The participants do not share a common language in which to describe the plan"],
   "The problem is agreement without a leader over an unreliable, possibly compromised network.")
it("History", R, "In which years did the chapter's three landmarks of Bitcoin's history fall?",
   ["The paper in 2008, the network in 2009, and its author's withdrawal in 2011",
    "The paper in 2009, the network in 2010, and the first halving in 2011",
    "The paper in 2008, the first exchange in 2009, and the whitepaper's revision in 2012",
    "The network in 2008, the paper in 2009, and Bitcoin Core in 2011"],
   "The chapter gives 2008 for the paper, 2009 for the network and April 2011 for the withdrawal.")
it("Whitepaper", R, "What is the title of the 2008 paper that first described Bitcoin?",
   ["Bitcoin: A Peer-to-Peer Electronic Cash System",
    "Mastering Bitcoin: Programming the Open Blockchain",
    "Hashcash: A Denial of Service Counter-Measure",
    "The Byzantine Generals Problem"],
   "That is the title under which Satoshi Nakamoto published the design.")
it("ReferenceImplementation", U, "Why is Bitcoin Core called the reference implementation?",
   ["It descends from the first implementation and shows how each part should be built",
    "It is the only program that the consensus rules allow to connect to the network",
    "It is maintained by the person who invented Bitcoin",
    "It defines the exchange rate that wallets display"],
   "It grew out of Nakamoto's own software and serves as the model for the parts of the system.")
it("SatoshiNakamoto", R, "What is known about Satoshi Nakamoto, according to the chapter?",
   ["The name is an alias and the identity behind it is unknown",
    "The name belongs to a company registered in 2008",
    "The person behind the name has continued to lead the project ever since it started",
    "The name belongs to a group of university researchers"],
   "The chapter states that the identity of the person or people is still unknown.")
it("Hashcash", U, "What was Hashcash originally proposed for?",
   ["To throttle systematic abuse of un-metered internet resources such as email",
    "To issue a digital currency that was backed by a reserve of gold or a national currency",
    "To replace passwords on web sites",
    "To compress the storage of a shared ledger"],
   "Back's paper gives that purpose, from which Bitcoin's proof of work descends.")
it("Hashcash", A, Q, ["16", "4", "0", "256"],
   "Four zero hexadecimal digits are sixteen zero bits, so the first 1 bit stands at position 16.",
   "import hashlib\nbits = format(int(hashlib.sha256(b'SEN0401-15083').hexdigest(), 16), '0256b')\nprint(bits.index('1'))")
it("PriorDigitalCurrency", N, "What weakness did the digital currencies before Bitcoin share?",
   ["They were centralized, so a single point could be attacked or shut down",
    "They used no cryptography at all",
    "They could not be exchanged for national currencies",
    "They had no limit on how much of their money could be issued by the company behind them"],
   "The chapter's sidebar says they were centralized and therefore easy to attack.")
it("Standards", U, "Why does the chapter's openness group matter for a decentralized system?",
   ["Written, public documents and open code let anyone check what the rules are",
    "They give one organisation the authority to approve or to reject every proposed change",
    "They keep the protocol secret from attackers",
    "They guarantee that every wallet behaves identically"],
   "Openness of documents and source is what makes the rules checkable by anyone.")
it("BitcoinImprovementProposal", R, "What is a Bitcoin Improvement Proposal?",
   ["A numbered design document that describes a feature or a convention",
    "A vote taken among the miners of the network about a proposed change to the rules",
    "A release of the reference implementation",
    "A court filing against a currency exchange"],
   "A BIP is a numbered design document, cited by its number.")
it("BitcoinImprovementProposal", A, Q, ["[(128, 4, 12), (256, 8, 24)]", "[(128, 4, 11), (256, 8, 23)]",
                                        "[(128, 4, 12), (256, 8, 24), (512, 16, 48)]", "[(12, 4, 128), (24, 8, 256)]"],
   "BIP 39 relates the entropy, the checksum of ENT/32 bits and the word count (ENT + CS) / 11.",
   "print([(ent, ent // 32, (ent + ent // 32) // 11) for ent in (128, 256)])")
it("OpenSourceSoftware", U, "What does the Open Source Definition require beyond access to the source code?",
   ["Free redistribution and permission to modify and to make derived works",
    "A fee for commercial use of the program",
    "Approval of each change by the original author",
    "That the program be written in a particular programming language and build system"],
   "The definition opens by saying that open source is not just access to the source code.")
it("W3cStandard", R, "What is a finished standard of the World Wide Web Consortium called?",
   ["A Recommendation", "A Request for Comments", "An Improvement Proposal", "A Specification Draft"],
   "The consortium's finished standards carry the status Recommendation.")

# ===================================================================================== WALLET
it("Wallet", U, "Along which three dimensions does the chapter classify wallets?",
   ["Platform, degree of autonomy, and who controls the keys",
    "Purchase price, country of origin, and the programming language it is written in",
    "Age, number of users, and licence",
    "Block size, fee rate, and address format"],
   "The chapter classifies by platform, by how the wallet interacts with the network, and by key control.")
it("WalletPlatform", R, "Which four wallet platforms does the chapter list?",
   ["Desktop, mobile, web and hardware signing device",
    "Desktop, server, mainframe and router",
    "Full node, lightweight client, third-party interface client and miner",
    "Custodial, noncustodial, hot and cold"],
   "Those are the four kinds in the section on the types of Bitcoin wallets.")
it("DesktopWallet", U, "What security disadvantage does the chapter name for desktop wallets?",
   ["General-purpose operating systems are often insecure and poorly configured",
    "Desktop computers cannot store private keys at all",
    "Desktop wallets are obliged to hand their keys over to a third-party service",
    "Desktop wallets cannot validate transactions"],
   "The chapter warns that platforms such as Windows and macOS are often insecure and poorly configured.")
it("MobileWallet", U, "Why do most mobile wallets reduce their user's privacy?",
   ["They fetch information from remote servers, disclosing addresses and balances",
    "They publish the user's name together with each payment",
    "They store a copy of the recovery code on the server of the phone's manufacturer",
    "They sign transactions with a key shared by all users"],
   "To avoid storing large amounts of data they ask remote servers, which learn what they ask for.")
it("WebWallet", U, "What does a web wallet usually give up in exchange for ease of use?",
   ["Control of the keys, which the third-party server holds",
    "The ability to receive payments at all",
    "The ability to show a balance converted into the user's national currency",
    "Any connection to the Bitcoin network"],
   "Most web wallets take control of the keys from users in exchange for ease of use.")
it("HardwareSigningDevice", N, "Why does the chapter prefer the name hardware signing device to hardware wallet?",
   ["Because the device must be paired with a full-featured wallet to send and receive",
    "Because the device cannot store private keys",
    "Because the device is not made of hardware",
    "Because the device holds no bitcoin of its own and cannot display a balance"],
   "The chapter notes the pairing requirement, and that the paired wallet's security also matters.")
it("NodeType", U, "What does the second classification of wallets, by node type, actually measure?",
   ["How much of the data a wallet checks for itself rather than trusting others",
    "How fast the wallet can display a balance",
    "How many addresses the wallet can hold",
    "Which operating system and which kind of device the wallet was written for"],
   "It measures the degree of autonomy: what the wallet validates and whom it depends on.")
it("FullNode", R, "What does a full node validate?",
   ["The entire history of Bitcoin transactions",
    "Only the transactions of its own wallet",
    "Only the blocks that were produced during the last day of the network",
    "Only the signatures, not the amounts"],
   "The chapter defines it as a program that validates the entire history of transactions.")
it("LightweightClient", U, "What is the other name for a lightweight client, and what does it describe?",
   ["Simplified-payment-verification client, which validates only partly and asks others for data",
    "Pruned node, which deletes the old blocks once it has finished checking them",
    "Mining client, which produces blocks for a pool",
    "Custodial client, which holds other people's keys"],
   "The chapter gives SPV as the alternative name and says it validates partially.")
it("ThirdPartyApiClient", U, "What must a third-party API client trust the remote system for?",
   ["Accurate information and the privacy of what it asks",
    "The security of the user's private keys, but nothing else about the data",
    "The exchange rate it displays only",
    "Nothing, because it checks every rule itself"],
   "The chapter says it trusts the remote server for accurate information and for its privacy.")
it("PeerAndClient", N, "In the chapter's vocabulary, what is the difference between a peer and a client?",
   ["A peer validates every confirmed transaction itself; a client depends on peers for valid data",
    "A peer is a miner and a client is a wallet",
    "A peer is a company and a client is a private user",
    "A peer stores the keys of its user and a client stores the blocks of the chain"],
   "The chapter's tip calls the full nodes the peers and the lightweight software the clients.")
it("KeyControl", R, "Which phrase does the chapter use to summarise the importance of key control?",
   ["Your keys, your coins; not your keys, not your coins",
    "One CPU, one vote",
    "Do not trust anybody on the network; verify everything yourself",
    "Code is law"],
   "The author coined that phrase to emphasise who controls the funds.")
it("NoncustodialWallet", U, "What responsibility follows from using a noncustodial wallet?",
   ["Backing up the keys, because losing them means losing access to the bitcoin",
    "Reporting each payment that is made to the exchange which issued the wallet",
    "Running a full node alongside the wallet",
    "Keeping the wallet connected to the internet at all times"],
   "Only the user holds the keys, so only the user can back them up.")
it("CustodialWallet", U, "What is held by somebody else when a user keeps funds with a custodian?",
   ["The keys, and therefore the control of the funds",
    "The addresses, but not the keys",
    "The recovery code, but not the keys",
    "The record of the transaction history, though not the funds themselves"],
   "In a custodial arrangement the third party controls the keys and the funds on the user's behalf.")
it("Backup", U, "Why does a wallet where the user holds the keys need a backup mechanism?",
   ["Because nobody else can restore the keys if the device is lost",
    "Because the network deletes any address that has not been used for a year",
    "Because the keys expire after a fixed period",
    "Because the exchange rate changes the keys"],
   "No third party holds a copy, so the user alone can provide for recovery.")
it("RecoveryCode", U, "What is a recovery code used for in a noncustodial wallet?",
   ["As the basis from which all the wallet's keys are generated and can be rebuilt",
    "As the password that encrypts the wallet's connection to the nodes of the network",
    "As the address to which other people send payments",
    "As the fee rate the wallet will pay for a transaction"],
   "The chapter says it is used as the basis for the keys the wallet generates.")
it("RecoveryCode", A, Q, ["12", "11", "24", "2048"],
   "The sample recovery code of the chapter is a sentence of twelve words.",
   "code = 'nephew dog crane clever quantum crazy purse traffic repeat fruit old clutch'\nprint(len(code.split()))")
it("WalletMetadata", N, "What does the chapter say a recovery code will not restore?",
   ["The labels and other data the user entered, such as the name of each payee",
    "The private keys of the wallet",
    "The addresses the wallet had generated",
    "The transactions recorded in the chain that the wallet had already received"],
   "Recovery rebuilds the onchain history but not the metadata the user added.")

# ===================================================================================== USAGE
it("Usage", R, "Whose story does the chapter use to show Bitcoin in use?",
   ["Alice, who buys her first bitcoin from her friend Joe",
    "Satoshi Nakamoto, who mines the first block of the chain in January 2009",
    "Bob, who runs a currency exchange",
    "Eve, who attacks the network"],
   "The chapter follows Alice and Joe from the first wallet to the first confirmation.")
it("Address", U, "What is the point of the address group of the chapter?",
   ["It explains what a payee publishes, in which formats, and what that costs in privacy",
    "It explains how the miners of the network are paid for each block that they produce",
    "It explains how a node stores the blockchain",
    "It explains how exchanges set their prices"],
   "The group covers the address, the invoice and the privacy consequence of reuse.")
it("BitcoinAddress", U, "Where is a new Bitcoin address registered when a wallet creates it?",
   ["Nowhere: the wallet generates it without reference to any service",
    "With the reference implementation's registry",
    "With the currency exchange that sold the user their first bitcoin",
    "In the first block that follows its creation"],
   "The chapter stresses that addresses are generated independently, with no registration.")
it("BitcoinAddress", N, "Why can an address be shared without risking the funds behind it?",
   ["Because spending requires the private key, and only the owner can start a spend",
    "Because the address expires after one payment",
    "Because the address is encrypted by the wallet before it is shared with anyone",
    "Because the network refuses payments from strangers"],
   "Unlike a bank account number, knowing an address does not let anyone withdraw.")
it("Invoice", U, "What can an invoice carry that a bare address cannot?",
   ["An amount and a human-readable description, which the wallet can prefill",
    "The private key that is needed in order to spend the funds it points at",
    "The fee rate that the miner must accept",
    "The identity of the payer"],
   "The chapter shows an invoice as a URI with an address, an amount and a description.")
it("Invoice", A, Q, ["1577764", "157776", "15777640", "0.01577764"],
   "The amount parameter of the payment URI is converted to satoshis by multiplying by 10**8.",
   "from decimal import Decimal\nfrom urllib.parse import parse_qs\nq = parse_qs('amount=0.01577764&label=Store')\nprint(int(Decimal(q['amount'][0]) * 10**8))")
it("AddressReuse", N, "What can two people learn if they are both given the same address?",
   ["How much the other one sent to it",
    "The private key that controls it",
    "The name of the wallet's owner",
    "The balance of every other address of the wallet"],
   "The chapter warns that two payees of one address can see each other's payments.")
it("Privacy", N, "In what sense is Bitcoin's privacy pseudonymous rather than anonymous?",
   ["Payments are public but attached to addresses, which are names without a person behind them",
    "The payments themselves are hidden, while the names of the two parties are public",
    "Payments are visible only to the miner who includes them",
    "Payments are encrypted and nobody can read them"],
   "The record is public; the addresses stand in for identities until one is linked to a person.")
it("Transfer", R, "What does the transfer group of the chapter follow?",
   ["A payment from the moment Send is pressed to the moment it is confirmed",
    "The history of the releases of the reference implementation, one by one",
    "The path of a block from one miner to the next",
    "The derivation of the keys from a recovery code"],
   "The group follows Joe's payment to Alice through its objects and stages.")
it("SendingAndReceiving", U, "What does the receiving side of a payment actually do?",
   ["It shows an address or invoice for the sender to pay",
    "It signs the transaction that actually moves the funds to the new owner",
    "It chooses the fee the transaction will pay",
    "It adds the transaction to a block"],
   "Receiving shows a destination; the sender's wallet does the signing.")
it("SendingAndReceiving", A, Q, ["(1.0, 100000)", "(0.001, 100000)", "(1.0, 1000)", "(100000, 1.0)"],
   "0.001 bitcoin is 1.0 millibitcoin and 100000 satoshis.",
   "print((0.001 * 10**3, round(0.001 * 10**8)))")
it("Transaction", R, "What is a transaction, in the words of the book's glossary?",
   ["A signed data structure expressing a transfer of value",
    "A request sent to a server asking it to move part of an account balance",
    "A block of recent payments produced by a miner",
    "An entry in a wallet's list of labels"],
   "The glossary defines it precisely as a signed data structure expressing a transfer of value.")
it("Transaction", A, Q, ["0.001", "100000", "0.1", "1e-05"],
   "A transaction recorded as 100000 satoshis is 0.001 bitcoin.",
   "tx = {'to': 'Alice', 'amount_sat': 100000}\nprint(tx['amount_sat'] / 10**8)")
it("InputsAndOutputs", U, "What are the inputs and outputs of a transaction?",
   ["The inputs name the funds being spent and the outputs assign amounts to new owners",
    "The inputs are the senders of the payment and the outputs are the miners who confirm it",
    "The inputs are the fees and the outputs are the subsidies",
    "The inputs are the addresses and the outputs are the keys"],
   "Inputs identify what is spent; outputs create the new spendable amounts.")
it("InputsAndOutputs", A, Q, ["(110000, 105000)", "(110000, 110000)", "(105000, 110000)", "(100000, 5000)"],
   "The one input totals 110000 satoshis and the two outputs total 105000.",
   "print((sum([110000]), sum([100000, 5000])))")
it("TransactionFee", U, "Where does a transaction fee come from?",
   ["From the difference between the amounts a transaction spends and the amounts it pays out",
    "From a charge that is added by the currency exchange which sold the bitcoin",
    "From a percentage of the block subsidy",
    "From a deposit the receiver makes in advance"],
   "The whitepaper states that the difference between input and output value is the fee.")
it("TransactionFee", A, Q, ["10000", "110000", "100000", "210000"],
   "Spending 110000 satoshis and paying 100000 leaves 10000 satoshis as the fee.",
   "print(110_000 - 100_000)")
it("Confirmation", U, "What gives a transaction its first confirmation?",
   ["Its inclusion in a block",
    "Its arrival at the first node",
    "The signature of the sender",
    "The payment of a fee above the suggested rate"],
   "The glossary says that once a transaction is in a block it has one confirmation.")
it("Confirmation", A, Q, ["0.0002428", "0.0009137", "0.0131722", "0.1"],
   "The whitepaper's formula with a tenth of the computing power and six blocks gives 0.0002428.",
   "import math\nq = 0.1\np = 1 - q\nz = 6\nl = z * q / p\nprint(round(1 - sum(math.exp(-l) * l**k / math.factorial(k) * (1 - (q / p)**(z - k)) for k in range(z + 1)), 7))")
it("Irreversibility", N, "Why does irreversibility make it hard to buy bitcoin with a credit card?",
   ["The seller cannot undo the bitcoin payment if the card payment is reversed afterwards",
    "Credit card networks refuse to carry bitcoin payments",
    "The bitcoin transaction takes considerably longer to arrive than the card payment",
    "The seller must pay the fee of both payments"],
   "The asymmetry gives the seller the whole risk, which is why identity checks are demanded.")
it("OffchainPayment", U, "What does an offchain payment not do?",
   ["Record every payment in the public blockchain",
    "Move value from one party to another",
    "Require any software to be installed on the user's own device",
    "Use Bitcoin's units of account"],
   "Offchain technology keeps most payments out of the public chain.")
it("PaymentChannel", U, "How many transactions does a typical payment channel add to the blockchain?",
   ["Two", "One for each payment", "None at all", "Six"],
   "The glossary says only two transactions are added while many payments are made between the parties.")
it("PaymentChannel", A, Q, ["(59000, 41000, 100000, 2)", "(41000, 59000, 100000, 2)",
                            "(59000, 41000, 100000, 100)", "(60000, 40000, 100000, 2)"],
   "A hundred payments of ten satoshis move 1000 satoshis, the total is unchanged, and two transactions are onchain.",
   "onchain, a, b = 2, 60_000, 40_000\nfor _ in range(100):\n    a, b = a - 10, b + 10\nprint((a, b, a + b, onchain))")
it("LightningNetwork", U, "What does the Lightning Network add to a single payment channel?",
   ["Routing, so a payment can cross several channels to reach someone with no direct channel",
    "A guarantee that no channel can ever be closed",
    "A central server that keeps every balance",
    "A second unit of currency that is used only inside the network itself"],
   "The glossary describes it as routing payments across multiple peer-to-peer channels.")
it("LightningNetwork", A, Q, ["(['Alice', 'Bob', 'Carol', 'Dave'], 3, False)",
                              "(['Alice', 'Dave'], 1, True)",
                              "(['Alice', 'Bob', 'Carol', 'Dave', 'Erin'], 4, False)",
                              "(['Alice', 'Bob', 'Dave'], 2, False)"],
   "Alice reaches Dave over three channels, and no direct channel between them exists.",
   "channels = {('Alice', 'Bob'), ('Bob', 'Carol'), ('Carol', 'Dave')}\nnbr = {}\nfor x, y in channels:\n    nbr.setdefault(x, []).append(y)\n    nbr.setdefault(y, []).append(x)\nprev = {'Alice': None}\nfrontier = ['Alice']\nwhile 'Dave' not in prev:\n    nxt = []\n    for f in frontier:\n        for n in nbr[f]:\n            if n not in prev:\n                prev[n] = f\n                nxt.append(n)\n    frontier = nxt\npath = ['Dave']\nwhile prev[path[-1]]:\n    path.append(prev[path[-1]])\npath.reverse()\nprint((path, len(path) - 1, ('Alice', 'Dave') in channels))")
it("ElectronicPayment", R, "Which payment methods does the chapter name as reversible?",
   ["Credit cards, debit cards, PayPal and bank account transfers",
    "Cash, cheques and money orders",
    "Bitcoin, Lightning and payment channels",
    "Gift cards, shop vouchers and the loyalty points of a retailer"],
   "The chapter lists exactly those four as reversible electronic payment networks.")
it("SemanticBridge", U, "What idea of the chapter does the semantic bridge carry over to the web?",
   ["Control proved by holding a key, with no central registry",
    "A fixed supply of identifiers",
    "An interval of ten minutes between one update of the record and the next",
    "A fee paid for every lookup"],
   "The W3C identity standards apply the same principle of control without a registry.")
it("DecentralizedIdentity", U, "What can the controller of a W3C Decentralized Identifier do without anyone's permission?",
   ["Prove control over the identifier",
    "Change the identifier's syntax",
    "Revoke another controller's identifier",
    "Issue a national identity document"],
   "The specification says the design enables the controller to prove control without permission.")
it("VerifiableCredential", R, "Which three roles make up the ecosystem of verifiable credentials?",
   ["Issuers, holders and verifiers",
    "Miners, nodes and wallets",
    "Authors, editors, reviewers and the publishers who print them",
    "Buyers, sellers and exchanges"],
   "The specification names a three-party ecosystem of issuers, holders and verifiers.")
it("Acquisition", R, "Which four ways of getting a first bitcoin does the chapter list?",
   ["Buying from a friend, earning it, a Bitcoin ATM, and a currency exchange",
    "Mining, staking, lending, and borrowing",
    "A bank transfer, a cheque, a payment in cash, and a gift card",
    "An airdrop, a faucet, a lottery, and a grant"],
   "Those are the four methods the chapter gives for a new user.")
it("BuyFromFriend", U, "Why does the chapter call buying from a friend the least complicated method?",
   ["No company, identity check or account is needed between the two people",
    "The friend is able to reverse the payment afterwards if something goes wrong",
    "It is the only method that needs no wallet",
    "It is the only method with no exchange rate"],
   "The two parties simply agree a rate and make the transfer themselves.")
it("EarnBitcoin", U, "What does earning bitcoin mean in the chapter's two examples?",
   ["Selling a product or service and being paid in bitcoin",
    "Being paid interest on a deposit of bitcoin left with a custodian",
    "Receiving the block subsidy for mining",
    "Winning bitcoin in a prize draw"],
   "The chapter's examples are a programmer selling skills and a hairdresser cutting hair for bitcoin.")
it("BitcoinATM", R, "What does a Bitcoin ATM do?",
   ["It takes cash and sends bitcoin to the user's smartphone wallet",
    "It prints out a paper copy of the user's private key for safe keeping",
    "It stores bitcoin on behalf of the user",
    "It mines blocks on behalf of the user"],
   "The chapter defines it as a machine that accepts cash and sends bitcoin to a phone wallet.")
it("CurrencyExchange", U, "What does a currency exchange provide?",
   ["A market where buyers and sellers swap bitcoin for local currency",
    "A wallet whose keys the user holds alone",
    "A node that validates the whole blockchain",
    "A published list of the improvement proposals that Bitcoin Core implements"],
   "The chapter describes exchanges as markets linked to a bank account.")
it("IdentityVerification", N, "Why do companies that sell bitcoin for card payments demand identity checks?",
   ["Because the card payment can be reversed after the irreversible bitcoin has been sent",
    "Because the protocol itself requires a verified identity for every address that is used",
    "Because the miners refuse transactions from unknown senders",
    "Because the exchange rate depends on the buyer's country"],
   "The check offsets the risk created by the difference in reversibility.")

# ===================================================================================== FOUNDATIONS
it("Foundations", U, "Why does the chapter's foundations branch exist?",
   ["Because chapter 1 uses technical words such as signature, key and node as if they were known",
    "Because the book's later chapters are optional",
    "Because Bitcoin invented all of those ideas itself",
    "Because the worked examples of the chapter need one particular operating system"],
   "The branch explains the vocabulary that the story takes for granted.")
it("Cryptography", N, "What is cryptography used for in Bitcoin, and what is it not used for?",
   ["To prove who authorised a payment, not to hide the payments themselves",
    "To hide the amounts of payments from the miners",
    "To encrypt the connection between every pair of nodes that exchange blocks",
    "To compress the blockchain so that it fits on a phone"],
   "Bitcoin's transactions are public; the cryptography proves authorisation and protects the record.")
it("HashFunction", U, "What does a hash function guarantee about its output?",
   ["It has a fixed length and changes completely when the input changes",
    "It can be reversed to recover the input",
    "It is different on each occasion that the very same input is hashed again",
    "It is shorter for shorter inputs"],
   "A hash is a fixed-length fingerprint, and any change to the input gives a different result.")
it("HashFunction", A, Q, ["ba7816bf", "00000000", "d41d8cd9", "abcabcab"],
   "The standard's test vector for the three letters abc begins with ba7816bf.",
   "import hashlib\nprint(hashlib.sha256(b'abc').hexdigest()[:8])")
it("DigitalSignature", U, "What does a valid digital signature prove?",
   ["That someone holding the private key signed exactly this data",
    "That the signer is a particular named person",
    "That the data was signed at a particular time",
    "That the person who signed intended the payment to be a fair one"],
   "It binds the data to the key, not to an identity or an intention.")
it("DigitalSignature", A, Q, ["(588, True, False)", "(588, True, True)", "(65, True, False)", "(588, False, False)"],
   "Signing 65 with the private exponent gives 588, which verifies as 65 and not as 66.",
   "n, e, d, m = 3233, 17, 2753, 65\nsig = pow(m, d, n)\nprint((sig, pow(sig, e, n) == m, pow(sig, e, n) == 66))")
it("PublicKeyCryptography", U, "What makes a pair of keys suitable for public-key cryptography?",
   ["The private key cannot be worked out from the public key in practice",
    "The two keys are identical to each other but are stored in different places",
    "Both keys must be kept secret from everyone else",
    "The public key changes each time it is used"],
   "The pair is generated so that deriving the private key from the public one is infeasible.")
it("PublicKeyCryptography", A, Q, ["65", "3233", "2753", "588"],
   "What the public exponent does to the message, the private exponent undoes, recovering 65.",
   "print(pow(pow(65, 17, 3233), 2753, 3233))")
it("PrivateKey", U, "Why is a Bitcoin private key chosen from an enormous range of numbers?",
   ["So that nobody can find it by trying one value after another",
    "So that it can be written down in few words",
    "So that the network can index it quickly",
    "So that each address derived from it can be written in a shorter form"],
   "A 256-bit number has far too many possible values to search.")
it("PrivateKey", A, Q, ["78", "256", "64", "32"],
   "Two to the power 256 written in decimal has 78 digits.",
   "print(len(str(2**256)))")
it("Entropy", U, "What does entropy measure?",
   ["How much uncertainty an attacker faces in guessing a secret",
    "How long a secret is when written as words",
    "How often a wallet generates a new address for an incoming payment",
    "How much disk space a wallet needs"],
   "It is an information-theoretic measure, in bits, of the attacker's uncertainty.")
it("Entropy", A, Q, ["(11, 132, 132)", "(2048, 132, 128)", "(11, 128, 132)", "(12, 132, 132)"],
   "Each of 2048 words carries 11 bits, twelve words carry 132, which is 128 bits plus a 4-bit checksum.",
   "print((2048 .bit_length() - 1, 12 * 11, 128 + 128 // 32))")
it("Checksum", N, "What can a checksum do and what can it not do?",
   ["It detects accidental changes but does not stop an attacker who recomputes it",
    "It corrects any single error in the data",
    "It hides the contents of the data from anyone who happens to read it",
    "It proves who wrote the data"],
   "A checksum catches mistakes; it carries no secret, so it is no defence against tampering.")
it("Checksum", A, Q, ["3", "0", "15", "128"],
   "The first four bits of the SHA-256 hash of sixteen zero bytes are the value 3.",
   "import hashlib\nprint(hashlib.sha256(bytes(16)).digest()[0] >> 4)")
it("KeyedHash", U, "What does mixing a secret key into a hash add?",
   ["Evidence that the result was produced by a holder of the key",
    "Confidentiality of the data that was hashed",
    "A shorter result than the hash function alone gives",
    "A signature which anybody at all is able to verify without knowing a secret"],
   "A keyed hash authenticates as well as fingerprints, but only for holders of the key.")
it("KeyedHash", A, Q, ["64", "32", "512", "128"],
   "HMAC with SHA-512 produces a result of 512 bits, which is 64 bytes.",
   "import hmac\nprint(len(hmac.new(b'key', b'message', 'sha512').digest()))")
it("KeyStretching", U, "What does key stretching make expensive?",
   ["Every single guess that an attacker tries",
    "The storage of the derived key",
    "The transmission of the key over the network",
    "The generation of the original entropy"],
   "Repeating the function many times multiplies the attacker's cost by the same factor.")
it("KeyStretching", A, Q, ["(64, 'd96147bf')", "(64, 'abandon01')", "(32, 'd96147bf')", "(2048, 'd96147bf')"],
   "Two thousand and forty-eight applications of HMAC-SHA512, combined with exclusive-or, give a 64-byte key beginning d96147bf.",
   "import hmac\npassword, salt, iters = b'abandon', b'mnemonic', 2048\nu = hmac.new(password, salt + bytes([0, 0, 0, 1]), 'sha512').digest()\nseed = u\nfor _ in range(iters - 1):\n    u = hmac.new(password, u, 'sha512').digest()\n    seed = bytes(a ^ b for a, b in zip(seed, u))\nprint((len(seed), seed.hex()[:8]))")
it("Chain", R, "Which four ideas does the chain group of the chapter explain?",
   ["The block, the blockchain, the timestamp and the node",
    "The key, the address, the invoice and the fee",
    "The wallet, the exchange, the ATM and the friend",
    "The protocol, the browser, the server and the database"],
   "Those are the four concepts of the group, explained from the inside out.")
it("Block", U, "What does a block commit to, besides its own transactions?",
   ["The block before it", "The address of the payee", "The exchange rate of the day", "The next block"],
   "The glossary says a block carries a commitment to the previous block.")
it("Block", A, Q, ["(3050, 1)", "(1, 3050)", "(3050, 3050)", "(840000, 0)"],
   "Block 840000 holds 3050 transactions and the first block holds one.",
   "b840 = {'tx_count': 3050}\nb0 = {'tx_count': 1}\nprint((b840['tx_count'], b0['tx_count']))")
it("Blockchain", N, "Why is an old block hard to change once later blocks exist?",
   ["Changing it changes its hash, so every later link and every later proof of work must be redone",
    "The blocks are encrypted with a key that nobody holds",
    "Old blocks are deleted and cannot be edited",
    "The network signs every block with the private key of the person who made it"],
   "The chain of hashes propagates any change forward, and the work would have to be repeated.")
it("Blockchain", A, Q, ["(True, False)", "(True, True)", "(False, False)", "(False, True)"],
   "Rebuilding the chain from the original data matches the stored hashes; from tampered data it does not.",
   "import hashlib\ndef link(prev, data):\n    return hashlib.sha256((prev + data).encode()).hexdigest()\ndef build(items):\n    hs, prev = [], 'genesis'\n    for d in items:\n        prev = link(prev, d)\n        hs.append(prev)\n    return hs\ndata = ['Joe pays Alice 1', 'Alice pays Eve 2', 'Eve pays Joe 3']\nstored = build(data)\ntampered = ['Joe pays Alice 100'] + data[1:]\nprint((build(data) == stored, build(tampered) == stored))")
it("Timestamp", N, "What does a block's timestamp prove, and what does it not prove?",
   ["That the data was marked at that time, not that the event happened then",
    "That the miner was honest about the transactions that the block contains",
    "That the block was accepted by the network",
    "That the fee was paid before the block was found"],
   "A timestamp records when a marking was affixed; the miner chooses it within limits.")
it("Timestamp", A, Q, ["2009-01-03 18:15:05+00:00", "2009-01-03 00:00:00+00:00",
                        "1970-01-01 00:00:00+00:00", "2009-01-03 18:15:05.000+00:00"],
   "The first block's time, 1231006505 seconds after the start of 1970, is this moment in universal time.",
   "import datetime\nprint(datetime.datetime.fromtimestamp(1231006505, datetime.timezone.utc))")
it("Node", U, "What does a node do that a wallet by itself need not do?",
   ["Receive, check and relay the blocks and transactions of the network",
    "Store the private keys of its user and sign payments with them",
    "Display the balance of an address",
    "Produce a QR code for a payment"],
   "A node takes part in the network and validates; holding keys is the wallet's job.")
it("Computing", U, "Why does the chapter compare a Bitcoin wallet with a web browser?",
   ["Both are applications that speak a protocol on top of the internet",
    "Both store their data on a third-party server",
    "Both of them are written by the same group of volunteer developers",
    "Both must be installed on a desktop computer"],
   "The analogy puts the protocol below and the competing applications above.")
it("Internet", R, "What is the Internet, in the words of the glossaries the chapter relies on?",
   ["A worldwide network of networks that share one protocol suite",
    "A single very large computer that routes all of the world's traffic",
    "A company that sells access to web pages",
    "A protocol for exchanging web pages"],
   "Both glossaries describe it as the interconnected worldwide system of networks sharing a protocol suite.")
it("Protocol", R, "What is a protocol?",
   ["A set of rules, formats and procedures for exchanging data between systems",
    "A program that displays data to a user",
    "A machine that stores data for others",
    "A written document that describes a proposed feature of a system"],
   "The security glossary defines it as a set of rules, that is formats and procedures.")
it("Http", U, "What does the chapter use HTTP for in its explanation?",
   ["As the model of a protocol with many competing applications on top of it",
    "As the protocol that the nodes of Bitcoin use to exchange blocks with each other",
    "As the format in which addresses are written",
    "As the encryption that protects a wallet's keys"],
   "The chapter likens Bitcoin and its wallets to HTTP and its browsers.")
it("Http", A, Q, ["['GET', '/index.html', 'HTTP/1.1']", "['GET /index.html HTTP/1.1']",
                   "['GET', '/index.html', 'HTTP', '1.1']", "['GET', 'index.html', '1.1']"],
   "The standard says a request line is a method, a target and a version, each separated by one space.",
   "print('GET /index.html HTTP/1.1'.split(' '))")
it("WebBrowser", R, "What does a web browser do?",
   ["It retrieves and displays pages and follows the links between them",
    "It stores the pages that other computers on the network may fetch",
    "It routes traffic between networks",
    "It signs the documents a user sends"],
   "The glossary defines it as a program that retrieves and displays pages and follows hyperlinks.")
it("Server", U, "Why does the chapter say that Bitcoin has no central server?",
   ["Because every full node both provides and consumes the same services",
    "Because the nodes use no network connections at all",
    "Because a single company owns every node",
    "Because the servers of the network are hidden behind the reference implementation"],
   "In the peer-to-peer design the roles are mixed, so no one machine serves the rest.")
it("Api", U, "What does an API define?",
   ["Which operations may be requested and the form of each request and answer",
    "The programming language in which a program using it must be written",
    "The hardware on which a program may run",
    "The price that a service charges for an answer"],
   "An API is the contract between the program that offers it and the programs that use it.")
it("Api", A, Q, ["True", "False", "sha256", "None"],
   "The hashlib module's guaranteed set of algorithms includes sha256, which is part of its interface.",
   "import hashlib\nprint('sha256' in hashlib.algorithms_guaranteed)")
it("Uri", R, "What is a URI?",
   ["A string that identifies a resource, with a scheme before the colon",
    "A program that displays a resource",
    "A number which identifies one particular computer on the network",
    "A standard for encoding binary data as text"],
   "The standard defines it as a simple and extensible means of identifying a resource.")
it("Uri", A, Q, ["('bitcoin', '175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W', 'amount=20.3')",
                  "('bitcoin:', '175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W', 'amount=20.3')",
                  "('', 'bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W', 'amount=20.3')",
                  "('bitcoin', '', 'amount=20.3')"],
   "In a bitcoin payment URI the scheme is bitcoin, the path is the address and the query holds the parameters.",
   "from urllib.parse import urlsplit\nu = urlsplit('bitcoin:175tWpb8K1S7NmH4Zx6rewF9WQrcZv245W?amount=20.3')\nprint((u.scheme, u.path, u.query))")
it("QrCode", U, "What problem does a QR code solve in the chapter's story?",
   ["Joe does not have to type Alice's long address by hand",
    "Alice does not have to reveal her address at all",
    "The payment does not have to pay a fee",
    "The wallet does not have to connect to the network at all to be paid"],
   "The code carries the same information in a form a camera can read.")
it("QrCode", A, Q, ["[21, 177]", "[21, 160]", "[1, 40]", "[21, 181]"],
   "Version 1 is 21 modules across and every further version adds four, so version 40 is 177.",
   "print([21 + 4 * (v - 1) for v in (1, 40)])")
it("Database", R, "What is a database?",
   ["A storage system for organized data, easier to search, structure and extend",
    "A program that displays data to a user",
    "A protocol for moving organized data between two or more computers",
    "A fixed-length fingerprint of a data object"],
   "That is the definition the chapter's glossary source gives.")
it("Database", A, Q, ["('Alice', ['Joe'], False)", "('Alice', ['Joe', 'Alice'], False)",
                       "('Alice', ['Joe'], True)", "('Alice', [], False)"],
   "The lookup by key finds Alice, the scan finds Joe, and the unknown address is absent.",
   "rows = [{'address': 'addr1', 'label': 'Alice'}, {'address': 'addr2', 'label': 'Joe'}]\nindex = {r['address']: r for r in rows}\nprint((index['addr1']['label'], [r['label'] for r in rows if r['address'] == 'addr2'], 'addr3' in index))")
it("OperatingSystem", R, "What does an operating system do?",
   ["It manages a computer's hardware and software resources and serves its programs",
    "It validates the blocks and transactions of the Bitcoin network",
    "It signs the transactions a user sends",
    "It stores the pages that a browser displays"],
   "That is the definition of the source the chapter relies on.")
it("DistributedSystem", U, "What makes a system distributed?",
   ["Its parts run on different networked computers and work together",
    "It runs on one single computer that has several processors inside it",
    "It stores its data in more than one file",
    "It is used by people in more than one country"],
   "A distributed system's inter-communicating components sit on different networked computers.")
it("BitsAndBytes", U, "How many hexadecimal digits does a 256-bit hash need?",
   ["64", "32", "256", "16"],
   "Each hexadecimal digit stands for four bits, so 256 bits take 64 digits.")
it("BitsAndBytes", A, Q, ["(32, 64)", "(64, 32)", "(256, 64)", "(32, 32)"],
   "A SHA-256 result is 32 bytes, and its hexadecimal form is 64 characters long.",
   "import hashlib\nh = hashlib.sha256(b'')\nprint((len(h.digest()), len(h.hexdigest())))")
it("Threats", U, "What do the two threats of the chapter have in common?",
   ["Both attack the person or the device rather than the cryptography",
    "Both break the hash function used by Bitcoin",
    "Both of them require control of the greater part of the mining power",
    "Both work only against custodial wallets"],
   "Malware and phishing aim at the weakest part, which is usually not the mathematics.")
it("Malware", R, "What is malware?",
   ["Software written on purpose to damage, to leak information or to gain unauthorised access",
    "Software whose source code is not published",
    "Software that contains a defect which its author never intended to put there",
    "Software that runs without an operating system"],
   "The definition turns on the intention to cause harm or to gain unauthorised access.")
it("Phishing", N, "When is a request for a recovery code a sign of phishing?",
   ["At any time other than the first set-up and a genuine recovery",
    "Only in the case where the request for it arrives by electronic mail",
    "Only when the wallet is custodial",
    "Only when the user has no bitcoin yet"],
   "The chapter's rule is that a legitimate wallet asks only during set-up or recovery.")

# ===================================================================================== NATURE
it("Nature", U, "What two kinds of statement does the nature branch separate?",
   ["What Bitcoin is like, and what it is built from",
    "What Bitcoin costs, and what it earns",
    "What Bitcoin was, and what it will be",
    "What Bitcoin permits its users to do, and what the law permits them to do"],
   "The branch has the characteristics on one side and the four architectural parts on the other.")
it("Characteristic", R, "Which four characteristics does the chapter give Bitcoin?",
   ["Virtual, borderless, decentralized and robust",
    "Fast, cheap, private and legal",
    "Open, documented, tested and released",
    "Deflationary, infinitely divisible, durable and easily portable"],
   "Two come from the opening description and two from the sidebar on earlier currencies.")
it("Virtual", U, "In what sense is the bitcoin currency entirely virtual?",
   ["There are no coins at all; the coins are implied by the transactions",
    "The coins exist as individual files that their owner keeps and stores",
    "The coins exist only inside exchanges",
    "The coins are backed by a reserve of gold"],
   "The chapter says there are no physical coins or even individual digital coins.")
it("Virtual", A, Q, ["(70000, 35000)", "(35000, 70000)", "(100000, 30000)", "(70000, 30000)"],
   "Adding what each person received and subtracting what they sent gives Alice 70000 and Eve 35000.",
   "txs = [('Joe', 'Alice', 100_000), ('Alice', 'Eve', 30_000), ('Joe', 'Eve', 5_000)]\ndef balance(who):\n    return sum(a for f, t, a in txs if t == who) - sum(a for f, t, a in txs if f == who)\nprint((balance('Alice'), balance('Eve')))")
it("Borderless", N, "What limits the chapter puts on the word borderless?",
   ["Where bitcoin meets traditional systems, national regulations still apply",
    "Only residents of certain countries may run a node",
    "The protocol refuses payments between different countries",
    "Every payment must pass through a currency exchange in the sender's own country"],
   "The protocol knows no borders, but exchanges and banks are regulated.")
it("Decentralized", U, "What does decentralized by design mean for Bitcoin?",
   ["There is no central authority or point of control that could be attacked or corrupted",
    "The software of the network is written by volunteers living in many countries",
    "The blockchain is stored in several data centres",
    "Each user may choose their own consensus rules"],
   "The chapter's words are: free of any central authority or point of control.")
it("Robust", N, "Against whom does the chapter say a decentralized currency must be robust?",
   ["Antagonists, whether legitimate governments or criminal elements",
    "Competing digital currencies only",
    "Its own developers only",
    "Users of the currency who have lost their own recovery codes"],
   "The sidebar names both legitimate governments and criminal elements.")
it("Architecture", R, "Which four parts does the chapter say Bitcoin consists of?",
   ["A peer-to-peer network, a public journal, consensus rules and proof of work",
    "A wallet, an exchange, a miner and a node",
    "A protocol, a browser for it, a server and a shared database",
    "A key, an address, a transaction and a block"],
   "The chapter lists exactly those four innovations brought together.")
it("PeerToPeerProtocol", U, "What does peer-to-peer mean for the full nodes of the network?",
   ["They can all perform the same functions and there are no special nodes",
    "Each node is assigned a rank of its own by the reference implementation",
    "Each node connects to exactly one other node",
    "Only the oldest nodes may relay transactions"],
   "The network chapter says the peers can all perform the same functions, with no special nodes.")
it("PeerToPeerProtocol", A, Q, ["4", "7", "2", "3"],
   "Starting from A, the gossip reaches every one of the seven nodes after four rounds.",
   "links = {'A': ['B', 'C'], 'B': ['A', 'D'], 'C': ['A', 'E'], 'D': ['B', 'F'], 'E': ['C', 'F'], 'F': ['D', 'E', 'G'], 'G': ['F']}\nseen, frontier, rounds = {'A'}, {'A'}, 0\nwhile len(seen) < len(links):\n    frontier = {n for f in frontier for n in links[f]} - seen\n    seen |= frontier\n    rounds += 1\nprint(rounds)")
it("PublicJournal", U, "Why must Bitcoin's transaction journal be public?",
   ["Because the absence of a transaction can only be confirmed by knowing all of them",
    "Because the law requires the record to be open",
    "Because a record kept privately would be far too large for anyone to store",
    "Because the miners are paid for publishing it"],
   "The whitepaper argues that transactions must be publicly announced for this reason.")
it("ConsensusRuleSet", U, "What do the consensus rules cover, in the chapter's list of Bitcoin's parts?",
   ["Independent transaction validation and currency issuance",
    "The format of addresses and invoices",
    "The fee rate that wallets should suggest",
    "The choice of the operating system on which a node is to be run"],
   "The third part is the set of rules for independent validation and for issuance.")
it("ConsensusRuleSet", A, Q, ["[True, False, True]", "[True, True, True]", "[False, False, True]", "[True, False, False]"],
   "A claim of exactly the subsidy passes, one satoshi more fails, and the subsidy plus fees passes.",
   "def accept(claim, height, fees):\n    subsidy = (50 * 10**8) >> (height // 210000)\n    return claim <= subsidy + fees\nprint([accept(312_500_000, 840000, 0), accept(312_500_001, 840000, 0), accept(325_000_000, 840000, 12_500_000)])")

# ===================================================================================== assemble
# The page draws its first multiple-choice question from the concept of the bank's first item, so the items for the
# concepts of the chapter (level 3) are listed before those for the branch and group headings (levels 1 and 2).
HERE = os.path.dirname(os.path.abspath(__file__))
_pd = sorted(glob.glob(os.path.join(HERE, "ch01-page", "page_data_v*.json")))[-1]
_lvl = {n["id"]: n["level"] for n in json.load(open(_pd, encoding="utf-8"))["nodes"]}
ITEMS.sort(key=lambda t: 0 if _lvl.get(t[0]) == 3 else 1)

OUT = []
for i, (concept, level, q, opts, why, code) in enumerate(ITEMS):
    pos = i % 4
    rest = list(opts[1:])
    options = rest[:pos] + [opts[0]] + rest[pos:]
    item = {"concept": concept, "level": level, "q": q}
    if code: item["code"] = code
    item["options"] = options; item["answer"] = pos; item["why"] = why
    OUT.append(item)

path = os.path.join(HERE, "ch01-page", "question_bank_v1_1_0.json")
json.dump(OUT, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("wrote %s - %d items" % (path, len(OUT)))
print("levels:", dict(sorted(collections.Counter(i["level"] for i in OUT).items())))
print("answer positions:", dict(sorted(collections.Counter(i["answer"] for i in OUT).items())))
print("longest-is-correct:", sum(1 for i in OUT if max(i["options"], key=len) == i["options"][i["answer"]]))
