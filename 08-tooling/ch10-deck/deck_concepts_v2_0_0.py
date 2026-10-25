"""The key concepts of chapter 10 for the deck 2.0.0: the 56 distinct primary-source concepts of the chapter research (03-materials/ch10/rdodi/sen0401_ch10_research_v1_2_0.ttl, de-duplicated by
normalised label as the deck standard check does), each with the part of the chapter it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line meaning and
analogy of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept (its label exactly as the research names it), its meaning, then 'Think of ...'.
NEW file; nothing earlier is edited."""
__version__ = "2.0.0"

PARTS = ["WhoIsOnTheNetwork", "PeersBlocksTransactions", "LightClientsPrivacyTransport"]
LABEL = {"WhoIsOnTheNetwork": "Who is on the network", "PeersBlocksTransactions": "Peers, blocks and transactions", "LightClientsPrivacyTransport": "Light clients, privacy and transport"}
SHORT = {"WhoIsOnTheNetwork": "Who is on it", "PeersBlocksTransactions": "Peers and blocks", "LightClientsPrivacyTransport": "Light and private"}

# level 1: divider subtitle (carries the meaning and the analogy of the part)
L1 = {
    "WhoIsOnTheNetwork": "Like a village market with no manager: every stall only talks to its neighbours.",
    "PeersBlocksTransactions": "Like a postal service without a post office: letters pass from hand to hand.",
    "LightClientsPrivacyTransport": "Like a tourist with a map: ask the locals, and mind what your question gives away.",
}

# level 2: part -> list of (pill, meaning, analogy)   pill at most 4 words
L2 = {
    "WhoIsOnTheNetwork": [
        ("Nodes and roles", "Full, archival, pruned and light nodes keep different data.", "a town where some keep the whole archive and others a pocket diary"),
        ("The handshake", "Two nodes swap version and verack before anything else.", "two strangers who exchange names before they talk"),
        ("Services", "A node announces what it offers in one bit field.", "a shop window that lists what is on sale"),
    ],
    "PeersBlocksTransactions": [
        ("Finding peers", "DNS seeds and addr messages give a new node its first neighbours.", "a newcomer who asks the phone directory, then friends"),
        ("Connections", "Eight full-relay and two block-relay-only links, at most 125 in all.", "a switchboard with a fixed number of lines"),
        ("Blocks", "Headers come first; compact blocks send only what is missing.", "a contents page first, then only the missing chapters"),
        ("Transactions", "Payments wait in each node's own pool until a block takes them.", "each shop's own waiting list of orders"),
    ],
    "LightClientsPrivacyTransport": [
        ("Light clients", "A Merkle path proves a payment to a client with only headers.", "a name proved from the headings on its path"),
        ("Bloom filters", "A fuzzy guest list that leaks which addresses a wallet owns.", "a guest list that admits a few strangers"),
        ("Block filters", "One small filter per block lets the client ask nothing at all.", "a library that posts each day's index"),
        ("Transport", "Version 2 encrypts peer traffic; Tor and I2P hide who is who.", "a sealed envelope, and a note passed through friends"),
    ],
}

# the key concepts: label (exactly as the research names it) -> (part, meaning, analogy)
K3 = {
    # ---- part A ----------------------------------------------------------------------------------------------------------------
    "The Network": ("WhoIsOnTheNetwork", "The computers that follow the same rules and pass the same messages.", "a road system that no single company owns"),
    "Bitcoin": ("WhoIsOnTheNetwork", "A money system and a network, run by software that anyone may run.", "an open recipe book that every kitchen cooks from"),
    "peer-to-peer networks, Bitcoin as": ("WhoIsOnTheNetwork", "Every participant is both client and server, and nobody is in charge.", "a village market with no manager"),
    "Bitcoin network": ("WhoIsOnTheNetwork", "The nodes that speak the Bitcoin protocol to each other over TCP.", "a club whose members all speak one dialect"),
    "Node Types and Roles": ("WhoIsOnTheNetwork", "Nodes differ in what they store and what they do for others.", "a town where some keep the archive and others a diary"),
    "nodes": ("WhoIsOnTheNetwork", "A node is a computer that runs Bitcoin software and joins the network.", "a post office in a national postal system"),
    "Full Nodes": ("WhoIsOnTheNetwork", "A full node checks every block and transaction itself and trusts no one.", "an auditor who rechecks every receipt in person"),
    "archival full nodes": ("WhoIsOnTheNetwork", "A full node that keeps every block since the first.", "a library that never throws a book away"),
    "peers": ("WhoIsOnTheNetwork", "The other nodes that one node is directly connected to.", "the neighbours you can call without a go-between"),
    "Bitcoin Core": ("WhoIsOnTheNetwork", "The reference software, written by volunteers, that most nodes run.", "the standard edition of the recipe book, with many editors"),
    "mining": ("WhoIsOnTheNetwork", "The work of finding new blocks; miners also run nodes.", "a lottery whose winner writes the next page of the ledger"),
    # ---- part B ----------------------------------------------------------------------------------------------------------------
    "Network Discovery": ("PeersBlocksTransactions", "A new node finds its first peers, then learns about many more.", "a newcomer who asks the phone directory, then friends"),
    "DNS seeds": ("PeersBlocksTransactions", "Servers that answer a DNS query with addresses of reachable nodes.", "a phone directory that hands out a few numbers"),
    "blocks": ("PeersBlocksTransactions", "A block bundles transactions and names the block before it.", "a ledger page that cites the page before it"),
    "blockchain": ("PeersBlocksTransactions", "The chain of all blocks, each committing to the hash of its parent.", "a ledger whose pages are glued, so none can be swapped"),
    "syncing blockchain": ("PeersBlocksTransactions", "A new node downloads headers first, then the blocks, and checks them.", "reading the contents page before asking for chapters"),
    "UTXOs (unspent transaction outputs)": ("PeersBlocksTransactions", "The outputs not yet spent; a full node keeps this set to check payments.", "the coins in the drawer, not those already handed over"),
    "transactions": ("PeersBlocksTransactions", "Payments that peers announce, fetch and forward before a miner takes them.", "letters passed from hand to hand toward a postbox"),
    "unconfirmed transactions": ("PeersBlocksTransactions", "Valid transactions that no block contains yet.", "cheques handed in but not yet cleared"),
    "Mempools and Orphan Pools": ("PeersBlocksTransactions", "Each node keeps its own waiting areas for transactions.", "a shop with a waiting list and a shelf of incomplete orders"),
    "memory pool": ("PeersBlocksTransactions", "The valid, unconfirmed transactions that one node holds.", "each shop's own waiting list"),
    "orphan pools": ("PeersBlocksTransactions", "Transactions whose parent is unknown wait here until it arrives.", "a child's form that waits for the parent's signature"),
    "Compact Block Relay": ("PeersBlocksTransactions", "A block is sent as short ids of transactions the peer already has.", "telling a friend the page numbers of a book they own"),
    "low-bandwidth mode (compact block relay)": ("PeersBlocksTransactions", "The peer announces the block and sends the compact block on request.", "a waiter who asks before bringing the dish"),
    "high-bandwidth mode (compact block relay)": ("PeersBlocksTransactions", "The peer pushes the compact block at once, before full checks.", "a courier who runs over with the parcel unasked"),
    "block-finding races": ("PeersBlocksTransactions", "Two miners may find a block almost together; speed decides which stays.", "two runners finishing within a breath"),
    "Private Block Relay Networks": ("PeersBlocksTransactions", "Miners pass blocks to each other over fast private networks.", "an express lane beside the public road"),
    "private block relay": ("PeersBlocksTransactions", "Blocks pass over a dedicated, fast channel, not the open network.", "a private courier for urgent parcels"),
    "FEC (Forward Error Correction)": ("PeersBlocksTransactions", "Extra parity data lets a receiver rebuild lost packets without asking.", "a spare part packed in the box, so no repair call is needed"),
    "Bitcoin Relay Network": ("PeersBlocksTransactions", "Matt Corallo's relay network for miners, built to move blocks quickly.", "a ring road built only for lorries"),
    "FIBRE (Fast Internet Bitcoin Relay Engine)": ("PeersBlocksTransactions", "A relay network that sends blocks with FEC over UDP.", "a conveyor belt that adds a spare part to every box"),
    "BIP 152": ("PeersBlocksTransactions", "The proposal that defines compact blocks and the messages that carry them.", "the rule-book page for the page-number shortcut"),
    # ---- part C ----------------------------------------------------------------------------------------------------------------
    "Lightweight Clients": ("LightClientsPrivacyTransport", "Clients that keep only block headers and ask full nodes for the rest.", "a tourist with a map who asks the locals"),
    "SPV (simplified-payment-verification) clients": ("LightClientsPrivacyTransport", "Clients that check a payment with a Merkle path and the header chain.", "proving a name is in a phone book by the headings on its path"),
    "Bloom Filters": ("LightClientsPrivacyTransport", "A compact set that may say yes by mistake but never no by mistake.", "a guest list that admits a few strangers"),
    "How Bloom Filters Work": ("LightClientsPrivacyTransport", "Several hash functions set bits for each item; a test reads the same bits.", "stamping boxes on a card, then checking the same boxes"),
    "How Lightweight Clients Use Bloom Filters": ("LightClientsPrivacyTransport", "The client sends a filter of its addresses and gets matching transactions.", "describing roughly what to deliver to a courier"),
    "false positives": ("LightClientsPrivacyTransport", "Items reported as present although they were never added.", "a stranger waved in because he looked like a guest"),
    "BIP 37": ("LightClientsPrivacyTransport", "The 2012 proposal that added Bloom filters to the protocol.", "the 2012 rule-book page for guest lists"),
    "Compact Block Filters": ("LightClientsPrivacyTransport", "A small filter per block, built by the node, that clients download and test.", "a library that posts each day's index"),
    "Golomb-Rice Coded Sets (GCS)": ("LightClientsPrivacyTransport", "A compressed set made by sorting hashes and coding their differences.", "a staircase described by the height of each step"),
    "GCS (Golomb-Rice coded sets)": ("LightClientsPrivacyTransport", "The compression behind the filters of BIP 158.", "a long list squeezed by saying only how much each entry rises"),
    "What Data to Include in a Block Filter": ("LightClientsPrivacyTransport", "The basic filter holds output scripts and spent scripts, not OP_RETURN data.", "an index that lists the names and skips the fine print"),
    "Downloading Block Filters from Multiple Peers": ("LightClientsPrivacyTransport", "A client compares the filter headers of several peers before it trusts one.", "asking several witnesses and comparing their stories"),
    "downloading multiple block filters": ("LightClientsPrivacyTransport", "Filters are fetched in ranges, and filter headers chain them together.", "buying a whole shelf of index cards in one trip"),
    "Reducing Bandwidth with Lossy Encoding": ("LightClientsPrivacyTransport", "Accepting some false positives makes the filter smaller.", "a small blurry thumbnail instead of the full photo"),
    "lossless encoding": ("LightClientsPrivacyTransport", "Coding that restores the original exactly, as Golomb-Rice coding does.", "a zip file that unpacks to the identical document"),
    "lossy encoding": ("LightClientsPrivacyTransport", "Coding that drops detail for size; the original cannot be rebuilt.", "a thumbnail from which the photo cannot be restored"),
    "Using Compact Block Filters": ("LightClientsPrivacyTransport", "The client tests its scripts against each filter and fetches only matching blocks.", "checking the index, then borrowing only the books it names"),
    "Lightweight Clients and Privacy": ("LightClientsPrivacyTransport", "Asking a node about your addresses tells that node about you.", "asking a clerk for one book in front of the whole queue"),
    "privacy": ("LightClientsPrivacyTransport", "Who sends, who asks and who owns a coin should not be learnable by watchers.", "curtains on a window"),
    "BIP 157": ("LightClientsPrivacyTransport", "The proposal for client-side block filtering over the peer-to-peer network.", "the rule-book page for posting the daily index"),
    "BIP 158": ("LightClientsPrivacyTransport", "The proposal that fixes the filter format, its parameters and its test vectors.", "the rule-book page that fixes the size of the index card"),
    "Encrypted and Authenticated Connections": ("LightClientsPrivacyTransport", "Peers can hide their traffic; version 2 encrypts but does not authenticate.", "a sealed envelope that still carries no signature"),
    "encryption": ("LightClientsPrivacyTransport", "Scrambling the traffic so that only the two peers can read it.", "a sealed envelope instead of a postcard"),
    "Tor transport": ("LightClientsPrivacyTransport", "Reaching peers through Tor so that nobody learns the node's address.", "a note passed through several friends, none knowing both ends"),
}
