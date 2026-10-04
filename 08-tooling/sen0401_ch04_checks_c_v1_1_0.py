"""SEN0401 chapter 4, executed claims, part C (version 1.1.0): representations, key encodings and checksummed text."""
from sen0401_ch04_checkhelp_v1_1_0 import *
from sen0401_ch04_checks_a_v1_1_0 import BK, KH, NH, XH, YH, PUB
B173 = rd(S1 + "bip-0173.mediawiki")
B16 = rd(S1 + "bip-0016.mediawiki")
FILES = rd(S1 + "core_doc_files.md")
VA = evj("core_validateaddress_31_1_v1_0_0.json")
KHX = KH[2:]
WIF_U, WIF_C = "5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn", "KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ"
COMP = "03F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A"
UNCOMP = "04F028892BAD7ED57D2FB57BF33081D5CFCF6F9ED3D3D7F159C2E2FFF579DC341A07CF33DA18BD734C600B96A72BBC4749D5141C90EC8AC328AE52DDFE2E505BDB"
ADDR_C, ADDR_U = "1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy", "1424C2F4bC9JidNjjTUZCbUxv6Sa1Mt62x"
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
W_ = lambda s: X(s, KH=KH, KHX=KHX, WIFU=WIF_U, WIFC=WIF_C, COMP=COMP, UNCOMP=UNCOMP, ADDRC=ADDR_C, B58=B58, B64=B64)

CHECKS_C = [
 # ---- the branch (format)
 (has(BK, "any mistake made in copying a commitment would result in the bitcoins being sent to an unspendable output, causing them to be lost forever",
      "Hexadecimal and raw binary formats are used internally in software and rarely shown to users", "The WIF is used for import/export of keys between wallets and often used in QR code (barcode) representations of private keys",
      "All of these representations are different ways of showing the same number, the same private key"), "True"),
 # ---- bits and bytes
 (has(BK, "256 bits shown as 64 hexadecimal digits, each 4 bits", "shown as a 520-bit number (130 hex digits)", "stored in 264 bits (66 hex digits)", "65 bytes, the equivalent of 130 characters when written in hexadecimal", "65 bytes, the equivalent of 130 characters"), "True"),
 (W_("(65 * 8, 33 * 8, 65 * 2, 33 * 2, len('$KHX') // 2, 0x80, 2 ** 160)"), "(520, 264, 130, 66, 32, 128, 1461501637330902918203684832716283019655932542976)"),
 (W_("(len(bytes.fromhex('$UNCOMP')), len(bytes.fromhex('$COMP')), bytes.fromhex('$COMP').hex().upper() == '$COMP', (0x$KHX).bit_length())"), "(65, 33, True, 253)"),
 # ---- number base
 (has(BK, "the traditional decimal system uses 10 numerals, 0 through 9, the hexadecimal system uses 16, with the letters A through F as the six additional symbols",
      "A number represented in hexadecimal format is shorter than the equivalent decimal representation",
      "base64 representation uses 26 lowercase letters, 26 capital letters, 10 numerals, and 2 more characters such as \"+\" and \"/\" to transmit binary data over text-based media such as email",
      "base58 is base64 without the 0 (number zero), O (capital o), l (lower L), I (capital i), and the symbols \"+\" and \"/.\"",
      "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz", "omitting some characters that are frequently mistaken for one another and can appear identical when displayed in certain fonts".replace("omitting", "but omitting")), "True"),
 (W_("(int('ff', 16), int('11111111', 2), len('$B58'), len(set('$B58')), len('$B64'), sorted(set('$B64') - set('$B58')))"), "(255, 255, 58, 58, 64, ['+', '/', '0', 'I', 'O', 'l'])"),
 (W_("(lambda n: [next(i for i in range(1, 300) if b ** i > n) for b in (2, 10, 16, 58, 64)])(0x$KHX)"), "[253, 77, 64, 44, 43]"),
 (W_("('$B58'.index('1'), '$B58'.index('2'), int.from_bytes(bytes(20), 'big'))"), "(0, 1, 0)"),
 # ---- QR code
 (has(BK, "QR codes, which are commonly used to share addresses and invoices between wallets", "A mixed-case alphabet also requires extra space to encode in QR codes",
      "That extra space means QR codes need to be larger at the same resolution or they become harder to scan quickly",
      "Notice the difference in size and complexity of the two QR codes for the same address"), "True"),
 (has(B173, "Base58 needs a lot of space in QR codes, as it cannot use the ''alphanumeric mode''.", "Encoders MUST always output an all lowercase Bech32 string.",
      "(e.g.- for presentation purposes, or QR code use), then an uppercasing procedure can be performed external to the encoding process",
      "Decoders MUST NOT accept strings where some characters are uppercase and some are lowercase", "inside QR codes uppercase SHOULD be used, as those permit the use of",
      "which is 45% more compact than the normal"), "True"),
 (has(B16, "short enough to scan from a QR code or easily copied and pasted"), "True"),
 (has(prev("02"), "QR code", "label", "amount"), "True"),
 (X("(lambda T: (lambda a: (T.segwit_decode('bc', a)[1].hex(), T.segwit_decode('bc', a.upper()) == T.segwit_decode('bc', a), T.segwit_decode('bc', a[:10].upper() + a[10:]), 'BC1Q9D3XA5GG45Q2J39M9Y32XZVYGCGAY4RGC6AAEE'.lower() == a))('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'))($T)"),
  "('2b626ed108ad00a944bb2922a309844611d25468', True, None, True)"),
 # ---- compressed and uncompressed public key
 (has(BK, "Bitcoin was first authored, its developers only knew how to create 65-byte public keys", "an alternative encoding for public keys that used only 33 bytes and which was backward compatible with all Bitcoin full nodes at the time, so there was no need to change the Bitcoin protocol",
      "Using smaller public keys results in smaller transactions, allowing more payments to be made in the same block",
      "if we know the _x_ coordinate, we can calculate the _y_ coordinate by solving the equation", "An almost 50% reduction in size in every transaction",
      "we store a compressed public key with the prefix +02+ if the _y_ is even, and +03+ if it is odd",
      "Compressed public keys are now the default in almost all Bitcoin software and were required when using certain new features added in later protocol upgrades",
      "Failure to scan for the correct type can lead to the user not being able to spend their full balance"), "True"),
 (W_("(round(1 - 33 / 65, 3), round(100 * (1 - 33 / 65), 1))"), "(0.492, 49.2)"),
 (X("(lambda T: (lambda K: (T.pub_bytes(K).hex().upper(), T.decompress(T.pub_bytes(K)) == K, T.pub_bytes(K, False).hex().upper(), K[1] % 2))(T.ec_mul(0x$KHX)))($T)", KHX=KHX),
  "('%s', True, '%s', 1)" % (COMP, UNCOMP)),
 (X("(lambda T: (lambda K: all(T.decompress(T.pub_bytes(Q)) == Q for Q in (T.ec_mul(k) for k in range(1, 40))))(None))($T)"), "True"),
 (X("$T.decompress(bytes.fromhex('$COMP')) == ($XH, $YH)", COMP=COMP, XH=XH, YH=YH), "True"),
 (X("(2 ** 256 - 2 ** 32 - 977) % 2"), "1"),
 ("[%s['%s']['isvalid'], %s['%s']['isvalid'], %s['%s']['scriptPubKey'] != %s['%s']['scriptPubKey']]" % (VA, ADDR_C, VA, ADDR_U, VA, ADDR_C, VA, ADDR_U), "[True, True, True]"),
 # ---- wallet import format and compressed private key
 (has(BK, "WIF", "Base58check encoding: base58 with version prefix of 128 and 32-bit checksum", "As above, with added suffix 0x01 before encoding",
      "5J3mBbAH58CpQ3Y5RNJpUKPE62SQ5tfcvU2JpbnkeyhfsYB1Jcn", "KxFC1jmwwCoACiCAWZ3eXa96mBM6tb3TYzGmf6YwgdGWZgawvrtJ",
      "1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD01"), "True"),
 (W_("(lambda T: (T.wif(0x$KHX, False), T.wif(0x$KHX, True), len(T.wif(0x$KHX, False)), len(T.wif(0x$KHX, True))))($T)"), "('%s', '%s', 51, 52)" % (WIF_U, WIF_C)),
 (W_("(lambda T: (T.b58check_decode('$WIFU').hex(), T.b58check_decode('$WIFC').hex()))($T)"), "('80%s', '80%s01')" % (KHX.lower(), KHX.lower())),
 (has(BK, "The commonly used term \"compressed private key\" is a misnomer, because when a private key is exported as WIF-compressed, it is actually one byte _longer_ than an \"uncompressed\" private key",
      "which signifies that the private key is from a newer wallet and should only be used to produce compressed public keys", "Private keys are not themselves compressed and cannot be compressed",
      "private key from which only compressed public keys should be derived", "private key from which only uncompressed public keys should be derived",
      "While the base58 encoding version prefix is the same (0x80) for both WIF and WIF-compressed formats, the addition of one byte on the end of the number causes the first character of the base58 encoding to change from a 5 to either a _K_ or _L_",
      "While 100 is one digit longer than 99, it also has a prefix of 1 instead of a prefix of 9",
      "In a newer wallet that implements compressed public keys, the private keys will only ever be exported as WIF-compressed (with a _K_ or _L_ prefix)",
      "You should only refer to the export format as \"WIF-compressed\" or \"WIF\" and not refer to the private key itself as \"compressed\""), "True"),
 (W_("(len('$WIFC') - len('$WIFU'),)"), "(1,)"),
 (X("(lambda T: [(T.wif(k, False)[0], T.wif(k, True)[0], len(T.b58check_decode(T.wif(k, False))), len(T.b58check_decode(T.wif(k, True)))) for k in (0, 2 ** 256 - 1, 1, T.N - 1)])($T)"),
  "[('5', 'K', 33, 34), ('5', 'L', 33, 34), ('5', 'K', 33, 34), ('5', 'L', 33, 34)]"),
 # ---- checksum and base58check
 (has(BK, "includes a _checksum_ encoded in the base58 alphabet. The checksum is an additional four bytes added to the end of the data that is being encoded",
      "The checksum is derived from the hash of the encoded data and can therefore be used to detect transcription and typing errors",
      "If the two do not match, an error has been introduced and the base58check data is invalid",
      "This prevents a mistyped Bitcoin address from being accepted by the wallet software as a valid destination, an error that would otherwise result in loss of funds",
      "checksum = SHA256(SHA256(prefix||data))", "we take only the first four bytes", "The result is composed of three items: a prefix, the data, and a checksum",
      "a base58check-encoded private key wallet import format (WIF) that starts with a 5",
      "In Bitcoin, other data besides public key commitments are presented to the user in base58check encoding to make that data compact, easy to read, and easy to detect errors",
      "Bech32 can both detect and help correct errors", "Checksum:: Exactly 6 characters. This is created using a BCH code, a type of error correction code"), "True"),
 (W_("(lambda T: T.dsha(bytes.fromhex('80$KHX'))[:4].hex())($T)"), "'c47e83ff'"),
 (W_("(lambda T: (T.b58check_decode('$ADDRC').hex(),))($T)"), "('00bbc1e42a39d05a4cc61752d6963b7f69d09bb27b',)"),
 (W_("(lambda T: (lambda a: (lambda ok: (ok(a), sum(ok(a[:i] + ch + a[i + 1:]) for i in range(len(a)) for ch in '$B58' if ch != a[i])))(lambda s: T.is_valid_b58check(s)))('$ADDRC'))($T)"), "(True, 0)"),
 (W_("('%.1e' % 2 ** -32, 1 / 2 ** 30 < 1e-9, 6 * 5, 4 * 8)"), "('2.3e-10', True, 30, 32)"),
 (has(B173, "This implements a [https://en.wikipedia.org/wiki/BCH_code BCH code] that guarantees detection of '''any error affecting at most 4 characters''' and has less than a 1 in 10<sup>9</sup> chance of failing to detect more errors"), "True"),
 (has(B173, "Base58 needs a lot of space in QR codes", "The mixed case in base58 makes it inconvenient to reliably write down, type on mobile keyboards, or read out loud.", "The double SHA256 checksum is slow and has no error-detection guarantees.", "Base58 decoding is complicated and relatively slow."), "True"),
 (has(BK, "It can detect errors, but it can't help users correct those errors", "your wallet will almost certainly warn that a mistake exists, but it won't help you figure out where the error is located"), "True"),
 (W_("(lambda T: T.b58check(b'\\x00' + bytes(20))[0])($T)"), "'1'"),
 (W_("(lambda T: T.b58check_decode(T.wif(0x$KHX, False)) == bytes.fromhex('80$KHX'))($T)"), "True"),
 # ---- version prefix
 (has(BK, "the prefix zero (0x00 in hex) indicates that the data should be used as the commitment (hash) in a legacy P2PKH output script", "0x6F", "0xC4", "0x0488B21E", "5, K, or L", "m or n", "xpub"), "True"),
 (X("(lambda T: [(v.hex(), n, sorted({T.b58check(v + bytes([f]) * n)[0] for f in (0, 255)})) for v, n in ((b'\\x00', 20), (b'\\x05', 20), (b'\\x6f', 20), (b'\\xc4', 20), (b'\\x80', 32))])($T)"),
  "[('00', 20, ['1']), ('05', 20, ['3']), ('6f', 20, ['m', 'n']), ('c4', 20, ['2']), ('80', 32, ['5'])]"),
 (X("(lambda T: sorted({T.b58check(b'\\x80' + bytes([f]) * 32 + b'\\x01')[0] for f in (0, 255)}))($T)"), "['K', 'L']"),
 (X("(lambda T: sorted({T.b58check(bytes.fromhex('0488B21E') + bytes([f]) * 74)[:4] for f in (0, 255)}))($T)"), "['xpub']"),
 (has(BK, "Address for pay to public key hash (P2PKH)", "Address for pay to script hash (P2SH)", "Testnet Address for P2PKH", "Testnet Address for P2SH", "Private Key WIF", "BIP32 Extended Public Key"), "True"),
 # ---- network selector
 (has(FILES, "All content of the data directory, except for `bitcoin.conf` file, is chain-specific", "`-chain=test` or `-testnet` | *path_to_datadir*`/testnet3/`", "`-chain=testnet4` or `-testnet4` | *path_to_datadir*`/testnet4/`",
      "`-chain=signet` or `-signet` | *path_to_datadir*`/signet/`", "`-chain=regtest` or `-regtest` | *path_to_datadir*`/regtest/`"), "True"),
 (has(BK, "bc", "Bitcoin mainnet", "tb", "Bitcoin testnet"), "True"),
 (has(B173, "tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx", "bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4"), "True"),
 ("('bc1q9d3xa5gg45q2j39m9y32xzvygcgay4rgc6aaee'[:2], 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx'[:2])", "('bc', 'tb')"),
 (X("(lambda T: (T.segwit_decode('tb', 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx') is not None, T.segwit_decode('bc', 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx'), T.segwit_decode('tb', 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kv8f3t4'), T.segwit_decode('bc', 'bc1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx')))($T)"), "(True, None, None, None)"),
 (has(B173, "the human-readable part", "feeding the higher bits of each character's US-ASCII value into the checksum calculation followed by a zero and then the lower bits of each"), "True"),
 (X("(lambda T: (T.bech_encode('bc', [0, 14], T.BECH32) != T.bech_encode('tb', [0, 14], T.BECH32)))($T)"), "True"),
]
