"""SEN0401 chapter 12 (Mining and Consensus): the teaching paragraphs of the leaves of subject 3 (building the candidate block) and of the lottery of subject 4. One paragraph per leaf, one line, full sentences.
Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
B = {}

B["TemplateFields"] = (
 "A miner does not build a block from nothing: the node hands over a template, a list of everything the miner needs except the work, through the RPC getblocktemplate that BIP 22 defines (Dashjr, 2012). "
 "The template of the Bitcoin Core 31.1 test chain at height 1 carried the hash of the parent, the height, the bits and the target, the current time and the earliest allowed time, the coinbasevalue of 5,000,000,000 satoshis, the limits weightlimit 4,000,000 and sigoplimit 80,000, the nonce range 00000000ffffffff, the active rules csv, segwit and taproot, and the default witness commitment (Bitcoin Core, 2026). "
 "The book describes the same steps as building a candidate block (Antonopoulos and Harding, 2023). "
 "It is like a work order from a workshop: the foreman gives you the drawings, the material and the deadline, and you only add the labour.")

B["FeeRateOrdering"] = (
 "A block has room for only 4,000,000 weight units, so a node fills the template with the transactions that pay the most for the room they take, measured as the fee rate in satoshis per virtual byte, as the chapter on fees explains (Antonopoulos and Harding, 2023). "
 "On the test chain four transactions paying 200, 50, 10 and 2 satoshis per virtual byte were placed in the mempool in the reverse order, and the node put them in the block in the order 200, 50, 10, 2 (Bitcoin Core, 2026). "
 "The block assembler of release 31.1 adds the chunks of the mempool to the template in the order of their fee rate, and tests each chunk against the weight and signature-operation limits of the block (Bitcoin Core, 2026). "
 "It is like the last seats on an overbooked flight: the airline sells them first to the passengers who pay the most per kilo of luggage.")

B["CoinbaseInputIsNull"] = (
 "The first transaction of every block, the coinbase, creates coins instead of moving them, so its single input spends nothing: the previous transaction hash is 32 zero bytes and the output index is ffffffff (Antonopoulos and Harding, 2023). "
 "The coinbase of block 1 of the test chain, in the getblock output of Bitcoin Core 31.1, had exactly one input, a script of 5100, which is the height 1 followed by OP_0, and the sequence 4294967294 (Bitcoin Core, 2026). "
 "That script field is where the miner may write free data, and it must be 2 to 100 bytes long. "
 "It is like a bank note printed by the mint: it has no previous owner, only a serial number that says when it was printed.")

B["Bip34HeightPush"] = (
 "A coinbase has no input to make it unique, so two blocks could in theory have coinbases with the same identifier; BIP 34 closes the gap by requiring the block height as the first item in the coinbase script, written as a 'minimally encoded serialized CScript' number (Andresen, 2012). "
 "On the test chain the coinbase at height 2204 began 029c08, a push of two bytes holding 0x089c, which is 2204 in little-endian order, and the lines of chainparams.cpp fix the mainnet height at which the rule applies as 227,931 (Bitcoin Core, 2026); (Bitcoin Core, 2026). "
 "The book lists the field as 'arbitrary data used for extra nonce and mining tags' and says that in version 2 blocks it must begin with the block height (Antonopoulos and Harding, 2023). "
 "It is like numbering every cheque in a cheque book: even if the amount is the same, no two cheques have the same number.")

B["CoreCoinbaseFieldsToday"] = (
 "Bitcoin Core 31.1 fills in three details of the coinbase that the book does not mention: nLockTime is the height minus 1, nSequence is 0xfffffffe, and the script ends with OP_0 (Bitcoin Core, 2026). "
 "The test coinbase at height 2204 had locktime 2203 and sequence 4294967294, and the coinbase of block 1 ended with the byte 00; the reason, given in BIP 54, is that a locktime tied to the height makes every new coinbase differ from the early violations of BIP 34, so that no coinbase can repeat a previous one (Poinsot and Corallo, 2025). "
 "The book's table of the coinbase lists only the input fields and the free data (Antonopoulos and Harding, 2023). "
 "It is like the date stamped on a receipt by a modern till, a detail that an old manual describing receipts does not show.")

B["WitnessCommitment"] = (
 "Segregated witness moved signatures out of the transaction identifier, so the block needed a new place to commit to them, and BIP 141 puts a hash in an output of the coinbase whose script begins 6a24aa21a9ed (Lombrozo et al., 2015). "
 "The 32 bytes that follow are the double SHA-256 of the witness merkle root and a 32-byte reserved value of zeros; the test chain's template gave the script, and an independent computation from the five witness transaction identifiers, with the coinbase counted as 32 zero bytes, gave the same commitment as the block (Bitcoin Core, 2026). "
 "The book describes the merkle tree of witness identifiers and the 32 zero bytes standing for the coinbase (Antonopoulos and Harding, 2023). "
 "It is like a sealed envelope stapled to the cover of a report: the pages inside can be checked against the seal, and the seal itself is listed on the cover.")

B["CoinbaseDataAndTags"] = (
 "The free data of the coinbase script is where pools sign their blocks: block 840,000 contains /ViaBTC/ and 'Mined by buzz120', block 709,632 contains /F2Pool/ and block 277,316 contains /P2SH/, and the scripts have 96, 100 and 15 bytes, all within the limit of 2 to 100 bytes (Mempool Space, 2026); (Mempool Space, 2026). "
 "The limit is enforced: a test block with a one-byte script and one with 101 bytes were both refused with bad-cb-length (Bitcoin Core, 2026). "
 "The book says that miners use this space for extra nonce values and strings identifying the mining pool (Antonopoulos and Harding, 2023). "
 "That is how the statistics of pools in this chapter can be made at all, by reading the tags. "
 "It is like the stamp of a printer in the corner of a poster: nobody requires it, but it tells you who made it.")

B["ExtraNonceChangesRoot"] = (
 "The coinbase is the first leaf of the merkle tree, so any change to its script changes its identifier, then every hash above it up to the merkle root in the header, and so the hash of the whole header (Antonopoulos and Harding, 2023). "
 "On the test chain two blocks that differed only in an extra nonce in the coinbase script and had the same header nonce gave different coinbase identifiers, different merkle roots and different block hashes (Bitcoin Core, 2026). "
 "This is the extra-nonce trick: when the 4-byte nonce runs out, the miner changes the extra nonce and starts over on a completely different header. "
 "It is like changing one word in the first line of a letter that is sealed with a wax stamp built from all lines: the stamp for the whole letter is new.")

B["HeaderOfBlock277316"] = (
 "The book builds its mining example on block 277,316 and gives its target, 0x0000000000000003A30C followed by zeros (Antonopoulos and Harding, 2023); the 80-byte header of that block can be taken apart: version 2, the hash of the previous block, the merkle root c91c008c..., the time 1388185914, the bits 1903a30c and the nonce 924591752. "
 "Parsed from the saved copy, the time is 2013-12-27 23:11:54 UTC, the merkle root equals the one listed by mempool.space, the double SHA-256 of the 80 bytes is the block hash 0000000000000001b6b9a13b095e96db41c4a928b97ef2d944a9b31b2cc7bdc4, and that hash is below the target of the bits (Mempool Space, 2026); (Mempool Space, 2026). "
 "Anyone with the 80 bytes can repeat the check in a few lines. "
 "It is like checking a lottery ticket against the published winning numbers: you need only the ticket and the list.")

B["VersionHistory"] = (
 "The first field of the header was meant as a version number but became a bulletin board: block 277,316 has the version 2 of BIP 34, block 709,632 has 0x20200004, and block 840,000 has 0x2a5fe000 (Mempool Space, 2026); (Mempool Space, 2026). "
 "BIP 9 requires the top three bits to be 001 for blocks that signal for a soft fork, so every version from 0x20000000 on follows its pattern, and bit 2 of block 709,632 is the signal for taproot (Wuille et al., 2015); (Wuille et al., 2020). "
 "In block 840,000 the lower bits 0x0a5fe000 are no signal but data that mining hardware rolls, as BIP 320 allows (BtcDrak, 2018). "
 "The book says that the use of the field has changed over time (Antonopoulos and Harding, 2023). "
 "It is like a form whose 'title' box has been used for years as a free note field: the old meaning is still printed, the actual meaning is whatever the writers agree on.")

B["MedianTimePast"] = (
 "The timestamp in a header is written by the miner and cannot be proven, so the rules bound it: a block must be later than the median of the previous 11 blocks, a value called the median time past, and BIP 113 uses the same median for lock times (Kerin and Friedenbach, 2015). "
 "The test chain refused a block whose time was equal to the median with the reason time-too-old, and Bitcoin Core's chain code defines the median by taking the middle of the last 11 timestamps (Bitcoin Core, 2026). "
 "For block 277,316 the median time past was 2013-12-27 22:34:35 UTC, and the block's own time was 2,239 seconds later; the book states the rule as 'no node will accept a block with a time less than or equal to the median time of the last 11 blocks' (Mempool Space, 2026); (Antonopoulos and Harding, 2023). "
 "It is like a witness who is believed if his clock is no earlier than what most of the previous eleven witnesses said: one liar cannot pull the median.")

B["TwoHourRule"] = (
 "The other bound on a timestamp is to the future: a node does not accept a block more than two hours ahead of its own clock, which Bitcoin Core writes as MAX_FUTURE_BLOCK_TIME = 2 * 60 * 60 seconds, 7,200 (Bitcoin Core, 2026). "
 "A test block whose time was two hours and a second ahead was refused with time-too-new (Bitcoin Core, 2026). "
 "The two bounds together keep the time in a window, which matters because the time sets the difficulty; the book gives the reason that a miner could otherwise lower difficulty by lying about the time (Antonopoulos and Harding, 2023). "
 "Optech's topic on the time warp attack explains what happens when these bounds are bent: the median time past then increases much more slowly than normal (Bitcoin Optech, 2026). "
 "It is like a rule that an exam may not be started earlier than the invigilator's clock allows, nor claimed to have started more than two hours late.")

B["HelloWorldNonce"] = (
 "The book explains proof of work with a toy: add a counter, the nonce, to the phrase 'Hello, world!' and hash until the result starts with a zero (Antonopoulos and Harding, 2023). "
 "The first counter that works is 32, whose hash begins 09cb91f8, exactly as the book prints; two zeros first appear at 228 and three zeros at 3,460, each roughly 16 times harder. "
 "The book's prose writes the phrase 'Hello, World! 32' with a capital W, which gives a different hash (6bbe6a3d), while its shell example uses a lowercase w: a typing slip, shown by the recomputation. "
 "The idea is older than Bitcoin, from Back's Hashcash and the pricing function of Dwork and Naor (Back, 2002); (Dwork and Naor, 1992). "
 "It is like asking a friend to spin a roulette wheel until a zero comes up: a quick spin for a green zero is luck, and the number of spins is the proof of effort.")

B["DiceAnalogy"] = (
 "The book compares the hunt for a hash to a game with two dice, in which the players throw until someone gets a throw less than a target, and a lower target makes winning harder (Antonopoulos and Harding, 2023). "
 "The numbers can be counted: of the 36 possible throws of two dice, 3 are at most 3 (8.33%), 6 are at most 4 and 26 are at most 8, so the odds fall as the target falls. "
 "A hash does the same with a number of 256 bits instead of 36 outcomes: the target is the threshold, and the proportion of hashes that win is the target divided by 2 to the 256 (Bitcoin Wiki, 2026). "
 "It is like a fairground game where the prize is on a shelf that gets higher each week: the throw is the same, the chance is smaller.")

B["ProofIsCheapToCheck"] = (
 "Proof of work is expensive to produce and cheap to check, the property that makes it useful (Bitcoin Wiki, 2026). "
 "On the Bitcoin Core 31.1 test chain a search for a hash below the target with bits 1e0fffff took 1,031,915 attempts, near the expected 1,048,577, and a search at 1f00ffff took 72,470 against 65,537 expected, while the regtest target needed one; each winning hash was confirmed by a single comparison (Bitcoin Core, 2026). "
 "The first scheme of this kind to price a resource by computation was proposed by Dwork and Naor, and Back's Hashcash used hash prefixes for the same purpose before Bitcoin; Nakamoto's paper cites Hashcash (Dwork and Naor, 1992); (Back, 2002); (Nakamoto, 2008). "
 "It is like a jigsaw puzzle: finding the solution takes an evening, but a guest sees at a glance that it is finished.")
