__version__ = "1.0.0"
# Every computation the SEN0401 chapter 4 deck shows. The outputs come from executing them, never from typing.
# PRELUDE is the chapter toolkit (08-tooling/ch04-evidence/sen0401_keys_toolkit_v1_0_0.py) and the values the slides name
# but do not print in full: the three witness programs and the length-extension strings the book prints.
import os
HERE = os.path.dirname(os.path.abspath(__file__)); EVID = os.path.join(HERE, "..", "ch04-evidence")
TOOLKIT = open(os.path.join(EVID, "sen0401_keys_toolkit_v1_0_0.py")).read()
EC_SRC = TOOLKIT.split("# --- ec ---\n")[1].split("# --- end ec ---")[0].rstrip("\n")   # the function text the slide shows must equal this
PRELUDE = (TOOLKIT + "\nPROG_WPKH = '2b626ed108ad00a944bb2922a309844611d25468'\n"
           "PROG_WSH = '648a32e50b6fb7c5233b228f60a6a2ca4158400268844c4bc295ed5e8c3d626f'\n"
           "PROG_TR = '2ceefa5fa770ff24f87c5475d76eab519eda6176b11dbe1618fcf755bfac5311'\n"
           "EXT = ['bc1pqqqsq9txsqp', 'bc1pqqqsq9txsqqqqp', 'bc1pqqqsq9txsqqqqqqp', 'bc1pqqqsq9txsqqqqqqqqp', 'bc1pqqqsq9txsqqqqqqqqqp', 'bc1pqqqsq9txsqqqqqqqqqqqp']\n")
K_HEX = "0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD"
EX = {
 "range": ["n = N", "n < 2**256", "P == 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1", "import secrets", "k = secrets.randbelow(n - 1) + 1", "0 < k < n"],
 "curve": ["x = 55066263022277343669578718895168534326250603453777594175500187360389116729240", "y = 32670510020758816978083085130507043184471273380659243275938904335757337482424", "(x ** 3 + 7 - y ** 2) % P"],
 "pubkey": ["k = " + K_HEX, "K = ec_mul(k)", "hex(K[0])", "hex(K[1])", "ec_mul(N) is None"],
 "compress": ["K = ec_mul(" + K_HEX + ")", "pub = pub_bytes(K)", "pub.hex()", "len(pub), len(pub_bytes(K, False))", "decompress(pub) == K"],
 "commit": ["hashlib.sha256(b'2007.  He said about a year and a half before Oct 2008\\n').hexdigest()", "K = ec_mul(" + K_HEX + ")", "hash160(pub_bytes(K)).hex()", "hash160(pub_bytes(K)) == hash160(pub_bytes(K, False))"],
 "addr": ["K = ec_mul(" + K_HEX + ")", "p2pkh(pub_bytes(K))", "p2pkh(pub_bytes(K, False))"],
 "wif": ["k = " + K_HEX, "wif(k, False)", "wif(k)", "b58check_decode(wif(k)).hex()"],
 "prefix": ["[b58check(bytes([v]) + bytes(20))[0] for v in (0x00, 0x05, 0xc4)]", "b58check(b'\\x80' + bytes(32) + b'\\x01')[0], b58check(b'\\x80' + b'\\xff' * 32 + b'\\x01')[0]", "b58check(bytes.fromhex('0488B21E') + bytes(74))[:4]"],
 "collide": ["hr = 9.5e20", "round(hr * 3600 / 2**80, 1)", "round(2**128 / hr / 31_557_600 / 1e9)", "round(2**128 / (2**80 / 3600) / 31_557_600 / 1e9)"],
 "bech": ["segwit_address('bc', 0, bytes.fromhex(PROG_WPKH))", "segwit_address('bc', 0, bytes.fromhex(PROG_WSH))", "segwit_address('bc', 1, bytes.fromhex(PROG_TR))", "segwit_address('bc', 16, bytes.fromhex('0000'))"],
 "ext": ["BECH32, hex(BECH32M)", "[bech_check(a) == BECH32 for a in EXT]", "[bech_check(a) == BECH32M for a in EXT]"],
 "vanity": ["[58**n for n in (2, 3, 4)]", "round(58**8 / 2 / 100_000 / 31_557_600, 1)", "58**11"],
}
