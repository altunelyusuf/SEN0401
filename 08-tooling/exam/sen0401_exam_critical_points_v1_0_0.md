# SEN0401 critical points of the exam chapters, version 1.0.0

Chapters are a parameter: default 1 to 6; chapter 7 is doubtful and selectable.
A point is listed in A only when a source carries it; the source is named. List B is separate.

## A. Points carried by a source

### Chapter 1
- CP1.01 [SUM] Origins: block 0 carries a dated headline, and the first payment went from person to person.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 60, slide)
- CP1.02 [SUM] Money is a ledger; the 21 million cap is arithmetic, and the price is discovered by trades.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 60, slide)
- CP1.03 [SUM] The network has no bank: every node checks every rule and proof of work makes history costly.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 60, slide)
- CP1.04 [SUM] A wallet holds keys, not coins; whoever holds the keys holds the coins.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 60, slide)
- CP1.05 [SUM] A first payment needs an address or invoice, whole coins, change, and a fee for the miner.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 60, slide)
- CP1.06 [EMP] A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 36, notes)
- CP1.07 [EMP] A double spend is refused by a shared rule, and no bank decides.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 33, notes)
- CP1.08 [EMP] The key is both the key and the proof of ownership, so it must prove without being shown.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 42, notes)
- CP1.09 [LES] Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 44, notes)
- CP1.10 [SUM] Two old solved problems joined in 2008: proof of work (Hashcash, 1997) and agreement without trust (Byzantine Generals, 1982).  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 55, slide)
- CP1.11 [EMP] Price is discovered by trades; a day figure is a volume-weighted average.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 23, slide)
- CP1.12 [SUM] Bitcoin is virtual, borderless, decentralized and robust, built from a peer-to-peer protocol, a public journal and a consensus rule set.  (source: SEN0401_Ch01_Introduction_3e_v3_2_0.pptx, slide 59, slide)

### Chapter 2
- CP2.01 [Q] What a payment contains: inputs that spend earlier outputs, outputs for the payee and the change, and a fee.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.02 [Q] Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.03 [Q] How a payment is built: pick coins, write the outputs, leave the fee, sign.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.04 [Q] How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.05 [Q] Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.06 [Q] Consensus rules are checked by every node; block 74,638 broke one.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 33, slide)
- CP2.07 [EMP] The txid is stored in one byte order and printed by explorers in the other; reversing converts between them.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 13, notes)
- CP2.08 [EMP] Blocks have limited room, so miners pick the best fee rates first.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 14, notes)
- CP2.09 [EMP] Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 18, notes)
- CP2.10 [EMP] A higher fee rate leaves less change.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 22, notes)
- CP2.11 [EMP] Only unspent outputs can be spent; wallets and nodes keep exactly that set.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 16, notes)
- CP2.12 [EMP] Mining is a search that nobody can shortcut but anyone can check with one hash.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 25, notes)
- CP2.13 [LES] Block 74,638 (15 August 2010): a value overflow created about 184 billion bitcoin; a rule was shipped within hours and the honest chain won.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 32, notes)
- CP2.14 [EMP] In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.  (source: SEN0401_Ch02_HowBitcoinWorks_3e_v3_0_0.pptx, slide 19, notes)

### Chapter 3
- CP3.01 [Q] Why Bitcoin Core is the reference: it came first, it defines the rules by running them, and it is built in the open.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.02 [Q] A release you trust: check out a final tag, build it, and compare its hash with the published one.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.03 [EMP] Release tags sort by number, not by text; release candidates carry rc.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 11, notes)
- CP3.04 [Q] Settings decide what is stored, how much memory is used, and which alerts run.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.05 [EMP] An option on the command line overrides the configuration file.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 16, notes)
- CP3.06 [EMP] Pruning and the transaction index do not mix: the node refuses both at once.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 19, notes)
- CP3.07 [Q] Asking a node: JSON-RPC calls; the cookie or an rpcauth credential lets you in.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.08 [EMP] rpcauth stores a salted hash, so a leaked configuration file does not reveal the password.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 26, notes)
- CP3.09 [Q] Reading a transaction: decode it; the txid ignores the witness, and weight counts it.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.10 [EMP] Weight units: base bytes count four units each, witness bytes one; 194 bytes weigh 569 units, 143 virtual bytes.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 31, notes)
- CP3.11 [Q] Checking a block: hash the 80-byte header and rebuild the merkle root yourself.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 40, slide)
- CP3.12 [EMP] Block timestamps are guesses; Bitcoin Core uses the median time of the last eleven blocks.  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 36, notes)
- CP3.13 [LES] A reference implementation needs a team and public review, not one keyholder (7 April 2014).  (source: SEN0401_Ch03_BitcoinCore_3e_v3_0_0.pptx, slide 22, notes)
- CP3.14 [OWN25] Option alertnotify: sends emergency alerts to the owner of the node, usually by email.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 25, diagram)
- CP3.15 [OWN25] Option datadir: selects the directory and filesystem for all blockchain data; it needs several gigabytes of free space.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 26, diagram)
- CP3.16 [OWN25] Option prune: reduces the disk space requirement by deleting old blocks.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 27, diagram)
- CP3.17 [OWN25] Option txindex: maintains an index of all transactions, which means a complete copy of the blockchain.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 28, diagram)
- CP3.18 [OWN25] Option maxconnections: the maximum number of nodes to accept connections from; it reduces bandwidth use.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 29, diagram)
- CP3.19 [OWN25] Options maxmempool and maxreceivebuffer/maxsendbuffer: limit the transaction memory pool and the per-connection buffers to reduce memory use.  (source: Chapter_3_BitcoinCore_TheReferenceImplementation_v1_0_0.pptx, slide 30, diagram)

### Chapter 4
- CP4.01 [Q] A private key is a random number between 1 and n - 1 with 256 bits of entropy.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.02 [EMP] A key must come from a proper random source: only 256 fair coin flips match a Bitcoin key.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 10, notes)
- CP4.03 [Q] Public key from private key: multiply G by k with doubling and adding; nobody can run it backwards.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.04 [Q] Legacy address: HASH160, a version byte and four checksum bytes, written in base58.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.05 [EMP] P2PKH holds only a 20-byte hash of the key, a commitment; the key is revealed only when the coins are spent.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 21, notes)
- CP4.06 [Q] What P2SH and Bech32 change: P2SH hashes a script; Bech32 and Bech32m add a version, a program and a stronger checksum.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.07 [EMP] A 160-bit hash gives only 80 bits against collisions, which is why SegWit scripts use SHA256.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 31, notes)
- CP4.08 [EMP] Bech32m closes a weakness of Bech32 (an extra q before a final p keeps the checksum valid).  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 34, notes)
- CP4.09 [Q] WIF: Base58Check of version 80, the key and a final 01 when compressed.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.10 [EMP] One private key gives two public key encodings and so two addresses; coins sent to one are not seen at the other.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 38, notes)
- CP4.11 [Q] A valid address can have no key: a checksum catches typos, not a missing key (the eater address).  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 45, slide)
- CP4.12 [EMP] Vanity addresses: each further letter divides the chance by 58 and the work cannot be shortcut.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 41, notes)
- CP4.13 [EMP] A paper wallet must give back its address before any coins are sent.  (source: SEN0401_Ch04_KeysAndAddresses_3e_v3_4_0.pptx, slide 42, notes)

### Chapter 5
- CP5.01 [EXAM] The deck states that its six Check-yourself questions are the ones the exam will build on.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, notes)
- CP5.02 [EXAM] Why is one seed better than many loose keys? (Code 1)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.03 [EXAM] How many words does 256 bits of entropy make? (Code 5)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.04 [EXAM] What does the checksum protect against? (Code 7)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.05 [EXAM] Why does a passphrase change the wallet? (Code 10)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.06 [EXAM] Why are account levels hardened? (Code 14)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.07 [EXAM] How do you know a backup works? (Code 27)  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 65, slide)
- CP5.08 [SUM] A recovery code is entropy in words: 11 bits a word, checksum included.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 66, slide)
- CP5.09 [SUM] Words become a 512-bit seed by deliberate slowness; a passphrase forks the wallet.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 66, slide)
- CP5.10 [SUM] The HD tree gives every purpose a numbered key; hardened steps protect the parent.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 66, slide)
- CP5.11 [EMP] A forgotten passphrase loses the funds; the same twelve words with another passphrase give a different wallet.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 28, notes)
- CP5.12 [EMP] Where the book differs from the standards: the book's 2,147,483,647 is the largest normal index, not the count of children.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 39, notes)
- CP5.13 [EMP] Where the book differs from the standards: the book's table uses coin type one for BIP49, the testnet type.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 48, notes)
- CP5.14 [EMP] Implicit paths need no record (standard); explicit paths must be written down with the code.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 48, notes)
- CP5.15 [SUM] A complete backup: recovery code, passphrase if used, paths or descriptors, other signers' public keys, labels and protocol data; then restore and check the first address.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 63, slide)
- CP5.16 [EMP] A typo in a recovery code gives no error but a different, empty wallet.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 62, notes)
- CP5.17 [EMP] Labels are not derivable from the seed and need their own backup (BIP329).  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 54, notes)
- CP5.18 [LES] An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 56, notes)
- CP5.19 [LES] Stefan Thomas was paid 7,002 bitcoin in 2011, lost the password and has two guesses left.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 5, notes)
- CP5.20 [EMP] The gap limit decides how far a recovery scan looks.  (source: SEN0401_Ch05_WalletRecovery_3e_v3_4_0.pptx, slide 59, notes)

### Chapter 6
- CP6.01 [SUM] A transaction asks strangers to update their ledgers: inputs point, witnesses prove, outputs assign.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 60, slide)
- CP6.02 [SUM] The sequence field has meant three things, and the lock time is read against the median of eleven blocks.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 60, slide)
- CP6.03 [SUM] An output is an amount and a condition; the fee is a difference, and dust is a policy about everyone's database.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 60, slide)
- CP6.04 [SUM] Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 60, slide)
- CP6.05 [SUM] The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 60, slide)
- CP6.06 [EMP] Two serializations, two identifiers: the legacy hash is the txid, the extended hash is the wtxid.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 9, notes)
- CP6.07 [EMP] Marker and flag: a legacy parser would read the zero marker as an empty input list.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 13, notes)
- CP6.08 [EMP] Byte order of the txid in an outpoint is a classic source of mistakes.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 19, notes)
- CP6.09 [EMP] A spend updates the UTXO set: remove what is spent, add what is created.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 21, slide)
- CP6.10 [EMP] The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 26, notes)
- CP6.11 [EMP] Lock time: values below 500 million are heights, larger ones are times, read against the median time past.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 49, notes)
- CP6.12 [EMP] Dust: an output is dust when it costs more to spend than it is worth, at the relay fee; data-carrier outputs are exempt.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 37, notes)
- CP6.13 [LES] Block 74,638 (15 August 2010): a signed amount needs a range check.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 35, notes)
- CP6.14 [EMP] Segwit changes the witness but keeps the txid; the wtxid still covers the witness.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 42, notes)
- CP6.15 [EMP] Segregated witness was a soft fork: old nodes saw anyone-can-spend scripts and accepted the blocks.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 46, notes)
- CP6.16 [LES] Mt. Gox blamed malleability (10 February 2014) and researchers checked the claim.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 43, notes)
- CP6.17 [EMP] Coinbase coins are locked for 100 blocks so a reorganisation cannot invalidate coins already spent.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 53, notes)
- CP6.18 [EMP] The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 51, notes)
- CP6.19 [EMP] Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 56, notes)
- CP6.20 [EMP] A txid is not a field: it is the double SHA-256 of the legacy serialization, shown in reverse byte order.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 58, notes)
- CP6.21 [EMP] CompactSize counts: up to 252 one byte, then fd, fe or ff announce two, four or eight more bytes.  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 17, notes)
- CP6.22 [LES] The first spend of an output: ten bitcoins to Hal Finney in block 170 (12 January 2009).  (source: SEN0401_Ch06_Transactions_3e_v2_2_0.pptx, slide 10, notes)
- CP6.23 [PAGE] The course page asks, as a discussion item, to select one critical issue from the chapter and explain it.  (source: sen0401_ch06_page_v9_84_0.html)

### Chapter 7 (doubtful)
- CP7.01 [SUM] A coin is locked by a script; the spender's script is the key, and the two run apart on a stack.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 59, slide)
- CP7.02 [SUM] Key hashes, multisignatures and script hashes lock a coin to what the spender can prove and move the long lock to the spender.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 59, slide)
- CP7.03 [SUM] Lock time and sequence make a spend wait, and flow control gives one output several ways out.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 59, slide)
- CP7.04 [SUM] Segregated witness moves the proof out of the identifier, as a soft fork that old nodes accept.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 59, slide)
- CP7.05 [SUM] Taproot commits to a tree of scripts with one key, so agreement looks like a single signature.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 59, slide)
- CP7.06 [LES] The OP_RETURN bug of 2010: run the two scripts separately, and fail closed on anything unknown.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 10, notes)
- CP7.07 [LES] The fork of 4 July 2015 (BIP66, strict DER): a rule that you do not check for yourself protects nobody.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 18, notes)
- CP7.08 [EMP] A 2-of-3 multisignature needs signatures in key order, and the opcode pops one item too many so a dummy must be empty.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 21, notes)
- CP7.09 [EMP] Pay to script hash: the output holds only a hash of the script; the spender reveals the script and nodes hash it and then run it.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 25, notes)
- CP7.10 [EMP] CLTV needs a lock time at least the script's number and a non-final sequence; CSV counts the age of the coin and needs version 2.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 31, notes)
- CP7.11 [EMP] Taproot key path: one 64-byte Schnorr signature and nothing about hidden scripts is revealed.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 52, notes)
- CP7.12 [EMP] Tapscript replaces CHECKMULTISIG with OP_CHECKSIGADD, which counts valid signatures.  (source: SEN0401_Ch07_AuthorizationAuthentication_3e_v2_2_0.pptx, slide 57, notes)

Basis codes: Q = chapter question answered in the summary; SUM = line of the deck summary; LES = lesson line of a true story; EMP = speaker note or slide sets the point apart; EXAM = deck says the exam builds on it; OWN25 = owner's 2025 deck titles it most important; PAGE = course page discussion item

## B. What no source carries (for the owner)

- B1 (chapters all): No source marks which points the owner stressed when he lectured. The decks, speaker notes, pages and corpus carry no stress marker, except chapter 5 slide 65 (exam), the owner's 2025 chapter 3 slides 25-30, and the stories' lesson lines. Every other point in list A is a point the deck itself sets apart (question answered in the summary, summary line, lesson line, emphasis in the note), not a point the sources prove he spoke aloud.  ASKED OF THE OWNER: Name, per chapter, the points you stressed aloud that you want examined; or confirm list A as it stands.
- B2 (chapters 6, 7): Which parts of chapter 6 were actually lectured, and whether chapter 7 is covered: the final chapter list is due on 2026-10-30. List A holds points of chapters 1 to 6 as default and chapter 7 as selectable (marked doubtful).  ASKED OF THE OWNER: Fix the chapter list before each sitting (1 to 6, or 1 to 7).
- B3 (chapters all): Remarks made in class that were not written into any slide, speaker note or page. By definition no source holds them.  ASKED OF THE OWNER: Dictate them if they should be examined.
- B4 (chapters 1, 2): The owner's 2025 decks of chapters 1 and 2 ask students to select and explain one critical issue of the chapter (2025 slide 54 and slide 65); no answer key or list of expected issues exists in any source. The 2025 speaker notes of chapters 1 to 7 hold only dates and web addresses.  ASKED OF THE OWNER: Say which issue(s) per chapter count as critical.
- B5 (chapters all): The 2025 chapter 3 slides 25-30 show the options as a graphic; only the option names and one-line purposes could be read from the diagram data. A search of the 2025 slides of chapters 1 to 7 for the words important, remember, critical, exam, key point, warning found no other importance marker.  ASKED OF THE OWNER: None unless you want 2025 emphasis for other chapters added.
- B6 (chapters all): The book itself. 02-textbook holds only a 10 KB pinned reference (sen0401_textbook_v1_2_0.ttl) to the private repository altunelyusuf/mastering-bitcoin; the text of Mastering Bitcoin, third edition, is not in this repository. Terms were therefore checked against the decks, speaker notes, the 2025 decks and the pages, not against the book text.  ASKED OF THE OWNER: Provide the book text (or the pinned commit) if every term must be checked against it.
- B7 (chapters all): Weights per chapter, number of items, paper size, sitting date and the share of higher-Bloom items are owner-only (excluded from this task).  ASKED OF THE OWNER: Decide them.
- B8 (chapters all): Brief statement not matching the repository: the brief says the decks, the rdodi folders and the bank generators are not found at their paths; the newest decks (03-materials/chNN/*.pptx) and the rdodi folders (03-materials/chNN/rdodi) exist for chapters 1 to 7. Bank generators named sen0401_chNN_bank_gen exist in 08-tooling for chapters 1, 2, 4, 5, 6 and 7 only; for chapters 3 and 8 no such file exists, and the pages of those chapters carry the exam engine (xExamStart), so their items live inside the pages.  ASKED OF THE OWNER: Tell the coordinator whether the chapter 3 items are to be read from the page.
