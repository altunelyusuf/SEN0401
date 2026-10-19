from spec_common import *
PROPS = [
 P("plotsPrice", "plots the price of", "PriceVsHashRate", "MarketPrice", "The scatter puts price against hash rate", ("Price vs hash rate", "A scatter of price against hash rate"), ("Market price", "The average US-dollar price across major exchanges")),
 P("plotsHashRate", "plots the hash rate of", "PriceVsHashRate", "AnnualHashRate", "The scatter puts price against hash rate", ("Price vs hash rate", "A scatter of price against hash rate"), ("Annual hash rate", "The hash rate averaged over each year")),
 P("marksHalvingOn", "marks the halving of", "MarketPrice", "HalvingEra", "Halvings are marked on the price chart", ("Market price", "halvings are marked on the chart"), ("Halving era", "The subsidy halves every 210,000 blocks")),
 P("dropsAtHalving", "drops at each halving of", "AnnualIssuance", "HalvingEra", "Annual issuance drops in steps at each halving", ("Annual issuance", "dropping in steps at each halving"), ("Halving era", "The subsidy halves every 210,000 blocks")),
 P("estimatesHashRate", "estimates", "HashRateEstimate", "NetworkHashRate", "The hash rate is estimated from difficulty and block times", ("Hash-rate estimate", "it is estimated from mining difficulty and block times"), ("Network hash rate", "The estimated number of hashes the whole network computes per second")),
 P("snapshotsPrice", "snapshots the price of", "BlockchainComSnapshot", "MarketPrice", "The snapshot holds the Blockchain.com chart Market Price (USD)", ("Blockchain.com snapshot", "Blockchain.com charts API - Market Price (USD)"), ("Market price", "The average US-dollar price across major exchanges")),
 P("snapshotsHashRate", "snapshots the hash rate of", "BlockchainComSnapshot", "NetworkHashRate", "The snapshot holds the Blockchain.com chart Hash Rate", ("Blockchain.com snapshot", "Blockchain.com charts API - Hash Rate"), ("Network hash rate", "The estimated number of hashes the whole network computes per second")),
 P("snapshotsCirculation", "snapshots the circulation of", "BlockchainComSnapshot", "CirculatingSupply", "The snapshot holds the Blockchain.com chart Bitcoins in circulation", ("Blockchain.com snapshot", "Blockchain.com charts API - Bitcoins in circulation"), ("Circulating supply", "The number of bitcoins issued so far")),
]
REJECT = {}
