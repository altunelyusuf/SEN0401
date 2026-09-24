"""SEN0401 chapter 1 (Mastering Bitcoin 3rd edition, Introduction) for the RDODI build.
Every claim was read on 2026-09-25 from the source it cites; every computation executed under Python 3.14.4."""
CH = 1
TITLE = "Bitcoin from first principles: chapter 1 of Mastering Bitcoin, 3rd edition, and Bitcoin today"
QUESTION = "What does chapter 1 of Mastering Bitcoin's 3rd edition establish about Bitcoin as money, network and wallet, what has changed since its December 2023 publication, and where does it meet the course theme of semantic technologies?"
PUBS = [
 ("P01","Mastering Bitcoin, 3rd edition - Chapter 1, Introduction (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)","https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch01_intro.adoc",True),
 ("P02","Bitcoin: A Peer-to-Peer Electronic Cash System (Nakamoto, 2008)","https://bitcoin.org/bitcoin.pdf",False),
 ("P03","Hashcash - A Denial of Service Counter-Measure (Back, 2002)","http://www.hashcash.org/papers/hashcash.pdf",False),
 ("P04","Bitcoin Core releases (Bitcoin Core project)","https://bitcoincore.org/en/releases/",False),
 ("P05","Controlled supply - Bitcoin Wiki","https://en.bitcoin.it/wiki/Controlled_supply",False),
 ("P06","BIP 39 - Mnemonic code for generating deterministic keys (Palatinus, Rusnak, Voisine and Bowe, 2013)","https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki",False),
 ("P07","Decentralized Identifiers (DIDs) v1.0, W3C Recommendation, 9 July 2022","https://www.w3.org/TR/did-core/",False),
 ("P08","Verifiable Credentials Data Model v2.0, W3C Recommendation, 5 May 2025","https://www.w3.org/TR/vc-data-model-2.0/",False),
]
CONCEPTS = [("Section",x) for x in ("Introduction","History of Bitcoin","Getting Started","Choosing a Bitcoin Wallet","Types of Bitcoin wallets","Full node versus Lightweight","Who controls the keys","Quick Start","Recovery Codes","Bitcoin Addresses","Receiving Bitcoin","Getting Your First Bitcoin","Finding the Current Price of Bitcoin","Sending and Receiving Bitcoin")] + \
 [("Concept",x) for x in ("proof of work","consensus","double-spend","recovery code","floating exchange rate","noncustodial wallet","full node","lightweight client","desktop wallet","mobile wallet","web wallet")]
FINDINGS = [
 ("F1","Background","Chapter 1 presents Bitcoin as money, network and software: bitcoin the unit with a small b and Bitcoin the system with a capital B; its history from a 2008 paper by Satoshi Nakamoto and a network started in 2009; proof of work as a lottery run every 10 minutes on average that lets a decentralized network reach consensus and solves the double-spend; a supply just below 21 million; and a practical start - choosing a wallet by platform and by node type, who controls the keys, recovery codes, addresses, receiving, pricing and sending.",["P01"]),
 ("F2","Contemporary developments","Since the book's publication the subsidy halved at block 840000 on 2024-04-20 to 3.125 bitcoin per block, and the reference implementation it describes has moved on: Bitcoin Core's releases page lists 31.1 as the newest.",["P05","P04"]),
 ("F3","Comparative analysis","The chapter's claims can be checked against its sources and by computation: Nakamoto's paper proposes a purely peer-to-peer electronic cash system, and proof of work descends from Back's Hashcash, first proposed to throttle abuse; the supply schedule sums to 20999999.9769 bitcoin, just below 21 million as the book says; and the recovery codes the book shows follow BIP 39, whose initial entropy is 128 to 256 bits.",["P02","P03","P05","P06"]),
 ("F4","Conclusion","For SEN0401's theme of semantic technologies, the chapter's key idea - control by whoever holds the keys, with no central registry - is the same idea W3C standardised for identity in Decentralized Identifiers and Verifiable Credentials, which gives projects a bridge from the book to semantic web standards.",["P01","P07","P08"]),
]
TAX = [
 ("Money","Unit","BitcoinUnit","bitcoin with a small b, Bitcoin with a capital B","The unit of currency is bitcoin with a small b; the system is Bitcoin with a capital B.",None),
 ("Money","Supply","SupplyCap","the sum of every block subsidy","New bitcoin is created on a schedule that halves the subsidy every 210000 blocks, so the total supply stays just below 21 million.",("sum((50 * 10**8 >> era) * 210000 for era in range(33)) / 10**8","20999999.9769")),
 ("Money","Supply","Halving","the subsidy after four halvings","The block subsidy halves every 210000 blocks; after the halving at block 840000 on 2024-04-20 it is 3.125 bitcoin.",("(50 * 10**8 >> 4) / 10**8","3.125")),
 ("Money","Price","FloatingExchangeRate","the BTC/USD rate","The price of bitcoin is set by markets: a floating exchange rate that moves with supply and demand.",None),
 ("Network","Consensus","ProofOfWork","a toy search for a hash starting with 0000","Proof of work makes adding a block costly and easy to check; a toy version searches for a number whose SHA-256 hash starts with zeros.",("next(n for n in range(10**6) if __import__('hashlib').sha256(f'SEN0401-{n}'.encode()).hexdigest().startswith('0000'))","15083")),
 ("Network","Consensus","DoubleSpend","spending the same coin twice","The double-spend problem - spending one unit twice - which Bitcoin's consensus solves without a central clearinghouse.",None),
 ("Network","History","Whitepaper","Bitcoin: A Peer-to-Peer Electronic Cash System","The 2008 paper by Satoshi Nakamoto that first described Bitcoin.",None),
 ("Network","History","ReferenceImplementation","Bitcoin Core","The software Nakamoto published in 2009, since revised by many programmers; Bitcoin Core's newest listed release is 31.1.",None),
 ("Wallet","WalletPlatform","DesktopWallet","a desktop wallet","The first type of Bitcoin wallet, run on a general-purpose operating system.",None),
 ("Wallet","WalletPlatform","MobileWallet","a mobile wallet","The most common type of Bitcoin wallet, run on a smartphone.",None),
 ("Wallet","WalletPlatform","WebWallet","a web wallet","A wallet used through a web browser.",None),
 ("Wallet","NodeType","FullNode","a full node","A program that validates the entire history of Bitcoin transactions itself.",None),
 ("Wallet","NodeType","LightweightClient","a lightweight client","A client that relies on others for validation instead of checking every transaction itself.",None),
 ("Wallet","KeyControl","NoncustodialWallet","a noncustodial wallet","A wallet where only the user holds the keys - who controls the keys controls the bitcoin.",None),
 ("Wallet","Backup","RecoveryCode","a list of twelve words","A recovery code of words, numbers or letters chosen by the wallet from which its keys are generated; the book's samples follow BIP 39.",None),
 ("Usage","Address","BitcoinAddress","an address shown as a QR code","A number derived from the private key that others use to pay you; a new one per invoice protects privacy.",None),
 ("Usage","Transfer","SendingAndReceiving","Alice paying Joe","Receiving shows an address or invoice; sending signs a transaction that spends to someone else's address.",None),
 ("Usage","SemanticBridge","DecentralizedIdentity","a DID controlled by its holder","W3C Decentralized Identifiers apply the same principle to identity: control by whoever holds the keys, with no central registry.",None),
]
S = "Antonopoulos and Harding, 2023"; N = "Nakamoto, 2008"; BK = "Back, 2002"; W = "Bitcoin Wiki, 2026"; C = "Bitcoin Core, 2026"; B39 = "Palatinus et al., 2013"; DID = "World Wide Web Consortium, 2022"; VC = "World Wide Web Consortium, 2025"
BODY = {
 "Money": "Bitcoin is first of all money: a unit of account that is stored and transmitted among participants in the Bitcoin network (%s)." % S,
 "Unit": "The chapter's Introduction fixes the vocabulary before anything else, and the capital letter matters (%s)." % S,
 "BitcoinUnit": "The unit of currency is bitcoin with a small b, and the system is Bitcoin with a capital B, so a student who writes about both must keep the two apart (%s)." % S,
 "Supply": "Bitcoin's supply follows a schedule written into the software rather than a decision by any authority (%s)." % S,
 "SupplyCap": "The schedule creates bitcoin in eras of 210000 blocks, halving each time, so the sum of every subsidy is 20999999.9769 bitcoin - just below 21 million, as the chapter says (%s)." % W,
 "Halving": "The subsidy halved at block 840000 on 2024-04-20, after the book was published, to 3.125 bitcoin per block (%s)." % W,
 "Price": "The section Finding the Current Price of Bitcoin answers who sets the price: nobody does, markets do (%s)." % S,
 "FloatingExchangeRate": "Bitcoin has a floating exchange rate: its value moves with supply and demand in the markets where it is traded, and pricing services average those markets (%s)." % S,
 "Network": "Bitcoin is also a network of participants that agree on transactions without a central authority (%s)." % S,
 "Consensus": "Consensus is the network's agreement about the state of transactions, reached without a trusted party (%s)." % S,
 "ProofOfWork": "Proof of work runs a global lottery every 10 minutes on average that lets the decentralized network reach consensus; it descends from Hashcash, which used costly computation to throttle abuse (%s)." % BK,
 "DoubleSpend": "Proof of work solves the double-spend, the weakness of earlier digital currencies that had been handled only by clearing every transaction through a central clearinghouse (%s)." % S,
 "History": "The History of Bitcoin section traces the system from a paper to a running network (%s)." % S,
 "Whitepaper": "Bitcoin was first described in 2008 in Bitcoin: A Peer-to-Peer Electronic Cash System, a paper written under the name Satoshi Nakamoto that proposes a purely peer-to-peer version of electronic cash (%s)." % N,
 "ReferenceImplementation": "The network started in 2009 from a reference implementation published by Nakamoto and revised since by many programmers; Bitcoin Core's releases page now lists 31.1 as its newest release (%s)." % C,
 "Wallet": "Getting Started turns to the wallet, the software through which people actually use Bitcoin, and Choosing a Bitcoin Wallet warns that the choice depends on use and expertise rather than any single brand (%s)." % S,
 "WalletPlatform": "The section Types of Bitcoin wallets sorts wallets first by the platform they run on (%s)." % S,
 "DesktopWallet": "A desktop wallet was the first type of Bitcoin wallet, created as a reference implementation, and runs on general-purpose operating systems whose security is often weak (%s)." % S,
 "MobileWallet": "A mobile wallet is the most common type of Bitcoin wallet, running on smartphone operating systems such as iOS and Android (%s)." % S,
 "WebWallet": "Web wallets are accessed through a web browser, which makes them convenient and places trust in whoever runs the service (%s)." % S,
 "NodeType": "The section Full node versus Lightweight sorts wallets by how much of the network's work they do themselves (%s)." % S,
 "FullNode": "A full node validates the entire history of Bitcoin transactions itself, so it depends on nobody else for the truth of the ledger (%s)." % S,
 "LightweightClient": "A lightweight client relies on other nodes for validation, trading some independence for convenience (%s)." % S,
 "KeyControl": "The section Who controls the keys asks the question that decides who really owns the bitcoin (%s)." % S,
 "NoncustodialWallet": "In a noncustodial wallet only the user holds the keys, so only the user can spend - and only the user can lose access (%s)." % S,
 "Backup": "Because the user holds the keys, the user must also be able to restore them, which is what the section Recovery Codes is about (%s)." % S,
 "RecoveryCode": "A recovery code is a list of words, numbers or letters chosen randomly by the wallet and used as the basis for its keys; the book's samples follow BIP 39, whose initial entropy is 128 to 256 bits (%s)." % B39,
 "Usage": "The rest of the chapter follows Alice through Quick Start, Getting Your First Bitcoin, and Sending and Receiving Bitcoin (%s)." % S,
 "Address": "The section Bitcoin Addresses explains what a user gives others in order to be paid (%s)." % S,
 "BitcoinAddress": "A Bitcoin address is derived from the user's private key and registered nowhere; sharing it lets others pay but never withdraw, and a new address for each invoice protects privacy (%s)." % S,
 "Transfer": "Receiving Bitcoin and Sending and Receiving Bitcoin show the two directions of a payment (%s)." % S,
 "SendingAndReceiving": "To receive, a wallet shows an address or invoice, often as a QR code; to send, the wallet signs a transaction spending to the recipient's address (%s)." % S,
 "SemanticBridge": "The course theme of semantic technologies meets the chapter at its central idea: control by whoever holds the keys, without a central registry (%s)." % DID,
 "DecentralizedIdentity": "W3C's Decentralized Identifiers apply that idea to identity, and Verifiable Credentials build signed claims on top of it, so a project can carry the chapter's key principle into semantic web standards (%s)." % VC,
}
