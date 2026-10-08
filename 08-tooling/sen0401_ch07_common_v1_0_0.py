#!/usr/bin/env python3
"""Shared parts of the SEN0401 chapter 7 corpus (version 1.0.0): the writing-guide facets, the citation markers, the source list
(one entry per source read; the research record is generated from it), the builders of the executed claims and the small programs a
worked example runs in the reader's browser (a stack machine of Script words, an ECDSA verifier, Base58Check). Used by
sen0401_ch07_text_*_v1_0_0.py and sen0401_ch07_corpus_v1_0_0.py. Python standard library only. Follows chapter 6's
sen0401_ch06_common_v1_0_0.py; the sources and the library (sen0401_ch07_script_lib_v1_0_0.py) are this chapter's."""
__version__ = "1.0.0"
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))
W, Y, E, H, K = "What it is", "Why it matters", "Where you meet it", "How it works", "Watch out"

GH = "https://raw.githubusercontent.com/"
CORE_C = "05bc2f53ce0cb239c17dbdd6b261bd2db7d2a940"
BOOK_C = "275c4eb8eab8800c6adc39f8def8e8f8fa356a57"
_core = lambda f: GH + "bitcoin/bitcoin/" + CORE_C + "/" + f
def _bip(n, title, auth, status, year, ext="mediawiki"):
    return ("B%d" % int(n), auth.split(" and ")[0].split(",")[0].split()[-1] + (" et al." if ("," in auth or " and " in auth) else "") + ", " + str(year),
            "BIP%d, %s, the BIPs repository (%s, assigned %s), status %s" % (int(n), title, auth, year, status),
            GH + "bitcoin/bips/master/bip-%04d.%s" % (int(n), ext), "secondary", "ev:bip-%04d.%s" % (int(n), ext))
def _book(m, ch, what, role="secondary"):
    return (m, "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - %s (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8)" % what,
            GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/" + ch, role, "book:" + ch)
def _core_src(m, f, what):
    return (m, "Bitcoin Core, 2026", "Bitcoin Core source at commit 05bc2f5: %s (Bitcoin Core, 2026)" % what, _core(f), "secondary", "ev:core_" + f.replace("/", "_"))
# (marker, author-year string, label of the publication, url, role, saved copy, one entry per source read)
SOURCES = [
 ("AH", "Antonopoulos and Harding, 2023", "Mastering Bitcoin, 3rd edition - Chapter 7, Authorization and Authentication (Antonopoulos and Harding, 2023; O'Reilly; CC BY-SA 4.0; commit 275c4eb8)", GH + "bitcoinbook/bitcoinbook/" + BOOK_C + "/ch07_authorization-authentication.adoc", "primary", "ev:book_ch07_authorization-authentication.adoc"),
 _book("AH6", "ch06_transactions.adoc", "Chapter 6, Transactions: inputs, outputs, the sequence field, the witness structure and lock time"),
 _book("AH8", "ch08_signatures.adoc", "Chapter 8, Digital Signatures: ECDSA, schnorr, signature hashes and hash types"),
 _book("AH4", "ch04_keys.adoc", "Chapter 4, Keys and Addresses: compressed public keys, Base58Check, bech32"),
 _book("AH9", "ch09_fees.adoc", "Chapter 9, Fees: the timelock defense against fee sniping"),
 _book("AHG", "glossary.asciidoc", "Glossary"),
 _bip(11, "M-of-N Standard Transactions", "Gavin Andresen", "Deployed", 2011),
 _bip(13, "Address Format for pay-to-script-hash", "Gavin Andresen", "Deployed", 2011),
 _bip(16, "Pay to Script Hash", "Gavin Andresen", "Deployed", 2012),
 _bip(32, "Hierarchical Deterministic Wallets", "Pieter Wuille", "Deployed", 2012),
 _bip(65, "OP_CHECKLOCKTIMEVERIFY", "Peter Todd", "Deployed", 2014),
 _bip(66, "Strict DER signatures", "Pieter Wuille", "Deployed", 2015),
 _bip(68, "Relative lock-time using consensus-enforced sequence numbers", "Mark Friedenbach, BtcDrak, Nicolas Dorier and kinoshitajona", "Deployed", 2015),
 _bip(86, "Key Derivation for Single Key P2TR Outputs", "Ava Chow", "Deployed", 2021),
 _bip(112, "CHECKSEQUENCEVERIFY", "BtcDrak, Mark Friedenbach and Eric Lombrozo", "Deployed", 2015),
 _bip(114, "Merkelized Abstract Syntax Tree", "Johnson Lau", "Closed", 2016),
 _bip(116, "MERKLEBRANCHVERIFY", "Mark Friedenbach, Kalle Alm and BtcDrak", "Draft", 2017),
 _bip(141, "Segregated Witness (Consensus layer)", "Eric Lombrozo, Johnson Lau and Pieter Wuille", "Deployed", 2015),
 _bip(143, "Transaction Signature Verification for Version 0 Witness Program", "Johnson Lau and Pieter Wuille", "Deployed", 2016),
 _bip(146, "Dealing with signature encoding malleability", "Johnson Lau and Pieter Wuille", "Closed", 2016),
 _bip(147, "Dealing with dummy stack element malleability", "Johnson Lau", "Deployed", 2016),
 _bip(173, "Base32 address format for native v0-16 witness outputs", "Pieter Wuille and Greg Maxwell", "Deployed", 2017),
 _bip(327, "MuSig2 for BIP340-compatible Multi-Signatures", "Jonas Nick, Tim Ruffing and Elliott Jin", "Deployed", 2022),
 _bip(340, "Schnorr Signatures for secp256k1", "Pieter Wuille, Jonas Nick and Tim Ruffing", "Deployed", 2020),
 _bip(341, "Taproot: SegWit version 1 spending rules", "Pieter Wuille, Jonas Nick and Anthony Towns", "Deployed", 2020),
 _bip(342, "Validation of Taproot Scripts", "Pieter Wuille, Jonas Nick and Anthony Towns", "Deployed", 2020),
 _bip(350, "Bech32m format for v1+ witness addresses", "Pieter Wuille", "Deployed", 2020),
 _bip(379, "Miniscript", "Pieter Wuille, Andrew Poelstra, Sanket Kanjalkar, Antoine Poinsot and Ava Chow", "Draft", 2023, "md"),
 _core_src("BCI", "src/script/interpreter.cpp", "src/script/interpreter.cpp, EvalScript, VerifyScript and the signature hashes"),
 _core_src("BCH", "src/script/interpreter.h", "src/script/interpreter.h, the script verification flags and the signature hash types"),
 _core_src("BCS", "src/script/script.h", "src/script/script.h, the opcodes and the script limits"),
 _core_src("BCC", "src/script/script.cpp", "src/script/script.cpp, the opcode names and the sigop counting"),
 _core_src("BCE", "src/script/script_error.h", "src/script/script_error.h, the named script errors"),
 _core_src("BCV", "src/script/solver.cpp", "src/script/solver.cpp, the standard script templates and the multisignature solver"),
 _core_src("BCP", "src/policy/policy.cpp", "src/policy/policy.cpp, the relay policy - standard scripts, the data carrier"),
 _core_src("BCQ", "src/policy/policy.h", "src/policy/policy.h, the standardness constants and the standard verification flags"),
 _core_src("BCK", "src/consensus/consensus.h", "src/consensus/consensus.h, MAX_BLOCK_SIGOPS_COST and the other consensus constants"),
 _core_src("BCL", "src/kernel/chainparams.cpp", "src/kernel/chainparams.cpp, the mainnet activation heights"),
 _core_src("BCA", "src/consensus/params.h", "src/consensus/params.h, the deployment parameters"),
 _core_src("BCU", "src/pubkey.cpp", "src/pubkey.cpp, the strict encodings of keys and signatures"),
 _core_src("BCG", "src/script/sign.cpp", "src/script/sign.cpp, the signing of the standard templates"),
 ("BCD", "Bitcoin Core, 2026", "Bitcoin Core documentation: doc/bips.md at commit 05bc2f5, the proposals the project implements and when (Bitcoin Core, 2026)", _core("doc/bips.md"), "secondary", "ev:core_doc_bips.md"),
 ("BCJ", "Bitcoin Core, 2026", "Bitcoin Core test data at commit 05bc2f5: src/test/data/script_tests.json, 1,292 rows of which 1,237 are script tests, and src/test/data/sighash.json, 500 signature hash vectors (Bitcoin Core, 2026)", _core("src/test/data/script_tests.json"), "secondary", "git:src/test/data/script_tests.json"),
 ("BCW", "Bitcoin Core, 2026", "Bitcoin Core test data at commit 05bc2f5: src/test/data/bip341_wallet_vectors.json, the wallet test vectors of BIP341 (Bitcoin Core, 2026)", _core("src/test/data/bip341_wallet_vectors.json"), "secondary", "git:src/test/data/bip341_wallet_vectors.json"),
 ("O0", "Nakamoto, 2010", "Bitcoin 0.3.0 source, tag v0.3.0, script.cpp: the script engine as first released, in which the input and output scripts are joined and OP_RETURN jumps to the end (Nakamoto, 2010)", GH + "bitcoin/bitcoin/v0.3.0/script.cpp", "secondary", "ev:old_bitcoin_v0.3.0_script.cpp"),
 ("O0M", "Nakamoto, 2010", "Bitcoin 0.3.0 source, tag v0.3.0, main.cpp: the transaction check that calls the script engine (Nakamoto, 2010)", GH + "bitcoin/bitcoin/v0.3.0/main.cpp", "secondary", "ev:old_bitcoin_v0.3.0_main.cpp"),
 ("O7", "Nakamoto, 2010", "Bitcoin 0.3.7 source, tag v0.3.7, script.cpp: the script engine after the repair, in which VerifyScript evaluates the two scripts one after the other and OP_RETURN fails (Nakamoto, 2010)", GH + "bitcoin/bitcoin/v0.3.7/script.cpp", "secondary", "ev:old_bitcoin_v0.3.7_script.cpp"),
 ("CVE", "Bitcoin Wiki, 2026", "Bitcoin Wiki, Common Vulnerabilities and Exposures: the entry CVE-2010-5141, 2010-07-28, wxBitcoin and bitcoind, 'OP_RETURN could be used to spend any output' (Bitcoin Wiki contributors, 2026)", "https://en.bitcoin.it/wiki/Common_Vulnerabilities_and_Exposures", "secondary", "ev:bitcoinwiki_common_vulnerabilities_v1_0_0.txt"),
 ("MP", "mempool.space, 2026", "mempool.space, an open-source block explorer: the first 599 non-coinbase transactions of block 775,072 with the output each input spends, fetched 2026-10-08 (mempool.space, 2026)", "https://mempool.space/api/block/000000000000000000027d39da52dd790d98f85895b02e764611cb7acf552e90/txs/0", "secondary", "ev:mainnet_block775072_census_v1_0_0.json"),
 ("ML", "mempool.space, 2026", "mempool.space, an open-source block explorer: three landmark transactions - the first payment between people (block 170), the pizza payment, and Alice's payment of chapter 6 - with the outputs they spend, fetched 2026-10-08 (mempool.space, 2026)", "https://mempool.space/api/tx/f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16", "secondary", "ev:mainnet_landmarks_v1_0_0.json"),
 _core_src("BCT", "src/consensus/tx_verify.cpp", "src/consensus/tx_verify.cpp, IsFinalTx and the relative lock-time (sequence lock) calculation"),
 _core_src("BCX", "src/primitives/transaction.h", "src/primitives/transaction.h, the sequence constants and flags of a transaction input"),
 ("MA", "mempool.space, 2026", "mempool.space, an open-source block explorer: the six blocks at the heights where the soft forks of this chapter took effect on mainnet - 227,931, 363,725, 388,381, 419,328, 481,824 and 709,632 - fetched 2026-10-08 (mempool.space, 2026)", "https://mempool.space/api/block-height/709632", "secondary", "ev:mainnet_activation_blocks_v1_0_0.json"),
 ("AL", "Altunel, 2021", "Course notes: Chapter_7_AdvancedTransactionsAndScripting.pptx, SEN0401 (then CSE0469) Blockchain, Yusuf Altunel, 2021 - based on Mastering Bitcoin 2nd edition; the owner's file in 03-materials/owner-legacy-2025 (sha256 e10d9fd80b59aa30)", "urn:sen0401:course-notes:Chapter_7_AdvancedTransactionsAndScripting.pptx:e10d9fd80b59aa30", "secondary", "file:../03-materials/owner-legacy-2025/slides-2025/Chapter_7_AdvancedTransactionsAndScripting_v1_0_0.pptx"),
]
CITE = {s[0]: s[1] for s in SOURCES}
_MARK = dict(CITE)
def c(t):
    for k in sorted(_MARK, key=len, reverse=True): t = t.replace(" [" + k + "]", " (" + _MARK[k] + ")")
    bad = re.findall(r" \[[A-Z0-9]{2,5}\]", t)
    assert not bad, (bad, t[:120])
    return t
def P(*items):
    """paragraph list: items are (facet, text) pairs; markers are resolved"""
    return [(f, c(t)) for f, t in items]

# ---- builders of the executed claims (each result is an expression the chapter builder evaluates) ----
_LIBS = "__import__('sys').path.insert(0, %r)" % HERE
def _CL(): return "(%s or __import__('sen0401_ch07_checklib_v1_0_0'))" % _LIBS
def _SL(): return "(%s or __import__('sen0401_ch07_script_lib_v1_0_0'))" % _LIBS
def Qb(name, *phrases): return ("%s.has_book(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")      # phrases in a chapter of the book
def Qe(name, *phrases): return ("%s.has_ev(%r%s)" % (_CL(), name, "".join(", %r" % p for p in phrases)), "True")        # phrases in a source saved in ch07-evidence
def Qc(path, *phrases): return ("%s.has_core(%r%s)" % (_CL(), path, "".join(", %r" % p for p in phrases)), "True")        # in a file of Bitcoin Core at the pinned commit
def X(expr, expected):
    """an executed claim: expr is evaluated with L = the chapter 7 script library and C = the check library"""
    return ("(lambda L, C: %s)(%s, %s)" % (expr, _SL(), _CL()), repr(expected))
CL, SL = _CL, _SL
def Pp(name, *phrases): return ("%s.has_pptx(%r%s)" % (_CL(), "../03-materials/owner-legacy-2025/slides-2025/" + name, "".join(", %r" % p for p in phrases)), "True")
def PROG(code, var="result"):
    """a small program (several statements) as one expression: its variable `result`. The page runs a worked example in the
    reader's browser, so such a program uses the standard library only and reads no files."""
    return "(lambda g: (exec(%r, g), g[%r])[1])({})" % (code, var)

# ---- programs a worked example runs in the browser (standard library only; RIPEMD-160 is not available there, so a program that needs
# a HASH160 is given the hash) ----
MINI = '''import hashlib
def enc(n):                                  # a script number: little-endian, the sign in the top bit of the last byte
    a, out = abs(n), bytearray()
    while a: out.append(a & 255); a >>= 8
    if out and out[-1] & 0x80: out.append(0x80 if n < 0 else 0)
    elif out and n < 0: out[-1] |= 0x80
    return bytes(out)
def dec(b): return -int.from_bytes(b[:-1] + bytes([b[-1] & 0x7f]), 'little') if b and b[-1] & 0x80 else int.from_bytes(b, 'little')
def true(b): return any(b[:-1]) or (len(b) > 0 and b[-1] not in (0, 0x80))
def run(script, stack=()):
    st, branch = list(stack), []             # branch holds one flag per open IF: True while that arm is running
    for w in script.split():
        live = all(branch)
        if w in ('IF', 'NOTIF'): branch.append(live and (true(st.pop()) == (w == 'IF'))); continue
        if w == 'ELSE': branch[-1] = not branch[-1] and all(branch[:-1]); continue
        if w == 'ENDIF': branch.pop(); continue
        if not live: continue
        if w.startswith('0x'): st.append(bytes.fromhex(w[2:]))
        elif w.lstrip('-').isdigit(): st.append(enc(int(w)))
        elif w == 'DUP': st.append(st[-1])
        elif w == 'DROP': st.pop()
        elif w == 'SWAP': st[-2:] = st[-1], st[-2]
        elif w == 'ADD': b, a = dec(st.pop()), dec(st.pop()); st.append(enc(a + b))
        elif w == 'SUB': b, a = dec(st.pop()), dec(st.pop()); st.append(enc(a - b))
        elif w == 'NOT': st.append(enc(int(not true(st.pop()))))
        elif w == 'SIZE': st.append(enc(len(st[-1])))
        elif w == 'SHA256': st.append(hashlib.sha256(st.pop()).digest())
        elif w in ('EQUAL', 'EQUALVERIFY'):
            same = st.pop() == st.pop()
            if w == 'EQUAL': st.append(enc(int(same)))
            elif not same: return 'FAIL: EQUALVERIFY'
        elif w == 'VERIFY':
            if not true(st.pop()): return 'FAIL: VERIFY'
        elif w == 'RETURN': return 'FAIL: RETURN'
        else: raise ValueError('unknown word ' + w)
    return st
'''
SECP = '''import hashlib
P = 2**256 - 2**32 - 977
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
def add(a, b):                               # point addition on y^2 = x^3 + 7 (None is the point at infinity)
    if a is None or b is None: return a or b
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    m = (3 * a[0] * a[0] * pow(2 * a[1], -1, P) if a == b else (b[1] - a[1]) * pow(b[0] - a[0], -1, P)) % P
    x = (m * m - a[0] - b[0]) % P
    return x, (m * (a[0] - x) - a[1]) % P
def mul(k, p):
    r = None
    while k:
        if k & 1: r = add(r, p)
        p, k = add(p, p), k >> 1
    return r
def pubkey(sec):                             # a 33- or 65-byte public key as a point
    x = int.from_bytes(sec[1:33], 'big')
    if sec[0] == 4: return x, int.from_bytes(sec[33:65], 'big')
    y = pow(x**3 + 7, (P + 1) // 4, P)
    return x, y if y % 2 == sec[0] % 2 else P - y
def verify(sec, z, r, s):                    # ECDSA: R = (z/s)G + (r/s)Q must have x = r (mod n)
    w = pow(s, -1, N)
    R = add(mul(z * w % N, G), mul(r * w % N, pubkey(sec)))
    return R is not None and R[0] % N == r
'''
B58 = '''import hashlib
A = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58check(version, payload):              # Base58Check: version byte + payload + 4 checksum bytes, written in base 58
    d = bytes([version]) + payload
    d += hashlib.sha256(hashlib.sha256(d).digest()).digest()[:4]
    n, s = int.from_bytes(d, 'big'), ''
    while n: n, r = divmod(n, 58); s = A[r] + s
    return '1' * (len(d) - len(d.lstrip(b'\\0'))) + s
'''
# the first payment between people (block 170): the transaction, and the output it spends (a pay-to-public-key script)
TX170 = ("0100000001c997a5e56e104102fa209c6a852dd90660a20b2d9c352423edce25857fcd3704000000004847304402204e45e16932b8af514961a1d3a1a25fdf3f4f7732e9d624c6c61548ab5fb8cd410220181522ec8eca07de4860a4acdd12909d831cc56cbbac4622082221a8768d1d0901ffffffff0200ca9a3b00000000434104ae1a62fe09c5f51b13905f07f06b99a2f7159b2225f374cd378d71302fa28414e7aab37397f554a7df5f142c21c1b7303b8a0626f1baded5c72a704f7e6cd84cac00286bee0000000043410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac00000000")
SPK170 = "410411db93e1dcdb8a016b49840f8c53bc1eb68a382e97b1482ecad7b148a6909a5cb2e0eaddfb84ccf9744464f82e160bfa9b8b64f9d4c03f999b8643f656b412a3ac"

# the input script of the first input of the pizza transaction (a pay-to-public-key-hash spend: a 73-byte signature and a 65-byte public key)
SS_PIZZA = "493046022100bc57dc26f46fecc1da03272cb2298d8a08b22d865541f5b3a3e862cc87da4b47022100ce1fc72771d164d608b15065832542a0e9040cfdf28862c5175c81fcb0e0b65501410434417dd8d89deaf0f6481c2c160d6de0921624ef7b956f38eef9ed4a64e36877be84b77cdee5a8d92b7d93694f89c3011bf1cbdf4fd7d8ca13b58a7bb4ab0804"

# ---- bech32 and bech32m (BIP173, BIP350) for the browser: the checksum constant is 1 for witness version 0 and 0x2bc830a3 for later versions ----
BECH = '''CH = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
def polymod(values):
    gen = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for v in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ v
        for i in range(5): chk ^= gen[i] if (top >> i) & 1 else 0
    return chk
def segwit_address(hrp, version, program):
    const = 1 if version == 0 else 0x2bc830a3        # bech32 for version 0, bech32m for versions 1 to 16
    data, acc, bits = [version], 0, 0
    for byte in program:                              # regroup 8-bit bytes into 5-bit characters
        acc = (acc << 8) | byte; bits += 8
        while bits >= 5: bits -= 5; data.append((acc >> bits) & 31)
    if bits: data.append((acc << (5 - bits)) & 31)
    values = [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp] + data
    mod = polymod(values + [0] * 6) ^ const
    checksum = [(mod >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + '1' + ''.join(CH[d] for d in data + checksum)
'''


# browser code to follow SECP: BIP340 Schnorr verification and the taproot output key (BIP341); used by text part I
SCHNORR = '''def tagged(tag, data):                       # BIP340's tagged hash: SHA-256(SHA-256(tag) + SHA-256(tag) + data)
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + data).digest()
def lift_x(x):                               # the curve point with this x and an even y (None when x is not on the curve)
    y = pow((pow(x, 3, P) + 7) % P, (P + 1) // 4, P)
    return None if pow(y, 2, P) != (x ** 3 + 7) % P else (x, y if y % 2 == 0 else P - y)
def schnorr_verify(pub32, msg, sig):         # BIP340: s*G - e*P must have an even y and the x of R
    Pt, r, s = lift_x(int.from_bytes(pub32, 'big')), int.from_bytes(sig[:32], 'big'), int.from_bytes(sig[32:], 'big')
    if Pt is None or r >= P or s >= N: return False
    e = int.from_bytes(tagged('BIP0340/challenge', sig[:32] + pub32 + msg), 'big') % N
    R = add(mul(s, G), mul(N - e, Pt))
    return R is not None and R[1] % 2 == 0 and R[0] == r
def output_key(internal32, root=b''):        # BIP341: Q = P + tagged_hash('TapTweak', P + root) * G; returns (parity of Q's y, x of Q)
    t = int.from_bytes(tagged('TapTweak', internal32 + root), 'big')
    Q = add(lift_x(int.from_bytes(internal32, 'big')), mul(t, G))
    return Q[1] & 1, Q[0].to_bytes(32, 'big')
'''

# the network alert of July 2015, read for the story of the strict-DER fork (sen0401_ch07_stories_v1_0_0.py); added after the text parts were written
SOURCES.append(("BA", "Bitcoin.org, 2015", "Bitcoin.org network alert 'Some Miners Generating Invalid Blocks', 4 July 2015, last updated 15 July 2015 (Bitcoin.org, 2015)",
                "https://bitcoin.org/en/alert/2015-07-04-spv-mining", "secondary", "ev:bitcoinorg_alert_2015_07_04_spv_mining_v1_0_0.html"))
