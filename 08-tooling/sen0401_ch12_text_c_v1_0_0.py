"""SEN0401 chapter 12 (Mining and Consensus): the teaching paragraphs of the leaves of subject 4 (target, difficulty, retargeting) and of the nonce space of subject 5. One paragraph per leaf, one line, full sentences.
Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
C = {}

C["HashBelowTarget"] = (
 "A block is valid proof of work if the number that is its header hash, read as a 256-bit integer, is not above the target written in its header, which means that the hash must start with many zero bits (Antonopoulos and Harding, 2023). "
 "Block 277,316 had a target that fits in 194 bits, so a winning hash needed at least 62 leading zero bits; its hash 0000000000000001b6b9a13b... has 63, and the book says 'more than 60' (Mempool Space, 2026). "
 "The check is one double SHA-256 and one comparison, as the saved header showed. "
 "It is like a high-jump bar set at a fixed height: the jumper is judged only by whether he cleared it, and the judge needs a second to see.")

C["DifficultyFromTarget"] = (
 "Difficulty is a more convenient name for the same thing: the ratio of the largest allowed target, the one with the bits 0x1d00ffff and difficulty 1, to the target of the block (Bitcoin Wiki, 2026). "
 "For block 277,316 with bits 1903a30c this gives 1,180,923,195, the same figure as mempool.space lists, and for block 840,000 it gives 86,388,558,925,171, about 73,000 times harder (Mempool Space, 2026); (Mempool Space, 2026). "
 "The book writes the target as a long hexadecimal number and the difficulty as its reciprocal in disguise (Antonopoulos and Harding, 2023). "
 "It is like the handicap in golf: the same course, but each year the par is made smaller and the number that says how much smaller is the difficulty.")

C["CompactBits"] = (
 "A target has 256 bits but the header has room for only 4 bytes, so it is stored in a compact form: one byte of exponent and three bytes of mantissa, with the target equal to the mantissa times 256 to the power of the exponent minus 3 (Antonopoulos and Harding, 2023). "
 "The code of Bitcoin Core turns a target into this form with a function named GetCompact (Bitcoin Core, 2026). "
 "Block 277,316 has bits 0x1903a30c, which is 0x03a30c times 256 to the power 22; converting back gave 0x1903a30c, the value 0x1d00ffff expanded to the difficulty-1 target, and a mantissa with its high bit set, 0x00800000, was shifted to 0x04008000 because that bit is a sign bit. "
 "It is like writing a big number in scientific notation, 3.2 x 10^22, to fit a small box on a form: three digits and the position of the point.")

C["TerahashMinerWait"] = (
 "The book works out how long a single machine would take: a miner doing 1 TH/s, one trillion hashes per second, would find a block for height 277,316 'once in 8,496 blocks or once every 59 days' (Antonopoulos and Harding, 2023). "
 "Recomputed, the expected number of hashes is the difficulty 1,180,923,195 times 2 to the 32, so at 10 to the 12 per second it takes 58.7 days, which is 8,453 blocks of ten minutes, about 0.5 percent fewer than the book's figure; 8,496 blocks of ten minutes are 59.0 days, so the number of blocks and the number of days of the book agree with each other and not with the difficulty (Mempool Space, 2026). "
 "It is a small slip, but a good habit for a reader: the figure can be recomputed with two lines. "
 "It is like a bus timetable that says 59 minutes when the clock on the route says 58.7: fine for a traveller, wrong for an engineer.")

C["HashrateFromDifficulty"] = (
 "Nobody measures the hash rate of the network directly; it is estimated from the difficulty, because difficulty times 2 to the 32 hashes is the expected work for a block and a block comes every 600 seconds (Bitcoin Wiki, 2026). "
 "The difficulty of the last retarget, 132,716,002,350,731, gives 9.5e20 hashes per second, 8 percent under the 1.029e21 that mempool.space reports from recent blocks and near the 1.003e21 of blockchain.com; the two services estimate over different windows (Mempool Space, 2026); (Blockchain Charts, 2026). "
 "The network is therefore about 121,738 times faster than the 8.45e15 that the difficulty of block 277,316 implied in 2013, when the book's example was chosen. "
 "It is like estimating the traffic of a city from the number of tickets sold: you do not count every car, you count what is needed to explain the numbers.")

C["RetargetFormulaOnRealEpoch"] = (
 "Every 2,016 blocks the network resets the target so that the next 2,016 blocks should take two weeks, 1,209,600 seconds: the new target is the old one multiplied by the time the last period took and divided by two weeks (Antonopoulos and Harding, 2023). "
 "The rule was applied to real headers: block 838,656 and block 840,671 are the first and the last of a period and 1,186,047 seconds apart; with the bits 17034219 of the last block the function gives 170331db, which is the value that block 840,672 really carries, so the code reproduces the network to the last digit (Mempool Space, 2026); (Bitcoin Core, 2026). "
 "That period was 1.02 times faster than planned, so the target fell by 2 percent and mining became 2 percent harder. "
 "It is like a thermostat that is set after each fortnight: if the room warmed up faster than planned, the heater is turned down a little.")

C["TwoThousandFifteenGaps"] = (
 "The retarget has a small famous flaw: it measures the time from the first to the last block of the period, which is 2,015 intervals and not 2,016, so the intended pace is a block every 599.7 seconds instead of every 600 (Bitcoin Core, 2026). "
 "The ratio 2016 divided by 2015 is 1.000496, or 0.05 percent faster than the aim, and the code takes the first block at height minus 2,015 and subtracts its time from that of the last block (Bitcoin Core, 2026). "
 "The book's listing of the code shows the same arithmetic without naming the effect (Antonopoulos and Harding, 2023). "
 "It is like a fence with 2,016 posts that has only 2,015 gaps between them: if you plan the length with the wrong count, the fence is a little off.")

C["ClampFactorFour"] = (
 "The measured time of a period is limited to between a quarter and four times the aim before it is used, so that the target can change by at most a factor of four at a retarget, in either direction (Antonopoulos and Harding, 2023). "
 "In the recomputation a period ten times too long gave a target exactly 4 times larger (bits 170d0864 from 17034219) and a period ten times too short gave 0.25 times (1700d086), and the two lines of pow.cpp that apply the limits were found in the source (Bitcoin Core, 2026). "
 "The limit protects against a wild estimate after a sudden loss of most of the hash rate, though it also means that recovery can take several periods. "
 "It is like a car with a speed limiter on the gas pedal: however hard you push, the speed changes only so fast.")

C["RegtestNeverRetargets"] = (
 "The regtest chain switches the difficulty adjustment off with a parameter, fPowNoRetargeting, which is true for regtest and false for mainnet in chainparams.cpp (Bitcoin Core, 2026). "
 "The test chain of this chapter was mined through heights 1, 2015, 2016, 2017 and 2100 and the bits stayed 207fffff throughout, so a real retarget by Bitcoin Core was not executed; the retarget function was instead checked against real mainnet headers. "
 "Release 29.0 also turned off the timewarp rule of BIP 94 on regtest (Bitcoin Core developers, 2025). "
 "It is like practising a free kick without a wall: the ball goes in, but the real difficulty has been switched off.")

C["Bip94Branch"] = (
 "The listing of the retarget code in the book is an older version, and the file pow.cpp of Bitcoin Core 31.1 has an extra branch, if (params.enforce_BIP94), which builds the new target from the bits of the first block of the period instead of the last, because the first block is not allowed to use the minimum-difficulty exception and so keeps the real difficulty, as a comment in the code explains (Bitcoin Core, 2026). "
 "The flag is true for testnet4 and false for mainnet, and the word enforce_BIP94 does not occur in the book (Antonopoulos and Harding, 2023). "
 "BIP 94, assigned on 2024-05-27, describes the rules, among them the 'Time Warp Attack Prevention' (Jahr, 2024). "
 "It is like the extra clause that a contract acquires after a dispute: the old text is still there, and the new clause applies only to one customer.")

C["RecentAdjustments"] = (
 "The retargets of the last two years show the controller at work: 52 changes between 2024-10-22 and 2026-10-03, the smallest a fall to 0.888 times the old difficulty and the largest a rise to 1.147 times, 20 of them downward (Mempool Space, 2026). "
 "None came near the limit of a factor of four, and over the two years the difficulty rose by a factor of 1.39 in all, so the hash rate grew by about the same. "
 "The book explains the mechanism but could not know these numbers (Antonopoulos and Harding, 2023). "
 "It is like the speedometer of a car on a motorway: it shifts a little up and down but stays near the speed limit.")

C["NextAdjustmentToday"] = (
 "On 2026-10-15 the tip of the main chain stood at height 971,561, and the next retarget was due at height 971,712, a multiple of 2,016, after 151 more blocks; mempool.space estimated the change as plus 6.44 percent, after a previous change of minus 3.09 percent (Mempool Space, 2026); (Mempool Space, 2026). "
 "The estimate rests on the blocks so far in the period, which have come on average every 564 seconds and not every 600, and it can still move until the last block. "
 "The rule it uses is the one the book describes (Antonopoulos and Harding, 2023). "
 "It is like a forecast made at the middle of the month for the electricity bill: it changes as the rest of the month is seen.")

C["NonceSpaceIsTiny"] = (
 "The nonce of the header is 4 bytes, so a miner can try 4,294,967,296 values before the header is used up and a new one is needed (Antonopoulos and Harding, 2023). "
 "The network now runs at about 1.029e21 hashes per second, which uses up 2 to the 32 values in 4.17 picoseconds and means that the network works through 2.4e11 whole nonce spaces every second (Mempool Space, 2026). "
 "That is why a single nonce cannot keep a machine busy and miners need more room in the header to vary. "
 "The book dates this problem to the arrival of ASICs, when hardware exceeded 4 GH/s and then 1 TH/s (Antonopoulos and Harding, 2023). "
 "It is like a car's trip counter with only four digits on a lorry that drives a million kilometres: the counter rolls over faster than anyone can read it.")

C["ExtraNonceSpace"] = (
 "The first solution was to use the coinbase script as extra room: eight bytes of extra nonce added to the 4-byte nonce give 2 to the 96 possible headers, a number the book writes as 8 followed by 28 zeros (Antonopoulos and Harding, 2023). "
 "Calculated exactly, it is 7.923e28 and has 29 digits, so the book's rounded form is right, and 2 to the 64 times 2 to the 32 equals 2 to the 96. "
 "Because the coinbase is the first leaf of the merkle tree, each new extra nonce means recomputing the left side of the tree up to the root, which the book calls more complicated for equipment and protocols than changing only the header (Antonopoulos and Harding, 2023). "
 "It is like a lock with a second dial added to the first: the combinations multiply instead of adding.")

C["VersionRolling"] = (
 "The solution of the machine makers is to roll 16 bits of the version field, the mask 0x1fffe000 of BIP 320, which gives 65,536 versions for each coinbase (BtcDrak, 2018). "
 "Together with the 2 to the 32 nonces this is 2 to the 48 hashes per header, so one machine can run at 281.5 TH/s if it finishes a header every second, the 281 TH/s of the book (Antonopoulos and Harding, 2023). "
 "On the test chain a block with the rolled version 0x2000e000 was accepted at height 3 (Bitcoin Core, 2026). "
 "Pool protocols carry the same idea: BIP 310 adds a 'version-rolling' extension to Stratum so that the machine may roll these bits without asking the pool (Palatinus et al., 2017). "
 "BIP 320 has the status Draft, although it is widely used, and BIP 323 was proposed as its replacement. "
 "It is like a combination lock with sixteen free switches on the side: the machine can flip them without changing the keys of the lock.")

C["AsicBoostCovert"] = (
 "ASICBoost is a technique for constructing the block header specially so that the hardware does less work per hash (Bitcoin Optech, 2026). "
 "The book tells that segwit unintentionally interfered with covert ASICBoost, so that miners who used it would lose their hidden advantage if segwit were activated, and that this conflict of interest became part of the dispute over activation in 2017 (Antonopoulos and Harding, 2023). "
 "The segwit commitment sits in the coinbase, where BIP 141 requires it (Lombrozo et al., 2015). "
 "The case is a good lesson that a technical rule can change the profit of a group of miners, and the miners then take a side. "
 "It is like a new traffic rule that happens to ban the shortcut that only some drivers knew: they will have views on the rule.")
