"""SEN0401 chapter 13 (Bitcoin Security): the teaching paragraphs of the leaves of subject 1 (the security model: what a transaction reveals, the encrypted transport, the root of trust and the software one runs). One paragraph per leaf, one line, full sentences:
what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run or recomputed, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the Bitcoin Core 31.1 test chains are single-run values."""
__version__ = "1.0.0"
A = {}

A["SignedTransactionHidesKey"] = (
 "The chapter's first claim is that a Bitcoin payment can travel over an open channel because it authorizes one value to one recipient and reveals no secret, in contrast to a card number that lets anyone charge again (Antonopoulos and Harding, 2023). "
 "On the test chain a wallet whose key we knew signed a payment of 222 bytes, and the spending input held exactly two witness items, a signature of 71 bytes and the public key of 33 bytes; the 32 secret bytes and their WIF text were nowhere in the transaction, which is what Nakamoto's design of anonymous public keys intends (Nakamoto, 2008). "
 "This is also why a transaction can be published to every node: the private key never leaves the signing code, and only its mathematical shadow, the signature, is shared. "
 "It is like signing a cheque with a pen whose ink cannot be turned back into the pen: everybody can see the signature, and nobody can use it to write another cheque.")

A["TamperBreaksSignature"] = (
 "A signature is not a stamp on a blank page but a seal over the exact content, so changing the content breaks it (Lau and Wuille, 2016). "
 "We took the valid payment and swapped the recipient's output script for an attacker's script, and in a second try lowered the first output from 1.5 to 1 coin; the original was accepted by testmempoolaccept and both altered copies were refused with mempool-script-verify-flag-failed, because the signature no longer matched the data it had to cover (Bitcoin Core, 2026). "
 "A block with the swapped version was refused too, which is the same rule one level up. "
 "It is like a sealed envelope with a wax stamp: a thief can open it and copy the letter, but a new address written inside breaks the stamp, and the post office rejects it.")

A["SighashAllIsTheDefault"] = (
 "The chapter's promise that a payment cannot be forged depends on what the signature covers, and the default type SIGHASH_ALL covers every input and every output (Antonopoulos and Harding, 2023). "
 "The signature of the test payment ended with the byte 01, the code of SIGHASH_ALL, and the interpreter of Bitcoin Core 31.1 shows that other types exist, NONE, SINGLE and the ANYONECANPAY flag, while BIP 143 states that the hash of all outputs is used only when the type is neither SINGLE nor NONE (Bitcoin Core, 2026); (Lau and Wuille, 2016). "
 "A signer should therefore know which type a wallet or device uses: with NONE the outputs are left open for whoever builds the transaction. "
 "It is like signing a contract on every page versus signing one page that says only that you agree to something: the first protects the whole, the second protects only what the page says.")

A["ReplayPaysNothing"] = (
 "The book contrasts the credit card, from which anyone holding the number can pull funds again and again, with Bitcoin, where a payment cannot authorize additional payments (Antonopoulos and Harding, 2023). "
 "We tried the replay: after the payment was in a block, sendrawtransaction answered error code -27 with Transaction outputs already in utxo set, testmempoolaccept said txn-already-known, and the receiving wallet held 1.5 coins before and after another block was mined, so broadcasting an old payment moved nothing (Bitcoin Core, 2026). "
 "The reason is the unspent-output model: a transaction spends particular outputs once, and a node that sees the same spend again finds that its inputs are gone. "
 "It is like a train ticket that is punched at the gate: showing the same ticket a second time does not open the gate again.")

A["BookSaysNoEncryption"] = (
 "The chapter says that because security rests on independent verification, no encryption is required for Bitcoin traffic, and it adds that encryption can still be useful (Antonopoulos and Harding, 2023). "
 "The book's chapter 10 is plainer about the state of the software at the time of writing: Bitcoin communicates entirely in the clear, as does the modern implementation of Bitcoin Core, with Tor as the only encrypted option (Antonopoulos and Harding, 2023). "
 "That changed by default: BIP 324 defines a version 2 transport, release 26.0 added it switched off, release 27.0 turned it on, and the help text of 31.1 reads -v2transport Support v2 transport (default: 1) (Mehta et al., 2019); (Bitcoin Core developers, 2023); (Bitcoin Core developers, 2024); (Bitcoin Core developers, 2026). "
 "The value of the chapter's sentence is therefore that encryption is not needed for the safety of the money, while the reason to encrypt is privacy and the cost of eavesdropping; it is like a postcard that cannot be altered but can be read, now sent in an envelope by default.")

A["V2SessionOnBothSides"] = (
 "The version 2 transport is an encrypted channel between two nodes, built from a Diffie-Hellman exchange and an authenticated cipher, and it exports a session id that identifies the channel (Mehta et al., 2019). "
 "We started two private nodes of Bitcoin Core 31.1 on the loopback address and connected them: both reported the transport v2 in getpeerinfo and the same session id of 64 hexadecimal digits, which is the value that two operators could compare by telephone to detect a man in the middle (Bitcoin Core, 2026). "
 "Nothing was captured on the wire here, so what we know is what the two nodes say about themselves. "
 "It is like two people who whisper in a language they invented a minute ago and then each read out the same code word to prove that nobody else joined the conversation.")

A["DowngradeToV1"] = (
 "Encryption in Bitcoin's peer-to-peer network is opportunistic: a node speaks v2 if the other side does and falls back to v1 otherwise (Mehta et al., 2019). "
 "A third test node started with -v2transport=0 did not list P2P_V2 among its services and connected to the listening node as a v1 peer with an empty session id, so that node had one v2 peer and one v1 peer at the same moment (Bitcoin Core, 2026). "
 "BIP 324 says that an eavesdropper who wants to keep listening must become active, by a persistent man in the middle, by downgrading connections to v1 or by running nodes of its own, and that is exactly what the session id allows to be noticed. "
 "It is like a shop that talks to every customer in private if the customer asks, and in the open if not: the open conversation is still possible, but the quiet one is the default.")

A["GenesisHashHardCoded"] = (
 "The chapter's root of trust is the genesis block, the single block that a node does not verify but is given, from which the chain of trust runs up to the current block (Antonopoulos and Harding, 2023). "
 "In the source of Bitcoin Core 31.1 the mainnet genesis hash is typed in and asserted, and the genesis block in the explorer data has exactly that id at height 0; the regtest chain of our test nodes has a typed-in genesis too, with no previous block (Bitcoin Core, 2026); (Mempool Space, 2026). "
 "Every other block is justified by the proof of work that links it to this one, the chain of hash-based proof-of-work that Nakamoto's paper describes as a record that cannot be changed without redoing the work (Nakamoto, 2008). "
 "It is like the zero-kilometre stone of a road network: all distances are measured from it, and it is not itself measured from anywhere.")

A["GenerateblockRefusesBadSignature"] = (
 "A node enforces the rules even on the blocks it makes itself, so it will not turn a forged payment into a block (Antonopoulos and Harding, 2023). "
 "The call generateblock with the address-swapped transaction answered error code -25 with TestBlockValidity failed: block-script-verify-flag-failed (Script evaluated without error but finished with a false/empty top stack element), while the same call with the correct transaction returned a block hash (Bitcoin Core, 2026). "
 "The signature check and the script rules are the consensus check that every full node repeats, which is the sense of the chapter's advice not to outsource validation. "
 "It is like a bank clerk who checks the signature on every cheque himself instead of taking the word of the person who handed it over.")

A["AssumeValidShortcut"] = (
 "The book says that the only thing to be explicitly trusted is a fully validated blockchain, and for nearly everything that is so, but Bitcoin Core 31.1 contains a second anchor that the chapter does not mention (Antonopoulos and Harding, 2023). "
 "The default assumevalid value in chainparams.cpp is block 938,343, mined on 2026-02-25 by F2Pool, and the help text says the node assumes that block and its ancestors are valid and potentially skips their script verification, a saving that ends when the option is set to 0; on the day of the fetch the tip was 971,580, so the shortcut covered the chain up to 33,237 blocks below it (Bitcoin Core, 2026); (Bitcoin Core developers, 2026); (Mempool Space, 2026). "
 "The help text speaks only of script verification, and the hash is part of the software that people download, which is why the release check of the next paragraphs matters. "
 "It is like a customs officer who has checked every parcel of a sealed container once and then lets the container's earlier contents pass on a stamp, looking only at what has been added since.")

A["TarballHashMatches"] = (
 "The experiments of this chapter ran on a binary that was first checked against the published list of hashes, the smallest step of the advice not to trust what one has not verified (Antonopoulos and Harding, 2023). "
 "The SHA-256 of the 90,293,352-byte tarball bitcoin-31.1-x86_64-linux-gnu.tar.gz, beginning b80d9c3e04da78fb, equals its line among the 28 lines of SHA256SUMS, and the same line is in the saved copy of the list (Bitcoin Core release signers, 2026). "
 "This catches a corrupted download or a mirror that serves another file, but it says nothing about who wrote the list. "
 "It is like comparing the weight printed on a parcel with the weight on the scale: it shows that nothing fell out on the way, not that the sender is honest.")

A["SignatureNeedsKeys"] = (
 "A list of hashes is only as good as the channel it came by, so Bitcoin Core publishes SHA256SUMS together with detached signatures of its builders, and the user must check them against keys obtained elsewhere (Bitcoin Core release signers, 2026). "
 "The signature file holds 11 signatures; gpg with an empty keyring found all 11 of them and could call none good, exit code 2 and No public key eleven times, which is the honest answer when no builder's key has been imported and shows that the check cannot be done by the hash alone (Bitcoin Core release signers, 2026). "
 "The project goes further than signing: its Guix instructions say the aim is to reproduce the toolchain instead of blindly trusting binary downloads, so that many builders arrive at the same bytes (Bitcoin Core, 2026). "
 "It is like a notary's stamp: the stamp on the paper means nothing until you know whose stamp it is and have a reason to believe it.")
