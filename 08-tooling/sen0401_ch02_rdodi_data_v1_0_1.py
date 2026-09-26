"""SEN0401 chapter 2 (Mastering Bitcoin 3rd edition, How Bitcoin Works) for the RDODI build.
Every claim read on 2026-09-25 from the source it cites; every computation executed under Python 3.14.4 -
including the whitepaper's attacker-success procedure, which reproduces the paper's own table exactly."""
__version__ = "1.0.1"
CH = 2
TITLE = "How Bitcoin works: one transaction from wallet to blockchain, checked against the whitepaper"
QUESTION = "How does chapter 2 of Mastering Bitcoin's 3rd edition explain a transaction's path from wallet to blockchain, which of its quantitative claims can be reproduced from primary sources, and how does its transaction chain meet the course theme?"
VERSION = "1_1_0"  # MINOR: concepts added from the owner's course notes, checked against the 3rd edition  # revision: the owner's course notes added as a source, 2026-09-25
LABELS = {'Bip21Uri': 'BIP21 URI'}
PUBS = [
 ("P01","Mastering Bitcoin, 3rd edition - Chapter 2, How Bitcoin Works (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)","https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch02_overview.adoc",True),
 ("P02","Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)","https://bitcoin.org/bitcoin.pdf",False),
 ("P03","Bitcoin Core releases (Bitcoin Core project)","https://bitcoincore.org/en/releases/",False),
 ("P04","PROV-O: The PROV Ontology, W3C Recommendation, 30 April 2013","https://www.w3.org/TR/prov-o/",False),
 ('P_NOTES', 'Course notes: Chapter_2_HowBitcoinWorks.pptx, SEN0401 (then CSE0469) Block Chain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; supplied by the owner on 2026-09-25 (sha256 8629b856328bf0cf)', 'urn:sen0401:course-notes:Chapter_2_HowBitcoinWorks.pptx:8629b856328bf0cf', False),
 ('P06', 'Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus (Antonopoulos and Harding, 2023)', 'https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch12_mining.adoc', False),
 ('P07', 'Blockchain Demo (Brownworth), interactive web page', 'https://andersbrownworth.com/blockchain/hash', False),
]
CONCEPTS = [("Section",x) for x in ("How Bitcoin Works","Bitcoin Overview","Buying from an Online Store","Bitcoin Transactions","Transaction Inputs and Outputs","Transaction Chains","Making Change","Coin Selection","Common Transaction Forms","Constructing a Transaction","Getting the Right Inputs","Creating the Outputs","Adding the Transaction to the Blockchain","Bitcoin Mining","Spending the Transaction")] + \
 [("Concept",x) for x in ("input","output","transaction fee","change address","consolidation transaction","block explorer","confirmation","genesis block","satoshi","consensus rules")]
FINDINGS = [
 ("F1","Background","Chapter 2 follows one real transaction - Alice paying Bob's Store - through wallet, network and blockchain: transactions as double-entry lines of inputs and outputs with an implied fee, transaction chains, change and coin selection, common transaction forms, constructing and propagating a transaction, mining that bundles transactions into blocks, and confirmations that make a payment harder to reverse as blocks pile up.",["P01"]),
 ("F2","Contemporary developments","The Bitcoin Core software that full nodes run to verify every rule has continued to release after the book; its releases page lists 31.1 as the newest.",["P03"]),
 ("F3","Comparative analysis","The chapter's claim that a payment becomes harder to reverse with each confirmation is quantified in Nakamoto's paper: for an attacker with a tenth of the hash power the probability of catching up falls from 0.2045873 at one confirmation to 0.0002428 at six, and a Python transcription of the paper's own procedure reproduces that table exactly.",["P02","P01"]),
 ("F4","Conclusion","For the course theme, a transaction chain - each input spending an earlier output - is a provenance graph, and W3C's PROV Ontology offers the vocabulary to describe it: entities derived from entities by activities, attributed to agents.",["P01","P04"]),
 ("F5","Course notes","The owner's course notes for this chapter (2021, after the 2nd edition) surfaced topics now added to the deck, each checked against the 3rd edition: the invoice as a BIP21 URI, which the 3rd edition prints in full with a bech32 address where the notes had the older format; why ten minutes is an average and six confirmations a convention, with small payments accepted unconfirmed at low double-spend risk as coffee shops accept small card payments, from the 3rd edition's chapter 12; the notes' own analogy of mining as a giant competitive sudoku, kept and labelled as an analogy because the 3rd edition does not use it; and the Blockchain Demo the notes link to, verified reachable.",["P_NOTES","P01"]),
]
TAX = [
 ("Transaction","TransactionPart","Input","an earlier output being spent","An input spends funds by referring to an earlier transaction's output and proving ownership with a digital signature.",None),
 ("Transaction","TransactionPart","Output","an amount locked to an address","An output receives funds; the outputs add up to slightly less than the inputs.",None),
 ("Transaction","TransactionPart","TransactionFee","inputs minus outputs","The fee is implied: the difference between the inputs and the outputs, collected by the miner.",("sum([15_000_000]) - sum([10_000_000, 4_990_000])","10000")),
 ("Transaction","Linkage","TransactionChain","Alice's payment spending Joe's output","Each transaction's inputs spend earlier outputs, so transactions form chains back through history.",None),
 ("Transaction","Linkage","MakingChange","paying 5 from a 20 input","An output larger than the payment returns the rest as change to a new address of the payer.",("20 - 5","15")),
 ("Transaction","Linkage","CoinSelection","choosing which inputs to spend","Wallets choose which inputs to spend, balancing many small inputs against few large ones, much as people handle cash.",None),
 ("Transaction","Form","SimplePayment","one input, two outputs","The most common form: one input, and two outputs - the payment and the change.",None),
 ("Transaction","Form","Consolidation","many inputs, one output","Many inputs spent into a single output, like exchanging a pile of coins for one note.",None),
 ("Transaction","Unit","Satoshi","one hundred-millionth of a bitcoin","The smallest unit: a bitcoin divides into 100,000,000 satoshis.",("10**8 // 1000","100000")),
 ("Network","Propagation","TransactionPropagation","a transaction relayed across nodes","A signed transaction is transmitted to the network and relayed by nodes until it reaches miners.",None),
 ("Network","Propagation","BlockExplorer","a site that shows a transaction or block","A block explorer looks up addresses, transactions and blocks - and may learn what you look up.",None),
 ("Blockchain","Mining","Block","a bundle of transactions with a small header","Transactions are bundled into blocks whose header is hard to form correctly and easy to verify.",None),
 ("Blockchain","Mining","ConsensusRules","the rules every block must follow","Miners earn honest income only from blocks that follow all consensus rules, which keeps blocks valid.",None),
 ("Blockchain","Security","Confirmation","each block built on top","Each block mined on top of the one containing a transaction is one more confirmation; more confirmations make reversal harder.",("round(1 - sum(__import__('math').exp(-6*0.1/0.9) * (6*0.1/0.9)**k / __import__('math').factorial(k) * (1 - (0.1/0.9)**(6-k)) for k in range(7)), 7)","0.0002428")),
 ("Blockchain","Security","GenesisBlock","block number 0","The first block of the chain, to which every block links back.",None),
 ("Semantics","ProvenanceModel","ProvenanceGraph","a transaction chain described in PROV-O","A transaction chain is a provenance graph: outputs derived from outputs by transactions, attributed to key holders - expressible in W3C PROV-O.",None),

 ("Transaction","PaymentRequest","Bip21Uri","the invoice encoded in the store's QR code","A BIP21 URI carrying the address, amount, label and message, which the wallet reads so the payer never types an address.",("__import__('urllib.parse').parse.parse_qs(__import__('urllib.parse').parse.urlsplit('bitcoin:bc1qk2g6u8p4qm2s2lh3gts5cpt2mrv5skcuu7u3e4?amount=0.01577764&label=Bob%27s%20Store').query)['label'][0]","\"Bob's Store\"")),
 ("Blockchain","Security","UnconfirmedTransaction","a payment propagated but not yet in a block","Propagated to the network but not yet recorded in a block; blocks arrive every 10 minutes on average, not on a timetable.",None),
 ("Blockchain","Security","SmallPaymentAcceptance","a cheap item sold without waiting","A merchant may accept a small payment unconfirmed because the double-spend risk is low, as coffee shops accept small card payments without a signature.",None),
 ("Blockchain","Mining","SudokuAnalogy","mining pictured as a giant sudoku","An analogy from the course notes: hard to solve, easy to check, adjustable in size, restarted after every solution.",None),
 ("Practice","InteractiveDemo","BlockchainDemo","Anders Brownworth's blockchain demo","An interactive page where changing one earlier block invalidates every later block's hash.",None),
]
S = "Antonopoulos and Harding, 2023"; N = "Nakamoto, 2008"; C = "Bitcoin Core, 2026"; P = "World Wide Web Consortium, 2013"
BODY = {
 "Transaction": "How Bitcoin Works follows one payment, Buying from an Online Store, and its Bitcoin Transactions section treats a transaction like a line in a double-entry ledger whose difference is the transaction fee (%s)." % S,
 "TransactionPart": "Transaction Inputs and Outputs names the two sides of every transaction and what lies between them (%s)." % S,
 "Input": "An input spends funds by pointing at an earlier output and carrying a digital signature from its owner that anyone can check (%s)." % S,
 "Output": "An output receives funds, and the outputs add up to slightly less than the inputs (%s)." % S,
 "TransactionFee": "The fee is never written down as such: it is the difference between inputs and outputs, collected by the miner who includes the transaction (%s)." % S,
 "Linkage": "Transaction Chains, Making Change and Coin Selection show how transactions connect to one another (%s)." % S,
 "TransactionChain": "Alice's payment to Bob's Store spends an output of the transaction in which her friend Joe paid her, so each payment links back to earlier ones (%s)." % S,
 "MakingChange": "Buying an item that costs 5 bitcoins with a 20-bitcoin input sends 5 to the store and 15 back as change, not counting the fee, often to a new change address for privacy (%s)." % S,
 "CoinSelection": "Coin selection is the wallet's choice of inputs: aggregating many small ones or using one large one, a balance people also strike with cash (%s)." % S,
 "Form": "Common Transaction Forms names the shapes transactions usually take (%s)." % S,
 "SimplePayment": "The most common transaction is a simple payment with one input and two outputs, one of them change (%s)." % S,
 "Consolidation": "A consolidation transaction spends several inputs into one output, the real-world equivalent of exchanging a pile of coins for a single note (%s)." % S,
 "Unit": "Amounts can be fractional, down to a smallest indivisible unit (%s)." % S,
 "Satoshi": "A bitcoin divides into units from the millibitcoin, a thousandth, down to the satoshi, a hundred-millionth, so a millibitcoin is 100,000 satoshis (%s)." % S,
 "Network": "Constructing a Transaction and Adding the Transaction to the Blockchain follow the payment from Alice's wallet onto the network (%s)." % S,
 "Propagation": "A transaction does not need a central server: Getting the Right Inputs, Creating the Outputs and transmitting it are all done by the wallet (%s)." % S,
 "TransactionPropagation": "Once signed, the transaction is transmitted to the network and relayed by nodes until miners hold it (%s)." % S,
 "BlockExplorer": "Block explorers such as Mempool.Space let anyone look up a transaction or block - and a Bitcoin Overview warning says the operator may learn what you look up (%s)." % S,
 "Blockchain": "The blockchain is the authoritative journal of all transactions, produced by miners through competitive computation (%s)." % S,
 "Mining": "The Bitcoin Mining section explains how transactions become part of that journal (%s)." % S,
 "Block": "Transactions are bundled into blocks whose small header needs an enormous amount of computation to form correctly but little to verify (%s)." % S,
 "ConsensusRules": "Miners can only earn honest income from blocks that follow all of Bitcoin's consensus rules, so they are incentivised to include only valid transactions (%s)." % S,
 "Security": "Spending the Transaction shows how confidence in a payment grows over time (%s)." % S,
 "Confirmation": "Each block on top adds a confirmation; Nakamoto's paper computes that an attacker with a tenth of the hash power catches up from six blocks behind with probability 0.0002428 (%s)." % N,
 "GenesisBlock": "Every block links back through hundreds of thousands of blocks to block number 0, the genesis block (%s)." % S,
 "Semantics": "The course theme of semantic technologies meets the chapter in its transaction chain (%s)." % P,
 "ProvenanceModel": "A chain of spends is a record of where each value came from - a provenance record (%s)." % P,
 "ProvenanceGraph": "W3C's PROV Ontology describes entities derived from other entities by activities and attributed to agents, which is exactly the shape of outputs spent by transactions signed by key holders (%s)." % P,
}
BODY.update({
 "PaymentRequest": "Buying from an Online Store shows the invoice Alice's wallet scans (Antonopoulos and Harding, 2023).",
 "Bip21Uri": "The invoice QR code encodes a URI defined in BIP21 with the address, the payment amount 0.01577764, the label Bob's Store and a message, so Alice never types an address (Antonopoulos and Harding, 2023).",
 "UnconfirmedTransaction": "A payment first shows as unconfirmed: propagated but not yet in a block, and blocks arrive every 10 minutes on average rather than on a timetable - the ten-minute misconception the course notes warn about (Altunel, 2021).",
 "SmallPaymentAcceptance": "Selling a cheap item unconfirmed carries low double-spend risk, as coffee shops accept small card payments without a signature, while an expensive item justifies waiting for confirmations (Antonopoulos and Harding, 2023).",
 "SudokuAnalogy": "The course notes picture mining as a giant competitive sudoku - hard to solve, easy to verify, harder or easier by grid size, and restarted after each solution - an analogy the 3rd edition does not use (Altunel, 2021).",
 "Practice": "The course notes point students to an interactive demonstration of the chain of hashes this chapter describes (Altunel, 2021).",
 "InteractiveDemo": "Seeing a hash chain break is more convincing than reading about it (Altunel, 2021).",
 "BlockchainDemo": "Anders Brownworth's Blockchain Demo shows that changing one character in an earlier block invalidates every later block, which is what makes the journal tamper-evident (Altunel, 2021).",
})
