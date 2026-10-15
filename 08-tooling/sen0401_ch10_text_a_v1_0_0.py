"""SEN0401 chapter 10: the teaching paragraphs of the leaves of subjects 1 (network and nodes) and 2 (peers and discovery). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
A = {}

A["PeersAreEqual"] = (
 "The Bitcoin network is a peer-to-peer network: every node is a peer, there is no central server, no privileged coordinator, and a node that wants to join needs only the address of one other node (Antonopoulos and Harding, 2023). "
 "This matters because there is nothing to switch off: file sharing systems such as Napster, which kept a central index, could be shut down by closing that index, whereas a network of equals goes on as long as two peers talk (Wikipedia contributors, 2026). "
 "Think of a village well where everybody carries water for everybody, against a single water tower that one person can lock. To test the claim on a machine, a small script written for this chapter, which knows nothing of Bitcoin Core except the message format, opened a connection to a Bitcoin Core 31.1 node on a private test chain and introduced itself like any other peer. "
 "The node answered with its version message (user agent /Satoshi:31.1.0/), then wtxidrelay, sendaddrv2 and verack, all framed with the magic bytes fabfb5da of that private chain; it did not ask who the script was, because the protocol has no accounts (Bitcoin Core, 2026).")

A["ReachableNodesToday"] = (
 "A reachable node is one that accepts incoming connections, and the crawler Bitnodes counts them by trying to connect to every address it learns about, so its number is a lower bound of the nodes that exist, since a node behind a home router that does not listen is invisible to it (Bitnodes, 2026). "
 "The book of 2023 says that the network has about 10,000 listening nodes (Antonopoulos and Harding, 2023). The snapshot fetched on 2026-10-15 lists 25,361: 12,488 onion services, 7,473 on IPv4, 4,208 on I2P, 1,191 on IPv6 and one on CJDNS, so only 8,664 can be reached on the plain internet. "
 "The number has therefore more than doubled, but almost all of the growth is on the hidden networks, which is itself a result: more people want to run a node without their address being known. "
 "It is like counting the shops in a town by walking along the streets: the shops with a door on the street are counted, those that deliver only to the back door are not, and a new kind of door (the onion address) has been opened since the book was written.")

A["SoftwareShare"] = (
 "A node is defined by the rules it follows, not by the program that follows them, and in practice the great majority of nodes run the reference implementation Bitcoin Core or a fork of it, which the book states as more than 95 percent of full nodes (Antonopoulos and Harding, 2023). "
 "In the snapshot of 2026-10-15 of the 25,361 reachable nodes 25,278 (99.67 percent) report a user agent beginning /Satoshi:, of which 4,083 are Bitcoin Knots, a fork that changes policy, and 21,195 (83.57 percent of all) plain Bitcoin Core; the most common single agent is /Satoshi:31.1.0/ with 7,442 nodes (Bitnodes, 2026). "
 "The agent is only a text the node chooses for itself, as BIP 14 says, so the census shows what nodes claim, not what they run (Taaki and Strateman, 2011). The picture is a shop street in which almost every shop is a branch of one chain, with a fifth of them repainted in the colours of a relative. "
 "The consequence for safety is double: one program gives the network a common behaviour, and one program means that a single bug could reach nearly every node, and that is the argument for a diversity of implementations.")

A["ServiceBitsOfNetwork"] = (
 "Every node tells its peers in the version message which services it offers, as a set of bits: NETWORK (the full block history), WITNESS (segregated witness data), BLOOM (the old filtering of BIP 37), COMPACT_FILTERS (the block filters of BIP 157), NETWORK_LIMITED (only the last 288 blocks) and P2P_V2 (the encrypted transport) (Bitcoin Core, 2026). "
 "The census of 2026-10-15 counts 22,402 nodes with NETWORK, 24,582 with WITNESS, 25,322 with NETWORK_LIMITED, 7,905 with COMPACT_FILTERS, 4,308 with BLOOM and 21,768 with P2P_V2, which is 85.8 percent of all (Bitnodes, 2026). "
 "The bits matter because a new node chooses its peers by them: a light wallet looks for nodes with COMPACT_FILTERS, a node that must download the whole history looks for NETWORK. It is like the pictograms on a motorway service station sign, petrol, food, toilets: the driver reads the sign and does not go in to ask. "
 "The book's listing of getpeerinfo shows the services value 0000000000000409 with its names (Antonopoulos and Harding, 2023); the table of the census is a list of what the nodes of today offer in addition.")

A["ArchivalNodeServices"] = (
 "An archival full node keeps and serves every block since the genesis block, and it says so with the service bit NETWORK, which in the book is the description of a full node that keeps a complete copy of the blockchain (Antonopoulos and Harding, 2023). "
 "In the run a Bitcoin Core 31.1 node that was not pruned advertised the services value 3081, which is hexadecimal c09 and decodes to NETWORK, WITNESS, NETWORK_LIMITED and P2P_V2; the node's own getnetworkinfo says so in the field localservicesnames (Bitcoin Core, 2026). "
 "The 3081 is the sum of four bits (1 + 8 + 1024 + 2048), like a menu card on which every dish has a number and the order is the sum of the numbers. "
 "The importance is practical: a new node that needs the whole history can only get it from a peer that has the NETWORK bit, and the census counts 22,402 such nodes out of 25,361, so a few thousand nodes serve the whole past for everybody else.")

A["PrunedNodeServices"] = (
 "A pruned node deletes old block files after validating them and keeps the chain state and the most recent blocks, which saves disk space but means it can no longer serve the old history; because of this it must not set the NETWORK bit and uses NETWORK_LIMITED instead, which promises at least the last 288 blocks, about two days (Schnelli, 2017). "
 "In the run a node started with the smallest possible pruning target (getblockchaininfo reports pruned true) advertised exactly WITNESS, NETWORK_LIMITED and P2P_V2, both in its network information and in the version message it sent to a peer, whereas the archival node of the same run also had NETWORK (Bitcoin Core, 2026). "
 "It is like a librarian who has thrown out the old newspapers but keeps the last two days on the desk: the librarian can tell today's news and cannot find last year's. "
 "The book's peer listing shows the name NETWORK_LIMITED without explaining it, so BIP 159 is the place to read what it promises (Antonopoulos and Harding, 2023).")

A["MessageFraming"] = (
 "Every message of the Bitcoin peer-to-peer protocol on the old transport is a block of bytes with a header of 24 bytes: 4 bytes of magic that name the network, 12 bytes with the command padded with zeros, 4 bytes with the length of the payload and 4 bytes with the first four bytes of the double SHA-256 of the payload as a checksum (Bitcoin Wiki, 2026). "
 "The magic of the main chain is f9beb4d9, which chainparams.cpp writes as the four values 0xf9, 0xbe, 0xb4 and 0xd9, and the private test chain of the run uses fabfb5da (Bitcoin Core, 2026). "
 "The smallest message is verack, which has no payload at all: 24 bytes, fabfb5da, the word verack and zeros, the length 0 and the checksum 5df6e0e2 of the empty input, reproduced here by the independent code of this chapter. "
 "The frame is like the envelope of a letter: the stamp (the magic) says which postal system the letter belongs to, the label says what kind of letter it is, and the weight is written on the outside so that the receiver knows how much to read.")

A["VersionMessageFields"] = (
 "The first message that two peers exchange is version, in which each side states its protocol version, its services, the time, the addresses it sees, a random nonce to detect a connection to itself, its user agent, the height of its chain and whether it wants transactions to be relayed to it (Bitcoin Wiki, 2026). "
 "The book explains the fields of the message (nLocalServices and the others) and then prints the peer listing of getpeerinfo, in which the same facts return as services, version and subver (Antonopoulos and Harding, 2023). The version message of the Bitcoin Core 31.1 test node in the run was 102 bytes with the version 70016, the services 3081, the user agent /Satoshi:31.1.0/, the height 2099 of its chain and the relay flag true, in eleven fields that the independent parser of this chapter read. "
 "The user agent is a free text that clients set for themselves, defined in BIP 14 (Taaki and Strateman, 2011). The message is the exchange of cards at the start of a business meeting: name, position, and what each side can do for the other.")

A["ProtocolVersionNumber"] = (
 "The protocol version is a single number that says which messages a peer understands, and a node sends it in the version message; a feature that needs new messages is tied to a number, so that an old peer never receives a message it cannot read (Bitcoin Wiki, 2026). "
 "The book shows the example 70002 in its description of the handshake and in its listing, a number of 2013 (Antonopoulos and Harding, 2023). Bitcoin Core 31.1 defines PROTOCOL_VERSION as 70016 in protocol_version.h, the node sent 70016 in the run, and the same number is the least version for wtxid relay, WTXID_RELAY_VERSION (Bitcoin Core, 2026). "
 "The number 70016 is also the one that BIP 339 and BIP 155 build on (Daftuar, 2020). A version number is like the edition number of a manual: two people who hold different editions can still work together if both can see which pages are new.")

A["HandshakeMessageOrder"] = (
 "A connection begins with a fixed order of messages: the initiating side sends version, the other side answers with its own version and then with the feature messages that must come before verack, wtxidrelay (BIP 339) and sendaddrv2 (BIP 155), and finally verack, the acknowledgement that the version has been accepted (Daftuar, 2020). "
 "After verack both sides may send ordinary messages: in the run the node followed verack with sendcmpct (compact blocks), ping, getheaders (what chain does the peer have), inv (what it announces) and feefilter (the minimum fee it wants), in exactly this order (Bitcoin Core, 2026). "
 "The rule that a feature message must come before verack is the reason that BIP 155 says an old peer will simply ignore it (Van der Laan, 2019). The handshake is like the greeting at a meeting of two people who do not know each other: names, then what each can do, then the nod that says we may begin.")

A["RelayFlagSilencesTransactions"] = (
 "The version message has a last field, relay, which says whether the peer wants to be told about loose transactions; a node that sets it to false asks to receive blocks only, which saves bandwidth and is the base of the block-relay-only connections of Bitcoin Core (Bitcoin Core, 2026). "
 "The book mentions the flag in the description of the version message (Antonopoulos and Harding, 2023). In the run three peers were connected to the same node: one normal peer, one with relay false and one that had set a minimum fee with feefilter. "
 "Two transactions were created; the node announced both to the normal peer, none to the peer with relay false and only the one with the higher fee rate to the peer with the feefilter of 5 satoshis per virtual byte (Morcos, 2016). "
 "It is like a newspaper subscription with three plans: everything, only the headlines of big events, or nothing but the weekly summary, and the sender respects the plan without being asked twice.")

A["DnsSeedList"] = (
 "A node that has just been installed knows no peers, and it solves the problem with DNS seeds: names that a few trusted volunteers keep pointing at the addresses of currently reachable nodes, which the node looks up once, so that it learns some addresses without any central list of nodes (Bitcoin Wiki, 2026). "
 "Bitcoin Core 31.1 lists eight seeds in chainparams.cpp for the default port 8333, and the option -dnsseed is on unless the user gave -connect or limited the connections to none (Bitcoin Core, 2026). "
 "On 2026-10-15 all eight names were resolved from the sandbox and gave 182 distinct IPv4 addresses, 20 to 29 for each seed; a raw TCP connection to port 8333 of one of them could not be opened from the sandbox, so no mainnet peer was contacted and the claim is about the seeds, not the peers behind them. "
 "A seed is like the information desk at a station: you ask once, you get a handful of names, and from then on you ask the people you meet. The developer guide describes the same procedure (Bitcoin Project, 2026).")

A["AddrGossipFormat"] = (
 "Once a node is connected it learns more addresses by asking, with the message getaddr, and the peer answers with addr or addrv2 messages of addresses it knows; Bitcoin Core answers at most 23 percent of its address book, with a ceiling on the number, so that no crawler can copy the whole list with one question (Bitcoin Core, 2026). "
 "In the run the address manager of the test node held 103 addresses and the answer held 23, both in the old addr message and in the addrv2 message, which is the 23 percent of MAX_PCT_ADDR_TO_SEND in net_processing.cpp. "
 "The book explains the idea of bootstrapping from one connection that offers introductions to further peers, and the use of seed nodes as the last resort (Antonopoulos and Harding, 2023). Gossip of this kind works like telling a stranger the names of a quarter of your friends: enough to get them started, not enough to hand over the whole address book.")

A["Addrv2Networks"] = (
 "The old addr message had room for 16 bytes of address, enough for IPv4 and IPv6, and it could hold the old 80-bit Tor addresses in a disguise, but not the 32-byte keys of Tor version 3, of I2P and of CJDNS; BIP 155 therefore introduced addrv2, in which each entry has a network number and an address of the length that network needs (Van der Laan, 2019). "
 "A peer that sends sendaddrv2 before verack asks to be told addresses in this form; in the run the node answered with addrv2 entries of network 1 (IPv4, 4 bytes) and network 2 (IPv6, 16 bytes), and the node's address manager held 78 IPv4 and 25 IPv6 addresses, 103 in all (Bitcoin Core, 2026). "
 "Bitcoin Core supports the message since release 0.21.0, together with Tor version 3 (Bitcoin Core developers, 2021). It is like a form with a new box for long names: the old form cut the name off after 16 letters, the new one says how long the name is.")

A["ConnectionTypes"] = (
 "A node does not treat all its connections alike: Bitcoin Core keeps 8 outbound full-relay connections, 2 outbound block-relay-only connections that carry no loose transactions and no addresses, which makes it harder to map the network, short-lived feeler connections that test whether an address is alive, and addr-fetch connections that only ask for addresses and leave, up to 125 connections in all (Bitcoin Core, 2026). "
 "These numbers are written as constants in net.h and the type of each connection is reported in the field connection_type of getpeerinfo, which the book lists (Antonopoulos and Harding, 2023). "
 "In the run, connections of the three types were opened and read from the peer listing: outbound-full-relay and addr-fetch relayed transactions, and block-relay-only did not and spoke the v1 transport, the old plaintext one. "
 "It is like a restaurant with different tables: the regular table gets everything, the table by the kitchen door only gets what the kitchen sends out, and a few waiters walk through the room only to see if anybody is still there.")
