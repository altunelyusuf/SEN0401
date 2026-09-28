"""SEN0401 chapter 4 (Mastering Bitcoin 3rd edition, Keys and Addresses) for the RDODI build.
Every claim read on 2026-09-29 from the source it cites; every computation executed under Python 3.14.4 by a toolkit
written for the chapter and checked against Bitcoin Core 31.1, the book's own bech32 reference library and the BIP350 test
vectors (08-tooling/ch04-evidence/)."""
__version__ = "1.0.0"
CH = 4
DATE = "2026-09-29"
PYVER = "3.14.4"
TITLE = "Keys and addresses: from a random number to a payable string, recomputed and cross-checked"
QUESTION = "How does chapter 4 of Mastering Bitcoin's 3rd edition lead from a private key to the public key, the legacy and the segwit address, which of its numbers, examples and statements can be reproduced from primary sources and by independent software, and where does the current software differ from the book?"
VERSION = "1_0_0"
CQS = ("Which examples, figures and statements of the chapter can be reproduced by execution, and by independent software, and what does the execution give?",
       "What in the chapter differs from primary sources or from Bitcoin Core as it is now, and on what source?")
LABELS = {'PublicKeyCryptography': 'Public key cryptography', 'PrivateKey': 'Private key', 'PublicKey': 'Public key', 'Secp256k1': 'The secp256k1 curve',
          'PointMultiplication': 'Elliptic curve multiplication', 'CompressedPublicKey': 'Compressed public key', 'UncompressedPublicKey': 'Uncompressed public key',
          'WalletImportFormat': 'Wallet import format (WIF)', 'Base58Check': 'Base58check encoding', 'VersionPrefix': 'Version prefix', 'Commitment': 'Hash commitment (HASH160)',
          'P2pkhAddress': 'P2PKH address', 'P2shAddress': 'P2SH address', 'Bech32Address': 'Bech32 address', 'Bech32mAddress': 'Bech32m address', 'WitnessProgram': 'Witness program',
          'ErrorDetection': 'Error detection', 'DefaultAddressType': 'Default address type', 'KeyExport': 'Exporting a single key', 'VanityAddress': 'Vanity address', 'PaperWallet': 'Paper wallet',
          'TestVectors': 'BIP350 test vectors', 'DecentralizedIdentifier': 'Decentralized identifier (DID)', 'KeyControlProof': 'Proof of control by a key',
          'KeyPair': 'Key pair', 'Curve': 'The curve', 'KeyEncoding': 'Key encoding', 'Checksummed': 'Checksummed text', 'Legacy': 'Legacy addresses', 'Segwit': 'Segwit addresses',
          'Modern': 'Practice now', 'Assurance': 'Assurance', 'Identifiers': 'Identifiers', 'RandomSource': 'Randomness', 'PassphraseProtection': 'Passphrase-protected key'}
PUBS = [
 ("P01", "Mastering Bitcoin, 3rd edition - Chapter 4, Keys and Addresses (Antonopoulos and Harding, O'Reilly, 2023; CC BY-SA 4.0; tag third_edition_print1)", "https://raw.githubusercontent.com/bitcoinbook/bitcoinbook/third_edition_print1/ch04_keys.adoc", True),
 ("P02", "SEC 2: Recommended Elliptic Curve Domain Parameters, version 2.0, Standards for Efficient Cryptography (Certicom Research, 2010)", "https://www.secg.org/sec2-v2.pdf", False),
 ("P03", "BIP173 and BIP350: Base32 address format and Bech32m, the BIPs repository (Wuille, 2020), Status lines and test vectors", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0350.mediawiki", False),
 ("P04", "sipa/bech32 reference implementation for Python, segwit_addr.py, the code the book runs (Wuille, 2020)", "https://raw.githubusercontent.com/sipa/bech32/master/ref/python/segwit_addr.py", False),
 ("P05", "Bitcoin Core 31.1 release, downloaded, checked against its checksums and signatures, and run as an offline node: descriptors, address validation and wallet addresses (Bitcoin Core, 2026); evidence in 08-tooling/ch03-evidence and ch04-evidence", "https://bitcoincore.org/bin/bitcoin-core-31.1/", False),
 ("P06", "Bitcoin Core 30.0 release notes: legacy wallet RPCs removed, among them dumpprivkey and importprivkey (Bitcoin Core, 2026)", "https://raw.githubusercontent.com/bitcoin/bitcoin/05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940/doc/release-notes/release-notes-30.0.md", False),
 ("P07", "Bitcoin network hash rate, mempool.space API, read 2026-09-28 (Mempool Space, 2026), a third party's estimate", "https://mempool.space/api/v1/mining/hashrate/3m", False),
 ("P08", "Decentralized Identifiers (DIDs) v1.0, W3C Recommendation, 19 July 2022 (World Wide Web Consortium, 2022)", "https://www.w3.org/TR/did-core/", False),
 ("P09", "Python 3.14.4 documentation source: the secrets module, Doc/library/secrets.rst at the tag v3.14.4 (Python Software Foundation, 2026)", "https://raw.githubusercontent.com/python/cpython/v3.14.4/Doc/library/secrets.rst", False),
 ("P10", "BIP38: Passphrase-protected private key, the BIPs repository (Caldwell, 2012)", "https://raw.githubusercontent.com/bitcoin/bips/master/bip-0038.mediawiki", False),
 ("P_NOTES", "Course notes: Chapter_4_KeysAddresses.pptx, SEN0401 (then CSE0469) Blockchain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; the owner's file in 03-materials/owner-legacy-2025 (sha256 c390329c7a065303)", "urn:sen0401:course-notes:Chapter_4_KeysAddresses.pptx:c390329c7a065303", False),
]
SEC = ("Keys and Addresses", "Public Key Cryptography", "Private Keys", "Elliptic Curve Cryptography Explained", "Public Keys", "Output and Input Scripts",
       "IP Addresses: The Original Address for Bitcoin (P2PK)", "Legacy Addresses for P2PKH", "Base58check Encoding", "Compressed Public Keys",
       "Legacy Pay to Script Hash (P2SH)", "Bech32 Addresses", "Problems with Bech32 Addresses", "Bech32m", "Private Key Formats", "Compressed Private Keys",
       "Advanced Keys and Addresses", "Vanity Addresses", "Paper Wallets")
CONCEPTS = [("Section", x) for x in SEC] + [("Concept", x) for x in (
    "public key", "private key", "key pair", "entropy", "secp256k1", "generator point", "point at infinity", "elliptic curve multiplication", "output script", "input script",
    "P2PK", "P2PKH", "commitment", "SHA256", "RIPEMD-160", "HASH160", "base58", "checksum", "version prefix", "compressed public key", "uncompressed public key", "P2SH",
    "redeem script", "collision attack", "preimage attack", "bech32", "bech32m", "witness version", "witness program", "human-readable part", "WIF", "WIF-compressed",
    "vanity address", "paper wallet")]
FINDINGS = [
 ("F1", "Background", "Chapter 4 follows a payment's receiver from the private key, a random number, to the public key by elliptic curve multiplication, to the ways a public key becomes something a payer can type: the original pay to public key, the P2PKH commitment in base58check, compressed keys, P2SH, and the bech32 and bech32m segwit addresses, with private key formats, vanity addresses and paper wallets at the end.", ["P01"]),
 ("F2", "Comparative analysis", "The chapter's worked example reproduces in full, and from three independent directions: for the private key 1E99...AEDD a Python toolkit written for this chapter gives the book's public key coordinates, its compressed and uncompressed forms, both P2PKH addresses and both WIF strings; Bitcoin Core 31.1 gives the same two addresses from the public keys and from the WIF strings through descriptors and validates every address the chapter prints; and the book's own bech32 reference library gives its four segwit addresses, as does the toolkit, which also passes all 8 valid and 15 invalid BIP350 segwit vectors.", ["P01", "P05", "P04", "P03"]),
 ("F3", "Comparative analysis", "One statement in the chapter does not match its primary source: the book says secp256k1 was established by the National Institute of Standards and Technology, but the curve is defined in SEC 2 of the Standards for Efficient Cryptography, published by Certicom Research, and that document's Table 2 marks secp256k1 as not among the NIST-recommended curves while secp256r1 is.", ["P01", "P02"]),
 ("F4", "Comparative analysis", "The chapter's vanity-address table is exact in its frequencies from one to ten characters and gives 23 quintillion for eleven where 58 to the eleventh is 25 quintillion; its search times follow the rule average time equals half the frequency over 100,000 keys a second for patterns up to seven characters and are about a third shorter than that rule gives from eight characters on: 13 to 18 years against 20, 800 years against 1,180, 46,000 against 68,000 and 2.5 million against 4.0 million.", ["P01"]),
 ("F5", "Contemporary developments", "The bech32 family the chapter presents is now deployed: the BIPs repository gives BIP173 and BIP350 the status Deployed, Bitcoin Core 31.1 hands out bech32 P2WPKH addresses by default, bech32m taproot addresses on request, and validates the chapter's typo and length-extension examples as the book describes, locating the two typing errors at positions 25 and 40 and refusing all six strings that carry only a bech32 checksum after a version 1 witness.", ["P03", "P05", "P01"]),
 ("F6", "Contemporary developments", "The wallet the owner's notes drive with getnewaddress and dumpprivkey has changed: the 31.1 release still creates addresses but no longer knows dumpprivkey or importprivkey, which the 30.0 release notes list among the removed legacy wallet RPCs, and its default address is a bech32 P2WPKH address rather than the 1J7... address of the notes; a single WIF key can still be turned into an address through a descriptor such as pkh(WIF).", ["P05", "P06", "P_NOTES"]),
 ("F7", "Comparative analysis", "The bech32 error guarantees the chapter cites hold on the book's own P2WPKH address: none of its 39-character data part's one-character substitutions, none of its two-character substitutions and none of 200,000 random three- and four-character substitutions still carries a valid checksum, and the six length-extension strings the chapter prints carry a valid bech32 checksum and no valid bech32m checksum.", ["P01", "P03", "P05"]),
 ("F8", "Comparative analysis", "The chapter's collision-attack figures need updating to the network as it is: the book puts all miners at about 2 to the 80 hashes an hour in early 2023 and 2 to the 128 hashes at about 32 billion years, while a third party's estimate of the hash rate now is about 2.8 times that hourly figure and puts 2 to the 128 hashes at about 11 billion years.", ["P01", "P07"]),
 ("F9", "Course notes", "The owner's course notes for this chapter (2021, after the 2nd edition) add topics the 3rd edition's chapter no longer carries or treats differently, each checked: generating a private key with the operating system's random source, for which Python's documentation recommends the secrets module over the random module; the passphrase-protected key of BIP38, which the BIPs repository still marks Deployed but with the comment summary Unanimously Discourage for implementation; the Bitcoin Core commands getnewaddress and dumpprivkey (see the finding on the wallet); and vanity pools and paper wallets, which the 3rd edition keeps but calls obsolete or almost gone.", ["P_NOTES", "P09", "P10", "P05"]),
 ("F10", "Conclusion", "For the course theme, a key pair is an identifier whose holder can prove control without asking anyone, the property W3C's Decentralized Identifiers are designed around: a DID is a URI that associates a subject with a DID document that can carry cryptographic material such as verification methods, and its controller can prove control without permission from any other party.", ["P01", "P08"]),
]
TAX = [
 ("Keys", "KeyPair", "PublicKeyCryptography", "signatures, not secrecy", "Public key cryptography lets a private key produce a signature that anyone can check against the public key, which is what Bitcoin uses it for, not for encrypting transactions.", None),
 ("Keys", "KeyPair", "PrivateKey", "a random number below n", "A private key is a number picked at random between 1 and n minus 1, where n, about 1.1579 times 10 to the 77, is the order of the curve and slightly less than 2 to the 256.", ("0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 < 2**256", "True")),
 ("Keys", "KeyPair", "PublicKey", "K = k x G", "A public key is the point K = k x G obtained by multiplying the generator point by the private key, which is easy in one direction and infeasible to reverse.", None),
 ("Keys", "RandomSource", "SecureRandomness", "secrets rather than random", "A private key must come from a cryptographically secure random source; Python's secrets module is documented for that use and its random module for simulation.", None),
 ("Keys", "Curve", "Secp256k1", "y squared equals x cubed plus 7 over F(p)", "The secp256k1 curve, y squared = x cubed + 7 over the prime field with p = 2 to the 256 minus 2 to the 32 minus 977, is defined in SEC 2 by Certicom Research and is not a NIST-recommended curve.", ("2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1 == 2**256 - 2**32 - 977", "True")),
 ("Keys", "Curve", "PointMultiplication", "double and add", "Multiplying a point by a whole number k is adding it to itself k times, done in about 256 doublings and additions by the double-and-add method.", None),
 ("Format", "KeyEncoding", "CompressedPublicKey", "33 bytes: 02 or 03 and x", "A compressed public key keeps only x and one byte for the parity of y, 33 bytes instead of 65, and the y coordinate is recovered by solving the curve equation.", ("round(1 - 33 / 65, 3)", "0.492")),
 ("Format", "KeyEncoding", "UncompressedPublicKey", "65 bytes: 04, x and y", "An uncompressed public key is the prefix 04 followed by the x and y coordinates, 65 bytes, and it hashes to a different address than the compressed form of the same key.", None),
 ("Format", "KeyEncoding", "WalletImportFormat", "5J3m... and KxFC...", "The wallet import format is the base58check encoding of version byte 0x80 and the private key, with a 0x01 suffix for the compressed form, which changes the first character from 5 to K or L.", None),
 ("Format", "Checksummed", "Base58Check", "an alphabet without 0, O, l and I", "Base58check encodes a version byte, the data and the first four bytes of a double SHA-256 checksum in a 58-character alphabet that leaves out the characters easily mistaken for each other.", ("len('123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz')", "58")),
 ("Format", "Checksummed", "VersionPrefix", "0x00 gives 1, 0x05 gives 3", "The version byte makes the encoded text start with a recognisable character: 1 for a P2PKH address, 3 for P2SH, 5, K or L for a WIF key, and xpub for a BIP32 extended public key.", None),
 ("Address", "Legacy", "Commitment", "a hash of the public key", "A hash function output is a commitment to its input; Bitcoin commits to a public key with HASH160, the RIPEMD-160 of the SHA-256 of it, 20 bytes instead of 65.", ("__import__('hashlib').sha256(b'2007.  He said about a year and a half before Oct 2008\\n').hexdigest()", "'94d7a772612c8f2f2ec609d41f5bd3d04a5aa1dfe3582f04af517d396a302e4e'")),
 ("Address", "Legacy", "P2pkhAddress", "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "A P2PKH address is the base58check encoding of version 0x00 and the HASH160 of the public key, and a compressed and an uncompressed key give two different addresses.", None),
 ("Address", "Legacy", "P2shAddress", "3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM", "A P2SH address commits with HASH160 to a redeem script instead of a key, uses version byte 0x05 and starts with 3.", None),
 ("Address", "Segwit", "Bech32Address", "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee", "A bech32 address is a human-readable part, the separator 1, a witness version, a witness program and a six-character checksum, in one case of a 32-character alphabet.", ("len('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee')", "42")),
 ("Address", "Segwit", "Bech32mAddress", "bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7", "Bech32m differs from bech32 only in the constant merged into the checksum, 0x2bc830a3 instead of 1, and is required for witness version 1 and later.", ("hex(0x2bc830a3)", "'0x2bc830a3'")),
 ("Address", "Segwit", "WitnessProgram", "20 or 32 bytes for version 0", "The witness program is 2 to 40 bytes and, for witness version 0, exactly 20 or 32; for version 1, taproot, it is a 32-byte point.", None),
 ("Address", "Segwit", "ErrorDetection", "detects, and locates, typing errors", "Bech32 is guaranteed to detect any error affecting four characters or fewer, and Bitcoin Core points to where a typing error is, while bech32's original constant let a q be added before a final p without detection, which bech32m fixes.", None),
 ("Practice", "Modern", "DefaultAddressType", "bech32 by default, bech32m on request", "Bitcoin Core's addresstype option defaults to bech32, a P2WPKH address, and the four types are legacy, p2sh-segwit, bech32 and bech32m, the last a taproot address.", None),
 ("Practice", "Modern", "KeyExport", "no dumpprivkey any more", "Deterministic descriptor wallets no longer export single keys, and Bitcoin Core removed dumpprivkey and importprivkey in 30.0, while a WIF key can still be used inside a descriptor.", None),
 ("Practice", "Modern", "PassphraseProtection", "BIP38", "BIP38 encrypts a private key under a passphrase; the BIPs repository lists it as Deployed with the comment summary Unanimously Discourage for implementation, and the 3rd edition does not cover it.", None),
 ("Practice", "Modern", "VanityAddress", "1Kids and 58 to the fourth", "A vanity address starts with a chosen string found by trying keys one after another, and each further character multiplies the work by 58, so four characters take 58 to the fourth, about 11 million keys.", ("58**4", "11316496")),
 ("Practice", "Modern", "PaperWallet", "a private key on paper", "A paper wallet is a private key printed on paper, which the 3rd edition calls an obsolete technology and dangerous for most users.", None),
 ("Practice", "Assurance", "TestVectors", "BIP350's list of valid and invalid addresses", "The BIP350 test vectors give valid and invalid segwit addresses and bech32m strings against which any bech32m implementation should be run, including those for future witness versions.", None),
 ("Semantics", "Identifiers", "KeyControlProof", "signing to prove control", "Whoever holds a private key can prove control of the matching public key by signing, without a central registry or anyone's permission.", None),
 ("Semantics", "Identifiers", "DecentralizedIdentifier", "a DID and its DID document", "A decentralized identifier is a URI that associates a subject with a DID document that can carry verification methods such as public keys, so its controller can prove control without permission from another party.", None),
]
S = "Antonopoulos and Harding, 2023"; C = "Bitcoin Core, 2026"; CR = "Certicom Research, 2010"; WU = "Wuille, 2020"; M = "Mempool Space, 2026"; D = "World Wide Web Consortium, 2022"; PY = "Python Software Foundation, 2026"; CA = "Caldwell, 2012"
BODY = {
 "Keys": "Keys and Addresses begins with Alice paying Bob without the network learning who either is, using the scheme of the original paper in which a payment goes to a public key and is signed by the spender (%s)." % S,
 "KeyPair": "Public Key Cryptography and its subsections introduce the pair of a private and a public key (%s)." % S,
 "PublicKeyCryptography": "Asymmetric cryptography is not used to encrypt transactions: its useful property is that a private key produces a signature that anyone with the public key can verify, while only the private key's owner could have produced it (%s)." % S,
 "PrivateKey": "A private key is a number picked at random between 0 and n minus 1, where n, about 1.1578 times 10 to the 77 in the book, is the order of the curve, and it must come from a cryptographically secure random number generator (%s)." % S,
 "PublicKey": "The public key is K = k x G, the private key multiplied by the constant generator point of secp256k1, and for the book's example key it is the point whose x coordinate begins F028892B (%s)." % S,
 "RandomSource": "The chapter warns against writing your own random number code or using a simple generator, and asks for a cryptographically secure one with enough entropy (%s)." % S,
 "SecureRandomness": "Python's documentation says the secrets module generates cryptographically strong random numbers suitable for secrets and should be used in preference to the random module, which is designed for modelling and simulation (%s)." % PY,
 "Curve": "Elliptic Curve Cryptography Explained describes the curve Bitcoin uses and the arithmetic on its points (%s)." % S,
 "Secp256k1": "The book says secp256k1 was established by NIST, but the curve is defined in SEC 2 from Certicom Research, whose Table 2 lists it with no NIST recommendation and lists secp256r1 with one (%s)." % CR,
 "PointMultiplication": "Adding a point to itself is drawing a tangent and reflecting the third intersection, multiplication by k extends that addition, and the toolkit does it in about 256 doublings and additions for the book's key (%s)." % S,
 "Format": "Base58check Encoding, Compressed Public Keys and Private Key Formats describe how keys and hashes become text (%s)." % S,
 "KeyEncoding": "The same public key can be written in two forms and the same private key exported in two forms (%s)." % S,
 "CompressedPublicKey": "A compressed public key of 33 bytes carries the prefix 02 or 03 for the parity of y and the x coordinate, and the y coordinate is recovered from y squared = x cubed + 7 (%s)." % S,
 "UncompressedPublicKey": "The uncompressed key is 04 followed by x and y, 65 bytes, and hashing it gives a different commitment and so a different address from the compressed key of the same private key (%s)." % S,
 "WalletImportFormat": "The book's example private key exports as the WIF 5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn and, with the 01 suffix, as the WIF-compressed KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ (%s)." % S,
 "Checksummed": "Base58check adds a version byte and a checksum to data before encoding it (%s)." % S,
 "Base58Check": "Base58 is base64 without 0, O, l, I, plus and slash, and base58check appends the first four bytes of the double SHA-256 of the prefixed data as a checksum (%s)." % S,
 "VersionPrefix": "The version byte 0x00 gives an address starting with 1, 0x05 starts with 3, 0x80 gives a WIF starting with 5, K or L, and 0x0488B21E gives xpub (%s)." % S,
 "Address": "Legacy Addresses for P2PKH, Legacy Pay to Script Hash and Bech32 Addresses describe the ways a payer is given a receiver's script (%s)." % S,
 "Legacy": "The legacy address types use base58check and are two of the script templates Bitcoin supports (%s)." % S,
 "Commitment": "The book commits to an answer with a SHA-256 value beginning 94d7a772 and reveals it by hashing the sentence again, and Bitcoin commits to a public key the same way with RIPEMD-160 of its SHA-256 (%s)." % S,
 "P2pkhAddress": "For the book's key, the compressed public key gives the address 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy and the uncompressed one 1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x, and Bitcoin Core 31.1 derives the same two from the public keys (%s)." % C,
 "P2shAddress": "P2SH lets an output commit to a redeem script with HASH160, its address uses version 5 and starts with 3, and the book's example 3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM has a valid checksum (%s)." % S,
 "Segwit": "Bech32 Addresses, Problems with Bech32 Addresses and Bech32m describe the address format for segregated witness outputs (%s)." % S,
 "Bech32Address": "A bech32 address such as bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee is 42 characters for a 20-byte witness program and 62 for a 32-byte one, and the book's reference library and the toolkit both produce it from the script's program (%s)." % WU,
 "Bech32mAddress": "Bech32m changes the checksum constant from 1 to 0x2bc830a3 and is used from segwit version 1, so the taproot example bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7 carries a bech32m checksum (%s)." % WU,
 "WitnessProgram": "A witness program is 2 to 40 bytes, exactly 20 or 32 for version 0, and for version 1 the book's example is a 32-byte point on the secp256k1 curve (%s)." % S,
 "ErrorDetection": "Bitcoin Core validates the book's typo example as invalid with a bech32m checksum error at positions 25 and 40, the two characters the book underlines, and rejects the length-extension strings that carry only a bech32 checksum (%s)." % C,
 "Practice": "Vanity Addresses, Paper Wallets and the sections after them describe what is done with keys and addresses beyond the basics (%s)." % S,
 "Modern": "Some of that practice has changed in current software (%s)." % C,
 "DefaultAddressType": "Bitcoin Core 31.1 lists the address types legacy, p2sh-segwit, bech32 and bech32m and defaults to bech32, and a new wallet's default address is a version 0 witness address (%s)." % C,
 "KeyExport": "Bitcoin Core 30.0 removed the legacy wallet RPCs including dumpprivkey and importprivkey, and the 31.1 release answers that they are unknown commands (%s)." % C,
 "PassphraseProtection": "The BIPs repository lists BIP38, a passphrase-protected private key, as Deployed and carries the comment summary Unanimously Discourage for implementation (%s)." % CA,
 "VanityAddress": "Vanity addresses were popular early and are almost gone, and the book's table of search times is exact in frequency and consistent with its own rule up to seven characters (%s)." % S,
 "PaperWallet": "The book calls paper wallets an obsolete technology that is dangerous for most users and shows them only for information (%s)." % S,
 "Assurance": "An implementation of bech32m can be tested against published vectors (%s)." % WU,
 "TestVectors": "BIP350 publishes 8 valid and 15 invalid segwit address vectors and 7 valid bech32m strings, and the toolkit and the reference library both pass all of the address vectors (%s)." % WU,
 "Semantics": "The course theme of semantic technologies meets the chapter in what a key pair is: an identifier whose holder can prove control (%s)." % D,
 "Identifiers": "Keys and decentralized identifiers both name a subject and let its controller prove control (%s)." % D,
 "KeyControlProof": "A signature by the private key proves control of the public key and so of the funds or the identifier, without permission from a registry (%s)." % S,
 "DecentralizedIdentifier": "W3C's Decentralized Identifiers are URIs that associate a subject with a DID document that can express cryptographic material and verification methods, designed so a controller can prove control without permission from any other party (%s)." % D,
}
_TK = "exec(open('08-tooling/ch04-evidence/sen0401_keys_toolkit_v1_0_0.py').read())\nk = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD\nK = ec_mul(k)\n"
_EV = "08-tooling/ch04-evidence/"
_J = lambda f: "__import__('json').load(open('%s%s'))" % (_EV, f)
_T = lambda f: "open('%s%s').read()" % (_EV, f)
CLAIMS = [
 (_TK + "(K[0] == 0xF028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A, K[1] == 0x07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB)", "(True, True)"),
 ("(lambda p, x, y: (x ** 3 + 7 - y ** 2) % p)(115792089237316195423570985008687907853269984665640564039457584007908834671663, 55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)", "0"),
 (_TK + "(ec_mul(N) is None, ec_mul(N - 1) == (G[0], P - G[1]), G[1] ** 2 % P == (G[0] ** 3 + 7) % P)", "(True, True, True)"),
 (_TK + "(pub_bytes(K).hex(), len(pub_bytes(K)), len(pub_bytes(K, False)), pub_bytes(K, False).hex()[:2])", "('03f028892bad7ed57d2fb57bf33081d5cfcf6f9ed3d3d7f159c2e2fff579dc341a', 33, 65, '04')"),
 (_TK + "decompress(pub_bytes(K)) == K", "True"),
 (_TK + "(p2pkh(pub_bytes(K)), p2pkh(pub_bytes(K, False)), hash160(pub_bytes(K)) != hash160(pub_bytes(K, False)))", "('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy', '1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', True)"),
 (_TK + "(wif(k, False), wif(k), b58check_decode(wif(k))[0], b58check_decode(wif(k))[-1], len(b58check_decode(wif(k))), len(b58check_decode(wif(k, False))))", "('5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn', 'KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ', 128, 1, 34, 33)"),
 (_TK + "[b58check(b'\\x80' + bytes(32))[0], b58check(b'\\x80' + b'\\xff' * 32)[0], b58check(b'\\x80' + bytes(32) + b'\\x01')[0], b58check(b'\\x80' + b'\\xff' * 32 + b'\\x01')[0]]", "['5', '5', 'K', 'L']"),
 (_TK + "[b58check(bytes([v]) + bytes(20))[0] for v in (0x00, 0x05, 0xc4)] + [b58check(bytes([0x6f]) + bytes(20))[0], b58check(bytes([0x6f]) + b'\\xff' * 20)[0], b58check(bytes.fromhex('0488B21E') + bytes(74))[:4]]", "['1', '3', '2', 'm', 'n', 'xpub']"),
 (_TK + "(b58check_decode('3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM')[0], b58check_decode('1LoveBPzzD72PUXLzCkYAtGFYmK5vYNR33')[0], '1LoveBPzz'[:5])", "(5, 0, '1Love')"),
 (_TK + "(set('0OIl') & set(B58), len(B58), len(set(B58)))", "(set(), 58, 58)"),
 (_TK + "(lambda x: pow((x ** 3 + 7) % P, (P + 1) // 4, P) ** 2 % P == (x ** 3 + 7) % P)(0x2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311)", "True"),
 (_TK + "[len(segwit_address('bc', 0, bytes(20))), len(segwit_address('bc', 0, bytes(32))), len(segwit_address('bc', 1, bytes(32)))]", "[42, 62, 62]"),
 (_TK + "(BECH32, hex(BECH32M))", "(1, '0x2bc830a3')"),
 ("(lambda d: [d[k] for k in ('book_addresses_toolkit', 'book_addresses_sipa_library', 'bip350_valid_vectors', 'bip350_invalid_vectors', 'bip350_bech32m_strings', 'length_extension_bech32_valid', 'length_extension_bech32m_valid', 'core_validate_agrees_on_segwit_examples')])(%s)" % _J("verify_results_v1_0_0.json"), "[True, True, [8, 8], [15, 15], [6, 6], [6, 6], [0, 6], True]"),
 ("(lambda d: (d['one'], d['two'], d['three_or_four_random_of_200000'], d['data_characters']))(%s['substitution_errors_undetected'])" % _J("verify_results_v1_0_0.json"), "(0, 0, 0, 39)"),
 ("(lambda a, b, v: ([i for i, (x, y) in enumerate(zip(a, b)) if x != y], v[b]['error_locations'], v[b]['isvalid']))('bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7', 'bc1p9nh05ha8wrljf7ru236awn4t2x0d5ctkkywmv9sclnm4t0av2vgs4k3au7', %s)" % _J("core_validateaddress_31_1_v1_0_0.json"), "([25, 40], [25, 40], False)"),
 ("(lambda v: [v[a]['isvalid'] for a in v if a[:2] in ('1J', '14', '3F', '1L')] + [v[a]['isvalid'] for a in v if a.startswith('bc1') and a in ('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee', 'bc1sqqqqkfw08p')])(%s)" % _J("core_validateaddress_31_1_v1_0_0.json"), "[True, True, True, True, True, True]"),
 ("[l.split('=> ')[1] for l in %s.splitlines()]" % _T("core_deriveaddresses_31_1_v1_0_0.txt"), "['1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy', '1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', 'bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck', '3FyC6EYuxW22uj4CaEGjNCjxeg7gHyFeVv', 'bc1pyjqgwc0t990afumlh6m9hpmrh7pxd7x0nev83xvzqwvuyevymwgqtjhuxh', '1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x', '1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy', 'bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck']"),
 (_TK + "(segwit_address('bc', 0, hash160(pub_bytes(K))), p2sh(bytes([0, 20]) + hash160(pub_bytes(K))))", "('bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck', '3FyC6EYuxW22uj4CaEGjNCjxeg7gHyFeVv')"),
 ("(lambda d: {t: (v['desc_kind'], v['witness_version']) for t, v in d.items()})(%s)" % _J("core_wallet_addresses_31_1_v1_0_0.json"), "{'default': ('wpkh', 0), 'legacy': ('pkh', None), 'p2sh-segwit': ('sh', None), 'bech32': ('wpkh', 0), 'bech32m': ('tr', 1)}"),
 ("'default: \"bech32\"' in ' '.join(%s.split())" % _T("core_help_addresstype_31_1_v1_0_0.txt"), "True"),
 ("[l.split(': ', 1)[1] for l in %s.splitlines()]" % _T("core_removed_rpcs_31_1_v1_0_0.txt"), "['help: unknown command: dumpprivkey', 'help: unknown command: importprivkey']"),
 ("[l.split()[:1] + l.split()[7:8] for l in %s.splitlines() if l.startswith('secp256')]" % _T("sec2_table2_v1_0_0.txt"), "[['secp256k1', '-'], ['secp256r1', 'r']]"),
 ("%s.splitlines()" % _T("bip_status_v1_0_0.txt"), "['BIP: 173', 'Title: Base32 address format for native v0-16 witness outputs', 'Status: Deployed', 'BIP: 350', 'Title: Bech32m format for v1+ witness addresses', 'Status: Deployed']"),
 ("(lambda hr: (round(hr * 3600 / 2**80, 1), round(2**128 / hr / 31_557_600 / 1e9), round(2**128 / (2**80 / 3600) / 31_557_600 / 1e9)))(%s['currentHashrate'])" % _J("hashrate_v1_0_0.json"), "(2.8, 11, 32)"),
 ("[(n, 58**n) for n in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)][-1]", "(11, 24986644000165537792)"),
 ("[round(58**n / 2 / 100_000 / 31_557_600, 1) for n in (8, 9, 10, 11)]", "[20.3, 1176.8, 68256.8, 3958894.8]"),
 ("[round(58**n / 2 / 100_000 / 86400, 1) for n in (4, 5, 6, 7)]", "[0.0, 0.0, 2.2, 127.8]"),
 ("[round(58**n / 1e6, 3) for n in (2, 3, 4)] + [58**29 > 1.3e51, 58**29 < 1.4e51 * 1.001]", "[0.003, 0.195, 11.316, True, True]"),
 ("'prove control' in ' '.join(%s.split())" % _T("did_core_abstract_v1_0_0.txt"), "True"),
 ("__import__('subprocess').run(['python3', '-c', 'import secrets; N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141; k = secrets.randbelow(N - 1) + 1; print(0 < k < N)'], capture_output=True, text=True).stdout.strip()", "'True'"),
]
BEH = [
 ("pow(a, -1, p) is the modular inverse the curve arithmetic needs", "p = 97\nprint(all(a * pow(a, -1, p) % p == 1 for a in range(1, p)))", "True"),
 ("the y coordinate of a point on a curve with p = 3 mod 4 is a modular square root computed by one exponentiation", "P = 2**256 - 2**32 - 977\nprint(P % 4)", "3"),
]
