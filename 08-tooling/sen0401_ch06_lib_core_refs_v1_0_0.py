#!/usr/bin/env python3
"""Writes sen0401_ch06_tx_lib_v1_1_0.py from the committed v1_0_0 (never edited): the module docstring gains a 'BITCOIN CORE, rule by rule' table and each function a comment naming the Bitcoin Core function it restates.
Behaviour is unchanged (every other line is byte-identical). Every Core name was read in the local clone of bitcoin/bitcoin at commit 079437c (master, 2026-11-19) when this file was written. Usage: python3 sen0401_ch06_lib_core_refs_v1_0_0.py"""
__version__ = "1.0.0"
import os, re
H = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(H, "sen0401_ch06_tx_lib_v1_0_0.py"), encoding="utf-8").read()
TABLE = '''
BITCOIN CORE, rule by rule. Every function below restates a rule of Bitcoin Core, and the comment above it names the Core function. Each name was read in the clone of bitcoin/bitcoin at commit 079437c (master, 2026-11-19):
  src/serialize.h               ReadCompactSize, WriteCompactSize                          the compactSize integer      -> cs_decode, cs_encode
  src/primitives/transaction.h  UnserializeTransaction, SerializeTransaction               the extended and legacy format -> parse_tx, serialize
  src/primitives/transaction.h  CTransaction::ComputeHash, ComputeWitnessHash             the txid and the wtxid       -> txid, wtxid
  src/consensus/validation.h    GetTransactionWeight                                       weight = legacy * 3 + full   -> weight
  src/policy/policy.cpp         GetVirtualTransactionSize (weight + 3) / 4                 virtual bytes                -> vbytes
  src/consensus/consensus.h     WITNESS_SCALE_FACTOR, COINBASE_MATURITY, MAX_BLOCK_WEIGHT  the constants of the chapter  -> WITNESS_SCALE_FACTOR, COINBASE_MATURITY
  src/primitives/transaction.h  CTxIn::SEQUENCE_FINAL, SEQUENCE_LOCKTIME_DISABLE_FLAG, SEQUENCE_LOCKTIME_TYPE_FLAG, SEQUENCE_LOCKTIME_MASK, SEQUENCE_LOCKTIME_GRANULARITY -> the SEQUENCE_ constants
  src/util/rbf.h                MAX_BIP125_RBF_SEQUENCE (0xfffffffd)                        the opt-in replace signal    -> sequence_decode
  src/consensus/tx_verify.cpp   CalculateSequenceLocks, EvaluateSequenceLocks              BIP68 relative timelock      -> sequence_decode, earliest_block
  src/consensus/tx_verify.cpp   IsFinalTx                                                  the lock time of a transaction -> locktime_decode, locktime_satisfied
  src/script/script.h           LOCKTIME_THRESHOLD (500,000,000)                           height or time               -> LOCKTIME_THRESHOLD
  src/chain.h                   CBlockIndex::GetMedianTimePast                             median of the last 11 block times -> median_time_past
  src/consensus/amount.h        COIN, MAX_MONEY, MoneyRange                                the amount                   -> COIN, MAX_MONEY, money_range
  src/consensus/tx_check.cpp    CheckTransaction ('bad-txns-vout-toolarge', 'bad-txns-txouttotal-toolarge', 'bad-cb-length') the per-output range and the coinbase field -> money_range, coinbase_field_ok
  src/policy/policy.cpp         GetDustThreshold; src/policy/policy.h DUST_RELAY_TX_FEE    the dust limit              -> dust_threshold
  src/validation.cpp            GetBlockSubsidy                                            the subsidy                  -> block_subsidy, total_subsidy, last_subsidy_height
  src/primitives/transaction.h  CTransaction::IsCoinBase                                   the null outpoint            -> is_coinbase
  src/consensus/tx_verify.cpp   CheckTxInputs ('bad-txns-premature-spend-of-coinbase')     coinbase maturity            -> coinbase_mature
  src/script/script.h           CScript::IsWitnessProgram                                  the witness program          -> segwit_output_version
The push encodings (push_encodings) and the two witness helpers (with_input_script, with_witness_item) have no Core counterpart: they build the chapter's demonstrations.
'''
CMT = {
 "def cs_encode(": "# Core: WriteCompactSize (src/serialize.h)", "def cs_decode(": "# Core: ReadCompactSize (src/serialize.h)",
 "def parse_tx(": "# Core: UnserializeTransaction (src/primitives/transaction.h)", "def serialize(": "# Core: SerializeTransaction (src/primitives/transaction.h)",
 "def txid(": "# Core: CTransaction::ComputeHash (src/primitives/transaction.h)", "def wtxid(": "# Core: CTransaction::ComputeWitnessHash (src/primitives/transaction.h)",
 "def weight(": "# Core: GetTransactionWeight (src/consensus/validation.h)", "def vbytes(": "# Core: GetVirtualTransactionSize (src/policy/policy.cpp)",
 "def sequence_decode(": "# Core: the SEQUENCE_ constants of CTxIn (src/primitives/transaction.h), MAX_BIP125_RBF_SEQUENCE (src/util/rbf.h), CalculateSequenceLocks (src/consensus/tx_verify.cpp)",
 "def earliest_block(": "# Core: CalculateSequenceLocks, EvaluateSequenceLocks (src/consensus/tx_verify.cpp)",
 "def locktime_decode(": "# Core: LOCKTIME_THRESHOLD (src/script/script.h), IsFinalTx (src/consensus/tx_verify.cpp)", "def locktime_satisfied(": "# Core: IsFinalTx (src/consensus/tx_verify.cpp)",
 "def median_time_past(": "# Core: CBlockIndex::GetMedianTimePast (src/chain.h)", "def money_range(": "# Core: MoneyRange (src/consensus/amount.h)",
 "def dust_threshold(": "# Core: GetDustThreshold (src/policy/policy.cpp)", "def block_subsidy(": "# Core: GetBlockSubsidy (src/validation.cpp)",
 "def is_coinbase(": "# Core: CTransaction::IsCoinBase (src/primitives/transaction.h)", "def coinbase_field_ok(": "# Core: CheckTransaction, 'bad-cb-length' (src/consensus/tx_check.cpp)",
 "def coinbase_mature(": "# Core: CheckTxInputs, 'bad-txns-premature-spend-of-coinbase' (src/consensus/tx_verify.cpp)", "def segwit_output_version(": "# Core: CScript::IsWitnessProgram (src/script/script.h)",
}
a = 'against the figures of BIP68, BIP141 and Bitcoin Core\'s sources."""\n__version__ = "1.0.0"'
assert src.count(a) == 1
out = src.replace(a, 'against the figures of BIP68, BIP141 and Bitcoin Core\'s sources.\n' + TABLE + '"""\n__version__ = "1.1.0"')
lines = out.split("\n"); res = []; n = 0
for ln in lines:
    for k, c in CMT.items():
        if ln.startswith(k): res.append(c); n += 1; break
    res.append(ln)
assert n == len(CMT), (n, len(CMT))
dst = os.path.join(H, "sen0401_ch06_tx_lib_v1_1_0.py"); assert not os.path.exists(dst)
open(dst, "w", encoding="utf-8").write("\n".join(res)); print("wrote", dst, n, "comments")
