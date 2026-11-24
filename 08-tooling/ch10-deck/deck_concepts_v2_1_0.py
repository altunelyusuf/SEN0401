"""The key concepts of chapter 10 for the deck 2.4.0 (a redesign of deck_concepts_v2_0_0.py by the owner's ruling of 2026-11-24: no everyday analogy anywhere in the course materials): the 56 distinct primary-source
concepts of the chapter research (03-materials/ch10/rdodi/sen0401_ch10_research_v1_2_0.ttl, de-duplicated by normalised label as the deck standard check does), each with the part of the chapter it belongs to and a
one-sentence meaning; the literal one-line meaning of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept (its label exactly as the research names it) and its meaning;
there is no analogy line. NEW file; v2_0_0 stays as committed."""
__version__ = "2.1.0"

PARTS = ['WhoIsOnTheNetwork', 'PeersBlocksTransactions', 'LightClientsPrivacyTransport']
LABEL = {'LightClientsPrivacyTransport': 'Light clients, privacy and transport', 'PeersBlocksTransactions': 'Peers, blocks and transactions', 'WhoIsOnTheNetwork': 'Who is on the network'}
SHORT = {'LightClientsPrivacyTransport': 'Light and private', 'PeersBlocksTransactions': 'Peers and blocks', 'WhoIsOnTheNetwork': 'Who is on it'}

# level 1: divider subtitle (the literal meaning of the part)
L1 = {'LightClientsPrivacyTransport': 'A light client asks full nodes for proofs, so what it asks can reveal what it owns.',
 'PeersBlocksTransactions': 'Blocks and payments pass from peer to peer; no central server relays them.',
 'WhoIsOnTheNetwork': 'Every node follows the same rules and talks only to the nodes it is connected to.'}

# level 2: part -> list of (pill, meaning)   pill at most 4 words
L2 = {'LightClientsPrivacyTransport': [('Light clients', 'A Merkle path proves a payment to a client with only headers.'),
                                  ('Bloom filters', 'A compact filter that may say yes by mistake and leaks which addresses a wallet owns.'),
                                  ('Block filters', 'One small filter per block lets the client ask nothing at all.'),
                                  ('Transport', 'Version 2 encrypts peer traffic; Tor and I2P hide who is who.')],
 'PeersBlocksTransactions': [('Finding peers', 'DNS seeds and addr messages give a new node its first neighbours.'),
                             ('Connections', 'Eight full-relay and two block-relay-only links, at most 125 in all.'),
                             ('Blocks', 'Headers come first; compact blocks send only what is missing.'),
                             ('Transactions', "Payments wait in each node's own pool until a block takes them.")],
 'WhoIsOnTheNetwork': [('Nodes and roles', 'Full, archival, pruned and light nodes keep different data.'),
                       ('The handshake', 'Two nodes swap version and verack before anything else.'),
                       ('Services', 'A node announces what it offers in one bit field.')]}

# the key concepts: label (exactly as the research names it) -> (part, meaning)
K3 = {'BIP 152': ('PeersBlocksTransactions', 'The proposal that defines compact blocks and the messages that carry them.'),
 'BIP 157': ('LightClientsPrivacyTransport', 'The proposal for client-side block filtering over the peer-to-peer network.'),
 'BIP 158': ('LightClientsPrivacyTransport', 'The proposal that fixes the filter format, its parameters and its test vectors.'),
 'BIP 37': ('LightClientsPrivacyTransport', 'The 2012 proposal that added Bloom filters to the protocol.'),
 'Bitcoin': ('WhoIsOnTheNetwork', 'A money system and a network, run by software that anyone may run.'),
 'Bitcoin Core': ('WhoIsOnTheNetwork', 'The reference software, written by volunteers, that most nodes run.'),
 'Bitcoin Relay Network': ('PeersBlocksTransactions', "Matt Corallo's relay network for miners, built to move blocks quickly."),
 'Bitcoin network': ('WhoIsOnTheNetwork', 'The nodes that speak the Bitcoin protocol to each other over TCP.'),
 'Bloom Filters': ('LightClientsPrivacyTransport', 'A compact set that may say yes by mistake but never no by mistake.'),
 'Compact Block Filters': ('LightClientsPrivacyTransport', 'A small filter per block, built by the node, that clients download and test.'),
 'Compact Block Relay': ('PeersBlocksTransactions', 'A block is sent as short ids of transactions the peer already has.'),
 'DNS seeds': ('PeersBlocksTransactions', 'Servers that answer a DNS query with addresses of reachable nodes.'),
 'Downloading Block Filters from Multiple Peers': ('LightClientsPrivacyTransport', 'A client compares the filter headers of several peers before it trusts one.'),
 'Encrypted and Authenticated Connections': ('LightClientsPrivacyTransport', 'Peers can hide their traffic; version 2 encrypts but does not authenticate.'),
 'FEC (Forward Error Correction)': ('PeersBlocksTransactions', 'Extra parity data lets a receiver rebuild lost packets without asking.'),
 'FIBRE (Fast Internet Bitcoin Relay Engine)': ('PeersBlocksTransactions', 'A relay network that sends blocks with FEC over UDP.'),
 'Full Nodes': ('WhoIsOnTheNetwork', 'A full node checks every block and transaction itself and trusts no one.'),
 'GCS (Golomb-Rice coded sets)': ('LightClientsPrivacyTransport', 'The compression behind the filters of BIP 158.'),
 'Golomb-Rice Coded Sets (GCS)': ('LightClientsPrivacyTransport', 'A compressed set made by sorting hashes and coding their differences.'),
 'How Bloom Filters Work': ('LightClientsPrivacyTransport', 'Several hash functions set bits for each item; a test reads the same bits.'),
 'How Lightweight Clients Use Bloom Filters': ('LightClientsPrivacyTransport', 'The client sends a filter of its addresses and gets matching transactions.'),
 'Lightweight Clients': ('LightClientsPrivacyTransport', 'Clients that keep only block headers and ask full nodes for the rest.'),
 'Lightweight Clients and Privacy': ('LightClientsPrivacyTransport', 'Asking a node about your addresses tells that node about you.'),
 'Mempools and Orphan Pools': ('PeersBlocksTransactions', 'Each node keeps its own waiting areas for transactions.'),
 'Network Discovery': ('PeersBlocksTransactions', 'A new node finds its first peers, then learns about many more.'),
 'Node Types and Roles': ('WhoIsOnTheNetwork', 'Nodes differ in what they store and what they do for others.'),
 'Private Block Relay Networks': ('PeersBlocksTransactions', 'Miners pass blocks to each other over fast private networks.'),
 'Reducing Bandwidth with Lossy Encoding': ('LightClientsPrivacyTransport', 'Accepting some false positives makes the filter smaller.'),
 'SPV (simplified-payment-verification) clients': ('LightClientsPrivacyTransport', 'Clients that check a payment with a Merkle path and the header chain.'),
 'The Network': ('WhoIsOnTheNetwork', 'The computers that follow the same rules and pass the same messages.'),
 'Tor transport': ('LightClientsPrivacyTransport', "Reaching peers through Tor so that nobody learns the node's address."),
 'UTXOs (unspent transaction outputs)': ('PeersBlocksTransactions', 'The outputs not yet spent; a full node keeps this set to check payments.'),
 'Using Compact Block Filters': ('LightClientsPrivacyTransport', 'The client tests its scripts against each filter and fetches only matching blocks.'),
 'What Data to Include in a Block Filter': ('LightClientsPrivacyTransport', 'The basic filter holds output scripts and spent scripts, not OP_RETURN data.'),
 'archival full nodes': ('WhoIsOnTheNetwork', 'A full node that keeps every block since the first.'),
 'block-finding races': ('PeersBlocksTransactions', 'Two miners may find a block almost together; speed decides which stays.'),
 'blockchain': ('PeersBlocksTransactions', 'The chain of all blocks, each committing to the hash of its parent.'),
 'blocks': ('PeersBlocksTransactions', 'A block bundles transactions and names the block before it.'),
 'downloading multiple block filters': ('LightClientsPrivacyTransport', 'Filters are fetched in ranges, and filter headers chain them together.'),
 'encryption': ('LightClientsPrivacyTransport', 'Scrambling the traffic so that only the two peers can read it.'),
 'false positives': ('LightClientsPrivacyTransport', 'Items reported as present although they were never added.'),
 'high-bandwidth mode (compact block relay)': ('PeersBlocksTransactions', 'The peer pushes the compact block at once, before full checks.'),
 'lossless encoding': ('LightClientsPrivacyTransport', 'Coding that restores the original exactly, as Golomb-Rice coding does.'),
 'lossy encoding': ('LightClientsPrivacyTransport', 'Coding that drops detail for size; the original cannot be rebuilt.'),
 'low-bandwidth mode (compact block relay)': ('PeersBlocksTransactions', 'The peer announces the block and sends the compact block on request.'),
 'memory pool': ('PeersBlocksTransactions', 'The valid, unconfirmed transactions that one node holds.'),
 'mining': ('WhoIsOnTheNetwork', 'The work of finding new blocks; miners also run nodes.'),
 'nodes': ('WhoIsOnTheNetwork', 'A node is a computer that runs Bitcoin software and joins the network.'),
 'orphan pools': ('PeersBlocksTransactions', 'Transactions whose parent is unknown wait here until it arrives.'),
 'peer-to-peer networks, Bitcoin as': ('WhoIsOnTheNetwork', 'Every participant is both client and server, and nobody is in charge.'),
 'peers': ('WhoIsOnTheNetwork', 'The other nodes that one node is directly connected to.'),
 'privacy': ('LightClientsPrivacyTransport', 'Who sends, who asks and who owns a coin should not be learnable by watchers.'),
 'private block relay': ('PeersBlocksTransactions', 'Blocks pass over a dedicated, fast channel, not the open network.'),
 'syncing blockchain': ('PeersBlocksTransactions', 'A new node downloads headers first, then the blocks, and checks them.'),
 'transactions': ('PeersBlocksTransactions', 'Payments that peers announce, fetch and forward before a miner takes them.'),
 'unconfirmed transactions': ('PeersBlocksTransactions', 'Valid transactions that no block contains yet.')}
