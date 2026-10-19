# SEN0401 ch14 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.0 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.0) | 68 | 0 | 4 |
| after (1.1.0) | 68 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 68 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:paysOnSecretOf | pays on the secret whose hash is carried by | HtlcSecretBranch | InvoiceStructure | the chapter says of The HTLC secret branch: 'The hash branch of the HTLC pays whoever shows the secret'; the chapter says of The structure of an invoice: 'the secret released later hashed to the payment hash'. |
| chx:refundsAfterTimelockOf | refunds after a time set by | HtlcTimeoutBranch | TimelockStaircase | the chapter says of The HTLC timeout branch: 'The time branch refunds the payer only after the lock height'; the chapter says of The timelock staircase: 'Every hop must have more time than the next'. |
| chx:isHandBuiltFormOf | is the hand-built form of | FundingNeedsBothKeys | FundingOutputIsMultisig | the chapter says of Funding needs both keys: 'The funding output is a 2-of-2 multisignature script'; the chapter says of The funding output is a multisignature: 'a 2-of-2 multisignature script'. |
| chx:usesRevocationKeyOf | needs the revocation key derived in | RevocationNeedsBothHalves | RevocationKeyVector | the chapter says of Revocation needs both halves: 'The penalty path needs the revocation private key'; the chapter says of The revocation key vector: 'needs both the revocation base secret and the per-commitment secret'. |
| chx:explainsPenaltyOf | explains the penalty taken in | PenaltyTakesEverything | BreachJusticeTransaction | the chapter says of The penalty takes everything: 'if he is caught the honest party takes all 10'; the chapter says of The justice transaction: 'answered with a justice transaction that spent its penalty output'. |
| chx:comparesFeeOf | compares the fee of | BookFeeVersusNetworkFee | FeeArithmetic | the chapter says of The book fee versus the network fee: 'The book's fee of 0.001 per hop'; the chapter says of The fee arithmetic: 'with a fee of 0.001 from each of three intermediaries'. |
| chx:comparesDelayOf | compares the delay of | CsvDelayThousandVersus2016 | AsymmetricCommitment | the chapter says of A delay of 1,000 versus 2016: 'The book's revocable delay is 1,000 blocks'; the chapter says of The asymmetric commitment: 'a branch with 1000 and OP_CHECKSEQUENCEVERIFY'. |
| chx:setsDeltaOf | sets the timelock delta of | LndDefaults | TimelockStaircase | the chapter says of The lnd defaults: 'a timelock delta of 80'; the chapter says of The timelock staircase: 'the delta of 80 blocks that is their default'. |
| chx:advertisesAnchorsOf | advertises the anchors of | LndDefaults | CommitmentTransactionShape | the chapter says of The lnd defaults: 'anchor commitments with zero-fee HTLC transactions'; the chapter says of The shape of a commitment transaction: 'two are anchors of 330 satoshis'. |
| chx:replacesDoubleSpendOf | is shown by the replacement in | FullRbfIsStandard | DoubleSpendRejected | the chapter says of Full RBF is standard: 'the higher-fee replacement of the double spend was accepted'; the chapter says of A double spend is rejected: 'one with a higher fee replaced the first in the node's memory pool'. |
| chx:countsNetworkOf | counts the network the book calls proposed in | LightningNoLongerProposed | MainnetGraphSize | the chapter says of Lightning is no longer proposed: 'The chapter calls the Lightning Network a proposed network'; the chapter says of The size of the public graph: 'The public network that the book calls proposed'. |
| chx:leavesUnrunPublicNetwork | records as not run | WhatWasNotExecuted | MainnetGraphSize | the chapter says of What was not executed: 'the public network'; the chapter says of The size of the public graph: 'The public network that the book calls proposed'. |
| chx:leavesUnrunExpiry | records as not run | WhatWasNotExecuted | HtlcTimeoutBranch | the chapter says of What was not executed: 'an HTLC expiring on the chain'; the chapter says of The HTLC timeout branch: 'The time branch refunds the payer only after the lock height'. |
| chx:closesOnlyOnceLike | closes once like | UtxoIsASingleUseSeal | DoubleSpendRejected | the chapter says of An output is a single-use seal: 'an unspent output is exactly that'; the chapter says of A double spend is rejected: 'No output can be spent twice in one valid chain'. |
| chx:commitsInTransactionLike | commits to data in a transaction like | ContractStaysOffChain | ProofOfExistence | the chapter says of The contract stays off the chain: 'the 69-byte contract was committed in the key tweak'; the chapter says of Proof of existence: 'A proof of existence needs only a commitment in a transaction'. |
| chx:letsPartyKeepLadder | lets a channel party keep the commitments of | NonExpiration | RefundTimelockLadder | the chapter says of A transaction does not expire: 'lets a channel party keep a signed transaction for weeks'; the chapter says of The refund timelock ladder: '30 days at 144 blocks a day are the book's 4,320 blocks'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
