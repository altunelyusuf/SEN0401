"""SEN0401 chapter 12 (Mining and Consensus): the teaching paragraphs of the leaves of subject 5 (pools, attacks) and subject 6 (hard forks, soft forks and their activation), then the introductions of the six subjects (TOP)
and of the fifteen sections (MID). One paragraph per leaf, one line, full sentences. Every paragraph cites a source in the form (Name and Name, 2023). Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
D = {}

D["PoolConcentration"] = (
 "Most miners do not mine alone but in pools, which add the work of many machines and share the rewards, so that the identity of the finder of a block says who runs the largest pools (Antonopoulos and Harding, 2023). "
 "In the 52,371 blocks of the last year, Foundry USA found 14,750 (28.2 percent), AntPool 9,510 (18.2), F2Pool 6,602 (12.6) and ViaBTC 5,077 (9.7), so the two largest pools together found 46.3 percent and the four largest 68.6 percent, from a list of 32 named pools (Mempool Space, 2026). "
 "A pool is a manager of machines and not the owner of all of them, and the machines may leave for another pool, but the concentration is the first number to look at when asking how far the network is from the thresholds of attack. "
 "It is like a few big wholesale markets that supply many small stalls: the stalls are many, but the trucks start from a few gates.")

D["SoloMinerVariance"] = (
 "The book says that a miner with 1 percent of the network hash rate would find more than one block per day on average (Antonopoulos and Harding, 2023); with 144 blocks a day this is 1.44 blocks. "
 "A miner with 0.01 percent would find 5.26 blocks per year, would wait 69 days on average between blocks, and would see no block in a whole year with a probability of 0.52 percent, but in any single month the chance of no block is 65 percent, because the waiting time is exponentially distributed. "
 "That variance is why small miners join a pool and accept a smaller, steady income and a fee of the manager in place of a rare large prize. "
 "It is like fishing alone with one line or in a fleet that shares the catch: the fleet's income is stable, the loner's depends on one lucky day.")

D["PoolSharesAndFees"] = (
 "A pool needs a way to see that its members really work, so it asks for shares: hashes that are below an easier target than the network's, and a member proves effort by showing many of them (Bitcoin Wiki, 2026). "
 "If one hash in 1,024 is a share, a miner expects 1,024 shares for each hash that would win a block, and the chance of finding at least one share in 1,024 tries is 63 percent, as the arithmetic shows; the book's own count for a pool is typically more than 1,000 shares per block, with managed pools taking a percentage fee for the service, and P2Pool as the decentralized alternative (Antonopoulos and Harding, 2023). "
 "Different pools pay by different rules, for example pay per share or pay per last N shares (Bitcoin Wiki, 2026). "
 "It is like a collective that pays pickers by the full baskets they hand in, although only one in a thousand baskets contains the golden strawberry.")

D["StratumProtocols"] = (
 "A pool and a machine speak a protocol, and the usual one is Stratum, which has been used since 2012 for pooled mining and replaced the older getwork (Bitcoin Wiki, 2026). "
 "BIP 310 extends it with a 'version-rolling' feature, and the RPC getblocktemplate of BIP 22 is the other way a miner obtains work from a node (Palatinus et al., 2017); (Dashjr, 2012). "
 "Stratum V2 is a binary protocol that encrypts the channel and optionally lets miners declare their own block templates, so that the pool does not choose every transaction, and Bitcoin Core 30.0 added an experimental IPC mining interface to work with Stratum v2 or other client software (Stratum contributors, 2026); (Bitcoin Core developers, 2025). "
 "The book says that pool miners connect to the pool server using Stratum, version 1 or version 2, and that in version 1 the pool builds the candidate header and sends it to its miners as a template (Antonopoulos and Harding, 2023). No pool session was run for this chapter. "
 "It is like the difference between a delivery company that picks your route and one that lets you plan your own: the packages are the same, the control is not.")

D["BlockWithholding"] = (
 "A pool has an attack against it that the book's pool section does not mention: a member submits shares and is paid for them, but never submits a share that would be a full block, so the pool gets none of the block rewards he finds (Bitcoin Optech, 2026). "
 "The Optech topic estimates that such a miner keeps 99.9 percent of the expected revenue without doing any good for the pool, and it names oblivious shares as a proposed remedy. "
 "The case shows that a pool depends on trust and on what it can verify. "
 "It is like a pickers' collective in which one member hands in only the unripe fruit and keeps the ripe fruit for himself.")

D["NakamotoCatchUpOdds"] = (
 "Nakamoto's paper computes the chance that an attacker with a share q of the hash rate ever catches up from z blocks behind, a Poisson sum that falls fast with z when q is under one half (Nakamoto, 2008). "
 "Recomputed, a 10 percent attacker has a chance of 0.0002428 from 6 blocks behind, the value printed in the paper, and 0.2045873 from one block; a 30 percent attacker has 0.1321 from 6 blocks and a 45 percent attacker 0.766, while a half-share attacker is nearly sure to win, which is why the book advises more confirmations for large amounts (Antonopoulos and Harding, 2023). "
 "Rosenfeld extends the analysis to the case where the merchant waits for a number of confirmations (Rosenfeld, 2014). "
 "It is like a race where the runner who is behind by 6 laps needs a long run of luck to catch up, unless he is nearly as fast as the leader.")

D["SelfishMiningThreshold"] = (
 "Selfish mining is a strategy in which a miner keeps found blocks secret and releases them to waste the work of others; Eyal and Sirer show that it pays above a threshold that depends on the share g of honest miners who follow the selfish block, and that the upper bound of the threshold is 1/3 of the network (Eyal and Sirer, 2013). "
 "The threshold is (1 - g) / (3 - 2g): one third when g is 0, one quarter when g is one half, and nothing when g is 1, as the formula gave in the recomputation. "
 "Optech summarises that it allows a miner with less than a majority to earn more than his share (Bitcoin Optech, 2026). "
 "It is like a card player who hides cards up his sleeve and shows them at the right time: only if enough of the table believes him does the trick pay.")

D["TopPoolVersusThresholds"] = (
 "Putting the numbers together: the largest pool of the last year, Foundry USA, found 28.16 percent of the blocks, below the one third of the strongest selfish-mining threshold but above the one quarter of its middle case, and the two largest pools found about 46 percent (Mempool Space, 2026); (Eyal and Sirer, 2013). "
 "A pool's share of blocks is not the share of an owner, since members can leave, so the figures say how concentrated the coordination is and not that the attack is likely; the book itself notes that the consensus depends on a majority of the miners acting honestly in their own interest (Antonopoulos and Harding, 2023). "
 "It is like the largest party in a parliament that has under a third of the seats: not a majority, but enough that others must listen.")

D["MajorityAttackLimits"] = (
 "A majority attack, usually called a 51 percent attack, lets a group with most of the hash rate build a private chain longer than the public one and publish it, so that its own earlier payments disappear (Bitcoin Wiki, 2026). "
 "The book states what the attacker can do: double-spend his own transactions and censor chosen transactions by re-mining any block that includes them; and it adds that the attack does not actually require 51 percent but only becomes almost certain there (Antonopoulos and Harding, 2023). "
 "The recomputed odds agree: 45 percent has a chance of 0.766 from 6 blocks behind, and 50 percent is above 0.99. "
 "No attack on a public chain was run for this chapter; only the private double spend of the reorganization leaf. "
 "It is like a person who owns most of the votes in a club: he cannot forge another member's signature, but he can outvote everybody on what the minutes say.")

D["MinorityChainSlow"] = (
 "In a hard fork, nodes with new rules accept blocks that the old nodes reject, and the two groups follow different chains (Antonopoulos and Harding, 2023). "
 "The book's example of an 80 to 20 split gives the arithmetic: the 80 percent chain gets a block every 12.5 minutes, so 2,016 blocks take 25,200 minutes, 17.5 days, before its difficulty drops, while the 20 percent chain gets a block every 50 minutes and needs 70 days for a retarget. "
 "A fork where the minority chain is that slow will probably wither, which is one way in which hard forks end. "
 "It is like a road that splits where 80 of 100 cars take the left branch: the right branch is almost empty, and almost no one uses it a week later.")

D["ChainSplitMarch2013"] = (
 "The book mentions in a single sentence the unanticipated hard fork of the upgrade from Bitcoin Core 0.7 to 0.8, caused by a limitation of the Berkeley DB used to store blocks (Antonopoulos and Harding, 2023); the dates and numbers are as follows. The fork happened on 2013-03-11 at 23:24:19 UTC, when block 225,430, a block with 797 transactions and 249,119 bytes, was accepted by Bitcoin 0.8 and rejected by older versions (Mempool Space, 2026). "
 "BIP 50 explains why: versions before 0.8 had too few Berkeley DB locks to process a large but valid block, which made the lock limit an accidental consensus rule, while 0.8 used LevelDB and did not have that limit (Andresen, 2013); (Wikipedia contributors, 2026). "
 "Vitalik Buterin reported for Bitcoin Magazine that for about six hours there were two networks with two histories, and the split lasted 24 blocks, which agrees with block 225,454 at 06:19:32 UTC the next morning (Buterin, 2013); (Mempool Space, 2026). "
 "The pools Slush and BTCGuild went back to 0.7 to restore the old chain, giving up some income (Andresen, 2013). "
 "It is like two railway lines that go to different stations because a switch was set differently in two depots.")

D["BitcoinCashFork2017"] = (
 "A fork can also be made on purpose: Bitcoin Cash split from Bitcoin on 1 August 2017 at block 478,559, and the last block that both share is 478,558 (Wikipedia contributors, 2026). "
 "It changed the rules and kept the 2016-block difficulty adjustment but added an emergency adjustment, which is the kind of hard fork the book describes: nodes that do not upgrade cannot follow, and those that do end up on another chain (Antonopoulos and Harding, 2023). "
 "The split happened a few weeks before segwit became active, on 24 August 2017 at block 481,824 (Wikipedia contributors, 2026). "
 "It is like a group of friends who agree to separate at a crossroads, and from then on neither can follow the other's route.")

D["SoftForkOnlyTightens"] = (
 "A soft fork makes the rules stricter, so that blocks valid under the new rules are also valid under the old ones, and old nodes keep following the chain as long as a majority of the miners enforce the new rules (Antonopoulos and Harding, 2023). "
 "The test pair of Bitcoin Core 31.1 nodes showed the asymmetry: a lax node accepted a block with no height in the coinbase while the strict node answered bad-cb-height, the strict node then could not follow the lax chain (prev-blk-not-found), and when the strict chain became longer the lax node reorganized onto it (Bitcoin Core, 2026). "
 "Both nodes rejected a block of version 1, which is rule BIP 34 in force. "
 "It is like a club that bans shorts: those in trousers are welcome in both the old and the new club, but someone in shorts can enter only the old one.")

D["Bip34Activation"] = (
 "BIP 34 was the first soft fork to be activated by counting the version of recent blocks: when 750 of the last 1,000 blocks were version 2 or greater, invalid version-2 blocks were refused, and when 950 of the last 1,000 were, all version-1 blocks were refused (Andresen, 2012). "
 "The book gives the same two thresholds (Antonopoulos and Harding, 2023). "
 "The history is now written into the code as plain heights: BIP 34 applies from block 227,931 on mainnet and 21,111 on testnet3 (Bitcoin Core, 2026). "
 "On the test pair of nodes the strict node reported BIP 34 as buried and active from height 1. "
 "It is like a library that waits until three quarters of the members have the new card and then, when nearly all have it, stops accepting the old card.")

D["Bip9StateMachine"] = (
 "BIP 9 replaced the counting of BIP 34 with a state machine for each deployment: defined, started, locked_in, active or failed, decided once per period of 2,016 blocks, with the threshold of 1,916 blocks (95 percent) and one of bits 0 to 28 to signal on (Wuille et al., 2015). "
 "The book shows the diagram and says that proposals that reach the threshold are activated one period later (Antonopoulos and Harding, 2023). "
 "On the Bitcoin Core 31.1 test chain, with a period of 144 and a threshold of 108, the deployment was defined at height 143, started at 144, locked_in at 288 and active at 432 (Bitcoin Core, 2026), and the node's source has the same state names (Bitcoin Core, 2026). "
 "It is like a bill in a parliament: introduced, voted on, approved and then in force after a waiting period.")

D["FailedDeployment"] = (
 "A proposal that does not get enough signals before its timeout is not shelved but marked failed, and stays failed for ever (Antonopoulos and Harding, 2023). "
 "On the test chain a deployment with the timeout 1 was defined at height 143, started at 144 and failed at height 288, at the end of the first period, and the block version the node itself produced stayed 0x20000000, signalling nothing (Bitcoin Core, 2026). "
 "The state machine is the one of BIP 9 (Wuille et al., 2015). "
 "Failure is part of the design: a change that the miners do not want does not take effect by accident. "
 "It is like a petition that closes on a set date: if it has too few signatures by then, it lapses and cannot be opened again.")

D["Segwit2017Activation"] = (
 "Segregated witness was proposed for activation with BIP 9 on bit 1 between 2016-11-15 and 2017-11-15, but it was not activated by miners for a long time (Hilliard, 2017). "
 "BIP 91 specified a method to activate it with a majority of hashpower below 95 percent, and BIP 148 a flag day on which nodes would reject blocks that did not signal, which the book recounts as the proposal of a pseudonymous developer (Hilliard, 2017); (Shaolinfry, 2017); (Antonopoulos and Harding, 2023). "
 "The Wikipedia article states that blocks 477,792 to 479,807 signalled, locking it in, and that it was active on 24 August 2017 at block 481,824, the figure that chainparams.cpp gives, with CSV at 419,328 (Wikipedia contributors, 2026); (Bitcoin Core, 2026). "
 "BIP 141 is also where the witness commitment explained earlier is defined (Lombrozo et al., 2015). "
 "It is like a strike notice that is withdrawn when the other side starts to talk: the deadline did its work without being used.")

D["Bip8LockInByHeight"] = (
 "BIP 8 is a redesign of BIP 9: it counts in block heights instead of time, and has a flag lockinontimeout which, if true, requires blocks to signal in the final period, so that the soft fork is locked in by the timeout height (Fry and Dashjr, 2017). "
 "The book explains that many users saw it as a flaw of BIP 9 that miners could prevent an activation by not signalling for a year, and that BIP 8 therefore defines a MUST_SIGNAL period in which miners must signal; software using it was published for taproot in 2021 (Antonopoulos and Harding, 2023). "
 "Optech's overview of soft fork activation lists the proposals and the debate (Bitcoin Optech, 2026). "
 "No node of this chapter ran BIP 8. "
 "It is like a deadline in a contract that says what happens if nobody signs: the default is no longer 'nothing'.")

D["SpeedyTrialTaproot"] = (
 "Taproot was activated by a quick variant of BIP 9 called Speedy Trial: start 2021-04-24, timeout 2021-08-11, a threshold of 1,815 of 2,016 blocks (90 percent, instead of 1,916) and a minimum activation height of 709,632 (Wuille et al., 2020). "
 "Bitcoin Core 0.21.1 shipped these parameters, and the chain parameters of release 31.1 still carry them with bit 2 (Bitcoin Core developers, 2021); (Bitcoin Core, 2026). "
 "The first block under taproot rules, block 709,632, was mined by F2Pool on 2021-11-14 at 05:15:27 UTC (Mempool Space, 2026). "
 "Optech has a topic on taproot and its activation (Bitcoin Optech, 2026). "
 "It is like a trial period in a shop for a new till: if enough staff accept it within three months, it starts on the date after the next stocktake.")

D["BuriedDeployments"] = (
 "When a soft fork is long past, the node no longer needs to count votes and writes down only its height: BIP 34, 65, 66 and CSV and segwit are in the chain parameters as heights, for example SegwitHeight 481,824 and CSVHeight 419,328 (Bitcoin Core, 2026). "
 "The deploymentinfo source names them bip34, bip65, dersig, csv and segwit next to taproot and a test dummy, and on the two test nodes BIP 34 was reported as buried, active from height 1 on the strict node and at height 100,000 on the lax one (Bitcoin Core, 2026); (Bitcoin Core, 2026). "
 "BIP 65 (OP_CHECKLOCKTIMEVERIFY) and BIP 66 (strict DER signatures) are among those soft forks, and both have the status Deployed in their documents (Todd, 2014); (Wuille, 2015). "
 "It is like a street that was once a building site: after it opens, the plan shrinks to a line on the map.")

D["Bip54ConsensusCleanup"] = (
 "The next proposed change of the rules, BIP 54, the consensus cleanup, fixes the time warp attack, makes a transaction invalid if its inputs have more than 2,500 signature operations, forbids transactions of exactly 64 bytes without witness data, and sets the coinbase locktime to the height minus 1 (Poinsot and Corallo, 2025). "
 "Optech explains the time warp: miners can make a period look four weeks long and halve the difficulty (Bitcoin Optech, 2026), and Bitcoin Core 30.0 has a change made to prepare for a possible BIP 54 deployment in the future (Bitcoin Core developers, 2025). "
 "The same rules have a test network version in BIP 94 (Jahr, 2024). "
 "It is not active on mainnet, and the book, written in 2023, does not mention it (Antonopoulos and Harding, 2023). "
 "It is like a spring clean of the rules: several small repairs bundled so that the cost of one change is shared.")

TOP = {}
TOP["MoneyCreation"] = ("The first subject is the way new coins come into being: a reward that is cut in half on a fixed timetable and the fees of the transactions, claimed in the first transaction of each block (Antonopoulos and Harding, 2023). "
 "Each statement was recomputed from the code and the real halving blocks, and the reward rules were tried on a private chain of Bitcoin Core 31.1 (Bitcoin Core, 2026).")
TOP["DecentralizedConsensus"] = ("The second subject is why nobody has to be trusted: every node checks every transaction and block by the same rules, picks the chain with the most work and rejects the rest (Antonopoulos and Harding, 2023). "
 "Thirteen transaction cases and fourteen block cases were run against a Bitcoin Core 31.1 node (Bitcoin Core, 2026).")
TOP["BuildingTheCandidateBlock"] = ("The third subject is how a miner assembles a block from the template, the coinbase and the header before any hashing is done (Antonopoulos and Harding, 2023). "
 "The fields were read from real blocks of the main chain and from templates of a node (Mempool Space, 2026).")
TOP["ProofOfWork"] = ("The fourth subject is the work itself: a hash below a target, a target that follows from a compact number, and a difficulty that adjusts every 2,016 blocks (Antonopoulos and Harding, 2023). "
 "The retarget rule reproduced a real adjustment of 2024 (Bitcoin Core, 2026).")
TOP["MiningCompetition"] = ("The fifth subject is the contest among miners: how they get enough room to vary the header, how they join in pools, and how large a share of the hash rate would be needed to attack (Antonopoulos and Harding, 2023). "
 "The statistics come from the blocks of the last year (Mempool Space, 2026).")
TOP["ChangingConsensusRules"] = ("The sixth subject is how the rules can be changed without breaking the network: hard forks that need everybody and soft forks that need only the miners, with the signalling schemes that decide when (Antonopoulos and Harding, 2023). "
 "The deployments were followed on real blocks and in state machines run on test chains (Wuille et al., 2015).")

MID = {}
MID["SubsidySchedule"] = ("This section is about the timetable of the reward: the halving every 210,000 blocks, the limit on the supply, an error in the book's script and the shortened interval of regtest (Antonopoulos and Harding, 2023).")
MID["RewardComposition"] = ("This section is about what the reward is made of, the subsidy and the fees, and about the rule that the sum may be claimed in full, partly, but never above the limit (Bitcoin Core, 2026).")
MID["IndependentVerification"] = ("This section is about the checklists: the transaction rules, the block rules and the maturity of rewards, each tested with a rule broken on purpose (Bitcoin Core, 2026).")
MID["ChainSelection"] = ("This section is about choosing between competing chains by most work and about what happens to a payment when the chain that holds it is replaced (Antonopoulos and Harding, 2023).")
MID["BlockTemplate"] = ("This section is about the template that a node gives to a miner and the order in which it fills a block with transactions (Dashjr, 2012).")
MID["CoinbaseTransaction"] = ("This section is about the first transaction of the block: its null input, the height, the locktime, the witness commitment, the tags and the extra nonce (Antonopoulos and Harding, 2023).")
MID["HeaderConstruction"] = ("This section is about the 80-byte header that is hashed: its fields in a real block, the version bits and the two rules for the time (Antonopoulos and Harding, 2023).")
MID["TheLottery"] = ("This section is about the idea of proof of work shown with a toy hash, a pair of dice and the cost of checking compared to the cost of finding (Back, 2002).")
MID["TargetAndDifficulty"] = ("This section is about the target, the way it is packed in the header, the difficulty and the hash rate that follows from it (Bitcoin Wiki, 2026).")
MID["Retargeting"] = ("This section is about the adjustment every 2,016 blocks, tested against a real epoch, with its flaws, its limits and its newest branch (Bitcoin Core, 2026).")
MID["NonceSpace"] = ("This section is about running out of nonces and the three ways round it: the extra nonce, the rolled version bits and the tricks of the hardware (Antonopoulos and Harding, 2023).")
MID["MiningPools"] = ("This section is about pools: how concentrated they are, why small miners join, how shares are counted, which protocols they speak and what attacks them (Antonopoulos and Harding, 2023).")
MID["HashrateAttacks"] = ("This section is about the attacks that need a large share of the hash rate and how likely they are to succeed at each share (Nakamoto, 2008).")
MID["HardForks"] = ("This section is about changes that split the network: the arithmetic of a minority chain, the accidental fork of 2013 and the deliberate fork of 2017 (Antonopoulos and Harding, 2023).")
MID["SoftForks"] = ("This section is about changes that keep old nodes on the chain, and the schemes used to decide when to switch them on: counting, BIP 9, BIP 8 and Speedy Trial (Antonopoulos and Harding, 2023).")
