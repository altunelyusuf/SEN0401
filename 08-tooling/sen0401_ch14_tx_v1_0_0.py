#!/usr/bin/env python3
"""SEN0401 chapter 14: a small transaction toolkit for the contracts of the chapter (funding outputs, commitments, HTLCs, revocation scripts) on a private chain.
Standard library only, on top of sen0401_ch14_crypto_v1_0_0: script assembly, the serialization of a segwit transaction, the BIP 143 signature hash, witness signing and bech32 addresses of witness programs.
The node (Bitcoin Core 31.1) is the judge of every transaction built here: testmempoolaccept and sendrawtransaction give the verdict."""
__version__ = "1.0.0"
import os, struct, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch14_crypto_v1_0_0 as C

OP = {"0": 0x00, "IF": 0x63, "NOTIF": 0x64, "ELSE": 0x67, "ENDIF": 0x68, "VERIFY": 0x69, "RETURN": 0x6a, "DROP": 0x75, "DUP": 0x76, "EQUAL": 0x87, "EQUALVERIFY": 0x88, "SHA256": 0xa8,
      "HASH160": 0xa9, "CHECKSIG": 0xac, "CHECKSIGVERIFY": 0xad, "CHECKMULTISIG": 0xae, "CLTV": 0xb1, "CSV": 0xb2}
SIGHASH_ALL, SIGHASH_NONE, SIGHASH_SINGLE, ANYONECANPAY = 1, 2, 3, 0x80


def varint(n):
    if n < 0xfd:
        return bytes([n])
    if n <= 0xffff:
        return b"\xfd" + struct.pack("<H", n)
    return b"\xfe" + struct.pack("<I", n)


def push(b):
    if len(b) < 0x4c:
        return bytes([len(b)]) + b
    return b"\x4c" + bytes([len(b)]) + b


def num(n):
    """minimal script number push"""
    if n == 0:
        return b"\x00"
    if 1 <= n <= 16:
        return bytes([0x50 + n])
    out = bytearray()
    a = n
    while a:
        out.append(a & 0xff)
        a >>= 8
    if out[-1] & 0x80:
        out.append(0)
    return push(bytes(out))


def script(*items):
    """items: opcode names, ints (script numbers), bytes (data pushes)"""
    out = b""
    for it in items:
        if isinstance(it, str):
            out += bytes([OP[it]])
        elif isinstance(it, int):
            out += num(it)
        else:
            out += push(it)
    return out


def p2wpkh(pubkey):
    return b"\x00\x14" + C.hash160(pubkey)


def p2wsh(witness_script):
    return b"\x00\x20" + C.sha256(witness_script)


def multisig2(pk1, pk2):
    a, b = sorted([pk1, pk2])           # BOLT 3: the lexicographically lesser key first
    return script(2, a, b, 2, "CHECKMULTISIG")


def segwit_addr(program, hrp="bcrt", ver=0):
    data = [ver] + C.convertbits(list(program), 8, 5)
    pm = C._polymod([ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp] + data + [0] * 6) ^ (1 if ver == 0 else 0x2bc830a3)
    chk = [(pm >> 5 * (5 - i)) & 31 for i in range(6)]
    return hrp + "1" + "".join(C.B32[d] for d in data + chk)


class Tx:
    def __init__(self, version=2, locktime=0):
        self.version, self.locktime = version, locktime
        self.vin = []        # [txid_hex, vout, sequence, witness list]
        self.vout = []       # [value_sat, spk bytes]

    def add_in(self, txid, vout, sequence=0xfffffffe):
        self.vin.append([txid, vout, sequence, []])
        return len(self.vin) - 1

    def add_out(self, value, spk):
        self.vout.append([value, spk])

    def ser(self, witness=True):
        w = witness and any(i[3] for i in self.vin)
        b = struct.pack("<i", self.version) + (b"\x00\x01" if w else b"") + varint(len(self.vin))
        for txid, vout, seq, _ in self.vin:
            b += bytes.fromhex(txid)[::-1] + struct.pack("<I", vout) + b"\x00" + struct.pack("<I", seq)
        b += varint(len(self.vout))
        for v, spk in self.vout:
            b += struct.pack("<q", v) + varint(len(spk)) + spk
        if w:
            for _, _, _, wit in self.vin:
                b += varint(len(wit)) + b"".join(varint(len(x)) + x for x in wit)
        return b + struct.pack("<I", self.locktime)

    def txid(self):
        return C.sha256d(self.ser(False))[::-1].hex()

    def hex(self):
        return self.ser().hex()

    def sighash(self, idx, script_code, value, htype=SIGHASH_ALL):
        """BIP 143 signature hash of input idx"""
        anyone = htype & ANYONECANPAY
        base = htype & 0x1f
        hp = b"\0" * 32 if anyone else C.sha256d(b"".join(bytes.fromhex(i[0])[::-1] + struct.pack("<I", i[1]) for i in self.vin))
        hs = b"\0" * 32 if (anyone or base in (SIGHASH_SINGLE, SIGHASH_NONE)) else C.sha256d(b"".join(struct.pack("<I", i[2]) for i in self.vin))
        if base not in (SIGHASH_SINGLE, SIGHASH_NONE):
            ho = C.sha256d(b"".join(struct.pack("<q", v) + varint(len(s)) + s for v, s in self.vout))
        elif base == SIGHASH_SINGLE and idx < len(self.vout):
            v, s = self.vout[idx]
            ho = C.sha256d(struct.pack("<q", v) + varint(len(s)) + s)
        else:
            ho = b"\0" * 32
        i = self.vin[idx]
        pre = (struct.pack("<i", self.version) + hp + hs + bytes.fromhex(i[0])[::-1] + struct.pack("<I", i[1]) + varint(len(script_code)) + script_code
               + struct.pack("<q", value) + struct.pack("<I", i[2]) + ho + struct.pack("<I", self.locktime) + struct.pack("<I", htype))
        return C.sha256d(pre)

    def sig(self, idx, secret, script_code, value, htype=SIGHASH_ALL):
        return C.sign(secret, self.sighash(idx, script_code, value, htype)) + bytes([htype])

    def sign_p2wpkh(self, idx, secret, value, htype=SIGHASH_ALL):
        pk = C.pub(secret)
        sc = b"\x76\xa9\x14" + C.hash160(pk) + b"\x88\xac"
        self.vin[idx][3] = [self.sig(idx, secret, sc, value, htype), pk]

    def vsize(self):
        base, full = len(self.ser(False)), len(self.ser(True))
        return -(-(3 * base + full) // 4)
