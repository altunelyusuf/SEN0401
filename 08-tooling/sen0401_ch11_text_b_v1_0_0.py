"""SEN0401 chapter 11: the teaching paragraphs of the leaves of subjects 3 (the genesis block) and 4 (linking blocks). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
B = {}

B["GenesisHashRecomputed"] = (
 "The genesis block is the one block that no node needs to download, because its numbers are written in the program: chainparams.cpp calls CreateGenesisBlock with the time 1231006505, the nonce 2083236893, the bits 0x1d00ffff, version 1 and a reward of 50 coins (Bitcoin Core, 2026). "
 "The code of this chapter rebuilt the 204-byte coinbase transaction from those constants, got the transaction id 4a5e1e4b..., put it in an 80-byte header, and hashed it twice to obtain 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f, the hash that the book prints (Antonopoulos and Harding, 2023). "
 "Nothing was fetched from the network for this result, so the genesis block is a computation anyone can repeat. "
 "It is like the foundation stone of a building that carries its own date and can be checked against the plans: no one has to take the builder's word for it.")

B["GenesisCoinbaseMessage"] = (
 "The only input of the genesis block's single transaction has no previous output to spend, as in every coinbase, and its script carries a free text, here the 69 characters The Times 03/Jan/2009 Chancellor on brink of second bailout for banks (Antonopoulos and Harding, 2023). "
 "The script is a push of the number 486604799 (the bits 0x1d00ffff), a push of the number 4, and a push of the 69 bytes of text, which in hexadecimal begins 04ffff001d010445 and then spells the words (Bitcoin Core, 2026). "
 "The text proves that the block cannot have been made before that day, because the newspaper could not be quoted earlier, and it also marks the moment of the financial crisis of 2008 and 2009. "
 "It is like holding up the day's newspaper in a photograph of a hostage or a lottery winner: the photograph cannot be older than the paper.")

B["GenesisHardcoded"] = (
 "Every node starts with a chain of at least one block, because the genesis block is compiled into the program and cannot be changed, so it is the root from which a trusted chain is built (Antonopoulos and Harding, 2023). "
 "A Bitcoin Core 31.1 node started on the private test chain, with no peers and no data directory, reported height 0, 0 headers and 293 bytes of chain data, and the hash it called its best block equalled the genesis hash that the code of this chapter rebuilt from the regtest constants of chainparams.cpp (Bitcoin Core, 2026). "
 "A new node can therefore check any chain it is offered by following the parent links back to a block it already knows. "
 "It is like a family tree in which the oldest ancestor is printed on the first page: a visitor with a name can follow the line back until it reaches that page, and has no need to ask anybody who is on it.")

B["GenesisListingMatchesBook"] = (
 "The book prints the output of getblock for the genesis block, and the values can be checked against a block explorer's data: size 285, weight 1140, nonce 2083236893, bits 1d00ffff, time 1231006505 and a single transaction all agree with mempool.space (Antonopoulos and Harding, 2023); (Mempool Space, 2026). "
 "The chainwork shown in the listing ends in 100010001, which is the number 0x100010001 = 4,295,032,833, the work of one block at difficulty 1, as the code of this chapter computed (Bitcoin Core, 2026). "
 "The only things that have aged are the confirmations, 790,496 when the book was written and now over 971,000, and two fields that later releases added. "
 "A listing like this is a reference photograph: it has not changed, but the world around it has.")

B["SharedGenesisTransaction"] = (
 "Mainnet, testnet3, signet and regtest all start with the very same coinbase transaction, the 204-byte one with the id 4a5e1e4b... and the message from The Times, and differ only in the header around it: the time, the nonce and the bits (Bitcoin Core, 2026). "
 "Testnet4 breaks the pattern: its genesis coinbase is 180 bytes long, has the id 7aa0a7ae... and carries the message 03/May/2024 followed by a 64-digit hexadecimal number in the form of a block hash, in the manner of the headline in the first genesis block (Bitcoin Core, 2026); (Jahr, 2024). "
 "A shared transaction means shared coinbase text, which is why the regtest genesis block on a laptop also says The Times, and why the book's regtest listing and mainnet listing share the same merkle root 4a5e1e4b... (Antonopoulos and Harding, 2023). "
 "It is like a school that prints the same cover on every notebook: the covers are alike and only the pages inside differ.")

B["GenesisCoinbaseUnspendable"] = (
 "The 50 coins of the genesis block can never be spent: the Bitcoin Wiki says that this follows from a quirk in the way the genesis block is written in the code, and that it is not known whether it was intended (Bitcoin Wiki, 2026). "
 "A Bitcoin Core 31.1 node on the test chain confirmed the quirk in three ways: getrawtransaction refused the genesis coinbase with the message that it is not an ordinary transaction, gettxout found no output for it, and the UTXO set at height 0 held 0 outputs (Bitcoin Core, 2026). "
 "The book is silent on the point, and a student who tries to look the transaction up with the usual tools will be surprised (Antonopoulos and Harding, 2023). "
 "It is like the first coin that a shopkeeper nails to the wall: it is the first takings, it is proudly displayed, and it can never go into the till.")

B["ChancellorOfTheHeadline"] = (
 "The headline in the genesis block speaks of the Chancellor on brink of second bailout for banks, and the Chancellor of the Exchequer in office on 3 January 2009 was Alistair Darling, who served under Prime Minister Gordon Brown from 2007 to 2010 (Wikipedia contributors, 2026). "
 "The newspaper, The Times, began in 1785 under the title The Daily Universal Register and took its modern name on 1 January 1788, so it is a daily with a long record, a respectable witness for a date (Wikipedia contributors, 2026). "
 "The book points to the headline as proof of the earliest date and as a reminder of the crisis in which Bitcoin was launched (Antonopoulos and Harding, 2023). "
 "The timestamp in the genesis header, 2009-01-03 18:15:05 UTC, falls on the same day as the issue. "
 "A headline in a block is like the date on a milk carton: it tells you the earliest day the milk could be fresh.")

B["PreviousHashPointsToParent"] = (
 "Each block commits to its parent by carrying the parent's hash in its previous-block field, and that sequence of hashes is the chain that runs back to the genesis block (Antonopoulos and Harding, 2023). "
 "For ten consecutive headers of the test chain, heights 480 to 489, the code of this chapter recomputed every header's hash and compared it with the previous-block field of the next header: 9 of 9 links agreed (Bitcoin Core, 2026). "
 "A full node checks this link for every block it receives, which is how it knows where to attach the block. "
 "It is like the page numbers and references in a ledger where each page begins with the closing balance of the page before: a missing or changed page shows at once.")

B["Block277315Links"] = (
 "The book's example is a real pair of blocks: a node whose tip is block 277,314 with the hash 00000000000000027e7b... receives a block whose previousblockhash is that value, and so extends the chain to height 277,315 (Antonopoulos and Harding, 2023). "
 "The raw header of block 277,315 from mempool.space parses to version 2, time 1388185038 (2013-12-27 22:57:18 UTC), nonce 4215469401 and merkle root 5e049f40..., exactly the values in the book's listing, its previous hash equals the recomputed hash of block 277,314, and the difficulty 1180923195.25803, the size 43,560 bytes and the 40 transactions all agree (Mempool Space, 2026). "
 "The example therefore holds after more than ten years: a hash does not age. "
 "It is like a train whose coupling is checked at each station: the new carriage is accepted only if it fits the one in front.")

B["TamperingBreaksDescendants"] = (
 "Because the previous-block field is part of the header and so of the hash, changing a block changes its own hash and breaks the link in the next block, which would have to be changed and mined again, and so on up to the tip (Antonopoulos and Harding, 2023). "
 "In the experiment of this chapter one bit of the merkle root of block 483 of the test chain was flipped: the block's own hash changed, the previous-hash link of block 484 no longer matched, and 7 blocks, from 483 to 489, would have to be mined again (Bitcoin Core, 2026). "
 "At the difficulty of block 277,315 each of these re-mined blocks would take about 5 x 10^18 hashes, which is the practical meaning of a deep block being safe. "
 "It is like a row of dominoes glued edge to edge: you cannot take out one without breaking the glue of all those that stand behind it.")

B["ChainWorkAccumulates"] = (
 "A node does not follow the longest chain but the chain with the most accumulated work, and each header adds the work that its target stands for (Bitcoin Core, 2026). "
 "On the test chain, where every block has the bits 0x207fffff, one block is worth 2 units of work, so the chainwork printed by the node was 2, 4, 6 and 8 at heights 0 to 3 and 1002 (0x3ea) after the 501 blocks of the run, exactly 2 x 501; the genesis block of mainnet starts at 0x100010001, as the book's listing shows (Antonopoulos and Harding, 2023). "
 "The difference between length and work matters only when difficulty differs between the branches, and that is why the book can say 'longer chain' for the simple case. "
 "It is like a tug of war decided by the total strength on each rope and not by the number of people holding it.")

B["HashChainedTimestamps"] = (
 "The idea of linking records by hashes is older than Bitcoin: Stuart Haber and W. Scott Stornetta published How to Time-Stamp a Digital Document in the Journal of Cryptology in 1991, describing how each time-stamp can contain the hash of the one before so that records cannot be inserted or altered afterwards (Haber and Stornetta, 1991). "
 "Nakamoto's paper cites their work for the timestamp server on which the block chain is based, and describes how transactions are hashed in a Merkle tree, a structure from Ralph Merkle's work of 1980 on protocols for public-key systems (Nakamoto, 2008); (Merkle, 1980). "
 "What the block chain added was a way to agree on the order without a trusted time-stamping office, using proof of work. "
 "It is like a notary's book with numbered pages: nothing in it needs to be secret, but a page cannot be slipped in without the numbers showing it.")

B["GlacierCoreAnalogy"] = (
 "The book compares the chain to the layers of a glacier or an ice core: the top is loose and may change with the seasons, but a little way down the layers are stable and further down they are a record of millions of years (Antonopoulos and Harding, 2023). "
 "The comparison is not far off, because an ice core is built from the incremental buildup of annual layers of snow, the cores at Dome C in Antarctica go back nearly 800,000 years, and cores drilled in 2016 at the Allan Hills held ice up to 2.7 million years old (Wikipedia contributors, 2026). "
 "In blocks, the six topsoil blocks are about an hour of work and the 100 blocks of coinbase maturity about 16.7 hours, so the 'millions of years' of the book are meant as a picture and not as a measure, since the whole chain is only about 18.5 years old. "
 "It is the same picture as a stack of newspapers in a cellar: today's paper is on top and can be taken off, but nobody can slip an issue into the middle of last year's pile without the whole pile showing it.")

B["TwoChildrenOneParent"] = (
 "A block has one parent but may have several children, and when two miners find a block at almost the same time the chain forks for a while: two blocks that both commit to the same parent (Antonopoulos and Harding, 2023). "
 "On the test chain this was made to happen on purpose: two blocks with different hashes and the same previous-block field were both at height 511, and the node's getchaintips listed two tips, one active and one of status valid-fork with branch length 1 (Bitcoin Core, 2026). "
 "A fork is not an error, it is the normal result of two miners racing on a network where messages need time to travel. "
 "It is like two people arriving at a till at the same moment: for a second there are two candidates, and then one of them is served first.")

B["ForkResolvedByMoreWork"] = (
 "A fork is resolved when one branch becomes heavier: nodes switch to the branch with the most accumulated work, and the other branch is kept as a valid-fork that may come back if it is extended later (Antonopoulos and Harding, 2023). "
 "On the test chain a third block was built on the first child; the tip moved to height 512, the first child's branch became the active chain, and the second child stayed in the list as a valid-fork at height 511 with branch length 1, so nothing was deleted, only passed over (Bitcoin Core, 2026). "
 "The book calls the situation temporary and says that eventually only one child becomes part of the chain accepted by all full nodes. "
 "It is like a road with two lanes that merge: both cars were driving legally, one is waved on first, and the other follows at once behind it.")

B["ReorgProbabilityFalls"] = (
 "The book says that blocks near the tip may be revised, and that further down they are less and less likely to change until the probability becomes infinitesimal; Nakamoto's paper gives the numbers (Antonopoulos and Harding, 2023); (Nakamoto, 2008). "
 "For an attacker with 10 percent of the hash rate, the chance of ever catching up from 0, 1, 2, 6 and 10 blocks behind is 1.0, 0.2045873, 0.0509779, 0.0002428 and 0.0000012, and for 30 percent at 6 blocks it is 0.1321; the code of this chapter reproduced the paper's table from its Poisson formula to the printed digits. "
 "This is the mathematical reason for the habit of waiting six confirmations. "
 "It is like the chance of a runner who starts six laps behind to catch up with someone who runs almost as fast as he does: not zero, but small enough to bet against.")
