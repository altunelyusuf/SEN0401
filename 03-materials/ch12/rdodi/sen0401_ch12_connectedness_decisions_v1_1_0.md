# SEN0401 ch12 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.1 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.1) | 86 | 0 | 5 |
| after (1.1.0) | 86 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 86 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:carriesBitsOf | carries the bits of | HeaderOfBlock277316 | CompactBits | the chapter says of Header of block277316: 'bits 1903a30c'; the chapter says of Compact bits: '0x1903a30c is 0x03a30c times 256 to the power 22'. |
| chx:hashesBelowTarget | hashes below the target of | HeaderOfBlock277316 | HashBelowTarget | the chapter says of Header of block277316: 'hashes to the block id 0000000000000001b6b9a13b'; the chapter says of Hash below target: 'hash 0000000000000001b6b9a13b'. |
| chx:changesWithExtraNonce | changes with | ExtraNonceChangesRoot | ExtraNonceSpace | the chapter says of The extra nonce changes the root: 'two coinbases that differed only in extra nonce gave different txids'; the chapter says of The extra nonce space: 'An 8-byte extra nonce in the coinbase'. |
| chx:rollsVersionBits | rolls bits of | VersionHistory | VersionRolling | the chapter says of Version history: 'the bits 0x0a5fe000 carry rolled data'; the chapter says of Version rolling: 'BIP 320 reserves the 16 bits of mask 0x1fffe000 for rolling'. |
| chx:signalsTaproot | signals | VersionHistory | SpeedyTrialTaproot | the chapter says of Version history: '0x20200004 in block 709,632, which signals bit 2 for taproot'; the chapter says of Speedy Trial and taproot: 'block 709,632 was mined by F2Pool'. |
| chx:startsWithBip34 | follows the rule of | Bip34HeightPush | Bip34Activation | the chapter says of BIP 34 height push: 'Since BIP 34 the coinbase script begins with the block height as a minimally encoded number'; the chapter says of BIP 34 activation: 'BIP 34 activated by counting'. |
| chx:rejectsMissingHeight | makes the strict node refuse a block without | SoftForkOnlyTightens | Bip34HeightPush | the chapter says of A soft fork only tightens: 'the lax node accepted a block with no height in its coinbase and the strict node answered bad-cb-height'; the chapter says of BIP 34 height push: 'Since BIP 34 the coinbase script begins with the block height'. |
| chx:mintedByViaBtc | was mined by the pool tagged in | FeesOfBlock840000 | CoinbaseDataAndTags | the chapter says of The fees of block 840,000: 'mined by ViaBTC'; the chapter says of Coinbase data and tags: 'block 840,000 has /ViaBTC/'. |
| chx:fillsCoinbaseValue | fills the coinbase value of | TemplateFields | RewardIsSubsidyPlusFees | the chapter says of Template fields: 'the coinbasevalue (5,000,000,000 satoshis at height 1)'; the chapter says of Reward is subsidy plus fees: 'The most a coinbase may claim is the subsidy plus the fees of the block'. |
| chx:sizesNonceAgainstNetwork | measures the nonce space against | NonceSpaceIsTiny | HashrateFromDifficulty | the chapter says of The nonce space is tiny: 'today's network of 1.029e21 hashes per second'; the chapter says of Hash rate from difficulty: '1.029e21 of mempool.space'. |
| chx:setsEasierTarget | sets an easier target than | PoolSharesAndFees | HashBelowTarget | the chapter says of Pool shares and fees: 'A pool sets an easier target so that members prove their work with shares'; the chapter says of Hash below target: 'Block 277,316 had to hash below a target'. |
| chx:isShownByReorganization | is carried out in the test by | MajorityAttackLimits | DoubleSpendByReorganization | the chapter says of The limits of a majority attack: 'a majority attacker can double-spend his own transactions'; the chapter says of Double spend by reorganization: 'a competing block with a refund of the same coins was added with one block more of work'. |
| chx:addressesTimeWarp | addresses the time warp attack of | Bip54ConsensusCleanup | Bip94Branch | the chapter says of BIP 54 consensus cleanup: 'proposes to fix the time warp attack'; the chapter says of The BIP 94 branch: 'BIP 94 describes the time warp prevention'. |
| chx:checksMedianTime | checks | BlockChecklist | MedianTimePast | the chapter says of Block checklist: 'a time not after the median'; the chapter says of Median time past: 'The time of a block must be greater than the median of the previous 11 blocks'. |
| chx:checksFutureTime | checks | BlockChecklist | TwoHourRule | the chapter says of Block checklist: 'a time two hours and a second ahead'; the chapter says of Two hour rule: 'A node refuses a block whose time is more than 2 hours'. |
| chx:checksRewardLimit | checks | BlockChecklist | GreedyCoinbaseRejected | the chapter says of Block checklist: 'a reward one satoshi too high'; the chapter says of Greedy coinbase rejected: 'A coinbase that claims one satoshi more than subsidy plus fees makes the block invalid'. |
| chx:checksCoinbaseHeight | checks | BlockChecklist | Bip34HeightPush | the chapter says of Block checklist: 'no height'; the chapter says of BIP 34 height push: 'Since BIP 34 the coinbase script begins with the block height'. |
| chx:usesDifficultyOf | uses the difficulty from | TerahashMinerWait | DifficultyFromTarget | the chapter says of The wait of a terahash miner: 'the difficulty 1,180,923,195 times 2 to the 32 divided by 10 to the 12 gives 58.7 days'; the chapter says of Difficulty from target: 'bits 1903a30c give 1,180,923,195 for block 277,316'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
| SYN-1 X_TerahashMinerWait -> X_DifficultyFromTarget | medium | rejected | The text is right and the relation is set where the model carries it: chx:usesDifficultyOf links the classes The wait of a terahash miner and Difficulty from target. An individual-level link would change the A-Box, which this repair does not touch. |

The rejected rows are the ledger sen0401_ch12_link_decisions_v1_1_0.tsv, in the format of LINK_DECISIONS_v*.tsv.
