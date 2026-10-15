"""SEN0401 chapter 9: the teaching paragraphs of the leaves of subject 7 (fee sniping and the incentives), and the introductions of the 20 mid-level and 7 top-level subjects
(the data module adds to each introduction a sentence that lists its members)."""
__version__ = "1.0.0"
D = {}

D["SubsidyHalvings"] = (
 "The block subsidy is the amount of new bitcoin that the miner of a block may create in its coinbase transaction; it started at 50 bitcoins and is cut in half every 210,000 blocks, which the book describes in its chapter on mining as 6.25 new bitcoins in 2023 and a coming halving at block 840,000 (Antonopoulos and Harding, 2023). "
 "In the source function GetBlockSubsidy the rule is a shift: the number of halvings is the height divided by 210,000, the starting value is 50 coins, and the value is shifted right by the number of halvings (Bitcoin Core, 2026). It is like a pie that is cut in half at every anniversary. "
 "The chapter's function gives 5,000,000,000 satoshis at the heights 0 and 209,999, 2,500,000,000 at 210,000, 625,000,000 at 839,999 and 312,500,000 at 840,000 and at the height 971,489 of 2026-10-15. "
 "The subsidy matters for this chapter because every halving makes the fees a larger part of what a miner earns (Nakamoto, 2008).")

D["FeesVsSubsidy"] = (
 "The book says in its section on fee sniping that the attack is not very lucrative today because the block subsidy is much higher than the total fees per block, and that at some point in the future fees will be the majority of the reward (Antonopoulos and Harding, 2023). "
 "Whether that is true depends on the block. Block 840,000, mined on 2024-04-20, paid its miner 4,075,061,499 satoshis of which 3,762,561,499 (37.6 bitcoins) were fees, only 312,500,000 (3.125 bitcoins) subsidy: the fees were 92.33 percent of the reward. Block 971,489 of 2026-10-15 carried fees of 1,454,221 satoshis against the same subsidy, 0.46 percent (Mempool Space, 2026). "
 "It is like the tips of a restaurant, which on one evening can be larger than the wage and on another a few coins. The statement of the book is a fair description of an average block and is wrong for the halving block, a correction that the chapter lists among its findings; the share is computed here from the explorer's numbers and the rule of the subsidy (Bitcoin Core, 2026).")

D["FeeOnlyFuture"] = (
 "Satoshi Nakamoto's paper says that the incentive for miners can also be funded with transaction fees: if the output value of a transaction is less than its input value, the difference is a transaction fee that is added to the incentive value of the block, and once a predetermined number of coins have entered circulation the incentive can transition entirely to fees (Nakamoto, 2008). "
 "The book follows this line when it says that the fees become more and more important as the subsidy declines and provide the incentive to continue securing Bitcoin with proof of work (Antonopoulos and Harding, 2023). "
 "Carlsten and his coauthors at Princeton asked whether it makes no difference to security whether miners are paid by block rewards or by fees, and showed that it does: with only fees the variance of the reward grows and new strategies appear (Carlsten et al., 2016). "
 "It is like a shop that is paid only by tips and not by a wage. The chapter finds both passages in its saved copies of the papers and does not simulate their models; the question is open in the sense that it depends on the future of the fee market.")

D["SnipingProbability"] = (
 "Fee sniping is the attack in which a miner deliberately re-mines one or more earlier blocks to take the fees from the miners who first created them, perhaps with a block extending the chain at the same time; the Optech topic page gives the dishonest miner's chance of success, if every other miner is honest, as (x / (1 - x)) squared, where x is the miner's share of the hash rate (Bitcoin Optech, 2026). "
 "The formula is small but telling: a miner with a tenth of the hash rate succeeds with probability 1.23 percent, one with 30 percent with 18.37 percent, one with 45 percent with 66.94 percent, and one with half with certainty, since a miner who can out-mine all others combined can always win the race. "
 "It is like a race in which the cheat has to run two laps while the honest runners run one. "
 "The chapter computed the values with the formula and does not claim that real miners do this; the book calls it a theoretical attack scenario and the hash rate of single miners is below the levels where the chance is high (Antonopoulos and Harding, 2023).")

D["UndercuttingAttack"] = (
 "In the study On the Instability of Bitcoin Without the Block Reward, Carlsten, Kalodner, Weinberg and Narayanan from Princeton University show that when transaction fees are the only reward, mining honestly may no longer be the best strategy; a miner can profit by forking the head of the chain and leaving the high-fee transactions of the latest block unmined, so that the next blocks collect them, which they call the undercutting attack (Carlsten et al., 2016). "
 "It is like a bakery that waits for the neighbour's best bread to be taken away and sells it as its own. "
 "The paper's simulator explores strategies and finds that undercutting can be harmful to the stability of Bitcoin consensus, and the authors conclude that the role of block rewards must be rethought. "
 "The chapter found the passages in the saved copy of the paper, which is dated 2016 and was presented at the ACM conference on computer and communications security in Vienna; it did not rerun the simulator, and it reports the paper as a reason for the defence in the next leaves (Carlsten et al., 2016).")

D["WalletLockTimeRule"] = (
 "A lock time is a field of the transaction that says in which block height or at which time the transaction becomes valid. To discourage fee sniping a wallet sets it to the height of the current tip, so that only the next block can include the transaction; the source comment says that a miner who considers fee sniping then has fewer options for pulling off the attack (Bitcoin Core, 2026). "
 "In about one case in ten the code subtracts a random number of 0 to 99 blocks, which is good for the privacy of transactions that are broadcast late. "
 "The run made 60 payments with the wallet and read their lock times: 56 equal the tip and four were back-dated, by 6, 28, 35 and 54 blocks, all below 100; every one carried the sequence 0xfffffffd. The expected share is 10 percent and the run gave 6.7 percent, which is within the chance of a sample so small. "
 "It is like a date stamp that says not before today. The book recommends this defence for all wallets (Antonopoulos and Harding, 2023).")

D["WalletLagFallback"] = (
 "The defence only makes sense if the wallet knows the real tip. The source of the wallet defines the function IsCurrentForAntiFeeSniping, which returns false while the node is in initial block download or when the best block is older than 8 hours, a constant MAX_ANTI_FEE_SNIPING_TIP_AGE of 8 x 60 x 60 seconds (Bitcoin Core, 2026). "
 "In that case the code sets the lock time to a constant 0, with the comment that this avoids leaking a potentially unique lock time fingerprint, since a wallet with an old tip would write an old height that others do not. "
 "It is like a clerk who does not write the date on a form when the office calendar is out of date. "
 "The chapter found the constant and the two statements in the saved source and computed 8 x 60 x 60 = 28,800 seconds; the case was not run, because a regtest chain made on the same day is never older than eight hours and the test would only show the same value 0.")

D["MainnetPrevHeightShare"] = (
 "Do real wallets use the defence? The chapter counted, in the first 599 transactions after the coinbase of two mainnet blocks, how many carry a lock time equal to the height of the previous block, which is what a wallet that follows the rule writes when the transaction is created while that block is the tip. In block 840,000 (2024-04-20) it was 89 of 599 (15 percent) and in block 971,489 (2026-10-15) 33 of 599 (6 percent); a lock time of 0 was carried by 507 and 563 (Mempool Space, 2026). "
 "The share is a lower bound for wallets that follow the rule, because a transaction created some blocks earlier will show an older height, and an upper bound for nothing in particular, because other software may write the same number. "
 "It is like counting how many cars have their lights on at noon. The defence is therefore used but not general (Bitcoin Optech, 2026), and BIP 326 mentions that about a fifth of recent transactions had anti-fee-sniping lock times in the author's data (Belcher, 2021).")

D["LockTimeBoundary"] = (
 "The book sets the lock time of the example to 100,001 when the highest block is 100,000 and says that the transaction can only be included in block 100,001, the next block; the chapter on transactions says that a lock time of 123,456 can be included in block 123,456 (Antonopoulos and Harding, 2023). "
 "The consensus rule in the function IsFinalTx is different by one: a transaction with a lock time below the height of the block is final, so a lock time equal to the height is not, and the earliest block for a lock time of L is the block L + 1 (Bitcoin Core, 2026); BIP 113 says the same in other words, that a transaction is excluded while the block height is less than or equal to the lock time (Kerin, 2015). "
 "The chapter computed the function for 100,001 in block 100,001 (not final) and for 100,000 (final), and ran it: with the tip at 129 a lock time of 130 was refused as non-final by the mempool and a block of height 130 containing it was rejected with bad-txns-nonfinal, while a lock time of 129 was accepted and mined; the wallet, in the run above, used the tip. "
 "It is like a ticket that is valid from the day after the date printed on it. This is an error of the printed book, and it is not corrected on the development branch.")

D["FinalSequenceDisablesLockTime"] = (
 "A lock time is only enforced when at least one input of the transaction has a sequence number that is not final; if every input has the sequence 0xffffffff, the transaction is final whatever its lock time says, and the function IsFinalTx returns true after its loop over the inputs (Bitcoin Core, 2026). "
 "The book's chapter on transactions describes the same: setting the sequence to its maximum value finalizes the transaction (Antonopoulos and Harding, 2023). It is like an agreement in which a special clause overrides the date. "
 "In the run, at the tip 254, a transaction with the lock time 255 and the sequence 0xffffffff was accepted by the mempool, the same transaction with the sequence 0xfffffffd was refused as non-final, the one with lock time equal to the tip was accepted, and after one block (tip 255) the transaction with 255 and 0xfffffffd became acceptable. "
 "This is why a wallet that wants the defence against fee sniping must never use the final sequence, and the source asserts it, in the code that sets the lock time (Bitcoin Core, 2026).")

D["TaprootAntiSniping"] = (
 "The lock time field has a disadvantage: it is used by few wallets for other reasons, so it can reveal which software made a transaction. BIP 326 proposes that wallets set the sequence field in their taproot transactions, in place of their regular lock time protection, so that a transaction with a sequence value is not unusual and the anti-fee-sniping protection also works for those who use the sequence of BIP 68 (Belcher, 2021). "
 "It argues that with the protection by lock time or sequence the bad miner soon runs out of transactions to put in the first block and has to change the plan. It is like using a stamp that many people use so that the letter does not stand out. "
 "The proposal is for taproot outputs, which the book discusses in other chapters, and it keeps the lock time as well in some transactions, because absolute lock times are still used. "
 "The chapter found the passages in the saved copy of the BIP and did not execute the proposal, because Bitcoin Core 31.1 was not shown to implement it.")

# ------------------------------------------------------------------------------------------------------------------------ mid-level introductions
MID = {}
MID["FeeAsDifference"] = ("The first subject asks what a fee is on the level of the bytes: no field, only a gap between what goes in and what comes out, and the consequences for a sender who forgets a change output (Antonopoulos and Harding, 2023). "
 "It matters because a transaction built by hand is the one place where a wrong subtraction costs real money, and because every wallet, explorer and estimator reads the fee the same way.")
MID["SpenderAndSignature"] = ("The second subject asks who can pay a fee: the sender, because the signature covers the outputs, and the receiver only through a second transaction (Antonopoulos and Harding, 2023). "
 "It matters because the design explains why fee bumping comes in two kinds, one that only the sender can do and one that anyone who receives an output can do.")
MID["MinerChoice"] = ("The third subject asks who decides which transactions enter a block: the miner, who treats the fees as bids and fills a scarce space with the highest-paying transactions, and who alone may claim the subsidy in the coinbase (Antonopoulos and Harding, 2023). "
 "It matters because everything in the chapter, from fee rates to carve-outs, is a way of speaking to that decision.")
MID["SizeAndWeight"] = ("This subject asks in what unit the size of a transaction is measured, because a price per unit needs a unit: weight units and virtual bytes, with the discount for witness data and the limit of the block (Lombrozo et al., 2015). "
 "It matters because the same transaction has three sizes, in bytes, in virtual bytes and in weight units, and mixing them gives wrong fee rates.")
MID["FeeRateArithmetic"] = ("This subject asks how the price of block space is computed and written: the division of the fee by the size, the units in which it is written, the mistakes between units and the guard against absurd amounts (Antonopoulos and Harding, 2023). "
 "It matters because a wallet is trusted with money and a wrong power of ten in a field is the commonest way to lose it.")
MID["MinimumRates"] = ("This subject asks how low a fee rate may be: the minimum that nodes relay, the minimum that the wallet accepts and the smallest output that is worth creating, the dust limit (Bitcoin Core, 2026). "
 "It matters because these floors are policies and not laws of Bitcoin, they change from release to release and they decide whether a presigned transaction can ever be broadcast.")
MID["EstimatorMechanics"] = ("This subject asks how a node guesses the fee rate that is needed: from the record of the past, with thresholds, targets and a mode that was changed in release 28.0 (Bitcoin Core developers, 2024). "
 "It matters because the guess is the default behaviour of most wallets, and a user who understands its limits knows when to override it.")
MID["FeeMarketOnMainnet"] = ("This subject asks what the market looks like in real data: two mainnet blocks 2.5 years apart, a public explorer's recommendation of today and an early study of how people paid fees (Mempool Space, 2026). "
 "It matters because the book's statements about the market were written at one moment, and the numbers show how far the market can move.")
MID["ReplaceableSignal"] = ("This subject asks which transactions can be replaced: those that signal, as BIP 125 defined, or all, which is now the default since release 28.0, and the option that was removed in release 29.0 (Harding, 2015) (Bitcoin Core developers, 2025). "
 "It matters because the book's statement that full replacement is disabled by default is the first one that is out of date, and because merchants who accept unconfirmed payments depend on the answer.")
MID["ReplacementRules"] = ("This subject asks what a replacement must pay: the absolute fee, the incremental fee, and the idea of the feerate diagram, together with the wallet command that does it all (Harding, 2015) (Bitcoin Core, 2026). "
 "It matters because each rule is a defence against an attack on the bandwidth of the network, and the numbers can be tested on a node.")
MID["ReplacementHazards"] = ("This subject asks what can go wrong with replacement: a payee paid twice, a replacement made expensive by a big child, and an attack that cycles replacements (Antonopoulos and Harding, 2023). "
 "It matters because these are the reasons for later designs such as version-3 transactions.")
MID["PackagesAndMining"] = ("This subject asks how a miner prices a transaction together with its unconfirmed ancestors, the idea behind child pays for parent, and when a child helps and when it does not (Antonopoulos and Harding, 2023). "
 "It matters because it is the one method of fee bumping that a receiver can use.")
MID["PackageRelay"] = ("This subject asks how a parent that is too cheap to be relayed can be helped by its child: by sending them together, with the RPC submitpackage, the relay of one parent and one child, and the message with which a peer names its minimum (Bitcoin Core developers, 2024). "
 "It matters because the book says that package relay is the solution to a critical problem and that a limited early version may be available.")
MID["ClusterMempool"] = ("This subject asks how the mempool is organised in release 31.0: in clusters of at most 64 transactions, ordered into chunks, replacing the old limits of 25 related transactions (Bitcoin Core developers, 2026). "
 "It matters because the numbers and the sentence about a day's worth of transactions in the book no longer describe the software.")
MID["CarveOut"] = ("This subject asks what the carve-out was: a 2018 exception to the descendant limits for Lightning, its real size, the quadratic reasoning behind the limits and its removal in release 31.0 (Corallo, 2018). "
 "It matters because the book teaches it as a present rule and the numbers it gives differ from the code.")
MID["TrucPolicy"] = ("This subject asks how version-3 transactions solve the problems of pinning: one parent, one child, small sizes, sibling eviction and a bound on the cost of a replacement (Zhao, 2024). "
 "It matters because it is the replacement of the carve-out in the new software.")
MID["AnchorOutputs"] = ("This subject asks how a transaction that is signed long before it is sent can still be fee bumped: with an output that anyone can spend, the pay-to-anchor script, and the allowance of one dust output without fee (Sanders, 2025). "
 "It matters because Lightning channels are exactly this kind of presigned transaction.")
MID["BlockRewardMix"] = ("This subject asks what part of a miner's income are fees: the subsidy and its halvings, the fee share of two real blocks and the arguments about a future of fees only (Nakamoto, 2008). "
 "It matters because the defence against fee sniping is only needed when fees are large.")
MID["SnipingAttack"] = ("This subject asks how likely and how dangerous fee sniping is: the formula of its chance and the undercutting attack of the Princeton study (Bitcoin Optech, 2026). "
 "It matters because the book calls the attack theoretical, and the numbers show how the chance rises with the hash rate.")
MID["LockTimeDefense"] = ("This subject asks how a wallet defends against fee sniping with the lock time: the rule of Bitcoin Core, its fallback, the use on the real chain, the exact boundary of the consensus rule, the effect of the final sequence and the proposal for taproot (Bitcoin Core, 2026). "
 "It matters because the book's example is off by one block, and the correct rule is the one the node enforces.")

# ------------------------------------------------------------------------------------------------------------------------ top-level introductions
TOP = {}
TOP["WhoPaysTheFee"] = ("The first section of the chapter explains that a transaction fee is a bid in an auction for the room in a block, that it is paid by the spender because only the spender's signature can commit to it, and that it is nothing but the gap between inputs and outputs (Antonopoulos and Harding, 2023). "
 "The subject is a good first lesson for a newcomer because it needs no special software: a calculation with two numbers explains it, and the node's refusals show the safeguards. "
 "In the study each statement of the section was checked on a private test chain of Bitcoin Core 31.1 and in a block of the real chain.")
TOP["FeesAndFeeRates"] = ("The second section teaches that the price of block space is the fee rate, which is the fee divided by the size, and that the size is measured in virtual bytes after the discount for witness data (Antonopoulos and Harding, 2023). "
 "It also has to tell the user about the units, the guards against absurd fees and the minimum rates, which changed in release 30.0 (Bitcoin Core developers, 2025). "
 "The study recomputed the sizes with an independent parser and tried the minimum rates on a node.")
TOP["FeeEstimation"] = ("The third section shows how a node estimates the fee rate that is needed for a transaction to confirm in a given number of blocks, from its record of the past, and how far the numbers of the real network can be compared (Antonopoulos and Harding, 2023). "
 "The default mode of the estimator was changed in release 28.0 (Bitcoin Core developers, 2024), and the study adds real data from two blocks of the chain.")
TOP["ReplaceByFee"] = ("The fourth section is about replacing a transaction by a conflicting one that pays more, the first of the two fee bumping methods, and it is the part of the chapter that has changed most: full replacement is now the default and its option has been removed (Bitcoin Core developers, 2024) (Bitcoin Core developers, 2025). "
 "The study ran the rules on a node and reproduced the book's warning about paying twice.")
TOP["ChildPaysForParent"] = ("The fifth and sixth sections of the chapter are about the second fee bumping method, child pays for parent, and about package relay that makes it work when the parent is too cheap to be kept (Antonopoulos and Harding, 2023). "
 "In release 31.0 the mempool was rebuilt around clusters, which changes the limits that the book describes (Bitcoin Core developers, 2026). "
 "The study ran packages, a chain of 65 transactions and a miner with a very small block.")
TOP["PinningAndAnchors"] = ("The seventh and eighth sections of the chapter describe transaction pinning, in which the rules that protect nodes also make fee bumping impossible, and the carve-out and anchor outputs, which were made for Lightning (Antonopoulos and Harding, 2023). "
 "Version-3 transactions and pay-to-anchor outputs are the newer solutions, and the carve-out has been removed in release 31.0 (Zhao, 2024) (Bitcoin Core developers, 2026). "
 "The study ran each of the newer rules on a node.")
TOP["FeeSnipingAndIncentives"] = ("The ninth and tenth sections of the chapter are about adding fees correctly and about the defence against fee sniping with the lock time, which only matters when fees are a large part of the miner's income (Antonopoulos and Harding, 2023). "
 "The study computed the subsidy and the fee share of real blocks, measured the lock times of a wallet and of the chain, and found that the book's example of the lock time is off by one block (Bitcoin Core, 2026).")
