# SEN0401 midterm: analysis of the items v1.3.0 for the owner (second edition, with points G to P)

Written for you to read, not to decide. Nothing here drops or changes an item. Each row says what an item tests, which important points of the chapters (critical points, CP) it holds and which of your topics it touches. Your topics: T1 to T9 are the first list (T1 serverless peer-to-peer, T2 distributed trust, T3 double-spending prevention, T4 independent confirmations, T5 approval without private keys, T6 genuine against fake transaction, T7 timing differences in spending, T8 why seed words replaced random keys, T9 borderless nature). A to F are the six added points of 21:23, and G to P are the ten added points of 21:49 (G coinbase amounts, H the first spend and the pizza, I hash capacity, ten-minute rule, price and pools, J choice by fee per size, K why digital money failed, L old currencies, M lost keys, N input and output scripts, O who confirms and fake transactions, P the 51 percent attack). A to F are the six added points (A inputs against outputs and fee, B block reward by height, C coins minted by miners, D blocks link to the previous block, E hash search and difficulty target, F the 10-minute rule and soft forks).

How to read the numbers: the paper has 4 questions of 25 points and a hand-marked bonus of 10. There are 21 items; they give 24 machine-read units (sub-questions) because items i07, i15 and i23 fill two sub-questions each, and 2 bonus prompts that you mark by hand.

## 1. All items of the exam

| Item | Chapter | Sub-question (points) | What it tests, in plain words | Critical points it holds | Your topics it touches |
|---|---|---|---|---|---|
| i01 | 1, 5 | Q1.b (4) | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09, CP5.18, CP1.04 | none |
| i02 | 1, 2 | Q1.a (3) | Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee. | CP1.06, CP2.02, CP2.14, CP2.09, CP2.10, CP2.03 | A |
| i03 | 1, 6 | Q2.b (3) | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP1.02, CP6.18, CP6.05 | B |
| i04 | 1 | Q2.h (3) | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11, CP1.02 | none |
| i05 | 2 | Q1.d (4) | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 | T4 |
| i06 | 2 | Q3.a (8) | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | CP2.01, CP2.11 | T7, C |
| i07 | 2, 6 | Q4.a (4), Q4.b (4) | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.01, CP2.04, CP2.11, CP6.09 | T7, C |
| i09 | 3 | Q1.c (3) | Which setting a Bitcoin node really uses when the command line and the configuration file disagree. | CP3.05, CP3.06 | none |
| i10 | 3 | Q3.b (8) | Match each node setting (pruning, index, connections and similar) to the need it serves. | CP3.14, CP3.16, CP3.17, CP3.18 | none |
| i11 | 3 | Q2.e (3) | Why release tags must be sorted by version number, not as text, shown by a small program. | CP3.03 | none |
| i12 | 3, 4 | Q1.f (4) | Why both the node password setting and the older address keep a hash instead of the secret. | CP3.08, CP4.05 | none |
| i13 | 4 | Q2.a (3) | Why every extra letter of a vanity address makes the search 58 times harder. | CP4.12 | none |
| i14 | 4, 5 | Q1.e (4) | Why a backup key in the wrong form shows a zero balance and what the paper wallet must give back. | CP4.09, CP4.10, CP4.13, CP5.07 | none |
| i15 | 4 | Q4.c (4), Q4.d (4) | Why the older address hides the key behind a hash (a commitment) and why newer scripts use a longer hash. | CP4.05, CP4.07 | none |
| i17 | 5 | Q2.f (3) | How long a recovery code is, from the bits each word carries and the checksum. | CP5.03, CP5.08 | T8 |
| i18 | 5, 2, 3, 6 | Q3.c (9) | Match each short real story (a lost password, a block that created coins from nothing, and so on) to the lesson it teaches. | CP5.19, CP6.13, CP2.13, CP3.13, CP6.16 | T6 |
| i19 | 5 | Q2.g (4) | How far a recovery scan looks before it stops (the gap limit), shown by a small program. | CP5.20 | T8 |
| i20 | 5 | Q1.g (3) | Why a phone restored from the words alone shows other addresses and no labels: the passphrase and labels matter. | CP5.05, CP5.11, CP5.17, CP5.15, CP5.09 | T8 |
| i21 | 6 | Q2.c (3) | How a count is written in few bytes (CompactSize), shown by a small program at the edges. | CP6.21 | none |
| i22 | 6 | Q2.d (3) | Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program. | CP6.10, CP6.02 | T7 |
| i23 | 6, 3 | Q4.e (5), Q4.f (4) | Why a payment tracker can rely on the transaction identifier after the witness change, and why witness bytes make a payment cheaper. | CP6.14, CP6.04, CP3.09, CP6.19 | none |
| b1 | 1 | Q5.a (5) | Bonus, written by hand: who refuses a double spend when no bank stands in the middle, and why that makes history costly to change. | CP1.03, CP1.07 | T1 (half), T2 (half), T3 |
| b2 | 2 | Q5.b (5) | Bonus, written by hand: why mining is a search nobody can shortcut, yet every node can check a block easily. | CP2.12 | E (half) |

Count by chapter (an item with two chapters counts under its first): chapter 1: i01, i02, i03, i04 (4); chapter 2: i05, i06, i07 (3); chapter 3: i09, i10, i11, i12 (4); chapter 4: i13, i14, i15 (3); chapter 5: i17, i18, i19, i20 (4); chapter 6: i21, i22, i23 (3).

## 2. What your topics have today

| Topic | Today | Items |
|---|---|---|
| T1 serverless peer-to-peer | not asked by the machine-read items | only half of bonus b1 |
| T2 distributed trust | not asked | only half of bonus b1 |
| T3 double-spending prevention | not asked by the machine-read items | bonus b1 by hand |
| T4 independent confirmations | asked | i05 |
| T5 approval without private keys | not asked | none |
| T6 genuine against fake transaction | partly | i18 (one story: a range check refuses a bad amount) |
| T7 timing differences in spending | partly (my reading: order and moment of spending) | i06, i07, i22 |
| T8 why seed words replaced random keys | partly: the words are used, the reason is not asked | i20, i17, i19 |
| T9 borderless | not asked | none |
| A inputs against outputs and fee | asked | i02 |
| B block reward by height | asked, but not the end of halving at one satoshi and not that the names satoshi and bitcoin are not on the chain | i03 |
| C coins minted by miners, inputs back to a coinbase | asked | i06 (and i07) |
| D block links to the previous block | not asked | none |
| E hash trials, difficulty target, adjustment | not asked; only the 'nobody can shortcut' half in bonus b2 | bonus b2 |
| F ten-minute rule and soft forks | not asked; soft fork appears only inside i23 | i23 (a side mention) |
| G Coinbase amount, reward by block number, minting end, first blocks, totals | PARTIAL: i03 asks the reward by height with the halving interval and the fees, and a claim that is too large; NOT asked: the first blocks' amounts, the total over a halving era, the coinbase after minting ends (fees only) | i03 (and i02 for the fee) |
| H First spend and the pizza | GAP: no item asks it | none |
| I Hash capacity, the 10-minute rule and price; pools | GAP for the machine-read items; only the half 'nobody can shortcut the search' sits in the hand-marked bonus b2 | bonus b2 (half) |
| J Choice of transactions by fee per size | PARTIAL: i02 asks the fee as the difference of inputs and outputs, i23 asks the weight that makes witness bytes cheaper; NOT asked: that miners choose by fee per size (CP2.08) | i02, i23 |
| K Why digital money failed before Bitcoin | GAP for the machine-read items; the double-spend half sits in the hand-marked bonus b1 | bonus b1 (half) |
| L Why old currencies are no longer used (Ottoman, TL and YTL) | GAP: no critical point or deck slide carries it; it is your own material and the items would be new text with synthetic data | none |
| M Losing access to private keys; best practices | PARTIAL: i18 (a lost password story), i01 (an untested backup), i20 (what a full backup holds) touch it; NOT asked as the list of best practices | i01, i18, i20 |
| N Why an input cannot carry its own confirmation; locking and unlocking scripts | GAP: the decks name the lock of an output but no item asks why both scripts must run together; the nearest points are CP6.01 (no holder) and CP4.05 (i12, i15) | none (i12 and i15 touch hashes in locks) |
| O Who confirms; fake transactions and blocks | PARTIAL: i18 (a range check refuses an invalid amount), i05 (confirmations) and bonus b1 (every node checks) touch it; NOT asked: how a fake source is met | i05, i18, bonus b1 |
| P The 51 percent rule and the attack | PARTIAL: i05 asks the chance that an attacker with a share of the hash power catches up and how many confirmations protect; NOT asked: the 51 percent rule itself | i05 |

## 3. The critical points that each item alone holds

If you drop an item, these important points would have no other item that asks about them (bonus prompts count as holders; they are marked by hand).

| Item | Critical points held by this item alone | Critical points it shares with other items |
|---|---|---|
| i01 | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) | none |
| i02 | CP1.06 (A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.); CP2.02 (Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.); CP2.14 (In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.); CP2.09 (Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.); CP2.10 (A higher fee rate leaves less change.); CP2.03 (How a payment is built: pick coins, write the outputs, leave the fee, sign.) | none |
| i03 | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) | CP1.02 |
| i04 | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) | CP1.02 |
| i05 | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) | none |
| i06 | none | CP2.01, CP2.11 |
| i07 | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) | CP2.01, CP2.11 |
| i09 | CP3.05 (An option on the command line overrides the configuration file.); CP3.06 (Pruning and the transaction index do not mix: the node refuses both at once.) | none |
| i10 | CP3.14 (Option alertnotify: sends emergency alerts to the owner of the node, usually by email.); CP3.16 (Option prune: reduces the disk space requirement by deleting old blocks.); CP3.17 (Option txindex: maintains an index of all transactions, which means a complete copy of the blockchain.); CP3.18 (Option maxconnections: the maximum number of nodes to accept connections from; it reduces bandwidth use.) | none |
| i11 | CP3.03 (Release tags sort by number, not by text; release candidates carry rc.) | none |
| i12 | CP3.08 (rpcauth stores a salted hash, so a leaked configuration file does not reveal the password.) | CP4.05 |
| i13 | CP4.12 (Vanity addresses: each further letter divides the chance by 58 and the work cannot be shortcut.) | none |
| i14 | CP4.09 (WIF: Base58Check of version 80, the key and a final 01 when compressed.); CP4.10 (One private key gives two public key encodings and so two addresses; coins sent to one are not seen at the other.); CP4.13 (A paper wallet must give back its address before any coins are sent.); CP5.07 (How do you know a backup works? (Code 27)) | none |
| i15 | CP4.07 (A 160-bit hash gives only 80 bits against collisions, which is why SegWit scripts use SHA256.) | CP4.05 |
| i17 | CP5.03 (How many words does 256 bits of entropy make? (Code 5)); CP5.08 (A recovery code is entropy in words: 11 bits a word, checksum included.) | none |
| i18 | CP5.19 (Stefan Thomas was paid 7,002 bitcoin in 2011, lost the password and has two guesses left.); CP6.13 (Block 74,638 (15 August 2010): a signed amount needs a range check.); CP2.13 (Block 74,638 (15 August 2010): a value overflow created about 184 billion bitcoin; a rule was shipped within hours and the honest chain won.); CP3.13 (A reference implementation needs a team and public review, not one keyholder (7 April 2014).); CP6.16 (Mt. Gox blamed malleability (10 February 2014) and researchers checked the claim.) | none |
| i19 | CP5.20 (The gap limit decides how far a recovery scan looks.) | none |
| i20 | CP5.05 (Why does a passphrase change the wallet? (Code 10)); CP5.11 (A forgotten passphrase loses the funds; the same twelve words with another passphrase give a different wallet.); CP5.17 (Labels are not derivable from the seed and need their own backup (BIP329).); CP5.15 (A complete backup: recovery code, passphrase if used, paths or descriptors, other signers' public keys, labels and protocol data; then restore and check the first address.); CP5.09 (Words become a 512-bit seed by deliberate slowness; a passphrase forks the wallet.) | none |
| i21 | CP6.21 (CompactSize counts: up to 252 one byte, then fd, fe or ff announce two, four or eight more bytes.) | none |
| i22 | CP6.10 (The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.); CP6.02 (The sequence field has meant three things, and the lock time is read against the median of eleven blocks.) | none |
| i23 | CP6.14 (Segwit changes the witness but keeps the txid; the wtxid still covers the witness.); CP6.04 (Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.); CP3.09 (Reading a transaction: decode it; the txid ignores the witness, and weight counts it.); CP6.19 (Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes.) | none |

## 4. Your emphasised concepts: where each could go and what it would cost

For each concept: the chapter whose slot could host it, the items that sit in that area, and, for each, the important points that would lose their only holder if that item were dropped. A new item would take the dropped item's place and answer type, so the paper keeps 25/25/25/25 + 10. Each table drops one item at a time; dropping two items together can lose more. Reworking an item in place is also possible and loses nothing; it is not shown as a row because it keeps the old item's topic.

### D: Each block links to the previous block, so miners restart on a new block

- Slot: chapter 2 (mining, CP2.04 and CP2.12) or chapter 3 (checking a block header, CP3.11).
- Today: No critical point of the chapters states this exactly; CP2.04 (how a payment reaches a block) and CP3.11 (hash the 80-byte header) are the nearest: CP2.04 is held by i07 alone, CP3.11 by no item.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |
| i09 | ChoiceFourCode, 3 points | Which setting a Bitcoin node really uses when the command line and the configuration file disagree. | CP3.05 (An option on the command line overrides the configuration file.); CP3.06 (Pruning and the transaction index do not mix: the node refuses both at once.) |
| i10 | Matching, 8 points | Match each node setting (pruning, index, connections and similar) to the need it serves. | CP3.14 (Option alertnotify: sends emergency alerts to the owner of the node, usually by email.); CP3.16 (Option prune: reduces the disk space requirement by deleting old blocks.); CP3.17 (Option txindex: maintains an index of all transactions, which means a complete copy of the blockchain.); CP3.18 (Option maxconnections: the maximum number of nodes to accept connections from; it reduces bandwidth use.) |
| i11 | CodeTrace, 3 points | Why release tags must be sorted by version number, not as text, shown by a small program. | CP3.03 (Release tags sort by number, not by text; release candidates carry rc.) |
| i12 | ChoiceFour, 4 points | Why both the node password setting and the older address keep a hash instead of the secret. | CP3.08 (rpcauth stores a salted hash, so a leaked configuration file does not reveal the password.) |

### E: Hash trials are unpredictable; the requirement is a value below a difficulty target, adjusted after a fixed number of blocks

- Slot: chapter 2 (CP2.12, mining is a search nobody can shortcut), or chapter 4 where i13 (vanity search) already asks a related unshortcut-able search.
- Today: CP2.12 is held only by the hand-marked bonus b2. i13 could be reworked in place instead of dropped.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |
| i13 | NumericAnswer, 3 points | Why every extra letter of a vanity address makes the search 58 times harder. | CP4.12 (Vanity addresses: each further letter divides the chance by 58 and the work cannot be shortcut.) |
| i14 | ChoiceFour, 4 points | Why a backup key in the wrong form shows a zero balance and what the paper wallet must give back. | CP4.09 (WIF: Base58Check of version 80, the key and a final 01 when compressed.); CP4.10 (One private key gives two public key encodings and so two addresses; coins sent to one are not seen at the other.); CP4.13 (A paper wallet must give back its address before any coins are sent.); CP5.07 (How do you know a backup works? (Code 27)) |
| i15 | FillBlankGroup, 8 points | Why the older address hides the key behind a hash (a commitment) and why newer scripts use a longer hash. | CP4.07 (A 160-bit hash gives only 80 bits against collisions, which is why SegWit scripts use SHA256.) |

### F: The 10-minute rule and soft forks: the steady block interval protects against forking risk

- Slot: chapter 6 (CP6.15 soft fork, held by no item) with i23, which already mentions the soft fork as a side point.
- Today: CP6.15 and the interval rule have no holder today.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i21 | CodeTrace, 3 points | How a count is written in few bytes (CompactSize), shown by a small program at the edges. | CP6.21 (CompactSize counts: up to 252 one byte, then fd, fe or ff announce two, four or eight more bytes.) |
| i22 | CodeTrace, 3 points | Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program. | CP6.10 (The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.); CP6.02 (The sequence field has meant three things, and the lock time is read against the median of eleven blocks.) |
| i23 | FillBlankGroup, 9 points | Why a payment tracker can rely on the transaction identifier after the witness change, and why witness bytes make a payment cheaper. | CP6.14 (Segwit changes the witness but keeps the txid; the wtxid still covers the witness.); CP6.04 (Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.); CP3.09 (Reading a transaction: decode it; the txid ignores the witness, and weight counts it.); CP6.19 (Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |

### T1: Serverless peer-to-peer

- Slot: chapter 1 (CP1.12 and CP1.03).
- Today: Only the hand-marked bonus b1 touches half of it.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i02 | ChoiceFour, 3 points | Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee. | CP1.06 (A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.); CP2.02 (Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.); CP2.14 (In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.); CP2.09 (Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.); CP2.10 (A higher fee rate leaves less change.); CP2.03 (How a payment is built: pick coins, write the outputs, leave the fee, sign.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

### T2: Distributed trust

- Slot: chapter 1 (CP1.10 and CP1.03).
- Today: Only half of bonus b1.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i02 | ChoiceFour, 3 points | Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee. | CP1.06 (A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.); CP2.02 (Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.); CP2.14 (In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.); CP2.09 (Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.); CP2.10 (A higher fee rate leaves less change.); CP2.03 (How a payment is built: pick coins, write the outputs, leave the fee, sign.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

### T3: Double-spending prevention

- Slot: chapter 1 (CP1.07) or chapter 2 next to i05.
- Today: Only bonus b1, by hand.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |

### T5: Approval without private keys: what a signature proves

- Slot: chapter 6 (CP6.01) or chapter 1 (CP1.08, the key is the proof of ownership).
- Today: CP6.01 is held by no item.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i21 | CodeTrace, 3 points | How a count is written in few bytes (CompactSize), shown by a small program at the edges. | CP6.21 (CompactSize counts: up to 252 one byte, then fd, fe or ff announce two, four or eight more bytes.) |
| i22 | CodeTrace, 3 points | Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program. | CP6.10 (The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.); CP6.02 (The sequence field has meant three things, and the lock time is read against the median of eleven blocks.) |
| i23 | FillBlankGroup, 9 points | Why a payment tracker can rely on the transaction identifier after the witness change, and why witness bytes make a payment cheaper. | CP6.14 (Segwit changes the witness but keeps the txid; the wtxid still covers the witness.); CP6.04 (Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.); CP3.09 (Reading a transaction: decode it; the txid ignores the witness, and weight counts it.); CP6.19 (Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes.) |
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

### T9: The borderless nature of Bitcoin

- Slot: chapter 1 (CP1.12).
- Today: CP1.12 is held by no item.
| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i02 | ChoiceFour, 3 points | Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee. | CP1.06 (A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.); CP2.02 (Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.); CP2.14 (In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.); CP2.09 (Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.); CP2.10 (A higher fee rate leaves less change.); CP2.03 (How a payment is built: pick coins, write the outputs, leave the fee, sign.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

The unit count stays 24 as long as an item is replaced by one of the same unit count; dropping i07, i15 or i23 frees two sub-questions at once.

## 4b. Your added points G to P: where each could go and what it would cost

Same reading as section 4: one item dropped at a time, nothing decided. Critical points marked 'no item' today are held by no item, so a new item could add a first holder. Many of G to P are economic and trust topics of chapters 1 and 2; the mechanics are chapters 3 and 6, as the slot lines say.

### G: Coinbase amount, reward by block number, minting end, first blocks, totals

- Today: PARTIAL: i03 asks the reward by height with the halving interval and the fees, and a claim that is too large; NOT asked: the first blocks' amounts, the total over a halving era, the coinbase after minting ends (fees only).
- Related critical points: CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999., held by i03); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by., held by i03); CP1.02 (Money is a ledger; the 21 million cap is arithmetic, and the price is discovered by trades., held by i03, i04); CP6.17 (Coinbase coins are locked for 100 blocks so a reorganisation cannot invalidate coins already spent., no item).
- Slot: chapter 6 (the schedule, CP6.18 and CP6.05) with chapter 1 (the cap, CP1.02); i03 could carry the other parts by rework with varied numbers.

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |
| i13 | NumericAnswer, 3 points | Why every extra letter of a vanity address makes the search 58 times harder. | CP4.12 (Vanity addresses: each further letter divides the chance by 58 and the work cannot be shortcut.) |
| i17 | NumericAnswer, 3 points | How long a recovery code is, from the bits each word carries and the checksum. | CP5.03 (How many words does 256 bits of entropy make? (Code 5)); CP5.08 (A recovery code is entropy in words: 11 bits a word, checksum included.) |

### H: First spend and the pizza

- Today: GAP: no item asks it.
- Related critical points: CP1.01 (Origins: block 0 carries a dated headline, and the first payment went from person to person., no item); CP6.22 (The first spend of an output: ten bitcoins to Hal Finney in block 170 (12 January 2009)., no item); CP1.02 (Money is a ledger; the 21 million cap is arithmetic, and the price is discovered by trades., held by i03, i04).
- Slot: chapter 1 (the first payment, CP1.01, and the first spend, CP6.22 in chapter 6); a numeric slot with easy arithmetic.

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i17 | NumericAnswer, 3 points | How long a recovery code is, from the bits each word carries and the checksum. | CP5.03 (How many words does 256 bits of entropy make? (Code 5)); CP5.08 (A recovery code is entropy in words: 11 bits a word, checksum included.) |
| i13 | NumericAnswer, 3 points | Why every extra letter of a vanity address makes the search 58 times harder. | CP4.12 (Vanity addresses: each further letter divides the chance by 58 and the work cannot be shortcut.) |

### I: Hash capacity, the 10-minute rule and price; pools

- Today: GAP for the machine-read items; only the half 'nobody can shortcut the search' sits in the hand-marked bonus b2.
- Related critical points: CP2.12 (Mining is a search that nobody can shortcut but anyone can check with one hash., held by bonus b2); CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block., held by i07); CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average., held by i04).
- Slot: chapter 2 (mining, CP2.12) with chapter 1 (price, CP1.11); the same family as your points D, E and F.

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

### J: Choice of transactions by fee per size

- Today: PARTIAL: i02 asks the fee as the difference of inputs and outputs, i23 asks the weight that makes witness bytes cheaper; NOT asked: that miners choose by fee per size (CP2.08).
- Related critical points: CP2.08 (Blocks have limited room, so miners pick the best fee rates first., no item); CP2.10 (A higher fee rate leaves less change., held by i02); CP6.19 (Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes., held by i23); CP3.10 (Weight units: base bytes count four units each, witness bytes one; 194 bytes weigh 569 units, 143 virtual bytes., no item).
- Slot: chapter 2 (CP2.08, best fee rates first) or chapter 6 (weight, CP6.19).

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |
| i22 | CodeTrace, 3 points | Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program. | CP6.10 (The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.); CP6.02 (The sequence field has meant three things, and the lock time is read against the median of eleven blocks.) |

### K: Why digital money failed before Bitcoin

- Today: GAP for the machine-read items; the double-spend half sits in the hand-marked bonus b1.
- Related critical points: CP1.07 (A double spend is refused by a shared rule, and no bank decides., held by bonus b1); CP1.03 (The network has no bank: every node checks every rule and proof of work makes history costly., held by bonus b1); CP1.02 (Money is a ledger; the 21 million cap is arithmetic, and the price is discovered by trades., held by i03, i04).
- Slot: chapter 1 (CP1.07 and CP1.03).

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i02 | ChoiceFour, 3 points | Your case 3: a payment with several inputs and outputs; find the change and see that, with no change output, the miner collects the whole left-over as the fee. | CP1.06 (A transaction has no fee field: the fee is the difference between inputs and outputs, implied and never written.); CP2.02 (Inputs equal outputs plus the fee: the ledger must balance and the remainder is the miner's fee.); CP2.14 (In every transaction shape (payment, consolidation, batching) inputs minus outputs is the fee.); CP2.09 (Coins are spent whole; a wallet cannot cut a coin in two, so the surplus returns as change.); CP2.10 (A higher fee rate leaves less change.); CP2.03 (How a payment is built: pick coins, write the outputs, leave the fee, sign.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |

### L: Why old currencies are no longer used (Ottoman, TL and YTL)

- Today: GAP: no critical point or deck slide carries it; it is your own material and the items would be new text with synthetic data.
- Related critical points: CP1.02 (Money is a ledger; the 21 million cap is arithmetic, and the price is discovered by trades., held by i03, i04).
- Slot: chapter 1 (money as a ledger, CP1.02).

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i04 | NumericAnswer, 3 points | How a day's volume-weighted price is built from trades, with one trade left out to find. | CP1.11 (Price is discovered by trades; a day figure is a volume-weighted average.) |
| i01 | ChoiceFour, 4 points | Two stories about a lost exchange: who holds the keys matters, and a stored wallet file must be tested before you trust it. | CP1.09 (Custody: whoever holds the keys holds the coins, exchanges included (Mt. Gox, Tokyo, February 2014).); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin).); CP1.04 (A wallet holds keys, not coins; whoever holds the keys holds the coins.) |
| i03 | NumericAnswer, 3 points | Your point B: a toy chain where the block reward halves every 10 blocks; find how much a block's coinbase claims too much. | CP6.18 (The subsidy starts at 50 bitcoin and halves every 210,000 blocks; it reaches zero after block 6,929,999.); CP6.05 (The coinbase creates coins under a schedule that ends at block 6,929,999, and weight is what a block is filled by.) |

### M: Losing access to private keys; best practices

- Today: PARTIAL: i18 (a lost password story), i01 (an untested backup), i20 (what a full backup holds) touch it; NOT asked as the list of best practices.
- Related critical points: CP5.15 (A complete backup: recovery code, passphrase if used, paths or descriptors, other signers' public keys, labels and protocol data; then restore and check the first address., held by i20); CP5.18 (An untested backup file is not an empty one (Mt. Gox, March 2014, about 200,000 bitcoin)., held by i01); CP5.19 (Stefan Thomas was paid 7,002 bitcoin in 2011, lost the password and has two guesses left., held by i18); CP5.07 (How do you know a backup works? (Code 27), held by i14); CP5.17 (Labels are not derivable from the seed and need their own backup (BIP329)., held by i20).
- Slot: chapter 5 (backups, CP5.15); i20, i17 or i19 slots.

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i17 | NumericAnswer, 3 points | How long a recovery code is, from the bits each word carries and the checksum. | CP5.03 (How many words does 256 bits of entropy make? (Code 5)); CP5.08 (A recovery code is entropy in words: 11 bits a word, checksum included.) |
| i19 | CodeTrace, 4 points | How far a recovery scan looks before it stops (the gap limit), shown by a small program. | CP5.20 (The gap limit decides how far a recovery scan looks.) |
| i20 | ChoiceFour, 3 points | Why a phone restored from the words alone shows other addresses and no labels: the passphrase and labels matter. | CP5.05 (Why does a passphrase change the wallet? (Code 10)); CP5.11 (A forgotten passphrase loses the funds; the same twelve words with another passphrase give a different wallet.); CP5.17 (Labels are not derivable from the seed and need their own backup (BIP329).); CP5.15 (A complete backup: recovery code, passphrase if used, paths or descriptors, other signers' public keys, labels and protocol data; then restore and check the first address.); CP5.09 (Words become a 512-bit seed by deliberate slowness; a passphrase forks the wallet.) |
| i14 | ChoiceFour, 4 points | Why a backup key in the wrong form shows a zero balance and what the paper wallet must give back. | CP4.09 (WIF: Base58Check of version 80, the key and a final 01 when compressed.); CP4.10 (One private key gives two public key encodings and so two addresses; coins sent to one are not seen at the other.); CP4.13 (A paper wallet must give back its address before any coins are sent.); CP5.07 (How do you know a backup works? (Code 27)) |

### N: Why an input cannot carry its own confirmation; locking and unlocking scripts

- Today: GAP: the decks name the lock of an output but no item asks why both scripts must run together; the nearest points are CP6.01 (no holder) and CP4.05 (i12, i15).
- Related critical points: CP6.01 (A transaction asks strangers to update their ledgers: inputs point, witnesses prove, outputs assign., no item); CP4.05 (P2PKH holds only a 20-byte hash of the key, a commitment; the key is revealed only when the coins are spent., held by i12, i15); CP4.06 (What P2SH and Bech32 change: P2SH hashes a script; Bech32 and Bech32m add a version, a program and a stronger checksum., no item).
- Slot: chapter 6 (CP6.01) or chapter 4 (scripts that hash, CP4.05 and CP4.06).

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i21 | CodeTrace, 3 points | How a count is written in few bytes (CompactSize), shown by a small program at the edges. | CP6.21 (CompactSize counts: up to 252 one byte, then fd, fe or ff announce two, four or eight more bytes.) |
| i22 | CodeTrace, 3 points | Which inputs allow replacement and carry a relative timelock, read from the sequence field by a small program. | CP6.10 (The sequence field carries finality, opt-in replacement (BIP125) and a relative timelock (BIP68); bit 31 switches the timelock off.); CP6.02 (The sequence field has meant three things, and the lock time is read against the median of eleven blocks.) |
| i23 | FillBlankGroup, 9 points | Why a payment tracker can rely on the transaction identifier after the witness change, and why witness bytes make a payment cheaper. | CP6.14 (Segwit changes the witness but keeps the txid; the wtxid still covers the witness.); CP6.04 (Witnesses in the input script made identifiers malleable; segregated witness moved them out, as a soft fork.); CP3.09 (Reading a transaction: decode it; the txid ignores the witness, and weight counts it.); CP6.19 (Weight: each field weighs its bytes times four, except marker, flag and witness (one); 569 weight units, 143 virtual bytes.) |
| i12 | ChoiceFour, 4 points | Why both the node password setting and the older address keep a hash instead of the secret. | CP3.08 (rpcauth stores a salted hash, so a leaked configuration file does not reveal the password.) |
| i15 | FillBlankGroup, 8 points | Why the older address hides the key behind a hash (a commitment) and why newer scripts use a longer hash. | CP4.07 (A 160-bit hash gives only 80 bits against collisions, which is why SegWit scripts use SHA256.) |

### O: Who confirms; fake transactions and blocks

- Today: PARTIAL: i18 (a range check refuses an invalid amount), i05 (confirmations) and bonus b1 (every node checks) touch it; NOT asked: how a fake source is met.
- Related critical points: CP2.06 (Consensus rules are checked by every node; block 74,638 broke one., no item); CP2.13 (Block 74,638 (15 August 2010): a value overflow created about 184 billion bitcoin; a rule was shipped within hours and the honest chain won., held by i18); CP6.13 (Block 74,638 (15 August 2010): a signed amount needs a range check., held by i18); CP3.11 (Checking a block: hash the 80-byte header and rebuild the merkle root yourself., no item); CP1.03 (The network has no bank: every node checks every rule and proof of work makes history costly., held by bonus b1).
- Slot: chapter 2 (consensus rules checked by every node, CP2.06) or chapter 3 (checking a block, CP3.11).

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |
| i09 | ChoiceFourCode, 3 points | Which setting a Bitcoin node really uses when the command line and the configuration file disagree. | CP3.05 (An option on the command line overrides the configuration file.); CP3.06 (Pruning and the transaction index do not mix: the node refuses both at once.) |
| i10 | Matching, 8 points | Match each node setting (pruning, index, connections and similar) to the need it serves. | CP3.14 (Option alertnotify: sends emergency alerts to the owner of the node, usually by email.); CP3.16 (Option prune: reduces the disk space requirement by deleting old blocks.); CP3.17 (Option txindex: maintains an index of all transactions, which means a complete copy of the blockchain.); CP3.18 (Option maxconnections: the maximum number of nodes to accept connections from; it reduces bandwidth use.) |
| i11 | CodeTrace, 3 points | Why release tags must be sorted by version number, not as text, shown by a small program. | CP3.03 (Release tags sort by number, not by text; release candidates carry rc.) |
| i12 | ChoiceFour, 4 points | Why both the node password setting and the older address keep a hash instead of the secret. | CP3.08 (rpcauth stores a salted hash, so a leaked configuration file does not reveal the password.) |

### P: The 51 percent rule and the attack

- Today: PARTIAL: i05 asks the chance that an attacker with a share of the hash power catches up and how many confirmations protect; NOT asked: the 51 percent rule itself.
- Related critical points: CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent)., held by i05); CP1.03 (The network has no bank: every node checks every rule and proof of work makes history costly., held by bonus b1).
- Slot: chapter 2 (CP2.05); i05 could carry it by rework.

| Item that could be dropped | Answer type and points | What it tests | Critical points that would lose their only holder |
|---|---|---|---|
| i05 | ChoiceFour, 4 points | Why a shop waits for confirmations, and how many it needs against a stronger attacker, read from a small table. | CP2.05 (Why confirmations: an attacker's chance falls with each block (10 percent attacker: 20.5 to 0.02 percent).) |
| i06 | Ordering, 8 points | Your case 1: put five transactions in order by the spending references, back to the coinbase transaction. | none |
| i07 | FillBlankGroup, 8 points | Your case 2: which of five transactions are surely mined from the spending references, and which are not shown to be. | CP2.04 (How a payment reaches a block: a node relays it, a miner finds a valid nonce and adds a block.); CP6.09 (A spend updates the UTXO set: remove what is spent, add what is created.) |

## 5. The C2 question: mined or not, under your simpler rule

Your rule: a spending reference means the referenced transaction was already mined. The current C2 (item i07) is more careful: it says a transaction that only names an output of another, unmined transaction does not prove that one mined. So today A, B and C are mined (C is stated to be in a block, and A and B are named by the chain above it), and D and E are left undecided.

The facts of the current item: C spends an output of B; B spends an output of A; E spends an output of D; C is stated to be inside a block; nothing is said of E.

Under your simpler rule C2 becomes:

- A, B and D are mined, because each of them is named by a spending reference (B by C, A by B, D by E).
- C and E are not shown to be mined: nobody spends them yet, so they may be in a block or still waiting.
- The sentence 'C is inside a block' is no longer needed as a fact; the rule itself gives A and B.
- The two blanks become: 'A, B and D are ____' (mined) and 'C and E are ____' (not shown to be mined, may still wait). The wrong entries stay: 'not mined (still waiting)' and 'mined later than C'.
- The tip must then state your rule in words: a spending reference can only point at an output that already exists in a block.
- The answer sheet is unchanged (same fill-in block type); only the key changes (D moves from undecided to mined, C and E become the undecided pair).
- If you want a strict 'mined / not mined' two-way answer, the item must also say which transactions are known to be waiting (for example, 'F and G are in a node's waiting list'); without that the student cannot know, and the honest third answer 'not shown to be mined' stays.
- Note for you: a node can hold chains of unmined transactions that spend each other, so your rule is exactly right for references written in blocks. The item can say that the references shown are the ones written in blocks, which makes your rule true as stated.

Nothing in this file has been applied to the items. Items v1.3.0 stay as committed.
