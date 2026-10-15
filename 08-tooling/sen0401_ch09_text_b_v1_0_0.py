"""SEN0401 chapter 9: the teaching paragraphs of the leaves of subjects 3 (fee estimation) and 4 (replace by fee). One paragraph per leaf, one line, full sentences."""
__version__ = "1.0.0"
B = {}

B["EstimateSmartFeeCall"] = (
 "Because fees are bids in an auction, no one can know in advance which fee rate will be enough, but a full node can learn from the past: it notes when it first saw each transaction, in which block it was confirmed and what fee rate it paid, groups similar ones and reads off how many blocks transactions of a given rate usually waited (Antonopoulos and Harding, 2023). "
 "Bitcoin Core offers this as the RPC estimatesmartfee, and the book shows the call bitcoin-cli -named estimatesmartfee conf_target=144 answering 0.00006570 bitcoin per kilo-virtual-byte for 144 blocks, about one day. It is like a weather forecast made from the record of earlier days. "
 "A brand-new regtest node answered the same call with the error Insufficient data or no feerate found, because it had seen no history; after the chapter's script had made 120 blocks with 2,640 payments of mixed fee rates the node answered 1.225 satoshis per virtual byte for 2 blocks and 1.173 for 6 and 25 blocks. "
 "These numbers describe the artificial market of the test and say nothing about the real network, whose estimate on the day of the study could not be asked because no network node was run (Bitcoin Core, 2026).")

B["ConfirmationTargetLimits"] = (
 "The RPC takes a confirmation target in blocks from 1 to 1008, as its help text in the source says, but a target is only as good as the history behind it: the estimator keeps several time scales and the function MaxUsableEstimate limits the target to half the span of blocks it has seen, so that there are enough failing data points for the estimate to mean something (Bitcoin Core, 2026). "
 "A forecaster with two weeks of records cannot honestly promise a forecast for next year. "
 "On the test chain, which was 231 blocks high at the time, the call for the target 144 was answered with the field blocks equal to 60 instead of 144, so the answer states for which target it is valid, and the book's listing, which shows 144 returned as 144, is true only for a node with a long history (Antonopoulos and Harding, 2023). "
 "A wallet that asks for a long target must therefore read the blocks field of the answer and not assume that its wish was granted (Bitcoin Optech, 2026).")

B["EstimatorThresholds"] = (
 "The estimator does not average fees; it looks for the lowest fee rate bucket for which enough of the transactions that paid it were really confirmed within the target. In the header file of the estimator three constants state what enough means: more than 85 percent of the transactions of a rate must confirm within the target (SUCCESS_PCT), 60 percent within half the target (HALF_SUCCESS_PCT) and 95 percent within double the target (DOUBLE_SUCCESS_PCT) (Bitcoin Core, 2026). "
 "It is the same logic as a school that wants a grade to be passed by most pupils who studied that much, and not only by the average pupil. "
 "The book describes the method in words and does not give these numbers; the chapter read them from the saved source of release 31.1, and they explain why an estimate can be higher than the lowest fee that was ever confirmed in time (Antonopoulos and Harding, 2023). "
 "The conservative mode demands the double-target condition for longer time horizons in addition (Bitcoin Core, 2026).")

B["DefaultModeEconomical"] = (
 "The estimator can answer in two modes, economical, which reacts quickly to recent data and so may give lower fee rates, and conservative, which also requires the longer horizon to agree and so gives higher and steadier ones. Release 28.0 changed the default mode of estimatesmartfee from conservative to economical, in the words of its notes expecting less overestimation, particularly for users of replace by fee (Bitcoin Core developers, 2024). "
 "It is like choosing between today's forecast and the forecast that also respects the season. "
 "The source of release 31.1 shows the argument default economical (Bitcoin Core, 2026), and the run confirms it: at the targets 2, 6, 25 and 144 the default answer equals the economical answer, and at 144 blocks the economical estimate was 1.122 satoshis per virtual byte, the conservative one 1.173, and the default 1.122, so a program written for an older release that relied on the conservative default now receives lower numbers. "
 "Optech lists the change among its entries for fee estimation (Bitcoin Optech, 2026).")

B["BlockFeeCensus"] = (
 "To see what fees look like on the real network, the chapter downloaded from the explorer mempool.space the first 600 transactions of two blocks and recomputed the fee rate of each as its fee divided by its weight over four, leaving out the coinbase: block 840,000, the fourth halving block of 2024-04-20, and block 971,489, mined on 2026-10-15 (Mempool Space, 2026). "
 "Within the 599 transactions that follow the coinbase, the median fee rate was 1,436.45 satoshis per virtual byte in the first block and 3.02 in the second, while the explorer's own median for the whole block is 200 and 1 satoshis per virtual byte; the sample is the first part of the explorer's list of the block, and the large difference of the medians shows that it is the better-paying part and not the whole block. "
 "It is like looking at the price tags on the first shelf of a shop. The census shows that fee levels differ by a factor of hundreds between times, which is why an estimator must always be fed with recent data (Antonopoulos and Harding, 2023).")

B["RecommendedFeesToday"] = (
 "Public explorers publish fee recommendations that the book calls web-based fee estimation services (Antonopoulos and Harding, 2023). On 2026-10-15 the endpoint of mempool.space answered with a fastest, half-hour, hour, economy and minimum fee of 1 satoshi per virtual byte each, which suggests that the blocks had spare room and that the lowest rate was enough (Mempool Space, 2026). "
 "Its record of average fees per block group over the last year contains 1,096 points, from 798,426 satoshis at the lowest to 8,098,275 satoshis at the highest, about a tenfold range in what miners were paid in fees on average per block. "
 "It resembles the fare of a taxi that is cheap at night and expensive in the rain. The numbers are a snapshot of one site on one day and not a property of Bitcoin; they illustrate the book's remark that demand can change and move the equilibrium of fees up or down (Antonopoulos and Harding, 2023).")

B["RevealedFeeBehaviour"] = (
 "Before the fee market could be studied as a market, someone had to look at what people really paid. Moeser and Boehme analysed the historical behaviour of Bitcoin users in paying fees, identified several regime shifts that are largely explained by changes in the default client software or by the actions of big intermediaries, and concluded that rules dominate ratio, a state that is sustainable only while fees remain negligible (Moeser and Boehme, 2015). "
 "Their table of transaction latency for June 2012 to May 2013 gives the median wait in seconds: 1,339 for 1,503 transactions that paid no fee, 600 for 5,735 transactions that paid 0.0005 bitcoin and 520 for 1,905 that paid 0.001, and ten percent of the zero-fee transactions waited almost four hours, 13,927 seconds. "
 "It is like finding the price of a service by watching what people really put into the basket and not by asking them. The chapter's check confirms that these numbers stand in the saved copy of the paper; it does not recompute them, because that would need the blockchain of 2012 and 2013 (Moeser and Boehme, 2015).")

B["OptInSignalRule"] = (
 "Replace by fee (RBF) means that a node replaces a transaction in its mempool with a conflicting one that pays more. The version of the rule that Bitcoin Core introduced in release 0.12.0 was optional for the sender: a transaction signals that it may be replaced when at least one of its inputs has a sequence number below 0xfffffffe, as BIP 125 specifies (Harding, 2015), and release 0.12.0 listed it among its changes (Bitcoin Core developers, 2016). "
 "It is like a note on a parcel saying that the contents may be exchanged. The chapter's rule function gives true for 0xfffffffd, false for 0xfffffffe and 0xffffffff, and true for a transaction with several inputs when at least one signals; all 60 transactions that Bitcoin Core's wallet built in the run carried the single sequence 0xfffffffd, the value that signals while leaving the lock time active (Bitcoin Core, 2026). "
 "The book calls opt-in RBF the signalling variant that has been default in Core for several years, and notes that a wallet only has to set a sequence number to use it (Antonopoulos and Harding, 2023).")

B["SignalInTheWild"] = (
 "If every wallet signalled, the signal would say nothing; the chapter therefore counted how many real transactions signal. Of the first 599 transactions after the coinbase of block 840,000, mined on 2024-04-20, 485 (81 percent) had an input with a sequence number below 0xfffffffe, and of the same number of block 971,489, mined on 2026-10-15, 273 (46 percent) did (Mempool Space, 2026). "
 "The share is large enough that merchants cannot treat the lack of a signal as a safe sign any more, but also shows that many wallets have no reason to set the signal now that nodes replace transactions without it; it is the same as a lock that half of the doors in a street no longer have. "
 "The count reads the sequence fields in the explorer's record and applies the BIP 125 rule of the preceding leaf (Harding, 2015). "
 "A sample of 599 transactions of two blocks cannot give a figure for the whole chain, and the book's statement that merchants can check the signal remains technically true but of lower value (Antonopoulos and Harding, 2023).")

B["FullRbfDefault"] = (
 "Full RBF means that any unconfirmed transaction can be replaced by a conflicting one that pays enough, with or without a signal. The book says that full RBF can be optionally enabled in Bitcoin Core but is disabled by default (Antonopoulos and Harding, 2023); this has changed. "
 "Release 24.0.1 added the option -mempoolfullrbf with default off (Bitcoin Core developers, 2022), and release 28.0 changed its default from 0 to 1 (Bitcoin Core developers, 2024). It is as if a shop that only exchanged goods in boxes marked exchangeable now exchanges any goods. "
 "On the 31.1 node getmempoolinfo reports fullrbf true; a transaction with the final sequence 0xffffffff, which does not signal, was replaced by a transaction that spent the same output and paid twice the fee, and the first transaction left the mempool. "
 "The change is the end of a long dispute between merchants who accepted unconfirmed payments and developers, told in the first story of this chapter, and it is the first of the book's statements that is out of date today (Todd, 2022).")

B["RemovedOption"] = (
 "A configuration option that stays forever makes a policy look like a choice, so developers remove options once nobody benefits from switching them. Release 29.0 notes that, starting with 28.0, -mempoolfullrbf defaulted to 1, that with widespread adoption users no longer benefit from disabling it, and that the option has been removed (Bitcoin Core developers, 2025). "
 "It is like taking the switch out of a lamp that always has to be on. A 31.1 node was started on purpose with -mempoolfullrbf=0 and stopped at once with the message Error parsing command line arguments: Invalid parameter -mempoolfullrbf=0 and exit code 1; a node that is told to run with the option the book describes does not start at all. "
 "This is an example of a change of default that is also a change of interface, and a script or a service file that still passes the option breaks after an upgrade (Bitcoin Core developers, 2025).")

B["ConflictRule"] = (
 "Two transactions conflict when they spend at least one common output, because only one transaction can spend a given output in the valid chain; the book defines conflicting transactions this way and says that replacement means creating a conflicting version that pays a higher fee (Antonopoulos and Harding, 2023). "
 "It is like two cheques drawn on the same banknote. The chapter built three versions of one payment: version 0 spends input A, version 1 spends A and B, and version 2 spends B and C, and checked conflicts with the definition: versions 0 and 1 conflict (they share A), versions 1 and 2 conflict (they share B), versions 0 and 2 do not. "
 "On the node, version 1 replaced version 0 in the mempool and version 2 then replaced version 1, so only version 2 was waiting, which is what the conflict rule predicts (Harding, 2015); the consequence of the pair 0 and 2 not conflicting is shown in the leaf about paying twice.")

B["AbsoluteFeeRule"] = (
 "A replacement must pay at least as much in total fee as all the transactions it throws out; BIP 125 requires that the replacement pays an absolute fee of at least the sum paid by the original transactions, and Bitcoin Core's policy document of release 31.1 still lists the rule with its reason, that only requiring a higher fee rate could allow an attacker to make a miner lose revenue (Harding, 2015) (Bitcoin Core, 2026). "
 "It is like an auction in which a new bid must at least equal the old one in money and not only in percentage. "
 "On the regtest node a payment of 282 satoshis was replaced by one of 564, and then two more replacements of the second were tried: one paying 514 satoshis was refused with the message less fees than conflicting txs, and one paying the same 564 satoshis was refused with not enough additional fees to relay. "
 "The book mentions that Core requires a higher total fee and that developers wished to remove this requirement because of its side effects, which are the subject of the leaf on pinning by a large child (Antonopoulos and Harding, 2023).")

B["IncrementalFeeRule"] = (
 "A replacement must also pay for the bandwidth it costs the network: the extra fee over the replaced transactions must be at least the incremental relay fee times the replacement's own virtual size, which the policy document illustrates with 0.1 satoshi per virtual byte and a replacement of 500 virtual bytes, that must pay at least 50 satoshis more (Bitcoin Core, 2026). "
 "Without this rule an attacker could send endless replacements that each raise the fee by one satoshi, like a bidder who raises by a cent a thousand times. "
 "On the regtest node the first payment of 564 satoshis was replaced by a transaction of the same size, 141 virtual bytes, so the least acceptable fee was 564 + 15 = 579 satoshis (the chapter's function gives 579); 578 satoshis were refused with 14 satoshis of additional fee when 15 were needed, and 579 were accepted. "
 "The rule exists in BIP 125 and the incremental fee is a setting of the node that became 0.1 satoshi per virtual byte in release 30.0 (Harding, 2015) (Bitcoin Core developers, 2025).")

B["FeeBumpWithWallet"] = (
 "A user does not have to build replacements by hand: the wallet RPC bumpfee creates the new version, reduces the change or adds inputs, signs it and sends it. The book advises developers to give users a fee-bumping interface that does all this work and asks only how much the fee rate should rise (Antonopoulos and Harding, 2023). "
 "The wallet's source computes the least acceptable total fee as the old fee plus the incremental relay fee for the new size, the same rule as above (Bitcoin Core, 2026). It is like a lift button that asks only for the floor. "
 "In the run a two-input transaction of 208 virtual bytes paid 416 satoshis (2.0 satoshis per virtual byte) and signalled with the sequence 0xfffffffd on both inputs; bumpfee replaced it with a transaction of the same size paying 1,457 satoshis (7.0 per virtual byte) and the original left the mempool. "
 "This is the method that the book calls the efficient one, because the replacement is often no larger than the original (Antonopoulos and Harding, 2023).")

B["FeerateDiagramRule"] = (
 "Newer versions of Bitcoin Core judge a replacement by a more general idea than a higher fee rate: the feerate diagram, a curve that shows how much fee a miner collects as the block space used grows when the mempool is taken in the best order. A replacement is accepted only if the diagram after the replacement is strictly better, and the code says so in a comment of its function ImprovesFeerateDiagram (Bitcoin Core, 2026). "
 "It is like comparing two shopping routes by the whole receipt at every stage and not by one price. The rules numbered 3 and 4 of the older policy, the absolute fee and the incremental fee, are still listed in the policy document of release 31.1, with the marks that some of the older rules were removed (Bitcoin Core, 2026). "
 "The diagram is built from the ordered chunks of the cluster mempool that Daftuar and his coauthors describe (Daftuar et al., 2024). "
 "This leaf quotes the source and is checked only as a passage; no test of the run was designed to make a replacement fail this rule alone.")

B["ThreeVersionsPaidTwice"] = (
 "The book warns that when a payment is replaced more than once, all versions must conflict with each other, or several of them can be confirmed and the receiver is paid twice. It gives the example of version 0 with input A, version 1 with A and B, and version 2 with B and C: a miner who saved version 0 can mine both it and version 2 (Antonopoulos and Harding, 2023). "
 "The chapter ran this on the node. The payment was 0.4 bitcoin; versions 0, 1 and 2 were created, and a miner that kept version 0 was imitated by the generateblock RPC, which mines a raw transaction that need not be in the mempool. Block one contained version 0; version 2 was still valid and waiting, and block two contained it; the payee received 80,000,000 satoshis instead of the 40,000,000 asked. "
 "It is like paying a bill twice because the first receipt was not cancelled. The simple remedy of the book is that every replacement keeps all the inputs of the previous version (Antonopoulos and Harding, 2023).")

B["LargeChildPin"] = (
 "Transaction pinning is making a fee bump so expensive or so impossible that it fails. One kind arises from the rule of absolute fees: if Alice's payment is about 100 virtual bytes and Bob spends it in a child of 100,000, replacing Alice's payment needs a fee that also covers Bob's child, and at the same fee rate it costs 1,001 times what she paid in the first place (Antonopoulos and Harding, 2023). "
 "It is like a parked car that is boxed in by a lorry: moving it means paying for the lorry too. In the run a parent of 141 virtual bytes paid 705 satoshis, and a child of 90,012 virtual bytes was attached to it at 5 satoshis per virtual byte; a replacement at 6 satoshis per virtual byte was refused with less fees than conflicting txs, and the least replacement that the node accepted paid 450,780 satoshis, which is 639 times the original fee. "
 "Release 28.0 and BIP 431 limit this kind of pin for version-3 transactions, which a later leaf measures (Zhao, 2024).")

B["ReplacementCycling"] = (
 "Replacement cycling is an attack on protocols with time limits, such as the hash time-locked contracts (HTLCs) of the Lightning Network, in which a payment must be claimed before a certain block. Mallory, who is the counterparty, repeatedly replaces Bob's claim transaction with one of her own and then removes her transaction in turn, so that Bob's claim is dropped from mempools and does not confirm in time, and she can steal the payment (Bitcoin Optech, 2026). "
 "It is like a thief who pulls the document from the letterbox, every time just before the postman takes it. "
 "Antoine Riard described it on the mailing lists in October 2023 and Optech's newsletter 274 of 2023-10-25 summarised the attack and the mitigations that Lightning implementations deployed (Bitcoin Optech, 2023). "
 "This leaf reports a published claim; the chapter's check finds the passages in the saved copies, and the attack was not executed because it needs several peers with their own mempools while the study ran one node, so it is listed among the experiments not carried out.")
