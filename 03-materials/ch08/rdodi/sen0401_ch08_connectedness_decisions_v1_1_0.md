# SEN0401 ch08 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.0 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.0) | 109 | 0 | 6 |
| after (1.1.0) | 109 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 109 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:mayNameHashType | may name a hash type of | SignatureSizes | TaprootHashTypes | the chapter says of Schnorr signature sizes: 'in taproot one more byte may name a hash type'; the chapter says of Valid taproot hash types: 'A taproot signature may use only the hash types'. |
| chx:endsWithHashType | ends with a byte holding | DerLayout | FlagValues | the chapter says of Layout of a DER signature: 'followed in Bitcoin by the hash type byte'. |
| chx:changesDigestCommitment | shows what the flag covers of | CommitmentMatrix | DigestCommitment | the chapter says of Matrix of commitments: 'changing a field that the flag covers changes the hash of the signed input'; the chapter says of The signed digest: 'What a signature signs is a hash computed from selected fields of the transaction'. |
| chx:includesAmountInDigest | adds the amount to | AmountCommitment | DigestCommitment | the chapter says of Commitment to the amount (BIP143): 'the signature hash includes the amount of the coin being spent'; the chapter says of The signed digest: 'What a signature signs is a hash computed from selected fields of the transaction'. |
| chx:limitedByAnyoneCanPay | is limited by | TaprootAmounts | AnyoneCanPayEffect | the chapter says of Commitment to all amounts (BIP341): 'unless ANYONECANPAY is used, when it commits only to its own'. |
| chx:rejectsZeroHashType | rejects an explicit zero hash type of | TaprootVerdicts | TaprootHashTypes | the chapter says of Core's taproot verdicts: 'rejects an explicit zero hash type'. |
| chx:holdsSchnorrSignature | holds a signature of the size of | FirstTaprootSpend | SignatureSizes | the chapter says of A first taproot spend: 'a one-element witness holding a 64-byte schnorr signature'. |
| chx:usesEcdsaFormulas | uses the formulas of | LibraryNonceMatches | EcdsaFormulas | the chapter says of Library nonce matches the standard: 'RFC 6979's nonce and the plain ECDSA formulas'. |
| chx:reusesEcdsaNonce | breaks the signer of | NonceReuse | EcdsaFormulas | the chapter says of Nonce reuse: 'If two ECDSA signatures from the same key use the same nonce k'; the chapter says of ECDSA formulas: 'ECDSA signs with a random nonce k'. |
| chx:setsAuxiliaryValue | sets the auxiliary data of | GrindingSource | DefaultNonce | the chapter says of Grinding in the source: 'sign.cpp has the zero auxiliary value'; the chapter says of The default BIP340 nonce: 'derives its nonce from the key, the message and auxiliary data'. |
| chx:changesSchnorrSigning | changes | LibsecpChanges | SchnorrSignatures | the chapter says of Changes in libsecp256k1: 'removed its deprecated function alias for schnorr signing'. |
| chx:supportsMuSig | supports | CoreMusigSupport | MuSigKeyAgg | the chapter says of musig() in Bitcoin Core: 'Bitcoin Core 30.0 added the musig() descriptor and the MuSig2 fields of PSBT'. |
| chx:lacksThresholdBip | finds no BIP for | ThresholdBipGap | ThresholdSharing | the chapter says of No threshold BIP: 'The BIP index has no entry for a threshold signature scheme'. |
| chx:statesSigopsLimit | states | Core30Sigops | LegacySigopsCap | the chapter says of Release note of Core 30.0: 'state the limit of 2,500 legacy signature operations'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
