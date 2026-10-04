"""Every computation the SEN0401 chapter 5 lecture deck shows. The outputs come from executing these statements,
never from typing them: examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE is the chapter's own library (sen0401_ch05_wallet_lib_v1_1_0.py, the module the chapter corpus also uses,
checked against the BIP32 and BIP380 test vectors and against Bitcoin Core 31.1 by sen0401_ch05_verify_v1_1_0.py),
the values the chapter prints and the slides name, and the saved evidence in 08-tooling/ch05-evidence. Every group is
named after the concept of the chapter 5 taxonomy whose slide shows it, so that a slide and its computation cannot
drift apart. deck_check_v1_0_0.py re-runs every '>>>' line of the finished deck in this same namespace.
"""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))
EVID = os.path.join(TOOLING, "ch05-evidence")

PRELUDE = """
import sys, json, math
sys.path.insert(0, %r)
from sen0401_ch05_wallet_lib_v1_1_0 import *          # hashlib, hmac, unicodedata come with it
EVID = %r

# the chapter's own worked example: 128 bits of entropy, its twelve words, its passphrase
ENT = '0c1e24e5917779d297e14d45f14e1a1a'
WORDS = 'army van defense carry jealous true garbage claim echo media make crunch'
PASSPHRASE = 'SuperDuperSecret'
BOOK_SEED = 'f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73'   # the chapter's hashed-seed example

# BIP32's first test vector, and the extended keys the chapter prints
TV = bytes.fromhex('000102030405060708090a0b0c0d0e0f')
BOOK_XPRV = ('xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67L'
             'ctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9c')
BOOK_XPUB = ('xpub67xpozcx8pe95XVuZLHXZeG6XWXHpGq6Qv5cmNfi7cS5mtjJ2tgypeQbB'
             's2UAR6KECeeMVKZBPLrtJunSDMstweyLXhRgPxdp14sk9tJPW9')

# the recovery code of BIP84's test vector, and the descriptor Bitcoin Core 31.1 derived from it
B84 = ('abandon abandon abandon abandon abandon abandon abandon abandon '
       'abandon abandon abandon about')
DESC = ('wpkh([73c5da0a/84h/0h/0h]xpub6CatWdiZiodmUeTDp8LT5or8nmbKNcuyvz7WyksVFkKB4RHwCD3Xyuv'
        'PEbvqAQY3rAPshWcMLoP2fMFMKHPJ4ZeZXYVUhLv1VMrjPC7PW6V/0/*)')
C32 = 'ms10testsxxxxxxxxxxxxxxxxxxxxxxxxxx4nzvca9cmczlw'    # BIP93's own unshared example

_rd = lambda n: open(EVID + '/' + n, encoding='utf-8', errors='replace').read()
_js = lambda n: json.load(open(EVID + '/' + n, encoding='utf-8'))
CORE_WALLET = _js('core_fresh_wallet_31_1_v1_0_0.json')
CORE_DESCINFO = _js('core_getdescriptorinfo_31_1_v1_0_0.json')['getdescriptorinfo']
CORE_BIP84 = _js('core_deriveaddresses_bip84_31_1_v1_0_0.json')
CORE_KEYPOOL = _rd('core_help_keypool_31_1_v1_0_0.txt')
CORE_BACKUP = _rd('core_help_backupwallet_31_1_v1_0_0.txt')
CORE_LISTDESC = _rd('core_help_listdescriptors_31_1_v1_0_0.txt')
CORE_DESCDOC = _rd('core_doc_descriptors.md')
BIP39_DOC = _rd('bip-0039.mediawiki')
BIP32_DOC = _rd('bip-0032.mediawiki')
BIP329_DOC = _rd('bip-0329.mediawiki')
BIP380_DOC = _rd('bip-0380.mediawiki')
BIP389_DOC = _rd('bip-0389.mediawiki')
BIP379_DOC = _rd('bip-0379.md')
BIP93_DOC = _rd('bip-0093.mediawiki')
SLIP39_DOC = _rd('slip-0039.md')
AEZEED = _rd('aezeed_README.md')
ELECTRUM = _rd('electrum_seeds.rst')
LND = _rd('lnd_recovery.md')
MUUN = _rd('muun_recovery_README.md')
LOPP = _rd('lopp_attacks.md')
BTCPAY = _rd('btcpayserver_README.md')
TREZOR = _js('trezor_vectors.json')
flat = lambda t: ' '.join(t.split())
""" % (TOOLING, EVID)

# One group per concept of the chapter 5 taxonomy; the key is the concept identifier the corpus uses.
EX = {
    # ---- Wallet keys / Wallet contents ----
    "WalletDatabase": [
        "len(CORE_WALLET['descriptors'])",
        "sorted({d['desc'][:d['desc'].index('(')] for d in CORE_WALLET['descriptors']})",
        "sum(d['range'][1] - d['range'][0] + 1 for d in CORE_WALLET['descriptors'])",
    ],
    "PublicKeyOnlyWallet": [
        "acct = parse_extended(BOOK_XPUB)",
        "K0, c0 = ckd_pub(decompress(acct['key']), acct['chain'], 0)",
        "p2wpkh_address(ser_p(K0))",
        "acct['key'][0]",
    ],
    "ExternalSigning": [
        "z = int.from_bytes(hashlib.sha256(b'an unsigned transaction').digest(), 'big')",
        "device_key, _ = keys_at(B84, 'm/84h/0h/0h/0/0')",
        "sig = ecdsa_sign(device_key, z, 0x27182818284590452353602874713526)",
        "ecdsa_verify(ec_mul(device_key), z, sig)",
    ],
    # ---- Wallet keys / Key generation methods ----
    "IndependentKeyGeneration": [
        "32 * 1000",
        "32 * 1001 - 32 * 1000",
    ],
    "Seed": [
        "len(bytes.fromhex(BOOK_SEED)) * 8",
        "len(mnemonic_to_seed(WORDS)) * 8",
    ],
    "DeterministicKeyGeneration": [
        "line = lambda i: (BOOK_SEED + ' + %d\\n' % i).encode()",
        "[hashlib.sha256(line(i)).hexdigest()[:8] for i in range(3)]",
        "hashlib.sha256((BOOK_SEED + ' + 0\\n').encode()).hexdigest()[:8]",
    ],
    "KeyTweak": [
        "ec_mul(5 + 123) == ec_add(ec_mul(5), ec_mul(123))",
        "ser_p(ec_add(ec_mul(5), ec_mul(123))) == ser_p(ec_mul(128))",
    ],
    "HdKeyGeneration": [
        "2 ** 31 + 2 ** 31",
        "len(path_indices('m/84h/0h/0h/0/0'))",
    ],
    # ---- Recovery codes / Recovery code schemes ----
    "Bip39Code": [
        "entropy_to_mnemonic(bytes.fromhex(ENT))",
        "mnemonic_to_entropy(WORDS)[0].hex()",
        "mnemonic_to_entropy(WORDS)[1]",
    ],
    "ElectrumV2Code": [
        "132 // 11",
        "electrum_hash(WORDS)[:8]",
        "electrum_has_version(WORDS, '01'), electrum_has_version(WORDS, '100')",
    ],
    "AezeedCode": [
        "1 + 2 + 16",
        "(19 + 8 + 1 + 5) * 8 // 11",
        "'wallet birthday' in flat(AEZEED).lower()",
    ],
    "MuunCode": [
        "'This process requires no collaboration from Muun to work' in flat(MUUN)",
        "'transfer all funds out of your Muun account' in flat(MUUN)",
    ],
    "Slip39Code": [
        "SHARES = shamir_split(0x1337c0de, 3, 5, [11, 22])",
        "[x for x, y in SHARES]",
        "shamir_combine(SHARES[:3]) == 0x1337c0de",
        "shamir_combine(SHARES[:2]) == 0x1337c0de",
    ],
    "Codex32Code": [
        "len(C32)",
        "codex32_check(C32)",
        "codex32_payload(C32).hex()",
    ],
    # ---- Recovery codes / Choices behind a recovery code ----
    "RecoveryPassphrase": [
        "mnemonic_to_seed(WORDS).hex()[:16]",
        "mnemonic_to_seed(WORDS, PASSPHRASE).hex()[:16]",
    ],
    "PlausibleDeniability": [
        "[mnemonic_to_seed(WORDS, p).hex()[:12] for p in ('', 'wrong', 'also wrong')]",
        "{len(mnemonic_to_seed(WORDS, p)) for p in ('', 'wrong', 'also wrong')}",
    ],
    "Brainwallet": [
        "(2048 ** 12).bit_length() - 1",
        "128 + 128 // 32",
    ],
    "Memorization": [
        "(len(ENT), len(WORDS.split()))",
        "max(len(w) for w in WORDS.split())",
    ],
    "PhysicalCoercion": [
        "'this list is not comprehensive' in flat(LOPP).lower()",
        "'many attacks are not publicly reported' in flat(LOPP)",
    ],
    "WalletBirthday": [
        "2009 + 2 ** 16 // 365",
        "'Bitcoin Days Genesis' in flat(AEZEED)",
    ],
    # ---- The BIP39 stack / Generating a recovery code ----
    "Entropy": [
        "len(bytes.fromhex(ENT)) * 8",
        "round(math.log10(2 ** 128), 1)",
    ],
    "Bip39Checksum": [
        "digest = hashlib.sha256(bytes.fromhex(ENT)).digest()",
        "bin(digest[0])[2:].zfill(8)[:4]",
        "128 // 32",
    ],
    "WordList": [
        "2 ** 11, len(wordlist())",
        "[wordlist()[i] for i in (96, 1929, 459)]",
        "sorted(wordlist()) == wordlist()",
    ],
    "BitSegment": [
        "bits = bin(int.from_bytes(bytes.fromhex(ENT), 'big'))[2:].zfill(128)",
        "[int(bits[i:i + 11], 2) for i in range(0, 33, 11)]",
        "WORDS.split()[:3]",
    ],
    "CodeLength": [
        "[(e, e // 32, (e + e // 32) // 11) for e in (128, 160, 192, 224, 256)]",
    ],
    "TextNormalization": [
        "(len('\\u00e9'), len(unicodedata.normalize('NFKD', '\\u00e9')))",
        "unicodedata.normalize('NFKD', '\\u00e9').encode().hex()",
    ],
    # ---- The BIP39 stack / From the code to the seed ----
    "KeyStretchingFunction": [
        "32768 // 2048",
        "round(math.log2(2048), 1)",
    ],
    "Pbkdf2": [
        "mnemonic_to_seed(WORDS).hex()[:16]",
        "len(mnemonic_to_seed(WORDS))",
        "hashlib.pbkdf2_hmac('sha512', 'words', b'mnemonic', 2048)",
    ],
    "Salt": [
        "hashlib.pbkdf2_hmac('sha512', WORDS.encode(), b'mnemonic', 2048).hex()[:16]",
        "salted = b'mnemonic' + PASSPHRASE.encode()",
        "hashlib.pbkdf2_hmac('sha512', WORDS.encode(), salted, 2048).hex()[:16]",
    ],
    "RootSeed": [
        "512 // 8",
        "len(mnemonic_to_seed(WORDS))",
    ],
    "Bip39Passphrase": [
        "mnemonic_to_seed(WORDS, PASSPHRASE).hex()[:16]",
        "mnemonic_to_seed(WORDS, 'SuperDuperSecre').hex()[:16]",
    ],
    "SecurityStrength": [
        "[(2 ** b - 1).bit_length() for b in (512, 256, 128)]",
        "round(math.log10(2 ** 128), 1)",
    ],
    # ---- Hierarchical deterministic wallet / Master keys ----
    "HmacSha512": [
        "I = hmac.new(b'Bitcoin seed', TV, hashlib.sha512).digest()",
        "(len(I), I.hex()[:16])",
        "hmac.new('Bitcoin seed', TV, hashlib.sha512)",
    ],
    "MasterPrivateKey": [
        "k, c = master(TV)",
        "'%064x' % k",
        "0 < k < N",
    ],
    "MasterChainCode": [
        "k, c = master(TV)",
        "c.hex()",
        "len(c) * 8",
    ],
    # ---- Hierarchical deterministic wallet / Deriving child keys ----
    "ChildKeyDerivation": [
        "(512 // 2, 512 // 2 // 8)",
        "k, c = master(TV)",
        "k1, c1 = ckd_priv(k, c, 0)",
        "(len(c1), k1 < N)",
    ],
    "ChainCode": [
        "k, c = master(TV)",
        "len(c) * 8",
        "ckd_priv(k, c, 0)[1] != c",
    ],
    "IndexNumber": [
        "(2 ** 31 - 1, 2 ** 31, 2 ** 32 - 1)",
        "path_indices(\"m/0'/1\")",
    ],
    "PrivateChildDerivation": [
        "k, c = master(TV)",
        "k1, c1 = ckd_priv(k, c, 0)",
        "'%064x' % k1",
    ],
    "HardenedDerivation": [
        "k, c = master(TV)",
        "kh, ch = ckd_priv(k, c, 2 ** 31)",
        "'%064x' % kh",
        "ckd_priv(k, c, 0)[0] == kh",
    ],
    "PublicChildDerivation": [
        "k, c = master(TV)",
        "k1, c1 = ckd_priv(k, c, 0)",
        "ckd_pub(ec_mul(k), c, 0) == (ec_mul(k1), c1)",
        "ckd_pub(ec_mul(k), c, 2 ** 31)",
    ],
    "ChildKeyIndependence": [
        "2 ** 31 - 1",
        "k, c = master(TV)",
        "k1, c1 = ckd_priv(k, c, 0)",
        "leak_parent_private_key(ec_mul(k), c, 0, k1) == k",
    ],
    # ---- Hierarchical deterministic wallet / Extended keys ----
    "ExtendedKey": [
        "4 + 1 + 4 + 4 + 32 + 33",
        "len(b58check_decode(BOOK_XPUB))",
    ],
    "ExtendedPrivateKey": [
        "d = parse_extended(BOOK_XPRV)",
        "(d['version'].hex(), d['depth'], d['index'])",
        "(d['key'][0], len(d['key']))",
    ],
    "ExtendedPublicKey": [
        "len(BOOK_XPUB)",
        "d = parse_extended(BOOK_XPUB)",
        "(d['version'].hex(), d['key'][0])",
    ],
    "ExtendedKeyEncoding": [
        "xprv, xpub = derive_serialized(TV, 'm')",
        "(xprv[:4], xpub[:4])",
        "(len(xprv), len(xpub))",
        "parse_extended('xprv9tyUQV64JT5qs')",
    ],
    "KeyFingerprint": [
        "k, c = master(TV)",
        "fingerprint(ec_mul(k)).hex()",
        "len('3442193e') * 4",
    ],
    # ---- Hierarchical deterministic wallet / Navigating the tree ----
    "KeyPath": [
        "path_indices('m/84h/0h/0h/0/2')",
        "[i - 2 ** 31 for i in path_indices('m/84h/0h/0h')]",
    ],
    "Bip43Purpose": [
        "hex(2 ** 31 + 44)",
        "[hex(2 ** 31 + p) for p in (44, 49, 84, 86)]",
    ],
    "Bip44Structure": [
        "LEVELS = 'purpose / coin_type / account / change / address_index'.split(' / ')",
        "len(LEVELS)",
        "[i >= 2 ** 31 for i in path_indices('m/44h/0h/0h/0/2')]",
    ],
    "AccountBranch": [
        "['m/44h/0h/%dh' % a for a in (0, 1)]",
        "path_indices('m/44h/0h/1h')[2] - 2 ** 31",
    ],
    "ChangeBranch": [
        "'M/44h/0h/%dh/%d/%d' % (3, 1, 14)",
        "path_indices('m/44h/0h/3h/1/14')[3:]",
    ],
    "AddressIndex": [
        "'M/44h/0h/0h/0/%d' % (3 - 1)",
        "'(default: 1000)' in flat(CORE_KEYPOOL)",
    ],
    # ---- Backing up derivation paths / Implicit and explicit paths ----
    "ImplicitPath": [
        "PATHS = {44: 'P2PKH', 49: 'nested P2WPKH', 84: 'P2WPKH', 86: 'P2TR'}",
        "[path_indices('m/%dh/0h/0h' % p)[0] - 2 ** 31 for p in PATHS]",
        "list(PATHS.values())",
    ],
    "ExplicitPath": [
        "DESC[:DESC.index('(')]",
        "parse_origin(DESC)[0]",
        "DESC[-5:]",
    ],
    "StandardPath44": [
        "'m/%dh/0h/0h' % 44",
        "CORE_WALLET['descriptors'][0]['desc'][:40]",
    ],
    "StandardPath49": [
        "hex(2 ** 31 + 49)",
        "[d['desc'][:12] for d in CORE_WALLET['descriptors'] if '49h' in d['desc']][0]",
    ],
    "StandardPath84": [
        "k0, c0 = keys_at(B84, 'm/84h/0h/0h/0/0')",
        "p2wpkh_address(ser_p(ec_mul(k0)))",
        "CORE_BIP84['addresses'][0]",
        "p2wpkh_address(ser_p(ec_mul(k0))) == CORE_BIP84['addresses'][0]",
    ],
    "StandardPath86": [
        "k0, c0 = keys_at(B84, 'm/86h/0h/0h/0/0')",
        "p2tr_address(taproot_output_key(ser_p(ec_mul(k0))))",
    ],
    "Multisignature": [
        "math.comb(3, 2)",
        "[sorted(s) for s in ((1, 2), (1, 3), (2, 3))]",
    ],
    # ---- Backing up derivation paths / Output script descriptors ----
    "OutputScript": [
        "k0, c0 = keys_at(B84, 'm/84h/0h/0h/0/0')",
        "script = bytes.fromhex('0014') + hash160(ser_p(ec_mul(k0)))",
        "(script.hex()[:4], len(script))",
    ],
    "OutputScriptDescriptor": [
        "DESC[:DESC.index('(')]",
        "DESC[DESC.index('['):DESC.index(']') + 1]",
        "DESC[-5:]",
    ],
    "DescriptorChecksum": [
        "descsum_create('raw(deadbeef)')",
        "len(descsum_create(DESC).split('#')[1])",
        "descsum_create(DESC)[-9:] == '#afwvtk2s'",
    ],
    "KeyOrigin": [
        "parse_origin(DESC)",
        "[i - 2 ** 31 for i in parse_origin(DESC)[1]]",
    ],
    "MultipathDescriptor": [
        "m = 'wpkh([73c5da0a/84h/0h/0h]xpub.../<0;1>/*)'",
        "head, rest = m.split('<'); choices, tail = rest.split('>')",
        "[head + ch + tail for ch in choices.split(';')]",
    ],
    "Miniscript": [
        "[4 - i for i in range(4)]",
        "'thresh(' in CORE_DESCDOC",
        "'Miniscript' in BIP379_DOC",
    ],
    # ---- Backing up data that is not keys / Labels and notes ----
    "AddressLabel": [
        "record = {'type': 'addr', 'ref': CORE_BIP84['addresses'][0], 'label': 'order 1041'}",
        "(record['type'], record['label'])",
        "'privacy sensitive nature of the data' in flat(BIP329_DOC)",
    ],
    "TransactionLabel": [
        "round(0.00100 - 0.00075, 5)",
        "round(0.00100 - 0.00075, 5) == 0.00025",
    ],
    "LabelExportFormat": [
        "record = {'type': 'addr', 'ref': 'bc1qcr8te4k...', 'label': 'order 1041'}",
        "json.dumps(record, sort_keys=True)",
        "'JSON Lines' in BIP329_DOC or 'JSONL' in BIP329_DOC",
    ],
    # ---- Backing up data that is not keys / Other data a wallet keeps ----
    "LightningNetwork": [
        "'On-Chain Recovery' in LND and 'Off-Chain Recovery' in LND",
        "'payment channel' in flat(LND).lower()",
    ],
    "StaticChannelBackup": [
        "'channel.backup' in LND",
        "'static channel backup' in flat(LND).lower()",
    ],
    "Encryption": [
        "key = hashlib.sha256(bytes.fromhex('5b56c417303faa3f') + b'backup').digest()",
        "note = b'Paid Bob for podcast'",
        "hidden = bytes(a ^ b for a, b in zip(note, key))",
        "hidden.hex()[:16]",
        "bytes(a ^ b for a, b in zip(hidden, key)).decode()",
    ],
    "EncryptedWalletBackup": [
        "seed = mnemonic_to_seed(WORDS)",
        "hashlib.sha256(seed[:8] + b'backup').hexdigest()[:8]",
        "hashlib.sha256(bytes.fromhex('5b56c417303faa3f') + b'backup').hexdigest()[:8]",
    ],
    # ---- Deploying keys in practice / An extended key on a web store ----
    "XpubDeployment": [
        "['M/84h/0h/0h/0/%d' % i for i in range(3)]",
        "acct = parse_extended(BOOK_XPUB)",
        "K, ch = decompress(acct['key']), acct['chain']",
        "[p2wpkh_address(ser_p(pub_at(K, ch, '0/%d' % i)[0])) for i in range(2)]",
    ],
    "GapLimit": [
        "scan_with_gap({0, 3, 25}, 20)",
        "scan_with_gap({0, 3, 25}, 30)",
    ],
    "PaymentProcessor": [
        "'free and open-source, self-hosted Bitcoin payment processor' in flat(BTCPAY)",
        "'without fees or intermediaries' in flat(BTCPAY)",
    ],
    # ---- Deploying keys in practice / Keys kept offline ----
    "ColdStorage": [
        "(parse_extended(BOOK_XPUB)['key'][0], parse_extended(BOOK_XPRV)['key'][0])",
        "parse_extended(BOOK_XPUB)['chain'] == parse_extended(BOOK_XPRV)['chain']",
    ],
    "HardwareSigningDevice": [
        "k0, c0 = keys_at(B84, 'm/84h/0h/0h/0/0')",
        "z = int.from_bytes(hashlib.sha256(b'pay 0.01 BTC to bc1q...').digest(), 'big')",
        "sig = ecdsa_sign(k0, z, 0x14142135623730950488016887242097)",
        "(ecdsa_verify(ec_mul(k0), z, sig), ecdsa_verify(ec_mul(k0), z + 1, sig))",
    ],
    "WrittenBackup": [
        "(len(ENT), len(WORDS.split()))",
        "(len(ENT) * 4, len(mnemonic_to_entropy(WORDS)[0]) * 8)",
    ],
    # ---- Foundations / Cryptographic primitives ----
    "HashFunction": [
        "hashlib.sha256(b'abc').hexdigest()[:8]",
        "hashlib.sha256(b'abd').hexdigest()[:8]",
        "hashlib.sha256(b'abc').hexdigest()[:8]",
    ],
    "ShaAlgorithm": [
        "(len(hashlib.sha256(b'').digest()), len(hashlib.sha512(b'').digest()))",
        "len(hmac.new(b'Bitcoin seed', TV, hashlib.sha512).digest())",
    ],
    "DigitalSignature": [
        "k0, c0 = keys_at(B84, 'm/84h/0h/0h/0/0')",
        "z = int.from_bytes(hashlib.sha256(b'a transaction').digest(), 'big')",
        "r, s = ecdsa_sign(k0, z, 0x16180339887498948482045868343656)",
        "ecdsa_verify(ec_mul(k0), z, (r, s))",
    ],
    "SecretSharing": [
        "SHARES = shamir_split(0x1337c0de, 3, 5, [11, 22])",
        "len(SHARES)",
        "shamir_combine([SHARES[0], SHARES[2], SHARES[4]]) == 0x1337c0de",
        "shamir_combine([SHARES[0], SHARES[2]]) == 0x1337c0de",
    ],
    # ---- Foundations / Recovery as a practice ----
    "DataLoss": [
        "'Safely copies the current wallet file' in flat(CORE_BACKUP)",
        "'(default: 1000)' in flat(CORE_KEYPOOL)",
    ],
    "BackupTesting": [
        "mnemonic_to_seed(WORDS) == mnemonic_to_seed(WORDS)",
        "mnemonic_to_entropy(WORDS)[1]",
        "mnemonic_to_entropy(WORDS.replace('crunch', 'cruise'))[1]",
    ],
}
