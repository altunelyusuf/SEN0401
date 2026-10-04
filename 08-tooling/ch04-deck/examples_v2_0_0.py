"""Every computation the SEN0401 chapter 4 lecture deck shows, version 2.0.0. The outputs come from executing these
statements, never from typing them: examples_run_v2_0_0.py writes examples_out_v2_0_0.json and the deck reads that file.

PRELUDE is the chapter's own toolkit (sen0401_ch04_keys_v1_1_0.py, the module the chapter corpus also uses), the values
the slides name but do not print in full (the book's example key and the three witness programs), and the saved
evidence of the run of Bitcoin Core 31.1 and of the primary standards kept in 08-tooling/ch04-evidence. Every group is
named after the concept of the chapter 4 taxonomy whose slide shows it, so that a slide and its computation cannot
drift apart. deck_check_v2_0_0.py re-runs every '>>>' line of the finished deck in this same namespace.
"""
__version__ = "2.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLKIT_PATH = os.path.join(HERE, "..", "sen0401_ch04_keys_v1_1_0.py")
EVID = os.path.abspath(os.path.join(HERE, "..", "ch04-evidence"))
TOOLKIT = open(TOOLKIT_PATH, encoding="utf-8").read()

# the function text the "double and add" slide shows must equal the one that computes every key on the slides
EC_SRC = TOOLKIT.split("# --- ec ---\n")[1].split("# --- end ec ---")[0].rstrip("\n")

K_HEX = "0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD"

PRELUDE = TOOLKIT + """
import json, math, secrets
EVID = %r

# the book's worked example, and the values derived from it that the slides use by name
k = %s
K = ec_mul(k)
PUB = pub_bytes(K)            # compressed, 33 bytes
PUBU = pub_bytes(K, False)    # uncompressed, 65 bytes
H160 = hash160(PUB)

# the three witness programs the book prints, and its length-extension strings
PROG_WPKH = '2b626ed108ad00a944bb2922a309844611d25468'
PROG_WSH = '648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f'
PROG_TR = '2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311'
EXT = ['bc1pqqqsq9txsqp', 'bc1pqqqsq9txsqqqqp', 'bc1pqqqsq9txsqqqqqqp',
       'bc1pqqqsq9txsqqqqqqqqp', 'bc1pqqqsq9txsqqqqqqqqqp', 'bc1pqqqsq9txsqqqqqqqqqqqp']

# the book's taproot address, and the same address with the two typing errors its figure underlines
TYPED_OK = 'bc1p9nh05ha8wrljf7ru236awm4t2x0d5ctkkywmu9sclnm4t0av2vgs4k3au7'
TYPED_BAD = 'bc1p9nh05ha8wrljf7ru236awn4t2x0d5ctkkywmv9sclnm4t0av2vgs4k3au7'

# the specification's testnet address for the same kind of output
TB_WPKH = 'tb1qw508d6qejxtdg4y5r3zarvary0c5xw7kxpjzsx'

SEED = 'f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73'
BIP38 = '6PRHv1jg1ytiE4kT2QtrUz8gEjMQghZDWg1FuxjdYDzjUkcJeGdFj9q9Vi'
EC_SRC = %r

# saved evidence: the primary standards and the run of Bitcoin Core 31.1 (08-tooling/ch04-evidence)
_rd = lambda n: open(EVID + '/' + n, encoding='utf-8').read()
_js = lambda n: json.load(open(EVID + '/' + n, encoding='utf-8'))
SEC2 = _rd('sec2_table2_v1_0_0.txt')
BIP_STATUS = _rd('bip_status_v1_0_0.txt')
CORE_ADDRESSTYPE = _rd('core_help_addresstype_31_1_v1_0_0.txt')
CORE_REMOVED = _rd('core_removed_rpcs_31_1_v1_0_0.txt')
CORE_DERIVE = _rd('core_deriveaddresses_31_1_v1_0_0.txt')
DID_ABSTRACT = _rd('did_core_abstract_v1_0_0.txt')
CORE_VALIDATE = _js('core_validateaddress_31_1_v1_0_0.json')
CORE_WALLET = _js('core_wallet_addresses_31_1_v1_0_0.json')
VECTORS = _js('bip350_vectors_v1_0_0.json')
VERIFY = _js('verify_results_v1_0_0.json')
HASHRATE = _js('hashrate_v1_0_0.json')['currentHashrate']
""" % (EVID, K_HEX, EC_SRC)

# One group per concept of the chapter 4 taxonomy; the key is the concept identifier the corpus uses.
EX = {
    # ---- Keys / Key pair ----
    "PublicKeyCryptography": [
        "K == ec_mul(k)",
        "ec_mul(k + 1) == ec_add(K, G)",
        "pub_bytes(K).hex()[:16]",
    ],
    "DigitalSignature": [
        "z = int.from_bytes(hashlib.sha256(b'pay Bob 0.1 BTC').digest(), 'big')",
        "sig = ecdsa_sign(k, z, 0x5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A5A)",
        "ecdsa_verify(K, z, sig)",
        "ecdsa_verify(K, z + 1, sig)",
    ],
    "PrivateKey": [
        "2**256 - N",
        "0 < k < N",
        "(2 ** 256).to_bytes(32, 'big')",
    ],
    "PublicKey": [
        "hex(K[0])",
        "hex(K[1])",
        "ec_mul(N) is None",
    ],
    # ---- Keys / Randomness ----
    "Entropy": [
        "round(math.log10(2 ** 256), 2)",
        "(2 ** 256 - 1).bit_length()",
    ],
    "SecureRandomness": [
        "key = secrets.randbelow(N - 1) + 1",
        "0 < key < N",
        "key.bit_length() > 200",
    ],
    # ---- Keys / The curve ----
    "FiniteField": [
        "pow(5, -1, 17)",
        "5 * 7 % 17",
        "pow(0, -1, 17)",
    ],
    "EllipticCurve": [
        "sum(1 for x in range(17) for y in range(17) if (y * y - x ** 3 - 7) % 17 == 0)",
        "(G[0] ** 3 + 7 - G[1] ** 2) % P",
    ],
    "PointAddition": [
        "small_add((1, 5), (2, 7), 17)",
        "small_add((1, 5), (1, 12), 17) is None",
        "small_order((1, 5), 17)",
    ],
    "Secp256k1": [
        "P == 2**256 - 2**32 - 977",
        "P == 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1",
        "is_probable_prime(P), is_probable_prime(N)",
    ],
    "CurveStandard": [
        "[(l.split()[0], l.split()[7]) for l in SEC2.splitlines() if l.startswith('secp256')]",
    ],
    "GeneratorPoint": [
        "pub_bytes(G).hex()",
        "ec_add(ec_mul(N - 1), G) is None",
    ],
    "PointMultiplication": [
        "(k.bit_length() - 1, bin(k).count('1') - 1)",
        "ec_mul(3) == ec_add(ec_add(G, G), G)",
    ],
    "DiscreteLogarithm": [
        "next(i for i in range(1, 101) if pow(2, i, 101) == 7)",
        "round(math.log2(N))",
    ],
    "CryptoLibrary": [
        "len(EC_SRC.splitlines())",
        "ec_mul(k) == K",
    ],
    # ---- Keys / Hash functions ----
    "HashFunction": [
        "hashlib.sha256(b'a').hexdigest()[:16]",
        "hashlib.sha256(b'`').hexdigest()[:16]",
        "a, b = hashlib.sha256(b'a').digest(), hashlib.sha256(b'`').digest()",
        "bin(int.from_bytes(a, 'big') ^ int.from_bytes(b, 'big')).count('1')",
    ],
    "Sha256": [
        "hashlib.sha256(b'abc').hexdigest()",
        "len(hashlib.sha256(b'abc').digest())",
        "hashlib.sha256('abc')",
    ],
    "Ripemd160": [
        "hashlib.new('ripemd160', hashlib.sha256(PUB).digest()).hexdigest()",
        "len(hashlib.new('ripemd160', b'').digest())",
    ],
    "Hash160": [
        "hash160(PUB).hex()",
        "hash160(PUBU).hex()",
        "hash160(PUB) == hash160(PUBU)",
    ],
    # ---- Format / Representation ----
    "BitsAndBytes": [
        "(len(PUBU), len(PUBU) * 8)",
        "(len(PUB), len(PUB) * 8)",
        "bytes.fromhex('abc')",
    ],
    "NumberBase": [
        "(int('ff', 16), int('11111111', 2))",
        "(len(hex(k)) - 2, k.bit_length())",
        "B58[0], B58[57]",
    ],
    "QrCode": [
        "ADDR = segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))",
        "ADDR.upper()",
        "ADDR.upper().lower() == ADDR",
    ],
    # ---- Format / Key encoding ----
    "CompressedPublicKey": [
        "PUB.hex()",
        "round(1 - 33 / 65, 3)",
        "decompress(PUB) == K",
    ],
    "UncompressedPublicKey": [
        "PUBU.hex()[:66]",
        "PUBU.hex()[66:]",
        "(PUBU[0], len(PUBU))",
    ],
    "WalletImportFormat": [
        "wif(k, False)",
        "wif(k)",
        "b58check_decode(wif(k)).hex()",
    ],
    "CompressedPrivateKey": [
        "len(wif(k)) - len(wif(k, False))",
        "b58check_decode(wif(k))[-1]",
        "len(b58check_decode(wif(k))) - len(b58check_decode(wif(k, False)))",
    ],
    # ---- Format / Checksummed text ----
    "Checksum": [
        "dsha(b'\\x00' + H160)[:4].hex()",
        "b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZy').hex()",
        "b58check_decode('1J7mdg5rbQyUHENYdx39WVWK7fsLpEoXZz')",
    ],
    "Base58Check": [
        "len(B58), '0' in B58, 'O' in B58, 'l' in B58, 'I' in B58",
        "b58check(b'\\x00' + H160)",
    ],
    "VersionPrefix": [
        "[b58check(bytes([v]) + bytes(20))[0] for v in (0x00, 0x05, 0x6f, 0xc4)]",
        "b58check(b'\\x80' + bytes(32))[0], b58check(b'\\x80' + bytes(32) + b'\\x01')[0]",
    ],
    "NetworkSelector": [
        "ADDR = segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))",
        "(ADDR[:2], TB_WPKH[:2])",
        "segwit_decode('tb', ADDR) is None",
    ],
    # ---- Address / Scripts ----
    "OutputScript": [
        "script = bytes.fromhex('76a914') + H160 + bytes.fromhex('88ac')",
        "script.hex()",
        "len(script)",
    ],
    "InputScript": [
        "stack = ['<signature>', '<public key>']",
        "stack[-1], len(stack)",
    ],
    "StackExecution": [
        "stack = ['<signature>', '<public key>']",
        "stack + [stack[-1]]",
        "run_p2pkh('<signature>', PUB, H160) == ['<signature>', PUB]",
        "run_p2pkh('<signature>', PUB, hash160(PUBU))",
    ],
    # ---- Address / Legacy ----
    "IpAddressPayment": [
        "(4 * 8, 2 ** 32)",
    ],
    "P2pk": [
        "script = bytes([len(PUBU)]) + PUBU + bytes([0xac])",
        "(len(script), hex(script[-1]))",
        "len(bytes([len(PUB)]) + PUB + bytes([0xac]))",
    ],
    "Commitment": [
        "SENTENCE = b'2007.  He said about a year and a half before Oct 2008\\n'",
        "hashlib.sha256(SENTENCE).hexdigest()",
        "(len(PUBU), len(H160))",
    ],
    "P2pkhAddress": [
        "p2pkh(PUB)",
        "p2pkh(PUBU)",
        "CORE_VALIDATE[p2pkh(PUB)]['scriptPubKey']",
    ],
    "RedeemScript": [
        "redeem = bytes.fromhex('0014') + H160",
        "redeem.hex()",
        "hash160(redeem).hex()",
    ],
    "MultisigScript": [
        "(3 + 15 * 34, 3 + 16 * 34)",
        "3 + 16 * 34 > 520",
    ],
    "P2shAddress": [
        "p2sh(bytes.fromhex('0014') + H160)",
        "b58check_decode('3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM')[0]",
        "CORE_VALIDATE['3F6i6kwkevjR7AsAd4te2YB2zZyASEm1HM']['isscript']",
    ],
    "PreimageAttack": [
        "2 ** 160",
        "len(str(2 ** 160))",
    ],
    "SecondPreimageAttack": [
        "1 / 2 ** 160",
        "round(math.log2(2 ** 160))",
    ],
    "CollisionAttack": [
        "(2 ** 160) ** 0.5 == 2 ** 80",
        "round(HASHRATE * 3600 / 2 ** 80, 1)",
        "round(2 ** 128 / (2 ** 80 / 3600) / 31_557_600 / 1e9)",
        "round(2 ** 128 / HASHRATE / 31_557_600 / 1e9)",
    ],
    # ---- Address / Segwit ----
    "SegwitUpgrade": [
        "body, witness = b'transaction without its witness', b' and the witness bytes'",
        "dsha(body).hex()[:16]",
        "dsha(body + witness).hex()[:16]",
    ],
    "NestedSegwit": [
        "redeem = bytes.fromhex('0014') + H160",
        "p2sh(redeem)",
        "CORE_DERIVE.count('3FyC6EYuxW22uj4CaEGjNCjxeg7gHyFeVv')",
    ],
    "Bech32Address": [
        "segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))",
        "len(segwit_address('bc', 0, bytes.fromhex(PROG_WPKH)))",
        "segwit_decode('bc', segwit_address('bc', 0, bytes.fromhex(PROG_WPKH)))[0]",
    ],
    "WitnessVersion": [
        "(CHARSET.index('q'), CHARSET.index('p'), CHARSET.index('s'))",
        "segwit_address('bc', 16, bytes.fromhex('0000'))",
        "hex(0x50 + 1), hex(0x50 + 16)",
    ],
    "WitnessProgram": [
        "[len(bytes.fromhex(p)) for p in (PROG_WPKH, PROG_WSH, PROG_TR)]",
        "len(segwit_address('bc', 0, bytes.fromhex(PROG_WSH)))",
        "ADDR = segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))",
        "segwit_decode('bc', ADDR[:-1] + 'f') is None",
    ],
    "HumanReadablePart": [
        "ADDR = segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))",
        "ADDR.rsplit('1', 1)[0]",
        "hrp_expand('bc')",
    ],
    "BchCode": [
        "(6 * 5, 2 ** 30)",
        "1 / 2 ** 30 < 1e-9",
        "BECH32, hex(BECH32M)",
    ],
    "ErrorDetection": [
        "[i for i, (a, b) in enumerate(zip(TYPED_OK, TYPED_BAD)) if a != b]",
        "segwit_decode('bc', TYPED_BAD) is None",
        "UNDETECTED = VERIFY['substitution_errors_undetected']",
        "UNDETECTED['one'], UNDETECTED['two'], UNDETECTED['three_or_four_random_of_200000']",
    ],
    "LengthExtension": [
        "[len(a) for a in EXT]",
        "[bech_check(a) == BECH32 for a in EXT]",
        "[bech_check(a) == BECH32M for a in EXT]",
    ],
    "Bech32mAddress": [
        "segwit_address('bc', 1, bytes.fromhex(PROG_TR))",
        "bech_check(segwit_address('bc', 1, bytes.fromhex(PROG_TR))) == BECH32M",
        "bech_check(segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))) == BECH32",
    ],
    "P2wpkh": [
        "script = bytes.fromhex('0014') + H160",
        "(script.hex()[:4], len(script))",
        "segwit_address('bc', 0, H160)",
    ],
    "P2wsh": [
        "script = bytes.fromhex('0020') + bytes.fromhex(PROG_WSH)",
        "len(script)",
        "segwit_address('bc', 0, bytes.fromhex(PROG_WSH))",
    ],
    "P2tr": [
        "len(bytes.fromhex(PROG_TR))",
        "segwit_address('bc', 1, bytes.fromhex(PROG_TR))",
    ],
    # ---- Practice / Practice now ----
    "DefaultAddressType": [
        "[t for t in ('legacy', 'p2sh-segwit', 'bech32', 'bech32m') if t in CORE_ADDRESSTYPE]",
        "'default: \"bech32\"' in ' '.join(CORE_ADDRESSTYPE.split())",
        "{n: a['desc_kind'] for n, a in CORE_WALLET.items()}",
    ],
    "KeyExport": [
        "[l.split(':')[0] for l in CORE_REMOVED.splitlines()]",
        "'unknown command: dumpprivkey' in CORE_REMOVED",
        "CORE_DERIVE.count('pkh(<WIF>)')",
    ],
    "PassphraseProtection": [
        "(len(BIP38), BIP38[:2])",
        "is_valid_b58check(BIP38)",
    ],
    "DeterministicWallet": [
        "[hashlib.sha256((SEED + ' + %d\\n' % i).encode()).hexdigest()[:8] for i in range(3)]",
        "hashlib.sha256((SEED + ' + 0\\n').encode()).hexdigest()[:8]",
    ],
    "AddressReuse": [
        "reused = [p2pkh(PUB)] * 3",
        "fresh = [p2pkh(pub_bytes(ec_mul(k + i))) for i in range(3)]",
        "(len(set(reused)), len(set(fresh)))",
    ],
    "VanityAddress": [
        "[58 ** n for n in (1, 2, 3, 4)]",
        "round(58 ** 8 / 2 / 100_000 / 31_557_600, 1)",
        "58 ** 11",
    ],
    "PaperWallet": [
        "(len('%064x' % k), len(k.to_bytes(32, 'big')))",
        "CORE_VALIDATE['1LoveBPzzD72PUXLzCkYAtGFYmK5vYNR33']['isvalid']",
    ],
    "HardwareSigningDevice": [
        "steps = ['prepare', 'sign', 'broadcast']",
        "(steps.index('sign'), 'private key' in steps)",
    ],
    # ---- Practice / Assurance ----
    "TestVectors": [
        "V = VECTORS",
        "(len(V['valid_bech32m']), len(V['valid_segwit']), len(V['invalid_segwit']))",
        "VERIFY['bip350_valid_vectors'], VERIFY['bip350_invalid_vectors']",
    ],
    "IndependentCheck": [
        "V = VERIFY",
        "(V['book_addresses_toolkit'], V['book_addresses_sipa_library'], V['book_addresses_agree'])",
        "p2pkh(PUB) in CORE_DERIVE and CORE_VALIDATE[p2pkh(PUB)]['isvalid']",
        "VERIFY['core_validate_agrees_on_segwit_examples']",
    ],
    # ---- Semantics / Identifiers ----
    "KeyControlProof": [
        "challenge = int.from_bytes(hashlib.sha256(b'a fresh challenge').digest(), 'big')",
        "sig = ecdsa_sign(k, challenge, 0x27182818284590452353602874713526)",
        "ecdsa_verify(K, challenge, sig)",
        "ecdsa_verify(ec_mul(k + 1), challenge, sig)",
    ],
    "Uri": [
        "'did:example:123456789abcdefghi'.split(':')",
        "len('did:example:123456789abcdefghi'.split(':'))",
    ],
    "DecentralizedIdentifier": [
        "ABSTRACT = ' '.join(DID_ABSTRACT.split())",
        "'prove control over it without requiring permission' in ABSTRACT",
        "'verifiable, decentralized digital identity' in ABSTRACT",
    ],
}
