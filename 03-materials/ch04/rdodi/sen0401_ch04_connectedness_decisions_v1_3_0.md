# SEN0401 ch04 - connectedness and link decisions for the domain T-Box 1.3.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.2.0 is untouched; 1.3.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.2.0) | 87 | 0 | 4 |
| after (1.3.0) | 87 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 87 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:encodesHash160 | commits to | P2pkhAddress | Hash160 | the chapter says of P2PKH address: 'the base58check encoding of version 0x00 and the HASH160 of the public key'. |
| chx:isEncodedAsBase58Check | is encoded as | P2pkhAddress | Base58Check | the chapter says of P2PKH address: 'the base58check encoding of version 0x00 and the HASH160 of the public key'. |
| chx:locksWithPublicKey | locks funds with | P2pk | PublicKey | the chapter says of Pay to public key (P2PK): 'locks funds with the receiver's public key'. |
| chx:containsSignature | contains | InputScript | DigitalSignature | the chapter says of Input script: 'it consists of a signature and the public key'. |
| chx:containsPublicKey | contains | InputScript | PublicKey | the chapter says of Input script: 'it consists of a signature and the public key'. |
| chx:usesCurvePoint | uses a point of | P2tr | Secp256k1 | the chapter says of Pay to taproot (P2TR): 'a point on the secp256k1 curve'. |
| chx:commitsToSha256 | commits to | P2wsh | Sha256 | the chapter says of Pay to witness script hash (P2WSH): 'OP_0 followed by the 32-byte SHA256 of a script'. |
| chx:targetsHash160 | targets | PreimageAttack | Hash160 | the chapter says of Preimage attack: 'for a secure 160-bit function such as HASH160'. |
| chx:appliesRipemd160 | applies | Hash160 | Ripemd160 | the chapter says of HASH160: 'HASH160 is the RIPEMD-160 of the SHA256 of the data'. |
| chx:appliesSha256 | applies | Hash160 | Sha256 | the chapter says of HASH160: 'HASH160 is the RIPEMD-160 of the SHA256 of the data'. |
| chx:specialises | specialises | Secp256k1 | EllipticCurve | the chapter says of The secp256k1 curve: 'The secp256k1 curve, y squared = x cubed + 7'; the chapter says of Elliptic curve: 'set of points (x, y) that satisfy an equation such as y squared = x cubed + 7'. |
| chx:encodesPrivateKey | encodes | WalletImportFormat | PrivateKey | the chapter says of Wallet import format (WIF): 'the base58check encoding of version byte 0x80 and the private key'. |
| chx:extendsPrivateKey | extends | CompressedPrivateKey | PrivateKey | the chapter says of Compressed private key: 'it is the private key followed by a one-byte suffix 01'. |
| chx:prefixesAddress | starts the text of | VersionPrefix | P2pkhAddress | the chapter says of Version prefix: '1 for a P2PKH address, 3 for P2SH'. |
| chx:defaultsToP2wpkh | defaults to | DefaultAddressType | P2wpkh | the chapter says of Default address type: 'defaults to bech32, a P2WPKH address'. |
| chx:derivesPrivateKeys | derives | DeterministicWallet | PrivateKey | the chapter says of Deterministic wallet and seed: 'derives all its private keys from a single seed'. |
| chx:linksPaymentsTo | links the payments received at | AddressReuse | Address | the chapter says of Address reuse and privacy: 'Receiving several payments to the same address links them all together'. |
| chx:holdsPrivateKeys | holds | HardwareSigningDevice | PrivateKey | the chapter says of Hardware signing device: 'holds private keys and uses them only to sign'. |
| chx:printsPrivateKey | prints | PaperWallet | PrivateKey | the chapter says of Paper wallet: 'a private key printed on paper'. |
| chx:encryptsPrivateKey | encrypts | PassphraseProtection | PrivateKey | the chapter says of Passphrase-protected key: 'BIP38 encrypts a private key under a passphrase into a 58-character base58check string'. |
| chx:testsBech32m | gives test cases for | TestVectors | Bech32mAddress | the chapter says of BIP350 test vectors: 'valid and invalid segwit addresses and bech32m strings'. |
| chx:carriesPublicKey | can carry | DecentralizedIdentifier | PublicKey | the chapter says of Decentralized identifier (DID): 'verification methods such as public keys'. |
| chx:provesControlOf | proves control with | KeyControlProof | PrivateKey | the chapter says of Proof of control by a key: 'Whoever holds a private key can prove control of the matching public key by signing'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
| SYN-1 X_Secp256k1 -> X_EllipticCurve | medium | rejected | The text is right and the relation is set where the model carries it: chx:specialises links the classes The secp256k1 curve and Elliptic curve. An individual-level link would change the A-Box, which this repair does not touch. |
| SYN-1 X_SecondPreimageAttack -> X_PreimageAttack | medium | rejected | The definition only says the chance is 'again' about 1 in 2 to the 160; it contrasts what is found (a different input for a given input) and states no relation of dependence between the two attacks, which are siblings in the model. |

The rejected rows are the ledger sen0401_ch04_link_decisions_v1_3_0.tsv, in the format of LINK_DECISIONS_v*.tsv.
