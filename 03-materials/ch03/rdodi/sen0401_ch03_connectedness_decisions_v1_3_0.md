# SEN0401 ch03 - connectedness and link decisions for the domain T-Box 1.3.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.2.0 is untouched; 1.3.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.2.0) | 115 | 0 | 7 |
| after (1.3.0) | 115 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 115 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:reportsChainWork | reports | BlockchainInfo | ChainWork | the chapter says of Blockchain information (getblockchaininfo): 'its difficulty and chain work'. |
| chx:reportsDifficulty | reports | BlockchainInfo | Difficulty | the chapter says of Blockchain information (getblockchaininfo): 'its difficulty and chain work'. |
| chx:indexesTransactions | indexes | TransactionIndex | Transaction | the chapter says of Transaction index (txindex): 'builds an index of every transaction so that getrawtransaction can find any of them'. |
| chx:sizesCacheOf | sizes the cache of | DatabaseCache | UtxoSet | the chapter says of Database cache (dbcache): 'sizes the cache of the unspent-output set'. |
| chx:acceptsBlocksFrom | accepts blocks from | BlocksOnlyMode | Peer | the chapter says of Blocks-only mode: 'a node accepts blocks from its peers but not unconfirmed transactions'. |
| chx:timesBlockHeader | gives the times in | UnixTime | BlockHeader | the chapter says of Unix time: 'Bitcoin uses it for the times in block headers'. |
| chx:isComputedByShift | is computed by | BlockSubsidy | BitShift | the chapter says of Block subsidy: 'is shifted right once for every 210,000 blocks'. |
| chx:isWrittenIn | is written in | SourceCode | ProgrammingLanguage | the chapter says of Source code: 'mainly C++ in Bitcoin Core'; the chapter says of Programming language: 'the chapter meets C++ for the node'. |
| chx:isDrawnForCookie | is drawn for | RandomNumber | CookieAuthentication | the chapter says of Random number: 'for cookies and salts'; the chapter says of Cookie authentication: 'Bitcoin Core creates a random credential on each start'. |
| chx:isDrawnForSalt | is drawn for | RandomNumber | Salt | the chapter says of Random number: 'for cookies and salts'; the chapter says of Salt: 'A salt is a random value mixed into the hashing of a password'. |
| chx:isFollowedByTests | is followed by | Compilation | SoftwareTesting | the chapter says of Compilation: 'is followed by the unit tests'. |
| chx:isStoredInDataDirectory | is stored in | CookieAuthentication | DataDirectory | the chapter says of Cookie authentication: 'stores it in the data directory as .cookie'. |
| chx:usesHmac | uses | RpcAuth | Hmac | the chapter says of Hashed credentials (rpcauth): 'the HMAC-SHA256 of the password under that salt'. |
| chx:usesSalt | uses | RpcAuth | Salt | the chapter says of Hashed credentials (rpcauth): 'a user name, a random salt and the HMAC-SHA256 of the password'. |
| chx:includesCommandLineClient | includes | Executable | CommandLineClient | the chapter says of Executable: 'bitcoin-cli the command-line client'. |
| chx:providesNode | provides | Executable | Node | the chapter says of Executable: 'bitcoind is the node'. |
| chx:buildsReproducibly | builds reproducibly | ReproducibleBuild | SourceCode | the chapter says of Reproducible build: 'bit-for-bit identical files from the same source'. |
| chx:checksAgainstChecksum | is checked against | ReleaseVerification | Checksum | the chapter says of Release verification: 'checked against the SHA-256 checksums the project publishes'. |
| chx:checksSignature | is checked against | ReleaseVerification | OpenPgpSignature | the chapter says of Release verification: 'and the signatures on them'. |
| chx:checksTransactions | checks | FullNode | Transaction | the chapter says of Full node: 'checks every confirmed transaction against every rule of the system'. |
| chx:isUpdatedByBlock | is updated for every | UtxoSet | Block | the chapter says of Set of unspent outputs: 'a node updates it for every block'. |
| chx:deletesOldBlocks | deletes old | PrunedNode | Block | the chapter says of Pruned node: 'deletes old blocks to reduce disk use'. |
| chx:isDeployedBy | is deployed by | SoftFork | ImprovementProposal | the chapter says of Soft fork: 'BIP 9 lets several be deployed in parallel by signalling in the block version'. |
| chx:mapsKeysOf | maps the keys of | JsonLdContext | JsonFormat | the chapter says of JSON-LD context: 'maps the keys of a JSON text to IRIs'. |
| chx:comesFromFullNode | comes from | VerifiedData | FullNode | the chapter says of Verified data: 'Data from your own node is authoritative because the node verified it itself'; the chapter says of Full node: 'A full verification node checks every confirmed transaction against every rule of the system'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
| SYN-1 X_JsonFormat -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_Api -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_JsonRpc -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_AutotoolsBuild -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_CookieAuthentication -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_HttpRequest -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_SoftwareTesting -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_RandomNumber -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_LegacyWallet -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_ConfigurationFile -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_ConfigurationFile -> X_StartupLog | medium | rejected | The definition says only where bitcoind -printtoconsole shows the file being looked for; the start-up log is mentioned as the place a message appears, not as a thing the configuration file is related to. |
| SYN-1 X_SourceCode -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_Database -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_OpenSourceSoftware -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_DataDirectory -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |
| SYN-1 X_DatabaseCache -> X_ReferenceImplementation | medium | rejected | The text names Bitcoin Core, the reference implementation, only in passing, as the program the described thing belongs to or runs in; the two individuals are not related by that mention, and the class-level relations of this file already carry what the chapter states about the reference implementation. |

The rejected rows are the ledger sen0401_ch03_link_decisions_v1_3_0.tsv, in the format of LINK_DECISIONS_v*.tsv.
