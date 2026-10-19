# SEN0401 ch01 - connectedness and link decisions for the domain T-Box 1.3.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.2.0 is untouched; 1.3.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.2.0) | 117 | 0 | 5 |
| after (1.3.0) | 117 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 117 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:canBeReadBy | can be read by | Invoice | Wallet | the chapter defines Invoice as 'a payment request that a wallet can read'. |
| chx:isDerivedFromKey | is derived from | BitcoinAddress | PrivateKey | the chapter defines Bitcoin address as 'a number derived from the private key that others use to pay you'. |
| chx:holdsKeys | holds the keys as | KeyControl | PrivateKey | the chapter defines Custodial wallet ('a third party, the custodian, holds the keys') and Noncustodial wallet ('only the user holds the keys'). |
| chx:generatesKeys | generates keys | RecoveryCode | PrivateKey | the chapter defines Recovery code as one 'from which all its keys are generated and from which the wallet can be restored'. |
| chx:carriesChecksum | carries a checksum | RecoveryCode | Checksum | the chapter defines Checksum with 'a BIP 39 recovery code carries ENT/32 bits taken from a SHA-256 hash'. |
| chx:specifiesRecoveryCode | specifies the recovery code | BitcoinImprovementProposal | RecoveryCode | the chapter defines BIP with 'BIP 39 describes the mnemonic code behind recovery codes'. |
| chx:specifiesUriScheme | specifies the URI scheme | BitcoinImprovementProposal | Uri | the chapter defines URI with 'the bitcoin: scheme of BIP 21 writes an address, an amount and a label as a URI'. |
| chx:includesWallet | includes a wallet | ReferenceImplementation | Wallet | the chapter defines Reference implementation: 'Bitcoin Core is its descendant and includes a wallet'. |
| chx:isPeerIn | is a peer in | FullNode | PeerToPeerProtocol | the chapter defines Peer-to-peer protocol: 'a decentralized peer-to-peer network in which every full node is a peer'. |
| chx:isRecordedIn | is recorded in | Transaction | Blockchain | the chapter defines Transaction: 'broadcast over the network, collected into a block, and made permanent on the blockchain'. |
| chx:recordsTransactions | records transactions | PublicJournal | Transaction | the chapter defines Public journal: 'a public transaction journal, the blockchain, in which every confirmed transaction is recorded'. |
| chx:isSignedWith | is signed with | Transaction | DigitalSignature | the chapter defines Transaction as 'a signed data structure' and Digital signature as 'computed from data and a private key'. |
| chx:earnedByMining | is earned by | TransactionFee | Mining | the chapter defines Transaction fee as 'the amount a sender adds for the miner who includes the transaction in a block'. |
| chx:earnsSubsidy | earns the subsidy | Mining | BlockSubsidy | the chapter defines Mining ('add a block and earn the reward') and Block subsidy ('new bitcoin that a block may create for its miner'). |
| chx:takesOverFunctionsOf | takes over the functions of | Mining | CentralBank | the chapter defines Central bank replacement: 'Mining decentralizes the currency-issuance and clearing functions of a central bank'. |
| chx:setsPriceThrough | sets the price through | CurrencyExchange | FloatingExchangeRate | the chapter defines Currency exchange ('a market where buyers and sellers swap bitcoin and local currency') and Floating exchange rate ('set by markets'). |
| chx:solvesProblem | is a practical solution to | ProofOfWork | ByzantineGeneralsProblem | the chapter defines Byzantine Generals' Problem: 'Bitcoin's proof of work is a practical solution'. |
| chx:descendsFrom | descends from | ProofOfWork | Hashcash | the chapter defines Hashcash: 'Bitcoin's proof of work descends from it'. |
| chx:preventsDoubleSpend | prevents | Consensus | DoubleSpend | the chapter defines Double-spend: 'Bitcoin's consensus prevents it without a central clearinghouse'. |
| chx:isAuthoredBy | is authored by | Whitepaper | SatoshiNakamoto | the chapter defines Whitepaper as 'the 2008 paper by Satoshi Nakamoto'. |
| chx:wasPublishedBy | was published by | ReferenceImplementation | SatoshiNakamoto | the chapter defines Reference implementation: 'the software that Nakamoto published in 2009'. |
| chx:reliesOn | relies on | LightweightClient | FullNode | the chapter defines Lightweight client: 'relies on a full node or server for most data and validates only partly'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
| SYN-1 X_LightweightClient -> X_FullNode (A-Box individuals) | medium | class-level relation set; individual link not set | The text is right (a lightweight client relies on a full node), so chx:reliesOn links the two classes in the T-Box; the A-Box is outside this repair and is not changed. |
| SYN-1 X_LightweightClient -> X_FullNode | medium | rejected | The text is right and the relation is set where the model can carry it: chx:reliesOn links the classes Lightweight client and Full node in this T-Box. An individual-level link would change the A-Box, which this repair does not touch. |

The rejected rows are the ledger sen0401_ch01_link_decisions_v1_3_0.tsv, in the format of LINK_DECISIONS_v*.tsv.
