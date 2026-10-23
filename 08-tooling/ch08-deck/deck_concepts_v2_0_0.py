"""The key concepts of chapter 8 for the deck 2.0.0: the 45 distinct primary-source concepts of the chapter research (03-materials/ch08/rdodi/sen0401_ch08_research_v1_2_0.ttl, de-duplicated by
normalised label), each with the branch of the chapter it belongs to, a one-sentence meaning and one everyday analogy (deck standard D4); the one-line meaning and analogy of every branch (level 1) and
group (level 2) that the dividers show. A card reads: the concept, its meaning, then 'Think of ...'. NEW file; nothing earlier is edited."""
__version__ = "2.0.0"

# level 1: divider subtitle (carries the meaning and the analogy of the branch)
L1 = {
    "SignatureFoundations": "A signature is a wax seal that only the owner of the ring can press.",
    "SighashFlags": "A flag chooses how much of the letter the seal covers.",
    "SchnorrSignatures": "Schnorr is a seal whose imprints can be added together.",
    "EcdsaSignatures": "ECDSA is the older seal, with a messier imprint and two valid shapes.",
    "Randomness": "The nonce is a one-time pad: use it twice and the secret leaks.",
    "SegwitSigning": "Segwit changed what is signed, as a cheque that also states the amount.",
    "SinceTheBook": "Standards move on after print, like a map that needs a new edition.",
}

# level 2: (pill, meaning, analogy)   pill at most 4 words
L2 = {
    "SignatureRoles": ("What a signature does", "Three inputs go in and a yes or no comes out.", "a bank clerk who checks cheque, ID and signature card"),
    "GroupArithmetic": ("Arithmetic of the curve", "Two moduli: scalars wrap at n, coordinates at p.", "two clocks of different sizes on one wall"),
    "TransactionSigning": ("Signing a transaction", "What is signed is a digest of the transaction.", "signing the fingerprint of a contract, not the paper"),
    "FlagCoding": ("How flags are coded", "A flag is one byte appended to the signature.", "a tick box printed at the bottom of a form"),
    "Commitments": ("Commitments by flag", "Each flag fixes some fields and leaves others open.", "a contract with some clauses left blank"),
    "KnownPitfalls": ("Known pitfalls", "SINGLE with no matching output signs the number one.", "a lock that opens when the keyhole is missing"),
    "IdentityProtocol": ("Proof to signature", "A three-move proof becomes a signature by hashing.", "a quiz whose questions are drawn by a dice you cannot cheat"),
    "Bip340Format": ("The BIP340 format", "Fixed sizes, x-only keys and tagged hashes.", "a standard envelope that fits every letterbox"),
    "Aggregation": ("Aggregating keys", "Keys and signatures add up, with one trap.", "pooling several keys into one master key"),
    "ThresholdSharing": ("Threshold sharing", "Any two of three key holders can sign.", "a vault that opens when two of three managers turn their keys"),
    "EcdsaMath": ("The ECDSA equations", "Two formulas, and two valid values of s.", "a coin that has two faces and both count"),
    "DerEncoding": ("DER serialization", "A signature is written as nested length-prefixed fields.", "a parcel with labels on each box inside"),
    "ConsensusAndPolicy": ("Consensus and policy", "Miners enforce the law; nodes add house rules.", "the law of the land and the rules of a shop"),
    "NonceSafety": ("Safety of the nonce", "A repeated nonce lets anyone solve for the key.", "reusing a one-time pad"),
    "DeterministicNonces": ("Deterministic nonces", "The nonce is derived from key and message.", "a recipe that always bakes the same cake"),
    "SignatureSize": ("Size and grinding", "Signing again until R is small saves a byte.", "re-folding a letter until it fits the smaller envelope"),
    "HashingCost": ("Cost of hashing", "The old algorithm re-reads the transaction per input.", "reading the whole book again for every page you sign"),
    "ValueCommitment": ("Commitment to amounts", "New signatures cover the value being spent.", "a cheque that states the sum it releases"),
    "TaprootSigning": ("Taproot signing", "A taproot spend carries one 64-byte signature.", "a single stamp in place of a pile of papers"),
    "StandardsStatus": ("Standards status", "Proposals move from draft to deployed.", "a bill becoming law"),
    "LibrarySupport": ("Library support", "Core and its library add features after print.", "a car model year with new options"),
    "History": ("History and dates", "The patent, the first spend, the activation.", "the dates on a family tree"),
    "EvidenceTrail": ("The evidence trail", "Every claim is tied to a saved source or a run.", "the receipts kept in a shoebox"),
}

# key concepts: label as in the research -> (branch, meaning, analogy)
K3 = {
    "Digital Signatures": ("SignatureFoundations", "Proof that the owner of a private key approved a message.", "a handwritten signature that nobody else can forge"),
    "How Digital Signatures Work": ("SignatureFoundations", "A signer holds a secret; everyone checks with the public key.", "a padlock anyone can close but only you can open"),
    "Creating a Digital Signature": ("SignatureFoundations", "The signer combines the message digest, the secret key and a nonce.", "pressing a personal seal into hot wax"),
    "Verifying the Signature": ("SignatureFoundations", "Message, public key and signature go in; yes or no comes out.", "a clerk comparing your signature with the card on file"),
    "discrete logarithm problem": ("SignatureFoundations", "Given a point, finding the number that produced it is infeasible.", "mixing paint: easy to mix, impossible to unmix"),
    "Signature Hash Types (SIGHASH)": ("SighashFlags", "One byte says which parts of the transaction the signature covers.", "a tick box that says how much of the contract you sign"),
    "signature hash": ("SighashFlags", "The digest of the transaction fields that is actually signed.", "the fingerprint of a document"),
    "SIGHASH_ALL": ("SighashFlags", "Signs all inputs and all outputs; the default.", "signing a cheque with payee, amount and date all filled in"),
    "SIGHASH_NONE": ("SighashFlags", "Signs the inputs but no output.", "a signed blank cheque"),
    "SIGHASH_SINGLE": ("SighashFlags", "Signs only the output with the same number as the input.", "initialling a single line of an invoice"),
    "SIGHASH_ANYONECANPAY": ("SighashFlags", "Signs only this input; others may add theirs.", "a collection tin that anyone may add to"),
    "BIP118": ("SighashFlags", "A proposal for signatures that leave out the coin they spend.", "a ticket valid for any seat in the row"),
    "SIGHASH_DEFAULT": ("SighashFlags", "Taproot's zero byte, which means the same as ALL and is left out.", "the standard setting you never have to tick"),
    "Schnorr Signatures": ("SchnorrSignatures", "A signature s = k + e x, proven by one equation on points.", "a seal whose imprints can be added"),
    "Serialization of Schnorr Signatures": ("SchnorrSignatures", "A BIP340 signature is 64 bytes: R's x coordinate and s.", "a form with two fixed boxes"),
    "Schnorr-based Scriptless Multisignatures": ("SchnorrSignatures", "Several signers produce one ordinary signature.", "a group photo that looks like a single portrait"),
    "Schnorr-based Scriptless Threshold Signatures": ("SchnorrSignatures", "A subset of the key holders produces one ordinary signature.", "a committee vote that leaves one signature on the minutes"),
    "challenge": ("SchnorrSignatures", "The value e that ties the nonce point to the message.", "a question the exam board sets after you commit to an answer"),
    "Fiat-Shamir transform": ("SchnorrSignatures", "Replace the verifier's random challenge by a hash.", "letting a dice-rolling machine play the examiner"),
    "BIP340": ("SchnorrSignatures", "The specification of Schnorr signatures for Bitcoin.", "the standard plug that makes every device fit"),
    "x-only public key": ("SchnorrSignatures", "A 32-byte key: the x coordinate, with an even y assumed.", "a map reference that always faces north"),
    "linearity": ("SchnorrSignatures", "Sums of keys and signatures are keys and signatures of the sum.", "adding two bills and paying the total at once"),
    "batch verification": ("SchnorrSignatures", "Many signatures are checked with one combined equation.", "weighing a whole crate instead of every apple"),
    "key prefixing": ("SchnorrSignatures", "The public key is hashed into the challenge.", "writing your name on your own envelope"),
    "scriptless multisignature": ("SchnorrSignatures", "Keys are added so no script is needed to count signers.", "one master key made from several keys"),
    "key cancellation attack": ("SchnorrSignatures", "A signer picks a key that cancels the other's key.", "a partner who copies your key and subtracts it"),
    "MuSig2": ("SchnorrSignatures", "Key aggregation with hashed weights that defeats the attack.", "master keys cut from a mould that includes every member"),
    "Shamir secret sharing": ("SchnorrSignatures", "A secret is the height of a line, shared as points on it.", "a treasure map torn so that any two pieces show the way"),
    "scriptless threshold signature": ("SchnorrSignatures", "Any k of n signers produce one signature without a script.", "two of three managers opening the vault"),
    "ECDSA Signatures": ("EcdsaSignatures", "The signature Bitcoin used from 2009; Schnorr joined it in 2021.", "the older seal still on every old document"),
    "ECDSA Algorithm": ("EcdsaSignatures", "Sign with a nonce and invert it; verify by rebuilding a point.", "a recipe with one step that must be undone exactly"),
    "Serialization of ECDSA Signatures (DER)": ("EcdsaSignatures", "The pair (R, s) written in nested length-prefixed fields.", "a nest of labelled boxes inside a parcel"),
    "ECDSA": ("EcdsaSignatures", "Elliptic Curve Digital Signature Algorithm.", "a notary's stamp of the pre-2021 era"),
    "R and s": ("EcdsaSignatures", "The two numbers that make up an ECDSA signature.", "the two halves of a torn ticket"),
    "malleability": ("EcdsaSignatures", "Anyone can alter a valid signature without the key.", "a receipt that can be reprinted in another font"),
    "DER": ("EcdsaSignatures", "Distinguished Encoding Rules, the byte layout of signatures.", "the postal rules for addressing a parcel"),
    "low-S rule": ("EcdsaSignatures", "Of s and n minus s, only the smaller is relayed.", "of two coin faces, always showing heads"),
    "The Importance of Randomness in Signatures": ("Randomness", "The nonce must be unpredictable and used only once.", "a combination lock set by a coin toss, never reused"),
    "nonce": ("Randomness", "The one-time secret number k of a signature.", "a one-time pad"),
    "RFC 6979": ("Randomness", "Derives the nonce from key and message by HMAC.", "a recipe that always bakes the same cake"),
    "nonce reuse": ("Randomness", "Two signatures with one nonce reveal the private key.", "reusing a one-time pad, which hands the secret to a snoop"),
    "Segregated Witness's New Signing Algorithm": ("SegwitSigning", "BIP143 hashes less and signs the spent amount.", "reading the table of contents instead of the whole book"),
    "BIP143": ("SegwitSigning", "The signature hash of segregated witness version 0.", "a new form with a box for the sum"),
    "O(n) hashing": ("SegwitSigning", "BIP143 hashes a number of bytes in proportion to the inputs.", "one walk down the line instead of a full lap per person"),
    "taproot signature": ("SegwitSigning", "A BIP340 signature over the BIP341 message, 64 bytes.", "one stamp that stands for the whole bundle"),
}

# aliases: a second label of the same concept that a card shows as 'Also called'
ALIAS = {}
