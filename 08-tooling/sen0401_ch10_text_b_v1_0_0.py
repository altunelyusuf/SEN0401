"""SEN0401 chapter 10: the teaching paragraphs of the leaves of subjects 3 (block relay) and 4 (syncing). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
B = {}

B["BlockFindingRaceProbability"] = (
 "Blocks are found by chance at an average of one in ten minutes, and while a new block travels through the network, other miners are still working on the old tip; if one of them finds a block in that time, two blocks compete for the same height, and one of them will be orphaned, its work wasted (Antonopoulos and Harding, 2023). "
 "If blocks arrive as a Poisson process with an average gap of 600 seconds, the chance that a rival block appears within d seconds is 1 minus e to the power of minus d over 600; this gives 0.33 percent for 2 seconds, 1.65 percent for 10 seconds and 6.45 percent for 40 seconds, computed in the chapter's library. "
 "That is why faster block relay is a security matter and not only a comfort: the Bitcoin Optech topic page on compact block relay presents it as a way to cut the delay (Bitcoin Optech, 2026). "
 "It is like two runners who start a relay at almost the same moment: the longer the baton takes to be passed, the more likely that somebody else has already started on the same leg.")

B["SendheadersAnnouncement"] = (
 "In the original protocol a node announces a new block to its peers with an inv message that holds only the hash of the block; the peer must answer with getheaders or getdata, and only then does the header arrive, which costs a round trip. "
 "BIP 130 added the message sendheaders: a peer that sends it says that new blocks should be announced directly with a headers message, and the saved text of the BIP gives the reason that it saves one round trip and the bandwidth of the hash lists (Daftuar, 2015). "
 "In the run a peer that did not send sendheaders was told of a new block by an inv message and a peer that did was sent a headers message, as the protocol says (Bitcoin Core, 2026). It is like a shop that, instead of a card saying that a parcel has arrived for you, phones you and reads you the label: you save the walk to the counter.")

B["ShortIdsAreSixBytes"] = (
 "A compact block, defined by BIP 152, is a block that does not repeat what the receiver most likely has already: instead of each transaction it contains a short identifier of 6 bytes, computed from the transaction's wtxid with SipHash-2-4 and a key derived from the block header and a nonce (Corallo, 2016). "
 "The constant SHORTTXIDS_LENGTH of blockencodings.h is 6 (Bitcoin Core, 2026). In the run a block of 13 transactions was announced as a cmpctblock message of 332 bytes where the whole block had 3,062 bytes (10.84 percent), with 12 short ids that the independent SipHash code of this chapter reproduced one by one; the same code reproduced the reference test value a129ca6149be45e5 of the SipHash paper. "
 "The saving grows with the block: a mainnet block of 1,000 transactions is shorter by a few hundred kilobytes, but this was not measured here, since the sandbox cannot reach mainnet peers. "
 "It is like a seating plan: instead of writing every guest's full name, the host writes a short code for each, because everybody in the room already knows who is who.")

B["CoinbaseIsPrefilled"] = (
 "A compact block can carry a few transactions in full, the prefilled transactions, because the sender knows that the receiver cannot have them: the first one is always the coinbase transaction, which exists only inside the block and was never in anyone's mempool (Corallo, 2016). "
 "The book says that Bitcoin Core always sends a block's first transaction this way, in its description of compact blocks (Antonopoulos and Harding, 2023). In the run the compact block listed exactly one prefilled transaction, at index 0, and its transaction id was the id of the coinbase transaction of the block. "
 "The index is sent as a difference from the one before, so index 0 is a single byte. The coinbase is like the host's own name card on the table plan: all the other guests are known by a code, but nobody except the host holds that one.")

B["MissingTransactionsRequest"] = (
 "When a compact block names a transaction that the receiver does not have, the receiver asks for it with getblocktxn, giving the block hash and the indexes of the missing transactions, and the sender answers with blocktxn that holds those transactions in full; with that the block is complete and can be checked as usual (Corallo, 2016). "
 "In the run the script asked with getblocktxn for the transactions at indexes 1 and 2 of the block, as if it had not had them, and the blocktxn message that came back held exactly the two transaction ids that the block lists at those positions (Bitcoin Core, 2026). "
 "A missing transaction costs one round trip more, which is why the efficiency of compact blocks depends on how similar the mempools of the sender and receiver are. It is like a recipe that says use the butter you have in the fridge: if you have none, you phone and ask for it, and cooking goes on a little later.")

B["HighAndLowBandwidthModes"] = (
 "BIP 152 has two modes. In high-bandwidth mode the sender pushes the cmpctblock to a peer at once, before even validating the whole block, which is the fastest; in low-bandwidth mode it only announces the block with a headers or inv message, and the peer asks for the compact block if it wants it (Corallo, 2016). "
 "A peer picks the mode with the message sendcmpct, and because high-bandwidth mode costs the sender bandwidth when several peers are told of the same block, Bitcoin Core allows only three peers to be in that mode, which is the test lNodesAnnouncingHeaderAndIDs.size() >= 3 in net_processing.cpp (Bitcoin Core, 2026). "
 "In the run the node showed the script in its peer listing as a high-bandwidth peer (bip152_hb_to true) and sent the compact block without being asked; in low-bandwidth mode the node announced nothing by cmpctblock, and the compact block that the script then asked for was identical to the unasked one. "
 "It is like a newsagent who delivers the paper to three loyal customers at the door and keeps it on the counter for everybody else.")

B["CompactBlockDepthLimit"] = (
 "A node answers a request for a compact block only if the block is recent: older blocks are sent whole, because a long time has passed and the receiver's mempool may have changed so much that a compact block would need many more round trips than a whole one. "
 "The limit is the constant MAX_CMPCTBLOCK_DEPTH = 5 in net_processing.cpp (Bitcoin Core, 2026). In the run the script asked for a block that was 20 blocks deep as a compact block and the node answered with a normal block message. "
 "The reasoning behind the limit follows from BIP 152, where compact blocks are meant to be used at the tip of the chain, where mempools agree most (Corallo, 2016). It is like the rule that you may borrow the fresh newspaper from the counter, but last month's papers have to be fetched from the archive.")

B["CompactBlocksYear"] = (
 "The book dates compact block relay to a release of Bitcoin Core in 2015 (Antonopoulos and Harding, 2023). That is an error of the year. BIP 152 was assigned its number on 2016-04-27 according to its header, and Bitcoin Core's own table of BIPs says that the BIP is implemented as of version 0.13.0, whose release notes list compact blocks as a pull request of Suhas Daftuar (Corallo, 2016); (Bitcoin Core, 2026). "
 "Release 0.13.0 appeared in August 2016 (Bitcoin Core developers, 2016). The 2015 of the book may come from the earlier work of Matt Corallo on the relay network, which was in use in 2015 but was a different thing, a separate network of servers. "
 "Dates in a book are like the dates on an old photograph: if two sources written at the time agree, they outweigh the caption.")

B["ForwardErrorCorrectionDemo"] = (
 "Forward error correction adds redundant data to a message so that the receiver can rebuild parts that were lost without asking for them again, which matters on a link where a lost packet costs a whole round trip or where the sender cannot be asked; FIBRE, Matt Corallo's relay system for miners, uses it on UDP together with compact blocks (Corallo, 2016). "
 "The simplest code of this kind is parity. A message of 24 bytes was cut into four parts of 6 bytes and a fifth part was made as the XOR of the four; when one of the four was deleted, the XOR of the other three and the fifth part gave it back and the whole message was equal to the original, in the chapter's library. "
 "Real FIBRE codes are stronger, they survive several losses, but the idea is the same. The Bitcoin Optech topic page on compact block relay describes the compact block idea on which FIBRE builds (Bitcoin Optech, 2026). It is like sending a letter with an extra page that says the sum of all the page numbers: if one page is lost on the way, the sum tells you what is missing.")

B["RelayNetworkHistory"] = (
 "Before compact blocks, miners built private networks for sending blocks to each other fast. The book names the relay network of Matt Corallo, created in 2015 and replaced in 2016 by a better design (Antonopoulos and Harding, 2023). "
 "The successor is FIBRE, the Fast Internet Bitcoin Relay Engine, which according to its own site is a UDP transport with forward error correction and compact blocks (Corallo, 2016). "
 "Neither could be run in the sandbox, because both need a real network of servers, so this leaf is a claim taken from the book and the site and not recomputed. Their point is also that they are not part of the peer-to-peer protocol that every node speaks: they are extra roads that miners build for themselves, like a private motorway beside the public road.")

B["HeadersBatchOf2000"] = (
 "A new node first downloads the headers of the whole chain and only then the blocks, which is called headers-first synchronization; the node asks with getheaders and the peer answers with at most 2,000 headers in one headers message, the constant MAX_HEADERS_RESULTS in net_processing.h (Bitcoin Core, 2026). "
 "Each header in the message takes 81 bytes, the 80 bytes of the header and a zero for the number of transactions. In the run a node whose chain was 2,101 blocks high answered a request with one message of 2,000 headers (162,003 bytes) and a second of 101, and the two together equalled the height of the chain. "
 "The book describes the same process, a getheaders request answered by the first 2,000 headers in a headers message, repeated until the node has all of them (Antonopoulos and Harding, 2023). It is like asking for the table of contents of a book first: a few pages tell you what is in it before you decide what to carry home.")

B["HeaderChainLinks"] = (
 "Every block header holds the hash of the header before it, so that the headers form a chain from the genesis block to the tip, and a node can check the whole chain of headers by itself, without any block, by hashing each header twice with SHA-256 and comparing the result with the next one's previous-hash field, also checking that the work is high enough (Nakamoto, 2008). "
 "In the run the independent code of this chapter walked the 2,101 headers received from the node, 80 bytes each, and found that each one pointed at the hash of the one before it and that the last one hashed to the tip that the node reported. "
 "The book describes the header in its chapter on the blockchain (Antonopoulos and Harding, 2023), and in its chapter 10 it shows lightweight clients that synchronize the headers alone. It is like a line of people who each hold the hand of the one before: you can see that nobody was skipped without asking what they carry in their bags.")

B["DownloadWindow"] = (
 "Once the headers are known, the node fetches the blocks in parallel from several peers, but not too far ahead: Bitcoin Core only requests blocks inside a window of 1,024 blocks beyond the last block that it has, and it keeps at most 16 blocks in transit from one peer, so that one slow peer cannot hold up the whole download (Bitcoin Core, 2026). "
 "The two numbers are the constants BLOCK_DOWNLOAD_WINDOW and MAX_BLOCKS_IN_TRANSIT_PER_PEER of net_processing.cpp. In the run a fresh node was connected to the test node and synchronized a chain of 2,105 blocks in about 2.5 seconds, the chain then being equal to the peer's, and the getheaders request in its log was 69 bytes. "
 "The book describes the same limit as a queue of up to 1,024 blocks and adds that a node drops a peer that is too slow to deliver the oldest block in the queue, while the per-peer limit of 16 is not in the book (Antonopoulos and Harding, 2023). A window is like the number of books you are allowed to take from the library at the same time: enough to keep reading, but no more than you can carry.")

B["HeadersPresync"] = (
 "A node that has only headers cannot yet tell whether a peer's chain is true, and an attacker could send millions of low-work headers to fill its memory; Bitcoin Core therefore uses headers presync: the headers of a new peer are first only counted and hashed down to a small commitment in a phase called PRESYNC, and are stored only once the chain has been shown to have enough work (Bitcoin Core, 2026). "
 "The phase is described in headerssync.h with the words PRESYNC means the peer has not yet demonstrated their chain has sufficient work. The field presynced_headers of getpeerinfo shows how far it is, and the field is already in the listing of the book, and was present in the peer information of the run (Antonopoulos and Harding, 2023). "
 "The protection is like a doorman who, before he lets a stranger into the club, asks him to show proof of an invitation and only then writes his name in the guest book.")
