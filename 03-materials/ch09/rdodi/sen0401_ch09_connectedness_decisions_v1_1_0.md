# SEN0401 ch09 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.1 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.1) | 96 | 0 | 6 |
| after (1.1.0) | 96 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 96 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:isPackagedAs | is part of the package | FeePaidInAnotherTransaction | PackageFeeRate | the chapter says of Fee paid in another transaction: 'the parent paid 141 satoshis, its child 14,100, and the node mined both together in one block'; the chapter says of Package fee rate: 'A parent paying 141 satoshis and a child paying 14,100 form a package of 14,241 satoshis'. |
| chx:guardsAgainstForgottenChange | refuses | AbsurdFeeGuard | ForgottenChangeBecomesFee | the chapter says of Absurd fee guard: 'the forgotten-change transaction paid 17,272,727 satoshis per virtual byte and was refused'; the chapter says of Forgotten change becomes fee: 'The node refuses the transaction that forgot its change with the reason max-fee-exceeded'. |
| chx:ranksByFeeRate | ranks by | FeeIsABid | FeeRateDefinition | the chapter says of A fee is a bid: 'listed them from the highest fee rate'; the chapter says of Fee rate definition: 'The fee rate is the fee divided by the size'. |
| chx:extendsRankingByAncestors | extends the ranking of | AncestorFeerateMining | FeeIsABid | the chapter says of Ancestor feerate mining: 'miners rank transactions with their unconfirmed ancestors'; the chapter says of A fee is a bid: 'listed them from the highest fee rate'. |
| chx:usesSubsidyOfEra | uses the subsidy of | CoinbaseIsExcluded | SubsidyHalvings | the chapter says of Coinbase is excluded: 'equals the subsidy of 312,500,000'; the chapter says of Subsidy halvings: '312,500,000 from it'. |
| chx:answersEstimateSmartFee | converts the answer of | UnitsOfFeeRate | EstimateSmartFeeCall | the chapter says of Units of fee rate: 'estimatesmartfee answer 0.00006570 bitcoin per kilo-virtual-byte is exactly 6.57 satoshis per virtual byte'; the chapter says of The estimatesmartfee call: 'it answered 1.225 satoshis per virtual byte for 2 blocks'. |
| chx:isCensusedWithSignals | is counted in the same sample as | SignalInTheWild | BlockFeeCensus | the chapter says of Signal in the wild: 'In the first 599 transactions after the coinbase'; the chapter says of Block fee census: 'Of the first 599 transactions after the coinbase'. |
| chx:isCensusedWithLockTimes | is counted in the same sample as | MainnetPrevHeightShare | BlockFeeCensus | the chapter says of Share of mainnet transactions with the previous height: 'of the first 599 transactions of block 840,000'; the chapter says of Block fee census: 'Of the first 599 transactions after the coinbase'. |
| chx:boundsLargeChildPin | bounds | TrucPinningBound | LargeChildPin | the chapter says of TRUC pinning bound: '88 times less than the 450,780 of the unrestricted pin'; the chapter says of Large child pin: 'in the run a 90,012-byte child raised the price of replacing'. |
| chx:failsMinimumRelay | was refused for | MinimumRelayProblem | MinRelayFee | the chapter says of The minimum relay problem: 'was refused alone with min relay fee not met'; the chapter says of Minimum relay fee: 'the node refused 8 and 14 with min relay fee not met, and accepted 15'. |
| chx:appliesFeeRate | is a fee rate by | PackageFeeRate | FeeRateDefinition | the chapter says of Package fee rate: 'form a package of 14,241 satoshis over 280.5 virtual bytes'; the chapter says of Fee rate definition: 'The fee rate is the fee divided by the size'. |
| chx:replacesDescendantLimits | was removed because of | CarveOutRemoved | ClusterLimits | the chapter says of Carve out removed: 'because the cluster limits replaced the descendant limits it worked around'. |
| chx:exceedsAncestorLimits | goes beyond | CarveOutRule | RemovedAncestorLimits | the chapter says of Carve out rule: 'beyond the 25-descendant and 101,000-byte limits'; the chapter says of Removed ancestor limits: 'The old limits of 25 ancestors or descendants and 101,000 virtual bytes are gone in release 31.0'. |
| chx:letsParentPayNothing | lets the parent pay nothing in | EphemeralDust | OneParentOneChild | the chapter says of Ephemeral dust: 'the zero-fee parent was refused alone and mined with its child'; the chapter says of One parent one child: 'lets the parent of such a one-parent-one-child package pay nothing'. |
| chx:bumpsByChildPaysForParent | lets a side fee bump by | LightningAnchorOutputs | ChildPaysForParent | the chapter says of Lightning anchor outputs: 'so either side can fee bump by child pays for parent'. |
| chx:sizesDustOfAnchor | has a dust threshold for | DustThreshold | PayToAnchor | the chapter says of Dust threshold: '294 satoshis for P2WPKH, 330 for P2WSH and 240 for pay-to-anchor'; the chapter says of Pay to anchor (P2A): 'anyone can spend it'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
