"""SEN0401 chapter 9: the teaching paragraphs of the leaves of subjects 5 (child pays for parent, packages and the cluster mempool) and 6 (pinning, carve-out, TRUC and anchors)."""
__version__ = "1.0.0"
C = {}

C["PackageFeeRate"] = (
 "When a child spends an output of an unconfirmed parent, a miner who wants the child must also take the parent, so the sensible thing to price is the pair: the book calls it a package, with an aggregate size and aggregate fees, and the package fee rate is the total fee divided by the total size (Antonopoulos and Harding, 2023). Bitcoin Core's policy document defines the package feerate as the total modified fees divided by the total virtual size of all transactions in the package (Bitcoin Core, 2026). "
 "It is like a lorry whose driver is paid for the whole load, the good and the poor parcels together. "
 "In the run a parent paid 141 satoshis and its child 14,100 satoshis; the node's mempool entries show a chunk (a group priced together) with the fee 14,241 satoshis and the weight 1,122 weight units, which is 280.5 virtual bytes and 50.77 satoshis per virtual byte, while the chapter's exact fraction with each transaction rounded up to 141 virtual bytes gives 50.5. "
 "The parent alone, at 1 satoshi per virtual byte, would have waited for a long time (Bitcoin Optech, 2026).")

C["ChildBeatsHighRateTransaction"] = (
 "Child pays for parent works because miners rank packages and not single transactions; since release 0.13.0, Bitcoin Core builds its block templates from the feerate of a transaction inclusive of its unconfirmed ancestors (Bitcoin Core developers, 2016). "
 "To see it the node was restarted with a very small limit on the block size, so that only two of three transactions fitted: an unrelated transaction A that paid 20 satoshis per virtual byte, a parent P that paid 1, and its child C that paid 100. "
 "Taken alone A has a higher rate than P, but the package of P and C paid about 50.8, so the next block contained P and C, in that order because a parent must precede its child, and not A; the block weighed 2,014 weight units in all. "
 "It resembles a taxi dispatcher who takes the pair of passengers that together pay most. The test is a single run with an artificial limit on the block size and shows the ranking rule, not the real mix of the network (Antonopoulos and Harding, 2023).")

C["LowFeeChildLoses"] = (
 "A child does not always help: it must lift the average of the package above the competitors. In the second scenario of the run the child paid only 5 satoshis per virtual byte, so the package of parent and child paid 846 satoshis for 280.5 virtual bytes, 3.02 per virtual byte, below the 20 of the unrelated transaction A. "
 "The block with the same artificial limit contained A, and the parent and its child stayed in the mempool unconfirmed, which shows that the miner's rule is a comparison of rates and that a small tip on a stuck parent can be wasted. "
 "It is like adding a one-coin tip to a long taxi fare: it changes the average very little. The book makes the same point when it says that the miner sorts the transactions and packages by fee rate and includes the highest-revenue ones up to the maximum weight (Antonopoulos and Harding, 2023). "
 "A wallet that wants to bump with a child should therefore compute the child's fee from the package rate it needs and not from a fixed amount (Bitcoin Optech, 2026).")

C["AncestorFeerateMining"] = (
 "Ancestor fee rate mining means that a miner looks at each transaction together with all of its unconfirmed ancestors, evaluates them as one package and can take them into the block as one unit; the book says that Core has done this for many years and that it is believed that almost all miners use it (Antonopoulos and Harding, 2023). "
 "Release 0.13.0 introduced it as an algorithm that selects transactions by their feerate inclusive of unconfirmed ancestor transactions (Bitcoin Core developers, 2016). In release 31.0 the same idea lives in the cluster mempool, where the unit is the chunk, a part of the best ordering of a cluster (Bitcoin Core, 2026). "
 "In the mempool entries of the run, the parent's chunk fee equals the child's ancestor fee, and both chunks weigh 1,122 weight units, so the node's own bookkeeping treats the two transactions as one unit of 14,241 satoshis. "
 "It is like a bus fare shared by a group, where the conductor wants the group that pays most for its seats.")

C["MinimumRelayProblem"] = (
 "Child pays for parent has a hole: if the parent pays less than the minimum relay fee, a node will not keep it, and so the child that arrives later is an orphan whose parent is not known; the book calls this the minimum relay fee rate problem and says that package relay solves it, by letting nodes evaluate the fee rate of the whole package before deciding on any single transaction (Antonopoulos and Harding, 2023). "
 "It is like a letter whose stamp is too cheap: the post office rejects it at the counter, though a second stamp is in your pocket. "
 "In the run a version-2 parent paid 8 satoshis for 141 virtual bytes, below the 15 needed; testmempoolaccept refused it alone with min relay fee not met, 8 < 15, a child alone was refused as spending a missing output, and the RPC submitpackage accepted both as a package, because the child's fee of 10,400 satoshis paid for the pair. "
 "This is the behaviour that release 31.0 extended from version-3 parents to all parents of a package with one parent and one child (Bitcoin Core developers, 2026).")

C["SubmitPackageRpc"] = (
 "The RPC submitpackage, which began as an RPC for the test network only and was opened to the other networks in 2023, hands a list of related transactions to the node to be validated and accepted together; the policy document says that packages must be child-with-parents, a child and at least one of its unconfirmed parents, and that a package is limited to 25 transactions (Bitcoin Core, 2026) (Bitcoin Optech, 2026). "
 "In release 28.0 the notes tell users to use it to send packages directly and let a version-3 parent be below the minimum relay feerate, even free (Bitcoin Core developers, 2024). "
 "It is like handing in an application with all its attachments in one envelope. In the run a zero-fee version-3 parent of 123 virtual bytes and a child of 151 virtual bytes paying 10,000 satoshis were accepted with the message success; each result reports the same effective feerate of 0.00036496 bitcoin per kilo-virtual-byte, which is 36.5 satoshis per virtual byte over 274 virtual bytes. "
 "Alone, the parent was refused with min relay fee not met, 0 < 13.")

C["OneParentOneChild"] = (
 "A node cannot always be handed a package by the user; the aim of package relay is that nodes pass packages to each other. Release 28.0 delivered a limited form: a transaction whose fee rate is too low is opportunistically paired with its child and submitted as a package, so that nodes can download one-parent-one-child packages with the existing relay protocol (Bitcoin Core developers, 2024). "
 "Release 31.0 allows the parent of such a package to pay even nothing when it is not a version-3 transaction, and notes that further unconfirmed parents of the child must already be in the mempool (Bitcoin Core developers, 2026). "
 "It is like a shop that accepts a coupon only when the product comes with a paying item. The book's prediction that a limited early version may be available at the time of publication has therefore come true, while the general package relay of BIP 331, which lets nodes ask for the ancestors of a transaction, is still a proposal (Zhao, 2022). "
 "The relay between nodes was not tested in this study, which ran a single node.")

C["FeeFilterMessage"] = (
 "Nodes protect their memory with a minimum fee rate, and BIP 133 added the message feefilter to tell the peers about it: a node instructs its peers not to send it announcements, called inv messages, for transactions with a fee rate below the one it names, which saves the bandwidth on both sides (Morcos, 2016). "
 "It is like telling the paper boy not to bring the free leaflets. The book's chapter on the network prints a peer listing in which the field minfeefilter is 0.00000000, a peer that asks for everything (Antonopoulos and Harding, 2023). "
 "Release 0.13.0 notes the message among its changes and the effect on relaying below the filter feerate (Bitcoin Core developers, 2016). "
 "The reason it belongs to this chapter is that a low-fee parent that the peers filter out may never reach the miners, which is why the relay of a package as a whole has to be thought together with these filters. "
 "The study did not run a second node, so the message itself was not observed; the leaf is checked as a passage in the saved BIP and the saved chapter.")

C["ClusterLimits"] = (
 "In release 31.0 Bitcoin Core replaced the old mempool with the cluster mempool: transactions that are linked through parents and children form a cluster, and the default policy limits a cluster to 64 transactions and 101,000 virtual bytes (Bitcoin Core developers, 2026). "
 "A small number of transactions per cluster limits the work needed to order them again each time something changes, which the old limits of 25 related transactions tried to do in a coarser way. It is like a library that limits each shelf to a size that one person can sort quickly. "
 "The source constant DEFAULT_CLUSTER_LIMIT is 64 and getmempoolinfo of the node returned limitclustercount 64 and limitclustersize 101000; a chain in which each payment spent the output of the one before was sent until it was refused: 65 were attempted, 64 accepted, and the 65th was refused with too-large-cluster (Bitcoin Core, 2026). "
 "The Optech topic page describes the design (Bitcoin Optech, 2026).")

C["ChunksAndLinearization"] = (
 "A cluster is a connected component of the graph of mempool transactions; a linearization is an order of its transactions in which every parent comes before its children, and the aim is an order in which the best subset of the cluster comes first, then the best of the rest, and so on; these subsets are the chunks, whose feerates fall from one chunk to the next (Bitcoin Core, 2026). "
 "Daftuar and his coauthors propose that the sorted clusters are merged so that block building selects from the best chunks and eviction removes the set that would be selected last (Daftuar et al., 2024). It is like sorting a cupboard so that the most valuable items are in front, while keeping the boxes that are stacked together. "
 "In the run the parent paid 1 satoshi per virtual byte and its child 100: the node placed both in one chunk of 1,122 weight units, the sum of the two weights of 561, with a chunk fee equal to the sum of the two fees. "
 "The node reports these values in its mempool entries as the fee field chunk and the field chunkweight, and the terminology document of release 31.1 defines the weight fields (Bitcoin Core, 2026).")

C["RemovedAncestorLimits"] = (
 "Before release 31.0 Bitcoin Core refused to keep a transaction that would make more than 25 related transactions, or more than 101,000 virtual bytes of them, in its mempool; the book states the limits as 25 ancestors or descendants and 100,000 virtual bytes (Antonopoulos and Harding, 2023), and the notes of release 0.19.0.1 give 25 descendants and 101,000 virtual bytes (Bitcoin Core developers, 2019). "
 "Release 31.0 states that the mempool no longer enforces ancestor or descendant size and count limits and uses the cluster limits instead (Bitcoin Core developers, 2026). "
 "It is as if a speed limit had been replaced by a limit on the size of the whole convoy. In the run a chain of 26 transactions, each spending the output of the one before, was accepted, which the old rule would have refused at the 26th, and 64 were accepted in all. "
 "Two things in the book's description are therefore out of date for release 31: the numbers were wrong by 1,000 virtual bytes, and the limits no longer exist.")

C["MempoolSizeAndExpiry"] = (
 "The mempool is the memory in which a node keeps the transactions it has not yet seen confirmed. The book says that later versions of Bitcoin Core limited its size to hold about one day's worth of transactions (Antonopoulos and Harding, 2023). "
 "The constants of release 31.1 give two limits that are not about days: DEFAULT_MAX_MEMPOOL_SIZE_MB is 300 megabytes, and DEFAULT_MEMPOOL_EXPIRY_HOURS is 336 hours, which is 14 days, so that a transaction that was not mined is forgotten after two weeks (Bitcoin Core, 2026); the regtest node reports maxmempool 300,000,000 bytes. "
 "The book also says that the mempool keeps only the transactions or packages with the highest fee rate, so how long a transaction stays depends on the fee market and not on a clock; the sentence about a day is a rough picture and does not match the numbers in the code (Antonopoulos and Harding, 2023). "
 "It resembles a lift lobby with a fixed number of seats: how long a person waits depends on who else arrives (Bitcoin Core, 2026).")

C["CarveOutRule"] = (
 "In 2018 Matt Corallo proposed an exception to the descendant limits for protocols such as Lightning, in which two parties sign transactions long before they are broadcast: one extra child of the transaction may be added even when the limit is reached, so that a malicious counterparty cannot fill the space and block the other from bumping the fee (Corallo, 2018). "
 "His message of 2018-11-29 proposed that this extra transaction be of size no greater than 1K in virtual size; the rule was merged as pull request 15681 and released in 0.19.0.1, where the notes say that one extra descendant is allowed provided that it is an immediate child and its size is 10,000 virtual bytes or less (Bitcoin Core developers, 2019). "
 "The constant of release 31.1 still bears the name EXTRA_DESCENDANT_TX_SIZE_LIMIT and equals 10000 (Bitcoin Core, 2026). "
 "The book says the extra transaction may be up to 1,000 virtual bytes and the total up to 100,000, the first being the number of the proposal and the second a rounding of the 101,000 of the code (Antonopoulos and Harding, 2023); it is like quoting a price from the catalogue and not from the till. The chapter found all these texts in the saved sources.")

C["CarveOutRemoved"] = (
 "The carve-out was a patch on top of the descendant limits, and when release 31.0 replaced those limits by cluster limits, the patch had nothing to attach to. The release notes say that the CPFP Carveout has been removed from the mempool logic, and that nothing is allowed to bypass the cluster count limit; the notes expect that smart-contract uses that need similar functionality will employ TRUC transactions and sibling eviction instead (Bitcoin Core developers, 2026). "
 "It is as if a fire exit that had been added to a building was not needed after the building was redesigned. "
 "This is a change that the book could not foresee, but the book's text on the carve-out, which is a section of the chapter, now describes a rule of releases 0.19.0.1 to 30 and not of 31 (Antonopoulos and Harding, 2023). "
 "Optech's topic page still describes the carve-out as a relay policy implemented in Bitcoin Core and lists the later developments (Bitcoin Optech, 2026). The chapter found the removal in the saved notes and did not run it on a node of an older release.")

C["QuadraticWork"] = (
 "The old limits were not arbitrary; the book explains that they protect the node from work that grows with the square of the limit. If a child pays for 25 ancestors and each of the ancestors has 25 other children, then including the package in a block requires updating about 625 packages, and doubling the parameter from 25 to 50 would quadruple the work (Antonopoulos and Harding, 2023). "
 "The chapter's arithmetic gives 25 x 25 = 625, 50 x 50 = 2,500 and the factor 4. It is like a handshake round in a room: with twice the people there are four times as many pairs to greet. "
 "The same reasoning drives the cluster mempool, whose limit of 64 transactions per cluster is set so that the ordering work of a cluster stays small (Daftuar et al., 2024). "
 "The lesson for a designer is that every limit in a peer-to-peer system is a trade between the freedom of the users and the work that an attacker can make the nodes do.")

C["TrucLimits"] = (
 "Topologically restricted until confirmation (TRUC) transactions, also called version 3 transactions, are an opt-in set of rules from BIP 431: a version-3 transaction may have at most one unconfirmed parent and one unconfirmed child, may be at most 10,000 virtual bytes, and its child at most 1,000 (Zhao, 2024). "
 "A version-3 transaction also signals replaceability even without the BIP 125 signal, and the unconfirmed relatives of a version-3 transaction must all be version 3 (Zhao, 2024). The aim is that a replacement can never be made very expensive by a large attached child. It is like a parking space that can hold one car and one trailer of limited size. "
 "The source constants of release 31.1 are TRUC_VERSION 3, TRUC_ANCESTOR_LIMIT 2, TRUC_MAX_VSIZE 10000 and TRUC_CHILD_MAX_VSIZE 1000 (Bitcoin Core, 2026), where the limit of two counts the transaction itself and one relative. "
 "In the run a version-3 parent had a child of 141 virtual bytes, which was accepted, and a child of 1,350 virtual bytes, which was refused with the message TRUC-violation, version=3 child tx; release 28.0 introduced the policy (Bitcoin Core developers, 2024).")

C["TrucSiblingEviction"] = (
 "Because a version-3 parent may have only one unconfirmed child, a second child that arrives could be blocked by the first one, so the rule lets the second child replace the first, called sibling eviction, if it pays more: the replacement must pay a higher fee than the sibling it evicts (Zhao, 2024). "
 "It is like a single seat that goes to the highest bidder, though not to a bidder who only matches the first. "
 "In the run the first child was accepted; a second child of the same parent at the same fee rate was refused with the message insufficient fee including sibling eviction, and a second child at a higher fee rate was accepted and the first child left the mempool. "
 "For Lightning this means that one party cannot permanently occupy the single place beside the commitment transaction with a cheap child, which is the pinning that the carve-out tried to prevent (Bitcoin Core, 2026).")

C["TrucVersionMixing"] = (
 "The rules of version 3 bind both sides: a version-3 transaction can only spend unconfirmed outputs of other version-3 transactions, and any other transaction can only spend an unconfirmed output of a version-3 parent if it is itself of version 3 (Zhao, 2024). "
 "It is like a club in which a member may only bring a guest who has signed the same rules. "
 "In the run a version-2 transaction that spent an unconfirmed output of a version-3 parent was refused with the message TRUC-violation, non-version=3 tx followed by its identifier, so a parent that opts in to the restrictions cannot be pinned by a child that did not. "
 "The restriction lasts only until confirmation, which is the origin of the name, and after that the output can be spent by anyone with any version (Zhao, 2024) (Bitcoin Core, 2026).")

C["TrucPinningBound"] = (
 "Pinning by a large child is bounded under the TRUC rules because the child cannot be larger than 1,000 virtual bytes, so the extra fee that a replacement must pay is bounded too; BIP 431 says that restricting children to 1000 virtual bytes lowers the upper bound of the added fees by a factor of 100 compared with a child of 100,000 (Zhao, 2024). "
 "The run repeated the pin of the earlier leaf with a version-3 parent of 141 virtual bytes that paid 705 satoshis and a child of 885 virtual bytes that paid 4,425 satoshis; the replacement that the node accepted had to pay 5,145 satoshis, against the 450,780 satoshis of the version-2 case, about 88 times less. "
 "It is like a lorry replaced by a small trailer in the example of the parked car. "
 "The numbers are a single run with one child size, and the bound of the specification is a factor of 100 in general (Bitcoin Optech, 2026).")

C["PayToAnchor"] = (
 "A pay-to-anchor (P2A) output is a small output with a standard script that anyone can spend: it is a segregated witness output of version 1 with the two-byte program 0x4e73, so the script is 51024e73, and it needs no signature, which makes it a handle for a child transaction to fee bump a parent (Sanders, 2025). "
 "It is like a hook on a wall that anyone can hang a rope on. The chapter parsed the zero-fee parent of the run and found its first output with exactly this script and the value 0; the address of such an output on the test chain is bcrt1pfeesnyr2tx, and the node refused a P2A output of 239 satoshis as dust and accepted one of 240. "
 "BIP 433, the specification, defines the type as an output with the script OP_1 followed by the push of 4e73 (Sanders, 2025). "
 "BOLT 3 lists a shared anchor output for commitments without fees, and the output needs no key, so it can be created long before it is spent (Lightning developers, 2026) (Bitcoin Optech, 2026).")

C["EphemeralDust"] = (
 "Ephemeral dust is the rule that makes a zero-fee anchor possible. Dust outputs are normally not relayed; release 29.0 allows one dust output in a transaction provided that the transaction pays no fee, and requires that any spender of its other outputs also spends the dust, so that the dust cannot stay in the set of unspent outputs (Bitcoin Core developers, 2025). "
 "It is like a free sample that must be taken away by whoever buys anything else from the stand. In the run the zero-fee version-3 parent had an anchor output of value 0: alone it was refused with min relay fee not met, 0 < 13, together with its child it was accepted, and after mining the mempool was empty, so the dust was spent in the same block. "
 "The source file of the policy explains the safety conditions of its functions, and Optech's page on ephemeral anchors shows the history (Bitcoin Core, 2026) (Bitcoin Optech, 2026). "
 "The book mentions ephemeral anchors as a proposal that is being developed (Antonopoulos and Harding, 2023).")

C["AnchorSpend"] = (
 "Spending the anchor shows why the construction fits a time-sensitive contract: the child has two inputs, one for the money that pays the fee and one for the anchor; the anchor input has an empty witness, because the output needs no signature, and the child paid 10,000 satoshis from a 1-bitcoin input. "
 "The chapter parsed the child's raw bytes and found two inputs and exactly one with an empty witness stack. "
 "Whoever sees the parent, the counterparty or a third party, can attach a child like this, and that is the strength of the anchor and also the reason for the careful limits, because an anyone-can-spend handle invites competition (Sanders, 2025). "
 "It is like a tow rope on a car that any helper may take, with the rule that only one rope may be attached. The version-3 rules of the previous leaves make sure that only one child can occupy the place of the anchor spend (Zhao, 2024).")

C["LightningAnchorOutputs"] = (
 "The Lightning Network keeps payments between two parties in channels, whose commitment transactions are signed in advance and may be broadcast at an unknown time; the book says that most popular implementations use a template called anchor outputs, designed to be used with the carve-out (Antonopoulos and Harding, 2023). "
 "In the specification of the commitment transaction, BOLT 3, the anchor output of each party is fixed at 330 satoshis, the default dust limit for P2WSH, and after 16 blocks anyone can sweep it, so that the outputs do not stay for ever in the set of unspent outputs (Lightning developers, 2026). "
 "It is like a small deposit on a trolley that is returned when someone takes it back. Optech's page records that later designs came to depend on the carve-out to circumvent pinning and that the newest designs differ (Bitcoin Optech, 2026). "
 "The specification also lists the dust limit of 240 satoshis for the pay-to-anchor type, and the chapter found these passages in the saved copies; the protocol itself was not run.")
