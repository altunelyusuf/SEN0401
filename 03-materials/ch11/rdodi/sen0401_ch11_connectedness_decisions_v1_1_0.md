# SEN0401 ch11 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.1 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.1) | 91 | 0 | 5 |
| after (1.1.0) | 91 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 91 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:givesRootOfBlock | gives the merkle root of | Block277315Links | RealBlockRoot | the chapter says of Links of block 277,315: 'merkle root 5e049f40...'; the chapter says of Real block root: 'the code reproduces the merkle root 5e049f40...'. |
| chx:holdsReversedHashOfParent | holds the hash that links to | HashNotStoredInBlock | PreviousHashPointsToParent | the chapter says of Hash not stored in block: 'the header of block 481 holds the reversed hash of block 480'; the chapter says of Previous hash points to parent: 'every header's previous-hash field equalled the recomputed hash of the header before'. |
| chx:explainsTwoChildren | is shown by | HeightIsNotUnique | TwoChildrenOneParent | the chapter says of Height is not unique: 'two children of the same parent were both at height 511'; the chapter says of Two children one parent: 'two different blocks with the same parent hash and the same height 511'. |
| chx:hashesTheHeader | is the hash of | BlockHashIsDoubleSha256 | HeaderIs80Bytes | the chapter says of Block hash is double sha256: 'The block hash is the SHA-256 of the SHA-256 of the 80-byte header'; the chapter says of The header is 80 bytes: 'Every header'. |
| chx:constrainsTimestamp | constrains | Bip94Rules | TimestampField | the chapter says of BIP 94 rules: 'the first block of a period may be no more than 600 seconds earlier than its parent'; the chapter says of Timestamp field: 'The timestamp is a 4-byte count of seconds since 1970-01-01'. |
| chx:reportsMedianTime | reports | RegtestStartState | MedianTimePast | the chapter says of Regtest start state: 'median time 1296688602'; the chapter says of Median time past: 'A block's timestamp must be later than the median of the previous 11 timestamps'. |
| chx:usesDoubleHashOfChallenge | uses the same double SHA-256 as | SignetMagicFromChallenge | BlockHashIsDoubleSha256 | the chapter says of Signet message start from the challenge: 'the first four bytes of the double SHA-256 of its challenge'; the chapter says of Block hash is double sha256: 'The block hash is the SHA-256 of the SHA-256 of the 80-byte header'. |
| chx:differsInGenesisFrom | differs in genesis from | SharedGenesisTransaction | Testnet4Replaces | the chapter says of Shared genesis transaction: 'testnet4 has its own coinbase of 180'; the chapter says of Testnet4 replaces testnet3: 'Testnet4 begins with a genesis block that quotes the Bitcoin block hash of 3 May 2024'. |
| chx:rebuildsFromBits | is rebuilt from the bits of | GenesisHashRecomputed | TargetCompactEncoding | the chapter says of Genesis hash recomputed: 'the bits 0x1d00ffff'; the chapter says of Target compact encoding: '0x1d00ffff is the target 0xffff followed by 26 zero bytes'. |
| chx:hasHeaderAndCount | has the header and count of | MerkleblockForLightClients | BlockIsHeaderPlusTransactions | the chapter says of Merkleblock for light clients: 'header, count 16, 5 hashes, flags'; the chapter says of Block is header plus transactions: 'A block is the 80-byte header, then a counter of the transactions'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
