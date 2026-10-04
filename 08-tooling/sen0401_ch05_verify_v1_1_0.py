"""Checks sen0401_ch05_wallet_lib_v1_1_0.py against published vectors: BIP32 test vector 1 and 2, the Trezor BIP39 vectors (passphrase TREZOR),
the BIP380 checksum vector, the BIP84 and BIP49 vectors, and the book's own numbers. Run: /root/.local/bin/python3.14 sen0401_ch05_verify_v1_0_0.py"""
import json, re, os, hashlib, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch05_wallet_lib_v1_1_0 as W
EV = os.path.join(W.HERE, "ch05-evidence"); bad = []; n = 0
def ok(name, cond):
    global n; n += 1
    if not cond: bad.append(name)
# BIP32 vector 1 from the BIP text
t = open(os.path.join(EV, "bip-0032.mediawiki")).read()
seed = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
for path, want in [("m", None), ("m/0'", None), ("m/0'/1", None), ("m/0'/1/2'", None), ("m/0'/1/2'/2", None), ("m/0'/1/2'/2/1000000000", None)]:
    xprv, xpub = W.derive_serialized(seed, path)
    ok("bip32 v1 " + path + " xprv", xprv in t); ok("bip32 v1 " + path + " xpub", xpub in t)
seed2 = bytes.fromhex("fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542")
for path in ["m", "m/0", "m/0/2147483647'", "m/0/2147483647'/1", "m/0/2147483647'/1/2147483646'", "m/0/2147483647'/1/2147483646'/2"]:
    xprv, xpub = W.derive_serialized(seed2, path); ok("bip32 v2 " + path, xprv in t and xpub in t)
# BIP39 trezor vectors
for ent, mn, sd, xprv in json.load(open(os.path.join(EV, "trezor_vectors.json")))["english"]:
    e = bytes.fromhex(ent)
    ok("bip39 mnemonic " + ent[:8], W.entropy_to_mnemonic(e) == mn)
    ok("bip39 seed " + ent[:8], W.mnemonic_to_seed(mn, "TREZOR").hex() == sd)
    k, c = W.master(bytes.fromhex(sd)); ok("bip39 xprv " + ent[:8], W.serialize_xprv(k, c) == xprv)
    ok("bip39 roundtrip " + ent[:8], W.mnemonic_to_entropy(mn) == (e, True))
# BIP380
ok("bip380 valid", W.descsum_check("raw(deadbeef)#89f8spxm")); ok("bip380 create", W.descsum_create("raw(deadbeef)") == "raw(deadbeef)#89f8spxm")
ok("bip380 bad", not W.descsum_check("raw(deedbeef)#89f8spxm"))
# BIP84 vector
mn = "abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon abandon about"
sd = W.mnemonic_to_seed(mn); k, c = W.master(sd)
ak, ac = W.derive_priv(k, c, "m/84'/0'/0'")
b84 = open(os.path.join(EV, "bip-0084.mediawiki")).read()
ok("bip84 account xpub", W.serialize_xpub(W.ec_mul(ak), ac) != "")  # xpub prefix differs (zpub in the BIP)
K1, c1 = W.ckd_pub(W.ec_mul(ak), ac, 0); K0, _ = W.ckd_pub(K1, c1, 0)
ok("bip84 first address", W.p2wpkh_address(W.ser_p(K0)) == "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu" and "bc1qcr8te4kr609gcawutmrza0j4xv80jy8z306fyu" in b84)
ok("bip84 first pubkey", W.ser_p(K0).hex() == "0330d54fd0dd420a6e5f8d3624f5f3482cae350f79d5f0753bf5beef9c2d91af3c")
# BIP49 vector (testnet)
ak, ac = W.derive_priv(k, c, "m/49'/1'/0'"); kk, cc = W.derive_priv(ak, ac, "m/0/0")
pub = W.ser_p(W.ec_mul(kk)); ok("bip49 pubkey", pub.hex() == "03a1af804ac108a8a51782198c2d034b28bf90c8803f5a53f76276fa69a4eae77f")
script = b"\x00\x14" + W.hash160(pub); ok("bip49 address", W.b58check(b"\xc4" + W.hash160(script)) == "2Mww8dCYPUpKHofjgcXcBCEGmniw9CoaiD2")
# book numbers
ok("book K+123G", W.ec_add(W.ec_mul(5), W.ec_mul(123)) == W.ec_mul(128))
seedhex = "f1cc3bc03ef51cb43ee7844460fa5049e779e7425a6349c8e89dfbb0fd97bb73"
ok("book seed+i", [hashlib.sha256(("%s + %d\n" % (seedhex, i)).encode()).hexdigest() for i in range(3)] == ["50b18e0bd9508310b8f699bad425efdf67d668cb2462b909fdb6b9bd2437beb3", "a965dbcd901a9e3d66af11759e64a58d0ed5c6863e901dfda43adcd5f8c744f3", "19580c97eb9048599f069472744e51ab2213f687d4720b0efc5bb344d624c3aa"])
ent = bytes.fromhex("0c1e24e5917779d297e14d45f14e1a1a"); m = W.entropy_to_mnemonic(ent)
ok("book 12 words", m == "army van defense carry jealous true garbage claim echo media make crunch")
ok("book seed 1", W.mnemonic_to_seed(m).hex() == "5b56c417303faa3fcba7e57400e120a0ca83ec5a4fc9ffba757fbe63fbd77a89a1a3be4c67196f57c39a88b76373733891bfaba16ed27a813ceed498804c0570")
ok("book seed 2", W.mnemonic_to_seed(m, "SuperDuperSecret").hex() == "3b5df16df2157104cfdd22830162a5e170c0161653e3afe6c88defeefb0818c793dbb28ab3ab091897d0715861dc8a18358f80b79d49acf64142ae57037d1d54")
e2 = bytes.fromhex("2041546864449caff939d32d574753fe684d3c947c3346713dd8423e74abcf8c"); m2 = W.entropy_to_mnemonic(e2)
ok("book 24 words", m2 == "cake apple borrow silk endorse fitness top denial coil riot stay wolf luggage oxygen faint major edit measure invite love trap field dilemma oblige")
ok("book seed 3", W.mnemonic_to_seed(m2).hex() == "3269bce2674acbd188d4f120072b13b088a0ecf87c6e4cae41657a0bb78f5315b33b3a04356e53d062e55f1e0deaa082df8d487381379df848a6ad7e98798404")
x = "xprv9tyUQV64JT5qs3RSTJkXCWKMyUgoQp7F3hA1xzG6ZGu6u6Q9VMNjGr67Lctvy5P8oyaYAL9CAWrUE9i6GoNMKUga5biW6Hx4tws2six3b9c"
p = W.parse_extended(x); kk = int.from_bytes(p["key"][1:], "big")
ok("book xprv/xpub pair", W.serialize_xpub(W.ec_mul(kk), p["chain"], p["depth"], p["fp"], p["index"]) == "xpub67xpozcx8pe95XVuZLHXZeG6XWXHpGq6Qv5cmNfi7cS5mtjJ2tgypeQbBs2UAR6KECeeMVKZBPLrtJunSDMstweyLXhRgPxdp14sk9tJPW9")
# version 1.1.0 additions
k, c = W.master(W.mnemonic_to_seed(mn)); kk, cc = W.derive_priv(k, c, "m/86'/0'/0'/0/0")
ok("bip86 root xprv", W.serialize_xprv(*W.master(W.mnemonic_to_seed(mn))) == "xprv9s21ZrQH143K3GJpoapnV8SFfukcVBSfeCficPSGfubmSFDxo1kuHnLisriDvSnRRuL2Qrg5ggqHKNVpxR86QEC8w35uxmGoggxtQTPvfUu")
ok("bip86 internal key", W.ser_p(W.ec_mul(kk))[1:].hex() == "cc8a4bc64d897bddc5fbc2f670f7a8ba0b386779106cf1223c6fc5d7cd6fc115")
ok("bip86 output key", W.taproot_output_key(W.ser_p(W.ec_mul(kk))).hex() == "a60869f0dbcf1dc659c9cecbaf8050135ea9e8cdc487053f1dc6880949dc684c")
ok("bip86 address", W.p2tr_address(W.taproot_output_key(W.ser_p(W.ec_mul(kk)))) == "bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr")
kk, cc = W.derive_priv(k, c, "m/86'/0'/0'/1/0"); ok("bip86 change", W.p2tr_address(W.taproot_output_key(W.ser_p(W.ec_mul(kk)))) == "bc1p3qkhfews2uk44qtvauqyr2ttdsw7svhkl9nkm9s9c3x4ax5h60wqwruhk7")
d_, z_ = 0x1E99423A4ED27608A15A2616A2B0E9E52CED330AC530EDCC32C8FFC6A526AEDD, 12345
sig = W.ecdsa_sign(d_, z_, 987654321); ok("ecdsa ok", W.ecdsa_verify(W.ec_mul(d_), z_, sig)); ok("ecdsa other msg", not W.ecdsa_verify(W.ec_mul(d_), z_ + 1, sig))
b = open(os.path.join(EV, "bip-0093.mediawiki")).read()
cx = "ms10testsxxxxxxxxxxxxxxxxxxxxxxxxxx4nzvca9cmczlw"
ok("codex32 vector 1 in BIP", cx in b); ok("codex32 checksum", W.codex32_check(cx)); ok("codex32 seed", W.codex32_payload(cx).hex() == "318c6318c6318c6318c6318c6318c631")
ok("codex32 xprv", W.serialize_xprv(*W.master(bytes.fromhex("318c6318c6318c6318c6318c6318c631"))) == "xprv9s21ZrQH143K3taPNekMd9oV5K6szJ8ND7vVh6fxicRUMDcChr3bFFzuxY8qP3xFFBL6DWc2uEYCfBFZ2nFWbAqKPhtCLRjgv78EZJDEfpL")
ok("codex32 typo", not W.codex32_check(cx[:-1] + "v"))
ok("origin parse", W.parse_origin("pkh([d34db33f/44'/0'/0']xpub/1/*)") == ("d34db33f", [2147483692, 2147483648, 2147483648]))
print(n, "verifications; failures:", bad)
