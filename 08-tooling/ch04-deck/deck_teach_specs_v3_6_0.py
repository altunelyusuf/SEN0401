#!/usr/bin/env python3
"""Specs of the 32 picture slides added in the chapter 4 deck v3.6.0 (a NEW tool file): (after old slide, key, title, subtitle, takeaway, drawing function). The order inside one 'after' is the order on the deck."""
from deck_teach_slides_a_v3_6_0 import *
from deck_teach_slides_b_v3_6_0 import *

SPECS = [
    (8, "SIG", "A digital signature proves you hold the key", "Sign with the private key, verify with the public key", "Only the key holder can sign; anyone can verify", SIG),
    (8, "L0", "A lambda is a function without a name", "The one-line helper that the next code uses", "A lambda is a tiny function written where it is needed", L0),
    (10, "RAND", "Secure randomness decides how safe a key is", "The secrets module for keys, random only for simulation", "If the source can be guessed, the key can be guessed", RAND),
    (11, "FF", "A finite field: arithmetic on a clock face", "Why every coordinate stays inside 256 bits", "Wrap around at p and every answer stays exact", FF),
    (11, "SECP", "The curve secp256k1 and the curve standard", "One curve, one generator, one agreed list of parameters", "A standard fixes the numbers so every program agrees", SECP),
    (12, "PA", "Adding points, and the point at infinity", "Line, third point, mirror: the rule behind k times G", "Adding points is the one step the whole chapter repeats", PA),
    (15, "DL", "Why the multiplier cannot be found", "The discrete logarithm problem and brute-force search", "Going forward is quick; going back is a search through half of all keys", DL),
    (15, "LIB", "Do not write your own cryptography", "A readable sketch next to a tested library", "Use a tested library for anything that guards real money", LIB),
    (19, "BB", "Bits, bytes and number bases", "The same public key written in four ways", "A larger base writes the same number in fewer characters", BB),
    (19, "IP", "The first way to pay: an IP address", "Why Bitcoin moved to addresses", "An address lets anyone pay you while you are offline", IP),
    (21, "STACK", "Scripts run on a stack", "A P2PKH script, one opcode at a time", "Each opcode takes the top items and pushes its result", STACK),
    (22, "COMMIT", "A hash is a commitment to a key", "Publish the hash now, reveal the key when spending", "The address commits to the key without showing it", COMMIT),
    (25, "P2PKH", "The P2PKH address and its script", "One lock and its printed label", "The address is a short label for the 25-byte script", P2PKH),
    (26, "NET", "Mainnet and testnet look different on purpose", "Version bytes and human-readable parts keep the chains apart", "An address tells a wallet which chain it belongs to", NET),
    (29, "MSIG", "Multisignature: any two of three keys", "OP_CHECKMULTISIG in a 105-byte script", "Several keys share control; no single key decides alone", MSIG),
    (31, "SECOND", "Second preimage: matching a given hash", "Three attacks and the work each one needs", "Matching a given hash is as hard as 2 to the 160 tries", SECOND),
    (31, "SW", "Segregated witness separates the signatures", "Why the transaction identifier stops changing", "Signatures leave the identifier, so nobody can alter it", SW),
    (31, "NEST", "Segwit inside P2SH: a bridge for old wallets", "A witness program wrapped in a script hash", "An old payer can pay a new receiver without knowing it", NEST),
    (32, "BCHERR", "Bech32 catches typing mistakes", "A BCH code with a guarantee", "Any error in four letters or fewer is always caught", BCHERR),
    (33, "TYPES", "Three segwit output types", "Key hash, script hash and Taproot key", "All three are a version, a push and a program", TYPES),
    (34, "LEN", "The weakness that bech32m repairs", "A letter q before the final p", "In bech32 one q more or less goes unnoticed", LEN),
    (34, "B32M", "Bech32m changes one constant", "Which checksum constant goes with which witness version", "Version 0 uses bech32; versions 1 and later use bech32m", B32M),
    (34, "QR", "Capitals make smaller QR codes", "The alphanumeric mode of a QR code", "A bech32 address in capitals needs fewer bits", QR),
    (42, "DEFAULT", "Which address a wallet hands out by default", "The four values of the addresstype option", "Bitcoin Core hands out bech32 unless you ask otherwise", DEFAULT),
    (42, "EXPORT", "Why a wallet no longer exports one key", "dumpprivkey and importprivkey are gone", "One exported key can endanger a whole deterministic wallet", EXPORT),
    (42, "BIP38", "BIP38: a private key under a passphrase", "Something you have plus something you know", "Encrypted keys are met on old paper wallets, not in new software", BIP38),
    (42, "SEED", "One seed, every key", "How a deterministic wallet derives its keys", "Back up the seed once and every key comes back", SEED),
    (42, "REUSE", "One address, one payment", "Why reusing an address costs privacy", "A fresh address for each payment keeps payments unlinked", REUSE),
    (42, "HW", "A hardware signing device keeps the key inside", "The computer prepares, the device signs", "The key never meets general-purpose software", HW),
    (44, "TVXC", "Test vectors and independent checks", "How an implementation earns trust", "Agreement between independent programs is the evidence", TVXC),
    (44, "CTL", "A key proves control without a registry", "Challenge, signature, check", "Control is shown by signing, not by being on a list", CTL),
    (44, "URIDID", "URIs and decentralized identifiers", "A name for a thing, and a name you control with a key", "A DID is a URI whose controller proves control with a key", URIDID),
]
assert len(SPECS) == 32 and len({s[1] for s in SPECS}) == 32
