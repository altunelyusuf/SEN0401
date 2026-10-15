"""SEN0401 chapter 9: the teaching paragraphs of the leaves of subjects 1 (who pays the fee) and 2 (fees and fee rates). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023)."""
__version__ = "1.0.0"
A = {}

A["FeeIsInputsMinusOutputs"] = (
 "A Bitcoin transaction has no field called fee; the fee is whatever is left over when the values of all the outputs are subtracted from the values of all the inputs, and the miner who includes the transaction collects that remainder (Antonopoulos and Harding, 2023). "
 "This matters because the person building a transaction has to account for every satoshi: the node can only check that the outputs do not exceed the inputs, and it cannot know what the sender meant to keep. "
 "Think of paying a shop bill with a banknote and walking away without waiting for the change; the difference is gone, and nobody can tell it was a mistake. In this study the 31.1 node of Bitcoin Core was started on a private test chain (regtest) and a transaction spent one 20-bitcoin output to make a payment of 1 bitcoin with no change output at all; "
 "an independent parser written for this chapter read the raw bytes of the transaction, summed the output values, and obtained 1,900,000,000 satoshis (19 bitcoins) as the difference, exactly the fee the node listed for the transaction in its mempool, the waiting room of unconfirmed transactions (Bitcoin Core, 2026).")

A["ForgottenChangeBecomesFee"] = (
 "A change output is the output that sends the unspent remainder of an input back to the sender; if it is left out, the remainder silently becomes fee, which the book illustrates with a 20-bitcoin output used for a 1-bitcoin payment so that 19 bitcoins would go to the miner (Antonopoulos and Harding, 2023). "
 "Nodes therefore carry a safety net: sendrawtransaction refuses by default any transaction whose fee rate is above DEFAULT_MAX_RAW_TX_FEE_RATE, a constant of COIN divided by 10 per kilo-virtual-byte (Bitcoin Core, 2026). It is like a bank that stops a transfer of an absurd amount until you confirm it. "
 "In the run the node answered testmempoolaccept with the reason max-fee-exceeded and sendrawtransaction with an error naming maxfeerate; the transaction was then submitted on purpose with that check switched off, mined in the next block, and the coinbase transaction of that block paid out 4,400,000,000 satoshis, the regtest subsidy of 2,500,000,000 plus the 1,900,000,000 that should have been change.")

A["NoFeeFieldInTransaction"] = (
 "The serialized transaction that nodes exchange contains a version, a list of inputs, a list of outputs, optional witness data and a lock time, and nothing else; the fee is never written into it (Antonopoulos and Harding, 2023). "
 "That design is deliberate and efficient: because the signature of every input commits to all the outputs, the spender commits to the fee without spending one extra byte of block space on a fee field, and any node can recompute the fee by looking up the values of the outputs being spent. "
 "It is the same as a receipt that lists only what was handed over and what came back, so that the shop's take is simply the gap. The chapter's own parser, written without Bitcoin Core code, split the 191-byte transaction of the run into its parts, found one input and one output, rebuilt the transaction identifier (txid) by hashing the serialization without witness data, and confirmed that it matched the node's identifier; no key called fee exists in the result (Antonopoulos and Harding, 2023).")

A["FeeNeedsSpendersSignature"] = (
 "Because a signature commits to the outputs of a transaction, nobody can add to the fee of someone else's transaction, and a fee needs the spender's agreement; the book states that it is not possible for a transaction to pay a fee without the permission of the spender (Antonopoulos and Harding, 2023). "
 "In the run a signed one-input transaction was first checked with testmempoolaccept, the RPC that tests a transaction against the mempool rules without broadcasting it, and was allowed; the same bytes were then altered so that the first output was 5,000 satoshis smaller, which would have increased the miner's fee by 5,000 satoshis, and the node refused it with a script verification failure saying that the signature must be zero for failed CHECK(MULTI)SIG operation, which is the way the node reports that the signature no longer fits the changed data. "
 "A cheque works in the same way: if a stranger changes the amount after you have signed, the bank will not honour it. This is why fees are customarily paid by the spender and why a receiver who wants more speed must pay in a separate transaction (Antonopoulos and Harding, 2023).")

A["FeePaidInAnotherTransaction"] = (
 "A receiver of money cannot raise the fee of the transaction that paid them, but they can spend the output they received in a new transaction that pays a high fee; because that child can only be mined together with its parent, the miner is paid for both, which is the idea of child pays for parent (CPFP) (Antonopoulos and Harding, 2023). "
 "The fee is then paid in a different transaction than the one it helps. It is like a passenger who is stuck in a queue and pays the ferryman extra so that the whole line moves. "
 "In the run a parent paid 141 satoshis (1 satoshi per virtual byte) and its child 14,100 satoshis (100 per virtual byte); the block that the node assembled contained both, with the parent placed before the child as the rules of consensus demand, and the miner received 14,241 satoshis for the pair (Bitcoin Optech, 2026). "
 "This is the exception the book mentions when it says that the receiver of a transaction can pay a fee in a different transaction (Antonopoulos and Harding, 2023).")

A["FeeIsABid"] = (
 "The book explains that a transaction fee is not a price set by the protocol or by a miner but a bid in an auction for the limited space of a block, and that miners choose the set of transactions whose bids earn the greatest revenue (Antonopoulos and Harding, 2023). "
 "Bitcoin Core's block assembler works that way: it takes groups of transactions in order of fee rate, the fee divided by the size, until the block weight limit is reached (Bitcoin Core, 2026). It is the same as a market stall owner who fills a limited table with the goods that bring the most money per square centimetre. "
 "To test this the node was offered ten independent transactions of the same size with fees from 141 to 7,050 satoshis, that is 1 to 50 satoshis per virtual byte, in scrambled order, and its block template listed all ten sorted from the highest fee rate to the lowest, 50.0 first and 1.0 last; the ordering was recomputed by the chapter from the fee and weight that the template reports. "
 "The result is a single run on one node, and other miners may use other software or other rules, because only the block's validity is enforced by the network (Antonopoulos and Harding, 2023).")

A["CoinbaseIsExcluded"] = (
 "The first transaction of every block is the coinbase transaction, which creates the new bitcoins of the block subsidy and collects the fees of all the other transactions; it spends no earlier output, so it pays no fee and cannot be fee bumped, and the book therefore ignores it when it talks about transactions in this chapter (Antonopoulos and Harding, 2023). "
 "The sum it may claim is set by consensus: the subsidy of the block height plus the total of the fees, checked in the source function that connects a block (Bitcoin Core, 2026). It is like the cashier's own till, which receives the takings of the day without having paid anyone. "
 "In block 840,000, mined on 2024-04-20 by the pool ViaBTC according to the explorer mempool.space, the first transaction has the coinbase marker in its input, the subsidy computed by the chapter for that height is 312,500,000 satoshis, the fees reported are 3,762,561,499 satoshis, and their sum, 4,075,061,499 satoshis, is exactly the block reward the explorer lists (Mempool Space, 2026).")

A["WeightAndVirtualSize"] = (
 "Since segregated witness, the size of a transaction that matters for fees is its weight, in weight units: the bytes without witness data count four times and the witness bytes (the signatures) once, so weight is three times the base size plus the total size, and the virtual size in virtual bytes is the weight divided by four and rounded up (Lombrozo et al., 2015). "
 "It is like a post office that charges full price for the parcel and a quarter price for the packing paper. A one-input, two-output transaction of the run has 113 bytes without witness and 222 bytes with it; the chapter's parser computed 3 x 113 + 222 = 561 weight units and 141 virtual bytes, and both numbers equal what the node says when it decodes the same transaction (Bitcoin Core, 2026). "
 "This matters because block space and fees are counted in these units, and a wallet that estimated a fee from the plain byte length would overpay for the discounted witness bytes (Antonopoulos and Harding, 2023).")

A["BlockWeightLimit"] = (
 "A block may weigh at most 4,000,000 weight units, a limit defined by BIP 141 and written in Bitcoin Core as the constant MAX_BLOCK_WEIGHT, together with the witness scale factor of 4 (Lombrozo et al., 2015). "
 "Because the room in a block is finite, transactions compete for it, and that competition is what gives fees their value; it is the same as seats in a lift, where the operator prefers the passengers who pay the most for each seat taken. "
 "Block 840,000 weighed 3,993,281 weight units according to the explorer, which is 998,321 virtual bytes and 99.83 percent of the limit, so the block was full and the 3,050 transactions it contained had to be chosen from a longer queue (Mempool Space, 2026). "
 "The chapter recomputed the share from the numbers of the block record and read the constant from the source file at the pinned release, v31.1 (Bitcoin Core, 2026).")

A["FeeRateDefinition"] = (
 "The fee rate is the price per unit of block space: the fee divided by the size of the transaction, in satoshis per virtual byte (sat/vB) or per weight unit; the book compares it to dividing the price of bags of rice by their weight to find the best deal (Antonopoulos and Harding, 2023). "
 "One sentence of the printed book says the opposite, that the term fee rate is used for a transaction's size divided by weight, which gives a number without any price in it; the sentence is an error of wording that the book's later text and every wallet contradict, and it is not corrected in the development branch of the book repository either (Antonopoulos and Harding, 2023). "
 "The chapter computed it for a transaction of the run that paid 282 satoshis for 141 virtual bytes: the fee divided by the size is 2.0 satoshis per virtual byte, or 0.5027 per weight unit, while the size divided by the weight is 0.2513, a pure number that no miner could use to compare bids (Bitcoin Core, 2026).")

A["UnitsOfFeeRate"] = (
 "A fee rate can be written in several units: the book lists satoshis per virtual byte (the most common today), satoshis per weight unit, and bitcoin per kilo-virtual-byte, which is the unit Bitcoin Core uses in its RPC answers (Antonopoulos and Harding, 2023). "
 "Converting needs care, as between litres per hundred kilometres and miles per gallon. The book's example answer of estimatesmartfee is 0.00006570 bitcoin per kilo-virtual-byte; multiplied by 100,000,000 satoshis per bitcoin and divided by 1,000 bytes per kilo-byte it is exactly 6.57 satoshis per virtual byte, computed in the chapter with exact fractions, and the 31.1 node's own answer of the run, 0.00001225, is 1.225. "
 "The same arithmetic shows that one bitcoin per kilo-virtual-byte would be 100,000 satoshis per virtual byte, which is the size of the mistake that a user could make by writing a number in the wrong field (Antonopoulos and Harding, 2023) (Bitcoin Core, 2026).")

A["WrongUnitFactor"] = (
 "The book warns that a fee rate copied into a field with another denominator can overpay by a factor of 1,000, or by 100,000,000 if the numerator is changed as well, and that wallets should make such a mistake hard (Antonopoulos and Harding, 2023). "
 "Bitcoin Core's wallet RPCs have two fields for the same idea, fee_rate in satoshis per virtual byte and feeRate in bitcoin per kilo-virtual-byte, and the run shows that the two are consistent: asking fundrawtransaction for fee_rate 10 and for feeRate 0.0001 produced the identical fee of 1,410 satoshis on the same transaction (Bitcoin Core, 2026). "
 "The same number 10 in the bitcoin field would mean 10 bitcoins per kilo-virtual-byte, and the node refused it because the coins to be spent could not cover such a fee; the factor between the two units is 10^8 / 10^3 = 100,000. This is like writing a distance in miles on a form that wants metres; the safety net is the wallet, not the number (Antonopoulos and Harding, 2023).")

A["AbsurdFeeGuard"] = (
 "An absurd fee, in the book's words, is a fee rate far above what estimators expect to be needed for the next block, and wallets should make it hard to pay one by accident without forbidding it, because there are rare legitimate reasons (Antonopoulos and Harding, 2023). "
 "Bitcoin Core implements the guard for raw transactions as DEFAULT_MAX_RAW_TX_FEE_RATE, set to COIN divided by 10 per kilo-virtual-byte, which is 0.1 bitcoin per kilo-virtual-byte or 10,000 satoshis per virtual byte; the override is the argument maxfeerate (Bitcoin Core, 2026). "
 "It resembles the limit on a payment card that asks for a second confirmation. The transaction of the run that paid 19 bitcoins over 110 virtual bytes paid 17,272,727 satoshis per virtual byte, 1,727 times the guard, and the node refused it with max-fee-exceeded until the argument was changed. "
 "The guard is a policy of the node and not a rule of the network, so a miner would still accept such a transaction in a block (Antonopoulos and Harding, 2023).")

A["MinRelayFee"] = (
 "The minimum relay fee rate is the lowest rate at which a node will accept a transaction into its mempool and pass it on, so that nobody can fill the memory of the network with free transactions; since release 30.0 its default and that of the incremental relay fee are 0.1 satoshi per virtual byte (Bitcoin Core developers, 2025). "
 "It is like a minimum stamp price for letters. The source constants DEFAULT_MIN_RELAY_TX_FEE and DEFAULT_INCREMENTAL_RELAY_FEE both read 100 in the unit of satoshis per kilo-virtual-byte, which is 0.1 per virtual byte (Bitcoin Core, 2026). "
 "On the regtest node, whose getmempoolinfo reports the same minimum, a 141-virtual-byte transaction needs 14.1 satoshis, so 15; the node refused 8 satoshis and 14 satoshis with min relay fee not met, giving the numbers 8 < 15 and 14 < 15 in its message, and accepted 15. "
 "The rate is a default of the software and not a rule of Bitcoin, so some nodes and miners have different ones, which is why a transaction that is below it may still be mined by a miner who accepts it directly (Antonopoulos and Harding, 2023).")

A["WalletMinimumFee"] = (
 "The wallet that builds transactions for the user has its own floor, set by -mintxfee and defaulting to DEFAULT_TRANSACTION_MINFEE of 1,000 satoshis per kilo-virtual-byte, that is 1 satoshi per virtual byte (Bitcoin Core, 2026). "
 "That is ten times the 0.1 that relaying nodes accept since release 30.0, so the wallet is more cautious than the network, like a shopkeeper who adds a margin to the wholesale price. "
 "The second regtest run asked the wallet's send RPC for rates of 0.5, 0.1 and 1 satoshis per virtual byte: it refused 0.5 and 0.1 with the message that the fee rate is lower than the minimum fee rate setting of 1.000 sat/vB and accepted 1, while the node's own getmempoolinfo reported a minimum relay rate of 0.1. "
 "A wallet that wants to use the new low rates must therefore have its setting changed too, while the release notes advise that the two relay settings, the minimum and the incremental fee rate, are changed together (Bitcoin Core developers, 2025).")

A["DustThreshold"] = (
 "An output is called dust when spending it would cost more in fees than it is worth, and nodes refuse to relay transactions that create such outputs; at the default dust rate of 3 satoshis per byte the threshold is the output size plus the 67 bytes of a witness input, times 3 (Bitcoin Core, 2026). "
 "A coin worth less than the cost of picking it up is not worth picking up. The chapter computed (31 + 67) x 3 = 294 satoshis for a P2WPKH output, (43 + 67) x 3 = 330 for a P2WSH output and (13 + 67) x 3 = 240 for a pay-to-anchor output, the values the Lightning specification lists (Lightning developers, 2026). "
 "On the regtest node outputs of 293, 329 and 239 satoshis were refused with the reason dust, and outputs of 294, 330 and 240 were accepted. "
 "Dust matters for fee bumping because the anchor outputs of channels are deliberately close to this limit, and release 29.0 made one exception, a zero-fee transaction with a single dust output that must be spent by its child (Bitcoin Core developers, 2025).")
