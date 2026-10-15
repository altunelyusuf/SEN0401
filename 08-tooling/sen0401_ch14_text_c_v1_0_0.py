"""SEN0401 chapter 14 (Second-Layer Applications): the teaching paragraphs of the leaves of subject 4 (the Lightning Network: the routed payment of the book run on five lnd nodes, the transport and the onion recomputed from the published test vectors, and the channel on the chain).
One paragraph per leaf, one line, full sentences, with an everyday comparison, and a citation in the form (Name and Name, 2023). Values from the test network of five lnd 0.21.3-beta nodes on a private Bitcoin Core 31.1 chain are single-run values."""
__version__ = "1.0.0"
C = {}

C["FeeArithmetic"] = (
 "The routed payment of the book is a staircase of amounts: to deliver 1 bitcoin through three intermediaries who each want 0.001, Alice must offer Bob 1.003, Bob offers Carol 1.002, Carol offers Diana 1.001, and Diana pays Eric 1 (Antonopoulos and Harding, 2023). "
 "We built that network of five lnd nodes on a private chain, with channels of 4 bitcoin and the three middle nodes charging a base fee of 0.001 and no proportional fee; the payment of 1 bitcoin cost exactly 300,000 satoshis in fees, and the hop amounts reported by the route were 100,200,000, 100,100,000 and 100,000,000 satoshis, the book's staircase scaled to satoshis. "
 "Each fee rewards the node for tying up its balance until the secret comes back, and the fee fields are part of the instructions in the onion (Lightning developers, 2026). "
 "It is like a relay of couriers each adding a tip to the envelope: the last one gets the parcel, and every earlier one keeps his tip.")

C["TimelockStaircase"] = (
 "Every hop of a routed payment must have more time than the next, so that a node that has paid forward can still collect from the one behind it: the book's HTLCs expire in 10, 9, 8 and 7 blocks, a step of one block (Antonopoulos and Harding, 2023). "
 "On the real network of five lnd nodes the expiries of the hops stepped down by 80 blocks twice and by 0 at the last hop, the invoice asked for a final delta of 80, and the sample configuration of lnd 0.21.3 gives the same 80 as the default timelock delta (Lightning Labs, 2026). "
 "A step of one block would be unsafe, because a congested chain can delay a transaction by more than that, so the real number is a margin for the time a node needs to get its refund or claim on to the chain (Lightning developers, 2026). "
 "It is like the cut-off times of a chain of banks: each bank closes its window earlier than the one it relies on, with enough hours left to react.")

C["BalancesAfterPayment"] = (
 "At the end of the book's example Alice has 0.997 and Bob 3.003 in their channel, each intermediary has earned 0.001, and Eric has received 1 bitcoin (Antonopoulos and Harding, 2023). "
 "The nodes of the test network ended in the same way: Alice's balance fell by 100,300,000 satoshis, each of Bob, Carol and Diana gained 100,000, Eric gained 100,000,000, and the sum of all changes was exactly zero, so nothing was created or lost on the way; Alice's side of her channel stood at 99,696,530 and Bob's at 300,300,000, the 0.997 and 3.003 of the book once the small commitment fee of the channel is counted. "
 "No transaction touched the chain in the process, and the commitment fee is only deducted from the funder's side of each channel (Lightning developers, 2026). "
 "It is like moving money between the tills of a row of shops by notes in the shared ledger: the cash in the drawers does not move until someone closes the shop.")

C["InvoiceStructure"] = (
 "The invoice is how the receiver gives the sender the hash H: a bech32 string, the format of BIP 173, that BOLT 11 fills with the network prefix, the amount, a timestamp and tagged fields for the payment hash, the payment secret, the expiry and the final delay (Wuille and Maxwell, 2017); (Lightning developers, 2026). "
 "The invoice of the test payment had the prefix lnbcrt1, which our decoder read as the regtest network and 1 bitcoin, which is 100,000,000,000 millisatoshi; the payment hash, the payment secret and the expiry in its fields were the same as the ones lnd reported, the final delta was 80, and the secret that came back after payment hashed to the payment hash with SHA-256. "
 "That last check is the proof of payment: the sender holds a secret that only the receiver could have released. "
 "It is like a receipt that is also a key: whoever holds the matching stub can prove the shop took the money.")

C["HoldInvoiceInFlight"] = (
 "A hold invoice lets the receiver delay the release of the secret, which makes the HTLCs of the book's steps 2 to 5 visible at the same time on all hops (Antonopoulos and Harding, 2023). "
 "On the test network a hold invoice for 0.1 bitcoin was paid by Alice: while the receiver withheld the secret, every one of the five nodes showed an HTLC pending in a channel; when the receiver settled the invoice, the secret travelled back and the payment succeeded; a second hold invoice was cancelled, the HTLCs failed back along the route, and the balances of all channels were exactly what they had been before. "
 "Optech describes the contract that makes this possible and its use also in atomic swaps (Bitcoin Optech, 2026). "
 "It is like a parcel held at a depot: everybody on the route has signed for it, and it either goes through when the recipient signs or goes back to the sender.")

C["NoiseHandshakeVector"] = (
 "All traffic between Lightning nodes is encrypted and authenticated point to point; the book states it in one sentence (Antonopoulos and Harding, 2023), and BOLT 8 specifies the handshake as Noise_XK with secp256k1, ChaCha20-Poly1305 and SHA-256 in three acts (Lightning developers, 2026). "
 "The Noise Protocol Framework is the same family of designs that other secure channels use (Wikipedia contributors, 2026). "
 "We wrote the initiator in pure Python and fed it the fixed keys of the published test vector: it produced the 50-byte first act and the 66-byte third act of the vector and the sending key beginning 969ab31b, all equal to the published values. "
 "Because the initiator already knows the responder's static key, an eavesdropper learns neither side's identity from the first acts. "
 "It is like a secret handshake at a club door in which each side proves a piece of knowledge before showing a face.")

C["TransportMessageVector"] = (
 "After the handshake every message is sent as an encrypted two-byte length with a 16-byte tag and then the encrypted body with another 16-byte tag, and the keys rotate after 1,000 uses (Lightning developers, 2026). "
 "The vector sends the five bytes hello: our code, using the sending key from the handshake, produced the 39 bytes that BOLT 8 lists, which are 2 plus 16 plus 5 plus 16, and the ciphertext equalled the published one. "
 "The overhead of 34 bytes per message is the price of hiding even the length of a message from a listener on the network. "
 "It is like sending every letter in a sealed bag with a second sealed bag for its length: the courier cannot see how long the letter is.")

C["OnionPacketVector"] = (
 "The onion that Alice builds follows the Sphinx design, in which each hop peels one layer and learns only the next hop (Danezis and Goldberg, 2009); the book describes it in prose (Antonopoulos and Harding, 2023). "
 "BOLT 4 gives a test vector of five hops with the session key 41 repeated, the five node keys, the payloads and the associated data 42 repeated: our Python code derived the shared secrets, the filler and the layers and produced the packet of 1366 bytes that equals the vector byte for byte (Lightning developers, 2026). "
 "The test also shows the variable-length payload: the last hop of the vector carries 275 bytes while the others carry fewer than 90, and the packet size does not change. "
 "It is like a Russian doll of letters in which every doll is sealed with a different stamp: the first postman can open only the outer one.")

C["OnionFixedSize"] = (
 "A node must not learn from the size of the packet how far it is from the destination, so the packet has a fixed size whatever the length of the path (Antonopoulos and Harding, 2023). "
 "Built with one, two or five hops from the vector's keys and payloads, the packet was always 1366 bytes: one version byte, a 33-byte public key, 1300 bytes of hop payloads and a 32-byte HMAC, as BOLT 4 defines (Lightning developers, 2026). "
 "The unused room is filled with a pseudo-random stream derived from the session key, and a filler is added as each layer is peeled so that the packet keeps its size and its integrity check (Danezis and Goldberg, 2009). "
 "It is like a fixed-size envelope used for every letter: a thick and a thin message arrive in the same envelope.")

C["OnionIntegrityByHmac"] = (
 "Each hop checks the integrity of the packet before it does anything: it derives a shared secret from its own private key and the ephemeral key in the packet, takes the key mu from it and compares the HMAC of the routing bytes and the associated data with the HMAC in the packet (Lightning developers, 2026). "
 "With the private key of the first node from the vector, the vector packet passed, and the same packet with one bit flipped, at the first bit or in the very last bit of the 1300 routing bytes, failed. "
 "The book's promise that intermediate nodes can verify and decrypt their portion of the route information rests on this check (Antonopoulos and Harding, 2023). "
 "It is like a tamper-evident seal on every layer: one scratch on the wrapper and the courier refuses the parcel.")

C["InvoiceVector"] = (
 "BOLT 11 lists invoices to test a parser, among them the one for a cup of coffee, 2500 micro-bitcoin, to be paid within a minute (Lightning developers, 2026). "
 "Our decoder read the prefix lnbc2500u as the main network and 2500 micro-bitcoin, which is 250,000,000 millisatoshi or 250,000 satoshis, the timestamp as 2017-06-01 10:57:38 in UTC, the payment hash as 32 bytes, the expiry as 60 seconds and the signature as 65 bytes. "
 "The format uses the bech32 alphabet and checksum of BIP 173 but without its 90-character limit (Wuille and Maxwell, 2017). "
 "It is like reading a price tag in a foreign unit: the prefix tells the unit, the digits the quantity, and the tail the proof that the shop wrote it.")

C["FundingOutputIsMultisig"] = (
 "The funding transaction of a channel pays into one output that both nodes must sign to spend (Antonopoulos and Harding, 2023). "
 "In lnd the output is a pay-to-witness-script-hash of a 2-of-2 multisignature script; on the test network its value was 4 bitcoin, its type witness_v0_scripthash, and the script read as 2, two 33-byte keys, 2 and OP_CHECKMULTISIG with the keys in lexicographic order, as BOLT 3 requires (Lightning developers, 2026). "
 "The funding transaction was 165 virtual bytes. "
 "Optech notes that newer lnd versions can use taproot with MuSig2 for the funding output, which makes the channel look like any other payment (Bitcoin Optech, 2026). "
 "It is like a safe-deposit box whose two keys are always filed in the same order: anyone can check that the box is the right one without opening it.")

C["CommitmentTransactionShape"] = (
 "Every commitment transaction of an lnd channel carries the marks of BOLT 3: the high bytes of the lock time and the sequence are fixed at 0x20 and 0x80, and the lower 24 bits of each hold half of the obscured 48-bit commitment number, so that a watcher cannot read the state number from it (Lightning developers, 2026). "
 "The revoked commitment that Irene's node broadcast in the test was a version-2 transaction of 279 virtual bytes with four outputs: two anchors of 330 satoshis each, one for each side, the delayed output of the owner, and the immediate output of the other side. "
 "The anchors let either side raise the fee of a stuck commitment later, which is why the fee does not have to be guessed in advance (Bitcoin Optech, 2026). "
 "It is like a form with a fixed header: the clerk can see it is a valid form, but the case number is written in a code that only the parties can read.")

C["RevocationKeyVector"] = (
 "The revocation key of the book is built from two secrets, and BOLT 3 gives the exact formulas: the key is the revocation base point times the hash of the base point and the per-commitment point, plus the per-commitment point times the hash in the other order (Lightning developers, 2026); the private key is derived with the same weights. "
 "From the base secret and the per-commitment secret of the appendix our Python code derived the local key by adding the hash times the generator to the base point, the revocation public key and the revocation private key, and all three equalled the published values, as did the base point. "
 "The point of the formula is that neither the base secret alone nor the per-commitment secret alone can sign, which is the book's 'each party knows only half' (Antonopoulos and Harding, 2023). "
 "It is like a door that opens only when two numbers are dialled together: each partner holds one number, and neither can open the door alone.")

C["CooperativeCloseIsOneTx"] = (
 "The channel of the book lives on two transactions of the chain, the funding and the settlement, and anything in between stays off the chain (Antonopoulos and Harding, 2023). "
 "On the test network Bob and Carol closed their channel by agreement: the closing transaction had a lock time of 0 and final sequence numbers, so it was valid at once, spent the funding output with a witness of an empty item, two signatures and the script, had two taproot outputs worth 399,995,175 satoshis in total, and was 193 virtual bytes. "
 "The 4,825 satoshis missing from the 4 bitcoin are the fee. "
 "A cooperative close avoids the delays of a unilateral one, which BOLT 5 describes for the cases when the other side does not answer (Lightning developers, 2026). "
 "It is like closing a joint account at the counter with both signatures: the money is yours the same day, and nobody has to wait out a notice period.")

C["BreachJusticeTransaction"] = (
 "The book's Hitesh and Irene example was run on two lnd nodes with a channel of 10 bitcoin: they moved 2 bitcoin so that the state went from 5 and 5 to 7 for Hitesh and 3 for Irene (Antonopoulos and Harding, 2023). "
 "We then stopped both, restored Irene's directory from a copy made at the first state, and had her force-close, which published the revoked commitment; Hitesh, restarted, saw the breach and published a justice transaction with two inputs, his own immediate output with a witness of 72 and 37 bytes, and Irene's delayed output through the revocation branch with the items 72, 1 and 77 (the signature is 71 or 72 bytes from run to run), and his wallet received 999,990,380 satoshis, 9,620 less than the whole 10 bitcoin, the difference being the fee. "
 "The node reported the channel as closed by a breach, and Hitesh took 3 bitcoin more than his due of 7, exactly the book's penalty (Lightning developers, 2026). "
 "It is like a bank that, finding you used a cancelled cheque, closes the account and gives the whole balance to the other holder.")

C["MainnetGraphSize"] = (
 "The book calls the Lightning Network proposed and shows five nodes; the statistics page of mempool.space, fetched on 15 October 2026, reported for its latest day, 30 August 2026, 32,518 channels, 16,225 nodes and a total capacity of 375,370,668,018 satoshis, which is about 3,753.7 bitcoin (Mempool Space, 2026). "
 "That makes an average of 4.0 channels per node, and the same page gives the tip of the Bitcoin chain at the time of fetching as height 971,604 (Mempool Space, 2026). "
 "The figures are a snapshot of a public service that can change by the hour and are not part of the executed experiments; the Wikipedia article says that Lightning Labs launched the network in 2018 (Wikipedia contributors, 2026). "
 "It is like the number of branches of a bank printed on its brochure: it tells the scale, not the experience of any one customer.")
