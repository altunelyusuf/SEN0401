"""SEN0401 chapter 11: the teaching paragraphs of the leaves of subject 5 (merkle trees). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
C = {}

C["FourLeafTree"] = (
 "A merkle tree is built from the bottom: each transaction is hashed to give a leaf, and every pair of neighbours is joined (their two 32-byte hashes written one after the other, 64 bytes) and hashed twice again to give the parent, until one hash, the merkle root, is left (Antonopoulos and Harding, 2023). "
 "For the block of four transactions on the test chain the code of this chapter hashed the pairs by hand, H_AB = SHA256(SHA256(H_A || H_B)) and H_CD likewise, then the pair of those, and the result equalled the merkle root in the block's header, with levels of 4, 2 and 1 hashes (Bitcoin Core, 2026). "
 "The same method is described in the Bitcoin developer guide with the letters A to E (Bitcoin Project, 2026). "
 "Think of a knockout tournament: the players are the leaves, each match produces a winner, and the champion at the top stands for the whole field.")

C["OddLeafDuplicated"] = (
 "When a level has an odd number of hashes, the last one is paired with itself, so that the tree stays balanced; the book shows this for three transactions, where transaction C is duplicated (Antonopoulos and Harding, 2023). "
 "On the test chain the block with three transactions had levels of 3, 2 and 1 hashes, the root h(h(A||B) || h(C||C)) equalled the header's merkle root, and the same rule reproduced the root of all eight blocks with 1 to 8 transactions (Bitcoin Core, 2026). "
 "The developer guide draws the same picture with E paired with itself (Bitcoin Project, 2026). "
 "The rule is simple and has a price, which the section on the design flaw shows. "
 "It is like a football draw with an odd number of teams, in which one team plays a 'match' against its own shadow and moves on.")

C["RootIsAlways32Bytes"] = (
 "However many transactions a block holds, its summary in the header is a single 32-byte hash, because a hash always has the same length (Antonopoulos and Harding, 2023). "
 "The test chain's blocks of 1, 2, 8 and 16 transactions all have a 32-byte root, block 840,000 with its 3,050 transactions has a root of 32 bytes too (031b417c...), and for a block with a single transaction the root is that transaction's id: the genesis block's merkle root 4a5e1e4b... is the id of its only transaction (Mempool Space, 2026); (Bitcoin Core, 2026). "
 "This is the strength of a commitment: the header can stay small and the data behind it can grow. "
 "It is like the barcode on a pack, which has the same width whether the pack holds a single biscuit or a whole case.")

C["TreeDepth"] = (
 "The depth of a merkle tree, the number of hashing steps from a leaf to the root, is the ceiling of the base-2 logarithm of the number of leaves, so proving that one transaction is included takes about log2(N) hashes (Antonopoulos and Harding, 2023). "
 "The code gave depths of 0 for 1 transaction, 2 for 4, 4 for 16, 6 for the 40 transactions of block 277,315, 12 for the 3,050 of block 840,000 and 14 for 16,000, and building the real tree of block 277,315 level by level gave exactly 6 steps (Mempool Space, 2026); (Bitcoin Core, 2026). "
 "A logarithm grows so slowly that doubling the size of a block adds only one step. "
 "It is like finding a name in a phone book by opening in the middle each time: a book ten times as thick needs only about three more openings.")

C["RealBlockRoot"] = (
 "The strongest test of the construction is a real block: mempool.space lists the 40 transaction ids of block 277,315, from 257e7497... to 05cfd38f..., and the merkle root computed from them with the rule of the book is 5e049f40..., the value in the block's header and in the book's listing (Mempool Space, 2026); (Antonopoulos and Harding, 2023). "
 "The code does nothing but the pairing and double hashing of the chapter, with the ids taken in their internal byte order (Bitcoin Core, 2026). "
 "The result holds for a block mined in December 2013 as it does for one mined today. "
 "It is like checking a sum of forty receipts: if the total at the bottom of the page is right, then every receipt that was added must be among them.")

C["HashTreeHistory"] = (
 "The hash tree is named after Ralph Merkle, who patented it in 1979; the patent, US 4309569 'Method of providing digital signatures', was published on 5 January 1982 and assigned to Stanford University, and it explains both the tree and its use for many one-time signatures (Wikipedia contributors, 2026). "
 "Merkle wrote about tree authentication for public file directories in his paper Protocols for Public Key Cryptosystems of 1980 (Merkle, 1980). "
 "Nakamoto's paper uses the tree to let old blocks be compressed by discarding the interior hashes of the tree, so only the root remains in the header (Nakamoto, 2008). "
 "The tree is like a company's organization chart: the chief executive need not know every employee, only the few managers who each answer for a branch.")

C["Cve20122459Trees"] = (
 "The rule that an odd last hash is duplicated has a consequence that a comment in the source calls a serious flaw: different lists of transactions can have the same merkle root (Antonopoulos and Harding, 2023); (Bitcoin Core, 2026). "
 "The book's example is the lists [1,2,3,4,5,6] and [1,2,3,4,5,6,5,6], and the code of this chapter reproduced it with six dummy ids: the roots are equal although the lists have 6 and 8 entries; [1,2,3] and [1,2,3,3] also agree, whereas [1,2,3,4] and [1,2,3,4,3,4] do not, because the duplication only works at the end of a level that is odd. "
 "A block with the longer list has the same header and the same block hash but is invalid, and Optech's description is that a node that stored the invalid form's hash as bad would refuse the good block from everybody (Bitcoin Optech, 2026). "
 "It is like a cashier who, to save time, counts the last odd coin twice: a customer can hand in an extra coin pair that changes nothing in the total.")

C["NodeRejectsMutatedBlock"] = (
 "Because the mutated block has the same hash as the original, a careless node could remember that hash as bad and then refuse the good block (Bitcoin Optech, 2026). "
 "Bitcoin Core avoids it, and the test chain showed how: a block of 3 transactions was changed into one of 4 by repeating the last transaction, with the header unchanged and the same hash; submitblock answered bad-txns-duplicate, the node still did not know the block afterwards (getblockheader said Block not found), and when the original block was submitted afterwards it was accepted and became the tip (Bitcoin Core, 2026). "
 "The attack would have let someone feed a node a doctored copy and keep it from learning the true block, a form of the eclipse attack. "
 "It is like a post office that returns a forged parcel to the sender but does not blacklist the address: the real parcel with the same label is still delivered when it arrives.")

C["MutationDefenseInSource"] = (
 "The defence is written into the code: merkle.cpp warns against the flaw in its comment and its root function reports through a mutated flag when two identical hashes meet at the end of a level, and validation.cpp turns this into the result BLOCK_MUTATED with the reason bad-txns-duplicate (Bitcoin Core, 2026). "
 "The book reproduces the comment, with slight revisions, in a box (Antonopoulos and Harding, 2023). "
 "Optech's timeline is that the vulnerability was reported in 2012, assigned the number CVE-2012-2459 and fixed quietly without being exploited as far as is known, that a variation was reintroduced in version 0.13.0 of 2016 and fixed in 0.14.0, and that another variation was found and fixed in 2023 (Bitcoin Optech, 2026). "
 "A bug of this kind is like a hole that is closed in the fence and then reopens when the fence is rebuilt, which is why a good comment stays in the code.")

C["SixtyFourByteWeakness"] = (
 "The tree has a second weakness: an inner node is the hash of exactly 64 bytes, two child hashes side by side, and a transaction whose serialization without witness data is exactly 64 bytes can be mistaken for an inner node (Poinsot and Corallo, 2025). "
 "The code showed the size, 2 x 32 = 64 bytes for the inner node of the test chain's block, and the smallest transaction is 60 bytes (a weight of 240), so a 64-byte transaction is only four bytes above the minimum and can exist (Bitcoin Core, 2026). "
 "Optech names this weakness CVE-2017-12842, discovered in 2017, and BIP 54 of the consensus cleanup proposal closes it by making such transactions invalid (Bitcoin Optech, 2026); (Poinsot and Corallo, 2025). "
 "A light client that checks a merkle path is the one at risk, because it cannot see the whole block. "
 "It is like a counterfeit note printed to the size of a wage envelope: at a glance the envelope and the note are the same thing.")

C["MerklePathOf16"] = (
 "To prove that one transaction is in a block, a node does not send the whole block but a merkle path: the one sibling hash at every level of the tree, so that the checker can recompute the root (Antonopoulos and Harding, 2023). "
 "The book's example is transaction K among 16, a path of four hashes, H_L, H_IJ, H_MNOP and H_ABCDEFGH, 128 bytes; the block of 16 transactions on the test chain gave the same thing for its 11th transaction, index 10: a path of 4 hashes with the siblings on the right, left, right and left, and following it reproduced the merkle root in the header (Bitcoin Core, 2026). "
 "Bitcoin Core's own gettxoutproof for that transaction verified with verifytxoutproof. "
 "It is like proving that you belong to a family by showing a chain of cousins' names instead of the whole family album.")

C["PathLengthLogarithm"] = (
 "The size of a path grows with the logarithm, not with the count of transactions: a block of 1,024 transactions needs 10 hashes (320 bytes), 4,096 needs 12 (384 bytes) and 16,000 needs 14 (448 bytes), the numbers behind the book's statement of paths of 10 or 12 hashes (Antonopoulos and Harding, 2023). "
 "The code checked these, and a path through the real tree of block 277,315, which has 40 transactions, had 6 hashes, 192 bytes (Mempool Space, 2026); (Bitcoin Core, 2026). "
 "A thousand transactions are therefore proved by a few hundred bytes. "
 "It is like the questions in the game of twenty questions: with ten questions that cut the field in half each time you can single out one of a thousand.")

C["ProofSizeVsBlock"] = (
 "The book closes the section by saying that the largest possible proof is almost 10,000 times smaller than the largest block, but the numbers do not quite support this (Antonopoulos and Harding, 2023). "
 "A proof needs the 80-byte header and 448 bytes of path, 528 bytes, and a block of 4,000,000 bytes is 7,576 times larger than that; if the transaction itself, say 250 bytes, is counted as the book says, the ratio is 5,141; to reach 10,000 the proof would have to be 400 bytes, less than the header and the path together. "
 "The idea of the book is right and the factor is overstated by about a third against the header and path alone and by almost double with a typical transaction, an erratum of arithmetic and not of principle. "
 "It is like saying that a postcard is ten thousand times lighter than a parcel when it is in fact five or seven thousand times: the point that it is far lighter stands.")

C["MerkleblockForLightClients"] = (
 "A lightweight client does not download blocks; it receives a merkleblock message, which holds the header and a merkle path to the transaction it asked for, and with the header it checks that the transaction is in the block and the block is in the chain (Antonopoulos and Harding, 2023). "
 "Bitcoin Core's gettxoutproof makes such a message, and on the test chain the one for a transaction of the block with 16 transactions was 248 bytes (80 of header, the count 16, 5 hashes, 2 bytes of flags) against 3,580 bytes for the block, verified by verifytxoutproof; for a block of 4 transactions it was 183 bytes (Bitcoin Core, 2026). "
 "The book states that the client receives less than a kilobyte, more than a thousand times less than the block of about 2 MB; block 840,000 had 2,325,617 bytes (Mempool Space, 2026). "
 "The book ties this to Bloom filters, which Bitcoin Core now keeps off by default, so a client today gets the proof by other means. "
 "It is like a receipt with a stamp: a small piece of paper that proves a purchase without the whole shop's accounts.")

C["MerkleProofDirection"] = (
 "A merkle path is not just a list of hashes: it also matters on which side each sibling lies, because the double hash of A||B is not that of B||A (Antonopoulos and Harding, 2023). "
 "The sides are given by the position of the transaction: for the transaction at index 10, binary 1010, the lowest bit 0 means that the node is a left child and its sibling is on the right, the next bit 1 that the sibling is on the left, and so on, so the sides run right, left, right, left. "
 "The code followed the path with the right sides and recovered the root of the test chain's block, and with the sides swapped it did not (Bitcoin Core, 2026). "
 "It is like the two halves of a handshake password: the same words in the wrong order do not open the door.")
