"""SEN0401 chapter 14 (Second-Layer Applications): the teaching paragraphs of the leaves of the subjects 1 and 2 (the guarantees that the base system gives to applications, and colored coins with single-use seals, pay to contract and client-side validation).
One paragraph per leaf, one line, full sentences: what the thing is, why it matters, where it lives in Bitcoin Core or the book, how it was run on the private test chain of Bitcoin Core 31.1, and an everyday comparison. Every paragraph cites a source in the form (Name and Name, 2023).
Values from the test chains are single-run values."""
__version__ = "1.0.0"
A = {}

A["DoubleSpendRejected"] = (
 "The first guarantee on the chapter's list is that no output can be spent twice in the same valid chain (Antonopoulos and Harding, 2023). "
 "We tested it on a private chain: the first payment of an output paid a fee of 100,000 satoshis and entered the memory pool; a second payment of the same output with a lower fee of 50,000 was refused as an insufficient replacement; a second payment with the higher fee of 200,000 replaced the first, which Bitcoin Core now allows by default without any signal (Bitcoin Core developers, 2024); and after a block had confirmed the winner, an attempt to send the first transaction again was refused because its input was already spent. "
 "The memory pool is only a waiting room, so what the guarantee really says is that the chain of blocks will contain at most one of the two, and nothing is final before the block. "
 "It is like two people holding tickets for the same seat: the usher lets only one of them in, and which one is decided by who is processed first, not by who arrived first.")

A["OutputsCannotExceedInputs"] = (
 "The accounting guarantee says that the outputs of a transaction cannot exceed its inputs, so that value cannot be created in a payment (Antonopoulos and Harding, 2023). "
 "We built a transaction whose outputs asked for more than the output it spent and the node refused it with the reason bad-txns-in-belowout, the very reason that appeared when one pledger of the crowdfunding test below sent his part alone and the sum fell short of the goal. "
 "The rule is applied to every transaction by every node, and a miner who ignores it produces a block that the others reject, which is why the ledger can be trusted without a bookkeeper. "
 "It is like a cashier who counts the notes in the drawer before and after each sale: the books balance every time, and a mistake of one coin is found at once.")

A["NonExpiration"] = (
 "A valid transaction does not expire: if it is valid today it will be valid later, as long as its inputs remain unspent and the rules do not change (Antonopoulos and Harding, 2023). "
 "On the test chain we signed a payment at block height 301 and kept it back; at height 451, 150 blocks later, the node still accepted it. "
 "This property is what lets the parties of a payment channel keep signed transactions in a drawer for weeks, and it is also why a channel needs special rules to cancel an old state, because an old signed transaction never goes bad by itself (Poon and Dryja, 2016). "
 "It is like a cheque without an expiry date: it can be cashed years later, so the only way to make it useless is to empty the account it is drawn on.")

A["EighteenBuildingBlocks"] = (
 "The chapter begins with a list of guarantees, which it calls building blocks, from no double spend, immutability and neutrality to timelocks, forgery protection and predictable issuance (Antonopoulos and Harding, 2023). "
 "Counted in the saved text of the chapter the list has 18 entries, and the chapter says plainly that it is not complete and that new blocks are added with each new feature, as the package rules and the pay-to-anchor output of Bitcoin Core 28.0 show (Bitcoin Core developers, 2024). "
 "The practical lesson is that an application should name the guarantees it relies on, because each one has conditions, for example the depth of confirmation for immutability or the unchanged rules for non-expiration. "
 "It is like the list of materials in a building plan: the builder can only promise a roof if the walls are certified to carry it.")

A["ProofOfExistence"] = (
 "A digital notary needs nothing but a commitment recorded in a transaction: the data stays with its owner and only its fingerprint goes into the chain, where immutability and the timestamp of the block do the rest (Antonopoulos and Harding, 2023). "
 "On the test chain we computed the 32-byte SHA-256 of a document, wrote it as an OP_RETURN output with a value of zero, had the node confirm it, and read the output script back as OP_RETURN followed by exactly that hash; from then on the document is proved to have existed no later than that block. "
 "Bitcoin Core relays such data-carrier outputs by default up to a size that its help text states (Bitcoin Core developers, 2026). "
 "It is like posting a sealed copy of your manuscript to yourself: the postmark proves the date, the seal proves the content, and nobody else has to read it.")

A["LighthouseCrowdfund"] = (
 "The Lighthouse style of crowdfunding combines three guarantees, integrity, atomicity and consistency: each pledger signs his own input and the single agreed output with the ANYONECANPAY flag, and the transaction cannot be spent until the goal is funded (Antonopoulos and Harding, 2023). "
 "In the test two pledges of 1.0005 and 1 coin met a goal of 2 coins plus a fee of 50,000 satoshis: with one pledge alone the node refused the transaction because the outputs exceeded the inputs, with both it accepted it, and changing the output after the signatures made the script check fail, because the signature hash of the signed input covers the output (Lau and Wuille, 2016). "
 "The flag that makes this possible is explained in the signature chapter of the book (Antonopoulos and Harding, 2023). "
 "It is like a petition sheet that is only valid when the last signature has filled it: the earlier names stay on the sheet, but the office does not act on it before.")

A["UtxoIsASingleUseSeal"] = (
 "A single-use seal is a thing that can be closed over a message only once, like the tamper-evident seal on a parcel, and an unspent transaction output is exactly that, because it can be spent once in a valid chain and the spending transaction is the message (Antonopoulos and Harding, 2023). "
 "Peter Todd described this idea for asset transfer in a text dated 5 December 2017 (Todd, 2017). "
 "In the test, three outputs served as seals in a chain of transfers, each earlier one was spent by the transaction that carried the next commitment, and the three outpoints were all different, so each seal was closed once. "
 "It is like a numbered sheet of postage stamps that the post office cancels when used: the number can appear on only one cancelled letter.")

A["PayToContractTweak"] = (
 "Pay to contract lets two parties agree on contract terms and then tweak the receiver's public key with a hash of those terms, so that the output commits to the contract while looking like any other key (Antonopoulos and Harding, 2023). "
 "We recomputed it in Python: the tweaked key equalled the plain key plus the tweak times the generator point, the output was not the same as the plain pay-to-witness-key-hash output, the revealed key and contract were accepted by the check while a wrong contract was rejected, and the node accepted a spend with the tweaked key and refused one with the plain key, with the script failure at the hash comparison. "
 "The same construction became part of the basis of taproot, whose rules are in BIP 341 (Wuille et al., 2020). "
 "It is like writing the terms of a deal inside the ink of a signature: nobody can see them, but whoever knows them can show that the signature carries them.")

A["ContractStaysOffChain"] = (
 "Because only the tweaked key is published, the contract can be as long and detailed as the parties like, in any language, and nothing is revealed about it, not even that it exists (Antonopoulos and Harding, 2023). "
 "In the test the contract was 69 bytes, the outputs on the chain were ordinary pay-to-witness-key-hash outputs, and the token amounts were not visible anywhere in the transactions. "
 "The Optech topic on client-side validation describes the same trade: the data lives with the owners and the chain only anchors it (Bitcoin Optech, 2026). "
 "It is like a letter in a closed envelope: the post office sees the address and the stamp, and the content is between sender and receiver.")

A["ClientSideValidationWalk"] = (
 "Since the nodes do not check the contract, the receiver does, and this is client-side validation: the sender hands over the history of the asset and the receiver checks that every step is anchored in a transaction and follows the contract rules (Antonopoulos and Harding, 2023). "
 "In the test the history had three steps, an issue of 100 tokens and two transfers; the checker recomputed each commitment against the public key in the output on the chain and found all three equal, and a forged contract text did not match. "
 "The receiver needs only the history that concerns his coins, which is also the privacy gain the book names, and which Optech lists among the properties of the protocols that use the method (Bitcoin Optech, 2026). "
 "It is like buying a used car with its service book: the buyer checks every stamp against the garage, and does not need the records of other cars.")

A["ColoredCoinsHistory"] = (
 "Colored coins are the oldest of the applications in the chapter: Meni Rosenfeld's overview is dated 4 December 2012 and describes marking small amounts of bitcoin to stand for other assets (Rosenfeld, 2012), the Bitcoin Wiki still describes the term as a class of methods for real-world assets (Bitcoin Wiki, 2026), and Peter Todd's single-use-seal design that the book builds on is dated 5 December 2017, five years later (Todd, 2017). "
 "The book names the first implementation Enhanced Padded-Order-Based Coloring and then three newer mechanisms, seals, pay to contract and client-side validation (Antonopoulos and Harding, 2023). "
 "The shift in those five years was from writing the asset data into the chain to keeping it off the chain and anchoring it only by commitments. "
 "It is like moving from stamping the message on the banknote itself to filing it in a private ledger that points at the banknote's number.")

A["RgbAndTaprootAssets"] = (
 "The two protocols that the chapter names for colored coins are RGB and Taproot Assets, and both are built on seals, pay to contract and client-side validation (Antonopoulos and Harding, 2023). "
 "The RGB site describes its smart contracts as post-blockchain and says that nothing is kept on the chain (RGB developers, 2026); the documentation of Lightning Labs describes Taproot Assets with Lightning in mind (Lightning Labs, 2026); and the Optech topic lists RGB, Taro and Taproot Assets together as client-side validation protocols (Bitcoin Optech, 2026). "
 "The book adds the note that taproot is part of Bitcoin and Taproot Assets is not, and that forwarding an asset over Lightning can be native or translated, with the risk of a free option for the receiver in the translated case. "
 "We did not install either protocol; they are in the list of what was not executed. "
 "It is like two currencies exchanged at a booth that is in the city but not run by the city: the booth uses the city's bank for settlement and keeps its own books.")
