# SEN0401 ch06 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.0 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.0) | 115 | 0 | 7 |
| after (1.1.0) | 115 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 115 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:separatesFromTxid | separates the witness from | Segwit | Txid | the chapter says of Segregated witness: 'Segregated witness is the separation of a transaction's witness from the data its txid is computed over'. |
| chx:emptiesInputScript | leaves empty | Segwit | InputScript | the chapter says of Segregated witness: 'an empty input script keeps witnesses from affecting the txid'. |
| chx:changesTxid | changes the txid of | ThirdPartyMalleability | Txid | the chapter says of Third-party transaction malleability: 'a stranger's ability to change a transaction's txid without invalidating it'. |
| chx:dependsOnTxid | arises from the dependence of | CircularDependency | Txid | the chapter says of Circular dependency: 'in the legacy format the deposit's txid depends on its signatures'. |
| chx:isDataInOutputScript | is the data in | WitnessProgram | OutputScript | the chapter says of Witness program: 'A witness program is the data in a segwit output script'. |
| chx:includesPaymentChannel | includes | ContractProtocol | PaymentChannel | the chapter says of Contract protocols: 'the payment channel is one'. |
| chx:computedOverLegacyFormat | is computed over | Txid | LegacyFormat | the chapter says of Transaction identifier: 'double SHA-256 of a transaction's legacy serialization'. |
| chx:computedOverExtendedFormat | is computed over | Wtxid | ExtendedFormat | the chapter says of Witness transaction identifier: 'double SHA-256 of the whole extended serialization, witness included'. |
| chx:weighsLegacyFormat | counts the size of | Weight | LegacyFormat | the chapter says of Weight: 'the legacy serialization's size times 3 plus the full serialization's size'. |
| chx:addsMarker | adds | ExtendedFormat | MarkerByte | the chapter says of Extended serialization format: 'adds a marker byte, a flag byte and a witness structure to the legacy layout'. |
| chx:addsFlag | adds | ExtendedFormat | FlagByte | the chapter says of Extended serialization format: 'adds a marker byte, a flag byte and a witness structure to the legacy layout'. |
| chx:addsWitnessStructure | adds | ExtendedFormat | WitnessStructure | the chapter says of Extended serialization format: 'adds a marker byte, a flag byte and a witness structure to the legacy layout'. |
| chx:hasVersionField | has | TransactionParts | VersionField | the chapter says of The parts of a transaction: 'A serialized transaction has a version, an inputs field, an outputs field, a lock time'. |
| chx:hasInputList | has | TransactionParts | InputList | the chapter says of The parts of a transaction: 'A serialized transaction has a version, an inputs field, an outputs field, a lock time'. |
| chx:hasOutputList | has | TransactionParts | OutputList | the chapter says of The parts of a transaction: 'A serialized transaction has a version, an inputs field, an outputs field, a lock time'. |
| chx:hasLockTime | has | TransactionParts | LockTimeField | the chapter says of The parts of a transaction: 'A serialized transaction has a version, an inputs field, an outputs field, a lock time'. |
| chx:hasWitnessStructure | has, when it spends segwit outputs, | TransactionParts | WitnessStructure | the chapter says of The parts of a transaction: 'when it spends segwit outputs, a marker, a flag and a witness structure'. |
| chx:identifiesTransactionByTxid | identifies the transaction by | PreviousTxid | Txid | the chapter says of The previous transaction's identifier: 'double-SHA-256 identifier of the transaction that created the output being spent'. |
| chx:isOutputOfHash | is the output of | Digest | HashFunction | the chapter says of Digest: 'A digest is the output of a hash function'. |
| chx:countedByCompactSizeInputs | is a | InputCount | CompactSize | the chapter says of Input count: 'The input count is the compactSize integer that opens the inputs field'. |
| chx:countedByCompactSizeOutputs | is a | OutputCount | CompactSize | the chapter says of Output count: 'The output count is the compactSize integer that opens the outputs field'. |
| chx:isNullOutpoint | is a null form of | NullOutpoint | Outpoint | the chapter says of The null outpoint: 'an outpoint with a null txid of all zeros'. |
| chx:isInputScriptField | is the field of | CoinbaseField | InputScript | the chapter says of The coinbase field: 'the coinbase transaction's input-script field'. |
| chx:followsRelayPolicy | is allowed by | StandardOutput | RelayPolicy | the chapter says of Standard transaction outputs: 'Bitcoin Core's policy for relaying and mining transactions'. |
| chx:isRelayPolicy | is a | OptInRbf | RelayPolicy | the chapter says of Opt-in replace-by-fee: 'Opt-in replace-by-fee is the relay policy'. |
| chx:enablesRelativeTimelock | enables | VersionTwo | Bip68Timelock | the chapter says of Version 2 and BIP68: 'only in a transaction of version 2 or higher is a sequence value below 2 to the 31 a relative timelock'. |
| chx:changesOnlyRelayPolicy | changes only | VersionThree | RelayPolicy | the chapter says of The version 3 proposal: 'changes only the relay policy of full nodes'. |
| chx:wouldReadAsInputCount | would be read by a legacy parser as | MarkerByte | InputCount | the chapter says of Marker byte: 'a legacy parser would read it as a count of zero inputs'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
