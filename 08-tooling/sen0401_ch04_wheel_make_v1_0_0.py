#!/usr/bin/env python3
"""sen0401_ch04_wheel_make v1.0.0: writes the library sen0401_ch04_lib_v1_1_0.py (the code of v1_0_0 unchanged; the docstring gains the pointers to Bitcoin Core,
each read in the source tree of Bitcoin Core at the commit 079437c) and its wheel 03-materials/ch04/assets/sen0401_ch04_lib-1.1.0-py3-none-any.whl.
Neither file is written if it exists. Usage: python3 sen0401_ch04_wheel_make_v1_0_0.py"""
import os, zipfile, re
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(H)
old = open(os.path.join(H, "sen0401_ch04_lib_v1_0_0.py"), encoding="utf-8").read()
m = re.match(r'"""(.*?)"""\n__version__ = "1.0.0"\n', old, re.S); assert m
doc = m.group(1).replace("sen0401_ch04_lib v1.0.0", "sen0401_ch04_lib v1.1.0", 1)
doc += """

Relation to Bitcoin Core (v1.1.0; each pointer was read in the source tree of Bitcoin Core, commit 079437c; behaviour of this file is unchanged from v1.0.0):
* b58check(), b58check_decode(): EncodeBase58Check and DecodeBase58Check in src/base58.cpp (the alphabet is pszBase58 in the same file; the checksum is the first four bytes of a double SHA256).
* polymod(), bech_encode(), bech_check(), segwit_address(), segwit_decode(): bech32::Encode and bech32::Decode in src/bech32.cpp; EncodingConstant there returns 1 for Bech32 and 0x2bc830a3 for Bech32m, the two
  constants of BECH32 and BECH32M here; the address layer is DestinationEncoder and DecodeDestination in src/key_io.cpp.
* key_to_address(), p2pkh_script(), p2pk_script(), multisig_script(): the version byte of a P2PKH or P2SH address is chain parameter Base58Prefix(PUBKEY_ADDRESS) or Base58Prefix(SCRIPT_ADDRESS) (src/key_io.cpp);
  the locking script of a destination is built by GetScriptForDestination (src/addresstype.cpp); OP_CHECKMULTISIG is evaluated in EvalScript (src/script/interpreter.cpp).
* wif(): EncodeSecret in src/key_io.cpp writes the SECRET_KEY prefix, the 32 key bytes and, for a compressed key, a final byte 1, in Base58Check.
* hash160 of a public key: Hash160 and CHash160 in src/hash.h. pub_bytes(): CPubKey::COMPRESSED_SIZE is 33 and CPubKey::SIZE is 65 in src/pubkey.h.
* a private key is valid when 0 < k < n: CKey::Check calls secp256k1_ec_seckey_verify (src/key.cpp); CKey::MakeNewKey draws the bytes with GetStrongRandBytes until that check holds.
* ec_add(), ec_mul(): Core does not carry this arithmetic; it calls the library libsecp256k1 (secp256k1_ec_pubkey_create and others), which this readable sketch does not replace."""
new = '"""' + doc + '"""\n__version__ = "1.1.0"\n' + old[m.end():]
f = os.path.join(H, "sen0401_ch04_lib_v1_1_0.py")
assert not os.path.exists(f); open(f, "w", encoding="utf-8").write(new)
w = os.path.join(R, "03-materials", "ch04", "assets", "sen0401_ch04_lib-1.1.0-py3-none-any.whl"); assert not os.path.exists(w)
with zipfile.ZipFile(w, "w", zipfile.ZIP_DEFLATED) as z:
    def put(n, b):
        zi = zipfile.ZipInfo(n, (2026, 11, 25, 0, 0, 0)); zi.compress_type = zipfile.ZIP_DEFLATED; z.writestr(zi, b)
    put("sen0401_ch04_lib_v1_1_0.py", new.encode("utf-8"))
    put("sen0401_ch04_lib-1.1.0.dist-info/METADATA", b"Metadata-Version: 2.1\nName: sen0401-ch04-lib\nVersion: 1.1.0\nSummary: The chapter 4 (Keys and Addresses) library of the SEN0401 course.\n")
    put("sen0401_ch04_lib-1.1.0.dist-info/WHEEL", b"Wheel-Version: 1.0\nGenerator: sen0401_ch04_wheel_make_v1_0_0\nRoot-Is-Purelib: true\nTag: py3-none-any\n")
print("wrote", f, w)
