"""SEN0401 chapter 10: the teaching paragraphs of the leaves of subject 5 (light clients: SPV, bloom filters, block filters). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
C = {}

C["HeaderChainSize"] = (
 "A lightweight client does not download the blocks; it downloads only the block headers, 80 bytes per block, and asks other nodes for proof that a payment is in a block, an idea that Satoshi Nakamoto described as simplified payment verification in the eighth section of the paper (Nakamoto, 2008). "
 "The book says that the headers are about 10,000 times smaller than the blockchain (Antonopoulos and Harding, 2023). With the data of 2026-10-15 the claim holds almost exactly: at height 971,499 the headers total 80 x 971,500 = 77.7 megabytes, the Blockchain.com chart gives about 775,272 megabytes for the whole chain, and the ratio is 9,975 (Blockchain Charts, 2026); (Mempool Space, 2026). "
 "The ratio only grows with time, because every block adds 80 bytes to the headers and more than a megabyte to the chain. A library catalogue is small next to the library, and you can carry it on your phone, though you have to trust the librarian for what the shelves hold.")

C["MerklePathProof"] = (
 "A transaction can be shown to be in a block with a Merkle path: the transactions of a block are hashed in pairs up to a single root that sits in the header, and the proof for one transaction is the hash of each sibling on the way up, so that a client with the header can recompute the root and compare (Nakamoto, 2008). "
 "In the run a block of 5 transactions needed a path of 3 hashes, since the tree for 5 leaves is three levels high; the independent code of this chapter rebuilt the root from the transaction and the path and found it equal to the root in the header, the proof message was 215 bytes against the 4,448 bytes of the block, and the node's own verifytxoutproof returned the same transaction (Bitcoin Core, 2026). "
 "The path grows with the logarithm of the number of transactions, so for a block of 4,000 transactions it is about 12 hashes. It is like proving that a letter was in a sealed mailbag by showing the seals of a few other letters, so that the person with the master seal can check the whole bag.")

C["SixConfirmationsOdds"] = (
 "A light client cannot check the rules itself, so it trusts the work: a payment buried under six blocks is safe unless an attacker has a large share of the hash rate, and Nakamoto's paper calculates the chance that an attacker with a share q ever catches up from z blocks behind, using a Poisson distribution for the progress the attacker makes while the honest chain finds its z blocks (Nakamoto, 2008). "
 "The computation in the chapter's library gives 0.0002428 for q = 0.1 and z = 6, the value printed in the paper, and 0.1321 for q = 0.3. "
 "The headers that a client needs to watch these six blocks are small: 80 bytes x 6 blocks an hour x 24 x 365 days is 4,204,800 bytes, about 4 megabytes a year, which the paper puts as a small fraction of what a full node stores (Nakamoto, 2008). "
 "It is like a bet on a race that the chaser has already almost lost: the further ahead the leader is, the longer the odds on the chaser.")

C["ToyBloomFilter"] = (
 "A Bloom filter is a row of bits and a few hash functions, used to ask whether an item might be in a set: to add an item, the bits at the positions given by its hashes are set; to test an item, all its positions are looked at, and a single zero means definitely not there, while all ones mean maybe there (Wikipedia contributors, 2026). "
 "The book explains the filter with a row of 16 bits and the patterns A and B (Antonopoulos and Harding, 2023). In the chapter's version with three hash functions two patterns set 6 bits, both patterns are found, and a test with 20,000 random patterns said maybe in 5.3 percent of the cases although none of them had been added. "
 "The usual formula gives 3.1 percent; the exact value for six bits set out of sixteen is (6/16) to the third power, 5.27 percent, because the formula assumes a large filter. "
 "It is a doorman with a list that has been smudged: he can say definitely not on your name, but when the smudges fit, he lets someone in by mistake.")

C["BloomFilterWireFormat"] = (
 "BIP 37 let a lightweight client send a Bloom filter to its peer with the message filterload, and from then on the peer sent only the transactions that matched it, together with a merkleblock for each block (Hearn and Corallo, 2012). "
 "The message holds the filter bytes, the number of hash functions, a tweak and flags; the limits of 36,000 bytes and 50 hash functions are the constants MAX_BLOOM_FILTER_SIZE and MAX_HASH_FUNCS (Bitcoin Core, 2026). "
 "The unit test of Bitcoin Core builds a filter for three elements at a false-positive rate of 0.01 and compares it to the bytes 03614e9b050000000000000001; the independent MurmurHash3 code of this chapter produced the same bytes, which shows that the description of the hash is complete and correct. "
 "Like a postal code, the filter is a short code that many addresses share, so the post office can tell you which houses might be yours but not which one exactly.")

C["MerkleblockForOneMatch"] = (
 "When a filter is loaded, the node answers a request for a filtered block with a merkleblock message: the header and a partial Merkle tree holding only the paths to the transactions that match, followed by those transactions as ordinary tx messages (Hearn and Corallo, 2012). "
 "In the run a wallet transaction was the only one to match a filter of 7 bytes with 12 hash functions; the merkleblock was 215 bytes against 4,448 bytes for the block of 5 transactions, the partial tree led to the root in the header, and the node then sent the one transaction. "
 "The book gives the same sequence in its explanation of how lightweight clients use filters (Antonopoulos and Harding, 2023). It is like asking an accountant for only the pages of the ledger that mention you, with the seal of the ledger that proves they belong to it.")

C["BloomDisabledByDefault"] = (
 "Bloom filters cost the node work and, as Gervais and others showed, give the node a view of the client's addresses with weak privacy, since a node that gets the filter can often work out which addresses belong to the wallet (Gervais et al., 2014). "
 "Bitcoin Core therefore turned the service off by default: the release notes of 0.19.0.1 say that the -peerbloomfilters option now defaults to false, and the table of BIPs says that BIP 37 is disabled by default since v0.19.0 (Bitcoin Core developers, 2019). "
 "A service bit, NODE_BLOOM of BIP 111, tells the peers if it is offered (Corallo and Todd, 2015). In the run a node with default options did not set the bit and closed the connection of a peer that sent filterload, and the help text of Bitcoin Core 31.1 shows the default 0; in the census only 4,308 of 25,361 nodes set the bit. "
 "The book explains the filters at length and presents the block filters as the safer replacement of BIP 37, but it does not say that Bitcoin Core switched the service off by default in 0.19 (Antonopoulos and Harding, 2023). A shop that stopped handing out loyalty cards because they revealed what customers buy is a fair picture.")

C["GolombWorkedExample"] = (
 "A Golomb-coded set stores a sorted list of numbers compactly by storing the differences between neighbours, which are small, and the book explains it with the numbers 849, 653, 476, 900 and 379 (Antonopoulos and Harding, 2023). "
 "Sorted they are 379, 476, 653, 849, 900; the differences are 379, 97, 177, 196 and 51, so after the first number the largest needs 8 bits where the largest original needs 10, and adding them back gives the list again, as the chapter's code verified. "
 "The book then explains the idea with two dice, counting how often each difference 0 to 5 occurs among the 36 throws: 6, 10, 8, 6, 4 and 2, which the code confirmed. "
 "Wikipedia describes Golomb coding as a lossless method for numbers drawn from a geometric distribution (Wikipedia contributors, 2026). It is like telling someone the way by the distance from one crossing to the next, never from the start: the numbers stay short.")

C["GolombRiceRoundTrip"] = (
 "Golomb-Rice coding writes each difference d in two parts, the quotient d divided by 2 to the power P in unary (that many ones and a zero) and the remainder in P plain bits; the choice of P fits the code to how big the differences usually are (Osuntokun and Akselrod, 2017). "
 "The code of this chapter coded the sorted numbers 379, 476, 653, 849 and 900 with P = 7: the result took 44 bits in 6 bytes, whereas the same five numbers with a fixed width of 10 bits would take 50, and decoding gave the same numbers back. "
 "For such a tiny list the saving is small, but real filters hold thousands of numbers. It is like writing amounts in a shop as small change plus a tally mark for each hundred: short for small amounts, and longer only when the amount is big.")

C["BasicFilterParameters"] = (
 "The one filter type that BIP 158 defines, the basic filter, hashes every script of a block to a number in a range of N x M with SipHash-2-4 keyed by the block hash, sorts them and stores the differences with Golomb-Rice coding at P = 19, where M = 784931 (Osuntokun and Akselrod, 2017). "
 "The constants are the result of an analysis in the BIP: P = 19 makes the filters small, and M = 784931 sets the false-positive rate to about one in 784,931 per element. "
 "The independent implementation of this chapter reproduced all 10 test vectors that the BIP publishes for testnet blocks, both the filters and the chained filter headers, and its SipHash returned the reference value a129ca6149be45e5 of the SipHash paper (Osuntokun et al., 2018). "
 "Bitcoin Core builds the same filters in blockfilter.cpp (Bitcoin Core, 2026). The two numbers are like the mesh of a net: a fixed size chosen so that nearly all fish of the wrong kind pass through.")

C["FilterEqualsNodeFilter"] = (
 "A block filter is the compressed set of what a block touches: the output scripts of the block and the scripts of the outputs it spends, without duplicates and without OP_RETURN scripts, and the node can serve it with the RPC getblockfilter (Osuntokun and Akselrod, 2017). "
 "In the run a block of 9 transactions gave 104 elements and a filter of 275 bytes; the independent code of this chapter, which uses only the block, the scripts of the spent outputs and the BIP, built the same 275 bytes and the same filter header, the hash of the filter chained with the header before it (Bitcoin Core, 2026). "
 "That two programs that share no code agree is the best test that a specification is complete. The book explains the filter as something that a client downloads and checks locally, which is why a faithful copy matters (Antonopoulos and Harding, 2023). It is like two cooks who follow the same recipe in separate kitchens and get the same cake.")

C["FilterBitsPerElement"] = (
 "The book explains the filter as a lossy encoding in which each output script of at least 160 bits is reduced to just 64 bits, and the 64-bit values are sorted and coded as differences (Antonopoulos and Harding, 2023). "
 "That description is not the size of the filter. BIP 158 does not use a 64-bit range: it hashes each script into the range N x M, so that a block with 104 elements needs numbers of about 26 bits, and Golomb-Rice coding with P = 19 then stores each difference in about 21 bits (Osuntokun and Akselrod, 2017). "
 "The filter in the run held 104 elements in 275 bytes, which is 21.15 bits per element, a third of the 64 bits of the book. "
 "A student who sized the download of filters for a wallet with the book's 64 bits would be three times too pessimistic. It is as if the shop receipt said that each item was reduced to a barcode of 64 digits, whereas the cash register keeps only the last 21.")

C["FilterSkipsOpReturn"] = (
 "The basic filter leaves out every output script that starts with OP_RETURN, because such an output carries data and can never be spent, so a wallet would never look for it; BIP 158 says that the elements are all output scripts of the block and the spent ones aside from all OP_RETURN output scripts (Osuntokun and Akselrod, 2017). "
 "The block in the run had 2 OP_RETURN outputs, none of them was in the filter, and 144 scripts reduced to 104 elements after the OP_RETURN scripts and the repeated scripts were removed; the code in blockfilter.cpp has the matching test (Bitcoin Core, 2026). "
 "The book lists what goes into the filter, and the omission is a detail that is easy to miss (Antonopoulos and Harding, 2023). It is like an index at the end of a book that leaves out the footnotes that nobody will look up.")

C["FilterFalsePositiveRate"] = (
 "A client tests its own scripts against the filter it downloaded, and a match means that the block probably holds a payment to the client; the false-positive rate of the basic filter is about 1 in M = 784,931 per script, so the client rarely downloads a block for nothing (Osuntokun and Akselrod, 2017). "
 "In the run 400,000 random scripts were tested against the filter of the block and one of them matched, where 0.51 matches would be expected by 400,000 / 784,931; as it was a single run the count is a plausible draw and not a measurement of the rate, and every script of the block itself matched. "
 "Because a hit costs only a download of the block, the false positives do not harm privacy as the Bloom filters did, since the client asks for blocks and not for its addresses (Antonopoulos and Harding, 2023). A sieve that lets one wrong grain in a million pass is good enough for a kitchen.")

C["FiltersOverP2P"] = (
 "BIP 157 defines how a client gets the filters over the peer-to-peer network: getcfilters asks for the filters of a range of blocks, getcfheaders for the chain of filter headers and getcfcheckpt for a checkpoint every 1,000 blocks, and a node that offers this sets the service bit COMPACT_FILTERS (Osuntokun et al., 2017). "
 "In the run a node started with -peerblockfilters=1 advertised the bit, answered a request for 3 filters with 3 cfilter messages that equalled the filter of the block, and the cfheaders and cfcheckpt messages had 162 and 34 bytes; a node without the option disconnected the asking peer. "
 "The option -peerblockfilters is off by default, as the help text of Bitcoin Core 31.1 shows, and in the census of 2026-10-15 7,905 of 25,361 nodes set the bit (Bitnodes, 2026). Neutrino, the light client of Lightning Labs, is the best known user of the protocol (Lightning Labs, 2026).")

C["FilterIdeaPost2016"] = (
 "The idea that the client should download a small filter and test it itself came in a message to the bitcoin-dev mailing list from the anonymous developer bfd on 2016-05-09, with the title Committed Bloom filters for improved wallet performance and SPV security (Bfd, 2016). "
 "The book tells that an anonymous developer proposed it in 2016 (Antonopoulos and Harding, 2023). It became BIP 157 and BIP 158 through the work of Olaoluwa Osuntokun and Alex Akselrod, who replaced the Bloom filter by the Golomb-coded set (Osuntokun et al., 2017). "
 "Bitcoin Core indexed the filters in release 0.19.0 and served them to peers from 0.21.0, according to the table of BIPs (Bitcoin Core, 2026). The history shows how a design is moved from one forum post to a standard in about two years, a little like a recipe passed from a neighbour on a note to a cookbook.")
