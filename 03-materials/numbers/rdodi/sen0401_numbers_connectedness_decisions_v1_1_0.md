# SEN0401 numbers - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.0 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.0) | 23 | 0 | 3 |
| after (1.1.0) | 23 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 23 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:plotsPrice | plots the price of | PriceVsHashRate | MarketPrice | the chapter says of Price vs hash rate: 'A scatter of price against hash rate'; the chapter says of Market price: 'The average US-dollar price across major exchanges'. |
| chx:plotsHashRate | plots the hash rate of | PriceVsHashRate | AnnualHashRate | the chapter says of Price vs hash rate: 'A scatter of price against hash rate'; the chapter says of Annual hash rate: 'The hash rate averaged over each year'. |
| chx:marksHalvingOn | marks the halving of | MarketPrice | HalvingEra | the chapter says of Market price: 'halvings are marked on the chart'; the chapter says of Halving era: 'The subsidy halves every 210,000 blocks'. |
| chx:dropsAtHalving | drops at each halving of | AnnualIssuance | HalvingEra | the chapter says of Annual issuance: 'dropping in steps at each halving'; the chapter says of Halving era: 'The subsidy halves every 210,000 blocks'. |
| chx:estimatesHashRate | estimates | HashRateEstimate | NetworkHashRate | the chapter says of Hash-rate estimate: 'it is estimated from mining difficulty and block times'; the chapter says of Network hash rate: 'The estimated number of hashes the whole network computes per second'. |
| chx:snapshotsPrice | snapshots the price of | BlockchainComSnapshot | MarketPrice | the chapter says of Blockchain.com snapshot: 'Blockchain.com charts API - Market Price (USD)'; the chapter says of Market price: 'The average US-dollar price across major exchanges'. |
| chx:snapshotsHashRate | snapshots the hash rate of | BlockchainComSnapshot | NetworkHashRate | the chapter says of Blockchain.com snapshot: 'Blockchain.com charts API - Hash Rate'; the chapter says of Network hash rate: 'The estimated number of hashes the whole network computes per second'. |
| chx:snapshotsCirculation | snapshots the circulation of | BlockchainComSnapshot | CirculatingSupply | the chapter says of Blockchain.com snapshot: 'Blockchain.com charts API - Bitcoins in circulation'; the chapter says of Circulating supply: 'The number of bitcoins issued so far'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
