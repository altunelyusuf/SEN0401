"""Every computation the SEN0401 chapter 6 lecture deck shows. The outputs come from executing these statements,
never from typing them: examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE is the chapter's own library (sen0401_ch06_tx_lib_v1_0_0.py, the module the chapter corpus also uses, checked
against the chapter's transaction, three more saved transactions and Bitcoin Core's sources by
sen0401_ch06_verify_v1_0_0.py), the values the chapter prints and the slides name, and the saved evidence in
08-tooling/ch06-evidence. Every group is named after the concept of the chapter 6 taxonomy whose slide shows it, so
that a slide and its computation cannot drift apart. deck_check_v1_0_0.py re-runs every '>>>' line of the finished
deck in this same namespace. No Bitcoin Core node is available here: the one figure the book took from a running
node, the weight 569, is recomputed from the bytes and compared with the saved explorer record, as the slide says.
"""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))
EVID = os.path.join(TOOLING, "ch06-evidence")

PRELUDE = """
import sys, json, hashlib
sys.path.insert(0, %r)
from sen0401_ch06_tx_lib_v1_0_0 import *
EVID = %r
_rd = lambda n: open(EVID + '/' + n, encoding='utf-8', errors='replace').read()
_js = lambda n: json.load(open(EVID + '/' + n, encoding='utf-8'))

# the chapter's own transaction, Alice's payment to Bob, as the book prints it and as the explorer saved it
ALICE = _rd('tx_alice_46620030_v1_0_0.hex').strip()
ALICE_REC = _js('mempool_tx_466200308696215b_v1_0_0.json')
PREV = _rd('tx_alice_prev_4ac54180_v1_0_0.hex').strip()
PREV_REC = _js('mempool_tx_4ac5418026798669_v1_0_0.json')
# the two legacy transactions of the chapter's stories: block 170 and the pizza
FIRST = _rd('tx_first_f4184fc5_v1_0_0.hex').strip()
FIRST_REC = _js('mempool_tx_f4184fc596403b9d_v1_0_0.json')
PIZZA = _rd('tx_pizza_a1075db5_v1_0_0.hex').strip()
PIZZA_REC = _js('mempool_tx_a1075db55d416d3c_v1_0_0.json')
tx = parse_tx(ALICE)
legacy = serialize(tx, witness=False)
h = lambda s: s[:16] + '...'
""" % (TOOLING, EVID)

# One group per concept of the chapter 6 taxonomy; the key is the concept identifier the corpus uses.
EX = {
    # ---- What a transaction is ----
    "SerializedTransaction": [
        "len(ALICE) // 2, tx['size']",
        "tx['version'], tx['marker'], tx['flag'], tx['segwit']",
        "len(tx['inputs']), len(tx['outputs']), len(tx['witness'][0]), tx['locktime']",
    ],
    "ByteMap": [
        "[s for s in tx['spans'] if s[0] in ('version', 'marker', 'flag', 'lock time')]",
        "sum(k for n, p, k in tx['spans'])",
    ],
    "LegacyFormat": [
        "len(legacy), len(bytes.fromhex(ALICE))",
        "parse_tx(FIRST)['segwit'], FIRST_REC['status']['block_height']",
    ],
    # ---- Inputs ----
    "Outpoint": [
        "i0 = tx['inputs'][0]",
        "i0['txid_internal'][:16], i0['vout']",
        "internal_to_display(i0['txid_internal'])[:16]",
        "PREV_REC['vout'][1]['value'], PREV_REC['status']['block_height']",
    ],
    "DisplayByteOrder": [
        "d = 'eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a'",
        "''.join(reversed([d[i:i + 2] for i in range(0, 64, 2)]))[:16]",
        "txid(PREV)[:16]",
    ],
    "InputCount": [
        "p = parse_tx(PIZZA)",
        "len(p['inputs']), bytes.fromhex(PIZZA)[4], len(p['outputs'])",
        "p['outputs'][0]['value'] // COIN, PIZZA_REC['fee'] / COIN",
        "txid(PIZZA)[:16], PIZZA_REC['status']['block_height']",
    ],
    "CompactSize": [
        "[cs_encode(n).hex() for n in (1, 252, 253, 65535, 65536)]",
        "[len(cs_encode(n)) for n in (252, 253, 65536, 2 ** 32)]",
    ],
    # ---- The sequence field ----
    "SequenceNumber": [
        "hex(tx['inputs'][0]['sequence']), tx['inputs'][0]['sequence'] == SEQUENCE_FINAL",
    ],
    "Bip125Signal": [
        "[(hex(s), sequence_decode(s)['rbf_signal']) for s in (0xffffffff, 0xfffffffe, 0xfffffffd)]",
    ],
    "Bip68Timelock": [
        "sequence_decode(30)['relative_timelock'], earliest_block(774958, 30)",
        "s = sequence_for(seconds=3600)",
        "hex(s), sequence_decode(s)['relative_timelock']",
        "hex(SEQUENCE_LOCKTIME_TYPE_FLAG), hex(SEQUENCE_LOCKTIME_DISABLE_FLAG), hex(SEQUENCE_LOCKTIME_MASK)",
    ],
    "LockTimeField": [
        "tx['locktime'], parse_tx(PREV)['locktime'], PREV_REC['status']['block_height']",
        "locktime_decode(123456), locktime_decode(ALICE_REC['status']['block_time'])",
    ],
    "MedianTimePast": [
        "times = [1675556500 + 100 * k for k in (15, 21, 5, 27, 24, 0, 26, 18, 12, 23, 25)]",
        "median_time_past(times), max(times) - median_time_past(times)",
    ],
    # ---- Outputs ----
    "AmountField": [
        "[(o['value'], o['value'] / COIN) for o in tx['outputs']]",
        "PREV_REC['vout'][1]['value'] - sum(o['value'] for o in tx['outputs']), ALICE_REC['fee']",
        "MAX_MONEY, money_range(MAX_MONEY + 1)",
    ],
    "AmountRange": [
        "big = 92_233_720_368_54277039",
        "w = (2 * big) & 0xffffffffffffffff",
        "big > MAX_MONEY, w - 2 ** 64 if w >= 2 ** 63 else w",
        "money_range(w - 2 ** 64), money_range(big), 50 * COIN - (w - 2 ** 64) > 50 * COIN",
    ],
    "DustLimit": [
        "P2PKH = '76a914' + '00' * 20 + '88ac'",
        "P2WPKH, P2TR = '0014' + '00' * 20, '5120' + '00' * 32",
        "RET = '6a04deadbeef'",
        "[dust_threshold(s) for s in (P2PKH, P2WPKH, P2TR, RET)]",
        "DUST_RELAY_TX_FEE, (34 + 148) * 3, (31 + 67) * 3",
    ],
    "OutputScript": [
        "[(o['value'], len(bytes.fromhex(o['script'])), segwit_output_version(o['script'])[0]) for o in tx['outputs']]",
    ],
    # ---- Witnesses ----
    "PushEncoding": [
        "push_encodings(2)",
        "sorted({txid(with_input_script(FIRST, s))[:8] for s in push_encodings(2).values()})",
    ],
    "Segwit": [
        "txid(ALICE)[:16], hash256(legacy)[::-1].hex()[:16]",
        "mutated = with_witness_item(ALICE, '00' * 65)",
        "txid(mutated) == txid(ALICE), wtxid(mutated) == wtxid(ALICE)",
    ],
    "WitnessProgram": [
        "segwit_output_version(tx['outputs'][0]['script'])[0], segwit_output_version(tx['outputs'][1]['script'])[0]",
        "tx['inputs'][0]['script'] == '', len(bytes.fromhex(tx['witness'][0][0]))",
    ],
    # ---- Lock time and the coinbase ----
    "BlockSubsidy": [
        "[block_subsidy(h * 210000) / COIN for h in range(9)]",
        "[block_subsidy(h) for h in (6720000, 6929999, 6930000)]",
        "last_subsidy_height(), total_subsidy() / COIN",
    ],
    "MaturityRule": [
        "r = FIRST_REC",
        "r['vin'][0]['txid'][:16], r['status']['block_height']",
        "coinbase_mature(9, 170), 170 - 9, COINBASE_MATURITY",
    ],
    # ---- Weight ----
    "Weight": [
        "len(legacy) * 3 + len(bytes.fromhex(ALICE)), weight(ALICE)",
        "ALICE_REC['weight'], vbytes(ALICE)",
        "weight(FIRST) == 4 * parse_tx(FIRST)['size']",
    ],
    "WeightUnits": [
        "W = {n: w for n, b, f, w in field_weights(ALICE)}",
        "[W['version'], W['marker'] + W['flag'], W['input count'], W['input 0 txid'] + W['input 0 output index'], W['input 0 script length'] + W['input 0 script'], W['input 0 sequence'], W['output count'], W['output 0 amount'] + W['output 1 amount'], W['output 0 script length'] + W['output 0 script'] + W['output 1 script length'] + W['output 1 script'], W['witness 0 count'], W['witness 0 item 0 length'] + W['witness 0 item 0'], W['lock time']]",
    ],
    "WeightFactor": [
        "[w for n, b, f, w in field_weights(ALICE) if f == 1]",
        "sum(w for n, b, f, w in field_weights(ALICE)), 80 * 3 + 80",
    ],
}
