"""SEN0401 chapter 12 (Mining and Consensus): the teaching paragraphs of the leaves of subjects 1 (creation of money) and 2 (decentralized consensus). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
A = {}

A["HalvingEvery210000"] = (
 "The reward that a miner may claim in the first transaction of a block, the subsidy, starts at 50 coins and is cut in half every 210,000 blocks, which the book describes as about every four years (Antonopoulos and Harding, 2023). "
 "In the code it is one line, the subsidy is shifted right by the number of halvings, and the interval is a constant of the chain parameters (Bitcoin Core, 2026); (Bitcoin Core, 2026). "
 "Real blocks show the schedule: block 210,000 was mined on 2012-11-28 and pays 25 coins, block 420,000 on 2016-07-09 pays 12.5, block 630,000 on 2020-05-11 pays 6.25 and block 840,000 on 2024-04-20 pays 3.125, and the block before each one pays exactly twice as much (Mempool Space, 2026). "
 "It is like a fruit tree that bears half as much every four years on a fixed timetable: nobody votes on it, the calendar of blocks decides.")

A["TotalSupplyBelow21Million"] = (
 "Because the subsidy is an integer number of satoshis that is halved by a shift, it reaches 1 satoshi in the thirty-third period and zero after that, so the total can be added up exactly (Bitcoin Core, 2026). "
 "The sum of all rewards is 2,099,999,997,690,000 satoshis, which is 2,310,000 satoshis, or 0.0231 coins, less than the round figure of 21 million coins; the last block that pays anything is block 6,929,999, and the book places the end of issuance in about the year 2140 (Antonopoulos and Harding, 2023). "
 "The small gap is rounding, since each halving drops the odd satoshi, and the Bitcoin Wiki states the same fixed supply as a necessary condition for a meaningful currency (Bitcoin Wiki, 2026). "
 "It is like a savings jar into which a smaller and smaller number of coins is dropped each year until the last coin is a single cent: the jar never quite reaches the round figure on the label.")

A["BookScriptFloatErratum"] = (
 "The book prints a short script to add up all the rewards and shows the answer 2099999997690000 (Antonopoulos and Harding, 2023). "
 "The script that ships with the book divides the reward with current_reward /= 2 (Antonopoulos and Harding, 2023); in Python 3 the slash is a float division, so the reward never reaches zero by halving to 1 satoshi and then 0, but goes on through fractions for 1,107 steps until the float underflows, and the script as printed gives 2100000000000000.0 and not the number of the book. "
 "With integer division, as the Bitcoin Core code does, the sum is again 2,099,999,997,690,000, which this chapter recomputed from both versions. "
 "It is like a baker who rounds every half loaf down to a whole loaf: with a calculator that keeps the half loaves forever you get a slightly different, and wrong, bill.")

A["RegtestHalvesEvery150"] = (
 "A developer cannot wait four years to watch a halving, so the regtest chain halves every 150 blocks, a constant in the chain parameters (Bitcoin Core, 2026). "
 "On the Bitcoin Core 31.1 test chain the subsidy was 50 coins at heights 1 and 149, 25 at 150 and 299, 12.5 at 300 and 449 and 6.25 at 450, and at height 2,000 it had fallen to 610,351 satoshis, the value that the same shift rule gives (Bitcoin Core, 2026). "
 "The book relies on this interval when it mines 500 blocks on regtest, and the test chain of this chapter reached height 2,101 within seconds because no real work is needed (Antonopoulos and Harding, 2023). "
 "It is like a flight simulator with the clock at fast forward: the controls are the real ones, only the hours are shortened.")

A["RewardIsSubsidyPlusFees"] = (
 "The first transaction of a block, the coinbase, may create at most the subsidy plus the fees of all the other transactions of the block, a rule that the book explains with the miner who 'keeps the change' (Antonopoulos and Harding, 2023). "
 "A block template of Bitcoin Core 31.1 on the test chain stated the sum in its coinbasevalue: 345,369 satoshis, made of 305,175 of subsidy and 40,194 of fees from four transactions (Bitcoin Core, 2026). "
 "The same sum holds on the real chain: block 277,316, the book's example, had a reward of 2,509,094,928 satoshis, 25 coins plus 9,094,928 satoshis of fees (Mempool Space, 2026). "
 "It is like the till at the end of the day: the new money printed for the shift plus the tips left on the tables is the most the waiter can take home.")

A["FeesOfBlock840000"] = (
 "The book says that fees are usually a small percentage of a miner's income, with the vast majority coming from the new coins (Antonopoulos and Harding, 2023). "
 "Block 840,000, the first block to pay only 3.125 coins, which ViaBTC mined on 2024-04-20, held 3,050 transactions with fees of 3,762,561,499 satoshis, 37.6 coins, which is 12.04 times the subsidy of 312,500,000 satoshis (Mempool Space, 2026). "
 "That block was an exception, and the book's claim held for most blocks of its time, but it shows that the claim is not a law and that the share of fees can change from one block to the next, which fits the book's remark that fees will matter more as the reward decreases. "
 "It is like a restaurant where the tips on one holiday evening were twelve times the wage: unusual, but proof that the tips can matter.")

A["MinerMayClaimLess"] = (
 "A rule that only caps the reward lets a miner take less than the cap, and the book notes that a miner may intentionally mine a block with less than the full reward, which lowers the total ever issued (Antonopoulos and Harding, 2023). "
 "On the test chain a block whose coinbase took 345,368 satoshis, one less than the 345,369 allowed, was accepted by the node; the satoshi that was not claimed never comes into existence (Bitcoin Core, 2026). "
 "Validation only compares the sum of the coinbase outputs with the limit, which the source of validation.cpp shows as a check for 'greater than' (Bitcoin Core, 2026). "
 "It is like a ceiling price on a market stall: the seller may sell below it, and nothing makes the stall owner charge the full amount.")

A["GreedyCoinbaseRejected"] = (
 "The cap is enforced by every node, not by trust: a coinbase that takes one satoshi more than subsidy plus fees makes the whole block invalid (Antonopoulos and Harding, 2023). "
 "On the test chain the node answered bad-cb-amount to a block that claimed 345,370 satoshis where 345,369 were allowed, and again to a hand-built block one satoshi above its limit, and the string bad-cb-amount appears in the source of validation.cpp (Bitcoin Core, 2026); (Bitcoin Core, 2026). "
 "The miner loses all the work spent on the block, since honest nodes ignore it, so cheating costs far more than the satoshi gained. "
 "It is like a cashier whose drawer is counted by every other cashier before the shift is accepted: one extra coin and the whole count is thrown out.")

A["TransactionChecklist"] = (
 "Before a miner puts a transaction in a block, and before any node relays it, the node applies a fixed list of checks to it, which the book lists as the first part of independent verification (Antonopoulos and Harding, 2023). "
 "On the Bitcoin Core 31.1 test chain thirteen cases were run through testmempoolaccept: transactions with no outputs, a negative output, an output over 21 million coins, a total over 21 million coins, a repeated input, an input that does not exist, outputs larger than the inputs, a locktime in the future and a wrong signature were each refused with their own named reason, such as bad-txns-vout-empty or bad-txns-in-belowout, a transaction with no inputs could not be decoded at all, and a coinbase of depth 100 was allowed (Bitcoin Core, 2026). "
 "The names come from the rejection reasons in the source (Bitcoin Core, 2026); (Bitcoin Core, 2026). "
 "It is like the checks at an airport: ticket, passport, bag, each with its own reason for turning you back.")

A["BlockChecklist"] = (
 "The same strictness is applied to a whole block, with a longer list of reasons, and a block that fails any one of them is thrown away by every node (Antonopoulos and Harding, 2023). "
 "For this chapter fourteen blocks were assembled byte by byte, each broken in one way, and submitted to a Bitcoin Core 31.1 node: a wrong merkle root (bad-txnmrklroot), no proof of work (high-hash), a time equal to the median (time-too-old), a time two hours and a second ahead (time-too-new), a reward one satoshi too high (bad-cb-amount), no height in the coinbase (bad-cb-height), a version of 1 (bad-version), wrong difficulty bits (bad-diffbits), coinbase scripts of 1 and 101 bytes (bad-cb-length), a second coinbase (bad-cb-multiple), a missing coinbase (bad-cb-missing) and a block over the weight limit (bad-blk-length), while the correct block was accepted (Bitcoin Core, 2026). "
 "The reasons are defined in the validation source of the node (Bitcoin Core, 2026). "
 "It is like a quality inspector with a clipboard of fourteen boxes: the product ships only when every box is ticked.")

A["CoinbaseMaturity"] = (
 "A coinbase output cannot be spent until 100 blocks have been built on top of its block, a rule that the book states when it describes the first transaction of a block (Antonopoulos and Harding, 2023). "
 "The constant COINBASE_MATURITY is 100 in the consensus code (Bitcoin Core, 2026), and on the test chain a transaction spending a coinbase was refused with bad-txns-premature-spend-of-coinbase at depth 1 and at depth 99, and allowed at depth 100 (Bitcoin Core, 2026). "
 "The delay protects everyone downstream: if the block that created the coins is replaced in a reorganization, the coins disappear with it, and nobody has yet received them. "
 "It is like a bank that holds a cheque for ten days before letting you draw on it, in case the cheque bounces.")

A["MostWorkNotLongest"] = (
 "When two valid chains compete, a node follows the one with the most cumulative proof of work, which the book defines as the best chain, rather than the one with the most blocks (Antonopoulos and Harding, 2023). "
 "In the test the winning tip had the chainwork 208 against 206 for the chain it replaced; and when two blocks of equal work arrived at height 102, the node kept the first it had seen as its tip and marked the other valid-headers until more work arrived (Bitcoin Core, 2026). "
 "On regtest every block adds 2 units of work, so 208 is the work of the 104 blocks from the genesis block to height 103, and on the real chain a block with a harder target adds more work than an easier one (Bitcoin Core, 2026). "
 "It is like a tug of war decided by total pull and not by the number of pullers: one strong team beats two weak ones.")

A["DoubleSpendByReorganization"] = (
 "A payment is only as final as the chain that holds it, and the book shows how a double spend works: the buyer sends a competing transaction that spends the same coins and cancels the payment (Antonopoulos and Harding, 2023). "
 "On two Bitcoin Core 31.1 test nodes the payment of 49.999 coins to Carol was confirmed once and the wallet showed that she had received it; a competing branch that refunded the same coins to Mallory was then given one block more work, and the node reorganized, the payment showed -2 confirmations (a conflicted transaction), Carol had received 0 and the refund had 2 confirmations (Bitcoin Core, 2026). "
 "Rosenfeld's analysis of hashrate-based double spending gives the probability of such a reversal for attackers of every size (Rosenfeld, 2014). "
 "It is like a shop that hands over goods against a cheque, only to learn later that the bank has cancelled it: the more banks have countersigned, the less likely it is.")

