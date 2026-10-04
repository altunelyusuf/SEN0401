"""SEN0401 chapter 4, executed claims, part E (version 1.1.0): the segregated witness addresses (bech32 and bech32m) and the
witness output kinds. Each entry is (expression, expected repr); the chapter builder evaluates it alone under CPython 3.14.
Sentences the text takes from the book, a BIP or Bitcoin Core are checked by reading the saved copy of the source (has);
addresses, scripts, lengths and checksum properties are computed by the chapter's own toolkit."""
from sen0401_ch04_checkhelp_v1_1_0 import *
from sen0401_ch04_checks_a_v1_1_0 import BK, B141, KH
B173 = rd(S1 + "bip-0173.mediawiki")
B350 = rd(S1 + "bip-0350.mediawiki")
B340 = rd(S1 + "bip-0340.mediawiki")
B142 = rd(S1 + "bip-0142.mediawiki")
DESCR = core("doc/descriptors.md")
SCRIPTH = core("src/script/script.h")
OPS = "{m.group(1): int(m.group(2), 16) for m in __import__('re').finditer(r'(OP_\\w+) = (0x[0-9a-fA-F]+)', %s)}" % SCRIPTH
VA = evj("core_validateaddress_31_1_v1_0_0.json")
WAD = evj("core_wallet_addresses_31_1_v1_0_0.json")
DERIVE = ev("core_deriveaddresses_31_1_v1_0_0.txt")
ATYPE = ev("core_help_addresstype_31_1_v1_0_0.txt")
VR = evj("verify_results_v1_0_0.json")
VEC = evj("bip350_vectors_v1_0_0.json")
STATUS = ev("bip_status_v1_0_0.txt")
KHX = KH[2:]
WPKH = "2b626ed108ad00a944bb2922a309844611d25468"
WSH = "648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f"
TR = "2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311"
A_WPKH = "bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee"
A_WSH = "bc1qvj9r9egtd7mu2gemy28kpf4zefq4ssqzdzzycj7zjhk4arpavfhsct5a3p"
A_TR = "bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7"
A_FUT = "bc1sqqqqkfw08p"
A_TYPO = "bc1p9nh05ha8wrljf7ru236awn4t2x0d5ctkkywmv9sclnm4t0av2vgs4k3au7"
H160C = "bbc1e42a39d05a4cc61752d6963b7f69d09bb27b"
A_NEST = "3FyC6EYuxW22uj4CaEGjNCjxeg7gHyFeVv"
A_OWN_WPKH = "bc1qh0q7g23e6pdye3sh2ttfvwmld8gfhvnmmfxuck"
EXT = ("bc1pqqqsq9txsqp", "bc1pqqqsq9txsqqqqp", "bc1pqqqsq9txsqqqqqqp", "bc1pqqqsq9txsqqqqqqqqp",
       "bc1pqqqsq9txsqqqqqqqqqp", "bc1pqqqsq9txsqqqqqqqqqqqp")
E_ = lambda s, **kw: X(s, KHX=KHX, WPKH=WPKH, WSH=WSH, PTR=TR, AWPKH=A_WPKH, AWSH=A_WSH, ATR=A_TR, AFUT=A_FUT,
                       ATYPO=A_TYPO, H160C=H160C, ANEST=A_NEST, AOWN=A_OWN_WPKH, EXT=repr(EXT), **kw)

CHECKS_E = [
 # ---- the segwit level
 (has(BK, "In 2017, the Bitcoin protocol was upgraded", "it prevents transaction identifiers (txids) from being changed without the consent of a spending user (or a quorum of signers when multiple signatures are required)",
      "called _segregated witness_ (or _segwit_ for short), also provided additional capacity for transaction data in blocks and several other benefits",
      "users wanting direct access to segwit's benefits had to accept payments to new output scripts",
      "encompass the ability to parse bech32 addresses and are the current recommended address format for Bitcoin wallets"), "True"),
 (has(BK, "Its mixed-case presentation made it inconvenient to read aloud or transcribe", "It can detect errors, but it can't help users correct those errors",
      "A mixed-case alphabet also requires extra space to encode in QR codes", "It requires every spender wallet upgrade to support new protocol features like P2SH and segwit",
      "many wallet authors are busy with other work and can sometimes delay upgrading for years"), "True"),
 (has(BK, "At first, Bitcoin developers proposed BIP142, which would continue using base58check with a new version byte, similar to the P2SH upgrade"), "True"),
 (has(B142, "Title: Address Format for Segregated Witness"), "True"),
 (has(STATUS, "BIP: 173", "Title: Base32 address format for native v0-16 witness outputs", "BIP: 350", "Title: Bech32m format for v1+ witness addresses", "Status: Deployed"), "True"),
 (E_("($WAD['default']['desc_kind'], $WAD['default']['witness_version'], $WAD['default']['address'][:3])", WAD=WAD), "('wpkh', 0, 'bc1')"),
 # ---- the segregated witness upgrade
 (has(B141, "This BIP defines a new structure called a \"witness\" that is committed to blocks separately from the transaction merkle tree",
      "This structure contains data required to check transaction validity but not required to determine transaction effects. In particular, scripts and signatures are moved into this new structure",
      "Status: Deployed", "A new <code>wtxid</code> is defined: the double SHA256 of the new serialization with witness data",
      "A non-witness program (defined hereinafter) txin MUST be associated with an empty witness field, represented by a <code>0x00</code>",
      "A new block rule is added which requires a commitment to the <code>wtxid</code>",
      "'''Transmission of signature data becomes optional'''. It is needed only if a peer is trying to validate a transaction instead of just checking its existence"), "True"),
 (has(B141, "Segregated witness fixes the problem of transaction malleability fundamentally, which enables the building of unconfirmed transaction dependency chains in a trust-free manner"), "True"),
 (has(prev("03"), "segregated witness"), "True"),
 ("len(['txid', 'wtxid'])", "2"),
 # ---- segwit inside P2SH
 (has(BK, "one of the advantages of the P2SH output type was that a spender (such as Alice) didn't need to know the details of the script the receiver (such as Bob) used",
      "The segwit upgrade was designed to use this mechanism, allowing users to immediately begin accessing many of the new benefits by using a P2SH address",
      "But for Bob to gain access to all of the benefits, he would need Alice's wallet to pay him using a different type of script"), "True"),
 (has(B141, "Comparing with the previous example, the scriptPubKey is 1 byte bigger and the scriptSig is 23 bytes bigger"), "True"),
 (has(DESCR, "`sh(wpkh(03fff97bd5755eeea420453a14355235d382f6472f8568a18b2f057a1460297556))` describes a P2SH-P2WPKH output with the specified public key"), "True"),
 (has(ATYPE, "What type of addresses to use (\"legacy\", \"p2sh-segwit\", \"bech32\", \"bech32m\", default: \"bech32\")"), "True"),
 (E_("(lambda T: (lambda h: (bytes([0, 20]).hex(), T.p2sh(bytes([0, 20]) + h), T.hash160(T.pub_bytes(T.ec_mul(0x$KHX))).hex()))(T.hash160(T.pub_bytes(T.ec_mul(0x$KHX)))))($T)"),
  "('0014', '%s', '%s')" % (A_NEST, H160C)),
 (E_("[l.split(' => ')[1] for l in $D.strip().splitlines() if l.startswith('sh(wpkh(')]", D=DERIVE), "['%s']" % A_NEST),
 (E_("($VA['$ANEST'] if '$ANEST' in $VA else 'not asked')", VA=VA), "'not asked'"),
 # ---- the bech32 address
 (has(BK, "bech32 (pronounced with a soft \"ch\", as in \"besh thirty-two\")", "The \"bech\" stands for BCH, the initials of the three individuals who discovered the cyclic code in 1959 and 1960 upon which bech32 is based",
      "The \"32\" stands for the number of characters in the bech32 alphabet (similar to the 58 in base58check)",
      "Bech32 uses only numbers and a single case of letters (preferably rendered in lowercase)",
      "Despite its alphabet being almost half the size of the base58check alphabet, a bech32 address for a pay to witness public key hash (P2WPKH) script is only slightly longer than a legacy address for an equivalent P2PKH script"), "True"),
 (has(B173, "\"Bech\" contains the characters BCH (the error", "detection algorithm used) and sounds a bit like \"base\"",
      "Version 0 witness addresses are always 42 or 62 characters, but implementations MUST allow the use of any version"), "True"),
 (E_("(len('$AWPKH'), len('$AWSH'), len('$ATR'), len('$AFUT'))"), "(42, 62, 62, 14)"),
 (E_("(lambda T: (T.CHARSET, len(T.CHARSET), sorted(set('abcdefghijklmnopqrstuvwxyz0123456789') - set(T.CHARSET))))($T)"),
  "('qpzry9x8gf2tvdw0s3jn54khce6mua7l', 32, ['1', 'b', 'i', 'o'])"),
 (E_("(lambda T: (T.segwit_address('bc', 0, bytes.fromhex('$WPKH')), T.segwit_address('bc', 0, bytes.fromhex('$WSH')), T.segwit_address('bc', 1, bytes.fromhex('$PTR')), T.segwit_address('bc', 16, bytes(2))))($T)"),
  "('%s', '%s', '%s', '%s')" % (A_WPKH, A_WSH, A_TR, A_FUT)),
 (E_("($VA['$AWPKH']['isvalid'], $VA['$AWPKH']['witness_version'], $VA['$AWPKH']['witness_program'])", VA=VA), "(True, 0, '%s')" % WPKH),
 (E_("$VR['book_addresses_toolkit'] and $VR['book_addresses_sipa_library'] and $VR['book_addresses_agree']", VR=VR), "True"),
 (E_("(lambda T: T.segwit_decode('bc', '$AWPKH') == (0, bytes.fromhex('$WPKH')) and T.segwit_decode('bc', '$AWPKH'[:-1] + 'f') is None)($T)"), "True"),
 # ---- the witness version
 (has(BK, "A single byte that encodes as a single character in a bech32m Bitcoin address immediately following the separator",
      "The letter \"q\" is the encoding of \"0\" for segwit v0, the initial version of segwit where bech32 addresses were introduced",
      "The letter \"p\" is the encoding of \"1\" for segwit v1 (also called taproot) where bech32m began to be used",
      "There are seventeen possible versions of segwit and it's required for Bitcoin that the first byte of a bech32m data part decode to the number 0 through 16 (inclusive)",
      "a witness version of `0` is for `OP_0`, which uses the byte 0x00--but a witness version of `1` uses `OP_1`, which is byte 0x51",
      "Witness versions `2` through `16` use 0x52 through 0x60, respectively"), "True"),
 (has(B173, "MUST verify that the first decoded data value (the witness version) is between 0 and 16, inclusive",
      "witness version ''n'' is stored as ''OP_n''. OP_0 is", "encoded as 0x00, but OP_1 through OP_16 are encoded as 0x51 though 0x60",
      "If a bech32 address is converted to an incorrect", "scriptPubKey the result will likely be either unspendable or insecure"), "True"),
 (E_("(lambda T: (T.CHARSET.index('q'), T.CHARSET.index('p'), T.CHARSET.index('s')))($T)"), "(0, 1, 16)"),
 ("[0x00 if v == 0 else 0x50 + v for v in (0, 1, 2, 16)]", "[0, 81, 82, 96]"),
 (X("(lambda ops: (ops['OP_0'], ops['OP_1'], ops['OP_16']))($OPS)", OPS=OPS), "(0, 81, 96)"),
 (E_("($VA['$AFUT']['witness_version'], $VA['$AFUT']['scriptPubKey'])", VA=VA), "(16, '60020000')"),
 (E_("(lambda T: T.segwit_decode('bc', '$AFUT'))($T)"), "(16, b'\\x00\\x00')"),
 # ---- the witness program
 (has(BK, "From 2 to 40 bytes. For segwit v0, this witness program must be either 20 or 32 bytes; no other length is valid",
      "For segwit v1, the only defined length as of this writing is 32 bytes but other lengths may be defined later",
      "OP_0 2b626ed108ad00a944bb2922a309844611d25468", "OP_0 648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f",
      "OP_1 2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311", "OP_16 0000"), "True"),
 (has(B173, "A conversion of the 2-to-40-byte witness program (as defined by", "Decoders SHOULD enforce known-length restrictions on witness programs.",
      "For example, BIP141 specifies ''If the version byte is 0, but the witness", "program is neither 20 nor 32 bytes, the script must fail.''",
      "As a result of the previous rules, addresses are always between 14 and 74 characters long, and their length modulo 8 cannot be 0, 3, or 5"), "True"),
 (E_("(len(bytes.fromhex('$WPKH')), len(bytes.fromhex('$WSH')), len(bytes.fromhex('$PTR')))"), "(20, 32, 32)"),
 (E_("[$VA[a]['scriptPubKey'] for a in ('$AWPKH', '$AWSH', '$ATR', '$AFUT')]", VA=VA),
  "['0014%s', '0020%s', '5120%s', '60020000']" % (WPKH, WSH, TR)),
 (E_("(lambda T: (len(T.segwit_address('bc', 0, bytes(20))), len(T.segwit_address('bc', 0, bytes(32))), len(T.segwit_address('bc', 1, bytes(2))), len(T.segwit_address('bc', 1, bytes(40)))))($T)"),
  "(42, 62, 14, 74)"),
 (E_("(lambda T: sorted({len(T.segwit_address('bc', v, bytes(n))) % 8 for v in range(17) for n in range(2, 41)}))($T)"), "[1, 2, 4, 6, 7]"),
 (E_("(lambda T: (T.segwit_decode('bc', T.segwit_address('bc', 0, bytes(21))), T.segwit_decode('bc', T.segwit_address('bc', 0, bytes(20))) is not None))($T)"), "(None, True)"),
 # ---- the human-readable part
 (has(BK, "Bech32m addresses start with a human readable part (HRP)", "for Bitcoin you only need to know about the HRPs already chosen",
      "The HRP is followed by a separator, the number \"1.\"",
      "Earlier proposals for a protocol separator used a colon but some operating systems and applications that allow a user to double-click a word to highlight",
      "The number \"1\" was chosen because bech32 strings don't otherwise use it in order to prevent accidental transliteration between the number \"1\" and the lowercase letter \"l.\""), "True"),
 (has(B173, "This part MUST contain 1 to 83 US-ASCII characters, with each character having a value in the range [33-126]. HRP validity may be further restricted by specific applications",
      "The '''separator''', which is always \"1\". In case \"1\" is allowed inside the human-readable part, the last one in the string is the separator",
      "'bc' is shorter", "It was chosen to", "be of the same length as the mainnet counterpart (to simplify", "implementations' assumptions about lengths), but still be visually",
      "which is intended to convey the type of data, or anything else that is relevant to the reader"), "True"),
 (E_("('$AWPKH'.rpartition('1')[0], 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx'.rpartition('1')[0])"), "('bc', 'tb')"),
 (E_("(lambda T: T.hrp_expand('bc'))($T)"), "[3, 3, 0, 2, 3]"),
 (E_("(lambda T: T.bech_check('tb' + '$AWPKH'[2:]))($T)"), "None"),
 # ---- the BCH code
 (has(BK, "Checksum:: Exactly 6 characters. This is created using a BCH code, a type of error correction code (although for Bitcoin addresses, we'll see later that it's essential to use the checksum only for error detection--not correction)"), "True"),
 (has(B173, "The last six characters of the data part form a checksum and contain no", "information. Valid strings MUST pass the criteria for validity specified",
      "def bech32_polymod(values):", "GEN = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]",
      "return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1",
      "An unfortunate side effect of error correction is that", "it erodes error detection: correction changes invalid inputs into valid",
      "implementations SHOULD", "NOT implement correction beyond potentially suggesting to the user where", "in the string an error might be found, without suggesting the correction"), "True"),
 (has(B350, "BECH32M_CONST = 0x2bc830a3", "return bech32m_polymod(bech32m_hrp_expand(hrp) + data) == BECH32M_CONST"), "True"),
 ("(6 * 5, 2 ** 30, 1 / 2 ** 30 < 1e-9)", "(30, 1073741824, True)"),
 (E_("(lambda T: (T.bech_check('$AWPKH') == T.BECH32, T.bech_check('$ATR') == T.BECH32M))($T)"), "(True, True)"),
 # the guarantee, tried exhaustively for one and two characters of the data part and on a fixed random sample for three and four
 (E_("""(lambda T, it: (lambda hrp, d: (lambda n1, n2: (n1[0], n1[1], n2[0], n2[1]))(
   (lambda L: (len(L), sum(1 for s in L if T.bech_check(s) is not None)))([hrp + '1' + d[:i] + c + d[i + 1:] for i in range(len(d)) for c in T.CHARSET if c != d[i]]),
   (lambda L: (len(L), sum(1 for s in L if T.bech_check(s) is not None)))([hrp + '1' + d[:i] + c + d[i + 1:j] + e + d[j + 1:] for i, j in it.combinations(range(len(d)), 2) for c in T.CHARSET if c != d[i] for e in T.CHARSET if e != d[j]])
 ))(*('$AWPKH'.rpartition('1')[0], '$AWPKH'.rpartition('1')[2])))($T, __import__('itertools'))"""),
  "(1209, 0, 712101, 0)"),
 (E_("""(lambda T, R: (lambda hrp, d: (lambda rnd: (lambda trials: (len(trials), sum(1 for s in trials if T.bech_check(s) is not None)))(
   [(lambda pos: hrp + '1' + ''.join(rnd.choice([c for c in T.CHARSET if c != d[k]]) if k in pos else d[k] for k in range(len(d))))(set(rnd.sample(range(len(d)), rnd.choice((3, 4))))) for _ in range(100000)]
 ))(R.Random(20260928)))(*('$AWPKH'.rpartition('1')[0], '$AWPKH'.rpartition('1')[2])))($T, __import__('random'))"""),
  "(100000, 0)"),
 (E_("($VR['substitution_errors_undetected']['data_characters'], len('$AWPKH'.rpartition('1')[2]))", VR=VR), "(39, 39)"),
 # ---- error detection and the located errors
 (has(BK, "In an address of an", "expected length, it is mathematically guaranteed to detect any error", "affecting four characters or less; that's more reliable than",
      "base58check.  For longer errors, it will fail to detect them less than", "one time in a billion, which is roughly the same reliability as",
      "Even better, for an address typed with just a few", "errors, it can tell the user where those errors occurred, allowing them to",
      "bech32 address decoder demo", "The mathematical guarantees about their ability to detect",
      "errors only apply if the length of the address you enter into a wallet", "is the same length of the original address"), "True"),
 (E_("($VA['$ATYPO']['isvalid'], $VA['$ATYPO']['error'], $VA['$ATYPO']['error_locations'])", VA=VA),
  "(False, 'Invalid Bech32m checksum', [25, 40])"),
 (E_("[i for i, (a, b) in enumerate(zip('$ATR', '$ATYPO')) if a != b]"), "[25, 40]"),
 (E_("(len('$ATR') == len('$ATYPO'), sum(1 for a, b in zip('$ATR', '$ATYPO') if a != b))"), "(True, 2)"),
 (E_("(lambda T: T.bech_check('$ATYPO'))($T)"), "None"),
 (has(B350, "Bech32m, like Bech32, does support locating"), "True"),
 # ---- the length extension weakness
 (has(BK, "the choice for one of the constants in the bech32", "algorithm just happened to make it very easy to add or remove the letter",
      "in the penultimate position of an address that ends with the letter", "In those cases, you can also add or remove the letter",
      "Only two valid lengths were defined for v0 segwit outputs: 22", "bytes and 34 bytes.  Those correspond to bech32 addresses that are 42 characters",
      "or 62 characters long, so someone would need to add or remove the letter \"q\"", "from the penultimate position of a bech32 address 20 times in order to",
      "bc1pqqqsq9txsqp", "bc1pqqqsq9txsqqqqqqqqqqqp"), "True"),
 (has(B350, "Bech32 has an unexpected", "weakness]: whenever the final character is a 'p', inserting or deleting any number of 'q' characters immediately preceding it does not invalidate the checksum",
      "This does not affect existing uses of witness version 0 BIP173 addresses due to their restriction to two specific lengths, but may affect future uses"), "True"),
 (E_("[len(a) for a in $EXT]"), "[15, 18, 20, 22, 23, 25]"),
 (E_("(lambda T: ([T.bech_check(a) == T.BECH32 for a in $EXT], [T.bech_check(a) == T.BECH32M for a in $EXT]))($T)"),
  "([True, True, True, True, True, True], [False, False, False, False, False, False])"),
 (E_("($VR['length_extension_bech32_valid'], $VR['length_extension_bech32m_valid'])", VR=VR), "([6, 6], [0, 6])"),
 (E_("sorted({$VA[a]['error'] for a in $EXT})", VA=VA), "['Version 1+ witness address must use Bech32m checksum']"),
 (E_("[$VA[a]['isvalid'] for a in $EXT]", VA=VA), "[False, False, False, False, False, False]"),
 (E_("(lambda T: [T.segwit_decode('bc', a) for a in $EXT])($T)"), "[None, None, None, None, None, None]"),
 (E_("(22 * 2 - 2, 42, 62, (62 - 42) // 2 * 2)"), "(42, 42, 62, 20)"),
 # ---- bech32m
 (has(BK, "Developers exhaustively analyzed the bech32", "problem and found that changing a single constant in their algorithm",
      "would eliminate the problem, ensuring that any insertion or deletion of", "up to five characters will only fail to be detected less often than one",
      "time in a billion", "The version of bech32 with a single different constant is known as", "bech32 modified (bech32m)",
      "All of the characters in bech32 and bech32m", "addresses for the same underlying data will be identical except for the",
      "last six (the checksum)", "both address", "types contain an internal version byte that makes determining that easy",
      "BECH32_CONSTANT = 1", "BECH32M_CONSTANT = 0x2bc830a3", "the appropriate constant is merged into the value using an xor",
      "operation"), "True"),
 (has(B350, "Bech32m modifies the checksum of the Bech32 specification, replacing the constant ''1'' that is xored into the checksum at the end with ''0x2bc830a3''",
      "Addresses for segregated witness outputs version 1 through 16 use Bech32m",
      "Permitting both encodings reduces the error detection capabilities (it makes it equivalent to only have 29 bits of checksum)",
      "No, a valid Bech32 and Bech32m string will always differ by at least 3 characters if they are the same length",
      "If its witness version is 0, encode it using Bech32.", "If its witness version is 1 or higher, encode it using Bech32m."), "True"),
 ("hex(0x2bc830a3)", "'0x2bc830a3'"),
 (E_("(lambda T: (T.BECH32, T.BECH32M))($T)"), "(1, 734539939)"),
 (E_("(lambda T: (lambda a, b: (a[:-6] == b[:-6], a[-6:] != b[-6:], len(a) == len(b)))(T.bech_encode('bc', [0] + T.convertbits(bytes.fromhex('$WPKH'), 8, 5), T.BECH32), T.bech_encode('bc', [0] + T.convertbits(bytes.fromhex('$WPKH'), 8, 5), T.BECH32M)))($T)"),
  "(True, True, True)"),
 (E_("(lambda T: (lambda s: (T.bech_check(s) == T.BECH32, T.segwit_decode('bc', s)))(T.bech_encode('bc', [1] + T.convertbits(bytes.fromhex('$PTR'), 8, 5), T.BECH32)))($T)"), "(True, None)"),
 (E_("(lambda T: (lambda a, b: sum(1 for x, y in zip(a, b) if x != y) >= 3)(T.bech_encode('bc', [0] + T.convertbits(bytes.fromhex('$WPKH'), 8, 5), T.BECH32), T.bech_encode('bc', [0] + T.convertbits(bytes.fromhex('$WPKH'), 8, 5), T.BECH32M)))($T)"), "True"),
 (E_("($VA['$ATR']['witness_version'], $VA['$ATR']['isvalid'])", VA=VA), "(1, True)"),
 # ---- P2WPKH
 (has(BK, "For the P2WPKH output, the witness program contains a commitment constructed in exactly the same", "way as the commitment for a P2PKH output seen in",
      "A public key is passed into a SHA256 hash", "function.  The resultant 32-byte digest is then passed into a RIPEMD-160",
      "hash function.  The digest of that function (the commitment) is placed", "in the witness program"), "True"),
 (has(B141, "The '0' in scriptPubKey indicates the following push is a version 0 witness program. The length of the witness program indicates that it is a P2WPKH type. The witness must consist of exactly 2 items. The HASH160 of the pubkey in witness must match the witness program",
      "Comparing with a traditional P2PKH output, the P2WPKH equivalent occupies 3 less bytes in the scriptPubKey, and moves the signature and public key from scriptSig to witness",
      "Only compressed public keys are accepted in P2WPKH and P2WSH"), "True"),
 (E_("(len(bytes.fromhex('0014$WPKH')), len(bytes.fromhex('76a914$WPKH88ac')), len(bytes.fromhex('76a914$WPKH88ac')) - len(bytes.fromhex('0014$WPKH')))"), "(22, 25, 3)"),
 (E_("(lambda T: T.segwit_address('bc', 0, T.hash160(T.pub_bytes(T.ec_mul(0x$KHX)))))($T)"), "'%s'" % A_OWN_WPKH),
 (E_("[l.split(' => ')[1] for l in $D.strip().splitlines() if l.startswith('wpkh(0')]", D=DERIVE), "['%s']" % A_OWN_WPKH),
 (has(B173, "All examples use public key", "<tt>0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798</tt>",
      "Mainnet P2WPKH: <tt>bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4</tt>"), "True"),
 (E_("(lambda T: (lambda h: (h.hex(), T.segwit_address('bc', 0, h)))(T.hash160(bytes.fromhex('0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798'))))($T)"),
  "('751e76e8199196d454941c45d1b3a323f1433bd6', 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4')"),
 (E_("($WAD['bech32']['desc_kind'], $WAD['bech32']['witness_version'], $WAD['bech32']['scriptPubKey'][:4])", WAD=WAD), "('wpkh', 0, '0014')"),
 # ---- P2WSH
 (has(BK, "For the pay to witness script hash (P2WSH) output, we don't use the P2SH algorithm.  Instead we take",
      "the script, pass it into a SHA256 hash function, and use the 32-byte", "digest of that function in the witness program",
      "For P2SH, the SHA256", "digest was hashed again with RIPEMD-160, but that may not be secure in", "some cases",
      "A result of", "using SHA256 without RIPEMD-160 is that P2WSH commitments are 32 bytes", "(256 bits) instead of 20 bytes (160 bits)",
      "newer Bitcoin addresses provide at least 128 bits of collision resistance"), "True"),
 (has(B173, "The P2WSH examples use <tt>key OP_CHECKSIG</tt> as script", "Testnet P2WSH: <tt>tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7</tt>",
      "00201863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262"), "True"),
 (E_("len(bytes.fromhex('0020$WSH'))"), "34"),
 (E_("(lambda T, h: (lambda s: (h.sha256(s).hexdigest(), T.segwit_address('tb', 0, h.sha256(s).digest())))(bytes([33]) + bytes.fromhex('0279BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798') + bytes([0xac])))($T, __import__('hashlib'))"),
  "('1863143c14c5166804bd19203356da136c985678cd4d27a1b8c6329604903262', 'tb1qrp33g0q5c5txsp9arysrx4k6zdkfs4nce4xj0gdcccefvpysxf3q0sl5k7')"),
 (E_("($VA['$AWSH']['isvalid'], $VA['$AWSH']['witness_version'], $VA['$AWSH']['isscript'], len(bytes.fromhex($VA['$AWSH']['scriptPubKey'])))", VA=VA), "(True, 0, True, 34)"),
 (E_("(32 * 8, 20 * 8, 256 // 2)"), "(256, 160, 128)"),
 # ---- P2TR
 (has(BK, "For the pay-to-taproot (P2TR) output, the witness program is a point on", "the secp256k1 curve.  It may be a simple public key, but in most cases",
      "it should be a public key that commits to some additional data"), "True"),
 (has(B340, "resulting in 32-byte public keys and 64-byte signatures", "Instead of using [https://www.secg.org/sec1-v2.pdf ''compressed''] 33-byte encodings of elliptic curve points which are common in Bitcoin today, public keys in this proposal are encoded as 32 bytes"), "True"),
 (has(DESCR, "`tr(KEY)` or `tr(KEY,TREE)` (top level only): P2TR output with the specified key as internal key",
      "`rawtr(KEY)` (top level only): P2TR output with the specified key as output key"), "True"),
 (E_("[l.split(' => ')[1] for l in $D.strip().splitlines() if l.startswith('tr(')]", D=DERIVE), "['bc1pyjqgwc0t990afumlh6m9hpmrh7pxd7x0nev83xvzqwvuyevymwgqtjhuxh']"),
 (E_("'bc1pyjqgwc0t990afumlh6m9hpmrh7pxd7x0nev83xvzqwvuyevymwgqtjhuxh' != '$ATR'"), "True"),
 (E_("(lambda T: (lambda x: (lambda y: ((y * y - x ** 3 - 7) % T.P, sorted((y % 2, (T.P - y) % 2))))(pow((x ** 3 + 7) % T.P, (T.P + 1) // 4, T.P)))(int('$PTR', 16)))($T)"), "(0, [0, 1])"),
 (E_("(lambda T: T.segwit_address('bc', 1, bytes.fromhex('$PTR')))($T)"), "'%s'" % A_TR),
 (E_("($WAD['bech32m']['desc_kind'], $WAD['bech32m']['witness_version'], $WAD['bech32m']['scriptPubKey'][:4])", WAD=WAD), "('tr', 1, '5120')"),
 (E_("$VEC['read']", VEC=VEC), "'2026-09-28'"),
]
