"""SEN0401 supplement "Bitcoin in numbers": the owner's dashboard (a claude.ai artifact built on 25 September 2026
from Blockchain.com's public charts) turned into an RDODI unit, so it gets the chapter pages' interaction.
Every figure stated below was computed from the dashboard's own snapshot under Python 3.14.4, and the snapshot
was spot-checked against the Blockchain.com API on 2026-09-25 (market price and hash rate matched exactly at
shared dates)."""
__version__ = "1.0.1"
CH = "numbers"
UNIT_LABEL = "Bitcoin in numbers"
SOURCE_OF = "the Bitcoin: price, supply and mining power dashboard (v1.1.0) and its Blockchain.com data"
DOC_INTRO = "This document turns the Bitcoin price, supply and mining power dashboard into SEN0401 course material, grounded in its Blockchain.com snapshot and in Mastering Bitcoin's 3rd edition (Blockchain.com, 2026)."
VERSION = "1_0_0"
TITLE = "Bitcoin in numbers: price, supply and mining power since 2009"
QUESTION = "What do Bitcoin's price, supply and mining-power histories show, which of the dashboard's statements can be recomputed from its own data, and how do they connect to chapters 1 and 2?"
LABELS = {"YearOnYearChange": "Year-on-year change", "MinedVsRemaining": "Mined vs still to mine", "PriceVsHashRate": "Price vs hash rate", "HashRateEstimate": "Hash-rate estimate", "BlockchainComSnapshot": "Blockchain.com snapshot"}
PUBS = [
 ("P01","Bitcoin: price, supply and mining power v1.1.0 - interactive dashboard, claude.ai artifact built 25 September 2026 (owner's)","https://claude.ai/artifact/YW85r4NW1APUyQGMw8CtL2",True),
 ("P02","Blockchain.com charts API - Market Price (USD)","https://api.blockchain.info/charts/market-price",False),
 ("P03","Blockchain.com charts API - Bitcoins in circulation","https://api.blockchain.info/charts/total-bitcoins",False),
 ("P04","Blockchain.com charts API - Hash Rate","https://api.blockchain.info/charts/hash-rate",False),
 ("P05","Controlled supply - Bitcoin Wiki","https://en.bitcoin.it/wiki/Controlled_supply",False),
 ("P06","Mastering Bitcoin, 3rd edition - Chapter 12, Mining and Consensus (Antonopoulos and Harding, 2023)","https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch12_mining.adoc",False),
]
CONCEPTS = [("Section",x) for x in ("Price","Market price, USD","Yearly trading range","Year-on-year change","Minted coins","Circulating supply","Mined vs still to mine","New coins minted per year","Mining capacity","Network hash rate, EH/s","Average hash rate by year","Price vs hash rate")]
FINDINGS = [
 ("F1","Background","The dashboard shows seventeen years of Bitcoin in three parts - price, minted coins and mining capacity - drawn from Blockchain.com's public charts and sampled about every four days, as a snapshot rather than a live feed.",["P01"]),
 ("F2","Verification","The snapshot was spot-checked against the Blockchain.com API on 2026-09-25: the market price and the hash rate match exactly at shared dates, for example 78521.7 dollars on 2026-08-26 and 825.5 EH/s on 2026-08-28.",["P02","P04"]),
 ("F3","Comparative analysis","The dashboard's statements recompute from its own data: 20,087,925 bitcoins in circulation is 95.66 per cent of the 21 million cap; yearly average hash rate grew from 4.358e-12 EH/s in 2009 to 952.8 EH/s in 2026, a factor of about 2.19e14, matching its 'about 200 trillion times'; and the fourth halving on 2024-04-20 set the subsidy at 3.125 bitcoin, as the Bitcoin Wiki records.",["P01","P03","P05"]),
 ("F4","Conclusion","For the course, the dashboard makes chapters 1 and 2 visible: the supply schedule and halvings of chapter 1 as a stepped curve and shrinking yearly issuance, and chapter 2's security by computation as a hash rate spanning fourteen orders of magnitude.",["P01","P06"]),
]
TAX = [
 ("Price","PriceHistory","MarketPrice","the average USD price across exchanges","The average US-dollar price across major exchanges, sampled about every four days; halvings are marked on the chart.",None),
 ("Price","PriceHistory","YearlyTradingRange","each year's low, high and close","Floating bars from each year's lowest to highest price, with the closing price marked.",None),
 ("Price","PriceChange","YearOnYearChange","close against previous close","Each year's closing price compared with the previous year's close.",None),
 ("Supply","Circulation","CirculatingSupply","bitcoins in circulation","The number of bitcoins issued so far, growing in steps toward the 21 million cap.",None),
 ("Supply","Circulation","MinedVsRemaining","share of the cap already issued","The issued share of the 21 million cap against what remains to be mined.",("round(20087925 / 21e6 * 100, 2)","95.66")),
 ("Supply","Issuance","AnnualIssuance","new coins minted per year","Bitcoins minted each year, dropping in steps at each halving.",None),
 ("Supply","Issuance","HalvingEra","the fourth block-reward era","The subsidy halves every 210,000 blocks; the fourth halving, on 2024-04-20, set it at 3.125 bitcoin.",("(50 * 10**8 >> 4) / 10**8","3.125")),
 ("Mining","HashPower","NetworkHashRate","hashes per second securing the chain","The estimated number of hashes the whole network computes per second, in exahashes (10^18) per second.",None),
 ("Mining","HashPower","AnnualHashRate","yearly average hash rate","The hash rate averaged over each year, on a logarithmic axis because it spans about fourteen orders of magnitude.",("f'{952.8 / 4.358e-12:.3g}'","'2.19e+14'")),
 ("Mining","Relationship","PriceVsHashRate","price against hash rate over time","A scatter of price against hash rate, both on logarithmic scales, coloured from early to recent.",None),
 ("Provenance","DataSource","BlockchainComSnapshot","the data behind every chart","A snapshot of Blockchain.com's public charts taken when the page was built - not a live feed.",None),
 ("Provenance","DataSource","HashRateEstimate","hash rate inferred, not measured","The hash rate cannot be observed directly; it is estimated from mining difficulty and block times.",None),
]
CHARTS = {"MarketPrice": "cPrice", "YearlyTradingRange": "cRange", "YearOnYearChange": "cYoy", "CirculatingSupply": "cSupply", "MinedVsRemaining": "cDonut", "AnnualIssuance": "cMint", "NetworkHashRate": "cHash", "AnnualHashRate": "cHashYear", "PriceVsHashRate": "cScatter"}
B = "Blockchain.com, 2026"; W = "Bitcoin Wiki, 2026"; M = "Antonopoulos and Harding, 2023"
BODY = {
 "Price": "The first part of the dashboard follows the market price, where boom-and-bust cycles dominate the history (%s)." % B,
 "PriceHistory": "The price history is shown two ways: the full series, and each year's range (%s)." % B,
 "MarketPrice": "The chart Market price, USD shows the market price: the average US-dollar price across major exchanges; a logarithmic scale shows the whole history and a linear scale shows recent dollar swings, and the price at its last sample was 86,184.81 dollars (%s)." % B,
 "YearlyTradingRange": "In the Yearly trading range chart each year appears as a floating bar from its low to its high with the closing price marked, so a volatile year is a tall bar (%s)." % B,
 "PriceChange": "Change is easier to compare than level when prices span six orders of magnitude (%s)." % B,
 "YearOnYearChange": "The Year-on-year change chart compares each close with the previous close; bars beyond plus 400 per cent are cut off and labelled (%s)." % B,
 "Supply": "The second part, Minted coins, shows the coins issued against the 21 million cap that chapter 1 describes (%s)." % M,
 "Circulation": "Circulation is the running total of every block subsidy paid so far (%s)." % B,
 "CirculatingSupply": "The Circulating supply chart grows in steps toward the 21 million ceiling, each step flatter than the last (%s)." % B,
 "MinedVsRemaining": "Mined vs still to mine puts it plainly: at the snapshot, 20,087,925 bitcoins had been issued - 95.66 per cent of the 21 million cap - leaving less than a twentieth to be mined over more than a century (%s)." % B,
 "Issuance": "Yearly issuance falls in steps because the block subsidy halves every 210,000 blocks (%s)." % W,
 "AnnualIssuance": "The chart New coins minted per year drops sharply after each halving, from over three million in 2010 to about 165,000 in 2025 (%s)." % B,
 "HalvingEra": "The subsidy started at 50 bitcoin and halves every 210,000 blocks; the fourth halving, on 2024-04-20, set it at 3.125 bitcoin (%s)." % W,
 "Mining": "The third part, Mining capacity, shows the computing power securing the chain, which is chapter 2's security by computation made visible (%s)." % M,
 "HashPower": "Hash power is the total rate of guesses miners make in the proof-of-work search (%s)." % M,
 "NetworkHashRate": "The chart Network hash rate, EH/s plots the estimate in exahashes per second - a billion billion hashes each second - on a logarithmic scale (%s)." % B,
 "AnnualHashRate": "Average hash rate by year shows it rising from about 4.358e-12 EH/s in 2009 to 952.8 EH/s in 2026, a factor of about 2.19e14 - the dashboard's 'about 200 trillion times' (%s)." % B,
 "Relationship": "Setting price against hash rate asks whether security followed value (%s)." % B,
 "PriceVsHashRate": "The Price vs hash rate scatter puts price against hash rate on logarithmic scales, coloured from early to recent, so the joint rise of both shows as a path to the upper right (%s)." % B,
 "Provenance": "Every chart rests on one data source, and its limits belong on the page (%s)." % B,
 "DataSource": "The dashboard states where its numbers come from and how current they are (%s)." % B,
 "BlockchainComSnapshot": "The data are a snapshot of Blockchain.com's public charts, sampled about every four days and taken when the page was built - so the numbers change only when the page is rebuilt (%s)." % B,
 "HashRateEstimate": "Hash rate is an estimate derived from difficulty and block times, because no one can count every miner's hashes directly (%s)." % B,
}
