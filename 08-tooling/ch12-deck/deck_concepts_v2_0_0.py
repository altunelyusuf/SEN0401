"""The key concepts of chapter 12 for the deck 2.0.0 (Mining and Consensus; a NEW file, nothing earlier is edited).
Two lists, kept apart on purpose (disclosed in the build log):
 (1) the concepts of the chapter itself, taken from the chapter taxonomy of the research package (sen0401_ch12_rdodi_data_v1_0_1.py: six parts, fourteen groups, 39 of its leaves with a label),
     each with a one-sentence meaning and one everyday analogy (the owner's rule: every key concept has an everyday comparison);
 (2) the 41 concepts that the research file 03-materials/ch12/rdodi/sen0401_ch12_research_v1_0_1.ttl lists as primary-source concepts, which the deck standard check reads for D4 and D11.
     MEASURED FACT: those 41 labels are the headings and terms of chapter 11 (The Blockchain: block, header, merkle tree, test chains), not of chapter 12. The deck does not edit the research;
     it shows these 41 concepts in a last part, 'From chapter 11', as the ideas on which mining stands (a miner builds a header, commits to a merkle root, writes a height into the coinbase and
     tests on regtest), with the meanings and analogies of the chapter 11 deck 2.0.0, so that both the research file as it stands and the real subject of chapter 12 are covered.
A card reads: the concept, its meaning, then 'Think of ...'. The label is written exactly as in the research (list 2) or as the taxonomy labels it (list 1)."""
__version__ = "2.0.0"

BRANCHES = ["MoneyCreation", "DecentralizedConsensus", "BuildingTheCandidateBlock", "ProofOfWork", "MiningCompetition", "ChangingConsensusRules", "RecapChapter11"]
LAB = {"MoneyCreation": "Money and rewards", "DecentralizedConsensus": "Verifying and agreeing", "BuildingTheCandidateBlock": "Building the block", "ProofOfWork": "Proof of work",
       "MiningCompetition": "Competition and attacks", "ChangingConsensusRules": "Changing the rules", "RecapChapter11": "From chapter 11"}
SHORT = {"MoneyCreation": "Money", "DecentralizedConsensus": "Verify", "BuildingTheCandidateBlock": "Block", "ProofOfWork": "Work", "MiningCompetition": "Rivals",
         "ChangingConsensusRules": "Rules", "RecapChapter11": "Chapter 11"}

L1 = {
    "MoneyCreation": "The reward is a wage that halves on a fixed calendar, plus tips.",
    "DecentralizedConsensus": "Every node is a customs officer who checks each parcel against the same list.",
    "BuildingTheCandidateBlock": "The miner packs a parcel and writes the label before sealing it.",
    "ProofOfWork": "Proof of work is a lottery whose tickets are costly to draw and cheap to check.",
    "MiningCompetition": "Mining is a race of lottery syndicates, and a big syndicate may cheat.",
    "ChangingConsensusRules": "Changing the rules is repainting the road signs while cars still drive.",
    "RecapChapter11": "A miner stands on the block, the header and the test chain of chapter 11.",
}

# groups of a part, in order: (key, pill (at most 4 words), meaning, analogy)
GROUPS = {
    "MoneyCreation": [
        ("SubsidySchedule", "The subsidy schedule", "New coins halve every 210,000 blocks, so the supply stops just below 21 million.", "a wage cut in half on a fixed calendar"),
        ("RewardComposition", "Subsidy plus fees", "A block pays its miner the subsidy plus the fees of its transactions, and no more.", "a salary plus tips"),
    ],
    "DecentralizedConsensus": [
        ("IndependentVerification", "Independent checking", "Every node tests every transaction and block against the same list of rules.", "a customs officer with a printed checklist"),
        ("ChainSelection", "Choosing the chain", "Nodes follow the chain with the most accumulated work, not the one with most blocks.", "the heaviest rope, not the longest"),
    ],
    "BuildingTheCandidateBlock": [
        ("BlockTemplate", "The block template", "A node picks transactions by fee rate up to a weight limit.", "a loader who packs the best-paying parcels first"),
        ("CoinbaseTransaction", "The coinbase", "The first transaction creates the reward and carries the height and a witness commitment.", "the first line of a ledger, with no payer"),
        ("HeaderConstruction", "The header", "Six fields in 80 bytes, with a time that must pass two rules.", "the address label on the parcel"),
    ],
    "ProofOfWork": [
        ("TheLottery", "The nonce lottery", "Try numbers until the hash falls under the target; checking takes one hash.", "rolling dice until a six"),
        ("TargetAndDifficulty", "Target and difficulty", "A four-byte code holds the target; difficulty says how small it is.", "the height of a limbo bar"),
        ("Retargeting", "Retargeting", "Every 2,016 blocks the target is scaled so blocks keep coming every ten minutes.", "a thermostat for the pace of the lottery"),
    ],
    "MiningCompetition": [
        ("NonceSpace", "The nonce space", "Four billion tries are used up at once, so miners vary other fields too.", "a combination lock with too few wheels"),
        ("MiningPools", "Mining pools", "Small miners pool power and share the pay, at the price of trust.", "a lottery syndicate that splits small wins"),
        ("HashrateAttacks", "Hash rate attacks", "A share of the power buys odds of rewriting recent history.", "a runner chasing a leader"),
    ],
    "ChangingConsensusRules": [
        ("HardForks", "Hard forks", "Looser rules split the chain into two histories.", "a road that forks, with no way back"),
        ("SoftForks", "Soft forks", "Stricter rules stay valid for old nodes and are switched on by a vote.", "a stricter door policy"),
    ],
    "RecapChapter11": [
        ("Anatomy", "Block and header", "A block is an 80-byte header with six fields and a list of transactions.", "a parcel with a label on top"),
        ("Merkle", "Merkle trees", "Pairs of hashes are hashed again until one root remains in the header.", "a knockout draw with one winner"),
        ("Testchains", "Test chains", "Testnet, signet and regtest follow Bitcoin's rules with other constants.", "a rehearsal room next to the stage"),
    ],
}

# every key concept: label -> (part, meaning, analogy without 'Think of' and without the closing full stop)
K3 = {
    # ---- part 1: money and rewards
    "Halving every 210,000 blocks": ("MoneyCreation", "the reward is cut in half after every 210,000 blocks, about four years.", "a wage that is halved on every fourth birthday of the system"),
    "Total supply below 21 million": ("MoneyCreation", "all rewards ever paid add up to 2,099,999,997,690,000 satoshis, just short of 21 million coins.", "a mint with a fixed stock of metal that is never topped up"),
    "The float erratum of the book's script": ("MoneyCreation", "the printed script divides with a slash, so Python 3 keeps halving fractions of a satoshi.", "a calculator that keeps cutting a coin into smaller crumbs"),
    "Reward is subsidy plus fees": ("MoneyCreation", "the miner is paid the new coins plus the fees of the included transactions.", "a wage plus tips"),
    "The fees of block 840,000": ("MoneyCreation", "the first block of the 3.125-coin era paid fees twelve times its subsidy.", "a waiter whose tips on a busy night beat the salary"),
    # ---- part 2: verifying and agreeing
    "Transaction checklist": ("DecentralizedConsensus", "each transaction is tested against fixed rules and refused with a named reason.", "a customs officer with a printed checklist"),
    "Block checklist": ("DecentralizedConsensus", "each block must also obey the rules of reward, height, merkle root, time and version.", "an exam paper marked against a model answer"),
    "Coinbase maturity": ("DecentralizedConsensus", "a mining reward can be spent only after 100 confirmations.", "a cheque that clears only after a hundred days"),
    "Most work, not longest": ("DecentralizedConsensus", "nodes follow the chain with the most accumulated work, not the one with the most blocks.", "the heaviest rope, not the longest rope"),
    # ---- part 3: building the candidate block
    "Block template": ("BuildingTheCandidateBlock", "a node offers a template with transactions picked by fee rate, up to a weight limit.", "a loader who packs the best-paying parcels first"),
    "BIP 34 height push": ("BuildingTheCandidateBlock", "the coinbase script starts with the block height, so every coinbase differs.", "the page number written on the first line of each page"),
    "Witness commitment": ("BuildingTheCandidateBlock", "an extra coinbase output commits to the witness data of all transactions.", "a sealed envelope that lists what lies in the second drawer"),
    "The extra nonce changes the root": ("BuildingTheCandidateBlock", "a counter in the coinbase script changes the merkle root and so opens a fresh search space.", "reshuffling the deck before the next draw"),
    "Median time past": ("BuildingTheCandidateBlock", "a block's time must be later than the median of the last eleven blocks.", "a clock that follows the majority, not a single watch"),
    "Two-hour rule": ("BuildingTheCandidateBlock", "a block time more than two hours ahead of a node's clock is refused.", "a rule against post-dated cheques"),
    # ---- part 4: proof of work
    "The Hello World nonce": ("ProofOfWork", "hash a text with a counter added, again and again, until the hash starts with zeros.", "rolling a die until a six turns up"),
    "Proof is cheap to check": ("ProofOfWork", "finding a valid header takes billions of hashes, and checking it takes one.", "a jigsaw piece: hard to find, easy to see that it fits"),
    "Hash below target": ("ProofOfWork", "a header is valid when its hash, read as a number, is not above the target.", "a limbo bar that the hash must pass under"),
    "Compact bits": ("ProofOfWork", "the target is stored in four bytes: one for the size and three for the digits.", "scientific notation for a huge number"),
    "The wait of a terahash miner": ("ProofOfWork", "at the difficulty of block 277,316 a miner doing one terahash a second waited about 59 days.", "one person with a single ticket in a national lottery"),
    "Hash rate from difficulty": ("ProofOfWork", "difficulty times 2 to the 32, over 600 seconds, estimates the hashes a second of the network.", "guessing the size of a crowd from the effort needed to get in"),
    "The 2015-gap retarget": ("ProofOfWork", "2,016 blocks have only 2,015 gaps, and the rule measures the span from the first block to the last.", "counting fence posts and the spaces between them"),
    "The factor-of-four clamp": ("ProofOfWork", "one retarget never moves the target by more than a factor of four either way.", "a speed limiter on the steering wheel"),
    "The BIP 94 branch": ("ProofOfWork", "testnet4 measures the period from its first block, so a late block cannot trick the rule.", "a stopwatch started at the start line"),
    # ---- part 5: competition and attacks
    "The nonce space is tiny": ("MiningCompetition", "32 bits give 4.3 billion tries, which a modern machine uses up in a fraction of a second.", "a padlock with only a few wheels"),
    "Version rolling": ("MiningCompetition", "16 bits of the version field may be changed freely, which multiplies the search space.", "a spare dial on the lock"),
    "Pool shares and fees": ("MiningCompetition", "a pool pays members for easy partial solutions and keeps a fee.", "a lottery syndicate that splits small wins"),
    "Solo miner variance": ("MiningCompetition", "a small miner may wait years for one block, so income is very uneven.", "fishing alone in a very large lake"),
    "Block withholding": ("MiningCompetition", "a pool member who hides a full solution harms the pool and not the member.", "a saboteur on a team who pockets the winning ticket"),
    "Nakamoto's catch-up odds": ("MiningCompetition", "the chance that an attacker catches up falls quickly with the number of blocks behind.", "a runner who starts further behind each time"),
    "The selfish-mining threshold": ("MiningCompetition", "above a share between one quarter and one third, hiding blocks can pay.", "a card player who holds back a winning card"),
    "The limits of a majority attack": ("MiningCompetition", "a majority can rewrite recent history and refuse transactions, but it cannot forge signatures.", "a librarian who may reorder the shelves but cannot forge a book"),
    # ---- part 6: changing the rules
    "A soft fork only tightens": ("ChangingConsensusRules", "the new rules are a subset of the old, so old nodes still accept the new blocks.", "a stricter door policy that the old doorman still accepts"),
    "The minority chain is slow": ("ChangingConsensusRules", "a branch with a small share of the power keeps the old difficulty and runs slowly.", "a bus timetable kept after most buses left"),
    "The chain split of March 2013": ("ChangingConsensusRules", "a large block was valid for new nodes and refused by old ones, and the chain split for hours.", "two dictionaries that disagree on one word"),
    "The Bitcoin Cash fork of 2017": ("ChangingConsensusRules", "a group changed the rules so that its blocks were refused by the old network, and a second coin was born.", "a village that splits in two but keeps one history"),
    "The BIP 9 state machine": ("ChangingConsensusRules", "a deployment moves from defined through started and locked in to active as miners signal.", "a traffic light that changes in a fixed order"),
    "Speedy Trial and taproot": ("ChangingConsensusRules", "a three-month vote that needed 90 percent, then a delay before the new rules began.", "a short referendum with a high bar"),
    "Buried deployments": ("ChangingConsensusRules", "old soft forks are now plain activation heights in the source code.", "a law so old that it is printed in the constitution"),
    # ---- part 7: the 41 concepts of the research file (they are the concepts of chapter 11; see the header)
    'Structure of a Block': ("RecapChapter11", 'an 80-byte header, a count of transactions, then the transactions themselves.', 'a parcel with a label on top, an item count, then the items'),
    'Block Header': ("RecapChapter11", 'six fixed fields in 80 bytes that summarise the whole block.', 'the cover page of a report that lists what follows'),
    'Block Identifiers: Block Header Hash and Block Height': ("RecapChapter11", 'two names for a block: the hash of its header, and its position in the chain.', "a person's fingerprint and their seat number in a queue"),
    'The Genesis Block': ("RecapChapter11", 'block zero, mined on 3 January 2009, has no parent and quotes a newspaper headline.', 'the first page of a diary, with no page before it'),
    'Linking Blocks in the Blockchain': ("RecapChapter11", 'each header holds the hash of its parent, so the blocks form one chain.', 'train carriages, each coupled to the one before'),
    'blockchain': ("RecapChapter11", 'the chain of blocks, each linked to its parent, that every node keeps.', 'layers of a glacier: disturb one and every later layer is disturbed'),
    'parent blocks': ("RecapChapter11", 'the block that a header names as the one before it.', "the parent named on a child's birth certificate"),
    'genesis block': ("RecapChapter11", 'the only block with no parent; its hash is fixed in the software.', 'the founder at the top of a family tree'),
    'child blocks': ("RecapChapter11", 'blocks that name an earlier block as parent; one parent may have several children.', 'two children of one parent, only one of whom carries the family on'),
    'blocks': ("RecapChapter11", 'bundles of transactions with a header, added to the chain about every ten minutes.', 'pages of a ledger, sealed when full'),
    'block header hash': ("RecapChapter11", 'the double SHA-256 of the 80 header bytes: the name of the block.', 'a fingerprint taken from the block and never printed inside it'),
    'block height': ("RecapChapter11", 'the number of blocks between a block and the genesis block.', 'the floors of a building counted from the ground'),
    'Bitcoin Core': ("RecapChapter11", 'the reference software that checks every rule and stores the chain.', 'the rulebook and the referee in one program'),
    'Nakamoto, Satoshi': ("RecapChapter11", 'the pseudonymous creator of Bitcoin, who mined the genesis block and wrote the 2008 paper.', 'an author known only by a pen name'),
    'linking blocks in blockchain': ("RecapChapter11", "each block commits to its parent's hash, so rewriting history means redoing all later work.", 'a wax seal pressed over the seal of the previous letter'),
    'BIP 34': ("RecapChapter11", 'the proposal that puts the block height at the start of every coinbase script.', 'a page number written on the first line of each page'),
    'Bitcoin network': ("RecapChapter11", 'the peer-to-peer system of nodes that relay blocks and transactions.', 'a postal system where every office copies the letters it sees'),
    'Merkle Trees': ("RecapChapter11", 'a tree of hashes: each parent hashes its two children and the top is a single root.', 'a knockout tournament, matched in pairs until one name is left'),
    'Merkle Trees and Lightweight Clients': ("RecapChapter11", 'a light client keeps headers only and asks for a short proof that a transaction is in a block.', 'checking one ledger line against a signed total using subtotals'),
    'binary hash trees': ("RecapChapter11", 'every node has two children, so a tree over many leaves is only a few levels deep.', 'a sports bracket folded in pairs'),
    'balanced merkle trees': ("RecapChapter11", 'an odd level is padded by repeating its last hash, so every level pairs up.', 'a lone dancer given a mirror image as partner'),
    'authentication path': ("RecapChapter11", 'the sibling hashes from a leaf up to the root; with them anyone can recompute the root.', 'the receipts that prove one subtotal belongs in the grand total'),
    'merkle path': ("RecapChapter11", 'another name for the authentication path: one sibling hash for each level.', 'directions that list each turn on the way up a staircase'),
    'lightweight clients': ("RecapChapter11", 'wallets that download headers only and verify transactions with merkle proofs.', 'a reader who keeps the table of contents, not the whole book'),
    "Bitcoin's Test Blockchains": ("RecapChapter11", "separate chains with Bitcoin's rules and worthless coins, for experiments.", 'a flight simulator, a training pitch and the match: same rules, different stakes'),
    "Testnet: Bitcoin's Testing Playground": ("RecapChapter11", 'a public test chain whose coins have no value.', 'a sandpit in a park, where castles may be knocked down'),
    'Using testnet': ("RecapChapter11", 'point a wallet or node at testnet and take free coins from a faucet.', 'practising with play money'),
    'Problems with testnet': ("RecapChapter11", 'its minimum-difficulty rule let miners flood it with blocks, so testnet4 replaced it.', 'a sandpit that nobody tidies'),
    'Signet: The Proof of Authority Testnet': ("RecapChapter11", 'a test chain whose blocks need a signature from a trusted signer.', 'a club with a doorman who knows the guests'),
    'The default signet and custom signets': ("RecapChapter11", 'one public signet is maintained, and anyone can start another with their own challenge.', 'a public park and a private garden with your own gate'),
    'Regtest: The Local Blockchain': ("RecapChapter11", 'a private chain on your own computer where blocks are mined on demand.', 'a private rehearsal room that only you can enter'),
    'Using Test Blockchains for Development': ("RecapChapter11", 'build on regtest, try on signet or testnet, release on mainnet.', 'rehearsal, dress rehearsal and opening night'),
    'test blockchains': ("RecapChapter11", "chains that follow Bitcoin's rules with different constants.", 'a model railway with the same signals as the real one'),
    'testnet': ("RecapChapter11", 'the public test chain; the current one is testnet4.', 'a sandpit for trying things'),
    'signet': ("RecapChapter11", 'a test chain where each block must carry a valid signature.', 'a doorman who checks every guest'),
    'default signet': ("RecapChapter11", 'the public signet that most developers share.', 'the village green that everyone may use'),
    'custom signets': ("RecapChapter11", 'signets you create by choosing your own challenge script.', "a members' club with your own guest list"),
    'challenge script': ("RecapChapter11", "the script that a signet block's signature must satisfy.", 'the password that the doorman checks'),
    'regtest': ("RecapChapter11", 'regression-test mode: a private chain with trivial difficulty.', 'a rehearsal room with the lights already on'),
    'BIP 325': ("RecapChapter11", 'the proposal that defines signet.', "the club's written rules"),
    'mainnet': ("RecapChapter11", 'the real Bitcoin chain, where coins have value.', 'the match itself, with real stakes'),
}
