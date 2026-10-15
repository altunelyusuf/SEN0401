"""Every computation the SEN0401 chapter 9 (Transaction Fees) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch09_lib_v1_0_0.py: an independent transaction parser, the rules of the chapter as functions, readers of the saved sources) and the
three saved records it reads: R and R2 are the two runs of Bitcoin Core 31.1 on regtest (ch09-evidence/regtest_run and regtest2_run; one run each, so their values are Recorded on the
slides), C is the census of two mainnet blocks (840,000 and 971,489, saved on 2026-10-15). Rows that read R or R2 only read the record; rows that call L.parse_tx, L.rbf_signal,
L.min_replacement_fee, L.snipe_probability and so on compute. The statements are the research package's executed claims (sen0401_ch09_leaves_v1_0_0.py), cut into one-line rows.
Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace, so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, json
sys.path.insert(0, %r)
import sen0401_ch09_lib_v1_0_0 as L
R = L.run(); R2 = L.run2(); C = L.census(); B = C['blocks']
why, src, seen, kvb = L.reason, L.const, L.has, L.btc_kvb_to_sat_vb
A = R['ancestor_mining']
mined = lambda q, k: q[k]['txid'] in q['block_txids']
chunk = lambda q: q['mempoolentries']['P']
X = R['rbf']
""" % TOOLING

EX = {
 # ---- part A: what a fee is, how it is priced ---------------------------------------------------------------------------
 "FeeDiff": [
  "t, a, w = L.parse_tx(R['fee_arith']['tx']['hex']), R['fee_arith'], R2['tamper']",
  "'fee' in t, sorted(k for k in t if k in ('version', 'vin', 'vout', 'locktime'))",
  "round(a['inputs_btc'] * 10 ** 8) - sum(o['value'] for o in t['vout'])",
  "a['testmempoolaccept']['reject-reason']",
  "[w[k]['allowed'] for k in ('original', 'tampered')], w['tampered']['reject-reason'][:36]",
 ],
 "SizeRate": [
  "x, u, t = R['rbf']['t1'], R['units'], L.parse_tx(R['rbf']['t1']['hex'])",
  "t['base_size'], t['size'], t['weight'], t['vsize']",
  "x['fee_sat'] / x['vsize'], round(x['vsize'] / x['weight'], 4)",
  "float(kvb('0.00006570')), float(kvb('0.00001225'))",
  "u['fee_rate_sat_vb_10']['ok']['fee'] == u['feeRate_btc_kvb_0.0001']['ok']['fee']",
  "src('core_src_consensus_consensus.h', 'MAX_BLOCK_WEIGHT'), B['840000']['weight']",
 ],
 "MinFees": [
  "m, d, w = R['minrelay'], R2['dust'], R2['wallet_min']",
  "[(v['fee_sat'], v['result']['ok'][0]['allowed']) for v in list(m.values())[:3]]",
  "R2['mempool_min']['minrelaytxfee'] * 10 ** 8 / 1000",
  "['ok' in w[k] for k in ('fee_rate_0.5', 'fee_rate_0.1', 'fee_rate_1')]",
  '(31 + 67) * 3, (43 + 67) * 3, (13 + 67) * 3',
  "[d[k]['result']['allowed'] for k in list(d)[:6]]",
 ],
 # ---- part B: estimating and the market -------------------------------------------------------------------------------
 "Estimator": [
  "E = R['estimate']['results']",
  "R['estimate_fresh']['ok']['errors'][0], R['estimate']['rounds'], R['estimate']['sent']",
  "[round(E[k]['ok']['feerate'] * 10 ** 8 / 1000, 3) for k in ('2_default', '6_default', '25_default')]",
  "E['144_default']['ok']['blocks'], R['estimate']['tip']",
  "all(E[f'{t}_default'] == E[f'{t}_economical'] for t in (2, 6, 25, 144))",
  "E['144_default'] == E['144_conservative']",
 ],
 "Census": [
  'a, b = L.census_stats(840000), L.census_stats(971489)',
  "a['n'], a['median_rate'], b['median_rate']",
  "[round(100 * B[h]['extras']['totalFees'] / B[h]['extras']['reward'], 2) for h in ('840000', '971489')]",
  "[round(100 * z['signal_rbf'] / z['n']) for z in (a, b)]",
  "[round(100 * z['locktime_prev_height'] / z['n']) for z in (a, b)]",
 ],
 "Halving": [
  "e, g = B['840000']['extras'], B['971489']['extras']",
  "e['totalFees'], e['reward'], e['reward'] - e['totalFees']",
  "[round(100 * z['totalFees'] / z['reward'], 2) for z in (e, g)]",
 ],
 # ---- part C: replace, bump, pin -------------------------------------------------------------------------------------------
 "RbfRules": [
  "L.rbf_signal([0xfffffffd]), L.rbf_signal([0xfffffffe]), L.rbf_signal([0xffffffff, 0xfffffffd])",
  "X['lower_fee']['fee_sat'], 'less fees than conflicting txs' in why(X['lower_fee']['result'])",
  "X['equal_fee']['fee_sat'], 'not enough additional fees to relay' in why(X['equal_fee']['result'])",
  "L.min_replacement_fee(564, 141), X['short_by_one']['fee_sat'], 'error' in X['short_by_one']['result']",
  "X['exactly_enough']['fee_sat'], 'ok' in X['exactly_enough']['result']",
 ],
 "FullRbf": [
  "x, o = R['rbf'], R2['removed_option']",
  "x['fullrbf_flag'], x['t1']['sequence'], 'ok' in x['t2']['result']",
  "o['exit_code'], 'Invalid parameter -mempoolfullrbf=0' in o['message']",
  "[L.census_stats(h)['signal_rbf'] for h in (840000, 971489)]",
 ],
 "Hazards": [
  "h, p, i = R2['hazard'], R['pinning']['v2'], R2['hazard']['inputs']",
  "h['payee_asked_sat'], h['payee_received_sat']",
  "L.conflict(i['v0'], i['v1']), L.conflict(i['v1'], i['v2']), L.conflict(i['v0'], i['v2'])",
  "p['child']['vsize'], p['replacement_enough']['fee_sat'], p['parent']['fee_sat']",
  "round(p['replacement_enough']['fee_sat'] / p['parent']['fee_sat'])",
  "seen('optech_topic_replacement_cycling.html', 'especially concerning in protocols that use')",
 ],
 "Cpfp": [
  "a, l, p = A['cpfp_wins'], A['cpfp_loses'], R['package']",
  "a['fees_sat']['P'], a['fees_sat']['C'], mined(a, 'P'), mined(a, 'C')",
  "round(chunk(a)['fees']['chunk'] * 10 ** 8 / (chunk(a)['chunkweight'] / 4), 2)",
  "round((l['fees_sat']['P'] + l['fees_sat']['C']) / (chunk(l)['chunkweight'] / 4), 2), mined(l, 'A'), mined(l, 'P')",
  "p['v2_parent']['fee_sat'], why(p['child_alone']), p['submitpackage_v2']['ok']['package_msg']",
 ],
 # ---- part D: pinning, anchors, clusters, sniping --------------------------------------------------------------------------
 "Truc": [
  "v2, v3, t = R['pinning']['v2'], R['pinning']['v3'], R['truc']",
  "v2['child']['vsize'], v2['replacement_enough']['fee_sat']",
  "v3['child']['vsize'], v3['replacement_enough']['fee_sat']",
  "round(v2['replacement_enough']['fee_sat'] / v3['replacement_enough']['fee_sat'])",
  "t['big_child']['vsize'], 'TRUC-violation' in why(t['big_child']['result'])",
  "t['child1']['vsize'], 'ok' in t['child1']['result']",
  "'sibling eviction' in why(t['sibling_same_rate']['result']), 'ok' in t['sibling_higher_rate']['result']",
 ],
 "Anchors": [
  "p = R['package']; t, c = L.parse_tx(p['truc_parent']['hex']), L.parse_tx(p['anchor_child']['hex'])",
  "t['vout'][0]['spk'], t['vout'][0]['value'], t['version']",
  "why(p['parent_alone']), p['submitpackage_truc']['ok']['package_msg']",
  "[v['witness'] for v in c['vin']].count([]), p['anchor_child']['fee_sat']",
  "f = list(p['submitpackage_truc']['ok']['tx-results'].values())[0]['fees']",
  "round(f['effective-feerate'] * 10 ** 8 / 1000, 1)",
 ],
 "CarveOut": [
  "src('core_src_policy_policy.h', 'EXTRA_DESCENDANT_TX_SIZE_LIMIT')",
  "seen('book_ch09_fees.adoc', 'additional transaction up to 1,000 vbytes')",
  "seen('ml_corallo_2018-12_carveout.html', 'no greater than 1K')",
  "seen('core_relnotes_31.0.html', 'removed from the mempool logic')",
 ],
 "Cluster": [
  "c, o = R['cluster'], 'core_src_kernel_mempool_options.h'",
  "c['mempoolinfo']['limitclustercount'], c['mempoolinfo']['limitclustersize']",
  "c['chain']['attempted'], c['chain']['accepted'], why(c['chain']['first_refusal'])",
  "c['chain']['accepted_26th'], 25 ** 2, 50 ** 2",
  "src(o, 'DEFAULT_MAX_MEMPOOL_SIZE_MB'), src(o, 'DEFAULT_MEMPOOL_EXPIRY_HOURS')",
  "seen('core_relnotes_31.0.html', 'removed from the mempool logic')",
 ],
 "Sniping": [
  "s = R['sniping']['samples']; d = sorted(z['tip'] - z['locktime'] for z in s)",
  "len(s), d.count(0), [z for z in d if z]",
  "L.is_final(100001, 100001, [0xfffffffd]), R2['locktime_block']['mempool_next']['reject-reason']",
  "[round(100 * L.snipe_probability(x), 2) for x in (0.1, 0.3, 0.45)]",
  "[L.census_stats(h)['locktime_prev_height'] for h in (840000, 971489)]",
  "seen('bip-0326.mediawiki', 'in place of their regular nLockTime anti-fee-sniping protection')",
 ],
 "Instability": [
  "seen('nakamoto_2008_bitcoin.pdf', 'added to the incentive value')",
  "seen('carlsten_2016_instability.pdf', 'actively fork the head of the')",
  'round(100 * L.snipe_probability(0.45), 2), L.snipe_probability(0.5)',
 ],
}
