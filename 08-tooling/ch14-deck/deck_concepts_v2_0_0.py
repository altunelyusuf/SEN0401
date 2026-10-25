"""The key concepts of chapter 14 for the deck 2.0.0 (Second-Layer Applications; a NEW file, nothing earlier is edited).
The 61 concepts are the primary-source concepts of the research file 03-materials/ch14/rdodi/sen0401_ch14_research_v1_0_0.ttl (69 labels; eight repeat a label of an earlier one in other letter case,
so the deck standard check counts 61), which the deck standard check reads for D4 and D11. Here they are in four parts, each with a one-sentence meaning and one everyday analogy
(the owner's rule: every key concept has an everyday comparison). A card reads: the concept, its meaning, then 'Think of ...'. The label is written exactly as in the research."""
__version__ = "2.0.0"

BRANCHES = ["Guarantees", "ColoredCoins", "PaymentChannels", "Lightning"]
LAB = {"Guarantees": "What the chain guarantees", "ColoredCoins": "Colored coins and seals", "PaymentChannels": "Payment channels", "Lightning": "The Lightning Network"}
SHORT = {"Guarantees": "Guarantees", "ColoredCoins": "Colored coins", "PaymentChannels": "Channels", "Lightning": "Lightning"}

L1 = {
    "Guarantees": "The chain is a toolbox of guarantees; an application is a recipe.",
    "ColoredCoins": "A colored coin is a banknote stamped with a second meaning.",
    "PaymentChannels": "A payment channel is a bar tab: many small orders, one bill at closing time.",
    "Lightning": "Lightning is a chain of couriers who pass a parcel on and each keep a small fee.",
}

# groups of a part, in order: (key, pill (at most 4 words), meaning, analogy)
GROUPS = {
    "Guarantees": [
        ("Primitives", "The building blocks", "Guarantees such as no double spend and immutability can be reused by any application.", "bricks that fit many buildings"),
        ("Applications", "Applications from blocks", "A digital notary and a crowdfund each mix several guarantees.", "a recipe that mixes basic ingredients"),
    ],
    "ColoredCoins": [
        ("Seals", "Single-use seals", "An unspent output can be tied to a statement only once, when it is spent.", "a tamper seal that breaks when opened"),
        ("P2C", "Pay to contract", "A key is tweaked so that it commits to a contract nobody else sees.", "an invisible engraving on a key"),
        ("CSV", "Client-side validation", "The receiver checks the whole history of an asset; the chain holds only commitments.", "a buyer reading a car's service book"),
    ],
    "PaymentChannels": [
        ("Channel", "Funding and settling", "Two transactions on the chain, and any number of signed updates between them.", "opening and closing a bar tab"),
        ("Revocable", "Revocable commitments", "Each side's payout is delayed, and an old state can be punished with a revocation key.", "a contract that forfeits the safe to a cheat"),
        ("Htlc", "Hash time locks", "A secret claims the payment before a deadline; after it the payer takes the money back.", "a locker with a code and a return date"),
    ],
    "Lightning": [
        ("Routing", "Routing and fees", "A payment crosses several channels, and each relay keeps a small fee.", "parcel couriers who each take a fee"),
        ("Onion", "Onion routing", "The sender wraps the path in layers, and each relay peels exactly one.", "pass-the-parcel at a party"),
        ("Invoices", "Invoices and BOLTs", "A payee's invoice names an amount and a hash; the BOLTs are the shared standards.", "a bill and the plug standards"),
    ],
}

# every key concept: label -> (part, meaning, analogy without 'Think of' and without the closing full stop)
K3 = {
    # ---- part 1: what the chain guarantees
    "Second-Layer Applications": ("Guarantees", "services built on Bitcoin's first layer that use its guarantees and change none of its rules.", "shops on a busy high street that never rebuild the road"),
    "Building Blocks (Primitives)": ("Guarantees", "the guarantees Bitcoin offers, which every application may reuse.", "bricks that fit many different buildings"),
    "Applications from Building Blocks": ("Guarantees", "each application mixes several guarantees, as a digital notary mixes immutability, a timestamp and durability.", "a recipe that mixes a few basic ingredients"),
    "second layer": ("Guarantees", "a system that settles on the chain but does most of its work away from it.", "a tram line that meets the main railway at a few stations"),
    "primitives": ("Guarantees", "the basic guarantees themselves, small enough to be combined in many ways.", "the notes of a scale that every song is built from"),
    "no double spend": ("Guarantees", "no output can be spent twice in the same valid chain of blocks.", "a cheque that the bank cashes only once"),
    "immutability": ("Guarantees", "the more work lies on top of a transaction, the more energy it takes to rewrite it.", "wet concrete that sets harder every hour"),
    "neutrality": ("Guarantees", "the network relays any valid transaction with a sufficient fee, whoever sends it.", "a post office that stamps every parcel with enough postage"),
    "secure timestamping": ("Guarantees", "the consensus rules keep block times roughly honest, so a recorded fact has a trusted date.", "a postmark that the sender cannot choose"),
    "authorization": ("Guarantees", "a script that asks for a signature cannot run without the holder of the private key.", "a door that opens only to its owner's key"),
    "auditability": ("Guarantees", "every transaction is public and links back to the genesis block.", "a ledger that anyone may read from the first page"),
    "accounting": ("Guarantees", "outputs never exceed inputs, so a transaction cannot create or destroy value.", "a till that must balance to the last coin"),
    "nonexpiration": ("Guarantees", "a valid transaction stays valid for as long as its inputs are unspent.", "a cheque with no expiry date"),
    "integrity": ("Guarantees", "a signature covers the parts of a transaction it commits to, so they cannot be altered.", "a wax seal that breaks if the letter is changed"),
    "transaction atomicity": ("Guarantees", "a transaction is mined in full or not at all, never halfway.", "a light switch: on or off, never half"),
    "quorum of control": ("Guarantees", "a multisignature script demands a set number of keys, such as two of two.", "a safe that needs two keyholders"),
    "timelock": ("Guarantees", "a script clause can run only after a set time or block height.", "a bank vault on a time lock"),
    "replication": ("Guarantees", "every full node keeps a copy of the chain, so the data survives local failures.", "the same book on the shelves of many libraries"),
    "forgery protection": ("Guarantees", "a transaction can spend only existing, validated outputs, so value cannot be counterfeited.", "a bank that checks every note against its register"),
    "consistency": ("Guarantees", "the deeper a block lies, the less likely it is to be reorganised.", "footprints in drying cement: the older, the firmer"),
    "recording external state": ("Guarantees", "a transaction can commit to outside data through OP_RETURN or pay to contract.", "a notary who stamps a page of someone else's contract"),
    "predictable issuance": ("Guarantees", "fewer than 21 million bitcoin will ever exist, issued at a known rate.", "a mint that follows a published timetable"),
    "proof of existence": ("Guarantees", "a document's hash in a transaction proves the document existed when that block was mined.", "a notary's date stamp on a sealed envelope"),
    "Lighthouse": ("Guarantees", "a crowdfunding application whose pledges are signed inputs, spendable only when the goal is met.", "a street collection that pays out only when the target is reached"),
    # ---- part 2: colored coins and seals
    "Colored Coins": ("ColoredCoins", "a small amount of bitcoin is marked so that it stands for another asset, such as a share.", "a banknote stamped 'this is a stock certificate'"),
    "Single-Use Seals": ("ColoredCoins", "a data structure that can be tied to another only once; an unspent output does that.", "a tamper seal on a parcel that breaks when opened"),
    "Pay to Contract (P2C)": ("ColoredCoins", "a public key is tweaked so that it commits to a contract that nobody else sees.", "a key with an invisible engraving of the agreement"),
    "Client-Side Validation": ("ColoredCoins", "the receiver checks the whole history of an asset; the chain holds only commitments.", "a buyer who reads a car's whole service book"),
    "RGB": ("ColoredCoins", "a colored coin protocol made to work with channels, built from seals, contracts and client checks.", "a club with its own rules, meeting in a public hall"),
    "Taproot Assets": ("ColoredCoins", "a colored coin protocol, once called Taro, built around taproot-style contracts.", "foreign banknotes carried on the same railway"),
    "native forwarding": ("ColoredCoins", "every hop on a Lightning path must know the asset and hold a balance of it.", "a relay in which every courier handles the special parcel"),
    "translated forwarding": ("ColoredCoins", "only the first and last hops know the asset, and the hops between forward plain bitcoin.", "exchange booths at both ends of a bridge, plain coins in the middle"),
    # ---- part 3: payment channels
    "Payment Channels and State Channels": ("PaymentChannels", "two parties exchange signed transactions off the chain and settle on it later.", "a bar tab that is paid once, at closing time"),
    "State Channels - Basic Concepts and Terminology": ("PaymentChannels", "a funding transaction opens the channel, commitments change it, and a settlement closes it.", "opening, using and paying a hotel bill"),
    "Simple Payment Channel Example": ("PaymentChannels", "Emma pays Fabian for each second of video, and a signed refund protects her.", "a taxi meter that counts up while you ride"),
    "Making Trustless Channels": ("PaymentChannels", "signed refunds and lock times let each side leave safely without trusting the other.", "a deposit with a clause that returns it by a set date"),
    "Asymmetric Revocable Commitments": ("PaymentChannels", "each side holds a commitment that delays its own payout and can be punished once it is old.", "a contract that hands the safe to the other party if you cheat"),
    "Hash Time Lock Contracts (HTLC)": ("PaymentChannels", "a secret can claim the payment before a deadline, and the payer can reclaim it after.", "a locker opened by a code today, reclaimed by its owner tomorrow"),
    "payment channel": ("PaymentChannels", "two parties keep a running balance of signed transactions that they do not publish.", "a running tab between two friends"),
    "state channel": ("PaymentChannels", "the general form: any shared state is changed off the chain and secured by a final settlement.", "a score sheet that both players sign after every point"),
    "funding transaction": ("PaymentChannels", "the one transaction that locks the shared funds in a two-of-two output and opens the channel.", "the deposit paid into a joint account"),
    "commitment transaction": ("PaymentChannels", "a signed transaction that could be published but is held back and replaced by newer ones.", "a cheque kept in a drawer and replaced by a newer one"),
    "settlement transaction": ("PaymentChannels", "the final transaction that closes the channel and pays each side its share.", "the final bill at checkout"),
    "refund transaction": ("PaymentChannels", "a signed, time-locked transaction that returns the funds if the channel never starts.", "the return ticket bought before the journey"),
    "Spillman-style payment channel": ("PaymentChannels", "a one-way channel of 2013: ever larger signed payments, and a refund behind a lock time.", "a prepaid card that only goes down, with a refund date"),
    "revocation key": ("PaymentChannels", "a key of two secret halves that lets the wronged side take the whole channel after a cheat.", "a spare key to the cheater's safe, held by the victim"),
    "asymmetric commitment": ("PaymentChannels", "the two commitments differ: the holder's own payout waits, the other side is paid at once.", "two cheques where only the signer has to wait"),
    "preimage": ("PaymentChannels", "the secret that hashes to the value in an HTLC; whoever knows it can claim the payment.", "the original text behind a published fingerprint"),
    # ---- part 4: the Lightning Network
    "Routed Payment Channels (Lightning Network)": ("Lightning", "many channels linked end to end, so that anyone can pay anyone through intermediaries.", "a chain of couriers who pass a parcel hand to hand"),
    "Basic Lightning Network Example": ("Lightning", "Alice pays Eric one bitcoin through Bob, Carol and Diana, who each keep a small fee.", "parcel relays where each courier takes a fee"),
    "Lightning Network Transport and Pathfinding": ("Lightning", "nodes talk over encrypted links, share channel news by flooding, and the sender plans the path.", "a driver who plans a route from a shared road map"),
    "Lightning Network Benefits": ("Lightning", "privacy, fungibility, speed, granularity, capacity and trustless operation.", "express lanes beside an old toll road"),
    "Lightning Network": ("Lightning", "a network of payment channels that routes payments with hash time locks and onion packets.", "pneumatic tubes in an office building"),
    "route": ("Lightning", "the chain of channels from payer to payee that a payment will follow.", "the stops of a bus line"),
    "invoice": ("Lightning", "a payee's request for payment that carries an amount, a payment hash and an expiry.", "a bill with the payer's reference printed on it"),
    "onion routing": ("Lightning", "the sender wraps the path in layers, and each relay peels one and sees only the next hop.", "pass-the-parcel at a party"),
    "Sphinx": ("Lightning", "the packet format of the Lightning onion: fixed in size, with a check value for every hop.", "an envelope of one size, so thin and thick letters look alike"),
    "BOLT": ("Lightning", "Basis of Lightning Technology: the numbered specifications that let different programs work together.", "plug standards that let any appliance fit any socket"),
    "pathfinding": ("Lightning", "choosing a route with enough capacity and low fees, using the channel announcements.", "a satnav that knows how wide each road is"),
    "fee": ("Lightning", "a relay earns a fee for locking its funds while the payment is in flight.", "a toll collected at each bridge"),
    "capacity": ("Lightning", "the sum locked in a channel; a payment must fit in the balance on the sending side.", "a pipe that carries no more than its width"),
}
