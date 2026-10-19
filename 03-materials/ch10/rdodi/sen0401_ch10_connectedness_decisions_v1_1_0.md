# SEN0401 ch10 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.1 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.1) | 86 | 0 | 6 |
| after (1.1.0) | 86 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 86 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:countsBloomNodes | counts the nodes of | ServiceBitsOfNetwork | BloomDisabledByDefault | the chapter says of Service bits of network: '4,308 with BLOOM'; the chapter says of Bloom disabled by default: 'only 4,308 of 25,361 nodes of the census advertise the bit'. |
| chx:countsCompactFilterNodes | counts the nodes of | ServiceBitsOfNetwork | FiltersOverP2P | the chapter says of Service bits of network: '7,905 with COMPACT_FILTERS'; the chapter says of Block filters over the peer-to-peer network: '7,905 nodes of the census advertise the bit'. |
| chx:countsV2Nodes | counts the nodes of | ServiceBitsOfNetwork | V2DefaultHistory | the chapter says of Service bits of network: '21,768 with P2P_V2'; the chapter says of Default history of the v2 transport: '85.8 percent of the nodes of the census advertise P2P_V2'. |
| chx:sizesHeaders | is the total size of | HeaderChainSize | HeaderChainLinks | the chapter says of Header chain size: 'the 80-byte headers total 77.7 megabytes'; the chapter says of Header chain links: 'each header is 80 bytes'. |
| chx:prefillsBecauseNotInMempool | is prefilled because of | CoinbaseIsPrefilled | MempoolIsLocalUtxoIsShared | the chapter says of Coinbase is prefilled: 'because no peer can have it in its mempool'; the chapter says of The mempool is local, the UTXO set is shared: 'Two connected nodes held 6 and 0 transactions in their mempools'. |
| chx:needsVersion70016 | is needed for | ProtocolVersionNumber | TxAnnouncementByWtxid | the chapter says of Protocol version number: 'wtxid relay needs 70016 too'; the chapter says of Transaction announcement by wtxid: 'With wtxid relay the transactions were announced with inv entries of type 5'. |
| chx:negotiatesWtxidRelay | negotiates | HandshakeMessageOrder | TxAnnouncementByWtxid | the chapter says of Handshake message order: 'the feature messages wtxidrelay and sendaddrv2'; the chapter says of Transaction announcement by wtxid: 'With wtxid relay the transactions were announced with inv entries of type 5'. |
| chx:sendsFeefilter | sends | HandshakeMessageOrder | FeefilterHonoured | the chapter says of Handshake message order: 'after verack it sends sendcmpct, ping, getheaders, inv and feefilter'; the chapter says of Feefilter honoured: 'A peer that sent feefilter for 5,000 satoshis per kilovirtual byte'. |
| chx:hidesMagicOf | hides the magic of | EncryptedV2 | MessageFraming | the chapter says of Encrypted v2 transport (BIP 324): 'neither the magic nor the word version appears in the stream'; the chapter says of Message framing: 'Every message starts with a 24-byte header of magic, command, length and checksum'. |
| chx:addsNetworks | adds the networks of | Addrv2Networks | I2pAndCjdns | the chapter says of Addrv2 networks (BIP 155): 'BIP 155 adds TORV3, I2P and CJDNS entries'; the chapter says of I2P and CJDNS: 'Support for I2P came in release 22.0 and for CJDNS in 23.0'. |
| chx:countsOnionNodes | is counted in | TorHiddenService | ReachableNodesToday | the chapter says of Tor hidden service: '12,488 nodes of the census are onion addresses'; the chapter says of Reachable nodes today: '12,488 are onion services'. |
| chx:countsI2pNodes | is counted in | I2pAndCjdns | ReachableNodesToday | the chapter says of I2P and CJDNS: 'the census holds 4,208 I2P nodes and one CJDNS node'; the chapter says of Reachable nodes today: '4,208 I2P'. |
| chx:introducesAsSatoshi | introduces itself in | PeersAreEqual | VersionMessageFields | the chapter says of Peers are equal: 'the node answered with its version message as /Satoshi:31.1.0/'; the chapter says of Version message fields: 'the user agent /Satoshi:31.1.0/'. |
| chx:advertisesServicesInVersion | advertises services in | ArchivalNodeServices | VersionMessageFields | the chapter says of Archival node services: 'advertises the services value 3081'; the chapter says of Version message fields: 'services 3081'. |
| chx:advertisesPrunedServicesInVersion | advertises services in | PrunedNodeServices | VersionMessageFields | the chapter says of Pruned node services: 'in both its networkinfo and its version message'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
