#!/usr/bin/env python3
"""SEN0401 chapter 2 corpus, version 1.2.0: How Bitcoin works - the concepts of chapter 2 of Mastering Bitcoin (3rd edition), each explained in
several full paragraphs (what it is, why it matters, where it is met, how it works, what to watch for), plus the concepts the explanations rely on
(hash function, public-key cryptography, elliptic curve, digital signature, unspent output, node, mempool, script, BIP, QR code, checksum, block
header, Merkle tree, hash rate, ontology ...), so that no term is used unexplained.

Used by sen0401_chapter_build_v1_0_0.py (TBox/ABox/document). Every concept id of version 1.1.0 is kept; new ones are added. Written in the session of
2026-10-02, re-reading every source from its text: the chapter (ch02_overview.adoc, tag third_edition_print1 working copy), chapters 1, 4, 6, 7, 9,
10, 11 and 12 of the same book, its glossary and appendix C; Nakamoto's paper; BIP 1, 21, 173, 321 and 350; Bitcoin Core at commit 05bc2f5
(consensus/amount.h, consensus/consensus.h, kernel/chainparams.cpp, pow.cpp, validation.cpp, primitives/transaction.cpp, secp256k1 sources);
the W3C PROV-O recommendation; the page of Anders Brownworth's Blockchain Demo and its script; and the owner's 2021 course notes
(Chapter_2_HowBitcoinWorks.pptx, text of the slides, their diagrams and notes saved in ch02-sources). The earlier, interrupted draft of this file was
reviewed claim by claim: what a source did not support was rewritten. Every number, hash, address, size or output quoted is executed in CHECKS or
in a worked example by the chapter builder (python 3.14), and every statement taken from a source carries a CHECKS entry that re-reads the phrase
from the saved copy of that source (08-tooling/sen0401_ch02_checklib_v1_1_0.py).
"""
__version__ = "1.2.0"
import os
HERE = os.path.dirname(os.path.abspath(__file__))
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"
_CITES = {"[AH]": " (Antonopoulos and Harding, 2023)", "[NK]": " (Nakamoto, 2008)", "[AL]": " (Altunel, 2021)", "[B21]": " (Schneider and Corallo, 2012)",
          "[B321]": " (Corallo, 2024)", "[B173]": " (Wuille and Maxwell, 2017)", "[BC]": " (Bitcoin Core, 2026)", "[PV]": " (Lebo et al., 2013)",
          "[BR]": " (Brownworth, n.d.)", "[B1]": " (Taaki, 2011)"}
def _c(t):
    for k, v in _CITES.items(): t = t.replace(" " + k, v)
    assert not any(k in t for k in _CITES), t
    return t

# ---- the executed claims: a helper library restates the algorithms that were read in the sources ----
_LIB = "__import__('runpy').run_path(%r)" % os.path.join(HERE, "sen0401_ch02_checklib_v1_1_0.py")
def _E(body):
    """an expression that loads the helper library as L and evaluates body"""
    return "(lambda L: %s)(%s)" % (body, _LIB)
def Qb(name, *phrases): return (_E("L['has_book'](%r%s)" % (name, "".join(", %r" % p for p in phrases))), "True")        # a phrase of a chapter of the book
def Qc(path, *phrases): return (_E("L['has_core'](%r%s)" % (path, "".join(", %r" % p for p in phrases))), "True")        # a phrase of a Bitcoin Core file at commit 05bc2f5
def Qs(name, *phrases): return (_E("L['has_saved'](%r%s)" % (name, "".join(", %r" % p for p in phrases))), "True")       # a phrase of a source saved in ch02-sources
CHECKS = []
_TXID = "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"
_URI = "bitcoin:bc1qk2g6u8p4qm2s2lh3gts5cpt2mrv5skcuu7u3e4?amount=0.01577764&label=Bob%27s%20Store&message=Purchase%20at%20Bob%27s%20Store"
_ADDR = "bc1qk2g6u8p4qm2s2lh3gts5cpt2mrv5skcuu7u3e4"
_GENHASH = "000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f"
_GENMERKLE = "4a5e1e4baab89f3a32518a88c31bc87f618f76673e2cc77ab2127b7afdeda33b"
_ALICE = "ALICE"   # Alice's transaction: L['ALICE_HEX'] in the helper library (ch06 and ch03 print it; a check compares it with the book)

NODES = []
# (id, label or None for the camel-case label, level, parent, leaf, paras)
# leaf = None for levels 1 and 2, else (example label, definition, io-or-None); io expressions must run on their own in the page (standard library only)

# ============================ TRANSACTION ============================
NODES += [
 ("Transaction", None, 1, None, None, [
  (W, "A transaction is the unit of action in Bitcoin: a message telling the network that the owner of certain bitcoins has authorized the transfer of that value to another owner. The new owner can in turn spend the value by creating another transaction, and so on, which gives a chain of ownership. This first branch of the chapter follows one such transaction, Alice's payment for a podcast episode in Bob's online store, from the moment it is conceived to the moment it is spent onward [AH]."),
  (Y, "Everything else in Bitcoin exists to carry transactions safely. The network propagates them, miners gather them into blocks and the blockchain records them, so a student who knows what a transaction contains, and how transactions refer to one another, has the vocabulary for the rest of the course. The book adds a point that is easy to miss: bitcoins do not exist physically or as digital data that could be emailed. What exists is a database on every full node that says who controls how many bitcoins, and a transaction is the data that convinces the nodes to update that database [AH]."),
  (E, "In the chapter Alice scans a payment request in Bob's store, her wallet builds a transaction, the network relays it and a miner records it in a block. The same object is met in every wallet, every block explorer and every node, because all of them read and write the same kind of data. Later chapters open it up: the keys and signatures that authorize it, the format in which it is sent, and the fees that pay for it."),
  (H, "The branch is organised around the questions a learner asks in order. What parts does a transaction have? Who is allowed to spend an output, and how is that proved? How do transactions link to one another, and what forms do they commonly take? In which units is value counted? How does a wallet construct a transaction, and how does the payment begin with a request? Each question is a group of concepts below, and later groups rely on the words defined in earlier ones."),
  (K, "Two cautions apply from the start. A transaction does not move coins from one place to another: it changes who may spend certain outputs, because the book says there are no physical coins or even individual digital coins and that the coins are implied in transactions [AH]. And this chapter simplifies on purpose: it names the signature, the script and the identifier without opening them, so each is given a concept here and a full treatment in a later chapter."),
 ], None),
 ("TransactionPart", "Transaction part", 2, "Transaction", None, [
  (W, "A transaction part is one of the pieces a transaction is assembled from. The chapter names the two sides, the inputs that spend funds and the outputs that receive them, and the small difference between them that pays the miner. To describe them exactly this group also explains the unspent output, the identifier by which a transaction is referred to, the size that a transaction occupies, the fee rate by which miners compare fees, and the ledger image that gives the whole structure its meaning [AH]."),
  (Y, "Reading a transaction correctly means knowing which part does which job. An input says what is being spent and who allows it, an output says what is created and who may spend it next, and the fee is whatever remains. Confusing these parts leads to the classic misunderstandings, such as believing that a payment is a single amount sent from one address to another."),
  (E, "The parts are met in every block explorer, which retrieves a transaction and shows what it spends and what it creates, and in every wallet that has to assemble them. The chapter's own illustration shows Alice's payment to Bob's store as one transaction whose input is an earlier output and whose two outputs are the payment and the change. The same transaction is printed byte by byte in the book's chapter on transactions, which lets this course check every figure in its description."),
  (H, "The concepts of this group are taken in the order in which a transaction is read: the double-entry ledger, which supplies the bookkeeping picture that holds the parts together, then the input, the output, the fee that is implied by both, the size that the transaction takes up in a block, the fee rate that turns a fee and a size into a comparable price, the unspent output that links an input to its past, and the identifier that names a transaction."),
 ], None),
 ("DoubleEntryLedger", "Double-entry ledger", 3, "TransactionPart", ("inputs balance outputs plus fee", "A ledger records every movement of value as an entry; the chapter pictures a transaction as a double-entry line whose two sides, inputs and outputs, differ only by the fee.", ("sum([75000, 20000, 5000]) == 100000", "True")), [
  (W, "A ledger is a book of record in which each movement of value is written down as an entry, and double-entry bookkeeping is the practice of recording every movement from two sides: what leaves one account and what arrives in another. The chapter uses this picture directly. It says that transactions are like lines in a double-entry bookkeeping ledger, with one or more inputs, which spend funds, on one side and one or more outputs, which receive funds, on the other [AH]."),
  (Y, "The image gives a student a first mental model for something that has no physical form. Instead of thinking of coins travelling between wallets, one thinks of entries in a shared book, each entry saying which earlier entries it consumes and which new ones it creates. The same image explains why the blockchain is described as the authoritative journal of all transactions: a journal is the chronological book in which such entries are first written down [AH]."),
  (E, "The picture appears in the chapter's figure of a transaction as a bookkeeping line, in the discussion of the transaction fee, and in the very first overview of Bitcoin, where the system is said to consist of users with wallets, transactions that are propagated across the network, and miners who produce the consensus blockchain, the authoritative journal of all transactions [AH]. Nakamoto's paper speaks of a record that cannot be changed without redoing the proof of work [NK]."),
  (H, "In an ordinary ledger the two sides of an entry balance exactly. In Bitcoin they balance only once the fee is counted: the outputs add up to slightly less than the inputs, and the difference is an implied fee collected by the miner [AH]. For Alice's payment the inputs total 100000 satoshis, the outputs 75000 and 20000, and the fee 5000, so that outputs plus fee equal inputs. The check sum([75000, 20000, 5000]) == 100000 evaluates to True, and the same total follows when the two output amounts are read out of the transaction's own bytes."),
  (K, "The analogy is a teaching device and has limits. A bookkeeper's ledger names accounts and their owners, while a Bitcoin transaction names no person: it refers to earlier outputs and to conditions for spending the new ones. The transaction data also has no field for a running balance per owner. A balance is computed by a wallet, which adds up the unspent outputs it can spend."),
 ]),
 ("Input", None, 3, "TransactionPart", ("an earlier output being spent", "An input spends funds by referring to an earlier transaction's output and proving ownership with a digital signature.", ("bytes.fromhex('eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a')[::-1].hex()", "'4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb'")), [
  (W, "An input is the part of a transaction that spends funds. It does not contain coins; it points to an earlier transaction's output, and it carries the proof that the person spending is entitled to do so. In the chapter's figure, the input of Alice's payment is labelled Tx1:0, meaning the output of her earlier transaction in which Joe sold her bitcoins [AH]."),
  (Y, "Inputs are what turn separate transactions into a connected history. Because every input names the output it consumes, anyone can follow a payment backward through the chain of ownership, and anyone can see whether the same output is being spent twice. The proof of ownership in the input, a digital signature that can be independently validated by anyone, is what lets strangers accept a payment without knowing who the payer is [AH]."),
  (E, "Inputs are found in every transaction. A simple payment has one input, a consolidation has many, and a miner's reward transaction has a special input that spends nothing [AH]. When a wallet constructs a transaction, choosing the inputs is its first task, as the concepts on coin selection and on getting the right inputs explain."),
  (H, "The book's chapter on transactions calls the reference that an input contains an outpoint. It consists of the 32-byte identifier of the transaction in which the funds were received and an output index, a 4-byte unsigned integer counted from zero that picks one output of that transaction [AH]. A full node uses the outpoint to find the earlier output, and from it learns the amount and the conditions for spending it. Real transactions do not state the value of their inputs; software must look up the output that is referenced, which for Alice's real transaction is an output of 100,000 satoshis [AH]. Reading the bytes of that transaction shows one small difference from the figure: the output index stored in the input is 1, whereas the simplified figure labels the reference Tx1:0. The identifier inside the input is also stored in the opposite byte order to the one used when it is displayed: reversing the bytes eb3ae38f... of the stored form gives 4ac54180..., the form that Bitcoin Core's commands accept [AH]."),
  (K, "An input cannot be partly spent, in the same way that a banknote cannot be torn in two: the whole of the referenced output is consumed, and any surplus must be sent back to the payer as change [AH]. The word input also invites a misreading. It does not mean money entering an account, but an earlier output being used up. And a figure is a simplification: when a detail matters, such as which output of the earlier transaction is meant, read it from the transaction itself."),
 ]),
 ("Output", None, 3, "TransactionPart", ("an amount locked to an address", "An output receives funds; the outputs add up to slightly less than the inputs.", ("sum([75000, 20000])", "95000")), [
  (W, "An output is the part of a transaction that receives funds. It consists of an amount, counted in satoshis, and a script, the condition that must be satisfied to spend that amount later. In Alice's payment one output carries 75000 satoshis for Bob's store and another carries 20000 satoshis back to Alice, so the outputs together add up to 95000 [AH]."),
  (Y, "Outputs are where ownership is created. The chapter explains that an output is created with a script saying, in effect, that it is paid to whoever can present a signature from the key corresponding to Bob's public address. Because only Bob's wallet holds that key, only Bob can later spend the output. The book calls this encumbering the output with a demand for a signature from Bob [AH]."),
  (E, "Outputs are met in every transaction. They are also what a wallet counts when it reports a balance: the balance is the sum of the outputs that the wallet's keys can spend and that nobody has spent yet. Each output that is still unspent is a coin-like unit that a later transaction can take as an input. The book notes that an output can hold as little as zero and as much as 21 million bitcoins, a limit explained under the concept of consensus rules [AH]."),
  (H, "A transaction can have several outputs, and they are numbered from zero in the order in which they appear, which is what the second half of an outpoint refers to. In the bytes of Alice's real transaction the output at position 0 carries 20000 satoshis, her change, and the output at position 1 carries 75000 satoshis for Bob's store; the later figure of the chain accordingly shows Bob spending the output Tx2:1. The sum of all outputs is at most the sum of all inputs, and what is left over is the fee: sum([75000, 20000]) evaluates to 95000, and the 5000 satoshis missing from the 100000 that Alice spent form the fee."),
  (K, "Outputs are all-or-nothing in the same way as inputs: a later transaction takes a whole output or leaves it alone. An output also never expires. It stays unspent, and is counted in every full node's database, until a valid transaction spends it, which is why the book warns that outputs of very small value can become uneconomical to spend and are a burden on the nodes that must keep track of them [AH]."),
 ]),
 ("TransactionFee", "Transaction fee", 3, "TransactionPart", ("inputs minus outputs", "The fee is implied: the difference between the inputs and the outputs, collected by the miner who includes the transaction.", ("100000 - sum([75000, 20000])", "5000")), [
  (W, "The transaction fee is a small payment to the miner who includes a transaction in a block. It is never written in the transaction as a separate number. It is implied by the difference between the value of the inputs and the value of the outputs, so any value that the outputs do not claim goes to the miner [AH]."),
  (Y, "The fee is how a user asks the network to process a payment in a timely fashion. The chapter on fees explains that it is not a fee in the usual sense: it is not an amount set by the protocol or by any miner, but much more like a bid in an auction for the limited space in a block [AH]. It is one of two payments that reward a miner, the other being the newly created bitcoins of the block reward. Nakamoto's paper already described it: if the output value of a transaction is less than its input value, the difference is a fee added to the incentive of the block containing the transaction [NK]."),
  (E, "The wallet adds the fee when it constructs the transaction; Alice only has to choose a destination, an amount and a fee. The fee can always be read as the difference between the sum of the inputs and the sum of the outputs, and a miner's reward transaction collects the sum of all fees in its block."),
  (H, "For Alice's payment the arithmetic is simple. Her input is Tx1's output of 100000 satoshis, the two outputs total 95000 satoshis, and so 100000 - sum([75000, 20000]) evaluates to 5000: the fee is 5000 satoshis. The figure is derived from the amounts that the book prints, and it is the miner, not Bob, who receives it. The book's own diagram of the chain lists the same fee of 5000 for the transaction to Bob's store and a fee of 8000 for Bob's onward transaction."),
  (K, "Because the fee is implied, a wallet that mistakes the amounts can send an enormous fee without any warning from the format, since there is no field to check. Wallets should therefore make it hard to pay an excessive fee by accident, while still allowing it on purpose, as the chapter on fees advises [AH]. Fees also do not depend on the value being sent, but on how much space the transaction takes, which the concepts of size and fee rate explain."),
 ]),
 ("TransactionSize", "Transaction size", 3, "TransactionPart", ("Alice's payment: 194 bytes, weight 569, 143 vbytes", "A block has limited room; transactions are measured in weight units, four of which make one virtual byte (vbyte), and a miner compares them by fee per unit.", ("(569 + 3) // 4", "143")), [
  (W, "The size of a transaction is the room that it takes up in a block. Because every block can hold only a limited amount of transaction data, software needs a measure for it. The book names the modern unit weight, and an alternative expression of the same measure, the virtual byte or vbyte, of which one equals four units of weight; a vbyte is thus easy to compare with the plain byte, the unit of eight bits, that older blocks used [AH]."),
  (Y, "Size is what makes block space a scarce good. A block is limited to 4 million units of weight, so the number of transactions that fit depends on how large each one is, not on how much value it moves [AH]. A payment of a million bitcoins and one of a single satoshi may occupy the same room, and a miner who has to choose between them looks at the fee that each pays for that room, which is the idea behind the fee rate."),
  (E, "Size appears whenever a wallet shows how much a payment costs, and in the figures that block explorers and Bitcoin Core report for a transaction. Alice's real transaction is reported by Bitcoin Core as 194 bytes in size, 143 vbytes and 569 units of weight [AH]. Bitcoin Core's consensus code defines the block limit as MAX_BLOCK_WEIGHT of 4,000,000 and the factor between the weight and the old byte as WITNESS_SCALE_FACTOR of 4 [BC]."),
  (H, "The weight of a transaction is the sum of the weights of its fields, each field's serialized size in bytes being multiplied by a factor [AH]. The factors are chosen so that the part of a transaction that holds its proofs counts for less than the rest, which keeps the cost of spending an output low. Reading the 194 bytes of Alice's transaction and counting the proof part once and everything else four times gives 569 units of weight, and 569 divided by four, rounded up, gives 143 vbytes, as (569 + 3) // 4 evaluates to 143 in whole numbers. A block of 4,000,000 units of weight is therefore a block of at most one million vbytes."),
  (K, "The three numbers answer different questions. The size in bytes is the length of the serialized data, the weight is what the block limit counts, and the virtual byte is the weight expressed in a familiar unit. Mixing them up is a common reason for fee figures that do not match between two tools. The factors themselves belong to a later chapter on transactions, and a student should treat the number 4 as a fixed part of today's rules, not a law of nature."),
 ]),
 ("FeeRate", "Fee rate", 3, "TransactionPart", ("fee divided by size", "A miner compares transactions by their fee for the space they use, the fee rate, usually quoted in satoshis per virtual byte.", ("round(5000 / 143, 2)", "34.97")), [
  (W, "The fee rate is the fee a transaction pays for each unit of the space it takes in a block. Miners do not compare transactions by their total fee alone; they divide the fee by the size of the transaction, as a shopper divides the price of a bag of rice by its weight to find the best deal. The most common unit today is the satoshi per virtual byte [AH]."),
  (Y, "Block space is scarce, and the fee rate is the price at which it is sold. A transaction pays a single fee however large it is, but a larger transaction leaves room for fewer others in the block, so a miner who wants the most revenue from a block fills it with the transactions that pay the highest fee per unit of space. The chapter says accordingly that transactions are added to a new block prioritized by the highest fee rate first [AH]."),
  (E, "Fee rates matter whenever a wallet lets a user choose how quickly a payment should be processed. A user who wants a payment confirmed sooner chooses a higher fee rate; one who can wait chooses a lower one. The book lists several units in which a fee rate is written, among them satoshis per virtual byte, which it calls the most commonly used today, and bitcoin per kilo-vbyte, which Bitcoin Core mainly uses [AH]."),
  (H, "The calculation is a plain division. Alice's payment paid 5000 satoshis and takes up 143 virtual bytes, so its fee rate is 5000 / 143, which rounds to 34.97 satoshis per virtual byte. A miner sorts the candidate transactions by this ratio and takes them from the top until the block is full. The size of 143 comes from the transaction's own bytes, as the concept of transaction size shows, and the fee of 5000 from the amounts in the chapter."),
  (K, "The units are a source of expensive mistakes. The book warns that a fee rate copied from a field with one denominator into a field with another can lead to paying a thousand times too much, and that switching the numerator could mean a hundred million times too much [AH]. A fee rate is also a market price, not a rule of the protocol, so what counts as a good rate changes with demand for block space; the figure of 34.97 describes one payment, not a recommendation."),
 ]),
 ("UnspentOutput", "Unspent transaction output", 3, "TransactionPart", ("an output nobody has spent", "An unspent transaction output (UTXO) is an output that no later transaction has consumed; full nodes keep the set of all of them.", ("[o for o, spent in {'Tx1:0': True, 'Tx2:0': False, 'Tx2:1': False}.items() if not spent]", "['Tx2:0', 'Tx2:1']")), [
  (W, "An unspent transaction output, abbreviated UTXO, is a transaction output that has not yet been used as an input by any later transaction. The glossary defines it as an unspent transaction output that can be spent as an input in a new transaction [AH]. A wallet's bitcoins are, in this sense, nothing other than the unspent outputs it can unlock."),
  (Y, "The idea explains how Bitcoin keeps track of ownership without accounts. A full node holds a copy of every confirmed transaction's unspent outputs, and a valid new transaction may spend only outputs that are in that set. Each time a new block arrives, the outputs that its transactions spend are removed from the database and the outputs they create are added, so the set of unspent outputs is the current state of the whole system, and a double-spend is simply an attempt to use an output that is already gone [AH]."),
  (E, "The chapter meets UTXOs when it describes how Alice's wallet gets the right inputs. A wallet that runs on a full node holds every unspent output, while many user wallets run as lightweight clients that track only their own [AH]. The network chapter adds that some implementations keep a database of all unspent outputs, which holds millions of entries and, unlike the mempool, does not usually differ between nodes [AH]."),
  (H, "Mark each output with a flag that says whether it has been spent. Starting from the outputs of Alice's chain, the expression that lists the outputs whose flag is false returns Tx2:0 and Tx2:1, because Tx1:0 was consumed by Alice's payment. A node that receives a new transaction performs the same filter at scale: for each outpoint it looks the output up in its set, rejects the transaction if the output is missing or already spent, and otherwise treats it as valid in this respect."),
  (K, "Two misreadings are common. An unspent output is not an account balance, and a wallet's total is the sum of many separate outputs, each of which is spent whole. And an unspent output is still tied to a condition: it counts as spendable only for the party that can satisfy its script. Wallets therefore track UTXOs for their own keys and ignore the rest."),
 ]),
 ("TransactionIdentifier", "Transaction identifier", 3, "TransactionPart", ("a 32-byte name for Alice's payment", "The transaction identifier, or txid, is a 32-byte value derived from the transaction's data; an input points to an earlier output by txid and position.", ("bytes.fromhex('eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a')[::-1].hex()", "'4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb'")), [
  (W, "The transaction identifier, or txid, is the 32-byte name of a transaction. It is derived from the transaction's own data by a hash function, so it is not assigned by anyone, and two different transactions cannot sensibly share one. In the chapter the txid is what an input uses to refer to the transaction in which funds were received [AH]."),
  (Y, "Names make references possible. Because a txid summarizes the transaction it identifies, a reference to it cannot be redirected to different content, and anyone holding the transaction can recompute the name and confirm it. This is also what makes a chain of transactions auditable: every link is a txid plus a position, and both can be checked independently by any node."),
  (E, "The txid is the search key in every block explorer: the chapter says that explorers accept a Bitcoin address, a transaction hash, a block number or a block hash. The book prints the identifier of Alice's payment to Bob as 466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177, which is 64 hexadecimal characters, since the book notes that it takes 64 hexadecimal characters to display 32 bytes [AH]."),
  (H, "Bitcoin Core computes the identifier by hashing the serialized transaction without its proof data [BC]; hashing means applying the double SHA-256 construction that the concept of the hash function shows, and the result is shown with its bytes reversed. Doing exactly that to the 194 bytes of Alice's real transaction reproduces the printed identifier. The reversal is the byte-order trap the book describes: a hash is displayed to users in one byte order but used internally in another, so the identifier that the transaction's input stores, eb3ae38f..., is the earlier transaction's identifier read the other way round, and reversing its bytes gives 4ac54180... [AH]."),
  (K, "A txid belongs to the transaction as it was built, and it is not proof that the transaction has been confirmed: a payment can have a txid and still wait in the mempool. The byte-order difference is a frequent source of confusion for programmers: pasting the stored form into a block explorer, or the displayed form into a program that expects the stored one, finds nothing, because the hash is the same and only its reading differs [AH]."),
 ]),
]
CHECKS += [
 Qb("ch06_transactions.adoc", "bitcoins don't exist either physically or as digital data", "There exists a database on every Bitcoin full node that says that Alice controls some number of bitcoins"),
 Qb("ch01_intro.adoc", "There are no physical coins or even individual digital coins. The coins are implied in transactions that transfer value from spender to receiver."),
 Qb("ch02_overview.adoc", "a transaction tells the network that the owner of certain bitcoins has authorized the transfer of that value to another owner", "Transactions are like lines in a double-entry bookkeeping ledger", "outputs add up to slightly less than inputs and the difference represents an implied _transaction fee_", "which is the authoritative journal of all transactions"),
 Qs("nakamoto_bitcoin_whitepaper.txt", "If the output value of a transaction is less than its input value, the difference is a transaction fee that is added to the incentive value of the block containing the transaction", "a record that cannot be changed without redoing the proof-of-work"),
 Qb("ch06_transactions.adoc", "The outpoint contains a 32-byte txid", "Output indexes are 4-byte unsigned integers starting from zero", "the value of the previous output was 100,000 satoshis", "it keeps a database that stores every UTXO", "all of the outputs they spend are removed from the UTXO database and all of the outputs they create are added to the database"),
 Qb("ch06_transactions.adoc", "Digests provide unique identifiers for blocks and transactions", "digests are iterated upon in Bitcoin's proof-of-work function", "hash digests are displayed to users in one byte order but are used internally in a different byte order", "it takes 64 hexadecimal characters to display 32 bytes", "eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a"),
 Qb("ch06_transactions.adoc", "Bitcoin's consensus rules allow an output to have a value as small as zero and as large as 21 million bitcoins", "Such outputs are known as _uneconomical outputs_", "for Bitcoin is called _weight_", "four units of weight equal one vbyte", "Blocks are limited to 4 million weight", "To calculate the weight of a particular field in a transaction, the size of that serialized field in bytes is multiplied by a factor"),
 Qb("ch03_bitcoin-core.adoc", '"size": 194, "vsize": 143, "weight": 569', '"txid": "466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177"', '"txid": "4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19...aeb"'),
 Qb("ch09_fees.adoc", "it's not a fee in the usual sense of that word", "much more like a bid in an auction", "The good being purchased is the portion of limited space in a block", "Satoshi/Vbyte (most commonly used today)", "BTC/Kilo-vbyte (used mainly in Bitcoin Core)", "they could overpay fees by 1,000 times", "they could theoretically overpay by 100,000,000 times", "Wallets should make it hard for the user to pay an excessive fee rate", "Each transaction only pays a single fee--it doesn't matter how large the transaction is"),
 Qb("ch10_network.adoc", "contains millions of entries of unspent transaction outputs", "will not usually vary between nodes"),
 Qb("glossary.asciidoc", "UTXO is an unspent transaction output that can be spent as an input in a new transaction"),
 Qc("src/consensus/consensus.h", "MAX_BLOCK_WEIGHT{4'000'000}", "WITNESS_SCALE_FACTOR = 4"),
 Qc("src/primitives/transaction.cpp", "Txid::FromUint256((HashWriter{} << TX_NO_WITNESS(*this)).GetHash())"),
 # Alice's real transaction, read out of its own bytes
 (_E("L['ALICE_HEX'] in ''.join(open('/home/claude/src/bitcoinbook/ch06_transactions.adoc').read().replace(chr(92), '').split())"), "True"),
 (_E("L['ALICE_HEX'] in ''.join(open('/home/claude/src/bitcoinbook/ch03_bitcoin-core.adoc').read().replace(chr(92), '').split())"), "True"),
 (_E("L['txid_of'](L['ALICE_HEX'])"), repr(_TXID)),
 (_E("len(bytes.fromhex(L['txid_of'](L['ALICE_HEX'])))"), "32"),
 (_E("len(L['txid_of'](L['ALICE_HEX']))"), "64"),
 (_E("[o[0] for o in L['parse_tx'](L['ALICE_HEX'])['outputs']]"), "[20000, 75000]"),
 (_E("sum(o[0] for o in L['parse_tx'](L['ALICE_HEX'])['outputs'])"), "95000"),
 (_E("100000 - sum(o[0] for o in L['parse_tx'](L['ALICE_HEX'])['outputs'])"), "5000"),
 (_E("(len(L['parse_tx'](L['ALICE_HEX'])['inputs']), len(L['parse_tx'](L['ALICE_HEX'])['outputs']))"), "(1, 2)"),
 (_E("L['parse_tx'](L['ALICE_HEX'])['inputs'][0][1]"), "1"),
 (_E("L['parse_tx'](L['ALICE_HEX'])['inputs'][0][0]"), repr("4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb")),
 (_E("bytes.fromhex(L['parse_tx'](L['ALICE_HEX'])['inputs'][0][0])[::-1].hex()"), repr("eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a")),
 (_E("L['parse_tx'](L['ALICE_HEX'])['total']"), "194"),
 (_E("L['weight_of'](L['ALICE_HEX'])"), "569"),
 (_E("L['vsize_of'](L['ALICE_HEX'])"), "143"),
 (_E("L['parse_tx'](L['ALICE_HEX'])['stripped']"), "125"),
 ("569 / 4", "142.25"), ("4_000_000 // 4", "1000000"), ("round(5000 / 143, 4)", "34.965"),
 (_E("round((100000 - sum(o[0] for o in L['parse_tx'](L['ALICE_HEX'])['outputs'])) / L['vsize_of'](L['ALICE_HEX']), 2)"), "34.97"),
 ("sum([75000, 20000, 5000]) == 100000", "True"),
 ("(75000 - 67000, 100000 - 75000 - 20000)", "(8000, 5000)"),
]

# ============================ the parts of this corpus, executed in this namespace ============================
for _part in ("b", "c", "d", "e"):
    _f = os.path.join(HERE, "sen0401_ch02_text_%s_v1_2_0.py" % _part)
    exec(compile(open(_f, encoding="utf-8").read(), _f, "exec"))

# ============================ the tail: citations resolved and the supplements of the chapter builder ============================
NODES = [(n[0], n[1], n[2], n[3], n[4], [(f, _c(t)) for f, t in n[5]]) for n in NODES]
CHAPTER = "02"
RAISES = [
 ("bytes.fromhex('abc')", "ValueError"),
 ("bytes.fromhex('zz')", "ValueError"),
 ("__import__('hashlib').sha256('abc')", "TypeError"),
 ("(2 ** 64).to_bytes(8, 'little')", "OverflowError"),
 ("int('0.001', 10)", "ValueError"),
 ("__import__('decimal').Decimal('0.5') + 0.5", "TypeError"),
 ("1 / 0", "ZeroDivisionError"),
 ("[20000, 75000][2]", "IndexError"),
 ("(256).to_bytes(1, 'little')", "OverflowError"),
 ("{'4ac54180:1': 100000}['4ac54180:0']", "KeyError"),
]
OWNERS = [
 ("Script", "Output"), ("Outpoint", "Input"), ("Witness", "Input"), ("Satoshi", "Output"),
 ("FeeRate", "TransactionFee"), ("Serialization", "TransactionSize"), ("ByteOrder", "TransactionIdentifier"),
 ("Entropy", "KeyPair"), ("EllipticCurve", "KeyPair"), ("Nonce", "DigitalSignature"),
 ("Checksum", "Address"), ("Address", "Bip21Uri"), ("Uri", "Bip21Uri"), ("QrCode", "Bip21Uri"),
 ("Gossiping", "TransactionPropagation"), ("Transmission", "TransactionPropagation"), ("Mempool", "FullNode"),
 ("MerkleTree", "BlockHeader"), ("Difficulty", "BlockHeader"), ("BlockHeader", "Block"),
 ("CoinbaseTransaction", "Block"), ("BlockReward", "CoinbaseTransaction"), ("HashRate", "ProofOfWork"),
 ("BlockHeight", "Block"), ("Probability", "Confirmation"), ("Triple", "Ontology"), ("ProvenanceGraph", "Ontology"),
]
ERRORS = [
 ("HexadecimalNotation", "bytes.fromhex('abc') raises ValueError: fromhex() arg must contain an even number of hexadecimal digits"),
 ("HashFunction", "__import__('hashlib').sha256('abc') raises TypeError: Strings must be encoded before hashing"),
 ("Serialization", "(2 ** 64).to_bytes(8, 'little') raises OverflowError: int too big to convert"),
 ("Satoshi", "__import__('decimal').Decimal('0.5') + 0.5 raises TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'"),
 ("Output", "[20000, 75000][2] raises IndexError: list index out of range"),
 ("BitsAndBytes", "(256).to_bytes(1, 'little') raises OverflowError: int too big to convert"),
 ("Outpoint", "{'4ac54180:1': 100000}['4ac54180:0'] raises KeyError: '4ac54180:0'"),
 ("Difficulty", "1 / 0 raises ZeroDivisionError: division by zero"),
]
CQS = [
 "Which parts does a Bitcoin transaction consist of, what does each part contribute, and what are the values of each part in the real transaction that chapter 2 follows?",
 "Which mathematical tools does a transaction rely on - hashing, key pairs, the elliptic curve, signatures, checksums - and what exactly does each of them guarantee and not guarantee?",
 "How does a payment begin: what does the invoice of the chapter contain, which document defines its format, and what is the status of that document today?",
 "How does a signed transaction reach the miners, who takes part in that journey, and how much of a payment can each kind of participant verify for itself?",
 "How is a transaction recorded: how is a block built, what makes it valid, how is the miner paid, and how are the numbers of the reward, the target and the hash rate obtained?",
 "What exactly does a confirmation buy, how fast does the probability of reversal fall, and when may a merchant accept a payment that has none?",
 "How can the chapter's transaction chain be expressed as a provenance graph in the vocabulary of the W3C PROV Ontology, and what does that model leave out?",
 "Which terms do the explanations of this chapter rely on, and is each of them a concept of this chapter or of chapter 1?",
]
PROVENANCE = (
 "Concepts are corpus-derived from the 3rd edition's chapter 2 through the Stage 1 research record; the explanations were rewritten for version 1.2.0 from the "
 "documents listed at the head of this module, each read in the session of 2026-10-04, with every quotation re-read from the saved copy of its source and every "
 "number, hash, address, encoding and size recomputed by a claim that the chapter builder executes; the supporting concepts (bits and bytes, hexadecimal notation, "
 "entropy, the nonce, encryption, serialization, byte order, the outpoint, the witness, the address, the exchange rate, the wallet, the participants and the stages "
 "of propagation, and the whole mining and security vocabulary of the blockchain branch) were added because an audit of the terms used in the explanations found them "
 "used without a concept of their own in this chapter or in chapter 1.")
TOOLING = "CPython 3.14.4"
DOC_TITLE = "How Bitcoin works: one real transaction from Alice's wallet to the blockchain, every figure recomputed"
DOC_ABOUT = ("This document explains chapter 2 of the 3rd edition concept by concept, adding the terms the chapter uses without defining them, and re-reads every "
             "quotation from its source and recomputes every number, hash and encoding from the bytes of the real transaction the chapter follows.")
CHANGE = (
 "1.2.0 rewrites every explanation as four to six paragraphs of continuous prose, keeps every concept identifier of 1.1.0 with its parent, and adds the concepts that "
 "an audit of the terms used showed to be missing: the cryptographic and computing foundations (the hash function, the key pair, public-key cryptography, the elliptic "
 "curve, the digital signature, the checksum, entropy, the nonce, encryption, bits and bytes, hexadecimal notation), the remaining parts of a transaction (the script, "
 "the double-entry ledger, the size, the fee rate, the unspent output, the identifier, serialization, byte order, the outpoint, the witness), the payment request "
 "(the URI, the QR code, the improvement proposal, the address, the exchange rate), construction and the wallet, the participants and stages of the network branch, and "
 "the whole mining, security and spending vocabulary of the blockchain branch, plus the ontology and triple of the semantics branch and the five pages of the "
 "demonstration in the practice branch; so MAJOR in the text and MINOR in the structure, numbered MINOR because no identifier was removed and no parent changed.")

def run_checks_inprocess():
    bad = []; n = 0
    def ev(e): return repr(eval(e, {}))
    for e, x in CHECKS:
        n += 1
        try: got = ev(e)
        except BaseException as ex: got = "EXC %r" % (ex,)
        if got != x: bad.append((e[:160], x, got))
    for nd in NODES:
        if nd[4] and nd[4][2]:
            n += 1; e, x = nd[4][2]
            try: got = ev(e)
            except BaseException as ex: got = "EXC %r" % (ex,)
            if got != x: bad.append((nd[0], x, got))
    for e, typ in RAISES:
        n += 1
        try: eval(e, {}); bad.append((e, typ, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != typ: bad.append((e, typ, type(ex).__name__))
    for leaf, text in ERRORS:
        n += 1; e, rest = text.split(" raises ", 1); et, msg = rest.split(": ", 1)
        try: eval(e, {}); bad.append((e, et, "no error"))
        except BaseException as ex:
            if type(ex).__name__ != et or not str(ex).startswith(msg): bad.append((e, rest, "%s: %s" % (type(ex).__name__, ex)))
    return n, bad

if __name__ == "__main__":
    import sys
    n, bad = run_checks_inprocess()
    print(n, "claims executed under CPython", sys.version.split()[0], "- failures:", bad)
    ids = [x[0] for x in NODES]; assert len(ids) == len(set(ids)), "duplicate ids"
    byid = {x[0]: x for x in NODES}
    for x in NODES:
        assert x[3] is None or x[3] in byid, x[0]
        assert (x[2] == 3) == (x[4] is not None), x[0]
        if x[3]: assert byid[x[3]][2] == x[2] - 1 and ids.index(x[3]) < ids.index(x[0]), x[0]
        assert (x[2] == 3 and 4 <= len(x[5]) <= 6) or (x[2] < 3 and 3 <= len(x[5]) <= 6), (x[0], len(x[5]))
    for leaf, owner in OWNERS: assert leaf in byid and owner in byid and byid[leaf][2] == 3 and byid[owner][2] == 3, (leaf, owner)
    for leaf, t in ERRORS: assert leaf in byid and byid[leaf][2] == 3, leaf
    print(len(NODES), "concepts;", sum(len(x[5]) for x in NODES), "paragraphs;",
          sum(len(t.split()) for x in NODES for f, t in x[5]), "words;", len(CHECKS) + len(RAISES) + len(ERRORS) + sum(1 for x in NODES if x[4] and x[4][2]), "executed claims")
