"""Every computation the SEN0401 chapter 7 lecture deck shows. The outputs come from executing these statements, never from typing
them: examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE is the chapter's own script interpreter (sen0401_ch07_script_lib_v1_0_0.py, checked against Bitcoin Core's script_tests,
sighash tests, the BIP341 vectors and the 1,022 inputs of block 775,072 by sen0401_ch07_verify_v1_0_0.py) and the chapter's
helpers that build real, signed spends (sen0401_ch07_checklib_v1_0_0.py). Every group is named after the concept of the chapter 7
taxonomy whose slide shows it. deck_check_v1_0_0.py re-runs every '>>>' line of the finished deck in this same namespace.
No Bitcoin Core node is available here: the engine is a faithful Python port, and the slides say so.
"""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, json, hashlib
sys.path.insert(0, %r)
import sen0401_ch07_script_lib_v1_0_0 as L
import sen0401_ch07_checklib_v1_0_0 as K

def p2pkh(signer=1, flags=None, loose=False, amount_after=None):
    pk = L.pubkey_create(K.secret(1)); spk = L.p2pkh_script(L.hash160(pk))
    tx, spent = L.credit_and_spend(b'', spk, amount=100000)
    sig = L.sign_ecdsa_input(tx, 0, spk, K.secret(signer))
    if loose:
        r, s = L.der_parse_lax(sig[:-1])[:2]
        rb = r.to_bytes(32, 'big'); sb = s.to_bytes(32, 'big')
        rb = (b'\\x00' + rb) if rb[0] < 0x80 else rb
        rb = b'\\x00' + rb
        sb = (b'\\x00' + sb) if sb[0] >= 0x80 else sb
        body = b'\\x02' + bytes([len(rb)]) + rb + b'\\x02' + bytes([len(sb)]) + sb
        sig = b'\\x30' + bytes([len(body)]) + body + sig[-1:]
    tx.vin[0] = (tx.vin[0][0], tx.vin[0][1], L.push_data(sig) + L.push_data(pk), tx.vin[0][3])
    if amount_after is not None:
        tx.vout[0] = (amount_after, b'')
    return L.verify_input(tx, 0, spent, L.MAINNET_FLAGS if flags is None else flags)

def old_joined(sig_asm, lock_asm):
    words = (sig_asm + ' ' + lock_asm).split()
    if 'OP_RETURN' in words:
        words = words[:words.index('OP_RETURN')]
    return L.run(' '.join(words), '', flags=())

LOCK = 'OP_SHA256 0x20' + hashlib.sha256(b'secret').hexdigest() + ' OP_EQUAL'
CLTV = L.push_int(800000) + b'\\xb1\\x75' + L.push_data(K.pub(1)) + b'\\xac'
CSV = L.push_int(4320) + b'\\xb2\\x75' + L.push_data(K.pub(1)) + b'\\xac'
RED = L.multisig_script(2, [K.pub(i) for i in range(3)])
MOH_LEAVES = [K.csa_script([0, 1, 2], 2),
              L.push_int(4320) + b'\\xb2\\x75' + L.push_data(K.xpub(3)) + b'\\xad' + L.push_data(K.xpub(0)) + b'\\xac' + L.push_data(K.xpub(1)) + b'\\xba' + L.push_data(K.xpub(2)) + b'\\xba' + L.push_int(1) + b'\\x9c',
              L.push_int(12960) + b'\\xb2\\x75' + L.push_data(K.xpub(3)) + b'\\xac']
MOH_ITEMS = [([b'', ('sig', 1), ('sig', 0)], 0xffffffff), ([('sig0',), ('sig', 1), ('sig0',), ('sig', 3)], 4320), ([('sig', 3)], 12960)]
def census_groups():
    names = {'witness_v0_keyhash': 'P2WPKH', 'pubkeyhash': 'P2PKH', 'p2sh-p2wpkh': 'P2SH-P2WPKH', 'p2sh-p2wsh': 'P2SH-P2WSH'}
    g = {}
    for k, v in K.census(L).items():
        n = names.get(k) or ('P2WSH' if k.startswith('p2wsh') else 'taproot' if k.startswith('p2tr') else 'P2SH multisig' if k.startswith('p2sh-multisig') else k)
        g[n] = g.get(n, 0) + v
    return sorted(g.items(), key=lambda kv: -kv[1])
def moh_tap(i):
    return K.tr_spend(MOH_LEAVES, i, MOH_ITEMS[i][0], sequence=MOH_ITEMS[i][1])
def moh_wsh(path):
    out = []
    K.moh_spend(path, sequence=[0xffffffff, 4320, 12960][path - 1], tx_out=out)
    return out[0].weight()
""" % (TOOLING,)

# One group per concept of the chapter 7 taxonomy; the key is the concept identifier the corpus uses.
EX = {
    "StackExecution": [
        "L.run('2 3', 'OP_ADD 5 OP_EQUAL')",
        "L.run('2 3', 'OP_ADD 6 OP_EQUAL')",
        "L.assemble('2 3 OP_ADD 5 OP_EQUAL').hex()",
    ],
    "OpReturnBug": [
        "old_joined('OP_1 OP_RETURN', LOCK)",
        "L.run('OP_1 OP_RETURN', LOCK, flags=())",
        "L.run('0x06' + b'secret'.hex(), LOCK, flags=())",
    ],
    "PayToPublicKeyHash": [
        "spk = L.p2pkh_script(L.hash160(K.pub(1)))",
        "len(spk), L.classify(spk)[0]",
        "p2pkh(), p2pkh(signer=2), p2pkh(amount_after=99999)",
    ],
    "SignatureEncoding": [
        "sig = L.ecdsa_sign(K.secret(1), L.sha256(b'pay Bob'))",
        "len(sig) + 1, sig[0], L.is_valid_der(sig + b'\\x01'), L.is_low_s(sig + b'\\x01')",
        "p2pkh(loose=True, flags=L.MAINNET_FLAGS - {'DERSIG'}), p2pkh(loose=True)",
    ],
    "ScriptedMultisignature": [
        "len(RED), L.classify(RED)[0]",
        "K.ms_spend(2, 3, [0, 2]), K.ms_spend(2, 3, [2, 0]), K.ms_spend(2, 3, [1])",
        "K.ms_spend(2, 3, [0, 1], dummy=b'\\x01'), K.ms_spend(2, 3, [0, 1], dummy=b'\\x01', flags=L.MAINNET_FLAGS - {'NULLDUMMY'})",
    ],
    "RedeemScript": [
        "spk = L.p2sh_script(L.hash160(RED))",
        "L.script_to_address(spk)[:6], len(spk)",
        "K.ms_spend(2, 3, [0, 1], wrap='p2sh'), K.p2sh_spend(RED, hashed=RED + b'\\x00')",
    ],
    "CheckLockTimeVerify": [
        "K.key_spend(CLTV, locktime=800000, sequence=0xfffffffe)",
        "K.key_spend(CLTV, locktime=799999, sequence=0xfffffffe), K.key_spend(CLTV, locktime=800000)",
        "K.is_final(800000, 800000, 0, [0xfffffffe]), K.is_final(800000, 800001, 0, [0xfffffffe])",
    ],
    "CheckSequenceVerify": [
        "K.key_spend(CSV, version=2, sequence=4320)",
        "K.key_spend(CSV, version=2, sequence=4319), K.key_spend(CSV, version=1, sequence=4320)",
        "K.key_spend(CSV, version=2, sequence=0x80000000 | 4320)",
    ],
    "MohammedScript": [
        "len(K.moh_script()), K.moh_spend(1)",
        "K.moh_spend(2, sequence=4320), K.moh_spend(2, sequence=4319)",
        "K.moh_spend(3, sequence=12960), K.moh_spend(3, sequence=4320)",
    ],
    "P2wpkh": [
        "K.wpkh_spend(), K.wpkh_spend(nested=True)",
        "K.wpkh_spend(signed_amount=99999)",
        "L.script_to_address(L.p2wpkh_script(L.hash160(K.pub(1))))",
    ],
    "BlockCensus": [
        "sum(K.census(L).values())",
        "census_groups()",
    ],
    "Mast": [
        "[len(p) for p in K.tap_tree(MOH_LEAVES)[1]]",
        "[(n, (n - 1).bit_length()) for n in (3, 8, 1024, 2**20)]",
    ],
    "Taproot": [
        "par, q = L.taproot_tweak_pubkey(K.xpub(1), b'')",
        "L.script_to_address(L.p2tr_script(q))[:6], len(q)",
        "r, wit, wt = K.tr_keypath(1)",
        "r, len(wit[0]), wt",
        "K.tr_keypath(1, MOH_LEAVES)[0], K.tr_keypath(1, MOH_LEAVES, tamper='untweaked')[0]",
    ],
    "ScriptPathSpending": [
        "[moh_tap(i)[0] for i in range(3)]",
        "[moh_tap(i)[2] for i in range(3)]",
        "[moh_wsh(p) for p in (1, 2, 3)]",
        "[len(moh_tap(i)[1][-1]) for i in range(3)]",
    ],
    "ChecksigAdd": [
        "len(K.csa_script([0, 1, 2], 2)), len(RED)",
        "K.tr_spend([K.csa_script([0, 1, 2], 2)], 0, [b'', ('sig', 1), ('sig', 0)])[0]",
        "K.tr_spend([K.csa_script([0, 1, 2], 2)], 0, [b'', b'', ('sig', 0)])[0]",
    ],
    "OpSuccess": [
        "sum(1 for o in range(256) if L.is_op_success(o))",
        "K.tr_spend([bytes([0x51, 152])], 0, [])[0]",
        "L.run('OP_1 OP_LSHIFT', 'OP_1', flags=())",
    ],
}
