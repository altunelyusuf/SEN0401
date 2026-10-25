"""The key concepts of chapter 1 for the deck 3.0.0: the 33 distinct primary-source concepts of the chapter research (03-materials/ch01/rdodi/sen0401_ch01_research_v1_2_0.ttl, de-duplicated by
normalised label as the deck standard check does), each with the part of the deck it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line meaning and
analogy of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept, its meaning, then 'Think of ...'. The meanings follow the chapter's own definitions in the
chapter corpus (sen0401_ch01_corpus_v1_2_0.py). NEW file; nothing earlier is edited."""
__version__ = "3.0.0"

PARTS = ["Origins", "Money", "Network", "Wallets", "FirstUse", "Foundations"]
PART_LABEL = {"Origins": "Origins", "Money": "Money and price", "Network": "The network", "Wallets": "Wallets and keys", "FirstUse": "A first payment", "Foundations": "Foundations"}
PART_SHORT = {"Origins": "Origins", "Money": "Money", "Network": "Network", "Wallets": "Wallets", "FirstUse": "First use", "Foundations": "Basics"}

# level 1: divider subtitle (carries the meaning and the analogy of the part)
L1 = {
    "Origins": "Bitcoin combines old parts, like a recipe of familiar ingredients.",
    "Money": "Money is a ledger of who owns what; Bitcoin keeps that ledger in public.",
    "Network": "No bank sits in the middle: shared rules and shared work do its job.",
    "Wallets": "A wallet holds keys, not coins, like a ring of keys to many safes.",
    "FirstUse": "From an empty wallet to a first payment, like a first driving lesson.",
    "Foundations": "Two old solved problems, joined into one system, like two rivers.",
}

# level 2: (pill, meaning, analogy)   pill at most 4 words
L2 = {
    "Origins": [("The first block", "Block 0 carries a newspaper headline dated 3 January 2009.", "a time capsule sealed with that day's paper"),
                ("The first payment", "Satoshi sent ten bitcoin to Hal Finney nine days later.", "the first coin dropped into a new machine"),
                ("Forty years before", "Chaum, Back, Dai and Szabo each built a part first.", "the wheel, chain and frame before the bicycle")],
    "Money": [("What money was", "Stones, coins, notes and bank balances are all ledgers.", "a scoreboard that everyone agrees to trust"),
              ("Units and supply", "One coin divides into 100 million satoshis; the cap is 21 million.", "a cake cut into a hundred million crumbs"),
              ("Price and exchange", "Markets set the price; exchanges and ATMs convert it.", "a market stall whose prices change by the hour")],
    "Network": [("Peers, not a bank", "Every node checks the same rules, so none is in charge.", "neighbours who all keep a copy of the land register"),
                ("Work and agreement", "Proof of work makes honest history cheap to check.", "a lock that took a day to make and a second to inspect"),
                ("Fees and depth", "Fees pay miners; each new block makes a payment safer.", "a courier's tip and cement poured over a footprint")],
    "Wallets": [("Kinds of wallet", "Desktop, mobile, web and hardware wallets differ in risk.", "a pocket, a safe and a cloakroom ticket"),
                ("Nodes and clients", "A full node checks everything; a light client trusts others.", "an auditor beside a tourist with a map"),
                ("Keys and backup", "Whoever holds the keys controls the coins; a recovery code restores them.", "a spare key kept in a bank locker")],
    "FirstUse": [("Getting bitcoin", "Buy it, earn it, or use an exchange or an ATM.", "swapping money at an airport booth"),
                 ("Addresses and invoices", "An address says where; an invoice adds the amount.", "a mailbox number and a bill with the sum"),
                 ("Receiving and sending", "Receiving shows an address; sending signs a transaction.", "giving and taking change at a till")],
    "Foundations": [("Two old problems", "Hashcash made messages cost work; the generals agreed without trust.", "two rivers that meet in one channel"),
                    ("Payments off-chain", "Payment channels keep most payments off the public ledger.", "a bar tab settled once at closing time"),
                    ("What kind of thing", "Virtual, borderless, decentralized and robust, by design.", "a public library no single person owns")],
}

# key concepts: label as in the research -> (part, meaning, analogy)
K3 = {
    "Introduction": ("Origins", "The chapter that says what Bitcoin is and why it matters.", "the welcome page of a guidebook, before the maps"),
    "History of Bitcoin": ("Origins", "The path from earlier digital money to the first block in January 2009.", "a family tree that shows who the new member descends from"),
    "floating exchange rate": ("Money", "The price of bitcoin is set by markets and moves with supply and demand.", "the price of tomatoes at a stall, which moves with the harvest and the crowd"),
    "Finding the Current Price of Bitcoin": ("Money", "Exchanges quote prices; a volume-weighted average gives one fair daily figure.", "reading the board of a stock exchange instead of asking one trader"),
    "currency exchange": ("Money", "A market where buyers and sellers swap bitcoin and local money, with identity checks.", "the money-changer's booth at an airport"),
    "Bitcoin ATM": ("Money", "A machine that takes cash and sends bitcoin to your phone wallet.", "a vending machine that sells coins instead of snacks"),
    "proof of work": ("Network", "Adding a block costs real computation, and anyone can check it cheaply.", "a jigsaw puzzle: hard to solve, a glance to see it is done"),
    "consensus": ("Network", "Every node applies the same rules, so all agree on one history without a leader.", "neighbours who all keep the same record of who owns which field"),
    "double-spend": ("Network", "Spending one unit of digital money twice; the network refuses the second try.", "photocopying a banknote and paying with both"),
    "confirmation": ("Network", "Each block added after a payment makes the payment harder to reverse.", "another layer of cement poured over a footprint"),
    "transaction fee": ("Network", "The amount a sender adds for the miner who puts the payment in a block.", "a tip for the courier who picks your parcel for the next van"),
    "Getting Started": ("Wallets", "The first decisions: what a wallet is and which one to choose.", "choosing a bag before you go shopping"),
    "Choosing a Bitcoin Wallet": ("Wallets", "Pick a wallet by who holds the keys, which device it runs on, and how far you trust it.", "choosing between a pocket, a home safe and a bank locker"),
    "Types of Bitcoin wallets": ("Wallets", "Desktop, mobile, web and hardware signing devices, each with its own trade-offs.", "a bicycle, a car and a bus: all travel, with different limits"),
    "desktop wallet": ("Wallets", "The first kind of wallet, run on Windows, macOS or Linux.", "the cash register on the shop counter"),
    "mobile wallet": ("Wallets", "The most common kind of wallet, run on a smartphone.", "the purse in your pocket"),
    "web wallet": ("Wallets", "Used through a browser; its data usually sits on someone else's server.", "leaving your coat at a cloakroom"),
    "hardware signing device": ("Wallets", "A small device that keeps keys inside and signs payments.", "a stamp kept in a locked drawer: paper goes in, stamped paper comes out"),
    "third-party API client": ("Wallets", "A program that asks a remote service for data instead of the Bitcoin network.", "asking a travel agent instead of reading the timetable yourself"),
    "full node": ("Wallets", "Software that checks the whole history of transactions by itself.", "an auditor who rereads every page of the ledger"),
    "lightweight client": ("Wallets", "Keeps your keys but relies on other nodes for most of the data.", "a tourist who asks locals for directions instead of studying the whole map"),
    "Full node versus Lightweight": ("Wallets", "Independence and storage on one side, convenience and trust on the other.", "cooking from raw ingredients against buying a ready meal"),
    "Who controls the keys": ("Wallets", "Whoever holds the private keys controls the coins.", "whoever holds the house keys controls the house"),
    "noncustodial wallet": ("Wallets", "A wallet where only you hold the keys, so only you can spend or lose the coins.", "a safe in your own home with the only key in your pocket"),
    "Recovery Codes": ("Wallets", "Twelve or more words from which all of a wallet's keys can be rebuilt.", "a master key in a bank locker that can cut every lost key again"),
    "Quick Start": ("FirstUse", "The chapter's first payment: install a wallet, share an address, receive bitcoin.", "a first driving lesson in an empty car park"),
    "Bitcoin Addresses": ("FirstUse", "Receiving addresses: make a fresh one for each payer to protect your privacy.", "a new locker number for every delivery"),
    "Bitcoin address": ("FirstUse", "The destination of a payment, derived from your private key and registered nowhere.", "a postbox anyone may drop money into but only you can empty"),
    "invoice": ("FirstUse", "A payment request, often a QR code, that carries an address and an amount.", "a bill with the account number and the sum printed on it"),
    "Receiving Bitcoin": ("FirstUse", "Show an address or an invoice; the payment appears once it is broadcast.", "handing a customer the payment slip of your shop"),
    "Getting Your First Bitcoin": ("FirstUse", "Buy from a friend, earn it, or use an exchange or an ATM.", "your first foreign money: you can swap for it, earn it or be given it"),
    "Sending and Receiving Bitcoin": ("FirstUse", "Receiving shows an address; sending signs a transaction to someone else's.", "giving and taking change at a till"),
    "offchain technology": ("Foundations", "Payments that move value without recording each one on the public chain.", "a bar tab that is settled once at closing time"),
}
