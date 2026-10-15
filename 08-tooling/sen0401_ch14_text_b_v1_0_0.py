"""SEN0401 chapter 14 (Second-Layer Applications): the teaching paragraphs of the leaves of subject 3 (payment channels: the one-way channel of Emma and Fabian, the revocable commitments of Hitesh and Irene, and the hash time lock contract).
One paragraph per leaf, one line, full sentences, with an everyday comparison, and a citation in the form (Name and Name, 2023). Values from the test chains are single-run values."""
__version__ = "1.0.0"
B = {}

B["EmmaFabianArithmetic"] = (
 "The streaming-video example of the book is a channel in which Emma pays Fabian 0.01 millibit for each second, which is 0.00001 bitcoin or 1,000 satoshis, so an hour costs 3,600,000 satoshis, the 36 millibits that she locks, and 600 seconds cost 600,000 and leave 3,000,000 for her refund (Antonopoulos and Harding, 2023). "
 "The same sums were used on the test chain: the funding output held 3,600,000 satoshis and the settlement after six seconds paid Fabian 6,000 satoshis. "
 "The idea that a stream of tiny payments can be settled by one transaction at the end is an old one, discussed under micropayments long before Lightning (Wikipedia contributors, 2026), and the Bitcoin Wiki records the channel techniques that followed (Bitcoin Wiki, 2026). "
 "It is like a taxi meter: the fare grows every second in the cab, and only the final amount is paid at the door.")

B["FundingNeedsBothKeys"] = (
 "The funding transaction pays into a 2-of-2 multisignature output, so that neither party can take the money without the other (Antonopoulos and Harding, 2023). "
 "The witness script of the test channel was 71 bytes long, starting with the opcode for 2 and ending with 2 and OP_CHECKMULTISIG; the funding transaction was 165 virtual bytes; a spend signed by Emma alone was refused by the node with the script error about the signature check, and a spend signed by both was accepted. "
 "This is also the weakness the book points out: after funding, Emma needs Fabian's signature even to get her money back, which is why the refund must be signed before the funding is broadcast (Decker and Wattenhofer, 2015). "
 "It is like a safe-deposit box that needs two keys: the bank cannot open it alone and neither can you, which is secure until one key holder disappears.")

B["RefundTimelockLadder"] = (
 "The book solves the vanishing-partner problem with transaction-level lock times: Emma obtains a signed refund with a lock time 30 days ahead, which is 4,320 blocks at 144 a day, and every later commitment gets a lock time one block shorter, so that the newest can be broadcast first (Antonopoulos and Harding, 2023). "
 "On the test chain six commitments had lock times from 488 down to 483; at the start all six were refused as non-final, at height 483 only the sixth was accepted, and once it was mined the earlier ones were refused with missing inputs, because the sixth had spent the shared funding output. "
 "The book then shows why this is not good enough: it fixes the life of the channel and limits the number of updates to the number of blocks, which is why revocation was invented (Poon and Dryja, 2016). "
 "It is like a row of postdated cheques in which the latest has the earliest date: the bank honours the first it can, and the others bounce.")

B["AsymmetricCommitment"] = (
 "In the asymmetric scheme each party holds a commitment transaction that pays the other side at once and pays himself only after a delay, so that broadcasting costs the broadcaster time (Antonopoulos and Harding, 2023). "
 "The delayed output has the script of the book: IF the revocation key, ELSE 1000 blocks, CHECKSEQUENCEVERIFY, DROP and the owner's key, then CHECKSIG. On the test chain a spend of that output with 999 confirmations was refused as non-BIP68-final, with 1000 it was accepted, and a spend whose input carried no sequence number was refused by the script with the lock time not satisfied; the rules are in BIP 68 and BIP 112 (Friedenbach et al., 2015); (BtcDrak et al., 2015). "
 "The commitment was 181 virtual bytes. "
 "It is like a loan whose payout date is written on the cheque: the bank pays the other party now but makes you wait.")

B["RevocationNeedsBothHalves"] = (
 "The revocation key is built so that both parties know the public key but each knows only half of the private key, and each reveals his half when he moves on to a new state (Antonopoulos and Harding, 2023). "
 "On the test chain a spend of the penalty branch signed with one half was refused by the node with the signature check failing, a spend signed with the sum of both halves was accepted and confirmed, and its witness had three items of 72, 1 and 77 bytes in the recorded run: the signature, whose length varies between 71 and 72 bytes from run to run, a one that selects the revocation branch, and the script. "
 "The derivation that lnd uses is specified in BOLT 3 and checked below against the published vectors (Lightning developers, 2026). "
 "It is like a vault door with a dial each partner sets: once you have told your half of the number to the other, he alone can open it if you ever try to cheat.")

B["PenaltyTakesEverything"] = (
 "The punishment is what makes revocation work, and the book gives the numbers: the channel of 10 coins moves from 5 and 5 to 7 for Hitesh and 3 for Irene, going back to the old state would give Irene 2 more, but if she broadcasts it Hitesh has the revocation key and takes all 10 (Antonopoulos and Harding, 2023). "
 "Irene would lose her whole 3 and Hitesh would gain 3 over his due of 7, so cheating has a negative expected value as soon as there is any chance of being caught. "
 "On the hand-built channel the penalty spend was confirmed, and on the lnd nodes the same thing happened with a justice transaction, described below. "
 "The catch, which the book states, is that the wronged party must watch the chain and answer within the delay, which is the reason for watchtowers (Bitcoin Optech, 2026). "
 "It is like a deposit forfeited for breaking a lease: the landlord need not prove a loss, he simply keeps all of it.")

B["StateIndexBits"] = (
 "The book says that the state of a Lightning channel is identified by a 48-bit index, which allows 281 trillion changes (Antonopoulos and Harding, 2023). "
 "The exact figure is 2 to the power 48, 281,474,976,710,656, or about 2.8 times 10 to the 14. "
 "BOLT 3 derives the per-commitment secret of each state from one seed with a chain of hashes that flips bits of the seed, and its test vectors include the secret of the highest index for a seed of all ff bytes, which our Python code reproduced as 7cc854b5 and so on (Lightning developers, 2026). "
 "The shachain lets the other side store all revealed secrets in a small tree instead of a long list. "
 "It is like the numbering of lottery tickets from a single seed: you can print the ticket for any number, but you cannot guess the next one from the last.")

B["HtlcSecretBranch"] = (
 "A hash time lock contract commits funds to a secret: whoever shows the preimage R of the hash H, together with the receiver's signature, can take the payment (Antonopoulos and Harding, 2023). "
 "On the test chain the hand-built contract paid out with the right 32-byte secret and the receiver's key, refused a wrong secret at the hash comparison, refused the right secret with the payer's key, and, in the book's basic form without a key in the first branch, paid anyone who knew the secret. "
 "The Bitcoin Wiki and Optech describe the construction and its uses in channels and atomic swaps (Bitcoin Wiki, 2026); (Bitcoin Optech, 2026). "
 "It is like a locker whose code is known to one person: the code opens it, and the code alone is enough.")

B["HtlcTimeoutBranch"] = (
 "The second branch gives the money back if the secret is never shown: the payer can claim a refund after the absolute time in a CHECKLOCKTIMEVERIFY, so that nobody's funds stay locked forever (Antonopoulos and Harding, 2023). "
 "On the test chain the contract was funded at height 1495 with a lock at 1514, 19 blocks later; the refund was refused as non-final before the lock and one block short of it, accepted at the lock, and a refund transaction whose own lock time was lower than the one in the script was refused by the script, as BIP 65 requires (Todd, 2014). "
 "In a routed payment the lock times shrink along the path, so each node can still refund himself after the next one has failed. "
 "It is like a gift card with an expiry: if nobody claims it before the date, it goes back to the buyer.")

B["HashIsRipemdOfSha"] = (
 "There is a small difference between the book's script and the real one: the book writes HASH160 of H, and BOLT 3 writes RIPEMD160 of the SHA-256 of the preimage in the scripts for the 20-byte hash comparison (Antonopoulos and Harding, 2023); (Lightning developers, 2026). "
 "On the test chain the hand-built contract used a 20-byte hash, equal to the RIPEMD-160 of the 32-byte payment hash, and the witness script of the book's form came to 101 bytes. "
 "The payment hash in an invoice is the 32-byte SHA-256 of the secret, so one secret serves every hop. "
 "It is like two stamp sizes for one seal: the big one on the invoice, the small one inside the lock, both made from the same die.")
