"""The key concepts of chapter 9 for the deck 2.0.0: the 36 distinct primary-source concepts of the chapter research (03-materials/ch09/rdodi/sen0401_ch09_research_v1_0_1.ttl, de-duplicated by
normalised label as the deck standard check does), each with the part of the chapter it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line meaning and
analogy of every part (level 1) and group (level 2) that the dividers show. A card reads: the concept, its meaning, then 'Think of ...'. Five labels of the research are second spellings of a
concept that has a card (CPFP and RBF written the other way round, 'estimating fee rates', 'carve outs (CPFP)', 'anchor outputs (CPFP)'): they stand on the card of that concept as 'Also written'.
NEW file; nothing earlier is edited."""
__version__ = "2.0.0"

# level 1: divider subtitle (carries the meaning and the analogy of the part)
L1 = {
    "WhoPaysTheFee": "The spender pays the fee, like a tip left on the counter.",
    "FeesAndFeeRates": "A fee is a bill, and the rate is its price per unit of space.",
    "FeeEstimation": "Estimating a fee is guessing the fare from past journeys.",
    "ReplaceByFee": "Replacing a payment is raising your bid at an auction.",
    "ChildPaysForParent": "A child pays for its parent, like a friend who covers your fare.",
    "PinningAndAnchors": "Pinning is a lorry parked behind your car; an anchor is a spare handle.",
    "FeeSnipingAndIncentives": "Fee sniping is a thief rewriting the last page of the ledger.",
}

# level 2: (pill, meaning, analogy)   pill at most 4 words
L2 = {
    "FeeAsDifference": ("Fee as difference", "The fee is inputs minus outputs; no field holds it.", "the change you forget to take back from the counter"),
    "SpenderAndSignature": ("Spender and signature", "Only the spender can add to the fee, since the signature covers the amounts.", "a cheque that cannot be altered after it is signed"),
    "MinerChoice": ("Miner choice", "Miners choose what goes into a block and prefer the highest rates.", "a bus driver who boards the highest bidders first"),
    "SizeAndWeight": ("Size and weight", "Virtual size is the space a payment takes in a block.", "postage priced by the volume of the parcel"),
    "FeeRateArithmetic": ("Fee rate arithmetic", "A rate is the fee over the virtual size, in satoshis per byte.", "the price per kilo on a market scale"),
    "MinimumRates": ("Minimum rates", "Nodes, wallets and dust rules each set a floor.", "a minimum fare below which no taxi starts the meter"),
    "EstimatorMechanics": ("Estimator mechanics", "The estimator reads recent blocks to answer for a target.", "a driver who recalls the usual fare for each hour"),
    "FeeMarketOnMainnet": ("Fee market", "Two real blocks show how far fee rates can move.", "seat prices at the rush hour and at midnight"),
    "ReplaceableSignal": ("Replaceable signal", "A sequence number says whether replacement is welcome.", "a sticker that says this seat may be swapped"),
    "ReplacementRules": ("Replacement rules", "A new copy must pay more than the old one, by a step.", "an auction bid that must beat the last one by a step"),
    "ReplacementHazards": ("Replacement hazards", "Replacements can pay a payee twice or be cycled to cause harm.", "a cheque cashed twice because two copies exist"),
    "PackagesAndMining": ("Packages and mining", "Miners price a parent and its child together.", "a shopper who buys the bundle with the best price per item"),
    "PackageRelay": ("Package relay", "Nodes accept a pair that a single payment could not be.", "a gate that admits a pair who pay the entry together"),
    "ClusterMempool": ("Cluster mempool", "Connected payments are grouped and ordered as one cluster.", "a timetable that sorts linked carriages together"),
    "CarveOut": ("Carve out", "One extra small child was allowed beyond the usual limits.", "a lane kept free for the ambulance"),
    "TrucPolicy": ("TRUC policy", "Version 3 payments get strict limits that bound pinning.", "a parking bay with a size limit for the car behind"),
    "AnchorOutputs": ("Anchor outputs", "A small output lets any party add a fee later.", "a spare handle on a door"),
    "BlockRewardMix": ("Block reward mix", "A block pays a subsidy and the fees of its payments.", "a wage plus tips whose mix changes over the years"),
    "SnipingAttack": ("Sniping attack", "A miner may re-mine a block to take its best fees.", "a clerk who rewrites yesterday's entries to keep the big ones"),
    "LockTimeDefense": ("Lock time defense", "Wallets lock a payment to the next block height.", "dating a cheque so that it cannot be moved back"),
}

# key concepts: label as in the research -> (part, meaning, analogy); an "Also written" label of the research is appended to the meaning
K3 = {
    "Who Pays the Transaction Fee?": ("WhoPaysTheFee", "The spender, by leaving part of the inputs unclaimed by the outputs.", "the tip you leave on the table when you pay the bill"),
    "transaction fees": ("WhoPaysTheFee", "What a miner may claim for putting a payment into a block.", "the postage that gets a letter carried"),
    "Adding Fees to Transactions": ("WhoPaysTheFee", "A wallet chooses inputs and a fee rate, and leaves the difference.", "a diner who writes a tip on the card slip"),
    "fees": ("WhoPaysTheFee", "The coins that inputs hold and outputs do not claim.", "the gap between the price on the tag and the note you handed over"),
    "inputs": ("WhoPaysTheFee", "Earlier outputs that a payment spends, each one entirely.", "banknotes from your wallet, handed over whole"),
    "outputs": ("WhoPaysTheFee", "The new amounts, each with the lock that says who may spend it next.", "the sealed envelopes you fill for each recipient"),
    "change output": ("WhoPaysTheFee", "An output that sends the rest of an input back to the spender.", "the coins a cashier hands back to you"),
    "payments": ("WhoPaysTheFee", "Value moving from one holder to another, as a person sees it.", "passing a note across a table to a friend"),
    "transactions": ("WhoPaysTheFee", "The signed records that spend inputs and create outputs.", "a cheque that lists the notes it uses and who gets what"),
    "overpaying transaction fees": ("WhoPaysTheFee", "A fee far above what the market needs, wasted on the miner.", "paying for express delivery on an empty street"),
    "excessive fees": ("WhoPaysTheFee", "A fee so high that a node refuses it unless told otherwise.", "a till that rejects a price with a zero too many"),
    "absurd fees": ("WhoPaysTheFee", "A fee above the safety limit, usually a forgotten change output.", "a bank that asks twice before wiring a million"),
    "Fees and Fee Rates": ("FeesAndFeeRates", "A fee is a sum in satoshis; a rate divides it by size.", "a freight bill: the total, and the price per cubic metre"),
    "fee rates": ("FeesAndFeeRates", "The price per virtual byte by which miners sort payments.", "the price per kilo at a market stall"),
    "blocks": ("FeesAndFeeRates", "Batches of payments, limited to four million units of weight.", "a bus that leaves every ten minutes with fixed seats"),
    "Estimating Appropriate Fee Rates": ("FeeEstimation", "The node learns from past blocks which rate confirmed within a target. Also written: estimating fee rates.", "a taxi driver who knows the usual fare for each hour"),
    "Bitcoin Core": ("FeeEstimation", "The reference node software whose rules and estimator the chapter measures.", "the reference clock by which other clocks are set"),
    "Replace By Fee (RBF) Fee Bumping": ("ReplaceByFee", "Send a conflicting copy that pays more, so miners prefer it. Also written: RBF (replace by fee) fee bumping.", "raising your bid at an auction by at least one step"),
    "BIP 125 opt-in replaceability signal": ("ReplaceByFee", "An input sequence below 0xfffffffe marks a payment as replaceable.", "a sticker that says this seat may be swapped"),
    "conflicting transactions": ("ReplaceByFee", "Two payments that spend the same output; only one can be mined.", "two cheques written against the same banknote"),
    "fee bumping": ("ReplaceByFee", "Raising the fee of a waiting payment, by replacement or by a child.", "adding stamps to a letter that is stuck in the post"),
    "Child Pays for Parent (CPFP) Fee Bumping": ("ChildPaysForParent", "A child spends the parent's output and pays enough for both. Also written: CPFP (child pays for parent) fee bumping.", "a friend who pays your fare together with his own"),
    "Package Relay": ("ChildPaysForParent", "Nodes judge a parent and its child together, not one by one.", "a gate that admits a pair when the pair pays the entry"),
    "package fee rate": ("ChildPaysForParent", "The pair's total fee over its total virtual size.", "the price per kilo of a parcel and its box together"),
    "ancestor fee rate mining": ("ChildPaysForParent", "Miners pick a payment with the ancestors it needs, by their joint rate.", "a shopper who buys the bundle because it is cheapest per item"),
    "Transaction Pinning": ("PinningAndAnchors", "A cheap parent made hard to replace by a big or crowded family.", "a lorry parked behind your car: the bigger it is, the dearer to move"),
    "CPFP Carve Out and Anchor Outputs": ("PinningAndAnchors", "Rules and outputs that keep a child possible when the fee is unknown in advance. Also written: carve outs (CPFP), anchor outputs (CPFP).", "a spare door handle that anyone can grab to add the fee later"),
    "Timelock Defense Against Fee Sniping": ("FeeSnipingAndIncentives", "A wallet sets the lock time to the current height, so a rewritten block cannot take the payment.", "a ledger line dated today that cannot be moved to an older page"),
    "fee sniping": ("FeeSnipingAndIncentives", "A miner re-mines a block to take the payments with the best fees.", "a clerk who rewrites yesterday's entries to keep the big ones"),
    "timelocks": ("FeeSnipingAndIncentives", "Rules that make a payment valid only after a time or a height.", "a post-dated cheque"),
    "lock time": ("FeeSnipingAndIncentives", "The field of a transaction that holds that height or time.", "the date written on a post-dated cheque"),
}
