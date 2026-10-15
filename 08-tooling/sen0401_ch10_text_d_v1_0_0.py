"""SEN0401 chapter 10: the teaching paragraphs of the leaves of subjects 6 (privacy and transport) and 7 (mempool and orphans), and the introductions of the 17 mid-level and 7 top-level subjects
(the data module adds to each introduction a sentence that lists its members). Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
D = {}

D["PlaintextV1"] = (
 "The original transport of the Bitcoin peer-to-peer protocol, now called v1, sends every message as plain bytes: anybody on the path, a router, a provider or a coffee shop's Wi-Fi, can read which transactions and blocks a node sends and can tell from the first bytes that the connection is Bitcoin (Bitcoin Wiki, 2026). "
 "The book states that the Bitcoin network communicates entirely in the clear, even in the modern Bitcoin Core at the time of writing (Antonopoulos and Harding, 2023). In the run the first bytes that the script sent over a v1 connection were fabfb5da, the magic of the test chain, the word version could be read in the stream, and the session identifier that getpeerinfo reports for the connection was empty. "
 "It is like a postcard: the postman, the neighbours and the people who sort the mail can read it, and the sender cannot stop them.")

D["EncryptedV2"] = (
 "BIP 324 defines the v2 transport, in which the two sides first make a shared secret with a key exchange whose public keys are encoded with ElligatorSwift so that they look like random bytes, and then send every message encrypted and authenticated with the ChaCha20-Poly1305 construction, in packets of which even the length is hidden (Mehta et al., 2019). "
 "In the run a connection between two nodes used the v2 transport: the stream held neither the magic bytes nor the word version, the first 4,096 bytes had an entropy of 7.953 bits per byte (8 would be perfect noise), and both sides reported the same session identifier of 64 hexadecimal characters, which two people can compare out of band to detect an attack (Bitcoin Core, 2026). "
 "The Bitcoin Optech topic page describes the aim, to make the traffic harder to recognize and to read (Bitcoin Optech, 2026). The change is from the postcard to a sealed envelope that is also not marked as a Bitcoin letter.")

D["V2DefaultHistory"] = (
 "The v2 transport came in two steps. Bitcoin Core 26.0 added it as an option, which the release notes call off by default, and 27.0 turned it on, with the words that BIP324 v2 transport is now enabled by default (Bitcoin Core developers, 2023); (Bitcoin Core developers, 2024). "
 "In the source the constant DEFAULT_V2_TRANSPORT is true, and in the census of 2026-10-15 21,768 of 25,361 nodes, 85.8 percent, advertise the service bit P2P_V2, so most of the network already speaks it (Bitcoin Core, 2026); (Bitnodes, 2026). "
 "The book is therefore out of date on this point, because it says that Bitcoin Core communicates entirely in the clear and suggests Tor as the solution (Antonopoulos and Harding, 2023). "
 "A default matters because few people change settings: the postcard became a sealed letter for everybody when the post office changed its form, and not when each customer asked for an envelope.")

D["UnauthenticatedTransport"] = (
 "Encryption keeps out the eavesdropper but does not say who is on the other end: BIP 324 encrypts the connection but does not authenticate the peers, so an attacker who sits on the path can still pose as the peer to both sides, a man-in-the-middle attack, or can downgrade the connection to v1, and the BIP says that it protects against passive observers only; the session identifier lets users compare and notice (Mehta et al., 2019). "
 "The earlier proposal BIP 151 also sought encryption, with an authentication option, and its status is Closed (Schnelli, 2016). "
 "The book's section on encrypted and authenticated connections presents Tor as the solution for both (Antonopoulos and Harding, 2023). A friend who whispers to you in a crowd keeps the others from hearing, but you still have to know it is your friend.")

D["FiveNetworks"] = (
 "A Bitcoin Core node can speak on five networks: IPv4 and IPv6, which is the plain internet, and onion (Tor), i2p and cjdns, three overlay networks that hide the address of a node; each has its own address format, which is why addrv2 was invented (Van der Laan, 2019). "
 "The RPC getnetworkinfo lists them with a flag reachable. In the run a normal node showed ipv4 and ipv6 as reachable and onion, i2p and cjdns as not, because they need a proxy or a local router, and a second node started with a Tor proxy at 127.0.0.1:9 showed onion as reachable (Bitcoin Core, 2026). "
 "Tor was the only overlay network in the book, which speaks of transport over Tor (Antonopoulos and Harding, 2023). Think of five postal systems with different address forms, where a letter can only cross to another system through a gateway that the node must be told about.")

D["TorHiddenService"] = (
 "Tor is an overlay network that sends traffic through three relays, each of which knows only its neighbours, and that lets a server hide itself behind an onion address that ends in .onion, so that neither side learns the other's internet address (Wikipedia contributors, 2026). "
 "A Bitcoin Core node makes an onion service by itself if a local Tor is running and the control cookie is readable: the option -listenonion defaults to 1, and doc/tor.md says how to switch it off with -listenonion=0 (Bitcoin Core, 2026). "
 "The book describes the same behaviour from version 0.12 on and prints the log line tor: ADD_ONION successful (Antonopoulos and Harding, 2023). Tor version 3 is the only form since release 22.0, and release 28.0 changed the local port for the incoming onion connections to 127.0.0.1:8334. "
 "The census of 2026-10-15 lists 12,488 onion nodes, half of all reachable nodes. It was not possible to start Tor in the sandbox, so no onion service was created: the claim is that of the sources and the census. Biryukov and colleagues showed in 2014 that a client's identity could be linked to its address when it was not protected this way (Biryukov et al., 2014).")

D["I2pAndCjdns"] = (
 "I2P, the Invisible Internet Project, and CJDNS are two more overlay networks, I2P a layer of tunnels in which each application has its own destination, CJDNS an encrypted IPv6 network that routes by public keys; Bitcoin Core added I2P in release 22.0 and CJDNS in release 23.0 (Bitcoin Core developers, 2021); (Bitcoin Core developers, 2022). "
 "Each has its document in the source tree that tells how to run a node over it (Bitcoin Core, 2026). The census of 2026-10-15 holds 4,208 I2P nodes, one in six of all, and one CJDNS node. "
 "The book knows only Tor, so the choice of networks in the book is shorter than in the code (Antonopoulos and Harding, 2023). An I2P node cannot be reached from the plain internet, like a house that is only on a private road: this tutorial's sandbox had neither network, so no connection was tried.")

D["EclipseAttack"] = (
 "An eclipse attack surrounds a victim node with the attacker's peers, so that the victim sees only what the attacker shows; it may then be fed a false chain, be kept away from the real one, or be used as a tool against others, such as in a double-spend (Heilman et al., 2015). "
 "Heilman, Kendler, Zohar and Goldberg showed at USENIX Security 2015 that an attacker with enough IP addresses could fill the address tables of a node, and the Bitcoin Core defences that followed include anchor connections, which a node remembers and reconnects to after a restart, and a choice of peers from different autonomous systems (Bitcoin Optech, 2026). "
 "The two block-relay-only connections of Bitcoin Core are part of the answer, since they are not seen by transaction gossip. It could not be tried in the sandbox, as it needs many real addresses, so the leaf records that the paper and the defences exist in the saved copies. "
 "It is like a traveller whose phone calls are all answered by the same impostor: only a call to a number not chosen by the impostor breaks the spell.")

D["RoutingAttack"] = (
 "A routing attack does not need any node: an attacker who controls part of the internet's routes, such as an internet provider or an autonomous system that announces false routes with BGP, can cut the network in two or delay blocks to some nodes (Apostolaki et al., 2017). "
 "Apostolaki, Zohar and Vanbever found that a few autonomous systems carry most of the traffic of the network and that a hijack of fewer than 100 prefixes can isolate about 50 percent of the mining power. "
 "The remedy is wider: encryption does not help against a route that is simply dropped, whereas peers from different networks, such as Tor, do. The attack was not run in the sandbox, as it needs the real internet. "
 "It is like a landslide that blocks a mountain road: no traveller is attacked, but if there is only one road, nobody gets through.")

D["TxAnnouncementByWtxid"] = (
 "A node does not send a whole transaction to every peer: it announces it with an inv message that holds only the identifier, and the peer asks with getdata if it does not have it already; since BIP 339 the identifier is the wtxid, the hash that also covers the witness, announced with the type MSG_WTX (0x00000005) after both sides sent wtxidrelay (Daftuar, 2020). "
 "In the run the node announced both transactions to the normal peer with entries of type 5, the peer with the feefilter was announced one, and the transaction the script then fetched had the id of the one with the higher fee rate (Bitcoin Core, 2026). "
 "The book's description of the inventory exchange is in terms of the txid and the MSG_TX type (Antonopoulos and Harding, 2023). The wtxid closes a weakness: two transactions with the same txid but different witnesses could stop each other. How a transaction spreads also decides how well its origin is hidden, which Fanti and Viswanath studied for the trickle and diffusion spreading rules (Fanti and Viswanath, 2017). It is like a parcel label that includes the contents' checksum and not only the sender's name.")

D["FeefilterHonoured"] = (
 "BIP 133 gave every node a way to say what the lowest fee rate is that it wants to hear about: the message feefilter carries a number in satoshis per kilobyte, and the sender holds back every transaction below it, which saves bandwidth for the nodes with a small mempool (Morcos, 2016). "
 "In the run a peer sent feefilter for 5,000 satoshis per kilovirtual byte, that is 5 per virtual byte; of the two transactions with 2.0 and 20.0 satoshis per virtual byte the node announced only the one with 20.0, and the node's own feefilter to the script was 100, 0.1 satoshi per virtual byte, the new default minimum of release 30.0 (Bitcoin Core, 2026). "
 "The handshake order of the run shows that the feefilter message follows verack. It is like a notice on the door of a shop: no deliveries under a certain size, and the courier who respects it does not bring the smaller parcels.")

D["MempoolIsLocalUtxoIsShared"] = (
 "The book says that the mempool and the orphan pool are a node's local view and may differ from node to node, whereas the UTXO set is the shared outcome of consensus (Antonopoulos and Harding, 2023). "
 "In the run two connected nodes were set up so that the second asked not to be sent transactions; after the first had accepted 6 transactions, the second had 0 in its mempool, and after the next block both held the same UTXO set of 107 outputs with the same hash. "
 "The first node saw the second's relay flag as false, which is what the relay field of the version message says (Bitcoin Core, 2026). The mempool is therefore like a waiting room that is different in every building, while the UTXO set is like the land register, which must be the same in every office.")

D["MempoolDefaults"] = (
 "The mempool has limits that are options of the node: Bitcoin Core 31.1 holds at most 300 MB in memory (-maxmempool), drops a transaction after 336 hours or 14 days (-mempoolexpiry), and, with the cluster mempool of release 31.0, allows 64 transactions in a cluster (Bitcoin Core developers, 2026). "
 "In the run getmempoolinfo showed maxmempool 300,000,000 bytes, fullrbf true, limitclustercount 64 and loaded true, and the help text of the command line gives 336 as the default expiry (Bitcoin Core, 2026). "
 "The book describes the mempool as a list of unconfirmed transactions without giving a number (Antonopoulos and Harding, 2023). The memory is a fixed table at a market stall: when the table is full, the cheapest goods are taken off first, and what has lain too long is thrown out.")

D["OrphanWaitsForParent"] = (
 "An orphan is a transaction whose input refers to a parent that the node does not know yet, which happens because transactions travel by different routes and a child can arrive before its parent; the node cannot check it, so it keeps it in a small separate pool, the orphanage, and does not relay it (Antonopoulos and Harding, 2023). "
 "In the run the script announced a child before its parent; the node asked for the child by its wtxid (an inv entry of type 5), the child did not enter the mempool (size 0), and getorphantxs listed one entry of 191 bytes, 110 virtual bytes, which came from one peer (Bitcoin Core, 2026). "
 "The data structure is in txorphanage.h and the download logic in txdownloadman.h (Bitcoin Core, 2026). An orphan is like a guest who turns up at a party before the friend who invited him: he waits in the hall until the friend arrives.")

D["NodeRequestsMissingParent"] = (
 "When the node meets an orphan it does not wait for luck: it asks the peer that sent the child for the parent, with getdata for the transaction by its parent's identifier; the type 0x40000001 is MSG_WITNESS_TX, a transaction with its witness data, which BIP 144 defined (Lombrozo and Wuille, 2016). "
 "In the run the node answered the orphan with getdata of type 0x40000001 for the parent's txid, which the script then sent. "
 "Release 29.0 improved this: the node now downloads missing parents from all peers who announced the orphan, so that a peer that holds the parent back cannot block it (Bitcoin Core developers, 2025). "
 "This is the old trick of asking a guest at the party where his friend is; since 29.0 the host asks everybody who knows the guest.")

D["ParentReleasesOrphan"] = (
 "When the parent arrives and is accepted into the mempool, the node looks in the orphanage for transactions that spend its outputs and tries them again; each child that is now valid joins the mempool and the search repeats for the children's children until no more are found, the cascade that the book describes (Antonopoulos and Harding, 2023). "
 "In the run the parent was accepted, the child followed at once, both were in the mempool and the orphanage was empty again (Bitcoin Core, 2026). "
 "The cascade is the reason a chain of dependent transactions can arrive in any order and still be rebuilt. It is like the pages of a letter that arrive by different mail: the letter can be read when the first page turns up, and the later pages fall into place one after another.")

D["OrphanageLimits"] = (
 "The orphanage is a place where an attacker could try to fill the memory with transactions that never become valid, and so it has limits. Until release 29 the limit was the number of orphans, 100 by default with -maxorphantx; release 30.0 replaced it with two limits, the number of entries plus a tenth of their inputs at most 3,000, and the total weight 404,000 weight units for each peer, and release 31.0 removed the option (Bitcoin Core developers, 2025); (Bitcoin Core developers, 2026). "
 "The per-peer reserve is the constant DEFAULT_RESERVED_ORPHAN_WEIGHT_PER_PEER{404'000} in txorphanage.h, which means that one peer cannot evict the orphans of the others (Bitcoin Core, 2026). "
 "The book has no limit to quote, only the statement that some implementations keep an orphan pool (Antonopoulos and Harding, 2023). It is like a cloakroom that gives each guest the same number of hooks, so one guest cannot hang up the coats of the whole street.")

MID = {}
MID["FlatNetwork"] = ("The first subject asks what kind of network Bitcoin is: a flat peer-to-peer network without a centre, how many nodes there are today, which program they run and which services they say they offer (Antonopoulos and Harding, 2023). "
 "The numbers come from the Bitnodes snapshot of 2026-10-15 and the answers of a test node (Bitnodes, 2026).")
MID["NodeKinds"] = ("This subject asks how nodes differ in what they keep: the archival node that has all of the history and the pruned node that has only the latest, and how they say it with service bits (Schnelli, 2017). "
 "It matters because new nodes can only download the past from the first kind.")
MID["Handshake"] = ("This subject asks how two peers who have never met start to talk: the frame of every message, the version message, the protocol number, the order of the first messages and the flag that asks for silence about transactions (Bitcoin Wiki, 2026).")
MID["Discovery"] = ("This subject asks how a new node finds its first peers and how it learns more: DNS seeds, the exchange of addresses with getaddr and the addrv2 format that holds the long addresses of Tor, I2P and CJDNS (Van der Laan, 2019).")
MID["Connections"] = ("This subject asks which kinds of connection a node keeps and why they differ: full relay, block-relay-only, addr-fetch and the others, with the limits that Bitcoin Core sets (Bitcoin Core, 2026).")
MID["RaceAndAnnouncement"] = ("This subject asks why the speed of block announcement matters, because a slow announcement lets a rival block be found, and how the sendheaders message saves one round trip (Daftuar, 2015).")
MID["CompactBlocks"] = ("This subject asks how a block can be sent without repeating what the receiver has already: short ids of 6 bytes, a prefilled coinbase, a request for what is missing, two modes of sending and the depth limit, and it corrects the year of the book (Corallo, 2016).")
MID["PrivateRelay"] = ("This subject asks how miners got blocks around faster before and beside compact blocks: private relay networks and the forward error correction of FIBRE (Corallo, 2016).")
MID["HeadersFirst"] = ("This subject asks how a new node catches up with the chain: headers first, in batches of 2,000, then the blocks inside a window, with a protection against floods of headers (Bitcoin Core, 2026).")
MID["Spv"] = ("This subject asks how a client with only the headers can be sure of a payment: the small size of the headers, the Merkle path and the odds of an attacker catching up as Nakamoto calculated them (Nakamoto, 2008).")
MID["BloomFilters"] = ("This subject asks how a light client asked a full node for its transactions with a Bloom filter, how the filter works, what the messages look like and why the service was switched off by default (Hearn and Corallo, 2012).")
MID["BlockFilters"] = ("This subject asks how block filters turned the question around: the node gives a compact filter of each block and the client decides what to download, with the Golomb-coded set, the parameters of BIP 158, the size of the filters and the history of the idea (Osuntokun and Akselrod, 2017).")
MID["EncryptedTransport"] = ("This subject asks what an observer can see of a connection: everything on the old transport, almost nothing on the v2 transport of BIP 324, which is on by default since release 27.0 and which still does not say who the peer is (Mehta et al., 2019).")
MID["AnonymityNetworks"] = ("This subject asks how a node can hide where it is: the five networks, Tor with its automatic onion service, and the later I2P and CJDNS (Bitcoin Core, 2026).")
MID["NetworkAttacks"] = ("This subject asks how the network itself can be attacked: the eclipse attack on the choice of peers and the routing attack on the internet below the network (Heilman et al., 2015).")
MID["MempoolRelay"] = ("This subject asks how unconfirmed transactions travel: the announcement by wtxid, the minimum fee rate a peer asks for, the difference between a local mempool and the shared UTXO set and the defaults of the mempool (Antonopoulos and Harding, 2023).")
MID["OrphanPool"] = ("This subject asks what a node does with a transaction whose parent it does not know: it keeps it, asks for the parent, releases it when the parent comes and limits the memory it may use, with limits that changed in releases 29, 30 and 31 (Bitcoin Core developers, 2025).")

TOP = {}
TOP["NetworkAndNodes"] = ("The first section of the chapter explains that Bitcoin runs on a peer-to-peer network of nodes that are equal, and that nodes differ in the services they offer, such as keeping the whole chain or only the latest part (Antonopoulos and Harding, 2023). "
 "In 2026 the network has about 25,000 reachable nodes, nearly all of them running Bitcoin Core or a fork (Bitnodes, 2026).")
TOP["PeersAndDiscovery"] = ("The second section teaches how a node joins: it finds first peers by DNS seeds, speaks a framed message protocol that begins with a version handshake, learns more addresses from its peers and keeps different kinds of connection (Antonopoulos and Harding, 2023). "
 "Everything here was run against a Bitcoin Core 31.1 node on a private test chain (Bitcoin Core, 2026).")
TOP["BlockRelay"] = ("The third section is about how a new block gets through the network quickly, because the network must carry a block within seconds if rival blocks are to remain rare: announcement with headers, compact blocks and the private networks of the miners (Corallo, 2016). "
 "It is the part of the chapter where the book is wrong about a date and where its picture is simplest.")
TOP["Syncing"] = ("The fourth section shows how a node that was offline, or never online, gets the chain: headers first, then blocks inside a download window, with the checks that stop a peer from filling the node's memory (Antonopoulos and Harding, 2023).")
TOP["LightClients"] = ("The fifth section is about nodes that do not keep the chain: simplified payment verification with headers and Merkle paths, the Bloom filters of BIP 37 that have been switched off, and the compact block filters of BIP 157 and 158 that replaced them (Antonopoulos and Harding, 2023). "
 "It is the section with the most numbers that can be recomputed.")
TOP["PrivacyAndTransport"] = ("The sixth section is about who can see a node's traffic and where it is: the encrypted v2 transport, which is the largest change since the book, the Tor, I2P and CJDNS networks and the attacks on the network (Mehta et al., 2019). "
 "The book says the traffic is in the clear, and that is no longer true of the default.")
TOP["MempoolAndOrphans"] = ("The seventh section is about the unconfirmed transactions of a node: how they are announced, how a peer filters them, why every mempool is local, and what happens to a child that arrives before its parent, which changed with the orphan handling of releases 29 to 31 (Antonopoulos and Harding, 2023).")
