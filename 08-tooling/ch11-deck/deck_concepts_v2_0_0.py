"""The key concepts of chapter 11 for the deck 2.0.0: the 41 distinct primary-source concepts of the chapter research (03-materials/ch11/rdodi/sen0401_ch11_research_v1_1_0.ttl, de-duplicated by
normalised label, as the deck standard check reads them), each with the part of the chapter it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line
meaning and analogy of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept, its meaning, then 'Think of ...'. The label is written exactly as in the
research. NEW file; nothing earlier is edited."""
__version__ = "2.0.0"

BRANCHES = ["BlockAndChain", "MerkleTrees", "TestChains"]
LAB = {"BlockAndChain": "The block and the chain", "MerkleTrees": "Merkle trees", "TestChains": "Test blockchains"}
SHORT = {"BlockAndChain": "Block and chain", "MerkleTrees": "Merkle trees", "TestChains": "Test chains"}

L1 = {
    "BlockAndChain": "A chain is a train: every carriage is coupled to the one before it.",
    "MerkleTrees": "A merkle tree is a knockout draw that ends with one winner, the root.",
    "TestChains": "A test chain is a rehearsal room: same stage, no real audience.",
}

# groups of a part, in order: (key, pill (at most 4 words), meaning, analogy)
GROUPS = {
    "BlockAndChain": [
        ("Anatomy", "Anatomy of a block", "A block is an 80-byte header with six fields and a list of transactions.", "a parcel with a label on top, an item count, then the items"),
        ("Names", "Hash, height, genesis", "A block has a name, the hash of its header, and a position, its height.", "a fingerprint and a seat number"),
        ("Links", "Links and forks", "Each header names its parent, so changing one block breaks every later link.", "train carriages coupled one behind the other"),
    ],
    "MerkleTrees": [
        ("Tree", "The tree of hashes", "Pairs of hashes are hashed again until one root remains in the header.", "a knockout draw with one winner at the top"),
        ("Proof", "Short proofs", "A path of sibling hashes proves one transaction without the whole block.", "subtotals that prove one line of a ledger"),
        ("Weak", "Weaknesses", "Repeating the last hash can make two lists share one root.", "a lone dancer paired with their own mirror image"),
    ],
    "TestChains": [
        ("Family", "Five chains", "Mainnet and four test chains share one code base with different constants.", "five stages built to one plan with different props"),
        ("Testnet", "Testnet", "A public test chain with worthless coins and a minimum-difficulty rule.", "a sandpit in a park where castles may be knocked down"),
        ("SignetRegtest", "Signet and regtest", "Signet needs a signature for each block; regtest is private and mined on demand.", "a club with a doorman, and a private rehearsal room"),
    ],
}

# every key concept: label as in the research -> (part, meaning, analogy without 'Think of' and without the closing full stop)
K3 = {
    # ---- part A: the block and the chain
    "Structure of a Block": ("BlockAndChain", "an 80-byte header, a count of transactions, then the transactions themselves.", "a parcel with a label on top, an item count, then the items"),
    "Block Header": ("BlockAndChain", "six fixed fields in 80 bytes that summarise the whole block.", "the cover page of a report that lists what follows"),
    "Block Identifiers: Block Header Hash and Block Height": ("BlockAndChain", "two names for a block: the hash of its header, and its position in the chain.", "a person's fingerprint and their seat number in a queue"),
    "The Genesis Block": ("BlockAndChain", "block zero, mined on 3 January 2009, has no parent and quotes a newspaper headline.", "the first page of a diary, with no page before it"),
    "Linking Blocks in the Blockchain": ("BlockAndChain", "each header holds the hash of its parent, so the blocks form one chain.", "train carriages, each coupled to the one before"),
    "blockchain": ("BlockAndChain", "the chain of blocks, each linked to its parent, that every node keeps.", "layers of a glacier: disturb one and every later layer is disturbed"),
    "parent blocks": ("BlockAndChain", "the block that a header names as the one before it.", "the parent named on a child's birth certificate"),
    "genesis block": ("BlockAndChain", "the only block with no parent; its hash is fixed in the software.", "the founder at the top of a family tree"),
    "child blocks": ("BlockAndChain", "blocks that name an earlier block as parent; one parent may have several children.", "two children of one parent, only one of whom carries the family on"),
    "blocks": ("BlockAndChain", "bundles of transactions with a header, added to the chain about every ten minutes.", "pages of a ledger, sealed when full"),
    "block header hash": ("BlockAndChain", "the double SHA-256 of the 80 header bytes: the name of the block.", "a fingerprint taken from the block and never printed inside it"),
    "block height": ("BlockAndChain", "the number of blocks between a block and the genesis block.", "the floors of a building counted from the ground"),
    "Bitcoin Core": ("BlockAndChain", "the reference software that checks every rule and stores the chain.", "the rulebook and the referee in one program"),
    "Nakamoto, Satoshi": ("BlockAndChain", "the pseudonymous creator of Bitcoin, who mined the genesis block and wrote the 2008 paper.", "an author known only by a pen name"),
    "linking blocks in blockchain": ("BlockAndChain", "each block commits to its parent's hash, so rewriting history means redoing all later work.", "a wax seal pressed over the seal of the previous letter"),
    "BIP 34": ("BlockAndChain", "the proposal that puts the block height at the start of every coinbase script.", "a page number written on the first line of each page"),
    "Bitcoin network": ("BlockAndChain", "the peer-to-peer system of nodes that relay blocks and transactions.", "a postal system where every office copies the letters it sees"),
    # ---- part B: merkle trees
    "Merkle Trees": ("MerkleTrees", "a tree of hashes: each parent hashes its two children and the top is a single root.", "a knockout tournament, matched in pairs until one name is left"),
    "Merkle Trees and Lightweight Clients": ("MerkleTrees", "a light client keeps headers only and asks for a short proof that a transaction is in a block.", "checking one ledger line against a signed total using subtotals"),
    "binary hash trees": ("MerkleTrees", "every node has two children, so a tree over many leaves is only a few levels deep.", "a sports bracket folded in pairs"),
    "balanced merkle trees": ("MerkleTrees", "an odd level is padded by repeating its last hash, so every level pairs up.", "a lone dancer given a mirror image as partner"),
    "authentication path": ("MerkleTrees", "the sibling hashes from a leaf up to the root; with them anyone can recompute the root.", "the receipts that prove one subtotal belongs in the grand total"),
    "merkle path": ("MerkleTrees", "another name for the authentication path: one sibling hash for each level.", "directions that list each turn on the way up a staircase"),
    "lightweight clients": ("MerkleTrees", "wallets that download headers only and verify transactions with merkle proofs.", "a reader who keeps the table of contents, not the whole book"),
    # ---- part C: test blockchains
    "Bitcoin's Test Blockchains": ("TestChains", "separate chains with Bitcoin's rules and worthless coins, for experiments.", "a flight simulator, a training pitch and the match: same rules, different stakes"),
    "Testnet: Bitcoin's Testing Playground": ("TestChains", "a public test chain whose coins have no value.", "a sandpit in a park, where castles may be knocked down"),
    "Using testnet": ("TestChains", "point a wallet or node at testnet and take free coins from a faucet.", "practising with play money"),
    "Problems with testnet": ("TestChains", "its minimum-difficulty rule let miners flood it with blocks, so testnet4 replaced it.", "a sandpit that nobody tidies"),
    "Signet: The Proof of Authority Testnet": ("TestChains", "a test chain whose blocks need a signature from a trusted signer.", "a club with a doorman who knows the guests"),
    "The default signet and custom signets": ("TestChains", "one public signet is maintained, and anyone can start another with their own challenge.", "a public park and a private garden with your own gate"),
    "Regtest: The Local Blockchain": ("TestChains", "a private chain on your own computer where blocks are mined on demand.", "a private rehearsal room that only you can enter"),
    "Using Test Blockchains for Development": ("TestChains", "build on regtest, try on signet or testnet, release on mainnet.", "rehearsal, dress rehearsal and opening night"),
    "test blockchains": ("TestChains", "chains that follow Bitcoin's rules with different constants.", "a model railway with the same signals as the real one"),
    "testnet": ("TestChains", "the public test chain; the current one is testnet4.", "a sandpit for trying things"),
    "signet": ("TestChains", "a test chain where each block must carry a valid signature.", "a doorman who checks every guest"),
    "default signet": ("TestChains", "the public signet that most developers share.", "the village green that everyone may use"),
    "custom signets": ("TestChains", "signets you create by choosing your own challenge script.", "a members' club with your own guest list"),
    "challenge script": ("TestChains", "the script that a signet block's signature must satisfy.", "the password that the doorman checks"),
    "regtest": ("TestChains", "regression-test mode: a private chain with trivial difficulty.", "a rehearsal room with the lights already on"),
    "BIP 325": ("TestChains", "the proposal that defines signet.", "the club's written rules"),
    "mainnet": ("TestChains", "the real Bitcoin chain, where coins have value.", "the match itself, with real stakes"),
}
