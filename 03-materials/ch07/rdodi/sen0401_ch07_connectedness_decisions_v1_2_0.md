# SEN0401 ch07 - connectedness and link decisions for the domain T-Box 1.2.0

Written 2026-10-19 by the connectedness repair of the branch connectedness-repair. The committed T-Box 1.1.0 is untouched; 1.2.0 is the new version (MINOR: no class added, removed or renamed).

## Measured (oe_connectedness, discipline v2.18.0 BP-D56)

| | classes | standing alone | islands |
|---|---|---|---|
| before (1.1.0) | 83 | 0 | 8 |
| after (1.2.0) | 83 | 0 | 0 |
| after, with chx:hasOwner left out of the graph | 83 | 0 | 0 |

The last row shows that the repair does not lean on chx:hasOwner, whose domain and range are the union of every type the A-Box shows.

## Relations set (each is an object property with one domain and one range; the basis is the chapter's own definition)

| property | label | domain | range | basis |
|---|---|---|---|---|
| chx:isOutputWithData | is an output whose script is the | OpReturnOutput | OutputScript | the chapter says of OP_RETURN output: 'An OP_RETURN output is an output whose script begins with OP_RETURN followed by data'. |
| chx:comparesTopOfStack | compares with the top of | CheckLockTimeVerify | StackExecution | the chapter says of OP_CHECKLOCKTIMEVERIFY: 'the number on top of the stack'. |
| chx:isKindOfOutputScript | is a kind of | WitnessProgram | OutputScript | the chapter says of Witness program: 'A witness program is an output script made of a version byte'. |
| chx:holdsPublicKeyHash | holds | P2wpkh | PublicKeyHash | the chapter says of Pay to witness public key hash: 'A P2WPKH output holds a version 0 and the 20-byte hash of a compressed public key'; the chapter says of Public key hash: 'A public key hash is the 20-byte digest'. |
| chx:wrapsRedeemScript | has as redeem script | NestedSegwit | RedeemScript | the chapter says of Nested segregated witness: 'A nested segregated witness output is a script hash output whose redeem script is a witness program'. |
| chx:definesSighashOfWitness | defines the signature hash for | WitnessSighash | SignatureHash | the chapter says of Witness signature hash: 'BIP143 defines the signature hash for version-0 witness programs'. |
| chx:isWitnessProgramOfVersion1 | is a | Taproot | WitnessProgram | the chapter says of Taproot output: 'A taproot output is a witness program of version 1'. |
| chx:commitsToScriptTree | commits to | Taproot | Mast | the chapter says of Taproot output: 'the root of a script tree'; the chapter says of Merklized alternative script tree: 'commits to a set of alternative scripts with the root of a Merkle tree'. |
| chx:disablesMultisigOpcodes | disables the old opcodes of | TapscriptChanges | ScriptedMultisignature | the chapter says of Changes in tapscript: 'Tapscript disables the old multisignature opcodes'. |
| chx:makesScriptDisappear | makes the script disappear from | ScriptlessMultisignature | ScriptedMultisignature | the chapter says of Scriptless multisignature: 'the script that would count the keys and signatures disappears'; the chapter says of Scripted multisignature: 'lists k public keys and requires at least t valid signatures'. |
| chx:isOutputScriptHoldingHash | is an output script holding a hash of a key in | PayToPublicKeyHash | OutputScript | the chapter says of Pay to public key hash: 'A pay to public key hash output script contains a hash that commits to a public key'. |
| chx:endsInFailureUnlessTrue | ends in failure unless it is | VerifyGuard | ScriptTruth | the chapter says of VERIFY guard clause: 'ends the script with failure unless its result is true'; the chapter says of When a script succeeds: 'A script succeeds when it runs without error'. |
| chx:selectsPathByInputScript | selects the path by | MultiPathScript | InputScript | the chapter says of Scripts with several paths: 'the input script selects the path'. |
| chx:composesScript | is a structured way of writing a subset of | Miniscript | Script | the chapter says of Miniscript: 'a structured way of writing a subset of Bitcoin Script'. |
| chx:isOutputScriptHoldingScriptHash | is an output script holding a hash of a script in | PayToScriptHashOutput | OutputScript | the chapter says of Pay to script hash output: 'A pay to script hash output script holds only the 20-byte HASH160 of a script'. |
| chx:isRevealedInInputScript | is revealed in | RedeemScript | InputScript | the chapter says of Redeem script: 'revealed as the last item of the input script'. |
| chx:isPoppedFromStack | is popped from | CheckmultisigDummy | StackExecution | the chapter says of The CHECKMULTISIG dummy element: 'the extra stack item that OP_CHECKMULTISIG pops after its signatures'. |

## Classes for which no honest relation was found

None: every island of the file is joined to the rest by at least one relation that the chapter's sources state.

## Link discovery (oe_link_discovery, discipline v2.19.0 BP-D57): decision for each candidate

| candidate | trust | decision | reason |
|---|---|---|---|
| SEM-1 hasOwner | high | set | domain and range declared as the union of every type the A-Box shows on the two sides (BP-D57 step 3) |
| SYN-2 input, output | high | declare | chx:input and chx:output declared as datatype properties of rd:IOExample, range xsd:string, with label and comment |
