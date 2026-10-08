#!/usr/bin/env python3
"""Writes ch06-page/question_bank_v1_0_0.json, the question bank of SEN0401 chapter 6: at least one item for every concept of the
chapter, at least two for every concept with a worked example, one of those two an Apply item whose program prints the marked option.
The items are kept here as tuples (concept, level, question, options with the RIGHT one first, why, code or None); this script rotates
the right option to a position that cycles 0, 1, 2, 3 through the bank, so that each position carries a quarter of the items, and
writes the JSON the page reads. Follows chapter 5's sen0401_ch05_bank_gen_v1_0_0.py with one addition: the right option of an Apply
item is never typed - it is what the item's program printed when this script ran it under the course's CPython 3.14, so the bank
cannot carry an answer the interpreter did not give.
Every program uses the standard library only and no file access, because the page runs it in the reader's browser (Pyodide, an
older CPython), and the checker re-runs each one under every interpreter on this machine.
Run: python3 sen0401_ch06_bank_gen_v1_0_0.py        then: python3 question_bank_check_v1_2_0.py 06"""
__version__ = "1.0.0"
import json, os, re, subprocess, sys

PY = "/root/.local/bin/python3.14"
ALICE = ("01000000000101eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a0100000000ffffffff02204e0000000000002251203b41daba"
         "4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068f8240100000000001600147752c165ea7be772b2c0acb7f4d6047ae6f4768e0141cf5efe"
         "2d8ef13ed0af21d4f4cb82422d6252d70324f6f4576b727b7d918e521c00b51be739df2f899c49dc267c0ad280aca6dab0d2fa2b42a45182fc83e817130100000000")
TX = "tx = bytes.fromhex('%s')\n" % ALICE
I = []     # (concept, level, q, [right, wrong, wrong, wrong], why, code)


def q(concept, level, question, options, why):
    I.append((concept, level, question, options, why, None))


def a(concept, question, code, wrongs, why):
    """an Apply item: the right option is whatever the program prints, filled in when the bank is built"""
    I.append((concept, "Apply", question, [None] + list(wrongs), why, code))


# ============================== 1 WHAT A TRANSACTION IS ==============================
q("TransactionAnatomy", "Understand", "Why does the comparison with a land register fit Bitcoin better than the comparison with cash?",
  ["Bitcoins are not handed over; a record kept by every full node is updated to say who controls them", "Bitcoins are physical tokens like banknotes", "A land register is also kept on a blockchain", "Cash cannot be sent by email, but bitcoins can"],
  "Alice pays Bob by convincing full nodes to update their databases, exactly as a land register is updated.")
q("TransactionIdea", "Understand", "What are the three ideas a reader needs before the bytes of a transaction make sense?",
  ["The transaction as a request, the ownership record it changes, and the parts every transaction has", "The price, the exchange and the wallet", "The miner, the block and the difficulty", "The private key, the seed and the recovery code"],
  "A transaction is a request addressed to the record every full node keeps, built from a fixed set of parts.")
q("Transaction", "Understand", "Who is the audience of a transaction?",
  ["The full nodes, which check it and update their databases", "Bob, who receives it by email", "The miner who created the previous block", "The exchange where Alice bought her bitcoins"],
  "A transaction is the data Alice uses to convince full nodes; Bob learns of the payment from the shared record.")
a("Transaction", "How many bytes long is Alice's serialized transaction?", "print(len(bytes.fromhex('%s')))" % ALICE, ["388", "125", "569"],
  "The 388 hexadecimal characters the listing prints are 194 bytes.")
q("OwnershipRecord", "Understand", "What does the record of a full node hold for each entry?",
  ["A whole unspent output with its amount, its conditions and the height of its block", "A balance per person", "A list of addresses and their owners' names", "A copy of every wallet file"],
  "Bitcoin Core stores every UTXO with essential metadata; there are no names and no balances.")
a("OwnershipRecord", "A record maps 'Alice' to 100000. After the update that removes Alice and adds Bob with the same amount, what does the record hold?",
  "record = {'Alice': 100000}\nrecord.pop('Alice')\nrecord['Bob'] = 100000\nprint(record)", ["{'Alice': 100000, 'Bob': 100000}", "{'Alice': 0, 'Bob': 100000}", "{}"],
  "The spent entry is removed and the new one added, which is what a node does with outputs.")
q("TransactionParts", "Remember", "In what order are the top-level fields of an extended-format transaction serialized?",
  ["Version, marker, flag, inputs, outputs, witness structure, lock time", "Inputs, outputs, version, lock time, witness", "Lock time, version, inputs, outputs", "Version, inputs, witness, outputs, lock time"],
  "The marker and flag follow the version, the witness structure follows the outputs, and the lock time is last.")
a("TransactionParts", "How many top-level fields does an extended-format transaction have?",
  "print(len(['version', 'marker', 'flag', 'inputs', 'outputs', 'witness structure', 'lock time']))", ["5", "4", "8"],
  "Five fields plus the marker and the flag of the extended format.")
q("SerializationFormats", "Understand", "Why does it matter which bytes a transaction is serialized into?",
  ["Because the identifier is a hash of the bytes, so two serializations would give two identifiers", "Because the bytes are shown to users", "Because a longer serialization pays a lower fee", "Because the wallet stores transactions as text"],
  "Commitments are hashes over the serialization, so every node must agree on the exact bytes.")
q("SerializedTransaction", "Understand", "Why is Bitcoin Core's serialization format special?",
  ["It is the format used to make commitments to transactions and to relay them across the network", "It is the only format the law recognises", "It compresses transactions with a dictionary", "It is encrypted with the sender's key"],
  "Other programs may use another format as long as they transmit the same data, but commitments and relay use this one.")
a("SerializedTransaction", "The listing prints 388 hexadecimal characters. How many bytes is that?", "print(len('%s') // 2)" % ALICE, ["388", "776", "97"],
  "Two hexadecimal characters encode one byte.")
q("ExtendedFormat", "Remember", "What values must the marker and the flag have in the extended format today?",
  ["Marker 0x00 and flag 0x01", "Marker 0x01 and flag 0x00", "Both 0xff", "Both 0x00"],
  "The marker must be zero and the flag nonzero; in the current protocol the flag is always one.")
a("ExtendedFormat", "What are the fifth and sixth bytes of Alice's transaction, in hexadecimal?", TX + "print(tx[4:6].hex())", ["0100", "ffff", "0000"],
  "The marker 00 and the flag 01 follow the four version bytes.")
q("LegacyFormat", "Understand", "When must the legacy format still be used on the network?",
  ["For any transaction with an empty witness structure, which spends no witness programs", "Never; it was retired in 2017", "For every transaction above 1,000 bytes", "For coinbase transactions only"],
  "A transaction without witnesses must not carry the marker and flag.")
a("LegacyFormat", "How many bytes does Alice's transaction have in the legacy serialization, without marker, flag and witness?",
  TX + "legacy = tx[:4] + tx[6:-71] + tx[-4:]\nprint(len(legacy))", ["194", "122", "127"],
  "Two bytes of marker and flag and 67 bytes of witness structure are removed from 194.")
q("PsbtFormat", "Understand", "What is the PSBT format for?",
  ["Letting an untrusted program build a transaction template that trusted programs with the keys verify and complete", "Compressing transactions for the peer-to-peer network", "Storing transactions in the UTXO database", "Replacing the legacy format on the network"],
  "PSBT carries metadata a signer needs, which makes it less compact than the standard serialization.")
a("PsbtFormat", "What do the first four bytes of a PSBT, 70736274, spell?", "print(bytes.fromhex('70736274').decode())", ["bip1", "tx00", "sign"],
  "The magic bytes spell psbt, followed by a 0xff separator.")
q("ByteMap", "Understand", "What does a byte map show that a list of fields hides?",
  ["How unequal the fields are: scripts and signatures take most of the bytes", "The fee of the transaction", "The names of the sender and the recipient", "The block the transaction is in"],
  "Drawn to scale, the two output scripts and the witness item dominate the map.")
a("ByteMap", "At which byte offset does the witness structure of Alice's transaction begin, after a 42-byte inputs field and a 75-byte outputs field?",
  "print(4 + 1 + 1 + 42 + 75)", ["122", "190", "48"],
  "Version 4, marker 1, flag 1, inputs 42 and outputs 75 come first.")

# ============================== 2 VERSION, MARKER AND FLAG ==============================
q("VersionMarkerFlag", "Understand", "Why do six bytes deserve a branch of their own?",
  ["They decide which rules apply to everything that follows and which layout the bytes are in", "They carry the fee", "They identify the sender", "They are the only bytes a miner reads"],
  "The version gates BIP68 and BIP112; the marker and flag select the extended layout.")
q("VersionField", "Understand", "Why is a new constraint tied to a new version number rather than applied to every transaction?",
  ["So that presigned transactions of the old version stay valid", "Because old versions are deleted from the chain", "Because the version field is otherwise unused", "To make transactions larger"],
  "A rule that applied to existing versions could invalidate transactions that cannot be re-signed.")
q("VersionOne", "Remember", "How is the version 1 written in the first four bytes of a transaction?",
  ["01000000", "00000001", "0001", "ffffffff"],
  "The integer is little-endian: the least significant byte comes first.")
a("VersionOne", "What integer do the bytes 01000000 encode when read little-endian?", "print(int.from_bytes(bytes.fromhex('01000000'), 'little'))", ["16777216", "256", "0"],
  "Read least significant byte first, the bytes give 1.")
q("VersionTwo", "Understand", "What did BIP68 change for version 2 transactions?",
  ["A sequence below 2 to the 31 is read as a relative timelock", "The amount field became 16 bytes", "The lock time was removed", "Outputs may be negative"],
  "Version 1 transactions are unaffected; only version 2 and higher get the new reading of the sequence.")
a("VersionTwo", "A version 2 transaction has an input with sequence 30. What does the rule say?",
  "version, seq = 2, 30\nprint('relative timelock' if version >= 2 and seq < 2 ** 31 else 'no timelock')", ["no timelock", "final", "replaceable"],
  "Version 2 or higher and a sequence below 2 to the 31 means a relative timelock.")
q("VersionThree", "Understand", "What kind of change is the version 3 proposal?",
  ["A relay policy change, not a consensus change", "A hard fork", "A new serialization format", "A change to the subsidy"],
  "BIP431 restricts how a version 3 transaction is relayed; validity in a block is unchanged.")
a("VersionThree", "Bitcoin Core builds version 2 by default and treats up to version 3 as standard. What is the difference between the two numbers?",
  "current, max_standard = 2, 3\nprint(max_standard - current)", ["0", "2", "3"],
  "The transaction class names 2 as current, the policy header 3 as the highest standard version.")
q("PresignedTransaction", "Understand", "Why can a presigned transaction be lost for ever if a new rule applies to it?",
  ["The holder may no longer have the keys to sign a replacement", "Presigned transactions expire after a year", "The network deletes old signatures", "Full nodes refuse any transaction older than a block"],
  "Months or years later the private keys may be gone, so the invalidated transaction cannot be re-signed.")
a("PresignedTransaction", "A transaction was presigned as version 1 and a new rule applies from version 2. Is it still valid?",
  "presigned, rule_from = 1, 2\nprint('still valid' if presigned < rule_from else 'at risk')", ["at risk", "invalid", "replaced"],
  "The rule applies only to version 2 or higher, so the version 1 transaction is untouched.")
q("MarkerAndFlag", "Understand", "What do the two bytes after the version buy the format?",
  ["Backward compatibility: old parsers cannot misread the extended layout and new parsers recognise it", "A checksum of the transaction", "A record of the fee rate", "Room for a second version number"],
  "The zero marker is impossible as a legacy input count, so it is a safe signal.")
q("MarkerByte", "Understand", "Why is the marker a zero byte?",
  ["Because a legacy parser would read it as a count of zero inputs, which no transaction can have", "Because zero is the first version number", "Because zero bytes compress well", "Because the flag must be nonzero"],
  "The value is impossible under the old format, so the old format can never be confused with the new.")
a("MarkerByte", "Alice's transaction has 00 at byte 4 and 01 at byte 5. Which format is it in?",
  TX + "print('extended format' if tx[4] == 0 and tx[5] != 0 else 'legacy format')", ["legacy format", "PSBT", "unknown"],
  "A zero marker followed by a nonzero flag announces the extended format.")
q("FlagByte", "Understand", "Why does BIP144 give the flag a byte of its own instead of using a single zero marker?",
  ["A single zero byte would make an empty test transaction look like new serialized data, and the flag can be a bit vector for later data", "Because every field must be two bytes", "Because the flag holds the fee", "Because old nodes require it"],
  "BIP144 states both reasons in its rationale.")
a("FlagByte", "Read as a bit vector, which bits of the flag 0x01 are set?", "flag = 0x01\nprint([bit for bit in range(8) if flag >> bit & 1])", ["[1]", "[0, 1]", "[7]"],
  "Only bit 0 is set; the other seven are reserved.")

# ============================== 3 INPUTS ==============================
q("Inputs", "Understand", "Why are the inputs where a transaction connects to the past?",
  ["They point at outputs of earlier transactions, from which a node reads the amount and the conditions", "They contain the sender's balance", "They hold the block height", "They store the recipient's address"],
  "An input states no amount; everything is read from the output its outpoint names.")
q("InputList", "Understand", "Why does the inputs field begin with a count?",
  ["The inputs that follow have no terminator, so a parser must know how many to read", "To tell the miner the fee", "Because the count is hashed separately", "To limit a transaction to one input"],
  "The count is a compactSize integer; a parser reads it before anything else in the field.")
q("InputCount", "Remember", "What is the minimum number of inputs a transaction may have?",
  ["One", "Zero", "Two", "Any number, including none"],
  "Bitcoin Core refuses an empty input list with bad-txns-vin-empty.")
a("InputCount", "What is the input count stored at byte 6 of Alice's transaction?", TX + "print(tx[6])", ["2", "0", "131"],
  "After the version, the marker and the flag comes the count 1.")
q("CompactSize", "Understand", "How many bytes does a compactSize integer use for the value 253?",
  ["Three: the prefix 0xfd and two bytes", "One", "Two", "Nine"],
  "Values from 253 to 0xffff take the prefix 0xfd followed by a 16-bit number.")
a("CompactSize", "What is the compactSize encoding of 65536, in hexadecimal?",
  "n = 65536\nprint((b'\\xfe' + n.to_bytes(4, 'little')).hex())", ["fd000001", "ff0000010000000000", "010000"],
  "65536 is above 0xffff, so it takes the 0xfe prefix and four little-endian bytes.")
q("VarintVarieties", "Understand", "Which name is used for the variable-length integers of transaction serialization, and why the full name?",
  ["compactSize, because Bitcoin Core's VarInts and the header's Compact encoding are different things", "varint, because all three encodings are the same", "Compact, because it is the shortest", "VarInts, because the UTXO database uses it"],
  "Three encodings share a family resemblance; only compactSize is used in transactions.")
a("VarintVarieties", "Sort the three encodings' names: compactSize, VarInts, Compact.",
  "print(sorted({'compactSize': 'transactions', 'VarInts': 'UTXO database', 'Compact': 'nBits'}))", ["['compactSize', 'Compact', 'VarInts']", "['VarInts', 'Compact', 'compactSize']", "['Compact', 'compactSize', 'VarInts']"],
  "Capital letters sort before lower-case ones in Python's default order.")
q("OutpointField", "Understand", "What does an input say about the amount it spends?",
  ["Nothing directly: the amount is read from the output the outpoint names, and all of it is spent", "It states the amount in its last four bytes", "It states half the amount; the rest is fee", "It states the amount in the input script"],
  "A node obtains the amount, the conditions and the confirmation data from the previous output.")
q("Outpoint", "Remember", "How long is an outpoint, and what does it hold?",
  ["36 bytes: a 32-byte txid and a 4-byte output index", "32 bytes: a txid", "40 bytes: a txid and an 8-byte amount", "4 bytes: an index"],
  "Each input has exactly one outpoint pointing at one previous output.")
a("Outpoint", "What output index does Alice's outpoint carry?",
  TX + "outpoint = tx[7:43]\nprint(int.from_bytes(outpoint[32:], 'little'))", ["0", "2", "4294967295"],
  "The four bytes after the txid read as 1: the second output of the previous transaction.")
q("PreviousTxid", "Understand", "Why does changing one byte of a previous transaction break every outpoint that names it?",
  ["The txid is a hash of the bytes, so it changes completely", "Outpoints are stored by block height", "The index would no longer fit", "Outpoints expire when a transaction is edited"],
  "A digest changes unpredictably with any change to its input.")
a("PreviousTxid", "How many bytes is the identifier in an outpoint?",
  "prev = bytes.fromhex('eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a')\nprint(len(prev))", ["64", "20", "16"],
  "A double SHA-256 digest is 32 bytes; 64 hexadecimal characters display it.")
q("OutputIndex", "Understand", "Why does an outpoint need an index as well as a txid?",
  ["A transaction may have several outputs, and the index chooses one", "The index is the fee", "The index is the block height", "The txid alone is too short"],
  "Naming a transaction alone would be ambiguous and would let a spender claim all its outputs.")
a("OutputIndex", "What value do the index bytes 01000000 encode?", "print(int.from_bytes(bytes.fromhex('01000000'), 'little'))", ["16777216", "0", "100"],
  "Little-endian: the first byte is the least significant.")
q("DoubleSpendRule", "Understand", "What does the rule against double spending forbid?",
  ["Any output being spent more than once within a valid blockchain", "Spending an output before it has 100 confirmations", "Paying two recipients in one transaction", "Spending more than 21 million bitcoins"],
  "Alice cannot use the same previous output to pay both Bob and Carol.")
a("DoubleSpendRule", "A node has already seen outpoint '4ac54180:1' spent. A new transaction names it. What does the check say?",
  "spent = {'4ac54180:1'}\noutpoint = '4ac54180:1'\nprint('refused: already spent' if outpoint in spent else 'accepted')", ["accepted", "pending", "replaced"],
  "The outpoint is in the spent set, so the transaction is refused.")
q("ConflictingTransactions", "Understand", "When do two transactions conflict?",
  ["When they each try to spend the same previous output", "When they pay the same address", "When they are in the same block", "When they have the same fee"],
  "Only one of two conflicting transactions can be included in a valid blockchain.")
a("ConflictingTransactions", "Two input lists share the outpoint '4ac54180:1'. Do the transactions conflict?",
  "a = ['4ac54180:1']\nb = ['4ac54180:1', 'f4184fc5:0']\nprint('conflict' if set(a) & set(b) else 'compatible')", ["compatible", "duplicate", "invalid"],
  "A shared outpoint is exactly the definition of a conflict.")
q("UtxoDatabase", "Understand", "What does Bitcoin Core do to its UTXO database when a new block arrives?",
  ["Removes the outputs the block's transactions spend and adds the outputs they create", "Deletes everything and rebuilds from the genesis block", "Adds the block header only", "Stores the block's transactions as text"],
  "The database is a running set of unspent outputs with metadata such as the confirmation height.")
a("UtxoDatabase", "After Alice's transaction, how many entries remain of the two outputs of the previous transaction plus her two new outputs?",
  "utxo = {'4ac54180:0': 18210494, '4ac54180:1': 100000}\nutxo.pop('4ac54180:1')\nutxo['46620030:0'] = 20000\nutxo['46620030:1'] = 75000\nprint(len(utxo))", ["4", "2", "1"],
  "One entry is removed and two are added: three remain.")
q("ByteOrder", "Understand", "Why did bitcoin-cli reject the txid copied straight from Alice's outpoint?",
  ["The outpoint stores the digest in internal byte order and the command expects display order, the reverse", "The txid was too short", "The transaction had been pruned", "The command only accepts block hashes"],
  "Reversing the 32 bytes gave the identifier the node recognised.")
q("Digest", "Remember", "How long is the digest Bitcoin uses as a transaction identifier?",
  ["32 bytes", "20 bytes", "64 bytes", "16 bytes"],
  "Double SHA-256 gives 32 bytes whatever the input's length.")
a("Digest", "How many bytes does SHA-256 of SHA-256 of a short string give?",
  "import hashlib\nprint(len(hashlib.sha256(hashlib.sha256(b'a serialized transaction').digest()).digest()))", ["64", "20", "256"],
  "The output length of SHA-256 is fixed at 32 bytes.")
q("InternalByteOrder", "Understand", "Which data is in internal byte order?",
  ["Digests as they appear within transactions and blocks and as they are hashed", "Amounts and sequence numbers", "Addresses shown to users", "The hexadecimal an explorer prints"],
  "The authors also call it little-endian; only the 32-byte digests have the two spellings.")
a("InternalByteOrder", "Reverse the display-order identifier 4ac54180...33aeb into internal order. What are its first four hexadecimal characters?",
  "d = bytes.fromhex('4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb')\nprint(d[::-1].hex()[:4])", ["4ac5", "aeb3", "eb3e"],
  "The last byte eb becomes the first; the internal form begins eb3a.")
q("DisplayByteOrder", "Understand", "What is the practical lesson about byte order for developers?",
  ["Developers must remember to reverse the bytes of identifiers they show to users", "Users must type identifiers backwards", "Explorers use internal order", "Block hashes are not reversed"],
  "The sidebar calls the split an unintentional consequence of an early design decision.")
a("DisplayByteOrder", "Apply the fold-tac pipeline to eb3ae38f...c54a. What are the first eight characters of the result?",
  "internal = 'eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a'\npairs = [internal[i:i + 2] for i in range(0, 64, 2)]\nprint(''.join(reversed(pairs))[:8])", ["eb3ae38f", "a45c1408", "f83ea3be"],
  "Reversing the two-character pairs gives the display form 4ac54180....")
q("InputScriptField", "Understand", "Why is Alice's input script empty?",
  ["Her input spends a native segwit output, whose witness goes in the witness structure instead", "Her transaction has no signature", "The input script is never used any more", "Empty scripts pay no fee"],
  "The field is a remnant of the legacy format; segwit moved the witness out of it.")
q("InputScript", "Understand", "What does the 107-byte legacy input script of the example contain?",
  ["A push of a 72-byte signature and a push of a 33-byte public key", "Two signatures", "An address and an amount", "The previous transaction"],
  "0x48 pushes 72 bytes, then 0x21 pushes 33: one plus 72 plus one plus 33 is 107.")
a("InputScript", "The legacy input script begins with 0x48. How many bytes does that opcode push?", "print(0x48)", ["48", "107", "33"],
  "Opcodes 1 to 75 push that many following bytes; 0x48 is 72.")
q("LengthPrefix", "Understand", "Why can a parser not find the sequence field without the script length prefix?",
  ["An input script may contain any bytes and has no terminator, so only the prefix says where it ends", "The sequence is encrypted", "The prefix holds the sequence", "Scripts always end with 0xff"],
  "A wrong prefix shifts every later field.")
a("LengthPrefix", "What script length does the prefix byte 0x6b announce?", "print(0x6b)", ["6", "11", "171"],
  "0x6b is 107 in decimal.")

# ============================== 4 THE SEQUENCE FIELD ==============================
q("SequenceField", "Understand", "Which three meanings has the sequence field carried?",
  ["A transaction version counter for replacement, the BIP125 replaceability signal, and a BIP68 relative timelock", "A fee, a timestamp and a checksum", "An input index, an output index and a block height", "A public key, a signature and a hash"],
  "The same four bytes have been read three ways over time.")
q("SequenceReplacement", "Understand", "What was the original purpose of the sequence field?",
  ["To let later versions of a transaction replace earlier ones as candidates for confirmation", "To number the inputs", "To record the block height", "To signal a hard fork"],
  "The sequence number tracked the version of the transaction.")
q("SequenceNumber", "Remember", "What is the sequence value Bitcoin Core calls final?",
  ["0xffffffff", "0x00000000", "0xfffffffe", "0x80000000"],
  "The maximal value opts out of replacement, of the BIP125 signal and of any timelock.")
a("SequenceNumber", "What integer is the sequence ffffffff?", "print(int.from_bytes(bytes.fromhex('ffffffff'), 'little'))", ["2147483648", "65535", "4294967296"],
  "Four bytes of 0xff are 2 to the 32 minus 1.")
q("SetupTransaction", "Understand", "Why must the refund be signed before the setup transaction is broadcast?",
  ["Otherwise one party could lock the other's money by refusing to cooperate", "Because the refund has a higher sequence", "Because miners require it", "Because the setup is a coinbase"],
  "The refund is what makes depositing into a two-signature output safe.")
a("SetupTransaction", "Alice and Bob each deposit 50,000 satoshis. What does the multisignature output hold?",
  "deposits = {'Alice': 50000, 'Bob': 50000}\nprint(sum(deposits.values()))", ["50000", "150000", "0"],
  "The setup output holds both deposits together.")
q("PaymentChannel", "Understand", "Why does a payment channel move value many times with one confirmed transaction?",
  ["Every version is a valid signed transaction, but only the final one is broadcast", "Because miners mine every version", "Because the setup is repeated each round", "Because the refund is broadcast first"],
  "The chain records the setup and the settlement whatever the number of rounds.")
a("PaymentChannel", "After the refund, two rounds and the final version, how many versions of the spend exist?",
  "versions = [0, 1, 2, 0xffffffff]\nprint(len(versions))", ["3", "2", "5"],
  "The refund, one version per round and the final version.")
q("ReplacementAttack", "Understand", "Why was the original replacement scheme disabled?",
  ["Unlimited free replacements let an attacker burden every relaying node for almost nothing", "Miners refused to run it", "It required a hard fork", "It was replaced by PSBT"],
  "Each replacement consumed the bandwidth of all relaying nodes at no cost to the attacker.")
a("ReplacementAttack", "1,000 replacements a minute of 200 bytes each reach 50,000 nodes. How many gigabytes a minute is that?",
  "print(50000 * 1000 * 200 // 10 ** 9)", ["20", "1", "100"],
  "Ten gigabytes a minute across the network for about 200 kilobytes of the attacker's own bandwidth.")
q("ReplaceByFee", "Understand", "What compromise let replacement return to Bitcoin Core?",
  ["Replacement became opt-in, signalled through the sequence field", "Replacement was limited to coinbase transactions", "Only miners may replace", "Replacement requires a hard fork"],
  "Users who objected could ignore unconfirmed transactions that carried the signal.")
q("OptInRbf", "Understand", "What must a replacement pay under replace-by-fee?",
  ["More total fee than the original and enough extra to pay for its own relay", "The same fee as the original", "Nothing, if it has a higher sequence", "A fee to the original sender"],
  "A higher fee rate alone is not enough; the replacement must also pay for its bandwidth.")
a("OptInRbf", "An original pays 5,000 satoshis and a replacement 8,000, both 143 vbytes. Does the replacement qualify?",
  "old_fee, new_fee, size = 5000, 8000, 143\nprint(new_fee > old_fee and new_fee / size > old_fee / size)", ["False", "None", "5000"],
  "It pays more in total and has the higher rate.")
q("Bip125Signal", "Remember", "Which sequence values signal replaceability under BIP125?",
  ["Any value below 0xfffffffe", "Only 0x00000000", "Only 0xffffffff", "Any value above 2 to the 31"],
  "At least two below the maximum: 0xfffffffd and lower.")
a("Bip125Signal", "Does a sequence of 0xfffffffe signal replaceability?", "print(0xfffffffe <= 0xfffffffd)", ["True", "0xfffffffe", "None"],
  "0xfffffffe is only one below the maximum, so it does not signal.")
q("RelativeTimelock", "Understand", "What is a relative timelock relative to?",
  ["The confirmation of the output being spent", "The genesis block", "The current date", "The transaction's own confirmation"],
  "The spent output must have aged by the lock before the spend can be confirmed.")
q("Bip68Timelock", "Understand", "An input has a relative timelock of 30 blocks. How many blocks must lie strictly between the output's block and the confirming block?",
  ["29", "30", "31", "0"],
  "The authors' example: a lock of 30 allows confirmation with at least 29 blocks between.")
a("Bip68Timelock", "The output was confirmed at 774,958 and the lock is 30 blocks. What is the earliest confirming height?",
  "print(774958 + 30)", ["774959", "774987", "775072"],
  "774,988 leaves 29 blocks strictly between.")
q("TypeFlag", "Remember", "What does a set type flag mean?",
  ["The lock counts units of 512 seconds", "The lock counts blocks", "The timelock is disabled", "The transaction is replaceable"],
  "Bit 22 chooses time; clear, the value counts blocks.")
a("TypeFlag", "What is the value of the type flag, 1 shifted left 22, in hexadecimal?", "print(hex(1 << 22))", ["0x800000", "0x200000", "0x80000000"],
  "1 shifted left 22 is 0x400000.")
q("DisableFlag", "Understand", "What does the disable flag let a transaction do?",
  ["Mix inputs with a relative timelock and inputs without one", "Skip the signature check", "Spend a coinbase early", "Use version 1 rules"],
  "An input with bit 31 set has no relative timelock even in a version 2 transaction.")
a("DisableFlag", "Is the disable flag set in the sequence 0x7fffffff?", "print(bool(0x7fffffff & (1 << 31)))", ["True", "0x7fffffff", "1"],
  "0x7fffffff has bit 31 clear, so it is read as a lock.")
q("TimelockMask", "Understand", "How many bits of the sequence carry the relative timelock value?",
  ["16", "32", "22", "8"],
  "The value is masked with 0x0000ffff, so the maximum is 65,535.")
a("TimelockMask", "What is the largest relative timelock value, 0xffff, in decimal?", "print(0xffff)", ["65536", "4096", "32767"],
  "Sixteen bits give at most 65,535.")

# ============================== 5 OUTPUTS ==============================
q("Outputs", "Understand", "What two things does every output state?",
  ["An amount of satoshis and the script giving the conditions for spending it", "A sender and a recipient", "A fee and a timestamp", "A txid and an index"],
  "Outputs are where value and conditions are written down.")
q("OutputList", "Understand", "How is the fee of a transaction determined?",
  ["It is the difference between the inputs' previous amounts and the sum of the outputs", "It is stored in a fee field", "It is the first output", "It is the lock time"],
  "No field holds the fee; the miner may claim whatever the inputs are worth beyond the outputs.")
q("OutputCount", "Remember", "What is the minimum output count?",
  ["One", "Zero", "Two", "Three"],
  "Bitcoin Core refuses an empty output list with bad-txns-vout-empty.")
a("OutputCount", "What is the output count byte at offset 48 of Alice's transaction?", TX + "print(tx[48])", ["1", "0", "3"],
  "Alice's transaction has two outputs: the payment and the change.")
q("AmountField", "Remember", "How is an output's amount encoded?",
  ["An 8-byte signed little-endian integer of satoshis", "A 4-byte unsigned integer of bitcoins", "A decimal string", "A compactSize integer"],
  "Bitcoin Core calls the field value and types it as a 64-bit signed integer.")
a("AmountField", "What amount do the bytes 204e000000000000 encode?", "print(int.from_bytes(bytes.fromhex('204e000000000000'), 'little'))", ["2000", "75000", "8270"],
  "The payment to Bob is 20,000 satoshis.")
q("Satoshi", "Remember", "How many satoshis are in one bitcoin?",
  ["100,000,000", "1,000,000", "100,000", "21,000,000"],
  "The ratio is Bitcoin Core's constant COIN.")
a("Satoshi", "Express 75,000 satoshis in bitcoin.", "print(75000 / 100_000_000)", ["0.0075", "7.5e-05", "0.075"],
  "Divide by one hundred million.")
q("AmountRange", "Understand", "Why does the amount need a range check if it is a 64-bit integer?",
  ["The integer can hold negative values and sums that wrap around, which the 2010 overflow exploited", "Because amounts are floating point", "Because fees must be positive", "Because 64 bits are too few for 21 million bitcoins"],
  "Bitcoin Core refuses negative, oversized and overflowing totals and cites CVE-2010-5139.")
a("AmountRange", "How many satoshis is the consensus maximum of 21 million bitcoins?", "print(21_000_000 * 100_000_000)", ["21000000000000", "2100000000000", "210000000000000000"],
  "2.1 quadrillion satoshis, Bitcoin Core's MAX_MONEY.")
q("DustPolicy", "Understand", "Why is an uneconomical output a cost to everyone?",
  ["Its owner has no reason to spend it, so every full node keeps it in the UTXO set for ever", "It makes blocks larger", "It raises the fee of every other transaction", "It must be mined twice"],
  "Every UTXO makes it slightly harder to run a full node.")
q("UneconomicalOutput", "Understand", "When is an output uneconomical?",
  ["When its value is less than the extra fee that spending it adds", "When it is below one bitcoin", "When it pays a public key", "When it has no script"],
  "A zero-value output is always uneconomical; others become so when fee rates rise.")
a("UneconomicalOutput", "Spending a 68-vbyte input at 10 satoshis per vbyte costs how much, and is a 500-satoshi output worth spending?",
  "cost = 68 * 10\nprint((cost, 500 < cost))", ["(680, False)", "(68, True)", "(500, True)"],
  "680 satoshis of fee exceed the output's 500, so it is uneconomical at that rate.")
q("DustLimit", "Remember", "What dust limit do many programs simply assume?",
  ["546 satoshis", "1,000 satoshis", "294 satoshis", "1 satoshi"],
  "Bitcoin Core's own policy is more complicated; 546 is the legacy P2PKH figure.")
a("DustLimit", "Compute Bitcoin Core's dust threshold for a legacy output: 34 plus 148 bytes at 3,000 satoshis per kilobyte.", "print((34 + 148) * 3000 // 1000)", ["294", "182", "330"],
  "182 bytes at 3 satoshis a byte is 546.")
q("DataCarrierOutput", "Understand", "Why may an OP_RETURN output have a value of zero?",
  ["It can never be spent, so nodes need not keep it and no satoshis are stranded", "It is spent by the miner", "It is a coinbase output", "Its value is paid as fee"],
  "OP_RETURN makes the script fail at once, so the output never enters the UTXO set.")
a("DataCarrierOutput", "What is the opcode byte 0x6a in decimal?", "print(0x6a)", ["81", "96", "16"],
  "0x6a, 106, is OP_RETURN.")
q("OutputScriptField", "Understand", "What does the output script contain?",
  ["The conditions that will need to be fulfilled in order to spend the bitcoins", "The sender's signature", "The transaction's fee", "The block height"],
  "Parsing and using scripts is the subject of the following chapter.")
q("OutputScript", "Understand", "What do the bytes 5120 at the start of Alice's first output script mean?",
  ["The number 1 followed by a 32-byte push: a segwit version 1 (taproot) program", "A 51-byte script", "OP_RETURN with data", "A legacy pay-to-public-key-hash script"],
  "0x51 is the number 1 and 0x20 pushes 32 bytes.")
a("OutputScript", "How long is Alice's second output script, whose length byte follows the second amount?",
  TX + "len0 = tx[57]\nprint(tx[58 + len0 + 8])", ["34", "20", "25"],
  "The change output pays a 22-byte version 0 script: 0014 and twenty bytes.")
q("ScriptSizeLimit", "Remember", "How large may an output script be for a later transaction to spend it?",
  ["10,000 bytes or smaller", "520 bytes", "Any size", "100 bytes"],
  "There is no explicit limit at creation, but a spend is refused above 10,000 bytes.")
a("ScriptSizeLimit", "Would a 10,000-byte script fit a block by weight, at four weight units a byte?", "print(10000 * 4 <= 4000000)", ["False", "40000", "4000000"],
  "40,000 weight is far below the 4,000,000 limit.")
q("AnyoneCanSpend", "Understand", "Why are anyone-can-spend scripts useful to protocol developers?",
  ["Upgrades take such a script and add constraints, which old nodes accept because they would have accepted any spend", "They pay the highest fees", "They cannot be mined", "They are the standard templates"],
  "Segwit outputs are anyone-can-spend to old nodes; new nodes require a witness.")
a("AnyoneCanSpend", "What is the length of the empty output script, and is 0x51 the opcode OP_TRUE?", "print((len(b''), 0x51 == 81))", ["(1, True)", "(0, False)", "(81, True)"],
  "The empty script has length zero; OP_TRUE is 0x51, which is 81.")
q("StandardOutput", "Understand", "What are standard transaction outputs?",
  ["The few output script templates Bitcoin Core's relay policy allows", "The outputs of a coinbase", "Outputs above the dust limit", "Outputs paying exactly one bitcoin"],
  "A non-standard output is valid under consensus but is not relayed by default nodes.")
a("StandardOutput", "Sort the template names P2PKH, P2SH, P2WPKH, P2WSH, P2TR. Which comes first?", "print(sorted(['P2PKH', 'P2SH', 'P2WPKH', 'P2WSH', 'P2TR'])[0])", ["P2SH", "P2TR", "P2WPKH"],
  "In the default string order P2PKH sorts before the others.")

# ============================== 6 WITNESSES ==============================
q("Witnesses", "Understand", "Why did where a witness is stored turn out to matter?",
  ["Witnesses in the input script were hashed into the txid, which made identifiers malleable", "Witnesses are shown to users", "Witnesses change the fee", "Witnesses are stored in the block header"],
  "Segregated witness leaves the witness out of the identifier to remove the problems.")
q("WitnessIdea", "Understand", "What is the common role of a signature in an input script and a value solving a toy script?",
  ["Both are data that let a node verify an authorisation without trusting anyone", "Both are public keys", "Both are fees", "Both are hashes"],
  "The role is named witness so that the question of where it goes can be asked.")
q("Witness", "Understand", "What is the witness for the script 2 OP_ADD 4 OP_EQUAL?",
  ["The value 2", "The value 4", "The value 6", "A signature"],
  "Adding 2 to the witness must give 4.")
a("Witness", "Does the witness 2 solve the script 2 OP_ADD 4 OP_EQUAL?", "witness = 2\nprint(witness + 2 == 4)", ["False", "4", "2"],
  "Two plus two equals four.")
q("SignatureWitness", "Understand", "In a signature scheme, what is the public key?",
  ["A public identifier of secret data that only its holder can use to solve the equation", "The solution to the equation", "The secret itself", "A hash of the transaction"],
  "The solution is the signature; it is the witness in a script with OP_CHECKSIG.")
a("SignatureWitness", "Which role is the witness in the triple identifier, solver, witness?",
  "problem = {'identifier': 'public key', 'solver': 'the holder of the private key', 'witness': 'signature'}\nprint(problem['witness'])", ["public key", "the holder of the private key", "OP_CHECKSIG"],
  "The signature is the datum the spender supplies.")
q("ContractProtocol", "Understand", "Why do contract protocols sign transactions out of order?",
  ["So that each party is protected by a refund before committing funds", "Because miners require it", "Because signatures expire", "To reduce the fee"],
  "The payment channel and the two-party deposit are the examples.")
a("ContractProtocol", "How many stages does the card game have: setup, refund, rounds, final?",
  "print(len(['setup transaction', 'refund transaction', 'rounds of the game', 'final transaction']))", ["3", "2", "5"],
  "Four stages, each a transaction that is signed and held.")
q("MalleabilityProblems", "Understand", "How do all three malleability problems end for the party that presigned?",
  ["A presigned transaction becomes invalid because the identifier it spends has changed", "The fee is lost", "The block is rejected", "The private key leaks"],
  "Bob loses his payment to Carol; Alice loses her refund.")
q("CircularDependency", "Understand", "Why could Alice and Bob not build the refund before signing the deposit, in the legacy format?",
  ["The refund needs the deposit's txid, which depends on the deposit's signatures", "The refund needs a higher fee", "Refunds are not allowed before confirmation", "The deposit has no outputs until mined"],
  "If they know the signatures, one of them can broadcast the deposit first.")
a("CircularDependency", "Does the chain of needs refund -> deposit txid -> deposit signatures close a circle?",
  "needs = {'refund': 'txid of the deposit', 'txid of the deposit': 'signatures of the deposit'}\nprint(needs[needs['refund']] == 'signatures of the deposit')", ["False", "txid of the deposit", "None"],
  "The refund depends on signatures that should come last.")
q("ThirdPartyMalleability", "Understand", "What can a third party change about Alice's legacy transaction without invalidating it?",
  ["The encoding of a push in the input script, which changes the txid", "The amount of an output", "The recipient", "The lock time"],
  "The signature cannot cover the input script that contains it.")
a("ThirdPartyMalleability", "Three encodings of a push give three legacy bodies. How many distinct identifiers result?",
  "import hashlib\nh256 = lambda b: hashlib.sha256(hashlib.sha256(b).digest()).digest()\nbody = bytes.fromhex('01000000') + bytes(36)\nids = {h256(body + bytes([len(v) // 2]) + bytes.fromhex(v) + bytes.fromhex('ffffffff')).hex() for v in ('52', '0102', '4c0102')}\nprint(len(ids))", ["1", "2", "0"],
  "Different bytes hash to different digests.")
q("PushEncoding", "Understand", "Why does OP_2 and OP_PUSH1 0x02 give the same script result but a different txid?",
  ["The interpreter treats them alike while the hash function hashes different bytes", "The interpreter rejects OP_2", "The txid is computed over the outputs only", "Push opcodes are not hashed"],
  "Any of the forms changes the legacy serialization.")
a("PushEncoding", "What are the bytes of OP_PUSHDATA1 pushing the single byte 0x02, in hexadecimal?", "print(bytes([0x4c, 0x01, 0x02]).hex())", ["0102", "52", "020200"],
  "OP_PUSHDATA1 is 0x4c, then a one-byte length, then the data.")
q("SecondPartyMalleability", "Understand", "Why can a counterparty change the txid even with canonical encodings?",
  ["A signer chooses a random number, and a different number gives a different valid signature", "The counterparty can change the amount", "Signatures are not checked", "The txid ignores the outputs"],
  "Like a handwritten signature, each signing looks slightly different.")
a("SecondPartyMalleability", "Two signatures of the same data with different random numbers. Are they different?",
  "nonce_a, nonce_b = 1234, 5678\nprint(nonce_a != nonce_b)", ["False", "1234", "None"],
  "A different random number yields a different signature and, in the legacy format, a different txid.")
q("WantedMalleability", "Understand", "What is an example of wanted malleability?",
  ["Alice using a signature hash to let Bob add an input and help pay the fee", "A stranger re-encoding a push", "Bob re-signing the deposit", "A miner changing the lock time"],
  "The sender permits the change; that is why the authors say unwanted for the other kind.")
a("WantedMalleability", "Which of the three kinds is permitted: unwanted third-party, unwanted second-party, sender-permitted (sighash)?",
  "kinds = {'unwanted third-party': False, 'unwanted second-party': False, 'sender-permitted (sighash)': True}\nprint([k for k in kinds if kinds[k]][0])", ["unwanted third-party", "unwanted second-party", "none"],
  "Only the sighash-based mutation is wanted.")
q("SegregatedWitness", "Understand", "What did segwit change besides where the witness is stored?",
  ["The measure of transaction size, from bytes to weight", "The number of outputs allowed", "The subsidy", "The hash function"],
  "The weight unit discounts witness bytes.")
q("Segwit", "Understand", "What does an empty input script achieve under segwit?",
  ["It keeps witnesses from affecting the txid, removing circular dependencies and both malleabilities", "It makes the transaction smaller", "It hides the sender", "It removes the need for signatures"],
  "The identifier covers the legacy serialization only.")
a("Segwit", "Hashing the legacy serialization of Alice's transaction twice gives her txid. What are its first eight characters?",
  "import hashlib\n" + TX + "legacy = tx[:4] + tx[6:-71] + tx[-4:]\nd = hashlib.sha256(hashlib.sha256(legacy).digest()).digest()\nprint(d[::-1].hex()[:8])", ["f7cdbc7c", "eb3ae38f", "4ac54180"],
  "The identifier 46620030... is the double SHA-256 of the 125 legacy bytes, reversed.")
q("HardFork", "Understand", "What makes a change a hard fork?",
  ["Older full nodes would reject blocks that newer nodes accept", "It adds a new opcode", "It changes the subsidy", "It is proposed in a BIP"],
  "A hard fork requires every node to upgrade or be left on another chain.")
a("HardFork", "Old rules accept the set A, new rules accept A plus blocks old nodes reject. Hard or soft?",
  "old = {'legacy blocks'}\nnew = {'legacy blocks', 'blocks old nodes reject'}\nprint('hard fork' if new - old else 'soft fork')", ["soft fork", "no fork", "both"],
  "New rules accept something old rules reject: a hard fork.")
q("SoftFork", "Understand", "What must a soft fork never do?",
  ["Accept a block that nodes without the change would consider invalid", "Reject a block old nodes accept", "Change relay policy", "Use a new version number"],
  "Newer nodes may reject more but accept no more.")
a("SoftFork", "New rules accept a subset of what old rules accept. Hard or soft?",
  "old = {'any spend of a segwit output', 'other blocks'}\nnew = {'other blocks'}\nprint('soft fork' if new <= old else 'hard fork')", ["hard fork", "no fork", "both"],
  "A subset of the old acceptances is a soft fork.")
q("WitnessProgram", "Understand", "What is the segwit output script template?",
  ["A number 0 to 16 followed by 2 to 40 bytes of data", "OP_RETURN followed by data", "A public key and OP_CHECKSIG", "Any script longer than 40 bytes"],
  "The number is the version and the data the witness program.")
a("WitnessProgram", "Alice's first output script begins 51 20. What witness version and program length does it declare?",
  "s = bytes.fromhex('51203b41daba4c9ace578369740f15e5ec880c28279ee7f51b07dca69c7061e07068')\nprint((s[0] - 0x50, s[1]))", ["(0, 20)", "(81, 32)", "(1, 34)"],
  "0x51 is the number 1 and 0x20 is a push of 32 bytes.")
q("WitnessStructure", "Understand", "Where is the witness structure serialized?",
  ["After the outputs and before the lock time", "Before the version", "Inside each input", "In the block header"],
  "It holds one stack per input and is excluded from the txid.")
a("WitnessStructure", "In the table of terms, what pair does segwit use for authorization and authentication?",
  "rows = [('whitepaper', 'public key', 'signature'), ('legacy', 'output script', 'input script'), ('segwit', 'witness program', 'witness structure')]\nprint(rows[2][1:])", ["('output script', 'input script')", "('public key', 'signature')", "('witness structure', 'witness program')"],
  "Witness program for authorization, witness structure for authentication.")
q("WitnessSerialization", "Understand", "Why has the witness structure no count of its own?",
  ["There is one witness stack for every input, so the input count implies it", "Witnesses are never counted", "The count is in the flag", "The lock time holds the count"],
  "A parser reuses the input count when it reaches the witness.")
q("WitnessStack", "Understand", "What does a witness stack begin with?",
  ["A count of its items", "A signature", "The input's outpoint", "A version byte"],
  "Each item is then prefixed by its own compactSize length.")
a("WitnessStack", "What are the input count (byte 6) and the item count of the first witness stack (byte 123) of Alice's transaction?",
  TX + "print((tx[6], tx[123]))", ["(1, 65)", "(2, 1)", "(1, 0)"],
  "One input, one witness item.")
q("WitnessItem", "Understand", "How is a witness item delimited?",
  ["By a compactSize length prefix", "By a terminating zero byte", "By a fixed size of 65 bytes", "By the lock time"],
  "Items of any size are possible, each with its own prefix.")
a("WitnessItem", "How long is Alice's single witness item, whose length byte is at offset 124?", TX + "print(tx[124])", ["64", "72", "33"],
  "A 64-byte Schnorr signature plus a one-byte sighash flag.")
q("LegacyInputWitness", "Remember", "What is the witness stack of a legacy input in a segwit transaction?",
  ["A single count byte of zero", "Absent entirely", "The input script copied", "A count of one and an empty item"],
  "Legacy inputs have no witness items, so their stack is 0x00.")
a("LegacyInputWitness", "Two stacks: one empty and one with a signature and a public key. What are their item counts?",
  "stacks = [[], ['signature', 'public key']]\nprint([len(s) for s in stacks])", ["[1, 2]", "[0, 1]", "[2, 0]"],
  "The legacy input's stack has zero items; the other has two.")

# ============================== 7 LOCK TIME AND THE COINBASE ==============================
q("LockTimeAndCoinbase", "Understand", "What theme do the lock time and the coinbase share?",
  ["Time and height as conditions on validity", "Both carry the fee", "Both are optional", "Both are signed by the miner"],
  "A lock time says the earliest block; the maturity rule says how long coinbase outputs must wait.")
q("LockTime", "Understand", "Since when has the lock time been a consensus rule rather than a mining policy?",
  ["Since block 31,000, Bitcoin's earliest known soft fork", "Since segwit in 2017", "Since BIP68", "Since the genesis block"],
  "Before that height it was only enforced by the policy for choosing transactions to mine.")
q("LockTimeField", "Remember", "What does a lock time of zero mean?",
  ["The transaction is eligible for inclusion in any block", "The transaction is invalid", "The transaction must wait one block", "The transaction is a coinbase"],
  "Alice's transaction ends with four zero bytes.")
a("LockTimeField", "What integer do the last four bytes 00000000 encode?", "print(int.from_bytes(bytes.fromhex('00000000'), 'little'))", ["1", "4", "255"],
  "Zero: any block.")
q("HeightLock", "Understand", "A lock time of 123,456 allows inclusion from which block?",
  ["Block 123,456 or any later block", "Block 123,457 only", "Any block before 123,456", "Block 500,000,000"],
  "A value below 500,000,000 is a height, and the block's height must equal it or be higher.")
a("HeightLock", "Is a lock time of 123,456 satisfied by block 123,456?", "lt, h = 123456, 123456\nprint(lt < 500_000_000 and h >= lt)", ["False", "123456", "None"],
  "The height equals the lock time, which is allowed.")
q("TimeLock", "Understand", "How is a lock time of 500,000,000 or more read?",
  ["As an epoch time, compared with the block's median time past", "As a block height", "As a number of satoshis", "As a sequence value"],
  "Epoch time counts seconds since 1970-01-01 UTC.")
a("TimeLock", "Is the lock time 1675559245 a height or a time?", "lt = 1675559245\nprint('epoch time' if lt >= 500_000_000 else 'block height')", ["block height", "invalid", "any block"],
  "It is above the 500,000,000 threshold.")
q("MedianTimePast", "Understand", "Why are time locks compared with the median time past rather than a block's own timestamp?",
  ["A single timestamp is chosen by one miner; the median of eleven is much harder to move", "The median is always earlier", "Block timestamps are not stored", "The median is the current time"],
  "BIP113 made the median the endpoint of lock-time calculations.")
a("MedianTimePast", "What is the median of the eleven times 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11?", "print(sorted([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])[5])", ["5", "7", "5.5"],
  "The sixth of eleven sorted values is the median.")
q("CoinbaseTransaction", "Understand", "Why are all the rules that limit creation of bitcoins rules about the coinbase?",
  ["The coinbase is the only transaction that creates bitcoins", "The coinbase pays the fees", "The coinbase has no outputs", "The coinbase is signed by every node"],
  "The subsidy schedule, the output sum and the maturity are all enforced on it.")
q("Coinbase", "Remember", "What did older documentation call the coinbase transaction?",
  ["A generation transaction", "A setup transaction", "A refund transaction", "A witness transaction"],
  "Not to be confused with the company of the same name.")
a("Coinbase", "How many defining properties are listed: first in the block, created by the miner, claims fees and subsidy?",
  "print(len(['the first transaction in the block', 'created by the miner', 'claims the fees and the subsidy']))", ["2", "4", "1"],
  "Three properties define the coinbase's role.")
q("NullOutpoint", "Remember", "What outpoint must a coinbase input carry?",
  ["A txid of all zeros and the output index 0xffffffff", "The previous block's hash and index 0", "Any unspent output", "Its own txid"],
  "The null outpoint prevents the coinbase from referencing a previous output.")
a("NullOutpoint", "What is the maximal output index 0xffffffff in decimal?", "print(0xffffffff)", ["2147483647", "65535", "4294967296"],
  "Four bytes of 0xff.")
q("CoinbaseField", "Remember", "How long may the coinbase field be?",
  ["At least 2 and at most 100 bytes", "Exactly 4 bytes", "Up to 10,000 bytes", "Any length"],
  "Bitcoin Core refuses other lengths with bad-cb-length.")
a("CoinbaseField", "A coinbase field begins 03 e0 e6 0b. What block height does the three-byte push encode?",
  "field = bytes.fromhex('03e0e60b')\nprint(int.from_bytes(field[1:4], 'little'))", ["781008", "3", "224"],
  "BIP34 puts the height first; e0e60b little-endian is 780,000.")
q("BlockSubsidy", "Understand", "How does the subsidy change over time?",
  ["It starts at 50 BTC and halves every 210,000 blocks, rounded down to the satoshi", "It grows with the fee rate", "It is fixed at 6.25 BTC", "It halves every block"],
  "Bitcoin Core shifts 50 times COIN right once per halving.")
a("BlockSubsidy", "What is the subsidy at block 840,000, in bitcoins?", "print(((50 * 100_000_000) >> (840_000 // 210_000)) / 100_000_000)", ["6.25", "1.5625", "12.5"],
  "The fourth halving leaves 3.125 bitcoins.")
q("BlockReward", "Understand", "What is the block reward?",
  ["The fees of the block's transactions plus the subsidy, as a ceiling on the coinbase's outputs", "The subsidy alone", "The largest fee in the block", "The sum of all outputs in the block"],
  "A miner may claim less, never more.")
a("BlockReward", "Fees of 5,000, 12,000 and 3,000 satoshis plus a subsidy of 312,500,000. What is the reward?", "print(5000 + 12000 + 3000 + 312_500_000)", ["312500000", "20000", "312520000000"],
  "The sum is 312,520,000 satoshis.")
q("MaturityRule", "Remember", "How many confirmations must a coinbase have before its outputs can be spent?",
  ["100", "6", "1", "210,000"],
  "Bitcoin Core's COINBASE_MATURITY is 100; younger outputs are immature.")
a("MaturityRule", "A coinbase in block 9 is spent in block 170. How many blocks later, and is that mature?",
  "print((170 - 9, 170 - 9 >= 100))", ["(161, False)", "(100, True)", "(179, True)"],
  "161 blocks is more than the 100 required.")

# ============================== 8 WEIGHT AND FOUNDATIONS ==============================
q("WeightAndFoundations", "Understand", "Why does weight rather than byte size decide what a transaction pays?",
  ["Blocks are filled by weight, and witness bytes weigh a quarter of other bytes", "Bytes are no longer counted", "Weight equals the fee", "Miners ignore size"],
  "The factors make spending a UTXO cheaper and creating one relatively dearer.")
q("WeightUnits", "Understand", "Why is the weighting uneven on purpose?",
  ["To reduce the weight used when spending a UTXO and so discourage uneconomical outputs", "To make old transactions invalid", "To favour large blocks", "To simplify parsing"],
  "A signature that spends is witness data at a factor of 1.")
q("Weight", "Remember", "How is a transaction's weight defined?",
  ["Legacy serialization size times three plus full serialization size", "Size in bytes times four", "Size in bytes plus the witness", "Number of inputs times 100"],
  "For Alice's transaction, 125 times 3 plus 194 is 569.")
a("Weight", "Compute the weight of a transaction whose legacy size is 125 bytes and full size 194 bytes.", "print(125 * 3 + 194)", ["776", "319", "500"],
  "569, the figure the book obtained from Bitcoin Core.")
q("Vbyte", "Understand", "How are vbytes computed from weight?",
  ["Weight divided by four, rounded up", "Weight times four", "Weight minus the witness", "Weight divided by three"],
  "569 weight is 143 vbytes.")
a("Vbyte", "How many vbytes is a weight of 569, rounded up?", "print(-(-569 // 4))", ["142", "142.25", "144"],
  "142.25 rounds up to 143.")
q("BlockWeightLimit", "Remember", "What is the block weight limit?",
  ["4,000,000 weight", "1,000,000 bytes", "2,000,000 weight", "8,000,000 vbytes"],
  "Bitcoin Core's MAX_BLOCK_WEIGHT, from BIP141.")
a("BlockWeightLimit", "How many transactions of 569 weight would fill a 4,000,000-weight block?", "print(4_000_000 // 569)", ["7030", "1000000", "4000"],
  "Integer division gives 7,029.")
q("WeightFactor", "Remember", "Which fields carry a weight factor of 1?",
  ["The marker, the flag and the witness structure", "The version and the lock time", "The outputs", "The input scripts"],
  "Everything legacy nodes see weighs four per byte.")
a("WeightFactor", "A 36-byte outpoint at factor 4 and a 65-byte witness item at factor 1: what do they weigh together?", "print(36 * 4 + 65 * 1)", ["404", "101", "144"],
  "144 plus 65 is 209.")
q("Foundations", "Understand", "Why does the distinction between relay policy and consensus keep coming up?",
  ["Half the rules met - dust, standardness, replacement, version 3 - are policy, which a node may choose, not validity", "Because policy is written in BIPs", "Because consensus changes every release", "Because policy decides the subsidy"],
  "Only consensus decides which blocks are valid.")
q("HashFunction", "Understand", "Which two properties of a hash function do transaction identifiers rely on?",
  ["A fixed-length output and unpredictable change when the input changes", "Reversibility and speed", "Compression and encryption", "Randomness and a secret key"],
  "Fixed length lets a 32-byte txid stand for any transaction; sensitivity is why identifiers are trustworthy and malleability dangerous.")
a("HashFunction", "What is the length of SHA-256 of an empty input, in bytes?", "import hashlib\nprint(len(hashlib.sha256(b'').digest()))", ["0", "64", "20"],
  "The output length does not depend on the input.")
q("DoubleSha256", "Remember", "How is a transaction identifier computed?",
  ["SHA-256 of SHA-256 of the legacy serialization, shown reversed", "SHA-256 of the full serialization", "RIPEMD-160 of the outputs", "A checksum of the version"],
  "Bitcoin Core calls the construction hash256.")
a("DoubleSha256", "Double-hash the bytes b'hello' and reverse the digest. What are the first four hexadecimal characters?",
  "import hashlib\nd = hashlib.sha256(hashlib.sha256(b'hello').digest()).digest()\nprint(d[::-1].hex()[:4])", ["9595", "2cf2", "0000"],
  "The reversed double SHA-256 of hello begins 503d.")
q("Txid", "Understand", "What does the txid of a segwit transaction exclude?",
  ["The witness, so a change of witness leaves the txid unchanged", "The outputs", "The version", "The inputs"],
  "That is the whole repair segregated witness makes.")
a("Txid", "How many hexadecimal characters does a txid have?", "print(len('466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177'))", ["32", "128", "40"],
  "32 bytes are 64 characters.")
q("Wtxid", "Understand", "Why does BIP141 add a second identifier?",
  ["Something must commit to the witness, which the txid leaves out", "The txid was too short", "To number the outputs", "To replace the merkle root"],
  "A block commits to wtxids through an output of its coinbase.")
a("Wtxid", "Are Alice's txid 46620030... and wtxid f7cdbc7c... different?",
  "txid = '466200308696215bbc949d5141a49a4138ecdfdfaa2a8029c1f9bcecd1f96177'\nwtxid = 'f7cdbc7cf8b910d35cc69962e791138624e4eae7901010a6da4c02e7d238cdac'\nprint(txid != wtxid)", ["False", "None", "0"],
  "A transaction with a witness has two different identifiers.")
q("RelayPolicy", "Understand", "What is relay policy?",
  ["The rules a node applies to unconfirmed transactions it relays and keeps, chosen by the node", "The rules every node must enforce identically", "The subsidy schedule", "The format of a block"],
  "A transaction that violates policy can still be mined and be valid.")
a("RelayPolicy", "Sort the five policies met: dust limit, standard outputs, version 3 restrictions, replace-by-fee, reserved features. Which is first?",
  "print(sorted(['dust limit', 'standard outputs', 'version 3 restrictions', 'replace-by-fee', 'reserved features'])[0])", ["replace-by-fee", "reserved features", "standard outputs"],
  "In the default string order, dust limit sorts first.")
q("ConsensusRule", "Understand", "Which of these is a consensus rule rather than a policy?",
  ["The maturity of coinbase outputs", "The dust limit", "The standard output templates", "The version 3 topology restrictions"],
  "Maturity is checked by every node in block validation; the other three are relay policy.")
a("ConsensusRule", "How many consensus rules are listed in the sorted list of eight?",
  "print(len(sorted(['at least one input and one output', 'amount range', 'no double spend', 'BIP68 sequence locks', 'lock time since block 31,000', 'subsidy and reward', 'coinbase maturity', 'block weight'])))", ["7", "6", "9"],
  "Eight rules from this chapter.")

# ============================== the file ==============================
_XMETA = re.compile(r"\b(chapter|section|the book|the author|the authors|this text)\b", re.I)
# the right option of an Apply item is what its program prints; one program at a time, like the checker
for k, it in enumerate(I):
    concept, level, question, options, why, code = it
    if code:
        r = subprocess.run([PY, "-c", code], capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            raise SystemExit("item %d (%s) failed: %s" % (k, concept, r.stderr[-300:]))
        out = r.stdout.strip()
        if not out:
            raise SystemExit("item %d (%s) printed nothing" % (k, concept))
        if out in options[1:]:
            raise SystemExit("item %d (%s): a distractor equals the real output %r" % (k, concept, out))
        options = [out] + options[1:]
        I[k] = (concept, level, question, options, why, code)
    assert len(options) == 4 and len(set(options)) == 4, (concept, options)
    assert not _XMETA.search(question) and not _XMETA.search(options[0]), (concept, question)
items = []
for k, (concept, level, question, options, why, code) in enumerate(I):
    pos = k % 4
    opts = options[1:1 + pos] + [options[0]] + options[1 + pos:]
    assert opts[pos] == options[0] and sorted(opts) == sorted(options), (concept, question)
    it = {"concept": concept, "level": level, "q": question, "options": opts, "answer": pos, "why": why}
    if code:
        it = {"concept": concept, "level": level, "q": question, "code": code, "options": opts, "answer": pos, "why": why}
    items.append(it)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ch06-page", "question_bank_v1_0_0.json")
json.dump(items, open(out, "w"), indent=1)
import collections
print("wrote %s: %d items, %d concepts covered, %d with code" % (os.path.basename(out), len(items), len({i['concept'] for i in items}), sum(1 for i in items if 'code' in i)))
print("positions:", dict(sorted(collections.Counter(i["answer"] for i in items).items())))
