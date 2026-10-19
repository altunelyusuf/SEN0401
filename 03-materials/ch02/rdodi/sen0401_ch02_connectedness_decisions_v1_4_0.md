# SEN0401 ch02 - connectedness and link decisions for the domain T-Box 1.4.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.3.0 is untouched; 1.4.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.3.0) | 101 | 0 | 4 |
| after (1.4.0) | 101 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 101 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:aggregatesTransactions | aggregates | Block | Transaction | the chapter says of Block: 'A block is a container that aggregates transactions'. |
| chx:includesFees | includes the fees | BlockReward | TransactionFee | the chapter says of Block reward: 'The reward is the subsidy of new bitcoins plus the fees'. |
| chx:isConfirmedBy | is confirmed by | Transaction | Confirmation | the chapter says of Confirmation: 'A transaction has one confirmation when it is in a block, and one more for each block built on top'. |
| chx:spendsOutputTwice | tries to spend twice | DoubleSpend | Output | the chapter says of Double spend: 'A double spend is the attempt to spend one output in two transactions'. |
| chx:holdsMerkleRoot | holds the root of | BlockHeader | MerkleTree | the chapter says of Merkle tree: 'the block header holds the root'. |
| chx:verifiesBy | verifies by | LightweightClient | PaymentVerification | the chapter says of Lightweight client: 'so it verifies a payment only partly; this is simplified payment verification'. |
| chx:buildsFromMempool | is built from | CandidateBlock | Mempool | the chapter says of Memory pool: 'miners build candidate blocks from it'. |
| chx:holdsUnconfirmed | holds | Mempool | UnconfirmedTransaction | the chapter says of Memory pool: 'The memory pool is the list of verified but unconfirmed transactions that a node keeps in memory'. |
| chx:propagatesTransaction | spreads | TransactionPropagation | Transaction | the chapter says of Transaction propagation: 'Transaction propagation is the spread of a signed transaction across the network by gossip'. |
| chx:keepsUtxoSet | keeps the set of | FullNode | UnspentOutput | the chapter says of Unspent transaction output: 'full nodes keep the set of all of them'. |
| chx:showsHash | shows | HashDemo | HashFunction | the chapter says of Hash page: 'shows a data box and its SHA-256 digest, recomputed at every keystroke'. |
| chx:showsProofOfWork | shows | BlockDemo | ProofOfWork | the chapter says of Block page: 'so that the asymmetry of proof of work can be felt'. |
| chx:showsBlockLinking | shows | BlockchainDemo | Blockchain | the chapter says of Blockchain page: 'links five blocks by a previous-hash field'. |
| chx:showsPeers | shows | DistributedDemo | PeerToPeerNetwork | the chapter says of Distributed page: 'gives three peers, A, B and C, each a full copy of the five-block chain'. |
| chx:showsCoinbase | shows | CoinbaseDemo | CoinbaseTransaction | the chapter says of Coinbase page: 'adds a coinbase line and transaction rows to every block of every peer'. |
| chx:describesTransactionChain | describes | ProvenanceGraph | TransactionChain | the chapter says of Provenance graph: 'The chapter's transaction chain is a provenance graph'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
