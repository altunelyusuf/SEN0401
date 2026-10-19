from spec_common import *
PROPS = [
 P("aggregatesTransactions", "aggregates", "Block", "Transaction", "A block aggregates transactions", ("Block", "A block is a container that aggregates transactions")),
 P("includesFees", "includes the fees", "BlockReward", "TransactionFee", "The block reward is the subsidy plus the transaction fees", ("Block reward", "The reward is the subsidy of new bitcoins plus the fees")),
 P("isConfirmedBy", "is confirmed by", "Transaction", "Confirmation", "A transaction gains a confirmation when it is in a block and one more for each block built on it", ("Confirmation", "A transaction has one confirmation when it is in a block, and one more for each block built on top")),
 P("spendsOutputTwice", "tries to spend twice", "DoubleSpend", "Output", "A double spend is the attempt to spend one output in two transactions", ("Double spend", "A double spend is the attempt to spend one output in two transactions")),
 P("holdsMerkleRoot", "holds the root of", "BlockHeader", "MerkleTree", "The block header holds the merkle root", ("Merkle tree", "the block header holds the root")),
 P("verifiesBy", "verifies by", "LightweightClient", "PaymentVerification", "A lightweight client verifies a payment by simplified payment verification", ("Lightweight client", "so it verifies a payment only partly; this is simplified payment verification")),
 P("buildsFromMempool", "is built from", "CandidateBlock", "Mempool", "Miners build candidate blocks from the memory pool", ("Memory pool", "miners build candidate blocks from it")),
 P("holdsUnconfirmed", "holds", "Mempool", "UnconfirmedTransaction", "The memory pool holds the verified but unconfirmed transactions", ("Memory pool", "The memory pool is the list of verified but unconfirmed transactions that a node keeps in memory")),
 P("propagatesTransaction", "spreads", "TransactionPropagation", "Transaction", "Propagation is the spread of a signed transaction across the network", ("Transaction propagation", "Transaction propagation is the spread of a signed transaction across the network by gossip")),
 P("keepsUtxoSet", "keeps the set of", "FullNode", "UnspentOutput", "Full nodes keep the set of all unspent outputs", ("Unspent transaction output", "full nodes keep the set of all of them")),
 P("showsHash", "shows", "HashDemo", "HashFunction", "The first demonstration page shows a hash recomputed at every keystroke", ("Hash page", "shows a data box and its SHA-256 digest, recomputed at every keystroke")),
 P("showsProofOfWork", "shows", "BlockDemo", "ProofOfWork", "The second demonstration page lets the reader feel the asymmetry of proof of work", ("Block page", "so that the asymmetry of proof of work can be felt")),
 P("showsBlockLinking", "shows", "BlockchainDemo", "Blockchain", "The third demonstration page links blocks by a previous-hash field", ("Blockchain page", "links five blocks by a previous-hash field")),
 P("showsPeers", "shows", "DistributedDemo", "PeerToPeerNetwork", "The fourth demonstration page gives three peers each a full copy of the chain", ("Distributed page", "gives three peers, A, B and C, each a full copy of the five-block chain")),
 P("showsCoinbase", "shows", "CoinbaseDemo", "CoinbaseTransaction", "The last demonstration page adds a coinbase line to every block", ("Coinbase page", "adds a coinbase line and transaction rows to every block of every peer")),
 P("describesTransactionChain", "describes", "ProvenanceGraph", "TransactionChain", "The chapter's transaction chain is a provenance graph", ("Provenance graph", "The chapter's transaction chain is a provenance graph")),
]
