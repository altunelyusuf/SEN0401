"""Every computation the SEN0401 chapter 12 (Mining and Consensus) lecture deck shows. The outputs come from executing these statements, never from typing them:
sen0401_deck_examples_run_v1_0_0.py writes examples_out_v1_0_0.json and the deck reads that file.

PRELUDE loads the chapter's own library (sen0401_ch12_lib_v1_0_0.py: an independent subsidy, target, retarget and header code, and readers of the saved sources) and the saved records it reads:
R is the single run of Bitcoin Core 31.1 on regtest (ch12-evidence/regtest_run; one run, so its values are Recorded on the slides); the real blocks, headers and statistics are public figures from mempool.space,
saved in ch12-evidence on 2026-10-15 (L.jload and L.raw read them). seen(file, text) finds a passage in a saved source, src(file, name) reads a constant from a saved source file, cv(chain, regex) reads a chain parameter
of chainparams.cpp. Rows that read R only read the record; rows that call L.subsidy, L.retarget, L.difficulty, L.bits_to_target, hw and pw compute. The statements are the research package's executed claims
(sen0401_ch12_leaves_v1_0_0.py, research v1_0_1), cut into one-line rows. Every group is named after the slide that shows it. deck_check re-runs every '>>>' line of the finished deck in this same namespace,
so a statement is ONE line."""
__version__ = "1.0.0"
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLING = os.path.abspath(os.path.join(HERE, ".."))

PRELUDE = """
import sys, math, hashlib, datetime
sys.path.insert(0, %r)
import sen0401_ch12_lib_v1_0_0 as L
R = L.run()
src, seen, cv, pw = L.const, L.has, L.chain_value, L.p_attacker_ever_wins
J = lambda n: L.jload('mempool_block_' + str(n) + '.json')
hw = lambda n, w='w': hashlib.sha256(('Hello, ' + w + 'orld! ' + str(n) + chr(10)).encode()).hexdigest()
""" % TOOLING

EX = {
 # ---- part A: money and rewards -------------------------------------------------------------------------------------------
 "Supply": [
  "hs = {n: J(n) for n in (210000, 420000, 630000, 840000)}",
  "[(n, L.iso(b['timestamp'])[:4], f'{L.subsidy(n) / 1e8:g}') for n, b in hs.items()]",
  "L.total_supply(), 2100000000000000 - L.total_supply(), L.subsidy(33 * 210000 - 1), 33 * 210000 - 1",
  "L.book_script_as_printed(), L.total_supply()",
 ],
 "Reward": [
  "r, e, m = R['b5_reward'], J(840000)['extras'], R['b5_modest']",
  "r['coinbasevalue'], r['subsidy'] + r['fees'], r['fees']",
  "e['totalFees'], L.subsidy(840000), round(e['totalFees'] / L.subsidy(840000), 2), e['pool']['name']",
  "m['coinbase_output_sat'], r['coinbasevalue'] - m['coinbase_output_sat'], m['submit']",
  "R['b5_greedy_submit'], R['b4_rules']['reward_one_satoshi_too_high']",
 ],
 "HalvingStory": [
  "b = J(840000); e = b['extras']",
  "b['height'], b['tx_count'], e['totalFees'], e['pool']['name']",
  "round(e['totalFees'] / 3.125e8, 2), e['reward']",
 ],
 # ---- part B: verifying and building a block --------------------------------------------------------------------------------
 "Checks": [
  "c, r = R['b3_tx_checklist'], R['b4_rules']",
  "len(c) - 1, len(r), c['coinbase_100_confirmations']['allowed'], R['b4_tip_is_valid']",
  "[c[k]['reject-reason'] for k in ('duplicate_input', 'negative_output', 'coinbase_99_confirmations')]",
  "[r[k] for k in ('reward_one_satoshi_too_high', 'no_height_in_coinbase', 'merkle_root_wrong')]",
  "[r[k] for k in ('time_equal_to_median_time_past', 'time_two_hours_and_a_second_ahead', 'version_1')]",
 ],
 "ChainSel": [
  "a, b = R['b7_after'], R['b7_before']",
  "int(a['chainwork_tip'], 16), int(a['chainwork_x'], 16), a['tip_is_y2']",
  "b['carol_received'], b['pay_confirmations'], a['pay_confirmations'], a['carol_received']",
  "a['back_confirmations'], [t['status'] for t in a['tips']], R['b7_deliver_y2']",
 ],
 "Coinbase": [
  "t, k, w = R['b1_template0'], R['b5_core_coinbase'], J(840000)['weight']",
  "t['weightlimit'], src('core_src_policy_policy.h', 'DEFAULT_BLOCK_RESERVED_WEIGHT'), 4000000 - 8000, w",
  "L.push_num(k['height']).hex(), k['scriptsig'], k['height']",
  "k['locktime'] == k['height'] - 1, hex(k['sequence']), k['scriptsig'][-2:], k['version']",
 ],
 # ---- part C: proof of work -------------------------------------------------------------------------------------------------
 "Lottery": [
  "h = L.header(L.raw('mempool_header_277316.txt')); t = L.bits_to_target(h['bits'])",
  "next(n for n in range(1, 10 ** 6) if hw(n).startswith('0')), hw(32)[:8], hw(32, 'W')[:8]",
  "[next(n for n in range(1, 10 ** 6) if hw(n).startswith('0' * z)) for z in (2, 3)]",
  "L.leading_zero_bits(h['hash']), 256 - t.bit_length(), int(h['hash'], 16) < t",
 ],
 "Difficulty": [
  "d = L.difficulty('1903a30c'); s = d * 2 ** 32 / 1e12",
  "round(d), round(s / 86400, 1), round(s / 600), round(8496 * 600 / 86400, 1)",
  "d2 = L.jload('mempool_difficulty_adjustments_2y.json')[0][2]; r = L.jload('mempool_hashrate_3m.json')['currentHashrate']",
  "f'{d2 * 2 ** 32 / 600:.3e}', f'{r:.3e}', round(r / (d * 2 ** 32 / 600))",
 ],
 "Retarget": [
  "a, z, n = [L.header(L.raw('mempool_header_%d.txt' % k)) for k in (838656, 840671, 840672)]",
  "z['time'] - a['time'], z['bits'], n['bits'], hex(L.retarget(a['time'], z['time'], z['bits']))",
  "L.retarget(a['time'], z['time'], z['bits']) == int(n['bits'], 16), round(1209600 / (z['time'] - a['time']), 4)",
  "round((2016 / 2015 - 1) * 100, 3), [hex(L.retarget(0, t, '17034219')) for t in (12096000, 120960)]",
 ],
 "Bip94": [
  "R['b2_bits']['2017'], [cv(c, r'fPowNoRetargeting = (\\w+)') for c in ('regtest', 'main')]",
  "[cv(c, r'enforce_BIP94 = (\\w+)') for c in ('testnet4', 'main')]",
  "[seen(f, 'enforce_BIP94') for f in ('core_src_pow.cpp', 'book_ch12_mining.adoc')]",
  "a = L.jload('mempool_difficulty_adjustments_2y.json'); ch = [x[3] for x in a]",
  "len(a), round(min(ch), 3), round(max(ch), 3), sum(1 for c in ch if c < 1)",
 ],
 "HashStory": [
  "seen('back_2002_hashcash.txt', '1st August 2002')",
  "seen('nakamoto_2008_bitcoin.txt', \"similar to Adam Back's Hashcash\")",
  "next(n for n in range(1, 99) if hw(n)[0] == '0'), hw(32)[:8]",
 ],
 # ---- part D: competition and rule changes --------------------------------------------------------------------------------------
 "NonceSpace": [
  "h, v, e = L.jload('mempool_hashrate_3m.json')['currentHashrate'], R['b10_rolled'], R['b5_extranonce']",
  "2 ** 32, f'{h / 2 ** 32:.2e}', f'{2 ** 96:.3e}'",
  "bin(0x1fffe000).count('1'), 2 ** bin(0x1fffe000).count('1'), f'{2 ** 48 / 1e12:.1f}'",
  "v['rolled_bits'], v['versionHex'], v['accepted_height']",
  "e['coinbase_txid_1'] != e['coinbase_txid_2'], e['merkle_1'] != e['merkle_2'], e['nonce_1'] == e['nonce_2']",
 ],
 "Pools": [
  "p = L.jload('mempool_pools_1y.json'); n = sum(q['blockCount'] for q in p['pools'])",
  "n, [(q['name'], round(100 * q['blockCount'] / n, 1)) for q in p['pools'][:4]]",
  "round(100 * sum(q['blockCount'] for q in p['pools'][:4]) / n, 1), len(p['pools'])",
  "round(144 * 0.01, 2), round(144 * 1e-4 * 365, 2), round(1 / (144 * 1e-4))",
 ],
 "Attacks": [
  "[round((1 - g) / (3 - 2 * g), 4) for g in (0, 0.5, 1)]",
  "[round(pw(q, 6), d) for q, d in ((0.1, 7), (0.3, 4), (0.45, 3))]",
  "p = L.jload('mempool_pools_1y.json')['pools']; s = p[0]['blockCount'] / sum(q['blockCount'] for q in p)",
  "p[0]['name'], round(s, 4), s < 1 / 3, s > 1 / 4",
 ],
 "Forks": [
  "r, c, v = R['b9_lax_block'], R['b9_lax_chain'], R['b8_versionbits']['V']['rows']",
  "r['lax_node'], r['strict_node'], c['strict_node_on_block_6'], c['same_tip']",
  "[(x['height'], x['status']) for x in v]",
  "v[1]['statistics']['threshold'], v[1]['statistics']['period'], math.ceil(0.95 * 2016)",
  "cv('main', r'BIP34Height = (\\d+)'), cv('main', r'SegwitHeight = (\\d+)')",
 ],
 "SplitStory": [
  "a, z = J(225430), J(225454)",
  "a['height'], a['tx_count'], a['size'], z['height'] - a['height']",
  "L.blocks_per_period(0.8), L.blocks_per_period(0.2)",
 ],
 "TapStory": [
  "b = J(709632)",
  "b['height'], hex(b['version']), b['extras']['pool']['name']",
  "L.iso(1619222400)[:10], L.iso(1628640000)[:10], 1815 * 100 // 2016",
 ],
}
