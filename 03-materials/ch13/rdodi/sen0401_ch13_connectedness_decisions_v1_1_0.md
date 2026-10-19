# SEN0401 ch13 - connectedness and link decisions for the domain T-Box 1.1.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.0.2 is untouched; 1.1.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.0.2) | 84 | 0 | 5 |
| after (1.1.0) | 84 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 84 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:swapsRecipientOf | swaps the recipient that a signature commits to in | HardwareDoesNotCheckTheAddress | TamperBreaksSignature | the chapter says of The device does not check the address: 'swap out the recipient's address'; the chapter says of Tampering breaks the signature: 'A signature covers the outputs'. |
| chx:explainsAddressOf | explains the different address of | SortedmultiOrder | DescriptorIsPartOfBackup | the chapter says of The order in sortedmulti: 'multi with the same keys in two orders gave different addresses'; the chapter says of The descriptor is part of the backup: 'the same three keys in a different order under multi gave another address'. |
| chx:mentionsSameSuccessorAs | names the same SLIP39 as | Codex32AndSlip39 | CoreHasNoMnemonics | the chapter says of Codex32 and SLIP39: 'the book's chapter 5 lists SLIP39 as a successor to BIP39'; the chapter says of Core has no mnemonics: 'the book's chapter 5 does mention SLIP39'. |
| chx:signsPsbtLike | signs a PSBT as in | TwoOfThreeSigning | PsbtThroughColdNode | the chapter says of Two-of-three signing: 'the first key alone left the PSBT incomplete with 1 signature'; the chapter says of A PSBT through a cold node: 'took the unsigned PSBT of 528 characters'. |
| chx:callsForNewBackupLike | calls for a new backup as the lesson of | EncryptionMakesNewSeed | StaleBackupMissesFunds | the chapter says of Encryption makes a new seed: 'both say to make a new backup at once'; the chapter says of A stale backup misses funds: 'A backup does not know what happens after it'. |
| chx:keepsKeyOnPaperLike | keeps a private key on paper like | CasasciusHologram | PaperWalletsAreObsolete | the chapter says of The Casascius hologram: 'a private key on paper under a tamper-evident hologram'; the chapter says of Paper wallets are obsolete: 'a single private key on paper'. |
| chx:failsAsCustodianLike | fails as a custodian like | BitfinexSegregatedWallets | MtGoxLoss | the chapter says of Bitfinex segregated wallets: 'a custodian's wallet design can fail'; the chapter says of The Mt. Gox loss: 'exchanges that concentrate user funds in a single hot wallet'. |
| chx:leavesUnrunDevice | records as not run | WhatWasNotExecuted | ExternalSignerSupport | the chapter says of What was not executed: 'the hardware device'; the chapter says of External signer support: 'signs for a hardware device'. |
| chx:leavesUnrunPaper | records as not run | WhatWasNotExecuted | PaperWalletsAreObsolete | the chapter says of What was not executed: 'paper and metal backups'; the chapter says of Paper wallets are obsolete: 'a seed printed on paper'. |
| chx:leavesUnrunBreach | records as not run | WhatWasNotExecuted | MtGoxLoss | the chapter says of What was not executed: 'an exchange breach'; the chapter says of The Mt. Gox loss: 'closed after losing 744,408 bitcoins'. |
| chx:leavesUnrunShamir | records as not run | WhatWasNotExecuted | ShamirTwoOfThree | the chapter says of What was not executed: 'Shamir in a wallet'; the chapter says of Shamir two-of-three: 'any two of them recovered the secret'. |
| chx:leavesUnrunBip39 | records as not run | WhatWasNotExecuted | CoreHasNoMnemonics | the chapter says of What was not executed: 'BIP 39 recovery in Core'; the chapter says of Core has no mnemonics: 'Bitcoin Core does not use BIP 39 words'. |
| chx:leavesUnrunGpg | records as not run | WhatWasNotExecuted | SignatureNeedsKeys | the chapter says of What was not executed: 'a good gpg verification'; the chapter says of A signature needs keys: 'could call none of them good with an empty keyring'. |
| chx:leavesUnrunBip324 | records as not run | WhatWasNotExecuted | V2SessionOnBothSides | the chapter says of What was not executed: 'BIP 324 on the wire'; the chapter says of The v2 session on both sides: 'both reported the transport v2'. |
| chx:leavesUnrunEstate | records as not run | WhatWasNotExecuted | HeirWaitsTenBlocks | the chapter says of What was not executed: 'estate planning with a lawyer'; the chapter says of The heir waits ten blocks: 'A script can give an heir a delayed path'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
