"""Reader-facing speaker notes for SEN0401 chapters 7 and 8.

The slides are handed to students together with these notes, so each note explains the short wording of its slide in full sentences,
fits the concept among related ones and points to further information. No note gives directions to a presenter.
"{EX}" is replaced by the number of the matching example in the chapter code tab."""
RN7 = {}
RN8 = {}

RN7.update({
1: """This chapter is about the two halves of every Bitcoin spend: the script that locks a coin and the data that unlocks it. It is chapter 7 of Mastering Bitcoin, third edition, and the figure on the slide shows a locking script paired with an unlocking script.

Every result in this deck was computed with the chapter's own Python library under Python 3.14.6, so no Bitcoin Core node was needed. Each code slide has a twin in the chapter code tab of the course page, where you can edit the listing and run it yourself.

It helps to recall chapter 6 first: a transaction spends earlier outputs, and this chapter explains the rule that decides whether such a spend is allowed.""",
2: """This slide lists the route through the chapter in nine parts, each with the slide numbers where it lives, so you can jump straight to a topic. The order follows the book: the Script language, locking a coin to a key, multisignatures, pay to script hash, data and timelocks, flow control, segregated witness, script trees and key tweaks, and finally taproot and tapscript.

The figures on the right summarise the deck: sixty-one slides, three true stories, and fifteen code examples that each end in a picture of the result.

The table on every divider slide repeats this route, so you always know which part you are in. Later ideas such as segregated witness and taproot are changes to the earlier ones, so a hard part is easier after revisiting the part before it.""",
3: """These seven questions are the chapter's own competency questions: the things you should be able to answer after studying it. Each is answered on a slide of this deck, and the closing slide returns to them.

Use them as a self-test. Try to answer each in a sentence before reading on, and let an unanswered question send you to the part of the route where its answer lives. The first two concern the foundations: how scripts decide a spend, and why Script is deliberately limited. The next three concern cost, time and malleability. The last two concern taproot and tapscript.

If a question contains an unfamiliar word, the course page for chapter 7 has an entry for it under the concept of the same name.""",
4: """The concept map shows the whole chapter as nine groups, each with the number of concepts the book introduces there: fourteen for the Script language, six for locking to a key, five for multisignatures, six for pay to script hash, eleven for data and timelocks, eight for flow control, sixteen for segregated witness, ten for script trees and key tweaks, and eleven for taproot and tapscript.

The counts show where the weight lies. Segregated witness carries the most concepts because it changes how a transaction is organised, not only how a script runs.

Every later slide belongs to one of these groups. The same map is on the course page, where you can filter it and open each concept for a full explanation.""",
5: """This divider opens the first part, which answers a basic question: how does the network decide that a spender may take a coin? A script is a lock and key recipe made of data items and operation words, and every node follows the same recipe in the same way, so every node reaches the same verdict.

The part has two themes. Language and limits explains what Script is and why it is kept small and free of loops. Locking and running explains how the lock placed by the payer and the data shown by the spender run one after the other.

The table at the bottom marks where this part sits among the nine parts of the chapter.""",
6: """Transaction scripts are the small language in which every coin's spending rule is written. That is why each output carries a script rather than just an owner's name.

Script is Turing incomplete: it has no loops, so every script ends. The limit is deliberate, because it lets every node check any script quickly and safely.

Verification is stateless. The result depends only on the script and the data given to it, never on the clock or on other transactions, so all nodes reach the same verdict.

A script is built in two parts, the lock made by the payer and the unlocking data made by the spender, and the node checks them together.

Slide 7 runs the smallest example, and slide 8 names the pieces it uses.""",
7: """Script is read from left to right. In the first box the numbers 2 and 3 are pushed onto a stack, OP_ADD takes the top two items and pushes their sum, the number 5 is pushed, and OP_EQUAL compares the top two items. Because the sum is five, the script ends true and the result is OK. With a six in place of the five the comparison fails and the result is EVAL_FALSE, the error for a final false answer.

The third box assembles the five words into five bytes. In 5253935587, 0x52 and 0x53 are the opcodes for the numbers 2 and 3, 0x93 is OP_ADD, 0x55 is the number 5 and 0x87 is OP_EQUAL.

Example {EX} in the chapter code tab lets you change the numbers and watch the verdict change.""",
8: """The script execution stack is a pile in which items are pushed on top and taken from the top, last in and first out. Every operation works on the top items.

A simple script such as 2 3 OP_ADD 5 OP_EQUAL adds two numbers and compares the sum with a third. It is the smallest complete example of a lock that checks a condition.

Output and input scripts are executed separately. The two scripts run apart, and only the stack passes from the first to the second. Slide 9 shows what went wrong when they were joined.

A script is a list of data items and operation words. Remember that the words are fixed by the protocol, whereas the data items are chosen by the people who write the lock and the spend.""",
9: """In 2010 the software joined the input script and the output script into one program before running it. An input script of OP_1 followed by OP_RETURN stopped that program at once with a true result, whatever the lock demanded, so the coin could be spent without knowing its secret. That is the first row of the result table: OK, meaning that anyone could spend.

Today the two scripts run apart. The same input still fails, now with OP_RETURN as the error, and only the real secret opens the lock, in both engines.

The design lesson is to run what a stranger supplies separately from the rule it must satisfy, and to treat anything unknown as a failure. Slide 10 tells the history of the bug.""",
10: """On 28 July 2010 two bugs in Bitcoin's script handling were shown on the test network. One of them let a stranger spend coins that were not theirs. The cause was that the first software joined the input script and the output script into one program, so an input script of 1 followed by OP_RETURN ended the run with a true result before the lock was ever tested.

Satoshi Nakamoto's fix, released in version 0.3.5, split the two scripts apart for good, which is the behaviour slide 9 reproduces. Many unused opcodes were disabled as well. In tapscript, unknown opcodes such as OP_LSHIFT (152) are now OP_SUCCESS, a different safeguard explained later in the chapter.

The picture is a bust of Satoshi Nakamoto in Budapest by Fekist, CC BY-SA 4.0.""",
11: """A stack is the pile of items on which a script works. New items go on top and operations take their inputs from the top, like plates in a cafeteria.

A language is Turing complete if, given enough time and memory, it can compute anything a computer can. Script is not, because it has no loops, and that is a design decision.

The output script is the lock that the payer places on a coin when creating it.

The input script is the data a spender shows to open that lock.

These two names are used throughout the book, and slide 12 gives their older names. You can compare the stack with the call stack of a programming language such as Python.""",
12: """The scriptSig is the older name of the input script. It was called a signature script because in the first and most common kind of spend the data it carries is a signature and a public key.

The scriptPubKey is the older name of the output script, because the lock was usually placed on a public key or on the hash of one.

Both names still appear in code, in the output of Bitcoin Core and in older books, so it is worth recognising them. A simple way to remember them is that the scriptSig sits in the input that spends, and the scriptPubKey sits in the output that is spent.

Modern descriptions say input script and output script, because the content is no longer always a signature or a public key. Slide 11 introduced the newer names.""",
13: """A key lock is a safe-deposit box labelled with a fingerprint. Anyone can read the label, but only the holder of the matching key opens the box.

This second part moves from the language to its most common use. Key and key hash explains how a coin is locked either to a public key directly or to the hash of one, and why the hash is the usual choice. Checking signatures explains how a signature is tied to this particular transaction and how it is written down in bytes.

The part leads into multisignatures, which replace the single key by several keys.""",
14: """Pay to public key hash, written P2PKH, locks a coin to the hash of a public key instead of the key itself. The spender later shows the key and a signature, and the node checks that the key matches the hash. Legacy addresses that begin with 1 are of this kind.

A public key hash is a 20-byte fingerprint of a public key, made with SHA-256 followed by RIPEMD-160. The chapter's library calls this hash160.

OP_CHECKSIG checks one signature against one public key and leaves true or false on the stack.

Slide 15 tries the lock with the right key, a wrong key and a changed amount.""",
15: """The first box builds a P2PKH lock. It is exactly 25 bytes long: OP_DUP, OP_HASH160, the 20-byte key hash, OP_EQUALVERIFY and OP_CHECKSIG, and the library classifies it as pubkeyhash.

The second box spends it in three ways. With the right key signing the real transaction, the result is OK. A signature from another key does not verify against the key in the lock, and a changed amount no longer matches what was signed, so both end in EVAL_FALSE.

The point to remember is that a signature is more than proof of owning a key: it also commits to the transaction, so changing the amount breaks it. Slide 16 names what exactly is signed, and chapter 8 treats signatures in depth. Example {EX} lets you change the signer or the amount.""",
16: """The signature hash is the digest of the transaction that a signature really signs. A signature does not cover the raw transaction directly. It covers this digest, which is made by following the signing rules.

The hash type is a one-byte flag added to the signature that says which parts of the transaction the digest covers, for example all inputs and outputs or only some of them. Chapter 8 returns to these flags, called SIGHASH flags.

DER, the Distinguished Encoding Rules, is the strict byte format in which a signature is written, so that every node reads the same bytes.

Slide 17 measures a real DER signature, and slide 18 tells what happened when nodes disagreed about the format.""",
17: """The first box signs the message 'pay Bob' with secret key number 1, which gives a DER-encoded signature. The second box adds the hash-type byte. The result is 72 bytes long, begins with 0x30 (48), the byte that marks a DER sequence, and has a low s value. Low s is the rule that of the two valid forms of s only the smaller is accepted.

The third box shows why the encoding is a consensus rule. A padded signature, with extra leading zero bytes, passes under the older loose rules but fails with SIG_DER once the strict DERSIG rule is switched on.

Nodes must agree on every byte they accept, otherwise the network splits. Slide 18 tells such a case from 2015, and chapter 8 explains the two forms of s.""",
18: """On 4 July 2015, at block 363,725, Pieter Wuille's BIP66 took effect and made strict DER signatures a consensus rule. A fork of six blocks followed. About half of the hash rate was mining without fully validating, so those miners built on an invalid block from a miner that had not upgraded.

The fork lasted from 02:10 to 03:50 UTC. A second fork of three blocks followed on 5 July, and the first fork showed no double spend. Bitcoin Core 0.9.5 and later checked the rule and were unaffected. The lesson is that a rule you do not check protects nobody, which connects back to slide 17.

The photograph shows a bitcoin mining farm in 2014 by Marko Ahtisaari, CC BY 2.0. The bitcoin.org notice linked on the slide is the primary account.""",
19: """A multisignature is a vault that opens when enough directors turn their keys. This part covers scripts that ask for t signatures out of k keys, such as two out of three.

The t-of-k script shows the shape of such a lock and how large it may grow, because every public key takes space in the output. The extra element explains a historical oddity: the CHECKMULTISIG opcode removes one item too many from the stack, so one useless item must sit in front of the signatures.

Multisignatures serve shared wallets, escrow and company treasuries. Slide 21 tests a 2-of-3 lock, and the next parts show how pay to script hash and taproot make such locks cheaper.""",
20: """A scripted multisignature is a script that wants t signatures out of k listed public keys, so no single key can spend alone.

The oddity in CHECKMULTISIG is an old bug: the opcode takes one more item off the stack than it needs, so the spender must put one dummy element in front of the signatures. Repairing it would have changed the consensus rules, so it stayed, and later the dummy was required to be empty. That is the error SIG_NULLDUMMY on slide 21.

Multisignature in general means that more than one key must approve a spend. The idea is older than Bitcoin: banks already asked for two signatures on large cheques.

Slide 21 puts a 2-of-3 lock to the test.""",
21: """The lock lists three public keys and asks for two signatures. In the first box the signatures of keys 0 and 2, given in the same order as the keys, are accepted. The same two signatures in swapped order fail, because the opcode walks through the keys once and never goes back. One signature alone is too few and ends in an invalid stack operation.

The second box shows that the extra dummy element must be empty. A dummy with content is refused with SIG_NULLDUMMY.

The script is 105 bytes long, mostly three public keys. To remember the rules: signatures follow the order of the keys, and one empty item leads. Example {EX} in the chapter code tab lets you try other combinations of keys.""",
22: """OP_CHECKMULTISIG checks t signatures against k public keys, in order. It takes the first signature, searches the keys from the first unused one onward, and then continues with the next signature, which is why signatures must follow the order of the keys.

The dummy element is the unused item that the extra pop consumes. It must be empty, a rule called NULLDUMMY. The rule also closes a way of changing a transaction's identifier without changing its meaning, which is called malleability.

Slide 20 describes the oddity, and this slide names the part that carries it. In pay to script hash, introduced next, the long list of keys stays hidden until the coin is spent.""",
23: """A script hash is a sealed envelope that shows only a code number. In pay to script hash the payer locks a coin to the hash of a script, and the script itself is revealed only when the coin is spent.

Hashing the script covers how the lock holds just the hash and how the full script, called the redeem script, appears at spending. What the hash changes covers who pays for the size. A long multisignature script no longer burdens the payer, and different validation rules apply to the revealed script.

P2SH comes from BIP16 and gives addresses that begin with 3. Compare it with slide 14, where the lock held the hash of a key. Here it holds the hash of a whole script.""",
24: """Pay to script hash, P2SH, locks a coin to the hash of a whole script instead of the script itself. It generalises pay to public key hash, which hashes only a key.

P2SH addresses begin with the digit 3 and stand for a script hash, so a payer can send coins to a multisignature without seeing or understanding its script.

The benefit is a short lock for the payer. Whoever pays writes a small output of fixed size, while the spender carries the long script and pays for its size when spending. The fee falls on the party who gains from the complexity.

Slide 25 shows a real 23-byte lock and two reveals.""",
25: """The lock is 23 bytes long: OP_HASH160, a 20-byte hash and OP_EQUAL, however long the script behind it is. The address made from it begins with 3.

In the second box the spender reveals the redeem script, a 2-of-3 multisignature, and the spend is accepted because the script hashes to the value in the lock and then runs successfully. A different script, whose hash does not match, fails with EVAL_FALSE even if it would have succeeded on its own.

So a node does two things in order: it checks the hash and then it runs the revealed script. The cost of the long script moves from the payer to the spender. Example {EX} lets you try other scripts.""",
26: """Redeem script and validation describes what a node does with a P2SH spend. The spender reveals the script, the node hashes it and compares the result with the lock, and only then runs it with the other data supplied.

The redeem script is the script whose hash locked the coin. It stays off the chain until the coin is spent, which also keeps the payer's output small.

A P2SH address is the hash in the lock written in Base58Check, with a version byte and a checksum that catches typing mistakes. Addresses of this kind start with 3, so they are easy to recognise. Base58Check is also used by the older addresses that start with 1.""",
27: """A timelock is a post-dated cheque, and a data output is a note on a noticeboard. This part covers two uses of scripts that are not about who may spend.

Recording data explains how a few bytes of data go on the chain in an output that nobody can spend. Absolute timelocks make a transaction or a coin wait for a fixed time or block height. Relative timelocks make a coin wait for an age, counted from the day it was mined.

The two kinds of waiting live in different places. Lock time is a field of the transaction, while the script words OP_CHECKLOCKTIMEVERIFY and OP_CHECKSEQUENCEVERIFY make a coin demand a wait. Slides 29 and 31 test one of each.""",
28: """A data recording output uses OP_RETURN to make an output that carries a few bytes of data and can never be spent, so nodes need not keep it as a spendable coin.

Transaction lock time has a limit. It stops one transaction from being valid too early, but it does not stop the owner, who can spend the same coin in a different transaction. It cannot lock the coin itself.

OP_CLTV, short for OP_CHECKLOCKTIMEVERIFY, puts the rule inside the script: this coin is not spendable before a time or height.

Relative timelocks count the wait from the day the coin was mined, not from a fixed date.

Slide 29 tests OP_CLTV, and slide 31 tests the relative lock.""",
29: """The script says that the coin may not be spent before block 800,000, and three spends are tried. In the first, the transaction's lock time is 800,000 and its sequence is below the maximum value 0xffffffff, so it is not final: the lock time is switched on and the check passes. With a lock time of 799,999, one block too early, the check fails. In the third spend the lock time is right but the sequence is final, which tells nodes to ignore the lock time, so the script fails with UNSATISFIED_LOCKTIME.

In short, the lock time of the transaction must reach the number in the script, and the sequence must not be final. A lock time below 500,000,000 is read as a block height, and above it as a Unix time. Example {EX} lets you try other values.""",
30: """Relative timelocks with OP_CHECKSEQUENCEVERIFY, called OP_CSV, is the script rule that enforces a relative wait. The sequence of the spending input must show an age at least as large as the number in the script.

OP_RETURN is the word that ends a script in failure, which is why an output that starts with it can never be spent. It also marks outputs that carry data.

A data carrier output is the relay policy's name for an OP_RETURN output. Policy decides what nodes pass along and is not part of consensus.

Lock time is a transaction field holding the earliest time or block at which the transaction may be included.

Absolute waits use lock time and CLTV, and relative waits use sequence and CSV.""",
31: """The script demands a wait of 4,320 blocks, about thirty days at ten minutes a block. A version 2 transaction with an input sequence of 4,320 passes. One block short, at 4,319, fails with UNSATISFIED_LOCKTIME, and so does the same sequence in a version 1 transaction, because relative locks are enforced only from transaction version 2. In the third box, setting bit 31 (0x80000000) of the sequence switches the relative lock off, and the script then fails.

Compare slide 29. There the absolute lock time was read from the transaction, whereas here the age is read from the sequence of each input. Relative waits are the basis of designs such as payment channels. Example {EX} lets you change the numbers.""",
})

RN7.update({
32: """OP_CHECKLOCKTIMEVERIFY is the full name of OP_CLTV, the script word that keeps a coin unspendable until a time or block height. OP_CHECKSEQUENCEVERIFY is the full name of OP_CSV, the word that keeps it unspendable until it has reached a certain age. The long names say what each word does: it checks the lock time, or the sequence, and it verifies, which means that the script fails at once if the check does not hold.

The sequence is a field of each input. Its uses include the relative wait, which is why OP_CSV reads it. On slide 29 the sequence only had to be not final.

Keep the pairs together: lock time goes with CLTV and means a date or a height, and sequence goes with CSV and means an age.""",
33: """Flow control is a fork in the road with a checkpoint on each path. A script can choose between several ways of being spent, and it can stop early when a check fails.

Conditionals and guards covers the branches that choose a path, written with IF, ELSE and ENDIF, and the VERIFY words that stop a script when a check fails. Complex scripts covers a real lock that mixes partners, a lawyer and delays. It is Mohammed's capital account from the book, built and tested on slide 35.

That example combines multisignatures, relative timelocks and flow control, so this part is also a revision of the earlier ones.""",
34: """Flow control lets a script choose between several paths, so one output can have more than one way of being spent.

VERIFY words stop the script at once when a check fails, instead of leaving a false value on the stack for a later step to find.

In practice, IF, ELSE and ENDIF select which one of several spending paths runs, depending on a value that the spender supplies.

The complex example is Mohammed's capital account. Either the partners spend together, or a lawyer spends after a delay. Slide 35 builds it and tests every path, and slide 36 names the opcodes behind it more closely.""",
35: """Mohammed's capital account is one script of 192 bytes with three ways of being spent. Path one needs two of the three partners and no waiting. Path two lets the lawyer and one partner spend after 4,320 blocks, about thirty days. Path three lets the lawyer alone spend after 12,960 blocks, about ninety days. Each path works only after its wait, and asking one block early fails with UNSATISFIED_LOCKTIME, as the table shows.

The script picks its path from a value that the spender supplies, which IF and ELSE read. The example combines three earlier ideas: the multisignature of slide 21, the relative timelock of slide 31 and flow control. Example {EX} lets you change the waits.""",
36: """OP_IF runs the next clause only if the top item of the stack is true. With OP_ELSE and OP_ENDIF it forms a branch.

A conditional clause is one branch of a script that runs only under a condition, such as the partners' path or the lawyer's path on slide 35.

OP_VERIFY fails the script unless the top item is true. Many words have a VERIFY form, such as OP_EQUALVERIFY, which compares and then verifies in one step.

Miniscript is a structured language that compiles to Script and can be analysed, so tools can check the spending paths and the cost of a lock before it is used. Hand-written scripts like Mohammed's are easy to get wrong, which is why it is worth knowing. The Bitcoin Optech topic page on Miniscript is a good place to continue.""",
37: """Segregated witness moves the proof to a window beside the counter. The signatures and other proofs of a spend, called the witness, are kept apart from the part of the transaction that gives it its identifier.

Witness programs explains how a segregated witness lock is written and addressed. The upgrade explains how the change reached old nodes without splitting the network, which leads to the idea of a soft fork on slide 44.

This is the largest part of the chapter, with sixteen concepts on the map of slide 4.""",
38: """Segregated witness outputs and transactions are real examples of locks and spends in which the proof lives in the witness.

Pay to witness public key hash, P2WPKH, is the key-hash lock of slide 14 in a new form. The lock names the hash, and the signature and the key sit in the witness.

Wallet construction of P2WPKH describes how a wallet builds the output and the witness for a spend.

Pay to witness script hash, P2WSH, does the same for a script-hash lock. The script is revealed in the witness, which makes it the successor of P2SH from slide 25.

Slide 39 tests P2WPKH.""",
39: """A witness key-hash output can be spent directly, or wrapped in a P2SH output so that older wallets, which cannot send to the new addresses, can still pay it. Both give OK. In the second box the signed amount is changed and the spend fails with EVAL_FALSE, because a segregated witness signature commits to the amount being spent.

The third box builds the 22-byte witness program, made of a version byte and a 20-byte hash, and encodes it as a bech32 address, which begins with bc1q.

Compare slide 15. The idea of the lock is the same, but the proof moved and the signature covers more. Example {EX} lets you change the amount.""",
40: """The chart shows what real coins are spent from. The chapter's own interpreter ran every input of the first 599 non-coinbase transactions of block 775,072, which makes 1,022 inputs, using bytes from mempool.space, and sorted the inputs by the kind of output they spend. Coinbase transactions are left out because they create new coins and have no earlier output to classify.

Witness key hashes lead, and taproot is still rare. So most real coins already move through witness programs.

The chart is a sample of one block, not a statistic for the whole chain, so read the proportions as a snapshot. You can repeat the check on any block with the chapter's library and an explorer such as mempool.space.""",
41: """The program length tells P2WPKH and P2WSH apart: a 20-byte hash means a key-hash lock, and a 32-byte hash means a script-hash lock.

Upgrading to segregated witness is about how old and new software live side by side. Old nodes treat witness outputs as outputs whose rules they do not examine, so they still accept the blocks.

Embedding segregated witness inside P2SH wraps a witness program in a script hash, so that wallets which cannot yet pay to the new addresses can still pay to it.

Nested P2WPKH is P2WPKH placed inside P2SH. Its address begins with 3, although the spend uses a witness.

Slide 44 explains the kind of fork behind the upgrade.""",
42: """Nested P2WSH is P2WSH placed inside P2SH. It is the same device as on the previous slide, now for script-hash locks.

Segregated witness is the upgrade that moves signatures out of the data from which the transaction identifier is made. For spends that use a witness, that removes a source of malleability, because nobody can change the identifier any more by re-encoding a signature.

A witness program is the version number and the hash that lock a segwit output.

P2WPKH is the short name of pay to witness public key hash.

Slide 43 completes the vocabulary, and slide 44 explains why old nodes keep following the chain.""",
43: """P2WSH is the short name of pay to witness script hash. In the two short names, P2WPKH and P2WSH, the first letters say that the lock is a witness lock, and the rest says whether it holds a key hash or a script hash.

Bech32 is the segwit address format. Its checksum finds typing mistakes more reliably than Base58Check, and the addresses are written in lower case and begin with bc1.

Nested segregated witness is segwit hidden inside the older script hash format, which is why such addresses begin with 3.

A soft fork is a rule change that old nodes still accept. Slide 44 compares it with a hard fork.""",
44: """A hard fork loosens the rules. Blocks that old nodes reject become valid, so every node must upgrade or the chain splits in two. A new road standard that old cars cannot use is a fair picture.

A soft fork tightens the rules. New nodes reject more than before and accept nothing new, so old nodes still follow the chain and accept its blocks. It is like a stricter speed limit that old cars can still obey.

Segregated witness was activated as a soft fork. Because it only restricts what is valid, nodes that did not upgrade carried on, although they no longer checked the new rules themselves. Remember the lesson of slide 18: a rule that you do not check protects nobody.""",
45: """A script tree is a menu of which only the ordered dish is shown. Many spending rules can be committed to with a single hash, and a spender reveals just the one rule they use.

Script trees covers how many spending rules hide behind one hash. Key tweaks covers how a key is changed a little to commit to hidden data, so that the key itself carries a promise about that data.

Both ideas are the building blocks of taproot, which is the next part, so this part is best read before it.""",
46: """A Merklized alternative script tree, MAST, puts many scripts under one hash, and a spend shows only the one it uses. A Merkle tree is a tree of hashes in which every node is the hash of its children.

Pay to contract, P2C, tweaks a key so that it commits to a contract, which can later be shown to prove what the key promised.

Scriptless multisignatures and threshold signatures let many signers combine into one key and one signature, so that the chain sees no script at all.

MAST is simply the short name of the script tree. Slide 47 counts the hashes that a proof needs.""",
47: """A spend from a script tree shows the chosen script and a proof, which is the list of sibling hashes leading from its leaf up to the top of the tree. Mohammed's three scripts need proofs of 2, 2 and 1 hashes. The second box computes the depth of trees of 3, 8, 1,024 and about a million scripts. The depth grows with the base-two logarithm, so a tree of 1,048,576 scripts needs only 20 hashes in a proof.

That is why a huge number of spending rules can sit behind one hash at little cost. Compare slide 25: P2SH reveals the whole script, whereas a script tree reveals one leaf and a short proof. Example {EX} lets you change the number of scripts.""",
48: """A Merkle root is the single hash at the top of a tree of hashes. Changing any leaf changes the root, so the root commits to every leaf.

A membership proof is the list of sibling hashes that proves a leaf belongs to the tree. The verifier recomputes the root from the leaf and the proof and compares it with the root it knows.

A key tweak is a small number, derived from a hash, that is added to a key. The new key then commits to the hashed data.

A scriptless multisignature is a joint signature that shows no script at all. Compare it with the scripted multisignature of slide 21, where every key is visible on the chain.

The first two cards make slide 47 work, and the third underlies slide 52.""",
49: """A threshold signature lets any t of n holders sign for one shared key. Outsiders see one key and one signature, and not the t of n.

A partial public key is one signer's share. Added to the others, the shares make the joint public key.

Both cards continue the idea of the scriptless multisignature on the previous slide: the group structure is kept off the chain, and the chain checks one ordinary signature.

Simply adding keys has a danger, because one signer can choose a share that cancels the others. Chapter 8 explains why keys that simply add up are unsafe and what MuSig2 changes.""",
50: """Taproot is a front door with a hidden side entrance. The output is one key. The owner may spend it with a plain signature, which is the front door, or by revealing one script from a hidden tree, which is the side entrance.

Taproot outputs covers the single output key that can be spent either way. Tapscript covers the script rules that apply inside a taproot spend, which differ in small ways from the older Script.

This last part brings together the ideas of the previous ones: the script trees of slide 47, the key tweaks of slide 48 and Schnorr signatures, which chapter 8 treats in full.""",
51: """Taproot is an output that is a key, which may hide a script tree. Tapscript is the set of script rules that apply inside taproot spends.

Key path spending uses one signature for the output key, and nothing else is revealed.

Script path spending reveals one leaf script, its proof and its data, so only the branch that is used becomes public.

The two ways correspond to the front door and the side entrance of the divider. Slide 52 tests the key path, and slide 55 tests the script path.""",
52: """In the first box the internal key, key number 1, is tweaked with an empty script tree, which gives the output key: 32 bytes, in an address that begins with bc1p. The output key is the internal key plus a tweak, and here there is no script at all.

In the second box the output is spent along the key path with one signature of 64 bytes, in 308 weight units, and the result is OK. A key that was not tweaked as the output says is refused with SCHNORR_SIG.

The prefix helps recognition: bc1q marks a version 0 witness program, as on slide 39, and bc1p marks version 1, which is taproot. Slide 53 tells the history, and chapter 8 explains Schnorr signatures. Example {EX} lets you try other keys.""",
53: """At block 709,632, mined on 14 November 2021, the taproot rules took effect together with Schnorr signatures. They are specified in BIPs 340 to 342. BIP340 was assigned in January 2020, and a soft fork then added taproot and tapscript to the running chain.

Claus-Peter Schnorr had patented his signature, which kept it out of open standards for almost two decades, so ECDSA was used instead. A key path spend is one 64-byte signature that looks the same whether one person or a million made it, which connects to the threshold signatures of slide 49.

The portrait shows Claus-Peter Schnorr in 1986, by Konrad Jacobs, CC BY-SA 2.0 de. The mempool.space link on the slide leads to a live view of the chain.""",
54: """The taproot internal key is the key before the tweak is added. The taproot output key is the tweaked key that appears in the output: the internal key plus a number derived from the script tree.

A leaf script is a script at the end of a branch of the tree, and it is the thing that a script path spend reveals.

OP_CHECKSIGADD adds one to a counter for each valid signature, which is how tapscript counts signatures. Slide 57 shows it at work.

To keep the two keys apart, recall that they differ by the tweak (slide 52), and that anyone can recompute the output key from the internal key and the tree.""",
55: """Each of the three leaves of Mohammed's account script can be spent through the script path, and all three verify. The chart compares the weight of each spend in two ways: the orange bars are the taproot script path, and the green bars are the same path as an ordinary witness script hash. Weight units are the unit in which block capacity is counted. Each path costs about as much as a plain witness script.

So taproot does not make script spends much cheaper in this example. The script path reveals only the leaf that is used and a proof, whereas the witness script hash reveals the whole script. The large saving comes when all parties agree and use the key path of slide 52. Example {EX} lets you change the path.""",
56: """A Schnorr signature is a short signature that adds up when many signers sign. The signatures and keys of several people can be combined into one signature and one key.

OP_SUCCESS marks opcode values that make a tapscript succeed at once. They are kept free for upgrades, because a soft fork can later give them a meaning. Slide 58 shows how this works.

Mutual satisfaction means that all parties agree, so the script never needs to be shown. They sign together on the key path, and the rules for a dispute stay hidden, like a contract that is never taken to court.

Chapter 8 treats Schnorr signatures in full.""",
57: """In tapscript the t-of-k rule works as a counter. For each public key in turn, OP_CHECKSIGADD adds one to the counter if the signature is valid, and an empty slot adds nothing. At the end the counter is compared with t.

A 2-of-3 lock written this way is 104 bytes, one byte shorter than the old CHECKMULTISIG form of 105 bytes on slide 21, and it needs no dummy element. Two valid signatures and one empty slot reach the count and give OK. One signature leaves the count at one, and the result is EVAL_FALSE.

Compare slide 20: the oddity that required an empty dummy is gone. Example {EX} lets you change which signatures are present.""",
58: """Of the 256 possible opcode values, 87 are OP_SUCCESS in tapscript, and a script that contains one succeeds on sight. The second box shows opcode 152, formerly the disabled shift OP_LSHIFT. In tapscript it makes the script succeed, but in an old script the same word fails with DISABLED_OPCODE.

It may sound unsafe for unknown words to succeed. The reason is upgrading: a later soft fork can give any of these words a meaning under which some scripts fail, which is a tightening, so old nodes keep accepting the blocks. This is the soft fork idea of slide 44 applied to the language itself, and slide 10 mentioned the same words. Example {EX} lets you try other opcode values.""",
59: """The five lines summarise the chapter, one line for each group of parts, and each can be proved from its slides.

A coin is locked by a script, the spender's script is the key, and the two run apart on a stack. Key hashes, multisignatures and script hashes lock a coin to what the spender can prove and move the long lock to the spender. Lock time and sequence make a spend wait, and flow control gives one output several ways out. Segregated witness moves the proof out of the identifier, as a soft fork that old nodes accept. Taproot commits to a tree of scripts with one key, so agreement looks like a single signature.

If a line feels unproven, the code slide of its part carries the receipt.""",
60: """Everything on this slide is free to read or watch, and each entry is a live link in the file. The groups form a path. Read and explore starts with the Bitcoin white paper, the Bitcoin Wiki pages on Script and on taproot, and the Optech summary of taproot. Standards are the authoritative texts: BIP 66 for strict DER signatures, BIP 141 for segregated witness, and BIPs 341 and 342 for taproot and tapscript.

The stories give the primary sources for slides 10 and 18: the early script engine, the entry for the 2010 bug and the 2015 miner alert. The community entries are where questions get answered, and the two Optech workshops are videos on Schnorr signatures and on tapscript.

The course page for chapter 7 carries the full text behind every slide.""",
61: """These four statements are what you should be able to say after the chapter: how a lock and a key decide a spend, how signatures and script hashes are checked, how timelocks shape who spends and when, and what segregated witness and taproot change.

Each is carried by a computation that ran on a slide of this deck, and slide 59 lists where. A statement you cannot yet say in your own words sends you back to that slide.

The course page for chapter 7 has every word behind the slides, the stories with their sources and the question bank for testing yourself. Bring remaining questions to your instructor, and use the community links on slide 60.""",
})

RN8.update({
1: """This is chapter 8 of Mastering Bitcoin, third edition. It explains what a digital signature proves and commits to, how Schnorr and ECDSA signatures work, and what has moved since the book went to print. The picture is the Bitcoin logo, which is in the public domain.

Every result was computed with the chapter's own Python library under Python 3.14.6. The answers of Bitcoin Core 31.1.0 were recorded once on a test network and are only read back in this deck, not run again. Each code slide has a twin in the chapter code tab of the course page, where you can change the listing and run it.

In chapter 7 a signature opened a lock. Here the signature itself is opened up.""",
2: """After the questions and the concept map, seven parts follow: the foundations of digital signatures, the signature hash flags called SIGHASH, Schnorr signatures, ECDSA signatures, randomness and signature size, signing in segregated witness, and what has changed since the book went to print. Each entry on the slide shows the slides where it lives, so you can jump straight to it.

The figures summarise the deck: fifty-one slides, twenty code examples that each end in a picture of the result, and three true stories.

The table on every divider slide repeats the route, so you always know which part you are reading. Chapter 7 is a good companion, because it shows where these signatures are checked.""",
3: """These seven questions are the chapter's own competency questions. Each has its answer on a slide, and the closing slide returns to them.

Use them as a self-test. The first asks what a verifier must have, and belongs to the foundations. The second concerns the SIGHASH flags and a bug in the flag called SINGLE. The third and fourth belong to Schnorr signatures: how a three-move proof becomes a 64-byte signature, and why adding keys is unsafe and how MuSig2 helps. The fifth concerns ECDSA, which can take two forms of one signature, and the difference between what consensus and policy accept. The sixth concerns the nonce and RFC 6979. The seventh asks what segregated witness changed in what is signed.

If a word is unfamiliar, the course page for chapter 8 has an entry for it.""",
4: """The concept map shows the chapter as seven parts, with the number of key concepts and examples in each. Foundations has five concepts and three examples, SIGHASH eight and three, Schnorr signatures sixteen and five, ECDSA eight and three, randomness and signature size four and three, and segwit signing four and two. The last part, since the book went to print, has one example and the dates.

The counts show where the weight lies: Schnorr signatures carry the most concepts, because the book builds them up from a proof in several steps. The examples add up to twenty.

Every later slide belongs to one of these parts. The same map is on the course page, where you can filter it and open each concept.""",
5: """A signature is a wax seal that only the owner of the ring can press. Anyone can look at the seal, but only the owner can make it.

This part has three themes. What a signature does: three inputs go in, a message, a public key and a signature, and a yes or no comes out. Arithmetic of the curve: two moduli are used, and scalars wrap at n while coordinates wrap at p. Signing a transaction: what is signed is not the transaction itself but a digest of it.

The table at the bottom marks where this part sits among the seven parts of the chapter.""",
6: """A digital signature is proof that the owner of a private key approved a message. It is the electronic counterpart of a seal, and anybody can check it.

To see how it works, note that the signer holds a secret, the private key, and everyone else checks the result with the matching public key. The checkers learn nothing about the secret.

To create a signature, the signer combines three things: the digest of the message, the secret key and a nonce, a number used once. The next slides show why the nonce matters so much.

Slide 7 makes these ideas concrete with a real signature and three checks.""",
7: """The first box makes a secret key and a message, derives the public key that follows from the secret, and signs the message. The public key is what others hold. The second box makes two altered inputs: the message with one bit flipped, and a different public key. The third box defines a small function, accepts, that asks the library to verify the signature for a given key and text, and tries three cases.

Only the unchanged triple of message, key and signature is accepted. Changing the message or the key gives False. The signature is 70 bytes long.

This answers the first question of slide 3: a verifier needs the message, the public key and the signature, and then it can say yes or no. Example {EX} lets you flip other bits.""",
8: """Verifying the signature takes the message, the public key and the signature as inputs and gives yes or no. The verifier needs no secret.

The discrete logarithm problem explains why a public key is safe to publish. Given a point on the curve, finding the number that produced it is infeasible. A public key is such a point, and the secret key is that number, so the key can be shown to everybody.

Signature schemes rest on this problem together with hash functions. Slide 7 verified with the first idea, and slide 10 will show the second at work.

If you want to remember the pair: signing needs the secret, verifying needs only what is public.""",
9: """Two moduli are used, and they are two clocks of different sizes. A remainder keeps a number inside a fixed range, like the hours of a clock, and 5 divided by 3 leaves 2. The group order n and the field prime p are different 256-bit numbers, which differ by a number of 129 bits.

The result table shows why this matters. The response s is reduced modulo n and modulo p, and the equation sG = kG + eX holds only when it is reduced modulo n. The book says that everything is modulo p, but the response must be reduced modulo n.

A good rule is that the coordinates of points live modulo p, while secret keys, nonces and responses live modulo n. Example {EX} lets you try other numbers.""",
10: """The signature covers a hash of the transaction, not the bytes themselves. The first box builds two identical transactions of two inputs and two outputs, and then raises one output amount of the second by one satoshi. The second box defines a function that computes the digest that is signed for the first input and shows its first twelve hexadecimal digits.

The result is the point of the slide. The same bytes give the same digest, 18bdeda48b41, twice. One satoshi more gives a different digest, ff64b81fb946, so the old signature no longer fits.

Remember that any change to the covered bytes changes the digest. The SIGHASH flags of the next part decide which bytes are covered. Example {EX} lets you change other fields.""",
11: """A flag chooses how much of the letter the seal covers. Part three is about the signature hash flags, called SIGHASH, which tell the verifier which fields of a transaction the signature commits to.

How flags are coded: a flag is one byte appended to the signature. Commitments by flag: each flag fixes some fields and leaves others open, so a signer can allow others to add inputs or change outputs. Known pitfalls: a flag called SINGLE signs the number one when no matching output exists, which slide 16 demonstrates.

Remember that a signature without a flag choice is a signature with the default, which commits to everything. The table at the bottom marks this part among the seven.""",
12: """Signature hash types, called SIGHASH, are one byte that says which parts of the transaction the signature covers.

The signature hash is the digest of the transaction fields that is actually signed, made after the covered fields have been chosen by the flag.

SIGHASH_ALL signs all inputs and all outputs. It is the default and the safest choice, because nothing can be changed afterwards.

SIGHASH_NONE signs the inputs but no output. The signer commits to spending these coins and leaves the destination open, so anybody can decide where they go.

Slide 13 shows how the flag is coded, and slide 14 completes the list.""",
13: """A flag is one byte. The first box lists the three base flags, SIGHASH_ALL, SIGHASH_NONE and SIGHASH_SINGLE, which are the numbers 1, 2 and 3. The second box takes the modifier, SIGHASH_ANYONECANPAY, which is 128, the top bit of the byte. The third box adds the modifier to every base flag with the bitwise or operator and prints the result: 129, 130 and 131.

Because the modifier is a single high bit, it combines with every base flag. Six flag values result: three base flags, alone and with the modifier. These are the six values probed on slide 15.

To remember it, the low bits choose the outputs and the top bit chooses the inputs. Example {EX} lets you print the values.""",
14: """SIGHASH_SINGLE signs only the output with the same number as the input being signed. The signer commits to one output and leaves the others open.

SIGHASH_ANYONECANPAY signs only this input, so that others may add theirs. This is the flag behind transactions to which many people contribute coins.

BIP118 is a proposal for signatures that leave out the coin they spend. It is a proposal, and not part of Bitcoin's rules today.

SIGHASH_DEFAULT is taproot's zero byte. It means the same as SIGHASH_ALL and is left out of the signature, which keeps a taproot signature at 64 bytes.

Slide 15 measures what each flag commits to, and slide 16 shows a bug in SINGLE.""",
15: """The first box lists six flags: the three base flags, alone and with the ANYONECANPAY modifier. The second box probes five parts of a transaction. For each flag it changes one field at a time and checks whether the digest moves; a field that moves the digest is covered by the flag. The third box counts the covered fields for each flag.

ALL covers five of the five fields. NONE with ANYONECANPAY covers only one. The field pattern in the result text, such as ....Y., marks which fields are covered.

Only plain ALL covers every probed field, including the sequence numbers of the other inputs. The other flags leave something open for others to change. Example {EX} lets you probe other fields.""",
16: """The first box builds a transaction with three inputs and only one output. SIGHASH_SINGLE signs the output with the same number as the input being signed. Input 0 has an output, but inputs 1 and 2 have none. For those two, the legacy algorithm signs the constant number one instead of a real digest. That is why their digests begin with 01000000, the number one written in bytes, and why the third box prints False for input 0 and True for the other two.

A digest that is always the number one can be reused on any transaction, so a signature made this way commits to nothing. The book does not mention this bug. The slides on segwit signing show how the newer algorithm changed what is signed. Example {EX} lets you add outputs.""",
17: """Schnorr is a seal whose imprints can be added together. This part builds up the scheme in four steps.

Proof to signature shows how a three-move proof becomes a signature by hashing. The BIP340 format covers the fixed sizes, the x-only keys and the tagged hashes of the Bitcoin version. Aggregating keys shows that keys and signatures add up, with one trap that slide 26 demonstrates. Threshold sharing shows that any two of three key holders can sign.

Chapter 7 told why this matters: taproot spends with a key path, one signature that hides how many people signed. This part explains that signature.""",
18: """A Schnorr signature is a number s = k + e x, built from a secret nonce k, a challenge e and the secret key x. One equation on points proves it.

The serialization of a BIP340 signature is 64 bytes: the x coordinate of the point R and the number s.

Schnorr-based scriptless multisignatures let several signers produce one ordinary signature, so the chain sees a single key and a single signature.

Schnorr-based scriptless threshold signatures do the same when only a subset of the key holders signs.

Compare the scripted multisignature of chapter 7, slide 21, where every key and signature was visible on the chain. Slides 19 and 21 build up the equation.""",
19: """The book first explains Schnorr with whole numbers. The toy run uses the secret x = 3, the generator G = 5, the nonce k = 7 and the challenge e = 11. The point of a number is just five times it, so the public key xG is 15 and the commitment kG is 35.

The response is s = k + e x = 7 + 33 = 40. The verifier checks that sG = kG + e xG, which is 200 = 35 + 165, and the check holds.

The danger is on the last line: dividing the public number xG by G returns the secret 3. With points on a curve that division is impossible, which is why points are used. Example {EX} lets you change the numbers.""",
20: """The challenge e is the value that ties the nonce point to the message. In an interactive proof the verifier chooses it at random.

The Fiat-Shamir transform replaces the verifier's random challenge by a hash, so that the proof becomes a signature. Slide 21 shows it.

BIP340 is the specification of Schnorr signatures for Bitcoin. It fixes the sizes and the hashing, so that all wallets produce signatures that all nodes can check.

An x-only public key is 32 bytes: only the x coordinate, with an even y assumed. It is one byte shorter than the compressed key of ECDSA, as slide 24 measures.

Remember the order of the ideas: proof, challenge, hash, signature.""",
21: """A prover with the secret x publishes the point X = xG, picks a nonce k, sends the point R = kG and receives a challenge e. The prover answers with s = k + e x, and the verifier checks that sG equals R + eX. The honest response is accepted, and the response plus one is rejected.

The third box applies the Fiat-Shamir idea: the hash of the message plays the examiner, so no examiner has to be online. The signature on the message 'A' is accepted for 'A' and rejected for 'B', because a signature fits only the message whose hash chose the challenge.

The numbers are small toy values for readability. Slide 19 showed the same equation with whole numbers, and example {EX} lets you change the message.""",
22: """Claus-Peter Schnorr's signature scheme was patented in the United States as patent 4,995,082, published on 19 February 1991. The patent kept the scheme out of open standards, so ECDSA was the only signature that Bitcoin knew until 2021.

The term of the patent was the longer of 17 years from the grant and 20 years from the filing, so it ended on 23 February 2010. BIP340 is Schnorr's scheme fitted to the curve secp256k1, and it went live with taproot, thirty years after the paper. Chapter 7, slide 53, tells the same activation from the side of taproot.

The portrait shows Claus-Peter Schnorr at Oberwolfach in 1986, by Konrad Jacobs, MFO, CC BY-SA 2.0 de. The patent itself is linked on the slide.""",
23: """Linearity means that sums of keys and signatures are keys and signatures of the sum. It is the property that lets signers combine.

Batch verification checks many signatures with one combined equation, which is faster than checking them one by one.

Key prefixing puts the public key into the hash that makes the challenge, so that a signature is bound to the key that made it.

A scriptless multisignature adds the keys, so that no script is needed to count the signers. Compare chapter 7, slide 21, where OP_CHECKMULTISIG counted them.

The four ideas follow each other: linearity makes aggregation possible, batch verification saves work, key prefixing binds the signature, and the scriptless form hides the group.""",
24: """BIP340 keys are 32 bytes and signatures are 64 bytes. The first box makes a secret key and the hash of a message. The second box makes the BIP340 objects, an x-only public key and a 64-byte signature, and for comparison the ECDSA objects: the compressed public key and the signature of the same key. The third box verifies the Schnorr signature and lists the four sizes.

The Schnorr signature verifies, and it always takes 64 bytes. The x-only key saves one byte over the compressed key. DER signatures vary in size, as slide 41 shows.

Fixed sizes make fees easier to estimate and parsing simpler. Example {EX} lets you sign other messages.""",
25: """A key cancellation attack happens when a signer who sees the other public keys first picks a key that cancels them, so that the sum is a key that this signer alone controls.

MuSig2 aggregates keys with weights taken from a hash of all the keys, which defeats the attack. It needs only two rounds of messages between the signers.

Shamir secret sharing hides a secret as the height of a line and shares it as points on that line. Any two points give the line, and fewer than that give nothing.

A scriptless threshold signature lets any k of n signers produce one signature without a script.

Slide 26 shows the attack, and slide 27 shows the sharing.""",
26: """The table compares two ways of combining keys. Against a plain sum of keys, Bob can sign alone: yes, valid. Against MuSig2 weighted keys he cannot.

In the first box the attacker waits for Alice's public key and then publishes his own key minus hers. The plain sum of the two keys is then a key that he alone controls, so he signs for both of them. The second box runs the same attempt against MuSig2. Every key is weighted by a hash of all the keys, so Bob cannot choose a key that cancels Alice's, and the attack fails.

Remember that adding public keys is not enough. The group must bind each key to the whole group, which is what the weights do. Example {EX} lets you change the attacker's numbers.""",
27: """The secret, 31337, is the height of a line at zero. Three shares are points on the line. Any two points determine the line and therefore the secret, so every pair of shares gives 31337. One share alone gives 31414, which is not the secret.

The second box combines every pair, and the third box tries one share alone. A single share is consistent with every possible secret, so fewer shares than the threshold reveal nothing, and the threshold reveals everything.

This is the idea behind the scriptless threshold signatures of slide 25. Compare slide 26: there the danger was a dishonest signer, here the danger is losing shares. Example {EX} lets you change the secret.""",
})

RN8.update({
28: """ECDSA is the older seal, with a messier imprint and two valid shapes. It was Bitcoin's only signature from 2009 until Schnorr joined it in 2021, so the signatures in older transactions are all of this kind.

The part has three themes. The ECDSA equations: two formulas, and two valid values of s. DER serialization: a signature is written as nested length-prefixed fields. Consensus and policy: miners enforce the law, and nodes add house rules, a difference that slides 34 and 35 explain.

Compare this part with the Schnorr part before it, whose equation is simpler. The differences you meet here are the price of the older design.""",
29: """ECDSA signatures are the signature that Bitcoin used from 2009. Schnorr signatures joined them in 2021.

The ECDSA algorithm signs with a nonce and inverts it, and it verifies by rebuilding a point. The inversion is what makes ECDSA messier than Schnorr, whose equation s = k + e x needs none.

The serialization of ECDSA signatures, called DER, writes the pair R and s in nested length-prefixed fields.

ECDSA stands for Elliptic Curve Digital Signature Algorithm.

Slide 30 follows the algorithm with chosen numbers, and slide 32 takes a real DER signature apart.""",
30: """The first box takes toy values: the key x = 0x1234, the message hash h = 0x5678 and the nonce k = 0x9abc. It signs with that explicit nonce, where R is the x coordinate of the point kG and s follows from the book's formula. The second box defines verification: the library rebuilds a point K from s, R and the public key and compares it with R. The third box tries both s and n minus s.

Both verify. The smaller of the two is the low-S form, and here it is n minus s. If s verifies, so does n minus s, so the signature has two forms.

This is the malleability of slide 31 and the policy of slide 34. Example {EX} lets you try other nonces.""",
31: """R and s are the two numbers that make up an ECDSA signature.

Malleability means that anyone can alter a valid signature without the key. Replacing s by n minus s gives another valid signature on the same message, as slide 30 showed.

DER, the Distinguished Encoding Rules, is the byte layout of signatures. Chapter 7, slide 17, met it as a consensus rule.

The low-S rule says that of s and n minus s only the smaller is relayed.

The four cards belong together: two forms exist, which is malleability, a relay rule picks one of them, which is the low-S rule, and DER is how the chosen pair is written down.""",
32: """A real signature plus the one-byte hash type is 71 bytes, as it sits in a script. The library splits it into the nine elements that the book lists and counts the bytes of each. R and s take 32 bytes each, and the other seven elements take one byte each: the sequence marker, the total length, the integer marker and length of R, the integer marker and length of s, and the hash type. Strict DER accepts it.

The elements add up to the length of the whole signature. When the top bit of R is set, a zero byte is added in front and R takes 33 bytes, as slides 33 and 41 show. Example {EX} lets you cut other signatures.""",
33: """The long hexadecimal signature that the book dissects in its DER section is a real signature from a mined payment. It was mined in block 277,316 on 27 December 2013 at 23:11:54 UTC. A real example can be checked: the chapter recomputes it, and signature, key and transaction agree.

Its R has 33 bytes because its top bit is set, which is the case of slide 32. Its S is already the low form, so a node would still relay it today, as slide 34 explains.

No photograph exists, because nobody knows who sent this payment. The Bitcoin logo, by Grayliptrot and in the public domain on Wikimedia Commons, stands in. The mempool.space link on the slide opens the transaction itself.""",
34: """The first box takes one low-S signature and builds its twin by replacing s with n minus s. The second box defines two checks: is_valid asks whether the signature verifies, and is_low_s asks whether it has the low-S form. The third box applies both checks to the two signatures.

The low-S form is valid and relayed. The high-S twin is valid but not relayed. Miners accept both, because both are valid. Nodes relay only the low-S form, which is a stricter house rule.

Remember that valid is not the same as relayed. Consensus is the law, and policy is a stricter house rule. Slide 35 compares the two. Example {EX} lets you try other messages.""",
35: """Consensus decides what is valid. Every node must agree on it, or the chain splits, and a change needs a soft or a hard fork. It is like the law of the land.

Policy decides what is relayed. Each node may choose its own rules, and a change needs only a new release. It is like the house rules of a shop.

This is why a transaction can be valid and still not be relayed. Policy can change with a release, while consensus changes only by a fork, as chapter 7, slide 44, explained.

Two examples from this chapter: the low-S rule of slide 34 is policy, and the strict DER rule of chapter 7, slide 18, is consensus.""",
36: """The nonce is a one-time pad: use it twice and the secret leaks. This part is about the number that every signature needs and that must never be repeated.

Safety of the nonce shows that a repeated nonce lets anyone solve for the key. Deterministic nonces shows that the nonce can be derived from the key and the message, so that no random number is needed. Size and grinding shows that signing again until R is small saves a byte.

The order matters: slides 38 and 39 show the danger, slide 40 the cure, and slide 41 a small optimisation.""",
37: """The importance of randomness in signatures is that the nonce must be unpredictable and used only once. Its secrecy protects the private key.

The nonce is the one-time secret number k of a signature.

RFC 6979 derives the nonce from the key and the message by HMAC, so that no random number generator is needed at signing time.

Nonce reuse means that two signatures with one nonce reveal the private key.

Slide 38 computes the leak, slide 39 tells a real incident, and slide 40 shows the cure.""",
38: """Two different messages are signed with the same nonce k and the same key. Because both signatures share R, anyone can see that the nonce was reused. Two equations with two unknowns remain: subtracting one equation from the other and dividing gives the nonce, and from the nonce the private key falls out. The values are small toy numbers.

The third box signs the second message with a fresh nonce. Then R differs and nothing leaks. The table shows the observations: the same R in both signatures, the private key recovered, and the nonce recovered.

Slide 39 tells how this attack became possible in 2013. Example {EX} lets you change the nonce.""",
39: """On 11 August 2013 Bitcoin.org warned that the random number generator of Android was weak, and that wallets built on it could be robbed. A weak generator can repeat or leak a nonce, and a repeated nonce hands over the private key, as slide 38 computed.

Alex Klyubin of Google explained the flaw on 14 August, and Bitcoin Wallet and other wallets shipped updates. RFC 6979 derives the nonce from the key and the message, which is why Bitcoin Core no longer needs a good generator for it.

The Android robot, by Google Inc. and designed by Irina Blok, CC BY 3.0, stands in for the platform and does not show the incident. The Bitcoin.org alert is linked on the slide.""",
40: """The first box derives a nonce from the secret key and the hash of a message. The second box derives one for another message, and the third box repeats the first derivation and the signature itself.

The same key and message always give the same nonce, 0x1f8bce02bda8 at the start, and so the same signature. Another message gives another nonce, which starts with 0x80fb94370ee8.

Nothing random is drawn, so there is nothing to repeat by accident. Two different messages never share a nonce, so the attack of slide 38 has nothing to work on. The derivation uses HMAC, a keyed hash. Example {EX} lets you derive nonces for other messages.""",
41: """The first box signs 200 different messages with one key. The second box collects the length of every signature. The third box counts the lengths: about half of the signatures are 70 bytes long and about half are 71.

A 33-byte R, needed when its top bit is set, makes the signature one byte longer. It is the zero byte of slide 32. Bitcoin Core signs again until R is small, to save a byte.

One byte hardly matters for one signature, but it adds up over many. Compare slide 24, where a Schnorr signature always takes 64 bytes, so there is no length to optimise. Example {EX} lets you sign more messages.""",
42: """Segwit changed what is signed, as a cheque that also states the amount.

Cost of hashing: the old algorithm re-reads the transaction for every input. Commitment to amounts: new signatures cover the value being spent. Taproot signing: a taproot spend carries one 64-byte signature.

Slide 44 counts how much hashing the change saves, and slide 45 shows the amount inside the digest. Chapter 7, slide 39, showed the same fact from the side of the script: a changed amount makes a witness spend fail.""",
43: """Segregated witness's new signing algorithm, written in BIP143, hashes less and signs the spent amount.

BIP143 is the signature hash of segregated witness version 0.

O(n) hashing means that the bytes hashed grow in proportion to the number of inputs. The old algorithm grew with the square of that number.

A taproot signature is a BIP340 signature over the BIP341 message, and it is 64 bytes.

Slide 44 counts the bytes, and slide 45 shows the amount in the digest.""",
44: """The first box makes transactions with 1, 10, 100 and 1,000 inputs and one output. The second box counts the bytes that enter SHA-256 with the old algorithm and with BIP143. The third box divides the two counts.

The old method hashes the transaction again for each input, so its bytes grow with the square of the inputs. Doubling the inputs roughly quadruples the bytes hashed. BIP143 grows in a straight line. At 1,000 inputs the old method hashes 41,107,000 bytes and BIP143 only 254,130, which is 161.8 times less.

Remember the words quadratic and linear. This is the cost of hashing named on slide 42. Example {EX} lets you try other sizes.""",
45: """The first box makes one input and the script of a pay-to-key-hash coin, which stays the same: OP_DUP, OP_HASH160, a 20-byte hash, OP_EQUALVERIFY and OP_CHECKSIG. The second box defines a function that computes the BIP143 digest for a given amount. The third box computes it for 5,000 satoshis twice and for 5,001, and the legacy digest for comparison.

The BIP143 digest for 5,000 is 3d02f61132ca both times, and for 5,001 it is 89c355aa699d. The legacy digest, 0d29c866d5f0, has no amount in it, so a wallet could be told any value.

With the amount signed, a wallet can no longer be lied to about the value. Compare chapter 7, slide 39. Example {EX} lets you change the amount.""",
46: """Standards move on after print, like a map that needs a new edition. This part marks what in the book may have changed.

Standards status: proposals move from draft to deployed. Library support: Bitcoin Core and its library add features after print. History and dates: the patent, the first spend and the activation. The evidence trail: every claim is tied to a saved source or to a run.

When you read the book, treat a statement of status as a snapshot of its print date and check it against the sources listed on slide 50.""",
47: """Schnorr's patent was filed on 23 February 1990 and granted on 19 February 1991. The term is the longer of 17 years from the grant, which is 2008-02-19, and 20 years from the filing, which is 2010-02-23. So the term ended on 2010-02-23.

The third box counts the days from the genesis block, 3 January 2009, to the activation of taproot on 14 November 2021, which is 4,698 days. The patent ended in 2010, and taproot came eleven years later.

The code uses the date type of Python, which does the calendar arithmetic. Compare slide 22, which told the story of the patent. Example {EX} lets you change the dates.""",
48: """The chapter names thirteen BIPs, and their status was read from the saved BIP index. Deployed: 66, 143, 327, 340, 341 and 342. Drafts: 118, 361, 390 and 461. Complete: 54 and 373. Closed: 146.

A deployed proposal is in use on the network. A draft is still being worked on and may change. The counts were made from the saved index in deck 1.1.0 under Python 3.14.6.

A status can change after print, so check the index of the BIPs repository when you rely on it. Two examples from this chapter: BIP118 on slide 14 is a proposal, and BIP327 on slide 25 is deployed in the sense of this index.""",
49: """The five lines summarise the chapter, one line for each part, and each can be proved from its slides.

A signature is checked from message, public key and signature, scalars wrap at n, and the digest is what is signed. A SIGHASH flag chooses what is signed, and SINGLE with no matching output signs the number one. Schnorr turns a three-move proof into 64 bytes, keys add up safely only with MuSig2, and shares give thresholds. ECDSA has two forms of s and a nested byte layout, and a reused nonce leaks the key, which RFC 6979 prevents. Segwit hashes less and signs the amount, policy is stricter than consensus, and standards moved after print.

If a line feels unproven, the code slide of its part carries the receipt.""",
50: """Everything on this slide is free to read or watch, and every entry was opened on 2026-10-23 and is a live link in the file. The groups form a path. Read starts with the BIP340 specification, which has reference code and test vectors, the chapter's source on GitHub and the Bitcoin Wiki article on OP_CHECKSIG.

Standards and papers are the authoritative texts: BIP327 for MuSig2, RFC 6979 for the nonce, and Schnorr's paper of 1991. Watch has the MIT course Blockchain and Money, and the Optech workshop on Schnorr and taproot. Community has the Optech newsletters, the Delving Bitcoin forum, and the bitcoin-dev mailing list, where BIPs and soft forks are first proposed.

A good order is the workshop first, then BIP340 beside the chapter.""",
51: """These four statements are what you should be able to say after the chapter: what a verifier needs, what each SIGHASH flag commits to, how Schnorr, MuSig2 and ECDSA signatures work, and why the nonce matters and how policy differs from consensus.

Each is carried by a computation that ran on a slide of this deck, and slide 49 lists where. A statement you cannot yet say in your own words sends you back to that slide, and the questions on slide 3 are a good test.

The course page for chapter 8 has every word behind the slides, the stories with their sources and the question bank. Bring remaining questions to your instructor, and use the community links on slide 50.""",
})
