# SEN0401 ch05 - connectedness and link decisions for the domain T-Box 1.2.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.1.0 is untouched; 1.2.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.1.0) | 111 | 0 | 7 |
| after (1.2.0) | 111 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 111 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:recordsFingerprint | records | KeyOrigin | KeyFingerprint | the chapter says of Key origin: 'records, in brackets, the fingerprint of the master key and the path from it to the key'. |
| chx:recordsKeyPath | records | KeyOrigin | KeyPath | the chapter says of Key origin: 'records, in brackets, the fingerprint of the master key and the path from it to the key'. |
| chx:followsBip44Structure | follows | StandardPath44 | Bip44Structure | the chapter says of BIP44 path for legacy scripts: 'BIP44's account path for pay-to-public-key-hash scripts'. |
| chx:isBackedUpAlongside | is backed up alongside | ExplicitPath | RecoveryCodes | the chapter says of Explicit path: 'derivation information backed up alongside the recovery code'. |
| chx:includesBip39Checksum | includes | Bip39Code | Bip39Checksum | the chapter says of BIP39 recovery code: 'encodes a random number together with a short checksum'. |
| chx:derivesRootSeed | gives rise to | Bip39Code | RootSeed | the chapter says of BIP39 recovery code: 'from which a 512-bit seed is derived'. |
| chx:mixesIntoSeed | is mixed into | RecoveryPassphrase | Seed | the chapter says of Recovery code passphrase: 'mixed into the derivation of the seed'. |
| chx:splitsSeed | splits | Slip39Code | Seed | the chapter says of SLIP39 share set: 'SLIP39 splits one seed into several word codes with a threshold'. |
| chx:underpinsSlip39 | is the mathematics behind | SecretSharing | Slip39Code | the chapter says of Secret sharing: 'the mathematics behind SLIP39'. |
| chx:isTakenFromSha | is taken from | Bip39Checksum | ShaAlgorithm | the chapter says of BIP39 checksum: 'of the SHA-256 hash of the entropy'. |
| chx:appliesHmacSha512 | applies | Pbkdf2 | HmacSha512 | the chapter says of PBKDF2: 'it applies HMAC-SHA512 2,048 times to the words and the salt'. |
| chx:isRootSeedOf | is the root of | RootSeed | HdWallet | the chapter says of Root seed: 'The root seed is the value from which every key of a hierarchical deterministic wallet is derived'. |
| chx:isDerivedFromRootSeed | is derived from | MasterPrivateKey | RootSeed | the chapter says of Master private key: 'the left 32 bytes of HMAC-SHA512 over the seed'. |
| chx:explainsPublicDerivation | explains | KeyTweak | PublicChildDerivation | the chapter says of Key tweak: 'so that the child public key can be computed by someone who does not know the private key'; the chapter says of Public child key derivation: 'adding a value to a public key gives the public key of the sum'. |
| chx:copiesWalletDatabase | copies | EncryptedWalletBackup | WalletDatabase | the chapter says of Encrypted wallet backup: 'a complete copy of the wallet database'. |
| chx:isEncryptedUnderSeedKey | is encrypted under a key derived from | EncryptedWalletBackup | Seed | the chapter says of Encrypted wallet backup: 'encrypted under a key derived from the seed'. |
| chx:testsRecoveryCode | tests | BackupTesting | RecoveryCodes | the chapter says of Testing a backup: 'learn that a code, a path and the non-key data are all sufficient'. |
| chx:testsPathBackup | tests | BackupTesting | PathBackup | the chapter says of Testing a backup: 'learn that a code, a path and the non-key data are all sufficient'. |
| chx:testsNonkeyBackup | tests | BackupTesting | NonkeyBackup | the chapter says of Testing a backup: 'learn that a code, a path and the non-key data are all sufficient'. |
| chx:usesHardwareSigningDevice | can use | ExternalSigning | HardwareSigningDevice | the chapter says of External signing: 'a hardware signing device or the other signers of a multisignature scheme'. |
| chx:writesDownRecoveryCode | writes down | WrittenBackup | RecoveryCodes | the chapter says of Written backup: 'the recovery code on paper'. |
| chx:deploysExtendedPublicKey | deploys | XpubDeployment | ExtendedPublicKey | the chapter says of Extended public key deployment: 'Deploying an extended public key means putting the watching half of a wallet on an exposed computer'. |
| chx:watchesWithExtendedPublicKey | watches with | PaymentProcessor | ExtendedPublicKey | the chapter says of Payment processor: 'with the extended public key'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
