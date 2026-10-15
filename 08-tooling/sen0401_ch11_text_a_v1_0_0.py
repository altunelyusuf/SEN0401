"""SEN0401 chapter 11: the teaching paragraphs of the leaves of subjects 1 (structure of a block) and 2 (block identifiers). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chain are single-run values."""
__version__ = "1.0.0"
A = {}

A["BlockIsHeaderPlusTransactions"] = (
 "A block is a container: a small header of metadata, then a counter that says how many transactions follow, then the transactions themselves, which make up nearly all of the bytes (Antonopoulos and Harding, 2023). "
 "The genesis block shows the arithmetic exactly: 80 bytes of header, 1 byte for the counter and 204 bytes for its single coinbase transaction make 285 bytes, the size that mempool.space lists for block 0 (Mempool Space, 2026). "
 "On the private test chain run for this chapter, blocks holding 1, 2, 3 and 4 transactions measured 250, 472, 694 and 915 bytes, so each added transaction cost about 222 bytes, which is why a block grows almost in a straight line with its transaction count (Bitcoin Core, 2026). "
 "Think of a parcel: a shipping label of fixed size on the outside, a packing list that says how many items are inside, and then the items, which decide how heavy the parcel is.")

A["BlockSizeFieldIsFileStorage"] = (
 "The first table of the chapter starts with a 4-byte field called block size, but that field belongs to the way Bitcoin Core stores blocks on disk and not to the block as it travels between nodes or as consensus sees it (Antonopoulos and Harding, 2023). "
 "In the blk files each block is written as 4 magic bytes, then 4 bytes giving the size of the block, then the block, and since release 28.0 the whole file is scrambled with a random key kept in a file named xor.dat (Bitcoin Core developers, 2024). "
 "Reading the first bytes of the test chain's blk00000.dat gave nonsense until the key d462ed9f917fe79d was applied; then the file began fabfb5da, the magic of the test chain, followed by 1d010000, which is the little-endian number 285, the size of the genesis block, and the genesis block that followed equalled the one the node reported (Bitcoin Core, 2026). "
 "The chain data at height 0 occupied 293 bytes on disk, which is 285 plus the 8 bytes of magic and size. The release notes warn that older releases and external software cannot read such a directory, and the scrambling is like a diary in a private code: the owner reads it with the key, a stranger who opens the file sees noise.")

A["TransactionCounter"] = (
 "After the header comes a counter of transactions written as a compactSize integer, a number format that takes 1 byte for values up to 252, 3 bytes for 253 to 65,535 and 5 bytes beyond that (Bitcoin Wiki, 2026). "
 "The book says the counter takes 1 to 3 bytes, which is right because a block cannot hold more than 65,535 transactions: the smallest possible transaction weighs 4 x 60 = 240 weight units, so the limit of 4,000,000 allows at most 16,666 of them (Bitcoin Core, 2026); (Antonopoulos and Harding, 2023). "
 "Real blocks are far from that bound, block 840,000 had 3,050 transactions and so spent 3 bytes on its counter. "
 "A compactSize number is like the page-number system of a book: small numbers get a short mark, and only a very thick book needs the long form.")

A["GetblockOutputToday"] = (
 "The book prints the answer of getblock for the genesis block, and anyone who runs the command today sees a listing that is longer. Bitcoin Core 29.0 added the field target, the 256-bit number the block hash had to stay under, and 31.0 added an object coinbase_tx that carries the version, locktime, sequence, coinbase script and witness of the first transaction, so a program can read the coinbase without fetching the full transaction list (Bitcoin Core developers, 2025); (Bitcoin Core developers, 2026). "
 "On the test chain the genesis block listing contained exactly these two fields beyond the book's, and lacked only nextblockhash, because no second block existed yet (Bitcoin Core, 2026). "
 "None of this changes what a block is; it is the same record with two more labelled drawers (Antonopoulos and Harding, 2023). "
 "It is like a bank statement that gains two new lines after a software update: the old numbers are all still there and still add up.")

A["BlockReservedWeight"] = (
 "A miner's block template does not fill the consensus limit to the last unit, because room must be kept for the header, the transaction counter and the coinbase that the mining software adds later. "
 "Bitcoin Core reserves 8,000 weight units by default with the option -blockreservedweight, so the fullest template it builds is 4,000,000 - 8,000 = 3,992,000 weight units, a number that release 29.0 names when it explains a bug that had reserved the 4,000 units twice (Bitcoin Core developers, 2025); (Bitcoin Core developers, 2026). "
 "Block 840,000 weighed 3,993,281 weight units, more than that, so it was built by other software with a smaller reserve (Mempool Space, 2026). "
 "The book speaks only of the limit of about 4,000,000 bytes (Antonopoulos and Harding, 2023). "
 "It is like a lift that is rated for 1,000 kg but whose operator leaves room for the attendant: the rating is the law, the sign on the door is the habit.")

A["HeaderIs80Bytes"] = (
 "Every Bitcoin block header is exactly 80 bytes: 4 for the version, 32 for the previous block hash, 32 for the merkle root, 4 each for the time, the target and the nonce (Antonopoulos and Harding, 2023). "
 "The genesis header, the header of block 277,315 and a header of the test chain all parse to 80 bytes in the code of this chapter, and because a serialized block may be at most 4,000,000 bytes, a full block is 4,000,000 / 80 = 50,000 times the size of its header, the figure the book gives as almost 50,000 (Bitcoin Core, 2026). "
 "The fixed size is what makes light clients possible: a phone can keep all 971,538 headers of today's chain in about 78 megabytes, since 971,538 x 80 bytes is 77.7 million bytes, while the whole chain is some 775,000 megabytes (Blockchain Charts, 2026). "
 "A header is like the spine label of a book on a library shelf: always the same size, enough to find the book and check that it is the right one, while the pages stay on the shelf.")

A["BlockWeightLimit"] = (
 "The book says that the transactions of a block can total about 4,000,000 bytes, but the rule that consensus enforces is a limit of 4,000,000 weight units, in which every byte of a transaction counts four times except the witness data, which counts once (Antonopoulos and Harding, 2023); (Bitcoin Core, 2026). "
 "The test chain shows the formula: its block 120 had a size of 249 bytes, a stripped size of 213 bytes (without witness data) and a weight of 888, which is 3 x 213 + 249. "
 "Block 840,000 on the main chain held 3,050 transactions with a weight of 3,993,281, which is 99.83 percent of the limit, while its size was only 2,325,617 bytes, about 762 bytes per transaction, so a block full by weight is smaller than 4,000,000 bytes (Mempool Space, 2026). "
 "It is like a lorry with a weight limit and not a size limit: a load of feathers and a load of bricks fill the same lorry in very different volumes.")

A["VersionBitsField"] = (
 "The version field started as a plain version number, 1 for the genesis block and 2 for block 277,315, but it is now a row of 32 flags (Antonopoulos and Harding, 2023). "
 "BIP 9 lets miners signal readiness for a soft fork by setting one bit each, and requires the top three bits to be 001 so that the number stays at least 0x20000000, which is what every block of the test chain carries (Wuille et al., 2015). "
 "The draft BIP 320 goes further and reserves sixteen bits, from bit 13 to bit 28 (the mask 0x1fffe000), for miners to use as extra nonce space; block 840,000 carries 0x2a5fe000, which has bits inside that mask set, and the BIP is still a Draft with a proposed replacement, BIP 323 (BtcDrak, 2018); (Mempool Space, 2026). "
 "The version field is like the dashboard of a car: it began as one dial and now has a row of small warning lamps, some for the manufacturer and some left free for the driver.")

A["FieldOrderAndEndianness"] = (
 "The six fields of the header sit in a fixed order in the 80 bytes: version, previous block hash, merkle root, time, bits, nonce (Bitcoin Project, 2026). "
 "Integers are stored least significant byte first, so the version 2 appears as 02000000, and the two hashes are stored in the reverse of the order in which people display them, which is why a hash that begins with many zeros when printed ends with them in the raw header. "
 "Rebuilding block 277,315 from its decoded fields in exactly this order gave back the 80 bytes that mempool.space returns, with the bits 1903a30c at the end of the target bytes and the parent hash ending a1632249 in display order (Mempool Space, 2026); (Antonopoulos and Harding, 2023). "
 "Little-endian is like writing a date as day, month, year when you are used to the opposite: nothing is wrong, but you must know which convention a file uses before you read it.")

A["TimestampField"] = (
 "The timestamp is a 4-byte count of seconds since 1 January 1970, the Unix time, and the book calls it the approximate creation time (Antonopoulos and Harding, 2023). "
 "The genesis block says 1231006505, which is 2009-01-03 18:15:05 UTC, block 840,000 says 2024-04-20 00:09:27 UTC, and a node refuses a block whose time is more than 2 x 60 x 60 = 7,200 seconds ahead of its own clock (Bitcoin Core, 2026). "
 "Because the counter is 4 bytes, it can only run until 2106-02-07 06:28:15 UTC, the overflow date that Unix time discussions mention and that Optech lists among the consequences of the timewarp fix of BIP 54 (Wikipedia contributors, 2026); (Bitcoin Optech, 2026). "
 "A block's timestamp is like the date stamp on a letter: roughly right is good enough, but the post office will not accept one dated far in the future.")

A["MedianTimePast"] = (
 "A block's timestamp must be greater than the median of the timestamps of the previous 11 blocks, and BIP 113 uses this median time past as the clock for time locks, because it cannot be moved far by a single miner (Kerin and Friedenbach, 2015). "
 "Bitcoin Core keeps nMedianTimeSpan = 11 and computes it in GetMedianTimePast (Bitcoin Core, 2026). "
 "On the test chain the median of blocks 111 to 121 was 1792052132, equal to the value that the node itself reported for block 121, and on the real chain block 277,315 has a timestamp 1,651 seconds later than its median time past, which shows that the median can run behind the wall clock by about 27 minutes (Mempool Space, 2026); (Bitcoin Wiki, 2026). "
 "It is like judging the time by the middle value of eleven clocks in a room: one clock that runs wrong cannot change the middle.")

A["TargetCompactEncoding"] = (
 "The target is the number the block hash must not exceed, and the header stores it in 4 bytes as a floating-point style 'compact' form: one byte of exponent and three of mantissa, so that target = mantissa x 256^(exponent - 3) (Bitcoin Wiki, 2026). "
 "The value 0x1d00ffff, that of the genesis block and the lowest difficulty ever used on mainnet, expands to 0xffff followed by 26 zero bytes and equals a difficulty of 1; the 0x1903a30c of block 277,315 gives a difficulty of 1,180,923,195.258, the number in the book's listing; and the test chain's 0x207fffff expands to the target 7fffff followed by zeros, which the node itself printed (Antonopoulos and Harding, 2023); (Bitcoin Core, 2026). "
 "The work of one block at difficulty 1 is 0x100010001, the chain work printed for the genesis block. "
 "The compact form is like scientific notation on a pocket calculator: it keeps the first few digits and the size of the number, and throws away the digits nobody needs.")

A["NonceAndExtraNonce"] = (
 "The nonce is the 4-byte number that miners change again and again to get a different hash, and it is here that the proof of work happens, as the next chapter of the book explains (Antonopoulos and Harding, 2023). "
 "But 4 bytes give only 2^32 = 4,294,967,296 tries, and at the difficulty of block 277,315 a block took about 5 x 10^18 hashes, 1,180,941,215 times as many, so a miner must change something else when the nonce runs out: the extra nonce in the coinbase script, spare bits of the version field, or the timestamp, as the mining chapter says (Antonopoulos and Harding, 2023). "
 "Block 277,315 itself was found with nonce 4215469401, near the upper end, while the blocks of the private test chain, at the lowest difficulty, needed only nonce 1 (Mempool Space, 2026). "
 "It is like a combination lock with only four digits: when the digits are used up you must reset something else in the lock to go on trying.")

A["BlockHashIsDoubleSha256"] = (
 "The block hash is the SHA-256 of the SHA-256 of the 80-byte header, and nothing else is hashed: the transactions are covered only through the merkle root inside the header (Bitcoin Wiki, 2026). "
 "Hashing the genesis header twice gives 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f once the bytes are reversed for display, a single SHA-256 gives something unrelated beginning 6dd6c5716cc8e243, and the header of block 277,315 hashes to the id that mempool.space lists (Mempool Space, 2026). "
 "In the source the hash is the one line return (HashWriter{} << *this).GetHash(); of CBlockHeader::GetHash (Bitcoin Core, 2026). "
 "A cryptographic hash is a fingerprint: change one bit of the finger and the print changes completely, which is why the header can stand for the whole block (Wikipedia contributors, 2026). "
 "It is like the seal on a bottle of medicine, small but impossible to copy onto a changed bottle.")

A["HashNotStoredInBlock"] = (
 "The block hash is not a field of the block: each node computes it when the block arrives, and may then keep it in an index for fast lookup (Antonopoulos and Harding, 2023). "
 "The 285 bytes of the test chain's genesis block contain neither its hash 0f9188f1... nor the reverse of that hash, but the header of the next block does contain the reversed hash as its previous-block field, so the name of a block is written down by its child and not by itself (Bitcoin Core, 2026). "
 "The reason is simple logic: a block cannot contain a hash of itself, because the hash would have to be known before the content that it is the hash of. "
 "It is like a person who cannot sign a letter with a name that has not yet been given: it is the next page of the register that records the name.")

A["HashLeadingZeros"] = (
 "Block hashes famously begin with many zeros, but the zeros are not stored or demanded as such: they are the visible result of the rule that the hash, read as a number, must not exceed the target (Bitcoin Wiki, 2026). "
 "The genesis hash begins with 10 zero hexadecimal digits, block 277,315 with 15 and block 840,000 with 19, and each of the first two was checked in the code to be no larger than the target in its own header (Mempool Space, 2026); (Bitcoin Core, 2026). "
 "On the test chain, whose target 7fff... is the easiest possible, the genesis hash 0f9188f1... has a single zero. "
 "More zeros mean a smaller target and therefore more work, as when a lottery draws only the numbers below a limit and the limit is lowered: the tickets with the winning numbers become rarer. "
 "The book does not discuss the zeros here but in the mining chapter (Antonopoulos and Harding, 2023).")

A["HeightIsNotUnique"] = (
 "A block has two names: its hash, which identifies it uniquely, and its height, the count of blocks between it and the genesis block, which does not (Antonopoulos and Harding, 2023). "
 "The book says in a tip box that a height can be shared by competing blocks, and the test chain showed it: two different children of the same parent were both at height 511, with different hashes and the same previous-block field (Bitcoin Core, 2026). "
 "This is why software that needs certainty uses the hash, and treats the height as a position that can change owner when the chain reorganizes. "
 "A hash is like a passport number and a height like a seat number: two people may have held the same seat on different days, but nobody else has your passport number.")

A["HeightFromGenesis"] = (
 "The height of a block is its distance from the genesis block, which sits at height 0, so a chain with the tip at height h has h + 1 blocks (Antonopoulos and Harding, 2023). "
 "On 2026-10-15 the tip of the main chain was at height 971,537, which means 971,538 blocks and, at one block in ten minutes, about 18.5 years of history, whereas the book says that height 800,000 was reached in mid 2023 (Mempool Space, 2026). "
 "Block 840,000, the first with the lower reward of 3.125 coins, has the timestamp 2024-04-20 00:09:27 UTC (Mempool Space, 2026). "
 "A fresh node with no data reported height 0 and 0 headers, since it knows only the genesis block (Bitcoin Core, 2026). "
 "Height is like the kilometre posts along a motorway: they tell you how far you have come, and they are numbered from the same starting point for everybody.")

A["Bip34HeightInCoinbase"] = (
 "In the early chain a block's height was not stored in the block; BIP 34 changed this by requiring the height as the first item of the coinbase script, in the 'minimally encoded serialized CScript' form, and its stated purpose is to make every coinbase transaction unique (Andresen, 2012); (Antonopoulos and Harding, 2023). "
 "The coinbases of the test chain show how the encoding works: height 17 is 011100 (one byte, the number 0x11), 128 is 02800000 (two bytes, 0x0080, because a single 0x80 would read as negative) and 256 is 02000100, while the small heights 1 to 16 are written as the opcodes OP_1 to OP_16, so height 1 starts 5100 (Bitcoin Core, 2026). "
 "All eight recorded prefixes decoded back to their heights in the code of this chapter. The older rule BIP 30, assigned to Pieter Wuille on 2012-02-22, goes at the same problem from another side: a block may not contain a transaction whose identifier matches that of an earlier, not-fully-spent transaction, apart from two historic blocks at heights 91842 and 91880 (Wuille, 2012). "
 "It is like the number on a cheque: it does not make the cheque valuable, it makes it different from all the others in the book.")

A["CoinbaseMaturity100"] = (
 "The reward and fees that a miner earns in the coinbase transaction cannot be spent at once but only after the block is 100 blocks deep, because a short reorganization would otherwise destroy coins that had already been spent onward (Antonopoulos and Harding, 2023). "
 "The constant is COINBASE_MATURITY = 100 in consensus.h; on the test chain a transaction spending a coinbase at depth 99 was rejected with bad-txns-premature-spend-of-coinbase, the same transaction at depth 100 was accepted, and the node's wallet showed the last 100 blocks of the 500 as immature (Bitcoin Core, 2026). "
 "The rule applies to every chain, test chains included, so a developer meets it on regtest first. "
 "It is like the cooling period of a cheque paid in from abroad: the bank shows the amount at once but lets you draw on it only after the cheque has really cleared.")
