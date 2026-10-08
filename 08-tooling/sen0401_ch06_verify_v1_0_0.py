#!/usr/bin/env python3
"""Checks sen0401_ch06_tx_lib_v1_0_0.py against what can be checked without a Bitcoin Core node: the chapter's own transaction as the
book prints it and as an independent explorer records it (identifier, size, weight, fields), three more saved transactions (the
transaction Alice's spends, the first bitcoin transaction, the pizza transaction), the figures of BIP68, BIP125 and BIP141, and the
constants of Bitcoin Core's sources at the pinned commit (consensus.h, amount.h, transaction.h, script.h, policy.cpp, chain.h,
validation.cpp). Every comparison is printed; one failure exits 1.
Run: /root/.local/bin/python3.14 sen0401_ch06_verify_v1_0_0.py"""
__version__ = "1.0.0"
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sen0401_ch06_tx_lib_v1_0_0 as T
import sen0401_ch06_checklib_v1_0_0 as C

bad = 0; n = 0
def check(name, got, want):
    global bad, n
    n += 1; ok = got == want
    if not ok: bad += 1
    print("%s %-62s %s" % ("ok  " if ok else "FAIL", name, got if ok else "got %r want %r" % (got, want)))

TXS = {"alice": ("tx_alice_46620030_v1_0_0.hex", "mempool_tx_466200308696215b_v1_0_0.json"),
       "alice_prev": ("tx_alice_prev_4ac54180_v1_0_0.hex", "mempool_tx_4ac5418026798669_v1_0_0.json"),
       "first": ("tx_first_f4184fc5_v1_0_0.hex", "mempool_tx_f4184fc596403b9d_v1_0_0.json"),
       "pizza": ("tx_pizza_a1075db5_v1_0_0.hex", "mempool_tx_a1075db55d416d3c_v1_0_0.json")}
for name, (hx, js) in TXS.items():
    h = C.ev_hex(hx); j = C.ev_json(js); tx = T.parse_tx(h)
    check("%s: txid = explorer's" % name, T.txid(h), j["txid"])
    check("%s: size = explorer's" % name, tx["size"], j["size"])
    check("%s: weight = explorer's" % name, T.weight(h), j["weight"])
    check("%s: version, locktime = explorer's" % name, (tx["version"], tx["locktime"]), (j["version"], j["locktime"]))
    check("%s: input count, output count" % name, (len(tx["inputs"]), len(tx["outputs"])), (len(j["vin"]), len(j["vout"])))
    check("%s: outpoints = explorer's" % name, [(i["txid"], i["vout"]) for i in tx["inputs"]], [(v["txid"], v["vout"]) for v in j["vin"]])
    check("%s: amounts and scripts = explorer's" % name, [(o["value"], o["script"]) for o in tx["outputs"]], [(v["value"], v["scriptpubkey"]) for v in j["vout"]])
    check("%s: witness = explorer's" % name, tx["witness"], [v.get("witness", []) for v in j["vin"]] if tx["segwit"] else [])
    check("%s: re-serialization is byte-identical" % name, T.serialize(tx).hex(), h)
    check("%s: fee = explorer's" % name, sum(v["prevout"]["value"] for v in j["vin"]) - sum(o["value"] for o in tx["outputs"]), j["fee"])

# the book's figures for Alice's transaction
A = C.ev_hex(TXS["alice"][0])
check("book: Alice's transaction is 388 hex characters", len(A), 388)
check("book: bitcoin-cli reported weight 569", T.weight(A), 569)
check("book: the previous output was 100,000 satoshis", C.ev_json(TXS["alice"][1])["vin"][0]["prevout"]["value"], 100000)
check("book: the outpoint txid in internal order", T.parse_tx(A)["inputs"][0]["txid_internal"], "eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a")
check("book: fold | tac reversal", T.internal_to_display("eb3ae38f27191aa5f3850dc9cad00492b88b72404f9da135698679268041c54a"), "4ac541802679866935a19d4f40728bb89204d0cac90d85f3a51a19278fe33aeb")
W = dict((r[0], r[3]) for r in T.field_weights(A))
check("book's weight table: version 16", W["version"], 16)
check("book's weight table: marker & flag 2", W["marker"] + W["flag"], 2)
check("book's weight table: outpoint 144", W["input 0 txid"] + W["input 0 output index"], 144)
check("book's weight table: input script 4", W["input 0 script length"] + W["input 0 script"], 4)
check("book's weight table: amount 64", W["output 0 amount"] + W["output 1 amount"], 64)
check("book's weight table: output script 232", W["output 0 script length"] + W["output 0 script"] + W["output 1 script length"] + W["output 1 script"], 232)
check("book's weight table: witness count 1, items 66", (W["witness 0 count"], W["witness 0 item 0 length"] + W["witness 0 item 0"]), (1, 66))
check("book's weight table: lock time 16, total 569", (W["lock time"], sum(W.values())), (16, 569))
check("book: the 0x6b input script is 107 bytes", 0x6b, 107)
check("book: previous transaction in block 774,958", C.ev_json(TXS["alice_prev"][1])["status"]["block_height"], 774958)
check("explorer: Alice's own transaction in block 775,072 (book says 774,958)", C.ev_json(TXS["alice"][1])["status"]["block_height"], 775072)

# BIP68 / BIP125 / BIP141
check("BIP68: type flag is 1 << 22", T.SEQUENCE_LOCKTIME_TYPE_FLAG, 1 << 22)
check("BIP68: 512-second units", T.sequence_decode(T.sequence_for(seconds=1024))["relative_timelock"], ("seconds", 1024))
check("BIP68: a lock of 30 blocks, output at 774,958, earliest 774,988", T.earliest_block(774958, 30), 774988)
check("BIP125: 0xfffffffd signals, 0xfffffffe does not", (T.sequence_decode(0xfffffffd)["rbf_signal"], T.sequence_decode(0xfffffffe)["rbf_signal"]), (True, False))
check("BIP141: vbytes = ceil(weight / 4)", T.vbytes(A), 143)
check("BIP141: txid ignores the witness, wtxid does not", (T.txid(T.with_witness_item(A, "00" * 65)) == T.txid(A), T.wtxid(T.with_witness_item(A, "00" * 65)) == T.wtxid(A)), (True, False))
check("BIP141: legacy transaction's wtxid equals its txid", T.wtxid(C.ev_hex(TXS["first"][0])) == T.txid(C.ev_hex(TXS["first"][0])), True)

# Bitcoin Core's constants, read from the saved sources
src = lambda f: C.ev_raw(f)
num = lambda f, pat: int(re.search(pat, src(f)).group(1).replace("'", "").replace(",", ""))
check("Core consensus.h: MAX_BLOCK_WEIGHT", num("core_src_consensus_consensus.h", r"MAX_BLOCK_WEIGHT\{([0-9']+)\}"), 4000000)
check("Core consensus.h: COINBASE_MATURITY", num("core_src_consensus_consensus.h", r"COINBASE_MATURITY = (\d+);"), T.COINBASE_MATURITY)
check("Core consensus.h: WITNESS_SCALE_FACTOR", num("core_src_consensus_consensus.h", r"WITNESS_SCALE_FACTOR = (\d+);"), T.WITNESS_SCALE_FACTOR)
check("Core amount.h: COIN", num("core_src_consensus_amount.h", r"COIN\{([0-9']+)\}"), T.COIN)
check("Core amount.h: MAX_MONEY = 21,000,000 * COIN", num("core_src_consensus_amount.h", r"MAX_MONEY\{([0-9']+) \* COIN\}") * T.COIN, T.MAX_MONEY)
check("Core transaction.h: SEQUENCE_LOCKTIME_MASK", int(re.search(r"SEQUENCE_LOCKTIME_MASK\{(0x[0-9a-f]+)\}", src("core_src_primitives_transaction.h")).group(1), 16), T.SEQUENCE_LOCKTIME_MASK)
check("Core transaction.h: SEQUENCE_LOCKTIME_GRANULARITY", num("core_src_primitives_transaction.h", r"SEQUENCE_LOCKTIME_GRANULARITY\{(\d+)\}"), T.SEQUENCE_LOCKTIME_GRANULARITY)
check("Core script.h: LOCKTIME_THRESHOLD", num("core_src_script_script.h", r"LOCKTIME_THRESHOLD\{([0-9']+)\}"), T.LOCKTIME_THRESHOLD)
check("Core policy.h: DUST_RELAY_TX_FEE", num("core_src_policy_policy.h", r"DUST_RELAY_TX_FEE\{(\d+)\}"), T.DUST_RELAY_TX_FEE)
check("Core policy.cpp: 546 and 294 from the comment", (T.dust_threshold("76a914" + "00" * 20 + "88ac"), T.dust_threshold("0014" + "00" * 20)), (546, 294))
check("Core chain.h: nMedianTimeSpan 11", num("core_src_chain.h", r"nMedianTimeSpan = (\d+);"), 11)
check("Core chainparams.cpp: halving interval", num("core_src_kernel_chainparams.cpp", r"nSubsidyHalvingInterval = (\d+);"), T.SUBSIDY_HALVING_INTERVAL)
check("Core validation.cpp: subsidy at the 4th halving is 3.125 BTC", T.block_subsidy(840000), 312500000)
check("Core validation.cpp: last non-zero subsidy at 6,929,999 (book says up until 6,720,000)", (T.last_subsidy_height(), T.block_subsidy(6720000)), (6929999, 1))
check("schedule: total issued just under 21 million", T.total_subsidy(), 2099999997690000)

print("\n%d checks, %d failed" % (n, bad))
sys.exit(1 if bad else 0)
