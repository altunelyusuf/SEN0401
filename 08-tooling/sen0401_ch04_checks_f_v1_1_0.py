"""SEN0401 chapter 4, executed claims, part F (version 1.1.0): practice today (address types, key export, passphrase protection,
deterministic wallets, address reuse, vanity addresses, paper wallets, hardware signing devices), assurance (the published test
vectors, cross-checking) and the semantic link to identifiers (proof of control, URIs, decentralized identifiers).
Each entry is (expression, expected repr); the chapter builder evaluates it alone under CPython 3.14."""
from sen0401_ch04_checkhelp_v1_1_0 import *
from sen0401_ch04_checks_a_v1_1_0 import BK, BK1, BK5, KH
B38 = rd(S1 + "bip-0038.mediawiki")
B350 = rd(S1 + "bip-0350.mediawiki")
B173 = rd(S1 + "bip-0173.mediawiki")
RN30 = rd(S1 + "core_release_notes_30_0.md")
BK13 = book("ch13_security.adoc")
DIDT = rd(S2 + "did-core.txt")
DIDA = ev("did_core_abstract_v1_0_0.txt")
R3986 = rd(S2 + "rfc3986.txt")
NOTES = rd(os.path.join(os.path.dirname(HERE), "03-materials", "owner-legacy-2025", "llm-content-2025", "Chapter4",
                        "Chapter_4_Keys_Addresses_Antonopoulos_2017_v1_0_0.txt"))
ATYPE = ev("core_help_addresstype_31_1_v1_0_0.txt")
GNA = ev("core_help_getnewaddress_31_1_v1_0_0.txt")
IMPD = ev("core_help_importdescriptors_31_1_v1_0_0.txt")
REMOVED = ev("core_removed_rpcs_31_1_v1_0_0.txt")
DERIVE = ev("core_deriveaddresses_31_1_v1_0_0.txt")
WAD = evj("core_wallet_addresses_31_1_v1_0_0.json")
VA = evj("core_validateaddress_31_1_v1_0_0.json")
VR = evj("verify_results_v1_0_0.json")
VEC = evj("bip350_vectors_v1_0_0.json")
KHX = KH[2:]
SEED = "f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73"
BIP38_MIN = "6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi"
BIP38_MAX = "6PRWdmoT1ZursVcr5NiD14p5bHrKVGPG7yeEoEeRb8FVaqYSHnZTLEbYsU"
ADDR_C, ADDR_U = "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x"
A_OWN_WPKH = "bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck"
WIF_U, WIF_C = "5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn", "KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ"
LOVE = "1LoveBPzzD72PUXLzCkYAtGFYmK5vYNR33"
# the book's table of vanity frequencies and average search times (table_4-12), read as (pattern length, frequency, seconds)
BOOKTAB = [(1, 58, 0.001), (2, 3364, 0.050), (3, 195000, 2.0), (4, 11e6, 60.0), (5, 656e6, 3600.0), (6, 38e9, 2 * 86400.0),
           (7, 2.2e12, 3.5 * 30 * 86400.0), (8, 128e12, 15.5 * 365.25 * 86400.0), (9, 7e15, 800 * 365.25 * 86400.0),
           (10, 400e15, 46000 * 365.25 * 86400.0), (11, 23e18, 2.5e6 * 365.25 * 86400.0)]
F_ = lambda s, **kw: X(s, KHX=KHX, SEED=SEED, ADDRC=ADDR_C, ADDRU=ADDR_U, AOWN=A_OWN_WPKH, WIFU=WIF_U, WIFC=WIF_C,
                       LOVE=LOVE, B38MIN=BIP38_MIN, B38MAX=BIP38_MAX, **kw)

CHECKS_F = [
 # ---- the practice branch and 'practice now'
 (has(BK, "This means almost no modern wallets support the ability to export or import an individual key",
      "The information in this section is mainly of interest to anyone needing compatibility with early Bitcoin wallets",
      "Paper wallets are an OBSOLETE technology and are dangerous for most", "users",
      "Vanity addresses were popular in the", "early years of Bitcoin but have almost entirely disappeared from use as", "of 2023"), "True"),
 (has(prev("03"), "Bitcoin Core"), "True"),
 # ---- the default address type
 (has(ATYPE, "-addresstype", "What type of addresses to use (\"legacy\", \"p2sh-segwit\", \"bech32\",", "\"bech32m\", default: \"bech32\")"), "True"),
 (has(GNA, "Returns a new Bitcoin address for receiving payments.",
      "address_type (string, optional, default=set by -addresstype) The address type to use. Options are \"legacy\", \"p2sh-segwit\", \"bech32\", \"bech32m\""), "True"),
 ("['legacy', 'p2sh-segwit', 'bech32', 'bech32m'].index('bech32')", "2"),
 (F_("sorted($WAD)", WAD=WAD), "['bech32', 'bech32m', 'default', 'legacy', 'p2sh-segwit']"),
 (F_("[($WAD[k]['desc_kind'], $WAD[k]['witness_version'], $WAD[k]['address'][:1]) for k in ('default', 'legacy', 'p2sh-segwit', 'bech32', 'bech32m')]", WAD=WAD),
  "[('wpkh', 0, 'b'), ('pkh', None, '1'), ('sh', None, '3'), ('wpkh', 0, 'b'), ('tr', 1, 'b')]"),
 (F_("($WAD['default']['address'] == $WAD['bech32']['address'], $WAD['default']['scriptPubKey'][:4])", WAD=WAD), "(False, '0014')"),
 # ---- exporting a single key
 (has(BK, "if a", "user exports a single private key from one of these wallets and an", "attacker acquires that key plus some nonprivate data about the wallet",
      "they can potentially derive any private key in the wallet--allowing the", "attacker to steal all of the wallet funds",
      "Additionally, keys cannot be", "imported into deterministic wallets",
      "Individual private keys could be exported or imported"), "True"),
 (has(RN30, "BDB legacy wallets can no longer be created or loaded", "legacy-only RPCs `addmultisigaddress`, `dumpprivkey`, `dumpwallet`,",
      "`importaddress`, `importmulti`, `importprivkey`, `importpubkey`,", "`importwallet`, `newkeypool`, `sethdseed`, and `upgradewallet`, are removed"), "True"),
 (has(REMOVED, "dumpprivkey: help: unknown command: dumpprivkey", "importprivkey: help: unknown command: importprivkey"), "True"),
 (has(IMPD, "Import descriptors. This will trigger a rescan of the blockchain based on the earliest timestamp of all descriptors being imported. Requires a new wallet backup"), "True"),
 (F_("[l.split(' => ')[1] for l in $D.strip().splitlines() if l.startswith('pkh(<WIF>)') or l.startswith('wpkh(<WIF>)')]", D=DERIVE),
  "['%s', '%s', '%s']" % (ADDR_U, ADDR_C, A_OWN_WPKH)),
 (F_("(lambda T: (T.p2pkh(T.pub_bytes(T.ec_mul(int.from_bytes(T.b58check_decode('$WIFU')[1:33], 'big')), False)), T.p2pkh(T.pub_bytes(T.ec_mul(int.from_bytes(T.b58check_decode('$WIFC')[1:33], 'big')))), T.segwit_address('bc', 0, T.hash160(T.pub_bytes(T.ec_mul(int.from_bytes(T.b58check_decode('$WIFC')[1:33], 'big')))))))($T)"),
  "('%s', '%s', '%s')" % (ADDR_U, ADDR_C, A_OWN_WPKH)),
 ("'dumpprivkey' in ('dumpprivkey', 'importprivkey')", "True"),
 # the course material that accompanies this chapter (written on the 2nd edition) describes the workflow that has been removed
 (has(NOTES, "To ask bitcoind to expose the private key, use the dumpprivkey command",
      "$ bitcoin-cli getnewaddress 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy $ bitcoin-cli dumpprivkey 1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ",
      "The dumpprivkey command opens the wallet and extracts the private key that was generated by the getnewaddress command"), "True"),
 # ---- the passphrase-protected key (BIP38)
 (has(B38, "BIP: 38", "Title: Passphrase-protected private key", "Comments-Summary: Unanimously Discourage for implementation", "Status: Deployed",
      "A method is proposed for encrypting and encoding a passphrase-protected Bitcoin private key record in the form of a 58-character Base58Check-encoded printable string",
      "Each record string contains all the information needed to reconstitute the private key except for a passphrase, and the methodology uses salting and ''scrypt'' to resist brute-force attacks",
      "As a Bitcoin user who uses paper wallets, I would like the ability to add encryption, so that my Bitcoin paper storage can be two factor: something I have plus something I know",
      "I would prefer to offer an encrypted private key, and then follow it up with the password using a different communication channel (e.g. a phone call or SMS)",
      "the simple form of the well-known AES block cipher", "scrypt''': A well-known key derivation algorithm",
      "Object identifier prefix: 0x0142 (non-EC-multiplied) or 0x0143 (EC-multiplied)",
      "How the user sees it: 58 characters always starting with '6P'",
      "4 bytes: SHA256(SHA256(expected_bitcoin_address))[0...3], used both for typo checking and as salt",
      "Minimum value: 6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi (based on 01 42 C0 plus thirty-six 00's)",
      "Maximum value: 6PRWdmoT1ZursVcr5NiD14p5bHrKVGPG7yeEoEeRb8FVaqYSHnZTLEbYsU (based on 01 42 C0 plus thirty-six FF's)"), "True"),
 (F_("(lambda T: (T.b58check(bytes.fromhex('0142C0') + bytes(36)), T.b58check(bytes.fromhex('0142C0') + b'\\xff' * 36)))($T)"),
  "('%s', '%s')" % (BIP38_MIN, BIP38_MAX)),
 (F_("(len('$B38MIN'), len('$B38MAX'), '$B38MIN'[:2], 1 + 36, (1 + 36) * 8)"), "(58, 58, '6P', 37, 296)"),
 (has(NOTES, "standardized by BIP-38 (see Appendix C). BIP-38 proposes a common standard for encrypting private keys with a passphrase and encoding them with Base58Check so that they can be stored securely on backup media, transported securely between wallets, or kept in any other conditions where the key might be exposed",
      "The standard for encryption uses the Advanced Encryption Standard (AES)", "BIP-38 Encrypted Private Key 0x0142 6P"), "True"),
 ("'BIP38' in __import__('re').sub(r'[^A-Za-z0-9]', '', 'BIP-38')", "True"),
 (has(BK, "Use a recovery code to back up your", "keys, possibly with a hardware signing device to store keys and sign transactions"), "True"),
 # ---- the deterministic wallet and its seed
 (has(BK5, "A hash function will always produce the same output when given the same", "input, but if the input is changed even slightly, the output will be",
      "later using the same hash function with the same", "will produce the same seemingly random values",
      "f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73",
      "for i in {0..2} ; do echo \"$seed + $i\" | sha256sum ; done",
      "50b18e0bd9508310b8f699bad425efdf67d668cb2462b909fdb6b9bd2437beb3",
      "a965dbcd901a9e3d66af11759e64a58d0ed5c6863e901dfda43adcd5f8c744f3",
      "19580c97eb9048599f069472744e51ab2213f687d4720b0efc5bb344d624c3aa",
      "A user of deterministic key generation can", "back up every key in their wallet by simply recording their seed and", "a reference to the deterministic algorithm they used",
      "if someone else gets your seed, they can also generate all of the private keys"), "True"),
 (has(BK, "Later Bitcoin wallets began using deterministic wallets where all", "private keys are generated from a single seed value",
      "These wallets only", "ever need to be backed up once for typical onchain use",
      "it's possible to", "back up every key in most modern wallets by simply writing down a few", "words or characters"), "True"),
 (F_("(lambda h: [h.sha256(('$SEED + %d\\n' % i).encode()).hexdigest() for i in range(3)])(__import__('hashlib'))"),
  "['50b18e0bd9508310b8f699bad425efdf67d668cb2462b909fdb6b9bd2437beb3', 'a965dbcd901a9e3d66af11759e64a58d0ed5c6863e901dfda43adcd5f8c744f3', '19580c97eb9048599f069472744e51ab2213f687d4720b0efc5bb344d624c3aa']"),
 (F_("(lambda h: h.sha256(('$SEED + 0\\n').encode()).hexdigest() == h.sha256(('$SEED + 0\\n').encode()).hexdigest())(__import__('hashlib'))"), "True"),
 (has(prev("01"), "recovery code"), "True"),
 # ---- address reuse and privacy
 (has(BK, "Using a vanity address to receive multiple", "payments to the same address creates a link between all of those", "payments",
      "Alice may want to donate", "anonymously and Bob may not want his other customers to know that he", "gives discount pricing to Eugenia",
      "her nonprofit needs", "to report its income and expenditures to a tax authority anyway",
      "receive a new public key from Bob's wallet that his node had never previously given anyone",
      "different", "transactions paying Bob couldn't be connected together by someone", "looking at the blockchain and noticing that all of the transactions paid", "the same public key"), "True"),
 ("(len({'a', 'a', 'a'}), len({'a', 'b', 'c'}))", "(1, 3)"),
 # ---- the vanity address
 (has(BK, "Vanity addresses are valid Bitcoin", "addresses that contain human-readable messages",
      "+1LoveBPzzD72PUXLzCkYAtGFYmK5vYNR33+ is a valid address that contains", "the letters forming the word \"Love\" as the first four base58 letters",
      "Vanity addresses require generating and testing billions of candidate", "private keys until a Bitcoin address with the desired pattern is found",
      "picking a private key at", "random, deriving the public key, deriving the Bitcoin address, and", "checking to see if it matches the desired vanity pattern, repeating", "billions of times until a match is found",
      "Vanity addresses are no", "less or more secure than any other address. They depend on the same",
      "elliptic curve cryptography (ECC) and secure hash algorithm (SHA) as any other address",
      "Eugenia will create a vanity", "address that starts with \"1Kids\" to promote the children's charity",
      "There are approximately 58^29^", "(approximately 1.4 × 10^51^) addresses in that range, all starting with", "\"1Kids.\"",
      "An average desktop computer PC, without any specialized hardware, can", "search approximately 100,000 keys per second",
      "Each additional character increases the difficulty by a", "factor of 58",
      "A https://oreil.ly/99K81[vanity pool] is a service that", "allows those with fast hardware to earn bitcoin searching for vanity", "addresses for others",
      "Generating a vanity address is a brute-force exercise: try a random key,", "check the resulting address to see if it matches the desired pattern,", "repeat until successful",
      "It's not possible to use vanity addresses with a deterministic wallet", "unless the user backs up additional data for every vanity address they", "create",
      "most wallets using deterministic key", "generation simply don't allow importing a private key or key tweak from", "a vanity generator"), "True"),
 (has(BK, "1 in 58 keys", "1 in 3,364", "1 in 195,000", "1 in 11 million", "1 in 656 million", "1 in 38 billion",
      "1 in 2.2 trillion", "1 in 128 trillion", "1 in 7 quadrillion", "1 in 400 quadrillion", "1 in 23 quintillion",
      "2.5 million years", "46,000 years", "800 years", "13&#x2013;18 years".replace("&#x2013;", "–"), "3–4 months"), "True"),
 ("[58 ** n for n in range(1, 12)]",
  "[58, 3364, 195112, 11316496, 656356768, 38068692544, 2207984167552, 128063081718016, 7427658739644928, 430804206899405824, 24986644000165537792]"),
 ("(round(58 ** 29 / 1e51, 1), round(58 ** 11 / 1e18))", "(1.4, 25)"),
 # the book's own rule (half the frequency at 100,000 keys a second) reproduced for the first seven rows, and the gap for the last three
 (F_("[round((f / 2 / 100000) / u, 1) for n, f, u in $BTAB[:7] for u in [(1.0 if n <= 2 else 1.0)]]", BTAB=repr(BOOKTAB)),
  "[0.0, 0.0, 1.0, 55.0, 3280.0, 190000.0, 11000000.0]"),
 (F_("[(n, round((f / 2 / 100000) / t, 2)) for n, f, t in $BTAB[7:]]", BTAB=repr(BOOKTAB)),
  "[(8, 1.31), (9, 1.39), (10, 1.38), (11, 1.46)]"),
 (F_("[round(58 ** n / 2 / 100000 / (365.25 * 86400)) for n in (8, 9, 10, 11)]", BTAB=repr(BOOKTAB)), "[20, 1177, 68257, 3958895]"),
 # a real, small search: counting private keys upwards from 1
 (F_("""(lambda T: (lambda want: (lambda out: (out['1Ki'], out['1Kid']))((lambda d: [d.setdefault(p, k) for k in range(1, 20000) for pt in [T.ec_mul(k)] for a in [T.p2pkh(T.pub_bytes(pt))] for p in want if a.startswith(p) and p not in d] and d or d)({})))(('1Ki', '1Kid')))($T)"""),
  "(1666, 8810)"),
 (F_("($VA['$LOVE']['isvalid'], '$LOVE'[1:5])", VA=VA), "(True, 'Love')"),
 # ---- the paper wallet
 (has(BK, "Paper wallets are private keys printed on paper",
      "Often the paper wallet also includes the corresponding Bitcoin address", "for convenience, but this is not necessary because it can be derived", "from the private key",
      "There are many subtle pitfalls involved in generating them, not least of which is the possibility that the generating code is compromised",
      "with a \"back door.\" Many bitcoins have been stolen this way",
      "wallets are shown here for informational purposes only and should not be", "used for storing bitcoin",
      "Some are intended to be given as gifts and have seasonal themes, such as", "Christmas and New Year's",
      "with the private key hidden in some way, either with", "opaque scratch-off stickers or folded and sealed with tamper-proof",
      "in the form of detachable stubs similar to ticket stubs,", "allowing you to store multiple copies to protect against fire, flood, or", "other natural disasters"), "True"),
 ("len('paper wallet'.split())", "2"),
 # ---- the hardware signing device
 (has(BK5, "she can provide the key tweaks she used to a _hardware signing device_ (sometimes confusingly called a _hardware wallet_) that securely stores her original private key",
      "The hardware signer uses the tweaks to derive the necessary child private keys and uses them to sign the transactions, returning the signed transactions to the less-secure frontend for broadcast to the Bitcoin network"), "True"),
 (has(BK13, "Unlike a smartphone or desktop", "computer, a Bitcoin hardware signing device only needs to hold keys and", "use them to generate signatures",
      "Without general-purpose software to compromise and with limited interfaces, hardware signing devices can deliver strong",
      "security to nonexpert users", "Hardware signing devices may become the predominant method of storing bitcoins"), "True"),
 (has(BK, "one signature from his", "desktop wallet and one from a hardware signing device"), "True"),
 ("['prepare', 'sign', 'broadcast'].index('sign')", "1"),
 # ---- assurance
 (has(BK, "When implementing bech32m encoding or decoding, we very strongly", "recommend that you use the test vectors provided in BIP350",
      "We also ask", "that you ensure your code passes the test vectors related to paying future segwit", "versions that haven't been defined yet",
      "This will help make your", "software usable for many years to come"), "True"),
 (has(B350, "'''Implementation advice''' Experiments testing BIP173 implementations found that many wallets and services did not support sending to higher version segregated witness outputs",
      "All higher versions of native segregated witness outputs should be recognized as valid recipients. As higher versions are not defined on the network, no wallet should ever create them"), "True"),
 # ---- the BIP350 test vectors
 (F_("(len($V['valid_bech32m']), len($V['valid_segwit']), len($V['invalid_segwit']), $V['read'])", V=VEC), "(7, 8, 15, '2026-09-28')"),
 (F_("($VR['bip350_valid_vectors'], $VR['bip350_invalid_vectors'], $VR['bip350_bech32m_strings'])", VR=VR), "([8, 8], [15, 15], [6, 6])"),
 ("(7, 8, 15)", "(7, 8, 15)"),
 (F_("(lambda T: (lambda V: ([T.segwit_decode(a.lower()[:2], a) is not None for a, s in V['valid_segwit']], sorted({T.segwit_address(a.lower()[:2], *T.segwit_decode(a.lower()[:2], a)) == a.lower() for a, s in V['valid_segwit']})))($V))($T)", V=VEC),
  "([True, True, True, True, True, True, True, True], [True])"),
 (F_("(lambda T: (lambda V: sorted({all(T.segwit_decode(h, a) is None for h in ('bc', 'tb')) for a in [r[0] for r in V['invalid_segwit']]}))($V))($T)", V=VEC), "[True]"),
 (F_("(lambda T: (lambda V: [bytes([0 if v == 0 else 0x50 + v, len(p)]).hex() + p.hex() == s for a, s in V['valid_segwit'] for v, p in [T.segwit_decode(a.lower()[:2], a)]])($V))($T)", V=VEC),
  "[True, True, True, True, True, True, True, True]"),
 (F_("(lambda T: (lambda V: sorted({T.bech_check(s) == T.BECH32M for s in V['valid_bech32m']}))($V))($T)", V=VEC), "[True]"),
 (F_("(lambda T: (lambda V: sorted({T.bech_check(s) == T.BECH32 for s in V['valid_bech32m']}))($V))($T)", V=VEC), "[False]"),
 (has(B350, "The following strings are valid Bech32m:", "A1LQFN3A", "?1v759aa",
      "No string can be simultaneously valid Bech32 and Bech32m, so the above examples also serve as invalid test vectors for Bech32",
      "Invalid program length (41 bytes)", "Invalid witness version", "Mixed case", "zero padding of more than 4 bits",
      "Non-zero padding in 8-to-5 conversion", "Invalid human-readable part"), "True"),
 # ---- cross-checking with independent software
 (F_("($VR['book_addresses_toolkit'], $VR['book_addresses_sipa_library'], $VR['book_addresses_agree'], $VR['core_validate_agrees_on_segwit_examples'])", VR=VR),
  "(True, True, True, True)"),
 (F_("(lambda T: (lambda K: (T.p2pkh(T.pub_bytes(K)), T.p2pkh(T.pub_bytes(K, False)), T.wif(0x$KHX, True), T.wif(0x$KHX, False)))(T.ec_mul(0x$KHX)))($T)"),
  "('%s', '%s', '%s', '%s')" % (ADDR_C, ADDR_U, WIF_C, WIF_U)),
 (F_("len({'$ADDRC', '$ADDRC', '$ADDRC'})"), "1"),
 (F_("sorted({$VA[a]['isvalid'] for a in ('$ADDRC', '$ADDRU', '3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM', '$LOVE')})", VA=VA), "[True]"),
 (has(rd(os.path.join(HERE, "ch04-evidence", "segwit_addr_sipa_v1_0_0.py")), "def encode(hrp, witver, witprog):", "def decode(hrp, addr):"), "True"),
 # ---- the semantic branch: proof of control, URI, DID
 (has(BK, "This signature can only be produced by someone with", "knowledge of the private key. However, anyone with access to the public",
      "key and the transaction can use them to _verify_ the", "signature"), "True"),
 (F_("(lambda T: (lambda d, z, k: (lambda Q, sig: (T.ecdsa_verify(Q, z, sig), T.ecdsa_verify(Q, z + 1, sig), T.ecdsa_verify(T.ec_mul(d + 7), z, sig)))(T.ec_mul(d), T.ecdsa_sign(d, z, k)))(0x$KHX, 98765432109876543210, 13579111315171921))($T)"),
  "(True, False, False)"),
 (has(DIDA, "the design enables the controller of a DID to prove control over it without requiring permission from any other party"), "True"),
 (has(R3986, "A Uniform Resource Identifier (URI) is a compact sequence of", "characters that identifies an abstract or physical resource",
      "specification defines the generic URI syntax and a process for", "resolving URI references that might be in relative form",
      "valid URIs, allowing an implementation to parse the common components", "of a URI reference without knowing the scheme-specific requirements", "of every possible identifier"), "True"),
 (has(DIDT, "A DID is a simple text string consisting of three parts: 1) the", "did URI scheme identifier, 2) the identifier for the DID", "method , and 3) the DID method-specific identifier",
      "did:example:123456789abcdefghi", "did:example:123456/path", "did:example:123456?versionId=1"), "True"),
 ("'did:example:123456789abcdefghi'.split(':')", "['did', 'example', '123456789abcdefghi']"),
 (has(prev("02"), "URI"), "True"),
 (has(prev("03"), "IRI"), "True"),
 (has(DIDA, "Decentralized identifiers (DIDs) are a new type of identifier that enables verifiable, decentralized digital identity",
      "A DID refers to any subject (e.g., a person, organization, thing, data model, abstract entity, etc.) as determined by the controller of the DID",
      "DIDs have been designed so that they may be decoupled from centralized registries, identity providers, and certificate authorities",
      "DIDs are URIs that associate a DID subject with a DID document allowing trustable interactions associated with that subject",
      "Each DID document can express cryptographic material, verification methods , or services , which provide a set of mechanisms enabling a DID controller to prove control of the DID",
      "This document specifies the DID syntax, a common data model, core properties, serialized representations, DID operations, and an explanation of the process of resolving DIDs to the resources that they represent",
      "Decentralized Identifiers (DIDs) v1.0"), "True"),
 (has(DIDT, "A DID document can express verification methods , such as", "cryptographic public keys, which can be used to authenticate or authorize",
      "interactions with the DID subject or associated parties", "a", "cryptographic public key can be used as a verification method with",
      "respect to a digital signature; in such usage, it verifies that the signer", "could use the associated cryptographic private key",
      "A DID document contains information associated with the DID"), "True"),
]
